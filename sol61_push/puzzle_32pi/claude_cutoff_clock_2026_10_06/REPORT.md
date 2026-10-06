# Claude's high-force turnoff creates a critical clock-response surface

Observed input HEAD:3e3b4f295a3449defd83d75667c3b9ddb11f1e76. This investigation directly builds on sonnet55 p35 (kernel tail repair), p54 (vacuum integral/remaining turnoff scale), and p56 (phenomenological solar/ETNO response). Their scripts and saved outputs were read; no SPARC or astronomical fetch/run was repeated. Their kernel can be transplanted as a normalized-clock response without breaking the logarithmic classical vacuum map, but the turnoff changes the stationary principal coefficient and the required flow substantially. It does not inherit those scripts' observational conclusions automatically.

## 1. Exact source-to-response dictionary

Let s>0 denote the Newtonian source field in the leading spherical mass balance, A>0 the kernel acceleration scale, y=s/A, T>0, and k=2 for the current p35 kernel:
ν(y)=1+[√(1+1/y)−1]/[1+(y/T)^k],
g(s)=sν(s/A)=A f(y), f(y)=y+h(y),
h(y)=b(y)/[1+(y/T)^k], b(y)=1/[√(1+1/y)+1].
The last expression is cancellation-free. The acceleration excess is δg=A h(y), positive, vanishing at both y→0 and y→∞ for k>0. Define the response on its monotone inverse by
W_g(g)=s(g), W(0)=0, W_gg=ds/dg=1/f'(y)=1/[1+h'(y)].
The covariant added term remains Lresp=K_E U(g_a), U=g_a²−2W(g_a), where g_a is the clock's proper acceleration. Consequently
U_gg=2[1−W_gg]=2h'/(1+h'),
U_g/g=2h/(y+h)>0.
Including K_E, the longitudinal lapse-gradient Hessian coefficient is K_E U_gg; conventionally its quadratic-action coefficient carries another1/2. These are derivatives with respect to clock acceleration, not a claim that g_a equals the measured metric force on a full sourced solution.

The use of W_g=s is the leading stationary exterior mass-flux dictionary from flowing_clock/source_asymptotics. It is not the BIMOND vacuum dictionary in p54. In particular the latter's ∫δg ds and exchange parameter cannot be transferred into logarithmic KGB as a cosmological selector. Its exact vacuum adjustment and H* come from a different varied action. The positive Einstein–Hilbert signs checked in p54 are also not a proof of full constrained finite-gradient health for this completion.

## 2. Universal sign-crossing theorem and kernel-specific uniqueness

Assume δg is C¹ on s>0, tends to0 at both endpoints, is positive somewhere, and g'(s)=1+δg'(s)>0 so the inverse is regular. By the mean-value theorem δg' is positive somewhere before a positive value, and negative somewhere on its return to0. Continuity therefore forces a zero separating the positive and negative regions. At that zero g'=1, W_gg=1 and U_gg=0; on the returning side U_gg<0. If g' ceases to be positive instead, the prescribed source-to-response inversion has already failed. Thus a positive extra force that turns off to zero cannot keep this clock response longitudinally convex everywhere. This is a universal statement under these hypotheses, not a conclusion from a finite grid. The uncut P2 excess tends to A/2 and is an explicit exception to the endpoint hypothesis.

For p35,
y b'/b=1/{2[y+1+√(y(y+1))]} is strictly decreasing,
y D'/D=k(y/T)^k/[1+(y/T)^k] is strictly increasing.
Hence h' has exactly one zero. For k=2 its location y_c obeys
T²=y_c²[4y_c+3+4√(y_c(y_c+1))],
y_c≈T^(2/3)/2 for large T.
It occurs appreciably below the nominal turnoff T. Global invertibility is retained in the tested kernels: b≤1/2,b'>0 imply
h'≥−[k/(2T)] max_x x^(k−1)/(1+x^k)².
For k=2 the maximum is9/(16√3), so f'≥1−9/(16√3T)>0 for T>9/(16√3). No target integral is fitted in this work. The existing T=128.9153707043 is an inherited input alongside T=100,128,1000; it is not a newly derived value.

The exact k=2 critical points are:

| inherited T | y_c | g_c/A | U_gg at2y_c |
|---|---:|---:|---:|
|100|10.56963|11.05293|−0.00332338|
|128|12.49581|12.98156|−0.00243529|
|128.9153707043|12.55626|13.04207|−0.00241344|
|1000|49.79294|50.28923|−0.000170093|

Thus the current cutoff becomes longitudinally nonconvex above a clock acceleration near13A, long before its nominal y≈129 suppression scale. This statement concerns the prescribed clock operator, not an observed acceleration threshold in a completed metric theory.

## 3. What is singular, and what is not proved about health

