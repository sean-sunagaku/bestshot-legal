# BestShot legal & support

BestShotの公開用規約・サポートサイトです。アプリ・APIのソースコードとは別の公開リポジトリで管理します。公開ディレクトリは `docs/` のみです。

**Website:** https://sean-sunagaku.github.io/bestshot-legal/

## Documents

| Document | Stable default URL |
| --- | --- |
| Privacy policy | https://sean-sunagaku.github.io/bestshot-legal/privacy/ |
| Terms of use | https://sean-sunagaku.github.io/bestshot-legal/terms/ |
| Support | https://sean-sunagaku.github.io/bestshot-legal/support/ |
| Data deletion | https://sean-sunagaku.github.io/bestshot-legal/delete-data/ |

Full documents are provided in Japanese (`ja`), English (`en`), Simplified Chinese (`zh-Hans`), Traditional Chinese (`zh-Hant`), and Korean (`ko`). Add the locale before the document path, for example `/en/privacy/`. Default URLs serve Japanese without requiring JavaScript, cookies, or sign-in. The language selector preserves the current document.

## Edit and deploy

1. Edit all five `content/*.json` files together when the policy changes.
2. Update `DATE` in `build.py` for policy changes. Update `BASE` if the repository or hostname changes.
3. Run `python3 build.py` and `python3 check.py`.
4. Commit the source and generated `docs/` files and push to `main`.
5. GitHub Pages publishes the `main` branch’s `/docs` folder. Check the Pages deployment and public URLs after pushing.

Python 3.10+ is the only build dependency. The published pages contain no JavaScript, external fonts, advertising, analytics, contact forms, or app credentials. GitHub’s infrastructure still logs visitor IP addresses for security, as disclosed in the policy. The app icon is a BestShot brand asset, not a grant to reuse the brand.

## Content baseline

Effective 2026-10-23, matching the current TestFlight beta: local media storage, explicit consent before sending up to 12 reduced images to OpenAI through BestShot, Cloudflare processing and metadata storage, no user registration, no advertising tracking, and no in-app purchases. Server metadata currently has no automatic retention deadline. The policy discloses this and provides a request route; it does not claim automatic deletion or zero provider retention.

The website translations do not imply the app UI or AI explanations are localized. Those are currently Japanese. Future billing, retention, processors, account, or localization changes require corresponding policy and app updates before release.

Japanese App Store Connect and TestFlight URL fields have been registered and verified. App-source links have also been updated; distribution of those additional in-app links requires a new app build. See [App Store URL mapping and integration status](APP_STORE.md).
