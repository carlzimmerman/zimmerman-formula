#!/usr/bin/env python3
"""
mi2026_figs.py -- two simple figures for MI_FIELD_THEORY_RESULTS_2026.md
  fig 1: the omega_c crossover window (planetary falsification lane numbers,
         verbatim from prep_2026/mi_planetary_falsification/{WINDOW,LOWEREDGE_FULLSPARC}.md)
  fig 2: the RAR landmark triplet (equation_book E1, exact closed forms)
No fitted numbers are produced here; every plotted number is copied from the
source .md files cited above. Exit 0 on success.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/papers/figs_mi2026"

# ----------------------------------------------------------------------
# FIGURE 1 -- the omega_c window (log frequency axis)
# Numbers verbatim from WINDOW.md / LOWEREDGE_FULLSPARC.md / SYNTHESIS.md:
#   action-forced corner  a0/2c = 1.56e-19 rad/s (canon)
#   horizon rate          H_Lambda = 1.807e-18 s^-1 (canon)
#   full-SPARC max deep-MOND orbital freq = 5.94e-15 rad/s  (UGC05721 innermost)
#   hardened window canon [1.78e-14, 2.21e-14], alt [1.78e-14, 1.83e-14]
#   planetary orbital band ~ 1e-9 (Neptune) .. 2.7e-8 (Saturn) .. 8.3e-7 (Mercury)
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.0, 3.2))
ax.set_xscale("log")
ax.set_xlim(3e-20, 3e-6)
ax.set_ylim(0, 1)
ax.set_yticks([])

# windows (canon and alt), drawn as bands
ax.axvspan(1.78e-14, 2.21e-14, ymin=0.52, ymax=0.88, color="#2b8cbe", alpha=0.85,
           label="allowed $\\omega_c$ window, canonical [1.78, 2.21]e-14")
ax.axvspan(1.78e-14, 1.83e-14, ymin=0.12, ymax=0.48, color="#e6550d", alpha=0.9,
           label="allowed $\\omega_c$ window, alt [1.78, 1.83]e-14  (x1.027)")

# markers
marks = [
    (1.56e-19, "action-forced corner\n$a_0/2c$ (RAR-dead)", "#636363"),
    (1.807e-18, "$H_\\Lambda$", "#636363"),
    (5.94e-15, "max deep-MOND\norbital freq (SPARC)", "#31a354"),
    (2.21e-14, "LLR $\\dot G/G$ ceiling\n(Biskupek 2021, canon)", "#756bb1"),
]
for x, lab, c in marks:
    ax.axvline(x, color=c, lw=1.4, ls="--", alpha=0.9)
    ax.text(x, 0.97, lab, rotation=0, ha="center", va="top", fontsize=7.5, color=c)

# planetary band
ax.axvspan(1e-9, 8.3e-7, ymin=0.30, ymax=0.70, color="#bdbdbd", alpha=0.5)
ax.text(3e-8, 0.5, "planetary orbital\nfrequencies", ha="center", va="center", fontsize=8)

ax.set_xlabel("$\\omega$  [rad s$^{-1}$]")
ax.set_title("The gated crossover: where $\\omega_c$ must sit (both footings)", fontsize=10)
ax.legend(loc="lower left", fontsize=7.5, framealpha=0.9)
fig.tight_layout()
fig.savefig(f"{OUT}/omega_c_window.png", dpi=180)
plt.close(fig)

# ----------------------------------------------------------------------
# FIGURE 2 -- the RAR landmark triplet (exact closed forms, equation_book E1)
#   sigma(y) = (2y+1)/(2(y+1)),  C(y) = y/(2(y+1)^2)
#   sum rule sigma(y)+sigma(1/y) = 3/2;  C(1/y) = C(y);  max at y=1: (3/4, 1/8)
# Comparison nu's evaluated numerically for the same landmarks.
# ----------------------------------------------------------------------
ell = np.linspace(-4, 4, 801)          # ell = ln y
y = np.exp(ell)

sigma_fw = (2*y + 1) / (2*(y + 1))
C_fw = y / (2*(y + 1)**2)

# McGaugh RAR-fit nu: g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0)))  -> slope/curv numerically
def slopes(gobs_of_y):
    ln_gobs = np.log(gobs_of_y(y) * y)   # g_obs/a0 = nu(y)*y
    s = np.gradient(ln_gobs, ell)
    c = np.gradient(s, ell)
    return s, c

nu_mcg = lambda yy: 1.0/(1.0 - np.exp(-np.sqrt(yy)))
nu_simple = lambda yy: 0.5 + np.sqrt(0.25 + 1.0/yy)
s_mcg, c_mcg = slopes(nu_mcg)
s_simp, c_simp = slopes(nu_simple)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.6))
a1.plot(ell, sigma_fw, color="#2b8cbe", lw=2, label="framework $\\nu=\\sqrt{1+1/y}$ (exact)")
a1.plot(ell, s_mcg, color="#e6550d", lw=1.4, ls="--", label="McGaugh RAR-fit $\\nu$")
a1.plot(ell, s_simp, color="#31a354", lw=1.4, ls=":", label="MOND 'simple' $\\nu$")
a1.axhline(0.75, color="k", lw=0.7, alpha=0.5)
a1.plot([0], [0.75], "o", color="#2b8cbe")
a1.annotate("$\\sigma(1)=3/4$", (0, 0.75), textcoords="offset points",
            xytext=(8, -12), fontsize=8)
a1.set_xlabel("$\\ln y$   ($y=g_{\\rm bar}/a_0$)")
a1.set_ylabel("log-log RAR slope $\\sigma$")
a1.set_title("slope: sum rule $\\sigma(y)+\\sigma(1/y)=3/2$ (framework only)", fontsize=9)
a1.legend(fontsize=7.5)

a2.plot(ell, C_fw, color="#2b8cbe", lw=2, label="framework (exact, even in $\\ln y$)")
a2.plot(ell, c_mcg, color="#e6550d", lw=1.4, ls="--", label="McGaugh (peak at $y=3.46$)")
a2.plot(ell, c_simp, color="#31a354", lw=1.4, ls=":", label="simple (peak at $y=2.00$)")
a2.plot([0], [0.125], "o", color="#2b8cbe")
a2.annotate("$C_{\\max}=1/8$ at $y=1$\n($g_{\\rm bar}=a_0$)", (0, 0.125),
            textcoords="offset points", xytext=(8, -22), fontsize=8)
a2.set_xlabel("$\\ln y$")
a2.set_ylabel("curvature $C=d\\sigma/d\\ln y$")
a2.set_title("curvature: even symmetry $C(1/y)=C(y)$, max $(3/4,\\,1/8)$", fontsize=9)
a2.legend(fontsize=7.5)

fig.tight_layout()
fig.savefig(f"{OUT}/landmark_triplet.png", dpi=180)
plt.close(fig)

# minimal self-checks (exact identities)
yy = np.array([0.1, 0.5, 2.0, 30.0])
sig = lambda t: (2*t+1)/(2*(t+1))
Cf = lambda t: t/(2*(t+1)**2)
assert np.allclose(sig(yy) + sig(1/yy), 1.5, atol=1e-12)
assert np.allclose(Cf(yy), Cf(1/yy), atol=1e-12)
assert abs(sig(1.0) - 0.75) < 1e-12 and abs(Cf(1.0) - 0.125) < 1e-12
print("mi2026_figs: 2 figures written, landmark identities check exact. exit 0")
