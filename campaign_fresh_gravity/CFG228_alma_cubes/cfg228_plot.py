#!/usr/bin/env python3
"""CFG228 figure (plot only, from the committed results JSONs; no new analysis).
LEFT: the radial-acceleration plane (g_bar, g_obs in m/s^2) with the z = 0 RAR for FLAT (nu_mono, canonical footing), the same RAR with a0 x E(z) and x the PROXY at z = 4.2 and 5.5, the floor g_obs = g_bar, and the six ALPINE rotators (circles) and
SPT0418-47 (diamond); horizontal bars = the joint gas + stellar band on g_bar (thick inner, thin outer), vertical bars = the velocity error.
RIGHT: the implied a0 scale s* (vs the canonical footing 9.3603e-11 m/s^2) against z with the four laws' curves and the z ~ 0 footings band; statistical bars black (68% thick, 95% thin), the systematic envelope of the band corners in orange, no-root galaxies as triangles at the floor.
Descriptive compilation; two un-optimised tracers; calibration-limited; not a detection; not a verdict.  LambdaCDM has no a0: the purple curve is an effective-a0 PROXY.  kappa = 1/2 FITTED."""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG4_common as K
sys.path.insert(0, os.path.join(REPO, "sonnet55_push", "puzzle_32pi", "agents", "Z1_causal_horizon_a0z"))
import zcommon as Z1

R = json.load(open(os.path.join(LANE, "cfg228_score_results.json")))
A0 = K.A0["canonical"]; A0ALT = K.A0["alt"]; NU = K.nu_mono
OM = 0.315
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
gid = R["gid"]; z = np.array(R["z"]); GO = np.array(R["GO"]); GB = np.array(R["GB"]); n = len(gid); EV = np.array(R["EV"]); V = np.array(R["V"])
BG = R["BANDS_GB"]

fig, (ax, bx) = plt.subplots(1, 2, figsize=(15.5, 6.8), gridspec_kw=dict(width_ratios=[1.0, 1.0]))
x = np.logspace(-12, -7, 400)
ax.plot(x, x, color="0.55", lw=1, label="Newtonian floor g_obs = g_bar (every law has nu >= 1)")
ax.plot(x, x * NU(x / A0), color="#1f77b4", lw=2, label="FLAT a0 (z = 0 RAR, nu_mono, canonical footing)")
ax.plot(x, x * NU(x / A0ALT), color="#1f77b4", lw=1, ls="--", label="FLAT, alt footing 1.131e-10")
for zz, ls in ((4.2, "-"), (5.5, ":")):
    ax.plot(x, x * NU(x / (A0 * E(zz))), color="#d62728", lw=1.5, ls=ls, label=f"a0 ~ H(z) at z = {zz}")
    ax.plot(x, x * NU(x / (A0 * Z1.lcdm_native(zz))), color="#9467bd", lw=1.5, ls=ls, label=f"LCDM effective-a0 PROXY at z = {zz}")
cm = plt.cm.viridis
LOFF = {"CG32": (-44, 10), "DC396844": (16, 14), "DC494057": (-70, 46), "DC881725": (-80, -10), "DC552206": (-26, -46), "VC5110377875": (12, -18), "SPT0418-47": (10, 10)}   # label offsets in points (two galaxies nearly coincide)
for i in range(n):
    c = cm((z[i] - 4.2) / (5.6 - 4.2))
    lo_o, hi_o = BG["joint +outer"][i], BG["joint -outer"][i]
    lo_i, hi_i = BG["joint +inner"][i], BG["joint -inner"][i]
    ax.plot([min(lo_o, hi_o), max(lo_o, hi_o)], [GO[i], GO[i]], color=c, lw=1, alpha=0.8)
    ax.plot([min(lo_i, hi_i), max(lo_i, hi_i)], [GO[i], GO[i]], color=c, lw=4, alpha=0.9, solid_capstyle="butt")
    ev = 2 * 0.4343 * EV[i] / V[i]
    ax.errorbar([GB[i]], [GO[i]], yerr=[[GO[i] * (1 - 10 ** (-ev))], [GO[i] * (10 ** ev - 1)]], color=c, lw=1.2, capsize=2)
    ax.plot([GB[i]], [GO[i]], marker="D" if gid[i] == "SPT0418-47" else "o", ms=9, color=c, mec="k", mew=0.8, ls="none")
    ax.annotate(gid[i].replace("VC5110377875", "VC5110"), (GB[i], GO[i]), textcoords="offset points", xytext=LOFF.get(gid[i], (6, 6)), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.5, color="0.35"), bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75))
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(1e-11, 2e-8); ax.set_ylim(1e-11, 2e-8)
ax.set_xlabel("g_bar  [m/s^2]   (ALPINE: thin disc, stars + [CII]/dust gas; SPT0418-47: stars point mass + gas disc)"); ax.set_ylabel("g_obs = V_c^2/R_out  [m/s^2]")
ax.set_title("ALMA sample in the RAR plane at R_out = 2 R_e,[CII] (SPT0418-47: 4 R_gas)\n(horizontal bars: joint gas + stellar band, thick inner / thin outer; vertical: velocity error)", fontsize=8.5)
ax.legend(fontsize=7, loc="upper left")
sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(4.2, 5.6)); cb = fig.colorbar(sm, ax=ax, pad=0.01, fraction=0.04); cb.set_label("z")

