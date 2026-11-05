"""Figures for Parts I and II (chapters 1-6). Run: python3 figures_math_a.py
Quoted numbers come from the fried chicken paper (v2.3) and PAPER67 (v1.2);
curves are computed from the formulas printed beside them in the book."""
import math
import numpy as np
from numpy.polynomial import Polynomial
from scipy.optimize import brentq
from figstyle import *

# ---------------- Chapter 1 ----------------

def fig_panels():
    fig, axs = plt.subplots(1, 4, figsize=(W, 1.75))
    titles = ["the law", "$\\Lambda$CDM at the CMB", "$\\Lambda$CDM in galaxies", "the landscape"]
    for ax, t in zip(axs, titles):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1.05); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.9, boxstyle="round,pad=0.01,rounding_size=0.05",
                                    facecolor="#f6f6f2", edgecolor=GREY, lw=0.8))
        ax.text(0.5, 0.97, t, ha="center", va="bottom", fontsize=7.2, weight="bold", color=INK)
    dial(axs[0], 0.5, 0.52, 0.2, 0.35, nticks=11, label="$\\kappa=\\frac{1}{2}$", fs=7)
    names = ["$\\omega_b$", "$\\omega_c$", "$\\theta_*$", "$\\tau$", "$A_s$", "$n_s$"]
    for k, nm in enumerate(names):
        x = 0.2 + 0.3 * (k % 3); y = 0.7 - 0.38 * (k // 3)
        dial(axs[1], x, y, 0.085, 0.2 + 0.1 * k, nticks=9, label=nm, fs=6)
    rng = np.random.default_rng(4)
    for i in range(7):
        for j in range(6):
            dial(axs[2], 0.1 + 0.133 * j, 0.82 - 0.115 * i, 0.04, rng.uniform(0.05, 0.95), nticks=5, lw=0.5)
    axs[2].text(0.5, 0.035, "...up to $\\sim$1066", ha="center", fontsize=6, color=RED)
    dial(axs[3], 0.5, 0.52, 0.2, 0.618, nticks=400, color=GOLD, label="$10^{500}$ clicks", fs=7)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.02, wspace=0.08)
    fig.savefig("figures/panels.pdf"); plt.close(fig)


def fig_elephant():
    rng = np.random.default_rng(3)
    x = np.linspace(0, 1, 8); y = 0.3 + 0.6 * x + rng.normal(0, 0.06, x.size)
    xx = np.linspace(-0.04, 1.04, 500)
    line = Polynomial.fit(x, y, 1); poly = Polynomial.fit(x, y, 7)
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(xx, line(xx), color=BLUE, lw=1.6, label="2 knobs: a straight line")
    ax.plot(xx, poly(xx), color=RED, lw=1.4, label="8 knobs: exact through all 8 points")
    ax.scatter(x, y, color=INK, zorder=4, s=18, label="8 measurements")
    ax.set_ylim(-0.3, 1.5); ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.text(0.5, 1.33, "$\\chi^2=0$ with 8 knobs: perfect, and meaningless", ha="center", color=RED, fontsize=7.5)
    ax.legend(frameon=False, loc="lower right")
    save(fig, "elephant")


def fig_holdout():
    rng = np.random.default_rng(1)
    f = lambda x: np.sin(2 * np.pi * x)
    xt = np.sort(rng.uniform(0, 1, 15)); yt = f(xt) + rng.normal(0, 0.25, xt.size)
    xv = rng.uniform(0, 1, 400); yv = f(xv) + rng.normal(0, 0.25, xv.size)
    ks, tr, te = [], [], []
    for deg in range(0, 14):
        p = Polynomial.fit(xt, yt, deg)
        ks.append(deg + 1)
        tr.append(max(np.sqrt(np.mean((p(xt) - yt) ** 2)), 1e-3))
        te.append(np.sqrt(np.mean((p(xv) - yv) ** 2)))
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.semilogy(ks, tr, "o-", color=BLUE, ms=3, label="error on the data used to set the knobs")
    ax.semilogy(ks, te, "s-", color=RED, ms=3, label="error on data held out")
    best = int(np.argmin(te))
    ax.annotate("sweet spot", (ks[best], te[best]), xytext=(ks[best] + 1.5, te[best] * 4),
                arrowprops=dict(arrowstyle="->", color=INK), fontsize=7.5)
    ax.axhline(0.25, color=GREY, ls=":", lw=0.8); ax.text(0.8, 0.27, "noise level", color=GREY, fontsize=7)
    ax.set_xlabel("number of knobs (polynomial coefficients)"); ax.set_ylabel("rms error")
    ax.legend(frameon=False, loc="upper left"); ax.set_ylim(1e-3, 30)
    save(fig, "holdout")


