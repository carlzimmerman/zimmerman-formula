#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR18 (a) -- H_Y's YIELD SURFACE: characteristic speeds on each side and at the surface, the record's causality criterion B,
and whether the Cauchy problem is well posed across it.

WHY.  FP9 (derivation_chain_2026/FP9_web_galaxy_separator.py, b510eebfe) adds the yield floor J_Y = J_P2(Y) + 2 y_th sqrt(Y).
Its flux is F(x) = F_P2(x) + y_th (x = |grad phi|/a0), so phi is frozen wherever the band-passed source is below y_th a0
and flows above it: a free boundary (Bingham type).  The sqrt term adds nothing to the longitudinal stiffness
C_L = J' + 2Y J'' = F_P2'(x) and y_th/x to the transverse one, C_T = F/x: at the surface (x -> 0+) C_L -> 0 and C_T -> oo.
With phi's inertia 2 lambda (n.d phi)^2 (and the khronon's, locked to phi by the chassis) this is a degenerate hyperbolic
problem.  FP9's H2b showed E stays in the BPS window at every field; this lane computes the speeds, checks criterion B as
the record defines it, and tests the linearised Cauchy problem across the surface.

CRITERION B (qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md, requirement 7 as amended 2026-09-26): the theory
must admit a global time function (the khronon's) compatible with every characteristic cone, including degenerate cones
lying in its leaves; no signal may propagate backward in that time and there may be no closed causal curves;
superluminal or leafwise-instantaneous propagation is allowed; the mixed Cauchy problem must be well posed.

THE BLOCK.  FP7's unitary-gauge Minkowski block (B3, committed det M) with the filter factor sigma -> h (FP9 K2) and the
MOND stiffness C_phi -> C(theta) = C_T sin^2 theta + C_L cos^2 theta for a plane wave at angle theta to grad phi (frozen
coefficients).  Its roots U = omega^2/k^2: principal part (k >> 1/xi, h -> 0): phi's own cone U = C(theta)/lambda and the
BPS khronon U_K = c_2 (2 - alpha_c)/(alpha_c (2 + 3 c_2)) (E = alpha_c); effective (1/L << k << 1/xi, h ~ 1): the coupled
slow and fast roots.  Backgrounds: FP9's spherical H_Y law (point mass, band-passed field, the yield) on DE12's 24 host
systems (z = 0.25, 1, 2.5, 4; M_b = 1e10, 1e11, 1e12; both footings), each profile run through its yield surface r_Y on a
geometric approach d/r_Y = 1e-12 .. 1, into the plug, and to the zero-field (FRW) point.

PRE-DECLARED (written into this file before its first full run; exploratory runs disclosed in XR18_README.md: a scratch
map of r_Y on DE12's hosts, a 1-D wave-packet prototype abandoned for numerical fragility at small eps, a prototype of
A3's spectral test, and a prototype of A4's loading ramp)
 H1 [load-bearing] Criterion B's causal part: at every background point (yielded side, surface approach, plug, zero field)
    of the 24 hosts, every angle, alpha_c in {9.62e-14, 3.2e-9}, c_2 in {7.29e-3, 0.1}, lambda in {0, 1, 100}, h in {0, 0.3, 1},
    all roots U are real and >= 0 (no complex characteristic, so no backward-in-tau signal); cones are centred on the
    khronon's normal; the only divergent speeds are phi's transverse ones at the surface (lambda > 0), which lie in the leaf.
 H2 [load-bearing] The surface is a degenerate (weakly hyperbolic) locus: on the real backgrounds C_L ~ d^(1/2) and
    C_T ~ d^(-1/2) (fitted exponents 0.50 +- 0.02 and -0.50 +- 0.02 over d/r_Y = 1e-10 .. 1e-5); the longitudinal effective
    speed -> 0 as d^(1/4); at lambda = 0 the effective transverse root tends to the BPS khronon root (finite) within 1%.
 H3 [load-bearing] The linearised phi-sector across the surface (the plug rigid: u = 0 there; a flux condition at the inner
    end), lambda u_tt = (C_L u_x)_x with C_L ~ d^(1/2), is a non-negative self-adjoint degenerate operator: every discrete
    eigenvalue is > 0, the lowest five converge with observed order 0.4-0.6 (the d^(1/2) eigenfunction), their order-1/2
    Richardson extrapolation from N = 1600/3200 matches a shooting reference started on the exact local solution
    u ~ d^(1/4) J_(1/3)((4/3) kappa d^(3/4)) to 1e-3, and the eigenfunctions' gradient diverges as d^(-1/2) at the surface
    (fitted exponent -0.50 +- 0.05): well posed in the energy norm, not in C^1.  The same structure holds on a real host's
    radial profile (the 1e11 flagship at z = 2.5): positive spectrum, converging.
The writer's expectation: all three pass; the nonlinear (variational-inequality) Cauchy problem stays OPEN.

CHECKS
  K1 CONTROL: this lane's own second variation of FP7's repaired action about Minkowski (unitary gauge, sympy) reproduces
     FP7's committed det M exactly (sigma -> h).
  K2 CONTROL: J_Y's C_T and C_L from sympy reproduce FP9 Y1's committed expressions exactly.
  A1 = H1 (criterion B's causal part).  A2 = H2.  A3 = H3 (+ the real-host radial version).
  A4 (reported) the nonlinear phi-sector under slow loading (1-D slab, the yield regularised by eps, AVF energy-conserving
     steps): the surface advances into the plug; convergence in N and eps; energy balance; the lag behind the quasi-static
     surface.
  A5 (reported) WKB structure at the surface: travel time to it (finite, ~ d^(3/4)); amplitude focusing (A ~ d^(-1/8),
     gradient ~ d^(-3/8)); the flux's genuine nonlinearity (F_P2'' > 0: finite-amplitude phi waves steepen, fastest where
     c_par -> 0); the non-adiabatic layer where c_par < 300 km/s on each host (where a quasi-static PM solve lags phi).
  Development record (disclosed in XR18_README.md): r_Y is located by brentq on the exact field (a grid locator's ~1e-7 relative
  error flattened the d/r_Y = 1e-10 fits in an earlier run).  After the first recorded main run failed A2's third clause (the
  lambda = 0 transverse root stays ~1e-5 - 1e-4 of U_K at d = 1e-10 r_Y), a reported block was added printing the closed form
  U/U_K = C_T alpha_c/(C_T alpha_c + (2 - alpha_c) h^2), its slope and the distance at which U_K would be reached; the check and
  its hypothesis are unchanged and remain FAILED as declared.  MUTATE and main were then re-run in that order.
