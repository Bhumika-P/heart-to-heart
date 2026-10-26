# Local migration handoff

## User instructions

Work only in the main-site repository for local review. No commit, push, deployment, or DNS changes are authorized. CP means Commit Push. The user plans to open root index.html using VS Code Live Server.

Check Codex usage periodically. At 10% or less remaining in either reported five-hour or weekly allowance, save progress and pause until Sherée or Darren explicitly asks to resume. This preference is saved in AGENTS.md. Do not consume reset credits automatically.

## Implemented locally

- 83 active public source pages are generated at their original URL paths, plus resources, directory, and 404 pages. The retired About Your Coach address redirects locally to Coach Sherée.
- The homepage and shared layouts use the support site's burgundy/cream palette, Cormorant Garamond/Lato typography, mountain imagery, header, buttons, and footer patterns. Fonts are local; photos are optimized to WebP where appropriate.
- Source text, original images, external resources, TimeTap booking links, hosted PayPal donation destinations, the YouTube embed, and 11 distinct client PDFs are retained. Legacy text graphics have readable HTML transcriptions. Empty original pages remain explicitly identified rather than receiving invented content.
- Main pricing: complimentary 20-minute discovery call, $100/hour phone/virtual, $150/hour emergency phone/virtual. Legacy catalog prices removed; no in-person price is published. In-person service content retained.
- Four forms preserve their original user-entry fields with improved labels, grouping, validation, and status announcements. These are explicitly local previews and do not send, store, or email any input.
- Titles, descriptions, canonical URLs, organization/website/webpage and breadcrumb JSON-LD, sitemap, and deliberate preview noindex/robots protections are generated.
- Mobile menu supports keyboard use and Escape with focus return. Focus styles, input borders, descriptive images, and solid-color contrast were improved.

## Verified

- scripts/check.py: 87 generated pages checked, all 84 source pages present, all local links/assets resolve on disk, JSON-LD parses, all 4 forms retain source entry-field names and have accessible names, and all 11 PDFs are present. No static check errors.
- Solid-surface brand contrast ratios checked: body 13.06:1, muted text 6.73:1, burgundy links/headings 12.07:1, white-on-burgundy button 12.78:1, eyebrow 6.04:1, review banner 8.83:1.
- Browser inspected all 84 pages at 320px and 1440px: no horizontal overflow; one h1 and one main per page. Seven representative pages were additionally checked at 390, 768, and 1024px. A pricing-card overflow discovered at 320px was fixed and the complete 320px pass succeeded afterward.
- Mobile menu open/close tested. Contact form tested with synthetic data; it stayed on the local page and announced that no information was sent or saved.
- These checks are partial accessibility validation, not WCAG conformance certification. No Lighthouse or field Core Web Vitals results are claimed.

## Remaining work

1. Owner review of the local design and all source content, including older coaches/services and unfinished pages. Preserve content unless the user authorizes changes.
2. Full manual and automated WCAG 2.1 AA audit, including assistive technology, zoom/text spacing, image-background contrast, media, and PDF accessibility. Resolve any failures; external TimeTap screens require their own assessment.
3. Separate main-site backend design and implementation for private inquiries, testimonial submissions, client reports, administration, notifications, permissions, anti-abuse controls, and appropriate data retention. No support-site credentials or rules have been copied.
4. Confirm the legacy cart's actual use and implement an equivalent approved commerce path. The current draft preserves product pages and points to current booking/pricing; it is not a migrated cart.
5. Account-level inventory and transfer of non-public records, orders, submissions, unpublished pages, payment settings, and appointment history as appropriate. Public crawling did not provide these.
6. Verify external TimeTap pricing agrees with the user's approved amounts. The external account has not been changed.
7. Performance measurements with production-like hosting and representative mobile conditions; optimize as indicated, then monitor field Core Web Vitals after an authorized launch. Current optimization work is not a measured pass.
8. Production SEO/indexing review, structured-data validation, redirect mapping, appropriate publishing of older/empty pages, Search Console setup and sitemap submission when authorized. Local preview noindex rules must not accidentally reach production.
9. Prepare a deployment-only output directory and hosting configuration that excludes docs, work, source JSON, and tooling. No production hosting configuration has been created yet.

## Local tooling

Build and checks use scripts/build.py and scripts/check.py with lxml and Pillow. All generated HTML lives at repository root / original subdirectories for Live Server. Work captures and QA intermediates are ignored in work/. Production integrations are not enabled in the preview.

## Owner-approved homepage cleanup

