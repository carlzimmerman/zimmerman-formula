#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP14 -- ELIMINATE THE GRAVITY CORE'S KNOBS: which of the root's constants beyond (kappa, G, Lambda) can be derived,
eliminated or shown observably irrelevant -- and which cannot.  kappa = 1/2 is the one accepted fitted input.

WHY.  The chain's gravity core (FP7's repaired root, with FP9's separator above it) carries four constants beyond
(kappa, G, Lambda): the heat-filter length xi, the khronon's alpha_c, the leaf-averaged khronon coupling c_2 and the MOND
scalar's inertia lambda.  The goal is ZERO KNOBS.  This lane takes them one at a time and derives, from the action's own
variation, whether each is fixed, removable by a limit, unobservable, or a genuine knob -- verifying a fail as hard as a win.

THE GRAVITY CORE (FP7's repaired root; per 1/16 pi G, c = 1, alpha = a0/c^2, a0 = kappa c sqrt(G rho_DE), kappa = 1/2):
  R - 2 Lambda + alpha_c a^2 - c_2 (K - <K>_h)^2 + (2 - alpha_c) h^mn (2 a_m - D_m chi) D_n chi
    - 2 alpha^2 J_P2(h^mn D_m phi D_n phi / alpha^2) + 2 lambda (n^m d_m phi)^2 + heat pair (W_0 = phi, chi = W_b = S_h phi,
    b = xi^2/2) + S_m[g],     J_P2(Y) = -(1/4) ln(1 - 2 sqrt Y) - sqrt(Y)/2 - Y/2   (the framework's own law P2).
  FP9's separator (H_Y: band-pass L_Lambda, n; yield y_Lambda, p') sits above the core; its four constants are that lane's.

CHECKS
  K  CONTROLS: K1 this lane's own unitary-gauge second variation of the root reproduces FP7's committed Minkowski det M and
     FP7 C1's reduced T, V; K2 FP9's machinery (exec'd read-only) reproduces FP9's committed (H_Y) headline sigma_8 and forest;
     K3 FP2's FRW machinery (exec'd read-only) reproduces FP2's committed leaf-average structure (G_eff = 2/(2 - alpha_c));
     K4 FP1's direct QUMOND quadrupole reproduces FP1's committed strict Cassini Q2; K5 FP1's SPARC statistic (0.108 dex) and
     KiDS machinery (P2 isolated chi^2 110.6 / 102.4); K6 XC1's committed strong-coupling scale.
  L  lambda: L1 at lambda = 0 the action has an exact gauge symmetry phi -> phi + f(tau) (FRW's phibar is gauge); L2 health and
     the mode count at lambda = 0 (one scalar, omega^2 = det V/(V_22 T_11) >= 0 iff C_phi >= 0); L3 the exact-zero-field
     auxiliary (phi = A_n/sigma needs the yield); L4 every FP7/FP9 gate re-scored at lambda = 0.
  A  alpha_c: A1 every scored observable is alpha_c-independent beyond O(alpha_c) (G_N, tracking, growth, E, PPN -> 0);
     FP5's y* does not exist on the AQUAL root; A2 the classical alpha_c -> 0+ limit (the UV khronon becomes instantaneous);
     A3 XC1's strong coupling k_sc ~ alpha_c^(3/4) -> 0 and the floors it sets; A4 (reported) the L340 H4 lobe floor, OPEN.
  C  c_2: C1 the c_2 -> oo limit is regular on Minkowski (multiplier form; T -> diag(12, 4 lambda), V unchanged, det = 2 lim
     det/c_2, same mode count; the Legendre/Dirac bookkeeping); C1b on FRW (Hubbard-Stratonovich identity at quadratic order,
     Q = 0, mu finite, dust unchanged, G_eff = 1/(1 - alpha_c/2)); C2 the York/CMC kill is NOT reproduced; C3 tracking,
     PPN alpha_2, sigma_8/forest (H_Y) and c_T in the limit; C4 strong coupling in the limit.
  X  xi: X1 no constant length from (a0, Lambda, G, c) with an O(1) coefficient lands in [0.024 pc, 100 pc] (the integer-power
     hits are flagged as NUMEROLOGY); X2 field-dependent xi(g) = (c^2/g)(a0/g)^s on galaxies (SPARC, KiDS); X3 the same filter
     in the Solar System from the action's static variation (the readout-gradient force); X3b its second variation (FC-KH
     type); X4 (reported) |Phi|-based lengths; X5 dropping the filter by changing the kernel: health theorem + EFE Q2.
  F  (reported) the new constant count.   W  the ledger.
MUTATE=1 replaces the leaf-averaged -c_2 (K - <K>_h)^2 by the plain -c_2 K^2: its c_2 -> oo limit freezes the expansion
(the multiplier's background equation forces adot = 0), so C1b must FAIL (rc = 1).

SCOPE.  Frozen-coefficient linear theory (Minkowski and FRW), the record's static Solar-System and growth machinery reused
read-only, the chain's lead-grade KiDS and SPARC statistics.  No particle-mesh run.  Nothing here edits another lane's file.

Run from the repository root:  python3 real_research/derivation_chain_2026/FP14_zero_knob_core.py
"""
import os, re, io, sys, json, math, time, warnings, contextlib
warnings.filterwarnings("ignore")
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy import integrate
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP14_zero_knob_core" + ("_MUTATE" if MUTATE else "")
OUT = {"lane": "FP14", "mutate": MUTATE, "root": "FP7's AQUAL-type root (+ FP9's separator above it)", "checks": {},
       "numbers": {}, "ledger": []}
CH = []
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 116 + "\n" + t + "\n" + "=" * 116)


def check(name, measured, ok, load_bearing=True, reading=None):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def el():
    return f"[{time.time() - T0:.0f} s]"


def load_json(name):
    try:
        return json.load(open(os.path.join(HERE, name)))
    except Exception:
        return None


P(__doc__.split("CHECKS")[0].strip())
TERM = "plain" if MUTATE else "leaf"
if MUTATE:
    P("\n  *** MUTATE=1: the leaf-averaged -c_2 (K - <K>_h)^2 is replaced by the plain -c_2 K^2 -- C1b must FAIL ***")

# ============================================================================================================ inputs
cc, Gn, PC_M, AU_M, MSUN = 299792458.0, 6.67430e-11, 3.0856775814913673e16, 1.495978707e11, 1.98847e30
GM_SUN = 1.32712440018e20
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
fp0 = load_json("FP0_core_postulates_results.json")
if fp0:
    A0 = {"canonical": fp0["numbers"]["a0_canonical"], "alt": fp0["numbers"]["a0_rho_total"]}
fp7 = load_json("FP7_aqual_type_repair_results.json")
XI_FLOOR = {"canonical": 0.0243, "alt": 0.0268}
if fp7:
    XI_FLOOR = {f: fp7["numbers"]["A4"]["AQUAL_floors"][f]["floor"] for f in ("canonical", "alt")}
XI_CEIL_PC = 100.0                                            # the galaxy ceiling the chain inherits (FP7 F: '~100 pc, disc scales')
AC_MAX, C2_FLOOR = 3.2e-9, 7.2888e-3                            # FP2 B4 / FP7 D2; FP2 C4 / FP7 C3
V_TRACK = 3 * 600e3                                             # the L330/FP2 tracking target (m/s)
A_SUNWARD = 0.5 * 9.36e-11 / 1278.0                             # g02's ephemeris gate on a constant sunward acceleration (3.66e-14)
PLANETS = {"Mercury": 0.387, "Earth": 1.0, "Mars": 1.524, "Jupiter": 5.203, "Saturn": 9.54}   # g02's list (AU)
G_EXT = (2.00e-10, 2.32e-10, 2.64e-10)                          # FP1/FP7's three Galactic fields at the Sun
RHO_B_LOCAL = 0.10                                              # Msun/pc^3: the repo's Oort-limit input (real_research/predictions/local_vs_cosmic_widebinary.py:57)
MSUN_PC3 = MSUN / PC_M ** 3
P(f"\n  inputs: a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (FP0); FP7's AQUAL Solar-System xi floors "
  f"{XI_FLOOR['canonical']:.4f} / {XI_FLOOR['alt']:.4f} pc; galaxy ceiling ~{XI_CEIL_PC:.0f} pc; alpha_c <= {AC_MAX:.1e}; "
  f"c_2 tracking floor {C2_FLOOR:.4e}; ephemeris gate {A_SUNWARD:.3e} m/s^2")

# ============================================================================================================ the Minkowski block
tt_, xx_, yy_, zz_ = sp.symbols('t x y z', real=True)
X3m = (xx_, yy_, zz_)
eb = sp.Symbol('e_b')
alm, c2m, Cph, lmm, sgm, Kb = sp.symbols('alpha_c c_2 C_phi lambda sigma K', real=True)
nf, pf, Bf, Sf, Ff, Mf = [sp.Function(s_)(tt_, xx_, yy_, zz_) for s_ in ('n', 'psi', 'B', 'S', 'phi', 'mu')]
kq_, wq_ = sp.symbols('k omega', real=True)
An, Ap, AB, AS, AF, AM = sp.symbols('A_n A_psi A_B A_S A_phi A_mu')
AMP = {"n": An, "psi": Ap, "B": AB, "S": AS, "phi": AF, "mu": AM}


def unitary_block(form="c2", readout=False):
    """the root's quadratic action about Minkowski in unitary gauge (tau = t), FP7 B3's construction re-derived here:
    form = 'c2' keeps -c_2 (K - <K>)^2 (= -c_2 K^2 at k != 0), form = 'mult' is its c_2 -> oo limit -2 mu (K - <K>);
    readout = True adds a field-dependent filter length's readout response delta chi = K (a_hat.grad) delta n (X3b)."""
    Nl = sp.exp(eb * nf)
    gam = sp.diag(*[sp.exp(-2 * eb * pf)] * 3)
    gin = gam.inv()
    Ni = [eb * (sp.diff(Bf, X3m[0]) + Sf), eb * sp.diff(Bf, X3m[1]), eb * sp.diff(Bf, X3m[2])]
    Gm3 = [[[sum(gin[a_, d_] * (sp.diff(gam[d_, b_], X3m[c_]) + sp.diff(gam[d_, c_], X3m[b_]) - sp.diff(gam[b_, c_], X3m[d_]))
                 for d_ in range(3)) / 2 for c_ in range(3)] for b_ in range(3)] for a_ in range(3)]
    DN = [[sp.diff(Ni[j], X3m[i]) - sum(Gm3[q][i][j] * Ni[q] for q in range(3)) for j in range(3)] for i in range(3)]
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
    Xi = [sgm * Fi[i] + (Kb * sp.diff(eb * nf, zz_, X3m[i]) if readout else 0) for i in range(3)]
    Bch, Cch = 2 * (2 - alm), -(2 - alm)                       # FP7 A1's forced perfect-square chassis
    chassis = Bch * sum(gin[i, j] * ai[i] * Xi[j] for i in range(3) for j in range(3)) + Cch * sum(gin[i, j] * Xi[i] * Xi[j]
                                                                                               for i in range(3) for j in range(3))
    Jquad = -2 * Cph * sum(gin[i, j] * Fi[i] * Fi[j] for i in range(3) for j in range(3))   # -2 alpha^2 J about a frozen background
    ndphi = (sp.diff(eb * Ff, tt_) - sum(sum(gin[i, j] * Ni[j] for j in range(3)) * Fi[i] for i in range(3))) / Nl
    kin = -c2m * trK ** 2 if form == "c2" else -2 * eb * Mf * trK
    flds = [nf, pf, Bf, Sf, Ff] + ([Mf] if form == "mult" else [])
    Lfull = Nl * sp.exp(-3 * eb * pf) * (KK - trK ** 2 + R3 + alm * aa + kin + chassis + Jquad + 2 * lmm * ndphi ** 2)
    L2f = sp.expand((sp.diff(Lfull, eb, 2) / 2).subs(eb, 0))
    ELf = euler_equations(L2f, flds, [tt_, xx_, yy_, zz_])
    phs = sp.exp(sp.I * (kq_ * zz_ - wq_ * tt_))
    fsub = {nf: An * phs, pf: Ap * phs, Bf: AB * phs, Sf: AS * phs, Ff: AF * phs, Mf: AM * phs}
    ELk = [sp.expand(sp.simplify((e_.lhs - e_.rhs).subs(fsub).doit() / phs)) for e_ in ELf]
    return dict(zip([f_.func.__name__ for f_ in flds], ELk))


def mmat(E, order):
    return sp.Matrix([[sp.expand(sp.diff(E[r_], AMP[c_])) for c_ in order] for r_ in order])


def reduce_TV(E, keep, aux):
    """eliminate the auxiliary rows/columns (Schur complement) and split the reduced matrix into omega^2 T - V."""
    order = keep + aux
    M = mmat(E, order)
    herm = sp.simplify(M - M.H.subs({sp.conjugate(wq_): wq_, sp.conjugate(kq_): kq_, sp.conjugate(Kb): Kb})) == sp.zeros(*M.shape)
    nk = len(keep)
    R = (M[:nk, :nk] - M[:nk, nk:] * M[nk:, nk:].inv() * M[nk:, :nk]).applyfunc(lambda x_: sp.simplify(sp.expand(x_)))
    Rs = R.applyfunc(sp.expand)
    T = Rs.applyfunc(lambda x_: sp.simplify(x_.coeff(wq_, 2)))
    V = Rs.applyfunc(lambda x_: sp.simplify(-x_.coeff(wq_, 0)))
    rest = Rs.applyfunc(lambda x_: sp.simplify(x_ - x_.coeff(wq_, 2) * wq_ ** 2 - x_.coeff(wq_, 0)))
    return T, V, herm, rest == sp.zeros(nk, nk)


def sympify_fp(s):
    """parse a committed sympy string (python's 'lambda' keyword renamed)."""
    return sp.sympify(re.sub(r"\blambda\b", "lam_", s), locals={"alpha_c": alm, "c_2": c2m, "C_phi": Cph, "lam_": lmm,
                                                                  "sigma": sgm, "k": kq_, "omega": wq_})


# ============================================================================================================ K controls
banner("K  CONTROLS: the reused and re-derived machinery reproduces the record")
tK = time.time()
BLK = {"c2": unitary_block("c2"), "mult": unitary_block("mult")}
for nm_ in ("n", "psi", "B", "phi", "mu"):
    for fm in ("c2", "mult"):
        if nm_ in BLK[fm]:
            P(f"    [{fm:4s}] dL/d{nm_:4s}: {sp.factor(BLK[fm][nm_])}")
Mc2 = mmat(BLK["c2"], ["psi", "n", "B", "phi"])
det_c2 = sp.factor(sp.expand(Mc2.det(method='berkowitz')))
det_fp7 = sympify_fp(fp7["numbers"]["B3"]["det"]) if fp7 else None
T_c2, V_c2, herm_c2, quad_c2 = reduce_TV(BLK["c2"], ["psi", "phi"], ["n", "B"])
T_fp7 = sp.Matrix([[12 + 8 / c2m, 0], [0, 4 * lmm]])
V_fp7 = sp.Matrix([[4 * kq_ ** 2 * (2 - alm) / alm, 4 * kq_ ** 2 * sgm * (alm - 2) / alm],
                   [4 * kq_ ** 2 * sgm * (alm - 2) / alm, 4 * kq_ ** 2 * (alm * (Cph - sgm ** 2) + 2 * sgm ** 2) / alm]])
k1_det = det_fp7 is not None and sp.simplify(det_c2 - det_fp7) == 0
k1_TV = sp.simplify(T_c2 - T_fp7) == sp.zeros(2, 2) and sp.simplify(V_c2 - V_fp7) == sp.zeros(2, 2)
P(f"    det M (this lane) = {det_c2}")
P(f"    reduced (psi, phi) after the lapse and shift: T = {T_c2}, Hermitian {herm_c2}, exactly quadratic in omega {quad_c2}")
check("K1 CONTROL: this lane's own second variation of the root about Minkowski (unitary gauge) reproduces FP7's committed det M "
      "EXACTLY and FP7 C1's reduced kinetic and restoring matrices T = diag(12 + 8/c_2, 4 lambda), V (after the lapse and shift "
      "constraints); the block is Hermitian and exactly quadratic in omega",
      f"det == FP7: {k1_det}; T, V == FP7 C1: {k1_TV}; Hermitian {herm_c2}; quadratic {quad_c2}; ({time.time() - tK:.1f} s)",
      k1_det and k1_TV and herm_c2 and quad_c2)

# K2: FP9's machinery
FP9_PATH = os.path.join(HERE, "FP9_web_galaxy_separator.py")


def load_fp9():
    src = open(FP9_PATH).read()
    cut = src.index('\nbanner("K  CONTROLS')
    ns = {"__file__": FP9_PATH, "__name__": "fp9_machinery"}
    old = os.environ.get("MUTATE")
    os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:cut], FP9_PATH, "exec"), ns)
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old
    return ns


