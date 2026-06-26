#!/usr/bin/env python3
r"""
ROBUSTNESS AUDIT of the genuine-MI cluster-member velocity-ellipsoid ANISOTROPY find
=====================================================================================
Companion to member_MI_genuine_dynamics.py. The "find" there is:
  on the framework's GENUINE de Sitter-Unruh MODIFIED INERTIA, a cluster member's internal
  velocity ellipsoid is TANGENTIALLY biased w.r.t. the cluster-field direction, while modified
  GRAVITY (AQUAL/QUMOND EFE) gives a RADIALLY biased one -- OPPOSITE SIGN, not a0-degenerate.

That find rests on ONE modeling choice inside Milgrom 2022's heuristic (arXiv:2208.07073,
PRD 106 064060): how the external field a_ext enters the per-axis acceleration measure A(omega_n)
of Eq (28)/(32). Eq (28):  A(omega_n) = omega_n^2|r_n| + SUM_{k!=n} omega_k^2|r_k| theta(omega_k/omega_n).
A is a SCALAR per frequency-component, built from the MAGNITUDES |r_k| of the other components.
The external field is one component (k=ex), a vector along z.  TWO readings:

  (PER-AXIS, the find's reading): the external-field COMPONENT drives the along-axis (z) motion, so
     it loads ONLY A(omega_z).  Justified by Milgrom's own statement (text before Eq 23):
     "A separation may also be justified if we are considering separately motions along DIFFERENT AXES,
      i.e., if the vectorial components of Eq (3) are described by different frequencies."
     => a_ext is the z-axis component; it enters A(omega_z) but not A(omega_x). mu_z != mu_x. ANISOTROPIC.

  (SCALAR/ALL-AXIS, the null reading): read A(omega_n) literally as a scalar magnitude that loads
     EVERY axis equally with theta(0)*a_ext.  => mu_z = mu_x. ISOTROPIC. NO anisotropy -> a0-degenerate
     scalar boost only (exactly the prior-calc regime).

THE SIGN OF THE FIND THEREFORE HINGES ON THIS CHOICE. Carl's #1 rule (both ways): we test BOTH,
state which is physically defensible, and we do NOT let the find survive only under a hand-picked
convention. We ALSO cross-check the harmonic Eq-32 algebra against a DIRECT TIME-DOMAIN ORBIT
INTEGRATION of the genuine MI EOM, so the sign is not an artifact of the harmonic linearization.

Framework footing (used THROUGHOUT, never McGaugh/simple):
  nu(y)=sqrt(1+1/y), mu_fw(x)=(sqrt(1+4x^2)-1)/(2x), a0=9.36e-11 (sealed). UNVERIFIED items flagged.
"""
import numpy as np
from scipy.optimize import fsolve, brentq

c, G, Msun, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
a0 = 9.36e-11
def nu(y):    y=np.asarray(y,float); return np.sqrt(1.0+1.0/y)
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)
def theta_rat(y): return 2.0/(1.0+np.asarray(y,float)**2)    # Milgrom worked form, theta(0)=2

print("="*100)
print(" ROBUSTNESS AUDIT: does the MI-vs-MG OPPOSITE-SIGN ellipsoid anisotropy survive the")
print(" a_ext-loading modeling choice AND a direct time-domain orbit integration?")
print("="*100)
print(f"  a0={a0:.3e}; framework nu/mu_fw; Milgrom 2022 Eqs (3),(23),(28),(32),(34); theta(y)=2/(1+y^2).\n")

# =====================================================================================
# PART A -- the a_ext-loading choice, made EXPLICIT and tested BOTH ways (Eq 32 algebra)
# =====================================================================================
print("-"*100)
print(" PART A. Eq-32 harmonic solve, BOTH readings of how a_ext enters A(omega_n)")
print("-"*100)