def fig_bic_rent():
    n = 3373; k = np.logspace(0, 3.1, 200)
    fig, ax = plt.subplots(figsize=(W, 2.4))
    ax.loglog(k, k * np.log(n), color=RED, label="BIC rent, $k\\ln n$ ($n=3373$)")
    ax.loglog(k, 2 * k, color=BLUE, ls="--", label="AIC rent, $2k$")
    for kk, nm in ((1, "law"), (12, "R11"), (14, "R11b"), (26, "R13"), (1026, "R9")):
        ax.scatter(kk, kk * np.log(n), color=INK, s=14, zorder=3)
        ax.annotate(nm, (kk, kk * np.log(n)), xytext=(4, -9), textcoords="offset points", fontsize=7)
    ax.set_xlabel("number of knobs $k$"); ax.set_ylabel("penalty added to $\\chi^2$")
    ax.legend(frameon=False, loc="upper left")
    save(fig, "bic_rent")


def fig_bits_per_knob():
    """How many bits a knob extracts: log2(prior width / posterior width)."""
    ratio = np.logspace(0, 4, 200)
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.semilogx(ratio, np.log2(ratio), color=INK)
    pts = [(2 / 0.0212, "$\\kappa$: 2-dex prior, 5% width"), (1000, "a Planck-class knob")]
    for r, lab in pts:
        ax.scatter(r, np.log2(r), color=RED, zorder=3, s=16)
        ax.annotate(f"{lab}\n{np.log2(r):.1f} bits", (r, np.log2(r)), xytext=(-95, 8), textcoords="offset points", fontsize=7)
    ax.set_xlabel("prior width / data-allowed width"); ax.set_ylabel("information (bits)")
    save(fig, "bits_per_knob")


# ---------------- Chapter 2 ----------------

def fig_friedmann():
    Or, Om, OL = 9.1e-5, 0.315, 0.685
    zp1 = np.logspace(0, 5, 400)
    fig, ax = plt.subplots(figsize=(W, 2.7))
    ax.loglog(zp1, Or * zp1**4, color=GOLD, label="radiation $\\propto(1+z)^4$")
    ax.loglog(zp1, Om * zp1**3, color=BLUE, label="matter $\\propto(1+z)^3$")
    ax.loglog(zp1, OL * np.ones_like(zp1), color=RED, label="$\\Lambda$: constant")
    zeq = Om / Or; zl = (OL / Om) ** (1 / 3)
    for z, lab in ((zeq, f"matter = radiation\n$z\\approx{zeq-1:.0f}$"), (zl, "matter = $\\Lambda$\n$z\\approx0.3$"), (1091, "CMB released\n$z\\approx1090$")):
        ax.axvline(z, color=GREY, lw=0.6, ls=":")
        ax.text(z * 1.1, 1e-1 if z < 10 else (3e9 if z > 2000 else 3e5), lab, fontsize=6.5, color=INK)
    ax.set_xlabel("$1+z$ (looking back in time $\\rightarrow$)"); ax.set_ylabel("density / today's critical density")
    ax.legend(frameon=False, loc="upper left"); ax.set_ylim(1e-2, 1e14)
    save(fig, "friedmann")


def toy_cmb(ell, b=0.18, ellA=300.0, tau=0.054, ns=0.965):
    phase = np.pi * (ell + 80.0) / ellA
    osc = (np.cos(phase) - b) ** 2 + 0.22 * np.sin(phase) ** 2
    damp = np.exp(-(ell / 1350.0) ** 1.6)
    reion = np.exp(-2 * tau * (1 - np.exp(-ell / 20.0)))
    return (ell / 220.0) ** (ns - 1) * osc * damp * reion * (1 + 0.9 * np.exp(-ell / 250.0))


def fig_cmb_cartoon():
    ell = np.linspace(2, 2000, 1500)
    base = toy_cmb(ell)
    cases = [("baryons $\\omega_b$ up: odd peaks rise", dict(b=0.27)),
             ("acoustic angle $\\theta_*$: peaks shift", dict(ellA=325.0)),
             ("reionisation $\\tau$ up: all peaks drop", dict(tau=0.15)),
             ("tilt $n_s$ up: small scales rise", dict(ns=1.08))]
    fig, axs = plt.subplots(2, 2, figsize=(W, 3.3), sharex=True, sharey=True)
    for ax, (title, kw) in zip(axs.flat, cases):
        ax.plot(ell, base, color=GREY, lw=1.0, label="base")
        ax.plot(ell, toy_cmb(ell, **kw), color=RED, lw=1.1, label="knob turned")
        ax.set_title(title, fontsize=7.2); ax.set_yticks([])
    for ax in axs[1]:
        ax.set_xlabel("multipole $\\ell$")
    axs[0, 0].legend(frameon=False, fontsize=6.5)
    fig.text(0.01, 0.5, "temperature power (cartoon units)", rotation=90, va="center", fontsize=7.5)
    fig.tight_layout(rect=(0.03, 0, 1, 1)); fig.savefig("figures/cmb_cartoon.pdf"); plt.close(fig)


