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

---

## 2026-08-27 — THE DECIDING GATE: FC exponential kernel FAILS Cassini (6.1× ceiling)

> **⚠️ THIS SECTION CONTAINS A CORRECTED ERROR — see the 2026-08-28 CORRECTION below.** The 6.09×
> number and "FC worse than plain exponential / exponential family eliminated" verdict are WRONG:
> they computed the quadrupole from the internal AeST *field* function tanh(y/2) instead of the
> *observable* μ_obs=1−e⁻ʸ. The correct FC number is 3.76× (identical to plain exponential), and the
> FC-AeST *chassis* is NOT closed. Section kept verbatim as the record of the error. RETRACTIONS.md filed.

The c_s²/r_C squeeze (this file, above) found a real nonempty overlap and correctly showed the
old `ks/(1−2s)` **pole is gone** — a genuine FC improvement in the scalar-sound-speed channel
(λ_s=1−e⁻ˣ is bounded in [0,1], never diverges, so no superluminal c_s and no a₀/2 force from
*that* mechanism). But that overlap is **not the binding solar-system constraint.** The gate that
killed μ=1−e⁻ʸ is the **EFE phantom quadrupole** Q₂ at the solar-circle external field
y_ext=GEXT/a₀≈2.48, and the squeeze never tested it.

Computed with the **committed DHF integral** `q_direct2D` (route1B, verbatim; guard reproduces the
published RouteA anchor q(2)=0.221 exactly). Script: `scripts/fc_cassini_quadrupole_2026.py`.

| kernel | class | q(solar) | Q₂/ceiling | verdict |
|---|---|---|---|---|
| RouteA/MS08 | exp | 0.275 | 6.23× | FAIL |
| μ=1−e⁻ʸ | exp | 0.166 | 3.76× | FAIL |
| **FC tanh(y/2)** | **exp** | **0.268** | **6.09×** | **FAIL** |
| μ₅ | sharp | 0.014 | 0.31× | PASS |
| μ₁₀ | sharp | 0.003 | 0.06× | PASS |

**The structural trap, sharpest form:** the gradual (exponential) transition that removes the pole
is the SAME shape that maximizes the phantom quadrupole. One kernel cannot both remove the pole and
clear Cassini. FC (tanh) is in fact *slightly worse* than plain μ=1−e⁻ʸ, because tanh approaches
Newtonian even more gradually near y_ext. To pass Cassini FC must swap tanh for a sharp μ_n — at
which point it is no longer the exact-exponential FC kernel; it is the μ_n MMG chassis, paying the
same RAR price (0.108→0.127 dex). **Robustness:** the two-field f_G=½ split could at most halve the
scalar-channel quadrupole; 6.09× → ~3× is still a FAIL. The margin (6×) is not a marginal call.

**VERDICT:** FC-AeST's exact-exponential kernel is **eliminated by Cassini**, the same wall as the
whole exponential family. The pole removal is a real but non-decisive result. FC does not get to
live as an exponential-kernel theory; the only Cassini-safe MOND kernel in this repo remains μ_n.

---

## 2026-08-28 — CORRECTION + FINAL SCOPED STANDING (3 independent refuters: C1/C2 SUPPORTED, C3 PARTIAL)

The 2026-08-27 section above made a **field-vs-observable category error.** Corrected below and
independently re-verified (workflow fc-cassini-correction-verify; guard reproduces RouteA
q(η=2)=0.221). Script: `scripts/fc_cassini_CORRECTED_2026.py`.

**(1) Corrected number.** Matter minimally couples to g_μν, so Cassini feels the **observable** boost
ν=g/g_N — i.e. the QUMOND function inverse to μ_obs=1−e⁻ʸ, **NOT** the internal field function
μ̃=tanh(y/2). At η_solar=G_ext/a₀=2.478 (ceiling q<0.0441): **observable μ_obs=1−e⁻ʸ → q=0.166 =
3.76× ceiling = FAIL, numerically IDENTICAL to plain exponential.** The earlier "6.09×" fed tanh(y/2)
into q_direct2D as if it were ν — reproduced exactly (0.268=6.09×), thereby diagnosed as the error.
FC is **not** "worse than plain exponential"; it fails identically to it.

