"""Illustration: where the baryons, settled cold energy, unsettled cold energy and dark energy are in a
Milky-Way-like galaxy under the framework (round cold-energy rule, census edge), and how each pulls.
Inputs (record values): bulge 0.9e10 Msun (Hernquist a=0.7 kpc), disc 4.03e10 (R_d 2.6 kpc), gas 1.08e10 (R_d 6 kpc)
= 6.0e10 total (CFG513); a0 = 9.36e-11 (canonical, kappa = 1/2 fitted); f_ret = 0.10 (census, CFG416); Planck-like
densities. Spherical enclosed-mass approximation for the round rule (CFG516). Illustration, not a fit."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; c=2.998e8
a0=9.36e-11
H0=67.4e3/3.0857e22; rho_crit=3*H0**2/(8*np.pi*G)
rho_DE=0.685*rho_crit; Om_c=0.265; f_b=0.157
rho_c_cos=Om_c*rho_crit
Mb_bulge,ab=0.9e10,0.7; Md,Rd=4.03e10,2.6; Mg,Rg=1.08e10,6.0

def Menc_b(r):  # spherical approx of enclosed baryons [Msun], r in kpc
    x=r/Rd; xg=r/Rg
    return Mb_bulge*r**2/(r+ab)**2 + Md*(1-(1+x)*np.exp(-x)) + Mg*(1-(1+xg)*np.exp(-xg))
nu=lambda y: 1/(1-np.exp(-np.sqrt(y)))
Mb_tot=Mb_bulge+Md+Mg
r_M=np.sqrt(G*Mb_tot*Msun/a0)/kpc
f_ret=0.10
r_edge=r_M/np.log(1+f_ret*f_b/(1-f_b))

r=np.logspace(-1,np.log10(3000),2000)
Mb=Menc_b(r); gN=G*Mb*Msun/(r*kpc)**2; y=gN/a0
Mph=Mb*(nu(y)-1)                       # settled cold energy = round phantom (enclosed)
# supply cap: phantom stops growing beyond the edge (settled mass frozen there)
Mcap=np.interp(r_edge,r,Mph); Mset=np.where(r<=r_edge,Mph,Mcap)
def dens(M):
    dM=np.gradient(M,r); return dM*Msun/(4*np.pi*(r*kpc)**2*kpc)
rho_b=dens(Mb); rho_set=np.clip(dens(Mset),0,None)
g_set=G*Mset*Msun/(r*kpc)**2
g_tot=gN+g_set
Lam=8*np.pi*G*rho_DE/c**2
g_L=Lam*c**2*(r*kpc)/3                 # outward (repulsive) Newtonian-limit Lambda acceleration
v=np.sqrt(g_tot*r*kpc)/1e3; vN=np.sqrt(gN*r*kpc)/1e3

fig=plt.figure(figsize=(15,9.6))
# ---- panel 1: face-on-ish map (log density), 3 zoom levels in one log-radius image
ax1=fig.add_subplot(2,2,1)
n=500; L=60
xx,yy=np.meshgrid(np.linspace(-L,L,n),np.linspace(-L,L,n)); R=np.hypot(xx,yy)+1e-3
Sd=np.exp(-R/Rd)+0.3*np.exp(-R/Rg)
rr=np.interp(R,r,rho_set)
ax1.imshow(rr,extent=[-L,L,-L,L],origin="lower",cmap="Purples",norm=LogNorm(rr.max()/1e4,rr.max()))
ax1.contour(xx,yy,Sd,levels=[0.003,0.03,0.3],colors=["#d9a400","#e8b800","#fff066"],linewidths=[1,1.5,2])
th=np.linspace(0,2*np.pi,300)
ax1.plot(r_M*np.cos(th),r_M*np.sin(th),"w--",lw=1); ax1.text(r_M*0.72,r_M*0.72,f"r_M = {r_M:.1f} kpc\n(g = a₀)",color="w",fontsize=8)
ax1.set_title("Face-on view (±60 kpc): baryon disc (gold contours)\ninside a ROUND cloud of settled cold energy (purple)",fontsize=10)
ax1.set_xlabel("kpc"); ax1.set_ylabel("kpc")
# ---- panel 2: density profiles out to 3 Mpc
ax2=fig.add_subplot(2,2,2)
ax2.loglog(r,rho_b,color="#d9a400",lw=2.2,label="baryons (stars + gas)")
ax2.loglog(r,np.where(r<=r_edge,rho_set,np.nan),color="purple",lw=2.2,label="settled cold energy (round, = the law's extra mass)")
ax2.loglog(r,np.where(r>r_edge,rho_c_cos,np.nan),color="purple",lw=2,ls="--",label="unsettled cold energy (cosmic reservoir)")
ax2.axhline(rho_DE,color="tab:green",lw=2,label="dark energy (uniform, everywhere)")
ax2.axvline(r_edge,color="0.4",ls=":",lw=1.2); ax2.text(r_edge*1.05,1e-20,f"supply edge\n≈ {r_edge:.0f} kpc",fontsize=8,color="0.3")
ax2.axvline(r_M,color="0.6",ls="--",lw=0.8); ax2.text(r_M*1.05,1e-17,"r_M",fontsize=8,color="0.4")
ax2.set_ylim(1e-29,1e-17); ax2.set_xlabel("radius [kpc]"); ax2.set_ylabel("density [kg/m³]")
ax2.set_title("What is where: density vs radius (to 3 Mpc)",fontsize=10); ax2.legend(fontsize=7.5,loc="lower left"); ax2.grid(alpha=0.25,which="both")
# ---- panel 3: accelerations (pulls)
ax3=fig.add_subplot(2,2,3)
ax3.loglog(r,gN,color="#d9a400",lw=2,label="pull of baryons (Newton)")
ax3.loglog(r,g_set,color="purple",lw=2,label="pull of settled cold energy")
ax3.loglog(r,g_tot,color="k",lw=2.4,label="total inward pull (the law)")
ax3.loglog(r,g_L,color="tab:green",lw=2,ls="--",label="dark energy push (outward)")
ax3.axhline(a0,color="0.5",ls=":",lw=1); ax3.text(0.12,a0*1.3,"a₀ = ½ c√(Gρ_DE): dark energy sets where the extra pull switches on",fontsize=7.5,color="0.3")
rz=r[np.argmin(np.abs(g_tot-g_L))]
ax3.axvline(rz,color="tab:green",ls=":",lw=1); ax3.text(rz*0.45,3e-15,f"pull = push\n≈ {rz/1000:.1f} Mpc",fontsize=8,color="tab:green")
ax3.set_ylim(1e-15,1e-8); ax3.set_xlabel("radius [kpc]"); ax3.set_ylabel("acceleration [m/s²]")
ax3.set_title("Who pulls the stars: accelerations vs radius",fontsize=10); ax3.legend(fontsize=7.5,loc="upper right"); ax3.grid(alpha=0.25,which="both")
# ---- panel 4: rotation curve
ax4=fig.add_subplot(2,2,4)
m=r<=60
ax4.plot(r[m],v[m],"k",lw=2.4,label="total (baryons + settled cold energy)")
ax4.plot(r[m],vN[m],color="#d9a400",lw=2,label="baryons alone (Newton)")
ax4.fill_between(r[m],vN[m],v[m],color="purple",alpha=0.18,label="lift from settled cold energy")
ax4.set_xlabel("radius [kpc]"); ax4.set_ylabel("circular speed [km/s]"); ax4.set_xlim(0,60); ax4.set_ylim(0,280)
ax4.set_title("Result: the rotation curve stays high",fontsize=10); ax4.legend(fontsize=8,loc="lower right"); ax4.grid(alpha=0.25)
fig.suptitle("A Milky-Way-like galaxy in the framework: baryons, settled cold energy, the cosmic reservoir, and dark energy\n"
             "(M_b = 6.0×10¹⁰ M☉; a₀ = 9.36×10⁻¹¹ m/s², κ = ½ fitted; f_ret = 0.10; round cold-energy rule; illustration, not a fit)",fontsize=11)
fig.tight_layout(rect=[0,0,1,0.94])
fig.savefig("explainers/img/galaxy_cold_energy_map.png",dpi=140)
print(f"r_M {r_M:.2f} kpc, r_edge {r_edge:.0f} kpc, settled cold mass {Mcap:.3e} Msun, pull=push {rz:.0f} kpc, v(8)={np.interp(8,r,v):.0f}, v(20)={np.interp(20,r,v):.0f}, v(50)={np.interp(50,r,v):.0f}")
