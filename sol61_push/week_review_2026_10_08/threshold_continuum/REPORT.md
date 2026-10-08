# The continuum coupling gate and a constructive repair

October 8, 2026. Follow-up to commit 425d71471 and the threshold chain in ../astra_derivation_chains/DERIVATIONS.md. All variables below are dimensionless. This is a conditional spectral mechanism, not a BFSS response calculation or a derivation of the physical Zimmerman coefficient.

**New result:** a nonzero continuum-to-continuum coupling need not destroy the three-halves response. A form bound with exponent greater than 1/3 preserves its leading coefficient. At the boundary the coefficient can change; below it the response can be overwhelmed. A spectral modification of the source enforces the safe bound while leaving its unperturbed transition spectrum unchanged.

## 1. A robustness theorem with nonzero continuum coupling

Fix one source direction. Let P be a rank-one zero state, Q=1-P, K=QH0Q nonnegative, v=QO|0>, and POP=0. Assume O is bounded and self-adjoint. In this direction write
\[
H(D)=
\begin{pmatrix}0&-D\langle v|\\-D|v\rangle&K-DB\end{pmatrix},
\quad B=QOQ,\quad D>0.
\]
Suppose the finite spectral measure of v has density
\[
d\mu(E)=[C E^{-1/3}(1+o(1))]\,dE,\quad E\downarrow0,\quad C>0,
\]
in a neighborhood of zero. Its remaining finite mass may be arbitrary away from zero. Assume, on the form domain of K, for a fixed b,
\[
|\langle\psi,B\psi\rangle|\le b\langle\psi,K^\alpha\psi\rangle,
\qquad 1/3<\alpha\le1.
\]
Then the bottom of the spectrum satisfies
\[
\boxed{\inf\sigma H(D)=-A D^{3/2}(1+o(1)),\qquad
A=(2\pi C/\sqrt3)^{3/4}.}
\]
No commutation of B with K is required. This statement concerns the spectral infimum; it does not assert a normalizable isolated ground state for every perturbed model.

Proof: replace K by cK while keeping v fixed and B=0. The scalar equation is
\[
\epsilon=D^2\int\frac{d\mu(E)}{cE+\epsilon}.
\]
Its threshold integral is asymptotic to
\(C c^{-2/3}(2\pi/\sqrt3)\epsilon^{-1/3}\); finite spectral mass separated from zero contributes a bounded term. Thus
\(\inf\sigma H_c(D)=-A c^{-1/2}D^{3/2}(1+o(1))\).
This estimate is uniform for c approaching 1, by bounding the resolvents between any two fixed nearby c values.

For 0<alpha<1, maximization of bD x^alpha-delta x on x>=0 gives the operator form inequality
\[
bD K^\alpha\le\delta K+r_\delta I,\qquad
r_\delta=(1-\alpha)\alpha^{\alpha/(1-\alpha)}
(bD)^{1/(1-\alpha)}\delta^{-\alpha/(1-\alpha)}.
\]
Consequently
\[
\inf\sigma H_{1-\delta}(D)-r_\delta
\le\inf\sigma H(D)\le
\inf\sigma H_{1+\delta}(D)+r_\delta .
\]
Choose delta=D^s with
\[
0<s<\frac{3\alpha-1}{2\alpha}.
\]
Then delta tends to zero and r_delta=o(D^{3/2}); squeezing proves the result. For alpha=1, take delta=bD and r_delta=0. This also shows why the strict boundary is alpha>1/3.

If the spectral infimum is converted to a constitutive energy, epsilon(D)=-inf sigma H(D) is convex because H is affine in D. Its subgradients obey epsilon'(D)~(3A/2)sqrt(D), interpreted one-sided where necessary: bound every subgradient between the two secant slopes at (1-h)D,D,(1+h)D, take D to zero, then h to zero. Thus the response exponent follows without assuming differentiability of a ground state.

## 2. A linear, even source model shows the boundary is sharp

Use two identical continua on 0<E<L with v(E)=sqrt(C E^{-1/3}). Couple the discrete state to each with -D v/sqrt(2), and put diagonal continuum energies E-bD E^alpha and E+bD E^alpha. This Hamiltonian is affine in signed D. Swapping the continua and reversing the sign of the discrete state implements D -> -D; the spectral bottom is even. Its total unperturbed transition measure remains exactly C E^{-1/3}dE.

Below both continua, the eigenvalue -epsilon obeys
\[
\epsilon=\frac{CD^2}{2}\int_0^L E^{-1/3}
\left[\frac1{E-bD E^\alpha+\epsilon}
+\frac1{E+bD E^\alpha+\epsilon}\right]dE.
\]
For alpha=1/3, set E=D^{3/2}x and epsilon=e D^{3/2}. The limiting coefficient is the unique root
\[
e=\frac C2\int_0^\infty x^{-1/3}
\left[\frac1{x-bx^{1/3}+e}
+\frac1{x+bx^{1/3}+e}\right]dx,\qquad
e>2(b/3)^{3/2}.
\]
The right side decreases from infinity at the lower threshold to zero at infinity. The paired reciprocal is strictly larger than 2/(x+e), so e>A for b>0. The same unperturbed spectral density therefore does NOT fix the response coefficient at the critical coupling.

For 0<alpha<1/3 and small enough D, the negative continuum alone reaches
\[
-m(D),\quad m(D)=(1-\alpha)\alpha^{\alpha/(1-\alpha)}
(bD)^{1/(1-\alpha)}.
\]
This minimum is attained at E_*=(alpha bD)^{1/(1-alpha)} inside (0,L). Trial states supported only in that continuum establish inf sigma H(D)<=-m(D), irrespective of the off-diagonal coupling. Since 1/(1-alpha)<3/2, m(D)/D^{3/2} diverges. The old three-halves leading asymptote is impossible in this example. Alpha=0 gives the even simpler continuum edge -bD.

