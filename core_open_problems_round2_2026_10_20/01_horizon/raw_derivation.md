# Raw derivation: force observables and vacuum normalization

Checkpoint HORIZON-R2-2026-10-20. These calculations were derived before viewing
other Round2 agents' work; no such work was consulted. The base publication is
8aa3f7046a7ae14a99f3515fd42df5bf061fb1db. Documentary input copies and hashes are
under frozen_inputs/. Only this Round2 horizon directory is modified.

## 1. A Gaussian in-in force observable

Use hbar=c=kB=1, signature -+++, a real massless conformally coupled scalar in
the conformal de Sitter vacuum, and a prescribed stationary uniformly
accelerated worldline z(tau). Define alpha=sqrt(H^2+a^2), with a its proper
acceleration. The system is a real internal coordinate Q conjugate to the
applied generalized force J:

\[
S=S_\phi+\int d\tau\left[\frac M2(\dot Q^2-\Omega_b^2 Q^2)
+JQ+\lambda Q\phi(z(\tau))\right],\qquad
S_\phi=-\frac12\int\sqrt{-g}\,[(\nabla\phi)^2+R\phi^2/6].
\]

This specifies a physical mechanical response, delta<Q>/delta J. It does not
promote z to a dynamical center of mass. No gravitational force law has been
identified with this observable.

The frozen Round1 correlator gives, for positive omega,

\[
W^+(s)=-\frac{\alpha^2}{16\pi^2\sinh^2[\alpha(s-i0)/2]},\quad
\mathcal F(\omega)=\int ds\,e^{-i\omega s}W^+(s)
=\frac{\omega}{2\pi(e^{2\pi\omega/\alpha}-1)}.
\]

The decisive subtraction, including its normalization, is

\[
\rho_\phi(\omega)=\mathcal F(-\omega)-\mathcal F(\omega)
=\frac{\omega}{2\pi},\qquad
N_\phi(\omega)=\frac{\mathcal F(-\omega)+\mathcal F(\omega)}2
=\frac{\omega}{4\pi}\coth\frac{\pi\omega}{\alpha}.
\]

Our retarded convention is G_R(s)=i theta(s)<[phi(s),phi(0)]>, Fourier
transform exp(+i omega s), so Im G_R=rho_phi/2. Integrating out the free field
on the closed time path gives the exactly Gaussian influence action

\[
S_{\rm IF}=\lambda^2\int Q_- G_R Q_+
+\frac{i\lambda^2}{2}\int Q_-N_\phi Q_-,
\quad Q_-=Q_1-Q_2,\quad Q_+=(Q_1+Q_2)/2.
\]

The imaginary part describes fluctuations, not an additional mean source.
With a common regulator and common local frequency/mass subtraction for all
alpha, the renormalized Ohmic mean equation and susceptibility are

\[
M(\ddot {\bar Q}+2\gamma\dot{\bar Q}+\Omega_R^2\bar Q)=J,
\quad\gamma=\frac{\lambda^2}{8\pi M},\qquad
\chi_R(\omega)=\frac1{M(\Omega_R^2-\omega^2)-i\lambda^2\omega/(4\pi)}.
\]

The spectral subtraction fixes the nonlocal/absorptive part. The local real
subtraction fixes the displayed Omega_R; it is not a result of KMS. For
J(t)=Re[J0 exp(-i omega t)], the measurable cycle-averaged work rate is

\[
\overline{J\dot Q}=\frac\omega2\operatorname{Im}\chi_R(\omega)|J_0|^2.
\]

It is positive and independent of alpha in this model, whereas the stationary
Q noise is lambda^2 |chi_R|^2 N_phi. For a finite bandwidth one can instead
choose the same positive regulated spectral density at each alpha; its
dispersion integral and therefore its retarded response remain identical.
The local Ohmic expression is the pointlike low-frequency limit, not a claim
that a physical oscillator has unlimited bandwidth.