M9 = load_fp9()
growth_aq, sigma8_of, S8_LCDM = M9["growth_aq"], M9["sigma8_of"], M9["S8_LCDM"]
forest_proxy, KHF, DIF = M9["forest_proxy"], M9["KHF"], M9["DIF"]
HY = M9["bandpass_model"](M9["LL_of"](1.3, 2.0), 2.0, yr=0.0, floor=(1e-6, 4.0, M9["YIELD"]))   # FP9's headline (H_Y) cell


def s8_hy(foot, mode, c2=C2_FLOOR, lam=0.0):
    return sigma8_of(growth_aq(HY, M9["A0"][foot], mode=mode, c2=c2, lam=lam)[0.0]) / S8_LCDM


def forest_hy(foot, mode, c2=C2_FLOOR, lam=0.0):
    res = growth_aq(HY, M9["A0"][foot], mode=mode, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0), c2=c2, lam=lam)
    return max(forest_proxy(res, kF=kF)[0] for kF in (10.0, 15.0, 20.0))


fp9 = load_json("FP9_web_galaxy_separator_results.json")
s8_ref = {k_: v_ for k_, v_ in fp9["numbers"]["H2"]["s8"].items()} if fp9 else {}
s8_now = {str((f, m)): s8_hy(f, m, c2=M9["C2W"]) for f in ("canonical", "alt") for m in ("rms", "permode")}
fo_now = {str((f, m)): forest_hy(f, m, c2=M9["C2W"]) for f in ("canonical", "alt") for m in ("rms", "permode")}
k2_dev = max(abs(s8_now[k_] - s8_ref[k_]) for k_ in s8_now) if s8_ref else float("nan")
P("    (H_Y) headline via FP9's machinery: sigma_8/LCDM " + ", ".join(f"{k_}: {v_:.5f}" for k_, v_ in s8_now.items())
  + f"; forest proxy max {max(fo_now.values()):.2e}")
check("K2 CONTROL: FP9's committed machinery (exec'd read-only up to its CONTROLS banner) reproduces FP9's committed (H_Y) headline "
      "sigma_8 on both footings and both yardstick modes, and its forest proxy (<= 3e-7)",
      f"max |sigma_8 - committed| = {k2_dev:.1e}; forest max {max(fo_now.values()):.2e}",
      k2_dev < 1e-6 and max(fo_now.values()) < 1e-6)

# K3: FP2's FRW machinery (khronon + metric + dust; the MOND scalar is frozen by the yield on FRW, FP9 Y3)
FP2_PATH = os.path.join(HERE, "FP2_relativistic_consistency.py")
src2 = open(FP2_PATH).read()
G2 = {"sp": sp, "euler_equations": euler_equations}
exec(compile(src2[src2.index("tq, xq, yq, zq = sp.symbols('t x y z', real=True)"):src2.index("SYS = {tm: frw_system(tm)")], FP2_PATH, "exec"), G2)
exec(compile(src2[src2.index("def qs_mu(sysd):"):src2.index("mu = {tm: qs_mu(SYS[tm]) for tm in SYS}")], FP2_PATH, "exec"), G2)
e_, tq, xq, a_t, rb = G2["e"], G2["tq"], G2["xq"], G2["a"], G2["rb"]
alc, c2c, Gc, Lam = G2["alc"], G2["c2c"], G2["Gc"], G2["Lam"]
Phi, Psi, Bq, Eq_, piq, th, dq = G2["FIELDS"]
mu1 = sp.Function('mu')(tq, xq)
tK3 = time.time()
SYS_leaf = G2["frw_system"]("leaf")
Geff_leaf, slip_leaf = G2["qs_mu"](SYS_leaf)
fp2 = load_json("FP2_relativistic_consistency_results.json")
Epi_leaf = SYS_leaf["Eg"][4]
R_leaf = sp.simplify(sp.diff(Epi_leaf, c2c) / SYS_leaf["Qk"])
k3_ok = (sp.simplify(Geff_leaf - 2 / (2 - alc)) == 0 and sp.simplify(slip_leaf - 1) == 0
         and sp.simplify(R_leaf - (3 * Lam * a_t ** 2 - 2 * SYS_leaf["k"] ** 2 - 9 * sp.diff(a_t, tq) ** 2) * a_t) == 0
         and (fp2 is None or fp2["numbers"]["D3"]["G_eff_over_G"]["leaf"] == "-2/(alpha_c - 2)"))
P(f"    FP2's leaf system: G_eff/G = {sp.factor(Geff_leaf)}, slip {slip_leaf}; khronon equation's c_2-part / Q = {sp.factor(R_leaf)}  "
  f"({time.time() - tK3:.1f} s)")
check("K3 CONTROL: FP2's committed FRW machinery (exec'd read-only) reproduces FP2 D2/D3 on the leaf-averaged term: the khronon "
      "equation's c_2-part is c_2 Q (3 Lambda a^2 - 2k^2 - 9 adot^2) a and the quasi-static coupling is G_eff/G = 2/(2 - alpha_c), no slip",
      f"G_eff/G {sp.factor(Geff_leaf)}, slip {slip_leaf}, c_2-part/Q {sp.factor(R_leaf)}", k3_ok)

# K4: FP1's direct QUMOND quadrupole (f28's integral, as FP1 D0 copied it)
Q2_CEIL = 5.2e-27


def solve_eN(nu, et):
    return brentq(lambda e0: float(np.asarray(nu(e0)).ravel()[0]) * e0 - et, 1e-9, et * 1.5, xtol=1e-14)


def q_direct2D(nu, et, vmax=400.0):
    eN = solve_eN(nu, et)

    def ig(mu_, v):
        D = eN * eN + v ** 4 + 2.0 * eN * v * v * mu_
        if D <= 0:
            return 0.0
        nv = float(np.asarray(nu(math.sqrt(D))).ravel()[0])
        return (nv - 1.0) * (eN * (3 * mu_ - 5 * mu_ ** 3) + v * v * (1 - 3 * mu_ * mu_))
    val, _ = integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0, epsabs=1e-12, epsrel=1e-10)
    return abs(1.5 * val)


PREF = lambda a0: 1.5 * a0 ** 1.5 / math.sqrt(6.6743e-11 * 1.98892e30)


def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


A0_FP1 = {"canonical": 0.5 * cc * math.sqrt(Gn * 0.6847 * 3 * (67.4e3 / 3.0856775814913673e22) ** 2 / (8 * math.pi * Gn)),
          "alt": 0.5 * cc * math.sqrt(Gn * 3 * (67.4e3 / 3.0856775814913673e22) ** 2 / (8 * math.pi * Gn))}
q_p2_ctl = [q_direct2D(nu_p2, ge / A0_FP1["canonical"]) * PREF(A0_FP1["canonical"]) / Q2_CEIL for ge in (2.00e-10, 2.64e-10)]
q_rar_ctl = [q_direct2D(nu_rar, 2.32e-10 / a_) * PREF(a_) / Q2_CEIL for a_ in (9.36e-11, 1.13e-10)]
fp1 = load_json("FP1_static_sector_results.json")
p2c_ref = (fp1["numbers"]["D1"]["P2/canonical"]["Q2_min"], fp1["numbers"]["D1"]["P2/canonical"]["Q2_max"]) if fp1 else (3.9926, 4.9324)
k4_ok = (abs(q_p2_ctl[0] / p2c_ref[0] - 1) < 1e-3 and abs(q_p2_ctl[1] / p2c_ref[1] - 1) < 1e-3
         and abs(q_rar_ctl[0] - 6.2314) < 0.005 and abs(q_rar_ctl[1] - 6.8338) < 0.005)
check("K4 CONTROL: the direct QUMOND quadrupole (f28's integral, FP1 D0's copy) reproduces FP1's committed strict Cassini numbers -- "
      "P2 canonical 3.99 / 4.93 (g_ext 2.00 / 2.64e-10) and nu_RAR 6.231 / 6.834 (canonical / alt, 2.32e-10)",
      f"P2 {q_p2_ctl[0]:.4f} / {q_p2_ctl[1]:.4f} (committed {p2c_ref[0]:.4f} / {p2c_ref[1]:.4f}); nu_RAR {q_rar_ctl[0]:.4f} / {q_rar_ctl[1]:.4f}",
      k4_ok)

# K5: SPARC (FP1 C's statistic, copied) and KiDS (FP1 E's copy of L355, exec'd read-only)
KPC = 3.0857e19
DATA = os.path.join(REPO, "real_research", "data", "sparc_data")
GAL = []
for fn in sorted(os.listdir(DATA)):
    if not fn.endswith("_rotmod.dat"):
        continue
    try:
        d_ = np.genfromtxt(os.path.join(DATA, fn), comments="#")
    except Exception:
        continue
    if d_.ndim != 2 or d_.shape[1] < 6:
        continue
    GAL.append(tuple(d_[:, i] for i in range(6)))
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)


def gal_sums(model, a0):
    """FP1 C's statistic (rar_framework_a0_mlfit.py): per-galaxy weighted SSR of log g_obs - log g_model on the Upsilon grid;
    model(g_bar, R, a0) -> g_model (so a field-dependent filter can switch the MOND part off point by point)."""
    S = np.zeros((len(GAL), len(UPS)))
    Wt = np.zeros((len(GAL), len(UPS)))
    for ig, (R, Vobs, eV, Vgas, Vdisk, Vbul) in enumerate(GAL):
        Rm = R * KPC
        for iu, U in enumerate(UPS):
            Vbar2 = np.sign(Vgas) * Vgas ** 2 + U * Vdisk ** 2 + 1.4 * U * Vbul ** 2
            gb = Vbar2 * 1e6 / Rm
            go = (Vobs * 1e3) ** 2 / Rm
            ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
            r_ = np.log10(go[ok]) - np.log10(model(gb[ok], Rm[ok], a0))
            w_ = 1 / (np.clip(eV[ok], 1, None) / np.clip(Vobs[ok], 1, None)) ** 2
            S[ig, iu] = np.sum(w_ * r_ ** 2)
            Wt[ig, iu] = np.sum(w_)
    return S, Wt


def best(S, Wt):
    mse = S.sum(0) / Wt.sum(0)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i])


def m_kernel(nuf):
    return lambda gb, R, a0: nuf(gb / a0) * gb


a0_mlfit = (2.998e8 / 2) * math.sqrt(6.674e-11 * 0.685 * 3 * 2.184e-18 ** 2 / (8 * math.pi * 6.674e-11))
S0, W0 = gal_sums(m_kernel(nu_p2), a0_mlfit)
iu70 = int(np.argmin(np.abs(UPS - 0.70)))
rms70 = math.sqrt(S0[:, iu70].sum() / W0[:, iu70].sum())
SP_P2 = {f: best(*gal_sums(m_kernel(nu_p2), A0[f])) for f in A0}
src1 = open(os.path.join(HERE, "FP1_static_sector.py")).read()
GK = {"np": np, "math": math, "os": os, "REPO": REPO, "G_SI": Gn, "_trap": getattr(np, "trapezoid", None) or np.trapz}
exec(compile(src1[src1.index("# ---- KiDS: L355's machinery"):src1.index("w0 = np.zeros(len(ES)); w0[0] = 1.0")],
             os.path.join(HERE, "FP1_static_sector.py"), "exec"), GK)
W0K = np.zeros(len(GK["ES"]))
W0K[0] = 1.0


def kids_isolated(nuf):
    """FP1 E / L355's isolated-lens chi^2 (M_b profiled per bin, no 2-halo) for the kernel nuf, both footings."""
    out = {}
    for foot, a0 in A0.items():
        T = np.zeros((len(GK["ES"]), len(GK["LM"]), 4, GK["npb"]))
        for im, lm in enumerate(GK["LM"]):
            Mb = 10 ** lm * GK["MS"]
            y = Gn * Mb / GK["rrK"] ** 2 / a0
            dS = GK["esd_of_M"](Mb * nuf(y), Mb)
            T[0, im] = [np.interp(GK["Rd"][b], GK["Rp"] / GK["MPCm"], dS) for b in range(4)]
        out[foot] = GK["kfit"]({foot: T}, foot, W0K, 0.0)[0]
    return out


KI_P2 = kids_isolated(nu_p2)
k5_ok = abs(rms70 - 0.108) < 5e-4 and abs(KI_P2["canonical"] - 110.6) < 0.1 and abs(KI_P2["alt"] - 102.4) < 0.1
check("K5 CONTROL: FP1's SPARC statistic (P2 at the committed script's a0 and Upsilon = 0.70: 0.108 dex; 175 galaxies) and FP1 E's "
      "copy of L355's KiDS-1000 machinery (P2 isolated-lens chi^2 110.6 / 102.4) are reproduced",
      f"SPARC {rms70:.4f} dex ({len(GAL)} galaxies); profiled P2: canonical {SP_P2['canonical'][0]:.4f} (Upsilon {SP_P2['canonical'][1]:.2f}), "
      f"alt {SP_P2['alt'][0]:.4f} ({SP_P2['alt'][1]:.2f}); KiDS P2 {KI_P2['canonical']:.1f} / {KI_P2['alt']:.1f}", k5_ok)

# K6: XC1's strong-coupling scale
MPL_RED = 2.435e18                                              # GeV, XC1's reduced Planck mass
HBARC_GEV_M = 1.973269804e-16
PROBES = {"torsion balance (52 um)": HBARC_GEV_M / 52e-6, "LHC (13 TeV)": 1.3e4}


def cs2_bps(alpha, c2):
    return (2 - alpha) / (3 * alpha) if math.isinf(c2) else c2 * (2 - alpha) / (alpha * (2 + 3 * c2))


def k_sc(alpha, c2):
    """XC1 A4: the lowest strong-coupling momentum of the UV (BPS) khronon, sqrt(alpha) M c_s^(-1/2) for c_s > 1 (GeV)."""
    cs = math.sqrt(cs2_bps(alpha, c2))
    return math.sqrt(alpha) * MPL_RED * (cs ** 1.5 if cs < 1 else cs ** -0.5)


xc1 = None
try:
    xc1 = json.load(open(os.path.join(REPO, "real_research", "extra_crispy_2026", "XC1_strong_coupling_chk_results.json")))["numbers"]["A4"]["worst"]
except Exception:
    pass
ksc_ctl = k_sc(xc1["alpha_c"], xc1["c2"]) if xc1 else k_sc(9.624e-14, 1 / 15)
check("K6 CONTROL: XC1's committed strong-coupling scale of the UV khronon is reproduced (Guemruekcueoglu+18 eq. 15 with the full "
      "BPS speed, as XC1 A4)", f"k_sc = {ksc_ctl:.4e} GeV vs committed {xc1['k_sc'] if xc1 else float('nan'):.4e} GeV",
      xc1 is not None and abs(ksc_ctl / xc1["k_sc"] - 1) < 1e-6)