zz = np.linspace(0, 6.0, 300)
bx.axhspan(1.0, A0ALT / A0, color="0.85", label="z ~ 0: both footings 9.36e-11 / 1.131e-10 (record)")
bx.plot(zz, np.ones_like(zz), color="#1f77b4", lw=2, label="FLAT")
bx.plot(zz, [E(v) for v in zz], color="#d62728", lw=2, label="a0 ~ H(z) (the rival)")
bx.plot(zz, [Z1.lcdm_native(v) if v <= 5.0 else float("nan") for v in zz], color="#9467bd", lw=2, label="LCDM effective-a0 PROXY (not LCDM; to z = 5)")
R_dec = lambda zv, w0=-0.838, wa=-0.62: math.sqrt((1.0 + zv) ** (3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * zv / (1.0 + zv)))
bx.plot(zz, [R_dec(v) for v in zz], color="#2ca02c", lw=2, label="a0 ~ sqrt(rho_DE), DESI CPL (record's w0, wa)")
IMP = R["IMPL"]
SHIFT = {"CG32": -0.10, "DC396844": -0.03, "DC881725": 0.07, "VC5110377875": 0.10, "DC494057": 0.07, "DC552206": -0.07, "SPT0418-47": 0.0}   # display-only shift in z (legibility); the z values are in the results JSON
for i in range(n):
    g = gid[i]; r = IMP[g]; zi = z[i] + SHIFT.get(g, 0.0)
    if r["s0"][1]:
        bx.plot([zi], [0.04], marker="v", ms=9, color="0.25", ls="none", label="no root (D <= 1)")
        bx.annotate(g.replace("VC5110377875", "VC5110").replace("SPT0418-47", "SPT0418"), (zi, 0.04), textcoords="offset points", xytext=(-3, 8), fontsize=6.5, rotation=90)
        continue
    q = r["stat"]["q"]; s0 = 10 ** r["s0"][0]
    bx.errorbar([zi], [s0], yerr=[[max(s0 - 10 ** q[1], 0)], [10 ** q[3] - s0]], color="k", lw=3, capsize=0, zorder=5)
    bx.errorbar([zi], [s0], yerr=[[max(s0 - 10 ** q[0], 0)], [10 ** q[4] - s0]], color="k", lw=1, capsize=3, zorder=5)
    cs = [v for v in list(r["corners"].values()) + list(r["variants"].values()) if not v[1]]
    if cs:
        bx.plot([zi + 0.035, zi + 0.035], [min(10 ** v[0] for v in cs), max(10 ** v[0] for v in cs)], color="#ff7f0e", lw=5, alpha=0.8, zorder=4, label="systematic envelope (band corners + variants)")
    bx.plot([zi], [s0], marker="D" if g == "SPT0418-47" else "o", ms=8, color="k", mec="w", zorder=6, label="implied a0 (stat: 68% thick, 95% thin)")
    bx.annotate(g, (zi + 0.035, 2600), ha="center", va="top", rotation=90, fontsize=7)
for pn, lab in (("ALPINE6", "ALPINE6 pooled"), ("ALL7", "ALL7 pooled")):
    r = IMP.get(pn)
    if r and not r["s0"][1]:
        q = r["stat"]["q"]; s0 = 10 ** r["s0"][0]
        bx.errorbar([4.88 if pn == "ALPINE6" else 5.02], [s0], yerr=[[max(s0 - 10 ** q[1], 0)], [10 ** q[3] - s0]], color="m", lw=3)
        bx.plot([4.88 if pn == "ALPINE6" else 5.02], [s0], marker="s", ms=8, color="m", mec="w", label=f"{lab} (median rule)")
bx.set_yscale("log"); bx.set_xlim(0, 6.0); bx.set_ylim(0.012, 3000)
bx.set_xlabel("z"); bx.set_ylabel("implied a0 scale s*  (a0 / 9.3603e-11 m/s^2)")
nn = sum(1 for g in gid if IMP[g]["s0"][1])
bx.set_title(f"implied a0: {nn} of 7 have NO ROOT (D <= 1); descriptive, not a verdict", fontsize=10)
h, l = bx.get_legend_handles_labels(); seen = {}
for hh, ll in zip(h, l):
    seen.setdefault(ll, hh)
bx.legend(seen.values(), seen.keys(), fontsize=6.8, loc="lower left", ncol=1, framealpha=0.92)
fig.suptitle("CFG228: six ALPINE [CII] rotators (rotation from our own forward model) and SPT0418-47 (the authors' curve); gas from [CII] and dust, class S/L", fontsize=11.5)
fig.text(0.5, 0.005, "descriptive compilation; two un-optimised tracers; calibration-limited; not a detection; not a verdict; right panel: points shifted by <= 0.1 in z for legibility.  criteria 71ec12282; Stage 1 0694d7fc1; blind pre-flight 0c4c5778d; Stage 3 bb2caa47d. LCDM has no a0; kappa = 1/2 is FITTED.", ha="center", fontsize=7.5)
fig.tight_layout(rect=(0, 0.02, 1, 0.95))
fig.savefig(os.path.join(LANE, "cfg228_alma.png"), dpi=140)
print("wrote cfg228_alma.png")
