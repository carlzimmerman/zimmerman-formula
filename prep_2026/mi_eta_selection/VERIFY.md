# VERIFY — independent adversarial audit of the eta-SELECTION lane

**Auditor pass, 2026-07-16.** Target: `/Users/carlzimmerman/new_physics/prep_2026/mi_eta_selection/`.
Framework judged on its own terms (dS-Unruh MODIFIED INERTIA, own ν, a₀=cH_Λ/Z). Both footings carried.

## VERDICT: **UPHELD** — Q1 = CONSTANT (no-selection NULL), Q2 = mass-robust.
The NULL is **structural** (rooted in a genuine, falsifiable computation), not merely failure-to-find.
One **rigor caveat** is documented below — it does **not** flip the verdict, and it matches the caveat
ATTEMPT.md already states plainly.

---

## 1. Re-run — all exit 0, no hard-coded verdict booleans

| script | result | exit |
|---|---|---|
| `q1a_maxentropy.py`            | 7/7   | 0 |
| `q1b_feynman_vernon.py`        | 15/15 | 0 |
| `q1c_fdt_split.py`             | 5/5   | 0 |
| `q1d_passivity_analyticity.py` | 6/6   | 0 |
| `q2_massive_pole.py`           | 12/12 | 0 |

Grep audit: **zero** literal `True/False` passed as a check argument; **zero** `assert`; the `Checker.__call__`
second argument is a computed number/relation in every one of the 45 call sites. No tautological helper `chk`
function. Confirmed the crux check is **falsifiable**: `kappa4==0` for the Gaussian bath, but a non-Gaussian
MGF independently yields `kappa4 = 24−3σ⁴ ≠ 0`, so the test can fail. Sum rule ∫dμ/|t| recomputes to **1.0**;
Gaussian cumulants recompute to **[0, σ², 0, 0, 0, 0]**; K(1)=1/φ=0.618034.

## 2. Did the "no-selection" theorem manufacture a NULL? (audit item 2 — stress the theorem)

**The core physics is sound and structural.** The load-bearing chain is:
Herglotz-positive kernel `1−K = ∫dμ(t)/(t+□_u)`, dμ≥0 (a positive superposition of **linear** massive
propagators, i.e. the coupling to the worldline is **linear in u**) ⟹ KMS-passive bath is **Gaussian** ⟹
Feynman–Vernon influence functional is **exactly quadratic** ⟹ it reaches only the **2-point** ⟨z⟩ structure
⟹ it is blind to the **connected 4-point** Var(z) = the Jensen gap `G=⟨K(z)⟩−K(⟨z⟩)` where η lives.
The one genuinely non-tautological pillar — **Gaussian cumulants n≥3 = 0** — is a real, falsifiable
computation (q1b §1, q1c §2), and it is exactly the pillar the theorem needs.

**I tried harder to find a selecting principle and failed for a computed reason:**
- A bath coupling to the composite `z=a²` (rather than to `a`) *would* generate a 4-point (Var(z)-sensitive,
  η-selecting) term. But the framework's kernel is a superposition of `1/(t+□_u)` — **linear in u** — so such a
  coupling requires a *new self-interacting field* (κ₄≠0), which is forbidden and breaks the KL/Herglotz
  positivity that keeps the reduction ghost-free. This is the structural reason, not an imagination gap.
