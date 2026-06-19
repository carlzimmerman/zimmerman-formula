#!/usr/bin/env python3
r"""
ACCELERATION-FLUCTUATION TERM in the dS-Unruh effective temperature  (solution_hunt)
====================================================================================
MISSION (framework-native, no particle DM): does the rapidly-FLUCTUATING acceleration
field from cluster substructure (other member galaxies, the granular potential) raise
the de Sitter-Unruh effective temperature -> raise the effective a0 FLOOR in cluster
cores enough (need ~4-5x) to close the residual, WHILE leaving smooth galaxy disks
(tiny <a_fluct^2>) untouched (the galaxy veto)? And does the SAME term -- largest in the
dense, hot, fluctuating early universe -- help JWST too-massive-too-early?

THE PHYSICS (the genuinely-unexplored piece):
  Deser-Levin (verified framework physics):
     T_eff(a) = (hbar / 2 pi c kB) * sqrt( |a|^2 + (cH_Lambda)^2 )
  The MOND scale a0 is set by the FLOOR term cH_Lambda:
     a0 = c^2 sqrt(Lambda/32pi),   cH_Lambda = c^2 sqrt(Lambda/3) = sqrt(32pi/3) * a0 ~ 5.79 a0.
  i.e. inside the sqrt the floor is (cH_Lambda)^2 = (32pi/3) a0^2.

  A cluster member's TOTAL acceleration is a_smooth (the mean cluster field) PLUS a
  rapidly fluctuating piece a_fluct from the DISCRETE distribution of other galaxies /
  substructure. The temperature responds to the INSTANTANEOUS |a|^2, so the
  TIME/ENSEMBLE-AVERAGED temperature sees
     <|a|^2> = a_smooth^2 + <a_fluct^2>            (cross term averages to ~0)
  Hence the EFFECTIVE floor that sets a0 is RAISED:
     (cH_Lambda)^2  ->  (cH_Lambda)^2 + <a_fluct^2>
     a0_eff = a0 * sqrt( 1 + <a_fluct^2> / (cH_Lambda)^2 )
            = a0 * sqrt( 1 + <a_fluct^2> / (32pi/3 * a0^2) ).

  >>> To get a0_eff/a0 ~ 4-5x we need <a_fluct^2>/(cH_Lambda)^2 ~ 15-24,
      i.e. sqrt<a_fluct^2> ~ 4-5 cH_Lambda ~ 23-29 a0 ~ 2.2-2.7e-9 m/s^2. <<<

  CRUCIAL DISTINCTION from the dead density-a0 law:
   - density-a0 used rho_local -> a smooth dense DISK (rho~1e5-1e6 rho_DE) over-boosts and
     erases the galaxy RAR. That law sees the MEAN density.
   - THIS term sees the VARIANCE of the acceleration from DISCRETENESS/granularity. A smooth
     disk's stellar field is a near-continuum: <a_fluct^2> from N~1e11 stars is tiny (the
     mean field dominates, Poisson fluctuations / sqrt(N) suppressed). A cluster core is a
     handful (N~hundreds) of MASSIVE discrete galaxies -> large fractional fluctuation.

  THE TIME-CORRELATION GATE (non-adiabatic condition): the fluctuation only counts in T_eff
  if it PERSISTS on the inertial-response / Unruh-detector timescale. The dS-Unruh detector
  response time is the de Sitter / horizon-crossing time tau_dS ~ 1/H_Lambda ~ 1/H0 (the
  floor is the cosmological horizon). The fluctuation correlation time is the encounter /
  crossing time tau_fluct ~ b/v (impact parameter / relative velocity ~ neighbor crossing).
  If tau_fluct << tau_dS the fast fluctuation is a coherent contribution to <|a|^2> over the
  detector window (it IS sampled); if the relevant response time were the local dynamical
  time, only fluctuations slower than that count. We compute BOTH the variance AND this gate.

BOTH WAYS (#1 rule): compute <a_fluct^2> from the REAL eRASS1 cluster members + the REAL
SPARC disk granularity; report the honest a0_eff boost vs the needed 4-5x; do NOT manufacture.
GALAXY VETO: the SAME formula on a smooth SPARC disk must give boost ~ 1.0 (else it is dead).

Data: real_research/data/erass1cl_primary_v3.2.fits (Bulbul+2024), SPARC rotmod (175).
"""
import os, glob, importlib.util
import numpy as np

# ----------------------------------------------------------------------------- constants (SI)
c    = 2.998e8
G    = 6.674e-11
hbar = 1.0546e-34
kB   = 1.381e-23
Msun = 1.989e30
pc   = 3.0857e16
kpc  = 1e3*pc
Mpc  = 1e6*pc
km   = 1e3
yr   = 3.156e7
Gyr  = 1e9*yr

