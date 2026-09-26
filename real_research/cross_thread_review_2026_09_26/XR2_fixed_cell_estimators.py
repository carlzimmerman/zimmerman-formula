#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR2 (PART B) -- THE CLEARING ESTIMATORS: what L379's fixed-cell measure estimates, what a baryon-selected one would, and
whether Lean I28's hypotheses are L379's statistic.

Reviewed: real_research/dark_sector_2026/L379_clearing_by_environment.py (1c5a52dd5), L380_pooled_window_fixed_cell_
clearing.py (4e16ccf58), fable_independent_2026/lean_2026/I28_selection_inflates_retention.lean (8ad1d1e69).  Nothing
is imported from them and no simulation is run.

Notation (per cell, z = 2, L377's mesh units): rho = total matter / mean matter; c = carrier / mean matter (= WC x L377's
rhoc2); b = rho - c = baryons / mean matter.  In L377's LCDM run the two species share initial positions and feel the same
field (L377.py run(): xcar = xb.copy(), pcar = pb.copy(); mode 'none' gives both the same grad phi), so b_l = WB rho_l.
  (A) the record's G3 (L377.py lines 196-198): [sum_{rho_m>50} c_m/sum rho_m] / [sum_{rho_l>50} c_l/sum rho_l]
  (B) L379's fixed cells (L379.py line 144, L380.py lines 98/108/118): sum_F c_m / sum_F c_l,  F = {rho_l > 50}
  (C) baryons kept in the fixed cells: sum_F b_m / sum_F b_l
  (D) fixed-cell dark-to-baryon ratio: (B)/(C) = [sum_F c_m/sum_F b_m] / [sum_F c_l/sum_F b_l]
  (E) baryon-selected, the model's own baryons: S_m = {b_m/WB > 50}: [sum_S_m c_m/sum_S_m b_m] / [sum_F c_l/sum_F b_l]
  (E_rank) as E with S_m = the |F| cells of largest b_m (rank-matched)
  (L) Lagrangian: the carrier-to-baryon ratio at the model positions of the baryons that sit in F in LCDM (needs particle
      identities; in the synthetic tests below the displacement map is known, in the PM it is not saved)

