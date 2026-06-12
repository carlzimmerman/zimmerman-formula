#!/usr/bin/env python3
"""
make_figures.py — the whitepaper's evidence figures, generated from the repo's banked data only.
Conventions locked to the corpus: framework footing a0 = 9.36e-11 (Ud = 0.52, the agentCC gate),
canonical 1.2e-10 where shown. No mock data anywhere: fig1/fig3 from the SPARC rotmod files with
the agentCC loader; fig2 from the banked jackknife npz (the 181k-lens re-measurement); fig4 from
the byte-identical agentHH keystone table + the independent fit (agentHH_independent_fit.py);
fig5 from the banked closed forms (agentHH verdict / agentEE fingerprint); fig6 from the repo's
locked CPL sets (agentGG). Output: figures/*.pdf
"""
import os, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FIGD = os.path.join(HERE, "figures")
os.makedirs(FIGD, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.dpi": 150, "savefig.bbox": "tight"})

A0_FW, A0_CANON = 9.36e-11, 1.2e-10
UD, UB = 0.52, 1.4 * 0.52          # the locked SPARC conventions (agentCC gate: fw best-Ud 0.52)
KMS2 = 1e6                          # (km/s)^2 -> (m/s)^2 over kpc: handled explicitly below
KPC = 3.0857e19

# ---------- SPARC loader (agentCC conventions) ----------
def load_sparc():
    pts = []
    for f in sorted(glob.glob(os.path.join(ROOT, "real_research/data/sparc_data/*_rotmod.dat"))):
        for line in open(f):
            if line.startswith("#"): continue
            w = line.split()
            if len(w) < 8: continue
            r, vobs, evobs, vgas, vdisk, vbul = (float(w[0]), float(w[1]), float(w[2]),
                                                 float(w[3]), float(w[4]), float(w[6]))
            if r <= 0 or vobs <= 0 or evobs <= 0: continue
            vbar2 = vgas * abs(vgas) + UD * vdisk * abs(vdisk) + UB * vbul * abs(vbul)
            if vbar2 <= 0: continue
            gbar = vbar2 * KMS2 / (r * KPC)
            gobs = vobs**2 * KMS2 / (r * KPC)
            pts.append((gbar, gobs))
    return np.array(pts).T

# ---------- fig 1: the SPARC RAR ----------
def fig1():
    gbar, gobs = load_sparc()
    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    ax.loglog(gbar, gobs, ".", ms=1.5, alpha=0.25, color="C0", rasterized=True,
              label=f"SPARC ({len(gbar)} points, 175 galaxies)")
    x = np.logspace(-12.6, -8.4, 200)
    nu_fw = np.sqrt(1 + A0_FW / x)          # the framework baseline shape nu = sqrt(1+1/y)
    ax.loglog(x, x * nu_fw, "-", color="crimson", lw=1.8,
              label=r"$\nu=\sqrt{1+a_0/g_{\rm bar}}$,  $a_0=c^2\sqrt{\Lambda/32\pi}$")
    ax.loglog(x, x, "--", color="gray", lw=1, label="$g_{\\rm obs}=g_{\\rm bar}$ (Newton)")
    ax.axvline(A0_FW, color="crimson", ls=":", lw=0.8, alpha=0.7)
    ax.text(A0_FW * 1.15, 2.5e-12, "$a_0$", color="crimson")
    ax.set_xlabel(r"$g_{\rm bar}$ [m s$^{-2}$]"); ax.set_ylabel(r"$g_{\rm obs}$ [m s$^{-2}$]")
    ax.set_xlim(2e-13, 4e-9); ax.set_ylim(2e-13, 4e-9)
    ax.legend(loc="upper left", fontsize=7)
    fig.savefig(os.path.join(FIGD, "fig_rar_sparc.pdf")); fig.savefig(os.path.join(FIGD, "fig_rar_sparc.png"), dpi=160); plt.close(fig)
    print("fig1: SPARC RAR,", len(gbar), "points")

# ---------- fig 2: the lensing-RAR early/late split (own 181k-lens re-measurement) ----------
def fig2():
    d = np.load(os.path.join(ROOT, "real_research/data/lensing_rar/lr_esd_jackknife_analysis.npz"))
    gbar, esd, err = d["gbar_cen"], d["esd"], d["err"]
    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    ax.errorbar(gbar, esd[0], yerr=err[:15], fmt="o", ms=4, color="firebrick",
                label="early-type lenses", capsize=2)
    ax.errorbar(gbar * 1.06, esd[1], yerr=err[15:], fmt="s", ms=4, color="royalblue",
                label="late-type lenses", capsize=2)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"$g_{\rm bar}$ [m s$^{-2}$]")
    ax.set_ylabel(r"ESD  $\Delta\Sigma$  [$h\,M_\odot$ pc$^{-2}$]")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_title("the early/late lensing split — own re-measurement\n"
                 r"(181k lenses; 14/15 bins early above late; $6.8\sigma$ Hartlap-corrected)",
                 fontsize=8)
    fig.savefig(os.path.join(FIGD, "fig_lensing_split.pdf")); fig.savefig(os.path.join(FIGD, "fig_lensing_split.png"), dpi=160); plt.close(fig)
    print("fig2: lensing split from the banked jackknife npz")

