"""CFG103-A3c (POST-HOC, written AFTER reading CFG43's A3 .out; labelled as such).  CFG43's f_h is the halo-to-baryon MASS ratio M_h = f_h M_b
(f_h = 10, 20, 40), not a linear size multiplier as I had (mis)read it in the frozen grid.  This script (1) re-solves directly at CFG43's
'direct check' configuration (f_h=20, k=pi/R_L(M_h)), (2) re-does the convention grid with f_h as a MASS ratio in {1,1/f_b,10,20,40}, using the
frozen nu_min(k;d) table from cfg103_A3_results.json (log-log spline) and the same nu_M / R_L definitions.  Nothing here changes the frozen results."""
import os, sys, json, itertools, numpy as np
from scipy.interpolate import CubicSpline
from multiprocessing import get_context
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg103_growth import Cosmo, numin_scan
HERE = os.path.dirname(os.path.abspath(__file__))
RES = json.load(open(os.path.join(HERE, "cfg103_A3_results.json")))
cos = Cosmo(); out = []
def P(*a): s = " ".join(str(x) for x in a); print(s); out.append(s)
G = 6.6743e-11; c = 299792458.0; Msun = 1.98847e30; Mpc = 3.0856775814913673e22
H0s = cos.H0 * 1e3 / Mpc; a0 = cos.kappa * c * H0s * np.sqrt(3 * cos.OL / (8 * np.pi)); rhoL = 3 * H0s**2 * cos.OL / (8 * np.pi * G)
rho_m0 = cos.Om * 3 * H0s**2 / (8 * np.pi * G) / Msun * Mpc**3
nu_M = lambda Mb: a0 / (4 * np.pi * G * np.sqrt(G * Mb * Msun / a0) * np.sqrt(2)) / rhoL
R_L = lambda Mh: (3 * Mh / (4 * np.pi * rho_m0))**(1 / 3)
def kof(Mb, fh_mass, kconv, ku): return kconv / R_L(fh_mass * Mb) * (cos.h if ku == "h" else 1.0)
D = [0.05, 0.2, 0.3, 0.5]
tab = {d: np.array(RES["numin_table"][str(d)]) for d in D}
spl = {}
for d in D:
    t = tab[d]; t = t[np.isfinite(t[:, 1])]; spl[d] = CubicSpline(np.log(t[:, 0]), np.log(t[:, 1]))
numin_k = lambda k, d: float(np.exp(spl[d](np.log(k))))
xF = lambda F: np.sqrt(F / (1 - F))
# (1) direct re-solves, f_h = 20, k = pi/R
def job(args):
    Mb, d = args; k = kof(Mb, 20.0, np.pi, "Mpc"); o, _ = numin_scan(k, Cosmo(), [d]); return Mb, d, k, o[d]
with get_context("fork").Pool(4) as p: r = p.map(job, [(1e9, 0.05), (3e11, 0.05), (1e9, 0.2), (3e11, 0.2)])
P("(1) DIRECT, f_h = 20 (M_h = 20 M_b), k = pi/R_L(M_h), F>=1/2:   [CFG43: g0(5%)=0.32, g0(20%)=0.94 at 3e10; direct check 1.079/1.037 at 1e9/3e11; referee 0.36/0.355, 1.06/1.04]")
for Mb, d, k, nm in r: P("    M_b=%.0e d=%2.0f%% k=%.3f nu_min=%.4g nu_M=%.4g g0=%.4f" % (Mb, d * 100, k, nm, nu_M(Mb), nu_M(Mb) / nm))
# (2) grid with f_h as mass ratio
P("(2) grid with f_h = M_h/M_b in {1, 1/f_b=%.2f, 10, 20, 40}; k conv {pi,1,2pi}/R_L(M_h); d in {5,20,30,50}%%; F in {0.5,0.9,0.1,0.01}; units {1/Mpc, h/Mpc}" % (1 / cos.fb))
rows = []
for d, F, kc, fh, ku in itertools.product(D, [0.5, 0.9, 0.1, 0.01], [np.pi, 1.0, 2 * np.pi], [1.0, 1 / cos.fb, 10.0, 20.0, 40.0], ["Mpc", "h"]):
    g = nu_M(1e9) / (xF(F) * numin_k(kof(1e9, fh, kc, ku), d)); g2 = nu_M(3e11) / (xF(F) * numin_k(kof(3e11, fh, kc, ku), d))
    rows.append(dict(d=d, F=F, kc=kc, fh=fh, ku=ku, g=g, g2=g2))
