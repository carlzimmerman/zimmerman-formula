"""UD3: the a0 law on Malin 1 with a warped outer disc (FROZEN_CRITERIA.md).

Inputs: Lelli+2010 Table 3 (as UD2) and UD2's committed baryon components (../UD2_malin1_giant_lsb/ud2.json).
Law g = nu(g_b/a0) g_b, nu(y) = 1/2 + sqrt(1/4 + 1/y); both footings, never pooled. kappa = 1/2 FITTED; not theory
closed. One galaxy excludes nothing.
"""
import json, os
import numpy as np
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__))
CONV = 1e6 / 3.0857e19
FOOT = dict(canonical=9.3603e-11, alt=1.1312e-10)
I0, R_W, R_END = 38.0, 24.0, 101.6
RT = np.array([12.5, 37.5, 62.5, 87.5]); VT = np.array([236.9, 216.2, 197.4, 214.1]); ET = np.array([9.4, 2.6, 4.7, 11.8])
U2 = json.load(open(os.path.join(HERE, "..", "UD2_malin1_giant_lsb", "ud2.json")))
GAS, LSB, HSB = (np.array(U2["decoHL"][k]) for k in ("gas", "lsb", "hsb"))
MOND_TOT = np.array(U2["mond2comp"]["total"])
OUT = []


def P(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s)


def nu(y): y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)
def chi2p(v, e, m): c = float(np.sum(((v - m) / e) ** 2)); return c, float(CHI2.sf(c, len(v)))
def label(p): return "CONSISTENT" if p >= 0.05 else ("FAIL" if p < 0.01 else "TENSION")


def incl(model, i_out):
    if model == "step": return np.where(RT > R_W, i_out, I0)
    if model == "step_outer2": return np.where(RT > 50.0, i_out, I0)
    if model == "ramp": return np.where(RT > R_W, I0 + (i_out - I0) * (RT - R_W) / (R_END - R_W), I0)
    raise ValueError(model)


def grade(model, i_out, a0, deproj, model_v=None):
    i = incl(model, i_out); s = np.sin(np.radians(I0)) / np.sin(np.radians(i))
    v, e = VT * s, ET * s
    f = np.cos(np.radians(i)) / np.cos(np.radians(I0)) if deproj else np.ones_like(RT)
    vb2 = f * (GAS ** 2 + LSB ** 2) + HSB ** 2
    gN = vb2 / RT * CONV
    m = np.sqrt(nu(gN / a0) * gN / CONV * RT) if model_v is None else model_v
    return chi2p(v, e, m) + (v, m)


R = {}
P("UD3 Malin 1 warp. kappa = 1/2 FITTED; not theory closed; footings never pooled; one galaxy excludes nothing.")
UD2C = {f: U2[f]["chi2"] for f in FOOT}
k0 = max(abs(grade(mo, I0, a0, dp)[0] - UD2C[f]) for f, a0 in FOOT.items() for mo in ("step", "ramp", "step_outer2") for dp in (False, True))
P(f"K0 i_out = 38 returns UD2 chi2 (canonical {UD2C['canonical']:.3f}, alt {UD2C['alt']:.3f}): max |d chi2| {k0:.2e} (line 1e-6) -> {'PASS' if k0 < 1e-6 else 'FAIL'}")
R["K0"] = k0
grid = np.round(np.arange(15.0, 60.0001, 0.1), 1)
for f, a0 in FOOT.items():
    R[f] = {}
    P(f"\n=== [{f}] a0 {a0:.4e}")
    for mo in ("step", "ramp", "step_outer2"):
        for dp in (False, True):
            tag = f"{mo}{'_deproj' if dp else ''}"
            c, p, v, m = grade(mo, 32.0, a0, dp)
            sc = np.array([grade(mo, io, a0, dp)[:2] for io in grid]); ok = grid[sc[:, 1] >= 0.05]
            ib = float(grid[np.argmin(sc[:, 0])])
            R[f][tag] = dict(chi2_32=c, p_32=p, label_32=label(p), V_obs_32=v.tolist(), V_law=m.tolist(), i_best=ib,
                             chi2_best=float(sc[:, 0].min()), p_ok_range=[float(ok.min()), float(ok.max())] if len(ok) else None)
            P(f"  {tag:18s} i_out 32: V_obs {np.round(v,1).tolist()} V_law {np.round(m,1).tolist()} chi2 {c:6.1f}/4 p {p:.2e} -> {label(p):10s}"
              f" | best i_out {ib:.1f} (chi2 {sc[:,0].min():.1f}); p>=0.05 for {R[f][tag]['p_ok_range']}")
    st = R[f]["step"]; ok = st["p_ok_range"]
    resc = ok is not None and ok[1] >= 32.0
    R[f]["verdict"] = "RESCUED BY WARP" if resc else "NOT RESCUED"
    need = "none in 15-60" if ok is None else f"{ok[0]:.1f}-{ok[1]:.1f}"
    P(f"  PRIMARY step, fixed baryons: i_out 32 -> {st['label_32']}; {R[f]['verdict']} (i_out with p>=0.05: {need}; line i_out >= 32)")
    ck = grade("step", 32.0, a0, False, model_v=MOND_TOT)
    P(f"  K2 paper's MOND-fit total under the 32 deg step (same code path): chi2 {ck[0]:.1f}/4")
    R[f]["K2_mond_fit_chi2_32"] = ck[0]
src = open(os.path.abspath(__file__)).read()
bad = [w for w in ("curve_fit", "minimize(", "least_squares", "leastsq", "emcee") if w in src.replace('"curve_fit", "minimize(", "least_squares", "leastsq", "emcee"', "")]
P(f"\nK1 optimiser grep: {bad if bad else 'none'} -> {'PASS' if not bad else 'FAIL'}")
json.dump(R, open(os.path.join(HERE, "ud3.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, "ud3.out"), "w").write("\n".join(OUT) + "\n")
