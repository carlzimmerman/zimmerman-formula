# Independent review of projection and conservative solver diagnostics

**Verdict:** the pinned projection formula, canonical field factors, carrier transformation, angular extraction, and C v2 positive-face energy partition are consistent. The saved synthetic controls validate a conditional linear coordinate. They do not identify a merged, near-stationary remnant or prove that an actual collision stores persistent mode energy. No pair, eigenvalue, BVP, outgoing, or snapshot-extraction experiment was rerun for this review.

`sources_review_projection_solver.json` pins 15 inputs and records 37 passing independent saved-cache/algebra checks (56.4 MB measured RSS). The original synthetic run has 28 passing checks; its v2 manifest validates, and its recorded input/output hashes match. C v2 preflight has 27 passing saved checks and matching manifest input/output hashes. These three check counts refer to different audits, not 92 independent physics experiments.

## Canonical projection and carrier gauge

For real canonical reduced variables in order `(u,s,xi,v,t)`, the linear equation is

    q_tt + G q_t + W q = 0,
    G^T=-G, W^T=W, (W-Omega^2+i Omega G)Z=0.

The momentum is p=q_t+Gq/2. With R=(Z,(i Omega+G/2)Z), the complex bilinear symplectic product gives

    S(R*,R)=2i Omega <Z,Z>+<Z,GZ>=i kappa/Omega,
    kappa=Omega^2 <Z,Z>+<Z,WZ>.

Consequently

    c=-i Omega/kappa <Z,v+(G+i Omega)q>,
    q_mode=2 Re(cZ), v_mode=2 Re(i Omega cZ).

This confirms the code's sign, gyro term, velocity term, dr measure, and absence of an extra factor two. The cached Q160000 mode independently gives kappa=0.9999999999998856 from the QEP identity. Three exact linear snapshot states recover their prescribed real/imaginary complex coordinates within 1e-10, without reconstructing W, solving an eigenproblem, or invoking the extraction implementation. For the unit-kappa cache, |c|^2 is the quadratic excitation K of a valid isolated linear mode.

The charged fields use sqrt(2) canonical real/imaginary components, while xi is unscaled. The code correctly transforms both lab velocities:

    Psi_rot,t = exp(-i theta) Psi_t - i omega_used Psi_rot,
    X_rot,t   = exp(-2i theta) X_t - 2i omega_used X_rot.

Its instantaneous carrier-frequency estimator is the least-squares projection on the shared U(1) generator `(i Psi,2i X)`:

    omega_fit = integral[Im(Psi* Psi_t)+2 Im(X* X_t)]
                    / integral[|Psi|^2+4|X|^2].

The weighting and charge-two phase lock are correct. The Psi reference overlap chooses the common phase; X supplies a lock diagnostic rather than an independently fitted phase. The Noether inventory correctly uses twice the numerator density. Neither that estimator nor a high overlap coherence proves stationarity.

**Frame acceptance:** if omega_used differs from the cache's omega_reference, the transformed velocity is not the velocity in the frozen reference frame used by W/G. The code reports the mismatch and keeps G pinned, which is transparent, but a physical modal-energy interpretation needs `carrier_frequency=omega_reference` and sensitivity to the fitted value, or a newly matched stationary reference/cache. A substantial carrier mismatch is not cured by labeling the same coordinate K. A static `center_z` shift is supported; centre-velocity/Lorentz rest-frame correction, moving reference-family derivatives, and time-dependent recentering derivatives are not implemented. They must be negligible or handled before physical interpretation.

## Spherical interpolation, reconstruction and saved controls

The angular coefficient is correctly normalized as

    q_20(r)=r 2pi integral[-1,1] Y20(mu) delta z(r,mu) dmu.

Gauss-Legendre quadrature, the radial dr measure, field ordering, and the extra r factor agree with the radial mode. Cell centres are mapped consistently from the 32-byte CEPAIR1 header and ten array order. The reader checks complete byte length, and the sample routine pads the regular cylindrical axis by even reflection. It rejects nonfinite samples; the declared outer margin keeps the interpolation stencil inside the actual grid. Cubic interpolation near the axis and background-to-evolution-grid anisotropy remain convergence errors, not exact symmetry identities.

The supplied continuum Hermite profile differs from the mode's finite radial-grid background by max absolute 0.000112398980. This is reported rather than hidden. A purely spherical mismatch cancels in the ideal angular ell=2 integral, but cylindrical sampling and nonlinear/grid anisotropy can leak it into a coordinate. The saved centred spherical negative control measures one such false signal; an actual evolved control is still required.

The saved synthetic run uses a common carrier phase 0.37 and known |c|=0.1 at phases 0.2 and 1.1. Fine dx=0.2 complex-coordinate relative errors are 1.0364e-5 and 1.0377e-5; the matched dx=0.4 case gives 3.2742e-4. The spherical negative control gives false |c|^2=1.0777e-12. Reconstruction residual fractions for the fine perturbed examples are about 3.8e-10. These are meaningful centred coordinate/interpolation/velocity controls. The generator and analyzer share the same cached eigenvector and profile, so they are not an independent validation of that eigenpair or reference action.

The reported reconstruction residual is

    integral[Omega^2 |q-q_mode|^2+|v-v_mode|^2] dr.

It is a positive displacement/velocity state norm, not an energy assigned to unmeasured modes. The separately reported full canonical field mismatch likewise includes the chosen reference mismatch and monopole/nonlinear structure. It is not a bound-charge or energy decomposition. Fractions obtained by dividing a nearly zero reference signal are not informative.

