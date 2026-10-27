# Actual source-produced occupations and the missing dipole map

19 October 2026. Lane owner: `occupied_spectrum`. Base: `CE-GRAV-2026-10-19 /
CE087`, requested initial HEAD `f4424595259bd1ae40addb890e338f85c4f48eb1`.
The checkout changed concurrently; `source_pins.json` identifies the exact
source bytes and the observed later HEAD. This lane writes only here and
does not modify the parallel CE088 transport lane, manuscripts, queues,
current research records, or publication files.

**Result.** The canonical scalar vertex supplies a definite leading,
regulated source-to-pair coupling measure and, after a source preparation is
declared, an actual occupied pair-energy distribution. It does not supply a
population of local saturating gravitational dipoles. The generic occupied
threshold density is proportional to the square root of excess pair energy;
a source tuned exactly to its dressed threshold instead gives an inverse
square root. Neither is the required linear soft reduced-gap weight under a
constant-dipole identification. A formal inverse-square high-energy tail
exists for a particular uncut canonical source projection, but its first
energy moment diverges. A finite-energy source preparation or regulator
changes that endpoint. Bose thermalization can give a linear phonon
occupation spectrum in the infrared, with exponentially suppressed thermal
ultraviolet occupation; it still supplies neither the target tail nor local
two-level dipoles. Gravity normalization remains undetermined.

These are restrictions on explicit proposed identifications, not a theorem
that every state or collective phase of the full scalar action is excluded.

## 1. Contract, actual input state, and what must be derived

Use canonical complex fields with charges 1 and 2, masses `m` and `M>2m`,
and interaction `g(X* Phi^2 + c.c.)`. The repulsive matched threshold
coupling is `g2=lambda_rep/(2m^2)>0`, with

\[
 M=2m\sqrt{1+u_*^2},\qquad
 \lambda_{\rm tot}=\lambda_{\rm rep}
 +\frac{g^2}{M^2-4m^2}.
\]

The original action fixes a Hamiltonian after a regulator, matching, and
counterterm prescription are specified. It does not fix the initial state,
number of sources, volume, source momentum distribution, energy spread,
temperature, condensate fraction, or chemical potential. Different allowed
states of the same action have different occupation spectra.

The source/pair/contact Hamiltonian analyzed here is the **flat-space
production Hamiltonian without Newtonian gravitational pair binding**.
Neither its protected `2m` threshold nor its no-subthreshold-pole result
is a bound-state theorem for the full gravitating model. Including an
attractive gravitational pair potential changes the pair resolvent and
can produce ordinary gravitational levels below `2m`; their production
overlaps and continuum threshold behavior require a separate calculation.

The first route below specifies one resting positive-charge source and no
initial pairs, in a box of volume `V`, and retains its coupling to the
same-charge positive-frequency two-daughter continuum. This is a controlled
dilute, leading-vertex projection near the resonance. The free pair measure
is derived first; the retained NR quartic is then included exactly by its
rank-one resolvent below. Relativistic rescattering, antiparticle and higher
sectors, and the UV completion remain explicit limitations. The general
resolvent and preparation formulas also apply to a more complete pair
Hamiltonian with its induced coupling measure.

The target from the rational-completion lane is an *occupied dipole-magnitude
density*, in field units,

\[
 w(\Delta)=p_{\rm sat}\frac{a\Delta}{(a^2+\Delta^2)^{3/2}},\qquad
 \Delta=\frac{\Omega}{2d},\qquad
 w\sim\Delta\ (\mathrm{IR}),\quad w\sim\Delta^{-2}\ (\mathrm{UV}).
\]

Its isotropic-axis parent weight is

\[
 w_0(\Delta)=p_{\rm sat}
 \frac{a\Delta(4a^2+\Delta^2)}{(a^2+\Delta^2)^{5/2}}.
\]

