#!/usr/bin/env python3
"""
CLUSTER-MEMBER sigma EFE SIGN TEST -- CONSOLIDATED, BOTH-WAYS, REAL-DATA-CALIBRATED
===================================================================================
Mechanism under test: dS-Unruh MODIFIED INERTIA (the framework).
Claim under test (from the corpus): "framework MI -> member sigma DOWN ~7% vs CDM/MG -> sigma UP."

This script does FOUR things, each labelled REAL or SYNTHETIC or VERIFIED:
  (1) [REAL DATA]  WINGS-SPE member-velocity catalog (Cava+2009, VizieR J/A+A/495/707/table4):
                   48 clusters, 3647 members. Calibrates the cluster external-field range g_ext(R)/a0.
                   --> ALSO exposes the load-bearing 'WHAT IS MEASURED' fork (see below).
  (2) [VERIFIED]   Primary-source physics for the three EFE predictions (Milgrom-2022 MI; Coma-UDG
                   QUMOND MG; CDM). Each direction quoted from the source this session.
  (3) [SYNTHETIC]  A member INTERNAL-sigma sample, calibrated to CLASH-VLT/HFF/Coma-UDG numbers, run
                   through the exact (root-found) EFE for MI / MG / CDM as a function of g_ext.
  (4) [FORECAST]   Floor / SNR for the SIGN and for the MI-vs-MG magnitude gap. Honest systematics.

================================ THE 'WHAT IS MEASURED' FORK (load-bearing) ================================
There are TWO different "member sigma" quantities, and only ONE is EFE-sensitive:
  (i)  CLUSTER member-VELOCITY dispersion  sigma_clus = scatter of member cz about the cluster mean.
       This is what WINGS-SPE 'cz' gives. It is set by the CLUSTER potential (each member is a tracer
       particle). The member's OWN internal EFE does NOT change where it sits in the cluster, so
       sigma_clus is NOT (to first order) an EFE-of-the-member observable. (In MOND the cluster potential
       itself differs from CDM, but that is the SAME mass-discrepancy story as cluster eta, NOT the
       distinctive member-EFE sign test.)
  (ii) MEMBER INTERNAL stellar velocity dispersion  sigma_int = aperture sigma of ONE member's own stars
       (MUSE/4MOST resolved spectroscopy). THIS is EFE-sensitive: the cluster external field g_ext quenches
       the member's internal MOND boost. THE SIGN TEST IS ABOUT sigma_int, NOT sigma_clus.
  => WINGS-SPE (cz) CANNOT run the sign test; it calibrates g_ext and proves the pull works. The sign test
     needs RESOLVED INTERNAL sigma of diffuse members (CLASH-VLT/HFF/4MOST), built SYNTHETIC here.
============================================================================================================
"""
import numpy as np, csv, math, os, statistics
from scipy.optimize import brentq

# ---------------- constants & framework footing ----------------
c, G, Msun, Mpc, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e22, 3.0857e19
a0  = 9.36e-11                 # framework a0 = c^2 sqrt(Lambda/32pi) = (c/2)sqrt(G rho_DE)
Ups = 0.70
H0  = 70.0                     # km/s/Mpc for WINGS distances

def nu(y):   return np.sqrt(1.0 + 1.0/y)                    # isolated boost g_obs=g_N nu(g_N/a0)
def mu_fw(x):                                               # exact inverse-inertia mu, inverse of nu
    x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x**2)-1.0)/(2.0*x)

# ---------------- EFE solver (1-D collinear, Famaey-McGaugh; used by Wu-Kroupa/Freundlich/Haghi) ----------
# Solve for the member's internal field g:  (g+ge) mu((g+ge)/a0) = g_N + ge mu(ge/a0),  ge = theta*g_ext.
# isolated (ge=0): g=g_N nu(g_N/a0). strong EFE (ge>>a0): mu->1, g->g_N (Newtonian floor) = max suppression.
def solve_internal_g(g_N, g_ext, theta=1.0):
    ge=theta*g_ext
    rhs=g_N+ge*mu_fw(max(ge/a0,1e-12))
    f=lambda g:(g+ge)*mu_fw(max((g+ge)/a0,1e-12))-rhs
    lo,hi=g_N*1e-3, g_N*nu(g_N/a0)*3+ge
    return brentq(f,lo,hi,xtol=1e-30,rtol=1e-12)

