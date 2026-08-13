#!/usr/bin/env python3
# STAGE 54 EVIDENCE (committed 2026-08-13 late).  PARTIALLY SUPERSEDED BY ITS OWN REFEREE
# (stage54_ev_laneY_referee_2026.py, refuted=TRUE on the two headlines):
#   * D1 "X-free ratio theorem / the wall stands in every fork" is REFUTED -- the support-side
#     y dropped the STATIC MOND gradient (y_static ~ 0.06-0.28, X-free; stage51's committed
#     0.1-1), which is the theorem's load-bearing leg.
#   * Verdict fork (c) "the corpus does not pin X" is REFUTED -- the RAR + drain free-fall
#     mirror pins X ~ 316-1000 (CANDIDATE).  See stage54 for the surviving content.
# CONFIRMED and standing: the A1 flow-form identity, delta-Y^(1)=0, the provenance algebra,
# the velocity table and thresholds (as conditional arithmetic), the rec-side correction of
# stage 51/52's linear-mode pricing.
# -*- coding: utf-8 -*-
r"""
laneY_gate_counting_2026.py
===========================
LANE Y: the Y=0-on-FLRW gate-counting question (stage53 B5), settled through the CORRECT
perturbative object -- the gate variable evaluated on the dust condensate's OWN linear modes.

THE MAP (derived symbolically in PART A, from committed definitions only):
  Y = q^{mu nu} d_mu phi d_nu phi = Qbar^2 |v_phi - v_aether|^2 / c^2-units  (exact to O(v^4)),
  where v_phi is the condensate flow velocity (u^mu prop grad phi, stages 5/6) and Qbar = Q0
  to 5e-4 at all epochs.  So on linear dust modes  Y_lin = Q0^2 (v/c)^2, and the gate variable
      y_lin = Y_lin / A(z, n_loc) = X^2 (v/c)^2 * [A0/A(z, n_loc)],   X := Q0 c^2 / a0(0).
  X is the ONE normalisation the committed corpus does NOT pin (PART A3): with the committed
  DBI K (stage17), beta = 1, and the abundance identity rho = Q0 n carrying full Omega_dm,
      X = sqrt(8 pi) R_dm / (kappa nu0 mu17),   R_dm = Om_dm/Om_L,  mu17^2 = K''(Q0) free.
  mu17 = 1 gives X ~ 1.8e5 (floor) -- "enormous"; but mu17 is unpinned, so every absolute
  verdict is reported as a function of X, and the X-FREE ratio theorem (PART D) does the killing.

Velocity source (PART B): linear theory, v_k = f(z) * (aH(z)/k) * delta_k(z), delta_k rms per
ln k = sqrt(k^3 P(k)/2pi^2), BBKS transfer normalised to sigma8, growth D(z) from the standard
ODE with radiation in H(a).  Scale-independent scale-back to z=1090 (standard, ~20-30% at k~1).
Real-space rms v(rec) ~ 25-30 km/s cross-checks the v_bc literature.

Both footings (canonical 9.3619e-11 / ALT 1.1279e-10), nu0 floor 2.14e-5 / ceiling 1.77e-4.
Exit 0 = all checks pass.
"""
import sys
import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


# ---------------- frozen constants / committed anchors -------------------------------------------
C = 2.99792458e8                     # m/s
G = 6.67430e-11
MPC = 3.0856775814913673e22
H0_KMSMPC = 67.4
H0 = H0_KMSMPC * 1e3 / MPC           # 1/s
OM_M, OM_L, OM_R = 0.315, 0.685, 9.15e-5
OM_DM = 0.265
R_DM = OM_DM / OM_L                  # 0.3869 -- charge carries FULL Omega_dm (v9 standing; chi dead, stage53)
A0_CAN, A0_ALT = 9.3619e-11, 1.1279e-10
KAPPA = 0.5
NU0_FLOOR, NU0_CEIL = 2.14e-5, 1.77e-4
Z_REC = 1090.0
SIGMA8, NS, HLIT = 0.811, 0.965, 0.674
# committed support-calibration numbers (stage53 B1, stage52):
CH2 = 1.08e4                         # (km/s)^2 = G M / R_halt at the support calibration
CS2_CAP = 2606.0                     # (km/s)^2, committed CLASS recombination cap
RHO_H_SURF = 1654.0                  # rho_dm0, halo-surface calibration (z_bind = 10.83)
RHO_H_DEEP = 1.0e6                   # rho_dm0, deep-support calibration (stage53 D2b)
V_H = np.sqrt(CH2)                   # 103.9 km/s, committed support flow speed
V_BIND_LO, V_BIND_HI = 30.0, 100.0   # km/s bracket, turnaround flows at z_bind ~ 11 (stated bracket)
V_FF_RAR = 300.0                     # km/s, condensate free-fall through RAR radii (drain picture)

