# Migration quality requirements

Approved scope additions on October 22, 2026. This document specifies acceptance criteria; it does not assert that the unbuilt site has passed them.

## Pricing

Use content/pricing.json as the central pricing source. The main pricing page controls prices: free 20-minute discovery call, $100/hour phone or virtual coaching, $150/hour emergency phone or virtual coaching. Ignore legacy store prices. Remove the in-person price from visible text, metadata, structured data, and any migrated product listings; preserve in-person service content. Keep downloaded source snapshots unchanged for provenance. Verify the external booking and payment journeys display the approved prices before launch.

## Accessibility

Target WCAG 2.1 Level AA across pages and complete workflows, including mobile navigation, forms, errors, dialogs, and booking handoffs. Matching the support theme does not override accessibility.

- Text contrast at least 4.5:1, or 3:1 for qualifying large text. Essential UI boundaries, states, and meaningful graphics at least 3:1 against adjacent colors. Test actual combinations, including hover, focus, disabled explanations, and image backgrounds.
- Semantic landmarks, skip link, descriptive titles, logical headings, appropriate native controls, meaningful link text, and correct page language.
- Full keyboard access with visible focus, logical order, no keyboard traps, accessible menu and dialog state, and focus restoration.
- Meaningful alternative text, empty alt for decorative images, descriptive frame titles, and review captions/transcripts for retained media. Review public PDF accessibility separately; retaining a PDF is not proof it conforms.
- Explicit form labels and instructions, appropriate autocomplete, accessible required states and validation, error association, announced submission status, and no loss of entered information after validation errors.
- No information conveyed only through color, hover, pointer position, or animation. Respect reduced motion; remove flashing and blinking effects.
- Readable at 200% text zoom and reflow at 320 CSS pixels / equivalent 400% desktop zoom without two-dimensional scrolling except legitimate exceptions. Support text-spacing overrides and portrait/landscape use.
- Use comfortable touch targets (44 by 44 CSS pixels as a design target, beyond WCAG 2.1 AA minimum requirements), no hover-only interactions, and robust focus/hover content behavior.
- Run automated accessibility scans on all page templates and representative content, plus manual keyboard, screen-reader, zoom, contrast, and mobile checks. Automated scans alone do not establish WCAG conformance. Record third-party limitations and resolve blockers before claiming conformance.

Reference: https://www.w3.org/TR/WCAG21/

## Responsive experience and performance

Build content-first, pre-rendered HTML with progressive enhancement and minimal JavaScript. Preserve the support site's visual system while adjusting typography, navigation, and layouts for the main site's larger content inventory. Verify 320, 375, 390, 768, 1024, and 1440 CSS pixel widths, long text, and actual touch interactions.

Core Web Vitals good targets at the 75th percentile of real visits: LCP at most 2.5 seconds, INP at most 200 milliseconds, CLS at most 0.1. Evaluate mobile and desktop. Lab checks before launch are diagnostic and do not prove field performance; monitor real-user/PageSpeed Insights/Search Console data after deployment when available.

Use responsive modern image formats and sensible compression, explicit image dimensions/aspect ratios, lazy loading below the fold, and appropriately prioritized hero imagery. Subset/self-host licensed fonts where practical with stable fallbacks and font-display behavior. Minimize CSS/JS, avoid unnecessary frameworks and third-party scripts, defer noncritical embeds, cache fingerprinted assets, compress responses, and reserve space for embeds and async content. Test representative long pages, forms, image-heavy pages, and external booking handoffs, not just the homepage. Do not report a Lighthouse score or a Core Web Vitals pass without measured evidence.

Reference: https://web.dev/articles/vitals

## SEO and answer and generative search discoverability

- Preserve existing public URLs where feasible. Create an explicit old-to-new mapping and permanent redirects for any changed URL. Avoid redirecting unrelated retired pages indiscriminately to the homepage.
- Unique descriptive page titles and meta descriptions, canonical URLs, crawlable HTML and internal links, logical navigation, breadcrumbs, XML sitemap, deliberate robots policy, correct HTTP status codes, and a useful 404 page.
- Keep preview/staging environments out of search indexing; remove staging noindex rules intentionally on production launch. Exclude client submissions, private administration, and source archives from public output and sitemaps. Indexing controls are not access controls.
- Preserve all substantive source content. Use descriptive headings and clear answers to real visitor questions without keyword stuffing, invented claims, fabricated reviews, or mass-generated filler. Any new substantive claims or changed promises require owner review.
- Present clear business identity, Sherée's verified biography and credentials, actual service areas, contact information, policies, and the distinctions between coaching and other services. Keep facts consistent across pages and listings. Publish genuine authorship and meaningful update dates where appropriate.
- Add validated Schema.org markup only for facts and visible content actually present: organization/business identity, person, website/webpage, breadcrumbs, services/offers, books and FAQs where appropriate. Do not imply special AI schema or guaranteed rich-result eligibility; FAQ rich results have restricted eligibility. Never fabricate ratings, addresses, credentials, dates, or prices.
- Make key information readable in initial HTML and image alternatives. Structure useful explanations so search systems can identify and quote them accurately. Google advises the same foundational SEO and helpful-content practices for AI features and requires no special AI schema.
- Validate metadata, structured data, link integrity, sitemap coverage, mobile rendering, redirects, and production crawl/index settings. Set up Search Console verification and sitemap submission when account access is available, then monitor indexing and errors.
- Rankings, traffic, citations, and inclusion in AI answers are outcomes to monitor, not guarantees. Optional AI-specific files are not substitutes for crawlability, factual content, or evidence-backed technical work.

References:
- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
