# CA4-GNC-PQ action audit addendum

The earlier 120-check action closeout is preserved unchanged. This addendum
records the subsequently requested quadratic repair, defined solely in
`VACUUM_STIFFNESS_VARIANT.md`. CA4-GNC-P is not retrospectively assigned
the improved de Sitter result.

`check_pq.py`, `pq_contract.json` and `pq_run1/` give 27 additional exact
SymPy checks, all passed. The computation-audit runner completed with exit
zero, and the manifest validator accepted the evidence record. Checks
include full lapse/source/projected stress, the h-volume gauge identity,
unchanged homogeneous first variation, canonical Hessian increment, actual
de Sitter quadratic normalization, lapse reduction, time integration of
the mixed term, and the all-wavelength stiffness factorization. No random
sample or empirical campaign was run.

The all-finite-nonzero-mode inequalities are analytic: for the explicitly
restricted window `0<alpha<=1`, `0<ell<=1`, `eta<=1/10`, the report proves
`0<d<=123/80<2` and `d+2+2u d_u>=3/5`. The independent evolution agent
received these bounds before this report was frozen. The starting on-shell
ADM expansion is the evolution lane's `frw_check.py`; this action lane
independently derives the added term and the resulting reduction, rather
than repeating the complete ADM expansion.

Root's `assembly/VACUUM_STIFFNESS.md` extends the fixed-data positive-floor
barrier proof. This lane read and checked the multiplier change
`q+tq'=3A(t-2/3)^2-A/3`, the changed multiplier bound and the minimum-point
inequality using `t_min<=1`. Those steps are consistent with the prior
smooth compact fixed-data hypotheses. The result is not a propagated
bound for the simultaneous U/lapse/metric equations.

The exact new source is `sigma_PQ=rho_P/t-2V0 zeta z`; the lapse instead
sees `rho_P+V0 zeta z^2`. All future uses of the repaired action must retain
these changed equations and the extra projector stress. The homogeneous
vacuum stress remains unchanged, while its scalar second variation is
changed by construction. There is no new field and no new dimensional
scale, but there is an explicit new constitutive choice `zeta=4/ell-1`.

The improved result applies to the actual zero-excitation vacuum de Sitter
branch. Zero-mode coercivity, excited/inhomogeneous backgrounds, complete
Dirac count, global evolution and original empirical requirements remain
open. The 27 new checks plus the earlier 120 span different actions and
scopes; they do not constitute 147 proofs of one completed theory.

`pq_evidence.json` pins all new source and run hashes and the observed HEAD.
No old script, run, action definition or completion record was changed for
this addendum. No commit was made.
