#!/usr/bin/env python3
"""Cut 12 (NSS screen) stub: the union over the DR4 `nss_*` tables that the
owner declares as counted, returning a boolean flag per source_id.

STUB.  There is no DR4 data model yet and no archive access here.  What exists:
the union logic, the pre-registration guard rails (Amendment 15(b): the list
of counted tables is decided BEFORE the data are opened and recorded in the
manifest; every excluded table needs a recorded reason), and a manifest-ready
report.  What does not exist: any table loader, any real `nss_*` table name,
any decision about which tables count (a judgement about their content, made
from the published data model on release day and never tuned after seeing the
sample size; RELEASE_DAY_CHECKLIST.md section 0 item E).

Frozen text (PREREGISTRATION_DR4.md section 1.2 row 12): "reject pairs where
either component has ANY DR4 non-single-star solution (astrometric orbit,
acceleration, or spectroscopic orbit)".  This module changes no cut.

Release-day parameters (nothing hard-coded beyond the placeholder below):
    counted_tables : list of table names the owner declared counted
    excluded       : {table name: reason} for every OTHER table supplied
    ids_by_table   : {table name: array of source_id} as loaded from the archive
The literal string PLACEHOLDER_NSS_TABLE is documentation only; passing it as
a counted table raises, so a forgotten placeholder cannot run silently.
"""
from __future__ import annotations

import json
import sys
from typing import Mapping, NamedTuple, Sequence

import numpy as np

PLACEHOLDER_TABLE = "PLACEHOLDER_NSS_TABLE"   # documented placeholder, never valid at run time

_MUTATE = False   # test hook only (self-test control): union replaced by intersection


class NssResult(NamedTuple):
    flag: np.ndarray        # bool per input source_id: appears in >= 1 counted table
    report: dict            # manifest-ready record (JSON-serialisable)


def nss_union_flags(source_ids, ids_by_table: Mapping[str, Sequence[int]],
                    counted_tables: Sequence[str],
                    excluded: Mapping[str, str] | None = None) -> NssResult:
    """Boolean flag per source_id: True if it appears in ANY counted table.

    Raises (rather than guessing) when:
      * counted_tables is empty, None, or contains the placeholder;
      * a counted table name is absent from ids_by_table (typo or missing load);
      * a supplied table is neither counted nor listed in `excluded` with a
        non-empty reason (the checklist requires the reason in the manifest);
      * a table is both counted and excluded.
    """
    if not counted_tables:
        raise ValueError("counted_tables must be declared (non-empty) before the data are opened; "
                         "if no nss_* table can be counted, report UNIMPLEMENTABLE: cut 12 (Amendment 15(d)) "
                         "and run without the cut, choosing no substitute")
    counted = list(dict.fromkeys(counted_tables))
    if PLACEHOLDER_TABLE in counted:
        raise ValueError(f"'{PLACEHOLDER_TABLE}' is a documentation placeholder; name the real tables")
    excluded = dict(excluded or {})
    missing = [t for t in counted if t not in ids_by_table]
    if missing:
        raise KeyError(f"counted table(s) not supplied: {missing}")
    both = [t for t in counted if t in excluded]
    if both:
        raise ValueError(f"table(s) both counted and excluded: {both}")
    unaccounted = [t for t in ids_by_table if t not in counted and not str(excluded.get(t, "")).strip()]
    if unaccounted:
        raise ValueError(f"table(s) supplied but neither counted nor excluded with a reason: {unaccounted}")

    sid = np.asarray(source_ids, dtype=np.int64)
    per_table = {}
    union = None
    for t in counted:
        ids = np.asarray(ids_by_table[t], dtype=np.int64)
        u = np.unique(ids)
        per_table[t] = {"rows": int(ids.size), "unique_source_ids": int(u.size),
                        "matched_in_sample": int(np.isin(sid, u).sum())}
        if union is None:
            union = u
        else:
            union = np.intersect1d(union, u) if _MUTATE else np.union1d(union, u)
    flag = np.isin(sid, union)
    report = {"cut": 12, "counted_tables": counted, "per_table": per_table,
              "excluded_tables": {t: excluded[t] for t in excluded},
              "n_sample": int(sid.size), "n_flagged_union": int(flag.sum()),
              "n_union_unique_ids": int(union.size)}
    return NssResult(flag, report)


