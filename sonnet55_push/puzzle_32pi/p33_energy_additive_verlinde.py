"""p33: does Verlinde's elastic dark-energy response, combined by FIELD-ENERGY additivity instead of mass additivity, give the framework's law?
Verlinde (arXiv:1611.02269; CFG117 form): M_D^2(r) = (a_V r^2/G) d(M_B r)/dr,  a_V = c H/6.  g_N = G M_B/r^2, g_D = G M_D/r^2.
  Verlinde (mass additivity):         g = g_N + g_D                        (CFG117: wrong shape, off x2 at r = r_M)
  energy additivity (this test):      g^2/(8 pi G) = g_N^2/(8 pi G) + g_D^2/(8 pi G)   ->  g^2 = g_N^2 + g_D^2
  framework law:                      g^2 = g_N^2 + a0 g_N
Exact (sympy): g_D^2 = a_V (g_N + 4 pi G rho_B r). So energy additivity = framework law with a0 = a_V wherever rho_B(r) = 0, with an extra local term inside matter.
Numeric: exponential spheres (CFG117's four cases, H_Lambda), the ratio g_energy/g_framework over x = r/r_M in [0.1, 30].
Run: python3 p33_energy_additive_verlinde.py  |  MUTATE=1: mass additivity instead (check P must fail)
"""
import os, sys, math
import numpy as np
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
r, G, aV = sp.symbols("r G a_V", positive=True); MB = sp.Function("M_B")(r)
MD2 = aV * r**2 / G * sp.diff(MB * r, r)
gN = G * MB / r**2; gD2 = G**2 * MD2 / r**4
rhoB = sp.diff(MB, r) / (4 * sp.pi * r**2)
check("E1 exact: g_D^2 = a_V (g_N + 4 pi G rho_B r)", sp.simplify(gD2 - aV * (gN + 4 * sp.pi * G * rhoB * r)) == 0)
# point mass: M_B = M constant
M = sp.symbols("M", positive=True)
gN_pm = G * M / r**2; gD_pm = sp.sqrt(sp.simplify(gD2.subs(MB, M).doit()))
g_comb = (gN_pm + gD_pm) if MUTATE else sp.sqrt(gN_pm**2 + gD_pm**2)
g_fw = sp.sqrt(gN_pm**2 + aV * gN_pm)
check("P point mass: energy additivity gives EXACTLY the framework law g^2 = g_N^2 + a_V g_N at every radius", sp.simplify(g_comb - g_fw) == 0)
# exponential spheres, numeric (G in kpc (km/s)^2 / Msun; a_V = c H_Lambda/6)
Gk = 4.30091e-6; c_kms = 299792.458; H = 67.4 * math.sqrt(0.685) / 1000.0     # km/s/kpc
aVn = c_kms * H / 6.0                                                          # (km/s)^2/kpc
print(f"   a_V = c H_Lambda/6 = {aVn * 1e3 / 3.0857e19 * 1e3:.4e} m/s^2 (framework footing a0 = 9.360e-11; ratio {aVn*1e6/3.0857e19/9.3603e-11:.3f})")
worst_out = 0.0
for Mb, h in ((1e9, 2.0), (1e10, 3.0), (1e11, 4.0), (1e12, 5.0)):
    rM = math.sqrt(Gk * Mb / aVn)
    x = np.geomspace(0.1, 30, 400); rr = x * rM
    MBr = Mb * (1 - np.exp(-rr / h) * (1 + rr / h + (rr / h)**2 / 2))          # exponential sphere rho ~ e^(-r/h)
    rho = Mb / (8 * math.pi * h**3) * np.exp(-rr / h)
    g_N = Gk * MBr / rr**2
    gD2n = aVn * (g_N + 4 * math.pi * Gk * rho * rr)
    g_e = (g_N + np.sqrt(gD2n)) if MUTATE else np.sqrt(g_N**2 + gD2n)
    g_f = np.sqrt(g_N**2 + aVn * g_N)
    ratio = g_e / g_f
    outside = rr > 15 * h
    worst_out = max(worst_out, float(np.max(np.abs(ratio[outside] - 1))) if outside.any() else 0)
    i1 = np.argmin(abs(x - 1))
    print(f"   exp sphere M_b = {Mb:.0e}, h = {h} kpc (r_M = {rM:6.2f} kpc): g_energy/g_framework at x = 0.1, 1, 3: "
          f"{ratio[0]:.3f}, {ratio[i1]:.3f}, {ratio[np.argmin(abs(x-3))]:.3f};  max |dev| beyond 15h: {np.max(np.abs(ratio[outside]-1)) if outside.any() else float('nan'):.1e}")
check(f"X extended galaxies: energy additivity matches the framework law to {worst_out:.1e} beyond 15 scale lengths (where rho_B is negligible)", worst_out < 1e-2)
print("   Y (reported, not a check): inside the matter the local term 4 pi G rho_B r raises g by up to x2 at x = 0.1 (low-mass galaxies most): a testable difference from the framework law")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
