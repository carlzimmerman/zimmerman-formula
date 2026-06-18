import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# DESI DR2-class CPL background: w(a)=w0+wa(1-a)
Om=0.31; w0=-0.75; wa=-0.86
def rhoDE(z):
    a=1.0/(1.0+z)
    return a**(-3.0*(1.0+w0+wa))*np.exp(-3.0*wa*(1.0-a))
def rhotot(z):
    return Om*(1.0+z)**3 + (1.0-Om)*rhoDE(z)

z=np.linspace(0,3,400)
# framework footing: a0 tracks sqrt(rho_DE)
a0rat=np.sqrt(rhoDE(z))
v_fw=a0rat**0.25               # BTFR: v ~ a0^(1/4) at fixed baryonic mass
# rival footing: a0 tracks sqrt(rho_total) -> rises
a0riv=np.sqrt(rhotot(z)/rhotot(0))
v_riv=a0riv**0.25

fig, ax = plt.subplots(figsize=(7.4,4.6))
ax.axhline(1.0,color=C_NEWTON,ls="--",lw=1.3,label="local BTFR (today's a$_0$)")
ax.plot(z,v_fw,color=C_FW,lw=2.6,label="framework: a$_0$ $\\propto\\sqrt{\\rho_{DE}}$ (slow at high z)")
ax.plot(z,v_riv,color=C_DATA,lw=2.2,ls="-",label="rival footing: a$_0$ $\\propto\\sqrt{\\rho_{tot}}$ (fast)")

# annotate the two diagnostic points from the chapter
zb=0.405; vb=(np.sqrt(rhoDE(zb)))**0.25
ax.scatter([zb],[vb],color=C_FW,s=42,zorder=5)
ax.annotate("+%.1f%% bump near z≈0.4\n(phantom-divide crossing)"%((vb-1)*100),
    (zb,vb),(0.55,1.07),fontsize=8.3,color=C_FW,
    arrowprops=dict(arrowstyle="->",color=C_FW,lw=1.1))
z3=3.0; v3=(0.74)**0.25
ax.scatter([z3],[v3],color=C_FW,s=42,zorder=5)
ax.annotate("a$_0$=0.74 a$_0$(0) → %.1f%% slow\n(26%% in a$_0$ → 7%% in speed)"%((1-v3)*100),
    (z3,v3),(1.45,0.945),fontsize=8.3,color=C_FW,
    arrowprops=dict(arrowstyle="->",color=C_FW,lw=1.1))

ax.axhspan(0.99,1.01,color=C_NEWTON,alpha=0.08)
ax.text(2.55,1.40,"opposite SIGN\n= the diagnostic",fontsize=8.2,color=C_DATA,ha="center")
ax.set_xlim(0,3); ax.set_ylim(0.90,1.50)
ax.set_xlabel("redshift  z  (look-back into the past →)")
ax.set_ylabel("flat rotation speed  v$_f$(z) / v$_f$(0)\nat fixed baryonic mass")
ax.set_title("The high-z Tully–Fisher test: which way does a fixed-mass galaxy spin?")
ax.legend(frameon=False,fontsize=8.6,loc="upper left")
ax.text(2.98,0.905,"framework a$_0$(z) curve, fourth-rooted through v$^4$=GM a$_0$",
    ha="right",fontsize=6.6,color="#94a3b8")
fig.tight_layout(); fig.savefig("ch32_a0z_btfr_offset.png", bbox_inches="tight"); print("ok")
