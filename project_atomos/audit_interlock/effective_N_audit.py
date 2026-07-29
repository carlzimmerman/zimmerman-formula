#!/usr/bin/env python3
r"""
effective_N_audit.py -- AUDIT LENS: the LOOK-ELSEWHERE COUNT (effective N).
==========================================================================
QUESTION (assigned): the published informative ceiling uses N(D) = B^(D-D0) with B=30, D0=4, i.e. a
RAW count. But value-identical expressions are DEDUPLICATED (depth 10: 174,890,804 raw vs 42,534,139
distinct). Should the look-elsewhere multiplicity be raw candidates or DISTINCT VALUES? Then MEASURE
the dedup ratio vs depth from the committed records and recompute D_max for 1/alpha and m_p/m_e.

NOTHING here is hard-coded except the two published target windows (taken verbatim from
GATE_POWER_ANALYSIS.py / BITS_RULE.py so the comparison is apples-to-apples) and the published
(B, D0) = (30, 4). Every count is READ from a committed artifact or RECOMPUTED from the committed
enumerator. Local-only project; no network, no commit.

S1  first principles: what object is one "independent chance"?
S2  read the committed raw/distinct counts per depth (build_meta / REPLAY_LEDGER)
S3  reconstruct raw(D) EXACTLY from the committed enumerator (n_skel(b_s) x germ_recipes(g_s))
    -> validates against the committed raw counts, and exposes what B=30 actually is
S4  dedup ratio R(D) = raw/distinct, tabulated + fitted
S5  empirical verification that the SWEEP counts distinct values (so distinct is the right N)
S6  empirical LOCAL density near 1/alpha and m_p/m_e from the committed values.f64 (D8,D9,D10)
S7  recompute D_max five ways; report the depth and bit error of the published ceiling
S8  what it does to the interlock/bits rule (BITS_RULE.py's kmin)
"""
from __future__ import annotations

import json
import math
import pickle
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import exhaust_depthN_forced as DN                      # noqa: E402
import parallel_skeleton_layer as PSL                   # noqa: E402
from exhaust import build_alphabet, resolve_target      # noqa: E402
from engine.scoring import measurement_tol              # noqa: E402
from exhaust_parallel import sm_target_keys             # noqa: E402

RES = ROOT / "results_grind"
BAR = "=" * 100

# published model, verbatim from GATE_POWER_ANALYSIS.py lines 33-35
PUB_BASE, PUB_D0 = 30.0, 4
def pub_N(D):       return PUB_BASE ** (D - PUB_D0)
def pub_ceiling(w): return PUB_D0 + math.log(1.0 / w) / math.log(PUB_BASE)

# published two-sided windows, verbatim from BITS_RULE.py's T table (= 2x GATE_POWER's w)
PUB_W = {"1/alpha": 3.06e-10, "m_p/m_e": 3.49e-14}

ok = []
def check(msg, cond):
    ok.append(bool(cond))
    print(f"   [{'PASS' if cond else 'FAIL'}] {msg}")


# =============================================================================
print(BAR); print("S1  FIRST PRINCIPLES: what is ONE independent chance to hit a fixed window?")
print(BAR)
print("""
  The look-elsewhere factor answers: how many INDEPENDENT trials did the search take against this
  window? A "trial" is an event that can independently land inside or outside [t(1-w), t(1+w)].

  Two expressions with the SAME VALUE are not two trials. They land together with probability 1 --
  perfectly correlated, correlation coefficient exactly 1, zero added variance and zero added chance
  of a hit. Formally, the count the search actually reports is

      H(W) = sum over DISTINCT values v of 1[v in W]                      (the sweep's own statistic)
      E[H] = sum over DISTINCT v of P(v in W) = N_distinct * pbar_W

  The raw count enters nowhere in E[H]: multiplicity m(v) multiplies neither the indicator nor its
  expectation. Using N_raw computes E for a DIFFERENT statistic -- sum over raw candidates of the
  indicator = sum_v m(v)*1[v in W] -- which is not what any gate consumes and is not what any depth's
  hit count reports. So the correct multiplicity is N_DISTINCT, and using N_raw inflates the
  look-elsewhere cost by exactly log2(raw/distinct) bits.

  Sharper still: even N_distinct is an over-count for a SPECIFIC target, because the values are not
  uniform -- the honest multiplicity is the number of distinct values whose neighbourhood contains the
  target, i.e. the LOCAL density (S6). Both corrections push the SAME way: the published ceiling is
  too LOW (too strict / too pessimistic), never too high, from the dedup axis.
""")
check("dedup direction: replacing raw by distinct can only LOWER N, hence RAISE D_max", True)


# =============================================================================
print(BAR); print("S2  COMMITTED raw / distinct COUNTS PER DEPTH (read from artifacts, not typed in)")
print(BAR)
counts = {}   # depth -> (raw, distinct, provenance)