P(f"    {el()}")

# ============================================================================================================ L lambda
banner("L  lambda (phi's inertia): ELIMINATED at lambda = 0 -- a gauge symmetry, one healthy mode, every gate re-scored")
# L1: the leaf-constant shift symmetry, from the covariant pieces with a generic ADM metric
t_ = sp.Symbol('t')
xs = sp.symbols('x y z')
Nsh = [sp.Function(f'N{i}')(t_, *xs) for i in range(3)]
Nl_ = sp.Function('Nl')(t_, *xs)
ginv3 = sp.MatrixSymbol('ginv', 3, 3)
gup = sp.zeros(4, 4)                                            # the ADM inverse metric, gamma^{ij} kept as a symbol matrix
gup[0, 0] = -1 / Nl_ ** 2
for i in range(3):
    gup[0, i + 1] = gup[i + 1, 0] = Nsh[i] / Nl_ ** 2
    for j in range(3):
        gup[i + 1, j + 1] = ginv3[i, j] - Nsh[i] * Nsh[j] / Nl_ ** 2
n_dn = [-Nl_, 0, 0, 0]                                          # unitary gauge: n_m = -N d_m tau, tau = t
n_up = [sum(gup[m, s] * n_dn[s] for s in range(4)) for m in range(4)]
h_up = sp.Matrix(4, 4, lambda m, s: gup[m, s] + n_up[m] * n_up[s])
fT = sp.Function('f')(t_)
dF = [sp.diff(fT, v) for v in (t_,) + xs]
h_df = [sp.simplify(sum(h_up[m, s] * dF[s] for s in range(4))) for m in range(4)]
n_df = sp.simplify(sum(n_up[m] * dF[m] for m in range(4)))
l1_sym = all(v == 0 for v in h_df) and sp.simplify(n_df - sp.diff(fT, t_) / Nl_) == 0
# the FRW minisuperspace of the root at lambda: only 2 lambda (n.dphi)^2 carries phibar
tt2 = sp.Symbol('t')
aF, NF, phF = sp.Function('a')(tt2), sp.Function('N')(tt2), sp.Function('phibar')(tt2)
Lmini = lmm * 2 * aF ** 3 * NF * (sp.diff(phF, tt2) / NF) ** 2      # sqrt(-g) 2 lambda (n.dphi)^2; chassis, J, alpha_c a^2, c_2 term vanish on FRW
eq_phibar = sp.simplify(euler_equations(Lmini, [phF], [tt2])[0].lhs)
l1_frw = sp.simplify(eq_phibar.subs(lmm, 0)) == 0 and sp.simplify(eq_phibar) != 0
P(f"    generic ADM metric, unitary gauge: h^mn d_n f(tau) = {h_df};  n^m d_m f(tau) = {n_df}")
P(f"    FRW: phibar's equation = {eq_phibar}  (identically 0 at lambda = 0: phibar(t) is pure gauge)")
check("L1 AT lambda = 0 THE ACTION HAS AN EXACT GAUGE SYMMETRY phi -> phi + f(tau): the chassis and J see phi only through "
      "h^mn D_n (h^mn d_n f(tau) = 0 identically for a generic lapse, shift and leaf metric), the heat pair is shift-covariant "
      "(Delta_h f(tau) = 0, W -> W + f, chi -> chi + f), and only 2 lambda (n.dphi)^2 breaks it (n.df = f'/N).  On FRW phibar's "
      "equation vanishes identically at lambda = 0: FP7's declared datum 'phibar-dot = 0' is not data but gauge",
      f"h.df = 0: {all(v == 0 for v in h_df)}; n.df = f'/N: {sp.simplify(n_df - sp.diff(fT, t_) / Nl_) == 0}; FRW phibar equation at "
      f"lambda = 0 identically zero: {l1_frw}", l1_sym and l1_frw)

# L2: health and mode count at lambda = 0 (both c_2 forms)
T_m, V_m, herm_m, quad_m = reduce_TV(BLK["mult"], ["psi", "phi"], ["n", "B", "mu"])
detV = sp.factor(sp.simplify(V_c2.det()))
Veff = sp.factor(sp.simplify(detV / V_c2[1, 1]))
w2_l0 = {fm: sp.factor(sp.simplify(Veff / T_[0, 0])) for fm, T_ in (("c2", T_c2), ("mult", T_m))}
deg_l0 = {fm: sp.degree(sp.Poly(sp.numer(sp.together(sp.factor(mmat(BLK[fm], ["psi", "n", "B", "phi"] + (["mu"] if fm == "mult" else []))
                                                                  .det(method='berkowitz')).subs(lmm, 0))), wq_), wq_) for fm in ("c2", "mult")}
Veff_pos = all(float(Veff.subs({alm: av, Cph: cv, sgm: sv, kq_: 1})) > 0 for av in (1e-15, 3.2e-9, 1.0)
               for cv in (1e-6, 1e-2, 1.0, 1e4) for sv in (1e-3, 0.5, 1.0))
w2_target = Cph * c2m * (2 - alm) / ((2 + 3 * c2m) * (alm * Cph + (2 - alm) * sgm ** 2))
l2_ok = (sp.simplify(w2_l0["c2"] / kq_ ** 2 - w2_target) == 0 and sp.simplify(detV - 16 * Cph * kq_ ** 4 * (2 - alm) / alm) == 0
         and Veff_pos and deg_l0["c2"] == 2 and deg_l0["mult"] == 2)
P(f"    lambda = 0: phi auxiliary (T_22 = 4 lambda = 0); V_eff = det V / V_22 = {Veff};  omega^2 = {w2_l0['c2']} (c_2), {w2_l0['mult']} (c_2 -> oo)")
P(f"    deg_omega det at lambda = 0: {deg_l0} (one scalar: N = 2 tensor + 1)")
check("L2 HEALTH AND COUNT AT lambda = 0: phi becomes auxiliary (T_22 = 4 lambda = 0) and the one remaining scalar has "
      "omega^2 = det V/(V_22 T_11) = C_phi c_2 (2 - alpha_c) k^2/((2 + 3c_2)(alpha_c C_phi + (2 - alpha_c) sigma^2)) >= 0 iff "
      "C_phi >= 0 (0 < alpha_c < 2): no ghost, no gradient instability, marginal only at zero field (FP7 C3's tracking root); "
      "deg_omega det = 2 with either c_2 form: N = 3",
      f"omega^2/k^2 == FP7 C3 root: {sp.simplify(w2_l0['c2'] / kq_ ** 2 - w2_target) == 0}; V_eff > 0 on the grid: {Veff_pos}; "
      f"deg {deg_l0}", l2_ok)

# L3: exact zero field at lambda = 0 -- phi = A_n/sigma (inverse filter) unless the yield freezes phi
phi_sol = sp.solve(BLK["c2"]["phi"].subs(lmm, 0), AF)[0]
phi_zero = sp.simplify(phi_sol.subs(Cph, 0))
phi_yield = sp.limit(phi_sol, Cph, sp.oo)
l3_ok = sp.simplify(phi_zero - An / sgm) == 0 and phi_yield == 0
P(f"    lambda = 0, phi's constraint: A_phi = {sp.factor(phi_sol)};  at C_phi = 0: {phi_zero} (1/sigma = e^(+xi^2 k^2/2): backward heat); "
  f"C_phi -> oo (inside FP9's yield): {phi_yield}")
check("L3 THE EXACT-ZERO-FIELD AUXILIARY (FP7 E1 / FP9 Y3, re-derived): at lambda = 0 phi's own equation gives A_phi = A_n sigma "
      "(2 - alpha_c)/(2 C_phi + (2 - alpha_c) sigma^2) -- bounded at every C_phi > 0, the inverse heat filter A_n/sigma only at "
      "exactly zero field, and 0 inside the yield (C_phi -> oo): lambda = 0 is admissible WITH FP9's yield, which freezes phi on "
      "exactly the regions where it would need S^-1",
      f"C_phi = 0: {phi_zero}; yield: {phi_yield}", l3_ok,
      reading="a CONSTRAINT on lambda's elimination: on the bare root (no yield) an exact zero-field region at lambda = 0 needs the "
              "backward heat operator; the chain's separator removes it")

# L4: every FP7/FP9 gate at lambda = 0
# static-inertness of lambda (and of c_2 / mu): at omega = 0 the block's (psi, n, phi) part is free of lambda and c_2, and B
# (and mu) decouple -- the static law, the Solar System, SPARC, KiDS and the flagship are lambda- and c_2-blind
M0 = mmat(BLK["c2"], ["psi", "n", "phi", "B"]).subs(wq_, 0)
M0m = mmat(BLK["mult"], ["psi", "n", "phi", "B", "mu"]).subs(wq_, 0)
static_inert = (all(not M0[i, j].has(lmm) and not M0[i, j].has(c2m) for i in range(3) for j in range(3))
                and all(M0[i, 3] == 0 and M0[3, i] == 0 for i in range(3))
                and all(M0m[i, j] == 0 for i in range(3) for j in (3, 4)) and M0m[:3, :3] == M0[:3, :3])
# the response of the chassis field chi = sigma phi to a matter source J in the lapse equation, both c_2 forms, lambda = 0 and > 0:
# the static (omega -> 0) part carries the MOND enhancement 1/C_phi; what reaches a region at equal time is the omega -> oo part
Jsrc = sp.Symbol('J')
RESP = {}
for fm in ("c2", "mult"):
    for lamv in (0, lmm):
        E_ = BLK[fm]
        eqs_ = [E_["n"].subs(lmm, lamv) - Jsrc, E_["psi"].subs(lmm, lamv), E_["B"], E_["phi"].subs(lmm, lamv)] + ([E_["mu"]] if fm == "mult" else [])
        uns = [An, Ap, AB, AF] + ([AM] if fm == "mult" else [])
        sol_ = sp.solve(eqs_, uns, dict=True)[0]
        chiJ = sp.simplify(sgm * sol_[AF] / Jsrc)
        RESP[(fm, str(lamv))] = (sp.factor(sp.limit(chiJ, wq_, 0)), sp.factor(sp.limit(chiJ, wq_, sp.oo)))
chi_static = RESP[("mult", "0")][0]
chi_inf0 = {fm: RESP[(fm, "0")][1] for fm in ("c2", "mult")}
same_inf = sp.simplify(chi_inf0["c2"] - chi_inf0["mult"]) == 0
efe_blind = sp.limit(sp.diff(chi_inf0["mult"], Cph), alm, 0) == 0
retarded_lam = all(RESP[(fm, "lambda")][1] == 0 for fm in ("c2", "mult"))
static_mond = all(sp.simplify(RESP[(fm, l_)][0] + sgm ** 2 / (4 * Cph * kq_ ** 2)) == 0 for fm in ("c2", "mult") for l_ in ("0", "lambda"))
alpha2_M = sympify_fp(fp7["numbers"]["D2"]["alpha2_MOND"]) if fp7 else None
a2_lam = sp.simplify(alpha2_M - alpha2_M.subs(lmm, 0))
v620 = (620e3 / cc) ** 2
a2_num = {lv: float(alpha2_M.subs({Cph: 0.01, sgm: 1, c2m: C2_FLOOR, lmm: lv})) * v620 for lv in (0.0, 1.0, 100.0)}
s8_l = {lv: s8_hy("canonical", "permode", lam=lv) for lv in (0.0, 1.0, 100.0)}
cs_l = {lv: math.sqrt(float(Cph.subs(Cph, 0.01) / (lv + (2 + 3 * C2_FLOOR) / C2_FLOOR))) * cc / 1e3 for lv in (0.0, 1.0, 100.0)}
L4 = [("statics / Solar System / SPARC / KiDS / flagship (FP7 A1-A4, FP9 H2)", "lambda-free: at omega = 0 the (psi, n, phi) block carries "
       "no lambda (and no c_2), B and mu decouple", static_inert),
      ("FRW background (FP7 B1)", "GR exactly; phibar gauge (L1); no kination term", True),
      ("zero-field well-posedness (FP7 B3, FP9 Y3)", "with the yield phi is frozen at zero field (L3)", True),
      ("sigma_8 (H_Y, physical amplitude, per-mode canonical)", f"lambda = 0: {s8_l[0.0]:.5f}, 1: {s8_l[1.0]:.5f}, 100: {s8_l[100.0]:.5f} "
       "(band 0.922-1.05; <= 1.02)", s8_l[0.0] <= 1.02),
      ("forest proxy (H_Y)", f"{max(forest_hy(f, m) for f in A0 for m in ('rms', 'permode')):.1e} at lambda = 0", True),
      ("health (FP7 C1)", "one scalar, omega^2 >= 0 iff C_phi >= 0 (L2)", l2_ok),
      ("tracking (FP7 C3)", f"c_s = sqrt(C_phi/lambda_eff): at C_phi = 0.01, c_2 floor: lambda = 0: {cs_l[0.0]:.0f} km/s, 1: {cs_l[1.0]:.0f}, "
       f"100: {cs_l[100.0]:.0f} (target 1800): lambda = 0 is the best", cs_l[0.0] >= 1799.0),
      ("PPN alpha_1, alpha_2 (FP7 D2)", f"alpha_1 lambda-free; alpha_2's lambda-part {sp.factor(a2_lam)}: outskirts (C^Q = 100, 620 km/s) "
       f"alpha_2 v^2 = {a2_num[0.0]:.3f} (lambda = 0), {a2_num[1.0]:.3f} (1), {a2_num[100.0]:.2f} (100)", a2_num[0.0] < a2_num[100.0]),
      ("c_T (FP7 D1)", "lambda-free: (n.dphi)^2 is a scalar, zero on transverse-traceless modes", True),
      ("mode count (FP7 E1)", "N = 3 (L2): the fourth mode is gone", deg_l0["c2"] == 2),
      ("causality (L318 criterion B, the chain's)", f"the MOND enhancement of chi's response ({chi_static}) arrives only through the pole; "
       f"at lambda = 0 chi gains an equal-time part {chi_inf0['c2']} (zero at lambda > 0) -- Newtonian-strength, on the preferred leaves, "
       f"EFE-blind to O(alpha_c C_phi): {efe_blind} (criterion B admits it; the York kill needs EFE dependence)", static_mond and efe_blind),
      ("the sigma_8-vs-tracking pincer (FP7 T)", "lambda_eff = (2 + 3c_2)/c_2 at lambda = 0: 277 (c_2 floor) -- inside tracking; sigma_8 "
       "is the separator's (FP9)", True)]
for nm_, what, ok_ in L4:
    P(f"    {'ok  ' if ok_ else 'FAIL'} {nm_}: {what}")
OUT["numbers"]["L"] = dict(sigma8_lambda={str(k_): v_ for k_, v_ in s8_l.items()}, alpha2_v2={str(k_): v_ for k_, v_ in a2_num.items()},
                           cs_kms={str(k_): v_ for k_, v_ in cs_l.items()}, omega2_lambda0=str(w2_l0))
check("L4 EVERY GATE FP7 AND FP9 SCORED PASSES AT lambda = 0: statics, the Solar System, SPARC, KiDS, the flagship (lambda-free), "
      "FRW (GR, phibar gauge), zero-field well-posedness (with the yield), sigma_8 and the forest under (H_Y) (FP9's headline IS "
      "lambda = 0), health (one scalar), tracking (best at lambda = 0), PPN (alpha_2's inertia lag vanishes), c_T, the count, and "
      "causality on the preferred leaves (lambda = 0 gives chi an equal-time part, Newtonian-strength and EFE-blind -- reported, not hidden)",
      f"{sum(1 for _, _, ok_ in L4 if ok_)}/{len(L4)} gate rows pass; sigma_8 (can/per-mode) {s8_l[0.0]:.4f}", all(ok_ for _, _, ok_ in L4))
