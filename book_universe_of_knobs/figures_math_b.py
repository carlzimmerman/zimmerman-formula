"""Figures for Parts II-V and the appendix (chapters 7-14). Run: python3 figures_math_b.py
Quoted numbers come from the fried chicken paper (v2.3) and PAPER67 (v1.2);
curves are computed from the formulas printed beside them in the book."""
import math
import numpy as np
from scipy.special import gammaln
from figstyle import *

A0K = A0 / UNIT_G  # a0 in (km/s)^2/kpc

# ---------------- Chapter 7 ----------------

def project(rho_fun, R):
    """Surface density Sigma(R) = 2 int rho(R cosh t) R cosh t dt."""
    out = []
    for Rv in R:
        t = np.linspace(0, np.arccosh(2e5 / Rv), 3000)
        rr = Rv * np.cosh(t)
        out.append(2 * np.trapz(rho_fun(rr) * rr, t))
    return np.array(out)


def delta_sigma(rho_fun, R):
    Rg = np.logspace(-2.5, np.log10(R.max()), 500)
    Sg = project(rho_fun, Rg)
    cum = np.concatenate([[0], np.cumsum(0.5 * (Sg[1:] * Rg[1:] ** 2 + Sg[:-1] * Rg[:-1] ** 2) * np.diff(np.log(Rg)))])
    mean_in = 2 * np.interp(R, Rg, cum) / R**2
    return mean_in - np.interp(R, Rg, Sg)


def fig_delta_sigma():
    M = 5e10
    rgrid = np.logspace(-3, 5.5, 4000)
    gN = G_KPC * M / rgrid**2
    Meff = law(gN, A0K) * rgrid**2 / G_KPC
    rho_ph = np.gradient(Meff - M, rgrid) / (4 * np.pi * rgrid**2)
    rho_law = lambda r: np.interp(r, rgrid, rho_ph)
    r200, rs = nfw_params(1.5e12, 8.0)
    rhos = 1.5e12 / (4 * np.pi * rs**3 * m_nfw(8.0))
    rho_nfw = lambda r: rhos / ((r / rs) * (1 + r / rs) ** 2)
    R = np.logspace(np.log10(30), np.log10(3000), 40)
    point = M / (np.pi * R**2)
    ds_law = (delta_sigma(rho_law, R) + point) / 1e6
    ds_nfw = (delta_sigma(rho_nfw, R) + point) / 1e6
    fig, ax = plt.subplots(figsize=(W, 2.7))
    ax.loglog(R, point / 1e6, color=BLUE, ls="--", label="stars and gas alone (Newton)")
    ax.loglog(R, ds_law, color=RED, lw=1.6, label="the law around the same galaxy")
    ax.loglog(R, ds_nfw, color=INK, label="plus an NFW halo, $1.5\\times10^{12}M_\\odot$")
    v2 = math.sqrt(G_KPC * M * A0K)
    ax.loglog(R, v2 / (4 * G_KPC * R) / 1e6, color=GREY, ls=":", lw=0.9, label="deep limit $\\sqrt{GMa_0}/4GR$")
    ax.set_xlabel("projected radius $R$ (kpc)"); ax.set_ylabel("$\\Delta\\Sigma$ ($M_\\odot$ pc$^{-2}$)")
    ax.legend(frameon=False, fontsize=6.5, loc="lower left")
    save(fig, "delta_sigma")


def fig_kids_chi2():
    rows = [("base $\\Lambda$CDM, untuned", 563.1), ("R12 cut at $R_{200}$", 457.7), ("R11 (12 knobs)", 277.9),
            ("plain law", 276.1), ("R11b (14 knobs)", 242.1), ("R13 (26 knobs)", 145.2), ("R14 ($\\sim$1066)", 69.6)]
    fig, ax = plt.subplots(figsize=(W, 2.4))
    for i, (nm, v) in enumerate(rows):
        col = RED if "law" in nm else (GREEN if v < 72 else INK)
        ax.barh(i, v, color=col)
        ax.text(v + 6, i, f"{v}", va="center", fontsize=7)
    ax.axvline(88.4, color=GOLD, ls="--"); ax.text(92, -0.75, "pass line ($p=0.01$)", color=GOLD, fontsize=6.6)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
    ax.set_xlabel("$\\chi^2$ on KiDS-1000 isolated lenses (60 points)"); ax.set_xlim(0, 640)
    save(fig, "kids_chi2")


def fig_r13_scoreboard():
    cols = ["L1\nlaw", "L2\nSPARC", "L3\nKiDS", "L4\nX-COP", "L5\ntie", "L6\n$a(z)$", "L7\nCassini", "L8\nunseen", "L9\nbounds"]
    fig, ax = plt.subplots(figsize=(W, 1.25))
    tiles(ax, [["F", "P", "F", "W", "W", "W", "P", "F", "F"]], ["R13"], cols, fs=6.5)
    fig.text(0.02, 0.02, "weak: L4 rests on a baryon fraction at its bound; L5 and L6 rest on five hand terms.", fontsize=6.2)
    fig.tight_layout(rect=(0, 0.12, 1, 1)); fig.savefig("figures/r13_scoreboard.pdf"); plt.close(fig)