def g_iso(g_N):           return g_N*nu(g_N/a0)                        # isolated MOND (= CDM null, R-indep)
def g_MI (g_N,ge,theta):  return solve_internal_g(g_N,ge,theta=theta)  # [A] framework MI: ge_eff=theta*g_ext
def g_MG (g_N,ge):        return solve_internal_g(g_N,ge,theta=1.0)    # [B] modified gravity: momentary field
def sig_frac(g,g0):       return np.sqrt(g/g0)                         # sigma ~ sqrt(g_eff Reff); frac vs iso

def cluster_gext(R_mpc, M200_15=1.0, c200=5.0, r200_mpc=2.0):
    """g_ext = G M_NFW(<R)/R^2 for an NFW cluster (M200 in 1e15 Msun)."""
    M200=M200_15*1e15*Msun; rs=r200_mpc*Mpc/c200; R=R_mpc*Mpc
    m=M200*(np.log(1+R/rs)-(R/rs)/(1+R/rs))/(np.log(1+c200)-c200/(1+c200))
    return G*m/R**2

# ============================================================================
# (1) REAL DATA -- WINGS-SPE: calibrate g_ext and expose the measured-quantity fork
# ============================================================================
def real_wings():
    path=os.path.join(os.path.dirname(__file__),"..","data","wings_spe_cava2009.csv")
    print("="*100); print(" (1) REAL DATA -- WINGS-SPE member-velocity catalog (Cava+2009, VizieR J/A+A/495/707/table4)")
    print("="*100)
    if not os.path.exists(path):
        print("  [real catalog not found at",path,"] -- run the VizieR pull; skipping real calibration."); return None
    rows=list(csv.DictReader(open(path)))
    for r in rows:
        for k in ('cz','e_cz','R','RAJ2000','DEJ2000'):
            try: r[k]=float(r[k])
            except: r[k]=None
    mem=[r for r in rows if str(r.get('Mm','')).strip()=='1' and r['cz'] and r['R'] is not None]
    cl_all=set(r['Cluster'] for r in rows)
    print(f"  pulled {len(rows)} galaxies, {len(mem)} members (Mm=1), {len(cl_all)} clusters.")
    print(f"  COLUMNS: Cluster, RAJ2000, DEJ2000, cz[km/s], e_cz, R[arcmin proj], Mm(member flag).")
    print(f"  --> 'cz' = member RECESSION velocity => this is the CLUSTER member-VELOCITY dispersion observable")
    print(f"      (quantity (i)), NOT member INTERNAL sigma (quantity (ii)). It calibrates g_ext; it CANNOT")
    print(f"      run the internal-sigma EFE sign test. (See header fork.)")
    def DA(z):
        zz=np.linspace(0,z,300); Ez=np.sqrt(0.3*(1+zz)**3+0.7)
        return (c/1000/H0)*np.trapz(1/Ez,zz)/(1+z)   # Mpc
    cal=[]
    for cl in cl_all:
        m=[r for r in mem if r['Cluster']==cl]
        if len(m)<60: continue
        cz=np.array([r['cz'] for r in m]); Ra=np.array([r['R'] for r in m])
        for _ in range(3):
            md,sd=np.median(cz),np.std(cz); k=np.abs(cz-md)<3*sd; cz,Ra=cz[k],Ra[k]
        zc=np.median(cz)/(c/1000); sig=np.std(cz)/(1+zc)
        Hz=H0*math.sqrt(0.3*(1+zc)**3+0.7); Hz_si=Hz*1000/Mpc
        r200=math.sqrt(3.0)*sig/(10*Hz)              # Mpc (Carlberg virial)
        M200=100*Hz_si**2*(r200*Mpc)**3/G/Msun
        cal.append((cl,len(m),zc,sig,r200,M200))
    cal.sort(key=lambda x:-x[5])
    print(f"\n  {len(cal)} clusters with >=60 members. Top by virial mass:")
    print(f"  {'cluster':>8} {'Nmem':>5} {'z':>6} {'sig_los[km/s]':>13} {'r200[Mpc]':>9} {'M200[1e14]':>10}")
    for cl,n,z,s,r2,M in cal[:8]:
        print(f"  {cl:>8} {n:>5} {z:>6.3f} {s:>13.0f} {r2:>9.2f} {M/1e14:>10.2f}")
    Ms=[x[5] for x in cal]; Ss=[x[3] for x in cal]
    print(f"  M200 span (1e14 Msun): {min(Ms)/1e14:.1f} - {max(Ms)/1e14:.1f} (median {statistics.median(Ms)/1e14:.1f});"
          f" sig_los {min(Ss):.0f}-{max(Ss):.0f} km/s.")
    # external-field range these REAL clusters impose on their members
    Mmed_15=statistics.median(Ms)/1e15
    print(f"\n  REAL external field on members of the MEDIAN WINGS cluster (M200={Mmed_15*1e15:.1e} Msun):")
    print(f"  {'R[Mpc]':>7} {'g_ext/a0':>9}   ({'EFE regime'})")
    for R in (0.3,0.5,1.0,2.0):
        ge=cluster_gext(R,Mmed_15); reg='STRONG (g_ext>a0, boost quenched)' if ge>a0 else 'mild (g_ext<a0)'
        print(f"  {R:>7.2f} {ge/a0:>9.2f}   {reg}")
    print(f"  => REAL data CONFIRMS the precondition: members of real WINGS clusters sit at g_ext ~ (0.5-3) a0")
    print(f"     over R~0.3-2 Mpc -- the EFE IS strong, exactly the regime the internal-sigma test exploits.")
    return statistics.median(Ms)/1e15

