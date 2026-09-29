#!/usr/bin/env python3
"""r3_reimplementation.py -- lane R1: INDEPENDENT re-implementation of the September-2025 'Relator' closure of alpha, from the equations printed in the paper
(Zenodo 17109113, `Alpha.pdf`; equation numbers cited below). Nothing of the author's code is imported at run time: own quadratures, own Biot-Savart integral for the loop
field (no elliptic-integral formulas), own root solve. Double precision except where noted (accuracy checked in the output to ~1e-14 relative).
The ONE piece of the author's code that appears here is a two-line recurrence for int x^m cos/sin(a x) dx, retyped and labelled 'author recurrence' (Amendment 1): it is
reproduced in order to show that it does not equal the printed integral, and to build the 'author-lineage' L_2m values.

What is computed
  1  spectrum K, L_2m, eqs (30)-(32) and Appendix-M (M2)-(M4), (M16); K also from the closed form printed in the April-2026 program header ((150 pi^2 - 8 pi^4 - 315)/(180 pi^6));
     L_2m by the printed definition (M4) (Gauss-Legendre and, as a second method, mpmath quad) AND by the author's recurrence (retyped, labelled)
  2  Coulomb block D_C(alpha), eqs (27), (28), (33)
  3  vector chain: Lambda_ind (37), C_UV (38), P_IR (47), Delta Lambda_out from (a) the literal projection (41)-(43) [basis (1-x^2)P_l'], (b) the printed closed form (44) and series (45),
     (c) the physical exterior energy (orthogonal projection with the basis sqrt(1-x^2)P_l', checked against a direct volume integral of |B|^2 outside the shell), (d) the l=1 term
  4  synchronisation (49)-(59) with the map ladder and the self ladder; lock (84)/(86) and the alpha-solve (88)
  5  the printed choice set is compared with the author's program values (cfg-1 137.0359991769773; cfg-2..4 137.0359991770872; cfg-5 ...873; Table VI, transcribed constants)
  6  every declared choice point (R1_PREREGISTRATION.md) is swapped alone; then the full factorial family (author-lineage inputs) is enumerated; stage-wise landing is computed

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 r3_reimplementation.py            -> exit 0 iff the AMENDED flag vector (Amendment 1 of R1_PREREGISTRATION.md) is reproduced:
                 {H2_printed_definitions: False, H2_author_table: True, H3: True, H4: True, H5a: True, H5b: True, H7: True} (Amendment 2)
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 r3_reimplementation.py --mutate   -> C_UV is replaced by gamma/2 inside the 'H2_author_table' reproduction only; that check must then fail: exit 1
"""
import sys, os, json, itertools, time, math
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
import numpy as np
import mpmath as mp
from scipy import integrate
from scipy.special import eval_legendre as Pl
MUTATE = "--mutate" in sys.argv
mp.mp.dps = 30
PI = math.pi
def P(*a):
    print(" ".join(str(x) for x in a), flush=True)

T_INV = 137.035999177            # CODATA 2022 (NIST)
SIG_REL = 2.1e-8 / T_INV         # CODATA 2022 relative uncertainty
BAR = 5e-10
AUTHOR_CFG1 = 137.0359991769773  # Table VI cfg 1
AUTHOR_CFG2 = 137.0359991770872  # Table VI cfg 2-4
AUTHOR_CFG5 = 137.0359991770873  # Table VI cfg 5 (printed headline)

# ------------------------------------------------------------------ 1. spectrum
def K_sum():
    def term(n):
        n = int(n)
        I = (-1) ** (n - 1) / (((n - 1) * mp.pi) ** 2) + (-1) ** n / (((n + 1) * mp.pi) ** 2)      # eq (30)
        return (2 * I) ** 2 / (n ** 2 - 1)
    return float(2 / mp.pi ** 2 * mp.nsum(term, [2, mp.inf]))
K_closed = (150 * PI ** 2 - 8 * PI ** 4 - 315) / (180 * PI ** 6)
_xg, _wg = np.polynomial.legendre.leggauss(700)
_xg = 0.5 * (_xg + 1); _wg = 0.5 * _wg
def L2m_M4(m, nmax=200):
    """(M4): L_2m = (2/pi^2) sum_n (2 I_n^(2m))^2/(n^2-1), I_n^(2m) = 2 int_0^1 x^(2m) sin(pi x) sin(n pi x) dx (Gauss-Legendre, 700 nodes)."""
    s = 0.0
    for n in range(2, nmax + 1):
        I = 2 * np.sum(_wg * _xg ** (2 * m) * np.sin(PI * _xg) * np.sin(n * PI * _xg))
        s += (2 * I) ** 2 / (n ** 2 - 1)
    return 2 / PI ** 2 * s
def L2m_M4_partial_mpquad(m, nmax=12):
    """second, independent method: mpmath adaptive quadrature of the same integrals, partial sum over n = 2..nmax."""
    s = mp.mpf(0)
    for n in range(2, nmax + 1):
        I = 2 * mp.quad(lambda x: x ** (2 * m) * mp.sin(mp.pi * x) * mp.sin(n * mp.pi * x), mp.linspace(0, 1, 2 * n + 1))
        s += (2 * I) ** 2 / (n ** 2 - 1)
    return float(2 / mp.pi ** 2 * s)