def fig_xcop_compare():
    fig, axs = plt.subplots(1, 2, figsize=(W, 1.9))
    axs[0].axvspan(-0.05, 0.05, color=LIGHT); axs[0].scatter([-0.467, -0.001], [1, 0], color=[RED, INK], s=22)
    axs[0].set_yticks([1, 0]); axs[0].set_yticklabels(["the law", "R13 (tuned)"]); axs[0].axvline(0, color=INK, lw=0.6)
    axs[0].set_xlabel("mean log offset on X-COP (dex)"); axs[0].set_xlim(-0.55, 0.15)
    axs[1].barh([1, 0], [0.476, 0.075], color=[RED, INK]); axs[1].axvline(0.12, color=GOLD, ls="--")
    axs[1].set_yticks([]); axs[1].set_xlabel("rms (dex); pass line 0.12")
    save(fig, "xcop_compare")


# ---------------- Chapter 8 ----------------

def fig_sum_vs_law():
    y = np.logspace(-3, 3, 400)
    nu_law = 0.5 + np.sqrt(0.25 + 1 / y); nu_sum = 1 + 1 / np.sqrt(y)
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.3))
    axs[0].loglog(y, nu_law, color=RED, label="the law")
    axs[0].loglog(y, nu_sum, color=INK, ls="--", label="$g_{\\rm bar}+\\sqrt{a\\,g_{\\rm bar}}$")
    axs[0].set_xlabel("$g_{\\rm bar}/a$"); axs[0].set_ylabel("boost $g/g_{\\rm bar}$"); axs[0].legend(frameon=False, fontsize=6.5)
    d = np.log10(nu_sum / nu_law)
    axs[1].semilogx(y, d, color=INK); axs[1].axhline(0, color=RED, lw=0.8)
    axs[1].scatter([1], [math.log10(2 / 1.6180)], color=GOLD, zorder=3)
    axs[1].annotate("at $g_{\\rm bar}=a$: 2 vs $\\varphi=1.618$\n0.092 dex", (1, 0.0915), xytext=(3, 0.06), arrowprops=dict(arrowstyle="->"), fontsize=6.6)
    axs[1].set_xlabel("$g_{\\rm bar}/a$"); axs[1].set_ylabel("sum form minus law (dex)")
    save(fig, "sum_vs_law")


def fig_kitchens_map():
    pts = [("R11", 12, 0.0415, INK), ("R11b", 14, 0.0275, INK), ("A16", 15, 0.0252, INK), ("A25", 28, 0.0222, INK),
           ("A25 wide", 28, 0.0204, INK), ("R10", 42, 0.0213, INK), ("SIDM A19", 343, 0.0487, INK), ("SIDM A41", 514, 0.0472, INK),
           ("R9", 1026, 0.0152, INK), ("wave A17", 6, 0.0921, GREY), ("hydro A18", 3, 0.073, GREY), ("superfluid, emergent", 1, 0.0392, GREY), ("de Sitter A37", 1, 0.0189, GREY), ("dipolar (shape chosen)", 3, 0.0036, GREEN),
           ("k-mouflage", 3, 0.0086, GREEN), ("Kaplinghat-Turner x0.398", 1, 0.0152, GREEN), ("R6 empirical", 1, 0.0075, GREEN),
           ("Magneticum (published)", 0.7, 0.029, BLUE)]
    fig, ax = plt.subplots(figsize=(W, 3.1))
    for nm, k, d, col in pts:
        ax.scatter(k, d, color=col, s=16, zorder=3)
        off = {"A25 wide": (3, -8), "R10": (4, 3), "A25": (-12, 5), "A16": (-14, -9), "R11b": (3, 2), "de Sitter A37": (4, -8),
               "SIDM A41": (3, -8), "Kaplinghat-Turner x0.398": (4, -3)}.get(nm, (3, 2))
        ax.annotate(nm, (k, d), xytext=off, textcoords="offset points", fontsize=5.8, color=col)
    ax.axhline(0.02, color=RED, ls="--", lw=0.8); ax.text(120, 0.0185, "frozen target 0.02", color=RED, fontsize=6.5)
    ax.axhspan(0.0218, 0.0226, color=LIGHT, zorder=0); ax.text(60, 0.0232, "the 28-ingredient plateau", fontsize=6.3, color=INK)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("knobs"); ax.set_ylabel("best distance to the law (dex)")
    ax.set_ylim(0.003, 0.12)
    ax.text(0.7, 0.0034, "green: law's shape put in by choice; grey: other kitchens; dark: $\\Lambda$CDM recipes", fontsize=6)
    save(fig, "kitchens_map")


# ---------------- Chapter 9 ----------------

