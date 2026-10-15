#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
make_figure.py -- the single figure of `mnras_a0_lambda_short.tex` (two panels, page width).
    (a) log10[a0(z)/a0(0)] for the three predictions of Section 4.1.
    (b) the error amplification A_obs, A_bar of Section 4.2 against y = g_bar/a0.
Every curve is computed here from the formulas printed in the paper; the only numbers read from a file are the four
gate-halo points of panel (a) and the RC100 y-range of panel (b), both from the committed
../mnras_submission_2026_v3/paper_numbers.json.
Run:  python3 make_figure.py
"""
import os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
PN = json.load(open(os.path.join(HERE, "..", "mnras_submission_2026_v3", "paper_numbers.json")))

plt.rcParams.update({"font.family": "STIXGeneral", "font.size": 8, "axes.labelsize": 9, "legend.fontsize": 7.5,
                     "xtick.labelsize": 8, "ytick.labelsize": 8, "axes.linewidth": 0.6, "lines.linewidth": 1.4,
                     "xtick.direction": "in", "ytick.direction": "in", "xtick.top": True, "ytick.right": True,
                     "mathtext.fontset": "stix", "pdf.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
BLACK, ORANGE, SKY, GREEN, BLUE, VERM, GREY = "#000000", "#E69F00", "#56B4E9", "#009E73", "#0072B2", "#D55E00", "#7f7f7f"

OM, OL, H = 0.315, 0.685, 0.674


def E(z):
    return np.sqrt(OM * (1 + z) ** 3 + OL)


def c200_dm14(z, M=1e12):
    a = 0.520 + 0.385 * np.exp(-0.617 * z ** 1.21)
    b = -0.101 + 0.026 * z
    return 10 ** (a + b * np.log10(M / (1e12 / H)))


def f(x):
    return np.log(1 + x) - x / (1 + x)


def delta_halo(z, M=1e12):
    c0, cz = c200_dm14(0.0, M), c200_dm14(z, M)
    return (4 / 3) * np.log10(E(z)) + np.log10((cz ** 2 / f(cz)) / (c0 ** 2 / f(c0)))


def n_of_y(y):
    s = np.sqrt(y)
    return -(s / 2) / np.expm1(s)


fig, (ax, bx) = plt.subplots(1, 2, figsize=(6.97, 2.1), gridspec_kw={"wspace": 0.28})

# ---- (a) three predictions
z = np.linspace(0, 3.5, 200)
ax.axhline(0, color=BLACK, lw=2.0, label=r"tied to $\Lambda$: constant")
ax.plot(z, np.log10(E(z)), color=VERM, ls="--", label=r"tied to $\rho_{\rm crit}$: $a_0\propto H(z)$")
ax.plot(z, delta_halo(z), color=BLUE, ls="-.", label=r"$\Lambda$CDM haloes, $10^{12}\,{\rm M_\odot}$")
gz = [0.0] + [row["z"] for row in PN["S4"]["laws"]]
gv = [0.0] + [row["gate"] for row in PN["S4"]["laws"]]
ax.plot(gz, gv, "o", color=BLUE, ms=3.5, mfc="white", label=r"$\Lambda$CDM haloes of the gated discs")
ax.set_xlim(0, 3.5)
ax.set_ylim(-0.08, 0.95)
ax.set_xlabel(r"redshift $z$")
ax.set_ylabel(r"$\Delta(z)=\log_{10}[a_0(z)/a_0(0)]$")
ax.legend(loc="upper left", frameon=False, handlelength=2.4)
ax.set_title("(a)", loc="left", fontsize=9)

# ---- (b) amplification
y = np.logspace(-2.3, 1.2, 300)
Aobs = 1 / np.abs(n_of_y(y))
Abar = Aobs - 1
yn = PN["S5_native"]["y_native"]
bx.axvspan(10 ** -2.3, 0.3, color=GREEN, alpha=0.18, lw=0)
bx.axvspan(yn["p16"], yn["p84"], color=GREY, alpha=0.25, lw=0)
bx.plot(y, Aobs, color=BLACK, label=r"$A_{\rm obs}=1/|n|$  (velocity)")
bx.plot(y, Abar, color=BLACK, ls="--", label=r"$A_{\rm bar}=1/|n|-1$  (baryonic mass)")
bx.set_xscale("log")
bx.set_yscale("log")
bx.set_xlim(10 ** -2.3, 10 ** 1.2)
bx.set_ylim(0.9, 30)
bx.set_xlabel(r"$y=g_{\rm bar}/a_0$")
bx.set_ylabel("error amplification")
bx.text(0.0065, 18, "proposed\ngate", color="#00684a", fontsize=7.5, va="top")
bx.text(1.15, 18, "RC100\n(central 68%)", color="#444444", fontsize=7.5, va="top")
bx.legend(loc="lower right", frameon=False, bbox_to_anchor=(1.0, 0.0), handlelength=2.4)
bx.set_title("(b)", loc="left", fontsize=9)

out = os.path.join(HERE, "fig1_laws_amplification.pdf")
fig.savefig(out)
print("wrote", out)
# the two spot values the caption relies on
assert abs(float(np.log10(E(2.5))) - 0.576) < 5e-4
assert abs(float(delta_halo(2.5)) - PN["S4"]["laws"][2]["dm14"]) < 6e-3, (delta_halo(2.5), PN["S4"]["laws"][2]["dm14"])
print("spot checks passed: Delta_H(2.5) = %.3f, Delta_halo(2.5, 1e12) = %.3f" % (np.log10(E(2.5)), delta_halo(2.5)))
