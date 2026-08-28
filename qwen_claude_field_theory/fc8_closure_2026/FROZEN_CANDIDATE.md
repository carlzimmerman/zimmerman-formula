# FC-FINAL — FROZEN CANDIDATE (constant-a₀ AeST with a fixed J₁₀ constitutive law, 2026-08-28)

**This directory is a closure lane, not a construction lane.** FC-FINAL is frozen. Derive its field
equations and run the gates until each returns **PASS / FAIL / OPEN** — nothing else. Do **not** improve
the theory here. See `REQUIREMENTS.md`. This does **not** supersede the MMG closure in `../closure_2026/`.

> **Supersedes FC-8R (same lane).** The FC-7/FC-8/FC-8R exploration added a cosmological scalar σ +
> potential lock `a₀²=κ²GV(σ)` to make a₀ dynamical. That works (σ verified fully healthy: canonical,
> no MOND–σ kinetic/linear coupling — `../closure_2026/FC_AEST/scripts/fc8_clean_lock_2026.py`,
> `fc8_symbolic_audit.py` A0/A3/A6), **but every dynamical a₀ mechanism spawns its own closure problem
> (σ stability + PPN + cosmology).** FC-FINAL removes that recursion: **a₀ is a fundamental constant**
> (like G, c). The `a₀²∝ρ_DE` relation is demoted from a structural beam to a **testable cross-sector
> hypothesis** investigated separately, not part of the action.

---

## The frozen action — no new field

$$
\boxed{\,S_{\rm FINAL}=S_{\rm AeST}^{\star}+S_m[g,\psi]\,}\qquad\text{fundamental fields: } g_{\mu\nu},\,A_\mu,\,\phi.
$$

$$
S_{\rm AeST}^{\star}=\frac{c^3}{16\pi\tilde G}\int d^4x\sqrt{-g}\Big[
R-\tfrac{K_B}{2}F_{\mu\nu}F^{\mu\nu}+2(2-K_B)J^\mu\nabla_\mu\phi-(2-K_B)Y-\mathcal F(Y,Q)-\lambda(A_\mu A^\mu+1)\Big]
$$

`Q=A^μ∇_μφ`, `Y=(g^{μν}+A^μA^ν)∇_μφ∇_νφ`, `F_{μν}=2∇_[μA_ν]`, `J^μ=A^ν∇_νA^μ`.

**The modification is ONLY the AeST free function (no double-counting the Y-sector):**

$$
\boxed{\,\mathcal F(Y,Q)=\underbrace{\mathcal F_Q^{\star}(Q)}_{\text{AeST cosmology (retained)}}+\;a_0^2\,J_{10}\!\Big(\frac{\sqrt Y}{a_0}\Big)\,},\qquad
\boxed{\,a_0=\text{constant}\,}
$$

**AeST Q-sector (frozen, retained as the AeST dark component — NOT asked to carry dark energy):**
`𝓕_Q^★(Q)=K(Q)=−2Λ+𝒦₂(Q−Q₀)²` (SZ21 quadratic, 𝒦₂>0). [Non-quadratic K(Q) (cosh/exp, A&A 676 A100) is an
allowed re-freeze for early-time cosmology, but changing it is a *re-freeze*, not a run-time move.]

**MOND interpolation (frozen — sharp, Cassini-safe n=10):**