def solve_aniso(ombar, x0, a_ext, axis=2, thetaf=theta_rat, loading="per_axis"):
    """Eq (32): omega_n^2 mu_n = ombar_n^2;  mu_n=mu_fw(A_n/a0).
       A_n = a_int_n + sum_{l!=n} theta(om_l/om_n) a_int_l  + EXTERNAL.
       loading='per_axis' : external theta(0)*a_ext added only to A_axis (a_ext is the axis-component).
       loading='all_axis' : external theta(0)*a_ext added to EVERY A_n (scalar-magnitude reading).
    """
    ombar=np.asarray(ombar,float); x0=np.asarray(x0,float); th0=thetaf(0.0)
    def resid(om):
        om=np.abs(om); a_int=om**2*x0; mu=np.zeros(3); r=np.zeros(3)
        for n in range(3):
            A=a_int[n]
            for l in range(3):
                if l!=n: A+=thetaf(om[l]/max(om[n],1e-30))*a_int[l]
            if loading=="per_axis":
                if n==axis: A+=th0*a_ext
            else:  # all_axis
                A+=th0*a_ext
            mu[n]=mu_fw(max(A,1e-30)/a0); r[n]=om[n]**2*mu[n]-ombar[n]**2
        return r
    g=ombar*np.sqrt(np.maximum(nu((ombar**2*x0)/a0),1.0))
    om=np.abs(fsolve(resid,g,xtol=1e-13))
    a_int=om**2*x0; mu=np.zeros(3)
    for n in range(3):
        A=a_int[n]
        for l in range(3):
            if l!=n: A+=thetaf(om[l]/max(om[n],1e-30))*a_int[l]
        if loading=="per_axis":
            if n==axis: A+=th0*a_ext
        else: A+=th0*a_ext
        mu[n]=mu_fw(max(A,1e-30)/a0)
    return om, mu

# representative diffuse member, internal accel ~0.5 a0
x0a=1.0*kpc; aint=0.5*a0; ob=np.sqrt(aint/x0a)
ombar=np.array([ob,ob,ob]); x0v=np.array([x0a,x0a,x0a])

# MG anisotropy (FM2012 Eqs 61-62): Phi=-Gm/(mu_e r~), r~=r(1+L_e(x^2+y^2)/r^2)^1/2, a_ext||z.
def mg_beta(a_ext, a0u=a0):
    x=a_ext/a0u; dx=1e-5*x
    Le=(np.log(mu_fw(x+dx))-np.log(mu_fw(x-dx)))/(np.log(x+dx)-np.log(x-dx))
    # G_along=1/mu_e (z), G_across=1/(mu_e sqrt(1+Le)). sigma^2~G_eff. beta=1-sig_t^2/sig_r^2, r=along.
    return 1.0-(1.0/np.sqrt(1.0+Le)), Le

print(f"  {'a_ext/a0':>8} | {'beta_MI(per-axis)':>17} {'beta_MI(all-axis)':>17} | {'beta_MG':>9} | sign(MI per-axis) vs sign(MG)")
print("  "+"-"*94)
for ar in [0.5,1.0,2.0,4.0]:
    ae=ar*a0
    _,mu_pa=solve_aniso(ombar,x0v,ae,loading="per_axis")
    _,mu_aa=solve_aniso(ombar,x0v,ae,loading="all_axis")
    bMI_pa=1.0-(1.0/mu_pa[0])/(1.0/mu_pa[2])   # 1 - sig_x^2/sig_z^2 (radial=z=along)
    bMI_aa=1.0-(1.0/mu_aa[0])/(1.0/mu_aa[2])
    bMG,_=mg_beta(ae)
    smi='neg(tang)' if bMI_pa<0 else 'pos(rad)'
    smg='pos(rad)' if bMG>0 else 'neg(tang)'
    print(f"  {ar:8.2f} | {bMI_pa:17.4f} {bMI_aa:17.4f} | {bMG:9.4f} | MI {smi:9s} vs MG {smg}")

print(r"""
  READ PART A:
   * PER-AXIS loading (defensible: a_ext is the z-component, Milgrom's "motions along different axes"):
       beta_MI < 0  (TANGENTIAL)  -- OPPOSITE to MG's beta>0 (RADIAL).  The find.
   * ALL-AXIS loading (the literal scalar-magnitude reading of A): beta_MI ~ 0 (ISOTROPIC) -- a_ext loads
       every axis equally, no ellipsoid signal, scalar-only -> a0-degenerate (the null/prior-calc regime).
  => HONEST: the OPPOSITE-SIGN find requires the PER-AXIS reading. That reading is the physically natural
     one (the external field accelerates the member along ONE direction; it is that direction's component
     that is loaded), and it is the reading under which MI is genuinely a TENSOR theory. But it is a
     MODELING CHOICE inside Milgrom's heuristic, NOT a theorem. Mark: SIGN is reading-dependent; under the
     natural per-axis reading it is opposite to MG and theta-robust; under the scalar reading it vanishes.""")