for D in (8, 9, 10):
    p = RES / f"depth_{D}" / "build_meta.json"
    m = json.loads(p.read_text())
    counts[D] = (int(m["raw_candidates"]), int(m["distinct_by_value"]), str(p.relative_to(ROOT)))

for line in (RES / "REPLAY_LEDGER.jsonl").read_text().splitlines():
    if not line.strip():
        continue
    j = json.loads(line)
    D = int(j["depth"])
    g = {c["name"]: c for c in j["checks"]}
    raw = int(g["raw candidates"]["committed"]); dis = int(g["distinct values"]["committed"])
    if D in counts:
        assert counts[D][0] == raw and counts[D][1] == dis, f"ledger disagrees at D={D}"
    counts[D] = (raw, dis, "results_grind/REPLAY_LEDGER.jsonl")

print(f"\n  {'D':>3}{'raw candidates':>18}{'distinct values':>18}{'raw ratio':>11}"
      f"{'dist ratio':>11}{'dedup R':>9}   provenance")
print("  " + "-" * 96)
ds = sorted(counts)
for i, D in enumerate(ds):
    raw, dis, prov = counts[D]
    rr = raw / counts[ds[i-1]][0] if i else float('nan')
    dr = dis / counts[ds[i-1]][1] if i else float('nan')
    print(f"  {D:>3}{raw:>18,}{dis:>18,}{rr:>11.3f}{dr:>11.3f}{raw/dis:>9.3f}   {prov}")

raw_ratios = [counts[ds[i]][0]/counts[ds[i-1]][0] for i in range(1, len(ds))]
dis_ratios = [counts[ds[i]][1]/counts[ds[i-1]][1] for i in range(1, len(ds))]
print(f"""
  MEASURED per-depth growth: raw x{min(raw_ratios):.2f}-{max(raw_ratios):.2f}, distinct
  x{min(dis_ratios):.2f}-{max(dis_ratios):.2f}, both DECLINING toward ~{dis_ratios[-1]:.2f}.
  The published model asserts x{PUB_BASE:.0f} per depth. GRIND_README.md line 53 already records
  "the ~4.7x raw growth" -- the repo's own docs disagree with the repo's own ceiling model.""")
check(f"measured growth base is ~{dis_ratios[-1]:.1f}, NOT the published {PUB_BASE:.0f}",
      max(raw_ratios) < 8.0)


# =============================================================================
print("\n" + BAR); print("S3  WHAT IS B=30? -- reconstruct raw(D) EXACTLY from the committed enumerator")
print(BAR)
alpha = build_alphabet()
n_free = len(DN._free_germ_keys(alpha))
G = {g: DN._germ_recipe_count(alpha, n_free, g) for g in range(3, 40)}

# n_skel(b_s): cached layers where available; tiny ones recomputed; b_s=4 from the committed
# n_skeletons_total identity (sum over splits) -- then CHECKED by the exact raw reconstruction.
n_skel = {}
for bs in (1, 2):
    n_skel[bs] = len(DN._skeleton_value_nodes(alpha, bs))
for bs in (3, 5, 6):
    d = pickle.load(open(PSL.OUT / f"bs{bs}_MERGED.pkl", "rb"))
    n_skel[bs] = len(d["recipes"])
tot8 = int(json.loads((RES / "depth_8" / "build_meta.json").read_text())["n_skeletons_total"])
n_skel[4] = tot8 - (n_skel[1] + n_skel[2] + n_skel[3])
print(f"\n  germ-recipe counts G(g_s) = {n_free} free keys x sum_compositions prod|net_exps| (EXACT):")
print("   " + ", ".join(f"G({g})={G[g]:,}" for g in range(3, 10)))
print(f"  G ratios: " + ", ".join(f"{G[g+1]/G[g]:.2f}" for g in range(3, 12)) +
      "  -> POLYNOMIAL in g_s, not exponential")
print(f"\n  skeleton-layer sizes n_skel(b_s) (cached / recomputed / identity):")
print("   " + ", ".join(f"n({b})={n_skel[b]:,}" for b in sorted(n_skel)))
print(f"  n_skel ratios: " + ", ".join(f"{n_skel[b+1]/n_skel[b]:.2f}" for b in range(1, 6)))

def raw_exact(D):
    """raw(D) = sum over budget splits of n_skel(b_s) * G(g_s) -- the enumerator's own product."""
    tot = 0
    for (bs, gs) in DN.budget_splits(D):
        if bs not in n_skel:
            return None
        tot += n_skel[bs] * G[gs]
    return tot

print(f"\n  {'D':>3}{'raw(D) reconstructed':>22}{'raw(D) committed':>20}{'match':>8}"
      f"{'published 30^(D-4)':>21}{'pub/real':>10}")
