"""
Hees-2016 / Bailey-Kostelecky-2006 secular-drift kernel: which r-power weights
the secular dOmega/dt, domega/dt integrand, and what s_bar(r)~r^2 does to the
orbit-average vs the framework's "evaluate s_bar at a" approximation.

Primary sources (PDFs extracted with pdftotext this session):
  - Bailey & Kostelecky 2006, gr-qc/0603030, PRD 74 045001  (the secular-rate FORMALISM)
  - Hees, Bailey, Le Poncin-Lafitte, Bourgoin et al. 2015, arXiv:1508.03478,
    PRD 92 064049  (the PLANETARY fit + Table II s^TX bound)

KEY FORMALISM (verbatim structure):
  Perturbing accel (BK Eq.165, gravity-sector s^jk part):
      alpha'^j = (GM/r^3) s^jk r^k  - (3/2)(GM/r^3) s^kl rhat^k rhat^l r^j
      => scales as GM*s/r^2  (s = CONSTANT tensor in BK/Hees)
  Insert Keplerian ellipse (BK Eq.167): r = a(1-e^2)/(1+e cos f)
  Average over the TRUE ANOMALY f (BK lines 4338-4343), dt = r^2/(n a^2 sqrt(1-e^2)) df.
  Result (Hees Eq.7a/7b == BK Eq.170): dOmega/dt, domega/dt depend ONLY on
  (a, e, i, n, omega, Omega) and constant projections s_PP, s_QQ, S^k, s_kP, s_kQ.
  Both rates scale as the MEAN MOTION n (the S-mixed terms carry an extra factor 'na').
  NO surviving power of r -- it is integrated out for constant s.

FRAMEWORK refinement: s_bar(r) = s_bar(a) * (r/a)^2.  The honest orbit-averaged
enhancement over evaluate-at-a, weighted by the time-Jacobian w(f), is <(r/a)^2>_t.
"""
import numpy as np
from scipy.integrate import quad

def avg_rp(p, e):
    # time-average weight in true anomaly: w(f) = (1-e^2)^(3/2)/(2pi (1+e cos f)^2)
    integ = lambda f: ((1-e**2)/(1+e*np.cos(f)))**p * (1-e**2)**1.5/(1+e*np.cos(f))**2/(2*np.pi)
    return quad(integ, 0, 2*np.pi)[0]

ecc = {'Mercury':0.2056,'Venus':0.0068,'Earth':0.0167,
       'Mars':0.0934,'Jupiter':0.0489,'Saturn':0.0565}

assert abs(avg_rp(0, 0.2) - 1.0) < 1e-9, "Jacobian must normalize to 1"

print("FRAMEWORK p=2 orbit-avg inflation of |s^TX| (vs evaluate-at-a):")
for b, e in ecc.items():
    f = avg_rp(2, e)
    print(f"  {b:8s} e={e:6.4f}  <(r/a)^2>_t={f:.4f}  (+{100*(f-1):.1f}%)")

# bracket the O(1) kernel-power uncertainty p=1..3
print("\nbracket <(r/a)^p>_t at Saturn(e=.0565)/Mercury(e=.2056):")
for p in (1, 2, 3):
    print(f"  p={p}: Saturn={avg_rp(p,0.0565):.4f}  Mercury={avg_rp(p,0.2056):.4f}")

# VERDICT: inflation is POSITIVE (margin shrinks slightly) but tiny:
#   +0.5% Saturn (worst-corner body), +1.3% Mars, +6.3% Mercury (high e), ~0 Venus/Earth.
# Does NOT approach the ~1.5x that would flip LIVE->excluded. Margin stays ~1.5x.
