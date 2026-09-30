#!/usr/bin/env python3
"""DR4-READY-1, WP4 (offline half): the cut-12 NSS union driven by the release-day manifest (Amendment 15(b), 16(c)).

NEW file.  NO NETWORK.  Reads per-table source-id lists from local files named in the manifest and calls
catalog_builder_dr4/cut12_stub.py's nss_union_flags / pair_nss_flags.  The list of COUNTED tables and the reasons for every
EXCLUDED table must be declared in the manifest BEFORE any id file is opened (cut12_stub refuses an empty list, the
placeholder, unknown tables and unaccounted tables).  Table names are run-time data: DR3 has nss_two_body_orbit,
nss_acceleration_astro, nss_non_linear_spectro, nss_vim_fl; ESA's DR4 page names nss_acceleration_astro,
nss_two_body_orbit, nss_resolved_pair, nss_multiplicity, nss_multiple_orbits, nss_masses (data chat, d9ac3a13f) --
nothing here assumes either list.

load_ids(path)            -> numpy int64 array of source_id from .npz (key 'source_id'), .csv/.txt (column 'source_id'),
                             or .fits (column 'source_id')
run(manifest, pair_ids_a, pair_ids_b) -> (pair flags, report); the report is written back into manifest['cut12_nss']
"""
import sys
sys.dont_write_bytecode = True
import csv
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "catalog_builder_dr4"))
import cut12_stub                                               # read-only


def load_ids(path):
    p = Path(path)
    if p.suffix == ".npz":
        return np.asarray(np.load(p)["source_id"], dtype=np.int64)
    if p.suffix in (".csv", ".txt"):
        with open(p, newline="") as f:
            return np.array([int(r["source_id"]) for r in csv.DictReader(f)], dtype=np.int64)
    if p.suffix in (".fits", ".fit"):
        from astropy.io import fits
        with fits.open(p, memmap=True) as h:
            return np.asarray(h[1].data["source_id"], dtype=np.int64)
    raise ValueError(f"unsupported id file type: {p.name}")


def run(manifest, pair_ids_a, pair_ids_b):
    c12 = manifest["cut12_nss"]
    counted, excluded = c12.get("counted_tables"), c12.get("excluded") or {}
    if not counted:
        raise ValueError("manifest['cut12_nss']['counted_tables'] must be declared before any NSS id file is opened")
    files = c12.get("id_files") or {}
    for t in list(counted) + list(excluded):
        if t not in files:
            raise KeyError(f"no id file declared for table {t!r}")
    # every SUPPLIED id file is passed on: a table that is neither counted nor excluded with a reason makes cut12_stub raise
    # (it is never silently ignored)
    two = [t for t in files if "source_id_secondary" in _colnames(files[t])]      # guard added 2026-09-29 (see run_a17)
    if two:
        raise ValueError(f"two-source table(s) {two}: run() matches source_id only; use run_a17, which searches both id columns")
    ids_by_table = {t: load_ids(files[t]) for t in files}
    sids = np.unique(np.concatenate([np.asarray(pair_ids_a, np.int64), np.asarray(pair_ids_b, np.int64)]))
    res = cut12_stub.nss_union_flags(sids, ids_by_table, counted, excluded)
    flag_of = dict(zip(sids.tolist(), np.asarray(res.flag).tolist()))
    pair_flags = np.array([flag_of[int(x)] or flag_of[int(y)] for x, y in zip(pair_ids_a, pair_ids_b)], bool)
    c12["row_counts"] = {t: int(len(v)) for t, v in ids_by_table.items()}
    c12["n_components_flagged"] = int(np.sum(res.flag))
    c12["stub_report"] = res.report
    c12["n_pairs_flagged"] = int(pair_flags.sum())
    return pair_flags, c12


