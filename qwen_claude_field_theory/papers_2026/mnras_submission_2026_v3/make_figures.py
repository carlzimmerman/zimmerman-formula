#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
make_figures.py -- the six figures of `mnras_a0_lambda_v3.tex`, built from the same functions and inputs as
paper_numbers.py (imported, so a figure cannot drift from a quoted number).  Vector PDF, MNRAS column widths
(single 3.33 in, double 6.97 in), colour-blind-safe palette (Okabe & Ito).
    fig1_rar.pdf            the SPARC radial-acceleration relation and the three a0 values on it
    fig2_kappa.pdf          (a) kappa against the disc mass-to-light ratio, (b) the two estimators against the
                            candidate coefficients, (c) the H0 lock
    fig3_laws.pdf           log10[a0(z)/a0(0)] for the constant, H(z) and halo-emergent laws, with the decision bar
    fig4_amplification.pdf  the error amplification of the kernel inversion against g_bar/a0
    fig5_rc100.pdf          the closed-form inversion of the RC100 dark-matter fractions
    fig_deep.pdf            the deep regime in SPARC and MIGHTEE-HI: (a) the per-galaxy slope against the kernel's own slope,
                            (b) the deep-regime kappa by survey and mass-to-light convention.  It is Figure 3 of the manuscript
                            (it sits in Section 3); the older files keep their names, so fig3_laws.pdf is Figure 4, and so on.
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

