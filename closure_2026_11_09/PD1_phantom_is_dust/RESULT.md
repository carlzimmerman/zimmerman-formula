# PD1 RESULT: FAIL / FAIL (criteria 0dc7929421), first failing gate P2 KiDS

Variant N: the law's phantom IS the conserved dust. TEST lane, quarantined. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
Footings never pooled.

| gate | canonical | alt |
|---|---|---|
| P1 population conservation, q_N at z 0.5 / 1 / 2 (line <= 1) | **PASS** 0.485 / 0.391 / 0.271 | **PASS** 0.534 / 0.430 / 0.299 |
| **P2 KiDS** (pointwise, truncated phantom) | **FAIL**: 20/59 points over, worst -0.635 dex, mean -0.133 | **FAIL**: 24/59, -0.675 |
| P2 SPARC | PASS: rms 0.0563 (line 0.0660); no galaxy truncated inside its last point (median R_trunc 186 kpc) | PASS 0.0558 |
| **P3 groups** | **FAIL** 7/20, 2/20 | **FAIL** 4, 1 |
| **P3 X-COP** | **FAIL** mean -0.319. Bins -0.45 / -0.26 / -0.22 (over-filled). Dark / M_dyn 2.85 / 1.75 / 1.53 vs TR1 0.71 / 0.66 / 0.58; leftover alone 2.66 / 1.55 / 1.23 | **FAIL** -0.308 |
| P4 cosmology | PASS, carried: cold dust + Newtonian baryons is the record's cold reference (lensing 8.56, forest 0, fsigma8 ratio 1, S8 0, seeds 1; QX15 L1 PASS). The 1-halo redistribution is NOT EVALUATED | PASS |
| **P5 Bullet** | **FAIL**: M300 Z +8.41 / +2.31 (the leftover over-fills both subclusters, 9.5 / 8.1 M_b inside R200). The phantom-on-gas part alone is DB1's law-only row, also FAIL (Z -4.55) | **FAIL** +8.47 / +2.41 |
| P6 | Ursa Major and Cassini carried (N equals the law inside R_trunc); Coma UDGs as law-only (+1.12, reported) | |

**Known answers, all pass.**
- KA-P1: WL1's q_pop z 1 is 0.9363 / 1.0793 (WL1 0.936 / 1.079).
- KA-P2: the KiDS ceiling mean is +0.0011 / +0.0009, as WL1.
- KA-P3: with truncation off this is law-only (KiDS 2e-16, X-COP +0.4675 / +0.4345, groups 0/0).
- KA-P4: the deep-phantom closed form, to 5e-4.

## The share, per halo

**The share at z 0.** The dust in the Lagrangian sphere of the turnaround shell is a fixed **59.5 M_b** for every mass (seed
M_b (1 + R)). The Lagrangian radius x_ta is 0.73 / 3.4 / 15.7 Mpc at log M_b 9 / 11 / 13.

| log M_b | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|
| R_ms (Mpc) | 0.08 | 0.17 | 0.36 | 0.78 | 1.69 | 3.64 | 7.84 |
| M_ph(<R_ms) / share | 3.41 | 2.32 | 1.58 | 1.07 | 0.73 | 0.49 | 0.33 |
| R_trunc (kpc) | 23 | 73 | 231 | 732 | = R_ms | = R_ms | = R_ms |

Alt: 3.74 to 0.37.

**Mass dependence.**
- **Below about 10^11.1 the phantom wants more than the share.** The truncation is at 23-730 kpc: outside SPARC's radii, inside
  KiDS's (to 3 Mpc).
- **Above it, the share is left over and over-fills.** At group and cluster scale the leftover is 1-3 M_dyn.
- P1 passes because the population is dominated by the galaxies whose phantom is capped. Per-halo conservation fails below
  10^11.1, which shows up in KiDS.

## Where it fails, and why the FAILs are robust

1. **KiDS:** past R_trunc the lens is Newtonian with M_b + share. Lensing falls as 1/r^2 instead of the law's 1/r, so up to
   -0.64 dex at 1-3 Mpc.
   - With the share x 10 (MP1), KiDS fails the other way: the leftover over-fills, 0.95, all 59 points.
   - The Moster bracket also fails: KiDS 1.03 (27-28 points), SPARC rms 0.27.
   - No single share passes: the light bins need more dust, the heavy bins less.
   - The source's 1.35 Mpc R_trunc for an L* galaxy needs a share of 123-156 M_b, two to three times the Lagrangian dust.
2. **Groups and X-COP:** the phantom acts on the baryons, and the leftover share (nearly all of it in clusters) piles on top.
   Dark mass reaches 1.5-2.9 M_dyn, against TR1's 0.58-0.71.
3. **Bullet:** the phantom follows the gas (the law-only failure, Z -4.5); the leftover follows the galaxies but over-fills
   (Z +8.4). Neither placement matches.

## P7: dynamics (stated)

- A conserved collisionless dust in a Jeans equilibrium in a flat potential has rho = 2 sigma^2 / (4 pi G r^2). The law's phantom
  needs v_f^4 = G M_b a0, i.e. sigma^4 tied to M_b a0. Nothing in a dust action (shift-symmetric khronon, T^mn conserved) sets
  that normalisation or the profile's inner shape.
- The "own multi-stream dispersion" S^2 = c^2 h_mn T^mn / (u u T) of a single scalar field is identically 0: its gradient
  defines one velocity per point, so it is single-stream by construction. It cannot act as the switch.
- **The phantom profile is a phenomenological closure put in by hand, not a consequence of the stated action.**
- What would change that: an equation of motion in which the dust's equilibrium density is sourced by
  ∇.((nu - 1) g_N,b). That is the QUMOND phantom equation itself, i.e. the law put back in as the dust's dynamics.

## Reading

N keeps everything the cold reference gets right, by construction: the CMB, lensing, growth, the forest, seeds, and P1's
population budget. It gets SPARC, because truncation happens beyond the last measured points.

**It breaks on halo bookkeeping.** One conserved share per halo cannot match the law's phantom at every mass:
- light galaxies run out of dust inside the KiDS radii;
- groups and clusters have dust to spare, which over-fills them and the Bullet.

The law's phantom grows as sqrt(M_b) r while the Lagrangian share scales as M_b. So the phantom/share ratio falls as M_b^-1/2
times the radius factor, and no constant mass-to-share map fits both ends.

**What a repair would need:**
1. A mass-dependent share: about 2-3x more dust per M_b around L* and lighter lenses, much less in clusters. That is a transfer
   of dust from clusters to galaxies, against the infall direction.
2. And an action that produces the phantom profile (P7), not a closure.

## Files

- Criteria: `FROZEN_CRITERIA.md`.
- Scripts: `pd1.py` (P1-P3, P5 via WM1's bchild, KAs, MUTATE, brackets), `pd1_grade.py`.
- Outputs: `pd1.json` / `pd1.out`, `pd1_MUTATE.json`, `pd1_grade.json` / `pd1_grade.out`, the log `run_pd1.txt`.
- Compute: one thread, 65 s, RSS < 0.3 GB.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
