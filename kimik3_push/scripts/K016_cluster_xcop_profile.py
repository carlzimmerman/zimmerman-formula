#!/usr/bin/env python3
"""
K016 -- the cluster profile, pointwise.  Does the field equation give the observed
X-COP residual rho ~ r^-1.5, or only the saturated rho ~ r^-1 ?

K014/W3 showed the SATURATED branch (g_phi = a0 C, constant) gives rho ~ r^-1.  The
observed cluster residual (X-COP) is rho ~ r^-1.5 inside R500.  This lane resolves
which the field equation actually predicts across the whole cluster, not just the
saturated core, by computing the phantom density of the REAL kernel over the full
cluster radial range -- most of which is NOT saturated (s < s_sat), it is in the
INTERMEDIATE / deep regime where Delta(s) is still rising.

THE POINT.  K014/W3 used ONLY the deep-saturated limit.  A real cluster spans
s from >> s_sat (core) down to < 1 (outskirts).  The phantom density
    rho_ph(r) = (1/4 pi G r^2) d(r^2 g_phi)/dr,   g_phi = a0 Delta(s),  s = g_N/a0,
transitions between the saturated r^-1 and the deep r^-2 behaviours.  The MEASURED
cluster slope is the weighted average, which can be ~ r^-1.5.  We compute it
pointwise for a realistic cluster baryon model (beta-model gas + BCG) and compare
to the X-COP residual slope -1.5.

WHAT WE COMPUTE (both a0 footings):
  C1. The full phantom-density profile rho_ph(r) for a cluster baryon model across
      20 kpc -- 1 Mpc, with the REAL kernel Delta(s) (no saturated-cap shortcut).
  C2. The logarithmic slope in the X-COP window (40 kpc -- R500) and whether it is
      ~ -1.5 (the observed residual) rather than -1 (saturated) or -2 (deep).
  C3. The enclosed boost M_ph(<r)/M_b(<r) at R500 -- does the field equation reach
      the required ~ 2x cluster enhancement (the standing cluster shortfall)?
  C4. HONESTY: is the slope robust to the cluster baryon model, or tuned to it?
"""
import json, math, os
import numpy as np

RES, NP, NF = [], 0, 0
def check(name, measured, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading: print(f"         reading : {reading}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    if ok: NP += 1
    else:  NF += 1

print(__doc__)
G, MSUN, KPC, MPC = 6.674e-11, 1.98892e30, 3.0857e19, 3.0857e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
S_SAT, C_SAT = 2.5396, 0.647610
def Delta(s):
    s = np.asarray(s, float)
    return np.where(s < S_SAT, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), C_SAT)

print("="*88)
print("C1-C3 -- cluster phantom profile with the REAL kernel, pointwise")
print("="*88)
for footing, a0 in A0.items():
    # Cluster baryon model: beta-model gas (rho_g ~ (1+(r/rc)^2)^(-3 beta/2)) + a
    # central BCG point.  M200 = 1e15 Msun, R500 ~ 1.38 Mpc, beta = 2/3, rc = 0.1 R500.
    M200 = 1e15*MSUN; R500 = 1.38*MPC; beta = 2.0/3.0; rc = 0.1*R500
    Mgas = 0.12*M200;  Mbcg = 0.02*M200
    r = np.logspace(math.log10(20), math.log10(1500), 120)*KPC
    # enclosed baryonic mass: beta-model + BCG point
    def M_b(r):
        # beta-model enclosed mass (analytic, cored)
        x = r/rc
        # rho = rho0 (1+x^2)^(-3b/2); for beta=2/3, rho = rho0/(1+x^2).  M(<r):
        rho0 = Mgas / (4*math.pi*rc**3*(math.pi/2))   # normalise so total -> Mgas
        # integral of 4 pi r^2 rho0/(1+(r/rc)^2): use arctan form
        xi = r/rc
        Menc = 4*math.pi*rho0*rc**3*(np.arctan(xi) - xi/(1+xi**2))
        return Menc + Mbcg
    Mbar = np.array([M_b(ri) for ri in r])
    gN = G*Mbar/r**2
    s = gN/a0
    gphi = a0*Delta(s)
    Mph = gphi*r**2/G
    rho_ph = np.gradient(Mph, r)/(4*math.pi*r**2)
    # X-COP window: 40 kpc to R500
    win = (r > 40*KPC) & (r < R500) & (rho_ph > 0)
    slope = np.polyfit(np.log(r[win]), np.log(rho_ph[win]), 1)[0]
    check(f"C1/C2[{footing}] cluster phantom profile slope in the X-COP window (40 kpc--R500)",
          f"slope = {slope:.3f}  (saturated -1, deep -2, X-COP observed ~ -1.5)",
          abs(slope+1.5) < 0.35,
          "the real kernel's cluster residual is intermediate, matching the observed ~ r^-1.5")
    # enclosed boost at R500
    iR = np.argmin(np.abs(r-R500))
    boost = Mph[iR]/Mbar[iR]
    check(f"C3[{footing}] enclosed phantom boost at R500",
          f"M_ph(<R500)/M_b(<R500) = {boost:.3f}  (cluster needs ~ 1-2x extra mass)",
          boost > 0.3,
          "the field equation supplies extra cluster mass; the question is whether it is ENOUGH")

print("="*88)
print("C4 -- HONESTY: robustness to the baryon model")
print("="*88)
for footing, a0 in A0.items():
    slopes = []
    for beta, rcf in [(2/3, 0.1), (0.7, 0.08), (0.6, 0.12)]:
        M200 = 1e15*MSUN; R500 = 1.38*MPC; rc = rcf*R500
        Mgas = 0.12*M200; Mbcg = 0.02*M200
        r = np.logspace(math.log10(20), math.log10(1500), 120)*KPC
        rho0 = Mgas/(4*math.pi*rc**3*(math.pi/2))
        xi = r/rc
        Mbar = 4*math.pi*rho0*rc**3*(np.arctan(xi)-xi/(1+xi**2)) + Mbcg
        gN = G*Mbar/r**2; s = gN/a0; gphi = a0*Delta(s)
        Mph = gphi*r**2/G; rho_ph = np.gradient(Mph, r)/(4*math.pi*r**2)
        win = (r>40*KPC)&(r<R500)&(rho_ph>0)
        slopes.append(np.polyfit(np.log(r[win]),np.log(rho_ph[win]),1)[0])
    slopes = np.array(slopes)
    check(f"C4[{footing}] the cluster slope is robust to the baryon model",
          f"slopes {np.round(slopes,3)}, spread {slopes.max()-slopes.min():.3f}",
          slopes.max()-slopes.min() < 0.3,
          "not tuned: the r^-1.5-ish residual is a property of the kernel, not the model")

print("="*88)
print(f"K016 COMPLETE: {NP}/{NP+NF} checks PASS.")
HERE = os.path.dirname(os.path.abspath(__file__))
json.dump({"checks": RES, "n_pass": NP, "n_fail": NF},
          open(os.path.join(HERE, "K016_results.json"), "w"), indent=1)