gmax = lambda rs: max(r_["g"] for r_ in rs)
def line(name, rs):
    g = gmax(rs); P("    %-70s g0max = %8.3g  window = %s" % (name, g, "%.3g" % g**2 if g > 1 else "EMPTY"))
line("F=0.5, d<=20%, f_h in {10,20,40}, k conv {pi,2pi}/R (CFG43-style grid), 1/Mpc", [r_ for r_ in rows if r_["F"] == 0.5 and r_["d"] <= 0.2 and r_["fh"] in (10, 20, 40) and r_["kc"] in (np.pi, 2 * np.pi) and r_["ku"] == "Mpc"])
line("F=0.5, d<=50%, f_h in {10,20,40}, k conv {pi,2pi}/R (CFG43 'most generous corner')", [r_ for r_ in rows if r_["F"] == 0.5 and r_["d"] <= 0.5 and r_["fh"] in (10, 20, 40) and r_["kc"] in (np.pi, 2 * np.pi) and r_["ku"] == "Mpc"])
line("F=0.5, d<=50%, f_h in {10,20,40}, k conv incl. 1/R", [r_ for r_ in rows if r_["F"] == 0.5 and r_["d"] <= 0.5 and r_["fh"] in (10, 20, 40) and r_["ku"] == "Mpc"])
line("F=0.9 (hydrostatic), d<=50%, f_h in {10,20,40}, k conv incl. 1/R", [r_ for r_ in rows if r_["F"] == 0.9 and r_["fh"] in (10, 20, 40) and r_["ku"] == "Mpc"])
line("referee stack: d=30%, F=0.01, f_h=40, k=1/R, 1/Mpc", [r_ for r_ in rows if r_["d"] == 0.3 and r_["F"] == 0.01 and r_["fh"] == 40 and r_["kc"] == 1.0 and r_["ku"] == "Mpc"])
line("same stack with F=0.9", [r_ for r_ in rows if r_["d"] == 0.3 and r_["F"] == 0.9 and r_["fh"] == 40 and r_["kc"] == 1.0 and r_["ku"] == "Mpc"])
line("same stack with F=0.5", [r_ for r_ in rows if r_["d"] == 0.3 and r_["F"] == 0.5 and r_["fh"] == 40 and r_["kc"] == 1.0 and r_["ku"] == "Mpc"])
line("everything free, F in {0.5,0.9}, 1/Mpc", [r_ for r_ in rows if r_["F"] in (0.5, 0.9) and r_["ku"] == "Mpc"])
line("everything free incl. F=0.01 and h/Mpc unit confusion", rows)
n4 = sum(1 for r_ in rows if r_["g"] >= 100); P("    grid points with window >= 1e4: %d of %d ; with F>=0.9: %d ; with F>=0.9 and 1/Mpc and f_h<=1/f_b: %d" %
    (n4, len(rows), sum(1 for r_ in rows if r_["g"] >= 100 and r_["F"] >= 0.9), sum(1 for r_ in rows if r_["g"] >= 100 and r_["F"] >= 0.9 and r_["ku"] == "Mpc" and r_["fh"] <= 1 / cos.fb + 1e-9)))
top = sorted([r_ for r_ in rows if r_["g"] >= 100 and r_["F"] >= 0.9], key=lambda r_: -r_["g"])[:3]
for r_ in top: P("      F>=0.9 top: d=%g F=%g kconv=%.3f f_h=%g units=%s g0=%.3g window=%.3g" % (r_["d"], r_["F"], r_["kc"], r_["fh"], r_["ku"], r_["g"], r_["g"]**2))
# hydrostatic P/Pcap = g_N/a0 inside r_M : what the target demands of the cap at r_M
P("(3) hydrostatic requirement (CFG44): P_target/P_cap = g_N/a0 = (r_M/r)^2 >= 1 for r <= r_M; at r = r_M it is exactly 1 -> F(x_M) -> 1 needs x_M >> 1.")
for F in (0.5, 0.9, 0.99): P("    F(r_M) >= %.2f requires x_M >= %.2f i.e. g0 reduced by %.2fx relative to F=1/2" % (F, xF(F), xF(F)))
open(os.path.join(HERE, "cfg103_A3c_fh_mass.out"), "w").write("\n".join(out) + "\n")
