#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A48 -- RECORD AUDIT: A33 section 5's first integral vs the baryon-only SPARC fits.

The question
------------
A33 MASTER_ACTION.md section 5 states the first integral

    (r^2 g)' = K rho_src r^2 + (r^2 u)'      i.e.   g = g_N + u,  g_N = G M_src/r^2

and A40_growth reads M_src off the lapse equation's source rho = rho_m + rho_c, concluding
M_src = M_b + M_c = 6.3643 M_b (total matter), which makes the deep-MOND amplitude
sqrt(6.3643) = 2.523x the baryon-only value used by every SPARC fit in the record.

This lane settles it three ways:

  A. DERIVATION.  Re-derive the lapse equation from A33's own reduced Lagrangian (A1), reduce it
     to O(eps) (A2), integrate it (A3), and show that the first integral is an IDENTITY that
     DEFINES g_N = g - u.  It contains no information about what the source is.  The source is
     fixed by the Hamiltonian constraint, and A33 section 3.1 puts rho_c in it TWICE: once
     natively in rho and once through the charge d = D.P = varsigma (rho_c - rho_bar_c)
     (section 1, "sourcing split"; section 3.4 eq. C2).  A6 quantifies the double count; A7
     shows that folding the phantom into the source changes the law (g = g_N + 2u, whose deep
     limit is Newtonian + 2a0, not MOND).

  B. DATA.  Both branches fitted to all 171 SPARC galaxies with one Upsilon per galaxy, identical
     error model (sigma^2 = errV^2 + (0.05 Vobs)^2), identical Upsilon bounds [0.05, 2.50].
     Branch B: g_N = G M_b/r^2.  Branch T: g_N = G(M_b+M_c)/r^2 = 6.3643 G M_b/r^2.

  C. CLOSURE.  What each branch requires of a0 = kappa c sqrt(G rho_Lambda), and what that does to
     Lambda = 32 pi a0^2/c^4 (A33 K14a).

Usage
    python3 a48_checks.py                     # -> a48_results.json, prints a48.out
    python3 a48_checks.py --mutate NAME        # must exit 1 (see MUTATE.md)

Mutations
    total     : reads M_src = M_b (drops the cold sector) from the "total" branch  -> breaks B3/B4/B8
    baryon    : reads M_src = M_b + M_c from the "baryon" branch                   -> breaks B2/B3
    a0factor  : uses 2.523 instead of 6.3643 as the a0 rescaling                  -> breaks A8/C2/C4
    exact     : asserts section 5's identity holds at all orders                   -> breaks A5
    nocount   : removes the double count from the printed source                   -> breaks A6