def L2m_M4_partial_gl(m, nmax=12):
    s = 0.0
    for n in range(2, nmax + 1):
        I = 2 * np.sum(_wg * _xg ** (2 * m) * np.sin(PI * _xg) * np.sin(n * PI * _xg))
        s += (2 * I) ** 2 / (n ** 2 - 1)
    return 2 / PI ** 2 * s
def _cs_author(m, a):
    """AUTHOR'S RECURRENCE, retyped from the published program (Zenodo 17109113, function _CS_pair): returns (C_m, S_m) meant to be int_0^1 x^m cos(ax) dx and int_0^1 x^m sin(ax) dx.
    The sine update carries (1 - cos a)/a at every step; the correct update is -cos(a)/a + (k/a) C_(k-1) (checked below against mpmath quad)."""
    C = mp.sin(a) / a; S = (1 - mp.cos(a)) / a
    if m == 0: return C, S
    for k in range(1, m + 1):
        C, S = mp.sin(a) / a - (k / a) * S, (1 - mp.cos(a)) / a + (k / a) * C
    return C, S
def _cs_correct(m, a):
    C = mp.sin(a) / a; S = (1 - mp.cos(a)) / a
    if m == 0: return C, S
    for k in range(1, m + 1):
        C, S = mp.sin(a) / a - (k / a) * S, -mp.cos(a) / a + (k / a) * C
    return C, S
def L2m_author(m, tol=mp.mpf("1e-40"), nmax=1200):
    """the author's series as programmed: (2/pi^2) sum (2 I_nm)^2/(n^2-1), I_nm = (C1 - C2)/2 from the retyped recurrence, stop when n > 80 and |term| < tol."""
    mp.mp.dps = 50
    S = mp.mpf(0)
    for n in range(2, nmax + 1):
        C1, _ = _cs_author(2 * m, (n - 1) * mp.pi); C2, _ = _cs_author(2 * m, (n + 1) * mp.pi)
        I = (C1 - C2) / 2
        t = (2 * I) ** 2 / (n ** 2 - 1)
        S += t
        if n > 80 and abs(t) < tol: break
    v = float(2 / mp.pi ** 2 * S)
    mp.mp.dps = 30
    return v
KMAX = 12

# ------------------------------------------------------------------ 2. Coulomb block
CUNI = {"u0": (1 / PI) * (4 / 3 + 1 / (4 * PI ** 2)),   # eq (27) with |u0|^2 = j0^2 weight
        "vol": (1 / PI) * (6 / 5)}                      # alternative B3: uniform-volume weight
def cuni_check():
    w = np.sin(PI * _xg) ** 2
    ex2 = np.sum(_wg * _xg ** 2 * w) / np.sum(_wg * w)
    return (3 - ex2) / (2 * PI)
def make_dc(K, Ls, cuni, content):
    def dc(alpha):
        xi = 2 * cuni * alpha
        if content == "uniform":
            return alpha / PI * math.sqrt(1 - xi)
        s = math.sqrt(1 - xi) - (xi / 2) * K
        if content == "full":
            for m, Lm in enumerate(Ls, start=2):
                s -= (xi / 2) ** m * Lm
        return alpha / PI * s
    return dc
def solve_dc(dc, target, a0):
    a = a0
    for _ in range(60):
        f = dc(a) - target
        h = a * 1e-7
        d = (dc(a + h) - dc(a - h)) / (2 * h)
        na = a - f / d
        if abs(na - a) < 1e-18: a = na; break
        a = na
    return a

# ------------------------------------------------------------------ 3. vector chain
ETA = 1 / PI
EPS = 1 / math.sqrt(PI)
ELL = EPS * ETA
GAMMA_E = float(mp.euler)
LIND = {"m2": math.log(8 * math.sqrt(PI)) - 2, "m74": math.log(8 * math.sqrt(PI)) - 1.75}
CUV = {"full": 0.5 * (math.log(2) + GAMMA_E), "gamma_half": 0.5 * GAMMA_E}
def p_ir(ell=ELL, c=1 / 3, expo=2, fform="a"):     # eq (47)
    def f(x):
        return (1 - x) ** 2 / ((1 - x) ** 2 + ell ** 2) if fform == "a" else (1 - x) / ((1 - x) + ell)
    def g(x):
        return x ** 2 * math.sin(PI * x) ** 2 * (1 - c * f(x)) * math.exp(-(((1 - x) / ell)) ** expo)
    num, err = integrate.quad(g, 0, 1, epsabs=1e-17, epsrel=1e-14, limit=400, points=[1 - 3 * ell, 1 - ell, 1 - 0.3 * ell])
    den = 1 / 6 - 1 / (4 * PI ** 2)
    return num / den
