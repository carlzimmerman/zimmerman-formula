import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# constants
G  = 6.674e-11             # m^3 kg^-1 s^-2
a0 = 9.36e-11             # m/s^2 framework value
Msun = 1.989e30           # kg
kpc  = 3.0857e19          # m
M = 6.0e10*Msun           # Milky Way baryonic mass ~1.2e41 kg (chapter value)

r = np.linspace(0.5, 40, 500)*kpc      # radius 0.5 - 40 kpc

# Newtonian (visible mass only, point-mass approximation outside the disk)
v_newt = np.sqrt(G*M/r)
# Framework modified inertia: solve mu_fw(|a|/a0)*a = G M / r^2 for circular a=v^2/r.
# Equivalent closed form for the framework mu: g_obs = sqrt(g_N^2 + g_N*a0) ... but to stay
# exactly on the chapter's mu_fw we solve numerically per radius.
gN = G*M/r**2
v_fw = np.zeros_like(r)
for i,(rr,gg) in enumerate(zip(r,gN)):
    # solve mu_fw(a/a0)*a = gg  ->  (sqrt(1+(a/a0)^2)-1)/(a/a0) * a = gg
    # let a be the true acceleration; bracket and bisect (monotonic in a)
    lo, hi = 1e-14, 1e-6
    for _ in range(80):
        mid = np.sqrt(lo*hi)
        x = mid/a0
        lhs = (np.sqrt(1+x**2)-1)/x*mid
        if lhs < gg: lo = mid
        else: hi = mid
    a_true = np.sqrt(lo*hi)
    v_fw[i] = np.sqrt(a_true*rr)

# deep-MOND asymptote v^4 = 2 a0 G M (flat)
v_flat = (2*a0*G*M)**0.25

rk = r/kpc
fig, ax = plt.subplots(figsize=(7,4.3))
ax.plot(rk, v_newt/1e3, color=C_NEWTON, lw=1.9, ls="--", label="Newtonian (visible mass only)")
ax.plot(rk, v_fw/1e3,   color=C_FW,     lw=2.6, label=r"modified inertia $\mu_{\rm fw}\,m a=GMm/r^2$")
ax.axhline(v_flat/1e3, color=C_MOND, lw=1.3, ls=":",
           label=r"deep-MOND flat speed $v=(2a_0GM)^{1/4}$")
ax.axhspan(195, 205, color=C_DATA, alpha=0.12)
ax.text(31, 207, "Milky Way outer\nrotation $\\approx200\\,$km/s", fontsize=9, color=C_DATA)

ax.annotate(r"$r$ cancels: $v^4=2a_0GM$", xy=(28, v_flat/1e3),
            xytext=(16, v_flat/1e3+55), color=C_MOND, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=C_MOND, lw=1.0))

ax.set_xlim(0,40); ax.set_ylim(0, 360)
ax.set_xlabel("radius  (kpc)")
ax.set_ylabel("circular orbital speed  (km/s)")
ax.set_title("Flat rotation curve from inertia that knows about dark energy")
ax.legend(frameon=False, fontsize=8.7, loc="upper right")
ax.text(0.01,0.02,"framework-computed (Milky Way $M_b\\approx6\\times10^{10}M_\\odot$)",
        transform=ax.transAxes,ha="left",va="bottom",fontsize=7,color="#999")
fig.tight_layout(); fig.savefig("ch21_flat_rotation_curve.png", bbox_inches="tight"); print("ok")