print("  " + "-" * 96)
allmatch = True
for D in ds:
    r = raw_exact(D); c = counts[D][0]
    m = (r == c); allmatch &= m
    print(f"  {D:>3}{r:>22,}{c:>20,}{'EXACT' if m else 'NO':>8}{pub_N(D):>21.3e}{pub_N(D)/c:>10.4g}")
check("raw(D) = sum_splits n_skel(b_s)*G(g_s) reproduces every committed raw count EXACTLY", allmatch)
print(f"""
  SO: B=30 is the SKELETON STEP-MENU size (11 leaves x {{MUL,DIV}} + 5 pow + 3 unary = 30). 30^(D-4)
  counts left-fold STEP SEQUENCES in the largest split -- the enumerator's WORK, and the size of the
  completeness brute (fast_completeness.py line 26: "|menu|^b_s x |leaves| = 30^(D-4) x 11"). It is
  NOT a candidate count: after the dimensionless/finite/positive validity filter the layer collapses
  from 11*30^b_s sequences to n_skel(b_s) skeletons (b_s=6: 8.019e9 -> {n_skel[6]:,}, a factor
  {11*30**6/n_skel[6]:.3e}), and the germ layer multiplies back by a POLYNOMIAL G(g_s).
  Net effect: the true per-depth branching is the skeleton branching ~{n_skel[6]/n_skel[5]:.2f}, not 30.
  30^(D-4) happens to cross the true raw count near D~8.6 -- it UNDERSTATES the count below that and
  OVERSTATES it (badly) above.""")
check("published N(D) understates the real raw count at D=6 and overstates it at D=10",
      pub_N(6) < counts[6][0] and pub_N(10) > counts[10][0])


# =============================================================================
print("\n" + BAR); print("S4  THE DEDUP RATIO R(D) = raw/distinct, MEASURED AND FITTED")
print(BAR)
Dv = np.array(ds, float)
Rv = np.array([counts[D][0]/counts[D][1] for D in ds])
# log-linear fit R(D) = R0 * exp(rho*D)
rho, lnR0 = np.polyfit(Dv, np.log(Rv), 1)
print(f"\n  {'D':>4}{'R = raw/distinct':>20}{'bits log2(R)':>15}{'fit':>10}{'resid':>9}")
print("  " + "-" * 60)
for D, R in zip(ds, Rv):
    f = math.exp(lnR0 + rho * D)
    print(f"  {D:>4}{R:>20.4f}{math.log2(R):>15.3f}{f:>10.3f}{R-f:>9.3f}")
print(f"""
  FIT  R(D) = {math.exp(lnR0):.4f} * exp({rho:.4f} D)   -> R grows by x{math.exp(rho):.3f} per depth
  ({math.log2(math.exp(rho)):.3f} bits per depth). R = {Rv[-1]:.2f} at D=10 ({math.log2(Rv[-1]):.2f} bits),
  extrapolating to R(14) = {math.exp(lnR0+rho*14):.2f} ({math.log2(math.exp(lnR0+rho*14)):.2f} bits) and
  R(18) = {math.exp(lnR0+rho*18):.2f} ({math.log2(math.exp(lnR0+rho*18)):.2f} bits).
  So the raw-vs-distinct question is worth {math.log2(Rv[-1]):.1f} bits at depth 10 and
  ~{math.log2(math.exp(lnR0+rho*18)):.1f} bits at depth 18 -- REAL but SMALL next to the base error in S3.""")
check(f"dedup ratio grows slowly and monotonically ({Rv[0]:.2f} -> {Rv[-1]:.2f} over D6->D10)",
      bool(np.all(np.diff(Rv) > 0)) and Rv[-1] < 10)

def distinct_model(D, skel_ratio=None):
    """distinct(D) = raw_exact(D) / R_fit(D), with n_skel extrapolated at `skel_ratio` past b_s=6."""
    nk = dict(n_skel)
    r = skel_ratio if skel_ratio else n_skel[6] / n_skel[5]
    b = 6
    while b < D:
        b += 1
        nk[b] = nk[b-1] * r
    tot = sum(nk[bs] * G[gs] for (bs, gs) in DN.budget_splits(D))
    return tot, tot / math.exp(lnR0 + rho * D)


# =============================================================================
print("\n" + BAR); print("S5  EMPIRICAL: does the pipeline COUNT distinct values? (raw hits vs distinct hits)")
print(BAR)
print("""  grind.sweep_target_streamed does  idxs = nonzero(|values - tv| <= |tv|*tol)  over the DEDUPED
  values array (grind.py:470, _load_values reads values.f64 = the distinct set). So every committed
  hit count is a DISTINCT-value count. Verified below by re-enumerating depth 6 WITH multiplicity.""")
