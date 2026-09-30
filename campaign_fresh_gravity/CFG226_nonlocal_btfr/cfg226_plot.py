#!/usr/bin/env python3
"""CFG226 figure: the record's nonlocal point-source relation G M = v^4/a0 + (pi beta/2) v^2 against SPARC's baryonic Tully-Fisher relation.  Reads cfg226_nonlocal_btfr_results.json.
The relation is the far-field amplitude of an ideal point source in a declared phenomenological model; fixed-a0 curves use the framework's two footings; no law verdict."""
import os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LANE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(LANE, "cfg226_nonlocal_btfr_results.json")))
d = J["data"]; R = J["results"]["fiducial"]
G = 6.6743e-11; MSUN = 1.98847e30; KPC = 3.0856775814913673e19


def Mmod(v, a0, b):
    v = np.asarray(v) * 1e3
    return np.log10((v ** 4 / a0 + (math.pi * b * KPC / 2) * v ** 2) / G / MSUN)


v = np.array(d["v"]); logM = np.array(d["logM"]); sM = np.array(d["sM"]); ev = np.array(d["ev"])
fig, (ax, bx) = plt.subplots(1, 2, figsize=(15, 6.4), gridspec_kw=dict(width_ratios=[1.35, 1.0], wspace=0.22))
ax.errorbar(np.log10(v), logM, xerr=ev, yerr=sM, fmt="o", ms=3.6, color="#1d4e89", ecolor="#9db7d5", elinewidth=0.8, alpha=0.85, zorder=2, label=f"SPARC, {len(v)} galaxies (Upsilon = 0.5)")
vv = np.logspace(math.log10(15), math.log10(350), 200)
F1 = R["F1"]["fit"]
ax.plot(np.log10(vv), Mmod(vv, 9.3603e-11, 0.0), color="#888888", ls=":", lw=2, label="beta = 0, a0 = 9.36e-11 (canonical footing)")
ax.plot(np.log10(vv), Mmod(vv, 1.1312e-10, 0.0), color="#888888", ls="-.", lw=2, label="beta = 0, a0 = 1.13e-10 (alt footing)")
f4a0 = R["F1"]["fit"]["a0"]
ax.plot(np.log10(vv), Mmod(vv, 1.58e-10, 0.0), color="k", lw=2, label="beta = 0, a0 free (1.58e-10): the plain BTFR")
ax.plot(np.log10(vv), Mmod(vv, F1["a0"], F1["beta"]), color="#d62828", lw=2.4, label=f"M given v: beta = {F1['beta']:.2f} kpc, a0 = {F1['a0']:.2e}")
ax.plot(np.log10(vv), Mmod(vv, 1.709e-10, 0.0988), color="#e07b00", lw=2.4, label="v given M (post hoc): beta = 0.10 kpc, a0 = 1.71e-10")
ax.set_xlabel("log10 v_flat (km/s)", fontsize=12); ax.set_ylabel(r"log10 $M_{bar}$ ($M_\odot$)", fontsize=12)
ax.set_xlim(1.15, 2.55); ax.set_ylim(6.3, 12.3)
ax.grid(True, color="#cccccc", lw=0.5, alpha=0.7); ax.legend(loc="upper left", fontsize=8.6, framealpha=0.93)
ax.set_title("the relation against the SPARC BTFR", fontsize=12, loc="left")
Ms = np.logspace(6, 12, 200)
def a0inf(M, a0, b):
    eta = math.pi * b * KPC * math.sqrt(a0) / (4 * math.sqrt(G * M * MSUN))
    return 1.0 / (math.sqrt(1 + eta * eta) + eta) ** 2
for b, a0, c, lab in ((0.2615, F1["a0"], "#d62828", "beta = 0.26 kpc (M given v fit)"), (R["F1"]["limits"]["up95"], F1["a0"], "#d62828", "95% upper limit 0.39 kpc"), (0.0988, 1.709e-10, "#e07b00", "beta = 0.10 kpc (v given M, post hoc)")):
    bx.plot(np.log10(Ms), [a0inf(M, a0, b) for M in Ms], color=c, lw=2.2, ls="-" if "upper" not in lab else "--", label=lab)
bx.axhline(1, color="k", lw=0.8)
bx.set_xlabel(r"log10 $M_{bar}$ ($M_\odot$)", fontsize=12); bx.set_ylabel(r"predicted $a_{0,inferred}/a_0$ = $(\sqrt{1+\eta^2}-\eta)^2$", fontsize=11.5)
bx.set_ylim(0, 1.05); bx.grid(True, color="#cccccc", lw=0.5, alpha=0.7); bx.legend(loc="lower right", fontsize=9, framealpha=0.93)
bx.set_title("what the relation predicts at low mass", fontsize=12, loc="left")
fig.suptitle("The record's nonlocal relation  G M = v^4/a0 + (pi beta/2) v^2  against the SPARC baryonic Tully-Fisher relation (far-field amplitude of an ideal point source; no law verdict)", fontsize=11.5, x=0.06, ha="left", y=0.995)
fig.text(0.06, 0.012, "beta is fitted with a0 free: the M-given-v fit prefers beta = 0.26 kpc, the v-given-M fit 0.10 kpc, and beta = 0 for Upsilon = 0.7 or gas-dominated galaxies in that direction;\n"
         "with a0 fixed at the framework's footings beta = 0 (95% upper limit 0.05 to 0.07 kpc). A plain-BTFR slope below 4 has other causes (Upsilon, distances, pressure support).", fontsize=8.8, va="bottom", ha="left", linespacing=1.4)
fig.subplots_adjust(left=0.06, right=0.985, top=0.90, bottom=0.15)
out = os.path.join(LANE, "cfg226_nonlocal_btfr.png")
fig.savefig(out, dpi=150); print("wrote", out)
