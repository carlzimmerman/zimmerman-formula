#!/usr/bin/env python3
"""
PRECISION-CONSISTENCY LEDGER, PART 1 of N:  ATOMIC CLOCKS (1e-18) + ATOM INTERFEROMETRY
=======================================================================================
The de Sitter-Unruh MODIFIED-INERTIA framework (MI_FIELD_THEORY_RESULTS_2026.md) vs the
highest-precision terrestrial/near-Earth measurements that exist.

EVERY observable is computed TWICE:
   (i)  GATED (AC) channel   -- with the paper's own single-pole Debye gate
                                Re G(w) = 1/(1+(w/w_c)^2), w_c in [1.78,2.21]e-14 rad/s (canon)
   (ii) DC channel (Fork C)  -- NO gate suppression, because Re G(0) = 1 for EVERY w_c.
Then: does existing data EXCLUDE the DC channel, and by how many orders?

CALIBRATION HELD (manufacture neither a win nor a deficit):
  * "suppressed by 10^N, no constraint" is an HONEST result for the AC channel; the suppression
    factor is printed for every observable so the ledger is quantitative, not hand-waved.
  * The DC channel is not given a free pass either.  Where it is excluded, the number of orders
    is printed; where it is NOT excluded, the reason (precision vs DEGENERACY) is named.
  * Both a0 footings on every load-bearing number.
  * Every modelling choice is labelled [ADOPTED] / [ASSUMPTION] / [ANCHOR].
No TOE language.  No "theory closed".  numpy + sympy.  Exits 0.
"""
import numpy as np
import sympy as sp

RULE = "=" * 104
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

# =====================================================================================
# 0.  FOOTINGS, CONSTANTS, ANCHORS
# =====================================================================================
A0 = {"canon": 9.355e-11,   # a0 = c H_Lambda / Z, Z = sqrt(32 pi/3)   [framework canonical]
      "alt":   1.13e-10}    # rho_total / c H0 footing                  [framework alt]
WC = {"canon": (1.78e-14, 2.21e-14),   # paper Sec 5.2 hardened window
      "alt":   (1.78e-14, 1.83e-14)}   # knife-edge, +2.7%
C   = 299792458.0
GM_E, R_E = 3.986004418e14, 6.371e6
GM_S, AU  = 1.32712440018e20, 1.495978707e11
G_SURF    = GM_E / R_E**2                      # 9.823 m/s^2 (Newtonian, no rotation)

# ---- frequency ladder (rad/s).  See Section 2 for WHICH one gates WHICH observable.
W_OPT_CARRIER = 2*np.pi*429.228e12    # Sr-87 clock transition   429 THz
W_AI_PULSE    = 2*np.pi*1.0e5         # AI Raman/Bragg pulse rate, ~100 kHz scale
W_AI_CYCLE    = 2*np.pi/1.0           # AI drop/measurement cycle ~1 Hz
W_AI_DROP     = 1.0/0.3               # 1/T, T ~ 0.3 s free-fall interrogation
W_MICRO_ORB   = 2*np.pi/5946.0        # MICROSCOPE orbit, T = 5946 s  (710 km, SSO)
W_MICRO_SPIN  = 2*np.pi*3.11e-4       # spin-mode rate ~3.1e-4 Hz; f_EP = f_orb + f_spin
W_ISS         = 2*np.pi/5580.0        # ISS orbit ~93 min
W_GALILEO     = 2*np.pi/(14.0805*3600) # Galileo eccentric sats, T = 14.08 h
W_EARTH_ROT   = 7.292115e-5           # sidereal rotation
W_TIDE_M2     = 2*np.pi/(12.4206*3600) # semidiurnal lunar tide
W_EARTH_ORB   = 2*np.pi/(365.256*86400)
W_SUN_GAL     = 233e3/(8.2*3.0857e19) # Sun's galactic orbit ~9.2e-16
W_DC          = 0.0

# ---- measurement anchors  [ANCHOR: literature, rounded CONSERVATIVELY toward weaker]
CLK_SYST         = 1.0e-18    # state-of-art optical-clock systematic (Al+ 9.4e-19, Sr ~2e-18)
SKYTREE_DH       = 450.0      # Takamoto+ Nat.Photon. 14, 411 (2020): Sr clocks, 450 m
SKYTREE_FRAC     = 1.0e-4     # agreement with GR as a FRACTION of the redshift (conservative)
BOTHWELL_DH      = 1.0e-3     # Bothwell+ Nature 602, 420 (2022): mm-scale redshift
BOTHWELL_ABS     = 7.6e-21    # fractional-frequency comparison uncertainty
GAL_A, GAL_E     = 27977e3, 0.162   # Galileo GSAT0201/0202 eccentric orbit
GAL_ALPHA        = 5.0e-5     # Delva+ PRL 121,231101 (2018) / Herrmann+ 231102: |alpha| < ~5e-5
AI_ABS_ACC       = 4.3e-8     # Gillot+ Metrologia 51, L15 (2014): 4.3 uGal absolute accuracy
AI_RESOLUTION    = 1.0e-10    # best long-integration resolution (~0.01 uGal)
AI_PROJECTED     = 1.0e-11    # 10-m fountain / space AI projection
MICRO_ETA        = (-1.5e-15, 2.3e-15)  # Touboul+ PRL 129,121102 (2022) (paper's ledger value)
MICRO_ALT        = 710e3
AI_WEP_ETA       = 1.8e-12    # Asenbaum+ PRL 125,191101 (2020) 85Rb/87Rb dual-species
EB_TI, EB_PT     = 8.723, 7.921        # MeV/nucleon, Ti-48 / Pt-195
M_NUCLEON_MEV    = 939.0
GW170817_ORDERS  = 6.5        # paper erratum v2: disformal photon sector excluded 6-7 orders