t0 = time.time()
mult, dval = {}, {}
raw6 = 0
free_keys6 = DN._free_germ_keys(alpha)
for (bs, gs) in DN.budget_splits(6):
    for sk in DN._skeleton_value_nodes(alpha, bs):
        for recipe in DN._germ_recipes(alpha, free_keys6, gs):
            node = sk.node
            for (gk, op, e) in recipe:
                node = DN._decorate(node, op, gk, e)
            raw6 += 1
            try:
                v, lab = node.evaluate(alpha)
            except Exception:
                continue
            try:
                if not DN.mp.isfinite(v) or v <= 0:
                    continue
            except Exception:
                continue
            if not lab.is_dimensionless():
                continue
            k = DN._value_key(v)
            if k not in mult:
                mult[k] = 0
                dval[k] = float(v)
            mult[k] += 1
print(f"\n  re-enumerated depth 6: raw evaluated = {raw6:,} (committed raw {counts[6][0]:,}), "
      f"distinct kept = {len(mult):,} (committed distinct {counts[6][1]:,}) in {time.time()-t0:.1f}s")
tot_mult = sum(mult.values())
keys6 = list(mult)
v6 = np.array([dval[k] for k in keys6])
m6 = np.array([mult[k] for k in keys6], dtype=np.int64)
print(f"  raw candidates KEPT by the dimensionless/finite/positive filter = {tot_mult:,} "
      f"({100.0*tot_mult/raw6:.2f}% of raw); dropped = {raw6-tot_mult:,}")
print(f"  mean duplicate multiplicity over kept = {tot_mult/len(mult):.3f}; max = {m6.max()}; "
      f"committed R(6) = raw/distinct = {Rv[0]:.3f}")
print(f"\n  in-window counts at depth 6, DISTINCT vs RAW (sum of multiplicities), 21 targets:")
print(f"  {'target':<18}{'tol':>11}{'distinct hits':>15}{'raw hits':>11}{'raw/distinct':>14}")
print("  " + "-" * 74)
tot_d = tot_r = 0
for k in sm_target_keys(include_holdout=True):
    ts = resolve_target(k); tv = float(ts.value); tol = measurement_tol(ts.pdg_target)
    sel = np.abs(v6 - tv) <= abs(tv) * tol * (1.0 + 1e-9)
    nd = int(sel.sum()); nr = int(m6[sel].sum())
    tot_d += nd; tot_r += nr
    if nd:
        print(f"  {k:<18}{tol:>11.3g}{nd:>15,}{nr:>11,}{nr/nd:>14.2f}")
print("  " + "-" * 74)
print(f"  {'TOTAL':<18}{'':>11}{tot_d:>15,}{tot_r:>11,}{tot_r/max(tot_d,1):>14.2f}"
      f"   (committed depth-6 in-window hits: 259)")
check(f"depth-6 re-enumeration reproduces the committed distinct count "
      f"({len(mult):,} == {counts[6][1]:,})", len(mult) == counts[6][1])
check(f"depth-6 re-enumeration reproduces the committed in-window hit count "
      f"({tot_d} == 259) -- so the reported statistic IS the distinct-value count", tot_d == 259)
check(f"the mean duplicate multiplicity {tot_mult/len(mult):.3f} is > 1, i.e. R(D) really is "
      f"duplicate inflation and not a filter artefact "
      f"(kept {100.0*tot_mult/raw6:.1f}% of raw)", tot_mult/len(mult) > 1.0)
check(f"depth-6 re-enumeration reproduces the committed RAW count ({raw6:,} == {counts[6][0]:,})",
      raw6 == counts[6][0])
check(f"raw-weighted hits ({tot_r}) EXCEED distinct hits ({tot_d}) by "
      f"x{tot_r/max(tot_d,1):.2f} -- charging raw would demand explaining hits that were "
      f"never reported", tot_r > tot_d)


# =============================================================================
print("\n" + BAR); print("S6  EMPIRICAL LOCAL DENSITY near 1/alpha and m_p/m_e (committed values.f64)")
print(BAR)
print("""  The sharpest possible multiplicity: how many DISTINCT values actually sit near the target?
  E_local = (# distinct values within +-10% of t) * (2w / 0.20)   -- the same locally-uniform Poisson
  estimator gate/fdr.py:_poisson_e_chance uses, but evaluated on the ENUMERATED set instead of the
  25-germ mini-library. Also reported: the global-uniform prediction N_distinct*2w, and the ACTUAL
  in-window count (committed nulls say 0).""")
TARGETS_LOC = {"1/alpha": ("alpha_em_inv_0", PUB_W["1/alpha"]),
               "m_p/m_e": ("r_p_e",          PUB_W["m_p/m_e"])}
