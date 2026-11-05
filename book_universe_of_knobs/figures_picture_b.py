"""Picture-book illustrations and explainer charts, chapter 8 to the appendix.
Run: python3 figures_picture_b.py
Illustrations are drawings, not data. Every number printed on a chart is quoted from the
fried chicken paper (v2.3) or PAPER67 (v1.2), or computed from the formula beside it."""
import math
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, Polygon, Arc
from figstyle import *
from figures_picture_a import canvas, box, arrow, savefig


def stars(ax, x, y, n, size=26):
    for i in range(4):
        ax.scatter(x + 0.32 * i, y, marker="*", s=size, color=GOLD if i < n else "white", edgecolors=GOLD, linewidths=0.6, zorder=4)


# ---------------- Chapter 8 ----------------

def plate_town_map():
    fig, ax = canvas(h=3.8)
    for y in (2.2, 5.6):
        ax.add_patch(Rectangle((0, y - 0.25), 10, 0.5, color=LIGHT))
    for x in (3.3, 6.7):
        ax.add_patch(Rectangle((x - 0.25, 0), 0.5, 8.6, color=LIGHT))
    shops = [("Feedback Grill\n(28 knobs)", 0.2, 6.2, 2), ("Simulation\nSteakhouse", 3.75, 6.2, 2), ("Superfluid Bar", 7.1, 6.2, 2),
             ("Emergent Eatery", 0.2, 3.0, 2), ("Dipole Deli\n(shape chosen)", 3.75, 3.0, 3), ("k-mouflage\nKitchen", 7.1, 3.0, 3),
             ("Self-Interaction\nDiner", 0.2, 0.2, 1), ("Fuzzy Boson\nCafe", 3.75, 0.2, 1), ("Cooling-Scale\nBistro", 7.1, 0.2, 3)]
    for name, x, y, n in shops:
        box(ax, x, y + 0.45, 2.7, 1.25, name, fs=6.3, fc="#fffdf5", ec="#c9b37e")
        stars(ax, x + 0.85, y + 0.2, n)
    ax.text(5.0, 8.35, "stars: how close to the law (3 = under the target). the fourth star, for the dark energy tie: nobody",
            ha="center", fontsize=6.3, color=INK, style="italic")
    savefig(fig, "plate_town_map")


def waffle_a28():
    fig, ax = plt.subplots(figsize=(W, 2.2)); ax.set_aspect("equal"); ax.axis("off")
    for i in range(171):
        r, c = divmod(i, 19)
        ax.add_patch(Rectangle((c, -r), 0.88, 0.88, color=RED if i < 154 else BLUE))
    ax.text(19.6, -1.5, "154 galaxies: cored halos\nfit better, even after\npaying the knob rent", fontsize=6.8, color=RED, va="center")
    ax.text(19.6, -6.5, "17 galaxies: the law\nfits better", fontsize=6.8, color=BLUE, va="center")
    ax.set_xlim(-0.2, 27); ax.set_ylim(-9.2, 1.0)
    savefig(fig, "waffle_a28")


def systematics_budget():
    fig, ax = plt.subplots(figsize=(W, 2.3))
    ax.barh(1, 0.101, left=0, color=GOLD, height=0.5); ax.text(0.105, 1, "non-circular motions, pressure, thickness: up to +0.101", va="center", fontsize=6.4)
    ax.barh(0, 0.157 + 0.174, left=-0.174, color=GREY, height=0.5); ax.text(0.162, 0, "mass-to-light and gas: $-0.174$ to $+0.157$", va="center", fontsize=6.4)
    marks = [(0.0, "$\\kappa=\\frac{1}{2}$ on $\\rho_{\\rm DE}$", RED), (math.log10(1.042e-10 / 9.3603e-11), "Milgrom $cH_0/2\\pi$", INK),
             (math.log10(1.0766e-10 / 9.3603e-11), "SPARC best fit", GREEN), (math.log10(1.1312e-10 / 9.3603e-11), "alternative footing", BLUE)]
    for i, (x, lab, col) in enumerate(marks):
        ax.axvline(x, color=col, lw=1, ls="-" if i == 0 else "--", label=f"{lab} ({x:+.3f})")
    ax.legend(frameon=False, fontsize=5.9, loc="upper right")
    ax.set_yticks([]); ax.set_ylim(-0.6, 2.6); ax.set_xlim(-0.25, 0.6)
    ax.set_xlabel("shift in the fitted $a_0$ (dex)"); ax.spines["left"].set_visible(False)
    save(fig, "systematics_budget")


