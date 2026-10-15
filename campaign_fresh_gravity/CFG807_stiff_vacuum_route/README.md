# CFG807: does the stiffened action revive "dark energy = the a₀-field's vacuum energy" (PAPER42)?

**Verdict (frozen rule): STILL BLOCKED.**
- As frozen, the label is BLOCKED-SOLAR, because one TNO check is mis-specified (see below).
- The real block is structural. The stiffness does lift the solar-system objections. But in the stiffened action the
  P-sector vacuum energy is not well-defined, and the PAPER41 turn-off cannot be written in it.
- Nothing in the action fixes the coefficient 4 (C = 16π). κ = ½ stays FITTED.

Criteria: `FROZEN_CRITERIA.md`, committed alone first (1d343d77b).

## Scripts

Both run in seconds:
- `nice python3 cfg807_solar.py`, with `CFG807_MUTATE=M1` for stiffness off
- `nice python3 cfg807_vacuum.py`, with `CFG807_MUTATE=M2` for a crippled detector

Both MUTATE runs bite.

## (1) Solar system, with the stiffness on (L* = 5.75 pc)

**S1 Cassini: PASS.**
- With a k = 2 phantom turn-off at y_t = 32, 64, 128.9 or 1000, Q2 is at most 3.6e-6 of the Park+2026 ceiling.
- Without a turn-off it is 3.5e-6, which reproduces CFG770.
- The turn-off changes Q2 by at most 4%. It only touches the Galactic background's response.

**S2 TNOs: FAILED as frozen.**
- The Sun's stiff response is a constant sunward 4.2e-15 m/s² (= GM/L*², 4.5e-5 a₀) from 30 to 10⁴ AU. Inside L* the
  turn-off cannot act at all.
- All 90 SBDB objects have anomaly apsidal periods of 118–170 Gyr. Under p56's turn-off, Sedna's is 0.02 Gyr.
- 89/90 precess at less than 0.04× the giant-planet rate. The exception is 2020 MQ53 (a = 13 940 AU). There the
  planets' quadrupole is itself negligible, so the ratio test was mis-specified.
- POST-HOC (declared after the first run; the verdict is NOT changed): measured against the larger of the planets and
  the Galactic tide, the worst object sits at 0.039.
- `cfg807_solar_firstrun.out` is kept.
- M1 (stiffness off): 90/90 objects are faster than the planets.

## (2) Vacuum energy and coefficient

- **V0 (sympy).** The Euler–Lagrange equations do not depend on an additive constant in W_rem. K W_rem″(0) = 0 for
  every such constant. γ is absent from the uniform state. So L*, γ and K cannot enter the vacuum energy.
- **V1.** Under PAPER42's premise ("no vacuum constant in strong fields"), the frozen W_rem gives an ill-defined answer
  in both available normalisations:
  - potential form: ε_W = −∞ (the log wall at u → a₀, AdS sign);
  - QUMOND-dual form: ε_Q = +∞. Here I(Y) = Y − ln Y + ½, exact, because the phantom saturates at a₀.
- **V2.** A finite ε_Q needs the phantom to return to zero at strong field. Then u(g_N) is non-monotone, so
  R = K W_rem′ is double-valued and no W_rem(u) exists.
  - Controls: the RAR kernel (finite 12.99, as in p21) and the turn-off are both non-representable.
  - For any continuous admissible R, ε_Q grows at least linearly (4 families). Whenever ε_W is finite it is negative.
- **V3.** L*, γ and K do not fix y_t:
  - c²/(a₀L*) gives y_t ≈ 5e9, which is ×1.7e8 off.
  - The point-mass screening edge (r_M/L*)² scales ∝ M/L*², so it is not universal.
  - K only sets the unit a₀²/K.
- **V4.** These numbers are hand-set, and they come from the QUMOND-dual form, outside S2. The coefficient is
  C(y_t) ≈ (π/2) y_t − log terms. C = 16π needs y_t = 33.98 (k = 2), 44.3 (k = 3) or 48.3 (k = 4), i.e.
  g_t = 3.2e-9 m/s² at the canonical a₀. A turn-off this low is not checked against SPARC for the simple-μ kernel.

## Reading
- The stiffness removes the solar-system objections to the vacuum route, for any turn-off.
- But the vacuum route needs a finite, positive zero-field energy. The polarization (W_rem) form of the stiffened action
  cannot supply one: the energy diverges, or comes out with the AdS sign.
- Reviving the route needs a new structure, such as an extra field or a multi-branch potential, plus a hand-set y_t.
  The coefficient 4 stays an input (D_kappa Route D).
- Cold energy is still required. There is no dark matter particle species. This is not "theory closed".
