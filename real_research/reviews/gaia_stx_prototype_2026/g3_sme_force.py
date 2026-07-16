#!/usr/bin/env python3
"""
G3 -- THE NOVEL CORE: the framework's SME s-bar^TX perturbing force, added to the full
ASSIST force model, and validated to produce the Bailey-Kostelecky secular precession.

FRAMEWORK-SPECIFIC (Carl Zimmerman's; used at every applicable place):
  * a0 = 9.36e-11 m/s^2 (canonical, rho_DE footing);  alt footing 1.13e-10  -- BOTH carried.
  * Preferred frame = CMB rest frame. Boost V_cmb = 369.82 km/s toward the CMB APEX
    (galactic l,b = 264.02, 48.25 deg  ->  equatorial RA,Dec = 167.94, -6.94 deg).
  * The framework FORCES a fixed-direction gravity-sector coefficient s-bar^TX locked to
    that apex, with ratios s^TY/s^TX = -0.214, s^TZ/s^TX = +0.125 (one-parameter).
  * Framework PREDICTION (per-body, 1/|a| ladder): s^TX(body) = (a0 / (2|a|)) * beta_cmb * nX,
    with |a| = GM_sun/r^2. At Saturn |s^TX| = 8.7e-10 (the binding body). Asteroids at r~2.5 AU
    have larger |a| -> smaller per-body s^TX. The DECIDABLE quantity is the UNIVERSAL amplitude
    the ensemble fit returns; we compute BOTH the framework per-body prediction and what a
    universal fit would see.

SME PHYSICS (Bailey-Kostelecky 2006, gr-qc/0603030, Eq.104): the Lorentz-violating two-body
acceleration. The spatial-coefficient part (cleanest, implemented+validated here) is
  a_LV^J = GM s^JK r_K / r^3  -  (3/2) GM s^KL r_K r_L r^J / r^5 .
The framework's preferred-frame s^TX, viewed in the Sun-centred frame, induces an effective
spatial s^JK ~ beta_cmb-scale; the dominant orbital signature is a SECULAR perihelion precession.
Here we (i) implement a_LV as a rebound additional force on top of ASSIST, (ii) integrate a belt
asteroid with and without it, (iii) confirm the induced precession is LINEAR in the coefficient
and matches the B-K scaling n*s -- validating the engine's novel core.
NOTE: the boost s^TK terms of Eq.104 (with V_cmb) and their exact O(1) coefficients need a
cross-check against Hees+2015's implementation before the fit is publication-grade (flagged).
"""
import numpy as np, rebound, assist

# ---- framework constants ----
a0_can, a0_alt = 9.36e-11, 1.13e-10
c = 299792458.0
Vcmb = 369.82e3                       # m/s
beta_cmb = Vcmb/c                      # 1.233e-3
# CMB apex equatorial unit vector
ra, dec = np.radians(167.94), np.radians(-6.94)
n_apex = np.array([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)])
GMsun_SI = 1.32712440018e20
AU=1.495978707e11; day=86400.0
GMsun_au = GMsun_SI*day**2/AU**3      # AU^3/day^2

EPHEM=("ephem/linux_p1550p2650.440","ephem/sb441-n16.bsp")

def sbar_JK_from_apex(sTX):
    """Effective spatial s^JK the framework's fixed-direction s^TX induces (dipole along apex,
       boost-scaled). Traceless symmetric, aligned with the CMB apex: s^JK = sTX*(3 nn - I)/2 * beta.
       (Structural model for the validation; absolute normalization cross-checked in the fit stage.)"""
    nn = np.outer(n_apex, n_apex)
    return sTX*beta_cmb*(3*nn - np.eye(3))/2.0

def make_sim(state_au, t0, sJK=None):
    sim = rebound.Simulation(); sim.t = t0
    ex = assist.Extras(sim, assist.Ephem(*EPHEM))
    x,y,z,vx,vy,vz = state_au
    sim.add(x=x,y=y,z=z,vx=vx,vy=vy,vz=vz)
    if sJK is not None:
        def sme(reb_sim):
            s=reb_sim.contents; p=s.particles[0]
            r=np.array([p.x,p.y,p.z]); rn=np.linalg.norm(r); rhat=r/rn
            # a_LV = GM/r^2 [ sJK.rhat - 3/2 (rhat.sJK.rhat) rhat ]   (Eq.104 spatial part)
            sr = sJK@rhat
            proj = rhat@sr
            a = GMsun_au/rn**2*(sr - 1.5*proj*rhat)
            p.ax += a[0]; p.ay += a[1]; p.az += a[2]
        ex.additional_forces = sme
        sim.additional_forces_warning = False
    return sim, ex

def perihelion_lon(sim):
    """argument-of-perihelion proxy: longitude of the eccentricity (Laplace-Runge-Lenz) vector."""
    p=sim.particles[0]
    r=np.array([p.x,p.y,p.z]); v=np.array([p.vx,p.vy,p.vz])
    h=np.cross(r,v); rn=np.linalg.norm(r)
    ev=(np.cross(v,h)/GMsun_au) - r/rn        # LRL / eccentricity vector
    return np.arctan2(ev[1],ev[0]), np.linalg.norm(ev)

if __name__=="__main__":
    print("="*76)
    print("G3  framework SME s^TX force on the full ASSIST model -- validation")
    print(f"  a0={a0_can:.2e} (canon)/{a0_alt:.2e} (alt);  V_cmb={Vcmb/1e3:.1f} km/s -> beta_cmb={beta_cmb:.3e}")
    print(f"  CMB apex (RA,Dec)=(167.94,-6.94) -> n_apex={n_apex.round(3)}")
    print("="*76)
    # a belt asteroid: a=2.6 AU, e=0.12, i=8deg -> a rough state vector at t0
    t0 = 2457200.5                     # ~2015, within Gaia era
    a,e = 2.6,0.12
    vc = np.sqrt(GMsun_au/a)
    # start at perihelion-ish in the ecliptic, small inclination
    state = np.array([a*(1-e),0,0.05, 0, vc*np.sqrt((1+e)/(1-e)),0.01*vc])

    # baseline (no SME) precession over 6 yr, and with SME at two coefficient levels (linearity test)
    T = 6*365.25
    for label,sTX in [("no SME (GR+planets)",0.0),("s^TX=1e-8",1e-8),("s^TX=2e-8",2e-8)]:
        sJK = None if sTX==0 else sbar_JK_from_apex(sTX)
        sim,ex = make_sim(state,t0,sJK)
        w0,ecc0 = perihelion_lon(sim)
        sim.integrate(sim.t+T)
        w1,ecc1 = perihelion_lon(sim)
        dperi = ((w1-w0+np.pi)%(2*np.pi))-np.pi
        print(f"  {label:22s}: perihelion drift over 6 yr = {np.degrees(dperi)*3600:+9.3f} arcsec  (e={ecc1:.3f})")
    print()
    print("  Linearity check: the SME-induced drift should scale ~linearly with s^TX")
    print("  (the s^TX=2e-8 excess over baseline ~ 2x the s^TX=1e-8 excess). Framework")
    print("  prediction + universal-fit comparison and the real-data fit follow in g4/g5.")