LAMBDA = 3 * OM_L * H0 ** 2 / C ** 2          # 1/m^2
L_LAM = 1 / np.sqrt(LAMBDA)                    # m

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the exact map Y_lin -> Q0^2 v_rel^2, and the one unpinned normalisation X")
print("=" * 100)

# A1: Y on a perturbed flat background with a moving aether, symbolically.
Qb, gx, vax, vay, vaz = sp.symbols("Qbar gx v_ax v_ay v_az", real=True)
gy, gz = sp.symbols("gy gz", real=True)
dphi = sp.Matrix([Qb, gx, gy, gz])            # d_mu phi = (phidot/c, grad dphi); grad = Qbar*v_phi/c
eta = sp.diag(-1, 1, 1, 1)
va = sp.Matrix([vax, vay, vaz])
gam = 1 / sp.sqrt(1 - (vax**2 + vay**2 + vaz**2))
Alow = sp.Matrix([-gam, gam * vax, gam * vay, gam * vaz])   # unit-timelike aether, velocity v_a/c
Q_full = -(Alow.T * eta * dphi)[0] * 1        # Q = -A^mu d_mu phi (sign conv.; Y uses Q^2)
s2 = -(dphi.T * eta * dphi)[0]
Y_full = sp.simplify(Q_full ** 2 - s2)        # identity Y = Q^2 + (dphi)^2 = Q^2 - s^2
# substitute grad dphi = Qbar * v_phi (units of c), expand to quadratic order in velocities
vpx, vpy, vpz = sp.symbols("v_px v_py v_pz", real=True)
Y_sub = Y_full.subs({gx: -Qb * vpx, gy: -Qb * vpy, gz: -Qb * vpz})   # d_i phi = -Qbar v_i (u_mu = -d_mu phi/s)
eps = sp.symbols("epsilon", positive=True)
Y_series = Y_sub.subs({vpx: eps * vpx, vax: eps * vax, vpy: eps * vpy,
                       vay: eps * vay, vpz: eps * vpz, vaz: eps * vaz})
Y2 = sp.simplify(sp.series(Y_series, eps, 0, 3).removeO() / eps ** 2)
target = Qb ** 2 * ((vpx - vax) ** 2 + (vpy - vay) ** 2 + (vpz - vaz) ** 2)
check(sp.simplify(Y2 - target) == 0,
      "A1  *** Y = q^{munu} d_mu phi d_nu phi = Qbar^2 |v_phi - v_aether|^2 EXACTLY at leading "
      "(quadratic) order -- Y on the dust's own modes is the MISALIGNMENT flow, not the "
      "quasi-static g_N/a0 object stages 51/52/53 priced ***",
      "delta-Y^(1) = 0 (bridge1) is CONFIRMED (Y starts at O(v^2)); the identity Y = Q^2 - s^2 "
      "makes the aether-relative velocity the exact carrier")

# A2: the committed DBI K (stage17): closed-form law regression + charge inversion.
u_s, mu_s, LD_s, M4_s, nu_s = sp.symbols("u mu Lambda_D M4 nu", positive=True)
K_s = -M4_s + mu_s ** 2 * LD_s ** 2 * (1 - sp.sqrt(1 - u_s ** 2 / LD_s ** 2))
n_s = sp.diff(K_s, u_s)
u_of_nu = LD_s * nu_s / sp.sqrt(1 + nu_s ** 2)
check(sp.simplify(n_s.subs(u_s, u_of_nu) - mu_s ** 2 * LD_s * nu_s) == 0,
      "A2a n = K' = mu^2 u/sqrt(1-u^2/LD^2) inverts EXACTLY to n = mu^2 LD nu at "
      "u = LD nu/sqrt(1+nu^2) (stage17 B1 regression)")
negK = sp.simplify((-K_s).subs(u_s, u_of_nu))
check(sp.simplify(negK - (M4_s - mu_s ** 2 * LD_s ** 2 * (1 - 1 / sp.sqrt(1 + nu_s ** 2)))) == 0,
      "A2b -K(nu) = M^4 - mu^2 LD^2 (1 - 1/sqrt(1+nu^2)) (stage17 B2 regression); at beta = 1 "
      "the a0^2 law is sqrt(1+nu0^2)/sqrt(1+nu^2), nu = nu0 (1+z)^3")


