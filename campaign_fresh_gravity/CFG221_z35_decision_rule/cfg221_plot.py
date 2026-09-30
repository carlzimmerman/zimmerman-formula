#!/usr/bin/env python3
"""CFG221 figure: the operating characteristics of the frozen z > 3.5 decision rule on mocks (a description of THIS rule on THIS template, not a claim about any real sample).
Left: P(correct separation) against the number of discs N, REAL scatter, true gas-calibration offset c = 0 (solid) and drawn from the prior (dashed), flat truth (blue) and H(z) truth (orange),
with the frozen 0.8 feasibility line.  Middle: the same at c = 0 for the frozen prior width (scale 1) and the swept widths (scale 0.5 and 0.33).  Right: the rate of the WRONG separation
against the true offset c at N = 36, with the frozen 0.094 control line.  Reads cfg221_decision_rule_results.json and cfg221_prior_width_results.json.
Run: python3 campaign_fresh_gravity/CFG221_z35_decision_rule/cfg221_plot.py -> cfg221_operating_characteristics.png
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "cfg221_decision_rule_results.json")))["results"]
W = json.load(open(os.path.join(HERE, "cfg221_prior_width_results.json")))
K = 100
NG = (6, 13, 20, 30, 36, 50)


def main_rate(scen, truth, c, N):
    cnt = R[f"{scen}|{truth}|{c}|{N}|('nu_mono', 'canonical')|('FLAT', 'H(z)')"]
    return (cnt["LO"] if truth == "FLAT" else cnt["HI"]) / K, (cnt["HI"] if truth == "FLAT" else cnt["LO"]) / K


def sweep_rate(s, truth, c, N):
    cnt = W[f"{s}|{truth}|{c}|{N}"]
    return (cnt["LO"] if truth == "FLAT" else cnt["HI"]) / K


fig, ax = plt.subplots(1, 3, figsize=(17.5, 5.8))
for truth, col in (("FLAT", "#1f6fd1"), ("H(z)", "#d1541f")):
    for c, ls in ((0.0, "-"), ("PRIOR", "--")):
        ax[0].plot(NG, [main_rate("REAL", truth, c, N)[0] for N in NG], color=col, ls=ls, lw=2.2, marker="o", ms=4, label=f"{truth} true, c = {c}")
ax[0].axhline(0.8, color="0.25", lw=1.2); ax[0].text(50, 0.815, "frozen feasibility line 0.8", fontsize=8.5, ha="right")
ax[0].set_ylim(0, 1.02); ax[0].set_xlabel("number of discs N"); ax[0].set_ylabel("P(correct separation)"); ax[0].set_title("frozen rule (σ_dust = σ_CO = 0.30 dex), REAL scatter", fontsize=11)
ax[0].legend(fontsize=8.5, loc="center right", bbox_to_anchor=(1.0, 0.42)); ax[0].grid(alpha=0.25)
NS = (13, 20, 36, 50)
cols = {"1.0": "#2a2a2a", "0.5": "#2a9d8f", "0.33": "#e9a23b"}
for s, lab in (("1.0", "σ scale 1 (0.30 dex)"), ("0.5", "0.5 (0.15 dex)"), ("0.33", "0.33 (0.10 dex)")):
    y = [min(sweep_rate(s, "FLAT", 0.0, N), sweep_rate(s, "H(z)", 0.0, N)) for N in NS]
    ax[1].plot(NS, y, color=cols[s], lw=2.4, marker="o", label=lab)
ax[1].axhline(0.8, color="0.25", lw=1.2)
ax[1].set_ylim(0, 1.02); ax[1].set_xlabel("number of discs N"); ax[1].set_ylabel("min over the two truths of P(correct), c = 0")
ax[1].set_title("how well must the gas calibration be known? (Addendum 3 sweep)", fontsize=11); ax[1].legend(fontsize=9, loc="upper left"); ax[1].grid(alpha=0.25)
cs = (-0.60, -0.30, 0.0, 0.30, 0.60, "PRIOR")
xl = ["−0.6", "−0.3", "0", "+0.3", "+0.6", "prior"]
x = np.arange(len(cs)); w = 0.38
for j, (truth, col) in enumerate((("FLAT", "#1f6fd1"), ("H(z)", "#d1541f"))):
    ax[2].bar(x + (j - 0.5) * w, [main_rate("REAL", truth, c, 36)[1] for c in cs], w, color=col, label=f"{truth} true: wrong separation")
ax[2].axhline(0.094, color="0.25", lw=1.2); ax[2].text(-0.4, 0.099, "frozen control line 0.094", fontsize=8.5); ax[2].set_ylim(0, 0.115)
ax[2].set_xticks(x); ax[2].set_xticklabels(xl); ax[2].set_xlabel("true shared gas-calibration offset c (dex); ±0.3 = ±1σ of the frozen prior")
ax[2].set_ylabel("P(WRONG separation), N = 36"); ax[2].set_title("false separation against the true calibration", fontsize=11); ax[2].legend(fontsize=9); ax[2].grid(alpha=0.25, axis="y")
fig.suptitle("CFG221: operating characteristics of the frozen z > 3.5 decision rule on mocks (a description of this rule on this template; κ = ½ fitted)", fontsize=12)
plt.tight_layout(rect=(0, 0, 1, 0.95))
out = os.path.join(HERE, "cfg221_operating_characteristics.png")
plt.savefig(out, dpi=150)
print("wrote", os.path.basename(out))
