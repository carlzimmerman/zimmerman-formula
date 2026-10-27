# Occupied soft pairs from a declared baryon landscape

19 October 2026. Parent: CE-SHARED-STATE-2026-10-19 / CE-FM092.
Exact input bytes and observed HEAD are in `source_pins.json`.
This lane writes only `occupied_landscape/`.

**New result.** A specific disjoint-pair selection from a dilute Poisson
baryon snapshot gives a gap/dipole joint measure without choosing the target
weight. Its three-dimensional void statistics produce a log-cubic soft tail,
not a Griffiths power. Fixed-level Newtonian binding does justify an
exponential overlap asymptotically; changing the binding level does not
preserve its localization length. The complete gravitational source includes
both baryons and their quantum recoil, and has zero uniform dipole. A
conditional hard-core scalar trace supplies an actual singly occupied
fraction. It also reveals a soft-pair loading obstruction from the original
attractive interwell gravity. The original contact supplies a conditional
phonon bath with energy-fifth-power dipole noise and a correspondingly slow
relaxation rate. No target spectrum, actual halo inventory, or universal
normalization is obtained.

## 1. Original particles and physical hypotheses

Use the pinned original charge-one daughter Phi, charge-two source X,
repulsive positive-square scalar potential, minimal gravity, and the
threshold-matched daughter contact

\[
g_2=\lambda_{\rm rep}/(2m^2)>0,\qquad
H_d=\int\left[|\nabla\psi|^2/(2m)+(g_2/2)\psi^{\dagger2}\psi^2\right]
 +H_{\rm gravity}.
\]

Natural units hbar=c_light=k_B=1 are used. This is the daughter-only dilute
NR regime, with negligible real X stock, chemical/excitation energies well
below the eliminated-channel detuning, and separately specified ordinary
matter. No independent scalar-baryon contact, fermion force sector, target
gap weight, or negative gravitational mass is introduced.

The declared environment consists of identical baryon centers of mass M_b
and number density n_b, approximately Poisson on the separations considered.
It is a finite patch or a conditional local landscape, not an infinite
unscreened Newtonian equilibrium. Large-scale potential, tides, baryon
stress and the patch's lifetime must be specified separately. Identical
centers, inversion symmetry of an isolated pair, a dilute localized scalar,
and weak external tidal detuning are additional hypotheses. A real ordinary
matter phase is not established by naming these hypotheses.

Take only **mutual nearest-neighbor** pairs as candidate hosts. This makes
the selected pairs disjoint: one baryon belongs to at most one pair. They
are not statistically independent, and a sum of independent pair responses
additionally neglects interpair scalar hopping and mutual interactions.
Below, M=2 M_b is one physical host mass, counted once. One daughter in a
host has mass m. Large occupations, a coherent GP droplet, or an actual
many-particle collective double well need the separate nonlinear analysis.

## 2. Exact geometric intensity, without duplicated host mass

For a tagged Poisson center, absence of another center within radius r
has probability exp[-4 pi n_b r^3/3]. Differentiating gives the familiar
directed nearest-neighbor density. Directed choices are not disjoint hosts.

For two centers at separation r to be mutual nearest neighbors, their
union of radius-r balls must contain no other centers. The intersection
volume is 5 pi r^3/12, hence the union volume is 9 pi r^3/4. The expected
unordered-pair intensity per physical volume is therefore

\[
 {d n_{\rm pair}\over dr}=2\pi n_b^2 r^2 e^{-b r^3},\qquad
 b={9\pi n_b\over4}.
\]

The factor one-half in unordered counting is essential. Integrating gives

\[
 n_{\rm pair}={8n_b\over27},\quad
 p_{\rm pair}(r)=3br^2e^{-br^3},\quad
 {2n_{\rm pair}\over n_b}={16\over27}.
\]

Thus this selection uses 16/27 of the baryons, once each. These identities
are derived from the Poisson empty-volume law, not taken from an empirical
pair distribution. A minimum admissible separation r_min or another host
selection multiplies the intensity by its actual retention indicator; it
does not preserve the same normalization automatically. If r>=r_min is
the only restriction, its retained density is n_pair exp[-b r_min^3].
Hard-core baryon structure, correlations, tidal rejection or a non-Poisson
phase change the intensity and must be propagated.