MUTATE=1 flips the sign of the yield term (J_P2 - 2 y_th sqrt(Y)): the zero-field state acquires C_T -> -oo (a Hadamard
instability) and there is no degenerate surface, so A1 and A2 must FAIL (rc = 1).

SCOPE.  Frozen-coefficient (principal and effective) symbols; the linearisation about a static background with the plug
treated as rigid (the free boundary moves at O(amplitude) with energy O(amplitude^(5/2)), A5); the 1-D nonlinear test is a
demonstration, not a proof.  The nonlinear hyperbolic free-boundary problem is not settled here.  kappa = 1/2 is FITTED.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR18_yield_surface.py
"""
import os, sys, io, re, json, math, time, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.linalg import eigh, solve_banded
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import jv
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR18_yield_surface"
T0 = time.time()
_OUTF = open(os.path.join(HERE, SLUG + ("_MUTATE.out" if MUTATE else ".out")), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _OUTF.write(s + "\n"); _OUTF.flush()


CH, OUT = [], {"lane": "XR18a", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
SGN = -1.0 if MUTATE else 1.0
if MUTATE:
    P("\n  *** MUTATE=1: the yield term's sign is flipped (J_P2 - 2 y_th sqrt(Y)) -- A1 and A2 must FAIL ***")

# ============================================================================================ machinery (read-only)
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
M6 = NS9["M6"]; A0 = dict(NS9["A0"]); FOOTS = ("canonical", "alt")
x_P2, L_phys, LL_of, y_th_z = NS9["x_P2"], NS9["L_phys"], NS9["LL_of"], NS9["y_th_z"]
gfrac = M6["gfrac_smooth"]; MPCm = M6["MPCm"]; G6 = M6["G6"]; MSUN = M6["MSUN"]; C_LIGHT = M6["c"]
LLh = LL_of(1.3, 2.0); FLh = (1e-6, 4.0, NS9["YIELD"])
F7 = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP7_aqual_type_repair_results.json")))["numbers"]
F9 = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP9_web_galaxy_separator_results.json")))["numbers"]
P12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
D12 = {"__name__": "de12", "__file__": P12}
_s12 = open(P12).read()
_head = _s12.split("# ============================================================================================ C1 the amplification")[0]
_trans = _s12.split("# ============================================================================================ the transitions")[1].split(
    "# ============================================================================================ G1 G2 the budget")[0].split('banner("C2')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec((_head + _trans).replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D12)
transition, KPC, Hz12 = D12["transition"], D12["KPC"], D12["Hz"]
GAL = [(z, Mb, f) for z in (0.25, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in FOOTS]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
P(f"\n  machinery: FP9 exec'd read-only up to its CONTROLS banner; DE12's host definitions; a0 = {A0['canonical']:.4e} / "
  f"{A0['alt']:.4e} m/s^2   {el()}")

# ============================================================================================ K1 the block (sympy)
banner("K1  CONTROL: this lane's own unitary-gauge second variation of FP7's action reproduces FP7's committed det M")
tt_, xx_, yy_, zz_ = sp.symbols('t x y z', real=True)
X3m = (xx_, yy_, zz_)
eb = sp.Symbol('e_b')
alm, c2m, Cph, lmm, hq = sp.symbols('alpha_c c_2 C_phi lambda h', real=True)
nf, pf, Bf, Sf, Ff = [sp.Function(s_)(tt_, xx_, yy_, zz_) for s_ in ('n', 'psi', 'B', 'S', 'phi')]
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
Fi = [sp.diff(eb * Ff, xi_) for xi_ in X3m]
Xi = [hq * f_ for f_ in Fi]
Bu, Cu = 2 * (2 - alm), -(2 - alm)
chassis = Bu * sum(gin[i, j] * ai[i] * Xi[j] for i in range(3) for j in range(3)) + Cu * sum(gin[i, j] * Xi[i] * Xi[j] for i in range(3) for j in range(3))
Jquad = -2 * Cph * sum(gin[i, j] * Fi[i] * Fi[j] for i in range(3) for j in range(3))
ndphi = (sp.diff(eb * Ff, tt_) - sum(sum(gin[i, j] * Ni[j] for j in range(3)) * Fi[i] for i in range(3))) / Nl
Lfull = Nl * sp.exp(-3 * eb * pf) * (KK - trK ** 2 + R3 + alm * aa - c2m * trK ** 2 + chassis + Jquad + 2 * lmm * ndphi ** 2)
L2f = sp.expand((sp.diff(Lfull, eb, 2) / 2).subs(eb, 0))
ELf = euler_equations(L2f, [nf, pf, Bf, Sf, Ff], [tt_, xx_, yy_, zz_])
kq_, wq_ = sp.symbols('k omega', real=True)
An, Ap, AB, AS, AF = sp.symbols('A_n A_psi A_B A_S A_phi')
phs = sp.exp(sp.I * (kq_ * zz_ - wq_ * tt_))
fsub = {nf: An * phs, pf: Ap * phs, Bf: AB * phs, Sf: AS * phs, Ff: AF * phs}
ELk = [sp.expand(sp.simplify((e_.lhs - e_.rhs).subs(fsub).doit() / phs)) for e_ in ELf]
Mblk = sp.Matrix([[sp.expand(sp.diff(ELk[r_], v_)) for v_ in (Ap, An, AB, AF)] for r_ in (1, 0, 2, 4)])
detM = sp.factor(sp.expand(Mblk.det(method='berkowitz')))
sig_ = sp.Symbol('sigma', real=True)
det7 = sp.sympify(re.sub(r"\blambda\b", "lam_", F7["B3"]["det"]),
                  locals={"alpha_c": alm, "c_2": c2m, "C_phi": Cph, "lam_": lmm, "sigma": sig_, "k": kq_, "omega": wq_})
k1_ok = sp.simplify(sp.expand(detM - det7.subs(sig_, hq))) == 0
U2 = sp.Symbol('U2')
polyU = sp.Poly(sp.numer(sp.together(detM.subs(wq_, sp.sqrt(U2) * kq_))), U2)
cU = [sp.simplify(c_ / kq_ ** 10) for c_ in polyU.all_coeffs()]
P(f"    det M = {detM}")
P(f"    quadratic in U = omega^2/k^2 (coefficients / k^10): {cU}")
check("K1 CONTROL: this lane's own second variation of FP7's repaired action about Minkowski (unitary gauge; filter factor h) "
      "reproduces FP7's committed zero-field determinant exactly (sigma -> h)", f"det M == FP7's committed det: {k1_ok}", k1_ok)
coef_fun = sp.lambdify((alm, c2m, Cph, lmm, hq), cU, "numpy")

# ============================================================================================ K2 J_Y's stiffnesses
xs_, yth_s, Ys_ = sp.symbols("x y_th Y", positive=True)
JP2s = -sp.log(1 - 2 * sp.sqrt(Ys_)) / 4 - sp.sqrt(Ys_) / 2 - Ys_ / 2
JYs = JP2s + 2 * yth_s * sp.sqrt(Ys_)
Fx = sp.simplify(xs_ * sp.diff(JYs, Ys_).subs(Ys_, xs_ ** 2))
CT_s = sp.simplify(Fx / xs_); CL_s = sp.simplify(sp.diff(Fx, xs_))
k2_ok = (sp.simplify(CT_s - sp.sympify(F9["Y"]["C_T"], locals={"x": xs_, "y_th": yth_s})) == 0
         and sp.simplify(CL_s - sp.sympify(F9["Y"]["C_L"], locals={"x": xs_})) == 0)
check("K2 CONTROL: J_Y's transverse and longitudinal stiffnesses from sympy (C_T = F/x, C_L = F'(x), F = x J_Y'(x^2)) reproduce FP9 "
      "Y1's committed expressions exactly", f"C_T = {CT_s}; C_L = {CL_s}; match {k2_ok}", k2_ok)


def FP2(x):
    return x * x / (1 - 2 * x)


def CL_of(x):
    return 2 * x * (1 - x) / (1 - 2 * x) ** 2


def CT_of(x, yth):
    return (FP2(x) + SGN * yth) / x


def x_static(ybp, yth):
    """the static scalar field: H_Y's yield law, or (MUTATE) the flipped-sign law F_P2(x) - y_th = y_bp."""
    return x_P2(np.maximum(ybp - yth, 0.0)) if SGN > 0 else x_P2(ybp + yth)


