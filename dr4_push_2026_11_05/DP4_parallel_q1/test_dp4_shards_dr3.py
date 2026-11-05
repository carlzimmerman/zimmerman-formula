#!/usr/bin/env python3
"""DP4 test (criteria FROZEN_CRITERIA.md, 43d86506d1): sharded Q1 cones give the driver's final CSV byte for byte on DR3.
OFFLINE (the driver's socket guard stays). DR3 numbers are code-path tests, never results; NON-SCORING; no verdict words.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -B dr4_push_2026_11_05/DP4_parallel_q1/test_dp4_shards_dr3.py [--scratch DIR]
     MUTATE=1 (one shard left out: S1 must FAIL, ConeCoverageError) | MUTATE=2 (one shard's pair ids shifted: S5 must FAIL)."""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, os, tempfile, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
READY = REPO / "prep_2026" / "gaia_dr4_prep" / "dr4_ready_1"
sys.path.insert(0, str(READY)); sys.path.insert(0, str(HERE))
import dry_run_driver as D                                              # read only
import cones_cut13 as CC                                                # read only
import dr4_shard_q1 as SQ

ap = argparse.ArgumentParser()
ap.add_argument("--scratch", default=None)
args = ap.parse_args()
MUT = os.environ.pop("MUTATE", "").strip()
SFX = f"_MUTATE{MUT}" if MUT else ""
LOG, CHK, RES = [], {}, {}
T0 = time.time()


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def X(name, ok, detail=""):
    CHK[name.split()[0]] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))


D.init(False)
WB = REPO / "real_research" / "data" / "widebinaries"
IN = WB / "dr3_extract" / "dr4_ready_1"
FINAL_CSV, DELTA_CSV = WB / "dr3_extract" / "wide_binaries_dr3.csv", IN / "q1_delta_pairs.csv"
FULL_FITS, DELTA_FITS = IN / "q1_full_neighbours.fits", IN / "q1_delta_neighbours.fits"
scratch = Path(args.scratch or tempfile.mkdtemp(prefix="dp4_"))
scratch.mkdir(parents=True, exist_ok=True)

P("DP4: SHARDED Q1 CONES AGAINST THE UNSHARDED DRIVER RUN ON THE 10,231 DR3 CANDIDATES (code-path test; non-scoring)"
  + (f"   *** MUTATE={MUT} ***" if MUT else ""))
ext = D.extract_dir("dr3", "primary")
S = dict(np.load(ext / "stage_A.npz"))
sid = S["source_id"]
order = np.argsort(sid)
rows_of = lambda ids: order[np.searchsorted(sid[order], ids)]

f1, f2 = CC.read_pairs_csv(FINAL_CSV)
d1, d2 = CC.read_pairs_csv(DELTA_CSV)
nb_full, nb_delta = CC.read_neighbour_fits(FULL_FITS), CC.read_neighbour_fits(DELTA_FITS)
P(f"final {len(f1):,d}, delta {len(d1):,d}; neighbour rows full {len(nb_full['source_id']):,d}, delta {len(nb_delta['source_id']):,d}")

# the unsharded reference (as cones_all_candidates_dr3.py builds it)
ref_tab = CC.ConeTable().add(nb_full, f1, f2).add(nb_delta, d1, d2)
REF = {}
for kind in ("cones-literal", "cones-orbit"):
    _, r = D.run("dr3", "primary", kind, None, False, cones=ref_tab, missing_cones="error")
    REF[kind] = (r["sha256"], r["n_pairs"])
    P(f"unsharded {kind}: {r['n_pairs']:,d} pairs, sha256 {r['sha256'][:16]}")
RES["reference"] = {k: dict(sha256=v[0], n_pairs=v[1]) for k, v in REF.items()}

# all candidates with their own neighbour rows: (s1, s2, nb rows) per source file
all1, all2 = np.concatenate([f1, d1]), np.concatenate([f2, d2])
src = np.concatenate([np.zeros(len(f1), int), np.ones(len(d1), int)])
loc = np.concatenate([np.arange(len(f1)), np.arange(len(d1))])
nbs = (nb_full, nb_delta)


