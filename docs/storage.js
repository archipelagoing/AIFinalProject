import { emptyState } from './engine.js';
export const STORAGE_KEY = 'compass:alpha:1';
export function loadState(storage) {
  const raw = storage.getItem(STORAGE_KEY);
  if (!raw) return emptyState();
  const state = JSON.parse(raw);
  if (state.version !== 1 || !Array.isArray(state.imports) || !Array.isArray(state.transactions)) throw new Error('Saved data has an unsupported format. Clear Compass data to start again.');
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
