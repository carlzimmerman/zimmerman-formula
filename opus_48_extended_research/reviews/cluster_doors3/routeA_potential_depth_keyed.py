#!/usr/bin/env python3
r"""
ROUTE A -- POTENTIAL-DEPTH-keyed (|Phi|/c^2) galaxy-safe cluster boost.
=======================================================================
The natural complement to the FAILED density-keying. Clusters out-rank galaxies in
exactly ONE thing relevant here: potential DEPTH |Phi|/c^2. The density-a0 floor BROKE
galaxies because galaxies are DENSER than clusters. So: key the modification on |Phi|/c^2
(the TRUE integrated potential depth, deepest at the CENTER) -- NOT density -- and ask:

  G1 SUFFICIENCY: does a |Phi|-keyed boost reach the ~30-49% gas-tracking cluster-core
                  residual at a0=9.36e-11?  (magnitude AND radial shape)
  G2 GALAXY-VETO: SPARC RAR scatter stays <~0.13 dex?  (real 175-galaxy data)
  G3 NO-NEW-PARTICLE: is the term own-field / known-physics, or a hand-placed threshold?
  G4 DATA / CASSINI: the Sun's CENTER |Phi|/c^2~2e-6, a neutron star ~0.2 -- does a
                  |Phi|-keyed term violate Cassini |gamma-1|<2.3e-5, pulsar, BBN?

THE LOAD-BEARING FIX over the prior solution_hunt/galaxy_veto_potential_route.py:
  that script used |Phi|/c^2 ~ Vbar^2/c^2 (the LOCAL circular speed squared). That is
  the WRONG quantity. The gravitational potential DEPTH is
        |Phi(r)|/c^2 = (1/c^2) * integral_r^inf  g(r') dr'
  which is DEEPEST at the center and FAR larger than the local v^2 (for an isothermal/NFW
  the central depth is ~ several * v_flat^2, not v^2). Using the true integrated depth
  is the framework's fairest footing for Route A -- it MAXIMIZES the cluster/galaxy
  contrast (clusters are deep AND extended). We compute the true depth for both clusters
  (from the real A2029/RXJ1347 total profiles) and SPARC (from the integrated baryonic g).

FRAMEWORK FOOTING (quarantine: a0/Z/kappa NEVER asserted derived):
  a0 = 9.36e-11 m/s^2 ; modified-inertia g_obs = sqrt(g_bar^2 + g_bar*a0) ; Ups=0.70.
BOTH-WAYS (#1 rule): hunt a genuine galaxy-safe + Cassini-safe depth-keyed cluster boost
HARD; concede honestly if a gate breaks. No manufactured cure, no reflexive dismissal.
"""
import numpy as np, glob, os
from scipy.integrate import quad

# ---------------- constants ----------------
G=6.674e-11; c=2.998e8; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
Msun_g=1.989e33; kpc_cm=3.0857e21
a0=9.36e-11
HERE=os.path.dirname(__file__)
SPARC=os.path.join(HERE,"..","..","..","real_research","data","sparc_data")

print("="*94)
print(" ROUTE A -- POTENTIAL-DEPTH |Phi|/c^2 keyed cluster boost  (both ways, quarantine held)")
print("="*94)

# =====================================================================================
# STEP 0 -- the TRUE potential depth for clusters (real A2029 + RXJ1347 total profiles)
# =====================================================================================
# Potential depth |Phi(r)|/c^2 = (1/c^2) * [ G*M(<r)/r  +  integral_r^inf G*M(<r')/r'^2 dr' ]
# (the standard |Phi(r)| = G*M(<r)/r + G*int_r^inf M(<r')/r'^2 dr', vanishing at infinity).
def phi_depth_from_Mofr(M_of_r_Msun, r_kpc, r_out_kpc=5000.0):
    """|Phi(r)|/c^2 from a cumulative-mass function M(<r) [Msun], r in kpc."""
    r_m = r_kpc*kpc
    inner = G*(M_of_r_Msun(r_kpc)*Msun)/r_m                       # G M(<r)/r
    def integrand(rp_kpc):                                        # G M(<r')/r'^2 dr', SI
        return G*(M_of_r_Msun(rp_kpc)*Msun)/((rp_kpc*kpc)**2) * kpc
    outer,_ = quad(integrand, r_kpc, r_out_kpc, limit=200)
    return (inner+outer)/c**2

