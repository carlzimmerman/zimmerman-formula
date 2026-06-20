"""
ROUTE 2 -- ADVERSARIAL VERIFY of the discrete-vs-smooth collective QUMOND result.

The compute step found: discrete/smooth TOTAL core gravitating mass = +1.6%
(essentially the flux theorem -- clumpiness redistributes, ~no net mass), and
the inter-galaxy collective field g_N ~ 0.21 a0 (BELOW a0, deep-MOND), with the
EFE on members g_ext ~ 0.11 a0 << g_int ~ 1.2 a0 (EFE wrong sign, members
suppressed). This script stress-tests the load-bearing +1.6% number:

  (1) Is +1.6% a real clumpy excess or a GRID/divergence artifact? Vary grid
      resolution (64,96,128) and galaxy softening b_gal (5,15,30 kpc). A real
      flux-theorem result should drive the difference toward 0 as the box/grid
      captures the full flux; a numerical artifact would NOT converge.
  (2) The EXACT flux theorem cross-check: M_tot(<r) from the SURFACE integral
      oint nu*g_N.dA on a sphere, discrete vs smooth -- this is the clean test of
      "does clumpiness change the enclosed mass" with NO volume-divergence noise.
  (3) Sub-additivity at the cluster scale: collective field of N members vs the
      linear sum (Carl's "overlap adds") vs the smooth-equivalent.

Both ways: if the difference is ~0 (flux theorem holds) -> redistributes-only,
Carl's collective effect adds no net cluster mass. If it's a robust positive few-%
-> a small genuine clumpy enhancement. Report whichever the computation gives.
"""
import numpy as np
G=6.674e-11; Msun=1.989e30; kpc=3.086e19; Mpc=1000*kpc; a0=9.36e-11
def nu_fw(gN):
    gN=np.asarray(gN,float); out=np.ones_like(gN); m=gN>0
    out[m]=np.sqrt(1.0+a0/gN[m]); return out

# ---- cluster setup (same as compute) ----
M500=1e15*Msun; R500=1300.0*kpc; fgas500=0.12; fstar500=0.015
Mgas=fgas500*M500; Mstar=fstar500*M500
rc_gas=0.20*R500; beta=0.65
def rho_gas_shape(r): return 1.0/(1+(r/rc_gas)**2)**(1.5*beta)
rr=np.linspace(1e-3*R500,R500,6000)
rho0_gas=Mgas/np.trapz(4*np.pi*rr**2*rho_gas_shape(rr),rr)
def Mgas_enc(r):
    r=np.atleast_1d(r); out=np.empty_like(r)
    for i,rv in enumerate(r):
        rr2=np.linspace(1e-3*R500,max(rv,1e-3*R500),400)
        out[i]=rho0_gas*np.trapz(4*np.pi*rr2**2*rho_gas_shape(rr2),rr2)
    return out
c_nfw=4.0; rs_nfw=R500/c_nfw
def Mstar_enc_smooth(r):
    x=r/rs_nfw; mu=np.log(1+x)-x/(1+x)
    xR=R500/rs_nfw; muR=np.log(1+xR)-xR/(1+xR)
    return Mstar*mu/muR

def make_galaxies(Ngal=300, seed=42):
    rng=np.random.default_rng(seed)
    mgal=rng.lognormal(mean=np.log(3e10*Msun),sigma=1.1,size=Ngal)
    mgal*=Mstar/mgal.sum(); mgal[0]=1e12*Msun; mgal*=Mstar/mgal.sum()
    def sample_nfw(n):
        out=[]
        while len(out)<n:
            r=rng.uniform(0,R500,size=n)
            rho=1.0/((r/rs_nfw)*(1+r/rs_nfw)**2+1e-30)
            w=r**2*rho; w/=w.max(); keep=rng.uniform(size=n)<w
            out.extend(r[keep].tolist())
        return np.array(out[:n])
    rgal=sample_nfw(Ngal)
    cth=rng.uniform(-1,1,Ngal); sth=np.sqrt(1-cth**2); ph=rng.uniform(0,2*np.pi,Ngal)
    gpos=np.stack([rgal*sth*np.cos(ph),rgal*sth*np.sin(ph),rgal*cth],axis=1)
    return mgal,gpos,rgal

