# Self-gravity supplies a tidal 1/G normalization

Parent: CE-GRAV-2026-10-19 / CE087. Assigned initial HEAD:
`f4424595259bd1ae40addb890e338f85c4f48eb1`; observed HEAD at first read:
`e28f35029437f94ec2c52f324ba081e30cc67620`. Concurrent work subsequently
changed HEAD; the run manifest records its observed revision and exact input
bytes. This lane writes only `virial_normalization/`. It changes no action,
manuscript, current summary, queue, publication or live simulation.

**Result.** The original repulsive daughter contact admits a constructive
self-gravitating Thomas-Fermi (TF) branch. Its spherical n=1 equilibrium is
locally stable against mass-preserving density perturbations, modulo
translations, in the declared TF Newtonian model. Its physical quadrupole
susceptibility is

\[
 Q_{ij}=-\lambda_T\mathcal E_{ij},\qquad
 \lambda_T={15-\pi^2\over3\pi^2}{R^5\over G}.
 \tag{1}
\]

This is an actual gravity-generated inverse-G normalization; an expansion
about a nongravitating state would miss this branch. It is a response to the
STF tidal Hessian \(\mathcal E_{ij}\), not to uniform acceleration. A separated
object ensemble gives a derivative-dependent coarse polarization with
\(4\pi G\chi_{\rm eff}=0.17327258\,f(kR)^2\), where f is its geometric filling
fraction. Gravity fixes the inverse-G factor and the n=1 shape coefficient;
it does not fix the occupied mass/number density, the filling fraction, a
universal acceleration scale, or the requested acceleration-driven spectrum.

## 1. Exact input and effective-theory boundary

Use a canonical complex daughter Phi of mass m, charge one, and a canonical
complex source X of mass M>2m, charge two, with

\[
 V=m^2|\Phi|^2+M^2|X|^2+g_s(X^*\Phi^2+\mathrm{c.c.})
       +\lambda_{\rm tot}|\Phi|^4,\qquad
 \lambda_{\rm tot}=\lambda_{\rm rep}+{g_s^2\over M^2-4m^2},\quad
 \lambda_{\rm rep}>0.
\]

The **fully threshold-matched**, dilute, one-component daughter contact is
\(g_2=\lambda_{\rm rep}/(2m^2)\) in natural units. This is the coefficient
checked in the pinned `micro_response/DERIVATION.md`, section 1, and its
`EXCHANGE_REVIEW.md`. The older positive-frequency-only coefficient has an
additional analytic source term and is not substituted here. This note takes
the threshold-matched one-component theory as its input, rather than claiming
that the source elimination remains valid at arbitrary density.

Let psi have particle normalization, \(N=\int|\psi|^2\), \(\rho=m|\psi|^2\),
and let \(\mathcal M=mN\) denote the configuration's mass, distinct from the
source particle mass M. Write Newtonian potential U, \(\mathbf g=-\nabla U\),
and \(\nabla^2U=4\pi G\rho\). After removing the rest energy, the isolated
GP-Poisson energy is

\[
 E=T+S+W,\quad
 T={\hbar^2\over2m^2}\int|\nabla\sqrt\rho|^2d^3x,\quad
 S=K\int\rho^2d^3x,\quad
 W=-{G\over2}\iint{\rho(x)\rho(y)\over|x-y|}d^3x\,d^3y,
 \quad K={g_2\over2m^2}.
 \tag{2}
\]

Here K is the equation-of-state coefficient, not 4 pi G. In natural units
\(K=\lambda_{\rm rep}/(4m^4)\). The pressure is \(p=K\rho^2\); the specific
enthalpy is \(h=2K\rho\). For SI numerical work the conversions are

\[
 g_{2,\mathrm{SI}}={\lambda_{\rm rep}\hbar^3\over2m_{\mathrm{SI}}^2c},
 \quad K_{\mathrm{SI}}={\lambda_{\rm rep}\hbar^3\over4m_{\mathrm{SI}}^4c},
 \quad a_s={m g_{2,\mathrm{SI}}\over4\pi\hbar^2}
          ={\lambda_{\rm rep}\hbar\over8\pi m c}.
 \tag{3}
\]

