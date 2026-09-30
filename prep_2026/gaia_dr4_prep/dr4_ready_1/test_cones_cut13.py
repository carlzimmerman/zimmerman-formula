#!/usr/bin/env python3
"""DR4-READY-1: the controls K1-K6 of CONES_CUT13_DESIGN_FROZEN.md (9ea1d20e7) for cones_cut13.py and the driver's cones kinds (NEW file).  OFFLINE (socket guard); DR3 numbers are code-path tests, never results (Amendment 7(e)).
Run:  python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_cones_cut13.py            (MUTATE=1: cone pair ids shifted by one (K3b must FAIL); =2: the neighbour rows that produce the literal hits dropped (K3 and K4 must FAIL); =3: a planted kinematic neighbour in a cone (K1 must FAIL))"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, os, subprocess, tempfile, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
MUT = os.environ.pop("MUTATE", "").strip()
SFX = f"_MUTATE{MUT}" if MUT else ""
import dry_run_driver as D
import cones_cut13 as CC
D.init(False)
B = D.B
LOG, RES = [], {}
T0 = time.time()


def P(s=""):
    print(s, flush=True); LOG.append(s)


def K(name, ok, detail=""):
    RES[name] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


ext = D.extract_dir("dr3", "primary")
WB = REPO / "real_research" / "data" / "widebinaries"
Q1DIR = WB / "dr3_extract" / "dr4_ready_1"
P("CONES CUT 13: controls K1-K6 (DR3 numbers are code-path tests, never results)" + (f"; MUTATE = {MUT}" if MUT else ""))
tmpd = Path(tempfile.mkdtemp())
S = dict(np.load(ext / "stage_A.npz"))
sid = S["source_id"]
order = np.argsort(sid)
rows_of = lambda ids: order[np.searchsorted(sid[order], ids)]

# ---------------------------------------------------------------- K6 (first: it produces the candidate list) defaults and --dump-candidates
cand_path = tmpd / "candidates.csv"
b_ref, r_ref = D.run("dr3", "primary", "extract-builder", None, False, dump_candidates=str(cand_path))
b_def, r_def = D.run("dr3", "primary", "extract-builder", None, False)
c1, c2 = CC.read_pairs_csv(cand_path)
F = dict(np.load(ext / "stage_F.npz"))
extra = {"third": np.zeros(len(F["a"]), bool)}
pre, _, _ = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
idx = np.flatnonzero(pre)
indep = {(int(sid[F["a"][i]]), int(sid[F["b"][i]])) for i in idx}
st = subprocess.run([sys.executable, "-B", str(HERE / "dry_run_driver.py"), "--self-test"], capture_output=True, text=True, cwd=str(REPO), env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
K("K6 the driver's defaults are unchanged (reference CSV sha256 prefix 6fff64d964ebaa72, byte-identical with and without --dump-candidates, no 'cut13_cones' key, self-test 7/7) and --dump-candidates writes the 10,231 pairs that reach cut 13, equal to an independent computation",
  r_ref["sha256"].startswith("6fff64d964ebaa72") and b_ref == b_def and "cut13_cones" not in r_def and "7/7 pass -> ALL PASS" in st.stdout and len(c1) == len(indep) == 10231 and set(zip(c1.tolist(), c2.tolist())) == indep,
  f"sha256 {r_ref['sha256'][:16]}; {len(c1):,d} candidate pairs (independent {len(indep):,d}); self-test {st.stdout.strip().splitlines()[-1][:40]}")

# ---------------------------------------------------------------- K1 fidelity on ALL candidates (cones built from the extract)
a_rows, b_rows = rows_of(c1), rows_of(c2)
nb, s1, s2 = CC.build_extract_cones(S, a_rows, b_rows)
if MUT == "3":                                                                          # plant a kinematic neighbour (same parallax and proper motion as the primary, G = 15) inside pair 0's cone
    i = 0; r0 = int(a_rows[i])
    for k, v in (("pair_id", i), ("comp", 0), ("source_id", 4_000_000_000_000_000_000)):
        nb[k] = np.append(nb[k], v)
    for c in ("ra", "dec", "parallax", "parallax_error", "pmra", "pmdec", "pmra_error", "pmdec_error"):
        nb[c] = np.append(nb[c], float(S[c][r0]) + (1e-4 if c in ("ra",) else 0.0))
    nb["phot_g_mean_mag"] = np.append(nb["phot_g_mean_mag"], 15.0)
cones_x = CC.ConeTable().add(nb, s1, s2)
b_lit, r_lit = D.run("dr3", "primary", "extract-literal", None, False)
b_co, r_co = D.run("dr3", "primary", "cones-orbit", None, False, cones=cones_x)
b_cl, r_cl = D.run("dr3", "primary", "cones-literal", None, False, cones=cones_x)
K("K1 cones built from the extract for ALL 10,231 candidates reproduce the driver's extract stand-ins BYTE FOR BYTE: 'cones-orbit' = 'extract-builder' (the builder's own cut 13) and 'cones-literal' = 'extract-literal'; every candidate covered, the report carries the cone block",
  b_co == b_ref and b_cl == b_lit and r_co["cut13_cones"]["n_missing"] == 0 and r_co["cut13_cones"]["n_covered"] == 10231 and r_cl["cut13_cones"]["n_covered"] == 10231,
  f"{len(nb['source_id']):,d} cone rows; cones-orbit {r_co['n_pairs']:,d} pairs (extract-builder {r_ref['n_pairs']:,d}) identical {b_co == b_ref}; cones-literal {r_cl['n_pairs']:,d} (extract-literal {r_lit['n_pairs']:,d}) identical {b_cl == b_lit}; flagged {r_co['cut13_cones']['n_flagged_total']} / {r_cl['cut13_cones']['n_flagged_total']}")

# ---------------------------------------------------------------- the real Q1 (final-pair cones)
final_csv = WB / "dr3_extract" / "wide_binaries_dr3.csv"
cones_real = CC.ConeTable.from_files([(Q1DIR / "q1_full_neighbours.fits", final_csv)])
if MUT == "1":                                                                           # pair ids shifted by one
    t = cones_real._table(); n_ids = int(t["pair_id"].max()) + 1
    t["pair_id"] = (t["pair_id"] + 1) % n_ids
if MUT == "2":                                                                           # drop the neighbours that produce the literal hits
    t = cones_real._table()
    keep = ~np.isin(t["source_id"], [1184817069913979904, 6899203128039496960])
    cones_real.nb = {k: v[keep] for k, v in t.items()}

# ---------------------------------------------------------------- K2 coverage guard
try:
    D.run("dr3", "primary", "cones-literal", None, False, cones=cones_real, missing_cones="error")
    msg, raised = "", False
except CC.ConeCoverageError as e:
    msg, raised = str(e), True
K("K2 with the real Q1 (final pairs only) and missing = 'error' the driver raises ConeCoverageError naming 4,021 of 10,231 pairs without cones (covered 6,210): a pair without a cone is never treated as 'no third star'",
  raised and "4021 of 10231" in msg and "covered 6210" in msg, msg[:160])

# ---------------------------------------------------------------- K3 WP1 agreement on the final pairs
fa, fb = CC.read_pairs_csv(final_csv)
ra_, rb_ = rows_of(fa), rows_of(fb)
fl_lit, inf_lit = cones_real.flags(S, ra_, rb_, "literal")
fl_orb, inf_orb = cones_real.flags(S, ra_, rb_, "orbit")
wp1 = json.load(open(HERE / "wp1_cut13_full_dr3.json"))
want = sorted(a_["pair"] for a_ in wp1["attributions"]["literal"])
got = sorted(np.flatnonzero(fl_lit).tolist())
K("K3 on the real Q1 and the 6,210 final pairs the cones path flags what WP1 flagged: literal 2 (final-CSV indices 1371 and 5584), orbit-aware 0",
  got == want == [1371, 5584] and int(fl_orb.sum()) == 0 and inf_lit["n_missing"] == 0, f"literal flagged {got} (WP1 {want}); orbit-aware {int(fl_orb.sum())}; neighbours {inf_lit.get('n_neighbours')}; covered {inf_lit['n_covered']}")

# ---------------------------------------------------------------- K3b a SUBSET of the pairs in the table picks the right cones (the release-day case; added after the first MUTATE=1 run, design Addendum 1)
rng_ = np.random.default_rng(3)
sub = np.unique(np.concatenate([[1371, 5584], rng_.choice(len(fa), 100, replace=False)]))
fl_sub, inf_sub = cones_real.flags(S, ra_[sub], rb_[sub], "literal")
K("K3b evaluating a SUBSET of the pairs held (the two WP1 hits plus 100 drawn with a fixed seed) returns exactly the full evaluation's flags restricted to it: the two hits, nothing else",
  np.array_equal(fl_sub, fl_lit[sub]) and sorted(sub[np.flatnonzero(fl_sub)].tolist()) == [1371, 5584],
  f"{len(sub)} pairs; flagged pair indices {sorted(sub[np.flatnonzero(fl_sub)].tolist())} (full evaluation restricted: {sorted(sub[np.flatnonzero(fl_lit[sub])].tolist())}); neighbour rows used {inf_sub.get('n_neighbour_rows')}")

# ---------------------------------------------------------------- K4 fallback path
b_fb, r_fb = D.run("dr3", "primary", "cones-literal", None, False, cones=cones_real, missing_cones="extract-fallback")
blk = r_fb["cut13_cones"]
txt = b_fb.decode().strip().split("\n"); head = txt[0].split(","); i1, i2 = head.index("source_id1"), head.index("source_id2")
fin = {tuple(sorted((int(c[i1]), int(c[i2])))) for c in (l.split(",") for l in txt[1:])}
hits = {tuple(sorted((int(fa[i]), int(fb[i])))) for i in (1371, 5584)}
b_ref2, _ = D.run("dr3", "primary", "extract-builder", None, False)
K("K4 with 'extract-fallback' on the real Q1 the driver completes (6,210 covered by cones, 4,021 by the builder's own flags): the two literal hits are absent from the final CSV, the flag counts are reported, and the default extract-builder CSV beside it is unchanged",
  blk["n_covered"] == 6210 and blk["n_missing"] == 4021 and not (hits & fin) and b_ref2 == b_ref and r_fb["n_pairs"] > 5000,
  f"covered {blk['n_covered']:,d}, uncovered {blk['n_missing']:,d}; flagged by cones {blk['n_flagged_cones']}, by the fallback {blk.get('n_flagged_fallback')}; final pairs {r_fb['n_pairs']:,d} (extract-builder {r_ref['n_pairs']:,d}); the two hits in the final set: {len(hits & fin)}")

# ---------------------------------------------------------------- K5 MUTATE report line
P("  [K5 MUTATE] MUTATE = %s: %s" % (MUT or "none", {"1": "cone pair ids shifted by one (K3b must FAIL)", "2": "the neighbour rows of the literal hits dropped (K3 must FAIL)", "3": "a planted kinematic neighbour in pair 0's cone (K1 must FAIL)"}.get(MUT, "no planted fault")))
ok = all(RES.values())
P(f"\n{sum(RES.values())}/{len(RES)} checks pass -> {'ALL PASS' if ok else 'FAILURES'}  ({time.time() - T0:.0f} s)")
(HERE / f"test_cones_cut13{SFX}.out").write_text("\n".join(LOG) + "\n")
(HERE / f"test_cones_cut13_results{SFX}.json").write_text(json.dumps(dict(results=RES, mutate=MUT, seconds=round(time.time() - T0, 1)), indent=1) + "\n")
sys.exit(0 if ok else 1)
