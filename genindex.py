#!/usr/bin/env python3
"""Generate an index.html listing all operator and log metadata files."""

import argparse
import html
import json
import sys
from pathlib import Path


def load_json(path: Path):
    try:
        with path.open() as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"warning: could not read {path}: {e}", file=sys.stderr)
        return None


def render(operators_dir: Path) -> str:
    lines = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>CT Operator Metadata</title>",
        "<style>",
        "body { font-family: sans-serif; max-width: 50rem; margin: 2rem auto; padding: 0 1rem; }",
        "h1 { border-bottom: 1px solid #ccc; padding-bottom: 0.25rem; }",
        "h2 { margin-top: 2rem; }",
        "ul { line-height: 1.6; }",
        "code { background: #f4f4f4; padding: 0 0.25rem; border-radius: 3px; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>CT Operator Metadata</h1>",
        "<p>Operator-published Certificate Transparency log metadata.</p>",
    ]

    for operator_dir in sorted(p for p in operators_dir.iterdir() if p.is_dir()):
        operator_file = operator_dir / "operator.json"
        if not operator_file.is_file():
            continue
        data = load_json(operator_file)
        name = (data or {}).get("operator_name") or operator_dir.name
        operator_href = f"{operator_dir.name}/operator.json"
        lines.append(f"<h2>{html.escape(name)}</h2>")
        lines.append(
            f'<p>Operator file: <a href="{html.escape(operator_href)}">'
            f"<code>{html.escape(operator_href)}</code></a></p>"
        )

        logs_dir = operator_dir / "logs"
        if logs_dir.is_dir():
            log_files = sorted(p for p in logs_dir.iterdir() if p.suffix == ".json")
            if log_files:
                lines.append("<ul>")
                for log_file in log_files:
                    rel = f"{operator_dir.name}/logs/{log_file.name}"
                    log_data = load_json(log_file) or {}
                    friendly = log_data.get("friendly_name") or log_file.stem
                    status = log_data.get("status")
                    label = html.escape(friendly)
                    if status:
                        label += f" <em>({html.escape(status)})</em>"
                    lines.append(
                        f'<li><a href="{html.escape(rel)}">{label}</a> '
                        f'&mdash; <code>{html.escape(rel)}</code></li>'
                    )
                lines.append("</ul>")

    lines.append("</body></html>")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--operators",
        default="operators",
        type=Path,
        help="Path to the operators directory (default: operators)",
    )
    parser.add_argument(
        "--output",
        default=None,
        type=Path,
        help="Output HTML file (default: <operators>/index.html)",
    )
    args = parser.parse_args()

    if not args.operators.is_dir():
        print(f"error: {args.operators} is not a directory", file=sys.stderr)
        return 1

    output = args.output or (args.operators / "index.html")
    output.write_text(render(args.operators))
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