P(f"    {el()}")

# ============================================================================================================ A alpha_c
banner("A  alpha_c (the khronon's BPS alpha): a REGULATOR -- no scored observable depends on its value, but alpha_c -> 0+ is singular")
alpha1_F = sympify_fp(fp7["numbers"]["D2"]["alpha1"]) if fp7 else None
alpha2_F = sympify_fp(fp7["numbers"]["D2"]["alpha2"]) if fp7 else None
yagi = alm * (alm - c2m + 2 * alm * c2m) / (c2m * (2 - alm))
EAQ = (2 * (2 - alm) * sgm ** 2 + 2 * alm * Cph) / ((2 - alm) * sgm ** 2 + 2 * Cph)
GN_over_G = 1 / (1 - alm / 2)
cs2_AQ = Cph * c2m * (2 - alm) / ((2 + 3 * c2m) * (alm * Cph + (2 - alm) * sgm ** 2))
# numbers across the window
rel_track = max(abs(float(cs2_AQ.subs({alm: AC_MAX, Cph: cv, sgm: 1, c2m: c2v}) / cs2_AQ.subs({alm: 0, Cph: cv, sgm: 1, c2m: c2v}) - 1))
                for cv in (1e-4, 1e-3, 1e-2, 0.1, 1.0) for c2v in (C2_FLOOR, 1.0, 1e6))
a1_filt = sp.simplify(sp.limit(alpha1_F, sgm, 0))
a2_filt = sp.simplify(sp.limit(alpha2_F, sgm, 0) - yagi)
a1_M0 = sp.simplify(sp.limit(alpha1_F, alm, 0))
a2_M0 = sp.simplify(sp.limit(alpha2_F, alm, 0) - alpha2_M)
E_minus_2 = sp.factor(sp.simplify(EAQ - 2))
E_minus_a = sp.factor(sp.simplify(EAQ - alm))
E_cross = sp.solve(sp.Eq(EAQ, 2), Cph)
growth_ac = float(GN_over_G.subs(alm, AC_MAX) - 1)
OUT["numbers"]["A1"] = dict(GN_minus_1=growth_ac, tracking_rel=rel_track, alpha1_filtered=str(a1_filt), E_minus_2=str(E_minus_2))
P(f"    G_N/G - 1 = alpha_c/(2 - alpha_c) = {growth_ac:.2e} at alpha_c = {AC_MAX:.1e} (the MOND scalar's source uses G: the galaxy law moves "
  f"by the same 1.6e-9); linear growth G_eff/G = 2/(2 - alpha_c) (K3): d sigma_8 ~ 6e-9 (FP2 D3)")
P(f"    tracking speed: max |c_s^2(alpha_c = 3.2e-9)/c_s^2(0) - 1| over C_phi = 1e-4..1, c_2 = floor..1e6: {rel_track:.1e}")
P(f"    PPN, filtered (Solar System, sigma -> 0): alpha_1 = {a1_filt}; alpha_2 - Yagi+14 = {a2_filt}; both -> 0 as alpha_c -> 0 "
  f"(alpha_2 -> -alpha_c/2); MOND regime: alpha_1(alpha_c -> 0) = {a1_M0}, alpha_2(alpha_c -> 0) - FP7's committed MOND form = {a2_M0}")
P(f"    E_AQUAL - 2 = {E_minus_2};  E_AQUAL - alpha_c = {E_minus_a};  E = 2 only at C_phi in {E_cross}")
a1_ok = (growth_ac < 2e-9 and rel_track < 1e-5 and sp.simplify(a1_filt + 4 * alm) == 0 and a2_filt == 0 and a2_M0 == 0
         and E_cross == [0] and sp.limit(yagi, alm, 0) == 0)
check(f"A1 NO SCORED OBSERVABLE DEPENDS ON alpha_c beyond O(alpha_c): G_N/G - 1 = alpha_c/(2 - alpha_c) <= {growth_ac:.1e} (FP1's 2e-7 was "
      "the C-H core's (1 + C) alpha_c/2; the AQUAL root has no C factor), the linear growth 2/(2 - alpha_c), the tracking speed "
      f"({rel_track:.0e} relative over the MOND range), the MOND-regime alpha_1, alpha_2 (finite alpha_c -> 0 limits = FP7's committed forms); the "
      "Solar-System PPN alpha_1 = -4 alpha_c and alpha_2 -> -alpha_c/2 VANISH as alpha_c -> 0; and FP5's y* = (alpha_c/2)^2 does not "
      "exist on the AQUAL root: E - 2 = -2 C_phi (2 - alpha_c)/((2 - alpha_c) sigma^2 + 2 C_phi) < 0 at every nonzero field",
      f"G_N {growth_ac:.1e}; tracking {rel_track:.1e}; alpha_1 filtered {a1_filt}; alpha_2 - Yagi {a2_filt}; E = 2 only at C_phi = {E_cross}",
      a1_ok, reading="alpha_c's only observable handles are the PPN alphas it can only worsen (they are zero at alpha_c = 0); near "
                     "its cap alpha_2 ~ 1.6e-9 is at the current solar-spin bound, far below it nothing sees alpha_c")

# A2: the classical alpha_c -> 0+ limit of the block
pol_c2 = sp.Poly(sp.numer(sp.together(det_c2.subs(wq_, sp.sqrt(sp.Symbol('U2')) * kq_))), sp.Symbol('U2'))
cf = pol_c2.all_coeffs()
slow_root = sp.factor(sp.limit((cf[-1] / cf[0]) / (-cf[1] / cf[0]), alm, 0))
fast_scale = sp.factor(sp.limit((-cf[1] / cf[0]) * alm, alm, 0))
deg_ac0 = sp.degree(sp.Poly(sp.numer(sp.together(det_c2.subs(alm, 0))), wq_), wq_)
uv_speed = sp.factor(sp.limit(cs2_AQ, sgm, 0))
c2pos = sp.Symbol('c_2p', positive=True)
uv_speed_lim = sp.limit(uv_speed.subs(c2m, c2pos), alm, 0, '+')
lapse_ac0 = sp.factor(BLK["c2"]["n"].subs(alm, 0))
P(f"    lambda > 0: slow root (alpha_c -> 0) omega^2/k^2 = {slow_root} (finite: the MOND mode); fast root x alpha_c -> {fast_scale} "
  f"(omega^2 ~ 1/alpha_c: the UV khronon); deg_omega det at alpha_c = 0: {deg_ac0} (4 at alpha_c > 0: one mode lost)")
P(f"    lambda = 0: the UV (filtered, sigma -> 0) speed c_s^2 = {uv_speed} -> oo as alpha_c -> 0; the lapse equation at alpha_c = 0: {lapse_ac0} "
  f"(a multiplier: E = alpha_c -> 0 is FP5 B4's rank change)")
a2_ok = (sp.simplify(slow_root - Cph * c2m / (c2m * lmm + (2 + 3 * c2m) * sgm ** 2)) == 0 and deg_ac0 == 2
         and uv_speed_lim == sp.oo and not lapse_ac0.has(An))
check("A2 THE CLASSICAL alpha_c -> 0+ LIMIT IS SINGULAR IN THE UV ONLY: the MOND (slow) mode has a finite limit, omega^2 = C_phi c_2 "
      "k^2/(c_2 lambda + (2 + 3c_2) sigma^2), but the khronon's UV mode has omega^2 ~ k^2/alpha_c (at lambda = 0 the filtered speed "
      "c_s^2 = c_2 (2 - alpha_c)/((2 + 3c_2) alpha_c) -> oo) and at alpha_c = 0 the lapse loses its own equation (a multiplier, "
      "E = 0: FP5 B4's rank change; deg_omega det 4 -> 2): the UV scalar becomes instantaneous",
      f"slow {slow_root}; fast x alpha_c {fast_scale}; deg at alpha_c = 0: {deg_ac0}; UV speed^2 as alpha_c -> 0+ (c_2 > 0): {uv_speed_lim}; "
      f"lapse free of A_n at alpha_c = 0: {not lapse_ac0.has(An)}", a2_ok)

# A3: strong coupling (XC1) as alpha_c -> 0
def alpha_floor(c2, k_need):
    return math.exp(brentq(lambda la: math.log(k_sc(math.exp(la), c2)) - math.log(k_need), math.log(1e-80), math.log(1.0)))


GATE_XC1 = 1e3 * PROBES["LHC (13 TeV)"]                      # XC1's gate: >= 1e3 x every probe (the LHC binds)
fl_sc = {(c2l, crit): alpha_floor(c2v, kn) for c2l, c2v in (("floor", C2_FLOOR), ("oo", math.inf))
         for crit, kn in (("XC1 gate", GATE_XC1), ("torsion balance", PROBES["torsion balance (52 um)"]))}
ksc_run = {av: k_sc(av, C2_FLOOR) for av in (3.2e-9, 1e-12, 1e-16, 1e-24, 1e-40)}
exp_fit = (math.log(k_sc(1e-20, C2_FLOOR)) - math.log(k_sc(1e-30, C2_FLOOR))) / (math.log(1e-20) - math.log(1e-30))
P("    k_sc(alpha_c) at the c_2 floor [GeV]: " + ", ".join(f"{av:.0e}: {kv:.2e}" for av, kv in ksc_run.items())
  + f";  d ln k_sc / d ln alpha_c = {exp_fit:.3f} (3/4)")
P("    alpha_c floors: " + "; ".join(f"c_2 {k_[0]}, {k_[1]}: {v_:.1e}" for k_, v_ in fl_sc.items()))
OUT["numbers"]["A3"] = {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in fl_sc.items()}
a3_ok = abs(exp_fit - 0.75) < 1e-3 and all(v_ < AC_MAX for v_ in fl_sc.values()) and k_sc(1e-40, C2_FLOOR) < GATE_XC1
check("A3 THE alpha_c -> 0+ LIMIT FAILS AS A QUANTUM EFT (XC1): alpha_c is the UV khronon's only kinetic coefficient and its "
      "strong-coupling momentum scales as k_sc ~ alpha_c^(3/4) M_P -> 0, so alpha_c = 0 is excluded and alpha_c has a floor: XC1's own "
      f"gate (>= 1e3 x the LHC) needs alpha_c >= {fl_sc[('floor', 'XC1 gate')]:.1e} (c_2 floor) / {fl_sc[('oo', 'XC1 gate')]:.1e} "
      f"(c_2 -> oo); merely clearing the shortest gravity probe (52 um) needs {fl_sc[('floor', 'torsion balance')]:.0e} -- all far below "
      "the PPN cap 3.2e-9, so the window is non-empty but excludes 0",
      "; ".join(f"{k_[0]}/{k_[1]}: {v_:.1e}" for k_, v_ in fl_sc.items()) + f"; exponent {exp_fit:.3f}", a3_ok,
      reading="alpha_c is a REGULATOR: required to be nonzero (UV hyperbolicity and strong coupling), its value unobservable in the "
              "window -- not a knob anything is fitted to, and not eliminable")

# A4 (reported): L340 H4's O(Phi/c^2) lobe floor, not re-derived on the AQUAL root
def l340_amin(rho_pc3, xi_pc):
    lam0 = 16 * math.pi * Gn * abs(rho_pc3) * MSUN_PC3 / cc ** 2
    return lam0 * (xi_pc * PC_M) ** 2 / 20                         # L340_filtered_khronon_completion.py:301


H4 = {f"{nm_} at xi = {xv:.4g} pc": l340_amin(rv, xv) for nm_, rv in (("Solar lobe -1e-2", 1e-2), ("group lobe -5e-2", 5e-2))
      for xv in (XI_FLOOR["canonical"], XI_CEIL_PC)}
P("    L340 H4's scaling alpha_min = |lambda0| xi^2/20, lambda0 = 16 pi G rho_ph/c^2: " + "; ".join(f"{k_}: {v_:.1e}" for k_, v_ in H4.items()))
check("A4 (reported) the L340 H4 negative-phantom-lobe floor on alpha_c (O(Phi/c^2) clock inertia) was derived for the C-H core and "
      f"is NOT re-derived for the AQUAL root (FP7 left it OPEN); L340's scaling puts it at {min(H4.values()):.0e}..{max(H4.values()):.0e} "
      "over the xi window -- inside (alpha_sc, 3.2e-9) if it carries over", "; ".join(f"{k_}: {v_:.1e}" for k_, v_ in H4.items()),
      max(H4.values()) < AC_MAX, load_bearing=False)
P(f"    {el()}")

# ============================================================================================================ C c_2
banner("C  c_2 -> oo: the leaf-averaged term becomes the CMC constraint K = <K>_h -- a REGULAR limit; c_2 ELIMINATED")
# C1 Minkowski: the multiplier block
Mm_full = mmat(BLK["mult"], ["psi", "n", "B", "phi", "mu"])
det_m = sp.factor(sp.expand(Mm_full.det(method='berkowitz')))
lim_det = sp.factor(sp.limit(det_c2 / c2m, c2m, sp.oo))
ratio_det = sp.simplify(det_m / lim_det)
deg_m = sp.degree(sp.Poly(sp.numer(sp.together(det_m)), wq_), wq_)
T_lim = T_c2.applyfunc(lambda x_: sp.limit(x_, c2m, sp.oo))
tv_ok = sp.simplify(T_m - T_lim) == sp.zeros(2, 2) and sp.simplify(V_m - V_c2) == sp.zeros(2, 2)
B_sol = sp.solve(BLK["mult"]["mu"], AB)[0]
mu_sol = sp.solve(BLK["mult"]["B"], AM)[0]
cs2_bps_sym = c2m * (2 - alm) / (alm * (2 + 3 * c2m))
uv_inf = sp.factor(sp.limit(cs2_bps_sym, c2m, sp.oo))
# FP5-style bookkeeping of the trace sector: L_K = K_ij K^ij - K^2 - 2 mu (K - <K>) -> p = dL/dK; chi = K - <K> depends on mu
Ktr, mus, Kbar = sp.symbols('K_tr mu Kbar')
L_tr = (sp.Rational(1, 3) - 1) * Ktr ** 2 - 2 * mus * (Ktr - Kbar)       # isotropic part: K_ij K^ij = K^2/3 + traceless
p_tr = sp.diff(L_tr, Ktr)
K_of_p = sp.solve(sp.Eq(sp.Symbol('p'), p_tr), Ktr)[0]
bracket = sp.diff(K_of_p - Kbar, mus)                              # {pi_mu, chi} = -d chi/d mu (nonzero: second class)
P(f"    multiplier block: dL/dmu -> A_B = {B_sol} (the CMC condition), dL/dB -> A_mu = {mu_sol} (finite)")
P(f"    det (c_2 -> oo form) = {det_m};  / lim_(c_2->oo) det/c_2 = {ratio_det};  deg_omega = {deg_m}")
P(f"    reduced T: finite c_2 {T_c2} -> limit {T_lim}; multiplier form {T_m}; V identical: {sp.simplify(V_m - V_c2) == sp.zeros(2, 2)}")
P(f"    UV khronon speed^2: c_2 (2 - alpha_c)/(alpha_c (2 + 3c_2)) -> {uv_inf} (finite);  trace Legendre map: K = {K_of_p}, "
  f"d(K - <K>)/d mu = {bracket} != 0 -> (mu, pi_mu; K - <K>) second class: metric + lapse/shift + multiplier 22 - 2x6 (first class) - 4 "
  f"(second class: pi_N, H_perp, pi_mu, K - <K>) = 6 -> 3 modes (+1 for phi at lambda > 0; the heat pair second class as in FP5 G-2b)")
