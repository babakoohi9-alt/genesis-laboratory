"""Optional independent review of Genesis runs by Anthropic Claude.

Set ANTHROPIC_API_KEY and optionally ANTHROPIC_MODEL in the environment.
The key is read only from the environment and is never written to disk.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

LOG_FILE = Path("genesis_log.jsonl")
OUTPUT_FILE = Path("claude_review.md")
API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"


def latest_records(limit=20):
    if not LOG_FILE.exists():
        return []
    lines = LOG_FILE.read_text().splitlines()
    records = []
    for line in lines[-limit:]:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Claude review skipped: ANTHROPIC_API_KEY is not configured.")
        return 0

    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
    records = latest_records()
    if not records:
        print("Claude review skipped: no experiment records found.")
        return 0

    prompt = (
        "You are the independent scientific reviewer for Genesis, an artificial-life "
        "simulation. Review the experiment records below. Do not assume the model "
        "represents real biology. Identify: (1) what the data actually show, "
        "(2) possible bugs or confounders, (3) one alternative explanation, "
        "(4) one specific next experiment, and (5) confidence and limitations. "
        "Challenge assumptions respectfully. Never invent measurements. "
        "Return a concise Markdown report.\n\n"
        "Recent Genesis records (JSON):\n"
        + json.dumps(records, indent=2)
    )
    payload = {
        "model": model,
        "max_tokens": 1400,
        "messages": [{"role": "user", "content": prompt}],
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        print(f"Claude API returned HTTP {error.code}: {detail}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError) as error:
        print(f"Claude API connection failed: {error}", file=sys.stderr)
        return 1

    answer = "\n".join(
        block.get("text", "")
        for block in result.get("content", [])
        if block.get("type") == "text"
    ).strip()
    if not answer:
        print("Claude returned no text review.", file=sys.stderr)
        return 1

    OUTPUT_FILE.write_text(
        "# Claude's independent Genesis review\n\n"
        f"Model: {model}\n\n"
        + answer
        + "\n"
    )
    print("Claude review saved to claude_review.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
