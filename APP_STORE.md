# App Store submission links

Updated 2026-10-23. The public URLs below are available in all five website languages. The Japanese App Store Connect and TestFlight URL fields were subsequently registered and read back successfully. Other store localizations have not been created by this website task.

| Locale | Privacy Policy URL | Support URL | Terms of Use URL |
| --- | --- | --- | --- |
| Japanese / `ja` | https://sean-sunagaku.github.io/bestshot-legal/ja/privacy/ | https://sean-sunagaku.github.io/bestshot-legal/ja/support/ | https://sean-sunagaku.github.io/bestshot-legal/ja/terms/ |
| English / `en-US`, `en-GB` | https://sean-sunagaku.github.io/bestshot-legal/en/privacy/ | https://sean-sunagaku.github.io/bestshot-legal/en/support/ | https://sean-sunagaku.github.io/bestshot-legal/en/terms/ |
| Simplified Chinese / `zh-Hans` | https://sean-sunagaku.github.io/bestshot-legal/zh-Hans/privacy/ | https://sean-sunagaku.github.io/bestshot-legal/zh-Hans/support/ | https://sean-sunagaku.github.io/bestshot-legal/zh-Hans/terms/ |
| Traditional Chinese / `zh-Hant` | https://sean-sunagaku.github.io/bestshot-legal/zh-Hant/privacy/ | https://sean-sunagaku.github.io/bestshot-legal/zh-Hant/support/ | https://sean-sunagaku.github.io/bestshot-legal/zh-Hant/terms/ |
| Korean / `ko` | https://sean-sunagaku.github.io/bestshot-legal/ko/privacy/ | https://sean-sunagaku.github.io/bestshot-legal/ko/support/ | https://sean-sunagaku.github.io/bestshot-legal/ko/terms/ |

Stable default Japanese URLs are also available at `/privacy/`, `/support/`, `/terms/`, and `/delete-data/`. The homepage can serve as the informational website / optional Marketing URL. Data-deletion pages exist for every locale at `/{locale}/delete-data/`.

## Integration status and future submissions

The Japanese App Store Connect `privacyPolicyUrl`, `privacyChoicesUrl`, `supportUrl`, and `marketingUrl` fields now point to this site. The Japanese TestFlight `privacyPolicyUrl` and `marketingUrl` were also updated. A final metadata dry run reported no pending changes.

App source now includes privacy, terms, support, and deletion links in settings, with privacy access before AI transfer. These app UI changes require a new app build to reach installed users; no new TestFlight/App Store binary was uploaded for this URL update. For existing builds, the old API `/privacy` URL redirects to this site in both development and production. A Simulator Release build and opening the terms page from settings were verified.

- Set localized Privacy Policy and Support URLs in App Store Connect for localizations actually offered by the app/store listing. A website translation alone does not add an app language.
- Make the privacy policy accessible in app settings and the AI consent flow. Link support and terms where appropriate. A published website alone does not change an installed binary.
- Preserve the explicit pre-transfer explanation and consent identifying OpenAI and the information sent. A policy link alone does not replace that consent.
- Reconcile App Privacy answers with actual processing, retention, providers, support correspondence, and the privacy manifest. Images are sent to an external AI service; do not claim that no data is handled based only on local media storage or `store: false`. Consider Apple’s definition of collection and any applicable exceptions against actual provider settings. The site does not configure App Privacy answers.
- The published service terms supplement Apple’s standard EULA. This project does not register a custom EULA in App Store Connect.
- The current beta has no billing. Before adding subscriptions, implement and verify the purchase flow and display the actual product name, period, price, renewal/cancellation conditions, privacy and terms links, and restoration/management options. No price or unlimited-use promise is made here.
- This site uses the existing public operator name `sunagaku` and support email. Any seller identity, business address, regional trader disclosures, tax details, or payment-specific disclosures must match verified information when those fields become applicable. No address, price, corporate status, or registration number is fabricated here.

The URL integration did not upload an app build, submit a review, change pricing, enroll regions, change App Privacy answers, or register a custom EULA. Billing-specific and future-localization items above still apply when those features are introduced.

## Official references checked

- [App Review Guidelines, privacy and consent](https://developer.apple.com/app-store/review/guidelines/#privacy)
- [Platform version information, including Support URL](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/)
- [App privacy details](https://developer.apple.com/app-store/app-privacy-details/)
- [Apple standard EULA](https://www.apple.com/legal/internet-services/itunes/dev/stdeula/)
- [OpenAI API data controls](https://developers.openai.com/api/docs/guides/your-data)
- [GitHub Pages availability and visitor data](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
