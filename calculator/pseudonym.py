"""Pseudonymous patient ids: the same patient gets the same id from every source.

A site keeps one secret key. Each patient's MRN, normalized, is hashed with that key
(HMAC-SHA256), and the hash becomes the patient id. So:

- the registry, the EHR report, the workbook and a FHIR export all give the same patient
  the same pseudonym, and their tables join;
- the same MRN gets the same pseudonym every month, as long as the key is kept;
- without the key, nobody can reverse a pseudonym or test a guessed MRN against it.

The site can keep a crosswalk (MRN to pseudonym) to look patients back up. Like the key,
it stays at the site.

    new_key() -> key text, to save in a file
    pseudonymize(tables, key_text) -> (tables, crosswalk rows)

Standard library only, so it runs in the browser too.
"""

import base64
import csv
import hashlib
import hmac
import io
import re
import secrets

from .data import TABLES

PREFIX = "cocm-pseudonym-key-v1:"
ID_PREFIX = "p-"


def new_key():
    """A new random key, as the one line of text to keep in the key file."""
    return PREFIX + base64.b64encode(secrets.token_bytes(32)).decode() + "\n"


def read_key(text):
    text = (text or "").strip()
    if not text.startswith(PREFIX):
        raise ValueError("not a pseudonym key file (it should start with " + PREFIX + ")")
    try:
        key = base64.b64decode(text[len(PREFIX):], validate=True)
    except ValueError:
        raise ValueError("the pseudonym key file is damaged") from None
    if len(key) != 32:
        raise ValueError("the pseudonym key file is damaged")
    return key


def normalize(mrn):
    """The form of an MRN that's hashed, so systems that format it differently agree:
    spaces, hyphens and dots removed, letters in capitals, and leading zeros dropped from
    an all-digit MRN ("00123" and "123" are the same patient)."""
    value = re.sub(r"[\s.\-]", "", str(mrn)).upper()
    if value.isdigit():
        value = value.lstrip("0") or "0"
    return value


def pseudonym(key, mrn):
    digest = hmac.new(key, normalize(mrn).encode(), hashlib.sha256).digest()
    return ID_PREFIX + base64.b32encode(digest).decode().lower()[:16]


def pseudonymize(tables, key_text):
    """Replace patient_id in every table with its pseudonym.

    tables is {table: csv text}. Returns the new tables and the crosswalk, a list of
    (original id, pseudonym) rows, sorted, one per distinct original id.
    """
    key = read_key(key_text)
    crosswalk = {}
    out = {}
    for table in TABLES:
        text = tables.get(table)
        if not text:
            continue
        reader = csv.DictReader(io.StringIO(text))
        if "patient_id" not in (reader.fieldnames or []):
            out[table] = text
            continue
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=reader.fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in reader:
            original = row["patient_id"]
            if original:
                if original not in crosswalk:
                    crosswalk[original] = pseudonym(key, original)
                row["patient_id"] = crosswalk[original]
            writer.writerow(row)
        out[table] = buf.getvalue()
    return out, sorted(crosswalk.items())


def crosswalk_csv(rows):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["original_id", "patient_id"])
    writer.writerows(rows)
    return buf.getvalue()
