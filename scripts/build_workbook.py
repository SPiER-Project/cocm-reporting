"""Build the reporting workbook from the data contract.

    python3 scripts/build_workbook.py           write the workbooks into web/
    python3 scripts/build_workbook.py --check   exit non-zero if they're out of date

Writes two Excel workbooks, published with the browser calculator:

    web/cocm-workbook.xlsx           the blank template
    web/cocm-workbook-example.xlsx   the same, filled with the guide's example caseload

Each has an Instructions tab, one tab per data-contract table with a dropdown for every
allowed value, date and number checks and a tooltip on each column, and a Columns tab
listing every column. The columns come from docs/reference/data-contract.md, so the
workbook can't drift from the contract.

The .xlsx is written with the standard library (it's a zip of XML files). The output is
byte-for-byte reproducible, which is what lets CI check it.
"""

import csv
import glob
import io
import os
import sys
import tomllib
import zipfile
from datetime import date
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contract  # noqa: E402

ROOT = contract.ROOT
OUT = os.path.join(ROOT, "web")
EXAMPLE = os.path.join(ROOT, "tests", "fixtures", "example-caseload")
PAGE = "https://spier-project.github.io/nys-omh-cocm-caseload-reporting/"
GUIDE = "https://github.com/SPiER-Project/nys-omh-cocm-caseload-reporting"
ROWS = 2000  # rows the dropdowns and checks cover

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
EPOCH = date(1899, 12, 30)  # Excel's day zero, in the 1900 date system

# Cell styles, by index in styles.xml.
DEFAULT, HEADER, DATE, WRAP, TITLE, TEXT = range(6)

STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="{MAIN}">
<numFmts count="1"><numFmt numFmtId="164" formatCode="yyyy-mm-dd"/></numFmts>
<fonts count="3">
<font><sz val="11"/><name val="Calibri"/><family val="2"/></font>
<font><b/><sz val="11"/><name val="Calibri"/><family val="2"/></font>
<font><b/><sz val="14"/><name val="Calibri"/><family val="2"/></font>
</fonts>
<fills count="3">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFE8EEF7"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="6">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="49" fontId="1" fillId="2" borderId="0" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1"/>
<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="49" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>
"""


def esc(text):
    return escape(str(text), {'"': "&quot;"})


def col_letter(n):
    """1 -> A, 27 -> AA."""
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


# ------------------------------------------------------------------------- cells


def cell(ref, value, style):
    if value is None or value == "":
        return ""
    if isinstance(value, date):
        return f'<c r="{ref}" s="{DATE}"><v>{(value - EPOCH).days}</v></c>'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{ref}" s="{style}"><v>{value}</v></c>'
    return f'<c r="{ref}" t="inlineStr" s="{style}"><is><t xml:space="preserve">{esc(value)}</t></is></c>'


def typed(column, text):
    """A CSV value as the Python value to store, by the column's contract type."""
    if text == "":
        return None
    if column["type"] == "date":
        return date.fromisoformat(text)
    if column["type"] == "int":
        return int(text)
    if column["type"] == "decimal":
        return float(text) if "." in text else int(text)
    return text


# ------------------------------------------------------------------------- sheets


def validation(column):
    """The <dataValidation> for a column, with its notes as the input tooltip."""
    t, allowed = column["type"], column["allowed"]
    if column["name"] == "primary_scale":
        allowed = [v for v in contract.instrument_values() if v != "phq2"]
    if t == "bool":
        allowed = ["true", "false"]
    attrs, formula = "", ""
    if allowed:
        attrs = ' type="list" allowBlank="1" showErrorMessage="1" errorTitle="Not an allowed value"' \
                f' error="{esc("Choose one of: " + ", ".join(allowed))[:255]}"'
        formula = f'<formula1>"{esc(",".join(allowed))}"</formula1>'
    elif t == "date":
        attrs = ' type="date" operator="greaterThan" allowBlank="1" showErrorMessage="1"' \
                ' errorTitle="Not a date" error="Enter a date, for example 2025-03-12."'
        formula = "<formula1>1</formula1>"
    elif t in ("int", "decimal"):
        kind = "whole" if t == "int" else "decimal"
        attrs = f' type="{kind}" operator="greaterThanOrEqual" allowBlank="1" showErrorMessage="1"' \
                f' errorTitle="Not a number" error="Enter a {"whole " if t == "int" else ""}number."'
        formula = "<formula1>0</formula1>"
    required = "Required. " if column["required"] else "Optional. "
    prompt = (required + column["notes"])[:255].rstrip()
    return attrs, formula, prompt