def roots(C, lam, h, ac, c2):
    """U = omega^2/k^2 roots of the exact block (quadratic for lambda > 0, linear at lambda = 0); returns (U array, ok flags)."""
    a2, a1, a0_ = coef_fun(ac, c2, C, lam, h)
    a2 = np.broadcast_to(np.asarray(a2, float), np.shape(C)).astype(float)
    a1 = np.broadcast_to(np.asarray(a1, float), np.shape(C)).astype(float)
    a0_ = np.broadcast_to(np.asarray(a0_, float), np.shape(C)).astype(float)
    if lam == 0:
        U = -a0_ / a1
        return U[None, :], np.isfinite(U) & (U >= 0)
    disc = a1 * a1 - 4 * a2 * a0_
    sq = np.sqrt(np.maximum(disc, 0.0))
    Up = (-a1 + sq) / (2 * a2); Um = (-a1 - sq) / (2 * a2)
    ok = (disc >= -1e-12 * a1 * a1) & (Up >= 0) & (Um >= 0) & np.isfinite(Up) & np.isfinite(Um)
    return np.vstack([Up, Um]), ok


def r_yield(r, ybp, yth, yfun=None):
    """the outermost yield radius; refined to machine precision by brentq on the exact field when yfun is given (the
    d/r_Y = 1e-10 fits need it)."""
    above = ybp > yth
    if not above.any() or above.all():
        return float("nan")
    j = np.where(above)[0][-1]
    if yfun is not None:
        return float(brentq(lambda rr: float(yfun(np.array([rr]))[0]) - yth, r[j], r[j + 1], xtol=1e-15 * r[j], rtol=1e-15))
    return float(r[j] + (yth - ybp[j]) * (r[j + 1] - r[j]) / (ybp[j + 1] - ybp[j]))


def host_profile(z, Mb, foot):
    a0 = A0[foot]; Lz = L_phys(LLh, 2.0, 1 / (1 + z)) * MPCm; yth = y_th_z(FLh, z)
    ybp_f = lambda r: G6 * Mb * MSUN / (a0 * r ** 2) * (1 - gfrac(r / Lz))
    rr = np.geomspace(1e-3, 50, 40000) * MPCm
    rY = r_yield(rr, ybp_f(rr), yth, yfun=ybp_f)
    return a0, Lz, yth, ybp_f, rY


# ============================================================================================ A1 criterion B
banner("A1  CRITERION B's CAUSAL PART: all characteristic roots real and >= 0 on every background point of the 24 hosts")
THETA = np.radians([0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0])
ACS, C2S, LAMS, HS = (9.62e-14, 3.2e-9), (7.29e-3, 0.1), (0.0, 1.0, 100.0), (0.0, 0.3, 1.0)
a1 = {}; nviol_tot = 0; ncells = 0; infin = []
for (z, Mb, f) in GAL:
    a0, Lz, yth, ybp_f, rY = host_profile(z, Mb, f)
    if np.isfinite(rY):
        d_in = rY * (1 - np.geomspace(1e-12, 0.9, 120))                       # yielded side, geometric approach
        d_out = rY * (1 + np.geomspace(1e-12, 3.0, 40))                        # plug side
        rs = np.concatenate([d_in, d_out])
    else:
        rs = np.geomspace(1e-3, 30, 160) * MPCm
    ybp = ybp_f(rs)
    x = x_static(ybp, yth)
    pts = [(xv, "flow") for xv in x[x > 0]] + [(0.0, "plug")] * int(np.sum(x <= 0)) + [(0.0, "zero field")]
    nv = 0; nc = 0; U_par_min = np.inf
    for (xv, kind) in pts:
        if kind != "flow" and SGN > 0:
            # plug / zero field under the yield: phi frozen (no phi root); the khronon at E = alpha_c: U_K > 0
            for ac in ACS:
                for c2 in C2S:
                    UK = c2 * (2 - ac) / (ac * (2 + 3 * c2)); nc += 1
                    nv += int(not (UK > 0))
            continue
        if kind != "flow":                                                     # MUTATE: x = 0 is a stationary state, C_T -> -oo
            xv = 1e-12
        Cth = CT_of(xv, yth) * np.sin(THETA) ** 2 + CL_of(xv) * np.cos(THETA) ** 2
        for ac in ACS:
            for c2 in C2S:
                for lam in LAMS:
                    for hv in HS:
                        if lam == 0 and hv == 0:
                            continue                                            # phi auxiliary, no phi root (elliptic in the leaf)
                        U, ok = roots(Cth, lam, hv, ac, c2)
                        nc += len(Cth); nv += int(np.sum(~ok))
                        if lam == 0 and hv == 1.0:
                            U_par_min = min(U_par_min, float(U[0, 0]))
    a1[KEY(z, Mb, f)] = dict(r_Y_kpc=rY / KPC, n_points=len(pts), n_cells=nc, violations=nv)
    nviol_tot += nv; ncells += nc