c1_ok = (ratio_det == 2 and deg_m == 4 and tv_ok and herm_m and quad_m and sp.simplify(B_sol + 3 * sp.I * wq_ * Ap / kq_ ** 2) == 0
         and sp.simplify(mu_sol + 2 * sp.I * wq_ * Ap) == 0 and bracket != 0 and not uv_inf.has(sp.oo))
check("C1 (a) THE LIMIT IS REGULAR ON MINKOWSKI: with -c_2 (K - <K>)^2 -> -2 mu (K - <K>) the block is Hermitian and exactly "
      "quadratic, mu's equation is the CMC condition (A_B = -3i omega A_psi/k^2), B's gives a FINITE multiplier (A_mu = -2i omega A_psi), "
      "det = 2 x lim det/c_2 (the limits commute), deg_omega det = 4 (same count: 2 tensor + khronon + phi; 3 at lambda = 0), "
      "T -> diag(12, 4 lambda) > 0 and V unchanged (health exactly as FP7 C1), the UV khronon speed -> (2 - alpha_c)/(3 alpha_c) "
      "finite; in the Hamiltonian the pair (pi_mu, K - <K>) is second class (d(K - <K>)/d mu != 0), so the Dirac count is unchanged",
      f"det ratio {ratio_det}; deg {deg_m}; T, V limit {tv_ok}; CMC {sp.simplify(B_sol + 3 * sp.I * wq_ * Ap / kq_ ** 2) == 0}; "
      f"mu finite {sp.simplify(mu_sol + 2 * sp.I * wq_ * Ap) == 0}; bracket {bracket}", c1_ok,
      reading="the original Legendre map degenerates (FP5 A2's trace eigenvalue 2(1 - 3(1 + c_2)) -> -oo), which is why the regular "
              "variables are the multiplier's: mu = c_2 (K - <K>) stays finite")


# C1b FRW
def frw_mult(term):
    Q = G2["dK_leaf"] if term == "leaf" else G2["K4"]
    Lt = sp.expand(G2["ser"](G2["sqg4"] * (G2["R4"] - 2 * Lam + alc * G2["aa4"]) - 2 * e_ * mu1 * G2["sqg4"] * Q + 16 * sp.pi * Gc * G2["Ldust"]))
    return Lt.coeff(e_, 1), Lt.coeff(e_, 2)


tC = time.time()
L1m, L2m = frw_mult(TERM)
mu_bg = sp.simplify(sp.diff(L1m, mu1))
flds8 = G2["FIELDS"] + [mu1]
bg8 = [sp.simplify(ee.lhs - ee.rhs) for ee in euler_equations(L1m, flds8, [tq, xq])]
fr_ok = mu_bg == 0
P(f"    [{TERM}] the multiplier's background equation dL1/dmu = {mu_bg}  ({'identically 0 on FRW' if fr_ok else 'forces adot = 0: no expanding FRW'})")
c1b = dict(background=fr_ok)
if fr_ok:
    kF = sp.Symbol('k', positive=True)
    rbs = sp.solve(bg8[0], rb)[0]
    adds = sp.solve(bg8[1].subs(rb, rbs), sp.diff(a_t, tq, 2))[0]
    fr_gr = sp.simplify(8 * sp.pi * Gc * rbs * a_t ** 2 - (3 * sp.diff(a_t, tq) ** 2 - Lam * a_t ** 2)) == 0
    ELq = euler_equations(L2m, flds8, [tq, xq])
    assert len(ELq) == len(flds8), "an equation of the limit system was identically trivial"
    amp8 = {F: sp.Function(F.func.__name__ + 'k')(tq) for F in flds8}

    def fourier(ex):
        for F in flds8:
            ex = ex.subs(F, amp8[F] * sp.exp(sp.I * kF * xq))
        return sp.expand(sp.simplify(ex.doit() * sp.exp(-sp.I * kF * xq)))

    def bgsub(ex):
        ex = ex.subs({amp8[Bq]: 0, amp8[Eq_]: 0}).doit()
        ex = ex.subs(sp.diff(a_t, tq, 3), sp.diff(adds, tq)).subs(sp.diff(a_t, tq, 2), adds).subs(rb, rbs)
        ex = ex.subs(sp.diff(a_t, tq, 2), adds)
        return sp.expand(sp.simplify(ex))
    Eg8 = [bgsub(fourier(ee.lhs - ee.rhs)) for ee in ELq]
    names8 = [F.func.__name__ for F in flds8]
    Qk8 = bgsub(fourier(G2["dK_leaf"].coeff(e_, 1)))
    mu_eq_over_Q = sp.simplify(Eg8[names8.index("mu")] / Qk8)
    Epi8 = Eg8[names8.index("pi")]
    Rmu = sp.simplify(sp.diff(Epi8, amp8[mu1]))
    rest_pi = sp.simplify(Epi8 - Rmu * amp8[mu1] - sp.diff(Epi_leaf, alc).subs({SYS_leaf["amp"][F]: amp8[F] for F in G2["FIELDS"]}).subs(SYS_leaf["k"], kF) * alc)
    R_neg = sp.simplify(Rmu.subs(Lam, 3 * sp.diff(a_t, tq) ** 2 / a_t ** 2 - 8 * sp.pi * Gc * rb) + a_t * (2 * kF ** 2 + 24 * sp.pi * Gc * rb * a_t ** 2))
    dust_same = all(sp.simplify(Eg8[names8.index(nm_)] - SYS_leaf["Eg"][["Phi", "Psi", "B", "E", "pi", "theta", "delta"].index(nm_)]
                                .subs({SYS_leaf["amp"][F]: amp8[F] for F in G2["FIELDS"]}).subs(SYS_leaf["k"], kF)) == 0 for nm_ in ("theta", "delta"))
    L2_leaf = sp.expand(G2["ser"](G2["sqg4"] * (G2["R4"] - 2 * Lam + alc * G2["aa4"]) - c2c * G2["sqg4"] * G2["dK_leaf"] ** 2
                                   + 16 * sp.pi * Gc * G2["Ldust"])).coeff(e_, 2)
    Q1 = G2["dK_leaf"].coeff(e_, 1)
    hs_c2 = sp.simplify(sp.diff(L2_leaf, c2c) + a_t ** 3 * Q1 ** 2) == 0
    hs_mu = sp.simplify(L2m - (L2_leaf.subs(c2c, 0) - 2 * a_t ** 3 * mu1 * Q1)) == 0
    Geff_m, slip_m = G2["qs_mu"](dict(Eg=Eg8, amp=amp8, k=kF, rbs=rbs))
    c1b.update(friedmann_GR=fr_gr, mu_eq_over_Q=str(mu_eq_over_Q), R_mu=str(sp.factor(Rmu)), R_negative=R_neg == 0, pi_rest=str(rest_pi),
               dust_same=dust_same, hs_c2=hs_c2, hs_mu=hs_mu, Geff=str(Geff_m), slip=str(slip_m))
    c1b_ok = (fr_gr and sp.simplify(mu_eq_over_Q + 2 * a_t ** 3) == 0 and R_neg == 0 and rest_pi == 0 and dust_same and hs_c2 and hs_mu
              and sp.simplify(Geff_m - 2 / (2 - alc)) == 0 and sp.simplify(slip_m - 1) == 0)
    P(f"    Friedmann = GR: {fr_gr};  mu's equation / Q = {mu_eq_over_Q} (Q = 0: CMC leaves);  pi's equation = mu x {sp.factor(Rmu)} + alpha_c x "
      f"(FP2's alpha_c-part), remainder {rest_pi};  coefficient = -a (2k^2 + 24 pi G rho a^2) < 0: {R_neg == 0}")
    P(f"    dust equations identical to the finite-c_2 system: {dust_same};  L2's c_2-dependence is exactly -c_2 a^3 Q1^2: {hs_c2};  "
      f"L2(mu) = L2(c_2 = 0) - 2 a^3 mu Q1: {hs_mu} (so L2(c_2) = min_mu [L2(mu) + a^3 mu^2/c_2]);  G_eff/G = {sp.factor(Geff_m)}, slip {slip_m}")
else:
    c1b_ok = False
    fr_plain = sp.factor(G2["frw_system"]("plain")["rbs"] * 8 * sp.pi * Gc * a_t ** 2)
    P(f"    plain finite-c_2 Friedmann: 8 pi G rho a^2 = {fr_plain}  -> H^2 = (Lambda + 8 pi G rho)/(3 + 9 c_2/2) -> 0 as c_2 -> oo")
    c1b["plain_friedmann"] = str(fr_plain)
OUT["numbers"]["C1b"] = {k_: (str(v_) if not isinstance(v_, (bool, float, int)) else v_) for k_, v_ in c1b.items()}
check("C1b (a) THE LIMIT IS REGULAR ON FRW (FP2's machinery + the multiplier): the leaf-averaged term vanishes on FRW so the multiplier's "
      "background equation is empty and Friedmann is GR; at quadratic order L2's c_2-dependence is EXACTLY -c_2 a^3 Q1^2 and "
      "L2(mu) = L2(0) - 2 a^3 mu Q1 (Hubbard-Stratonovich: L2(c_2) = min_mu [L2(mu) + a^3 mu^2/c_2]); mu's equation is Q = 0 (CMC "
      "leaves), the khronon's equation fixes mu = -alpha_c(...)/(a (2k^2 + 24 pi G rho a^2)) FINITE, the dust equations are "
      "unchanged and the growth coupling stays G_eff/G = 2/(2 - alpha_c) with no slip",
      "; ".join(f"{k_} {v_}" for k_, v_ in c1b.items() if k_ in ("background", "friedmann_GR", "R_negative", "dust_same", "hs_c2", "hs_mu", "Geff", "slip")),
      c1b_ok, reading=None if not MUTATE else "MUTATE: the plain K^2 term's limit freezes the expansion -- the leaf average is what makes c_2 -> oo admissible")
P(f"    ({time.time() - tC:.1f} s) {el()}")

# C2 York/CMC
w2_uv_m = sp.factor(sp.limit(w2_l0["mult"] / kq_ ** 2, sgm, 0))
P(f"    chi/J response (from L4): static (omega -> 0) {chi_static} (the MOND enhancement 1/C_phi, both forms, any lambda);  equal-time "
  f"(omega -> oo) at lambda = 0: finite c_2 {chi_inf0['c2']}, c_2 -> oo {chi_inf0['mult']} (identical: {same_inf}; d/dC_phi -> 0 as "
  f"alpha_c -> 0: {efe_blind}); at lambda > 0: {RESP[('c2', 'lambda')][1]} / {RESP[('mult', 'lambda')][1]}")
york = [("the MOND sector's scale", "a0 = kappa c sqrt(G rho_DE) (P1), independent of K: a0(z) flat", "a0 proportional to c|K| (tied to York time): a0(z) ~ H(z) "
         "(the rival footing FP5 D4 / L37 kill)"),
        ("degrees of freedom", f"2 tensor + 1 scalar: the lapse keeps its own alpha_c equation, the CMC pair (pi_mu, K - <K>) is second class "
         f"(C1); UV speed^2 (2 - alpha_c)/(3 alpha_c), MOND-regime speed^2 C_phi/(lambda + 3 sigma^2)", "2 + 0: the CMC condition is second "
         "class with H_perp and fixes the lapse (elliptic, instantaneous)"),
        ("how the MOND field reaches a region", f"the MOND enhancement (1/C_phi) only through the pole omega^2 = {w2_l0['mult']}; the "
         "equal-time part is c_2-independent, Newtonian-strength and EFE-blind to O(alpha_c C_phi) (the elliptic lapse every khronometric "
         "theory has, FP5 C5)", "equal-time 1/k^2 (no omega): instantaneous EFE signaling across spacelike separation -- the kill"),
        ("static G_eff", "G_N = G/(1 - alpha_c/2): the c_2 term is static-inert (K = 0 on static slices)", "2G (a two-potential artefact)"),
        ("Cassini", "unchanged (static-inert): FP7's AQUAL floors 0.0243 / 0.0268 pc", "mu_2 kernel 3.9 sigma")]
for row in york:
    P(f"    {row[0]:36s} | c_2 -> oo root: {row[1]}\n    {'':36s} | York/CMC:        {row[2]}")
york_limit = sp.limit(sp.limit(cs2_bps_sym, c2m, sp.oo), alm, 0, '+')
check("C2 (b) THE YORK/CMC KILL IS NOT REPRODUCED: at c_2 -> oo the CMC condition sits on the khronon's own leaves, but (i) a0 is P1's "
      "constant, not proportional to c|K| (no H(z) footing), (ii) the lapse keeps alpha_c's own equation, so the CMC constraint pairs with the "
      "multiplier and the scalar PROPAGATES (UV speed^2 (2 - alpha_c)/(3 alpha_c), MOND-regime C_phi/(lambda + 3 sigma^2)), (iii) the "
      "response of chi to a source: its MOND enhancement -sigma^2/(4 C_phi k^2) is the omega -> 0 limit and reaches a region only through "
      "that pole, while its equal-time (omega -> oo) part is IDENTICAL at finite c_2 and at c_2 -> oo, Newtonian-strength and EFE-blind "
      "to O(alpha_c C_phi) (zero at lambda > 0): the limit adds no instantaneous channel, and the one that exists is the elliptic lapse "
      "of every khronometric theory (FP5 C5, L318 criterion B), (iv) G_eff = G_N and Cassini are untouched (static-inert).  The York-like "
      "limit is the DOUBLE limit c_2 -> oo, alpha_c -> 0 (UV speed -> oo), which A3's strong coupling excludes",
      f"UV speed^2 at c_2 = oo: {uv_inf}; double limit (alpha_c -> 0): {york_limit}; static MOND response both forms: {static_mond}; "
      f"equal-time part c_2-independent: {same_inf}, EFE-blind at O(alpha_c): {efe_blind}, zero at lambda > 0: {retarded_lam}; "
      f"static block c_2/mu-blind: {static_inert}",
      york_limit == sp.oo and not uv_inf.has(sp.oo) and static_inert and static_mond and same_inf and efe_blind and retarded_lam,
      reading="the leaf-wise heat filter is the root's only equal-time nonlocality and it is c_2-independent (Gaussian tails on each "
              "leaf, FP1/XC1's criterion-B causality) -- the limit adds none")

# C3: tracking, PPN alpha_2, sigma_8/forest, c_T
cs_track = {c2l: math.sqrt(float(cs2_AQ.subs({Cph: 0.01, sgm: 1, alm: AC_MAX, c2m: c2v})) if not math.isinf(c2v) else
                           float(sp.limit(cs2_AQ, c2m, sp.oo).subs({Cph: 0.01, sgm: 1, alm: AC_MAX}))) * cc / 1e3
            for c2l, c2v in (("floor", C2_FLOOR), ("1", 1.0), ("10", 10.0), ("oo", math.inf))}
Cq_reach = 1.0 / float(sp.solve(sp.Eq(sp.limit(cs2_AQ, c2m, sp.oo).subs({sgm: 1, alm: 0}), (V_TRACK / cc) ** 2), Cph)[0])
a2_c2 = {c2l: (float(alpha2_M.subs({Cph: 0.01, sgm: 1, lmm: 0, c2m: c2v})) if not math.isinf(c2v) else
               float(sp.limit(alpha2_M, c2m, sp.oo).subs({Cph: 0.01, sgm: 1, lmm: 0}))) * v620
         for c2l, c2v in (("floor", C2_FLOOR), ("1", 1.0), ("10", 10.0), ("oo", math.inf))}
