# FC-ISOTROPIC-LEGENDRE — REFUTE: Σ_P ≠ 0 is structurally FORCED (unified no-go)

**Task.** Try HARD to PROVE the obstruction is forced: for **any** second-class auxiliary
completion that (a) reproduces the isotropic MOND Gauss law `D_i[μ(y) D^i q] = 4πGρ` with
`μ′≠0`, (b) keeps `N_grav = 2` (no new propagating DOF), and (c) has `c_T = 1`, the on-shell
traceless metric stress `Σ_P ≠ 0` (⇒ Φ≠Ψ, γ_PPN≠1). Report **RESCUE** only if a completion
genuinely evades it.

**Verdict: OBSTRUCTION-PROVEN-FORCED** within the two completion classes that constitute the
constraint-first 2-DOF program; every constructed escape is closed by premise (b) or (c); one
residual (general tensor multiplier, C4) is honestly flagged.

**Certificate:** `fc_iso_refute.py` → `fc_iso_refute.out`, **37/37 boolean checks PASS, exit 0**
(sympy). No asserted PASS: every load-bearing line prints `simplify(...)==0`, a sign, or a
directional-derivative residual.

Frozen kernel (do NOT tweak — the obstruction is kernel-general, any `μ′≠0`):
`μ₁₀(y) = y/(1+y¹⁰)^(1/10)`, `μ₁₀′ = (1+y¹⁰)^(−11/10) > 0`.
Phenomenological input (never derived): `a₀² = κ²c²Gρ_Λ`, `κ=1/2`, `Z~21`.

---

## The theorem in one paragraph

After eliminating its non-propagating auxiliary fields, a 2-DOF completion is a **local action of
the metric and the non-propagating MOND scalar**. A *static* scalar gradient `D_i q` is purely
spatial, so the metric can build a scalar from it in exactly two invariant ways, and **both** feed
the anisotropic constitutive Hessian into `δ/δγ^{ij}` with a nonzero traceless part:

- **CLASS A (covariant / QUMOND-carrier / passive-AQUAL):** the field enters through
  `X = γ^{ij}D_iq D_jq`. **`Σ_P^cov = −μ s²`** (`s=|Dq|`). The **same** `μ = J′/s` is the
  coefficient of the MOND Gauss operator `D_i[μ D^iq]` — this is the **rigidity**:
  `Σ_P^cov = 0 ⟺ μ = 0 ⟺ the Gauss law loses its q-Laplacian (no MOND at all)`.
- **CLASS B (lapse-tied second-class multiplier / naive-Legendre / 4-AC):** the multiplier
  `λ_i = D_iN` pins the **lapse** to the **tangent** modulus `μ+yμ′` while the Gauss constraint
  fixes the **curvature** on the **secant** modulus `μ`. **`Σ_P^constr = y μ′`**, slip `(μ+yμ′)/μ`.
  `Σ_P^constr = 0 ⟺ μ′ = 0 ⟺ linear law (no MOND enhancement)`.

In **both**, `Σ_P` is a nonzero multiple of the constitutive nonlinearity, vanishing only in the
non-MOND limit. Removing it requires adding a field carrying an equal-and-opposite traceless
stress — and every such field **breaks a premise**. The mechanism is that the cancelling structure
must be **timelike and propagating** (exactly the AeST aether), which a pure 2-DOF constraint
theory lacks.

---

## PART A — CLASS A: the metric-variation lemma (DERIVATION, checks 01–10)

**Metric-variation lemma.** For a gradient-energy density `√γ · J(s)`, `s²=γ^{ij}D_iq D_jq`, the
3-stress `τ_ij = −(2/√γ) δ(√γ J)/δγ^{ij}` is

> `τ_ij = γ_ij J − μ D_iq D_jq`,  `μ := J′(s)/s`,  traceless part `Σ_P^cov = −μ s²`.

The two variation identities are certified by an **honest directional derivative** along a generic
symmetric variation `H = δγ^{ij}` (checks 01–02, residual 0) — this avoids the symmetric
double-count pitfall entirely. Assembly + traceless extraction give `Σ_P^cov = −μ s²` (checks
03–04).

**Rigidity (checks 05–07).** The Gauss/flux coefficient is obtained by *differentiating* `J(|Dq|)`
w.r.t. `D_iq` — the flux is isotropic, `flux^i = μ_gauss D^iq`, with `μ_gauss` direction-independent
`= J′/s` (check 05, genuine differentiation, not asserted). The stress coefficient from `δγ` is the
**same** `J′/s` (check 06). Under the flux law `J′(s)=μ(s)s` both equal `μ` (check 07). Hence the
anisotropic metric stress and the MOND kinetic operator are **one object**: you cannot cancel one
without cancelling the other.