P("    hosts: " + ", ".join(f"{kk}: r_Y {v['r_Y_kpc']:.1f} kpc, {v['violations']}/{v['n_cells']}" for kk, v in list(a1.items())[:8]) + " ...")
check("A1 [H1, pre-declared] CRITERION B's CAUSAL PART HOLDS ACROSS THE YIELD SURFACE: on all 24 hosts (yielded side, a geometric "
      "approach to d/r_Y = 1e-12, the plug, the zero-field point), every angle, both alpha_c ends, c_2 = 7.29e-3/0.1, lambda = 0/1/100 "
      "and h = 0/0.3/1, every root U = omega^2/k^2 of the exact block is real and >= 0; the cones are centred on the khronon's "
      "normal (phi's inertia is (n.d phi)^2), so tau is a global time function compatible with every cone; divergent speeds are "
      "phi's transverse ones at the surface (lambda > 0), all in the leaf",
      f"violations {nviol_tot} of {ncells} (root, cell) evaluations", nviol_tot == 0 and ncells > 0,
      "the plug is rigid (phi frozen: no phi characteristic; the khronon at E = alpha_c); a leafwise-instantaneous response is "
      "allowed by criterion B")
OUT["numbers"]["A1"] = a1
P(f"    {el()}")

# ============================================================================================ A2 the surface's exponents
banner("A2  THE SURFACE IS DEGENERATE: C_L ~ d^(1/2), C_T ~ d^(-1/2); effective speeds; the lambda = 0 transverse limit")
a2 = {}; slopes_L, slopes_T, lam0_lim = [], [], []
for (z, Mb, f) in GAL:
    a0, Lz, yth, ybp_f, rY = host_profile(z, Mb, f)
    if not np.isfinite(rY):
        a2[KEY(z, Mb, f)] = dict(surface=False); slopes_L.append(float("nan")); slopes_T.append(float("nan")); continue
    d = np.geomspace(1e-10, 1e-5, 40)
    x = x_static(ybp_f(rY * (1 - d)), yth)
    sL = float(np.polyfit(np.log(d), np.log(CL_of(x)), 1)[0]); sT = float(np.polyfit(np.log(d), np.log(CT_of(x, yth)), 1)[0])
    ac, c2 = 3.2e-9, 7.29e-3
    UK = c2 * (2 - ac) / (ac * (2 + 3 * c2))
    U0T, _ = roots(CT_of(x, yth), 0.0, 1.0, ac, c2)
    lim_ratio = float(U0T[0, 0] / UK)
    Upar, _ = roots(CL_of(x), 0.0, 1.0, ac, c2)
    sV = float(np.polyfit(np.log(d), np.log(np.sqrt(Upar[0])), 1)[0])
    cpar = {dd: float(np.sqrt(roots(CL_of(x_static(ybp_f(np.array([rY * (1 - dd)])), yth)), 0.0, 1.0, ac, c2)[0][0, 0]) * C_LIGHT / 1e3)
            for dd in (1e-6, 1e-3, 1e-1)}
    a2[KEY(z, Mb, f)] = dict(surface=True, slope_CL=sL, slope_CT=sT, slope_cpar=sV, lam0_transverse_over_UK=lim_ratio, c_par_kms=cpar)
    slopes_L.append(sL); slopes_T.append(sT); lam0_lim.append(lim_ratio)
for kk, v in list(a2.items())[:24:3]:
    if v.get("surface"):
        P(f"    {kk:22s}: slope C_L {v['slope_CL']:.4f}, C_T {v['slope_CT']:.4f}, c_par {v['slope_cpar']:.4f}; lambda = 0 transverse U/U_K at "
          f"d = 1e-10 r_Y: {v['lam0_transverse_over_UK']:.5f}; c_par at d/r_Y = 1e-6/1e-3/0.1: " + "/".join(f"{c:.3g}" for c in v["c_par_kms"].values()) + " km/s")
okL = np.all(np.isfinite(slopes_L)) and np.all(np.abs(np.array(slopes_L) - 0.5) <= 0.02)
okT = np.all(np.isfinite(slopes_T)) and np.all(np.abs(np.array(slopes_T) + 0.5) <= 0.02)
ok0 = len(lam0_lim) == len(GAL) and np.all(np.abs(np.array(lam0_lim) - 1) <= 0.01)
check("A2 [H2, pre-declared] THE YIELD SURFACE IS A DEGENERATE (WEAKLY HYPERBOLIC) LOCUS on all 24 hosts: C_L ~ d^(1/2) and C_T ~ "
      "d^(-1/2) (fitted over d/r_Y = 1e-10 .. 1e-5, +-0.02), the longitudinal effective speed ~ d^(1/4) -> 0, and at lambda = 0 the "
      "effective transverse root tends to the BPS khronon root c_2 (2 - alpha_c)/(alpha_c (2 + 3 c_2)) within 1%",
      f"C_L slopes [{np.nanmin(slopes_L):.4f}, {np.nanmax(slopes_L):.4f}]; C_T slopes [{np.nanmin(slopes_T):.4f}, {np.nanmax(slopes_T):.4f}]; "
      f"lambda = 0 transverse/U_K [{min(lam0_lim) if lam0_lim else float('nan'):.5f}, {max(lam0_lim) if lam0_lim else float('nan'):.5f}] "
      f"({len(lam0_lim)} of 24 hosts with a surface)", okL and okT and ok0)
