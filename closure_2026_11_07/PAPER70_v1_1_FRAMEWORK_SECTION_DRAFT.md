# The one framework the record allows, and its four open gates (CONDITIONAL)

**NOT FOLDED: CK1 8e171a71a8 FAIL; see FRAMEWORK_CANDIDATE_2026_11_07.md post-result.**

Draft section for PAPER70 v1.1, written for the Field equations session. Fold it in **only if CK1-CK4 pass**. The
source is FRAMEWORK_CANDIDATE_2026_11_07.md (51cd404f0c), with RESOLUTION (ab75dae2e3) and DEDUCTION (same day).
Every number below is a literal from the committed file named beside it; `framework_section_check.py` checks each one,
and MUTATE must bite. This draft adopts nothing. CK1-CK4 have no frozen criteria and no result on origin/main at the
time of writing, so every gate they own reads OPEN. Kappa = 1/2 FITTED; not theory closed. Nothing here says the data
favour the framework.

## Postulates

- **P1. Law and action.** Gravity is GR plus a khronon carrying the v3s action in Legendre form, with the
  owner-adopted Pi^6 stiffness blend (b = rho_DE; OWNER_DECISION_2026-11-07_ADOPT_PI6_BLEND.md, 71e4014cd5). Its field
  equations are QX17's with Pi_+ -> F'(Pi) and 2F h_mn -> Pi F'(Pi) h_mn (QX17D, R2 CERTIFIED). The law is
  a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED. Footings are 9.3603e-11 / 1.1312e-10 m/s^2, never pooled. The
  static scope is the Solar System, isolated galaxies, galaxy lensing and GWs.
- **P2. A two-phase vacuum carrier.** The smooth phase is the dark energy rho_DE, which sets a0. The condensed phase is
  **cold dark energy**: cold, collisionless and gravitating, Newtonian in its own gravity, with the cosmic abundance
  the primary CMB requires. QX15 passes the footing background only with a cold component (L1 PASS 3741.08 /
  3741.15). The control, baryons-only plus the law, FAILS at +172,848 / +166,612. It is a phase of the vacuum sector,
  not a particle species.
- **P3. Release at virialisation.** When a well virialises, the condensed phase inside it converts to a free,
  collisionless phase with one fixed release speed v_k. The record's carrier ran at v_k 575-650 km/s (L388), and
  the top bin's X-COP need is met near 546 km/s by linear extrapolation, not a run (XR13). Whether the action
  supplies v_k is CK2. Until then P3 is the framework's one new postulate, and v_k is set by hand.

## Gates

| gate | the framework's reading | status | source |
|---|---|---|---|
| Solar System, PPN, c_T | law only; carrier cleared from the Galaxy | PASS | C6P, V3W, QX19 |
| Gaia DR4 wide binaries | v3s predicts Newton | kill test, waits on data | CQ2, PREDICTIONS_2026_11_07.md |
| SPARC exact field | law only; carrier cleared (progenitor v_esc 107-421 km/s, below every kick) | PASS | QX8; XR16 |
| ellipticals, KiDS colour split, bright M31 dSphs | systematics | EXPLAINED | SE2 |
| KiDS isolated lenses 100-300 kpc | law plus kSZ-measured gas, no bound carrier | label NO VERDICT; the bound-halo window is killed where it has power | KX1 |
| AGC 114905, Malin 1, FG1 canonical tilt | law only, unchanged | FAIL (not rescued) | QX4, QX11, QX14 |
| X-COP clusters | retained free phase | **OPEN (CK1)** | need from SE2 / ALL_GATES_NOGO; retention and profile from CK1's own framework-native run (L388 inadmissible, disclosure 1) |
| groups (20 Lovisari) | partial retention rising with mass | **OPEN (CK3)** | UA1; retention from CK1 (L388 inadmissible) |
| Coma UDGs | n/a | NOT A TEST (2 of 9 admissible) | UA1 |
| Bullet, Harvey mergers | collisionless free phase passes through | **OPEN (CK1)**; see disclosure 4 | L370 |
| primary CMB | cold parent | PASS with a cold component | QX15 |
| CMB-lensing shape, fsigma8, forest, early BHs | cold parent; daughters only where halos virialise | **OPEN (CK4)** | CE2 passed these for a fluid |
| release speed from the action | no knob | **OPEN (CK2)** | QX17D equations |
| a0(z) | flat to z 2.33 | kill test, waits on data | CFG689, AT2 |

The needed extra mass over the law, canonical / alt (ALL_GATES_NOGO_2026_11_06.md):

| class | needed extra mass |
|---|---|
| SPARC discs | <= 0.33 / 0.19 |
| X-COP clusters | ~4.2 / 3.8 |
| groups | 1.2-3.5 / 0.9-2.9 |
| dSph satellites | ~1.7 / 1.3 |
| Coma UDGs | ~80 |