# ======================================================================================================================
# Amendment 17 readings (DRAFT, NOT FILED: prep_2026/gaia_dr4_prep/AMENDMENT17_DRAFT_NOT_FILED.md revision 2, 6bc58d468).
# New code, 2026-09-29, built so that every reading can run whether or not the amendment is filed.  `run` above matches the
# `source_id` column only; a TWO-SOURCE table (rows naming source_id and source_id_secondary, e.g. nss_resolved_pair,
# optical_pair) must go through run_a17, which searches BOTH id columns (A17 (b)) -- `run` refuses such a table.
#   * a row of a two-source table is classified, per pipeline pair it touches, as OWN-PAIR (its two ids are exactly the pair's
#     two components, matched as an UNORDERED pair) or THIRD-SOURCE (a component paired with any other source); a row of a
#     one-source table (or with a null secondary) is a solution ON the component;
#   * a reading = {counted_tables, own_pair_exempt: {table: [solution_type, ...]}}: an own-pair row of an exempt type does
#     not reject; every other row of a counted table that touches a component rejects every pipeline pair containing it;
#   * diagnostic (A17 (c)): components found only in the uncounted diagnostic tables (nss_masses, nss_multiplicity: matched
#     on source_id and, if present, source_id_secondary; nss_multiplicity's related_sources list is NOT parsed) or carrying a
#     nonzero optical_pair flag without any counted row -- reported and flagged, never used to reject.
# Nothing is decided here: table names, roles, the recorded solution_type strings and the readings are manifest data.
# ======================================================================================================================
from collections import Counter

_MUTATE_A17 = None      # test hook only: "ordered" | "exempt_all" | "third_as_own"


def _isnull(v):
    if v is None:
        return True
    if isinstance(v, float) and v != v:
        return True
    return isinstance(v, str) and v.strip().lower() in ("", "nan", "none", "null", "--")


def _read_table(path):
    """-> {lower-case column name: list of python values, None for null}; empty tables keep their column names."""
    p = Path(path)
    if p.suffix == ".npz":
        z = np.load(p, allow_pickle=False)
        return {k.lower(): [None if _isnull(v) else v for v in np.asarray(z[k]).tolist()] for k in z.files}
    if p.suffix in (".csv", ".txt"):
        with open(p, newline="") as f:
            r = csv.DictReader(f)
            rows = list(r)
            names = list(r.fieldnames or [])
        return {n.lower(): [None if _isnull(row[n]) else row[n] for row in rows] for n in names}
    if p.suffix in (".fits", ".fit"):
        from astropy.table import Table
        t = Table.read(p, format="fits")
        out = {}
        for n in t.colnames:
            c = t[n]
            vals = [v.decode() if isinstance(v, bytes) else v for v in np.asarray(c).tolist()]
            mask = np.broadcast_to(np.asarray(getattr(c, "mask", False), bool), (len(vals),))
            out[n.lower()] = [None if (m or _isnull(v)) else v for v, m in zip(vals, mask)]
        return out
    raise ValueError(f"unsupported file type: {p.name}")


def _colnames(path):
    return set(_read_table(path))


def load_entries(path, two_source, flag_column=None):
    """Rows of one NSS-group table: source_id, source_id_secondary (None for one-source rows), solution_type (None if the
    table has no such column) and, for the optical_pair diagnostic, the named flag column.  Refuses a declared two-source
    table without source_id_secondary, and an undeclared table that has one (it would otherwise be half-matched)."""
    cols = _read_table(path)
    name = Path(path).name
    if "source_id" not in cols:
        raise KeyError(f"{name}: no source_id column")
    has_sec = "source_id_secondary" in cols
    if two_source and not has_sec:
        raise KeyError(f"{name}: declared two-source but has no source_id_secondary column")
    if has_sec and not two_source:
        raise ValueError(f"{name}: has source_id_secondary but is not declared in two_source_tables")
    n = len(cols["source_id"])
    if any(v is None for v in cols["source_id"]):
        raise ValueError(f"{name}: null source_id")
    sid = [int(v) for v in cols["source_id"]]
    sec = [None if v is None else int(v) for v in cols["source_id_secondary"]] if has_sec else [None] * n
    typ = [None if v is None else str(v).strip() for v in cols["solution_type"]] if "solution_type" in cols else [None] * n
    flg = None
    if flag_column:
        if flag_column.lower() not in cols:
            raise KeyError(f"{name}: no {flag_column!r} column")
        flg = [None if v is None else float(v) for v in cols[flag_column.lower()]]
    return dict(n=n, source_id=sid, source_id_secondary=sec, solution_type=typ, has_solution_type="solution_type" in cols,
                flag=flg)