These examples make 1/3 sharp for this sufficient form-bound criterion. They do not classify every operator lacking the bound; cancellations or additional structures need separate analysis.

## 3. Constructive source repair, preserving the desired spectrum

Given bounded O_i with PO_iP=0, define, for a new positive energy scale E_c,
\[
F=\left(\frac K{K+E_c}\right)^{1/2},\qquad
\boxed{\widetilde O_i=PO_iQ+QO_iP+FQO_iQF.}
\]
Here F acts only on Q. The off-diagonal pair and the filtered block are each bounded and self-adjoint. If H0 and P are gauge and rotation invariant, the new source has the same gauge and vector transformation laws as O_i. The perturbation remains linear in the source vector.

Two exact properties are useful:
\[
Q\widetilde O_i|0\rangle=QO_i|0\rangle,
\]
so its operator-weighted transition spectrum is unchanged, and
\[
|\langle\psi,FQO_iQF\psi\rangle|
\le\|O_i\|\langle\psi,K(K+E_c)^{-1}\psi\rangle
\le\frac{\|O_i\|}{E_c}\langle\psi,K\psi\rangle.
\]
The robustness theorem applies with alpha=1. This is a concrete completion of the earlier solvable model with nonzero continuum coupling, conditional on obtaining the required transition density from the underlying dynamics. It does not merely set QOQ to zero.

For the finite-cutoff density C E^{-1/3} on (0,L), let b=||O_i||/E_c. The same comparison gives a usable finite-source error bound, for bD<1:
\[
A(1+bD)^{-1/2}D^{3/2}
-\frac{3C}{1+bD}L^{-1/3}D^2
\le-\inf\sigma H(D)
\le A(1-bD)^{-1/2}D^{3/2}.
\]
The lower bound uses the cutoff remainder in the earlier report, with K replaced by (1+bD)K. Thus the new continuum uncertainty is explicitly bounded, rather than hidden inside an asymptotic symbol.

The cost is explicit: this changes the physical source operator, uses the ground-state projection and spectral functional calculus, and introduces E_c. It is generally nonlocal in matrix configuration space and has no derived gravitational interpretation here. It is a candidate construction, not something proved to arise from BFSS. It cannot manufacture an E^{-1/3} density if the original transition density has another exponent.

## 4. Why the previous local bounded BFSS source remains unsafe

The preceding report proposed
\[
O_i(X)=\frac{\operatorname{Tr}(X_i\sum_jX_j^2)}
{(\ell^2+\sum_j\operatorname{Tr}X_j^2)^{3/2}}.
\]
On the commuting SU(3) ray X_1=R diag(-1,-2,3), X_{i>1}=0,
\[
O_1(R)=\frac{18R^3}{(\ell^2+14R^2)^{3/2}}
\longrightarrow m=\frac{18}{14^{3/2}}>0.
\]
The centers are distinct. Boundedness removes an unbounded runaway, but does not remove the possibility of a moving continuum threshold.

Here is the exact conditional obstruction. If there exist normalized physical channel packets psi_n, weakly escaping to infinity, with
\[
\langle H_0\rangle_{\psi_n}\to0,\qquad
\langle O_1\rangle_{\psi_n}\to m>0,
\]
then the variational principle gives inf sigma(H0-D O1)<=-mD for every D>0. Together with H0-D O1>=-D, this bounds the response between mD and D and excludes a leading A D^{3/2} asymptote. No inference about QOQ from the diagonal ground expectation <O>=0 can evade that bound.

The matrix-ray limit is exact. The required gauge-invariant low-energy packet construction and its O-weighted localization have NOT been proved here. The standard continuous-spectrum result for supersymmetric matrix models motivates this test but, by itself, does not establish those two packet limits for this particular operator.

Literature scope: inspected the publisher's abstract of de Wit, Luescher and Nicolai, [The supermembrane is unstable (1989)](https://www.sciencedirect.com/science/article/pii/0550321389902149), which states the continuous-spectrum result; an attempted primary PDF fetch from the Max Planck archive returned 403. No theorem from the inaccessible proof is imported. The cached OpenAI BFSS manuscript and its normalization were inspected in the preceding chain; its claimed threshold state remains unaudited. No new experimental data claim is made in this follow-up.

## 5. Research decision and remaining gates

Continue with the spectrally modified source as an explicitly conditional construction. Before interpreting the old local bounded source's response, prove or refute the channel-packet obstruction. Do not spend effort extracting a three-halves coefficient from an unperturbed spectrum while ignoring the continuum shift.

The next decisive calculation is still the actual transition measure of a physically specified source. A fit to total density of states does not answer it. If the E^{-1/3} measure can be established, the theorem above now supplies a controlled route past nonzero continuum coupling, rather than leaving that issue entirely open.

Neither construction selects C or the conversion between matrix energy, gravitational flux and energy density. The previous coefficient remains a_toy=(9/4)eta^2(2pi C/sqrt(3))^{3/2}. Consequently k=1/2 and the 32pi^2 normalization are still unselected. Full filtered MONO, the two metric potentials and the gravitational degree-of-freedom count remain separate unsatisfied requirements.

Verification: see VALIDATION.md and the bounded experiment records. The analytic statements were self-reviewed, not independently refereed. The numerical cases test implementations and examples, not all operators in the theorem.
