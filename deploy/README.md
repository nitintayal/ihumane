# iHumane site — deploy guide

## What's here
- `site/index.html` — generic homepage. Mission/how-it-works copy plus a
  compact callout for whichever cause is currently active, linking out to
  its dedicated page.
- `site/assamfloods.html` — the Assam Floods 2026 cause page, served at
  `ihumane.in/assamfloods`. Content (bank account, IFSC, PAN, UPI ID,
  contact number) is copied verbatim from the official Government of Assam
  page: https://cm.assam.gov.in/donate
- `site/vercel.json` — sets `cleanUrls: true` so `assamfloods.html` is
  reachable at `/assamfloods` (no `.html`, no trailing slash).
- `deploy/deploy.py` — CLI that deploys `site/` to Vercel and (optionally)
  attaches your domain.

## Adding a future cause
1. Copy `site/assamfloods.html` to `site/<causename>.html` and update its
   content (title, meta tags, figures, bank/UPI details, canonical URL).
2. Update the "Current cause" callout in `site/index.html` to point at
   `/<causename>` (and archive the old cause's link somewhere if you want
   to keep it reachable).
3. Redeploy (see below) — no `vercel.json` changes needed, `cleanUrls`
   already covers any `<name>.html` file in `site/`.

## One-time setup (on your own machine)
1. Install Node.js if you don't have it (needed for the Vercel CLI):
   https://nodejs.org
2. Have a Vercel account (free tier is fine): https://vercel.com/signup

## Deploy
```bash
cd deploy
python3 deploy.py
```
This installs the Vercel CLI if missing, opens a browser login the first
time, then deploys `site/` and prints your live `*.vercel.app` URL.

## Attach your domain
Since ihumane.in is already registered, run:
```bash
python3 deploy.py --domain ihumane.in
```
Vercel will either verify it automatically (if it detects the registrar) or
print DNS records to add. In the common case, at your domain registrar
(GoDaddy, Namecheap, BigRock, etc.) add:

| Type  | Host | Value                  |
|-------|------|-------------------------|
| A     | @    | 76.76.21.21              |
| CNAME | www  | cname.vercel-dns.com     |

DNS changes can take a few minutes to a few hours to propagate. Once done,
`vercel domains inspect yourdomain.com` will confirm it's verified.

## Updating content later
Edit `site/index.html` (homepage) or `site/assamfloods.html` (cause page)
directly, then re-run `python3 deploy.py` from the `deploy/` folder — it
redeploys to the same production URL.

## Note on accuracy
Every donation detail on the page (account number, IFSC, PAN, UPI ID,
contact phone) was pulled directly from cm.assam.gov.in/donate on the day
this was built. Before wide distribution, double-check the live official
page in case details changed, and keep the "Donate Now" button pointing at
the official domain rather than duplicating payment collection yourself.
