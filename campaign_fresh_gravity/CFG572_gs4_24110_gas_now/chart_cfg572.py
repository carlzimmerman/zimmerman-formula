#!/usr/bin/env python3
"""CFG572 chart: GS4_24110's predicted (CFG571, frozen) vs measured (CFG572) gas mass, Delta_v per model, and the two line spectra."""
import os, json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "cfg572_gas_results.json")))
M, P5, DV, SP = R["measured"], R["cfg571"], R["delta_v"], R["spectra"]
MOD = ["F-DESI", "F-flat", "R-H", "L-fb(RAR-eq)"]
LAB = {"F-DESI": "framework\na0∝√ρ_DE", "F-flat": "framework\nflat a0", "R-H": "rival\na0 ∝ H(z)", "L-fb(RAR-eq)": "ΛCDM+fb\nRAR-equiv."}
COL = {"F-DESI": "#1a9988", "F-flat": "#2c7bb6", "R-H": "#d7301f", "L-fb(RAR-eq)": "#8c510a"}
FT = {"canon 9.36e-11": ("canon a0 9.36e-11", "o"), "alt 1.13e-10": ("alt a0 1.13e-10", "s")}
fig = plt.figure(figsize=(20, 7.2)); gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 1.0, 1.0], wspace=0.30)

# --- panel A: gas mass, predicted vs measured ---
ax = fig.add_subplot(gs[0]); FLOORY = 8.75
for i, mn in enumerate(MOD):
    for j, lm in enumerate(("10.89", "10.76")):
        for k, (fn, (fl, mk)) in enumerate(FT.items()):
            v = P5[lm][f"{fn}|{mn}"]; x = i + (j - 0.5) * 0.36 + (k - 0.5) * 0.14
            if v is None: ax.plot(x, FLOORY, marker="v", ms=9, color=COL[mn], mfc="white" if lm == "10.76" else COL[mn], mew=1.5)
            else: ax.plot(x, v, marker=mk, ms=9, color=COL[mn], mfc="white" if lm == "10.76" else COL[mn], mew=1.5)
d = M["DUST"]["logM"]["alphaCO 4.36 (primary)"]
ax.axhspan(d - 0.2, d + 0.2, color="#7f7f7f", alpha=0.18, lw=0); ax.axhline(d, color="#555", lw=1.6)
ax.text(3.62, d, "dust (Boogaard+20 L850)\n10.51 ± 0.2", fontsize=8.5, va="center", ha="left", color="#333")
co = M["CO43"]["logM"]; ax.axhspan(co["r41 0.55"], co["r41 0.25"], color="#984ea3", alpha=0.15, lw=0); ax.axhline(co["r41 0.37"], color="#984ea3", lw=1.6)
ax.text(3.62, co["r41 0.37"], f"CO(4–3) measured, 17σ\n{co['r41 0.37']:.2f} (r41 0.25–0.55)", fontsize=8.5, va="center", ha="left", color="#6a2c75")
ci = M["CI10"]["logM"]["X_CI 1.9e-5"]; ax.annotate("", xy=(3.5, ci - 0.25), xytext=(3.5, ci), arrowprops=dict(arrowstyle="-|>", color="#e08214", lw=2))
ax.plot([3.35, 3.65], [ci, ci], color="#e08214", lw=2.2)
ax.text(3.62, ci - 0.12, f"[CI](1–0) not detected\n< {ci:.2f} (3σ)", fontsize=8.5, va="center", ha="left", color="#a65f00")
ax.axhline(FLOORY + 0.12, color="#999", lw=0.7, ls=":")
ax.text(-0.45, FLOORY - 0.17, "▼ = FLOOR: the stars alone already exceed what this model allows (no gas permitted)", fontsize=8, color="#444")
ax.set_xticks(range(4)); ax.set_xticklabels([LAB[m] for m in MOD], fontsize=9)
ax.set_xlim(-0.55, 4.9); ax.set_ylim(8.5, 11.4); ax.set_ylabel("total gas mass  log M_gas [M☉]", fontsize=11)
ax.set_title("A. Gas required (frozen first) vs measured", fontsize=11, loc="left", fontweight="bold")
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], marker="o", ls="", color="k", label="M★ 10.89 (KMOS3D)"), Line2D([], [], marker="o", ls="", mfc="white", color="k", label="M★ 10.76 (RC100)"),
                   Line2D([], [], marker="o", ls="", color="#777", label="circle = canon a0, square = alt a0")], fontsize=8, loc="upper left", frameon=False)