# =====================================================================================
# 1.  THE FRAMEWORK'S OWN AMPLITUDE:  A(a) = 1 - K = a0/(2|a|)   (derived, not adopted)
# =====================================================================================
head("1.  THE MI AMPLITUDE AT LAB / NEAR-EARTH ACCELERATIONS  (framework's own kernel)")
y = sp.symbols("y", positive=True)
K_sym = (sp.sqrt(1 + 4*y**2) - 1)/(2*y)          # K(X), X = |a|^2/a0^2, y = |a|/a0
ser = sp.series(1 - K_sym, y, sp.oo, 3).removeO()
lead = sp.limit((1 - K_sym)*2*y, y, sp.oo)
print(f"""
  Kernel (paper Sec 2.1):   K(X) = (sqrt(1+4X) - 1)/(2 sqrt(X)),   X = |a|^2/a0^2
  Inertia DEFICIT           A(|a|) == 1 - K  = {sp.nsimplify(ser)}
  large-|a| limit           lim 2y (1-K) = {lead}      =>   A = a0/(2|a|)   EXACT to O(a0^2/a^2)
  cross-check vs the a0-line: nu = g_obs/g_bar = sqrt(1 + a0/g_bar), mu = 1/nu = 1 - a0/(2 g_bar) + ...
  So the ANOMALOUS ACCELERATION is  delta_a = A*|a| = a0/2, CONSTANT, independent of |a|.
  This is the SAME a0/2 tail the paper faces at the planets (Sec 5.1), now at the lab.
""")
assert lead == sp.Rational(1, 1) or sp.simplify(lead - 1) == 0, "A -> a0/(2a) failed"

def A_amp(a_mag, foot):   return A0[foot]/(2.0*a_mag)
def a0_half(foot):        return A0[foot]/2.0

print(f"  {'setting':<44}{'|a| [m/s^2]':>13}{'|a|/a0 (canon)':>16}{'A canon':>12}{'A alt':>12}")
print("  " + "-" * 98)
_settings = [("ground lab clock / AI (supported or free-fall)", G_SURF),
             ("MICROSCOPE orbit (710 km)", GM_E/(R_E+MICRO_ALT)**2),
             ("ISS (410 km)", GM_E/(R_E+410e3)**2),
             ("Galileo perigee (r=23440 km)", GM_E/(GAL_A*(1-GAL_E))**2),
             ("Galileo apogee (r=32514 km)", GM_E/(GAL_A*(1+GAL_E))**2),
             ("electron in H atom (internal, a~9e22)", 9.0e22),
             ("nucleon in a nucleus (internal, a~1e29)", 1.0e29)]
for lab, am in _settings:
    print(f"  {lab:<44}{am:>13.4g}{am/A0['canon']:>16.3e}"
          f"{A_amp(am,'canon'):>12.3e}{A_amp(am,'alt'):>12.3e}")

r_deep_sun = np.sqrt(GM_S/A0["canon"]); r_deep_e = np.sqrt(GM_E/A0["canon"])
print(f"""
  THE EFE OBSTRUCTION (regression vs reviews/lab_door.py):  the deep-MOND regime |a| < a0 needs
      heliocentric r > sqrt(GM_sun/a0) = {r_deep_sun:.3e} m = {r_deep_sun/AU:.0f} AU
      geocentric   r > sqrt(GM_E/a0)   = {r_deep_e:.3e} m = {r_deep_e/R_E:.0f} R_E (Sun-dominated first)
  NO laboratory, no Earth orbit, no planetary probe reaches |a| < a0.  Every test below therefore
  probes the framework only through its HIGH-|a| tail amplitude A = a0/(2|a|) ~ 5e-12 at the ground.
  Atom interferometers reach ~1e-10 m/s^2 SENSITIVITY -- of order a0 itself -- but their test mass
  sits at |a| = g = {G_SURF:.2f} m/s^2 = {G_SURF/A0['canon']:.1e} a0.  Sensitivity ~ a0 does NOT buy access to
  the |a| ~ a0 regime; only the a0/2 tail is on offer.  (Section 4 shows why that still nearly bites.)
""")

# =====================================================================================
# 2.  THE GATE, AND *WHICH* FREQUENCY GATES A CLOCK / AN INTERFEROMETER
# =====================================================================================
head("2.  THE GATE  Re G(w) = 1/(1+(w/w_c)^2)  --  and the frequency-assignment argument")
w_s, wc_s = sp.symbols("omega omega_c", positive=True)
G_s = 1/(1 + sp.I*w_s/wc_s)
ident = sp.simplify(sp.Abs(G_s)**2 - sp.re(sp.expand(sp.simplify(G_s))))
assert sp.simplify(ident) == 0, "|G|^2 = Re G identity failed"
ReG0 = sp.limit(sp.re(sp.expand(sp.simplify(G_s))), w_s, 0)
assert sp.simplify(ReG0 - 1) == 0, "Re G(0) = 1 failed"

def ReG(w, wc): return 1.0/(1.0 + (w/wc)**2)

print(f"""
  sympy: |G|^2 - Re G = {sp.simplify(ident)}  (must be 0);   Re G(w->0) = {ReG0}  (must be 1)
  ==> FORK C IS A THEOREM OF THE GATE: a STATIC/DC anomaly is retained in FULL at EVERY w_c.
      No choice of the free fifth constant suppresses a DC signal.  That is why every observable
      below is computed twice.

  [ADOPTED #1 -- the frequency argument, following the paper's own prescription]
  The gate is a MEMORY kernel acting on the time-dependence of the BODY'S OWN acceleration.  The
  paper evaluates it at the frequency at which the body's acceleration VECTOR varies: w_gal = V/r
  for SPARC gas (lower window edge) and w_p = 2pi/T_p for planets (upper edge).  Applied here:
    * the optical CARRIER (429 THz) is NOT the gate argument -- it is an internal atomic frequency,
      not a variation of the body's acceleration.  Quoting it would inflate the suppression by 19
      orders for free.  It is listed below only to show it is the WRONG choice.
    * for a STATIC ground apparatus the acceleration MAGNITUDE |a| = g is constant (DC to ~1e-7,
      the tidal fraction), while its DIRECTION rotates in the u (cosmic) frame at w_Earth-rot.
      K's argument X = |a|^2/a0^2 is a SCALAR, so the scalar channel of a ground apparatus is
      INTRINSICALLY DC; only the vector/anisotropic channel (the gamma a_mu a_nu stress) rotates.
      => a ground lab is a Fork-A / Fork-C FORK in miniature.  Both are carried.
    * for an ORBITING clock/accelerometer the vector rotates at the orbital frequency, and the
      magnitude |a| = GM/r^2 also modulates at the orbital frequency if e != 0.
""")
print(f"  {'candidate frequency':<46}{'w [rad/s]':>12}{'Re G @2.21e-14':>16}"
      f"{'Re G @1.78e-14':>16}{'role':>12}")
