#!/usr/bin/env python3
"""Fail if the example in quickstart.mdx has drifted from the file it was copied from.

The quickstart embeds checkout_agent.py verbatim. Nothing enforces that by
itself, so the page can keep claiming an output the code it shows can no longer
produce. That has happened before, on the landing page: the block was copied
before a correctness fix landed, and the page printed a claim the code never
checked, directly above terminal output showing the corrected behaviour.

    python3 scripts/check_quickstart_sync.py          # verify
    python3 scripts/check_quickstart_sync.py --fix    # rewrite the page to match

A reachable source that disagrees with the page fails. An unreachable source
warns and passes, because a GitHub outage is not a reason to block a docs change.
"""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

SOURCE = (
    "https://raw.githubusercontent.com/cellaflow/cellaflow-sdks/main"
    "/examples/quickstart/checkout_agent.py"
)
PAGE = Path(__file__).resolve().parent.parent / "quickstart.mdx"

#: The page may hold several Python blocks. The one under guard is the whole
#: example, identified by the function the quickstart is built around. Anchoring
#: on content rather than on position means reordering the page cannot silently
#: point this check at a different block.
ANCHOR = "def checkout("

BLOCK = re.compile(r"(?P<open>```python[^\n]*\n)(?P<body>.*?)(?P<close>```)", re.DOTALL)


def fail(message: str) -> None:
    print(f"  quickstart-sync: {message}", file=sys.stderr)
    sys.exit(1)


def fetch_example() -> str | None:
    try:
        with urllib.request.urlopen(SOURCE, timeout=15) as response:
            if response.status != 200:
                raise urllib.error.URLError(f"HTTP {response.status}")
            return response.read().decode("utf-8")
    except Exception as err:  # noqa: BLE001 - any failure to reach it is the same answer
        print(
            f"  quickstart-sync: SKIPPED, could not reach the example ({err}).\n"
            "  The page was not checked.",
        )
        return None


def main() -> None:
    fix = "--fix" in sys.argv[1:]

    expected = fetch_example()
    if expected is None:
        return
    expected = expected.rstrip("\n")

    if ANCHOR not in expected:
        fail(
            f"{ANCHOR!r} is not in the example any more.\n"
            "  The example was restructured. Update ANCHOR in this script to whatever\n"
            "  now identifies the block the quickstart embeds."
        )

    page = PAGE.read_text(encoding="utf-8")
    matches = [m for m in BLOCK.finditer(page) if ANCHOR in m.group("body")]

    if not matches:
        fail(
            f"no ```python block in {PAGE.name} contains {ANCHOR!r}.\n"
            "  Either the example is no longer on the page, or it was split across\n"
            "  blocks. The page is supposed to show the file in one piece."
        )
    if len(matches) > 1:
        fail(
            f"{len(matches)} ```python blocks in {PAGE.name} contain {ANCHOR!r}.\n"
            "  This check cannot tell which one is the example. Keep one."
        )

    match = matches[0]
    on_page = match.group("body").rstrip("\n")

    if on_page == expected:
        print(f"  quickstart-sync: OK ({len(expected.splitlines())} lines match the example)")
        return

    if fix:
        updated = (
            page[: match.start()]
            + match.group("open")
            + expected
            + "\n"
            + match.group("close")
            + page[match.end() :]
        )
        PAGE.write_text(updated, encoding="utf-8")
        print(f"  quickstart-sync: {PAGE.name} updated to match the example.")
        return

    page_lines = on_page.splitlines()
    example_lines = expected.splitlines()
    first = next(
        (
            n
            for n in range(max(len(page_lines), len(example_lines)))
            if (page_lines[n] if n < len(page_lines) else None)
            != (example_lines[n] if n < len(example_lines) else None)
        ),
        None,
    )
    detail = ""
    if first is not None:
        shown_page = page_lines[first] if first < len(page_lines) else "<missing>"
        shown_example = example_lines[first] if first < len(example_lines) else "<missing>"
        detail = (
            f"    first difference at line {first + 1}:\n"
            f"      page:     {shown_page!r}\n"
            f"      example:  {shown_example!r}\n"
        )

    fail(
        f"the example in {PAGE.name} does NOT match the file it was copied from.\n\n"
        f"    page:     {len(page_lines)} lines\n"
        f"    example:  {len(example_lines)} lines\n"
        f"{detail}\n"
        "  The page has to show code that runs, and that produces the output printed\n"
        "  beside it. Fix with:\n\n"
        "      python3 scripts/check_quickstart_sync.py --fix\n"
    )


if __name__ == "__main__":
    main()
