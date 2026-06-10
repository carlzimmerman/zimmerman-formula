#!/usr/bin/env python3
"""
Verification for MI_BATH_TAIL_CONSTRAINT.md (trilemma calculation #1, the bath-inertia kernel's two limits).
Checks, with sympy where symbolic and numpy where numeric:
  (1) mu(x) = [sqrt(x^2+1)-1]/x limits: deep x<<1 -> x/2 (=> a0_bath = 2cH); high x>>1 -> 1 - 1/x + 1/(2x^2).
  (2) The high-a EOM mu(a)*a = g_N  =>  a = g_N + cH + O((cH)^2/g_N): the constant-cH anomaly, exact root vs asymptote.
  (3) Saturn numbers, BOTH footings (rho_DE: cH_L = Z*a0_fw; rho_total: cH_0) -- the kill must be footing-robust.
  (4) The quadratic-tail alternative mu = 1 - (cH)^2/(2a^2): delta_a(Saturn) -- must come out SAFE (~2e-15).
  (5) a0_bath / a0_framework = 2Z check.
Inline, no swarms.  C. Zimmerman 2026-06-10.
"""
import numpy as np, sympy as sp

# ---------- (1) symbolic limits ----------
x = sp.symbols('x', positive=True)
mu = (sp.sqrt(x**2 + 1) - 1)/x
deep = sp.series(mu, x, 0, 4).removeO()
high = sp.series(mu.subs(x, 1/sp.symbols('u', positive=True)), sp.symbols('u', positive=True), 0, 3)
print("mu(x) deep-MOND series (x->0):", sp.simplify(deep), "   [expect x/2 leading]")
u = sp.symbols('u', positive=True)
high = sp.series(((sp.sqrt(1/u**2 + 1) - 1)*u), u, 0, 3).removeO()   # mu in terms of u=1/x
print("mu(x) high-a series (u=1/x->0):", sp.expand(high), "   [expect 1 - u + u^2/2]")

# ---------- constants ----------
c = 2.998e8
a0_fw = 9.36e-11                  # framework a0 (rho_DE footing)
Z = np.sqrt(32*np.pi/3)           # 5.789
cH_L = Z * a0_fw                  # = c * H_Lambda (rho_DE footing)
H0 = 2.184e-18; cH_0 = c * H0     # rho_total footing
GMsun = 1.327e20
r_sat = 9.58 * 1.496e11
gN_sat = GMsun / r_sat**2
print(f"\ncH (rho_DE footing)   = {cH_L:.3e} m/s^2")
print(f"cH (rho_total footing)= {cH_0:.3e} m/s^2")
print(f"g_N(Saturn)           = {gN_sat:.3e} m/s^2")
print(f"a0_bath = 2cH         = {2*cH_L:.3e} (rho_DE) / {2*cH_0:.3e} (rho_total)")
print(f"a0_bath / a0_framework= {2*cH_L/a0_fw:.2f}   [expect 2Z = {2*Z:.2f}]")

# ---------- (2,3) exact root of mu(a)*a = g_N at Saturn ----------
def anomaly(cH, gN):
    # mu(a)*a = sqrt(a^2 + cH^2) - cH = gN  =>  a = sqrt((gN + cH)^2 - cH^2)... solve exactly:
    # sqrt(a^2+cH^2) = gN + cH  =>  a^2 = gN^2 + 2 gN cH  =>  a = gN sqrt(1 + 2cH/gN)
    a = gN*np.sqrt(1 + 2*cH/gN)
    return a - gN
for lab, cH in [("rho_DE", cH_L), ("rho_total", cH_0)]:
    da = anomaly(cH, gN_sat)
    print(f"\n[{lab}] exact anomalous accel at Saturn = {da:.3e} m/s^2   [asymptote cH = {cH:.3e}]")
    for bound in (1e-12, 1e-13, 1e-14):
        print(f"   vs ephemeris bound {bound:.0e}: excess x{da/bound:,.0f}  ({np.log10(da/bound):.1f} orders)")

# ---------- (4) quadratic-tail alternative ----------
for lab, cH in [("rho_DE", cH_L), ("rho_total", cH_0)]:
    da2 = cH**2/(2*gN_sat)
    print(f"[{lab}] quadratic-tail delta_a(Saturn) = {da2:.3e} m/s^2   [SAFE if < 1e-14]")

print("""
READING: deep-MOND emerges (mu -> x/2) but a0_bath = 2cH misses SPARC by 2Z ~ 11.6x; the high-a tail gives a
constant ~cH anomaly, 3.5-4.5 orders over the ephemeris bounds (footing-robust, both ways); the quadratic tail
passes. => viable kernels need mu-1 = o(cH/a); both the coefficient and the tail pinch the Step-4 coupling.
Kills THIS ansatz, not the class. See MI_BATH_TAIL_CONSTRAINT.md.""")
