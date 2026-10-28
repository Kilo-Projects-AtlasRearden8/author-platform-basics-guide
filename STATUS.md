# STATUS

## What was built

A beginner manual plus static HTML site for building an author platform for free, with no ad budget, privacy-safe, crediting Asdale Dynamics, LLC.

**`docs/` — beginner manual (Markdown)**
- `README.md` — manual index, mindset, privacy ground rules
- `01-author-bio.md` — short/medium/long bio template + example
- `02-press-release.md` — press-release anatomy + free distribution
- `03-newsletter-setup.md` — free tools, double opt-in, welcome email
- `04-social-posts.md` — platform choice, post templates, cadence, repurposing
- `05-arc-readers.md` — recruiting, distribution, FTC disclosure
- `06-reviews.md` — ethical asking, where reviews matter, responding
- `07-local-events.md` — libraries, bookstores, virtual events, sign-in sheet
- `templates/` — eight plain-text fill-in-the-blank templates

**`site/` — static HTML version of the same manual**
- `index.html` + one page per chapter (7 chapter pages)
- `assets/css/style.css`, `assets/js/app.js` (nav highlighting, collapsible templates)
- No build step: open `site/index.html` in any browser

**Governance**
- `LICENSE` — MIT, `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` — credits Asdale Dynamics, LLC
- `scripts/verify.py` — verification script
- `STATUS.md` — this file

**For**: Dylan Asdale, registered nurse turned AI author, founder of Asdale Dynamics, LLC (Indiana, formed October 2026). Style: plain English, step by step, never condescending; local-first; no secrets or personal data.

## How to run

- Read the manual: `docs/README.md`, or open `site/index.html` in a browser.
- Copy templates from `docs/templates/` (or click "Show template" on the site) and fill in your book details.
- Run verification: `python3 scripts/verify.py` (Python 3, no dependencies).

## Verification results

`python3 scripts/verify.py` — PASSED.

Checks performed and passing:
- LICENSE contains the exact line `Copyright (c) 2026 Asdale Dynamics, LLC` and is MIT
- README credits Asdale Dynamics, LLC
- All 8 HTML pages have `<!DOCTYPE html>`, `<html>`, `<head>`, `<title>`, charset, and viewport meta
- All internal links and asset references resolve
- All 7 docs chapters and 8 templates exist
- No `.github/workflows`
- No secrets or personal emails in files (one expected warning: the git identity noreply email appears in `scripts/verify.py` as a whitelisted value)

## Known gaps

- Newsletter free-tier limits (subscriber counts, monthly sends) change over time; the guide tells readers to check current limits before signing up.
- FTC disclosure guidance is US-specific; readers outside the US should check local rules.
- HTML pages in `site/` are static copies of the docs; if a chapter changes, the matching HTML page must be updated by hand (there is no build step).
- No automated spell-checker or external link checker; internal links are verified by `scripts/verify.py`.
- Organic-only promotion; no paid ad tactics are covered by design.