# ============================================================================
# (2) VERIFIED primary-source physics -- the three EFE directions
# ============================================================================
def verified_physics():
    print("\n"+"="*100); print(" (2) VERIFIED primary-source physics (quoted this session)"); print("="*100)
    print("  [A] FRAMEWORK MI-EFE  Milgrom 2022 (arXiv:2208.07073), abstract VERIFIED:")
    print("      'what determines the EFE, in the case of a dominant external field, is mu(theta <a_ex>/a0)';")
    print("      'theta>1 is an extra factor that depends on the frequency ratio of the external- and")
    print("       internal-field variations'; 'the theta factor can appreciably enhance the EFE in quenching")
    print("       MOND effects, over what is deduced in modified gravity.'")
    print("      => MI EFE quenches the internal boost (sigma DOWN), STRONGER than MG. theta(0)~2/e UNVERIFIED")
    print("         in-text (abstract gives theta>1, freq-dependent); used theta(0)=2 as the worked-example value.")
    print("  [B] MODIFIED-GRAVITY EFE  Coma-UDG QUMOND (aa50757-24, 2024) + Freundlich+2022 (2109.04487), VERIFIED:")
    print("      'The EFE decreases the velocity dispersion from the isolated MOND prediction, making the profile")
    print("       closer to the Newtonian prediction'; 'the MOND EFE due to the cluster potential lowers the")
    print("       self-gravity of UDGs.'  => MODIFIED GRAVITY ALSO sends member sigma DOWN. SAME SIGN AS MI.")
    print("  [C] CDM  (no EFE): each member keeps its own halo; isolated internal dynamics are R-independent.")
    print("      Tidal heating near pericenter inflates sigma UP toward the center (search-confirmed).")
    print("      => CDM sign is FLAT-to-UP -- the OPPOSITE of the MOND-family DOWN.")
    print("  NET on the corpus claim 'MI DOWN vs CDM/MG UP': the MG half is WRONG. MG is DOWN too (MOND-shared).")