The owner requested further compact styling for all six cards, removal of the legacy Welcome heading, book promotion and image, old coach photo/caption and introductory copy, old heart-of-the-matter heading, Types of Coaching button, and bottom heart logo. The main Meet Your Coach section remains. The complete Christian-coaching question and answer was moved from homepage source content to the FAQ in content/pages.json under faith-and-coaching. Normal builds preserve these edits; do not rerun the raw source importer over approved content changes without merging them. Card heights were verified at 176px for all six at 1440, 390, and 320 CSS pixels, with no horizontal overflow.

## About page consolidation

Coach Sherée (coach-shereacutee.html) is the single active About page. The top navigation and homepage About Sherée button point there. About Your Coach was retired, removed from the active content list, directories, and sitemap, and all internal links were updated. content/redirects.json records the old-to-new path; the old local address contains only an immediate redirect and fallback link. Configure a permanent HTTP redirect at production hosting setup. The former source record is archived in ignored work/retired/; the original public capture is retained.

## Resources consolidation — October 23, 2026

- Homepage Books by Sherée card is now Resources, with the requested healing-and-growth description and the same resources.html destination as the top navigation.
- All three Shop book covers, titles, and About links now appear on Resources for your journey in a responsive grid. content/resources.json stores this content. Shop heading and directory entry removed; shop.html redirects locally to resources.html. Configure permanent hosting redirects before launch.
- Current build has 82 active source pages and two retired-page redirects. Static checker passed all 88 checked pages, four forms, and 11 PDFs; focused assertions verified the card destination, book content and image alternatives. All changes remain local, uncommitted and unpushed.

- Resources follow-up: added the homepage description period, reduced book titles from 25px to 22px, and added BUY buttons using the three existing Amazon destinations from https://www.shereebergman.com/books.html (main book B0FNLVWCBQ, guide B0FQ2RTYVY, journal B0FQ4ZVDT6). ABOUT buttons retained.

- Added Resources cards for I Can’t Love You Through the Fence (cover and ABOUT from shereebergman.com/books.html; Coming soon, awaiting purchase/preorder URL) and Discovering the Mind of a Woman by Ken Nair (retailer ABOUT and Amazon ISBN 0785278117 BUY). Covers sourced from author site and Christianbook listing. No invented purchase link for upcoming book.

- Owner confirmed no Amazon link yet for I Can’t Love You Through the Fence and requested an inactive BUY button. Added a native disabled button with a Coming soon accessible label; retain the visible Coming soon notice.

- Split Resources ABOUT destinations into five individual local book pages with covers, descriptions, BUY controls and a Resources return link. Original about-start-at-start.html now describes only the main book; its original guide/journal descriptions moved intact to their respective pages (legacy headings removed). Upcoming Fence page has a clearly forthcoming description and disabled BUY pending owner copy/link. Ken Nair has a brief factual synopsis. Checker now also covers the four added pages.

- Added emotional-abuse-coaching.html and connected the Emotional Abuse page button. New page uses existing owner-approved coaching language, with discovery-call and support-group links. Local review only.

- Moved Schedule Appointment scheduler introduction, external TimeTap button/note and donation text/PayPal button onto Pricing (invest-in-yourself.html). Schedule links now use Pricing; old schedule-appointment.html redirects locally to Pricing. Configure corresponding permanent redirect at launch. No CP.

- Owner requested removal of Types of Coaching. Removed active page/directory/sitemap entry; navigation and homepage Explore coaching now open Why Coaching. Old types-of-coaching.html redirects locally to why-coaching.html. Original content archived under ignored work/retired.

- Client resources temporarily unavailable at owner request. Footer link removed; client-intake-packet.html shows update/contact message. All 11 PDFs moved outside the site root to ../Heart to Heart - Private Client Resources/documents, with original page content backed up there. Other PDF links now open the temporary resource notice. docs/client-resource-archive.json maps old paths to the local archive; checker verifies preservation and absence from public upload paths. Archive must never be published.

- Extra Links temporarily hidden: footer link and sitemap entry removed; public directory replaced with update notice. Original page and readable link list preserved beside site in Heart to Heart - Private Client Resources/extra-links-original.html and Extra Links.md. Underlying individual pages unchanged.

- Explore every page temporarily hidden: All pages footer/404 links and sitemap entry removed; directory replaced with unavailable notice. Original HTML and readable page list saved outside site root in Heart to Heart - Private Client Resources. Individual pages remain available at their addresses.

## Resources and FAQ update — October 24, 2026

