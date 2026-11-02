#!/usr/bin/env python3
"""UX7 M_L: lg M500 = a + b lg L500 + c lg(1+z) on hydrostatic tables S09, L15, L20 x eRASS1; no shear. Writes ux7_mass.json, ux7_mass.out. kappa = 1/2 FITTED; not theory closed."""
import csv
from ux7_common import *
OUT = []
def P(s): print(s, flush=True); OUT.append(str(s))
h = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; EN = [str(n).strip() for n in h["NAME"]]; ra, de, zz, L5, M5c, Mgc = [np.array(h[c], float) for c in ("RA", "DEC", "BEST_Z", "L500", "M500", "MGAS500")]
def sep(a, d): c = np.cos(np.radians(d)); return np.hypot(((ra - a + 180) % 360 - 180) * c, de - d) * 60
rows = []
for r in csv.DictReader(open(os.path.join(RB, "GS4_pointed_gas_offset", "gs4_inputs.csv"))):
    if r["cat"] not in ("S09", "L15", "L20") or not r["M500"]: continue
    s = sep(float(r["ra"]), float(r["dec"])); j = int(np.argmin(s)); z = float(r["z"])
    if s[j] < 5 and abs(z - zz[j]) < .03 and L5[j] > 0: rows.append((math.log10(float(r["M500"]) * float(r["h"]) / .7), math.log10(L5[j]), math.log10(1 + zz[j]), r["cat"], j))
Y = np.array([q[0] for q in rows]); A = np.c_[np.ones(len(Y)), [q[1] for q in rows], [q[2] for q in rows]]; co, *_ = np.linalg.lstsq(A, Y, rcond=None); rs = Y - A @ co; cat = np.array([q[3] for q in rows])
P(f"calibration N {len(Y)} ({', '.join(f'{c} {(cat == c).sum()}' for c in ('S09', 'L15', 'L20'))}); a {co[0]:.3f}, b {co[1]:.3f}, c {co[2]:.3f}; scatter {rs.std():.3f} dex; lg M range {Y.min():.2f}-{Y.max():.2f}; K7 {'PASS' if len(Y) >= 30 else 'FAIL'}")
for c in ("S09", "L15", "L20"): P(f"  residual by table {c}: median {np.median(rs[cat == c]):+.3f}")
X7 = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); nm = [str(x).strip() for x in X7["name"]]; ix = np.array([EN.index(n) for n in nm]); ML = 10 ** (co[0] + co[1] * np.log10(L5[ix]) + co[2] * np.log10(1 + zz[ix])); MC = M5c[ix] * 1e13; Mg = np.asarray(X7["Mgas500"], float); Mg = Mg if np.median(Mg) > 1e10 else Mg * 1e11
d = np.log10(ML / MC); P(f"326: lg(M_L/M_cat) median {np.median(d):+.3f}, sd {d.std():.3f}; corr lg M_L, lg Mg {np.corrcoef(np.log10(ML), np.log10(Mg))[0, 1]:.3f}; corr lg M_cat, lg Mg {np.corrcoef(np.log10(MC), np.log10(Mg))[0, 1]:.3f}; slope lg Mg on lg M_L {np.polyfit(np.log10(ML), np.log10(Mg), 1)[0]:.2f}; median Mg {np.median(Mg):.3e}; median M/Mg {np.median(ML / Mg):.2f}")
XX, xn, _, _ = xcop_full(); of = []; D = os.path.join(REPO, "real_research", "data", "xcop")
for n in sorted(x for x in os.listdir(D) if os.path.isdir(os.path.join(D, x))):
    H = fits.open(os.path.join(D, n, f"{n}_hydro_mass.fits"))[1].header; s = sep(H["RA"], H["DEC"]); j = int(np.argmin(s))
    if s[j] < 5 and L5[j] > 0: q = co[0] + co[1] * math.log10(L5[j]) + co[2] * math.log10(1 + zz[j]) - math.log10(H["M500"] * 1e14); of.append(q); P(f"  X-COP {n}: lg(M_L/M_HSE) {q:+.3f}")
K6 = float(np.median(of)); P(f"K6 median lg(M_L/M_HSE) on {len(of)} X-COP clusters in eRASS1: {K6:+.3f}: {'PASS' if abs(K6) <= .15 else 'FAIL'}")
rg = np.random.default_rng(20261102); pm = rg.permutation(len(nm)); J = dict(L={n: float(v) for n, v in zip(nm, ML)}, cat={n: float(v) for n, v in zip(nm, MC)}, shuf={n: float(v) for n, v in zip(nm, ML[pm])}, gas10={n: float(v) * 10 ** .005 for n, v in zip(nm, Mg)}, coef=co.tolist(), N=len(Y), scatter=float(rs.std()), K6=K6)
json.dump(J, open(os.path.join(HERE, "ux7_mass.json"), "w")); open(os.path.join(HERE, "ux7_mass.out"), "w").write("\n".join(OUT) + "\n")
