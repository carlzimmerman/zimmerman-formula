"""EUC13R instrument checks and known answers that need no source distribution:
analytic checks, quadrature convergence, sample P count, KA1 (SLACS), KA2 (source-free b_med on P), KA6 (COSMOS).
Writes euc13r_checks.json. Exit 0 if all pass, 2 otherwise."""
import json
import math
import os
import sys

import numpy as np
from scipy.integrate import quad

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import euc13r_core as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
res = {}
ok_all = True


def check(name, ok, **kw):
    global ok_all
    ok_all &= bool(ok)
    res[name] = dict(passed=bool(ok), **kw)
    print(f"{name}: {'PASS' if ok else 'FAIL'} {kw}")


# --- analytic: point mass (a0 -> 0) and deep regime
def point_m2d(R, M, a0, k=C.K_NODES):
    x, w = C.gl(k)
    U = math.acosh(C.RMAX / R)
    u = 0.5 * U * (x + 1)
    r = R * np.cosh(u)
    gN = C.G * M / r ** 2
    g = C.g_law(gN, a0)
    return R ** 2 / C.G * np.sum(0.5 * U * w * g)


M, R = 1e11, 5.0
v = point_m2d(R, M, 0.0)
check("AN1_point_mass_newton", abs(v / M - 1) < 1e-6, rel_err=v / M - 1)
a0big = 1e9 * C.A0["canonical"]
v = point_m2d(R, M, a0big)
# deep regime: g ~ sqrt(a0 G M)/r + GM/(2r^2) ... compare with exact numeric quad of the same integrand
f = lambda r: C.g_law(C.G * M / r ** 2, a0big) / math.sqrt(r * r - R * R)
ref = R ** 2 / C.G * (quad(lambda u: C.g_law(C.G * M / (R * math.cosh(u)) ** 2, a0big), 0, math.acosh(C.RMAX / R),
                           limit=500, epsabs=0, epsrel=1e-11)[0])
check("AN2_point_mass_deep_vs_quad", abs(v / ref - 1) < 1e-4, rel_err=v / ref - 1)
deep = R * math.sqrt(a0big * C.G * M) / C.G * math.asin(math.sqrt(1 - (R / C.RMAX) ** 2))
res["AN2_info_deep_analytic_ratio"] = v / deep
print("deep analytic ratio (includes Newton term):", v / deep)

# --- Sersic (PS) projection vs direct line-of-sight integral (Newtonian), and PS vs exact 2D Sersic light
worst = 0.0
worst_ps = 0.0
for n in (1.0, 2.5, 4.0, 7.0):
    Re = 5.0
    p = C.ps_p(n)
    bn = float(C.b_n(n))
    norm = quad(lambda r: 4 * math.pi * r * r * C.ps_rho_shape(r / Re, n), 0, np.inf, limit=400)[0]
    for x in (0.2, 0.7, 1.5, 4.0):
        Rr = x * Re
        wu, h = C.h_nodes(np.array([Rr]), Re, n, 1.0)
        m_law = C.m2d_from_nodes(np.array([Rr]), wu, h, np.array([1.0]), 0.0)[0]
        # direct: M2D(R) = M - int_R^inf 4 pi r^2 rho sqrt(1 - R^2/r^2) dr
        outside = quad(lambda r: 4 * math.pi * r * r * C.ps_rho_shape(r / Re, n) * math.sqrt(1 - (Rr / r) ** 2),
                       Rr, np.inf, limit=400)[0] / norm
        m_dir = 1.0 - outside
        worst = max(worst, abs(m_law / m_dir - 1))
        worst_ps = max(worst_ps, abs(m_law / float(C.sersic_lfrac2d(x, n)) - 1))
check("AN3_PS_projection_vs_direct_los", worst < 1e-3, max_rel=worst)
res["AN4_PS_vs_exact_2D_sersic_max_rel"] = worst_ps
print("PS vs exact 2D Sersic light, max rel:", worst_ps)

# --- sample P
key, obj = C.load_eclipse()
rows, removed = C.select_P(key, obj)
L = C.lens_arrays(rows)
N = len(rows)
check("P_count", N == 3192, N=N, removed=removed)