Both require a real local source operator of magnitude `d`, independent
saturation, a gap `Omega`, and an occupied distribution. A count of available
continuum modes, a source width, or a density-response spectral function
alone supplies none of that dictionary. Success would establish this full
dictionary and both endpoints, rather than match one raw-energy exponent.

## 2. The vertex and phase space fix an off-shell distinction

Normalize a box source state `|s>=b_0^dagger|0>` and, for nonzero `p`, the
unordered pair `|p,-p>=a_p^dagger a_-p^dagger|0>`. Write
`omega_p=sqrt(m^2+p^2)`. The two contractions of the identical daughters give

\[
 v_{\bf p}=\frac{g}{\omega_p\sqrt{2MV}},\qquad
 E_{\bf p}=2\omega_p.
\]

The exceptional zero-momentum normalized pair has the usual square-root-of-two
factor; it has zero weight in the continuum integral. Counting unordered
pairs once gives

\[
\begin{split}
 J_H(E)&=\sum_{\{\bf p,-p\}}|v_{\bf p}|^2
                  \delta(E-2\omega_p)\\
 &=\frac{g^2}{4M}\int\frac{d^3p}{(2\pi)^3\omega_p^2}
                  \delta(E-2\omega_p)\\
 &=\boxed{\frac{g^2}{16\pi^2M}
             \sqrt{1-\frac{4m^2}{E^2}}}\,\theta(E-2m).
\end{split}
\]

The source factor is `1/sqrt(2M)`, because the one bare source basis vector
has fixed mass and normalization. Consequently

\[
 2\pi J_H(M)=\Gamma(M),\qquad
 2\pi J_H(E)=\frac E M\Gamma_{\rm vac}(E),\qquad
 \Gamma_{\rm vac}(E)=\frac{g^2}{8\pi E}
                  \sqrt{1-\frac{4m^2}{E^2}}.
\]

Inserting `Gamma_vac(E)/(2pi)` into the star Hamiltonian is a different
off-shell effective model. The earlier `DILUTE_UNITARY_DECAY.md` explicitly
declared precisely that continuation in a narrow resonant band. That was
adequate for its stated on-shell decay check, but does not derive far tails
of the original canonical source state. The distinction is negligible on
that old band and decisive if extrapolated to infinity.

For excess pair energy `epsilon=E-2m`,

\[
 J_H(2m+\epsilon)=A\sqrt\epsilon[1+O(\epsilon/m)],\qquad
 A=\frac{g^2}{16\pi^2M\sqrt m}.
\]

The factor `sqrt(epsilon)` is the full leading vertex times two-body phase
space, rather than an assumed Lorentzian or a bare density of states.

### Retaining the original NR quartic exactly

There is a stronger result than simply postponing contact rescattering. In
the regulated `Q=2`, zero-total-momentum NR sector, let `|F>` have component
`1/sqrt(V)` for each retained unordered nonzero pair (with the corresponding
normalized zero-mode factor). The leading positive-frequency Hamiltonian
from the pinned action has the exact block form

\[
 H_{\rm pair}=H_{\rm free}+U|F\rangle\langle F|,\quad
 H_{s,{\rm pair}}=\gamma\langle F|,\quad
 U=4k_c,\quad\gamma=2c_3,
\]

where `k_c=lambda_tot/(4m^2)` and `c3=g/(2m sqrt(2M))`. Use the same finite
contact regulator for both terms. With

\[
 L(z)=\langle F|(z-H_{\rm free})^{-1}|F\rangle,\qquad
 j_0(\epsilon)=-\pi^{-1}\operatorname{Im}L(\epsilon+i0),
\]

the rank-one resolvent identity gives

\[
 \boxed{\Sigma_{\rm contact}(z)
      =\gamma^2\frac{L(z)}{1-U L(z)}},\qquad
 \boxed{J_{\rm contact}(\epsilon)
      =\gamma^2\frac{j_0(\epsilon)}{|1-U L(\epsilon+i0)|^2}}.
\]

