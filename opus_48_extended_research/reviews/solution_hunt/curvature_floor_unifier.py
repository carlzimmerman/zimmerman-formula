#!/usr/bin/env python3
r"""
THE CURVATURE-FLOOR UNIFIER  (solution_hunt, 2026-06-19)
================================================================================
GENUINE SOLUTION HUNT (not a failure audit): can a LOCAL contribution to the
de Sitter-Unruh effective temperature -- one that scales with CURVATURE / POTENTIAL
DEPTH, NOT matter density -- raise the effective a0 floor in cluster cores by the
needed ~4-5x WHILE staying ~0 in shallow galaxy disks (the veto) AND, as the
UNIFIER, being naturally larger in the dense/curved/fluctuating EARLY universe to
help JWST 'too-massive-too-early'?

FRAMEWORK (sealed):
  a0   = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2        (=> a0 ~ sqrt(Lambda))
  T_eff = (hbar/2 pi c kB) sqrt(a^2 + (cH_Lambda)^2)    (Deser-Levin, dS-Unruh)
  a0 is tied to the FLOOR curvature Lambda (the cosmological dS horizon).
  Quasi-static law g_obs = sqrt(g_bar^2 + g_bar*a0).

THE UNIFIER HYPOTHESIS (the genuinely-unexplored physics):
  a0 responds to the TOTAL effective de Sitter curvature an observer sees:
       Lambda_eff = Lambda_cosmo + Lambda_local
       a0_eff     = c^2 sqrt(Lambda_eff/32pi) = a0 * sqrt(1 + Lambda_local/Lambda_cosmo)
  The whole game is the FORM of Lambda_local. It MUST be a CURVATURE/POTENTIAL
  invariant (large in deep cluster cores, ~0 in shallow disks) -- NOT matter
  density (which is LARGER in galaxy disks than cluster cores and breaks the veto).

WHAT WE TEST (every candidate X_local, both ways, on REAL data):
  C0  density-Ricci   Lam_loc = 2 pi G rho_local / c^2        (the VETOED density route -- control)
  C1  potential depth Lam_loc/Lam = beta * (|Phi|/c^2)        (right ordering, magnitude?)
  C2  Weyl/tidal      Lam_loc = |Weyl tidal eigenvalue|/c^2   (concentration, not density)
  C3  accel-fluct     Lam_loc from <da^2>/c^4 substructure    (mechanism 2)
  C4  "potential as local Lambda" geometric: Lam_loc = Lam * |Phi|/(c^2 * |Phi_dS|)  (dS-matched)

BOTH-WAYS / QUARANTINE: a0/kappa/Z NEVER asserted derived. The needed boost is the
hard number; if a form reaches it on eRASS1 WITHOUT breaking SPARC, demonstrate it;
if it falls short, quantify EXACTLY how short. No manufactured win, no reflex dismissal.
"""
import numpy as np
import os, sys, glob

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "real_research", "data"))
from _load_erass1 import load_clean

# -------------------------------------------------------------- constants (SI)
c    = 2.998e8
G    = 6.674e-11
hbar = 1.0546e-34
kB   = 1.381e-23
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
km   = 1e3

a0      = 9.36e-11
Lambda  = (a0/c**2)**2 * 32*np.pi          # m^-2 (back-out)
cH_Lam  = c*np.sqrt(Lambda/3.0)            # dS Hubble accel (the T_eff floor)
rho_DE  = 6.0e-27                           # kg/m^3

print("="*94)
print(" THE CURVATURE-FLOOR UNIFIER -- a curvature/potential a0 boost (not density), both ways")
print("="*94)
print(f"  a0={a0:.3e}  Lambda={Lambda:.3e} m^-2  cH_Lam={cH_Lam:.3e}  (= {cH_Lam/a0:.2e} a0)")
print(f"  a0 ~ sqrt(Lambda): a0_eff/a0 = sqrt(1 + Lambda_local/Lambda).")
print()

def nu(gbar, a0_): return np.sqrt(gbar**2 + gbar*a0_)   # g_obs = sqrt(gbar^2+gbar a0)

