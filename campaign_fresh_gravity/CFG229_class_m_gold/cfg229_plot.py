#!/usr/bin/env python3
"""CFG229 figure (plot only, from the committed results JSONs; no new analysis).
LEFT: the radial-acceleration plane (g_bar, g_obs in m/s^2) with the z = 0 RAR for FLAT (nu_mono, canonical footing), the same RAR with a0 x E(z) and x the PROXY at z = 2.0 and 2.9, the floor g_obs = g_bar,
and the seven class-M galaxies (horizontal bars: the joint gas + stellar band on g_bar, thick = inner, thin = outer; vertical: the velocity error).
RIGHT: the implied a0 scale s* (vs the canonical footing 9.3603e-11 m/s^2) against z with the four laws' curves and the z ~ 0 footings band; galaxies with NO ROOT (D <= 1) are triangles at the floor.
Descriptive compilation; class-M gas; calibration-limited; not a detection.  LambdaCDM has no a0: the purple curve is an effective-a0 PROXY.  kappa = 1/2 FITTED."""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
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

R = json.load(open(os.path.join(LANE, "cfg229_score_results.json")))
PF = json.load(open(os.path.join(LANE, "cfg229_preflight_results.json")))
ST = pd.read_csv(os.path.join(LANE, "cfg229_inputs_static.csv"))
KN = pd.read_csv(os.path.join(LANE, "cfg229_inputs_kin.csv"))
A0 = K.A0["canonical"]; A0ALT = K.A0["alt"]
NU = K.nu_mono
OM = 0.315
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
gid = R["gid"]; z = np.array(R["z"]); GO = np.array(R["GO"]); GB = np.array(R["GB"]); n = len(gid)

fig, (ax, bx) = plt.subplots(1, 2, figsize=(15.5, 6.6), gridspec_kw=dict(width_ratios=[1.0, 1.0]))
# ---------------------------------------------------------------- left
x = np.logspace(-12, -7, 400)
ax.plot(x, x, color="0.55", lw=1, ls="-", label="Newtonian floor g_obs = g_bar (every law has nu >= 1)")
ax.plot(x, x * NU(x / A0), color="#1f77b4", lw=2, label="FLAT a0 (z = 0 RAR, nu_mono, canonical footing)")
ax.plot(x, x * NU(x / A0ALT), color="#1f77b4", lw=1, ls="--", label="FLAT, alt footing 1.131e-10")
for zz, ls in ((2.0, "-"), (2.9, ":")):
    ax.plot(x, x * NU(x / (A0 * E(zz))), color="#d62728", lw=1.5, ls=ls, label=f"a0 ~ H(z) at z = {zz}")
    ax.plot(x, x * NU(x / (A0 * Z1.lcdm_native(zz))), color="#9467bd", lw=1.5, ls=ls, label=f"LCDM effective-a0 PROXY at z = {zz}")
cm = plt.cm.viridis
zmin, zmax = 2.0, 2.95
for i in range(n):
    c = cm((z[i] - zmin) / (zmax - zmin))
    # the band corners on g_bar are re-derived with the same closed form as the scorer (asserted equal at the nominal baryons to 1e-9)
    from scipy.special import i0e, i1e, k0e, k1e
    G_KPC, G2SI, XN = 4.30091e-6, 1e6 / 3.0856775814913673e19, 1.678
    def gb(ts, tg):
        Ms, Mg, Re, Rr = ST["Mstar"][i] * 10 ** ts, 10 ** (ST["logMgas_He"][i] + tg), ST["Re_kpc"][i], ST["R_kpc"][i]
        Rd = Re / XN; y = Rr / (2 * Rd)
        return (Ms + Mg) * 2 * G_KPC / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y)) / Rr * G2SI
    assert abs(gb(0.0, 0.0) / GB[i] - 1) < 1e-9, (gid[i], gb(0.0, 0.0), GB[i])
    lo_o, hi_o = gb(-0.30, -0.093), gb(+0.30, +0.093)
    lo_i, hi_i = gb(-ST["e_logMstar_inner"][i], -0.03), gb(ST["e_logMstar_inner"][i], 0.03)
    ax.plot([lo_o, hi_o], [GO[i], GO[i]], color=c, lw=1, alpha=0.8)
    ax.plot([lo_i, hi_i], [GO[i], GO[i]], color=c, lw=4, alpha=0.9, solid_capstyle="butt")
    sV = ST["sigV_dex"][i]
    ax.errorbar([GB[i]], [GO[i]], yerr=[[GO[i] * (1 - 10 ** (-sV))], [GO[i] * (10 ** sV - 1)]], color=c, lw=1.2, capsize=2)
    if np.isfinite(ST["e_i_used"][i]):
        iu, ei = ST["i_used"][i], ST["e_i_used"][i]
        f_lo = (math.sin(math.radians(iu)) / math.sin(math.radians(min(85.0, iu + ei)))) ** 2
        f_hi = (math.sin(math.radians(iu)) / math.sin(math.radians(max(5.0, iu - ei)))) ** 2
        ax.plot([GB[i] * 1.06, GB[i] * 1.06], [GO[i] * f_lo, GO[i] * f_hi], color=c, lw=1, ls="--", alpha=0.8)
    ax.plot([GB[i]], [GO[i]], marker="D", ms=9, color=c, mec="k", mew=0.8, ls="none")
    ax.annotate(gid[i].replace("ALPAKA", "A").replace("_", " "), (GB[i], GO[i]), textcoords="offset points", xytext=(6, 6), fontsize=8)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(2e-11, 5e-7); ax.set_ylim(2e-11, 5e-7)