In the continuum limit of this regulated three-dimensional model,
`j0(epsilon)=m^(3/2) sqrt(epsilon)/(8pi^2)` at small positive energy. Since
`L0=L(0)<0` is finite and `U>0`, the denominator is nonzero; contact therefore
changes the coefficient but preserves the square-root threshold. The
source's dressed threshold detuning is

\[
 \nu=\delta+\frac{\gamma^2L_0}{1-U L_0}
 =\frac{\delta+(\gamma^2-\delta U)L_0}{1-U L_0}.
\]

Here `delta` is the detuning coefficient specified in this retained
Hamiltonian, rather than a dressed pole location after new counterterms.
The action's regulated positivity inequality
`k_c-c3^2/delta>0` implies `U>gamma^2/delta`, and hence **`nu>0` for finite
`delta>0`**. Thus this displayed flat-space NR source/pair/contact
Hamiltonian does not reach the critical threshold or produce a bound state
below its protected `2m` energy threshold by changing the source population.
The conclusion explicitly excludes gravitational pair binding and does
not apply to the full gravitating Hamiltonian. This is an exact
finite-regulator NR statement; the numerical critical/subthreshold models
below are independent diagnostic controls, not claims of physical states
of this positive Hamiltonian. New mass counterterms or full relativistic
loop matching can change the relation between its coefficients and a
physical pole and require a separate analysis. The finite contact matching correction used
to express the physical low-energy coupling as `g2=lambda_rep/(2m^2)` does
not authorize discarding the repulsive contact or the conserved energy.

In an exact finite box, the continuum densities are discrete measures; the
displayed threshold powers concern the thermodynamic continuum limit with
the regulator held fixed. The rank-one resolvent identity itself is valid
already for the finite matrix. If the exact zero-momentum pair is retained,
`L(0-)=-infinity` in that finite box; use the resolvent's limiting ratio,
which gives `nu=delta-gamma^2/U>0`. The finite `L0` used for the continuum
threshold density is obtained after the thermodynamic limit. In both
orders the no-zero-threshold conclusion for this nongravitating block
follows from `U delta>gamma^2`.

For the requested benchmark, the bounded run finds

\[
\begin{array}{ll}
m=10^6\ {\rm eV},&g=2168\ {\rm eV},\\
M=2000399.960008\ {\rm eV},&\delta=M-2m=399.960008\ {\rm eV},\\
\Gamma=0.00186941194\ {\rm eV},&\Gamma/\delta=4.67399716\times10^{-6},\\
A=1.48792825\times10^{-5}\sqrt{\rm eV},
 &(\pi A)^2=2.18506181\times10^{-9}\ {\rm eV}.
\end{array}
\]

This source lies hundreds of eV above threshold and is very narrow. Width
does not populate all cold energies with a target-shaped broad spectrum.

## 3. Occupation follows the source's spectral measure and preparation

At a finite regulator, use excess energies and a real cutoff form factor:

\[
 H=\epsilon_b|s\rangle\langle s|
 +\int_0^\infty \epsilon|\epsilon\rangle\langle\epsilon|d\epsilon
 +\int_0^\infty\sqrt{J(\epsilon)}
    (|s\rangle\langle\epsilon|+|\epsilon\rangle\langle s|)d\epsilon.
\]

All basis states have charge two. `epsilon_b` is the *bare excess energy in
this regulated model*; it need not equal the dressed resonance detuning.
Solving the block resolvent directly gives

\[
 G_s(z)=\frac1{z-\epsilon_b-\Sigma(z)},\qquad
 \Sigma(z)=\int_0^\infty\frac{J(x)}{z-x}\,dx,
\]
\[
 \boxed{\rho_s(\epsilon)=
 \frac{J(\epsilon)}{
 [\epsilon-\epsilon_b-\operatorname{PV}\Sigma(\epsilon)]^2
       +\pi^2J(\epsilon)^2}}.
\]

Bound poles must be added to the spectral measure separately. Without a
bound component, the initial `|s>` has survival amplitude
`a(t)=integral rho_s(epsilon) exp(-i epsilon t) d epsilon`. This identity is
used to derive occupation, not to repeat the prior decay-probability test.
The pair amplitude solves exactly