def bfield(rho, z, nphi=128):     # Biot-Savart of a unit loop (radius 1, mu0*I = 1): direct phi integral (trapezoid on a periodic analytic integrand)
    ph = 2 * PI * np.arange(nphi) / nphi
    c = np.cos(ph)
    d2 = rho ** 2 + 1 - 2 * rho * c + z ** 2
    inv = d2 ** -1.5
    return np.mean(c * z * inv) / 2.0, np.mean((1 - rho * c) * inv) / 2.0     # (B_rho, B_z)
_th, _wth = np.polynomial.legendre.leggauss(220)
_th = 0.5 * PI * (_th + 1); _wth = 0.5 * PI * _wth       # Gauss-Legendre in theta on [0, pi]: exponentially convergent (int f(x) dx = int f sin(theta) dtheta)
def _bth_theta(eta):
    rs = 1 / eta
    x = np.cos(_th); s = np.sin(_th)
    Bth = np.empty(len(_th))
    for i in range(len(_th)):
        br, bz = bfield(rs * s[i], rs * x[i])
        Bth[i] = br * x[i] - bz * s[i]            # B.e_theta with e_theta = cos(theta) e_rho - sin(theta) e_z  (paper, below (41))
    return rs, x, s, Bth
def dlam_out_terms(eta=ETA, lmax=121, basis="literal"):
    """eqs (41)-(43): a_l = r*^(l+2)/I_l int B_theta T_l dx ; Delta Lambda_out = -4 pi sum_l (l+1)/(2l+1) a_l^2 r*^(-(2l+1)).
    basis='literal': T_l = (1-x^2) P_l'  (as printed);  basis='ortho': T_l = sqrt(1-x^2) P_l'  (the basis orthogonal with the norm I_l)."""
    rs, x, s, Bth = _bth_theta(eta)
    terms = []
    for l in range(1, lmax + 1, 2):
        Pp = l * (Pl(l - 1, x) - x * Pl(l, x)) / np.where(s > 0, s ** 2, 1.0)        # P_l'(x) = l (P_{l-1} - x P_l)/(1 - x^2)
        T = (s ** 2 * Pp) if basis == "literal" else (s * Pp)
        Il = 2 * l * (l + 1) / (2 * l + 1)
        al = rs ** (l + 2) * np.sum(_wth * s * Bth * T) / Il                         # dx = sin(theta) dtheta
        terms.append(-4 * PI * (l + 1) / (2 * l + 1) * al ** 2 * rs ** (-(2 * l + 1)))
    return terms
def dlam_out_closed(eta=ETA):                      # eq (44)
    return -PI * (math.log(1 - eta ** 4) / (2 * eta) + math.atanh(eta) - math.atan(eta))
def dlam_out_series(eta=ETA, lmax=19):             # eq (45)
    return -PI * sum(eta ** (2 * l + 1) / ((l + 1) * (2 * l + 1)) for l in range(1, lmax + 1, 2))
def dlam_out_dipole(eta=ETA):                      # the l = 1 term of (45)
    return -PI / 6 * eta ** 3
def dlam_out_volume(eta=ETA):                      # direct: -int_{r > r*} |B|^2 dV (mu0 I = 1), Gauss-Legendre in (u = r*/r, x)
    rs = 1 / eta
    xo, wo = np.polynomial.legendre.leggauss(100)
    uo, wu = np.polynomial.legendre.leggauss(70); uo = 0.5 * (uo + 1); wu = 0.5 * wu
    tot = 0.0
    for u, wuu in zip(uo, wu):
        r = rs / u
        ang = 0.0
        for x, w in zip(xo, wo):
            sx = math.sqrt(1 - x * x)
            br, bz = bfield(r * sx, r * x, nphi=96)
            ang += w * (br * br + bz * bz)
        tot += wuu * ang * u ** -4
    return -2 * PI * rs ** 3 * tot

# ------------------------------------------------------------------ 4. sync + lock + solve
def alpha_inv(o, comp):
    K = comp["K"]; dc = comp["dc"][(o["dcc"], o["cuni"])]
    out = comp["out"][o["out"]]
    P_ = comp["pir"][o["pir"]]; Cuv = comp["cuv"][o["cuv"]]
    lam_base = comp["lind"][o["lind"]] + Cuv * P_ + out
    eta = ETA
    gg = 0.5 * math.sinh(eta) / eta if o["gam"] == "sinh" else 0.5
    kappa = (math.sinh(eta) / eta - 1) if o["kap"] == "sinh" else eta ** 2 / 6
    cchi = 2 * PI ** 2 if o["cchi"] == "2pi2" else 2 * PI
    clog = 1 / 3 if o["clog"] == "13" else 2 / 3
    def G(lam):
        z = K * lam / (2 * PI ** 2)
        return (cchi / (2 * clog)) * z * ((1 + z) if o["dress"] == "1pz" else 1.0)
    lam = lam_base
    alpha = PI * G(lam)
    for it in range(60):
        alpha_new = solve_dc(dc, G(lam), alpha)
        Dk = dc(alpha_new)
        if o["zeta"] == "nosync":
            lam_new = lam_base
        else:
            X = K / (2 * Dk) * Cuv * P_
            sync = (gg + X) * P_ * out
            if o["chi"]:
                sync += (-kappa * X ** 2 / (1 + kappa * X)) * P_ * out
            if o["self"]:
                epsdy = {"std": alpha_new / PI * K / (2 * PI ** 2) * P_ * lam,
                         "noP": alpha_new / PI * K / (2 * PI ** 2) * lam,
                         "half": alpha_new / (2 * PI) * K / (2 * PI ** 2) * P_ * lam}[o["eps"]]
                sync += -gg * P_ * lam * (epsdy / (1 + kappa * epsdy))
            lam_new = lam_base + sync
        if abs(alpha_new - alpha) < 1e-18 and abs(lam_new - lam) < 1e-16:
            alpha = alpha_new; lam = lam_new; break
        alpha, lam = alpha_new, lam_new
    return 1 / alpha, lam

