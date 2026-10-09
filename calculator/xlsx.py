"""Reading the reporting workbook (.xlsx) into the data-contract tables.

    read_workbook(data) -> {table: csv text}

The workbook has one tab per table, named after it, with the column names in row 1. Other
tabs (Instructions, Columns) are ignored. The result is the same CSV text the calculator
reads from files, so a workbook and a directory of CSVs go through the same checks.

Written with the standard library only: an .xlsx is a zip of XML files. It reads what
Excel, Google Sheets, Numbers and LibreOffice save, including shared strings and dates
stored as Excel serial numbers.
"""

import csv
import io
import re
import zipfile
from datetime import date, datetime, timedelta
from xml.etree import ElementTree

from .data import BOOLS, INTS, TABLES

EPOCH = date(1899, 12, 30)  # Excel's day zero, in the 1900 date system
TRUE = {"true", "yes", "y", "1"}
FALSE = {"false", "no", "n", "0"}


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _find(element, name):
    return [e for e in element.iter() if _local(e.tag) == name]


def _text(element):
    """All the text in an <si> or <is>, joining rich-text runs."""
    return "".join(t.text or "" for t in element.iter() if _local(t.tag) == "t")


def _column_index(ref):
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def _number(text):
    value = float(text)
    return str(int(value)) if value.is_integer() else str(value)


def _date(value, is_number, month_only=False):
    """An Excel serial number or a typed date, as ISO text."""
    if is_number:
        d = EPOCH + timedelta(days=int(float(value)))
    else:
        value = value.strip()
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y/%m/%d", "%Y-%m"):
            try:
                d = datetime.strptime(value, fmt).date()
                break
            except ValueError:
                continue
        else:
            return value  # leave it for the calculator to report
    return d.strftime("%Y-%m") if month_only else d.isoformat()


def _convert(column, value, kind):
    """A cell's raw value as contract text. kind is 'n' (number), 'b' (boolean) or 's'."""
    if value is None or value == "":
        return ""
    if column.endswith("_date"):
        return _date(value, kind == "n")
    if column == "reporting_month":
        return _date(value, kind == "n", month_only=True)
    if column in BOOLS:
        v = str(value).strip().lower()
        return "true" if v in TRUE else "false" if v in FALSE else v
    if kind == "n":
        return _number(value)
    value = str(value).strip()
    if column in INTS and re.fullmatch(r"-?\d+\.0+", value):
        return value.split(".")[0]
    return value


def read_workbook(data):
    """{table: csv text} from the bytes of a reporting workbook."""
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        raise ValueError("not an Excel workbook (.xlsx)") from None
    names = set(z.namelist())

    shared = []
    if "xl/sharedStrings.xml" in names:
        root = ElementTree.fromstring(z.read("xl/sharedStrings.xml"))
        shared = [_text(si) for si in root if _local(si.tag) == "si"]

    book = ElementTree.fromstring(z.read("xl/workbook.xml"))
    rels = ElementTree.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    targets = {r.get("Id"): r.get("Target") for r in rels if _local(r.tag) == "Relationship"}

    tables = {}
    for sheet in _find(book, "sheet"):
        table = (sheet.get("name") or "").strip().lower()
        if table not in TABLES:
            continue
        rid = next(v for k, v in sheet.attrib.items() if _local(k) == "id")
        target = targets[rid].lstrip("/")
        path = target if target.startswith("xl/") else "xl/" + target
        root = ElementTree.fromstring(z.read(path))

        grid = []
        for row in _find(root, "row"):
            values = {}
            for i, c in enumerate(e for e in row if _local(e.tag) == "c"):
                index = _column_index(c.get("r")) if c.get("r") else i
                t = c.get("t", "n")
                v = next((e.text for e in c if _local(e.tag) == "v"), None)
                if t == "s" and v is not None:
                    values[index] = (shared[int(v)], "s")
                elif t == "inlineStr":
                    inline = next((e for e in c if _local(e.tag) == "is"), None)
                    values[index] = (_text(inline) if inline is not None else "", "s")
                elif t == "b":
                    values[index] = ("true" if v == "1" else "false", "b")
                elif t in ("str", "e"):
                    values[index] = (v or "" if t == "str" else "", "s")
                elif v is not None:
                    values[index] = (v, "n")
            grid.append(values)
        if not grid:
            tables[table] = ""
            continue

        header = [(i, str(v).strip()) for i, (v, _) in sorted(grid[0].items()) if str(v).strip()]
        out = io.StringIO()
        writer = csv.writer(out, lineterminator="\n")
        writer.writerow([name for _, name in header])
        for values in grid[1:]:
            row = [_convert(name, *values.get(i, ("", "s"))) for i, name in header]
            if any(row):
                writer.writerow(row)
        tables[table] = out.getvalue()
    if not tables:
        raise ValueError("the workbook has no tabs named after data-contract tables")
    return tables