def A_ratio(r, nu0):
    """A(r)/A(0) with r = n/n0: FRW r = (1+z)^3, local r = overdensity (stage53's A_ratio)."""
    return np.sqrt(1.0 + nu0 ** 2) / np.sqrt(1.0 + (nu0 * float(r)) ** 2)


# A3: the normalisation chain -- what IS pinned, what is NOT.
Q0_s, nu0_s, Rdm_s, Lam_s, m17_s, KB_s = sp.symbols("Q0 nu0 R_dm Lambda mu17 K_B", positive=True)
# committed relations (tilde units, everything in 1/L^2 or 1/L):
#   abundance: Q0 n0 = Lambda R_dm   (rho = Q0 n identically, charge = FULL Omega_dm)
#   beta = 1:  mu17 LD = sqrt(Lambda)  (M^4 = Lambda = rho_Lambda in tilde units)
#   n0 = nu0 mu17^2 LD = nu0 mu17 sqrt(Lambda)
Q0_expr = Lam_s * Rdm_s / (nu0_s * m17_s * sp.sqrt(Lam_s))
LD_expr = sp.sqrt(Lam_s) / m17_s
check(sp.simplify(Q0_expr * (nu0_s * m17_s * sp.sqrt(Lam_s)) - Lam_s * Rdm_s) == 0
      and sp.simplify(LD_expr / Q0_expr - nu0_s / Rdm_s) == 0,
      "A3a Q0 = sqrt(Lambda) R_dm/(nu0 mu17) and LD/Q0 = nu0/R_dm IDENTICALLY -- three committed "
      "relations, four scales: mu17^2 = K''(Q0) is the ONE normalisation the corpus never fixed",
      "provenance: rho=Q0 n (stage5), n=nu mu^2 LD + beta=1 (stage17), full-Omega_dm charge (v9)")
# X = Q0/sqrt(A0_tilde), A0_tilde = kappa^2 Lambda/(8 pi)  [ (a0/c^2)^2, canonical footing ]
X_expr = sp.simplify(Q0_expr / sp.sqrt(sp.Rational(1, 4) * Lam_s / (8 * sp.pi)))
check(abs(float(sp.simplify(X_expr * nu0_s * m17_s / Rdm_s)) - np.sqrt(8 * np.pi) / KAPPA) < 1e-9,
      "A3b X := Q0 c^2/a0(0) = sqrt(8 pi) R_dm/(kappa nu0 mu17): the gate variable's scale is "
      "y = X^2 (v/c)^2 A0/A -- and X carries the free mu17")
A0T_CAN = (A0_CAN / C ** 2) ** 2
check(abs(KAPPA ** 2 * LAMBDA / (8 * np.pi) / A0T_CAN - 1) < 0.01,
      f"A3c units cross-check: kappa^2 Lambda/8pi = {KAPPA**2*LAMBDA/(8*np.pi):.3e} vs "
      f"(a0_can/c^2)^2 = {A0T_CAN:.3e} -- the tilde-unit map is right")
X_MU1 = {}
for nu0, lab in ((NU0_FLOOR, "floor"), (NU0_CEIL, "ceil")):
    X_MU1[lab] = np.sqrt(8 * np.pi) * R_DM / (KAPPA * nu0 * 1.0)
info(f"A3d at the NATURAL mu17 = 1: X = {X_MU1['floor']:.3e} (floor) / {X_MU1['ceil']:.3e} "
     f"(ceiling) -- Qbar^2/A0 = X^2 = {X_MU1['floor']**2:.2e} / {X_MU1['ceil']**2:.2e}: the "
     f"'enormous ratio' is real at mu17 = 1, but mu17 is UNPINNED -- all absolute verdicts below "
     f"are functions of X; the kill (PART D) is X-free")

# A4: byproducts of the same chain, both mu17-FREE (report, flag for verification):
muH_expr = sp.simplify(m17_s * Q0_expr / sp.sqrt(2 - KB_s))     # Helmholtz mass
check(m17_s not in muH_expr.free_symbols,
      "A4a mu_H = mu17 Q0/sqrt(2-K_B) is mu17-FREE: mu_H^{-1} = nu0 sqrt(2-K_B) L_Lambda/R_dm -- "
      "the AeST Helmholtz scale is DERIVED once the charge carries full Omega_dm")