def plateau_curve():
    k = [4, 9, 12, 14, 15, 28, 42]; d = [0.0715, 0.0408, 0.0415, 0.0275, 0.0252, 0.0222, 0.0213]
    lab = ["R1 tuned", "R7", "R11", "R11b", "A16", "A25", "R10"]
    fig, ax = plt.subplots(figsize=(W, 2.4))
    ax.plot(k, d, "o-", color=INK)
    for kk, dd, ll in zip(k, d, lab):
        ax.annotate(ll, (kk, dd), xytext=(4, 4), textcoords="offset points", fontsize=6.4)
    ax.axhline(0.02, color=RED, ls="--"); ax.text(4.2, 0.0185, "frozen target 0.02", color=RED, fontsize=6.5)
    ax.axhspan(0.0212, 0.0226, color=LIGHT); ax.text(5.5, 0.0228, "the floor: about 0.022", fontsize=6.6)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("global knobs in one recipe"); ax.set_ylabel("distance to the law (dex)")
    save(fig, "plateau_curve")


# ---------------- Chapter 9 ----------------

def plate_landscape():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    rng = np.random.default_rng(12)
    x = np.linspace(-5, 5, 160); X, Y = np.meshgrid(x, x)
    Z = 0.35 * np.sin(1.3 * X) * np.cos(1.1 * Y) + 0.2 * np.sin(2.7 * X + 1) * np.sin(2.3 * Y)
    for _ in range(40):
        cx, cy = rng.uniform(-4.5, 4.5, 2); w = rng.uniform(0.3, 0.9); dpt = rng.uniform(0.2, 0.9)
        Z -= dpt * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * w**2))
    fig = plt.figure(figsize=(W, 3.0)); ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="gist_earth", linewidth=0, antialiased=True, rstride=2, cstride=2, alpha=0.95)
    i, j = np.unravel_index(np.argmin(Z[40:120, 40:120]), (80, 80)); i += 40; j += 40
    ax.plot([X[i, j]] * 2, [Y[i, j]] * 2, [Z[i, j], Z[i, j] + 2.2], color=RED, lw=1.6, zorder=10)
    ax.scatter([X[i, j]], [Y[i, j]], [Z[i, j] + 2.2], color=RED, s=30, zorder=10)
    ax.text(X[i, j] + 0.2, Y[i, j], Z[i, j] + 2.45, "us?", color=RED, fontsize=9, weight="bold", zorder=10)
    ax.set_axis_off(); ax.view_init(elev=42, azim=-58); ax.set_box_aspect((1, 1, 0.42), zoom=1.45)
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig("figures/plate_landscape.pdf"); plt.close(fig)


def garden_hose():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    fig = plt.figure(figsize=(W, 2.2))
    ax = fig.add_subplot(121, projection="3d")
    u = np.linspace(0, 2 * np.pi, 40); x = np.linspace(0, 6, 40); U, Xx = np.meshgrid(u, x)
    ax.plot_surface(Xx, 0.6 * np.cos(U), 0.6 * np.sin(U), color=BLUE, alpha=0.55, linewidth=0)
    for xx in (1, 3, 5):
        ax.plot([xx] * 40, 0.6 * np.cos(u), 0.6 * np.sin(u), color=INK, lw=0.6)
    ax.set_axis_off(); ax.set_box_aspect((6, 1.4, 1.4)); ax.set_title("up close: a tiny curled-up direction", fontsize=7)
    ax2 = fig.add_subplot(122); ax2.axis("off"); ax2.set_xlim(0, 10); ax2.set_ylim(0, 4)
    ax2.plot([0.5, 9.5], [2, 2], color=BLUE, lw=1.2); ax2.set_title("from far away: just a line", fontsize=7)
    ax2.text(5, 1.0, "string theory curls up six such directions", ha="center", fontsize=6.6)
    fig.savefig("figures/garden_hose.pdf", bbox_inches="tight", pad_inches=0.03); plt.close(fig)


def counts_ladder():
    rows = [("reflexive polytopes\n(Kreuzer-Skarke)", math.log10(473800776)), ("flux vacua,\nthe famous estimate", 500), ("one F-theory\ngeometry", 272000)]
    fig, ax = plt.subplots(figsize=(W, 1.9))
    for i, (nm, v) in enumerate(rows):
        ax.barh(i, v, color=[GREY, GOLD, RED][i]); ax.text(v * 1.25, i, f"{v:,.0f} digits" if v > 10 else f"{v:.1f} digits", va="center", fontsize=6.8)
    ax.set_xscale("log"); ax.set_xlim(1, 3e6); ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows], fontsize=6.5); ax.invert_yaxis()
    ax.set_xlabel("how many digits it takes to write the count")
    save(fig, "counts_ladder")


