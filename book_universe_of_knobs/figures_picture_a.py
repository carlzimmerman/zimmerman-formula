"""Picture-book illustrations and explainer charts, preface to chapter 7.
Run: python3 figures_picture_a.py
Illustrations are drawings, not data. Every number printed on a chart is quoted from the
fried chicken paper (v2.3) or PAPER67 (v1.2), or computed from the formula beside it."""
import math
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle, Wedge, Polygon, Arc
from scipy import stats
from figstyle import *

rng_global = np.random.default_rng(7)


def canvas(w=W, h=3.0):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10 * h / w); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc="#f6f6f2", ec=GREY, fs=7, color=INK, weight="normal", r=0.15):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={r}", fc=fc, ec=ec, lw=0.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color, weight=weight, wrap=True)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=0.9, style="->"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle=style, color=color, lw=lw))


def savefig(fig, name, tight=True):
    if tight:
        fig.savefig(f"figures/{name}.pdf", bbox_inches="tight", pad_inches=0.03)
    else:
        fig.tight_layout(); fig.savefig(f"figures/{name}.pdf")
    plt.close(fig)


# ---------------- Preface ----------------

def plate_roadmap():
    fig, ax = canvas(h=2.6)
    x = np.linspace(0.4, 9.6, 400); y = 2.6 + 1.0 * np.sin(x * 1.25)
    ax.plot(x, y, color=LIGHT, lw=14, solid_capstyle="round", zorder=0)
    ax.plot(x, y, color="white", lw=1.2, ls=(0, (4, 4)), zorder=1)
    stops = [(1.0, "I", "The Knob Shop", "what a knob is", INK), (3.0, "II", "The Fried\nChicken Kitchen", "12 to 1066 knobs", RED),
             (5.0, "III", "$10^{500}$ Clicks", "the landscape", GOLD), (7.0, "IV", "One Knob", "$\\kappa=\\frac{1}{2}$", BLUE),
             (9.0, "V", "The Knob That\nCan't Be Turned", "$a_0(z)$", GREEN)]
    for xs, num, title, sub, col in stops:
        ys = 2.6 + 1.0 * np.sin(xs * 1.25)
        ax.add_patch(Circle((xs, ys), 0.42, fc=col, ec="white", lw=1.5, zorder=3))
        ax.text(xs, ys, num, ha="center", va="center", color="white", fontsize=9, weight="bold", zorder=4)
        ax.text(xs, ys + 0.55, title, ha="center", va="bottom", fontsize=6.8, weight="bold", color=col)
        ax.text(xs, ys - 0.55, sub, ha="center", va="top", fontsize=6.2, color=INK)
    savefig(fig, "plate_roadmap")


# ---------------- Chapter 1 ----------------

def plate_amplifier():
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.0))
    t = np.linspace(0, 4 * np.pi, 400)
    song = np.sin(t) + 0.45 * np.sin(2.7 * t + 0.4) + 0.25 * np.sin(5.3 * t)
    for ax, n, title in ((axs[0], 1, "one dial: one kind of sound"), (axs[1], 30, "thirty dials: any sound at all")):
        ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(FancyBboxPatch((0.3, 1.0), 4.2, 3.6, boxstyle="round,pad=0.05,rounding_size=0.3", fc="#2b2f3a", ec=INK))
        ax.add_patch(Circle((1.4, 2.4), 0.8, fc="#555b6a", ec="white", lw=0.8))
        ax.add_patch(Circle((1.4, 2.4), 0.3, fc="#888", ec="white", lw=0.5))
        if n == 1:
            dial(ax, 3.3, 3.2, 0.45, 0.6, nticks=9, color="white", face="#2b2f3a")
        else:
            for k in range(n):
                dial(ax, 2.6 + 0.36 * (k % 5), 4.15 - 0.36 * (k // 5), 0.13, (k * 0.37) % 1, nticks=5, color="white", face="#2b2f3a", lw=0.5)
        tt = np.linspace(5.2, 9.7, 400)
        ax.plot(tt, 4.2 + 0.35 * song, color=GREY, lw=0.9)
        out = 0.9 * np.sin(t) if n == 1 else song
        ax.plot(tt, 2.2 + 0.35 * out, color=RED, lw=1.1)
        ax.text(7.45, 5.1, "the song", ha="center", fontsize=6.5, color=GREY)
        ax.text(7.45, 0.9, "what the box plays", ha="center", fontsize=6.5, color=RED)
        ax.set_title(title, fontsize=7.2)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.02, wspace=0.05)
    fig.savefig("figures/plate_amplifier.pdf"); plt.close(fig)


def knob_anatomy():
    fig, ax = canvas(h=3.2)
    cx, cy, r = 2.3, 3.4, 1.45
    th0, th1 = np.deg2rad(225), np.deg2rad(-45)
    ax.add_patch(Circle((cx, cy), r, fc="white", ec=INK, lw=1.2))
    tt = np.linspace(th0, th1, 300)
    ax.plot(cx + 1.25 * r * np.cos(tt), cy + 1.25 * r * np.sin(tt), color=BLUE, lw=5, alpha=0.25)
    sel = np.linspace(th0 + (th1 - th0) * 0.48, th0 + (th1 - th0) * 0.62, 60)
    ax.plot(cx + 1.25 * r * np.cos(sel), cy + 1.25 * r * np.sin(sel), color=RED, lw=5, alpha=0.6)
    for t, lab in ((th0, "lower\nbound"), (th1, "upper\nbound")):
        ax.plot([cx + 1.1 * r * np.cos(t), cx + 1.45 * r * np.cos(t)], [cy + 1.1 * r * np.sin(t), cy + 1.45 * r * np.sin(t)], color=INK, lw=2)
        ax.text(cx + 1.75 * r * np.cos(t), cy + 1.75 * r * np.sin(t), lab, ha="center", va="center", fontsize=6.6)
    tp = th0 + (th1 - th0) * 0.55
    ax.plot([cx, cx + 0.85 * r * np.cos(tp)], [cy, cy + 0.85 * r * np.sin(tp)], color=RED, lw=2.4)
    ax.add_patch(Circle((cx, cy), 0.15 * r, color=INK))
    notes = [(7.25, 6.2, "the prior: every setting allowed\nbefore looking (blue arc)", BLUE),
             (7.25, 4.6, "the data-allowed width:\nsettings the data still permit (red arc)", RED),
             (7.25, 3.0, "the setting: the best value\n(the pointer)", INK),
             (7.25, 1.4, "bits = log$_2$(blue / red):\nhow much the data taught you", GREEN)]
    for x, y, t, col in notes:
        ax.text(x, y, t, ha="center", va="center", fontsize=6.8, color=col,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=col, lw=0.7))
    savefig(fig, "knob_anatomy")


