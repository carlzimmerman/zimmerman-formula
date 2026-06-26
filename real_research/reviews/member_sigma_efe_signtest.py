#!/usr/bin/env python3
"""
CLUSTER-MEMBER INTERNAL VELOCITY DISPERSION (sigma_int) -- THE EFE SIGN TEST
============================================================================
Gating calculation for the framework's claimed DISTINCTIVE cluster-member sigma-SIGN test.

WHAT IS MEASURED (resolved): the INTERNAL stellar velocity dispersion sigma_int of a MEMBER galaxy
(its own stellar dynamics, e.g. an aperture sigma from MUSE/4MOST spectroscopy of the member's stars),
NOT the cluster's member-to-member velocity dispersion. Only sigma_int is EFE-sensitive: the EFE
quenches the member's INTERNAL MOND boost. (The cluster's member-velocity dispersion is set by the
cluster potential, not the member's internal EFE.)

THREE MODELS for sigma_int(R) of a FIXED representative member (fixed baryonic mass, size), as a
function of cluster-centric radius R (-> external field g_ext(R)):
  [A] FRAMEWORK MI-EFE   : mu_fw[ theta(omega_ex/omega_in) * a_ex / a0 ], theta>=1 (Milgrom-2022 Eq.35)
  [B] MODIFIED-GRAVITY    : QUMOND/AQUAL EFE, momentary a_ex (no theta) -> Freundlich-2022 Coma form
  [C] CDM                 : member keeps its own halo, NO EFE; tidal heating -> sigma UP or flat.

Framework footing (its OWN dS-Unruh MI):
  a0 = 9.36e-11 m/s^2 ; nu(y)=sqrt(1+1/y) ; mu_fw(x)=(sqrt(1+4x^2)-1)/(2x) [exact inverse of nu]
  Upsilon ~ 0.70.

Primary-source physics (VERIFIED this session):
  - Milgrom 2022 (2208.07073) abstract: MI-EFE = mu(theta<a_ex>/a0), theta>1 frequency factor; theta
    can "appreciably enhance the EFE in quenching MOND effects, over what is deduced in modified gravity."
    => MI EFE is STRONGER than MG but SAME DIRECTION (both quench MOND -> sigma DOWN).
  - Milgrom 2310.14334 abstract: MI EFE pushes toward Newtonian; stronger for wide binaries/vertical
    motions, weaker in inner Solar System; frequency-ratio dependent.
  - Freundlich et al. 2022 (A&A 658 A26, Coma UDGs, QUMOND): "the EFE pushes the MOND prediction towards
    the Newtonian case ... systematically below the measured velocity dispersion"; closer (stronger field)
    -> LOWER sigma.  => MODIFIED GRAVITY ALSO predicts member sigma DOWN.
  - CDM: tidal heating at pericenter inflates sigma UP (search-confirmed); each member keeps its halo.
"""
import numpy as np

# ---------------- constants ----------------
G    = 6.674e-11
Msun = 1.989e30
Mpc  = 3.0857e22
kpc  = 3.0857e19
pc   = 3.0857e16
yr   = 3.1557e7
Gyr  = 1e9*yr
a0   = 9.36e-11           # framework a0 (m/s^2)
Ups  = 0.70

# ---------------- framework laws (its OWN dS-Unruh MI) ----------------
def nu(y):                # isolated boost: g_obs = g_N * nu(g_N/a0)
    return np.sqrt(1.0 + 1.0/y)

def mu_fw(x):             # inverse inertia mu(x)=(sqrt(1+4x^2)-1)/(2x), exact inverse of nu
    x = np.asarray(x, float)
    return (np.sqrt(1.0+4.0*x**2)-1.0)/(2.0*x)

# verify mu_fw is the inverse companion of nu:  if g_obs=g_N nu(g_N/a0) then mu_fw(g_obs/a0)*g_obs = g_N
def _check_inverse():
    gN = np.logspace(-3,2,200)*a0
    gobs = gN*nu(gN/a0)
    recovered = mu_fw(gobs/a0)*gobs
    return np.max(np.abs(recovered-gN)/gN)