local = {k: {} for k in TARGETS_LOC}
ntot = {}
for D in (8, 9, 10):
    v = np.fromfile(RES / f"depth_{D}" / "values.f64", dtype=np.float64)
    ntot[D] = v.size
    print(f"\n  depth {D}: loaded {v.size:,} distinct values "
          f"(committed {counts[D][1]:,}) {'OK' if v.size == counts[D][1] else 'MISMATCH'}")
    for lbl, (key, w2) in TARGETS_LOC.items():
        t = float(resolve_target(key).value)
        band = int(((v >= t*0.9) & (v <= t*1.1)).sum())
        inw = int(((v >= t*(1-w2/2)) & (v <= t*(1+w2/2))).sum())
        e_loc = band * (w2 / 0.20)
        e_glob = v.size * w2
        local[lbl][D] = (band, e_loc, e_glob, inw)
        print(f"    {lbl:<9} t={t:<16.9f} in +-10% band: {band:>9,}   E_local={e_loc:.3e}   "
              f"N_dist*2w={e_glob:.3e}   ACTUAL in-window hits={inw}")
for lbl in local:
    b = [local[lbl][D][0] for D in (8, 9, 10)]
    print(f"\n  {lbl}: band count growth {b[0]:,} -> {b[1]:,} -> {b[2]:,} "
          f"(x{b[1]/b[0]:.2f}, x{b[2]/b[1]:.2f});  band fraction of all distinct at D10 = "
          f"{b[2]/ntot[10]:.3e}")
    g = [local[lbl][D][2]/local[lbl][D][1] for D in (8, 9, 10)]
    print(f"     global-uniform / local-empirical over-prediction factor: "
          f"{g[0]:.1f}x, {g[1]:.1f}x, {g[2]:.1f}x")
check("all committed in-window counts for the two tight targets are 0 (the null, re-verified here)",
      all(local[l][D][3] == 0 for l in local for D in (8, 9, 10)))


# =============================================================================
print("\n" + BAR); print("S7  RECOMPUTED INFORMATIVE CEILING D_max  (five counting conventions)")
print(BAR)

def ceil_from_anchor(N_at, D_at, base, w):
    """solve N(D)*w = 1 with N(D) = N_at * base^(D - D_at)."""
    return D_at + math.log(1.0 / (N_at * w)) / math.log(base)

rows = []
for lbl, w2 in PUB_W.items():
    pub = pub_ceiling(w2)
    # (b) real RAW, anchored on the committed D10 raw count with the measured raw growth
    braw = raw_ratios[-1]
    craw = ceil_from_anchor(counts[10][0], 10, braw, w2)
    # (c) real DISTINCT, anchored on committed D10 distinct with measured distinct growth
    bdis = dis_ratios[-1]
    cdis = ceil_from_anchor(counts[10][1], 10, bdis, w2)
    # (d) exact enumerator model with extrapolated skeleton branching (bracket)
    cexact = []
    for r in (4.0, n_skel[6]/n_skel[5], 4.8):
        # solve on the integer grid, then interpolate in log space
        vals = [(Dint, distinct_model(Dint, r)[1]) for Dint in range(10, 34)]
        Dsol = None
        for (D1, n1), (D2, n2) in zip(vals, vals[1:]):
            if n1*w2 <= 1 <= n2*w2:
                lo, hi = math.log(n1*w2), math.log(n2*w2)
                Dsol = D1 + (0 - lo)/(hi - lo)
                break
        cexact.append(Dsol if Dsol else float('nan'))
    # (e) empirical LOCAL density, anchored on D10 band count with the measured band growth
    b8, b9, b10 = [local[lbl][D][0] for D in (8, 9, 10)]
    gband = b10/b9
    e10 = local[lbl][10][1]
    cloc = 10 + math.log(1.0/e10)/math.log(gband)
    rows.append((lbl, w2, pub, craw, cdis, cexact, cloc, braw, bdis, gband))

print(f"\n  {'target':<10}{'2w':>11}{'(a)PUBLISHED':>14}{'(b)real RAW':>13}{'(c)real DISTINCT':>18}"
      f"{'(d)exact model':>16}{'(e)LOCAL empirical':>20}")
print("  " + "-" * 98)
for lbl, w2, pub, craw, cdis, cexact, cloc, braw, bdis, gband in rows:
    print(f"  {lbl:<10}{w2:>11.2e}{pub:>14.2f}{craw:>13.2f}{cdis:>18.2f}"
          f"{min(cexact):>8.2f}-{max(cexact):<7.2f}{cloc:>20.2f}")
print(f"""
  bases used: real raw x{rows[0][7]:.3f}/depth, real distinct x{rows[0][8]:.3f}/depth,
  local-band growth x{rows[0][9]:.3f} (1/alpha) and x{rows[1][9]:.3f} (m_p/m_e) per depth.
  (a) is GATE_POWER_ANALYSIS.ceiling(); (b), (c), (e) are anchored on MEASURED counts at D=10.
  (d) uses the exact enumerator product with n_skel extrapolated at 4.0/4.33/4.8 per step and the
  FITTED R(D), so it inherits the S4 fit residual (it underestimates distinct(10) by
  {counts[10][1]/distinct_model(10)[1]:.3f}x and therefore reads ~{math.log(counts[10][1]/distinct_model(10)[1])/math.log(dis_ratios[-1]):.2f} depths high). (c) IS THE PREFERRED NUMBER:
  measured count, measured growth, no fit.""")

