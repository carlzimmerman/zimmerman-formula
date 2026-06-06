#!/usr/bin/env python3
"""
Publication figures for "The Zimmerman Theory of Gravity".
  Fig 1 -- the Radial Acceleration Relation with the framework curve g_obs=sqrt(g_bar^2+g_bar a0), a0=9.36e-11, Ups=0.70.
  Fig 2 -- a0(z)/a0(0): framework DECLINING sqrt(rho_DE) vs constant vs rising-cH, with RC100 deep-MOND data.
  Fig 3 -- the Baryonic Tully-Fisher Relation (total M_b vs V_flat) with the deep-MOND slope-4 line at the framework a0.
All on the framework's OWN equation (NOT regular MOND). Outputs PNGs to papers/figures/.  C. Zimmerman 2026-06-06.
"""
import numpy as np, glob, os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

c=2.998e8; G=6.674e-11; kpc=3.0857e19; Msun=1.989e30
H0=2.184e-18; OmL=0.685; Om=0.315
rho_crit=3*H0**2/(8*np.pi*G); rho_L=OmL*rho_crit
a0=(c/2)*np.sqrt(G*rho_L)                      # framework a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11
Ud,Ub=0.70,0.98
HERE=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(os.path.dirname(HERE),"data")
OUT=os.path.join(HERE,"figures"); os.makedirs(OUT,exist_ok=True)
print(f"framework a0 = {a0:.3e} m/s^2")

# ---------- Fig 1: RAR ----------
gb_all,go_all=[],[]
for f in sorted(glob.glob(os.path.join(DATA,"sparc_data","*_rotmod.dat"))):
    try: d=np.genfromtxt(f,comments="#")
    except: continue
    if d.ndim!=2 or d.shape[1]<6: continue
    R,Vobs,eV,Vgas,Vdisk,Vbul=(d[:,i] for i in range(6)); Rm=R*kpc
    Vbar2=np.sign(Vgas)*Vgas**2+Ud*Vdisk**2+Ub*Vbul**2
    gbar=Vbar2*1e6/Rm; gobs=(Vobs*1e3)**2/Rm
    ok=(gbar>0)&(gobs>0)&np.isfinite(gbar)&np.isfinite(gobs)&(Vobs>0)
    gb_all+=list(gbar[ok]); go_all+=list(gobs[ok])
gb_all,go_all=np.array(gb_all),np.array(go_all)
xs=np.logspace(-12.5,-8.0,200); ys=np.sqrt(xs**2+xs*a0)
fig,ax=plt.subplots(figsize=(6.2,5.6))
ax.scatter(gb_all,go_all,s=5,alpha=0.18,color="#2b6cb0",rasterized=True,label=f"SPARC points (N={len(gb_all)}, Υ=0.70)")
ax.plot(xs,ys,"k-",lw=2.2,label=r"framework $g_{obs}=\sqrt{g_{bar}^2+g_{bar}a_0}$")
ax.plot(xs,xs,"--",color="0.5",lw=1.2,label="Newton (1:1)")
ax.axvline(a0,color="#c05621",ls=":",lw=1.3); ax.text(a0*1.15,1e-12,r"$a_0=9.36\times10^{-11}$",color="#c05621",fontsize=9,rotation=90,va="bottom")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(3e-13,1e-8); ax.set_ylim(3e-13,1e-8)
ax.set_xlabel(r"$g_{bar}$  [m s$^{-2}$]"); ax.set_ylabel(r"$g_{obs}$  [m s$^{-2}$]")
ax.set_title("Radial Acceleration Relation — framework $a_0$, scatter 0.108 dex")
ax.legend(loc="upper left",fontsize=8.5,framealpha=0.9); ax.grid(alpha=0.2,which="both")
fig.tight_layout(); fig.savefig(os.path.join(OUT,"fig1_rar.png"),dpi=160); plt.close(fig)
print("wrote fig1_rar.png")

# ---------- Fig 2: a0(z)/a0(0) models + RC100 deep-MOND data ----------
def rhoDE_ratio(z,w0=-0.752,wa=-0.86):
    a=1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