def fig_flux_lattice():
    q1, q2 = 1.0, 1.37
    i, j = np.meshgrid(np.arange(-12, 13), np.arange(-9, 10))
    x, y = (i * q1).ravel(), (j * q2).ravel()
    r = np.hypot(x, y); R0, dR = 8.6, 0.35
    sel = np.abs(r - R0) < dR
    fig, ax = plt.subplots(figsize=(W, 3.0))
    ax.scatter(x[~sel], y[~sel], s=3, color=GREY)
    ax.scatter(x[sel], y[sel], s=14, color=RED, zorder=3)
    t = np.linspace(0, 2 * np.pi, 400)
    for rr in (R0 - dR, R0 + dR):
        ax.plot(rr * np.cos(t), rr * np.sin(t), color=RED, lw=0.6)
    ax.set_aspect("equal"); ax.set_xlabel("$n_1q_1$"); ax.set_ylabel("$n_2q_2$")
    ax.set_title("every dot is a universe; red dots have $\\Lambda\\approx0$", fontsize=7.2)
    save(fig, "flux_lattice")


def fig_vacua_count():
    J = np.arange(10, 801)
    fig, ax = plt.subplots(figsize=(W, 2.6))
    for x, col in ((10, BLUE), (30, INK), (54, RED)):
        lg = (J / 2) * np.log10(2 * np.pi * np.e * x**2 / J) - 0.5 * np.log10(np.pi * J)
        ax.plot(J, lg, color=col, label=f"fluxes up to $\\pm${x}")
    ax.axhline(120, color=GOLD, ls="--"); ax.text(15, 135, "$10^{120}$: enough to reach the observed $\\Lambda$", fontsize=6.6, color=GOLD)
    ax.axhline(500, color=GREY, ls=":"); ax.text(15, 515, "$10^{500}$", fontsize=6.6, color=GREY)
    ax.set_xlabel("number of flux cycles $J$"); ax.set_ylabel("$\\log_{10}$ (number of flux vacua)")
    ax.set_ylim(0, 800); ax.legend(frameon=False, fontsize=6.5, loc="upper right")
    save(fig, "vacua_count")


def fig_bits_ladder():
    rows = [("$\\kappa$ (my law)", 6.6, RED), ("base $\\Lambda$CDM, 6 knobs", 50, BLUE),
            ("all measured constants", 360, GREY), ("the landscape, $10^{500}$", 1661, GOLD),
            ("one F-theory geometry", 903564, GOLD)]
    fig, ax = plt.subplots(figsize=(W, 2.0))
    for i, (nm, b, col) in enumerate(rows):
        ax.barh(i, b, color=col); ax.text(b * 1.2, i, f"{b:,}" if b > 100 else f"{b}", va="center", fontsize=7)
    ax.set_xscale("log"); ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
    ax.set_xlabel("information needed to set the knobs (bits)"); ax.set_xlim(1, 1e8)
    save(fig, "bits_ladder")


# ---------------- Chapter 10 ----------------

def fig_law_quadratic():
    g = np.linspace(0, 3, 400)
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.3))
    axs[0].plot(g, g**2 / (g + 1), color=RED, label="$g_{\\rm bar}=g^2/(g+a_0)$")
    axs[0].plot(g, g, color=GREY, ls="--", label="Newton, $g_{\\rm bar}=g$")
    axs[0].axhline(0.5, color=BLUE, lw=0.7); axs[0].axvline(1, color=BLUE, lw=0.7)
    axs[0].scatter([1], [0.5], color=BLUE, zorder=3)
    axs[0].annotate("$g=a_0$ needs only\n$g_{\\rm bar}=a_0/2$", (1, 0.5), xytext=(1.5, 0.25), arrowprops=dict(arrowstyle="->"), fontsize=6.6)
    axs[0].set_xlabel("$g/a_0$ (what stars feel)"); axs[0].set_ylabel("$g_{\\rm bar}/a_0$ (Newton from baryons)")
    axs[0].legend(frameon=False, fontsize=6.3, loc="upper left")
    y = np.logspace(-3, 2, 300); nu = 0.5 + np.sqrt(0.25 + 1 / y)
    axs[1].loglog(y, nu, color=RED)
    for yy in (0.1, 0.5, 10):
        v = 0.5 + math.sqrt(0.25 + 1 / yy); axs[1].scatter(yy, v, color=INK, s=12, zorder=3)
        axs[1].annotate(f"{v:.2f}", (yy, v), xytext=(4, 3), textcoords="offset points", fontsize=6.5)
    axs[1].set_xlabel("$g_{\\rm bar}/a_0$"); axs[1].set_ylabel("boost $g/g_{\\rm bar}$")
    save(fig, "law_quadratic")


