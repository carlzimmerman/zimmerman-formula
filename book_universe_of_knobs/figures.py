"""Figures for 'The Universe of Knobs'. Every plotted number is quoted from the
ACDM fried chicken paper (v2.3) or PAPER67 (v1.2); the curves are the law itself."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"serif","font.size":9,"axes.spines.top":False,"axes.spines.right":False})
INK="#1f2a44"; RED="#c0392b"; GOLD="#d4a017"; GREY="#8a8f98"; BLUE="#2e6da4"

# 1. knob counts
fig,ax=plt.subplots(figsize=(4.4,2.9))
names=["the law ($\\kappa$)","base $\\Lambda$CDM (CMB)","R11 feedback","R11b","R13 'complete'","R10 global fns","R9 per galaxy","R14 patchwork"]
k=[1,6,12,14,26,42,1026,1066]
cols=[RED,BLUE]+[INK]*6
ax.barh(range(len(k)),k,color=cols); ax.set_xscale("log"); ax.set_yticks(range(len(k))); ax.set_yticklabels(names)
ax.invert_yaxis(); ax.set_xlabel("number of knobs (log scale)")
for i,v in enumerate(k): ax.text(v*1.15,i,str(v),va="center",fontsize=8)
ax.set_xlim(0.7,2e4)
ax.annotate("string landscape: $10^{500}$ vacua\n(keep going right for about\n$10^{496}$ more page-widths)",xy=(1.9e4,1.0),xytext=(70,1.0),fontsize=7.2,color=GOLD,ha="left",va="center",
            arrowprops=dict(arrowstyle="->",color=GOLD))
fig.tight_layout(); fig.savefig("figures/knob_counts.pdf"); plt.close(fig)

# 2. the law
a0=1.0
gN=np.logspace(-3,2,400); g=gN/2+np.sqrt(gN**2/4+gN*a0)
fig,ax=plt.subplots(figsize=(4.0,3.0))
ax.loglog(gN,g,color=RED,lw=2,label="$g_N=g^2/(g+a_0)$")
ax.loglog(gN,gN,color=GREY,ls="--",label="Newton, $g=g_N$")
ax.loglog(gN,np.sqrt(gN*a0),color=BLUE,ls=":",label="deep limit, $g=\\sqrt{g_N a_0}$")
ax.axvline(1,color=GOLD,lw=0.8); ax.text(1.15,2e-3*30,"$g_N=a_0$",color=GOLD,fontsize=8)
ax.set_xlabel("Newtonian pull of the baryons, $g_N/a_0$"); ax.set_ylabel("observed pull, $g/a_0$")
ax.legend(frameon=False,fontsize=7.5,loc="upper left"); fig.tight_layout(); fig.savefig("figures/the_law.pdf"); plt.close(fig)

# 3. menu: distance to law vs parameters
menu=[("R1 untuned",1,0.1419),("R1 tuned",4,0.0715),("R2",6,0.0721),("R3",2,0.2245),("R4",342,0.0609),("R7",9,0.0408),
      ("R11",12,0.0415),("R11b",14,0.0275),("R10",42,0.0213),("R9 1$\\sigma$",1026,0.0376),("R9 2$\\sigma$",1026,0.0152),
      ("R8p",684,0.0396),("R8 wide",684,0.0056),("A16",15,0.0252),("A25",28,0.0222),("R13",26,0.0290)]
fig,ax=plt.subplots(figsize=(4.4,3.0))
for n,p,d in menu:
    x=max(p,0.8) if n!="R1 untuned" else 0.8
    ax.scatter(x,d,color=INK if d>0.02 else RED,s=18,zorder=3)
    ax.annotate(n,(x,d),xytext=(3,3),textcoords="offset points",fontsize=6.5)
ax.axhline(0.02,color=RED,ls="--",lw=0.9); ax.text(1.0,0.0215,"frozen target E1: 0.02 dex",color=RED,fontsize=7)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("number of fitted parameters"); ax.set_ylabel("rms distance to the law (dex)")
ax.set_ylim(0.004,0.3); fig.tight_layout(); fig.savefig("figures/menu.pdf"); plt.close(fig)

# 4. a0(z)
fig,ax=plt.subplots(figsize=(4.4,3.1))
ax.plot([0,1,1.5,2.33],[1,1.76,2.35,3.49],color=BLUE,ls=":",marker="^",ms=4,label="rival: $a_0\\propto H(z)$, same reconstruction")
ax.axhline(1,color=GREY,lw=0.8,ls="--",label="$w=-1$: exactly flat")
zb=[1,1.5,2.33]; m=[0.91,0.94,0.91]; lo=[0.76,0.71,0.33]; hi=[1.03,1.12,1.21]
ax.errorbar(zb,m,yerr=[np.subtract(m,lo),np.subtract(hi,m)],fmt="o",color=RED,capsize=3,label="law, from measured $\\rho_{\\rm DE}(z)$ (68%)")
ax.plot([2.33,2.33],[3.02,4.55],color=INK,lw=5,alpha=0.5,solid_capstyle="butt",label="tuned $\\Lambda$CDM recipe (A26)")
ax.errorbar([1.0],[2.38e-10/9.3603e-11],yerr=[[0.10e-10/9.3603e-11],[0.12e-10/9.3603e-11]],fmt="s",color=GOLD,capsize=3,label="MUSE-DARK III, face value")
ax.set_xlabel("redshift $z$"); ax.set_ylabel("$a_0(z)/a_0(0)$"); ax.set_ylim(0,5); ax.set_xlim(0,2.6)
ax.legend(frameon=False,fontsize=6.8,loc="upper left"); fig.tight_layout(); fig.savefig("figures/a0z.pdf"); plt.close(fig)

# 5. Occam factor cartoon: evidence vs prior width
fig,ax=plt.subplots(figsize=(4.0,2.6))
x=np.linspace(-6,6,500); like=np.exp(-x**2/2/0.5**2)
ax.fill_between(x,like,color=RED,alpha=0.25); ax.plot(x,like,color=RED,label="likelihood, width $\\sigma_{\\rm post}$")
for w,cc,lab in ((2,INK,"tight prior"),(10,GREY,"wide prior")):
    ax.plot([-w/2,-w/2,w/2,w/2],[0,1/w*2,1/w*2,0],color=cc,label=f"{lab}, width {w}")
ax.set_yticks([]); ax.set_xlabel("knob value"); ax.legend(frameon=False,fontsize=7); fig.tight_layout(); fig.savefig("figures/occam.pdf"); plt.close(fig)
print("ok")
