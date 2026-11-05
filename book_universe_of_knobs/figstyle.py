"""Shared style and helpers for the book's figures."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

plt.rcParams.update({
    "font.family": "serif", "font.size": 8.5, "axes.titlesize": 8.5,
    "axes.labelsize": 8.5, "legend.fontsize": 7.2, "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5, "axes.spines.top": False, "axes.spines.right": False,
})
INK = "#1f2a44"; RED = "#c0392b"; GOLD = "#d4a017"; BLUE = "#2e6da4"
GREY = "#8a8f98"; GREEN = "#2e8b57"; LIGHT = "#e6e8ec"; PURPLE = "#7d3c98"
W = 4.4  # text width in inches

# physical constants (SI) and convenient units
G = 6.674e-11; C = 2.99792458e8; KPC = 3.0857e19; MSUN = 1.989e30
A0 = 9.3603e-11; A0_ALT = 1.1312e-10
G_KPC = 4.30091e-6          # kpc (km/s)^2 / Msun
UNIT_G = 1e6 / KPC          # (km/s)^2/kpc -> m/s^2
H0_KPC = 0.0674             # km/s/kpc for H0 = 67.4 km/s/Mpc


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"figures/{name}.pdf")
    plt.close(fig)


def law(gb, a=1.0):
    """Observed acceleration from the law g_N = g^2/(g+a)."""
    return gb / 2 + np.sqrt(gb**2 / 4 + gb * a)


def m_nfw(x):
    return np.log1p(x) - x / (1 + x)


def tiles(ax, matrix, rows, cols, notes=None, fs=7):
    """Pass/fail tile chart. Codes: P pass, F fail, U undecided, W weak pass, - not graded."""
    colours = {"P": GREEN, "F": RED, "U": GOLD, "W": "#8fbf6a", "-": LIGHT}
    words = {"P": "pass", "F": "fail", "U": "undec.", "W": "weak", "-": "--"}
    for i, row in enumerate(matrix):
        for j, code in enumerate(row):
            key = code[0] if code else "-"
            ax.add_patch(Rectangle((j, -i - 1), 0.94, 0.9, color=colours.get(key, LIGHT), lw=0))
            label = words.get(key, code)
            if len(code) > 1:
                label += code[1:]
            ax.text(j + 0.47, -i - 0.55, label, ha="center", va="center", fontsize=fs,
                    color="white" if key in "PFW" else INK)
    ax.set_xlim(0, len(cols)); ax.set_ylim(-len(rows), 0.05)
    ax.set_yticks([-i - 0.55 for i in range(len(rows))]); ax.set_yticklabels(rows)
    ax.set_xticks([j + 0.47 for j in range(len(cols))]); ax.set_xticklabels(cols)
    ax.xaxis.tick_top(); ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)


def dial(ax, x, y, r, angle_frac, nticks=11, color=INK, face="white", lw=1.0, label=None, fs=6.5):
    """A knob: a circle, tick marks over a 270-degree sweep, and a pointer."""
    ax.add_patch(Circle((x, y), r, facecolor=face, edgecolor=color, lw=lw, zorder=2))
    th0, th1 = np.deg2rad(225), np.deg2rad(-45)
    for t in np.linspace(th0, th1, nticks):
        ax.plot([x + 1.08 * r * np.cos(t), x + 1.25 * r * np.cos(t)],
                [y + 1.08 * r * np.sin(t), y + 1.25 * r * np.sin(t)], color=color,
                lw=0.35 if nticks > 60 else 0.6, zorder=1)
    t = th0 + (th1 - th0) * angle_frac
    ax.plot([x, x + 0.8 * r * np.cos(t)], [y, y + 0.8 * r * np.sin(t)], color=RED, lw=1.4, zorder=3)
    ax.add_patch(Circle((x, y), 0.12 * r, color=color, zorder=4))
    if label:
        ax.text(x, y - 1.55 * r, label, ha="center", va="top", fontsize=fs)


def freeman_v2(R, M, Rd):
    """Circular speed squared (km/s)^2 of a thin exponential disc (Freeman 1970)."""
    from scipy.special import i0, i1, k0, k1
    y = R / (2 * Rd)
    sigma0 = M / (2 * np.pi * Rd**2)
    return 4 * np.pi * G_KPC * sigma0 * Rd * y**2 * (i0(y) * k0(y) - i1(y) * k1(y))


def nfw_params(M200, c, H=H0_KPC):
    r200 = (G_KPC * M200 / (100 * H**2)) ** (1 / 3)
    return r200, r200 / c


def nfw_mass(r, M200, c):
    r200, rs = nfw_params(M200, c)
    return M200 * m_nfw(r / rs) / m_nfw(c)
