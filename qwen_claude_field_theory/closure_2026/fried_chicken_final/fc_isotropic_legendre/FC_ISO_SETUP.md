# FC-ISOTROPIC-LEGENDRE — SETUP

**Mission.** Settle the LAST open door of the constraint-first 2-DOF MOND program:
does an **isotropic** second-class Legendre completion exist whose on-shell traceless
metric stress vanishes (Φ=Ψ, γ_PPN=1)? This file is the **SETUP** — it reproduces the
two committed obstructions with sympy certificates, *defines* the obstruction object
Σ_P, and states the decisive question. It does **not** prejudge the no-go/rescue.

**Certificate:** `fc_iso_setup.py` → `fc_iso_setup.out`, **19/19 checks PASS, exit 0.**

Frozen kernel (do NOT tweak — the obstruction is kernel-general, any μ′≠0):
μ₁₀(y) = y/(1+y¹⁰)^(1/10), μ₁₀′ = (1+y¹⁰)^(−11/10) > 0.
Phenomenological input (never derived): a₀² = κ²c²Gρ_Λ, κ=1/2, Z~21.

---

## 1. The constitutive Hessian is intrinsically anisotropic — DERIVATION

The isotropic MOND flux is Pⁱ = μ(y)Dⁱq, y = |Dq|/a₀, s := |Dq|. Its gradient-Hessian,
computed by brute symbolic differentiation on a generic 3-vector and matched to closed
form (check 01), is

> **Aⁱʲ = ∂Pⁱ/∂(D_jq) = μ γⁱʲ + (y μ′) uⁱuʲ,  u = Dq/|Dq|.**

Eigenstructure (checks 02–03): **transverse eigenvalue = μ** (SECANT modulus, ×2),
**longitudinal eigenvalue = μ + y μ′** (TANGENT modulus). The anisotropy amplitude is
exactly **y μ′** along the dyad u u. Any μ′≠0 ⇒ anisotropic Hessian.

## 2. Carl's naive-Legendre chain — DERIVATION (reproduced)

Action S_M = ∫[ N(D_iPⁱ − 4πGρ) + λ_i(Pⁱ − μ(y)Dⁱq) ]. Variations, each step certified:

| variation | result | check |
|---|---|---|
| δN | D_iPⁱ = 4πGρ (Gauss) | — |
| δλ | Pⁱ = μ(y)Dⁱq (constitutive) | — |
| δPⁱ (after IBP N D_iPⁱ → −(D_iN)Pⁱ) | coefficient = λ_i − D_iN ⇒ **λ_i = D_iN** | 04 |
| δq | conjugate flux Ψⁱ = Aⁱʲλ_j ⇒ **D_i[Aⁱʲλ_j] = 0** | 05 (A symmetric, 06) |

On shell: **D_i[ Aⁱʲ D_jN ] = 0.** The Gauss constraint fixes q on the **secant** modulus
μ; the q-EOM feeds the lapse N through the **same** Hessian A, i.e. through its
**tangent** eigenvalue μ + y μ′. Naive Legendre is DEAD — second-class does *not* mean
gravitationally invisible; the tangent modulus returns via the multiplier.

## 3. The radial slip — COMPUTATION

> **Φ′/Ψ′ = (μ + y μ′)/μ.** For μ₁₀: **= (y¹⁰+2)/(y¹⁰+1)** (checks 07–08).

Limits (checks 09–11): y≫1 → **1** (solar/Newtonian, Φ=Ψ, PASS — checked as hard as the
FAIL); y~1 → **3/2**; y≪1 → **2** (deep galactic, Φ≠Ψ, FAIL). Define A_slip := slip−1 =
**y μ′/μ** (check 12); A_slip = 0 ⟺ μ′ = 0 ⟺ linear law. This reproduces the committed
`fc_final_4ac/fc4ac_slip.py` verdict (deep-MOND 50% weak-lensing excess; solar-system safe).

## 4. York auxiliary-scalar anisotropic stress — EXTERNAL-INPUT (reproduced + cited)

Committed: `theory_2026/york/ppn_lensing_cassini_2026.py`, **commit 0184ba7e, exit 0**.
Stress T_μν = (1/8πG)[2U′(Y)∂_μΦ∂_νΦ − g_μν a₀²U(Y)], Y=|DΦ|²/a₀², U′=μ(√Y). Reproduced
here (checks 13–16):

