# SWT1 RESULT (criteria 4d86f4d107, amendment A1 4af87eb9c0)

**SWT1-CP: KEY-DEPENDENT / KEY-DEPENDENT. SWT1-WP: NOT A NO-GO AS FROZEN / NOT A NO-GO AS FROZEN.**

TEST lane, quarantined. Adopts nothing and relabels nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled
(canonical / alt below). Every known answer passes, every MUTATE arm bites, and the Lean file compiles with standard axioms only.

The lane asks two things about any switch on the law that comes from an action (S multiplying the law's Lagrangian J).

## 1. Compensation (T1, T2): WL1's population statistic is not the lensing source of such a switch

- **T1, exact (Lean).** For a spherical switched law the effective enclosed mass r^2 g / G is M_b nu(y) inside the switch radius and
  exactly M_b outside it. The switch surface carries a layer of -M_b (nu - 1). From outside, a law-on region shows only its baryons.
- WL1 stage 2 summed the phantom each host retains and counted it as mass at bias 1. The solver here reproduces that statistic to
  1.5e-4 (0.9361 / 1.0792 for WL1's graded reading, 0.3843 / 0.4228 for its self-consistent one).
- **The compensated statistic.** Law-on regions act on long-wavelength sources as inclusions with the law's incremental permittivity
  (radial u (2 + u) / (1 + u)^2, tangential u / (1 + u)). Their polarizability is -0.43 to -0.50, close to the insulating limit -1/2.
  The large-scale lensing amplitude rises by q_C = 1 / mu_M - 1 (Maxwell-Garnett). Lean bounds it by (3/2) f / (1 - f) for filling f,
  so WL1's line 0.0354 is met only if **f <= 0.0231**.

| reading at z 1 (WL1's graded epoch) | filling | q_C + form factor | line 0.0354 | WL1's own statistic |
|---|---|---|---|---|
| **L**, law-on turnaround, baryons only (WL1's graded reading) | 0.170 / 0.196 | **0.303 / 0.361** | **FAIL** (x8.6 / x10.2) | 0.936 / 1.079 |
| C, ceiling | 0.70 / 0.81, not dilute | at least 0.64 / 0.65 | FAIL | 1.50 / 1.73 |
| NC, self-consistent (Newtonian collapse outside the switch) | 0.0124 / 0.0124 | **0.0180 / 0.0182** | **PASS** | 0.384 / 0.423 |
| NL, self-consistent, baryons only | 0.0019 / 0.0019 | 0.0026 / 0.0026 | PASS | 0.203 / 0.224 |

z 0.5 and 2 read the same way (L 0.37 / 0.44 and 0.18 / 0.21; NC 0.015 and 0.020). The form-factor term is 5e-5 to 4e-2 throughout.

**Reading.**
- WL1's FAIL stands on the reading it graded: L still fails by about 9-10x, on the correct statistic, instead of 26-30x.
- WL1's scope sentence, that the kill "holds for any arm-(i) key" because it "depends only on the phantom retained inside the
  KiDS range", does not hold for a variational switch. The statistic depends on the volume the law-on regions fill. The
  self-consistent reading WL1 reported as 11x over the line passes by a factor of 2.
- **What replaces it (reported).** Keeping the law on down to KiDS's lowest tabulated acceleration (g_bar 1.38e-15 m/s^2, 0.50 to
  2.83 Mpc for log M 9.4 to 10.9) around every lens with log M* >= 9.4 needs a filling of 0.29 (Poisson union 0.25), 12.6 times the
  allowance. The allowance lets the law reach **0.43 of that radius, g_bar >= 7.5e-15 m/s^2**. Fixed radii: 0.43 Mpc needs 0.003,
  1 Mpc needs 0.038, 2.8 Mpc needs 0.83.
- So the conflict in arm (i) is real, but it is between KiDS's outermost three or four points per bin and the filling, not between
  the population's phantom mass and the lensing line.

## 2. Wall pressure (T3): exact, and the self-clearing gate does not close the class

- **Identity, exact (Lean, and KA-W3 by direct bookkeeping of the full Lagrangian to 3e-9).** At fixed displacement y (the sources'
  Newtonian field at the wall, in units of a0) the outward force per unit area on whatever carries the switch is

      p_wall = (a0^2 / 4 pi G) W(u),   W(u) = u - ln(1 + u) - u^2 / (2 (1 + u)^2),   u = nu(y) y.

  It equals (a0^2 / 8 pi G) F(y) with F' = 2 y (nu - 1), the law's own field energy at fixed sources. Lean: W' = u^2 (2 + u) /
  (1 + u)^3 = (u - y) dy/du, 0 <= W <= y, and W <= (2/3) y^(3/2).
- **Sign.** The law's term enters its action as +S J, so a carrier that lowers S is pushed out of high-field regions. SQ1 graded
  the source's stated Lagrangian (-U_Q S, attraction), which has the opposite sign to the law's own term; the sign SQ1 reported
  as a bracket is the law's. M-W confirms that flipping the sign flips the force.
- **Gate as frozen (A1 pressure).** Carrier: the record's cosmic share R M_b, isothermal out to WL1's self-consistent radius
  (0.26-0.83 Mpc), chosen as the most diffuse placement the record allows.

| log M_b | p_wall / p_d at 30 kpc, 100 kpc, R_h (canonical) | alt | uncleared inside 200 kpc (line 0.9 M_b) | share multiple at which clearing fails |
|---|---|---|---|---|
| 9.4 | 19.4 / 10.4 / 5.0 | 21.4 / 11.4 / 5.4 | 0.001 M_b | 2.8 / 3.0 |
| 10.45 | 15.6 / 10.9 / 3.3 | 17.3 / 12.0 / 3.6 | 0.002 | 3.3 / 3.5 |
| 10.7 | 14.4 / 10.7 / 3.0 | 16.0 / 11.9 / 3.3 | 0.002 | 3.5 / 3.8 |
| 10.9 | 13.3 / 10.5 / 2.8 | 14.8 / 11.6 / 3.1 | 0.003 | 3.8 / 4.0 |

  Every mass clears on both footings, so the label is **NOT A NO-GO AS FROZEN**. My pre-freeze expectation (a no-go) was wrong; A1
  recorded the correction before any number.
- **Reported brackets.**
  - Groups and clusters (baryons enclosed in proportion to r, share in the same sphere): p_wall / p_d is 0.07-0.26 in a group and
    0.02-0.11 in a cluster. The same field stress that exceeds the share's pressure around galaxies by 3-20x falls short of it in
    groups and clusters by 4-40x. No constant was added to get that ordering.
  - Carrier B, a halo on the law's own Tully-Fisher line (the halo a single-counting reading needs): the ratio never reaches 1
    (maximum 0.48; 0.29, 0.12, 0.04 at 3, 10, 30 MOND radii). Such a halo cannot be cleared.
  - Ram-pressure bracket: divide the galaxy ratios by 4; they stay above 1 at 100 kpc (2.6-3.0).

## 3. Post-freeze extras (swt1_extra.py; reported only, no label rests on them)

- **E1.** The polarizability solver against a coated sphere's closed form: 1e-11.
- **E2, concentration.** The same share confined to R_h / 2 still clears. Confined to R_h / 4 it leaves 1.3-2.0 M_b inside 200 kpc
  for the three heavier bins (canonical; 0.7-1.5 alt) against the 0.9 line; at R_h / 8, 2.3-5.4 M_b. So the field stress clears a
  share that is still at turnaround scale, and is marginal to short against one that has settled to a quarter of that radius.
- **E3, bubbles held by pressure balance, at the 59 KiDS points.** The wall sits where p_wall equals the pressure of mean-density
  component with the stated dispersion. Projected 4 G DeltaSigma with the law inside, the compensated field outside and the
  swept-up component in a shell; chi2 from the Fig. 9 per-point errors only (no covariance, no hot-gas term; a pointer).

| dispersion | filling at z 0 | q_C | reach / KiDS's outermost radius | KiDS points outside the wall | chi2, law -> bubble (canonical) |
|---|---|---|---|---|---|
| 17.5 km/s | 0.167 / 0.183 | 0.295 / 0.331 FAIL | 0.84 / 0.87 | 4 of 59 | 279 -> 284 to 311 |
| 35 km/s | 0.042 / 0.046 | 0.064 / 0.070 FAIL | 0.53 / 0.54 | 12 | 279 -> 383 to 406 |
| 52.5 km/s | 0.018 / 0.020 | 0.027 / 0.030 PASS | 0.40 / 0.42 | 16 | 279 -> 484 to 506 |

  No dispersion passes both: bubbles small enough for the lensing line leave 16 KiDS points outside the wall and cost about 200 in
  chi2; bubbles that hold KiDS fail the line by about 8x.

## 4. Checks

- **Known answers, all PASS.** KA-CP1 1.5e-4 / 7.0e-4 / 1.4e-4 / 4.1e-4; KA-CP2 exact; KA-CP3 2.1e-9 outside, nu recovered inside;
  KA-W1 1.5e-10; KA-W2 0.99963 and 0.99913; KA-W3 3.3e-9, outward.
- **MUTATE, all bite.** M-CP: counting the phantom as exterior mass fails the line on every reading (0.20 to 3.5). M-W: the flipped
  sign gives an inward force at all four radii. M-WP: as frozen (pressure / 100) it has no power once the gate clears, disclosed;
  the added arm (pressure x 100) stops every mass from clearing.
- **Lean.** SWT1.lean: 19 theorems, `exit 0`, axioms propext, Classical.choice, Quot.sound only (compile.txt). SWT1_MUTATE.lean:
  five false versions, six errors, `exit 1` (compile_MUTATE.txt). T1 and T3's identity are certified, so both labels stand.

## 5. What the lane does and does not show

- It does not complete the theory, and it grades no mechanism.
- It replaces a statistic. The record's "population-phantom bound" should read: a variational switch may keep the law on in at most
  2.3 % of space, which reaches 0.43 of KiDS's range.
- It removes a general reading of SQ1. The law's field stress has the sign and the size to clear the record's share from around
  galaxies and not from groups or clusters. What SQ1 showed is that one screening function does not deliver it; and E2 shows the
  margin closes once the share has settled.
- The class "law on in cleared regions, component elsewhere" therefore stands or falls on one conflict, now with numbers: KiDS's
  points below g_bar 7.5e-15 m/s^2 against the lensing allowance.

## Files

FROZEN_CRITERIA.md, AMENDMENT_A1.md, swt1.py -> swt1.json / .out, swt1_MUTATE.json / .out, swt1_extra.py -> swt1_extra.json /
.out, SWT1.lean, SWT1_MUTATE.lean, compile.txt, compile_MUTATE.txt. One thread, 36 s, under 0.2 GB. Lean compiled with
`lake env lean` from the copy of fable_independent_2026/lean_2026 that has its Mathlib build.

Not registered: the closure register belongs to the orchestrator. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