# --- A2029 NFW total (Sohn+2019 caustic: M200=8.47e14, c=4, R200=1.91 Mpc) ---
def nfw_M(r_kpc,M200,c_nfw,r200_kpc):
    rs=r200_kpc/c_nfw; m=lambda x: np.log(1+x)-x/(1+x)
    return M200*m(np.asarray(r_kpc)/rs)/m(c_nfw)
A2029_M  = lambda r: nfw_M(r, 8.47e14, 4.0, 1910.0)
# --- RXJ1347 NFW total (Umetsu+2016: M200c=34.2e14, c=3.09, R200~2.9 Mpc) ---
RXJ_M    = lambda r: nfw_M(r, 34.2e14, 3.09, 2900.0)

R_KPC=np.array([20.,50.,100.,200.,300.,500.])
print("\n[STEP 0] TRUE potential depth |Phi|/c^2 (integrated, deepest at center):")
print(f"  {'r(kpc)':>7} {'A2029 |Phi|/c^2':>16} {'RXJ1347 |Phi|/c^2':>18}")
A2029_phi=np.array([phi_depth_from_Mofr(A2029_M,r) for r in R_KPC])
RXJ_phi  =np.array([phi_depth_from_Mofr(RXJ_M,r)   for r in R_KPC])
for i,r in enumerate(R_KPC):
    print(f"  {r:7.0f} {A2029_phi[i]:16.3e} {RXJ_phi[i]:18.3e}")
phi_core_cluster = A2029_phi[1]   # at 50 kpc, the core anchor
phi_RXJ_core     = RXJ_phi[1]
print(f"\n  central (50 kpc) cluster depth: A2029={phi_core_cluster:.2e}  RXJ1347={phi_RXJ_core:.2e}")
print(f"  -> TRUE depth at cluster center is ~{phi_core_cluster/8.4e-6:.1f}x the prior v^2/c^2 proxy (8.4e-6)")

# =====================================================================================
# STEP 1 -- the cluster-core residual we must close (gas-tracking, banked)
# =====================================================================================
# Banked A2029 (framework footing): M_MOND/M_tot ~ 50-71% -> residual ~30-49% of total.
# The boost must MULTIPLY the MOND phantom enough to source the residual mass.
# Required boost factor B(r) = M_tot(r) / M_MOND(r). We compute it from the real profiles.
def M_mond(Mbar_Msun, r_kpc):
    r_m=np.asarray(r_kpc)*kpc; Mbar=np.asarray(Mbar_Msun)*Msun
    gbar=G*Mbar/r_m**2; gobs=np.sqrt(gbar**2+gbar*a0)
    return gobs*r_m**2/G/Msun
# A2029 baryons: gas (LBS03 cusp-beta) + IC1101 stars (published saturating profile)
rho_gc=6.6e-26; beta_g=0.54; alpha_g=0.55; rc_gas=77.6
def rho_gas_cgs(r):
    x=np.asarray(r)/rc_gas
    return rho_gc*2.0**(1.5*beta_g-0.5*alpha_g)*x**(-alpha_g)*(1+x**2)**(-1.5*beta_g+0.5*alpha_g)
def Mgas(r_kpc):
    def one(rr):
        v,_=quad(lambda rp:4*np.pi*(rp*kpc_cm)**2*rho_gas_cgs(rp)*kpc_cm,1e-3,rr,limit=200)
        return v/Msun_g
    return np.array([one(r) for r in np.atleast_1d(r_kpc)])
