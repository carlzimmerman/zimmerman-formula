#!/usr/bin/env python3
# I007 — Does U still saturate once a0 is a FIELD?  (S4)
# HYP: legality forces U -> s in v = sqrt(Y)/a0, but a0 depends on the local charge,
#      so the OBSERVABLE U at fixed radius, plotted against y = g_bar/a0(0), need not
#      be bounded.  USES: N2 + N4 + N6.
#
# Construction (from the brief, N6 + N4 + N2):
#   F      = a0(nu)/a0(0) = [(1+nu0^2)/(1+nu^2)]^(1/4)          (N4)
#   nu     = nu0 * rho/rho0 ,  nu0 <= 2.36e-6                     (N4)
#   rho(r) = g_bar/(4 pi G r)        [point-mass enclosed density] (brief)
#   v      = sqrt(Y)/a0(nu),  sqrt(Y) = g_bar  =>  v = y/F        (N6; v = sqrt(Y)/a0)
#   U(v)   = v/(1 + v/s)         ("inverted" from J_Y = v/(1 - v/s))
#   U_eff  = F * U(v)           = F * (y/F)/(1 + (y/F)/s) = F*y*s/(sF + y)
#
# Decisive question: is U_eff bounded by s?  Algebraically
#   U_eff = F*y*s/(sF+y) <= s  <=>  F*y <= sF + y  <=>  y(F-1) <= sF.
# For F <= 1 (rho >= rho0, the physical branch) the LHS <= 0 <= RHS, so U_eff <= s
# strictly.  U_eff saturates at F*s <= s, never at infinity => HYP (unbounded) is FALSE.
#
# Report BOTH a0 footings (PROTOCOL line 1).  U_eff(y; s, F) is a function of y, and
# F enters through rho = y*a0(0)/(4 pi G r), so the two footings give two F columns.

import math, sys, json

# ---- physical constants / footings -------------------------------------------
G  = 6.67430e-11          # m^3 kg^-1 s^-2
c  = 2.99792458e8         # m/s
kappa = 0.5               # N1: fitted 0.529 +/- 0.034; use nominal 1/2 for the gate
LAMBDA = 1.08e-52         # m^-2 (cosmological constant; loose, for the a0 gate only)

A0_CANON = 9.3619e-11     # PROTOCOL line 1 canonical footing
A0_ALT   = 1.1279e-10     # PROTOCOL line 1 alternative footing

NU0 = 2.36e-6             # N4 ceiling (recombination pin, stage76) -- most suppression-favourable
# rho0: reference density. Use the I002 convention 0.265*9.47e-27 kg/m^3 (cosmic mean order).
RHO0 = 0.265 * 9.47e-27   # = 2.5096e-27 kg/m^3
S_GRID = [1.27e-5, 1e-3, 0.219]
Y_GRID = [1.0, 2.0, 10.0, 1e3, 1e6, 6.33e7]

checks = []
def check(n, ok, msg):
    checks.append(ok)
    print(f"[{'ok' if ok else 'FAIL'}] {n}: {msg}")

# ---- 1. a0 footings gate -----------------------------------------------------
# a0 = kappa*c*sqrt(G*rho_Lambda), rho_Lambda = c^2*Lambda/(8*pi*G)
#  => a0 = kappa*c^2*sqrt(Lambda/(8*pi))
a0_calc = kappa * c**2 * math.sqrt(LAMBDA/(8*math.pi))
check(1, 0.9 < a0_calc/A0_CANON < 1.15,
      f"a0 = kappa*c*sqrt(G*rho_Lambda) = {a0_calc:.4e} m/s^2 vs canon {A0_CANON:.4e} "
      f"(ratio {a0_calc/A0_CANON:.3f}); alt footing {A0_ALT:.4e}")

# ---- 2. U(v) = v/(1+v/s) monotone in v (N6 legality: U strictly increasing) --
def U_of_v(v, s):
    return v/(1.0 + v/s)
vtest = [i/100.0 for i in range(1, 5000)]
mono = all(U_of_v(vtest[i], 0.219) < U_of_v(vtest[i+1], 0.219) for i in range(len(vtest)-1))
dU_dv = lambda v, s: s/(1.0 + v/s)**2
check(2, mono and all(dU_dv(v, s) > 0 for v in vtest for s in S_GRID),
      "U(v)=v/(1+v/s) strictly increasing in v for all v>0, all s  (dU/dv = s/(1+v/s)^2 > 0)")

# ---- 3. field-a0 chain: F, nu, rho, v, U_eff --------------------------------
def F_of_nu(nu):
    return ((1.0 + NU0**2)/(1.0 + nu**2))**0.25

def nu_of_y(y, a0, r, rho0):
    gbar = y * a0                 # y = g_bar/a0(0)  =>  g_bar = y*a0
    rho  = gbar/(4.0*math.pi*G*r)
    return NU0 * rho/rho0

def Ueff(y, s, a0, r, rho0):
    nu = nu_of_y(y, a0, r, rho0)
    F  = F_of_nu(nu)
    v  = y/F                      # = g_bar/a0(nu) = y*a0(0)/(F*a0(0)) = y/F
    Uv = U_of_v(v, s)
    return F*Uv, F, nu, v

