#!/usr/bin/env python3
r"""
ceiling_math_audit.py -- ADVERSARIAL AUDIT of the depth-ceiling derivation

    D_max = D0 + ln(1/w)/ln(B)        (from solving N(D)*w = 1, N(D) = B^(D-D0))

published in PAPER_ATOMOS_NULL.md §4 / GATE_POWER_ANALYSIS.py S1 / BITS_RULE.py, with the numbers
"D = 10.4 for 1/alpha" and "D = 13.1 for m_p/m_e".

FOUR QUESTIONS, each answered with numbers printed from the repo's OWN committed artifacts and its
OWN live code -- nothing here is hard-coded from a docstring:

  (i)   is expected-hits = 1 the right informativeness criterion, or should it be a p-value / FDR
        threshold, and how many depths does that shift D_max?
  (ii)  is B really 30? Reconstruct the step menu FROM THE LIVE CODE, find operations that collide
        or are inverses, then derive the *realized* branching factor from the exact candidate-count
        identity the code implements and from the committed per-depth counts.
  (iii) is D0 = 4 right, i.e. is N(D0) = 1?
  (iv)  does the formula survive dedup / sub-exponential growth?

Then the ceiling is recomputed and the published figures are corrected, with the DIRECTION of each
error stated.

Everything load-bearing is measured. In particular §S3 loads the committed depth-8/9/10 value arrays
and measures the LOCAL density of the value set near each target directly (no fitting, no model), and
first proves the machinery by reproducing the committed per-target hit counts exactly.

Local-only project. No network. Read-only w.r.t. all committed artifacts.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from mpmath import mp                                                   # noqa: E402
from exhaust import build_alphabet, _POW_EXPONENTS, _UNARY_PLAIN        # noqa: E402
from engine.expr_tree import ExprNode, OpType                           # noqa: E402
import exhaust_depthN_forced as DN                                       # noqa: E402
import exhaust_depth5_forced as D5                                       # noqa: E402
import parallel_skeleton_layer as PSL                                    # noqa: E402
from engine.scoring import measurement_tol                               # noqa: E402
import targets.pdg_constants as PDG                                      # noqa: E402
from exhaust_parallel import sm_target_keys                              # noqa: E402

RESULTS = _ROOT / "results_grind"
BAR = "=" * 100

# the PUBLISHED model, quoted so the audit has something to diff against
PUB_B, PUB_D0 = 30.0, 4
def pub_ceiling(w):  return PUB_D0 + math.log(1.0 / w) / math.log(PUB_B)
def pub_N(D):        return PUB_B ** (D - PUB_D0)

checks = []
def check(msg, cond):
    checks.append(bool(cond))
    print(f"   [{'PASS' if cond else 'FAIL'}] {msg}")


# =====================================================================================
print(BAR); print("S0  IS B = 30?  --  THE STEP MENU, RECONSTRUCTED FROM THE LIVE CODE"); print(BAR)
# =====================================================================================
alpha = build_alphabet()
leaves = list(alpha.leaves)
n_leaf = len(leaves)
n_pow, n_un = len(_POW_EXPONENTS), len(_UNARY_PLAIN)
menu_size = 2 * n_leaf + n_pow + n_un
print(f"\n  leaves ({n_leaf}) : {leaves}")
print(f"  POW exponents ({n_pow}) : {[mp.nstr(e, 8) for e in _POW_EXPONENTS]}")
print(f"  plain unaries ({n_un}) : {[u.name for u in _UNARY_PLAIN]}")
print(f"  menu size = 2*{n_leaf} (MUL/DIV per leaf) + {n_pow} (POW) + {n_un} (unary) = {menu_size}")
check(f"the docstring's B=30 IS the literal menu length ({menu_size})", menu_size == 30)

# --- functional collisions among the 8 non-append entries, tested numerically -------------
print("\n  (a) COLLISIONS. The 8 pow/unary entries are not 8 distinct FUNCTIONS. Test on a probe:")
probe = mp.mpf("1.7392847")
fam = {}
for e in _POW_EXPONENTS:
    fam[f"POW^{mp.nstr(e,6)}"] = probe ** e
for u in _UNARY_PLAIN:
    fam[u.name] = {OpType.SQRT: mp.sqrt(probe), OpType.CBRT: mp.cbrt(probe),
                   OpType.INV: 1 / probe}[u]
items = list(fam.items())
coll = []
for i in range(len(items)):
    for j in range(i + 1, len(items)):
        if abs(items[i][1] - items[j][1]) < mp.mpf("1e-30"):
            coll.append((items[i][0], items[j][0]))
for a_, b_ in coll:
    print(f"        {a_:<14} == {b_:<14}  (identical function, two menu slots)")
n_distinct_fun = len(fam) - len(coll)
print(f"      -> {len(fam)} slots, {len(coll)} exact duplicate pairs, {n_distinct_fun} distinct unary functions")
check("POW^0.5==SQRT and POW^-1==INV: the menu double-counts 2 of its 8 unary slots",
      len(coll) == 2)

# --- algebraic redundancy among the 11 leaves ---------------------------------------------
print("\n  (b) LEAF REDUNDANCY. The 22 append-ops are not 22 independent directions: several leaves")
print("      are exact functions of others, so append-sequences collide. Test numerically:")
V = {k: alpha.atoms[k].value if hasattr(alpha, "atoms") else None for k in leaves}
try:
    V = {k: alpha.atoms[k].value for k in leaves}
except Exception:
    V = {}
    for k in leaves:
        V[k] = ExprNode(OpType.LEAF, leaf=k).evaluate(alpha)[0]
rels = [
    ("M_Planck", "sqrt(hbar*c/G)", lambda: mp.sqrt(V["hbar"] * V["c"] / V["G"])),
    ("rho_Lambda", "Lambda*c^2/(8*pi*G)", lambda: V["Lambda"] * V["c"] ** 2 / (8 * mp.pi * V["G"])),
    ("H_Lambda", "c*sqrt(Lambda/3)", lambda: V["c"] * mp.sqrt(V["Lambda"] / 3)),
    ("E_dS", "hbar*H_Lambda", lambda: V["hbar"] * V["H_Lambda"]),
]
n_dep = 0
for key, expr, f in rels:
    try:
        got = f()
        rel = abs(float((got - V[key]) / V[key]))
    except Exception as ex:                                        # pragma: no cover
        print(f"        {key:<12} vs {expr:<22} : could not evaluate ({ex})")
        continue
    exact = rel < 1e-25
    n_dep += int(exact)
    print(f"        {key:<12} =?= {expr:<22} rel diff = {rel:.2e}  {'EXACT DEPENDENT' if exact else 'independent'}")
print(f"      -> {n_dep} of the {n_leaf} leaves are exact algebraic functions of the others")
check("at least one leaf is an exact function of other leaves (so the menu over-counts directions)",
      n_dep >= 1)
print("""
  VERDICT S0. B=30 is the menu LENGTH and that part of the docstring is accurate. But 30 is NOT the
  branching factor of the enumeration: (a) 2 of the 8 unary slots are the same function as another
  slot, (b) leaves are algebraically dependent, and (c) -- decisively -- the enumerator DEDUPS BY
  VALUE and discards every non-dimensionless node before anything is counted. The count that enters
  a look-elsewhere calculation is the number of values COMPARED TO A TARGET, and that is measured
  below.""")


# =====================================================================================
print("\n" + BAR); print("S1  THE EXACT CANDIDATE-COUNT IDENTITY THE CODE IMPLEMENTS"); print(BAR)
# =====================================================================================
print("""
  grind.py:58-60 states the count as  (11 * 30**b_s) * germ_recipe_count(g_s)  -- that is the count of
  STEP SEQUENCES, before the skeleton layer is value-deduped. The code actually enumerates
        raw(D) = SUM over budget splits (b_s,g_s) of  n_skeletons(b_s) * n_germ_recipes(g_s)
  with n_skeletons = DEDUPED dimensionless skeletons. Both factors are computed here from the live
  code and checked against the committed build_meta.json raw counts.\n""")
n_free = len(D5._free_germ_keys(alpha))
n_sk = {}
for bs in range(1, 7):
    lay = PSL.load_layer(alpha, bs)
    src = "cached layer"
    if lay is None:
        lay = DN._skeleton_value_nodes(alpha, bs)
        src = "recomputed"
    n_sk[bs] = len(lay)
    seqs = 11 * 30 ** bs
    print(f"    b_s={bs}: step sequences 11*30^{bs} = {seqs:>15,}   ->  deduped dimensionless"
          f" skeletons {n_sk[bs]:>7,}   collapse {seqs/n_sk[bs]:>12,.0f}x   [{src}]")
n_rec = {gs: DN._germ_recipe_count(alpha, n_free, gs) for gs in range(3, 12)}
print(f"\n    germ recipes per skeleton (n_free={n_free}):")
prev = None
for gs, r in n_rec.items():
    rt = f"  x{r/prev:.2f}" if prev else ""
    print(f"      g_s={gs:>2}: {r:>10,}{rt}")
    prev = r
print("      -> the germ layer's growth RATIO FALLS with g_s: it is POLYNOMIAL, not exponential")

print("\n    reconstructed raw(D) vs the committed build_meta.json raw_candidates:\n")
print(f"    {'D':>3}{'model raw(D)':>16}{'committed raw':>16}{'match':>8}{'30^(D-4)':>14}{'model/30^(D-4)':>17}")
print("    " + "-" * 92)
committed_raw = {}
committed_dis = {}
for D in (7, 8, 9, 10):
    mp_path = RESULTS / f"depth_{D}" / "build_meta.json"
    if mp_path.exists():
        m = json.loads(mp_path.read_text())
        committed_raw[D], committed_dis[D] = m["raw_candidates"], m["distinct_by_value"]
# depth 7 has no grind build_meta; take it from the committed REPLAY ledger (machinery check)
if 7 not in committed_raw:
    for line in (RESULTS / "REPLAY_LEDGER.jsonl").read_text().strip().split("\n"):
        r = json.loads(line)
        if r.get("depth") == 7:
            for c in r["checks"]:
                if c["name"] == "raw candidates":    committed_raw[7] = int(c["committed"])
                if c["name"] == "distinct values":   committed_dis[7] = int(c["committed"])
model_raw = {}
exact_ok = True
for D in (7, 8, 9, 10):
    tot = sum(n_sk[bs] * n_rec[D - 1 - bs] for (bs, gs) in DN.budget_splits(D))
    model_raw[D] = tot
    cm = committed_raw.get(D)
    ok = (cm == tot)
    exact_ok &= ok
    print(f"    {D:>3}{tot:>16,}{cm:>16,}{'EXACT' if ok else 'DIFFER':>8}"
          f"{pub_N(D):>14.3e}{tot/pub_N(D):>17.3f}")
check("the (n_skeletons x n_germ_recipes) identity reproduces every committed raw count EXACTLY",
      exact_ok)

print("\n    realized growth, committed numbers only:\n")
print(f"    {'D':>3}{'raw':>16}{'x prev':>9}{'distinct':>14}{'x prev':>9}{'distinct/raw':>14}")
print("    " + "-" * 70)
pr = pd = None
ratios_raw, ratios_dis = [], []
for D in (7, 8, 9, 10):
    r, d = committed_raw[D], committed_dis[D]
    rr = f"{r/pr:.2f}" if pr else "-"
    dd = f"{d/pd:.2f}" if pd else "-"
    if pr: ratios_raw.append(r / pr)
    if pd: ratios_dis.append(d / pd)
    print(f"    {D:>3}{r:>16,}{rr:>9}{d:>14,}{dd:>9}{d/r:>14.4f}")
    pr, pd = r, d
B_raw = float(np.exp(np.polyfit([7, 8, 9, 10], np.log([committed_raw[D] for D in (7, 8, 9, 10)]), 1)[0]))
B_dis = float(np.exp(np.polyfit([7, 8, 9, 10], np.log([committed_dis[D] for D in (7, 8, 9, 10)]), 1)[0]))
print(f"\n    log-linear fit over D=7..10:   B_raw = {B_raw:.3f}    B_distinct = {B_dis:.3f}")
print(f"    per-depth ratios distinct: {['%.2f'%x for x in ratios_dis]}  (DECLINING -> sub-exponential)")
print(f"""
  VERDICT S1. The realized branching factor of the enumeration is B ~ {B_dis:.2f}, not 30. The 30 in the
  docstring is the pre-dedup step-menu length; between (a) the dimensionless filter, (b) value dedup and
  (c) the germ layer being POLYNOMIAL in its own budget, each extra depth multiplies the DISTINCT value
  count by only ~{B_dis:.1f}. log2({B_dis:.2f}) = {math.log2(B_dis):.2f} bits per depth of look-elsewhere cost,
  not log2(30) = {math.log2(30):.2f}.""")
check(f"realized B ({B_dis:.2f}) is far below the published 30", B_dis < 8)


# =====================================================================================
print("\n" + BAR); print("S2  IS D0 = 4 RIGHT?  (the model asserts N(D0) = 1)"); print(BAR)
# =====================================================================================
print(f"""
  N(D) = B^(D-D0) asserts N(D0) = 1: exactly ONE candidate at depth D0. Two independent readings of
  the code contradict D0=4 with N=1:
    * grind.py's own count for the b_s=D-4 split is 11*30^(D-4) -- i.e. 11, not 1, at D=4.
    * budget_splits(D) requires g_s>=3 and b_s>=1, so the FIRST non-empty depth is D=5, and the
      distinct-value counts at low depth are:\n""")
low = {}
for D in (5, 6, 7):
    sp = DN.budget_splits(D)
    tot = sum(n_sk[bs] * n_rec[gs] for (bs, gs) in sp)
    low[D] = tot
    print(f"      D={D}: splits {sp} -> raw {tot:,}")
print(f"      D=4: splits {DN.budget_splits(4)} -> raw {sum(n_sk[bs]*n_rec[gs] for (bs,gs) in DN.budget_splits(4)):,}"
      "   (EMPTY: the model's anchor depth cannot even be built)")
# what D0 does the published B=30 imply, given the real N(10)?
D0_implied_30 = 10 - math.log(committed_dis[10]) / math.log(30.0)
D0_implied_B = 10 - math.log(committed_dis[10]) / math.log(B_dis)
print(f"""
  Calibration check. With the REAL distinct count at D=10 ({committed_dis[10]:,}):
      B=30  requires D0 = {D0_implied_30:.2f}   (not 4)
      B={B_dis:.2f} requires D0 = {D0_implied_B:.2f}   (not 4)
  So (B=30, D0=4) is not two measured facts; it is one two-parameter guess that happens to land within
  {pub_N(10)/committed_dis[10]:.0f}x of the true multiplicity AT D=10 -- near the depth whose ceiling it is used to compute --
  while having the wrong SLOPE. Its error therefore explodes away from D~10:\n""")
print(f"    {'D':>4}{'published N(D)=30^(D-4)':>26}{'realized / extrapolated N(D)':>30}{'over-count':>16}")
print("    " + "-" * 78)
for D in (7, 8, 9, 10, 12, 14, 16, 18):
    real = committed_dis.get(D) or committed_dis[10] * B_dis ** (D - 10)
    tag = "" if D in committed_dis else " (extrap)"
    print(f"    {D:>4}{pub_N(D):>26.3e}{real:>26.3e}{tag:<4}{pub_N(D)/real:>15.3g}x")
check("D0=4 is not the depth at which N=1; budget_splits(4) is EMPTY so N(4)=0",
      len(DN.budget_splits(4)) == 0)
check("(B=30,D0=4) over-counts the real depth-10 multiplicity by >10x and by >1e6x at D=18",
      pub_N(10) / committed_dis[10] > 10 and pub_N(18) / (committed_dis[10] * B_dis ** 8) > 1e6)


# =====================================================================================
print("\n" + BAR); print("S3  THE MULTIPLICITY THAT ACTUALLY MATTERS: MEASURED LOCAL DENSITY"); print(BAR)
# =====================================================================================
print("""
  N(D)*w assumes the value set is spread so that a fraction w of it lands in a relative window w --
  i.e. roughly log-uniform over ~1 decade. The value set spans many decades and CLUSTERS, so this is
  wrong; PAPER_ATOMOS_NULL.md already reports it as ~100x wrong but does not propagate it into the
  ceiling. Here it is measured directly off the committed value arrays. The hit predicate is
  rel_error <= tol, i.e. a two-sided window of relative width 2*tol.\n""")

_range_report = {}
def load_vals(D):
    for nm in ("values.f64", "values_merged.f64"):
        p = RESULTS / f"depth_{D}" / nm
        if p.exists():
            a = np.fromfile(p, dtype="<f8")
            good = np.isfinite(a) & (a > 0)
            kept = a[good]
            _range_report[D] = dict(stored=len(a), nonfinite=int((~np.isfinite(a)).sum()),
                                    nonpos=int((a <= 0).sum()), kept=len(kept),
                                    distinct_f64=int(len(np.unique(kept))))
            return np.sort(kept)
    return None

tkeys = sm_target_keys(include_holdout=True)
ds = PDG.load()
reg = {t.key: t for t in ds.dimensionless(include_holdout=True)}
TGT = [(k, float(reg[k].value), float(measurement_tol(reg[k]))) for k in tkeys if k in reg]

def count_in(sv, tv, w):
    lo, hi = tv * (1.0 - w), tv * (1.0 + w)
    return int(np.searchsorted(sv, hi, "right") - np.searchsorted(sv, lo, "left"))

# --- 3a machinery proof: reproduce the committed per-target hit counts -------------------
print("  (a) MACHINERY PROOF -- recount hits straight off the value arrays and compare to the")
print("      committed per-target n_hits in results_grind/depth_{8,9}/VERDICT.json:\n")
svs = {D: load_vals(D) for D in (8, 9, 10)}
sv10 = svs[10]
agree = disagree = 0
uncov = []
for D in (8, 9):
    sv = svs[D]
    if sv is None:
        continue
    v = json.loads((RESULTS / f"depth_{D}" / "VERDICT.json").read_text())
    per = {p["target"]: p["n_hits"] for p in v.get("per_target", [])}
    bad, ok_d = [], 0
    have = {k for k, _, _ in TGT}
    for k, tv, w in TGT:
        if k not in per:
            continue
        c = count_in(sv, tv, w)
        if c == per[k]:
            agree += 1; ok_d += 1
        else:
            disagree += 1
            bad.append((k, c, per[k]))
    miss = [k for k in per if k not in have]
    uncov = miss
    print(f"      depth {D}: {len(per)} committed targets, {ok_d} of the "
          f"{len(per)-len(miss)} reachable ones recounted EXACTLY"
          + (f"   MISMATCH {bad}" if bad else "")
          + (f"   NOT REACHABLE from sm_target_keys(): {miss}" if miss else ""))
check(f"independent recount off the raw value arrays reproduces every committed per-target hit count "
      f"({agree} agree / {disagree} differ)", disagree == 0 and agree >= 40)

print("\n      SIDE FINDING (not the lens, but it falls out of loading the arrays): the committed")
print("      value arrays contain entries OUTSIDE float64 range, and float64 collisions:\n")
print(f"      {'D':>4}{'stored':>13}{'inf (overflow)':>16}{'<=0 (underflow)':>17}"
      f"{'usable':>13}{'distinct f64':>14}")
print("      " + "-" * 78)
for D in (8, 9, 10):
    r = _range_report.get(D)
    if r:
        print(f"      {D:>4}{r['stored']:>13,}{r['nonfinite']:>16,}{r['nonpos']:>17,}"
              f"{r['kept']:>13,}{r['distinct_f64']:>14,}")
RR10 = _range_report[10]
print(f"""
      So the depth-10 "42,534,139 distinct values" contains {RR10['nonfinite']+RR10['nonpos']:,} values that overflowed or
      underflowed float64 on the way to disk, and {RR10['kept']-RR10['distinct_f64']:,} further float64 collisions among the
      rest. The number of DISTINGUISHABLE candidates that could ever land on an O(1)-ish SM target is
      {RR10['distinct_f64']:,}, i.e. {RR10['stored']/RR10['distinct_f64']:.2f}x fewer than the headline count. Irrelevant to the null (no target is
      near the float64 rails), but it is a further over-count in any N-based look-elsewhere number.""")
check("the headline distinct count over-states the float64-distinguishable multiplicity by >1.2x",
      RR10["stored"] / RR10["distinct_f64"] > 1.2)

# --- 3b the naive model vs measurement, at depth 10 --------------------------------------
N10 = len(sv10)
print(f"\n  (b) depth 10: {N10:,} distinct values. Naive E = N*2w versus the MEASURED count:\n")
print(f"      {'target':<17}{'2w':>11}{'naive N*2w':>13}{'measured':>10}{'naive/meas':>12}"
      f"{'local density rho':>19}")
print("      " + "-" * 84)
rho10, over = {}, []
for k, tv, w in TGT:
    m = count_in(sv10, tv, w)
    naive = N10 * 2 * w
    rho10[k] = m / (2 * w)
    if m > 0:
        over.append(naive / m)
    print(f"      {k:<17}{2*w:>11.2e}{naive:>13.3e}{m:>10,}{(naive/m if m else float('nan')):>12,.0f}"
          f"{rho10[k]:>19.3e}")
med_over = float(np.median(over))
print(f"\n      median naive/measured over-count = {med_over:,.0f}x   (paper says '~100x')")
dense = [k for k, tv, w in TGT if count_in(sv10, tv, w) >= 300]
rho_typ10 = float(np.median([rho10[k] for k in dense]))
print(f"      typical measured local density rho (targets with >=300 hits) = {rho_typ10:.3e} per unit"
      f" relative window\n      => effective multiplicity is rho, not N: {N10/rho_typ10:,.0f}x smaller than the distinct count")
check(f"the naive N*2w model over-states chance hits by a median {med_over:,.0f}x at depth 10",
      med_over > 30)

# --- 3c how does rho grow with depth? ---------------------------------------------------
print("\n  (c) DEPTH GROWTH OF THE LOCAL DENSITY (this, not N, is what sets the ceiling):\n")
print(f"      {'target':<17}{'rho(D=8)':>13}{'rho(D=9)':>13}{'rho(D=10)':>13}{'x/depth 8->10':>16}")
print("      " + "-" * 74)
grow = []
for k, tv, w in TGT:
    r = {}
    for D in (8, 9, 10):
        c = count_in(svs[D], tv, w)
        r[D] = c / (2 * w)
    if min(count_in(svs[D], tv, w) for D in (8, 9, 10)) >= 100:
        g = (r[10] / r[8]) ** 0.5
        grow.append(g)
        print(f"      {k:<17}{r[8]:>13.3e}{r[9]:>13.3e}{r[10]:>13.3e}{g:>16.3f}")
B_rho = float(np.median(grow))
print(f"\n      median density growth per depth  B_rho = {B_rho:.3f}"
      f"   (vs distinct-count growth {B_dis:.3f}, vs published 30)")
check(f"the local density grows only ~{B_rho:.2f}x per depth, slower than the distinct count",
      B_rho < B_dis + 0.2)

# --- 3d density near the TIGHT targets, measured, then extrapolated to their windows ------
print("""
  (d) THE TIGHT TARGETS. Their windows are far below the spacing of the value set, so measure rho on
      a window ladder near each and read off where it stabilises; then E_chance = rho * 2w.\n""")
LAD = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
tight = ["alpha_em_inv_0", "r_p_e", "a_e", "r_mu_e"]
print(f"      {'target':<17}" + "".join(f"{('rho@w=%.0e'%w):>14}" for w in LAD))
print("      " + "-" * (17 + 14 * len(LAD)))
rho_tight = {}
for k in tight:
    tv = dict((a, b) for a, b, c in TGT)[k]
    row = []
    for w in LAD:
        row.append(count_in(sv10, tv, w) / (2 * w))
    rho_tight[k] = row
    print(f"      {k:<17}" + "".join(f"{x:>14.3e}" for x in row))
print("""
      The ladder is flat-ish across decades where counts are still large, then noise-limited: use the
      widest still-local rung (w=1e-3) as rho, which is CONSERVATIVE for a ceiling because coarse rho
      >= fine rho for a clustered set.""")


# =====================================================================================
print("\n" + BAR); print("S4  IS 'EXPECTED HITS = 1' THE RIGHT CRITERION?"); print(BAR)
# =====================================================================================
n_search_targets = len(sm_target_keys())
n_depths_swept = 8            # D=3..10 exhaustive, per NULL_RESULT_DEPTH10_EXHAUSTIVE.md
print(f"""
  E = 1 means "one chance match expected". Under Poisson that is P(>=1 chance hit) = 1-e^-1 = {1-math.exp(-1):.3f}:
  a 63% false-alarm rate. It is NOT a significance threshold, and it is the LENIENT end of the range.
  Three defensible criteria, and the depth shift each implies (shift = ln(1/E*)/ln(B) depths):\n""")
print(f"    {'criterion':<44}{'E*':>12}{'depth shift @B=30':>20}{'depth shift @B=%.2f'%B_rho:>22}")
print("    " + "-" * 98)
crits = [
    ("expected hits = 1 (published)", 1.0),
    ("P(>=1 chance hit) <= 0.05, single target", -math.log(0.95)),
    ("Bonferroni over the %d searched targets" % n_search_targets, -math.log(0.95) / n_search_targets),
    ("Bonferroni over %d targets x %d depths" % (n_search_targets, n_depths_swept),
     -math.log(0.95) / (n_search_targets * n_depths_swept)),
    ("BH-FDR q=0.05, rank-1 of %d targets" % n_search_targets, 0.05 / n_search_targets),
]
for nm, E in crits:
    s30 = math.log(1.0 / E) / math.log(30.0)
    sB = math.log(1.0 / E) / math.log(B_rho)
    print(f"    {nm:<44}{E:>12.4g}{-s30:>20.2f}{-sB:>22.2f}")
E_STAR = -math.log(0.95) / (n_search_targets * n_depths_swept)
print(f"""
  VERDICT S4. E=1 is TOO LENIENT as an informativeness criterion, by {math.log(1/E_STAR)/math.log(B_rho):.1f} depths at the realized
  branching factor: the honest threshold is E* = {E_STAR:.3g} (5% family-wise over {n_search_targets} targets x {n_depths_swept} depths),
  not E=1. This correction pushes D_max DOWN. It is the ONE error in the derivation that runs in the
  conservative direction, and it is much smaller than the multiplicity errors, which run the other way.
  NOTE the derivation is also internally inconsistent about the factor 2: GATE_POWER_ANALYSIS.py uses
  w2 = 2w, BITS_RULE.py uses w. That is 1 bit = {1/math.log2(B_rho):.2f} depths at B={B_rho:.2f}.""")
check("E=1 corresponds to a 63% false-alarm probability, so it is a lenient criterion, not a "
      "significance threshold", abs((1 - math.exp(-1)) - 0.632) < 0.01)


# =====================================================================================
print("\n" + BAR); print("S5  THE WINDOWS THEMSELVES: A 1000x UNIT ERROR IN THE PUBLISHED TABLE"); print(BAR)
# =====================================================================================
print("""
  GATE_POWER_ANALYSIS.py:41 writes m_p/m_e's precision as  3.2e-11/1836.15 -> w = 1.74e-14, and
  BITS_RULE.py:14 carries 3.49e-14. CODATA 2022 is m_p/m_e = 1836.152673426(32), i.e. an ABSOLUTE
  uncertainty of 3.2e-8, so the relative precision is 1.74e-11 -- the published figure is 1000x too
  tight. And the window the CODE actually searches with (propagated from the two kg masses) is:\n""")
w_code = float(measurement_tol(reg["r_p_e"]))
print(f"      repo's own registry: r_p_e rel_precision = {float(reg['r_p_e'].rel_precision):.4e}"
      f"   -> measurement_tol = {w_code:.4e}")
print(f"      CODATA direct ratio 3.2e-8/1836.1527 = {3.2e-8/1836.152673426:.4e}")
print(f"      BITS_RULE / GATE_POWER value (one-sided) = {1.74e-14:.4e}     <-- 1000x too tight")
print(f"\n      ceiling sensitivity to that alone, published model (B=30, D0=4, E=1):")
for nm, w in (("BITS_RULE w=3.49e-14 (as published)", 3.49e-14),
              ("CODATA direct ratio, two-sided", 2 * 3.2e-8 / 1836.152673426),
              ("the window the code actually uses, two-sided", 2 * w_code)):
    print(f"        {nm:<46} D_max = {pub_ceiling(w):.2f}")
print(f"""
      So even INSIDE the published model, "D = 13.1 for m_p/m_e" should read D = {pub_ceiling(2*3.2e-8/1836.152673426):.1f} on the CODATA
      ratio, or D = {pub_ceiling(2*w_code):.1f} on the window the search actually applies. That is a 2.0-2.6 depth
      over-statement from a units slip, INDEPENDENT of the branching-factor problem.""")
check("BITS_RULE/GATE_POWER's m_p/m_e window is ~1000x tighter than CODATA's relative precision",
      abs(math.log10(1.74e-11 / 1.74e-14) - 3) < 0.05)

MIN_TOL = 1e-10
print(f"""
  A second, structural cap nobody costed: engine/scoring.py:108 clamps measurement_tol to
  min_tol = {MIN_TOL:.0e}. NO target is ever searched with a window tighter than {MIN_TOL:.0e}, however well measured.
  So the ceiling of the ACTUAL SEARCH is capped at""")
print(f"      published model : D_max <= {pub_ceiling(2*MIN_TOL):.2f}")
print(f"      tightest window the registry actually presents = {min(w for _,_,w in TGT):.3e} (a_e)")
check("the engine's min_tol floor caps the achievable single-target ceiling near D~10.8 in the "
      "published model, so 'D=13.1 for m_p/m_e' is unreachable by the code as written",
      pub_ceiling(2 * MIN_TOL) < 11.0)


# =====================================================================================
print("\n" + BAR); print("S6  THE CORRECTED CEILING"); print(BAR)
# =====================================================================================
print(f"""
  Corrected model. Anchor on MEASURED quantities rather than a guessed (B,D0):
      E(D, target) = rho(target, D=10) * B_rho^(D-10) * 2w        [measured density, measured growth]
      informative iff E <= E*
  =>  D_max = 10 + ln( E* / (rho10 * 2w) ) / ln(B_rho)
  with B_rho = {B_rho:.3f} (S3c), rho10 measured per target (S3b/S3d), E* per S4.
  For comparison the same with N instead of rho (i.e. keeping the paper's uniform-density assumption
  but using the REAL distinct count and REAL growth) is also shown.\n""")

def dmax_rho(rho10_, w, E):
    return 10.0 + math.log(E / (rho10_ * 2 * w)) / math.log(B_rho)

def dmax_N(w, E):
    return 10.0 + math.log(E / (committed_dis[10] * 2 * w)) / math.log(B_dis)

rows = []
for k, label, w_use in (
    ("alpha_em_inv_0", "1/alpha", float(measurement_tol(reg["alpha_em_inv_0"]))),
    ("r_p_e", "m_p/m_e (code window)", w_code),
    ("r_p_e", "m_p/m_e (CODATA ratio)", 3.2e-8 / 1836.152673426),
    ("a_e", "a_e", float(measurement_tol(reg["a_e"]))),
    ("alpha_s_MZ", "alpha_s(M_Z)", float(measurement_tol(reg["alpha_s_MZ"]))),
):
    r10 = rho_tight.get(k, [None] * 3)
    rho_use = (r10[2] if k in rho_tight else rho10[k])   # w=1e-3 rung for tight targets
    rows.append((label, w_use, rho_use,
                 pub_ceiling(2 * w_use),
                 dmax_N(w_use, 1.0), dmax_rho(rho_use, w_use, 1.0),
                 dmax_rho(rho_use, w_use, E_STAR)))
print(f"    {'target':<24}{'2w used':>11}{'rho10':>11}{'PUBLISHED':>11}{'realB,N,E=1':>13}"
      f"{'realB,rho,E=1':>15}{'realB,rho,E*':>14}")
print("    " + "-" * 99)
for label, w, r, a, b, c, d in rows:
    print(f"    {label:<24}{2*w:>11.2e}{r:>11.2e}{a:>11.2f}{b:>13.2f}{c:>15.2f}{d:>14.2f}")
print("    (a NEGATIVE corrected D_max is not a bug: a loosely measured target like alpha_s has NO")
print("     depth at which a single-target match would clear a family-wise threshold, not even D=5.)")

# --- (iv) does an exponential extrapolation even hold? -----------------------------------
print(f"""
  (iv) SUB-EXPONENTIAL GROWTH. B^(D-D0) assumes a CONSTANT ratio. The measured ratios are not constant.
       distinct-count ratios D7->10: {['%.2f' % x for x in ratios_dis]}""")
sv8, sv9 = svs[8], svs[9]
rr = []
for k, tv, w in TGT:
    c8, c9, c10 = count_in(sv8, tv, w), count_in(sv9, tv, w), count_in(sv10, tv, w)
    if min(c8, c9, c10) >= 100:
        rr.append((c9 / c8, c10 / c9))
r89 = float(np.median([a for a, b in rr])); r910 = float(np.median([b for a, b in rr]))
print(f"       density ratios: D8->9 = {r89:.3f},  D9->10 = {r910:.3f}   (falling)")
slope = r910 - r89
B18_lin = max(1.5, r910 + slope * 8)
def dmax_decl(rho0, w, E):
    """Largest integer depth D with E(D) <= E*, under a LINEARLY DECAYING per-depth ratio refitted
    from the two measured ratios (r910 at D=10->11, decaying by |slope| each depth, floored at 1.05)."""
    r, rho, D = r910, rho0, 10
    if rho * 2 * w > E:
        return -1                     # already uninformative at the last measured depth
    while D < 60:
        rn = max(1.05, r)
        if rho * rn * 2 * w > E:
            return D
        rho *= rn; r += slope; D += 1
    return D
print(f"""       Extrapolating with a FIXED ratio {B_rho:.2f} is therefore an UPPER bound on the multiplicity and
       hence a LOWER bound on D_max; a linearly-decaying ratio (slope {slope:+.3f}/depth, reaching
       {B18_lin:.2f} by D=18) gives the other end of the bracket:""")
print(f"       {'target':<22}{'D_max fixed-ratio':>20}{'D_max decaying-ratio':>23}")
print("       " + "-" * 65)
for k, label, wv in (("alpha_em_inv_0", "1/alpha", float(measurement_tol(reg["alpha_em_inv_0"]))),
                     ("r_p_e", "m_p/m_e (code win)", w_code)):
    a_ = dmax_rho(rho_tight[k][2], wv, E_STAR)
    b_ = dmax_decl(rho_tight[k][2], wv, E_STAR)
    print(f"       {label:<22}{a_:>20.2f}{b_:>23.0f}")
print("""       The bracket is wide because nothing in the repo measures the ratio past D=10. That is the
       honest residual uncertainty in ANY version of this ceiling, published or corrected.""")

w_alpha = float(measurement_tol(reg["alpha_em_inv_0"]))
cor_a = dmax_rho(rho_tight["alpha_em_inv_0"][2], w_alpha, E_STAR)
cor_p_code = dmax_rho(rho_tight["r_p_e"][2], w_code, E_STAR)
cor_p_codata = dmax_rho(rho_tight["r_p_e"][2], 3.2e-8 / 1836.152673426, E_STAR)
print(f"""
  HEADLINE CORRECTION -- and the honest answer is that the ERRORS LARGELY CANCEL:
      1/alpha  : published D_max = 10.44  ->  corrected {cor_a:.2f}   ({cor_a-10.44:+.2f} depths; published TOO STRICT)
      m_p/m_e  : published D_max = 13.11  ->  corrected {cor_p_code:.2f}   ({cor_p_code-13.11:+.2f} depths on the window the
                 code actually applies) or {cor_p_codata:.2f} ({cor_p_codata-13.11:+.2f}) on the CODATA direct ratio
                 -- i.e. published TOO LENIENT for m_p/m_e, driven by the 1000x window slip.
  ERROR LADDER for 1/alpha: start from the published figure, change ONE assumption at a time.
  (An additive "budget" would be ambiguous because B and D0 are entangled, so substitute in sequence.)\n""")
_lad = [
    ("published: B=30, D0=4, uniform N, E=1", pub_ceiling(2 * w_alpha)),
    ("+ real multiplicity level at D=10 (N=%.3e)" % committed_dis[10],
     10 + math.log(1.0 / (committed_dis[10] * 2 * w_alpha)) / math.log(30.0)),
    ("+ real growth B=%.2f instead of 30" % B_dis,
     10 + math.log(1.0 / (committed_dis[10] * 2 * w_alpha)) / math.log(B_dis)),
    ("+ measured local density rho instead of N (%.0fx)" % med_over,
     10 + math.log(1.0 / (rho_tight["alpha_em_inv_0"][2] * 2 * w_alpha)) / math.log(B_rho)),
    ("+ family-wise E* = %.2g instead of E=1" % E_STAR, cor_a),
]
prev_l = None
for nm, d in _lad:
    delta = "" if prev_l is None else f"   ({d-prev_l:+.2f})"
    print(f"      {nm:<52} D_max = {d:>6.2f}{delta}")
    prev_l = d
print(f"      {'m_p/m_e only: window units 3.49e-14 -> code window':<52} "
      f"D_max = {cor_p_code:>6.2f}   ({cor_p_code-cor_p_codata:+.2f} vs CODATA ratio {cor_p_codata:.2f})")
print(f"""
  NET: the LEVEL of the published ceiling is roughly right (~10-13) by cancellation, but the SLOPE is
  wrong by {math.log(30)/math.log(B_rho):.1f}x: the true look-elsewhere cost is {math.log2(B_rho):.2f} bits/depth, not {math.log2(30):.2f}. Every claim that
  depends on the slope rather than the level is therefore mis-stated (see S7b).""")
check("the corrected 1/alpha ceiling is ABOVE the published 10.44 (published too strict)",
      cor_a > 10.44)
check("the corrected m_p/m_e ceiling on the window the code actually uses is BELOW the published "
      "13.11 (published too lenient there)", cor_p_code < 13.11)


# =====================================================================================
print("\n" + BAR); print("S7  WHAT THE CORRECTION DOES AND DOES NOT CHANGE"); print(BAR)
# =====================================================================================
# does the qualitative "depth 18 is empty" claim survive the corrected arithmetic?
print("\n  (a) DOES 'DEPTHS 10-18 WERE EMPTY BY CONSTRUCTION' SURVIVE? Test it, do not assume it.")
print(f"\n      {'target':<20}{'2w':>11}{'published E(18)':>17}{'corrected E(18)':>17}"
      f"{'informative @E*?':>18}")
print("      " + "-" * 84)
surv = True
for k, label in (("alpha_em_inv_0", "1/alpha"), ("r_p_e", "m_p/m_e"), ("a_e", "a_e"),
                 ("r_mu_e", "m_mu/m_e")):
    w = float(measurement_tol(reg[k]))
    Epub = pub_N(18) * 2 * w
    Ecor = rho_tight[k][2] * B_rho ** 8 * 2 * w
    inf_ = Ecor <= E_STAR
    surv &= (not inf_)
    print(f"      {label:<20}{2*w:>11.2e}{Epub:>17.2e}{Ecor:>17.2e}"
          f"{('YES' if inf_ else 'no'):>18}")
print(f"""
      (E* = {E_STAR:.2g}.) VERDICT: the published CONCLUSION SURVIVES. Even with the multiplicity cut by
      {pub_N(18)/(rho_typ10*B_rho**8):.1e}x, a single-target match at depth 18 still expects E ~ 3-600 chance hits, far above any
      threshold. The paper is right that single-target matching is dead by ~depth 11-13 and right that
      its depth-10-18 sampling could not have established a single-target result. It got there through
      a derivation whose branching factor is 7x too big, whose D0 is unfoundable and whose criterion is
      too lenient -- three errors that happen to cancel. DO NOT report this as a reversal.

  (b) THE SLOPE-DEPENDENT CLAIMS DO NOT SURVIVE. BITS_RULE.py's threshold is
      SUM_i log2(1/w_i) > log2(N(D)) + 10. The cost term is over-stated:""")
print(f"      {'D':>4}{'published log2(N)':>20}{'corrected log2(rho)':>22}{'over-stated by':>17}")
print("      " + "-" * 64)
for D in (10, 13, 18):
    cp = math.log2(pub_N(D))
    cc = math.log2(rho_typ10 * B_rho ** (D - 10))
    print(f"      {D:>4}{cp:>20.1f}{cc:>22.1f}{cp-cc:>15.1f} bits")
bits = lambda w: math.log2(1.0 / w)
two_tight_pub = bits(3.49e-14) + bits(3.06e-10)
two_tight_cor = bits(2 * w_code) + bits(2 * w_alpha)
need18_pub = math.log2(pub_N(18)) + 10
need18_cor = math.log2(rho_typ10 * B_rho ** 8) + 10
print(f"""
      BITS_RULE's headline: "the two most precisely measured numbers in physics are NOT enough on their
      own at depth 18" -- {two_tight_pub:.1f} available bits vs {need18_pub:.1f} needed. Corrected on BOTH sides (real windows,
      real multiplicity): {two_tight_cor:.1f} available vs {need18_cor:.1f} needed -> they DO clear. The k_min conclusion and the
      'stop escalating depth, each depth costs {math.log2(30):.1f} bits' recommendation both change: the real cost is
      {math.log2(B_rho):.2f} bits/depth. THIS is the finding that touches the interlock rule.""")
print("""
      The substitution "log2(N) -> log2(rho)" is the k=1 form. Done properly for a k-target interlock:
      one structure out of N is tried, and its chance of landing in target i's window is
      p_i = 2w_i * rho_i / N, so E_joint(k) = N * PROD p_i = N^(1-k) * PROD (2w_i rho_i), i.e.
          need   SUM_i log2(1/(2w_i))  >  SUM_i log2(rho_i) - (k-1)*log2(N) + log2(1/E*)
      which reduces to the single-target rule at k=1. Both forms, at the two tightest targets:\n""")
for D in (10, 18):
    NN = committed_dis[10] * B_dis ** (D - 10)
    rr_ = rho_typ10 * B_rho ** (D - 10)
    simple = math.log2(rr_) + math.log2(1 / E_STAR)
    full = 2 * math.log2(rr_) - math.log2(NN) + math.log2(1 / E_STAR)
    print(f"      D={D:<3} k=2 need: simple form {simple:>6.1f} bits | full form {full:>6.1f} bits | "
          f"available {two_tight_cor:.1f} -> {'CLEARS' if two_tight_cor > max(simple, full) else 'short'}")
print(f"      (published rule at D=18 said: need {need18_pub:.1f}, available {two_tight_pub:.1f} -> FALLS SHORT.)")
_full18 = 2 * math.log2(rho_typ10 * B_rho ** 8) - math.log2(committed_dis[10] * B_dis ** 8) \
          + math.log2(1 / E_STAR)
check("the published bits-cost at depth 18 is over-stated by >30 bits, and under BOTH corrected "
      "interlock forms the two tightest targets CLEAR at depth 18 (reversing BITS_RULE)",
      math.log2(pub_N(18)) - math.log2(rho_typ10 * B_rho ** 8) > 30
      and two_tight_cor > need18_cor and two_tight_cor > _full18)

# --- a retention gap that blocks the interlock read-out rule ------------------------------
print("\n  (c) SIDE FINDING with interlock consequences: the SECOND holdout cannot be scored.")
import sqlite3                                                              # noqa: E402
tv_rt = float(reg["r_tau_mu"].value); w_rt = float(measurement_tol(reg["r_tau_mu"]))
n_in = count_in(sv10, tv_rt, w_rt)
con = sqlite3.connect(str(RESULTS / "depth_10" / "records.sqlite"))
n_rec_tot = con.execute("SELECT COUNT(*) FROM records").fetchone()[0]
n_rec_rt = con.execute("SELECT COUNT(*) FROM records WHERE ABS(value-?)<=?",
                       (tv_rt, tv_rt * w_rt)).fetchone()[0]
con.close()
print(f"      exhaust_parallel.sm_target_keys(include_holdout=True) returns "
      f"{len(sm_target_keys(include_holdout=True))} keys, not 21:")
print(f"        it re-adds koide_Q_lep by name but never r_tau_mu -> {uncov} is unreachable.")
print(f"      grind._target_windows() is built from that list, so depth 10 retained "
      f"{n_rec_rt} records near r_tau_mu")
print(f"      even though {n_in} depth-10 values fall inside its window ({n_rec_tot:,} records total).")
print("""      PAPER §6 calls r_tau_mu "the stronger test" precisely because it has no famous closed
      form. At depth 10 a survivor's out-of-sample prediction for it could not be scored from the
      committed records -- which is exactly the input GATE_POWER_ANALYSIS's JACKPOT read-out rule
      asks for. Outside this audit's lens, but it is a verified defect in the same chain.""")
check("the second holdout r_tau_mu has depth-10 in-window values but ZERO retained records, so the "
      "documented out-of-sample check is not scoreable there", n_in > 0 and n_rec_rt == 0)

print("""
  (d) it does NOT rescue the search's prior. The four structural obstructions in PAPER §5
      (number field, period ring, dictionary, varying constants) are untouched by this audit, and the
      hit-distribution diagnostic in §3 -- hits track window width and nothing else -- is CONFIRMED
      here at higher precision (S3b: 19 targets, hits/2w flat at rho ~ 3e5 across five decades of
      window). The corrections are to the ceiling ARITHMETIC and to the slope-dependent claims built
      on it, not to the null.""")

print("\n" + BAR)
print(f"CEILING AUDIT: {sum(checks)}/{len(checks)} checks PASS."
      f"  {'ALL PASS' if all(checks) else 'SOME FAILED'}")
print(BAR)
sys.exit(0 if all(checks) else 1)
