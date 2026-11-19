import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const css = await readFile(new URL('../docs/styles.css', import.meta.url), 'utf8');
const contrastReport = JSON.parse(await readFile(new URL('../docs/design-system-contrast.json', import.meta.url), 'utf8'));

function tokensFrom(block) {
  return Object.fromEntries([...block.matchAll(/--(compass-[\w-]+):\s*(#[\da-f]{6})/gi)].map(([, name, value]) => [name, value]));
}

function contrast(foreground, background) {
  const luminance = color => {
    const channels = [1, 3, 5].map(index => parseInt(color.slice(index, index + 2), 16) / 255)
      .map(value => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4);
    return channels[0] * 0.2126 + channels[1] * 0.7152 + channels[2] * 0.0722;
  };
  const [lighter, darker] = [luminance(foreground), luminance(background)].sort((a, b) => b - a);
  return (lighter + 0.05) / (darker + 0.05);
}

const tokenStart = css.indexOf('/* Compass design tokens;');
const darkStart = css.indexOf('@media (prefers-color-scheme: dark)', tokenStart);
const lightTokens = tokensFrom(css.slice(tokenStart, darkStart));
const darkBlock = css.slice(darkStart).match(/:root\s*\{([^}]+)\}/)?.[1];
assert.ok(darkBlock, 'dark color-scheme token block exists');
const darkTokens = tokensFrom(darkBlock);

test('light and dark semantic text pairs meet WCAG AA contrast', () => {
  const pairs = [
    ['primaryTextOnSurface', 'compass-ink', 'compass-surface'],
    ['mutedTextOnSurface', 'compass-muted', 'compass-surface'],
    ['actionTextOnAction', 'compass-action-ink', 'compass-action'],
    ['brandTextOnSoftBrand', 'compass-brand', 'compass-brand-soft'],
    ['warningTextOnWarningSurface', 'compass-warning', 'compass-warning-surface'],
    ['errorTextOnErrorSurface', 'compass-danger', 'compass-danger-surface'],
    ['focusRingOnCanvas', 'compass-focus', 'compass-canvas']
  ];

  for (const [theme, tokens] of [['light', lightTokens], ['dark', darkTokens]]) {
    for (const [reportName, foreground, background] of pairs) {
      assert.ok(tokens[`--${foreground}`], `${theme} ${foreground} token exists`);
      assert.ok(tokens[`--${background}`], `${theme} ${background} token exists`);
      const ratio = contrast(tokens[`--${foreground}`], tokens[`--${background}`]);
      assert.ok(
        ratio >= 4.5,
        `${theme} ${foreground} on ${background} meets 4.5:1`
      );
      assert.ok(Math.abs(contrastReport.results[theme][reportName].ratio - ratio) < 0.01, `${theme} ${reportName} audit matches token colors`);
    }
  }
  assert.equal(contrastReport.standard, 'WCAG 2.2 AA');
  assert.equal(contrastReport.normalTextMinimum, 4.5);
});

test('design system honors reduced-motion preference and documents coverage limits', async () => {
  assert.match(css, /@media\s*\(prefers-reduced-motion:\s*reduce\)/);
  const html = await readFile(new URL('../docs/index.html', import.meta.url), 'utf8');
  assert.match(html, /Statement coverage is not verified/);
  assert.match(html, /not a bank-balance reconciliation/);
});
