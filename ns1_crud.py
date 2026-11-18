#!/usr/bin/env python3
"""Manage NS1 DNS zones and records. Install the SDK with: pip install ns1-python."""

import argparse
import base64
import json
import os
import sys
from pathlib import Path


class TSIGUpdateError(Exception):
    """Invalid key file or missing secondary-zone configuration."""


def answer_tuple(value):
    """Parse one DNS answer, including multi-field answers such as MX."""
    try:
        fields = json.loads(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a JSON array of answer fields") from exc
    if not isinstance(fields, list) or not fields:
        raise argparse.ArgumentTypeError("expected a nonempty JSON array of answer fields")
    return fields


def build_parser():
    parser = argparse.ArgumentParser(
        description="Manage NS1 DNS zones and records using NS1_API_KEY."
    )
    resources = parser.add_subparsers(dest="resource", required=True)
    for resource in ("zone", "record"):
        group = resources.add_parser(resource)
        actions = group.add_subparsers(dest="action", required=True)
        for action in ("list", "get", "create", "update", "delete"):
            command = actions.add_parser(action)
            if resource == "record" or action != "list":
                command.add_argument("zone", help="NS1 zone name, e.g. example.com")
            if resource == "record" and action != "list":
                command.add_argument("domain", help="Full record name, e.g. www.example.com")
                command.add_argument("type", type=str.upper, help="DNS record type")
            if action in ("create", "update"):
                command.add_argument("--ttl", type=int, help="TTL in seconds")
                if resource == "zone" and action == "update":
                    command.add_argument(
                        "--tsig-key-file", type=Path,
                        help="File containing only the new base64 TSIG secret for a secondary zone",
                    )
                if resource == "record":
                    answers = command.add_mutually_exclusive_group(required=action == "create")
                    answers.add_argument(
                        "--answer", action="append", help="Single-field answer, repeatable"
                    )
                    answers.add_argument(
                        "--answer-tuple", action="append", type=answer_tuple,
                        help='JSON array for one answer, e.g. \'[10, "mail.example.com"]\'',
                    )
    return parser


def secondary_with_new_key(resource, zone, key_file):
    try:
        key = key_file.read_text(encoding="ascii").strip()
        if not base64.b64decode(key, validate=True):
            raise ValueError
    except ValueError:
        raise TSIGUpdateError("TSIG key file must contain a nonempty base64 secret") from None
    except OSError as exc:
        raise TSIGUpdateError(f"could not read TSIG key file: {exc.strerror}") from None

    secondary = resource.retrieve(zone).get("secondary")
    if not isinstance(secondary, dict) or not secondary.get("enabled"):
        raise TSIGUpdateError("TSIG key rotation requires an enabled secondary zone")
    tsig = secondary.get("tsig")
    if not isinstance(tsig, dict) or not tsig.get("name") or not tsig.get("hash"):
        raise TSIGUpdateError("the zone must already have a TSIG key name and hash configured")

    # Leave transfer status fields out of the update payload.
    updated = {
        name: value for name, value in secondary.items()
        if name not in ("expired", "last_xfr", "status", "error")
    }
    updated["tsig"] = dict(tsig, key=key)
    return updated


def redact_tsig_keys(value):
    if isinstance(value, list):
        return [redact_tsig_keys(item) for item in value]
    if isinstance(value, dict):
        result = {name: redact_tsig_keys(item) for name, item in value.items()}
        tsig = result.get("tsig")
        if isinstance(tsig, dict) and "key" in tsig:
            tsig["key"] = "[redacted]"
        return result
    return value


def run(client, args):
    if args.action == "list":
        if args.resource == "zone":
            return client.zones().list()
        return client.zones().retrieve(args.zone)["records"]

    identifiers = [args.zone]
    if args.resource == "record":
        resource = client.records()
        identifiers.extend((args.domain, args.type))
    else:
        resource = client.zones()

    if args.action == "get":
        return resource.retrieve(*identifiers)
    if args.action == "delete":
        return resource.delete(*identifiers)

    fields = {}
    if args.ttl is not None:
        fields["ttl"] = args.ttl
    if args.resource == "record":
        answers = args.answer if args.answer is not None else args.answer_tuple
        if answers is not None:
            fields["answers"] = answers
    if args.action == "create":
        return resource.create(*identifiers, **fields)
    if args.resource == "zone" and args.tsig_key_file is not None:
        fields["secondary"] = secondary_with_new_key(resource, args.zone, args.tsig_key_file)
    return resource.update(*identifiers, **fields)


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.action in ("create", "update") and args.ttl is not None and args.ttl < 0:
        parser.error("--ttl must be nonnegative")
    rotating_tsig = getattr(args, "tsig_key_file", None) is not None
    if args.action == "update" and args.ttl is None:
        if args.resource == "zone" and not rotating_tsig:
            parser.error("update requires --ttl or --tsig-key-file")
        if args.resource == "record" and args.answer is None and args.answer_tuple is None:
            parser.error("update requires at least one field to change")

    api_key = os.environ.get("NS1_API_KEY", "").strip()
    if not api_key:
        parser.error("set NS1_API_KEY to your NS1 API key")

    try:
        from ns1 import NS1
        from ns1.rest.errors import ResourceException
    except ImportError:
        parser.exit(1, "Install the NS1 SDK with: python3 -m pip install ns1-python\n")

    try:
        result = run(NS1(apiKey=api_key), args)
    except TSIGUpdateError as exc:
        parser.exit(1, f"{exc}\n")
    except (ResourceException, OSError) as exc:
        if rotating_tsig:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            detail = f" (HTTP {status})" if status is not None else ""
            parser.exit(1, f"NS1 TSIG request failed{detail}\n")
        parser.exit(1, f"NS1 request failed: {exc}\n")
    print(json.dumps(redact_tsig_keys(result), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