# ---------- fig 3: the deep-MOND flattening window (agentCC) ----------
def fig3():
    gbar, gobs = load_sparc()
    m = gbar < 0.1 * A0_FW
    gb, go = gbar[m], gobs[m]
    bins = np.logspace(np.log10(gb.min()), np.log10(0.1 * A0_FW), 11)
    cen, med, lo, hi = [], [], [], []
    for i in range(len(bins) - 1):
        s = (gb >= bins[i]) & (gb < bins[i + 1])
        if s.sum() < 8: continue
        cen.append(np.sqrt(bins[i] * bins[i + 1]))
        q = np.percentile(go[s], [16, 50, 84])
        lo.append(q[0]); med.append(q[1]); hi.append(q[2])
    cen, med, lo, hi = map(np.array, (cen, med, lo, hi))
    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    ax.loglog(gb, go, ".", ms=2, alpha=0.2, color="gray", rasterized=True,
              label=f"SPARC deep points (N={m.sum()})")
    ax.errorbar(cen, med, yerr=[med - lo, hi - med], fmt="o", ms=4, color="k",
                label="binned median (16–84%)", zorder=5)
    x = np.logspace(np.log10(gb.min()) - 0.2, np.log10(0.12 * A0_FW), 200)
    ax.loglog(x, np.sqrt(x * A0_FW), "-", color="crimson", lw=1.6,
              label=r"deep-MOND $\sqrt{g_{\rm bar}a_0}$ (no floor)")
    for astar, c, lab in [(0.107 * A0_FW, "darkorange", r"floor at $a_\star=0.107a_0$ (95% excl.)"),
                          (0.05 * A0_FW, "seagreen", r"floor at $a_\star=0.05a_0$ (band ceiling)")]:
        gfloor = x * np.sqrt(1 + astar / x)   # nu with floor: response saturates below astar
        ax.loglog(x, np.maximum(np.sqrt(x * A0_FW), x * np.sqrt(astar / x) * 0 + np.sqrt(x * astar)
                                * np.sqrt(A0_FW / astar)) * 0 + np.where(
            x > astar, np.sqrt(x * A0_FW), np.sqrt(astar * A0_FW) * (x / astar)), "--",
            color=c, lw=1.4, label=lab)
    ax.set_xlabel(r"$g_{\rm bar}$ [m s$^{-2}$]"); ax.set_ylabel(r"$g_{\rm obs}$ [m s$^{-2}$]")
    ax.legend(loc="upper left", fontsize=6.5)
    ax.set_title("the flattening prediction: alive, untested in its window\n"
                 r"(data prefer $a_\star=0$; the allowed window lies below the deepest bins)",
                 fontsize=8)
    fig.savefig(os.path.join(FIGD, "fig_astar_window.pdf")); fig.savefig(os.path.join(FIGD, "fig_astar_window.png"), dpi=160); plt.close(fig)
    print("fig3: a-star window,", m.sum(), "deep points")