PRINTED = dict(chi=1, self=1, out="literal", gam="sinh", clog="13", zeta="sync", dcc="full", lind="m2", cuv="full", cuni="u0",
               pir=(1 / 3, 2, "a"), cchi="2pi2", dress="1pz", eps="std", kap="sinh")

def build_components(Ls, outs):
    comp = {}
    comp["K"] = K_NUM
    comp["Ls"] = Ls
    comp["dc"] = {}
    for dcc in ("full", "Konly", "uniform"):
        for cu in CUNI:
            comp["dc"][(dcc, cu)] = make_dc(K_NUM, Ls, CUNI[cu], dcc)
    comp["lind"] = dict(LIND); comp["cuv"] = dict(CUV)
    comp["pir"] = PIR_TABLE
    comp["out"] = outs
    return comp

# ------------------------------------------------------------------ main
t0 = time.time()
P("== 1  spectrum K, L_2m  (eqs (30)-(32); Appendix M (M2)-(M4), (M16)) ==")
K_NUM = K_sum()
P("  K (own sum of (32)/(M3), mpmath nsum)      = %.18g" % K_NUM)
P("  K (closed form of the April-2026 header)   = %.18g   |difference| = %.2e" % (K_closed, abs(K_NUM - K_closed)))
P("  paper Table II: K = 0.00223153891653197018640879 ; |own - paper| = %.2e" % abs(K_NUM - 0.00223153891653197018640879))
TAB = {2: 0.00373155489837063530553899, 3: 0.00143830013553058946046987, 4: 0.00060470414931351794924673}
Ls_M4 = [L2m_M4(m) for m in range(2, KMAX + 1)]
Ls_auth = [L2m_author(m) for m in range(2, KMAX + 1)]
P("  L_2m: printed definition (M4) [GL] | author recurrence (retyped) | paper Table II | (M4)/author")
for m in (2, 3, 4):
    P("    L_%d : %.12e | %.12e | %.12e | %.4f" % (2 * m, Ls_M4[m - 2], Ls_auth[m - 2], TAB[m], Ls_M4[m - 2] / Ls_auth[m - 2]))
P("  author recurrence reproduces Table II to: L4 %.1e, L6 %.1e, L8 %.1e (relative)" % tuple(abs(Ls_auth[m - 2] / TAB[m] - 1) for m in (2, 3, 4)))
P("  (M16) check: L_2 = 4K by the printed definition: L_2(M4) = %.15g ; 4K = %.15g" % (L2m_M4(1), 4 * K_NUM))
for m in (2, 3):
    a1 = L2m_M4_partial_mpquad(m, 12); a2 = L2m_M4_partial_gl(m, 12)
    aa = float(2 / mp.pi ** 2 * sum((2 * ((_cs_author(2 * m, (n - 1) * mp.pi)[0] - _cs_author(2 * m, (n + 1) * mp.pi)[0]) / 2)) ** 2 / (n ** 2 - 1) for n in range(2, 13)))
    P("  second method for L_%d (partial sum n = 2..12): mpmath quad %.15e ; Gauss-Legendre %.15e ; |diff| %.1e ; author-recurrence partial sum (program normalisation, (2 I_nm)^2) %.6e" % (2 * m, a1, a2, abs(a1 - a2), aa))
for m, a in ((2, 3.0), (4, 7.0), (6, 12.0)):
    cq = mp.quad(lambda x: x ** m * mp.sin(a * x), [0, 1])
    P("  recurrence check m=%d a=%g: int x^m sin(ax): quad %.12f | author recurrence %.12f | corrected recurrence %.12f" % (m, a, cq, _cs_author(m, a)[1], _cs_correct(m, a)[1]))
P("  C_uni: printed (1/pi)(4/3 + 1/(4 pi^2)) = %.16g ; from quadrature of <3 - x^2> under the j0^2 weight: %.16g" % (CUNI["u0"], cuni_check()))