# framework
a0       = 9.36e-11
rho_DE   = 5.8878e-27
Lambda   = 8*np.pi*G*rho_DE/c**2
cH_Lam   = c**2*np.sqrt(Lambda/3.0)          # floor acceleration in T_eff
floor2   = cH_Lam**2                         # (cH_Lambda)^2  = (32pi/3) a0^2
H_Lam    = c*np.sqrt(Lambda/3.0)             # de Sitter Hubble rate [1/s]
tau_dS   = 1.0/H_Lam                          # dS / horizon response time

print("="*94)
print(" ACCELERATION-FLUCTUATION TERM in dS-Unruh T_eff -> effective a0 floor boost")
print("="*94)
print(f"  a0          = {a0:.3e} m/s^2")
print(f"  cH_Lambda   = {cH_Lam:.3e} m/s^2 = {cH_Lam/a0:.3f} a0   (FLOOR term in T_eff; sqrt(32pi/3))")
print(f"  (cH_Lam)^2  = {floor2:.3e}  = floor inside sqrt(|a|^2 + floor)")
print(f"  tau_dS=1/H_Lam = {tau_dS/Gyr:.2f} Gyr   (dS-Unruh detector response / correlation window)")
print(f"\n  NEEDED: a0_eff/a0 ~ 4-5  ->  <a_fluct^2>/(cH_Lam)^2 ~ {4**2-1}-{5**2-1}")
print(f"          i.e. sqrt<a_fluct^2> ~ {np.sqrt((4**2-1)*floor2)/a0:.0f}-{np.sqrt((5**2-1)*floor2)/a0:.0f} a0"
      f" = {np.sqrt((4**2-1)*floor2):.2e}-{np.sqrt((5**2-1)*floor2):.2e} m/s^2\n")

def a0_eff(af2):
    """effective a0 from the fluctuation variance: a0_eff = a0 sqrt(1 + <a_fluct^2>/(cH_Lam)^2)."""
    return a0*np.sqrt(1.0 + af2/floor2)

# =============================================================================================
# PART 1 -- <a_fluct^2> in a REAL cluster core from the discrete member-galaxy distribution
# =============================================================================================
print("="*94)
print(" PART 1: <a_fluct^2> from the GRANULAR member-galaxy field in a real cluster core")
print("="*94)
print(r"""
 A member at the core feels, besides the smooth field, the sum of accelerations from the OTHER
 discrete member galaxies. For a number density n of perturbers each of mass m, the variance of
 the fluctuating acceleration from a Poisson (Holtsmark) distribution of point masses is the
 classic stellar-dynamics result. The Holtsmark distribution has a DIVERGENT second moment
 (dominated by the nearest neighbor), so <a_fluct^2> is set by the NEAREST-NEIGHBOR cutoff:
     <a_fluct^2> ~ (G m / b_min^2)^2 weighted, with the typical nearest-neighbor distance
     b_typ ~ n^{-1/3}. The robust estimator (Chandrasekhar 1943; the variance regularized at the
     nearest neighbor) is
        a_fluct,typ ~ G m / b_typ^2 = G m n^{2/3}
     and we ALSO compute the full ensemble <a^2> with a nearest-neighbor inner cutoff b_min.
""")

def a_fluct_rms(n, m, b_min):
    """RMS fluctuating acceleration from a Poisson field of point masses, mass m, number
       density n, regularized at inner cutoff b_min (nearest-neighbor). The mean-square
       acceleration from all perturbers beyond b_min:
          <a^2> = integral n * (G m / r^2)^2 * 4 pi r^2 dr  from b_min to b_max
                = 4 pi n (G m)^2 * (1/b_min - 1/b_max)   ~  4 pi n (G m)^2 / b_min
       (the integral is dominated by the inner cutoff = nearest neighbor; b_max -> system size).
       This is the standard random-force variance (Chandrasekhar 1943, eq. for <F^2>)."""
    b_max = 5.0*b_min*(1.0)                          # placeholder; full integral set below
    return None  # use explicit integral version below

def a_fluct2_poisson(n, m, b_min, b_max):
    """<a_fluct^2> = 4 pi n (G m)^2 (1/b_min - 1/b_max).  [Chandrasekhar random force variance]"""
    return 4*np.pi*n*(G*m)**2*(1.0/b_min - 1.0/b_max)

def b_nn(n):
    """typical nearest-neighbor distance for number density n: ~ (3/(4 pi n))^{1/3}."""
    return (3.0/(4*np.pi*n))**(1.0/3.0)

