#!/usr/bin/env python3
"""
make_figures.py -- the four figures of the MNRAS manuscript 'The MOND acceleration scale and the cosmological constant:
what fixes the coefficient, and the observations that decide it' (2026-09-06).  Every number plotted is either computed
here from the stated formula or copied from a committed script named in the caption; nothing is tuned.
  fig1_kappa_h0.pdf   : the measured kappa against the candidate coefficients, and the H0 lock (kappa H0 = const at fixed Omega_L)
  fig2_fourform.pdf   : the environmental a0 of the four-form promotion and its wide-binary shift (kappa_closure/k04)
  fig3_dr4_rule.pdf   : the Gaia DR4 decision rule with both registered arms (Amendment 11)
  fig4_a0z.pdf        : a0(z) laws and the z ~ 2.5 zero-point separation (prep_2026/a0z_crossscale, PAPER7)
Checks that can fail are asserted at the end.
"""
import os, math, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
OUT = os.path.dirname(os.path.abspath(__file__))
plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "legend.fontsize": 7.5, "figure.dpi": 150})
G = 6.674e-11; c = 2.998e8; MPC = 3.0857e22; MSUN = 1.989e30; AU = 1.496e11
OL = 0.685
def a0_pred(kappa, H0kms): H0 = H0kms*1e3/MPC; return kappa*c*math.sqrt(G*OL*3*H0**2/(8*math.pi*G))
K_2PI = math.sqrt(8*math.pi/3)/(2*math.pi)
MEAS = {"BTFR intercept (SPARC)": (0.465, 0.076), "shape-only, distance-immune (SPARC)": (0.551, 0.043)}
CANDS = [(K_2PI, "0.461 horizon"), (0.5, "1/2"), (0.5566, r"0.557 $cH_0/2\pi$"), (1/math.sqrt(3), r"0.577 $1/\sqrt{3}$"), (math.sqrt(3/8), r"0.612 $\sqrt{3/8}$")]
# ---------------- Figure 1 ----------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.7), gridspec_kw=dict(wspace=0.32))
for i, (lab, (m, e)) in enumerate(MEAS.items()):
    ax1.errorbar(m, i, xerr=e, fmt="o", color="k", capsize=3, label=lab if i == 0 else None)
    ax1.text(0.285, i + 0.14, lab, fontsize=7)
ax1.errorbar([0.450], [0 - 0.25], xerr=[0.076], fmt="s", color="0.5", capsize=2, ms=4)
ax1.text(0.285, -0.52, "BTFR with Planck-consistent distances (0.450)", fontsize=6.5, color="0.4")
ax1.plot([0.492, 0.591], [1 - 0.25, 1 - 0.25], color="0.5", lw=3, alpha=0.6)
ax1.text(0.285, 0.50, "shape-only, $H_0$-convention range [0.49, 0.59]", fontsize=6.5, color="0.4")
for k, lab in CANDS:
    ax1.axvline(k, color="C3" if abs(k - 0.5) < 1e-9 else "C0", lw=1.4 if abs(k - 0.5) < 1e-9 else 0.8, ls="-" if abs(k - 0.5) < 1e-9 else "--")