def powers_of_ten_zoom():
    fig, axs = plt.subplots(1, 4, figsize=(W, 1.6))
    for k, ax in enumerate(axs):
        ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis("off")
        ax.plot([0.5, 9.5], [1.5, 1.5], color=INK, lw=1)
        for t in np.linspace(0.5, 9.5, 11):
            ax.plot([t, t], [1.3, 1.7], color=INK, lw=0.6)
        ax.add_patch(Rectangle((4.6, 1.2), 0.9, 0.6, fill=False, ec=RED, lw=1.2))
        ax.set_title(["the whole ruler", "zoom x10", "zoom x100", "zoom x1000"][k], fontsize=6.8)
        if k < 3:
            ax.annotate("", xy=(10.4, 1.5), xytext=(9.6, 1.5), arrowprops=dict(arrowstyle="->", color=RED), annotation_clip=False)
    fig.text(0.5, 0.04, "finding one part in $10^{120}$ takes 120 such zooms; three are shown", ha="center", fontsize=6.8, color=RED)
    fig.subplots_adjust(left=0.01, right=0.97, top=0.82, bottom=0.18, wspace=0.15)
    fig.savefig("figures/powers_of_ten_zoom.pdf"); plt.close(fig)


def weinberg_window():
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.0), gridspec_kw=dict(width_ratios=[2, 1]))
    ax = axs[0]
    ax.axvspan(-3, 2.5, color=GREEN, alpha=0.2); ax.scatter([0.34], [0], color=RED, zorder=3); ax.scatter([123], [0], color=INK)
    ax.text(123, 0.25, "naive Planck-scale\nestimate", ha="center", fontsize=6.4); ax.text(10, 0.25, "galaxies can form\nonly in the green sliver", fontsize=6.4, color=GREEN)
    ax.set_xlim(-10, 135); ax.set_ylim(-0.6, 0.8); ax.set_yticks([]); ax.axhline(0, color=GREY, lw=0.6)
    ax.set_xlabel("$\\log_{10}$(vacuum / matter density)")
    ax = axs[1]
    ax.axvspan(-3, 2.5, color=GREEN, alpha=0.2); ax.scatter([0.34], [0], color=RED, zorder=3); ax.axhline(0, color=GREY, lw=0.6)
    ax.text(0.34, 0.25, "measured", ha="center", fontsize=6.4, color=RED); ax.text(2.5, -0.4, "roughly where\nstructure stalls", ha="center", fontsize=6.0, color=GREEN)
    ax.set_xlim(-3, 4); ax.set_ylim(-0.6, 0.8); ax.set_yticks([]); ax.set_title("zoomed in", fontsize=6.8)
    save(fig, "weinberg_window")


# ---------------- Chapter 10 ----------------

def plate_one_dial():
    fig, ax = canvas(h=3.2)
    dial(ax, 2.2, 3.5, 1.5, 0.35, nticks=11, lw=1.6)
    ax.text(2.2, 1.35, "$\\kappa=\\frac{1}{2}$", ha="center", fontsize=12, color=RED)
    ax.text(2.2, 0.55, "set once, by galaxies today", ha="center", fontsize=6.6, color=GREY)
    outs = ["rotation curves", "Tully-Fisher, slope 4", "dwarf galaxies", "galaxy groups", "the shape of galaxy lensing"]
    for i, o in enumerate(outs):
        y = 6.0 - 1.1 * i
        arrow(ax, 3.9, 3.5, 5.6, y + 0.1, color=GREY)
        ax.text(5.75, y, o, fontsize=7, va="bottom", color=INK)
    ax.text(5.75, 0.25, "through $a_0=\\kappa\\,c\\sqrt{G\\rho_{\\rm DE}}$ and $g_{\\rm bar}=g^2/(g+a_0)$", fontsize=6.8, color=RED)
    savefig(fig, "plate_one_dial")


def law_family():
    R = np.linspace(0.1, 40, 400)
    fig, ax = plt.subplots(figsize=(W, 2.6))
    for M, col in ((1e8, GREY), (1e9, BLUE), (1e10, INK), (1e11, RED)):
        Rd = 0.5 * (M / 1e8) ** 0.3
        vb2 = freeman_v2(R, M, Rd); gb = vb2 / R * UNIT_G
        v = np.sqrt(law(gb, A0) * R * KPC) / 1e3
        vf = (G * M * MSUN * A0) ** 0.25 / 1e3
        ax.plot(R, v, color=col, label=f"$10^{{{int(math.log10(M))}}}M_\\odot$")
        ax.axhline(vf, color=col, ls=":", lw=0.7); ax.text(40.5, vf, f"{vf:.0f}", fontsize=6.3, color=col, va="center")
    ax.set_xlabel("radius (kpc)"); ax.set_ylabel("rotation speed (km s$^{-1}$)"); ax.legend(frameon=False, fontsize=6.5, title="baryonic mass", title_fontsize=6.5)
    ax.set_xlim(0, 44)
    save(fig, "law_family")


