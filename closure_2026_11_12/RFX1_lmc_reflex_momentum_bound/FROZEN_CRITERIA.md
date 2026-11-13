# RFX1 FROZEN CRITERIA: the LMC reflex against a momentum bound (no simulation)

2026-11-12. TEST lane. Adopts nothing. Written before any bound is computed and before any measured reflex value
is looked up beyond the one the lead quoted (Petersen and Penarrubia 2021, 32 +/- 4 km/s toward (56, -34)).
The baryonic mass inventories below were looked up before this freeze (allowed: they are inputs).

## 1. Question

Is the measured reflex (travel) velocity of the Milky Way's inner Galaxy relative to its outer halo (stars beyond
about 40 kpc) larger than the framework's light LMC can produce, by a bound that holds for any force law?

## 2. The bound

Two-body momentum conservation (inertial masses m_MW, m_L; mu = m_L / (m_MW + m_L)): in the pair's centre-of-mass
frame v_MW = -mu v_rel, v_rel = v_L - v_MW. If the distant halo has kept the Milky Way's velocity of the LMC's last
apocentre (the least responsive halo), the travel velocity is

  V_B = -mu [ v_rel(now) - v_rel(last apocentre) ],   B_first = |V_B|,   direction of V_B = the bound's apex.

A halo that follows partly, or that the LMC pulls directly, gives less, so the measured travel velocity must not
exceed B_first. Absolute ceiling, reported and used as a FRAGILE variant: B_abs = 2 mu v_peri (v_peri the relative
speed at the last pericentre).

Relative orbit, both readings: the force on the LMC is m_L g_MW(|d|) toward the Milky Way centre, the reaction on the
Milky Way is equal and opposite, so d'' = -(1 + m_L / m_MW) g_MW(|d|) d_hat. g_MW is the framework's field
g = nu(g_b / a0) g_b, nu(y) = 1 / (1 - exp(-sqrt(y))), g_b from the McMillan 2017 census (copied from
closure_2026_11_12/LMC1_lmc_pull_on_halo_stars/lmc1_core.py, which copies raw1_model.py). Footings canonical
(a0 9.36e-11) and alt (1.13e-10 m/s^2), never pooled.

Last apocentre: integrate the relative orbit back from today (kick-drift-kick leapfrog, step 0.1 Myr); pass the
first minimum of |d| (the last pericentre); the first maximum of |d| after it is the last apocentre. Cap 6 Gyr; if
no maximum is found by then, use the state at -6 Gyr and flag CAPPED in the output.

## 3. Readings (inertial masses), each graded on both footings

- R1 baryonic inertia (the kernel as a law of force; only baryons carry momentum).
  m_MW primary = the census baryons M_b(<200 kpc) from the copied module (expected 6.68e10; check within 1 %).
  m_L primary = LMC + SMC baryons as a bound pair: LMC 3.2e9 (stars 2.7e9 + HI 5e8 x 1.33 helium, the repository's
  hunt_2026/h37_lmc_bound.py line 40, as used by LMC1) + SMC 8.7e8 (stars 3.1e8 + neutral gas 5.6e8) = 4.07e9.
  Stated errors used in sigma_B: m_L +/- 25 per cent, m_MW +/- 10 per cent (assessed, not published errors).
  Variants (FRAGILE): (a) LMC alone 3.2e9; (b) plus all Magellanic Stream, Bridge and Leading Arm gas, neutral and
  ionised, 2.0e9 x 1.33 = 2.66e9 -> 6.73e9 (upper end; helium factor applied because the source does not say it is
  included); (c) m_MW with the rotation-curve stellar mass: 7.08e10 (canonical) / 6.42e10 (alt) + the census gas
  (M_b(200) - 5.49e10); (d) m_MW plus hot halo gas inside 50 kpc, 3.846e9 (Miller and Bregman 2015 model as
  computed by closure_2026_11_12/MWG1_hot_halo_gas, RESULT.md line 70). Reported only, no flip power: m_L with the
  Stream's neutral gas only (4.87e8 x 1.33 = 6.5e8 -> 4.72e9).
- R2 the cold dark energy moves with its galaxy and carries momentum.
  m_MW = the framework's dynamical mass inside r_c, g_MW(r_c) r_c^2 / G, primary r_c = 40 kpc; variants 30, 50, 80.
  m_L = LMC1's effective-mass bracket: primary 2.5e10, variants 1.6e10 and 4.0e10.
  sigma_B from the LMC speed error only; the mass bracket and r_c enter as FRAGILE variants (not double counted).