# ---------- fig 4: the keystone transcription + independent fit (agentHH) ----------
NU = np.array([4.096, 5.832, 8.000, 10.648, 13.824, 17.576, 21.952, 27.000,
               32.768, 39.304, 46.656, 54.872, 64.000, 74.088, 85.184, 97.336])
DD = np.array([+1.435222e-02, -7.748661e-03, -1.363932e-02, -8.348990e-03,
               -1.349531e-03, +2.470333e-03, +2.873668e-03, +1.598310e-03,
               +2.489429e-04, -4.582363e-04, -5.406332e-04, -3.145350e-04,
               -6.577796e-05, +7.273299e-05, +9.753810e-05, +6.179302e-05])

def _fit(s_fix, n=200):
    # the banked protocol + SEED (agentHH_independent_fit G2/G3, rng 20260612): q free;
    # s FREE for the class fit (s_fix=None) and frozen for the rivals — the banked comparison
    rng = np.random.default_rng(20260612)
    ay = np.abs(DD)
    env = np.array([max(ay[max(0, i-1):i+2].max(), 1e-12) for i in range(len(ay))])
    w = 1 / env
    def model(p, x):
        A, q, al, be, phi, sv = p
        return A * x**q * np.exp(-al * x**sv) * np.cos(be * x**sv + phi)
    best = None
    for _ in range(n):
        s0 = s_fix if s_fix is not None else rng.uniform(0.15, 0.8)
        q0 = rng.uniform(-3, 1)
        al0 = rng.uniform(0.3, 6.0)
        p0 = [rng.uniform(0.2, 5) * rng.choice([-1, 1]), q0,
              al0, al0 * rng.uniform(0.5, 4.0), rng.uniform(-np.pi, np.pi), s0]
        lo = [-50, -3, 0.1, 0.1, -2*np.pi, 0.05 if s_fix is None else s_fix - 1e-12]
        hi = [50, 1, 12, 40, 2*np.pi, 1.2 if s_fix is None else s_fix + 1e-12]
        try:
            r = least_squares(lambda p: (model(p, NU) - DD) * w, p0, bounds=(lo, hi),
                              max_nfev=20000)
        except Exception:
            continue
        c = float(np.sum(r.fun**2))
        if best is None or c < best[0]: best = (c, r.x, model)
    return best

def fig4():
    fits = {"free": _fit(None, n=200), 0.5: _fit(0.5, n=120), 1.0: _fit(1.0, n=120)}
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    pos, neg = DD > 0, DD < 0
    ax.semilogy(NU[pos], np.abs(DD[pos]), "^", color="k", ms=6, label=r"$\Delta\rho_c>0$ (banked scan)")
    ax.semilogy(NU[neg], np.abs(DD[neg]), "v", color="k", ms=6, mfc="white", label=r"$\Delta\rho_c<0$")
    x = np.linspace(4, 100, 600)
    for (k, st, c) in [("free", "-", "crimson"), (0.5, "--", "royalblue"),
                       (1.0, ":", "seagreen")]:
        cst, p, model = fits[k]
        lab = (rf"best fit, $s$ free: $s={p[5]:.2f}$ (the 1/3 class)" if k == "free" else
               rf"rival $s={k}$: {cst/fits['free'][0]:.0f}$\times$ worse")
        ax.semilogy(x, np.abs(model(p, x)) + 1e-12, st, color=c, lw=1.5, label=lab)
    ax.set_xlabel(r"$\nu$"); ax.set_ylabel(r"$|\Delta\rho_c(\nu)|$")
    ax.set_ylim(1e-6, 5e-2); ax.legend(fontsize=6.5, loc="upper right")
    ax.set_title("the keystone: the constructed profile's transcribed response\n"
                 "(16-point scan, byte-identical across two regenerations; independent fit)",
                 fontsize=8)
    fig.savefig(os.path.join(FIGD, "fig_keystone_fit.pdf")); fig.savefig(os.path.join(FIGD, "fig_keystone_fit.png"), dpi=160); plt.close(fig)
    print("fig4: keystone fit; free-s =", f"{fits['free'][1][5]:.4f},", "rival ratios",
          {k: f"{fits[k][0]/fits['free'][0]:.0f}x" for k in (0.5, 1.0)})