def knob_species():
    fig, axs = plt.subplots(2, 3, figsize=(W, 3.0))
    titles = ["global knob", "per-object knobs", "shape knob", "hand term", "prior", "choices"]
    for ax, t in zip(axs.flat, titles):
        ax.set_xlim(0, 4); ax.set_ylim(0, 3); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(FancyBboxPatch((0.05, 0.05), 3.9, 2.9, boxstyle="round,pad=0.02,rounding_size=0.2", fc="#f6f6f2", ec=GREY, lw=0.6))
        ax.set_title(t, fontsize=7.2, color=INK)
    dial(axs[0, 0], 2, 1.5, 0.75, 0.4, nticks=9)
    for k in range(12):
        dial(axs[0, 1], 0.55 + 0.97 * (k % 4), 2.3 - 0.8 * (k // 4), 0.24, (k * 0.29) % 1, nticks=5, lw=0.6)
    x = np.linspace(0.3, 3.7, 100)
    for f, col in ((lambda u: 0.4 + 1.8 * (1 - np.exp(-u)), INK), (lambda u: 0.4 + 0.65 * u, BLUE), (lambda u: 0.4 + 2.0 * u / (1 + u), RED)):
        axs[0, 2].plot(x, f(x), color=col, lw=1)
    axs[1, 0].text(2, 1.5, "$c\\propto\\rho_{\\rm DE}^{\\,3}$", ha="center", va="center", fontsize=11, color=RED, rotation=-6, family="serif")
    axs[1, 0].plot([0.6, 3.4], [0.9, 0.85], color=RED, lw=0.6)
    axs[1, 1].add_patch(Rectangle((0.4, 1.2), 3.2, 0.6, fc=BLUE, alpha=0.25))
    axs[1, 1].plot([0.4, 0.4], [1.0, 2.0], color=INK, lw=2); axs[1, 1].plot([3.6, 3.6], [1.0, 2.0], color=INK, lw=2)
    axs[1, 1].scatter([3.55], [1.5], color=RED, zorder=3, s=14); axs[1, 1].text(2, 0.6, "pinned at the edge?", ha="center", fontsize=6)
    for k, (dx, dy) in enumerate([(1, 0.8), (1, -0.8)]):
        axs[1, 2].plot([0.4, 1.4], [1.5, 1.5 + dy * 0.8], color=INK, lw=1)
        for dy2 in (0.45, -0.45):
            axs[1, 2].plot([1.4, 2.6], [1.5 + dy * 0.8, 1.5 + dy * 0.8 + dy2], color=INK, lw=0.8)
            for dy3 in (0.2, -0.2):
                axs[1, 2].plot([2.6, 3.6], [1.5 + dy * 0.8 + dy2, 1.5 + dy * 0.8 + dy2 + dy3], color=GREY, lw=0.6)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.01, wspace=0.06, hspace=0.25)
    fig.savefig("figures/knob_species.pdf"); plt.close(fig)


def chi2_dist():
    fig, ax = plt.subplots(figsize=(W, 2.4))
    x = np.linspace(0, 140, 800)
    for nu, col in ((5, BLUE), (20, INK), (60, RED)):
        ax.plot(x, stats.chi2.pdf(x, nu), color=col, label=f"$\\nu={nu}$")
        ax.axvspan(nu - math.sqrt(2 * nu), nu + math.sqrt(2 * nu), color=col, alpha=0.08)
    ax.axvline(stats.chi2.ppf(0.99, 60), color=GOLD, ls="--")
    ax.text(stats.chi2.ppf(0.99, 60) + 2, 0.08, "99% line for 60 points:\n$\\chi^2=88.4$", fontsize=6.6, color=GOLD)
    for v, lab in ((145.2, "R13"), (276.1, "the law")):
        ax.annotate(f"{lab}: {v}, off the chart", (139, 0.004), xytext=(96, 0.03 if lab == "R13" else 0.045), fontsize=6.4, arrowprops=dict(arrowstyle="->", color=GREY))
    ax.set_xlabel("$\\chi^2$"); ax.set_ylabel("probability density"); ax.legend(frameon=False, fontsize=6.6)
    ax.set_xlim(0, 140); ax.set_ylim(0, 0.17)
    savefig(fig, "chi2_dist", tight=False)


def mackay_occam():
    fig, ax = plt.subplots(figsize=(W, 2.4))
    d = np.linspace(-10, 10, 600)
    simple = stats.norm.pdf(d, 0, 1.2); flex = stats.norm.pdf(d, 0, 5.0)
    ax.plot(d, simple, color=RED, lw=1.6, label="few knobs: bets on a narrow range of outcomes")
    ax.plot(d, flex, color=INK, lw=1.4, ls="--", label="many knobs: spreads its bets thin")
    ax.axvspan(-0.8, 0.8, color=GREEN, alpha=0.15); ax.text(0, 0.36, "what we\nobserved", ha="center", fontsize=6.6, color=GREEN)
    ax.axvspan(5.5, 7.0, color=GOLD, alpha=0.15); ax.text(6.25, 0.12, "a surprise", ha="center", fontsize=6.6, color=GOLD)
    ax.set_xlabel("every outcome the data could have had"); ax.set_ylabel("$P$(data | model)")
    ax.set_yticks([]); ax.legend(frameon=False, fontsize=6.4, loc="upper left")
    savefig(fig, "mackay_occam", tight=False)


def forking_paths():
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.2), gridspec_kw=dict(width_ratios=[1.3, 1]))
    m = np.arange(1, 61)
    axs[0].plot(m, 1 - 0.95 ** m, color=RED)
    for mm in (1, 5, 14, 30):
        axs[0].scatter(mm, 1 - 0.95 ** mm, color=INK, s=12, zorder=3)
        axs[0].annotate(f"{100*(1-0.95**mm):.0f}%", (mm, 1 - 0.95 ** mm), xytext=(4, -9), textcoords="offset points", fontsize=6.5)
    axs[0].set_xlabel("analysis choices tried after seeing the data"); axs[0].set_ylabel("chance of a fluke 'win'")
    axs[0].set_ylim(0, 1.02)
    ax = axs[1]; ax.axis("off"); ax.set_xlim(0, 4); ax.set_ylim(0, 4)
    def tree(x, y, depth, spread):
        if depth == 0:
            ax.scatter(x, y, s=8, color=GOLD if rng_global.random() < 0.15 else GREY, zorder=3); return
        for s in (-1, 1):
            ax.plot([x, x + 1], [y, y + s * spread], color=INK, lw=0.6)
            tree(x + 1, y + s * spread, depth - 1, spread / 2)
    tree(0.2, 2, 3, 1.0)
    ax.text(2, 0.1, "each fork is a hidden knob", ha="center", fontsize=6.6)
    savefig(fig, "forking_paths", tight=False)


def freeze_timeline():
    fig, ax = canvas(h=1.7)
    steps = [("write the\ntargets", INK), ("commit\nthem", INK), ("write the\nscript", INK), ("run it", INK),
             ("broken twin\nmust fail", RED), ("rerun:\nsame bytes", INK), ("publish,\nwin or lose", GREEN)]
    for i, (t, col) in enumerate(steps):
        x = 0.05 + i * 1.42
        box(ax, x, 1.4, 1.30, 1.2, t, fs=5.4, color=col, ec=col)
        if i < len(steps) - 1:
            arrow(ax, x + 1.31, 2.0, x + 1.46, 2.0)
    ax.text(5, 0.7, "nothing to the right of 'commit' may change anything to its left", ha="center", fontsize=6.8, style="italic", color=GREY)
    savefig(fig, "freeze_timeline")