## 3. Fixed-level gravitational tunneling and its domain

For one daughter and two well-separated heavy centers, the leading
Born-Oppenheimer relative-coordinate potential is

\[
 V(\boldsymbol q;r)=-GmM_b\left({1\over|\boldsymbol q-\boldsymbol r/2|}
                  +{1\over|\boldsymbol q+\boldsymbol r/2|}\right).
\]

Finite baryon size, a common scalar mean field, and tides may change this
potential. They are not included in the Coulomb control. Define
mu_r=mM/(m+M), a_G=1/(mu_r GmM_b). In a heavy-center approximation one may
replace mu_r by m; finite nuclear/host recoil and nonadiabatic corrections
are not fully captured by this one-coordinate BO Hamiltonian. Its isolated
one-center 1s state has E_b=-1/(2 mu_r a_G^2). The normalized density is
exp[-2|q|/a_G]/(pi a_G^3), with Fourier form factor

\[
 F(q)=[1+(a_G q/2)^2]^{-2}.
\]

For a fixed bound level, E_b stays negative as r grows. The longitudinal
forbidden-region action is

\[
 S(r)=\int_{q_-}^{q_+}
       \sqrt{2\mu_r[V(q;r)-E_b]}\,dq
       ={r\over a_G}+O(\log(r/a_G)).
\]

One elementary justification is to exclude fixed-width neighborhoods of
the turning points. The integrand in the interior approaches 1/a_G; its
Coulomb correction integrates like int dq/q at the two ends. The excluded
end pieces contribute at most sublinear terms. In particular S(r)/r ->1/a_G.
The finite control evaluates the explicit action at fixed E_b, not an exact
two-center energy splitting. The actual hopping has the form

\[
 J(r)=J_* A(r/a_G)e^{-r/a_G},\qquad \log A(x)=O(\log x)
\]

in the fixed-level separated-well asymptotic, with a prefactor and matching
that require the actual wavefunctions. A constant square barrier gives the
exact diagnostic exponential J=J_0 exp[-r/xi] at this level of description,
where xi=[2 mu_r(V_barrier-E_b)]^(-1/2). This diagnostic is useful for an
exact pushforward below; it is not asserted as the entire Coulomb splitting.

There is also an explicit, original-potential two-orbital control, without
an invented square barrier. Put x=r/a_G and E_H=1/(mu_r a_G^2), and use
translated 1s orbitals phi_L,phi_R. Direct Coulomb/overlap integrals give

\[
 S=e^{-x}(1+x+x^2/3),\quad
 C=-1/x+e^{-2x}(1+1/x),\quad K=-(1+x)e^{-x},
\]
\[
 H_{LL}/E_H=-1/2+C,\quad H_{LR}/E_H=-S/2+K,\quad
 \boxed{J_{\rm LCAO}=E_H{CS-K\over1-S^2}
              \sim {2E_H\over3}x e^{-x}}.
\]

This is the exact generalized-eigenvalue splitting in the two-1s trial
subspace. It is an explicitly specified approximate physical gap map for
(3), (5) and (10), not an exact solution of the three-dimensional two-center
Schrodinger equation or its exact asymptotic prefactor. Varying the orbitals
would improve that approximation. The gap is obtained from potential matrix
elements, not selected to fit an occupied spectrum. It supplies the same
leading log-cubic void exponent as the WKB action. A chosen r_min>>a_G
keeps the separated-well approximation distinct from a merged single well.

The constant localization length is **not** generic to all soft gravitational
states. If the isolated level itself approaches zero binding, xi changes;
for hydrogenic level n, its outer exponential scale grows as n a_G. Mixing
such levels requires their own density, source sizes, and capture weights.
The soft tail below concerns fixed-level, large-separation pairs only.

There is also a lifetime condition. For unsupported baryons the host's
dynamical time is polynomial, tau_host~sqrt[r^3/(GM)], whereas J^(-1)
grows exponentially. Eventually J tau_host<<1. A static TLS extrapolation
to arbitrarily soft pairs is then invalid. A supporting material phase or a
fully dynamical host calculation is needed; a Poisson snapshot supplies
neither. The mathematical tail is conditional even before occupation.

## 4. Complete finite-wavelength source, including recoil fluctuations

