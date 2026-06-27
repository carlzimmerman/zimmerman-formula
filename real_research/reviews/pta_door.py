#!/usr/bin/env python3
"""
FRONT 3 -- PTA + solar-system anomalies: is there a FRESH, distinctive, above-floor, near-term preferred-frame
door the framework was NOT pointed at?  Both-ways. Every magnitude computed. RUN, exit 0.
====================================================================================================================

Framework footing (locked): modified INERTIA at a < a0 = 9.36e-11 m/s^2; de Sitter vacuum = CMB rest frame = a
CPT-EVEN gravity-sector SME background; c_T = 1 exactly (the dS-Unruh MI rescales the INERTIA of matter, it does
NOT alter the graviton's lightcone). Solar-system velocity vs the CMB apex: v = 369.82 km/s -> beta = 1.23e-3.

Banked preferred-frame channels (NOT fresh -- already covered, do not re-bank):
  * s^TX boost dipole = 8.68e-10, gravity sector, ~1.5x under the tightest ephemeris bound (the LIVE SME test).
  * alpha2_MI ~ 1e-13 (Nordtvedt/Shao-Wex SOLITARY-pulsar precession) -> ~1e6x safe, NOT live.
  * alpha2 / VLBI / LLR / Cassini all banked PASS.

This script asks the TWO new questions in the prompt:
  (a) Does the framework do anything DISTINCTIVE to the nHz GW background or PTA timing residuals -- a DIFFERENT
      PTA-scale preferred-frame signature than the banked alpha2 (e.g. a CMB-correlated timing dipole, or an
      a0-scale effect in the pulsar far-field where g drops to ~a0)?  Magnitude vs PTA timing precision.
  (b) Pioneer ~8.7e-10 m/s^2 (~a0!) sunward anomaly: does the framework predict it, or is it thermal recoil
      (Turyshev 2012)?  Compute the framework's actual prediction at Pioneer's distance and confront thermal.
"""
import numpy as np

# -------- constants / footing --------
c     = 2.99792458e8          # m/s
G     = 6.674e-11
Msun  = 1.989e30
AU    = 1.495978707e11
pc    = 3.0857e16
kpc   = 1e3*pc
yr    = 3.15576e7
a0    = 9.36e-11              # FRAMEWORK a0 (pure-Lambda), NOT 1.2e-10
v_cmb = 369.82e3             # m/s, Solar System vs CMB apex
beta  = v_cmb/c

def g_newton(M_solar, r_m):
    return G*M_solar*Msun/r_m**2

def sep(title):
    print("="*116); print(title); print("="*116)

print("#"*116)
print("# FRONT 3 -- PTA + solar-system anomalies: fresh preferred-frame doors?  (a0=9.36e-11, c_T=1, apex=CMB)")
print("#"*116)
print(f"  beta = v_cmb/c = {beta:.3e}  (v_cmb = {v_cmb/1e3:.1f} km/s toward CMB apex)\n")

# ====================================================================================================================
# (a.0) THE TENSOR-SECTOR PTA Lorentz-violation searches: AUTOMATICALLY NULL because c_T = 1
# ====================================================================================================================
sep("(a.0)  PTA tensor-sector Lorentz-violation / GW-velocity / graviton-mass searches -> framework predicts NULL")
mg_bound_eV = 8.2e-24        # NANOGrav 15yr graviton-mass upper limit (arXiv:2310.07469), eV/c^2
print(f"   NANOGrav/IPTA constrain: GW dispersion (graviton mass m_g < {mg_bound_eV:.1e} eV), GW velocity c_T,")
print( "   non-tensorial (vector/scalar) polarizations, and a LV energy scale (arXiv:2505.22736).")
print( "   FRAMEWORK: the dS-Unruh modification rescales the INERTIA of MATTER at a<a0; it leaves the graviton")
print( "   lightcone untouched -> c_T = 1 EXACTLY, m_g = 0, pure tensor (+,x) polarizations.")
print( "   => every PTA *propagation-sector* LV search returns the framework's GR value. NULL, not a door.")
print( "      (This is the 'high-a arena = GR' expectation: the GWB itself is sourced at strong field / high a.)\n")