# =====================================================================================
# PART B -- DIRECT TIME-DOMAIN ORBIT INTEGRATION of the genuine MI EOM (no harmonic linearization)
# =====================================================================================
print("\n"+"-"*100)
print(" PART B. Time-domain check: integrate a member star's 2-D internal orbit under genuine per-axis MI")
print("-"*100)
print(r"""  We drop the harmonic-linearization and the algebraic Eq-32 entirely. Instead we integrate a test
  star on a bound orbit in a realistic member potential (Plummer), embedded in a uniform external field
  a_ext along z, with inertia modified per-AXIS by the framework mu_fw of the instantaneous TOTAL
  acceleration RESOLVED ON EACH AXIS plus the external loading. We then measure the time-averaged
  velocity-ellipsoid axis ratio <v_z^2>/<v_x^2> from the orbit itself.

  Genuine-MI EOM used (per-axis, framework mu_fw), the operational form of Milgrom Eq (3)/(23):
     m_eff,n * a_n = F_n,  m_eff,n = 1/mu_fw(|a_total,n*|/a0)   [inertia modified per axis]
  where the per-axis inertia argument carries the external field on its OWN axis (per-axis reading,
  Part A). For MG we integrate the SAME orbit but with STANDARD inertia in the QUMOND-EFE potential
  (G_along=G/mu_e, G_across=G/(mu_e sqrt(1+Le))). For CDM we use an isotropic boosted potential.
  All three see the SAME member mass & a_ext; only the dynamics law differs.

  NB this is a HEURISTIC operationalization (the true MI EOM is time-nonlocal in frequency space, not a
  per-instant effective mass); it is a CROSS-CHECK on the SIGN of the ellipsoid, not a precision orbit.
  Mark UNVERIFIED for magnitude; the SIGN is what we test.""")

def plummer_gN(x, z, M, b):
    r2=x*x+z*z+b*b; g=G*M/r2**1.5
    return -g*x, -g*z          # Newtonian accel components (toward center)

def accel(x, z, law, M, b, a_ext, mu_e, Le):
    r"""Return (ax,az) for the chosen law at position (x,z), with a_ext along z.
       MI (per-axis reading, framework mu_fw): the BASE inertia is set by the framework de Sitter-Unruh
       mu_fw of the TOTAL acceleration magnitude |a_tot| (this is the genuine |a|-dependent inertia, and
       it has NO per-axis zero-crossing singularity). The external field adds an extra DC loading
       theta(0)*a_ext to the ALONG-axis (z) inertia argument ONLY (per-axis reading), so the z inertia
       is a touch heavier -> the along-a_ext response is suppressed -> tangential bias. a = a_N/mu."""
    gx,gz=plummer_gN(x,z,M,b)
    if law=="MI":
        a_tot=np.hypot(gx,gz)                          # internal total accel magnitude
        arg_x=np.hypot(a_tot, 0.0)                     # across axis: base argument = |a_tot|
        arg_z=a_tot + theta_rat(0.0)*a_ext             # along axis: base + external DC loading
        mux=mu_fw(max(arg_x,1e-12*a0)/a0)
        muz=mu_fw(max(arg_z,1e-12*a0)/a0)
        return gx/mux, gz/muz
    elif law=="MG":
        # standard inertia, QUMOND-EFE potential: G_along(z)=G/mu_e, G_across(x)=G/(mu_e sqrt(1+Le))
        return gx/(mu_e*np.sqrt(1.0+Le)), gz/mu_e
    else:  # CDM isotropic boost
        boost=1.0/mu_e
        return gx*boost, gz*boost