**(2) Structurally closed? NO — only the exponential CHOICE dies.** μ_obs=1−e⁻ʸ is a FREE INPUT
(`fc_aest_kernel_bridge.py` line 13, "OBSERVABLE MOND function (target)"), not forced. The bridge
μ̃=f_G·μ_obs/(1−f_G·μ_obs) is algebraic in μ_obs and healthy (∈(0,1), monotone, invertible) for ANY
monotone μ_obs<1; the old ks/(1−2s) pole vanishes only at μ_obs=2 (outside [0,1]), so **pole-removal
is kernel-independent, not exponential-specific.** c_T=1, γ_PPN=1 (Φ=Ψ lensing), the 6-DOF count, and
the Q-sector a₀/DE lock are set by the AeST K_B **vector** sector, not the Y-sector interpolation.
Swapping μ_obs→μ_n is Cassini-SAFE (μ₅ 0.31×, μ₁₀ 0.064× canonical, healthy field function).
**The FC-AeST chassis is NOT closed by Cassini; the exact-exponential kernel is.**

**(3) Exclusion is by SHARPNESS, not smoothness.** μ_n is one-scale and C^∞-smooth, yet μ₂=2.83×/
μ₃=1.25× FAIL while μ₄=0.59×/μ₅=0.31×/μ₁₀=0.064× PASS → discriminant is transition **sharpness n≳4**
(Q₂ generated at r_t~5600 AU, y~2, where sharp kernels leave near-zero phantom residual). So the
earlier "one-scale smooth excluded" was too strong.

**Cost ledger of the μ_n survivor (all real):** RAR 0.108→0.123/0.127 dex + growing χ-shape
systematic; 6 DOF not 2; κ/Z still fitted; Carl's a₀-line / deep-MOND / BTFR untouched but NOT the
surviving kernel; **μ₅ Cassini margin THIN on the alt footing (0.74–0.95×; only μ₁₀ comfortable)**;
bridge degenerates as n→∞ (step kernel inadmissible), window finite-n ~4≲n≲few·10; and **μ_n predicts
null wide-binary EFE (γ_v≈1.000–1.004) → if Gaia DR4 confirms the registered Amendment-10 band
(1.16–1.23), FC-AeST+μ_n is FALSIFIED.** Cassini-safety and a wide-binary signal are the same lever.

**Residual open caveats (could still move it):** (a) the 3.76× is the single-field QUMOND estimate — a
full 6-DOF AeST quasistatic solar-system solve WITH the A_μ vector is NOT committed (vector rescue
judged implausible: fractional corrections, and cancelling ~73% of the scalar Q₂ would also weaken the
deep-MOND monopole the a₀ amplitude references — implausible, not excluded). (b) The a₀²(Q)=−κ²c²G·K(Q)
lock FORM is superseded in-repo (K(Q) dust-like; clock moved to a separate quintessence χ —
kernel-independence survives, the equation does not). (c) AeST c_T/γ_PPN/6-DOF inheritances for the
μ_n-shaped F are asserted-**pending-recertification** ("must re-run"). (d) Keep FC-AeST DISTINCT from
the sibling 2-DOF MMG constraint-first chassis, which IS killed kernel-blindly (γ_PPN=0, α₃=−1;
REFEREE_REPORT_FINAL FAILED) — that verdict does not touch FC-AeST. (e) A χ-channel Cassini load
(0.90/3.88/8.99× for μ_exp/μ₅/μ₁₀, largest for μ_n) flagged in the MMG chassis is unpriced for AeST.
(f) Inherited-open AeST liabilities untouched: c_s² superluminal at SS scales (set by K₂ not kernel),
low-k unbounded-H mode (2109.13287), oscillatory 3rd quasistatic regime (2304.05134).

**ONE-LINE BANK:** The exact-exponential MOND kernel is eliminated by Cassini at 3.76× the ceiling
(the earlier 6.09× was a field-vs-observable error, now diagnosed); FC-AeST *the chassis* is NOT
closed — a sharper μ_n (n≳4) passes Cassini kernel-independently — but the survivor costs 0.127-dex
RAR, 6 DOF, fitted κ, and a null wide-binary EFE the registered DR4 band would falsify. Exclusion is
by sharpness, not smoothness.