def attempts_grid():
    fig, ax = plt.subplots(figsize=(W, 2.0)); ax.set_aspect("equal"); ax.axis("off")
    for i in range(550):
        r, c = divmod(i, 50)
        ax.add_patch(Circle((c, -r), 0.36, color=GREY))
    ax.text(25, 1.6, "550 recorded attempts to derive $\\kappa=\\frac{1}{2}$. Successes: 0.", ha="center", fontsize=7.4, color=INK)
    ax.text(25, -12.4, "every route reduces to one missing piece: a length of exactly $c/\\sqrt{G\\rho}$ that no field equation supplies",
            ha="center", fontsize=6.4, color=RED)
    ax.set_xlim(-1, 50); ax.set_ylim(-13.2, 2.6)
    savefig(fig, "attempts_grid")


def footing_pie():
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.0), gridspec_kw=dict(width_ratios=[1, 1.4]))
    axs[0].pie([0.685, 0.315], colors=[RED, BLUE], startangle=90, labels=["dark energy\n0.685", "matter\n0.315"],
               textprops=dict(fontsize=6.4), wedgeprops=dict(linewidth=1, edgecolor="white"))
    axs[0].set_title("the critical density", fontsize=7)
    ax = axs[1]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.text(0, 4.6, "canonical: $\\kappa=\\frac{1}{2}$ on the red slice", fontsize=6.8, color=RED)
    ax.text(0, 3.9, "$a_0=9.36\\times10^{-11}$ m s$^{-2}$", fontsize=6.8, color=RED)
    ax.text(0, 2.7, "alternative: $\\kappa=\\frac{1}{2}$ on the whole pie", fontsize=6.8, color=INK)
    ax.text(0, 2.0, "$a_0=cH_0/Z=1.131\\times10^{-10}$ m s$^{-2}$", fontsize=6.8, color=INK)
    ax.text(0, 0.7, "ratio $1/\\sqrt{0.685}=1.21$: never averaged", fontsize=6.6, color=GREY)
    savefig(fig, "footing_pie")


# ---------------- Chapter 11 ----------------

def check(ax, x, y, s=0.25, col=GREEN):
    ax.plot([x - s, x - 0.3 * s, x + s], [y, y - 0.6 * s, y + 0.8 * s], color=col, lw=2, solid_capstyle="round")


def plate_wins_checklist():
    fig, ax = canvas(h=3.9)
    ax.add_patch(FancyBboxPatch((1.2, 0.2), 7.6, 8.1, boxstyle="round,pad=0.02,rounding_size=0.2", fc="#fffdf5", ec="#c9b37e", lw=1.2))
    ax.add_patch(FancyBboxPatch((4.1, 8.0), 1.8, 0.55, boxstyle="round,pad=0.02,rounding_size=0.1", fc=GREY, ec=INK))
    wins = ["SPARC scatter: 0.054 dex", "no tilt with rotation speed", "flat with surface brightness", "LITTLE THINGS dwarfs",
            "63 galaxy groups", "MeerKAT: same $a_0$", "lensing shape around galaxies", "Tully-Fisher slope 4, for free",
            "Solar System, with v3s's screen"]
    for i, w in enumerate(wins):
        y = 7.3 - 0.78 * i
        ax.add_patch(Rectangle((1.8, y - 0.2), 0.4, 0.4, fill=False, ec=INK, lw=0.8)); check(ax, 2.0, y, 0.22)
        ax.text(2.5, y, w, va="center", fontsize=7, color=INK)
    savefig(fig, "plate_wins_checklist")


