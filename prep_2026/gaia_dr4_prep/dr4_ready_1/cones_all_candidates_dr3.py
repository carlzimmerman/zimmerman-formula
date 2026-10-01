#!/usr/bin/env python3
"""DR4-READY-1: the all-source cut 13 (WP1 cones) on ALL 10,231 DR3 candidate pairs through the driver, against the extract-based path (NEW file; OFFLINE: the driver's socket guard stays).
Design, hand estimates and controls: CONES_VS_EXTRACT_DESIGN_FROZEN.md (96a00a65a), written before this code and before the delta Q1 had finished.  DR3 numbers are code-path tests, never results (Amendment 7(e)); NON-SCORING; no verdict words.
Objects: the 10,231 candidates (the driver's --dump-candidates), the 6,210 final pairs (cones: q1_full_neighbours.fits) and the 4,021 delta pairs (cones: q1_delta_neighbours.fits, pair_id = row index of q1_delta_pairs.csv), one ConeTable, missing = 'error'.
Paths: cones-literal / cones-orbit against the extract stand-ins extract-literal / extract-builder (and extract-orbit).  Quantities: Q1 direct flags, Q2 final sets and flips (half the symmetric difference) with the 30-draw random-removal NULL, Q3 the gamma-hat shift
from the pipeline's own --catalog fit, Q4 neighbour statistics.  Controls X0-X4; MUTATE=1 (delta file left out: X1 must FAIL), =2 (delta parallax shifted: X3 must FAIL), =3 (delta pair ids shifted: X1b must FAIL) run the controls only.
--standin: the delta cones are built from the EXTRACT (a dry run before the real delta exists; outputs named *_standin; nothing from it is a result).
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/cones_all_candidates_dr3.py [--standin] [--no-fit] [--null-draws 30] [--null-fits 10] [--jobs 4]"""
import sys
sys.dont_write_bytecode = True
import argparse, concurrent.futures as cf, hashlib, json, os, tempfile, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import dry_run_driver as D
import cones_cut13 as CC
import seed_sweep as SS

ap = argparse.ArgumentParser()
ap.add_argument("--standin", action="store_true")
ap.add_argument("--no-fit", action="store_true")
ap.add_argument("--null-draws", type=int, default=30)
ap.add_argument("--null-fits", type=int, default=10)
ap.add_argument("--jobs", type=int, default=4)
args = ap.parse_args()
MUT = os.environ.pop("MUTATE", "").strip()
SFX = ("_standin" if args.standin else "") + (f"_MUTATE{MUT}" if MUT else "")
T0 = time.time()
D.init(False)                                                                       # the socket guard stays: nothing here touches the network
B = D.B
WB = REPO / "real_research" / "data" / "widebinaries"
IN = WB / "dr3_extract" / "dr4_ready_1"
FINAL_CSV, DELTA_CSV = WB / "dr3_extract" / "wide_binaries_dr3.csv", IN / "q1_delta_pairs.csv"
FULL_FITS, DELTA_FITS = IN / "q1_full_neighbours.fits", IN / "q1_delta_neighbours.fits"
OUTD = IN / ("cones_vs_extract" + SFX)
OUTD.mkdir(exist_ok=True)
LOG, CHK, RES = [], {}, {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def X(name, ok, detail=""):
    CHK[name.split()[0]] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))


def key(x, y):
    return (int(x), int(y)) if x < y else (int(y), int(x))


P("THE ALL-SOURCE CUT 13 ON ALL 10,231 DR3 CANDIDATES THROUGH THE DRIVER, AGAINST THE EXTRACT-BASED PATH (DR3 numbers are code-path tests, never results; non-scoring)"
  + ("   *** STAND-IN: the delta cones are built from the EXTRACT; nothing here is a result ***" if args.standin else "")
  + (f"   *** MUTATE={MUT}: " + {"1": "the delta file is left out (X1 must FAIL)", "2": "the delta parallax shifted by 1e-3 mas (X3 must FAIL)", "3": "the delta pair ids shifted by one (X1b must FAIL)"}[MUT] + " ***" if MUT else ""))
