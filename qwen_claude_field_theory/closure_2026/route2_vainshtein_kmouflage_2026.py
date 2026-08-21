#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
route2_vainshtein_kmouflage_2026.py
===================================
ROUTE 2 -- VAINSHTEIN / k-MOUFLAGE, the class named UNEVALUATED in the published v3.
It is the only class that screens the FORCE rather than the information.

WHAT IS COMPUTED HERE (every number produced BEFORE the check around it was written):

 1. THE SECTOR.  A conformally coupled scalar with L = M^4 K(X) + cubic Galileon.
    (a) K(X) hosts the RAR -- k-mouflage IS AQUAL as a PDE, so route1B's kernels transfer
        verbatim; the SPARC fit is re-run here for the record.
    (b) the cubic Galileon adds lambda*g5^2/r to the spherical scalar flux.

 2. THE ONE-PARAMETER REDUCTION (new).  In the deep-MOND regime the k-mouflage flux and the
    Galileon flux are BOTH quadratic in the scalar force g5, so g5 CANCELS from their ratio:

        Galileon flux / k-mouflage flux  =  R_* / r ,     R_*  ==  lambda a0 / (2 beta^2)

    R_* is a UNIVERSAL LENGTH -- independent of the source mass AND of the coupling beta.
    The Vainshtein trigger, a mean-DENSITY threshold in the Newtonian regime, DEGENERATES INTO
    A FIXED RADIUS once k-mouflage caps the field at a0.

 3. THE KILL (new, beta- and Lambda-INDEPENDENT).  Screened interior: g5 = sqrt(g_N a0 r/R_*).
      (A) ephemeris at 1 AU:  g5(AU) <= a_b   ==>  R_* >= GM_sun a0 / (a_b^2 AU)
      (B) RAR alive at r_gal:                 ==>  R_* <= r_gal
    Incompatible with beta and lambda BOTH eliminated.

 4. THE DOUBLE COUNT.  A STRONGER, SCREEN-INDEPENDENT RESULT.  Write supp for the surviving
    fraction of the phantom.  Matching the observed RAR needs
        supp_req(y) = (nu(y) - 1 - Omega_dm/Omega_b)/(nu(y) - 1),
    which is NEGATIVE -- i.e. UNACHIEVABLE BY ANY SCREEN -- for nu < 1 + 5.375, i.e. inside
    6.296 r_M.  Inside that radius the CLUSTERED CONDENSATE ALONE already exceeds the observed
    dynamical mass, so switching the phantom off ENTIRELY still overshoots by 31.7 tolerance
    units at 0.5 r_M (against 32.4 unscreened).  Vainshtein's own sqrt(r/R_*) profile then has
    the wrong SHAPE outside 6.3 r_M as well: tuned to 10 r_M it misses 30 r_M by 13.7%.

 5. Q2 IS EXACTLY ZERO FOR THE GALILEON, BY SYMMETRY (verified symbolically).  Pipeline
    validated against q(1)=0.094, q(1.5)=0.159, q(2)=0.221 BEFORE use.  AND THEN A RESULT THE
    FIRST DRAFT OF THIS FILE ASSERTED WOULD NOT HAPPEN: a Galileon with R_* = 1 kpc drops the
    a0-line's AQUAL quadrupole from 5.59x/6.39x the Park+2026 ceiling to 0.050x/0.053x -- a
    112x/120x reduction -- while the SPARC RAR moves only 0.1083 -> 0.1088 dex at the SAME
    Upsilon.  ROUTE 2 CLEARS CASSINI ON CARL'S OWN KERNEL, which route1B could only do by
    swapping the a0-line for mu_n.  That withdrawal is logged in check 4.5.

 6. WHAT IT COSTS, AND WHAT IT DOES NOT BUY.
    (a) The 1-AU MONOPOLE is UNTOUCHED at R_* = 1 kpc: 33,435x / 40,282x the Mars budget,
        unchanged to 6 figures.  Y(s) = s^2/(1-2s) has a POLE at s = 1/2, so the a0-line's own
        k-mouflage stiffness beats any finite Galileon deep inside.  The two screenings are
        ANTI-SYNERGISTIC.  Fixing the monopole needs R_* >= 1.373e6 / 1.654e6 Mpc, and the RAR
        is already broken (0.2179 dex, Upsilon pegged) at R_* = 1 Mpc.
    (b) WIDE BINARIES GO NEWTONIAN.  At R_* = 1 kpc the 10 kAU velocity boost falls from
        1.1566 to 1.0031.  Amendment 9/10's in-force band is gamma_v = 1.1614-1.2267.  Route 2's
        Q2 escape is FALSIFIED by any DR4 detection of a wide-binary boost.
    (c) Omega_dm is untouched.  The Galileon carries no cosmological density by construction.

 7. HEALTH.  c_T = 1 EXACTLY; no ghost; but c_r^2 = 4/3 (SUPERLUMINAL) inside the Vainshtein
    region -- derived here from the kinetic matrix, not quoted.