def fig_interp_family():
    y = np.logspace(-3, 3, 400)
    fams = [("simple (the law)", 0.5 + np.sqrt(0.25 + 1 / y), RED, "-"),
            ("standard $\\mu=x/\\sqrt{1+x^2}$", np.sqrt(0.5 + np.sqrt(0.25 + 1 / y**2)), BLUE, "--"),
            ("RAR exponential", 1 / (1 - np.exp(-np.sqrt(y))), GREEN, "-."),
            ("sum form", 1 + 1 / np.sqrt(y), INK, ":")]
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.4))
    for nm, nu, col, ls in fams:
        axs[0].loglog(y, nu, color=col, ls=ls, label=nm)
        axs[1].semilogx(y, np.log10(nu / fams[0][1]), color=col, ls=ls)
    axs[0].set_xlabel("$g_{\\rm bar}/a_0$"); axs[0].set_ylabel("boost $g/g_{\\rm bar}$"); axs[0].legend(frameon=False, fontsize=5.9)
    axs[1].set_xlabel("$g_{\\rm bar}/a_0$"); axs[1].set_ylabel("difference from the law (dex)")
    save(fig, "interp_family")


def fig_btfr():
    Mb = np.logspace(7, 12, 200)
    fig, ax = plt.subplots(figsize=(W, 2.6))
    for a, col, lab in ((A0, RED, "canonical, $a_0=9.36\\times10^{-11}$"), (A0_ALT, BLUE, "alternative, $a_0=1.131\\times10^{-10}$")):
        ax.loglog((G * Mb * MSUN * a) ** 0.25 / 1e3, Mb, color=col, label=lab)
    for m in (1e9, 1e10, 6e10, 1e11):
        v = (G * m * MSUN * A0) ** 0.25 / 1e3; ax.scatter(v, m, color=INK, s=12, zorder=3)
        ax.annotate(f"{v:.0f} km/s", (v, m), xytext=(-48, 4), textcoords="offset points", fontsize=6.5)
    ax.text(20, 3e10, "slope 4:\n$M_b=v_f^4/Ga_0$", fontsize=7)
    ax.set_xlabel("flat rotation speed $v_f$ (km s$^{-1}$)"); ax.set_ylabel("baryonic mass $M_b$ ($M_\\odot$)")
    ax.legend(frameon=False, fontsize=6.5, loc="lower right")
    save(fig, "btfr")


def fig_footings():
    pts = [("$2\\pi$ horizon form on $\\rho_{\\rm DE}$", 8.62, 2.83, 154.3, GREY), ("$\\kappa=\\frac{1}{2}$ on $\\rho_{\\rm DE}$ (canonical)", 9.36, 1.82, 63.9, RED),
           ("Milgrom $cH_0/2\\pi$", 10.42, 0.53, 5.34, INK), ("free best fit", 10.766, 0.0, 0.0, GREEN),
           ("$\\kappa=\\frac{1}{2}$ on $\\rho_c$ (alternative)", 11.312, 0.60, 7.04, BLUE)]
    fig, ax = plt.subplots(figsize=(W, 2.5))
    for nm, x, s, d, col in pts:
        ax.plot([x, x], [0, s], color=col, lw=1.2); ax.scatter(x, s, color=col, s=18, zorder=3)
        ax.annotate(f"{nm}\n$\\Delta\\chi^2={d}$", (x, s), xytext=(5, 14 if "alternative" in nm else 2), textcoords="offset points", fontsize=6.2, color=col)
    ax.set_xlabel("$a_0$ ($10^{-11}$ m s$^{-2}$)"); ax.set_ylabel("distance from best fit ($\\sigma$, clustered)")
    ax.set_xlim(8.3, 12.6); ax.set_ylim(0, 3.4)
    save(fig, "footings")


# ---------------- Chapter 11 ----------------

def fig_sb_tilt():
    fig, ax = plt.subplots(figsize=(W, 1.8))
    ax.axvspan(-0.29, -0.17, color="#f1c9c4"); ax.text(-0.285, 2.3, "mass-set halos (retired sector):\n$-0.17$ to $-0.29$ per dex", fontsize=6.5, color=RED)
    ax.errorbar([-0.016, -0.023], [1, 0], xerr=[0.061, 0.063], fmt="o", color=INK, capsize=3)
    ax.set_yticks([1, 0]); ax.set_yticklabels(["law, canonical", "law, alternative"]); ax.axvline(0, color=GREY, lw=0.7)
    ax.set_xlabel("residual slope with surface brightness (per dex)"); ax.set_ylim(-0.6, 3.2)
    save(fig, "sb_tilt")


def fig_wins_panels():
    fig, axs = plt.subplots(2, 2, figsize=(W, 3.2))
    a = axs[0, 0]; a.bar(["law", "native\nhalo 1", "native\nhalo 2"], [0.0541, 0.0682, 0.0694], color=[RED, INK, INK])
    a.set_title("SPARC rms (dex), lower is tighter", fontsize=7); a.set_ylim(0, 0.08)
    a = axs[0, 1]; a.bar(["law", "native halo"], [-0.025, 0.138], color=[RED, INK]); a.axhline(0, color=GREY, lw=0.7)
    a.set_title("LITTLE THINGS dwarfs, median $E$", fontsize=7)
    a = axs[1, 0]; a.axhspan(-2, 2, color=LIGHT); a.bar(["canonical", "alternative"], [0.31, -0.31], color=[RED, BLUE])
    a.set_title("63 groups, $Z$ (inside $\\pm2$ passes)", fontsize=7); a.set_ylim(-2.5, 2.5)
    a = axs[1, 1]; a.axhspan(-0.15, 0.15, color=LIGHT); a.bar(["MeerKAT vs SPARC"], [0.032], color=RED, width=0.4)
    a.set_title("local $a_0$ offset (dex), line 0.15", fontsize=7); a.set_ylim(-0.2, 0.2)
    for a in axs.flat:
        a.tick_params(axis="x", labelsize=6.5)
    save(fig, "wins_panels")


