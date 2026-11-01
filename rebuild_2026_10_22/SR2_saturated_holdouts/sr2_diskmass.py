#!/usr/bin/env python3
"""UR3 Part A: DiskMass sigma_z on CFG576's estimator, route E + response. FROZEN_CRITERIA.md. kappa = 1/2 FITTED, unused; not theory closed."""
import contextlib, io, json, math, os, sys
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from sr2_common import *
S576 = os.path.join(RB, "..", "campaign_fresh_gravity", "CFG576_diskmass_sigz", "cfg576_diskmass.py"); n = {"__file__": os.path.abspath(S576), "__name__": "h"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(S576).read().split('P("=" * 100)')[0], "h", "exec"), n)
gal, terms, K_V = n["gal"], n["galaxy_terms"], n["K_VERT"]; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def v2(R, M, h):
    if M <= 0: return np.zeros_like(R)
    S0 = M / (2 * math.pi * h * h); y = R / (2 * h); return 4 * math.pi * G * S0 * h * y * y * (i0e(y) * k0e(y) - i1e(y) * k1e(y))
def Mbar(r, t, Y, BD): return np.maximum.accumulate((v2(r, Y * t["Ld"], t["hR"]) + v2(r, t["Ma"], 2 * t["hR"]) + v2(r, t["Mm"], t["hR"])) * r / G + Y * t["Ld"] * BD)
YG = np.geomspace(0.02, 5.0, 90)
def one(g, R, mode, tag, d=0.0, dl=0.0, mut=1.0, nohalo=False):
    t = terms(g, R); BD = g["BD"]; lMb = math.log10(0.5 * t["Ld"] * (1 + BD) + t["Ma"] + t["Mm"]) + dl; M, R2, S, r0 = halo(lMb, tag, d); rg = np.geomspace(R * 0.01, R2, 500); gobs = t["vrot"] ** 2 / R; F = []
    def gs(Y):
        Rv = np.array([R]); gb = float(v2(Rv, Y * t["Ld"], t["hR"])[0] + v2(Rv, t["Ma"], 2 * t["hR"])[0] + v2(Rv, t["Mm"], t["hR"])[0]) / R + G * Y * t["Ld"] * BD / R ** 2
        if nohalo: return gb, 0.0
        Mb_ = Mbar(rg, t, Y, BD); Ms_ = Mbar(rg, dict(t, Ma=0.0, Mm=0.0), 0.5, BD); M0_ = math.pi * S * r0 ** 2 * Bs(rg / r0); Mg = sat_contract(rg, Mb_, Ms_, M0_, float(Mb_[-1] / M0_[-1])); return gb, G * float(np.interp(math.log(R), np.log(rg), Mg)) / R ** 2
    fs = [sum(gs(y)) - gobs for y in YG]; Y = None
    for i in range(len(YG) - 1):
        if fs[i] <= 0 < fs[i + 1]: Y = YG[i] * (YG[i + 1] / YG[i]) ** (-fs[i] / (fs[i + 1] - fs[i])); break
    if Y is None: return None
    gb, gc = gs(Y); Sig = Y * t["I0"] * math.exp(-R / t["hR"]) + n["sexp"](R, t["Ma"], 2 * t["hR"]) + n["sexp"](R, t["Mm"], t["hR"]); KN = 2 * math.pi * G * Sig * (1 - math.exp(-1)); B = 1 + gc * t["hz"] / R / KN
    return dict(Y=float(Y), B=float(B), r=math.sqrt(math.pi * G * K_V * t["hz"] * Sig * B) / t["smeas"], fc=gc / gobs)
def run(mode, tag="A_c2b_refit", fR=1.5, **kw):
    x = [one(g, fR * g["hR"], mode, tag, **kw) for g in gal.values()]; x = [a for a in x if a]; return dict(n=len(x), r=float(np.median([a["r"] for a in x])), Y=float(np.median([a["Y"] for a in x])), B=float(np.median([a["B"] for a in x])), fc=float(np.median([a["fc"] for a in x])), rs=[a["r"] for a in x])
R = {}
k = run("x", nohalo=True); P(f"K0 no halo r {k['r']:.3f} Y {k['Y']:.3f}")
SAT["on"] = False; k = run("x"); R["K1"] = k; P(f"K1 denominator off: r {k['r']:.3f} Y_K {k['Y']:.3f} n {k['n']} (UR3 1.071, 0.287, 28)"); SAT["on"] = True
for lab, kw in (("1.5 hR", dict()), ("2.2 hR", dict(fR=2.2)), ("B bg", dict(tag="B_cfg886_bg")), ("delta -0.05", dict(d=-0.05)), ("lgMb -0.1", dict(dl=-0.1)), ("lgMb +0.1", dict(dl=0.1))):
    a = run("x", **kw); R[lab] = a; P(f"  {lab:12s} r {a['r']:.3f} Y_K {a['Y']:.3f} B {a['B']:.3f} halo share {a['fc']:.2f} n {a['n']}")
SAT["ms"] = 0.1; a = run("x"); R["MUT"] = a; P(f"MUTATE M* x 0.1: r {a['r']:.3f} Y_K {a['Y']:.3f}"); SAT["ms"] = 1.0
b = R["1.5 hR"]; rs = np.array(b["rs"]); bs = np.median(np.random.default_rng(1).choice(rs, (4000, len(rs))), axis=1); P(f"primary r {b['r']:.3f} [{np.percentile(bs, 16):.3f}, {np.percentile(bs, 84):.3f}], n {b['n']}: " + ("NOT DECIDED" if b["n"] < 27 else "REACHED" if 0.9 <= b["r"] <= 1.1 else "NOT REACHED"))
json.dump(R, open(os.path.join(HERE, "sr2_diskmass.json"), "w"), indent=1); open(os.path.join(HERE, "sr2_diskmass.out"), "w").write("\n".join(OUT) + "\n")
