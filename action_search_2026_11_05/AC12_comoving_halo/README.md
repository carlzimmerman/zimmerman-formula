# AC12: the Sun's own charged halo — partly dragged, subsonic at 1 AU, but not self-consistent; moving Sun stays NO VERDICT

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (4db782ee4e), frozen
before any graded number. Script: ac12.py (sympy + DOP853, about 1 s, one thread, 0.12 GB). v3s (s = 0) and
AC2q are run side by side, on both footings, never pooled. Astra's AZ37 is read only.

## The question

AC11 found that the Sun's own static khronon charge, q_sun = Phi_N/gamma, dominates the Galactic rho0 inside
r_eq = 1,007-1,562 AU. So the AU-scale test that AZ37 and AC11 ran, on a frozen Galactic background, used the
wrong background. AC12 asks whether the khronon's own equation drags that halo along with the Sun.

## Results

- **H0: the sigma equation is charge continuity**, d_t q + div(q v) = 0, with v = -grad sigma (exact, sympy).
  In the Sun's frame, a stationary charge pattern needs div(q w) = 0 for the relative flow w = v - V.
  Writing w = V grad(u cos theta), this becomes q(u'' + 2u'/r - 2u/r^2) + q'u' = 0, with u -> -r at infinity.
  - In units x = r/r_eq, with q = rho0(1 + 1/x), the problem is universal.
  - Inside the 1/r halo, u ~ r^sqrt(2), so the relative flow grows as r^(sqrt(2) - 1). KA2 measures the
    slope as 0.414211 against 0.414214.
- **H1: the halo is partly carried with the Sun.** The relative flow is f = |w|/V:

  | Radius | f |
  |---|---|
  | 1 AU | 0.064-0.076 |
  | 9.58 AU | 0.16-0.19 |
  | r_eq | 0.889 |

  Across the Lstar sets and both footings, that is 14-28 km/s at 1 AU for V = 220-369 km/s.
- **H2: the local phase speed is the Keplerian speed.** With the correct local charge, c_ph^2 = gamma q c^2 =
  v_K^2 + c_gal^2: 29.8 km/s at 1 AU, 9.65 km/s at 9.58 AU, and 1.07-1.33 km/s at r_eq. AZ37 and AC11 had
  753-938 m/s, which is the Galactic-only value.

  | Radius | Mach | Resonance |
  |---|---|---|
  | 1 AU | 0.47-0.94 | absent locally (subsonic) |
  | 9.58 AU | 3.7-7.4 | present |
  | r_eq | 147-308 | present |

- **H3: the kinematic halo is not self-consistent.** In the Sun's frame the flow's Bernoulli term,
  |w|^2/2, is not small next to Phi_N:
  - B = 0.093-0.38 at 1 AU. Only the V = 220 km/s, Lstar 21.68 pc canonical cell is below the 0.1 line.
  - B = 5.7-23 at 9.58 AU.
  - B = 1e4 or more at r_eq.

  The flow therefore reshapes the charge that it carries, and the halo needs a nonlinear, Bernoulli-coupled
  solve. This holds for every cell in both theories.
- **H4: capped bounds at the planets (reported, conditional).**
  - Matching-region tide, assuming the response there is at most the local charge: <= 4.3e-17 / 4.9e-17 g_N at
    1 AU and <= 3.8e-14 / 4.3e-14 at 9.58 AU.
  - Screened metric effect of a flow-induced charge of size max(B, 1) q_sun: <= 1.0e-13 / 9.0e-14 g_N at 1 AU and
    <= 2.1e-10 / 1.8e-10 at 9.58 AU.

  These hold only if the nonlinear response stays at that size, which AC12 does not prove.
- **v3s and AC2q agree** to every digit printed: eps = s^2/rho0 is about 4e-6.

**Label: NO VERDICT** on the complete moving Sun, by AZ37's lines, for both theories. AC12 does not change the label;
it sharpens it.
- AZ37/AC11's AU-scale resonance is an artefact of the wrong background. At 1 AU the true local flow is subsonic.
- The resonance is real at 9.58 AU and at r_eq.
- The halo inside about 10 AU cannot be treated kinematically.

No physical inconsistency appeared: c_ph is real everywhere and a regular solution exists. No alpha_1 or alpha_2
is claimed.

## Checks, known answers, control

- PASS: H0, KA1_f (halo off gives f = 1 to 2e-10), KA1_cph (halo-off phase speeds against AC11's stored JSON on
  24 rows, 2.2e-16), KA2, H1_conv (3e-10 against 1e-6).
- **H1_fit FAILS as frozen.** The two-term far-field fit on [50, 200] spreads by 4.95e-3 against the 1e-4 line,
  because q is still 0.5-2 % non-uniform there. This failure stays on the record, and the script exits 1.
  A post-freeze diagnostic on [2e3, 1e4] (spread 1.3e-4) moves alpha by 3.0e-3. That rescales f and Mach by 0.997
  and B by 0.994, and no label changes. The nearest margin, B = 0.093 against 0.1, survives.
- MUTATE (AC12_MUTATE=1, q'u' sign flipped, ac12_MUTATE.*): the inner slope becomes -0.267949 = sqrt(3) - 2, and
  KA2 fails. The control bites.

## Still open

A nonlinear, Bernoulli-coupled solve for the Sun's co-moving halo inside about 10 AU, a supersonic matching to
the Galactic flow from about 10 AU out to r_eq (a bow-shock-like region, Mach 4-300), and the metric response
that would give alpha_1 and alpha_2. The same calculation is open for v3s and for AC2q.
