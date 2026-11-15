const assert = require('node:assert/strict');
const { readFileSync, existsSync } = require('node:fs');
const { resolve } = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const root = resolve(__dirname, '..');
const html = readFileSync(resolve(root, 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const shell = html.slice(0, html.indexOf('<script>'));
const content = vm.runInNewContext(script.slice(0, script.indexOf('function restoreLanguage')) + ';CONTENT');

test('page JavaScript parses', () => { new vm.Script(script); });

test('every UI translation has nonempty SK and EN copy', () => {
  assert.deepEqual(Object.keys(content.sk).sort(), Object.keys(content.en).sort());
  for (const [, key] of shell.matchAll(/data-(?:t|html)="([^"]+)"/g)) {
    for (const language of ['sk', 'en']) {
      assert.equal(typeof content[language][key], 'string', `${language}: ${key}`);
      assert.ok(content[language][key].trim(), `${language}: ${key} is empty`);
    }
  }
});

test('project and note identities agree across languages', () => {
  for (const group of ['projects', 'notes']) {
    const ids = content.sk[group].map(row => row.id);
    assert.equal(new Set(ids).size, ids.length);
    assert.deepEqual(content.en[group].map(row => row.id), ids);
  }
});

test('all static fragment links resolve to unique IDs', () => {
  const ids = [...shell.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(new Set(ids).size, ids.length, 'Duplicate HTML/SVG ID');
  for (const [, id] of shell.matchAll(/href="(?:\?[^"#]*)?#([^"]+)"/g)) {
    assert.ok(ids.includes(id), `Missing destination #${id}`);
  }
});

test('language-specific profile downloads exist', () => {
  for (const language of ['sk', 'en']) {
    const path = resolve(root, `output/pdf/jan-janda-profile-${language}.pdf`);
    assert.ok(existsSync(path));
    assert.equal(readFileSync(path).subarray(0, 5).toString(), '%PDF-');
  }
});

test('working notes and work areas remain readable without JavaScript', () => {
  for (const row of content.sk.notes) {
    assert.ok(shell.includes(`id="note-${row.id}"`));
    assert.ok(shell.includes(row.title));
    assert.ok(shell.includes(row.paragraphs.at(-1)));
  }
  for (const row of content.sk.projects) assert.ok(shell.includes(row.title));
});