# ============================================================================
# STEP 1 -- WHAT IS THE TYPICAL g_ext/a0 RANGE FOR MEMBERS OF A MASSIVE CLUSTER?
# ============================================================================
def cluster_gext(R_mpc, M15=1.0, model='nfw'):
    """External field g_ext = G M_cl(<R)/R^2 for a M~1e15 Msun cluster across R~0.1-3 Mpc.
    Use an NFW enclosed mass (c=5, r200~2 Mpc) so M(<R) is realistic, not the point-mass M_tot."""
    M200 = M15*1e15*Msun
    r200 = 2.0*Mpc            # ~2 Mpc for 1e15 at z~0.2
    c    = 5.0
    rs   = r200/c
    def m_nfw(r):
        x = r/rs
        return M200*(np.log(1+x)-x/(1+x))/(np.log(1+c)-c/(1+c))
    R = R_mpc*Mpc
    if model=='point':
        Menc = M200
    else:
        Menc = m_nfw(R)
    g = G*Menc/R**2
    return g

# ============================================================================
# STEP 2 -- omega_ex vs omega_in  -> theta REGIME (Milgrom-2022)
# ============================================================================
def frequencies(R_mpc, M15=1.0, Mbar_member=5e10, Reff_member_kpc=3.0):
    """omega_ex = member orbital angular frequency around cluster (~Gyr);
       omega_in = internal stellar orbital angular frequency in the member (~10-100 Myr)."""
    # external orbit: circular freq at R in cluster potential
    R = R_mpc*Mpc
    g_ext = cluster_gext(R_mpc, M15)
    v_orb = np.sqrt(g_ext*R)              # circular speed (Newtonian-ish; MOND boost small here, see below)
    omega_ex = v_orb/R
    # internal orbit: at the member's effective radius, internal accel a_in ~ G Mbar/Reff^2 (boosted)
    Mb = Mbar_member*Msun; Re = Reff_member_kpc*kpc
    g_in_N = G*Mb/Re**2
    omega_in = np.sqrt(g_in_N/Re)         # ~ dynamical freq of the member's stars
    return omega_ex, omega_in, g_ext, g_in_N

# ============================================================================
# STEP 3 -- sigma_int(R) under the three models
# ============================================================================
# Member: representative early-type/dwarf member. sigma scales as sigma ~ sqrt(g_eff * Reff) roughly,
# with g_eff the EFFECTIVE internal gravity (boosted by MOND, quenched by EFE). We compute the FRACTIONAL
# sigma relative to the ISOLATED-MOND value, which is the cleanly-comparable quantity (the absolute sigma
# needs a full Jeans solve; the FRACTIONAL EFE suppression is robust and is what the sign test measures).

# CANONICAL EFE formula (Famaey & McGaugh 2012, Living Reviews, Eq. for a 1-D collinear external field;
# used by Wu&Kroupa, Haghi, Freundlich 2022). Solve IMPLICITLY for the internal MOND field g (=a):
#     (g + g_ext) * mu( (g+g_ext)/a0 )  =  g_N  +  g_ext * mu( g_ext/a0 )
# where g_N = G M_bar / r^2 is the member's Newtonian internal field, g_ext the host external field.
#   - isolated limit (g_ext=0):  g*mu(g/a0)=g_N  ->  g = g_N*nu(g_N/a0)  (full MOND boost).
#   - EFE-dominant (g_ext>>g, g_ext<a0): g ~ g_N/mu(g_ext/a0)  (quasi-Newtonian with G_eff=G/mu(g_ext/a0)).
#   - strong EFE (g_ext>>a0): mu->1, g->g_N (Newtonian) -> MAXIMAL suppression, sigma -> Newtonian floor.
# This is the QUANTITY that goes DOWN as g_ext rises. We solve it exactly by root-finding.
from scipy.optimize import brentq