def table_sheet(name, columns, rows):
    widths = []
    for c in columns:
        longest = max([len(c["name"])] + [len(str(r.get(c["name"], ""))) for r in rows])
        widths.append(min(max(longest + 3, 12), 45))
    cols = "".join(
        f'<col min="{i}" max="{i}" width="{w}" customWidth="1" '
        f'style="{DATE if c["type"] == "date" else TEXT if c["type"] not in ("int", "decimal") else DEFAULT}"/>'
        for i, (c, w) in enumerate(zip(columns, widths), start=1))
    header = "".join(cell(f"{col_letter(i)}1", c["name"], HEADER) for i, c in enumerate(columns, start=1))
    data = [f'<row r="1">{header}</row>']
    for n, r in enumerate(rows, start=2):
        cells = "".join(cell(f"{col_letter(i)}{n}", typed(c, r.get(c["name"], "")),
                             TEXT if c["type"] not in ("int", "decimal") else DEFAULT)
                        for i, c in enumerate(columns, start=1))
        data.append(f'<row r="{n}">{cells}</row>')
    checks = []
    for i, c in enumerate(columns, start=1):
        attrs, formula, prompt = validation(c)
        ref = f"{col_letter(i)}2:{col_letter(i)}{ROWS}"
        checks.append(f'<dataValidation{attrs} showInputMessage="1" promptTitle="{esc(c["name"])[:32]}"'
                      f' prompt="{esc(prompt)}" sqref="{ref}">{formula}</dataValidation>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<worksheet xmlns="{MAIN}" xmlns:r="{REL}">'
            '<sheetViews><sheetView workbookViewId="0">'
            '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
            '</sheetView></sheetViews><sheetFormatPr defaultRowHeight="15"/>'
            f'<cols>{cols}</cols><sheetData>{"".join(data)}</sheetData>'
            f'<dataValidations count="{len(checks)}">{"".join(checks)}</dataValidations>'
            '</worksheet>')


def text_sheet(lines, widths, selected=False):
    """A sheet of text rows. Each line is a list of cells; a str line is one cell, and a
    line starting with '# ' is a title."""
    cols = "".join(f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>'
                   for i, w in enumerate(widths, start=1))
    rows = []
    for n, line in enumerate(lines, start=1):
        if isinstance(line, str):
            style = TITLE if line.startswith("# ") else WRAP
            line = [line[2:] if line.startswith("# ") else line]
        else:
            style = HEADER if n == 1 or line and line[0] == "Table" else WRAP
        cells = "".join(cell(f"{col_letter(i)}{n}", v, style) for i, v in enumerate(line, start=1))
        rows.append(f'<row r="{n}">{cells}</row>')
    view = ' tabSelected="1"' if selected else ""
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<worksheet xmlns="{MAIN}" xmlns:r="{REL}">'
            f'<sheetViews><sheetView workbookViewId="0"{view}/></sheetViews>'
            f'<sheetFormatPr defaultRowHeight="15"/><cols>{cols}</cols>'
            f'<sheetData>{"".join(rows)}</sheetData></worksheet>')


def instructions(example):
    with open(os.path.join(ROOT, "rules", "calls.toml"), "rb") as f:
        history = tomllib.load(f)["extraction"]["phq_history_months"]
    lines = [
        "# CoCM caseload reporting workbook" + (" (example)" if example else ""),
        "One tab per table of the data contract. Fill them in, then open the calculator page and "
        "add this workbook. It calculates the eleven NYS metrics in your browser; the workbook is "
        "never uploaded.",
        f"Calculator: {PAGE}",
        f"Guide: {GUIDE}",
        "",
        "# How to fill it in",
        "1. Work through the tabs in order. Each row is one fact your registry, EHR or billing "
        "system already records: a patient, a coverage period, an enrollment, a contact, a scale "
        "result, a case review, a practice visit.",
        "2. Click a column heading's cell below it to see what the column holds. Columns with "
        "fixed values have a dropdown.",
        "3. Use the same patient id on every tab: a registry number or another id your site "
        "assigns, never a name. Keep the workbook at your site.",
        "4. Enter dates as dates (for example 2025-03-12). Leave a cell blank if you don't know "
        "the value.",
        "5. Add each month's new rows rather than starting over: the calculator looks back "
        f"to each enrollment, and {history} months for practice-wide PHQ results.",
        "6. Fill in one row on site_month for the month you're reporting.",
        "7. Don't rename the tabs or the column headings; the calculator reads them by name.",
        "",
        "# What goes on each tab",
    ]
    for name, title, _ in contract.tables():
        lines.append([name, title[:1].upper() + title[1:] if title else ""])
    lines += [
        "",
        "How far back to go, and how each table's facts are found in a registry, an EHR or "
        "billing, is in the guide: docs/collecting/overview.md.",
    ]
    if example:
        lines.insert(2, "This copy is filled with the guide's example caseload: ten invented "
                        "patients, reported for March 2025.")
    return lines