ext = D.extract_dir("dr3", "primary")
S = dict(np.load(ext / "stage_A.npz"))
sid = S["source_id"]
order = np.argsort(sid)
rows_of = lambda ids: order[np.searchsorted(sid[order], ids)]
tmp = Path(tempfile.mkdtemp())
b_ref, r_ref = D.run("dr3", "primary", "extract-builder", None, False, dump_candidates=str(tmp / "candidates.csv"))
assert r_ref["sha256"].startswith(D.REF_SHA_DR3), "the driver's reference CSV changed"
c1, c2 = CC.read_pairs_csv(tmp / "candidates.csv")
f1, f2 = CC.read_pairs_csv(FINAL_CSV)
d1, d2 = CC.read_pairs_csv(DELTA_CSV)
finalset = {key(x, y) for x, y in zip(f1.tolist(), f2.tolist())}
candset = {key(x, y) for x, y in zip(c1.tolist(), c2.tolist())}
assert len(c1) == len(candset) == 10231 and len(finalset) == 6210 and finalset <= candset and {key(x, y) for x, y in zip(d1.tolist(), d2.tolist())} == candset - finalset
a_rows, b_rows = rows_of(c1), rows_of(c2)
is_final = np.array([key(x, y) in finalset for x, y in zip(c1.tolist(), c2.tolist())])
P(f"candidates {len(c1):,d} (final {int(is_final.sum()):,d}, delta {int((~is_final).sum()):,d}); stage A {len(sid):,d} sources; reference CSV sha256 {r_ref['sha256'][:16]}")

# ------------------------------------------------------------------ the neighbour tables
t = time.time()
nb_full = CC.read_neighbour_fits(FULL_FITS)
if args.standin:
    ad, bd = rows_of(d1), rows_of(d2)
    nb_delta, _, _ = CC.build_extract_cones(S, ad, bd)
    nb_delta = {k: nb_delta[k] for k in nb_full if k in nb_delta}
else:
    nb_delta = CC.read_neighbour_fits(DELTA_FITS)
if MUT == "1":
    nb_delta = None                                                                 # the delta file is left out
if nb_delta is not None and MUT == "2":
    nb_delta = dict(nb_delta); nb_delta["parallax"] = np.asarray(nb_delta["parallax"], float) + 1e-3
if nb_delta is not None and MUT == "3":
    nb_delta = dict(nb_delta); nb_delta["pair_id"] = (nb_delta["pair_id"] + 1) % len(d1)
P(f"neighbour tables read in {time.time() - t:.0f} s: full-Q1 {len(nb_full['source_id']):,d} rows" + (f", delta {len(nb_delta['source_id']):,d} rows" if nb_delta is not None else ", delta file left out"))


def make_table(extra=None, with_delta=True):
    tab = CC.ConeTable().add(nb_full, f1, f2)
    if with_delta and nb_delta is not None:
        tab.add(nb_delta, d1, d2)
    if extra is not None:
        tab.add(*extra)
    return tab


# ------------------------------------------------------------------ X1 coverage
P("\nCONTROLS")
cones = make_table()
cov = cones.covered_mask(sid[a_rows], sid[b_rows])
cov_ok, cov_msg = bool(cov.all()), f"covered {int(cov.sum()):,d} of {len(c1):,d}, missing {int((~cov).sum())}"
if not cov_ok:
    cones = None
try:
    make_table(with_delta=False).flags(S, a_rows, b_rows, "literal", missing="error"); guard_ok, guard_msg = False, "no error raised"
except CC.ConeCoverageError as e:
    guard_ok, guard_msg = ("4021 of 10231" in str(e)), str(e)[:100]
X("X1 the combined cone table covers all 10,231 candidates, and a table of the final-pair file alone raises ConeCoverageError naming 4,021 of 10,231", cov_ok and guard_ok, f"{cov_msg}; final-only guard: {guard_msg}")
if cones is None:
    P("\nthe combined table does not cover the candidates: the analysis stops here (a pair without a cone is never treated as 'no third star')")
    ok = (MUT == "1") and (not CHK["X1"])
    P(f"\n[MUTATE CONTROL] X1 {'FAILED as designed' if not CHK['X1'] else 'did NOT fail'}" if MUT == "1" else "\nSTOPPED: X1 failed")
    (HERE / f"cones_all_candidates_dr3{SFX}.out").write_text("\n".join(LOG) + "\n")
    sys.exit(0 if ok else 1)