def fig_knob_economy():
    pts = [("the law", 1, 0.1951, RED), ("R7", 9, 0.1964, INK), ("R11", 12, 0.1953, INK), ("R11b", 14, 0.1933, INK), ("R13", 26, 0.1943, INK)]
    fig, ax = plt.subplots(figsize=(W, 2.3))
    for nm, k, v, col in pts:
        ax.scatter(k, v, color=col, s=24, zorder=3); ax.annotate(nm, (k, v), xytext=(4, 4), textcoords="offset points", fontsize=7, color=col)
    ax.axhspan(0.1933, 0.1964, color=LIGHT, zorder=0)
    ax.set_xscale("log"); ax.set_ylim(0.185, 0.205); ax.set_xlim(0.7, 50)
    ax.set_xlabel("knobs"); ax.set_ylabel("rms to observed curves (dex)")
    ax.text(0.8, 0.1865, "same fit to the data; the difference is what was tuned, and to what", fontsize=6.6)
    save(fig, "knob_economy")


def fig_v3s_tiles():
    cols = ["every\nclass", "Solar\nSystem", "PPN\n$\\gamma,\\beta$", "lensing", "GW\nspeed", "health\n(a),(c)", "health\n(b)", "W2\nnumerics", "clusters,\nCMB"]
    fig, ax = plt.subplots(figsize=(W, 1.3))
    tiles(ax, [["P", "P", "P", "W", "P", "P", "U", "U", "-"]], ["v3s"], cols, fs=6.3)
    fig.text(0.02, 0.02, "weak: lensing gate has little power.  --: outside the adopted scope; failures there stand.", fontsize=6.1)
    fig.tight_layout(rect=(0, 0.12, 1, 1)); fig.savefig("figures/v3s_tiles.pdf"); plt.close(fig)


# ---------------- Chapter 12 ----------------

def fig_fg1_heatmap():
    cols = ["S", "Tl", "LT", "G", "K", "X", "Ln", "Dw", "MW", "DM", "IC"]
    rows = ["C1 native N", "C2 N + response", "C3 basin split", "C4 the law alone", "C5 native + resp."]
    m = [list("PFFPFPFFFFF"), ["F", "F", "F", "P", "F", "F", "F", "-", "F", "P", "-"], ["P", "P", "P", "P", "F", "P", "P", "P", "F", "-", "F"],
         list("PPPPFFPFFFF"), list("FFFFFFFFPPF")]
    fig, ax = plt.subplots(figsize=(W, 2.1))
    tiles(ax, m, rows, cols, fs=5.6)
    fig.text(0.01, 0.01, "S SPARC, Tl tilt, LT LITTLE THINGS, G groups, K cluster keys, X X-COP, Ln KiDS, Dw Local Group,\nMW Milky Way, DM DiskMass, IC IC 1613.", fontsize=5.8)
    fig.tight_layout(rect=(0, 0.13, 1, 1)); fig.savefig("figures/fg1_heatmap.pdf"); plt.close(fig)


def fig_clusters():
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.3))
    a = axs[0]
    a.bar([0, 1], [2.93, 2.72], color=[RED, BLUE], width=0.35, label="as measured")
    a.bar([0.4, 1.4], [2.23, 2.06], color=[RED, BLUE], width=0.35, alpha=0.45, label="hydrostatic masses 0.12 dex lower")
    a.axhline(1, color=INK, lw=0.8); a.set_xticks([0.2, 1.2]); a.set_xticklabels(["canonical", "alternative"])
    a.set_ylabel("$M_{\\rm HSE}/M_{\\rm law}$ (X-COP)"); a.legend(frameon=False, fontsize=5.6, loc="upper center"); a.set_ylim(0, 4.6)
    a = axs[1]
    a.errorbar([0, 1], [1.91, 1.01], yerr=[0.12, 0.09], fmt="o", color=RED, capsize=3, label="canonical")
    a.errorbar([0.1], [1.75], yerr=[0.11], fmt="s", color=BLUE, capsize=3, label="alternative")
    a.axhline(1, color=INK, lw=0.8); a.set_xticks([0, 1]); a.set_xticklabels(["0.5--1.2 Mpc", "1.2--3 Mpc"])
    a.set_ylabel("shear amplitude $A$ (318 clusters)"); a.set_xlim(-0.5, 1.5); a.set_ylim(0.7, 2.2); a.legend(frameon=False, fontsize=6)
    save(fig, "clusters")