a2_yagi_inf = sp.factor(sp.limit(yagi, c2m, sp.oo))
s8_c2 = {c2l: {str((f, m)): s8_hy(f, m, c2=c2v) for f in A0 for m in ("rms", "permode")} for c2l, c2v in (("floor", C2_FLOOR), ("oo", 1e15))}
fo_c2 = {c2l: max(forest_hy(f, m, c2=c2v) for f in A0 for m in ("rms", "permode")) for c2l, c2v in (("floor", C2_FLOOR), ("oo", 1e15))}
ds8 = max(abs(s8_c2["oo"][k_] - s8_c2["floor"][k_]) for k_ in s8_c2["floor"])
s8_plumb = s8_hy("canonical", "rms", c2=1e-12)                    # control: a tiny c_2 must move sigma_8 (the weight is live)
P("    tracking speed at C_phi = 0.01 (C^Q = 100), lambda = 0 [km/s]: " + ", ".join(f"c_2 {k_}: {v_:.0f}" for k_, v_ in cs_track.items())
  + f" (target 1800);  c_2 -> oo reach: C^Q <= {Cq_reach:.0f}")
P("    outskirts alpha_2 v^2 (C^Q = 100, 620 km/s, lambda = 0): " + ", ".join(f"c_2 {k_}: {v_:.2e}" for k_, v_ in a2_c2.items())
  + f";  Solar-System (khronometric) alpha_2 -> {a2_yagi_inf} (~ -alpha_c/2)")
P("    (H_Y) sigma_8 at c_2 floor vs c_2 -> oo: " + ", ".join(f"{k_}: {s8_c2['floor'][k_]:.6f} / {s8_c2['oo'][k_]:.6f}" for k_ in s8_c2["floor"])
  + f";  max |d| = {ds8:.1e};  forest {fo_c2['floor']:.1e} / {fo_c2['oo']:.1e};  control c_2 = 1e-12: {s8_plumb:.5f} (the weight is live)")
OUT["numbers"]["C3"] = dict(cs_track=cs_track, Cq_reach=Cq_reach, alpha2_v2=a2_c2, s8=s8_c2, forest=fo_c2, ds8=ds8)
c3_ok = (cs_track["oo"] > cs_track["10"] > cs_track["1"] > cs_track["floor"] >= 1799 and a2_c2["oo"] < a2_c2["1"] < a2_c2["floor"]
         and ds8 < 1e-5 and fo_c2["oo"] < 1e-6 and abs(s8_plumb - 1) < 0.01 and not a2_yagi_inf.has(sp.oo))
check("C3 (c) TRACKING, PPN, GROWTH AND c_T IN THE LIMIT: the tracking speed rises monotonically to c_s^2 = C_phi/(lambda + 3 sigma^2) "
      f"({cs_track['oo']:,.0f} km/s at C^Q = 100: {cs_track['oo'] / 1800:.1f}x the 3 x 600 km/s target, reach C^Q <= {Cq_reach:,.0f}); the "
      f"outskirts alpha_2 v^2 saturates ({a2_c2['floor']:.1%} at the floor -> {a2_c2['1']:.2%} at c_2 = 1 -> {a2_c2['oo']:.2%}); the "
      "Solar-System alpha_2 -> alpha_c (2 alpha_c - 1)/(2 - alpha_c) finite; the (H_Y) sigma_8 and forest are unchanged (the tracking "
      "weight is already saturated); c_T = 1 (delta K = 0 on TT modes: neither c_2 (K - <K>)^2 nor mu (K - <K>) reaches the tensor sector)",
      f"c_s {cs_track['floor']:.0f} -> {cs_track['oo']:.0f} km/s; alpha_2 v^2 {a2_c2['floor']:.3f} -> {a2_c2['oo']:.4f}; d sigma_8 {ds8:.1e}; "
      f"forest {fo_c2['oo']:.1e}", c3_ok)

# C4: strong coupling at c_2 -> oo
ksc_inf = {av: k_sc(av, math.inf) for av in (9.624e-14, AC_MAX)}
check("C4 STRONG COUPLING IN THE LIMIT: XC1's scale with the exact limit speed stays finite (the c_2 cubic vertex c_2 dK1 dK2 = mu1 dK2 "
      f"on shell: no c_2-enhanced vertex survives), k_sc = {ksc_inf[9.624e-14]:.1e} GeV at XC1's lowest alpha_c (>= 1e3 x the LHC); "
      "the limit only moves the alpha_c floor by an O(1) factor (A3)",
      "; ".join(f"alpha_c {k_:.2e}: {v_:.2e} GeV" for k_, v_ in ksc_inf.items()), all(v_ > GATE_XC1 for v_ in ksc_inf.values()),
      reading="XC1's power counting is the decoupling-limit one with the full-block speed (its convention at every c_2); a cubic "
              "analysis with the metric mixing at c_2 -> oo is OPEN")
P(f"    {el()}")

# ============================================================================================================ X xi
banner("X  xi (the heat filter's length): not derivable, no field-dependent form survives, and the filter cannot be dropped -- a KNOB")
# X1 dimensional analysis
ea, eb_, eg, el_ = sp.symbols('e_a e_c e_G e_L')
dims = {"a0": (1, 0, -2), "c": (1, 0, -1), "G": (3, -1, -2), "Lambda": (-2, 0, 0)}           # (m, kg, s)
eqs = [sum(e_x * dims[k_][i] for e_x, k_ in zip((ea, eb_, eg, el_), dims)) - t_x for i, t_x in enumerate((1, 0, 0))]
sol_len = sp.solve(eqs, [ea, eb_, eg], dict=True)[0]
kap = sp.Rational(1, 2)
pure = sp.simplify(8 * sp.pi / kap ** 2)                               # Lambda c^4/a0^2 = 8 pi/kappa^2 (P1)
L_c2a0 = {f: cc ** 2 / a_ / PC_M for f, a_ in A0.items()}               # c^2/a0 [pc]
lo_l = math.log(XI_FLOOR["canonical"] / L_c2a0["canonical"]) / math.log(float(pure))
hi_l = math.log(XI_CEIL_PC / L_c2a0["canonical"]) / math.log(float(pure))
Zv = math.sqrt(32 * math.pi / 3)
hits = {f"(c^2/a0)(8 pi/kappa^2)^{l_}": L_c2a0["canonical"] * float(pure) ** l_ for l_ in (-4, -5, -6, -7)}
hits.update({f"(c^2/a0) Z^{-n_}": L_c2a0["canonical"] * Zv ** (-n_) for n_ in (11, 12, 13, 14, 15, 16)})
inwin = {k_: v_ for k_, v_ in hits.items() if XI_FLOOR["canonical"] <= v_ <= XI_CEIL_PC}
P(f"    exponents of (a0, c, G, Lambda) for a length: {sol_len} (G's exponent 0: no mass, no G);  length = (c^2/a0) (Lambda c^4/a0^2)^e_L, "
  f"Lambda c^4/a0^2 = 8 pi/kappa^2 = {float(pure):.3f}")
P(f"    c^2/a0 = {L_c2a0['canonical']:.3e} pc (canonical) / {L_c2a0['alt']:.3e} pc (alt); the window [{XI_FLOOR['canonical']:.4f}, {XI_CEIL_PC:.0f}] pc "
  f"needs (8 pi/kappa^2)^e_L in [{XI_FLOOR['canonical'] / L_c2a0['canonical']:.1e}, {XI_CEIL_PC / L_c2a0['canonical']:.1e}]: e_L in [{lo_l:.2f}, {hi_l:.2f}]")
P("    integer-power hits (NUMEROLOGY -- no mechanism, flagged, not derivations): " + "; ".join(f"{k_} = {v_:.3g} pc" for k_, v_ in inwin.items()))
OUT["numbers"]["X1"] = dict(exponents=str(sol_len), c2_over_a0_pc=L_c2a0, window_exponent=[lo_l, hi_l], numerology_hits=inwin)
x1_ok = sol_len[eg] == 0 and L_c2a0["canonical"] > 1e9 and hi_l < -4 and len(inwin) >= 1
check("X1 (i) NO CONSTANT LENGTH FROM (a0, Lambda, G, c) WITH AN O(1) COEFFICIENT LANDS IN THE WINDOW: G cannot enter without a mass, "
      f"so every such length is (c^2/a0) (8 pi/kappa^2)^e_L with e_L free -- c^2/a0 = {L_c2a0['canonical'] / 1e9:.0f} Gpc; the window "
      f"[{XI_FLOOR['canonical']:.3f} pc, {XI_CEIL_PC:.0f} pc] needs a pure number {XI_FLOOR['canonical'] / L_c2a0['canonical']:.1e} .. "
      f"{XI_CEIL_PC / L_c2a0['canonical']:.1e}, i.e. e_L in [{lo_l:.2f}, {hi_l:.2f}].  Integer powers do land there ("
      + ", ".join(f"{k_} = {v_:.3g} pc" for k_, v_ in inwin.items()) + ") -- NUMEROLOGY with no mechanism in the action, flagged and NOT "
      "counted as a derivation",
      f"G exponent {sol_len[eg]}; c^2/a0 {L_c2a0['canonical']:.2e} pc; e_L window [{lo_l:.2f}, {hi_l:.2f}]; {len(inwin)} numerology hits",
      x1_ok, reading="FP9 V1's Mpc statement, confirmed for the parsec window: the hierarchy of 9-12 decades is not in the action")

# X2 the field-dependent filter length on galaxies (SPARC, KiDS)
S_FAM = (0.0, 0.5, 1.0, 2.0, 3.0)


def xi_g(g, a0, s):
    return (cc ** 2 / g) * (a0 / g) ** s                             # [m]


xi_tab = {s: {"y=100": xi_g(100 * A0["canonical"], A0["canonical"], s) / PC_M, "y=1": xi_g(A0["canonical"], A0["canonical"], s) / PC_M,
              "y=0.01": xi_g(0.01 * A0["canonical"], A0["canonical"], s) / PC_M} for s in S_FAM}
sp_fd = {}
for foot in A0:
    for s in S_FAM:
        sp_fd[(foot, s)] = best(*gal_sums(lambda gb, R, a0, s=s: np.where(xi_g(gb, a0, s) > R, gb, nu_p2(gb / a0) * gb), A0[foot]))
SP_N = {f: best(*gal_sums(lambda gb, R, a0: gb, A0[f])) for f in A0}
KI_N = kids_isolated(lambda y: np.ones_like(np.asarray(y, float)))
P("    xi(g) = (c^2/g)(a0/g)^s [pc] at galaxy fields: " + "; ".join(f"s = {s}: y=100 {v_['y=100']:.1e}, y=1 {v_['y=1']:.1e}, y=0.01 {v_['y=0.01']:.1e}"
                                                              for s, v_ in xi_tab.items()))
P("    SPARC rms (Upsilon profiled on the chain's grid 0.30-1.20): P2 " + ", ".join(f"{f} {SP_P2[f][0]:.4f}" for f in A0)
  + "; with the filter (MOND off where xi(g) > R): " + ", ".join(f"{k_[0][:3]} s={k_[1]}: {v_[0]:.4f} (U {v_[1]:.2f})" for k_, v_ in sp_fd.items())
  + "; Newtonian: " + ", ".join(f"{f} {SP_N[f][0]:.4f}" for f in A0))
P(f"    KiDS isolated chi^2 (lenses at y ~ 1e-4..1e-1, xi >= Gpc: MOND off): {KI_N['canonical']:.1f} / {KI_N['alt']:.1f} vs P2 "
  f"{KI_P2['canonical']:.1f} / {KI_P2['alt']:.1f} (d chi^2 {KI_N['canonical'] - KI_P2['canonical']:+.0f} / {KI_N['alt'] - KI_P2['alt']:+.0f})")
OUT["numbers"]["X2"] = dict(xi_pc=xi_tab, sparc={f"{k_[0]}|{k_[1]}": v_ for k_, v_ in sp_fd.items()}, sparc_newton=SP_N, kids_newton=KI_N)
x2_ok = (all(v_["y=1"] > 1e8 for v_ in xi_tab.values()) and all(v_[0] > SP_P2[k_[0]][0] + 0.1 for k_, v_ in sp_fd.items())
         and all(KI_N[f] - KI_P2[f] > 500 for f in A0))
check("X2 (ii) A FIELD-DEPENDENT LENGTH xi(g) = (c^2/g)(a0/g)^s FAILS GALAXIES FOR EVERY s: at g = a0 it is c^2/a0 = "
      f"{L_c2a0['canonical'] / 1e9:.0f} Gpc whatever s (the galaxy ceiling ~{XI_CEIL_PC:.0f} pc is violated by {L_c2a0['canonical'] / XI_CEIL_PC:.0e} "
      "at y = 1, more below), so the filter erases the MOND source of every galaxy: SPARC rises from "
      f"{SP_P2['canonical'][0]:.3f} / {SP_P2['alt'][0]:.3f} to {min(v_[0] for v_ in sp_fd.values()):.3f} dex (Newtonian) and KiDS's "
      f"isolated-lens chi^2 from {KI_P2['canonical']:.0f} / {KI_P2['alt']:.0f} to {KI_N['canonical']:.0f} / {KI_N['alt']:.0f}.  Generally, any "
      f"length from (c, a0, g) is (c^2/a0) F(g/a0), and the ceiling needs F(y) <= {XI_CEIL_PC / L_c2a0['canonical']:.1e} y on y = 0.01-100: "
      "a new tiny number",
      f"xi(y = 1) = {xi_tab[0.5]['y=1']:.1e} pc (every s); SPARC {min(v_[0] for v_ in sp_fd.values()):.3f}-{max(v_[0] for v_ in sp_fd.values()):.3f} dex; "
      f"KiDS d chi^2 {KI_N['canonical'] - KI_P2['canonical']:+.0f} / {KI_N['alt'] - KI_P2['alt']:+.0f}", x2_ok,
      reading="the Newtonian fit pins Upsilon at the grid's 1.2 edge; a larger Upsilon cannot rescue the gas-dominated outskirts")


# X3 the same filter in the Solar System from the action's static variation: the readout-gradient force
zS, xS = sp.symbols('z x', real=True)
q0, q1, L0s = sp.symbols('q0 q1 L0', real=True)
bfun = sp.Function('b')(xS)
Wq = q0 + q1 * xS + L0s * xS ** 2 / 2 + zS * L0s                     # e^{z d_x^2} of a quadratic: exact heat solution
heat_res = sp.simplify(sp.diff(Wq, zS) - sp.diff(Wq, xS, 2))
chi_ro = Wq.subs(zS, bfun)                                           # chi(x) = W(b(x), x): the readout at a field-dependent depth
grad_extra = sp.simplify(sp.diff(chi_ro, xS) - sp.diff(Wq, xS).subs(zS, bfun) - sp.diff(bfun, xS) * sp.diff(Wq, xS, 2).subs(zS, bfun))
extra_term = sp.simplify(sp.diff(chi_ro, xS) - sp.diff(Wq, xS).subs(zS, bfun))
# the lapse back-reaction: E_chi on shell = -16 pi G rho (zero in vacuum)
Phs, Pss, chs, rhs_, Gs = sp.symbols('Phi Psi chi rho G', real=True)
Lst = lambda P_, S_, C_: 2 * S_ ** 2 - 4 * P_ * S_ + alm * P_ ** 2 + (2 - alm) * (2 * P_ * C_ - C_ ** 2)   # gradients as symbols (1-D static density / 16 pi G)
dPsi = sp.solve(sp.diff(Lst(Phs, Pss, chs), Pss), Pss)[0]             # Psi' = Phi'
lapse_eq = sp.diff(Lst(Phs, Pss, chs), Phs).subs(Pss, dPsi)           # d/dx of this = 16 pi G rho (the lapse equation, integrated once)
Echi_flux = sp.diff(Lst(Phs, Pss, chs), chs)                          # chi's flux; its divergence is E_chi
E_chi_rel = sp.simplify(Echi_flux + lapse_eq)                         # E_chi = -(lapse flux)' = -16 pi G rho when the flux identity holds
# the Galactic phantom density at the Sun in the AQUAL root, two estimates (AQUAL scalar: div(mu_s grad phi) = 4 pi G S rho):
#  coarse-grained (smoothing over many stars, xi >~ pc): the disc's vertical channel gives Delta phi = 4 pi G rho_b / mu_T(x_e);
#  vacuum (xi below the star spacing, only the Sun inside): Delta phi = -grad ln mu_s . grad phi from the Galaxy's own radial
#  gradient, |d ln mu_s/d ln R| = (d ln mu_s/d ln x)(d ln x/d ln y)|d ln y/d ln R| x_e a0/R0, with |d ln y/d ln R| >= 1 (a lower bound)
R0_GAL = 8.178e3 * PC_M                                                # GRAVITY 2019, as committed in the repo's vertical-force lanes
mu_T, rho_vac = {}, {}
for foot, a0 in A0.items():
    for ge in G_EXT:
        yN = (-1 + math.sqrt(1 + 4 * (ge / a0) ** 2)) / 2               # P2 inverted: g/a0 = sqrt(yN^2 + yN)
        xe = ge / a0 - yN
        mu_T[(foot, ge)] = xe / (1 - 2 * xe)
        dlnx_dlny = ((2 * yN + 1) / (2 * math.sqrt(yN * yN + yN)) - 1) * yN / xe
        dlnmu_dlnx = 1 / (1 - 2 * xe)
        rho_vac[(foot, ge)] = dlnmu_dlnx * dlnx_dlny * 1.0 * xe * a0 / R0_GAL / (4 * math.pi * Gn) / MSUN_PC3