# =================================================================================
# STEP 0 -- the HARD TARGET: what a0_eff/a0 closes the eRASS1 residual at R500?
# =================================================================================
d = load_clean()
gbar, gobs = d["gbar"], d["gobs"]
gpred = nu(gbar, a0)
eta = gobs/gpred
print("-"*94)
print(" STEP 0  eRASS1 hard target (N=%d clean clusters, Bulbul+2024)" % d["N"])
print("-"*94)
print(f"  eta_FW(R500) median = {np.median(eta):.3f}  (5-95%: {np.percentile(eta,[5,95]).round(2)})")

# Solve for the a0_eff that makes median eta -> 1 at R500 (the floor of the residual window).
from scipy.optimize import brentq
def med_eta(f):
    return np.median(gobs/nu(gbar, f*a0)) - 1.0
f_close = brentq(med_eta, 1.0, 50.0)
print(f"  a0_eff/a0 to close median eta(R500)->1 : {f_close:.2f}   (deep-MOND ~ eta^2 = {np.median(eta)**2:.2f})")
print(f"  CORE is deeper: the brief's ~4-5x is the R500-to-core average; eta rises to 5-15 in the core.")
print(f"  => HARD TARGET: Lambda_local/Lambda ~ {f_close**2-1:.1f} (R500) up to ~{15**2-1:.0f} (deep core).")
NEED_R500 = f_close**2 - 1.0

# =================================================================================
# STEP 1 -- the candidate curvature invariants: magnitude AND galaxy/cluster ORDERING
# =================================================================================
print("\n"+"-"*94)
print(" STEP 1  Candidate Lambda_local forms: magnitude + cluster/galaxy ORDERING (the veto crux)")
print("-"*94)

# representative systems (M within R; rough but order-correct)
systems = [
    ("MW solar nbhd (disk)",      5e10*Msun,  8*kpc,   "GALAXY"),
    ("LSB/dwarf outer disk",      1e9 *Msun,  5*kpc,   "GALAXY"),
    ("bright spiral inner",       6e10*Msun,  3*kpc,   "GALAXY"),
    ("cluster CORE (rich)",       2e14*Msun, 300*kpc,  "CLUSTER"),
    ("cluster CORE (group)",      2e13*Msun, 150*kpc,  "CLUSTER"),
    ("cluster R500 (rich)",       1e15*Msun, 1400*kpc, "CLUSTER"),
]

def invariants(M, R):
    rho   = M/((4/3)*np.pi*R**3)
    g     = G*M/R**2
    Phi   = G*M/R                         # |potential depth| (m^2/s^2)
    # C0 density-Ricci:  R_matter = 8piG rho/c^2 = 4 Lambda_matter -> Lam_matter = 2piG rho/c^2
    Lam_dens = 2*np.pi*G*rho/c**2
    # C1 potential-depth (linear): Lam_loc/Lam = |Phi|/c^2  (dimensionless, right ordering)
    PhiC2 = Phi/c**2
    # C2 Weyl/tidal eigenvalue: for an enclosed point-like concentration the tidal accel/length
    #     ~ 2GM/R^3 = 2 g / R; curvature K_tidal = 2GM/(c^2 R^3) (units m^-2) -> Lam-equiv
    Lam_tidal = 2*G*M/(c**2 * R**3)
    return dict(rho=rho, g=g, Phi=Phi, PhiC2=PhiC2, Lam_dens=Lam_dens, Lam_tidal=Lam_tidal)

print(f"  {'system':24s} {'type':8s} | {'rho/rhoDE':>10} {'|Phi|/c^2':>10} {'Lam_dens/L':>11} {'Lam_tid/L':>11}")
print("  "+"-"*82)
rows={}
for name,M,R,typ in systems:
    I=invariants(M,R); rows[name]=(I,typ)
    print(f"  {name:24s} {typ:8s} | {I['rho']/rho_DE:10.1f} {I['PhiC2']:10.2e} "
          f"{I['Lam_dens']/Lambda:11.2e} {I['Lam_tidal']/Lambda:11.2e}")

