#!/usr/bin/env python3
import argparse
import http.client
import json
import sys
import datetime
import urllib.parse
import io

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='Operator Name', required=True)
    parser.add_argument('--out', help='Output to file (stdout by default)', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('log', nargs='+', help='URL for log metadata')
    args = parser.parse_args()

    logs = []
    for log in args.log:
        parsed_url = urllib.parse.urlparse(log)
        conn = http.client.HTTPSConnection(parsed_url.netloc)
        conn.request('GET', parsed_url.path)
        data = json.loads(conn.getresponse().read().decode('utf-8'))
        logs.append({
            'friendly_name': data['friendly_name'],
            'log_id': data['log_id'],
            'metadata_url': log,
        })

    data = {
        '$schema': 'https://www.certificate-transparency.org/schemas/operator-list-v1.json',
        'operator_name': args.name,
        'last_updated': datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'logs': logs,
    }

    json.dump(data, args.out, indent=2)
    args.out.write('\n')
    args.out.close()

if __name__ == '__main__':
    main()
