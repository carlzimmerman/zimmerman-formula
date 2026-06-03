#!/usr/bin/env python3
"""Figures for the z~3 a0-measurement observing-proposal paper. Vector PDFs in ../figures/."""
import os, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

OM, OL = 0.315, 0.685
E = lambda z: np.sqrt(OM*(1+z)**3 + OL)
OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "figures"))
os.makedirs(OUT, exist_ok=True)


def fig1_prediction():
    zz = np.linspace(0, 6, 240)
    zd  = np.array([0.00, 0.05, 0.90]); a0d = np.array([1.36, 1.69, 2.38]); a0e = np.array([0.26, 0.13, 0.11])
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.plot(zz, E(zz), "b-", lw=2.3, label=r"framework: $a_0(z)/a_0(0)=E(z)$")
    ax.axhline(1, color="0.5", ls=":", lw=1.6, label="constant $a_0$ (null)")
    ax.errorbar(zd, a0d/1.36, yerr=a0e/1.36, fmt="o", color="0.35", ms=6, capsize=3,
                lw=1.4, label="current data (~2$\\sigma$ hint)")
    # the proposed z=3 measurement: framework value with a 7% error bar (a ~25-galaxy sample)
    z3 = 3.0; a3 = E(z3); s3 = 0.07*a3
    ax.errorbar([z3], [a3], yerr=[s3], fmt="*", color="crimson", ms=18, capsize=4, lw=2.2,
                label="proposed $z{=}3$ measurement (~25 gal, 7%)")
    ax.annotate("constant-$a_0$ predicts\nthis point at 1.0\n(0.66 dex below)",
                xy=(z3, 1.0), xytext=(3.4, 1.9), fontsize=8.5, color="0.3",
                arrowprops=dict(arrowstyle="->", color="0.5"))
    ax.set_xlabel("redshift $z$"); ax.set_ylabel(r"$a_0(z)\,/\,a_0(0)$")
    ax.set_title("The decisive lever arm: $a_0$ at $z{=}3$ is $4.6\\times$ local (or $1\\times$ if constant)")
    ax.set_xlim(0, 6); ax.set_ylim(0.7, 11); ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.25)
    plt.tight_layout(); plt.savefig(os.path.join(OUT, "z3_fig1_prediction.pdf")); plt.close()


def fig2_samplesize():
    dlogE = np.log10(E(3.0)); s_gal = 0.15
    N = np.linspace(3, 120, 300)
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    for s_anchor, c, lab in [(0.09, "firebrick", "current anchor $\\sigma{=}0.09$ dex (M/L-limited)"),
                             (0.03, "seagreen", "tightened anchor $\\sigma{=}0.03$ dex (gas-rich)")]:
        sig = dlogE/np.sqrt((s_gal/np.sqrt(N))**2 + s_anchor**2)
        ax.plot(N, sig, color=c, lw=2.3, label=lab)
    for s in (3, 5):
        ax.axhline(s, color="0.6", ls=":", lw=1.1); ax.text(112, s+0.1, f"{s}$\\sigma$", fontsize=9, color="0.4")
    ax.axvline(15, color="0.7", ls="--", lw=1); ax.text(15.5, 1.0, "~15 gal", fontsize=8.5, color="0.45")
    ax.set_xlabel("number of $z{\\sim}3$ extended, deep-MOND galaxies")
    ax.set_ylabel("significance of constant-$a_0$ rejection")
    ax.set_title("Few galaxies suffice — but the current $z{=}0$ anchor caps it at ~7$\\sigma$")
    ax.set_xlim(0, 120); ax.set_ylim(0, 12); ax.legend(fontsize=9, loc="lower right"); ax.grid(alpha=0.25)
    plt.tight_layout(); plt.savefig(os.path.join(OUT, "z3_fig2_samplesize.pdf")); plt.close()


def main():
    fig1_prediction(); fig2_samplesize()
    print("figures ->", OUT)
    print(f"  E(3)={E(3):.2f}  a0(z=3)/a0(0)={E(3):.2f}  log10E(3)={np.log10(E(3)):.2f} dex")


if __name__ == "__main__":
    main()