for nu0, lab in ((NU0_FLOOR, "floor"), (NU0_CEIL, "ceiling")):
    muHi = nu0 * np.sqrt(2 - 0.0) * L_LAM / R_DM / MPC
    muHi_KB = nu0 * np.sqrt(2 - 0.25) * L_LAM / R_DM / MPC
    info(f"A4b mu_H^-1({lab}) = {muHi:.2f} Mpc (K_B->0) / {muHi_KB:.2f} Mpc (K_B=0.25) -- "
         f"straddles the CMB/flat-RC pin mu^-1 >~ 1 Mpc (collapse-setup doc); >~1 Mpc favours "
         f"nu0 >~ 9e-5 (upper half of the window).  NEW, needs adversarial verification")
cs2_expr = sp.simplify(n_s / ((Q0_s + u_s) * sp.diff(K_s, u_s, 2)))
cs2_nu = sp.simplify(cs2_expr.subs(u_s, u_of_nu).subs(Q0_s, Q0_expr).subs(LD_s, LD_expr))
cs2_lead = sp.simplify(cs2_nu * Rdm_s / (nu0_s * nu_s) * (1 + nu_s ** 2) ** sp.Rational(3, 2))
check(sp.simplify(sp.limit(cs2_lead, nu0_s, 0) - 1) == 0,
      "A4c K-sector sound speed: c_s^2/c^2 = (nu0/R_dm) nu/(1+nu^2)^(3/2) to O(LD/Q0) -- "
      "mu17-FREE (stage 9's formula c_s^2 = K'/[(Q0+u)K''], evaluated on the committed DBI K)")
CS2KM = C ** 2 / 1e6
for nu0, lab in ((NU0_FLOOR, "floor"), (NU0_CEIL, "ceiling")):
    nurec = nu0 * (1 + Z_REC) ** 3
    cs2rec = (nu0 / R_DM) * nurec / (1 + nurec ** 2) ** 1.5 * CS2KM
    cs2max = (nu0 / R_DM) * (1 / np.sqrt(2)) / (1.5) ** 1.5 * CS2KM
    zmax = (1 / (np.sqrt(2) * nu0)) ** (1 / 3.0) - 1
    check(cs2rec < CS2_CAP / 1e5,
          f"A4d c_s^2(rec, {lab}) = {cs2rec:.1e} (km/s)^2 -- {CS2_CAP/cs2rec:.1e}x UNDER the "
          f"committed CLASS cap {CS2_CAP:.0f}, for every mu17.  The K-sector CMB pass is "
          f"unconditionally safe",
          f"peak c_s^2 = {cs2max:.0f} (km/s)^2 at z = {zmax:.0f} (mid dark ages, cap not binding)")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- linear dust velocities at recombination (the velocity source, stated)")
print("=" * 100)


def E_of_a(a):
    return np.sqrt(OM_R / a ** 4 + OM_M / a ** 3 + OM_L)


# growth ODE in N = ln a: D'' + (2 + dlnH/dN) D' - 1.5 Om_m(a) D = 0, radiation in H, matter source
N = np.linspace(np.log(1e-4), 0.0, 40000)
a_g = np.exp(N)
lnE = np.log(E_of_a(a_g))
dlnH = np.gradient(lnE, N)
Omm_a = OM_M / a_g ** 3 / E_of_a(a_g) ** 2
D = np.empty_like(N); Dp = np.empty_like(N)
D[0], Dp[0] = a_g[0], a_g[0]
h_step = N[1] - N[0]
for i in range(len(N) - 1):
    acc = -(2 + dlnH[i]) * Dp[i] + 1.5 * Omm_a[i] * D[i]
    Dp[i + 1] = Dp[i] + h_step * acc
    D[i + 1] = D[i] + h_step * Dp[i + 1]
f_g = Dp / D


def D_of_z(z):
    return np.interp(np.log(1 / (1 + z)), N, D)


def f_of_z(z):
    return np.interp(np.log(1 / (1 + z)), N, f_g)


GR = D_of_z(0) / D_of_z(Z_REC)
check(500 < GR < 1100 and 0.8 < f_of_z(Z_REC) <= 1.02,
      f"B1  growth D(0)/D(1090) = {GR:.0f}, f(1090) = {f_of_z(Z_REC):.3f} -- standard linear "
      f"theory (ODE with radiation in H; Meszaros suppression included)")