# --- panel B: Delta_v ---
ax = fig.add_subplot(gs[1])
for i, mn in enumerate(MOD):
    for j, (lm, rn) in enumerate((("10.89", "DUST a4.36"), ("10.76", "DUST a4.36"), ("10.89", "CO43 r41 0.37"), ("11.1", "DUST a4.36"))):
        e = DV[f"{lm}|{rn}|canon 9.36e-11|{mn}"]; x = i + (j - 1.5) * 0.17
        mk = {0: "o", 1: "o", 2: "D", 3: "^"}[j]; mf = "white" if j in (1, 3) else COL[mn]
        ax.errorbar(x, e["dv"], yerr=2 * e["err"], fmt=mk, ms=8, color=COL[mn], mfc=mf, capsize=3, lw=1.2, alpha=0.55 if j == 3 else 1)
for lm, ls in (("10.89", "-"), ("10.76", "--")):
    nw = DV[f"{lm}|DUST a4.36|Newton-max"]["dv"]; ax.axhline(nw, color="#555", ls=ls, lw=1)
ax.text(3.45, DV["10.89|DUST a4.36|Newton-max"]["dv"] - 0.05, "Newton, no dark matter\n(dust gas; solid M★ 10.89, dashed 10.76)", fontsize=7.5, ha="right", va="top", color="#444")
ax.axhline(0, color="k", lw=1.4); ax.axhspan(-0.6, 0, color="#2ca25f", alpha=0.05, lw=0)
ax.text(3.45, 0.74, "above 0 = more baryons\nthan the model allows", fontsize=8.5, color="#a50f15", ha="right", va="top")
ax.set_xticks(range(4)); ax.set_xticklabels([LAB[m] for m in MOD], fontsize=9); ax.set_xlim(-0.55, 3.55); ax.set_ylim(-0.35, 0.8)
ax.set_ylabel("Δ_v = log(V²_bar,measured / V²_bar,required) at R_e", fontsize=10.5)
ax.set_title("B. Too many baryons? (bars ±2σ)", fontsize=11, loc="left", fontweight="bold")
ax.legend(handles=[Line2D([], [], marker="o", ls="", color="k", label="dust gas, M★ 10.89"), Line2D([], [], marker="o", ls="", mfc="white", color="k", label="dust gas, M★ 10.76"),
                   Line2D([], [], marker="D", ls="", color="k", label="CO(4–3) gas, M★ 10.89"), Line2D([], [], marker="^", ls="", mfc="white", color="k", alpha=0.55, label="dust gas, M★ 11.1 (post-freeze)")],
          fontsize=8, loc="upper left", bbox_to_anchor=(0, 0.93), frameon=False)

# --- panel C: spectra ---
ax = fig.add_subplot(gs[2])
for ln, c, off, lab in (("CO43", "#984ea3", 0.0, "CO(4–3)"), ("CI10", "#e08214", -1.6, "[CI](1–0)")):
    v = np.array(SP[ln]["v"]); s = np.array(SP[ln]["spec"]) * 1e3; o = np.argsort(v); v, s = v[o], s[o]
    k = 12; sb = np.convolve(s, np.ones(k) / k, mode="same")
    ax.step(v, sb + off * 1e0, where="mid", color=c, lw=1.3)
    ax.text(-1450, off + (0.75 if ln == "CO43" else -1.25), f"{lab}: {SP[ln]['S']:.2f} ± {SP[ln]['sig']:.2f} Jy km/s", color=c, fontsize=9.5, fontweight="bold")
    ax.axhline(off, color="#bbb", lw=0.7)
ax.axvspan(-300, 300, color="#ffd166", alpha=0.25, lw=0); ax.set_xlim(-1500, 1500)
ax.set_xlabel("velocity about z = 1.9975 [km/s]", fontsize=10.5); ax.set_ylabel("aperture flux [mJy], ~45 km/s smoothing (offset)", fontsize=10)
ax.set_title("C. Public ALMA spectra (1.5″ aperture)", fontsize=11, loc="left", fontweight="bold")

fig.suptitle("GS4_24110 (z = 2.0): baryons fill almost the whole rotation.  With the dust gas mass the framework (and plain Newton) fit; a larger a0 at z ≈ 2 does not.\nWith the CO(4–3) gas mass every model has too many baryons.  One galaxy, a demonstration.",
             fontsize=13, fontweight="bold", x=0.5, y=1.02)
fig.text(0.5, 0.005, "CFG571 predictions frozen before data (259f7825c); CFG572 criteria 9c60f25ad. Gas tracers disagree by ~0.7 dex (CO(4–3) vs [CI] limit), so the gas amount is the weak link; "
         "M★ systematics ~0.2 dex. ΛCDM itself is NOT tested (a baryon-dominated inner disc is allowed); 'ΛCDM+feedback' here is CFG565's RAR-equivalent scale. κ = ½ fitted; cold mass still required.",
         fontsize=8.3, ha="center", color="#555", wrap=True)
plt.savefig(os.path.join(HERE, "cfg572_gs4_24110_chart.png"), dpi=130, bbox_inches="tight")
print("written")