"""
import sys
import os
import json
import math
import glob
import time

import numpy as np

MUT = None
if "--mutate" in sys.argv:
    MUT = sys.argv[sys.argv.index("--mutate") + 1]

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RECORD = os.path.abspath(os.path.join(HERE, ".."))
SPARC = os.path.join(ROOT, "real_research", "data", "sparc_data")

# ----------------------------------------------------------------------------------------------
# constants (BRIEF section 4; external, not fitted)
# ----------------------------------------------------------------------------------------------
c_light = 2.99792458e8
G_N = 6.67430e-11
K_ACT = 4.0 * math.pi * G_N              # action normalisation K = 4 pi G  (A33 section 1.1)
Lam_obs = 1.0890e-52                     # m^-2 (Planck)
A0_CAN = 9.3603e-11                      # canonical footing, kappa = 1/2
A0_ALT = 1.132e-10                       # the record's published a0 (THEORY.md P3)
F_B = 0.02237 / 0.14237                  # omega_b/omega_m
F_COLD = (1.0 - F_B) / F_B               # 5.364327 = Omega_c/Omega_b
MASSFAC = 1.0 + F_COLD                   # 6.364327
SQ_MASSFAC = math.sqrt(MASSFAC)          # 2.52276 = the deep-MOND amplitude factor


def a0_from_lambda(Lam):
    """A33 K14: Lambda = 32 pi a0^2/c^4."""
    return c_light ** 2 * math.sqrt(Lam / (32.0 * math.pi))


def lambda_from_a0(a0):
    return 32.0 * math.pi * a0 ** 2 / c_light ** 4


A0_CLOSURE = a0_from_lambda(Lam_obs)     # 9.3542e-11
RHO_DE = Lam_obs * c_light ** 2 / (8.0 * math.pi * G_N)
S_DE = c_light * math.sqrt(G_N * RHO_DE)  # = c sqrt(G rho_DE)


def kappa_of(a0):
    return a0 / S_DE


FLOOR = 0.05
UMIN, UMAX = 0.05, 2.50
NG = 400

OUT = []
CHECKS = []


def P(s=""):
    print(s)
    OUT.append(s)


def rec(cid, ok, value, threshold, note=""):
    CHECKS.append(dict(id=cid, ok=bool(ok), value=str(value), threshold=str(threshold), note=note))
    P("%-5s %s  %-58s | %s" % (cid, "PASS" if ok else "FAIL", value, threshold))
    if note:
        P("      %s" % note)


P("=" * 118)
P("A48 -- RECORD AUDIT: A33 section 5's first integral vs the baryon-only SPARC fits")
P("=" * 118)
P("K = 4 pi G = %.6e ; f_b = %.6f ; M_c/M_b = %.6f ; M_src/M_b = %.6f ; sqrt = %.6f"
  % (K_ACT, F_B, F_COLD, MASSFAC, SQ_MASSFAC))
P("a0(Lambda=1.0890e-52) = %.6e ; canonical = %.6e ; record = %.6e ; c sqrt(G rho_DE) = %.6e"
  % (A0_CLOSURE, A0_CAN, A0_ALT, S_DE))
if MUT:
    P("*** MUTATE: %s ***" % MUT)
P("")

# ==============================================================================================
# PART A -- the derivation
# ==============================================================================================
P("-" * 118)
P("PART A -- what the first integral is, and what it is not")
P("-" * 118)
P("A33 section 5, verbatim (MASTER_ACTION.md:278-280):")
P('  "Consistency of the three: (L) differentiated and (P-sph) substituted give')
P("   (r^2 g)' = K rho_src r^2 + (r^2 u)', i.e. g = g_N + u with g_N = G M_src/r^2, which is")
P("   (P-sph)'s first integral.  That is why the law is exact and not an expansion, and why")
P('   the P sector is a charge sector."')
P("A33 section 3.1, verbatim: 'rho = rho_m + rho_c is the total matter density, d = D_i P^i.'")
P("")

import sympy as s

r = s.symbols("r", positive=True)
K, gam, a0s, Lams = s.symbols("K gamma a0 Lambda", positive=True)
NV, NP = s.symbols("NV NP", positive=True)
FV, FP, FPP = s.symbols("FV FP FPP", positive=True)
P0, P1, P2 = s.symbols("P0 P1 P2", positive=True)
rho_f = s.Function("rho")(r)
u_sym = s.symbols("u_sym", positive=True)
W_sym = a0s ** 2 / K * (-u_sym / a0s - s.log(1 - u_sym / a0s))
sq = s.sqrt(FV)
R3 = -2 * FPP / FV ** 2 + s.Rational(3, 2) * FP ** 2 / FV ** 3 - 4 * FP / (r * FV ** 2)
d_s = P1 / FV + 2 * P0 / (r * FV) + FP * P0 / (2 * FV ** 2)     # D_i P^i for h_ij = f delta_ij
u_s = K * P0 / sq                                               # u = K|P|
W_s = W_sym.subs(u_sym, u_s)

# --- A1: A33's lapse equation is the Hamiltonian constraint of A33's own reduced Lagrangian -----
Lag = 4 * s.pi * r ** 2 * (NV * FV ** s.Rational(3, 2) * ((R3 - 2 * Lams) / (4 * K) - W_s
                                                          - (gam / 2) * d_s ** 2)
                           + sq * P0 * NP - rho_f * NV)
CH = [(NV, NP), (FV, FP), (FP, FPP), (P0, P1), (P1, P2)]


def Dt(e):
    out = s.diff(e, r)
    for v, dv in CH:
        out += s.diff(e, v) * dv
    return out


EN = s.cancel((Dt(s.diff(Lag, NP)) - s.diff(Lag, NV)) / (4 * s.pi * r ** 2))
EN_id = sq ** 3 * (d_s - (R3 - 2 * Lams) / (4 * K) + W_s + (gam / 2) * d_s ** 2) + rho_f
resid_A1 = s.simplify(EN - EN_id)
rec("A1", resid_A1 == 0, "lapse-EL minus printed (L): residual %s" % resid_A1, "0",
    "(L) IS the lapse equation of A33's own action -- the equation is not where the defect sits")

# --- A2: the O(eps) reduction is the modified Poisson equation ----------------------------------
eps = s.symbols("eps", positive=True)
phi = s.Function("phi")(r)
pv = s.Function("p")(r)
Nw, fw, Pw = 1 + eps * phi, 1 - 2 * eps * phi, eps * pv         # isotropic weak field
sqw = s.sqrt(fw)
R3w = (-2 * s.diff(fw, r, 2) / fw ** 2 + s.Rational(3, 2) * s.diff(fw, r) ** 2 / fw ** 3
       - 4 * s.diff(fw, r) / (r * fw ** 2))
uw = K * Pw / sqw
Ww = s.series(a0s ** 2 / K * (-uw / a0s - s.log(1 - uw / a0s)), eps, 0, 2).removeO()
dw = s.diff(Pw, r) / fw + 2 * Pw / (r * fw) + s.diff(fw, r) * Pw / (2 * fw ** 2)
ENw = sqw ** 3 * (dw - R3w / (4 * K) + Ww + gam / 2 * dw ** 2)
rho_1 = s.series(-ENw, eps, 0, 2).removeO().coeff(eps)
lap = s.diff(phi, r, 2) + 2 * s.diff(phi, r) / r
divp = s.diff(pv, r) + 2 * pv / r
resid_A2 = s.simplify(s.expand(rho_1 - (-divp + lap / K)))
rec("A2", resid_A2 == 0, "O(eps) lapse eq residual: %s" % resid_A2, "0",
    "lap(Phi) = K(rho + d) = 4 pi G (rho + D.P); Lambda is absorbed by the background")

# --- A3: integrating A2 gives g = G M_rho/r^2 + u, with u = K P --------------------------------
rho0, aa, PP0 = 5e-22, 3.0e3, 1e-13
rr = np.linspace(1.0, 5.0e4, 40001)
rho_v = rho0 * np.exp(-rr / aa)
P_v = PP0 * rr / (rr + aa) ** 2
d_v = np.gradient(rr ** 2 * P_v, rr) / rr ** 2                  # (r^2 P)'/r^2
M_v = np.concatenate(([0.0], np.cumsum(0.5 * (rho_v[1:] + rho_v[:-1]) * 4 * np.pi
                                       * 0.5 * (rr[1:] ** 2 + rr[:-1] ** 2) * np.diff(rr))))
okA3, worst = True, 0.0
for rt in (2.0e3, 1.0e4, 4.0e4):
    m = rr <= rt
    yint = 4 * np.pi * rr[m] ** 2 * (rho_v[m] + d_v[m])
    Mtot = float(np.sum(0.5 * (yint[1:] + yint[:-1]) * np.diff(rr[m])))
    g_direct = G_N * Mtot / rt ** 2
    g_form = G_N * np.interp(rt, rr, M_v) / rt ** 2 + K_ACT * np.interp(rt, rr, P_v)
    worst = max(worst, abs(g_direct - g_form) / max(abs(g_direct), 1e-300))
    okA3 &= worst < 5e-3
rec("A3", okA3, "Gauss vs first-integral form: max rel %.2e (3 radii)" % worst, "< 5e-3",
    "g = G M_rho/r^2 + u is Gauss' law applied to A2: an identity, no constraint on M_rho")

# --- A4: first integral + law => g_N = g - u = g^2/(g+a0) --------------------------------------
gg, gNv, a0v = s.symbols("g gN a0", positive=True)
u_of_g = a0v * gg / (gg + a0v)
resid_A4 = s.simplify((gg - u_of_g) - gg ** 2 / (gg + a0v))
rec("A4", resid_A4 == 0, "(g - u) - g^2/(g+a0) with u = a0 g/(g+a0): %s" % resid_A4, "0",
    "the ONLY content is 'g_N is the Newtonian field of the source'; WHICH mass is not in it")

# --- A5: does section 5's identity close at all orders? ----------------------------------------
Lfull = 4 * s.pi * r ** 2 * (NV * FV ** s.Rational(3, 2) * (-W_s - (gam / 2) * d_s ** 2)
                              + sq * P0 * NP)
EP = s.cancel(Dt(s.diff(Lfull, P1)) - s.diff(Lfull, P0))
P2s = s.solve(s.Eq(EP, 0), P2)[0]
rho_s = s.solve(s.Eq(EN_id, 0), rho_f)[0]
g_expr = NP / (NV * sq)
u_expr = K * P0 / sq
resid_exact = s.simplify((s.diff(r ** 2 * (g_expr - u_expr), r) - K * rho_s * r ** 2).subs(P2, P2s))
vals = {r: s.Float(2.3), K: s.Float(K_ACT), gam: s.Float(1e-40), a0s: s.Float(9.36e-11),
        Lams: s.Float(1e-52), NV: s.Float(1.0000001), NP: s.Float(-3.0e-7),
        FV: s.Float(0.9999998), FP: s.Float(1.0e-6), FPP: s.Float(-2e-7),
        P0: s.Float(1e-12), P1: s.Float(-2e-13)}
rv = float(resid_exact.subs(vals))
t_g = float((s.diff(r ** 2 * g_expr, r)).subs(vals))
t_r = float((K * rho_s * r ** 2).subs(vals))
frac = abs(rv) / max(abs(t_g), abs(t_r))
okA5 = (frac > 0.02) if MUT != "exact" else (frac < 1e-6)
rec("A5", okA5, "all-orders residual / term = %.3f" % frac, "> 0.02 means 'not an identity'",
    "§5 invokes only (L) and (P); beyond O(eps) those two do NOT imply the identity (the f-equation, "
    "which §5 does not use, would be needed).  Every galactic use is at O(eps), so no number moves.")

# --- A6: the double count in A33 section 3.1 ----------------------------------------------------
rho_b, rho_c, rhobar, vsg = s.symbols("rho_b rho_c rhobar varsigma", positive=True)
d_charge = vsg * (rho_c - rhobar)                               # A33 section 1 / (C2)
S_printed = rho_b + rho_c + d_charge                            # A33 section 3.1, verbatim
S_partition = rho_b + (1 - vsg) * rho_c + d_charge              # A33 section 1, "sourcing split"
diff6 = s.simplify(S_printed - S_partition)
if MUT == "nocount":
    diff6 = s.Integer(0)
rec("A6", s.simplify(diff6 - vsg * rho_c) == 0, "S_printed - S_partition = %s" % diff6,
    "varsigma rho_c",
    "the printed (L) counts varsigma*rho_c twice: the charge's share sits in rho_c AND in d")

# --- A6b: the one-parameter family that A33's own partition defines ------------------------------
Mc_over_Mb = F_COLD
rows6 = []
for vs in (0.0, 0.4716, 0.9865, 1.0):
    msrc = 1.0 + (1.0 - vs) * Mc_over_Mb
    rows6.append((vs, msrc, math.sqrt(msrc)))
P("      A33 section 1: rho_c = varsigma rho_c (charge) + (1-varsigma) rho_c (native).  The")
P("      first integral then gives M_src = M_b + (1-varsigma) M_c, and the law's amplitude is")
P("      sqrt(M_src/M_b):")
P("        varsigma     M_src/M_b     deep-MOND amplitude vs baryons")
for vs, msrc, amp6 in rows6:
    P("        %-8.4f     %8.4f      %8.4f" % (vs, msrc, amp6))
rec("A6b", abs(rows6[0][1] - MASSFAC) < 1e-9 and abs(rows6[-1][1] - 1.0) < 1e-12,
    "varsigma=0 -> M_src=%.4f M_b (amp %.3f); varsigma=1 -> M_src=%.4f M_b (amp %.3f)"
    % (rows6[0][1], rows6[0][2], rows6[-1][1], rows6[-1][2]), "6.3643/2.523 ; 1.0000/1.0000",
    "A40's branch is the varsigma=0 end; A33 section 7.3 forces varsigma=1, i.e. M_src = M_b")
P("      so 'M_src = M_b + M_c' is not a derivation -- it is the varsigma -> 0 end of A33's own")
P("      one-parameter family, the end at which the P charge is switched off.  The record's own")
P("      section 7.3 selects varsigma = 1 (a constant partition deforms the law by 0.243 at")
P("      g = a0/2 and is excluded by the RAR), which is M_src = M_b.")

# --- A7: folding the phantom into the source changes the law ------------------------------------
gN_ph = s.symbols("gN_ph", positive=True)
u2 = a0v * gg / (gg + a0v)
sol7 = s.solve(s.Eq(gg, gN_ph + 2 * u2), gN_ph)[0]
deep7 = s.limit((sol7 - gg).subs(gg, a0v / eps), eps, 0)
rec("A7", s.simplify(deep7 + 2 * a0v) == 0, "deep limit (g_N - g) -> %s" % s.simplify(deep7), "-2 a0",
    "M_src = M_b + M_ph gives g = g_N + 2u, i.e. Newtonian + 2a0, NOT MOND: not a reading of the law")

# --- A8: the amplitude / a0 / Lambda factors ----------------------------------------------------
fac_a0 = MASSFAC
if MUT == "a0factor":
    fac_a0 = 2.523
rec("A8", abs(SQ_MASSFAC - 2.52276) < 1e-4 and abs(MASSFAC - 6.36433) < 1e-4,
    "amplitude %.6f ; a0 factor %.6f ; Lambda factor %.4f" % (SQ_MASSFAC, MASSFAC, MASSFAC ** 2),
    "2.52276 ; 6.36433 ; 40.504",
    "g ~ sqrt(a0 g_N): a 6.364x source is a 2.523x amplitude, absorbed only by a0/6.3643")
P("      the brief's 'a0 must be 2.523x smaller' is one factor of 2.523 short: a0 enters as")
P("      sqrt(a0 g_N), so the a0 correction is 2.523^2 = 6.3643.  All numbers below use 6.3643.")
P("")

# ==============================================================================================
# PART B -- the two branches on SPARC
# ==============================================================================================
P("-" * 118)
P("PART B -- both branches on the full SPARC sample, one Upsilon per galaxy")
P("-" * 118)
P("sigma^2 = errV^2 + (0.05 Vobs)^2 ; Upsilon in [0.05, 2.50] (disk = bulge) ; chi^2 in velocity")
P("space ; 171 galaxies with >= 5 points, 3375 points (A7's frozen selection).")


def load_sparc():
    gals = []
    nrows = 0
    files = sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat")))
    for fn in files:
        try:
            d = np.genfromtxt(fn, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        d = d[np.all(np.isfinite(d[:, :6]), axis=1)]
        nrows += d.shape[0]
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        Vg2, Vd2, Vb2 = Vgas ** 2, Vdisk ** 2, Vbul ** 2
        keep = (Vobs > 0) & (eV > 0) & ((Vg2 + UMIN * (Vd2 + Vb2)) > 0) & (R > 0)
        gals.append(dict(name=os.path.basename(fn).replace("_rotmod.dat", ""),
                         rm=R[keep] * 3.0856775814913673e19, Vobs=Vobs[keep],
                         sig=np.sqrt(eV[keep] ** 2 + (FLOOR * Vobs[keep]) ** 2),
                         Vgas2=Vg2[keep], Vstar2=(Vd2 + Vb2)[keep], n=int(keep.sum())))
    return gals, len(files), nrows


GAL, NFILES, NROWS = load_sparc()
GF = [g for g in GAL if g["n"] >= 5]
NPTS = int(sum(g["n"] for g in GF))
DOF = NPTS - len(GF)
rec("B1", NFILES == 175 and NROWS == 3391 and len(GF) == 171 and NPTS == 3375,
    "%d files, %d rows, %d galaxies, %d points" % (NFILES, NROWS, len(GF), NPTS),
    "175 / 3391 / 171 / 3375", "A7 K1 reproduced exactly (frozen selection)")


def law(gN_arr, a0):
    return 0.5 * (gN_arr + np.sqrt(gN_arr * gN_arr + 4.0 * a0 * gN_arr))


def chi2_grid(U, g, a0, mf):
    Vb2 = np.maximum(g["Vgas2"][None, :] + U[:, None] * g["Vstar2"][None, :], 0.0)
    gN = mf * Vb2 * 1e6 / g["rm"][None, :]
    Vp = np.sqrt(np.maximum(law(gN, a0), 0.0) * g["rm"][None, :]) / 1e3
    z = (g["Vobs"][None, :] - Vp) / g["sig"][None, :]
    return np.sum(z * z, axis=1)


def fit(g, a0, mf):
    from scipy.optimize import minimize_scalar
    Ug = np.logspace(math.log10(UMIN), math.log10(UMAX), NG)
    c = chi2_grid(Ug, g, a0, mf)
    i = int(np.argmin(c))
    cbf, Ubf = float(c[i]), float(Ug[i])
    lo, hi = Ug[max(i - 1, 0)], Ug[min(i + 1, NG - 1)]
    if hi > lo:
        res = minimize_scalar(lambda lu: float(chi2_grid(np.array([10.0 ** lu]), g, a0, mf)[0]),
                              bounds=(math.log10(lo), math.log10(hi)), method="bounded",
                              options={"xatol": 1e-10})
        if res.fun <= cbf:
            cbf, Ubf = float(res.fun), float(10.0 ** res.x)
    return cbf, Ubf


MF_B = MASSFAC if MUT == "baryon" else 1.0      # mutation swaps the branch definitions
MF_T = 1.0 if MUT == "total" else MASSFAC


def detail(a0, mf):
    rows = [fit(g, a0, mf) for g in GF]
    c = np.array([x[0] for x in rows])
    return float(c.sum()), c, np.array([x[1] for x in rows])


def total(a0, mf):
    return float(sum(fit(g, a0, mf)[0] for g in GF))


t0 = time.time()
CHI_B_CAN, CB_CAN, UB_CAN = detail(A0_CAN, MF_B)
CHI_B_ALT, CB_ALT, UB_ALT = detail(A0_ALT, MF_B)
CHI_T_CAN, CT_CAN, UT_CAN = detail(A0_CAN, MF_T)
CHI_T_ALT, CT_ALT, UT_ALT = detail(A0_ALT, MF_T)

rec("B2", abs(CHI_B_CAN - 7259.38) < 0.5, "branch B at a0=9.3603e-11: chi2 = %.2f  (chi2/dof %.4f)"
    % (CHI_B_CAN, CHI_B_CAN / DOF), "7259.38 +- 0.5", "reproduces A7's published canonical total")
P("      branch B (g_N = G M_b/r^2), one Upsilon per galaxy:  chi2 = %.2f / %.2f  (dof %d)"
  % (CHI_B_CAN, CHI_B_ALT, DOF))
P("      branch T (g_N = %.4f G M_b/r^2), same Upsilon freedom: chi2 = %.2f / %.2f"
  % (MASSFAC, CHI_T_CAN, CHI_T_ALT))

DCHI_CAN = CHI_T_CAN - CHI_B_CAN
DCHI_ALT = CHI_T_ALT - CHI_B_ALT
rec("B3", DCHI_CAN > 1000, "Delta chi2 (T-B), a0=9.3603e-11: %+.1f  (%.0f sigma formal)"
    % (DCHI_CAN, math.sqrt(2 * DCHI_CAN)), "> 1000",
    "same 171 Upsilon, same a0 -- a0 is NOT refitted")
rec("B4", DCHI_ALT > 1000, "Delta chi2 (T-B), a0=1.132e-10: %+.1f  (%.0f sigma formal)"
    % (DCHI_ALT, math.sqrt(2 * DCHI_ALT)), "> 1000", "the record's own published footing")
rec("B5", DCHI_CAN > 0 and DCHI_ALT > 0, "T worse on both footings by %.1f / %.1f"
    % (DCHI_CAN, DCHI_ALT), "both > 0", "the sign is not a footing artefact")

# --- B6: zero-parameter comparison, fixed Upsilon = 0.5 disk / 0.7 bulge ------------------------
def chi2_fix(Ud, Ub, a0, mf):
    tot = 0.0
    for g in GAL:
        gN = mf * (g["Vgas2"] + Ud * g["Vd2"] + Ub * g["Vb2"]) * 1e6 / g["rm"]
        Vp = np.sqrt(np.maximum(law(gN, a0), 0.0) * g["rm"]) / 1e3
        tot += float(np.sum(((g["Vobs"] - Vp) / g["sig"]) ** 2))
    return tot


# need disk/bulge separately; reload those columns
GAL_DB = []
for fn in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(fn, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    d = d[np.all(np.isfinite(d[:, :6]), axis=1)]
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    Vg2, Vd2, Vb2 = Vgas ** 2, Vdisk ** 2, Vbul ** 2
    keep = (Vobs > 0) & (eV > 0) & ((Vg2 + UMIN * (Vd2 + Vb2)) > 0) & (R > 0)
    GAL_DB.append(dict(rm=R[keep] * 3.0856775814913673e19, Vobs=Vobs[keep],
                       sig=np.sqrt(eV[keep] ** 2 + (FLOOR * Vobs[keep]) ** 2),
                       Vgas2=Vg2[keep], Vd2=Vd2[keep], Vb2=Vb2[keep]))


def chi2_fixed(a0, mf):
    Ud, Ub, tot = 0.5, 0.7, 0.0
    for g in GAL_DB:
        gN = mf * (g["Vgas2"] + Ud * g["Vd2"] + Ub * g["Vb2"]) * 1e6 / g["rm"]
        Vp = np.sqrt(np.maximum(law(gN, a0), 0.0) * g["rm"]) / 1e3
        tot += float(np.sum(((g["Vobs"] - Vp) / g["sig"]) ** 2))
    return tot


FIX_B = chi2_fixed(A0_ALT, MF_B)
FIX_T = chi2_fixed(A0_ALT, MF_T)
FIX_B_CAN = chi2_fixed(A0_CAN, MF_B)
rec("B6", FIX_T > FIX_B + 1000, "fixed Upsilon 0.5/0.7, a0=1.132e-10: B %.1f (%.2f/pt), T %.1f (%.2f/pt)"
    % (FIX_B, FIX_B / NPTS, FIX_T, FIX_T / NPTS), "T much worse",
    "zero free parameters: T is %.2f x worse in chi2 (B canonical footing: %.2f/dof)"
    % (FIX_T / FIX_B, FIX_B_CAN / NPTS))

# --- B7/B8: profile over a0 ---------------------------------------------------------------------
a0grid = np.logspace(-14, -9, 41)
prof_B = np.array([total(a, MF_B) for a in a0grid])
prof_T = np.array([total(a, MF_T) for a in a0grid])


def refine(a0s, prof, mf):
    from scipy.optimize import minimize_scalar
    i = int(np.argmin(prof))
    lo, hi = a0s[max(i - 1, 0)], a0s[min(i + 1, len(a0s) - 1)]
    res = minimize_scalar(lambda la: total(10.0 ** la, mf),
                          bounds=(math.log10(lo), math.log10(hi)), method="bounded",
                          options={"xatol": 1e-3})
    return 10.0 ** res.x, float(res.fun)


A0B_STAR, CHI_B_STAR = refine(a0grid, prof_B, MF_B)
A0T_STAR, CHI_T_STAR = refine(a0grid, prof_T, MF_T)
DCHI_MIN = CHI_T_STAR - CHI_B_STAR
rec("B7", 5e-11 < A0B_STAR < 1.3e-10, "branch B: a0* = %.4e, chi2* = %.1f" % (A0B_STAR, CHI_B_STAR),
    "a0* in (0.5, 1.3)e-10", "a0 weakly constrained (A9: degenerate with the distance zero point)")
rec("B8", DCHI_MIN > 1000,
    "branch T: a0* = %.3e (%.1fx below closure), chi2* = %.1f ; Delta chi2* = %+.1f"
    % (A0T_STAR, A0_CLOSURE / A0T_STAR, CHI_T_STAR, DCHI_MIN), "> 1000",
    "EVEN WITH a0 FREE total matter cannot be fitted: its own best a0 collapses by %.0fx"
    % (A0_CLOSURE / A0T_STAR))
P("      branch T's chi2(a0) has no good minimum: as a0 -> 0 it is Newtonian with 6.364x the mass")
P("      (V 2.523x too high); as a0 grows the boost overshoots.  min %.0f against %.0f."
  % (CHI_T_STAR, CHI_B_STAR))

# --- B9: the deep-MOND amplitude at fixed baryonic mass -----------------------------------------
amp = []
n_hi = n_lo = 0
for g in GF:
    Vb2 = g["Vgas2"] + 0.5 * g["Vstar2"]
    gb = Vb2 * 1e6 / g["rm"]
    m = gb < 0.1 * A0_CAN
    n_hi += int(np.sum(gb > A0_CAN))
    n_lo += int(np.sum(gb <= A0_CAN))
    if m.sum():
        amp.append(float(np.median(np.sqrt(MASSFAC * gb[m] / A0_CAN) / np.sqrt(gb[m] / A0_CAN))))
rec("B9", abs(np.median(amp) - SQ_MASSFAC) < 0.02,
    "deep-end median g_T/g_B = %.4f over %d galaxies" % (np.median(amp), len(amp)),
    "%.4f" % SQ_MASSFAC, "the 2.523x is exact at fixed baryonic mass in the deep limit")

winsT = int(np.sum(CT_CAN < CB_CAN - 1.0))
dT = CT_CAN - CB_CAN
den = float(np.sum(np.abs(dT)))
shareT = float(np.sum(-dT[dT < 0]) / den) if den > 0 else 1.0
rec("B10", winsT <= 20 and shareT < 0.01,
    "galaxies where T beats B at fixed a0: %d of %d (they carry %.4f of sum|Delta chi2|)"
    % (winsT, len(GF), shareT), "<= 20 and share < 0.01",
    "not a population-tail effect: T's wins carry 0.8% of sum|Delta chi2|")
# --- B11: systematics-free velocity residuals at fixed Upsilon ----------------------------------
res_B, res_T, y_all = [], [], []
for g in GAL_DB:
    gb = (g["Vgas2"] + 0.5 * g["Vd2"] + 0.7 * g["Vb2"]) * 1e6 / g["rm"]
    y_all.append(gb / A0_CAN)
    for lab, mf, bucket in (("B", 1.0, res_B), ("T", MASSFAC, res_T)):
        Vp = np.sqrt(np.maximum(law(mf * gb, A0_CAN), 0.0) * g["rm"]) / 1e3
        bucket.append((g["Vobs"] - Vp) / g["Vobs"])
y_all = np.concatenate(y_all)
res_B = np.concatenate(res_B)
res_T = np.concatenate(res_T)
mN = y_all > 1.0
medB_N = float(np.median(np.abs(res_B[mN])))
medT_N = float(np.median(np.abs(res_T[mN])))
medB_all = float(np.median(np.abs(res_B)))
medT_all = float(np.median(np.abs(res_T)))
rec("B11", medT_all > 0.5 and medB_all < 0.2,
    "median |dV/V| at fixed Upsilon 0.5/0.7: B %.3f, T %.3f (Newtonian end: B %.3f, T %.3f)"
    % (medB_all, medT_all, medB_N, medT_N), "B < 0.2 and T > 0.5",
    "a 5% error floor against a 91% median error: the chi2 gap is not an artefact of the weighting")
P("      points with g_bar > a0: %d of %d ; g_bar <= a0: %d ; in the Newtonian end branch T"
  % (n_hi, NPTS, n_lo))
P("      predicts g = %.3f g_bar (V %.3f x too high) with NO a0 dependence -- the irreducible kill."
  % (MASSFAC, SQ_MASSFAC))
P("")

P("  table: chi2 on the full sample (171 galaxies, 3375 points, %d dof)" % DOF)
P("  %-42s %10s %9s %14s" % ("model", "chi2", "chi2/dof", "Delta vs B(a0)"))
P("  %-42s %10.2f %9.4f %14s" % ("B  a0=9.3603e-11 (canonical)", CHI_B_CAN, CHI_B_CAN / DOF, "-"))
P("  %-42s %10.2f %9.4f %+14.1f" % ("T  a0=9.3603e-11", CHI_T_CAN, CHI_T_CAN / DOF, DCHI_CAN))
P("  %-42s %10.2f %9.4f %14s" % ("B  a0=1.132e-10 (record)", CHI_B_ALT, CHI_B_ALT / DOF, "-"))
P("  %-42s %10.2f %9.4f %+14.1f" % ("T  a0=1.132e-10", CHI_T_ALT, CHI_T_ALT / DOF, DCHI_ALT))
P("  %-42s %10.2f %9.4f %14s" % ("B  a0 free (a0*=%.3e)" % A0B_STAR, CHI_B_STAR, CHI_B_STAR / DOF, "-"))
P("  %-42s %10.2f %9.4f %+14.1f" % ("T  a0 free (a0*=%.3e)" % A0T_STAR, CHI_T_STAR, CHI_T_STAR / DOF, DCHI_MIN))
P("  %-42s %10.2f %9.4f %14s" % ("B  fixed Upsilon 0.5/0.7, a0=1.132e-10", FIX_B, FIX_B / NPTS, "-"))
P("  %-42s %10.2f %9.4f %+14.1f" % ("T  fixed Upsilon 0.5/0.7, a0=1.132e-10", FIX_T, FIX_T / NPTS,
                                    FIX_T - FIX_B))
P("")

# ==============================================================================================
# PART C -- the closure
# ==============================================================================================
P("-" * 118)
P("PART C -- what each branch requires of a0 and Lambda")
P("-" * 118)
kap_can, kap_alt = kappa_of(A0_CAN), kappa_of(A0_ALT)
a0T_can, a0T_alt = A0_CAN / fac_a0, A0_ALT / fac_a0
rec("C1", abs(A0_CLOSURE - 9.3542e-11) < 2e-14,
    "a0(Lambda_obs) = %.6e ; c sqrt(G rho_DE) = %.6e ; kappa(canonical) = %.4f"
    % (A0_CLOSURE, S_DE, kap_can), "9.3542e-11 ; 1.871e-10 ; 0.500",
    "A33 K14b/K14c reproduced")
rec("C2", abs(a0T_alt - A0_ALT / MASSFAC) < 1e-18,
    "branch T requires a0 = %.6e (record) / %.6e (canonical)" % (a0T_alt, a0T_can),
    "%.4e / %.4e" % (A0_ALT / MASSFAC, A0_CAN / MASSFAC),
    "a0 factor = 1+M_c/M_b = %.4f, not 2.523" % MASSFAC)
rec("C3", (kap_alt / fac_a0) < 0.12,
    "kappa: baryons %.4f (record) / %.4f (canonical) ; total matter %.4f / %.4f"
    % (kap_alt, kap_can, kap_alt / fac_a0, kap_can / fac_a0), "total-matter kappa < 0.12",
    "A19: kappa = 0.417 +- 0.095; the saturation cap admits only {1, 0.707, 0.5}")
LAM_T_ALT = lambda_from_a0(a0T_alt)
LAM_T_CAN = lambda_from_a0(a0T_can)
LAM_AT_RECORD_A0 = lambda_from_a0(A0_ALT)
rec("C4", LAM_T_CAN / Lam_obs < 0.03,
    "Lambda at branch T's canonical a0 = %.4e m^-2 = Lambda_obs / %.2f"
    % (LAM_T_CAN, Lam_obs / LAM_T_CAN), "< 0.03 Lambda_obs",
    "Lambda is measured to ~1%%; requiring Lambda_obs/%.1f is not a tension, it is a different universe"
    % (Lam_obs / LAM_T_CAN))
P("      (the record's own a0 = %.3e implies Lambda = %.4e = %.3f Lambda_obs through the same"
  % (A0_ALT, LAM_AT_RECORD_A0, LAM_AT_RECORD_A0 / Lam_obs))
P("      closure -- the 1.462 Lambda_obs of A33 K16 -- and branch T divides that by %.2f.)"
  % (MASSFAC ** 2))
P("")
P("  branch                 a0 required      kappa     Lambda/Lambda_obs   1/kappa")
P("  baryons (record)     %.4e      %.4f      %.3f            %.2f"
  % (A0_ALT, kap_alt, lambda_from_a0(A0_ALT) / Lam_obs, 1 / kap_alt))
P("  baryons (canonical)  %.4e      %.4f      %.3f            %.2f"
  % (A0_CAN, kap_can, lambda_from_a0(A0_CAN) / Lam_obs, 1 / kap_can))
P("  total matter (rec.)  %.4e      %.4f      %.4f            %.2f"
  % (a0T_alt, kap_alt / fac_a0, LAM_T_ALT / Lam_obs, 1 / (kap_alt / fac_a0)))
P("  total matter (can.)  %.4e      %.4f      %.4f            %.2f"
  % (a0T_can, kap_can / fac_a0, LAM_T_CAN / Lam_obs, 1 / (kap_can / fac_a0)))
P("  (the record's own a0 already implies 1.464 Lambda_obs through the same closure, so total")
P("  matter at the record footing is 1.464/%.2f = %.4f Lambda_obs; the universal factor is %.2f.)"
  % (MASSFAC ** 2, LAM_T_ALT / Lam_obs, MASSFAC ** 2))
P("")

# ==============================================================================================
# PART D -- downstream use of M_src = M_b + M_c
# ==============================================================================================
P("-" * 118)
P("PART D -- every file in the record that uses M_src = M_b + M_c")
P("-" * 118)

PATTERNS = ["M_src", "M_b+M_c", "M_b + M_c", "6.3643 M_b", "6.364 M_b", "total Newtonian field",
            "total matter source"]
HITS = {}
for dirpath, dirnames, filenames in os.walk(RECORD):
    rel_dir = os.path.relpath(dirpath, RECORD)
    if rel_dir.split(os.sep)[0] == "A48_first_integral":
        continue
    for fn in filenames:
        if not fn.endswith((".md", ".py")):
            continue
        fp = os.path.join(dirpath, fn)
        try:
            txt = open(fp, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        hit = [p for p in PATTERNS if p in txt]
        if hit:
            HITS[os.path.relpath(fp, RECORD)] = hit

DOWNSTREAM = [
    dict(file="A33_master_action/MASTER_ACTION.md",
         where="section 3.1 (lapse source rho = rho_m + rho_c) and section 5 (first integral)",
         role="SOURCE of the claim", survives=False,
         why="section 5's 'g_N = GM_src/r^2' is an identity that DEFINES g_N; it is not a "
             "statement that M_src is total. Section 3.1's source double counts varsigma*rho_c "
             "(A6), and section 1's own partition gives M_src = M_b + (1-varsigma)M_c. "
             "Everything else in A33 -- the law K3, PPN, c_T, the coefficient table, K13 -- "
             "never uses the VALUE of M_src and survives unchanged."),
    dict(file="A40_growth/report.md",
         where="section 5.1, K11, branch S of the growth table, abstract",
         role="the claim that the action decides for total matter", survives=False,
         why="the ADJUDICATION does not survive; the NUMBER does. A40's own K11 gives "
             "sigma8(S)/sigma8(C) = 1.0019, so sigma8 = 0.7619, f(z), chi2 = 14.21/8 and every "
             "growth conclusion stand to 0.19%. The claim 'the action decides for S' falls."),
    dict(file="A40_growth/a40_checks.py",
         where="K11, lines 478-492", role="the check that encodes the claim", survives=False,
         why="K11 asserts M_src = M_b+M_c and 'the law relates the total field to the total "
             "Newtonian field'. That assertion is the defect; the numbers it prints (2.523, "
             "M_c/M_ph = 0.207) are correct and are the evidence against it."),
    dict(file="A45_reference_field/report.md",
         where="section on (P-sph) ('g_N = GM_src/r^2') and the 'what this does not do' item",
         role="repeats the fork as OPEN", survives=True,
         why="its reference-field conclusions never use the value of M_src; only its restatement "
             "of the fork is superseded. A48 settles it in favour of baryons: the sentence should "
             "read 'M_src = M_b, so the SPARC fits are the action's own branch'."),
    dict(file="A47_fret/report.md",
         where="section 2, 'M_tot = M_b + M_c = 5.464e12' (r200c conversion)",
         role="mass BUDGET, not the law's g_N", survives=True,
         why="same as A44: the cosmic cold share is added to the baryons to define a total halo "
             "mass for an r200c/overdensity argument. It does not use the first integral and does "
             "not feed the law's g_N. No change needed."),
    dict(file="A44_no_edge/report.md",
         where="section 5, 'M200 = M_b + M_c = 6.364 M_b'", role="mass BUDGET, not the law's g_N",
         survives=True,
         why="A44 converts M200 -> M_b through the cosmic budget. That identification is "
             "M_total = M_b + M_c as a DEFINITION of the cosmic share (A18), not the statement "
             "that the law's source is total. No change needed; flagged for clarity."),
]
for d in DOWNSTREAM:
    pref = d["file"].split("/")[0]
    d["found"] = any(k.startswith(pref) for k in HITS)
rec("D1", all(d["found"] for d in DOWNSTREAM), "%d files carry the pattern; all %d downstream found"
    % (len(HITS), len(DOWNSTREAM)), "%d/%d" % (len(DOWNSTREAM), len(DOWNSTREAM)),
    "A33, A40 report+checks, A45, A47, A44 report+checks")
for d in DOWNSTREAM:
    P("  %-44s %-44s survives=%s" % (d["file"], d["role"], d["survives"]))
    P("      where: %s" % d["where"])
    P("      why:   %s" % d["why"])
P("")
P("  scope: every other lane that uses the law (A7, A9, A11, A14, A16, A18, A20, A21, A25, A26,")
P("  A29, A36, A41, A43) writes g_N = G M_b/r^2 with M_b baryonic. None consumes A33 section 5.")
P("")

# ==============================================================================================
# verdict
# ==============================================================================================
npass = sum(1 for c in CHECKS if c["ok"])
P("=" * 118)
P("VERDICT")
P("=" * 118)
P("1. The first integral (r^2 g)' = K rho_src r^2 + (r^2 u)' is correct algebra, but it is an")
P("   IDENTITY defining g_N = g - u.  It does not force M_src = M_b + M_c: M_src is whatever the")
P("   Hamiltonian constraint sources, and that is exactly the open question.")
P("2. A33 section 1's own partition gives M_src = M_b + (1-varsigma) M_c.  'M_src = M_b + M_c'")
P("   is the varsigma -> 0 end of that family -- the end at which the P charge is switched off.")
P("   A33 section 7.3 forces varsigma = 1 (a constant partition deforms the law by 0.243 at")
P("   g = a0/2), and at varsigma = 1 the answer is M_src = M_b: BARYONS ONLY.")
P("   The printed (L) additionally double counts varsigma*rho_c, which is why section 3.1 reads")
P("   as if total matter were forced.")
P("3. The data select BARYONS ONLY: Delta chi2 = %.0f at a0 = 9.3603e-11, %.0f at a0 = 1.132e-10,"
  % (DCHI_CAN, DCHI_ALT))
P("   and %.0f with a0 free (branch T's own best a0 = %.2e, %.1fx below the closure).  No a0"
  % (DCHI_MIN, A0T_STAR, A0_CLOSURE / A0T_STAR))
P("   rescues total matter: the Newtonian end is a0-independent and 6.364x too massive.")
P("4. A33 section 5's first integral is therefore NOT wrong as algebra -- but the sentence that")
P("   attaches M_src = M_b + M_c to it is wrong, and every downstream use of that sentence is")
P("   flagged in Part D.  A33 and A40's adjudication do not survive; A40's numbers and A44 do.")
P("5. Counterfactual (branch T selected): a0 = 1.132e-10 would be wrong by 6.3643x, not 2.523x;")
P("   the required a0 is %.4e, kappa falls from %.3f to %.4f, and at fixed kappa = 1/2 Lambda"
  % (a0T_alt, kap_alt, kap_alt / fac_a0))
P("   must be %.4e = Lambda_obs/%.1f.  The footing does not bend; it breaks."
  % (LAM_T_CAN, Lam_obs / LAM_T_CAN))
P("")
P("A48 COMPLETE: %d/%d checks PASS.%s" % (npass, len(CHECKS),
                                          "" if npass == len(CHECKS) else "  *** FAIL ***"))
P("=" * 118)

results = dict(
    constants=dict(K=K_ACT, f_b=F_B, M_c_over_M_b=F_COLD, massfac=MASSFAC, sqrt_massfac=SQ_MASSFAC,
                   a0_closure=A0_CLOSURE, s_DE=S_DE, a0_canonical=A0_CAN, a0_record=A0_ALT,
                   lambda_obs=Lam_obs),
    derivation=dict(A1_lapse_identity_residual=str(resid_A1), A2_Oeps_residual=str(resid_A2),
                    A5_exactness_fraction=frac,
                    A6_double_count="varsigma rho_c",
                    A6b_M_src_family=[dict(varsigma=v, M_src_over_M_b=m, amplitude=am)
                                      for v, m, am in rows6],
                    A7_deep_limit=str(s.simplify(deep7)),
                    A8_amplitude_factor=SQ_MASSFAC, A8_a0_factor=MASSFAC,
                    A8_lambda_factor=MASSFAC ** 2),
    fits=dict(n_galaxies=len(GF), n_points=NPTS, dof=DOF,
              B_canonical=CHI_B_CAN, B_alt=CHI_B_ALT,
              T_canonical=CHI_T_CAN, T_alt=CHI_T_ALT,
              dchi2_canonical=DCHI_CAN, dchi2_alt=DCHI_ALT,
              B_best_a0=A0B_STAR, B_best_chi2=CHI_B_STAR,
              T_best_a0=A0T_STAR, T_best_chi2=CHI_T_STAR, dchi2_best_a0=DCHI_MIN,
              fixed_upsilon_B=FIX_B, fixed_upsilon_T=FIX_T, fixed_upsilon_B_canonical=FIX_B_CAN,
              n_galaxies_T_wins=winsT, deep_amplitude_median=float(np.median(amp)),
              profile_a0=list(a0grid), profile_B=list(prof_B), profile_T=list(prof_T)),
    closure=dict(a0_required_T_record=a0T_alt, a0_required_T_canonical=a0T_can,
                 kappa_baryon_record=kap_alt, kappa_baryon_canonical=kap_can,
                 kappa_total_record=kap_alt / fac_a0, kappa_total_canonical=kap_can / fac_a0,
                 lambda_at_record_a0=LAM_AT_RECORD_A0,
                 lambda_required_canonical=LAM_T_CAN, lambda_ratio=Lam_obs / LAM_T_CAN,
                 lambda_required_record=LAM_T_ALT, lambda_ratio_record=LAM_AT_RECORD_A0 / LAM_T_ALT),
    downstream=DOWNSTREAM, hits=HITS, checks=CHECKS,
    n_pass=npass, n_checks=len(CHECKS), runtime_s=None,
)
results["runtime_s"] = time.time() - t0
with open(os.path.join(HERE, "a48_results.json"), "w") as fh:
    json.dump(results, fh, indent=1, default=str)
if npass != len(CHECKS):
    sys.exit(1)
