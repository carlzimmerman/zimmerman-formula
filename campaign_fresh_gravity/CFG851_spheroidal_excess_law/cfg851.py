"""CFG851 -- one excess law for spheroidal systems: calibrate on red lenses, predict the dSphs blind.  Criteria: FROZEN_CRITERIA.md.
Reuses cfg829.py's loader.  Run: python3 cfg851.py (CFG851_MUTATE=1: calibrate on blue).  kappa = 1/2 FITTED; not theory closed."""
import os, json, math, numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG851_MUTATE") == "1"; os.environ.pop("CFG829_MUTATE", None)
src = open(os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py")).read().split("P(\"CFG829  KiDS")[0]
M = {"__file__": os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py"), "__name__": "d"}; exec(compile(src, "cfg829.py", "exec"), M)
load, nu_e, A0 = M["load"], M["nu_e"], M["A0"]; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
RED = ("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5)
BLUE = ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0)
R28 = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))
def calibrate(ds, shift, foot):
    gb, go, C = load(*ds); gbs = gb * 10 ** shift; gl = gbs * nu_e(gbs / A0[foot]); Ci = np.linalg.inv(C)
    def chi2(p):
        b, lgd = p
        if b < 0: return 1e30
        d = b * np.maximum(0.0, lgd - np.log10(gbs)); r = go - gl * 10 ** d; return float(r @ Ci @ r)
    best = min((minimize(chi2, [b0, l0], method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-6, maxiter=4000)) for b0 in (0.05, 0.2, 0.5) for l0 in (-14, -12.5, -11)), key=lambda r: r.fun)
    b, lgd = best.x; c0 = best.fun
    bs = np.linspace(0, 1.5, 301); prof = [min(minimize(lambda l: chi2([bb, l[0]]), [lgd], method="Nelder-Mead").fun for _ in [0]) for bb in bs]
    ok = bs[np.array(prof) <= c0 + 1]; chi_law = chi2([0.0, -12.0])
    return dict(b=float(b), lgd=float(lgd), chi2=c0, chi2_law=chi_law, b_lo=float(ok.min()), b_hi=float(ok.max()), n=len(gb))
def predict(cal, lg):
    return cal["b"] * max(0.0, cal["lgd"] - lg)
P("CFG851  one excess law for spheroidal systems" + ("  [MUTATE: calibrated on BLUE lenses]" if MUT else ""))
RES = dict(lane="CFG851", mutate=MUT)
for foot in ("canonical", "alt"):
    key = "canonical|nu_e" if foot == "canonical" else "alt|nu_e"
    dw = [r for r in R28[key]["rows"] if r["lgbar"] < -11.9]; dobs = np.array([r["delta"] for r in dw])
    for shift in ((0.0,) if MUT else (0.123, 0.0)):
        cal = calibrate(BLUE if MUT else RED, shift, foot)
        pr = np.array([predict(cal, r["lgbar"]) for r in dw])
        # sigma_pred: spread of the mean prediction over b in its 1 sigma range at fixed g_dagger
        prl = np.mean([cal["b_lo"] * max(0, cal["lgd"] - r["lgbar"]) for r in dw]); prh = np.mean([cal["b_hi"] * max(0, cal["lgd"] - r["lgbar"]) for r in dw])
        sp = 0.5 * abs(prh - prl); so = float(np.std(dobs, ddof=1) / math.sqrt(len(dobs))); diff = float(dobs.mean() - pr.mean()); z = diff / math.hypot(so, sp)
        und = cal["b_lo"] <= 0 and cal["b_hi"] > 1
        cls = "NOT DIAGNOSTIC" if und else ("UNIFIED" if abs(z) < 2 else ("DSPHS ABOVE" if z >= 2 else "DSPHS BELOW"))
        RES[f"{foot}|shift{shift}"] = dict(cal=cal, N_dw=len(dw), d_obs=float(dobs.mean()), d_pred=float(pr.mean()), se_obs=so, se_pred=sp, z=z, cls=cls)
        P(f"\n  [{foot} | {'blue' if MUT else 'red'} M* shift +{shift}] fit b = {cal['b']:.3f} (1 sigma {cal['b_lo']:.3f}-{cal['b_hi']:.3f}), log g_dagger = {cal['lgd']:.2f}; chi2 {cal['chi2']:.1f} vs law {cal['chi2_law']:.1f} ({cal['n']} pts)")
        P(f"     dSphs (N {len(dw)}, g_bar < 1e-11.9): observed mean Delta {dobs.mean():+.3f} +- {so:.3f};  predicted {pr.mean():+.3f} +- {sp:.3f};  z {z:+.1f} -> {cls}")
if not MUT:
    cb = calibrate(BLUE, 0.0, "canonical"); P(f"\n  reported: blue lenses best-fit b = {cb['b']:.3f} (1 sigma {cb['b_lo']:.3f}-{cb['b_hi']:.3f}), log g_dagger {cb['lgd']:.2f}")
    RES["blue_b"] = cb
RES["cls"] = RES["canonical|shift0.123" if not MUT else "canonical|shift0.0"]["cls"]; P(f"\n  CLASS (canonical, M*-corrected red calibration): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg851_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg851{sfx}.out"), "w").write("\n".join(OUT) + "\n")
