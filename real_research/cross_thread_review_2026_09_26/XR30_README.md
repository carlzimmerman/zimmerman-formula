# XR30 — one clock or two?

The derivation chain now carries two global time structures:

- **the khronon's CMC foliation.** FP14 takes c₂ → ∞, which turns the leaf-averaged term into the multiplier term
  −2μ(K − ⟨K⟩_h). Every leaf then has K = ⟨K⟩_h, so the leaves are constant-mean-curvature (York-time) slices.
- **the unimodular clock.** XR20 T1 adds the Henneaux–Teitelboim (HT) term: Λ → Λ(x) plus 2Λ ∂_m T^m, with α = α(Λ).
  dΛ = 0 is then a field equation, Λ is conjugate to the four-volume time T, and a₀ = κ c √(G ρ_Λ) holds on every solution.

Are they one structure? This lane varies the actual action (FP14's zero-knob root at λ = 0 plus XR20's T1 term) in
minisuperspace, in FRW plus perturbations, about Minkowski, and in a Hamiltonian (Dirac) analysis on a lattice.

Script: `XR30_one_clock.py`. It writes `XR30_one_clock.out` and `XR30_one_clock_results.json`, and the `_MUTATE` versions.
Nothing outside this folder was edited. **κ = ½ stays fitted (equivalently Z = 5.7888); nothing here derives it. The closure
target stays open.**

## The answer: no merge

The two structures cannot be written as one term. Three facts, each computed, prove it.

1. **They have different Poisson-bracket classes** (D2, lattice).
   - HT's local constraints (∂_iΛ ≈ 0 and π_X ≈ 0) are **first class**. Their bracket rows vanish identically.
   - The CMC constraints are **second class**. Their bracket block with π_μ has rank N_L − 1, full on the non-zero modes.
   - The rank of the bracket matrix is a canonical invariant, so a first-class family cannot be identified with a
     second-class one.
2. **They live in complementary sectors** (M1).
   - The CMC condition has **no global part**: Σ_j v_j (K_j − ⟨K⟩) = 0 identically.
   - Its multiplier's zero mode is pure gauge: μN → μN + c(t) is an exact symmetry.
   - HT's physical content is **purely global**: one conserved pair (Λ₀, T). Its local fields are gauge.
3. **A conserved momentum cannot be the York clock** (M2, M3).
   - HT's Λ₀ is conserved (ṗ_T = 0 exactly).
   - York time ticks: on dust FRW, dK/dt = −12πGρ_m.
   - So any identification Λ ≡ f(K) freezes K. The only conserved combination of the CMC leaf data is the Friedmann one,
     Q = K²/3 − 8πGρ_m = Λ₀, which is Λ itself.

Every single-term merger was built and varied, and each one fails:

