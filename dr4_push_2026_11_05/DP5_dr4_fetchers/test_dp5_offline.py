#!/usr/bin/env python3
"""DP5 offline tests (criteria FROZEN_CRITERIA.md, c4c56e708e): F1-F3, N1-N3 against a fake archive; no connection.
Run: python3 -B dr4_push_2026_11_05/DP5_dr4_fetchers/test_dp5_offline.py   [MUTATE=1: truncation off -> F3 FAILS;
     MUTATE=2: secondary-id query dropped -> N1 FAILS]"""
import sys
sys.dont_write_bytecode = True
import json, os, re, socket, tempfile
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))


def _no_net(*a, **k):
    raise RuntimeError("network blocked in the offline test")


socket.socket.connect = _no_net                                        # socket guard
import fetch_extract_dr4 as FE
import fetch_nss_dr4 as FN

MUT = os.environ.pop("MUTATE", "").strip()
SFX = f"_MUTATE{MUT}" if MUT else ""
LOG, CHK = [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def X(name, ok, detail=""):
    CHK[name.split()[0]] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))


P("DP5 OFFLINE TESTS (fake archive; socket guard on)" + (f"   *** MUTATE={MUT} ***" if MUT else ""))

# ---------------------------------------------------------------- F1 regression against the frozen DR3 manifest
frozen = json.loads((REPO / "prep_2026/gaia_dr4_prep/catalog_builder/manifest_dr3.json").read_text())
s3, _ = FE.load_spec("dr3")
mine = [FE.chunk_query(s3, k) for k in range(12)] + [FE.sigma18_query(s3)]
theirs = [frozen["chunks"][str(k)]["query"] for k in range(12)] + [frozen["sigma18"]["query"]]
bad = [i for i, (x, y) in enumerate(zip(mine, theirs)) if x != y]
X("F1 DR3 spec: all 13 query texts byte-identical to the frozen fetch_extract.py's (manifest_dr3.json)", not bad and
  frozen["columns"] == s3["columns"] and frozen["where"] == FE.WHERE, f"mismatches at {bad}")

# ---------------------------------------------------------------- F2 DR4 text
s4, _ = FE.load_spec("dr4")
q4 = FE.chunk_query(s4, 3)
c3 = [c.strip() for c in s3["columns"].split(",")]; c4 = [c.strip() for c in s4["columns"].split(",")]
X("F2 DR4 default: table gaiadr4.gaia_source, no non_single_star, the other 16 columns and the WHERE unchanged",
  "non_single_star" not in q4 and s4["table"] == "gaiadr4.gaia_source" and c4 == [c for c in c3 if c != "non_single_star"]
  and len(c4) == 16 and FE.WHERE in q4, q4[:160] + " ...")