def fig_cmb_lensing_shape():
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.loglog([28, 377], [14, 0.08], "o-", color=RED, label="the law alone (QUMOND, baryons-only start)")
    ax.loglog([28, 377], [7, 0.04], "o:", color=GOLD, label="with $a_0$ tracking dark energy: same shape, about half")
    ax.fill_between([100, 1000], [1 / 7, 1 / 7], [1 / 1.5, 1 / 1.5], color=BLUE, alpha=0.2, label="screening added by hand: 1.5--7$\\times$ low")
    ax.axhline(1, color=INK, lw=0.8); ax.text(12, 1.15, "matches the measured lensing", fontsize=6.6)
    ax.set_xlim(10, 1500); ax.set_ylim(0.02, 40); ax.set_xlabel("lensing multipole $L$"); ax.set_ylabel("predicted / measured")
    ax.legend(frameon=False, fontsize=6.1, loc="upper right")
    save(fig, "cmb_lensing_shape")


def fig_dwarf_z():
    names = ["MW ultra-\nfaints", "bright\nM31", "other\nM31", "MW\nclassicals", "field"]
    z0 = [5.22, 2.20, 2.29, 1.69, 0.57]; zefe = [6.76, 3.97, None, None, None]
    fig, ax = plt.subplots(figsize=(W, 2.3))
    x = np.arange(len(names))
    ax.axhspan(-2, 2, color=LIGHT)
    ax.bar(x - 0.18, z0, width=0.34, color=RED, label="the law")
    ax.bar([i + 0.18 for i, v in enumerate(zefe) if v], [v for v in zefe if v], width=0.34, color=INK, label="with the external field")
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=6.6); ax.set_ylabel("$Z$ (inside $\\pm2$ passes)")
    ax.legend(frameon=False, fontsize=6.5)
    save(fig, "dwarf_z")


def fig_solar_system():
    fig, ax = plt.subplots(figsize=(W, 2.2))
    ax.plot([0, 0], [2.44, 4.59], color=RED, lw=8, solid_capstyle="butt"); ax.plot([0.25, 0.25], [2.85, 5.19], color=BLUE, lw=8, solid_capstyle="butt")
    ax.plot([1, 1], [1.69, 5.18], color=INK, lw=8, solid_capstyle="butt")
    ax.scatter([2, 2.25], [1 / 4.8e7, 1 / 5.7e7], color=[RED, BLUE], s=30, zorder=3)
    ax.axhline(1, color=GOLD, ls="--"); ax.text(1.55, 1.4, "Cassini's 2$\\sigma$ line", color=GOLD, fontsize=6.8)
    ax.set_yscale("log"); ax.set_ylim(1e-9, 30)
    ax.set_xticks([0.12, 1, 2.12]); ax.set_xticklabels(["law, unscreened\n(canonical, alt)", "every unscreened\naction class (AX1)", "v3s, screened\n(C6P)"], fontsize=6.6)
    ax.set_ylabel("$Q_2$ signal / allowed")
    save(fig, "solar_system")


def fig_rq3_counts():
    rows = [("Newton", 10, 38, 0, 48), ("law, canonical", 22, 25, 2, 47), ("law, alternative", 20, 27, 2, 47),
            ("gas term, canonical", 29, 15, 0, 52), ("gas term, alt", 25, 19, 0, 52)]
    fig, ax = plt.subplots(figsize=(W, 2.1))
    for i, (nm, p, f, d, n) in enumerate(rows):
        left = 0
        for v, col in ((p, GREEN), (f, RED), (d, GOLD), (n, LIGHT)):
            ax.barh(i, v, left=left, color=col); left += v
        ax.text(1, i, f"{p} pass, {f} fail", va="center", fontsize=6.3, color="white")
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
    ax.set_xlabel("rows of the 96-row list (grey: not computable)")
    save(fig, "rq3_counts")


def fig_lens_colour():
    fig, ax = plt.subplots(figsize=(W, 2.1))
    steps = ["first lane", "forward model,\nhot gas added", "with measured\nkSZ gas"]
    ax.errorbar([0], [1.016], yerr=[0.086], fmt="o", color=BLUE, capsize=3)
    ax.plot([0, 1, 2], [1.016, 0.878, 0.861], "o-", color=BLUE, label="blue lenses")
    ax.plot([0, 1, 2], [1.587, 1.313, 1.306], "s-", color=RED, label="red lenses")
    ax.axhline(1, color=INK, lw=0.8); ax.set_xticks([0, 1, 2]); ax.set_xticklabels(steps, fontsize=6.6)
    ax.set_ylabel("lensing amplitude $A$"); ax.legend(frameon=False, fontsize=6.5); ax.set_xlim(-0.4, 2.4)
    save(fig, "lens_colour")


# ---------------- Chapter 13 ----------------

def cpl_ratio(z, w0, wa):
    return np.sqrt((1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z)))