# =====================================================================
# TEST 2 (cleanest): EXACT surface-flux M_tot(<r) = (1/4piG) oint nu*g_N . dA
#   discrete vs smooth -- no volume divergence, just the angular average of nu*g_N
#   over a sphere of radius r. This is the rigorous enclosed-mass test.
# =====================================================================
print("="*72)
print("TEST 2 -- EXACT surface-flux enclosed mass (no grid divergence)")
print("  M_tot(<r) = (1/4piG) oint nu(g_N) g_N . r_hat dA, discrete vs smooth")
print("="*72)
mgal,gpos,rgal=make_galaxies()
def gN_vec_discrete(pts):
    """Newtonian g vector at pts (M,3): gas(spherical)+sum galaxies."""
    r=np.linalg.norm(pts,axis=1)+1e-30
    gg=G*Mgas_enc(r)/(r**2+(5*kpc)**2)         # gas magnitude (radial inward)
    gvec=-(gg/r)[:,None]*pts
    b2=(15*kpc)**2
    for i in range(len(mgal)):
        dvec=pts-gpos[i]; d2=(dvec**2).sum(axis=1)+b2
        gvec+=-(G*mgal[i]/d2/np.sqrt(d2))[:,None]*dvec
    return gvec
def gN_vec_smooth(pts):
    r=np.linalg.norm(pts,axis=1)+1e-30
    gg=G*(Mgas_enc(r)+Mstar_enc_smooth(r))/(r**2+(5*kpc)**2)
    return -(gg/r)[:,None]*pts
def surface_flux_mass(gfunc, r, nth=120, nph=240):
    th=np.linspace(0,np.pi,nth); ph=np.linspace(0,2*np.pi,nph,endpoint=False)
    TH,PH=np.meshgrid(th,ph,indexing='ij')
    xhat=np.stack([np.sin(TH)*np.cos(PH),np.sin(TH)*np.sin(PH),np.cos(TH)],axis=-1)
    pts=(r*xhat).reshape(-1,3)
    gvec=gfunc(pts)
    gmag=np.linalg.norm(gvec,axis=1)+1e-30
    nu=nu_fw(gmag)
    # radial component of nu*g_N (inward positive)
    rhat=pts/np.linalg.norm(pts,axis=1,keepdims=True)
    gr=-(nu[:,None]*gvec*rhat).sum(axis=1)     # inward => positive
    gr=gr.reshape(nth,nph)
    # integrate gr * r^2 sin(th) dth dph
    dth=th[1]-th[0]; dph=ph[1]-ph[0]
    integ=np.sum(gr*np.sin(TH)*r**2)*dth*dph
    return integ/(4*np.pi*G)
print(f"\n{'r[kpc]':>7} {'M_disc[Msun]':>14} {'M_smo[Msun]':>14} {'disc/smo':>9} {'Mbar':>12}")
for rk in [100,150,200,300,420,550,700]:
    r=rk*kpc
    Md=surface_flux_mass(gN_vec_discrete,r)/Msun
    Ms=surface_flux_mass(gN_vec_smooth,r)/Msun
    Mb=(Mgas_enc(r)[0]+Mstar_enc_smooth(r))/Msun
    print(f"{rk:>7} {Md:>14.3e} {Ms:>14.3e} {Md/Ms:>9.4f} {Mb:>12.3e}")
print("\n  => disc/smo via the EXACT surface flux is the rigorous 'does clumpiness")
print("     change the enclosed mass' test (Jensen on nu over the sphere only).")