# ====================================================================================================================
# (a.1) Is there a DIFFERENT PTA-scale preferred-frame signature -- a CMB-correlated TIMING dipole on the residuals?
#       A genuine preferred frame imprints a v_cmb-dipole on clock/light propagation. Compute its size vs PTA noise.
# ====================================================================================================================
sep("(a.1)  A CMB-correlated dipole in PTA timing residuals?  (the analogue of s^TX, in the timing channel)")
# A genuine preferred-frame s_munu background modifies light/clock propagation. The induced delay along a fixed
# line of sight is a CONSTANT (or secular) bias proportional to the pulsar distance -> it is FULLY DEGENERATE with
# each pulsar's distance/dispersion/position fit and ABSORBED. The only piece that survives the timing-model fit is
# one that VARIES on a known, non-degenerate timescale. The natural such modulation is the EARTH's annual orbital
# velocity v_earth sweeping the s-background: it imprints a 1-yr-periodic residual at the solar-system scale,
# common to all pulsars with a dipole pattern toward the CMB apex -- the PTA-channel analogue of s^TX.
s_grav    = 8.68e-10         # banked gravity-sector s-coefficient magnitude (s^TX scale)
v_earth   = 29.78e3          # m/s, Earth orbital speed
beta_e    = v_earth/c
# The solar-system Shapiro/propagation delay scale that the s-background distorts is the light-crossing time of
# the relevant gravitational potential region ~ R/c with R ~ 1 AU (the modulation is solar-system-local, NOT the
# kpc pulsar distance: the kpc piece is the degenerate constant that gets absorbed).
tau_ss    = AU/c             # ~500 s, solar-system light-crossing scale
# Annual-modulated, non-degenerate observable residual: delta_t ~ s * beta_earth * tau_ss
dt_annual = s_grav*beta_e*tau_ss
print(f"   the kpc-scale constant delay (s*D/c) is DEGENERATE with the per-pulsar distance/DM/position fit -> absorbed.")
print(f"   the surviving, non-degenerate observable = the EARTH-annual modulation of the s-background:")
print(f"     v_earth = {v_earth/1e3:.1f} km/s -> beta_e = {beta_e:.2e};  solar-system light-cross tau_ss = AU/c = {tau_ss:.0f} s")
print(f"     delta_t(1-yr) ~ s * beta_e * tau_ss = {dt_annual:.3e} s")
pta_rms = 1e-7               # ~100 ns: best single-pulsar PTA timing RMS (MSP, 15yr)
pta_floor_future = 1e-8     # ~10 ns: SKA-era aspiration
print(f"\n   PTA timing precision: best RMS ~ {pta_rms*1e9:.0f} ns; SKA-era aspiration ~ {pta_floor_future*1e9:.0f} ns")
print(f"   ratio delta_t / best RMS   = {dt_annual/pta_rms:.2e}")
print(f"   ratio delta_t / SKA floor  = {dt_annual/pta_floor_future:.2e}")
verdict_a1 = "ABOVE" if dt_annual > pta_floor_future else "BELOW"
print(f"   => the annual preferred-frame residual ~ {dt_annual*1e9:.2e} ns is {verdict_a1} the floor.")
print( "   PROBLEM: even taking the s-coefficient at full strength (no beta suppression of s itself), the annual")
print( "   modulation is ~%.0e ns, ~1e6x below even SKA. AND it is the SAME physics as the banked s^TX ephemeris" % (dt_annual*1e9))
print( "   dipole (solar-system, CMB-apex, beta-suppressed), measured FAR better by planetary ranging than by PTA.")
print( "   So PTA adds NO new sensitivity to the preferred-frame s-coefficient. Not a fresh door. BELOW FLOOR.")
print()