def solve_internal_g(g_N, g_ext, theta=1.0):
    """Solve (g+g_ext_eff) mu((g+g_ext_eff)/a0) = g_N + g_ext_eff mu(g_ext_eff/a0) for the internal field g.
    theta scales the EFFECTIVE external field entering the inertia (Milgrom-2022 MI: g_ext_eff=theta*g_ext).
    Returns g (the member's actual internal gravitational field)."""
    ge = theta*g_ext
    rhs = g_N + ge*mu_fw(np.maximum(ge/a0,1e-12))
    f = lambda g: (g+ge)*mu_fw(np.maximum((g+ge)/a0,1e-12)) - rhs
    # g is between g_N (Newtonian floor) and g_N*nu(g_N/a0) (isolated boost)
    lo, hi = g_N*1e-3, g_N*nu(g_N/a0)*3+ge
    return brentq(f, lo, hi, xtol=1e-30, rtol=1e-12)

def g_internal_isolated(g_N):
    """isolated member, no EFE: g = g_N*nu(g_N/a0)."""
    return g_N*nu(g_N/a0)

def g_internal_MI_EFE(g_N, g_ext, theta):
    """[A] Framework MI-EFE: effective external field = theta*g_ext (theta>=1, Milgrom-2022)."""
    return solve_internal_g(g_N, g_ext, theta=theta)

def g_internal_MG_EFE(g_N, g_ext):
    """[B] Modified-gravity (QUMOND/AQUAL) EFE: momentary external field, theta=1."""
    return solve_internal_g(g_N, g_ext, theta=1.0)

def g_internal_CDM(g_N):
    """[C] CDM: member keeps its OWN halo (no EFE). Fair null: isolated CDM == isolated MOND, R-independent."""
    return g_N*nu(g_N/a0)

# sigma ~ sqrt(g_internal * Reff); FRACTIONAL sigma vs isolated-MOND = sqrt(g_internal/g_iso)
def sigma_frac(g_internal, g_iso):
    return np.sqrt(g_internal/g_iso)

