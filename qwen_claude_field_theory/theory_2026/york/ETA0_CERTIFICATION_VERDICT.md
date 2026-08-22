# η=0 THEORY — FINAL DOF CERTIFICATION VERDICT

**Date:** 2026-08-22
**Scope:** Direct, full-nonlinear Dirac certification of the (ξ,η)=(1,0) theory analyzed
ON ITS OWN — not inherited from the η→0 limit of the frozen 2+1 Dirac theory.
**Scripts (green, committed):**
- `eta0_direct_dirac_2026.py` — 70/70 checks PASS, 0 FAIL (commit `fced273f`)
- `eta0_cubic_quartic_2026.py` — 34/34 checks PASS, 0 FAIL (commit `3690ac6a`)

Independent sympy re-derivation of the rank-deciding algebra confirms every load-bearing
coefficient (this session).

---

## THE FORMULATION STATEMENT (as the paper MUST state it)

> **The theory IS the York-reduced one.** CMC is a **global York gauge-fixing** of the
> Hamiltonian constraint H_⊥ (K = q(t), q a single global variable; the lapse is fixed by
> the Lichnerowicz–York elliptic equation). This is a **2-DOF** theory.
>
> The **local-multiplier form** — adding Λ_CMC(x)·(K − q) to the action as a spacetime
> field — is a **DIFFERENT theory with 3 DOF** (Λ_CMC is a propagating khronon-like scalar).
> It is **not** the η=0 theory and must not be presented as an equivalent formulation.

The action, as the *definition* (not derived, not to be re-derived here):

```
S = (c³/16πG) ∫ N√h (K_ij K^ij − λ K² + ⁽³⁾R)                      [ξ=1, η=0; λ free]
  − (1/8πG)  ∫ N√h a₀² U(y),   y = |DΦ|²/a₀²,  U_y = μ_gal(√y) = √y/√(1+y),
                                U(y) = √(y(1+y)) − arcsinh(√y)
  + S_m[ g̃(Φ) ]                                                    [CONFORMAL matter map]
```

Φ has **no time derivative**. a₀ = cq/Z, q_FLRW = 3H ⇒ **a₀(z) = a₀,₀ H(z)/H₀** (derived,
Z-independent). This selection came from ξ=1 (c_T=1 exact) and G_eff = 2G/(2ξ−η) = G ⇒ η=0;
but **selection within the ansatz is not a proof of the DOF count** — that is what this
verdict certifies directly.

---

## (1) DIRECT FULL-NONLINEAR DIRAC — DOES THE CHAIN TERMINATE?

**YES. CERTIFIED 2+0 at the nonlinear-constraint level.** Not inherited from η→0.

The certification rests on three computed facts, each scripted and independently reproduced:

**(a) H_⊥ stays first-class WITH the MOND term.** The MOND potential density
`√h a₀² U(|DΦ|²/a₀²)` is **ultralocal in h** — δV/δh_ij is the MOND stress and carries no
∂_k h_ij. Over random positive-definite metrics the non-ultralocal residual is ≤ 6×10⁻¹⁶.
So the Dirac–DeWitt bracket {H_⊥(x), H_⊥(x')} closes as in pure gravity, and the global
CMC York gauge-fixing is admissible.

**(b) The Dirac chain TERMINATES — no tertiary constraint.** Φ has no time derivative, so
its momentum gives a primary constraint P_Φ ≈ 0. Preserving it generates the secondary
`C_Φ = −δV/δΦ = D_i[μ_gal D^iΦ] − 4πGρ`. The 2×2 antisymmetric Dirac matrix of the pair
(P_Φ, C_Φ) has

```
det Δ = B²,   principal symbol  B = N√h · 2P(Y),   P(Y) = U_y + 2y U_yy = √y (y+2)/(1+y)^{3/2}
```

**P(Y) > 0 strictly for all Y > 0** (independent sympy check: P(1) = 1.0607; P → 2√y → 0⁺
as y → 0). Therefore Δ is invertible on {Y>0}: preserving C_Φ **fixes the multiplier**
λ_Φ = {C_Φ, H_can}/B rather than generating a new constraint. **The chain stops.**
(P_Φ, C_Φ) are **second-class**. Count = **2 tensor + 0 scalar = 2**, York-reduced.

This is a *direct* result on the η=0 theory: no limit was taken.

---

## (2) CUBIC / QUARTIC — HIDDEN MODE? STRONG COUPLING?

**NO hidden mode. NO propagating strong coupling.** Two independent arguments (Path A and
Path C) agree.

**Path A — No-Φ̇ theorem to all orders.** The entire time-derivative content of
S_grav + S_CMC + S_Φ lives in `K_ij K^ij − λ K²`, which contains **no Φ**; and S_Φ has **no
ḣ** (ultralocal in h). So δΦ is an exact kernel of the field-space time-derivative form at
*every* order — no cubic/quartic δΦ̇ or δΦ·δḣ vertex is ever generated. No hidden dynamical
mode can appear.

**Path C — direct strong-coupling test (the previously-missing piece, now scripted).**
Third/fourth gradient variations of the AQUAL functional f = U(|DΦ|²):

```
H_L = 2P(Y₀),   H_T = 2U_y(Y₀),
T_LLL = 2(2 − Y₀)/(...) ,   Q_LLLL = 6√Y₀ (Y₀ − 4)/(...)
```

The dimensionless canonical strong-coupling ratios r₃ = T_LLL/H_L^{3/2}, r₄ = Q_LLLL/H_L²
are **FINITE at every physical background** Y₀ ∈ (0,∞) — scanned 10⁻³…10⁴, e.g. r₃ = 0.114
at Y₀ = 1. The constraint rank is nonlinearly robust through quartic order.

**Strong-coupling scale.** For the *propagating* sector: **Λ_sc = ∞** — there is no
propagating scalar to strong-couple (Φ is constrained, not kinetic). The relevant finite
scale is the *elliptic* nonlinear amplitude scale of the AQUAL BVP, u_*/a₀ ≈ 54 at y₀ = 1
(weakly nonlinear), collapsing only at the y→0 boundary. This is a PDE-regularity scale,
not a mode-strong-coupling cutoff.

---

## (3) WHAT IS NOW CERTIFIED vs STILL OPEN

### NOW CERTIFIED (within the defined scope: York gauge-fixing + conformal matter map D=0)

- **η=0 theory is 2+0 by DIRECT full-nonlinear Dirac**, not by the η→0 limit. Chain
  terminates; (P_Φ, C_Φ) second-class; det Δ = (N√h·2P(Y))² > 0 on Y>0.
- **No hidden dynamical mode** at cubic/quartic order (Path A no-Φ̇ theorem + Path C finite
  ratios). No propagating strong coupling; Λ_sc(propagating) = ∞.
- **Formulation fixed:** the theory is the York-reduced 2-DOF theory; the local-multiplier
  form is a different 3-DOF theory.
- Load-bearing algebra reproduces in an independent sympy check.

### STILL OPEN (labelled INCOMPLETE, not fail, not manufactured)

- **Disformal branch D ≠ 0 is INCOMPLETE.** CANDIDATE_ACTION §1 leaves the matter map
  g̃ = C(Φ,X) g + D(Φ,X) ∇Φ∇Φ with C, D **UNSPECIFIED**. The certification is **conditional
  on D = 0** (conformal, which is what the gate's g̃(Φ) notation means). D ≠ 0 injects
  Z_Φ ~ D·ρ via g̃_00 = C g_00 + D Φ̇², **reviving a propagating mode**. That branch needs D
  fixed under (c_T=1, G_eff=G) before it can be certified — it is an OPEN DOOR, not a pass.
- **Measure-zero deep-MOND set Y=0** (zero-acceleration turning points, spatial infinity):
  H_L = 2P(Y) → 0 and r₃ ~ ½ Y^{−3/4} diverges. This is the intrinsic AQUAL
  non-analyticity (L ~ |DΦ|³) — a **perturbation-theory breakdown at isolated points, NOT a
  rank change.** C_Φ still fixes Φ uniquely there via the convex (Hessian PSD) + coercive
  (U ~ ⅔Y^{3/2} deep-MOND, ~ Y Newtonian) AQUAL BVP. No DOF restored.
- **Infinite-dimensional bracket not brute-forced.** The H_⊥ first-class closure rides on
  ultralocality of the MOND density + the standard Dirac–DeWitt gravity algebra; the full
  infinite-dim bracket is not finitely scriptable. The **rank-deciding pieces ARE computed.**
- **Covariant standalone equivalence assumed.** The York-reduced theory is a Hamiltonian
  gauge-fixing; that it equals a manifestly covariant standalone theory is taken from the
  gate's definition (local Λ_CMC = 3 DOF, York = 2), not independently proven here.

---

## THE HONEST CEILING (a clean 2+0 does NOT finish the theory)

Even granting the certified 2+0 within scope, two structural gaps remain and must be stated
plainly in any paper:

**(a) ALL novel gravitational phenomenology lives in the Φ sector — and its relativistic
completion is NOT built.** The g_obs interpolation, RAR, BTFR, and especially **relativistic
lensing** all come from Φ's coupling to matter and to the metric through (C, D). With D
left open and γ_PPN=1 currently *engineered* (CANDIDATE_ACTION line 110, marked OPEN), the
lensing sector is the **next construction, not a done result.** A correct DOF count does not
supply the phenomenology.

**(b) a₀/Z is POSTULATED, not first-principles.** a₀ = cq/Z with Z ≈ 21 fitted and κ=½
undecided upstream. The a₀(z) = a₀,₀ H(z)/H₀ scaling is *derived from the action given
q=3H*, but the *coefficient* a₀ enters as an input. This remains a **candidate EFT at a
frontier**, not a first-principles derivation.

---

## BOTTOM LINE

**The η=0 theory, analyzed on its own by direct full-nonlinear Dirac, is a CERTIFIED 2+0 —
the constraint chain terminates and no hidden mode reappears at cubic/quartic order —
conditional on the conformal matter map (D=0); the disformal D≠0 branch and all Φ-sector
lensing/phenomenology remain the open construction, and a₀/Z is postulated, so this is a
certified-DOF candidate EFT, not a finished first-principles theory.**
