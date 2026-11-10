import { emptyState, TYPES, months, summarize } from './engine.js';
export const STORAGE_KEY = 'compass:alpha:1';
export function loadState(storage) {
  const raw = storage.getItem(STORAGE_KEY);
  if (!raw) return emptyState();
  const state = JSON.parse(raw);
  if (state.version !== 1 || !Array.isArray(state.imports) || !Array.isArray(state.transactions)) throw new Error('Saved data has an unsupported format. Clear Compass data to start again.');
  const imports = new Set(state.imports.map(i => i.id));
  const ids = new Set();
  for (const i of state.imports) {
    if (typeof i.id !== 'string' || typeof i.filename !== 'string' || typeof i.digest !== 'string') throw new Error('Invalid saved import.');
  }
  for (const t of state.transactions) {
    if (typeof t.id !== 'string' || ids.has(t.id) || !imports.has(t.import_id) || !/^\d{4}-\d{2}-\d{2}$/.test(t.date) || typeof t.description !== 'string' || typeof t.account !== 'string' || !Number.isSafeInteger(t.amount_cents) || !TYPES.includes(t.predicted_type) || typeof t.predicted_category !== 'string' || (t.corrected_type !== null && !TYPES.includes(t.corrected_type)) || (t.corrected_category !== null && typeof t.corrected_category !== 'string') || !t.original_row_json) throw new Error('Invalid saved transaction.');
    ids.add(t.id);
  }
  for (const month of months(state.transactions)) summarize(state.transactions, month);
  return state;
}
export function saveState(storage, state) {
  // setItem is atomic. Failure leaves the previous saved value untouched.
  storage.setItem(STORAGE_KEY, JSON.stringify(state));
  return state;
}
export function clearState(storage) {
  storage.removeItem(STORAGE_KEY);
  return emptyState();
}