print("  " + "-" * 102)
_ladder = [("optical clock carrier (Sr 429 THz)", W_OPT_CARRIER, "WRONG"),
           ("AI Raman/Bragg pulse rate (~100 kHz)", W_AI_PULSE, "WRONG"),
           ("AI drop/cycle rate (~1 Hz)", W_AI_CYCLE, "transient"),
           ("AI free-fall 1/T (T = 0.3 s)", W_AI_DROP, "transient"),
           ("MICROSCOPE EP frequency (orbit+spin)", W_MICRO_ORB + W_MICRO_SPIN, "USED"),
           ("ISS orbital", W_ISS, "USED"),
           ("Galileo orbital (T = 14.08 h)", W_GALILEO, "USED"),
           ("semidiurnal tide M2", W_TIDE_M2, "context"),
           ("Earth sidereal rotation", W_EARTH_ROT, "USED (gnd)"),
           ("Earth orbital", W_EARTH_ORB, "context"),
           ("Sun's galactic orbit", W_SUN_GAL, "BELOW w_c"),
           ("DC / static  (Fork C)", W_DC, "USED (DC)")]
for lab, wv, role in _ladder:
    print(f"  {lab:<46}{wv:>12.4e}{ReG(wv,2.21e-14) if wv>0 else 1.0:>16.3e}"
          f"{ReG(wv,1.78e-14) if wv>0 else 1.0:>16.3e}{role:>12}")
print(f"""
  Read the two columns: at EVERY frequency any clock or interferometer actually modulates at, the
  gate retains between 1e-19 and 1e-56 of the MI response.  The most permissive relevant case is
  the Sun's galactic orbit (w < w_c, Re G ~ 1) which no lab observable rides.  The single row where
  the gate does nothing at all is the last one.
""")

# =====================================================================================
# 3.  CHANNEL 1 -- GRAVITATIONAL REDSHIFT / CLOCK COMPARISON AT 1e-18
# =====================================================================================
head("3.  CHANNEL 1: CLOCK REDSHIFT / LOCAL POSITION INVARIANCE  (1e-18)")
print(f"""
  WHAT CAN THE ACTION TOUCH?  Matter couples MINIMALLY to the single metric g; S_EH is unmodified
  and no new field sources g.  So the redshift itself is GR's, exactly.  The only way a clock can
  feel K is if the inertial-scalar dressing W = s u.K(Box_u/a0^2).u reaches the clock's INTERNAL
  energy levels.  The action as written admits TWO readings, and they differ by ~3 orders of data:

  READING C1  [the paper's own words, Sec 2.2: "rods, clocks, and photons-in-g-sense ride g"]
      K dresses the CENTRE-OF-MASS kinetic term only.  Internal atomic structure is untouched.
      => delta_nu/nu = 0 IDENTICALLY, at every precision, gated or not.  STRUCTURAL null.

  READING C2  [the literal S_matter = -(1/2) int rho_m [s u.K.u]: rho_m is TOTAL mass-energy]
      The rest-mass density -- binding energy included -- is dressed by K(|a|^2/a0^2), so
      m_eff = m K and every transition frequency carries the factor K(|a|):
          nu_i / nu_j - 1 = K(a_i)/K(a_j) - 1 = A(a_j) - A(a_i),   A = a0/(2|a|), A ~ r^2.
      NOTE: a COMMON factor is unobservable (it rescales the second); frequency RATIOS at a FIXED
      |a| are also null because K carries no species label (m_e and m_p dress identically, so
      m_e/m_p, alpha, and every clock-ratio LPI test stay exactly null).  What survives is the
      comparison of two clocks at DIFFERENT |a| -- i.e. exactly a redshift experiment.
""")
def A_of_r(r, foot): return A0[foot]/(2.0*(GM_E/r**2))     # = a0 r^2/(2 GM)

clock_rows = []
# (a) Tokyo Skytree, 450 m
for foot in ("canon", "alt"):
    z_gr   = G_SURF*SKYTREE_DH/C**2
    dA     = A_of_r(R_E+SKYTREE_DH, foot) - A_of_r(R_E, foot)
    meas   = SKYTREE_FRAC*z_gr
    clock_rows.append(("Skytree 450 m (Takamoto+2020)", foot, z_gr, dA, meas, dA/meas))
# (b) Bothwell mm-scale
for foot in ("canon", "alt"):
    z_gr   = G_SURF*BOTHWELL_DH/C**2
    dA     = A_of_r(R_E+BOTHWELL_DH, foot) - A_of_r(R_E, foot)
    clock_rows.append(("mm-scale (Bothwell+2022)", foot, z_gr, dA, BOTHWELL_ABS, dA/BOTHWELL_ABS))
print(f"  {'DC-channel test (Reading C2)':<34}{'foot':<7}{'GR redshift':>13}{'MI anomaly':>13}"
      f"{'meas. accuracy':>16}{'anomaly/accuracy':>18}")
