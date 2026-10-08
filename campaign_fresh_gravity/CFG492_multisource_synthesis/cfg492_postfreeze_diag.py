#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG492 POST-FREEZE DIAGNOSTICS (labelled; written after the frozen run was seen; they change no frozen verdict).
Attacks on the MASS PROPERTY verdict:
  D1 an analytic check of the general-density Jeans solver (Hernquist tracer in its own Newtonian Hernquist potential, isotropic;
     Hernquist 1990 eq. 10 for sigma_r^2) -- the frozen C2 only tested the r^-3 identity;
  D2 the PN tracer slope: power-law rho ~ r^-3 and r^-3.5 instead of the Hernquist starlight profile;
  D3 leave-one-galaxy-out on M_PN and D;
  D4 the 2.5-sigma clip per galaxy (the frozen reported row moved M_PN most);
  D5 matched radii: both tracers restricted to bins inside the common radial interval of that galaxy.
"""
import os, sys, math, json, runpy, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(s=""):
    print(s); OUT.append(str(s))

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    try:
        M = runpy.run_path(os.path.join(HERE, "cfg492_gc_vs_pn.py"), run_name="cfg492_main")
    except SystemExit as e:
        M = None
if M is None:   # run_path raises SystemExit after populating; re-run capturing globals without exit
    src = open(os.path.join(HERE, "cfg492_gc_vs_pn.py")).read().replace("sys.exit(0 if all(checks) else 1)", "pass")
    g = {"__file__": os.path.join(HERE, "cfg492_gc_vs_pn.py"), "__name__": "cfg492_main"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, "cfg492_gc_vs_pn.py", "exec"), g)
    M = g
# the exec above rewrote the main outputs with identical content (same seed); nothing else is written by it
G, KPC, MSUN, RG = M["G"], M["KPC"], M["MSUN"], M["RG"]
PAIR, A0, RES = M["PAIR"], M["A0"], M["RES"]

P("=" * 110); P("CFG492 POST-FREEZE DIAGNOSTICS (labelled; no frozen verdict changes)"); P("=" * 110)

# D1 analytic Hernquist check
Mh, a = 1e11, 3.0
gN = G * Mh * MSUN / (RG + a) ** 2 / KPC ** 2
rho = lambda r: 1.0 / (r * (r + a) ** 3)
s2num = M["s2_general"](gN, rho, 0.0)
x = RG / a
GMa = G * Mh * MSUN / (a * KPC)
with np.errstate(all="ignore"):
    s2an = GMa * (12 * x * (x + 1) ** 3 * np.log((x + 1) / x) - x / (x + 1) * (25 + 52 * x + 42 * x ** 2 + 12 * x ** 3)) / 12.0
sel = (RG > 0.1 * a) & (RG < 30 * a)
d1 = float(np.max(np.abs(0.5 * np.log10(s2num[sel] / s2an[sel]))))
P(f"D1 Hernquist analytic sigma_r (0.1-30 a): max |log10 sigma_num/sigma_an| = {d1:.2e} dex  -> {'PASS' if d1 < 0.002 else 'FAIL'}")

res = {"D1": d1}
for foot, a0 in A0.items():
    P("\n" + "-" * 110); P(f"footing {foot}"); P("-" * 110)
    r = RES[foot]
    # D2
    for gam in (3.0, 3.5):
        vals = []
        for n in PAIR:
            mod = M["model"](n, a0)
            b = M["bins_of"](M["PNc"][n], n)
            rf = lambda rr, gg=gam: rr ** -gg
            vals.append(M["offset_of"](b, M["proj"](b["Rb"], M["s2_general"](mod["g"], rf), rf)))
        P(f"D2 PN tracer rho ~ r^-{gam}: M_PN = {np.mean(vals):+.4f} (galaxy-to-galaxy err {np.std(vals, ddof=1)/math.sqrt(len(vals)):.4f}); "
          f"D = {np.mean(np.array(vals) - np.array([r[n]['O_GC'] for n in PAIR])):+.4f}")
        res[f"D2_{foot}_gamma{gam}"] = vals
    # D3
    op = np.array([r[n]["O_PN"] for n in PAIR]); og = np.array([r[n]["O_GC"] for n in PAIR])
    P("D3 leave-one-out:")
    for i, n in enumerate(PAIR):
        k = np.arange(len(PAIR)) != i
        mp, ep = op[k].mean(), op[k].std(ddof=1) / math.sqrt(k.sum())
        dd = op[k] - og[k]; md, ed = dd.mean(), dd.std(ddof=1) / math.sqrt(k.sum())
        P(f"   without NGC{n:<5}: M_PN {mp:+.4f} +- {ep:.4f} ({mp/ep:+.2f} sigma); D {md:+.4f} +- {ed:.4f}")
    # D4
    P("D4 2.5-sigma clip per galaxy (O_PN 3-sigma -> 2.5-sigma, N_clean):")
    for n in PAIR:
        P(f"   NGC{n:<5}: {r[n]['O_PN']:+.3f} -> {r[n]['O_PN_clip25']:+.3f}   N {len(M['PNc'][n])} -> {len(M['PNc_25'][n])}")
    # D5 matched radii
    vp, vg = [], []
    for n in PAIR:
        Rp, Rg = np.array(r[n]["RPN"]), np.array(r[n]["RGC"])
        lo, hi = max(Rp.min(), Rg.min()), min(Rp.max(), Rg.max())
        mod = M["model"](n, a0)
        bp = M["bins_of"](M["PNc"][n], n); bg = M["bins_of"](M["GCc"][n], n)
        ah = mod["ah"]; rh = lambda rr: 1.0 / (rr * (rr + ah) ** 3); r3 = lambda rr: rr ** -3.0
        sp = M["proj"](bp["Rb"], M["s2_general"](mod["g"], rh), rh); sg = M["proj"](bg["Rb"], M["s2_general"](mod["g"], r3), r3)
        mp = (bp["Rb"] >= lo) & (bp["Rb"] <= hi); mg = (bg["Rb"] >= lo) & (bg["Rb"] <= hi)
        if mp.any() and mg.any():
            vp.append(float(np.mean(np.log10(bp["Sb"][mp] / sp[mp])))); vg.append(float(np.mean(np.log10(bg["Sb"][mg] / sg[mg]))))
            P(f"   D5 NGC{n:<5} common {lo:5.1f}-{hi:5.1f} kpc: O_PN {vp[-1]:+.3f} ({mp.sum()} bins)  O_GC {vg[-1]:+.3f} ({mg.sum()} bins)")
        else:
            P(f"   D5 NGC{n:<5} no bins in the common interval")
    if vp:
        dd = np.array(vp) - np.array(vg)
        P(f"D5 matched radii (N {len(vp)}): M_PN {np.mean(vp):+.4f}, M_GC {np.mean(vg):+.4f}, D {dd.mean():+.4f} +- {dd.std(ddof=1)/math.sqrt(len(dd)):.4f}")
    res[f"D5_{foot}"] = dict(PN=vp, GC=vg)

json.dump(res, open(os.path.join(HERE, "cfg492_postfreeze_diag_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg492_postfreeze_diag.out"), "w").write("\n".join(OUT) + "\n")
