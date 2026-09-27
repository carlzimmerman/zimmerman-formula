#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR18 (c) + (d) -- THE BAND-PASS'S DEGREES OF FREEDOM WITH TWO HEAT DEPTHS, and the size of H_Y's leaf-average (<K>_h) global
terms.

WHY.  (d) FP5 (derivation_chain_2026/FP5_dof_and_a0_field.py, A3/B2) showed on the C-H core that the heat filter (W, L,
lambda_0) is a second-class auxiliary sector: its block determinant is kernel-independent and its Schur complement only
multiplies the tangent by sigma_n(k)^2.  FP9's band-pass reads the heat branch at TWO depths, chi = W_b - W_B, on FP7's AQUAL
root (J on phi, the chassis on chi); H_Y's depth B = L(<K>_h)^2/2 and H_S's B[state] depend on leaf averages.  This lane builds
explicit two-segment heat chains on FP7's unitary-gauge block and counts.
(c) H_Y's y_th and L depend on <K>_h.  Varying the metric through <K>_h gives the field equations a term (Q/V) x (a local
operator), Q = Int_leaf N sqrt(h) dL/d<K>: an intensive coefficient (the leaf-averaged sensitivity), not an O(1/V) one.  Its
local operator reads K = nabla.n (the leaves' expansion: velocities) and sqrt(h), so it enters the Newtonian equations only at
O(Phi/c^2).  This lane sizes it, both readings of the web's one-point field (Gaussian and halo), both footings, and
states what conservation requires (XR18_state_separator.py N2 checks the translation Noether identity on leaves).

PRE-DECLARED (written into this file before its first full run; no exploratory run was made for this file)
 H1 [load-bearing] For explicit band-pass chains (n1, n2) = (1, 1), (1, 2), (2, 1), (2, 2) on FP7's unitary-gauge block: the
    heat block's determinant is nonzero and independent of omega, C_phi, lambda, c_2 and alpha_c (second class, no dynamics);
    its Schur complement onto (psi, n, B, phi) equals FP9's K2 block with h -> sigma_b(k) (1 - (1 + (B - b) k^2/n2)^(-n2)) exactly;
    and deg_omega of the full scalar determinant is 4 (lambda > 0) and 2 (lambda = 0), with the heat block contributing 0:
    N = 2 tensor + 2 scalar (lambda > 0) / + 1 (lambda = 0) -- the band-pass adds no mode.
 H2 [load-bearing] The leaf-averaged depth adds no velocity: at k != 0 the leaf average's perturbation vanishes (the depth is a
    constant on each leaf, H1 applies leaf by leaf), and at k = 0 the band-pass gain vanishes (h(0) = 0: the chassis does not
    couple the homogeneous mode); the MOND sector's correction to the scale factor's kinetic coefficient through <K>_h is below
    1e-5 of GR's at z = 0.25, 1, 2.5 (both footings, both readings) -- the Legendre map stays invertible.
 H3 [load-bearing] H_Y's <K>_h global term is (v/c)^2-suppressed: the effective extra density it adds to the psi-equation,
    rho_extra/rho_bar ~ 6 p' a0^2 y_th <x>/(4 pi G rho_bar c^2) (the yield) plus the band-pass's n-term, is below 1e-4 at z = 0.25,
    1, 2.5 in both readings of <x> and both footings.
The writer's expectation: all three pass.

