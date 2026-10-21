# Scope check: alpha=1 is a tensor-only cancellation identity

This is an independent analytic check of the proposed operator family, not a viable completion or a claim that its full constrained scalar/vector system has been solved. No field evolution or numerical experiment was run for this note. Units are c=1; `C=u^mu partial_mu chi` is the local comoving derivative.

Define

`tau^(alpha)_munu = tau_munu + alpha C sigma_munu`,

with `sigma_munu` the symmetric traceless projected velocity gradient, normalized as `sigma_ij=partial_(i v_j)-delta_ij div(v)/3` in a locally flat rest frame.

## Homogeneous shear identity: verified

For comoving Bianchi I `g_ij=a^2 exp(2 beta_i) delta_ij`, `sum beta_i=0`, and homogeneous chi,

`tau_ij=-C g_ij betadot_i`, `sigma_ij=g_ij betadot_i`.

Therefore

`[tau^(alpha)]^2 = (1-alpha)^2 C^2 sum_i betadot_i^2`,

and the tensor/shear coefficient from the specified tidal square plus Einstein-Hilbert is

`Q_T(alpha)=1-3 gamma C^2 (1-alpha)^2/K`.

The signs and factors agree. Alpha=1 cancels this particular homogeneous-shear correction. It is the only alpha that cancels it identically for arbitrary nonzero C in this family. This statement neither proves all tensor-sector properties on arbitrary backgrounds nor selects alpha from a symmetry/microscopic derivation.

On a static medium, `C=0` and `sigma=0`, so the added tensor `alpha C sigma` vanishes. Its first variation vanishes there as well. Consequently this modification preserves the original static background and first-variation matching; it does not preserve the entire time-dependent perturbation operator.

## Restricted fixed-metric longitudinal kinetic check: verified

Freeze a locally homogeneous C, the metric and the Poisson elimination `delta chi=-K delta rho/k^2`, with no velocity dependence in that elimination. Use a longitudinal mode `v_i=v khat_i` of spatial wavenumber k. With the above shear convention,

`|sigma(v)|^2 = (2/3) k^2 |v|^2`.

The added square then contributes

`Delta L_(v^2,tidal) = -gamma alpha^2 C^2 k^2 |v|^2/(2K^2)`.

This follows from the original coefficient `-3 gamma/(4K^2)`; no hidden factor of two is needed. The mixed term between the original tau(delta chi) and alpha C sigma(v) is not another v-squared term under the frozen elimination. For constant coefficients its longitudinal coordinate-velocity part can be a total time derivative; it must be kept in a complete calculation rather than discarded by assumption when the background varies.

The medium-frame gradient also changes at first order. In the fixed metric,

`D_i chi = partial_i delta chi + C v_i`.

Since `W_full(u)=u^2/(2K)+O(u^3)`, the quadratic W term contains

`Delta L_(v^2,W)=-C^2 |v|^2/(2K)`.

Combining those terms with the nonrelativistic dust kinetic `rho |v|^2/2`, the restricted coefficient is

`L_(v^2)=1/2 [rho-C^2/K-gamma alpha^2 C^2 k^2/K^2] |v|^2`.

Thus alpha=1 removes the displayed tensor deficit while introducing a negative, k-dependent velocity-gradient contribution in this restricted longitudinal calculation. For nonzero alpha and C with gamma>0, the displayed coefficient formally becomes negative at sufficiently large k; if its k=0 value is already nonpositive, there is no positive starting coefficient in this restricted approximation. Whether any crossing lies inside a valid EFT range is a separate question.

## Why this is not yet a ghost verdict for the proposed repair

The calculation freezes exactly the pieces that must now be restored: lapse/shift/metric constraints, multiplier and chi perturbations, variations of the medium projector, background time dependence, and the full velocity/density dependence of the covariant constraint. Eliminating those fields may change the reduced kinetic matrix and its degree count. A frozen Poisson substitution on a time-dependent chi background is not automatically the on-shell constraint reduction of the new covariant action. Kinetic signs cannot be inferred from one unreduced sub-block alone.

The safe conclusion is therefore:

**Alpha=1 is a proposed cancellation of the verified homogeneous tensor defect, with unchanged static first variation. It is not an established repair. The next gate is the full mixed scalar/vector/tensor quadratic action and constrained kinetic/principal-symbol analysis on the actual FRW chi background.**

That gate must also check the current-vector/current-density normalization and the original projected-Hessian constraint's time derivatives. It should preserve both the successful tensor identity and this adverse fixed-metric high-k diagnostic; neither may be promoted into a verdict on the full constrained system without the reduction.