print("  " + "-" * 102)
for lab, foot, z, dA, meas, ratio in clock_rows:
    print(f"  {lab:<34}{foot:<7}{z:>13.3e}{dA:>13.3e}{meas:>16.3e}{ratio:>17.2e}x")

# (c) Galileo eccentric-orbit test, WITH the degeneracy projection done properly
head("3b.  GALILEO ECCENTRIC-ORBIT LPI TEST -- with the 1/r template projection (not assumed)")
M_anom = np.linspace(0, 2*np.pi, 20001)[:-1]
Ecc = M_anom.copy()
for _ in range(80):                       # Newton solve of Kepler's equation
    Ecc = Ecc - (Ecc - GAL_E*np.sin(Ecc) - M_anom)/(1 - GAL_E*np.cos(Ecc))
r_orb = GAL_A*(1 - GAL_E*np.cos(Ecc))
sig_z  = -2*GM_E/(C**2*r_orb)             # the GREAT template: modulating part ~ 1/r
sig_mi = {f: A0[f]*r_orb**2/(2*GM_E) for f in A0}      # A(r) = a0 r^2 / 2GM
def demean(x): return x - x.mean()
tz = demean(sig_z)
print(f"  redshift template modulation (pk-pk)  = {tz.max()-tz.min():.4e}   (fractional frequency)")
gal_rows = []
for foot in A0:
    s  = demean(sig_mi[foot])
    amp = s.max() - s.min()
    beta_fit = np.dot(s, tz)/np.dot(tz, tz)            # best-fit absorption into the GR template
    resid = s - beta_fit*tz
    nd = resid.max() - resid.min()                     # NON-degenerate residual, pk-pk
    r2 = np.dot(s, tz)**2/(np.dot(tz, tz)*np.dot(s, s))  # variance fraction absorbable by 1/r
    meas_abs = GAL_ALPHA*(tz.max()-tz.min())
    gal_rows.append((foot, amp, r2, nd, meas_abs, amp/meas_abs, nd/meas_abs))
print(f"\n  {'foot':<7}{'MI amp pk-pk':>14}{'var frac absorbed':>19}{'non-degen resid':>18}"
      f"{'LPI accuracy':>15}{'raw/acc':>11}{'resid/acc':>12}")
print("  " + "-" * 100)
for foot, amp, r2, nd, ma, rr, rn in gal_rows:
    print(f"  {foot:<7}{amp:>14.3e}{r2:>19.5f}{nd:>18.3e}{ma:>15.3e}{rr:>10.2e}x{rn:>11.2e}x")
print(f"""
  The MI anomaly scales as r^+2 while the redshift template scales as r^-1.  Projecting A(r) onto
  {{1, 1/r}} over one full orbit (uniform in mean anomaly, Kepler solved numerically) absorbs
  {100*gal_rows[0][2]:.3f}% of its VARIANCE -- so the eccentric-orbit fit is nearly, but not quite, blind to it.
  The orthogonal residual is {gal_rows[0][3]:.2e} pk-pk against an LPI accuracy of {gal_rows[0][4]:.2e},
  i.e. still {gal_rows[0][6]:.1e}x over.  The projection is COMPUTED, not assumed -- it is the load-bearing
  step, and it is what stops this from being a manufactured exclusion.
""")

# ---- the verdict table for Channel 1, both channels
head("3c.  CHANNEL 1 VERDICT -- gated vs DC, in orders")
best = max([r[5] for r in clock_rows] + [r[6] for r in gal_rows])
worst_gate = min(ReG(W_EARTH_ROT, 2.21e-14), ReG(W_GALILEO, 2.21e-14))
print(f"""
  GATED (AC) prediction.  Relevant frequency: Earth rotation {W_EARTH_ROT:.3e} rad/s for a ground pair
  (vector channel), Galileo orbital {W_GALILEO:.3e} rad/s for the satellite test.
      Re G(w_Earth-rot, w_c=2.21e-14) = {ReG(W_EARTH_ROT,2.21e-14):.3e}
      Re G(w_Galileo,   w_c=2.21e-14) = {ReG(W_GALILEO,2.21e-14):.3e}
      Skytree gated anomaly = {clock_rows[0][3]*ReG(W_EARTH_ROT,2.21e-14):.3e}  vs accuracy {clock_rows[0][4]:.2e}
      Galileo gated residual = {gal_rows[0][3]*ReG(W_GALILEO,2.21e-14):.3e}  vs accuracy {gal_rows[0][4]:.2e}
      => the gated clock channel is suppressed by ~{-np.log10(ReG(W_GALILEO,2.21e-14)):.0f} orders and is
         {gal_rows[0][4]/(gal_rows[0][3]*ReG(W_GALILEO,2.21e-14)):.1e}x BELOW reach.  NO CONSTRAINT.  Consistent, gated off.  Expected.

  DC prediction (Fork C, no gate).  Reading C2 is EXCLUDED:
      Skytree  {clock_rows[0][5]:.2e}x over accuracy   = {np.log10(clock_rows[0][5]):.1f} orders (canon)
      Galileo  {gal_rows[0][6]:.2e}x over accuracy (orthogonalized) = {np.log10(gal_rows[0][6]):.1f} orders (canon)
      alt footing: {np.log10(clock_rows[1][5]):.1f} / {np.log10(gal_rows[1][6]):.1f} orders.  Both footings excluded.
      Headline: the DC channel in the INTERNAL-ENERGY (clock) sector is excluded by
      {np.log10(best):.1f} ORDERS.  (mm-scale test is weaker: {clock_rows[2][5]:.2e}x, i.e. NOT excluding.)

  WHICH BRANCH OF THE CALIBRATION IS THIS?  (a), not (b).  It is a STRUCTURAL constraint on the
  matter coupling, not trouble for the framework: it says the MI dressing must NOT reach internal
  atomic energy levels -- i.e. the paper's own Reading C1 ("clocks ride g") is now DATA-REQUIRED,
  not merely asserted.  Under C1 the prediction is exactly zero and clocks say nothing at all.
  The 1e-18 clock frontier therefore buys the framework a MATTER-COUPLING SELECTION RULE, and no
  test of a0.  Anyone writing "clocks confirm the framework" would be manufacturing a win; anyone
  writing "clocks kill it" would be manufacturing a deficit.
""")