Let q be the daughter position relative to the baryon host COM. In the
total COM frame, the scalar coordinate is alpha q and the two baryon
coordinates are -beta q +/- r e/2, with

\[
 \alpha={M\over M+m},\quad \beta={m\over M+m},\quad
 \alpha+\beta=1,\quad m\alpha=M\beta=\mu_r.
\]

For the physical common gravitational probe h_k(z)=sin(kz)/k, the internal
operator in this BO coordinate is

\[
 D_k(q)={m\sin(k\alpha q_z)
       -M\cos(kr u/2)\sin(k\beta q_z)\over k},\quad u=e_z.
\]

It is odd in q and includes both centers and their recoil. For localized
1s packets centered at q=+/-r e/2, write x=kr u/2. Their opposite source
expectations are +/-d_signed, where

\[
 d_{\rm signed}(r,u;k)
 ={m F(\alpha k)\sin(\alpha x)
    -M\cos x F(\beta k)\sin(\beta x)\over k}.       \tag{1}
\]

The baryon form factor F(beta k) is the host's **quantum recoil** caused
by the relative wavefunction width. Omitting it treats the host as recoiling
only with the mean packet center. Its cos x factor is the actual two-center
host shape; replacing this by a point recoil host is another physical model.
In the separated-well limit, orthogonalizing left/right localized packets
changes (1) by exponentially small overlap corrections. The exact density
matrix elements of the actual two-center eigenstates would replace the
1s approximation when the full spectrum is solved.

Within the explicit two-1s subspace above, parity gives
<L|D_k|R>=0 and the transition/saturation dipole is exactly
d_LCAO=|d_signed|/sqrt(1-S^2). This follows by normalizing the even and odd
states (L+R)/sqrt[2(1+S)] and (L-R)/sqrt[2(1-S)]. Use this corrected d
together with J_LCAO when implementing that finite-overlap control; (1)
itself is the localized expectation before orthogonalization.

For k=0, D_0(q)=0 pointwise. A large subsystem dipole m alpha r/2 is not a
physical uniform gravitational dipole. At small k, put s=ru/2. Expansion of
the full expression gives

\[
 d_{\rm signed}=k^2\mu_r\left[{(1+\beta)s^3\over3}
                    -{a_G^2(\alpha-\beta)s\over2}\right]+O(k^4).
                                                        \tag{2}
\]

The packet-width term is required by the full source. The cubic term
dominates at large r for fixed nonzero u inside kr<<1. Equation (2) must
not be extended to r->infinity at fixed k: the exact source is bounded by
(m+M)/|k|. Its zeros and orientation dependence remain in the exact
pushforward. Different sources have different form factors.

With symmetric wells and one scalar, the retained TLS is
H_1=E_b I-J sigma_x-g d_signed sigma_z. Its zero-field gap is Omega=2J.
Here and in the occupation formulas below, E_b=E_b(r) denotes the common
one-particle level center, including the other well's common energy shift;
the isolated E_b in section 3 is its r->infinity limit. In the two-1s
control the center is E_H[-1/2+(C-KS)/(1-S^2)].
Writing d=|d_signed|, its ground-state response is

\[
 P_1(g)={d^2g\over\sqrt{J^2+d^2g^2}},\qquad
 \Delta={J\over d}={\Omega\over2d},
\]

and saturates at +/-d within this projection. Actual higher vibrational
states, escape and deformation must stay inaccessible. A bias epsilon
changes H_1 to E_b I-J sigma_x+(epsilon/2-g d_signed)sigma_z, gives
Omega=sqrt(4J^2+epsilon^2), and removes the symmetric one-parameter kernel.
In its energy basis the transition dipole is d*(2J/Omega), distinct from
the saturation magnitude d. Small J does not imply small actual gap when
ordinary tidal or well-depth detuning is present.

## 5. Available joint measure and actual occupation measures

The zero-bias, one-candidate-per-disjoint-pair available measure is

\[
 \nu_{\rm av}(dd\,d\Omega)=n_{\rm pair}\int_0^\infty
 p_{\rm pair}(r)dr\int_{-1}^{1}{du\over2}
 \delta_{|d_{\rm signed}(r,u;k)|}(dd)\delta_{2J(r)}(d\Omega).
                                                        \tag{3}
\]

