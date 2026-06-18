import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Fig 11.1 -- the 1998 surprise as a magnitude-redshift (Hubble) diagram.
# PUBLISHED-RELATION: the Taylor-expanded m(z) from the chapter's Deeper Dive,
# m(z) = M + 5 log10[ (cz/H0)(1 + 0.5(1-q0) z) ] + 25, plotted as MODEL curves
# for three values of q0. Curves only -- NO fabricated supernova data points.
c = 2.998e5            # km/s
H0 = 70.0              # km/s/Mpc
M = -19.3              # SN Ia calibrated absolute magnitude (illustrative)
z = np.linspace(0.02, 0.9, 400)

def m_of_z(q0):
    dL = (c*z/H0)*(1.0 + 0.5*(1.0 - q0)*z)   # Mpc, low-z expansion
    return M + 5.0*np.log10(dL*1e6/10.0)       # distance modulus (dL converted to pc)

fig, ax = plt.subplots(figsize=(7,4.3))
ax.plot(z, m_of_z(+0.5), color=C_NEWTON, ls="--", lw=2,
        label=r"decelerating  $q_0=+0.5$ (expected)")
ax.plot(z, m_of_z(0.0), color="#94a3b8", ls=":", lw=2,
        label=r"coasting  $q_0=0$")
ax.plot(z, m_of_z(-0.5), color=C_FW, lw=2.6,
        label=r"accelerating  $q_0=-0.5$ (1998 result)")

ax.annotate("distant SNe appear\nFAINTER than braking predicts",
            xy=(0.8, m_of_z(-0.5)[-1]), xytext=(0.30, m_of_z(-0.5)[-1]+0.18),
            fontsize=9.5, color=C_FW,
            arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.4))

ax.set_xlabel("redshift  z   (deeper into the past →)")
ax.set_ylabel("apparent magnitude  m   (fainter ↑)")
ax.set_title("The 1998 surprise: distant supernovae are too faint")
ax.legend(frameon=False, fontsize=9, loc="lower right")
ax.text(0.99,0.01,"model curves -- chapter Deeper Dive m(z); not fitted to data",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch11_magnitude_redshift_surprise.png", bbox_inches="tight"); print("ok")
