"""The browser page's entry point.

The page runs this module in Pyodide and passes only strings across, so nothing about the
calculation lives in JavaScript:

    run(texts_json, rules_text, month) -> results JSON

texts_json is {"patient": csv text, ...}. The result is the calculator's results plus,
under "rows", each metric's display text, or {"error": message} if the input couldn't be
read.
"""

import json

from .compute import calculate
from .data import read_rules, read_tables
from .report import NAMES, value


def run(texts_json, rules_text, month):
    try:
        texts = json.loads(texts_json)
        results = calculate(read_tables(texts), read_rules(rules_text), month)
    except (ValueError, KeyError, TypeError) as e:
        return json.dumps({"error": str(e)})
    results["rows"] = [{"metric": m[1:], "name": name, "value": value(m, results["metrics"][m])}
                       for m, name in NAMES.items()]
    return json.dumps(results, default=str)
