#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR2 (PART A) -- AN INDEPENDENT CHECK OF DE1: where does the vacuum-gated switch turn MOND off around an isolated
galaxy, and is DE1's p = 2 "flagship failure" an observational exclusion?

Checked lane: real_research/dark_energy_2026/DE1_vacuum_gate_flagship.py as committed in c8bb50813 (a corrected
version was being written in the working tree during this review; the controls below read the COMMITTED results via
`git show`).  Nothing from DE1 or L352 is imported: kernels, derivatives, background and edges are re-implemented here.

WHAT DE1 COMPUTES (read from its source, c8bb50813):
  * the switch variable is x = 4 pi G (rho_dyn - rho_bar)/H(z)^2 (DE1.py lines 136-141, L352 model_M2 lines 189-196),
    with rho_dyn = dM/dr/(4 pi r^2), M(r) = M_b nu(g_N/a0): the ON-BRANCH (phantom-inclusive) density of an isolated
    point mass -- the baryons contribute nothing at r > 0, so x is the MOND phantom's density -- minus the mean matter
    density rho_bar = Omega_m rho_crit0 (1+z)^3 (the Hamiltonian-constraint form (3/2) Omega_m(z) delta).  K = 3 H(z)
    (background value), the shear part of x~ = 9(R3 + sigma^2)/(4K^2) is dropped (L359: it can only lower the
    effective threshold).  The gate is x_c,eff = x_c0 E_g(z)^(2p), E_g^2 = 0.3138 (1+z)^3 + 0.6862 (L359/L347).
  * MOND is on where x >= x_c,eff; the edge is the LARGEST such r ("the most favourable placement", L352 Z2).
  * the edge is computed with nu_mono for BOTH kernel labels (DE1.py c8bb50813 lines 136-157: r_edge_numeric always
    uses nu_mono_vec; the label only changes the size of the Newtonian jump), as the lead-track review noted.

THIS SCRIPT, in y = g_N/a0 variables (r = sqrt(G M_b/(a0 y))), for a point mass:
      X(y) = D(y) (a0 y)^(3/2) / (sqrt(G M_b) H(z)^2) - (3/2) Omega_m(z),     D(y) = -2 y nu'(y)
  (rho_dyn = M_b D(y)/(4 pi r^3)); D is ANALYTIC for nu_RAR (D = s e^s/(e^s - 1)^2, s = sqrt(y)), for nu_mono (closed
  form of L340's construction: h' = max(h'_RAR, 0.05 h_p/(y + y_p)), which equals nu_RAR for y <= y_s < y_p) and for
  mu_exp (x (1 - e^-x) = y, the law in the lead-track review).  X rises from -(3/2)Omega_m at y -> 0 to a peak in the
  Newtonian regime (y ~ 15 for nu_RAR) and falls again, so MOND is on for y_e <= y <= y_in; the flagship radius r_F
  (g_N = 0.1 a0) is inside the MOND region iff y_e <= 0.1.  Fractional margins: m_r = r_e/r_F - 1 = sqrt(0.1/y_e) - 1
  and m_X = X(0.1)/x_c,eff - 1.

CHECKS
  C1 CONTROL: DE1's committed F1 edges and flagship radii (canonical/alt, M_b = 1e10, 1e10.5, 1e11, p = 2, x_c0 = 2,
     z = 2.5) reproduced (edges 2e-4, radii 1e-9).
  C2 CONTROL: DE1's committed p_max at x_c0 = 2 (numeric 1.9650 / 2.0709; closed form 1.9696 / 2.0751) reproduced
     (numeric 1e-3, closed form 1e-9).
  C3 CONTROL: the lead-track review's independent X_F (REPORT.md: nu_RAR 364.4986385 / 482.4698532, mu_exp 364.3176614 /
     482.2305308 canonical/alt) and the p = 2 threshold 399.9004102813 reproduced (1e-6).
  C4 CONTROL: DE1's committed z_max for (p, x_c0) = (2, 2) (2.4623 / 2.5774) and its E1 ratios r_e/r_F at 1e11 for the
     three cells (z = 0.5 ... 3) reproduced (2e-3 / 5e-4).
  K1 (reported) the kernel labels: the nu_mono and nu_RAR edges coincide wherever y_e < y_s; mu_exp's differs slightly.
  T1 (reported) margins for (p, x_c0) in {(2, 2), (1, 2.5), (1, 1.5)}, M_b = 1e9 ... 1e11.5, z = 0.5 ... 3, both footings.
  T2 (reported) p = 1, x_c0 = 2.5: the smallest y with MOND on, z = 1-2.5, M_b = 1e9-1e10.5; is any y in [0.1, 0.3] off?
  T3 (reported) what the failing p = 2 cell loses at z = 2.5: the y-interval, radii, angular size; y_e at 1e11 vs z.
  T4 (reported) the branch: on L377's matter-only branch (the PM switch L380 ran) a point mass has no MOND region; the
     local baryon density the switch would need there, per cell and redshift.