P("\n== 2  vector chain ==")
P("  Lambda_ind = ln(8 sqrt(pi)) - 2 = %.16g (paper Table VIII 0.651806484604536)" % LIND["m2"])
P("  C_UV = (ln2 + gamma)/2 = %.16g (paper 0.635181422730739)" % CUV["full"])
PIR_TABLE = {}
for c in (1 / 3, 1 / 2, 2 / 3):
    for ex in (2, 1):
        for ff in ("a", "b"):
            PIR_TABLE[(c, ex, ff)] = p_ir(ELL, c, ex, ff)
pir0 = PIR_TABLE[(1 / 3, 2, "a")]
P("  P_IR(l0) own quadrature = %.16g (paper Table III 0.0857791925845556)  |diff| = %.2e" % (pir0, abs(pir0 - 0.0857791925845556011097469)))
P("  Delta Lambda_UV->IR = C_UV P_IR = %.16g (paper 0.0544853495865521)" % (CUV["full"] * pir0))
terms_lit = dlam_out_terms(lmax=141, basis="literal")
out_lit = sum(terms_lit)
P("  Delta Lambda_out, literal projection (41)-(43) [T_l = (1-x^2)P_l'], l <= 141 (own Biot-Savart, theta-quadrature) = %.17g" % out_lit)
P("      author's converged value (Table VI cfg 2, April-2026 direct sum): -0.0139671580625860254655  |own - author| = %.2e" % abs(out_lit + 0.0139671580625860254655225))
P("      partial sums l <= 19 / <= 41 / <= 101 / <= 141: %.16f  %.16f  %.16f  %.16f" % (sum(terms_lit[:10]), sum(terms_lit[:21]), sum(terms_lit[:51]), out_lit))
P("      author Table VI: l <= 19 (after his Aitken step) -0.01396715806205758 ; l <= 100 -0.01396715806258603")
P("      literal terms l = 1, 3, 5, 7, 9, 11, 21: %s" % ", ".join("%.4e" % terms_lit[i] for i in (0, 1, 2, 3, 4, 5, 10)))
terms_orth = dlam_out_terms(lmax=15, basis="ortho")
out_true = sum(terms_orth)
P("  Delta Lambda_out, physical exterior energy (orthogonal basis sqrt(1-x^2)P_l', l <= 15) = %.16g" % out_true)
vol = dlam_out_volume()
P("  direct volume integral  -int_(r>r*) |B|^2 dV                                    = %.16g   (|volume - orthogonal sum| = %.1e)" % (vol, abs(vol - out_true)))
cl = dlam_out_closed(); sr = dlam_out_series(lmax=19)
P("  printed closed form (44) = %.16g ; printed series (45) l <= 19 = %.16g ; l = 1 term = %.16g" % (cl, sr, dlam_out_dipole()))
P("  orthogonal-basis terms (l = 1,3,5,7): %s" % ", ".join("%.6e" % t for t in terms_orth[:4]))
P("  terms of the printed series (45)    : %s" % ", ".join("%.6e" % (-PI * ETA ** (2 * l + 1) / ((l + 1) * (2 * l + 1))) for l in (1, 3, 5, 7)))
P("  relative differences: literal vs printed closed form (44): %.4f ; literal vs physical: %.4f ; (44) vs physical: %.3e ; series (45) vs (44): %.1e" %
  ((out_lit - cl) / cl, (out_lit - out_true) / out_true, (cl - out_true) / out_true, abs(sr - cl) / abs(cl)))

OUTS = {"literal": out_lit, "closed": cl, "dipole": dlam_out_dipole(), "true": out_true}
comp_tab = build_components(Ls_auth, OUTS)
comp_def = build_components(Ls_M4, OUTS)

P("\n== 3  the printed choice set (converged) vs the author's program values ==")
inv_tab, lam_tab = alpha_inv(PRINTED, comp_tab)
P("  own (Table-II/author-recurrence L_2m, literal exterior projection): alpha^-1 = %.13f ; Lambda_eff = %.15f" % (inv_tab, lam_tab))
P("  author cfg-1 137.0359991769773 : own - author = %+.3e (relative %.2e)" % (inv_tab - AUTHOR_CFG1, abs(inv_tab / AUTHOR_CFG1 - 1)))
P("  author cfg-2..4 137.0359991770872 : own - author = %+.3e (relative %.2e)" % (inv_tab - AUTHOR_CFG2, abs(inv_tab / AUTHOR_CFG2 - 1)))
P("  author cfg-5 (headline) 137.0359991770873 : own - author = %+.3e (relative %.2e)" % (inv_tab - AUTHOR_CFG5, abs(inv_tab / AUTHOR_CFG5 - 1)))
P("  author Lambda_eff cfg-2 0.6916840202841763 : own - author = %+.2e" % (lam_tab - 0.6916840202841763119337))
if MUTATE:
    oo = dict(PRINTED); oo["cuv"] = "gamma_half"
    inv_repro, _ = alpha_inv(oo, comp_tab)
    P("  [MUTATE] the reproduction run uses C_UV = gamma/2: alpha^-1 = %.10f" % inv_repro)
else:
    inv_repro = inv_tab
