# P-wave brief (conductor tick 2026-09-23, spawned as background python3 lanes)

delegate_task is not available in this session; lanes spawn as background
python3 processes (the loop's own lane-counting convention). House rules
1-10 of LOOP_CONDUCTOR.md bind every lane. No git commits by lanes.

## O04b — three-channel joint deep a0_eff (door: O04 "next-lane arithmetic")
Goal: inverse-variance joint of the three LANDED deep-a0_eff channels, all
values read from lane files at runtime (no hardcoded physics):
  SPARC-deep: N05_results.json (a0eff_a0 0.72412..., z -4.17; SE derived as
  se_clustered/|Delta|*fraction... = se/(a0*E_gbar), cross-checked vs the
  0.0662 quoted in O03_results.json cross-block),
  G114 dwarfs: O01_results.json (0.6376 +/- 0.1625, z -1.77),
  Milky Way: O03_results.json deepest_probes/primary_R22 (0.7968 +/- 0.2362).
Kill conditions (pre-registered BEFORE the run):
  K1 chi2 heterogeneity df=2: chi2 > 5.991 -> channels HETEROGENEOUS; the
     joint is flagged, never banked as a single law (still reported).
  K2 MIGHTEE deep (a0eff_a0 = 2.164, z = +6.58, N05_results.json) is
     EXCLUDED from the joint by pre-registration (opposite-sign mirror; its
     arbitration is the N05 program card, not this door).
  K3 output is a C-class observable (observer-falsifiable); never promoted
     over the framework claim it tests.
  K4 exit 0 only if: all three channels found, SE-derivation cross-check
     agrees with O03's quoted 0.0662 within 2e-3, and the joint z is
     reproduced by two independent code routes.
Deliverables: O04b_joint_update.json, O04b.out.

## P01 — E[int r^6 ds] closed-form hunt (door: M05's open 0.212857, uncertified)
Measure: EXACTLY M05_geometric_anchors.py first_flight_moments (r_birth
uniform in unit ball, mu isotropic, chord = -R mu + sqrt(1-R^2+R^2 mu^2),
I3 = int_0^chord r^6 ds with the same polynomial expansion).
Protocol: (a) reproduce M05's chord 3/4, r^2 5/12, r^4 1/4 at 1e-12 (gate);
(b) mpmath 30-digit quadrature of E[int r^6 ds]; (c) rational reconstruction
(continued fractions, denominator <= 10^4); (d) MC confirmation 1e8 samples.
Kill conditions (pre-registered):
  K1 a closed form is CLAIMED only if a rational p/q (q <= 10^4) matches the
     30-digit value at |Delta| < 1e-12 AND an independent mpmath route
     (mu-integral done in closed form per R, i.e. the exact chord-length
     change of variables, then 1D quadrature in R) agrees at 1e-12.
  K2 if no such rational exists: verdict OPEN, value published to 12 digits,
     the near-miss list (top-5 continued-fraction convergents with errors)
     reported. NO tuning of denominators to force a hit.
  K3 the reproduction gate (a) failing => lane DIED, M05 unverified.
Deliverables: P01_r6_moment.py/.out/.json.

## P02 — N05 program-card power audit (door: "arbitration program card registered")
Goal: MC-verify the registered n_requirement block of N05_results.json
(per_ring_noise_a0E = 2.2452 a0E; N_req_ring_level = 1655.85 for the 5-SE
SPARC-deficit kill at Delta = -0.2759 a0E; 59 new galaxies at 3 rings each;
N_new_rings 177.14) and the detection-power curve around it.
Kill conditions (pre-registered):
  K1 re-derived N_req must match the registered 1655.85 within 1%.
  K2 MC (5e4 trials, seeded): at N = N_req, the median |z| of the kill
     statistic must sit at 5.00 within 2%; the power to EXCEED the 5-sigma
     threshold at N = N_req must be reported exactly (it is ~50% by
     construction -- recorded, not hidden).
  K3 power at the registered program size (194 gals / ~177 new rings =>
     N_total ~ 1656) reported; if the card's headline 'kill at 59 new
     galaxies' actually requires >60% power at 5 sigma, the card is
     UNDERPOWERED and the register row says so.
  K4 exit 0 only if K1 and K2 pass; K3's verdict recorded either way.
Deliverables: P02_power_audit.py/.out/.json.