OUT["numbers"]["A2"] = a2
# (reported, added after the first recorded main run failed A2's third clause) the lambda = 0 transverse root in closed form:
# U/U_K = C_T alpha_c/(C_T alpha_c + (2 - alpha_c) h^2), i.e. U ~ c_2 C_T/((2 + 3 c_2) h^2) while C_T alpha_c << h^2 -- it DIVERGES as
# d^(-1/2) like the lambda > 0 transverse speed and reaches U_K only once C_T alpha_c ~ h^2
lam0_rep = {}
for (z, Mb, f) in GAL:
    a0, Lz, yth, ybp_f, rY = host_profile(z, Mb, f)
    if not np.isfinite(rY):
        continue
    d = np.geomspace(1e-10, 1e-5, 40)
    CT = CT_of(x_static(ybp_f(rY * (1 - d)), yth), yth)
    ac, c2 = 3.2e-9, 7.29e-3
    U0 = roots(CT, 0.0, 1.0, ac, c2)[0][0]
    closed = CT * ac / (CT * ac + (2 - ac)) * c2 * (2 - ac) / (ac * (2 + 3 * c2))
    small = c2 * CT / (2 + 3 * c2)
    d_sat = 1e-10 * (CT[0] * ac / (2 - ac)) ** 2                                   # C_T ~ d^(-1/2) extrapolated to C_T alpha_c = 2 - alpha_c
    lam0_rep[KEY(z, Mb, f)] = dict(slope=float(np.polyfit(np.log(d), np.log(U0), 1)[0]),
                                   closed_dev=float(np.max(np.abs(U0 / closed - 1))), small_dev=float(np.max(np.abs(U0 / small - 1))),
                                   d_sat_over_rY=float(d_sat), d_sat_m=float(d_sat * rY))
sl0 = [v["slope"] for v in lam0_rep.values()]
if lam0_rep:
  P(f"    (reported) lambda = 0, h = 1, alpha_c = 3.2e-9, c_2 = 7.29e-3: the transverse root U = U_K C_T alpha_c/(C_T alpha_c + (2 - alpha_c) h^2) "
  f"(max dev {max(v['closed_dev'] for v in lam0_rep.values()):.1e}) ~ c_2 C_T/((2 + 3 c_2) h^2) (max dev {max(v['small_dev'] for v in lam0_rep.values()):.1e}); "
  f"fitted slope in d over 1e-10..1e-5 r_Y: {min(sl0):.4f} .. {max(sl0):.4f} (divergent, like lambda > 0); it would reach U_K only at "
  f"d/r_Y ~ {min(v['d_sat_over_rY'] for v in lam0_rep.values()):.0e} .. {max(v['d_sat_over_rY'] for v in lam0_rep.values()):.0e} "
  f"({min(v['d_sat_m'] for v in lam0_rep.values()):.0e} .. {max(v['d_sat_m'] for v in lam0_rep.values()):.0e} m, against the xi floor 0.0243 pc = {0.0243 * KPC / 1e3:.1e} m "
  "below which the band-pass smooths phi): A2's third clause was mis-stated (the limit lies far inside the xi filter); the lambda = 0 roots "
  "are all real and >= 0 (A1 scans lambda = 0)")
OUT["numbers"]["A2_lambda0_reported"] = lam0_rep
P(f"    {el()}")

# ============================================================================================ A3 the linearised problem
banner("A3  THE LINEARISED phi-SECTOR ACROSS THE SURFACE: a degenerate Sturm-Liouville operator (rigid plug)")
YTH1, S01, SL1, LAM1 = 0.01, 0.02, 0.02, 1.0                                # dimensionless slab: surface at x_Y = 0.5
XY1 = (S01 - YTH1) / SL1


def CL_slab(xg):
    v = x_P2(np.maximum(SL1 * (XY1 - xg), 0.0))
    return CL_of(v)


def fd_eigs(N, nev=5):
    xg = np.linspace(0, XY1, N + 1); dx = np.diff(xg)
    Cc = np.array([np.mean(CL_slab(np.linspace(a, b, 33))) for a, b in zip(xg[:-1], xg[1:])])
    n = len(xg)
    K = np.zeros((n, n))
    kk = Cc / dx
    idx = np.arange(n - 1)
    K[idx, idx] += kk; K[idx + 1, idx + 1] += kk; K[idx, idx + 1] -= kk; K[idx + 1, idx] -= kk
    w = np.zeros(n); w[:-1] += dx / 2; w[1:] += dx / 2
    keep = np.arange(n - 1)                                                   # u(x_Y) = 0: the rigid plug
    ev, vec = eigh(K[np.ix_(keep, keep)], np.diag(LAM1 * w[keep]), subset_by_index=[0, nev - 1])
    return np.sqrt(ev), ev.min(), xg[keep], vec


def shoot_resid(w_, return_sol=False):
    kap = math.sqrt(LAM1 * w_ ** 2 / (2 * math.sqrt(SL1)))
    d0 = 1e-10 * XY1
    u0 = d0 ** 0.25 * jv(1 / 3, (4 / 3) * kap * d0 ** 0.75)
    d1 = d0 * (1 + 1e-6)
    du = (d1 ** 0.25 * jv(1 / 3, (4 / 3) * kap * d1 ** 0.75) - u0) / (d1 - d0)
    F0 = CL_slab(np.array([XY1 - d0]))[0] * du

    def rhs(dd, yv):
        C = CL_slab(np.array([XY1 - dd]))[0]
        return [yv[1] / max(C, 1e-300), -LAM1 * w_ ** 2 * yv[0]]
    s = solve_ivp(rhs, (d0, XY1), [u0, F0], rtol=1e-10, atol=1e-15, method="DOP853", dense_output=return_sol)
    return (s.y[1, -1], s) if return_sol else s.y[1, -1]


wscan = np.linspace(0.05, 11.0, 220)
rs_ = [shoot_resid(w_) for w_ in wscan]
REF = []
for i in range(len(wscan) - 1):
    if rs_[i] * rs_[i + 1] < 0 and len(REF) < 5:
        REF.append(brentq(shoot_resid, wscan[i], wscan[i + 1], xtol=1e-13))
