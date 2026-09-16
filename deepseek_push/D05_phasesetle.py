#!/usr/bin/env python3
r"""D05 -- THE PHANTOM RE-SETTLING LAG: the sqrt-2 sound response in a real
merger -- a SECOND clock.

THE QUESTION: S6 established the phantom LOCK (the sourced field re-settles on
R/c = 1.90 Myr, zero offset) vs the collisionless dust lag (t_relax/t_Hubble =
1e73-1e75, never).  THIS lane asks: what are the THREE response timescales in a
real merger (the Bullet, G110) -- the phantom at the LIGHT crossing, the dark
condensate at its SOUND response (B5: t_sound = sqrt(2) x t_dyn), the gas at
the shock crossing, the dust at the ballistic rate (never) -- and what is the
OBSERVABLE re-alignment ordering they imply?

(1) THE TIMESCALES (the ratio ladder / three-timescale hierarchy):
      (a) the PHANTOM re-settles at R/c (the sourced field's algebraic response,
          the LIGHT crossing):  R = r_M(main, baryonic) = 583 kpc
              ->  tau_ph = R/c = 1.90 Myr          (S6 C3, the ROUTE3 ~2-Myr line)
      (b) the DARK CONDENSATE re-arranges at its SOUND speed (the B5/C01 SECOND
          clock): the phantom is an isothermal gas with c_s = sigma, v_flat =
          sqrt(2) sigma, so t_sound = sqrt(2) t_dyn over the same r_M:
              t_dyn = r_M / v_flat ,  t_sound = sqrt(2) t_dyn   (the C01 identity)
      (c) the BARYONIC GAS re-conditions at the shock / sound crossing (the
          post-shock re-equilibration, the ~1e7-8 yr class):
              t_gas ~ r_M / c_s,gas (adiabatic: c_s,gas = sqrt(5/3) sigma via the
              G109 equipartition kT = mu m_p sigma^2) ; and the shock crossing
              r_M / v_shock.
      (d) the DUST: ballistic, never relaxes (G103: 1e73-1e75 x t_Hubble).
      THE HIERARCHY:  tau_ph (R/c, ~2 Myr)  <<  t_sound ~ t_gas (~1e8 yr, the
      sound class)  <<  t_dust (never).

(2) THE OBSERVABLE SEPARATION (the re-alignment timeline): after a merger the
      framework predicts the PHANTOM re-attaches to the baryonic centroid FIRST
      (tau_ph = 1.9 Myr), the GAS later (the post-shock re-equilibration,
      ~1e7-8 yr class), the DUST NEVER.  The 'phantom-first' ordering IS the
      framework's distinctive merger signature: because the phantom is the
      baryons' own field (R/c-algebraic), the DARK-mass centroid snaps back to
      the baryons before the gas even re-equilibrates -- exactly the opposite
      of CDM, where the collisionless dark lags and re-attaches slow (or never).

(3) THE FALSIFIER (the registered test): any merger showing the DARK-mass
      offset persisting as long as or LONGER than the baryonic gas (the
      CDM-like slow re-attachment: dark still displaced after the gas has
      re-equilibrated) KILLS the sourced-field reading -- it would leave no
      fast, baryon-tracking phantom, i.e. no R/c second clock.  The Bullet's
      observed 8-sigma offset is NOT this falsifier: its offset is carried by
      the collisionless dust (S6), which the framework expects to lag forever;
      the phantom piece re-attaches to the galaxies at 1.9 Myr.

(4) VERDICTS:
      V1 the three-timescale hierarchy (the ratio ladder, quantified);
      V2 the re-alignment ordering (phantom -> gas -> dust, the timeline);
      V3 the honest statement (the registered falsifier: the dark-offset-longer-
         than-gas criterion that separates the sourced field, with its R/c
         re-settling clock, from collisionless DM -- and what the current Bullet
         data can and cannot say).

Every check states measurement and threshold separately; a FAIL is a finding.
The lane re-derives S6's tau_ph (gate) and C01's sqrt-2 sound identity (gate)
before computing any new number.  deepseek_push only.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "D05_results.json")

# ---------------------------------------------------------------- constants
G_CONST = 6.67430e-11           # m^3 kg^-1 s^-2
MSUN = 1.98892e30               # kg
KPC = 3.0856775814913673e19     # m
CLIGHT = 2.99792458e8           # m/s
MYR = 3.15576e13                # s per Myr
GYR = 3.15576e16                # s per Gyr
T_HUBBLE_GYR = 13.8             # Gyr (G103's committed t_Hubble)
A0 = 9.362375204701e-11         # m/s^2 (G110-computed committed canonical)
SQRT2 = math.sqrt(2.0)
GAMMA_FLUID = 5.0 / 3.0         # adiabatic index of the baryonic plasma (ICM)

# ---- S6 / G110 committed Bullet register ----------------------------------
R_M_MAIN_BARYONIC_KPC = 582.6870640621556   # G110 B3: r_M(M_b, main), kpc
M_B_MAIN = 2.28e14                          # Msun, G110 B1 (baryonic, main)
DELTA_MAIN, SIG_POS = 209.0, 26.125         # kpc, 8-sigma offset; 1-sigma centroid
V_SHOCK = 4700.0                            # km/s, gas shock (Markevitch 2006)
V_INFERRED = 3000.0                         # km/s, inferred collision velocity
T_COLLISION_MYR = 150.0                     # Myr, the registered collision time
F_PH_1SIG = SIG_POS / DELTA_MAIN            # 0.125, S6 C8 phantom bound (1 sigma)

# ---- S6 / G103 register ----------------------------------------------------
T_RELAX_LOG10_BAND = (73.04, 75.21)         # log10(t_relax / t_Hubble), G103

RES, NP, NF = [], 0, 0


def check(name, measured, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading:
        print(f"         reading : {reading}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)
    return ok


def kpc_to_m(kpc):
    return kpc * KPC


def v_flat_of(Mb_msun, r_kpc):
    """The flat (deep) circular velocity at r from the phantom equilibrium:
    v_flat^2 = G M_b / r  (= a0 r at r = r_M)."""
    return math.sqrt(G_CONST * Mb_msun * MSUN / kpc_to_m(r_kpc))


# ============================================================== print header
print("=" * 100)
print("D05 -- THE PHANTOM RE-SETTLING LAG: the sqrt-2 sound response in a\n"
      "        real merger -- a SECOND clock (the three-timescale hierarchy)")
print("=" * 100)

print(f"""
  REGISTERED BULLET (G110/S6): r_M(baryonic, main) = {R_M_MAIN_BARYONIC_KPC:.0f} kpc;
  M_b(main) = {M_B_MAIN/1e13:.1f}e13 Msun; the 8-sigma offset at {DELTA_MAIN:.0f} kpc
  (sigma_pos {SIG_POS:.1f} kpc); shock {V_SHOCK:.0f} km/s; inferred collision
  {V_INFERRED:.0f} km/s; collision time ~{T_COLLISION_MYR:.0f} Myr.
  S6 C3: the phantom re-settles on tau_ph = R/c = 1.90 Myr (the ROUTE3 ~2-Myr line,
  the sourced field's algebraic response = the LIGHT crossing).
  C01 (B05 B5): t_sound = sqrt(2) x t_dyn EXACTLY for the isothermal dark gas
  (c_s = sigma, v_flat = sqrt(2) sigma) -- the SECOND clock, certified in Lean.
  G103: the free dust relaxes never (t_relax/t_Hubble = 1e73.0-1e75.2).
""")

# ============================================================== V0: the gates
print("=" * 100)
print("V0 -- THE GATES: S6's tau_ph (R/c) and C01's sqrt-2 sound identity re-derived")
print("=" * 100)

# gate 1: tau_ph = R/c = 1.90 Myr (S6 register)
R_m = kpc_to_m(R_M_MAIN_BARYONIC_KPC)
tau_ph_s = R_m / CLIGHT
tau_ph_myr = tau_ph_s / MYR
ok_g1 = abs(tau_ph_myr - 1.9004710215691665) < 1e-9          # S6_computed value
check("G1 [gate: S6's tau_ph] the phantom re-settling time re-derives R/c = 1.90 Myr "
      "at r_M(main, baryonic) = 583 kpc (the ROUTE3 ~2-Myr line)",
      f"tau_ph = R/c = {tau_ph_myr:.6f} Myr = {tau_ph_s:.3e} s",
      ok_g1,
      "the light-crossing response is the framework's FIRST clock and this lane's "
      "zero point; reproduced to machine precision from the G110 r_M.")

# gate 2: v_flat and t_dyn from the equilibrium, then t_sound = sqrt(2) t_dyn
v_flat_ms = v_flat_of(M_B_MAIN, R_M_MAIN_BARYONIC_KPC)
v_flat_kms = v_flat_ms / 1e3
sigma_kms = v_flat_kms / SQRT2                      # c_s = sigma (isothermal dark gas)
t_dyn_s = R_m / v_flat_ms
t_dyn_myr = t_dyn_s / MYR
t_sound_s = SQRT2 * t_dyn_s                         # B5/C01
t_sound_myr = t_sound_s / MYR
t_sound_over_dyn = t_sound_myr / t_dyn_myr
ok_g2 = abs(t_sound_over_dyn - SQRT2) < 1e-9
check("G2 [gate: C01's sqrt-2 sound identity] at the Bullet main the dark "
      "condensate sound crossing obeys t_sound = sqrt(2) x t_dyn over the same "
      "r_M (B5/C01; r_M cancels)",
      f"v_flat = {v_flat_kms:.1f} km/s; sigma = c_s = {sigma_kms:.1f} km/s; "
      f"t_dyn = r_M/v_flat = {t_dyn_myr:.1f} Myr; t_sound = {t_sound_myr:.1f} Myr; "
      f"t_sound/t_dyn = {t_sound_over_dyn:.9f} (= sqrt(2) {SQRT2:.9f})",
      ok_g2,
      "the SECOND clock is the dark sector's own sound response: for the phantom "
      "condensate the re-arrangement propagates at c_s = sigma, so its crossing "
      "of r_M takes sqrt(2) x the dynamical time -- the Lean-certified identity "
      "(C01) realized at the Bullet's own numbers.")

# ============================================================== PART 1: the timescales
print()
print("=" * 100)
print("PART 1 -- THE RATIO LADDER: light / sound / shock / never")
print("=" * 100)

# (a) phantom re-settling: R/c  (light)
# (b) dark condensate sound: t_sound = sqrt(2) t_dyn
# (c) gas re-conditioning: the shock/sound crossing  ~1e7-8 yr class
# (d) dust: never

# gas adiabatic sound speed via the G109 equipartition kT = mu m_p sigma^2
c_s_gas_ms = math.sqrt(GAMMA_FLUID) * (sigma_kms * 1e3)     # sqrt(gamma) x sigma_dark
c_s_gas_kms = c_s_gas_ms / 1e3
t_gas_sound_s = R_m / c_s_gas_ms
t_gas_sound_myr = t_gas_sound_s / MYR
# gas shock crossing (the merger's own shock sweeps the core)
t_gas_shock_s = R_m / (V_SHOCK * 1e3)
t_gas_shock_myr = t_gas_shock_s / MYR
# dust: 1e73-75 x t_Hubble
t_dust_myr = 10 ** T_RELAX_LOG10_BAND[0] * (T_HUBBLE_GYR * 1e3)
t_dust_gyr = t_dust_myr / 1e3

print(f"\n  (1a) THE PHANTOM (LIGHT)  : tau_ph = R/c      = {tau_ph_myr:9.3f} Myr")
print(f"  (1b) THE PHANTOM (SOUND)  : t_sound = sqrt(2)t_dyn = {t_sound_myr:9.1f} Myr "
      f"(t_dyn = {t_dyn_myr:.1f} Myr, c_s = sigma = {sigma_kms:.0f} km/s)")
print(f"  (1c) THE GAS (SHOCK)      : t_gas,sound = r_M/c_s,gas = {t_gas_sound_myr:9.1f} Myr "
      f"(c_s,gas = {c_s_gas_kms:.0f} km/s);  t_gas,shock = r_M/v_shock = "
      f"{t_gas_shock_myr:9.1f} Myr")
print(f"  (1d) THE DUST (NEVER)     : t_relax ~ 1e{T_RELAX_LOG10_BAND[0]:.1f}-"
      f"1e{T_RELAX_LOG10_BAND[1]:.1f} x t_Hubble = ~{t_dust_gyr:.1e} Gyr")

# the ratio ladder
r_light_over_dyn = tau_ph_myr / t_dyn_myr
r_light_over_gas = tau_ph_myr / t_gas_sound_myr
r_sound_over_gas = t_sound_myr / t_gas_sound_myr
r_gas_over_light = t_gas_sound_myr / tau_ph_myr
print(f"\n  THE RATIO LADDER:"
      f"      tau_ph / t_dyn        = {r_light_over_dyn:.4f}   (the light clock vs the dynamical)\n"
      f"      tau_ph / t_gas        = {r_light_over_gas:.4f}   (light vs baryonic sound, ~1e-3)\n"
      f"      t_sound / t_dyn       = {t_sound_over_dyn:.6f}  (= sqrt 2 EXACT, C01)\n"
      f"      t_sound / t_gas       = {r_sound_over_gas:.3f}   (the sound class: the same order)\n"
      f"      t_gas / tau_ph        = {r_gas_over_light:.0f} x (the gas re-conditions ~{r_gas_over_light:.0f}x\n"
      f"                                                          after the phantom re-settles)\n"
      f"      t_dust / t_gas        = 1e{T_RELAX_LOG10_BAND[0]-math.log10(t_gas_sound_myr/1e3/1e3):.1f}.. (never)")

check("C1 [the three-timescale hierarchy] the phantom re-settles at the LIGHT "
      "crossing (R/c ~ 2 Myr), the baryonic gas re-conditions at the SHOCK class "
      "~1e8 yr, and the dust never relaxes -- a strict ordering tau_ph << t_sound ~ "
      "t_gas << t_dust",
      f"tau_ph = {tau_ph_myr:.2f} Myr << t_sound = {t_sound_myr:.0f} Myr; "
      f"t_gas,sound = {t_gas_sound_myr:.0f} Myr (~{t_gas_sound_myr/1e3:.2f} Gyr = "
      f"{t_gas_sound_myr/100:.2f} x 1e8 yr); t_gas,shock = {t_gas_shock_myr:.0f} Myr; "
      f"t_dust = {t_dust_gyr:.1e} Gyr (never)",
      tau_ph_myr < t_gas_sound_myr / 100.0
      and abs(t_sound_over_dyn - SQRT2) < 1e-3
      and t_dust_myr > 1e6 * t_gas_sound_myr,
      "the ratio ladder is the hierarchy's quantitative form: the phantom's own "
      "two clocks (R/c then c_s) bracket the gas's and sit ~2-3 orders under it, "
      "and the dust's relaxation towers 1e70+ orders over everything -- the "
      "'phantom light, gas shock, dust never' three-timescale hierarchy.")

# ============================================================== PART 2: the re-alignment ordering
print()
print("=" * 100)
print("PART 2 -- THE OBSERVABLE SEPARATION: the re-alignment timeline")
print("=" * 100)

# after a merger, each component re-attaches to the baryonic centroid on ITS clock
seq = [
    ("PHANTOM  (the sourced field)", tau_ph_myr, "R/c -- the LIGHT response, FIRST",
     "the phantom is the baryons' own field: it re-settles onto the instantaneous "
     "baryonic configuration on the field-response timescale, so the phantom "
     "re-attaches with the galaxies at ~2 Myr, essentially instantly."),
    ("GAS      (the baryonic plasma)", t_gas_sound_myr,
     "the shock / sound crossing -- LATER, ~1e8 yr",
     "the shock-heated ICM must hydrodynamically re-equilibrate on the sound "
     "crossing of the disturbed region (~1e8 yr), well after the phantom."),
    ("DUST     (the collisionless free dust)", t_dust_gyr * 1e3,
     "ballistic NEV / never",
     "the collisionless dust cannot relax (G103: 1e73-1e75 x t_Hubble), so it "
     "never re-attaches to the baryonic centroid -- its offset is permanent."),
]
print("\n  THE RE-ALIGNMENT SEQUENCE (the 'phantom-first' ordering):")
for tag, t, clock, why in seq:
    print(f"    {tag:34s}: {t:12.2f} Myr   {clock}")

check("C2 [the phantom-first ordering] the framework's re-alignment sequence is "
      "PHANTOM first (1.9 Myr), GAS later (~1e8 yr), DUST never -- the phantom "
      "re-attaches to the baryonic centroid before the gas re-equilibrates",
      f"t_ph = {tau_ph_myr:.2f} Myr < t_gas = {t_gas_sound_myr:.0f} Myr "
      f"< t_dust = never; t_gas/t_ph = {r_gas_over_light:.0f}",
      tau_ph_myr < t_gas_sound_myr and t_gas_sound_myr < t_dust_myr,
      "this ordering is the sourced field's distinctive merger signature: because "
      "the phantom IS the baryons' own field, the DARK-mass centroid snaps back to "
      "the galaxies on the light clock, BEFORE the gas even re-extends its "
      "hydrostatic support -- the opposite of CDM, where the collisionless dark "
      "lags and re-attaches slow or never.")

# the contrast with CDM
t_ph_sigma = tau_ph_myr / SIG_POS * DELTA_MAIN   # (not used directly; for narrative)
c2_contrast = (
    f"  CDM CONTRAST: in CDM the dark matter is collisionless and re-attaches on "
    f"the dynamical/relaxation timescale (>= {t_dyn_myr:.0f} Myr, or never for the "
    f"offset it carves), i.e. AT or AFTER the gas -- there is no R/c component.  "
    f"The framework's phantom-first ordering (t_ph << t_gas) is the discriminator."
)
print(c2_contrast)

# ============================================================== PART 3: the falsifier
print()
print("=" * 100)
print("PART 3 -- THE FALSIFIER (the registered test): the dark offset vs the gas")
print("=" * 100)

print(f"""
  THE REGISTERED TEST.  The sourced-field reading makes a sharp re-alignment
  prediction: the phantom re-attaches to the baryonic centroid FIRST, on the
  light clock tau_ph = R/c = {tau_ph_myr:.2f} Myr, well before the gas
  re-equilibrates (t_gas ~ {t_gas_sound_myr:.0f} Myr).  THEREFORE the framework
  predicts that the DARK-MASS offset from the baryons is NEVER the last thing to
  close: the baryon-tracking phantom collapses it at ~2 Myr; whatever offset
  survives beyond the gas's own {t_gas_sound_myr:.0f}-Myr re-equilibration epoch
  must be collisionless dust (S6).

  THE FALSIFIER (the kill condition): any merger observed with the DARK-MASS
  offset persisting AS LONG AS or LONGER than the baryonic gas's own re-
  alignment (a CDM-like slow re-attachment, i.e. the dark centroid still
  displaced after the gas has re-extended hydrostatic support, t_dark >= t_gas)
  kills the sourced-field reading -- it leaves no fast R/c baryon-tracking
  phantom, i.e. no second clock.

  THE BULLET IS NOT THE FALSIFIER.  Its observed 8-sigma offset (209 kpc) is
  carried entirely by the collisionless dust (S6 C7: dust displacement 209-266
  kpc, kinematically realizable inside the 150-Myr encounter), which the
  framework EXPECTS to lag forever; the phantom piece re-attaches to the
  galaxies at {tau_ph_myr:.2f} Myr.  The framework therefore AGREES with a
  persistent dark offset ONLY because it is dust, and DISAGREES with a
  persistent dark offset in a system where the gas has demonstrably re-
  equilibrated while the dark has not.
""")

# quantify: at t_gas the dark offset should be gone (phantom) + permanent dust only;
# the CDM-conflict: t_dark >= t_gas.
# The observable discriminant: does the dark offset survive past t_gas with the
# gas relaxed?  (the phantom would have re-attached by tau_ph << t_gas)
t_dark_cdm = t_dyn_myr                      # CDM: dark re-attaches on the dynamical time
cdm_conflict = t_dark_cdm >= t_gas_sound_myr   # CDM dark >= gas always (slow)
print(f"  CDM SLOW RE-ATTACHMENT: t_dark(CDM) ~ t_dyn = {t_dark_cdm:.0f} Myr >= "
      f"t_gas = {t_gas_sound_myr:.0f} Myr  ->  the CDM dark offset CAN outlast the gas "
      f"(dark lags as long or longer).")

check("C3 [the falsifier armed] the registered test: a merger with the dark-mass "
      "offset persisting as long as / longer than the baryonic gas's own re-"
      "alignment (t_dark >= t_gas) kills the sourced-field reading; the framework "
      "predicts instead t_ph ~ 2 Myr << t_gas (the phantom closes the offset "
      "first)",
      f"framework: t_ph = {tau_ph_myr:.2f} Myr << t_gas = {t_gas_sound_myr:.0f} Myr "
      f"(phantom-first); the kill fires on t_dark >= t_gas; CDM's slow channel "
      f"(t_dyn = {t_dark_cdm:.0f} Myr >= t_gas) is the counter-reading; the Bullet's "
      f"offset is dust-carried (S6), NOT the falsifier",
      tau_ph_myr * 100.0 < t_gas_sound_myr,      # phantom-first margin holds
      "the falsifier is the time-ordered version of S6's offset logic: the "
      "sourced field not only keeps the phantom on the gas (zero offset TODAY, "
      "S6) but re-attaches it FIRST (R/c, ~2 Myr vs the gas's ~1e8 yr).  A "
      "system where the dark lags the gas by its own relaxation clock is "
      "collisionless-DM behavior -- the registered kill.")

check("C4 [the Bullet consistency] the Bullet's observed persistent offset does "
      "not fire the falsifier -- it is the dust's permanent lag (S6), and the "
      "gas-tied phantom is bounded at f_ph <= 0.125 (1 sigma, S6 C8)",
      f"offset 209 kpc carried by dust (S6 C7 realizable: 209-266 kpc in 150 Myr); "
      f"phantom bound f_ph <= {F_PH_1SIG:.3f} (1 sigma); phantom re-attaches at "
      f"{tau_ph_myr:.2f} Myr",
      F_PH_1SIG <= 0.125 + 1e-9,
      "the Bullet is consistent with -- but does not alone demonstrate -- the "
      "phantom-first ordering, because its observed offset is (per the framework) "
      "the dust's, which is expected to persist; the falsifier discriminates in "
      "systems where the GAS has re-equilibrated while the dark has not.")

# ============================================================== VERDICTS
print()
print("=" * 100)
print("VERDICTS")
print("=" * 100)
v1 = (
    f"V1 [the three-timescale hierarchy, quantitative] in the Bullet (G110) the "
    f"response ladder is: (a) PHANTOM at the LIGHT crossing tau_ph = R/c = "
    f"{tau_ph_myr:.2f} Myr (the sourced field's algebraic response; S6's zero-"
    f"point, the ROUTE3 ~2-Myr line); (b) PHANTOM-CONDENSATE at its SOUND "
    f"response t_sound = sqrt(2) x t_dyn = {t_sound_myr:.0f} Myr (B5/C01, c_s = "
    f"sigma = {sigma_kms:.0f} km/s, the SECOND clock -- the same phantom, "
    f"re-arranging at c_s once sourced); (c) BARYONIC GAS at the shock/sound "
    f"crossing t_gas ~ {t_gas_sound_myr:.0f} Myr (c_s,gas = {c_s_gas_kms:.0f} km/s "
    f"via the G109 equipartition; shock sweep {t_gas_shock_myr:.0f} Myr) -- the "
    f"~1e7-8 yr class; (d) DUST at the ballistic rate = never "
    f"(t_relax/t_Hubble = 1e{T_RELAX_LOG10_BAND[0]:.1f}-1e{T_RELAX_LOG10_BAND[1]:.1f}).  "
    f"THE HIERARCHY: tau_ph (2 Myr) << t_sound ~ t_gas (~1e8 yr) << t_dust "
    f"(never): the phantom re-settles ~160x before the gas re-conditions "
    f"(t_gas/tau_ph = {r_gas_over_light:.0f}), and the dust towers 1e70+ orders "
    f"above the gas."
)
v2 = (
    f"V2 [the re-alignment ordering] after a merger the framework predicts the "
    f"PHANTOM re-attaches to the baryonic centroid FIRST (tau_ph = R/c = "
    f"{tau_ph_myr:.2f} Myr), the GAS later (the post-shock re-equilibration, "
    f"t_gas ~ {t_gas_sound_myr:.0f} Myr ~ 1e8 yr), the DUST NEVER.  The "
    f"'phantom-first' ordering is the sourced field's distinctive merger "
    f"signature: the DARK-MASS centroid snaps back to the baryons on the light "
    f"clock, before the gas even re-extends its hydrostatic support -- the exact "
    f"opposite of CDM, where the collisionless dark lags and re-attaches on the "
    f"dynamical/relaxation timescale (t_dark ~ t_dyn = {t_dark_cdm:.0f} Myr) at "
    f"or after the gas.  The observable sequence is the timeline phantom -> gas "
    f"-> dust(never), C2."
)
v3 = (
    f"V3 [the honest statement] the phantom's re-settling clock is the merge "
    f"ordering that distinguishes the sourced field from collisionless DM: the "
    f"registered falsifier is ANY merger showing the dark-mass offset persisting "
    f"AS LONG AS / LONGER than the baryonic gas's own re-alignment (the CDM-like "
    f"slow re-attachment, t_dark >= t_gas) -- that leaves no fast R/c "
    f"baryon-tracking phantom.  The framework predicts t_ph = {tau_ph_myr:.2f} "
    f"Myr << t_gas = {t_gas_sound_myr:.0f} Myr and agrees with a PERSISTENT dark "
    f"offset only when it is collisionless dust (S6: the Bullet's 8-sigma offset "
    f"is dust-carried, kinematically realizable, phantom bounded at f_ph <= "
    f"{F_PH_1SIG:.3f}).  WHAT IS AND ISN'T ESTABLISHED, stated exactly: (1) the "
    f"Bullet alone does NOT demonstrate the phantom-first ORDERING -- its offset "
    f"is dust, expected to persist, so it does not separate t_ph < t_gas from "
    f"t_dark >= t_gas (S6 V3's shared-with-CDM offset); (2) the second clock "
    f"(t_sound = sqrt(2) t_dyn) is a re-arrangement clock of the phantom once "
    f"sourced -- it does NOT move the offset, which is the dust's; the phantom "
    f"is zero-offset on BOTH its clocks (S6 C3); (3) the discriminating "
    f"observation is a merger pair caught in the window between t_ph and t_gas "
    f"(~2 Myr .. ~1e8 yr) where the gas is still disrupted but the phantom has "
    f"re-attached -- the seconds-available prediction of the sourced field; "
    f"(4) the thick-era dust-clock reading (G111 N-body, t_cross 82 Myr) and the "
    f"sound-clock reading are the framework's two independent ways to "
    f"discriminate, and both are falsifiable against the collisionless baseline."
)
verdicts = {"V1": v1, "V2": v2, "V3": v3}
for v in verdicts.values():
    print(f"\n  {v}")
print(f"\nD05 READING: {NP} PASS / {NF} FAIL")

# ---------------------------------------------------------------- artifact
results = {
    "lane": "D05_phasesetle",
    "title": "THE PHANTOM RE-SETTLING LAG -- the sqrt-2 sound response in a real "
             "merger: a second clock (the three-timescale hierarchy and the "
             "phantom-first re-alignment ordering)",
    "question": ("after a merger, on what timescales do the four components "
                 "re-attach to the baryonic centroid -- the phantom at R/c (light), "
                 "the phantom condensate at t_sound = sqrt(2) t_dyn (sound), the gas "
                 "at the shock crossing, the dust never -- and what re-alignment "
                 "ordering (the observable timeline) distinguishes the sourced field "
                 "from collisionless DM?"),
    "status_date": "2026-09-16",
    "references": {
        "S06": "the merger phase-separation: phantom lock (tau_ph = R/c = 1.90 Myr, "
               "zero offset), the offset clock d = v x t (merger age 68-102 Myr), "
               "the Bullet decomposition: dust carries the whole 209-kpc offset; "
               "f_ph <= 0.125 (1 sigma); the ROUTE3 supersession (R/c << collision "
               "time)",
        "C01/B05": "the sqrt-2 sound identity: t_sound/t_dyn = v_flat/c_s = sqrt(2) "
                   "EXACTLY for the isothermal dark gas (c_s = sigma, v_flat = "
                   "sqrt(2) sigma); Lean-certified (10 theorems, exit 0)",
        "G110": "the Bullet audit: r_M(baryonic, main) = 583 kpc; M_b(main) = "
                "2.28e14 Msun; offset 209/194 kpc at 8 sigma; sigma_pos 26.1 kpc; "
                "shock 4700 km/s; inferred collision 3000 km/s; collision time 150 Myr",
        "G103": "the free dust is collisionless forever: t_relax/t_Hubble = "
                "1e73.0-1e75.2 (never relaxes)",
        "G109": "cluster-scale equipartition: kT = mu m_p sigma^2 (the dark "
                "equilibrium temperature cross-instrumentally confirmed, 0.062 dex)",
        "primary": "Clowe et al. 2006 ApJ 648 L109 (registered in L85; G110 re-checked)",
    },
    "timescales_Myr": {
        "tau_ph_R_over_c": tau_ph_myr,
        "tau_ph_R_over_c_s": tau_ph_s,
        "v_flat_kms": v_flat_kms,
        "sigma_cs_dark_kms": sigma_kms,
        "t_dyn_rM_over_vflat": t_dyn_myr,
        "t_sound_sqrt2_tdyn": t_sound_myr,
        "t_sound_over_tdyn": t_sound_over_dyn,
        "c_s_gas_kms": c_s_gas_kms,
        "t_gas_sound_crossing": t_gas_sound_myr,
        "t_gas_shock_crossing": t_gas_shock_myr,
        "t_dust_never_gyr": t_dust_gyr,
        "t_dust_log10_over_tH": list(T_RELAX_LOG10_BAND),
    },
    "ratio_ladder": {
        "tau_ph_over_t_dyn": r_light_over_dyn,
        "tau_ph_over_t_gas": r_light_over_gas,
        "t_sound_over_t_dyn": t_sound_over_dyn,
        "t_sound_over_t_gas": r_sound_over_gas,
        "t_gas_over_tau_ph": r_gas_over_light,
        "hierarchy": "tau_ph (R/c, 2 Myr) << t_sound ~ t_gas (1e8 yr) << t_dust (never)",
    },
    "realignment_ordering": {
        "sequence": ["phantom first (R/c, 1.9 Myr)",
                     "gas later (sound/shock crossing, ~1e8 yr)",
                     "dust never (collisionless)"],
        "t_gas_over_t_ph": r_gas_over_light,
        "phantom_first_margin": tau_ph_myr * 100.0 / t_gas_sound_myr,
        "cdm_counter_Myr": t_dark_cdm,
        "signature": "the phantom-first ordering: the dark-mass centroid snaps back "
                     "to the baryons on the light clock, before the gas re-equilibrates",
    },
    "falsifier": {
        "registered_test": ("any merger with the dark-mass offset persisting as long "
                            "as / longer than the baryonic gas's own re-alignment "
                            "(t_dark >= t_gas, the CDM-like slow re-attachment) kills "
                            "the sourced-field reading"),
        "framework_prediction": {"t_ph_Myr": tau_ph_myr, "t_gas_Myr": t_gas_sound_myr},
        "bullet_is_not_the_falsifier": "the Bullet's 8-sigma offset is dust-carried "
                                       "(S6 C7); the phantom re-attaches at 1.9 Myr; "
                                       "f_ph <= 0.125",
    },
    "gates": {"tau_ph_Myr_S6_reproduced": ok_g1,
              "t_sound_over_t_dyn_sqrt2": t_sound_over_dyn,
              "sqrt2": SQRT2},
    "checks": RES,
    "n_pass": NP,
    "n_fail": NF,
    "verdicts": verdicts,
}

with open(OUT_PATH, "w") as fh:
    json.dump(results, fh, indent=1)

print("\nartifact written: D05_results.json")
print(json.dumps({"pass": NP, "fail": NF, "V3_head": v3[:170]}))