# ---------- fig 5: the constructed pump profile + the required fingerprint ----------
def fig5():
    ct = 2.13875
    w = np.logspace(-1, 4, 800)
    F = (w)**(-5/3) * np.exp(-ct * w**(1/3)) * np.cos(np.sqrt(3) * ct * w**(1/3) + np.pi/8 + np.pi/3)
    om = np.logspace(-0.5, 3, 800)
    D = om**(-1/3) * np.exp(-ct * om**(1/3)) * np.cos(np.sqrt(3) * ct * om**(1/3) + np.pi/8)
    fig, axs = plt.subplots(1, 2, figsize=(7.6, 3.0))
    axs[0].plot(w**(1/3), F * w**(5/3) * np.exp(ct * w**(1/3)), "-", color="navy", lw=1.2)
    axs[0].set_xlabel(r"$(c_\chi w)^{1/3}$")
    axs[0].set_ylabel(r"$F_{\rm req}\cdot w^{5/3}e^{+\tilde c w^{1/3}}$ (the locked oscillation)")
    axs[0].set_title("the constructed pump profile (closed form;\nGevrey-3 locked pair shown unwrapped)", fontsize=8)
    axs[1].plot(om**(1/3), np.sign(D) * np.abs(D)**0.5, "-", color="crimson", lw=1.2)
    axs[1].set_xlabel(r"$\omega^{1/3}$")
    axs[1].set_ylabel(r"sgn$(\Delta\tilde\rho_c)\,|\Delta\tilde\rho_c|^{1/2}$")
    axs[1].set_title(r"the required fingerprint $\sigma_{\rm req}$ class:"
                     "\n" r"$\omega^{-1/3}e^{-\tilde c\,\omega^{1/3}}\cos(\sqrt{3}\tilde c\,\omega^{1/3}+\tilde\varphi)$", fontsize=8)
    fig.savefig(os.path.join(FIGD, "fig_pump_profile.pdf")); fig.savefig(os.path.join(FIGD, "fig_pump_profile.png"), dpi=160); plt.close(fig)
    print("fig5: pump profile + fingerprint (banked closed forms, ct fw)")

# ---------- fig 6: the a0(z) branch fork + the REBELS-25 discriminator ----------
def fig6():
    OM = 0.315
    E = lambda z: np.sqrt(OM * (1 + z)**3 + (1 - OM))
    def rhoDE(z, w0, wa):
        a = 1 / (1 + z)
        return (1 + z)**(3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    z = np.linspace(0, 8, 400)
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    ax.plot(z, E(z), "-", color="seagreen", lw=1.6, label=r"rising $\propto E(z)$ (the rival)")
    ax.plot(z, np.ones_like(z), "-", color="gray", lw=1.2, label="constant")
    for (w0, wa, st) in [(-0.83, -0.75, "-"), (-0.752, -0.86, "--")]:
        ax.plot(z, np.sqrt(rhoDE(z, w0, wa)), st, color="crimson", lw=1.6,
                label=rf"declining $\sqrt{{\rho_{{\rm DE}}}}$ (CPL {w0},{wa})")
    ax.axvline(7.31, color="k", ls=":", lw=1)
    ax.text(7.31, 6.5, " REBELS-25\n (z=7.31)", fontsize=7, ha="right")
    ax.annotate(r"$V_{\rm flat}$ fork at fixed $M_{\rm bar}$:"
                "\ndeclining 86–143 km/s\nconstant 106–175\nrising 204–335",
                xy=(7.31, 3), xytext=(2.6, 4.5), fontsize=7,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_yscale("log"); ax.set_xlabel("z"); ax.set_ylabel(r"$a_0(z)/a_0(0)$")
    ax.legend(fontsize=7, loc="upper left")
    ax.set_title("the three a$_0$(z) branches and the registered\ndeep-[CII] discriminator (watch entry 12)", fontsize=8)
    fig.savefig(os.path.join(FIGD, "fig_a0z_fork.pdf")); fig.savefig(os.path.join(FIGD, "fig_a0z_fork.png"), dpi=160); plt.close(fig)
    print("fig6: a0(z) fork")

for f in (fig1, fig2, fig3, fig4, fig5, fig6):
    f()
print("ALL FIGURES WRITTEN to", FIGD)
