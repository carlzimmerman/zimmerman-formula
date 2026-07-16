#!/usr/bin/env python3
"""
G2 -- THE LOAD-BEARING TEST: does the fixed-direction s_TX fit actually separate from the
per-asteroid orbit fit, and by how much (the degeneracy efficiency)? Does it scale as sqrt(N)?
Is Yarkovsky separable? Measured by a linearized Fisher-matrix simulation on realistic orbits.

Physics (Bailey-Kostelecky 2006, Eq.107 + Table 2): s_TX enters an orbit as a SECULAR perihelion
precession whose amplitude is s01 = cos(Omega)*s_TX + sin(Omega)*s_TY (Omega = node longitude in
the CMB frame). So different asteroids project the fixed s_TX vector differently -> the correlated
cos(Omega)/sin(Omega) pattern across N asteroids is what the global fit isolates from each object's
own 6 orbital elements. We inject that signal, fit (6 elements/asteroid) + (global s_TX,s_TY),
marginalize the elements per asteroid (Schur complement), and read sigma(s_TX).

Robust outputs (independent of the absolute B-K normalization K):
  (1) DEGENERACY EFFICIENCY  eff = sigma_ideal / sigma_marginalized  (1 = no loss; <<1 = eaten)
  (2) sqrt(N) SCALING of sigma(s_TX)
  (3) YARKOVSKY SEPARABILITY: add a per-asteroid da/dt nuisance, re-check sigma(s_TX) inflation
Absolute sigma is then anchored to the analytic B-K/Hees scale separately (g3).
"""
import numpy as np
rng = np.random.default_rng(20260706)

AU=1.496e11; yr=365.25*86400; GMsun=1.327e20
Tbase=2.8*yr; Nobs=148                 # Gaia DR3 real: baseline + mean obs/asteroid
sigma_mas=0.5; sigma_rad=sigma_mas*(1e-3/3600)*np.pi/180   # per-obs along-scan noise

def kepler_E(M,e,it=60):
    E=M.copy()
    for _ in range(it): E=E-(E-e*np.sin(E)-M)/(1-e*np.cos(E))
    return E

def sky_xyz(elem, t, sTX, sTY, dadt=0.0, K=1.0):
    """Heliocentric ecliptic position of an asteroid at times t, with s_TX perihelion
       precession (secular) and optional Yarkovsky da/dt. Returns unit-vector angles (lon,lat)
       as seen geocentrically (asteroid - Earth)."""
    a,e,inc,Om,w0,M0 = elem
    n=np.sqrt(GMsun/a**3)
    # s_TX secular perihelion precession: wdot = K*n*(cosOm*sTX + sinOm*sTY)
    wdot = K*n*(np.cos(Om)*sTX + np.sin(Om)*sTY)
    w = w0 + wdot*t
    a_t = a + dadt*t                     # Yarkovsky drift in semi-major axis
    n_t=np.sqrt(GMsun/a_t**3)
    M = M0 + n_t*t
    E=kepler_E(M% (2*np.pi), e)
    # perifocal
    xp=a_t*(np.cos(E)-e); yp=a_t*np.sqrt(1-e**2)*np.sin(E)
    cO,sO=np.cos(Om),np.sin(Om); ci,si=np.cos(inc),np.sin(inc); cw,sw=np.cos(w),np.sin(w)
    x=(cO*cw-sO*sw*ci)*xp+(-cO*sw-sO*cw*ci)*yp
    y=(sO*cw+cO*sw*ci)*xp+(-sO*sw+cO*cw*ci)*yp
    z=(sw*si)*xp+(cw*si)*yp
    # Earth (circular, 1 AU ecliptic)
    lam_E=2*np.pi*t/yr
    xe=AU*np.cos(lam_E); ye=AU*np.sin(lam_E); ze=0.0
    dx,dy,dz=x-xe,y-ye,z-ze
    r=np.sqrt(dx**2+dy**2+dz**2)
    lon=np.arctan2(dy,dx); lat=np.arcsin(dz/r)
    return lon,lat