# v3.1: STIX fonts (a real upright Upsilon, close to the journal's Times) and no text below 7 pt at the printed width
plt.rcParams.update({"font.family": "STIXGeneral", "font.size": 8, "axes.labelsize": 8.5, "legend.fontsize": 7.0,
                     "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.linewidth": 0.6, "lines.linewidth": 1.2,
                     "xtick.direction": "in", "ytick.direction": "in", "xtick.top": True, "ytick.right": True,
                     "mathtext.fontset": "stix", "pdf.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
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
axr.text(-8.1, rms * 0.55, f"rms scatter {rms:.2f} dex", ha="right", va="center", fontsize=7, color="#444444")
ax.set_ylabel(r"$\log_{10} g_{\rm obs}$ [m s$^{-2}$]"); axr.set_ylabel(r"$\Delta\log_{10}g_{\rm obs}$"); axr.set_xlabel(r"$\log_{10} g_{\rm bar}$ [m s$^{-2}$]")
ax.set_xlim(-12.3, -8.0); ax.set_ylim(-11.6, -8.0); axr.set_ylim(-0.19, 0.19)
ax.legend(loc="upper left", frameon=False, handlelength=2.6)
ax.text(-8.1, -11.35, f"SPARC: {len(gb)} points, {ng} galaxies\n" + r"$\Upsilon_{\rm disc}=0.5$, $\Upsilon_{\rm bul}=0.7$" + "\nHubble-flow distances at $H_0=67.4$", ha="right", va="bottom", fontsize=7)
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
ax.text(0.6, 0.93, "population\nsynthesis", ha="center", va="top", fontsize=7, color="#444444")
ax.set_xlabel(r"disc mass-to-light ratio $\Upsilon_{\rm disc}$ [3.6 $\mu$m]"); ax.set_ylabel(r"$\kappa$ from the standard fit")
ax.set_xlim(0.35, 0.85); ax.set_ylim(0.25, 0.95); ax.legend(loc="lower left", frameon=False); ax.set_title("(a)", loc="left", fontsize=8)
ax = axs[1]
cand = [(pn.k_hor, r"$cH_\Lambda/2\pi$", GREEN, "right", 4.15), (0.5, r"$1/2$", VERM, "left", 4.15), (pn.k_hor / math.sqrt(pn.OL), r"$cH_0/2\pi$", BLUE, "right", 3.72),
        (math.sqrt(8 * math.pi / 3) / 6 / math.sqrt(pn.OL), r"$cH_0/6$", PURPLE, "left", 3.72)]
for k, lab, col, ha, yl in cand:
    ax.axvline(k, color=col, lw=1.0, ls="-" if k == 0.5 else "--", zorder=1)
    ax.text(k + (0.005 if ha == "left" else -0.005), yl, lab, rotation=0, ha=ha, va="center", fontsize=7.5, color=col,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.3, alpha=0.9), zorder=7)
BOXES = (pn.BOX_A, pn.BOX_B, pn.BOX_C)
meas = [(lab, k, s_, min(bx.values()), max(bx.values())) for (lab, k, s_), bx in zip(pn.MEAS, BOXES)]
for i, (lab, k, s_, lo, hi) in enumerate(meas):
    yv = 2.95 - i * 1.0
    ax.errorbar([k], [yv], xerr=[s_], fmt="o", ms=3.5, color=BLACK, capsize=2, lw=0.9, zorder=5)
    ax.plot([lo, hi], [yv - 0.22, yv - 0.22], color=GREY, lw=2.2, solid_capstyle="butt", zorder=4)
    ax.text(0.305, yv + 0.15, lab, ha="left", va="bottom", fontsize=7, bbox=dict(facecolor="white", edgecolor="none", pad=0.3, alpha=0.85), zorder=6)
ax.text(0.305, 0.14, r"grey: range over four $H_0$ conventions", ha="left", va="center", fontsize=7, color="#555555",
        bbox=dict(facecolor="white", edgecolor="none", pad=0.3, alpha=0.85))
ax.set_xlim(0.30, 0.82); ax.set_ylim(0.0, 4.45); ax.set_yticks([]); ax.set_xlabel(r"$\kappa\equiv a_0/(c\sqrt{G\rho_\Lambda})$"); ax.set_title("(b)", loc="left", fontsize=8)
ax = axs[2]
hh = np.linspace(64, 76, 50)
A_of_h = lambda h: pn.c * np.sqrt(pn.G * pn.OL * 3 * (h * 1e3 / pn.MPC)**2 / (8 * math.pi * pn.G))
ax.plot(hh, 0.5 * A_of_h(hh) / 1e-10, color=VERM, label=r"$\kappa=\frac{1}{2}$")
ax.plot(hh, pn.k_hor * A_of_h(hh) / 1e-10, color=GREEN, ls="--", label=rf"$\kappa={pn.k_hor:.3f}$")
ax.axvspan(67.4 - 0.5, 67.4 + 0.5, color=GREY, alpha=0.2, lw=0); ax.axvspan(73.04 - 1.04, 73.04 + 1.04, color=GREY, alpha=0.2, lw=0)
ax.text(67.4, 1.082, "Planck", ha="center", fontsize=7, color="#444444"); ax.text(73.04, 1.082, "SH0ES", ha="center", fontsize=7, color="#444444")
p1, p2 = 0.5 * A_of_h(67.4) / 1e-10, pn.k_hor * A_of_h(73.04) / 1e-10
ax.plot([67.4, 73.04], [p1, p2], "o", ms=3.8, color=BLACK, zorder=5); ax.axhline(p1, color=BLACK, lw=0.6, ls=":")
ax.set_xlabel(r"$H_0$ [km s$^{-1}$ Mpc$^{-1}$]"); ax.set_ylabel(r"predicted $a_0$ [$10^{-10}$ m s$^{-2}$]"); ax.set_xlim(64, 76); ax.set_ylim(0.80, 1.10)
ax.legend(loc="lower right", frameon=False); ax.set_title("(c)", loc="left", fontsize=8)
fig.savefig(os.path.join(HERE, "fig2_kappa.pdf")); plt.close(fig)
done("fig2: the H0-lock points coincide to better than 0.5 per cent, and panel (b) draws the three computed estimators with their computed convention ranges",
     abs(p2 / p1 - 1) < 5e-3 and len(meas) == 3 and all(lo_ <= k_ <= hi_ for _, k_, _, lo_, hi_ in meas), f"ratio {p2/p1:.4f}; " + ", ".join(f"{k_:.3f} [{lo_:.3f}, {hi_:.3f}]" for _, k_, _, lo_, hi_ in meas))

# ---------------------------------------------------------------------------------------------------------------- fig 3
zg = np.linspace(0, 4, 161)
fig, ax = plt.subplots(figsize=(W1, 3.0))
halo12 = np.log10(pn.ratio_halo(zg))
hlo = np.min([np.log10(pn.ratio_halo(zg, cfun=cf, M=M)) for cf in (pn.c_DM14, pn.c_D08) for M in (1e11, 1e12, 1e13)], axis=0)
hhi = np.max([np.log10(pn.ratio_halo(zg, cfun=cf, M=M)) for cf in (pn.c_DM14, pn.c_D08) for M in (1e11, 1e12, 1e13)], axis=0)
ax.fill_between(zg, hlo, hhi, color=GREY, alpha=0.20, lw=0)
# the gate's discs (V_f 83-125 km/s, V_f/V_200 = 1.0-1.2): the Dutton-Maccio law at the halo mass each selects, redshift by redshift
gl = np.array([[np.log10(pn.ratio_halo(z_, M=pn.m200_of_vf(g_["Vf_kms"], z_, r_))) if z_ > 0 else 0.0 for z_ in zg] for g_ in pn.gate for r_ in pn.VRAT])
gc = np.array([np.log10(pn.ratio_halo(z_, M=pn.m200_of_vf(pn.gate[1]["Vf_kms"], z_, 1.1))) if z_ > 0 else 0.0 for z_ in zg])
ax.fill_between(zg, gl.min(0), gl.max(0), color=GREY, alpha=0.45, lw=0)
ax.plot(zg, gc, color=BLACK, label=r"$\Lambda$CDM halo-emergent, gate's haloes")
ax.plot(zg, halo12, color=BLACK, ls="-.", lw=0.8, label=r"$\Lambda$CDM halo-emergent, $10^{12}\,{\rm M_\odot}$")
ax.plot(zg, np.log10(pn.ratio_vmax(zg)), color=BLACK, ls=":", lw=0.9, label=r"$\Lambda$CDM, $V_{\rm max}^4/M$ scaling")
ax.plot(zg, np.log10(pn.E(zg)), color=BLUE, ls="--", label=r"$a_0\propto c\sqrt{G\rho_{\rm crit}(z)}\propto H(z)$")
dl = np.min([pn.dens_map(zg, *v) for v in pn.DESI.values()], axis=0); dh = np.max([pn.dens_map(zg, *v) for v in pn.DESI.values()], axis=0)
ax.fill_between(zg, dl, dh, color=ORANGE, alpha=0.45, lw=0, label=r"$a_0\propto\sqrt{\rho_{\rm DE}(z)}$, DESI $w_0w_a$")
ax.plot(zg, 0 * zg, color=VERM, lw=1.6, label=r"$a_0=\frac{1}{2}c\sqrt{G\rho_\Lambda}$: constant")
d25 = pn.DELTA_GATE
for yv, se in ((0.0, pn.SE_REC[0]), (d25, pn.SE_REC[1])):
    ax.errorbar([2.5], [yv], yerr=[se], fmt="s", ms=3.2, color=BLACK, capsize=2.5, lw=0.9, zorder=6)
ax.text(2.6, 0.12, f"{pn.N_REC} discs at 0.20 dex:\nerror of the mean", fontsize=7, va="center")
ax.set_xlabel("redshift $z$"); ax.set_ylabel(r"$\Delta\equiv\log_{10}[a_0(z)/a_0(0)]$"); ax.set_xlim(0, 4); ax.set_ylim(-0.3, 1.42)
ax.legend(loc="upper left", frameon=False, handlelength=2.2, borderaxespad=0.2, fontsize=7)
fig.savefig(os.path.join(HERE, "fig3_laws.pdf")); plt.close(fig)
done("fig3: the decision value at z = 2.5 is the gated halo law (+0.22 dex), inside the gate band and below the 1e12 Msun curve",
     abs(d25 - float(np.interp(2.5, zg, gc))) < 1e-3 and 0.17 < d25 < 0.26 and d25 < float(np.interp(2.5, zg, halo12)), f"{d25:+.3f}")

# ---------------------------------------------------------------------------------------------------------------- fig 4
yy = np.logspace(-2.3, 1.2, 300); nn = pn.n_slope(yy)
fig, ax = plt.subplots(figsize=(W1, 2.6))
ax.plot(yy, 1 / np.abs(nn), color=VERM, label=r"$A_{\rm obs}=1/|n|$  (kinematics)")
ax.plot(yy, np.abs(1 + 1 / nn), color=BLUE, ls="--", label=r"$A_{\rm bar}=|1+1/n|$  (baryonic mass)")
ax.axhline(2, color=VERM, lw=0.5, ls=":"); ax.axhline(1, color=BLUE, lw=0.5, ls=":")
ylo, yhi = np.percentile(pn.yy, [16, 84])
ax.axvspan(ylo, yhi, color=GREY, alpha=0.25, lw=0); ax.text(math.sqrt(ylo * yhi), 11.3, "RC100\n$0.6<z<2.5$\n(16-84%)", ha="center", va="top", fontsize=7)
ax.axvspan(yy[0], 0.3, color=GREEN, alpha=0.13, lw=0); ax.text(0.04, 11.3, "gate:\n$g_{\\rm bar}<0.3\\,a_0$", ha="center", va="top", fontsize=7)
ax.set_xscale("log"); ax.set_xlim(yy[0], yy[-1]); ax.set_ylim(0, 12); ax.set_xlabel(r"$y=g_{\rm bar}/a_0$"); ax.set_ylabel("error amplification")
ax.legend(loc="center left", frameon=False, bbox_to_anchor=(0.0, 0.62))
fig.savefig(os.path.join(HERE, "fig4_amplification.pdf")); plt.close(fig)
done("fig4: the deep limits are 2 and 1", abs(1 / abs(pn.n_slope(1e-9)) - 2) < 1e-3 and abs(abs(1 + 1 / pn.n_slope(1e-9)) - 1) < 1e-3)

# ---------------------------------------------------------------------------------------------------------------- fig 5
zz, la, yv_ = pn.zz, pn.la, pn.yy
fig, ax = plt.subplots(figsize=(W1, 2.75))
sc = ax.scatter(zz, la, c=np.log10(yv_), cmap="cividis", s=9, linewidths=0.2, edgecolors="k", vmin=-0.7, vmax=1.0)
cb = fig.colorbar(sc, ax=ax, pad=0.02, aspect=30); cb.set_label(r"$\log_{10}(g_{\rm bar}/a_0)$", fontsize=7.5); cb.ax.tick_params(labelsize=7)
zl = np.linspace(0.55, 2.6, 50); zbar = zz.mean(); lbar = pn.icpt + pn.slope * zbar
ax.fill_between(zl, lbar + (pn.slope - pn.bs.std()) * (zl - zbar), lbar + (pn.slope + pn.bs.std()) * (zl - zbar), color=VERM, alpha=0.2, lw=0)
ax.plot(zl, lbar + pn.slope * (zl - zbar), color=VERM, label=rf"fit: ${pn.slope:+.2f}\pm{pn.bs.std():.2f}$ dex per unit $z$")
ax.plot(zl, lbar + np.log10(pn.ratio_halo(zl)) - np.log10(pn.ratio_halo(zbar)), color=BLACK, ls="-", lw=0.9, label=r"$\Lambda$CDM halo-emergent ($10^{12}\,{\rm M_\odot}$)")
ax.plot(zl, lbar + np.log10(pn.E(zl)) - np.log10(pn.E(zbar)), color=BLUE, ls="--", lw=0.9, label=r"$a_0\propto H(z)$")
ax.set_xlabel("redshift $z$"); ax.set_ylabel(r"$\log_{10}\hat a_0$ [m s$^{-2}$]"); ax.set_xlim(0.55, 2.6); ax.set_ylim(-11.4, -8.6)
ax.legend(loc="lower left", frameon=False, handlelength=2.2)
fig.savefig(os.path.join(HERE, "fig5_rc100.pdf")); plt.close(fig)
done("fig5: uses the same 99 inversions as paper_numbers.py", len(zz) == 99, f"N = {len(zz)}")

# ---------------------------------------------------------------------------------------------------------------- fig deep
S6 = pn.S6
fig, axs = plt.subplots(1, 2, figsize=(W2, 2.5), gridspec_kw=dict(wspace=0.70, width_ratios=[1.0, 1.0]))
ax = axs[0]
yl = np.logspace(math.log10(3e-3), math.log10(0.25), 200)
ax.plot(yl, pn.beta_of_y(yl), color=BLACK, lw=1.1, label=r"the kernel: $\beta(y)=1+n(y)$")
for yref in (1.0, 0.75):
    ax.axhline(yref, color=GREY, lw=0.7, ls=":")
ax.text(0.24, 0.985, "Newtonian slope", fontsize=7, color="#555555", va="top", ha="right")
ax.text(0.24, 0.738, r"$\beta=0.75$", fontsize=7, color="#555555", va="top", ha="right")
pts = []
for i, UD in enumerate((0.5, 0.6, 0.7)):
    g1, g2, e1, _ = pn.load_sparc(UD=UD, UB=0.7); gi1 = pn.GAL_INDEX[0].copy(); grp1 = pn.groups_in_window(g1, gi1)
    ymed = float(np.median(np.concatenate([g1[v] for v in grp1.values()]) / pn.a0_L)) * (1.0 + 0.10 * (i - 1))
    d = S6["sparc"][UD]["slope_L"]
    pts.append((ymed, d["beta"], d["se_beta"], d["beta_kernel"], [VERM, ORANGE, YELLOW][i], r"SPARC, $\Upsilon_{\rm disc}=" + f"{UD}" + r"$"))
ym = float(np.median(np.concatenate([pn.mgb[v] for v in pn.mig_grp.values()]) / pn.a0_L)); d = S6["mightee"]["slope_L"]
pts.append((ym, d["beta"], d["se_beta"], d["beta_kernel"], BLUE, "MIGHTEE-HI"))
for yv, b, sb, bk, col, lab in pts:
    ax.errorbar([yv], [b], yerr=[sb], fmt="o", ms=3.6, color=col, mec=BLACK, mew=0.4, capsize=2, lw=0.9, zorder=5, label=lab)
    ax.plot([yv], [bk], marker="D", ms=3.4, mfc="white", mec=col, mew=1.0, ls="none", zorder=6)
ax.plot([], [], marker="D", ms=3.4, mfc="white", mec=BLACK, mew=1.0, ls="none", label="the kernel at the same points")
ax.set_xscale("log"); ax.set_xlim(3e-3, 0.25)
ax.set_xlabel(r"$y=g_{\rm bar}/a_0$ (median of the window points)"); ax.set_ylabel(r"deep slope $\beta={\rm d}\ln g_{\rm obs}/{\rm d}\ln g_{\rm bar}$")
ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), frameon=False, fontsize=7, handlelength=1.4, labelspacing=0.15); ax.set_ylim(0.40, 1.38); ax.set_title("(a)", loc="left", fontsize=8)
ax = axs[1]
t3 = S6["mightee"]["table3"]
rows6 = [(r"SPARC, $\Upsilon_{\rm disc}=0.5$", S6["sparc"][0.5]["amp"], VERM), (r"SPARC, $\Upsilon_{\rm disc}=0.6$", S6["sparc"][0.6]["amp"], ORANGE),
         (r"SPARC, $\Upsilon_{\rm disc}=0.7$", S6["sparc"][0.7]["amp"], YELLOW),
         ("MIGHTEE-HI, our fit", S6["mightee"]["amp"], BLUE),
         ("MIGHTEE-HI, fiducial", t3["fiducial (spatially varying SED ratio, median 0.35)"], SKY),
         (r"MIGHTEE-HI, no H$_2$", t3["no molecular gas"], SKY), ("MIGHTEE-HI, radial mean", t3["radially averaged ratio"], SKY),
         (r"MIGHTEE-HI, $\Upsilon_K=0.6$", t3["fixed Upsilon_K = 0.6"], SKY),
         ("SPARC, fitted ratios", S6["kinematic_ratios"]["amp"], GREY)]
