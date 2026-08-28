# FC-AeST — investigation status (2026-08-27, consolidated)

**One line:** FC-AeST is the AeST chassis (Skordis–Złośnik) + Carl's `a₀²(Q)=−κ²c²G·K(Q)` promotion
+ the exact-exponential kernel translated correctly through AeST's two-field structure. Its new
physics is **cleanly sequestered to the nonlinear galactic regime**; linear cosmology, lensing, and
stability are *inherited AeST*, and the surviving distinctive prediction is `a₀²∝ρ_DE`. It is **not a
completed theory** — but it is fully characterized, and every checkable claim below is script-backed.

## Established (verified this session)
| Result | Status | Script |
|---|---|---|
| observable `μ_obs=1−e^{−y}` ↔ AeST field `μ̃=tanh(y/2)`, `x=(y/2)(1+e^{−y})`, monotone/invertible | **exact** | fc_aest_kernel_bridge |
| Newtonian + deep-MOND + BTFR survive the two-field translation | **exact** | fc_aest_kernel_bridge, fc_spherical_gate |
| radial solution reproduces the exact RAR (max err ~1e-8) | **PASS** | fc_spherical_gate |
| MOND term sequestered: `G(x)=(2/3)x³+O(x⁴)` ⇒ `F_MOND=O(δ³)` on FLRW | **PASS** | fc_flrw_quadratic_gate |
| **no direct δa₀–MOND linear coupling**: `∂²F_MOND/∂Q∂Y|_{Y=0}=0` | **PASS (new)** | (sympy, this file's commit) |
| χ-clock / DBI-K(Q) healthy: canonical `c_χ²=1`; DBI `K''>0` | supported | fc_flrw_quadratic_gate |
| w-drift bridge: `d ln a₀/d ln(1+z) = (3/2)(1+w_DE)` | **exact** | fc_flrw_quadratic_gate |

## Inherited from AeST (not FC wins, not re-derived here)
- c_T=1 (K_B structure, GW170817); γ_PPN=1 (no dark anisotropic stress; committed typeII_direct_variation);
  lensing 21σ→0.6σ; 6 physical DOF (PRD 110.044015). The FC kernel changes none of these at quadratic order.

## Inherited liabilities (FC does NOT fix)
- **AeST low-k unbounded-Hamiltonian mode** (2109.13287): F_MOND is O(δ³) and δa₀ decouples ⇒ FC cannot cure it.
- **AeST oscillatory 3rd spherical regime** (2304.05134): FC kernel shifts onset ~20% but does NOT remove it
  (the outer regime is driven by the mass term μ², not the interpolation — matches MNRAS 531,272).
- Both are pushed toward cosmological scales *if* μ_A ~ a₀/c² ~ H/c — which is natural because a₀~cH_Λ — but
  proving μ_A~H/c is *forced* by one F(Y,Q) (not tuned) is an **open** AeST-Hessian calculation.

## Honest retractions (made before they hardened into claims)
- "DESI directly tests a₀(z)∝√ρ_DE" — **too optimistic for the DBI clock**: `a₀(z=1)/a₀,₀=0.9999995`;
  the drift only turns on at z~17–35. The *structural* relation survives; the DBI *trajectory* is flat at DESI z.
  Forcing DESI-sized w(z) evolution needs ν₀ ~100–300× the committed ceiling ⇒ unacceptable recombination dust.
- The exponential-kernel **growth bracket is HEURISTIC, not a theory prediction** — the FC MOND term is absent
  from the linear FLRW action, so linear growth is pure AeST, not `ν_FC × δ_source`.

## Honest concessions
- **6 DOF, not 2** — the 2-DOF program (this session's F(A²)/MMG/CGD/two-channel no-gos) stays closed; FC is a
  different, heavier chassis. κ² and Z remain **fitted** (a₀ is a field; its coefficient is not derived).

## The one real remaining calculation
The **AeST linear perturbation matrix on the FC background** — `det K_scalar(k,a; Q̄)`, `μ_eff(k,a)`,
slip `η=Φ/Ψ` — gives growth + lensing-slip + scalar-stability in one pass, and (by sequestration) reuses the
*published* AeST machinery rather than a new theory. It is a faithful reproduction of Skordis–Złośnik
perturbation theory (2007.00082 / 2109.13287 / 2303.00038): a **major numerical undertaking**, not a one-script gate.

**Bottom line:** FC-AeST is a coherent, literature-anchored embedding whose FC-specific content is exact and
cleanly sequestered; its physics viability now rests entirely on the *inherited* AeST perturbation/outer-regime
sectors, whose faithful reproduction is the (large) next step. The distinctive, framework-level survivor across
this entire session's no-gos remains `a₀² = κ²c²G ρ_DE` with `w(z) = −1 + (2/3) d ln a₀/d ln(1+z)`.

## Addendum (final swing): FC removes the old pole; inherits c_s² unchanged
- **Genuine FC improvement (verified):** the exact exponential `F_Y=1−e^{−x}` is regular for all x
  and →1 as x→∞, so the **old `ks/(1−2s)` finite-gradient pole is GONE** — the a₀/2 constant
  Solar-System force (~10³× the ephemeris bound in the committed analysis) does not occur for FC.
- **Inherited unchanged:** the scalar sound speed `c_s² = (2−K_B)(1+K_B λ_s/2)/(K₂ K_B)` is set by
  the K(Q) sector's K₂; since `F_YQ|_{Y=0}=0` and F_MOND is O(δ³), the FC kernel does not touch K₂.
  So the committed **c_s² superluminal liability (~30c–184c at 1 AU; c_s=c at 27–165 AU) SURVIVES
  the FC translation** — a candidate liability of the underlying AeST/DBI K(Q) background, not of the
  MOND kernel. Note `route2_full_stack`/`route2_aest_embedding` still run the μ_n / `ks/(1−2s)`
  kernels — **not yet migrated to the exponential FC kernel**, so their Solar-System numbers must be
  recomputed before FC can claim or disclaim the pole/c_s outcome.

## Decision point (the FC gate is now surgical but large)
The exponential FC kernel is **frozen and clean**. Every remaining question is about the *inherited*
AeST K(Q)/aether background: (i) a finite scan over (K_B, Q₀, Λ_D) — M⁴ fixed by a₀ — for
`{c_s²≤c² at SS scales} ∩ {r_C ≫ r_gal} ∩ {K₂>0, c_T=1}`, where Λ_D controls BOTH c_s and r_C (the
squeeze); (ii) the AeST linear perturbation matrix (growth + slip + stability) on the FC background.
Both require first **migrating the numerical stack to the exponential kernel**, then a faithful
reproduction of Skordis–Złośnik perturbation theory. This is a well-defined program, not a one-script
gate — and its outcome is an AeST-background question, no longer a MOND-kernel question.