def solar_accel():
    au = 1.496e11; GM = 1.327e20
    r = np.logspace(-1, 5, 400); g = GM / (r * au) ** 2
    fig, ax = plt.subplots(figsize=(W, 2.6))
    ax.loglog(r, g / A0, color=INK)
    for nm, rr in (("Mercury", 0.39), ("Earth", 1.0), ("Jupiter", 5.2), ("Saturn", 9.54), ("Neptune", 30.1)):
        gg = GM / (rr * au) ** 2 / A0; ax.scatter(rr, gg, color=BLUE, s=12, zorder=3)
        ax.annotate(nm, (rr, gg), xytext=(4, 3), textcoords="offset points", fontsize=6.4)
    ax.axhline(1, color=RED, ls="--"); rM = math.sqrt(GM / A0) / au
    ax.annotate(f"the Sun's pull falls to $a_0$\nat about {rM:,.0f} AU", (rM, 1), xytext=(25, 1e-3), fontsize=6.6, arrowprops=dict(arrowstyle="->"))
    ax.axvspan(2000, 30000, color=GOLD, alpha=0.2); ax.text(2200, 1e6, "wide\nbinaries", fontsize=6.4, color="#9a7b0a")
    ax.set_xlabel("distance from the Sun (AU)"); ax.set_ylabel("Sun's pull / $a_0$")
    save(fig, "solar_accel")


def screen_schematic():
    y = np.logspace(-2, 9, 400)
    extra = law(y, 1.0) - y
    screened = extra / (1 + (y / 1e3) ** 1.5)
    fig, ax = plt.subplots(figsize=(W, 2.4))
    ax.loglog(y, extra, color=RED, label="unscreened: the extra pull tends to $a_0$")
    ax.loglog(y, screened, color=GREEN, label="screened: switched off in strong fields")
    ax.axvspan(7e5, 3e8, color=BLUE, alpha=0.1); ax.text(1.2e6, 3e-6, "the planets", fontsize=6.6, color=BLUE)
    ax.set_xlabel("$g_{\\rm bar}/a_0$"); ax.set_ylabel("extra pull / $a_0$"); ax.set_ylim(1e-8, 30)
    ax.legend(frameon=False, fontsize=6.4, loc="lower left"); ax.set_title("schematic of what a screen does (not v3s's own equations)", fontsize=6.8)
    save(fig, "screen_schematic")


def gw_speed():
    fig, ax = plt.subplots(figsize=(W, 1.5))
    ax.set_xscale("log"); ax.set_xlim(1e-35, 1e-10)
    ax.axvspan(1e-35, 1e-15, color=GREEN, alpha=0.15); ax.text(1e-24, 0.55, "allowed by the 2017 neutron-star merger: $|\\Delta v/c|\\lesssim10^{-15}$", ha="center", fontsize=6.4, color=GREEN)
    ax.scatter([5.1e-32], [0.2], color=RED, zorder=3); ax.text(5.1e-32, -0.2, "v3s: $\\leq5.1\\times10^{-32}$", ha="center", fontsize=6.6, color=RED)
    ax.set_ylim(-0.5, 0.9); ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_xlabel("difference between gravity's speed and light's, $|\\Delta v/c|$")
    save(fig, "gw_speed")


# ---------------- Chapter 12 ----------------

def plate_wall():
    fig, ax = canvas(h=3.6)
    fails = {(0, 0): "clusters: x2.9", (0, 2): "cluster shear x1.9", (1, 1): "CMB lensing shape", (1, 2): "Bullet Cluster",
             (2, 0): "IC 1613", (2, 2): "ultra-faint dwarfs", (3, 1): "Milky Way $K_z$", (3, 2): "stellar masses x2",
             (4, 0): "DiskMass discs", (4, 2): "Cassini, unscreened", (5, 1): "the matter term", (5, 2): "MUSE-DARK rise"}
    bw, bh = 3.2, 1.2
    for row in range(6):
        off = 0 if row % 2 == 0 else -bw / 2
        for col in range(5):
            x = off + col * bw; y = row * bh
            if x + bw < 0.05 or x > 9.95:
                continue
            lab = fails.get((row, col))
            ax.add_patch(Rectangle((max(x, 0), y), min(bw, 10 - max(x, 0)) - 0.08, bh - 0.08, fc=RED if lab else "#b9a89a", ec="white", alpha=0.9 if lab else 0.6))
            if lab:
                ax.text(x + bw / 2 - 0.04, y + bh / 2, lab, ha="center", va="center", fontsize=6.0, color="white", weight="bold", zorder=6)
    ax.set_ylim(0, 7.3)
    savefig(fig, "plate_wall")


def cluster_deficit():
    fig, ax = plt.subplots(figsize=(W, 2.0))
    ax.bar(["0.2 to 0.5 $R_{500}$", "0.5 to 1 $R_{500}$"], [8, 5], color=[RED, INK], width=0.5)
    ax.axhline(1, color=GREY, ls="--"); ax.text(1.32, 1.2, "1 = as much as the gas", fontsize=6.4, color=GREY)
    ax.set_ylabel("missing mass / gas mass"); ax.set_title("what the law leaves unexplained in clusters, as a description", fontsize=7)
    save(fig, "cluster_deficit")


