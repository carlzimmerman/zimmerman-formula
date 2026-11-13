# RFX1 RESULT: the measured LMC reflex against a force-law-free momentum bound

2026-11-12. TEST lane. Adopts nothing. Criteria `FROZEN_CRITERIA.md` (sha256 8f14a6c0...b444e, frozen
2026-11-13T02:06:24Z UTC), written before any bound was computed and before any reflex value beyond the lead's
quoted one was read. No amendment. One graded run; a second run reproduced all three outputs byte for byte.

## Labels (primary measurement: Petersen and Penarrubia 2021, 32 +/- 4 km/s, 40-120 kpc)

| reading | footing | label | B_first | z | flipped by |
|---|---|---|---|---|---|
| R1 baryonic inertia | canonical | **REFLEX WITHIN THE BOUND, FRAGILE** | 21.1 +/- 5.5 | 1.60 | (a) LMC alone; (c) rc stellar mass; Yaaqib+ 2024 50+ kpc; Li+ 2026 80-120 kpc |
| R1 baryonic inertia | alt | **REFLEX WITHIN THE BOUND, FRAGILE** | 21.7 +/- 5.7 | 1.49 | same four |
| R2 cold dark energy carries momentum | canonical | **REFLEX WITHIN THE BOUND, FRAGILE** | 28.3 +/- 0.8 | 0.90 | r_c 50; r_c 80; M_eff 1.6e10; Li+ 2026 80-120 kpc |
| R2 cold dark energy carries momentum | alt | **REFLEX WITHIN THE BOUND, FRAGILE** | 26.9 +/- 0.7 | 1.25 | same four |

WITHIN THE BOUND is only the absence of a contradiction: the bound is one-sided (least responsive halo).
Read plainly: the primary measurement sits 1.5 to 1.6 sigma above R1's bound and about 1 sigma above R2's. Neither
reading is contradicted in the primary configuration, and neither is safe: the LMC-alone inventory, the rotation-curve
stellar mass, a larger r_c, the low M_eff, and two of the newer measurements each push z past 2.

Which reading is the framework's is NOT decided by the record (quotes in FROZEN_CRITERIA.md section 3: the halo
"gravitates and lenses as mass", is kept by its galaxy, but its inertia and momentum are never stated, and M5 forbids
the simplest momentum-conserving medium). That is a decision for the owner.

## Numbers

Relative orbit, d'' = -(1 + m_L / m_MW) g_MW(|d|) d_hat, back from today. The last pericentre is 47.3-47.4 kpc,
47-49 Myr ago (v_peri 324 km/s) in every case; the last apocentre is 187-225 kpc, 1.46-1.79 Gyr ago; no run capped.

| | m_L | m_MW | mu | apocentre | |dv| | B_first (toward l, b) | B_abs |
|---|---|---|---|---|---|---|---|
| R1 canonical | 4.07e9 | 6.672e10 | 0.0575 | 224.5 kpc, -1787 Myr | 367.2 | 21.11 (74.4, -51.0) | 37.2 |
| R1 alt | 4.07e9 | 6.672e10 | 0.0575 | 191.5 kpc, -1497 Myr | 377.5 | 21.71 (74.1, -51.9) | 37.3 |
| R2 canonical | 2.5e10 | 3.011e11 (<40 kpc) | 0.0767 | 216.2 kpc, -1714 Myr | 369.5 | 28.33 (74.4, -51.2) | 49.7 |
| R2 alt | 2.5e10 | 3.273e11 | 0.0710 | 186.8 kpc, -1458 Myr | 379.4 | 26.92 (74.1, -52.0) | 46.0 |

sigma_B: R1 5.50 / 5.65 (speed 0.6, m_L +/- 25 % 5.1-5.2, m_MW +/- 10 % 2.1); R2 0.82 / 0.66 (speed only; frozen).
The R1 label rests mostly on the assessed 25 % error on the Magellanic baryons.

Variants, B_first and z against the primary measurement (canonical / alt):
- R1 (a) LMC alone 3.2e9: 16.74 / 17.21, z 2.57 / 2.45 EXCEEDS. (b) plus all Stream gas (6.73e9): 34.0 / 35.0,
  z -0.21 / -0.31. (c) rc stellar mass + census gas (8.27e10 / 7.61e10): 17.17 / 19.13, z 2.46 / 2.01 EXCEEDS.
  (d) plus hot gas: 20.0 / 20.6, z 1.82 / 1.71. Reported: Stream neutral gas only 24.3 / 25.0, z 1.03 / 0.92.
- R2 r_c 30: 36.0 / 34.4 (z -0.98 / -0.59); r_c 50: 23.4 / 22.2 (z 2.12 / 2.44 EXCEEDS); r_c 80: 15.4 / 14.5
  (z 4.13 / 4.36 EXCEEDS); M_eff 1.6e10: 18.5 / 17.5 (z 3.34 / 3.59 EXCEEDS); M_eff 4e10: 44.0 / 41.9.
