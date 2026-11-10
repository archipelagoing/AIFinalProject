// Shared by the browser and Node tests. No evaluation fixtures or remote services.
export const TYPES = ['income', 'expense', 'refund', 'transfer', 'unknown'];
export const CATEGORIES = ['Housing', 'Groceries', 'Restaurants', 'Utilities', 'Phone', 'Internet', 'Insurance', 'Transportation', 'Subscriptions', 'Fitness', 'Health', 'Shopping', 'Auto maintenance', 'Debt payment', 'Income', 'Transfer', 'Uncategorized'];
export const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
export const emptyState = () => ({ version: 1, imports: [], transactions: [] });
const sum = values => values.reduce((a, b) => exact(a + b), 0);
function exact(n) {
  if (!Number.isSafeInteger(n)) throw new Error('Amount exceeds the supported exact-integer range.');
  return n;
}
export function parseMoney(value) {
  if (typeof value !== 'string' || !/^[+-]?\d+(?:\.\d{1,2})?$/.test(value.trim())) {
    throw new Error('Use a signed decimal amount, such as -1275.00; no currency symbols or commas.');
  }
  const s = value.trim(), negative = s.startsWith('-');
  const [whole, fraction = ''] = s.replace(/^[+-]/, '').split('.');
  const cents = BigInt(whole) * 100n + BigInt(fraction.padEnd(2, '0'));
  if (cents > BigInt(Number.MAX_SAFE_INTEGER)) throw new Error('Amount is too large.');
  return negative ? -Number(cents) : Number(cents);
}
export function money(cents) {
  exact(cents);
  const n = Math.abs(cents);
  return `${cents < 0 ? '−' : ''}$${Math.floor(n / 100).toLocaleString('en-US')}.${String(n % 100).padStart(2, '0')}`;
}
export function monthName(month) {
  return `${MONTHS[Number(month.slice(5)) - 1]} ${month.slice(0, 4)}`;
}
export function parseCSV(text) {
  if (typeof text !== 'string' || text.includes('\uFFFD')) throw new Error('Save the CSV as UTF-8 and try again.');
  text = text.replace(/^\uFEFF/, '');
  const rows = []; let row = [], cell = '', quoted = false, closed = false;
  const finishCell = () => { row.push(cell); cell = ''; closed = false; };
  const finishRow = () => { finishCell(); if (row.some(x => x !== '')) rows.push(row); row = []; };
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; }
      else if (c === '"') { quoted = false; closed = true; }
      else cell += c;
    } else if (c === '"') {
      if (cell || closed) throw new Error('Malformed CSV: unexpected quote.');
      quoted = true;
    } else if (c === ',') finishCell();
    else if (c === '\n' || c === '\r') { if (c === '\r' && text[i + 1] === '\n') i++; finishRow(); }
    else { if (closed) throw new Error('Malformed CSV: text after closing quote.'); cell += c; }
  }
  if (quoted) throw new Error('Malformed CSV: an opening quote has no closing quote.');
  if (cell || row.length || closed) finishRow();
  return rows;
}
export function classify(description, amount) {
  const d = description.toUpperCase();
  const label = (type, category, rule) => ({ predicted_type: type, predicted_category: category, rule });
  if (/SAVINGS TRANSFER/.test(d)) return label('transfer', 'Transfer', 'Savings transfer description; excluded from spending and income.');
  if (/VENMO FRIEND DINNER (SPLIT|REIMBURSEMENT)/.test(d)) return label('transfer', 'Transfer', 'Peer dinner transfer; not wages. Confirm its treatment during review.');
  if (amount > 0 && /PAYROLL|FREELANCE/.test(d)) return label('income', 'Income', 'Positive payroll or freelance payment.');
  if (amount > 0 && /SHOPRITE RETURN/.test(d)) return label('refund', 'Groceries', 'Grocery return reduces grocery expenses.');
  const rules = [
    [/APARTMENTS RENT/, 'Housing'], [/ALDI|SHOPRITE|TRADER JOES/, 'Groceries'],
    [/THAI BASIL|SUSHI MARKET|CHIPOTLE|STARBUCKS/, 'Restaurants'],
    [/UTILITIES/, 'Utilities'], [/VERIZON/, 'Phone'], [/COMCAST/, 'Internet'],
    [/GEICO/, 'Insurance'], [/WAWA FUEL|SHELL GAS/, 'Transportation'],
    [/NETFLIX|SPOTIFY/, 'Subscriptions'], [/PLANET FITNESS/, 'Fitness'],
    [/CVS PHARMACY/, 'Health'], [/AMAZON/, 'Shopping'], [/CAR REPAIR/, 'Auto maintenance'],
    [/STUDENT LOAN/, 'Debt payment']
  ];
  if (amount < 0) for (const [pattern, category] of rules) {
    if (pattern.test(d)) return label('expense', category, `Description matches ${pattern.source}.`);
  }
  return label('unknown', 'Uncategorized', 'No reliable rule matched. Review before including in verified totals.');
}
function validDate(date) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return false;
  const n = Date.parse(`${date}T00:00:00Z`);
  return Number.isFinite(n) && new Date(n).toISOString().slice(0, 10) === date;
}
const fingerprint = t => JSON.stringify([t.account, t.date, t.description, t.amount_cents]);
const sourceKey = t => t.source_transaction_id ? JSON.stringify([t.account, t.source_transaction_id]) : null;
export async function importCSV(state, text, filename) {
  // Stage the entire import; the caller persists the returned state in one write.
  const digestBytes = await globalThis.crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  const digest = [...new Uint8Array(digestBytes)].map(n => n.toString(16).padStart(2, '0')).join('');
  if (state.imports.some(x => x.digest === digest)) return { state, added: 0, duplicate: true, message: 'This exact statement is already imported, even if its filename changed. No rows added.' };
  const rows = parseCSV(text);
  if (rows.length < 2) throw new Error('The CSV needs a header and at least one transaction. No rows imported.');
  const headers = rows[0].map(s => s.trim());
  const required = ['date', 'description', 'amount', 'account', 'transaction_id'];
  if (new Set(headers).size !== headers.length || required.some(h => !headers.includes(h))) throw new Error(`Required unique columns: ${required.join(',')}. No rows imported.`);
  const known = new Map(state.transactions.map(t => [sourceKey(t), t]).filter(([k]) => k));
  const previousFingerprints = new Set(state.transactions.map(fingerprint));
  const batchKeys = new Set();
  const staged = rows.slice(1).map((cells, index) => {
    const ordinal = index + 2;
    try {
      if (cells.length !== headers.length) throw new Error('Column count does not match the header.');
      const original = Object.fromEntries(headers.map((h, i) => [h, cells[i]]));
      const date = original.date.trim(), description = original.description.trim(), account = original.account.trim();
      if (!validDate(date)) throw new Error('Date must be a real calendar date in YYYY-MM-DD format.');
      if (!description || !account) throw new Error('Description and account must not be empty.');
      const amount_cents = parseMoney(original.amount);
      const t = { id: `${digest}:${ordinal}`, import_id: digest, source_row_number: ordinal, source_transaction_id: original.transaction_id.trim(), date, description, account, amount_cents, original_row_json: original, ...classify(description, amount_cents), corrected_type: null, corrected_category: null, reviewed: false };
      const key = sourceKey(t);
      if (key && batchKeys.has(key)) throw new Error('Repeated transaction ID within this account. Review the source file.');
      if (key) batchKeys.add(key);
      if (key && known.has(key)) {
        const same = fingerprint(known.get(key)) === fingerprint(t);
        throw new Error(same ? 'Overlapping statement: this source transaction already exists. Review overlap before importing.' : 'Conflicting source ID: an existing transaction has different values. Review the source file.');
      }
      if (previousFingerprints.has(fingerprint(t))) throw new Error('Possible cross-file duplicate: identical account/date/description/amount. Review before importing.');
      return t;
    } catch (error) { throw new Error(`Row ${ordinal}: ${error.message} No rows imported.`); }
  });
  const next = { ...state, imports: [...state.imports, { id: digest, digest, filename, count: staged.length, created_at: new Date().toISOString() }], transactions: [...state.transactions, ...staged] };
  // Catch an exact-integer overflow before any persistence.
  for (const month of months(next.transactions)) summarize(next.transactions, month);
  return { state: next, added: staged.length, duplicate: false, message: `${staged.length} transactions accepted; 0 rejected. Original rows preserved.` };
}
export const effective = t => ({ ...t, type: t.corrected_type ?? t.predicted_type, category: t.corrected_category ?? t.predicted_category });
export const months = transactions => [...new Set(transactions.map(t => t.date.slice(0, 7)))].sort();
export function correctTransaction(state, id, type, category, reset = false) {
  const row = state.transactions.find(t => t.id === id);
  if (!row) throw new Error('Transaction not found.');
  if (!TYPES.includes(type) || !category.trim() || category.length > 80) throw new Error('Choose a valid type and a category of 1–80 characters.');
  if ((type === 'income' || type === 'refund') && row.amount_cents <= 0) throw new Error('Income and refunds require a positive source amount.');
  if (type === 'expense' && row.amount_cents >= 0) throw new Error('Expenses require a negative source amount.');
  const next = { ...state, transactions: state.transactions.map(t => t.id === id ? { ...t, corrected_type: reset ? null : type, corrected_category: reset ? null : category.trim(), reviewed: !reset } : t) };
  summarize(next.transactions, row.date.slice(0, 7));
  return next;
}
export function summarize(transactions, month) {
  const rows = transactions.filter(t => t.date.startsWith(`${month}-`)).map(effective);
  const incomeRows = rows.filter(t => t.type === 'income');
  const expenseRows = rows.filter(t => t.type === 'expense' || t.type === 'refund');
  const unknown = rows.filter(t => t.type === 'unknown');
  const transfers = rows.filter(t => t.type === 'transfer');
  const income = sum(incomeRows.map(t => t.amount_cents));
  const expenses = sum(expenseRows.map(t => -t.amount_cents));
  const categories = Object.create(null);
  for (const t of expenseRows) categories[t.category] = exact((categories[t.category] ?? 0) - t.amount_cents);
  const dates = rows.map(t => t.date).sort();
  const warnings = [];
  if (rows.length) warnings.push(`Activity dates ${dates[0]}–${dates.at(-1)}. Full statement coverage is unverified; this month may be incomplete.`);
  if (unknown.length) warnings.push(`${unknown.length} unresolved transaction(s), ${money(sum(unknown.map(t => Math.abs(t.amount_cents))))} in absolute value, excluded from verified totals.`);
  const transferGroups = new Map();
  for (const t of transfers) {
    const k = `${t.date}:${Math.abs(t.amount_cents)}`;
    if (!transferGroups.has(k)) transferGroups.set(k, []);
    transferGroups.get(k).push(t);
  }
  const unmatched = [...transferGroups.values()].some(group => group.length !== 2 || group[0].account === group[1].account || sum(group.map(t => t.amount_cents)) !== 0);
  if (unmatched) warnings.push('Some transfers have no unique matching entry in another imported account. Transfer evidence is limited.');
  return { month, rows, incomeRows, expenseRows, unknown, transfers, income, expenses, surplus: exact(income - expenses), categories, warnings, reviewed: rows.filter(t => t.reviewed).length };
}
export function calculateScenario({ baseline, newRent, mode, existingRent, addedSpending = 0, incomeAdjustment = 0 }) {
  for (const value of [baseline, newRent, addedSpending, incomeAdjustment]) exact(value);
  if (newRent < 0 || addedSpending < 0) throw new Error('Rent and added spending must be nonnegative.');
  if (!['replace', 'additional'].includes(mode)) throw new Error('Choose replacement or additional rent.');
  if (mode === 'replace' && (!Number.isSafeInteger(existingRent) || existingRent < 0)) throw new Error('Confirm the existing rent already included in this baseline.');
  const rentDelta = mode === 'replace' ? exact(newRent - existingRent) : newRent;
  const projected = exact(exact(exact(baseline + incomeAdjustment) - addedSpending) - rentDelta);
  return { rentDelta, projected, change: exact(projected - baseline), sixMonths: exact(6 * projected) };
}
export function rentCandidates(summary) {
  return summary.rows.filter(t => t.type === 'expense' && t.category === 'Housing' && /\bRENT\b/i.test(t.description));
}
export function getIncome(transactions, month) {
  const s = summarize(transactions, month);
  return { amount: s.income, rows: s.incomeRows, calculation: 'Sum of classified income', summary: s };
}
export function getExpenses(transactions, month) {
  const s = summarize(transactions, month);
  return { amount: s.expenses, rows: s.expenseRows, calculation: 'Expenses minus refunds', summary: s };
}
export function getCategorySpending(transactions, month, category) {
  const s = summarize(transactions, month);
  return { amount: s.categories[category] ?? 0, rows: s.expenseRows.filter(t => t.category === category), calculation: `${category} expenses minus ${category} refunds`, summary: s };
}
export function getLargestExpenses(transactions, month, n = 5) {
  if (!Number.isInteger(n) || n < 1 || n > 20) throw new Error('Choose between 1 and 20 largest expenses.');
  const s = summarize(transactions, month);
  const rows = s.rows.filter(t => t.type === 'expense').sort((a, b) => a.amount_cents - b.amount_cents || a.date.localeCompare(b.date)).slice(0, n);
  return { amount: sum(rows.map(t => -t.amount_cents)), rows, calculation: `Sum of the ${rows.length} largest expense transactions`, summary: s };
}
export function getSurplus(transactions, month) {
  const s = summarize(transactions, month);
  return { amount: s.surplus, rows: [...s.incomeRows, ...s.expenseRows], calculation: `${money(s.income)} income − ${money(s.expenses)} net expenses`, summary: s };
}
export function askQuestion(transactions, question, selectedMonth) {
  let q = question.trim().toLowerCase().replace(/[?!.]+$/, '');
  if (!q) throw new Error('Enter a question or choose an example.');
  const available = months(transactions); let month = selectedMonth;
  // Reject unknown phrasing instead of silently ignoring part of a request.
  const suffix = q.match(/\s+(?:in|for)\s+(\d{4}-\d{2}|[a-z]+(?:\s+\d{4})?)$/);
  if (suffix) {
    const period = suffix[1]; q = q.slice(0, suffix.index);
    if (/^\d{4}-\d{2}$/.test(period)) month = period;
    else {
      const match = period.match(/^([a-z]+)(?:\s+(\d{4}))?$/);
      const m = MONTHS.findIndex(x => x.toLowerCase() === match[1]);
      if (m < 0) throw new Error('Use a month name and year, such as May 2026, or YYYY-MM.');
      const candidates = available.filter(x => Number(x.slice(5)) === m + 1 && (!match[2] || x.startsWith(match[2])));
      if (candidates.length !== 1) throw new Error('That month is missing or ambiguous. Include a year with imported data.');
      month = candidates[0];
    }
  }
  if (!available.includes(month)) throw new Error('Import a statement for that month first.');
  let result;
  if (/^(how much did i earn|what (?:was|is) my income|income)$/.test(q)) result = getIncome(transactions, month);
  else if (/^(what (?:were|are) my expenses|how much did i spend|expenses)$/.test(q)) result = getExpenses(transactions, month);
  else if (/^(what (?:was|is) my surplus|surplus)$/.test(q)) result = getSurplus(transactions, month);
  else {
    const largest = q.match(/^(?:what were my |show (?:my )?)?(?:(\d+|one|two|three|four|five|ten) )?largest expenses$/);
    const category = q.match(/^(?:how much did i spend on |spending on )(.+)$/);
    if (largest) {
      const words = { one: 1, two: 2, three: 3, four: 4, five: 5, ten: 10 };
      result = getLargestExpenses(transactions, month, words[largest[1]] ?? Number(largest[1] ?? 5));
    } else if (category) {
      const cats = [...new Set([...CATEGORIES, ...transactions.map(t => effective(t).category)])];
      const found = cats.find(x => x.toLowerCase() === category[1]);
      if (!found) throw new Error('Choose an existing category, such as Restaurants or Groceries.');
      result = getCategorySpending(transactions, month, found);
    } else throw new Error('Supported questions: income, expenses, category spending, largest expenses, and surplus. Try an example below.');
  }
  return { ...result, month };
}