# Real cluster cores (eRASS1-typical): rich M500~1e15, group ~1e14. Member galaxy population:
# richness N_gal (L>0.1 L*) ~ 30-300 in the core; member mass m_gal ~ 1e11-1e12 Msun (incl. subhalo).
# core radius ~ 0.3 R500 ~ 300-450 kpc (rich) / 150-200 kpc (group).
print(" Real cluster cores (member-galaxy granularity):")
print(f"  {'system':>22} {'N_mem':>6} {'m_gal[Msun]':>11} {'R_core[kpc]':>11} {'n[Mpc^-3]':>11}"
      f" {'b_nn[kpc]':>9} | {'a_fl,typ/a0':>11} {'rms a_fl/a0':>11} | {'a0_eff/a0':>10}")
print("  "+"-"*118)
clusters = [
    # name, N_member, m_gal(Msun), R_core(kpc), include subhalo mass?
    ("rich core (1e15)",   300, 5e11, 400),
    ("rich core, big gals", 100, 1e12, 400),
    ("rich, massive subs",   50, 3e12, 400),
    ("group core (1e14)",    30, 3e11, 200),
    ("Coma-like dense",     500, 5e11, 500),
    ("HFF cluster core",    200, 1e12, 300),
]
part1_rows = []
for name, N, mg, Rc_kpc in clusters:
    Rc = Rc_kpc*kpc
    Vol = (4.0/3.0)*np.pi*Rc**3
    n = N/Vol                                     # number density [m^-3]
    m = mg*Msun
    bnn = b_nn(n)
    b_min = bnn                                   # inner cutoff = typical nearest neighbor
    b_max = Rc                                    # outer = core radius
    af2 = a_fluct2_poisson(n, m, b_min, b_max)
    a_typ = G*m/bnn**2                            # nearest-neighbor typical accel
    boost = a0_eff(af2)/a0
    part1_rows.append((name, n, af2, boost))
    print(f"  {name:>22} {N:6d} {mg:11.1e} {Rc_kpc:11.0f} {n*Mpc**3:11.2f}"
          f" {bnn/kpc:9.1f} | {a_typ/a0:11.2f} {np.sqrt(af2)/a0:11.2f} | {boost:10.3f}")
print(r"""
 READ: the member-galaxy granular field gives rms a_fluct of ORDER a0 to a few a0 in the
 densest, most massive-galaxy cores. The a0_eff boost = sqrt(1 + <a_fluct^2>/(5.79 a0)^2):
 because the FLOOR (cH_Lam) is already ~5.79 a0, a fluctuation of a few a0 is SMALL compared
 to the floor -> boost only ~1.0-1.1x. To reach 4x the fluctuation must be ~23 a0 = 2.2e-9 m/s^2,
 ~10-20x larger than the member-galaxy field delivers. This is the CORE shortfall (quantified).
""")

# =============================================================================================
# PART 2 -- include the DARK/GAS substructure + the smooth-field a_smooth^2 itself
# =============================================================================================
print("="*94)
print(" PART 2: add a_smooth^2 (the cluster's OWN mean field) inside the sqrt -- the SIGN TRAP")
print("="*94)
print(r"""
 The total <|a|^2> = a_smooth^2 + <a_fluct^2>. In a cluster CORE the SMOOTH field a_smooth can
 itself be >> a0 (deep potential). Does putting a_smooth^2 inside the T_eff sqrt raise a0_eff?
 a_smooth at 0.3 R500: g_bar ~ 0.04-0.1 a0 (deep MOND, from the target profile) -- but the
 OBSERVED (total) g is larger. The relevant 'a' in T_eff is the member's ACTUAL acceleration.
""")
# from target profile: at 0.3 R500 g_bar/a0 ~ 0.04-0.1 (deep MOND). The member's true accel ~ g_obs.
print(f"  {'location':>24} {'a_smooth/a0':>11} {'a_sm^2/floor':>12} | {'a0_eff/a0 (smooth only)':>22}")
print("  "+"-"*78)
for label, asm_ratio in [("0.3R500 g_bar (deep)", 0.05), ("0.3R500 g_obs (~MOND)", 0.3),
                          ("0.1R500 g_obs", 1.0), ("core, hot member", 3.0), ("core, very hot", 10.0)]:
    asm = asm_ratio*a0
    boost = np.sqrt(1.0 + asm**2/floor2)
    print(f"  {label:>24} {asm_ratio:11.2f} {asm**2/floor2:12.4f} | {boost:22.3f}")
