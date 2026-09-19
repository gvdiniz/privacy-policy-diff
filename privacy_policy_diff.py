import argparse
import difflib
import html
from pathlib import Path


PRIVACY_TOPICS = {
    "data collection": ["collect", "collection", "dados coletados", "coletamos"],
    "sharing": ["share", "sharing", "third party", "third-party", "compartilh", "terceiros"],
    "retention": ["retain", "retention", "storage period", "retenção", "armazen"],
    "cookies": ["cookie", "tracking", "rastreamento"],
    "rights": ["rights", "access", "delete", "deletion", "correction", "direitos", "acesso", "exclusão", "correção"],
    "legal basis": ["legal basis", "consent", "legitimate interest", "base legal", "consentimento", "legítimo interesse"],
    "international transfers": ["international transfer", "cross-border", "transferência internacional"],
    "contact": ["contact", "dpo", "privacy officer", "contato", "encarregado"],
}


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def changed_lines(old_text: str, new_text: str):
    diff = difflib.ndiff(old_text.splitlines(), new_text.splitlines())
    removed, added = [], []

    for line in diff:
        if line.startswith("- "):
            removed.append(line[2:])
        elif line.startswith("+ "):
            added.append(line[2:])

    return removed, added


def detect_topics(lines):
    joined = "\n".join(lines).lower()
    matches = []

    for topic, keywords in PRIVACY_TOPICS.items():
        if any(keyword in joined for keyword in keywords):
            matches.append(topic)

    return matches


def build_unified_diff(old_text: str, new_text: str, old_name: str, new_name: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            fromfile=old_name,
            tofile=new_name,
            lineterm="",
        )
    )


def build_html_report(
    old_text: str,
    new_text: str,
    old_name: str,
    new_name: str,
    removed,
    added,
    topics,
) -> str:
    differ = difflib.HtmlDiff(wrapcolumn=90)
    diff_table = differ.make_table(
        old_text.splitlines(),
        new_text.splitlines(),
        fromdesc=html.escape(old_name),
        todesc=html.escape(new_name),
        context=True,
        numlines=3,
    )

    topic_items = "".join(f"<li>{html.escape(topic)}</li>" for topic in topics)
    if not topic_items:
        topic_items = "<li>No configured privacy topic was detected in the changed lines.</li>"

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Privacy Policy Diff Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    max-width: 1200px;
    margin: 40px auto;
    padding: 0 20px;
    line-height: 1.5;
}}
h1, h2 {{ margin-bottom: 0.4rem; }}
.summary {{
    background: #f4f4f4;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 24px;
}}
table.diff {{
    width: 100%;
    border-collapse: collapse;
    font-family: monospace;
    font-size: 13px;
}}
.diff_header {{ background: #eaeaea; }}
td, th {{ padding: 4px 6px; vertical-align: top; }}
.diff_add {{ background: #d8f5d0; }}
.diff_sub {{ background: #ffd6d6; }}
.diff_chg {{ background: #fff3b0; }}
</style>
</head>
<body>
<h1>Privacy Policy Diff Report</h1>

<div class="summary">
<p><strong>Old version:</strong> {html.escape(old_name)}</p>
<p><strong>New version:</strong> {html.escape(new_name)}</p>
<p><strong>Added lines:</strong> {len(added)}</p>
<p><strong>Removed lines:</strong> {len(removed)}</p>

<h2>Privacy topics detected in changed text</h2>
<ul>{topic_items}</ul>
</div>

<h2>Visual comparison</h2>
{diff_table}

</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Compare two privacy policy versions and highlight relevant changes."
    )
    parser.add_argument("old", help="Path to the older policy file")
    parser.add_argument("new", help="Path to the newer policy file")
    parser.add_argument(
        "--html",
        default=None,
        help="Optional path for an HTML diff report",
    )
    args = parser.parse_args()

    old_text = read_text(args.old)
    new_text = read_text(args.new)

    removed, added = changed_lines(old_text, new_text)
    topics = detect_topics(removed + added)
    unified = build_unified_diff(old_text, new_text, args.old, args.new)

    print("Privacy Policy Diff")
    print("=" * 40)
    print(f"Added lines:   {len(added)}")
    print(f"Removed lines: {len(removed)}")
    print()

    if topics:
        print("Privacy topics detected in changed text:")
        for topic in topics:
            print(f"- {topic}")
    else:
        print("No configured privacy topic was detected in the changed lines.")

    print("\nUnified diff:")
    print(unified or "No differences found.")

    if args.html:
        output = Path(args.html)
        output.parent.mkdir(parents=True, exist_ok=True)
        report = build_html_report(
            old_text,
            new_text,
            args.old,
            args.new,
            removed,
            added,
            topics,
        )
        output.write_text(report, encoding="utf-8")
        print(f"\nHTML report saved to: {output}")


if __name__ == "__main__":
    main()