zl = L["zl"]
DA = C.EUCLID.DA(zl)
RE = L["tE"] * C.ARCSEC * DA
Rek = L["te"] * C.ARCSEC * DA
Ms = 10 ** L["logm"]
T = math.pi * RE ** 2 * C.EUCLID.sigcr(zl, 1100.0)

# --- quadrature convergence on 200 lenses
idx = np.arange(0, N, N // 200)[:200]
for fp in ("canonical", "alt"):
    a0 = C.A0[fp]
    wu1, h1 = C.h_nodes(RE[idx], Rek[idx], L["n"][idx], Ms[idx], k=C.K_NODES)
    wu2, h2 = C.h_nodes(RE[idx], Rek[idx], L["n"][idx], Ms[idx], k=1200)
    m1 = C.m2d_from_nodes(RE[idx], wu1, h1, np.ones(len(idx)), a0)
    m2 = C.m2d_from_nodes(RE[idx], wu2, h2, np.ones(len(idx)), a0)
    check(f"QUAD_convergence_{fp}", np.max(np.abs(m1 / m2 - 1)) < 1e-5, max_rel=float(np.max(np.abs(m1 / m2 - 1))))

# --- KA2: source-free b_med on P, direct bisection
for fp, ref in (("canonical", -0.019), ("alt", -0.044)):
    b = C.solve_b_direct(RE, Rek, L["n"], Ms, T, C.A0[fp])
    med = float(np.median(b))
    check(f"KA2_{fp}", abs(med - ref) <= 0.001, b_med=round(med, 4), ref=ref)
    res[f"KA2_{fp}"]["f25_source_free"] = float(np.mean(b > 0.25))

# --- KA1: SLACS at true z_s
sl = C.load_slacs()
good = []
for r in sl:
    try:
        zl_, zs_, REk, lm, Fs, ReV = (float(r["zlens"]), float(r["zsrc"]), float(r["RE"]), float(r["Mass"]),
                                     float(r["Fs"]), float(r["Re(V)"]))
    except (ValueError, KeyError):
        continue
    good.append((zl_, zs_, REk, lm, Fs, ReV))
g = np.array(good)
res["KA1_N"] = len(g)
Re_kpc = g[:, 5] * C.ARCSEC * C.AUGER.DA(g[:, 0])
ME = 10 ** g[:, 3]
lf = C.sersic_lfrac2d(g[:, 2] / Re_kpc, 4.0)
Mst = g[:, 4] * ME / lf
for fp, ref in (("canonical", 0.082), ("alt", 0.070)):
    b = C.solve_b_direct(g[:, 2], Re_kpc, 4.0, Mst, ME, C.A0[fp])
    med = float(np.median(b))
    check(f"KA1_{fp}", abs(med - ref) <= 0.003, b_med=round(med, 4), ref=ref, N=len(g))
    # reference only: same lenses with the source at infinity (Auger cosmology), K5-like
    Tinf = ME * C.AUGER.sigcr(g[:, 0], 1100.0) / C.AUGER.sigcr(g[:, 0], g[:, 1])
    binf = C.solve_b_direct(g[:, 2], Re_kpc, 4.0, Mst, Tinf, C.A0[fp])
    res[f"KA1_{fp}"]["b_med_source_at_infinity_reference"] = float(np.median(binf))

# --- KA6: COSMOS sanity
mags, zs, info = C.load_cosmos_rows()
sel = (mags > 23.5) & (mags < 24.5) & np.isfinite(zs)
med = float(np.median(zs[sel]))
check("KA6_cosmos_median_z_23.5_24.5", 0.6 <= med <= 1.6, median=round(med, 3), n=int(sel.sum()))
H, ntot = C.cosmos_counts(mags, zs)
res["cosmos_slices"] = [dict(file=a, lo=b_, hi=c, rows_flag0_numeric=d, kept=e) for a, b_, c, d, e in info]
res["cosmos_total_in_grid"] = ntot
res["cosmos_rows_all"] = int(len(mags))
np.savetxt(os.path.join(HERE, "cosmos_counts_euc13r.csv"), H, fmt="%d", delimiter=",",
           header="rows: HSC i bins 16.0-28.0 step 0.1; cols: lpzBEST bins 0-6 step 0.05")

res["all_passed"] = bool(ok_all)
with open(os.path.join(HERE, "euc13r_checks.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)
print("ALL PASSED" if ok_all else "SOME CHECK FAILED")
sys.exit(0 if ok_all else 2)