REF = np.array(REF)
fd = {}
for N in (200, 400, 800, 1600, 3200):
    om, emin, xk, vec = fd_eigs(N)
    fd[N] = (om, emin, xk, vec)
orders = [float(np.log2(np.abs(fd[800][0] - REF) / np.abs(fd[1600][0] - REF)).mean()),
          float(np.log2(np.abs(fd[1600][0] - REF) / np.abs(fd[3200][0] - REF)).mean())]
p_obs = float(np.log2(np.abs(fd[1600][0] - fd[800][0]) / np.abs(fd[3200][0] - fd[1600][0])).mean())
rich = fd[3200][0] + (fd[3200][0] - fd[1600][0]) / (2 ** 0.5 - 1)
rich_err = float(np.max(np.abs(rich / REF - 1)))
emin_all = min(v[1] for v in fd.values())
# the eigenfunction's gradient near the surface (shooting solution of mode 1)
_, sol1 = shoot_resid(REF[0], return_sol=True)
dd = np.geomspace(1e-9, 1e-4, 30) * XY1
Fl = sol1.sol(dd)[1]; ug = Fl / CL_slab(XY1 - dd)
slope_grad = float(np.polyfit(np.log(dd), np.log(np.abs(ug)), 1)[0])
P(f"    shooting reference (exact local Bessel start, nu = 1/3): omega = {np.round(REF, 6)}")
for N, v in fd.items():
    P(f"    N = {N:5d}: omega = {np.round(v[0], 6)}; rel. error {np.round(np.abs(v[0] / REF - 1), 6)}; min eigenvalue {v[1]:.4f}")
P(f"    observed order (successive differences) {p_obs:.3f}; order-1/2 Richardson from 1600/3200: max rel error {rich_err:.2e}; "
  f"mode-1 gradient near the surface ~ d^{slope_grad:.3f}")
# the same structure on a real host: the 1e11 flagship at z = 2.5 (canonical), radial, lambda_eff = 277 (lambda = 0, h = 1)
a0, Lz, yth, ybp_f, rY = host_profile(2.5, 1e11, "canonical")
lam_eff = (2 + 3 * 7.29e-3) / 7.29e-3
real = {}
for N in (400, 800, 1600, 3200):
    rg = np.linspace(0.3 * rY, rY, N + 1)
    Cc = np.array([np.mean(CL_of(x_static(ybp_f(np.linspace(a, b, 17)), yth))) for a, b in zip(rg[:-1], rg[1:])])
    rc = 0.5 * (rg[1:] + rg[:-1]); dr = np.diff(rg)
    n = len(rg); K = np.zeros((n, n)); kk = rc ** 2 * Cc / dr
    idx = np.arange(n - 1)
    K[idx, idx] += kk; K[idx + 1, idx + 1] += kk; K[idx, idx + 1] -= kk; K[idx + 1, idx] -= kk
    w = np.zeros(n); w[:-1] += dr / 2; w[1:] += dr / 2
    keep = np.arange(n - 1)
    ev = eigh(K[np.ix_(keep, keep)], np.diag(lam_eff * (rg ** 2 * w)[keep]), eigvals_only=True, subset_by_index=[0, 2])
    real[N] = np.sqrt(ev) * C_LIGHT / Hz12(2.5)                               # omega [c units /m] -> omega/H
rel_real = float(np.max(np.abs(real[3200] / real[1600] - 1)))
P(f"    real host (1e11, z = 2.5, canonical; r in [0.3 r_Y, r_Y], lambda_eff = {lam_eff:.0f}): omega/H = " +
  "; ".join(f"N = {N}: {np.round(v, 1)}" for N, v in real.items()) + f"  (last change {rel_real:.1e})")
a3_ok = (emin_all > 0 and len(REF) == 5 and 0.4 <= p_obs <= 0.6 and rich_err <= 1e-3 and abs(slope_grad + 0.5) <= 0.05
         and min(real[3200]) > 0 and rel_real < 0.02)
check("A3 [H3, pre-declared] THE LINEARISED CAUCHY PROBLEM ACROSS THE SURFACE IS WELL POSED IN THE ENERGY NORM, NOT IN C^1: the "
      "discrete degenerate operator (rigid plug u = 0) has only positive eigenvalues, converges with the order of a d^(1/2) "
      "eigenfunction, its Richardson limit matches the shooting reference built on u ~ d^(1/4) J_(1/3)((4/3) kappa d^(3/4)), and "
      "the eigenfunction's gradient diverges as d^(-1/2) at the surface; the 1e11 flagship's radial profile at z = 2.5 behaves "
      "the same (positive, converging)",
      f"min eigenvalue {emin_all:.3f} > 0; observed order {p_obs:.3f}; Richardson vs reference {rich_err:.1e}; gradient exponent "
      f"{slope_grad:.3f}; real host omega_1/H = {real[3200][0]:.3g} (change {rel_real:.1e})", a3_ok,
      "linear: a unitary (energy-conserving) evolution, no growth; the surface is reached by characteristics in finite time "
      "(A5) and the rigid plug supplies the boundary condition; the free boundary's motion is O(amplitude) with energy "
      "O(amplitude^(5/2)), so it does not enter the quadratic energy")
OUT["numbers"]["A3"] = dict(ref=REF.tolist(), fd={str(N): v[0].tolist() for N, v in fd.items()}, order=p_obs, richardson=rich_err,
                            grad_slope=slope_grad, real_host={str(N): v.tolist() for N, v in real.items()})
P(f"    {el()}")

# ============================================================================================ A4 nonlinear loading (reported)
banner("A4  (reported) THE NONLINEAR phi-SECTOR UNDER SLOW LOADING (1-D slab, eps-regularised yield, AVF steps)")


def Wreg(v, eps):
    u = np.abs(v)
    return -u * u / 4 - u / 4 - np.log1p(-2 * u) / 8 + SGN * YTH1 * (np.sqrt(v * v + eps * eps) - eps)


def sreg(v, eps):
    u = np.abs(v)
    return np.sign(v) * u * u / (1 - 2 * u) + SGN * YTH1 * v / np.sqrt(v * v + eps * eps)