h2_tab = abs(inv_repro / AUTHOR_CFG2 - 1) <= 5e-12
P("  H2_author_table: the Table-II L values + literal projection reproduce the converged author value to 5e-12 relative: %s" % h2_tab)
miss_tab = abs(inv_tab / T_INV - 1)
P("  miss of that set vs CODATA 2022: %.3e relative (%.4f sigma_CODATA)" % (miss_tab, miss_tab / SIG_REL))
P("  --- what the printed definitions give (L_2m from (M4) instead of the author's recurrence), and other readings of the exterior term ---")
rows_def = []
for lab_l, cmp_ in (("author L", comp_tab), ("printed (M4) L", comp_def)):
    for lab_o, key in (("literal (41)-(43)", "literal"), ("closed (44)", "closed"), ("physical energy", "true")):
        inv, _ = alpha_inv(dict(PRINTED, out=key), cmp_)
        rows_def.append((lab_l, lab_o, inv))
        P("    L_2m = %-15s exterior = %-18s -> alpha^-1 = %.10f ; miss vs CODATA 2022 = %.3e relative (%.1f sigma_CODATA)" % (lab_l, lab_o, inv, abs(inv / T_INV - 1), abs(inv / T_INV - 1) / SIG_REL))
inv_def, _ = alpha_inv(PRINTED, comp_def)
h2_def = abs(inv_def / T_INV - 1) <= 1e-9
P("  H2_printed_definitions: (M4) L_2m + literal projection lands within 1e-9 of CODATA 2022: %s   [registered expectation: False]" % h2_def)
P("  effect of the L_2m recurrence error alone: alpha^-1 (printed L) - alpha^-1 (author L) = %+.3e = %.3e relative" % (inv_def - inv_tab, abs(inv_def / inv_tab - 1)))

P("\n== 4  H3: the printed closed form (44) in place of the literal projection ==")
inv3, lam3 = alpha_inv(dict(PRINTED, out="closed"), comp_tab)
P("  alpha^-1 with (44) = %.10f ; miss vs CODATA 2022 = %.3e relative" % (inv3, abs(inv3 / T_INV - 1)))
h3 = abs((cl - out_lit) / out_lit) > 1e-3 and abs(inv3 / T_INV - 1) > 1e-4
P("  H3 (closed form does not reproduce the value used; alpha misses by > 1e-4): %s" % h3)

P("\n== 5  stage-wise landing of the author-lineage set (relative alpha^-1 shift and miss vs target after each stage) ==")
inv0 = inv_tab
stages = [("no sync (Lambda_base)", dict(PRINTED, zeta="nosync")),
          ("+ geometric gain gamma_geom only", dict(PRINTED, chi=0, self=0, _noX=1)),
          ("+ order-one map gain X", dict(PRINTED, chi=0, self=0)),
          ("+ chi (map) ladder", dict(PRINTED, self=0)),
          ("+ self ladder (= printed set)", dict(PRINTED))]
prev = None; stage_rows = []
for lab, oo in stages:
    if oo.get("_noX"):
        oo = dict(oo); del oo["_noX"]
        c2 = dict(comp_tab); c2["cuv"] = {"full": 0.0}
        c2["lind"] = {"m2": comp_tab["lind"]["m2"] + CUV["full"] * comp_tab["pir"][(1 / 3, 2, "a")]}
        inv, _ = alpha_inv(oo, c2)
    else:
        inv, _ = alpha_inv(oo, comp_tab)
    miss = abs(inv / T_INV - 1)
    shift = abs(inv / prev - 1) if prev else float("nan")
    stage_rows.append((lab, inv, shift, miss))
    P("  %-36s alpha^-1 = %.10f   shift from previous = %.3e   miss vs CODATA 2022 = %.3e" % (lab, inv, shift, miss))
    prev = inv
land = 1.0
for i in range(2, len(stage_rows)):
    sh = stage_rows[i][2]; ms = stage_rows[i][3]
    p_i = min(1.0, ms / sh) if sh > 0 else 1.0
    P("    stage '%s': correction size %.3e, residual %.3e -> chance of landing that close if the correction's sign/magnitude were unconstrained within +-its size: %.2e" % (stage_rows[i][0], sh, ms, p_i))
    land *= p_i
P("    product over stages 3-5 (heuristic, independent-stage reading; not a bar quantity): %.2e" % land)