def collision_graph():
    names = ["1 tight galaxies", "2 flat with SB", "3 $\\Upsilon$ at every speed", "4 little contraction", "5 dwarfs", "6 IC 1613",
             "7 Milky Way", "8 isolated lenses", "9 cluster cores", "10 outer shear", "11 dust in the CMB", "12 an action"]
    fig, ax = plt.subplots(figsize=(W, 3.2)); ax.set_aspect("equal"); ax.axis("off")
    ang = np.linspace(90, 90 - 360, 13)[:-1]; pos = {i + 1: (3 * np.cos(np.deg2rad(a)), 3 * np.sin(np.deg2rad(a))) for i, a in enumerate(ang)}
    for a, b in ((4, 11), (1, 10), (2, 10), (3, 10), (7, 8)):
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=RED, lw=1.6, alpha=0.8)
    for i, nm in enumerate(names):
        x, y = pos[i + 1]; ax.add_patch(Circle((x, y), 0.32, color=INK))
        ax.text(x, y, str(i + 1), color="white", ha="center", va="center", fontsize=7)
        ha = "left" if x > 0.3 else ("right" if x < -0.3 else "center")
        ax.text(x * 1.17 + (0.25 if x > 0.3 else -0.25 if x < -0.3 else 0), y * 1.17, nm[nm.index(" ") + 1:], ha=ha, va="center", fontsize=6.0)
    ax.text(0, 0, "red lines:\nrequirements that\npull against\neach other", ha="center", va="center", fontsize=6.6, color=RED)
    ax.set_xlim(-6.2, 6.2); ax.set_ylim(-4.2, 4.2)
    savefig(fig, "collision_graph")


def outer_shear_slope():
    fig, ax = plt.subplots(figsize=(W, 1.7))
    ax.errorbar([0.90], [0], xerr=[0.21], fmt="o", color=INK, capsize=3); ax.text(0.90, 0.3, "measured: $0.90\\pm0.21$", ha="center", fontsize=6.6)
    ax.scatter([0.47], [0], color=RED, s=30, zorder=3); ax.text(0.47, -0.45, "the law: 0.47", ha="center", fontsize=6.6, color=RED)
    ax.scatter([0.84], [0], color=BLUE, marker="s", s=22, zorder=3); ax.text(0.84, -0.45, "Newton: 0.84", ha="center", fontsize=6.6, color=BLUE)
    ax.set_yticks([]); ax.set_ylim(-0.8, 0.7); ax.set_xlim(0.3, 1.3); ax.spines["left"].set_visible(False)
    ax.set_xlabel("how outer shear grows with gas mass: slope $s$ in $\\Delta\\Sigma\\propto M_{\\rm gas}^{s}$")
    save(fig, "outer_shear_slope")


def k_window():
    fig, ax = plt.subplots(figsize=(W, 2.2))
    bars = [("G-OUT-all needs $k\\leq7.2$", 0, 7.2, INK), ("G-OUT-M3 needs $k\\geq8.8$", 8.8, 20, INK), ("G-MID-T3 needs $k\\geq12.9$", 12.9, 20, INK),
            ("14 of 15 keys: $12.87\\leq k\\leq15.09$", 12.87, 15.09, GOLD)]
    for i, (nm, lo, hi, col) in enumerate(bars):
        ax.barh(i, hi - lo, left=lo, color=col, alpha=0.6, height=0.55)
        ax.text(7.5 if i == 0 else 0.2, i, nm, ha="left", va="center", fontsize=6.3)
    for j, (x, nm) in enumerate(((13.29, "fit on 4 X-COP"), (math.pi**2, "$\\pi^2$"), (8.38, "masses 0.12 dex high"))):
        ax.axvline(x, color=RED, lw=0.8, ls="--"); ax.text(x, 3.55 + 0.32 * (j % 2), nm, ha="center", fontsize=5.8, color=RED)
    ax.set_yticks([]); ax.set_xlim(0, 20); ax.set_ylim(-0.6, 4.0); ax.invert_yaxis()
    ax.set_xlabel("the gas-term knob $k$: no setting meets all three needs")
    save(fig, "k_window")


