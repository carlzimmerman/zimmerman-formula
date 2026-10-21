# W4-22: a model in W4-21's class — Gauss stiffness × 3D one-loop cubic (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-22 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Model-building lane. Footing **ρ_DE**. **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095, κ_crit = 0.345 ± 0.078; neither
value enters). Not theory closed.

## Question

W4-21 found that ξ = ¼ needs a medium ratio R = εC₃²/C₂³ with exactly one π (wt R = 1). Build the most natural model in
that class and see where it lands.

## K0: the three W4-21 "shapes" are one class (a correction to W4-21's reading, disclosed before any script)

Two conventions leave R unchanged and shift the weight vector (wt ε, wt C₃, wt C₂):
- a common factor: shift (1, 1, 1);
- a field rescaling φ → π^g φ: C₂ → π^{2g}C₂ and C₃ → π^{3g}C₃, shift (0, 3, 2).

These two shifts span the whole kernel of wt ε + 2 wt C₃ − 3 wt C₂. So (1,0,0), (−1,1,0) and (0,−1,−1) are one condition
written three ways. W4-21's listing is correct arithmetic, but "three shapes = three kinds of model" is wrong; the only
invariant content is wt R = 1. K0 checks the kernel claim symbolically, and an appendix is added to W4-21's README.

## Model M (every ingredient named)

- **M1. Newtonian stiffness with Gauss normalization:** C₂ = c⁴/(8πG), from the field energy g²/(8πG). With q = 1 the A1
  dictionary returns G_n = G. This is the convention (0, −1, −1) with G treated as π-free.
- **M2. MOND cubic from a 3D one-loop:** N light degrees of freedom whose mass is m = λh (h = |∇Φ|, Φ = potential/c²; λ
  dimensionless, m an inverse length). They sit in a 3D static reduction at scale k_BT: the zero Matsubara/KK mode.
  - The threshold term is T·m³/(12π) per degree of freedom, so |C₃| = N k_B T λ³/(12π).
  - The coefficient is W4-04 A2's (−γ^{3/2}θX^{3/2}/(12π) per boson, re-verified numerically in W4-21 K2c).
- **M3. Vacuum:** a tree-level ε = ρ_DE c², π-free, not tied to T.
- **A1 dictionary** (W4-04 PROOF §A) at n = 3: ξ = 8ΩC₂³/(9εC₃²) = 32π/(9R).

## Claims to check (hand expectations stated)

- **R1. π matched.** R = (32πN²/9)·Y, with Y ≡ ε(k_BT)²λ⁶G³/c¹². So ξ = 1/(N²Y), which is π-free. At N = 2 the prefactor is
  exactly 128π/9 = (8π)³/(6π)²: the target's π is "Gauss cubed over a 3D loop squared".
- **R2. The 4 relocates, it is not derived.** ξ = ¼ ⟺ N²Y = 4. Y is a ratio of three independent scales (ε, G, Tλ³), so
  κ = 1/(N√Y) is a TRADE. A posited Y = 1 at N = 2 gives κ = 1/N, which is the excluded H061 class (κ = 1/channel count).
- **R3. Shape no-go for the family.** A tree quadratic plus a loop cubic has the wrong ordering: C₂h² dominates as h → 0.
  - A MOND shape needs the loop's low-field quadratic to cancel C₂ at small h and the loop to decouple at large h.
  - The loop's low-field quadratic is N(k_BT)²λ²/24 (A2), glued to πT. Imposing C₂ = N(k_BT)²λ²/24 removes G.
  - With the tree ε, the result is ξ = π³N(k_BT)⁴/(27ε) (in units ħ = c = 1, λ absorbed as stated in the script), which is
    π-odd and never ¼ for π-free inputs.
  - With the loop's own vacuum, R = 16/15 (W4-04), so ξ = 10π/3.
  - So the π match and the MOND shape exclude each other inside this family.
- **R4. Sign.** For an affine mass-type source (m² ∝ X = h²) the loop cubic is ≤ 0: thermal −N T λ³/(12π). This is the
  record's inherited concavity principle (W4-08 `GOAL_STATUS.md`). It is checked here only as the elementary statement that
  F(X) = aX + bX^{3/2} concave on X > 0 forces b ≤ 0.
  - The opposite signs (negative quadratic, positive cubic, the ones R3's cancellation needs) arise from a periodic-fermion
    (−1)^F trace, which is not a stable state. Reported, not claimed as a model.

## Checks (`w4_22.out`; light single-core sympy)

- **K0:** the kernel of (1, 2, −3) on ℤ³ equals span{(1,1,1), (0,3,2)}, and the three W4-21 shapes differ by kernel vectors.
- **K1:** R1 symbolic. R = 32πN²Y/9, ξ = 1/(N²Y), wt R = 1 at rational Y. N = 2 gives 128π/9 exactly.
- **K2:** Y is dimensionless in SI. Base-unit exponents of ε(k_BT)²G³/c¹² are all zero.
- **K3:** R2. κ = 1/(N√Y) depends on Y (I2 dependence printed); N = 2, Y = 1 gives κ = ½ and is flagged H061.
- **K4:** R3. The ordering limit C₃h³/(C₂h²) → 0 as h → 0. With the cancellation imposed, ξ is π-odd with weight 3 (tree ε),
  and R = 16/15 for the loop vacuum.
- **K5:** R4. The concavity sign lemma, and the thermal cubic's sign from A2.
- **I-checks:**
  - I1: grep for §2 constants.
  - I2: symbolic dependence.
  - I3: under G → aG and ε → bε with Tλ³ fixed, κ moves, which confirms TRADE (expected).
  - I4: no law κ is read.
  - I5: no Friedmann.
  - I6: ρ_DE only.
  - I7: ħ-free (the zero-mode term is classical in T).
  - I8: weights printed.

## Entry screen (declared)

- **S1:** c enters through ε = ρ_DE c² and through Y's c¹².
- **S2:** passes (κ moves with Y).
- **S3:** the cubic is the zero-mode threshold power h^n of n = 3 spatial dimensions. The mechanism is tied to n = 3 and is
  reported, not cleared.
- **S4:** none (TRADE).
- **S6:** fails. ε is a free tree constant.
- **S7:** the Y = 1, N = 2 reading is H061.

**Option space Ω:** κ = 1/(N√Y), Y ∈ (0, ∞): class `free`.

## Mutation control (`W4_22_MUTATE=1`, separate `_MUTATE` outputs, exit 1 when the controls bite)

- **MU1. N = 2 → 1.** Expected: ξ = 1/(N²Y) → 1/Y at fixed Y; R's prefactor goes 128π/9 → 32π/9.
- **MU2. Einstein coupling 8πG → 4πG in M1.** Expected: R → (4π/9)·N²Y·… (prefactor halves cubed: ×1/8), so ξ → 8/(N²Y). wt R
  stays 1: still π-free, but the value moves.
- Both must move. A control that doesn't move voids the lane.

## Verdict (frozen)

- **π MATCHED, ½ NOT REACHED** if K1–K5 hold as stated. The family carries the target's π exactly but leaves the 4 as a free
  Y and cannot be MOND-shaped without re-gluing the π. Register as `free` (TRADE) with the shape no-go.
- **A MODEL OF ½** only if a named principle fixes N²Y = 4 and the MOND shape survives with a stable sign. Not expected.
- Any K failing is reported as is.

**Hand expectation:** π MATCHED, ½ NOT REACHED.