# =====================================================================================
# 4.  CHANNEL 2 -- ATOM INTERFEROMETRY / ABSOLUTE GRAVIMETRY  (the COM channel)
# =====================================================================================
head("4.  CHANNEL 2: ATOM INTERFEROMETRY & ABSOLUTE GRAVIMETRY  (centre-of-mass channel)")
print(f"""
  This is the channel Reading C1 leaves OPEN: the COM inertia IS dressed, so a free-falling atom
  in Earth's field accelerates at  g_obs = sqrt(g^2 + g a0) = g + a0/2 + O(a0^2/g).
  DC prediction:  delta_g = a0/2 = {a0_half('canon'):.3e} (canon) / {a0_half('alt'):.3e} (alt) m/s^2.

  THE INTERESTING COINCIDENCE, stated precisely:  a0/2 = {a0_half('canon'):.2e} m/s^2 sits at the SAME
  order as the best AI resolution ({AI_RESOLUTION:.0e} m/s^2) -- {AI_RESOLUTION/a0_half('canon'):.1f}x above it -- and only
  {AI_ABS_ACC/a0_half('canon'):.0f}x below the best ABSOLUTE accuracy ({AI_ABS_ACC:.1e} m/s^2).  So on raw numbers this is the
  closest any laboratory gets to the framework's own tail.  It still does not bite, and the reason
  is DEGENERACY, not precision: a uniform additive a0/2 along g is indistinguishable from the local
  value of g (GM_E, geology, local mass) which is not independently predicted at the 1e-12 level.
""")
print(f"  {'AI observable':<44}{'MI DC signal':>14}{'reach':>13}{'signal/reach':>14}{'limited by':>14}")
print("  " + "-" * 100)
ai_rows = []
# (a) single-station absolute g
ai_rows.append(("absolute g, single station (DEGENERATE)", a0_half("canon"), AI_ABS_ACC, "degeneracy"))
# (b) vertical gradient: d/dz (a0/2) = 0 exactly
ai_rows.append(("vertical gradient dg/dz (exact null)", 0.0, 5.0e-9, "structure"))
# (c) non-degenerate residual after fitting GM over a height baseline
for dh, tag in [(450.0, "450 m"), (1000.0, "1 km"), (10.0, "10 m fountain")]:
    nd = a0_half("canon")*(1 - (R_E/(R_E+dh))**2)     # residual after refitting GM at the base
    ai_rows.append((f"height-baseline residual, {tag}", nd, AI_RESOLUTION, "precision"))
for lab, sig, reach, lim in ai_rows:
    rr = (sig/reach) if reach > 0 else 0.0
    print(f"  {lab:<44}{sig:>14.3e}{reach:>13.2e}{rr:>14.2e}{lim:>14}")
nd450 = a0_half("canon")*(1 - (R_E/(R_E+450.0))**2)
print(f"""
  Detail of the non-degenerate construction: fit GM' at the base station, so the constant a0/2 is
  fully absorbed there; at height h the residual is (a0/2)[1 - (R/(R+h))^2] ~ (a0/2)(2h/R).
  At h = 450 m that is {nd450:.3e} m/s^2, which is {AI_RESOLUTION/nd450:.1e}x = {np.log10(AI_RESOLUTION/nd450):.1f} orders BELOW the best AI
  resolution, and {AI_PROJECTED/nd450:.1e}x below even the projected 10-m-fountain / space-AI figure.
  The gravity GRADIENT is an EXACT null: d/dz of a constant a0/2 is zero, so AI gradiometers --
  the most systematics-immune AI configuration -- have exactly zero MI signal by construction.

  GATED (AC) prediction.  For a ground AI the magnitude |a| = g is DC; the vector rotates at
  w_Earth-rot.  Re G({W_EARTH_ROT:.2e}) = {ReG(W_EARTH_ROT,2.21e-14):.3e}  =>  delta_g_gated = {a0_half('canon')*ReG(W_EARTH_ROT,2.21e-14):.3e} m/s^2,
  i.e. {AI_ABS_ACC/(a0_half('canon')*ReG(W_EARTH_ROT,2.21e-14)):.1e}x below reach: suppressed by ~{-np.log10(ReG(W_EARTH_ROT,2.21e-14)):.0f} orders.  NO CONSTRAINT.  Consistent, gated off.
  If instead one gates at the drop transient 1/T (T = 0.3 s): Re G = {ReG(W_AI_DROP,2.21e-14):.2e} -- {-np.log10(ReG(W_AI_DROP,2.21e-14)):.0f} orders.
  Either assignment kills it; the AC verdict is assignment-robust.

  DC prediction (Fork C, no gate):  NOT EXCLUDED.  Single-station absolute gravimetry is
  {AI_ABS_ACC/a0_half('canon'):.0f}x short AND degenerate; the non-degenerate height-baseline residual is {np.log10(AI_RESOLUTION/nd450):.1f} orders short;
  the gradient signal is identically zero.  Atom interferometry cannot test the DC COM channel now
  or with any near-term (x10-x100) improvement.  Stating otherwise would manufacture a constraint.
""")