def upsilon_compare():
    fig, ax = plt.subplots(figsize=(W, 1.9))
    bins = ["60-100 km/s", "100-150 km/s"]
    ax.scatter([0.62, 0.65], [1, 0], color=RED, s=30, zorder=3, label="what the law needs")
    ax.scatter([0.277, 0.304], [1, 0], color=BLUE, s=30, marker="s", zorder=3, label="stellar masses from GSWLC")
    for y, a, b, z in ((1, 0.277, 0.62, "+3.4"), (0, 0.304, 0.65, "+5.6")):
        ax.plot([a, b], [y, y], color=GREY, lw=0.8); ax.text((a + b) / 2, y + 0.18, f"$Z={z}$", ha="center", fontsize=6.4)
    ax.set_yticks([1, 0]); ax.set_yticklabels(bins); ax.set_xlim(0.15, 0.8); ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel("stellar mass-to-light ratio $\\Upsilon$"); ax.legend(frameon=False, fontsize=6.4, loc="upper left", ncol=2)
    save(fig, "upsilon_compare")


# ---------------- Chapter 13 ----------------

def plate_locked_knob():
    fig, ax = canvas(h=3.2)
    dial(ax, 3.0, 3.6, 1.5, 0.5, nticks=11, lw=1.6)
    ax.add_patch(Arc((3.0, 4.15), 1.2, 1.4, theta1=0, theta2=180, color=GOLD, lw=4, zorder=6))
    ax.add_patch(FancyBboxPatch((2.25, 2.85), 1.5, 1.3, boxstyle="round,pad=0.02,rounding_size=0.12", fc=GOLD, ec="#9a7b0a", zorder=6))
    ax.add_patch(Circle((3.0, 3.55), 0.14, color="#5a4a10", zorder=7)); ax.add_patch(Rectangle((2.95, 3.1), 0.1, 0.4, color="#5a4a10", zorder=7))
    ax.add_patch(Circle((7.3, 3.6), 0.45, fill=False, ec=INK, lw=2)); ax.add_patch(Rectangle((5.5, 3.5), 1.4, 0.2, color=INK))
    ax.add_patch(Rectangle((5.6, 3.25), 0.15, 0.25, color=INK)); ax.add_patch(Rectangle((5.9, 3.25), 0.15, 0.25, color=INK))
    ax.text(6.6, 1.9, "the key: $\\rho_{\\rm DE}(z)$,\nmeasured by baryon acoustic\noscillations and supernovae", ha="center", fontsize=6.8, color=INK)
    ax.text(5.0, 6.4, "$\\frac{a_0(z)}{a_0(0)}=\\sqrt{\\frac{\\rho_{\\rm DE}(z)}{\\rho_{\\rm DE}(0)}}$:  $\\kappa$ cancels, no galaxy knob left",
            ha="center", fontsize=8, color=RED)
    ax.text(3.0, 1.05, "nobody can turn this one", ha="center", fontsize=6.8, color=GREY, style="italic")
    savefig(fig, "plate_locked_knob")


def mass_route():
    rows = [("stellar masses fitted freely", 0.570, 0.094, RED), ("photometric + molecular gas", -0.115, 0.489, BLUE),
            ("photometric only", 0.036, 0.138, BLUE)]
    fig, ax = plt.subplots(figsize=(W, 1.9))
    for i, (nm, v, e, col) in enumerate(rows):
        ax.errorbar(v, i, xerr=e, fmt="o", color=col, capsize=3)
    ax.axvline(0, color=GREEN, lw=1); ax.text(0.01, 2.55, "no change", fontsize=6.4, color=GREEN)
    ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows], fontsize=6.6); ax.invert_yaxis(); ax.set_ylim(2.8, -0.6)
    ax.set_xlabel("change in $\\log a_0$ from $z=0.52$ to 1.20 (CFG262)")
    save(fig, "mass_route")


def common_mode_cartoon():
    rng = np.random.default_rng(4)
    fig, axs = plt.subplots(1, 2, figsize=(W, 2.2), sharey=True)
    for ax, bias, title in ((axs[0], 0.0, "errors only scatter: averaging works"), (axs[1], 0.3, "a shared error: averaging can't help")):
        vals = rng.normal(bias, 0.14, 60)
        ax.hist(vals, bins=np.linspace(-0.5, 0.8, 27), color=GREY, alpha=0.7)
        ax.axvline(0, color=GREEN, lw=1.4, label="the truth"); ax.axvline(vals.mean(), color=RED, lw=1.4, ls="--", label="average of 60")
        ax.set_title(title, fontsize=6.8); ax.set_xlabel("measured offset (dex)")
    axs[0].legend(frameon=False, fontsize=6.2); axs[0].set_ylabel("galaxies")
    save(fig, "common_mode_cartoon")