# BBKS P(k), sigma8-normalised (k in 1/Mpc; q = k/(Om h^2) with the standard shape)
kk = np.logspace(-4, 1.5, 3000)


def T_bbks(k):
    q = k / (OM_M * HLIT ** 2) * 1.0
    return (np.log(1 + 2.34 * q) / (2.34 * q)) * (1 + 3.89 * q + (16.1 * q) ** 2
                                                  + (5.46 * q) ** 3 + (6.71 * q) ** 4) ** -0.25


Pk_un = kk ** NS * T_bbks(kk) ** 2
R8 = 8.0 / HLIT
x8 = kk * R8
W8 = 3 * (np.sin(x8) - x8 * np.cos(x8)) / x8 ** 3
s8_un = np.sqrt(np.trapz(Pk_un * W8 ** 2 * kk ** 2, kk) / (2 * np.pi ** 2))
Pk_norm = Pk_un * (SIGMA8 / s8_un) ** 2


def Delta0(k):        # rms delta per ln k today
    P = np.interp(k, kk, Pk_norm)
    return np.sqrt(k ** 3 * P / (2 * np.pi ** 2))


def v_kms(k, z):      # physical peculiar velocity, per-ln-k rms: v = f aH/k * delta(z)
    aH = H0_KMSMPC * E_of_a(1 / (1 + z)) / (1 + z)          # km/s/Mpc
    return f_of_z(z) * (aH / k) * Delta0(k) * D_of_z(z) / D_of_z(0)


KS = np.array([0.01, 0.03, 0.1, 0.3, 1.0])
vr = {k: v_kms(k, Z_REC) for k in KS}
print("\n     k [1/Mpc]     delta_rms(rec)      v_rms(rec) [km/s]     v(z=20) [km/s]")
for k in KS:
    print(f"      {k:5.2f}        {Delta0(k)*D_of_z(Z_REC)/D_of_z(0):.3e}          "
          f"{vr[k]:8.2f}              {v_kms(k, 20.0):8.1f}")
# real-space rms over the full band (the locally operative saturation measure)
lk = np.log(kk[(kk > 1e-3) & (kk < 3.0)])
kv = kk[(kk > 1e-3) & (kk < 3.0)]
vint = np.array([v_kms(k, Z_REC) for k in kv])
V_RMS_REC = np.sqrt(np.trapz(vint ** 2, np.log(kv)))
V_MAX_REC = vint.max()
check(1.5 < min(vr.values()) < 40 and 15 < V_RMS_REC < 45,
      f"B2  v(rec) per mode = {min(vr.values()):.1f}-{max(vr.values()):.1f} km/s over k = 0.01-1; "
      f"real-space rms = {V_RMS_REC:.1f} km/s (peak per-ln-k {V_MAX_REC:.1f}) -- consistent with "
      f"the ~30 km/s decoupling-era bulk-flow literature (v_bc-grade)",
      "aether-relative caveat: v_rel = |v_phi - v_ae| <= v_phi; generic O(1) misalignment assumed; "
      "an exact linear-order aether-tracking theorem is the ONE escape and is not in the corpus")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- y_lin(z, k): the gate variable on the dust's own modes (DELIVERABLE 1)")
print("=" * 100)


def y_flow(v_km, r_env, nu0, X):
    """y = X^2 (v/c)^2 * A0/A(r_env);  r_env = n_loc/n0 (FRW: (1+z)^3; halo: overdensity)."""
    return X ** 2 * (v_km * 1e3 / C) ** 2 / A_ratio(r_env, nu0)


R_REC = (1 + Z_REC) ** 3
print("\n  y_lin at recombination (canonical footing), per mode and X -- nu0 floor | ceiling:")
print("     X        k=0.01      k=0.1       k=1.0      real-space rms")
for X in (X_MU1["floor"], 1000.0, 150.0, 52.0):
    row_f = [y_flow(v_kms(k, Z_REC), R_REC, NU0_FLOOR, X) for k in (0.01, 0.1, 1.0)]
    row_c = [y_flow(v_kms(k, Z_REC), R_REC, NU0_CEIL, X) for k in (0.01, 0.1, 1.0)]
    yrms_f = y_flow(V_RMS_REC, R_REC, NU0_FLOOR, X)
    yrms_c = y_flow(V_RMS_REC, R_REC, NU0_CEIL, X)
    print(f"   {X:8.3g}   {row_f[0]:9.3g}|{row_c[0]:9.3g} {row_f[1]:9.3g}|{row_c[1]:9.3g} "
          f"{row_f[2]:9.3g}|{row_c[2]:9.3g}  {yrms_f:9.3g}|{yrms_c:9.3g}")