- Resources for your journey now follows support Helpful Resources sections (five book cards, Polaris music, workbook tools); original main title retained and confidentiality agreement card omitted. Added local workbooks.html matching the support companion-guide page; support repository untouched.
- f-a-q.html replaced with owner-supplied FAQ copy: 46 native details/summary disclosures in ten sections, closed by default, with real scheduling, policy, service and support links. F.A.Q. footer link immediately left of Testimonials on all standard pages. Copy also preserved in content/faq.json.
- Static checker passed 96 pages. Browser verified click-open and keyboard-close, 46 initially closed answers, no horizontal overflow at 320px FAQ or 390px Resources, five loaded covers and matching desktop resource layout. Screenshot: work/faq-preview.png. No commit, push, deployment, or support-site changes.

- Restored Resources headphone background by copying missing support concept-details.png asset into main site. Centered Tools & Guides eyebrow/title and its single workbook box. Browser screenshot verified matching headphone picture on left and centered tools. Updated Heal opening Glass Walls and Orphan Wound sections with exact supplied replacement; asserted HTML from What Is Open-Heart Coaching onward unchanged. Static check passed 96 pages; no CP.

- Updated orphan-wound.html with owner-supplied father/identity reflection text and 21 questions; linked Orphan Wound within the Heal page mindset sentence. Updated become-a-christian.html with requested YouTube embed, gospel text and centered prayer box (tan/white inset border). Footer Become a Christian immediately precedes F.A.Q. on standard pages. Static checker passed 96 pages; focused assertions verified destinations, question count, footer order and video ID. Local only, no CP.

- Corrected main branch at owner request: merged migration/main-website into main so the website lives at root index.html with assets/content beside it. Removed work/ from Git tracking (local archive retained and ignored). Main branch is the requested push target; no deployment or DNS changes.

## Main contact form Firebase implementation — October 24, 2026

- User chose Firebase approach after inspection of support-group backend. Main-only functions draft added under functions/, codebase main-contact, exports submitMainContact/retryMainContactEmail, separate mainContactMessages/RateLimits/Admins paths, MAIN_SMTP_URL server secret and recipient hthlifecoaching@gmail.com. No credentials copied.
- Contact adapter preserves all form fields including multiple times and interests, server validation/honeypot/rate limits, idempotent message storage and delivery states, failure preservation and authenticated delivery retry. Public contact-config.js defaults disabled; SEND visibly disabled with explanatory note until a deployed endpoint is configured. Other forms remain previews.
- Seven focused backend validation/frontend transport tests passed using synthetic data (no email sent). JS syntax and 96-page static checker passed. No Firebase integration/emulator test or live inbox test completed; dependencies not installed/deployed yet. Setup steps in docs/firebase-contact-setup.md.
- Pending owner answer: dedicated main Firebase project vs sharing support project. Shared project requires explicit owner choice; do not overwrite existing support rules/functions/settings. No deployment/CP authorized this turn.

- Owner selected sharing Firebase project hearttoheart-14e56. Added .firebaserc and configured public endpoint, still disabled. Functions now reference existing SMTP_URL secret by name; only non-secret sender routing read from the support env file into ignored main-site env file. Existing support admins authorize main message reads/retries. firebase-shared-rules.review.json preserves every existing support rule and adds only main message/rate-limit paths; no rule deployment configured or performed. Installed local dependencies and lockfile, backend imports validated; seven tests and 96-page checker pass. Deployment and real inbox test still require authorization per local-only agreement.

- Extension-free URLs implemented using static directory index pages, rebased assets and navigation, clean canonicals/structured data/sitemap, and legacy .html redirect stubs. 96-page checker passed plus all-page .html-link assertions. Browser verified /resources/ and /connect-with-us/ with loaded assets. Explicit index.html normalizes to its directory URL. No CP or deployment.

## Main contact backend deployment — pending public-invoker approval

