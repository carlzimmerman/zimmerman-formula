# FROZEN ACTION — FULL DIRAC/DOF VERDICT

**Date:** 2026-08-22
**Gate:** DECISIVE — is the frozen minimal action 2+0 (2 tensor, no propagating scalar) or 2+1 (a
propagating khronon scalar)?
**Verdict:** **2+1 as literally frozen.** A khronon scalar PROPAGATES. This is a FAIL of the
first validation gate for the action as written.
**Scripts (all green, committed):**
`frozen_dirac_hamiltonian_2026.py` (14/14, d95f0da9),
`frozen_dirac_sectors_2026.py` (1f065152),
`frozen_dirac_degeneracy_2026.py` (b74777a0).

---

## The frozen action

    S = S_grav + S_CMC + S_Φ + S_m,   a_i = D_i ln N
    S_grav = (c³/16πG) ∫ N√h [ K_ij K^ij − λ K² + ξ ³R + η a_i a^i ]
    S_CMC  = (c³/16πG) ∫ N√h Λ_CMC (K − q(t))     [Λ_CMC LOCAL multiplier, q GLOBAL]
    S_Φ    = −(1/8πG) ∫ N√h a₀² U(y),  U_y = μ_gal(√y),  y = |DΦ|²/a₀²

The MOND-Φ sector is separately established second-class (P_Φ ≈ 0, 0 DOF) and is NOT the question.
The question is the GRAVITY+CMC scalar (the khronon).

---

## (1) Generic DOF count — **2 + 1 = 3**

Proven two independent, mutually-agreeing ways.

**(i) Hamiltonian Dirac rank.** The Legendre trace π/√h = (1−3λ)K + (3/2)Λ makes K invertible iff
λ ≠ 1/3. The 4×4 second-class matrix on {p_N, Φ_N, p_Λ, C_CMC} has

    Pf = −A·D,     det = (A·D)²,
    A = {p_N, Φ_N}   = 2 η k²        (0 iff η = 0)
    D = {p_Λ, C_CMC} = (3/2)/(1−3λ)  (0 iff λ = 1/3)

The York lapse-fixing operator B = {Φ_N, C_CMC} (Lichnerowicz–York) and G = {p_Λ, Φ_N} CANCEL from
the Pfaffian, so the rank is robust to them. Generic (η ≠ 0, λ ≠ 1/3): **rank 4**, giving

    N_local = ½[ 22 − 2·6 − 4 ] = 3 = 2 tensor + 1 khronon.

(First class = P_i(3) + H_i(3) = 6; second class = the 4.)

**(ii) Lagrangian sector reduction.** In spatial gauge E=0 the fields are (ψ, α, β, δΛ), only ψ
carrying a time derivative. The CMC multiplier δΛ enforces K⁽¹⁾=0, fixing the shift β = −3ψ̇/k².
The η a_i a^i term makes the lapse α **auxiliary** (algebraically α = −2ξψ/η), NOT a Hamiltonian
constraint, so it does NOT remove ψ. The reduced khronon Lagrangian is

    L_red = K_kin ψ̇² + V_grad ψ²,   K_kin = 6 (>0, independent of BOTH λ and η),
    c_s² = (2 − η)/(3η)   at ξ=1.

The Euler–Lagrange determinant factors as −8k⁶(η k² ξ + 3η ω² − 2k² ξ²): **linear in ω²** ⇒ exactly
ONE propagating scalar branch.

The two methods agree. This realizes the project ledger's own CRITICAL DISTINCTION: GR + a LOCAL
multiplier Λ(K−q) = 3 DOF (preserving p_Λ closes on K=q but supplies no gravitational constraint to
kill the scalar); only the GLOBAL York gauge-fixing gives 2. Every prior "2+0" script
(`dof_deformed_cmc_2026.py`, `york_step2_closure_2026.py`) silently used η=0 — the special case
that DELETES the khronon — which is NOT the frozen action.

---

