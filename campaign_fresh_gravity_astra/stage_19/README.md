# Checkpoint: finite pressure ambiguity survives bounded response error

2026-09-30, 13:29 UTC pass. Parent: [stage eighteen](../stage_18/README.md).
FGF031 changes the exact-response premise of FGF029 while keeping the same
fifteen annuli, sixteen free pressure coefficients, fixed offset and support.
No new response map, support extension or pressure fit was computed.

Let H=[U,c], with U the saved invertible15x15 response, and target [L,0].
For real errors E,e use the induced matrix infinity norm (maximum absolute
row sum) on E and the vector infinity norm on e. These differ from maximum
entrywise matrix error by a possible factor15. Exact rational interpretation
of the saved binary64 entries supplies the constants; an analytic inverse
bound then covers every real perturbation in the specified ball.

The author certificate uses radius approximately1.170742196159423e-6 for
both norms. An independent pivoted rational LU computation and sharper
row-target bound certify the simple radius1e-5. At that latter radius the
null direction's target response has lower bound approximately0.15712815903088392, strictly
positive. Thus target ambiguity persists throughout this finite uncertainty
set. These are sufficient radii, not optimal thresholds or measured errors.

The independent certificate uses a rational inverse-square synthetic
baseline and one common pressure step approximately5.366049012969053e-9.
Every allowed operator admits two strictly positive decreasing profiles,
including the last free node to the fixed-zero endpoint, with identical
bins and target separation with lower bound approximately1.6863148053546381e-9. The operator is
the same for both profiles in each pair. The pair and its synthetic bins
can vary across operators; this is not an actual-data confidence interval.
The author uses the inherited exponential baseline, so its smaller step
and separation are different synthetic witnesses, not conflicting estimates.

Root separately proved and independently audited the uniform inequalities.
A stronger fixed-nominal-synthetic-data version needs a baseline correction
and the extra strict-gap condition2A<m. No numerical radius is certified for
that stronger version in this pass. Failure at a sufficient-bound threshold
means inconclusive, not that identification has been restored.

## Units correction and provenance

The original FGF019 definition is p(x)=C_SZ R_t P_e(R_t x), x=r/R_t,
C_SZ=sigma_T/(m_e c²). Saved p and target dp/dx are dimensionless; physical
electron-pressure gradient is (dp/dx)/(C_SZ R_t²). The auditor's frozen plan
incorrectly called p keV/cm³ and x=r/R500. Root briefly relayed that label;
author caught it and root verified the original derivation/code. The frozen
note and explicit correction are preserved. No matrix or executed code was
silently rescaled; the arithmetic contained no such unit conversion.

Two bounded exact-arithmetic manifests validate. Author uses rational
Gauss-Jordan inversion; independent auditor uses pivoted rational LU and
triangular solves from original matrix bytes. Norms, nominal direction,
target response and the author's radius agree exactly. Each process uses
120s wall,110s CPU, cooperative one-library-thread cap and1MiB logs; no memory
cap is claimed. Root proof audit is not another computation. The independent
auditor discloses receiving an author formula preview after reasoning but
before its filesystem freeze; code and numerical implementation were separate.

- [Root uniform proof](operator_audit/ROOT_DERIVATION.md)
- [Root proof audit](operator_audit/INDEPENDENT_AUDIT.md)
- [Normalization correction](operator_audit/UNITS_RECONCILIATION.md)
- [Independent computation and review](independent_audit/INDEPENDENT_AUDIT.md)
- [Scoped reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-031_RECONCILIATION.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)

The bounds cover U,c uncertainty only in the fixed basis/target/row convention.
They do not establish actual instrument, beam, geometry, target-functional,
continuum, covariance or calibration errors. Agreement between implementations
is not that error budget. A calibrated outer-pressure datum sensitive to the
remaining direction is also missing. No gravitational force or mass is inferred.
Later conversion must retain density/composition calibration, both a0 values,
separate vacuum/H histories and distinct Q/RAR/registered M source laws.
No physical metric, observation or gravity-theory closure follows.

This finite robustness route stops here; no further radius/support/annulus
sweep or duplicate child was added. FGF034's fixed-mass, fixed-wall equilibrium
response is next. Actual calibration work remains gated on authenticated input,
and the AS228 metric repair remains with its existing primary owner.