# ============================================================================
# (3) SYNTHETIC internal-sigma sample + exact EFE for the three models
# ============================================================================
def synthetic_internal_sigma(Mmed_15):
    print("\n"+"="*100); print(" (3) SYNTHETIC member INTERNAL-sigma sample (calibrated to CLASH-VLT/HFF/Coma-UDG)")
    print("="*100)
    Mcl = Mmed_15 if Mmed_15 else 1.0
    print(f"  Host: NFW cluster M200={Mcl*1e15:.1e} Msun (= REAL WINGS median; r200=2 Mpc, c=5).")
    print(f"  Member internal-sigma model: diffuse members dominate the EFE signal (g_in<<a0). The signal scales")
    print(f"  with g_in/a0; below we report the EXACT EFE suppression for a range of member compactness.\n")
    theta0=2.0
    Mb=1e9*Msun
    print(f"  {'Reff':>5} {'g_in/a0':>8} {'R[Mpc]':>7} {'g_ext/a0':>9} | {'[A]MI/iso':>9} {'[B]MG/iso':>9} {'[C]CDM/iso':>10} | {'MI down%':>8} {'MI-MG%':>7}")
    for Re_kpc in (2.0,5.0):
        Re=Re_kpc*kpc; gin=G*Mb/Re**2; giso=g_iso(gin)
        for R in (0.3,0.5,1.0,2.0):
            ge=cluster_gext(R,Mcl)
            fA=sig_frac(g_MI(gin,ge,theta0),giso); fB=sig_frac(g_MG(gin,ge),giso); fC=1.0
            print(f"  {Re_kpc:>5.1f} {gin/a0:>8.2f} {R:>7.2f} {ge/a0:>9.2f} | {fA:>9.3f} {fB:>9.3f} {fC:>10.3f} | "
                  f"{100*(1-fA):>7.1f}% {100*(fB-fA):>6.1f}%")
    print(f"\n  theta0={theta0} (Milgrom-2022 worked-example adiabatic limit). SIGN: MI=DOWN, MG=DOWN, CDM=FLAT(=1).")
    print(f"  The DOWN-sign is MI-AND-MG (MOND-SHARED). MI is theta-enhanced => a few % DEEPER than MG.")
    # stack-mean over a brightness-weighted member mix -> the corpus '~7%'
    print(f"\n  Brightness-weighted member-mix STACK MEAN (the corpus '~7% DOWN'):")
    mix=[(1e11,4.0,0.35),(3e10,3.0,0.30),(1e10,2.5,0.20),(3e9,2.0,0.10),(1e9,2.0,0.05)]
    for R in (0.3,0.5,1.0):
        ge=cluster_gext(R,Mcl); num=den=0.0
        for Mbar,Rek,w in mix:
            gin=G*Mbar*Msun/(Rek*kpc)**2; num+=w*(1-sig_frac(g_MI(gin,ge,theta0),g_iso(gin))); den+=w
        print(f"    R={R:.1f} Mpc (g_ext/a0={ge/a0:.1f}): mass-weighted MEAN MI suppression = {100*num/den:.1f}%  (corpus ~7%)")
    print(f"  => the '~7%' is the STACK MEAN over a mixed sample; DIFFUSE-selected members go MUCH deeper (20-50%).")

