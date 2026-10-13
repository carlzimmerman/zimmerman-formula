#!/usr/bin/env python3
"""CFG713 (criteria 686c52f55): what extra mass do SLACS lenses need beyond stars + the law?
H-IMF: stars + law, M* the only freedom (fixed by theta_E). H-X: + an isothermal cold component holding a share f_x of the projected
mass inside theta_E; (M*, f_x) solved from theta_E and the imaging-only slope. kappa = 1/2 FITTED; not theory closed."""
import os, sys, io, re, json, math, contextlib
import numpy as np
from scipy.optimize import brentq
from scipy.stats import spearmanr
from astropy.cosmology import Planck18 as cosmo
import astropy.units as u
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG713_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
# reuse CFG712's verified machinery (universal de Vaucouleurs deprojection, law, projection) without re-running its prediction block
P712 = os.path.join(LANES, "CFG712_slacs_imaging_slopes", "cfg712_predict.py")
src = open(P712).read().split("out = {")[0]
g = {"__file__": P712, "__name__": "c712"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, P712, "exec"), g)
C4, X, m3, hcol, proj, eth, aug = g["C4"], g["X"], g["m3"], g["hcol"], g["proj"], g["eth"], g["aug"]
G, MSUN, C = C4.G_SI, C4.MSUN, 2.99792458e8
# observed imaging-only gamma (Etherington+2022), as parsed by the CFG712 scorer
s = open(os.path.join(os.path.dirname(REPO), "_external_data", "etherington2022", "src", "6_Results.tex")).read()
i = s.find("label{table: SLACS mass"); blk = s[s.rfind("begin{table", 0, i):i]; obs = {}
for line in blk.splitlines():
    m = re.search(r"(J\d{4}[+-]\d{4})", line)
    if not m or "&" not in line: continue
    cells = line.split("&"); k = [j for j, c in enumerate(cells) if m.group(1) in c][0]
    gg = re.findall(r"(\d+\.?\d*)\^\{(?:\\textrm\{)?\+?(\d+\.?\d*)\}?\}?_\{(?:\\textrm\{)?-?(\d+\.?\d*)", cells[k + 2])
    if gg: obs[m.group(1)] = (float(gg[0][0]), 0.5 * (float(gg[0][1]) + float(gg[0][2])))
# SPS stellar masses from the record's Auger+2009 file
AUG = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
lines = [l.rstrip("\n") for l in open(AUG, encoding="latin-1")]
hi = [j for j, l in enumerate(lines) if l.startswith("recno")][0]; hdr = lines[hi].split("\t"); col = {c: j for j, c in enumerate(hdr)}
sps = {}
for r in [l.split("\t") for l in lines[hi + 3:] if l.strip() and not l.startswith("#")]:
    mm = re.match(r"J?(\d{4})\d*\.?\d*([+-]\d{4})", r[col["SDSS"]].strip().replace(" ", ""))
    if mm:
        try: sps["J" + mm.group(1) + mm.group(2)] = (float(r[col["logMc"]]), float(r[col["logMs"]]))
        except ValueError: pass

def setup(zl, zs, Re_as, thE):
    Dl = cosmo.angular_diameter_distance(zl).to(u.m).value; Ds = cosmo.angular_diameter_distance(zs).to(u.m).value
    Dls = cosmo.angular_diameter_distance_z1z2(zl, zs).to(u.m).value
    Scr = C ** 2 / (4 * math.pi * G) * Ds / (Dl * Dls); arc = Dl / 206264.806
    Re = Re_as * arc; RE = thE * arc
    return Re * X, RE, Scr * math.pi * RE ** 2, Re

def law_M(r, Ms, a0):
    gN = G * Ms * m3 / r ** 2
    return (gN + a0 * hcol(gN / a0)) * r ** 2 / G

def slope(r, M, RE):
    e = 0.02
    kap = lambda R: (proj(r, M, R * (1 + e)) - proj(r, M, R * (1 - e))) / (2 * e * R) / (2 * math.pi * R)
    return 1 - (math.log(kap(RE * 1.05)) - math.log(kap(RE * 0.95))) / (math.log(1.05) - math.log(0.95))

def solve_fx(r, RE, ME, a0, gtarget):
    """for a given extra share f_x: isothermal A r with projected (pi/2) A RE = f_x ME; M* so the law part carries (1 - f_x) ME"""
    def gam(fx):
        A = fx * ME / (math.pi / 2 * RE); Mx = A * r
        f = lambda lm: (proj(r, law_M(r, 10 ** lm * MSUN, a0), RE) + proj(r, Mx, RE)) / ME - 1
        lm = brentq(f, 7.0, 13.5, xtol=1e-5)
        return slope(r, law_M(r, 10 ** lm * MSUN, a0) + Mx, RE), lm
    g0, lm0 = gam(0.0)
    if gtarget >= g0:
        return 0.0 if abs(gtarget - g0) < 1e-6 else -1.0, lm0, g0, g0   # needs LESS extended mass than the law: flagged
    g95, _ = gam(0.95)
    if gtarget < g95:
        return 0.95, None, g0, g95                                      # needs more than 95 %: flagged
    fx = brentq(lambda f: gam(f)[0] - gtarget, 0.0, 0.95, xtol=1e-4)
    return fx, gam(fx)[1], g0, None

