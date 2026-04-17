#!/usr/bin/env python3
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='Operator Name', required=True)
    parser.add_argument('--out', help='Output to file (stdout by default)', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('log', nargs='+', help='URL for log metadata')
    args = parser.parse_args()

    data = {
        '$schema': 'https://www.certificate-transparency.org/schemas/operator-list-v1.json',
        'operator_name': args.name,
        'logs': args.log,
    }

    json.dump(data, args.out, indent=2)
    args.out.write('\n')
    args.out.close()

if __name__ == '__main__':
    main()