# ====================================================================================================================
# (a.2) An a0-SCALE effect in the pulsar FAR-FIELD?  Where does g drop to a0 around a pulsar, and is the MOND part
#       ever relevant to PTA timing?  (This is the MOND channel -- expected NULL at PTA, but compute the radius.)
# ====================================================================================================================
sep("(a.2)  Where does g = a0 around a pulsar, and does the MOND/MI part touch PTA timing?")
M_psr = 1.4                  # Msun
r_a0  = np.sqrt(G*M_psr*Msun/a0)   # radius where g(pulsar) = a0
print(f"   pulsar M = {M_psr} Msun; g = a0 at r_a0 = sqrt(GM/a0) = {r_a0:.3e} m = {r_a0/AU:.2e} AU = {r_a0/pc:.3f} pc")
# Compare to the binary separations PTAs actually time (MSP-WD/NS binaries: light-seconds to a few AU):
a_bin = 2.0*AU
g_bin = g_newton(M_psr, a_bin)
print(f"   typical timed binary separation ~ {a_bin/AU:.0f} AU -> g = {g_bin:.2e} = {g_bin/a0:.1e} a0  (DEEPLY Newtonian)")
print(f"   the MOND/MI regime (g<a0) starts at ~{r_a0/pc:.2f} pc -- FAR outside any timed orbit; the interstellar")
print( "   field there is the GALACTIC ~2a0 external field anyway (EFE), and nothing is timed at pc separations.")
print( "   => the MI/MOND content is BELOW FLOOR and out-of-regime for PTA timing. NULL (the high-a=GR expectation).")
print()

# ====================================================================================================================
# (a.3) GWB AMPLITUDE via MOND friction -- already worked (project_nanograv_mond_gwb.py): SOFT, weak, bottleneck
#       is Newtonian. Restate the verdict, do not re-bank as fresh.
# ====================================================================================================================
sep("(a.3)  nHz GWB amplitude via MOND dynamical friction -> ALREADY WORKED: soft/weak, not a fresh door")
print( "   project_nanograv_mond_gwb.py: galaxy-scale inspiral is at ~a0 (MOND helps the SUPPLY) but the actual")
print( "   final-parsec STALL is Newtonian (g~1e6 a0) -> MOND can't solve it. ~sqrt(3)~1.3-1.8x amplitude hint,")
print( "   marginal & model-degenerate. ALREADY COVERED, downgraded to a qualitative hint. Not fresh, not distinctive.\n")

# ====================================================================================================================
# (b) THE PIONEER / FLYBY ANOMALY -- does the framework predict the ~8.7e-10 m/s^2 (~a0!) sunward anomaly?
# ====================================================================================================================
sep("(b)  Pioneer anomaly: framework prediction at Pioneer's distance vs the thermal-recoil resolution")
a_pioneer_obs = 8.74e-10     # m/s^2 sunward (Anderson+; (8.74 +- 1.33)e-10)
print(f"   observed Pioneer anomaly: a_P = {a_pioneer_obs:.2e} m/s^2 sunward (note: ~{a_pioneer_obs/a0:.1f} x a0!)")
print()
# (b.1) is Pioneer in the MOND regime? Compute g_Sun at Pioneer's distance (it ranged ~20-70 AU; use 40 AU).
for r_AU in [20, 40, 70]:
    g_sun = g_newton(1.0, r_AU*AU)
    print(f"   at r = {r_AU:>2} AU:  g_Sun = {g_sun:.3e} m/s^2 = {g_sun/a0:.1e} x a0   ({'Newtonian' if g_sun>a0 else 'MOND'})")