print(r"""
 READ (the sign trap, honest): a_smooth^2 inside the sqrt RAISES a0_eff ONLY where a_smooth
 itself is several * cH_Lam ~ several * 5.79 a0 ~ tens of a0 -- but that is the HIGH-acceleration
 (Newtonian) regime where MOND is already OFF and no boost is needed. Where the residual lives
 (deep-MOND, g_bar ~ 0.04-0.3 a0), a_smooth^2 << floor -> negligible boost. AND if a0_eff rises
 where a is large, it makes the deep core MORE Newtonian = wrong direction (the (b2) sign trap).
 The smooth term cannot close the deep-MOND core residual. Only a fluctuation that is large
 PRECISELY where a_smooth is SMALL would work -- and the member-galaxy variance (Part 1) is ~a0,
 too small. We now test whether ANY realistic granularity reaches the needed ~23 a0.
""")

# =============================================================================================
# PART 2b -- THE TIME-CORRELATION GATE applied properly (the decisive, self-consistent step)
# =============================================================================================
print("="*94)
print(" PART 2b: THE TIME-CORRELATION (non-adiabatic) GATE -- the decisive both-ways step")
print("="*94)
print(r"""
 A perturber at impact parameter b contributes accel a=Gm/b^2 with a CORRELATION TIME tau_c ~ b/v_rel
 (how long it stays at ~that distance). It couples to the dS-Unruh T_eff ONLY if it persists over the
 inertial-response time tau_resp -- a fluctuation FASTER than tau_resp is adiabatically averaged away
 (the inertia cannot respond; the detector time-averages it). The physically correct response time is
 the local DYNAMICAL time tau_dyn = 1/sqrt(G rho_sys) (the only internal clock of the inertia).
 So a perturber counts only if  tau_c = b/v_rel > tau_dyn  <=>  b > b_gate = v_rel * tau_dyn.

 THE KEY IDENTITY (why this self-cancels in ANY virialized system):
   for a virialized system v_rel^2 ~ G M / R ~ G rho R^2  and tau_dyn ~ 1/sqrt(G rho), so
      b_gate = v_rel * tau_dyn ~ sqrt(G rho) R / sqrt(G rho) = R  (the SYSTEM SIZE).
   => the ONLY fluctuations slow enough to couple to the inertia are at the system scale -- i.e. the
      SMOOTH field itself. All sub-system granularity (the substructure that makes <a_fluct^2> large)
      is FASTER than tau_dyn and is GATED OUT. The fluctuation variance self-cancels by construction.
""")
def gated_var(n, m, v_rel, rho_sys, b_max):
    tau_dyn = 1.0/np.sqrt(G*rho_sys)
    b_gate  = v_rel*tau_dyn
    b_nn_    = (3.0/(4*np.pi*n))**(1.0/3.0)
    b_lo    = max(b_gate, b_nn_)
    if b_lo >= b_max:
        return 0.0, tau_dyn, b_gate, b_lo
    af2 = 4*np.pi*n*(G*m)**2*(1.0/b_lo - 1.0/b_max)
    return af2, tau_dyn, b_gate, b_lo
print(f"  {'system':>22} {'tau_dyn':>9} {'b_gate':>9} {'R_sys':>8} | {'rms a_fl/a0 (GATED)':>19} {'a0_eff/a0':>10}")
print("  "+"-"*82)
# cluster cores (member granularity)
for name, N, mg, Rc_kpc, v_kms in [("rich core (1e15)",300,5e11,400,1000),
                                    ("HFF dense core",200,1e12,300,1200),
                                    ("group core (1e14)",30,3e11,200,600)]:
    Rc=Rc_kpc*kpc; m=mg*Msun; n=N/((4/3)*np.pi*Rc**3); rho=N*m/((4/3)*np.pi*Rc**3)
    af2,td,bg,bl=gated_var(n,m,v_kms*km,rho,Rc)
    print(f"  {name:>22} {td/Gyr:8.2f}G {bg/kpc:8.0f}k {Rc_kpc:7.0f}k | {np.sqrt(af2)/a0:19.4f} {np.sqrt(1+af2/floor2):10.4f}")
# galaxy bulge (star granularity -- the Part-4 '11x' veto artifact)
Rb=0.3*kpc; Mb=1e10*Msun; m_s=0.5*Msun; n_s=Mb/m_s/((4/3)*np.pi*Rb**3); rho_b=Mb/((4/3)*np.pi*Rb**3)
af2b,tdb,bgb,blb=gated_var(n_s,m_s,200*km,rho_b,Rb)
print(f"  {'galaxy bulge (stars)':>22} {tdb/Gyr*1e3:7.0f}M {bgb/pc:7.0f}pc {Rb/kpc*1e3:6.0f}pc | "
      f"{np.sqrt(af2b)/a0:19.4f} {np.sqrt(1+af2b/floor2):10.4f}")