_sr=np.array([50.,100.,200.,500.]); _sp=np.array([1.2e12,3.0e12,3.4e12,3.8e12])
def Mstar(r_kpc):
    out=np.exp(np.interp(np.log(np.atleast_1d(r_kpc)),np.log(_sr),np.log(_sp),
                         left=np.log(_sp[0]),right=np.log(_sp[-1])))
    out=np.where(np.atleast_1d(r_kpc)<50., _sp[0]*(np.atleast_1d(r_kpc)/50.)**1.5, out)
    return out
A2029_gas=Mgas(R_KPC); A2029_star=Mstar(R_KPC)
A2029_bar=A2029_gas+A2029_star
A2029_tot=A2029_M(R_KPC)
A2029_mond=M_mond(A2029_bar,R_KPC)
B_req = A2029_tot/A2029_mond           # boost factor MOND needs on g (to make M_MOND=M_tot)
print("\n[STEP 1] A2029 required boost factor B(r)=M_tot/M_MOND (gas-tracking residual):")
print(f"  {'r(kpc)':>7} {'M_tot':>11} {'M_MOND':>11} {'B_req=tot/MOND':>15} {'cover MOND/tot':>15}")
for i,r in enumerate(R_KPC):
    print(f"  {r:7.0f} {A2029_tot[i]:11.3e} {A2029_mond[i]:11.3e} {B_req[i]:15.3f} {1/B_req[i]*100:13.1f}%")
print("  -> NOTE the SHAPE: B_req is LARGEST at the center... or outward? read the column.")

# =====================================================================================
# STEP 2 -- the |Phi|-keyed boost law.  Candidate forms (own-field-plausible):
#   (i)   linear:  B = 1 + amp*(|Phi|/c^2)            (mechanism-forced if any)
#   (ii)  power:   B = 1 + amp*(|Phi|/c^2)^p          (p>1 steep)
#   (iii) running a0: a0_eff = a0*(1 + amp*(|Phi|/c^2)^p) -> via g_obs
# We REQUIRE the law to close the cluster core (tune amp at the core anchor), then read
# (a) the cluster radial SHAPE it predicts, and (b) what it does to SPARC (G2) + Sun (G4).
# =====================================================================================
print("\n[STEP 2] Does a |Phi|-keyed boost give the cluster the RIGHT RADIAL SHAPE?")
print("  The boost B(|Phi|) inherits |Phi|'s radial shape. |Phi| is DEEPEST at the center")
print("  and DECREASES outward. The required B_req shape is (from STEP 1):")
shape_Breq = np.log(B_req[-1]/B_req[1])/np.log(R_KPC[-1]/R_KPC[1])   # 50->500 log-slope
shape_phi  = np.log(A2029_phi[-1]/A2029_phi[1])/np.log(R_KPC[-1]/R_KPC[1])
print(f"    d ln(B_req)/d ln r [50->500] = {shape_Breq:+.3f}   (the boost the data want)")
print(f"    d ln(|Phi|)/d ln r [50->500] = {shape_phi:+.3f}   (what a |Phi|-key delivers)")
print(f"  Any monotone B(|Phi|) gives a boost that DECREASES outward (sign of d ln|Phi|/dlnr<0).")
print(f"  If B_req INCREASES outward (slope>0), a |Phi|-key gives the WRONG SHAPE (anti-correlated).")

# Now the magnitude: at fixed radius, can amp be tuned to hit B_req at the core?  Yes trivially.
# The real test is the JOINT (shape + galaxy veto + Cassini). Compute amp for each (form,p)
# by matching B at 200 kpc (mid-core, the residual's mass-weighted radius).
i_anchor=3  # 200 kpc
Bset = B_req[i_anchor]; phiset = A2029_phi[i_anchor]
print(f"\n  Tuning amp to hit B_req={Bset:.2f} at r={R_KPC[i_anchor]:.0f} kpc (|Phi|/c^2={phiset:.2e}):")

