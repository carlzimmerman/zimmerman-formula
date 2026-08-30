#!/usr/bin/env python3
"""KM-X1 DOOR #1: the acceleration-dependent 1PN. Can the running alpha(a) of the generalized-
khronometric MOND theory leave a residual at Solar-System accelerations that CANCELS the 4*alpha_inf
term GW170817 forces (KM-X1: beta=0 => alpha_1=4*alpha)? If yes the finite-alpha_inf route reopens.
Uses the in-repo derived running chi(y)=alpha_inf+(2-alpha_inf)e^{-y} (the a-dependent preferred-frame
coefficient that yields mu=1-e^{-y}). All checks sympy-exact + physical numerics."""
import sympy as sp

# ---------------------------------------------------------------- LINK 1: what acceleration runs?
print("=== LINK 1: the khronon congruence acceleration in the weak-field static limit ===")
Us, dU = sp.symbols('U dU', real=True)                # potential and its gradient d_i U (weak field)
# static observer u^mu=(1/sqrt(-g00),0,0,0), g00=-(1+2U); acceleration a_i = d_i ln sqrt(-g00)
# = (1/2) d_i ln(1+2U) = dU/(1+2U):
a_i = dU/(1 + 2*Us)
a_i_lin = sp.series(a_i, Us, 0, 1).removeO()          # linearize in U (weak field)
print(f"   a_i = d_i ln sqrt(-g00) = dU/(1+2U) = {a_i}")
print(f"       -> weak-field (U<<1): a_i = {a_i_lin}  = d_i U")
print("   => the acceleration entering f(a) IS the local gravitational field g = |grad U|.")

# ---------------------------------------------------------------- LINK 2: y = g/a0 in the solar system
print("\n=== LINK 2: y = g_local/a0 at the sites of the preferred-frame tests ===")
GM_sun = 1.32712e20        # m^3/s^2
AU = 1.495978707e11        # m
a0 = 1.2e-10               # m/s^2  (standard MOND a0; the 9.36e-11 gives an even larger y)
import math
for name, r_AU in [("Mercury",0.39),("Earth/LLR",1.0),("Saturn/Cassini",9.5),("Neptune",30.0),("Sun MOND-radius",7200.0)]:
    g = GM_sun/(r_AU*AU)**2
    y = g/a0
    print(f"   {name:16s} r={r_AU:7.2f}AU  g={g:.3e} m/s^2   y=g/a0={y:.3e}")

# ---------------------------------------------------------------- LINK 3: the running coupling
print("\n=== LINK 3: the running chi(y)=alpha_inf+(2-alpha_inf)e^{-y} — sign & monotonicity ===")
y, ainf = sp.symbols('y alpha_inf', positive=True)
chi = ainf + (2 - ainf)*sp.exp(-y)
print(f"   chi(y) = {chi}")
print(f"   chi(inf) = {sp.limit(chi, y, sp.oo)}   (asymptotic khronometric coupling = alpha_inf)")
print(f"   chi'(y)  = {sp.simplify(sp.diff(chi, y))}   (<0 for alpha_inf<2: chi DECREASES to alpha_inf from ABOVE)")
excess = sp.simplify(chi - ainf)
print(f"   chi(y) - alpha_inf = {excess}  >0 for all finite y  => chi(y) NEVER dips below alpha_inf,")
print("        so it NEVER reaches 0 at finite y unless alpha_inf<=0 (excluded). NO cancellation zero.")

# ---------------------------------------------------------------- LINK 4: alpha_1 at solar-system a
print("\n=== LINK 4: alpha_1(solar) = 4*chi(y_solar) on the c_T=1 slice (beta=0) ===")
# KM-X1: at beta=0, alpha_1 = 4*alpha ; with running, alpha -> chi(y_local)
alpha1 = 4*chi
print(f"   alpha_1(y) = 4*chi(y) = {sp.expand(alpha1)}")
print(f"             = 4*alpha_inf + 4*(2-alpha_inf)*e^{{-y}}")
print("   The correction to 4*alpha_inf is 4(2-alpha_inf)e^{-y} — POSITIVE and exponentially small.")
# numeric correction size at the tightest test site (Earth/LLR, y~5e7)
y_earth = (GM_sun/AU**2)/a0
corr_log10 = float(-y_earth/math.log(10))
print(f"   at Earth (y={y_earth:.2e}):  e^{{-y}} ~ 10^({corr_log10:.2e})  = utterly negligible")
print("   even derivative-of-coupling 1PN terms ~ chi'(y),chi''(y) ~ e^{-y}: same exponential floor.")

# ---------------------------------------------------------------- VERDICT
print("\n=== DOOR #1 VERDICT ===")
print("The running is evaluated at the LOCAL gravitational acceleration (LINK 1), which in every")
print("preferred-frame test site is y=g/a0 >~ 1e4..1e8 (LINK 2). On the in-repo running chi(y), the coupling")
print("sits on its asymptotic plateau chi=alpha_inf + (2-alpha_inf)e^{-y} (LINK 3): the excess over")
print("alpha_inf is POSITIVE and ~e^{-y}, so it can neither cancel nor even dent 4*alpha_inf (LINK 4).")
print("=> alpha_1(solar) = 4*alpha_inf to ~1 part in 10^(1e7). The GW170817-forced bound alpha_inf<2e-7")
print("   STANDS. Door #1 does NOT reopen the finite-alpha_inf window. The escape a MOND running could")
print("   provide is killed by the exponential plateau: MOND corrections are ~e^{-g/a0}, and the tests")
print("   live where g>>a0.")
print('CERTIFICATE_JSON: {"gate":"KM-X1-door1","status":"KILL","certificate":"Acceleration-dependent '
      '1PN does NOT rescue finite alpha_inf. Running coupling chi(y)=alpha_inf+(2-alpha_inf)e^{-y} is '
      'evaluated at the LOCAL field g (a_mu=grad U in weak field), and all preferred-frame tests sit at '
      'y=g/a0=1e4..1e8 where chi=alpha_inf+O(e^{-y}), excess POSITIVE => no cancellation of the 4alpha_inf '
      'that beta=0 forces. alpha_1(solar)=4alpha_inf to 1 part in 10^{1e7}; bound alpha_inf<2e-7 stands.",'
      '"numeric_values":{"y_earth":5e7,"correction":"e^{-5e7}"},'
      '"assumptions":["a_mu=grad U weak-field static (verified)","chi(y) = in-repo derived running",'
      '"preferred-frame tests at high g (LLR/Cassini/ephemeris)","asymptotic-khronometric alpha_1=4alpha from KM-X1"]}')
