"""CFG103-A3d (POST-HOC, exploratory, after the frozen runs): does a SHARPER barotropic cap F_p = x^p/(1+x^p) (p up to 32) evade the ceiling?
Same growth solver, same nu_M / R_L definitions (primary: k = pi/R_L(M_b/f_b), F>=F_crit, window g0^2).  x_F = (F/(1-F))^(1/p).
Reports the p-dependence of g0 at d = 5%, 20%, 50% for F_crit = 1/2 and 0.9 (hydrostatic), and the k=1/R variant."""
import os, sys, numpy as np
from multiprocessing import get_context
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg103_growth import Cosmo, numin_scan
HERE = os.path.dirname(os.path.abspath(__file__)); cos = Cosmo(); out = []
def P(*a): s = " ".join(str(x) for x in a); print(s); out.append(s)
G = 6.6743e-11; c = 299792458.0; Msun = 1.98847e30; Mpc = 3.0856775814913673e22
H0s = cos.H0 * 1e3 / Mpc; a0 = cos.kappa * c * H0s * np.sqrt(3 * cos.OL / (8 * np.pi)); rhoL = 3 * H0s**2 * cos.OL / (8 * np.pi * G)
rho_m0 = cos.Om * 3 * H0s**2 / (8 * np.pi * G) / Msun * Mpc**3
nu_M = lambda Mb: a0 / (4 * np.pi * G * np.sqrt(G * Mb * Msun / a0) * np.sqrt(2)) / rhoL
R_L = lambda Mh: (3 * Mh / (4 * np.pi * rho_m0))**(1 / 3)
ps = [2, 3, 4, 8, 16, 32]; Ds = [0.05, 0.2, 0.5]; Mbs = [1e9, 3e11]
def job(a):
    p, kconv, Mb = a; k = kconv / R_L(Mb / cos.fb); o, _ = numin_scan(k, Cosmo(), Ds, shape=(p if p != 2 else "atan")); return (p, kconv, Mb), o
jobs = [(p, kc, Mb) for p in ps for kc in (np.pi, 1.0) for Mb in Mbs]
with get_context("fork").Pool(12) as pool: r = dict(pool.map(job, jobs))
P("g0 = nu_M/(x_F nu_min), M_h = M_b/f_b, F_p = x^p/(1+x^p);  columns: p | k conv | d | g0(1e9) g0(3e11) at F=1/2 | at F=0.9 (x_F=9^(1/p)) | window(F=0.9)")
for kc, nm in ((np.pi, "pi/R"), (1.0, "1/R")):
    for d in Ds:
        for p in ps:
            g = [nu_M(Mb) / r[(p, kc, Mb)][d] for Mb in Mbs]; xf = 9.0**(1.0 / p)
            P("  p=%-2d k=%-5s d=%2.0f%% : g0 = %.3f / %.3f | F=0.9: %.3f / %.3f  window %s" % (p, nm, d * 100, g[0], g[1], g[0] / xf, g[1] / xf, ("%.3g" % (g[0] / xf)**2) if g[0] / xf > 1 else "EMPTY"))
open(os.path.join(HERE, "cfg103_A3d_sharp_caps.out"), "w").write("\n".join(out) + "\n")