# =====================================================================================
# STEP 3 -- THE GALAXY VETO on REAL SPARC, with the TRUE integrated depth |Phi|/c^2
# =====================================================================================
def load_sparc_depth():
    """Per galaxy: gbar, gobs, and TRUE |Phi|/c^2 = (1/c^2) int_r^inf gbar dr (+ outer tail)."""
    rows=[]
    for f in sorted(glob.glob(os.path.join(SPARC,"*_rotmod.dat"))):
        try: dat=np.loadtxt(f,comments="#")
        except Exception: continue
        if dat.ndim!=2 or dat.shape[1]<7: continue
        R=dat[:,0]; Vobs=dat[:,1]; Vgas=dat[:,3]; Vdisk=dat[:,4]; Vbul=dat[:,5]  # R[kpc],V[km/s]
        Ups=0.70
        Vbar2=Vgas*np.abs(Vgas)+Ups*Vdisk*np.abs(Vdisk)+1.4*Ups*Vbul*np.abs(Vbul)  # (km/s)^2
        Vbar2=np.clip(Vbar2,0,None)
        R_m=R*kpc; Vbar2_si=Vbar2*1e6  # (m/s)^2
        gbar=Vbar2_si/R_m; gobs=(Vobs*1e3)**2/R_m
        m=(R>0)&(gbar>0)&(gobs>0)&np.isfinite(gbar)&np.isfinite(gobs)
        if m.sum()<3: continue
        # TRUE |Phi(r)|/c^2 from the measured gbar(r): inner = int_0^r ... no; use
        # |Phi(r)| = int_r^inf gbar dr' + (inner already folded: Phi at r is the work to bring
        # a test mass from inf to r) = int_r^inf gbar(r') dr'. We integrate the measured gbar
        # outward, treating gbar~Vflat^2/r beyond the last point (flat-RC tail) to r_out=10*Rmax.
        Rs=R_m[m]; gb=gbar[m]; order=np.argsort(Rs); Rs=Rs[order]; gb=gb[order]
        phi=np.zeros_like(Rs)
        for k in range(len(Rs)):
            # integral from Rs[k] to last measured point (trapezoid)
            seg=0.0
            for j in range(k,len(Rs)-1):
                seg+=0.5*(gb[j]+gb[j+1])*(Rs[j+1]-Rs[j])
            # flat-tail beyond last point: gbar~g_last*(R_last/r')... use Vbar2 const -> gbar~Vb2/r'
            Vb2_last=gb[-1]*Rs[-1]
            tail=Vb2_last*np.log(10.0)   # int_{Rlast}^{10 Rlast} Vb2/r' dr' = Vb2 ln(10)
            phi[k]=(seg+tail)/c**2
        rows.append((gb, gobs[m][order], phi))
    return rows

rows=load_sparc_depth()
gbar_s=np.concatenate([r[0] for r in rows])
gobs_s=np.concatenate([r[1] for r in rows])
phi_s =np.concatenate([r[2] for r in rows])
print("\n[STEP 3] REAL SPARC galaxy veto with TRUE integrated |Phi|/c^2 (%d galaxies, %d pts):"
      % (len(rows), len(gbar_s)))
print(f"    SPARC |Phi|/c^2 (true depth): median={np.median(phi_s):.2e}  "
      f"range=[{phi_s.min():.1e},{phi_s.max():.1e}]  max={phi_s.max():.2e}")
print(f"    cluster core (A2029 @200 kpc) |Phi|/c^2={phiset:.2e};  "
      f"DEEPEST SPARC disk |Phi|/c^2={phi_s.max():.2e}")
contrast = phiset/phi_s.max()
print(f"    *** core/deepest-disk CONTRAST = {contrast:.2f}x ***  (the whole game: need ON@core, OFF@disk)")

def nu(gb,a0_): return np.sqrt(gb**2+gb*a0_)
def rar_scatter(a0eff):
    res=np.log10(gobs_s)-np.log10(nu(gbar_s,a0eff))
    return 1.4826*np.median(np.abs(res-np.median(res)))
