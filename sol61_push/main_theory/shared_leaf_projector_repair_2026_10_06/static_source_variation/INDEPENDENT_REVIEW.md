# Independent static shared-leaf source audit

Primary verdict: **proved as written for the action-level static variation and controlled coincident weak-field expansion**. The full matrix differential, individual lapse and metric Euler factors, quartic action difference, cubic source corrections and isotropic mismatch agree with independent reconstruction. This verdict does not admit a globally sourced solution or transfer an observational verdict.

Frozen pins: REPORT.md SHA256 `0052bc7eb27104e64e6a62cf935eb607a32c7ccca64b3536ed21db87a754aaa2`; checks.py SHA256 `5d0bdab6d04fde396ced062347b6c8c8eca80c72cacf4ebde5073b613798f491`. Both were read only. The parent geometric definition was also read directly. This review uses the actual varied interaction, not the author's check counts or imported helper functions.

## Domain and claim card

Both metrics are stationary with zero shifts and positive lapse and positive definite induced leaf metrics. The shared clock is timelike and theta=t, n>=3, K,a0>0, lambda>0. Variations are compactly supported or retain the stated boundary flux. The interaction is 2K a0² v M(I), v=sqrt(NL)(det gamma det gammahat)^(1/4), I=w^T B w/a0², w=grad ln(N/L). h=(gamma+gammahat)/2, d=(gamma−gammahat)/2, H=h+lambda d h^-1 d and B=H^-1. Exact first-variation formulas need differentiability of M on the admitted invariant domain. The weak-order statements use the actual retained envelope with controlled derivative expansion M(I)=−A+I/2−I^(3/2)/12+..., and bounded weak coefficient fields/derivatives, not arbitrary oscillatory differentiable remainders.

Einstein, matter and shear operators are retained. Their full static equations still need solving. Action-level static jets are not claimed to solve those equations. The first-variation clock cancellation and zero static shear are not proof of clock health.

## General matrix differential, including noncommuting metrics

Differentiate HH^-1=identity rather than commute matrices. The product rule gives

delta H=delta h+lambda(delta d h^-1 d+d h^-1 delta d−d h^-1 delta h h^-1 d),
delta B=−B delta H B.

Set z=Bw, q=h^-1 d z. Since h,d and their variations are symmetric,

w^T delta B w=−(zz^T−lambda qq^T):delta h−lambda(zq^T+qz^T):delta d.

This follows by contracting each ordered term: the delta h inverse term is +lambda q^T delta h q, and the two delta d terms are −lambda z^T delta d q and its transpose. It does not require d and h to commute. With delta h=(delta gamma+delta gammahat)/2 and delta d=(delta gamma−delta gammahat)/2, the coefficients are exactly −Ug and −Uh as displayed in the report. Exchange sends d,q to −d,−q and swaps Ug and Uh.

For ONE metric, delta v/v=tr(gamma^-1 delta gamma)/4. Therefore the volume contribution to its covariant spatial Euler density is (K a0²/2)v M gamma^-1, while its invariant term is −2K v M_I Ug. The hatted formula has Uh. The actual stress is 2Egamma/(N sqrt(det gamma)); the factor2 is the covariant metric stress definition, not an extra interaction normalization. The arithmetic comparator has its own coefficient (gamma^-1 w)(gamma^-1 w)^T/2, obtained by varying that individual inverse. Both its I and M(I) must change in an exact comparison.

## Individual lapse rows and boundary signs

Independent log lapses n=ln N,l=ln L give delta v=v(delta n+delta l)/2 and delta I=2(Bw)^i partial_i(delta n−delta l)/a0². Thus the interaction variation is

K a0²v M(delta n+delta l)+4K v M_I(Bw)^i partial_i(delta n−delta l).

Integration by parts gives E_n=K a0²v M−4K div(v M_I Bw), E_l=K a0²v M+4K div(v M_I Bw), with the stated +4K surface flux. Their sum is 2K a0²v M. Normal energy is −E_n/(N sqrt(det gamma)), so omitting the direct volume row would lose the retained vacuum source. These are interaction Euler rows, not standalone Poisson equations or a complete matter-source dictionary.

