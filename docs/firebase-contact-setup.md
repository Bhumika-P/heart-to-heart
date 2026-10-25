# Main website contact form — Firebase setup

Implementation is local only. No main-site backend has been deployed and no SMTP credentials have been copied from the support group.

## Before activation

Owner selected the existing support project: hearttoheart-14e56. .firebaserc and the public endpoint now target that project. The separate `main-contact` function codebase and `mainContactMessages`, `mainContactRateLimits`, `admins` database paths prevent accidental reuse of support records. If sharing the support project, deploy only this named function codebase; do not replace the support site's rules, environment settings, secrets or functions.

1. Enable Realtime Database and the billing required by Cloud Functions in the selected project.
2. Install the pinned dependencies in functions/ with npm install. Runtime: Node 22.
3. Create functions/.env.PROJECT_ID from .env.example. Set MAIN_DATABASE_URL, MAIN_MAIL_TO=hthlifecoaching@gmail.com and the verified MAIN_MAIL_FROM. Never commit that environment file.
4. Reference the existing SMTP_URL Secret Manager secret by name. Do not replace or rotate the support service credential. No SMTP value has been read or copied. The private local environment file reuses the existing non-secret verified sender.
5. Deploy `firebase deploy --only functions:main-contact --project PROJECT_ID` only after deployment authorization. No hosting deploy is needed for the backend.
6. The database must deny public reads/writes on mainContactMessages, mainContactRateLimits and admins. firebase-main-contact-rules.json is a template for a dedicated project; on a shared project merge these paths into the existing reviewed rules. Do not replace shared rules with the template. Keep private messages out of public access.
7. Reuse the existing approved support administrators (`admins/UID=true`); no new administrators are needed. Read saved messages and delivery status in the Firebase console. The authenticated retryMainContactEmail callable can retry failed delivery for an approved admin. There is no main-site admin UI yet.
8. Set the public submitMainContact HTTPS endpoint and enabled=true in assets/js/contact-config.js. Local sending stays off unless deliberately allowed for an authorized synthetic test. These are public settings, not secrets.
9. Test an authorized synthetic submission and confirm every contact field, multiple call times and interests, private saved record, and actual delivery to the inbox. Verify failure messages and retry behavior. Do not claim live delivery based on a local test alone.
10. Update privacy wording and the sitewide preview banner when publishing. Other local preview forms remain disconnected.

## Delivery behavior

The form POSTs the Firebase callable protocol without requiring the visitor to sign in. The server validates names, email, length limits, required choices, allowed values and the honeypot. IP/email counters limit abuse. A random request identifier avoids duplicate saved messages on network retry. Email uses a verified sender and the visitor's address as Reply-To.

Messages are saved before delivery. Delivery status is pending/sending/sent/failed. If email fails, the visitor is told the message was saved but email delivery failed; administrators can retry. A network interruption after SMTP accepts a message can still produce a duplicate notification on retry. Review retention and anti-abuse settings before launch; rate-limit counters expire logically but old entries need a retention/cleanup policy.

Current inactive form deliberately disables SEND and states that sending is not connected. Enabling the service must be backed by a real deployed endpoint and inbox test.

## Prepared shared-project configuration

The owner selected sharing the support Firebase project. firebase-shared-rules.review.json preserves all current support rules and adds only mainContactMessages (existing admins may read) and mainContactRateLimits (private). It is a review artifact, not wired to automatic deployment. Refresh it against current support rules before deployment. The standalone rules template is not for this shared project.

Run backend deployment only after owner authorization: `firebase deploy --only functions:main-contact --project hearttoheart-14e56`. The support codebase default must not be deleted or redeployed by this repository. Frontend remains disabled until authorized endpoint/inbox testing succeeds.
