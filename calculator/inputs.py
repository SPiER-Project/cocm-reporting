"""Reading the command line's inputs: CSV directories, workbooks and FHIR files.

    read_inputs(paths, settings, fhir_patient_identifier=None) -> (sources, notes)

Each source is {table: csv text}: one per CSV directory or workbook, and one for all the
FHIR files together. They're kept apart so each can be pseudonymized before they're
combined (see pseudonym.py).
"""

import glob
import os

from .data import TABLES
from .fhir import read_fhir
from .xlsx import read_workbook


def read_inputs(paths, settings, fhir_patient_identifier=None):
    sources, fhir_texts, notes = [], [], []
    for item in paths:
        files = sorted(glob.glob(os.path.join(item, "*"))) if os.path.isdir(item) else [item]
        if not files or not any(os.path.exists(f) for f in files):
            raise ValueError(f"{item}: not found")
        csvs = {}
        for path in files:
            lower = path.lower()
            if lower.endswith(".xlsx"):
                with open(path, "rb") as f:
                    try:
                        sources.append(read_workbook(f.read()))
                    except ValueError as e:
                        raise ValueError(f"{path}: {e}") from None
            elif lower.endswith((".json", ".ndjson")):
                with open(path) as f:
                    fhir_texts.append(f.read())
            elif lower.endswith(".csv"):
                name = os.path.splitext(os.path.basename(path))[0]
                if name in TABLES:
                    with open(path, newline="") as f:
                        csvs[name] = f.read()
        if csvs:
            sources.append(csvs)
    if fhir_texts:
        try:
            tables, notes = read_fhir(fhir_texts, settings, fhir_patient_identifier)
        except ValueError as e:
            raise ValueError(f"FHIR: {e}") from None
        sources.append(tables)
    return sources, notes