def fig_h0():
    fig, ax = plt.subplots(figsize=(W, 1.6))
    vals = [(67.4, 0.5, "CMB + base $\\Lambda$CDM", BLUE), (73.0, 1.0, "Cepheids + type Ia supernovae", RED)]
    for i, (v, e, lab, col) in enumerate(vals):
        ax.errorbar(v, i, xerr=e, fmt="o", color=col, capsize=3)
        ax.text(v, i + 0.28, lab, ha="center", fontsize=7, color=col)
    ax.axvspan(67.9, 72.0, color=LIGHT, zorder=0); ax.text(69.95, 0.5, "the gap", ha="center", fontsize=7, color=INK)
    ax.set_yticks([]); ax.set_ylim(-0.5, 1.7); ax.set_xlim(65, 76)
    ax.set_xlabel("$H_0$ (km s$^{-1}$ Mpc$^{-1}$)"); ax.spines["left"].set_visible(False)
    save(fig, "h0_tension")


# ---------------- Chapter 3 ----------------

def fig_nfw_profiles():
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.3))
    x = np.logspace(-2, 2, 300)
    axs[0].loglog(x, 1 / (x * (1 + x) ** 2), color=INK, label="NFW")
    a = 0.16; axs[0].loglog(x, 0.25 * np.exp(-(2 / a) * (x**a - 1)), color=RED, ls="--", label="Einasto, $\\alpha=0.16$")
    axs[0].loglog(x[x < 0.1], 0.4 / x[x < 0.1], color=GREY, lw=0.7); axs[0].text(0.012, 12, "$\\propto r^{-1}$", fontsize=7, color=GREY)
    axs[0].loglog(x[x > 8], 3 / x[x > 8] ** 3, color=GREY, lw=0.7); axs[0].text(12, 4e-3, "$\\propto r^{-3}$", fontsize=7, color=GREY)
    axs[0].set_xlabel("$r/r_s$"); axs[0].set_ylabel("$\\rho/\\rho_s$"); axs[0].legend(frameon=False, fontsize=6.5)
    xt = np.linspace(0.005, 1.2, 300)
    for c, col in ((5, BLUE), (10, INK), (20, RED)):
        axs[1].plot(xt, np.sqrt(m_nfw(c * xt) / m_nfw(c) / xt), color=col, label=f"$c={c}$")
    axs[1].set_xlabel("$r/r_{200}$"); axs[1].set_ylabel("$V_{\\rm circ}/V_{200}$"); axs[1].legend(frameon=False, fontsize=6.5)
    save(fig, "nfw_profiles")


def moster(M, M1=10**11.59, N=0.0351, beta=1.376, gamma=0.608):
    return 2 * N / ((M / M1) ** (-beta) + (M / M1) ** gamma)


def fig_shmr():
    M = np.logspace(10, 15, 400)
    fig, ax = plt.subplots(figsize=(W, 2.6))
    ax.loglog(M, moster(M), color=INK, lw=1.6)
    ax.loglog(M, moster(M, beta=1.0), color=BLUE, ls=":", lw=1, label="$\\beta$ turned down")
    ax.loglog(M, moster(M, gamma=0.9), color=RED, ls=":", lw=1, label="$\\gamma$ turned up")
    ax.axhline(0.156, color=GREY, ls="--", lw=0.7); ax.text(1.3e10, 0.17, "all baryons into stars (0.156)", fontsize=6.5, color=GREY)
    ax.annotate("$N$ sets the height", (10**11.59, 0.0351), xytext=(10**12.3, 0.08), arrowprops=dict(arrowstyle="->"), fontsize=7)
    ax.annotate("$M_1$ sets the position", (10**11.59, 0.02), xytext=(10**10.1, 0.045), arrowprops=dict(arrowstyle="->"), fontsize=7)
    ax.text(10**10.15, 1.5e-3, "low-mass slope $\\beta$", fontsize=7, color=BLUE)
    ax.text(10**13.6, 1.2e-3, "high-mass\nslope $\\gamma$", fontsize=7, color=RED)
    ax.set_xlabel("halo mass $M_{200}$ ($M_\\odot$)"); ax.set_ylabel("$M_*/M_{200}$")
    ax.set_ylim(5e-4, 0.4); ax.legend(frameon=False, loc="lower center", fontsize=6.5)
    save(fig, "shmr")