def shard_tables(k, mutate=""):
    sh = SQ.shard_index(all1, k)
    tabs, pairs = [], []
    for j in range(k):
        m = np.flatnonzero(sh == j)
        s1, s2 = all1[m], all2[m]
        parts = []
        for f in (0, 1):
            mm = m[src[m] == f]
            new_id = np.full(len(nbs[f]["pair_id"]) and (nbs[f]["pair_id"].max() + 1), -1, np.int64)
            new_id[loc[mm]] = np.flatnonzero(src[m] == f)                # index within the shard
            keep = new_id[nbs[f]["pair_id"]] >= 0
            nbj = {c: v[keep] for c, v in nbs[f].items()}
            nbj["pair_id"] = new_id[nbs[f]["pair_id"][keep]]
            parts.append(nbj)
        nbj = {c: np.concatenate([parts[0][c], parts[1][c]]) for c in parts[0]}
        if mutate == "2" and j == 0:
            nbj["pair_id"] = (nbj["pair_id"] + 1) % len(m)
        tabs.append((nbj, s1, s2)); pairs.append((s1, s2))
    return sh, tabs


def table_from(tabs, drop=None):
    t = CC.ConeTable()
    for j, (nbj, s1, s2) in enumerate(tabs):
        if j != drop:
            t.add(nbj, s1, s2)
    return t


# ---------------------------------------------------------------- S2 coverage
P("\nCONTROLS")
cand = {(int(x), int(y)) for x, y in zip(all1.tolist(), all2.tolist())}
s2_ok, s2_det = True, []
for k in (2, 4, 8):
    sh = SQ.shard_index(all1, k)
    keys = [{(int(x), int(y)) for x, y in zip(all1[sh == j].tolist(), all2[sh == j].tolist())} for j in range(k)]
    disjoint = sum(len(s) for s in keys) == len(set().union(*keys))
    ok = disjoint and set().union(*keys) == cand and len(cand) == 10231
    s2_ok &= ok; s2_det.append(f"K={k}: sizes {[len(s) for s in keys]}, disjoint {disjoint}, union = candidates {set().union(*keys) == cand}")
X("S2 every candidate is in exactly one shard (K = 2, 4, 8)", s2_ok, "; ".join(s2_det))

# ---------------------------------------------------------------- S1 byte identity
s1_ok, s1_det = True, []
runs = [(4, "cones-literal"), (4, "cones-orbit"), (2, "cones-literal"), (8, "cones-literal")]
for k, kind in runs:
    sh, tabs = shard_tables(k, MUT if MUT == "2" else "")
    if k == 4 and kind == "cones-literal":
        # the from-files path: write the shard FITS + CSV and read them back through ConeTable.from_files
        from astropy.table import Table
        files = []
        for j, (nbj, s1, s2) in enumerate(tabs):
            if MUT == "1" and j == 1:
                continue
            fp, cp = scratch / f"dr3_shard{j:02d}_of04_neighbours.fits", scratch / f"dr3_shard{j:02d}_of04_pairs.csv"
            Table({c: v for c, v in nbj.items()}).write(str(fp), overwrite=True)
            SQ.write_pairs(cp, s1, s2)
            files.append((fp, cp))
        tab = CC.ConeTable.from_files(files)
        how = "from files"
    else:
        tab = table_from(tabs, drop=1 if MUT == "1" else None)
        how = "in memory"
    try:
        _, r = D.run("dr3", "primary", kind, None, False, cones=tab, missing_cones="error")
        same = r["sha256"] == REF[kind][0]
        s1_det.append(f"K={k} {kind} ({how}): sha256 {r['sha256'][:16]} {'==' if same else '!='} reference, {r['n_pairs']:,d} pairs")
    except CC.ConeCoverageError as e:
        same = False
        s1_det.append(f"K={k} {kind} ({how}): ConeCoverageError: {str(e)[:120]}")
    s1_ok &= same
X("S1 the driver's final CSV from K shards is byte-identical to the unsharded run (K = 4 literal from files, 4 orbit, 2, 8)", s1_ok, "; ".join(s1_det))
RES["s1"] = s1_det

