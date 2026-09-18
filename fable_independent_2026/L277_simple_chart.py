#!/usr/bin/env python3
"""L277 -- the comparison stripped to three things: the framework's derived law (flat), LambdaCDM, and the real a0 data.
Same inputs as L274/L276 (the DM14 emergent scale with its halo-mass and concentration-scatter range; MUSE-DARK III's RAR-fitted a0(z)
with its quoted errors; Mayer+2023's LambdaCDM apparent a0, x3 by z = 2).  No DESI what-ifs, no alternative footing, no target bar."""
import os, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
OM = 0.3027; E = lambda z: np.sqrt(OM * (1 + z) ** 3 + (1 - OM)); dex = np.log10
def dm14_c(z, M=1e12):
    a = 0.520 + (0.905 - 0.520) * np.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z; return 10 ** (a + b * np.log10(M / 1e12))
fc = lambda c: np.log(1 + c) - c / (1 + c)
def lcdm(z, M=1e12, dl=0.0):
    c0 = dm14_c(0.0, M) * 10 ** dl; cz = dm14_c(z, M) * 10 ** dl; return E(z) ** (4 / 3) * (cz ** 2 / fc(cz)) / (c0 ** 2 / fc(c0))
zg = np.linspace(0, 5, 101); lc = [dex(lcdm(zg, M, dl)) for M in (1e11, 1e12, 1e13) for dl in (-0.11, 0.0, 0.11)]
zm = np.linspace(0.33, 1.44, 50); a00, a00e, a1, a1e = 1.0, 0.04, 1.59, 0.105
mu_c = dex((a00 + a1 * zm) / a00); mu_lo = dex((a00 - a00e + (a1 - a1e) * zm) / (a00 + a00e)); mu_hi = dex((a00 + a00e + (a1 + a1e) * zm) / (a00 - a00e))
fig, ax = plt.subplots(figsize=(10, 6), dpi=160); fig.patch.set_facecolor("#fcfcfb"); ax.set_facecolor("#fcfcfb")
ax.fill_between(zg, -0.004, 0.004, color="#2a78d6", alpha=0.25, linewidth=0); ax.plot(zg, np.zeros_like(zg), color="#2a78d6", linewidth=2.6, label=r"YOUR LAW:  $a_0^2=\kappa^2G(-p_Q)$, vacuum $w=-1$  $\Rightarrow$  $a_0$ flat to z = 5 (< 1%)")
ax.fill_between(zg, np.min(lc, axis=0), np.max(lc, axis=0), color="#e87ba4", alpha=0.18, linewidth=0); ax.plot(zg, dex(lcdm(zg)), color="#e87ba4", linewidth=2.6, label=r"$\Lambda$CDM:  emergent scale $E(z)^{4/3}[c^2/f(c)](z)/[c^2/f(c)](0)$, +0.33 dex at z = 2.5")
ax.plot([2.0], [dex(3.0)], marker="D", color="#e87ba4", ms=9, markeredgecolor="#0b0b0b", linestyle="none", label=r"$\Lambda$CDM simulations (Mayer+2023): what a RAR fit APPEARS to give, $\times3$ by z = 2")
ax.fill_between(zm, mu_lo, mu_hi, color="#0b0b0b", alpha=0.10, linewidth=0); ax.plot(zm, mu_c, color="#0b0b0b", linewidth=2.4, linestyle="--", label=r"REAL DATA:  MUSE-DARK III 2026, RAR-fitted $a_0(z)=1.0+1.59z$ over z = 0.33-1.44")
ax.errorbar([1.0], [dex(2.38)], yerr=[[dex(2.38) - dex(2.27)], [dex(2.49) - dex(2.38)]], fmt="s", color="#0b0b0b", ms=7, capsize=4, label=r"REAL DATA:  MUSE-DARK III at z $\simeq$ 1:  $a_0 = 2.38\pm0.11\times10^{-10}$ m s$^{-2}$  (+0.38 dex)")
ax.annotate("your prediction", xy=(5.0, 0.0), xytext=(6, 0), textcoords="offset points", va="center", fontsize=9, color="#2a78d6")
ax.annotate("ΛCDM", xy=(5.0, dex(lcdm(5.0))), xytext=(6, 0), textcoords="offset points", va="center", fontsize=9, color="#e87ba4")
ax.axhline(0, color="#52514e", linewidth=0.8, alpha=0.6); ax.set_xlim(0, 5); ax.set_ylim(-0.15, 1.0)
ax.set_xlabel("redshift  z"); ax.set_ylabel(r"$\Delta\log_{10}\,a_0(z)/a_0(0)$   [dex]   (0.30 dex = a factor of 2)")
ax.set_title("Your law, ΛCDM, and the only direct measurement of a₀ versus redshift", fontsize=11)
ax.grid(True, color="#e6e5e1", linewidth=0.6); ax.spines[["top", "right"]].set_visible(False); ax.tick_params(colors="#52514e")
ax.legend(loc="upper left", fontsize=8.3, frameon=False); plt.subplots_adjust(right=0.86)
png = os.path.join(HERE, "L277_simple_chart.png"); fig.savefig(png, bbox_inches="tight", facecolor=fig.get_facecolor()); print("written", png)