**This is the ACTUAL committed genuine-2-DOF carrier.** `sf42_aux_legendre_dof_2026.py` proves the
auxiliary Legendre carrier
`L_MOND = −(1/8πG) N√h [ χ D_iΦ D^iΦ + V(χ,q) ]` is **2 second-class pairs = 0 propagating DOF**
(Pf > 0 all directions, all regimes), i.e. a *genuine* 2-DOF isotropic completion exists — and it
explicitly flags its **open gate (ii): "χ D_iΦ D^iΦ contributes an anisotropic stress … whether it
yields γ_PPN=1 … is a SEPARATE gate."** The lemma with `J′/s → χ` gives
**`Σ_P = −χ s² = −μ s² ≠ 0`** (check 08) — **closing sf42's open gate (ii) ADVERSELY.** For the
frozen kernel `|Σ_P^cov| = a₀²y³(1+y¹⁰)^(−1/10) > 0 ∀ y>0` (check 09); nonzero **even for μ=const**
(check 10) — the "worse", passive-AQUAL manifestation (this is the York `γ = ln r/(ln r−2)` route).

## PART B — CLASS B: the lapse-multiplier obstruction (DERIVATION, checks 11–20)

The constitutive Hessian `A^{ij} = μ γ^{ij} + yμ′ u^iu^j` is confirmed by brute differentiation,
kernel-general (check 11). The multiplier chain (checks 12–13): `δP^i ⇒ λ_i = D_iN`;
`δq ⇒ D_i[A^{ij}D_jN] = 0`. The curvature rides the **secant** μ, the lapse the **tangent** μ+yμ′,
giving slip `(μ+yμ′)/μ = (y¹⁰+2)/(y¹⁰+1)` (check 14) with limits **1** (solar, `Φ=Ψ` PASS — verified
as hard as the FAIL), **3/2** (knee), **2** (deep MOND) (checks 15–17). Raw traceless amplitude
**`Σ_P^constr = y μ′`** (check 18).

**Forcing (check 19).** Because the Gauss constraint enters as `N·(D_iP^i − 4πGρ)` — **linear in
N** — `δP^i` ties `λ_i = D_iN` identically for *any* such completion, so the tangent modulus
returns and `Σ_P^constr = y μ′` is forced whenever `μ′≠0`. (Matches committed `fc4ac_slip.py`:
"H_can must be linear in N … the lapse is pinned to the linearised Hessian — structural.") Frozen
kernel `Σ_P^constr = y(1+y¹⁰)^(−11/10) > 0 ∀ y>0`; kernel-general `y>0, μ′>0 ⇒ y μ′ > 0` (checks
20–21).

## PART C — escapes: each closed by premise (b) or (c) (checks 22–32)

- **C1 — a second static scalar (ghost cancellation).** Cancelling the traceless stress needs
  `2L_X^{(1)}s_1² + 2L_X^{(2)}s_2² = 0` ⇒ `L_X^{(2)} = −L_X^{(1)}s_1²/s_2²`, **opposite sign** to the
  healthy MOND field (checks 22–23). The quadratic **time-kinetic** coefficient of a k-essence
  `L(X)` about a static background is `−L_X` (check 24, the only `χ̇²` term at quadratic order).
  Opposite-sign `L_X` ⇒ opposite-sign time kinetic term ⇒ one field is a **propagating ghost**
  (breaks `N_grav=2` + stability). Moreover **any** non-propagating auxiliary integrates out to a
  local scalar `L_eff(X)` (worked auxiliary-vector example, checks 25–26): its `L_eff,X` is the
  **same** coefficient in the Gauss law and the stress — `L_eff,X = 0 ⟺` no coupling ⟺ trivial
  Gauss. **PART A rigidity is inescapable.**
- **C2 — disformal with a SPACELIKE gradient** `ĝ = Cg + D ∂q∂q`. Longitudinal
  `c² = C/(C+D) ≠ 1` for `D≠0` (check 29) **and** the radial `n n` piece **adds** to the slip
  (check 31, same `u` dyad) — makes it worse and splits the cone (breaks `c_T=1`).
- **C3 — disformal with a TIMELIKE direction** `ĝ = Cg + D u u` (`u²=−1`). This **does** cancel
  (timelike `u u` has no spatial entries, shifts only `ĝ_00` = Φ; check 30) — but
  `c_γ² − c_GW² = −D/C ≠ 0` for `D≠0` (checks 27–28), so **GW170817** forbids a lensing-sized `D`
  unless the graviton also rides `ĝ`, which requires promoting `u` to a **dynamical unit vector**
  (the **AeST aether**) = an extra propagating DOF (breaks `N_grav=2`). This is the committed York
  result `gate2_cone_gw170817_2026.py` / `gate2_dof_preservation_2026.py`, now placed as the
  mechanism of the unified no-go.
