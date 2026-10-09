"""Build the browser calculator, web/index.html, from web/template.html.

    python3 scripts/build_web.py           write web/index.html
    python3 scripts/build_web.py --check   exit non-zero if web/index.html is out of date

The page is one self-contained file: the calculator's Python source, rules/calls.toml and
the example caseload are inlined, so it works from GitHub Pages, from a downloaded copy,
or from a file on a shared drive. Only Pyodide, the Python engine, is fetched from its CDN.
"""

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "web", "template.html")
OUTPUT = os.path.join(ROOT, "web", "index.html")
PYODIDE_VERSION = "v0.26.4"  # Python 3.12, which includes tomllib
SKIP = {"__main__.py"}       # the command-line entry point reads files; the page doesn't


def embed(value):
    """JSON that's safe inside a <script type="application/json"> element."""
    return json.dumps(value, sort_keys=True).replace("</", "<\\/")


def build():
    sources = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "calculator", "*.py"))):
        if os.path.basename(path) not in SKIP:
            with open(path) as f:
                sources[os.path.basename(path)] = f.read()
    with open(os.path.join(ROOT, "rules", "calls.toml")) as f:
        rules = f.read()
    example = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "tests", "fixtures", "example-caseload", "*.csv"))):
        with open(path) as f:
            example[os.path.splitext(os.path.basename(path))[0]] = f.read()
    with open(TEMPLATE) as f:
        page = f.read()
    for placeholder, value in (
        ("__CALCULATOR_SOURCES__", embed(sources)),
        ("__RULES__", embed(rules)),
        ("__EXAMPLE_CASELOAD__", embed(example)),
        ("__PYODIDE_VERSION__", PYODIDE_VERSION),
    ):
        if placeholder not in page:
            raise SystemExit(f"web/template.html has no {placeholder}")
        page = page.replace(placeholder, value)
    return page


def main(argv):
    page = build()
    if "--check" in argv:
        current = open(OUTPUT).read() if os.path.exists(OUTPUT) else ""
        if current != page:
            print("web/index.html is out of date; run python3 scripts/build_web.py")
            return 1
        print("web/index.html is up to date")
        return 0
    with open(OUTPUT, "w") as f:
        f.write(page)
    print(f"wrote web/index.html ({len(page) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