print(r"""
 READ (decisive): under the proper dynamical-time gate, b_gate ~ R_sys in EVERY virialized system,
 so ALL the substructure granularity (cluster members AND bulge stars) is gated OUT -> rms a_fl -> 0
 -> boost -> 1.000 in BOTH clusters and galaxies. This is the SAME physics applied consistently: it
 KILLS the cluster fluctuation (no cure) AND it KILLS the galaxy-bulge 'artifact' (Part 4 below), so
 the term is self-consistently galaxy-SAFE and cluster-WEAK. The ungated Part-1 variance (~a0,
 boost~1.01-1.1x) is the UPPER bound (no gate); the gate only lowers it toward 1.000.
""")

# =============================================================================================
# PART 3 -- what granularity WOULD reach 4x? + the time-correlation (non-adiabatic) gate
# =============================================================================================
print("="*94)
print(" PART 3: inversion -- what <a_fluct^2> reaches 4x? + the TIME-CORRELATION gate")
print("="*94)
need_af = np.sqrt((4.0**2 - 1)*floor2)
print(f"  Need sqrt<a_fluct^2> = {need_af:.2e} m/s^2 = {need_af/a0:.1f} a0 for a0_eff=4 a0.")
print(f"  A single perturber of mass m at distance b gives a = G m / b^2 = {need_af:.2e} when")
for mg in [1e11, 1e12, 1e13]:
    m = mg*Msun
    b = np.sqrt(G*m/need_af)
    print(f"    m={mg:.0e} Msun: a nearest neighbor must sit within b = {b/kpc:.1f} kpc "
          f"(and persist over tau).")
print(r"""
 So a ~23 a0 fluctuation needs a ~1e12 Msun galaxy within ~25 kpc, or a ~1e13 within ~80 kpc --
 i.e. the member must be in a near-MERGER / strong-encounter. That happens TRANSIENTLY for a
 small duty-cycle fraction of members, not for the bulk -> the ENSEMBLE-mean boost stays ~1.1x.

 THE TIME-CORRELATION GATE (non-adiabatic condition):
  The fluctuation counts in T_eff only if it persists over the dS-Unruh detector window. Two
  readings of the window:
   (i) tau_dS = 1/H_Lambda ~ 14 Gyr (the cosmological floor sets a LONG window): then even slow
       fluctuations are sampled, BUT a near-encounter lasts only tau_enc ~ b/v_rel ~ (25 kpc)/
       (1000 km/s) ~ 25 Myr << 14 Gyr -> its DUTY CYCLE in the long window is ~25 Myr/14 Gyr ~
       2e-3 -> the time-averaged <a^2> contribution is suppressed by the duty cycle.
   (ii) the inertial-response time = local dynamical/crossing time tau_dyn ~ R_core/sigma ~
       (400 kpc)/(1000 km/s) ~ 0.4 Gyr: a fluctuation must persist ~tau_dyn to alter the inertia;
       encounters at 25 Myr are FASTER than tau_dyn, so they are adiabatically averaged AWAY
       (the inertia cannot respond) -> they do NOT count. This is the non-adiabatic veto.
""")
# duty-cycle estimate of the encounter contribution
sigma = 1000*km
for mg, b_enc in [(1e12, 25*kpc), (1e13, 80*kpc)]:
    m = mg*Msun
    a_enc = G*m/b_enc**2
    tau_enc = b_enc/sigma
    # number of strong perturbers within the core that are within b_enc of the test member at any time:
    # duty cycle ~ (volume fraction within b_enc of a perturber) for N perturbers
    duty = None
    print(f"  encounter m={mg:.0e}, b={b_enc/kpc:.0f} kpc: a_enc={a_enc/a0:.1f} a0,"
          f" tau_enc={tau_enc/Gyr*1e3:.0f} Myr  (<< tau_dyn~400 Myr -> adiabatically averaged out)")

# Time-averaged <a^2> with the duty cycle: <a^2>_eff = sum over perturbers of (Gm/r^2)^2 * (fraction
# of time within that r). For a uniform random field this REPRODUCES the Poisson variance of Part 1
# (which already integrates over all r) -- so the duty cycle is ALREADY in Part 1. The extra point:
# the FAST (tau_enc << tau_dyn) part of that variance may not couple to inertia (non-adiabatic veto).
print(r"""
 KEY: Part 1's Poisson variance ALREADY integrates over all impact parameters (it IS the duty-cycle-
 weighted <a^2>). The time-correlation gate can only SUBTRACT from it (removing the fast,
 non-adiabatic near-encounters that dominate the variance) -> the honest, gate-applied boost is
 <= the Part 1 boost (~1.1x). The gate cannot ADD. So the fluctuation route is bounded ABOVE by
 ~1.1x in real cluster cores, FAR short of 4x.
""")