# ------------------------------------------------------------------ X0 plumbing: cones built from the extract for ALL candidates reproduce the extract paths' flags
fn_ext = {k: D.third_function(k, S) for k in ("extract-literal", "extract-builder", "extract-orbit")}
fl_ext = {k: np.asarray(f(S, a_rows, b_rows), bool) for k, f in fn_ext.items()}
nb_x, sx1, sx2 = CC.build_extract_cones(S, a_rows, b_rows)
cones_x = CC.ConeTable().add(nb_x, sx1, sx2)
x0_lit = np.array_equal(cones_x.flags(S, a_rows, b_rows, "literal")[0], fl_ext["extract-literal"])
x0_orb = np.array_equal(cones_x.flags(S, a_rows, b_rows, "orbit")[0], fl_ext["extract-builder"])
X("X0 cones built from the EXTRACT for all 10,231 candidates reproduce the extract paths' candidate flags exactly (literal = extract-literal; orbit = extract-builder)", x0_lit and x0_orb,
   f"flags: extract-literal {int(fl_ext['extract-literal'].sum())}, extract-builder {int(fl_ext['extract-builder'].sum())}, extract-orbit {int(fl_ext['extract-orbit'].sum())}")

# ------------------------------------------------------------------ X1b per-pair completeness (the pair_id mapping)
tabc = cones._table()
inv = {v: k for k, v in cones.key_to_id.items()}
have = set(zip(tabc["pair_id"].tolist(), tabc["comp"].tolist(), tabc["source_id"].tolist()))
lost = 0
for pid, comp, s in zip(nb_x["pair_id"].tolist(), nb_x["comp"].tolist(), nb_x["source_id"].tolist()):
    if (cones.key_to_id[(int(c1[pid]), int(c2[pid]))], comp, s) not in have:
        lost += 1
X("X1b every local-extract source inside the exact cone of each candidate is among the cone rows keyed to THAT pair in the combined table (the pair_id mapping)", lost == 0,
   f"{len(nb_x['source_id']):,d} (pair, comp, source) triples from the extract; missing from the combined table: {lost}")
del have

# ------------------------------------------------------------------ X3 column agreement for the sources the fetched files share with stage A
COLS9 = ("ra", "dec", "parallax", "parallax_error", "pmra", "pmdec", "pmra_error", "pmdec_error", "phot_g_mean_mag")
sid_sorted = sid[order]
x3_detail, x3_ok = [], True
for name, nb in (("full-Q1", nb_full), ("delta-Q1", nb_delta)):
    if nb is None:
        continue
    pos = np.searchsorted(sid_sorted, nb["source_id"]); pos = np.clip(pos, 0, len(sid_sorted) - 1)
    hit = sid_sorted[pos] == nb["source_id"]
    r = order[pos[hit]]
    worst, nanbad = 0.0, 0
    for c in COLS9:
        a, b = np.asarray(nb[c], float)[hit], np.asarray(S[c], float)[r]
        both_nan = np.isnan(a) & np.isnan(b)
        nanbad += int((np.isnan(a) ^ np.isnan(b)).sum())
        d = np.where(both_nan | np.isnan(a) | np.isnan(b), 0.0, np.abs(a - b) / np.maximum(1.0, np.abs(b)))
        worst = max(worst, float(d.max()) if len(d) else 0.0)
    x3_detail.append(f"{name}: {int(hit.sum()):,d} shared sources, max relative difference {worst:.1e}, NaN mismatches {nanbad}")
    x3_ok &= worst <= 1e-6 and nanbad == 0
X("X3 for every source the fetched files share with stage A, the nine numeric columns agree (relative difference <= 1e-6, NaNs matching)", x3_ok, "; ".join(x3_detail))
RES["x3"] = x3_detail

if MUT:
    expect = {"2": "X3", "3": "X1b"}[MUT]
    bit = not CHK[expect]
    P(f"\n[MUTATE CONTROL] MUTATE={MUT}: {expect} {'FAILED as designed' if bit else 'did NOT fail: the control does not bite'}; checks that failed: {[k for k, v in CHK.items() if not v]}")
    (HERE / f"cones_all_candidates_dr3{SFX}.out").write_text("\n".join(LOG) + "\n")
    sys.exit(0 if bit else 1)

# ------------------------------------------------------------------ Q1 the direct flags
fl = dict(fl_ext)
info = {}
for kind in ("cones-literal", "cones-orbit"):
    fn = D.third_function(kind, S, cones, "error")
    fl[kind] = np.asarray(fn(S, a_rows, b_rows), bool); info[kind] = fn.info
