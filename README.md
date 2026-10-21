# Kids Hotel — company website

English and Arabic static website for Kids Hotel and A.H.M HINDI LTD. No runtime JavaScript, cookies, browser storage, external fonts, or third-party dependencies.

## Architecture

- `src/locales/en.json`, `ar.json`: plain-text translations with matching keys.
- `src/templates/`: homepage and website privacy templates.
- `src/partials/`: shared header and footer.
- `scripts/build.mjs`: dependency-free Node.js generator; escapes translation values, validates translation completeness and rejects unresolved placeholders.
- `index.html`, `privacy.html`, `ar/*.html`: generated pages. **Edit templates or translations, not these outputs.**
- `styles.css`: readable shared CSS, responsive layouts, logical properties and Arabic typography.
- `assets/kids-hotel-logo-*.webp`, `assets/favicon.png`: original logo extracted from the supplied PDF. See `docs/brand-system.md` for the palette, typography and component rules.

English is the default. Arabic lives at `ar/index.html` and `ar/privacy.html`. Language links switch to the equivalent page; navigation stays within the selected language. Each page declares `lang`, `dir`, translated metadata and reciprocal `hreflang` links. Direct links and language switching work without JavaScript, including under a hosting subdirectory.

## Edit and verify

Requires Node.js for generation only. No installation step is needed.

```sh
node scripts/build.mjs
node scripts/build.mjs --check
python3 scripts/verify.py
git diff --check
```

Check mode fails if generated pages differ from their source. The verifier checks local links, assets, fragment targets, language routes, direction and landmarks.

## Preview

Open `index.html` directly, or run:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Visit `http://127.0.0.1:8080/`. Open `ar/index.html` to preview Arabic.

## Content and publication

- Contact information distinguishes the company registered address (7 Sadot, Ma’ale Adumim, Israel 9851356) from the nursery location (Al-Israa Street 11, Shuafat, Jerusalem), as supplied by the owner.
- The supplied original logo replaces the earlier decorative house illustration.
- Privacy pages cover only this informational website, **not the app**. The app’s audience and data practices have not been supplied.
- Review company details and privacy wording against the chosen hosting provider before publication.
- Upload only root HTML pages, `ar/`, `styles.css` and `assets/`. Do not upload source folders, scripts, this README or `.git`.
- Hosting has not been configured or published.
# kids-hotel-landing-page
