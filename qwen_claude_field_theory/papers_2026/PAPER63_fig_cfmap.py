#!/usr/bin/env python3
"""PAPER63 figure: CF1's c_f map. For each graded line, the grid c_f values at which it passes on both footings, against the
switch threshold (X43 crossover) each c_f implies. Read-only: rebuild_2026_10_22/CF1_cf_window_map/cf1_window_results.json."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
J = json.load(open(os.path.join(ROOT, "rebuild_2026_10_22", "CF1_cf_window_map", "cf1_window_results.json")))
GRID = sorted(float(k[3:]) for k in J if k.startswith("cf_"))
XO = {cf: J[f"cf_{cf:g}"]["crossover"] for cf in GRID}
LINES = ["lensing", "groups", "G-OUT-M3", "G-IN-Mall", "SPARC line", "dwarfs MW ultra-faint"]
LAB = {"lensing": "KiDS isolated-lens lensing", "groups": "groups (63, Tian+)", "G-OUT-M3": "cluster outskirts, top gas-mass tercile",
       "G-IN-Mall": "cluster centres, all 326", "SPARC line": "SPARC (both backgrounds)", "dwarfs MW ultra-faint": "MW ultra-faint dwarfs"}
passing = J["line_pass_cf"]


def build(path):
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for i, ln in enumerate(LINES):
        ok = set(passing.get(ln, GRID))
        for cf in GRID:
            ax.scatter(cf, i, s=70, marker="o" if cf in ok else "x", color="#1b7f3b" if cf in ok else "#b3261e", zorder=3)
    ax.set_yticks(range(len(LINES))); ax.set_yticklabels([LAB[l] for l in LINES], fontsize=8)
    ax.set_xlabel(r"formation concentration $c_f$ (one number)", fontsize=9)
    ax.set_xlim(GRID[0] - 0.2, GRID[-1] + 0.2); ax.invert_yaxis(); ax.grid(axis="x", alpha=0.3)
    top = ax.twiny(); top.set_xlim(ax.get_xlim()); top.set_xticks(GRID)
    top.set_xticklabels([f"{XO[cf]['canonical']:.2f}" for cf in GRID], fontsize=7)
    top.set_xlabel(r"switch threshold $\log_{10}(M_\times/M_\odot)$, canonical footing", fontsize=8)
    ax.scatter([], [], marker="o", color="#1b7f3b", label="passes on both footings"); ax.scatter([], [], marker="x", color="#b3261e", label="fails on a footing")
    ax.legend(loc="lower left", bbox_to_anchor=(-0.62, -0.32), fontsize=7, frameon=False, ncol=2)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)
    return {"grid": GRID, "crossover": XO, "passing": passing}


if __name__ == "__main__":
    out = build(os.path.join(HERE, "PAPER63_fig_cfmap.pdf"))
    build(os.path.join(HERE, "PAPER63_fig_cfmap.png"))
    print(json.dumps({"grid": out["grid"]}, indent=0))