def bounds_pileup():
    rng = np.random.default_rng(11)
    want = rng.normal(-0.35, 0.18, 171)
    got = np.clip(want, -0.22, 0.22)
    fig, ax = plt.subplots(figsize=(W, 2.2))
    bins = np.linspace(-0.8, 0.3, 45)
    ax.hist(want, bins=bins, color=GREY, alpha=0.5, label="what the galaxies 'want'")
    ax.hist(got, bins=bins, color=RED, alpha=0.8, label="what the bounded fit can give")
    ax.axvspan(-0.22, 0.22, color=BLUE, alpha=0.08); ax.axvline(-0.22, color=INK, lw=1.4)
    ax.text(-0.215, 60, "the bound", fontsize=6.8)
    ax.set_xlabel("shift of a knob from its expected value (dex)"); ax.set_ylabel("galaxies")
    ax.legend(frameon=False, fontsize=6.6, loc="upper left")
    savefig(fig, "bounds_pileup", tight=False)


# ---------------- Chapter 2 ----------------

def plate_cmb_sky():
    from figures_math_a import toy_cmb
    rng = np.random.default_rng(5)
    n = 256; L = np.deg2rad(20.0)
    kx = np.fft.fftfreq(n, d=L / n) * 2 * np.pi
    kk = np.sqrt(kx[:, None] ** 2 + kx[None, :] ** 2); ell = np.clip(kk, 2, None)
    Dl = toy_cmb(ell); Cl = Dl / (ell * (ell + 1)) * (1 - np.exp(-(kk / 40.0) ** 2))
    Cl[0, 0] = 0.0
    field = np.fft.ifft2(np.fft.fft2(rng.normal(size=(n, n))) * np.sqrt(Cl)).real
    field /= field.std()
    fig = plt.figure(figsize=(W, 3.0))
    ax = fig.add_axes([0.02, 0.28, 0.96, 0.7]); ax.imshow(field[:128, :], cmap="RdBu_r", vmin=-3, vmax=3, extent=(0, 20, 0, 10), aspect="equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.3, 9.1, "a simulated 20-by-10-degree patch of microwave sky (toy spectrum)", fontsize=6.6, color="white",
            bbox=dict(fc="black", alpha=0.35, ec="none", pad=1.5))
    ax2 = fig.add_axes([0.02, 0.0, 0.96, 0.26]); ax2.set_xlim(0, 12); ax2.set_ylim(0, 2.6); ax2.set_aspect("equal"); ax2.axis("off")
    for i, nm in enumerate(["$\\omega_b$", "$\\omega_c$", "$\\theta_*$", "$\\tau$", "$A_s$", "$n_s$"]):
        dial(ax2, 1.0 + 2.0 * i, 1.55, 0.5, 0.25 + 0.09 * i, nticks=9, label=nm, fs=7)
    fig.savefig("figures/plate_cmb_sky.pdf"); plt.close(fig)


def cmb_anatomy():
    from figures_math_a import toy_cmb
    ell = np.linspace(2, 2000, 1500); D = toy_cmb(ell)
    fig, ax = plt.subplots(figsize=(W, 2.6))
    ax.plot(ell, D, color=RED, lw=1.4)
    notes = [(30, "large scales:\nseeds as they were", (60, 0.12)), (220, "first peak: the\nacoustic angle $\\theta_*$", (330, 2.0)),
             (520, "second peak lower:\nbaryons load the wave", (600, 1.5)), (810, "third peak:\ndark matter driving", (960, 1.15)),
             (1500, "damping tail:\nphotons diffuse", (1380, 0.72))]
    for x, t, xy in notes:
        ax.annotate(t, (x, np.interp(x, ell, D)), xytext=xy, fontsize=6.3, arrowprops=dict(arrowstyle="->", color=GREY))
    ax.set_xlabel("multipole $\\ell$ (smaller angles $\\rightarrow$)"); ax.set_ylabel("power (cartoon units)"); ax.set_yticks([])
    ax.set_ylim(0, 2.3)
    savefig(fig, "cmb_anatomy", tight=False)


def sound_horizon():
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.2))
    ax = axs[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2)
    ax.add_patch(Circle((0, 0), 0.18, color=RED))
    for rr, a in ((0.7, 0.25), (1.3, 0.45), (1.9, 0.9)):
        ax.add_patch(Circle((0, 0), rr, fill=False, ec=BLUE, lw=1.4, alpha=a))
    ax.annotate("", xy=(1.9, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=INK))
    ax.text(0.95, 0.12, "$r_s$", fontsize=8); ax.set_title("a sound wave spreads from each clump", fontsize=7)
    ax = axs[1]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(-3, 3)
    ax.plot([0.5, 9.0], [0, 1.2], color=INK, lw=0.8); ax.plot([0.5, 9.0], [0, -1.2], color=INK, lw=0.8)
    ax.plot([9.0, 9.0], [-1.2, 1.2], color=BLUE, lw=2)
    ax.add_patch(Circle((0.5, 0), 0.18, color=INK)); ax.text(0.5, -0.6, "us", ha="center", fontsize=6.6)
    ax.add_patch(Arc((0.5, 0), 3, 3, theta1=-7.6, theta2=7.6, color=RED, lw=1.2)); ax.text(2.2, 0.0, "$\\theta_*$", fontsize=8, color=RED, va="center")
    ax.text(9.25, 0, "$r_s$", fontsize=8, color=BLUE, va="center")
    ax.text(4.8, -1.5, "$D_M$: distance to the CMB", ha="center", fontsize=6.6)
    ax.set_title("$\\theta_*=r_s/D_M$: a ruler seen from afar", fontsize=7)
    savefig(fig, "sound_horizon", tight=False)


def vacuum_catastrophe():
    hbar_c = 3.1615e-26  # J m
    GeV = 1.602e-10
    rows = [("Planck-scale cutoff", 1.22e19), ("grand unification, $10^{16}$ GeV", 1e16), ("electroweak, 100 GeV", 100.0), ("strong force, 0.2 GeV", 0.2)]
    meas = (A0 / (0.5 * C)) ** 2 / G * C**2
    fig, ax = plt.subplots(figsize=(W, 2.3))
    for i, (nm, E) in enumerate(rows):
        rho = (E * GeV) ** 4 / hbar_c**3
        ax.barh(i, math.log10(rho / meas), color=INK)
        ax.text(math.log10(rho / meas) + 1.5, i, f"$10^{{{math.log10(rho/meas):.0f}}}$ too big", va="center", fontsize=6.6)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
    ax.set_xlabel("$\\log_{10}$(naive estimate / measured value)"); ax.set_xlim(0, 145)
    savefig(fig, "vacuum_catastrophe", tight=False)


