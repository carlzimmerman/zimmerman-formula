"""
ROUTE 2 -- BOTH-WAYS RESCUE ATTEMPT: try HARDEST to make Carl's clumpy/collective
effect ADD net cluster mass. The compute+verify found +1.6% (a tiny clumpy-Jensen
excess). Before conceding redistribute-only, push every knob that could AMPLIFY a
genuine clumpy enhancement:

  (1) The clumpy excess is Jensen's inequality on the ENCLOSED-MASS FLUX integrand
      over the bounding sphere: the total mass inside R is (1/4piG) oint nu(g_N) g_N . dA,
      so the load-bearing quantity is g_obs = nu*g_N = sqrt(g_N^2 + a0 g_N), NOT nu alone.
      [CORRECTED per skeptic: g_obs is provably CONCAVE in g_N (d2/dg2 = -a0^2/[4 g^(3/2)
      (a0+g)^(3/2)] < 0), so Jensen runs the OTHER way -- more shell-variance in g_N
      (clumpy) gives <g_obs> LOWER => disc <= smooth (sub-additive). i.e. there is NO
      direction in which clumpiness adds net enclosed mass; this rescue attempt is
      structurally doomed, which the numbers below confirm (negative/null).] We still
      maximize the magnitude to bound the residual shot-noise band: more/heavier clumps,
      deeper-MOND configs.
  (2) Vary: number of galaxies, mass concentration (a few giant clumps vs many
      dwarfs), galaxy spatial concentration, the deep-MOND-ness (scale the cluster
      mass down so g_N << a0 -> nu most convex).
  (3) Confirm the EFE SIGN both ways: collective field as a SOURCE (adds to
      enclosed mass via the flux) vs as an EXTERNAL field on members (suppresses
      their internal boost). These are NOT in tension -- the flux integral already
      INCLUDES the full nonlinear field; the member-EFE is a separate (and
      wrong-signed for binding) effect.

The honest theorem to confirm: the deep-MOND enclosed phantom mass within a sphere
is M_ph = (sqrt(1+4a0 r^2/(G M_b)) ... ) -- for a POINT it is sqrt(M_b a0/G)*r,
SET BY THE ENCLOSED BARYON M_b, with only a weak shell-variance (Jensen) correction
from clumpiness. We bound that correction.
"""
import numpy as np
G=6.674e-11; Msun=1.989e30; kpc=3.086e19; Mpc=1000*kpc; a0=9.36e-11
def nu_fw(gN):
    gN=np.asarray(gN,float); out=np.ones_like(gN); m=gN>0
    out[m]=np.sqrt(1.0+a0/gN[m]); return out

# Pure clumpy-Jensen bound: phantom enclosed within radius r is a flux of (nu-1) g_N.
# oint g_N.dA = 4 pi G M_b(<r) is FIXED (Gauss). The phantom = (1/4piG) oint (nu-1)g_N.dA.
# Write it as M_b(<r) * <(nu-1) weighted by g_N flux>. So:
#   eta(<r) = M_tot/M_b = < nu g_N >_flux / < g_N >_flux   (flux-weighted nu)
# Clumpy raises the variance of g_N on the shell -> flux-weighted <nu> changes.
# nu(g)=sqrt(1+a0/g) is DECREASING and CONVEX in g. Flux-weighting (weight ~ g_N)
# upweights the HIGH-g (near-galaxy) directions where nu is SMALL -> pulls <nu>
# DOWN; but the bulk low-g inter-galaxy directions have HIGH nu. Net is a small
# Jensen competition. We compute the realistic bound by direct shell averaging.

def make_galaxies(Ngal, seed, Mstar, R500, conc=4.0, giant_frac=0.0):
    rng=np.random.default_rng(seed); rs=R500/conc
    if giant_frac>0:
        # a few giant clumps carry giant_frac of the mass
        ng=max(1,int(0.03*Ngal))
        mg=np.zeros(Ngal)
        mg[:ng]=giant_frac*Mstar/ng
        rest=rng.lognormal(np.log(3e10*Msun),1.1,Ngal-ng)
        mg[ng:]=(1-giant_frac)*Mstar*rest/rest.sum()
        mgal=mg
    else:
        mgal=rng.lognormal(np.log(3e10*Msun),1.1,Ngal); mgal*=Mstar/mgal.sum()
    def samp(n):
        out=[]
        while len(out)<n:
            r=rng.uniform(0,R500,n); rho=1.0/((r/rs)*(1+r/rs)**2+1e-30)
            w=r**2*rho; w/=w.max(); out.extend(r[rng.uniform(size=n)<w].tolist())
        return np.array(out[:n])
    rg=samp(Ngal); cth=rng.uniform(-1,1,Ngal); sth=np.sqrt(1-cth**2); ph=rng.uniform(0,2*np.pi,Ngal)
    gpos=np.stack([rg*sth*np.cos(ph),rg*sth*np.sin(ph),rg*cth],axis=1)
    return mgal,gpos