The effective description requires a cold, dilute coherent daughter state,
small source-channel occupation, energies and gradients below the source
elimination scale, small binding and interaction energy per particle relative
to \(mc^2\), weak gravity, and diluteness \(n a_s^3\ll1\). Its existence is a
state assumption, not a demonstrated outcome of X decay. A TF result is exact
for the reduced fluid model and asymptotic for GP: the quantum term cannot be
uniformly neglected at its sharp fluid edge. The compact TF profile has a
logarithmically divergent kinetic integral when inserted literally into T;
a finite-GP configuration must smooth the edge. No finite-parameter error
bound for that surface layer, or proof of convergence of its Love number,
is asserted here. The stability proved below belongs to the TF limit;
its full GP continuation is not proved by the homology calculation.

## 2. Equilibrium, virial balance and stability in the TF model

The stationary GP equation in density form is

\[
 {\mu\over m}=U+2K\rho
       -{\hbar^2\over2m^2}{\nabla^2\sqrt\rho\over\sqrt\rho}.
 \tag{4}
\]

Neglecting the last term gives \(2K\rho+U=\mu/m\). Taking a Laplacian and
requiring a regular center yields the exact n=1 Lane-Emden profile

\[
 \rho_0(r)=\rho_c{\sin(\pi r/R)\over\pi r/R},\quad 0\le r\le R,
 \qquad \rho_0(r)=0\quad(r>R),
\]
\[
 R^2={\pi K\over2G}
    ={\pi\lambda_{\rm rep}\over8Gm^4}\quad(\hbar=c=1),\qquad
 \rho_c={\pi\mathcal M\over4R^3},\quad
 \bar\rho={3\rho_c\over\pi^2},\quad
 {\mu\over m}=-{G\mathcal M\over R}.
 \tag{5}
\]

The amplitude \(\rho_c\), hence mass, is free. The radius is fixed by m and
the matched contact in this limit. Direct integration gives

\[
 S={G\mathcal M^2\over4R},\qquad
 W=-{3G\mathcal M^2\over4R},\qquad E=-{G\mathcal M^2\over2R}.
 \tag{6}
\]

For a general stationary GP configuration, the mass-preserving size variation
\(\rho_s(x)=s^{-3}\rho(x/s)\) gives
\(E(s)=T/s^2+S/s^3+W/s\), and therefore

\[
 2T+3S+W=0,\qquad E''(1)=2T+6S>0.
 \tag{7}
\]

The last result establishes stability under this size variation only. The
following additional argument establishes TF density-mode stability, rather
than extrapolating (7) to every mode.

For a smooth first-order density perturbation in the TF ball, the quadratic
energy coefficient at fixed mass is

\[
 E^{(2)}=K\int(\delta\rho)^2d^3x
   -{G\over2}\iint{\delta\rho(x)\delta\rho(y)\over|x-y|}d^3x\,d^3y.
 \tag{8}
\]

For angular order l>=1, diagonalize the Newton potential operator on the
ball. If its eigenvalue is nu, its regular radial potential is
\(j_l(xr/R)\), \(\nu=4\pi G R^2/x^2\). Matching to the exterior decaying
harmonic gives

\[
 xj_l'(x)+(l+1)j_l(x)=xj_{l-1}(x)=0.
 \tag{9}
\]

The coefficient in (8) in that eigenmode is
\(K-\nu/2=K[1-\pi^2/x^2]\). For l=1 the first root is x=pi and the mode is
\(\delta\rho=-\mathbf a\cdot\nabla\rho_0\), a translation. The higher l=1
roots are 2pi,3pi,... . For l>=2 the lowest root is at least the first
positive zero \(x_1=4.4934094579...\) of j1, by the radial Sturm comparison
as the angular barrier increases. One can check \(x_1>\pi\) directly:
\(\sin x-x\cos x>0\) on (0,pi], since its derivative is x sin x.
Thus every l>=2 density shape direction has positive energy.

