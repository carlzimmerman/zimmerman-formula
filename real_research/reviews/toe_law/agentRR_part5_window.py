"""
agentRR Part 5 -- the REAL bounded-fold window, and whether saturated gain reaches it.

Part 4 showed: sigma6 >= sigma6* = sigma4^2/(4 c_eff^2) is the NO-GHOST (omega^2>0) threshold, NOT
the fold-EXISTENCE threshold. A *visible* roton fold needs v_g^2 = d(omega^2)/dk^2 < 0 somewhere.
With omega^2 = c^2 u + s4 u^2 + s6 u^3 (u=k^2):
  v_g^2(u) = c^2 + 2 s4 u + 3 s6 u^2,  minimized at u_m = -s4/(3 s6) (needs s4<0,s6>0),
  v_g^2_min = c^2 - s4^2/(3 s6).
  => v_g^2_min < 0 (TRUE FOLD)  <=>  s6 < s4^2/(3 c^2) =: s6_fold.
  => omega^2(u)>0 with no ghost at the inflection (BOUNDED)  <=>  s6 > s6* = s4^2/(4 c^2).
So a BOUNDED, VISIBLE fold requires the WINDOW
     s6* = s4^2/(4c^2)  <  s6  <  s4^2/(3c^2) = s6_fold.
i.e. ratio s6/s6* must lie in (1, 4/3). A NARROW window: s6 only ~33% above threshold.

Now: where does the SATURATED PEAKED gain land? Its s6/s6* is fixed by the geometry (x=k0^2/Gam, y).
Scan and ask: does the saturated gain EVER land in (1, 4/3)? And is the landing FORCED or tunable?
"""
import numpy as np

def coeffs(A, Gam, k0, c=1.0):
    den4 = (Gam**2 + k0**4)
    c_eff2 = (-A*Gam**3 + A*Gam*k0**4 + Gam**4*c**2 + 2*Gam**2*c**2*k0**4 + c**2*k0**8)/(den4**2)
    sigma4 = A*Gam*k0**2*(-3*Gam**2 + k0**4)/(den4**3)
    sigma6 = A*Gam*(Gam**4 - 6*Gam**2*k0**4 + k0**8)/(den4**4)
    return c_eff2, sigma4, sigma6

print("WINDOW for a bounded VISIBLE fold:  1 < s6/s6* < 4/3")
print("(below 1 => ghost/unbounded; above 4/3 => no v_g^2<0, only softening, NO fold)\n")

Gam, c = 1.0, 1.0
in_window = []
xs = np.linspace(0.01, 3.0, 300)
ys = np.linspace(0.01, 200.0, 600)
total_irfold = 0
for x in xs:
    for y in ys:
        k0 = np.sqrt(x*Gam); A = y*c**2*Gam
        ceff2, s4, s6 = coeffs(A, Gam, k0, c)
        if ceff2 <= 0 or s4 >= 0 or s6 <= 0:
            continue
        s6star = s4**2/(4*ceff2)
        s6fold = s4**2/(3*ceff2)
        ratio = s6/s6star            # = 4/3 * s6/s6fold
        if s6 >= s6star:
            total_irfold += 1
        if s6star < s6 < s6fold:     # the genuine bounded-fold window
            in_window.append((x, y, ratio, ceff2, s4, s6))

print(f"points with sigma4<0 & sigma6>=sigma6* (IR no-ghost): {total_irfold}")
print(f"points in the GENUINE bounded-fold window (1<ratio<4/3): {len(in_window)}")
if in_window:
    rr = np.array([w[2] for w in in_window])
    print(f"  ratio range in window: {rr.min():.4f} .. {rr.max():.4f}")
    print("  sample in-window points (x=k0^2/Gam, y=A/(c^2 Gam), s6/s6*):")
    for w in in_window[:10]:
        print(f"    x={w[0]:.3f} y={w[1]:.3f}  ratio={w[2]:.4f}")
else:
    print("  NONE in scan grid. Let's find the MIN ratio s6/s6* the saturated gain can produce.")

# find the global min of s6/s6* over the active-bend region (s4<0)
best = (1e9, None)
for x in np.linspace(0.001, 5.0, 2000):
    for y in np.linspace(0.001, 500.0, 400):
        k0=np.sqrt(x*Gam); A=y*c**2*Gam
        ceff2,s4,s6 = coeffs(A,Gam,k0,c)
        if ceff2<=0 or s4>=0 or s6<=0: continue
        s6star=s4**2/(4*ceff2)
        ratio=s6/s6star
        if ratio < best[0]:
            best=(ratio,(x,y,ceff2,s4,s6,s6star))
print(f"\nGLOBAL MIN of s6/s6* over the active-bend (s4<0) saturated-gain family: {best[0]:.5f}")
print(f"   at {best[1]}")
print(f"   bounded-fold window is (1, 1.3333). Min achievable ratio = {best[0]:.4f}.")
if best[0] < 4/3:
    print("   => the saturated gain CAN dip into the window (ratio < 4/3 reachable).")
else:
    print("   => the saturated gain CANNOT reach the window (ratio always >= 4/3): NO fold, ever.")