PART 1  I28 vs L379's statistic.  I28 proves: for S = {i in s : c_m,i >= tau c_l,i} (ONE threshold tau on the per-cell
retained fraction, S inside LCDM's set s), sum_S c_m/sum_S c_l >= sum_s c_m/sum_s c_l.  L379's (A) selects on the MODEL's
total density, rho_m = b_m + c_m > 50, i.e. c_m,i/c_l,i > (50 - b_m,i)/c_l,i: a CELL-DEPENDENT threshold (through the
model's baryons), a set not contained in F, and a ratio of carrier FRACTIONS.  P1 gives an exact counterexample in which
the own-set statistic falls BELOW the fixed-cell value; P2 counts how often that happens in random instances.
PART 2  synthetic truth (a lognormal field, known retention):
  S1 carrier cleared in place, baryons unchanged:  B = D = E = truth; A overstates it (L379's bias).
  S2 galaxies move one cell and keep their retained carrier (the "bias the other way"):  E = L = truth; B understates it.
  S3 baryons stay denser where the carrier stayed (the carrier is 84% of the binding mass): D = L = truth; E (fixed
     threshold) overstates it -- selection on the model's own baryons is not free of the outcome either.
PART 3  ILLUSTRATION ONLY: the 128^3 code-test fields an uncommitted L379 development run left in $TMPDIR/L379_8o3o3c8p
  (2x coarser mesh than the committed 256^3 runs, particle number not recorded).  Not the committed runs, not a physics
  result, not load-bearing; skipped if absent.
MUTATE=1 selects E's set on the model's TOTAL density (rho_m > 50) instead of its baryons: S1's E check must FAIL (rc = 1).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR2_fixed_cell_estimators.py
Single-threaded, numpy only, < 30 s.
"""
import os, sys, json, math, time
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR2_fixed_cell_estimators"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR2-B", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 112); P(t); P("=" * 112)


P(__doc__.split("PART 1")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: estimator E selects on total density, not baryons; S1's E check must FAIL (rc = 1) ***")

H_, OM_ = 0.6736, 0.3138                                         # L362's PM background (L366 imports it)
WB = (0.02237 / H_ ** 2) / OM_; WC = 1.0 - WB                     # L366.py lines 73-74
THR = 50.0
P(f"\n  PM species weights (L366.py lines 73-74 with L362's h, Om): WB = {WB:.6f}, WC = {WC:.6f}; dense threshold {THR:g}")
# the PM cell at z = 2 in physical units, against R_e of L376's RC100 host (L376.out line 54: R_e = 5.4 kpc)
cell_phys_kpc = 100.0 / 256 / H_ * 1e3 / (1 + 2.0)
P(f"  one mesh cell (100 Mpc/h / 256) at z = 2 = {cell_phys_kpc:.0f} kpc physical = {cell_phys_kpc / 5.4:.0f} x R_e (5.4 kpc, L376)")
OUT["numbers"]["cell_phys_kpc_z2"] = cell_phys_kpc


# ------------------------------------------------------------------------------------------ the estimators
def estimators(rho_l, c_l, rho_m, c_m, lag_map=None):
    """sums over one box; returns numerators/denominators so boxes can be pooled by summing (as L380)."""
    b_l, b_m = rho_l - c_l, rho_m - c_m
    F = rho_l > THR
    D_m = rho_m > THR
    S_m = (rho_m > THR) if MUTATE else (b_m / WB > THR)
    nF = int(F.sum())
    top = np.argsort(b_m.ravel())[::-1][:nF]
    out = dict(
        A=(float(c_m[D_m].sum() / WC / max(rho_m[D_m].sum(), 1e-30)), float(c_l[F].sum() / WC / max(rho_l[F].sum(), 1e-30))),
        B=(float(c_m[F].sum()), float(c_l[F].sum())),
        C=(float(b_m[F].sum()), float(b_l[F].sum())),
        E=(float(c_m[S_m].sum()), float(b_m[S_m].sum())),
        Er=(float(c_m.ravel()[top].sum()), float(b_m.ravel()[top].sum())),
        Fref=(float(c_l[F].sum()), float(b_l[F].sum())),
        n=dict(F=nF, D_m=int(D_m.sum()), S_m=int(S_m.sum()), S_m_in_F=int((S_m & F).sum()),
               bmass_S_m_in_F=float(b_m[S_m & F].sum() / max(b_m[S_m].sum(), 1e-30))))
    if lag_map is not None:                                       # model location of the baryons that sit in F in LCDM
        idx = lag_map(np.flatnonzero(F.ravel()))
        out["L"] = (float(c_m.ravel()[idx].sum()), float(b_m.ravel()[idx].sum()))
    return out


def combine(rows):
    """pool over boxes by summing numerators and denominators (L380's convention; A as L380's g3a)."""
    s = lambda k, j: sum(r[k][j] for r in rows)
    ref = s("Fref", 0) / s("Fref", 1)
    res = dict(A=s("A", 0) / max(s("A", 1), 1e-30), B=s("B", 0) / s("B", 1), C=s("C", 0) / s("C", 1),
               E=(s("E", 0) / max(s("E", 1), 1e-30)) / ref if s("E", 1) > 0 else float("nan"),
               Er=(s("Er", 0) / s("Er", 1)) / ref)
    res["D"] = res["B"] / res["C"]
    if all("L" in r for r in rows):
        res["L"] = (s("L", 0) / s("L", 1)) / ref
    return res


# ============================================================================================ PART 1: I28's hypotheses
banner("PART 1  I28's HYPOTHESES AGAINST L379's STATISTIC (A)")
F_ = Fraction
wb = F_(WB); wc = 1 - wb
rl = F_(100)                                                      # two LCDM-dense cells, rho_l = 100 each
cl1 = cl2 = wc * rl
bm1, cm1 = F_(5), F_(40)                                          # cell 1: the model's baryons left, 47% of the carrier kept
bm2, cm2 = F_(49), F_(2)                                          # cell 2: baryons piled in, 2% of the carrier kept
sel1, sel2 = bm1 + cm1 > THR, bm2 + cm2 > THR                     # L379/L377's own-dense-set selection (total density)
fixed = (cm1 + cm2) / (cl1 + cl2)
own_restricted = (cm2 / cl2) if (sel2 and not sel1) else None
g3_fraction = (cm2 / (bm2 + cm2)) / ((cl1 + cl2) / (rl + rl))
P(f"    cell 1: LCDM rho 100 (c_l = {float(cl1):.2f}); model b = 5, c = 40 -> rho_m = 45, selected {sel1}; retained fraction {float(cm1 / cl1):.3f}")
P(f"    cell 2: LCDM rho 100 (c_l = {float(cl2):.2f}); model b = 49, c = 2 -> rho_m = 51, selected {sel2}; retained fraction {float(cm2 / cl2):.4f}")
P(f"    fixed-cell (B) = {float(fixed):.4f};  own set, I28's form sum_S c_m/sum_S c_l = {float(own_restricted):.4f};  own set, G3's "
  f"fraction form = {float(g3_fraction):.4f}  (exact rationals)")
ok_p1 = own_restricted < fixed and g3_fraction < fixed
check("P1 I28's conclusion does not transfer to L379's statistic: with selection on the model's TOTAL density (the implied "
      "retention threshold (50 - b_m,i)/c_l,i varies with the model's baryons) the own-set value can fall BELOW the "
      "fixed-cell value (exact counterexample)", f"own-set {float(own_restricted):.4f} / G3-form {float(g3_fraction):.4f} < "
      f"fixed {float(fixed):.4f}", ok_p1,
      "I28 needs ONE threshold on c_m/c_l and a selected set inside LCDM's; L379's (A) has neither, and normalises by each "
      "run's own total mass")
rng = np.random.default_rng(2026)
NT, NC = 20000, 20
v_unif = v_l379 = v_l379_g3 = 0
for _ in range(NT):
    rho_l_ = rng.uniform(55.0, 300.0, NC); c_l_ = WC * rho_l_
    r_ = rng.uniform(0.0, 0.4, NC); c_m_ = r_ * c_l_
    b_m_ = WB * rho_l_ * rng.uniform(0.2, 2.0, NC)                # the model's baryons move between cells
    fx = c_m_.sum() / c_l_.sum()
    tau = rng.uniform(0.0, 0.4); Su = r_ >= tau                   # I28's selection
    if Su.any() and c_m_[Su].sum() / c_l_[Su].sum() < fx - 1e-12:
        v_unif += 1
    S = (b_m_ + c_m_) > THR                                       # L379's selection
    if S.any():
        v_l379 += int(c_m_[S].sum() / c_l_[S].sum() < fx - 1e-12)
        v_l379_g3 += int((c_m_[S].sum() / (b_m_[S] + c_m_[S]).sum()) / (c_l_.sum() / rho_l_.sum()) < fx - 1e-12)
P(f"    {NT} random 20-cell instances (retention U(0, 0.4), model baryons x U(0.2, 2)): I28-type selection below fixed in "
  f"{v_unif}; L379-type selection below fixed in {v_l379} (I28 form) / {v_l379_g3} (G3 fraction form)")
OUT["numbers"]["P1"] = dict(fixed=float(fixed), own_restricted=float(own_restricted), g3_fraction=float(g3_fraction),
                            random=dict(n=NT, below_uniform_tau=v_unif, below_l379=v_l379, below_l379_g3=v_l379_g3))
check("P2 the theorem holds for its own hypothesis (uniform tau: no instance below fixed) and the L379-type selection can "
      "fall below in random instances", f"uniform tau {v_unif}/{NT}; L379-type {v_l379}/{NT} (I28 form), {v_l379_g3}/{NT} (G3 form)",
      v_unif == 0 and (v_l379 > 0 or v_l379_g3 > 0),
      f"the reversal is possible (P1, exact) but, in G3's fraction form, atypical ({v_l379_g3}/{NT} random instances): "
      "(A) > (B) in L379's data (e.g. 0.174 vs 0.052, galaxy bin, 700 km/s, L379.out) is an empirical ordering, not a "
      "consequence of I28; Part 3 shows the other way it can break (an EMPTY own set reads 0)")

# ============================================================================================ PART 2: synthetic truth
banner("PART 2  SYNTHETIC TRUTH: which estimator recovers the dark-to-baryon ratio at the model's galaxies")
N = 64
g = np.random.default_rng(7).normal(size=(N, N, N))
k = np.fft.fftfreq(N); KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
g = np.real(np.fft.ifftn(np.fft.fftn(g) * np.exp(-0.5 * (2 * np.pi * 1.5) ** 2 * (KX ** 2 + KY ** 2 + KZ ** 2))))
g = (g - g.mean()) / g.std() * 1.8
rho_l = np.exp(g - 0.5 * 1.8 ** 2); rho_l /= rho_l.mean()
c_l = WC * rho_l; b_l = WB * rho_l                                # LCDM: the two species coincide
F = rho_l > THR
ret = np.random.default_rng(11).uniform(0.0, 0.2, rho_l.shape)    # per-cell retention of the carrier
floor = lambda removed: removed.sum() / removed.size              # the removed carrier spread uniformly (mass conserved)
P(f"    lognormal field {N}^3, sigma_ln 1.8, 1.5-cell smoothing: {int(F.sum())} dense cells (rho_l > 50); retention U(0, 0.2)")
SYN = {}
# S1: cleared in place, baryons unchanged
c1 = ret * c_l; c1 = c1 + floor(c_l - c1); b1 = b_l.copy()
e1 = combine([estimators(rho_l, c_l, b1 + c1, c1, lag_map=lambda i: i)])
t1 = float((c1[F].sum() / b1[F].sum()) / (c_l[F].sum() / b_l[F].sum()))
SYN["S1"] = dict(truth=t1, **e1)
# S2: galaxies move one cell along x, carrier retained with them
shift = lambda a: np.roll(a, 1, axis=0)
c2 = shift(ret * c_l); c2 = c2 + floor(c_l - ret * c_l); b2 = shift(b_l)
lag2 = lambda i: np.ravel_multi_index(((np.unravel_index(i, (N, N, N))[0] + 1) % N, *np.unravel_index(i, (N, N, N))[1:]), (N, N, N))
e2 = combine([estimators(rho_l, c_l, b2 + c2, c2, lag_map=lag2)])
Fs = shift(F)
t2 = float((c2[Fs].sum() / b2[Fs].sum()) / (c_l[F].sum() / b_l[F].sum()))
SYN["S2"] = dict(truth=t2, **e2)
# S3: baryons stay denser where the carrier stayed (0.3x at no retention, 1.0x at full), galaxies in place
gb = 0.3 + 3.5 * ret
b3 = b_l * gb; b3 = b3 + (b_l.sum() - b3.sum()) / b3.size
c3 = ret * c_l; c3 = c3 + floor(c_l - c3)
e3 = combine([estimators(rho_l, c_l, b3 + c3, c3, lag_map=lambda i: i)])
t3 = float((c3[F].sum() / b3[F].sum()) / (c_l[F].sum() / b_l[F].sum()))
SYN["S3"] = dict(truth=t3, **e3)
for nm, d in SYN.items():
    P(f"    {nm}: truth {d['truth']:.4f} | A {d['A']:.4f}  B {d['B']:.4f}  C {d['C']:.4f}  D {d['D']:.4f}  E {d['E']:.4f}  "
      f"E_rank {d['Er']:.4f}  L {d['L']:.4f}")
OUT["numbers"]["synthetic"] = SYN
s1, s2, s3 = SYN["S1"], SYN["S2"], SYN["S3"]
check("S1 carrier cleared in place, baryons unchanged: B, D and E recover the truth (1e-10) and the record's own-set G3 (A) "
      "overstates it", f"truth {s1['truth']:.4f}: B {s1['B']:.4f}, D {s1['D']:.4f}, E {s1['E']:.4f}; A {s1['A']:.4f}",
      max(abs(s1[k_] - s1["truth"]) for k_ in ("B", "D", "E")) < 1e-10 and s1["A"] > 1.01 * s1["truth"],
      "L379's selection bias reproduced on a field where the answer is known")
check("S2 galaxies displaced with their retained carrier: E and L recover the truth (1e-10); fixed cells (B) understate it",
      f"truth {s2['truth']:.4f}: E {s2['E']:.4f}, L {s2['L']:.4f}; B {s2['B']:.4f}, D {s2['D']:.4f}",
      abs(s2["E"] - s2["truth"]) < 1e-10 and abs(s2["L"] - s2["truth"]) < 1e-10 and s2["B"] < 0.99 * s2["truth"],
      "the 'bias the other way' exists in principle: fixed cells do not follow the model's galaxies", load_bearing=False)
check("S3 baryon density tied to carrier retention: D and L recover the truth (1e-10); the fixed-threshold baryon selection "
      "(E) overstates it", f"truth {s3['truth']:.4f}: D {s3['D']:.4f}, L {s3['L']:.4f}; E {s3['E']:.4f}, E_rank {s3['Er']:.4f}",
      abs(s3["D"] - s3["truth"]) < 1e-10 and abs(s3["L"] - s3["truth"]) < 1e-10 and s3["E"] > 1.01 * s3["truth"],
      "selecting on the model's own baryons is not free of the outcome when the carrier is most of the binding mass; only "
      "the Lagrangian estimator is exact in all three cases", load_bearing=False)

# ============================================================================================ PART 3: code-test fields
banner("PART 3  ILLUSTRATION ONLY: the 128^3 code-test fields of an uncommitted L379 development run ($TMPDIR)")
TD = os.path.join(os.environ.get("TMPDIR", "/tmp"), "L379_8o3o3c8p")
if not os.path.isdir(TD):
    P(f"    {TD} not present: skipped (the committed 256^3 runs deleted their fields, L379.py line 158, L380.py line 110)")
    OUT["numbers"]["codetest"] = None
else:
    ld = lambda sp, run, f: np.load(os.path.join(TD, f"s{sp}_{run}_z2_{f}.npy")).astype(np.float64)
    ROWS, PER, ident, nulldev = {"v675": [], "v700": []}, {}, 0.0, 0.0
    for sp in (7, 17, 29):
        rl_, c2l = ld(sp, "lcdm", "rho"), ld(sp, "lcdm", "rhoc")
        ident = max(ident, float(np.max(np.abs(rl_ - c2l)) / rl_.max()))       # LCDM: rho = rhoc2 (species coincide)
        e0 = combine([estimators(rl_, WC * c2l, rl_, WC * c2l)])                 # null: model := LCDM
        nulldev = max(nulldev, max(abs(e0[k_] - 1) for k_ in ("A", "B", "C", "D", "E", "Er")))
        for t in ("v675", "v700"):
            rm_, c2m = ld(sp, t, "rho"), ld(sp, t, "rhoc")
            e = estimators(rl_, WC * c2l, rm_, WC * c2m)
            ROWS[t].append(e); PER[f"{sp}/{t}"] = dict(**combine([e]), n=e["n"])
            d = PER[f"{sp}/{t}"]
            P(f"    box ({sp:2d}) {t}: A {d['A']:.3f} (model dense cells {e['n']['D_m']} of LCDM's {e['n']['F']}) | B {d['B']:.3f} | "
              f"C {d['C']:.3f} | D {d['D']:.3f} | E {d['E']:.3f} (S_m {e['n']['S_m']}, in F {e['n']['S_m_in_F'] / max(e['n']['S_m'], 1):.2f}, "
              f"baryon mass in F {e['n']['bmass_S_m_in_F']:.2f}) | E_rank {d['Er']:.3f}")
    POOL = {t: combine(v) for t, v in ROWS.items()}
    for t, d in POOL.items():
        P(f"    POOLED {t}: A {d['A']:.3f} | B {d['B']:.3f} | C {d['C']:.3f} | D {d['D']:.3f} | E {d['E']:.3f} | E_rank {d['Er']:.3f}"
          f"   (E/B = {d['E'] / d['B']:.2f}, D/B = {d['D'] / d['B']:.2f})")
    OUT["numbers"]["codetest"] = dict(dir=TD, per_box=PER, pooled=POOL, lcdm_species_identity=ident, null_dev=nulldev)
    check("K (code-test controls) the LCDM fields satisfy rho = rhoc2 (the two species coincide, to float32) and the "
          "estimators return 1 when the model is LCDM itself", f"max |rho - rhoc2|/max rho = {ident:.1e}; null max |est - 1| = "
          f"{nulldev:.1e}", ident < 1e-5 and nulldev < 1e-5, load_bearing=False)
    P("    reading (ILLUSTRATION ONLY -- 2x coarser mesh than the committed runs, particle number not recorded, uncommitted "
      "files): the model keeps ~80% of LCDM's baryons in LCDM's dense cells and ~90% of its own baryon-dense cells lie in "
      "them; the baryon-normalised and baryon-selected values exceed the fixed-cell value by ~20-30%; the own-set G3 is "
      "degenerate at this resolution (0-4 model dense cells per box: it reads ~0 where the set is empty)")

# ============================================================================================ flip condition (L380)
banner("FLIP CONDITION: how far the model's baryons must leave LCDM's dense cells for D = B/C to exceed 0.30 (L380)")
R80 = os.path.join(HERE, "..", "dark_sector_2026", "L380_pooled_window_fixed_cell_clearing_results.json")
flip = {}
for t, g_ in json.load(open(R80))["numbers"]["table"]["pooled"].items():
    flip[t] = dict(B=g_["clear_fixed"], G3_own=g_["G3_own"], C_flip=g_["clear_fixed"] / 0.30)
    ct = OUT["numbers"].get("codetest")
    extra = ""
    if ct:
        cmin, cmax = min(v["C"] for v in ct["pooled"].values()), max(v["C"] for v in ct["pooled"].values())
        extra = f";  if C were the code-test's {cmin:.2f}-{cmax:.2f}: D = {g_['clear_fixed'] / cmax:.3f}-{g_['clear_fixed'] / cmin:.3f} (illustrative)"
    P(f"    L380 pooled {t}: B = {g_['clear_fixed']:.4f} (record's own-set G3 {g_['G3_own']:.3f}) -> D > 0.30 only if C < {flip[t]['C_flip']:.3f}{extra}")
OUT["numbers"]["flip_L380"] = flip

# ============================================================================================ verdict
banner("VERDICT (PART B)")
P("""  I28 certifies the idealised mechanism (one retention threshold, a subset of LCDM's cells); L379's own-set G3 selects on
  the model's total density, so the theorem does not apply to it (P1: exact counterexample; P2).  On a field with known
  truth the fixed-cell measure (B) is exact only while the model's galaxies stay in LCDM's cells; the baryon-selected
  measure (E) is exact only while the baryons' density does not depend on the carrier kept; the Lagrangian measure (L)
  is exact in all three cases and needs particle identities that no committed run saved.  See XR2_fixed_cell_review.md
  for the specification the same-cell re-run should record.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_fail; OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.1f}s]")
sys.exit(0 if n_fail == 0 else 1)