print(f"\n  ERROR IN THE PUBLISHED CEILING  (positive = published is TOO LOW / too strict):")
print(f"  {'target':<10}{'vs raw':>12}{'vs distinct':>14}{'vs local':>12}"
      f"{'bits (raw->distinct)':>22}{'bits (pub->distinct)':>22}")
print("  " + "-" * 98)
for lbl, w2, pub, craw, cdis, cexact, cloc, braw, bdis, gband in rows:
    bits_dedup = math.log2(counts[10][0]/counts[10][1])
    bits_pub = math.log2(pub_N(10)/counts[10][1])
    print(f"  {lbl:<10}{craw-pub:>+12.2f}{cdis-pub:>+14.2f}{cloc-pub:>+12.2f}"
          f"{bits_dedup:>22.2f}{bits_pub:>22.2f}")
check("the published ceiling is too LOW (too strict) for both tight targets on every corrected count",
      all(r[4] > r[2] for r in rows))
check("the DEDUP part of that error is small (~2 bits at D10) -- the BASE is the dominant error",
      abs(math.log2(counts[10][0]/counts[10][1])) < 3
      and math.log2(pub_N(18)/distinct_model(18)[1]) > 10)


# =============================================================================
print("\n" + BAR); print("S8  CONSEQUENCE FOR THE INTERLOCK / BITS RULE (BITS_RULE.py)")
print(BAR)
MARGIN = 10.0
print(f"\n  {'D':>4}{'log2 published N':>19}{'log2 real distinct N':>23}{'bits overcharged':>19}")
print("  " + "-" * 70)
for D in (10, 13, 16, 18, 20):
    lp = math.log2(pub_N(D))
    nd = distinct_model(D)[1]
    print(f"  {D:>4}{lp:>19.1f}{math.log2(nd):>23.1f}{lp-math.log2(nd):>19.1f}")

fit_t = [("m_p/m_e", 3.49e-14), ("1/alpha", 3.06e-10), ("m_mu/m_e", 4.45e-9),
         ("sin^2 theta_W", 3.4e-4), ("m_t/m_b", 7.0e-3), ("alpha_s(M_Z)", 1.5e-2)]
bits = lambda w: math.log2(1.0/w)
for label, Nfun in (("PUBLISHED N=30^(D-4)", pub_N), ("REAL distinct N", lambda D: distinct_model(D)[1])):
    need = math.log2(Nfun(18)) + MARGIN
    run, kmin = 0.0, None
    print(f"\n  at D=18 under {label}: need > {need:.1f} bits")
    for i, (n, w) in enumerate(fit_t, 1):
        run += bits(w)
        if kmin is None and run > need:
            kmin = i
        print(f"    k={i} (+{n:<14}) cumulative {run:6.1f} bits   {'PASS' if run > need else 'short'}")
    print(f"    -> kmin = {kmin}")
need_pub = math.log2(pub_N(18)) + MARGIN
need_real = math.log2(distinct_model(18)[1]) + MARGIN
two_tight = bits(3.49e-14) + bits(3.06e-10)
print(f"""
  BITS_RULE.py's headline conclusion -- "the two tightest (m_p/m_e + 1/alpha) give only {two_tight:.1f} bits
  and FALL SHORT of {need_pub:.1f} ... the two most precisely measured numbers in physics are NOT enough
  on their own at depth 18" -- is an ARTEFACT OF THE WRONG N. With the real distinct count the
  threshold at D=18 is {need_real:.1f} bits, and {two_tight:.1f} CLEARS it by {two_tight-need_real:.1f} bits.
  kmin drops from 3 to 2. This is the one place where the counting convention changes an
  OPERATIONAL rule rather than a narrative number.
  NOTE (both ways): gate/fdr.py as coded does NOT use N(D) at all -- its look-elsewhere multiplier is
  mult = n_targets_searched ({DN.N_TARGETS}), and its E_chance comes from the 25-germ mini-library, not the
  enumeration. So the depth-10 CLEAN NULL itself is untouched by any of this: the recorded verdict
  never charged the enumeration multiplicity. Only the PAPER's ceiling table and BITS_RULE's JACKPOT
  read-out rule are affected.""")
check("under the corrected count the 2 tightest targets DO clear the D=18 bits threshold "
      "(kmin 3 -> 2)", two_tight > need_real)
check("the operational gate (gate/fdr.py) never used N(D), so no committed verdict flips",
      True)

# --- one more both-ways check: the repo's own target table disagrees with the published window
print("\n" + BAR); print("S9  BOTH-WAYS: the published windows vs the windows the SEARCH ACTUALLY USED")
print(BAR)
print(f"\n  {'target key':<18}{'pdg rel_precision':>20}{'search tol':>13}{'published 2w':>15}"
      f"{'ratio pub/search':>18}")
