#!/usr/bin/env python3
"""CFG516 figure: (a) MW K_z cells, dchi2 vs NFW for PD / RM / homeoid MUTATE; (b) SPARC rms vs a0 for ALG / PD / RMphi / RMv;
(c) edge-on prediction, nu_z^2 PD/RM at R_last, HSB vs LSB. Reads the committed JSON outputs only."""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
mw = json.load(open(os.path.join(HERE, "cfg516_mw_results.json")))
mwm = json.load(open(os.path.join(HERE, "cfg516_mw_results_MUTATE.json")))
sp = json.load(open(os.path.join(HERE, "cfg516_sparc_results.json")))

fig, ax = plt.subplots(1, 3, figsize=(16, 5))
# (a)
cells = [c for c in mwm["cells"] if c["rm"] == "RMphi"]
cv = {(c["baryon"], c["foot"], c["var"]): c for c in mwm["cells"] if c["rm"] == "RMv"}
lab = [f"{c['baryon'].split('_')[0]} {c['foot'][:3]} {c['var']}" for c in cells]
x = np.arange(len(cells))
pd = [c["d_PD_vs_N"] for c in cells]
rphi = [c["d_RM_vs_N"] for c in cells]
rv = [cv[(c["baryon"], c["foot"], c["var"])]["d_RM_vs_N"] for c in cells]
mut = [c["d_RM_vs_N"] + c["d_MUT_minus_RM"] for c in cells]
ax[0].plot(x, pd, "s", color="#c0392b", label="PD (QUMOND phantom disc)")
ax[0].plot(x, mut, "v", color="#8e44ad", label="MUTATE: RM-phi mass in q=0.3 homeoid")
ax[0].plot(x, rphi, "o", color="#2471a3", label="RM-phi (round)")
ax[0].plot(x, rv, "D", color="#17a589", ms=4, label="RM-v (round)")
ax[0].axhline(0, color="k", lw=0.8); ax[0].axhline(4, color="grey", ls=":", lw=0.8)
ax[0].set_yscale("symlog", linthresh=10); ax[0].set_xticks(x); ax[0].set_xticklabels(lab, rotation=75, fontsize=7)
ax[0].set_ylabel("chi2(K_z,1.1) - chi2(NFW)  [Bovy & Rix, 43 MAPs]"); ax[0].set_title("(a) MW: round vs disc, 4 baryon models"); ax[0].legend(fontsize=7)
# (b)
a0g = np.geomspace(5e-11, 2e-10, 31)
for mn, col in (("ALG", "k"), ("PD", "#c0392b"), ("RMphi", "#2471a3"), ("RMv", "#17a589")):
    ax[1].plot(a0g, sp["free"][mn]["rms_curve"], color=col, label=f"{mn}: a0 {sp['free'][mn]['a0']:.2e}")
for a, l in ((9.36e-11, "canonical"), (1.13e-10, "alt")):
    ax[1].axvline(a, color="grey", ls=":", lw=0.8)
ax[1].set_xscale("log"); ax[1].set_xlabel("a0 [m/s^2]"); ax[1].set_ylabel("weighted rms log g_obs/g_model [dex]")
ax[1].set_title(f"(b) SPARC Q<=2 ({sp['n_gal']} gal, {sp['n_pts']} pts)"); ax[1].legend(fontsize=8)
# (c)
pg = sp["per_gal"]
ax[2].set_title("(c) edge-on: nu_z^2(PD)/nu_z^2(RM-phi) at R_last, canonical")
vals_all = []
for name, r in pg.items():
    v = r["vert"]["canonical"]["Rlast"]
    vals_all.append(v["nuz2_PD"] / v["nuz2_RMphi"])
ax[2].hist(np.clip(vals_all, 0, 8), bins=30, color="#5d6d7e")
ax[2].axvline(np.median(vals_all), color="k", ls="--", label=f"median {np.median(vals_all):.2f}")
ax[2].set_xlabel("vertical frequency^2 ratio, phantom disc / round"); ax[2].set_ylabel("galaxies"); ax[2].legend()
plt.tight_layout()
plt.savefig(os.path.join(HERE, "cfg516_round_rule.png"), dpi=130)
print("wrote cfg516_round_rule.png")