OUT, RES = [], {"lane": "CFG713", "criteria": "686c52f55", "mutate": MUT}
Pr = lambda x: (print(x, flush=True), OUT.append(x))
names = sorted(set(eth) & set(aug) & set(obs) & set(sps))
pred712 = json.load(open(os.path.join(LANES, "CFG712_slacs_imaging_slopes", "cfg712_predictions.json")))["lenses"]
for foot, a0 in C4.A0.items():
    rows = []
    for nm in names:
        A = aug[nm]
        if not all(math.isfinite(v) for v in (A["zl"], A["zs"], A["ReI"])): continue
        r, RE, ME, Re = setup(A["zl"], A["zs"], A["ReI"], eth[nm])
        gobs, eobs = obs[nm]
        gt = pred712[nm][foot]["gamma_pred"] if MUT else gobs
        fx, lm, g0, _ = solve_fx(r, RE, ME, a0, gt)
        lMc, lMs = sps[nm]
        f0 = brentq(lambda l: proj(r, law_M(r, 10 ** l * MSUN, a0), RE) / ME - 1, 7.0, 13.5, xtol=1e-5)
        imf_ok = (abs(g0 - gobs) <= eobs) and (lMc - 0.2 <= f0 <= lMs + 0.3)
        # the law's own cold fraction inside theta_E at f_x = 0
        Mlaw = law_M(r, 10 ** f0 * MSUN, a0); Mst = G * 10 ** f0 * MSUN * m3 / r ** 2 * r ** 2 / G
        cold_law = 1 - proj(r, Mst, RE) / proj(r, Mlaw, RE)
        rows.append(dict(name=nm, f_x=fx, logMstar_HX=lm, logMstar_HIMF=f0, lMc=lMc, lMs=lMs, gamma_obs=gobs, gamma_law=g0,
                         imf_ok=bool(imf_ok), Re_kpc=Re / C4.KPC, thE_over_Re=eth[nm] / A["ReI"], law_cold_fraction=cold_law))
    fx = np.array([x["f_x"] for x in rows]); ok = (fx >= 0) & (fx < 0.95)
    imf_frac = float(np.mean([x["imf_ok"] for x in rows]))
    lmx = np.array([x["logMstar_HX"] for x in rows if x["logMstar_HX"] is not None and 0 <= x["f_x"] < 0.95])
    lsal = np.array([x["lMs"] for x in rows if x["logMstar_HX"] is not None and 0 <= x["f_x"] < 0.95])
    lchab = np.array([x["lMc"] for x in rows if x["logMstar_HX"] is not None and 0 <= x["f_x"] < 0.95])
    trend = {}
    for key in ("Re_kpc", "thE_over_Re", "lMs"):
        v = np.array([x[key] for x in rows])[ok]; rho, p = spearmanr(v, fx[ok]); trend[key] = (float(rho), float(p))
    ratio = np.median(fx[ok] / np.array([x["law_cold_fraction"] for x in rows])[ok])
    RES[foot] = dict(n=len(rows), H_IMF_pass_fraction=imf_frac, H_IMF="EXCLUDED" if imf_frac < 0.5 else "NOT EXCLUDED",
                     f_x_median=float(np.median(fx[ok])) if ok.any() else None, f_x_16_84=[float(np.percentile(fx[ok], 16)), float(np.percentile(fx[ok], 84))] if ok.any() else None,
                     n_needs_less=int((fx < 0).sum()), n_needs_more_than_95=int((fx >= 0.95).sum()),
                     HX_logMstar_minus_Salp=float(np.median(lmx - lsal)) if lmx.size else None,
                     HX_logMstar_minus_Chab=float(np.median(lmx - lchab)) if lmx.size else None,
                     trends_spearman=trend, f_x_over_law_cold_fraction=float(ratio), rows=rows)
    Pr(f"== {foot}: n {len(rows)}")
    Pr(f"  H-IMF (stars + law, M* only): pass fraction {imf_frac:.2f} -> {RES[foot]['H_IMF']}")
    if ok.any():
        Pr(f"  H-X: f_x median {np.median(fx[ok]):.3f} (16-84 {np.percentile(fx[ok],16):.3f}-{np.percentile(fx[ok],84):.3f}); "
           f"need less than the law: {(fx<0).sum()}; need >95%: {(fx>=0.95).sum()}")
        Pr(f"  H-X implied M* - SPS: Salpeter {RES[foot]['HX_logMstar_minus_Salp']:+.2f}, Chabrier {RES[foot]['HX_logMstar_minus_Chab']:+.2f} dex")
        Pr(f"  f_x / law's own cold fraction inside theta_E (median): {ratio:.2f}")
        Pr(f"  trends (Spearman rho, p): " + "; ".join(f"{k} {v[0]:+.2f} ({v[1]:.2g})" for k, v in trend.items()))
code = 0
if MUT:
    med = abs(RES["canonical"]["f_x_median"] or 0); bite = med < 0.02
    Pr(f"MUTATE gamma_obs -> law's gamma_pred: median |f_x| {med:.4f} -> {'BITES' if bite else 'DOES NOT BITE'}"); code = 1 if bite else 0
json.dump(RES, open(os.path.join(HERE, f"cfg713_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg713{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(code)
