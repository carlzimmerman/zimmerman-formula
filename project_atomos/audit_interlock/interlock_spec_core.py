#!/usr/bin/env python3
"""interlock_spec_core.py -- the MEASURED inputs for INTERLOCK_SPEC.md (part 1 of 2).

Independent re-measurement (I do not trust any prior audit's number; every figure below is
recomputed from the real code and the committed depth-8/9/10 artifacts):

  S1  window / sigma convention: what the search's hit predicate actually is, in full-width
      relative units, probed against the REAL engine.scoring.score_value.
  S2  the m_p/m_e window contradiction between two prior audits, resolved by arithmetic on the
      CODATA-2022 digit string (is the direct ratio's rel uncertainty 1.7e-11 or 1.7e-14?).
  S3  the look-elsewhere COUNT: raw vs distinct vs float64-distinguishable, per-layer
      (skeleton x germ-recipe) decomposition solved from the committed raw counts, growth rates.
  S4  the LOCAL density rho_i (per unit ln|v|) at each target at depths 8/9/10, its growth, and
      the verification that measured hits H_i == rho_i * W_i (so global N*W is the wrong model).
  S5  CORE / DRESSING decomposition of the committed depth-10 records + the interlock chance
      model calibrated against (a) the observed core-level coincidence counts and (b) a
      label-permutation null.

Writes audit_interlock/interlock_spec_core.json. Local-only. No network, no commit.
"""
from __future__ import annotations
import json, math, sqlite3, sys, time
from array import array
from collections import defaultdict
from pathlib import Path

import numpy as np
from mpmath import mp
mp.dps = 40

ROOT = Path("/Users/carlzimmerman/new_physics/project_atomos")
sys.path.insert(0, str(ROOT))

import targets.pdg_constants as pdg                                    # noqa: E402
from engine.scoring import measurement_tol, score_value                # noqa: E402
from exhaust_parallel import sm_target_keys                            # noqa: E402
import exhaust_depthN_forced as DN                                     # noqa: E402

OUT = {}
CHECKS = []


def check(msg, cond):
    CHECKS.append(bool(cond))
    print(f"   [{'PASS' if cond else 'FAIL'}] {msg}")


def rule(t):
    print("\n" + "=" * 104)
    print(t)
    print("=" * 104)


DS = pdg.load()
POOL = sm_target_keys()                       # 19 searched (holdout excluded)
POOL_H = sm_target_keys(include_holdout=True)  # what retention actually used
HOLDOUT = sorted(pdg.HOLDOUT_KEYS)

# ============================================================ S1 window convention
rule("S1  WINDOW / SIGMA CONVENTION -- what the search's hit predicate IS")
print("""  grind.sweep_target_streamed: tol = measurement_tol(target); a value is a HIT iff
  score_value(v, target).rel_error <= tol, with rel_error = |v-tv|/|tv| and tol = sigma/|tv|.
  => half-width = 1.000 sigma; FULL relative window W = 2*tol. All bits below use W.\n""")
print(f"  {'target':20}{'tol=rel_prec':>14}{'W=2*tol':>12}{'bits=log2(1/W)':>16}"
      f"{'sigma@edge':>12}{'clamped':>9}")
