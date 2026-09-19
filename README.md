# Privacy Policy Diff

A small privacy engineering project that compares two versions of a privacy policy and highlights what changed.

It compares privacy policy versions and identifies changes related to **data collection, data sharing, retention, cookies, data subject rights, legal bases, and international data transfers**.

It can:

- show added and removed lines
- produce a unified text diff
- detect privacy-related topics in changed text
- generate a simple HTML comparison report

The project uses only Python's standard library.

## Why this project?

Privacy notices change over time. A useful review process should make it easier to spot changes involving topics such as:

- data collection
- sharing with third parties
- retention
- cookies and tracking
- data subject rights
- consent and legal bases
- international transfers
- privacy contacts

This project provides a lightweight example of that workflow.

## Project structure

```text
privacy-policy-diff/
├── privacy_policy_diff.py
├── README.md
├── LICENSE
├── .gitignore
├── samples/
│   ├── policy_v1.txt
│   └── policy_v2.txt
└── output/
    └── .gitkeep
```

## Requirements

Python 3.10+ is recommended.

No third-party packages are required.

## Usage

Compare the sample policies:

```bash
python privacy_policy_diff.py samples/policy_v1.txt samples/policy_v2.txt
```

Generate an HTML report:

```bash
python privacy_policy_diff.py \
  samples/policy_v1.txt \
  samples/policy_v2.txt \
  --html output/report.html
```

Then open:

```text
output/report.html
```

in your browser.

## Example output

```text
Privacy Policy Diff
========================================
Added lines:   8
Removed lines: 5

Privacy topics detected in changed text:
- data collection
- sharing
- retention
- cookies
- rights
- legal basis
- international transfers
```

## How topic detection works

The tool uses a small keyword-based ruleset.

For example:

```python
"retention": ["retain", "retention", "storage period"]
```

If changed text contains one of those terms, the topic is included in the summary.

This keeps the project simple and explainable.

## Limitations

This is an educational tool, not a legal review system.

Keyword matching can miss important changes or produce false positives. A real privacy review process may also require:

- legal interpretation
- semantic comparison
- jurisdiction-specific requirements
- structured notice inventories
- review by privacy professionals

## Possible next steps

- support Markdown and HTML cleaning
- compare privacy policy URLs
- assign change categories
- generate a Markdown summary
- add semantic similarity using NLP
- detect newly introduced third parties
- flag changes to retention periods
- add unit tests
- build a small web interface

## Tech

- Python
- `difflib`
- HTML

## License

MIT

## Author
Created by [giovanna diniz eduardo](https://github.com/gvdiniz) as part of a personal Privacy Engineering portfolio.
