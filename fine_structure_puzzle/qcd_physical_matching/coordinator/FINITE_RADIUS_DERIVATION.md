# A finite-radius observable for the actual target

Parent FSP-005; new FSP-006 coordinator derivation. This is an exact observable construction, not evaluated QCD data or a new theorem about QCD's infrared limit.

Use the round S4 prescription of `qcd_prediction/coordinator/METRIC_RESPONSE.md`: V=Omega H^-4, Omega=8 pi^2/3, W=-log Z, f=W/V, rho=(1-D/4)f, D=H partial_H. All radii use the same microscopic theory and regulator, with continuum limits at fixed physical radius. The flat proton mass is the calibration observable. A curved or finite-box proton mass is not retuned independently at every radius.

## Stress data: four radii, no local polynomial fit

Let E u(H)=u(2H). The unique cubic polynomial with unit highest coefficient annihilating H^0,H^2,H^4 is

P_E=(E-1)(E-4)(E-16)=E^3-21 E^2+84 E-64.

Since P_E H=28H,

R_H=[rho(8H)-21rho(4H)+84rho(2H)-64rho(H)]/(28 H m_p^3).

If rho(H)=rho_0+A_rho H+rho_2 H^2+rho_4 H^4+r(H), and each r(2^jH)=o(H), then R_H -> R=A_rho/m_p^3. This follows from a finite linear combination and requires no interchange with an infinite series or differentiation of a noisy remainder. Each permitted local term through curvature squared cancels at every H, including its alpha-dependent coefficient, provided the same parameters are used at every radius. A term H log H would fail this finite-limit test.

For any coefficient a_n multiplying H^n in rho, its residual is a_n H^(n-1) P_E(2^n)/(28m_p^3). In particular H^6 gives 6480 a_6 H^5/m_p^3. For H^4 log(H/mu), the residual is (720/7) log(2) a_4 H^3/m_p^3; it vanishes but is not exactly annihilated. For a specified common bound |r(2^j H)|<=epsilon H, the ratio error is <=170 epsilon/(28m_p^3). This epsilon convention bounds against the base H, not each larger radius separately.

Given a covariance matrix Sigma for the four stress measurements ordered H,2H,4H,8H, variance(R_H)=w^T Sigma w/(28 H m_p^3)^2 with w=(-64,84,-21,1). Therefore going to small H magnifies a fixed stress uncertainty. These identities do not provide the needed precision or an extrapolation error bound for actual QCD.

## Partition-function data: cancel the anomaly logarithm too

The functional W has local terms proportional to H^-4,H^-2,H^0; a scale-anomaly contribution may include log(H/mu). Define

Q_E=(E-1)^2(E-1/4)(E-1/16).

Both a constant and log H are killed by the double root at 1. With integer weights c=(1,-22,105,-148,64), 64Q_E W=sum_(j=0)^4 c_j W(2^j H), and 64Q_E(H^-3)=(-49/128)H^-3. Consequently

R_H^W= -96/(49 Omega) (H/m_p)^3 sum_(j=0)^4 c_j W(2^jH)

converges to A_rho/m_p^3 if f has the linear term plus local terms, an H^4 log H term, and a remainder o(H) on this finite set of radii. The 3/4 conversion from A_f to A_rho uses the actual stress definition; it additionally requires D r=o(H). Without this differentiability hypothesis R_H^W measures (3/4)A_f/m_p^3 rather than proving the physical stress coefficient exists. The four-radius stress construction has no such derivative premise. Higher or multiple running logarithms are not exactly killed, but ordinary H^4 log^k H terms give vanishing H^3 log^k H residuals.

This form can be built from partition-function differences because sum c_j=0. A common, radius-independent additive normalization of W cancels. An arbitrary radius-dependent multiplicative normalization of Z does not cancel unless its log is one of the annihilated terms; its physical metric matching must be specified. This is exactly why flat normalized topological probabilities cannot by themselves supply the observable. Thermodynamic integration would require a valid interpolation and all measure/contact terms; none has been simulated here.

## Charge dependence on the physical matching path

Let u=e^2 and lambda_a be all independently retuned non-electromagnetic parameters. Let M_b be a complete set of flat calibration observables (including the proton and the chosen quark-mass definitions). On a regular branch J_ba=partial_(lambda_a)M_b is invertible, and

v_a=d lambda_a/du=-(J^-1)_ab partial_u M_b.

At u=0 the same-theory tangent insertion is

I_tan=I_EM + sum_a v_a partial_(lambda_a) S,

including current, mass, strong, gravity, contact and regulator terms required by the chosen convention. Then dW_H/du=<I_tan,H>. Substitution into the five-radius functional gives the finite-H derivative of R_H^W when flat m_p and physical H are held fixed. At nonzero u replace the leading integrated-photon insertion by the full derivative of the matched action. d/dalpha=4pi d/du at zero charge. Renormalized Thomson matching at finite charge must also be included; this identity is not a full finite-alpha curve.

The limits H->0 and u->0 must still be checked separately. The earlier exact nonlocal example in `qcd_closure/qed_resummation/` demonstrates that a nonzero first insertion need not imply a nonzero fixed-charge linear term. This stencil removes local subtraction terms; it does not prove those limits commute.

## Evidence and missing physics

The accompanying exact-arithmetic run checks weights, nullspaces, logarithmic cancellations, local biases, normalizations and a non-tautological synthetic generating functional. No gauge-field ensemble or curved-space QCD partition function is supplied. The bounded repository path search found programme calculations and literature caches, not a declared usable ensemble/curved partition-function dataset. It is not an exhaustive proof that no data exists elsewhere. The missing measurements are explicitly the rho or W values and their matched current insertions, with common QCD inputs, continuum control, and radius-limit errors. Inventing those inputs would fit the desired answer.

## Exact-check correction

The first independent moment-system run rejected the initially hand-computed normalization 42: (2-1)(2-4)(2-16)=28. The current stress normalization and stress bias coefficients above use 28. The original derivation and failed executed input are preserved as RAW_DERIVATION_v1.md and check_finite_radius.py. The W functional is unaffected. The corrected check is check_finite_radius_v2.py; the discrepancy was an arithmetic/implementation error, not a QCD counterexample.