MATCH = (("literal", "extract-literal", "cones-literal"), ("orbit", "extract-builder", "cones-orbit"))
P("\nQ1  THE DIRECT EFFECT: candidates flagged by cut 13 (of 10,231)")
for k in ("extract-literal", "extract-builder", "extract-orbit", "cones-literal", "cones-orbit"):
    P(f"  {k:16s} {int(fl[k].sum()):4d} flagged  (final {int((fl[k] & is_final).sum())}, delta {int((fl[k] & ~is_final).sum())})")
viol = {}
for nm, e, c in MATCH:
    viol[nm] = int((fl[e] & ~fl[c]).sum())
viol["orbit_vs_extract-orbit"] = int((fl["extract-orbit"] & ~fl["cones-orbit"]).sum())
X("X2 flags(extract path) is a subset of flags(matched cones path): literal and orbit (and extract-orbit against cones-orbit)", all(v == 0 for v in viol.values()),
   "violations " + ", ".join(f"{k} {v}" for k, v in viol.items()))
extra_idx = {nm: np.flatnonzero(fl[c] & ~fl[e]) for nm, e, c in MATCH}
for nm, e, c in MATCH:
    P(f"  flagged by {c} but not by {e}: {len(extra_idx[nm])} pairs")
    for i in extra_idx[nm][:25]:
        P(f"      candidate index {int(i)}  source_id1 {int(c1[i])}  source_id2 {int(c2[i])}  {'final' if is_final[i] else 'delta'}  parallax {float(S['parallax'][a_rows[i]]):.2f} mas")
RES["q1"] = {k: dict(flagged=int(v.sum()), final=int((v & is_final).sum()), delta=int((v & ~is_final).sum())) for k, v in fl.items()}
RES["extra_flagged"] = {nm: [dict(index=int(i), source_id1=int(c1[i]), source_id2=int(c2[i]), final=bool(is_final[i])) for i in idx] for nm, idx in extra_idx.items()}
RES["cones_info"] = {k: {kk: (int(vv) if isinstance(vv, (np.integer,)) else vv) for kk, vv in v.items()} for k, v in info.items()}

# ------------------------------------------------------------------ X4 planted neighbours (positive and negative control)
from scipy.spatial import cKDTree
_v = np.stack([np.cos(np.radians(S["dec"][a_rows])) * np.cos(np.radians(S["ra"][a_rows])), np.cos(np.radians(S["dec"][a_rows])) * np.sin(np.radians(S["ra"][a_rows])), np.sin(np.radians(S["dec"][a_rows]))], -1)
_dist, _ = cKDTree(_v).query(_v, k=2)
isolated = _dist[:, 1] > 2 * np.sin(np.radians(1.0) / 2)                              # no other candidate's primary within 1 degree
lit_unflagged_delta = np.flatnonzero(~fl["cones-literal"] & ~is_final & isolated)
j = int(lit_unflagged_delta[0]); r0 = int(a_rows[j])


def planted(par_scale=1.0, dpm=0.0):
    nb = {k: np.array([0], np.int64) for k in ("pair_id", "comp", "source_id")}
    nb["source_id"] = np.array([4_000_000_000_000_000_000], np.int64)
    for c in ("ra", "dec", "parallax", "parallax_error", "pmra", "pmdec", "pmra_error", "pmdec_error"):
        nb[c] = np.array([float(S[c][r0])])
    nb["ra"] = nb["ra"] + 1e-4
    nb["parallax"] = nb["parallax"] * par_scale
    nb["pmra"] = nb["pmra"] + dpm; nb["pmdec"] = nb["pmdec"] + dpm
    nb["phot_g_mean_mag"] = np.array([15.0])
    for k, v in nb_full.items():                                                    # every key of the table, unset ones NaN / 0
        if k not in nb:
            nb[k] = np.array([np.nan]) if np.asarray(v).dtype.kind == "f" else np.zeros(1, np.asarray(v).dtype)
    return nb, np.array([c1[j]], np.int64), np.array([c2[j]], np.int64)