- B_abs in place of B_first: within on all four.
- Other measurements against the primary bound (z for R1 can / R1 alt / R2 can / R2 alt):
  Yaaqib+ 2024 50+ kpc 40 +/- 7: 2.12 / 2.03 / 1.66 / 1.86; 40-50 kpc 23 +/- 7: 0.21 / 0.14 / -0.76 / -0.56;
  Chandra+ 2024 100 kpc 37 +/- 9: 1.51 / 1.44 / 0.96 / 1.12; 120 kpc endpoint 47 +/- 12: 1.96 / 1.91 / 1.55 / 1.67;
  Bystrom+ 2025 >50 kpc 34.0 +/- 10.6: 1.08 / 1.02 / 0.53 / 0.67; Li+ 2026 50-120 kpc 24.0 +/- 3.8: 0.43 / 0.34 /
  -1.12 / -0.76; 50-60: -0.45 / -0.54 / -2.77 / -2.41; 60-80: -0.16 / -0.24 / -1.86 / -1.56; 80-120 kpc 44.0 +/- 5.4:
  2.97 / 2.85 / 2.87 / 3.14 EXCEEDS on all four.

Reported, no label:
- mu required by the primary measurement: 0.0871 / 0.0848 (R1), 0.0866 / 0.0844 (R2). R1 would need Magellanic
  inertial baryons of 6.4e9 (canonical) / 6.2e9 (alt) against the inventory 3.2e9 (LMC), 4.07e9 (LMC + SMC), 6.73e9
  (plus all Stream gas, helium added). R2 would need M_eff 2.85e10 / 3.0e10, inside LMC1's bracket.
- Direction: the bound points to (74, -51) in every case, 21.6-22.2 deg from the PP21 apex, close to the direction
  opposite the LMC's present velocity (76.7, -42.8; 18.4 deg from PP21, as the lead estimated).
- Own stars (DESI DR1 BHB, RAW1's bins; travel velocity fitted along the R1 canonical bound direction, monopole and
  dispersion free): 20-30 kpc -1.3 [-6.2, +3.7]; 30-40 -1.9 [-11.7, +8.0]; 40-55 +4.2 [-5.2, +13.6]; 55-80
  +20.4 [+8.8, +32.0] km/s. Along the PP21 apex: -3.6, -10.0, +3.2, +25.0 [+12.8, +37.2]. Power: only the 55-80 kpc
  bin (125 stars) is beyond 40 kpc and sees a signal (about 1.8 sigma from zero); its error of about 12 km/s cannot
  tell 21 (R1's bound) from 32 (the measurement) or 28 (R2's bound). These stars have no power on the labels.

## Checks

All passed. K1 r_GC 49.0820 kpc, speed 320.085 km/s; census M_b(<200) 6.6721e10 (stars 5.4838e10, gas 1.1883e10).
K4 max |dE/E| 1.74e-8 / 1.56e-8 over 6 Gyr. K2 (separate two-body integrator, all four primaries): momentum
drift <= 7.7e-14 of m_L |v_L|; Milky Way velocity change equals V_B to <= 3.1e-14 relative; today's separation
reproduced to 5e-12 kpc; 2000 force-free tracers give V_B to <= 3.1e-14. K3 passes on all four with chi 2.78-2.84
against 3: **a narrow pass**. K5 counts 865 / 264 / 241 / 125.
Mutations (rfx1_mut.out): M1 bites both footings (3 x m_L gives B 58.8 / 60.7, z -1.80 / -1.87, a shift of 3.4);
M2 bites on all four (apex moves to (-101, +33), 159-162 deg away, K3 chi 18.6-18.7, fails); M3 BORROWED,
context only: m_L 1.5e11 with m_MW 1.0e12 / 1.3e12 gives B_first 49.1 / 38.6 (canonical), 50.6 / 39.7 (alt), all at or
above 32: the bound is not too tight.
Byte-for-byte: a second run reproduced rfx1.out, rfx1_mut.out and rfx1_results.json exactly (run time about 3 s).
numpy printed spurious "divide by zero / overflow in matmul" RuntimeWarnings to stderr in the own-stars part
(a known macOS Accelerate artefact); the sample counts match RAW1 and every fitted number is finite.

Choices not fixed in the criteria (disclosed): sigma of B_abs uses the same procedure as sigma_B; the Chandra 120 kpc
row is a linear-model endpoint, graded like the others; Bystrom's v_dipole sign convention was not read, its amplitude
is graded.

## Lead's verification and reading (2026-11-12, after the result; not graded; no label changes)