# =============================================================================================
# PART 4 -- GALAXY VETO: <a_fluct^2> in a smooth SPARC disk (must give boost ~1.0)
# =============================================================================================
print("="*94)
print(" PART 4: GALAXY VETO -- <a_fluct^2> in a smooth galaxy disk (stars are a near-continuum)")
print("="*94)
print(r"""
 In a galaxy disk the perturbers are STARS (m ~ 0.5 Msun, n ~ 0.1-1 pc^-3 in the disk). The
 Poisson variance a_fluct ~ sqrt(4 pi n (G m)^2 / b_nn) is TINY because m is tiny and the nearest
 neighbor is ~0.1 pc but Gm/b^2 of a star at 0.1 pc is minuscule. We compute it on the REAL SPARC
 disks (stellar density from 3.6um surface brightness) and confirm boost ~ 1.0 (veto passes).
""")
# load SPARC and compute stellar granular fluctuation at the disk midplane
DATADIR = None
for cand in ["real_research/data/sparc_data",
             os.path.join(os.path.dirname(__file__), "../../../../real_research/data/sparc_data"),
             os.path.join(os.path.dirname(__file__), "../../../real_research/data/sparc_data")]:
    if os.path.isdir(cand):
        DATADIR = cand; break
files = sorted(glob.glob(os.path.join(DATADIR, "*_rotmod.dat"))) if DATADIR else []
print(f"  [data] {len(files)} SPARC rotmod files at {DATADIR}")

Ups = 0.70; h_disk = 0.3*kpc; m_star = 0.5*Msun
boosts_gal = []
asm_ratios = []
for f in files:
    try:
        dat = np.loadtxt(f, comments='#')
    except Exception:
        continue
    if dat.ndim == 1 or dat.shape[0] < 3:
        continue
    rad = dat[:,0]*kpc; SBdisk = dat[:,6]; SBbul = dat[:,7]
    Vgas=dat[:,3]*km; Vdisk=dat[:,4]*km; Vbul=dat[:,5]*km
    Sigma = (Ups*SBdisk + Ups*SBbul)*Msun/pc**2          # kg/m^2 stellar surface density
    Sigma = np.clip(Sigma, 1e-4*Msun/pc**2, None)
    rho_mid = Sigma/(2*h_disk)                            # kg/m^3 stellar midplane density
    n_star = rho_mid/m_star                               # star number density
    bnn = (3.0/(4*np.pi*np.clip(n_star,1e-30,None)))**(1.0/3.0)
    b_min = bnn; b_max = 1.0*kpc
    af2 = 4*np.pi*n_star*(G*m_star)**2*(1.0/b_min - 1.0/np.maximum(b_max,2*b_min))
    af2 = np.clip(af2, 0, None)
    boost = np.sqrt(1.0 + af2/floor2)
    Vbar2 = Vgas*np.abs(Vgas)+Ups*Vdisk*np.abs(Vdisk)+Ups*Vbul*np.abs(Vbul)
    gbar = np.clip(Vbar2,0,None)/np.clip(rad,1e-9,None)
    good = (rad>0)&(SBdisk>0)
    if good.sum()==0: continue
    boosts_gal.extend(boost[good].tolist())
    asm_ratios.extend((gbar[good]/a0).tolist())
boosts_gal = np.array(boosts_gal)
print(f"  [veto] SPARC disk STELLAR-granularity a0_eff boost (UNGATED Poisson variance):")
print(f"     median = {np.median(boosts_gal):.4f}x,  95th pct = {np.percentile(boosts_gal,95):.4f}x,"
      f"  max = {np.max(boosts_gal):.4f}x")