P("\n== 6  every declared choice point swapped alone (relative shift of alpha^-1 from the author-lineage set, in units of 1e-10; miss vs CODATA 2022) ==")
CH = [
    ("A1", "A", "chi", [1, 0], "chi ladder on / off"),
    ("A2", "A", "self", [1, 0], "self ladder on / off"),
    ("A3", "A", "out", ["literal", "closed", "dipole", "true"], "exterior term: literal (41)-(43) / printed closed form (44) / l=1 only / physical exterior energy"),
    ("A4", "A", "gam", ["sinh", "half"], "gamma_geom = sinh(eta)/(2 eta) / 1/2"),
    ("A5", "A", "clog", ["13", "23"], "C_log target 1/3 / 2/3"),
    ("A6", "A", "zeta", ["sync", "nosync"], "zeta from Lambda with sync / without sync"),
    ("A7", "A", "dcc", ["full", "Konly", "uniform"], "D_C content: full / K only / uniform only"),
    ("B1", "B", "lind", ["m2", "m74"], "Lambda_ind constant -2 / -7/4"),
    ("B2", "B", "cuv", ["full", "gamma_half"], "C_UV (ln2+gamma)/2 / gamma/2"),
    ("B3", "B", "cuni", ["u0", "vol"], "C_uni weighting |u0|^2 / uniform volume"),
    ("C1", "C", "pir_c", [1 / 3, 1 / 2, 2 / 3], "P_IR coefficient of f_swirl 1/3, 1/2, 2/3"),
    ("C2", "C", "pir_e", [2, 1], "P_IR Gaussian exponent 2 / 1"),
    ("C3", "C", "pir_f", ["a", "b"], "f_swirl (1-x)^2/((1-x)^2+l^2) / (1-x)/((1-x)+l)"),
    ("C4", "C", "cchi", ["2pi2", "2pi"], "C_chi 2 pi^2 / 2 pi"),
    ("C5", "C", "dress", ["1pz", "none"], "dressing (1+zeta) present / absent"),
    ("C6", "C", "eps", ["std", "noP", "half"], "eps_Dy: std / without P_IR / alpha/(2 pi)"),
    ("C7", "C", "kap", ["sinh", "eta2"], "kappa = sinh(eta)/eta - 1 / eta^2/6"),
]
def make_opts(sel):
    o = dict(PRINTED)
    pc, pe, pf = 1 / 3, 2, "a"
    for k, v in sel.items():
        if k == "pir_c": pc = v
        elif k == "pir_e": pe = v
        elif k == "pir_f": pf = v
        else: o[k] = v
    o["pir"] = (pc, pe, pf)
    return o
shift_rows = []
n_bar = 0; n_eff = 0
for cid, cls, key, alts, lab in CH:
    row = {"id": cid, "class": cls, "label": lab, "alts": []}
    maxshift = 0.0
    for v in alts[1:]:
        inv, _ = alpha_inv(make_opts({key: v}), comp_tab)
        sh = abs(inv / inv0 - 1)
        row["alts"].append((str(v), inv, sh, abs(inv / T_INV - 1)))
        maxshift = max(maxshift, sh)
        P("  %s %s  alt=%-10s alpha^-1 = %.9f  shift = %10.3e (= %.3g x 1e-10)  miss vs CODATA 2022 = %.3e" % (cid, cls, str(v)[:10], inv, sh, sh / 1e-10, abs(inv / T_INV - 1)))
    row["maxshift"] = maxshift
    shift_rows.append(row)
    if maxshift > BAR: n_bar += 1
    if maxshift > 1.7e-13: n_eff += 1
frac_bar = n_bar / len(CH)
P("  choice points: %d ; with a swap that moves alpha^-1 by more than the bar's 5e-10: %d (%.0f%%) ; 'effective' (some swap > 1.7e-13): %d" % (len(CH), n_bar, 100 * frac_bar, n_eff))
h4 = frac_bar >= 0.8
P("  H4 (>= 80%% of choice points shift alpha^-1 by more than 5e-10): %s" % h4)

P("\n== 7  H7: spread under the alternatives the source itself names (its own optional switches: chi ladder, self ladder, curvature on/off, literal vs closed-form exterior) ==")
vals = []
for chi, sf, gam, out in itertools.product((1, 0), (1, 0), ("sinh", "half"), ("literal", "closed")):
    inv, _ = alpha_inv(make_opts(dict(chi=chi, self=sf, gam=gam, out=out)), comp_tab)
    vals.append(((chi, sf, gam, out), inv))
rel = [abs(v / inv0 - 1) for _, v in vals]
P("  16 named-switch combinations: max relative shift from the author-lineage set = %.3e ; number within 5e-10 of that value = %d ; within 5e-10 of CODATA 2022 = %d" % (max(rel), sum(1 for r in rel if r <= BAR), sum(1 for _, v in vals if abs(v / T_INV - 1) <= BAR)))
spread10 = (max(v for _, v in vals) - min(v for _, v in vals)) / inv0 / 1e-10
P("  spread (max-min)/alpha^-1 = %.4g x 1e-10 (bar = 5 x 1e-10)" % spread10)
h7 = spread10 * 1e-10 > BAR
P("  H7 (spread over the source-named alternatives > 5e-10): %s" % h7)

P("\n== 8  full factorial family of the declared alternatives (A1-A7, B1-B3, C1-C7; author-lineage L_2m; node index A8 declared, NOT computed) ==")
keys = [(cid, key, alts) for cid, cls, key, alts, lab in CH]
tot = 1
for _, _, alts in keys: tot *= len(alts)
P("  family size |F| = %d (product of the a_i of the computed choice points)" % tot)
t1 = time.time()
fam = []
for combo in itertools.product(*[a for _, _, a in keys]):
    sel = {key: v for (cid, key, alts), v in zip(keys, combo)}
    inv, _ = alpha_inv(make_opts(sel), comp_tab)
    fam.append(inv)
