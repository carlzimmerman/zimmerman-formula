#!/usr/bin/env python3
"""LW1 DiskMass (FROZEN_CRITERIA.md part 4): the law's nu on CFG576's data and UR3's estimator; form R (round) and form A (QUMOND one-zone). Writes lw1_dm.json. kappa = 1/2 FITTED; not theory closed."""
import contextlib, io, json, math, os
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); S576 = os.path.join(RB, "..", "campaign_fresh_gravity", "CFG576_diskmass_sigz", "cfg576_diskmass.py"); n = {"__file__": os.path.abspath(S576), "__name__": "h"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(S576).read().split('P("=" * 100)')[0], "h", "exec"), n)
gal, terms, K_V, sexp, gbar, G = n["gal"], n["galaxy_terms"], n["K_VERT"], n["sexp"], n["gbar"], n["G"]; KU = 3.0857e13; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def nus(y): y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)
def num(y): y = np.maximum(y, 1e-30); return 1.0 / (-np.expm1(-np.sqrt(y)))
def one(g, R, a0, nu, form):
    n["gal_BD"] = g["BD"]; t = terms(g, R); gobs = t["vrot"] ** 2 / R; f = (lambda Y: gbar(t, R, Y) - gobs) if form == "N" else (lambda Y: nu(gbar(t, R, Y) / a0) * gbar(t, R, Y) - gobs)
    try: Y = brentq(f, 0.02, 5.0)
    except ValueError: return None
    gb = gbar(t, R, Y); Sig = Y * t["I0"] * math.exp(-R / t["hR"]) + sexp(R, t["Ma"], 2 * t["hR"]) + sexp(R, t["Mm"], t["hR"]); KN = 2 * math.pi * G * Sig * (1 - math.exp(-1))
    B = 1.0 if form == "N" else float(nu(math.hypot(gb, KN) / a0)) if form == "A" else 1 + (float(nu(gb / a0)) * gb - gb) * t["hz"] / R / KN
    return dict(Y=Y, B=B, r=math.sqrt(math.pi * G * K_V * t["hz"] * Sig * B) / t["smeas"])
def run(a0, nu, form, fR=1.5):
    x = [one(g, fR * g["hR"], a0, nu, form) for g in gal.values()]; x = [a for a in x if a]; rs = np.array([a["r"] for a in x]); bs = np.median(np.random.default_rng(576).choice(rs, size=(2000, len(rs))), axis=1)
    return dict(r=float(np.median(rs)), lo=float(np.percentile(bs, 16)), hi=float(np.percentile(bs, 84)), Y=float(np.median([a["Y"] for a in x])), B=float(np.median([a["B"] for a in x])), n=len(x))
A = dict(canonical=9.3603e-11, alt=1.1312e-10); R = {}; P("LW1 DiskMass, UR3's estimator, CFG576's data; line r 0.90-1.10, n >= 27; kappa = 1/2 FITTED; not theory closed")
k = run(0, nus, "N"); R["K5_noextra"] = k; c = {f: {m: run(v * KU, num, m) for m in ("R", "A")} for f, v in dict(canonical=9.36e-11, alt=1.13e-10).items()}; R["K5_cfg576"] = c
d = max(abs(c["canonical"]["R"]["r"] - 1.250), abs(c["canonical"]["A"]["r"] - 1.475), abs(c["alt"]["R"]["r"] - 1.212), abs(c["alt"]["A"]["r"] - 1.475), abs(k["r"] - 1.494), abs(k["Y"] - 0.821)); R["K5_d"] = d; P(f"K5 no extra r {k['r']:.3f} Y {k['Y']:.3f} (1.494, 0.821); CFG576 nu: RM {c['canonical']['R']['r']:.3f}/{c['alt']['R']['r']:.3f}, PD {c['canonical']['A']['r']:.3f}/{c['alt']['A']['r']:.3f}; max |d| {d:.1e}: {'PASS' if d <= 1e-3 else 'FAIL'}")
def lab(x): return "PASS" if 0.90 <= x["r"] <= 1.10 and x["n"] >= 27 else "FAIL"
for f, a in A.items():
    R[f] = {}
    for form, nm in (("R", "form R, round"), ("A", "form A, QUMOND one-zone")):
        for tag, ax, fR in (("1.5", 1.0, 1.5), ("2.2", 1.0, 2.2), ("MUTATE", 1.5, 1.5)):
            x = run(a * ax * KU, nus, form, fR); x["label"] = lab(x); R[f][f"{form}|{tag}"] = x; P(f"[{f}] {nm:24s} {tag:7s} r {x['r']:.3f} [{x['lo']:.3f}, {x['hi']:.3f}] Y_K {x['Y']:.3f} B {x['B']:.2f} n {x['n']}: {x['label']}")
json.dump(R, open(os.path.join(HERE, "lw1_dm.json"), "w"), indent=1); open(os.path.join(HERE, "lw1_dm.out"), "w").write("\n".join(OUT) + "\n")
