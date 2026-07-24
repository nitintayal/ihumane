# Assam Flood Relief site — deploy guide

## What's here
- `site/index.html` — the page. Single file, no build step. Content (bank
  account, IFSC, PAN, UPI ID, contact number) is copied verbatim from the
  official Government of Assam page: https://cm.assam.gov.in/donate
- `deploy/deploy.py` — CLI that deploys `site/` to Vercel and (optionally)
  attaches your domain.

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
Since you said the domain is already registered, run:
```bash
python3 deploy.py --domain yourdomain.com
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
Edit `site/index.html` directly, then re-run `python3 deploy.py` from the
`deploy/` folder — it redeploys to the same production URL.

## Note on accuracy
Every donation detail on the page (account number, IFSC, PAN, UPI ID,
contact phone) was pulled directly from cm.assam.gov.in/donate on the day
this was built. Before wide distribution, double-check the live official
page in case details changed, and keep the "Donate Now" button pointing at
the official domain rather than duplicating payment collection yourself.
