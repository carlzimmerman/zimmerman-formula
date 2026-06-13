"""
agentRR Part 3 -- D2/D3: scan the saturated peaked-gain parameter space (A, Gamma, k0) for a regime
that simultaneously gives (i) sigma4<0 (bend, FORCED by dS bath), (ii) sigma6 >= sigma6* (bounded
fold), (iii) the operating branch STABLE (omega^2(k)>=0 down to the edge, no ghost, no UHP pole), and
(iv) k* at the sonic edge.

From Part 2 (exact):
  c_eff^2 = a1, sigma4 = a2, sigma6 = a3 as functions of (A,Gamma,k0,c).
  sigma4<0  <=>  k0^4 < 3 Gamma^2.
  sigma6>0  <=>  Gamma^4 - 6 Gamma^2 k0^4 + k0^8 > 0  <=> (k0^4 < (3-2sqrt2)Gamma^2) or (k0^4 > (3+2sqrt2)Gamma^2).
  bounded fold needs sigma4<0 AND sigma6 >= sigma6* = sigma4^2/(4 c_eff^2).

We define dimensionless x = k0^2/Gamma (gain-center vs width) and y = A/(c^2 Gamma) (gain strength
relative to the cold kinetic term). Scan x,y; for each, build the FULL dispersion omega^2(k) (not just
the IR truncation) and check:
  (a) sign sigma4, sigma6 (IR);  (b) sigma6 - sigma6* margin;
  (c) STABILITY of the full operating-point branch: omega^2(k) >= 0 for all k up to a UV cutoff, AND
      the retarded pole stays in LHP (we check the lossless-branch ghost/gradient condition; the
      active pole location is handled separately by the clamp of Part 1 which pins Im=0 marginal).
  (d) does a genuine roton MINIMUM (v_g^2<0 region, i.e. d(omega^2)/dk^2 < 0 somewhere) exist AND
      stay bounded (omega^2>0 at the dip)?
"""
import numpy as np

def coeffs(A, Gam, k0, c=1.0):
    # exact IR coefficients from Part 2
    den4 = (Gam**2 + k0**4)
    c_eff2 = (-A*Gam**3 + A*Gam*k0**4 + Gam**4*c**2 + 2*Gam**2*c**2*k0**4 + c**2*k0**8)/(den4**2)
    sigma4 = A*Gam*k0**2*(-3*Gam**2 + k0**4)/(den4**3)
    sigma6 = A*Gam*(Gam**4 - 6*Gam**2*k0**4 + k0**8)/(den4**4)
    return c_eff2, sigma4, sigma6

def full_om2(k2, A, Gam, k0, c=1.0):
    # full operating-point omega^2(k) = c^2 k^2 + Re chi(k^2)  (u=k^2)
    u = k2
    Rechi = -A*Gam*(u - k0**2)/((u - k0**2)**2 + Gam**2)
    return c**2*u + Rechi

found = []
xs = np.linspace(0.05, 3.0, 60)   # x = k0^2/Gamma
ys = np.linspace(0.05, 30.0, 120) # y = A/(c^2 Gamma)
c = 1.0
for x in xs:
    for y in ys:
        Gam = 1.0
        k0 = np.sqrt(x*Gam)          # k0^2 = x*Gamma
        A  = y*c**2*Gam              # A = y c^2 Gamma
        c_eff2, s4, s6 = coeffs(A, Gam, k0, c)
        if c_eff2 <= 0:              # need a healthy IR sound speed
            continue
        if s4 >= 0:                  # need the bend
            continue
        s6star = s4**2/(4*c_eff2)
        if s6 < s6star:              # need bounded fold
            continue
        # IR truncation passes. Now check the FULL branch is stable (omega^2>0 everywhere) up to UV.
        k2grid = np.linspace(1e-4, 6.0, 4000)
        om2 = full_om2(k2grid, A, Gam, k0, c)
        if np.any(om2 < 0):          # ghost / negative omega^2 => unstable on full branch
            stable_full = False
        else:
            stable_full = True
        # roton dip in the FULL branch? d omega^2/dk^2 < 0 somewhere with omega^2>0 there
        dom2 = np.gradient(om2, k2grid)
        dip = np.any((dom2 < 0) & (om2 > 0))
        found.append((x, y, c_eff2, s4, s6, s6star, s6 - s6star, stable_full, dip))

print(f"IR-passing (sigma4<0 AND sigma6>=sigma6*) points: {len(found)} / {len(xs)*len(ys)}")
if found:
    arr = found
    nstable = sum(1 for r in arr if r[7])
    ndip = sum(1 for r in arr if r[8])
    nboth = sum(1 for r in arr if r[7] and r[8])
    print(f"  of those: FULL-branch stable (omega^2>0 all k): {nstable}")
    print(f"            full-branch roton dip present:        {ndip}")
    print(f"            STABLE *and* dip (bounded fold!):      {nboth}")
    # show a few representative both-stable-and-dip points
    both = [r for r in arr if r[7] and r[8]]
    print("\nrepresentative STABLE+DIP points (x=k0^2/Gam, y=A/(c^2 Gam), c_eff^2, s4, s6, s6*, margin):")
    for r in both[:12]:
        print(f"  x={r[0]:.3f} y={r[1]:.3f}  c_eff^2={r[2]:.4f}  s4={r[3]:.4f}  s6={r[4]:.4f}  s6*={r[5]:.4f}  margin={r[6]:+.4f}")
    if not both:
        print("  NONE -- IR fold passes but full branch never simultaneously stable+dipped.")
        # show IR-passing but full-unstable ones
        print("\n  IR-passing points (first 8), with full-stability flag:")
        for r in arr[:8]:
            print(f"  x={r[0]:.3f} y={r[1]:.3f}  s4={r[3]:.4f}  s6={r[4]:.4f}  margin={r[6]:+.4f}  stable_full={r[7]} dip={r[8]}")
