# FINAL-1 FROZEN CRITERIA: the theory, assembled (2026-11-11)

ASSEMBLY lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled:
a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s^2. G = 6.6743e-11, c = 299792458, K = 4 pi G.
kappa = 1/2 FITTED; not theory closed. Cold dark energy is a gravitating field component, never a particle.
**Written before any FINAL-1 script exists and before any FINAL-1 number is computed.**

---

## Question

The diagnostic is landed, not open:

- T4 (exact, SMF1 S0b) + LFS1 (exact) cap the settled halo at the cold charge its clock carried in:
  **1.06 / 1.40 M_b** delivered, against **41.5 / 97.8 M_b** demanded at FLD1's actual KiDS window edges
  (272 / 637 kpc). (CRUX.md, CLOSURE.md.)
- The hot-gas escape is closed on both exits: the amount-fixing gas is a fixed column
  Sigma_gas = a0/(pi G x_b^2) = **6.1627 / 7.4477 Msun/pc^2** out to 2.6 Mpc, and putting that gas in g_bar
  pushes the outer points to **0.0392 +- 0.0069 / 0.0324 +- 0.0057** of the law, against the record's 0.891 gate.
  (GAS1: MISSING BARYONS EXCLUDED [AMOUNT AND AMPLITUDE].)
- His data prefer the **formation reading**: the non-baryonic mass is real, conserved, and its AMOUNT IS SET WHEN A
  SYSTEM FORMED (HIS1: 4 of 5 frozen statements; HIS1R regraded with separate code and got the same label).
  The force reading scores 1 of 5. (HIS1, HIS1R, DD1.)

FINAL-1 writes the theory that the record supports, in seven numbered pieces, with a lane cited for every claim:

