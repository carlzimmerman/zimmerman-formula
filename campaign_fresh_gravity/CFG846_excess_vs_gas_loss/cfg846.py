"""CFG846 -- does the residual over the law track gas-poorness at matched g_bar (H-EX's prediction)?  Criteria: FROZEN_CRITERIA.md (a575dcd09).
Run: python3 cfg846.py (CFG846_MUTATE=1: s shuffled).  kappa = 1/2 FITTED; not theory closed."""
import os, glob, json, math, numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG846_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
KPC, a0 = 3.0857e19, 9.3603e-11; nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
Q = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: Q[v[0]] = dict(inc=float(v[5]), q=int(v[17]), L=float(v[7]), MHI=float(v[13]))
        except ValueError: pass
def run(ud):
    gals, allres = [], []
    for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        nm = os.path.basename(fn).replace("_rotmod.dat", ""); g = Q.get(nm)
        if not g or g["q"] > 2 or g["inc"] < 30: continue
        lgb, res = [], []
        for l in open(fn):
            if l.startswith("#") or not l.strip(): continue
            R, V, eV, Vg, Vd, Vb = [float(t) for t in l.split()[:6]]
            if V <= 0 or R <= 0 or eV / V >= 0.10: continue
            gb = (Vg * abs(Vg) + ud * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
            if gb <= 0: continue
            r = math.log10(V * V * 1e6 / (R * KPC) / float(gb * nu(gb / a0))); allres.append(r)
            if gb < 10 ** -10.5: lgb.append(math.log10(gb)); res.append(r)
        if res:
            Ms = ud * g["L"]; s = Ms / (Ms + 1.33 * g["MHI"]) if (Ms + g["MHI"]) > 0 else float("nan")
            gals.append(dict(name=nm, s=s, d=float(np.median(res)), lg=float(np.median(lgb)), n=len(res)))
    return gals, float(np.median(allres))
P("CFG846  residual over the law vs gas-poorness at matched g_bar (SPARC)" + ("  [MUTATE s shuffled]" if MUT else ""))
RES = dict(lane="CFG846", mutate=MUT); rng = np.random.default_rng(846)
for ud in (0.5, 0.4, 0.6):
    gals, med = run(ud); s = np.array([g["s"] for g in gals]); d = np.array([g["d"] for g in gals]); lg = np.array([g["lg"] for g in gals])
    if MUT: s = rng.permutation(s)
    A = np.vstack([np.ones_like(lg), lg]).T; rd = d - A @ np.linalg.lstsq(A, d, rcond=None)[0]; rs = s - A @ np.linalg.lstsq(A, s, rcond=None)[0]
    rho, p = spearmanr(rs, rd, alternative="greater"); t = np.argsort(s); n3 = len(s) // 3
    diff = float(np.mean(rd[t[-n3:]]) - np.mean(rd[t[:n3]]))
    cls = "H-EX PATTERN SEEN" if (p < 0.01 and diff >= 0.05) else ("NO PATTERN" if p >= 0.05 else "HINT")
    RES[f"ud{ud}"] = dict(N=len(gals), rho=float(rho), p=float(p), tercile_diff=diff, median_all=med, s_range=[float(s.min()), float(s.max())], cls=cls)
    P(f"  [Upsilon_disk {ud}] N {len(gals)} galaxies (s {s.min():.2f}-{s.max():.2f}): partial rho {rho:+.3f} (one-sided p {p:.3f}); gas-poor minus gas-rich tercile {diff:+.3f} dex -> {cls}" + (f"   [K1 median all {med:+.3f}]" if ud == 0.5 else ""))
c = [RES[f"ud{u}"]["cls"] for u in (0.5, 0.4, 0.6)]; RES["cls"] = c[0] if len(set(c)) == 1 else f"{c[0]} (not stable across Upsilon: {c})"
if not MUT:
    R28 = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))["canonical|nu_e"]["rows"]
    lowd = [r["delta"] for r in R28 if r["lgbar"] < -12]
    R29 = json.load(open(os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829_results.json")))
    b, rr = R29["canonical|nu_e|blue (u-r<2.5)"]["window"], R29["canonical|nu_e|red (u-r>2.5)"]["window"]
    P("\n  Test 2 (reported): at g_bar < 1e-12")
    P(f"    gas-free satellite dSphs/UFDs (CFG828, N {len(lowd)}): mean Delta {np.mean(lowd):+.2f} dex")
    P(f"    red (gas-poor) isolated lenses (CFG829): {math.log10(rr['A']):+.2f} dex;  blue (gas-rich) lenses: {math.log10(b['A']):+.2f} dex")
    P(f"    SPARC (gas-rich discs) reach only g_bar >= 8e-13; their lowest bin sits at +0.07 dex (CFG828)")
P(f"\n  CLASS (Test 1): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg846_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg846{sfx}.out"), "w").write("\n".join(OUT) + "\n")