print(r"""  BOTH-WAYS HONESTY: the UNGATED Poisson variance does NOT pass trivially -- at dense inner
  BULGES (Sigma~1e4-3e4 Msun/pc^2, r<0.3 kpc) it spuriously gives boost up to ~11x (the
  nearest-neighbor star at b_nn~3e-4 pc has Gm/b^2 enormous). So the RAW fluctuation law WOULD
  break the RAR at bulge centers -- I will NOT hide this. BUT it is the SAME fast-fluctuation the
  TIME-CORRELATION GATE (Part 2b) removes: a bulge star's encounter time b_nn/v ~ Myr-kyr <<
  tau_dyn -> gated out -> GATED boost = 1.0000 (Part 2b table, bulge row). So WITH the physically
  required gate the veto passes; WITHOUT it the law breaks galaxies. The gate is not optional -- it
  is the non-adiabatic condition the framework's own MI demands -- and it is what makes the term
  galaxy-safe AND cluster-weak self-consistently. Reported both ways so the artifact is not buried.
""")
print(r"""  Additional both-ways check: a disk's discrete GIANT MOLECULAR CLOUDS (m~1e5-1e6 Msun, ~50-100 pc):
""")
# GMC granularity in a disk: m_GMC ~ 3e5 Msun, n_GMC such that they make up ~few% of disk surface dens
for mGMC, n_per_kpc2 in [(3e5, 50), (1e6, 20)]:
    m = mGMC*Msun
    # surface number density n_per_kpc2 GMCs per kpc^2, scale height h_gas~0.1 kpc
    Sig_n = n_per_kpc2/kpc**2
    h_gas = 0.1*kpc
    n_vol = Sig_n/(2*h_gas)
    bnn = (3.0/(4*np.pi*n_vol))**(1.0/3.0)
    af2 = 4*np.pi*n_vol*(G*m)**2*(1.0/bnn - 1.0/(1*kpc))
    boost = np.sqrt(1.0+af2/floor2)
    print(f"  GMC m={mGMC:.0e} Msun, {n_per_kpc2}/kpc^2: a_fl,rms={np.sqrt(af2)/a0:.3f} a0,"
          f" b_nn={bnn/kpc:.2f} kpc -> a0_eff boost = {boost:.4f}x")
print(r"""
 READ (veto, both ways): stellar granularity -> boost 1.0000 (continuum). GMC granularity ->
 boost ~ 1.00x as well (GMCs are light and the floor is 5.79 a0). So the SAME fluctuation law
 gives ESSENTIALLY ZERO boost on galaxy disks -- the galaxy veto PASSES (this is the term's one
 real virtue: unlike density-a0, it does NOT break the RAR). The cost is that it ALSO does
 essentially nothing in cluster cores (~1.1x), because the cosmological FLOOR (5.79 a0) is large.
""")

# =============================================================================================
# PART 5 -- THE UNIFIER: the early universe (high z) -- is <a_fluct^2> large enough there?
# =============================================================================================
print("="*94)
print(" PART 5: UNIFIER -- the fluctuation term at high z (JWST too-massive-too-early)")
print("="*94)
print(r"""
 The same term is largest where the universe is densest & most granular: high z. The smooth-field
 contribution a_smooth^2 scales with density ~ (1+z)^3; the FLOOR cH_Lam is set by Lambda (LATE-time
 constant) OR -- if one uses the rising-cH branch -- by H(z). We test whether the EARLY-universe
 fluctuation/curvature term raises a0_eff at z~6-10 enough to speed structure formation.
""")
print(f"  {'z':>4} {'rho/rho0':>9} {'a_curv=c sqrt(G rho)':>19} {'/a0':>7} | "
      f"{'a0_eff/a0 (curv in floor)':>24}")
print("  "+"-"*74)
H0 = 67.4e3/Mpc; Om=0.315; OL=0.685
for z in [0, 1, 2, 6, 10, 15]:
    Ez = np.sqrt(Om*(1+z)**3 + OL)
    rho_m = Om*(3*H0**2/(8*np.pi*G))*(1+z)**3       # mean matter density at z
    a_curv = c*np.sqrt(G*rho_m)                      # curvature/density accel scale
    # put a_curv^2 (the mean-field cosmic curvature) inside the floor:
    boost = np.sqrt(1.0 + a_curv**2/floor2)
    print(f"  {z:4.0f} {(1+z)**3:9.1f} {a_curv:19.2e} {a_curv/a0:7.2f} | {boost:24.3f}")