def lcdm_panel_full():
    fig, ax = canvas(h=3.1)
    ax.add_patch(FancyBboxPatch((0.2, 0.2), 9.6, 5.6, boxstyle="round,pad=0.02,rounding_size=0.25", fc="#f6f6f2", ec=GREY))
    for i, nm in enumerate(["$\\omega_b$", "$\\omega_c$", "$\\theta_*$", "$\\tau$", "$A_s$", "$n_s$"]):
        dial(ax, 1.1 + 1.55 * i, 4.6, 0.45, 0.3 + 0.07 * i, nticks=9, label=nm, fs=7)
    ax.text(5, 5.45, "the six", ha="center", fontsize=7, weight="bold", color=BLUE)
    small = ["$\\Omega_k$", "$\\sum m_\\nu$", "$N_{\\rm eff}$", "$Y_P$", "running", "$r$", "$w_0$", "$w_a$", "$A_{\\rm lens}$"]
    for i, nm in enumerate(small):
        dial(ax, 0.9 + 1.03 * i, 2.55, 0.25, 0.5, nticks=7, label=nm, fs=5.6, color=GREY)
    ax.text(5, 3.2, "the defaults (set, not fitted)", ha="center", fontsize=6.6, color=GREY)
    for i in range(26):
        dial(ax, 0.75 + 0.33 * i, 0.85, 0.11, (i * 0.31) % 1, nticks=5, lw=0.4, color=GREY)
    ax.text(5, 0.35, "nuisance: foregrounds, calibration, beams", ha="center", fontsize=6.4, color=GREY)
    savefig(fig, "lcdm_panel_full")


def w0wa_plane():
    fig, ax = plt.subplots(figsize=(W, 2.7))
    w0 = np.linspace(-1.6, -0.3, 10)
    ax.fill_between([-1.0, -0.3], [-3, -3], [0, 0], color=GOLD, alpha=0.15)
    ax.text(-0.66, -2.6, "$w_0>-1$, $w_a<0$:\nwhere recent combined\nfits have leaned\n(schematic)", ha="center", fontsize=6.4, color=INK)
    ax.plot(w0, -1 - w0, color=GREY, ls="--"); ax.text(-1.55, 0.7, "$w_0+w_a=-1$:\nearly-time $w=-1$", fontsize=6.2, color=GREY)
    ax.scatter([-1], [0], color=RED, s=40, zorder=3); ax.annotate("cosmological constant:\n$a_0$ exactly flat", (-1, 0), xytext=(-1.55, -1.3), fontsize=6.6, arrowprops=dict(arrowstyle="->"))
    ax.scatter([-0.75], [-0.8], color=GOLD, s=30, zorder=3, marker="s"); ax.annotate("Chapter 13's\nillustration", (-0.75, -0.8), xytext=(-0.45, -1.3), fontsize=6.4, arrowprops=dict(arrowstyle="->"))
    ax.axhline(0, color=LIGHT, lw=0.8); ax.axvline(-1, color=LIGHT, lw=0.8)
    ax.set_xlim(-1.6, -0.3); ax.set_ylim(-3, 1.8); ax.set_xlabel("$w_0$ (today)"); ax.set_ylabel("$w_a$ (how fast it changes)")
    savefig(fig, "w0wa_plane", tight=False)


# ---------------- Chapter 3 ----------------

def plate_galaxy():
    rng = np.random.default_rng(3)
    fig, ax = plt.subplots(figsize=(W, 3.2)); ax.set_aspect("equal"); ax.axis("off")
    yy, xx = np.mgrid[-10:10:300j, -10:10:300j]; rr = np.hypot(xx, yy)
    ax.imshow(np.exp(-rr / 5.0), extent=(-10, 10, -10, 10), cmap="Purples", alpha=0.35, vmin=0, vmax=1.4, origin="lower")
    for arm in range(2):
        th = np.linspace(0.3, 4.4 * np.pi, 2200); r = 0.9 * np.exp(0.16 * th)
        sel = r < 8.0
        x = r[sel] * np.cos(th[sel] + arm * np.pi) + rng.normal(0, 0.22, sel.sum()); y = r[sel] * np.sin(th[sel] + arm * np.pi) + rng.normal(0, 0.22, sel.sum())
        ax.scatter(x, y, s=rng.uniform(0.3, 3, sel.sum()), color="#e3b505", alpha=0.75, lw=0)
    gx = rng.normal(0, 3.6, 900); gy = rng.normal(0, 3.6, 900)
    ax.scatter(gx, gy, s=0.8, color=BLUE, alpha=0.35, lw=0)
    ax.scatter(rng.normal(0, 0.7, 500), rng.normal(0, 0.7, 500), s=2, color="#ffefb0", alpha=0.9, lw=0)
    ax.add_patch(Circle((0, 0), 9.5, fill=False, ec=PURPLE, ls="--", lw=0.8))
    ax.text(5.6, 8.4, "where the extra gravity\nseems to be (a halo,\nor a modified law)", fontsize=6.4, color=PURPLE)
    ax.text(-9.6, -9.0, "stars: what we see in light", fontsize=6.4, color="#b8860b")
    ax.text(-9.6, 8.6, "gas: extends further out", fontsize=6.4, color=BLUE)
    ax.set_xlim(-10, 10); ax.set_ylim(-10, 10)
    fig.patch.set_facecolor("white")
    savefig(fig, "plate_galaxy")


def law_diversity():
    R = np.linspace(0.2, 30, 300)
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.4), sharey=True)
    for Rd, col, lab in ((1.0, INK, "compact disc"), (5.0, BLUE, "diffuse disc")):
        vb2 = freeman_v2(R, 2e10, Rd); gb = vb2 / R * UNIT_G
        axs[0].plot(R, np.sqrt(law(gb, A0) * R * KPC) / 1e3, color=col, label=lab)
        axs[1].plot(R, np.sqrt(vb2 + G_KPC * nfw_mass(R, 8e11, 10) / R), color=col, label=lab)
    axs[0].set_title("the law: shapes follow the baryons", fontsize=7); axs[1].set_title("one halo for both: shapes converge", fontsize=7)
    for ax in axs:
        ax.set_xlabel("radius (kpc)")
    axs[0].set_ylabel("rotation speed (km s$^{-1}$)"); axs[0].legend(frameon=False, fontsize=6.6)
    savefig(fig, "law_diversity", tight=False)


def rar_anatomy():
    x = np.logspace(-3, 2, 300)
    fig, ax = plt.subplots(figsize=(W, 2.9))
    ax.loglog(x, law(x, 1.0), color=RED, lw=1.8)
    ax.loglog(x, x, color=GREY, ls="--", lw=0.8)
    ax.fill_between([1e-3, 0.1], 1e-3, 1e3, color=BLUE, alpha=0.06); ax.fill_between([10, 100], 1e-3, 1e3, color=GREY, alpha=0.06)
    ax.text(1.3e-3, 20, "deep regime:\n$g=\\sqrt{g_{\\rm bar}a_0}$,\nslope $\\frac{1}{2}$", fontsize=6.8, color=BLUE)
    ax.text(12, 0.02, "Newton:\n$g=g_{\\rm bar}$,\nslope 1", fontsize=6.8, color=INK)
    ax.text(0.45, 0.08, "the bend:\n$g_{\\rm bar}\\approx a_0$", fontsize=6.8, color=GOLD)
    ax.plot([1e-2, 1e-1, 1e-1], [law(1e-2, 1), law(1e-2, 1), law(1e-1, 1)], color=BLUE, lw=0.7)
    ax.plot([20, 60, 60], [law(20, 1), law(20, 1), law(60, 1)], color=INK, lw=0.7)
    ax.set_xlabel("$g_{\\rm bar}/a_0$ (the pull of what we see)"); ax.set_ylabel("$g/a_0$ (the pull stars feel)")
    ax.set_xlim(1e-3, 100); ax.set_ylim(1e-2, 100)
    savefig(fig, "rar_anatomy", tight=False)


