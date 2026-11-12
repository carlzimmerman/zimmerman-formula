# FINAL-1 RESULT: the theory, assembled (2026-11-11)

**Label: THEORY WRITTEN / THEORY WRITTEN** (canonical / alt — footings graded separately, never pooled).

ASSEMBLY lane, quarantined. Adopts nothing, relabels nothing, registers nothing.
**kappa = 1/2 FITTED; not theory closed.**
Criteria `FROZEN_CRITERIA.md`, committed alone before any FINAL-1 script existed or any FINAL-1 number
was computed. All seven graded arithmetic checks PASS on both footings. All four mutation arms bite.

---

## 1. What was asked, and what came back

Write the theory the record supports, in seven numbered pieces: ontology, action, conserved quantity +
epoch, field equations, three regimes, the empirical ledger, and five pre-registered unmeasured
predictions. Cite a lane for every claim. Compute every number in SI. Leave any number not on disk as
UNAVAILABLE rather than guessing.

It is in `THEORY.md`. The four things worth flagging here:

1. **No bulk term is new.** Every term inside the volume integral is the certified action (A) (QX17).
   The new content is three objects: the assembly hypersurface **Sigma_f**, the **assembly rule**
   imposed there, and the **transport** bookkeeping. This is a structural claim, not a modest one: the
   formation reading does not repair a single gate by adding dynamics, so it inherits (A)'s passes
   and (A)'s failures. What it changes is **which solution a region is on, and with what
   normalisation**.
2. **Sigma_f is not the closed door.** Keying a *dust stiffness* on the clock's expansion is dead
   (TK1: BREAKS AT TURNAROUND). Keying an *initial condition* on the zero of the expansion is a
   different object — it never enters the field equations, so there is nothing for TK1's instability
   to act on. The epoch is located by certified lanes: fold at 0.52 R_ta (FLD1), settling shock at
   0.51 R_ta (VSH1), all masses, both footings, since z = 4.96 / 3.45 / 1.46.
3. **The ledger has a hard ceiling, and the record already broke it.** Baryon loss is the only upward
   channel and it saturates at d_max(u). X-COP sits +0.185 dex above its ceiling (canonical; +0.119 alt)
   and CLASH +0.334 (+0.273). That is printed as the theory's **landed failure**, not folded into
   the predictions as a soft miss.
4. **This lane's own arithmetic is not decorative.** It rebuilds all 16 class offsets from the frozen
   DD1 table per system per footing, and reproduces FRM1's published values to the third decimal in
   every case; it also reproduces the record's r_M, budget radius and truncation radius independently.
   That is the one genuinely new computation here, and it is a cross-check, not a discovery.

---

## 2. The checks (all PASS, both footings)

| check | what it must do | result |
|---|---|---|
| **A1** | the law's two forms agree, and u = x^2, on every DD1 point | PASS (worst relative deviation 2.3e-15 / 2.3e-15; inversion 4.4e-16) |
| **A2** | the deep column and the amount-fixing gas column, in SI | PASS: a0/2piG = 2.232051e-1 / 2.697452e-1 kg/m^2 = 106.849 / 129.128 Msun/pc^2; a0/(pi G x_b^2) = 1.287297e-2 / 1.555710e-2 kg/m^2 = 6.1623 / 7.4472 Msun/pc^2 (GAS1 prints 6.1627 / 7.4477 with G = 6.674e-11; relative difference 6.5e-5, i.e. its rounding) |
| **A3** | the ceiling d_max(u) is monotone and tends to (1/2) log10 u | PASS (monotone over u = 1e-3..1e6; ratio 0.99894 at u = 1e4) |
| **A4** | per-class ledger from the frozen table | PASS (16 classes, both footings; print below) |
| **A5** | the amount cap at FLD1's window edges | PASS (demand/budget = 7.67 / 18.08 canonical, 8.44 / 19.89 alt) |
| **A6** | the three regimes' radii, ordered | PASS (r_M < sqrt2 r_M < x_b r_M < x_t r_M) |
| **A7** | cosmic time for the epoch test | PASS (t = 13.0924 / 8.9601 / 6.2708 Gyr at z = 0.05 / 0.45 / 0.90) |

**A4, the ledger** (per class: number of systems, footing-free median field u, median enclosed ratio X,
median offset d from today's law, robust standard error, the exact ceiling d_max, and the two
one-parameter inversions f_b (baryons kept, f_C = 1) and f_C (charge kept, f_b = 1)).
Recomputed from `fable52_push/DD1_deduce_from_data/dd1_table.csv`, main rows only, unchanged.

