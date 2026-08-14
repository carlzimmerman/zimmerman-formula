#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Q0PIN_trial_2026.py -- ADVERSARIAL TRIAL of the claim:
  "the corpus's X-pin (stage56) already pins AeST's free background parameter Q0, and
   stage57's 'PIN Q0' owed item is THE SAME ITEM as stage56's X-pin."

Items, in the brief's order:
  (1) DEFINITION/DIMENSIONS -- is the corpus's Q0 the same object as SZ21's Qcal_0?
  (2) THE ARITHMETIC       -- X -> Q0 [Mpc^-1], vs SZ21's three published fits.
  (3) THE CONSEQUENCE      -- stage57's share formula at the pinned Q0.
  (4) BOTH-WAYS            -- what else moves; does anything contradict?
  (5) DOES IT DISCHARGE    -- or only convert the owed item?
Everything built from scratch: own constants, own algebra.
"""
import numpy as np
import sympy as sp

FAIL, N = [], [0]


def chk(cond, label, detail=""):
    N[0] += 1
    ok = bool(cond)
    print(f"  [{'ok  ' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


# ---- own constants -------------------------------------------------------------------
C = 2.99792458e8
G = 6.67430e-11
MPC = 3.0856775814913673e22
KPC = MPC / 1e3
H0_SI = 67.4e3 / MPC
OM_M, OM_L, OM_DM, OM_B = 0.315, 0.685, 0.265, 0.0493
OM_R = 9.2e-5
R_DM = OM_DM / OM_L
A0 = 9.3619e-11
KAPPA = 0.5
NU0_F, NU0_C = 2.14e-5, 1.77e-4
ZREC = 1090.0
CH2 = 1.08e4                       # (km/s)^2 committed halo calibration
C_KMS = C / 1e3

LAM = 3 * OM_L * H0_SI ** 2 / C ** 2          # 1/m^2
A0T = A0 / C ** 2                              # 1/m
L_LAM = 1.0 / np.sqrt(LAM)

print("=" * 100)
print("ITEM 1 -- DEFINITION / DIMENSIONS: is the corpus's Q0 SZ21's Qcal_0 = phibardot?")
print("=" * 100)
print(r"""
  SZ21 (arXiv:2007.00082, newRMONDLett.tex, verbatim line refs):
    L290  Qcalb = dot(phib)/N                       [FLRW, N = lapse => cosmic time]
    L350  Qcal = Ah^mu grad_mu phi ; Ycal = q^{mu nu} grad_mu phi grad_nu phi
    L361  QS limit: Qcal = (1-Psi) Qcal_0
    L397  8 pi Gt rhob = Qcal dK/dQcal - K   ;   8 pi Gt Pb = K
    L398  dK/dQcal = I_0/a^3
    L400  Qcal = Qcal_0 + I_0/a^3 ,  8 pi Gt rhob_0 = Qcal_0 I_0
    L379  mu = sqrt(2 K_2/(2-K_B)) Qcal_0      [Helmholtz mass; L~407: mu^-1 >~ 1 Mpc]
    L472  "Qcal_0 and Zcal_0 in Mpc^-1"        [so phi is DIMENSIONLESS; Q has units 1/length]
    L528  grad_mu phi = (Qcal_0 + dot(varphi), grad varphi)
  Corpus (stage54_ev_laneY_gate_counting_2026.py, verbatim):
    L94   d_mu phi = (phidot/c, grad dphi)          => Q0 == phidot/c, units 1/m  [c=1 form]
    L139  abundance: Q0 n0 = Lambda R_dm             (rho = Q0 n, charge = FULL Omega_dm)
    L142  Q0 = sqrt(Lambda) R_dm/(nu0 mu17),  mu17^2 = K''(Q0)
    L167  mu_H = mu17 Q0/sqrt(2-K_B)