def halo_scaling():
    M = np.logspace(9, 15, 200); H = H0_KPC
    r200 = (G_KPC * M / (100 * H**2)) ** (1 / 3); V200 = 10 * H * r200
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.3))
    axs[0].loglog(M, r200, color=INK); axs[1].loglog(M, V200, color=RED)
    for m in (1e10, 1e12, 1e14):
        r = (G_KPC * m / (100 * H**2)) ** (1 / 3); v = 10 * H * r
        axs[0].scatter(m, r, color=INK, s=12, zorder=3); axs[0].annotate(f"{r:.0f} kpc", (m, r), xytext=(4, -9), textcoords="offset points", fontsize=6.5)
        axs[1].scatter(m, v, color=RED, s=12, zorder=3); axs[1].annotate(f"{v:.0f} km/s", (m, v), xytext=(4, -9), textcoords="offset points", fontsize=6.5)
    axs[0].set_ylabel("halo radius $r_{200}$ (kpc)"); axs[1].set_ylabel("halo speed $V_{200}$ (km s$^{-1}$)")
    for ax in axs:
        ax.set_xlabel("halo mass $M_{200}$ ($M_\\odot$)")
    axs[0].set_title("both grow only as $M^{1/3}$", fontsize=7)
    savefig(fig, "halo_scaling", tight=False)


def knob_tree_galaxy():
    fig, ax = canvas(h=3.0)
    box(ax, 3.6, 5.3, 2.8, 0.8, "the six knobs (CMB)", fc="#e3ecf6", ec=BLUE, color=BLUE, weight="bold")
    items = [("halos:\n$M_{200}$, $c$", 0.2, "0"), ("stars per\nhalo", 2.2, "4-8"), ("feedback\nenergy", 4.2, "4+"),
             ("cores", 6.2, "2+"), ("contraction", 8.2, "1-2")]
    for t, x, k in items:
        box(ax, x, 2.8, 1.65, 1.2, t, fs=6.0)
        arrow(ax, 5.0, 5.25, x + 0.82, 4.05)
        ax.text(x + 0.82, 2.45, f"{k} knobs", ha="center", fontsize=6.4, color=RED)
    box(ax, 2.2, 0.4, 5.6, 1.0, "hydrodynamic simulations:\ndozens of subgrid efficiencies and thresholds", fs=6.2, fc="#fbeceb", ec=RED, color=RED)
    for x in (3.0, 5.0, 7.0):
        arrow(ax, x, 2.35, x, 1.45, color=GREY)
    savefig(fig, "knob_tree_galaxy")


# ---------------- Chapter 4 ----------------

def plate_recipe_card():
    fig, ax = canvas(h=3.6)
    ax.add_patch(FancyBboxPatch((0.4, 0.3), 9.2, 6.9, boxstyle="round,pad=0.02,rounding_size=0.2", fc="#fffdf5", ec="#c9b37e", lw=1.2))
    ax.text(5, 6.65, "RECIPE R11: HALOS TO MATCH A FORMULA", ha="center", fontsize=8.5, weight="bold", color=INK)
    ax.text(5, 6.2, "serves 171 galaxies  -  12 knobs  -  tuned to the law", ha="center", fontsize=6.4, color=GREY, style="italic")
    groups = [("stars per halo", ["norm", "$\\log M_1$", "$\\beta$", "$\\gamma$"]), ("feedback energy", ["$\\epsilon$", "$a_1$", "$a_2$", "$a_4$"]),
              ("core size", ["$\\eta_0$", "$a_3$"]), ("contraction", ["$f_0$", "$f_1$"])]
    bound = {"$\\gamma$", "$\\eta_0$", "$f_0$"}
    y = 5.3
    for g, ks in groups:
        ax.text(0.9, y, g, fontsize=7, weight="bold", color=INK, va="center")
        for i, k in enumerate(ks):
            col = RED if k in bound else INK
            dial(ax, 4.2 + 1.3 * i, y, 0.3, 1.0 if k in bound else 0.35 + 0.12 * i, nticks=7, color=col, label=k, fs=6.3)
        y -= 1.25
    ax.text(5, 0.6, "red: knobs that ran to the edge of their allowed range", ha="center", fontsize=6.4, color=RED)
    savefig(fig, "plate_recipe_card")


def dex_on_curve():
    R = np.linspace(0.3, 30, 300)
    vb2 = freeman_v2(R, 4e10, 3.0) + freeman_v2(R, 1e10, 6.0); gb = vb2 / R * UNIT_G
    v = np.sqrt(law(gb, A0) * R * KPC) / 1e3
    fig, ax = plt.subplots(figsize=(W, 2.4))
    for d, col, lab in ((0.0415, GREY, "$\\pm0.0415$ dex in $g$ (twelve knobs)"), (0.02, RED, "$\\pm0.02$ dex in $g$ (the target)")):
        f = 10 ** (d / 2)
        ax.fill_between(R, v / f, v * f, color=col, alpha=0.25, label=lab)
    ax.plot(R, v, color=INK, lw=1.2, label="the law")
    ax.set_xlabel("radius (kpc)"); ax.set_ylabel("rotation speed (km s$^{-1}$)"); ax.legend(frameon=False, fontsize=6.6, loc="lower right")
    ax.set_xlim(3, 30); ax.set_ylim(140, 215)
    ax.text(14, 205, "0.0415 dex in acceleration = about 5% in speed", fontsize=6.8)
    savefig(fig, "dex_on_curve", tight=False)


def train_test():
    rows = [("R11", 0.0405, 0.0445), ("R11b", 0.0275, 0.0326), ("R10", 0.0213, 0.0270), ("A16 (wide)", 0.0252, 0.0267), ("A25 (wide)", 0.0204, 0.0370)]
    fig, ax = plt.subplots(figsize=(W, 2.3))
    x = np.arange(len(rows))
    ax.bar(x - 0.18, [r[1] for r in rows], 0.34, color=BLUE, label="galaxies used for tuning")
    ax.bar(x + 0.18, [r[2] for r in rows], 0.34, color=RED, label="galaxies never seen")
    ax.axhline(0.02, color=GOLD, ls="--"); ax.text(4.45, 0.0205, "target", fontsize=6.5, color=GOLD)
    ax.set_xticks(x); ax.set_xticklabels([r[0] for r in rows]); ax.set_ylabel("distance to the law (dex)")
    ax.legend(frameon=False, fontsize=6.6, loc="upper right")
    savefig(fig, "train_test", tight=False)


