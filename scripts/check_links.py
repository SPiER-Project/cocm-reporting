"""Check that every relative link and #anchor in the repo's Markdown files resolves.

Run from the repo root: python3 scripts/check_links.py
Exits non-zero if anything is broken. External (http) links are not checked.
"""

import glob
import os
import re
import sys


def slug(heading):
    # GitHub's anchor rule: lowercase, drop punctuation except hyphens and underscores,
    # spaces to hyphens.
    heading = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return heading.replace(" ", "-")


def main():
    files = [os.path.normpath(f) for f in glob.glob("**/*.md", recursive=True)]
    anchors = {
        f: {slug(h) for h in re.findall(r"^#+ (.*)$", open(f).read(), re.M)}
        for f in files
    }
    broken = []
    for f in files:
        text = re.sub(r"```.*?```", "", open(f).read(), flags=re.S)
        for link in re.findall(r"\]\(([^)\s]+)\)", text):
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, anchor = link.partition("#")
            target = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
            if not os.path.exists(target):
                broken.append(f"{f}: missing file {link}")
            elif anchor and target.endswith(".md") and anchor not in anchors[target]:
                broken.append(f"{f}: missing anchor {link}")
    for line in broken:
        print(line)
    print(f"{len(files)} files checked, {len(broken)} broken links")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