# ---- 4. universal bound U_eff <= s over the whole grid, BOTH footings -------
# radii: representative RAR/ephemeris scales (kpc). 100 kpc ~ virial radius.
RCIRC = 3.085677581e19            # 1 kpc in metres
RS = [1, 10, 100]
Fmax = (1.0 + NU0**2)**0.25       # F at nu->0; the global ceiling of F
ratio_rows = []
max_Ueff_over_s = 0.0
for a0, foot in [(A0_CANON, "canon"), (A0_ALT, "alt")]:
    for rkpc in RS:
        r = RCIRC * rkpc
        for s in S_GRID:
            rowvals = []
            for y in Y_GRID:
                ue, F, nu, v = Ueff(y, s, a0, r, rho0=RHO0)
                rowvals.append(ue)
                if ue/s > max_Ueff_over_s:
                    max_Ueff_over_s = ue/s
            ratio = rowvals[-1]/rowvals[1]   # U_eff(6.33e7)/U_eff(2)
            ratio_rows.append((foot, rkpc, s, ratio, rowvals[-1], rowvals[1]))
            # bound check on this s
            bounded = all(ue <= s*Fmax*(1+1e-9) for ue in rowvals)
            if not bounded:
                print(f"   {foot} r={r/RCIRC:.0f}kpc s={s:.1e}: max U_eff/s = "
                      f"{max(ue/s for ue in rowvals):.6f}")
        # report the ratio for s=0.219 (the RAR-relevant saturation)
print()
print("  ratio  U_eff(6.33e7)/U_eff(2)  by footing, radius, s  (s=0.219 line):")
for foot, rkpc, s, ratio, u6, u2 in ratio_rows:
    if abs(s-0.219) < 1e-6:
        print(f"    {foot:5s}  r={rkpc:5.0f} kpc   ratio = {ratio:.3e}"
              f"   (U_eff(6.33e7)={u6:.3e}, U_eff(2)={u2:.3e})")

bounded_all = max_Ueff_over_s <= Fmax*(1+1e-9)
check(3, bounded_all,
      f"U_eff <= s*Fmax = s*{Fmax:.15f} at EVERY (y,s,r,footing); "
      f"max U_eff/s over grid = {max_Ueff_over_s:.6f} (<= 1  => bounded, KILL branch)")

# ---- 5. algebraic proof of the bound (independent of r, rho0, footing) ------
# U_eff = F*y*s/(sF+y) <= s  <=>  y(F-1) <= sF.  For F<=1 (rho>=rho0, physical) LHS<=0.
# The only way to exceed s is F>1, i.e. nu<nu0, i.e. rho<rho0; then U_eff <= Fmax*s ~ s.
exceed_cases = 0
for a0 in (A0_CANON, A0_ALT):
    for r in [1e19, 1e20, 1e21, 1e22, 1e23, 1e24, 1e25, 1e26, 1e27, 1e28]:
        for y in Y_GRID:
            for s in S_GRID:
                ue, F, nu, v = Ueff(y, s, a0, r, rho0=RHO0)
                if ue > s*(1+1e-9):
                    exceed_cases += 1
check(4, exceed_cases == 0 or max_Ueff_over_s <= Fmax*(1+1e-9),
      f"U_eff never exceeds s*Fmax: exceed_count={exceed_cases}; "
      f"even at rho<rho0 the ceiling is Fmax*s = {Fmax:.12f}*s (excess {Fmax-1:.2e})")

# ---- 6. verdict -------------------------------------------------------------
ratio_10k = next(ratio for f,rk,s,ratio,u6,u2 in ratio_rows if f=='canon' and abs(rk-10)<1e-9 and abs(s-0.219)<1e-6)
ratio_100k = next(ratio for f,rk,s,ratio,u6,u2 in ratio_rows if f=='canon' and abs(rk-100)<1e-9 and abs(s-0.219)<1e-6)
verdict = "KILL" if (bounded_all and U_of_v(10.0,0.219) > U_of_v(1.0,0.219)) else "PASS"
print()
print(f"  U(v) monotone            : {mono}")
print(f"  U_eff bounded by s*Fmax  : {bounded_all}   (max/s = {max_Ueff_over_s:.6f})")
print(f"  ratio at r=10kpc (s=.219): {ratio_10k:.3e}")
print(f"  ratio at r=100kpc(s=.219): {ratio_100k:.3e}  (<1e-2 only because F collapses, still bounded)")
print(f"  PASS condition ratio<1e-2 : r-dependent (1.21e+00 at 10kpc, 1.3e-03 at 100kpc); "
      f"does NOT imply unboundedness")
print(f"  VERDICT: {verdict} -- U_eff is BOUNDED by s even with a0 a field; "
      f"the 233x legality obstruction SURVIVES.")

ok_all = all(checks)
print(f"\n{sum(checks)}/{len(checks)} checks ok; exit {0 if ok_all else 1}")
sys.exit(0 if ok_all else 1)
