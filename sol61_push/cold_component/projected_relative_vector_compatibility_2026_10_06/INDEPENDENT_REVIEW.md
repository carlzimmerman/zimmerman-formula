# Independent vector compatibility audit

Accepted as written for the unchanged projected action, declared pure-decay scalar preparations and allowed flat additions. No blocking mathematical error found. The result does not classify every multishell preparation or a changed clock action.

Pinned REPORT: b8b2a17380f06f52f88c0e00d6c8e3d38c825795c47e84f4be60cd48b06d73e0.
Pinned checks: 64dd8e10cb73d62f9c8a4c58d67b73c29fab73c1490e9c66b33b6be3341e768d.
Audited 2026-10-06, read-only author inputs; this review is not a runner input.

## Raw reconstruction

For a transverse plane vector, mixed extrinsic curvature has off-diagonal entries ∂W/2. Its trace vanishes and its square is (∂W)²/2. The exact flat spatial pullback has unit determinant, so the leading projected acceleration and vacuum-volume difference give no vector quadratic term. The two Einstein sectors evaluated at opposite half-amplitudes consequently give Ka³k²(Fdot−S)²/4 in coordinate-wave-number normalization. Transverse shift variation sets S=Fdot at k≠0. This does not promote the remaining relative flat direction to a nonlinear independent diffeomorphism. Allowing all smooth divergence-free shifts is a legitimate generous rescue class.

I independently recovered the scalar clock current from the previously reconstructed normalized-clock/temporal-Noether variation:
Eθ2=2Ka div[(Δν)ΔS+νdot∇ν].
For ν=f/a on one shell, Δf=−k²f and ΔSscalar=2H∇ν/k². Its scalar divergence is −3H div(ν∇ν). The extra transverse contribution is −k²V·∇ν. At a nonzero extremum of a nonzero real compact eigenfunction it is zero, whereas the scalar contribution equals 3Hk²ν². The exact Euler density is therefore 6KaHk²ν² there. The proposed longitudinal cancellation has divergence 3Hν and violates the transverse premise; scalar constraints have already fixed it.

For arbitrary zero-mean f let w=Δf, u=(−Δ)⁻¹f. Direct substitution, without imposing a common wave number, gives
V·∇w=(H/a)div[f∇f−2w∇u].
Testing weak divergence-free V against the smooth periodic primitive of G(w) proves ∫G(w)R=0. This is a necessary, not sufficient, condition. I reproduced the two-shell integral independently with Laurent-Fourier convolution instead of importing the author's trigonometric integration. For f=cos x+αcos2x it gives
∫w²R dx=−3π(64α⁴+40α²+1)/2,
strictly negative for every real α, including α≠0. Unweighted averaging alone is blind.

At an eigenfunction extremum, the allowed frozen shift −∇Z0/(Ha²) contributes k²fΔZ0/(Ha³), and the actual homogeneous lapse c0+c3a⁻³ contributes 3Hk²c3f/a⁴. The pure decay contributes 3Hk²f²/a². Their distinct powers cannot cancel on an open interval; arbitrary time dependence of the transverse shift remains ineffective at that extremum. For the weighted two-shell test the same time-power separation applies because the transverse weighted integral is identically zero at each time. This is not permission to substitute an arbitrary homogeneous lapse history for a constraint-admitted one.

## Constraints and scope

The old-action linear clock Euler functional vanishes identically at coincidence, so a nonzero quadratic residue cannot be balanced by regular second-order corrections in that action. This is a Noether compatibility obstruction, not a new independent equation or an inferred ghost. Additional preparations not covered by the stated weighted sign argument remain open. In particular an explicit shear-clock deformation changes the linear operator and invalidates that premise; its admission must be audited separately.

## Computation audit

Independently validated all four current manifests against current inputs: main_a 20/20; control_time_a, control_longitudinal_a, control_weight_a each 19/20 with its declared single failure. All validator exits were zero. Raw ADM normalization, compact extremum and weak-test proofs, not those finite counts, support the report's uniform claims. No author scripts were rerun into their output directories or changed.