The support diagnostic is an ordinary modal L2 fraction. For a truncated sphere it is not exactly the truncated symplectic normalization or an error bound on c; the denominator remains the full cache kappa. Actual use needs negligible tails in the relevant canonical/symplectic measures and aperture sensitivity, rather than automatic renormalization by the L2 fraction. The current synthetic data include the full reduced cache through r=59.95.

Translated reference rejection, boosted/rest-frame rejection, independent angular-order refinement, reference-charge mismatch sensitivity, and time-series persistence were not demonstrated by these four synthetic snapshots. The derivation appropriately lists further controls; its list must not be read as completed evidence. Near-axis peak counting and enclosed charge fractions are descriptive diagnostics: they do not by themselves distinguish a bound single core from a broad/two-core/transient configuration. The synthetic snapshot need not have total Q exactly equal to its Qref label, because it contains finite-grid quadrature and raw quadratic mode charge; no fixed-total-Q initialization is claimed by that control.

## Axisymmetric loss coefficient

The normalized product coefficients in the derivation check:

    Y20^2=D0 Y00+D2 Y20+D4 Y40,
    D0=1/sqrt(4pi), D2=sqrt(5)/(7sqrt(pi)), D4=3/(7sqrt(pi)).

For H=(Y22+Y2,-2)/sqrt(2), the earlier standing source has the same D0, the opposite ell=2 coefficient, and ell=4 weights satisfying

    D4^2 = C4^2+C44^2/2 = 9/(49pi),
    C4=1/(14sqrt(pi)), C44=sqrt(5/(14pi)).

Spherical-background outgoing response is diagonal in ell and degenerate in m; its leading energy sums squared angular source weights. Therefore Y20 and this real standing pattern have equal **summed leading unit-K gamma**, for the same radial mode, background, frequency, outgoing conditions and weak-amplitude reduction. This is a valid new angular calculation; it is stronger than merely guessing a standing coefficient for an m=0 mode. It does not make their angular/DC fields identical, transfer the chiral gamma, or justify applying gamma to a strongly nonlinear collision's total excess energy. All axisymmetric outgoing sectors have m=0 and zero intrinsic Jz.

## C v2 action and positive-face partition

The reviewed original C SHA256 begins `228e28c8`; C v2 is `f4e8f96ad1f97a6bc506b4301e441ac696b46bd53d6c5a811d006cfee3360058`. The diff changes diagnostics only. Forces, Lorentz seeds and kick-drift-kick evolution remain unchanged. An independent sub-audit by `/root/isolated_binding/charge_backreaction` agreed with the following source-level conclusions; this report also independently checks the face identity on a deterministic toy array, without evolving fields.

With volume weights w_i=2pi R_i dx^2, radial link weights are 2pi R_face and axial weights 2pi R_i. They are symmetric between adjacent cells, so L is self-adjoint. For each canonical factor fac (1 for complex real components and 1/2 for chi), the new cell gradient term is the weighted sum of half each adjacent positive squared face difference. Interior faces are counted twice with factor 1/2; the regular axis has zero radial face weight. At an outer zero-Dirichlet face the odd ghost gives difference -2q and a half contribution 2q^2, precisely the doubled boundary penalty of the original -sum w fac q Lq. Thus the positive-face total equals the global gradient quadratic. All full-action potential and neutral derivative factors match `common_action.py`.

The unchanged kick preserves the charge-one/charge-two interaction charge: its torques obey T_Psi=-2gB and T_X=gB, where B=Xi(Pr^2-Pi^2)-2Xr Pr Pi, hence T_Psi+2 T_X=0. Weighted spatial torques cancel globally, and drift preserves each field's coordinate/momentum area. This establishes algebraic global U(1) conservation up to floating point error, not exact KDK energy conservation. The Lorentz seed also checks: r'=sqrt(R^2+gamma^2 z^2), r'_t=-gamma^2 v z/r', theta=alpha-omega gamma v z, theta_t=omega gamma; X has twice the phase/frequency. Interpolated profiles and a sum of overlapping fragments remain approximate initial data.

E10/E15/E20 select cells by strict spherical radius about the **fixed origin**. Faces crossing an aperture are split between their two adjacent cells. Eout20=Eface-E20 is a consistent complementary energy partition. It includes translating fragments, bound tails and returning waves, and is not an outgoing-flux or unbound-radiation measurement. The moving single-fragment aperture is not comoving. The old pointwise -qLq quantity was valid for a global sum but not a positive local density; v2 correctly fixes that localization issue.

Closed boundaries reflect waves. At radial size 80, fastest waves can return toward the centre after roughly t=160, subject to their emission location/time. T240 outcomes need box/time/flux controls. Massive slow waves can take longer, but a speed-one bound is the safe causal test for broadband collision emission. KDK energy needs timestep convergence, especially with M=100; Pz is a continuum-style finite-grid diagnostic rather than an exact discrete invariant.

## Permitted interpretation of subsequent snapshots

Actual pair snapshots were not interpreted in this review. Before |c|^2 is called merger-excited persistent mode energy, establish one near-stationary core, measured bound charge and rest frame, a sufficiently close same-action/grid reference, signal above isolated static/moving artifacts, and a coherent fundamental across multiple snapshots/windows with static and harmonic components resolved. Report the projected reconstruction and its reference/aperture/grid/frame sensitivity. Charge/energy leaving an aperture must be reconciled with actual flux and possible return.

A head-on axisymmetric run is a bounded zero-orbital-J m=0 experiment. A successful outcome would establish that specified collision's excitation channel under these controls; it would not determine generic impact-parameter/phase branching, physical merger rates, galactic orbital torque, or the four-dwarf budgets.
