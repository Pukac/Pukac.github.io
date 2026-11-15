const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

// Execute the page's actual startup code, without reimplementing its language logic.
// PORTFOLIO_HTML is only needed for an isolated regression/mutation check.
const pagePath = process.env.PORTFOLIO_HTML || resolve(__dirname, '../index.html');
const html = readFileSync(pagePath, 'utf8');
const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
assert.equal(scripts.length, 1, 'Expected the self-contained page script');
const script = scripts[0][1];
const start = script.indexOf('const CONTENT =');
const end = script.indexOf('let activeFilter=');
assert.ok(start >= 0 && end > start, 'Could not locate page startup code');
const startup = script.slice(start, end);
assert.ok(startup.includes('let language='), 'Language initialization must be exercised');

function boot(storage, search = '') {
  const context = { URLSearchParams, location: { search } };
  if (storage === 'blocked-access') {
    Object.defineProperty(context, 'localStorage', {
      get() { throw new Error('Storage access blocked'); }
    });
  } else if (storage !== 'missing-storage') {
    context.localStorage = storage;
  }
  return vm.runInNewContext(startup + `
    ({
      language,
      title: CONTENT[language].title,
      projectIds: CONTENT[language].projects.map(project => project.id),
      noteIds: CONTENT[language].notes.map(note => note.id)
    })
  `, context, { timeout: 1000 });
}

function storageWith(value) {
  return {
    getItem(key) {
      assert.equal(key, 'jan-janda-language');
      return value;
    }
  };
}

function expectLanguage(storage, expected, search = '') {
  const state = boot(storage, search);
  assert.equal(state.language, expected);
  assert.equal(typeof state.title, 'string');
  assert.ok(state.title.length > 0);
  assert.ok(state.projectIds.length > 0, 'Selected language must have usable project data');
  assert.ok(state.noteIds.length > 0, 'Selected language must have usable note data');
}

for (const language of ['sk', 'en']) {
  test(`restores supported language ${language}`, () => {
    expectLanguage(storageWith(language), language);
  });
}

for (const value of [null, undefined, '', 'de', 'SK', 'en-US', ' en ', 'null']) {
  test(`falls back to SK for ${JSON.stringify(value)}`, () => {
    expectLanguage(storageWith(value), 'sk');
  });
}

for (const value of ['constructor', 'toString', '__proto__', 'hasOwnProperty', 'valueOf']) {
  test(`rejects inherited property name ${value}`, () => {
    expectLanguage(storageWith(value), 'sk');
  });
}

test('falls back to SK when getItem throws', () => {
  expectLanguage({ getItem() { throw new Error('Read blocked'); } }, 'sk');
});

test('falls back to SK when access to localStorage throws', () => {
  expectLanguage('blocked-access', 'sk');
});

test('falls back to SK when localStorage is unavailable', () => {
  expectLanguage('missing-storage', 'sk');
});

for (const language of ['sk', 'en']) {
  test(`explicit URL language ${language} wins over saved preference`, () => {
    expectLanguage(storageWith(language === 'sk' ? 'en' : 'sk'), language, '?lang=' + language);
  });
  test(`explicit URL language ${language} works with blocked storage`, () => {
    expectLanguage('blocked-access', language, '?lang=' + language);
  });
}

for (const value of ['constructor', '__proto__', 'de', '']) {
  test(`unsupported URL language ${JSON.stringify(value)} keeps a valid preference`, () => {
    expectLanguage(storageWith('en'), 'en', '?lang=' + encodeURIComponent(value));
  });
}