def fig_cpl_family():
    z = np.linspace(0, 3, 200)
    fig, ax = plt.subplots(figsize=(W, 2.8))
    for w0 in np.linspace(-1.2, -0.6, 4):
        for wa in np.linspace(-1.4, 0.4, 5):
            ax.plot(z, cpl_ratio(z, w0, wa), color=GREY, lw=0.5, alpha=0.7)
    ax.plot(z, np.ones_like(z), color=RED, lw=2, label="$w=-1$: exactly flat")
    ax.plot(z, cpl_ratio(z, -0.75, -0.8), color=GOLD, lw=1.6, label="illustrative $w_0=-0.75$, $w_a=-0.8$")
    ax.plot([0, 1, 1.5, 2.33], [1, 1.76, 2.35, 3.49], "^:", color=BLUE, ms=4, label="rival: $a_0\\propto H(z)$")
    ax.set_xlabel("redshift $z$"); ax.set_ylabel("$a_0(z)/a_0(0)=\\sqrt{\\rho_{\\rm DE}(z)/\\rho_{\\rm DE}(0)}$")
    ax.set_ylim(0, 3.7); ax.legend(frameon=False, fontsize=6.5, loc="upper left")
    ax.text(1.65, 0.25, "grey: 20 dark energy histories,\nzero galaxy knobs in any of them", fontsize=6.5, color=INK)
    save(fig, "cpl_family")


def fig_btfr_shift():
    z = np.array([1, 1.5, 2.33]); m = np.array([0.91, 0.94, 0.91]); lo = np.array([0.76, 0.71, 0.33]); hi = np.array([1.03, 1.12, 1.21])
    fig, ax = plt.subplots(figsize=(W, 2.6))
    sh = -np.log10(m)
    ax.errorbar(z, sh, yerr=[sh - (-np.log10(hi)), -np.log10(lo) - sh], fmt="o", color=RED, capsize=3, label="the law (68% band)")
    ax.plot([0, 1, 1.5, 2.33], [0] + list(-np.log10([1.76, 2.35, 3.49])), "^:", color=BLUE, label="$a_0\\propto H(z)$")
    ax.plot([2.33, 2.33], [-math.log10(3.02), -math.log10(4.55)], color=INK, lw=6, alpha=0.5, solid_capstyle="butt", label="tuned $\\Lambda$CDM recipe (A26)")
    ax.axhline(0, color=GREY, lw=0.7)
    ax.set_xlabel("redshift $z$"); ax.set_ylabel("shift in $\\log M_b$ at fixed $v_f$ (dex)")
    ax.legend(frameon=False, fontsize=6.5, loc="lower left")
    save(fig, "btfr_shift")


def fig_decision_power():
    cm = np.linspace(0, 0.1, 400)
    fig, ax = plt.subplots(figsize=(W, 2.6))
    for budget, col, lab in ((0.055, RED, "$z=1$ (budget 0.055 dex)"), (0.084, BLUE, "$z=2.33$ (budget 0.084 dex)")):
        N = np.where(cm < budget, 0.14**2 / np.clip(budget**2 - cm**2, 1e-12, None), np.nan)
        ax.semilogy(cm, N, color=col, label=lab)
        ax.axvline(budget, color=col, ls=":", lw=0.7)
    ax.scatter([0.05, 0.05], [41, 5], color=INK, zorder=3)
    ax.annotate("frozen rule: 41 galaxies", (0.05, 41), xytext=(0.004, 300), arrowprops=dict(arrowstyle="->"), fontsize=6.6)
    ax.annotate("frozen rule: 5 galaxies", (0.05, 5), xytext=(0.004, 1.5), arrowprops=dict(arrowstyle="->"), fontsize=6.6)
    ax.text(0.058, 1.2e3, "every sample on disk:\n0.30--0.60 dex,\nfar off the chart", fontsize=6.4, color=INK)
    ax.set_xlabel("common-mode mass error of a sample (dex)"); ax.set_ylabel("galaxies needed (0.14 dex each)")
    ax.set_ylim(1, 1e4); ax.legend(frameon=False, fontsize=6.4, loc="lower right")
    save(fig, "decision_power")


def fig_timeline():
    ev = [("6 Nov 2026", "ALMA U4_28473 goes public: one galaxy's mass budget (not $a_0(z)$)", INK),
          ("28 Nov 2026*", "GS4_24110 [CI](2-1): cannot separate $n=1$ from $n=2$", INK),
          ("about Dec 2026", "Gaia DR4 wide binaries: sealed prediction $\\gamma=1.149$ (alt 1.208)", INK),
          ("not scheduled", "one clean deep-MOND $a_0$ at $z\\approx2.5$ to 0.10 dex: the real test of the tie", RED)]
    fig, ax = plt.subplots(figsize=(W, 2.0)); ax.axis("off")
    ax.plot([0.9, 0.9], [-0.3, len(ev) - 0.7], color=INK, lw=1.2)
    for i, (d, t, col) in enumerate(ev):
        y = len(ev) - 1 - i
        ax.scatter(0.9, y, color=col, s=30, zorder=3)
        ax.text(0.8, y, d, ha="right", va="center", fontsize=7, weight="bold", color=col)
        ax.text(1.0, y, t, ha="left", va="center", fontsize=6.6, color=col)
    ax.text(0.0, -0.75, "* date from earlier metadata, to be rechecked", fontsize=5.8, color=GREY)
    ax.set_xlim(0, 6.2); ax.set_ylim(-0.9, len(ev) - 0.5)
    fig.savefig("figures/timeline.pdf", bbox_inches="tight"); plt.close(fig)


