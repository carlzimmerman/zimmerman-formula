# T10 — the settling-flattening theorem

**The synthesis the campaign's own results force:** the JKO settling (T3)
and the rotation-curve kinematics (T1/T9) are the SAME statement in two
variables. The phantom's uniform μ-state is both the deep target the flow
converges to AND the exact-flatness condition of the curve.

## The theorem (7/7 checks PASS, rc 0; MUTATE flips C1+C2, rc 1)

**(S1) The settling IS the heat equation — exactly.** With μ := r²ρ, the
deep-target JKO flow (drift ∇logρ_ph = −2r̂/r) reduces by substitution to

    ∂ₜμ = ∂²μ/∂r²        (pure Neumann heat flow; drift terms cancel identically)

Symbolic check (sympy, two test functions): residual ≡ 0. Numeric
cross-check (4th-order differencing, N = 1000→2000): maxdev = 2.6e-6,
convergence factor 0.071 (quartic). The first-mode rate is π²/t_dyn —
the 9.87 of T7's STRUCTURAL keep — so the "why ×353?" question's answer
is unchanged: the π² mode is the rate, λ is the damping. Full-kernel
target: the cancellation is exact only in the deep regime (∇logρ_ph =
−2/r̂·(1 + O(r_t²/r²))); the residual is sub-leading there and O(1) only
at r ~ r_t, where the settled state is already uniform.

**(S2) Rotation curves are running μ-averages.** Newton's integral in
spherical symmetry: v²(r) = (4πG/r)∫₀^r μ(s)ds — verified to 1e-9 on 200
random profiles; μ ≡ const ⇔ exactly flat (flat_c = 3.2e-16 vs a 10%
μ-tilt giving a 4.9% curve variation). **Flatness is a μ-statement, not
a force-statement.**

**(S3) Deep-MOND is the uniform μ-state.** From the Lean-certified closed
form: μ_ph = r²ρ_ph = √(GMa₀)/(4πG) is CONSTANT (certified:
`mu_ph_is_constant`), and v_flat² = 4πGμ_ph ⇒ v⁴ = GMa₀ with the
16π²G²-cancellation exact (certified: `v4_from_uniform_mu`). The deep
rotation curve is flat *because* the phantom's μ is uniform.

**(S4) Area law:** M_ph(<r) = 4πμ_ph·r — the phantom halo is a 2-D screen
(mass ∝ radius), the geometric face of the ½-elasticity in T9.

**(S5) The falsifier — diffusive relaxation.** A baryonic μ-bump of width
ℓ relaxes at τ ∝ ℓ² (measured exponent 1.986 across ℓ = 1–8 kpc; first
mode e^{−π²Dt/r_out²}). Prediction: RAR-scatter bumps below ~10 kpc
relax on ~10⁸–10⁹ yr timescales, imprinted in the SPARC residual
radial-correlation structure as the heat kernel — a memory of the
settling, not white noise.

**(S6) P3-radius corollary — a new radius from the cosmic share.** The
kernel-exact mass law M_ph(<r) = M_b/(e^{r_t/r} − 1) reaches the cold
fluid's universal share 5.36 M_b exactly at

    r_supply = r_t / ln(1 + 1/5.36) = 5.8457 r_t

(C7, Lean-certified `supply_mass_exact`): **71.4 kpc** (MW, canonical),
**65.0 kpc** (alt), **714 kpc** for a 10¹³ M_b cluster — inside R500,
which is exactly why clusters present with their full cosmic share (P4)
while spiral galaxies below ~1e12 M_b are supply-limited at their
truncation. The share, the radius, and the completeness are one equation.

## Corrections to the freeze (dated, on top — no history rewrite)

- C7: 5.8480 → 5.8457 (hand-arithmetic slip in the frozen value; formula
  unchanged). Verified: 1/ln(1 + 1/5.36) = 5.84577.
- C8: the declared MUTATE flip set included C6; the bump relaxation is a
  pure-heat experiment and never sees the drift coefficient. Corrected
  declaration: MUTATE flips exactly C1 (symbolic residual ≠ 0) and C2
  (maxdev 1.7e-2 vs 2.6e-6 main) — verified empirically.

## Lean certificate (`../lean_certs/cert_settling_flattening.lean`)

Zero sorry, axioms = {propext, Classical.choice, Quot.sound}:
`mu_ph_is_constant` (r²ρ_ph const), `v4_from_uniform_mu` (v⁴ = GMa₀),
`supply_mass_exact` (1/(e^{ln(1+1/5.36)} − 1) = 5.36). The S1 substitution
is calculus and rides in the lane (sympy + numerics), per house pattern.

## Bottom line

The T9 elasticity (mass-response face) and this theorem (kinematics face)
are dual views of one object: the uniform-μ phantom state. One law, two
faces: ε(0) = ½ answers "how does the mass respond?", v⁴ = GMa₀ answers
"why is the curve flat?", and r_supply = 5.8457 r_t answers "where does
the share live?". All three certified; all three falsifiable.