pos_fl = make_table(extra=planted()).flags(S, a_rows, b_rows, "literal")[0]
neg_fl = make_table(extra=planted(par_scale=1 / 3, dpm=50.0)).flags(S, a_rows, b_rows, "literal")[0]
X("X4 a kinematic twin planted into the cone of a delta pair the real cones-literal does not flag FLAGS it (and changes no other pair); a background star (a third of the parallax, a different proper motion) does NOT",
  bool(pos_fl[j]) and int((pos_fl != fl["cones-literal"]).sum()) == 1 and not neg_fl[j] and np.array_equal(neg_fl, fl["cones-literal"]),
  f"pair index {j}: twin -> flagged {bool(pos_fl[j])} (pairs changed {int((pos_fl != fl['cones-literal']).sum())}); background star -> flagged {bool(neg_fl[j])} (pairs changed {int((neg_fl != fl['cones-literal']).sum())})")

# ------------------------------------------------------------------ Q4 neighbour statistics
rows_exact_full, rows_exact_delta = len(nb_full["source_id"]), len(nb_delta["source_id"])
loc_delta = int(sum(1 for pid, comp, s in zip(nb_x["pair_id"].tolist(), nb_x["comp"].tolist(), nb_x["source_id"].tolist()) if not is_final[pid]))
loc_final = int(len(nb_x["source_id"]) - loc_delta)
per_pair = np.bincount(tabc["pair_id"])
ratio_d, ratio_f = rows_exact_delta / loc_delta, rows_exact_full / loc_final
P("\nQ4  NEIGHBOUR STATISTICS")
P(f"  exact two-cone rows: full-Q1 {rows_exact_full:,d}, delta-Q1 {rows_exact_delta:,d}; local-extract sources in the same cones (candidates): final pairs {loc_final:,d}, delta pairs {loc_delta:,d}")
P(f"  fetched rows / local-extract sources: final {ratio_f:.1f}, delta {ratio_d:.1f} (full Q1 reference 40.9)")
P(f"  cone rows per pair (the combined table): mean {per_pair[per_pair > 0].mean():.0f}, median {np.median(per_pair[per_pair > 0]):.0f}, max {int(per_pair.max())}")
P(f"  neighbours entering the criterion: literal {info['cones-literal'].get('n_neighbours')}, orbit {info['cones-orbit'].get('n_neighbours')}; cone rows used {info['cones-literal'].get('n_neighbour_rows')}")
RES["q4"] = dict(rows_full=rows_exact_full, rows_delta=rows_exact_delta, local_final=loc_final, local_delta=loc_delta, ratio_final=ratio_f, ratio_delta=ratio_d,
                 per_pair_mean=float(per_pair[per_pair > 0].mean()), per_pair_median=float(np.median(per_pair[per_pair > 0])), per_pair_max=int(per_pair.max()))

# ------------------------------------------------------------------ Q2 the final sets
P("\nQ2  THE FINAL SETS THE DRIVER WRITES (seed offset 0, the primary build)")
csvb, rep = {}, {}
for kind in ("extract-builder", "extract-literal", "extract-orbit"):
    csvb[kind], rep[kind] = D.run("dr3", "primary", kind, None, False)
for kind in ("cones-literal", "cones-orbit"):
    csvb[kind], rep[kind] = D.run("dr3", "primary", kind, None, False, cones=cones, missing_cones="error")
paths = {}
for kind, b in csvb.items():
    paths[kind] = OUTD / f"final_{kind}.csv"
    paths[kind].write_bytes(b)
FS = {k: SS.pair_set(b) for k, b in csvb.items()}
for k in csvb:
    P(f"  {k:16s} {rep[k]['n_pairs']:5d} final pairs  sha256 {rep[k]['sha256'][:16]}")
assert rep["extract-builder"]["sha256"] == r_ref["sha256"]


def flips(a, b):
    return (len(a - b) + len(b - a)) / 2, len(a - b), len(b - a)


def flagged_keys(f):
    return {key(c1[i], c2[i]) for i in np.flatnonzero(f)}