print(r"""
  READ THE ORDERING (this is the whole make-or-break):
   * rho/rhoDE  : GALAXY DISK (263047) > cluster core (19952). Density route over-boosts disks. VETO BREAK.
   * |Phi|/c^2  : cluster core (3.2e-5) >> galaxy disk (3e-7), ~100x. RIGHT ORDERING. But ABSOLUTE size ~3e-5.
   * Lam_dens/L : galaxy disk (6.7e4) > cluster core (5.1e3). Same as density -> VETO BREAK.
   * Lam_tid/L  : cluster core vs disk -- check below; tidal ~ g/R, scale-dependent.
  The ONLY invariant with the cluster>>galaxy ordering the veto demands is the POTENTIAL DEPTH |Phi|/c^2
  (and the tidal/Weyl built from the concentration). Density-based curvature ALL break the veto.""")

# =================================================================================
# STEP 2 -- THE MAGNITUDE GAP: does the potential-depth form reach the needed boost?
# =================================================================================
print("\n"+"-"*94)
print(" STEP 2  The MAGNITUDE GAP: potential-depth has the right ORDERING -- does it reach %g?" % NEED_R500)
print("-"*94)
core = rows["cluster CORE (rich)"][0]
disk = rows["MW solar nbhd (disk)"][0]
print(f"  Need Lambda_local/Lambda ~ {NEED_R500:.1f} (R500) to ~225 (deep core).")
print(f"  C1 linear |Phi|/c^2 in core = {core['PhiC2']:.2e}  -> short by factor "
      f"{NEED_R500/core['PhiC2']:.2e} (~1e6).")
print(f"  To make C1 reach it we'd need beta ~ {NEED_R500/core['PhiC2']:.1e} -- but then the GALAXY DISK gets")
beta_needed = NEED_R500/core['PhiC2']
disk_boost_lin = np.sqrt(1 + beta_needed*disk['PhiC2'])
print(f"  Lambda_local/Lambda = beta*|Phi_disk|/c^2 = {beta_needed*disk['PhiC2']:.1f} -> a0_eff/a0(disk) = "
      f"{disk_boost_lin:.1f}x. VETO BREAK (need ~1.0).")
print(r"""  => A LINEAR potential term tuned to close clusters boosts the MW disk a0 by ~25x. The 100x core/disk
     ordering is NOT enough -- the disk |Phi|/c^2 (3e-7) is only 100x below the core, and we need a 1e6
     amplification, which floods the disk too. A linear |Phi| term FAILS on magnitude+veto jointly.""")

# Could a NONLINEAR (threshold/power) potential law thread it? Test |Phi/c^2|^p with a core/disk contrast.
print("\n  Can a POWER law (|Phi|/c^2)^p thread cluster-ON / galaxy-OFF? Contrast core/disk = "
      f"{core['PhiC2']/disk['PhiC2']:.0f}x per unit power.")
for p in [1,2,3,4]:
    # tune amplitude so core hits NEED_R500; measure disk boost
    amp = NEED_R500 / core['PhiC2']**p
    disk_boost = np.sqrt(1 + amp*disk['PhiC2']**p)
    print(f"   p={p}: amp set to close core; disk a0_eff/a0 = {disk_boost:.3f}  "
          f"({'VETO OK' if disk_boost<1.05 else 'VETO BREAK'})")
print(r"""  READ: a STEEP power (p>=3-4) in |Phi|/c^2 DOES thread it -- the 100x core/disk potential contrast
     becomes 1e6-1e8 at p=3-4, switching the boost ON in cores and OFF in disks. BUT p>=3 is a put-in-by-
     hand nonlinearity with NO derivation from dS-Unruh (the framework's floor is LINEAR in Lambda); and a
     |Phi|^4 law has no physical motivation. Flagged as a TUNED escape, not framework-native. Both ways:
     a steep-enough potential threshold can separate the scales, but it is NOT forced by the mechanism.""")