This is a direct in-in obstruction for this *specified linear observable*,
stronger than equating detector temperature with a putative force. It does not
show that all observables are acceleration independent: covariance, transition
statistics, emitted radiation and nonlinear response need not be. Nor does it
calculate the force obtained by varying z in the influence action. A general
worldline EFT also permits independent finite operators R Q^2 and a^2 Q^2;
adding them requires additional measured or microscopic coefficients. The
minimal conformal action above sets them absent except for its chosen
renormalization. They cannot be inferred from the KMS temperature alone.

## 2. A gapless candidate with an actual polarization source

The following is a concrete extension and normalization audit of the existing
NODAL_RING_ORIGIN construction, not a new origin of its cubic term. Let
P=|boldsymbol P|, K=4 pi G, and normalize the physical polarization by

\[
\mathcal L_{\rm stat}=-\frac{|\nabla\Phi|^2}{2K}-\rho_b\Phi
+\boldsymbol P\cdot\nabla\Phi-W_{\rm eff}(\boldsymbol P).
\]

Varying Phi gives div(grad Phi-K P)=K rho_b. In the spherical aligned sector
with no derivative energy, g_N=g-KP, and varying P gives g=W_eff'(P).
The fermion action in a preferred rest frame is

\[
S_f=\int dt\,d^3x\,\psi^\dagger(i\hbar\partial_t-H_f)\psi,
\quad
H_f=\frac{p_x^2+p_y^2-p_0^2}{2m_*}\Gamma_1+v p_z\Gamma_2
+h\sum_{j=1}^3P_j\Gamma_{j+2},\quad p=-i\hbar\nabla.
\]

An explicit four-dimensional Clifford realization is

\[
\Gamma_1=\sigma_x\otimes I,\ \Gamma_2=\sigma_z\otimes I,
\quad (\Gamma_3,\Gamma_4,\Gamma_5)
=\sigma_y\otimes(\sigma_x,\sigma_y,\sigma_z).
\]

Their anticommutators are 2 delta_ab. Thus E=+/-sqrt(q1^2+q2^2+Delta^2),
where q1=(p_perp^2-p0^2)/(2m*), q2=v pz, Delta=hP. Each energy has
degeneracy two; denote the total occupied negative-band degeneracy N (N=2 for
one such four-component fermion). The state is filled negative bands, empty
positive bands, zero chemical potential, zero temperature. Fix an energy-tube
cutoff q1^2+q2^2<Lambda^2 with Lambda<p0^2/(2m*). The full tube then lies in
the physical momentum domain. Exactly,

\[
\frac{d^3p}{(2\pi\hbar)^3}
=\frac{m_*}{4\pi^2v\hbar^3}dq_1dq_2,\qquad
A=\frac{Nm_*}{2\pi v\hbar^3},\qquad
\epsilon_f(\Delta)=-A\int_0^\Lambda q\sqrt{q^2+\Delta^2}\,dq
=-\frac A3[(\Lambda^2+\Delta^2)^{3/2}-\Delta^3].
\]

The source normalization is essential: rescaling P would change P dot grad
Phi, so h is a physical portal parameter, not a removable field convention.
The Hamiltonian fixes how P changes the microscopic bands. The gravitational
coupling P dot grad Phi itself is still an assumed bridge, not derived from
the band Hamiltonian or equivalence principle.

Introduce allowed local bare terms C0+b2 P^2/2. Then

\[
W_{\rm eff}=C_0+\frac{b_2}2P^2+\epsilon_f(hP),\qquad
b_2=K+A h^2\Lambda
\]

is the critical susceptibility condition. It is a tuning. The finite remainder
after that choice is

\[
W_{\rm eff}=\epsilon_{\rm vac}+\frac K2P^2+V_{\rm rem},\quad
\epsilon_{\rm vac}=C_0-\frac{A\Lambda^3}3,
\]
\[
V_{\rm rem}=\frac A3\left[
\Delta^3-(\Lambda^2+\Delta^2)^{3/2}+\Lambda^3
+\frac32\Lambda\Delta^2\right].
\]