What the record says about which reading is the framework's (searched before this freeze; quotes, file and line):
- closure_2026_11_10/THEORY_ASSEMBLED_2026-11-10.md lines 15-17: "the halo is the charge itself: an isothermal halo
  with sigma^2 = (1/2) sqrt(G M_b a0), gravitating and lensing like mass."
- qwen_claude_field_theory/papers_2026/PAPER72_law_with_cold_dark_energy_counted_once_2026.tex line 195: "The halo is
  the charge itself and gravitates and lenses as mass."; line 88: "In form B a dwarf keeps the phantom of its own
  baryons inside a host, cut only by tides."
- closure_2026_11_10/MEDIUM_DESIGN_2026-11-10.md line 28: any local, momentum-conserving, normally self-gravitating
  medium whose equilibrium is the law is a NO-GO (M5, a theorem); lines 42-44: the remaining class is a medium "that
  exchanges momentum and heat with something else".
- closure_2026_11_09/BI1_switched_coupling_consistency/RESULT.md line 193: a switched coupling "breaks momentum
  conservation: halos self-propel galaxies".
Reading of the record: it says the halo gravitates and lenses like mass and is kept by its galaxy, but it nowhere
states the halo's inertial mass or whether it carries momentum with the galaxy; the M5 theorem forbids the simplest
momentum-conserving medium. The record does NOT decide between R1 and R2. That is a decision for the owner, not for
this lane. Both are graded; neither is adopted.

## 4. Inherited ingredients and their class