Q2 = {}
for nm, e, c in MATCH:
    fx, fc = FS[e], FS[c]
    tot, only_e, only_c = flips(fx, fc)
    d_out = len(fx & flagged_keys(fl[c]))
    Q2[nm] = dict(ext=e, cones=c, n_ext=len(fx), n_cones=len(fc), only_extract=only_e, only_cones=only_c, flips=tot, D_out=d_out, mc_component=tot - d_out, n_extra=int(len(extra_idx[nm])))
    P(f"  {c} against {e}: {len(fc)} against {len(fx)} final pairs; only in the extract path {only_e}, only in the cones path {only_c}; FLIPS (half the symmetric difference) {tot:.1f}; "
      f"of which the DIRECT cut-13 removals D_out {d_out}, the stage-G Monte-Carlo re-roll component {tot - d_out:.1f}")
tot_o, oe, oc = flips(FS["extract-orbit"], FS["cones-orbit"])
P(f"  cones-orbit against extract-orbit: {len(FS['cones-orbit'])} against {len(FS['extract-orbit'])}; flips {tot_o:.1f}")
tot_lo, _, _ = flips(FS["cones-literal"], FS["cones-orbit"])
P(f"  cones-literal against cones-orbit: flips {tot_lo:.1f}")
RES["q2"] = dict(matched=Q2, cones_orbit_vs_extract_orbit=tot_o, cones_literal_vs_cones_orbit=tot_lo, n_final={k: rep[k]["n_pairs"] for k in rep}, sha256={k: rep[k]["sha256"] for k in rep})

# ------------------------------------------------------------------ the independent-realization reference: the committed G-only seed sweep (50 builds of the primary's array, independent stage-G realizations)
SW = json.load(open(HERE / "seed_sweep_manifest_g50_dr3.json"))
R1 = np.array([(x + y) / 2 for x, y in SW["flips_vs_k0"]])
P(f"\nREFERENCE R1  independent stage-G realizations at the primary's array (the committed G-only sweep, {len(R1)} builds): flips against k0 mean {R1.mean():.1f}, SD {R1.std(ddof=1):.1f}, 16-84% {np.percentile(R1, 16):.1f}-{np.percentile(R1, 84):.1f}")
RES["reference_r1"] = dict(n=int(len(R1)), mean=float(R1.mean()), sd=float(R1.std(ddof=1)), p16=float(np.percentile(R1, 16)), p84=float(np.percentile(R1, 84)))

# ------------------------------------------------------------------ the NULL: the extract path plus n_extra random extra removals
P(f"\nNULL  ({args.null_draws} draws per matched pair: the extract path's flags plus n_extra random extra candidates flagged, seeds 20261230 + i)")
P("  note: removing one pair re-aligns the stage-G stream of every later pair, so the null draws are NESTED versions of one alternative realization; their spread is small and is NOT the spread of independent realizations (REFERENCE R1 above, and the G-only sweep's SD of gamma-hat, are)")
orig_third = D.third_function
NULL = {}
for nm, e, c in MATCH:
    n_extra = Q2[nm]["n_extra"]
    if n_extra == 0:
        P(f"  {nm}: n_extra = 0, the cones path flags nothing the extract path does not: the null is empty")
        NULL[nm] = dict(n_extra=0)
        continue
    base = fl[e]
    pool = np.flatnonzero(~base)
    fl_flips, csv_null = [], []
    for i in range(args.null_draws):
        rng = np.random.default_rng(20261230 + i)
        fx = base.copy(); fx[rng.choice(pool, n_extra, replace=False)] = True

        def tf(kind, S_, cones_=None, missing="error", _fx=fx):
            def fn(S__, a, b):
                assert len(a) == len(c1) and np.array_equal(S__["source_id"][a], c1)
                return _fx.copy()
            return fn
        D.third_function = tf
        try:
            b_, r_ = D.run("dr3", "primary", "extract-builder", None, False)
        finally:
            D.third_function = orig_third
        fl_flips.append(flips(FS[e], SS.pair_set(b_))[0]); csv_null.append(b_)
    fl_flips = np.array(fl_flips)
    NULL[nm] = dict(n_extra=n_extra, flips=fl_flips.tolist(), mean=float(fl_flips.mean()), sd=float(fl_flips.std(ddof=1)), p16=float(np.percentile(fl_flips, 16)), p84=float(np.percentile(fl_flips, 84)))
    P(f"  {nm}: n_extra {n_extra}; null flips mean {fl_flips.mean():.1f}, SD {fl_flips.std(ddof=1):.1f}, 16-84% {np.percentile(fl_flips, 16):.1f}-{np.percentile(fl_flips, 84):.1f}  "
      f"(min {fl_flips.min():.1f}, max {fl_flips.max():.1f});  the cones path: {Q2[nm]['flips']:.1f} (D_out {Q2[nm]['D_out']})")
    if nm == "literal":
        for i in range(min(args.null_fits, len(csv_null))):
            (OUTD / f"null_literal_{i:02d}.csv").write_bytes(csv_null[i])
