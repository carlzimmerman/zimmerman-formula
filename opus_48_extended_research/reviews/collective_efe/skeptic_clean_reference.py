"""
SKEPTIC clean-reference adjudication of route 'collective_efe'.

The verdict hinges on disc/smo at 420 kpc. Three of the repo's methods give
DIFFERENT signs at baseline:
  - volume grid QUMOND  : +1.6%   (smooth = gas + Mstar NFW c=4)
  - surface flux        : +1.6%   (smooth = gas + Mstar NFW c=4)
  - Jensen shell_eta    : -0.67%  (smooth = nu(<g_N>) at the spherical field)

The discrepancy is the SMOOTH REFERENCE. The honest enclosed-mass test must hold
ONE thing fixed: the enclosed BARYON mass M_b(<r) at the bounding sphere. Then
eta(<r) = (1/M_b) * (1/4piG) oint nu(g_N) g_N . dA. The ONLY difference disc vs
smooth is the ANGULAR VARIANCE of g_N on the shell. So the cleanest, ambiguity-free
smooth reference is the EXACT SPHERICAL AVERAGE of the SAME discrete baryon mass:
M_b(<r) identical by construction, field made spherical. Anything else (assuming an
NFW c=4 for the smooth stars when the discrete stars are NOT drawn to match that
enclosed profile at r) injects a baryon-mass mismatch that masquerades as a
'collective effect'.

I rebuild it three ways and report whether the +1.6% survives a baryon-matched
smooth reference, or whether it was a profile-mismatch artifact.
"""
import numpy as np
G=6.674e-11; Msun=1.989e30; kpc=3.086e19; Mpc=1000*kpc; a0=9.36e-11
def nu_fw(gN):
    gN=np.asarray(gN,float); out=np.ones_like(gN); m=gN>0
    out[m]=np.sqrt(1.0+a0/gN[m]); return out

# ---- identical cluster setup to the repo ----
M500=1e15*Msun; R500=1300.0*kpc
Mgas=0.12*M500; Mstar=0.015*M500
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

mgal,gpos,rgal=make_galaxies()
b2=(15*kpc)**2

def gN_vec_discrete(pts):
    r=np.linalg.norm(pts,axis=1)+1e-30
    gg=G*Mgas_enc(r)/(r**2+(5*kpc)**2)
    gvec=-(gg/r)[:,None]*pts
    for i in range(len(mgal)):
        dvec=pts-gpos[i]; d2=(dvec**2).sum(axis=1)+b2
        gvec+=-(G*mgal[i]/d2/np.sqrt(d2))[:,None]*dvec
    return gvec

# ---- the ACTUAL discrete enclosed stellar mass (what the smooth ref MUST match) ----
def Mstar_enc_discrete(r):
    return mgal[rgal<=r].sum()

# ---- smooth reference #A: ASSUMED NFW c=4 (what the repo used) ----
def Mstar_enc_nfw(r):
    x=r/rs_nfw; mu=np.log(1+x)-x/(1+x)
    xR=R500/rs_nfw; muR=np.log(1+xR)-xR/(1+xR)
    return Mstar*mu/muR

# ---- smooth reference #B: baryon-MATCHED (exact spherical avg of the SAME mass) ----
# spherical smooth field uses the ACTUAL discrete enclosed stellar mass at r
def gN_vec_smooth_matched(pts):
    r=np.linalg.norm(pts,axis=1)+1e-30
    Ms=np.array([Mstar_enc_discrete(rv) for rv in r])
    gg=G*(Mgas_enc(r)+Ms)/(r**2+(5*kpc)**2)
    return -(gg/r)[:,None]*pts
def gN_vec_smooth_nfw(pts):
    r=np.linalg.norm(pts,axis=1)+1e-30
    gg=G*(Mgas_enc(r)+Mstar_enc_nfw(r))/(r**2+(5*kpc)**2)
    return -(gg/r)[:,None]*pts

def surface_flux_mass(gfunc, r, nth=160, nph=320):
    th=np.linspace(0,np.pi,nth); ph=np.linspace(0,2*np.pi,nph,endpoint=False)
    TH,PH=np.meshgrid(th,ph,indexing='ij')
    xhat=np.stack([np.sin(TH)*np.cos(PH),np.sin(TH)*np.sin(PH),np.cos(TH)],axis=-1)
    pts=(r*xhat).reshape(-1,3)
    gvec=gfunc(pts); gmag=np.linalg.norm(gvec,axis=1)+1e-30; nu=nu_fw(gmag)
    rhat=pts/np.linalg.norm(pts,axis=1,keepdims=True)
    gr=-(nu[:,None]*gvec*rhat).sum(axis=1)
    gr=gr.reshape(nth,nph)
    dth=th[1]-th[0]; dph=ph[1]-ph[0]
    return np.sum(gr*np.sin(TH)*r**2)*dth*dph/(4*np.pi*G)

print("="*78)
print("SKEPTIC: disc/smo at the bounding sphere -- WHICH smooth reference?")
print("  The enclosed-mass test requires the SAME enclosed baryon mass at r.")
print("="*78)
print(f"\n{'r[kpc]':>6} {'Mb_disc*':>11} {'Mb_nfw*':>11} {'ratio_b':>8}  "
      f"{'disc/NFW':>9} {'disc/MATCH':>11}")
for rk in [100,150,200,300,420,550,700]:
    r=rk*kpc
    Md   = surface_flux_mass(gN_vec_discrete, r)/Msun
    Snfw = surface_flux_mass(gN_vec_smooth_nfw, r)/Msun
    Smat = surface_flux_mass(gN_vec_smooth_matched, r)/Msun
    Mb_disc = Mstar_enc_discrete(r)/Msun
    Mb_nfw  = Mstar_enc_nfw(r)/Msun
    print(f"{rk:>6} {Mb_disc:>11.3e} {Mb_nfw:>11.3e} {Mb_disc/Mb_nfw:>8.4f}  "
          f"{Md/Snfw:>9.4f} {Md/Smat:>11.4f}")

print("\nKEY: 'ratio_b' = discrete enclosed STELLAR mass / assumed-NFW stellar mass.")
print("  If ratio_b != 1 at r, the NFW smooth ref has a DIFFERENT baryon mass than")
print("  the discrete cluster -> disc/NFW mixes a real Jensen term with a baryon")
print("  MISMATCH. disc/MATCH holds baryon mass fixed -> the PURE clumpy Jensen term.")
print("  Whichever sign disc/MATCH has at 420 kpc is the honest collective effect.")
