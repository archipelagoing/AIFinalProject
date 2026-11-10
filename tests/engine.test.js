import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { emptyState, parseMoney, parseCSV, importCSV, summarize, classify, effective, correctTransaction, calculateScenario, rentCandidates, askQuestion, getIncome, getExpenses, getCategorySpending, getLargestExpenses, getSurplus } from '../docs/engine.js';
import { loadState, saveState, clearState, STORAGE_KEY } from '../docs/storage.js';
const fixture = name => readFile(new URL(`../CompassProto1.0/${name}`, import.meta.url), 'utf8');
const checking = await fixture('synthetic_checking_2026_Jan-Jun.csv');
const savings = await fixture('synthetic_savings_2026_Jan-Jun.csv');
const expected = JSON.parse(await fixture('expected_monthly_totals.json'));
const truth = parseCSV(await fixture('synthetic_ground_truth.csv')).slice(1);
const checkingState = (await importCSV(emptyState(), checking, 'checking.csv')).state;
const state = (await importCSV(checkingState, savings, 'savings.csv')).state;
const header = 'date,description,amount,account,transaction_id\n';

test('money parsing is exact, signed, and rejects ambiguous and unsafe values', () => {
  for (const [input, cents] of [['0', 0], ['-1275.00', -127500], ['24.99', 2499], ['+0.01', 1], [' 10.5 ', 1050]]) assert.equal(parseMoney(input), cents);
  for (const input of ['', 'NaN', 'Infinity', '1e3', '$20', '1,200.00', '1.001', '.50', '1.', '900719925474099.99']) assert.throws(() => parseMoney(input));
});
test('CSV supports BOM, CRLF, quoted commas, escaped quotes, and newlines', () => {
  assert.deepEqual(parseCSV('\uFEFFa,b\r\n"hello, world","a""b"\r\n"two\nlines",ok'), [['a', 'b'], ['hello, world', 'a"b'], ['two\nlines', 'ok']]);
  for (const input of ['a,b\n"broken,b', 'a,b\n"x"extra,b', 'a,b\nx"y,b']) assert.throws(() => parseCSV(input));
});
test('fixture audit: 164 rows and all classifications match independent test oracle', () => {
  assert.equal(state.transactions.length, 164);
  assert.equal(checkingState.transactions.length, 158);
  assert.equal(truth.length, 164);
  for (const [id, type, category] of truth) {
    const t = state.transactions.find(x => x.source_transaction_id === id);
    assert.ok(t, id);
    assert.equal(t.predicted_type, type, `${id} type`);
    assert.equal(t.predicted_category, category, `${id} category`);
  }
});
test('all six monthly totals match expected JSON in exact cents', () => {
  for (const [month, values] of Object.entries(expected)) {
    const s = summarize(state.transactions, month);
    assert.equal(s.income, parseMoney(String(values.income)), `${month} income`);
    assert.equal(s.expenses, parseMoney(String(values.expenses_net_of_refunds)), `${month} expenses`);
    assert.equal(s.surplus, parseMoney(String(values.surplus_before_transfers_and_unknown)), `${month} surplus`);
    assert.equal(s.transfers.reduce((n, t) => n + t.amount_cents, 0), 0);
    assert.equal(s.unknown.reduce((n, t) => n + t.amount_cents, 0), parseMoney(String(values.unknown_net_excluded)));
    assert.equal(Object.values(s.categories).reduce((a, b) => a + b, 0), s.expenses);
  }
});
test('refunds offset categories, unknown ATM remains excluded, transfers require matching evidence', () => {
  const april = summarize(state.transactions, '2026-04');
  assert.ok(april.expenseRows.some(t => t.type === 'refund' && t.category === 'Groceries' && t.amount_cents === 2499));
  const june = summarize(state.transactions, '2026-06');
  assert.equal(june.unknown.length, 1); assert.equal(june.unknown[0].amount_cents, -8000);
  assert.equal(june.surplus, 171145); assert.ok(june.warnings.some(x => x.includes('unresolved')));
  assert.ok(summarize(checkingState.transactions, '2026-05').warnings.some(x => x.includes('matching entry')));
  assert.ok(!summarize(state.transactions, '2026-05').warnings.some(x => x.includes('matching entry')));
  assert.equal(classify('UNFAMILIAR MERCHANT', -1234).predicted_type, 'unknown');
});
test('same-file and renamed reimport are idempotent and preserve corrections', async () => {
  const t = state.transactions[0];
  const edited = correctTransaction(state, t.id, 'expense', 'Custom rent');
  const result = await importCSV(edited, checking, 'renamed.csv');
  assert.equal(result.duplicate, true); assert.equal(result.added, 0);
  assert.equal(result.state.transactions.length, 164);
  assert.equal(effective(result.state.transactions[0]).category, 'Custom rent');
});
test('distinct identical purchases survive, including missing source IDs', async () => {
  for (const ids of [['a', 'b'], ['', '']]) {
    const csv = header + ids.map(id => `2026-05-01,CHIPOTLE,-10.00,Checking,${id}`).join('\n');
    const result = await importCSV(emptyState(), csv, 'repeat.csv');
    assert.equal(result.added, 2); assert.notEqual(result.state.transactions[0].id, result.state.transactions[1].id);
  }
});
test('invalid imports reject atomically with row number and reason', async () => {
  const initial = JSON.stringify(state);
  for (const bad of ['2026-02-30,CHIPOTLE,-12.00,Checking,b', '05/01/2026,CHIPOTLE,-12,Checking,b', '2026-05-01,CHIPOTLE,NaN,Checking,b', '2026-05-01,CHIPOTLE,-1.001,Checking,b', '2026-05-01,CHIPOTLE,-12,,b', '2026-05-01,CHIPOTLE,-12,Checking']) {
    await assert.rejects(importCSV(state, header + '2026-05-01,CHIPOTLE,-9.00,Test,new\n' + bad, 'bad.csv'), /Row 3:/);
    assert.equal(JSON.stringify(state), initial);
  }
  for (const bad of ['', 'date,amount\n2026-05-01,-1', header, 'a,b\n\uFFFD,x']) await assert.rejects(importCSV(state, bad, 'bad.csv'));
});
test('overlap, conflicting IDs, repeated IDs and cross-file possible duplicates block entire import', async () => {
  const first = (await importCSV(emptyState(), header + '2026-05-01,CHIPOTLE,-10,Checking,a', 'a.csv')).state;
  for (const [row, reason] of [
    ['2026-05-01,CHIPOTLE,-10.00,Checking,a', /Overlapping/],
    ['2026-05-02,CHIPOTLE,-11,Checking,a', /Conflicting/],
    ['2026-05-01,CHIPOTLE,-10,Checking,b', /Possible cross-file duplicate/]
  ]) await assert.rejects(importCSV(first, header + row, 'b.csv'), reason);
  await assert.rejects(importCSV(emptyState(), header + '2026-05-01,CHIPOTLE,-10,Checking,a\n2026-05-02,CHIPOTLE,-12,Checking,a', 'a.csv'), /Repeated transaction ID/);
  const separateAccount = await importCSV(first, header + '2026-05-01,CHIPOTLE,-10,Savings,a', 'b.csv');
  assert.equal(separateAccount.added, 1);
});
test('corrections update reports and retain immutable original values', () => {
  const t = summarize(state.transactions, '2026-06').unknown[0];
  const before = JSON.stringify(t.original_row_json);
  const next = correctTransaction(state, t.id, 'expense', 'Shopping');
  assert.equal(summarize(next.transactions, '2026-06').surplus, 163145);
  const corrected = next.transactions.find(x => x.id === t.id);
  assert.equal(JSON.stringify(corrected.original_row_json), before);
  assert.equal(corrected.amount_cents, -8000); assert.equal(corrected.predicted_type, 'unknown');
  assert.equal(summarize(correctTransaction(next, t.id, 'unknown', 'Uncategorized', true).transactions, '2026-06').surplus, 171145);
  assert.throws(() => correctTransaction(state, t.id, 'income', 'Income'), /positive/);
  assert.throws(() => correctTransaction(state, t.id, 'expense', ''), /category/);
});
test('What If covers all exact May scenarios and both rent interpretations', () => {
  const s = summarize(state.transactions, '2026-05');
  const existingRent = -rentCandidates(s)[0].amount_cents;
  const base = { baseline: s.surplus, existingRent, mode: 'replace', newRent: 150000 };
  assert.equal(existingRent, 127500);
  assert.equal(calculateScenario({ ...base, newRent: existingRent }).projected, 74706);
  assert.deepEqual(calculateScenario(base), { rentDelta: 22500, projected: 52206, change: -22500, sixMonths: 313236 });
  assert.deepEqual(calculateScenario({ ...base, mode: 'additional' }), { rentDelta: 150000, projected: -75294, change: -150000, sixMonths: -451764 });
  assert.equal(calculateScenario({ ...base, newRent: 100000 }).projected, 102206);
  assert.equal(calculateScenario({ ...base, addedSpending: 10000, incomeAdjustment: 20000 }).projected, 62206);
  assert.equal(calculateScenario({ ...base, incomeAdjustment: -20000 }).projected, 32206);
  assert.equal(calculateScenario({ ...base, mode: 'additional', existingRent: null }).projected, -75294);
  for (const patch of [{ newRent: -1 }, { newRent: NaN }, { newRent: Infinity }, { newRent: 1.2 }, { addedSpending: -1 }, { existingRent: null }, { existingRent: -1 }, { mode: '' }, { baseline: Number.MAX_SAFE_INTEGER }]) assert.throws(() => calculateScenario({ ...base, ...patch }));
});
test('rent detection uses effective rent expenses, never the full Housing category', () => {
  const rent = rentCandidates(summarize(state.transactions, '2026-05'))[0];
  const changed = correctTransaction(state, rent.id, 'expense', 'Shopping');
  assert.equal(rentCandidates(summarize(changed.transactions, '2026-05')).length, 0);
});
test('five question tools return precise amounts and evidence rows', () => {
  const transactions = state.transactions, month = '2026-05';
  assert.equal(getIncome(transactions, month).amount, 370000);
  assert.equal(getExpenses(transactions, month).amount, 295294);
  assert.equal(getSurplus(transactions, month).amount, 74706);
  const cat = getCategorySpending(transactions, month, 'Restaurants');
  assert.ok(cat.rows.length); assert.equal(cat.amount, cat.rows.reduce((n, t) => n - t.amount_cents, 0));
  const large = getLargestExpenses(transactions, month, 5);
  assert.equal(large.rows.length, 5); assert.equal(large.rows[0].amount_cents, -127500);
  assert.ok(large.rows.every((t, i, rows) => !i || rows[i - 1].amount_cents <= t.amount_cents));
  for (const q of ['How much did I earn in May 2026?', 'What were my expenses in May?', 'How much did I spend on restaurants in April?', 'What were my five largest expenses in May?', 'What was my surplus in June?']) {
    const result = askQuestion(transactions, q, month);
    assert.ok(result.rows.length); assert.ok(result.calculation);
    assert.ok(result.rows.every(t => t.date.startsWith(result.month)));
  }
});
test('question routing rejects unsupported, ambiguous, and missing periods', async () => {
  for (const q of ['Can I afford a mortgage?', 'What were my expenses last year?', 'What were my expenses in July 2026?', 'What were my expenses in 2027-05?', 'How much did I spend on bitcoin?', 'Show 99 largest expenses', 'What were my expenses in May and June?']) assert.throws(() => askQuestion(state.transactions, q, '2026-05'));
  const multiYear = await importCSV(state, header + '2027-05-01,PAYROLL,5,Other,other', '2027.csv');
  assert.throws(() => askQuestion(multiYear.state.transactions, 'Income in May', '2026-05'), /ambiguous/);
  assert.equal(askQuestion(multiYear.state.transactions, 'Income in May 2027', '2026-05').amount, 500);
});
test('browser storage survives reopen, correction persists, clear removes app key only', () => {
  const data = new Map([['other-app', 'keep']]);
  const storage = { getItem: k => data.get(k) ?? null, setItem: (k, v) => data.set(k, v), removeItem: k => data.delete(k) };
  assert.deepEqual(loadState(storage), emptyState());
  const t = state.transactions[0]; const edited = correctTransaction(state, t.id, 'expense', 'Rent');
  saveState(storage, edited);
  assert.deepEqual(loadState(storage), edited);
  assert.equal(effective(loadState(storage).transactions[0]).category, 'Rent');
  assert.deepEqual(clearState(storage), emptyState());
  assert.equal(data.has(STORAGE_KEY), false); assert.equal(data.get('other-app'), 'keep');
  storage.setItem(STORAGE_KEY, '{bad'); assert.throws(() => loadState(storage));
  storage.setItem(STORAGE_KEY, '{"version":999}'); assert.throws(() => loadState(storage));
});
test('browser persistence failure leaves previous state intact', () => {
  let saved = JSON.stringify(state);
  const storage = { getItem: () => saved, setItem: () => { throw new Error('quota exceeded'); } };
  const next = correctTransaction(state, state.transactions[0].id, 'expense', 'Rent');
  assert.throws(() => saveState(storage, next)); assert.deepEqual(loadState(storage), state);
});
test('published demo copies match source data and production modules cannot read test oracles', async () => {
  for (const name of ['synthetic_checking_2026_Jan-Jun.csv', 'synthetic_savings_2026_Jan-Jun.csv']) assert.equal(await readFile(new URL(`../docs/demo/${name}`, import.meta.url), 'utf8'), await fixture(name));
  for (const name of ['app.js', 'engine.js', 'storage.js']) {
    const source = await readFile(new URL(`../docs/${name}`, import.meta.url), 'utf8');
    assert.doesNotMatch(source, /synthetic_ground_truth|expected_monthly_totals|https?:\/\//);
  }
});