At a static zero-shift clock variation theta=t+pi, the spatial normal accelerations vary by −partial_i pi_dot for both metrics, independent of their different lapse/leaf metrics. The induced covariant leaf metrics have no linear change on this stationary background: a tilted leaf adds its metric pullback only quadratically. Background acceleration time components vanish; changes of the leaf embedding cannot contribute to the first variation of its squared relative acceleration. Hence delta I=0. Each static extrinsic curvature and shear is zero, so the shear first variation also vanishes. This admits the clock equation at the stated static preparation without supplying a clock kinetic or stability verdict.

## Quartic action and cubic Euler corrections

Expanding h=identity+epsilon h1+..., d=epsilon d1+..., matrix inversion gives

B_lambda=h^-1−lambda h^-1 d h^-1 d h^-1+...,
B_arith=h^-1+h^-1 d h^-1 d h^-1+....

Consequently B_lambda−B_arith=−(1+lambda)epsilon² d1²+O(epsilon³), independently of commuting assumptions. Since w=epsilon w1+..., the invariant difference is −(1+lambda)epsilon⁴ w1^T d1²w1/a0². Using M_I(0)=1/2 and the common leading volume gives the first action difference −K(1+lambda)epsilon⁴ integral w1^T d1²w1. The norm-cube difference is order epsilon5: at a fixed weak coefficient it is a cube of a norm, whose metric change here is order epsilon2. Gradient zeros do not turn it into a lower-order action term. Uniform Euler-order estimates use the report's bounded derivative/controlled-envelope assumptions, not a full C3 smoothness claim at such zeros.

Vary that quartic term directly. Its w derivative is −2K(1+lambda)d1²w1; integrating the log-lapse gradient variation gives +2K(1+lambda)div(d1²w1) for g, and its negative for the other lapse. For a covariant spatial variation delta d=delta gamma/2, variation of w^T d²w gives half of [w(dw)^T+(dw)w^T]:delta gamma. Thus the first g metric Euler correction is −K(1+lambda)[w1(d1w1)^T+(d1w1)w1^T]/2, with opposite hatted sign. Each is order epsilon3. Variation of the common volume contributes only at order epsilon4 to this difference.

The action correction is nonpositive because w^T d²w=|dw|², but a local divergence source has no definite pointwise sign. The leading norm-cube source is order epsilon2 and is unchanged; the new source begins at order epsilon3. This preserves the simultaneous leading weak-field law, not an exact finite-field force or observational calculation. Degenerate leading balances and unbounded derivatives fall outside that order argument.

## Exact isotropic diagnostic

For gamma=G identity, gammahat=Ghat identity, h_s=(G+Ghat)/2, d_s=(G−Ghat)/2, positive G,Ghat imply h_s>|d_s|. Direct inversion gives B_lambda=h_s/(h_s²+lambda d_s²), B_arith=h_s/(h_s²−d_s²). Their difference is exactly −(1+lambda)h_s d_s²/[(h_s²+lambda d_s²)(h_s²−d_s²)]. It is nonzero at mismatch. The radial divergence is r^(1−n)partial_r[r^(n−1)v M_I B r_lapse']; its coefficient and generally its envelope argument differ between the actions. This is an exact action-operator discrepancy; it does not solve the full coupled spatial/lapse boundary problem or quantify a force error.

## Computation audit and verdict limits

I inspected the raw code's noncommuting SPD fixture, ordered inverse derivative, independent lapse/volume rows and arithmetic comparator, second inverse derivative at coincidence and differentiated quartic term. The symbolic fixtures corroborate formulas derived above; they do not prove general-dimensional coverage by sampling. The static-clock check is an equality of its established acceleration variations, not an independent substitute for the geometric derivation above.

Independently validated all four current standard manifests with validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula. Every record returned exit0 and `valid evidence record; mathematical interpretation requires review`. Main_a has22/22. Control_volume_a, control_metric_a and control_flux_a each have22/23 and fail exactly the declared omission/preservation assertion. Frozen report/script bytes remain unchanged.

Passed: general matrix/lapse/spatial-stress variations and normalization; boundary signs; exchange covariance; controlled weak action/source order and coefficient; exact isotropic discrepancy. Conditional: actual static/timelike domain, boundary conditions and retained envelope derivative expansion. Not addressed: conserved-matter on-shell source solution, full source-clock health, finite-field MOND/solar fitting, nonspherical QUMOND equivalence, abundance or coefficient selection.

The first missing physical implication is the new coupled static Einstein/lapse/spatial/clock boundary problem with an actual conserved source and physical metric dictionary. This changed operator cannot inherit the old source solution merely because its leading coincident kernel agrees. The source correction does not select A or32pi.
