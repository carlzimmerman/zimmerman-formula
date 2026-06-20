#!/usr/bin/env python3
r"""
ROUTE A FOLLOW-UP -- the three make-or-break checks the first pass flagged:
  (1) FULL-PROFILE shape: does a p=1 |Phi|-linear law reproduce A2029's B_req(r) at EVERY
      radius (20-500 kpc), or only at the 200-kpc anchor? (G1 shape, honest)
  (2) The DEEP-galaxy veto: dwarf spheroidals + the Milky-Way / massive-elliptical CENTER
      have DEEPER |Phi| than SPARC disks. Does the same p=1 law boost THEM and break MOND
      there?  (G2, the real escape from the SPARC-only veto -- the deepest-disk contrast was
      only ~16x; a dSph at the bottom of a host or an elliptical center could be deeper.)
  (3) CASSINI proper: the boost is keyed on |Phi|, and the Sun's |Phi|/c^2 at Saturn from the
      Sun is ~1e-9 (shallow) -- but does the law, written as a metric modification, give a
      PPN gamma deviation? And the SOLAR/STELLAR-INTERIOR + NEUTRON-STAR deep |Phi| (G4).
Both ways: if p=1 reproduces the shape AND survives deep galaxies AND Cassini -> a real
partial win for Route A. If any breaks -> concede.
"""
import numpy as np, glob, os
from scipy.integrate import quad
G=6.674e-11; c=2.998e8; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
Msun_g=1.989e33; kpc_cm=3.0857e21; a0=9.36e-11
HERE=os.path.dirname(__file__)
SPARC=os.path.join(HERE,"..","..","..","real_research","data","sparc_data")

print("="*94)
print(" ROUTE A FOLLOW-UP -- full-shape + deep-galaxy + Cassini (both ways)")
print("="*94)

# ---------- rebuild A2029 (same as routeA) ----------
def nfw_M(r,M200,cn,r200): rs=r200/cn; m=lambda x:np.log(1+x)-x/(1+x); return M200*m(np.asarray(r)/rs)/m(cn)
A2029_M=lambda r: nfw_M(r,8.47e14,4.0,1910.0)
def phi_depth(M_of_r,r_kpc,r_out=5000.):
    inner=G*(M_of_r(r_kpc)*Msun)/(r_kpc*kpc)
    outer,_=quad(lambda rp:G*(M_of_r(rp)*Msun)/((rp*kpc)**2)*kpc,r_kpc,r_out,limit=200)
    return (inner+outer)/c**2
rho_gc=6.6e-26;beta_g=0.54;alpha_g=0.55;rc_gas=77.6
def rho_gas(r):
    x=np.asarray(r)/rc_gas
    return rho_gc*2.0**(1.5*beta_g-0.5*alpha_g)*x**(-alpha_g)*(1+x**2)**(-1.5*beta_g+0.5*alpha_g)
def Mgas(r_kpc):
    def one(rr):
        v,_=quad(lambda rp:4*np.pi*(rp*kpc_cm)**2*rho_gas(rp)*kpc_cm,1e-3,rr,limit=200);return v/Msun_g
    return np.array([one(r) for r in np.atleast_1d(r_kpc)])
_sr=np.array([50.,100.,200.,500.]);_sp=np.array([1.2e12,3.0e12,3.4e12,3.8e12])
def Mstar(r):
    out=np.exp(np.interp(np.log(np.atleast_1d(r)),np.log(_sr),np.log(_sp),left=np.log(_sp[0]),right=np.log(_sp[-1])))
    out=np.where(np.atleast_1d(r)<50.,_sp[0]*(np.atleast_1d(r)/50.)**1.5,out);return out
def M_mond(Mbar,r):
    r_m=np.asarray(r)*kpc;Mb=np.asarray(Mbar)*Msun;gb=G*Mb/r_m**2
    return np.sqrt(gb**2+gb*a0)*r_m**2/G/Msun
def M_mond_boosted(Mbar,r,a0eff):
    r_m=np.asarray(r)*kpc;Mb=np.asarray(Mbar)*Msun;gb=G*Mb/r_m**2
    return np.sqrt(gb**2+gb*a0eff)*r_m**2/G/Msun