print("  " + "-" * 90)
WIN = {}
for k in POOL_H:
    t = DS[k]
    tol = measurement_tol(t)
    W = 2.0 * tol
    tv = float(t.value)
    # probe the REAL predicate at 0.999 and 1.001 of the tol edge (mpmath: 1e-10 windows are
    # below float64 resolution on an O(1e3) central value, so a float probe is meaningless)
    mtv = mp.mpf(t.value) if not isinstance(t.value, mp.mpf) else t.value
    lo = score_value(mtv * (1 + mp.mpf("0.999") * mp.mpf(tol)), t)
    hi = score_value(mtv * (1 + mp.mpf("1.001") * mp.mpf(tol)), t)
    edge = score_value(mtv * (1 + mp.mpf(tol)), t)
    clamped = "yes" if abs(tol - t.rel_precision) > 1e-18 else ""
    WIN[k] = dict(tol=tol, W=W, bits=math.log2(1.0 / W), value=tv,
                  sigma=float(t.sigma), rel=t.rel_precision, sector=t.sector,
                  n_digits=float(t.n_digits), bit_cap=float(t.n_digits) * math.log2(10.0))
    print(f"  {k:20}{tol:>14.4e}{W:>12.4e}{math.log2(1/W):>16.2f}{edge.n_sigma:>12.6f}{clamped:>9}")
    # score_value casts to float64 internally, so the edge is resolved to ~eps/|tv|/tol
    # (worst case a_e: 1.5e-6 of a sigma). Tolerance 1e-4 sigma is far inside that.
    check(f"{k}: hit at 0.999*tol, miss at 1.001*tol, edge == 1.0000 sigma",
          (lo.rel_error <= tol) and (hi.rel_error > tol) and abs(edge.n_sigma - 1.0) < 1e-4)
OUT["windows"] = WIN
n_clamped = sum(1 for k in POOL_H if abs(measurement_tol(DS[k]) - DS[k].rel_precision) > 1e-18)
check(f"min_tol=1e-10 / max_tol=0.2 clamps bind on {n_clamped} of {len(POOL_H)} targets",
      n_clamped == 0)

# the per-target Gate-A bit cap vs the window bits
print(f"\n  Gate A's own per-target cap (_bit_cap = n_digits*log2(10)) vs window bits log2(1/W):")
print(f"  {'target':20}{'cap':>9}{'window bits':>13}{'excess':>9}")
print("  " + "-" * 54)
exc = []
for k in POOL_H:
    w = WIN[k]
    e = w["bit_cap"] - w["bits"]
    exc.append(e)
    print(f"  {k:20}{w['bit_cap']:>9.2f}{w['bits']:>13.2f}{e:>9.3f}")
check(f"cap exceeds window bits by exactly +1.000 bit on every target "
      f"(min {min(exc):.6f}, max {max(exc):.6f}) -- n_digits = -log10(rel) so cap = log2(1/rel) "
      f"= log2(1/W)+1", max(abs(e - 1.0) for e in exc) < 1e-9)
OUT["bit_cap_excess_bits"] = 1.0

# ============================================================ S2 m_p/m_e window, resolved
rule("S2  RESOLVING THE m_p/m_e WINDOW CONTRADICTION (two prior audits disagree by 1000x)")
# CODATA-2022 direct ratio measurements (typed from the standard digit strings; cross-checked
# below against the repo's OWN stored alpha^-1 and a_e, which are CODATA-2022 to every digit).
CODATA = {
    "r_p_e":   (1836.152673426,   0.000000032),
    "r_mu_e":  (206.7682827,      0.0000046),
    "r_n_p":   (1.00137841946,    0.00000000045),
    "alpha_em_inv_0": (137.035999177, 0.000000021),
    "a_e":     (1.15965218059e-3, 0.00000000013e-3),
}
print(f"  {'key':18}{'CODATA direct':>20}{'sigma':>13}{'rel':>11}"
      f"{'stored rel':>12}{'ratio':>9}{'bits':>8}")
print("  " + "-" * 92)
for k, (v, s) in CODATA.items():
    t = DS[k]
    rel_d = s / v
    r = t.rel_precision / rel_d
    print(f"  {k:18}{v:>20.12g}{s:>13.3e}{rel_d:>11.4e}"
          f"{t.rel_precision:>12.4e}{r:>9.2f}{math.log2(max(r,1e-30)):>8.2f}")
    OUT.setdefault("codata_vs_stored", {})[k] = dict(
        codata_rel=rel_d, stored_rel=t.rel_precision, ratio=r, bits=math.log2(max(r, 1e-30)))
# the repo's stored alpha and a_e sigmas must equal CODATA exactly -> proves the source
check("repo's stored alpha^-1 sigma == CODATA-2022 exactly (source cross-check)",
      abs(float(DS['alpha_em_inv_0'].sigma) - 2.1e-8) < 1e-20)