## (2) Is there a coefficient point with c_T=1 AND G_eff=G AND 2+0 — and is it unique?

**Yes, unique — but it is NOT the frozen action.** Coefficients are DERIVED, not fitted:

| Condition | Requirement |
|---|---|
| A: c_T = 1 (tensor speed² = ξ) | ξ = 1 |
| B: metric G_eff = G, where G_eff = 2G/(2ξ − η) (sympy static weak-field, λ-free) | 2ξ − η = 2 |
| C: 2+0 (kill khronon) | η = 0 |

These are mutually compatible and meet at the **UNIQUE point (ξ=1, η=0, λ free).** Structurally,
**A & B ALREADY IMPLY C**: c_T=1 plus a metric G_eff=G force η=0. A propagating khronon (η≠0) is
INCOMPATIBLE with metric G_eff=G. λ is unconstrained by the DOF count (it cancels once the CMC
multiplier saturates the trace) and drops out of the static G_eff (K_ij=0 there).

Caveat on the two senses of G_eff: matter couples to Φ (not the lapse), so MATTER-dynamics G_eff=G
holds automatically and η-independently; the derived G_eff = 2G/(2ξ−η) is the METRIC-sector coupling
that light/PPN/lensing see (the load-bearing sense for the γ_PPN gate, already flagged
engineered/OPEN). The unique 2+0 point sits exactly where η=0.

---

## (3) Which CMC formulation must the frozen action use to get 2+0?

The **GLOBAL York gauge-fixing** of H_⊥ (with the Lichnerowicz–York lapse equation), NOT the LOCAL
Λ_CMC(K−q) multiplier field. The local multiplier fixes the trace K=q but leaves the khronon alive
(the 3-DOF outcome). Combined with (2): to carry 2+0 the frozen action must be amended to
**η = 0, ξ = 1, λ free**, with S_CMC read as the York global gauge-fixing. Equivalently, the 2+0
sub-formulation IS GR + CMC — the non-projectable khronometric structure the action advertises is
simply absent there.

The λ = 1/3 kinetic-conformal escape (D=0, a new primary π=(3/2)√h Λ appears, 4×4 chain inapplicable)
is a DISTINCT candidate 2+0 not verified here — **INCOMPLETE**. And the sector reduction shows λ
cancels once the CMC multiplier is present, so λ=1/3 is inoperative in that route anyway.

---

## (4) If 2+1 is forced, is the khronon healthy or fatal?

On the 2+1 branch the khronon is:
- **Ghost-free** (K_kin = 6 > 0, independent of λ, η);
- **Gradient-stable only on 0 < η ≤ 2** (c_s² = (2−η)/(3η) ≥ 0); fatal (c_s² < 0) for η > 2 or η < 0;
- **Strongly decoupled, not strongly coupled, as η→0** (c_s² → +∞, the mode stiffens and decouples —
  healthy; K_kin stays finite so there is no infinite-coupling pathology).

But healthy-as-a-scalar is not viable-as-a-theory: on the allowed window 0 < η ≤ 2 the metric
G_eff = 2G/(2−η) ≠ G and preferred-frame effects appear, squeezing η toward 0. The only place the
khronon is simultaneously healthy AND compatible with c_T=1 & metric G_eff=G is η=0 — where it
ceases to propagate. So the propagating khronon is a **NEW obstruction**, distinct from the already
recorded Gate E (G_eff=2G) and Gate F (Cassini) fails: it is an EXTRA dark scalar that the frozen
action cannot keep without breaking G_eff=G.

---

## (5) ONE-LINE bottom line for the paper spine

**The frozen action as literally written is 2+1 (a propagating khronon); the spine must change to the
amended coefficients η=0, ξ=1, λ free with S_CMC read as a GLOBAL York gauge-fixing (= GR + CMC) —
the ONLY point where c_T=1, metric G_eff=G and 2+0 hold simultaneously, and a DERIVED constraint, not
a fit.**