A retention factor for valid host lifetime, tides and single-level
projection belongs inside this integral. If detunings occur, integrate the
actual conditional measure q(d epsilon|r,u) and use the biased gap/source
dictionary. These factors are state data, not a new force law.

For a preparation with captured single-scalar probability f_1(r,u,t),
replace the integrand by f_1 times itself. This is an actual occupied
measure only after f_1 is calculated from a specified preparation or trace.
Conditional internal populations p_g,p_e must be recorded separately.
Phonon relaxation of p_g,p_e does not create a captured particle or set f_1.
For example, the fixed-single-sector Gibbs response is

\[
 P_1(g,T)={d^2g\over E(g)}\tanh[\beta E(g)],\quad
 E(g)=\sqrt{J^2+d^2g^2},\qquad
 \chi_1(T)={d^2\over J}\tanh(\beta J).
                                                        \tag{4}
\]

The thermal response contains the population difference, not a raw mode
count. Equations (3)-(4) retain both d and Omega; their thermal response
cannot in general be represented by a temperature-independent marginal
weight w(Delta).

### A derived conditional loading law from the same scalar contact

There is a more concrete trace than an unspecified f_1. Project the same
scalar field onto two localized modes and assume the **physical** on-site
energy U_eff is positive and large compared with J,T and reservoir energy
offsets, so n_L,n_R=0,1. Its contact part is

\[
 U_{\rm contact}=g_2\int|\phi_L|^4={g_2\over8\pi a_G^3}.
\]

On-site gravitational matrix elements and higher-level corrections belong
in U_eff; positivity of g_2 by itself does not verify this hierarchy. This
is a conditional hard-core limit derived from the projected original
Hamiltonian. It does not impose a new pair-level exclusion rule.

The four Fock states have energies 0, E_b-J, E_b+J, and 2E_b+V_LR.
Here V_LR is the interwell pair interaction. For a scalar reservoir chemical
potential mu_Q and z=exp[-beta(E_b(r)-mu_Q)], the exact retained trace gives

\[
 Z_{\rm pair}=1+2z\cosh(\beta J)+z^2e^{-\beta V_{LR}},\qquad
 \boxed{f_1={2z\cosh(\beta J)\over Z_{\rm pair}}}.       \tag{5}
\]

In (5) and (7), E_b is the full r-dependent projected one-body diagonal
defined in section 4, including attraction to the other baryon center.
Substituting the isolated fixed binding energy from the WKB control in its
place would change the loading law. The trace does not make that replacement.

Thus (3) weighted by (5) is an actual **conditional equilibrium** occupied
TLS measure. It depends on the conserved scalar inventory/reservoir and
temperature. Mu_Q is the original daughter chemical potential in this
source-eliminated branch, not a new independently conserved dipole number.
An unconfined global finite-T halo trace is not assumed; this is a local
restricted mode trace in a specified patch/reservoir.

On-site repulsion only forbids two particles in the same localized well.
It permits one in each well of the pair. The original contact and Newtonian
interaction give, to leading separated-well order,

\[
 V_{LR}=2g_2\int|\phi_L|^2|\phi_R|^2
       -Gm^2\iint {\rho_L(x)\rho_R(y)\over|x-y|}dxdy
       =-{Gm^2\over r}+\text{exponentially small terms}.
                                                        \tag{6}
\]

The factor 2 in the contact cross energy is the identical-boson exchange
factor in the two-orthogonal-mode Fock projection. Quantum exchange
gravitational and wavefunction-overlap terms are exponentially small here.
At fixed T=0 the singly occupied sector wins over both empty and doubly
occupied sectors precisely on the chemical-potential interval

\[
 E_b-J<\mu_Q<E_b+V_{LR}+J.                              \tag{7}
\]

Its width is V_LR+2J. With (6) and fixed-level exponential J, that width
eventually becomes negative: the softest widely separated candidate pairs
cannot be singly occupied equilibrium ground sectors in this approximation.
Equivalently, the energy cost to replace two singly occupied equivalent
pairs by one doubly occupied pair and one empty pair is V_LR+2J. This is
a conditional equilibrium selection effect from the original attraction,
not a claim that every metastable formed single packet disappears.
Interpair interactions and a common finite inventory require a coupled
trace and have not been solved. The stated sign argument uses the leading
heavy-host projected energy. Finite-host mass-polarization, host relaxation
and polarization corrections must be included in the actual effective
V_LR before using its very soft endpoint quantitatively. The window (7)
remains exact for the displayed four-sector Hamiltonian with that effective
interaction; the displayed Newtonian/contact matrix elements are not a
complete finite-host spectral theorem.

