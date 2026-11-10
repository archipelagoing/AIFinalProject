import { TYPES, CATEGORIES, emptyState, importCSV, summarize, months, monthName, money, effective, correctTransaction, parseMoney, calculateScenario, rentCandidates, askQuestion } from './engine.js';
import { loadState, saveState, clearState } from './storage.js';

const $ = selector => document.querySelector(selector);
const escape = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
let state = emptyState(), selectedMonth = '', currentAnswer = null, scenarioInputs = null, storageProblem = '';
try { state = loadState(localStorage); } catch { storageProblem = 'Saved data could not be opened. Storage may be blocked or the saved format may be invalid. Clear saved data to reset it; no saved records were overwritten.'; }
const colors = ['#315942', '#5f8f68', '#b86b45', '#c79a35', '#aeb7b2', '#c9d9bf'];
const titles = {
  overview: ['Your money, in perspective.', 'Understand where you are. Explore where you could go.'],
  transactions: ['The details make the difference.', 'Review the source. Keep your picture of spending accurate.'],
  ask: ['A question worth asking.', 'Real calculations, with the transactions to back them up.'],
  whatif: ['Make room for what’s next.', 'Explore how a recurring change could reshape your monthly surplus.']
};
function notice(message, error = false) {
  $('#notice').textContent = message;
  $('#notice').classList.toggle('error', error);
  $('#notice').hidden = !message;
}
function commit(next) {
  if (storageProblem) throw new Error('Saved storage could not be loaded. Clear Compass data before importing to avoid overwriting it.');
  try { saveState(localStorage, next); } catch { throw new Error('Could not save to this browser. Storage may be full or disabled. Previous data is unchanged; try clearing browser space.'); }
  state = next;
}
function showModal(title, html) {
  $('#modal-title').textContent = title;
  $('#modal-content').innerHTML = html;
  if (!$('#modal').open) $('#modal').showModal();
}
$('#close-modal').onclick = () => $('#modal').close();
$('#modal').addEventListener('click', event => { if (event.target === $('#modal')) { const r = $('#modal').getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) $('#modal').close(); } });

