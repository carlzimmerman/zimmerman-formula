# Independent audit of the root fixed-unit Q certificate

Reviewer: /root/pressure_extrema. Verdict: **accepted conditional analytic
certificate, with the scope below**. No algebraic correction is required.
I read only ROOT_DERIVATION.md and check.py for the proof review, then the
root's completed run_001/results.json and manifest.json. I did not read the
new worker derivation, code, or other independent-audit outputs. I did not
rerun the numerical certificate. Source and observed-output hashes are pinned
separately in audit_result.json.

## Common physical units

The same a_c and c_s define L_c=c_s²/a_c, t_c=c_s/a_c and rho_c for every
reference. Thus g/a_c, B/a_c and a/a_c are f,b and alpha exp(chi). J=c_s^4
gives J/L_c²=a_c²; S0/a_c²=1. The scale potential therefore acquires no
alpha² factor. With K=c²/c_s², the scalar kinetic density K phi_t²/c² has
scale a_c². With v_chi=c_s, J chi_t²/v_chi² has the same scale. Fluid kinetic
density rho xi_t² divided by a_c²/(4 pi G) has weight r, since L_c/t_c=c_s.
After integration, the common energy scale is E_c=a_c c_s²/(4 pi G).
These calculations support the stated N and both unit field weights under
the inherited action normalization; I have not rederived that action here.

The four reference values fit inside alpha in[1,11/5]. The two rational a0
values have ratio112790/93619. The frozen-H comparison at z=1 has
E²=641/200 and 1.79<E<1.8, whose largest product remains below2.2. These are
four stationary comparisons with fixed physical couplings/left data/domain,
not one time-dependent cosmological solution or one common vacuum density.

## Uniform constitutive and IVP enclosure

For |chi|<=.01, exp(chi)>=.99 and exp(chi)<100/99. Hence .99<=a<9/4.
With b in[.9,1.1], f² lies between1701/1000 and737/200, giving1.3<f<2.

A²=1-[a/(2b+a)]². The ratio increases with a and decreases with b, so its
maximum is at most5/9 and A²>=56/81>(4/5)². Since A>0, A>4/5 follows.
The function q=ab/(2b+a) increases separately with a and b, giving
q<=99/178<3/5. These are actual-point bounds.

For the separate integral-variable argument, on v in[13/20,13/10],
the ratio a/sqrt(a²+4v²) increases with a and decreases with v. The stated
squared lower denominator bound exceeds(5/2)², so the ratio is strictly
below9/10. The integrand consequently exceeds99/2000 and T exceeds
1287/40000>.03. This interval is inside[0,f]; no inappropriate lower bound
on the integrand at v=0 is used. T<af/2<9/4 also holds.

The sinh estimate follows, for example, from the positive series bound
sinh(t)<t/(1-t) at t=.02, giving |sinh(2chi)/2|<1/98<.011.
Thus -2.27<w'<-.019 throughout the box. Before first exit, r remains
in[.978,1], b in[1,1.011], w in[-.0226,.0001], and |chi|<=.0003.
Every bound is strictly inside the chosen box. Smoothness on its positive
a,b neighborhood justifies continuation through D=.01 uniformly in alpha.

w begins positive and decreases strictly. Integrating its strict derivative
bounds proves exactly one zero, with1/22700<d_*<1/190<D and
D-d_*>9/1900. The physical multiplier L_c is common; this does not equate
the four individual turn positions.

## Full quadratic form and spectral bound

Acceptance here is conditional on the explicitly supplied Q2 and N. Starting
from those forms, zero Psi trace removes the boundary term when integrating
-2(r Xi)'Psi, leaving+2r Xi Psi'. The pointwise inequality
(Xi'-f Xi)²>=Xi'²/2-f²Xi² follows by completing a square.

Allocate A/4 of Psi'² to each mixed term. Their penalties are4r²Xi²/A and
4q²eta²/A. Since m=cosh(2chi)-2T+f q>-7/2, the total Xi penalty is bounded
by209/20<11 and the eta penalty by53/10<6. Remaining derivative coefficients
are r/2>.45, A/2>.4 and1. Therefore

    Q2 >= (2/5)||u'||²-11||u||²

with all three components retained. For the common Dirichlet interval D=.01,
Poincare with pi²>9 gives

    Q2 >= (35989/90000)||u'||² >=35989||u||²,
    N <=(11/10)||u||²,
    Q2/N >=359890/11.

The norm is positive because r>=.9. The quadratic form is symmetric with
bounded smooth coefficients and positive leading terms under the stated
fixed-wall conditions. The Rayleigh lower bound is therefore a continuum
linear stability/gap statement for this conditional system, not merely a
sampled matrix spectrum. Vanishing boundary traces also make their time
derivatives vanish for admissible evolution, so the linear boundary flux
vanishes. No free-wall or nonlinear stability inference follows.

Restoration uses the one fixed inverse-time scale a_c/c_s. The common bound
is (359890/11)(a_c/c_s)², approximately2.867510982793e-28 s^-2. Using each
a_ref in its place would change the clock and invalidate this comparison.

## Computation inspection and limitations

The observed root record reports29 passing rational checks, exit0, and
0.024476 seconds under the120-second wall/110-second CPU bound. I inspected
the code and each claimed inequality against the analytic argument. This is
source/output inspection, not a new execution or an independent orbit/spectrum.
The script's final boundary-arithmetic assertion is only a toy arithmetic
control; the functional boundary conclusion comes from the zero-trace argument
above. Likewise the large-domain failed bound is not an instability proof.

This is a conservative short-domain certificate for the diagnostic Q
scalar/scale/fluid construction, with separately induced right-wall values
and background masses. It supplies no action derivation for filtered MONO,
RAR or registered M, no literal constant-vacuum interpretation of varying a,
no evolving cosmology, free-wall/nonlinear/3D result, physical metric/photon
coupling, two-gravitational-DOF proof, empirical coefficient selection or
theory closure. Those exclusions are material to acceptance.
