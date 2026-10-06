# Independent norm-cube forcing and physical-regularity review

Accepted as written for the specified cosine seed, zero second-order propagating data, fixed 0<η<1 and compact finite de-Sitter interval. No blocking algebraic or scope error found. This is not exclusion of all initial preparations, weak solutions, flattened-node seeds or the shear-repaired theory.

Pinned REPORT: d713cc02190f56b396ca5769f858353f9a038f883a42aacbf4df57c8cd197788.
Pinned checks: dfad3d500d6a917854c5f895f5259c8c74d6b06f466a74b5ae0bca8854433336.
Audited 2026-10-06 from unchanged raw author inputs; this note is outside execution inputs.

## Action and physical constrained operator reconstructed independently

The n=3 interaction coefficient 2Ka0² times −I^(3/2)/12 and the common volume a³ give −K|∇coordν|³/(6a0), because I=|∇ν|²/(a²a0²). Variation before any constraints yields +K div(|∇ν|∇ν)/(2a0). For ν=vcos(kx), differentiating on positive and negative sine cells gives exactly −Kk³v|v| |sin(kx)|cos(kx)/a0. Its directional amplitude is ε|ε|, so analytic cubic exchange arguments do not remove it. Smooth analytic pure-relative cubic contributions cancel; this nonpolynomial one survives. Common-source admission is a different calculation.

The actual new relative ADM action after both shift/shear rows is c[−A_s(zdot−Hν)²+P(ν+z)²]+Jνν, A_s=−3(1−η)/η. Differentiating this action gives ν=(A_sH zdot+Pz+J/(2c))/(A_sH²−P). Its denominator stays negative and its physical curvature kinetic is Kr=A_sP/(A_sH²−P)>0. Completing the square rather than freezing the lapse gives the source term J(A_sH zdot+Pz)/(A_sH²−P). Its Euler equation is precisely the forced row displayed in the report. There is no spatial smoothing implied by finite-mode lapse solvability.

## Fourier normalization, time limit and remainder

Independent integration over 0<X<π gives cosine coefficient 4/[π(4−j²)] for positive odd j; the zero/even coefficients vanish. The node force is Lipschitz and fails C1 at a gradient zero with nonzero amplitude. The odd force coefficients consequently have J_j=j⁻²J∞a⁻²+O(j⁻⁴), J∞=4Kk³v0|v0|/(πa0).

As j→∞ at fixed compact time interval, Kr→−A_s and the direct source factor P/(A_sH²−P)→−1; the derivative-source factor is O(j⁻²). Substitution in the FULL constrained equation gives
Zddot+3HZdot+2H²Z=C a⁻⁵,
C=J∞/(2KA_s),
with zero Z,Zdot at a=1. Direct differentiation confirms Z=C[a⁻⁵+3a⁻¹−4a⁻²]/(12H²). The numerator factorizes as (a−1)²(3a²+2a+1), so it is nonzero off the initial slice for the declared nonzero seed.

The uniform remainder argument is valid in this restricted setting: write δ=j⁻², factor P=P0/δ with P0 bounded away from zero on the compact interval, and divide the ODE coefficients by the nonvanishing kinetic coefficient. All coefficients and the normalized forcing extend analytically to δ=0 in a uniform neighborhood. The initial data are fixed at zero. Differentiating the finite-interval integral equation or its ordinary parameter-dependent fundamental matrix yields z_j=δZ+O(δ²), with the time derivatives needed for the Bardeen formulas. No infinite-time/high-mode interchange is used. The finite symbolic checks do not themselves prove this uniform statement; the analytic reduction supplies it.

## Why the cusp is physical in the tested correction

The odd series ∑cos(jX)/j²=π²/8−π|X|/4 on |X|≤π is piecewise linear. A uniform O(j⁻⁴) remainder has an absolutely convergent series of second spatial derivatives, hence is C2 and cannot cancel this cusp. The relative Bardeen shift B=t/P=−3(zdot−Hν)/(ηP) is O(j⁻⁴), including its relevant time derivatives, while the lapse equation gives ν=−z+O(j⁻⁴). Thus Φrel=−z−HB and Ψrel=ν+Bdot inherit the nonsmooth term. This is a metric-potential result after constraints, not a bare lapse Hessian or a ghost interpretation. It rules out a classical C2 metric perturbation for the stated zero-data cosine correction on a later interval.

Prepared data or different nodes can change the forcing and homogeneous response. The report correctly leaves those unclassified; in particular a smooth seed flat at gradient nodes can evade this particular norm-cube cusp mechanism. The action's C2 dependence on field jets also does not justify a generic C3 implicit-function theorem.

## Computation/provenance

Independently validated all four current manifests against current frozen inputs. main_a 15/15, control_half_a 11/15 with four intended Fourier-normalization failures, control_smooth_a and control_smoothing_a each 15/16 with the declared false smoothness/smoothing assertion. All validator exits were zero. The checks' limiting-symbol and finite Fourier benchmarks corroborate the proof but do not supply a numerical continuum regularity certificate. No author files, scripts or outputs were modified or rerun.