For l=0 impose \(\delta\mathcal M(R)=0\), where
\(\delta\mathcal M(r)=4\pi\int_0^r s^2\delta\rho(s)ds\). Then

\[
 E^{(2)}={K\over4\pi}\int_0^R{(\delta\mathcal M')^2\over r^2}dr
          -{G\over2}\int_0^R{(\delta\mathcal M)^2\over r^2}dr.
 \tag{10}
\]

The least weighted Dirichlet Rayleigh quotient is \(x_1^2/R^2\): its regular
eigenfunction is \(r^2j_1(x_1r/R)\), vanishing at R. Equations (5) and (10)
again give strict positivity. The weakest nontranslation density gap in this
comparison is \(1-\pi^2/x_1^2=0.51118136...\). The velocity kinetic energy
is nonnegative, so these TF density perturbations have no exponentially
growing linear mode. Vortical/barotropic relabeling zero modes need not change
density; the claim is not that every fluid coordinate has a positive gap.

For smooth free-surface deformations there is no first-order surface delta
mass, because \(\rho_0(R)=0\). The first-order density is covered by (8).
Outside the ball \(U-\mu/m\ge0\); placing first-order positive density there
does not introduce a negative first variation. These observations delimit the
usual local energetic stability statement. This is not a proof of nonlinear
global stability for arbitrary shocks, finite-temperature matter, quantum
tails or the full two-field relativistic model.

Rescaling the TF linear Euler-Poisson equations by R, \(\mathcal M/R^3\), and
\(t_{\rm dyn}=\sqrt{R^3/(G\mathcal M)}\) removes the mass amplitude. Each
positive density-mode frequency therefore has the form

\[
 \Omega_\alpha^2=c_\alpha{G\mathcal M\over R^3},\qquad
 {\bar\rho\over\Omega_\alpha^2}={3\over4\pi c_\alpha G}.
 \tag{11}
\]

The dimensionless \(c_\alpha\) is mode-specific; it is zero for translation.
This explicitly realizes the suggested gravity-generated displacement
normalization. The physically relevant source and mode overlap still matter.

## 3. Exact static quadrupolar susceptibility and the l=1 contrast

Use the STF mass moment and the STF external tidal Hessian

\[
 Q_{ij}=\int\rho(x)(x_ix_j-\delta_{ij}r^2/3)d^3x,\qquad
 \mathcal E_{ij}=\partial_i\partial_jU_{\rm ext}
                      -\delta_{ij}\nabla^2U_{\rm ext}/3.
 \tag{12}
\]

Coordinates are centered on the freely falling inertial COM. In external
vacuum the trace vanishes, and the applied quadrupole potential is
\(U_{\rm ext}^{(2)}=\mathcal E_{ij}x_ix_j/2\). The coupling is
\(E_{\rm ext}^{(2)}=Q_{ij}\mathcal E_{ij}/2\); there is no internal
\(-D_i g_i\) term. The quadrupole exterior potential is
\(\delta U_Q=-3G Q_{ij}n_in_j/(2r^3)\). These definitions remove possible
factors of 2 or 3 between mass-moment, Legendre and Love-number conventions.

For an axisymmetric tracefree source, take
\(\mathcal E_{zz}=e\), \(\mathcal E_{xx}=\mathcal E_{yy}=-e/2\). Then
\(U_{\rm ext}^{(2)}=(e/2)r^2P_2(\cos\theta)\). Set
\(H=\delta U_{\rm self}+U_{\rm ext}^{(2)}\). Linear hydrostatics gives
\(\delta\rho=-H/(2K)\). Since the applied potential is harmonic,

\[
 (\nabla^2+\pi^2/R^2)H=0,\quad
 H=A j_2(\pi r/R)P_2,\quad
 \delta U_{\rm self,out}=B r^{-3}P_2.
\]

Continuity of self-potential and radial derivative at R gives

\[
 A[\pi j_2'(\pi)+3j_2(\pi)]={5eR^2\over2},\quad
 \pi j_1(\pi)=1,\quad j_2(\pi)={3\over\pi^2},
\]
\[
 A={5eR^2\over2},\qquad
 B={eR^5\over2}{15-\pi^2\over\pi^2},\qquad
 Q_{zz}=-{2B\over3G}=-{15-\pi^2\over3\pi^2}{R^5\over G}e.
 \tag{13}
\]

Rotational covariance establishes (1) on the entire STF sector. Independently,
integrating \(Q_{zz}=(8\pi/15)\int_0^R r^4\delta\rho_2(r)dr\) gives the same
constant. The apsidal convention is
\(k_2=3G\lambda_T/(2R^5)=(15-\pi^2)/(2\pi^2)=0.2599088773...\).

For a regular harmonic source \(a_l r^lY_{lm}\), the same boundary calculation
has denominator \(\pi j_{l-1}(\pi)\). At l=1 it is zero: a static affine
force does not admit a supported equilibrium for an isolated freely falling
object. Removing COM motion removes this source altogether. An arbitrary
coefficient inferred from \(\bar\rho/\Omega^2\) cannot turn that translation
zero mode into an internal mass dipole. Nonzero-frequency l=1 internal
compressional modes, if present, also have zero total mass-dipole overlap in
the COM frame. This does not assert that all l=1 perturbations are translations.

The quadratic energy associated with the induced STF response can be written

\[
 E_{\rm shape}(Q,\mathcal E)={Q:Q\over4\lambda_T}
                  +{Q:\mathcal E\over2},\qquad
 E_{\rm on\ shell}=-{\lambda_T\over4}\mathcal E:\mathcal E.
 \tag{14}
\]

The linear, adiabatic regime needs
\(|\mathcal E|\ll G\mathcal M/R^3\) and forcing frequencies below the relevant
shape modes. Nonlinear distortion/disruption occurs at a density-dependent
tidal scale, not a selected universal acceleration. Gravitational binding
supplies the spring and inverse-G factor without an external anchor.

## 4. What an ensemble can produce at finite wavelength

Suppose a dilute ensemble consists of identical, separated spherical objects,
number density \(n_o\), with COM motion treated separately. Set
\(S_{ij}=n_oQ_{ij}=-n_o\lambda_T\mathcal E_{ij}\). To quadrupole order its
coarse source density relative to monopoles is

\[
 \delta\rho_Q={1\over2}\partial_i\partial_jS_{ij}
       =-\nabla\cdot\mathbf P_{\rm eff},\qquad
 (P_{\rm eff})_i=-{1\over2}\partial_jS_{ij}.
 \tag{15}
\]

This P is a multipole bookkeeping field; each object's physical internal mass
dipole is still exactly zero. With uniform \(n_o\), using the STF Hessian in
(12), and Fourier convention \(\nabla\to i\mathbf k\), one obtains

\[
 (P_{\rm eff})_i={n_o\lambda_T\over3}\partial_i\nabla^2U
       ={n_o\lambda_T\over3}k^2g_i,
 \quad \chi_{\rm eff}(k)={n_o\lambda_T\over3}k^2,
 \quad\delta\rho_Q=-{n_o\lambda_T\over3}\nabla^4U.
 \tag{16}
\]

Here a longitudinal Fourier source generally has a traceful Hessian; (16)
retains only its l=2 STF response. The monopole/trace compressibility is a
different channel, not silently included. Equivalently (16) follows by
varying the ensemble energy \(-n_o\lambda_T\mathcal E:\mathcal E/4\).
For a locally harmonic vacuum U and constant \(n_o\),
\(\partial_j\mathcal E_{ij}=0\): objects have nonzero quadrupoles but no leading
bulk \(P_{\rm eff}\). Boundaries and variations of \(n_o\) introduce gradients
of \(n_o\), as is explicit in (15).

Write the geometric filling fraction \(f=4\pi n_oR^3/3\), and
\(C=(15-\pi^2)/(3\pi^2)=0.173272584878...\). Comparison with the requested
acceleration susceptibility \(1/(4\pi G)\) gives

\[
 4\pi G\chi_{\rm eff}(k)=C f(kR)^2.
 \tag{17}
\]

In the separated long-wavelength regime \(f\le1\), \(kR\ll1\), this is much
smaller than one. Matching one would require
\(f(kR)^2=1/C=5.771253431...\), outside that joint regime. Choosing R or
\(n_o\) to fit one wavelength does not derive a local acceleration dipole law.
At \(kR\sim1\) the multipole expansion itself requires replacement; at large
overlap the independent-object model requires replacement. Neither is ruled
out as an unstudied many-body phase. The calculation does establish exactly
which inverse-G normalization occurs in the controlled branch and why it
does not yet supply the requested physical acceleration polarizers.

## 5. Quantum-pressure regime and absence of a selected a0

If contact pressure is negligible, the stationary Schrödinger-Poisson (SP)
equations are

\[
 -{\hbar^2\over2m^2}\nabla^2\sqrt\rho+U\sqrt\rho
       ={\mu\over m}\sqrt\rho,\qquad \nabla^2U=4\pi G\rho.
 \tag{18}
\]

Given any regular decaying equilibrium seed, the following is an **exact**
one-parameter family of SP equilibria at fixed m and G:

\[
 \rho_s(r)=s^4\rho_1(sr),\quad U_s(r)=s^2U_1(sr),\quad
 \mu_s=s^2\mu_1,\quad \mathcal M_s=s\mathcal M_1,\quad R_s=R_1/s.
 \tag{19}
\]

R can be any consistently scaled radius definition, e.g. the radius enclosing
a fixed mass fraction. Thus \(\mathcal M R=C_R\hbar^2/(Gm^2)\), where the
coefficient depends on the chosen seed and radius definition. No SP profile
was solved here, and no numerical value of \(C_R\) or a universal SP stability
theorem is claimed from (19). If the seed is a constrained energy minimum,
the rescaling preserves that energetic stability class: the mass constraint
and energy functional are mapped into each other, up to a positive factor.
In the time-dependent SP equations \(t\to s^2t\), so mode frequencies scale
as \(\Omega_s=s^2\Omega_1\). Its static tidal coefficient scales as
\(\lambda_{T,s}=s^{-5}\lambda_{T,1}\propto R_s^5/G\), when a finite adiabatic
shape response exists. Surface acceleration scales as \(s^3\), freely.

For general profiles, dimensional virial balance gives the two controlled
asymptotic sizes \(R_Q\sim\hbar^2/(G\mathcal M m^2)\) and
\(R_{\rm TF}\sim\sqrt{K/G}\). A fixed-shape interpolating ansatz is not an
exact GP mass-radius curve because the profile changes in the crossover.
At the TF radius define

\[
 \mathcal M_*={\hbar^2\over Gm^2R_{\rm TF}},\qquad
 {\xi_c^2\over R_{\rm TF}^2}={\mathcal M_*\over2\mathcal M},\quad
 \xi_c={\hbar\over\sqrt2 m c_{s,c}},\quad
 c_{s,c}^2=2K\rho_c={G\mathcal M\over R_{\rm TF}}.
 \tag{20}
\]

TF interiors require \(\mathcal M\gg\mathcal M_*\); small masses enter the
quantum-pressure regime. Weak gravity additionally requires
\(\mathcal M\ll R_{\rm TF}c^2/G\), plus the other effective-theory conditions
in section 1. In TF the radius is fixed but
\(g_{\rm surf}=G\mathcal M/R_{\rm TF}^2\), the mode frequencies, and the nonlinear
tidal threshold still depend on the free mass/density. SP has the continuous
rescaling (19). Neither relation selects a universal a0, an ensemble mass
function or the rational gap distribution. This is an unresolved selection
obligation, not a no-go theorem for every possible state of the original action.

## 6. Pinned benchmark and purely geometric length comparisons

The numeric input is \(m=1\,\mathrm{MeV}/c^2\),
\(\lambda_{\rm rep}=0.005875\). `inputs.json` declares fixed SI values
\(\hbar=1.054571817\times10^{-34}\,\mathrm{J\,s}\),
\(c=299792458\,\mathrm{m/s}\), \(1\,\mathrm{eV}=1.602176634\times10^{-19}\,J\),
\(G=6.67430\times10^{-11}\,\mathrm{m^3/(kg\,s^2)}\), and
\(1\,\mathrm{pc}=3.085677581491367\times10^{16}\,m\). These are numerical
conversion inputs, not a new measurement or a precision claim.

The executed results are

\[
 R_{\rm TF}=1.15716937\times10^8\,m=3.75013054\times10^{-9}\,pc,
 \quad a_s=4.61269226\times10^{-17}\,m,
\]
\[
 \mathcal M_*=4.53118393\times10^{-7}\,kg,\quad
 {R_{\rm TF}c^2\over G}=1.55823377\times10^{35}\,kg,
 \quad\lambda_T=5.38652628\times10^{49}\,\mathrm{kg\,m^2s^2}.
 \tag{21}
\]

The second mass is the compactness-one dimensional scale, not an actual GR
maximum mass. Setting the center's \(n a_s^3\) to one would give
\(3.58349212\times10^{43}\,kg\) within the TF formulas; source-elimination and
relativity limits can intervene first. A central healing-length estimate is
not a uniform error estimate at the surface.

For declared comparison domains L, define k=1/L, not 2pi/L. The numbers are
geometric comparisons only; no observed galaxy field or population is inferred.

| L | R/L | upper value of 4 pi G chi_eff at f=1 |
|---|---:|---:|
| 1 pc | 3.75013e-9 | 2.43682e-18 |
| 1 kpc | 3.75013e-12 | 2.43682e-24 |
| 10 kpc | 3.75013e-13 | 2.43682e-26 |

If L instead means full wavelength, k=2pi/L multiplies the last column by
4 pi squared. It does not remove the long-wavelength suppression.

## 7. Verification, source scope and remaining bridge

`check_virial.py` integrates the regular l=2,3,4 radial Helmholtz problem at
three tolerances, compares the boundary coefficient to spherical Bessel
functions, integrates the induced Qzz directly, checks the first j1 root,
and computes (21) and the table. These are nine finite ODE checks and one
independent moment quadrature, not a ground-state formation or quantum-tail
simulation. Worst ODE response discrepancy was 7.50e-16; direct Qzz discrepancy
was 2.78e-17 in units G=R=e=1. The strict gap and l=1 zero are analytic results;
floating residuals alone are not their proof.

The bounded runner completed in 1.216356 s, with 30 s wall timeout, 20 s
per-process CPU cap, 65536-byte log cap and one requested numerical-library
thread. No hard memory or CPU-affinity limit was requested. Python 3.9.6,
NumPy 1.26.2 and SciPy 1.11.4 were observed. The v2 manifest passed hash and
current-input validation. See `VERIFICATION.md` for exact regeneration commands,
`source_pins.json` for antecedent bytes, and `SOURCES.md` for exact primary
versions and convention checks.

The equilibrium, Hessian, boundary response, multipole expansion and scaling
arguments above were independently derived here. Checked primary-source
comparisons are limited to the n=1 equilibrium formulas and Love convention;
no cited Gaussian stability result is promoted to an exact GP theorem.

The strongest achieved bridge is therefore **a stable self-gravitating TF
shape polarizer whose physical tidal susceptibility has an exact inverse-G
normalization**. The remaining obligations are production and occupation of
such configurations, a source coupling that yields the requested physical
acceleration dipoles rather than STF tides, and selection of the distribution,
filling/size factors, nonlinear law and a0. A dense collective state beyond the
separated-object regime remains open; the present argument neither constructs
nor excludes it.