At finite T, maximizing (5) over z gives

\[
 f_{1,\max}={\cosh(\beta J)\over
          \cosh(\beta J)+e^{-\beta V_{LR}/2}}.
\]

For V_LR<-2J it tends to zero as T->0, even with the best reservoir
chemical potential. Without interwell interaction, f_1 ->2z/(1+z)^2<=1/2
when J/T->0. A captured fixed N_pair=1 state can have f_1=1, but its
formation and slow particle-exchange lifetime are separate required inputs.

## 6. Explicit soft pushforward and why it is not a universal power

The exact exponential diagnostic J=J_0 exp[-r/xi] gives

\[
 \rho_\Omega(\Omega)={3B x^2\over\Omega}e^{-Bx^3},\quad
 x=\log(2J_0/\Omega),\quad B=b\xi^3,\quad 0<\Omega<2J_0.
                                                        \tag{8}
\]

This is an available **gap density**, not an occupied dipole spectrum. Its
logarithmic slope is -1-2/x+3 B x^2; it does not approach a fixed exponent.
The exact Coulomb polynomial prefactor changes x by O(log x), leaving the
leading log-cubic rare-event exponent. Keeping a fixed binding level is
essential to that statement.

For illustration only, temporarily use the subsystem dictionary d=D r,
D=mu_r/2. This is not the physical complete source (1). It permits an
exact variable-dipole conversion, useful for detecting missing Jacobians:

\[
 \Delta=A{e^{-x}\over x},\quad A={J_0\over D\xi},\quad
 x=W(A/\Delta),\quad
 \left|{dr\over d\Delta}\right|={\xi x\over\Delta(1+x)}.
\]

For fixed single occupation and zero T, the dipole-magnitude weight is

\[
 \boxed{w_{\rm sub}(\Delta)
  ={3n_{\rm pair}D\xi B\over\Delta}
     {x^4\over1+x}e^{-Bx^3}}.                          \tag{9}
\]

The factor d(r) and the r-dependent reduced-gap Jacobian both matter.
Actual preparation multiplies (9) by the calculated f_1(r); a fixed-sector
linear Kubo measure additionally contains tanh(beta J). Formula (9) is a
diagnostic and must not normalize common gravity.

The **physical** zero-temperature weight is instead the exact pushforward

\[
 w_k(\Delta)=n_{\rm pair}\int dr\,p_{\rm pair}(r)
 \int_{-1}^{1}{du\over2}\,f_1(r,u)d(r,u;k)
 \delta\left(\Delta-{J(r)\over d(r,u;k)}\right).        \tag{10}
\]

At source zeros d=0 there is no response weight; one does not assign them
a finite reduced gap. A density representation sums all roots of
Delta=J/d with their actual derivative. Nonmonotone finite-k form factors
do not admit the single Lambert-W inversion in (9).

A useful exact bound avoids root counting. At fixed k!=0, put
d_max=(m+M)/|k| and assume 0<=f_1<=1. Then in the exact exponential control

\[
 \int_0^\delta w_k(\Delta)d\Delta
 \le n_{\rm pair}d_{\max}
 \exp\{-B[\log(J_0/(\delta d_{\max}))]^3\},
 \qquad \delta d_{\max}<J_0.                           \tag{11}
\]

Indeed Delta<delta implies J<delta d_max and therefore
r>xi log[J_0/(delta d_max)]. The Poisson tail integrates exactly. This
bound decays faster than every positive power of delta. Validity
retention, finite loading probability, and finite-T population difference
cannot increase it. A smooth bounded detuning density near epsilon=0
further restricts the set with Omega small; it does not remove the void
penalty. The leading conclusion survives Coulomb polynomial prefactors
as a log-cubic asymptotic bound with subleading log-log corrections.

This gapless ensemble can have arbitrarily soft sites while all its
inverse-gap moments remain finite: exp[-b r^3] beats exp[s r/xi] times
any fixed power of r. At T=0, its small-field response therefore has

