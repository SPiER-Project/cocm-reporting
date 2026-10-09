"""The data contract's tables, read from docs/reference/data-contract.md.

The contract page is the source of truth for the eight tables. Scripts that need the
columns (the fixture check, the workbook builder) read them from there, so a change to the
contract reaches them without a second copy to keep in step.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTRACT = os.path.join(ROOT, "docs", "reference", "data-contract.md")


def plain(markdown):
    """Notes text without Markdown: links become their text, backticks go."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", markdown)
    return text.replace("`", "").strip()


def tables():
    """[(table, title, [column, ...])] in contract order. Each column is a dict with
    name, type, required, allowed (a list, or None) and notes."""
    text = open(CONTRACT).read()
    out = []
    for m in re.finditer(r"^### T\d+\. `(\w+)`(.*?)\n\n(\|.*?)\n\n", text, re.M | re.S):
        name, title = m.group(1), m.group(2).strip(" —")
        columns = []
        for row in m.group(3).splitlines()[2:]:
            cells = [c.strip() for c in row.strip("|").split("|")]
            col, typ, req, notes = cells[0].strip("`"), cells[1], cells[2] == "✓", cells[3]
            allowed = None
            if typ == "enum" and " · " in notes:
                first = re.split(r"\. |$", notes, maxsplit=1)[0]
                allowed = re.findall(r"`(\w+)`", first)
            columns.append({"name": col, "type": typ, "required": req,
                            "allowed": allowed, "notes": plain(notes)})
        out.append((name, title, columns))
    return out


def instrument_values():
    """The allowed values of scale_result.instrument."""
    for name, _, columns in tables():
        if name == "scale_result":
            return next(c["allowed"] for c in columns if c["name"] == "instrument")
    raise KeyError("scale_result.instrument")
