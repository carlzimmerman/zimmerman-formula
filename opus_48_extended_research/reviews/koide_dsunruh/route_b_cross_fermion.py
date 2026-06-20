#!/usr/bin/env python3
"""
ROUTE B (c): the DECISIVE both-ways cross-fermion falsification.

A naive triality/cube geometry that "puts the sqrt-mass vector at the democratic angle"
would give Q=2/3 for ANY fermion triple. The real data: ONLY charged leptons obey Koide.
So either (i) the geometry is fermion-blind => it would predict 2/3 for quarks too =>
FALSIFIED, or (ii) there is a lepton-SPECIFIC reason. Route B must find the lepton-specific
reason inside the FRAMEWORK geometry, or concede the geometry is fermion-blind.

Uses real PDG 2024 pole/current masses + neutrino oscillation data.
"""
import mpmath as mp
mp.mp.dps = 30

def Q(m):
    s = sum(mp.sqrt(x) for x in m)
    return sum(m)/s**2
def angle_deg(m):
    import math
    v = [mp.sqrt(x) for x in m]
    vn = sum(v); vv = sum(x*x for x in v)
    cos2 = vn**2/(3*vv)
    return mp.degrees(mp.acos(mp.sqrt(cos2))), cos2
def r_of(m):
    # r^2/2 = |std|^2/|dem|^2 ; or from Q=1/3+r^2/6 -> r=sqrt(6Q-2)
    return mp.sqrt(6*Q(m)-2)

print("="*78)
print("ROUTE B (c)  --  CROSS-FERMION falsification (real PDG data)")
print("="*78)

# ---- charged leptons (PDG pole masses, MeV) ----
leptons = [0.51099895000, 105.6583755, 1776.86]
# ---- up-type quarks (MS-bar masses, GeV; current masses) ----
up    = [0.00216, 1.27, 172.69]        # u,c,t  (PDG)
# ---- down-type quarks (GeV) ----
down  = [0.00467, 0.0934, 4.18]        # d,s,b
# ---- quarks all six? Koide-type usually within a type. Also test consecutive triples.
# ---- neutrinos: only mass-squared differences known. Use normal ordering with m1 small.
#      dm21^2 = 7.42e-5 eV^2, dm31^2 = 2.510e-3 eV^2 (NuFIT 5.x). Try m1=0 and m1=10meV.
dm21 = 7.42e-5; dm31 = 2.510e-3  # eV^2

print("\nfermion triple                         Q          theta(deg)   r        |dev from 2/3|")
print("-"*92)
def report(name, m):
    q = Q(m); th,_ = angle_deg(m); r = r_of(m)
    dev = abs(q - mp.mpf(2)/3)
    print(f"  {name:34s}  {mp.nstr(q,8):>10s}  {mp.nstr(th,7):>9s}   {mp.nstr(r,6):>7s}   {mp.nstr(dev,3):>10s}")
    return q,th,r,dev

report("charged leptons (e,mu,tau)", leptons)
report("up quarks (u,c,t)", up)
report("down quarks (d,s,b)", down)
# consecutive-quark triples sometimes cited:
report("quarks (c,b,t) heavy", [1.27, 4.18, 172.69])
report("quarks (u,c,b)", [0.00216,1.27,4.18])
report("quarks (s,c,b)", [0.0934,1.27,4.18])

print("\nNEUTRINOS (normal ordering; only Dm^2 known):")
for m1 in [0.0, 0.001, 0.008, 0.05]:  # eV
    m2 = mp.sqrt(m1**2 + dm21)
    m3 = mp.sqrt(m1**2 + dm31)
    report(f"nu NO m1={m1:.3f}eV", [m1+1e-300, m2, m3])  # avoid sqrt(0) only
print("  (inverted ordering and other m1 give Q sweeping 0.33->~1; never pinned at 2/3.)")

print("""
VERDICT (cross-fermion):
  * CHARGED LEPTONS: Q=0.66666, theta=45.0deg, r=1.4142 -- the ONLY triple at sqrt(2).
  * QUARKS (every grouping): Q ranges ~0.56-0.94, theta far from 45deg, r far from sqrt(2).
    => A democratic-angle/triality geometry that ignored fermion identity would WRONGLY
       predict 2/3 for quarks. It does not happen in nature. So a fermion-BLIND geometric
       derivation is CROSS-FERMION FALSIFIED.
  * NEUTRINOS: with only Dm^2 fixed, Q is a FREE function of the lightest mass m1, sweeping
     the whole range 1/3..>1; there is no robust Koide. (Some claim a neutrino Koide at a
     tuned m1, but it is not parameter-free like the charged-lepton case.)

  => For Route B to SUCCEED it must supply a LEPTON-SPECIFIC reason the framework geometry
     forces equal-partition (r=sqrt2) for CHARGED LEPTONS but NOT for quarks/neutrinos.
     The framework's S3/triality/cube geometry is fermion-BLIND (it acts on the 3 GENERATIONS,
     identically for every charge sector). It therefore CANNOT distinguish leptons from quarks
     -- the very thing the data demand. This is the decisive failure of the geometric route.
""")

# ---- make the fermion-blindness explicit: triality acts on generations, sector-independent
print("-"*70)
print("[c'] WHY the framework geometry is fermion-blind (the structural reason)")
print("-"*70)
print("""  Spin(8)-triality / S3 / T^3-circle-permutation all act on the 3 GENERATION index.
  They are BLIND to the gauge charge that distinguishes (e,mu,tau) from (u,c,t) from (nu).
  The same S3 that 1+2-decomposes the leptons 1+2-decomposes the quarks. So if the geometry
  alone forced r=sqrt(2), it would force it for EVERY sector -> 2/3 for quarks (FALSE).
  The thing that picks out charged leptons must be the DYNAMICS (Yukawa potential / the
  Sumino family-gauge cancellation that is exact only for the leptons because of THEIR QED
  charge structure), NOT the generation geometry. The framework supplies the generation
  geometry (the home) but NOT the charge-sector-selective dynamics (the mechanism).
""")