def fig_corenfw():
    r = np.logspace(-2.5, 1.2, 400); rc = 0.5
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.3))
    for n, col in ((0, INK), (0.5, BLUE), (1, RED)):
        M = m_nfw(r) * np.tanh(r / rc) ** n
        rho = np.gradient(M, r) / (4 * np.pi * r**2)
        axs[0].loglog(r, rho, color=col, label=f"$n={n}$")
        axs[1].plot(r, np.sqrt(M / r), color=col, label=f"$n={n}$")
    axs[0].set_xlabel("$r/r_s$"); axs[0].set_ylabel("density (NFW units)"); axs[0].legend(frameon=False, fontsize=6.5)
    axs[0].text(0.004, 3, "cusp", fontsize=7); axs[0].text(0.004, 0.06, "core", fontsize=7, color=RED)
    axs[1].set_xscale("log"); axs[1].set_xlabel("$r/r_s$"); axs[1].set_ylabel("$V_{\\rm circ}$ (NFW units)")
    axs[1].axvline(rc, color=GREY, ls=":", lw=0.7); axs[1].text(rc * 1.1, 0.02, "$r_c$", fontsize=7)
    save(fig, "corenfw")


def fig_contraction():
    M200, c = 1e12, 10.0; Md, Rd = 5e10, 3.0; fb = Md / M200
    Mb = lambda r: Md * (1 - (1 + r / Rd) * np.exp(-r / Rd))
    Mi = lambda r: nfw_mass(r, M200, c)
    rf = np.logspace(-0.5, 2, 120); MDMf = []
    for r in rf:
        F = lambda ri: ri * Mi(ri) - r * (Mb(r) + (1 - fb) * Mi(ri))
        ri = brentq(F, r * 1e-3, r * 50); MDMf.append((1 - fb) * Mi(ri))
    MDMf = np.array(MDMf)
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(rf, np.sqrt(G_KPC * (1 - fb) * Mi(rf) / rf), color=GREY, ls="--", label="dark matter before the disc forms")
    ax.plot(rf, np.sqrt(G_KPC * MDMf / rf), color=RED, label="after full contraction")
    ax.plot(rf, np.sqrt(G_KPC * Mb(rf) / rf), color=BLUE, label="the disc ($5\\times10^{10}M_\\odot$)")
    ax.set_xscale("log"); ax.set_xlabel("radius (kpc)"); ax.set_ylabel("circular speed (km s$^{-1}$)")
    ax.legend(frameon=False, fontsize=6.5)
    save(fig, "contraction")


def toy_galaxy(R, Mstar=4e10, Rd=3.0, Mgas=1e10, Rg=6.0):
    vb2 = freeman_v2(R, Mstar, Rd) + freeman_v2(R, Mgas, Rg)
    return vb2


def fig_rotation_anatomy():
    R = np.linspace(0.3, 40, 400)
    vb2 = toy_galaxy(R); gb = vb2 / R * UNIT_G
    vlaw = np.sqrt(law(gb, A0) * R * KPC) / 1e3
    vnfw = np.sqrt(vb2 + G_KPC * nfw_mass(R, 1.5e12, 8) / R)
    vf = (G * 5e10 * MSUN * A0) ** 0.25 / 1e3
    fig, ax = plt.subplots(figsize=(W, 2.6))
    ax.plot(R, np.sqrt(vb2), color=BLUE, label="stars + gas, Newton")
    ax.plot(R, vlaw, color=RED, lw=1.8, label="the law (one knob)")
    ax.plot(R, vnfw, color=INK, ls="--", label="stars + gas + an NFW halo")
    ax.axhline(vf, color=GOLD, ls=":", lw=1); ax.text(30, vf + 4, "$(GM_ba_0)^{1/4}$", color=GOLD, fontsize=7)
    ax.set_xlabel("radius (kpc)"); ax.set_ylabel("rotation speed (km s$^{-1}$)"); ax.set_ylim(0, 260)
    ax.legend(frameon=False, loc="lower right", fontsize=6.8)
    save(fig, "rotation_anatomy")


def fig_rar_toy():
    R = np.linspace(0.5, 60, 200)
    vb2 = toy_galaxy(R); gb = vb2 / R * UNIT_G
    gnfw = (vb2 + G_KPC * nfw_mass(R, 1.5e12, 8) / R) / R * UNIT_G
    x = np.logspace(-12.5, -8.5, 300)
    fig, ax = plt.subplots(figsize=(W, 2.8))
    ax.loglog(x, x, color=GREY, ls="--", lw=0.8, label="Newton: $g=g_{\\rm bar}$")
    ax.loglog(x, law(x, A0), color=RED, lw=1.6, label="the law")
    ax.loglog(gb, law(gb, A0), "o", color=RED, ms=2.5, mfc="white", label="toy galaxy under the law")
    ax.loglog(gb, gnfw, "s", color=INK, ms=2, label="same galaxy, NFW halo")
    ax.axvline(A0, color=GOLD, lw=0.7); ax.text(A0 * 1.15, 2e-12, "$a_0$", color=GOLD)
    ax.set_xlabel("$g_{\\rm bar}$ (m s$^{-2}$)"); ax.set_ylabel("$g_{\\rm obs}$ (m s$^{-2}$)")
    ax.legend(frameon=False, loc="upper left", fontsize=6.6)
    save(fig, "rar_toy")


