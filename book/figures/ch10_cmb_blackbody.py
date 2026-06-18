import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Planck blackbody spectral radiance vs frequency, for T = 2.725 K (today's CMB).
# B_nu(T) = (2 h nu^3 / c^2) / (exp(h nu / kB T) - 1)   -- exact Planck law.
h  = 6.62607015e-34
c  = 2.99792458e8
kB = 1.380649e-23
T  = 2.725

nu = np.linspace(1e9, 6e11, 1200)          # 1 to 600 GHz
x  = h*nu/(kB*T)
B  = (2*h*nu**3/c**2) / np.expm1(x)         # expm1 is safe near x->0
# convert to MJy/sr for a familiar y-scale (1 Jy = 1e-26 W/m^2/Hz)
B_MJy = B / 1e-26 / 1e6

fig, ax = plt.subplots(figsize=(7,4.3))
ax.plot(nu/1e9, B_MJy, color=C_FW, lw=2.4,
        label="Planck blackbody law, T = 2.725 K")

# peak marker
ipk = np.argmax(B_MJy)
ax.axvline(nu[ipk]/1e9, color=C_NEWTON, ls=":", lw=1.2)
ax.annotate("peak near 160 GHz\n(wavelength ~ 1.9 mm,\nthe microwave band)",
            xy=(nu[ipk]/1e9, B_MJy[ipk]), xytext=(300, B_MJy[ipk]*0.78),
            fontsize=9, color=C_NEWTON,
            arrowprops=dict(arrowstyle="->", color=C_NEWTON, lw=1))

# illustrative "data points" sitting exactly on the curve (model-generated, no scatter)
nud = np.linspace(60e9, 560e9, 18)
xd  = h*nud/(kB*T); Bd = (2*h*nud**3/c**2)/np.expm1(xd)/1e-26/1e6
ax.plot(nud/1e9, Bd, "o", ms=5, color=C_DATA, mec="white", mew=0.6, zorder=5,
        label="illustrative points (on the curve)")

ax.set_xlabel("frequency  (GHz)")
ax.set_ylabel("spectral radiance  (MJy / sr)")
ax.set_title("The CMB is the most perfect blackbody ever measured (2.725 K)")
ax.set_xlim(0, 600); ax.set_ylim(bottom=0)
ax.legend(frameon=False, loc="upper right")
ax.text(0.60, 0.10,
        "speckles on top of this = 1 part in 100,000",
        transform=ax.transAxes, ha="left", va="bottom", fontsize=8, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch10_cmb_blackbody.png", bbox_inches="tight"); print("ok")
