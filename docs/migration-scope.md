# Main website migration

The main website at https://www.hearttoheartlifecoaching.com/ is to be migrated in full into this repository. Match the existing heart-to-heart-support website's theme, colors, typography, components, spacing, and responsive layouts. This is a full content and feature migration, not a condensed rewrite.

## Source and design

- Darren's Website Migration Findings document is accepted by the user as current project context.
- On October 22, 2026, all 84 public sitemap URLs were downloaded successfully for reference in ignored work/source/.
- docs/migration-inventory.json records each page, title, content checksum, images, links, embeds, and form fields.
- The adjacent heart-to-heart-support checkout is version 1.4.0 and is the design source. Its working files have not been changed.
- Implementation branch: migration/main-website.

## Preserve

Every information page, service, coach biography, educational article, faith resource, testimonial, book description, policy, older or unfinished page, and associated image. Preserve URLs where practical and document redirects explicitly. Retain all 11 distinct linked client PDFs.

Preserve TimeTap booking, PayPal donations, the support group subdomain, external book/author links, video embeds, and downloadable paperwork. Reimplement the contact inquiry, testimonial submission, pre-coaching report, and post-coaching report with equivalent fields and appropriate private storage and administration.

Account-held customer records, orders, submissions, appointment history, unpublished content, and settings are outside the public capture and still require account-level access for an inventory or transfer.

## Decisions before production cutover

- Pricing decision resolved October 22, 2026: use the main pricing page as authoritative, ignore legacy store prices, and remove the in-person price throughout the new site. Keep in-person service content unless separately changed. Verify the external TimeTap checkout agrees with the approved prices before launch; editing this site does not change TimeTap settings.
- Confirm whether the existing store and cart remain in use and how their checkout will be preserved or replaced.
- Confirm main-site Firebase project and administrator ownership before provisioning or deployment. Do not reuse support-site production credentials, rules, or data by copying its configuration.
- Preserve all older content in the source inventory; any retirement or substantive content changes require an explicit decision.
- Verify private handling, notifications, and permissions for client reports.
- Review the complete result and functionality before changing the existing domain's hosting or DNS.

## Build acceptance requirements

See docs/quality-requirements.md for accessibility, mobile, SEO, answer and generative search discoverability, and Core Web Vitals requirements. These requirements apply to every page and interactive workflow.

## Current status

First local review build created: 83 active public source pages plus one retired-page redirect, 11 linked PDFs, support-theme shared styling, homepage, resources directory, approved pricing, accessible form previews, and local search metadata. See docs/handoff.md for verified checks and outstanding work. No private backend, cart migration, account-data migration, deployment, or domain cutover has been completed. All changes remain uncommitted and local; no CP is authorized.