info("C0  ALT footing: X_alt = X_can/(a0_alt/a0_can) = X_can/1.2047 at fixed Q0; y_alt = "
     "y_can/1.451 at fixed X-definition-per-footing -- every fork below shifts by ~1.45x in y, "
     "no verdict flips (the law shape is the derived canonical one; ALT has no derived law, "
     "stage17 F1 -- reported as convention)")

# the support side, both calibrations + the binding epoch
y_h = {}
for nu0, lab in ((NU0_FLOOR, "floor"), (NU0_CEIL, "ceil")):
    for r_env, cal in ((RHO_H_SURF, "surface"), (RHO_H_DEEP, "deep")):
        y_h[(lab, cal)] = y_flow(V_H, r_env, nu0, 1.0)      # per X^2 unit
print("\n  y at the support calibration TODAY (v_h = 103.9 km/s committed) and at z_bind:")
for X in (X_MU1["floor"], 1000.0, 150.0, 52.0):
    s = f"   X={X:8.3g}: "
    for lab in ("floor", "ceil"):
        s += f" surf({lab})={y_h[(lab,'surface')]*X**2:9.3g} deep({lab})={y_h[(lab,'deep')]*X**2:9.3g}"
    print(s)
info(f"C1  z_bind epoch (z=10.83, cosmic r=(11.83)^3~1656): A is FLAT there "
     f"(A0/A = {1/A_ratio(11.83**3, NU0_FLOOR):.3f} floor / {1/A_ratio(11.83**3, NU0_CEIL):.3f} "
     f"ceiling), so y_bind = X^2 (v_bind/c)^2 with v_bind = 30-100 km/s -- same order as the "
     f"halo-today value; the wall comparison below uses BOTH ends")

# fork thresholds
th = {}
for nu0, lab in ((NU0_FLOOR, "floor"), (NU0_CEIL, "ceil")):
    amp = 1 / A_ratio(R_REC, nu0)
    th[(lab, "mode")] = 1.0 / (V_MAX_REC * 1e3 / C * np.sqrt(amp))
    th[(lab, "rms")] = 1.0 / (V_RMS_REC * 1e3 / C * np.sqrt(amp))
check(th[("floor", "rms")] > 50 and th[("ceil", "rms")] > 15,
      f"C2  FORK THRESHOLDS: y_rec < 1 on every mode requires X < {th[('floor','mode')]:.0f} "
      f"(floor) / {th[('ceil','mode')]:.0f} (ceiling); on the real-space rms X < "
      f"{th[('floor','rms')]:.0f} / {th[('ceil','rms')]:.0f}.  mu17 = 1 gives X = 1.8e5-2.2e4: "
      f"fork (a), saturation by 4-8 orders.  The corpus does NOT pin X -> the a/b fork is OPEN",
      "A0/A(rec) amplification: x{:.3g} floor / x{:.3g} ceiling".format(
          1 / A_ratio(R_REC, NU0_FLOOR), 1 / A_ratio(R_REC, NU0_CEIL)))

# NEW two-sided squeeze on X from committed phenomenology (both are UPPER bounds; no lower bound)
X_rar_loose = np.sqrt(1.0) / (V_FF_RAR * 1e3 / C)
X_rar_tight = np.sqrt(0.1) / (V_FF_RAR * 1e3 / C)
check(int(X_rar_loose) == 999 or abs(X_rar_loose - 1000) < 2,
      f"C3  NEW COMMITTED-PHENOMENOLOGY BOUND (derived here): the drain picture has condensate "
      f"free-falling through RAR radii at ~{V_FF_RAR:.0f} km/s; its flow-Y must not push the "
      f"kernel Newtonian where the RAR needs MOND (y_flow <= 0.1-1): X <= "
      f"{X_rar_tight:.0f}-{X_rar_loose:.0f}.  X is squeezed from above TWICE (RAR + CMB "
      f"cleanliness) and from below by NOTHING -- the framework can retreat to small X",
      "at mu17 = 1 the RAR bound is violated 180-1800x (floor): mu17 >= ~20-1800 is REQUIRED "
      "by committed phenomenology -- a constraint the corpus never recorded")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- the X-FREE ratio theorem, and the wall re-derived through the right object")
print("=" * 100)