# =====================================================================================
# 5.  CHANNEL 3 -- WEP: IS eta = 0 STRUCTURAL, OR ONLY APPROXIMATE?
# =====================================================================================
head("5.  CHANNEL 3: WEP / MICROSCOPE 1e-15 -- structural zero, and the composition question")
print(f"""
  THE VERIFICATION GAP, stated honestly.  The paper derives eta = 0 and machine-verifies a residual
  < 1e-12 over y in [1e-2, 1e2] (matter_coupling_Tmunu.py).  MICROSCOPE measures eta at 2.3e-15 --
  {1e-12/2.3e-15:.0f}x = {np.log10(1e-12/2.3e-15):.1f} orders TIGHTER than the numerical residual.  Is the derived zero exact?

  ANSWER FROM THE ACTION: YES, STRUCTURALLY -- with one named premise.
    * W = s u^mu K(Box_u/a0^2) u_mu is built from (u, g, partial u) ONLY.  It carries no species
      label, no charge, no baryon number, no binding-energy operator.  There is no object in the
      matter coupling that COULD distinguish Ti from Pt.
    * K's argument is X = |a|^2/a0^2 via the worldline-general identity u_mu Box_u u^mu = -|a|^2.
      Two co-located bodies share |a|, hence share K, hence share the SAME fractional inertia
      deficit A = a0/(2|a|).  The force balance inverts species-independently: eta = 0 EXACTLY.
    * Therefore the 1e-12 residual is a FLOATING-POINT / grid artifact of the check, NOT a physical
      prediction of 1e-12-level violation.  The derivation's zero is composition-independent BY
      CONSTRUCTION, and the correct statement is: eta = 0 to all orders in a0/|a|, so MICROSCOPE's
      1e-15 is passed by STRUCTURE and the 1e-12 number should not be quoted as the theory's bound.

  THE PREMISE THAT DOES THE WORK (and the loophole MICROSCOPE actually probes).  "The BODY'S OWN
  worldline" must mean the COLLECTIVE / centre-of-mass worldline.  A modified-INERTIA kernel could
  instead act on CONSTITUENT worldlines: nucleons inside a nucleus have |a| ~ 1e29 m/s^2, electrons
  ~ 1e23, so a per-constituent dressing gives A ~ a0/(2*1e29) ~ 1e-40 -- it would DESTROY the MOND
  effect for all composite matter.  The framework therefore REQUIRES the collective reading.  But a
  MIXED weighting -- fraction f of the dressing tracking internal binding energy rather than total
  rest mass -- is not excluded by the action's form, and it IS composition-dependent.
""")
dEB = (EB_TI - EB_PT)/M_NUCLEON_MEV
eta_bound_2s = abs(MICRO_ETA[0]) + 2*MICRO_ETA[1]
r_micro = R_E + MICRO_ALT
print(f"  [ASSUMPTION -- order-of-magnitude composition proxy]  Delta(E_B/Mc^2) for Ti-48 vs Pt-195")
print(f"  = ({EB_TI} - {EB_PT}) MeV/nucleon / {M_NUCLEON_MEV:.0f} MeV = {dEB:.3e}")
print(f"\n  {'footing':<8}{'A at MICROSCOPE orbit':>24}{'eta(f=1) DC':>14}{'MICROSCOPE 2sig':>17}"
      f"{'f allowed':>12}{'eta gated':>13}")
print("  " + "-" * 96)
wep_rows = []
for foot in A0:
    Amic = A_amp(GM_E/r_micro**2, foot)
    eta_dc = dEB*Amic
    f_allow = eta_bound_2s/eta_dc
    eta_g = eta_dc*ReG(W_MICRO_ORB + W_MICRO_SPIN, 2.21e-14)
    wep_rows.append((foot, Amic, eta_dc, f_allow, eta_g))
    print(f"  {foot:<8}{Amic:>24.3e}{eta_dc:>14.3e}{eta_bound_2s:>17.2e}{f_allow:>12.2f}{eta_g:>13.2e}")
print(f"""
  READ THIS CAREFULLY -- it is the sharpest number in the ledger and it cuts both ways:
    * A FULL-STRENGTH binding-energy-weighted MI dressing (f = 1) predicts eta = {wep_rows[0][2]:.2e} (canon)
      / {wep_rows[1][2]:.2e} (alt), against MICROSCOPE's 2-sigma allowance {eta_bound_2s:.2e}.  MICROSCOPE lands
      EXACTLY at the interesting scale: it constrains f <= {wep_rows[0][3]:.2f} (canon) / {wep_rows[1][3]:.2f} (alt).
    * So MICROSCOPE does NOT yet exclude an O(1) composition-dependent admixture -- it is at the
      knife of it.  A x10 successor (eta ~ 1e-16) would exclude f >= {eta_bound_2s/10/wep_rows[0][2]:.2f}, i.e. would enforce
      the pure-rho_m collective reading at the 10% level.  That is a REAL, cheap, decisive test of
      the framework's matter coupling, and it is the only lab test in this ledger that is within
      one instrument generation of the framework's own amplitude.
    * It is NOT a deficit today: the framework's stated coupling has f = 0 exactly, eta = 0, pass.
    * GATED: at the MICROSCOPE EP frequency {W_MICRO_ORB+W_MICRO_SPIN:.2e} rad/s, Re G = {ReG(W_MICRO_ORB+W_MICRO_SPIN,2.21e-14):.2e}, so even the
      f = 1 signal becomes {wep_rows[0][4]:.2e} -- {-np.log10(ReG(W_MICRO_ORB+W_MICRO_SPIN,2.21e-14)):.0f} orders down.  The AC channel is dead here too;
      MICROSCOPE, like every other row, constrains ONLY the DC channel.
    * Dual-species atom interferometry (85Rb/87Rb, eta ~ {AI_WEP_ETA:.1e}) is {AI_WEP_ETA/wep_rows[0][2]:.0f}x weaker than
      MICROSCOPE on the same f, and Rb-Rb has Delta(E_B/M) ~ 1e-3 x smaller still.  Not competitive.
""")

