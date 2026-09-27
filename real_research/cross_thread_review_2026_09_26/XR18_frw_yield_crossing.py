#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR18 (e) -- H_Y ON FRW: the linearisation about the frozen phi (FP9 Y3), and what happens to growth when overdensities cross
the yield.  Is there a jump in G_eff, or any instability, at the non-differentiable point?

WHY.  FP9 (derivation_chain_2026/FP9_web_galaxy_separator.py, b510eebfe; Y3) freezes phi on FRW: every cosmological
perturbation is infinitesimal and so below the yield y_th a0; the formal linearisation is GR + the BPS khronon and the linear
sigma_8 yardstick is exactly 1.  The physical web crosses the yield: FP9's physical-amplitude yardstick switches each mode's
MOND response on at y = y_th, and FP9 H2c reports z = 2 IGM lumps at delta ~ 10 switching on.  The response
x(y) = x_P2(y - y_th) is continuous at the yield but not differentiable (dx/dy ~ (y - y_th)^(-1/2)).  This lane asks whether
that non-differentiability produces a jump in G_eff, an ill-posed growth problem, or an instability.

THE OBJECTS.  (1) The plug block: FP7's unitary-gauge Minkowski block (committed det M, reproduced in XR18_yield_surface.py
K1) with phi removed (frozen by the yield): its roots and the static response (Cramer).  (2) The chord response the growth
yardstick uses, C^Q(y) = x(y)/y, and the tangent Q'' = dx/dy that small perturbations about an above-yield state feel.
(3) FP9's growth machinery (exec'd read-only up to its CONTROLS banner): the headline cell n = 2, L(0.25) = 1.3 Mpc,
y_th(0.25) = 1e-6, p' = 4, both footings; the per-mode fields along the growth solution, the crossing epochs; the yield
regularised, J_eps = J_P2 + 2 y_th (sqrt(Y + eps^2) - eps), eps -> 0.  (4) FP9 H2c's Gaussian lumps (comoving 0.1, 0.3,
1 Mpc/h), grown linearly to delta = 10 at z = 2: the epoch each crosses the yield, the chord G_eff through it, and the extra
Jeans e-folds of perturbations inside the lump from the tangent response.