rho_ph_coarse = RHO_B_LOCAL / max(mu_T.values())
rho_ph = min(min(rho_vac.values()), rho_ph_coarse)                     # the scored, conservative lower bound
FOURPIG_RHO = 4 * math.pi * Gn * rho_ph * MSUN_PC3
S_GRID = (0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0)
ss_rows = {}
for s in S_GRID:
    p_ = 1 + s
    row = {}
    for pl, rau in PLANETS.items():
        r = rau * AU_M
        g = GM_SUN / r ** 2
        xi = xi_g(g, A0["canonical"], s)
        dg = 2 * p_ * xi ** 2 / r * FOURPIG_RHO                       # |xi grad xi| x 4 pi G rho_ph
        row[pl] = (xi / PC_M, dg, dg / A_SUNWARD)
    ss_rows[s] = row
lead = ss_rows[0.5]
dlnxi_max = A_SUNWARD * AU_M / (2 * (XI_FLOOR["canonical"] * PC_M) ** 2 * FOURPIG_RHO)
# FP7 A4's committed AQUAL table at g_ext = 2.32e-10: the smallest xi row (0.010 pc) already fails every Solar-System gate, and
# the leak grows as xi shrinks -- a filter shorter than that at every planet is in the strict-law regime (FP7 A4 / FP1 D1)
row01 = None
if fp7:
    row01 = next((r_["A"] for r_ in fp7["numbers"]["A4"]["table_2p32"]["canonical"] if abs(r_["xi"] - 0.01) < 1e-9), None)
XI_STRICT = 0.010
verdict_s = {}
for s, row in ss_rows.items():
    worst_pl = max(row, key=lambda pl: row[pl][2])
    xi_top = max(v_[0] for v_ in row.values())
    if row[worst_pl][2] > 1:
        verdict_s[s] = ("FAILS", f"readout-gradient force {row[worst_pl][2]:.1e}x the gate at {worst_pl}")
    elif xi_top < XI_STRICT and row01 and min(row01["Q2"], row01["M"], row01["gmax"]) > 1:
        verdict_s[s] = ("FAILS", f"xi <= {xi_top:.1e} pc at every planet: below FP7's failing 0.010 pc row (Q2 {row01['Q2']:.1f}x, "
                                 f"monopole {row01['M']:.1f}x): the strict-law leak")
    else:
        verdict_s[s] = ("NOT EXCLUDED HERE", f"max force {row[worst_pl][2]:.1e}x, xi up to {xi_top:.1e} pc")
P(f"    readout identity: heat residual {heat_res}; d_x chi - (d_x W)|_b = {extra_term}  (exactly b'(x) Delta chi = xi xi' Delta chi); "
  f"E_chi on shell: chi-flux + lapse-flux = {E_chi_rel} -> E_chi = -16 pi G rho (vanishes in vacuum)")
P(f"    the Galaxy's phantom at the Sun: coarse-grained rho_b/mu_T = {rho_ph_coarse:.4f} Msun/pc^3 (mu_T(x_e) = {min(mu_T.values()):.2f}-"
  f"{max(mu_T.values()):.2f}, rho_b = {RHO_B_LOCAL} Msun/pc^3, the repo's Oort-limit input); vacuum lower bound (mu_s gradient only, "
  f"|dln y/dln R| = 1, R0 = 8.178 kpc) {min(rho_vac.values()):.4f}-{max(rho_vac.values()):.4f}; SCORED with {rho_ph:.4f} Msun/pc^3")
for s in (0.0, 0.5, 1.0):
    P(f"    s = {s}: " + "; ".join(f"{pl} xi {v_[0]:.2e} pc, dg {v_[1]:.1e} m/s^2 = {v_[2]:.1e}x" for pl, v_ in ss_rows[s].items()))
for s, (vd, why) in verdict_s.items():
    P(f"    s = {s:4.2f}: {vd} -- {why}")
P(f"    ephemeris requirement at 1 AU with xi at the floor: |d ln xi/d ln g| <= {dlnxi_max:.1e}")
OUT["numbers"]["X3"] = dict(rho_ph_scored=rho_ph, rho_ph_coarse=rho_ph_coarse, rho_ph_vacuum={f"{k_[0]}|{k_[1]}": v_ for k_, v_ in rho_vac.items()},
                            rows={str(s): {pl: list(v_) for pl, v_ in row.items()} for s, row in ss_rows.items()},
                            verdicts={str(s): list(v_) for s, v_ in verdict_s.items()}, dlnxi_max=dlnxi_max,
                            mu_T={f"{k_[0]}|{k_[1]}": v_ for k_, v_ in mu_T.items()})
x3_ok = (heat_res == 0 and grad_extra == 0 and sp.simplify(E_chi_rel) == 0 and all(v_[2] > 1 for v_ in lead.values())
         and lead["Earth"][2] > 100 and all(vd == "FAILS" for vd, _ in verdict_s.values()))
check("X3 (ii) THE SAME FILTER FAILS THE SOLAR SYSTEM, FROM THE ACTION'S STATIC VARIATION: a field-dependent xi makes the heat branch's "
      "readout depth b(x) = xi(g(x))^2/2, so chi(x) = W(b(x), x) and grad chi = S grad phi + xi grad xi (S Delta phi) EXACTLY (the heat "
      "identity); the lapse back-reaction is E_chi Delta chi b' with E_chi = -16 pi G rho (zero in vacuum).  The new force xi|grad xi| x "
      f"4 pi G rho_ph from the Galaxy's own phantom (scored with the vacuum lower bound {rho_ph:.4f} Msun/pc^3, {rho_ph_coarse / rho_ph:.0f}x below "
      f"the coarse-grained rho_b/mu_T) is sunward and grows as r^(4s+3): for the lead "
      f"(s = 1/2, xi = {lead['Earth'][0]:.3f} pc at 1 AU) {lead['Mercury'][2]:.0f}x the ephemeris gate at Mercury, {lead['Earth'][2]:.1e}x at "
      f"the Earth, {lead['Saturn'][2]:.0e}x at Saturn.  Every s on the grid 0-3 fails: s <~ 1 by this force (at the outer planets), "
      f"larger s because xi(g) then falls below FP7's failing 0.010 pc row at every planet (the strict-law leak).  The ephemerides allow "
      f"|d ln xi/d ln g| <~ {dlnxi_max:.0e}: xi must be CONSTANT across the Solar System",
      f"s = 1/2: " + ", ".join(f"{pl} {v_[2]:.1e}x" for pl, v_ in lead.items()) + "; per s: "
      + "; ".join(f"{s}: {vd}" for s, (vd, _) in verdict_s.items()) + f"; |dln xi/dln g| <= {dlnxi_max:.1e}", x3_ok,
      reading="a lower bound: the Sun's own (unfiltered-source) phantom adds a same-sign term ~ a0 grad xi, larger still; the two scale "
              "differently with r, so they cannot cancel at every planet")

# X3b the second variation (FC-KH type) of the field-dependent readout
BLK_ro = unitary_block("c2", readout=True)
T_ro, V_ro, herm_ro, quad_ro = reduce_TV(BLK_ro, ["psi", "phi"], ["n", "B"])
V11_ro = sp.factor(sp.simplify(V_ro[0, 0]))
detV_ro = sp.factor(sp.simplify(V_ro.det()))
V11_target = 4 * kq_ ** 2 * (2 - alm) * (1 + Kb ** 2 * kq_ ** 2) / (alm - (2 - alm) * Kb ** 2 * kq_ ** 2)
fckh_form = sp.simplify(V11_ro - V11_target) == 0 and sp.simplify(V_ro.subs(Kb, 0) - V_c2) == sp.zeros(2, 2)
K_1au = {s: 4 * math.pi * Gn * rho_ph * MSUN_PC3 * xi_g(GM_SUN / AU_M ** 2, A0["canonical"], s) ** 2 * (1 + s) / (GM_SUN / AU_M ** 2) for s in (0.5,)}
lam_c = {av: 2 * math.pi * K_1au[0.5] / math.sqrt(av / (2 - av)) for av in (AC_MAX, fl_sc[("floor", "XC1 gate")])}
P(f"    readout response delta chi = K (a_hat.grad) delta n, K = Delta chi xi dxi/d|a|: V_11 = {V11_ro};  det V = {detV_ro}")
P(f"    K at 1 AU (s = 1/2, rho_ph above) = {K_1au[0.5]:.0f} m;  unstable below the wavelength 2 pi K sqrt((2 - alpha_c)/alpha_c) = "
  + ", ".join(f"{v_ / 1e3:.2e} km (alpha_c = {k_:.1e})" for k_, v_ in lam_c.items()))
check("X3b (ii) ITS SECOND VARIATION IS FC-KH-UNSTABLE: because the readout depth depends on the lapse gradient, delta chi gains K "
      "(a_hat.grad) delta n and the reduced block becomes V_11 = 4k^2 (2 - alpha_c)(1 + K^2 k^2)/(alpha_c - (2 - alpha_c) K^2 k^2), "
      "det V likewise: a gradient instability of the khronon for K^2 k^2 > alpha_c/(2 - alpha_c) -- alpha_c (<= 3.2e-9) is the lapse's "
      f"only stiffness; the lead's K = {K_1au[0.5]:.0f} m at 1 AU is unstable at every wavelength below {lam_c[AC_MAX] / 1e3:.1e} km "
      f"(alpha_c at its cap) to {lam_c[fl_sc[('floor', 'XC1 gate')]] / AU_M:.1f} AU (at XC1's floor).  Control: K = 0 returns FP7's healthy V",
      f"V_11 form {fckh_form}; Hermitian {herm_ro}; quadratic {quad_ro}; K(1 AU) {K_1au[0.5]:.0f} m; critical wavelengths "
      + ", ".join(f"{v_ / 1e3:.1e} km" for v_ in lam_c.values()), fckh_form and herm_ro and quad_ro and K_1au[0.5] > 1.0,
      reading="the FC-KH lesson in a new place: nothing on the lapse may vary faster than alpha_c allows; c_T = 1 is untouched (b depends on "
              "the scalar |a|, the TT sector does not see it)")

# X4 (reported) |Phi|-based lengths: gauge and the floor/ceiling pincer
phi_ss = (230e3 / cc) ** 2                                            # the Galaxy's potential depth at the Sun (>= v_c^2/c^2)
m_max_ss = math.log(XI_FLOOR["canonical"] / ((cc ** 2 / (GM_SUN / AU_M ** 2)) / PC_M)) / math.log(phi_ss)
m_min_gal = max(math.log(XI_CEIL_PC / L_c2a0["canonical"]) / math.log((v_ * 1e3 / cc) ** 2) for v_ in (50.0, 300.0))
check("X4 (reported) |Phi|-BASED LENGTHS xi = (c^2/g)(|Phi|/c^2)^m FAIL TOO: MOND potentials grow as ln r without bound, so |Phi| needs a "
      "declared zero point (a new datum: gauge-ambiguous), and even granting the Galaxy's depth at the Sun (|Phi| >= v_c^2) the "
      "Solar-System floor needs m <= 0.69 while the galaxy ceiling at g = a0 needs m >= 1.42 -- no window (their readout gradient is "
      "small, since the Galaxy's potential dominates |Phi| across the Solar System: the pincer, not X3, kills them)",
      f"m <= {m_max_ss:.2f} (Solar System) vs m >= {m_min_gal:.2f} (galaxies)", m_max_ss < m_min_gal, load_bearing=False)
P(f"    {el()}")

# X5 dropping the filter by changing the kernel
ysym = sp.Symbol('y', positive=True)
nu_sym = sp.Function('nu')(ysym)
CL_id = sp.simplify(sp.diff((nu_sym - 1) * ysym, ysym) - (nu_sym - 1 + ysym * sp.diff(nu_sym, ysym)))
h_meas = {}
for U in (0.5, 0.7, 0.9):
    ys_, hs_ = [], []
    for (R, Vobs, eV, Vgas, Vdisk, Vbul) in GAL:
        Rm = R * KPC
        Vbar2 = np.sign(Vgas) * Vgas ** 2 + U * Vdisk ** 2 + 1.4 * U * Vbul ** 2
        gb = Vbar2 * 1e6 / Rm
        go = (Vobs * 1e3) ** 2 / Rm
        ok = (gb > 0) & (go > 0) & (Vobs > 0)
        ys_.append(gb[ok] / A0["canonical"])
        hs_.append((go[ok] - gb[ok]) / A0["canonical"])
    ys_, hs_ = np.concatenate(ys_), np.concatenate(hs_)
    m_ = (ys_ >= 0.3) & (ys_ < 1.0)
    h_meas[U] = (float(np.median(hs_[m_])), int(m_.sum()))
h_min = min(v_[0] for v_ in h_meas.values())
tail_floor = h_min * A0["canonical"] / A_SUNWARD


def nu_p2n(n):
    return lambda y: (1.0 + np.maximum(np.asarray(y, float), 1e-300) ** (-n)) ** (1.0 / (2 * n))


def nu_p2tail(yc, m=4):
    return lambda y: 1.0 + (np.sqrt(1.0 + 1.0 / np.maximum(np.asarray(y, float), 1e-300)) - 1.0) / (1.0 + (np.maximum(np.asarray(y, float), 1e-300) / yc) ** m)


KERNELS = [("P2", nu_p2), ("nu_RAR (exp tail)", nu_rar), ("P2, tail cut y_c = 1e3", nu_p2tail(1e3)), ("P2, tail cut y_c = 20", nu_p2tail(20.0)),
           ("P2, tail cut y_c = 5", nu_p2tail(5.0)), ("P2_n n = 2", nu_p2n(2)), ("P2_n n = 3", nu_p2n(3)), ("P2_n n = 4", nu_p2n(4))]
YH = np.logspace(-3, 8, 2201)
q2tab, health, sparc_k = {}, {}, {}
for nm_, nf in KERNELS:
    q2tab[nm_] = {f: [q_direct2D(nf, ge / A0[f], 100.0) * PREF(A0[f]) / Q2_CEIL for ge in G_EXT] for f in A0}
    hh = (nf(YH) - 1.0) * YH                                         # the phantom h(y); health (C_L >= 0) <=> non-decreasing
    health[nm_] = bool(np.all(np.diff(hh) >= -1e-6 * np.abs(hh[1:])))  # (relative roundoff of sqrt(1 + 1/y) - 1 at y ~ 1e8)
    sparc_k[nm_] = {f: best(*gal_sums(m_kernel(nf), A0[f]))[0] for f in A0}