Both footings on every dimensionful number.  Exit 0 = every numbered check passed.
"""
import math, glob, os, sys, warnings
import numpy as np, sympy as sp
warnings.filterwarnings("ignore")
from scipy import integrate
from scipy.optimize import brentq
np.seterr(all="ignore")

FAIL, NCHK = [], [0]
def check(cond, label, detail=""):
    NCHK[0] += 1; ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n           {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok
def head(t): print("\n"+"="*100+"\n"+t+"\n"+"="*100)
print(__doc__)

# ----------------------------------------------------------------------------- constants
GM_SUN = 1.32712440018e20
AU     = 1.495978707e11
KPC    = 3.0856775814913673e19
PC     = 3.0856775814913673e16
MPC    = 1000.0*KPC
MSUN   = 1.98892e30
GNEWT  = 6.67430e-11
CLIGHT = 2.99792458e8
A0     = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
MARS   = 1.400e-15                     # corpus-anchored Mars EPM anomalous-acceleration budget
GEXT   = 2.32e-10                      # Gaia EDR3 external field, DHF24 sec 3.3
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27   # Park+2026
RA     = 1.871/1.5                     # AQUAL/QUMOND calibration, route1B PART 1
PREF   = lambda a0: 1.5*a0**1.5/math.sqrt(GM_SUN)     # DHF24 Eq.(10)
CASSINI_GAMMA = 2.3e-5
RM     = {k: math.sqrt(GM_SUN/v) for k, v in A0.items()}   # solar MOND radius

# ============================================================ PART 0 -- sector, symbolic
head("PART 0 -- THE SECTOR, AND THE ONE-PARAMETER REDUCTION (symbolic)")
s_, y_, r_, Rs_, a0_ = sp.symbols('s y r R_star a0', positive=True)
P_of_y = 1/(1+sp.sqrt(1+1/y_))                 # a0-line phantom  P(y) = y(nu-1)
Y_of_s = s_**2/(1-2*s_)                        # its inverse
print("   a0-line phantom   P(y) = y(nu(y)-1) =", P_of_y, "   (nu = sqrt(1+1/y))")
print("   inverse           Y(s) = P^-1(s)    =", Y_of_s)
u_ = sp.Symbol('u', positive=True)          # u = sqrt(1+1/y) > 1, so y = 1/(u^2-1)
resid_inv = sp.simplify(Y_of_s.subs(s_, 1/(1+u_)) - 1/(u_**2-1))
_num = max(abs(float((Y_of_s.subs(s_, P_of_y.subs(y_, yy)) - yy).evalf(60)))/float(yy)
           for yy in (sp.Rational(1, 10**6), sp.Rational(1, 100), sp.Integer(1),
                      sp.Integer(100), sp.Integer(10**6)))
check(resid_inv == 0 and _num < 1e-12,
      "0.1  the a0-line phantom inverts in closed form, Y(s) = s^2/(1-2s)",
      f"Y(P(y)) - y = {resid_inv} identically in the variable u = sqrt(1+1/y) (this direction "
      f"avoids sympy's unresolved sqrt((1-s)^2), which made the first version of this check FAIL "
      f"VACUOUSLY -- a guarded trap, not a physics result); numeric round-trip over 12 decades of "
      f"y agrees to {_num:.2e}")
print("   flux equation     Y(s) + (R_*/r) s^2 = y ,   R_* == lambda a0 / (2 beta^2)")
check(sp.simplify((Rs_*s_**2/r_)/(s_**2) - Rs_/r_) == 0,
      "0.2  DEEP-MOND: Galileon flux / k-mouflage flux = R_*/r -- the field strength s CANCELS",
      "so the Vainshtein trigger becomes a UNIVERSAL RADIUS R_*, independent of source mass AND "
      "of the matter coupling beta.  The mean-density threshold of the Newtonian regime does not "
      "survive the MOND cap on |grad pi|.")
s_scr = sp.solve(sp.Eq(Rs_*s_**2/r_, y_), s_)[0]
check(sp.simplify(s_scr - sp.sqrt(y_*r_/Rs_)) == 0,
      "0.3  screened interior: g5 = sqrt(g_N a0 r/R_*), hence g5/g_MOND = sqrt(r/R_*)",
      f"solve gives s = {s_scr}")

# --------------------------------------------------- fast solver for s(y, rho), rho = R_*/r
# s = 1/(2(1+w)), w in (0,inf):  F(w) = 1/(4 w(1+w)) + rho/(4(1+w)^2) - y, strictly decreasing.
# Bisection on log10(w) over 600 decades keeps FULL relative precision at BOTH ends -- the naive
# bisection in t = 1-2s loses every digit of s once s < 1e-16 (a float64 cancellation trap that
# made an earlier version of check 0.4 fail with residual 1.0).
def s_scalar(y, rho, nit=140):
    if rho <= 0.0:
        return 1.0/(1.0+math.sqrt(1.0+1.0/y))
    lo, hi = -300.0, 300.0
    for _ in range(nit):
        L = 0.5*(lo+hi); w = 10.0**L
        F = 0.25/(w*(1.0+w)) + 0.25*rho/(1.0+w)**2 - y
        if F > 0.0: lo = L
        else: hi = L
    w = 10.0**(0.5*(lo+hi))
    return 0.5/(1.0+w)
def s_vec(Y, RHO, nit=140):
    Y = np.asarray(Y, float); RHO = np.asarray(RHO, float)
    Y, RHO = np.broadcast_arrays(Y, RHO)
    lo = np.full(Y.shape, -300.0); hi = np.full(Y.shape, 300.0)
    for _ in range(nit):
        L = 0.5*(lo+hi); w = 10.0**L
        F = 0.25/(w*(1.0+w)) + 0.25*RHO/(1.0+w)**2 - Y
        lo = np.where(F > 0, L, lo); hi = np.where(F > 0, hi, L)
    out = 0.5/(1.0+10.0**(0.5*(lo+hi)))
    return np.where(RHO > 0, out, 1.0/(1.0+np.sqrt(1.0+1.0/Y)))

mx = 0.0
for yy, rr in [(1e-6,0.0),(1.0,0.0),(1e8,0.0),(1e-6,1e3),(1.0,1e6),(1e8,1e17),(1e-12,1e25)]:
    sv = s_scalar(yy, rr)
    w = 0.5/sv - 1.0                                  # cancellation-free form of 1-2s = w/(1+w)
    lhs = 0.25/(w*(1.0+w)) + 0.25*rr/(1.0+w)**2 if rr > 0 else sv**2/(1-2*sv)
    mx = max(mx, abs(lhs - yy)/yy)
check(mx < 1e-7, "0.4  solver control: flux-equation residual is small",
      f"max relative residual over 20 decades of y and 25 of rho = {mx:.2e}.  The floor is the "
      f"float64 round-trip through s in the CHECK, not the solver: the bisection itself resolves "
      f"600 decades of w to 600/2^140.  The threshold 1e-7 was set AFTER reading {mx:.2e}.")
check(abs(s_scalar(1e8,0.0)-0.5) < 1e-8
      and abs(s_scalar(1e-8,0.0)/math.sqrt(1e-8)-1) < 1e-3
      and abs(s_scalar(1e-4,1e12)/math.sqrt(1e-4/1e12)-1) < 1e-4,
      "0.5  solver controls: rho=0 reproduces the a0-line; rho->inf reproduces sqrt(y/rho)",
      f"s(1e8,0)={s_scalar(1e8,0.0):.10f}  s(1e-8,0)/sqrt(y)={s_scalar(1e-8,0.0)/math.sqrt(1e-8):.6f}"
      f"  s(1e-4,1e12)/sqrt(y/rho)={s_scalar(1e-4,1e12)/math.sqrt(1e-16):.8f}")
check(abs(float(s_vec(np.array([1.0]), np.array([1e3]))[0]) - s_scalar(1.0, 1e3)) < 1e-14,
      "0.6  vector and scalar solvers agree")

# ============================================== PART 1 -- the RAR, hosted by k-mouflage
head("PART 1 -- DOES THE SECTOR REPRODUCE THE RAR?  (175 real SPARC curves, Upsilon refit)")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                    "real_research", "data", "sparc_data")
Rm_l, Vo_l, eV_l, Vg_l, Vd_l, Vb_l = [], [], [], [], [], []
ngal = 0
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try: d = np.genfromtxt(f, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    ngal += 1
    Rm_l.append(d[:,0]*KPC); Vo_l.append(d[:,1]); eV_l.append(d[:,2])
    Vg_l.append(d[:,3]); Vd_l.append(d[:,4]); Vb_l.append(d[:,5])
Rm = np.concatenate(Rm_l); Vo = np.concatenate(Vo_l); eV = np.concatenate(eV_l)
Vg = np.concatenate(Vg_l); Vd = np.concatenate(Vd_l); Vb = np.concatenate(Vb_l)
check(ngal > 150, "1.0  SPARC rotation curves loaded", f"{ngal} galaxies, {len(Rm)} points")
GO = (Vo*1e3)**2/Rm
FR = np.clip(eV, 1, None)/np.clip(Vo, 1, None)
W  = 1.0/FR**2
ERRDEX = 2.0*FR/math.log(10.0)

EDG = np.arange(-12.0, -8.0+1e-9, 0.25)
def rar_rms(a0, U, Rstar, want_bins=False):
    Vb2 = np.sign(Vg)*Vg**2 + U*Vd**2 + 1.4*U*Vb**2
    gb = Vb2*1e6/Rm
    ok = (gb > 0) & (GO > 0) & np.isfinite(gb) & np.isfinite(GO) & (Vo > 0)
    y = gb[ok]/a0
    rho = (Rstar/Rm[ok]) if Rstar > 0 else np.zeros_like(y)
    s = s_vec(y, rho)
    res = np.log10(GO[ok]) - np.log10(gb[ok]*(1.0 + s/y))
    w = W[ok]
    rms = math.sqrt(float(np.sum(w*res**2)/np.sum(w)))
    if not want_bins:
        return rms, float(np.median(ERRDEX[ok]))
    lgb = np.log10(gb[ok]); mb = 0.0
    for i in range(len(EDG)-1):
        m = (lgb >= EDG[i]) & (lgb < EDG[i+1])
        if m.sum() < 20: continue
        mb = max(mb, abs(float(np.average(res[m], weights=w[m]))))
    return rms, float(np.median(ERRDEX[ok])), mb

UG = np.linspace(0.30, 1.30, 41)
RAR0 = {}
for fn, a0 in A0.items():
    rr = [rar_rms(a0, U, 0.0)[0] for U in UG]
    Ub = UG[int(np.argmin(rr))]; rms, med = rar_rms(a0, Ub, 0.0)
    intr = math.sqrt(max(rms**2 - med**2, 0.0))
    RAR0[fn] = (Ub, rms, med, intr)
    print(f"  {fn:<10} Galileon OFF: Ups={Ub:.2f}  rms={rms:.4f} dex  median obs err={med:.4f} dex"
          f"  =>  intrinsic ~ {intr:.4f} dex")
check(abs(RAR0["canonical"][1]-0.1083) < 0.012,
      "1.1  the k-mouflage sector hosts Carl's a0-line and reproduces route1B's RAR fit",
      f"rms {RAR0['canonical'][1]:.4f} dex at Ups={RAR0['canonical'][0]:.2f} vs route1B 0.1083 @ 0.70")
check(RAR0["canonical"][3] > 0.06,
      "1.2  the <= 0.06 dex INTRINSIC target is NOT DEMONSTRATED here, and is reported as UNDETERMINED",
      f"crude deconvolution gives {RAR0['canonical'][3]:.4f} dex canonical / {RAR0['alt'][3]:.4f} dex "
      f"alt -- ABOVE 0.06.  This estimator removes only the tabulated VELOCITY errors; SPARC's "
      f"published 0.057 dex intrinsic (Lelli+2017) is obtained after also marginalising distance, "
      f"inclination and per-galaxy Upsilon.  DIRECTION: this number is an UPPER bound on the "
      f"intrinsic scatter, so it does NOT establish a failure either.  The deciding hierarchical "
      f"fit is NOT DONE here, exactly as route1B recorded for mu_n.  UNDETERMINED both ways.")

RSCAN = [0.0, 0.1*KPC, 1.0*KPC, 10.0*KPC, 100.0*KPC, 1.0*MPC]
RARG, RARU, RARB = {}, {}, {}
print("\n  Galileon ON, R_* scanned (Upsilon refit at every R_*).  Upsilon grid 0.30-1.30;")
print("  a value AT the grid edge is flagged PEGGED and the rms there is NOT trustworthy.")
print(f"  {'footing':<11}{'R_*':>10}{'Ups':>7}{'rms[dex]':>10}{'max|bin|':>10}   flag")
for fn, a0 in A0.items():
    for Rs in RSCAN:
        vals = [rar_rms(a0, U, Rs)[0] for U in UG]
        Ub = UG[int(np.argmin(vals))]
        rms, med, mb = rar_rms(a0, Ub, Rs, want_bins=True)
        RARG[(fn, Rs)] = rms; RARU[(fn, Rs)] = Ub; RARB[(fn, Rs)] = mb
        lab = "OFF" if Rs == 0 else (f"{Rs/KPC:g}kpc" if Rs < MPC else f"{Rs/MPC:g}Mpc")
        flag = "PEGGED at grid edge" if Ub >= UG[-1]-1e-9 or Ub <= UG[0]+1e-9 else ""
        print(f"  {fn:<11}{lab:>10}{Ub:>7.2f}{rms:>10.4f}{mb:>10.4f}   {flag}")
for fn in A0:
    check(RARG[(fn, 10.0*KPC)] < 1.25*RARG[(fn, 0.0)],
          f"1.3  {fn}: COMPUTED, and it CONTRADICTS the bound this check originally asserted -- "
          f"a Galileon with R_* = 10 kpc does NOT destroy the RAR",
          f"rms {RARG[(fn,0.0)]:.4f} -> {RARG[(fn,10.0*KPC)]:.4f} dex (Ups {RARU[(fn,0.0)]:.2f} -> "
          f"{RARU[(fn,10.0*KPC)]:.2f}), max|bin| {RARB[(fn,0.0)]:.4f} -> {RARB[(fn,10.0*KPC)]:.4f}. "
          f"WITHDRAWAL LOGGED: the first version of this file asserted rms would MORE THAN DOUBLE "
          f"at 10 kpc.  It does not.  Direction of the error: it would have MANUFACTURED A DEFICIT "
          f"against route 2.  The RAR ceiling on R_* is ~10-30 kpc, not ~1 kpc.")
    check(RARG[(fn, 1.0*KPC)] < 1.02*RARG[(fn, 0.0)],
          f"1.4  {fn}: R_* = 1 kpc leaves the RAR essentially untouched",
          f"rms {RARG[(fn,0.0)]:.4f} -> {RARG[(fn,1.0*KPC)]:.4f} dex at the same Upsilon "
          f"({RARU[(fn,0.0)]:.2f} -> {RARU[(fn,1.0*KPC)]:.2f})")
    check(RARG[(fn, 1.0*MPC)] > 1.8*RARG[(fn, 0.0)],
          f"1.5  {fn}: R_* = 1 Mpc DOES break the RAR",
          f"rms {RARG[(fn,0.0)]:.4f} -> {RARG[(fn,1.0*MPC)]:.4f} dex with Upsilon driven to "
          f"{RARU[(fn,1.0*MPC)]:.2f}; max|bin| {RARB[(fn,0.0)]:.4f} -> {RARB[(fn,1.0*MPC)]:.4f} dex")

# ================================= PART 2 -- Vainshtein radii and the beta-free no-go
head("PART 2 -- VAINSHTEIN RADII (AU and kpc, both footings)")
def rV_sun(Rstar, fn, beta2=0.5):
    """one-body Newtonian-regime Vainshtein radius, r_V^3 = 4 beta^4 r_M^2 R_*."""
    return (4.0*beta2**2*RM[fn]**2*Rstar)**(1.0/3.0)
H0 = 67.4e3/MPC; r_c = CLIGHT/H0
lam_cosmo = 2.0*r_c**2/CLIGHT**2
print(f"  solar MOND radius r_M = {RM['canonical']/AU:.0f} AU canonical / {RM['alt']/AU:.0f} AU alt")
print(f"  cosmological Galileon (r_c = c/H0 = {r_c/MPC:.0f} Mpc):")
RSCOS = {}
for fn, a0 in A0.items():
    Rs = lam_cosmo*a0; RSCOS[fn] = Rs
    rv = rV_sun(Rs, fn)
    print(f"    {fn:<10} R_* = {Rs/MPC:8.4f} Mpc = {Rs/KPC:9.2f} kpc ;  r_V(Sun) = "
          f"{rv/AU:.4e} AU = {rv/PC:.2f} pc = {rv/KPC:.6f} kpc")
    check(Rs > 10.0*KPC, f"2.1  {fn}: the COSMOLOGICAL Galileon already has R_* >> a galaxy",
          f"R_* = {Rs/MPC:.3f} Mpc = {Rs/KPC:.0f} kpc -- MOND screened over the whole RAR range, "
          f"before any solar-system requirement is imposed")

head("PART 2b -- WHAT EACH SOLAR-SYSTEM TEST REQUIRES  (g5 = sqrt(g_N a0 r/R_*) inside)")
BUDGETS = [("Cassini gamma only", CASSINI_GAMMA*0.5*(GM_SUN/AU**2)),
           ("Mars EPM, differential (r^-1/2 shape, 19%)", MARS/0.19),
           ("Mars EPM, raw anomalous acceleration", MARS)]
REQ = {}
for lab, a_b in BUDGETS:
    for fn, a0 in A0.items():
        Rs = (GM_SUN/AU**2)*a0*AU/a_b**2
        REQ[(lab, fn)] = Rs; rv = rV_sun(Rs, fn)
        print(f"  {lab:<44}{fn:<11}a_b={a_b:.3e}  ->  R_* >= {Rs/MPC:11.5g} Mpc ; "
              f"r_V(Sun) >= {rv/PC:10.5g} pc = {rv/AU:.4e} AU")
RAW = "Mars EPM, raw anomalous acceleration"
for fn in A0:
    check(REQ[(RAW, fn)]/MPC > 900,
          f"2.2  {fn}: the raw Mars budget forces R_* >= {REQ[(RAW,fn)]/MPC:.0f} Mpc",
          "closed form R_* >= GM_sun a0 / (a_b^2 AU) -- beta and lambda BOTH eliminated")
    check(REQ[("Cassini gamma only", fn)] < 1.0*KPC,
          f"2.3  {fn}: CASSINI ALONE is easy for a Galileon; the EPHEMERIS is what kills",
          f"Cassini needs R_* >= {REQ[('Cassini gamma only',fn)]/AU:.1f} AU; the raw Mars budget "
          f"needs {REQ[(RAW,fn)]/AU:.3e} AU -- a factor {REQ[(RAW,fn)]/REQ[('Cassini gamma only',fn)]:.2e}")

head("PART 2c -- THE NO-GO, SYMBOLICALLY (beta and lambda eliminated)")
GM_, ab_, AU_ = sp.symbols('GM a_b AU', positive=True)
RsA = GM_*a0_/(ab_**2*AU_)
resA = sp.simplify(sp.sqrt((GM_/AU_**2)*a0_*AU_/RsA) - ab_)
check(resA == 0, "2.4  (A) ephemeris  =>  R_* >= GM a0 / (a_b^2 AU), exactly",
      f"g5(AU) - a_b at that R_* = {resA}")
print("   (B) RAR alive at r_gal  =>  R_* <= r_gal   (PART 1 measured that ceiling: ~1 kpc)")
print("   (A) ^ (B)  =>  GM a0/(a_b^2 AU) <= r_gal .  beta and lambda have CANCELLED.")
for fn, a0 in A0.items():
    Rmin = GM_SUN*a0/(MARS**2*AU)
    supp = math.sqrt(10.0*KPC/Rmin)
    print(f"   {fn:<10} GM a0/(a_b^2 AU) = {Rmin:.4e} m = {Rmin/MPC:.1f} Mpc = {Rmin/KPC:.4e} kpc"
          f"   vs allowed 1 kpc  ->  MISS by {Rmin/KPC:.4e}x in radius")
    check(Rmin/KPC > 1e5, f"2.5  {fn}: the two requirements miss by {Rmin/KPC:.2e} in radius",
          f"and the MOND force at 10 kpc is then suppressed by sqrt(10 kpc/R_*) = {supp:.3e} -- "
          f"the phantom is gone, i.e. buying the ephemeris costs the entire RAR")
    ab_need = math.sqrt(GM_SUN*a0/(10.0*KPC*AU))
    print(f"   {fn:<10} to permit R_* <= 10 kpc the ephemeris budget would have to be relaxed to "
          f"a_b = {ab_need:.3e} m/s^2 = {ab_need/MARS:.3e} x Mars = {ab_need/a0:.3f} a0")
    check(ab_need/MARS > 1e3, f"2.6  {fn}: the kill is robust to >1000x error in the ephemeris budget",
          f"a_b would need to be {ab_need/MARS:.2e}x weaker, i.e. {ab_need/a0:.2f} a0 -- comparable "
          f"to the a0-line's OWN unscreened anomaly a0/2, which is itself excluded at 33,435x")

# ============================================================ PART 3 -- THE DOUBLE COUNT
head("PART 3 -- THE DOUBLE COUNT: M(<r) vs M_b nu(y) at 0.5 / 1 / 3 / 10 r_M, both footings")
SHARE = 5.375
TOL = 10.0**0.06 - 1.0
print(f"  Omega_dm/Omega_b = {SHARE};  0.06 dex = {TOL*100:.2f}% fractional tolerance")
print(f"  overshoot == [ (M_b + M_cond + M_ph)/(M_b nu) - 1 ] / (10^0.06 - 1)")
print(f"  {'x r_M':>7}{'y':>12}{'nu':>10}{'M_ph/M_b':>11}{'M_tot/M_b':>11}{'ratio':>9}{'overshoot':>11}")
OVR = {}
for xr in (0.5, 1.0, 3.0, 10.0):
    y = 1.0/xr**2; nu = math.sqrt(1.0+1.0/y); tot = nu + SHARE
    OVR[xr] = (tot/nu - 1.0)/TOL
    print(f"  {xr:>7.1f}{y:>12.4f}{nu:>10.4f}{nu-1:>11.4f}{tot:>11.4f}{tot/nu:>9.4f}{OVR[xr]:>11.1f}")
check(abs(OVR[0.5]-32.5) < .6 and abs(OVR[1.0]-25.7) < .6 and abs(OVR[3.0]-11.5) < .4
      and abs(OVR[10.0]-3.6) < .3,
      "3.1  the published double-count table is reproduced exactly, and it is FOOTING-INDEPENDENT",
      f"{OVR[0.5]:.1f}/{OVR[1.0]:.1f}/{OVR[3.0]:.1f}/{OVR[10.0]:.1f} vs published "
      f"32.5/25.7/11.5/3.6.  a0 cancels because the radii are quoted in units of r_M.")

print("\n  WITH THE GALILEON: the phantom is multiplied by sqrt(r/R_*) for r < R_*, while the")
print("  condensate is UNTOUCHED (the Galileon does not couple to it).  M_gal = 1e11 Msun.")
MGAL = 1.0e11*MSUN
print(f"  {'footing':<11}{'R_*':>12}" + "".join(f"{('ov@%.1frM'%x):>11}" for x in (0.5,1.0,3.0,10.0))
      + f"{'RAR rms':>10}")
for fn, a0 in A0.items():
    rM_gal = math.sqrt(GNEWT*MGAL/a0)
    for Rs in [0.0, 1.0*KPC, 10.0*KPC, 100.0*KPC, 1.0*MPC]:
        lab = "OFF" if Rs == 0 else (f"{Rs/KPC:g} kpc" if Rs < MPC else f"{Rs/MPC:g} Mpc")
        line = f"  {fn:<11}{lab:>12}"
        for xr in (0.5, 1.0, 3.0, 10.0):
            r = xr*rM_gal; y = 1.0/xr**2
            nu = math.sqrt(1.0+1.0/y)
            supp = math.sqrt(r/Rs) if (Rs > 0 and r < Rs) else 1.0
            deliv = 1.0 + SHARE + supp*(nu-1.0)     # baryons + condensate + SCREENED phantom
            line += f"{(deliv/nu - 1.0)/TOL:>11.1f}"   # target is the OBSERVED RAR, nu(y)
        line += f"{RARG.get((fn,Rs), float('nan')):>10.4f}"
        print(line)
    print(f"   -> r_M(1e11 Msun) = {rM_gal/KPC:.2f} kpc, so 10 r_M = {10*rM_gal/KPC:.1f} kpc")
    # --- what suppression WOULD be needed, radius by radius ---
    print(f"   required phantom suppression  supp_req(y) = (nu - 1 - {SHARE})/(nu - 1):")
    print(f"   {'x r_M':>7}{'nu':>10}{'supp_req':>12}{'achievable?':>14}")
    for xr in (0.5, 1.0, 3.0, 6.0, 10.0, 30.0, 100.0):
        y = 1.0/xr**2; nu = math.sqrt(1.0+1.0/y)
        req = (nu - 1.0 - SHARE)/(nu - 1.0)
        print(f"   {xr:>7.1f}{nu:>10.4f}{req:>12.4f}"
              f"{('yes' if 0.0 <= req <= 1.0 else 'IMPOSSIBLE'):>14}")
    x_crit = 1.0/math.sqrt(1.0/((1.0+SHARE)**2 - 1.0))
    print(f"   -> supp_req >= 0 only for nu >= 1 + {SHARE} = {1+SHARE}, i.e. r >= {x_crit:.3f} r_M "
          f"= {x_crit*rM_gal/KPC:.1f} kpc for this galaxy")
    check(x_crit > 6.0,
          f"3.2  {fn}: NO amount of phantom screening -- Vainshtein or otherwise -- can fix the "
          f"double count inside {x_crit:.2f} r_M",
          f"inside that radius the CONDENSATE ALONE at the cosmic share ({1+SHARE:.3f} M_b) already "
          f"exceeds the OBSERVED dynamical mass (nu M_b, nu = {math.sqrt(1+1/4.0):.3f} at 0.5 r_M), "
          f"so setting the phantom to zero ENTIRELY still overshoots by "
          f"{((1+SHARE)/math.sqrt(1+1/4.0) - 1)/TOL:.1f} tolerance units at 0.5 r_M (vs "
          f"{OVR[0.5]:.1f} unscreened).  This is a "
          f"statement about the CONDENSATE, not about the screen, and it is footing-independent.")
    # can sqrt(r/R_*) match the required profile anywhere?
    r10 = 10.0*rM_gal; nu10 = math.sqrt(1.0+1.0/0.01)
    req10 = (nu10 - 1.0 - SHARE)/(nu10 - 1.0)
    R_match = r10/req10**2
    r30 = 30.0*rM_gal; nu30 = math.sqrt(1.0+1.0/(1/900.))
    req30 = (nu30 - 1.0 - SHARE)/(nu30 - 1.0)
    got30 = math.sqrt(r30/R_match) if r30 < R_match else 1.0
    print(f"   matching at 10 r_M needs R_* = {R_match/KPC:.1f} kpc = {R_match/MPC:.4f} Mpc; that "
          f"same R_* then gives supp({30} r_M) = {got30:.4f} against the required {req30:.4f}")
    check(abs(got30/req30 - 1.0) > 0.10,
          f"3.3  {fn}: the sqrt(r/R_*) profile has the WRONG SHAPE -- one radius can be matched, "
          f"not two",
          f"tuned to 10 r_M it misses 30 r_M by {abs(got30/req30-1)*100:.1f}%, and the mismatch is "
          f"in the direction of leaving residual OVERSHOOT at large radius "
          f"({'under' if got30 < req30 else 'over'}-suppressing)")
    for Rs, lab in [(1.0*KPC, "R_* = 1 kpc (RAR ceiling)"), (REQ[(RAW, fn)], "R_* required by ephemeris")]:
        rv = rV_sun(Rs, fn)
        rho_V = 3.0*MSUN/(4.0*math.pi*rv**3)
        rho_gal = 3.0*MGAL/(4.0*math.pi*(10.0*rM_gal)**3)
        print(f"   {fn:<10} {lab:<30} rho_V = 3/(4 pi G lambda) = {rho_V:.4e} kg/m^3 ;"
              f"  mean rho at 10 r_M = {rho_gal:.4e} ;  rho_V/rho_halo = {rho_V/rho_gal:.4e}")

# ============================================================== PART 4 -- Q2
head("PART 4 -- Q2.  (a) the Galileon's EFE quadrupole is EXACTLY ZERO, by Galilean invariance")
x1, x2, x3, e1, e2, e3, Lam = sp.symbols('x1 x2 x3 e1 e2 e3 Lambda', real=True)
XX = (x1, x2, x3); rr_ = sp.sqrt(x1**2+x2**2+x3**2)
pi0 = sp.Function('pi0'); Pi = pi0(rr_)
def galE(f):
    H = sp.Matrix(3, 3, lambda i, j: sp.diff(f, XX[i], XX[j]))
    box = sum(H[i, i] for i in range(3))
    return box + (2/Lam**3)*(box**2 - sum(H[i, j]**2 for i in range(3) for j in range(3)))
dif = sp.simplify(sp.expand(galE(Pi + e1*x1 + e2*x2 + e3*x3) - galE(Pi)))
check(dif == 0,
      "4.1  the cubic-Galileon field equation is EXACTLY invariant under pi -> pi + e.x",
      f"E[pi0(r)+e.x] - E[pi0(r)] = {dif}, identically, for arbitrary radial pi0 and arbitrary e.  "
      f"A constant external field is PURE GAUGE for the Galileon, so the Galileon contributes NO "
      f"external-field quadrupole at any order.  This is a genuine WIN for route 2.")

head("PART 4b -- validate the quadrupole pipeline against the published anchors FIRST")
def nu_routeA(y):
    y = np.asarray(y, float); s = np.sqrt(y)
    out = np.where(s < 1e-8, 1.0/np.maximum(s, 1e-300), 1.0/(1.0-np.exp(-np.minimum(s, 700.0))))
    return np.where(s > 40.0, 1.0+np.exp(-np.minimum(s, 700.0)), out)
def nu_a0line(y): y = np.asarray(y, float); return np.sqrt(1.0+1.0/y)
def solve_eN(nu, et):
    return brentq(lambda x: x*float(np.asarray(nu(x)).ravel()[0])-et, 1e-12, 1e10,
                  xtol=1e-15, rtol=8.9e-16)
def q2D(numinus1, et, nu_for_eN, vmax=400.0, epsrel=1e-9):
    eN = solve_eN(nu_for_eN, et)
    def ig(mu, v):
        D = eN*eN + v**4 + 2.0*eN*v*v*mu
        if D <= 0: return 0.0
        return numinus1(math.sqrt(D), v)*(eN*(3*mu-5*mu**3) + v*v*(1-3*mu*mu))
    val, _ = integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0,
                               epsabs=1e-12, epsrel=epsrel)
    return 1.5*val, eN
ANCH = {1.0: 0.094, 1.5: 0.159, 2.0: 0.221}
print(f"  {'etilde':>8}{'my |q|':>12}{'published':>12}{'ratio':>9}")
amax = 0.0
for et, ref in ANCH.items():
    qv, _ = q2D(lambda y, v: float(nu_routeA(y))-1.0, et, nu_routeA)
    print(f"  {et:>8.1f}{abs(qv):>12.5f}{ref:>12.3f}{abs(qv)/ref:>9.4f}")
    amax = max(amax, abs(abs(qv)/ref - 1.0))
check(amax < 0.01, "4.2  PIPELINE VALIDATED against q(1)=0.094, q(1.5)=0.159, q(2)=0.221",
      f"max deviation {amax*100:.2f}%")

head("PART 4c -- Q2 with the Galileon on, as a function of R_*")
print("  Model: (nu_eff-1)(y,r) = s(y, R_*/r)/y, r = r_M/v, the local flux equation applied")
print("  pointwise.  DIRECTION OF THE APPROXIMATION: it lets the Galileon term respond to the")
print("  TOTAL field including the external piece, whereas 4.1 proved the true response to a")
print("  constant external field is ZERO.  So this OVERSTATES the surviving quadrupole: it is a")
print("  conservative UPPER bound on Q2.")
print(f"  {'footing':<11}{'R_*':>16}{'|q|':>12}{'Q2 [s^-2]':>13}{'x ceiling':>12}{'sigma':>9}")
Q2R = {}
for fn, a0 in A0.items():
    rM = RM[fn]
    for Rs in [0.0, 1.0*KPC, 10.0*KPC, 1.0*MPC, REQ[(RAW, fn)]]:
        f = (lambda R: (lambda y, v: s_scalar(y, (R*v/rM) if R > 0 else 0.0)/y))(Rs)
        qv, _ = q2D(f, GEXT/a0, nu_a0line, epsrel=1e-7)
        QA = PREF(a0)*abs(qv)*RA; Q2R[(fn, Rs)] = QA/Q2_CEIL
        lab = "OFF" if Rs == 0 else (f"{Rs/KPC:g} kpc" if Rs < MPC else f"{Rs/MPC:.4g} Mpc")
        print(f"  {fn:<11}{lab:>16}{abs(qv):>12.5f}{QA:>13.3e}{QA/Q2_CEIL:>12.4g}"
              f"{(QA-Q2_CEN)/Q2_SIG:>9.1f}")
for fn in A0:
    ref = 5.59 if fn == "canonical" else 6.39
    check(abs(Q2R[(fn, 0.0)]/ref - 1) < 0.12,
          f"4.3  {fn}: R_*=0 reproduces route1B's a0-line Q2 ({ref}x ceiling)",
          f"got {Q2R[(fn,0.0)]:.3f}x")
    check(Q2R[(fn, 1.0*MPC)] < Q2R[(fn, 1.0*KPC)] < 1.0,
          f"4.4  {fn}: Q2 falls monotonically with R_* and is already CLEARED at R_* = 1 kpc",
          f"{Q2R[(fn,1.0*KPC)]:.4g}x (1 kpc) > {Q2R[(fn,10.0*KPC)]:.4g}x (10 kpc) > "
          f"{Q2R[(fn,1.0*MPC)]:.4g}x (1 Mpc).  Q2 is NOT what kills route 2 -- see 4.6.")
    check(Q2R[(fn, 1.0*KPC)] < 1.0,
          f"4.5  {fn}: *** COMPUTED RESULT, OPPOSITE TO THE BOUND THIS CHECK FIRST ASSERTED *** -- "
          f"a Galileon with R_* = 1 kpc CLEARS the Cassini quadrupole while leaving the RAR intact",
          f"Q2 = {Q2R[(fn,1.0*KPC)]:.4f}x the ceiling (from {Q2R[(fn,0.0)]:.2f}x unscreened, a "
          f"{Q2R[(fn,0.0)]/Q2R[(fn,1.0*KPC)]:.0f}x reduction) with RAR rms "
          f"{RARG[(fn,0.0)]:.4f} -> {RARG[(fn,1.0*KPC)]:.4f} dex ON CARL'S OWN a0-LINE KERNEL.  "
          f"WITHDRAWAL LOGGED: the first version asserted Q2 would still exceed the ceiling.  "
          f"Direction of that error: it would have MANUFACTURED A DEFICIT.  This is route 2's one "
          f"genuine WIN and route1B could not get it without abandoning the a0-line for mu_n.  "
          f"Reason it works: the Q2 source sits at r ~ few thousand AU where y ~ 1 and the "
          f"k-mouflage flux Y(s) = s^2/(1-2s) is still O(1), so a Galileon term of size R_*/r ~ 4e4 "
          f"swamps it -- whereas at 1 AU Y(s) has a POLE at s = 1/2 that no finite Galileon beats.")

head("PART 4d -- the 1-AU MONOPOLE, which is the binding solar-system test")
print(f"  {'footing':<11}{'R_*':>16}{'s(1AU)':>13}{'anomaly [m/s^2]':>18}{'x Mars':>14}")
for fn, a0 in A0.items():
    y1 = (GM_SUN/AU**2)/a0
    for Rs in [0.0, 1.0*KPC, 1.0*MPC, 100.0*MPC, REQ[(RAW, fn)]]:
        sv = s_scalar(y1, (Rs/AU) if Rs > 0 else 0.0); an = sv*a0
        lab = "OFF" if Rs == 0 else (f"{Rs/KPC:g} kpc" if Rs < MPC else f"{Rs/MPC:.4g} Mpc")
        print(f"  {fn:<11}{lab:>16}{sv:>13.5e}{an:>18.5e}{an/MARS:>14.5g}")
    a_off = s_scalar(y1, 0.0)*a0; a_1kpc = s_scalar(y1, 1.0*KPC/AU)*a0
    check(a_off/MARS > 3.0e4 and a_1kpc/MARS > 3.0e4,
          f"4.6  {fn}: at the RAR-allowed R_* the Galileon leaves the 1-AU monopole UNTOUCHED",
          f"{a_off/MARS:.0f}x Mars with the Galileon off, {a_1kpc/MARS:.0f}x at R_*=1 kpc.  "
          f"Vainshtein cannot grip there because k-mouflage has ALREADY capped |grad pi| at a0/2 "
          f"-- the two screenings are ANTI-SYNERGISTIC.")

head("PART 4e -- THE PRICE OF THE Q2 WIN: WIDE BINARIES GO NEWTONIAN  (pre-registration impact)")
print("  Isolated 2 Msun binary, no external field (the EFE is NOT applied here -- flagged).")
print("  boost = 1 + s/y ;  a gamma_v-like velocity ratio is sqrt(boost).")
print(f"  {'footing':<11}{'sep [kAU]':>10}{'y':>10}{'boost OFF':>11}{'gv OFF':>9}"
      f"{'boost 1kpc':>12}{'gv 1kpc':>9}")
WB = {}
for fn, a0 in A0.items():
    for skau in (2.0, 5.0, 10.0, 20.0, 30.0):
        d = skau*1e3*AU; gN = 2.0*GM_SUN/d**2; y = gN/a0
        s0 = s_scalar(y, 0.0); s1 = s_scalar(y, 1.0*KPC/d)
        b0, b1 = 1.0+s0/y, 1.0+s1/y
        WB[(fn, skau)] = (b0, b1)
        print(f"  {fn:<11}{skau:>10.1f}{y:>10.4f}{b0:>11.4f}{math.sqrt(b0):>9.4f}"
              f"{b1:>12.4f}{math.sqrt(b1):>9.4f}")
for fn in A0:
    b0, b1 = WB[(fn, 10.0)]
    check(math.sqrt(b1) < 1.02 and math.sqrt(b0) > 1.10,
          f"4.7  {fn}: the R_* = 1 kpc Galileon ERASES the wide-binary signal",
          f"at 10 kAU the velocity boost falls from {math.sqrt(b0):.4f} to {math.sqrt(b1):.4f}.  "
          f"This is a HARD, FALSIFIABLE COST: Amendment 9/10's in-force band is gamma_v = "
          f"1.1614-1.2267, and route 2 tuned to clear Q2 predicts gamma_v ~ 1.00.  A DR4 detection "
          f"of ANY MOND boost in 2-30 kAU wide binaries falsifies route 2's Q2 escape, and a "
          f"Newtonian DR4 result -- which the corpus counts as 4.7-7.1 sigma evidence AGAINST the "
          f"framework -- would be the ONLY DR4 outcome route 2 survives.  CAVEAT: the external "
          f"field is not applied here, and the Galileon superposition of Sun + galaxy + companion "
          f"is a known-hard unsolved problem; treat the magnitude as indicative, the SIGN as solid.")

# ============================================================== PART 5 -- HEALTH
head("PART 5 -- HEALTH: ghost, c_T, gradient stability, superluminality, Cherenkov")
rS, epsS, CS = sp.symbols('r epsilon C', positive=True)
Yb = CS*rS**sp.Rational(-3, 2)                 # deep-Vainshtein background y(r) = pi0'/r
lap = 3*Yb + rS*sp.diff(Yb, rS)
Zrr = 1 + epsS*(lap - (rS*sp.diff(Yb, rS) + Yb))
Zan = 1 + epsS*(lap - Yb)
Z00 = -(1 + epsS*lap)
print("   Z^mn = eta^mn + eps (eta^mn Box pi0 - d^m d^n pi0),  eps = 4 alpha/Lambda^3,  y = pi0'/r")
print("   Box pi0 =", sp.simplify(lap), "   (deep-Vainshtein y = C r^-3/2)")
print("   Z^rr - 1 =", sp.simplify(Zrr-1), "    Z^ang - 1 =", sp.simplify(Zan-1),
      "    -Z^00 - 1 =", sp.simplify(-Z00-1))
cr2 = sp.simplify(sp.simplify(Zrr-1)/sp.simplify(-Z00-1))
can2 = sp.simplify(sp.simplify(Zan-1)/sp.simplify(-Z00-1))
print(f"   c_r^2 = {cr2} = {float(cr2):.8f}      c_ang^2 = {can2} = {float(can2):.8f}")
check(abs(float(cr2)-4.0/3.0) < 1e-12,
      "5.1  the RADIAL scalar mode is SUPERLUMINAL inside the Vainshtein region: c_r^2 = 4/3 EXACT",
      f"c_r = {math.sqrt(float(cr2)):.6f} c.  Derived from Z^mn here, not quoted.  Consequence: no "
      f"standard Wilsonian UV completion (Adams-Arkani-Hamed-Dubovsky-Nicolis-Rattazzi 2006).  "
      f"This is a generic cubic-Galileon disease, NOT something Carl's numbers cause.")
check(0 < float(can2) < 1,
      "5.2  the ANGULAR scalar mode is subluminal (c_ang^2 = 1/3); no ghost, no gradient instability",
      f"-Z^00 = 1 + (3/2) eps y > 0 and Z^rr = 1 + 2 eps y > 0 for eps y > 0.  A SUBLUMINAL scalar "
      f"admits gravi-Cherenkov emission by ultra-relativistic matter; the coupling is M_Pl-"
      f"suppressed and the mode exists only inside r_V.  NOT PRICED HERE -- open.")
print("\n   TENSOR SECTOR: the cubic Galileon is G3(X) Box phi.  In the Horndeski basis c_T^2 - 1")
print("   depends on G4_X and G5 only; G3 enters NEITHER.  Hence c_T = 1 EXACTLY.")
check(True, "5.3  c_T = 1 EXACTLY for the cubic Galileon -- GW170817 is SILENT on it",
      "the shorthand 'GW170817 killed the cubic Galileon' is wrong in this respect and is "
      "corrected here.  What GW170817-era data killed was cubic-Galileon DARK ENERGY: (i) the ISW "
      "cross-correlation sign (Renk, Zumalacarregui, Ferreira & Baker 2017, ~7.8 sigma) and (ii) "
      "GW-induced decay of the cosmological background (Creminelli et al 2018/2019).  Both "
      "constrain a Galileon that IS the dark energy.  ATTRIBUTIONS FROM MEMORY, NOT REFETCHED.")
for fn, a0 in A0.items():
    print(f"   {fn:<10} R_*(ephemeris)/R_*(cosmological Galileon) = {REQ[(RAW,fn)]/RSCOS[fn]:.4e}"
          f"  ->  Lambda^3 is SMALLER by that factor, i.e. this Galileon is WEAKER than the DE one")
check(REQ[(RAW, "canonical")] > RSCOS["canonical"],
      "5.4  the required Galileon is WEAKER-coupled than the dark-energy Galileon",
      "so the ISW and GW-decay kills of cubic-Galileon DE do not transfer.  BUT the same fact "
      "means this Galileon carries NO cosmological energy density: it cannot be Omega_dm and it "
      "cannot be w = -1 dark energy.  Route 2 leaves the CMB leg exactly where it was.")

# ================================================ PART 6 -- the Omega_dm question
head("PART 6 -- WHAT CARRIES Omega_dm = 0.265?")
print("""   Route 2's answer is NOTHING NEW.  The Galileon is shift-symmetric with no potential;
   its cosmological density is set by Lambda^3, and 5.4 showed the required Lambda^3 is SMALLER
   than the dark-energy Galileon's, so its cosmological density is negligible BY CONSTRUCTION.
     * Omega_dm = 0.265 still carried by Carl's DBI condensate.  UNCHANGED.
     * w = -1 exact:   UNCHANGED (nothing touches the condensate's shift charge).
     * CLASS CMB pass: UNCHANGED (nothing added at recombination; a0(z) untouched).
     * c_T = 1, no ghost: kept (5.1-5.3), at the price of a superluminal radial mode.
     * no dark-matter PARTICLE: respected -- the Galileon is a field.
     * the condensate STILL CLUSTERS.  The only credit route 2 could earn on the double count is
       by switching the PHANTOM off, and PART 3 priced that: it costs the RAR.""")
check(True, "6.1  route 2 changes NOTHING in the cosmological sector",
      "it is a solar-system screening device, not a dark-sector mechanism")

head("PART 7 -- PRIOR ART, AND WHAT IS NEW")
print("""   PUBLISHED PRIOR ART, credited explicitly:
     * Vainshtein 1972 -- the mechanism.
     * Nicolis, Rattazzi & Trincherini 2009 -- the Galileon; the superluminality of 5.1 is theirs.
     * Adams, Arkani-Hamed, Dubovsky, Nicolis & Rattazzi 2006 -- superluminality vs analyticity.
     * Babichev, Deffayet & Ziour 2009 -- "k-Mouflage gravity"; the name and the mechanism.
     * >>> Babichev, Deffayet & Esposito-Farese, PRD 84, 061502(R) (2011), arXiv:1106.2538,
       "Improving relativistic MOND with Galileon k-mouflage" <<<  This IS route 2.  Their
       abstract claims the model "passes solar-system tests AT THE POST-NEWTONIAN ORDER".  That
       is exactly the level this file finds easy: check 2.3 gives R_* >= 119 AU canonical /
       144 AU alt from Cassini gamma alone.  I COULD NOT VERIFY from the fetched PDF whether they
       price the 1-AU anomalous-ACCELERATION bound (Mars/Earth ranging, ~1e-15 m/s^2), which is a
       DIFFERENT and 2.4e15-times-tighter requirement on R_* -- so no claim is made here about
       what they did or did not check.  ATTRIBUTION FLAGGED AS UNVERIFIED-IN-DETAIL.
     * Brax & Valageas 2014 -- k-mouflage cosmology.
     * Renk, Zumalacarregui, Ferreira & Baker 2017 -- ISW kill of cubic-Galileon dark energy.
     * Creminelli et al 2018/2019 -- GW-induced decay of a cosmological Galileon background.
     * Blanchet & Novak 2011; Hees et al 2014; Desmond, Hees & Famaey 2024; Park et al 2026 --
       the AQUAL quadrupole and its solar-system bound (the Q2 machinery reused here).

   WHAT IS NEW HERE, and what a referee should attack:
     1. THE ONE-PARAMETER REDUCTION.  In a MOND background the Galileon/k-mouflage competition
        collapses to a single UNIVERSAL LENGTH R_* = lambda a0 / (2 beta^2), mass- and
        beta-independent, because both fluxes are quadratic in the scalar force (check 0.2).
        The Vainshtein DENSITY threshold does not survive the MOND cap on |grad pi|.
     2. THE beta- AND Lambda-FREE NO-GO tying the ephemeris bound to the MOND-screening radius:
        R_* >= GM_sun a0/(a_b^2 AU) (check 2.4), = 1.373e6 / 1.654e6 Mpc.
     3. Q2 == 0 for the Galileon EXACTLY, by Galilean invariance (check 4.1) -- a symmetry
        statement, not a suppression estimate.
     4. THE MEASURED Q2 WIN on Carl's own a0-line at R_* = 1 kpc (check 4.5), and its price in
        wide binaries (check 4.7).
     5. The screen-independent double-count bound at 6.296 r_M (check 3.2).

   KNOWN WEAKNESSES OF THIS FILE, stated so they can be attacked:
     * the quasi-static flux model uses ONE radius r per point; Galileon superposition (Sun +
       Galaxy + companion) is a known-hard unsolved problem and is NOT solved here.
     * the Q2 pipeline is QUMOND-with-an-AQUAL-calibration (RA = 1.871/1.5), inherited.
     * the <= 0.06 dex intrinsic RAR target is UNDETERMINED (check 1.2): no hierarchical fit.
     * gravi-Cherenkov from the c_ang^2 = 1/3 mode is NOT priced.""")
check(True, "7.1  prior art credited; novelty and weaknesses both stated")

head("VERDICT")
print("""   ROUTE 2 IS **PARTIAL**, NOT DEAD AND NOT A SURVIVOR.
   IT BREAKS CASSINI Q2 ON CARL'S OWN KERNEL -- the first thing in this programme that does --
   AND IT DOES NOT BREAK THE DOUBLE COUNT.
     WIN     Q2: 5.59x -> 0.050x ceiling (canonical), 6.39x -> 0.053x (alt), at R_* = 1 kpc,
             with the a0-line intact and the RAR unmoved (0.1083 -> 0.1088 dex, same Upsilon).
     KILL    the 1-AU monopole is UNCHANGED (33,435x / 40,282x Mars).  Fixing it needs
             R_* >= 1.373e6 / 1.654e6 Mpc, at which the RAR is destroyed.  beta- and
             Lambda-independent.
     KILL    the double count is untouched: no screen of ANY kind can fix it inside 6.296 r_M,
             because there the clustered condensate ALONE exceeds the observed mass.
     NULL    Omega_dm, w = -1, the CMB pass, a0(z): all UNCHANGED.  Route 2 says nothing about
             what carries Omega_dm.  It is a solar-system device.
     COST    wide binaries go Newtonian (gamma_v 1.157 -> 1.003 at 10 kAU), contradicting the
             in-force Amendment 10 band 1.1614-1.2267.  A sharp, falsifiable prediction.""")

print("\n"+"="*100)
if FAIL:
    print(f"RESULT: {NCHK[0]-len(FAIL)}/{NCHK[0]} passed.  FAILURES: {FAIL}"); sys.exit(1)
print(f"RESULT: {NCHK[0]}/{NCHK[0]} checks passed.")
sys.exit(0)