- 8πG(p_r − p_t) = **2U′(Y)P²** ≠ 0 for P>0 ⇒ traceless Σ_ij = (2U′/8πG)P²(n_in_j − δ_ij/3);
- deep-MOND point mass: Φ_g − Ψ_g = 2v₀⁶/(3a₀r);
- **Einstein-frame γ_PPN = ln r/(ln r − 2) ≠ 1.**

There γ_phys=1 is a **disformal MODEL INPUT**, not derived. (Memory: the York route also
hit 2-potential G_eff=2G and Cassini tension.)

## 5. The obstruction object Σ_P — DEFINITION + certificate

**DEFINITION.** Write the on-shell traceless metric stress of the 2-DOF construction as
Π^TF_ij = **Σ_P (u_iu_j − δ_ij/3)**; Σ_P is the scalar amplitude along the MOND-gradient
dyad. Then **γ_PPN = 1 (Φ=Ψ) ⟺ Σ_P = 0.**

In the naive-Legendre / 2-DOF construction q carries **no independent stress**; the slip
is sourced purely by the differential part of Aⁱʲ. The isotropic μ γ is pure-trace
(pressure) and cannot source a traceless slip; only the (y μ′) u u piece can. Certified
(checks 17–18):

> **Σ_P = y μ′** exactly — the traceless amplitude of the constitutive Hessian.

So Σ_P = 0 ⟺ y μ′ = 0 ⟺ μ′ = 0 ⟺ **linear law**. For the frozen kernel Σ_P =
y(1+y¹⁰)^(−11/10) > 0 for all y>0 — **never vanishes** (check 19).

**Honest distinction (both-ways).** The York AQUAL scalar is a *distinct, worse*
manifestation: its field carries a genuine gradient stress ~2μP², giving γ≠1 even at
μ=const (a scalar-tensor slip present for *any* stress-carrying auxiliary field). The
**2-DOF constraint** obstruction is the μ′-level one, Σ_P ~ y μ′, which is what the
isotropic-Legendre question is about. Both are nonzero for the nonlinear MOND law.

---

## THE DECISIVE QUESTION (precise)

Does there exist a **second-class** auxiliary Legendre completion of D_i[μ(y)Dⁱq] = 4πGρ
whose **on-shell traceless metric stress vanishes, Σ_P = 0** (⇒ Φ=Ψ, γ_PPN=1, FRIED
CHICKEN), **while**

- (a) reproducing D_i[μ Dⁱq] = 4πGρ (the MOND/AQUAL Gauss law),
- (b) keeping **N_grav = 2** (no new propagating DOF beyond the 2 metric polarizations),
- (c) **c_T = 1** (luminal tensor sector)?

- **RESCUE** — YES ⇒ an isotropic Legendre completion exists; the constraint-first 2-DOF
  program has a lensing-clean member.
- **UNIFIED NO-GO** — Σ_P ≠ 0 is FORCED whenever μ′≠0 for any such completion ⇒ the
  anisotropic Hessian of every nonlinear isotropic MOND law forces a metric slip in every
  2-DOF constraint construction ⇒ the entire constraint-first program is **closed on the
  lensing axis**.

**Critical contrast to derive next (load-bearing).** AeST + J₁₀ *does* get Φ=Ψ
(γ_PPN=1, M24 KiDS χ²/dof=0.64, committed) **with the same y μ′ Hessian** — but AeST has
6(+1) propagating DOF (scalar φ + aether A_μ). The mechanism: the aether/disformal
structure absorbs the scalar's anisotropic gradient stress. If that cancellation
*provably requires* the extra propagating field(s) a 2-DOF theory lacks, that IS the
mechanism of the unified no-go.

**Setup status.** The two committed dead-ends are reproduced with certificates; Σ_P is
defined and shown ~ y μ′. Whether Σ_P=0 is FORCED (no-go) or EVADABLE (rescue) for a
generic second-class completion is **OPEN** — the next task, not prejudged here.

## Files (output dir; not committed)

- `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_isotropic_legendre/fc_iso_setup.py`
- `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_isotropic_legendre/fc_iso_setup.out`
- `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_isotropic_legendre/FC_ISO_SETUP.md`