check("repo's stored a_e sigma == CODATA-2022 exactly (source cross-check)",
      abs(float(DS['a_e'].sigma) - 1.3e-13) < 1e-21)
# the arithmetic that settles it: 1836.152673426(32) means +-3.2e-8 ABSOLUTE
rel_direct = 3.2e-8 / 1836.152673426
print(f"""
  ARITHMETIC: '1836.152673426(32)' = 1836.152673426 +/- 3.2e-8  ->  rel = {rel_direct:.4e}.
  GATE_POWER_ANALYSIS.py:41 writes '3.2e-11/1836.15' = {3.2e-11/1836.15:.3e} and BITS_RULE.py:14
  writes 3.49e-14: BOTH are ~1000x too tight (they divided an already-relative 3.2e-11 by the
  value a second time, or mistook 3.2e-8 for 3.2e-11).
  The 'windows' audit repeated GPA's 3.2e-11 as if it were the absolute sigma -> its
  '24,459x / 14.6 bits' figure is wrong. The 'ceiling_math' audit is CORRECT.
  TRUE picture: stored (propagated) rel = {DS['r_p_e'].rel_precision:.4e}; direct CODATA rel =
  {rel_direct:.4e}; the search's window is {DS['r_p_e'].rel_precision/rel_direct:.1f}x too WIDE
  = {math.log2(DS['r_p_e'].rel_precision/rel_direct):.2f} bits left on the table (not 14.6).""")
OUT["r_p_e_direct_rel"] = rel_direct
OUT["r_p_e_bits_left_on_table"] = math.log2(DS['r_p_e'].rel_precision / rel_direct)
check("m_p/m_e: the direct-ratio rel uncertainty is ~1.7e-11, NOT 1.7e-14 "
      "(GPA/BITS_RULE and the 'windows' audit are wrong; 'ceiling_math' is right)",
      abs(math.log10(rel_direct) + 10.76) < 0.2)
# stored CENTRAL value already equals the direct ratio to ~1e-11 -> central from the direct
# measurement, sigma from propagation: an internal inconsistency, provable in-repo.
d = abs(float(DS['r_p_e'].value) - 1836.152673426) / 1836.152673426
print(f"  in-repo proof: stored central r_p_e differs from the CODATA direct ratio by "
      f"{d:.2e} rel = {d/rel_direct:.2f} direct-sigma -> the CENTRAL value is the direct "
      f"measurement while the SIGMA is propagated from two MeV masses.")
check("stored r_p_e central == CODATA direct ratio to better than its own propagated window",
      d < DS['r_p_e'].rel_precision)

# ============================================================ S3 look-elsewhere count
rule("S3  THE LOOK-ELSEWHERE COUNT: raw vs distinct vs float64-distinguishable, per layer")
COMMITTED = {}   # depth -> (raw, distinct, n_skel_total, splits)
for d in (6, 7, 8, 9, 10):
    for cand in (ROOT / "results_grind" / f"depth_{d}" / "build_meta.json",):
        if cand.exists():
            m = json.loads(cand.read_text())
            COMMITTED[d] = (m["raw_candidates"], m["distinct_by_value"],
                            m.get("n_skeletons_total"), [tuple(s) for s in m["splits"]])
# depths 6/7: the committed replay ground truth inside grind.py itself
import grind                                                          # noqa: E402
for d, c in grind.REPLAY_COMMITTED.items():
    COMMITTED[d] = (c["raw"], c["distinct"], None,
                    [(b, d - 1 - b) for b in range(1, d - 3)])
for d, v in sorted(COMMITTED.items()):
    print(f"  depth {d:>2}: raw {v[0]:>12,d}  distinct {v[1]:>12,d}  "
          f"R=raw/distinct {v[0]/v[1]:.3f}  n_skel_total {v[2]}")
OUT["committed_counts"] = {str(d): dict(raw=v[0], distinct=v[1], n_skel_total=v[2])
                           for d, v in sorted(COMMITTED.items())}