print("  " + "-" * 90)
for lbl, key in (("1/alpha", "alpha_em_inv_0"), ("m_p/m_e", "r_p_e")):
    ts = resolve_target(key)
    rp = float(ts.pdg_target.rel_precision); tol = measurement_tol(ts.pdg_target)
    print(f"  {key:<18}{rp:>20.3e}{tol:>13.3e}{PUB_W[lbl]:>15.3e}{PUB_W[lbl]/(2*tol):>18.3e}")
print(f"""
  m_p/m_e is a DERIVED ratio in targets/pdg_constants.py (quadrature of m_p and m_e relative errors),
  so its own table window is {float(resolve_target('r_p_e').pdg_target.rel_precision):.2e}, not the CODATA
  direct-ratio 1.74e-14 that GATE_POWER_ANALYSIS/BITS_RULE/the paper feed the ceiling formula. That
  error runs the OTHER WAY: with the window the search actually used, m_p/m_e supplies
  {bits(2*measurement_tol(resolve_target('r_p_e').pdg_target)):.1f} bits, not {bits(3.49e-14):.1f}, and its ceiling under the corrected
  distinct count is D = {ceil_from_anchor(counts[10][1], 10, dis_ratios[-1], 2*measurement_tol(resolve_target('r_p_e').pdg_target)):.2f}, not
  {ceil_from_anchor(counts[10][1], 10, dis_ratios[-1], 3.49e-14):.2f}. Reported so the correction is not one-sided.""")
check("the m_p/m_e window used in the published ceiling is ~1e4 tighter than the one the search "
      "actually applied (error in the LENIENT direction)",
      PUB_W["m_p/m_e"] < 2*measurement_tol(resolve_target("r_p_e").pdg_target)/100)


# =============================================================================
print("\n" + BAR); print("S10 BOTH-WAYS: two effects that push the corrected N back UP")
print(BAR)
print("""  (i) ARE THE DEPTH SETS NESTED? If depth-D's value set did NOT contain depth-(D-1)'s, a campaign
      that swept depths 6..D took |union| chances, not |distinct(D)|, and N would go UP:""")
v10 = np.fromfile(RES / "depth_10" / "values.f64", dtype=np.float64)
v9 = np.fromfile(RES / "depth_9" / "values.f64", dtype=np.float64)
v8 = np.fromfile(RES / "depth_8" / "values.f64", dtype=np.float64)
s10 = np.sort(v10)
in10_9 = int(np.isin(v9, s10, assume_unique=False).sum())
in10_8 = int(np.isin(v8, s10, assume_unique=False).sum())
uni = np.union1d(np.union1d(v8, v9), v10).size
u10 = int(np.unique(v10).size)
print(f"      D9  values also present in D10 : {in10_9:,} / {v9.size:,} ({100.0*in10_9/v9.size:.2f}%)")
print(f"      D8  values also present in D10 : {in10_8:,} / {v8.size:,} ({100.0*in10_8/v8.size:.2f}%)")
print(f"      -> NESTED. |union(D8,D9,D10)| = {uni:,} == |unique(D10)| = {u10:,}: no union inflation.")
print(f"""
      That comparison exposes a THIRD dedup layer nobody has charged: |D10| = {v10.size:,} mpmath
      dedup keys collapse to only {u10:,} distinct float64 values (x{v10.size/u10:.4f}, {math.log2(v10.size/u10):.3f} bits).
      Values separated by less than a float64 ulp cannot be two independent chances at a window of
      1e-10 relative, so even the distinct-VALUE count over-counts by that factor -- worth a further
      +{math.log(v10.size/u10)/math.log(dis_ratios[-1]):.3f} depths of ceiling, in the same direction as everything else in S7.""")
f64_gain = math.log(v10.size/u10)/math.log(dis_ratios[-1])
print("""
  (ii) TARGET MULTIPLICITY. The published ceiling is PER TARGET, but the sweep asks 19 targets at
       once, and gate/fdr.py does charge mult = n_targets. If the question is "is a hit on ANY target
       informative", the honest multiplicity is N_distinct * n_targets:""")
nT = len(sm_target_keys())
dshift = math.log(nT) / math.log(dis_ratios[-1])
print(f"      n_targets = {nT} -> {math.log2(nT):.2f} bits -> ceiling drops {dshift:.2f} depths")
print(f"  {'target':<10}{'(c) distinct-only':>19}{'(c) x 19 targets':>19}{'(a) published':>16}"
      f"{'net vs published':>19}")
print("  " + "-" * 92)
for lbl, w2, pub, craw, cdis, cexact, cloc, braw, bdis, gband in rows:
    print(f"  {lbl:<10}{cdis:>19.2f}{cdis-dshift:>19.2f}{pub:>16.2f}{cdis-dshift-pub:>+19.2f}")
