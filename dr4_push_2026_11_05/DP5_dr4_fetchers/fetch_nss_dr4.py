#!/usr/bin/env python3
"""DP5 (criteria FROZEN_CRITERIA.md, c4c56e708e): fetch the NSS-group rows touching the sample, as the id files that
`prep_2026/gaia_dr4_prep/dr4_ready_1/cut12_nss_union.py` (run / run_a17, via load_entries) reads.

NEW file. Tables fetched = every table counted in any declared reading (manifest cut12_nss.readings[*].counted_tables, or
cut12_nss.counted_tables) plus the declared diagnostic tables; nothing else. With none declared it refuses before any
query. Two-source tables (cut12_nss.two_source_tables) are matched on source_id AND source_id_secondary (A17 (b)); the two
results are unioned and rows identical in every selected column counted once.

Transports:
  upload  the frozen text of cut12_nss_union.adql_nss (an uploaded id table), unchanged;
  inlist  the same SELECT with `t.<id column> IN (...)` batches, sync; a result of exactly the sync cap is discarded and the
          batch split (upload joins stalled on the anonymous archive in 2026-09; literal conditions did not).
Every query needs the owner's go (--owner-go-recorded).

  python3 -B dr4_push_2026_11_05/DP5_dr4_fetchers/fetch_nss_dr4.py --manifest <dr4 manifest.json> --ids <component ids .csv/.npz>
      --out-dir <data_dir> [--transport inlist|upload] [--print-queries] --owner-go-recorded "<text>"
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
READY = REPO / "prep_2026" / "gaia_dr4_prep" / "dr4_ready_1"
sys.path.insert(0, str(READY))
import cut12_nss_union as U                                             # read only

SYNC_CAP = 2000
BATCH = 400


def tables_to_fetch(c12):
    """(table list, two-source set, extra columns per table) from the manifest's cut12_nss block; refuses an empty list."""
    tabs = set(c12.get("counted_tables") or [])
    for r in (c12.get("readings") or {}).values():
        tabs |= set(r.get("counted_tables") or [])
    diag = c12.get("diagnostic") or {}
    tabs |= set(diag.get("uncounted_tables") or [])
    extra = {}
    if diag.get("optical_pair_table"):
        tabs.add(diag["optical_pair_table"])
        extra[diag["optical_pair_table"]] = (diag["optical_pair_flag_column"],)
    tabs -= set((c12.get("excluded") or {}))
    if not tabs:
        raise ValueError("no counted tables declared in cut12_nss: declare them before any query (cut12_stub rule)")
    return sorted(tabs), set(c12.get("two_source_tables") or []), extra


def select_cols(two_source, extra=()):
    return ["source_id"] + (["source_id_secondary"] if two_source else []) + ["solution_type"] + list(extra)


def inlist_query(table, cols, id_col, ids):
    sel = ", ".join(f"t.{c}" for c in cols)
    return f"SELECT {sel} FROM {table} AS t WHERE t.{id_col} IN ({', '.join(str(int(i)) for i in ids)})"


def fetch_inlist(table, cols, two_source, ids, sync, cap=SYNC_CAP, batch=BATCH, detect_truncation=True, drop_secondary=False):
    id_cols = ["source_id"] + (["source_id_secondary"] if two_source and not drop_secondary else [])
    parts, n_q, n_tr = [], 0, 0
    for idc in id_cols:
        todo = [ids[i:i + batch] for i in range(0, len(ids), batch)]
        while todo:
            b = todo.pop()
            rows = sync(inlist_query(table, cols, idc, b))
            n_q += 1
            n = len(rows[cols[0]]) if rows else 0
            if detect_truncation and n >= cap:
                n_tr += 1
                if len(b) < 2:
                    raise RuntimeError(f"{table}: one id returned the cap")
                h = len(b) // 2
                todo += [b[:h], b[h:]]
                continue
            parts.append(rows)
    return _union(parts, cols), dict(queries=n_q, truncated=n_tr)