# ---------------- Chapter 4 ----------------

def fig_recipe_flow():
    fig, ax = plt.subplots(figsize=(W, 3.9)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10.6)
    steps = [("measured stars and gas of one SPARC galaxy", 0),
             ("stars $\\rightarrow$ halo mass: stellar-to-halo relation", 4),
             ("halo shape: Einasto, $\\alpha=0.16$, $c(M)$ from simulations", 0),
             ("feedback energy $e$ $\\rightarrow$ core exponent $n=\\tanh e$", 4),
             ("core radius $r_c=\\eta R_{1/2}$", 2),
             ("contraction fraction $f=f_0+f_1\\log M_b$", 2),
             ("$g_{\\rm model}=g_{\\rm bar}+GM_{\\rm DM}(r)/r^2$", 0),
             ("compare with the law: rms, 95th percentile, worst bin", 0)]
    ys = np.linspace(10, 0.6, len(steps))
    for (txt, k), y in zip(steps, ys):
        ax.text(4.6, y, txt, ha="center", va="center", fontsize=7.2,
                bbox=dict(boxstyle="round,pad=0.35", fc="#f6f6f2", ec=GREY, lw=0.7))
        if k:
            ax.text(9.4, y, f"{k} knobs" if k > 1 else "1 knob", ha="center", va="center", fontsize=7, color="white",
                    bbox=dict(boxstyle="round,pad=0.3", fc=RED, ec=RED))
    for y0, y1 in zip(ys[:-1], ys[1:]):
        ax.annotate("", xy=(4.6, y1 + 0.42), xytext=(4.6, y0 - 0.42), arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))
    ax.text(9.4, 10.5, "R11 total: 12", ha="center", fontsize=7.5, weight="bold", color=RED)
    fig.savefig("figures/recipe_flow.pdf", bbox_inches="tight"); plt.close(fig)


def fig_level_vs_shape():
    x = np.logspace(-12.5, -8.5, 300)
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.4))
    for a, col, lab in ((0.5 * A0, BLUE, "$a=a_0/2$"), (A0, RED, "$a=a_0$"), (2 * A0, INK, "$a=2a_0$")):
        axs[0].loglog(x, law(x, a), color=col, label=lab)
    axs[0].loglog(x, x, color=GREY, ls="--", lw=0.7)
    axs[0].set_title("the level knob slides the curve", fontsize=7.2); axs[0].legend(frameon=False, fontsize=6.5)
    axs[0].set_xlabel("$g_{\\rm bar}$ (m s$^{-2}$)"); axs[0].set_ylabel("$g_{\\rm obs}$ (m s$^{-2}$)")
    R = np.linspace(0.5, 40, 200)
    axs[1].axhline(0, color=RED, lw=1.4, label="the law (every galaxy on this line)")
    for Rd, col, lab in ((1.0, INK, "compact disc, $R_d=1$ kpc"), (8.0, BLUE, "diffuse disc, $R_d=8$ kpc")):
        Mb = 3e10 * (1 - (1 + R / Rd) * np.exp(-R / Rd))
        gb = G_KPC * Mb / R**2 * UNIT_G
        gh = (G_KPC * (Mb + nfw_mass(R, 8e11, 10)) / R**2) * UNIT_G
        axs[1].semilogx(gb, np.log10(gh / law(gb, A0)), "o", ms=1.8, color=col, label=lab)
    axs[1].set_title("same halo, two discs", fontsize=7.2)
    axs[1].set_xlabel("$g_{\\rm bar}$ (m s$^{-2}$)"); axs[1].set_ylabel("halo model minus law (dex)")
    axs[1].legend(frameon=False, fontsize=5.9, loc="upper right"); axs[1].set_ylim(-0.05, 0.5)
    save(fig, "level_vs_shape")