Verification: `FROZEN_CRITERIA.md` matches its stamp and predates the script; the lead re-ran `rfx1.py` and
`rfx1.out`, `rfx1_mut.out` and `rfx1_results.json` came back equal byte for byte. Source spot-checks on the
arXiv abstract pages (PROVISIONAL, summariser reads): Petersen and Penarrubia 2021 gives 32 +4/-4 km/s toward
(56 +/- 9, -34 +10/-9), tracers at 40 to 120 kpc, as used; Li et al. 2026 (arXiv:2604.01628) says the reflex
"increases from -19 to -44 km/s with radius" beyond 50 kpc, matching the table rows used; the Yaaqib et al.
2024 abstract gives no numbers, so its table rows rest on the lane's single read.

Post hoc (`rfx1_lead_check.py`, `rfx1_lead_check.out`): the bound against the look-back window T, where
V(T) = -mu (v_rel(today) - v_rel(today - T)).

1. **B_first is the largest the bound gets.** B(T) rises steadily with T and peaks at the last apocentre, so
   no shorter window gives more.
2. **The bound's direction swings across the sky with the window.** For T of 100 to 150 Myr it points near the
   LMC's present position, (-87, -53) to (-83, -62); for the full window it points opposite the LMC's velocity,
   (74, -51). The published apexes split the same way: Chandra et al. 2024 and Bystrom et al. 2025 lie 2 and
   8 degrees from the short-window direction; Petersen and Penarrubia 2021 and Yaaqib et al. 2024 lie 22 and 29
   degrees from the full-window one; Li et al. 2026 is matched by no window (38 to 52 degrees at best).
3. **Matched in direction, the short-window bound is far below the measured amplitudes, for any LMC.** At the
   window that matches Chandra's apex the bound is 5.3 to 7.3 km/s in the four readings against a measured
   37 +/- 9. But with the standard-model literature's masses (BORROWED, context only) it is still only 10 to
   13 km/s, 2.7 to 3.0 sigma below. So that comparison cannot be held against the framework: it shows that a
   pure momentum window is not what those measurements are. The frozen direction gate K3 would fail against
   them, and the lane would then be NOT EVALUABLE.
4. **Reading.** Against the one measurement whose direction this picture matches, the framework's light LMC is
   not contradicted, with thin margins (z 1.5 to 1.6 for baryonic inertia, 0.9 to 1.25 with a halo that
   carries momentum). For baryonic inertia the label turns on two things: whether the Magellanic Stream's gas
   counts as moving with the LMC, and which Milky Way baryon mass is used. With the stellar mass the
   framework's own rotation-curve fit needs (RCF1: 7.08e10 canonical, 6.42e10 alt) the reflex EXCEEDS the
   bound (z 2.46 / 2.01) unless the Stream gas is counted.
5. **Not settled here:** which reading of inertia is the framework's (the record is silent; an owner
   decision), and what a responsive halo does, which needs the framework's own response calculation.

LMC1's statement that its rigid model "is not validated against the measured reflex" was written against
Petersen and Penarrubia's apex only. Its apex is 17 to 37 degrees from Chandra's and Bystrom's (`C3` in the
check output). A dated note has been added to LMC1's RESULT.md.

## Limits

A bound, not a prediction (least responsive halo; a responsive halo gives less). The published travel velocities are
model fits, and they disagree: PP21 and Yaaqib+ put the apex at positive l (8 and 29 deg from this bound's
direction), Chandra+, Bystrom+ and Li+ at negative l (58-79 deg from it). K3 is frozen against PP21 only; against
the newer measurements the direction would not match, and the picture would then not be what was measured. The
amplitudes rise with radius (Li+ 2026: 18 at 50-60 to 44 at 80-120 kpc), which a single least-responsive bound
cannot follow: its 80-120 kpc row exceeds the bound in every reading. Baryon inventories carry mass-to-light,
distance and helium assumptions (the 25 % error on m_L is assessed, not published). Two bodies only: no M31, no
group, no external field, no dynamical friction, no mass loss of the Clouds, the SMC moved rigidly with the LMC.
The R2 bound depends strongly on r_c, which is a choice. The record does not decide R1 versus R2. The web reads are
PROVISIONAL summariser reads (SOURCES.md).

## Files

`FROZEN_CRITERIA.md`, `FREEZE_STAMP.txt`, `SOURCES.md`, `rfx1.py` (field and sample code copied from LMC1's
lmc1_core.py and lmc1.py, origins in its header), `rfx1.out` (graded run), `rfx1_mut.out` (mutations),
`rfx1_results.json`, this file; the lead's `rfx1_lead_check.py`, `rfx1_lead_check.out`.
Run: `nice -n 10 python3 -I -B rfx1.py <MWS_BHB.fits>` (about 3 s, one thread).
Data: https://data.desi.lbl.gov/public/dr1/vac/dr1/mws-bhb/v1.0/MWS_BHB.fits, sha256
5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246, not in the repository.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