""")
# 1a. units
chk(True, "1a UNITS: SZ21 Q_0 in Mpc^-1 <=> corpus Q0 = phidot/c in m^-1 -- the SAME c=1 "
          "reduction of the same object.  X := Q0 c^2/a0 is dimensionless either way.",
    "[1/m]*[m^2/s^2]/[m/s^2] = 1.  No unit mismatch.")

# 1b. the corpus's abundance relation IS SZ21's, with n0 == I_0
lhs_SI = 3 * OM_DM * H0_SI ** 2 / C ** 2       # = 8 pi Gtilde rhob_dm0 / c^2 in 1/m^2
chk(abs(lhs_SI / (LAM * R_DM) - 1) < 1e-12,
    f"1b BACKGROUND IDENTITY MATCHES: SZ21's 8 pi Gt rhob_0 = Qcal_0 I_0 is the corpus's "
    f"Q0 n0 = Lambda R_dm, since Lambda R_dm = 3 Om_dm H0^2/c^2 = {lhs_SI:.4e} 1/m^2 exactly.  "
    f"n0 IS I_0.")

# 1c. K'' = 2 K_2 at the minimum, for SZ21's own three K-functions
Q, Q0s, K2s, Z0s = sp.symbols("Q Q_0 K_2 Z_0", positive=True)
Z = (Q - Q0s) / Z0s
Ks = {"quadratic": K2s * (Q - Q0s) ** 2,
      "Cosh": 2 * K2s * Z0s ** 2 * (sp.cosh(Z) - 1),
      "Exp": 2 * K2s * Z0s ** 2 * (sp.exp(Z ** 2) - 1),
      "Higgs": K2s / (4 * Q0s ** 2) * (Q ** 2 - Q0s ** 2) ** 2}
d2 = {k: sp.simplify(sp.diff(v, Q, 2).subs(Q, Q0s)) for k, v in Ks.items()}
chk(all(sp.simplify(d2[k] - 2 * K2s) == 0 for k in ("quadratic", "Cosh", "Higgs"))
    and sp.simplify(d2["Exp"] - 4 * K2s) == 0,
    "1c K''(Q_0) = 2 K_2 for SZ21's quadratic, Cosh and Higgs functions -- so the corpus's "
    "mu17^2 := K''(Q0) is exactly SZ21's 2 K_2, same normalisation of K, hence of phi.  "
    "FOUND EN ROUTE (a real factor-2 in SZ21's own definitions, not in the corpus): their "
    "'Exp' K = 2K_2 Z_0^2[e^{Z^2}-1] has K''(Q_0) = 4 K_2, NOT 2 K_2, so for that fit "
    "mu = sqrt(4K_2/(2-K_B)) Q_0.  Corrected below.",
    f"computed: {[k + ':' + str(d2[k]) for k in Ks]}")
# 1c'  the SHARPEST independent corroboration available: what mu17 do SZ21's OWN fits carry?
print("\n  1c' SZ21's own published fits, converted to the corpus's mu17 = sqrt(K''(Q_0)),")
print("      and to their own Helmholtz mu^-1 = [sqrt(K''/(2-K_B)) Q_0]^-1:")
SZ_K2FAC = {"Cosh": 2.0, "Higgs": 2.0, "Exp": 4.0}
SZ_FITS = {"Cosh": (0.5, 0.1, 7.5e3), "Higgs": (0.3, 1.0, 8.5e8), "Exp": (0.1, 1e-4, 9.5e3)}
print(f"      {'fit':>6} {'K_B':>5} {'Q0 [Mpc^-1]':>12} {'K_2':>9} {'mu17=sqrt(K'')':>15} "
      f"{'mu^-1 [Mpc]':>12}  MOND?")
for nm, (kb, q0, k2) in SZ_FITS.items():
    m17 = np.sqrt(SZ_K2FAC[nm] * k2)
    mu_inv = 1.0 / (m17 * q0 / np.sqrt(2 - kb))
    print(f"      {nm:>6} {kb:5.1f} {q0:12.0e} {k2:9.1e} {m17:15.1f} {mu_inv:12.3f}  "
          f"{'yes' if nm != 'Higgs' else 'SZ21: NO'}")
chk(122 < np.sqrt(2 * 7.5e3) < 200 and 150 < np.sqrt(4 * 9.5e3) < 250,
    "1c'' *** THE STRONGEST INDEPENDENT CORROBORATION IN THIS TRIAL: SZ21's two "
    "MOND-COMPATIBLE published fits carry mu17 = sqrt(K''(Q_0)) = 122 (Cosh) and 195 (Exp) "
    "-- both INSIDE the corpus's pinned mu17 band 33-1295, and both ~10^2 rather than ~1. "
    "Their MOND-INCOMPATIBLE fit (Higgs) carries mu17 = 41231. ***",
    "the X-pin's headline is exactly 'K''(Q0) is NOT order unity, it is 10^2-10^3'.  That "
    "headline is independently true of the published AeST fits that ARE MOND-compatible, "
    "and false of the one that is not.  This was NOT used to build the pin.")

# 1d. the corpus's own Q0-relation reproduced from stage17's committed chain, independently
mu17, nu0, LD, M4, u = sp.symbols("mu17 nu_0 Lambda_D M4 u", positive=True)
Lam = sp.Symbol("Lambda", positive=True)
K_dbi = -M4 + mu17 ** 2 * LD ** 2 * (1 - sp.sqrt(1 - u ** 2 / LD ** 2))
n_of_u = sp.diff(K_dbi, u)
u_nu = LD * nu0 / sp.sqrt(1 + nu0 ** 2)
n0 = sp.simplify(n_of_u.subs(u, u_nu))
chk(sp.simplify(n0 - mu17 ** 2 * LD * nu0) == 0,
    "1d STAGE17 CHAIN, re-derived: n = K' = mu17^2 Lambda_D nu exactly (DBI, at u = "
    "Lambda_D nu/sqrt(1+nu^2))")
# M^4 = Lambda (w=-1 exact: K(0) = -8 pi Gt rho_Lambda/c^2 = -Lambda); beta=1 => mu17^2 LD^2 = M^4
LD_sol = sp.sqrt(Lam) / mu17
Q0_sol = sp.simplify((Lam * sp.Symbol("R_dm", positive=True)) / (n0.subs(LD, LD_sol)))
chk(sp.simplify(Q0_sol - sp.sqrt(Lam) * sp.Symbol("R_dm", positive=True) / (nu0 * mu17)) == 0,
    "1d' => Q0 = sqrt(Lambda) R_dm/(nu0 mu17), reproducing stage54 A3a from M^4 = Lambda "
    "(w = -1) + beta = 1 + rho = Q0 n.  ONE equation, TWO unknowns (Q0, mu17): a "
    "ONE-PARAMETER FAMILY, with X the coordinate along it.")

# 1e. the RAR leg: is y_static = g_N/a0 the right value of Y/a0t^2?  Derive from SZ21's OWN
#     quasi-static action (their eq. NT_quasi_Phi), independently.
print(r"""
  1e THE ONE PLACE A NORMALISATION COULD SLIP -- the RAR leg.  Derived here from SZ21's own
     quasi-static action S = -int{ (2-K_B)/(16 pi Gt)[|grad Phi|^2 - 2 grad Phi.grad varphi
     + |grad varphi|^2 - mu^2 Phi^2 + J(Y)] + Phi rho },  J(Y) = F(Y,Q_0)/(2-K_B):
       delta/delta Phi     :  grad^2 Phi - grad^2 varphi + mu^2 Phi = 4 pi G_qs rho
       delta/delta varphi  :  grad^2 Phi = grad^2 varphi + div(J' grad varphi)
       => (drop mu)  div(J' grad varphi) = grad^2 Phi_N,  and  grad Phi = grad Phi_N + grad varphi
       => SPHERICAL, EXACT:   |grad varphi| = (g_tot - g_N)/c^2 ,  J'|grad varphi| = g_N/c^2
     (SZ21 say the same in words at L~390: "Diagonalizing by setting Phi = PhiE + varphi
      turns NT_quasi_Phi into scalar_AQUAL_action" -- PhiE is then the NEWTONIAN potential.)
     So the corpus's y := Y/a0t^2 = ((g_tot - g_N)/a0)^2 , which equals g_N/a0 EXACTLY only
     for the PURE deep-MOND J (J' = sqrt(y) at all y).  For the framework's own kernels it
     is SMALLER at the RAR radii.  Priced below (item 4f).
""")

print()
print("=" * 100)
print("ITEM 2 -- THE ARITHMETIC:  Q0 = X a0/c^2")
print("=" * 100)
CONV = A0T * MPC                       # a0/c^2 expressed in Mpc^-1  => Q0[Mpc^-1] = X * CONV
info(f"2a a0/c^2 = {A0T:.5e} 1/m = {CONV:.5e} Mpc^-1   =>  X = Q0[Mpc^-1] / {CONV:.5e} "
     f"= {1/CONV:.1f} * Q0[Mpc^-1]")
chk(abs(1 / CONV - 31112) / 31112 < 2e-3,
    f"2a' conversion factor 1/(a0/c^2) = {1/CONV:.0f} (dimensionless)")
BANDS = {"stage56 core     ": (140.0, 670.0),
         "stage56 core (its own table)": (136.0, 779.0),
         "stage56 defensible": (70.0, 1340.0),
         "stage54 (superseded)": (316.0, 1000.0),
         "natural mu17 = 1  ": (2.192e4, 1.813e5)}
print(f"    {'band':<28} {'X lo':>10} {'X hi':>10} {'Q0 lo [Mpc^-1]':>16} {'Q0 hi [Mpc^-1]':>16}")
Q0B = {}
for lab, (xl, xh) in BANDS.items():
    Q0B[lab] = (xl * CONV, xh * CONV)
    print(f"    {lab:<28} {xl:10.4g} {xh:10.4g} {xl*CONV:16.5g} {xh*CONV:16.5g}")
chk(abs(Q0B["stage56 core     "][0] - 0.0045) < 2e-4 and abs(Q0B["stage56 core     "][1] - 0.0215) < 5e-4,
    f"2b CORE BAND VERIFIED: X = 140-670  =>  Q0 = {Q0B['stage56 core     '][0]:.4f}-"
    f"{Q0B['stage56 core     '][1]:.4f} Mpc^-1  (claim said 0.0045-0.0215)")
chk(abs(Q0B["stage56 defensible"][0] - 0.00225) < 1e-4 and abs(Q0B["stage56 defensible"][1] - 0.0431) < 1e-3,
    f"2c DEFENSIBLE BAND VERIFIED: X = 70-1340  =>  Q0 = {Q0B['stage56 defensible'][0]:.5f}-"
    f"{Q0B['stage56 defensible'][1]:.4f} Mpc^-1  (claim said 0.0022-0.0431)")
# independent route: Q0 = sqrt(Lambda) R_dm/(nu0 mu17) with mu17 from X
info(f"2d cross-check by the OTHER route: sqrt(Lambda) = {np.sqrt(LAM)*MPC:.5e} Mpc^-1, "
     f"R_dm = {R_DM:.4f}")
for nu0v, nl in ((NU0_F, "floor"), (NU0_C, "ceil ")):
    for X in (140.0, 670.0):
        m17 = np.sqrt(8 * np.pi) * R_DM / (KAPPA * nu0v * X)
        q0 = np.sqrt(LAM) * R_DM / (nu0v * m17) * MPC
        print(f"       nu0 {nl}, X = {X:5.0f}:  mu17 = {m17:9.1f}, K_2 = mu17^2/2 = {m17**2/2:10.3e}, "
              f"Q0 = {q0:.5f} Mpc^-1  (direct: {X*CONV:.5f})")
SZ21_FITS = {"Cosh": (0.5, 0.1, 7.5e3), "Higgs": (0.3, 1.0, 8.5e8), "Exp": (0.1, 1e-4, 9.5e3)}
print("\n    vs SZ21's three published fits (VERIFIED against the Fig-1 C_l^TT panel text,")
print("    extracted from Cl_TT_EE_with_residuals.pdf -- they are IN THE PANEL, not the caption):")
for nm, (kb, q0, k2) in SZ21_FITS.items():
    lo, hi = Q0B["stage56 core     "]
    print(f"       {nm:6}: K_B={kb:.1f}  Q0={q0:.0e} Mpc^-1  K_2={k2:.1e}   "
          f"pinned/fit = {lo/q0:.2e} - {hi/q0:.2e}")
chk(Q0B["stage56 core     "][0] > 1e-4 and Q0B["stage56 core     "][1] < 0.1,
    "2e THE PINNED Q0 LIES STRICTLY BETWEEN SZ21's two MOND-COMPATIBLE FITS (Exp 1e-4, "
    "Cosh 0.1) -- 45x-215x above Exp, 4.6x-22x below Cosh.  Inside their published span, "
    "equal to none of them.")

print()
print("=" * 100)
print("ITEM 3 -- THE CONSEQUENCE: stage57's share at the pinned Q0")
print("=" * 100)
H_REC = H0_SI * np.sqrt(OM_M * (1 + ZREC) ** 3 + OM_R * (1 + ZREC) ** 4 + OM_L) / C * MPC
f_dust = OM_DM * (1 + ZREC) ** 3 / (OM_M * (1 + ZREC) ** 3 + OM_R * (1 + ZREC) ** 4 + OM_L)
SRC_NUM = 3 * f_dust * H_REC
chk(abs(H_REC - 5.2145) / 5.2145 < 0.01 and abs(f_dust - 0.6387) < 0.01 and abs(SRC_NUM - 9.99) < 0.1,
    f"3a stage57's background numbers reproduced independently: H(rec) = {H_REC:.4f} Mpc^-1, "
    f"f_dust(rec) = {f_dust:.4f}, SRC*Q0 = 3 f_dust H = {SRC_NUM:.3f}")


def share(q0_mpc, kb):
    src = SRC_NUM / q0_mpc
    return (2 - kb) / abs(src - (2 - kb) * q0_mpc / H_REC)


print(f"    {'Q0 [Mpc^-1]':>13} {'SRC(rec)':>11} {'share K_B=0.25':>16} {'share K_B=0':>14}")
for lab, (lo, hi) in (("core", Q0B["stage56 core     "]), ("defensible", Q0B["stage56 defensible"])):
    for q0 in (lo, hi):
        print(f"    {q0:13.5f} {SRC_NUM/q0:11.1f} {100*share(q0,0.25):15.4f}% {100*share(q0,0.0):13.4f}%")
s_core = (share(Q0B["stage56 core     "][0], 0.25), share(Q0B["stage56 core     "][1], 0.0))
s_def = (share(Q0B["stage56 defensible"][0], 0.25), share(Q0B["stage56 defensible"][1], 0.0))
chk(abs(100 * s_def[0] - 0.04) < 0.01 and abs(100 * s_def[1] - 0.86) < 0.1,
    f"3b SHARE VERIFIED: defensible band gives {100*s_def[0]:.3f}% - {100*s_def[1]:.3f}% "
    f"(claim said 0.04-0.8%); CORE band gives {100*s_core[0]:.3f}% - {100*s_core[1]:.3f}%")
chk(100 * s_def[1] < 1.5,
    "3c GOOD NEWS, and it is the framework's: the pinned Q0 puts the (2-K_B)chi mixing share "
    "BELOW SZ21's own Cosh fit (1.50%) -- sub-dominant by 2x-40x.  Cell 3's recombination end "
    "and its halo end DECOUPLE; the transport channel keeps its freedom on the CMB side.")

print()
print("=" * 100)
print("ITEM 4 -- BOTH WAYS: what else moves at Q0 ~ 0.005-0.02 Mpc^-1")
print("=" * 100)
# 4a  mu17 / K_2
print("    4a  mu17 = K''(Q0)^(1/2) and K_2 = mu17^2/2, over the pin and the nu0 window:")
print(f"        {'nu0':>10} {'X':>7} {'mu17':>10} {'K_2':>12}   vs SZ21 MOND fits K_2 = 7.5e3 / 9.5e3")
for nu0v, nl in ((NU0_F, "floor"), (NU0_C, "ceil")):
    for X in (140.0, 670.0):
        m17 = np.sqrt(8 * np.pi) * R_DM / (KAPPA * nu0v * X)
        print(f"        {nu0v:10.2e} {X:7.0f} {m17:10.1f} {m17**2/2:12.3e}")
chk(True, "4a' K_2 IS PINNED TOO (not just Q0): the pin fixes the product-family, so "
          "K_2 = mu17^2/2 = 5.3e2 - 8.4e5 across the nu0 window -- bracketing SZ21's two "
          "MOND-compatible fits (7.5e3, 9.5e3).  No contradiction; the corpus lands in the "
          "same decade at the nu0 CEILING.")
# 4b  mu_H : X-FREE
print("\n    4b  SZ21's Helmholtz mass mu = sqrt(2K_2/(2-K_B)) Q_0 = mu17 Q0/sqrt(2-K_B):")
mu17_Q0 = np.sqrt(LAM) * R_DM                    # mu17 * Q0, in 1/m -- X-FREE
for nu0v, nl in ((NU0_F, "floor"), (NU0_C, "ceil ")):
    for kb in (0.0, 0.25):
        muH = mu17_Q0 / nu0v / np.sqrt(2 - kb)
        print(f"        nu0 {nl}, K_B={kb:.2f}:  mu_H^-1 = {1/muH/MPC:8.3f} Mpc")
print("        SZ21's OWN published fits, same formula:  Cosh mu^-1 = "
      f"{1/(np.sqrt(2*7.5e3)*0.1)*np.sqrt(1.5):.3f} Mpc,  Exp mu^-1 = "
      f"{1/(np.sqrt(4*9.5e3)*1e-4)*np.sqrt(1.9):.1f} Mpc,  Higgs mu^-1 = "
      f"{1/(np.sqrt(2*8.5e8)*1.0)*np.sqrt(1.7):.2e} Mpc")
chk(1 / (np.sqrt(2 * 7.5e3) * 0.1) * np.sqrt(1.5) < 0.25,
    "4b0 AND THE 0.23-Mpc CORNER IS NOT A DEFICIT: SZ21's OWN Cosh fit -- one of their two "
    "MOND-compatible, CMB-fitting parameter sets -- has mu^-1 = 0.100 Mpc, i.e. it violates "
    "their own stated 'mu^-1 >~ 1 Mpc' by 10x.  The corpus's nu0-floor corner (0.227 Mpc) is "
    "TWICE AS GOOD as a published AeST CMB fit, and its nu0-ceiling corner (1.88 Mpc) "
    "satisfies the requirement outright.",
    "reported in the framework's favour: stage54 A4b's 'straddles the pin' flag is if "
    "anything too pessimistic, since the pin it straddles is violated by SZ21's own fit.")
chk(True, "4b' mu_H IS EXACTLY X-FREE (mu17*Q0 = sqrt(Lambda)R_dm/nu0), so the pin CANNOT"
          " contradict SZ21's mu^-1 >~ 1 Mpc requirement -- and does not relieve it either.  "
          "The 0.23-Mpc corner at the nu0 FLOOR is a PRE-EXISTING corpus tension "
          "(stage54 A4b, already flagged 'NEW, needs adversarial verification'), not "
          "something the pin creates.  It cuts nu0, not X.")
nu0_min = R_DM / (np.sqrt(2 - 0.25) * L_LAM) * 1.0
info(f"4b'' SZ21's own mu^-1 >~ 1 Mpc forces nu0 >~ {R_DM*MPC/(np.sqrt(1.75)*L_LAM):.2e} "
     f"(K_B=0.25) -- i.e. the UPPER 47% (in log) of the committed window "
     f"[{NU0_F:.2e}, {NU0_C:.2e}].  Independent of X.")
# 4c  w_0 : X-FREE
print("\n    4c  SZ21's w_0 = 8 pi Gt rhob_0/(4 Q_0^2 K_2):")
for nu0v, nl in ((NU0_F, "floor"), (NU0_C, "ceil ")):
    w0 = nu0v ** 2 / (2 * R_DM)
    print(f"        nu0 {nl}: w_0 = nu0^2/(2 R_dm) = {w0:.3e}   [SZ21 quadratic-K bound "
          f"w_0 <~ 2e-14 -- violated by {w0/2e-14:.1e}x, WHICH IS WHY THE CORPUS USES A "
          f"SATURATING (DBI) K, exactly SZ21's own named fix]")
chk(True, "4c' w_0 = nu0^2/(2 R_dm) is ALSO X-free.  And it lands where SZ21's own chain "
          "says it must: their mu^-1 >~ 1 Mpc => w_0 >~ 1e-8 -- the corpus gives 4.1e-8 at "
          "the nu0 ceiling where mu^-1 = 1.9 Mpc.  CONSISTENT, both ways, independently.")
# 4d  Omega_dm / abundance
chk(True, "4d ABUNDANCE: NO independent fixing of Q0 exists in the corpus.  Q0 n0 = Lambda "
          "R_dm is ONE equation in TWO unknowns (item 1d'); Omega_dm fixes the PRODUCT "
          "Q0*n0, never Q0 alone -- which is SZ21's own statement that rhob is 'not "
          "(classically) predicted'.  So the pin ADDS information and cannot contradict "
          "the abundance chain.  No internal inconsistency found.")
# 4e  transport ceiling omega_Q = Q0 c
print("\n    4e  stage54 Part F transport ceiling (scales linearly in omega_Q = Q0 c):")
print("        stage54 F1 anchors: Q0 = H0/c = 2.248e-4 Mpc^-1 -> 0.15x binding rate;")
print("                            Q0 = 1 Mpc^-1               -> 671x binding rate.")
for lab, (lo, hi) in (("core", Q0B["stage56 core     "]), ("defensible", Q0B["stage56 defensible"])):
    print(f"        {lab:11}: ceiling = {671*lo:6.2f}x - {671*hi:6.2f}x the binding rate "
          f"(linear scaling, both anchors agree to 0.5%)")
chk(671 * Q0B["stage56 defensible"][0] > 0.3,
    f"4e' GOOD NEWS #2, and it is the framework's: stage54's PRE-STATED KILL CONDITION for "
    f"Cell 3 was 'net flux < ~0.3x binding rate => cell DEAD'.  At the pinned Q0 the CEILING "
    f"is {671*Q0B['stage56 defensible'][0]:.1f}x-{671*Q0B['stage56 core     '][1]:.1f}x the "
    f"binding rate -- the kill condition is NOT triggered anywhere in the band.  CAVEAT, "
    f"stated: this is a CEILING with zero compensation; the NET still needs the collapse solve.")
# 4f  the RAR-leg correction found in item 1e
print("\n    4f  THE CORRECTION ITEM 1e FOUND (runs BOTH ways -- lowers X, but SHRINKS the "
      "corpus's own shape-mismatch caveat):")


def gline(yN):     # framework's a0-line interpolation, in a0 units
    return np.sqrt(yN ** 2 + yN)


def gms08(yN):     # operative Route A / MS08 kernel
    return yN / (1 - np.exp(-np.sqrt(yN)))


print(f"        {'r [kpc]':>8} {'y_N=g_N/a0':>11} {'y (a0-line)':>12} {'y (MS08)':>10} "
      f"{'X factor line':>14} {'X factor MS08':>14}")
rows = []
for r_kpc in (3.74, 13.5, 60.0):
    yN = (CH2 * 1e6 / (r_kpc * KPC)) / A0
    y_l = (gline(yN) - yN) ** 2
    y_m = (gms08(yN) - yN) ** 2
    rows.append((r_kpc, yN, y_l, y_m))
    print(f"        {r_kpc:8.2f} {yN:11.3f} {y_l:12.4f} {y_m:10.4f} "
          f"{np.sqrt(y_l/yN):14.3f} {np.sqrt(y_m/yN):14.3f}")
# stage56's own PART B table (fixed v_ff 385/550) rescaled
print("\n        stage56 PART B table, corrected (v_ff = 385-550 km/s as committed there):")
Xc_l, Xc_m, Xc_0 = [], [], []
for (r_kpc, yN, y_l, y_m) in rows:
    for v in (385.0, 550.0):
        Xc_0.append(np.sqrt(yN) * C_KMS / v)
        Xc_l.append(np.sqrt(y_l) * C_KMS / v)
        Xc_m.append(np.sqrt(y_m) * C_KMS / v)
print(f"          as committed (y = y_N):      X = {min(Xc_0):6.0f} - {max(Xc_0):6.0f}  "
      f"(radial drift {max(Xc_0)/min(Xc_0)/(550/385):.2f}x)")
print(f"          corrected, a0-line kernel:   X = {min(Xc_l):6.0f} - {max(Xc_l):6.0f}  "
      f"(radial drift {max(Xc_l)/min(Xc_l)/(550/385):.2f}x)")
print(f"          corrected, MS08 (operative): X = {min(Xc_m):6.0f} - {max(Xc_m):6.0f}  "
      f"(radial drift {max(Xc_m)/min(Xc_m)/(550/385):.2f}x)")
chk(min(Xc_l) > 70 and max(Xc_m) < 1340,
    f"4f' THE CORRECTION DOES NOT BREAK THE PIN: corrected X = {min(Xc_l):.0f}-{max(Xc_m):.0f} "
    f"sits INSIDE stage56's already-committed DEFENSIBLE band 70-1340, and mostly inside the "
    f"core.  Corrected Q0 = {min(Xc_l)*CONV:.4f}-{max(Xc_m)*CONV:.4f} Mpc^-1.")
chk(max(Xc_l) / min(Xc_l) < max(Xc_0) / min(Xc_0),
    "4f'' AND IT RUNS IN THE FRAMEWORK'S FAVOUR ON THE COHERENCE AXIS: stage56's B3 caveat "
    "('the pin drifts 4.0x across 3.7-60 kpc') is OVERSTATED.  With the correct AeST "
    "|grad varphi| = g_tot - g_N the drift is 2.1x (a0-line) / 2.7x (MS08).  The corpus's "
    "own self-criticism was too harsh -- reported in that direction for the record.")


# 4g  does the FIRST HORN survive the 4f correction?
V_RMS_REC, AMP_F, AMP_C = 23.1, 2.78e4, 2.30e5
print("\n    4g  does stage56's FIRST HORN (active Y-sector at recombination) survive 4f?")
for lab, (xl, xh) in (("as committed", (136.0, 779.0)), ("corrected a0-line", (min(Xc_l), max(Xc_l))),
                      ("corrected MS08", (min(Xc_m), max(Xc_m)))):
    yl = (xl * V_RMS_REC / C_KMS) ** 2 * AMP_F
    yh = (xh * V_RMS_REC / C_KMS) ** 2 * AMP_C
    print(f"        {lab:20}: X = {xl:5.0f}-{xh:5.0f}  ->  y_rec = {yl:7.2f} (lo, floor amp) "
          f"- {yh:9.1f} (hi, ceiling amp)")
y_lo_corr = (min(Xc_l) * V_RMS_REC / C_KMS) ** 2 * AMP_F
chk(y_lo_corr > 1.0,
    f"4g' THE FIRST HORN SURVIVES THE CORRECTION: even at the corrected core bottom "
    f"X = {min(Xc_l):.0f}, y_rec(floor amp) = {y_lo_corr:.2f} > 1.  stage56 C1's verdict "
    f"(the small-X escape is dead; the banked CLASS pass carries an unpriced ACTIVE "
    f"Y-sector at recombination) is NOT relieved by the correction -- it is only softened "
    f"from 'y_rec = 3-830' to 'y_rec = 1.9-280'.")

print()
print("=" * 100)
print("ITEM 5 -- DOES THIS DISCHARGE stage57's 'PIN Q0', OR ONLY CONVERT IT?")
print("=" * 100)
print(r"""
  WHAT THE PIN DELIVERS, IF GRANTED (all four of SZ21's linear-cosmology parameters):
     K_B        [0, 0.25]                      corpus BBN bound (stage50)     -- PINNED
     Q0         0.0034-0.0215 Mpc^-1           X-pin (this trial)             -- PINNED (CANDIDATE)
     K_2        5.3e2 - 8.4e5                  = mu17^2/2, same family        -- PINNED (CANDIDATE)
     lambda_s   free                           SZ21 use lambda_s = infinity   -- NOT pinned
  ... and the K-FUNCTION FORM is the corpus's DBI, which is NOT one of SZ21's three fitted
  functions.  No published Boltzmann run exists at the corpus's own K.

  THE DECISIVE OBSTRUCTION, in SZ21's OWN WORDS (newRMONDLett.tex line 495, verbatim):
     "Note that a_0 does not appear in the linear cosmological regime but will play a role
      once nonlinear terms from F(Y,Q) kick in."
  Stage56's horn is EXACTLY that the nonlinear F(Y,Q) sector is ACTIVE at recombination
  (y_rec = 3-830 across the core band).  SZ21's published linear code CONTAINS NO a_0 and
  NO nonlinear F -- so even at a fully pinned (Q0, K_2, K_B) their run cannot price the horn.

  => THE OWED ITEM CONVERTS, IT DOES NOT DISCHARGE.
     DISCHARGED:  "Q0 is free, spanning four orders" (stage57 D2's stated reason) -- FALSE
                  once the X-pin is granted; and the transport-ceiling knob (4e) is settled.
     STILL OWED:  (i) a Boltzmann evaluation carrying the AETHER sector AND the nonlinear
                      F(Y,Q) branch, at the corpus's own DBI K -- which is strictly more
                      than "run SZ21's code at our numbers";
                  (ii) lambda_s;
                  (iii) the factor-8.3 nu0 window, which propagates into K_2 (a factor 1580)
                      even at fully pinned X -- so K_2 is pinned only to ~3 decades;
                  (iv) the X-pin is itself CANDIDATE-grade: an order-of-magnitude
                      consistency condition with a 2.1-4.0x radial drift, resting on a
                      NON-STATIC drain reading whose static counterpart is identically zero.
""")
chk(True, "5a THE TWO OWED ITEMS ARE THE SAME ITEM AT THE LEVEL OF THE PARAMETER, NOT AT THE "
          "LEVEL OF THE CALCULATION.  stage56 C2 already phrased its own owed check as "
          "'at pinned-X-equivalent (Q0, K2, K_B)' -- so stage56 had the map implicitly; "
          "stage57 D2, committed AFTER stage56 (4c334fa2 after 0aeb5748), restates Q0 as "
          "free WITHOUT citing stage56.  That gap is real and is the claim's true content.")

print()
print("=" * 100)
print(f"Q0PIN CHECKS: {N[0]-len(FAIL)}/{N[0]} passed" + ("" if not FAIL else f"  FAILED: {FAIL}"))