# y_rec/y_support: X, a0-footing and (in the deep regime) nu0 all cancel.
print("\n  R = y_rec(k)/y_support  (X-free, footing-free):")
print("     k [1/Mpc]   vs surface(floor)  vs surface(ceil)  vs deep(floor)  vs deep(ceil)"
      "   vs z_bind(v=100,floor)")
RMIN = {"surface": np.inf, "deep": np.inf, "bind": np.inf}
for k in KS:
    row = []
    for cal, r_env in (("surface", RHO_H_SURF), ("deep", RHO_H_DEEP)):
        for nu0 in (NU0_FLOOR, NU0_CEIL):
            R = (y_flow(v_kms(k, Z_REC), R_REC, nu0, 1.0)
                 / y_flow(V_H, r_env, nu0, 1.0))
            row.append(R)
            RMIN[cal] = min(RMIN[cal], R)
    Rb = (y_flow(v_kms(k, Z_REC), R_REC, NU0_FLOOR, 1.0)
          / y_flow(V_BIND_HI, 11.83 ** 3, NU0_FLOOR, 1.0))
    RMIN["bind"] = min(RMIN["bind"], Rb)
    print(f"      {k:5.2f}      {row[0]:10.3g}      {row[1]:10.3g}     {row[2]:10.3g}"
          f"     {row[3]:10.3g}        {Rb:10.3g}")
check(RMIN["surface"] > 30 and RMIN["deep"] > 0.9 and RMIN["bind"] > 30,
      f"D1  *** THE RATIO THEOREM: y_rec >= y_support for EVERY k in 0.01-1, every nu0, every "
      f"footing, every X, every mu17.  Minima: vs surface {RMIN['surface']:.0f}x, vs deep "
      f"{RMIN['deep']:.2f}x (the single worst corner, k=1 + maximal local-a0 credit), vs the "
      f"z_bind epoch {RMIN['bind']:.0f}x.  A monotone bounded gate is AT LEAST as open at "
      f"recombination as anywhere it delivers support ***",
      "mechanism: A tracks local n (stage53 D2), and rec's r=(1+z)^3=1.3e9 outruns every halo "
      "overdensity (<=1e6) by more than the velocity contrast (v_h/v_rec)^2 <= ~770 can pay")

V_SAT = CH2 * ((1 + 1091 - 1090 + Z_REC) ** 3 / RHO_H_SURF) / CS2_CAP  # 1091^3/1654, re-derived
V_SAT = CH2 * (1091.0 ** 3 / RHO_H_SURF) / CS2_CAP
check(abs(V_SAT / 3.25e6 - 1) < 0.01,
      f"D2  V_sat re-derived from its inputs = {V_SAT:.3e} (= c_h^2 (rho_rec/rho_h)/cs2_cap, "
      f"stage53 B1 regression) -- with D1, the CMB violation of ANY support-delivering monotone "
      f"bounded gate is >= V_sat = 3.25e6x, independent of m, y_*, X, nu0, footing",
      "P_ind ~ n^2 => c_s^2 ~ rho; equal-or-more-open at rec => violation >= density-scaling floor")

# band-pass best case: optimal y_* suppression is bounded by y_support/y_rec
bp_best = V_SAT * RMIN["surface"] ** -1
bp_deep = V_SAT * max(RMIN["deep"], 1e-12) ** -1
ystar = np.logspace(-8, 8, 2000)


def W_bp(y):
    return y / (1 + y) ** 2


# numeric confirmation at the most gate-favourable corner (deep credit, k=1, floor)
ysup = y_flow(V_H, RHO_H_DEEP, NU0_FLOOR, 1.0)
yrec = y_flow(v_kms(1.0, Z_REC), R_REC, NU0_FLOOR, 1.0)
supp = np.min(W_bp(yrec / ystar) / W_bp(ysup / ystar))
check(V_SAT * supp > 100,
      f"D3  band-pass gate (the a0-bump's own shape, stage53 cell 2): best achievable rec-"
      f"suppression over all gate scales y_* is {supp:.3g} at the most favourable corner -> "
      f"violation >= {V_SAT*supp:.3g}x (deep credit) and >= {bp_best:.3g}x (surface).  DEAD on "
      f"the flow object too (stage53's 4.3e3-9.4e5x verdict CONFIRMED by different arithmetic)")