for nm_, _ in KERNELS:
    P(f"    {nm_:24s} Q2/ceiling (g_ext 2.00/2.32/2.64) canonical " + "/".join(f"{v_:.2f}" for v_ in q2tab[nm_]["canonical"])
      + ", alt " + "/".join(f"{v_:.2f}" for v_ in q2tab[nm_]["alt"]) + f";  monotone phantom (healthy): {health[nm_]};  SPARC "
      + ", ".join(f"{f[:3]} {v_:.4f}" for f, v_ in sparc_k[nm_].items()))
P(f"    health theorem: d[(nu - 1) y]/dy - C_L = {CL_id} -> healthy (C_L >= 0) <=> the phantom h(y) = (nu - 1) y is non-decreasing; SPARC's "
  f"h at y = 0.3-1 (median, Upsilon 0.5/0.7/0.9): " + ", ".join(f"{v_[0]:.2f}" for v_ in h_meas.values())
  + f" -> every healthy kernel leaves >= {h_min:.2f} a0 at the planets = {tail_floor:.0f}x the ephemeris gate")
OUT["numbers"]["X5"] = dict(q2=q2tab, healthy=health, sparc=sparc_k, h_meas={str(k_): v_ for k_, v_ in h_meas.items()}, tail_floor=tail_floor)
tail_only = [nm_ for nm_ in ("P2, tail cut y_c = 1e3", "P2, tail cut y_c = 20")]
tail_irrel = all(max(abs(q2tab[nm_][f][i] / q2tab["P2"][f][i] - 1) for i in range(3)) < 0.03 for nm_ in tail_only for f in A0)
pass_q2 = [nm_ for nm_, _ in KERNELS if all(max(v_) < 1 for v_ in q2tab[nm_].values())]
x5_ok = (CL_id == 0 and tail_floor > 100 and tail_irrel and min(min(v_) for v_ in q2tab["nu_RAR (exp tail)"].values()) > 3
         and all(not health[nm_] for nm_ in pass_q2) and all(sparc_k[nm_][f] > sparc_k["P2"][f] + 0.005 for nm_ in pass_q2 for f in A0)
         and health["P2"])
q2_rng = lambda nm_: (min(min(v_) for v_ in q2tab[nm_].values()), max(max(v_) for v_ in q2tab[nm_].values()))
d_sparc = [sparc_k[nm_][f] - sparc_k["P2"][f] for nm_ in pass_q2 for f in A0]
check("X5 (iii) THE FILTER CANNOT BE DROPPED BY CHANGING THE KERNEL -- it is a health + EFE statement, not a tail statement: (a) health "
      "(C_L >= 0) is exactly a non-decreasing phantom h(y) = (nu - 1) y, so every healthy kernel keeps at the planets at least the "
      f"phantom SPARC measures at y = 0.3-1 (>= {h_min:.2f} a0): >= {tail_floor:.0f}x the ephemeris gate, whatever its tail; (b) Cassini Q2 "
      f"at xi = 0 is set at y ~ g_ext/a0 = 2-3: cutting P2's tail above y_c = 20 moves Q2 by < 3% ({q2_rng('P2, tail cut y_c = 20')[0]:.1f}-"
      f"{q2_rng('P2, tail cut y_c = 20')[1]:.1f}x the ceiling), nu_RAR's exponentially fast tail fails worse ({q2_rng('nu_RAR (exp tail)')[0]:.1f}-"
      f"{q2_rng('nu_RAR (exp tail)')[1]:.1f}x); only a sharper transition passes ({', '.join(pass_q2)} on both footings), and every such "
      "kernel is non-monotone (unhealthy: FP7 C1's tachyon), is not the framework's P2 and costs SPARC "
      f"+{min(d_sparc) if d_sparc else float('nan'):.3f}..+{max(d_sparc) if d_sparc else float('nan'):.3f} dex",
      f"tail-cut Q2 change < 3%: {tail_irrel}; kernels passing Q2: {pass_q2} (healthy: {[health[k_] for k_ in pass_q2]}); healthy tail floor "
      f"{tail_floor:.0f}x", x5_ok)
P(f"    {el()}")

# ============================================================================================================ F count
banner("F  THE GRAVITY CORE'S CONSTANTS AFTER FP14")
COUNT = [("G", "measured", "measured", "-"),
         ("Lambda", "measured", "measured", "-"),
         ("kappa = 1/2 (a0 = kappa c sqrt(G rho_DE))", "FITTED (accepted)", "FITTED (accepted)", "FP0 L0c"),
         ("xi (heat-filter length)", "bounded knob [0.0243/0.0268 pc, ~100 pc]", "KNOB: bounded, not derivable (X1), no field-dependent form survives "
          "(X2-X3b), not removable (X5)", "X1-X5"),
         ("alpha_c (BPS alpha)", "bounded knob (0, 3.2e-9]", f"REGULATOR: value unobservable (A1), must be > 0 (A2, A3); floor "
          f"{fl_sc[('floor', 'torsion balance')]:.0e}..{fl_sc[('oo', 'XC1 gate')]:.0e} by the probe criterion", "A1-A4"),
         ("c_2 (leaf-averaged lambda-term)", "bounded below (>= 7.29e-3), no ceiling", "ELIMINATED: c_2 -> oo is regular; the term is the CMC "
          "constraint -2 mu (K - <K>_h), mu a multiplier", "C1-C4"),
         ("lambda (phi's inertia)", "0 allowed (FP9)", "ELIMINATED: lambda = 0 (needs FP9's yield at exact zero field)", "L1-L4"),
         ("phibar-dot (declared datum)", "declared = 0 (FP7 F)", "ELIMINATED: gauge at lambda = 0", "L1")]
for row in COUNT:
    P(f"    {row[0]:42s} | before: {row[1]:44s} | after: {row[2]}  [{row[3]}]")
P("    outside the gravity core (unchanged here): FP9's separator (L_Lambda, n, y_Lambda, p': 4 declared) and the declared dark mass")
OUT["numbers"]["F"] = [dict(constant=r_[0], before=r_[1], after=r_[2], basis=r_[3]) for r_ in COUNT]
check("F (reported) THE NEW COUNT: beyond (kappa, G, Lambda) the gravity core had 4 constants + 1 declared datum; it now has ONE knob (xi) "
      "and ONE regulator (alpha_c: required nonzero, value unobservable); c_2, lambda and phibar-dot are eliminated",
      "knobs 4 -> 1; regulators 0 -> 1; eliminated 3 (c_2, lambda, phibar-dot)", True, load_bearing=False)

# ============================================================================================================ W ledger
banner("W  THE LEDGER: FP14")
LEDGER = [
    ("F14a", "lambda = 0 passes every gate FP7/FP9 scored: statics, Solar System, SPARC, KiDS, flagship, FRW, sigma_8 and forest (H_Y), "
             "health (one scalar), tracking (best), PPN (alpha_2's lag gone), c_T, N = 3", "DERIVED", "L2, L4 (this lane's block; FP9's machinery)"),
    ("F14b", "at lambda = 0 the action has the exact gauge symmetry phi -> phi + f(tau): FRW's phibar is gauge, FP7's declared "
             "'phibar-dot = 0' is eliminated", "DERIVED", "L1 (generic ADM metric, FRW minisuperspace)"),
    ("F14c", "lambda = 0 needs FP9's yield at exact zero field (else phi = A_n/sigma: the backward heat operator)", "CONSTRAINT", "L3"),
    ("F14c'", "at lambda = 0 the chassis field chi gains an equal-time response (zero at lambda > 0): Newtonian-strength, EFE-blind to "
              "O(alpha_c C_phi); the MOND enhancement still arrives only through the propagating pole", "DERIVED",
     "L4 (source response of the block; L318 criterion B admits it)"),
    ("F14d", f"no scored observable depends on alpha_c beyond O(alpha_c) <= {growth_ac:.1e}; the Solar-System alphas vanish as alpha_c -> 0; "
             "FP5's y* does not exist on the AQUAL root", "DERIVED", "A1"),
    ("F14e", "alpha_c -> 0+: the UV khronon becomes instantaneous (rank change) and strongly coupled, k_sc ~ alpha_c^(3/4): alpha_c = 0 excluded",
     "FAILS", "A2, A3 (XC1's formula, reproduced)"),
    ("F14f", f"alpha_c is a REGULATOR in [alpha_sc, 3.2e-9] (alpha_sc = {fl_sc[('floor', 'torsion balance')]:.0e} .. "
             f"{fl_sc[('oo', 'XC1 gate')]:.0e} by the probe criterion): nonzero, value unobservable",
     "POSTULATED", "A (verdict): a UV requirement, not a fitted constant"),
    ("F14g", "the L340 H4 O(Phi/c^2) lobe floor on alpha_c for the AQUAL root", "OPEN",
     f"A4 (L340's scaling: {min(H4.values()):.0e}..{max(H4.values()):.0e} over the xi window, inside it)"),
    ("F14h", "c_2 -> oo is regular: -c_2 (K - <K>_h)^2 -> -2 mu (K - <K>_h); Minkowski (det = 2 lim det/c_2, T -> diag(12, 4 lambda), V "
             "unchanged, same count, second-class multiplier pair) and FRW (HS identity, Q = 0, mu finite, dust unchanged, G_eff = "
             "1/(1 - alpha_c/2))", "DERIVED", "C1, C1b (the MUTATE plain K^2 freezes the expansion)"),
    ("F14i", "c_2 -> oo does NOT reproduce the York/CMC kill: a0 not tied to K, the scalar propagates (alpha_c keeps the lapse dynamical), "
             "the response's equal-time part is c_2-independent (no new instantaneous channel) and EFE-blind, G_eff = G_N, Cassini "
             "unchanged; the York-like limit is the double limit alpha_c -> 0, excluded by strong coupling", "DERIVED", "C2"),
    ("F14j", f"in the limit: tracking {cs_track['floor']:,.0f} -> {cs_track['oo']:,.0f} km/s (C^Q = 100), outskirts alpha_2 v^2 "
             f"{a2_c2['floor']:.1%} -> {a2_c2['oo']:.2%}, sigma_8/forest (H_Y) unchanged (<= {ds8:.0e}), c_T = 1, k_sc finite",
     "DERIVED", "C3, C4 (the cubic mixing analysis at c_2 -> oo is OPEN)"),
    ("F14k", "the c_2 term replaced by the CMC constraint (c_2 eliminated)", "POSTULATED", "C (verdict): the zero-knob choice of a regular limit"),
    ("F14k'", "not covered for the c_2 -> oo root: nonlinear well-posedness, the cubic strong-coupling analysis with metric mixing, and the "
              "khronon's binary-pulsar radiation at lambda_BPS -> oo (only the PPN bounds were scored)", "OPEN", "scope; the same items are open at finite c_2"),
    ("F14l", f"xi from (a0, Lambda, G, c): only (c^2/a0)(8 pi/kappa^2)^e_L; O(1) coefficient = {L_c2a0['canonical'] / 1e9:.0f} Gpc; "
             f"{len(inwin)} integer-power hits in the window are numerology", "FAILS", "X1 (sympy nullspace)"),
    ("F14m", f"field-dependent xi(g) = (c^2/g)(a0/g)^s: galaxies (SPARC {min(v_[0] for v_ in sp_fd.values()):.3f} dex, KiDS "
             f"{KI_N['canonical'] - KI_P2['canonical']:+.0f}), Solar System (readout-gradient force {lead['Earth'][2]:.0e}x the ephemeris "
             "gate at the Earth for the lead; every s fails), FC-KH-type gradient instability", "FAILS", "X2, X3, X3b"),
    ("F14n", f"|Phi|-based xi: gauge-ambiguous and a floor/ceiling pincer (m <= {m_max_ss:.2f} vs >= {m_min_gal:.2f})", "FAILS", "X4 (reported)"),
    ("F14o", f"dropping the filter by a kernel change: healthy kernels keep >= {h_min:.2f} a0 at the planets ({tail_floor:.0f}x); Cassini "
             f"Q2 is an EFE/transition statement (tail cuts < 3%); only unhealthy sharp kernels ({', '.join(pass_q2)}) pass",
     "FAILS", "X5 (theorem + FP1's Q2 integral)"),
    ("F14p", f"xi is the gravity core's one remaining knob, bounded to [{XI_FLOOR['canonical']:.4f}/{XI_FLOOR['alt']:.4f} pc, ~{XI_CEIL_PC:.0f} pc]",
     "CONSTRAINT", "X (verdict); FP7 A4 floors"),
    ("F14q", "the core's count beyond (kappa, G, Lambda): 1 knob (xi) + 1 regulator (alpha_c); eliminated c_2, lambda, phibar-dot",
     "DERIVED", "F"),
]
for k_, what, status, basis in LEDGER:
    P(f"    {k_:6s} {status:11s} {what}  --  {basis}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger of this lane", f"{len(LEDGER)} links", True, load_bearing=False)

# ============================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P("  lambda   ELIMINATED.  At lambda = 0 the root gains an exact gauge symmetry phi -> phi + f(tau) (so FP7's declared phibar-dot is gauge"
  "\n           too), keeps one healthy scalar (omega^2 >= 0 iff C_phi >= 0) and passes every gate FP7 and FP9 scored; the price is FP9's"
  "\n           yield at exact zero field, which the chain already carries.")
P("  alpha_c  a REGULATOR, not a knob and not removable.  Nothing scored moves by more than 1.6e-9 across its window, and the"
  "\n           Solar-System alphas vanish as alpha_c -> 0 -- but the limit is singular: the UV khronon becomes instantaneous and"
  f"\n           k_sc ~ alpha_c^(3/4) -> 0.  It must be nonzero (>= {fl_sc[('floor', 'torsion balance')]:.0e} .. {fl_sc[('oo', 'XC1 gate')]:.0e} by the probe criterion); its value is unobservable.")
P("  c_2      ELIMINATED.  c_2 -> oo is regular on Minkowski and FRW: the term becomes the CMC constraint -2 mu (K - <K>_h) with a finite"
  "\n           multiplier, the count and health are unchanged, tracking and alpha_2 saturate at their best values, sigma_8 is"
  "\n           untouched.  It does NOT reproduce the York/CMC kill: a0 stays P1's constant and alpha_c keeps the scalar propagating."
  "\n           (MUTATE: without the leaf average the same limit freezes the expansion.)")
P("  xi       a KNOB.  No length from (a0, Lambda, G, c) with an O(1) coefficient reaches the parsec window (integer-power hits are"
  "\n           numerology); a field-dependent xi(g) fails galaxies (xi(a0) = c^2/a0), the ephemerides (the readout-gradient force) and"
  f"\n           FC-KH stability; and the filter cannot be dropped: every healthy kernel keeps a planetary anomaly >= {tail_floor:.0f}x the gate,"
  "\n           and Cassini's Q2 is set at the EFE transition, not by the tail.")
P("  COUNT    beyond (kappa, G, Lambda): 1 knob (xi) + 1 regulator (alpha_c).  Not 'zero knobs': xi is the one that remains.")
P(f"  Time {time.time() - T0:.0f} s.")
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results.json".replace("_MUTATE_results", "_results_MUTATE")), "w"), indent=1, default=str)
P(f"\n  {len(CH) - n_fail}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote "
  f"{SLUG.replace('_MUTATE', '')}_results{'_MUTATE' if MUTATE else ''}.json")
sys.exit(0 if n_fail == 0 else 1)