# --- recipe counts from the REAL code
alpha = DN.build_alphabet(None, None)
n_free = len(DN._free_germ_keys(alpha))
nrec = {g: DN._germ_recipe_count(alpha, n_free, g) for g in range(3, 12)}
print(f"\n  germ layer (real DN._germ_recipe_count, n_free={n_free}):")
print("   g_s: " + "  ".join(f"{g}:{nrec[g]:,}" for g in range(3, 10)))
print("   ratios: " + "  ".join(f"{nrec[g+1]/nrec[g]:.2f}" for g in range(3, 9)))

# --- skeleton counts: compute b_s=1,2 directly from the REAL code, then SOLVE b_s=3..6 from
#     the committed raw counts via raw(D) = sum_{b_s=1..D-4} n_skel(b_s)*nrec(D-1-b_s).
t0 = time.time()
nskel = {b: len(DN._skeleton_value_nodes(alpha, b)) for b in (1, 2)}
print(f"\n  skeleton layer measured directly: n_skel(1)={nskel[1]}, n_skel(2)={nskel[2]} "
      f"({time.time()-t0:.1f}s)")
check(f"raw(6) identity from the two directly-measured skeleton layers reproduces the committed "
      f"replay ground truth 236,624 exactly",
      13 * nrec[4] + 73 * nrec[3] == COMMITTED[6][0])
for D in (7, 8, 9, 10):
    if D not in COMMITTED:
        continue
    b_new = D - 4
    known = sum(nskel[b] * nrec[D - 1 - b] for b in range(1, b_new))
    rem = COMMITTED[D][0] - known
    q, r = divmod(rem, nrec[D - 1 - b_new])
    nskel[b_new] = q
    check(f"n_skel({b_new}) solves EXACTLY from committed raw(D={D}): {q:,} (remainder {r})", r == 0)
# independent cross-check of the same numbers: committed n_skeletons_total at D = sum n_skel(1..D-4)
for D in (8, 9, 10):
    tot = sum(nskel[b] for b in range(1, D - 3))
    check(f"sum n_skel(1..{D-4}) = {tot:,} == committed depth-{D} n_skeletons_total "
          f"{COMMITTED[D][2]:,} (independent route to the same layer counts)",
          tot == COMMITTED[D][2])
print("  n_skel(b_s) = " + ", ".join(f"{b}:{nskel[b]:,}" for b in sorted(nskel)))
tot_sk = sum(nskel[b] for b in range(1, 7))
check(f"sum n_skel(1..6) = {tot_sk:,} == committed depth-10 n_skeletons_total "
      f"{COMMITTED[10][2]:,}", tot_sk == COMMITTED[10][2])
for D in sorted(COMMITTED):
    if D < 6:
        continue
    pred = sum(nskel[b] * nrec[D - 1 - b] for b in range(1, D - 3))
    check(f"raw({D}) identity reproduces committed exactly: {pred:,} vs {COMMITTED[D][0]:,}",
          pred == COMMITTED[D][0])
OUT["n_skel"] = {str(b): nskel[b] for b in sorted(nskel)}
OUT["n_recipe"] = {str(g): nrec[g] for g in sorted(nrec)}
OUT["n_free_germ_keys"] = n_free

ds = [COMMITTED[d][1] for d in (6, 7, 8, 9, 10)]
ratios = [ds[i + 1] / ds[i] for i in range(4)]
print(f"\n  DISTINCT-value growth ratios (D6->10): " + ", ".join(f"{r:.3f}" for r in ratios)
      + f"   -> last {ratios[-1]:.3f} = {math.log2(ratios[-1]):.3f} bits/depth")
print(f"  published model 30^(D-4): at D=10 gives {30.0**6:.3e} vs real distinct "
      f"{ds[-1]:,} = {30.0**6/ds[-1]:.1f}x over-count; at D=18 {30.0**14:.3e}")
OUT["distinct_growth_ratios"] = ratios
OUT["B_distinct_last"] = ratios[-1]

