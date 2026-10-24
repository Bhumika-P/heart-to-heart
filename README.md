# Heart to Heart main website

Local review build of the complete public main website, using the Heart to Heart support group's visual theme. All changes are local and uncommitted. No production hosting, DNS, support-site backend, or TimeTap settings have been changed.

## Review in VS Code Live Server

1. Open this `heart-to-heart` folder in VS Code.
2. Right-click root `index.html` and select **Open with Live Server**.
3. Browse **All pages** in the footer to reach all 83 active migrated source pages. Use **Pricing**, **Contact**, and **Client resources** to review those workflows.

No npm install or framework development server is required to view the generated site. Live Server reloads when the static page files or stylesheets change.

The local form previews do not send or save information. Booking and donation links lead to the existing external services; completing those external flows can affect the live accounts. The old store's prices have been removed and its product descriptions retained, but the shopping cart has not been rebuilt. Review-only indexing protections intentionally prevent this draft from being indexed.

## Editing

- `assets/css/theme.css`: copied support-site styling; theme photographs use optimized WebP files.
- `assets/css/main.css`: main-site components and responsive/accessibility refinements.
- `assets/js/site.js`: mobile menu and footer year.
- `assets/js/review.js`: local-only form behavior; no backend, email, or persistence.
- `content/pages.json`: imported public page content and page records.
- `content/pricing.json`: approved main pricing and removal of in-person prices.
- `content/image-descriptions.json`: descriptions and accessible text transcriptions of legacy graphics.
- `scripts/build.py`: shared layout and generated HTML. Edit this rather than making lasting changes directly to generated page files.
- `scripts/check.py`: coverage, links, page structure, form fields, PDFs, and solid-color contrast checks.

To regenerate pages, use Python 3 with the packages in `requirements.txt`:

```bash
python3 scripts/build.py
python3 scripts/check.py
```

The Codex bundled Python runtime currently has these dependencies available. Source reimport additionally requires the ignored `work/source` capture; the normal build uses the retained `content/` files and does not need the old website or network access.

## Continuing the migration

Read `AGENTS.md`, `docs/handoff.md`, `docs/migration-scope.md`, and `docs/quality-requirements.md`. CP means Commit Push and is not currently authorized. Check usage periodically and pause at 10% or less remaining in either reported allowance until the user explicitly resumes.