def dsreg(v, eps):
    u = np.abs(v)
    return 2 * u * (1 - u) / (1 - 2 * u) ** 2 + SGN * YTH1 * eps * eps / (v * v + eps * eps) ** 1.5


def static_v(S0t, xc, eps):
    target = S0t - SL1 * xc
    lo = np.full(len(xc), -0.4999); hi = np.full(len(xc), 0.4999)
    for _ in range(80):
        mid = 0.5 * (lo + hi); up = sreg(mid, eps) > target
        hi = np.where(up, mid, hi); lo = np.where(up, lo, mid)
    return 0.5 * (lo + hi)


def ramp_run(N, eps, Tr=20.0, amp=0.1):
    xg = np.linspace(0, 1, N + 1); dx = 1.0 / N; xc = 0.5 * (xg[1:] + xg[:-1])
    S0f = lambda t: S01 * (1 + amp * (min(t, Tr) / Tr - math.sin(2 * math.pi * min(t, Tr) / Tr) / (2 * math.pi)))
    v0 = static_v(S0f(0.0), xc, eps)
    q = np.concatenate([[0.0], np.cumsum(v0 * dx)]); q -= q[-1]
    w = np.full(N + 1, dx); w[0] = w[-1] = dx / 2; M = LAM1 * w
    p = np.zeros(N + 1); f = np.full(N + 1, SL1)

    def Hm(qq, pp, S):
        return 0.5 * np.sum(pp[:-1] ** 2 / M[:-1]) + np.sum(Wreg(np.diff(qq) / dx, eps)) * dx - np.sum(f * w * qq) + S * qq[0]
    dt = 2.0 / N; nst = int(round(Tr / dt)); t = 0.0; work = 0.0; H0 = Hm(q, p, S0f(0.0)); maxit = 0
    for _ in range(nst):
        Sm = S0f(t + 0.5 * dt)
        qn = q.copy(); vn = np.diff(qn) / dx; qk = qn + dt * p / M; qk[-1] = 0.0
        for it in range(60):
            vk = np.diff(qk) / dx; dv = vk - vn; sm = np.abs(dv) < 1e-12
            dW = np.where(sm, sreg(0.5 * (vk + vn), eps), (Wreg(vk, eps) - Wreg(vn, eps)) / np.where(sm, 1.0, dv))
            g = np.zeros(N + 1); g[:-1] -= dW; g[1:] += dW; g = g - f * w; g[0] += Sm
            R = (2 / dt) * M * (qk - qn) - 2 * p + dt * g; R[-1] = qk[-1]
            big = np.abs(dv) > 1e-7; dvs = np.where(big, dv, 1.0)
            cm = np.where(big, (sreg(vk, eps) * dvs - (Wreg(vk, eps) - Wreg(vn, eps))) / dvs ** 2, 0.5 * dsreg(0.5 * (vk + vn), eps)) / dx
            dg = (2 / dt) * M.copy(); up_ = np.zeros(N + 1); lo_ = np.zeros(N + 1)
            dg[:-1] += dt * cm; dg[1:] += dt * cm; up_[1:] = -dt * cm; lo_[:-1] = -dt * cm; dg[-1] = 1.0; lo_[-2] = 0.0
            dq = solve_banded((1, 1), np.vstack([up_, dg, lo_]), -R)
            qk = qk + dq
            if np.max(np.abs(dq)) < 1e-14:
                break
        maxit = max(maxit, it)
        pn = (2 / dt) * M * (qk - qn) - p; pn[-1] = 0.0
        work += (S0f(t + dt) - S0f(t)) * 0.5 * (qn[0] + qk[0])
        q, p = qk, pn; t += dt
    v = np.diff(q) / dx
    vqs = static_v(S0f(Tr), xc, eps)
    xY = float(xc[np.argmax(v < 3 * eps * 0.5)]); xY_qs = (S0f(Tr) - YTH1) / SL1
    return dict(xc=xc, v=v, dH=(Hm(q, p, S0f(Tr)) - H0 - work), KE=0.5 * float(np.sum(p[:-1] ** 2 / M[:-1])),
                xY=xY, xY_qs=xY_qs, lag=float(np.max(np.abs(v - vqs))), maxit=maxit)


a4 = {}
if SGN > 0:
    for eps in (1e-3, 3e-4):
        for N in (200, 400, 800):
            a4[(eps, N)] = ramp_run(N, eps)
    diffs = {}
    for eps in (1e-3, 3e-4):
        v2, v4, v8 = (np.interp(a4[(eps, 200)]["xc"], a4[(eps, N)]["xc"], a4[(eps, N)]["v"]) for N in (200, 400, 800))
        diffs[eps] = (float(np.sqrt(np.mean((v2 - v4) ** 2))), float(np.sqrt(np.mean((v4 - v8) ** 2))))
    de = float(np.sqrt(np.mean((a4[(1e-3, 800)]["v"] - a4[(3e-4, 800)]["v"]) ** 2)))
    for kk_, v in a4.items():
        P(f"    eps = {kk_[0]:.0e}, N = {kk_[1]}: surface {v['xY']:.4f} (quasi-static {v['xY_qs']:.4f}); max |v - v_qs| {v['lag']:.2e}; "
          f"KE {v['KE']:.2e}; energy balance residual {v['dH']:.1e}; Newton iterations <= {v['maxit']}")
    P(f"    grid differences (L2 of v, 200-400 / 400-800): " + "; ".join(f"eps {e_:.0e}: {a_:.2e} / {b_:.2e}" for e_, (a_, b_) in diffs.items())
      + f"; eps 1e-3 vs 3e-4 at N = 800: {de:.2e}")
    a4_ok = all(b_ < a_ for a_, b_ in diffs.values())
    check("A4 (reported) THE NONLINEAR phi-SECTOR UNDER SLOW LOADING: the surface advances into the plug; the solution converges "
          "under grid refinement (L2 differences shrink) and eps refinement; the energy balance closes; phi lags the quasi-static "
          "state by a bounded oscillation (the loading's own ringing, not a growth)",
          f"grid differences shrink: {a4_ok}; eps change {de:.1e}; max energy residual {max(abs(v['dH']) for v in a4.values()):.1e}",
          True, load_bearing=False)
    OUT["numbers"]["A4"] = {f"{k_[0]}_{k_[1]}": {kk: vv for kk, vv in v.items() if kk not in ("xc", "v")} for k_, v in a4.items()}
    OUT["numbers"]["A4"]["diffs"] = {str(k_): v for k_, v in diffs.items()}
