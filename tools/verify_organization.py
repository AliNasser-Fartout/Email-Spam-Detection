"""Verify that the documented notebooks differ from the originals only by comments and markdown.

For every (original, documented) pair this script checks that:
  1. every original cell appears in the documented notebook, in the same order;
  2. every cell that was added is a markdown cell;
  3. original markdown cells are byte-for-byte identical;
  4. each code cell's source equals the original source preceded only by '#' comment lines,
     and its Python syntax tree (which ignores comments) is identical to the original;
  5. outputs, execution counts and cell metadata are identical;
  6. notebook-level metadata is identical.

Usage (from the repository root):
    python tools/verify_organization.py
"""
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIRS = {
    "notebooks/01a_split_80_20_baseline.ipynb": "original_notebooks/mail_spam-Copy2.ipynb",
    "notebooks/01b_split_80_20_with_xgboost_roc.ipynb": "original_notebooks/mail_spam_1.ipynb",
    "notebooks/02_split_80_20_hyperparameter_tuning.ipynb": "original_notebooks/mail_spam-Copy1.ipynb",
    "notebooks/03_cross_validation.ipynb": "original_notebooks/mail_spam-Copy3.ipynb",
}


def source(cell):
    return "".join(cell["source"])


def same_except_source(a, b):
    keys = (set(a) | set(b)) - {"source"}
    return all(a.get(k) == b.get(k) for k in keys)


def check_pair(new_path, old_path):
    new = json.loads((ROOT / new_path).read_text(encoding="utf-8"))
    old = json.loads((ROOT / old_path).read_text(encoding="utf-8"))
    errors = []
    if new["metadata"] != old["metadata"] or new["nbformat"] != old["nbformat"] \
            or new["nbformat_minor"] != old["nbformat_minor"]:
        errors.append("notebook metadata/format differs")

    added = commented = 0
    j = 0  # position in the original notebook
    for k, cell in enumerate(new["cells"]):
        orig = old["cells"][j] if j < len(old["cells"]) else None
        if orig is not None and cell["cell_type"] == orig["cell_type"]:
            if cell["cell_type"] == "markdown" and cell == orig:
                j += 1
                continue
            if cell["cell_type"] == "code":
                s_new, s_old = source(cell), source(orig)
                prefix = s_new[: len(s_new) - len(s_old)]
                ok = s_new.endswith(s_old) and all(
                    line.startswith("#") for line in prefix.splitlines())
                ok = ok and ast.dump(ast.parse(s_new)) == ast.dump(ast.parse(s_old))
                ok = ok and same_except_source(cell, orig)
                if not ok:
                    errors.append(f"code cell {j} (documented cell {k}) differs beyond added comments")
                commented += s_new != s_old
                j += 1
                continue
        if cell["cell_type"] != "markdown":
            errors.append(f"documented cell {k} is an unmatched non-markdown cell")
        added += 1
    if j != len(old["cells"]):
        errors.append(f"only {j} of {len(old['cells'])} original cells were found in order")

    n_code = sum(c["cell_type"] == "code" for c in old["cells"])
    status = "OK" if not errors else "FAILED"
    print(f"[{status}] {new_path}  <-  {old_path}")
    print(f"       original cells: {len(old['cells'])} ({n_code} code), all preserved in order: {j == len(old['cells'])}")
    print(f"       markdown cells added: {added}; code cells with added comment lines: {commented}")
    for e in errors:
        print("       ERROR:", e)
    return not errors


if __name__ == "__main__":
    results = [check_pair(n, o) for n, o in PAIRS.items()]
    sys.exit(0 if all(results) else 1)