- **C4 — symmetric-tensor Lagrange multiplier enforcing Φ=Ψ.** **HONEST RESIDUAL.** A multiplier
  constraint on the geometry is a mimetic-type construction that generically adds a stress sector
  (minimal certificate, check 32: the mimetic scalar constraint gives `T_μν = 2λ u_μu_ν` = an extra
  **dust** energy density — a mode not in the 2-DOF count). This is *evidence* that enforcing Φ=Ψ by
  a multiplier breaks `N_grav=2`; a full proof for a **general** symmetric-tensor multiplier is
  **not machine-certified** here — it is the flagged residual of this no-go.

## PART D — synthesis (checks 33–37)

`Σ_P^cov(y)` and `Σ_P^constr(y)=yμ′` are **strictly positive across `y∈{0.01…100}`** (checks
33–34) and kernel-generally (products of positive quantities, checks 35–36). The **sole** zero of
`Σ_P^constr` is `y→∞` — the Newtonian / no-MOND limit (check 37, stated honestly).

> **Unified no-go.** The anisotropic Hessian of every nonlinear isotropic MOND law forces a metric
> slip in every 2-DOF constraint construction: the same constitutive object (`μ`, resp. `yμ′`)
> controls the MOND Gauss law and the traceless metric stress, so `Σ_P=0` forces `μ=0` (no MOND) or
> `μ′=0` (linear). Cancelling `Σ_P` requires a **timelike propagating** structure — the AeST aether
> `A_μ` (6+1 DOF) that reaches `Φ=Ψ` with the *same* `yμ′` Hessian — which a pure 2-DOF constraint
> theory lacks. **The constraint-first program is closed on the lensing axis**, modulo the C4
> tensor-multiplier residual.

---

## Honesty ledger (both directions)

| Claim | Label | Backing |
|---|---|---|
| `Σ_P^cov = −μ s²`, shares `μ` with the Gauss law | THEOREM | checks 01–07 (directional-deriv lemma + rigidity) |
| sf42 genuine-2-DOF carrier has `Σ_P = −μ s² ≠ 0` (gate ii closed adversely) | DERIVATION | check 08 + committed `sf42_aux_legendre_dof_2026.py` |
| `Σ_P^constr = y μ′`, forced by N-linearity | DERIVATION | checks 11–19 + committed `fc4ac_slip.py` |
| C1 ghost / C2 spacelike / C3 timelike escapes each break (b)/(c) | DERIVATION | checks 22–31 + committed York `gate2_*` |
| Cancellation needs a timelike propagating vector (AeST) | DERIVATION | check 27–28 (cone) + `frozen_dirac_*` 2+1 count |
| `Σ_P(y)` has no interior zero in the MOND regime | COMPUTATION | checks 33–37 |
| Solar limit `y≫1`: `Σ_P^constr→0` (genuine PASS, not a fudge) | COMPUTATION | checks 15, 37 |
| General symmetric-tensor multiplier (C4) also fails | **OPEN (residual)** | check 32 mimetic evidence only — **not** exhaustively proven |
| `a₀² = κ²c²Gρ_Λ`, `κ=½`, `Z~21` | MODEL-ASSUMPTION | phenomenological input, never derived |

**What this does NOT claim.** It does not prove that *no conceivable* Lagrangian evades the slip —
only that within the two completion classes that constitute the constraint-first 2-DOF program
(covariant-scalar + lapse-tied second-class), and against every *constructed* escape, `Σ_P≠0` is
forced. The one un-closed door is the general traceless-tensor Lagrange multiplier (C4), argued via
the mimetic mechanism to add a DOF but not machine-certified. The result is therefore a **forced
obstruction with one flagged residual**, not an absolute impossibility theorem over all field
content.

## Files (output dir; not committed)

- `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_isotropic_legendre/fc_iso_refute.py`
- `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_isotropic_legendre/fc_iso_refute.out`
- `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_isotropic_legendre/FC_ISO_refute.md`

### Cross-cited committed scripts (re-run this session, exit 0)
- `qwen_claude_field_theory/closure_2026/sf42_aux_legendre_dof_2026.py` — genuine 2-DOF carrier
  (0 DOF, Pf>0), flags the open metric-stress gate this task closes.
- `qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_final_4ac/fc4ac_slip.py` —
  `Σ_P^constr = yμ′`, slip `(μ+yμ′)/μ`, forced by N-linearity.
- `qwen_claude_field_theory/theory_2026/york/ppn_lensing_cassini_2026.py`,
  `gate2_cone_gw170817_2026.py`, `gate2_dof_preservation_2026.py` — the disformal-cone / AeST-vector
  escape mechanism (`c_γ²−c_GW² = −D/C`), referee-sustained.