MUTATE=1 freezes K at 3 H0 in the switch variable (x = 4 pi G rho/H0^2): the control C1 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR2_de1_edge_check.py
Single-threaded, numpy/scipy only, < 5 s.
"""
import os, sys, json, math, time, subprocess
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR2_de1_edge_check"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR2-A", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 112); P(t); P("=" * 112)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: K frozen at 3 H0 in the switch variable; C1 must FAIL (rc = 1) ***")

# ------------------------------------------------------------------ constants (the values L352/DE1 use, re-typed here)
c_ = 2.99792458e8; MPC_H = 3.0856775814913673e22; G = 6.67430e-11; MS = 1.98892e30
KPC = 3.0857e19                                                   # DE1's output unit (KPCm = 3.0857e16 * 1e6 / 1e3)
h = 0.6736; om_b, om_c = 0.02237, 0.1200; T_CMB, N_EFF = 2.7255, 3.046
H0 = 100 * h * 1e3 / MPC_H; RHO_C0 = 3 * H0 ** 2 / (8 * math.pi * G)
Og = (4 * 5.670374419e-8 * T_CMB ** 4 / c_ ** 3) / RHO_C0; Or = Og * (1 + N_EFF * (7 / 8) * (4 / 11) ** (4 / 3))
Om = (om_b + om_c) / h ** 2; OL = 1 - Om - Or
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
FEET = ("canonical", "alt")
OMG = 0.3138                                                      # the gate's background (L359 / L347)


def Hz(z):                                                        # the edge's H(z) (as L352: radiation only in OL)
    return H0 * math.sqrt(Om * (1 + z) ** 3 + OL)


def E2g(z):
    return OMG * (1 + z) ** 3 + (1 - OMG)


def xc_eff(z, xc0, p):
    return xc0 * E2g(z) ** p


def Hsw(z):                                                       # the H in the switch variable x = 4 pi G rho / H^2
    return H0 if MUTATE else Hz(z)


def xbar(z):                                                      # 4 pi G rho_bar / H^2 = (3/2) Omega_m(z)
    return 1.5 * Om * (1 + z) ** 3 * (H0 / Hsw(z)) ** 2


# ------------------------------------------------------------------ kernels: nu and the phantom-density factor D = -2 y nu'
def D_rar(y):
    s = math.sqrt(y); em = -math.expm1(-s)                        # 1 - e^-s
    return s * math.exp(-s) / em ** 2


def nu_rar(y):
    return 1.0 / (-math.expm1(-math.sqrt(y)))


def h_rar(y):
    return y / math.expm1(math.sqrt(y))


def dh_rar(y):                                                    # analytic d/dy [y/(e^s - 1)]
    s = math.sqrt(y); em1 = math.expm1(s)
    return 1.0 / em1 - s * math.exp(s) / (2.0 * em1 ** 2)


Y_P = brentq(dh_rar, 1.0, 5.0, xtol=1e-14); H_P = h_rar(Y_P); DELTA = 0.05
floor = lambda y: DELTA * H_P / (y + Y_P)
Y_S = brentq(lambda y: dh_rar(y) - floor(y), 1e-3, Y_P, xtol=1e-14)   # nu_mono leaves nu_RAR here (h'_RAR = floor)


def h_mono(y):
    return h_rar(y) if y <= Y_S else h_rar(Y_S) + DELTA * H_P * math.log((y + Y_P) / (Y_S + Y_P))


def dh_mono(y):
    return dh_rar(y) if y <= Y_S else floor(y)


def nu_mono(y):
    return 1.0 + h_mono(y) / y


def D_mono(y):
    return 2.0 * (h_mono(y) - y * dh_mono(y)) / y


def xexp(y):                                                      # mu_exp: x (1 - e^-x) = y  (g/a0 = x)
    return brentq(lambda x: x * (-math.expm1(-x)) - y, 1e-300, y + 10.0, xtol=1e-300, rtol=1e-15, maxiter=500)


def nu_exp(y):
    return xexp(y) / y


def D_exp(y):
    x = xexp(y); dx = 1.0 / ((-math.expm1(-x)) + x * math.exp(-x))
    return 2.0 * (x - y * dx) / y


KERN = {"nu_RAR": (nu_rar, D_rar), "nu_mono": (nu_mono, D_mono), "mu_exp": (nu_exp, D_exp)}


def X_of_y(y, Mb, a0, z, kern="nu_RAR"):
    """the switch variable at the point where g_N = y a0 around an isolated point mass M_b [Msun] (on-branch)."""
    return KERN[kern][1](y) * (a0 * y) ** 1.5 / (math.sqrt(G * Mb * MS) * Hsw(z) ** 2) - xbar(z)


def y_peak(Mb, a0, z, kern):
    r = minimize_scalar(lambda ly: -X_of_y(math.exp(ly), Mb, a0, z, kern), bounds=(math.log(0.05), math.log(400.0)),
                        method="bounded", options={"xatol": 1e-10})
    return math.exp(r.x)


LGRID = np.linspace(math.log(1e-14), math.log(1e6), 2001)          # scan grid for the FIRST (outermost) crossing


def edge(Mb, a0, z, xc, kern="nu_RAR"):
    """(y_e, y_in): MOND on for y_e <= y <= y_in (the outermost on-interval); (None, None) if X never reaches xc.
    y_e is the smallest y with X >= xc (the largest radius, DE1/L352's placement), found by scanning up from y = 1e-14
    for the first sign change and refining it with brentq; y_in the next crossing back down (inf if none by 1e6)."""
    f = lambda ly: X_of_y(math.exp(ly), Mb, a0, z, kern) - xc
    fv = np.array([f(float(l_)) for l_ in LGRID])
    up = np.where((fv[:-1] < 0) & (fv[1:] >= 0))[0]
    if not len(up):
        yp = y_peak(Mb, a0, z, kern)
        if X_of_y(yp, Mb, a0, z, kern) < xc:
            return None, None
        ye = math.exp(brentq(f, math.log(1e-14), math.log(yp), xtol=1e-13)); i0 = int(np.searchsorted(LGRID, math.log(yp)))
    else:
        i = int(up[0]); ye = math.exp(brentq(f, LGRID[i], LGRID[i + 1], xtol=1e-13)); i0 = i + 1
    dn = np.where((fv[i0:-1] >= 0) & (fv[i0 + 1:] < 0))[0]
    yin = math.exp(brentq(f, LGRID[i0 + dn[0]], LGRID[i0 + dn[0] + 1], xtol=1e-13)) if len(dn) else float("inf")
    return ye, yin


def r_of_y(Mb, a0, y):
    return math.sqrt(G * Mb * MS / (a0 * y))


def r_flag(Mb, a0):
    return r_of_y(Mb, a0, 0.1)


def margins(Mb, foot, z, xc0, p, kern="nu_RAR"):
    a0 = A0[foot]; xc = xc_eff(z, xc0, p); ye, yin = edge(Mb, a0, z, xc, kern)
    if ye is None:
        return dict(y_e=None, m_r=-1.0, m_X=X_of_y(0.1, Mb, a0, z, kern) / xc - 1, re_kpc=0.0, rF_kpc=r_flag(Mb, a0) / KPC)
    return dict(y_e=ye, y_in=yin, m_r=math.sqrt(0.1 / ye) - 1, m_X=X_of_y(0.1, Mb, a0, z, kern) / xc - 1,
                re_kpc=r_of_y(Mb, a0, ye) / KPC, rF_kpc=r_flag(Mb, a0) / KPC)


P(f"\n  background: H0 = {H0:.4e} s^-1, Om = {Om:.5f}, OL = {OL:.5f} (edge); gate E_g^2 = {OMG}(1+z)^3 + {1 - OMG:.4f}")
P(f"  nu_mono: y_p = {Y_P:.4f}, h_p = {H_P:.4f}; nu_mono = nu_RAR exactly for y <= y_s = {Y_S:.4f}")

# ------------------------------------------------------------------ committed DE1 numbers (git show c8bb50813)
def committed_de1():
    rel = "real_research/dark_energy_2026/DE1_vacuum_gate_flagship_results.json"
    try:
        txt = subprocess.run(["git", "-C", REPO, "show", f"c8bb50813:{rel}"], capture_output=True, text=True, check=True).stdout
        return json.loads(txt)["numbers"], "git show c8bb50813"
    except Exception:
        return json.load(open(os.path.join(REPO, rel)))["numbers"], "working tree (git unavailable)"


DE1, SRC = committed_de1()
P(f"  DE1 committed numbers read from: {SRC}:real_research/dark_energy_2026/DE1_vacuum_gate_flagship_results.json")

# ============================================================================================ C1-C4 controls
banner("C1-C4  CONTROLS against DE1's committed numbers and the lead-track review")
dev_e, dev_r, rows = 0.0, 0.0, []
for r_ in DE1["F1"]:
    if r_["kernel"] != "nu_mono":
        continue
    m = margins(10 ** r_["lMb"], r_["foot"], 2.5, 2.0, 2.0, "nu_mono")
    dev_e = max(dev_e, abs(m["re_kpc"] / r_["re_kpc"] - 1)); dev_r = max(dev_r, abs(m["rF_kpc"] / r_["rflag_kpc"] - 1))
    rows.append((r_["foot"], r_["lMb"], r_["re_kpc"], m["re_kpc"], r_["rflag_kpc"], m["rF_kpc"]))
    P(f"    {r_['foot']:9s} M_b = 1e{r_['lMb']:.1f}: r_e DE1 {r_['re_kpc']:8.4f} kpc | this script {m['re_kpc']:8.4f} kpc ; "
      f"r_F DE1 {r_['rflag_kpc']:.6f} | this {m['rF_kpc']:.6f}")
check("C1 CONTROL: DE1's committed F1 edges (2e-4) and flagship radii (1e-9) at z = 2.5, cell (2, 2), are reproduced by an "
      "independent analytic-derivative edge", f"edges max dev {dev_e:.1e}; radii max dev {dev_r:.1e}",
      dev_e < 2e-4 and dev_r < 1e-9, "DE1's np.gradient edge on its 4000-point grid agrees with the analytic derivative")

pm_rows, ok2 = {}, True
for foot in FEET:
    a0 = A0[foot]
    pm_n = math.log(X_of_y(0.1, 1e11, a0, 2.5, "nu_RAR") / 2.0) / math.log(E2g(2.5))
    pm_m = math.log(X_of_y(0.1, 1e11, a0, 2.5, "nu_mono") / 2.0) / math.log(E2g(2.5))
    rhs = 0.1 * a0 ** 1.5 / (2.0 * Hsw(2.5) ** 2 * math.sqrt(G * 1e11 * MS))       # DE1's closed form (deep MOND, no bg)
    pm_c = math.log(rhs) / math.log(E2g(2.5))
    ref = DE1["P1"][f"2.0/{foot}"]
    ok2 &= abs(pm_m - ref["pmax_numeric"]) < 1e-3 and abs(pm_c - ref["pmax_closed"]) < 1e-9
    pm_rows[foot] = dict(pmax_RAR=pm_n, pmax_mono=pm_m, pmax_closed=pm_c, de1_numeric=ref["pmax_numeric"], de1_closed=ref["pmax_closed"])
    P(f"    p_max (x_c0 = 2, M_b = 1e11, z = 2.5), {foot:9s}: nu_mono {pm_m:.5f} (DE1 {ref['pmax_numeric']:.5f}); nu_RAR {pm_n:.5f}; "
      f"closed form {pm_c:.10f} (DE1 {ref['pmax_closed']:.10f})")
check("C2 CONTROL: DE1's committed p_max at x_c0 = 2 reproduced (numeric 1e-3, closed form 1e-9), both footings",
      "; ".join(f"{f_}: {v['pmax_mono']:.4f} vs {v['de1_numeric']:.4f}" for f_, v in pm_rows.items()), ok2)
OUT["numbers"]["C2_pmax"] = pm_rows

REV = {("nu_RAR", "canonical"): 364.4986385, ("nu_RAR", "alt"): 482.4698532,
       ("mu_exp", "canonical"): 364.3176614, ("mu_exp", "alt"): 482.2305308}          # REPORT.md table (lead track)
thr = xc_eff(2.5, 2.0, 2.0)
dev3 = max(abs(X_of_y(0.1, 1e11, A0[f_], 2.5, k_) / v - 1) for (k_, f_), v in REV.items())
dev3 = max(dev3, abs(thr / 399.9004102813 - 1))
xf = {f"{k_}/{f_}": X_of_y(0.1, 1e11, A0[f_], 2.5, k_) for k_ in KERN for f_ in FEET}
P(f"    X_F at M_b = 1e11, z = 2.5: " + ", ".join(f"{k_} {v:.7f}" for k_, v in xf.items()) + f";  p = 2 threshold {thr:.10f}")
check("C3 CONTROL: the lead-track review's independent X_F (nu_RAR, mu_exp; both footings) and the (2, 2) threshold at "
      "z = 2.5 reproduced (1e-6)", f"max relative deviation {dev3:.1e}", dev3 < 1e-6)
OUT["numbers"]["X_F_1e11_z2.5"] = xf; OUT["numbers"]["threshold_p2_z2.5"] = thr


def zmax(xc0, p, foot, masses=(10.0, 10.5, 11.0), kern="nu_mono"):
    def mfun(z):
        return min(math.log(max(margins(10 ** l_, foot, z, xc0, p, kern)["m_r"] + 1, 1e-30)) for l_ in masses)
    return brentq(mfun, 0.01, 12.0, xtol=1e-6) if mfun(0.01) > 0 > mfun(12.0) else float("nan")


zm = {f_: zmax(2.0, 2.0, f_) for f_ in FEET}
dev4a = max(abs(zm[f_] - DE1["F2"][f"2.0/2.0/{f_}"]) for f_ in FEET)
dev4b = 0.0
for (p, xc0) in ((2.0, 2.0), (1.0, 2.5), (1.0, 1.5)):
    for row in DE1["E1"][f"{p}/{xc0}/canonical/11.0"]:
        if row["z"] <= 3.0:
            m = margins(1e11, "canonical", row["z"], xc0, p, "nu_mono")
            dev4b = max(dev4b, abs((m["m_r"] + 1) / row["ratio"] - 1))
P(f"    z_max (2, 2), all of 1e10-1e11: canonical {zm['canonical']:.4f} (DE1 {DE1['F2']['2.0/2.0/canonical']:.4f}), "
  f"alt {zm['alt']:.4f} (DE1 {DE1['F2']['2.0/2.0/alt']:.4f});  E1 ratios max dev {dev4b:.1e}")
check("C4 CONTROL: DE1's committed z_max for (2, 2) (2e-3) and its E1 ratios r_e/r_F at 1e11 canonical for the three cells, "
      "z = 0.5-3 (5e-4), reproduced", f"z_max max |diff| {dev4a:.1e}; E1 max rel dev {dev4b:.1e}", dev4a < 2e-3 and dev4b < 5e-4)
OUT["numbers"]["C4_zmax"] = zm

# ============================================================================================ K1 kernel labels
banner("K1  THE KERNEL LABELS: each kernel with its OWN edge (DE1 c8bb50813 used nu_mono's edge for both labels)")
k1, dmax_mono, dmax_exp = [], 0.0, 0.0
for foot in FEET:
    for lMb in (10.0, 10.5, 11.0):
        mm = {k_: margins(10 ** lMb, foot, 2.5, 2.0, 2.0, k_) for k_ in KERN}
        sh = {k_: (0.0 if mm[k_]["m_r"] >= 0 else -2 * math.log10(KERN[k_][0](0.1))) for k_ in KERN}
        dmax_mono = max(dmax_mono, abs(mm["nu_mono"]["re_kpc"] / mm["nu_RAR"]["re_kpc"] - 1))
        dmax_exp = max(dmax_exp, abs(mm["mu_exp"]["re_kpc"] / mm["nu_RAR"]["re_kpc"] - 1))
        k1.append(dict(foot=foot, lMb=lMb, **{f"re_{k_}": mm[k_]["re_kpc"] for k_ in KERN}, **{f"shift_{k_}": sh[k_] for k_ in KERN},
                       rF=mm["nu_RAR"]["rF_kpc"]))
        P(f"    {foot:9s} 1e{lMb:.1f}: r_F {mm['nu_RAR']['rF_kpc']:6.2f} kpc | r_e nu_RAR {mm['nu_RAR']['re_kpc']:7.3f}, nu_mono "
          f"{mm['nu_mono']['re_kpc']:7.3f}, mu_exp {mm['mu_exp']['re_kpc']:7.3f} kpc | shift beyond edge: " +
          ", ".join(f"{k_} {sh[k_]:+.3f}" for k_ in KERN))
OUT["numbers"]["K1"] = k1
check("K1 (reported) at the F1 points the nu_mono and nu_RAR edges coincide (y_e << y_s: the kernels are identical there) and "
      "mu_exp's edge differs by < 0.1%: the committed 'both kernels' flag was one edge, but the verdict is kernel-independent",
      f"max |r_e(mono)/r_e(RAR) - 1| = {dmax_mono:.1e}; mu_exp vs RAR {dmax_exp:.1e}", dmax_mono < 1e-9 and dmax_exp < 1e-3,
      load_bearing=False)

# ============================================================================================ T1 margins
banner("T1  FRACTIONAL MARGINS m_r = r_e/r_F - 1 (nu_RAR's own edge; > 0 = MOND on at the flagship radius g_N = 0.1 a0)")
CELLS = ((2.0, 2.0), (1.0, 2.5), (1.0, 1.5))
LMB = (9.0, 9.5, 10.0, 10.5, 11.0, 11.5)
ZS = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
T1, kdev = {}, 0.0
for (p, xc0) in CELLS:
    for foot in FEET:
        P(f"  cell p = {p:g}, x_c0 = {xc0:g}, {foot}   (columns z = " + ", ".join(f"{z:g}" for z in ZS) + ")")
        for lMb in LMB:
            row = []
            for z in ZS:
                m = margins(10 ** lMb, foot, z, xc0, p, "nu_RAR"); mm_ = margins(10 ** lMb, foot, z, xc0, p, "nu_mono")
                kdev = max(kdev, abs(m["m_r"] - mm_["m_r"]))
                row.append(m); T1[f"{p}/{xc0}/{foot}/{lMb}/{z}"] = m
            P(f"    M_b = 1e{lMb:4.1f}: " + "  ".join(f"{m['m_r']:+8.3f}" for m in row) + "   | y_e at z=2.5: "
              f"{row[4]['y_e']:.2e}")
OUT["numbers"]["T1"] = T1
fails = sorted({(k_.split('/')[0] + '/' + k_.split('/')[1], k_.split('/')[2], k_.split('/')[3], k_.split('/')[4])
                for k_, v in T1.items() if v["m_r"] < 0})
P("  cells/footings/masses/redshifts with m_r < 0 (MOND OFF at the flagship radius):")
for cell in sorted({f_[0] for f_ in fails}):
    P(f"    {cell}: " + "; ".join(f"{f_[1]} 1e{f_[2]} z={f_[3]}" for f_ in fails if f_[0] == cell))
if not fails:
    P("    none")
p1_fail = [f_ for f_ in fails if f_[0].startswith("1.0/")]
check("T1 (reported) the p = 1 cells keep the flagship radius inside the MOND region at every mass 1e9-1e11.5 and z <= 3 on "
      "both footings; nu_mono and nu_RAR margins agree on this grid", f"p = 1 failures: {p1_fail or 'none'}; "
      f"max |m_r(mono) - m_r(RAR)| = {kdev:.1e}", not p1_fail and kdev < 1e-6, load_bearing=False)

# ============================================================================================ T2 the low-mass regime
banner("T2  p = 1, x_c0 = 2.5: THE SMALLEST y WITH MOND STILL ON (outer edge), z = 1-2.5, M_b = 1e9-1e10.5")
T2, worst_ratio, any_off = {}, float("inf"), False
for cell in ((1.0, 2.5), (2.0, 2.0)):
    p, xc0 = cell
    for foot in FEET:
        P(f"  cell p = {p:g}, x_c0 = {xc0:g}, {foot}:")
        for lMb in (9.0, 9.5, 10.0, 10.5):
            parts = []
            for z in (1.0, 1.5, 2.0, 2.5):
                ye, yin = edge(10 ** lMb, A0[foot], z, xc_eff(z, xc0, p), "nu_RAR")
                ygrid = np.linspace(0.1, 0.3, 201)
                off = any(X_of_y(float(y), 10 ** lMb, A0[foot], z, "nu_RAR") < xc_eff(z, xc0, p) for y in ygrid)
                T2[f"{p}/{xc0}/{foot}/{lMb}/{z}"] = dict(y_e=ye, y_in=yin, off_in_0p1_0p3=off)
                if cell == (1.0, 2.5):
                    worst_ratio = min(worst_ratio, 0.1 / ye); any_off |= off
                parts.append(f"z={z:g}: y_e {ye:.2e} (y_in {yin:.0f})" + (" OFF in [0.1,0.3]" if off else ""))
            P(f"    M_b = 1e{lMb:4.1f}: " + "; ".join(parts))
OUT["numbers"]["T2"] = T2
check("T2 (reported) for p = 1, x_c0 = 2.5 the gate never switches MOND off at y = 0.1-0.3 for M_b = 1e9-1e10.5 at z = 1-2.5 "
      "(both footings): the outer edge lies at y_e far below 0.1", f"min 0.1/y_e over the grid = {worst_ratio:.0f}; any y in "
      f"[0.1, 0.3] off: {any_off}", (not any_off) and worst_ratio > 1, load_bearing=False)

# ============================================================================================ T3 what (2, 2) loses
banner("T3  WHAT THE FAILING CELL (p = 2, x_c0 = 2) LOSES AT z = 2.5, AND WHERE THAT IS")


def DA_Mpc(z):                                                    # flat LCDM angular-diameter distance, this background
    chi = quad(lambda zz: 1.0 / math.sqrt(Om * (1 + zz) ** 3 + OL), 0.0, z)[0] * c_ / (H0 * MPC_H)
    return chi / (1 + z)


arcsec_kpc = DA_Mpc(2.5) * 1e3 * math.pi / (180 * 3600)
t3 = {}
for foot in FEET:
    m = margins(1e11, foot, 2.5, 2.0, 2.0, "nu_RAR")
    r1 = r_of_y(1e11, A0[foot], 1.0) / KPC
    t3[foot] = dict(y_e=m["y_e"], re_kpc=m["re_kpc"], rF_kpc=m["rF_kpc"], r_y1_kpc=r1, m_r=m["m_r"], m_X=m["m_X"],
                    rF_arcsec=m["rF_kpc"] * KPC / 3.0856775814913673e19 / arcsec_kpc)
    P(f"    {foot:9s} M_b = 1e11, z = 2.5: MOND on down to y_e = {m['y_e']:.4f} (r_e = {m['re_kpc']:.2f} kpc); lost: "
      f"y in [0.1, {m['y_e']:.4f}]" if m["m_r"] < 0 else
      f"    {foot:9s} M_b = 1e11, z = 2.5: MOND on down to y_e = {m['y_e']:.4f} (r_e = {m['re_kpc']:.2f} kpc) -- flagship kept")
    P(f"              r_F = {m['rF_kpc']:.2f} kpc = {t3[foot]['rF_arcsec']:.2f} arcsec (1 arcsec = {arcsec_kpc:.2f} kpc at z = 2.5); "
      f"r(y = 1) = {r1:.2f} kpc; margins m_r {m['m_r']:+.4f}, m_X {m['m_X']:+.4f}")
ye_z = {z: margins(1e11, "canonical", z, 2.0, 2.0, "nu_RAR")["y_e"] for z in (2.0, 2.5, 3.0, 3.5)}
P("    y_e(M_b = 1e11, canonical) vs z: " + ", ".join(f"z={z:g}: {v:.3f}" for z, v in ye_z.items()))
OUT["numbers"]["T3"] = dict(per_footing=t3, arcsec_kpc_z2p5=arcsec_kpc, y_e_vs_z=ye_z)

# ============================================================================================ T4 the branch
banner("T4  THE BRANCH: the density the switch needs if x~ excludes the phantom (L377's matter-only PM switch)")
P("    on-branch (DE1/L352, phantom-inclusive) vs matter-only branch (L377 lines 18, 119-120: f = 1.5 Omega_m(a) (rho - 1) gate"
  " > x_c0 with rho = baryons + carrier): for a POINT mass the matter-only x is -(3/2)Omega_m(z) at every r > 0, so that "
  "branch has no MOND region at all; for extended baryons the switch needs a LOCAL density above")
MSPC3 = MS / (3.0856775814913673e16) ** 3                          # kg/m^3 per Msun/pc^3
t4 = {}
for (p, xc0) in CELLS:
    vals = {}
    for z in (0.0, 1.0, 2.0, 2.5):
        rho_req = (xc_eff(z, xc0, p) + xbar(z)) * Hz(z) ** 2 / (4 * math.pi * G) / MSPC3
        vals[z] = rho_req
    t4[f"{p}/{xc0}"] = vals
    P(f"    cell ({p:g}, {xc0:g}): rho_min [Msun/pc^3] at z = " + ", ".join(f"{z:g}: {v:.2e}" for z, v in vals.items()))
rph = {}
for foot in FEET:
    a0 = A0[foot]; r = r_flag(1e11, a0)
    rph[foot] = 1e11 * MS * D_rar(0.1) / (4 * math.pi * r ** 3) / MSPC3
P("    for scale: the on-branch phantom density at r_F of a 1e11 Msun point mass = " +
  ", ".join(f"{f_} {v:.2e}" for f_, v in rph.items()) + " Msun/pc^3")
OUT["numbers"]["T4"] = dict(rho_min_Msun_pc3=t4, phantom_at_rF_1e11=rph)

# ============================================================================================ verdict
banner("VERDICT (PART A)")
c = t3["canonical"]; a = t3["alt"]
P(f"""  DE1's numbers stand as arithmetic.  Rebuilt from scratch (analytic phantom-density derivative, no DE1/L352 code), the
  p = 2, x_c0 = 2 edge at M_b = 1e11, z = 2.5 is {c['re_kpc']:.2f} kpc against r_F = {c['rF_kpc']:.2f} kpc canonical (m_r = {c['m_r']:+.3f},
  m_X = {c['m_X']:+.3f}) and {a['re_kpc']:.2f} vs {a['rF_kpc']:.2f} kpc alt (m_r = {a['m_r']:+.3f}); p_max = {pm_rows['canonical']['pmax_RAR']:.3f} / {pm_rows['alt']['pmax_RAR']:.3f}
  (nu_RAR, x_c0 = 2).  The lead track's code note is right (one nu_mono edge under two labels) and inconsequential:
  below y_s = {Y_S:.2f} nu_mono IS nu_RAR, and the edges sit at y ~ 0.1.
  What fails is the framework's OWN deep-MOND prediction, not data: the lost interval is y = 0.100-{c['y_e']:.3f} at
  {c['re_kpc']:.0f}-{c['rF_kpc']:.0f} kpc ({c['rF_arcsec']:.1f} arcsec) around the most massive flagship galaxy, canonical footing only, at radii
  {c['re_kpc'] / c['r_y1_kpc']:.1f}x r(y = 1).  It is an internal (framework-own-terms) gate: the construction would stop making the flat-a0 prediction
  there and would predict a Newtonian outer disc instead -- itself untested.
  Low-mass lensed discs (M_b = 1e9-1e10.5, z = 1-2.5, y ~ 0.1-0.3): at p = 1, x_c0 = 2.5 MOND stays on to y_e <= 0.1/{worst_ratio:.0f};
  the gate never touches y = 0.1-0.3 there (T2).  Caveats: point-mass baryons; the phantom-inclusive (upper) branch, which is
  the most favourable placement but NOT the branch L377/L380's PM switch runs (T4); the omitted shear term can only move
  edges outward.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_fail; OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: None if o is None else float(o))
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.1f}s]")
sys.exit(0 if n_fail == 0 else 1)