def fig_core_exponent():
    x = np.logspace(-4, -1, 300)
    fig, ax = plt.subplots(figsize=(W, 2.3))
    for S, col in ((10, BLUE), (100, INK), (1000, RED)):
        e = 10 ** (-0.639) * (x / 0.01) ** (-0.760) * (S / 100) ** 0.091
        ax.semilogx(x, np.tanh(e), color=col, label=f"$\\Sigma_b={S}\\,M_\\odot\\,$pc$^{{-2}}$")
    ax.set_xlabel("star-formation efficiency $M_*/M_{200}$"); ax.set_ylabel("core exponent $n=\\tanh e$")
    ax.text(1.3e-4, 0.15, "tuned: $\\log\\epsilon=-0.639$, $a_1=-0.760$, $a_2=+0.091$", fontsize=6.8)
    ax.legend(frameon=False, fontsize=6.5); ax.set_ylim(0, 1.05)
    save(fig, "core_exponent")


def fig_observed_tie():
    names = ["the law\n(1 knob)", "R7\n(9)", "R11\n(12)", "R11b\n(14)"]; vals = [0.1951, 0.1964, 0.1953, 0.1933]
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.2), gridspec_kw=dict(width_ratios=[1, 1.2]))
    axs[0].bar(names, vals, color=[RED, INK, INK, INK]); axs[0].set_ylim(0, 0.22); axs[0].set_ylabel("rms to observed curves (dex)")
    axs[0].set_title("full scale", fontsize=7.2)
    axs[1].bar(names, vals, color=[RED, INK, INK, INK]); axs[1].set_ylim(0.19, 0.198)
    for i, v in enumerate(vals):
        axs[1].text(i, v + 0.0002, f"{v:.4f}", ha="center", fontsize=6.8)
    axs[1].set_title("zoomed: all within 0.003 dex", fontsize=7.2)
    for ax in axs:
        ax.tick_params(axis="x", labelsize=6.5)
    save(fig, "observed_tie")


# ---------------- Chapter 5 ----------------

def fig_bill():
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.8))
    crow = [("R9 (2$\\sigma$ priors)", -0.22, None), ("R8 (no priors)", -0.42, (-0.81, None)), ("R10 (functions)", -0.74, None),
            ("R5, formation start", math.log10(0.32), None)]
    mrow = [("R11", 0.11, (-0.23, 0.30)), ("R11b", 0.39, None), ("R8", 0.29, (None, 1.2)), ("R10", 0.46, None),
            ("A16 best", 0.64, None), ("R12", 0.11, (-0.23, 0.27)), ("R12, big galaxies", -0.80, None)]
    for ax, rows, s1, title in ((axs[0], crow, 0.11, "$\\Delta\\log c$ (median)"), (axs[1], mrow, 0.3, "$\\Delta\\log M_{200}$ (median)")):
        ax.axvspan(-2 * s1, 2 * s1, color=LIGHT, zorder=0); ax.axvspan(-s1, s1, color="#d5d9e0", zorder=0)
        for i, (nm, v, rng) in enumerate(rows):
            ax.scatter(v, -i, color=RED, zorder=3, s=16)
            if rng:
                lo, hi = rng
                ax.plot([lo if lo is not None else v, hi if hi is not None else v], [-i, -i], color=RED, lw=1)
        ax.set_yticks([-i for i in range(len(rows))]); ax.set_yticklabels([r[0] for r in rows], fontsize=6.4)
        ax.axvline(0, color=INK, lw=0.6); ax.set_title(title, fontsize=7.4); ax.tick_params(axis="y", length=0)
    axs[0].set_xlim(-0.95, 0.3); axs[1].set_xlim(-0.95, 1.3)
    fig.text(0.5, 0.01, "shaded: 1$\\sigma$ and 2$\\sigma$ prior widths around $\\Lambda$CDM's relations; bars: 16th--84th percentiles where reported", ha="center", fontsize=6, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig("figures/bill.pdf"); plt.close(fig)


def fig_needed_halo():
    R = np.logspace(-0.4, 1.7, 300)
    vb2 = toy_galaxy(R); gb = vb2 / R * UNIT_G
    vl2 = law(gb, A0) * R * KPC / 1e6
    Mdm = R * (vl2 - vb2) / G_KPC
    rho = np.gradient(Mdm, R) / (4 * np.pi * R**2)
    Mn = nfw_mass(R, 1.5e12, 8); rhon = np.gradient(Mn, R) / (4 * np.pi * R**2)
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.4))
    axs[0].loglog(R, Mdm, color=RED, label="halo the law needs (R5/R12)")
    axs[0].loglog(R, Mn, color=INK, ls="--", label="NFW, $1.5\\times10^{12}M_\\odot$, $c=8$")
    axs[0].set_xlabel("radius (kpc)"); axs[0].set_ylabel("dark mass inside $r$ ($M_\\odot$)"); axs[0].legend(frameon=False, fontsize=6)
    axs[1].loglog(R, rho / 1e9, color=RED); axs[1].loglog(R, rhon / 1e9, color=INK, ls="--")
    axs[1].set_xlabel("radius (kpc)"); axs[1].set_ylabel("density ($M_\\odot$ pc$^{-3}$)")
    save(fig, "needed_halo")