ax1.set_xlim(0.28, 0.72); ax1.set_ylim(-0.8, 2.3); ax1.set_yticks([]); ax1.set_xlabel(r"$\kappa = a_0/(c\sqrt{G\rho_\Lambda})$ at the Planck $H_0$")
ax1.set_title("(a) measured $\\kappa$ against candidate coefficients", fontsize=8.5)
for k, lab in CANDS: ax1.text(k + 0.004, 2.25, lab, rotation=90, fontsize=6, ha="left", va="top", color="C3" if abs(k - 0.5) < 1e-9 else "C0")
H = np.linspace(60, 80, 100)
ax2.plot(H, [a0_pred(0.5, h)*1e11 for h in H], color="C3", label=r"$\kappa=\frac{1}{2}$")
ax2.plot(H, [a0_pred(K_2PI, h)*1e11 for h in H], color="C0", ls="--", label=r"$\kappa=0.461$ (horizon)")
ax2.axvline(67.4, color="0.6", lw=0.8); ax2.axvline(73.0, color="0.6", lw=0.8)
ax2.text(67.5, 7.55, "Planck", fontsize=7, color="0.4"); ax2.text(73.1, 7.55, "SH0ES", fontsize=7, color="0.4")
lock = a0_pred(0.5, 67.4); ax2.axhline(lock*1e11, color="k", lw=0.6, ls=":")
ax2.plot([67.4, 73.0], [a0_pred(0.5, 67.4)*1e11, a0_pred(K_2PI, 73.0)*1e11], "ko", ms=4)
ax2.set_xlabel(r"$H_0$ [km s$^{-1}$ Mpc$^{-1}$] at fixed $\Omega_\Lambda=0.685$"); ax2.set_ylabel(r"predicted $a_0$ [$10^{-11}$ m s$^{-2}$]")
ax2.set_title("(b) the $H_0$ lock: $\\kappa H_0$ is what the data fix", fontsize=8.5); ax2.legend(loc="upper left"); ax2.set_ylim(7.5, 11.2)
fig.savefig(os.path.join(OUT, "fig1_kappa_h0.pdf"), bbox_inches="tight"); plt.close(fig)
# ---------------- Figure 2 ----------------
Delta = lambda s: s/np.expm1(np.sqrt(s)) if s > 0 else 0.0
opt = minimize_scalar(lambda s: -Delta(s), bounds=(0.5, 6), method="bounded"); s_sat, D_sat = opt.x, -opt.fun
def j_of(s): return 2*(s*Delta(s) - quad(Delta, 0, s)[0]) if s <= s_sat else 2*(s_sat*D_sat - quad(Delta, 0, s_sat)[0])
def Dl(s): return Delta(s) if s <= s_sat else D_sat
def a0loc(gN_over_a0, KB=0.0):
    r = 1.0
    for _ in range(300):
        s = gN_over_a0/r; r_new = 1.0/(1.0 + (2 - KB)*(s*Dl(s) - j_of(s))/(64*math.pi))
        if abs(r_new - r) < 1e-12: break
        r = r_new
    return r
ss = np.geomspace(0.01, 400, 160); rr = np.array([a0loc(s) for s in ss])
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.6), gridspec_kw=dict(wspace=0.32))
ax1.semilogx(ss, rr, color="C0"); ax1.axvline(155, color="0.6", ls="--", lw=0.8); ax1.text(160, 0.5, "scalar off\nabove $155\\,a_0$", fontsize=7)
ax1.axvspan(1.0, 2.54, color="C1", alpha=0.15); ax1.text(1.1, 0.08, "RAR knee", fontsize=7)
ax1.set_xlabel(r"$g_N/a_0$"); ax1.set_ylabel(r"$a_0^{\rm loc}/a_0$"); ax1.set_ylim(0, 1.05); ax1.set_title("(a) environmental $a_0$ of the four-form promotion", fontsize=8.5)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
kau = np.array([2, 2.5, 3, 4, 5, 7, 10, 15, 20])
for foot, a0 in A0.items():
    d = [0.1155*math.log(a0loc(G*1.5*MSUN/(k*1e3*AU)**2/a0)) for k in kau]
    ax2.plot(kau, d, "o-", ms=3, label=f"{foot} footing")
ax2.axhspan(-0.015, 0.015, color="0.8", alpha=0.5); ax2.text(8, 0.010, r"DR4 $\pm\sigma_{\rm fit}$", fontsize=7)
ax2.axhline(0, color="k", lw=0.6); ax2.set_xlabel("projected separation [kAU], $1.5\\,M_\\odot$ pair"); ax2.set_ylabel(r"$\delta\gamma_v$ (four-form $-$ Arm B)")
ax2.set_title("(b) the induced wide-binary shift", fontsize=8.5); ax2.legend(loc="lower right"); ax2.set_ylim(-0.025, 0.018)
fig.savefig(os.path.join(OUT, "fig2_fourform.pdf"), bbox_inches="tight"); plt.close(fig)
# ---------------- Figure 3 ----------------
fig, ax = plt.subplots(figsize=(7.0, 2.4))
ax.axvspan(1.1614, 1.1814, color="C3", alpha=0.35, label="Arm A band, canonical (Amdt 10)")
ax.axvspan(1.1917, 1.2267, color="C3", alpha=0.18, label="Arm A band, alt")
ax.axvspan(1.000, 1.0450, color="C0", alpha=0.35, label=r"Arm B: $1<\gamma_v\leq 1.0450$ canonical (Amdt 11)")
ax.axvspan(1.000, 1.0300, color="C0", alpha=0.18)
ax.axvline(1.0, color="k", lw=1.2); ax.text(1.001, 0.86, "Newton", fontsize=7.5)
ax.axvline(1.23, color="k", ls="--", lw=0.8); ax.text(1.231, 0.86, "no-verdict\nedge", fontsize=7)
for x, t in ((1.056, "A falsified\nbelow"), (1.129, "B falsified\nat/above")):
    ax.axvline(x, color="0.4", ls=":", lw=0.9); ax.text(x + 0.002, 0.05, t, fontsize=6.5, color="0.3")