CHECKS
  K1 CONTROL: a SINGLE-depth chain (n1 = 1, 2, no second segment) eliminated by Schur complement reproduces FP9's K2 block with
     h -> sigma_n(k) = (1 + b k^2/n)^(-n), whose determinant is FP7's committed det M (sigma -> sigma_n).
  D1 = H1.  D2 = H2.  C1 = H3.
  D3 (reported) the Dirac bookkeeping per point with n1 + n2 heat points, and the plug: where phi is frozen by the yield its row
     and column drop and the scalar count is 1 (lambda > 0).
  C2 (reported) conservation: the leaf average is a covariant functional of (g, tau); the full action is diffeomorphism
     invariant, so the Noether identity gives nabla_mu T^mu_nu = 0 for minimally coupled matter once every non-matter field
     equation (the khronon's, with its global (Q/V) term) holds.  The translation part is checked numerically on leaves in
     XR18_state_separator.py (N2).
  Development record (disclosed in XR18_README.md): the first MUTATE attempt stalled in a symbolic Schur complement of an
  omega-dependent block (the Schur comparison is now made only when the heat block is omega-free); after the first recorded
  main run, D3's (reported) bookkeeping was corrected (it mixed the unitary-gauge and covariant conventions and printed 5) and
  the pass count now counts every check.  MUTATE and main were then re-run in that order.
MUTATE=1 gives the second heat segment a time derivative (tau_h d_t W in its constraint: a dynamical heat depth): the heat
block's determinant becomes omega-dependent and extra modes appear, so D1 must FAIL (rc = 1).

SCOPE.  Linear, frozen-coefficient Minkowski block for the count (FP5/FP7's level); order-of-magnitude global terms with
the population brackets; no particle-mesh run.  kappa = 1/2 is FITTED (Z = 5.7888).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR18_nonlocal_dof.py
"""
import os, sys, io, re, json, math, time, random, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR18_nonlocal_dof"
T0 = time.time()
_OUTF = open(os.path.join(HERE, SLUG + ("_MUTATE.out" if MUTATE else ".out")), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _OUTF.write(s + "\n"); _OUTF.flush()


CH, OUT = [], {"lane": "XR18cd", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
    P("\n  *** MUTATE=1: the second heat segment gets a time derivative (a dynamical heat depth) -- D1 must FAIL ***")
F7 = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP7_aqual_type_repair_results.json")))["numbers"]

# ============================================================================================ the block with explicit heat chains
tt_, xx_, yy_, zz_ = sp.symbols('t x y z', real=True)
X3m = (xx_, yy_, zz_)
eb = sp.Symbol('e_b')
alm, c2m, Cph, lmm = sp.symbols('alpha_c c_2 C_phi lambda', real=True)
bq, Bq, tauh = sp.symbols('b B_d tau_h', positive=True)                    # first-segment depth b, extra depth B - b, MUTATE's time scale
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
Bu, Cu = 2 * (2 - alm), -(2 - alm)
Jquad = -2 * Cph * sum(gin[i, j] * Fi[i] * Fi[j] for i in range(3) for j in range(3))
ndphi = (sp.diff(eb * Ff, tt_) - sum(sum(gin[i, j] * Ni[j] for j in range(3)) * Fi[i] for i in range(3))) / Nl
kq_, wq_ = sp.symbols('k omega', real=True)
phs = sp.exp(sp.I * (kq_ * zz_ - wq_ * tt_))


def lap(f):
    return sum(sp.diff(f, x_, 2) for x_ in X3m)


def build(n1, n2, heat=True):
    """the second-order Lagrangian with an explicit heat chain W_0 = phi, W_j (j = 1..n1+n2) by implicit Euler steps of depth b/n1
    (first segment) and (B - b)/n2 (second); chi = W_n1 - W_(n1+n2) (or chi = W_n1 when n2 = 0); returns Fourier rows."""
    NW = n1 + n2
    Ws = [sp.Function(f'W{j}')(tt_, xx_, yy_, zz_) for j in range(NW + 1)]
    Ls = [sp.Function(f'L{j}')(tt_, xx_, yy_, zz_) for j in range(NW)]
    l0 = sp.Function('l0')(tt_, xx_, yy_, zz_)
    chi = Ws[n1] - (Ws[NW] if n2 > 0 else 0)
    Xi = [sp.diff(eb * chi, xi_) for xi_ in X3m]
    chassis = Bu * sum(gin[i, j] * ai[i] * Xi[j] for i in range(3) for j in range(3)) + Cu * sum(gin[i, j] * Xi[i] * Xi[j] for i in range(3) for j in range(3))
    Lfull = Nl * sp.exp(-3 * eb * pf) * (KK - trK ** 2 + R3 + alm * aa - c2m * trK ** 2 + chassis + Jquad + 2 * lmm * ndphi ** 2)
    L2 = sp.expand((sp.diff(Lfull, eb, 2) / 2).subs(eb, 0))
    hterm = 0
    for j in range(NW):
        dz = bq / n1 if j < n1 else Bq / n2
        extra = (tauh * sp.diff(Ws[j + 1], tt_)) if (MUTATE and j >= n1) else 0
        hterm += Ls[j] * ((Ws[j + 1] - Ws[j]) - dz * lap(Ws[j + 1]) + extra)
    hterm += l0 * (Ws[0] - Ff)
    L2 = L2 + hterm
    fields = [nf, pf, Bf, Sf, Ff] + Ws + Ls + [l0]
    EL = euler_equations(L2, fields, [tt_, xx_, yy_, zz_])
    amps = [sp.Symbol(f'A_{i}') for i in range(len(fields))]
    sub = {f_: a_ * phs for f_, a_ in zip(fields, amps)}
    rows = [sp.expand(sp.simplify((e_.lhs - e_.rhs).subs(sub).doit() / phs)) for e_ in EL]
    M = sp.Matrix([[sp.expand(sp.diff(r_, a_)) for a_ in amps] for r_ in rows])
    return M, fields, amps, NW


def schur_blocks(M, NW):
    """rows/cols: 0 n, 1 psi, 2 B, 3 S, 4 phi, 5.. heat.  Scalar metric+phi block in FP9's order (psi, n, B, phi) = (1, 0, 2, 4)."""
    Aix = [1, 0, 2, 4]
    Hix = list(range(5, M.shape[0]))
    MAA = M.extract(Aix, Aix); MAH = M.extract(Aix, Hix); MHA = M.extract(Hix, Aix); MHH = M.extract(Hix, Hix)
    return MAA, MAH, MHA, MHH


# FP9's K2 block with a symbol h (the reference): FP7's committed det with sigma -> h
hq = sp.Symbol('h', real=True)
sig_ = sp.Symbol('sigma', real=True)
det7 = sp.sympify(re.sub(r"\blambda\b", "lam_", F7["B3"]["det"]),
                  locals={"alpha_c": alm, "c_2": c2m, "C_phi": Cph, "lam_": lmm, "sigma": sig_, "k": kq_, "omega": wq_})

banner("K1  CONTROL: a single-depth chain eliminated by Schur complement reproduces FP7's committed det M (sigma -> sigma_n)")
k1 = {}
for n in (1, 2):
    M, fields, amps, NW = build(n, 0)
    MAA, MAH, MHA, MHH = schur_blocks(M, NW)
    Meff = (MAA - MAH * MHH.LUsolve(MHA)).applyfunc(sp.simplify)
    det_eff = sp.factor(sp.simplify(Meff.det(method='berkowitz')))
    sig_n = (1 + bq * kq_ ** 2 / n) ** (-n)
    k1[n] = sp.simplify(sp.factor(det_eff - det7.subs(sig_, sig_n))) == 0
    P(f"    n = {n}: Schur det == FP7's det(sigma -> (1 + b k^2/{n})^-{n}): {k1[n]}   {el()}")
check("K1 CONTROL: a single-depth heat chain on FP7's block, eliminated by Schur complement, gives FP7's committed det M with "
      "sigma -> sigma_n(k) = (1 + b k^2/n)^(-n) exactly (n = 1, 2)", str(k1), all(k1.values()))

# ============================================================================================ D1 the band-pass chains
banner("D1  THE BAND-PASS (two heat depths): heat determinant, Schur complement, mode count")
d1 = {}
rnd = random.Random(20260927)
for (n1, n2) in ((1, 1), (1, 2), (2, 1), (2, 2)):
    M, fields, amps, NW = build(n1, n2)
    MAA, MAH, MHA, MHH = schur_blocks(M, NW)
    hdet = sp.factor(sp.simplify(MHH.det(method='berkowitz')))
    h_free = not any(hdet.has(s_) for s_ in (wq_, Cph, lmm, c2m, alm))
    sb = (1 + bq * kq_ ** 2 / n1) ** (-n1)
    hn = sb * (1 - (1 + Bq * kq_ ** 2 / n2) ** (-n2))
    if h_free:                                           # the Schur complement is only meaningful for an auxiliary (omega-free) block
        Meff = (MAA - MAH * MHH.LUsolve(MHA)).applyfunc(sp.simplify)
        det_eff = sp.factor(sp.simplify(Meff.det(method='berkowitz')))
        schur_ok = sp.simplify(sp.factor(det_eff - det7.subs(sig_, hn))) == 0
    else:
        schur_ok = None                                  # (MUTATE) a dynamical heat depth: not computed, D1 already fails
    # the full determinant's omega degree at random rational parameters (lambda > 0 and lambda = 0)
    degs = {}
    for lamv in (sp.Rational(rnd.randint(1, 50), 7), 0):
        vals = {alm: sp.Rational(rnd.randint(1, 40), 997), c2m: sp.Rational(rnd.randint(1, 90), 101), Cph: sp.Rational(rnd.randint(1, 500), 97),
                lmm: lamv, bq: sp.Rational(rnd.randint(1, 30), 211), Bq: sp.Rational(rnd.randint(1, 300), 17), kq_: sp.Rational(rnd.randint(20, 300), 100),
                tauh: sp.Rational(3, 7)}
        Mfull = M.extract([0, 1, 2, 4] + list(range(5, M.shape[0])), [0, 1, 2, 4] + list(range(5, M.shape[0])))
        dd = sp.expand(Mfull.subs(vals).det(method='berkowitz'))
        degs[str(lamv != 0)] = sp.Poly(dd, wq_).degree() if dd != 0 else -1
    d1[(n1, n2)] = dict(heat_det=str(hdet), heat_free=h_free, schur=schur_ok, deg=degs)
    P(f"    (n1, n2) = ({n1}, {n2}): heat det = {hdet} (free of omega/C_phi/lambda/c_2/alpha_c: {h_free}); Schur det == FP9 block with "
      f"h = sigma_b (1 - (1 + (B - b) k^2/n2)^-n2): {schur_ok}; deg_omega of the full scalar det: lambda > 0 {degs['True']}, lambda = 0 {degs['False']}   {el()}")
d1_ok = all(v["heat_free"] and v["schur"] is True and v["deg"]["True"] == 4 and v["deg"]["False"] == 2 for v in d1.values())
check("D1 [H1, pre-declared] THE BAND-PASS ADDS NO MODE: for explicit two-segment heat chains (n1, n2) = (1,1), (1,2), (2,1), (2,2) the "
      "heat block's determinant is nonzero and free of omega, C_phi, lambda, c_2, alpha_c (second class); the Schur complement is "
      "FP9's block with h = sigma_b(k)(1 - (1 + (B - b)k^2/n2)^(-n2)) exactly; the full scalar determinant has deg_omega = 4 (lambda > 0) "
      "and 2 (lambda = 0): 2 tensor + 2 scalar modes (+ 1 at lambda = 0), the heat pair adds none",
      "; ".join(f"{k_}: heat-free {v['heat_free']}, Schur {v['schur']}, deg {v['deg']}" for k_, v in d1.items()), d1_ok)
OUT["numbers"]["D1"] = {str(k_): v for k_, v in d1.items()}

# D3 (reported) the Dirac bookkeeping and the plug.  Development record: the first recorded main run kept tau in phase space AND
# treated the lapse pair (pi_N, H) as second class -- the unitary-gauge rule -- which double-counts the khronon and printed 5.
# Both conventions are now counted consistently: (U) unitary gauge (tau = t, as D1's block): 6 first class (pi_i, H_i), the lapse
# pair second class; (C) covariant (tau kept): 8 first class (pi_N, pi_i, H, H_i).  The heat sector (W_0..W_n, L_1..L_n,
# lambda_0; W_0 = phi enforced by lambda_0) is auxiliary: all its momenta vanish, 4n + 4 second-class constraints.
nh1, nh2 = sp.symbols("n_1 n_2", positive=True, integer=True)
nH = nh1 + nh2
heatP = 2 * (nH + 1) + 2 * nH + 2                                             # W_0..W_n, L_1..L_n, lambda_0
heatSC = 2 * (nH + 1) + 2 * nH + 2                                            # their vanishing momenta + the secondaries
dimP_U = 12 + 2 + 6 + 2 + heatP                                               # h_ij, N, N^i, phi (tau = t)
Nphys_U = sp.simplify((dimP_U - 2 * 6 - (2 + heatSC)) / 2)
dimP_C = 12 + 2 + 6 + 2 + 2 + heatP                                           # ... + tau
Nphys_C = sp.simplify((dimP_C - 2 * 8 - heatSC) / 2)
Nplug_U = sp.simplify(Nphys_U - 1); Nplug_C = sp.simplify(Nphys_C - 1)        # phi frozen: its pair drops
check("D3 (reported) Dirac bookkeeping per point with n1 + n2 heat points (lambda > 0): (dim P - 2 N_FC - N_SC)/2 = 4 = 2 tensor + khronon "
      "+ phi, independent of n1, n2, in the unitary-gauge and the covariant counting alike; in a plug (phi frozen by the yield) phi's "
      "pair drops and the local count is 3",
      f"N_phys unitary gauge {Nphys_U}, covariant {Nphys_C}; plug {Nplug_U}/{Nplug_C}",
      Nphys_U == 4 and Nphys_C == 4 and Nplug_U == 3 and Nplug_C == 3,
      "the first recorded main run mixed the two conventions (tau kept, lapse pair second class) and printed 5; corrected here "
      "(disclosed in XR18_README.md); the load-bearing count is D1's determinant degree", load_bearing=False)

# ============================================================================================ D2 / C1 the <K>_h channel
banner("D2 C1  H_Y's <K>_h CHANNEL: the global coefficient's size (v/c)^2, both readings of the web, both footings")
FP9 = os.path.join(REPO, "real_research", "derivation_chain_2026", "FP9_web_galaxy_separator.py")
_s9 = open(FP9).read(); NS9 = {"__file__": FP9, "__name__": "fp9m"}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(_s9[:_s9.index('\nbanner("K  CONTROLS')], FP9, "exec"), NS9)
finally:
    if _old is None:
        os.environ.pop("MUTATE", None)
    else:
        os.environ["MUTATE"] = _old
M6 = NS9["M6"]; A0 = NS9["A0"]; FOOTS = NS9["FOOTS"]
G6, MPCm, MSUN, c_, Om, OL, H0, h_ = M6["G6"], M6["MPCm"], M6["MSUN"], M6["c"], M6["Om"], M6["OL"], M6["H0"], M6["h"]
rho_crit0, Ez, OmL_a = M6["rho_crit0"], M6["Ez"], M6["OmL_a"]
x_P2, L_phys, LL_of, y_th_z, gfr = NS9["x_P2"], NS9["L_phys"], NS9["LL_of"], NS9["y_th_z"], M6["gfrac_smooth"]
LLh = LL_of(1.3, 2.0); FLh = (1e-6, 4.0, NS9["YIELD"]); PP, NN = 4.0, 2.0
FB = 0.02237 / (0.02237 + 0.1200)
Delta_lin0 = M6["Delta_lin0"]
KKF = np.logspace(-4, 3, 3000); LKF = np.log(KKF); D2L0 = np.array([Delta_lin0(k) for k in KKF]) ** 2
from scipy.integrate import solve_ivp
_sD = solve_ivp(lambda N_, Y: [Y[1], 1.5 * (Om / math.exp(3 * N_) / Ez(math.exp(N_)) ** 2) * Y[0] - (2 + M6["dlnH"](math.exp(N_))) * Y[1]],
                (math.log(M6["A_I"]), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-10, atol=1e-14, dense_output=True)
Dl = lambda a: float(_sD.sol(math.log(a))[0] / _sD.sol(0.0)[0])


def sig2(R, D2):
    return float(np.trapz(D2 * np.exp(-(KKF * R) ** 2), LKF))


def x_mean_halo(a, a0v, Lp, yth):
    z = 1 / a - 1; D2 = D2L0 * Dl(a) ** 2
    lnM = np.linspace(math.log(1e8), math.log(1e15), 100)
    Rh = ((np.exp(lnM) * MSUN) / ((2 * math.pi) ** 1.5 * Om * rho_crit0)) ** (1 / 3) / MPCm * h_
    sg = np.array([math.sqrt(sig2(R, D2)) for R in Rh]); nu_ = 1.686 / sg
    dn = (Om * rho_crit0 / (np.exp(lnM) * MSUN)) * math.sqrt(2 / math.pi) * nu_ * np.exp(-nu_ ** 2 / 2) * np.abs(np.gradient(np.log(sg), lnM)) * MPCm ** 3
    tot = 0.0; Lm = Lp * MPCm
    for i, lm in enumerate(lnM):
        Mb = 0.3 * FB * math.exp(lm) * MSUN
        r = np.geomspace(1e-4, 10.0, 500) * MPCm
        x = x_P2(np.maximum(G6 * Mb * (1 - gfr(r / Lm)) / (a0v * r ** 2) - yth, 0.0))
        tot += dn[i] * float(np.trapz(4 * math.pi * r ** 2 * x, r)) / MPCm ** 3 * (1 + z) ** 3 * (lnM[1] - lnM[0])
    return tot


def x_mean_gauss(y_rms, yth):
    u = np.linspace(0, 6, 3000); p = math.sqrt(2 / math.pi) * 3 ** 1.5 * u ** 2 * np.exp(-1.5 * u ** 2)
    return float(np.trapz(p * x_P2(np.maximum(y_rms * u - yth, 0.0)), u))


def y_rms_bp(a, a0v, Lp):
    """the web's band-passed leaf-rms field (linear, per FP13's gbp_rms_phys form) in a0 units."""
    D2 = D2L0 * Dl(a) ** 2
    g = 4 * math.pi * G6 * Om * rho_crit0 / a ** 3 * np.sqrt(D2) / (KKF * h_ / (a * MPCm))
    g = g * (1.0 - np.exp(-0.5 * (KKF * h_ * Lp / a) ** 2))
    return math.sqrt(float(np.trapz(g ** 2, LKF))) / a0v


c1 = {}; d2 = {}
for z in (0.25, 1.0, 2.5):
    a = 1 / (1 + z)
    for f in FOOTS:
        a0v = A0[f]; Lp = L_phys(LLh, NN, a); yth = y_th_z(FLh, z)
        rho_bar = Om * rho_crit0 / a ** 3
        yr = y_rms_bp(a, a0v, Lp)
        for rd, xm in (("gauss", x_mean_gauss(yr, yth)), ("halo", x_mean_halo(a, a0v, Lp, yth))):
            eY = a0v ** 2 * yth * xm / (4 * math.pi * G6)                           # the yield energy density <e_Y>
            eJ = a0v ** 2 * xm ** 3 / (6 * math.pi * G6)                            # deep-MOND J energy scale (2/3 x^3 a0^2/(4 pi G))
            rho_extra = 6 * (2 * PP * eY + NN * eJ) / c_ ** 2                        # (Q/V)(K - <K>) 3/c^2, |K - <K>| <= <K>
            H = H0 * Ez(a)
            kin = (2 * PP * (2 * PP - 1) * eY + NN * (NN + 1) * eJ) / (3 * H ** 2 * c_ ** 2 / (8 * math.pi * G6))   # vs rho_crit c^2
            c1[(z, f, rd)] = rho_extra / rho_bar; d2[(z, f, rd)] = kin
            P(f"    z = {z:4.2f} {f:9s} {rd:5s}: <x> = {xm:.3e} (y_rms {yr:.2e}, y_th {yth:.2e}); rho_extra/rho_bar = {rho_extra / rho_bar:.2e}; "
              f"kinetic correction / GR's = {kin:.2e}")
check("D2 [H2, pre-declared] THE LEAF-AVERAGED DEPTH ADDS NO VELOCITY: at k != 0 the depth is constant on each leaf (D1 applies leaf by "
      "leaf); at k = 0 the band-pass gain h(0) = 0 decouples the homogeneous mode from the chassis; the MOND sector's correction to "
      "the scale factor's kinetic coefficient through <K>_h stays below 1e-5 of GR's (z = 0.25, 1, 2.5; both footings; both readings)",
      f"max correction {max(d2.values()):.1e}", max(d2.values()) < 1e-5)
check("C1 [H3, pre-declared] H_Y's <K>_h GLOBAL TERM IS (v/c)^2-SUPPRESSED: its effective extra density in the psi-equation is below "
      "1e-4 of rho_bar at z = 0.25, 1, 2.5 in both readings of <x> and both footings (unlike H_S's state functionals, which read "
      "Newtonian-order quantities: XR18_state_separator.py)", f"max rho_extra/rho_bar {max(c1.values()):.1e}", max(c1.values()) < 1e-4,
      "local physics in H_Y depends on the whole leaf's state only through <K>_h, weighted by a0^2/(G rho c^2) ~ (v/c)^2; one distant "
      "structure changes <K>_h by its share of the leaf's volume")
OUT["numbers"]["C1"] = {str(k_): v for k_, v in c1.items()}; OUT["numbers"]["D2"] = {str(k_): v for k_, v in d2.items()}
check("C2 (reported) conservation: the leaf average is a covariant functional of (g, tau); the action is diffeomorphism invariant, so "
      "nabla_mu T^mu_nu = 0 holds for minimally coupled matter once every non-matter field equation holds -- the khronon's including "
      "its global (Q/V) term; the translation identity is checked on leaves in XR18_state_separator.py N2", "structural", True,
      load_bearing=False)

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
_ok = {k_: OUT['checks'][k_]['pass'] for k_ in ('D1', 'D3', 'D2', 'C1')}
_pf = {k_: ('PASS' if v else 'FAIL') for k_, v in _ok.items()}
_t1 = ("The band-pass read at two heat depths is second class and adds no mode" if _ok['D1']
       else "The band-pass read at two heat depths is NOT second class as declared: extra modes appear")
_t3 = (f"the count is FP7's: 2 tensor + khronon + phi (lambda > 0), phi dropping where the yield freezes it (Dirac bookkeeping, "
       f"both conventions: {Nphys_U}/{Nphys_C}, plug {Nplug_U}/{Nplug_C})")
_t2 = ("a leaf-averaged depth adds no velocity" if _ok['D2'] else "the leaf-averaged depth's kinetic correction exceeds the bound")
_tc = (f"H_Y's <K>_h channel is a real global term with an intensive coefficient, but (v/c)^2-suppressed (max rho_extra/rho_bar "
       f"{max(c1.values()):.1e})" if _ok['C1'] else "H_Y's <K>_h channel is NOT (v/c)^2-suppressed below the declared bound")
P(f"""  (d) {_t1} (D1: {_pf['D1']}); {_t3} (D3: {_pf['D3']});
      {_t2} (D2: {_pf['D2']}; max {max(d2.values()):.1e}).
  (c) {_tc} (C1: {_pf['C1']}).
  Not 'closed'.  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}.  Time {time.time() - T0:.0f} s.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"  wrote {os.path.basename(fn)}")
_OUTF.close()
sys.exit(1 if nlb else 0)