# =====================================================================================
# 6.  CHANNEL 4 -- the disformal photon metric in a clock LINK (photon sector, separate)
# =====================================================================================
head("6.  CHANNEL 4: the disformal photon metric in an optical clock LINK  (S_photon, separate)")
gradB = 4*(A0["canon"]/2)/C**2      # grad B = 4(nu-1) g_bar / c^2 -> 2 a0/c^2 in the Newtonian tail
print(f"""
  Matter rides g, photons ride g_tilde = g + B u u, so a clock comparison carried over an OPTICAL
  LINK accumulates the two-metric mismatch B/2 along the path.  In the Newtonian tail
  (nu - 1) g_bar = a0/2 EXACTLY (the a0-line), so the gradient is scale-free:
      grad B = 4 (nu-1) g_bar / c^2 = 2 a0 / c^2 = {gradB:.3e} per metre   (canon)
  [ADOPTED: the /c^2 restores dimensions on the paper's grad B = 4(nu-1) g_bar; cross-checked
   against the paper's own B ~ 6-7e-7 at a galaxy: 4(V^2/c^2)ln(r2/r1) ~ 2e-6 for V=150 km/s. OK.]
""")
print(f"  {'link baseline':<26}{'Delta B':>13}{'signal B/2':>13}{'vs 1e-18 clock':>17}")
print("  " + "-" * 72)
for L, tag in [(1.0, "1 m"), (1.0e3, "1 km"), (1.0e6, "1000 km"), (R_E, "Earth radius")]:
    dB = gradB*L
    print(f"  {tag:<26}{dB:>13.3e}{dB/2:>13.3e}{(dB/2)/CLK_SYST:>17.2e}")
print(f"""
  Even over an Earth-radius baseline the effect is {gradB*R_E/2/CLK_SYST:.1e} of a 1e-18 clock, i.e.
  ~{-np.log10(gradB*R_E/2/CLK_SYST):.0f} orders below reach -- and this is DC, so the gate is irrelevant here too.
  Separately: this whole sector is already GW170817-excluded by ~{GW170817_ORDERS:.0f}-7 orders (paper erratum v2),
  so it is a dead sector regardless.  Recorded for completeness; carries no weight in the verdict.
""")

# =====================================================================================
# 7.  THE LEDGER
# =====================================================================================
head("7.  THE PRECISION-CONSISTENCY LEDGER  (clocks + atom interferometry)")
hdr = (f"  {'observable':<32}{'rel. w [rad/s]':>15}{'Re G (gate)':>12}"
       f"   {'GATED verdict':<20}{'DC verdict':<34}")
print(hdr); print("  " + "-" * 115)
ledger = [
 ("clock redshift, Reading C1", W_EARTH_ROT, ReG(W_EARTH_ROT,2.21e-14),
  "0 (structural)", "0 (structural) - no test"),
 ("clock redshift, Reading C2 gnd", W_EARTH_ROT, ReG(W_EARTH_ROT,2.21e-14),
  f"{-np.log10(ReG(W_EARTH_ROT,2.21e-14)):.0f} ord down: none", f"EXCLUDED {np.log10(clock_rows[0][5]):.1f} ord"),
 ("clock redshift, C2 Galileo", W_GALILEO, ReG(W_GALILEO,2.21e-14),
  f"{-np.log10(ReG(W_GALILEO,2.21e-14)):.0f} ord down: none", f"EXCLUDED {np.log10(gal_rows[0][6]):.1f} ord"),
 ("AI absolute g (single stn)", W_EARTH_ROT, ReG(W_EARTH_ROT,2.21e-14),
  f"{-np.log10(ReG(W_EARTH_ROT,2.21e-14)):.0f} ord down: none", f"NOT excl (degenerate; {AI_ABS_ACC/a0_half('canon'):.0f}x short)"),
 ("AI height-baseline residual", W_EARTH_ROT, ReG(W_EARTH_ROT,2.21e-14),
  f"{-np.log10(ReG(W_EARTH_ROT,2.21e-14)):.0f} ord down: none", f"NOT excl ({np.log10(AI_RESOLUTION/nd450):.1f} ord short)"),
 ("AI gravity gradiometry", W_EARTH_ROT, ReG(W_EARTH_ROT,2.21e-14),
  "0 (exact null)", "0 (exact null) - no test"),
 ("MICROSCOPE WEP eta (f=0)", W_MICRO_ORB+W_MICRO_SPIN, ReG(W_MICRO_ORB+W_MICRO_SPIN,2.21e-14),
  "0 (structural)", "0 (structural): PASS"),
 ("MICROSCOPE WEP eta (f=1)", W_MICRO_ORB+W_MICRO_SPIN, ReG(W_MICRO_ORB+W_MICRO_SPIN,2.21e-14),
  f"{-np.log10(ReG(W_MICRO_ORB+W_MICRO_SPIN,2.21e-14)):.0f} ord down: none", f"KNIFE: f <= {wep_rows[0][3]:.2f}"),
 ("dual-species AI WEP", W_AI_CYCLE, ReG(W_AI_CYCLE,2.21e-14),
  f"{-np.log10(ReG(W_AI_CYCLE,2.21e-14)):.0f} ord down: none", f"NOT excl ({AI_WEP_ETA/wep_rows[0][2]:.0f}x weaker)"),
 ("optical-link disformal B/2", W_DC, 1.0,
  "n/a (DC by nature)", f"NOT excl ({-np.log10(gradB*R_E/2/CLK_SYST):.0f} ord short)"),
]
for lab, wv, rg, gv, dv in ledger:
    print(f"  {lab:<32}{wv:>15.3e}{rg:>12.2e}   {gv:<20}{dv:<34}")

