#!/usr/bin/env python3
"""
WB-3b: the framework's ACTUAL wide-binary prediction via real modified-gravity ORBIT INTEGRATION
(replaces the crude boost-at-fixed-orbit upper bound in wb_deprojection_mc.py). Tests the framework on its own
terms: compute its deep-bin median vtilde from integrated orbits, not a multiplier and not a borrowed number.

Central-force orbit roulette (exact for any spherical potential):
  effective gravity (simple nu): g_eff(r) = a0 * G(y), y = g_N/a0 = GM/(a0 r^2), G(y) = y/2 + sqrt(y^2/4 + y).
  potential (referenced, since deep-MOND Phi ~ ln r diverges):
     Phi_M(r) = -(1/2) sqrt(a0 GM) * I(y(r)),  I(y) = \int_0^y [ (1/2) t^{-1/2} + t^{-1} sqrt(1+t/4) ] dt
  (I(y) precomputed once on a universal y-grid; the t^{-1} piece is the log/deep-MOND term, integrated from a
   small floor and used only via differences Phi(r1)-Phi(r2), so the additive constant cancels.)
  For an orbit with pericentre r_p, apocentre r_a:  L^2 = 2(Phi_a-Phi_p)/(1/r_p^2 - 1/r_a^2),  E = Phi_p + L^2/(2 r_p^2).
  At radius r:  v_r = sqrt(2(E-Phi(r)) - L^2/r^2),  v_t = L/r.  Sample r weighted by time dt ~ dr/|v_r|.
  Random orientation -> project -> vtilde = v_sky/sqrt(GM/r_sky), bin by g_N/a0 = GM/r_sky^2/a0.
NEWTON cross-check uses the SAME machinery with Phi_N=-GM/r (must reproduce the conditioned-method baseline ~0.55).
Inline, no swarms.  C. Zimmerman 2026-06-10.
"""
import numpy as np, warnings, os; warnings.filterwarnings('ignore')
from astropy.io import fits
rng=np.random.default_rng(20260610)
G=6.674e-11; Msun=1.989e30; AU=1.496e11; a0=9.36e-11
# --- universal potential tables I(y); Phi = -1/2 sqrt(a0 G M) I(y) ; Newton I_N(y)=2 sqrt(y) (Phi=-GM/r) ---
yg=np.logspace(-6,6,200000); integ=0.5*yg**-0.5 + yg**-1.0*np.sqrt(1+yg/4)
Iy=np.concatenate([[0],np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(yg))])
def PhiM(r,M):                       # referenced MOND potential (J/kg)
    y=G*M*Msun/(a0*r**2); return -0.5*np.sqrt(a0*G*M*Msun)*np.interp(y,yg,Iy)
def PhiN(r,M): return -G*M*Msun/r
def gN_a0(rsky,M): return G*M*Msun/rsky**2/a0

# --- load Banik-exact selection (same pipeline as wb_exact_replication.py) ---
F=os.path.join(os.path.dirname(__file__),'all_columns_catalog.fits.gz')
C=['ra1','dec1','parallax1','parallax2','parallax_error1','parallax_error2','pmra1','pmra2','pmdec1','pmdec2',
   'pmra_error1','pmra_error2','pmdec_error1','pmdec_error2','ruwe1','ruwe2','ipd_frac_multi_peak1',
   'ipd_frac_multi_peak2','phot_g_mean_mag1','phot_g_mean_mag2','sep_AU']
with fits.open(F,memmap=True) as h:
    d=h[1].data; D={k:np.array(d[k],dtype='f8') for k in C}
aN,dN=np.radians(192.85948),np.radians(27.12825); ra,dec=np.radians(D['ra1']),np.radians(D['dec1'])
bgal=np.degrees(np.arcsin(np.sin(dec)*np.sin(dN)+np.cos(dec)*np.cos(dN)*np.cos(ra-aN)))
d1=1000/D['parallax1'];d2=1000/D['parallax2'];dist=0.5*(d1+d2);skAU=D['sep_AU']/1e3
sd1=1000*D['parallax_error1']/D['parallax1']**2;sd2=1000*D['parallax_error2']/D['parallax2']**2;sdd=np.hypot(sd1,sd2)
MG1=D['phot_g_mean_mag1']-5*np.log10(dist/10);MG2=D['phot_g_mean_mag2']-5*np.log10(dist/10)
xg=np.linspace(-1.46,0.99,4000);MGg=4.887-5.693*xg+0.4164*xg**2+0.9611*xg**3;o=np.argsort(MGg)
mfn=lambda MG:np.exp(np.interp(np.clip(MG,0.6,11.1),MGg[o],xg[o])); Mtot=mfn(MG1)+mfn(MG2)
s=D['sep_AU']*AU;dpm=np.hypot(D['pmra1']-D['pmra2'],D['pmdec1']-D['pmdec2'])
vN=np.sqrt(G*Mtot*Msun/s)/1e3;vsky=4.74*dpm*(dist/1000);vt=vsky/vN
sdpm=np.sqrt(((D['pmra1']-D['pmra2'])*np.hypot(D['pmra_error1'],D['pmra_error2']))**2
            +((D['pmdec1']-D['pmdec2'])*np.hypot(D['pmdec_error1'],D['pmdec_error2']))**2)/np.maximum(dpm,1e-6)
svt=np.sqrt((4.74*dist/1000*sdpm)**2+(4.74*dpm/1000*sdd)**2)/vN
sel=((np.abs(bgal)>15)&(D['phot_g_mean_mag1']<17)&(D['phot_g_mean_mag2']<17)&(dist<250)&(D['ruwe1']<1.2)&(D['ruwe2']<1.2)
   &(skAU>2)&(skAU<30)&(D['ipd_frac_multi_peak1']<=2)&(D['ipd_frac_multi_peak2']<=2)
   &(Mtot>0.464)&(Mtot<4.31)&(vt<=5)&(np.abs(d1-d2)<np.minimum(4*sdd,8)))