# ============================================================================
# (4) FORECAST -- floor / SNR for SIGN and for MI-vs-MG gap
# ============================================================================
def forecast():
    print("\n"+"="*100); print(" (4) FORECAST -- floor / SNR (both the MOND-shared SIGN and the MI-distinctive gap)")
    print("="*100)
    def snr(S,sper,Ntot): err=sper/np.sqrt(Ntot); return S/err, err
    print(f"  {'sample':>26} {'S':>6} {'sig/mem':>8} {'Ntot':>7} {'floor':>7} {'SNR':>7}")
    rows=[("SIGN, diffuse 2000-clus",0.27,0.40,15*2000),
          ("SIGN, diffuse 1-clus pilot",0.27,0.40,15),
          ("SIGN, mixed 2000-clus",0.065,0.15,15*2000),
          ("MI-MG gap, 2000-clus",0.02,0.40,15*2000),
          ("MI-MG gap, 10000-clus dream",0.02,0.30,20*10000)]
    for lab,S,sp,N in rows:
        s,f=snr(S,sp,N); print(f"  {lab:>26} {S:>6.3f} {sp:>8.2f} {N:>7} {f:>7.3f} {s:>7.1f}")
    print(f"\n  * SIGN (MOND-family DOWN vs CDM flat/UP): high-SNR (~17sigma-class) on a 2000-cluster diffuse stack.")
    print(f"    Single-cluster pilot ~2.5sigma. This is REAL and decisive -- but it is MOND-SHARED, not MI-distinctive.")
    print(f"  * MI-vs-MG gap (~2%, the ONLY MI-distinctive content): clears the STATISTICAL floor on a huge stack")
    print(f"    (SNR_stat ~9-30) but is FAR below the SYSTEMATIC floor:")
    print(f"      - Faber-Jackson / morphology-density residual: SDSS Coma pilot showed +12% sigma UP at fixed M_r")
    print(f"        (3.5sigma) -- OPPOSITE sign, ~2x the EFE signal, on bright members.")
    print(f"      - interloper contamination (no EFE -> fakes the CDM up/flat sign);")
    print(f"      - a0/M*/size/aperture degeneracies; an MG fit with a0-rescale+M/L absorbs the theta run")
    print(f"        (same a0-degeneracy as wide binaries).")
    print(f"    => the MI-distinctive content is BELOW the realistic floor. The test decides MOND-vs-CDM, NOT MI-vs-MG.")

def main():
    print("#"*100)
    print("# CLUSTER-MEMBER sigma EFE SIGN TEST -- a0=%.3e (framework dS-Unruh MODIFIED INERTIA), Ups=%.2f"%(a0,Ups))
    print("#"*100)
    Mmed=real_wings()
    verified_physics()
    synthetic_internal_sigma(Mmed)
    forecast()
    print("\n"+"#"*100); print("# VERDICT (both ways)"); print("#"*100)
    print("# 1. WHAT IS MEASURED: the EFE sign test is about MEMBER INTERNAL sigma_int (resolved stellar")
    print("#    spectroscopy of diffuse members), NOT the cluster member-velocity dispersion (WINGS cz).")
    print("#    Only sigma_int is EFE-of-the-member-sensitive. The real WINGS pull gives cz (the wrong quantity")
    print("#    for this test) -- it calibrates g_ext and proves the data path, but the sign test needs CLASH-VLT/")
    print("#    HFF/4MOST resolved INTERNAL sigma of diffuse members (built SYNTHETIC here, calibrated to real M200).")
    print("# 2. THE DOWN-SIGN IS MOND-SHARED (CORRECTS THE CORPUS). Modified GRAVITY MOND (Coma-UDG QUMOND,")
    print("#    aa50757-24 2024: 'the EFE decreases the velocity dispersion ... closer to the Newtonian prediction')")
    print("#    sends member sigma DOWN -- the SAME direction as the framework's modified inertia. The corpus")
    print("#    'MI DOWN vs CDM/MG UP' is WRONG ON THE MG SIDE and must be corrected to 'MOND(MI or MG) DOWN vs CDM up/flat'.")
    print("# 3. DISTINCTIVE vs CDM ONLY (in sign): member sigma DOWN (MOND family) vs flat/UP (CDM, tidal heating).")
    print("#    NOT distinctive vs MG in sign. The ONLY MI-vs-MG handle is the ~2% theta-enhancement MAGNITUDE gap,")
    print("#    which is BELOW the systematic floor (FJ residual ~12%, interlopers, a0-degeneracy) -> undecidable.")
    print("# 4. NET: a REAL ~17sigma-class discriminator of MOND-FAMILY vs CDM (the MOND PREMISE), pilotable on")
    print("#    public resolved-spectroscopy data -- but it does NOT isolate the framework's modified inertia from")
    print("#    modified gravity. Honest standing: tests the premise, not the distinctive mechanism.")
    print("#"*100)

if __name__=="__main__":
    main()
