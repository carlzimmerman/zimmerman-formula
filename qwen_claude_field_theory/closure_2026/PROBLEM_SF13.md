# The exact problem: sf13

Self-contained. A new session should be able to work from this file alone.
Written 2026-08-19.

---

## 0. One-sentence statement

**Construct a bimetric interaction whose lapse Hessian vanishes identically, whose quasi-static
reduction is exactly the a₀-line, and whose acceleration scale is Carl's promotion — then check
whether its Hamiltonian constraint actually propagates.**

---

## 1. The framework (definitions you need, nothing more)

- **a₀ = κc√(Gρ_Λ) = c²√(Λ/32π)** = **9.3619e-11** m/s² (canonical) / **1.1279e-10** (alt).
  **Carry both footings on every dimensional number.**
- **κ = ½ is FITTED**, measured 0.529 ± 0.034. **Never call it derived.**
- **The a₀-line** (the phenomenology to be reproduced): g_obs² = g_bar² + a₀·g_bar.
- **The promotion** (Carl's contribution, and the novel part):

      a₀²(𝒬) = κ²G(−K(𝒬)),   K(𝒬) = −ρ_Λc²√(1 − (𝒬−𝒬₀)²/Λ_D²)

  the β=1 DBI kernel. 𝒬 = √(−g^{μν}∂_μφ∂_νφ) is the khronon's rate; on FRW, 𝒬 = φ̇.
  𝒬₀ pinned to 2.4e-3 – 1.46e-2 Mpc⁻¹. **Λ_D is unpinned** — a genuine free scale.
- The a₀–Λ *coincidence* is prior art (Milgrom 1983/1999; Blanchet & Le Tiec 2009; Pikhitsa
  2010; Klinkhamer & Kopp 2011) — **credit it**. The *identity* above is Carl's.

## 2. The target function — already derived, do not re-derive, do not substitute

Inverting the a₀-line gives the AQUAL interpolation and its free function in closed form
(`superfluid_2026/sf01` PART B, verified):

    mu(x) = (sqrt(1 + 4x^2) - 1) / (2x),          x = g_obs/a0

    F(z)  = (1/2)sqrt(z)sqrt(1 + 4z) + (1/4)asinh(2 sqrt z) - sqrt(z),     z = x^2

with `dF/dz = mu(sqrt z)`, deep-MOND limit **exactly (2/3)z^{3/2}** (AeST's own coefficient, no
fitted constant) and Newtonian limit `dF/dz → 1`.

⚠️ **A near-miss to avoid.** An external session proposed
`F = sqrt(X(X+a0^2)) - a0^2 asinh(sqrt X/a0)`, whose derivative is `mu = x/sqrt(1+x^2)`, and
claimed it reproduces the a₀-line. **It does not** — that is the *standard* MOND μ-function.
The residual is `x^2(x^2 - sqrt(x^2+1) + 1)/(x^2+1)^{3/2}`, equal to 0.207 at x = 1 and
vanishing nowhere. Both share the deep-MOND limit μ → x, so limit checks pass and the
*interpolation* — the part that is Carl's own content — is wrong. Note the shapes: **argument
1+4z (correct) versus 1+z (wrong).** Adjudicated in `sf12`.

## 3. Why this is the calculation (the chain that got here)

| result | file | verdict |
|---|---|---|
| Three necessary conditions on any host | DOI 10.5281/zenodo.22004372 | published |
| **Locality theorem** — the Sun sits at **0.67 of its own galaxy's MOND radius**, so between 1 AU and r_M the local field differs by 6.3e7 while the potential differs 1.5×, dark density 2.2×, dispersion 1.0×. **Any viable screening is a function of the local field.** | `superfluid_2026/sf06` | 10/10 |
| BIMOND + DBI khronon: R1/R3 by construction, ephemeris gap void | DOI 10.5281/zenodo.22015358 | published |
| Lapse-only Hessian test is the **wrong object** (BD is removed via a *shift* redefinition) | `superfluid_2026/sf10` | INCONCLUSIVE |
| For L ~ N·N̂⁻⁶·S, **det H = −(mixed)² ≠ 0** — a diagonal zero does not make a 2×2 Hessian singular | external SF11B, verified in `sf12` | correct; sf10 PART E **withdrawn** |
| **V = N·F(X) + N̂·B(X) with X lapse-free has every Hessian entry zero** | `sf12` PART D | real degeneracy |

So the only surviving architecture is the last row, and sf13 is: build it properly.

## 4. The construction to build

**Step 1 — the covariant foliation.** The khronon supplies one; it is a *field*, not a gauge
choice:

    n_mu = d_mu(phi) / sqrt(-(d phi)^2),      h_mu_nu = g_mu_nu + n_mu n_nu

**Step 2 — the relative geometry.** Keep BIMOND's object,
`C^a_bc = Gamma^a_bc(g) - Gammahat^a_bc(ghat)`, a genuine tensor.

**Step 3 — project it fully spatially with respect to n:**

    C_M^a_bc = h^a_d h_b^e h_c^f C^d_ef

**Step 4 — the scalar.** Build a quadratic contraction of `C_M` and normalise by the promotion:

    X = [ quadratic contraction of C_M ] / a0^2(Q)

**Step 5 — the interaction.**

    S_int = m^2 M_eff^2 * integral d^4x  N sqrt(h) [ F(X) + (Nhat/N) B(X) ]

with `F` the function of §2.

**Step 6 — why X should be lapse-free.** In unitary gauge (φ = t, legitimate because φ is a
dynamical field with a timelike gradient, so the adapted slicing exists) one has
`n_mu = -N delta^0_mu`, and the fully-projected `C_M` reduces to the ADM *spatial* components —
which contain `∂_i h_jk` and `∂_i hhat_jk` but **no lapse and no extrinsic curvature**.
**Verify this explicitly. It is the load-bearing step and it is where the construction can die.**

## 5. What sf13 must check, in order

1. **Lapse-freeness of X.** Compute `∂X/∂N` and `∂X/∂N̂` symbolically in unitary gauge. Must be
   exactly zero. If not, stop — the whole architecture fails and that is the result.
2. **Lapse Hessian.** `∂²V/∂N_A∂N_B` for A,B ∈ {N, N̂}. Must be **identically zero — all four
   entries**, not just the determinant, and not just the diagonal. (This is the trap that took
   sf10 down.)
3. **The quasi-static reduction.** Perturb both metrics, take the quasi-static limit, and show
   the field equation becomes

       div [ mu(|grad Phi|/a0) grad Phi ] = 4 pi G rho

   with **μ the function of §2**, and with a₀ = a₀(𝒬) from the promotion. Read off the exact μ
   rather than asserting the limits — matching only the deep-MOND and Newtonian ends is what let
   the wrong μ through in §2's warning.
4. **The secondary constraint.** ⚠️ **This is where the honest statement matters.** A vanishing
   lapse Hessian gives the *primary* constraint only. Ghost-freedom additionally requires a
   *secondary* constraint that (a) exists and (b) is preserved in time. **Do not assume this is
   inherited from Hassan–Rosen.** HR's published proof (JHEP 02 (2012) 126) applies to
   **non-derivative** potentials built from √(g⁻¹ĝ); the X here contains **spatial derivatives**,
   so it is *outside* that class and the secondary-constraint analysis is a fresh calculation.
   *(This corrects an overclaim in `sf12` PART D3, which said such a host "inherits the BD
   clearance." It clears the same first hurdle HR clears, and owes the rest.)*
5. **Both footings, every number.**

## 6. Success and failure conditions, stated in advance

- **PASS** = steps 1–3 all hold with the *correct* μ, and step 4 produces a secondary constraint
  that propagates. That is a closed, ghost-free relativistic host carrying Carl's a₀. Publish.
- **PARTIAL** = steps 1–3 hold, step 4 unresolved. Still a real advance: a lapse-degenerate host
  reproducing the a₀-line exactly, with one named owed calculation.
- **KILL** = X cannot be made lapse-free (step 1), or the reduction gives a different μ (step 3),
  or no secondary constraint exists (step 4). **A kill is a publishable result** — say which step
  and why.

Write it as `closure_2026/sf13_hr_potential_2026.py`, with numbered `[ok]`/`[FAIL]` checks,
exiting non-zero on failure.

## 7. The rules that have actually cost us

1. **Verify a "fails/deficit" claim as rigorously as a "works" claim.** Six errors in three days
   are logged in the top-level `RETRACTIONS.md` — roughly half manufactured deficits, half
   manufactured wins. Read them first.
2. **A partial-derivative zero is not a Hessian degeneracy.** Made twice in three files. Check
   the full matrix.
3. **Matching limits is not matching a function.** The wrong μ passed both its limit checks.
4. After removing a false kill, **re-run the other sectors before declaring survival.**
5. Every load-bearing claim needs a committed runnable script. No script, no claim.
6. Never say "no dark matter" — the slogan is **"no dark-matter PARTICLE."** Ω_dm is full here as
   a field's conserved shift charge; both the CMB pass and w = −1 depend on it.
7. Never say the theory is closed. Never modify `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`
   or any `*_HASH.txt`.
8. **Scope fence:** write only in `qwen_claude_field_theory/closure_2026/`. Read anything.
   Append to the top-level `RETRACTIONS.md` only to withdraw a claim.

## 8. What is already settled and must not be re-litigated

- The dust is **cold** at recombination (c_ad² ≈ 1e-9 c²) — the old "c_s² ∝ a⁻³, can't be cold"
  claim is **withdrawn**, the DBI wall turns it over (`sf08`).
- The dust **clusters like CDM** on every CMB scale, 100–900× Jeans margin (`sf09`).
- The promotion and a₀(z) are **host-independent** — they need only shift symmetry and FRW
  (`sf07` PART C).
- Still owed elsewhere, not part of sf13: a coupled-system Boltzmann run (decides growth rate,
  ISW, lensing potential); lensing Φ+Ψ; whether the 1e-3458.7 solar-system number is structurally
  robust or kernel-specific; formalising the locality *argument*; problem 2d.