The resulting force observable is the on-shell baryonic field:

\[
\boxed{g_N=R(P)=A h^2P[\Lambda-\sqrt{\Lambda^2+h^2P^2}+hP],
\qquad g=KP+R(P).}
\]

At small positive P,

\[
R=A h^3P^2-\frac{A h^4}{2\Lambda}P^3+O(P^5),
\qquad \boxed{a_0=\frac{K^2}{A h^3}},\qquad
g_N=\frac{g^2}{a_0}+O(g^3).
\]

The dimensions in SI are [P]=kg/m^2, [h]=m^4/s^2 (hP is energy),
[A]=s^4/(kg^2 m^7), [K]=m^3/(kg s^2). Consequently K^2/(A h^3) is
an acceleration. The h here is a portal coupling, not Planck's constant.

It does not yield the exact CFG695 potential. In particular inversion of
g=KP+R gives

\[
g_N=\frac{g^2}{a_0}
-\left[\frac2{a_0^2}+\frac{A h^4}{2\Lambda K^3}\right]g^3+O(g^4),
\]

whereas CFG695 has -g^3/a0^2. The sign and factor discrepancy cannot be removed
by positive h,A,Lambda in this bare-quadratic regulated model. An additional
analytic P^4 operator can change this subleading coefficient, but is new
input and still does not supply a capacity.

For x=hP/Lambda>0, R>0 and R'>0. The latter is equivalent to
1+2x>(1+2x^2)/sqrt(1+x^2), whose squared difference is
x(4+x+4x^2)>0. Thus g(P) is monotone and locally stable in the radial
algebraic reduction. In the fixed-cutoff model, as P goes to infinity,

\[
R=A h^2\Lambda P-\frac{A h\Lambda^2}2+O(P^{-1}),
\quad u=KP\longrightarrow\infty,\quad
\frac{g_N}{g}\longrightarrow\frac{A h^2\Lambda}{K+A h^2\Lambda}.
\]

There is no finite saturation capacity. At gaps above the cutoff this is a
mathematical fact about the regulated model, not a controlled prediction of a
material's unknown ultraviolet bands. A high-field redefinition of measured G
can change the asymptotic slope but cannot make the physical polarization
bounded. The low-field cubic mismatch is already within the cutoff expansion.

## 3. Finite-temperature discriminator

At zero chemical potential and temperature T expressed in energy units, the
same finite-cutoff determinant is

\[
\Omega_f(\Delta,T)=-2AT\int_0^\Lambda q
\log[2\cosh(\sqrt{q^2+\Delta^2}/(2T))]dq.
\]

Differentiating the integral, not assuming a thermal force law, gives

\[
\partial_\Delta\Omega_f
=-2AT\Delta\log\frac{\cosh(\sqrt{\Lambda^2+\Delta^2}/(2T))}
{\cosh(\Delta/(2T))}.
\]

Keeping the zero-temperature b2, the residual linear susceptibility is

\[
\lim_{P\to0}\frac{g_N}P
=A h^2[\Lambda-2T\log\cosh(\Lambda/(2T))]>0.
\]

It equals 2 A h^2 T ln2 up to exponentially small cutoff corrections at
T<<Lambda. Thus the zero-temperature critical tuning is lost. Even allowing
the extra tuning b2(T)=K+2 A h^2 T ln cosh[Lambda/(2T)], the residual is

\[
g_N=A h^4\left[\frac1{4T}-\frac{\tanh(\Lambda/(2T))}{2\Lambda}\right]P^3
+O(P^5),
\]

not P^2; the bracket is strictly positive for T>0. This extends the already
known thermal-rounding result by retaining the same finite regulator and the
two distinct critical-tuning choices. The force follows from the determinant
and its specified source, not a chosen map from temperature to acceleration.