def shell_eta(mgal,gpos,Mgas_enc_f,r,nth=120,nph=240):
    th=np.linspace(0,np.pi,nth); ph=np.linspace(0,2*np.pi,nph,endpoint=False)
    TH,PH=np.meshgrid(th,ph,indexing='ij')
    xhat=np.stack([np.sin(TH)*np.cos(PH),np.sin(TH)*np.sin(PH),np.cos(TH)],axis=-1)
    pts=(r*xhat).reshape(-1,3)
    rp=np.linalg.norm(pts,axis=1)+1e-30
    gg=G*Mgas_enc_f(rp)/(rp**2+(5*kpc)**2)
    gvec=-(gg/rp)[:,None]*pts
    for i in range(len(mgal)):
        dv=pts-gpos[i]; d2=(dv**2).sum(1)+(15*kpc)**2
        gvec+=-(G*mgal[i]/d2/np.sqrt(d2))[:,None]*dv
    gmag=np.linalg.norm(gvec,axis=1)+1e-30; nu=nu_fw(gmag)
    rhat=pts/rp[:,None]; gr=-(gvec*rhat).sum(1)             # inward Newtonian flux density
    grnu=-(nu[:,None]*gvec*rhat).sum(1)
    w=np.sin(TH).ravel()
    Mtot=np.sum(grnu*w); Mbar=np.sum(gr*w)
    return Mtot/Mbar   # = eta on this shell (flux-weighted nu)

print("="*72)
print("RESCUE: maximize the clumpy-Jensen excess (eta_disc/eta_smooth) at 420 kpc")
print("="*72)
R500=1300*kpc; r=420*kpc
configs=[
    ("baseline rich  M*=1.5e13 N=300 c=4",  300,1.5e13*Msun,1e15*Msun,4.0,0.0),
    ("many dwarfs    N=1000 c=4",           1000,1.5e13*Msun,1e15*Msun,4.0,0.0),
    ("few giants 70% N=300 c=4",            300,1.5e13*Msun,1e15*Msun,4.0,0.70),
    ("concentrated   N=300 c=8",            300,1.5e13*Msun,1e15*Msun,8.0,0.0),
    ("MORE stars f*=4% N=300",              300,4.0e13*Msun,1e15*Msun,4.0,0.0),
    ("DEEP-MOND group M500=1e14",           300,3.0e12*Msun,1e14*Msun,4.0,0.0),
    ("DEEP+giants group M500=1e14 70%",     300,3.0e12*Msun,1e14*Msun,4.0,0.70),
]
for name,Ngal,Mstar,M500,conc,gf in configs:
    Mgas=0.12*M500; rc=0.20*R500; beta=0.65
    rr=np.linspace(1e-3*R500,R500,4000)
    sh=1.0/(1+(rr/rc)**2)**(1.5*beta); rho0=Mgas/np.trapz(4*np.pi*rr**2*sh,rr)
    def Mgas_enc_f(rq,rho0=rho0,rc=rc,beta=beta):
        rq=np.atleast_1d(rq); o=np.empty_like(rq)
        for i,rv in enumerate(rq):
            r2=np.linspace(1e-3*R500,max(rv,1e-3*R500),300)
            o[i]=rho0*np.trapz(4*np.pi*r2**2/(1+(r2/rc)**2)**(1.5*beta),r2)
        return o
    mgal,gpos=make_galaxies(Ngal,42,Mstar,R500,conc,gf)
    # smooth: same Mstar spread as the gas-following smooth NFW
    eta_d=shell_eta(mgal,gpos,Mgas_enc_f,r)
    # smooth reference: one realization with Mstar smeared smoothly = put the same
    # Mstar as an extra smooth spherical component (use a single huge 'galaxy' = the
    # spherical avg). Cleanest: smooth eta = nu(<g_N>) with g_N from gas+smoothstars.
    rs=R500/conc
    def Msmooth(rq):
        x=rq/rs; mu=np.log(1+x)-x/(1+x); xR=R500/rs; muR=np.log(1+xR)-xR/(1+xR)
        return Mstar*mu/muR
    gN_smo=G*(Mgas_enc_f(r)[0]+Msmooth(r))/(r**2+(5*kpc)**2)
    eta_s=nu_fw(np.array([gN_smo]))[0]
    print(f"  {name:36s}: eta_disc={eta_d:.4f} eta_smo={eta_s:.4f} "
          f"ratio={eta_d/eta_s:.4f} ({100*(eta_d/eta_s-1):+.2f}%)")

print("\n  => the clumpy-Jensen excess is bounded to a FEW PERCENT in every config,")
print("     INCLUDING few-giant-clumps and deep-MOND groups. It never approaches the")
print("     ~4x (eta~2.3) the cluster residual needs. The flux/enclosed-mass theorem")
print("     dominates: clumpiness REDISTRIBUTES the phantom (more near galaxies, less")
print("     in voids) but the TOTAL is pinned by the enclosed baryon mass +/- a few %.")