| candidate | what the one term does | verdict |
|---|---|---|
| same foliation (HT's T = the khronon's τ) | HT has no foliation. The 3-form gauge is exact (∂_m∂_nω^{mn} = 0), and a surface displaced by up to 0.29 that encloses zero four-volume has the same T (to 4 × 10⁻¹⁶), which is Kuchař's equivalence classes. On the CMC leaves dT/dτ = N a³ > 0, and {T_tot, H} = Σ N v ≠ 0 | a **relabeling**: a gauge choice for the khronon's global reparametrization, not a merger (M5, D3) |
| MB: Λ ≡ f(K), one term 2f(K)(∂_mT^m − √−g) | At k ≠ 0 it **is** FP14's multiplier in other variables (det = f₁² × det FP14). T⁰'s equation is ∝ f′(K) dK/dt, so K is frozen. With K = K₀ the clock rate absorbs any dust and H = K₀/3 at every z | **FAILS FRW**: E(z) = 1 against ΛCDM's 1.322, 1.791, 3.769, 8.294 at z = 0.5, 1, 2.5, 5 (M3, L2) |
| MA: T^m ≡ ℓ √−g n^m (the linear-potential cuscuton's form) | Λ's equation pins K = 1/ℓ, a **new constant**. Λ(t) = 1/(3ℓ²) − 8πGρ_m then drifts | **FAILS**: with ℓ set today, Λ reaches zero at z = 0.469 (M4) |
| MC: μ ≡ β√Λ (β new) | HT forces δΛ = 0, so δμ = 0. The constant-μ̄ term is a total derivative. The block is FP14's c₂ = 0 block, whose only λ = 0 root is ω = 0 | **FAILS**: the CMC condition is lost and the khronon is frozen (L3) |
| SQ: one global multiplier c(t) on ∫N√h(K − ⟨K⟩)² = 0 | The only global way to impose CMC. The fluctuation δc is absent at quadratic order, and the quadratic action is FP14's c₂ block at c₂ = c̄, a value no equation fixes | **FAILS**: irregular. The scalar mode (|δK|/|mode| = 0.31, 4.9) and a time-dependent source (\|δK/J\| = 0.94, 2.8) carry δK ≠ 0, which the forceless constraint forbids (L4) |

A single *global* pair can give dΛ = 0. On the khronon's leaves, the term 2Λ₀(Ṫ − ∫N√h) reproduces the local HT fields'
count exactly (D1, "globalHT"). No single global constraint can give K = ⟨K⟩_h regularly.

**The minimal honest content is two structures that fit together.**
- The khronon's CMC foliation: a local, second-class constraint family whose global part is pure gauge.
- One global HT pair (Λ₀, T), living on that foliation.

The CMC foliation supplies the hypertime that Kuchař (1991) found missing in unimodular gravity. The HT pair deparametrizes
the khronon's one global Hamiltonian constraint. The literature's *unimodular shape dynamics* (Gryb & Thébault 2012) is the
same pairing: shape dynamics' single global Hamiltonian constraint, with the unimodular pair added to it and not merged.

## What changes when they are combined (not merged)

**Field content.** FP14's fields (g, the khronon τ, μ, φ with λ = 0 so auxiliary, the heat pair) plus HT's. On the khronon's
leaves, HT's fields can be reduced to one global pair (Λ₀, T).

**Local count.** Unchanged: FP5's and FP14's.
- About Minkowski, det(combined) = −4 × det(FP14 multiplier block), with the generic α(Λ) couplings included (L1). So the
  count is 2 tensor + 1 khronon scalar at λ = 0 (+φ at λ > 0), and the health is FP14's.
- D's row forces δΛ = 0. With δΛ = 0, FP14's five equations are unchanged.

**Global count.** +1 pair. In the lattice trace-sector model, the physical phase-space dimension is (D1):

| model | physical dimension |
|---|---|
| combined | 2N_L |
| core without HT | 2N_L − 2 |
| no CMC term (μ adds no degree of freedom) | 2N_L |
| one global HT pair | 2N_L |
| MB | 2N_L |

These hold at N_L = 3 and 4, with and without the MOND scalar. Constraint-surface and consistency residuals are ≤ 2 × 10⁻¹⁴
(no tertiary constraints), and the rank gaps are ≥ 7 × 10¹³.

**Classes at N_L = 4.** The combined model has FC = 2N_L + 2 = 10 and SC = 12 (D2). The first-class set is:
- HT's constraints (spatial, π_X);
- the μ zero mode Σπ_μ/N;
- the lapse scaling;
- the global Hamiltonian H_c + u·φ.

**FRW.** The background is GR + Λ₀, and the multiplier's background is gauge. At k ≠ 0, T^x's equation forces δΛ_k = 0. All
eight remaining linear equations equal FP14 C1b's: G_eff/G = 2/(2 − α_c), with no slip (F1).

**PPN.** Unchanged. The HT term is metric-free (XR20 T1d), and on shell δΛ = 0.

**The York/CMC G_eff = 2G kill is still evaded** (L1).
- The static Newtonian-limit lapse response is 2/(2 − α_c) of GR's, not 2.
- The responses FP14 C2 scored are unchanged, because the equations are unchanged: the static MOND pole, and an equal-time
  part that is c₂-blind and EFE-blind.

**The MOND sector feeds only the clock.** On the lattice, {T_tot, H}/ΣNv = 0.999954 with the MOND scalar present. That is
XR20 T1b's 1 − (κ²/8π)F.

**If MB were adopted** (the only one-term merger that keeps both local structures):
- the count is unchanged (D1);
- μ is absorbed;
- York time freezes (D3: dK/dt = 0 exactly), so FRW fails (M3).

## The status of the a₀ tie

**The footing identity (A1).** This is an algebraic identity, not a derivation.
- The canonical a₀ is (κ/√(24π)) c² K_∞, where K_∞ = √(3Λ) = 1.8087 × 10⁻²⁶ m⁻¹ is the asymptotic York time.
- The alt a₀ is the **same coefficient** on today's York time, K₀ = 3H₀/c = 2.1858 × 10⁻²⁶ m⁻¹.
- K₀/K_∞ = 1/√Ω_Λ = 1.2085.
- Both hold to 2 × 10⁻¹⁶ against FP0's committed values.
- Applied at every z, the alt reading **is** the rival law a₀ ∝ H(z).

**Tying a₀ to K_∞ is XR20's T1 re-expressed, not a new tie.**
- On shell, K_∞²/3 = Q = Λ₀, the conserved global quantity (M2).
- Read from Q on the CMC leaves, a₀(z)/a₀(0) = 1.000000 at z = 0.5, 1, 2.5, 5 and 1100, on both footings. The
  deviation |Q/Λ − 1| is 0 in 50-digit arithmetic (HEADLINE-FLAT).
- The large-volume global Hamiltonian of unimodular shape dynamics, 2Λ − (3/8)P², vanishes exactly at K = √(3Λ) (A2).

**The vacuum caveat is a choice of variable.** A constant matter vacuum energy is absorbed into HT's Λ by
Λ′ = Λ + 8πGρ_vac. That changes the action by −16πGρ_vac ∂_mT^m, a total derivative, so the field equations are identical
(A2). Whether α reads Λ or Λ_obs = K_∞²/3 is therefore a choice made in the action. XR20 T1e's caveat is that choice.

**The local York time gives the rival.**
- On the CMC root, K is **exactly** leaf-uniform. μ's equation is N√h(K − ⟨K⟩) = 0 whatever else the action contains,
  including a K-dependent MOND coupling (A3). So XR20 T3c's local-variation estimate scales to zero exactly.
- The local York time still gives a₀(z)/a₀(0) = E(z) (MUTATE).

**Status: TIED, as in XR20 T1.** κ is fitted. The √Λ power is dimensional.

## Literature (read before the hypotheses were written)

- M. Henneaux & C. Teitelboim, *The cosmological constant and general covariance*, Phys. Lett. B 222 (1989) 195. Λ is
  conjugate to the four-volume.
- W. G. Unruh, *Unimodular theory of canonical quantum gravity*, Phys. Rev. D 40 (1989) 1048. W. G. Unruh & R. M. Wald,
  Phys. Rev. D 40 (1989) 2598.
- K. V. Kuchař, *Does an unspecified cosmological constant solve the problem of time in quantum gravity?*, Phys. Rev. D 43
  (1991) 3332. The cosmological time labels only equivalence classes of hypersurfaces separated by zero four-volume, and
  needs a separate hypertime. This lane's M5 reproduces that statement.
- J. W. York, *Role of conformal three-geometry in the dynamics of gravitation*, Phys. Rev. Lett. 28 (1972) 1082. The mean
  curvature is conjugate to the 3-volume.
- H. Gomes, S. Gryb & T. Koslowski, *Einstein gravity as a 3D conformally invariant theory*, Class. Quantum Grav. 28 (2011)
  045005 [arXiv:1010.2481].
- J. Barbour, T. Koslowski & F. Mercati, *The solution to the problem of time in shape dynamics*, Class. Quantum Grav. 31
  (2014) 155001 [arXiv:1302.6264]. They give a volume-preserving CMC constraint plus one global Hamiltonian constraint, with
  {V, Y} = 3/2. A cosmological constant is an **extra input** there (the dimensionless Λ/Y₀²), not an output of the CMC
  structure.
- F. Mercati, *A Shape Dynamics Tutorial*, arXiv:1409.0105.
- S. Gryb & K. Thébault, *The role of time in relational quantum theories*, Found. Phys. 42 (2012) 1210 [arXiv:1110.2429],
  §7. "Unimodular shape dynamics": the unimodular pair is **added** to shape dynamics' single global Hamiltonian constraint,
  H_gl → ε + H_gl, with ε a constant of motion (Λ → Λ + E/2) and its conjugate the four-volume. They argue this escapes
  Kuchař's criticism because shape dynamics has only a global Hamiltonian constraint. This is the pairing this lane finds.
  Their leading large-volume constraint is reproduced in A2.
- N. Afshordi, D. J. H. Chung & G. Geshnizjani, Phys. Rev. D 75 (2007) 083513 [hep-th/0609150]. N. Afshordi, *Cuscuton and
  low energy limit of Hořava-Lifshitz gravity*, Phys. Rev. D 80 (2009) 081502 [arXiv:0907.5201]. The low-energy limit of
  non-projectable Hořava gravity is the quadratic cuscuton, with CMC leaves.
- J. Bhattacharyya, A. Coates, M. Colombo, A. E. Gümrükçüoğlu & T. P. Sotiriou, *Revisiting the cuscuton as a
  Lorentz-violating gravity theory*, Phys. Rev. D 97 (2018) 064020 [arXiv:1612.01824]. With a **linear** potential the
  cuscuton is a Lagrange multiplier imposing ∇·u = K₀. That is the HT term with T^m replaced by the unit-normal flux, which is
  this lane's MA, and it pins K to a constant.
- H. Gomes & D. C. Guariento, *Hamiltonian analysis of the cuscuton*, Phys. Rev. D 95 (2017) 104049 [arXiv:1703.08226]. The
  homogeneous cuscuton on a CMC foliation carries a single global degree of freedom and acts as a **time-dependent**
  cosmological constant tied to York time. That is the rival-type behaviour a York-tied Λ gives.
- J. Khoury, B. Muntz & A. Padilla, *A Lapse in the Cosmological Constant Problem*, arXiv:2604.08659 (2026). A global
  constraint from a projectable lapse, analogous to sequestering (compare XR20 T4). It is not used here.

No paper found identifies HT's multiplier with a CMC multiplier as one term. The existing constructions either add the pair
(unimodular shape dynamics) or pin K (the linear cuscuton).

## Checks

| run | result |
|---|---|
| main | 22/22, 0 load-bearing failures, **rc = 0** |
| MUTATE | 21/22, **rc = 1**. HEADLINE-FLAT fails: the tie reads the CMC leaf's York time K(z) = 3H(z)/c, giving a₀(z)/a₀(0) = 1.322, 1.791, 3.769, 8.294 at z = 0.5, 1, 2.5, 5 and 2.05 × 10⁴ at z = 1100 (both footings) |

**Controls (reproduced exactly).**
- **C1.** XR20 T1, from XR20's own source (read-only slices):
  - the inputs;
  - the unimodular-clock table: 2.65 × 10⁻³ / 3.87 × 10⁻³ at the RAR knee, 0.485 / 0.708 at y = 100;
  - the vacuum table (−0.0229 dex at ρ_vac = 0.1 ρ_Λ);
  - the five T1a–T1e measured strings, including T1c's lattice count (rank 4, 2 phase-space dimensions).
- **C2.** FP14's Dirac count and York/CMC check, from FP14's own source:
  - the K1, L2, C1 and C2 measured strings (K1's timing field aside);
  - the determinant line and the bookkeeping line 22 − 2×6 − 4 = 6 → 3 modes, verbatim in FP14's committed .out;
  - FP5 A3's count formula, N_phys = 3.
- **C3.** FP14 C1b through FP2's committed machinery: G_eff/G = 2/(2 − α_c), slip 1, μ's equation/Q = −2a³.
- **L0.** This lane's extended Minkowski block reproduces FP14's committed determinant string.

**MUTATE (pre-declared).** The headline tie reads the local York time instead of the conserved quantity. It must fail, and it
does (rc = 1).

## Pre-declaration and disclosures

**What was written when.**
- The hypotheses H1–H8 and the expected verdict were written into the script's docstring **before any code of this lane
  ran**. They came from the literature above and pencil-and-paper algebra.
- The CHECKS text was written afterwards, following the development probes below, and before the first run of the script.

**Development probes** (scratch, outside the repository; these are not the kept outputs):
1. The three controls via source slices.
2. Minisuperspace.
3. FRW perturbations. sympy's `euler_equations` silently drops identically-trivial equations, which misaligned the field list.
   The lane now uses its own Euler–Lagrange helper that keeps zeros.
4. The extended Minkowski block. Solving the 7-field combined block for the responses with `sp.solve` did not finish in
   20 minutes. It was replaced by the exact statement that, at δΛ = 0 (forced), the combined equations are FP14's. The
   responses therefore carry over, and FP14's own C2 flags are reproduced in C2.
5. The lattice.
   - The first lattice run crashed on unsubstituted dust parameters.
   - The MOND-scalar surface points failed to converge with a 5% lapse spread. The chassis locks Δφ to Δ ln N, which pushed
     J_P2's argument past its domain s < 1/4. The spread was set to 0.5%, starting from the φ = ln N lock.

**Debug runs of the script** (these wrote the lane's own output paths; only the final ordered pair is kept):
1. Run 1 scored 21/22. D2 failed because the check was ill-posed. It tested the bracket of G = ΣN ∂H/∂N, which by
   homogeneity is the canonical Hamiltonian H_c. With second-class constraints present, H_c is not first class on its own;
   the first-class global Hamiltonian is H_c + u·φ with the second-class multipliers solved. D2 was corrected to that
   combination, whose brackets are exactly the consistency residual (2 × 10⁻¹⁵). {T_tot, H} was re-signed to read the
   four-volume rate ΣNv.
2. Run 2 scored 22/22 (rc = 0).
3. A `np.errstate` guard was added around one matmul, and the ordered pair was started. That MUTATE run scored 21/22
   (rc = 1, the headline as below), but it printed one more spurious floating-point warning from the macOS BLAS, from a
   second matmul.
4. A second guard was added, with every bracket and gradient array checked finite (the result enters D1/D1m's `finite`
   flag). The ordered pair was then re-run: MUTATE, then main. **These are the kept outputs.** No number changed between
   runs 2–4.

**Scope, said plainly.**
- **The lattice is the trace sector of the root.** It has conformally flat leaf metrics, zero shift, no tensor modes and no
  heat pair.
  - FP14 C3: the CMC term does not reach the tensor sector.
  - Spatial diffeomorphisms are first class and untouched by both structures.
  - FP5 G-2b: the heat pair is second class and adds no mode.
- **The lattice uses illustrative values.** α_c = 0.3 and an R⁽³⁾ stand-in w = 0.2 are used for conditioning. The class
  structure needs only 0 < α_c < 2 (FP5 B4), but other values were not scanned.
- **The Minkowski blocks are FP14's scope:** frozen coefficients, principal order.
- **MB's minisuperspace uses a generic cubic f(K).** The freezing follows for any f with f′ ≠ 0, because T⁰'s equation is
  ∝ f′(K) K̇.
- **Not settled here:**
  - the full 3+1 Hamiltonian analysis with shift and tensor sectors;
  - nonlinear well-posedness;
  - whether a Λ₀ read through the global constraint would drift at O(⟨εF⟩) once structure forms. XR20 T1's exact dΛ = 0
    avoids that by construction.

## Reproduction

From the repository root:
```
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR30_one_clock.py
python3 real_research/cross_thread_review_2026_09_26/XR30_one_clock.py
```
Each run takes about 1.5–2 minutes on ≤ 2 threads (sympy + numpy + scipy).