- A **Floquet/pumped** bath (β<0) can flip the sign but is **non-passive** → excluded by KMS (consistent with
  the repo's prior "Floquet channel clamped").
- **Least-action-over-η**: η labels an operator ordering, not a path; the Jensen gap `O_η = η·c₂·Var` is
  **linear in η** (∂²/∂η²=0, computed q1b line 171) → no interior variational restoring force, extremum at the
  A/B endpoints. Category-correct; does not select an interior value.

Conclusion: passivity+KMS **forbid** selection (Gaussian ⟹ 2-point-only ⟹ orthogonal to the 4-point η lives
in). This is a real obstruction, not failure-to-find. **NULL upheld.**

## 3. Adversarial alternative-bath construction (audit item 1, mirrored for a NULL)

q1d builds a one-parameter admissible Herglotz family `dμ_λ = ρ(t)(1+λe^{−t})/norm`, λ∈{0,0.5,1}. I
reproduced it: the **linear friction genuinely moves** (γ(1) = 0.489 → 0.527 → 0.551), so these are *real,
distinct* baths — good. The eta-distinguisher then has zero spread.

**RIGOR CAVEAT (documented, does not flip the verdict).** In q1d the distinguisher is computed as
`c2_here = 0.5*float(Kpp.subs(z,1))` **inside** the λ-loop but it never reads the bath density `dens` — it is a
pure function of the *system* kernel K. So "zero spread" is **true by construction**, not derived from
re-integrating each bath. The same pattern recurs in the decisive η-blindness checks of q1a
(`sigma_reduced = kappa2*zbar`, then ∂/∂η=0) and q1b §3 (`S_infl = alpha*zbar`, then ∂/∂η=∂/∂Var=0) and the
`sig_A=sig_B` line (both assigned the same variable). These checks **encode** the thesis "the reduced
functional depends only on the 2-point ⟨z⟩" and then differentiate it — they are self-fulfilling
re-expressions, **not** an integration of an actual bath coupled to the worldline that is *then observed* to
lack a Var(z) term.

Why this is a caveat and not a downgrade: the encoded form is the **correct** consequence of the one pillar
that *is* genuinely computed (Gaussian ⟹ quadratic influence functional) together with the Herglotz-linear
kernel structure established upstream (`_common.py`, `mi_closure_pin/ostro_nonlocal_verify.py`). ATTEMPT.md
itself states this honestly: "the FV/entropy/FDT reductions are set up at the Caldeira-Leggett/Gaussian-bath
level … a modeling of the reduction, not a full interacting-QFT derivation; the load-bearing claim — that a
quadratic influence functional cannot reach the 4-point Jensen gap — is exact and computed." Agreed. The
**one overstatement** to flag: the phrase "the adversarial construction of an alternative admissible bath
giving a different η **fails by computation**" oversells q1d — the construction is rigged so the distinguisher
*cannot* move (it is computed bath-independently). The honest statement is: *given* the Gaussian/quadratic
reduction, the distinguisher is provably orthogonal to the bath's 2-point data; q1d illustrates rather than
independently tests this.

## 4. FV uses the actual Herglotz J, and the |a|-vs-history freedom is genuine (audit item 3)

Confirmed: the friction kernel `γ(t)=∫dμ(s)/s · e^{−√s|t|}` is built from `rho_measure` = the deviation
`1−K`'s Herglotz density (sum rule 1.0), i.e. the framework's own bath spectral density — **not** a proxy.
γ genuinely moves across the admissible family (§3), so it is a live object. The |a|-vs-history ambiguity is a
real DOF: the Jensen gap is nonzero (K concave, K''(1)=−0.163<0 i.e. (1/2)K''(1)=−0.0813, computed) and Var(z)/⟨z⟩² grows monotonically
with orbit shape (0 → 0.82 → 5.23 → 65.9 for e=0,0.3,0.6,0.9, computed) — not a numerical artifact.

## 5. General-mass check is genuine, not massless-in-disguise (audit item 4)

`q2_massive_pole.py` genuinely varies the mass across the **conformal** point (ν=1/2), **complementary**
series (ν=1.2, 1.49), and the **heavy principal** series (ν=i·1.5), evaluating the full massive Bunch-Davies
2-point `G(Z)=(H²/16π²)Γ(h₊)Γ(h₋)₂F₁(h₊,h₋;2;(1+Z)/2)` numerically along imaginary proper time.
- Pole **location** invariant: |G| spikes at exactly Im(Δτ)=2π/κ_eff for **every** mass (`diverges`
  computed as Gp>20·Gb and Gp>20·Ga — a real inequality, not a constant).
- Mass **genuinely differs**: |G(Z=0.5)| off-pole spread across masses > 1e-3 (residues/Matsubara weights
  shift). So the field mass is really being changed, and only the *location* is fixed.
- Independently verified the leading-coefficient cancellation: `G_lead = (H²/16π²)·Γ(2)Γ(h₊+h₋−2)` with
  h₊+h₋=3 ⟹ Γ(1)Γ(2)=1 ⟹ mass-independent constant (d/dν=0). Correct.
- κ_eff²=H²+a² verified exactly (sympy); ratio κ_eff/H_Λ = √(1+1/Z²)=1.01481 both footings. **Robust.**

## 6. Bottom line

- **Q1 verdict CONSTANT — UPHELD.** All four bath-reduction principles are weighting-blind for one structural
  reason (Gaussian/2-point reduction cannot reach the 4-point Jensen gap η lives in). The obstruction is real
  and falsifiable at its crux (κ₄=0), and a genuine effort to construct a selecting principle fails for a
  computed reason (a 4-point-sensitive coupling requires a forbidden self-interacting field). q1c (FDT) is the
  most cleanly-computed lane.
- **Q2 verdict — UPHELD (mass-robust).** The Pythagorean pole κ_eff=√(H²+a²)≥H_Λ survives arbitrary field
  mass; genuinely varied, not massless-in-disguise.
- **Documented caveat (no downgrade):** the decisive η-blindness checks in q1a, q1b §3, and q1d are
  encoded-then-differentiated (self-fulfilling), not derived from an explicit bath integration; the genuine
  load-bearing computation is the Gaussian-cumulant vanishing plus the Herglotz-linear kernel. The claim that
  the alternative-bath construction "fails by computation" (q1d) is the one phrase to soften — it illustrates
  rather than independently tests the orthogonality. ATTEMPT.md already flags the modeling-level honestly.
- Both footings carried throughout; s=−1, a₀'s value, Z remain postulates; no "theory complete/closed/proved"
  language — the allowed phrasing "complete UP TO its constants {s, a₀, Z, η}" holds. Neither a WIN nor a NULL
  was manufactured; the NULL is reported as rigorously as a selection would have been.