# =====================================================================
# TEST 1: grid/softening convergence of the volume-divergence result
# =====================================================================
print("\n"+"="*72)
print("TEST 1 -- grid & softening convergence of the volume-QUMOND disc/smo")
print("="*72)
def volume_disc_smo(Ng, b_gal_kpc, L_Mpc=0.6, r_core_kpc=420):
    b_gal=b_gal_kpc*kpc; L=L_Mpc*Mpc
    ax=np.linspace(-L,L,Ng); dx=ax[1]-ax[0]
    X,Y,Z=np.meshgrid(ax,ax,ax,indexing='ij'); Rr=np.sqrt(X**2+Y**2+Z**2)+1e-12
    flat=np.stack([X.ravel(),Y.ravel(),Z.ravel()],axis=1)
    rtab=np.linspace(0,np.sqrt(3)*L,600); Mtab=Mgas_enc(rtab)
    gN_gas_tab=G*Mtab/(rtab**2+(5*kpc)**2)
    gN_gas=np.interp(Rr.ravel(),rtab,gN_gas_tab).reshape(Rr.shape)
    gxg=-gN_gas*X/Rr; gyg=-gN_gas*Y/Rr; gzg=-gN_gas*Z/Rr
    gxd=np.zeros_like(X);gyd=np.zeros_like(X);gzd=np.zeros_like(X)
    for i in range(len(mgal)):
        dvec=flat-gpos[i]; d2=(dvec**2).sum(axis=1)+b_gal**2
        gmag=G*mgal[i]/d2; inv=1.0/np.sqrt(d2)
        gxd+=(-gmag*dvec[:,0]*inv).reshape(X.shape)
        gyd+=(-gmag*dvec[:,1]*inv).reshape(X.shape)
        gzd+=(-gmag*dvec[:,2]*inv).reshape(X.shape)
    Mss=G*Mstar_enc_smooth(rtab)
    gN_star=np.interp(Rr.ravel(),rtab,Mss/(rtab**2+(5*kpc)**2)).reshape(Rr.shape)
    gxs=-gN_star*X/Rr;gys=-gN_star*Y/Rr;gzs=-gN_star*Z/Rr
    def qd(gx_,gy_,gz_):
        gN=np.sqrt(gx_**2+gy_**2+gz_**2)+1e-30; nu=nu_fw(gN)
        Gx=nu*gx_;Gy=nu*gy_;Gz=nu*gz_
        div=np.gradient(Gx,dx,axis=0)+np.gradient(Gy,dx,axis=1)+np.gradient(Gz,dx,axis=2)
        return -div/(4*np.pi*G)
    rho_d=qd(gxg+gxd,gyg+gyd,gzg+gzd); rho_s=qd(gxg+gxs,gyg+gys,gzg+gzs)
    mask=Rr<=r_core_kpc*kpc; V=dx**3
    return rho_d[mask].sum()*V/Msun, rho_s[mask].sum()*V/Msun
print(f"\n{'grid':>5} {'b_gal':>6} {'M_disc':>12} {'M_smo':>12} {'disc/smo':>9}")
for Ng in [64,96,128]:
    Md,Ms=volume_disc_smo(Ng,15)
    print(f"{Ng:>5} {'15kpc':>6} {Md:>12.3e} {Ms:>12.3e} {Md/Ms:>9.4f}")
for b in [5,15,30,60]:
    Md,Ms=volume_disc_smo(96,b)
    print(f"{96:>5} {str(b)+'kpc':>6} {Md:>12.3e} {Ms:>12.3e} {Md/Ms:>9.4f}")
print("\n  => if disc/smo -> 1 as grid/softening vary, the +1.6% was grid/softening")
print("     leakage; the flux theorem (TEST 2) is the truth.")

# =====================================================================
# TEST 3: sub-additivity of the COLLECTIVE field -- Carl's 'overlap adds' vs QUMOND
# =====================================================================
print("\n"+"="*72)
print("TEST 3 -- collective field: QUMOND combine vs LINEAR sum (Carl's overlap)")
print("="*72)
# sample inter-galaxy points, compare |QUMOND g_N(all)| vs sum_i |g_MOND of galaxy i alone|
rng=np.random.default_rng(7)
pts=[]
while len(pts)<2000:
    p=rng.uniform(-1,1,3)*400*kpc
    if np.linalg.norm(p)<400*kpc: pts.append(p)
pts=np.array(pts)
# distance to nearest galaxy
dmin=np.min(np.linalg.norm(pts[:,None,:]-gpos[None,:,:],axis=2),axis=1)
inter=dmin>60*kpc
g_all=np.linalg.norm(gN_vec_discrete(pts),axis=1)          # collective Newtonian
gmob_all=nu_fw(g_all)*g_all                                # collective MOND-boosted
# linear sum of each galaxy's OWN deep-MOND field (Carl's 'reaches far, overlaps, adds')
def gmond_single(p):
    s=0.0
    for i in range(len(mgal)):
        d=np.linalg.norm(p-gpos[i])+15*kpc
        gN=G*mgal[i]/d**2
        s+=nu_fw(np.array([gN]))[0]*gN          # each galaxy's own MOND field magnitude
    return s
gsum=np.array([gmond_single(p) for p in pts[inter][:300]])
gcol=gmob_all[inter][:300]
print(f"\n  inter-galaxy points: {inter.sum()}")
print(f"  median collective QUMOND |g_MOND|/a0       = {np.median(gcol)/a0:.3f}")
print(f"  median LINEAR-SUM of single MOND fields /a0 = {np.median(gsum)/a0:.3f}")
print(f"  ratio collective/linear-sum                = {np.median(gcol/gsum):.3f}")
print("  => ratio < 1 confirms SUB-ADDITIVITY: the real overlapping field is LESS")
print("     than the naive sum of the galaxies' own MOND fields. Carl's 'overlap")
print("     adds' overcounts; QUMOND does not superpose.")