$$
\boxed{\,\mu_{10}(y)=\frac{y}{(1+y^{10})^{1/10}}\,}\quad
\boxed{\,x=\frac y2\big(2-\mu_{10}(y)\big)\,}\quad
\boxed{\,J_{10}'(x)=2x\,\frac{\mu_{10}(y(x))}{2-\mu_{10}(y(x))}\,}
$$

**Matter:** `S_m[g_{μν},ψ]` — universal metric coupling.

**Frozen parameters:** `{K_B, 𝒦₂, Q_0, Λ, μ, a_0}` (μ = AeST scalar mass from 𝒦₂,Q₀; a₀ is a fundamental
constant fixed by observation, like G). **DOF target = 6** (the established AeST count, if the modified
`𝓕(Y,Q)` preserves the degeneracy — to be proven, not assumed).

**Constitutive normalization FIXED by J₁₀ (not fitted):** matching `F_M=a₀²J₁₀(√Y/a₀)` to the AeST
spherical asymptotics (MNRAS 531,272: `𝒥→(1/β₀)Y` Newtonian, `𝒥→[2/(3(1+β₀)a₀)]Y^{3/2}` MOND) gives —
from **both** limits independently — **`β₀ = 1`, hence `λ_s = β₀⁻¹ = 1`** (`fc8_symbolic_audit.py` A6). A
genuine internal check, not a knob.

**Y=0 degenerate branch — RESOLVED BENIGN** (`y0_degenerate_dirac.py`, 5/5; 7-agent adversarial workflow,
3 derive + 3 refute all benign-6DOF). `F_YY~1/(4√Y·a₀)→∞` at Y=0, but this is a **Legendre-chart / AQUAL-like
non-analyticity**, not a pathology: (i) F_YY's dual `F*_qq=8a₀²q→0` with `F_YY·F*_qq≡1`, so which one
"blows up" is chart-dependent — regular in `x=√Y/a₀`; (ii) Y is aether-*orthogonal* (no φ̇), so φ's momentum
inverts through `F_QQ=2𝒦₂` (finite, Y-independent) — F_YY never enters the kinetic matrix; (iii) the
spatial eigenvalues `G_T,G_L→(2−K_B)>0` at Y=0 (the divergent `2Y·F_YY=√Y/(2a₀)→0`, tamed by the vanishing
gradient), supplied by the **analytic −(2−K_B)Y seed** ⇒ no ghost, no strong coupling; (iv) `δ²S_M=0` ⇒ the
declassifying auxiliary carries zero dynamics on the measure-zero ∇φ=0 locus ⇒ no DOF jump. **Control:**
bare AQUAL (delete the seed) *does* strong-couple at ∇φ=0 — AeST is saved specifically by the `−(2−K_B)Y`
term. **RESIDUAL (OPEN, completeness):** the full covariant nonlinear multi-constraint AeST Dirac
(lapse/shift + 4 diffeo + aether unit + vector A_i, simultaneously) — a completeness item, not a place a
pathology is hiding.

**IR requirement (observational, fitted — NOT a theoretical constant):** `μ⁻¹ ≳ 1 Mpc`, so the AeST
oscillatory-IR onset stays beyond the tested galactic (rotation-curve) domain. Verified numbers
(`spherical_fc8.py`, `r_C=⅓[18 r_M μ⁻²]^{1/3}`, `r_M=√(GM_b/a₀)=8.35 kpc`): `μ⁻¹=1 Mpc ⇒ r_C≈177 kpc`
(past the ~30 kpc disk); the conservative `r_C≥1 Mpc` needs `μ⁻¹≈13.4 Mpc`. **`μ⁻¹` is a fitted parameter,
NOT hard-coded** (an earlier `μ⁻¹=3 Mpc` fiducial is withdrawn as a frozen constant — it gives only
`r_C≈370 kpc`; use it as an exploratory numeric point if needed, explicitly labelled fiducial).

---

## What is already established (inputs — re-checked by `fc8_symbolic_audit.py`, NOT the closure)

- `μ_10(y)=y+O(y¹¹)` ⇒ `J_10(x)=x³/3+O(x¹³)` ⇒ `𝓕_M=a₀²J₁₀=O(Y^{3/2})=O(δ³)` ⇒ **δ²S_MOND=0** on `Y=0`.
- MOND law in the AeST spherical reduction: `∇²Φ̃=∇·[𝒥_Y∇χ]` with `𝒥_Y=μ̃=μ_10/(2−μ_10)` ⇒
  `g_N=μ_10(g/a₀)g=g²/(g^{10}+a₀^{10})^{1/10}`. Deep-MOND `g²=a₀g_N` ⇒ **BTFR `v⁴=Ga₀M_b`**.
- Newtonian recovery viciously sharp: `1−μ_10=O((a₀/g)¹⁰)` ⇒ no Solar-System screening mechanism needed.
- No σ ⇒ no new propagating scalar ⇒ nothing to add to the kinetic matrix; the MOND term is a fixed
  function of the existing AeST variable Y.

## Demoted (NOT in the action)

`a₀²=κ²Gρ_DE` is a **cross-sector empirical hypothesis** to test against the broader framework, not a field
equation. FC-FINAL predicts a₀ = constant; whether the observed a₀ tracks ρ_DE is a separate question,
no longer able to kill the gravitational theory via a Hamiltonian pathology.

---

## DO NOT (during the closure run)

```
DO NOT re-introduce sigma / a dynamical a0 (that is FC-8R, superseded).  a0 is a CONSTANT here.
DO NOT replace mu_10.        DO NOT introduce any new field.
DO NOT modify the matter coupling.   DO NOT add a hand-tuned PPN counterterm.
DO NOT assume the vector vanishes in the quasistatic limit (the m_x scale, PRD 110.024062).
DO NOT select boundary conditions solely to remove a pathology.
DO NOT inherit a PASS from ordinary AeST (the free function is MODIFIED -> re-derive).
DO NOT import Einstein-aether PPN formulas without deriving the FC-FINAL -> EA parameter map.
DO NOT convert OPEN into PASS.
```