def adql_nss(table, two_source=False, upload="ids", extra_cols=("solution_type",)):
    """Release-day query text (NOT run here) for one NSS-group table against an upload of the sample's component ids.
    A two-source table is matched on BOTH id columns (A17 (b)); the caller unions the two results and drops rows that are
    identical in every selected column (an own-pair row is returned by both queries)."""
    cols = ["t.source_id"] + (["t.source_id_secondary"] if two_source else []) + [f"t.{c}" for c in extra_cols]
    sel = ", ".join(cols)
    qs = [f"SELECT {sel} FROM tap_upload.{upload} AS u JOIN {table} AS t ON t.source_id = u.source_id"]
    if two_source:
        qs.append(f"SELECT {sel} FROM tap_upload.{upload} AS u JOIN {table} AS t ON t.source_id_secondary = u.source_id")
    return qs


def run_a17(manifest, pair_ids_a, pair_ids_b):
    """Every reading declared in manifest['cut12_nss']['readings'] -> ({reading: bool reject flag per pair}, report).
    The report (per-table and per-solution_type row counts for rows touching the sample, own-pair entries by type,
    third-source entries, the diagnostic) is also written into manifest['cut12_nss']['a17_report']."""
    c12 = manifest["cut12_nss"]
    readings = c12.get("readings")
    if not readings:
        raise ValueError("manifest['cut12_nss']['readings'] must be declared before any NSS file is opened")
    files = c12.get("id_files") or {}
    two = set(c12.get("two_source_tables") or [])
    recorded = c12.get("solution_types_recorded") or {}
    diag = c12.get("diagnostic") or {}
    unc = list(diag.get("uncounted_tables") or [])
    opt_tab, opt_col = diag.get("optical_pair_table"), diag.get("optical_pair_flag_column")
    if opt_tab and not opt_col:
        raise ValueError("diagnostic: optical_pair_table named without optical_pair_flag_column")
    excluded = {t: r for t, r in (c12.get("excluded") or {}).items() if str(r).strip()}
    diag_tabs = set(unc) | ({opt_tab} if opt_tab else set())
    counted_any = set()
    for name, rd in readings.items():
        ct = list(rd.get("counted_tables") or [])
        if not ct:
            raise ValueError(f"reading {name!r}: counted_tables must be declared")
        for t in ct:
            if t not in files:
                raise KeyError(f"reading {name!r}: no file declared for counted table {t!r}")
            if t in diag_tabs or t in excluded:
                raise ValueError(f"reading {name!r}: {t!r} is counted and also diagnostic/excluded")
        for t, types in (rd.get("own_pair_exempt") or {}).items():
            if t not in ct:
                raise ValueError(f"reading {name!r}: exemption declared for {t!r}, which it does not count")
            if t not in two:
                raise ValueError(f"reading {name!r}: exemption declared for {t!r}, which is not a two-source table")
            if t not in recorded:
                raise ValueError(f"reading {name!r}: the solution_type strings of {t!r} must be recorded before opening "
                                 "(A17 (d))")
            bad = [x for x in types if x not in recorded[t]]
            if bad:
                raise ValueError(f"reading {name!r}: exempt type(s) {bad} are not among the recorded strings of {t!r}")
        counted_any |= set(ct)
    for t in diag_tabs:
        if t not in files:
            raise KeyError(f"no file declared for diagnostic table {t!r}")
    stray = [t for t in files if t not in counted_any | diag_tabs | set(excluded)]
    if stray:
        raise ValueError(f"table(s) supplied but neither counted, diagnostic nor excluded with a reason: {stray}")

    A = [int(x) for x in np.asarray(pair_ids_a, np.int64)]
    B_ = [int(x) for x in np.asarray(pair_ids_b, np.int64)]
    pairs_of = {}
    for k, (x, y) in enumerate(zip(A, B_)):
        pairs_of.setdefault(x, []).append(k)
        pairs_of.setdefault(y, []).append(k)
    npair = len(A)
    load = {t: load_entries(files[t], t in two, flag_column=(opt_col if t == opt_tab else None))
            for t in sorted(counted_any | diag_tabs)}

    events, per_table, types_unrec = [], {}, {}
    ent = {k: Counter() for k in ("own", "third", "single")}
    for t in sorted(counted_any):
        E = load[t]
        touch, by_type = 0, Counter()
        for i in range(E["n"]):
            p, s, ty = E["source_id"][i], E["source_id_secondary"][i], E["solution_type"][i]
            ks = sorted(set(pairs_of.get(p, [])) | (set(pairs_of.get(s, [])) if s is not None else set()))
            if not ks:
                continue
            touch += 1
            by_type[(ty or "(null)") if E["has_solution_type"] else "(no solution_type column)"] += 1
            if t in recorded and ty not in recorded[t]:
                types_unrec.setdefault(t, set()).add(ty)
            for k in ks:
                if s is None or s == p:
                    kind, comps = "single", [p]
                else:
                    if _MUTATE_A17 == "ordered":
                        own = (p == A[k] and s == B_[k])
                    else:
                        own = {p, s} == {A[k], B_[k]}
                    if _MUTATE_A17 == "third_as_own":
                        own = True
                    kind = "own" if own else "third"
                    comps = [c for c in (p, s) if c in (A[k], B_[k])]
                ent[kind][(t, ty)] += 1
                events.append((t, k, kind, ty, comps))
        per_table[t] = {"rows_loaded": E["n"], "rows_touching_sample": touch, "by_solution_type": dict(by_type),
                        "two_source": t in two}

    def comps_in(t):
        E = load[t]
        out = set()
        for i in range(E["n"]):
            for c in (E["source_id"][i], E["source_id_secondary"][i]):
                if c is not None and c in pairs_of:
                    out.add(c)
        return out

    unc_comps = set().union(*[comps_in(t) for t in unc]) if unc else set()
    opt_accel, opt_own_rows, opt_null_flags = set(), 0, 0
    if opt_tab:
        E = load[opt_tab]
        for i in range(E["n"]):
            p, s, f = E["source_id"][i], E["source_id_secondary"][i], E["flag"][i]
            if s is not None and any({p, s} == {A[k], B_[k]} for k in pairs_of.get(p, [])):
                opt_own_rows += 1
            if f is None:
                opt_null_flags += 1 if (p in pairs_of or s in pairs_of) else 0
            elif f != 0:
                opt_accel |= {c for c in (p, s) if c is not None and c in pairs_of}

    out, rep_readings = {}, {}
    for name, rd in readings.items():
        ct = set(rd["counted_tables"])
        ex = {t: set(v) for t, v in (rd.get("own_pair_exempt") or {}).items()}
        reject = np.zeros(npair, bool)
        exempted, why, counted_comps = set(), Counter(), set()
        for (t, k, kind, ty, comps) in events:
            if t not in ct:
                continue
            counted_comps |= set(comps)
            if kind == "own" and t in ex and (ty in ex[t] or _MUTATE_A17 == "exempt_all"):
                exempted.add(k)
                continue
            reject[k] = True
            why[kind] += 1
        only_unc = sorted(unc_comps - counted_comps)
        accel_wo = sorted(opt_accel - counted_comps)
        out[name] = reject
        rep_readings[name] = {
            "counted_tables": sorted(ct), "own_pair_exempt": {t: sorted(v) for t, v in ex.items()},
            "n_pairs_rejected": int(reject.sum()),
            "rejecting_rows_by_kind": {"solution_on_component": why["single"], "own_pair_not_exempt": why["own"],
                                       "third_source": why["third"]},
            "n_pairs_kept_only_by_the_exemption": int(sum(1 for k in exempted if not reject[k])),
            "diagnostic": {"n_components_only_in_uncounted_tables": len(only_unc),
                           "n_components_nonzero_optical_flag_without_counted_row": len(accel_wo),
                           "flag_nonzero": bool(only_unc or accel_wo),
                           "expected": 0}}

    def by_tt(cnt):
        d = {}
        for (t, ty), n in cnt.items():
            d.setdefault(t, {})[str(ty)] = n
        return d

    report = {"a17_status": "DRAFT, NOT FILED (AMENDMENT17_DRAFT_NOT_FILED.md revision 2); which reading is primary is the "
                            "owner's decision",
              "n_pairs": npair, "n_components": len(pairs_of), "per_table": per_table,
              "own_pair_entries_by_type": by_tt(ent["own"]), "third_source_entries_by_type": by_tt(ent["third"]),
              "solution_on_component_entries_by_type": by_tt(ent["single"]),
              "types_seen_not_recorded": {t: sorted(map(str, v)) for t, v in types_unrec.items()},
              "diagnostic_tables": {"uncounted": unc, "optical_pair": opt_tab, "optical_flag_column": opt_col,
                                    "optical_pair_own_pair_rows (reported only)": opt_own_rows,
                                    "optical_rows_touching_sample_with_null_flag": opt_null_flags,
                                    "note": "nss_multiplicity's related_sources list is not parsed; matching uses source_id "
                                            "and source_id_secondary only"},
              "readings": rep_readings}
    c12["a17_report"] = report
    return out, report
