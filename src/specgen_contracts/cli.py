import argparse
import json
import sys

from .bundle import descriptor, schema_digest, validate


def main(argv=None):
    parser = argparse.ArgumentParser(prog="contract-bundle")
    sub = parser.add_subparsers(dest="command", required=True)
    digest = sub.add_parser("digest"); digest.add_argument("schema_id")
    check = sub.add_parser("validate"); check.add_argument("schema_id"); check.add_argument("document")
    args = parser.parse_args(argv)
    if args.command == "digest":
        print(schema_digest(args.schema_id)); return 0
    document = json.load(open(args.document, encoding="utf-8"))
    errors = validate(args.schema_id, document)
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