# --- float64-distinguishable
V = {}
for d in (8, 9, 10):
    p = ROOT / "results_grind" / f"depth_{d}" / "values.f64"
    V[d] = np.fromfile(p, dtype=np.float64)
    check(f"depth-{d} values.f64 length {len(V[d]):,} == committed distinct {COMMITTED[d][1]:,}",
          len(V[d]) == COMMITTED[d][1])
u10 = np.unique(V[10])
print(f"\n  depth-10: {len(V[10]):,} mpmath-distinct keys -> {len(u10):,} distinct float64 "
      f"({len(V[10])/len(u10):.3f}x, {math.log2(len(V[10])/len(u10)):.3f} bits)")
fin = np.isfinite(V[10]) & (V[10] > 0)
print(f"           finite&positive float64: {int(fin.sum()):,} "
      f"(inf/overflow {int((~np.isfinite(V[10])).sum()):,}, <=0/underflow "
      f"{int((V[10] <= 0).sum()):,})")
OUT["float64_distinct_d10"] = int(len(u10))

# ============================================================ S4 LOCAL density
rule("S4  LOCAL DENSITY rho_i (per unit ln|v|) AT EACH TARGET -- the correct chance model")
BAND = 0.1          # +-0.1 in ln  => 0.2 ln of support
LN = {d: np.log(V[d][np.isfinite(V[d]) & (V[d] > 0)]) for d in (8, 9, 10)}
for d in (8, 9, 10):
    print(f"  depth {d}: {len(LN[d]):,} finite positive values, "
          f"ln span {LN[d].min():.1f} .. {LN[d].max():.1f} "
          f"({(LN[d].max()-LN[d].min())/math.log(10):.0f} decades)")
    LN[d].sort()
OUT["ln_span_decades_d10"] = float((LN[10].max() - LN[10].min()) / math.log(10))

RHO = {}
print(f"\n  {'target':20}{'rho(d8)':>12}{'rho(d9)':>12}{'rho(d10)':>12}{'B_rho':>8}"
      f"{'H_pred=rho*W':>14}{'H_meas':>9}{'ratio':>8}")
print("  " + "-" * 96)
HITS = {}
for k in POOL_H:
    tv, W = WIN[k]["value"], WIN[k]["W"]
    lt = math.log(abs(tv))
    r = {}
    for d in (8, 9, 10):
        i0, i1 = np.searchsorted(LN[d], [lt - BAND, lt + BAND])
        r[d] = (i1 - i0) / (2 * BAND)
    # measured hits at depth 10 with the REAL predicate
    v = V[10]
    idx = np.nonzero(np.abs(v - tv) <= abs(tv) * WIN[k]["tol"] * (1 + 1e-9))[0]
    n = 0
    for i in idx:
        if score_value(float(v[i]), DS[k]).rel_error <= WIN[k]["tol"]:
            n += 1
    HITS[k] = n
    Hpred = r[10] * W
    B = (r[10] / r[8]) ** 0.5 if r[8] > 0 else float("nan")
    RHO[k] = dict(rho8=r[8], rho9=r[9], rho10=r[10], B_rho=B, H_pred=Hpred, H_meas=n)
    print(f"  {k:20}{r[8]:>12,.0f}{r[9]:>12,.0f}{r[10]:>12,.0f}{B:>8.3f}"
          f"{Hpred:>14,.1f}{n:>9,d}{(n/Hpred if Hpred>0 else float('nan')):>8.2f}")
OUT["rho"] = RHO
tot_meas = sum(HITS[k] for k in POOL)
check(f"my recount of depth-10 in-window hits over the 19 searched targets = {tot_meas:,} "
      f"== committed VERDICT.json n_hits 82,613", tot_meas == 82613)
good = [k for k in POOL_H if RHO[k]["H_pred"] > 5]
err = [HITS[k] / RHO[k]["H_pred"] for k in good]
print(f"\n  H_meas / (rho*W) over the {len(good)} targets with H_pred>5: "
      f"min {min(err):.3f}  median {float(np.median(err)):.3f}  max {max(err):.3f}")