def eddington_f(rho_of_psi, E):
    """Eddington inversion with the second-derivative form; rho given as a function of Psi."""
    out = []
    for e in E:
        u = np.linspace(0, np.sqrt(e), 4000)[1:-1]; P = e - u**2; h = 1e-5 * max(e, 1e-3)
        d2 = (rho_of_psi(P + h) - 2 * rho_of_psi(P) + rho_of_psi(np.maximum(P - h, 1e-12))) / h**2
        out.append(2 * np.trapz(d2, u))
    return np.array(out) / (np.sqrt(8) * np.pi**2)


def fig_eddington():
    hern = lambda P: P**4 / (2 * np.pi * (1 - P))
    plk = lambda P: P**5 / (1 + P**2) ** 2.5
    Eh = np.linspace(0.02, 0.97, 60); fh = eddington_f(hern, Eh)
    Ek = np.linspace(0.05, 20, 120); fk = eddington_f(plk, Ek)
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.2))
    axs[0].semilogy(Eh, fh, color=GREEN); axs[0].set_title("Hernquist sphere: $f>0$ everywhere", fontsize=7.2)
    axs[0].set_xlabel("binding energy $\\mathcal{E}$"); axs[0].set_ylabel("$f(\\mathcal{E})$")
    axs[1].plot(Ek, fk / fk.max(), color=RED); axs[1].axhline(0, color=INK, lw=0.6)
    axs[1].fill_between(Ek, fk / fk.max(), 0, where=fk < 0, color=RED, alpha=0.3)
    axs[1].set_title("cored tracer around a point mass", fontsize=7.2)
    axs[1].set_xlabel("binding energy $\\mathcal{E}$"); axs[1].set_ylabel("$f/f_{\\max}$")
    i = int(np.argmin(fk)); axs[1].annotate(f"negative: {fk[i]/fk.max():.2f}", (Ek[i], fk[i] / fk.max()), xytext=(8, 0.5), arrowprops=dict(arrowstyle="->"), fontsize=7)
    save(fig, "eddington")


def fig_halo_vs_z():
    z = [0, 1, 1.5, 2.33]
    fig, ax = plt.subplots(figsize=(W, 2.6))
    ax.plot(z, [1, 1, 1, 1], color=GREY, ls="--", label="law, $w=-1$")
    ax.plot(z, [1, 0.93, 0.91, 0.92], "o-", color=GREEN, ms=3, label="R10 + 5 hand terms (typed in)")
    ax.plot(z, [1, 1.58, 2.12, 3.44], "s-", color=INK, ms=3, label="R10, no hand terms")
    ax.plot(z, [1, 1.76, 2.35, 3.49], "^:", color=BLUE, ms=3, label="$a\\propto H(z)$")
    ax.plot(z, [1, 1.76 ** (4 / 3), 2.35 ** (4 / 3), 3.49 ** (4 / 3)], "d-", color=RED, ms=3, label="halo at fixed $M$, $c$: $\\propto H^{4/3}$")
    ax.set_xlabel("redshift $z$"); ax.set_ylabel("scale relative to today"); ax.legend(frameon=False, fontsize=6.5)
    save(fig, "halo_vs_z")


def fig_lambda_pull():
    r = np.logspace(-1, 7, 400)
    rho = (A0 / (0.5 * C)) ** 2 / G
    gL = 8 * np.pi * G * rho * r * KPC / 3
    gb = G * 5e10 * MSUN / (r * KPC) ** 2
    fig, ax = plt.subplots(figsize=(W, 2.9))
    ax.loglog(r, gL, color=GOLD, lw=1.6, label="$\\Lambda$'s push, $\\frac{8\\pi G\\rho_{\\rm DE}}{3}\\,r$")
    ax.loglog(r, gb, color=BLUE, label="a $5\\times10^{10}M_\\odot$ galaxy, Newton")
    ax.loglog(r, law(gb, A0), color=RED, label="the same galaxy, the law")
    ax.axhline(A0, color=INK, lw=0.7, ls=":"); ax.text(0.15, A0 * 1.6, "$a_0$", fontsize=7.5)
    ax.scatter([10], [8 * np.pi * G * rho * 10 * KPC / 3], color=GOLD, zorder=3)
    ax.annotate("at 10 kpc: $1.1\\times10^{-5}a_0$", (10, 1e-15), xytext=(60, 1e-17), arrowprops=dict(arrowstyle="->"), fontsize=7)
    rx = 3 * A0 / (8 * np.pi * G * rho) / KPC
    ax.annotate(f"reaches $a_0$ at {rx/1e6:.1f} Gpc", (rx, A0), xytext=(1e4, 3e-14), arrowprops=dict(arrowstyle="->"), fontsize=7)
    ax.set_xlabel("distance (kpc)"); ax.set_ylabel("acceleration (m s$^{-2}$)"); ax.set_ylim(1e-18, 1e-6)
    fig.legend(frameon=False, fontsize=6.5, loc="lower center", ncol=3)
    fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig("figures/lambda_pull.pdf"); plt.close(fig)