floor=rar_scatter(a0*np.ones_like(gbar_s))
print(f"    RAR scatter floor (constant a0): {floor:.4f} dex  (lit ~0.13)")

print("\n  Form (iii) a0_eff=a0*(1+amp*(|Phi|/c^2)^p), amp tuned to close A2029 core @200 kpc:")
print(f"  {'p':>3} {'amp':>12} {'core boost B':>13} {'med a0eff/a0 SPARC':>19} {'max a0eff/a0':>13} {'RAR dex':>9} {'G2':>6}")
for p in [1,2,3,4,6]:
    # close the core: a0_eff/a0 at the core must give g_obs boost ~ B_req(200). For deep-MOND
    # g_obs=sqrt(gbar*a0eff) so M_MOND ~ sqrt(a0eff) -> need a0eff/a0 = B_req^2 at the core.
    need_a0_ratio = Bset**2
    amp = (need_a0_ratio-1.0)/phiset**p
    a0eff_s = a0*(1+amp*phi_s**p)
    sc=rar_scatter(a0eff_s)
    core_boost=np.sqrt(1+amp*phiset**p)   # =B at core by constr
    g2="PASS" if sc<floor+0.02 else "BREAK"
    print(f"  {p:>3} {amp:12.3e} {core_boost:13.3f} {np.median(a0eff_s/a0):19.3f} "
          f"{np.max(a0eff_s/a0):13.2f} {sc:9.4f} {g2:>6}")

# =====================================================================================
# STEP 4 -- CASSINI / solar-system / compact-object veto (G4)
# =====================================================================================
print("\n[STEP 4] CASSINI / solar-system / compact-object veto (G4):")
# Sun surface |Phi|/c^2 = GM_sun/(R_sun c^2) = 2.12e-6 ; Sun CENTER ~ 3x deeper ~ 6e-6 (polytrope)
phi_sun_surf = G*1.989e30/(6.957e8*c**2)
phi_sun_cent = 2.8*phi_sun_surf   # central potential of an n=3 polytrope ~2.8x surface
phi_ns       = G*(1.4*1.989e30)/(12e3*c**2)   # 1.4 Msun, 12 km neutron star surface
print(f"    Sun surface |Phi|/c^2 = {phi_sun_surf:.2e}")
print(f"    Sun center  |Phi|/c^2 ~ {phi_sun_cent:.2e}  (n=3 polytrope ~2.8x surface)")
print(f"    Neutron star surface |Phi|/c^2 ~ {phi_ns:.2e}  (DEEPER than any cluster core!)")
print(f"    cluster core (A2029 @50 kpc) |Phi|/c^2 = {phi_core_cluster:.2e}")
print(f"    -> Saturn orbit is at HIGH acceleration g~6.5e-3 m/s^2 >> a0; |gamma-1| bound 2.3e-5.")
# A boost a0_eff/a0 = (1+amp*phi^p) at Saturn (where local |Phi|/c^2 from Sun = GM/(r c^2)):
r_saturn=9.58*1.496e11
phi_saturn = G*1.989e30/(r_saturn*c**2)   # |Phi|/c^2 of Sun at Saturn
print(f"    |Phi_sun|/c^2 at Saturn orbit = {phi_saturn:.2e}")

# =====================================================================================
# SUMMARY
# =====================================================================================
print("\n"+"="*94)
print(" SUMMARY -- to be interpreted in the verdict (both ways)")
print("="*94)
print(f"  core/deepest-disk |Phi| contrast = {contrast:.2f}x")
print(f"  required core boost B_req(200kpc) = {Bset:.2f}  (a0_eff/a0 = {Bset**2:.2f})")
print(f"  B_req radial slope = {shape_Breq:+.3f} ; |Phi| radial slope = {shape_phi:+.3f}")
print(f"  Sun-center |Phi|/c^2={phi_sun_cent:.1e}, NS surface={phi_ns:.1e} vs cluster core={phi_core_cluster:.1e}")