PRE-DECLARED (written into this file before its first full run; exploratory runs are disclosed in XR18_README.md -- none was
made for this part beyond reading FP9's committed outputs)
 H1 [load-bearing] The FRW linearisation about the frozen phi is GR + BPS with E = alpha_c: both scalar roots of the block
    without phi are strictly positive (FP7's zero-field marginal root omega^2 = 0 is absent) and the static response is
    Psi/Psi_N = 1/(1 - alpha_c/2) exactly (G_eff = G_N, no slip term from phi).
 H2 [load-bearing] No jump in G_eff at the yield: the chord response C^Q(y) = x(y)/y is continuous at y_th (|C^Q(y_th + d) -
    C^Q(y_th - d)| -> 0 as d -> 0, fitted onset exponent 0.50 +- 0.02); the tangent diverges as (y - y_th)^(-0.50 +- 0.02).  On the
    headline cell's per-mode yardstick every sigma_8 and forest mode crosses the yield at most once (the field grows, y_th falls),
    and the chord G_eff is continuous through every crossing.
 H3 [load-bearing] The growth through the non-differentiable crossing is well posed: with the yield regularised,
    eps/sqrt(y_th) = 0.1, 0.01, 0.001, sigma_8 (canonical, rms and per-mode) and the forest proxy converge monotonically to
    FP9's eps = 0 values, within 1e-4 (sigma_8) and 1e-6 (forest, absolute) at 0.001; and sigma_8's sensitivity to a 1e-3
    change of the initial amplitude at eps = 0 is within a factor 2 of its value at eps/sqrt(y_th) = 0.1 (the non-Lipschitz
    point does not amplify perturbations of the growth).
 H4 [load-bearing] FP9's lumps (0.1, 0.3, 1 Mpc/h comoving, grown to delta = 10 at z = 2) cross the yield once; the chord
    G_eff - 1 rises continuously from 0 (onset ~ (t - t_c)^(1/2)); the tangent response adds a FINITE number of Jeans e-folds to
    perturbations inside the lump over z = 3 -> 1.5, fewer than 5 more than plain band-passed P2 on the same lump history
    (cold matter, and 1e4 K gas at k = 1/R, 3/R, 10/R), both footings -- no instability at the crossing.
The writer's expectation: all four pass.

CHECKS
  K1 CONTROL: FP9's machinery, exec'd read-only up to its CONTROLS banner, reproduces FP9's committed headline numbers exactly:
     sigma_8 (both footings, both yardstick modes), the forest proxy (k_F = 10, 15, 20), the 1e10/1e11 flagships, SPARC, KiDS.
  E1 = H1.  E2 = H2.  E3 = H3.  E4 = H4.
  E5 (reported) the fraction of the sigma_8 and forest modes that are above the yield at z = 3, 2, 1, 0.25, 0 (per-mode),
     and the chord G_eff - 1 of the linear web at those epochs.
  Development record (disclosed in XR18_README.md): E2's and E4's continuity tests first compared the step at a crossing with the
  largest step elsewhere on one grid; that proxy fails for a sqrt onset (seen first in XR18_state_separator.py's first run), so
  before E2's and E4's first main run both became refinement tests (the step must shrink under 10x refinement).  This file's
  first run was its MUTATE run; the hypotheses' text is unchanged.  After the first recorded main run only the VERDICT text was
  rewritten (it now prints the measured numbers and says which clause a FAIL rests on); MUTATE and main were re-run in that order.
MUTATE=1 replaces the yield's square-root onset by a hard switch (C^Q = (nu_P2 - 1) Theta(y - y_th): MOND jumps fully on at
the yield): E2 and E4 must FAIL (a jump in G_eff at every crossing), rc = 1.

SCOPE.  Linear growth with FP9's physical-amplitude yardstick (L341's growing-mode ICs); the lumps are linear-theory
Gaussians with a local Jeans estimate for their interior; no particle-mesh run.  kappa = 1/2 is FITTED (Z = 5.7888).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR18_frw_yield_crossing.py
"""
import os, sys, io, re, json, math, time, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.optimize import brentq
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR18_frw_yield_crossing"
T0 = time.time()
_OUTF = open(os.path.join(HERE, SLUG + ("_MUTATE.out" if MUTATE else ".out")), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _OUTF.write(s + "\n"); _OUTF.flush()


CH, OUT = [], {"lane": "XR18e", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}" if (ok or not MUTATE) else
          f"         reading (written for the unmutated theory; this MUTATE run fails the check):  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 112); P(t); P("=" * 112)


def el():
    return f"[{time.time() - T0:.0f} s]"


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the yield's square-root onset is replaced by a hard switch -- E2 and E4 must FAIL ***")

# ============================================================================================ FP9's machinery (read-only)
FP9 = os.path.join(REPO, "real_research", "derivation_chain_2026", "FP9_web_galaxy_separator.py")
_src9 = open(FP9).read()
NS9 = {"__file__": FP9, "__name__": "fp9_machinery"}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(_src9[:_src9.index('\nbanner("K  CONTROLS')], FP9, "exec"), NS9)
finally:
    if _old is None:
        os.environ.pop("MUTATE", None)
    else:
        os.environ["MUTATE"] = _old
M6 = NS9["M6"]; A0 = dict(NS9["A0"]); FOOTS, MODES = NS9["FOOTS"], NS9["MODES"]
YIELD = NS9["YIELD"]
bandpass_model, L_phys, y_th_z, law_dev_dex, kids_class = (NS9[k] for k in ("bandpass_model", "L_phys", "y_th_z", "law_dev_dex", "kids_class"))
growth_aq, s8_aq, forest_aq, LL_of, forest_proxy = (NS9[k] for k in ("growth_aq", "s8_aq", "forest_aq", "LL_of", "forest_proxy"))
x_P2, OmL_z, OmL_a, nu_p2, gfield = NS9["x_P2"], NS9["OmL_z"], NS9["OmL_a"], NS9["nu_p2"], NS9["gfield"]
KH, KHF, DI, DIF, sigma8_of, S8_LCDM = NS9["KH"], NS9["KHF"], NS9["DI"], NS9["DIF"], NS9["sigma8_of"], NS9["S8_LCDM"]
Z_KIDS, Z_FLAG = NS9["Z_KIDS"], NS9["Z_FLAG"]
G6, MPCm, RHOM0, h_, H0, Ez = M6["G6"], M6["MPCm"], NS9["RHOM0"], NS9["h_"], NS9["H0"], NS9["Ez"]
F9 = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP9_web_galaxy_separator_results.json")))["numbers"]
F7 = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP7_aqual_type_repair_results.json")))["numbers"]
P(f"\n  FP9's machinery exec'd read-only up to its CONTROLS banner (FP6 inside it); a0 = {A0['canonical']:.4e} / {A0['alt']:.4e}   {el()}")

# ============================================================================================ K1 FP9's headline
banner("K1  CONTROL: FP9's committed headline numbers, recomputed with its own machinery")
HEAD = dict(n=2.0, L25=1.3, pp=4.0, y25=1e-6)
KB = {f: kids_class(A0[f]) for f in FOOTS}


def floor_of(y25, pp):
    return (y25, pp, YIELD)


def hy_model(n, L25, pp, y25):
    return bandpass_model(LL_of(L25, n), n, yr=0.0, floor=floor_of(y25, pp))


def flag_hy(n, L25, pp, y25, foot, M=1e11, z=Z_FLAG):
    fl = floor_of(y25, pp)
    return law_dev_dex(M, A0[foot], 0.1, L_phys(LL_of(L25, n), n, 1 / (1 + z)), y_th_z(fl, z), YIELD)


modh = hy_model(HEAD["n"], HEAD["L25"], HEAD["pp"], HEAD["y25"])
LLh = LL_of(HEAD["L25"], HEAD["n"]); FLh = floor_of(HEAD["y25"], HEAD["pp"])
k1 = {"s8": {}, "forest": {}, "flag": {}, "sparc": {}, "kids": {}}
for f in FOOTS:
    for m in MODES:
        k1["s8"][str((f, m))] = s8_aq(modh, f, m)
        res_ = growth_aq(modh, A0[f], mode=m, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0))
        for kF in (10.0, 15.0, 20.0):
            k1["forest"][str((f, m, kF))] = forest_proxy(res_, kF=kF)[0]
    for Mv in (1e10, 1e11):
        k1["flag"][str((f, Mv))] = flag_hy(HEAD["n"], HEAD["L25"], HEAD["pp"], HEAD["y25"], f, M=Mv)
    L0h = L_phys(LLh, HEAD["n"], 1.0); y0h = y_th_z(FLh, 0.0)
    k1["sparc"][f] = max(abs(law_dev_dex(Mv, A0[f], yv_, L0h, y0h, YIELD)) for Mv in (1e9, 1e10, 1e11, 1e12) for yv_ in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0))
    k1["kids"][f] = kids_class(A0[f], HEAD["L25"], y_th_z(FLh, Z_KIDS), YIELD) - KB[f]
ref = F9["H2"]
devs = []
for grp in ("s8", "forest", "flag", "sparc", "kids"):
    for kk, v in k1[grp].items():
        rv = ref[grp][kk]
        devs.append(abs(v - rv) if rv == 0 else abs(v / rv - 1))
k1dev = max(devs)
P("    sigma_8/LCDM: " + ", ".join(f"{kk}: {v:.6f}" for kk, v in k1["s8"].items()) + ";  flagship: " + ", ".join(f"{kk}: {v:+.5f}" for kk, v in k1["flag"].items()))
P("    SPARC: " + ", ".join(f"{kk}: {v:.3e}" for kk, v in k1["sparc"].items()) + ";  KiDS: " + ", ".join(f"{kk}: {v:+.3f}" for kk, v in k1["kids"].items())
  + ";  forest (max): " + f"{max(k1['forest'].values()):.3e}")
check("K1 CONTROL: FP9's machinery, exec'd read-only, reproduces FP9's committed headline numbers -- sigma_8 (4), the forest proxy "
      "(12), the 1e10/1e11 flagships (4), SPARC (2), KiDS (2)", f"max relative deviation {k1dev:.1e} over {len(devs)} numbers",
      k1dev <= 1e-9)
OUT["numbers"]["K1"] = k1
P(f"    {el()}")

# ============================================================================================ E1 the plug block
banner("E1  THE FRW LINEARISATION ABOUT THE FROZEN phi: FP7's block with phi removed (the plug)")
tt_, xx_, yy_, zz_ = sp.symbols('t x y z', real=True)
X3m = (xx_, yy_, zz_)
eb = sp.Symbol('e_b')
alm, c2m, lmm = sp.symbols('alpha_c c_2 lambda', positive=True)
nf, pf, Bf, Sf = [sp.Function(s_)(tt_, xx_, yy_, zz_) for s_ in ('n', 'psi', 'B', 'S')]
Nl = sp.exp(eb * nf)
gam = sp.diag(*[sp.exp(-2 * eb * pf)] * 3)
gin = gam.inv()
Ni = [eb * (sp.diff(Bf, X3m[0]) + Sf), eb * sp.diff(Bf, X3m[1]), eb * sp.diff(Bf, X3m[2])]
Gm3 = [[[sum(gin[a_, d_] * (sp.diff(gam[d_, b_], X3m[c_]) + sp.diff(gam[d_, c_], X3m[b_]) - sp.diff(gam[b_, c_], X3m[d_])) for d_ in range(3)) / 2
         for c_ in range(3)] for b_ in range(3)] for a_ in range(3)]
DN = [[sp.diff(Ni[j], X3m[i]) - sum(Gm3[kq][i][j] * Ni[kq] for kq in range(3)) for j in range(3)] for i in range(3)]
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(gam[i, j], tt_) - DN[i][j] - DN[j][i]) / (2 * Nl))
Kup = gin * Kij * gin
KK = sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3))
trK = sum(gin[i, j] * Kij[i, j] for i in range(3) for j in range(3))


def Ric3(b_, c_):
    return sum(sp.diff(Gm3[a_][b_][c_], X3m[a_]) - sp.diff(Gm3[a_][b_][a_], X3m[c_]) +
               sum(Gm3[a_][a_][d_] * Gm3[d_][b_][c_] - Gm3[a_][c_][d_] * Gm3[d_][b_][a_] for d_ in range(3)) for a_ in range(3))


R3 = sum(gin[b_, c_] * Ric3(b_, c_) for b_ in range(3) for c_ in range(3))
ai = [sp.diff(sp.log(Nl), xi_) for xi_ in X3m]
aa = sum(gin[i, j] * ai[i] * ai[j] for i in range(3) for j in range(3))
# the plug: delta phi = 0 (frozen by the yield), so delta chi = 0 and the chassis and J contribute nothing at quadratic order
Lplug = Nl * sp.exp(-3 * eb * pf) * (KK - trK ** 2 + R3 + alm * aa - c2m * trK ** 2)
L2p = sp.expand((sp.diff(Lplug, eb, 2) / 2).subs(eb, 0))
ELp = euler_equations(L2p, [nf, pf, Bf, Sf], [tt_, xx_, yy_, zz_])
kq_, wq_ = sp.symbols('k omega', positive=True)
An, Ap, AB, AS = sp.symbols('A_n A_psi A_B A_S')
phs = sp.exp(sp.I * (kq_ * zz_ - wq_ * tt_))
ELk = [sp.expand(sp.simplify((e_.lhs - e_.rhs).subs({nf: An * phs, pf: Ap * phs, Bf: AB * phs, Sf: AS * phs}).doit() / phs)) for e_ in ELp]
Mp = sp.Matrix([[sp.expand(sp.diff(ELk[r_], v_)) for v_ in (Ap, An, AB)] for r_ in (1, 0, 2)])
detP = sp.factor(sp.expand(Mp.det(method='berkowitz')))
U2 = sp.Symbol('U2')
rootsP = [sp.factor(r_) for r_ in sp.solve(sp.numer(sp.together(detP.subs(wq_, sp.sqrt(U2) * kq_))), U2)]
UK = c2m * (2 - alm) / (alm * (2 + 3 * c2m))
roots_ok = len(rootsP) >= 1 and all(sp.simplify(r_ - UK) == 0 for r_ in rootsP)
# the static response to a conserved source (Cramer, omega -> 0): rows (psi, n, B), lapse source R, momentum -D R
Rs_ = sp.Symbol('R')
SC = sp.Matrix([0, Rs_, sp.I * wq_ * Rs_])
Mi = Mp.copy(); Mi[:, 0] = SC
psiC = sp.cancel(sp.expand(Mi.det(method='berkowitz')) / sp.expand(Mp.det(method='berkowitz')))
stat = sp.factor(sp.limit(psiC / (-Rs_ / (4 * kq_ ** 2)), wq_, 0))
stat_ok = sp.simplify(stat - 1 / (1 - alm / 2)) == 0
num_pos = all(float(UK.subs({alm: a_, c2m: c_})) > 0 for a_ in (9.62e-14, 3.2e-9) for c_ in (7.29e-3, 0.1))
P(f"    plug block det = {detP};  roots omega^2/k^2 = {rootsP};  static Psi/Psi_N = {stat}")
P(f"    (FP7's zero-field block with phi live had the roots {F7['B3']['zero_field_roots']}: the first is the marginal omega^2 = 0)")
check("E1 [H1, pre-declared] THE FRW LINEARISATION ABOUT THE FROZEN phi IS GR + BPS (E = alpha_c): with phi removed by the yield the "
      "scalar block's roots are the BPS khronon's omega^2/k^2 = c_2 (2 - alpha_c)/(alpha_c (2 + 3 c_2)) > 0 (strictly hyperbolic; FP7's "
      "marginal omega^2 = 0 is gone) and the static response is Psi/Psi_N = 1/(1 - alpha_c/2) = G_N/G exactly",
      f"roots {rootsP} == U_K: {roots_ok}; positive at both alpha_c ends and c_2 = 7.29e-3/0.1: {num_pos}; static {stat}: {stat_ok}",
      roots_ok and num_pos and stat_ok)
P(f"    {el()}")

# ============================================================================================ E2 no jump in G_eff
banner("E2  NO JUMP IN G_eff AT THE YIELD: the chord C^Q = x/y and the tangent dx/dy; the per-mode crossings of the headline cell")


def x_law(y, yth):
    y = np.asarray(y, float)
    if MUTATE:
        return np.where(y > yth, x_P2(y), 0.0)                           # hard switch: MOND fully on above the yield
    return x_P2(np.maximum(y - yth, 0.0))


for yth in (1e-6, 0.0025, 0.0141):
    pass
jumps = {}; onset = {}; tang = {}
for yth in (1e-6, 3.67e-5, 0.0025, 0.0141):
    dd = np.geomspace(1e-14, 1e-3, 80) * yth
    cq_up = x_law(yth + dd, yth) / (yth + dd); cq_dn = x_law(yth - dd, yth) / (yth - dd)
    jumps[yth] = float(np.max(np.abs(cq_up[:10] - cq_dn[:10])))
    good = cq_up > 0
    onset[yth] = float(np.polyfit(np.log(dd[good][:40]), np.log(cq_up[good][:40]), 1)[0]) if good.sum() > 5 else float("nan")
    xs = x_law(yth + dd, yth)
    tq = np.gradient(xs, dd)
    tang[yth] = float(np.polyfit(np.log(dd[5:40]), np.log(np.abs(tq[5:40]) + 1e-300), 1)[0])
P("    |C^Q(y_th + d) - C^Q(y_th - d)| for d <= 1e-13 y_th: " + ", ".join(f"y_th {k_:g}: {v:.2e}" for k_, v in jumps.items()))
P("    onset exponent of C^Q in (y - y_th): " + ", ".join(f"{k_:g}: {v:.4f}" for k_, v in onset.items())
  + ";  tangent exponent: " + ", ".join(f"{k_:g}: {v:.4f}" for k_, v in tang.items()))
# the per-mode yardstick along the headline growth solution (canonical and alt): crossings of y_k(a) = y_th(a)
if MUTATE:
    def cut_mut(y, a, yL=HEAD["y25"] * OmL_z(Z_KIDS) ** HEAD["pp"]):
        yth_a = yL * OmL_a(a) ** (-HEAD["pp"])
        return np.where(np.asarray(y, float) > yth_a, 1.0, 0.0)
    model_e = {"hfac": modh["hfac"], "cut": cut_mut, "yr": 0.0}
else:
    model_e = modh
cross = {}; geff_jump = {}
for f in FOOTS:
    for KHg, Dig, lab in ((KH, DI, "sigma8"), (KHF, DIF, "forest")):
        stp = {}
        for nep in (160, 1600):                              # continuity by refinement: a sqrt onset's step shrinks ~ sqrt(10); a jump does not
            ZS = np.geomspace(9.0, 0.02, nep)
            res = growth_aq(model_e, A0[f], mode="permode", KHg=KHg, Dig=Dig, zs_out=tuple(ZS))
            zz = np.array(sorted(res.keys(), reverse=True))
            Y = np.array([gfield(res[z_], 1 / (1 + z_), KHg) * model_e["hfac"](1 / (1 + z_), KHg) / A0[f] for z_ in zz])
            yth_a = np.array([y_th_z(FLh, z_) for z_ in zz])
            above = Y > yth_a[:, None]
            ncross = np.sum(np.abs(np.diff(above.astype(int), axis=0)), axis=0)
            if nep == 160:
                cross[f"{f}/{lab}"] = dict(max_crossings=int(ncross.max()), modes_crossing=int(np.sum(ncross > 0)), n_modes=int(len(KHg)))
            CQ = x_law(Y, yth_a[:, None]) / np.maximum(Y, 1e-300)
            hk = np.array([model_e["hfac"](1 / (1 + z_), KHg) for z_ in zz])
            steps = np.abs(np.diff(CQ * hk ** 2, axis=0))
            at_cross = np.abs(np.diff(above.astype(int), axis=0)) > 0
            stp[nep] = float(steps[at_cross].max()) if at_cross.any() else 0.0
        geff_jump[f"{f}/{lab}"] = dict(step_160=stp[160], step_1600=stp[1600], shrink=stp[160] / max(stp[1600], 1e-300))
for kk, v in cross.items():
    P(f"    {kk:18s}: modes crossing {v['modes_crossing']}/{v['n_modes']}, max crossings per mode {v['max_crossings']}; the chord G_eff's largest "
      f"step across a crossing: {geff_jump[kk]['step_160']:.3e} (160 epochs) -> {geff_jump[kk]['step_1600']:.3e} (1600), shrink x{geff_jump[kk]['shrink']:.2f}")
e2_ok = (max(jumps.values()) < 1e-5 and all(abs(v - 0.5) <= 0.02 for v in onset.values()) and all(abs(v + 0.5) <= 0.02 for v in tang.values())
         and all(v["max_crossings"] <= 1 for v in cross.values())
         and all(v["shrink"] >= 2.0 for v in geff_jump.values()))
check("E2 [H2, pre-declared] NO JUMP IN G_eff AT THE YIELD: the chord response is continuous (|C^Q(y_th + d) - C^Q(y_th - d)| -> 0), "
      "its onset exponent is 0.50 +- 0.02 and the tangent's -0.50 +- 0.02; on the headline cell's per-mode yardstick every mode "
      "crosses the yield at most once and the chord G_eff is continuous through every crossing (its largest step at a crossing "
      "shrinks >= 2x under 10x refinement of the epoch grid; a jump would not)",
      f"max jump {max(jumps.values()):.1e}; onset {[round(v, 4) for v in onset.values()]}; tangent {[round(v, 4) for v in tang.values()]}; "
      f"max crossings per mode {max(v['max_crossings'] for v in cross.values())}; step shrink under refinement "
      f"{min(v['shrink'] for v in geff_jump.values()):.2f}-{max(v['shrink'] for v in geff_jump.values()):.2f}", e2_ok,
      "G_eff switches on as sqrt(y - y_th): continuous, with an integrable (y - y_th)^(-1/2) slope -- a kink, not a jump.  The step test "
      "was written before E2's first main run; XR18_state_separator.py's first run had shown a one-grid step comparison is a poor "
      "continuity test for a sqrt onset (disclosed in XR18_README.md)")
OUT["numbers"]["E2"] = dict(jumps={str(k_): v for k_, v in jumps.items()}, onset={str(k_): v for k_, v in onset.items()},
                            tangent={str(k_): v for k_, v in tang.items()}, crossings=cross, steps=geff_jump)
P(f"    {el()}")

# ============================================================================================ E3 regularised yield
banner("E3  WELL-POSED GROWTH THROUGH THE CROSSING: the yield regularised (eps -> 0), and sigma_8's sensitivity to the initial amplitude")


def x_eps(y, yth, eps):
    y = np.asarray(y, float)
    lo = np.zeros_like(y); hi = np.full_like(y, 0.4999999)
    for _ in range(64):
        mid = 0.5 * (lo + hi)
        F = mid * mid / (1 - 2 * mid) + yth * mid / np.sqrt(mid * mid + eps * eps)
        up = F > y
        hi = np.where(up, mid, hi); lo = np.where(up, lo, mid)
    return 0.5 * (lo + hi)


yL_h = HEAD["y25"] * OmL_z(Z_KIDS) ** HEAD["pp"]


def model_eps(er):
    def cut(y, a):
        yth_a = yL_h * OmL_a(a) ** (-HEAD["pp"])
        y = np.maximum(np.asarray(y, float), 1e-300)
        return (x_eps(y, yth_a, er * math.sqrt(yth_a)) / y) / (nu_p2(y) - 1.0)
    return {"hfac": modh["hfac"], "cut": cut, "yr": 0.0}


ref0 = {m: (k1["s8"][str(("canonical", m))] if not MUTATE else s8_aq(model_e, "canonical", m)) for m in MODES}
f0 = k1["forest"][str(("canonical", "permode", 15.0))] if not MUTATE else forest_aq(model_e, "canonical", "permode", kFs=(15.0,))
e3 = {}
for er in (0.1, 0.01, 0.001):
    me = model_eps(er)
    e3[er] = dict(s8={m: s8_aq(me, "canonical", m) for m in MODES}, forest=forest_aq(me, "canonical", "permode", kFs=(15.0,)))
    P(f"    eps/sqrt(y_th) = {er:g}: sigma_8/LCDM rms {e3[er]['s8']['rms']:.7f}, per-mode {e3[er]['s8']['permode']:.7f}; forest {e3[er]['forest']:.3e}")
P(f"    eps = 0 ({'hard switch' if MUTATE else 'FP9'}): rms {ref0['rms']:.7f}, per-mode {ref0['permode']:.7f}; forest {f0:.3e}")
d_s8 = {er: max(abs(e3[er]["s8"][m] - ref0[m]) for m in MODES) for er in e3}
mono = all(d_s8[a_] >= d_s8[b_] - 1e-9 for a_, b_ in ((0.1, 0.01), (0.01, 0.001)))


def sens(model):
    base = growth_aq(model, A0["canonical"], mode="permode")[0.0]
    up = NS9["growth_aq"](model, A0["canonical"], mode="permode", Dig=DI * (1 + 1e-3))[0.0]
    return (sigma8_of(up) / sigma8_of(base) - 1) / 1e-3


s_0 = sens(model_e); s_e = sens(model_eps(0.1))
e3_ok = d_s8[0.001] < 1e-4 and abs(e3[0.001]["forest"] - f0) < 1e-6 and mono and 0.5 <= s_0 / s_e <= 2.0
check("E3 [H3, pre-declared] THE GROWTH THROUGH THE NON-DIFFERENTIABLE CROSSING IS WELL POSED: the regularised yield converges "
      "monotonically to FP9's eps = 0 sigma_8 (within 1e-4 at eps/sqrt(y_th) = 1e-3) and forest proxy (within 1e-6), and sigma_8's "
      "sensitivity to the initial amplitude at eps = 0 is within a factor 2 of the smooth (eps/sqrt(y_th) = 0.1) value",
      f"|d sigma_8| at 0.1/0.01/0.001: {d_s8[0.1]:.1e}/{d_s8[0.01]:.1e}/{d_s8[0.001]:.1e} (monotone {mono}); forest diff "
      f"{abs(e3[0.001]['forest'] - f0):.1e}; d ln sigma_8/d ln A: eps = 0 {s_0:.4f}, smooth {s_e:.4f}", e3_ok)
OUT["numbers"]["E3"] = {str(er): v for er, v in e3.items()}
OUT["numbers"]["E3"]["sensitivity"] = [s_0, s_e]
P(f"    {el()}")

# ============================================================================================ E4 FP9's lumps crossing the yield
banner("E4  FP9's LUMPS THROUGH THE YIELD: chord G_eff, the crossing epoch, and the tangent Jeans e-folds inside the lump")
gfr = M6["gfrac_smooth"]
Dz = growth_aq(NS9["M6"]["lcdm_model"](), A0["canonical"], mode="permode", zs_out=tuple(np.linspace(0.5, 4.0, 141)))
zD = np.array(sorted(Dz.keys())); Dlin = np.array([float(np.mean(Dz[z_] / DI)) for z_ in zD])     # linear growth factor (k-independent in LCDM)
D_at = lambda z: float(np.interp(z, zD, Dlin))
KB_ = 1.380649e-23; MP_ = 1.67262e-27; CS4 = math.sqrt(KB_ * 1e4 / (0.6 * MP_))
Hphys = lambda z: H0 * Ez(1 / (1 + z))


def lump_state(z, Rc, foot, dl2=10.0, plain=False):
    """peak band-passed field y (a0 units), chord G_eff - 1 = max phantom/g_N, tangent dx/dy there, lump density."""
    a0 = A0[foot]; dl = dl2 * D_at(z) / D_at(2.0)
    Lz = L_phys(LLh, HEAD["n"], 1 / (1 + z)) * MPCm; yt = y_th_z(FLh, z)
    rhob = RHOM0 * (1 + z) ** 3
    sg = Rc / h_ / (1 + z) * MPCm
    Ml = dl * rhob * (2 * math.pi) ** 1.5 * sg ** 3
    r_ = np.geomspace(0.05, 5, 400) * sg
    gN_ = G6 * Ml * gfr(r_ / sg) / r_ ** 2
    gbp_ = G6 * Ml * (gfr(r_ / sg) - gfr(r_ / math.sqrt(sg ** 2 + Lz ** 2))) / r_ ** 2
    ybp = gbp_ / a0
    if plain:
        xs = x_P2(ybp); dxdy = (2 * ybp + 1) / (2 * np.sqrt(ybp ** 2 + ybp)) - 1
    else:
        xs = x_law(ybp, yt)
        D_ = np.maximum(ybp - yt, 1e-300)
        dxdy = np.where(ybp > yt, (2 * D_ + 1) / (2 * np.sqrt(D_ ** 2 + D_)) - 1, 0.0)
        if MUTATE:
            dxdy = np.where(ybp > yt, (2 * ybp + 1) / (2 * np.sqrt(ybp ** 2 + ybp)) - 1, 0.0)
    j = int(np.argmax(ybp))
    return dict(y=float(ybp[j]), yth=yt, chord=float(np.max(xs * a0 / gN_)), tang=float(dxdy[j]), rho=(1 + dl) * rhob, sigma=sg)


e4 = {}
zgrid = np.linspace(3.0, 1.5, 3001)
for foot in FOOTS:
    for Rc in (0.1, 0.3, 1.0):
        st = [lump_state(z, Rc, foot) for z in zgrid]
        stp = [lump_state(z, Rc, foot, plain=True) for z in zgrid]
        above = np.array([s["y"] > s["yth"] for s in st])
        ncr = int(np.sum(np.abs(np.diff(above.astype(int)))))
        chord = np.array([s["chord"] for s in st])
        jc = int(np.argmax(above)) if above.any() else None
        # continuity by refinement: the chord's step across the crossing on local grids of spacing 5e-4 and 5e-5 in z
        stp4 = {}
        if jc:
            zc_ = float(zgrid[jc])
            for dzl in (5e-4, 5e-5):
                zl = np.arange(zc_ + 20 * dzl, zc_ - 20 * dzl, -dzl)
                ch_l = np.array([lump_state(z_, Rc, foot)["chord"] for z_ in zl])
                ab_l = np.array([(lambda s_: s_["y"] > s_["yth"])(lump_state(z_, Rc, foot)) for z_ in zl])
                jl = int(np.argmax(ab_l)) if ab_l.any() else 1
                stp4[dzl] = float(np.abs(ch_l[jl] - ch_l[jl - 1]))
        stepc = stp4.get(5e-4, 0.0); stepo = stp4.get(5e-5, 0.0)
        # tangent Jeans e-folds over z = 3 -> 1.5: Gamma^2 = 4 pi G rho (1 + Q'') - c_s^2 k^2 (cold: c_s = 0)
        tgrid = np.array([-1.0 / Hphys(z) for z in zgrid])                 # d t = -dz/((1+z) H); integrate in z
        rows = {}
        for lab, cs in (("cold", 0.0), ("1e4K", CS4)):
            for kf in (1.0, 3.0, 10.0):
                def efolds(states):
                    tot = 0.0
                    for i in range(len(zgrid) - 1):
                        s0, s1 = states[i], states[i + 1]
                        k_ = kf / s0["sigma"]
                        g2a = 4 * math.pi * G6 * s0["rho"] * (1 + s0["tang"]) - cs ** 2 * k_ ** 2
                        g2b = 4 * math.pi * G6 * s1["rho"] * (1 + s1["tang"]) - cs ** 2 * k_ ** 2
                        dtz = abs(zgrid[i + 1] - zgrid[i]) / ((1 + 0.5 * (zgrid[i] + zgrid[i + 1])) * Hphys(0.5 * (zgrid[i] + zgrid[i + 1])))
                        tot += 0.5 * (math.sqrt(max(g2a, 0)) + math.sqrt(max(g2b, 0))) * dtz
                    return tot
                newton = [dict(s, tang=0.0) for s in st]
                rows[f"{lab}/{kf:g}"] = dict(HY=efolds(st), P2=efolds(stp), N=efolds(newton))
        e4[f"{foot}/{Rc}"] = dict(crossings=ncr, z_cross=float(zgrid[jc]) if jc else None, step_coarse=stepc, step_fine=stepo,
                                  shrink=stepc / max(stepo, 1e-300),
                                  chord_end=float(chord[-1]), efolds=rows)
for kk, v in e4.items():
    P(f"    lump {kk:16s}: crossings {v['crossings']}, z_c = {v['z_cross']:.4f}, chord G_eff - 1 step across the crossing {v['step_coarse']:.2e} "
      f"(dz = 5e-4) -> {v['step_fine']:.2e} (5e-5), shrink x{v['shrink']:.2f}; at z = 1.5 {v['chord_end']:.2f}; e-folds z = 3 -> 1.5 (H_Y / plain P2 / Newton): " +
      "; ".join(f"{k_}: {r['HY']:.2f}/{r['P2']:.2f}/{r['N']:.2f}" for k_, r in v["efolds"].items()))
extra = max(r["HY"] - r["P2"] for v in e4.values() for r in v["efolds"].values())
e4_ok = (all(v["crossings"] == 1 for v in e4.values()) and all(v["shrink"] >= 2.0 for v in e4.values())
         and extra < 5.0 and all(np.isfinite(r["HY"]) for v in e4.values() for r in v["efolds"].values()))
check("E4 [H4, pre-declared] FP9's LUMPS CROSS THE YIELD ONCE WITH NO JUMP AND NO INSTABILITY: each (0.1, 0.3, 1 Mpc/h; grown to delta = "
      "10 at z = 2) crosses once; the chord G_eff is continuous through it (its step across the crossing shrinks >= 2x from dz = 5e-4 to "
      "5e-5; a jump would not); the tangent response's extra Jeans e-folds over plain band-passed P2 are finite and < 5 (cold, "
      "1e4 K gas; k = 1, 3, 10 /R; both footings)",
      f"crossings {[v['crossings'] for v in e4.values()]}; step shrink under refinement {min(v['shrink'] for v in e4.values()):.2f}-{max(v['shrink'] for v in e4.values()):.2f}; "
      f"max extra e-folds over plain P2 {extra:.2f}", e4_ok,
      "the tangent's (t - t_c)^(-1/2) spike is integrable in time; the lump's own growth follows the continuous chord")
OUT["numbers"]["E4"] = e4
P(f"    {el()}")

# ============================================================================================ E5 (reported)
res5 = growth_aq(model_e, A0["canonical"], mode="permode", KHg=KHF, Dig=DIF, zs_out=(3.0, 2.0, 1.0, 0.25))
e5 = {}
for z_ in (3.0, 2.0, 1.0, 0.25, 0.0):
    a_ = 1 / (1 + z_)
    Y = gfield(res5[z_], a_, KHF) * model_e["hfac"](a_, KHF) / A0["canonical"]
    yt = y_th_z(FLh, z_)
    CQ = x_law(Y, yt) / np.maximum(Y, 1e-300)
    e5[str(z_)] = dict(frac_above=float(np.mean(Y > yt)), Geff_max=float(np.max(CQ * model_e["hfac"](a_, KHF) ** 2)),
                       k_first_above=float(KHF[np.argmax(Y > yt)]) if (Y > yt).any() else None)
P("    per-mode (forest grid 0.02-100 h/Mpc, canonical): " + "; ".join(
    f"z = {k_}: above-yield fraction {v['frac_above']:.2f}, max chord G_eff - 1 {v['Geff_max']:.3g}" for k_, v in e5.items()))
check("E5 (reported) the linear web's modes above the yield by epoch (per-mode yardstick) and their chord G_eff", e5, True, load_bearing=False)
OUT["numbers"]["E5"] = e5

# ============================================================================================ verdict
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
_e2_thr_only = (not OUT['checks']['E2']['pass'] and all(abs(v - 0.5) <= 0.02 for v in onset.values()) and all(abs(v + 0.5) <= 0.02 for v in tang.values())
                and all(v['max_crossings'] <= 1 for v in cross.values()) and all(v['shrink'] >= 2.0 for v in geff_jump.values()))
_e3_forest_only = (not OUT['checks']['E3']['pass'] and d_s8[0.001] < 1e-4 and mono and 0.5 <= s_0 / s_e <= 2.0)
banner("VERDICT")
_ok = {k_: OUT['checks'][k_]['pass'] for k_ in ('E1', 'E2', 'E3', 'E4')}
_pf = {k_: ('PASS' if v else 'FAIL') for k_, v in _ok.items()}
_t_e1 = ("On FRW the frozen phi leaves GR + BPS: FP7's marginal zero-field mode is gone" if _ok['E1']
         else "The FRW linearisation about the frozen phi is NOT GR + BPS")
_t_e2 = (f"onset exponent of the chord {min(onset.values()):.4f}-{max(onset.values()):.4f}, tangent {min(tang.values()):.4f}-{max(tang.values()):.4f}, at most "
         f"{max(v['max_crossings'] for v in cross.values())} crossing per mode, the chord's step at a crossing shrinks "
         f"x{min(v['shrink'] for v in geff_jump.values()):.2f}-{max(v['shrink'] for v in geff_jump.values()):.2f} under 10x refinement")
_n_e2 = (" -- on its absolute threshold only: the chord at d = 1.8e-13 y_th is " + format(max(jumps.values()), '.1e')
         + " = O(sqrt(d)/y_th) at y_th = 1e-6, not < 1e-5" if _e2_thr_only else "")
_t_e3 = (f"sigma_8 {'converges monotonically' if mono else 'does NOT converge monotonically'} as the yield is regularised "
         f"(|d sigma_8| {d_s8[0.1]:.1e}/{d_s8[0.01]:.1e}/{d_s8[0.001]:.1e} at eps/sqrt(y_th) = 0.1/0.01/0.001), d ln sigma_8/d ln A {s_0:.4f} "
         f"(eps = 0) vs {s_e:.4f} (smooth); forest proxy at the three eps {e3[0.1]['forest']:.1e}/{e3[0.01]['forest']:.1e}/{e3[0.001]['forest']:.1e} "
         f"vs {f0:.1e} at eps = 0")
_n_e3 = (" -- on its forest tolerance 1e-6 only: the regularised plug leaks x ~ eps y/y_th below the yield, so the forest proxy "
         "converges linearly in eps" if _e3_forest_only else "")
_t_e4 = ("FP9's z ~ 2 lumps switch on once, continuously, and the tangent's divergence adds a finite number of Jeans e-folds" if _ok['E4']
         else "FP9's z ~ 2 lumps do NOT switch on continuously (or add unbounded e-folds)")
_t_end = ("No jump in G_eff and no instability at the crossing on the tested yardsticks." if (_ok['E4'] and (_ok['E2'] or _e2_thr_only))
          else "A jump in G_eff or an instability at the crossing is NOT excluded by these runs.")
P(f"""  (e) {_t_e1} (E1: {_pf['E1']}).  Where the web crosses the yield: {_t_e2}
      (E2: {_pf['E2']}{_n_e2});
      {_t_e3} (E3: {_pf['E3']}{_n_e3});
      {_t_e4} (E4: {_pf['E4']}).
      {_t_end}
  Not 'closed'.  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}.  Time {time.time() - T0:.0f} s.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"  wrote {os.path.basename(fn)}")
_OUTF.close()
sys.exit(1 if nlb else 0)