def fetch_upload(table, cols, two_source, ids, upload_job, drop_secondary=False):
    extra = [c for c in cols if c not in ("source_id", "source_id_secondary")]
    qs = U.adql_nss(table, two_source=two_source, upload="ids", extra_cols=tuple(extra))
    if drop_secondary:
        qs = qs[:1]
    parts = [upload_job(q, {"source_id": np.asarray(ids, np.int64)}) for q in qs]
    return _union(parts, cols), dict(queries=len(qs), truncated=0)


def _union(parts, cols):
    if not parts:
        return {c: np.array([]) for c in cols}
    cat = {c: np.concatenate([np.asarray(p[c]) for p in parts]) for c in cols}
    keys = list(zip(*[cat[c].tolist() for c in cols]))
    seen, keep = set(), []
    for i, k in enumerate(keys):
        if k not in seen:
            seen.add(k); keep.append(i)
    keep = np.array(keep, int)
    return {c: v[keep] if len(keep) else v[:0] for c, v in cat.items()}


def write_table(rows, path):
    from astropy.table import Table
    Table({c: v for c, v in rows.items()}).write(str(path), overwrite=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--ids", required=True, help="component source_ids (.csv with source_id, or .npz)")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--transport", choices=("inlist", "upload"), default="inlist")
    ap.add_argument("--table-prefix", default="gaiadr4.", help="schema prefix for the table names on the day")
    ap.add_argument("--print-queries", action="store_true")
    ap.add_argument("--owner-go-recorded", default="")
    a = ap.parse_args(argv)
    man = json.loads(Path(a.manifest).read_text())
    tabs, two, extra = tables_to_fetch(man["cut12_nss"])
    ids = np.unique(U.load_ids(a.ids))
    if a.print_queries:
        for t in tabs:
            cols = select_cols(t in two, extra.get(t, ()))
            print(f"-- {t}: {len(ids):,d} ids, transport {a.transport}")
            print(inlist_query(a.table_prefix + t, cols, "source_id", ids[:3]) + "  ... (batches of %d)" % BATCH
                  if a.transport == "inlist" else U.adql_nss(a.table_prefix + t, t in two, extra_cols=tuple(c for c in cols if c not in ("source_id", "source_id_secondary")))[0])
        return 0
    if not a.owner_go_recorded.strip() or not a.out_dir:
        raise SystemExit("a fetch needs --out-dir and --owner-go-recorded (the owner's go, verbatim)")
    from astroquery.gaia import Gaia
    from astropy.table import Table

    def sync(q):
        t = Gaia.launch_job(q).get_results()
        return {c.lower(): np.asarray(t[c]) for c in t.colnames}

    def upload_job(q, tab):
        import tempfile
        f = Path(tempfile.mkdtemp()) / "ids.xml"
        Table(tab).write(str(f), format="votable")
        t = Gaia.launch_job_async(q, upload_resource=str(f), upload_table_name="ids").get_results()
        return {c.lower(): np.asarray(t[c]) for c in t.colnames}

    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    report = {}
    for t in tabs:
        cols = select_cols(t in two, extra.get(t, ()))
        rows, cnt = (fetch_inlist(a.table_prefix + t, cols, t in two, ids, sync) if a.transport == "inlist"
                     else fetch_upload(a.table_prefix + t, cols, t in two, ids, upload_job))
        p = out / f"{t}_ids.fits"
        write_table(rows, p)
        report[t] = dict(file=str(p), rows=int(len(rows["source_id"])), sha256=hashlib.sha256(p.read_bytes()).hexdigest(), **cnt)
        print(f"{t}: {report[t]['rows']:,d} rows, {cnt['queries']} queries, {cnt['truncated']} truncated and split")
    rp = out / "nss_fetch_report.json"
    rp.write_text(json.dumps(dict(transport=a.transport, owner_go=a.owner_go_recorded, n_ids=int(len(ids)), tables=report,
                                  id_files={t: report[t]["file"] for t in report}), indent=1) + "\n")
    print(f"id_files for manifest cut12_nss.id_files: {rp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