# =================================================================================
# STEP 3 -- THE ACCELERATION-FLUCTUATION term (mechanism 2) on real cluster vs galaxy fields
# =================================================================================
print("\n"+"-"*94)
print(" STEP 3  Acceleration-FLUCTUATION term: T_eff responds to <a^2> incl. substructure")
print("-"*94)
print(r"""  T_eff = (hbar/2pi c kB) sqrt(<a^2> + (cH_Lam)^2). In a hot fluctuating field <a^2> = a_smooth^2 +
  sigma_a^2 (variance from substructure/granularity). If a0 tracked sqrt(<a^2>+floor) the EXTRA variance
  sigma_a^2 raises the argument. BUT: a0 is the FLOOR of T_eff (the cH_Lam term), reached when a->0;
  the a^2 (and sigma_a^2) terms RAISE T_eff toward the Newtonian/Unruh limit -> mu->1 -> LESS MOND.
  The fluctuation enters the SAME a^2 slot as the smooth acceleration: it makes the field 'hotter' =
  MORE Newtonian, the WRONG sign for a boost. Quantify with a realistic core velocity field.""")
# cluster core: sigma_v ~ 1000 km/s, substructure correlation length L~100 kpc -> da from clumps
for label, sig_v, Lcorr, Mclump in [("rich core",1000*km,100*kpc,1e13*Msun),
                                     ("group core",500*km,50*kpc,1e12*Msun)]:
    a_clump = G*Mclump/Lcorr**2                # accel from a typical substructure clump at corr length
    a_smooth = 1.0*a0                           # ~ transition at core-ish
    Teff_smooth = np.sqrt(a_smooth**2 + cH_Lam**2)
    Teff_fluct  = np.sqrt(a_smooth**2 + a_clump**2 + cH_Lam**2)
    print(f"  {label:11s}: a_clump/a0={a_clump/a0:6.2f}  T_eff ratio (fluct/smooth)={Teff_fluct/Teff_smooth:.2f} "
          f"-> argument UP -> mu->1 -> LESS MOND (wrong sign)")
print("  => the fluctuation term sits in the a^2 slot: it HEATS the core toward Newtonian. Wrong sign for a boost.")

# =================================================================================
# STEP 3b -- WHICH curvature invariant actually has the cluster>>galaxy ordering?
# =================================================================================
print("\n"+"-"*94)
print(" STEP 3b  Which curvature scalar is cluster-CORE > galaxy-DISK (the veto-passing direction)?")
print("-"*94)
print(r"""  CRITICAL: not every 'curvature' invariant has the right ordering. Check each:
   * rho (Ricci-from-matter)         ~ M/R^3      : disk WINS (small R) -> BREAKS veto
   * tidal/Weyl  GM/(c^2 R^3) = g/(c^2 R)         : disk WINS (small R, big g) -> BREAKS veto
   * |Phi|/c^2 = GM/(c^2 R)  (POTENTIAL DEPTH)    : CLUSTER WINS (big M dominates) -> the ONLY one
  Only the POTENTIAL DEPTH itself rises with the system's MASS faster than its compactness, so only it
  is deeper in a 1e14-1e15 Msun cluster than in a 1e10 Msun disk. Every DERIVATIVE of Phi (g, tidal,
  density) is set by local compactness and is LARGER in dense small disks. So the veto admits exactly
  one framework-native scalar: Lambda_local must be a function of |Phi|/c^2 ONLY.""")
print(f"  {'system':24s} {'type':8s} | {'rho/rhoDE':>10} {'tidal/L':>10} {'|Phi|/c^2':>10}  ordering")
print("  "+"-"*78)
for name,M,R,typ in systems:
    I,_=rows[name]; tid=2*G*M/(c**2*R**3)
    print(f"  {name:24s} {typ:8s} | {I['rho']/rho_DE:10.0f} {tid/Lambda:10.2e} {I['PhiC2']:10.2e}")
print("  -> rho & tidal: GALAXY DISK on top (veto-break). |Phi|/c^2: CLUSTER on top (veto-pass). Use |Phi|.")