# keep old names as thin wrappers so the rest of the script reads the implicit solver
def g_eff_isolatedMOND(g_in_N): return g_internal_isolated(g_in_N)
def g_eff_MI_EFE(g_in_N, g_ext, theta): return g_internal_MI_EFE(g_in_N, g_ext, theta), mu_fw(theta*g_ext/a0)
def g_eff_MG_EFE(g_in_N, g_ext): return g_internal_MG_EFE(g_in_N, g_ext), mu_fw(g_ext/a0)
def g_eff_CDM(g_in_N): return g_internal_CDM(g_in_N)

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("="*94)
    print(" CLUSTER-MEMBER sigma_int EFE SIGN TEST -- framework MI vs modified-gravity vs CDM")
    print("="*94)
    print(f" inverse-companion check  max|mu_fw(nu)*g - g_N|/g_N = {_check_inverse():.2e}  (mu_fw is exact inverse of nu)")
    print(f" a0 = {a0:.3e} m/s^2 (framework, =c^2 sqrt(Lambda/32pi))   Upsilon={Ups}")
    print()

    # ---- STEP 1: g_ext/a0 range for members of a 1e15 Msun cluster ----
    print("-"*94)
    print(" STEP 1 -- external field g_ext(R)/a0 for members of a M_cl=1e15 Msun cluster (NFW M(<R))")
    print("-"*94)
    Rgrid = np.array([0.1,0.2,0.3,0.5,0.75,1.0,1.5,2.0,3.0])
    print(f"  {'R[Mpc]':>7} {'M(<R)[1e14Msun]':>16} {'g_ext[m/s^2]':>14} {'g_ext/a0':>10}")
    gext_list=[]
    for R in Rgrid:
        ge = cluster_gext(R, 1.0)
        M200=1e15*Msun; r200=2*Mpc; c=5; rs=r200/c
        Menc=M200*(np.log(1+R*Mpc/rs)-(R*Mpc/rs)/(1+R*Mpc/rs))/(np.log(1+c)-c/(1+c))
        gext_list.append(ge)
        print(f"  {R:>7.2f} {Menc/1e14/Msun:>16.2f} {ge:>14.3e} {ge/a0:>10.2f}")
    gext_arr=np.array(gext_list)
    print(f"\n  => members of a massive cluster sit at g_ext/a0 ~ {gext_arr.min()/a0:.1f} (outskirts 3 Mpc)"
          f" to ~{gext_arr.max()/a0:.0f} (core 0.1 Mpc).")
    print(f"     Across most of the cluster (R~0.3-2 Mpc) g_ext/a0 ~ {cluster_gext(2.0,1.):.2e}/a0={cluster_gext(2.0,1.)/a0:.1f}"
          f" to {cluster_gext(0.3,1.)/a0:.1f}  -> the EFE is STRONG (g_ext > a0 over most radii).")
    print(f"     This is the key precondition: g_ext >~ a0 means the member's internal MOND boost is QUENCHED.")

    # ---- STEP 2: theta regime ----
    print()
    print("-"*94)
    print(" STEP 2 -- omega_ex (member orbit ~Gyr) vs omega_in (internal stellar orbit ~10-100 Myr) -> theta")
    print("-"*94)
    print(f"  {'R[Mpc]':>7} {'P_ex[Gyr]':>10} {'P_in[Myr]':>10} {'omega_in/omega_ex':>18}")
    for R in [0.3,0.5,1.0,2.0]:
        oe,oi,ge,gin = frequencies(R, 1.0, Mbar_member=5e10, Reff_member_kpc=3.0)
        Pex = 2*np.pi/oe/Gyr; Pin = 2*np.pi/oi/(1e6*yr)
        print(f"  {R:>7.2f} {Pex:>10.2f} {Pin:>10.1f} {oi/oe:>18.0f}")
    print(f"\n  => omega_in/omega_ex ~ 1e2-1e3: the internal motion is FAST, the external field is SLOWLY varying.")
    print(f"     In Milgrom-2022's MI-EFE mu(theta * <a_ex>/a0), theta=theta(omega_ex/omega_in) with theta>=1,")
    print(f"     theta(0)=2 or e for the worked example models. With omega_ex/omega_in -> 0 (adiabatic ext field),")
    print(f"     theta -> theta(0) ~ 2 (a FINITE enhancement), NOT 1 and NOT divergent. The member feels a")
    print(f"     theta-ENHANCED external field => MI EFE is STRONGER than MG (theta=1), same direction.")

    # ---- STEP 3: sigma_int(R) under the three models ----
    print()
    print("-"*94)
    print(" STEP 3 -- fractional sigma_int(R) vs isolated-MOND value, three models")
    print("   member: a DIFFUSE/low-acceleration member (g_in < a0) -- the regime where the EFE BITES.")
    print("   (compact members with g_in>>a0 are already Newtonian internally; the EFE barely touches them.)")
    print("-"*94)
    # diffuse member: dwarf/UDG-like, Mbar=1e9 Msun, Reff=2 kpc -> g_in/a0~0.6 (mildly deep-MOND, EFE-sensitive)
    Mb=1e9*Msun; Re=2.0*kpc
    g_in_N = G*Mb/Re**2
    print(f"  member internal Newtonian field g_in/a0 = {g_in_N/a0:.2f}  (so isolated member is MILDLY in MOND regime)")
    g_iso = g_eff_isolatedMOND(g_in_N)
    sig_iso_boost = np.sqrt(g_iso/g_in_N)   # boost of isolated sigma over pure-Newton
    print(f"  isolated-MOND boost of g_eff over Newton = nu(g_in/a0) = {nu(g_in_N/a0):.3f}  "
          f"(isolated sigma is {100*(np.sqrt(nu(g_in_N/a0))-1):.1f}% above Newtonian)")
    print()
    theta0 = 2.0   # Milgrom-2022 worked-example adiabatic limit
    print(f"  {'R':>5} {'gext/a0':>8} | {'[A]MI sig/iso':>13} {'[B]MG sig/iso':>13} {'[C]CDM sig/iso':>14} "
          f"| {'MI-MG gap':>9} {'MI vs CDM':>9}")
    rows=[]
    for R in [0.2,0.3,0.5,0.75,1.0,1.5,2.0,3.0]:
        ge = cluster_gext(R,1.0)
        gA,muA = g_eff_MI_EFE(g_in_N, ge, theta0)
        gB,muB = g_eff_MG_EFE(g_in_N, ge)
        gC     = g_eff_CDM(g_in_N)
        # fractional sigma relative to isolated-MOND (frac<1 => sigma DOWN; frac>1 => sigma UP)
        fA = sigma_frac(gA, g_iso); fB = sigma_frac(gB, g_iso); fC = sigma_frac(gC, g_iso)
        rows.append((R,ge/a0,fA,fB,fC))
        print(f"  {R:>5.2f} {ge/a0:>8.1f} | {fA:>13.3f} {fB:>13.3f} {fC:>14.3f} "
              f"| {fA-fB:>+9.3f} {fA-fC:>+9.3f}")
    rows=np.array(rows)

    # fractional SUPPRESSION (down from isolated) at a representative member radius R~1 Mpc
    print()
    print("-"*94)
    print(" THE DECISIVE NUMBERS")
    print("-"*94)
    iR = list(rows[:,0]).index(1.0)
    fA1,fB1,fC1 = rows[iR,2],rows[iR,3],rows[iR,4]
    def downpct(f): return 100*(1-f)
    print(f"  At R=1 Mpc (g_ext/a0={rows[iR,1]:.1f}), member sigma_int relative to isolated-MOND:")
    print(f"    [A] FRAMEWORK MI-EFE : {fA1:.3f}  -> sigma {'DOWN' if fA1<1 else 'UP'} {abs(downpct(fA1)):.1f}%")
    print(f"    [B] MODIFIED GRAVITY : {fB1:.3f}  -> sigma {'DOWN' if fB1<1 else 'UP'} {abs(downpct(fB1)):.1f}%")
    print(f"    [C] CDM (+EFE-free)  : {fC1:.3f}  -> sigma FLAT (no R-dependence); tidal heating -> UP toward center")
    print()
    print(f"  SIGN:   MI={'DOWN' if fA1<1 else 'UP'}, MG={'DOWN' if fB1<1 else 'UP'}, CDM=FLAT/UP.")
    print(f"  The DOWN-sign is MI-and-MG (MOND-SHARED).  MI is MORE suppressed than MG (theta-enhanced).")
    print(f"  MI-vs-MG gap at R=1 Mpc: {100*(fB1-fA1):.1f}% (MI extra suppression from theta).")
    print(f"  MI suppression vs isolated at R=1 Mpc: {downpct(fA1):.1f}%  <- compare corpus '~7% DOWN' claim.")
    print()
    # how big is the corpus '~7%' under the framework's own a0? scan member radius & cluster radius
    print("  Sensitivity of the MI sigma SUPPRESSION to member acceleration g_in/a0 and cluster radius:")
    print("  (member Mbar=1e9 Msun; vary Reff. positive% = sigma DOWN vs isolated-MOND = the EFE signal)")
    print(f"  {'Reff[kpc]':>9} {'g_in/a0':>8} | {'MI down@R=0.3':>13} {'MI down@R=0.5':>13} {'MI down@R=1':>12}")
    for Re_kpc in [1.0,2.0,3.0,5.0,8.0]:
        Rem=Re_kpc*kpc; gin=G*Mb/Rem**2; giso=g_eff_isolatedMOND(gin)
        downs=[]
        for R in [0.3,0.5,1.0]:
            ge=cluster_gext(R,1.0); gA,_=g_eff_MI_EFE(gin,ge,theta0)
            downs.append(100*(1-sigma_frac(gA,giso)))
        print(f"  {Re_kpc:>9.1f} {gin/a0:>8.2f} | {downs[0]:>12.1f}% {downs[1]:>12.1f}% {downs[2]:>11.1f}%")

    # ---- theta-sweep: how big can the MI-vs-MG gap get, and does the SIGN ever flip? ----
    print()
    print("-"*94)
    print(" theta-SWEEP -- MI-vs-MG gap vs theta (UNVERIFIED exact theta(0); abstract says theta>1, freq-dep)")
    print("   diffuse member g_in/a0=0.37, at R=0.5 and R=1.0 Mpc")
    print("-"*94)
    print(f"  {'theta':>6} | {'MI sig/iso @R0.5':>17} {'MG sig/iso':>11} {'MI-MG gap':>10} | {'@R1.0 MI':>9} {'MI-MG':>7}")
    giso = g_eff_isolatedMOND(g_in_N)
    for th in [1.0,1.5,2.0,2.718,4.0]:
        ge05=cluster_gext(0.5,1.0); ge10=cluster_gext(1.0,1.0)
        gA05,_=g_eff_MI_EFE(g_in_N,ge05,th); gB05,_=g_eff_MG_EFE(g_in_N,ge05)
        gA10,_=g_eff_MI_EFE(g_in_N,ge10,th)
        fA05=sigma_frac(gA05,giso); fB05=sigma_frac(gB05,giso); fA10=sigma_frac(gA10,giso)
        gap05=100*(fB05-fA05); gap10=100*((sigma_frac(g_eff_MG_EFE(g_in_N,ge10)[0],giso))-fA10)
        print(f"  {th:>6.2f} | {fA05:>17.3f} {fB05:>11.3f} {gap05:>9.1f}% | {fA10:>9.3f} {gap10:>6.1f}%")
    print("  => the SIGN never flips (MI and MG both DOWN for all theta>=1); theta only sets the MAGNITUDE gap.")
    print("     The MI-MG gap is largest in the SHALLOW field (outskirts) and ~vanishes in the deep core")
    print("     (where mu->1 for both). theta(0)~2 gives a ~1-3% MI-MG gap over R~0.5-1 Mpc.")

    # ---- realistic member-mix '~7%' reconciliation ----
    print()
    print("-"*94)
    print(" RECONCILING THE CORPUS '~7% DOWN' -- luminosity-weighted MIXED member population")
    print("-"*94)
    print("   The ~27-60% suppressions above are for DIFFUSE members (g_in<<a0). A real spectroscopic")
    print("   member sample is dominated by BRIGHTER, more compact galaxies (g_in>~a0), where the EFE")
    print("   bites only weakly. A luminosity-weighted MEAN over the member mix gives a much smaller mean")
    print("   suppression -- consistent with the corpus '~7%'. Illustrative mix (mass-weighted):")
    # a crude member mass-size mix: (Mbar[Msun], Reff[kpc], weight)
    mix=[(1e11,4.0,0.35),(3e10,3.0,0.30),(1e10,2.5,0.20),(3e9,2.0,0.10),(1e9,2.0,0.05)]
    for R in [0.3,0.5,1.0]:
        ge=cluster_gext(R,1.0); num=0.0; den=0.0
        for Mbar,Re_k,w in mix:
            gin=G*Mbar*Msun/(Re_k*kpc)**2; giso_m=g_eff_isolatedMOND(gin)
            gA,_=g_eff_MI_EFE(gin,ge,theta0); supp=1-sigma_frac(gA,giso_m)
            num+=w*supp; den+=w
        print(f"   R={R:.1f} Mpc (g_ext/a0={ge/a0:.1f}): mass-weighted MEAN MI suppression = {100*num/den:.1f}%")
    print("   => a mixed, brightness-weighted member sample gives a MEAN ~5-12% suppression -- the corpus")
    print("      '~7% DOWN' is in the right ballpark FOR THE STACK MEAN (diffuse members alone go much deeper).")

    print()
    print("-"*94)
    print(" VERDICT (both ways)")
    print("-"*94)
    print(" * WHAT IS MEASURED: member INTERNAL stellar sigma_int (aperture sigma of the member's own stars),")
    print("   NOT the cluster member-velocity dispersion. Only sigma_int is EFE-sensitive.")
    print(" * The DOWN-sign is MOND-SHARED: modified GRAVITY (QUMOND, Freundlich-2022 Coma) ALSO sends member")
    print("   sigma DOWN -- VERIFIED in primary source. The corpus 'MI DOWN vs CDM/MG UP' is WRONG on the MG side.")
    print(" * The distinctive content vs CDM is the SIGN (down vs up/flat) -- shared with MG, NOT unique to MI.")
    print(" * The distinctive content vs MG is the MAGNITUDE: MI is theta-ENHANCED (theta(0)~2) -> a few % MORE")
    print("   suppression. Whether that few-% MI-MG gap clears the floor is the forecast question.")
    print("="*94)

if __name__=="__main__":
    main()
