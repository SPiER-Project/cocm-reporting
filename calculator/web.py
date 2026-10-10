"""The browser page's entry point.

The page runs this module in Pyodide and passes only strings across, so nothing about the
calculation lives in JavaScript:

    run(texts_json, rules_text, month) -> results JSON
    workbook(xlsx_base64) -> {"texts": {table: csv text}} JSON
    fhir(files_json, rules_text, identifier_system) -> {"texts": ..., "notes": [...]} JSON
    merge(texts_json, more_json) -> {table: csv text} JSON
    new_key() -> key text
    pseudonymize(texts_json, key_text) -> {"texts": ..., "crosswalk": [[id, pseudonym]]} JSON
    zip_tables(texts_json) -> base64 of a zip with one CSV per table

texts_json is {"patient": csv text, ...}. The result is the calculator's results plus,
under "rows", each metric's display text, or {"error": message} if the input couldn't be
read.
"""

import base64
import io
import json
import zipfile

from .compute import calculate
from .data import combine, read_rules, read_tables
from .fhir import read_fhir
from .pseudonym import new_key as _new_key
from .pseudonym import pseudonymize as _pseudonymize
from .report import NAMES, value
from .xlsx import read_workbook


def run(texts_json, rules_text, month):
    try:
        texts = json.loads(texts_json)
        results = calculate(read_tables(texts), read_rules(rules_text), month)
    except (ValueError, KeyError, TypeError) as e:
        return json.dumps({"error": str(e)})
    results["rows"] = [{"metric": m[1:], "name": name, "value": value(m, results["metrics"][m])}
                       for m, name in NAMES.items()]
    return json.dumps(results, default=str)


def workbook(data_base64):
    """The tables in a reporting workbook, as {"texts": {table: csv text}} or {"error": ...}."""
    try:
        return json.dumps({"texts": read_workbook(base64.b64decode(data_base64))})
    except (ValueError, KeyError) as e:
        return json.dumps({"error": f"couldn't read the workbook: {e}"})


def fhir(files_json, rules_text, identifier_system=""):
    """FHIR resources (a JSON list of file contents) as tables, with notes for the site."""
    try:
        tables, notes = read_fhir(json.loads(files_json), read_rules(rules_text),
                                  identifier_system or None)
        return json.dumps({"texts": tables, "notes": notes})
    except (ValueError, KeyError) as e:
        return json.dumps({"error": f"couldn't read the FHIR files: {e}"})


def merge(texts_json, more_json):
    """Two sets of tables combined, each fact kept once."""
    return json.dumps(combine(json.loads(texts_json), json.loads(more_json)))


def new_key():
    return _new_key()


def pseudonymize(texts_json, key_text):
    """Patient ids replaced with pseudonyms, and the crosswalk for the site to keep."""
    try:
        tables, crosswalk = _pseudonymize(json.loads(texts_json), key_text)
    except ValueError as e:
        return json.dumps({"error": str(e)})
    return json.dumps({"texts": tables, "crosswalk": crosswalk})


def zip_tables(texts_json):
    """A zip of one CSV per table, as base64, for the page to offer as a download."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for table, text in json.loads(texts_json).items():
            z.writestr(f"{table}.csv", text)
    return base64.b64encode(buf.getvalue()).decode()
