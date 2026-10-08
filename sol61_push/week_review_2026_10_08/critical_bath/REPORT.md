# A differential operator that generates the threshold spectrum

Checkpoint CB1, October 8, 2026. Base a51caafcab1b0f62c9a744fef62cab4d1703714a. This continues the threshold-continuum work without modifying Astra's campaign.

**Result:** an explicitly specified nonnegative inverse-square bath and a normalized localized source produce the required E^{-1/3} transition density. This replaces the assumed density with a solvable differential operator. Its potential coefficient and boundary condition are chosen, not derived from BFSS or gravity. It is a constructive deep-MOND toy mechanism, not the exact filtered-MONO theory or a selection of 32pi^2.

## 1. Operator, domain and source

Work in dimensionless units, with 0<nu<1/2 and bath Hilbert space L^2((0,infinity),dr). Define
\[
K_\nu=-\frac{d^2}{dr^2}+\frac{\nu^2-1/4}{r^2}.
\]
Choose the homogeneous self-adjoint realization whose origin boundary expansion has the r^{1/2-nu} term and no r^{1/2+nu} term. Specifying the differential expression alone does not specify this operator.

Its unitary spectral transform has kernel
\[
\phi_k(r)=\sqrt{kr}\,J_{-\nu}(kr),\qquad
\mathcal F_{-\nu}K_\nu\mathcal F_{-\nu}^{-1}=k^2.
\]
Thus K_nu is nonnegative with spectrum [0,infinity), despite its attractive potential. This is the established homogeneous Bessel operator H_m with m=-nu. Domain definitions, the real-parameter self-adjoint specialization, and diagonalization are given in Section 2.3, Theorem 4.1 and Propositions 4.5–4.6 of [Derezinski and Richard, published version (2017)](https://www.math.nagoya-u.ac.jp/~richard/papers/inverse-square.pdf). Their dimension-one Bessel notation includes a square-root prefactor; the kernel above uses ordinary J. We use only this real homogeneous specialization.

Choose the normalized source vector
\[
v_\nu(r)=N_\nu r^{1/2-\nu}e^{-r^2/2},\qquad
N_\nu=\sqrt{\frac2{\Gamma(1-\nu)}}.
\]
It is square-integrable, tends to zero at the origin in the chosen range, and is exponentially localized at infinity. Gaussian localization introduces a length scale; setting it to one is a choice of units, not a physical prediction.

Using the Bessel power series and Gaussian moments gives
\[
\int_0^\infty r^{1-\nu}e^{-r^2/2}J_{-\nu}(kr)\,dr
=k^{-\nu}e^{-k^2/2}.
\]
For completeness, each series term integrates to
(-1)^j k^{2j-nu}/(2^j j!), whose sum is the expression above. Absolute integration of the series is finite for each fixed k, justifying interchange.

Therefore
\[
(\mathcal F_{-\nu}v_\nu)(k)
=N_\nu k^{1/2-\nu}e^{-k^2/2}.
\]
Changing variables E=k^2 supplies the essential Jacobian 1/(2sqrt(E)):
\[
\boxed{\frac{d\mu_\nu}{dE}
=\frac{E^{-\nu}e^{-E}}{\Gamma(1-\nu)}.}
\]
The integral is exactly one. For nu=1/3 the potential coefficient is -5/36 and the threshold exponent is exactly -1/3. The spectrum is generated from a local bath differential expression and its domain. The discrete-state coupling below is a smeared rank-one coupling, not an asserted local spacetime field theory.

## 2. Exact response and a directly testable correlation function

Add a zero-energy discrete state and the bounded linear source:
\[
H(D)=\begin{pmatrix}0&-D\langle v_\nu|\\
-D|v_\nu\rangle&K_\nu\end{pmatrix}.
\]
The perturbation has norm |D|. The Hamiltonian is self-adjoint on the unperturbed domain and bounded below by -|D|. Three identical bath copies can be coupled to a three-vector source; only its longitudinal combination mixes, giving D=|boldsymbol D|.

For D>0, the unique negative eigenvalue -epsilon obeys
\[
\epsilon=D^2 I_\nu(\epsilon),\qquad
I_\nu(\epsilon)=\int_0^\infty\frac{d\mu_\nu(E)}{E+\epsilon}
=\epsilon^{-\nu}e^\epsilon\Gamma(\nu,\epsilon).
\]
The last equality follows independently from 1/(E+epsilon)=integral exp[-t(E+epsilon)]dt and the Gamma integral. Here Gamma(nu,epsilon) is the upper incomplete Gamma function.

The positive root is unique since I decreases from infinity to zero. Its continuum eigenvector is D(K+epsilon)^{-1}v times the discrete amplitude and is normalizable for epsilon>0.

As D tends to zero,
\[
\boxed{\epsilon\sim\Gamma(\nu)^{1/(1+\nu)}
D^{2/(1+\nu)}.}
\]
For nu=1/3, write A=Gamma(1/3)^{3/4}. The positive constitutive candidate Hcal(D)=D^2/2+eta epsilon(D), eta>0, then gives
\[
g\sim\frac32\eta A\sqrt D,\qquad
a_{\rm toy}=\frac94\eta^2\Gamma(1/3)^{3/2}.
\]
Convexity of minus the ground energy and secant-slope bounds justify the derivative asymptote. The sign and flux-to-gravity map are the same explicitly assumed static map as in the preceding chain.

There is also an exact Euclidean correlation, requiring no continuum eigenstate fitting:
\[
\boxed{C_\nu(t)=\langle v_\nu,e^{-tK_\nu}v_\nu\rangle
=(1+t)^{-(1-\nu)}.}
\]
At nu=1/3 the long-time power is t^{-2/3}. Its integrated susceptibility grows as
\[
\int_0^T C_{1/3}(t)\,dt
=3[(1+T)^{1/3}-1].
\]
This gives a specific diagnostic for an underlying physical theory: compute its connected source correlator and test both the long-time exponent and its normalization. A finite apparent scaling window is not an asymptotic proof.

Nonzero continuum couplings can be retained by the previous source repair FBF with F=[K/(K+E_c)]^{1/2}. It leaves v and this unperturbed correlation unchanged, and obeys the alpha=1 bound from ../threshold_continuum/REPORT.md. The exact root above applies to B=0; the leading coefficient survives the repaired B, but the finite-D root generally changes.

## 3. Boundary selection is a genuine, relevant missing equation

The same differential expression has a second homogeneous nonnegative realization with J_{+nu} eigenfunctions and the r^{1/2+nu} boundary. Keep the SAME source v_nu. Its small-k transform is
\[
\mathcal F_{+\nu}v_\nu(k)
\sim \frac{N_\nu 2^{-\nu}}{\Gamma(1+\nu)}
k^{1/2+\nu},
\]
because the remaining Gaussian moment is integral r exp(-r^2/2)dr=1. Its density is consequently
\[
\frac{d\mu_+}{dE}\sim
\frac{2^{-2\nu}}{\Gamma(1-\nu)\Gamma(1+\nu)^2}E^\nu.
\]
Its static susceptibility chi=integral E^{-1}dmu_+ is finite: the displayed threshold is integrable and above E=1 finiteness follows from the unit norm. The coupled eigenvalue now satisfies epsilon~chi D^2. Merely changing the operator domain removes the deep-MOND power.

For this same normalized source its value can be found exactly. The zero-energy regular Green kernel is
G_0(r,s)=(2nu)^{-1}r_<^{1/2+nu}r_>^{1/2-nu}. Splitting the double integral into r>s and s>r gives
\[
\chi=\frac{N_\nu^2}{\nu}\int_0^\infty
r^{1-2\nu}e^{-r^2/2}(1-e^{-r^2/2})\,dr
=\boxed{\frac{2^{1-\nu}-1}{\nu}}.
\]
The corresponding exact transform for this domain is
N_nu 2^{-nu} k^{1/2+nu} 1F1(1;1+nu;-k^2/2)/Gamma(1+nu), also obtained by Gaussian moments. It provides a direct spectral check of the Green-kernel result.

More generally, write the origin expansion as
u(r)~a r^{1/2-nu}+b r^{1/2+nu}, b/a=zeta. The continuum solution is proportional to
\[
\sqrt{kr}\,[J_{-\nu}(kr)+t(k)J_{+\nu}(kr)],\qquad
t(k)=\zeta(2/k)^{2\nu}
\frac{\Gamma(1+\nu)}{\Gamma(1-\nu)}.
\]
Its delta-k normalization divides by
sqrt[1+2t cos(pi nu)+t^2]. For fixed nonzero zeta the normalization changes the low-k power. For zeta>0 and this positive source the leading overlap cannot cancel; the density is proportional to E^nu, not E^{-nu}. The transition scale is
\[
E_b=4\left[\zeta\frac{\Gamma(1+\nu)}
{\Gamma(1-\nu)}\right]^{1/\nu}.
\]
At nu=1/3, an intermediate deep-MOND-like regime can occur only above the associated energy crossover and below the Gaussian cutoff; it is not the D->0 limit for zeta>0. Matching epsilon approximately to E_b estimates D_b approximately (E_b/A)^{2/3}, not an exact transition formula.

For zeta<0, a decaying solution sqrt(r)K_nu(kappa r) has
zeta=[Gamma(-nu)/Gamma(nu)](kappa/2)^{2nu}; hence there is a negative bath eigenvalue. That bath no longer has the stipulated nonnegative threshold.

The desired homogeneous boundary is therefore a special choice. Its exact stability must be supplied by a symmetry or boundary dynamics, not assumed from a numerical fit. Varying nu also changes the response exponent continuously; nothing in this construction selects nu=1/3.

### A positive quadratic form can impose that boundary

There is a constructive action-level way to specify the desired domain. Set s=1/2-nu and
\[
\mathcal A_s=\partial_r-s/r,\qquad
q_s[u]=\int_0^\infty|\mathcal A_su|^2dr,
\]
on the maximal first-order domain: u in L^2, locally absolutely continuous away from zero, and A_s u in L^2. This is a closed nonnegative form, associated to the self-adjoint operator A_s^* A_s. Its interior expression is -partial_r^2+s(s-1)/r^2, exactly K_nu.

For operator-domain solutions u~a r^s+b r^{1-s}, integration by parts in the form variation gives the lower-end term -2nu delta(a)* b (and its real conjugate). Allowing the trace a to vary freely therefore imposes b=0. The coefficient -5/36 and the desired boundary follow together from s=1/6 and this specific maximal-domain square form. This supplies a precise bath energy functional; it still does not derive s from gravity.

For this normalized Gaussian source, A_s v=-r v. Consequently
q_s[v]=1-nu, agreeing with the first spectral moment integral E dmu(E). The unrenormalized separate kinetic and potential integrals are not the definition of q_s: for functions with nonzero a they can diverge at the origin. With a lower cutoff epsilon the identity includes the boundary term s|u(epsilon)|^2/epsilon.

A positive allowed boundary energy lambda|a|^2 changes the natural condition to 2nu b=lambda a. Thus zeta=lambda/(2nu)>0 yields precisely the infrared crossover above. This shows both how the desired boundary can be implemented and which perturbation must be forbidden or controlled. Positivity alone does not forbid it.

## 4. The BFSS comparison identifies a concrete missing interaction

Lin and Yin's [2015 preprint, Section 3.1, equations (3.1)–(3.4)](https://arxiv.org/html/1402.0055v2#S3.SS1) reduces the leading Cartan supercharge, after a stated wavefunction rescaling, to free superparticles. Their SU(N) asymptotic wavefunction is a proposal with factorization checks, not a determination of this source spectrum. One must retain their measure and wavefunction conversion; a radial power read in another measure is not a physical spectral density.

Independently, for an ordinary free relative coordinate in d=9 with angular momentum l, reducing -Delta to L^2(dr) gives
\[
K_{\rm free,radial}=-\partial_r^2+
\frac{(l+7/2)^2-1/4}{r^2}.
\]
Its Bessel index is l+7/2, not 1/3. To turn this simple channel into the critical bath, an additional inverse-square attraction would have to be
\[
\boxed{\Delta V(r)=
\frac{1/9-(l+7/2)^2}{r^2}.}
\]
For l=0 this is -437/(36 r^2); for l=1 it is -725/(36 r^2), in the kinetic normalization used here. These are algebraic requirements for this simplified channel, not interactions derived in BFSS. Coupled channels, resonances and the full scattering measure are not excluded by this comparison.

This sharpens the task from “a threshold state might help” to finding a particular critical effective channel and its protected domain, or obtaining the same source spectral exponent by another mechanism.

## 5. Two exact limits on what this route can finish

**Full MONO:** for any bounded source O, the spectral infimum of H0-D O is Lipschitz in D with constant ||O||, by the variational principle. Hence its negative has bounded one-sided slopes. The operative MONO excess acceleration h(y) eventually grows as a positive constant times log(y). A single bounded-source bath with fixed conversion eta cannot reproduce that entire high-y tail. This model supplies a deep limit; an exact full-kernel construction needs another justified ingredient. Over a finite observational interval this is not an exclusion.

**Vacuum normalization:** adding V times the identity to a microscopic Hamiltonian changes its absolute energy but leaves its excitation spectrum and the subtracted response Eground(D)-Eground(0) unchanged. Therefore this response construction alone cannot select an absolute gravitational vacuum energy. A gravitating vacuum term and its physical normalization must enter the same action. Setting eta or a Gaussian scale to make k=1/2 would fit the target, not derive it.

## 6. Research checkpoint

Three different tests were pursued: the BFSS free-channel comparison, a constructive inverse-square realization, and the boundary/full-kernel counterchecks. The constructive route now has an explicit operator, source, spectrum, response, correlator and continuum-coupling control.

Still open: selection of the inverse-square coefficient and domain; physical source and energy units; the common gravitational action; exact filtered MONO and metric/DOF requirements; and k=1/2. This is a new concrete route within the reviewed project record, not a claim that inverse-square quantum mechanics or Friedrichs models are globally new.

Next decisive calculation: derive the effective radial operator and origin/domain matching from the proposed microscopic action, including the interaction that could change its Bessel index. On the BFSS route this requires an actual source scattering calculation; the leading free-channel result alone does not supply it. The boundary-crossover formula and correlator provide tests for that calculation.

Numerical evidence and retained negative controls are in VALIDATION.md. Neither the source papers nor this note received an independent full proof audit in this session.