\[
 P_k(g)=\chi_k g-C_{3,k}g^3+o(g^3),\quad
 \chi_k=n_{\rm pair}\langle f_1d^2/J\rangle,\quad
 C_{3,k}={n_{\rm pair}\over2}\langle f_1d^4/J^3\rangle.
                                                        \tag{12}
\]

This assumes a field-independent captured f_1 and the symmetric TLS sector.
Dominated Taylor remainders follow from the finite inverse-gap moments.
It does not assert convergence of the full Taylor series. In particular
the g|g| cusp of the exact rational target is absent in this explicitly
gapless, log-cubic family. This is stronger than simply invoking a finite
individual gap, and remains a restriction on this family only.

For a rare region of size R in dimension D, with survival probability
exp[-a R^D] and tunneling action kappa R^p, the same change of variables gives

\[
 \rho_\Omega\ \propto\ {1\over\Omega}
 [\log(\Omega_0/\Omega)]^{D/p-1}
 \exp\{-a[\log(\Omega_0/\Omega)/\kappa]^{D/p}\}.
\]

A genuine power occurs when D=p. For example a volume variable v with
probability density exp[-a v], J=J_0 exp[-kappa v], and d=D_0 v^q has

\[
 w(\Delta)\ \propto\ \Delta^{\gamma-1}
 [\log(1/\Delta)]^{q(\gamma+1)},\quad \gamma=a/\kappa,
\]

up to normalization and subleading log-log factors. A loading factor
scaling as Delta^s changes the power to gamma+s-1. For bounded constant
dipoles, the target w~Delta would require gamma+s=2. Neither the original
action nor an unspecified word such as disorder fixes this ratio,
occupation exponent, logarithmic correction, or amplitude. A critical
volume-action ensemble is a different physical construction from the
Poisson two-center route above.

## 7. Contact phonons: a conditional relaxation mechanism

The same scalar contact gives a checkable bath prediction, conditional on
a real locally homogeneous, dilute condensed daughter bath. Its density
n_0 fixes c_s=sqrt(g_2 n_0/m); the Bogoliubov energy is
E_q=sqrt[epsilon_q(epsilon_q+2g_2 n_0)], epsilon_q=q^2/(2m).
Its density fluctuation amplitude is sqrt[n_0 epsilon_q/(V E_q)].

The original scalar also gravitates. Linearizing its GP-Poisson equations
about a formally homogeneous density instead gives
omega_q^2=c_s^2 q^2+q^4/(4m^2)-4 pi G rho_d, rho_d=m n_0.
An unrestricted homogeneous bath is therefore Jeans unstable in the
infrared. The phonon formulas here require a stable supported/finite patch
and a local window q_Jeans<<q<<healing_length^(-1) in which gravitational
corrections are small. In the sound regime q_Jeans is approximately
sqrt(4 pi G rho_d)/c_s. No full-model E->0 phonon continuum is asserted;
confinement produces its own discrete spectrum and mode overlaps.

This is not a new scalar-baryon coupling. Projecting the one scalar field
into a localized **number-isolated fragmented mode** and orthogonal bath
modes gives the retained density coupling gamma=2g_2, from the same
identical-boson cross term as (6). Negligible number-changing terms,
orthogonal-mode corrections, a stable bath and weak coupling must be
justified for an actual state. A coherent density deformation of one
condensate requires its full Bogoliubov Hessian instead; it must not
silently be treated as a separate distinguishable impurity with adjustable
coupling. Writing gamma below exposes this projection dependence rather
than adding a freely fitted microscopic parameter.

For occupied left/right packets separated by r_D in the bath frame,
the retained sigma_z bath coupling is

\[
 \lambda_{\boldsymbol q}=i\gamma\sqrt{n_0/V}
 \sqrt{\epsilon_q/E_q}\,F_D(q)\sin(\boldsymbol q\cdot\boldsymbol r_D/2).
\]

Here F_D(0)=1 is the actual normalized packet-density form factor.
In the total COM coordinates used in section 4, r_D=alpha r for a fixed
bath reference; another bath/host relative coordinate must be transformed
consistently. Recoil and local bath scattering can change coefficients;
the two equal-number packets still have zero difference at q=0.

Define J_B(E)=sum_q |lambda_q|^2 delta(E-E_q). In the phonon range,
angular integration gives

