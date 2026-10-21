import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, dirname } from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const locales = ['en', 'ar'];
const pages = ['index', 'privacy'];
const checkOnly = process.argv.includes('--check');
const read = (path) => readFile(resolve(root, path), 'utf8');

// Translation values are plain text, including when used in HTML attributes.
// Only repository-owned partials may insert markup.
function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  })[character]);
}

function render(template, values) {
  const output = template.replace(/\{\{(\w+)\}\}/g, (_, key) => {
    if (!Object.hasOwn(values, key)) throw new Error(`Missing template value: ${key}`);
    return escapeHtml(values[key]);
  });
  if (output.includes('{{')) throw new Error('Unresolved template expression');
  return output;
}

const dictionaries = Object.fromEntries(await Promise.all(locales.map(async (locale) => [
  locale, JSON.parse(await read(`src/locales/${locale}.json`)),
])));
const expectedKeys = Object.keys(dictionaries.en).sort().join('\n');
for (const [locale, dictionary] of Object.entries(dictionaries)) {
  if (Object.keys(dictionary).sort().join('\n') !== expectedKeys) {
    throw new Error(`Translation keys do not match for ${locale}`);
  }
  for (const [key, value] of Object.entries(dictionary)) {
    if (typeof value !== 'string' || !value.trim()) {
      throw new Error(`Empty or invalid translation: ${locale}.${key}`);
    }
  }
}

const partials = Object.fromEntries(await Promise.all(['header', 'footer'].map(async (name) => [
  name, (await read(`src/partials/${name}.html`)).trimEnd(),
])));

for (const page of pages) {
  const template = (await read(`src/templates/${page}.html`)).replace(
    /\{\{>(\w+)\}\}/g,
    (_, name) => {
      if (!Object.hasOwn(partials, name)) throw new Error(`Unknown partial: ${name}`);
      return partials[name];
    },
  );
  for (const locale of locales) {
    const arabic = locale === 'ar';
    const values = {
      ...dictionaries[locale],
      locale,
      direction: arabic ? 'rtl' : 'ltr',
      assetPrefix: arabic ? '../' : '',
      homeUrl: 'index.html',
      aboutUrl: page === 'index' ? '#about' : 'index.html#about',
      contactUrl: page === 'index' ? '#contact' : 'index.html#contact',
      englishUrl: `${arabic ? '../' : ''}${page}.html`,
      arabicUrl: `${arabic ? '' : 'ar/'}${page}.html`,
      alternateUrl: `${arabic ? '../' : 'ar/'}${page}.html`,
      alternateLocale: arabic ? 'en' : 'ar',
      alternateDirection: arabic ? 'ltr' : 'rtl',
      alternateLabel: arabic ? 'English' : 'العربية',
    };
    // aria-current is markup owned here, never a translation value.
    const markup = template.replace('{{privacyCurrent}}', page === 'privacy' ? 'aria-current="page"' : '');
    const output = render(markup, values);
    const target = resolve(root, arabic ? `ar/${page}.html` : `${page}.html`);
    if (checkOnly) {
      if (await readFile(target, 'utf8') !== output) {
        throw new Error(`${target} is stale. Run node scripts/build.mjs`);
      }
    } else {
      await mkdir(dirname(target), { recursive: true });
      await writeFile(target, output);
    }
    console.log(`${checkOnly ? 'Verified' : 'Built'} ${locale}/${page}.html`);
  }
}