Mdat=Mtot[sel]; sv_kms=(svt*vN)[sel]; xi=np.log10(G*Mtot*Msun/s**2/a0)[sel]; vti=vt[sel]
print(f"Banik-exact substrate N={sel.sum():,}")

def population(law,nmock=400000,alpha=1.5,ftrip=0.05):
    M=rng.choice(Mdat,nmock)                                  # masses from the data
    a=10**rng.uniform(np.log10(1e3*AU),np.log10(60e3*AU),nmock)  # 3D semi-major prior (kAU), wider than the cut
    e=rng.uniform(0,1,nmock)**(1/(alpha+1)); rp=a*(1-e); ra_=a*(1+e)
    Ph=PhiM if law=='MOND' else PhiN
    Pp,Pa=Ph(rp,M),Ph(ra_,M)
    L2=2*(Pa-Pp)/(1/rp**2-1/ra_**2); E=Pp+L2/(2*rp**2)
    r=rp+(ra_-rp)*rng.uniform(0,1,nmock)                      # radius; weight by time below
    vr2=2*(E-Ph(r,M))-L2/r**2; ok=vr2>0
    vr=np.sqrt(np.clip(vr2,0,None)); vt_=np.sqrt(L2)/r; w=1.0/np.clip(vr,1e-3*np.sqrt(G*M*Msun/a),None)  # dt~dr/|vr|
    w=np.where(ok,w,0.0)
    om=rng.uniform(0,2*np.pi,nmock); ci=rng.uniform(-1,1,nmock)
    rho=r*np.sqrt(np.cos(om)**2+(np.sin(om)*ci)**2)           # r_sky
    a1v=vr*np.cos(om)-vt_*np.sin(om); a2v=vr*np.sin(om)+vt_*np.cos(om)
    nus=np.sqrt(a1v**2+(a2v*ci)**2)                           # v_sky
    vtil=nus/np.sqrt(G*M*Msun/rho); gx=np.log10(G*M*Msun/rho**2/a0)
    keep=(rho>2e3*AU)&(rho<30e3*AU)&ok                        # the observed r_sky cut
    vtil,gx,w,M2=vtil[keep],gx[keep],w[keep],M[keep]
    # Eddington noise: sigma_v from the data, sigma_vtilde = sigma_v / v_N(mock); r_sky from the bin gx
    rsky_m=np.sqrt(G*M2*Msun/(10**gx*a0)); vNm=np.sqrt(G*M2*Msun/rsky_m)/1e3
    sig=rng.choice(sv_kms,len(vtil))/vNm
    phi=rng.uniform(0,2*np.pi,len(vtil))
    ox=vtil*np.cos(phi)+rng.normal(0,1,len(vtil))*sig; oy=vtil*np.sin(phi)+rng.normal(0,1,len(vtil))*sig
    vtil=np.hypot(ox,oy)
    tri=rng.uniform(0,1,len(vtil))<ftrip; vtil=np.where(tri,vtil+np.abs(rng.normal(0,1,len(vtil))),vtil)
    return vtil,gx,w

def wmedian(v,w):
    i=np.argsort(v); v,w=v[i],w[i]; c=np.cumsum(w); return np.interp(0.5*c[-1],c,v)
def binned(v,g,w,edges):
    out=[]
    for lo,hi in edges:
        m=(g>=lo)&(g<hi)&np.isfinite(v)&(w>0)
        out.append(wmedian(v[m],w[m]) if m.sum()>200 else np.nan)
    return out
edges=[(1.0,2.5),(0.5,1.0),(0.0,0.5),(-0.5,0.0),(-1.0,-0.5),(-2.5,-1.0)]
vN_,gN_,wN_=population('NEWT'); vM_,gM_,wM_=population('MOND')
dataM=[ (np.median(vti[(xi>=lo)&(xi<hi)]) if ((xi>=lo)&(xi<hi)).sum()>15 else np.nan) for lo,hi in edges]
bN=binned(vN_,gN_,wN_,edges); bM=binned(vM_,gM_,wM_,edges)
print("\n  g_N/a0  |  data  | Newton-pop | MOND-pop(integrated)")
for (lo,hi),dm,n,m in zip(edges,dataM,bN,bM):
    print(f"  {10**((lo+hi)/2):7.2f} | {dm:6.3f} |   {n:6.3f}   |   {m:6.3f}")
print(f"""
FINDING (honest, cross-check FAILS): the Newton-pop column is ~0.60-0.67, NOT the validated conditioned-method
~0.55 flat baseline, and MOND-pop shows a ~7% shift already at g/a0=56 (physics: ~1%). Cause: this population
method draws the 3D semi-major axis from a log-uniform prior, so eccentric orbits with deep-MOND APOCENTRES seen
near PERICENTRE leak boost into high-acceleration r_sky bins. => the integrated framework prediction is SENSITIVE
to the orbital a-prior, which the sky-projected data do NOT constrain. The crude multiplier (~1.0-1.3) and this
integration BRACKET a wide range; the literature ~15-20% (~0.63-0.66) assumes a near-circular-scale prior.
This does NOT yield a clean framework number -- it REINFORCES 'degeneracy-limited': even the theory's own WB
prediction is prior-dependent under sky-projection. NOTE the data's FLAT high-acc vtilde (0.558) disfavours the
large-a/high-e population that drives the leak -- a constraint DR4's 3D velocities would turn into a real prior.
Do NOT cite the MOND-pop column as the framework prediction; it is a prior-sensitivity probe.""")