def fig_c_barrier():
    h = 0.674; H0 = 67.4e3 / 3.0857e22
    lM = np.linspace(10, 15, 200); M = 10**lM
    c = 10 ** (0.905 - 0.101 * np.log10(M * h / 1e12))
    r200 = (G * M * MSUN / (100 * H0**2)) ** (1 / 3); V200 = 10 * H0 * r200
    a = 10 * H0 * V200 * c**2 / (2 * m_nfw(c))
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(lM, np.log10(a / A0), color=RED, lw=1.6, label="$2\\pi G\\rho_sr_s$ with a $c(M)$ relation")
    ax.axhline(0, color=INK, lw=0.7); ax.axhspan(-0.05, 0.05, color=LIGHT)
    ax.axvline(12, color=GREY, ls=":"); ax.text(10.1, 0.3, "near $a_0$ at $10^{12}M_\\odot$,\nby coincidence", fontsize=6.8)
    ax.set_xlabel("$\\log_{10}M_{200}/M_\\odot$"); ax.set_ylabel("$\\log_{10}(a_{\\rm halo}/a_0)$")
    ax2 = ax.twiny(); ax2.set_xlim(ax.get_xlim())
    ticks = [10, 11, 12, 13, 14, 15]; ax2.set_xticks(ticks)
    vv = [10 * H0 * (G * 10**t * MSUN / (100 * H0**2)) ** (1 / 3) for t in ticks]
    ax2.set_xticklabels([f"{C/v:.0f}" for v in vv], fontsize=6.5); ax2.set_xlabel("$c/V_{200}$", fontsize=7.5)
    ax.legend(frameon=False, loc="lower right", fontsize=6.5)
    save(fig, "c_barrier")


def fig_tie_gates():
    rows = ["$\\Lambda$ coincidence", "$cH/2\\pi$", "NFW centre", "Tully--Fisher at $f_b$", "strongest swoop (A15)",
            "interacting vacuum (A20)", "R10, no hand terms", "R10 + 5 hand terms", "R12 (law typed in)"]
    cols = ["$\\kappa\\approx\\frac{1}{2}$", "slope $\\frac{1}{2}$", "$z$ band", "one over\nmass", "acts in\ngalaxies"]
    m = [["P", "P", "P", "P", "F"], ["P", "-", "F", "P", "-"], ["F", "F", "F", "F", "P"], ["F", "-", "-", "F", "P"],
         ["F", "-", "F", "F", "P"], ["P", "-", "F", "F", "P"], ["F", "F", "F", "-", "P"], ["F*", "P", "P", "-", "P"],
         ["P", "P", "P", "P", "P†"]]
    fig, ax = plt.subplots(figsize=(W, 3.0))
    tiles(ax, m, rows, cols, fs=6.5)
    fig.text(0.02, 0.01, "* narrow miss of the 5% target.   † needs a coupling to dark energy that $\\Lambda$CDM lacks.   -- not reported.", fontsize=6)
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig("figures/tie_gates.pdf"); plt.close(fig)


def fig_coincidences():
    fig, ax = plt.subplots(figsize=(W, 1.8))
    ax.barh(["expected by chance\n(target slid off)", "distinct hits\nfrom $\\Lambda$CDM constants"], [62.1, 63], color=[GREY, RED])
    for y, v in enumerate([62.1, 63]):
        ax.text(v + 1, y, f"{v}", va="center", fontsize=7.5)
    ax.set_xlim(0, 80); ax.set_xlabel("formulas passing all three gates (of 199,584)")
    save(fig, "coincidences")


if __name__ == "__main__":
    for f in [fig_panels, fig_elephant, fig_holdout, fig_bic_rent, fig_bits_per_knob, fig_friedmann, fig_cmb_cartoon, fig_h0,
              fig_nfw_profiles, fig_shmr, fig_corenfw, fig_contraction, fig_rotation_anatomy, fig_rar_toy, fig_recipe_flow,
              fig_level_vs_shape, fig_core_exponent, fig_observed_tie, fig_bill, fig_needed_halo, fig_eddington,
              fig_halo_vs_z, fig_lambda_pull, fig_c_barrier, fig_tie_gates, fig_coincidences]:
        f(); print("ok", f.__name__)