ax.set_xlabel("g_bar  [m/s^2]   (thin exponential disc, stars + 1.36 x Dunne+22 logMH2)"); ax.set_ylabel("g_obs = V^2/R  [m/s^2]")
ax.set_title("class-M galaxies in the RAR plane\n(horizontal bars: joint gas + stellar band, thick inner / thin outer; vertical: velocity error solid, ALPAKA inclination dashed)", fontsize=8.5)
ax.legend(fontsize=7, loc="upper left")
sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(zmin, zmax)); cb = fig.colorbar(sm, ax=ax, pad=0.01, fraction=0.04); cb.set_label("z")
# ---------------------------------------------------------------- right
zz = np.linspace(0, 3.3, 200)
bx.axhspan(1.0, A0ALT / A0, color="0.85", label="z ~ 0: both footings 9.36e-11 / 1.131e-10 (record)")
bx.plot(zz, np.ones_like(zz), color="#1f77b4", lw=2, label="FLAT")
bx.plot(zz, [E(v) for v in zz], color="#d62728", lw=2, label="a0 ~ H(z) (the rival)")
bx.plot(zz, [Z1.lcdm_native(v) for v in zz], color="#9467bd", lw=2, label="LCDM effective-a0 PROXY (not LCDM)")
def R_dec(zv, w0=-0.838, wa=-0.62):
    return math.sqrt((1.0 + zv) ** (3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * zv / (1.0 + zv)))
bx.plot(zz, [R_dec(v) for v in zz], color="#2ca02c", lw=2, label="a0 ~ sqrt(rho_DE), DESI CPL (record's w0, wa)")
IMP = R["IMPL"]
for i in range(n):
    g = gid[i]; r = IMP[g]; zi = z[i]
    if r["s0"][1]:
        bx.plot([zi], [0.045], marker="v", ms=9, color="0.25", ls="none", label="no root (D <= 1)")
    else:
        q = r["stat"]["q"]
        s0 = 10 ** r["s0"][0]
        bx.errorbar([zi], [s0], yerr=[[s0 - 10 ** q[1]], [10 ** q[3] - s0]], color="k", lw=3, capsize=0, zorder=5)
        bx.errorbar([zi], [s0], yerr=[[s0 - 10 ** q[0]], [10 ** q[4] - s0]], color="k", lw=1, capsize=3, zorder=5)
        cs = [v for v in list(r["corners"].values()) + list(r["variants"].values()) if not v[1]]
        lo, hi = min(10 ** v[0] for v in cs), max(10 ** v[0] for v in cs)
        bx.plot([zi + 0.03, zi + 0.03], [lo, hi], color="#ff7f0e", lw=5, alpha=0.8, zorder=4, label="ALESS 122.1 systematic envelope")
        bx.plot([zi], [s0], marker="D", ms=9, color="k", mec="w", zorder=6, label="ALESS 122.1 implied a0 (stat: 68% thick, 95% thin)")
        bx.annotate("ALESS 122.1", (zi, s0), textcoords="offset points", xytext=(12, -14), fontsize=8, bbox=dict(fc="w", ec="none", alpha=0.85))
bx.set_yscale("log"); bx.set_xlim(0, 3.3); bx.set_ylim(0.03, 40)
bx.text(2.6, 0.06, "no root (D <= 1): ALPAKA 15, 18, 19, 20, 22 and SINS BX610", ha="center", fontsize=7)
bx.set_xlabel("z"); bx.set_ylabel("implied a0 scale s*  (a0 / 9.3603e-11 m/s^2)")
bx.set_title("implied a0: 6 of 7 have NO ROOT (D <= 1, triangles at the floor); descriptive, not a verdict", fontsize=10)
h, l = bx.get_legend_handles_labels(); seen = {}
for hh, ll in zip(h, l):
    seen.setdefault(ll, hh)
bx.legend(seen.values(), seen.keys(), fontsize=7, loc="lower left", bbox_to_anchor=(0.0, 0.12))
fig.suptitle("CFG229: the class-M sample (seven z >= 2 galaxies with a Dunne+22 per-galaxy optimised multi-tracer gas mass)", fontsize=12)
fig.text(0.5, 0.005, "descriptive compilation; class-M gas; calibration-limited; not a detection; not a verdict.  criteria 5c131c037 + Addendum 1 7e3b14d20; blind pre-flight e3f30dee5 (flat vs H(z) and vs the proxy NOT POSSIBLE in every set). LCDM has no a0; kappa = 1/2 is FITTED.",
         ha="center", fontsize=7.5)
fig.tight_layout(rect=(0, 0.02, 1, 0.97))
fig.savefig(os.path.join(LANE, "cfg229_class_m.png"), dpi=140)
print("wrote cfg229_class_m.png")