def knob_staircase():
    steps = [(0, 0.1419, "untuned"), (4, 0.0715, "4"), (9, 0.0408, "9"), (14, 0.0275, "14"), (15, 0.0252, "15"), (28, 0.0222, "28"),
             (1026, 0.0152, "1026"), (3373, 0.0, "3373")]
    fig, ax = plt.subplots(figsize=(W, 2.6))
    xs = np.arange(len(steps))
    ys = [max(s[1], 0.0035) for s in steps]
    for i, (k, d, lab) in enumerate(steps):
        ax.add_patch(Rectangle((i - 0.45, 0.003), 0.9, ys[i] - 0.003, color=RED if d < 0.02 else INK, alpha=0.85))
        ax.text(i, ys[i] * 1.12, f"{d:.4f}" if d > 0 else "0", ha="center", fontsize=6.3)
    ax.axhline(0.02, color=GOLD, ls="--"); ax.text(-0.4, 0.0215, "frozen target", fontsize=6.4, color=GOLD)
    ax.set_yscale("log"); ax.set_ylim(0.003, 0.25); ax.set_xlim(-0.6, len(steps) - 0.4)
    ax.set_xticks(xs); ax.set_xticklabels([s[2] for s in steps], fontsize=6.2)
    ax.set_xlabel("knobs (1026: six per galaxy; 3373: the law renamed)"); ax.set_ylabel("distance to the law (dex)")
    savefig(fig, "knob_staircase", tight=False)


def needle_haystack():
    x = np.linspace(-0.8, 0.8, 600)
    fig, ax = plt.subplots(figsize=(W, 2.2))
    ax.plot(x, stats.norm.pdf(x, 0, 0.195), color=RED, label="the law: residuals spread 0.195 dex")
    ax.plot(x, stats.norm.pdf(x, 0.003, 0.195), color=INK, ls="--", label="a tuned recipe: shifted by 0.003 dex")
    ax.annotate("the whole difference\nbetween them", (0.0015, 2.06), xytext=(0.3, 1.6), fontsize=6.6, arrowprops=dict(arrowstyle="->"))
    ax.set_xlabel("residual against observed curves (dex)"); ax.set_yticks([]); ax.legend(frameon=False, fontsize=6.4, loc="upper left")
    savefig(fig, "needle_haystack", tight=False)


# ---------------- Chapter 5 ----------------

def plate_bill():
    fig, ax = canvas(h=4.2)
    xs = np.linspace(2.0, 8.0, 25)
    top = 8.0; bottom = 0.5
    zig = [(x, bottom + (0.15 if i % 2 else 0)) for i, x in enumerate(xs)]
    poly = [(2.0, top)] + [(8.0, top)] + zig[::-1]
    ax.add_patch(Polygon(poly, closed=True, fc="#fffdf5", ec="#c9b37e", lw=1.0))
    lines = [("THE EXACT DISH", ""), ("", ""), ("R9 per-galaxy knobs", "1026"), ("  concentration", "at bound"),
             ("  Einasto shape", "at bound"), ("R8 halo masses", "up to x16"), ("R10 galaxies inside", "0 of 171"),
             ("  both relations", ""), ("R5 shells", "3373 knobs"), ("  initial halos", "c x 0.32"), ("R12 the law as halo", "1 function"),
             ("", ""), ("SUBTOTAL", "a perfect match"), ("PLUS", "a coupling to"), ("", "dark energy"), ("", "LCDM lacks")]
    y = 7.55
    for l, r in lines:
        ax.text(2.35, y, l, fontsize=6.4, family="monospace", color=INK, weight="bold" if l in ("THE EXACT DISH", "SUBTOTAL", "PLUS") else "normal")
        ax.text(7.7, y, r, fontsize=6.4, family="monospace", color=RED if r and l in ("PLUS", "") else INK, ha="right")
        y -= 0.44
    savefig(fig, "plate_bill")


def shells_knobs():
    fig, ax = plt.subplots(figsize=(W, 2.8)); ax.set_aspect("equal"); ax.axis("off")
    for i, rr in enumerate(np.linspace(0.8, 4.4, 9)):
        ax.add_patch(Circle((0, 0), rr, fill=False, ec=GREY, lw=0.6))
        a = 0.6 + 0.55 * i
        dial(ax, rr * np.cos(a), rr * np.sin(a), 0.16, (i * 0.23) % 1, nticks=5, lw=0.5, color=RED)
    ax.scatter(np.random.default_rng(2).normal(0, 0.6, 300), np.random.default_rng(3).normal(0, 0.6, 300), s=1, color="#d4a017")
    ax.text(5.0, 2.0, "one knob per shell:\nthe dark mass is whatever\nmakes the law come out", fontsize=7, color=INK)
    ax.text(5.0, -1.4, "171 galaxies x ~20 shells\n= 3373 knobs for\n3373 data points", fontsize=7, color=RED)
    ax.set_xlim(-4.8, 9.5); ax.set_ylim(-4.8, 4.8)
    savefig(fig, "shells_knobs")


def jeans_check():
    R = np.logspace(-0.5, 2.3, 400)
    vb2 = freeman_v2(R, 4e10, 3.0) + freeman_v2(R, 1e10, 6.0); gb = vb2 / R * UNIT_G
    vl2 = law(gb, A0) * R * KPC / 1e6
    Mdm = R * (vl2 - vb2) / G_KPC; Mtot = R * vl2 / G_KPC
    rho = np.gradient(Mdm, R) / (4 * np.pi * R**2)
    integ = rho * G_KPC * Mtot / R**2
    sig = np.sqrt(np.array([np.trapz(integ[i:], R[i:]) for i in range(len(R))]) / rho)
    sel = R < 60
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.plot(R[sel], sig[sel], color=GREEN, lw=1.6, label="velocity dispersion the halo particles need")
    ax.plot(R[sel], np.sqrt(vl2[sel]), color=GREY, ls="--", label="circular speed, for scale")
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xscale("log"); ax.set_xlabel("radius (kpc)"); ax.set_ylabel("km s$^{-1}$"); ax.legend(frameon=False, fontsize=6.6, loc="lower right")
    ax.text(0.35, 175, "positive everywhere:\nthe isotropic Jeans check passes", fontsize=6.8, color=GREEN)
    savefig(fig, "jeans_check", tight=False)


# ---------------- Chapter 6 ----------------