On the stationary unitary ansatz ds²=−N²dt²+B²(dr+Vdt)²+r²dΩ², φ=qt, N'>0, the exact three Euler equations have a derivative matrix for (B',V',a'), with N'=aNB. Its determinant, in the action normalization used by source_asymptotics, is
4 K_E³ r⁴ V² U_gg/N².
Thus for finite nonzero V,N,r, U_gg=0 is a genuine rank loss of this reduced stationary differential system. The kernel inverse is nevertheless perfectly regular there (f'=1), so changing from a to s is a nonsingular variable change and cannot remove this rank loss. This is stronger than an incidental bad coordinate choice in the inverse kernel.

It is not a proof of a propagating ghost, a singular full covariant characteristic determinant, or nonexistence. In a local proper unitary frame the response's lapse-gradient Hessian has longitudinal eigenvalue K_E U_gg and transverse eigenvalue K_E U_g/g; the first vanishes and changes sign while the latter stays positive. This establishes an anisotropic change in the actual response operator. Einstein/KGB constraints, background shear/acceleration and other principal blocks can change the full physical symbol; that full finite-gradient constrained symbol has not been derived here. One cannot inherit homogeneous de Sitter health at finite acceleration, or infer a full ghost merely from U_gg<0.

A smooth stationary crossing must satisfy a compatibility condition. With the exact current definitions and fixed A,
j^r_KGB=(2c/(3H*q))[N'/B²−3H*V−(V/N)(V'+(B'/B+2/r)V)],
j^r_resp=K_E V(r²U_g)'/(qBr²).
The full stationary Euler identity gives zero total vacuum current when all three metric equations hold. At U_gg=0, a' drops out and the necessary compatibility becomes
j^r_KGB+2K_E V U_g/(qBr)=0.
This is an algebraic critical-surface condition, not an automatically unsatisfiable equation. Differentiating it with the remaining equations would be needed to determine permissible finite crossing slopes and branch uniqueness. Cosmological/source boundary data might impose further restrictions, but no universal selector has been established.

## 4. The formal flowing branch crosses the leading condition, then becomes demanding

On the leading vacuum mass balance W_g(a)=s=m/r², the candidate clock acceleration is a=g(s). The retained momentum constraint fixes
V≈−ηH*r a/[r a'+2a]
=−ηH*r g(s)/{2[g(s)−s g'(s)]}
=−ηH*r [y+h]/[2(h−y h')], η=c/(3K_EH*²)∈(0,1).
For this kernel h−yh'>0 because b−yb'>0 and the suppression denominator is increasing. At the critical point h'=0 the denominator is2h>0: the leading profile has a finite flow and automatically satisfies the leading zero-current compatibility. Therefore the sign crossing alone does **not** refute the formal branch. Exact subleading compatibility remains to be solved.

At high field,
δg≈A T^k/(2y^k),
V≈−ηH*r y^(k+1)/[(k+1)T^k].
For k=2 this is V≈−ηH*m³/(3A³T²r⁵), versus the uncut P2 high-force r^-1 flow. Its mass exponent is3 and radius exponent−5. The very small extra force entails a large required flow because r a'+2a is nearly zero in an inverse-square field. Weak flow cannot be presumed merely because the phenomenological force anomaly is tiny. Before the formal flow becomes large, omitted V² terms can invalidate the source-to-clock balance, requiring the exact equations rather than extending this asymptotic expression.

The benchmark uses only p56's stated numerical inputs GM_sun=1.32712440018e20 m³/s², AU=1.495978707e11m, A_SI=9.3603e−11m/s², and c_light=299792458m/s, with independently chosen η=.5 and A/H*∈{.3,1,3}. These are conditional model inputs, not new measurements or a target-coefficient fit. At1AU, y≈6.34e7. The formal k=2 flow for inherited T≈128.915 is far outside |V|≪1 for these ratios, even though the p35 phenomenological excess is tiny. This diagnoses breakdown of the formal weak-flow completion at that benchmark; it is not an observational exclusion of the full action, whose actual strong-flow solution has not been constructed. No published solar limit or p56 count is used as an independently verified constraint in this report.

p56 explicitly treats an imposed radial force, ignores external-field corrections in parts of the far orbit, and estimates arc visibility before orbit fitting. Its90-object visibility/precession summaries are therefore neither direct tests of the new covariant completion nor a reason to skip its clock/metric matching. New observational claims would require primary-source ephemeris/astrometric verification and actual force predictions; no astronomical refetch or rerun was made.

## 5. Preserved vacuum map, evidence and smallest missing step

Because W depends only on the invariant normalized-clock acceleration and fixed A,T, positive φ-rescaling leaves this entire response unchanged. W∼g³/(3A) at deep acceleration, so its first variation vanishes on the geodesic rolling background and the original logarithmic vacuum map/cosmological quadratic branch survives. Neither the cutoff parameter nor this invariance guarantees finite-gradient health.

checks.py verifies the exact unique-zero equation, analytic invertibility bound, inversion derivative, stationary derivative determinant, finite critical leading flow/current compatibility, high-force exponents and bounded cancellation-free evaluations. Negative controls transplant f' instead of its reciprocal, assert longitudinal positivity beyond turnoff, or discard the required flow. Fresh standard manifests pin actual Claude inputs and our prior source-asymptotic equations. The bounded calculations illustrate the proved sign theorem; they do not establish the full finite-gradient symbol or a global source solution.

Smallest missing implication: derive the constrained finite-acceleration covariant characteristic symbol and solve the critical-surface compatibility/matched source problem for the cutoff response. This determines whether the rank loss is a passable stationary critical surface, a physical instability, or an obstruction for the required boundary data. Only after that can p35/p56 phenomenology be attached to this same action. There is no32π derivation here.
