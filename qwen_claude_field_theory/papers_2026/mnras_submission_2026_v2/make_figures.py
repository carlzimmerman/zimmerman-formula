#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
make_figures.py -- the five figures of `mnras_a0_lambda_v2.tex`, built from the same functions and inputs as
paper_numbers.py (imported, so a figure cannot drift from a quoted number).  Vector PDF, MNRAS column widths
(single 3.33 in, double 6.97 in), colour-blind-safe palette (Okabe & Ito).
    fig1_rar.pdf            the SPARC radial-acceleration relation and the three a0 values on it
    fig2_kappa.pdf          (a) kappa against the disc mass-to-light ratio, (b) the two estimators against the
                            candidate coefficients, (c) the H0 lock
    fig3_laws.pdf           log10[a0(z)/a0(0)] for the constant, H(z) and halo-emergent laws, with the decision bar
    fig4_amplification.pdf  the error amplification of the kernel inversion against g_bar/a0
    fig5_rc100.pdf          the closed-form inversion of the RC100 dark-matter fractions
Run:  python3 make_figures.py     (prints one check line per figure; exit 1 on failure)
"""
import os, sys, io, math, csv, contextlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):          # import the numbers module without its report
    import paper_numbers as pn
if pn.FAILS:
    sys.exit("paper_numbers.py has failing checks: " + "; ".join(pn.FAILS))

plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.labelsize": 8.5, "legend.fontsize": 6.8,
                     "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.linewidth": 0.6, "lines.linewidth": 1.2,
                     "xtick.direction": "in", "ytick.direction": "in", "xtick.top": True, "ytick.right": True,
                     "mathtext.fontset": "dejavuserif", "pdf.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
BLACK, ORANGE, SKY, GREEN, YELLOW, BLUE, VERM, PURPLE, GREY = ("#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2",
                                                                "#D55E00", "#CC79A7", "#7f7f7f")
W1, W2 = 3.33, 6.97
OKS = []
def done(name, ok, detail=""):
    OKS.append(ok); print(f"  [{'PASS' if ok else 'FAIL'}] {name}   {detail}", flush=True)

# ---------------------------------------------------------------------------------------------------------------- fig 1
gb, go, ew, ng = pn.load_sparc(UD=0.5, UB=0.7)
a_fit, rms = pn.fit_a0(gb, go, ew)
fig, (ax, axr) = plt.subplots(2, 1, figsize=(W1, 3.9), sharex=True, gridspec_kw=dict(height_ratios=[3.0, 1.15], hspace=0.05))
ax.scatter(np.log10(gb), np.log10(go), s=1.2, c=GREY, alpha=0.35, linewidths=0, rasterized=True)
xg = np.logspace(-12.3, -8.0, 300)
ax.plot(np.log10(xg), np.log10(xg), color=BLACK, lw=0.6, ls=":")
for a0, col, ls, lab in ((a_fit, BLACK, "-", rf"best fit, $a_0={a_fit/1e-10:.2f}\times10^{{-10}}$"),
                         (pn.a0_C, BLUE, "--", rf"$\frac{{1}}{{2}}c\sqrt{{G\rho_{{\rm crit}}}}={pn.a0_C/1e-10:.2f}\times10^{{-10}}$"),
                         (pn.a0_L, VERM, "-.", rf"$\frac{{1}}{{2}}c\sqrt{{G\rho_\Lambda}}={pn.a0_L/1e-11:.2f}\times10^{{-11}}$")):
    ax.plot(np.log10(xg), np.log10(xg * pn.nu(xg / a0)), color=col, ls=ls, label=lab)
    axr.plot(np.log10(xg), np.log10(pn.nu(xg / a0) / pn.nu(xg / a_fit)), color=col, ls=ls)
axr.axhspan(-rms, rms, color=GREY, alpha=0.18, lw=0)
axr.text(-8.1, rms * 0.55, f"rms scatter {rms:.2f} dex", ha="right", va="center", fontsize=6.5, color="#444444")
ax.set_ylabel(r"$\log_{10} g_{\rm obs}$ [m s$^{-2}$]"); axr.set_ylabel(r"$\Delta\log_{10}g_{\rm obs}$"); axr.set_xlabel(r"$\log_{10} g_{\rm bar}$ [m s$^{-2}$]")
ax.set_xlim(-12.3, -8.0); ax.set_ylim(-11.6, -8.0); axr.set_ylim(-0.19, 0.19)
ax.legend(loc="upper left", frameon=False, handlelength=2.6)
ax.text(-8.1, -11.35, f"SPARC: {len(gb)} points, {ng} galaxies\n" + r"$\Upsilon_{\rm disc}=0.5$, $\Upsilon_{\rm bul}=0.7$", ha="right", va="bottom", fontsize=6.8)
fig.savefig(os.path.join(HERE, "fig1_rar.pdf"), dpi=400); plt.close(fig)
dmax = float(np.max(np.abs(np.log10(pn.nu(xg / pn.a0_L) / pn.nu(xg / a_fit)))))
done("fig1: the three curves differ by less than the scatter of the data everywhere on the plotted range", dmax < rms, f"max curve difference {dmax:.3f} dex vs rms {rms:.3f} dex")

# ---------------------------------------------------------------------------------------------------------------- fig 2
fig, axs = plt.subplots(1, 3, figsize=(W2, 2.45), gridspec_kw=dict(wspace=0.36))
ax = axs[0]
uds = np.linspace(0.35, 0.85, 11)
kL = np.array([pn.fit_a0(*pn.load_sparc(UD=u)[:3])[0] for u in uds])
ax.plot(uds, kL / pn.A_L, color=VERM, label=r"against $\rho_\Lambda$")
ax.plot(uds, kL / pn.A_C, color=BLUE, ls="--", label=r"against $\rho_{\rm crit}$")
ax.axhline(0.5, color=BLACK, lw=0.7, ls=":")
ax.axvspan(0.5, 0.7, color=GREY, alpha=0.15, lw=0)
ax.text(0.6, 0.93, "population\nsynthesis", ha="center", va="top", fontsize=6.3, color="#444444")
ax.set_xlabel(r"disc mass-to-light ratio $\Upsilon_{\rm disc}$ [3.6 $\mu$m]"); ax.set_ylabel(r"$\kappa$ from the standard fit")
ax.set_xlim(0.35, 0.85); ax.set_ylim(0.25, 0.95); ax.legend(loc="lower left", frameon=False); ax.set_title("(a)", loc="left", fontsize=8)
ax = axs[1]
cand = [(pn.k_hor, r"$cH_\Lambda/2\pi$", GREEN, "right"), (0.5, r"$\frac{1}{2}$", VERM, "left"), (pn.k_hor / math.sqrt(pn.OL), r"$cH_0/2\pi$", BLUE, "right"),
        (math.sqrt(8 * math.pi / 3) / 6 / math.sqrt(pn.OL), r"$cH_0/6$", PURPLE, "left")]
for k, lab, col, ha in cand:
    ax.axvline(k, color=col, lw=1.0, ls="-" if k == 0.5 else "--", zorder=1)
    ax.text(k + (0.006 if ha == "left" else -0.006), 2.75 if k == 0.5 else 3.52, lab, rotation=90, ha=ha, va="top", fontsize=6.5, color=col,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.4, alpha=0.85))
meas = [("A: Tully-Fisher intercept", 0.465, 0.076, 0.450, 0.465), ("B: shape only", pn.kB, pn.sB, 0.492, 0.589)]
for i, (lab, k, s_, lo, hi) in enumerate(meas):
    yv = 1.75 - i * 0.95
    ax.errorbar([k], [yv], xerr=[s_], fmt="o", ms=3.5, color=BLACK, capsize=2, lw=0.9, zorder=5)
    ax.plot([lo, hi], [yv - 0.2, yv - 0.2], color=GREY, lw=2.2, solid_capstyle="butt", zorder=4)
    ax.text(0.305, yv + 0.17, lab, ha="left", va="bottom", fontsize=6.4, bbox=dict(facecolor="white", edgecolor="none", pad=0.4, alpha=0.85), zorder=6)
ax.text(0.305, 0.14, r"grey bars: $H_0$-convention range", ha="left", va="center", fontsize=5.8, color="#555555",
        bbox=dict(facecolor="white", edgecolor="none", pad=0.4, alpha=0.85))
ax.set_xlim(0.30, 0.80); ax.set_ylim(0.0, 3.6); ax.set_yticks([]); ax.set_xlabel(r"$\kappa\equiv a_0/(c\sqrt{G\rho_\Lambda})$"); ax.set_title("(b)", loc="left", fontsize=8)
ax = axs[2]
hh = np.linspace(64, 76, 50)
A_of_h = lambda h: pn.c * np.sqrt(pn.G * pn.OL * 3 * (h * 1e3 / pn.MPC)**2 / (8 * math.pi * pn.G))
ax.plot(hh, 0.5 * A_of_h(hh) / 1e-10, color=VERM, label=r"$\kappa=\frac{1}{2}$")
ax.plot(hh, pn.k_hor * A_of_h(hh) / 1e-10, color=GREEN, ls="--", label=rf"$\kappa={pn.k_hor:.3f}$")
ax.axvspan(67.4 - 0.5, 67.4 + 0.5, color=GREY, alpha=0.2, lw=0); ax.axvspan(73.04 - 1.04, 73.04 + 1.04, color=GREY, alpha=0.2, lw=0)
ax.text(67.4, 1.082, "Planck", ha="center", fontsize=6.3, color="#444444"); ax.text(73.04, 1.082, "SH0ES", ha="center", fontsize=6.3, color="#444444")
p1, p2 = 0.5 * A_of_h(67.4) / 1e-10, pn.k_hor * A_of_h(73.04) / 1e-10
ax.plot([67.4, 73.04], [p1, p2], "o", ms=3.8, color=BLACK, zorder=5); ax.axhline(p1, color=BLACK, lw=0.6, ls=":")
ax.set_xlabel(r"$H_0$ [km s$^{-1}$ Mpc$^{-1}$]"); ax.set_ylabel(r"predicted $a_0$ [$10^{-10}$ m s$^{-2}$]"); ax.set_xlim(64, 76); ax.set_ylim(0.80, 1.10)
ax.legend(loc="lower right", frameon=False); ax.set_title("(c)", loc="left", fontsize=8)
fig.savefig(os.path.join(HERE, "fig2_kappa.pdf")); plt.close(fig)
done("fig2: the H0-lock points coincide to better than 0.5 per cent", abs(p2 / p1 - 1) < 5e-3, f"ratio {p2/p1:.4f}")

# ---------------------------------------------------------------------------------------------------------------- fig 3
zg = np.linspace(0, 4, 161)
fig, ax = plt.subplots(figsize=(W1, 2.95))
halo = np.log10(pn.ratio_halo(zg))
hlo = np.min([np.log10(pn.ratio_halo(zg, cfun=cf, M=M)) for cf in (pn.c_DM14, pn.c_D08) for M in (1e11, 1e12, 1e13)], axis=0)
hhi = np.max([np.log10(pn.ratio_halo(zg, cfun=cf, M=M)) for cf in (pn.c_DM14, pn.c_D08) for M in (1e11, 1e12, 1e13)], axis=0)
ax.fill_between(zg, hlo, hhi, color=GREY, alpha=0.25, lw=0)
ax.plot(zg, halo, color=BLACK, label=r"$\Lambda$CDM halo-emergent scale")
ax.plot(zg, np.log10(pn.ratio_vmax(zg)), color=BLACK, ls=":", lw=0.9, label=r"$\Lambda$CDM, $V_{\rm max}^4/M$ scaling")
ax.plot(zg, np.log10(pn.E(zg)), color=BLUE, ls="--", label=r"$a_0\propto c\sqrt{G\rho_{\rm crit}(z)}\propto H(z)$")
dl = np.min([pn.dens_map(zg, *v) for v in pn.DESI.values()], axis=0); dh = np.max([pn.dens_map(zg, *v) for v in pn.DESI.values()], axis=0)
ax.fill_between(zg, dl, dh, color=ORANGE, alpha=0.45, lw=0, label=r"$a_0\propto\sqrt{\rho_{\rm DE}(z)}$, DESI $w_0w_a$")
ax.plot(zg, 0 * zg, color=VERM, lw=1.6, label=r"$a_0=\frac{1}{2}c\sqrt{G\rho_\Lambda}$: constant")
d25 = float(np.log10(pn.ratio_halo(2.5)))
for yv in (0.0, d25):
    ax.errorbar([2.5], [yv], yerr=[0.13], fmt="s", ms=3.2, color=BLACK, capsize=2.5, lw=0.9, zorder=6)
ax.text(2.58, 0.165, r"$\pm0.13$ dex", fontsize=6.5, va="center")
ax.set_xlabel("redshift $z$"); ax.set_ylabel(r"$\Delta\equiv\log_{10}[a_0(z)/a_0(0)]$"); ax.set_xlim(0, 4); ax.set_ylim(-0.3, 1.32)
ax.legend(loc="upper left", frameon=False, handlelength=2.2, borderaxespad=0.2)
fig.savefig(os.path.join(HERE, "fig3_laws.pdf")); plt.close(fig)
done("fig3: the halo-emergent decision value at z = 2.5 is +0.33 dex", abs(d25 - 0.33) < 0.01, f"{d25:+.3f}")

# ---------------------------------------------------------------------------------------------------------------- fig 4
yy = np.logspace(-2.3, 1.2, 300); nn = pn.n_slope(yy)
fig, ax = plt.subplots(figsize=(W1, 2.6))
ax.plot(yy, 1 / np.abs(nn), color=VERM, label=r"$A_{\rm obs}=1/|n|$  (kinematics)")
ax.plot(yy, np.abs(1 + 1 / nn), color=BLUE, ls="--", label=r"$A_{\rm bar}=|1+1/n|$  (baryonic mass)")
ax.axhline(2, color=VERM, lw=0.5, ls=":"); ax.axhline(1, color=BLUE, lw=0.5, ls=":")
ylo, yhi = np.percentile(pn.yy, [16, 84])
ax.axvspan(ylo, yhi, color=GREY, alpha=0.25, lw=0); ax.text(math.sqrt(ylo * yhi), 11.3, "RC100\n$0.6<z<2.5$\n(16-84%)", ha="center", va="top", fontsize=6.3)
ax.axvspan(yy[0], 0.3, color=GREEN, alpha=0.13, lw=0); ax.text(0.04, 11.3, "gate:\n$g_{\\rm bar}<0.3\\,a_0$", ha="center", va="top", fontsize=6.3)
ax.set_xscale("log"); ax.set_xlim(yy[0], yy[-1]); ax.set_ylim(0, 12); ax.set_xlabel(r"$y=g_{\rm bar}/a_0$"); ax.set_ylabel("error amplification")
ax.legend(loc="center left", frameon=False, bbox_to_anchor=(0.0, 0.62))
fig.savefig(os.path.join(HERE, "fig4_amplification.pdf")); plt.close(fig)
done("fig4: the deep limits are 2 and 1", abs(1 / abs(pn.n_slope(1e-9)) - 2) < 1e-3 and abs(abs(1 + 1 / pn.n_slope(1e-9)) - 1) < 1e-3)

# ---------------------------------------------------------------------------------------------------------------- fig 5
zz, la, yv_ = pn.zz, pn.la, pn.yy
fig, ax = plt.subplots(figsize=(W1, 2.75))
sc = ax.scatter(zz, la, c=np.log10(yv_), cmap="cividis", s=9, linewidths=0.2, edgecolors="k", vmin=-0.7, vmax=1.0)
cb = fig.colorbar(sc, ax=ax, pad=0.02, aspect=30); cb.set_label(r"$\log_{10}(g_{\rm bar}/a_0)$", fontsize=7); cb.ax.tick_params(labelsize=6.5)
zl = np.linspace(0.55, 2.6, 50); zbar = zz.mean(); lbar = pn.icpt + pn.slope * zbar
ax.fill_between(zl, lbar + (pn.slope - pn.bs.std()) * (zl - zbar), lbar + (pn.slope + pn.bs.std()) * (zl - zbar), color=VERM, alpha=0.2, lw=0)
ax.plot(zl, lbar + pn.slope * (zl - zbar), color=VERM, label=rf"fit: ${pn.slope:+.2f}\pm{pn.bs.std():.2f}$ dex per unit $z$")
ax.plot(zl, lbar + np.log10(pn.ratio_halo(zl)) - np.log10(pn.ratio_halo(zbar)), color=BLACK, ls="-", lw=0.9, label=r"$\Lambda$CDM halo-emergent")
ax.plot(zl, lbar + np.log10(pn.E(zl)) - np.log10(pn.E(zbar)), color=BLUE, ls="--", lw=0.9, label=r"$a_0\propto H(z)$")
ax.set_xlabel("redshift $z$"); ax.set_ylabel(r"$\log_{10}\hat a_0$ [m s$^{-2}$]"); ax.set_xlim(0.55, 2.6); ax.set_ylim(-11.4, -8.6)
ax.legend(loc="lower left", frameon=False, handlelength=2.2)
fig.savefig(os.path.join(HERE, "fig5_rc100.pdf")); plt.close(fig)
done("fig5: uses the same 99 inversions as paper_numbers.py", len(zz) == 99, f"N = {len(zz)}")

print(f"FIGURES: {sum(OKS)}/{len(OKS)} checks passed", flush=True)
sys.exit(0 if all(OKS) else 1)