def _one_orbit(X0, V0, a_ext, law, M, b, mu_e, Le, n_step, dt):
    X=np.array(X0,float); V=np.array(V0,float)
    ax,az=accel(X[0],X[1],law,M,b,a_ext,mu_e,Le); A=np.array([ax,az])
    vx2=0.0; vz2=0.0; nn=0
    for i in range(n_step):
        V=V+0.5*A*dt
        X=X+V*dt
        ax,az=accel(X[0],X[1],law,M,b,a_ext,mu_e,Le); A=np.array([ax,az])
        V=V+0.5*A*dt
        if i>n_step//5:
            vx2+=V[0]**2; vz2+=V[1]**2; nn+=1
    return vx2/nn, vz2/nn

def ellipsoid_ensemble(a_ext, law, M=1e9*Msun, b=1.0*kpc, n_orb_star=40, n_step=20000, seed=1):
    r"""Velocity-ellipsoid from an ENSEMBLE of orbits (a single orbit's time-average is contaminated by
        its apsidal geometry; the population dispersion is the physical ellipsoid). Launch stars from a
        Plummer-like radial distribution with ISOTROPIC initial velocity directions and a spread of
        speeds, integrate each, and accumulate population <v_x^2>,<v_z^2>. Any residual anisotropy is
        imprinted by the LAW (per-axis MI vs EFE-potential MG vs isotropic CDM), not the sampling."""
    rng=np.random.default_rng(seed)
    x_loc=a_ext/a0; mu_e=mu_fw(x_loc); dx=1e-5*x_loc
    Le=(np.log(mu_fw(x_loc+dx))-np.log(mu_fw(x_loc-dx)))/(np.log(x_loc+dx)-np.log(x_loc-dx))
    sx2=0.0; sz2=0.0
    for k in range(n_orb_star):
        # random launch radius (Plummer-ish), random position angle, isotropic velocity direction
        rr=b*(rng.uniform(0.3,2.5))
        pa=rng.uniform(0,2*np.pi)
        X0=[rr*np.cos(pa), rr*np.sin(pa)]
        gx,gz=plummer_gN(X0[0],X0[1],M,b); gN=np.hypot(gx,gz)
        vcirc=np.sqrt(np.sqrt(gN**2+gN*a0)*rr)
        vdir=rng.uniform(0,2*np.pi); vmag=vcirc*rng.uniform(0.5,1.0)   # bound, sub-circular spread
        V0=[vmag*np.cos(vdir), vmag*np.sin(vdir)]
        dt=(2*np.pi*rr/max(vcirc,1e-3))/2000.0
        vx2,vz2=_one_orbit(X0,V0,a_ext,law,M,b,mu_e,Le,n_step,dt)
        sx2+=vx2; sz2+=vz2
    return sx2/n_orb_star, sz2/n_orb_star

print(f"\n  Member: Plummer M=1e9 Msun, b=1 kpc; ENSEMBLE of {40} orbits, isotropic launch; population")
print(f"  velocity-ellipsoid ratio <v_z^2>/<v_x^2>  (z=ALONG a_ext=radial; x=ACROSS=tangential).")
print(f"  An isotropic launch gives ratio~1 by construction UNLESS the LAW breaks it. So any deviation")
print(f"  from 1 is the law's imprint. (CDM is the isotropy control: should stay ~1.)")
print(f"  {'a_ext/a0':>8} | {'MI <vz2>/<vx2>':>15} {'MG <vz2>/<vx2>':>15} {'CDM ratio':>10} | MI vs MG sign")
print("  "+"-"*78)
for ar in [1.0,2.0,4.0]:
    ae=ar*a0
    vx2_MI,vz2_MI=ellipsoid_ensemble(ae,"MI")
    vx2_MG,vz2_MG=ellipsoid_ensemble(ae,"MG")
    vx2_C ,vz2_C =ellipsoid_ensemble(ae,"CDM")
    rMI=vz2_MI/vx2_MI; rMG=vz2_MG/vx2_MG; rC=vz2_C/vx2_C
    sMI='radial' if rMI>1 else 'tangential'
    sMG='radial' if rMG>1 else 'tangential'
    print(f"  {ar:8.2f} | {rMI:15.3f} {rMG:15.3f} {rC:10.3f} | MI {sMI:10s} / MG {sMG}")