def mock_decider():
    rng = np.random.default_rng(21)
    v = np.array([140, 165, 185, 205, 230.0])
    a_law = A0 * 0.91; a_riv = A0 * 3.49
    Mlaw = lambda vv, a: (vv * 1e3) ** 4 / (G * a) / MSUN
    cm = rng.normal(0, 0.05)
    obs = np.log10(Mlaw(v, a_law)) + cm + rng.normal(0, 0.14, v.size)
    vv = np.linspace(120, 260, 50)
    fig, ax = plt.subplots(figsize=(W, 2.4))
    ax.plot(vv, np.log10(Mlaw(vv, a_law)), color=RED, label="the law's prediction at $z\\approx2.3$")
    ax.plot(vv, np.log10(Mlaw(vv, a_riv)), color=BLUE, ls="--", label="the rival $a_0\\propto H(z)$")
    ax.errorbar(v, obs, yerr=0.14, fmt="o", color=INK, capsize=2, label="five mock galaxies")
    ax.set_xlabel("rotation speed (km s$^{-1}$)"); ax.set_ylabel("$\\log_{10}M_b/M_\\odot$")
    ax.legend(frameon=False, fontsize=6.4, loc="upper left")
    ax.set_title("MOCK DATA: what a deciding measurement could look like", fontsize=6.8, color=GREY)
    save(fig, "mock_decider")


# ---------------- Chapter 14 ----------------

def six_questions():
    qs = ["What was frozen\nbefore the data?", "How many numbers\ncame from the data?", "Any knobs at\ntheir bounds?",
          "How does it do on\ndata it never saw?", "Anything written\nin by hand?", "What does it predict\nthat it can't adjust?"]
    fig, ax = canvas(h=3.0)
    for i, q in enumerate(qs):
        r, c = divmod(i, 3); x = 0.2 + c * 3.3; y = 3.6 - r * 3.0
        box(ax, x, y, 3.0, 2.4, "", fc="#f6f6f2", ec=GREY)
        ax.add_patch(Circle((x + 0.5, y + 1.85), 0.33, color=RED)); ax.text(x + 0.5, y + 1.85, str(i + 1), color="white", ha="center", va="center", fontsize=8, weight="bold")
        ax.text(x + 1.5, y + 0.9, q, ha="center", va="center", fontsize=6.8, color=INK)
    savefig(fig, "six_questions")


# ---------------- Appendix ----------------

def formula_map():
    fig, ax = canvas(h=3.6)
    box(ax, 0.1, 6.3, 3.0, 1.3, "expansion surveys\n$\\rightarrow\\rho_{\\rm DE}(z)$", fc="#e3ecf6", ec=BLUE, color=BLUE, fs=6.8)
    box(ax, 6.9, 6.3, 3.0, 1.3, "galaxies today\n$\\rightarrow\\kappa=\\frac{1}{2}$ (fitted)", fc="#fbeceb", ec=RED, color=RED, fs=6.8)
    box(ax, 3.3, 4.4, 3.4, 1.3, "$a_0(z)=\\kappa c\\sqrt{G\\rho_{\\rm DE}(z)}$", fc="#fffdf5", ec=GOLD, color=INK, fs=7.4)
    arrow(ax, 3.1, 6.6, 4.2, 5.75); arrow(ax, 6.9, 6.6, 5.8, 5.75)
    outs = [("the law\n$g_{\\rm bar}=g^2/(g+a_0)$", 0.1), ("Tully-Fisher\n$v_f^4=GM_ba_0$", 2.6), ("lensing\n$\\Delta\\Sigma\\to\\sqrt{GMa_0}/4GR$", 5.1),
            ("the unturnable test\n$a_0(z)/a_0(0)$", 7.6)]
    for t, x in outs:
        box(ax, x, 1.4, 2.3, 1.6, t, fs=5.7, ec=GREY)
        arrow(ax, 5.0, 4.35, x + 1.15, 3.05, color=GREY)
    ax.text(5.0, 0.55, "every formula in the book hangs off one knob and one measured density", ha="center", fontsize=6.6, color=GREY, style="italic")
    savefig(fig, "formula_map")


if __name__ == "__main__":
    for f in [plate_town_map, waffle_a28, systematics_budget, plateau_curve, plate_landscape, garden_hose, counts_ladder,
              powers_of_ten_zoom, weinberg_window, plate_one_dial, law_family, attempts_grid, footing_pie, plate_wins_checklist,
              solar_accel, screen_schematic, gw_speed, plate_wall, cluster_deficit, collision_graph, outer_shear_slope, k_window,
              upsilon_compare, plate_locked_knob, mass_route, common_mode_cartoon, mock_decider, six_questions, formula_map]:
        f(); print("ok", f.__name__)
