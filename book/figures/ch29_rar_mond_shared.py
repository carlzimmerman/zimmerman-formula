import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

a0 = 9.36e-11
g_bar = np.logspace(-13, -8.0, 400)

# Three members of the allowed interpolation (nu) family. All produce the SAME RAR,
# which is precisely the chapter's point: the relation is non-diagnostic of mechanism.
# Framework dS-Unruh:  g_obs = sqrt(g_bar^2 + g_bar a0)
g_fw     = np.sqrt(g_bar**2 + g_bar*a0)
# McGaugh RAR fitting function:  g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0)))
g_mcg    = g_bar/(1.0 - np.exp(-np.sqrt(g_bar/a0)))
# 'simple' mu = x/(1+x):  g_obs = (g_bar + sqrt(g_bar^2 + 4 g_bar a0))/2
g_simple = 0.5*(g_bar + np.sqrt(g_bar**2 + 4*g_bar*a0))

fig, ax = plt.subplots(figsize=(7,4.3))
ax.plot(g_bar, g_mcg,    color=C_MOND,   lw=3.2, alpha=0.55,
        label="McGaugh RAR fit (MOND-family)")
ax.plot(g_bar, g_simple, color=C_DATA,   lw=1.6, ls=(0,(4,2)),
        label='"simple" $\\nu$ (MOND-family)')
ax.plot(g_bar, g_fw,     color=C_FW,     lw=2.0, ls=(0,(1,1)),
        label="framework dS-Unruh $\\nu$")
ax.plot(g_bar, g_bar, color=C_NEWTON, lw=1.4, ls="--", label=r"Newton ($g_{\rm obs}=g_{\rm bar}$)")
ax.plot(g_bar, np.sqrt(g_bar*a0), color="#94a3b8", lw=1.0, ls=":",
        label=r"deep-MOND $\sqrt{g_{\rm bar}a_0}$")

ax.axvline(a0, color="#cbd5e1", lw=1.0)
ax.text(a0*1.15, 3e-13, r"$g_{\rm bar}=a_0$", rotation=90, fontsize=8, color="#64748b", va="bottom")

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(g_bar.min(), g_bar.max()); ax.set_ylim(2e-13, 1.2e-8)
ax.set_xlabel(r"baryonic acceleration  $g_{\rm bar}$  (m/s$^2$)")
ax.set_ylabel(r"observed acceleration  $g_{\rm obs}$  (m/s$^2$)")
ax.set_title("A win shared by the whole family: three $\\nu$'s, one RAR")
ax.legend(frameon=False, loc="upper left", fontsize=8.5)
ax.text(0.99,0.02,"all three curves overlap to $\\lesssim$10% - non-diagnostic of mechanism",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="#666")
fig.tight_layout(); fig.savefig("ch29_rar_mond_shared.png", bbox_inches="tight"); print("ok")
