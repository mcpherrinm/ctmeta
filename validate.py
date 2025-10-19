#!/usr/bin/env python3
import argparse
import json
import jsonschema
import pathlib

def main():
    parser = argparse.ArgumentParser()
    schema_group = parser.add_mutually_exclusive_group(required=True)
    schema_group.add_argument(
        '--log', 
        action='store_true',
    )
    schema_group.add_argument(
        '--operator', 
        action='store_true',
    )
    parser.add_argument('json_file')
    args = parser.parse_args()

    if args.log:
        schema_type = 'log-metadata-v1.json'
    elif args.operator:
        schema_type = 'operator-list-v1.json'
    else: # Should be unreachable
        raise 'Unknown schema type'

    with open(pathlib.Path(__file__).parent / "schema" / schema_type, 'r') as f:
        schema = json.load(f)

    with open(args.json_file, 'r') as f:
        data = json.load(f)

    jsonschema.validate(instance=data, schema=schema)

if __name__ == '__main__':
    main()
