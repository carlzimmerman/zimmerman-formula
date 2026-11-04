# FN1b_fixed_length_static: NO UNIVERSAL LENGTH PASSES on either footing, in the form an action gives (R). Cassini and the planets pass at every length; the dwarfs pass only up to 0.1 kpc and the Milky Way only at 2 kpc

Criteria `FROZEN_CRITERIA.md` (e6e031a163), committed alone before any script, under FN1's criteria (72f9d70fd6).
**Not blind**: KT14–KT19, KT33, KT34, CZ1–CZ5, CW1 and CW3 were read first. κ = ½ FITTED, held fixed. Footings canonical
9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Not theory closed. Nothing here says the data favour the framework.
No cold component, no particle. No downloads.

- **Scripts.** `fn1b_small.py` (T1 Cassini, T2 dwarfs, T3 SPARC, T4 planets), `fn1b_mw.py` (T0 Milky Way, one footing per
  process), `fn1b_label.py` (frozen labels), `fn1b_ka_snapshot.py` (known-answer snapshot).
- **Outputs.** `fn1b_small.{out,json}`, `fn1b_mw_{canonical,alt}.{out,json}`, `fn1b_label.{out,json}`, MUTATE twins
  `*_MUTATE.*`, `.time` files, and the first runs `fn1b_small_RUN1.out`, `fn1b_mw_canonical_RUN1.out`.
- **Engines.** KT14's code (definitions loaded from `kt14.py`), CZ2's dwarf code, CZ5's plain3 row, KT19's SPARC code and
  CZ3's planet code, copied verbatim and marked. KT33's `mw_reciprocal.py` and `cassini_v2.py` are in `vendor_kt33/`,
  copied unchanged: KT33 and KT34 were uncommitted (`vendor_kt33/SOURCE.md`).
- **Compute.** One thread, nice 15. Small gates 197 s at 0.30 GiB peak. Milky Way 334 s (canonical) and 344 s (alt),
  peak **1.26 / 1.31 GiB, above the 1 GB target** (disclosed below).

## Labels (frozen rule)

| form | canonical | alt |
|---|---|---|
| **R**, Φ_N[ρ] + S Φ_ph[Sρ], the static limit of any action with a fixed kernel (primary) | **NO UNIVERSAL LENGTH PASSES** | **NO UNIVERSAL LENGTH PASSES** |
| SO, Φ_N[ρ] + Φ_ph[Sρ], the record's KT14–KT19 rule, no action (beside) | UNDECIDED (NOT EVALUABLE at L = 0.024 kpc) | NO UNIVERSAL LENGTH PASSES |

## R, per length (canonical / alt)

| L, kpc | T0 MW cells of 1,375 | T1 Q2 / ceiling | T2 dwarfs, E1 (line 15/24) | T3 SPARC | T4 worst Z | row |
|---|---|---|---|---|---|---|
| 0.024 | 0 / 0 | 7.41e-10 / 8.68e-10 | 18 / 18 | NOT EVALUABLE (V4) | 2.05e-09 / 2.51e-09 | FAILS: T0 |
| 0.1 | 0 / 0 | 1.02e-11 / 1.20e-11 | 16 / 16 | SURVIVES, d +0.0006 / +0.0013 | 2.84e-11 / 3.46e-11 | FAILS: T0 |
| 0.25 | 0 / 0 | 6.55e-13 / 7.68e-13 | 14 / 14 | SURVIVES | 1.82e-12 / 2.22e-12 | FAILS: T0, T2 |
| 0.5 | 0 / 0 | 8.19e-14 / 9.60e-14 | 12 / 13 | SURVIVES | 2.27e-13 / 2.77e-13 | FAILS: T0, T2 |
| 1.0 | 0 / 0 | 1.02e-14 / 1.20e-14 | 9 / 10 | HURT, d +0.0175 / +0.0110 | 2.84e-14 / 3.46e-14 | FAILS: T0, T2, T3 |
| 2.0 | 2 [GRID-DEPENDENT] / 38 | 1.28e-15 / 1.50e-15 | 6 / 6 | FAILS SPARC, d +0.0607 / +0.0498 | 3.55e-15 / 4.33e-15 | FAILS: T2, T3 |