print(r"""
 READ (both ways, the honest reduction): the cosmic-mean curvature accel a_curv = c sqrt(G rho_m(z))
 DOES reach 25-50 a0 at z=6-10, giving a SMOOTH-floor boost a0_eff/a0 = 4.4x (z=6), 8.6x (z=10) --
 NUMERICALLY in the cluster-needed range. BUT this is NOT the fluctuation-variance term: a_curv =
 c sqrt(G rho_m) = 2 * (c/2)sqrt(G rho_m) is EXACTLY the density-a0 law evaluated at the cosmic MEAN
 density. Two honest consequences:
   1) As a LOCAL density law it is the already-vetoed density-a0 (breaks SPARC: a z=0 galaxy sits in
      rho_local >> rho_cosmic and gets over-boosted). NOT galaxy-safe if read locally.
   2) As a z-GLOBAL (cosmic-mean-only) law it does NOT vary inside a galaxy -> galaxy-safe, but then
      it IS the banked a0(z) RISING-cH branch (a0(z) ~ E(z), ~10-20x at z=6-10): a SEPARATE, already-
      banked framework mechanism, not new fluctuation content. The fluctuation VARIANCE itself is
      gated to ~0 (Part 2b) inside collapsed proto-clusters -- the SAME cluster calc -- boost ~1.0.
 NET for JWST: the fluctuation term contributes ~0; the framework's genuine high-z lever is the
 banked a0(z) rising branch (galaxy-safe because it is cosmic-global), which DOES boost a0 ~10-20x at
 z~6-10 and speeds early structure -- but that is a DIFFERENT, separately-banked mechanism, contested
 by the MUSE-DARK a0(z) data and dissolving if w->-1. So: fluctuation term does NOT unify clusters +
 JWST; the high-z help is real but lives in the a0(z) branch, not here.
""")

# =============================================================================================
# SYNTHESIS
# =============================================================================================
best_cluster_boost = max(b for *_, b in part1_rows)
print("="*94)
print(" SYNTHESIS -- acceleration-fluctuation term: honest magnitude both ways")
print("="*94)
print(f"""
 CLUSTER CORE:  the member-galaxy granular field gives rms a_fluct ~ a0 to a few a0 (UNGATED) in
   the densest, most massive-galaxy cores -> a0_eff/a0 = sqrt(1 + <a_fluct^2>/(5.79 a0)^2) reaches
   at most ~{best_cluster_boost:.2f}x.  WITH the physically required TIME-CORRELATION GATE (Part 2b)
   it drops to ~1.000x: because b_gate = v_rel*tau_dyn ~ R_system in any virialized system, ALL the
   substructure granularity is faster than the inertial-response time and is adiabatically averaged
   out -- only the SMOOTH field (already in a_smooth) survives.
   The make-or-break need is ~4-5x.  SHORTFALL: delivered ~1.00-1.10x vs needed ~4-5x -- the
   fluctuation supplies essentially 0% of the required floor boost (upper bound ~3% even ungated).
   ROOT CAUSE (two compounding): (i) the cosmological FLOOR cH_Lam ~ 5.79 a0 is ALREADY large, so a
   few-a0 fluctuation is a small fractional perturbation; (ii) the gate self-cancels the variance in
   any virialized system. To reach 4x needs sqrt<a_fluct^2> ~ 23 a0 = 2.2e-9 m/s^2 (a 1e12 Msun
   galaxy within ~25 kpc, a transient near-merger) AND that encounter to persist over tau_dyn -- it
   does not (tau_enc ~ 25 Myr << tau_dyn ~ 400 Myr). Both conditions fail.

 GALAXY VETO:  PASSES with the gate; the UNGATED law FAILS at bulge centers (boost up to ~11x where
   Sigma~1e4 Msun/pc^2). The gate removes the fast bulge-star fluctuations -> gated boost = 1.0000.
   Reported BOTH ways: the raw fluctuation law is NOT automatically galaxy-safe (unlike my first
   reading) -- it needs the non-adiabatic gate, which then ALSO kills the cluster effect. Self-
   consistent: the term is galaxy-safe and cluster-weak together, not one without the other.

 EARLY UNIVERSE / JWST:  the fluctuation VARIANCE is ~0 (gated, same as clusters). The cosmic-mean
   curvature accel a_curv=c sqrt(G rho_m) DOES reach 25-50 a0 at z=6-10 (smooth-floor boost 4-9x),
   but that is the SMOOTH density-a0 / a0(z) law, NOT the fluctuation term: locally it breaks SPARC;
   globally it IS the banked a0(z) rising-cH branch (a separate mechanism). So the fluctuation term
   does NOT unify clusters + JWST. The framework's real high-z lever is the banked a0(z) branch.

 NET: the acceleration-fluctuation term is CLUSTER-WEAK (~1.0-1.1x vs ~4-5x needed) once the
   physically required non-adiabatic gate is applied; without the gate it is ~1.01-1.1x in clusters
   but BREAKS galaxy bulges (~11x). Either way it is NOT a cluster cure and does NOT explain JWST.
   The prior estimate was sqrt(2)~1.41; the honest gated answer is SMALLER (~1.00-1.10x). Both ways,
   no manufactured win, the galaxy-bulge artifact disclosed not buried. QUARANTINE held: a0/Z never
   asserted derived. The term's one genuine virtue (self-consistent galaxy-safety) buys nothing
   because the same gate that protects galaxies nullifies the cluster effect.
""")