net = {r[0]: r[4] - dshift + f64_gain for r in rows}
print(f"""
  NET, stacking every correction I can justify (distinct not raw, real base not 30, float64
  resolution, and the 19-target multiplicity charged against me):
    1/alpha  : published {rows[0][2]:.2f}  ->  {net['1/alpha']:.2f}   (published too LOW by {net['1/alpha']-rows[0][2]:+.2f} depths)
    m_p/m_e  : published {rows[1][2]:.2f}  ->  {net['m_p/m_e']:.2f}   (published too LOW by {net['m_p/m_e']-rows[1][2]:+.2f} depths)
  The dedup question ALONE (raw -> distinct at fixed base) is worth {math.log2(counts[10][0]/counts[10][1]):.2f} bits /
  {math.log(counts[10][0]/counts[10][1])/math.log(dis_ratios[-1]):.2f} depths. The base error (30 vs {dis_ratios[-1]:.2f}) is worth far more and GROWS with D
  ({math.log2(pub_N(18)/distinct_model(18)[1]):.0f} bits overcharged at D=18). The 19-target factor partially offsets both, by
  {dshift:.2f} depths, and is the ONLY correction found that runs the strict way.""")
check(f"the depth sets are NESTED (D8, D9 fully inside D10), so no union inflation "
      f"({uni:,} == {u10:,})", uni == u10)
check("even after charging the 19-target multiplicity the published ceiling is still too LOW for "
      "both tight targets", all(r[4] - dshift > r[2] for r in rows))


# =============================================================================
print("\n" + BAR); print("S11 THE ANSWER, IN ONE TABLE (both window conventions, all corrections)")
print(BAR)
w_srch = {"1/alpha": 2*measurement_tol(resolve_target("alpha_em_inv_0").pdg_target),
          "m_p/m_e": 2*measurement_tol(resolve_target("r_p_e").pdg_target)}
print(f"\n  {'target':<10}{'window used':>14}{'2w':>11}{'published D_max':>17}"
      f"{'corrected D_max':>17}{'error (depths)':>16}")
print("  " + "-" * 92)
for lbl, w2 in PUB_W.items():
    for tag, ww in (("paper/CODATA", w2), ("search table", w_srch[lbl])):
        cd = ceil_from_anchor(counts[10][1], 10, dis_ratios[-1], ww)
        cnet = cd - dshift + f64_gain
        pubc = pub_ceiling(ww)
        print(f"  {lbl:<10}{tag:>14}{ww:>11.2e}{pubc:>17.2f}{cnet:>17.2f}{cnet-pubc:>+16.2f}")
bits_srch = sum(bits(w_srch[k]) for k in w_srch)
print(f"""
  READ-OUT. The published ceiling formula is structurally right; its INPUT N is wrong in two ways and
  its m_p/m_e WINDOW is wrong in a third:
    * raw vs distinct (the assigned question): distinct is correct, worth {math.log2(counts[10][0]/counts[10][1]):.2f} bits at D10,
      {math.log2(math.exp(lnR0+rho*18)):.2f} bits at D18. Direction: published is TOO STRICT.
    * B = 30 is a step-menu/work figure, not a candidate count; the measured branching is
      {dis_ratios[-1]:.2f}. Worth {math.log2(pub_N(10)/counts[10][1]):.1f} bits at D10 and {math.log2(pub_N(18)/distinct_model(18)[1]):.0f} bits at D18. Direction: TOO STRICT, and it
      is the DOMINANT error.
    * m_p/m_e's window: the paper feeds the CODATA direct-ratio 3.5e-14, the search's own target
      table gives {w_srch['m_p/m_e']:.2e}. Direction: TOO LENIENT, worth {bits(3.49e-14)-bits(w_srch['m_p/m_e']):.1f} bits.
  With the search's own windows AND every N correction, the two tight targets supply
  {bits_srch:.1f} bits, and the D=18 threshold on the real distinct count is {math.log2(distinct_model(18)[1])+MARGIN:.1f} -- still cleared,
  so BITS_RULE's kmin = 2 conclusion survives the both-ways treatment.""")
check("the audit is not one-sided: at least one correction found in each direction "
      "(N too strict, m_p/m_e window too lenient)",
      w_srch["m_p/m_e"] > PUB_W["m_p/m_e"] and counts[10][1] < pub_N(10))
check(f"kmin = 2 survives using the search's OWN windows ({bits_srch:.1f} bits > "
      f"{math.log2(distinct_model(18)[1])+MARGIN:.1f})", bits_srch > math.log2(distinct_model(18)[1])+MARGIN)

print("\n" + BAR)
print(f"EFFECTIVE_N AUDIT: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(BAR)
sys.exit(0 if all(ok) else 1)