def fig_wide_binaries():
    fig, ax = plt.subplots(figsize=(W, 1.9))
    ax.axhline(0, color=INK, lw=0.8)
    marks = [(1.000, "Newton", INK, 0.35), (0.986, "failed local\nfilter rule", GREY, -0.55), (1.137, "AQUAL", BLUE, 0.35),
             (1.149, "the law,\nsealed (CW1)", RED, -0.55), (1.208, "alt footing", RED, 0.35), (1.33, "MOND\nbenchmark", BLUE, -0.55)]
    ax.fill_between([1.05, 1.10], -0.1, 0.1, color=GOLD, alpha=0.5); ax.text(1.075, 0.35, "MI band", ha="center", fontsize=6.3, color=GOLD)
    for x, lab, col, y in marks:
        ax.plot([x, x], [-0.12, 0.12], color=col, lw=1.6); ax.text(x, y, lab, ha="center", fontsize=6.2, color=col)
    ax.errorbar([1.205], [-0.95], xerr=[0.035], fmt="o", color=GREY, capsize=3)
    ax.text(1.205, -1.35, "DR3 dry run: evidence for nothing", ha="center", fontsize=6, color=GREY)
    ax.set_xlim(0.95, 1.38); ax.set_ylim(-1.5, 0.7); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("wide-binary velocity ratio $\\gamma$ (1 = Newton)")
    save(fig, "wide_binaries")


def fig_redshift_rise():
    rows = [("halo at fixed $M$, $c$ ($H^{4/3}$)", 5.29, 5.29, INK), ("tuned 14-knob recipe (A26)", 3.02, 4.55, INK),
            ("Verlinde with $H_0$ (A24)", 3.51, 3.51, INK), ("rival $a_0\\propto H(z)$", 3.49, 3.49, BLUE),
            ("R10, no hand terms", 3.44, 3.44, INK), ("$cH/2\\pi$", 3.432, 3.432, INK), ("feedback via SHMR (A14)", 3.2, 3.2, INK),
            ("strongest swoop (A15)", 1.493, 1.493, INK), ("Kaplinghat--Turner (A34)", 1.42, 1.42, INK), ("ZOMG simulation (A21)", 1.305, 1.428, INK),
            ("R10 + hand terms (typed in)", 0.92, 0.92, GREY), ("the law, $w=-1$", 1.0, 1.0, RED), ("the law, measured $\\rho_{\\rm DE}(z)$", 0.33, 1.21, RED)]
    fig, ax = plt.subplots(figsize=(W, 3.4))
    for i, (nm, lo, hi, col) in enumerate(rows):
        if hi > lo:
            ax.plot([lo, hi], [i, i], color=col, lw=5, solid_capstyle="butt", alpha=0.7)
        else:
            ax.scatter(lo, i, color=col, s=20, zorder=3)
    ax.scatter([0.91], [len(rows) - 1], color=RED, marker="|", s=80, zorder=4)
    ax.axvline(1, color=RED, lw=0.7, ls=":")
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=6.6); ax.invert_yaxis()
    ax.set_xlabel("acceleration scale at $z=2.33$ / today"); ax.set_xlim(0, 5.6)
    save(fig, "redshift_rise")


# ---------------- Appendix ----------------

def fig_dex_ruler():
    fig, ax = plt.subplots(figsize=(W, 1.3))
    ax.plot([0.015, 1.1], [0, 0], color=INK, lw=1.2)
    for d in (0.02, 0.0415, 0.1, 0.2, 0.3, 0.5, 1.0):
        ax.plot([d, d], [-0.05, 0.05], color=RED, lw=1)
        ax.text(d, 0.12, f"{d} dex", ha="center", fontsize=6.3)
        ax.text(d, -0.22, f"$\\times${10**d:.3g}", ha="center", fontsize=6.3)
    ax.set_xscale("log"); ax.set_xlim(0.014, 1.25); ax.set_ylim(-0.4, 0.35); ax.axis("off")
    save(fig, "dex_ruler")


if __name__ == "__main__":
    for f in [fig_delta_sigma, fig_kids_chi2, fig_r13_scoreboard, fig_xcop_compare, fig_sum_vs_law, fig_kitchens_map,
              fig_flux_lattice, fig_vacua_count, fig_bits_ladder, fig_law_quadratic, fig_interp_family, fig_btfr, fig_footings,
              fig_sb_tilt, fig_wins_panels, fig_knob_economy, fig_v3s_tiles, fig_fg1_heatmap, fig_clusters, fig_cmb_lensing_shape,
              fig_dwarf_z, fig_solar_system, fig_rq3_counts, fig_lens_colour, fig_cpl_family, fig_btfr_shift, fig_decision_power,
              fig_timeline, fig_wide_binaries, fig_redshift_rise, fig_dex_ruler]:
        f(); print("ok", f.__name__)