# ---------------------------------------------------------------- S5 subset check (the K3b form) on the K = 4 shards
sh, tabs = shard_tables(4, MUT if MUT == "2" else "")
tab4 = table_from(tabs, drop=1 if MUT == "1" else None)
ra_, rb_ = rows_of(f1), rows_of(f2)
rng_ = np.random.default_rng(3)
sub = np.unique(np.concatenate([[1371, 5584], rng_.choice(len(f1), 100, replace=False)]))
try:
    fl_sub, _ = tab4.flags(S, ra_[sub], rb_[sub], "literal")
    got = sorted(sub[np.flatnonzero(fl_sub)].tolist())
    s5_ok, s5_det = got == [1371, 5584], f"{len(sub)} pairs; flagged {got} (expected [1371, 5584])"
except CC.ConeCoverageError as e:
    s5_ok, s5_det = False, f"ConeCoverageError: {str(e)[:120]}"
X("S5 a subset of final pairs (the two WP1 literal hits + 100 seeded) evaluated on the K = 4 shards flags exactly the two hits", s5_ok, s5_det)

# ---------------------------------------------------------------- S3 plan overhead (information)
if not MUT:
    import dr4_archive_fetch as F
    spec, _ = F.load_spec("dr3_gaia_source")
    cpath = scratch / "dr3_candidates.csv"
    SQ.write_pairs(cpath, all1, all2)
    u_all = len(F.plan_pairs(str(ext / "stage_A.npz"), str(cpath), spec)["units"])
    s3 = {"unsharded": u_all}
    for k in (2, 4, 8):
        entries, _ = SQ.split(cpath, k, scratch / f"plan_k{k}", "dr3")
        u = [len(F.plan_pairs(str(ext / "stage_A.npz"), e["pairs"], spec)["units"]) for e in entries]
        s3[f"K{k}"] = dict(units=u, total=sum(u), ratio=sum(u) / u_all, max_shard_fraction=max(u) / u_all)
        P(f"  [INFO] S3 K={k}: units per shard {u}, total {sum(u):,d} vs unsharded {u_all:,d} (ratio {sum(u) / u_all:.3f}); "
          f"wall time ~ max shard = {max(u) / u_all:.3f} of serial"
          + ("   -> sharding inflates the query count" if k == 4 and sum(u) / u_all > 1.10 else ""))
    RES["s3"] = s3
    # S4 commands
    entries, man = SQ.split(cpath, 4, scratch / "cmd_k4", "dr4")
    cmds = SQ.commands(entries, "dr4_all_source", "<dr4_extract>/stage_A.npz", "<data_dir>", dict(accepted_mb=2540, received_mb=3100, max_queries=58900), "dr4")
    caps_ok = abs(sum(float(c.split("--cap-accepted-mb ")[1].split()[0]) for c in cmds) - 2540) < 0.5
    tags = [c.split("--tag ")[1].split()[0] for c in cmds]; mans = [c.split("--manifest ")[1].split()[0] for c in cmds]
    s4_ok = caps_ok and len(set(tags)) == 4 and len(set(mans)) == 4 and all("--spec dr4_all_source" in c for c in cmds)
    X("S4 the K = 4 commands use the frozen spec, distinct tags and manifests, caps summing to the given cap", s4_ok, cmds[0].replace(str(scratch), "<scratch>")[:200] + " ...")

P(f"\nchecks: {sum(CHK.values())} of {len(CHK)} pass; {time.time() - T0:.0f} s")
if MUT:
    expect = {"1": "S1", "2": "S5"}[MUT]
    bit = not CHK[expect]
    P(f"[MUTATE CONTROL] MUTATE={MUT}: {expect} {'FAILED as designed' if bit else 'did NOT fail: the control does not bite'}")
(HERE / f"test_dp4_shards_dr3{SFX}.out").write_text("\n".join(LOG) + "\n")
(HERE / f"test_dp4_shards_dr3{SFX}.json").write_text(json.dumps(dict(checks=CHK, results=RES), indent=1, default=str) + "\n")
sys.exit((0 if (not CHK[{"1": "S1", "2": "S5"}[MUT]]) else 1) if MUT else (0 if all(CHK.values()) else 1))