RES["null"] = NULL

# ------------------------------------------------------------------ Q3 the fit effect
FIT = {}
if not args.no_fit:
    P("\nQ3  THE FIT EFFECT (the pipeline's own --catalog fit at the registered seed 20261216; DR3 code-path numbers)")
    jobs = {k: paths[k] for k in ("extract-builder", "extract-literal", "extract-orbit", "cones-literal", "cones-orbit")}
    nfit = min(args.null_fits, args.null_draws) if NULL.get("literal", {}).get("n_extra") else 0
    for i in range(nfit):
        jobs[f"null_literal_{i:02d}"] = OUTD / f"null_literal_{i:02d}.csv"
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = {k: ex.submit(SS.fit_via_pipeline_cli, p) for k, p in jobs.items()}
        FIT = {k: f.result() for k, f in futs.items()}
    for k in ("extract-builder", "extract-literal", "extract-orbit", "cones-literal", "cones-orbit"):
        f = FIT[k]
        P(f"  {k:16s} canonical {f['canonical']['g']:.4f} +- {f['canonical']['s']:.4f}; alt {f['alt']['g']:.4f} +- {f['alt']['s']:.4f}; pipeline self-test passed: {f['self_test_passed']}")
    shifts = {}
    for nm, e, c in MATCH:
        sh = {foot: (FIT[c][foot]["g"] - FIT[e][foot]["g"]) / FIT[e][foot]["s"] for foot in ("canonical", "alt")}
        shifts[nm] = sh
        P(f"  gamma-hat shift, {c} minus {e}: canonical {sh['canonical']:+.3f} sigma_fit, alt {sh['alt']:+.3f} sigma_fit   (build-to-build SD 0.3 to 0.44 sigma_fit)")
    sh_o = {foot: (FIT["cones-orbit"][foot]["g"] - FIT["extract-orbit"][foot]["g"]) / FIT["extract-orbit"][foot]["s"] for foot in ("canonical", "alt")}
    sh_p = {k: {foot: (FIT[k][foot]["g"] - FIT["extract-builder"][foot]["g"]) / FIT["extract-builder"][foot]["s"] for foot in ("canonical", "alt")} for k in ("cones-literal", "cones-orbit", "extract-literal")}
    P("  shifts against the PRIMARY (extract-builder): " + "; ".join(f"{k} {v['canonical']:+.3f} / {v['alt']:+.3f}" for k, v in sh_p.items()) + "  (canonical / alt, sigma_fit)")
    gS = {foot: np.array(SW["sigma_build"][foot]["gammas"], float) for foot in ("canonical", "alt")}
    pos = {k: {foot: float((FIT[k][foot]["g"] - gS[foot].mean()) / gS[foot].std(ddof=1)) for foot in ("canonical", "alt")} for k in ("extract-builder", "extract-literal", "extract-orbit", "cones-literal", "cones-orbit")}
    P(f"  REFERENCE R2  the committed G-only sweep's gamma-hat ({len(gS['canonical'])} builds): canonical mean {gS['canonical'].mean():.4f}, SD {gS['canonical'].std(ddof=1):.4f}; alt mean {gS['alt'].mean():.4f}, SD {gS['alt'].std(ddof=1):.4f}")
    P("  position of each variant in that distribution (SD units; canonical / alt): " + "; ".join(f"{k} {v['canonical']:+.2f} / {v['alt']:+.2f}" for k, v in pos.items()))
    nulls = [k for k in FIT if k.startswith("null_literal_")]
    nsh = {}
    if nulls:
        for foot in ("canonical", "alt"):
            v = np.array([(FIT[k][foot]["g"] - FIT["extract-literal"][foot]["g"]) / FIT["extract-literal"][foot]["s"] for k in nulls])
            nsh[foot] = dict(mean=float(v.mean()), sd=float(v.std(ddof=1)) if len(v) > 1 else float("nan"), values=v.tolist())
        P(f"  NULL shifts (extract-literal plus {NULL['literal']['n_extra']} random extra removals, {len(nulls)} draws): canonical mean {nsh['canonical']['mean']:+.3f}, SD {nsh['canonical']['sd']:.3f}; alt mean {nsh['alt']['mean']:+.3f}, SD {nsh['alt']['sd']:.3f} (sigma_fit)")
    RES["reference_r2"] = dict(canonical=dict(mean=float(gS["canonical"].mean()), sd=float(gS["canonical"].std(ddof=1))), alt=dict(mean=float(gS["alt"].mean()), sd=float(gS["alt"].std(ddof=1))), positions=pos)
    RES["q3"] = dict(fits={k: {kk: vv for kk, vv in v.items() if kk != "risk_lines"} for k, v in FIT.items()}, shifts=shifts, shift_orbit_vs_extract_orbit=sh_o, shifts_vs_primary=sh_p, null_shifts=nsh)

