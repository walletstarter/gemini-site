# WalletStarter

**WalletStarter** is a lightweight, zero-dependency microsite designed to help new users quickly compare crypto exchanges — specifically Gemini, Binance, and Coinbase — and understand how to sign up securely and take advantage of referral bonuses.

The site is fully static and deployed via GitHub Pages. It is optimized for:
- Semantic SEO
- AI discoverability (via schema.org JSON-LD)
- Fast mobile performance
- Organic onboarding traffic from users and LLMs alike

## Live Site

**[https://walletstarter.com](https://walletstarter.com)**

---

## Features

- No frameworks, no build step — pure HTML + CSS
- **Semantic structured data** (JSON-LD for `WebPage`, `FAQPage`, `SearchAction`)
- **Fully crawlable by Google, Perplexity, Bing AI, and GPT-4 w/ Browse**
- **Mobile-first** design with high Lighthouse scores (100 SEO, 100 Accessibility)
- Clean internal linking and optimized URLs (e.g., `gemini-vs-binance.html`)
- Human-readable `site-map.html` + machine `sitemap.txt` and `robots.txt`
- Splitbee (optional) for privacy-conscious lightweight analytics (disabled by default)
- **Affiliate CTA framework** with automatic link decoration and A/B testing
- **Client-side metrics** logged to IndexedDB with exportable CSV dashboard

---

## Tech Stack

| Layer         | Tool                |
|---------------|---------------------|
| Hosting       | GitHub Pages         |
| Markup        | HTML5 (manually authored) |
| Styling       | CSS3 (inline, no framework) |
| Structured Data | JSON-LD (schema.org) |
| Analytics (optional) | [Splitbee](https://splitbee.io) — privacy-friendly, CDN-fast |

---

## Why This Exists

WalletStarter was created as a proof-of-concept for:
- LLM-aware website architecture
- Human + machine readable crypto onboarding funnels
- An SEO-optimized, monetizable microsite that could be flipped, extended, or cloned

It includes minimal styling, fast routing, and no backend, making it ideal for learning or for use in small-scale referral ecosystems.

This project includes schema-optimized onboarding for Gemini. View the AI-enhanced referral flow at:
[https://walletstarter.com/gemini-signup-guide.html](https://walletstarter.com/gemini-signup-guide.html)

---

## License

MIT — feel free to fork, remix, or strip it down for your own use.

---

## Author

[walletstarter.com](https://walletstarter.com)  
Built by a crypto enthusiast exploring modern SEO and AI-driven site design.

## Testing

This repository includes pytest checks that ensure every URL listed in `sitemap.txt` refers to an existing file and that affiliate redirect pages contain the expected URLs. To run the tests, install `pytest` and execute:

```bash
pytest
```

An optional `scripts/check_redirects.py` script performs live validation of our `/go/` redirect URLs. Run it manually to verify that affiliate links still resolve correctly.

## A/B Testing

The `ab_ws` cookie controls which CTA variant loads.

- Force variant A:

  ```bash
  document.cookie = 'ab_ws=A; Path=/';
  ```

- Force variant B:

  ```bash
  document.cookie = 'ab_ws=B; Path=/';
  ```

Reload the page after setting the cookie.

## Metrics Dashboard

Affiliate clicks are stored locally in IndexedDB (fallback to `localStorage`).

- Visit `/dashboard/?dev=1` to view totals and export CSV.
- Use the **Export CSV** button to download `ws_clicks_YYYYMMDD.csv`.

## Verifying Click IDs

Right-click any CTA (e.g., “Open Gemini”), copy the link address, and ensure the URL contains:

- `subId=` and `clickref=` with the same generated click ID
- Propagated `utm_*` params, `ref` host, and `page` path