\[
 J_B(E)={\gamma^2n_0 E^3\over8\pi^2m c_s^5}
       |F_D(E/c_s)|^2
       [1-\operatorname{sinc}(E r_D/c_s)]
       \sim {\gamma^2n_0 r_D^2\over48\pi^2m c_s^7}E^5.
                                                        \tag{13}
\]

Density noise without the left/right subtraction instead starts as E^3.
The two extra powers come from resolving the dipole, not from a chosen
cutoff or a target occupation spectrum. This coefficient is derived here
with the explicit J_B convention. As a primary cross-check of the spatial
form factor and dimensional power, Cirone et al.,
[arXiv:0909.2166v2](https://arxiv.org/pdf/0909.2166), Eqs. (17), (28)-(30),
derive sin^2(q.L) suppression and the power D+2 for a D-dimensional
interacting condensate. Their atoms are different species in externally
controlled traps; that paper does not prove the same-species scalar
projection, baryon landscape, or formation assumptions here.

For a finite-gap TLS in a continuum thermal bath, weak-coupling Golden
Rule/Markov and secular assumptions give

\[
 \Gamma_\downarrow=2\pi(2J/\Omega)^2J_B(\Omega)[n_B(\Omega)+1],\quad
 \Gamma_\uparrow=2\pi(2J/\Omega)^2J_B(\Omega)n_B(\Omega),
\]

so Gamma_up/Gamma_down=exp[-beta Omega] and

\[
 p_e(t)={1\over1+e^{\beta\Omega}}+
 \left[p_e(0)-{1\over1+e^{\beta\Omega}}\right]
 e^{-(\Gamma_\uparrow+\Gamma_\downarrow)t}.              \tag{14}
\]

These rates describe internal equilibration conditional on a captured
particle; they are not attachment or detachment rates and cannot set
f_1. For an unbiased pair, the local phonon approximation gives
Gamma_rel~2 pi C_B Omega^5 at T=0 and
~4 pi C_B T Omega^4 when Omega/T<<1, within the stated stable phonon window.
A finite time therefore leaves the softest sites essentially in their
prepared states.
The continuum/Markov limits must be checked as Omega approaches a finite
patch's bath level spacing. At exactly J=0 the coupling is diagonal in
the localized basis and yields dephasing, not automatic population
thermalization; a bath spectral power alone proves no Gibbs attractor.

## 8. Normalization, checks and physical continuation

For fixed captured single sectors the actual source susceptibility is

\[
 \chi_k(T)=n_{\rm pair}\int p_{\rm pair}(r)dr\int du/2\,
 f_1(r,u){d(r,u;k)^2\over J(r)}\tanh[\beta J(r)].
\]

It depends on n_b, the actual baryon phase/selection, wavefunctions,
bound-level scale, inventory/loading, temperature, and probe k. For this
fixed-level Poisson control its inverse moments are finite, and (2) gives
chi_k~k^4 as k->0 with a finite coefficient. Tails at r~1/k are
super-exponentially suppressed in that limit. No uniform acceleration
dipole survives. The combination 4 pi G chi_k is not forced to one by
the gravitational occurrence of a_G or by the conditional bath rates.

The exact formulas were self-reviewed algebraically, and the bounded
finite checks in `run_004/results.json` cover: independent sphere-slice
union volume and pair normalization; Lambert-W inverse and finite-
difference Jacobian; fixed-binding Coulomb WKB action and direct generalized
eigenvalues for the two-1s LCAO gap; full three-mass
source versus its compact expression and small-k coefficient; direct
Bogoliubov radial/angular integral versus its E^5 coefficient; detailed
balance; and direct four-state Fock diagonalization versus (5) and (7).
They test the stated finite points and tolerances, not the physical
existence of the declared state or all asymptotic claims. See
`VERIFICATION.md` for exact commands, caps and provenance.

This route supplies a concrete new occupied-spectrum mechanism and its
failure points. A physical continuation should choose a real baryon
material phase with its center correlations and lifetime, solve its
source-complete few-body/localized modes, compute on-site/off-site
matrix elements and capture/exchange kinetics from the original scalar
state, and test whether a long-lived singly occupied sector actually
exists. A different rare-region route would have to derive its joint
rarity/action/occupation statistics and source budget before claiming a
Griffiths exponent or normalization. None of those inputs can be
replaced by selecting the target w.