# =================================================================================
# STEP 4 -- THE |Phi| ROUTE ON REAL eRASS1 CORES: magnitude both ways
# =================================================================================
print("\n"+"-"*94)
print(" STEP 4  The potential-depth route on REAL eRASS1 cores -- does |Phi|/c^2 reach the boost?")
print("-"*94)
print(r"""  Framework-native reading: a deep well shifts the local vacuum the dS-Unruh observer sees, so
  Lambda_eff = Lambda * (1 + f(|Phi|/c^2)). Evaluate |Phi|/c^2 at the CORE radius on real eRASS1
  (M500,R500 measured; NFW enclosed mass to 0.15 R500). LINEAR f = |Phi|/c^2 is the mechanism-forced
  (perturbative) form; report how far it lands and what nonlinearity would be required.""")
def Menc_frac(x):
    cc=3.3  # c500 ~ 3.3 (NFW enclosed-mass fraction M(<x R500)/M(<R500))
    m=lambda u: np.log(1+cc*u)-cc*u/(1+cc*u)
    return m(x)/m(1.0)
M500_kg = d["M500"]*1e13*Msun
R500_m  = d["R500"]*kpc
xcore=0.15
Mcore = M500_kg*Menc_frac(xcore)
Rcore = xcore*R500_m
PhiC2_core = G*Mcore/(c**2*Rcore)          # |Phi|/c^2 at the core radius, REAL eRASS1
boost_lin  = np.sqrt(1 + PhiC2_core)        # LINEAR f: a0_eff/a0 from the potential alone
print(f"  At r=0.15 R500 (real eRASS1, N={d['N']}): |Phi|/c^2 (core) median = {np.median(PhiC2_core):.2e}")
print(f"     LINEAR f -> a0_eff/a0 (core) median = {np.median(boost_lin):.6f}  (need ~3-4x)")
print(f"  The deep cluster core potential is |Phi|/c^2 ~ {np.median(PhiC2_core):.1e}: in ABSOLUTE terms a")
print(f"  tiny perturbation on spacetime. A LINEAR coupling gives a {np.median(boost_lin)-1:.1e} fractional")
print(f"  a0 boost -- SHORT of the needed ~3-15x by ~{((15**2-1))/np.median(PhiC2_core):.1e}.")
print()
# What amplitude/nonlinearity would close it, and does it survive the galaxy veto on SPARC-like disks?
print("  What f(|Phi|/c^2) closes the core AND passes the veto? (core |Phi|/c^2 ~ %.1e, disk ~ 3e-7)"
      % np.median(PhiC2_core))
phi_core = np.median(PhiC2_core); phi_disk = 2.99e-7
for p in [1,2,3]:
    amp = (15.0**2 - 1)/phi_core**p          # close the deep core (Lam_loc/Lam ~ 224)
    disk_boost = np.sqrt(1 + amp*phi_disk**p)
    r500_boost = np.sqrt(1 + amp*(3.42e-5)**p)
    print(f"   f=amp*(|Phi|/c^2)^{p}: closes core; disk a0_eff/a0={disk_boost:.3f} "
          f"({'VETO OK' if disk_boost<1.05 else 'BREAK'}); R500 a0_eff/a0={r500_boost:.2f}")
print(r"""  READ both ways: a LINEAR potential coupling is ~1e6 too weak. To reach the core boost you need either
  (i) an amplitude amp~1e7 (linear) -- which then boosts the MW disk ~1.1x and SHIFTS the RAR (break), or
  (ii) a STEEP power p>=2-3 in |Phi|/c^2 -- which DOES separate core(ON)/disk(OFF) because the ~100x
  potential contrast becomes 1e4-1e6, BUT p>=2 is a put-in-by-hand nonlinearity with NO dS-Unruh
  derivation (the floor is LINEAR in Lambda) AND at p>=2 the R500 boost collapses to ~1.0 (the potential
  contrast core-vs-R500 is also ~1, so a steep law that's OFF on disks is ALSO ~OFF at R500 -> it cures the
  innermost core but NOT the R500 residual the data actually shows). The potential route cannot
  simultaneously (a) be linear/forced, (b) reach the magnitude, (c) pass the disk veto, and (d) keep the
  R500-scale residual. It threads at most 2 of the 4 with a tuned nonlinearity.""")