fam = np.array(fam)
P("  computed in %.0f s" % (time.time() - t1))
P("  finite values: %d ; alpha^-1 range [%.4g, %.4g]" % (int(np.isfinite(fam).sum()), np.nanmin(fam), np.nanmax(fam)))
rel_f = fam / T_INV - 1
uniq = np.unique(np.round(rel_f / 1e-13).astype(np.int64))
P("  distinct values (resolution 1e-13 relative) : %d" % len(uniq))
P("  windows around the target (relative half-width w): number of members / DISTINCT values inside and local density n(w)/(2w)")
win = {}
for w in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 5e-10, 1e-10, 1e-11, 1e-12):
    m = np.abs(rel_f) <= w
    n_d = len(np.unique(np.round(rel_f[m] / 1e-13).astype(np.int64)))
    win[w] = (int(m.sum()), n_d)
    P("    |miss| <= %8.0e : members %8d , distinct %7d , density %.3e per unit relative deviation" % (w, int(m.sum()), n_d, n_d / (2 * w)))
author_rel = inv0 / T_INV - 1
author_key = int(round(author_rel / 1e-13))
hits_bar = np.unique(np.round(rel_f[(np.abs(rel_f) <= BAR)] / 1e-13).astype(np.int64))
others = [h for h in hits_bar if abs(h - author_key) > 3]
P("  distinct family values within 5e-10 of the target: %d ; of which other than the author-lineage set's own value (allowing 3e-13 rounding): %d" % (len(hits_bar), len(others)))
for h in others[:12]:
    P("      other hit: relative miss %+.3e" % (h * 1e-13))
h5a = len(others) >= 1
close = [h for h in hits_bar if abs(h - author_key) > 3 and abs(h * 1e-13) <= 1e-10]
h5b = len(close) == 0
P("  H5a (at least one distinct family value other than the author-lineage value within 5e-10): %s (%d)" % (h5a, len(others)))
P("  H5b (no other family value within 1e-10): %s (nearest other: %.3e)" % (h5b, min([abs(h * 1e-13) for h in others] + [1.0])))
# which combinations are the other hits
names = [cid for cid, key, alts in keys]
for h in others:
    idx = np.where(np.abs(np.round(rel_f / 1e-13).astype(np.int64) - h) <= 0)[0][0]
    combo = list(itertools.product(*[a for _, _, a in keys]))[idx] if idx < 10**7 else None
    diffs = [(nm, str(v)) for nm, v, (cid, key, alts) in zip(names, combo, keys) if v != alts[0]]
    P("      other hit %+.3e : differs from the printed set in %s" % (h * 1e-13, diffs))
mid = [1e-3, 1e-4, 1e-5, 1e-6]
dens = float(np.mean([win[w][1] / (2 * w) for w in mid]))
lam_bar = dens * 2 * BAR
lam_ach = dens * 2 * max(abs(author_rel), 1e-16)
P("  empirical local density (mean over |miss| <= 1e-3..1e-6) = %.3e per unit relative deviation" % dens)
P("  expected number of distinct family members within 5e-10 of the target by that density = %.3e ; within the author-lineage set's own miss (%.2e) = %.3e" % (lam_bar, abs(author_rel), lam_ach))

json.dump(dict(K=K_NUM, K_closed=K_closed, Ls_M4=Ls_M4[:6], Ls_author=Ls_auth[:6], inv_tab=inv_tab, lam_tab=lam_tab, miss_tab=miss_tab, inv_def=inv_def,
               out_literal=out_lit, out_closed=cl, out_true=out_true, out_volume=vol, inv_closed=inv3, rows_def=rows_def, stage_rows=stage_rows,
               shifts=shift_rows, n_choice=len(CH), n_bar=n_bar, n_eff=n_eff, family_size=tot, distinct=len(uniq), windows={str(k): v for k, v in win.items()},
               n_hits_bar=len(hits_bar), n_other_hits=len(others), density=dens, expected_bar=lam_bar, expected_achieved=lam_ach, spread10=spread10,
               class_counts={c: [len(a) for cid, cl_, k, a, l in CH if cl_ == c] for c in "ABC"}),
          open(os.path.join(HERE, "r3_results%s.json" % ("_MUTATE" if MUTATE else "")), "w"), indent=1, default=str)

flags = dict(H2_printed_definitions=bool(h2_def), H2_author_table=bool(h2_tab), H3=bool(h3), H4=bool(h4), H5a=bool(h5a), H5b=bool(h5b), H7=bool(h7))
expected = dict(H2_printed_definitions=False, H2_author_table=True, H3=True, H4=True, H5a=True, H5b=True, H7=True)
P("\nflags   :", flags)
P("expected:", expected)
ok = flags == expected
P("total runtime %.0f s" % (time.time() - t0))
P("VERDICT of script: %s" % ("recorded flag vector reproduced (exit 0)" if ok else "flag vector differs from the recorded one (exit 1)"))
sys.exit(0 if ok else 1)