# ------------------------------------------------------------------ the hand estimates (frozen in the design file)
P("\nHAND ESTIMATES (frozen in CONES_VS_EXTRACT_DESIGN_FROZEN.md, scored by code)")
H = {}
H["H1"] = (2 <= fl["cones-literal"].sum() <= 7 and 0 <= fl["cones-orbit"].sum() <= 2, f"cones-literal flags {int(fl['cones-literal'].sum())} (2 to 7), cones-orbit {int(fl['cones-orbit'].sum())} (0 to 2)")
H["H2"] = (all(v == 0 for v in viol.values()), f"X2 violations {viol}")
H["H3"] = (80 <= Q2["literal"]["flips"] <= 250 and Q2["literal"]["D_out"] >= 2, f"flips {Q2['literal']['flips']:.1f} (80 to 250), D_out {Q2['literal']['D_out']} (>= 2)")
nl = NULL.get("literal", {})
H["H4"] = (bool(nl.get("n_extra")) and 100 <= nl["mean"] <= 230 and nl["p16"] - Q2["literal"]["D_out"] <= Q2["literal"]["flips"] <= nl["p84"] + Q2["literal"]["D_out"],
           (f"null mean {nl['mean']:.1f} (100 to 230); cones flips {Q2['literal']['flips']:.1f} in [{nl['p16'] - Q2['literal']['D_out']:.1f}, {nl['p84'] + Q2['literal']['D_out']:.1f}]" if nl.get("n_extra") else "no null (n_extra = 0)"))
if FIT:
    H["H5"] = (all(abs(shifts[nm][foot]) < 0.8 for nm in shifts for foot in ("canonical", "alt")), "shifts " + str({nm: {f: round(v, 3) for f, v in s.items()} for nm, s in shifts.items()}) + " (|shift| < 0.8 sigma_fit)")
H["H6"] = (35 <= ratio_d <= 47, f"delta rows / local-extract sources {ratio_d:.1f} (35 to 47)")
H["H7"] = (CHK["X3"], "X3 " + ("passes" if CHK["X3"] else "fails"))
for k, (ok_, txt) in H.items():
    P(f"  {k}: {'PASS' if ok_ else 'MISS'}  {txt}")
RES["hand_estimates"] = {k: dict(ok=bool(v[0]), text=v[1]) for k, v in H.items()}

ok = all(CHK.values())
P(f"\n{sum(CHK.values())}/{len(CHK)} controls pass -> {'ALL PASS' if ok else 'CONTROL FAILURES: Q1-Q3 are not to be interpreted'}   ({time.time() - T0:.0f} s)")
RES.update(controls=CHK, standin=bool(args.standin), seconds=round(time.time() - T0, 1),
           hashes=dict(delta_fits=hashlib.sha256(open(DELTA_FITS, "rb").read()).hexdigest() if (DELTA_FITS.exists() and not args.standin) else None, full_fits=json.load(open(HERE / "manifest_q1_full.json"))["sha256"],
                       delta_pairs_csv=hashlib.sha256(open(DELTA_CSV, "rb").read()).hexdigest(), final_csv_sha256=r_ref["sha256"], final_csvs={k: rep[k]["sha256"] for k in rep}))
(HERE / f"cones_all_candidates_dr3{SFX}.out").write_text("\n".join(LOG) + "\n")
(HERE / f"cones_all_candidates_dr3{SFX}.json").write_text(json.dumps(RES, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)) + "\n")
sys.exit(0 if ok else 1)
