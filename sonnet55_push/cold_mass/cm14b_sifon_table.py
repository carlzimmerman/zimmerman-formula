"""cm14b: cm14 redone on Sifon+2018's ACTUAL table (arXiv:1706.06125, Table t:mcmc, m* bins, spec+RS; H0 = 70, masses in Msun). These are CLUSTER satellites
(MENeaCS, host log M_h ~ 15.5, M_200,h = 6e14 used in the paper's text for r_200), <R_sat> 0.66-0.93 Mpc. m_bg = mass inside r_bg, where the subhalo density
equals the host's local density; r_bg is not tabulated, so it is ESTIMATED by matching an isothermal subhalo, m_bg/(4 pi r^3) = rho_host(R_sat), with an NFW host
(M200 = 6e14, c = 4) -- stated approximation (r_bg ~ 40-130 kpc).
Framework readings inside r_bg (baryons M_b = 1.2 M*, + retained cold 0.13 x 5.36 x M_b):
  A full MOND boost (satellite owns its phantom); B boost with the host's external field (1-D: nu at (g_N + g_ext)/a0, g_ext = host G M(<R_sat)/R_sat^2 with the
  NFW host, i.e. the cluster's measured mass); C candidate B's ownership (no phantom in a bound satellite).
Per reading and bin: pull = (log m_bg - log M_pred)/sigma(log m_bg); verdict per reading from the chi^2 over the 5 bins (5 dof): CONSISTENT if p > 0.01.
Run: python3 cm14b_sifon_table.py | MUTATE=1 sets a0 -> 0 in A (A must fail)
"""
import os, sys, math, re, numpy as np
from scipy.stats import chi2
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
tex = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "_external_data", "sifon2018", "src", "meneacs_satellite_lensing.tex")).read()
mstar, rsat = [], []
for line in tex.split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 9 and re.match(r"^M\d$", c[1]):
        rsat.append(float(re.sub(r"[^0-9.]", "", c[5]))); mstar.append(float(re.sub(r"[^0-9.]", "", c[7].replace("\\,", ""))))
mbg = [(float(a), float(lo), float(hi)) for a, lo, hi in re.findall(r"\\log\\langle m_\\mathrm\{bg,\d\} \\rangle\$ & \$\[7,14\]\$ & \$([0-9.]+)_\{-([0-9.]+)\}\^\{\+([0-9.]+)\}\$", tex)]
print(f"   parsed: log M* {mstar}; <R_sat> {rsat} Mpc; log m_bg {[m[0] for m in mbg]}")
assert len(mstar) == 5 and len(mbg) == 5
G, Msun, kpc, Mpc = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22; a0 = 9.3603e-11
rho_c = 3 * (70e3 / Mpc)**2 / (8 * math.pi * G) * Mpc**3 / Msun          # Msun/Mpc^3
M200, c = 6e14, 4.0; r200 = (3 * M200 / (4 * math.pi * 200 * rho_c))**(1 / 3); rs = r200 / c
mu = lambda x: math.log(1 + x) - x / (1 + x); rhos = M200 / (4 * math.pi * rs**3 * mu(c))
rho_h = lambda r: rhos / ((r / rs) * (1 + r / rs)**2); Mh = lambda r: 4 * math.pi * rhos * rs**3 * mu(r / rs)
def nu(y): return math.sqrt(1 + 1 / y)
rows = {"A": [], "B": [], "C": []}
for (lm, (lmb, elo, ehi), R) in zip(mstar, mbg, rsat):
    Ms = 10**lm; Mb = 1.2 * Ms; ret = 0.13 * (0.1200 / 0.02237) * Mb; mb = 10**lmb
    rbg = (mb / (4 * math.pi * rho_h(R)))**(1 / 3)                         # Mpc
    gN = G * Mb * Msun / (rbg * Mpc)**2; ge = G * Mh(R) * Msun / (R * Mpc)**2
    pA = (Mb if MUTATE else nu(gN / a0) * Mb) + ret; pB = nu((gN + ge) / a0) * Mb + ret; pC = Mb + ret
    sig = 0.5 * (elo + ehi)
    for k, p in (("A", pA), ("B", pB), ("C", pC)): rows[k].append((lmb - math.log10(p)) / sig)
    print(f"   log M* {lm:5.2f}: m_bg {mb:.2e} (+-{sig:.2f} dex), r_bg {rbg*1e3:4.0f} kpc, g_ext {ge/a0:.2f} a0 | A {pA:.2e}  B {pB:.2e}  C {pC:.2e}")
for k, lab in (("A", "full MOND boost"), ("B", "boost with host EFE"), ("C", "ownership: no phantom")):
    z = np.array(rows[k]); X2 = float((z**2).sum()); p = float(chi2.sf(X2, 5))
    print(f"   {k} {lab:22s}: pulls {np.round(z, 1)}  chi2 {X2:.1f}/5  p {p:.2g}  -> {'CONSISTENT' if p > 0.01 else 'EXCLUDED'} (mean log offset {np.mean(z * np.array([0.5*(m[1]+m[2]) for m in mbg])):+.2f} dex)")
    if k == "A": okA = p > 0.01
check("A the full-boost reading fits the five bins (MUTATE a0 -> 0 must fail)", okA)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