Plain QUMOND (L = 0) on the same models: MW 0 / 0 cells (KT14), dwarfs 18 / 18 (CZ2, E1).

## SO, per length, beside (canonical / alt)

| L, kpc | T0 MW cells | T2 dwarfs E1 | T3 SPARC | row |
|---|---|---|---|---|
| 0.024 | 0 / 0, NOT EVALUABLE (KT14's C3) | 18 / 18 | SURVIVES / HURT | NOT EVALUABLE: T0 / FAILS: T3 |
| 0.1 | 0 / 0 | 17 / 17 | SURVIVES | FAILS: T0 |
| 0.25 | 0 / 0 (KT14, reproduced) | 15 / 15 | SURVIVES | FAILS: T0 |
| 0.5 | 0 / 0 (KT14, carried) | 14 / 14 | SURVIVES | FAILS: T0, T2 |
| 1.0 | 0 / 0 (KT14, carried) | 12 / 12 | SURVIVES | FAILS: T0, T2 |
| 2.0 | 0 / 7 (KT14, carried) | 9 / 9 | HURT | FAILS: T0, T2, T3 / FAILS: T2, T3 |

T1 and T4 pass at every length in both forms: SO's Q2 is 2√2 times R's (2.46e-9 of the ceiling at most).

## Reading
- **The static gates pull the length two ways.**
  - The Milky Way needs about 2 kpc. Below that no in-prior cell passes on either footing in either form.
  - The dwarfs need 0.1 kpc or less in R (16/24 at 0.1, 14 at 0.25, 6 at 2 kpc).
  - SPARC in R survives from 0.1 to 0.5 kpc and is hurt or fails from 1 kpc.
  - Cassini and the planets set no upper limit: Q2 falls as L⁻³.
- **The action's form is stricter than the record's rule on dwarfs and SPARC.** The outer smoothing removes more of
  the boost: Fornax at Υ = 2 reads 6.16 km/s in R against 7.28 in SO at 2 kpc (canonical), observed 11.7.
- **On the Milky Way it helps at 2 kpc**: 2 cells in R against 0 for KT14's rule (canonical), 38 against 7 (alt).
- **So one Gaussian length cannot carry the five static gates.** A length that grows with mass, or a second length,
  would be another fitted input. Mass-scaled filters are on record and have no action (KT16–KT32, CZ1–CZ5).

## As hard as a fail
- **KA1-C3 FAILED on both footings.** KT14's radial smoothing test at 24 pc reads 1.5e-2 against its 1e-3 line.
  - Post-result diagnostic, disclosed: the error sits within 50 pc of the axis; at R ≥ 0.1 kpc it is 2.3e-6.
  - By the frozen rule the SO Milky Way row at 24 pc is NOT EVALUABLE, so SO canonical reads UNDECIDED.
  - The computed row there has 0 cells and the same line counts as KT14's plain row (L1 433, L2a 685, L2b 67, L3 170).
- **V4 FAILED at 24 pc on SPARC** (4.7e-1 against 1e-3). The dwarf paths pass at every L (≤ 9.9e-5).
  - Post-result diagnostic: KT19's 1,500-point grid step exceeds 24 pc at 45 of NGC 2403's 73 radii, up to 171 pc.
  - So R's SPARC row at 24 pc is NOT EVALUABLE (frozen). SO's 24 pc SPARC rows (canonical SURVIVES, d +0.0033; alt HURT,
    d +0.0060) carry the same under-resolution and are graded as frozen. The alt SO row at 24 pc fails on that T3.
- **[GRID-DEPENDENT], canonical R at 2 kpc:** one of the 2 passing cells fails at refine 2. On alt, none of the 10
  rechecked cells flips.
- **RSS above the 1 GB target:** 1.26 / 1.31 GiB peak in the final runs. KT14's smoothing operator alone is about
  0.6 GiB; KT14's own run peaked at 1.8 GB. No 1024³ run was live; the BK2 and SY1 searches were.
- **The real runs exit 1**, by the scripts' rule, because of the failed checks above (V4 in `fn1b_small`, KA1-C3 in
  each Milky Way run).