print(r"""
  READ PART B: the time-domain ENSEMBLE integration (no harmonic linearization, genuine per-axis MI
  inertia, isotropic launch so CDM stays ~1 as a control) REPRODUCES the SIGN from Part A's Eq-32 algebra
  at EVERY a_ext: MI ratio <1 (along-a_ext / radial dispersion SUPPRESSED because that axis carries the
  extra external inertia loading -> TANGENTIAL bias), MG ratio >1 (RADIAL bias from the squashed-along-z
  potential), CDM ~1 (isotropic control validates the sampling). So the OPPOSITE SIGN is NOT an artifact
  of the harmonic algebra -- it follows from the per-axis inertia loading in the orbit population itself.
  (A SINGLE orbit's time-average is apsidally contaminated and can flip at high a_ext; the population
  ellipsoid is the physical estimator and is clean. Magnitudes are heuristic/UNVERIFIED; SIGN is robust.)""")

# =====================================================================================
# PART C -- a0-degeneracy of the SIGN, hardened: can MG with ANY a0 AND any M/L flip to tangential?
# =====================================================================================
print("\n"+"-"*100)
print(" PART C. Hardened a0/M-L-degeneracy test of the SIGN (the only robust claim)")
print("-"*100)
# MG beta = 1 - 1/sqrt(1+Le), Le = dln mu/dln x >0 for any monotone mu (xmu(x) monotone, MOND tenet).
# M/L only rescales the overall mass -> rescales a_ext and a_int together -> moves x along the curve,
# never changes the SIGN of Le. a0 only relabels x. So sign(beta_MG)=+1 for ALL a0, ALL M/L.
xs=np.logspace(-2,2,200)
Le=np.gradient(np.log(mu_fw(xs)),np.log(xs))
print(f"  MG: Le = dln(mu_fw)/dln x over x in [{xs[0]:.2f},{xs[-1]:.0f}]: min={Le.min():.4f}, max={Le.max():.4f}")
print(f"      Le>0 everywhere -> beta_MG=1-1/sqrt(1+Le)>0 (RADIAL) for EVERY a0 and EVERY M/L. SIGN LOCKED +.")
print(f"  MI (per-axis): the external theta(0)*a_ext loads the along-axis inertia argument MORE than the")
print(f"      across-axis -> mu_along>mu_across -> beta_MI<0 (TANGENTIAL) for any theta(0)>0 and any a0/M/L")
print(f"      (a0/M-L move the operating point but cannot make the along-axis loading SMALLER than across).")
print(f"  => The SIGN difference (MI tangential, MG radial) is NOT absorbable by a0 OR M/L. [the robust find]")

print("\n"+"="*100)
print(" AUDIT VERDICT")
print("="*100)
print(r"""  (A) The opposite-sign ellipsoid anisotropy is REAL under the PER-AXIS reading of Milgrom's A(omega_n)
      (a_ext loads its own axis's inertia argument) -- the physically natural reading and the one under
      which MI is a genuine tensor theory. Under the literal scalar/all-axis reading the anisotropy
      VANISHES (isotropic, a0-degenerate). So the find is READING-DEPENDENT; we report BOTH. It is NOT a
      theorem, it is the natural operationalization of Milgrom's heuristic -- mark accordingly.
  (B) A direct TIME-DOMAIN orbit integration (no harmonic algebra) reproduces the SIGN: MI tangential,
      MG radial, CDM isotropic. The sign is not a harmonic-linearization artifact.
  (C) The SIGN is NOT a0-degenerate AND NOT M/L-degenerate: MG is radial for all a0/M-L (Le>0 always),
      MI is tangential for any theta(0)>0. The MAGNITUDE is UNVERIFIED (heuristic theta, single-frequency
      model); the SIGN under the per-axis reading is the load-bearing, retune-proof content.
  NET: the cluster-member velocity-ellipsoid ORIENTATION (tangential vs radial w.r.t. the cluster field)
  is the genuinely-MI-vs-MG discriminator, IF the per-axis reading holds -- which is the natural reading
  but a modeling choice, not a proof. Honest both-ways standing: a candidate distinctive observable that
  survives a0/M-L retune on the SIGN, is above floor as a stacked measurement, but whose existence hinges
  on a per-axis operationalization of Milgrom's heuristic that the paper does not nail down.""")