check("the LOCAL model H = rho*W is unbiased (median within 10% of 1.0)",
      abs(float(np.median(err)) - 1.0) < 0.10)
Nglob = len(V[10])
naive = [Nglob * WIN[k]["W"] / HITS[k] for k in POOL_H if HITS[k] > 0]
print(f"  GLOBAL model N*W over-states measured hits by median "
      f"{float(np.median(naive)):.0f}x  (min {min(naive):.0f}x, max {max(naive):.0f}x) "
      f"-> = {math.log2(float(np.median(naive))):.2f} bits, the 632-decade dynamic range.")
OUT["global_over_local_factor_median"] = float(np.median(naive))
Bs = [RHO[k]["B_rho"] for k in POOL_H if RHO[k]["rho8"] > 100]
print(f"  rho growth per depth (sqrt of d8->d10), median over {len(Bs)} targets: "
      f"{float(np.median(Bs)):.3f} = {math.log2(float(np.median(Bs))):.3f} bits/depth")
OUT["B_rho_median"] = float(np.median(Bs))

# ============================================================ S5 cores & the interlock model
rule("S5  CORE / DRESSING DECOMPOSITION + INTERLOCK CHANCE MODEL, calibrated on depth 10")
con = sqlite3.connect(str(ROOT / "results_grind" / "depth_10" / "records.sqlite"))
rows = con.execute("SELECT idx,value,b_s,skeleton_idx,recipe FROM records").fetchall()
con.close()
print(f"  retained records: {len(rows):,}")

FORCED = set(DN._forced_keys_present(alpha))


def core_ids(recipe_json, b_s, sk):
    """L1 core = (b_s, skeleton). L2 core = (b_s, skeleton, free-germ KEY, forced net exponents);
    the L2 dressing is then ONLY the net exponent of the single free germ."""
    steps = json.loads(recipe_json)
    net = defaultdict(float)
    for gk, opname, e in steps:
        net[gk] += (1.0 if opname == "MUL" else -1.0) * float(e)
    free = [g for g in net if g not in FORCED]
    fk = free[0] if len(free) == 1 else "|".join(sorted(free))
    forced_net = tuple(sorted((g, round(net[g], 6)) for g in net if g in FORCED))
    return (b_s, sk), (b_s, sk, fk, forced_net), round(net.get(fk, 0.0), 6)


tgt_of = defaultdict(list)      # record idx -> [target keys]
recs = []
for idx, v, b_s, sk, rj in rows:
    l1, l2, dress = core_ids(rj, b_s, sk)
    ks = [k for k in POOL if abs(v - WIN[k]["value"]) <= abs(WIN[k]["value"]) * WIN[k]["tol"]
          and score_value(float(v), DS[k]).rel_error <= WIN[k]["tol"]]
    recs.append((idx, v, b_s, sk, l1, l2, dress, ks))
    for k in ks:
        tgt_of[k].append(idx)
assigned = sum(len(r[7]) for r in recs)
check(f"target-assignment over retained records = {assigned:,} == 82,613 committed hits "
      f"(19 searched targets)", assigned == 82613)

for lvl, gi in (("L1 (skeleton only)", 4), ("L2 (skeleton+free-germ key+forced nets)", 5)):
    per = defaultdict(set)
    for r in recs:
        for k in r[7]:
            per[r[gi]].add(k)
    hist = defaultdict(int)
    for c, s in per.items():
        hist[len(s)] += 1
    kmax = max(hist)
    print(f"\n  {lvl}: {len(per):,} cores carry >=1 hit; distinct-targets-per-core histogram")
    print("    " + "  ".join(f"{k}:{hist[k]:,}" for k in sorted(hist)))
    print(f"    max distinct targets on ONE core = {kmax}")
    OUT.setdefault("core_hist", {})[lvl] = {str(k): hist[k] for k in sorted(hist)}
    OUT.setdefault("core_kmax", {})[lvl] = kmax
    OUT.setdefault("cores_with_hits", {})[lvl] = len(per)

