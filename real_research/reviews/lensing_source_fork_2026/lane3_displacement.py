#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE 3 -- VACUUM DISPLACEMENT (Verlinde-class elastic back-reaction of the dark-energy medium)
==============================================================================================
Framework premises (reason from THESE):
  * de Sitter-Unruh modified inertia; a0 = cH_Lambda/Z = c^2 sqrt(Lambda/32pi) = 9.36e-11 (canonical),
    Z = sqrt(32pi/3) = 5.787; alt footing a0 = cH0/Z = 1.13e-10.
  * REQUIRED TARGET for ANY source-side lensing mechanism (banked GW170817 constraint: the
    enhancement must live in the ONE shared metric as a SOURCE):
        M_eff(r) = M_bar (nu(y) - 1),  nu(y) = sqrt(1 + 1/y),  y = g_bar/a0
        deep-MOND: M_eff -> sqrt(a0 M_bar / G) * r   (per-galaxy ~ sqrt(M_bar))
  * CANDIDATE: Verlinde emergent-gravity apparent dark mass (arXiv:1611.02269 eq. 7.40-type):
        int_0^r G M_D^2(r')/r'^2 dr' = M_b(r) * a0_V * r / 6
     => point/const M_b:  M_D(r) = sqrt(a0_V M_b / (6G)) * r ,  g_D = sqrt(a0_V g_bar / 6).
    Verlinde's own scale a0_V = cH0 (he works in pure dS where H0 = H_Lambda).
    Framework medium = the dS bath with rho_Lambda -> natural scale a0_V = cH_Lambda.

Honesty: candidate failure verified as hard as success; both footings; orders quantified.
"""
import numpy as np

# ----------------------------- constants (SI) -----------------------------
c    = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
AU   = 1.495978707e11

Z        = np.sqrt(32*np.pi/3.0)            # 5.7873
A0_CANON = 9.36e-11                          # cH_Lambda / Z  (pure-Lambda footing)
A0_ALT   = 1.13e-10                          # cH0 / Z        (rho_total/cH0 footing)
cH_Lam   = Z * A0_CANON                      # 5.418e-10  (the framework's OWN medium scale)
H0       = 67.4 * 1e3 / (3.0857e22)          # Planck H0 [1/s]
cH0      = c * H0                            # 6.55e-10   (Verlinde's own scale)

print("="*100)
print(" LANE 3 -- VACUUM DISPLACEMENT (Verlinde-class) as the SOURCE of the lensing/dynamics enhancement")
print("="*100)
print(f"  Z = sqrt(32pi/3)          = {Z:.4f}   <-- note how close to Verlinde's forced 6")
print(f"  a0 canonical              = {A0_CANON:.3e} m/s^2   (cH_Lambda = Z a0 = {cH_Lam:.3e})")
print(f"  a0 alt                    = {A0_ALT:.3e} m/s^2   (cH0 = {cH0:.3e})")
print(f"  Verlinde effective MOND scale = a0_V/6:")
print(f"     medium=Lambda: cH_Lambda/6 = {cH_Lam/6:.3e}  vs canonical a0 {A0_CANON:.3e}  -> ratio {cH_Lam/6/A0_CANON:+.4f}")
print(f"     medium=H0:     cH0/6       = {cH0/6:.3e}  vs alt      a0 {A0_ALT:.3e}  -> ratio {cH0/6/A0_ALT:+.4f}")
print()

def nu(y):            return np.sqrt(1.0 + 1.0/y)
def M_eff(r, Mb, a0):                       # REQUIRED effective source mass
    gbar = G*Mb/r**2
    return Mb*(nu(gbar/a0) - 1.0)
def M_D(r, Mb, a0V):                        # CANDIDATE Verlinde apparent dark mass
    return np.sqrt(a0V*Mb/(6.0*G)) * r
def rho_from_M(r, Mfun, eps=1e-4):          # rho = dM/dr / (4 pi r^2)
    dM = (Mfun(r*(1+eps)) - Mfun(r*(1-eps))) / (2*r*eps)
    return dM/(4*np.pi*r**2)

# ============================================================================================
# (1) PROFILE CONFRONTATION -- M_bar = 1e11 Msun, r = 5..100 kpc, BOTH footings
# ============================================================================================
print("="*100)
print(" (1) CANDIDATE vs REQUIRED  --  M_bar = 1e11 Msun")
print("="*100)
Mb = 1e11*Msun
radii = np.array([5, 10, 20, 50, 100])*kpc

for tag, a0, a0V, lab in [
    ("CANONICAL", A0_CANON, cH_Lam, "a0=9.36e-11, medium scale a0_V=cH_Lambda"),
    ("ALT",       A0_ALT,   cH0,    "a0=1.13e-10, medium scale a0_V=cH0"),
    ("CROSS",     A0_CANON, cH0,    "a0=9.36e-11 vs Verlinde-original a0_V=cH0"),
]:
    print(f"\n  [{tag}]  {lab}")
    print(f"  {'r[kpc]':>7} {'g_bar':>10} {'y':>9} {'M_eff[Msun]':>12} {'M_D[Msun]':>12} "
          f"{'M_D/M_eff':>10} {'rho_eff':>11} {'rho_D':>11} {'rho ratio':>10}")
    for r in radii:
        gbar = G*Mb/r**2; y = gbar/a0
        Me  = M_eff(r, Mb, a0);  Md = M_D(r, Mb, a0V)
        rhoe = rho_from_M(r, lambda x: M_eff(x, Mb, a0))
        rhod = rho_from_M(r, lambda x: M_D(x, Mb, a0V))
        print(f"  {r/kpc:>7.0f} {gbar:>10.3e} {y:>9.3f} {Me/Msun:>12.3e} {Md/Msun:>12.3e} "
              f"{Md/Me:>10.3f} {rhoe:>11.3e} {rhod:>11.3e} {rhod/rhoe:>10.3f}")

print("""
  SHAPE: deep regime (y<<1) BOTH give M ~ r * sqrt(M_bar) (isothermal-like, per-galaxy sqrt(M_bar)
  -- the scaling that killed the fixed-amount condensate is REPRODUCED by displacement).""")
coef = np.sqrt(Z/6.0)
print(f"  DEEP-LIMIT COEFFICIENT (matched footing, a0_V = Z*a0):  M_D / M_eff -> sqrt(Z/6) = {coef:.4f}")
print(f"    i.e. the displacement amplitude is {100*(1-coef):.1f}% LOW; equivalent a0 mismatch:")
print(f"    a0_eff(Verlinde) = cH/6 vs cH/Z  ->  a0 shift = Z/6 - 1 = {100*(Z/6-1):.2f}%  (Z={Z:.4f} vs 6)")
print(f"    Absorbing the 6 exactly: Z_V = 6  =>  a0 -> cH_Lambda/6 = {cH_Lam/6:.3e} (canonical -3.6%),")
print(f"    and the closed form c^2 sqrt(Lambda/32pi) becomes c^2 sqrt(Lambda/108): 32pi={32*np.pi:.1f} vs 108/... ")
print(f"    [c^2 sqrt(L/3)/6 = c^2 sqrt(L/108); 108 vs 32pi=100.5: 7.4% inside the sqrt].")
print(f"    Banked SPARC verdict: RAR is NON-diagnostic at the 20% level in a0 (M/L degenerate) =>")
print(f"    a 3.6% a0 shift is INVISIBLE to SPARC. The 6-vs-Z fork is UNTESTABLE there; keeping Z=5.787")
print(f"    costs only a 1.8% deep-amplitude mismatch. Verdict: the sqrt-6 is ABSORBABLE.")
print("""
  HIGH-g DIVERGENCE (the wall Lelli+2017 hit): the raw candidate g_D = sqrt(a0_V g_bar/6) GROWS with
  g_bar and never screens; the required (nu-1) g_bar -> a0/2 = const. Overshoot factor:""")
for yv in [6, 60, 6e2, 6e4, 7e5]:
    gbar = yv*A0_CANON
    over = np.sqrt(cH_Lam*gbar/6.0) / ((nu(yv)-1.0)*gbar)
    print(f"    y = {yv:>9.0f}:  g_D / g_required = {over:>10.1f}x")
print("  => the candidate matches ONLY in the deep regime; at galaxy centers (y~6) it already")
print("     overshoots 5x, and in the solar system (y~7e5) by ~1600x. A SCREEN IS MANDATORY,")
print("     and Verlinde does NOT derive one -- the framework's nu must be POSITED as the medium's")
print("     elastic-to-rigid crossover (re-purposing the Deser-Levin interpolation as medium response).")

# ============================================================================================
# (2) SOLAR SYSTEM -- unscreened apparent mass, screening requirement, INPOP confrontation
# ============================================================================================
print("\n" + "="*100)
print(" (2) SOLAR SYSTEM  (M_b = 1 Msun)")
print("="*100)
r_sat, r_mars = 9.5826*AU, 1.5237*AU
# Pitjev & Pitjeva 2013 (Astron.Lett. 39, 141) ephemeris bounds on anomalous mass (approx, from lit):
M_lim_sat, M_lim_mars = 1.7e-10*Msun, 1.0e-11*Msun

print(f"  {'':<34}{'Saturn (9.58 AU)':>20}{'Mars (1.52 AU)':>20}")
for tag, a0, a0V in [("CANONICAL", A0_CANON, cH_Lam), ("ALT", A0_ALT, cH0)]:
    Md_s, Md_m = M_D(r_sat, Msun, a0V), M_D(r_mars, Msun, a0V)
    Me_s, Me_m = M_eff(r_sat, Msun, a0), M_eff(r_mars, Msun, a0)
    print(f"\n  [{tag}]")
    print(f"  {'UNSCREENED Verlinde M_D [Msun]':<34}{Md_s/Msun:>20.3e}{Md_m/Msun:>20.3e}")
    print(f"  {'  /INPOP-class bound':<34}{Md_s/M_lim_sat:>19.1e}x{Md_m/M_lim_mars:>19.1e}x")
    print(f"  {'  ORDERS OVER':<34}{np.log10(Md_s/M_lim_sat):>20.1f}{np.log10(Md_m/M_lim_mars):>20.1f}")
    print(f"  {'nu-SCREENED  M_sun(nu-1) [Msun]':<34}{Me_s/Msun:>20.3e}{Me_m/Msun:>20.3e}")
    print(f"  {'  /INPOP-class bound':<34}{Me_s/M_lim_sat:>19.1e}x{Me_m/M_lim_mars:>19.1e}x")
    print(f"  {'  ORDERS OVER':<34}{np.log10(Me_s/M_lim_sat):>20.1f}{np.log10(Me_m/M_lim_mars):>20.1f}")

gbar_sat = G*Msun/r_sat**2
print(f"""
  READING (honest, both directions):
  * UNSCREENED displacement fails Saturn-orbit mass bounds by ~{np.log10(M_D(r_sat,Msun,cH_Lam)/M_lim_sat):.0f} ORDERS. Dead on arrival
    without a screen. This is not a subtlety -- it is the sqrt(g_bar) growth of g_D.
  * Even nu-SCREENED, the NAIVE SPHERICAL monopole M_sun(nu-1) ~ a0 r^2/2G exceeds the Saturn bound
    by ~3.6 ORDERS (the 1/y tail of nu gives delta-g -> a0/2 = {A0_CANON/2:.2e} m/s^2, non-Keplerian, not
    absorbable into GM_sun). The naive spherical screen is NOT enough.
  * What actually saves ANY nu-of-this-family source theory in the ephemerides is the EXTERNAL-FIELD
    dominance: g_ext(galactic) ~ 2.3e-10 > a0 puts the local medium in the rigid regime; the residual is
    the Q2 QUADRUPOLE. Verlinde's medium has this feature qualitatively (the galaxy pre-strains the
    elastic medium at 8 kpc), but NO derived EFE exists -- the AQUAL-like completion supplies it.
  * BANKED NUMBERS (real_research/reviews/cassini_mi_q2_saturn_2026.py, committed):
      Cassini 2026:            Q2 = (1.6 +/- 1.8)e-27 s^-2   (2-sigma ceiling 5.2e-27)
      MG/AQUAL phantom-source: Q2 = +1.2..2.0e-26 s^-2  =  +6..10 SIGMA  (2.3-3.9x the ceiling)
      MI realization:          BELOW the ceiling (both footings)  <- this evasion is what Lane 3 SPENDS.
    A source-side displacement medium IS the phantom-source class: the Q2 WALL RETURNS at +6..10 sigma
    (equivalently the 3-15 sigma RAR-vs-Q2 range across MW mass models). Caveat: the exact displacement-
    medium Q2 coefficient is UNCOMPUTED (no Verlinde action); 'same class' is the honest default, not a
    theorem.""")

# ============================================================================================
# (3) THE COST LEDGER + literature walls
# ============================================================================================
print("="*100)
print(" (3) COSTS if Lane 3 is adopted")
print("="*100)
print("""  NEW POSITS REQUIRED:
   P1. An elastic dark-energy medium with Verlinde's entropy-displacement law (his derivation is
       heuristic: volume-law entanglement entropy + linear-elastic response + the 1/6; none of it is
       derived from the framework's dS-Unruh premises -- it must be IMPORTED).
   P2. A HIGH-g SCREEN: the medium must go rigid for g_bar >> a0 with EXACTLY the framework nu
       (posit; Verlinde gives none; the Deser-Levin interpolation would have to be re-derived as the
       medium's stress-strain law -- currently unwritten).
   P3. An EFE for the medium (galaxy pre-strain) to evade ephemerides -- brings back Q2 (above).
   P4. The coefficient: keep Z=5.787 and eat a 1.8% deep amplitude (SPARC-invisible), or set Z_V=6 and
       lose the c^2 sqrt(Lambda/32pi) closed form (and the banked Z in the SME s^TX numbers).

  WHAT IT DOES TO THE MI PREMISE (the banked double-count audit, mi_lensing_doublecount_audit.py):
   * The metric now carries the enhancement -> the MI matter response MUST trivialize (K -> 1),
     else rotation curves over-predict by the enhancement factor. The MODIFIED-INERTIA mechanism is
     REPLACED by elastic-medium modified gravity with a source.
   * LOST: the MI Cassini Q2 evasion (banked, below ceiling) -> replaced by the MG +6..10 sigma wall.
   * LOST: the MG-impossible cluster discriminator (non-adiabatic relational sigma-spread, MI 6-13%
     vs MG exactly 0) -- a source mechanism predicts 0; the framework's one distinctive observable dies.
   * MOOT: the v1-v12 covariant MI action program as dynamics (constraint closure, Herglotz K, loop
     stability); at best the K-machinery is repurposed as the medium response function (speculative).
   * NEEDS RECOMPUTE: the SME s^TX front (the induced s_mu-nu was MI-specific; a medium still defines
     a preferred frame, but the numbers do not carry over).
   SURVIVES:
   * a0 = c^2 sqrt(Lambda/32pi) as the DISPLACEMENT SCALE of the dark-energy medium (the reframing).
   * a0(z) ~ sqrt(rho_DE(z)) falsifiable content (medium = dark energy -> the scale tracks it).
   * GW170817 safety BY CONSTRUCTION (one shared metric, source-side) -- though 'safe by construction'
     here partly means 'safe by not having an action to check'.

  LITERATURE WALLS (from memory -- flagged, not re-fetched):
   * Lelli, McGaugh & Schombert 2017 (ApJ 836,152): EG vs SPARC RAR -- degenerate with MOND at low g
     (a0_eff = cH0/6), but the unscreened sqrt(g_bar) tail deviates at high g where data pin
     g_obs = g_bar; EG fits statistically worse than MOND. (Consistent with our 5x overshoot at y~6.)
     Caveat cutting the other way: they applied the point-mass formula to disks, outside its derivation.
   * Brouwer+ 2017/2021 (KiDS weak lensing, isolated galaxies): EG consistent at 0.3-3 Mpc -- the
     deep-regime shape (the part that matches our target) is the part lensing tests. Supportive.
   * Cluster cores (Ettori+2017/X-COP-type hydrostatic tests): EG improves outskirts but misses in
     cores, MOND-like -- the shared cluster wall persists (banked eta(R500)~1.0-1.3 unchanged).
   * No covariant action / no time-dependence: cosmology, structure formation, GW emission undefined.""")

# ============================================================================================
# VERDICT
# ============================================================================================
print("="*100)
print(" VERDICT")
print("="*100)
print(f"""  SHAPE-MATCH (deep regime), coefficient sqrt(Z/6) = {coef:.3f} on the framework's own footing
  (a0_V = cH_Lambda): the displacement profile M_D = sqrt(a0_V M_b/6G) r reproduces the REQUIRED
  isothermal M_eff -> sqrt(a0 M_b/G) r INCLUDING the per-galaxy sqrt(M_bar) scaling, 1.8% low in
  amplitude (a0_eff 3.6% low) -- SPARC-invisible; Z=5.787 vs Verlinde's 6 is a genuine near-coincidence.
  NOT a match outside the deep regime: 5x over at y~6, unscreened at Saturn {np.log10(M_D(r_sat,Msun,cH_Lam)/M_lim_sat):.0f} orders over
  ephemeris mass bounds (nu-screened still 3.6 orders over as a bare monopole; EFE/Q2 is the real
  regulator); nu-screen must be posited; and the source-side realization re-inherits the
  Cassini Q2 MG wall at +6..10 sigma -- the single costliest item, since the MI framing's banked
  evasion of exactly that wall is what gets spent. Lane 3 buys GW170817-safe lensing at the price of
  gutting the framework's mechanism (MI -> MG-with-source) and its one MG-impossible discriminator.""")
print("EXIT 0")
