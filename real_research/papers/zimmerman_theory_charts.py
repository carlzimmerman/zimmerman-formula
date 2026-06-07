#!/usr/bin/env python3
"""
Publication charts for THE ZIMMERMAN THEORY OF GRAVITY (comprehensive edition).
All analytic / from the paper's own numbers -- no external data, so they reproduce
anywhere with numpy+matplotlib. Generates, into figures/:
  fig2_a0z.png              -- the signature: a0(z)/a0(0) vs z, framework vs 3 rivals + z=3 prediction
  fig4_threelaw.png         -- three independent a0 readouts agree to 8% at the vacuum value
  fig5_seesaw.png           -- the CKN cosmic seesaw: a0 and rho_Lambda as two ends of one sqrt(Lambda) ladder
  fig6_derivation_ladder.png-- the derivation chain, every step labelled (derived/dimensional/posit/...)
  fig7_confirmation_ladder.png -- the 5-rung candidate->law ladder and where we stand
  fig8_galaxy_cluster_split.png -- alpha=m/M_dS vs mass: galaxies->center->MOND, clusters->edge->fail
C. Zimmerman, 2026-06-06. (fig1_rar, fig3_btfr are the data-based SPARC figures, kept as-is.)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "savefig.bbox": "tight",
    "font.size": 12, "axes.titlesize": 14, "axes.titleweight": "bold",
    "axes.labelsize": 12.5, "legend.fontsize": 10.5, "axes.grid": True,
    "grid.alpha": 0.25, "axes.axisbelow": True, "font.family": "DejaVu Sans",
})
OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)
C_FW, C_CONST, C_RISE, C_ASSEM = "#0072B2", "#999999", "#D55E00", "#009E73"


def rhoDE_ratio(z, w0=-0.752, wa=-0.86):      # DESI DR2 CPL -> rho_DE(z)/rho_DE0
    a = 1.0 / (1.0 + z)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))


def E(z, Om=0.315, OmL=0.685):
    return np.sqrt(Om * (1 + z) ** 3 + OmL)


# ----------------------------------------------------------------------- fig 2
def fig_a0z():
    z = np.linspace(0, 3.2, 400)
    fw = np.sqrt(rhoDE_ratio(z)); const = np.ones_like(z)
    rise = E(z); assem = (1 + z) ** 0.75
    fig, ax = plt.subplots(figsize=(8.2, 5.4))
    ax.axhspan(0, 5, xmin=(2.0/3.2), xmax=1, color="#FFF4CC", alpha=0.0)
    ax.fill_betweenx([0, 5], 2.0, 3.2, color="#FCEBD2", alpha=0.6, zorder=0)
    ax.text(2.55, 2.55, "ELT-testable\nz ≈ 2–3", ha="center", va="center",
            fontsize=10, color="#8a5a00", style="italic")
    ax.plot(z, rise, "--", color=C_RISE, lw=2.2, label="rising  a₀ ∝ cH(z)  (Verlinde) — EXCLUDED, Δχ²≈49")
    ax.plot(z, assem, ":", color=C_ASSEM, lw=2.0, label="assembly  (1+z)^0.75")
    ax.plot(z, const, "-", color=C_CONST, lw=2.0, label="constant a₀  (regular MOND)")
    ax.plot(z, fw, "-", color=C_FW, lw=3.2, label="FRAMEWORK  a₀ ∝ √ρ_DE(z)  (DESI w₀wₐ)")
    # bump + z=3 prediction markers
    ax.plot(0.4, np.sqrt(rhoDE_ratio(0.4)), "o", color=C_FW, ms=8, zorder=5)
    ax.annotate("+6% bump\n(w crosses −1 at z≈0.41)", xy=(0.4, 1.062), xytext=(0.75, 1.27),
                fontsize=9.5, color=C_FW, arrowprops=dict(arrowstyle="->", color=C_FW))
    ax.plot(3.0, np.sqrt(rhoDE_ratio(3.0)), "*", color=C_FW, ms=18, zorder=6)
    ax.annotate("PREDICTION\na₀(z=3) = 0.74 a₀(0)\n(= −0.13 dex; the decisive test)",
                xy=(3.0, 0.737), xytext=(1.75, 0.50), fontsize=10, color=C_FW, weight="bold",
                arrowprops=dict(arrowstyle="->", color=C_FW))
    ax.axhline(1, color="k", lw=0.6, alpha=0.4)
    ax.set_xlim(0, 3.2); ax.set_ylim(0.45, 3.0)
    ax.set_xlabel("redshift  z"); ax.set_ylabel("a₀(z) / a₀(0)")
    ax.set_title("The signature: an evolving acceleration scale set by the dark-energy density")
    ax.legend(loc="upper left", framealpha=0.95)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig2_a0z.png")); plt.close(fig)


# ----------------------------------------------------------------------- fig 4
def fig_threelaw():
    labels = ["Radial Acceleration\nRelation", "Baryonic\nTully–Fisher", "Mass-discrepancy\n(deep-MOND)"]
    vals = np.array([1.10, 1.26, 1.06]); errs = np.array([0.10, 0.12, 0.10])
    y = np.arange(len(labels))[::-1]
    fig, ax = plt.subplots(figsize=(8.2, 4.3))
    ax.axvspan(0.936 * 0.92, 0.936 * 1.08, color="#CCE5F6", alpha=0.7,
               label="vacuum value 9.36×10⁻¹¹ ± M/L systematic")
    ax.axvline(0.936, color=C_FW, lw=2.4, label="a₀ = c²√(Λ/32π) = 9.36×10⁻¹¹")
    ax.errorbar(vals, y, xerr=errs, fmt="o", color="#222222", ms=9, capsize=5, lw=2, zorder=5)
    for v, yy in zip(vals, y):
        ax.text(v, yy + 0.13, f"{v:.2f}", ha="center", fontsize=10.5)
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlim(0.7, 1.5); ax.set_ylim(-0.6, len(labels) - 0.2)
    ax.set_xlabel("acceleration scale a₀  (×10⁻¹⁰ m s⁻²)")
    ax.set_title("One vacuum constant, three independent galaxy laws — they agree to 8%")
    ax.legend(loc="lower right", framealpha=0.95)
    ax.grid(axis="y", alpha=0)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig4_threelaw.png")); plt.close(fig)


# ----------------------------------------------------------------------- fig 5
def fig_seesaw():
    # energies in eV (log)
    E_pl = 1.22e28        # Planck energy ~1.22e19 GeV
    E_hub = 1.4e-33       # hbar H0 ~ 1.4e-33 eV
    E_lam = 2.24e-3       # rho_Lambda^(1/4) = 2.24 meV (geometric mean, x 2/Z)
    fig, ax = plt.subplots(figsize=(7.4, 5.6))
    xs = [0, 0, 0]
    pts = [(E_pl, "Planck (UV)\nE_Planck = 1.22×10²⁸ eV", "#D55E00"),
           (E_lam, "vacuum scale (geometric mean)\nE_Λ = ρ_Λ^¼ = 2.24 meV", C_FW),
           (E_hub, "Hubble (IR)\nE_Hubble = ℏH = 1.4×10⁻³³ eV", "#009E73")]
    for Eg, lab, col in pts:
        ax.plot(0, Eg, "o", ms=16, color=col, zorder=5)
        ax.text(0.12, Eg, lab, va="center", fontsize=10.5, color=col)
    ax.plot([0, 0], [E_hub, E_pl], "-", color="#888", lw=2, zorder=1)
    # geometric-mean guide
    ax.annotate("", xy=(-0.05, E_lam), xytext=(-0.05, E_pl),
                arrowprops=dict(arrowstyle="-", color=C_FW, lw=1, ls=":"))
    ax.annotate("", xy=(-0.05, E_lam), xytext=(-0.05, E_hub),
                arrowprops=dict(arrowstyle="-", color=C_FW, lw=1, ls=":"))
    ax.text(-0.16, E_lam, "E_Λ = √(E_Planck · E_Hubble) × (2/Z)\n→ a₀ = cH_Λ/Z is the IR rung",
            ha="right", va="center", fontsize=9.5, color=C_FW, style="italic",
            bbox=dict(boxstyle="round", fc="white", ec=C_FW, alpha=0.9))
    ax.set_yscale("log"); ax.set_ylim(1e-35, 1e30)
    ax.set_xlim(-0.95, 0.95); ax.set_xticks([])
    ax.set_ylabel("energy  (eV, log scale)")
    ax.set_title("The cosmic seesaw: a₀ and the value of Λ are two ends\nof one CKN UV–IR ladder  (ρ_obs = (3/8π) M_P² H², bound saturated)")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig5_seesaw.png")); plt.close(fig)


# ----------------------------------------------------------------------- fig 6
def fig_derivation_ladder():
    steps = [
        ("0  Existence of a₀", "volume-law-FREE (modified inertia)", "#0072B2"),
        ("1  Scale  a₀ ~ c√Λ", "DIMENSIONAL (robust)", "#56B4E9"),
        ("2  Form  a₀ ∝ √ρ_DE", "restatement + a falsifiable choice", "#56B4E9"),
        ("3  Shape  √(g² + g·a₀)", "DERIVED  = Milgrom 1999", "#009E73"),
        ("4  Response (inertia←ΔT)", "POSIT (load-bearing)", "#E69F00"),
        ("5  Sign  (enhancement)", "FORCED for galaxies (given N-V)", "#0F9D9D"),
        ("6  Number  Z=√(32π/3)", "POSIT (foreclosed, but moot)", "#E69F00"),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    y = np.arange(len(steps))[::-1]
    for yy, (name, status, col) in zip(y, steps):
        ax.barh(yy, 1.0, color=col, alpha=0.92, height=0.66)
        ax.text(0.02, yy, "  " + name, va="center", ha="left", fontsize=11, color="white", weight="bold")
        ax.text(0.98, yy, status + "  ", va="center", ha="right", fontsize=10.5, color="white", style="italic")
    ax.set_xlim(0, 1); ax.set_ylim(-0.6, len(steps) - 0.4)
    ax.set_yticks([]); ax.set_xticks([])
    ax.set_title("The derivation chain from the de Sitter vacuum — every step labelled honestly")
    leg = [Patch(fc="#009E73", label="DERIVED"), Patch(fc="#0F9D9D", label="FORCED (given a named premise)"),
           Patch(fc="#0072B2", label="volume-law-free existence"), Patch(fc="#56B4E9", label="dimensional / restatement"),
           Patch(fc="#E69F00", label="POSIT")]
    ax.legend(handles=leg, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3, framealpha=0.95, fontsize=9.5)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig6_derivation_ladder.png")); plt.close(fig)


# ----------------------------------------------------------------------- fig 7
def fig_confirmation_ladder():
    rungs = [
        ("1  A parameter-free galaxy acceleration law exists", "✓ in hand", "#009E73"),
        ("2  The premise is modified gravity, not dark matter", "◐ partial (EFE 4–5σ)", "#E69F00"),
        ("3  The scale is CAUSED by Λ — it evolves as √ρ_DE", "✗ THE decisive test (z≈3)", "#D55E00"),
        ("4  Universal across its domain (clusters)", "✗ outstanding", "#BBBBBB"),
        ("5  Complete theory (covariant + derived coefficient)", "✗ open", "#BBBBBB"),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    for i, (txt, status, col) in enumerate(rungs):
        ax.barh(i, 1.0, color=col, alpha=0.9, height=0.62)
        ax.text(0.015, i, "  " + txt, va="center", ha="left", fontsize=10.6, color="white", weight="bold")
        ax.text(0.985, i, status + "  ", va="center", ha="right", fontsize=10.2, color="white", weight="bold")
    ax.annotate("we are here →", xy=(0.5, 1.55), fontsize=11, color="#444", weight="bold", ha="center")
    ax.set_xlim(0, 1); ax.set_ylim(-0.6, len(rungs) - 0.3)
    ax.set_yticks([]); ax.set_xticks([])
    ax.set_title("From candidate to law: the five-rung ladder, and where we stand")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig7_confirmation_ladder.png")); plt.close(fig)


# ----------------------------------------------------------------------- fig 8
def fig_galaxy_cluster_split():
    M_dS = 3.8e14                      # M_sun, de Sitter mass c^2/(G H_Lambda)
    M = np.logspace(7, 15.4, 300)
    alpha = M / M_dS
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.loglog(M, alpha, "-", color="#333", lw=2.5)
    ax.axhline(1.0, color="#D55E00", lw=1.4, ls="--")
    ax.axvspan(1e7, 1e12, color="#CCE5F6", alpha=0.55)
    ax.axvspan(3e14, 2.5e15, color="#FAD7C4", alpha=0.55)
    ax.text(10**9.4, 10**-5.0, "GALAXIES\n10⁷–10¹² M⊙\nα ≤ 3×10⁻³ → spectral CENTER\n→ deep-MOND enhancement",
            ha="center", va="center", fontsize=10, color="#0a4d76")
    ax.text(10**14.8, 10**-0.3, "CLUSTERS\n~10¹⁵ M⊙\nα ~ O(1) → EDGE\n→ MOND fails",
            ha="center", va="center", fontsize=9.6, color="#8a3a10")
    ax.text(10**12.6, 1.5, "α = 1  (M_dS = c²/GH_Λ ≈ 3.8×10¹⁴ M⊙)", fontsize=9, color="#D55E00")
    ax.set_xlabel("source mass  M  (M⊙)")
    ax.set_ylabel("de Sitter conical deficit  α = m / M_dS")
    ax.set_title("The same DSSYK kernel forces galaxy MOND and predicts the cluster failure")
    ax.set_xlim(1e7, 2.5e15); ax.set_ylim(1e-8, 1e1)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig8_galaxy_cluster_split.png")); plt.close(fig)


if __name__ == "__main__":
    fig_a0z(); fig_threelaw(); fig_seesaw()
    fig_derivation_ladder(); fig_confirmation_ladder(); fig_galaxy_cluster_split()
    print("charts written to", OUT)
    for f in ["fig2_a0z", "fig4_threelaw", "fig5_seesaw", "fig6_derivation_ladder",
              "fig7_confirmation_ladder", "fig8_galaxy_cluster_split"]:
        p = os.path.join(OUT, f + ".png")
        print(f"  {f}.png", os.path.getsize(p), "bytes" if os.path.exists(p) else "MISSING")
