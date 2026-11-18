"""Submit an A-record lookup in WebDig and print the IPv4 addresses."""

import argparse
import re
from ipaddress import IPv4Address

from playwright.sync_api import Error, sync_playwright

WEB_DIG_URL = "https://webdig.yzernetwork.ca/"
A_RECORD = re.compile(r"^\S+\s+\d+\s+IN\s+A\s+(\S+)\s*$", re.MULTILINE)


def lookup(hostname, *, executable_path=None, proxy_server=None):
    launch_options = {}
    if executable_path:
        launch_options["executable_path"] = executable_path
    if proxy_server:
        launch_options["proxy"] = {"server": proxy_server}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(**launch_options)
        try:
            page = browser.new_page()
            page.goto(WEB_DIG_URL, wait_until="domcontentloaded")
            page.locator("#hostnames").fill(hostname)
            page.locator("#record-type").select_option("A")
            page.locator("#dig").click()

            output = page.locator("#results:not([hidden]) #output")
            error = page.locator("#status.error:visible")
            output.or_(error).first.wait_for()
            if error.is_visible():
                raise RuntimeError(error.inner_text())
            return output.inner_text()
        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hostname", nargs="?", default="www.giumarcian.com")
    parser.add_argument("--chromium", help="Path to an installed Chromium executable")
    parser.add_argument("--proxy", help="Browser proxy URL")
    parser.add_argument("--raw", action="store_true", help="Print the full WebDig output")
    args = parser.parse_args()
    hostname = args.hostname.strip()
    if not hostname or any(character.isspace() for character in hostname):
        parser.error("Provide one hostname without whitespace.")

    try:
        output = lookup(hostname, executable_path=args.chromium, proxy_server=args.proxy)
        addresses = list(dict.fromkeys(str(IPv4Address(value)) for value in A_RECORD.findall(output)))
    except (Error, RuntimeError, ValueError) as exc:
        parser.exit(1, f"Lookup failed for {hostname}: {exc}\n")

    if args.raw:
        print(output)
    if not addresses:
        parser.exit(1, f"WebDig returned no IPv4 A records for {hostname}.\n")
    if not args.raw:
        print("\n".join(addresses))


if __name__ == "__main__":
    main()