def E(z): return np.sqrt(Om*(1+z)**3+OmL)
zz=np.linspace(0,3,200)
fig,ax=plt.subplots(figsize=(6.4,5.0))
ax.plot(zz,np.sqrt(rhoDE_ratio(zz)),"-",color="#2f855a",lw=2.4,label=r"framework  $a_0\propto\sqrt{\rho_{DE}(z)}$ (declining)")
ax.plot(zz,np.ones_like(zz),"--",color="0.4",lw=1.6,label="constant $a_0$ (regular MOND)")
ax.plot(zz,E(zz),"-.",color="#c53030",lw=1.8,label=r"rising-$cH$ rival  $a_0\propto E(z)$ (excluded, $\Delta\chi^2\approx49$)")
# RC100 deep-MOND data (per-galaxy a0 normalized to the framework value), if available
rc=os.path.join(DATA,"rc100_nestorshachar2023_table3.csv")
if os.path.exists(rc):
    zr,ar=[],[]
    with open(rc) as fh:
        for row in csv.DictReader(fh):
            try:
                deep=str(row.get("deepMOND_g_lt_a0","")).strip().lower() in ("true","1","yes")
                a_g=float(row["a0_Vc4_over_GMbar_ms2"]); zg=float(row["z"])
            except: continue
            if deep and a_g>0: zr.append(zg); ar.append(a_g/a0)
    if zr:
        ax.scatter(zr,ar,s=26,color="#2b6cb0",edgecolor="k",lw=0.4,alpha=0.8,label=f"RC100 deep-MOND (N={len(zr)})",zorder=5)
        print(f"RC100 deep-MOND points plotted: {len(zr)} (median a0/a0_fw={np.median(ar):.2f})")
ax.axhline(1,color="0.8",lw=0.8)
ax.set_xlabel("redshift  z"); ax.set_ylabel(r"$a_0(z)/a_0(0)$")
ax.set_ylim(0,3.2); ax.set_xlim(0,3)
ax.set_title("Evolution of the acceleration scale — the decisive test (ELT z≈3)")
ax.legend(loc="upper left",fontsize=8.5,framealpha=0.92); ax.grid(alpha=0.2)
ax.annotate("0.74× at z=3",(3,0.737),(2.2,0.45),fontsize=8.5,color="#2f855a",
            arrowprops=dict(arrowstyle="->",color="#2f855a"))
fig.tight_layout(); fig.savefig(os.path.join(OUT,"fig2_a0z.png"),dpi=160); plt.close(fig)
print("wrote fig2_a0z.png")

# ---------- Fig 3: BTFR ----------
mt=os.path.join(DATA,"sparc_master_clean.csv"); logV,logM=[],[]
with open(mt) as fh:
    for row in csv.DictReader(fh):
        try:
            Vf=float(row["Vflat"]); Q=float(row["Q"]); L36=float(row["L36"]); MHI=float(row["MHI"])
        except: continue
        if Vf<=20 or Q>2: continue
        Mb=(Ud*L36+1.33*MHI)*1e9
        if Mb>0: logV.append(np.log10(Vf)); logM.append(np.log10(Mb))
logV,logM=np.array(logV),np.array(logM)
fig,ax=plt.subplots(figsize=(6.2,5.2))
ax.scatter(10**logV,10**logM,s=20,color="#2b6cb0",edgecolor="k",lw=0.3,alpha=0.7,label=f"SPARC (N={len(logV)}, Υ=0.70)")
Vline=np.logspace(1.3,2.5,100)*1e3
Mb_pred=(Vline**4/(G*a0))/Msun
ax.plot(Vline/1e3,Mb_pred,"k-",lw=2.2,label=r"deep-MOND $M_b=V_{flat}^4/(G\,a_0)$ (slope 4)")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"$V_{flat}$  [km s$^{-1}$]"); ax.set_ylabel(r"$M_b=\Upsilon L_{3.6}+1.33M_{HI}$  [$M_\odot$]")
ax.set_title("Baryonic Tully–Fisher — normalization set by the framework $a_0$")
ax.legend(loc="upper left",fontsize=8.5); ax.grid(alpha=0.2,which="both")
fig.tight_layout(); fig.savefig(os.path.join(OUT,"fig3_btfr.png"),dpi=160); plt.close(fig)
print("wrote fig3_btfr.png")
print("DONE -> papers/figures/")