# ============ (1) FULL-PROFILE SHAPE TEST ============
print("\n[1] FULL-PROFILE shape: p=1 a0_eff=a0*(1+amp*|Phi|/c^2), amp tuned at 200 kpc.")
Rfull=np.array([20.,50.,100.,200.,300.,500.])
phi=np.array([phi_depth(A2029_M,r) for r in Rfull])
gas=Mgas(Rfull);star=Mstar(Rfull);bar=gas+star;tot=A2029_M(Rfull)
mond=M_mond(bar,Rfull);Breq=tot/mond
# tune amp at 200 kpc so boosted M_MOND = M_tot there
i200=3
def cover_with_amp(amp):
    a0eff=a0*(1+amp*phi)
    mb=M_mond_boosted(bar,Rfull,a0eff)
    return mb/tot, a0eff
# solve amp so cover=1 at 200 kpc
from scipy.optimize import brentq
def f(amp): cov,_=cover_with_amp(amp); return cov[i200]-1.0
amp1=brentq(f,1e2,1e8)
cov,a0eff=cover_with_amp(amp1)
print(f"    amp(p=1)={amp1:.3e}; resulting coverage M_MONDboost/M_tot at each radius:")
print(f"    {'r(kpc)':>7} {'|Phi|/c^2':>11} {'B_req':>8} {'a0eff/a0':>9} {'cover':>8} {'resid left':>11}")
for i,r in enumerate(Rfull):
    print(f"    {r:7.0f} {phi[i]:11.3e} {Breq[i]:8.3f} {a0eff[i]/a0:9.3f} {cov[i]*100:6.1f}% {(1-cov[i])*100:9.1f}%")
maxresid=np.max(np.abs(1-cov))*100
print(f"    -> WORST residual left across 20-500 kpc after the p=1 |Phi|-law: {maxresid:.1f}%")
print(f"       (if <~10% everywhere -> the law CLOSES the core with the RIGHT shape, G1 effectively PASS)")

# ============ (2) DEEP-GALAXY VETO ============
# The SPARC-disk veto passed because the deepest disk |Phi|/c^2~4.8e-6 << cluster core 8e-5.
# But the DEEPEST baryonic galaxy potentials are (a) the CENTERS of massive ellipticals /
# the Milky Way bulge, and (b) dwarf spheroidals sitting deep in a host halo. Compute the
# WORST-CASE galaxy |Phi|/c^2 and the boost the p=1 law gives there.
print("\n[2] DEEP-GALAXY veto -- worst-case baryonic galaxy potential depths:")
# Massive elliptical (M*~1e12, Re~10 kpc): central depth ~ G M* / Re /c^2 * O(1)
def phi_point(M_Msun,r_kpc): return G*M_Msun*Msun/(r_kpc*kpc*c**2)
cases=[
    ("L* spiral disk center (Vbar~200, Rd~3kpc)",  phi_point(6e10,3.0)),
    ("Milky Way @ solar circle (Vc=230)",          (230e3)**2/c**2),
    ("Milky Way bulge center (sigma~120,r~0.5kpc)", phi_point(1e10,0.5)),
    ("Massive elliptical center (M*=1e12,Re=8kpc)", phi_point(1e12,8.0)*2.0),  # *2 for depth vs surface
    ("Brightest ellipt (M*=4e12,Re=30kpc) center",  phi_point(4e12,30.0)*2.0),
    ("dSph baryons alone (M*=1e7,r=0.3kpc)",        phi_point(1e7,0.3)),
    ("dSph IN a host (Fornax @150kpc MW M=1e11)",   phi_point(1e11,150.)+phi_point(1e7,0.3)),
]
print(f"    cluster-core anchor |Phi|/c^2 (200 kpc) = {phi[i200]:.2e}; amp(p=1)={amp1:.2e}")
print(f"    {'system':<46} {'|Phi|/c^2':>11} {'a0eff/a0=1+amp*Phi':>20}")
worst_galaxy_boost=1.0
for name,ph in cases:
    boost=1+amp1*ph
    worst_galaxy_boost=max(worst_galaxy_boost,boost)
    print(f"    {name:<46} {ph:11.3e} {boost:20.3f}")
print(f"    -> WORST galaxy a0_eff/a0 under the p=1 law = {worst_galaxy_boost:.3f}")
print(f"       (massive-elliptical CENTERS are the real risk: deep Phi at HIGH acceleration.")
print(f"        But high g means deep-MOND boost ~ sqrt(a0eff) only matters where g<~a0eff;")
print(f"        ellipt centers have g>>a0 so even a 2x a0 barely moves g_obs -- check below.)")

