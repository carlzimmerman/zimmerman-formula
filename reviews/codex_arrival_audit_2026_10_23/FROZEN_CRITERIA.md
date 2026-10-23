# Codex arrival audit, 2026-10-23 — FROZEN CRITERIA (before any script or number)

Scope: two Codex commits on `main`:
- `420fde16a5` `sol61_push/mechanism_reassessment_2026_10_22/` — its **R1**: an explicit phase-space witness that
  A54/A68's "26 dims, 8 first-class, 0 second-class ⇒ 5 DOF" (DSF-21 / A33 action, `deepseek_push/DS_FINAL_2026_10_21/`)
  is false, because `{H[N], H[M]}` picks up `∫ (π_P^i/η)(N∂_iM − M∂_iN)` from the clock term `√h P^i ∂_i N`.
- `a64cd8be27` `sol61_push/compatible_gas_2026_10_23/` — energy-consistent moving-gas solver; claims no resolved bound
  core (central gas radius tracks the field cell at n128/256/512).

Nothing in `sol61_push/` or `deepseek_push/` is edited. κ = ½ FITTED. No data are used; a₀ does not enter any check
below (W'(0) = 0 at the witnesses), so both footings give identical numbers and nothing is pooled. Never "theory closed".

**Not blind.** I read Codex's R1 text (witness, claimed value `−2πJ/η`, lattice value `−n sin(2π/n)`) and its
compatible-gas RESULT/HANDOFF tables before writing this. I did **not** read Codex's `checks.py`; my script is written from
A54 §1.3's Hamiltonian and A68's frozen action. Before freezing I derived by hand (stated so it cannot steer anything):
the full bracket on `P = 0` data is `∫ (N∂_jM − M∂_jN)[H^j + (2β/(2+3β)) ∂^jπ + π_P^j/η]`, so there is a second
obstruction (β ≠ 0, the non-projectable Hořava λ ≠ 1 one, λ = 1 + β) independent of P; and preservation of `H_⊥` is
`∂_j(N²V^j) = 0` with `V^j` the bracket vector. I expect R1 to reproduce.

## Part A — constraint algebra (script `r1_bracket_check.py`, sympy + numpy, one thread)

Model: A54 §1.3's `H_⊥` in full — `(√h/4K)(2Λ − ³R) + (4K/√h)[π_ijπ^ij − c_β π²] + |π_P|²/(2√hη) + √h[D·P + (γ/2)(D·P)²
+ W(u)] + (γ/4)√h F_ijF^ij + ε` — and `H_i` as in A54, on a periodic lattice in x (all fields depend on x only;
`∂_y = ∂_z = 0`), central differences, canonical pairs (h_a, p_a) with p = π^ii (diagonal) and p = 2π^ij (off-diagonal).
`³R` from sympy for a general x-dependent metric. Gradients by central finite differences (two step sizes reported).
`ε` = dust at rest in Brown–Kuchař form (`∂_i T = 0`): commutes with every gravitational and P variable at that point, so
it enters `H_⊥` only as a non-negative density. K = 1, η = 1, γ = 0.3, a₀ = 1 (W'(0) = 0 makes a₀ irrelevant).

- **A1 (Codex witness).** h = δ, P = 0, π_P = (J, 0, 0), π^ij = q δ^ij with q from `H_⊥ = 0`, β = 0.02, Λ = 0.5, J = 1,
  ε = 0. PASS iff (i) max |H_⊥|, |H_i| ≤ 1e-12 at the witness; (ii) the lattice bracket `{H[sin x], H[cos x]}` equals
  `−(J/η) n sin(2π/n)` to relative 1e-6 at n = 32, 64, 128; (iii) the same with β = 0 (P obstruction alone).
- **A2 (MUTATE, clock term deleted).** Same witness: PASS iff |bracket| ≤ 1e-8 at every n (the check can fail).
- **A3 (β obstruction, mine).** P = π_P = 0, h = δ, π^xx = c, π^yy = π^zz = s(x) = s₀ + s₁ sin 2x, ε(x) ≥ 0 chosen so
  `H_⊥ = 0`. PASS iff all constraints vanish (≤ 1e-12), every ε ≥ 0, and the lattice bracket equals the prediction
  `Σ dx (2β/(2+3β)) (Dπ)(N DM − M DN)` to relative 1e-2 at n = 128 with the relative error falling from n = 64 to 128;
  and at β = 0 |bracket| ≤ 1e-8 (control: GR's kinetic term closes).
- **A4 (tertiary form).** On A3's witness with a non-constant lapse N = 1 + 0.3 cos x, the lattice `Ḣ_⊥(x) = {H_⊥(x), H[N]}`
  equals `(1/N) D(N² V)` with V = (2β/(2+3β)) Dπ, max relative error ≤ 1e-2 at n = 128, falling with n.
- **A5 (consequence, analytic).** sympy verifies on random trigonometric polynomials (torus) that
  `∫ π ∂_i(N² ∂_iπ) = −∫ N² |∂π|²` exactly. With A4 this gives: for π_P = 0 data with β ≠ 0, preservation forces
  `N ∂π = 0` — the lapse must vanish wherever `∂π ≠ 0` (HKLG arXiv:0912.0399's inconsistency). PASS = identity exact.

Reading rule: A1+A2 PASS ⇒ "Codex R1 REPRODUCED". A3+A4+A5 PASS ⇒ "second obstruction CONFIRMED". Any FAIL is reported
as a FAIL with its numbers; no tolerance is changed after a number is seen. What it does **not** test: v3 (β = 0,
η = 0, P auxiliary) — its constraint algebra is a different calculation and stays OPEN; the linear Minkowski 5-mode count
(C5 H1/H4), which lives on π = π_P = 0 where both obstructions vanish.

## Part B — compatible gas (script `cg_repro.py`; Codex's own code run read-only from a copy)

- **B1.** Rerun Codex's `cooling_scale.py` from a copy (inputs hashed): PASS iff ncrit(200 K) = 758 /cm³ (±0.5), min
  tcool/tff = 0.902 (f = 1e-3) and 9.02 (f = 1e-4) (±0.001 relative to the printed digits), Jeans 3276 M☉ (±1).
- **B2.** Independent arithmetic on Codex's committed `analysis_v2/result.json` (not RESULT.md): the table rows (peak nH,
  fixed-gas-mass radius, central cold contrast, first-cell cold mass, 0.3215 kpc aperture mass) match RESULT.md to the
  printed digits; the radius/field-cell ratio is 0.11–0.13 at all three n; the peak-contrast and first-cell-mass
  doubling ratios match 3.98/4.32 and 0.498/0.540.
- **B3 (rerun, bounded).** Rerun `crossing_base` (gas_v3.py, n128, z = 8; it starts afresh, recorded 49 s) and `ultra`
  (gas_v4.py, n512, z = 8; recorded 400 s) from copied code with Codex's recorded argv, `OMP_NUM_THREADS=1 nice -n 15`,
  ≤ 10 min each, RSS < 1 GB (a 384³ L1 job is live; these are small jobs). PASS iff every numeric leaf of the rerun
  `result.json` agrees with the committed one to relative 1e-9 (byte-identical is reported separately). If a run exceeds
  its bound it is stopped and reported NOT RUN — not a FAIL of Codex's result.

Reading rule: B1–B3 PASS ⇒ "compatible-gas numbers REPRODUCED" (numbers only — the physics reading, that the spherical
compact-core route shows no resolved core, is Codex's and is reported as theirs).

## AMENDMENT A1 (PRE-RESULT — no Part A script written or run yet; B3 reruns launched, none read)

Reason, disclosed: working A5 through by hand I found its *reading* was too strong. The preservation condition
`∂_j(N²V^j) = 0` with `V^j = (2β/(2+3β))∂^jπ + π_P^j/η + O(P)` is a condition on the lapse **and** the data together, not on
the lapse alone: for data with `P = π_P = 0` it forces `N∂π = 0` (A5's identity, unchanged), but data with longitudinal
P momentum can satisfy it with `N > 0`. So A5's PASS will be read as "**static-P data with non-uniform foliation
expansion are not admissible at β > 0**", not as HKLG's "the lapse must vanish" (that reading needs the P freedom absent,
as in pure Hořava). A5's check itself is unchanged. One check is added:

- **A6 (linear Dirac algorithm on Minkowski, scalar sector, sympy).** Background h = δ, π = 0, P = π_P = 0, N = 1, Λ = 0;
  scalar perturbations for k ∥ x: h = diag(1+a, 1+b, 1+b), π^xx = p_a, π^yy = π^zz = p_b/2, P_x, π_P^x, lapse n, shift s;
  quadratic Hamiltonian from A54 §1.3 with `(√h ³R)` expanded to second order by sympy. Run the algorithm: preservation of
  `H_⊥^(1)` under H^(2). PASS iff (i) it yields a tertiary `χ = (2β/(2+3β)) π'' + (π_P^x)'/η` modulo `H_x^(1)'` exactly
  (i.e. the eight constraints are NOT closed already at linear order); (ii) the Fourier symbol of `{χ, H_⊥^(1)}` is
  `∝ k² Z(k)`, Z = K(2+3β)/β + ηk² (A68's scalar kinetic coefficient), non-zero for k ≠ 0 at β, η > 0; (iii) preservation
  of χ involves the lapse with symbol `∝ k² Z(k)` (a quaternary fixing n); (iv) the scalar-sector bracket matrix of
  {π_n, H_⊥, χ, ψ} has rank 4 and {π_s, H_x} commute with everything on the surface, so the scalar sector has
  (10 − 2·2 − 4)/2 = 1 DOF. Reading: A6 PASS ⇒ "the linear 5-mode count survives with a different classification
  (π_N, H_⊥ second class with χ, ψ; the lapse is determined, not gauge)". A6 FAIL on (iv) ⇒ the linear count itself moves.

## AMENDMENT A2 (POST-RESULT for A1–A6, which ran 20/20 PASS and MUTATE 7 FAIL as required; PRE-RESULT for A7)

A1–A6 thresholds and readings unchanged. A6 showed `{χ, π_N}` vanishes on Minkowski (V = 0), which is why a
quaternary ψ appears there. On Codex's witness (π_P = J x̂ ≠ 0) the same bracket is `2∂_x(N V ·)` with V = J/η, non-zero
for k_x ≠ 0, so the chain should stop at χ there. Added, before computing it:

- **A7 (constraint rank on the moving-P background, sympy).** Same reduced scalar sector as A6 (k ∥ x, fields a, b, P_x,
  N, N^x and momenta) but **exact** (non-linearised) in the fields, with ³R exact for diag(1+a, 1+b, 1+b) and W kept to
  the order that fixes second derivatives at P = 0. χ := {H_⊥(x), H_T} is computed exactly. Background = A1's witness
  (a = b = P = 0, p_a = q, p_b = 2q, π_P^x = J, N = 1, N^x = 0; q from H_⊥ = 0). Linearise {π_N, π_s, H_⊥, H_x, χ} there and
  form the Fourier bracket matrix M(k) (skew-Hermitian). Report: (i) the symbol of {χ, π_N} (expected ∝ iJk/η);
  (ii) which rows vanish (expected π_s, H_x: first class); (iii) the complex rank r of the {π_N, H_⊥, χ} block at
  J = 1 and at J → 0 with q fixed; (iv) scalar-sector DOF per Fourier mode = (10 − 4 − r)/2 at J ≠ 0 vs the A6 value 1.
  Expectation, stated so it cannot steer: r = 3 at J ≠ 0, i.e. 1.5 DOF per mode — the Hořava half mode. **Reading:**
  r = 3 ⇒ "DSF-21's count is background-dependent: 1 scalar per mode on π_P = 0 backgrounds, 1.5 when P moves;
  the extra half mode's bracket → 0 as J → 0, so π_P = 0 backgrounds (Minkowski, static galaxies) are strongly coupled";
  r = 2 ⇒ "count 1 on both, classification differs, no jump found" (then no strong-coupling claim is made);
  any other r reported as found. A7 has a MUTATE (clock deleted) whose result is reported, with no expectation fixed.