1. the ontology, in plain words (what exists; no particle; dark mass is the sector's stress-energy);
2. the action, one term per line, each marked **FROM (A)** or **NEW**;
3. the conserved quantity and the epoch at which the amount is fixed;
4. the field equations;
5. the three regimes and what each looks like (expanding background, settled galaxy, cluster);
6. every empirical row the theory must satisfy, as a table with measured value and source lane;
7. the top five predictions it makes that are **not yet measured**, each with a number, a recipe and a falsifier.

It is an assembly. It grades nothing new about nature. What it grades is **its own arithmetic**: every number it
prints is either quoted from a landed lane (named) or computed here in SI from G, c and a0 (printed).

**Rule for missing numbers.** If a number a row needs is not on disk, the row is printed `UNAVAILABLE` with the
reason. Nothing is inferred, interpolated, recalled or invented.

---

## The objects (what is being assembled)

**Form B.** The a0 law with cold dark energy counted once:

    g_N = g^2/(g + a0);  g_c = g - g_N = a0 g/(g + a0) <= a0;
    M_c(<r) = M_b X(x), X(x) = (sqrt(1 + 4 x^2) - 1)/2, x = r/r_M, r_M = sqrt(G M_b/a0);
    deep field rho_c = a0/(2 pi G r); weak field rho_c = sqrt(G M_b a0)/(4 pi G r^2), v_inf^4 = G M_b a0.
    a0 = kappa c sqrt(G rho_Lambda) = c H_Lambda / Z, kappa = 1/2 FITTED, Z = 2 sqrt(8 pi/3) = 5.7893.

**Action (A)** (QX17, certified):

    S = Int sqrt(-g) { [R - 2 Lambda + 2 mu_K^2 (Q - 1)^2]/(4K) + P^m A_m - W(K|P|) - gamma_L F(Pi) + lambda n^m P_m } + S_m
    W(p) = (a0^2/K)[-p/a0 - ln(1 - p/a0)], F(Pi) = [max(Pi,0)]^2/2, gamma_L = K Lstar^2/2,
    Q = sqrt(-g^{mn} d_m tau d_n tau), n_m = -d_m tau/Q, A_m = n^n nabla_n n_m, Pi = D_m P^m.

**The formation reading** (FRM1, from HIS1/HIS1R): three objects **Q** (the ratio fixed at formation,
X_f = X_L(g_b,f)), **C** (the conserved non-baryonic charge M_C, plus the separately conserved baryons M_b, moved
only by transport: f_C, f_b), **E** (the epoch: baryon assembly; a0 does not run because rho_DE is constant), and
the master equation

    X = X_f (f_C/f_b),  d = Y - Y_L(g_bar) = log10[(1 + X_L(g_b,f) f_C/f_b)/(1 + X_L(g_bar))].

---

## Graded arithmetic checks (each PASS/FAIL; per footing, never pooled)

Every quantity below is printed in SI in `final1.out` with its unit.

- **A1 identities (footing-free).** On DD1's frozen table (main rows only), per point: `x = r/r_M`,
  `u = a0/g_bar`, `X(x) = (sqrt(1+4x^2)-1)/2`, `M_c = M_b a0/g`, `u = x^2`. All four must hold to 1e-10
  relative on every point, both footings.
- **A2 the deep column.** `a0/(2 pi G)` in Msun/pc^2 must print **106.9** (canonical) / **129.1** (alt) to
  0.05 Msun/pc^2; `a0/(pi G x_b^2)` with `x_b^2 = 5.41 x 6.41` must print **6.1627** / **7.4477** Msun/pc^2.
- **A3 the ceiling curve.** `d_max(u) = log10[(1+u)/(1+X_L(u))]`, `X_L(u) = (sqrt(1+4u)-1)/2`. Must be
  strictly increasing in u over u = 1e-3 .. 1e6, and `d_max/((1/2) log10 u) -> 1` to within 1 % at u = 1e4.
- **A4 the ledger, per class.** From DD1: median `u`, median `X = g_obs/g_bar - 1`, median `Y = log10(g_obs/g_bar)`,
  median `d = Y - Y_L`, `d_max` at the class's median u. Print per class per footing. Reachability: a class is
  **reachable** iff its median `X` ≤ `u` (then solve `X_L(u f_b)/f_b = X` for `f_b` at `f_C = 1`); otherwise print
  `UNREACHABLE` and the shortfall factor `X/u`.
- **A5 the amount cap.** At FLD1's KiDS window radii (272 / 637 kpc) and log M_b = 10.45, recompute `x = r/r_M` and
  the demand `X(x)`; against a delivered 1.06 and 1.40 M_b and against the cosmic budget 5.41. Print per footing.
- **A6 the three regimes.** For log M_b = 10.45 print: `r_M`, the radius where X = 1 (`x = sqrt(2)`), the budget
  radius `x_b r_M`, PD1/ONE1's truncation radius `x_t r_M` with `x_t^2 = X_f(X_f+1)` at X_f = 59.5, and check the
  ordering `r_M < sqrt(2) r_M < x_b r_M < x_t r_M`. Both footings.
- **A7 the epoch.** Print the age of the universe at z = 0.05, 0.45 and 0.90 with H0 = 67.4 km/s/Mpc,
  Om = 0.3153, OL = 1 - Om, and the ratio t(z)/t(0).
- **A8 the three-way discriminator (P4).** Print, for each of the three readings, the predicted value of
  `Delta d = d(z = 0.45) - d(z = 0.05)` at matched g_bar and matched aperture:
  formation + constant a0 → **0.000**; time-proportional source (X_src ∝ t) → `log10[t(0.45)/t(0.05)]`;
  force reading → **0.000** with both individual values 0. The three must be distinguishable at 3σ given the
  record's per-class se ~ 0.02-0.03 dex.

Printed, not graded: the master-equation inversion for `f_C` at fixed `g_b,f = g_bar/f_b` with `f_b` taken from the
standard picture for the hosted classes, for comparison with FRM1's table.

---

## MUTATE (`final1_MUTATE.json` / `.out`; each arm must change its stated outcome, else disclosed)

- **M1 the force reading.** Replace the formation reading by the plain law now: set `d := 0` for every system
  (equivalently `X := X_L(g_bar)`), then rerun A4. Required: the count of classes whose median offset falls outside
  its pre-registered band goes from **2** (formation) to **>= 6**, and the count of classes with `f_b` differing from
  1.000 by more than 0.05 goes from **>= 10** to **0**.
- **M2 a0 x 2 (both footings).** Required: every footing-free row (x, u, X, d, d_max, ratios) is bit-identical, while
  `r_M` scales by 2^(-1/2) `= 0.70711` (to 1e-5) and the deep column by 2.0000 (to 1e-5).
- **M3 class labels shuffled across systems (seed 20261110; the bands stay with the class names).** Required: the count
  of classes inside their pre-registered band falls below 13.
- **M4 the ceiling removed** (allow `f_b -> 0` without limit, i.e. drop the saturation bound). Required: the count of
  UNREACHABLE classes goes **2 -> 0**, and prediction P1 must be reclassified from VIOLATED to VACUOUS.

---

## The five predictions: pre-registered form

Each is printed with (a) the **number** the theory gives, (b) a **recipe** that says exactly what to compute from
what data, (c) a **falsifier** with a threshold and a significance. None of the five has been graded by a lane of
the record; each names the lane that supplies the inputs and the lane, if any, whose gate it would land on.

1. **P1 the ceiling.** `d <= d_max(u)` for every system, with `d_max` the exact saturation of the baryon-loss
   channel. Number: the curve, plus its value at each class's median u.
2. **P2 the floor.** Second-generation baryons carry no charge: `X = 0.000`, at every radius, not just on average.
3. **P3 the accretion deficit.** A system still assembling baryons sits at `d = -(1/2) log10 f_b` with `f_b > 1`;
   the faint rotators require `f_b ≈ 3`.
4. **P4 epoch invariance.** At matched g_bar and aperture, `d` is independent of the observed epoch; the three-way
   discriminator of A8.
5. **P5 the gas column.** The formation reading requires NO amount-fixing hot gas around isolated L* galaxies;
   GAS1 fixes the number a measurement would have to beat.

---

## Record checked first (quoted, not redone)

- CRUX.md, CLOSURE.md, ANALYSIS_2026-11-11.md, EXITS.md (`hy4_preview_push/`).
- fable52_push: CLOSURE.md, README.md, EQ1/EQUATIONS.md, DT1/DESIGN.md, FRM1/FROZEN_CRITERIA.md + RESULT.md,
  HIS1/RESULT.md, HIS1R/*, SHP1, ONE1, TPA1, SCS1, SCS2, MK1, MK2, COL1, FLD1, REL1, HE1, SWT1, DD1.
- closure_2026_11_10: MEDIUM_DESIGN_2026-11-10.md, THEORY_ASSEMBLED_2026-11-10.md, AMT1_amount_budget,
  VSH1, CLS1, LFS1, GO1, DG1, XCV1, NH2, KL1.
- closure_2026_11_09: PD1, RB1, RB2, CO1, CO2. closure_2026_11_06: QX17.
- GAS1 (this push) for Sigma_gas and the amplitude kill.

## Doors already closed — not re-run, not re-proposed

Spatial switches on the law (SWT1, EMV1, GAL1, KO1, KO1R, SNP1, HE1); one-variable dust terms (MK1, MK2
NO VALUE); expansion-keyed (TK1 BREAKS AT TURNAROUND); acceleration-keyed (AKS1 T1, AKD1 BREAKS AT A1);
cold-clock collapse (COL1 BREAKS DOWN); relative-acceleration law (REL1); leafwise flux (LFS1 ILL-POSED);
dissipation (AKS1 CLOSED); parent actions (PAR1, WV1, SMF1); contact opacity (NBC1 KILLED); DE clock (KDE1);
warm component (GRW1); held edge layer (EDG1); isotropic P = J (SET1); any local momentum-conserving
normally-self-gravitating medium (M5 NO-GO); missing baryons (GAS1).
**This lane does not open any of them. It writes down what survived.**

## Disclosures (seen before this file)

Every RESULT.md, FROZEN_CRITERIA.md and .out file named above. No FINAL-1 number of any kind exists at the time this
file is written.

## Operational

One thread, `nice -n 10`, no downloads, seconds. `final1.py` -> `final1.json` / `final1.out`;
`final1.py --mutate` -> `final1_MUTATE.json` / `.out`. Reads `fable52_push/DD1_deduce_from_data/dd1_table.csv`
(main rows only) read-only. Append-only: new files only; nothing is committed, pushed, deleted or modified outside
this lane's own folder.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