# ---------------------------------------------------------------- F3 sync-ranges completeness on a fake table
rng = np.random.default_rng(7)
k = 5
lo0 = k * FE.LEVEL0
# clustered ids so some pieces exceed the cap
centres = lo0 + rng.integers(0, FE.LEVEL0, 40)
sid = np.unique(np.concatenate([c + rng.integers(0, FE.LEVEL0 // 2000, 1500) for c in centres] + [lo0 + rng.integers(0, FE.LEVEL0, 3000)]))
sid = sid[(sid >= lo0) & (sid < lo0 + FE.LEVEL0)]
fake = {"source_id": sid, "parallax": rng.uniform(3.6, 20, len(sid))}
rx = re.compile(r"source_id >= (\d+) AND source_id < (\d+)$")


def fake_sync(q, cap=FE.SYNC_CAP):
    m = rx.search(q)
    lo, hi = int(m.group(1)), int(m.group(2))
    sel = (fake["source_id"] >= lo) & (fake["source_id"] < hi)
    idx = np.flatnonzero(sel)[:cap]                                  # the archive truncates silently
    return {c: v[idx] for c, v in fake.items()}


parts, cnt = FE.fetch_sync_ranges(s4, k, fake_sync, detect_truncation=(MUT != "1"))
got = np.concatenate([p["source_id"] for p in parts])
X("F3 sync-ranges returns exactly the brute-force row set (no duplicates, nothing lost); truncated pieces split",
  len(got) == len(np.unique(got)) and np.array_equal(np.sort(got), np.sort(sid)) and (cnt["truncated"] > 0 or MUT == "1"),
  f"{len(sid):,d} rows in the fake chunk; got {len(got):,d} ({len(np.unique(got)):,d} unique); {cnt['queries']} queries, {cnt['truncated']} truncated")

# ---------------------------------------------------------------- N1-N3 the NSS fetcher
ids = np.unique(rng.integers(10 ** 15, 10 ** 15 + 10 ** 7, 3000)).astype(np.int64)
others = rng.integers(10 ** 15, 10 ** 15 + 10 ** 7, 6000).astype(np.int64)
one = {"source_id": np.concatenate([rng.choice(ids, 900, replace=False), others[:2500]]),
       "solution_type": np.array(["Orbital"] * 900 + ["Acceleration7"] * 2500)}
pid = rng.choice(ids, 300, replace=False); sec_in = rng.choice(ids, 300, replace=False)
two = {"source_id": np.concatenate([pid, others[2500:2800], others[2800:3100]]),
       "source_id_secondary": np.concatenate([others[3100:3400], sec_in, others[3400:3700]]),
       "solution_type": np.array(["ResolvedPairFixed"] * 900)}
# 120 own pairs: both members in the sample (returned by both queries)
two["source_id_secondary"][:120] = rng.choice(ids, 120, replace=False)
DB = {"gaiadr4.nss_two_body_orbit": one, "gaiadr4.nss_resolved_pair": two}
rin = re.compile(r"SELECT (.+) FROM (\S+) AS t WHERE t\.(\w+) IN \((.*)\)$")
rup = re.compile(r"SELECT (.+) FROM tap_upload\.ids AS u JOIN (\S+) AS t ON t\.(\w+) = u\.source_id$")


def _rows(table, cols, idc, idset, cap=None):
    T = DB[table]
    m = np.isin(T[idc], np.fromiter(idset, np.int64))
    idx = np.flatnonzero(m)
    if cap is not None:
        idx = idx[:cap]
    return {c: T[c][idx] for c in cols}


def fake_nss_sync(q, cap=FN.SYNC_CAP):
    m = rin.match(q)
    cols = [c.strip()[2:] for c in m.group(1).split(",")]
    return _rows(m.group(2), cols, m.group(3), {int(x) for x in m.group(4).split(",")}, cap)


def fake_upload(q, tab):
    m = rup.match(q)
    cols = [c.strip()[2:] for c in m.group(1).split(",")]
    return _rows(m.group(2), cols, m.group(3), set(tab["source_id"].tolist()))


def truth(table, cols, two_source):
    T = DB[table]
    m = np.isin(T["source_id"], ids) | (np.isin(T["source_id_secondary"], ids) if two_source else False)
    return FN._union([{c: T[c][m] for c in cols}], cols)


def as_set(r, cols):
    return set(zip(*[r[c].tolist() for c in cols]))


n1_ok, n1_det, files = True, [], {}
tmp = Path(tempfile.mkdtemp(prefix="dp5_"))
for t, ts in (("gaiadr4.nss_two_body_orbit", False), ("gaiadr4.nss_resolved_pair", True)):
    cols = FN.select_cols(ts)
    r_in, c_in = FN.fetch_inlist(t, cols, ts, ids, fake_nss_sync, batch=1500, drop_secondary=(MUT == "2"))
    r_up, _ = FN.fetch_upload(t, cols, ts, ids, fake_upload, drop_secondary=(MUT == "2"))
    tr = truth(t, cols, ts)
    ok = as_set(r_in, cols) == as_set(r_up, cols) == as_set(tr, cols) and len(r_in["source_id"]) == len(as_set(tr, cols))
    n1_ok &= ok
    n1_det.append(f"{t}: truth {len(as_set(tr, cols))}, inlist {len(r_in['source_id'])} ({c_in['queries']} queries, {c_in['truncated']} truncated), upload {len(r_up['source_id'])}")
    p = tmp / f"{t.split('.')[1]}_ids.fits"
    FN.write_table(r_in, p); files[t] = (p, ts, tr)
X("N1 inlist and upload transports return the same row set per table, equal to the brute-force truth (A17 union, own pairs once)", n1_ok, "; ".join(n1_det))

sys.path.insert(0, str(REPO / "prep_2026/gaia_dr4_prep/dr4_ready_1"))
import cut12_nss_union as U
n2_ok, n2_det = True, []
for t, (p, ts, tr) in files.items():
    E = U.load_entries(p, ts)
    ok = sorted(E["source_id"]) == sorted(tr["source_id"].tolist()) and (not ts or sorted(E["source_id_secondary"]) == sorted(tr["source_id_secondary"].tolist()))
    n2_ok &= ok and set(U.load_ids(p).tolist()) == set(tr["source_id"].tolist())
    n2_det.append(f"{t}: {E['n']} entries, solution_type present {E['has_solution_type']}")
X("N2 the written id files load through cut12_nss_union.load_entries / load_ids and give the truth ids", n2_ok, "; ".join(n2_det))

try:
    FN.tables_to_fetch({"counted_tables": None, "readings": {}, "excluded": {"nss_epoch_flags": "x"}})
    refused = False
except ValueError:
    refused = True
tabs, twos, _ = FN.tables_to_fetch(json.loads((REPO / "prep_2026/gaia_dr4_prep/dr4_ready_1/manifest_template_dr4.json").read_text())["cut12_nss"])
X("N3 refuses with no counted tables; on the filed A17 template it fetches the union of the readings' tables, excluding nss_epoch_flags",
  refused and "nss_epoch_flags" not in tabs and "nss_resolved_pair" in tabs and "nss_resolved_pair" in twos, f"template tables {tabs}")

P(f"\nchecks: {sum(CHK.values())} of {len(CHK)} pass")
if MUT:
    exp = {"1": "F3", "2": "N1"}[MUT]
    P(f"[MUTATE CONTROL] MUTATE={MUT}: {exp} {'FAILED as designed' if not CHK[exp] else 'did NOT fail: the control does not bite'}")
(HERE / f"test_dp5_offline{SFX}.out").write_text("\n".join(LOG) + "\n")
sys.exit((0 if not CHK[{"1": "F3", "2": "N1"}[MUT]] else 1) if MUT else (0 if all(CHK.values()) else 1))