ax.errorbar([1.045], [0.5], xerr=[0.028], fmt="none", ecolor="C0", capsize=4, lw=1.5); ax.text(1.02, 0.56, r"$\sigma_{\rm tot}=0.028$", fontsize=7, color="C0")
ax.errorbar([1.1614], [0.35], xerr=[0.028], fmt="none", ecolor="C3", capsize=4, lw=1.5)
ax.set_xlim(0.985, 1.26); ax.set_ylim(0, 1); ax.set_yticks([]); ax.set_xlabel(r"measured wide-binary boost $\hat\gamma_v$ (2--30 kAU, frozen estimator)")
ax.set_title("Gaia DR4 decision rule: two mutually exclusive registered arms", fontsize=8.5); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=3, fontsize=6.5, frameon=False)
fig.savefig(os.path.join(OUT, "fig3_dr4_rule.pdf"), bbox_inches="tight"); plt.close(fig)
# ---------------- Figure 4 ----------------
z = np.array([0, 1, 2, 2.5, 3.25])
laws = {r"framework, $\Lambda$ constant": [1, 1, 1, 1, 1], r"framework, DESI $w_0w_a$": [1, 0.989, 0.874, 0.822, 0.754],
        r"$\Lambda$CDM-native (Dutton & Maccio 2014)": [1, 1.233, 1.756, 2.126, 2.823], r"$\Lambda$CDM-native (Duffy et al. 2008)": [1, 1.427, 2.284, 2.802, 3.667],
        r"$\Lambda$CDM-native (Magneticum $(1+z)^{0.92}$)": [1, 1.892, 2.748, 3.166, 3.785]}
fig, ax = plt.subplots(figsize=(3.4, 3.2))
for (lab, v), st in zip(laws.items(), ["-", "--", "-.", ":", (0, (3, 1, 1, 1))]):
    ax.plot(z, -np.log10(v), ls=st, marker="o", ms=3, label=lab)
ax.errorbar([2.5], [-0.33], yerr=[0.13], fmt="s", color="k", capsize=4, ms=4); ax.text(1.35, 0.06, r"decision values at $z=2.5$, $\pm0.13$ dex", fontsize=6.5)
ax.errorbar([2.5], [0.0], yerr=[0.13], fmt="s", color="k", capsize=4, ms=4)
ax.set_xlabel("redshift"); ax.set_ylabel(r"$\Delta_{\rm BTFR}=-\log_{10}[a_0(z)/a_0(0)]$ [dex]"); ax.legend(fontsize=6, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False)
ax.set_title("deep-MOND Tully--Fisher zero point vs $z$", fontsize=8.5)
fig.savefig(os.path.join(OUT, "fig4_a0z.pdf"), bbox_inches="tight"); plt.close(fig)
# ---------------- checks ----------------
lock_ratio = a0_pred(K_2PI, 73.0)/a0_pred(0.5, 67.4)
assert abs(lock_ratio - 1) < 0.005, lock_ratio
assert abs(a0loc(154.0)) > 0 and a0loc(1000.0) < 1e-3, (a0loc(154.0), a0loc(1000.0))
assert abs(0.1155*math.log(a0loc(G*1.5*MSUN/(2e3*AU)**2/A0["canonical"])) + 0.0187) < 0.002
for f in ("fig1_kappa_h0.pdf", "fig2_fourform.pdf", "fig3_dr4_rule.pdf", "fig4_a0z.pdf"):
    assert os.path.getsize(os.path.join(OUT, f)) > 5000, f
print(f"figures written; H0 lock ratio = {lock_ratio:.4f}; a0_loc(2 kAU, 1.5 Msun) = {a0loc(G*1.5*MSUN/(2e3*AU)**2/A0['canonical']):.3f}; checks passed")
