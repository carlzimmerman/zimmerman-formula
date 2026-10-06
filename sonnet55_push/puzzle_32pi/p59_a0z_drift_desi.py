"""p59: a0(z) drift if a0 tracks the dark-energy density (PAPER42 reading: rho_DE ~ a0^2 with the kernel fixed  =>  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0))),
under DESI DR2 w0-wa (CPL) fits, versus the rival a0 ~ H(z) and the flat law. Backs PAPER42's sentence "about 0.8x today's value at z = 2.5 ... the rival gives 3.7x".
CPL: rho_DE(a)/rho_DE(1) = a^(-3(1+w0+wa)) exp(-3 wa (1-a)).  H(z)/H0 = sqrt(Om (1+z)^3 + (1-Om) rho_DE ratio), Om = 0.31 (flat).
DESI DR2 (arXiv:2503.14738) w0, wa central values QUOTED FROM MEMORY -- PROVISIONAL, verify against the paper's table before citing:
  +DESY5 (-0.752, -0.86), +Pantheon+ (-0.838, -0.62), +Union3 (-0.667, -1.09).  Error bands: independent Gaussian draws (no covariance) -> conservative.
Checks: L LCDM (w0=-1, wa=0) gives a0(z)/a0(0) = 1 exactly; P PAPER42's numbers reproduced (0.7-0.9 at z = 2.5; rival 3.4-4.0).
Run: python3 p59_a0z_drift_desi.py | MUTATE=1 drops the CPL exponential (wrong rho_DE; P must fail)
"""
import os, sys, numpy as np
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
def rde(z, w0, wa):
    a = 1 / (1 + z); r = a**(-3 * (1 + w0 + wa))
    return r if MUTATE else r * np.exp(-3 * wa * (1 - a))
def H(z, w0, wa, Om=0.31): return np.sqrt(Om * (1 + z)**3 + (1 - Om) * rde(z, w0, wa))
zs = np.array([0.5, 1.0, 2.0, 2.5, 3.0, 5.0])
check("L LCDM gives a0(z)/a0(0) = 1 at every z", np.allclose(np.sqrt(rde(zs, -1, 0)), 1))
fits = {"DESY5": (-0.752, -0.86, 0.057, 0.22), "Pantheon+": (-0.838, -0.62, 0.055, 0.21), "Union3": (-0.667, -1.09, 0.088, 0.29)}
rng = np.random.default_rng(59)
print("   a0(z)/a0(0) = sqrt(rho_DE ratio)   [16-84% band, independent draws]      rival H(z)/H0 (LCDM)")
v25 = []
for k, (w0, wa, s0, sa) in fits.items():
    W0 = rng.normal(w0, s0, 20000); WA = rng.normal(wa, sa, 20000)
    row = []
    for z in zs:
        c = np.sqrt(rde(z, w0, wa)); band = np.percentile(np.sqrt(rde(z, W0, WA)), [16, 84])
        row.append(f"z={z:.1f}: {c:.3f} [{band[0]:.2f},{band[1]:.2f}]")
        if z == 2.5: v25.append(c)
    print(f"   {k:10s} " + "  ".join(row))
riv = H(zs, -1, 0)
print("   rival a0 ~ H(z):  " + "  ".join(f"z={z:.1f}: {r:.2f}" for z, r in zip(zs, riv)))
print(f"   log10 separation at z = 2.5: tracking {np.log10(min(v25)):.2f}..{np.log10(max(v25)):.2f} dex vs rival {np.log10(riv[3]):+.2f} dex vs flat 0")
check(f"P PAPER42's numbers: tracking 0.7-0.9 at z = 2.5 (got {min(v25):.2f}-{max(v25):.2f}), rival 3.4-4.0 (got {riv[3]:.2f})", all(0.7 <= v <= 0.9 for v in v25) and 3.4 <= riv[3] <= 4.0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