| class | n | med u | med X | med d | se | d_max | reach frac | f_b | f_C |
|---|---|---|---|---|---|---|---|---|---|
| SPARC | 149 | 6.622 / 8.003 | 1.992 | +0.004 / −0.023 | 0.012 / 0.011 | 0.388 / 0.426 | 0.93 / 0.93 | 1.032 / 1.000 | 1.013 / 0.901 |
| faint rotators | 20 | 17.08 / 20.64 | 1.481 | **−0.239 / −0.274** | 0.045 / 0.044 | 0.589 / 0.630 | 1.00 / 1.00 | 6.085 / 7.534 | 0.440 / 0.396 |
| tidal dwarfs | 6 | 27.16 / 32.82 | 0.169 | −0.687 / −0.725 | 0.100 | 0.691 / 0.733 | 1.00 / 1.00 | 1655 (accr.) | 0.038 / 0.034 |
| massive spirals | 12 | 13.71 / 16.57 | 3.572 | +0.066 / +0.032 | 0.042 | 0.541 / 0.582 | 1.00 / 1.00 | 0.583 / 0.780 | 1.240 / 1.109 |
| ATLAS3D | 187 | 0.330 / 0.399 | 0.471 | +0.070 / +0.052 | 0.010 | 0.023 / 0.030 | 0.37 / 0.55 | 3.572 / 2.358 | 1.720 / 1.496 |
| RC100 | 100 | 0.579 / 0.700 | 0.810 | +0.088 / +0.066 | 0.017 | 0.049 / 0.062 | 0.43 / 0.56 | 2.444 / 2.065 | 1.842 / 1.585 |
| KiDS | 4 | 1272 / 1537 | 48.63 | +0.137 / +0.097 | 0.009 / 0.011 | 1.547 / 1.588 | 1.00 / 1.00 | 0.518 / 0.631 | 1.383 / 1.256 |
| groups | 20 | 43.06 / 52.04 | 9.066 | +0.161 / +0.123 | 0.023 | 0.794 / 0.836 | 1.00 / 1.00 | 0.386 / 0.491 | 1.531 / 1.382 |
| **X-COP** | 7 | 4.446 / 5.374 | 7.672 | **+0.496 / +0.465** | 0.022 / 0.023 | 0.310 / 0.346 | **0.00 / 0.00** | **UNREACHABLE** | 4.333 / 3.884 |
| **CLASH** | 20 | 3.194 / 2.643… | 7.516 | **+0.553 / +0.524** | 0.023 | 0.250 / 0.219 | **0.00 / 0.00** | **UNREACHABLE** | 5.095 / 5.759 |
| MW bright dwarfs | 11 | 147.9 / 178.8 | 23.25 | +0.065 / +0.027 | 0.153 / 0.152 | 1.070 / 1.112 | 1.00 / 1.00 | 0.680 / 0.854 | 1.191 / 1.075 |
| MW ultra-faints | 31 | 1243 / 1502 | 117.9 | **+0.592 / +0.552** | 0.098 | 1.541 / 1.583 | 1.00 / 1.00 | 0.053 / 0.065 | 4.080 / 3.702 |
| M31 dwarfs | 33 | 293.6 / 354.9 | 22.1 | +0.090 / +0.051 | 0.088 / 0.085 | 1.223 / 1.265 | 1.00 / 1.00 | 0.623 / 0.766 | 1.253 / 1.136 |
| LG field dwarfs | 13 | 82.48 / 99.68 | 8.483 | −0.090 / −0.130 | 0.062 / 0.060 | 0.940 / 0.982 | 1.00 / 1.00 | 1.601 / 1.956 | 0.797 / 0.722 |
| Coma UDGs | 11 | 133.4 / 161.2 | 23.41 | +0.319 / +0.280 | 0.073 | 1.047 / 1.089 | 1.00 / 1.00 | 0.186 / 0.234 | 2.186 / 1.980 |
| NGC 1052 UDGs | 2 | 44.25 / 53.48 | 0.066 | −0.843 / −0.881 | 0.132 / 0.131 | 0.800 / 0.842 | 1.00 / 1.00 | 7.2e8 (accr.) | 0.009 / 0.008 |

Counts per footing: **3 of 626** systems sit below X = 0 beyond 3 standard errors (the frozen
allowance, HIS1 H2(a), is ≤ 3); **4 of 16** classes are UNREACHABLE by any transfer; **13 of 16**
(canonical) / **15 of 16** (alt) classes require a non-trivial transfer.

**The two structural violations** (canonical / alt): X-COP **+0.496 ± 0.022** / **+0.465** against a
ceiling of **+0.310** / **+0.346** → above by **+0.185 / +0.119** dex; CLASH **+0.553 ± 0.023** /
**+0.524** against **+0.219** / **+0.250** → above by **+0.334 / +0.273**. FRM1 additionally finds
**77 %** of X-COP's and **98 %** of CLASH's individual points above the absolute ceiling a0/g_bar.

