#!/usr/bin/env python3
"""
PROJECT 11: the joint forward-model fit -- the HONEST significance of rising a0.
================================================================================
framework_vs_siv.py fit the 3-point a0(z) compilation with a plain chi2 and got framework >> constant >>
SIV. This file does it RIGHT: it marginalizes the gas/pressure systematic that grows with z (the confound
that wrecks high-z dynamical masses), and it leave-one-out tests the single z=0.9 point the result leans
on. The deliverable is the honest, systematic-aware significance -- which is real but modest, motivating the
many-point compilation (#10). Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def siv(z):
    num = (1-Om)/(1+z)**1.5 + Om
    return (1+z)**-1.5 * num**(-4/3) / ((1-Om)+Om)**(-4/3)


MODELS = {"framework (rises)": E, "constant": lambda z: 1+0*z, "SIV (falls)": siv}
# a0(z) compilation [1e-10]: SPARC z=0; Varasteanu 2025 z=0.05; MUSE-DARK III 2026 z=0.9
Z = np.array([0.0, 0.05, 0.9]); A = np.array([1.36, 1.69, 2.38]); S = np.array([0.20, 0.13, 0.11])


def fit(f, extra=0.0, drop=None):
    z, a, s = Z, A, np.sqrt(S**2 + (extra*Z)**2)        # gas/pressure systematic: sigma_sys = extra*z
    if drop is not None:
        k = np.arange(len(z)) != drop; z, a, s = z[k], a[k], s[k]
    fz = f(z); amp = np.sum(a*fz/s**2)/np.sum(fz**2/s**2)
    return np.sum(((a-amp*fz)/s)**2)


def main():
    print("#"*92); print("# PROJECT 11 -- forward-model fit with marginalized gas/pressure systematic"); print("#"*92 + "\n")
    print("="*92); print("THE FIT (chi2; lower is better)"); print("="*92)
    print(f"  {'model':20}{'no sys':>10}{'+gas/press':>13}{'drop z=0.9':>13}")
    for n, f in MODELS.items():
        print(f"  {n:20}{fit(f):>10.1f}{fit(f, extra=0.30):>13.1f}{fit(f, drop=2):>13.1f}")
    dn = fit(MODELS["constant"]) - fit(MODELS["framework (rises)"])
    ds = fit(MODELS["constant"], extra=0.30) - fit(MODELS["framework (rises)"], extra=0.30)
    print(f"""
  gas/pressure systematic modeled as sigma_sys = 0.30*z (~27% extra error at z=0.9 -- the regime where
  turbulent pressure support and gas fractions bias dynamical masses upward).

  Delta chi2 (constant - framework):
     no systematic  : {dn:5.1f}  = {np.sqrt(max(dn,0)):.1f} sigma   (naive)
     with systematic: {ds:5.1f}  = {np.sqrt(max(ds,0)):.1f} sigma   (honest)
  Leave-one-out: dropping the z=0.9 MUSE-DARK point, framework chi2={fit(MODELS['framework (rises)'], drop=2):.1f} vs
  constant chi2={fit(MODELS['constant'], drop=2):.1f} -- nearly indistinguishable. The discriminating power is almost
  entirely in that one high-z point.\n""")
    print("="*92); print("PROJECT 11 VERDICT"); print("="*92)
    print(f"""  The rising-a0 preference is REAL but MODEST and fragile:
    * naive chi2 favors rising at ~5 sigma over constant (and crushes SIV);
    * a realistic z-growing gas/pressure systematic deflates that to ~{np.sqrt(max(ds,0)):.1f} sigma;
    * it rests almost entirely on the single z=0.9 point -- drop it and rising vs constant is a coin toss.
  So the current data LEAN to rising a0 (and clearly disfavor SIV's falling a0), but do not establish it.
  The honest significance is ~2-3 sigma, systematic- and single-point-limited. This is exactly why Project 10
  (the many-point, gas-controlled compilation) is the highest-value data project: it replaces this 3-point,
  one-point-dependent inference with a population that can reach decisive significance.""")
    print("="*92)


if __name__ == "__main__":
    main()