def plate_pantry():
    fig, ax = canvas(h=3.4)
    for y in (0.8, 3.3):
        ax.add_patch(Rectangle((0.2, y - 0.15), 9.6, 0.15, color="#8b6b4a"))
    jars = ["stars per\nhalo", "feedback", "cores", "contrac-\ntion", "concen-\ntration", "self-\ninteraction", "fuzzy\nbosons",
            "warm\nparticles", "simulations", "$\\Lambda$'s\nvalue"]
    for i, j in enumerate(jars):
        x = 0.4 + (i % 5) * 1.9; y = 3.3 if i < 5 else 0.8
        ax.add_patch(FancyBboxPatch((x, y), 1.35, 1.75, boxstyle="round,pad=0.02,rounding_size=0.15", fc="#e8f1e4", ec=GREEN, lw=0.8))
        ax.add_patch(Rectangle((x + 0.05, y + 1.75), 1.25, 0.25, color="#b0b7c3"))
        ax.text(x + 0.67, y + 0.85, j, ha="center", va="center", fontsize=6.0, color=INK)
    ax.add_patch(FancyBboxPatch((3.95, 5.95), 2.1, 0.0001, boxstyle="square", fc="none", ec="none"))
    ax.text(5.0, 6.45, "the ingredient no knob supplies: $a_0=\\kappa c\\sqrt{G\\rho_{\\rm DE}}$  (out of stock)", ha="center", fontsize=7, color=RED,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=RED, ls="--"))
    savefig(fig, "plate_pantry")


def three_clocks():
    z = np.linspace(0, 2.5, 200)
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(z, (1 + z) ** 1.5, color=BLUE, label="$\\sqrt{\\rho_m}$: matter thins as $(1+z)^{3}$")
    ax.plot([0, 1, 1.5, 2.33], [1, 1.76, 2.35, 3.49], "^:", color=INK, ms=4, label="$H(z)$: the expansion rate")
    ax.plot(z, np.ones_like(z), color=RED, lw=2, label="$\\sqrt{\\rho_{\\rm DE}}$ for a cosmological constant")
    ax.set_xlabel("redshift $z$"); ax.set_ylabel("value relative to today"); ax.legend(frameon=False, fontsize=6.6, loc="upper left")
    ax.text(1.15, 0.25, "the law follows the red clock;\nhalos follow the other two", fontsize=6.8, color=RED)
    ax.set_ylim(0, 6)
    savefig(fig, "three_clocks", tight=False)


def slope_ruler():
    rows = [("target", 0.5, 0.5, RED), ("$\\Lambda$ coincidence", 0.5, 0.5, GREY), ("logotropic fluid (A36)", 0.5, 0.5, GREY),
            ("R10 + 5 hand terms", 0.496, 0.496, GREEN), ("R10, no hand terms", 0.283, 0.283, INK), ("R13, no hand terms", 0.245, 0.245, INK),
            ("14-knob recipe in other universes (A26)", 0.1874, 1.4526, INK), ("NFW central acceleration", 1.381, 3.561, INK),
            ("halos in evolving backgrounds (A29)", -0.1241, 0.0256, INK)]
    fig, ax = plt.subplots(figsize=(W, 2.7))
    ax.axvspan(0.45, 0.55, color="#f6d5d1")
    for i, (nm, lo, hi, col) in enumerate(rows):
        if hi > lo:
            ax.plot([lo, hi], [i, i], color=col, lw=4, alpha=0.7, solid_capstyle="butt")
        else:
            ax.scatter(lo, i, color=col, s=22, zorder=3)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=6.4); ax.invert_yaxis()
    ax.set_xlabel("slope of $\\ln a$ against $\\ln\\rho_{\\rm DE}$ (target 0.50)"); ax.set_xlim(-0.3, 3.7)
    savefig(fig, "slope_ruler", tight=False)


def kappa_three_cosmo():
    rows = [("R10,\nno hand terms", [0.459, 0.614, 0.735]), ("R10 +\nhand terms", [0.485, 0.506, 0.525]),
            ("R13, with\nhand terms", [0.483, 0.49, 0.51]), ("R12, law\ntyped in", [0.5, 0.5, 0.5])]
    cos = ["$\\Omega_\\Lambda$ 0.70, $H_0$ 67.4", "0.685, 73", "0.65, 73"]
    fig, ax = plt.subplots(figsize=(W, 2.4))
    x = np.arange(len(rows)); w = 0.25
    for j, (lab, col) in enumerate(zip(cos, [BLUE, INK, GOLD])):
        ax.bar(x + (j - 1) * w, [r[1][j] for r in rows], w, color=col, label=lab)
    ax.axhspan(0.475, 0.525, color="#f6d5d1", zorder=0); ax.axhline(0.5, color=RED, lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels([r[0] for r in rows], fontsize=6.4); ax.set_ylabel("$\\kappa_{\\rm eff}$")
    ax.set_ylim(0.3, 0.8); ax.legend(frameon=False, fontsize=6.2, title="test universe", title_fontsize=6.4, loc="upper right")
    savefig(fig, "kappa_three_cosmo", tight=False)


def dimension_blocks():
    fig, ax = canvas(h=2.6)
    box(ax, 0.2, 3.2, 4.4, 1.3, "the law's scale:\n$a_0=\\kappa\\,c\\,\\sqrt{G\\rho_{\\rm DE}}$", fc="#fbeceb", ec=RED, color=RED, fs=7.4)
    box(ax, 5.4, 3.2, 4.4, 1.3, "a halo's scale:\n$a_{\\rm halo}\\sim(GM)^{1/3}H^{4/3}$", fc="#eef0f4", ec=INK, color=INK, fs=7.4)
    ax.text(2.4, 2.5, "contains $c$\n$\\sqrt{G\\rho}$ is a rate, like $H$\n$c\\times$rate = acceleration", ha="center", va="top", fontsize=6.6, color=RED)
    ax.text(7.6, 2.5, "no $c$ anywhere\nset by mass and expansion\nchanges with $M$ and with time", ha="center", va="top", fontsize=6.6, color=INK)
    ax.text(5.0, 0.15, "near $10^{12}M_\\odot$ the two agree only because $c/V_{200}\\approx2000$ happens to be cancelled", ha="center", fontsize=6.4, color=GREY, style="italic")
    savefig(fig, "dimension_blocks")


# ---------------- Chapter 7 ----------------

def plate_dinner():
    fig, ax = plt.subplots(figsize=(W, 3.0)); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Circle((0, 0), 4.3, fc="#fafafa", ec=GREY, lw=1.2)); ax.add_patch(Circle((0, 0), 3.7, fc="white", ec=LIGHT, lw=0.8))
    items = [("law shape", "F"), ("SPARC curves", "P"), ("KiDS lensing", "F"), ("X-COP", "W"), ("dark energy\nslope", "W"),
             ("$a(z)$", "W"), ("Cassini", "P"), ("unseen data", "F"), ("knobs at\nbounds", "F")]
    n = len(items)
    for i, (lab, code) in enumerate(items):
        a0_, a1_ = 360 * i / n + 90, 360 * (i + 1) / n + 90
        col = {"P": GREEN, "F": RED, "W": "#8fbf6a"}[code]
        ax.add_patch(Wedge((0, 0), 3.6, a0_, a1_, fc=col, ec="white", lw=1.5, alpha=0.85))
        am = np.deg2rad((a0_ + a1_) / 2)
        ax.text(2.3 * np.cos(am), 2.3 * np.sin(am), lab, ha="center", va="center", fontsize=5.8, color="white", weight="bold")
    ax.add_patch(Circle((0, 0), 0.9, fc="white", ec=LIGHT)); ax.text(0, 0, "R13", ha="center", va="center", fontsize=8, weight="bold", color=INK)
    ax.text(5.0, 1.0, "green: pass\nlight green: pass that\nleans on hand terms\nor a bound\nred: fail", fontsize=6.6, va="center")
    ax.set_xlim(-4.5, 8.6); ax.set_ylim(-4.5, 4.5)
    savefig(fig, "plate_dinner")