def columns_sheet():
    lines = [["Table", "Column", "Required", "Type", "Allowed values", "Notes"]]
    for name, _, columns in contract.tables():
        for c in columns:
            allowed = c["allowed"]
            if c["name"] == "primary_scale":
                allowed = [v for v in contract.instrument_values() if v != "phq2"]
            lines.append([name, c["name"], "yes" if c["required"] else "", c["type"],
                          ", ".join(allowed) if allowed else "", c["notes"]])
    return lines


# ------------------------------------------------------------------------- the file


def zip_bytes(parts):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for path, text in parts:
            info = zipfile.ZipInfo(path, date_time=(2025, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, text)
    return buf.getvalue()


def workbook(data=None):
    """The workbook as bytes. data is {table: [row dicts]} to fill it with, or None."""
    sheets = [("Instructions", text_sheet(instructions(data is not None), [110, 60], selected=True))]
    for name, _, columns in contract.tables():
        sheets.append((name, table_sheet(name, columns, (data or {}).get(name, []))))
    sheets.append(("Columns", text_sheet(columns_sheet(), [16, 26, 10, 10, 40, 90])))

    names = "".join(f'<sheet name="{esc(n)}" sheetId="{i}" r:id="rId{i}"/>'
                    for i, (n, _) in enumerate(sheets, start=1))
    rels = "".join(f'<Relationship Id="rId{i}" Type="{REL}/worksheet" Target="worksheets/sheet{i}.xml"/>'
                   for i in range(1, len(sheets) + 1))
    rels += f'<Relationship Id="rId{len(sheets) + 1}" Type="{REL}/styles" Target="styles.xml"/>'
    overrides = "".join(
        f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for i in range(1, len(sheets) + 1))
    head = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    parts = [
        ("[Content_Types].xml", head +
         '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
         '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
         '<Default Extension="xml" ContentType="application/xml"/>'
         '<Override PartName="/xl/workbook.xml" '
         'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
         '<Override PartName="/xl/styles.xml" '
         'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
         f'{overrides}</Types>'),
        ("_rels/.rels", head + f'<Relationships xmlns="{PKG}">'
         f'<Relationship Id="rId1" Type="{REL}/officeDocument" Target="xl/workbook.xml"/></Relationships>'),
        ("xl/workbook.xml", head + f'<workbook xmlns="{MAIN}" xmlns:r="{REL}">'
         f'<bookViews><workbookView activeTab="0"/></bookViews><sheets>{names}</sheets></workbook>'),
        ("xl/_rels/workbook.xml.rels", head + f'<Relationships xmlns="{PKG}">{rels}</Relationships>'),
        ("xl/styles.xml", STYLES),
    ]
    parts += [(f"xl/worksheets/sheet{i}.xml", xml) for i, (_, xml) in enumerate(sheets, start=1)]
    return zip_bytes(parts)


def example_data():
    data = {}
    for path in sorted(glob.glob(os.path.join(EXAMPLE, "*.csv"))):
        with open(path, newline="") as f:
            data[os.path.splitext(os.path.basename(path))[0]] = list(csv.DictReader(f))
    return data


def outputs():
    return {
        os.path.join(OUT, "cocm-workbook.xlsx"): workbook(),
        os.path.join(OUT, "cocm-workbook-example.xlsx"): workbook(example_data()),
    }


def main(argv):
    stale = []
    for path, content in outputs().items():
        rel = os.path.relpath(path, ROOT)
        if "--check" in argv:
            current = open(path, "rb").read() if os.path.exists(path) else b""
            if current != content:
                stale.append(rel)
        else:
            with open(path, "wb") as f:
                f.write(content)
            print(f"wrote {rel} ({len(content) // 1024} KB)")
    if "--check" in argv:
        for rel in stale:
            print(f"{rel} is out of date; run python3 scripts/build_workbook.py")
        if not stale:
            print("workbooks are up to date")
        return 1 if stale else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