\[
 c_\epsilon(t)=-i\sqrt{J(\epsilon)}e^{-i\epsilon t}
            \int_0^t a(t')e^{i\epsilon t'}dt'.
\]

For a sufficiently regular absolutely continuous spectrum and no bound
state, the outgoing amplitude is
`sqrt(J(epsilon)) G_s(epsilon+i0) exp(-i epsilon t)`. Its squared magnitude
therefore is exactly

\[
 \boxed{\frac{dP_{\rm outgoing\ pair}}{d\epsilon}=\rho_s(\epsilon)}.
\]

This is an **actual occupation distribution for the declared preparation**,
not a continuum DOS. If there are bound poles, their coherent persistent
source/pair cloud is not a freely outgoing daughter inventory. The continuum
formula accounts only for the initial state's absolutely continuous weight.

The width is generated by `Im Sigma=-pi J` in this Hermitian model; no
independent imaginary damping is inserted. Counting real `X <-> Phi Phi`
conversion and also adding the same real intermediate state as an
independent resonant pair collision would double count this process.

For `N_X` independently prepared sources, the dilute expectation is
`dN_pair/d epsilon=N_X rho_s(epsilon)`, and `dN_Phi/d epsilon=2N_X rho_s`.
The overall factor `N_X/V` is an input source density. For an isotropic
source-at-rest ensemble, in a box-normalized occupation convention,

\[
 f_\Phi(p)=\frac{16\pi^2 n_X}{pE}\rho_s(E-2m),\qquad
 E=2\sqrt{m^2+p^2},
\]

so that `integral d^3p/(2pi)^3 f_Phi = 2 n_X` when the continuum probability
is one. Partners remain correlated; this one-particle expectation does not
turn them into independent two-level sites.

A different physical preparation changes the distribution. For
`|psi_F>=F(H)|s>/||F(H)|s>||`, its spectral measure and outgoing energy
profile are proportional to `|F(epsilon)|^2 rho_s(epsilon)` (including any
bound measure in the normalization). An external production reaction fixes
its incoming energy and preparation envelope. A linewidth is not permission
to violate that reaction's exact energy conservation. A sufficiently narrow
prepared energy profile approaches the usual cold two-body shell, rather
than a broad universal gap inventory.