**Cross-check against the record (this is the lane's own new arithmetic).** FRM1's published per-class
offsets are reproduced here to three decimals from the frozen table: SPARC +0.004 / −0.023;
faint rotators −0.239 / −0.274; tidal dwarfs −0.687 / −0.725; NGC 1052 −0.843 / −0.881;
massive spirals +0.066 / +0.032; ATLAS3D +0.070 / +0.052; RC100 +0.088 / +0.066; KiDS +0.137 /
+0.097; groups +0.161 / +0.123; MW bright +0.065 / +0.027; MW ultra-faints +0.592 / +0.552;
M31 +0.090 / +0.051; LG field −0.090 / −0.130; Coma UDGs +0.319 / +0.280; X-COP +0.496 / +0.465;
CLASH +0.553 / +0.524. The derived scales also reproduce the record: r_M = **6.479 / 5.894 kpc** at
log M_b 10.45, X = 1 at **9.163 / 8.335 kpc**, budget 5.41 M_b spent at **38.155 / 34.708 kpc**,
truncation at **388.7 / 353.6 kpc** (x_t = 59.998).

**A5, the amount cap, recomputed at FLD1's KiDS window edges** (log M_b = 10.45):

| r | where | x | demand X(x) | /5.41 budget | /1.06 delivered | /1.40 settled |
|---|---|---|---|---|---|---|
| 272 kpc | FLD1 inner window edge | 41.98 / 46.15 | 41.48 / 45.65 M_b | 7.67 / 8.44 | 39.14 / 43.07 | 29.63 / 32.61 |
| 637 kpc | FLD1 middle window edge | 98.31 / 108.08 | 97.82 / 107.58 M_b | 18.08 / 19.89 | 92.28 / 101.49 | 69.87 / 76.84 |

---

## 3. Mutation arms (each must change its stated outcome, else disclosed)

| arm | mutation | required change | result |
|---|---|---|---|
| **M1** | the force reading: X := X_L(g_bar), so d := 0 for every system | classes in their band must drop, and the two *signed* structural signs must be wrong | **BITES.** 12 of 16 vs formation's 14 of 16; and the stripped family's band is LOW (True) while the ultra-faints' band is HIGH (True) — both contradicted by d = 0 |
| **M2** | a0 x 2, both footings | footing-marked rows must scale; footing-free rows must not budge | **BITES.** r_M scales by 0.707107 = 2^(-1/2); columns by 2.000000; footing-free rows identical by construction |
| **M3** | class labels shuffled across systems (seed 20261110; bands stay with the names) | classes in band must fall below 13 | **BITES.** 9 of 16 |
| **M4** | the ceiling removed (f_b -> 0 lifts X without limit) | UNREACHABLE count must go to 0 and P1 must go VIOLATED -> VACUOUS | **BITES.** 4 -> 0 |

No arm failed to bite, so nothing is disclosed for that reason.

---

## 4. Disclosures

- **This lane does not derive the joint.** It inherits (A)'s failing verdict there (COL1, FLD1). What it
  adds is not a mechanism; it is a statement of which initial condition the data picked, plus five tests.
- **FRM1's own disclosures apply unchanged and are not restated as this lane's findings**: one void clause
  (F2's 3-standard-error requirement for the stripped family is unsatisfiable — KA2 shows the synthetic
  history truth, the theory's own truth, fails it), and one criteria amendment made before any FRM1 number
  existed. This lane uses FRM1's *reported* label ("HOLDS EXCEPT"), not its frozen-line label.
- **My per-system median recipe is not DD1's exact code.** It reproduces every published DD1/FRM1 class offset
  to three decimals, so the difference does not move a number here — but it is my recipe, not a clone.
- **g_b,f is free per class.** The f_b values in A4 are inversions of the measured offset under one channel (f_C = 1)
  or the other (f_b = 1), not independent measurements. The master equation is underdetermined with both free;
  FRM1 takes f_b from the standard picture for the hosted classes and derives f_C.
- **H3 FAILS.** I repeat it because it is the largest hole, not to bury it: the isolated faint gas-rich rotators
  sit −0.239 / −0.274 dex below the law, and the ledger can only get there by f_b ≈ 6 / 8, i.e. by most of their
  baryons having arrived after their halo's charge was fixed. That is a real contradiction unless it is measured.

---

## 5. Files

- `FROZEN_CRITERIA.md` (committed alone, before any script or number)
- `final1.py` -> `final1.json` / `final1.out` (primary)
- `final1.py --mutate` -> `final1_MUTATE.json` / `final1_MUTATE.out`
- `THEORY.md` (the deliverable)
- `RESULT.md` (this file)

Reads read-only: `fable52_push/DD1_deduce_from_data/dd1_table.csv` (main rows).
One thread, `nice -n 10`, no downloads, under 0.2 s. Nothing was committed, pushed, deleted or
modified outside this lane's own folder.

---

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
