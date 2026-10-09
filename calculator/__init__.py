"""The CoCM caseload calculator: the eleven NYS OMH metrics from the eight data-contract
tables, following the rules in rules/calls.toml.

    from calculator import calculate, read_tables, read_rules
    results = calculate(read_tables({"patient": csv_text, ...}), read_rules(toml_text), "2025-03")

Standard library only, and no file access in the core, so it can run in a browser.
"""

from .compute import calculate
from .data import TABLES, Settings, read_rules, read_tables

__all__ = ["calculate", "read_rules", "read_tables", "Settings", "TABLES"]
