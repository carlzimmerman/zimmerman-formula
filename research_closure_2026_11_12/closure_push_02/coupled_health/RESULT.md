# CP02 coupled-health result

**The metric constraints do not provide a universal rescue of the flat density gate.** An explicit regular finite-density constraint solution, with `Q-1=10^-6` and active positive stiffness, has a physical scalar principal speed squared `-2.90764228269e-6`. Its growth rate is proportional to wavenumber and can exceed the expansion rate without bound when the action is used without an independently specified ultraviolet cutoff. This is stronger than a negative auxiliary polarization block and is not ordinary bounded Jeans growth.

The derivation also finds a surviving principal region. A second constraint solution with larger stiffness has positive scalar kinetic and gradient coefficients. It does not establish all-wavelength or nonlinear stability, formation, or preservation of that region.

## Exact reduction and scope

`DERIVATION.md` derives the action from the QX17 ADM form, imposes tangency, retains lapse, shift and metric scalar, and eliminates the actual constraints. On flat FRW, including nonzero gate derivatives,

```text
S2 = 1/2 integral a^3/h^2 [A(k) dot(zeta)^2 - q H_Q k^2 zeta^2],
A(k)=q²H_QQ + c²k²/(K-Dk²),
c=1-H_Pi+qH_QPi,  D=H_PiPi-Gamma.
```

The one-sided original stiffness has no single Hessian at FRW Pi=0; Gamma there must be zero or an explicitly smooth stiffness. The flat `exp(-u³)` gate has zero first and second derivatives at zero and passes this FRW quadratic test. The full time-dependent curvature equation must be used for cosmological evolution; its positive gradient coefficient does not exclude Jeans growth of density perturbations.

At a finite positive-Pi regular center, with an actual constraint solution and gamma active,

```text
c = 1+gamma Pi-H_Pi+qH_QPi,
D = H_PiPi-gamma,
A_infinity = q²H_QQ-c²/D,
n_eff = qH_Q+Pi(1+gamma Pi-H_Pi),
omega² = (n_eff/A_infinity) k² + lower-order terms.
```

An independent partial Legendre reduction of the fast P constraint gives the same physical lapse Hessian. The center clock-current equation equals the Einstein energy-conservation condition, so the chosen initial constraints do not conceal a current/momentum contradiction. No later-time background evolution was simulated.

## Executed constrained examples

Both use dimensionless `K=a0=Pi_c=Pi(0)=1`, `C=10^6`, `q=1.000001`, `H=C(q-1)^2 exp[-(Pi/Pi_c)^3]`, and a regular spherical patch of radius `10^-5`. These are examples of the specified action family, not fitted galaxy parameters.

| Quantity | Unstable example | Surviving principal example |
|---|---:|---:|
| Active gamma | 1e-8 | 1e-5 |
| D | 1.09363832333e-6 | -8.89636167667e-6 |
| A_infinity | -596965.019395 | 899590.858323 |
| n_eff | 1.73576073168 | 1.73577072168 |
| Scalar speed squared | -2.90764228269e-6 | 1.92951129463e-6 |
| Maximum K|P|/a0 | 3.333303e-6 | 3.333337e-6 |
| Relative variation of Pi over patch | 1.52404e-5 | 1.87343e-6 |
| Hamiltonian residual | 4.23e-15 | 6.15e-15 |
| Divergence residual | 2.76e-14 | 2.65e-14 |
| P-equation residual | 1.68e-8 | 2.29e-7 |

The residuals independently finite-difference the integrated fields. At k=1e8, k times patch radius is 1000 and the unstable principal growth rate is about158,515 times the expansion rate. The finite-k kinetic coefficient differs from its asymptotic value by about2.05e-10 relative. The positive-Pi branch and W amplitude domain hold throughout both integrated patches.

## Family consequence and surviving requirements

`FAMILY_OBSTRUCTION.md` proves the curvature lemma for every strictly positive, nonconstant, nonincreasing C2 gate with S'(0)=0. It then combines the finite-center principal coefficient with the exact large-q limit

```text
A_infinity/(Cq²) -> 2S-S'²/S'',
n_eff/(Cq²) -> 2S-uS' > 0.
```

At a point with `0<S''<S'²/(2S)`, sufficiently large finite q gives the same short-wavelength obstruction for any fixed finite gamma and Pi_c. Thus global health over the unrestricted local state/wavelength domain fails for this quadratic-clock gate family. This is not a theorem against all modified-gravity theories or a demonstration that every observed halo enters the bad region. The separate near-Newtonian example shows that failure need not require a large clock offset.

For H_QQ>0 and n_eff>0, D<0 is a sufficient condition for positive scalar principal kinetic/gradient signs in this construction. If D>0, one needs `q²H_QQ D>c²`. These are principal conditions, not a full health certificate. A trajectory entering D>0 through a point with c!=0 passes immediately into A_infinity<0. Avoiding that requires a preserved domain, a special vanishing of c at the crossing, or a changed action/domain. No such preservation law or physical cutoff is derived here.

## Verification and provenance

- `check_coupled.py` performs14 symbolic checks, including direct gate-density second variation, an independent ADM Kij matrix contraction, elimination of all three scalar auxiliary constraints, the Einstein time-dependent cross term, metric/lapse stresses, and the Hamiltonian/partial-Legendre comparisons.
- Two regular spherical Hamiltonian/P/divergence systems are integrated and their constraints independently finite-differenced. The momentum constraint is analytically zero for spatially constant extrinsic expansion because the reduced matter action is shift-independent.
- Three mutations remove H_Pi from the mixing, remove active stiffness, or omit the Einstein time integration by parts; each fails its intended identity.
- The accepted bounded execution is `v2_health_run_001`, produced by the standard computation-audit runner and validated against its v2 manifest schema. Fresh mutation executions are in `v2_mutation_*`. Their nested `payload/result.json` files hold the actual results. Earlier `run_001`–`run_003` and `mutate_002_*` directories are preserved custom-metadata executions; their hashes were checked, but they were not canonical runner records.
- `SOURCE_CHECK.md` records primary-paper checks of the ordinary Einstein/clock limit. Those papers do not prove the new density-gate result.

The [independent audit](../health_audit/RESULT.md) reconstructed the geometry, stress/current constraints and principal elimination without importing this checker. Its27 checks support the scoped principal and family results. It found a cubic radial-series omission, now corrected in the derivation; the original W gives a C2 center, not an asserted Cartesian C-infinity one. The finite numerical results are unaffected. The analytic claims and their exact hypotheses are in the derivation and family files. No coefficient normalization, lensing prediction, late-time formation solution or global nonlinear evolution is claimed. A subsequent repair investigation is isolated under `repair/` and does not alter these accepted results.