| ingredient | value | class |
|---|---|---|
| LMC position and velocity today (K13 proper motion 1.910, 0.229 mas/yr; distance 49.59 kpc; v_los 262.2; centre 78.76, -69.19; solar R0 8.122, z 20.8 pc, v (12.9, 245.6, 7.78)) | as built in lmc1.py lines 133-137 | raw measurement (PROVISIONAL, as in LMC1) |
| LMC speed error | 24 km/s (K13 as quoted by LMC1) | raw measurement |
| Milky Way baryon census (McMillan 2017) | 6.68e10; rc stellar 7.08e10 / 6.42e10 | raw-derived compilation (rc masses are the framework's own fit) |
| LMC baryons 3.2e9; SMC 3.1e8 + 5.6e8; Stream gas 2.0e9 (Fox 2014), neutral 4.87e8 (Bruns 2005) | see SOURCES.md | raw measurement (PROVISIONAL) |
| helium factor 1.33 | | standard physics (primordial helium), not cosmological-model-specific |
| hot halo gas inside 50 kpc 3.846e9 | MWG1 | a published model fitted to raw X-ray data (PROVISIONAL), variant only |
| kernel nu, a0 footings | | framework's own |
| LMC effective mass bracket 1.6e10 / 2.5e10 / 4e10 | LMC1 | framework's own (LMC1) |
| measured travel velocities | after the freeze | raw-derived fits (the published fits use standard-model halo models; flagged) |
| LMC 1.5e11, MW 1.0e12 / 1.3e12 | M3 only | BORROWED from the standard-model literature, CONTEXT ONLY, no label |

No standard-model or standard-MOND number enters a label.

## 5. Measurement and grading

Primary measurement: Petersen and Penarrubia 2021, travel velocity 32 +/- 4 km/s toward (l, b) = (56 +/- 9,
-34 +10/-9) deg, tracers 40 to 120 kpc (PROVISIONAL; confirmed after the freeze and recorded in SOURCES.md; if the
confirmed numbers differ from these, the confirmed numbers are used and the difference is reported).
After the freeze every other published reflex / travel velocity measurement found is graded as a variant row
(distance range, amplitude, error, direction).

z = (v_measured - B_first) / sqrt(sigma_measured^2 + sigma_B^2). For an asymmetric published error the larger side
is used. sigma_B: half the difference of B_first at speed x (1 +/- 24 / 320.1) (direction kept), and for R1 the
mass errors, propagated by recomputing B_first at m_L x (1 +/- 0.25) and m_MW x (1 +/- 0.10) (half differences),
all in quadrature.

## 6. Labels, per reading and footing

- REFLEX EXCEEDS THE BOUND: z >= 2 in the primary configuration.
- REFLEX WITHIN THE BOUND: z < 2 (only the absence of a contradiction; the bound is one-sided).
- FRAGILE appended if any listed variant flips the word: R1 variants (a)-(d), B_abs in place of B_first, any other
  published measurement as primary; R2 r_c 30 / 50 / 80, M_eff 1.6e10 / 4e10, B_abs, any other published
  measurement as primary. Every flipping variant is listed.
- NOT EVALUABLE if K3 fails for that reading and footing.
- NO LABEL for the whole lane if K1, K2 or K4 fails (the script stops before any label).

## 7. Known-answer checks (run first)

- K1 the LMC today: r_GC 49.08 +/- 0.01 kpc and speed 320.1 +/- 0.1 km/s (LMC1's values).
- K2 per reading and footing: a two-body integration in an inertial frame with that reading's masses (separate code
  path: two bodies with equal and opposite forces): total momentum constant to 1e-8 (relative to m_L |v_L|), and the
  Milky Way's velocity change from last apocentre to today equals V_B in size and direction to 1e-4 (relative);
  and 2000 force-free far tracers (r 200-400 kpc, isotropic, moving with the Milky Way's velocity at apocentre) give,
  by a least-squares dipole of their line-of-sight velocities relative to the Milky Way centre, the same travel
  velocity to 1e-4 relative.
- K3 direction: the bound's apex within 3 sigma of the published apex, chi = sqrt((dl / 9)^2 + (db / sigma_b)^2) <= 3
  (dl wrapped to [-180, 180], sigma_b = 10 if the bound's b is above -34, else 9). Fails -> NOT EVALUABLE.
- K4 the relative-orbit integrator conserves energy to 1e-6 in the static field (test-particle LMC, m_L = 0, 6 Gyr
  back, both footings).
- K5 (sample, for the reported own-stars item only): RAW1's bin counts 865 / 264 / 241 / 125. A failure stops only
  the own-stars item.

## 8. Mutations (separate output file)

- M1 three times the primary Magellanic baryon mass must flip R1 or move z by at least 2 (each footing).
- M2 the LMC's present velocity reversed: the bound's apex must move to the opposite side of the sky (more than 90
  deg from the unmutated apex) and K3 must fail (each reading and footing, primary).
- M3 BORROWED, CONTEXT ONLY, no label: m_L = 1.5e11, m_MW = 1.0e12 and 1.3e12 (orbit in the framework's field,
  canonical and alt). Expected B_first >= v_measured (z <= 0). If z >= 2 the bound's logic is too tight and that is
  stated prominently; if 0 < z < 2 it is stated.

## 9. Reported, no label

- mu_req = v_measured / |v_rel(now) - v_rel(apo)| and the Magellanic inertial mass R1 would need on each footing,
  beside the inventory.
- Own stars (DESI DR1 BHB, RAW1's sample and bins, sample building copied from lmc1.py): per bin, ML fit of
  v_gsr = m - T (u . n) + noise (dispersion free, star errors added), u the R1 canonical primary bound direction
  (and, reported, the published apex direction); T with its 1-sigma profile interval; a plain statement of power.

## 10. Known beforehand and own expectation

The lead's hand numbers (rough): the direction opposite to the LMC's present velocity is about 19 deg from the
published apex; R1 LMC alone 15 to 18 km/s; with the SMC 19 to 23; with all Magellanic gas 26 to 34; R2 16 to 37
across the bracket. My own expectation before computing: R1 primary mu about 0.057, |dv| 320 to 400 km/s, B_first
18 to 23, z about 1.5 to 2.5: on the threshold, FRAGILE on the gas budget either way; R2 primary B about 25 to 30,
REFLEX WITHIN THE BOUND, possibly FRAGILE at M_eff 1.6e10. Direction expected within K3.

## 11. Limits (stated beforehand)

A bound, not a prediction (least responsive halo). The published travel velocity is itself a fitted quantity. The
baryon inventories carry mass-to-light and distance assumptions. A two-body picture: no M31, no group, no external
field, no dynamical friction, no mass loss of the Clouds, the SMC moved with the LMC. Which inertia reading is the
framework's is undecided by the record.

Light job: one thread, nice -n 10, python3 -I -B; outputs carry no times.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
