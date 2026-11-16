# Language preference regression check

Run from the repository root with Node.js (no packages to install):

```sh
node --test tests/language-preference.test.cjs
```

The check executes the real language initialization and content data from index.html in an isolated JavaScript context. It covers SK/EN restoration, explicit URL language precedence, absent and invalid preferences, inherited property names such as constructor and __proto__, and storage that is blocked or unavailable. It also checks that the chosen language has usable title, project and note data.

This is a regression test for startup logic, not a browser layout, accessibility or full rendering test. Browser checks remain separate.

The optional PORTFOLIO_HTML environment variable points the same checks at a temporary HTML copy. It is used to verify that reintroducing the original unsafe membership check causes the regression suite to fail, without modifying the working page.

Run all checks with `node --test tests/*.test.cjs`. The content integrity suite also verifies translations, matching note/project identities, fragment targets, no-JavaScript content and PDF file presence.

## Browser smoke checks

With the repository served at `http://127.0.0.1:8765/`, open:

`http://127.0.0.1:8765/tests/browser-smoke.html?width=390&lang=en&scene=hero&report=1`

The same-origin test frame loads the actual page and uses programmatic clicks to check languages, links, notes, filters (including Android apps), modal close/focus and PDF responses. Choose width 320, 390, 768 or 1440; scene may be hero, mobile, notes, showcase or contact. A completed report has `complete: true` and `passed: true`. The report is hidden unless `report=1` is present, so screenshots can show the page without test text.

These checks do not simulate assistive technology or a complete keyboard-only journey. Fixed-width frames verify responsive CSS, not an actual mobile device.
