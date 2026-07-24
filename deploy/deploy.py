#!/usr/bin/env python3
"""
deploy.py — deploy the Assam Flood Relief site to Vercel and attach a custom domain.

Run this on YOUR machine (not in a sandbox), from the folder that contains
this script and the sibling "site/" folder with index.html.

Usage:
    python3 deploy.py                     # deploy only
    python3 deploy.py --domain example.com  # deploy + attach domain
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent / "site"


def run(cmd, **kwargs):
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)
    return result


def ensure_vercel_cli():
    if shutil.which("vercel") is None:
        print("Vercel CLI not found. Installing globally via npm...")
        run(["npm", "install", "-g", "vercel"])
    else:
        print("Vercel CLI found.")


def ensure_logged_in():
    result = subprocess.run(["vercel", "whoami"], capture_output=True, text=True)
    if result.returncode != 0:
        print("You're not logged in to Vercel. Opening login flow...")
        run(["vercel", "login"])
    else:
        print(f"Logged in as: {result.stdout.strip()}")


def deploy():
    if not SITE_DIR.exists():
        print(f"Site folder not found at {SITE_DIR}", file=sys.stderr)
        sys.exit(1)
    print(f"Deploying {SITE_DIR} to Vercel (production)...")
    run(["vercel", "--prod", "--yes"], cwd=str(SITE_DIR))


def attach_domain(domain: str):
    print(f"\nAttaching domain '{domain}' to this Vercel project...")
    run(["vercel", "domains", "add", domain], cwd=str(SITE_DIR))
    print(
        "\nDomain added to the project. If it's not verified automatically, "
        "Vercel will print the DNS records (A/CNAME) you need to add at your "
        "domain registrar. See README.md for the common case."
    )


def main():
    parser = argparse.ArgumentParser(description="Deploy the relief site to Vercel.")
    parser.add_argument("--domain", help="Custom domain to attach, e.g. assamfloodrelief.in")
    args = parser.parse_args()

    ensure_vercel_cli()
    ensure_logged_in()
    deploy()

    if args.domain:
        attach_domain(args.domain)

    print("\nDone. Run 'vercel ls' to see your deployments and their URLs.")


if __name__ == "__main__":
    main()
