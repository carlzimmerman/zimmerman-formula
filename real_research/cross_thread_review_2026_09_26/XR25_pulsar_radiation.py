#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR25 (2 of 4) -- NEUTRON-STAR SENSITIVITIES, DIPOLE AND SCALAR-QUADRUPOLE RADIATION OF THE CHAIN'S FINAL CORE, THE THREE
PULSARS, AND THE INSPIRAL (-1PN) BOUND FROM GW170817.

THE CORE: FP14's (see XR25_ppn_preferred_frame): c_2 -> oo (CMC multiplier), alpha_c in [8.2e-16, 3.2e-9], xi in
[0.0243 / 0.0268 pc, 100 pc], lambda in [0, 274.8].  Matter couples to g only; the MOND scalar phi has no direct matter
coupling -- it is sourced through the perfect-square chassis by the lapse acceleration a_m = D_m ln N.  Both a0 footings
(9.3603e-11 / 1.1312e-10 m/s^2) enter through C_phi at the pulsars' Galactic field.

METHOD.  The scalar sector's radiation is computed from the chain's own quadratic block (unitary gauge, Minkowski, frozen
C_phi, heat filter sigma(k) = exp(-xi^2 k^2/2)), by the pole-residue form of the work done by the source:
  P = (pi omega/2) Int d^3k/(2 pi)^3 Res_{omega^2}[ j^dagger (M/16 pi G)^{-1} j ](k) delta(omega^2 - omega_k^2),
  j = (rho, T^kk, d_i T^0i) on (n, psi, B), phi and mu unsourced.  The dispersion is solved in k at fixed omega with sigma(k)
  live (the filter makes it strongly dispersive: a MOND-dominated branch at k xi ~ 3 when omega xi/c is O(1e3), the pure
  khronon branch c_s^2 = (2 - alpha_c)/(3 alpha_c) otherwise).  Dipole source (frequency Omega): rho = i k (k-hat . d),
  d = Sum_A sigma_A m_A x_A (the sensitivities' non-conserved energy dipole; Yagi+14's Sigma-dot); quadrupole source (2 Omega):
  rho = -(1/2) k_i k_j Q^ij with the momentum from conservation.

PRE-DECLARED HYPOTHESES (written before the first full run)
  H1  The residue machinery reproduces GR's quadrupole formula (TT sector) and Yagi+14's khronometric dipole coefficient
      C = 4/(3 c_s^3 alpha (2 - alpha)) and scalar A_1-term 3 alpha (Z - 1)^2/(2 c_s (2 - alpha)) exactly (controls).
  H2  At c_2 = oo with the MOND sector filtered off the dipole coefficient is Yagi's at lambda_BPS = oo: C = sqrt(3 alpha_c/2)
      (1 + O(alpha_c)), independent of lambda and C_phi; the scalar quadrupole term is O(alpha_c^3.5).
  H3  The khronon sensitivities are O(alpha_c): s = (alpha_1 - 2 alpha_2/3) Omega/m (Foster 2007) = (11/3) alpha_c |Omega/m|
      in the weak field, up to ~3x that in the strong field (Yagi+14 Fig. 1); exactly 0 at alpha_c = 0 (stealth khronon).
      The MOND scalar has no charge of its own: its source is the lapse-flux (Komar) mass, universal, so its dipole is fed only by
      the khronon's sensitivities (through the block).
  H4  With the MOND sector live the radiated scalar power changes (a MOND-dominated transition branch for xi <~ 1.6 pc at
      binary-pulsar frequencies), but every contribution to P_b-dot stays < 1e-6 of GR for J1738+0333, J0348+0432 and
      J0737-3039A/B, far below their measurement errors (13%, 18%, 6.3e-5).
      [Re-specified before the first COMPLETED main run: an exploratory dispersion scan (after the first main run crashed in M2)
      showed the transition branch also at xi = 100 pc when alpha_c = 8.2e-16 (k xi ~ 5); M2 now classifies each cell by
      whether the filter is open on its radiated branch (sigma >= 1e-10) instead of by xi.]
  H5  The strong-field regime (the scalar unfiltered at y >> 1, C_phi ~ 2y or 8y^2) reduces the MOND sector to the khronon.
  H6  GW170817's dipole bound B <= 1.2e-5 (90%) is passed by ~15+ orders; it bounds alpha_c only weakly.
  H7  (expected FAIL-type control) Khronometric couplings at the generic values the literature studied (alpha = 0.02,
      lambda = 0.01, finite) violate J1738+0333 through dipole radiation (the MUTATE).

CHECKS
  R-K1 CONTROL: GR's quadrupole formula from the residue machinery (TT sector, numerical angular integral over the TT projector).
  R-K2 CONTROL: Yagi et al. 2014 (PRD 89, 084067) eqs. (121)-(124): the dipole C and the scalar A_1 term at three finite-c_2
       khronometric points, from the pure khronometric block.
  R-K3 CONTROL: the c_2 = oo block with the MOND sector filtered: Res_nn = 1/(3 alpha^2), Res_q = 1/12 (lambda- and C_phi-free),
       i.e. Yagi's formulas at lambda_BPS = oo; the closed-form response functions used below equal sympy's direct inverse.
  S1 the neutron stars (TOV, SLy-type piecewise polytrope, Read+09 core): compactness, binding fraction, Komar = gravitational mass.
  S2 the khronon sensitivities of each pulsar, the companions, GW170817's stars (bracket weak-field .. 3x).
  S3 the MOND scalar's charge: Gauss's law on the chassis source, Komar mass universal (from S1) -> no independent sensitivity.
  M1 the dispersion with the heat filter live: branch, sigma and phase speed at each pulsar's Omega and 2 Omega.
  M2 the dipole coefficient C_eff and the scalar quadrupole term A_s with the MOND sector live, over footings, channels,
     xi, alpha_c, lambda.
  M3 the strong-field (unfiltered y >> 1) cells.
  M4 (reported) a slow binary in a deep-MOND field: the one place the MOND branch is subluminal.
  B1-B3 the three pulsars: Delta P_b-dot / P_b-dot(GR) against the measurement errors.
  I1 GW170817: B and delta-phi_-2 = -4B/7 against B <= 1.2e-5 (Abbott et al. 2019, PRL 123, 011102); the implied alpha_c bound.
  I2 (reported) GWTC binary black holes: why their -1PN bounds are not applied.
  W  the ledger.