function table(rows, editable = false) {
  if (!rows.length) return '<p class="no-results">No matching transactions for this view.</p>';
  return `<div class="table-scroll"><table><thead><tr><th>Date</th><th>Transaction</th><th>Category / type</th><th class="amount">Amount</th>${editable ? '<th>Review</th>' : ''}</tr></thead><tbody>${rows.map(raw => {
    const t = effective(raw);
    return `<tr><td>${escape(t.date.slice(5))}<br><small class="muted">${escape(t.date.slice(0, 4))}</small></td><td class="description">${escape(t.description)}<small>${escape(t.account)} · ${escape(t.source_transaction_id || `row ${t.source_row_number}`)}</small></td><td><span class="tag ${t.type === 'unknown' ? 'unknown' : ''}">${escape(t.category)}</span><br><small class="muted">${escape(t.type)}${t.reviewed ? ' · reviewed' : ''}</small></td><td class="amount ${t.amount_cents > 0 ? 'positive' : ''}">${t.amount_cents > 0 ? '+' : ''}${money(t.amount_cents)}</td>${editable ? `<td><button class="edit-button" data-edit="${escape(t.id)}" aria-label="Review ${escape(t.description)} on ${escape(t.date)}">Review</button></td>` : ''}</tr>`;
  }).join('')}</tbody></table></div>`;
}
function warnings(summary) {
  return `<details class="quality-warning"><summary>${summary.unknown.length ? `${summary.unknown.length} unresolved transaction(s), ${money(summary.unknown.reduce((n, t) => n + Math.abs(t.amount_cents), 0))} excluded · ` : ''}Coverage and exclusions — inspect before relying on totals</summary><ul>${summary.warnings.map(x => `<li>${escape(x)}</li>`).join('')}<li>Verified means classified by rules or your corrections, not reconciled to a bank balance.</li></ul></details>`;
}
function evidence(summary, rows, label = 'Inspect source transactions') {
  return `<details class="evidence"><summary>${escape(label)} (${rows.length})</summary><p class="small muted">Period: ${escape(monthName(summary.month))}. Source amount, account, date, description, and ID are preserved from the statement.</p>${table(rows)}</details>`;
}
function render() {
  const available = months(state.transactions);
  if (!available.includes(selectedMonth)) selectedMonth = available.includes('2026-05') ? '2026-05' : available.at(-1) ?? '';
  $('#month').innerHTML = available.map(m => `<option value="${m}" ${m === selectedMonth ? 'selected' : ''}>${monthName(m)}</option>`).join('') || '<option>No statements yet</option>';
  $('#month').disabled = !available.length;
  $('#row-count').textContent = state.transactions.length;
  const page = Object.hasOwn(titles, location.hash.slice(1)) ? location.hash.slice(1) : 'overview';
  document.querySelectorAll('[data-page]').forEach(a => { a.classList.toggle('active', a.dataset.page === page); if (a.dataset.page === page) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
  $('#page-label').textContent = ({ overview: 'Overview', transactions: 'Transactions', ask: 'Ask Compass', whatif: 'What If?' })[page];
  $('#heading').textContent = titles[page][0]; $('#subtitle').textContent = titles[page][1];
  document.querySelectorAll('.view').forEach(v => { v.hidden = v.id !== `view-${page}`; });
  $('#empty').hidden = available.length > 0; $('#workspace').hidden = !available.length;
  if (!available.length) return;
  const summary = summarize(state.transactions, selectedMonth);
  const allDemo = state.imports.every(i => i.fictional_demo === true);
  $('#dataset-label').textContent = allDemo ? 'Fictional demo data' : 'Imported statement data';
  $('#dataset-detail').textContent = `· ${state.transactions.length} transactions · ${new Set(state.transactions.map(t => t.account)).size} accounts`;
  $('#quality').innerHTML = warnings(summary);
  $('#metrics').innerHTML = [
    ['Verified income', summary.income, 'Income transactions only', '↓', 'income'],
    ['Net expenses', summary.expenses, 'Expenses, less refunds', '↑', 'expenses'],
    ['Verified surplus', summary.surplus, 'Income minus net expenses', '↗', 'surplus']
  ].map(([label, value, note, icon, key], i) => `<button class="metric ${i === 2 ? 'featured' : ''}" data-metric="${key}"><span class="metric-label">${label}</span><span class="metric-icon" aria-hidden="true">${icon}</span><span class="metric-value ${value < 0 ? 'negative-text' : ''}">${money(value)}</span><span class="metric-note">${note}<span aria-hidden="true"> ↗</span></span></button>`).join('');
  renderSpending(summary); renderHistory();
  $('#recent').innerHTML = table([...summary.rows].sort((a, b) => b.date.localeCompare(a.date)).slice(0, 5), true);
  $('#review-count').textContent = `${summary.reviewed} / ${summary.rows.length} reviewed`;
  renderTransactions();
  renderRent(summary);
  renderScenario(summary);
  renderAnswer();
}
function renderSpending(summary) {
  $('#spending-period').textContent = monthName(selectedMonth);
  const categories = Object.entries(summary.categories).sort((a, b) => b[1] - a[1]);
  if (!categories.length) { $('#spending').innerHTML = '<p class="no-results">No classified spending in this month.</p>'; return; }
  const top = categories.slice(0, 5);
  if (categories.length > 5) top.push(['Other', categories.slice(5).reduce((s, [, n]) => s + n, 0)]);
  const positiveTotal = top.reduce((s, [, n]) => s + Math.max(0, n), 0);
  let cursor = 0;
  const stops = top.map(([, amount], i) => { const start = cursor; cursor += positiveTotal ? Math.max(0, amount) / positiveTotal * 100 : 0; return `${colors[i]} ${start}% ${cursor}%`; });
  $('#spending').innerHTML = `<div class="spend-layout"><div class="donut" role="img" aria-label="Net expenses ${money(summary.expenses)}. Category values listed alongside." style="background:conic-gradient(${positiveTotal ? stops.join(',') : '#e9eddf 0% 100%'})"><div><small>NET SPENDING</small><strong>${money(summary.expenses)}</strong></div></div><div class="spend-list">${top.map(([category, amount], i) => `<div class="spend-row"><i style="background:${colors[i]}"></i><span>${escape(category)}</span><strong>${money(amount)}</strong></div>`).join('')}</div></div>${categories.some(([, n]) => n < 0) ? '<p class="small muted">Net refund categories are listed but have no positive chart segment.</p>' : ''}`;
}
function renderHistory() {
  const totals = months(state.transactions).map(month => summarize(state.transactions, month));
  const max = Math.max(...totals.map(s => Math.abs(s.surplus)), 1);
  $('#history').innerHTML = totals.map(s => `<div class="history-column ${s.month === selectedMonth ? 'selected' : ''}"><span class="bar-value">${money(s.surplus)}</span><button class="${s.surplus < 0 ? 'negative' : ''}" style="height:${Math.max(3, Math.abs(s.surplus) / max * 112)}px" data-month="${s.month}" aria-label="${monthName(s.month)} surplus ${money(s.surplus)}"></button><small>${monthName(s.month).slice(0, 3)} '${s.month.slice(2, 4)}</small></div>`).join('');
  $('#history-insight').textContent = `${totals.length} imported month${totals.length === 1 ? '' : 's'} in view. Surplus describes classified activity, not the money currently in your account.`;
}
function renderTransactions() {
  if (!selectedMonth) return;
  const search = $('#search').value.trim().toLowerCase(), type = $('#type-filter').value;
  const rows = summarize(state.transactions, selectedMonth).rows.filter(t => (!type || t.type === type) && [t.description, t.account, t.source_transaction_id, t.category].join(' ').toLowerCase().includes(search)).sort((a, b) => b.date.localeCompare(a.date));
  $('#transaction-table').innerHTML = table(rows, true);
}
function renderRent(summary) {
  const candidates = rentCandidates(summary);
  const signature = JSON.stringify([summary.month, candidates.map(t => [t.id, t.amount_cents, t.reviewed])]);
  if ($('#existing-rent').dataset.signature === signature) return;
  $('#existing-rent').dataset.signature = signature;
  const detected = candidates.length === 1 ? -candidates[0].amount_cents : null;
  const value = detected === null ? '' : `${Math.floor(detected / 100)}.${String(detected % 100).padStart(2, '0')}`;
  $('#existing-rent').innerHTML = `<div class="rent-note">${candidates.length === 1 ? `Detected ${money(detected)} from ${escape(candidates[0].description)}. ${candidates[0].reviewed ? 'Classification reviewed.' : 'Rule-classified; please confirm below.'}` : candidates.length > 1 ? `Multiple possible rent charges: ${candidates.map(t => `${escape(t.description)} ${money(-t.amount_cents)}`).join('; ')}. Confirm the total rent already included.` : 'No unambiguous rent charge found. Confirm the rent already included in the selected baseline; do not substitute all Housing spending.'}<label>Existing rent included in baseline ($)<input id="confirmed-rent" inputmode="decimal" value="${value}" placeholder="Enter existing rent"></label><label class="check-label"><input id="confirm-rent" type="checkbox">I confirm this rent is already included in this month's expenses.</label></div>`;
}
function readScenario() {
  const mode = document.querySelector('[name="rent-mode"]:checked').value;
  const existingRent = mode === 'replace' && $('#confirm-rent').checked ? parseMoney($('#confirmed-rent').value) : null;
  return { newRent: parseMoney($('#new-rent').value), mode, existingRent, addedSpending: parseMoney($('#added-spending').value), incomeAdjustment: parseMoney($('#income-adjustment').value) };
}
function renderScenario(summary) {
  const node = $('#scenario-result');
  if (!scenarioInputs || scenarioInputs.month !== selectedMonth) { node.innerHTML = '<section class="card"><p class="eyebrow">YOUR POSSIBLE NEXT CHAPTER</p><h2>See the difference before making a change.</h2><p class="muted small">Choose how the rent applies, confirm your existing rent for replacement mode, then calculate. Every step will be shown here.</p></section>'; return; }
  // Read current inputs so a correction or a changed confirmation cannot leave a stale result.
  try {
    const inputs = readScenario();
    const result = calculateScenario({ baseline: summary.surplus, ...inputs });
    node.innerHTML = `<section class="card"><p class="eyebrow">${escape(monthName(selectedMonth))} BASELINE · ILLUSTRATIVE</p><h2>Projected monthly surplus</h2><div class="result-amount ${result.projected < 0 ? 'negative-text' : ''}">${money(result.projected)}</div><p class="result-change">${money(result.change)} change from your historical baseline</p>${result.projected < 0 ? '<p class="quality-warning">This scenario has a monthly shortfall: expenses exceed income.</p>' : ''}${inputs.mode === 'additional' ? '<p class="quality-warning">Additional mode keeps existing rent and adds the full proposed payment. Both rents count.</p>' : ''}<div class="formula-row"><span>Verified income</span><strong>${money(summary.income)}</strong></div><div class="formula-row"><span>Net expenses</span><strong>${money(summary.expenses)}</strong></div><div class="formula-row"><span>Baseline surplus</span><strong>${money(summary.surplus)}</strong></div><div class="formula-row"><span>Income change</span><strong>${money(inputs.incomeAdjustment)}</strong></div><div class="formula-row"><span>Added spending (subtract)</span><strong>${money(inputs.addedSpending)}</strong></div><div class="formula-row"><span>Rent delta (subtract)</span><strong>${money(result.rentDelta)}</strong></div><p class="small muted">${inputs.mode === 'replace' ? `Replacement rent delta: ${money(inputs.newRent)} − ${money(inputs.existingRent)} confirmed existing rent.` : `Additional rent delta: ${money(inputs.newRent)}.`}<br>Projected = ${money(summary.surplus)} + (${money(inputs.incomeAdjustment)}) − (${money(inputs.addedSpending)}) − (${money(result.rentDelta)}).</p><div class="six-month"><p>SIX MONTHS · STATIC EXTRAPOLATION</p><strong>${money(result.sixMonths)}</strong><p class="small">6 × ${money(result.projected)}. Repeats this month; not a starting cash balance. Historical activity may be atypical.</p></div>${evidence(summary, [...summary.incomeRows, ...summary.expenseRows], 'Inspect baseline source rows')}</section>`;
  } catch (error) { node.innerHTML = `<section class="card"><h2>Confirm your assumptions</h2><p class="modal-message" role="alert">${escape(error.message)}</p></section>`; }
}
function renderAnswer() {
  if (!currentAnswer) return;
  try {
    const result = askQuestion(state.transactions, currentAnswer.question, currentAnswer.month);
    $('#answer').innerHTML = `<section class="card answer-card"><p class="eyebrow">${escape(monthName(result.month))} · CALCULATED FROM SOURCE ROWS</p><h2>${escape(currentAnswer.question)}</h2><div class="answer-value">${money(result.amount)}</div><p class="small muted">${escape(result.calculation)} = ${money(result.amount)}</p><p class="small muted">Filters: ${escape(result.month)}; classified transaction types only. Transfers and unknowns are excluded.</p>${warnings(result.summary)}${evidence(result.summary, result.rows, 'Inspect answer evidence')}</section>`;
  } catch (error) { $('#answer').innerHTML = `<section class="notice error" role="alert">${escape(error.message)}</section>`; }
}

async function loadDemo() {
  const buttons = [$('#demo-button'), $('#load-demo')]; buttons.forEach(b => b.disabled = true);
  try {
    const original = state;
    let next = state; let added = 0;
    for (const name of ['synthetic_checking_2026_Jan-Jun.csv', 'synthetic_savings_2026_Jan-Jun.csv']) {
      const response = await fetch(new URL(`./demo/${name}`, import.meta.url));
      if (!response.ok) throw new Error('Demo files could not be loaded. Check your connection and try again.');
      const result = await importCSV(next, await response.text(), name); next = result.state; added += result.added;
      next = { ...next, imports: next.imports.map(i => i.filename === name ? { ...i, fictional_demo: true } : i) };
    }
    if (state !== original) throw new Error('Workspace changed while the demo was loading. Try loading it again; your latest changes were kept.');
    commit(next); selectedMonth = '2026-05'; render();
    notice(added ? `Loaded ${added} fictional transactions. Select a month to explore; original data and corrections stay in this browser.` : 'The fictional statements are already loaded. Existing corrections were kept.');
  } catch (error) { notice(error.message, true); }
  finally { buttons.forEach(b => b.disabled = false); }
}
$('#demo-button').onclick = loadDemo; $('#load-demo').onclick = loadDemo;
function openImport() {
  showModal('Import a CSV statement', '<p>Use fictional statements for this public prototype. Selected file contents are processed in your browser and saved here; they are not uploaded.</p><p>Required header: <code>date,description,amount,account,transaction_id</code></p><p>Dates: YYYY-MM-DD. Amounts: signed decimals (positive inflow, negative outflow). Leave transaction_id cells blank only when the source has no IDs. Imports are atomic: a rejected row means no rows are added.</p><p>Overlapping files and conflicting IDs are blocked for manual source review.</p><button class="primary" id="choose-file">Choose CSV file →</button><p id="import-message" class="modal-message" role="status"></p>');
  $('#choose-file').onclick = () => $('#file-input').click();
}
$('#import-button').onclick = openImport; $('#empty-import').onclick = openImport;
$('#file-input').onchange = async event => {
  const file = event.target.files[0]; if (!file) return;
  const button = $('#choose-file'); if (button) button.disabled = true;
  try {
    if (file.size > 5 * 1024 * 1024) throw new Error('Choose a CSV smaller than 5 MB for this browser-storage prototype.');
    const text = new TextDecoder('utf-8', { fatal: true }).decode(await file.arrayBuffer());
    const original = state;
    const result = await importCSV(original, text, file.name);
    if (state !== original) throw new Error('Workspace changed during this import. Try again; your latest changes were kept.');
    commit(result.state); render(); $('#modal').close(); notice(result.message);
  } catch (error) { if ($('#import-message')) $('#import-message').textContent = error instanceof TypeError ? 'Could not decode this file as UTF-8. Save it as a UTF-8 CSV and try again.' : error.message; else notice(error.message, true); }
  finally { event.target.value = ''; if (button) button.disabled = false; }
};
document.addEventListener('click', event => {
  const edit = event.target.closest('[data-edit]');
  if (edit) openEdit(edit.dataset.edit);
  const metric = event.target.closest('[data-metric]');
  if (metric) {
    const s = summarize(state.transactions, selectedMonth);
    const rows = metric.dataset.metric === 'income' ? s.incomeRows : metric.dataset.metric === 'expenses' ? s.expenseRows : [...s.incomeRows, ...s.expenseRows];
    showModal(`${monthName(selectedMonth)} · ${metric.dataset.metric}`, `<p>${money(s.income)} income − ${money(s.expenses)} net expenses = ${money(s.surplus)} verified surplus.</p>${warnings(s)}${table(rows)}`);
  }
  const month = event.target.closest('[data-month]');
  if (month) { selectedMonth = month.dataset.month; currentAnswer = null; $('#answer').innerHTML = ''; render(); }
});
function openEdit(id) {
  const raw = state.transactions.find(t => t.id === id); if (!raw) return;
  const t = effective(raw);
  showModal('Review classification', `<p><strong>${escape(t.description)}</strong><br>${escape(t.date)} · ${escape(t.account)} · ${money(t.amount_cents)}</p><form id="edit-form"><label>Transaction type<select id="edit-type">${TYPES.map(x => `<option ${x === t.type ? 'selected' : ''}>${x}</option>`).join('')}</select></label><label>Category<input id="edit-category" list="categories" value="${escape(t.category)}" required maxlength="80"><datalist id="categories">${CATEGORIES.map(x => `<option value="${escape(x)}">`).join('')}</datalist></label><p class="small muted">Rule: ${escape(raw.rule)}<br>Predicted: ${escape(raw.predicted_type)} / ${escape(raw.predicted_category)}. Overrides are stored separately from original values.</p><div id="edit-message" class="modal-message" role="alert"></div><div class="modal-actions"><button class="primary" type="submit">Save and mark reviewed</button><button class="secondary" type="button" id="reset-classification">Restore rule classification</button></div></form><details><summary class="small">Inspect immutable original source row</summary><pre>${escape(JSON.stringify(raw.original_row_json, null, 2))}</pre><p class="small muted">Source row ${raw.source_row_number} · Import SHA-256: ${escape(raw.import_id)}</p></details>`);
  $('#edit-form').onsubmit = event => { event.preventDefault(); saveEdit(false); };
  $('#reset-classification').onclick = () => saveEdit(true);
  function saveEdit(reset) {
    try {
      commit(correctTransaction(state, id, reset ? raw.predicted_type : $('#edit-type').value, reset ? raw.predicted_category : $('#edit-category').value, reset));
      // A changed baseline must be explicitly reconfirmed before another replacement result.
      $('#existing-rent').dataset.signature = '';
      render(); $('#modal').close(); notice(reset ? 'Rule classification restored. All totals recalculated.' : 'Classification saved. All totals and answers recalculated; source values preserved.');
    } catch (error) { $('#edit-message').textContent = error.message; }
  }
}
$('#month').onchange = event => { selectedMonth = event.target.value; currentAnswer = null; $('#answer').innerHTML = ''; render(); };
$('#search').oninput = renderTransactions; $('#type-filter').onchange = renderTransactions;
$('#scenario-form').onsubmit = event => { event.preventDefault(); scenarioInputs = { month: selectedMonth }; renderScenario(summarize(state.transactions, selectedMonth)); };
$('#scenario-form').addEventListener('input', () => { if (scenarioInputs) renderScenario(summarize(state.transactions, selectedMonth)); });
$('#scenario-form').addEventListener('change', () => { if (scenarioInputs) renderScenario(summarize(state.transactions, selectedMonth)); });
const examples = ['How much did I earn?', 'What were my expenses?', 'How much did I spend on restaurants?', 'What were my five largest expenses?', 'What was my surplus?'];
$('#examples').innerHTML = examples.map((q, i) => `<button type="button" data-question="${i}">${['Income', 'Expenses', 'Restaurants', 'Largest expenses', 'Surplus'][i]} ↗</button>`).join('');
$('#examples').onclick = event => { const b = event.target.closest('[data-question]'); if (b) { $('#question').value = examples[Number(b.dataset.question)]; $('#ask-form').requestSubmit(); } };
$('#ask-form').onsubmit = event => { event.preventDefault(); currentAnswer = { question: $('#question').value, month: selectedMonth }; renderAnswer(); };
function showPrivacy() {
  showModal('About your browser workspace', '<p>Compass Alpha is an experimental financial prototype. Use the bundled fictional data for demonstrations. It is not security-audited or a source of financial advice.</p><p>The app downloads static files and optional fictional CSVs from its host. Selected CSV contents, classifications, and calculations stay in browser localStorage. There are no cloud models, analytics, or statement uploads.</p><p>Browser storage is not encrypted by Compass, may be cleared by the browser, and is separate for each browser profile and site origin. Other scripts on the same origin may have access to it. Do not treat it as a secure financial vault.</p><p>There is no opening balance in the demo statements, so surplus is not available cash or an account balance. Month coverage cannot be established from transaction dates alone.</p><p>GitHub Pages replaces the planned Python server. SQLite, Ollama, PDF parsing, automatic bank sync, and arbitrary CSV column mapping are deferred.</p><button class="secondary" id="privacy-clear">Clear Compass data</button>');
  $('#privacy-clear').onclick = confirmClear;
}
function confirmClear() {
  showModal('Clear this browser workspace?', '<p>This removes Compass imports, original rows, and saved classification corrections from this browser. Bundled fictional demo files remain available. Other apps and browser data are unaffected.</p><form id="clear-form"><label class="check-label"><input type="checkbox" required>I understand my saved Compass data will be deleted.</label><button type="submit" class="primary danger">Delete Compass data</button><p id="clear-message" class="modal-message" role="alert"></p></form>');
  $('#clear-form').onsubmit = event => {
    event.preventDefault();
    try { state = clearState(localStorage); storageProblem = ''; selectedMonth = ''; scenarioInputs = null; currentAnswer = null; $('#answer').innerHTML = ''; render(); $('#modal').close(); notice('Compass data deleted from this browser. You can start again with fictional demo data.'); }
    catch { $('#clear-message').textContent = 'Browser storage is unavailable. Enable storage access before trying again.'; }
  };
}
$('#privacy-button').onclick = showPrivacy; $('#clear-button').onclick = confirmClear;
$('#mobile-privacy').onclick = showPrivacy; $('#mobile-clear').onclick = confirmClear;
window.addEventListener('hashchange', render);
window.addEventListener('storage', event => { if (event.key === 'compass:alpha:1' || event.key === null) { try { state = loadState(localStorage); storageProblem = ''; render(); notice('Workspace refreshed from another tab.'); } catch { storageProblem = 'Saved data changed in another tab and could not be loaded. Reload or clear Compass data before continuing.'; notice(storageProblem, true); } } });
render(); if (storageProblem) notice(storageProblem, true);