# total core counts (denominators) -- L1: n_skel(b_s) per split ; L2: x n_free x forced-net combos
n_cores_L1 = sum(nskel[b] for b in range(1, 7))
# L2 count: for each split (b_s,g_s), #(skeleton x free-key x forced-net-pair) =
# n_skel(b_s) * n_free * sum_over_compositions |net(n0)|*|net(n1)| , dressing = |net(n2)|
n_cores_L2 = 0
R_L2 = []
for (b_s, g_s) in COMMITTED[10][3]:
    per_split = 0
    dress_tot = 0
    for (n0, n1, n2) in DN._compositions(g_s, 3):
        f01 = len(DN._net_exps(n0)) * len(DN._net_exps(n1))
        per_split += f01
        dress_tot += f01 * len(DN._net_exps(n2))
    n_cores_L2 += nskel[b_s] * n_free * per_split
    R_L2.append(dress_tot / per_split)
print(f"\n  DENOMINATORS at depth 10:  n_cores(L1) = {n_cores_L1:,}   "
      f"n_cores(L2) = {n_cores_L2:,}")
print(f"  dressings per core: L1 = raw/n_cores = {COMMITTED[10][0]/n_cores_L1:,.0f}   "
      f"L2 = {float(np.mean(R_L2)):.1f} (mean |net_exps| of the free germ's step share)")
OUT["n_cores_L1_d10"] = n_cores_L1
OUT["n_cores_L2_d10"] = n_cores_L2
OUT["R_L1_d10"] = COMMITTED[10][0] / n_cores_L1
OUT["R_L2_d10"] = float(np.mean(R_L2))

# --- ANALYTIC interlock chance model, per core level:
#     E[#cores hitting every target in T] = n_cores * PROD_i min(1, H_i / n_cores)
def E_interlock(T, H, n_cores):
    e = float(n_cores)
    for k in T:
        e *= min(1.0, H[k] / n_cores)
    return e


# calibrate: predicted vs OBSERVED number of L1 cores reaching >= k distinct targets
perL1 = defaultdict(set)
for r in recs:
    for k in r[7]:
        perL1[r[4]].add(k)
obs_ge = {k: sum(1 for s in perL1.values() if len(s) >= k) for k in range(1, 13)}
# analytic >= k via Poisson-binomial over the 19 per-target per-core probabilities
p_i = np.array([min(1.0, HITS[k] / n_cores_L1) for k in POOL])
# distribution of #targets hit by one core
dist = np.zeros(len(p_i) + 1)
dist[0] = 1.0
for p in p_i:
    dist[1:] = dist[1:] * (1 - p) + dist[:-1] * p
    dist[0] *= (1 - p)
pred_ge = {k: n_cores_L1 * float(dist[k:].sum()) for k in range(1, 13)}
print(f"\n  MODEL CALIBRATION (L1 cores, independence across targets):")
print(f"  {'k':>3}{'observed cores >=k':>20}{'model (indep)':>16}{'obs/model':>11}")
print("  " + "-" * 52)
for k in range(1, 12):
    o, p = obs_ge[k], pred_ge[k]
    print(f"  {k:>3}{o:>20,d}{p:>16,.1f}{(o/p if p > 0 else float('nan')):>11.3f}")
ratios_k = [obs_ge[k] / pred_ge[k] for k in range(2, 9) if pred_ge[k] > 5]
check(f"HOMOGENEOUS-core independence (every core equally likely to reach a target) is "
      f"BADLY ANTI-CONSERVATIVE at high k: obs/model = {obs_ge[6]/pred_ge[6]:.1f}x at k=6 and "
      f"{obs_ge[8]/pred_ge[8]:.0f}x at k=8. Interlock bits may NOT be computed by multiplying "
      f"windows over a flat core count.", obs_ge[8] / pred_ge[8] > 10)