- User authorized Firebase connections on shared hearttoheart project. Refreshed rules from live database; deployed only mainContactMessages/admin-read and private mainContactRateLimits additions while preserving every original support rule. Public read checks return 401/403 for both main paths.
- Deployed main-contact submitMainContact and retryMainContactEmail successfully to hearttoheart-14e56 (Node22/us-central1). Build required functions/pnpm-workspace.yaml allowBuilds for @firebase/util and protobufjs plus explicit @google-cloud/functions-framework dependency. Standard support functions untouched.
- Authorized synthetic HTTP test returned 403 before reaching handler: endpoint invoker remains private. No test email sent. Frontend contact-config enabled remains false.
- Auto-review rejected a follow-up deployment setting invoker:public because user had not explicitly approved that exact persistent public access setting. Entire exec rejected, so proposed source change did NOT execute. Must obtain explicit approval for anonymous public contact submissions before adding invoker:public and redeploying. Do not bypass using IAM APIs or another route. Explain spam exposure and existing validation/rate limits/private storage.
- After approval: add invoker:public in functions/index.js options, redeploy only main-contact; run work/test-main-contact-live.py once. Confirm emailed:true and private database denial, then enable frontend with appropriate local-sending setting and rebuild. No additional CP yet.

## Contact form activation authorized

- User explicitly approved public submissions, making it live, testing and CP. Main-contact functions deployed successfully after adding Functions Framework and explicit pnpm dependency approvals. Corrected server allowlist to match the visible Marriage/Family/Relationship Restoration Coaching label; eight tests pass.
- Firebase CLI callable deployment ignored invoker:public; inspected actual Cloud Run IAM, then applied user-authorized allUsers roles/run.invoker to submitmaincontact only, preserving other bindings. SMTP secret value unchanged/unread.
- Synthetic endpoint test returned ok:true, emailed:true for hthlifecoaching@gmail.com. Anonymous reads denied. Message ID stored in ignored work/main-contact-live-test.json. No private client data used.
- Enabled contact-config.js for production and local preview (local contact submissions now send real email). Public website still needs the authorized CP and live browser test. Other submission forms stay local previews; main admin UI is not implemented. Retry endpoint remains transport-restricted.

## Activation push and live verification pending

- Main contact endpoint now publicly callable through explicit Cloud Run allUsers run.invoker binding (only submitmaincontact); backend synthetic test returned ok:true/emailed:true and anonymous stored-message access denied. Relationship option validation fixed and deployed.
- User explicitly authorized CP/publication. Commit 6636656 is pushed to main; origin/main matches. Includes enabled:true, allowLocalSending:true, config cache version live1 and deployment dependency fixes. Eight tests and 96-page checks pass.
- The first live browser reload after push still showed the previous disabled form, likely awaiting GitHub Pages publication/cache update. MUST verify actual live activation before claiming end-to-end browser completion. Browser handle liveContactTab is on https://hearttoheartlifecoaching.com/connect-with-us/. Inspect enabled SEND and note; then use synthetic test name Website / Live Form Test, email hthlifecoaching@gmail.com, subject Question, A.M. and P.M., Support Group and optional relationship option, message clearly labeled authorized setup test. Click SEND, verify success and save screenshot. Do not submit real client information.
- Backend test email subject TEST — main website Firebase connection (no action required), sent to hthlifecoaching@gmail.com; SMTP accepted it, inbox receipt not personally inspected. Other main forms remain previews.

## October 25 — branded main contact email prepared locally

- User confirmed the published main contact form successfully delivered immediately, resolving the older live-verification-pending note above.
- Built functions/contact-email.js: burgundy/cream HTML email, Main Website label, contact details, selected interests, preferred times, message, encoded mailto reply button. Native Reply-To and plaintext fallback remain. All visitor content is HTML escaped. No dashboard link.
- Wired HTML into main sendMail. Ten backend/frontend/email tests pass; git diff --check passes.
- Fictional preview: work/contact-email-preview.html (ignored). Not committed, pushed, or deployed in this turn. Live notifications still use previous plaintext format until backend deployment. Support group repo unchanged; its notification format still needs a separate change if requested.

## October 26 — branded main email deployed and live-tested

- User explicitly authorized deployment and live submission verification, with support-group template unchanged.
- Firebase CLI deployed only functions:main-contact to hearttoheart-14e56; submitMainContact and retryMainContactEmail updated successfully. No hosting, rules, support functions, or support template deployed.
- All 10 contact/backend/HTML tests pass.
- Submitted synthetic Website / Email Template Test through https://hearttoheartlifecoaching.com/connect-with-us/ to the existing hthlifecoaching@gmail.com destination. A.M., Weekdays are best, Support Group selected. Message explicitly TEST, no client information.
- Live form returned “Thank you. Your message has been received and emailed to Heart to Heart.” confirming storage and SMTP acceptance from the deployed HTML sendMail path. Form reset and SEND re-enabled.
- Screenshot: ignored work/live-html-email-submission.png. Gmail inbox rendering not directly inspected; no claim of visual Gmail verification. Support group template unchanged.
