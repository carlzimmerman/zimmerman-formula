# FSP-008 sea-flavor completion result

**The complete leading sea insertion has been reduced to an explicit estimator.
Its QCD expectation values have not been evaluated, so this does not calculate
the proton mass derivative, the global vacuum coefficient, their ratio, or
alpha.** No numerical alpha, cosmological target or mass-ratio fit was used.

Let delta=ms-ml, let B be the full proton contraction at e=0, and let source
derivatives include all current contacts. With S_l and S_s the propagators on
the actual same 2+1 gauge field, define

\[
T_a=\operatorname{Tr}(S_lS_sV_a),\qquad
h_{f,ab}=\operatorname{Tr}(S_fW_{ab}-S_fV_aS_fV_b).
\]

The exact additional sea kernel beyond the valence-only <B_ab> is

\[
\boxed{C^{sea}_{ab}=
 \operatorname{Cov}(B,5h_{l,ab}/9+h_{s,ab}/9)
 +\frac{\delta}{3}\{
 \operatorname{Cov}(B_a,T_b)+\operatorname{Cov}(B_b,T_a)\}
 +\frac{\delta^2}{9}\kappa(B,T_a,T_b).}
\]

This is an identity at the chosen finite regulator, without an expansion in
the physical strange-light splitting. The same-loop term survives at equal
masses. The previously omitted mixed class starts at the first allowed order
delta, while the two separate sea-current loops start at delta squared.
These are local orders near the SU3 point, not a numerical suppression bound
at physical ms/ml; propagators, baryon normalization and infrared gaps may
vary strongly with mass, curvature and volume.
These statements include normalization by the sea partition function; merely
multiplying traces and subtracting one vacuum product loses terms when the
one-current means are nonzero. The full third cumulant is retained here.

The exact light-strange resolvent identity and split-even noise strategy are
**known after notation translation**, authenticated in Harris et al.,
[arXiv:2301.03995v2](https://arxiv.org/abs/2301.03995v2), equations (11)-(19).
The current revision is from 1 May 2026 and corrects the approximate variance
formula (8). No such variance factorization is needed for this derivation.
The useful extension for this programme is the explicit normalized-baryon
formula above, its contact inventory, and the corresponding same-regulator
vacuum insertion. No novelty priority is claimed.

The actual sea completion is computationally actionable: estimate the
split-even trace with delta/3 already outside it; use independent noise pools
or off-diagonal noise pairs for the two-trace product; retain the same-loop
composite trace and W contact; form the proton covariances and cumulant on
the same configurations. This avoids subtracting independently noisy light
and strange loops. It does not remove gauge noise or the need for all
spacetime/tensor separations and their photon convolution.

For the unconditioned vacuum there is no valence term or mixed valence-sea
term. The leading effective insertion is

\[
I_g=-\tfrac12G_{ab}(g)
 [5h_{l,ab}/9+h_{s,ab}/9+\delta^2T_aT_b/9]+S_u^{ct},\quad W_u=\langle I_g\rangle.
\]

On a radius family with t=log(radius),
\(\rho_u=[\langle I_{g,t}\rangle-\operatorname{Cov}(I_g,T_g)]/(4V)\).
The derivative of the photon inverse, the current vertices, the measure and
all local metric/parameter contacts is part of I_g,t. A flat-volume sea
kernel cannot be substituted for this global curved-space response. The
strong-scale and quark-mass matching directions must be applied consistently
to both proton and vacuum. No identity makes this whole sea insertion a
pure strong-scale retuning.

A newer independent primary demonstration confirms that complete sea
contractions and matching are feasible in a different observable: RC*,
[arXiv:2506.19770v1](https://arxiv.org/abs/2506.19770v1), Appendix A (A.6) and
Sections 5-7. This is a full-sea QCD+QED/RM123 comparison of an HVP window at
unphysical masses, one spacing and volume, with C* boundaries and a charm
quark. Its SU3 light-flavor cancellations leave charm contributions. Its
numbers are not imported as proton or curved-vacuum data. In a theory with
charm or other heavy quarks, their determinant terms must be added to the
three-flavor formula above.

## Exact finite check and its scope

The [bounded run](run_001/manifest.json) completed and its v2 manifest validates
against the current frozen inputs. The test used exact rational arithmetic,
three explicit noncommuting 2x2 matrices, two source directions, nonzero
second-source contacts, four mass splittings and exhaustive Rademacher noise
averaging. **All 174 assertions passed.** An independent determinant/adjugate
source-jet construction agrees with the normalized topological decomposition
for every declared source pair and splitting. The test also exhibits:

- a surviving same-loop covariance at exact degeneracy;
- nonzero first allowed mixed and separate-loop coefficients;
- a nonzero error from dropping the W contact;
- a nonzero error from replacing the third cumulant by an ordinary covariance;
- finite-noise product bias that disappears with independent noise pairs.

This is a finite algebra benchmark, with no spacetime, QCD gauge ensemble,
physical proton or H limit. It validates the implementation and finite
identities in the declared range; it cannot establish the global QCD response
or its convergence. No expensive simulation was run.

The remaining physical evaluation is explicit rather than hidden: the
covariances/cumulants in the boxed formula over actual QCD configurations,
their fully matched photon convolution, and <I_g> plus its metric contacts on
the specified curved geometry. Even after those are computed, a controlled
small-H limit and higher electromagnetic orders are required for the requested
full ratio and finite-alpha dependence. The leading derivative would obey
R_u=A_u/M^3-3A M_u/M^4 and dR/dalpha|0=4pi R_u if the relevant limits exist.

A separate [residual bound](RESIDUAL_BOUND.md) controls the two omitted
classes by measurable gauge variances using Cauchy–Schwarz. No such variances
are available here, so this supplies an actionable stopping/error criterion,
not a numerical physical error bar.

See [DERIVATION.md](DERIVATION.md), [source receipts](SOURCES.json),
[computation contract](COMPUTATION_CONTRACT.json), and [reproduction](REPRODUCE.md).