def pair_nss_flags(sample_source_ids, flag, a, b):
    """Pair-level cut 12: True where EITHER component (rows a, b of the sample)
    is flagged.  `flag` is the per-source array from nss_union_flags for the
    same `sample_source_ids`.  Pairs to REJECT are those returned True."""
    flag = np.asarray(flag, bool)
    if len(flag) != len(sample_source_ids):
        raise ValueError("flag must be aligned with sample_source_ids")
    a, b = np.asarray(a, int), np.asarray(b, int)
    return flag[a] | flag[b]


# ---------------------------------------------------------------- self-test
def _selftest():
    bad = []

    def check(name, ok):
        if not ok:
            bad.append(name)
        print(f"  [{'ok' if ok else 'FAIL'}] {name}")

    sid = np.arange(1000, 1020)
    tabs = {"T_A": [1001, 1001, 1003], "T_B": [1003, 1010], "T_C": [1015]}   # synthetic names, not ESA's
    ex = {"T_C": "synthetic: excluded for the test"}
    r = nss_union_flags(sid, tabs, ["T_A", "T_B"], ex)
    want = np.isin(sid, [1001, 1003, 1010])
    check("union of counted tables only (T_C excluded is not counted)", np.array_equal(r.flag, want))
    check("report: rows 3 and 2, unique 2, union size 3, flagged 3",
          (r.report["per_table"]["T_A"]["rows"], r.report["per_table"]["T_A"]["unique_source_ids"],
           r.report["per_table"]["T_B"]["rows"], r.report["n_union_unique_ids"], r.report["n_flagged_union"])
          == (3, 2, 2, 3, 3))
    check("report is JSON-serialisable", bool(json.dumps(r.report)))
    r2 = nss_union_flags(sid, tabs, ["T_A", "T_B", "T_C"], {})
    check("counting T_C as well flags 1015 too (list is a run-time parameter)",
          r2.flag[sid == 1015][0] and r2.flag.sum() == 4)
    a, b = np.array([1, 3, 5]), np.array([2, 4, 6])         # rows: 1001,1002 | 1003,1004 | 1005,1006
    pf = pair_nss_flags(sid, r.flag, a, b)
    check("pair flagged iff either component flagged", list(pf) == [True, True, False])
    for label, fn in (
        ("empty counted list", lambda: nss_union_flags(sid, tabs, [], ex)),
        ("placeholder table name", lambda: nss_union_flags(sid, {PLACEHOLDER_TABLE: []}, [PLACEHOLDER_TABLE])),
        ("unknown counted table", lambda: nss_union_flags(sid, tabs, ["T_A", "T_Z"], ex)),
        ("supplied table with no decision", lambda: nss_union_flags(sid, tabs, ["T_A"], {"T_C": "x"})),
        ("blank exclusion reason", lambda: nss_union_flags(sid, tabs, ["T_A", "T_B"], {"T_C": "  "})),
        ("table both counted and excluded", lambda: nss_union_flags(sid, tabs, ["T_A", "T_B"], {"T_A": "x", "T_C": "y"})),
    ):
        try:
            fn()
            ok = False
        except (ValueError, KeyError):
            ok = True
        check(f"raises on {label}", ok)
    global _MUTATE
    _MUTATE = True
    try:
        rm = nss_union_flags(sid, tabs, ["T_A", "T_B"], ex)
    finally:
        _MUTATE = False
    caught = not np.array_equal(rm.flag, want)
    print(f"MUTATE control (union -> intersection): result differs from the union, i.e. the check above would fail: "
          f"{'DETECTED' if caught else 'NOT DETECTED'}")
    print(f"cut12_stub self-test: {len(bad)} failure(s); mutate {'detected' if caught else 'NOT detected'}")
    return not bad and caught


if __name__ == "__main__":
    sys.exit(0 if _selftest() else 1)