The regular resolvent model and its singular-coupling qualifications have
an independently checked primary reference: Facchi, Ligabo, and Lonigro,
[arXiv:1910.05957v2](https://arxiv.org/pdf/1910.05957v2), Eqs. (11)-(12),
Theorem 3.2, and Remark 3.3. Our occupation and normalization formulas above
are obtained directly from the displayed project Hamiltonian.

## 4. An exactly integrable threshold and bound-state control

Choose the explicit NR regulator

\[
 J(\epsilon)=\frac{A\sqrt\epsilon}{(1+\epsilon/\Lambda)^2},\qquad
 C=\frac{\pi A\sqrt\Lambda}{2}.
\]

This is a declared control model. It does not assert that the original
action chooses this form factor. Substitution `epsilon=Lambda t^2` and an
elementary rational integral give, with the branch continued from `z<0`,

\[
 \boxed{\Sigma(z)=-\frac C{(1+\sqrt{-z/\Lambda})^2}},\qquad
 \Sigma(0)=-C.
\]

The real boundary value at positive `epsilon` is

\[
 \operatorname{Re}\Sigma(\epsilon+i0)
   =-C\frac{1-\epsilon/\Lambda}{(1+\epsilon/\Lambda)^2},
 \quad\operatorname{Im}\Sigma=-\pi J.
\]

Define the dressed threshold detuning `nu=epsilon_b+Sigma(0)=epsilon_b-C`.
Then the real denominator is

\[
 D(\epsilon)=\epsilon-\nu
 -C\frac{(\epsilon/\Lambda)(3+\epsilon/\Lambda)}
 {(1+\epsilon/\Lambda)^2}.
\]

For `nu != 0`,

\[
 \rho_s(\epsilon)\sim\frac A{\nu^2}\sqrt\epsilon.
\]

At the tuned critical point `nu=0`, the term `pi^2 A^2 epsilon` dominates
the squared real denominator as `epsilon -> 0`, hence

\[
 \rho_s(\epsilon)\sim\frac1{\pi^2A}\epsilon^{-1/2}.
\]

The critical soft density remains integrable. The formal root at threshold
has zero pole residue and is not a normalizable bound state: its continuum
norm would contain `integral J(epsilon)/epsilon^2 d epsilon`, which diverges.
It does not yield the target's linear occupied soft weight. The same
threshold exponents hold for smooth short-range modifications preserving
`J ~ A sqrt(epsilon)`, absent an additional zero or singularity of the
effective vertex. Tuning an additional zero-energy two-body resonance is
a different hypothesis and must be analyzed using the interacting pair
Hamiltonian, rather than silently inserted here.

For `nu<0`, there is a unique bound energy `z_b=-Lambda kappa^2<0`, satisfying

\[
 -\Lambda\kappa^2-\nu-C+\frac C{(1+\kappa)^2}=0,
 \qquad
 Z_b=\left[1+\frac C{\Lambda\kappa(1+\kappa)^3}\right]^{-1}.
\]

Monotonicity follows from `1-Sigma'(z)>0` below the continuum. The control
run checked the continuum plus pole sum rules

\[
 Z_b+\int\rho_s=1,\qquad
 Z_bz_b+\int\epsilon\rho_s=\epsilon_b,\qquad
 Z_bz_b^2+\int\epsilon^2\rho_s=\epsilon_b^2+C\Lambda.
\]

For `A=.03, Lambda=1`, the three declared cases `nu=.2,0,-.04` give
threshold slopes `0.500000014,-0.500000174,0.499999891`. The negative-detuning
case has `z_b=-.0275401788`, `Z_b=.848068955`; only `.151931045` belongs to
the continuous outgoing component. These are finite numerical checks of
the formulas and sum rules, not a physical benchmark fit.

The source must be tuned to its *renormalized threshold*, not merely have
small bare `M-2m`. The crossover scale of the critical asymptotic is
`epsilon ~ (pi A)^2`, about `2.19e-9 eV` for the benchmark's fixed coupling.
Neither this tuning nor this asymptotic is realized by its `delta~400 eV`.

There is also a coupling-limit obstruction to an unqualified `delta -> 0`
continuation of the original matched action. At fixed `g`,
`lambda_min ~ g^2/(4m delta)` diverges, so the perturbative dilute control
eventually fails. Holding `lambda_min` finite instead forces `g^2=O(delta)`,
`A=O(delta)`, and `Gamma/delta=O(sqrt(delta/m)) -> 0`. The limiting source
decouples. The mathematical fixed-`A` critical Friedrichs control is not
automatically a physical critical path of that matched scalar action.

## 5. The tempting inverse-square tail and its energy cost

In the controlled NR intermediate range
`delta, (pi A)^2 << epsilon << m, Lambda`, with a weak self-energy slope
`A/sqrt(Lambda)<<1`, the occupation is

\[
 \rho_s(\epsilon)\sim A\epsilon^{-3/2}.
\]

If one *formally* extends the canonical relativistic one-source/two-particle
projection beyond its controlled range without a form factor,
`J_H(E) -> g^2/(16pi^2 M)`. After the required mass subtraction its
self-energy grows logarithmically, and

\[
 \rho_s(E)\sim\frac{g^2}{16\pi^2M E^2}.
\]

Thus a formal inverse-square occupied energy tail does arise after the
full phase-space and vertex factors are included. It is not an exact target
distribution: its threshold is different, it is only an energy distribution,
and the approximation has left the NR, two-particle and weak-dressing domain.
In particular `integral E rho_s(E) dE` diverges logarithmically for that
uncut initial bare state. A finite resonance mass after counterterms does
not make this chosen vector a finite-energy preparation. This is precisely
the sort of domain issue identified for singular couplings in Remark 3.3
of the cited Friedrichs-Lee paper.

Using the old off-shell prescription `J=Gamma_vac(E)/(2pi)` instead gives
`J~1/E` and a formal `rho_s~E^-3` tail. Neither prescription should be
confused with an invariant-mass spectral density of a covariant propagator,
or with the state prepared by a particular smeared field operator. Those
objects have additional Jacobian, normalization and preparation factors.
An on-shell width alone selects none of these off-shell occupation measures.

At a finite regulator, an outgoing state with finite mean energy must obey
the corresponding conserved first-moment budget. For the regulated flat-space
NR initial state of `N_X` resting sources and no daughters, with Newtonian
gravitational binding omitted, the excess
energy is `delta N_X`; the source number and this energy are external input.
In the subtracted control model it is `epsilon_b N_X`; substituting the
physical resonance detuning for `epsilon_b` would violate that model's
sum rule. For a separately specified finite-energy physical preparation,
use its actual first moment, including binding and any other sector.

A useful stronger conditional test is independent of a chosen constant
dipole size. Suppose each emitted pair is identified with one local object
whose gap equals its nonnegative pair excess energy,
`Omega=epsilon=2d Delta`. If `n(d,Delta)` is its number density, then

\[
 w(\Delta)=\int d\,n(d,\Delta)\,dd,
 \qquad
 U_{\rm gap}=\int\Omega n\,dd\,d\Delta
            =2\int_0^\infty\Delta w(\Delta)d\Delta.
\]

For the required spectrum, a cutoff `L` gives

\[
 \int_0^L\Delta w(\Delta)d\Delta
 =p_{\rm sat}a\left[
 \operatorname{arsinh}(L/a)
 -\frac L{\sqrt{a^2+L^2}}\right]
 \sim p_{\rm sat}a[\log(2L/a)-1].
\]

It diverges for both the aligned and isotropic-axis target spectra. Therefore
**no finite source excess-energy budget can produce the exact target
inventory by identifying each gap with an emitted pair's excess energy**,
even if its dipole size varies. A finite cutoff can give only a finite
interpolation window, with a logarithmically increasing energy requirement.

This does *not* exclude a ground-state ensemble of supported internal
two-level objects with large excitation gaps. A gap is then a possible
excitation cost and need not already have been paid in preparing the ground
state. Such an interpretation avoids this particular energy argument, but
requires the presently missing local objects, their internal Hamiltonian,
and a mechanism preparing their inventory. The scalar pair continuum is
not that construction.

## 6. Rabi gaps, probe spectra, and reduced dipole gaps are different

An isolated source plus one pair mode has the avoided-crossing splitting

\[
 \Omega_j=\sqrt{(\epsilon_b-\epsilon_j)^2+4|v_j|^2}.
\]

The continuum star is not a product of these two-level systems: every mode
shares the *same* source state. Treating every crossing as an independently
occupied saturator multiplies the source inventory without authorization.
The individual `v_j` scales as `V^-1/2` or as the square root of an energy
bin width and goes to zero in the continuum limit; those avoided gaps are
not an intrinsic volume-independent distribution of local splittings.
If one instead maps `Omega=|E-M|` by fiat, the resonance is an interior
point where `rho_s` is finite and nonzero, so its folded soft density is
constant, not linear. Taking `Omega=E` for free outgoing pairs gives a hard
lower threshold `2m`.
Taking `Omega=E-2m` gives the threshold exponents above. None of these choices
derives `d` or a local mass-dipole source.

Probe matrix elements add another independent factor. In a stationary
state with energy populations `p_n`, a linear response contains

\[
 \chi_{DD}(\omega)=\sum_{n,m}
 \frac{(p_n-p_m)|D_{nm}|^2}{\omega+E_n-E_m+i0}
\]

up to the declared response-sign convention. It is a population-difference
and transition-matrix-element spectrum, not the positive inventory `w`.
At zero spatial momentum the leading NR gravitational mass is `mQ`, which
commutes with the Hamiltonian and is `2m` times the identity in this sector.
Its off-diagonal matrix elements vanish exactly. Coupling to source number
alone would be a different operator. Finite-momentum density probes involve
recoil and spatial form factors; they do not create independent local mass
dipoles or an acceleration-conjugate operator automatically.

## 7. Actual Bose occupations: what thermalization could and cannot fix

If elastic collisions thermalize the positive-charge daughters while their
number is approximately conserved, a free NR gas has

\[
 f(p)=\frac1{e^{(p^2/2m-\mu_{\rm NR})/T}-1},\qquad\mu_{\rm NR}\leq0,
\]
\[
 \frac{dn}{de}=\frac{(2m)^{3/2}}{4\pi^2}
           \frac{\sqrt e}{e^{(e-\mu_{\rm NR})/T}-1}.
\]

For `mu_NR<0` its occupied infrared density scales as `sqrt(e)`; at the
condensation boundary `mu_NR=0` it scales as `T/sqrt(e)`. The condensed
number is an additional delta function at zero momentum. Thermal UV
occupation is exponentially small, rather than the required power law.
For a nondegenerate ideal final gas with `N_Phi=2N_X` and no other energy
reservoir, `3 N_Phi T/2=delta N_X`, so `T=delta/3`. Degeneracy, interactions,
expansion, source recoil or number-changing reactions alter that relation.
No thermalization or temperature is asserted by this conditional calculation.

A genuinely gapless interacting condensate permits a more interesting
*actual occupied* infrared spectrum. Put

\[
 \eta=g_2n_0=mc_s^2>0,\quad e_k=k^2/(2m),\quad
 \Omega_k=\sqrt{e_k(e_k+2\eta)},\quad
 n_B(\Omega)=\frac1{e^{\Omega/T}-1}.
\]

With `r=sqrt(eta^2+Omega^2)`, `e_k=r-eta`, the exact Bogoliubov DOS is

\[
 D(\Omega)=\frac{mk\Omega}{2\pi^2r},\qquad
 \frac{dn_{\rm qp}}{d\Omega}=D(\Omega)n_B(\Omega).
\]

Since `k~Omega/c_s`, the *thermally occupied quasiparticle count* obeys

\[
 \frac{dn_{\rm qp}}{d\Omega}
 \sim\frac{T\Omega}{2\pi^2c_s^3}\quad(\Omega\to0).
\]

This is a real population effect: three-dimensional phonon DOS times Bose
enhancement. It is stronger than merely observing an unoccupied mode
density or a vacuum PSD. At `T=0` the quasiparticle population is zero.
At high excitation energy its thermal tail is exponentially suppressed.
Even a hypothetical constant `d` would therefore match only the requested
infrared exponent, not the ultraviolet target or the full function.

The atom/daughter momentum population is a different quantity:

\[
 n_k=v_k^2+\frac{e_k+\eta}{\Omega_k}n_B(\Omega_k),\qquad
 v_k^2=\frac{e_k+\eta-\Omega_k}{2\Omega_k}.
\]

Quantum depletion is an actual noncondensed atom population, although it is
not a quasiparticle excitation population. In raw `Omega` units,
`D v^2 ~ Omega` at small `Omega` and `~ Omega^-3/2` at large `Omega` in the
NR contact regime. At nonzero `T`, the thermally depleted atom spectrum
`D (e_k+eta)n_B/Omega` tends to a constant in the infrared. Thus atom count,
quasiparticle count and a vacuum density-response PSD are not interchangeable.
The Bogoliubov population formulas and the distinction between the two
depletions were checked in the primary paper by Chang et al.,
[arXiv:1608.04693v2](https://arxiv.org/pdf/1608.04693v2), Eqs. (2), (3), (5).
The energy-variable exponents here follow from the displayed Jacobian.

Bogoliubov excitations are oscillators with unbounded occupation, not local
two-level systems with saturation. Density response has its own vertex
`sqrt(n0 e_k/Omega_k)` and Bose factors; it cannot be replaced by the above
counts. The state must establish a condensate, density, approximate
equilibration and `T` before even these conditional spectra apply. In a
charge-symmetric chemically equilibrated relativistic phase, the full
charge chemical potentials and number-changing reactions must instead be
included; the earlier thermal/charge-kinetics note explicitly leaves their
physical equilibration unresolved.

## 8. Verification, status, and continuation

`run_002/manifest.json` is a valid v2 evidence record with status `completed`;
all **42** deterministic checks pass. They test canonical vertex/phase-space
normalization, the off-shell `E/M` factor, the exact smooth-regulator
self-energy against independent negative-energy quadrature, three spectral
moments including the subthreshold pole, threshold and tail exponents,
actual free/Bogoliubov occupations, and the cutoff target first moment.
The mathematical interpretation is conditional on the explicitly declared
projection, regulator and state. It does not establish physical dipoles.

The completed run took under one second on the available host. It used
30-second wall, 20-second per-process CPU, 1-MiB combined-log and one-thread
caps. macOS refused the requested CPU-affinity cap before launch. The
subsequent `run_001` records `launch-failed` in `preexec_fn` with a requested
1-GiB address-space cap; no scientific output was produced. `run_002`
succeeded without the address-space/affinity caps. The finite arrays and
quadratures are small; no heavy computation or live external job remains.
The script was amended to accept the fresh run directory after the failed
launch, so `run_001` is a historical failed launch record, not current
validated mathematical evidence.

Reproduce and validate using `REPRODUCE.md`. Source checks and computation
review here are self-review. The coordinator independently confirmed the
canonical vertex, off-shell measure, daughter momentum occupation,
conditional energy-budget argument, and the contact Schur/positivity
derivation; see `INDEPENDENT_REVIEW.md` for its exact scope. Primary-source
authentication/extraction records are in `SOURCE_CHECKS.md`; no PDFs or
full-text source copies were added to the repository.

The original goal is **not reached**: no occupied local dipole distribution
or gravity normalization has been derived. The surviving constructive
results are the occupied source spectral measure, the exact retained-NR
contact correction, the regulated threshold continuation, and the
conditional thermal phonon infrared inventory. Their next missing arrows are:

1. **Physical dipole map:** derive a local gravity source `D`, two-level
   saturation and `d` from a supported scalar state. Without this, every
   conversion from pair energy to reduced gap is conditional.
2. **Prepared source state:** derive an incoming energy envelope and source
   density from a specified production process; then its outgoing occupation
   follows from the spectral measure. This remains open, rather than
   replacing it with a chosen broad line shape.
3. **Full matched pair continuum:** the retained NR rank-one contact is
   resolved above. Include relativistic momentum dependence, loop matching,
   regulator removal and higher sectors if a UV or critical prediction is
   required. If gravitational binding is retained, also include its pair
   potential, bound-state production overlaps and changed continuum
   resolvent; the flat-space positivity statement cannot exclude those
   bound states. None of these corrections establishes local sites by itself.
4. **Thermal collective route:** if another lane supplies real local
   saturators in a condensate, evaluate their *occupied reduced-gap* weight
   with their actual matrix elements and energy budget. A Bose phonon
   exponent alone does not justify a thermal UV power tail.
5. **Finite-window possibility:** any emitted-energy/gap identification must
   specify a UV cutoff and pay the displayed logarithmic gap-energy moment;
   compare to the actual source budget before fitting the rational window.

These continuations are deferred to the parent physical-dipole and state
selection obligations; the source-energy route does not close the general
scalar action's collective-state possibilities. There is no basis here for
fixing `p_sat=a/(4pi G)`, `a0`, `G`, a cosmological abundance, or a vacuum
exchange rate.
