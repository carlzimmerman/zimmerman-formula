#!/usr/bin/env python3
"""
Figures for the EFE-vs-z forecast paper (EFE_vs_z_Forecast_2026.tex).
Generates three vector PDFs in real_research/figures/ and prints the key numbers.
Self-contained: re-implements the MOND EFE so the charts match the forecast script.
Run: python efe_forecast_figures.py   (needs numpy, matplotlib)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OM, OL = 0.315, 0.685
E = lambda z: np.sqrt(OM*(1+z)**3 + OL)
A0 = 1.2e-10
mu = lambda x: x/(1.0+x)                          # simple interpolation function

OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "figures"))
os.makedirs(OUT, exist_ok=True)


def g_obs(g_bar, g_ext, a0):
    """Solve mu((g_obs+g_ext)/a0) g_obs = g_bar by log-bisection (SI)."""
    f = lambda go: mu((go+g_ext)/a0)*go - g_bar
    lo, hi = 1e-18, 1e-6
    for _ in range(200):
        mid = np.sqrt(lo*hi)
        if f(mid) < 0: lo = mid
        else: hi = mid
    return np.sqrt(lo*hi)


def offset_dex(g_bar0, g_ext0, z):
    """log10(boost_embedded / boost_isolated); 0 = no EFE, <0 = suppressed."""
    a0z = A0*E(z); gb, ge = g_bar0*A0, g_ext0*A0
    return np.log10((g_obs(gb, ge, a0z)/gb)/(g_obs(gb, 0.0, a0z)/gb))


# ----------------------------------------------------------------------------
def fig1_prediction():
    zz = np.linspace(0, 6, 240)
    zd  = np.array([0.00, 0.05, 0.90])
    a0d = np.array([1.20, 1.69, 2.38]); a0e = np.array([0.26, 0.13, 0.11])
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].plot(zz, E(zz), "b-", lw=2.2, label=r"prediction $a_0(z)/a_0(0)=E(z)$")
    ax[0].axhline(1, color="0.5", ls=":", lw=1.5, label=r"constant $a_0$ (no evolution)")
    ax[0].errorbar(zd, a0d/1.20, yerr=a0e/1.20, fmt="o", color="crimson", ms=7,
                   capsize=3, lw=1.5, label="current data (heterogeneous)")
    ax[0].set_xlabel("redshift $z$"); ax[0].set_ylabel(r"$a_0(z)\,/\,a_0(0)$")
    ax[0].set_title(r"(a) the evolving scale $a_0(z)=a_0(0)\,E(z)$")
    ax[0].set_xlim(0, 6); ax[0].set_ylim(0.7, 11); ax[0].legend(fontsize=8.5, loc="upper left")
    ax[0].text(0.55, 3.4, "current fit: a ~2$\\sigma$ hint,\nsingle-point-driven,\n$\\Lambda$CDM-degenerate",
               fontsize=8, color="0.35")

    ax[1].plot(zz, 1.0/E(zz), "g-", lw=2.2)
    ax[1].axhline(1, color="0.5", ls=":", lw=1.5)
    ax[1].set_xlabel("redshift $z$")
    ax[1].set_ylabel(r"$\eta(z)/\eta_0 = 1/E(z)$  (EFE strength)")
    ax[1].set_title(r"(b) the External Field Effect weakens with $z$")
    ax[1].set_xlim(0, 6); ax[1].set_ylim(0, 1.05)
    for zt in (2, 4, 6):
        ax[1].annotate(f"$\\times${1/E(zt):.2f}", xy=(zt, 1/E(zt)),
                       xytext=(zt-0.1, 1/E(zt)+0.10), fontsize=8.5,
                       arrowprops=dict(arrowstyle="->", color="0.4"))
    plt.tight_layout(); plt.savefig(os.path.join(OUT, "efe_fig1_prediction.pdf")); plt.close()


def fig2_discrimination():
    zz = np.linspace(0, 6, 60)
    fw = np.array([offset_dex(0.1, 0.5, z) for z in zz])      # framework: EFE ~1/E(z)
    const = fw[0]*np.ones_like(zz)                            # constant-a0 MOND: flat
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.axhline(0, color="navy", lw=2.2, label=r"$\Lambda$CDM / dark matter (no EFE)")
    ax.plot(zz, const, "--", color="darkorange", lw=2.2, label=r"constant-$a_0$ MOND (EFE non-evolving)")
    ax.plot(zz, fw, "-", color="seagreen", lw=2.4, label=r"this framework: EFE $\propto 1/E(z)$")
    # forecast points (optimistic 600-galaxy sample): err on the embedded-isolated offset per z-bin
    zb = np.array([0.3, 1.0, 2.0, 4.0]); off = np.array([offset_dex(0.1, 0.5, z) for z in zb])
    sig_gal, N_per_zbin = 0.25, 150
    err = sig_gal*np.sqrt(2.0/N_per_zbin)                     # difference of two means of N/2
    ax.errorbar(zb, off, yerr=err, fmt="s", color="seagreen", ms=7, capsize=3,
                lw=1.6, label=f"forecast (~600 gal, $\\sigma_{{gal}}$=0.25 dex)")
    ax.set_xlabel("redshift $z$")
    ax.set_ylabel(r"EFE signature: $\log_{10}(\,$boost$_{\rm embedded}/$boost$_{\rm isolated})$")
    ax.set_title("What the measurement separates (galaxy with $g_{\\rm bar}=0.1\\,a_0$, $g_{\\rm ext}=0.5\\,a_0$)")
    ax.set_xlim(0, 6); ax.legend(fontsize=9, loc="lower right"); ax.grid(alpha=0.25)
    plt.tight_layout(); plt.savefig(os.path.join(OUT, "efe_fig2_discrimination.pdf")); plt.close()


def fig3_samplesize():
    signal = abs(offset_dex(0.1, 1.0, 0.0) - offset_dex(0.1, 1.0, 6.0))   # ~0.123 dex
    N = np.linspace(50, 2500, 400)
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    for sg, c, lab in [(0.25, "seagreen", "optimistic $\\sigma_{gal}=0.25$ dex"),
                       (0.41, "firebrick", "realistic $\\sigma_{gal}=0.41$ dex")]:
        # 4 sub-samples (iso/emb x lo/hi-z) of N/4 each; sigma(double-diff)=2 sg/sqrt(N/4)
        signif = signal*np.sqrt(N)/(4*sg)                    # vs TOTAL N
        ax.plot(N, signif, color=c, lw=2.3, label=lab)
        for s in (3, 5):
            Nx = (4*s*sg/signal)**2                           # TOTAL galaxies for s-sigma
            if Nx <= N.max():
                ax.plot([Nx], [s], "o", color=c, ms=6)
                ax.annotate(f"{int(round(Nx))}", xy=(Nx, s), xytext=(Nx+60, s-0.35),
                            fontsize=8.5, color=c)
    for s in (3, 5):
        ax.axhline(s, color="0.6", ls=":", lw=1.2)
        ax.text(2300, s+0.1, f"{s}$\\sigma$", fontsize=9, color="0.4")
    ax.set_xlabel("total sample size (extended, environment-resolved galaxies)")
    ax.set_ylabel("detection significance of the EFE weakening")
    ax.set_title(f"Sample needed to detect EFE $\\propto 1/E(z)$ (signal $\\approx${signal:.2f} dex, $z{{=}}0{{\\to}}6$)")
    ax.set_xlim(0, 2600); ax.set_ylim(0, 8); ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.25)
    plt.tight_layout(); plt.savefig(os.path.join(OUT, "efe_fig3_samplesize.pdf")); plt.close()
    return signal


def main():
    fig1_prediction(); fig2_discrimination(); signal = fig3_samplesize()
    print("figures written to", OUT)
    print(f"  E(2)={E(2):.2f} E(4)={E(4):.2f} E(6)={E(6):.2f}")
    print(f"  EFE offset z=0 (gext=0.5 a0): {offset_dex(0.1,0.5,0.0):+.3f} dex; "
          f"z=4: {offset_dex(0.1,0.5,4.0):+.3f} dex")
    print(f"  distinctive signal (gext=1.0, z0->6): {signal:.3f} dex")
    for sg in (0.25, 0.41):
        print(f"  sigma_gal={sg}: TOTAL N(3sigma)={ (4*3*sg/signal)**2 :.0f}, "
              f"N(5sigma)={ (4*5*sg/signal)**2 :.0f} galaxies (4 sub-samples)")


if __name__ == "__main__":
    main()