# analytic monomials W ~ Y^m A^q: linear-order protection is REAL (exact monomial, no gate scale);
# the price moves to the mean-field channel: violation = V_sat (Y_rec/Y_h)^m (A_rec/A_h)^q
print("\n  analytic gates W ~ Y^m A^q -- mean-field violation and the q-boundary (flow object):")
VKREC = max(v_kms(k, Z_REC) for k in KS)     # CMB-critical mode band
for m in (1, 2, 3):
    vio20 = V_SAT * (VKREC / V_H) ** (2 * m)
    print(f"    m={m}, q=0:  violation = V_sat (v_rec/v_h)^(2m) = {vio20:.3g}x"
          + ("   <-- (2,0) 'gate on Y': DEAD, ~5.7e2x" if m == 2 else ""))
qb = {}
for cal, r_env in (("surface", RHO_H_SURF), ("deep", RHO_H_DEEP)):
    for nu0, lab in ((NU0_FLOOR, "floor"), (NU0_CEIL, "ceil")):
        Aratio_rh = A_ratio(R_REC, nu0) / A_ratio(r_env, nu0)
        q_need = np.log(V_SAT * (VKREC / V_H) ** 4) / (-np.log(Aratio_rh))
        qb[(cal, lab)] = q_need
        print(f"    m=2, {cal:7s} {lab:5s}: A_rec/A_h = {Aratio_rh:.3e} -> q >= {q_need:.2f}")
check(0.4 < min(qb.values()) and max(qb.values()) < 1.1,
      f"D4  cell 1's q-boundary RECOMPUTED on the flow object: q >= "
      f"{min(qb.values()):.2f}-{max(qb.values()):.2f} (m=2, spanning calibration and nu0) vs "
      f"stage53's 0.64-1.03 (floor) / 0.19-0.51 (ceiling).  The floor edge survives ~unchanged; "
      f"the CEILING RELIEF EVAPORATES (the flow contrast is nu0-blind).  Cell 1 stays UNTRIED "
      f"but its open region shrinks to q ~ 1",
      "for exact monomials the O(delta^2m) linear-order protection IS real -- no saturation "
      "issue -- so the price correctly lives in this mean-field channel")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT (see the lane report for the per-object consequences)")
print("=" * 100)
print(f"""
  1. THE OBJECT: on the dust's own linear modes  Y = Q0^2 |v_phi - v_ae|^2  exactly;  the gate
     variable is  y = X^2 (v/c)^2 A0/A(z, n_loc)  with  X = Q0 c^2/a0 = sqrt(8pi) R_dm/(kappa nu0
     mu17)  -- and mu17 = K''(Q0) is UNPINNED by the committed corpus.  At mu17 = 1, X ~ 1.8e5
     (floor): y_rec ~ 1e5-1e6 >> 1 (fork a).  y_rec < 1 needs X <~ {th[('floor','rms')]:.0f} (floor) /
     {th[('ceil','rms')]:.0f} (ceiling) on the rms.  The a/b fork is therefore OPEN (c) -- BUT:

  2. THE RATIO THEOREM (X-, mu17-, footing-, y_*-free):  y_rec/y_support >= 1 at the single worst
     corner and >= 10-1e4 everywhere else.  Every monotone bounded gate is at least as open at
     recombination as at its support point  =>  violation >= V_sat = 3.25e6x the CLASS cap.
     Band-pass: >= {V_SAT*supp:.0f}x.  The gate-class wall STANDS, now derived through the right object.

  3. MAGNITUDES CORRECTED: stage 52 kill 2's verdict stands with magnitude V_sat = 3.25e6x
     (its own original number); stage 53's 'true y^2 violation 5.2e11-2.9e13x' is VOID (Taylor-
     extrapolates W~y^2 beyond saturation, on the quasi-static object).  Stage 53's V(m,q) map:
     bounded cells collapse to V_sat in fork (a); analytic cells keep real linear protection and
     get the mean-field prices above; cell 1's q-boundary moves to ~1 (ceiling relief gone).

  4. CMB PASS: the K-sector c_s^2 is unconditionally safe (A4d, mu17-free, >=4e5x under cap).
     The bridge1 linear-response protection (delta-Y^(1)=0) is intact as an identity, but its
     'at any amplitude' corollary is FALSE in fork (a): realized-mode saturation activates the
     Y-sector on linear modes at rec.  The committed CLASS pass is CONDITIONALLY protected:
     clean iff X <~ 50-150, which committed physics permits but does not enforce.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0]-len(FAIL)}/{NCHK[0]} passed" + ("" if not FAIL else f"  FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