# ---- prove-by-moving-the-number: how much weaker must the anchors be to erase the C2 exclusion?
print(f"""
  ROBUSTNESS OF THE ONE EXCLUSION IN THIS LEDGER (prove-by-moving-the-number):
    Skytree would have to be {clock_rows[0][5]:.0f}x LESS accurate (agreement at {SKYTREE_FRAC*clock_rows[0][5]:.1e} of the redshift
      instead of {SKYTREE_FRAC:.0e}) for the Reading-C2 exclusion to vanish there.
    Galileo would need |alpha| < {GAL_ALPHA*gal_rows[0][6]:.1e} instead of {GAL_ALPHA:.0e} -- {gal_rows[0][6]:.0f}x weaker.
    Both anchors were already entered rounded toward WEAKER than published.  The exclusion also
    survives the footing swap ({np.log10(clock_rows[1][5]):.1f} / {np.log10(gal_rows[1][6]):.1f} orders) and the full 1/r-template orthogonalization
    (which removes {100*gal_rows[0][2]:.1f}% of the signal variance and still leaves {gal_rows[0][6]:.0f}x).
    It does NOT survive being applied to Reading C1 -- where the prediction is exactly zero.
""")

head("8.  VERDICT")
print(f"""
  (i) GATED / AC CHANNEL -- CONSISTENT, GATED OFF, at every row.
      Suppression factors, at the window's MOST PERMISSIVE corner w_c = 2.21e-14 rad/s:
          ground apparatus (w = Earth rotation {W_EARTH_ROT:.2e}):  Re G = {ReG(W_EARTH_ROT,2.21e-14):.2e}  ({-np.log10(ReG(W_EARTH_ROT,2.21e-14)):.0f} orders)
          MICROSCOPE / LEO (w ~ 1e-3):                        Re G = {ReG(W_MICRO_ORB+W_MICRO_SPIN,2.21e-14):.2e}  ({-np.log10(ReG(W_MICRO_ORB+W_MICRO_SPIN,2.21e-14)):.0f} orders)
          Galileo (w = {W_GALILEO:.2e}):                          Re G = {ReG(W_GALILEO,2.21e-14):.2e}  ({-np.log10(ReG(W_GALILEO,2.21e-14)):.0f} orders)
          AI drop transient (1/T, T=0.3 s):                   Re G = {ReG(W_AI_DROP,2.21e-14):.2e}  ({-np.log10(ReG(W_AI_DROP,2.21e-14)):.0f} orders)
      No clock or interferometer constrains the framework in the AC channel, and none can: the
      gap between w_c ~ 2e-14 rad/s (period ~1.6 Myr) and any lab modulation is 9-20 orders in w,
      hence 18-40 orders in Re G.  This is a legitimate low-value "no constraint", reported
      quantitatively.  It is NOT evidence for the framework.

  (ii) DC CHANNEL (Fork C) -- SPLIT VERDICT, and this is the informative half.
      EXCLUDED, by {np.log10(best):.1f} orders: a DC MI dressing that reaches INTERNAL atomic energy levels
        (Reading C2 of S_matter = -(1/2) int rho_m [s u.K.u]).  Skytree {np.log10(clock_rows[0][5]):.1f} orders,
        Galileo {np.log10(gal_rows[0][6]):.1f} orders after orthogonalizing against the 1/r redshift template.
        Both footings, no footing-dependence of the verdict.
        => calibration branch (a): this CONSTRAINS THE THEORY'S STRUCTURE.  The paper's Reading C1
           ("rods, clocks and photons-in-g-sense ride g") is not a stylistic choice -- it is now
           REQUIRED BY 1e-18 CLOCK DATA.  Under C1 the clock prediction is identically zero.
      NOT EXCLUDED: the DC MI dressing of the CENTRE-OF-MASS inertia -- the a0/2 = {a0_half('canon'):.2e} /
        {a0_half('alt'):.2e} m/s^2 tail.  Absolute gravimetry is {AI_ABS_ACC/a0_half('canon'):.0f}x short and, more decisively,
        DEGENERATE with the local value of g; the non-degenerate height-baseline residual is
        {np.log10(AI_RESOLUTION/nd450):.1f} orders short; gradiometry is an exact null.
      KNIFE-EDGE: the composition-dependence of the DC dressing.  MICROSCOPE's 1e-15 sits exactly
        at f ~ 1 of a binding-energy-weighted admixture (f <= {wep_rows[0][3]:.2f} canon / {wep_rows[1][3]:.2f} alt).

  (iii) INDEPENDENT LINE ON FORK C.  Clocks + atom interferometry do NOT close Fork C.  They
      close HALF of it -- the internal-energy half -- by {np.log10(best):.1f} orders, and leave the COM half
      (the half that actually carries the a0/2 planetary tail, hence the half Fork C is about)
      entirely untouched.  The ephemerides, not the lab, remain the DC channel's binding
      constraint (paper Sec 5.1: 1e3-1e4x ungated exclusion).  So: Fork C stays LIVE, and this
      ledger's contribution is a matter-coupling selection rule plus a x10-away WEP test.

  (iv) WHAT WOULD MAKE THE LAB BITE (forecast, not a claim):
      * a x10 MICROSCOPE successor (eta ~ 1e-16) -> excludes composition admixture f >= {eta_bound_2s/10/wep_rows[0][2]:.2f}.
      * DC accelerometry at 1e-11 m/s^2 ABSOLUTE accuracy far from the Sun: at 100 AU
        g_N = {GM_S/(100*AU)**2:.2e} m/s^2, so a0/2 / g_N = {a0_half('canon')/(GM_S/(100*AU)**2):.1e} -- a {a0_half('canon')/1e-11:.0f}-sigma signal for a
        1e-11 m/s^2-accurate instrument.  The obstacle is DC BIAS accuracy, not noise.
      * clocks: nothing.  Under the data-required Reading C1 the clock channel is exactly zero,
        so improving 1e-18 -> 1e-21 changes nothing.  Said plainly so it is not oversold.

  SCOPE: dynamics sector S_matter, plus one recorded (already-excluded) S_photon row.  No claim
  that any door is closed; w_c and a0's value remain postulates, unchanged by this ledger.
""")
print(RULE)
print("mi_clocks_atominterferometry_2026.py: sympy identities passed (|G|^2=ReG, ReG(0)=1, A->a0/2a);")
print("Kepler solve converged; Galileo template projection computed numerically.  exit 0.")
print(RULE)