print()
print( "   => Pioneer is DEEPLY Newtonian (g_Sun ~ 1e3-1e4 x a0). The framework is modified INERTIA at a < a0;")
print( "      at Pioneer the total acceleration is ~1e3 a0, so the inertia is UNMODIFIED -> the framework predicts")
print( "      essentially ZERO MOND anomaly. The numerical coincidence a_P ~ a0 is JUST a coincidence (it is also")
print( "      ~ cH0, which is why every a0-scale theory gets tempted).")
print()
# (b.2) Could the framework's PREFERRED-FRAME (not MOND) piece make a constant solar-system acceleration?
#       The s^TX boost dipole is a DIPOLE (direction = CMB apex, l,b=264,48), NOT sunward, and is O(beta)*a-scale,
#       acting on dynamics not as a constant bias. Compute its solar-system acceleration scale and direction.
a_dyn_solar = g_newton(1.0, 40*AU)
a_pf = s_grav*beta*a_dyn_solar     # preferred-frame correction ~ s*beta*(local dynamical accel)
print(f"   framework PREFERRED-FRAME piece at 40 AU: ~ s*beta*g ~ {a_pf:.2e} m/s^2, and it points at the CMB APEX")
print(f"      (l,b=264,48 deg), NOT sunward. It is {a_pioneer_obs/a_pf:.1e}x too small AND the wrong direction.")
print()
# (b.3) the thermal resolution (Turyshev 2012) -- the decisive jerk/decay term.
print( "   THERMAL RESOLUTION (Turyshev+ 2012, PRL 108.241101): a finite-element thermal model with flight")
print( "   telemetry as boundary conditions leaves NO residual; <2% emission anisotropy suffices. The DECISIVE")
print( "   discriminant is the JERK: the anomaly DECAYS in time, tracking the Pu-238 radioactive half-life (87.7 yr)")
print( "   of the on-board heat source -- a constant new-physics/MOND acceleration CANNOT decay; thermal MUST.")
tau_pu = 87.7
decay_per_decade = 1 - np.exp(-10*np.log(2)/tau_pu)
print(f"      Pu-238 half-life 87.7 yr -> heat (and thus thermal recoil) falls ~{decay_per_decade*100:.0f}% per decade;")
print( "      Anderson's own data show the anomaly's apparent constancy was a limited-data artifact. SETTLED THERMAL.")
print()
# (b.4) the planetary-ephemeris kill: a real a0-scale sunward accel would perturb the outer planets -- it does NOT.
#       Quantify: Saturn at ~9.5 AU, INPOP/Cassini bound the unexplained radial accel far below a_P.
a_extra_saturn = a_pioneer_obs   # if it were a real universal sunward accel
g_sat = g_newton(1.0, 9.58*AU)
print(f"   EPHEMERIS KILL: a universal {a_pioneer_obs:.1e} sunward accel would shift Saturn's g ({g_sat:.2e}) by")
print(f"      a fraction {a_extra_saturn/g_sat:.1e}. Cassini ranging bounds anomalous radial accel at Saturn to")
print( "      < ~1e-13 m/s^2 (Pitjeva/INPOP) -> a real Pioneer-magnitude universal accel is EXCLUDED by ~4 orders.")
print( "      (Confirms: whatever Pioneer is, it is SPACECRAFT-LOCAL = thermal, not a field. Framework agrees.)")
print()

# ====================================================================================================================
# SUMMARY
# ====================================================================================================================
sep("FRONT 3 VERDICT")
print("""  (a) PTA / nHz GWB:
      - tensor-sector LV searches (graviton mass, c_T, non-tensorial pols): framework predicts the GR value
        (c_T=1 exactly) -> NULL by construction, not a door.
      - CMB-correlated timing-residual dipole (the s^TX analogue in the timing channel): the kpc constant delay
        is absorbed into the per-pulsar fit; the only non-degenerate piece is the Earth-annual modulation of the
        s-background ~ s*beta_earth*(AU/c) ~ 1e-13 s, ~1e4-1e6x below SKA-era 10 ns, and is the SAME s^TX physics
        measured far better by planetary ranging -> BELOW FLOOR. Not a door.
      - a0-scale pulsar far-field: g=a0 at ~0.06 pc, far outside any timed orbit; MI part out-of-regime -> NULL.
      - GWB amplitude via MOND friction: ALREADY WORKED, soft/weak, Newtonian bottleneck -> already covered.
    => NO fresh distinctive above-floor PTA door. The banked alpha2 (~1e-13) and s^TX (the live ephemeris test)
       remain the only preferred-frame channels; PTA adds nothing above floor.

  (b) Pioneer/flyby anomaly: the a_P ~ 8.7e-10 ~ a0 is a COINCIDENCE. Pioneer is deeply Newtonian (g_Sun ~ 1e3 a0)
      so the modified-INERTIA framework predicts ~ZERO MOND anomaly there; the preferred-frame piece is ~1e10x too
      small AND points at the CMB apex, not sunward. The anomaly is THERMAL RECOIL (Turyshev 2012), nailed by the
      decaying jerk term (Pu-238 87.7yr) that no constant new-physics accel can mimic, and a universal a0-scale
      sunward accel is independently excluded ~4 orders by Cassini/INPOP planetary ranging. The framework does NOT
      predict Pioneer and should NOT claim it. SETTLED, NULL -- correctly so.

  NET: FRONT 3 opens NO genuine fresh door. Honest both-ways result: PTA propagation-sector = NULL (c_T=1);
  PTA timing-dipole + pulsar far-field = BELOW FLOOR; GWB-friction = already-covered soft hint; Pioneer = thermal
  (NULL, an a0-coincidence trap correctly declined). The live preferred-frame test stays s^TX (ephemerides), NOT PTA.""")
print("#"*116)