If a physical realization equilibrates at T_dS=hbar H/(2pi), the thermal
crossover is hP of order T_dS. Whether it does so is unresolved: a preferred
frame nodal medium is not the relativistic conformal vacuum. Even provisionally
identifying this bath does not select a0. In the low-field regime P~g/K,

\[
\frac{hP}{T_{\rm dS}}\simeq\frac{2\pi c h}{\hbar K}\frac g{a_H},
\]

and the independent dimensionless portal c h/(hbar K) remains.

## 4. Gravitating constant and independent counterterms

The same regulator gives epsilon_f(0)=-A Lambda^3/3, a negative filled-band
energy. Normal ordering to zero is a convention in a nongravitating material,
not a prediction of positive cosmic vacuum energy. Grant provisionally that
the completed model's constant contributes covariantly as
-integral sqrt(-g) epsilon_vac, so T_munu=-epsilon_vac g_munu. Then

\[
a_0=\kappa c\sqrt{G\rho_{\rm DE}}
=\kappa\sqrt{G\epsilon_{\rm vac}},\qquad
\kappa^2=\frac{K^4}{A^2h^6G(C_0-A\Lambda^3/3)}.
\]

For every desired positive kappa_* choose

\[
\boxed{C_0=\frac{A\Lambda^3}3+
\frac{K^4}{A^2h^6G\kappa_*^2}.}
\]

All P derivatives, the excitation spectrum, the critical tuning and the
local static response remain identical; the gravitating constant changes.
These are different cosmological solutions, not identical full cosmologies.
This freedom is the known vacuum zero-mode issue exhibited inside the same
explicit regulated determinant, not claimed as a new general no-go theorem.

At fixed A,Lambda,K the Jacobian of
(W''(0), a0, epsilon_vac) with respect to (b2,h,C0), evaluated using the
critical deep coefficient for a0, is triangular up to its (1,2) entry:

\[
\frac{\partial(W''(0),a_0,\epsilon_{\rm vac})}
{\partial(b_2,h,C_0)}=
\begin{pmatrix}
1&-2Ah\Lambda&0\\
0&-3K^2/(Ah^4)&0\\
0&0&1
\end{pmatrix}.
\]

Here a0 is a coordinate on the *critically tuned* family, not an asserted deep
MOND coefficient off that family. The nonzero determinant displays independent
directions: b2 fixes susceptibility, h changes the deep coefficient, C0 changes
vacuum energy. Symmetry of this Hamiltonian permits all three parameters and
provides no relation between them. A microscopic constraint that removes the
constant direction would be additional physics.

Finally, the finite momentum cutoff and preferred-frame band vacuum do not by
themselves define a conserved covariant stress tensor or equation of state
w=-1. Equating their energy density to dark energy is therefore an extra
assumption even before the constant ambiguity. Taking v=c removes neither
this issue nor the independent parameters N,m*,h,Lambda,C0.

## 5. Spatial applicability and exact remaining gap

The homogeneous determinant is useful but cannot by itself establish a galaxy
law. The frozen NODAL_FORCE_LIMITS analysis already shows a gapless |k| static
kernel and, in its weak-source regime, the wrong point-source mass scaling.
In its gapped derivative expansion it obtains a nonzero mass offset. A single
ring is anisotropic; an isotropic ensemble is an additional construction.
These earlier results are retained, not overwritten by the local reduction.
For P~B/r the local condition hP >> hbar v/r reduces to hB >> hbar v;
going farther out does not automatically improve it.

The remaining task is to produce a covariant microscopic source and state
whose on-shell spatial response has the desired mass law, whose critical
susceptibility is protected, and whose gravitating vacuum term is constrained
with the response coefficient. The Gaussian detector fails the selected
mechanical-response test; the specified nodal determinant passes a local
nonanalytic-power test but fails saturation and normalization tests. Interacting
or nonequilibrium completions remain open and are not solved by this checkpoint.