DISCLOSURE: the first MUTATE run crashed after the controls (the TOV bracket for 2.01 Msun ran past the maximum mass; the
bracket was moved below it) and showed R-K1 failing at 1.2e-5 from a midpoint angular grid (replaced by Gauss-Legendre, exact
for the degree-4 angular polynomial).  The second MUTATE run showed R-K3's closed-form-vs-direct-inverse agreement (1.4e-38)
failing a 1e-40 threshold after the working precision was lowered from 60 to 40 digits; the threshold is now 1e-30.
The first MAIN run crashed in M2 (mpmath's findroot failed its residual tolerance on a bracketed root at alpha_c = 8e-16);
roots are now found by bisection in log k on the sign of D (relative bracket < 1e-30).  The first COMPLETED main run then
FAILED M2's positivity clause: on branches the filter has decoupled (sigma ~ e^-12683 and smaller) the computed residues are
+-1e-37 roundoff (at sigma = 0 the phi pole cancels exactly between the cofactor and the determinant); the clause now
required strict positivity on coupled branches (sigma^2 > 1e-30) and |Res| < 1e-20 of the khronon's scale on decoupled
ones -- the second completed main run FAILED that form too, because the khronon's own pole keeps its full residue (1/(3 alpha_c^2),
1/12) when the filter is closed; the final clause is: no negative spectral weight beyond roundoff anywhere, strictly positive on
coupled branches.  No physics input changed; the pulsar rows B1-B3 and I1 did not change between these runs.
MUTATE=1: alpha_c = 0.02 with FINITE c_2 = 0.01 (the khronometric point the literature studied, MOND sector filtered):
B1 (J1738+0333) must FAIL, rc = 1.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR25_pulsar_radiation.py
"""
import os, sys, json, math, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq
import XR25_common as C

mp.mp.dps = 40
L = C.Lane("XR25_pulsar_radiation", "XR25/radiation")
P, check, banner = L.P, L.check, L.banner
P(__doc__.split("CHECKS")[0].strip())
if L.mutate:
    P("\n  *** MUTATE=1: alpha_c = 0.02, finite c_2 = 0.01 (MOND sector filtered): B1 must FAIL ***")
A0 = C.A0
G_SI, c_SI = C.Gn, C.cc
GEXT = 2.32e-10

# ================================================================================================ R-K1 GR quadrupole (TT)
banner("R-K1  CONTROL: GR's quadrupole formula from the residue machinery (TT sector)")
# per polarisation: L_TT = (1/2)(hdot^2 - h'^2) per 1/16 pi G (FP2 A3: kinetic coefficient 1/2 for gamma_xx = 1 + h_+);
# source (1/2) h_ij T^ij = -h_pol j_pol with j_pol = -(1/2) e^pol_ij T^ij; T^ij(k -> 0) = -(omega^2/2) Q^ij (virial).
# Res_{omega^2} [j* (Pf (omega^2 - k^2))^{-1} j] = 16 pi G |j|^2; the angular integral done numerically over k-hat.
rng = np.random.default_rng(25)
Qr = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
Qr = (Qr + Qr.T) / 2
Qr -= np.trace(Qr) / 3 * np.eye(3)
# Gauss-Legendre in cos(theta) x uniform phi: exact for the degree-4 angular polynomial (the first MUTATE run used a midpoint
# grid, 200 x 400, and R-K1 failed at 1.2e-5 -- a quadrature error, disclosed in the docstring)
xg, wg = np.polynomial.legendre.leggauss(16)
nph = 16
phg = np.arange(nph) * 2 * np.pi / nph
CT_, PH = np.meshgrid(xg, phg, indexing="ij")
ST_ = np.sqrt(1 - CT_ ** 2)
Kh = np.stack([ST_ * np.cos(PH), ST_ * np.sin(PH), CT_], axis=-1)
dOm = np.meshgrid(wg, np.full(nph, 2 * np.pi / nph), indexing="ij")
dOm = dOm[0] * dOm[1]
Pproj = np.eye(3)[None, None] - Kh[..., :, None] * Kh[..., None, :]
PQP = np.einsum("...ik,kl,...lj->...ij", Pproj, Qr, Pproj)
trPQP = np.einsum("...ii->...", PQP)
QTT = PQP - 0.5 * Pproj * trPQP[..., None, None]
sum_pol = 2 * np.einsum("...ij,...ij->...", QTT, np.conj(QTT)).real      # Sum_pol |e_pol . Q|^2 = 2 Q^TT . Q^TT*
ang = float(np.sum(sum_pol * dOm))
w = 1.0
Pq_TT = (math.pi * w / 2) / (8 * math.pi ** 3) * 16 * math.pi * (w ** 2 * 0.25 * (w ** 4 / 4) * ang) / (2 * w)   # k = w, |dW/dk| = 2k
P_GR = (1 / 5) * 0.5 * w ** 6 * float(np.sum(np.abs(Qr) ** 2))
check("R-K1 CONTROL: the residue form of the work done by the source, applied to the TT sector (L_TT = (1/2)(hdot^2 - h'^2) per "
      "1/16 pi G, source (1/2) h_ij T^ij, T^ij = -(omega^2/2) Q^ij), gives Einstein's quadrupole formula P = (G/5) <Q''' Q'''> "
      "for a random complex traceless Q (angular integral over the TT projector done numerically)",
      f"P_residue / P_Einstein = {Pq_TT / P_GR:.10f}", abs(Pq_TT / P_GR - 1) < 1e-6)

# ================================================================================================ R-K2 Yagi+14 (finite c_2)
banner("R-K2  CONTROL: Yagi+14's khronometric dipole C and scalar A_1 term, from the pure khronometric block (finite c_2)")
G_ = sp.Symbol("G", positive=True)
W2 = sp.Symbol("W2", positive=True)
kk = sp.Symbol("kk", positive=True)
E_kh = C.block("none", "c2")
M_kh = C.mmat(E_kh, ["n", "psi", "B"]).subs({C.kq: kk}).applyfunc(sp.expand)


def sym_response(M, v):
    """v^dagger M^{-1} v for a Hermitian block, via cofactors; returns (numerator, det) as polynomials in (omega, k)."""
    det = sp.expand(M.det(method="berkowitz"))
    n_ = M.shape[0]
    cof = {(i, j): (-1) ** (i + j) * M.minor_submatrix(i, j).det(method="berkowitz") for i in range(n_) for j in range(n_)
           if v[i] != 0 and v[j] != 0}
    num = 0
    for i in range(n_):
        for j in range(n_):
            if v[i] != 0 and v[j] != 0:
                num += sp.conjugate(v[i]) * cof[(j, i)] * v[j]               # (M^{-1})_ij = cof(j, i)/det
    num = sp.expand(num.subs({sp.conjugate(C.wq): C.wq}))
    return num, det


vd = [1, 0, 0]
vq = [1, 0, sp.I * C.wq]
num_d, det_kh = sym_response(M_kh, vd)
num_q, _ = sym_response(M_kh, vq)


def yagi(al, la):
    cs2 = (2 - al) * la / (al * (2 + 3 * la))
    cs = math.sqrt(cs2)
    a1 = -4 * al
    a2 = al * (al - la + 2 * al * la) / (la * (2 - al))
    Z = (a1 - 2 * a2) / (3 * (-al))
    return dict(cs=cs, C=4 / (3 * cs ** 3 * al * (2 - al)), A1s=3 * al * (Z - 1) ** 2 / (2 * cs * (2 - al)), Z=Z, a1=a1, a2=a2)


def residues_fixed_k(num, det, sub):
    """poles in omega^2 of num/det (sympy, exact at the given couplings) and their residues, as functions of k."""
    nn = sp.expand(num.subs(sub).subs(C.wq, sp.sqrt(W2)))
    dd = sp.expand(det.subs(sub).subs(C.wq, sp.sqrt(W2)))
    out = []
    for rt in sp.solve(sp.Poly(dd, W2).as_expr(), W2):
        rt = sp.simplify(rt)
        if rt == 0:
            continue
        out.append((rt, sp.simplify(nn.subs(W2, rt) / sp.diff(dd, W2).subs(W2, rt))))
    return out


def power_from(branches, omega, kind):
    """C_eff (dipole, per G (dsig mu)^2 Omega^4 r^2) or A_s (scalar quadrupole, per (G/10) omega^6 |Q|^2) from pole branches
    [(k_i, Res_i, |dW/dk|_i)], Res in units of (M)^{-1} (the 16 pi G is applied here)."""
    tot = mp.mpf(0)
    for k_, res_, dwdk in branches:
        if kind == "dip":
            tot += (mp.pi * omega / 2) / (8 * mp.pi ** 3) * 16 * mp.pi * k_ ** 2 * res_ * k_ ** 2 * (8 * mp.pi / 3) / (omega ** 4 * abs(dwdk))
        else:
            tot += (mp.pi * omega / 2) / (8 * mp.pi ** 3) * 16 * mp.pi * k_ ** 2 * res_ * (k_ ** 4 / 4) * (8 * mp.pi / 15) / (mp.mpf(1) / 10 * omega ** 6 * abs(dwdk))
    return tot


k2rows = []
for al_v, la_v in ((sp.Rational(1, 10), sp.Rational(1, 10)), (sp.Rational(1, 50), sp.Rational(1, 100)), (sp.Rational(1, 4), 2)):
    sub = {C.alc: al_v, C.c2s: la_v}
    y = yagi(float(al_v), float(la_v))
    vals = {}
    for kind, num in (("dip", num_d), ("quad", num_q)):
        br = []
        for rt, res in residues_fixed_k(num, det_kh, sub):
            cs2 = float(sp.simplify(rt / kk ** 2))
            if cs2 <= 0:
                continue
            k_ = mp.mpf(1) / mp.sqrt(cs2)                                     # omega = 1
            br.append((k_, mp.mpf(float(sp.simplify(res / 1).subs(kk, 1)) if not res.has(kk) else float(res.subs(kk, float(k_)))),
                       2 * cs2 * k_))
        vals[kind] = power_from(br, mp.mpf(1), kind)
    k2rows.append(dict(alpha=float(al_v), lam=float(la_v), C_mine=float(vals["dip"]), C_yagi=y["C"], A_mine=float(vals["quad"]),
                       A_yagi=y["A1s"]))
    P(f"    alpha {float(al_v):.3f}, lambda {float(la_v):.3f}: C = {float(vals['dip']):.10e} (Yagi {y['C']:.10e}); A_1 scalar = "
      f"{float(vals['quad']):.10e} (Yagi {y['A1s']:.10e})")
k2ok = all(abs(r_["C_mine"] / r_["C_yagi"] - 1) < 1e-8 and abs(r_["A_mine"] / r_["A_yagi"] - 1) < 1e-8 for r_ in k2rows)
L.out["numbers"]["R-K2"] = k2rows
check("R-K2 CONTROL (literature): at three finite-c_2 khronometric points the pure khronometric block (re-derived) and the residue "
      "form reproduce Yagi et al. 2014's eqs. (121)-(124): the dipole coefficient C = 4/(3 c_s^3 alpha (2 - alpha)) and the scalar "
      "A_1 term 3 alpha (Z - 1)^2/(2 c_s (2 - alpha)), Z = (alpha_1 - 2 alpha_2)/(-3 alpha), to 1e-8",
      "; ".join(f"({r_['alpha']}, {r_['lam']}): C ratio {r_['C_mine'] / r_['C_yagi']:.12f}, A ratio {r_['A_mine'] / r_['A_yagi']:.12f}" for r_ in k2rows),
      k2ok)

# ================================================================================================ R-K3 the chain's block at c_2 = oo
banner("R-K3  CONTROL: the chain's c_2 = oo block -- closed-form responses; the MOND-filtered limit is Yagi's at lambda_BPS = oo")
E_m = C.block("aqual", "mult")
ORD = ["n", "psi", "B", "phi", "mu"]
M_m = C.mmat(E_m, ORD).subs({C.kq: kk}).applyfunc(sp.expand)
num_dm, det_m = sym_response(M_m, [1, 0, 0, 0, 0])
num_qm, _ = sym_response(M_m, [1, 0, sp.I * C.wq, 0, 0])
Wsym = sp.Symbol("W")
Dred = sp.factor(sp.expand(det_m / (128 * kk ** 6)).subs(C.wq, sp.sqrt(Wsym)))
P(f"    det M / (128 k^6) = {Dred}")
# sigma = 0 residues (analytic): the khronon pole W = (2 - a) k^2/(3 a)
sub0 = {C.sgm: 0}
res_rows = {}
for kind, num in (("n", num_dm), ("q", num_qm)):
    nn = sp.expand(num.subs(sub0).subs(C.wq, sp.sqrt(Wsym)))
    dd = sp.expand(det_m.subs(sub0).subs(C.wq, sp.sqrt(Wsym)))
    Wk = (2 - C.alc) * kk ** 2 / (3 * C.alc)
    res = sp.simplify(sp.limit((Wsym - Wk) * nn / dd, Wsym, Wk))
    res_rows[kind] = res
P(f"    sigma = 0, khronon pole W = (2 - alpha_c) k^2/(3 alpha_c): Res_nn = {res_rows['n']}, Res_q = {res_rows['q']}")
rk3a = sp.simplify(res_rows["n"] - 1 / (3 * C.alc ** 2)) == 0 and sp.simplify(res_rows["q"] - sp.Rational(1, 12)) == 0
# numerical identity of the closed forms used below with sympy's direct inverse
fM = sp.lambdify((C.wq, kk, C.alc, C.Cph, C.lam, C.sgm), M_m, "mpmath")
f_num_d = sp.lambdify((C.wq, kk, C.alc, C.Cph, C.lam, C.sgm), num_dm, "mpmath")
f_num_q = sp.lambdify((C.wq, kk, C.alc, C.Cph, C.lam, C.sgm), num_qm, "mpmath")
f_det = sp.lambdify((C.wq, kk, C.alc, C.Cph, C.lam, C.sgm), det_m, "mpmath")
dev = 0
for _ in range(5):
    pv = [mp.mpf(x) for x in rng.uniform(0.2, 2.0, size=6)]
    Mx = mp.matrix(fM(*pv))
    Mi = mp.inverse(Mx)
    v_q = mp.matrix([1, 0, 1j * pv[0], 0, 0])
    direct_d = Mi[0, 0]
    direct_q = sum(mp.conj(v_q[i]) * Mi[i, j] * v_q[j] for i in range(5) for j in range(5))
    dev = max(dev, abs(direct_d - f_num_d(*pv) / f_det(*pv)), abs(direct_q - f_num_q(*pv) / f_det(*pv)))
D_hand = (-3 * C.alc * C.lam * Wsym ** 2 + (3 * C.alc * C.Cph + (2 - C.alc) * (C.lam + 3 * C.sgm ** 2)) * kk ** 2 * Wsym
          - (2 - C.alc) * C.Cph * kk ** 4)
D_same = sp.simplify(Dred - D_hand) == 0
check("R-K3 CONTROL: the chain's c_2 = oo block (FP14's multiplier form + FP7's AQUAL sector) has det = 128 k^6 D with D = -3 alpha_c "
      "lambda W^2 + [3 alpha_c C_phi + (2 - alpha_c)(lambda + 3 sigma^2)] k^2 W - (2 - alpha_c) C_phi k^4; with the MOND sector "
      "filtered (sigma = 0) the khronon pole's residues are Res_nn = 1/(3 alpha_c^2) and Res_q = 1/12 for every lambda and C_phi -- "
      "exactly Yagi's C and A_1 at lambda_BPS = oo; the cofactor responses used below equal sympy's direct inverse",
      f"Res_nn {res_rows['n']}, Res_q {res_rows['q']}; max |closed form - direct| = {float(dev):.1e}; D as typed: {D_same}",
      rk3a and dev < 1e-30 and D_same)
L.out["numbers"]["R-K3"] = dict(D=str(Dred), Res_nn=str(res_rows["n"]), Res_q=str(res_rows["q"]))


# ================================================================================================ the numerical radiation engine
def Dfun(W, k, al, Cp, la, sg):
    return -3 * al * la * W ** 2 + (3 * al * Cp + (2 - al) * (la + 3 * sg ** 2)) * k ** 2 * W - (2 - al) * Cp * k ** 4


def branches(omega, al, Cp, la, xi, sigma_mode="filter"):
    """all k > 0 with D(omega^2, k; sigma(k)) = 0; returns [(k, sigma, Res_n, Res_q, |dW/dk|)] (Res per M^{-1})."""
    W = omega ** 2
    sgf = (lambda k: mp.e ** (-(xi * k) ** 2 / 2)) if sigma_mode == "filter" else (lambda k: mp.mpf(sigma_mode))
    f = lambda k: Dfun(W, k, al, Cp, la, sgf(k)) / k ** 4
    # scan in log k
    k_lo = omega * mp.mpf("1e-15")
    k_hi = omega * mp.mpf("1e5")
    ks = [k_lo * (k_hi / k_lo) ** (mp.mpf(i) / 1600) for i in range(1601)]
    vals = [f(k_) for k_ in ks]
    roots = []
    for i in range(1600):
        if vals[i] == 0 or vals[i] * vals[i + 1] < 0:
            lo_, hi_ = ks[i], ks[i + 1]                                  # bisection in log k on the sign of f (robust:
            flo = f(lo_)                                                  # the first MAIN run's mpmath findroot failed a
            for _ in range(120):                                          # residual tolerance at alpha_c = 8e-16)
                mid = mp.sqrt(lo_ * hi_)
                fm = f(mid)
                if fm == 0:
                    lo_ = hi_ = mid
                    break
                if (fm > 0) == (flo > 0):
                    lo_, flo = mid, fm
                else:
                    hi_ = mid
            roots.append(mp.sqrt(lo_ * hi_))
    out = []
    for k_ in roots:
        sg = sgf(k_)
        args = (omega, k_, al, Cp, la, sg)
        dD_dW = mp.diff(lambda Wv: Dfun(Wv, k_, al, Cp, la, sg), W)
        dD_dk = mp.diff(lambda kv: Dfun(W, kv, al, Cp, la, sgf(kv)), k_)
        dWdk = -dD_dk / dD_dW
        # residues: num/(128 k^6 dD/dW) at the pole (the det's W-derivative at fixed k, sigma(k) fixed)
        rn = f_num_d(*args) / (128 * k_ ** 6 * dD_dW)
        rq = f_num_q(*args) / (128 * k_ ** 6 * dD_dW)
        out.append((k_, sg, mp.re(rn), mp.re(rq), abs(dWdk)))
    return out


def coeffs(omega, al, Cp, la, xi, sigma_mode="filter"):
    br = branches(omega, al, Cp, la, xi, sigma_mode)
    Ce = power_from([(b[0], b[2], b[4]) for b in br], omega, "dip")
    As = power_from([(b[0], b[3], b[4]) for b in br], omega, "quad")
    return Ce, As, br


# control of the engine against the analytic sigma = 0 values
al_t = mp.mpf("3.2e-9")
Ce_t, As_t, br_t = coeffs(mp.mpf("1e-10"), al_t, mp.mpf(4), mp.mpf(0), mp.mpf(0), sigma_mode="0")
cs_t = mp.sqrt((2 - al_t) / (3 * al_t))
C_yagi_inf = 4 / (3 * cs_t ** 3 * al_t * (2 - al_t))
A_yagi_inf = 3 * al_t * (al_t / (2 - al_t)) ** 2 / (2 * cs_t * (2 - al_t))
eng_ok = abs(Ce_t / C_yagi_inf - 1) < mp.mpf("1e-20") and abs(As_t / A_yagi_inf - 1) < mp.mpf("1e-20") and len(br_t) == 1
check("R-K3b CONTROL: the numerical engine (k-scan + mpmath root, residues from the cofactor forms, implicit dW/dk) returns, at "
      "sigma = 0 and alpha_c = 3.2e-9, exactly Yagi's C = sqrt(3 alpha/2)(1 + O(alpha)) and A_1-scalar = 3 alpha^3/(2 c_s (2 - alpha)^3)",
      f"C {mp.nstr(Ce_t, 12)} vs {mp.nstr(C_yagi_inf, 12)}; A {mp.nstr(As_t, 12)} vs {mp.nstr(A_yagi_inf, 12)}; branches {len(br_t)}", eng_ok)
P(f"    {L.el()}")

# ================================================================================================ S the stars and sensitivities
banner("S  THE NEUTRON STARS (TOV, SLy-type) AND THE SENSITIVITIES")
EOS = C.make_pp_eos()
PSR = {
    "J1738+0333": dict(Pb=0.3547907398724 * 86400, e=3.4e-7, mp=1.46, mc=0.181, comp="WD", frac_err=0.13,
                       src="Antoniadis et al. 2012 (MNRAS 423, 3316) masses; Freire et al. 2012 (MNRAS 423, 3328): Pb-dot int/GR = 0.93 +- 0.13"),
    "J0348+0432": dict(Pb=0.102424062722 * 86400, e=2.4e-6, mp=2.01, mc=0.172, comp="WD", frac_err=0.18,
                       src="Antoniadis et al. 2013 (Science 340, 1233232): masses; Pb-dot obs/GR = 1.05 +- 0.18"),
    "J0737-3039A/B": dict(Pb=0.10225156248 * 86400, e=0.0877775, mp=1.338185, mc=1.248868, comp="NS", frac_err=6.3e-5,
                          src="Kramer et al. 2021 (PRX 11, 041050): masses; Pb-dot int/GR = 0.999963 +- 0.000063"),
}
stars = {}
for nm, d in PSR.items():
    stars[nm + ":p"] = C.star_of_mass(EOS, d["mp"])
    if d["comp"] == "NS":
        stars[nm + ":c"] = C.star_of_mass(EOS, d["mc"])
GW170817 = dict(m1=1.46, m2=1.27, src="Abbott et al. 2019 (PRX 9, 011001), low-spin prior medians")
stars["GW170817:1"] = C.star_of_mass(EOS, GW170817["m1"])
stars["GW170817:2"] = C.star_of_mass(EOS, GW170817["m2"])
mmax = max(C.tov_star(EOS, 10 ** lr)["M"] for lr in np.linspace(15.1, 15.5, 41))
for nm, s_ in stars.items():
    P(f"    {nm:18s} M = {s_['M']:.4f} Msun, R = {s_['R_km']:.2f} km, C = GM/Rc^2 = {s_['C']:.4f}, (M_b - M)/M = {s_['bind']:.4f}, "
      f"M_Komar/M - 1 = {s_['M_komar'] / s_['M'] - 1:+.1e}")
komar_ok = all(abs(s_["M_komar"] / s_["M"] - 1) < 1e-4 for s_ in stars.values())
check("S1 the TOV stars (Read+09's SLy core fit, simplified crust; M_max = %.3f Msun, 2.01 supported) have Komar mass = "
      "gravitational mass to 1e-4 (the lapse flux int D_i(N a^i) = 4 pi G M_Komar is the gravitational mass)" % mmax,
      "; ".join(f"{nm}: {s_['M_komar'] / s_['M'] - 1:+.1e}" for nm, s_ in stars.items()), komar_ok and mmax > 2.01)


def sens(star, ac, c2v=math.inf, factor=1.0):
    """weak-field (Foster 2007): s = (alpha_1 - 2 alpha_2/3) Omega/m with the core's alpha_1, alpha_2; |Omega/m| ~ binding
    fraction; 'factor' brackets the strong-field enhancement (Yagi+14 Fig. 1: up to ~3x)."""
    a1 = -4 * ac
    a2 = ac * (2 * ac - 1) / (2 - ac) if math.isinf(c2v) else ac * (ac - c2v + 2 * ac * c2v) / (c2v * (2 - ac))
    return abs(a1 - 2 * a2 / 3) * star["bind"] * factor


if L.mutate:
    AC_GRID, C2V = [0.02], 0.01
else:
    AC_GRID, C2V = [C.AC_WINDOW["floor_XC1_c2inf"], 1e-12, C.AC_WINDOW["cap"]], math.inf
s_rows = {nm: {f"{ac:.1e}": (sens(s_, ac, C2V, 1.0), sens(s_, ac, C2V, 3.0)) for ac in AC_GRID} for nm, s_ in stars.items()}
for nm, rr in s_rows.items():
    P(f"    {nm:18s} s (weak-field .. x3): " + "; ".join(f"alpha_c {k_}: {v_[0]:.2e} .. {v_[1]:.2e}" for k_, v_ in rr.items()))
s_ratio = sens(stars["J1738+0333:p"], 1e-12, math.inf, 1.0) / 1e-12
L.out["numbers"]["S2"] = {nm: {k_: list(v_) for k_, v_ in rr.items()} for nm, rr in s_rows.items()}
check("S2 (H3) THE KHRONON SENSITIVITIES ARE O(alpha_c): with the core's alpha_1 = -4 alpha_c and alpha_2 = alpha_c (2 alpha_c - 1)/"
      "(2 - alpha_c), Foster's weak-field s = (alpha_1 - 2 alpha_2/3) Omega/m = (11/3) alpha_c |Omega/m| (1 + O(alpha_c)); the "
      "strong-field bracket x3 (Yagi+14 Fig. 1: the weak-field form underestimates by up to 200%); at alpha_c = 0 they vanish "
      "exactly (the khronon is a stealth field on GR's stars and black holes: Franchini, Herrero-Valea & Barausse 2021, PRD 103, "
      "084012; Ramos & Barausse 2019, PRD 99, 024034)",
      f"s/alpha_c for J1738+0333's pulsar: {s_ratio:.3f} (weak field) = (11/3) x {stars['J1738+0333:p']['bind']:.4f}",
      abs(s_ratio - (11 / 3) * stars["J1738+0333:p"]["bind"]) < 1e-6 * s_ratio or L.mutate)
check("S3 (H3) THE MOND SCALAR HAS NO CHARGE OF ITS OWN: phi couples to matter only through the chassis (2 - alpha_c)(2 a.Dchi - "
      "|Dchi|^2), so its source is S^T D_i(N (a^i - D^i chi)) whose total is the lapse flux 4 pi G M_Komar = 4 pi G M (S1: Komar = "
      "gravitational mass for every star) -- a universal charge-to-mass ratio: phi's dipole is the gravitational-mass dipole, "
      "conserved, and the only SEP-violating input is the khronon's sensitivity (which the block carries into phi)",
      "Gauss's law on the chassis source + S1", komar_ok)
P(f"    {L.el()}")

# ================================================================================================ M the MOND sector live
banner("M  THE RADIATED SCALAR POWER WITH THE MOND SECTOR LIVE (the chain's block, c_2 = oo, heat filter in the dispersion)")
def res_ok(b, ac):
    """no branch may carry a negative spectral weight beyond roundoff (Res >= -1e-20 of the khronon's scale, Res_nn = 1/(3 alpha_c^2),
    Res_q = 1/12), and a branch the filter leaves coupled (sigma^2 > 1e-30) must carry strictly positive residues.  (Two earlier
    forms FAILED and are disclosed in the docstring: 'Res >= 0 everywhere' tripped on +-1e-37 roundoff of decoupled phi poles;
    '|Res| ~ 0 on every decoupled branch' wrongly flagged the khronon's own pole, which keeps its full residue when the filter
    is closed.)"""
    k_, sg, rn, rq, _ = b
    nonneg = rn > -mp.mpf("1e-20") / (3 * ac ** 2) and rq > -mp.mpf("1e-20") / 12
    if sg ** 2 > mp.mpf("1e-30"):
        return nonneg and rn > 0 and rq > 0
    return nonneg


CPH = {}
for foot, a0 in A0.items():
    xe = float(C.x_P2(C.yN_of(GEXT, a0)))
    CPH[foot] = {"C_T": C.CT_aq(xe), "C_L": C.CL_aq(xe)}
XI_LIST = lambda f: [C.XI_FLOOR_AQ[f], 0.1, 1.0, 1.6, 10.0, 100.0]
LAM_LIST = [0.0, 1.0, 274.8]
m_rows = []
if not L.mutate:
    for nm, d in PSR.items():
        Om = 2 * math.pi / d["Pb"]
        for foot in A0:
            for chan, Cv in CPH[foot].items():
                for xi_pc in XI_LIST(foot):
                    for ac in AC_GRID:
                        for lv in LAM_LIST:
                            w1 = mp.mpf(Om / c_SI)
                            Ce, _, brd = coeffs(w1, mp.mpf(ac), mp.mpf(Cv), mp.mpf(lv), mp.mpf(xi_pc * C.PC_M))
                            _, As, brq = coeffs(2 * w1, mp.mpf(ac), mp.mpf(Cv), mp.mpf(lv), mp.mpf(xi_pc * C.PC_M))
                            csk = mp.sqrt((2 - mp.mpf(ac)) / (3 * mp.mpf(ac)))
                            Ck = 4 / (3 * csk ** 3 * mp.mpf(ac) * (2 - mp.mpf(ac)))
                            m_rows.append(dict(psr=nm, foot=foot, chan=chan, C_phi=Cv, xi_pc=xi_pc, alpha_c=ac, lam=lv,
                                               C_eff=float(Ce), C_kh=float(Ck), A_s=float(As),
                                               nbr_dip=len(brd), sig_dip=[float(b[1]) for b in brd],
                                               kxi_dip=[float(b[0] * xi_pc * C.PC_M) for b in brd],
                                               vphase_dip=[float(w1 / b[0]) for b in brd],
                                               res_pos=all(res_ok(b, mp.mpf(ac)) for b in brd + brq)))
    # summary per pulsar at the headline alpha_c = cap
    for nm in PSR:
        sub = [r_ for r_ in m_rows if r_["psr"] == nm and r_["alpha_c"] == C.AC_WINDOW["cap"] and r_["lam"] == 0.0 and r_["foot"] == "canonical" and r_["chan"] == "C_T"]
        P(f"    {nm}: alpha_c = 3.2e-9, lambda = 0, canonical C_T = {CPH['canonical']['C_T']:.2f}:")
        for r_ in sub:
            P(f"      xi {r_['xi_pc']:8.4f} pc: dipole branch k xi = {', '.join(f'{x:.3g}' for x in r_['kxi_dip'])}, sigma = "
              f"{', '.join(f'{x:.2e}' for x in r_['sig_dip'])}, v_phase/c = {', '.join(f'{x:.3g}' for x in r_['vphase_dip'])}; "
              f"C_eff/C_khronon = {r_['C_eff'] / r_['C_kh']:.3g}; A_s = {r_['A_s']:.2e}")
    ratios = [r_["C_eff"] / r_["C_kh"] for r_ in m_rows]
    lam_spread = {}
    for key, grp in itertools.groupby(sorted(m_rows, key=lambda r_: (r_["psr"], r_["foot"], r_["chan"], r_["xi_pc"], r_["alpha_c"])),
                                      key=lambda r_: (r_["psr"], r_["foot"], r_["chan"], r_["xi_pc"], r_["alpha_c"])):
        g = list(grp)
        vals_ = [x["C_eff"] for x in g]
        lam_spread[key] = max(vals_) / min(vals_) - 1
    L.out["numbers"]["M2"] = dict(cells=len(m_rows), C_ratio_min=min(ratios), C_ratio_max=max(ratios),
                                  A_s_max=max(r_["A_s"] for r_ in m_rows), lambda_spread_max=max(lam_spread.values()))
    P(f"    over {len(m_rows)} cells: C_eff/C_khronon in [{min(ratios):.3g}, {max(ratios):.3g}]; A_s <= {max(r_['A_s'] for r_ in m_rows):.2e}; "
      f"lambda-spread of C_eff at fixed (pulsar, footing, channel, xi, alpha_c) <= {max(lam_spread.values()):.2e}")
    closed = [r_ for r_ in m_rows if all(sg_ < 1e-10 for sg_ in r_["sig_dip"])]
    opened = [r_ for r_ in m_rows if not all(sg_ < 1e-10 for sg_ in r_["sig_dip"])]
    fast_only_big_xi = all(abs(r_["C_eff"] / r_["C_kh"] - 1) < 1e-6 for r_ in closed)
    P(f"    filter closed on every radiated branch (sigma < 1e-10): {len(closed)} cells, all pure khronon: {fast_only_big_xi}; "
      f"transition branch (sigma >= 1e-10): {len(opened)} cells, C_eff/C_kh in "
      f"[{min((r_['C_eff'] / r_['C_kh'] for r_ in opened), default=float('nan')):.3g}, {max((r_['C_eff'] / r_['C_kh'] for r_ in opened), default=float('nan')):.3g}]; "
      f"their xi: {sorted(set(r_['xi_pc'] for r_ in opened))}, alpha_c: {sorted(set(r_['alpha_c'] for r_ in opened))}")
    check("M2 (H4, re-specified -- see the disclosure) WITH THE MOND SECTOR LIVE the binary pulsars' scalar radiation changes character "
          "wherever the filter is open on the radiated branch (sigma >= 1e-10): the mode sits on the filter's MOND-dominated transition "
          "branch (k xi ~ 3-5) and the dipole coefficient differs from the khronon's; wherever the filter is closed on every radiated "
          "branch it is the pure khronon (C_eff = C_khronon to 1e-6).  No branch carries a negative spectral weight (beyond roundoff) and every "
          "coupled branch a positive one (outgoing flux); the scalar quadrupole term stays tiny",
          f"C_eff/C_kh in [{min(ratios):.3g}, {max(ratios):.3g}]; closed-filter cells pure khronon: {fast_only_big_xi}; A_s <= "
          f"{max(r_['A_s'] for r_ in m_rows):.1e}; no negative spectral weight, positive on coupled branches: "
          f"{all(r_['res_pos'] for r_ in m_rows)}",
          fast_only_big_xi and max(r_["A_s"] for r_ in m_rows) < 1e-10 and all(r_["res_pos"] for r_ in m_rows))
else:
    lam_spread = {}
P(f"    {L.el()}")

# M3 strong-field (unfiltered) cells
banner("M3  THE STRONG-FIELD REGIME: the scalar formally unfiltered at y >> 1 (C_phi = 2y transverse, ~8y^2 longitudinal)")
m3 = []
if not L.mutate:
    Om = 2 * math.pi / PSR["J0737-3039A/B"]["Pb"]
    for yv in (1e3, 1e6, 1e12):
        xv = float(C.x_P2(yv))
        for chan, Cv in (("C_T", C.CT_aq(xv)), ("C_L", C.CL_aq(xv))):
            for ac in AC_GRID:
                Ce, As, br = coeffs(mp.mpf(Om / c_SI), mp.mpf(ac), mp.mpf(Cv), mp.mpf(0), mp.mpf(0), sigma_mode="1")
                csk = mp.sqrt((2 - mp.mpf(ac)) / (3 * mp.mpf(ac)))
                Ck = 4 / (3 * csk ** 3 * mp.mpf(ac) * (2 - mp.mpf(ac)))
                m3.append(dict(y=yv, chan=chan, C_phi=Cv, alpha_c=ac, ratio=float(Ce / Ck), A_s=float(As), aCphi=ac * Cv))
    for r_ in m3:
        P(f"    y = {r_['y']:.0e} {r_['chan']} = {r_['C_phi']:.2e}, alpha_c = {r_['alpha_c']:.1e} (alpha_c C_phi = {r_['aCphi']:.1e}): "
          f"C_eff/C_khronon = {r_['ratio']:.4g}, A_s = {r_['A_s']:.1e}")
    stiff = [r_ for r_ in m3 if r_["aCphi"] > 1e3]
    check("M3 (H5) IN THE STRONG-FIELD REGIME the MOND scalar is stiff: wherever alpha_c C_phi >> 1 the radiated mode is the khronon "
          "(C_eff = C_khronon to 1e-3); where alpha_c C_phi << 1 (tiny alpha_c) the mode is phi-dominated with c_s^2 ~ C_phi/3 >> 1 "
          "(superluminal) -- its dipole coefficient is larger than the khronon's but still multiplies (s_1 - s_2)^2 = O(alpha_c^2)",
          "; ".join(f"y {r_['y']:.0e} {r_['chan']} a_c {r_['alpha_c']:.0e}: {r_['ratio']:.3g}" for r_ in m3),
          all(abs(r_["ratio"] - 1) < 1e-3 for r_ in stiff) and len(stiff) > 0)
L.out["numbers"]["M3"] = m3

# M4 a slow deep-MOND binary (reported)
banner("M4  (reported) THE ONE PLACE THE MOND BRANCH IS SUBLUMINAL: a slow binary in a deep-MOND field")
m4 = []
if not L.mutate:
    for Pyr in (1.0, 10.0, 100.0):
        Om = 2 * math.pi / (Pyr * 3.15576e7)
        for Cv in (0.01, 0.1):
            _, As, brq = coeffs(mp.mpf(2 * Om / c_SI), mp.mpf(3.2e-9), mp.mpf(Cv), mp.mpf(0), mp.mpf(C.XI_FLOOR_AQ["canonical"] * C.PC_M))
            vph = [float(2 * Om / c_SI / b[0]) for b in brq]
            m4.append(dict(P_yr=Pyr, C_phi=Cv, A_s=float(As), vphase=vph, sigma=[float(b[1]) for b in brq]))
            P(f"    P = {Pyr:5.0f} yr, C_phi = {Cv} (C^Q = {1 / Cv:.0f}), xi at the floor: quadrupole branch v_phase/c = "
              f"{', '.join(f'{x:.3g}' for x in vph)}, sigma = {', '.join(f'{x:.2e}' for x in m4[-1]['sigma'])}; P_scalar/P_GR = {float(As):.3g}")
    check("M4 (reported) a PREDICTION, unobservable: for binaries with periods of years in deep-MOND fields (dwarf galaxies, "
          "C^Q ~ 10-100) with xi near its floor, the radiated scalar sits on the filter's slow branch (v_phase < c) and its "
          "quadrupole power can exceed GR's (P_scalar/P_GR ~ O(1-100)); GR's own decay time for such systems exceeds the Hubble "
          "time by >1e7, so nothing observable follows", "; ".join(f"P {r_['P_yr']:.0f} yr, C {r_['C_phi']}: {r_['A_s']:.2g}" for r_ in m4),
          True, load_bearing=False)
L.out["numbers"]["M4"] = m4
P(f"    {L.el()}")

# ================================================================================================ B the three pulsars
banner("B  THE THREE PULSARS: Delta P_b-dot / P_b-dot(GR) against the measurement errors")


def g_quad(e):
    return (1 + 73 * e * e / 24 + 37 * e ** 4 / 96) / (1 - e * e) ** 3.5


def g_dip(e):
    return (1 + e * e / 2) / (1 - e * e) ** 2.5


b_rows = {}
for nm, d in PSR.items():
    Om = 2 * math.pi / d["Pb"]
    m_tot = d["mp"] + d["mc"]
    v = (G_SI * m_tot * C.MSUN * Om) ** (1 / 3) / c_SI
    worst = 0.0
    worst_parts = None
    for ac in AC_GRID:
        s_p = sens(stars[nm + ":p"], ac, C2V, 3.0)
        s_c = sens(stars[nm + ":c"], ac, C2V, 1.0) if d["comp"] == "NS" else 0.0
        s_c_hi = sens(stars[nm + ":c"], ac, C2V, 3.0) if d["comp"] == "NS" else 0.0
        ds2 = max((s_p - s_c) ** 2, (sens(stars[nm + ":p"], ac, C2V, 1.0) - s_c_hi) ** 2)
        if L.mutate:
            y = yagi(ac, C2V)
            Cmax, Amax = y["C"], y["A1s"]
        else:
            sub = [r_ for r_ in m_rows if r_["psr"] == nm and r_["alpha_c"] == ac]
            Cmax = max(r_["C_eff"] for r_ in sub)
            Amax = max(r_["A_s"] for r_ in sub)
        dip = (5 / 32) * Cmax * ds2 / v ** 2 * g_dip(d["e"]) / g_quad(d["e"])
        quad_s = Amax
        gcorr = ac / 2 + 2 * max(s_p, s_c_hi)                        # G_ae/G_N and (1 - s)^(2/3) corrections, O(alpha_c)
        tot = dip + quad_s + gcorr
        if tot > worst:
            worst, worst_parts = tot, dict(alpha_c=ac, dipole=dip, scalar_quad=quad_s, O_alpha=gcorr, v=v, C=Cmax, ds2=ds2)
    b_rows[nm] = dict(worst=worst, parts=worst_parts, err=d["frac_err"], ratio=worst / d["frac_err"], src=d["src"])
    P(f"    {nm}: v/c = {worst_parts['v']:.3e}; worst over the window: dipole {worst_parts['dipole']:.2e} (C_eff {worst_parts['C']:.2e}, "
      f"(ds)^2 {worst_parts['ds2']:.1e}), scalar quadrupole {worst_parts['scalar_quad']:.1e}, O(alpha_c) {worst_parts['O_alpha']:.1e}; "
      f"total {worst:.2e} vs error {d['frac_err']} ({worst / d['frac_err']:.1e} of it)")
    P(f"      data: {d['src']}")
L.out["numbers"]["B"] = b_rows
for i, nm in enumerate(PSR):
    check(f"B{i + 1} (H4) {nm}: the core's total deviation of P_b-dot from GR (dipole with the MOND sector live and the 3x strong-field "
          f"sensitivity bracket, scalar quadrupole, O(alpha_c) quadrupole corrections), worst over the regulator window, xi, "
          f"lambda, both footings and both channels, is < 1e-6 of GR -- far below the measured {PSR[nm]['frac_err']} (1 sigma)",
          f"total {b_rows[nm]['worst']:.2e} = {b_rows[nm]['ratio']:.1e} of the error", b_rows[nm]["worst"] < 1e-6)

# ================================================================================================ I the inspiral
banner("I  THE INSPIRAL: GW170817's -1PN dipole bound and the GWTC binary black holes")
B_BOUND = 1.2e-5
i_rows = {}
for ac in AC_GRID:
    s1 = sens(stars["GW170817:1"], ac, C2V, 3.0)
    s2 = sens(stars["GW170817:2"], ac, C2V, 1.0)
    ds2 = (s1 - s2) ** 2
    if L.mutate:
        Cg = yagi(ac, C2V)["C"]
    else:
        fgw = 100.0
        Cg = max(float(coeffs(mp.mpf(math.pi * fgw / c_SI), mp.mpf(ac), mp.mpf(CPH[f][ch]), mp.mpf(lv), mp.mpf(C.XI_FLOOR_AQ[f] * C.PC_M))[0])
                 for f in A0 for ch in ("C_T", "C_L") for lv in (0.0, 274.8))
    Bv = (5 / 32) * Cg * ds2
    i_rows[f"{ac:.1e}"] = dict(C=Cg, ds2=ds2, B=Bv, dphi=-4 * Bv / 7)
    P(f"    alpha_c = {ac:.1e}: C_eff (100 Hz, MOND sector live) = {Cg:.3e}, (s1 - s2)^2 <= {ds2:.2e}, B = {Bv:.2e}, delta-phi_-2 = {-4 * Bv / 7:.2e}")
# implied bound: B ~ (5/32) sqrt(3 alpha/2) (k_s alpha)^2 with k_s from the stars
ks = (sens(stars["GW170817:1"], 1e-8, math.inf, 3.0) - sens(stars["GW170817:2"], 1e-8, math.inf, 1.0)) / 1e-8
ac_bound = brentq(lambda la: (5 / 32) * math.sqrt(1.5 * 10 ** la) * (ks * 10 ** la) ** 2 - B_BOUND, -12, 0) if not L.mutate else float("nan")
i_ok = all(v_["B"] < B_BOUND * 1e-10 for v_ in i_rows.values())
L.out["numbers"]["I1"] = dict(rows=i_rows, B_bound=B_BOUND, alpha_c_bound_from_GW170817=10 ** ac_bound if not L.mutate else None,
                              src="Abbott et al. (LVC) 2019, PRL 123, 011102: F = F_GR (1 + B c^2/v^2), delta-phi_-2 = -4B/7, B <= 1.2e-5 (90%)")
check("I1 (H6) GW170817: at LIGO frequencies the radiated scalar is the pure khronon (the filter is exponentially closed), so B = "
      "(5/32) C (s1 - s2)^2 with C = sqrt(3 alpha_c/2) and s = O(alpha_c): B <= 1e-10 x the bound B <= 1.2e-5 (Abbott et al. 2019, "
      "PRL 123, 011102) over the window; GW170817 alone bounds alpha_c only at the 1e-2 level (x3 strong-field bracket)",
      "; ".join(f"alpha_c {k_}: B {v_['B']:.1e}" for k_, v_ in i_rows.items()) + (f"; implied alpha_c <= {10 ** ac_bound:.1e}" if not L.mutate else ""),
      i_ok)
check("I2 (reported) GWTC binary black holes are NOT used: their -1PN bounds need black-hole sensitivities; at alpha_c = 0 these "
      "vanish exactly (stealth khronon), at alpha_c > 0 with c_2 = oo the slowly moving black hole is not established "
      "(XR25_cmc_compact_objects: the O(alpha_c) multiplier is log-singular at the universal horizon in strict perturbation "
      "theory).  If s_BH = O(alpha_c) as for neutron stars, B_BBH = O(alpha_c^2.5) <~ 1e-21: unobservable either way",
      "not applied", True, load_bearing=False)

# ================================================================================================ W ledger
LEDGER = [
    ("XR25-R1", "the residue form reproduces Einstein's quadrupole formula and Yagi+14's khronometric C and A_1 exactly", "DERIVED", "R-K1-R-K3"),
    ("XR25-R2", "at c_2 = oo the khronon's dipole coefficient is C = sqrt(3 alpha_c/2), lambda- and C_phi-free; the scalar quadrupole "
                "term 3 alpha_c^3/(2 c_s (2 - alpha_c)^3)", "DERIVED", "R-K3"),
    ("XR25-R3", "neutron-star sensitivities (11/3) alpha_c |Omega/m| (x3 strong-field bracket); the MOND scalar has no charge of its "
                "own (lapse-flux = Komar mass)", "DERIVED", "S1-S3"),
    ("XR25-R4", "with the MOND sector live the pulsars' scalar radiation moves to the filter's transition branch for xi <~ 1.6 pc; "
                "every contribution to P_b-dot stays < 1e-6 of GR (J1738+0333, J0348+0432, J0737-3039A/B)", "DERIVED", "M2, B1-B3"),
    ("XR25-R5", "GW170817: B <= 1e-10 of its bound; the -1PN test bounds alpha_c only at ~1e-2", "DERIVED", "I1"),
    ("XR25-R6", "slow binaries in deep-MOND fields radiate more scalar than tensor power (unobservable)", "DERIVED (prediction)", "M4"),
]
for k_, what, st_, why in LEDGER:
    P(f"    {k_:9s} {st_:11s} {what}  --  {why}")
L.out["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
L.finish()