check(f"the same model is CONSERVATIVE at low k (obs/model {obs_ge[2]/pred_ge[2]:.2f} at k=2), "
      f"so the failure is a REACH-HETEROGENEITY (heavy-tailed) effect, not a uniform offset",
      obs_ge[2] / pred_ge[2] < 1.0)
n_zero = n_cores_L1 - len(perL1)
print(f"\n  ROOT CAUSE: only {len(perL1):,} of {n_cores_L1:,} cores ({100*len(perL1)/n_cores_L1:.1f}%) "
      f"place ANY dressed value inside ANY target window, although the mean is "
      f"{assigned/n_cores_L1:.2f} hits per core -- the per-core REACH into the O(1) decade is "
      f"heavy-tailed, so coincidences concentrate. Quantified in interlock_spec_model.py.")
OUT["n_cores_zero_reach_L1"] = int(n_zero)
OUT["calib_obs_ge"] = obs_ge
OUT["calib_model_ge"] = pred_ge

# --- permutation null: shuffle which core each hit belongs to, preserving per-core record
#     counts and per-target marginals
rng = np.random.default_rng(20260728)
core_of = {}
for i, r in enumerate(recs):
    core_of[i] = r[4]
core_list = [r[4] for r in recs]
tk_list = [r[7] for r in recs]
nperm = 200
null_ge = defaultdict(list)
for _ in range(nperm):
    perm = rng.permutation(len(recs))
    per = defaultdict(set)
    for i, j in enumerate(perm):
        if tk_list[j]:
            per[core_list[i]].update(tk_list[j])
    for k in range(1, 13):
        null_ge[k].append(sum(1 for s in per.values() if len(s) >= k))
print(f"\n  PERMUTATION NULL ({nperm} shuffles of hit->core assignment, marginals preserved):")
print(f"  {'k':>3}{'observed':>12}{'null mean':>12}{'null sd':>10}{'z':>9}{'obs/null':>10}")
print("  " + "-" * 58)
for k in range(2, 12):
    m, s = float(np.mean(null_ge[k])), float(np.std(null_ge[k]))
    z = (obs_ge[k] - m) / s if s > 0 else float("nan")
    print(f"  {k:>3}{obs_ge[k]:>12,d}{m:>12,.1f}{s:>10.1f}{z:>9.2f}"
          f"{(obs_ge[k]/m if m>0 else float('nan')):>10.3f}")
    OUT.setdefault("perm_null", {})[str(k)] = dict(obs=obs_ge[k], mean=m, sd=s, z=z)
zs = [(obs_ge[k] - np.mean(null_ge[k])) / (np.std(null_ge[k]) or 1) for k in range(2, 10)]
check("no ANTI-conservative core-level clustering: observed coincidences are at or BELOW the "
      f"permutation null at every k=2..9 (max z {max(zs):+.2f})", max(zs) < 1.0)

print(f"\n  => the interlock chance model is\n"
      f"       E[cores matching all of T] = n_cores * PROD_i min(1, rho_i*W_i / n_cores)\n"
      f"     with rho_i measured LOCALLY (S4) and n_cores the CORE count at the chosen "
      f"strictness level.")

OUT["hits_d10"] = {k: HITS[k] for k in POOL_H}
# per-core, per-target hit counts (L1) for the reach model in interlock_spec_model.py
percore = defaultdict(lambda: defaultdict(int))
for r in recs:
    for k in r[7]:
        percore[r[4]][k] += 1
OUT["percore_L1"] = [{"b_s": c[0], "sk": c[1], "hits": dict(v)} for c, v in percore.items()]
OUT["pool"] = POOL
OUT["pool_h"] = POOL_H
OUT["holdout"] = HOLDOUT
OUT["checks_passed"] = int(sum(CHECKS))
OUT["checks_total"] = len(CHECKS)
(Path(__file__).parent / "interlock_spec_core.json").write_text(json.dumps(OUT, indent=1))
rule(f"CHECKS {sum(CHECKS)}/{len(CHECKS)} PASS")
sys.exit(0 if all(CHECKS) else 1)