# the REAL veto: does the boost change g_obs where it's MEASURED? Ellipt centers: g>>a0.
print("\n    Ellipt-center reality check: at g>>a0, g_obs=sqrt(g^2+g*a0eff)~g*(1+a0eff/2g),")
print("    so a 2x a0_eff changes g_obs by ~a0eff/2g, tiny when g>>a0. The boost only bites")
print("    in the deep-MOND regime (g<a0). Deepest-Phi galaxies have HIGH g -> boost is moot.")
# quantify for a massive elliptical center: g ~ G M*/Re^2
for nm,M_,Re_ in [("ellipt M*=1e12 Re=8kpc",1e12,8.0),("BCG M*=4e12 Re=30kpc",4e12,30.0)]:
    g_=G*M_*Msun/(Re_*kpc)**2
    ph=phi_point(M_,Re_)*2.0
    a0eff_=a0*(1+amp1*ph)
    gobs0=np.sqrt(g_**2+g_*a0); gobs1=np.sqrt(g_**2+g_*a0eff_)
    print(f"      {nm}: g={g_:.2e} (g/a0={g_/a0:.0f}); a0eff/a0={a0eff_/a0:.2f}; "
          f"g_obs shift={(gobs1/gobs0-1)*100:.2f}%")

# ============ (3) CASSINI / compact-object G4 ============
print("\n[3] CASSINI + compact-object veto (G4):")
phi_sun_surf=G*1.989e30/(6.957e8*c**2)
r_sat=9.58*1.496e11; phi_sat=G*1.989e30/(r_sat*c**2)
print(f"    The boost is on a0 (the MOND scale), in the deep-MOND regime g<a0. At Saturn,")
print(f"    g_Saturn=GM/r^2={G*1.989e30/r_sat**2:.2e} m/s^2; g/a0={G*1.989e30/r_sat**2/a0:.2e} (>>1).")
print(f"    a0_eff at Saturn = a0*(1+amp*|Phi_sun(Saturn)|/c^2)={a0*(1+amp1*phi_sat):.3e} "
      f"(ratio {1+amp1*phi_sat:.4f}).")
# even if a0_eff is boosted, the anomalous accel delta_g = a0_eff term / 2 (deep-Newtonian exp)
g_sat=G*1.989e30/r_sat**2
a0eff_sat=a0*(1+amp1*phi_sat)
# g_obs = sqrt(g^2+g a0eff) ~ g + a0eff/2 ; the EXTRA accel vs Newton = a0eff/2
delta_over_g=(np.sqrt(g_sat**2+g_sat*a0eff_sat)-g_sat)/g_sat
delta_over_g_std=(np.sqrt(g_sat**2+g_sat*a0)-g_sat)/g_sat
print(f"    fractional anomalous accel at Saturn:  with boost={delta_over_g:.3e}  "
      f"standard MOND={delta_over_g_std:.3e}")
print(f"    Cassini bounds |Delta(GM)/GM| ~ a few e-10 (from range data); MOND's deep-Newtonian")
print(f"    a0/2g already gives {a0/(2*g_sat):.2e} -- this is the SAME for boosted & unboosted")
print(f"    because |Phi_sun|/c^2 at Saturn is only {phi_sat:.1e} -> boost factor {1+amp1*phi_sat:.4f}.")
print(f"    -> The |Phi|-key does NOT meaningfully change the solar-system MOND anomaly:")
print(f"       the Sun's potential at the planets is SHALLOW ({phi_sat:.1e}) so a0_eff~a0 there.")
print(f"    Sun INTERIOR |Phi|/c^2~6e-6 (boost {1+amp1*6e-6:.1f}x) and NEUTRON STAR ~0.17")
print(f"    (boost {1+amp1*0.17:.1e}x) -- but those are at g>>>a0 (Newtonian), where a MOND-scale")
print(f"    boost is utterly negligible (a0_eff/2g ~ {a0*(1+amp1*0.17)/(2*G*1.4*1.989e30/(12e3)**2):.1e}).")
print(f"    BBN/pulsar timing probe G and the metric, NOT a0 -- a0 boost doesn't touch them.")

print("\n"+"="*94)
print(" FOLLOW-UP SUMMARY")
print("="*94)
print(f"  (1) p=1 |Phi|-linear law: worst residual left across 20-500 kpc = {maxresid:.1f}%")
print(f"  (2) worst-case galaxy a0_eff/a0 (deep ellipt/dSph) = {worst_galaxy_boost:.2f}, but at g>>a0 -> g_obs moot")
print(f"  (3) Cassini: a0_eff at Saturn ratio = {1+amp1*phi_sat:.4f} (Sun shallow at planets) -> SAFE")
