# Ján Janda - professional portfolio

A static Slovak/English portfolio for full remote B2B collaboration in software development, AI automation and web solutions. The paper and olive visual identity is shared with the downloadable one-page profiles.

## Run locally

Open `index.html` directly, or serve the repository with Python:

```sh
python -m http.server 8765 --bind 127.0.0.1
```

Visit `http://127.0.0.1:8765/`. No JavaScript packages or build step are needed to use the website.

## Visitor guide

- Choose SK/EN in the header. The explicit `?lang=en` or `?lang=sk` URL takes precedence over a saved preference, making the language shareable.
- Select a work filter or open a work area for details. Close its dialog with the close button, Escape or the backdrop.
- Expand a working note with its summary. Its arrow link opens the note and provides a URL such as `?lang=en#note-remote-brief`.
- Download the profile from About. The selected language chooses the matching PDF.
- Use the collaboration section's LinkedIn action to start a conversation. The website does not submit messages or collect form data.

The Slovak work areas and full notes are also in the initial HTML, so they remain readable without JavaScript. Dynamic language selection, filters and modal dialogs need JavaScript.

## Checks and exports

```sh
node --test tests/*.test.cjs
python scripts/export-profiles.py
python scripts/package-share.py
```

Tests use the Node.js standard library. Profile export uses ReportLab and the installed Windows Arial/Georgia fonts. PDFs are generated from the website's own `CONTENT`, which keeps wording aligned. Re-export after changing profile text. The share archive contains only the page, the two PDFs and short opening instructions; it excludes backups and agent instructions.

See [tests/README.md](tests/README.md) for the reproducible browser smoke page and its limits. Local checks used the bundled Python runtime by absolute path; the `python` commands above require a working Python installation on the contributor's PATH.

`backups/portfolio-v0.1.zip` is the immutable original snapshot. `output/share/jan-janda-portfolio-v1.0.zip` is the client-facing handoff package, not a deployment record.

## Maintenance

Edit both languages inside `const CONTENT` in `index.html`. Keep project/note IDs aligned and update the corresponding initial Slovak HTML when changing content. Note links use stable IDs. Retain the strict SK/EN preference allowlist.

Work areas describe personal experience; they are not invented client case studies. The portfolio itself is the concrete AI SITES web example. Public CV dates, availability, company details and quantified project results require confirmed source information.

## GitHub Pages

Public portfolio: [pukac.github.io](https://pukac.github.io/). The English entry point is [pukac.github.io/?lang=en](https://pukac.github.io/?lang=en).

GitHub Pages builds and deploys the `master` branch. Check the repository's **pages build and deployment** Actions run for the release commit, then verify the public HTML and both PDF downloads. A successful local test alone does not verify a deployment.

Local collaboration context, original backups and file handoff archives are excluded by `.gitignore`. The downloadable profiles in `output/pdf/` are public website assets.
