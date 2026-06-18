import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))
r = np.linspace(2, 30, 400)
r_edge = 8.0
v_flat = 180.0
M_tot = v_flat**2 * r_edge          # so that the Keplerian branch matches at r_edge
v_kep = np.sqrt(M_tot / r)
v_obs = np.full_like(r, v_flat)
inner = r <= r_edge
v_kep[inner] = v_flat * np.sqrt(r[inner]/r_edge)
v_obs[inner] = v_flat * np.sqrt(r[inner]/r_edge)
ax.plot(r, v_obs, color=C_DATA, lw=2.6, label="Observed: stays flat")
ax.plot(r[r>=r_edge], v_kep[r>=r_edge], color=C_NEWTON, lw=2.4, ls="--",
        label=r"Newtonian prediction: $v\propto 1/\sqrt{r}$")
ax.plot(r[inner], v_kep[inner], color=C_NEWTON, lw=2.4, ls="-", alpha=0.6)
ax.axvspan(2, r_edge, color="#fbbf24", alpha=0.10)
ax.text(4.5, 60, "bright\nstellar disk", ha="center", fontsize=9, color="#92700a")
ax.text(22, 60, "light has\nessentially ended", ha="center", fontsize=9, color="#64748b")
ax.axvline(r_edge, color="#888", lw=0.8, ls=":")
ax.set_xlabel("radius from galaxy center  (kpc)")
ax.set_ylabel("orbital speed  (km/s)")
ax.set_title("The punchline: rotation curves stay flat where they should fall")
ax.set_ylim(0, 240); ax.set_xlim(2, 30)
ax.legend(frameon=False, loc="lower right")
ax.text(0.01,0.97,"schematic - framework/Newtonian forms", transform=ax.transAxes,
        ha="left", va="top", fontsize=7, color="#aaa")
fig.tight_layout(); fig.savefig("ch02_flat_vs_keplerian.png", bbox_inches="tight"); print("ok")