ax.axvspan(pn.kA - pn.sA, pn.kA + pn.sA, color=GREY, alpha=0.18, lw=0)
ax.axvline(0.5, color=BLACK, lw=0.9); ax.axvline(0.5 / math.sqrt(pn.OL), color=BLACK, lw=0.9, ls="--")
ax.text(0.49, len(rows6) - 0.25, r"$\kappa_\Lambda=\frac{1}{2}$", ha="right", va="center", fontsize=7)
ax.text(0.5 / math.sqrt(pn.OL) + 0.01, len(rows6) - 0.25, r"$\kappa_{\rm crit}=\frac{1}{2}$", ha="left", va="center", fontsize=7)
ax.text(pn.kA, -0.85, "estimator A", ha="center", va="bottom", fontsize=7, color="#444444")
plotted = []
for j, (lab, am, col) in enumerate(rows6):
    yv = len(rows6) - 1 - j; k = am["kappa_L"]; e = k * am["se_ln"]; plotted.append(k)
    ax.errorbar([k], [yv], xerr=[e], fmt="s" if col == SKY else "o", ms=3.4, color=col, mec=BLACK, mew=0.4, capsize=2, lw=0.9, zorder=5)
ax.set_yticks(range(len(rows6))); ax.set_yticklabels([r_[0] for r_ in rows6][::-1], fontsize=7)
ax.set_xlim(0.2, 1.25); ax.set_ylim(-1.0, len(rows6) + 0.2); ax.set_xlabel(r"$\kappa_\Lambda$ from $g_{\rm bar}<0.2a_0$")
ax.set_title("(b)", loc="left", fontsize=8)
fig.savefig(os.path.join(HERE, "fig_deep.pdf")); plt.close(fig)
done("fig deep: the plotted slopes and amplitudes are paper_numbers S6's, and the kernel curve is 0.603 at y = 0.2",
     abs(plotted[1] - S6["sparc"][0.6]["amp"]["kappa_L"]) < 1e-12 and abs(float(pn.beta_of_y(0.2)) - 0.6035) < 1e-3 and len(pts) == 4,
     f"kappa_L(SPARC, 0.6) = {plotted[1]:.3f}; beta(0.2) = {float(pn.beta_of_y(0.2)):.4f}")

print(f"FIGURES: {sum(OKS)}/{len(OKS)} checks passed", flush=True)
sys.exit(0 if all(OKS) else 1)