def lensing_cartoon():
    rng = np.random.default_rng(8)
    fig, ax = plt.subplots(figsize=(W, 3.0)); ax.set_aspect("equal"); ax.axis("off")
    ax.set_facecolor("#10131c"); fig.patch.set_facecolor("white")
    ax.add_patch(Rectangle((-10, -10), 20, 20, color="#10131c"))
    for _ in range(330):
        x, y = rng.uniform(-9.5, 9.5, 2); r = math.hypot(x, y)
        if r < 1.2:
            continue
        phi = math.degrees(math.atan2(y, x)) + 90
        e = min(0.6, 2.2 / r) + rng.normal(0, 0.05)
        a = 0.28 * (1 + e); b = 0.28 * (1 - e)
        ax.add_patch(Ellipse((x, y), 2 * a, 2 * b, angle=phi + rng.normal(0, 8), fc="#9fc3ff", ec="none", alpha=0.8))
    ax.add_patch(Circle((0, 0), 0.8, color="#ffdf8a")); ax.add_patch(Circle((0, 0), 1.6, color="#ffdf8a", alpha=0.15))
    ax.text(0, -2.0, "foreground galaxy", ha="center", color="white", fontsize=6.4, bbox=dict(fc="#10131c", ec="none", pad=1.5), zorder=5)
    ax.text(-9.4, 8.6, "background galaxies are stretched\nat right angles to the line to the lens", color="white", fontsize=6.4,
            bbox=dict(fc="#10131c", ec="none", pad=2), zorder=5)
    ax.set_xlim(-10, 10); ax.set_ylim(-10, 10)
    savefig(fig, "lensing_cartoon")


def hydrostatic_cartoon():
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.2), gridspec_kw=dict(width_ratios=[1.1, 1]))
    ax = axs[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    yy, xx = np.mgrid[-3:3:200j, -3:3:200j]
    ax.imshow(np.exp(-np.hypot(xx, yy) / 0.9), extent=(-3, 3, -3, 3), cmap="Oranges", alpha=0.9, origin="lower")
    for a in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        ax.annotate("", xy=(2.4 * np.cos(a), 2.4 * np.sin(a)), xytext=(1.6 * np.cos(a), 1.6 * np.sin(a)), arrowprops=dict(arrowstyle="->", color=RED))
        ax.annotate("", xy=(1.0 * np.cos(a + 0.4), 1.0 * np.sin(a + 0.4)), xytext=(1.7 * np.cos(a + 0.4), 1.7 * np.sin(a + 0.4)), arrowprops=dict(arrowstyle="->", color=BLUE))
    ax.set_title("hot gas: pressure out (red), gravity in (blue)", fontsize=6.8)
    ax = axs[1]
    ax.bar(["the law\n(from visible\nbaryons)", "hydrostatic\nmass"], [1, 2.93], color=[RED, INK])
    ax.set_ylabel("mass (law = 1)"); ax.set_title("X-COP: about 3 times more needed", fontsize=6.8)
    savefig(fig, "hydrostatic_cartoon", tight=False)


def patchwork_treemap():
    fig, ax = plt.subplots(figsize=(W, 2.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 5)
    total = 1066.0
    parts = [("R9: six knobs per SPARC galaxy\n1026", 1026, INK), ("R13 global\n21", 21, BLUE), ("lensing bins\n14", 14, GOLD), ("hand\nterms 5", 5, RED)]
    x = 0.0
    for nm, k, col in parts:
        w = 10 * k / total
        ax.add_patch(Rectangle((x, 0), w, 5, fc=col, ec="white", lw=1.5, alpha=0.9))
        if w > 1.2:
            ax.text(x + w / 2, 2.5, nm, ha="center", va="center", color="white", fontsize=7.2)
        x += w
    ax.annotate("R13's 21 knobs, the 14 lensing knobs\nand the 5 hand terms are these thin slivers", (9.8, 4.6), xytext=(4.2, 5.6), fontsize=6.6,
                arrowprops=dict(arrowstyle="->"), annotation_clip=False)
    savefig(fig, "patchwork_treemap")


def particle_window():
    fig, ax = plt.subplots(figsize=(W, 1.9))
    ax.set_xscale("log"); ax.set_xlim(1, 1e3); ax.set_ylim(-1.1, 2.9)
    ax.fill_between([9.2, 13.7], 0.9, 1.5, color=BLUE, alpha=0.5); ax.text(11.2, 1.65, "boson that condenses in\nSPARC but not clusters", ha="center", fontsize=6.3, color=BLUE)
    ax.fill_between([56, 1e3], -0.3, 0.3, color=RED, alpha=0.25); ax.text(70, -0.75, "fermion: above 56 eV (typical galaxy)\nand 245 eV (most demanding)", fontsize=6.3, color=RED)
    ax.axvline(245, color=RED, lw=0.8, ls="--")
    ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_xlabel("particle mass (eV)")
    ax.text(1.2, 2.6, "and no single equation of state holds the halos up: pressure scatters 0.52 dex", fontsize=6.3, color=INK)
    savefig(fig, "particle_window", tight=False)


def log_axis_primer():
    x = np.linspace(0.01, 10, 400)
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.3))
    for ax, logs in ((axs[0], False), (axs[1], True)):
        ax.plot(x, x**2, color=INK, label="$y=x^2$ (slope 2)")
        ax.plot(x, x, color=GREY, ls="--", label="$y=x$ (slope 1)")
        ax.plot(x, np.sqrt(x), color=RED, label="$y=\\sqrt{x}$ (slope $\\frac{1}{2}$)")
        if logs:
            ax.set_xscale("log"); ax.set_yscale("log"); ax.set_title("log-log axes: each tick is $\\times10$;\npower laws become straight lines", fontsize=6.8)
        else:
            ax.set_title("ordinary axes", fontsize=6.8); ax.set_ylim(0, 12)
        ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    axs[0].legend(frameon=False, fontsize=6.3)
    savefig(fig, "log_axis_primer", tight=False)


if __name__ == "__main__":
    for f in [log_axis_primer, plate_roadmap, plate_amplifier, knob_anatomy, knob_species, chi2_dist, mackay_occam, forking_paths, freeze_timeline,
              bounds_pileup, plate_cmb_sky, cmb_anatomy, sound_horizon, vacuum_catastrophe, lcdm_panel_full, w0wa_plane, plate_galaxy,
              law_diversity, rar_anatomy, halo_scaling, knob_tree_galaxy, plate_recipe_card, dex_on_curve, train_test, knob_staircase,
              needle_haystack, plate_bill, shells_knobs, jeans_check, plate_pantry, three_clocks, slope_ruler, kappa_three_cosmo,
              dimension_blocks, plate_dinner, lensing_cartoon, hydrostatic_cartoon, patchwork_treemap, particle_window]:
        f(); print("ok", f.__name__)