- **Scope.**
  - The dwarf model is CZ2's 1D one with the quadrature external field. The D3 row (vector ν) gives the same pass or fail
    at every length; E2 (MW + M31 field) reads one or two lower, and at 0.25 kpc SO's 15 would read 14.
  - The kernel is a Gaussian. A Helmholtz (Yukawa) kernel, the simplest local-field form, is not graded.
  - SPARC uses KT19's spherical approximation.
  - Cassini and the planets use the exact linear response; its error is of order the smoothed Sun's field over the
    Galactic one, ≤ 1e-6 here. CZ4's environment bounds (Cassini 1.81e-3 / 1.90e-3 of the ceiling; Saturn 3.03e-4 /
    3.63e-4) are far larger than the Sun's own terms and are reported beside, not graded.

## Checks

| check | result |
|---|---|
| KA1 | KT14's code at 0.25 kpc reproduces `kt14.json` exactly on both footings (n_pass, line counts, K_min_L1, vc_max, best D) |
| KA1-C3 | **FAIL** at 0.024 kpc (above); PASS at 0.1 kpc (8.4e-4) |
| KA2 | KT33's engine reproduces its grid run for 25 cells per footing: max rel 2.6e-11 / 6.6e-11 |
| KA3 | CZ2's E1 plain 18 and HALF 18 per footing; KT15's 2 kpc arm 9/24 with its field, 10/24 isolated |
| KA3b | CZ5's plain3 17 / 18, Fornax 12.59 / 13.15 km/s |
| KA4 | KT19's 0.1720 / 0.1697 and +0.0029 / −0.0004 |
| KA5a, KA5b | KT33's stored Cassini q to 1.1e-14; CZ2/CW1's HALF flux numbers 1.179 / 2.97 |
| KA6 | CZ3's HALF Saturn Z 11.17 / 18.13 |
| V1 | (a) and (b) pass at every L on both footings; largest (b) Ou difference 0.232 km/s at 0.25 kpc. (c) within its lines everywhere (Δv_c ≤ 0.099 km/s) |
| V2 | analytic Cassini q against KT33's numeric Hessian: max \|ratio − 1\| 2.54e-04 |
| V3 | analytic planet monopole against CZ3's numeric one at 24 pc: 1.25e-04 |
| V4 | dwarfs ≤ 9.9e-05; SPARC **FAIL** at 0.024 kpc (4.7e-01), ≤ 1.4e-04 from 0.1 to 2 kpc |
| K-finite | every graded value finite |
| MUTATE twin (ν ≡ 1) | see below |
| reruns | `fn1b_small` rerun equals RUN1 apart from timing and RSS (JSON SHA-256 def86d6f…, those fields removed). The canonical MW run with the vendored modules equals RUN1 (KT33's own files) apart from RSS, runtime and the added finiteness line. Both final MW runs equal the runs before them apart from RSS and runtime |

## MUTATE twin (ν ≡ 1 in every path), `*_MUTATE.*`

It bites as frozen, and every twin process exits 1.
- **Known answers fail.** Small gates: KA3, KA3b, KA4, KA5a, KA5b and KA6, with V2 and V3 (V4 fails as in the real
  run). Milky Way: KA1 and KA2 on both footings.
- **The physics goes Newtonian.** Dwarfs read 3/24 at every length in both forms; SPARC's rms is 0.573 at every length;
  every Milky Way row reads v_c max 200.0 km/s and 0 cells; Cassini Q2 and the planet rates are 0.
- **The twin's labels** (`fn1b_label_MUTATE.out`) read NO UNIVERSAL LENGTH PASSES for both forms and footings. For R this
  coincides with the real label, so the bite is read from the checks and the counts, as the criteria say.

## Disclosed changes before grading
- The first runs imported KT33's modules from its uncommitted folder. The two modules were then vendored unchanged,
  KT33's stored known answers snapshotted, and every graded output re-made from the final scripts. RUN1 is kept.
- Memory: a retained operator is now deleted and collected after each KT14 width (canonical peak 1.45 GiB in RUN1,
  1.26 GiB in the final run).
- A warning filter for this machine's false matmul FP flags (as KT14 and CW1), with a finiteness check added.
- The labeler's row text shows NE for gates that are not evaluable. Display only; no label changed.
- The KA1 message and `rel()` were made safe for a missing value after the twin first crashed on one (under ν ≡ 1 no
  cell has v_c in line). Both footings were then rerun from the final script; their outputs equal the earlier runs
  apart from RSS and runtime.