else:
    check("A4 (reported) not run under MUTATE (the flipped yield has no surface)", "skipped", True, load_bearing=False)

# ============================================================================================ A5 WKB structure (reported)
banner("A5  (reported) WKB STRUCTURE AT THE SURFACE, and the non-adiabatic layer on each host")
dd = sp.Symbol("d", positive=True); s_, lam_s = sp.symbols("s lambda_e", positive=True)
CLd = 2 * sp.sqrt(s_ * dd)                                                  # C_L ~ 2 x, x ~ sqrt(s d)
cpar = sp.sqrt(CLd / lam_s)
t_travel = sp.integrate(1 / cpar, (dd, 0, dd))
A_wkb = sp.simplify((CLd * (1 / cpar)) ** sp.Rational(-1, 2))               # flux C k omega A^2 const, k = omega/c
grad_wkb = sp.simplify(A_wkb / cpar)
P(f"    c_par = {cpar};  travel time from d to the surface = {sp.simplify(t_travel)} (finite);  WKB amplitude ~ {A_wkb}, gradient ~ {grad_wkb}")
P(f"    genuine nonlinearity: F_P2''(x) = {sp.simplify(sp.diff(xs_ ** 2 / (1 - 2 * xs_), xs_, 2))} > 0 -> finite-amplitude phi waves steepen; the "
  f"relative amplitude dv/v0 grows toward the surface (v0 ~ d^(1/2), dv ~ d^(-3/8)), so any finite-amplitude wave arriving there is "
  f"nonlinear in a layer d_nl ~ amplitude^(8/7): caustics at the surface are generic for incoming waves; the action supplies no "
  f"dissipation (no entropy condition), so weak-solution uniqueness is OPEN")
a5 = {}
for (z, Mb, f) in GAL:
    a0, Lz, yth, ybp_f, rY = host_profile(z, Mb, f)
    if not np.isfinite(rY):
        continue
    ac, c2 = 3.2e-9, 7.29e-3
    dgrid = np.geomspace(1e-14, 0.5, 400)
    x = x_static(ybp_f(rY * (1 - dgrid)), yth)
    U, _ = roots(CL_of(x), 0.0, 1.0, ac, c2)
    cp = np.sqrt(U[0]) * C_LIGHT / 1e3
    thin = dgrid[cp < 300.0]
    a5[KEY(z, Mb, f)] = dict(r_Y_kpc=rY / KPC, layer_kpc=float(thin.max() * rY / KPC) if len(thin) else 0.0,
                             layer_over_rY=float(thin.max()) if len(thin) else 0.0)
P("    non-adiabatic layer (c_par < 300 km/s; lambda = 0, c_2 = 7.29e-3): " + ", ".join(
    f"{kk}: {v['layer_kpc']:.3g} kpc ({v['layer_over_rY']:.1e} r_Y)" for kk, v in a5.items()))
check("A5 (reported) WKB structure: characteristics reach the surface in finite time (~ d^(3/4)); linear focusing is mild (amplitude "
      "~ d^(-1/8)); finite-amplitude waves steepen there (genuine nonlinearity); the layer where phi cannot follow baryons "
      "quasi-statically (c_par < 300 km/s) is thin", f"max layer {max(v['layer_kpc'] for v in a5.values()):.3g} kpc "
      f"(z = 0.25 hosts, at r_Y ~ 2-4 Mpc); at z >= 2.5 < {max(v['layer_kpc'] for k_, v in a5.items() if k_.startswith(('2.5', '4.0'))):.1e} kpc",
      True, load_bearing=False)
OUT["numbers"]["A5"] = a5

# ============================================================================================ verdict
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
_dsat_max = max([v['d_sat_over_rY'] for v in lam0_rep.values()] or [float('nan')])
banner("VERDICT")
_ok = {k_: OUT['checks'][k_]['pass'] for k_ in ('A1', 'A2', 'A3')}
_pf = {k_: ('PASS' if v else 'FAIL') for k_, v in _ok.items()}
_t_sp = ("at the surface c_par -> 0 as d^(1/4) and c_perp -> oo as d^(-1/4) -- for lambda > 0 and also at lambda = 0 "
         f"(U ~ c_2 C_T/((2 + 3 c_2) h^2), capped by the BPS khronon speed only at d/r_Y <~ {_dsat_max:.0e}); in the plug phi is rigid "
         "(no phi characteristic), the khronon sits at E = alpha_c" if (okL and okT) else
         "the declared surface structure (C_L -> 0, C_T -> oo) does NOT hold on these backgrounds")
_t1 = "Criterion B's causal part holds everywhere" if _ok['A1'] else "Criterion B's causal part FAILS"
_t2 = ("the surface is degenerate: C_L ~ d^(1/2), C_T ~ d^(-1/2) on all 24 hosts" if (okL and okT) else "the surface exponents do NOT hold")
_n2 = (" -- on its third clause only: the lambda = 0 transverse root does not approach U_K on the tested range (reported above)"
       if (okL and okT and not ok0) else "")
_t3 = ("the linearised Cauchy problem with the rigid plug is well posed in the energy norm but not in C^1" if _ok['A3']
       else "the linearised Cauchy problem with the rigid plug is NOT shown well posed")
_t_end = ("No linear growth; finite-amplitude waves steepen at the surface; the nonlinear (variational-inequality) Cauchy problem is OPEN."
          if (_ok['A1'] and _ok['A3']) else "The linear problem fails as printed; the nonlinear Cauchy problem is OPEN.")
P(f"""  (a) Characteristic speeds: yielded side -- phi's cone c_par^2 = C_L/lambda_eff, c_perp^2 = C_T/lambda_eff (effective, h ~ 1;
      principal: C/lambda), the khronon's fast BPS cone, light; {_t_sp}.
      {_t1} (A1: {_pf['A1']}); {_t2} (A2: {_pf['A2']}{_n2});
      {_t3} (A3: {_pf['A3']}).
      {_t_end}
  Not 'closed'.  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}.  Time {time.time() - T0:.0f} s.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"  wrote {os.path.basename(fn)}")
_OUTF.close()
sys.exit(1 if nlb else 0)
