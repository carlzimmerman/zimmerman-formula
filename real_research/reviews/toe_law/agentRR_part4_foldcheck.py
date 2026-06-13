"""
agentRR Part 4 -- does the saturated peaked-gain dispersion ACTUALLY fold, or does the IR truncation
lie? Part 3 found sigma4<0, sigma6>=sigma6* (IR says "bounded fold") but the FULL branch shows NO dip.
Resolve this honestly: compare the truncated omega^2 = c_eff^2 k^2 + sigma4 k^4 + sigma6 k^6 against
the FULL omega^2 = c^2 k^2 + Re chi, and find where (if anywhere) a roton minimum lives.

A roton MINIMUM in omega^2(k) needs d(omega^2)/dk^2 = 0 with a sign change (down then up) at finite k,
with omega^2>0 there. Equivalent: v_g^2 = d(omega^2)/dk^2 dips below the IR sound speed c_eff^2 and
ideally below 0 (a true non-monotone fold), but stays positive in omega^2 (bounded).
"""
import numpy as np
import sympy as sp

def full_om2(u, A, Gam, k0, c=1.0):
    Rechi = -A*Gam*(u - k0**2)/((u - k0**2)**2 + Gam**2)
    return c**2*u + Rechi

def trunc_om2(u, ceff2, s4, s6):
    return ceff2*u + s4*u**2 + s6*u**3

def coeffs(A, Gam, k0, c=1.0):
    den4 = (Gam**2 + k0**4)
    c_eff2 = (-A*Gam**3 + A*Gam*k0**4 + Gam**4*c**2 + 2*Gam**2*c**2*k0**4 + c**2*k0**8)/(den4**2)
    sigma4 = A*Gam*k0**2*(-3*Gam**2 + k0**4)/(den4**3)
    sigma6 = A*Gam*(Gam**4 - 6*Gam**2*k0**4 + k0**8)/(den4**4)
    return c_eff2, sigma4, sigma6

# Pick a representative IR-fold point from Part 3 with a big margin
x, y = 0.05, 0.805
Gam, c = 1.0, 1.0
k0 = np.sqrt(x*Gam); A = y*c**2*Gam
ceff2, s4, s6 = coeffs(A, Gam, k0, c)
print(f"point x={x} y={y}: c_eff^2={ceff2:.5f}  s4={s4:.5f}  s6={s6:.5f}  s6*={s4**2/(4*ceff2):.5f}")

# IR truncation: where does the truncated cubic-in-u dip? d/du = ceff2 + 2 s4 u + 3 s6 u^2 = 0
# v_g^2(u) = ceff2 + 2 s4 u + 3 s6 u^2 ; min at u_m = -s4/(3 s6); value there:
u_m = -s4/(3*s6)
vg2_min_trunc = ceff2 + 2*s4*u_m + 3*s6*u_m**2
print(f"\nIR-truncation: v_g^2 minimum at u_m={u_m:.5f} (k={np.sqrt(u_m):.4f}), v_g^2_min={vg2_min_trunc:.6f}")
print("  (v_g^2_min < 0 => truncation predicts a TRUE fold; >0 => only a softening, no fold)")

# But does the FULL dispersion fold? compute v_g^2 = d omega^2/du on the full thing analytically.
uu = sp.symbols('u', real=True, positive=True)
Av, Gv, k0v = sp.Rational(805,1000), sp.Integer(1), sp.sqrt(sp.Rational(5,100))
# careful: A=y=0.805, Gam=1, k0^2=0.05
Av = sp.Float(A); Gv = sp.Float(Gam); k0v = sp.Float(k0)
om2_full_sym = c**2*uu + (-Av*Gv*(uu - k0v**2)/((uu - k0v**2)**2 + Gv**2))
vg2_full = sp.diff(om2_full_sym, uu)
# find real roots of vg2_full = 0 for u>0
roots = sp.solve(sp.Eq(sp.numer(sp.together(vg2_full)), 0), uu)
realroots = [complex(r) for r in roots]
realpos = [r.real for r in realroots if abs(r.imag)<1e-9 and r.real>0]
print(f"\nFULL dispersion: v_g^2=0 real positive roots in u: {sorted(realpos)}")
if realpos:
    for ur in sorted(realpos):
        print(f"   at u={ur:.5f} (k={np.sqrt(ur):.4f}): omega^2={full_om2(ur,A,Gam,k0,c):.5f}, "
              f"v_g^2_min_full={float(vg2_full.subs(uu,ur)):.6f}")
else:
    print("   NONE -- the full saturated-gain branch is MONOTONE (v_g^2>0 everywhere): NO fold.")

# Direct numeric: minimum of full v_g^2 over u>0
ug = np.linspace(1e-4, 3.0, 200000)
om2f = full_om2(ug, A, Gam, k0, c)
vg2f = np.gradient(om2f, ug)
imin = np.argmin(vg2f)
print(f"\nnumeric full v_g^2 minimum over u in (0,3): {vg2f[imin]:.6f} at u={ug[imin]:.5f} (omega^2={om2f[imin]:.5f})")
print("  => if this is >0, NO fold in the full branch despite IR sigma4<0,sigma6>0.")

# Why: compare truncation radius of convergence. The Re chi has poles at u = k0^2 +/- i Gam, |u|~sqrt(k0^4+Gam^2)~Gam.
# So the IR series converges only for |u| < ~Gam=1. The fold the IR predicts sits at u_m -- is it inside?
print(f"\nIR series radius ~ |u_pole| = sqrt(k0^4+Gam^2) = {np.sqrt(k0**4+Gam**2):.4f}")
print(f"IR-predicted fold location u_m = {u_m:.4f}  -> inside radius? {u_m < np.sqrt(k0**4+Gam**2)}")
