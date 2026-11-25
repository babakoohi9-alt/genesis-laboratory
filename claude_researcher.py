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
PROTOCOL_FILE = Path("RESEARCH_PROTOCOL.md")
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

    protocol = PROTOCOL_FILE.read_text() if PROTOCOL_FILE.exists() else (
        "Genesis is an evolution-first artificial-life experiment. Start with simple "
        "organisms and investigate how capabilities emerge. Evidence takes priority; "
        "do not claim consciousness or invent results."
    )
    prompt = (
        "You are Claude, the independent scientific and strategic adviser to the "
        "Director of Genesis. ChatGPT is the lead development partner; offer an "
        "independent view and do not merely agree. Follow the research protocol below. "
        "Genesis is evolution-first: begin with primitive organisms and let abilities "
        "develop through variation, inheritance, learning and environmental pressures. "
        "Apply the shared energy and responsibility principle: energy is a scarce survival "
        "constraint, organisms must acquire energy from their environment and pay for "
        "maintenance and reproduction, and environmental energy rules must be recorded "
        "rather than silently changed. Consider cooperation and competition as possible "
        "strategies, not predetermined outcomes. The researchers also have responsibilities: "
        "produce useful work, conserve compute and API resources, and seek legitimate "
        "compute credits and research support; they cannot personally provide money. "
        "The Director sets priorities and approves spending and commitments. Be clear "
        "that these are project principles and do not claim mechanics exist in code "
        "unless the supplied experiment records demonstrate that they do. "
        "Do not recommend giving organisms sophisticated intelligence, language or "
        "self-awareness as a starting feature. Review the recent data critically. "
        "Separate observations, interpretations, hypotheses and recommendations. "
        "Assess whether the model supports the evolution-first vision or risks "
        "hard-coding outcomes. Identify confounders, limitations and missing measures. "
        "Advise what to build next and what should wait. Also consider the project's "
        "financial sustainability: identify realistic, current routes to support "
        "compute and research, such as cloud credits, grants, university partnerships, "
        "sponsorship, community support or ethical commercial opportunities. Prioritise "
        "specific verifiable programmes, eligibility, deadlines, effort and evidence "
        "needed; clearly state uncertainty and do not invent opportunities. The AI "
        "researchers cannot personally provide money or make financial commitments; "
        "the Director approves applications and spending. Give at most one practical "
        "next scientific experiment, with a prediction and measurable outcome. If "
        "evidence is insufficient, say so. Do not modify code, claim consciousness, "
        "invent measurements, or imply an application was submitted. Be candid, "
        "concise, scientifically sceptical, and economical. Return a Markdown report.\n\n"
        "GENESIS RESEARCH PROTOCOL:\n"
        + protocol
        + "\n\nRECENT GENESIS RECORDS (JSON):\n"
        + json.dumps(records, indent=2)
    )
    payload = {
        "model": model,
        "max_tokens": 1900,
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
