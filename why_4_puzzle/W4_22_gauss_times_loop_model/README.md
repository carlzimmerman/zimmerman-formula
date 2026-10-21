# W4-22: Gauss stiffness × 3D one-loop cubic. π MATCHED, ½ NOT REACHED

**Bottom line.**
- **The model** takes gravity's own field-energy normalization for the Newtonian stiffness, C₂ = c⁴/(8πG). Its MOND cubic
  comes from a 3D one-loop, the zero mode of N light degrees of freedom whose mass is λ|∇Φ|: C₃ = N k_BT λ³/(12π). The vacuum
  ε is a separate tree-level constant.
- **Then R = (32πN²/9)·Y,** with Y = ε(k_BT)²λ⁶G³/c¹², a pure number. So **ξ = 1/(N²Y) and κ = 1/(N√Y), with no π
  anywhere.** At N = 2 the prefactor is **exactly 128π/9 = (8π)³/(6π)²**.
- **So the target's π is "Gauss cubed over a 3D loop squared".** κ² comes out π-free, as in W4-07's superfluid seesaw
  (κ² = α⁶) and W4-01's KK reading. What's new here is that the single π of 128π/9 is traced to where it comes from: two
  named factors, one Gauss and one loop.
- **But the 4 is not derived; it moves into N²Y = 4.**
  - Y is a ratio of three independent scales (ε, G, Tλ³), so this is a TRADE.
  - Reading N = 2 and Y = 1 gives κ = ½ = 1/N, which is the excluded H061 class (κ = 1/channel count).
- **And the family can't be MOND-shaped without losing the π.**
  - A tree quadratic plus a loop cubic is Newtonian at low field, the wrong way round.
  - Turning it round needs the loop's low-field quadratic to cancel C₂. That ties C₂ to the temperature and re-glues the π:
    ξ = π³NT⁴/(27ε), or 10π/3 with the loop's own vacuum.
  - The signs the cancellation needs (negative quadratic, positive cubic) are forbidden for stable states by the record's
    concavity principle. Only a periodic-fermion (−1)^F trace has them, and that is not a state.

**κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095). Not theory closed.

## In plain words

The target 128π/9 needs one π left over. Gravity's stiffness brings 8π, and it enters cubed. A one-loop cubic in three
dimensions brings 6π (for two degrees of freedom), and it enters squared. (8π)³/(6π)² = 128π/9 exactly, so the π works
out on the nose.

What's left is one plain number, N²Y, which has to equal 4. Nothing in the model fixes it. Worse, the model is the wrong
shape: it behaves like Newton at weak fields instead of MOND. The only way to flip that is to let the loop cancel gravity's
stiffness at weak fields. Doing so welds gravity's constant to the loop's temperature, the π comes unstuck again, and the
signs needed for the cancellation don't occur in any stable physical state.

## Results (`w4_22.out`)

| check | what | result |
|---|---|---|
| K0 | W4-21's three shapes | **one class**: common-factor (1,1,1) and field-rescaling (0,3,2) shifts span the kernel of (1,2,−3) |
| K1 | R and ξ for every N | R = (32πN²/9)Y and ξ = 1/(N²Y); at N = 2, 128π/9 = (8π)³/(6π)², weight 1 |
| K2 | units | Y is dimensionless: (kg, m, s) exponents (0, 0, 0) |
| K3 | the 4 | κ = c⁶/(N G^{3/2} √ε k_BT λ³) depends on every scale (TRADE). Y = 1, N = 2 gives ½ = 1/N: H061 |
| K4 | MOND shape | tree + loop is Newton-leading as h → 0. With the cancellation: ξ = π³NT⁴/(27ε) (weight 3) or 10π/3 (loop vacuum, R = 16/15) |
| K5 | sign | F(X) = aX + bX^{3/2} is concave only if b ≤ 0; the thermal cubic is −NTλ³/(12π) |
| I1, I3 | forbidden constants; scaling | pass. κ moves as A^{−3/2}B^{−1/2} under G → AG, ε → Bε (TRADE, expected) |

## Correction to W4-21 (K0)

W4-21 listed (1,0,0), (−1,1,0) and (0,−1,−1) as "three shapes that survive". The arithmetic is right, but they are **one
condition**. Two conventions leave R unchanged:
- multiplying ε, C₂ and C₃ by a common factor shifts the weights by (1, 1, 1);
- rescaling the field φ → π^g φ shifts them by (0, 3g, 2g).

Together these span every solution of wt ε + 2 wt C₃ − 3 wt C₂ = 0. The only invariant content is **wt R = 1**. An appendix
is added to W4-21's README. This model sits in that class written as (0, −1, −1).

## Screen and register

- **S1:** c enters through ε = ρ_DE c² and through c¹² in Y.
- **S2:** passes.
- **S3:** the cubic is the zero-mode threshold power h^n of n = 3; reported, not cleared.
- **S4:** none.
- **S6:** fails (ε is a free tree constant).
- **S7:** the N = 2, Y = 1 reading is H061.
- **Register class:** `free` (TRADE).

## MUTATE (`w4_22_MUTATE.out`, exit 1 by design)

- **MU1, N = 2 → 1:** the prefactor becomes 32π/9 and ξ = 1/Y. Bites.
- **MU2, 8πG → 4πG:** the prefactor becomes 16π/9 and ξ = 2/Y = 8/(N²Y). The weight stays 1. Bites.

## What would rescue it

Two things would both have to happen:
1. A **non-affine** coupling of the gradient to the loop sector, so that concavity doesn't fix the sign. The record's
   pointers are a Gauss-law constraint or a derivative current (W4-08 `GOAL_STATUS.md`).
2. A **separate** low-field switch-off of the Newtonian stiffness, one that leaves C₂'s Gauss 8π unglued.

Only then could the π match survive in a MOND-shaped, stable medium. Even so, N²Y = 4 would still need a named principle and
a second prediction.

## Files

- `FROZEN_CRITERIA.md`: committed alone, f0294ae1c.
- `w4_22.py`: sympy, single core.
- `w4_22.out` / `w4_22_results.json`: the normal run.
- `w4_22_MUTATE.out` / `w4_22_results_MUTATE.json`: the control run.