The residue the law leaves (SE2 canonical medians, UA1 for the groups):
- X-COP +0.440 / +0.408;
- groups +0.259 / +0.221, NOT EXPLAINED.

## Why the four walls and CE2 / KX1 do not apply as stated

- **Wall 1 (cold fluid):** "Every well captures it, discs included (f_cap 4.1 vs <= 0.33)". Here the capture holds
  only until virialisation, when release clears galaxies, whose escape speeds sit below v_k.
- **Wall 2 (warm sea):** "Retention exp(depth/c_s^2) is too sharp". The free phase is not thermal with the host.
  Retention is set by one v_k against each well's escape speed. L388's bins rise 0.34 -> 0.50 -> 0.68 -> 0.85 at
  575 km/s.
- **Wall 3 (hot fermion):** this fails CMB lensing (chi^2 166-194). Here the parent is cold at recombination.
- **Wall 4 (shock entropy):** no shock heating is involved.
- **CE2:** a late-heated fluid FAILS X-COP (+0.324 / +0.287), the groups (0-1 of 20) and the Bullet (Mach 1.7-1.9,
  ram pressure strips the subcluster's sector). The free phase here is collisionless and bound below the cluster
  escape speed. CK1 must still show it.
- **KX1:** this excludes a bound puffed halo around galaxies. Here no carrier halo stays bound to a galaxy.

## Disclosures: what the cited sources actually support (read before folding)

1. **L388 carries ΛCDM inputs.**
   - Retention is eps = M_c,model / M_c,LCDM: carrier mass in a 1 Mpc/h sphere divided by the same quantity in a ΛCDM
     run.
   - The boxes start from a CLASS cosmology with "omega_cdm": 0.12 (L362, inherited via L366 -> L377 -> L379).
   - Under the standing raw-data / framework-native rule, CK1 must re-measure retention against a framework-native
     reference before any number here is graded.
2. **L388 used older footings and one footing.** A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; the simulations ran
   canonical only. Only the cosmic-shear gate was scored on both. Neither footing is today's.
3. **The bins are not X-COP's.**
   - Retention is measured inside 1 Mpc/h, not r500.
   - The top bin (2.5e14-1e17) holds n=7 halos.
   - The pooled ≥ 1e14 retention is 0.374-0.607.
   - XR13's own X-COP and group FAILs compare a "Without the phantom" requirement with retention measured "with the
     cluster phantoms on".
4. **The Bullet line is weaker than "beta_excess 0.000".**
   - The 0.000 comes from L370's MUTATE run (kernel off, nu = 1), which reduces to ΛCDM physics, and reads
     "-0.000 to -0.000".
   - The main L370 run gives intact "beta +0.001 to +0.072".
5. **The abundance ratio "5.4" is not a literal in the cited CMB lane.**
   - QX15 states no omega_d/omega_b; its canonical best fit is omega_b 0.02236, omega_d 0.1209.
   - QX12 states "R = omega_d/omega_b = 5.562".
6. **v_k is hand-set.**
   - L388 ran VK = (575.0, 600.0, 625.0, 650.0), and its output says "the trigger posited (no action)".
   - The owner's 09-26 rule (derive the kick, no knob scans) applies until CK2 lands.
7. **KX1's frozen label is NO VERDICT on both footings.** "Kill holds" is the reading under that label, not the
   label itself.

## Kill lines (frozen in FRAMEWORK_CANDIDATE section 4)

- **K1 (CK1):** the X-COP per-bin profile fails NA2's band ("between the gas and the stars") at every v_k in 500-650
  km/s, or no v_k passes G1-G9 together.
- **K2 (CK2):** the certified action releases no energy at the switch, or releases an energy per unit mass far from
  (5.5-6e5 m/s)^2. Then v_k is a knob.
- **K3 (CK3):** the 20 groups show no rise of f with mass, or the predicted slope is excluded.
- **K4 (CK4):** daughters at v_k break the PR4 lensing shape (chi^2 <= 18.5 at L <= 400), fsigma8, or the forest.
- **K5:** cluster weak lensing at 1-3 Mpc must exceed the hydrostatic mass inside r500 by the released fraction. This
  is owed as a prediction line.

## One paragraph

Gravity is the a0 law carried by the v3s action with the adopted Pi^6 blend. The vacuum has a smooth phase that sets
a0 and a cold condensed phase that the primary CMB requires. The condensed phase is released, at one fixed speed, as
a free collisionless phase when a well virialises. So galaxies shed it, groups keep part of it in proportion to their
depth, and clusters keep most of it. Every static test of the law stands. The framework is CONDITIONAL on four open
gates (CK1-CK4) and on one derivation, CK2, which decides whether the release speed belongs to the action or is a
postulate. By disclosures 1-7 the September carrier numbers carry no weight: L388 is inadmissible as KA or evidence, and the
candidate rests on CK1's own framework-native retention and profile (RESOLUTION / FRAMEWORK_CANDIDATE, same day). Kappa = 1/2 FITTED; not theory closed.