def design_and_fisher(elem, t, sTX0, sTY0, include_yark=False, K=1.0):
    """Numerical partials of (lon,lat) wrt [6 elements (+dadt)] and [sTX,sTY]; per-asteroid Fisher."""
    a,e,inc,Om,w0,M0=elem
    base=lambda p_el,stx,sty,dd: sky_xyz(p_el,t,stx,sty,dd,K)
    lon0,lat0=base(elem,sTX0,sTY0,0.0)
    cols=[]
    steps=[a*1e-6, 1e-6, 1e-6, 1e-6, 1e-6, 1e-6]   # element steps
    for k in range(6):
        ep=list(elem); ep[k]+=steps[k]
        lo,la=base(ep,sTX0,sTY0,0.0)
        # wrap-safe longitude diff
        dlon=((lo-lon0+np.pi)%(2*np.pi))-np.pi
        cols.append(np.concatenate([dlon/steps[k],(la-lat0)/steps[k]]))
    if include_yark:
        dd=1.0*AU/(1e6*yr)   # small da/dt step (~1 AU/Myr, realistic Yarkovsky)
        lo,la=base(elem,sTX0,sTY0,dd)
        dlon=((lo-lon0+np.pi)%(2*np.pi))-np.pi
        cols.append(np.concatenate([dlon/dd,(la-lat0)/dd]))
    # global s_TX, s_TY partials
    ds=1e-9
    for stx,sty in [(sTX0+ds,sTY0),(sTX0,sTY0+ds)]:
        lo,la=base(elem,stx,sty,0.0)
        dlon=((lo-lon0+np.pi)%(2*np.pi))-np.pi
        cols.append(np.concatenate([dlon/ds,(la-lat0)/ds]))
    A=np.array(cols).T                    # (2*Nobs, nparam)
    F=A.T@A/sigma_rad**2
    return F

def run(N, include_yark=False, K=1.0):
    nloc = 7 if include_yark else 6
    Fss=np.zeros((2,2)); Fss_ideal=np.zeros((2,2))
    for _ in range(N):
        a=rng.uniform(2.1,3.3)*AU; e=rng.uniform(0.02,0.30); inc=np.radians(rng.uniform(1,25))
        Om=rng.uniform(0,2*np.pi); w0=rng.uniform(0,2*np.pi); M0=rng.uniform(0,2*np.pi)
        t=np.sort(rng.uniform(0,Tbase,Nobs))
        F=design_and_fisher([a,e,inc,Om,w0,M0], t, 0.0,0.0, include_yark, K)
        Floc=F[:nloc,:nloc]; Fls=F[:nloc,nloc:]; Fs=F[nloc:,nloc:]
        # Schur complement: marginalize local nuisances
        Fmarg = Fs - Fls.T@np.linalg.solve(Floc+1e-30*np.eye(nloc),Fls)
        Fss+=Fmarg; Fss_ideal+=Fs
    cov=np.linalg.inv(Fss); cov_id=np.linalg.inv(Fss_ideal)
    return np.sqrt(cov[0,0]), np.sqrt(cov_id[0,0])

if __name__=="__main__":
    print("="*76)
    print("G2 Fisher prototype -- degeneracy efficiency, sqrt(N) scaling, Yarkovsky (K=1 units)")
    print(f"  Gaia DR3 real: baseline {Tbase/yr:.1f} yr, {Nobs} obs/asteroid, {sigma_mas} mas noise")
    print("="*76)
    print(f"  {'N_ast':>6} {'sigma(sTX)_marg':>16} {'sigma_ideal':>12} {'degeneracy eff':>15}")
    prev=None
    for N in [100,400,1600,6400]:
        sm,si=run(N)
        eff=si/sm
        scale=f"(x{prev/sm:.2f} vs prev, sqrt(4)=2.0)" if prev else ""
        print(f"  {N:6d} {sm:16.3e} {si:12.3e} {eff:15.3f}   {scale}")
        prev=sm
    print()
    smY,siY=run(1600, include_yark=True)
    sm0,si0=run(1600, include_yark=False)
    print(f"  YARKOVSKY test (N=1600): sigma(sTX) without da/dt = {sm0:.3e}, "
          f"with da/dt nuisance = {smY:.3e}  -> inflation x{smY/sm0:.2f}")
    print()
    print("READ: eff~1 => the fixed-direction pattern cleanly separates from orbital elements;")
    print("      eff<<1 => the orbit fit eats the signal. sqrt(N) scaling => statistics stack.")
    print("      Yarkovsky inflation ~1 => separable; >>1 => it's the systematic floor.")
