#!/usr/bin/env python3
"""L181 -- the Hubble-kernel growth equation (L180) against DESI DR1 full-shape growth measurements.
Data: DESI 2024 V (arXiv:2411.12021), Table 9, ShapeFit f sigma_s8 / (f sigma_s8)_fid per redshift bin (fiducial = Planck-2018 LCDM),
MAP with 68% intervals, both the ShapeFit-only and the ShapeFit+BAO sub-panels; errors symmetrised as the mean of the two sides.
Model: ratio = fsigma8_eq(z)/fsigma8_LCDM(z) from the L180 growth ODE with G_eff/G = nu(cH(z)/a0), both footings. Also the DESI
modified-gravity parameter mu0 = 0.05 +/- 0.22 (arXiv:2411.12026, DESI+CMB+DESY3+SN) against the equation's G_eff/G - 1 today.
No literal-True checks."""
import numpy as np
from scipy.integrate import solve_ivp
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""))
h = 0.6736; Om = 0.3138; OL = 1 - Om; c = 2.998e8; H0 = 100*h*1e3/3.0857e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
E = lambda a: np.sqrt(Om*a**-3 + OL); nu = lambda x: 1.0/(1.0 - np.exp(-np.sqrt(x)))
def growth(geff):
    rhs = lambda l, y: [y[1], 1.5*(Om*np.exp(l)**-3/E(np.exp(l))**2)*geff(np.exp(l))*y[0] - (2 - 1.5*Om*np.exp(l)**-3/E(np.exp(l))**2)*y[1]]
    ls = np.linspace(np.log(1/101), 0, 800); s = solve_ivp(rhs, [ls[0], 0], [1.0, 1.0], t_eval=ls, rtol=1e-9, atol=1e-12)
    return np.exp(ls), s.y[0], s.y[1]/s.y[0]
a_, D_L, f_L = growth(lambda a: 1.0)
def ratio(foot, z):
    r0 = c*H0/A0[foot]; a_, D, f = growth(lambda a: nu(r0*E(a))); i = np.argmin(abs(a_ - 1/(1+z)))
    return (f[i]*D[i])/(f_L[i]*D_L[i])
# DESI DR1 Table 9: (tracer, z_eff, ShapeFit-only ratio, +err, -err, ShapeFit+BAO ratio, +err, -err)
D = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
     ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084),
     ("ELG2", 1.317, 0.95, 0.11, 0.08, 0.945, 0.097, 0.077), ("QSO", 1.491, 1.16, 0.12, 0.12, 1.16, 0.12, 0.12)]
print("    DESI DR1 ShapeFit f sigma_s8/(f sigma_s8)_fid (Table 9) vs the equation's ratio to Planck-LCDM")
print(f"    {'bin':<5} {'z':>5} {'SF-only':>14} {'SF+BAO':>14} {'eq canon':>9} {'eq alt':>7}")
chi = {k: 0.0 for k in ("LCDM|SF", "canon|SF", "alt|SF", "LCDM|SFB", "canon|SFB", "alt|SFB")}
for t, z, r1, p1, m1, r2, p2, m2 in D:
    rc, ra = ratio("canonical", z), ratio("alt", z); e1 = 0.5*(p1 + m1); e2 = 0.5*(p2 + m2)
    for lab, mod in (("LCDM", 1.0), ("canon", rc), ("alt", ra)):
        chi[f"{lab}|SF"] += ((r1 - mod)/e1)**2; chi[f"{lab}|SFB"] += ((r2 - mod)/e2)**2
    print(f"    {t:<5} {z:5.3f} {r1:6.3f} +{p1:.3f}-{m1:.3f} {r2:6.3f} +{p2:.3f}-{m2:.3f} {rc:9.3f} {ra:7.3f}")
print("    chi^2 over 6 bins: " + ", ".join(f"{k}: {v:.2f}" for k, v in chi.items()))
dSF = chi["canon|SF"] - chi["LCDM|SF"]; dSFB = chi["canon|SFB"] - chi["LCDM|SFB"]
check("D1 the equation is consistent with DESI DR1 growth: chi^2 per bin below 1.5 on both footings and both sub-panels",
      all(chi[k]/6 < 1.5 for k in chi if not k.startswith("LCDM")), f"chi^2/6: canon SF {chi['canon|SF']/6:.2f}, SF+BAO {chi['canon|SFB']/6:.2f}; alt SF {chi['alt|SF']/6:.2f}, SF+BAO {chi['alt|SFB']/6:.2f}")
check("D2 DESI DR1 cannot yet discriminate the equation from LCDM: |delta chi^2| < 1 on both sub-panels (10-20% errors vs a 1-4% effect)",
      abs(dSF) < 1 and abs(dSFB) < 1, f"delta chi^2 (canon - LCDM): SF {dSF:+.2f}, SF+BAO {dSFB:+.2f}; alt: SF {chi['alt|SF']-chi['LCDM|SF']:+.2f}, SF+BAO {chi['alt|SFB']-chi['LCDM|SFB']:+.2f}")
mu0 = {f: nu(c*H0/A0[f]) - 1 for f in A0}
print(f"    DESI mu0 = 0.05 +/- 0.22 (2411.12026, DESI+CMB+DESY3+SN) vs the equation's G_eff/G - 1 today: canonical {mu0['canonical']:.3f}, alt {mu0['alt']:.3f}")
check("D3 the equation's present-day coupling excess sits within 0.3 sigma of DESI's mu0 on both footings", all(abs(v - 0.05)/0.22 < 0.3 for v in mu0.values()),
      ", ".join(f"{f}: {(v-0.05)/0.22:+.2f} sigma" for f, v in mu0.items()))
print("    Precision needed to test the equation at 3 sigma at z ~ 0.3-0.6: ~1% on f sigma8 (DESI DR1: 10-19%; DESI final ~ 1-2%).")
print(f"\nL181 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
