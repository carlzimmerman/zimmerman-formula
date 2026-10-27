# Existing phases change susceptibility, but do not derive the tether switch

20 October 2026. Assessment base
`ff7df583f7d6d3a8a60d0c9cbb8c602302d28653`. This lane writes only its new
`phases/` directory. Actual working source bytes, including untracked
notes, are pinned in `source_hashes.json`. No old packet, source, campaign,
production job, publication or Git state is changed.

**Normalized target and verdict: incomplete, with the physical
field-to-polarization map missing.** The original scalar action has a
genuine condensate state and a gapless charge phase. Deriving that phase
instead of discarding it still gives an ordinary longitudinal density
response, not the critical material polarization action. In the actual
homogeneous retained-source zero-temperature mean-field model, the stable
occupied branch is unique and joins the vacuum continuously; it does not
supply two equilibrium response states at the same controls. A separately
derived local-charge spectral-moment identity holds regardless of whether
the state is condensed. It prevents an exact disappearance of the *whole
cold density response* in a nonempty passive state in its continuum regime.
That identity alone does not forbid switching an additional, separately
identified response while ordinary gravitational response remains.

## 1. Raw action, conventions and actual comparison

The positive-charge retained-source NR Hamiltonian is

\[
 H=mQ+\int\left[{|\nabla\psi|^2\over2m}
 +{|\nabla b|^2\over2M}+\delta|b|^2
 +c(b^*\psi^2+b\psi^{*2})+k|\psi|^4\right]d^3x,
 \quad Q=\int(|\psi|^2+2|b|^2).
                                                               \tag{1}
\]

Natural units apply unless `hbar` is displayed in the commutator identity.
Here `delta=M-2m>0`, `c=c3`, and `k` may be the stated positive-frequency
`kc` or the separately threshold-matched `kR`. They are not interchanged:
the former obeys the original stronger remainder, while the latter obeys
`kR-c3^2/delta=lambda_rep/(4m^2)>0`. Both satisfy the hypothesis used here,

\[
 k>0,\qquad k\delta>c^2>0.                           \tag{2}
\]

This is the original `Phi,X` action, not the separate attractive `Psi,chi`
host and not the independent nodal-ring fermion medium. Gravity is first
an external weak probe with the leading cold source `rho_Q=m(n_a+2n_b)`.
Actual relativistic energy density contains additional detuning, stress,
gradient and interaction energy. No exact relativistic stress-response
sum rule is asserted by replacing it with `rho_Q`.

Dependency graph: (1)-(2) -> exact homogeneous mean-field grand functional
-> unique stable branch -> its common Goldstone action -> longitudinal
density response. Independently, local charge conservation plus the
kinetic term -> spectral moment. A proposed canonical `P` identification,
its critical restoring coefficient and response selector remain separate
obligations. Ordinary scalar susceptibility is not silently called the
extra canonical force.

## 2. Exact homogeneous mean-field branch and absence of its hysteresis

Let `mu` be the chemical potential per unit of `Q` above `m`, and put
`n=|psi|^2>=0`, `Delta=delta-2mu`. The homogeneous grand-energy density is

\[
 \mathcal G=-\mu n+\Delta|b|^2
      +2c\operatorname{Re}(b^*\psi^2)+kn^2.
\]

For `Delta>0`, completing the source square gives exactly

\[
 \mathcal G=\Delta\left|b+{c\psi^2\over\Delta}\right|^2
       -\mu n+\kappa(\mu)n^2,
 \qquad \kappa(\mu)=k-{c^2\over\delta-2\mu}.          \tag{3}
\]

Define the positive value

\[
 \mu_*={1\over2}\left(\delta-{c^2\over k}\right)>0.
\]

The complete classification for this homogeneous classical functional is:

| Range | Minimum/behavior |
|---|---|
| `mu<=0` | Unique amplitudes `n=b=0`; at `mu=0` the positive quartic still gives the vacuum minimum |
| `0<mu<mu_*` | Unique nonzero amplitude minimum `n=mu/(2 kappa)`, `b=-c psi^2/Delta` |
| `mu=mu_*` | Along the completed square, `G=-mu_* n` is unbounded below as `n` grows |
| `mu_*<mu<delta/2` | Negative `kappa` makes the same grand functional unbounded below |
| `mu>=delta/2` | The source quadratic is nonpositive; at equality the conversion term already makes the functional unbounded when `psi!=0` |

The broken common `U(1)` phase is degenerate on the occupied branch; the
statement of uniqueness concerns amplitudes and density, not that phase.
An unbounded grand functional is not a second stable phase. It marks the
end of this admitted grand-canonical truncation, which may also lose its
physical NR/dilute validity earlier. This does not assert instability of
every fixed-charge state or of the full relativistic theory.

The charge density on the unique occupied branch is

\[
 q=n+{2c^2n^2\over\Delta^2}.
\]

Because `kappa'=-2c^2/Delta^2<0`,

\[
 n'={\kappa-\mu\kappa'\over2\kappa^2}>0,\qquad
 q_\mu=n'\left(1+{4c^2n\over\Delta^2}\right)
           +{8c^2n^2\over\Delta^3}>0.                \tag{4}
\]

Moreover `q` tends to zero at `mu->0+` and to infinity at `mu->mu_*^-`.
Thus every positive uniform charge density has one amplitude branch in
this mean-field model. It has no two stable homogeneous amplitude states
at the same chemical potential or fixed charge density. In particular
there is no equilibrium hysteretic response bit in this branch.

The fixed-charge statement can also be checked directly without inferring
local stability from grand-canonical boundedness. For fixed `q>0`,
minimize the relative phase and set `|b|^2=(q-n)/2`, `0<=n<=q`. The
remaining energy density is

\[
 e_q(n)={\delta(q-n)\over2}
          -\sqrt2 c\,n\sqrt{q-n}+kn^2,
 \qquad
 e_q''(n)=2k+{\sqrt2 c(4q-3n)\over4(q-n)^{3/2}}>0.
                                                               \tag{4a}
\]

Its derivative is negative at `n=0` and tends to positive infinity as
`n->q^-`, so its unique stationary point is its unique minimum. The
opposite relative phase is unstable in that phase direction. Thus no
second locally stable homogeneous amplitude minimum is hidden by the
grand-canonical classification, within this classical truncation.

A weak host potential shifts the local chemical potential. In the
leading `mQ` gravity convention it is `mu_loc=mu-m Phi_N`; a local-density
approximation replaces `mu` by this value only where gradients and host
variation admit that approximation. In the further dilute limit,
`n0=[mu_loc/g2]_+`. This is a density/chemical-potential condition, not the
sign of one particle's orbital binding energy. A normal released stock
is not the empty vacuum merely because it has no condensate. If the
detuning correction to the source gravitational mass is retained, use
its actual `M Phi_N` term and rederive the local equations; it is not
exactly the same common shift.

Finite-temperature phases, vortices, finite-host order and strongly
nonuniform many-body states are not classified by (3). No universal
statement that all memories or phase transitions are impossible follows.

## 3. Keep the gapless common phase rather than integrating it away

On the stable coherent branch, write the slow common phase as
`psi=sqrt(n_a) exp(i theta)` and
`b=-sqrt(n_b) exp(2i theta)`. The cubic locks their relative phase.
The canonical one-form is `-q dot theta`. The spatial phase energy is

\[
 {C_\theta\over2}|\nabla\theta|^2,
 \qquad C_\theta={n_a\over m}+{4n_b\over M}>0.
\]

At frequencies and momenta below the retained relative/amplitude modes,
the actual leading hydrodynamic quadratic action is

\[
 \mathcal L_2=-\delta q\,\dot\theta
    -{(\delta q)^2\over2q_\mu}
    -{C_\theta\over2}|\nabla\theta|^2
    -m\Phi_N\delta q+\text{higher gradients}.          \tag{5}
\]

Its two Euler equations are
`dot delta q+C_theta nabla^2 theta=0` and
`dot theta=-delta q/q_mu-m Phi_N`. For Fourier frequency `omega`,

\[
 \delta\rho_Q=-\chi_\rho\Phi_N,\qquad
 \boxed{\chi_\rho(k,\omega)=
 {m^2C_\theta k^2\over
   (C_\theta/q_\mu)k^2-(\omega+i0)^2+O(k^4)}.}       \tag{6}
\]

The common Goldstone mode has
`c_s^2=C_theta/q_mu>0`, and the static long-wavelength susceptibility is
`m^2 q_mu>0`. The `O(k^4)` denotes the consistently retained positive
gradient corrections in the dilute scalar regime, not an all-momentum
error theorem for every dense branch. The higher relative mode cannot
be eliminated at its gap or near a singular branch.

For the dilute daughter limit this reproduces, with quantum pressure,

\[
 \chi_\rho(k,\omega)=
 {\rho_0 k^2\over c_s^2k^2+k^4/(4m^2)-(\omega+i0)^2},
 \qquad c_s^2={g_2n_0\over m}.                       \tag{7}
\]

The order of limits matters: at fixed nonzero `omega`, `k->0` gives zero
because the total charge is conserved; `omega->0` first instead gives
the positive compressibility. Neither limit means that release disabled
the microscopic coupling. Taking the density to zero at fixed nonzero
`k` removes the medium, while taking `k->0` first can retain the finite
one-sided vacuum-edge compressibility. Those limits also cannot be
called a finite-density switch.

Define only the longitudinal density displacement by
`div P_L=m delta q` and `j_Q=-dot P_L`. Eliminating the longitudinal phase
in (5) gives the actual matter action

\[
 \mathcal L_{P_L}={|\dot P_L|^2\over2m^2C_\theta}
    -{(\nabla\cdot P_L)^2\over2m^2q_\mu}
    +\nabla\Phi_N\cdot P_L+\text{higher derivatives}.
                                                               \tag{8}
\]

This gives a spatial restoring kernel proportional to `k^2`, not the
critical local `+K|P|^2/2` matter energy, and supplies neither a new local
transverse polarization field nor the required `|P|^3` remainder. The
inverse-divergence definition of `P_L` is nonlocal. The static mismatch
was identified earlier; (5)-(8) now test the actual gapless continuation
instead of appealing only to a finite-amplitude-gap expansion.

Restoring ordinary self-gravity contributes the negative longitudinal
energy `-K|P_L|^2/2`, `K=4piG`, rather than the missing positive tether.
In the dilute branch it gives the Jeans dispersion already recorded in
the source. The response formulas require a supported finite patch or
stable modes if self-gravity is retained. A Jeans pole is not an off
state or a stable material-polarization law.

## 4. A state-independent local-charge spectral moment

The following check is not restricted to mean-field condensates. Define
the leading cold-source Fourier operator

\[
 \rho_k=m\int e^{-ik\cdot x}
          (\psi^\dagger\psi+2b^\dagger b)\,d^3x.
\]

Every local interaction in (1) commutes with this local charge density:
`b^dagger psi^2` creates charge two and removes charge two at the same
point. Its commutator is `2-2=0`. The detuning, contact and a prescribed
local gravity potential commute as well. In the continuum quadratic-
kinetic convention, the double commutator is consequently

\[
 \boxed{\langle[\rho_{-k},[H,\rho_k]]\rangle
 =\hbar^2 k^2m^2\left({\langle N_a\rangle\over m}
                     +{4\langle N_b\rangle\over M}\right).}
                                                               \tag{9}
\]

One can verify it on each one-particle kinetic operator:
`[exp(ikx),[p^2/(2m_s),exp(-ikx)]]=hbar^2 k^2/m_s`.
The local conversion commutator is essential: using only daughter density
would incorrectly drop its nonzero reaction term. `M` need not be
artificially set equal to `2m` for (9); the probe is `mQ`. At `M=2m` its
right side is `hbar^2 k^2<mQ>`; the physical detuning gives the displayed
small cold-mass correction instead.

### Regulator statement

A hard momentum cutoff does not preserve the pointwise field algebra
used to discard local-interaction commutators. Equation (9) must not be
called exact for an unspecified such cutoff. A fully finite check uses
a common periodic spatial lattice of spacing `ell` with on-site cubic
and quartic terms. Put

\[
 T_s=t_s\sum_{\langle xy\rangle}
 (c_{s,x}^\dagger-c_{s,y}^\dagger)(c_{s,x}-c_{s,y}),
 \quad t_s={\hbar^2\over2m_s\ell^2},\quad
 w_a=m,\quad w_b=2m.
\]

The exact finite-lattice counterpart is

\[
 D_{\rm lat}(k)=\sum_{s,\langle xy\rangle}
 t_sw_s^2|e^{-ikx}-e^{-iky}|^2
 \langle c_{s,x}^\dagger c_{s,y}+c_{s,y}^\dagger c_{s,x}\rangle.
                                                               \tag{10}
\]

The on-site interaction commutators vanish exactly. In a homogeneous
continuum low-momentum regime, (10) tends to (9); equivalently each bond
factor tends to `(k dot (x-y))^2` and the kinetic occupation is concentrated
at `|p|ell<<1`. The displayed continuum coefficient is not asserted for
arbitrary states at the top of a finite lattice band. This is an analytic
regulator check, not a continuum renormalization theorem.

For a passive zero-temperature state with nondegenerate reference energy,
define
`S(k,E)=sum_(n!=0)|<n|rho_k|0>|^2 delta(E-(E_n-E_0))`
and `S_sym=(S(k,E)+S(-k,E))/2`. In a finite box the spectral expansion
of the double commutator gives directly

\[
 \int_0^\infty E S_{\rm sym}(k,E)dE={D(k)\over2},
 \qquad
 \chi_\rho(k,0)={2\over V}\int_0^\infty
                         {S_{\rm sym}(k,E)\over E}\,dE.
                                                               \tag{11}
\]

For `k!=0`, a nonempty state in the continuum regime has `D(k)>0`, so
its total density spectral measure cannot vanish. Its passive static
susceptibility is positive when finite, or divergent rather than zero.
Zero-energy degeneracy, a singular infinite-volume limit, excited
nonpassive ensembles and nonlocal regulators require their own spectral
qualification. At `k=0` the identity gives zero, consistent with a fixed
total charge, and gives no such static nonzero conclusion.

Equations (9)-(11) do **not** exclude ordinary matter retaining density
response while a distinct collective extra force disappears. They
exclude only identifying an exact finite-density off state with no
response of the very same cold density/displacement operator. A separate
definition of extra `P` is the missing dictionary, not supplied by this
sum rule. The sum rule also does not itself fix a static response
amplitude, cutoff, force normalization or storage lifetime.

## 5. Released matter and the separate nodal candidate

A released uncondensed positive-density gas provides a simple response
check without assuming condensation. In a prescribed Maxwell incoming
state of one-dimensional dispersion `sigma`,

\[
 \chi_{\rho,\rm gas}(k,0)={\rho_0\over\sigma^2}>0
\]

in its static long-wavelength, non-self-gravitating local control. This
follows directly by differentiating its distribution
`F(v^2/2+Phi_N)`: `F'=-F/sigma^2`. Other distributions need their actual
kinetic kernel. A loss of condensate changes response and transport; it
does not remove the original mass coupling or automatically change an
S4 response label. A vacuum control removes the carrier stock itself,
which is not S4's released ordinarily gravitating matter.

The existing nodal-ring action does generate a nonanalytic vector
potential from its filled fermion bands, through the declared vertex
`h P_j Psi_F^dagger Gamma_(j+2) Psi_F`. It contains no operator that
conditions that vertex, its filled-band state, or its counterterm on
the scalar condensate fraction, source abundance, or bound projector.
Its occupied band state and microscopic parameters were separately
assumed. In a fixed external gravitational probe the written carrier
and force-sector actions have no such portal; changing scalar phase
does not algebraically multiply the nodal determinant by that phase.
Common gravitational backreaction can alter states and density, but
must be computed as that interaction; it is not a derived binary
selector for a bound/free carrier label. Counting the same determinant
again would also double count the existing potential.

The attractive first-order phase of the separate `Psi,chi` host was
already explicit in the prior response note. Importing it here would
change the original scalar action and leave the same `P` source map
unproved. No new version or fitted coupling is inserted in this lane.

## 6. Decision and remaining implications

| Obligation | Result |
|---|---|
| Stable original uniform coherent source/daughter amplitudes | Unique occupied branch proved in the stated mean-field truncation |
| Same-control equilibrium hysteresis on that branch | Absent; the putative high-`mu` alternative is an unbounded grand functional |
| A gapless charge phase exists and responds | Derived explicitly with source fraction and positive compressibility |
| That phase produces critical local material `P` and its remainder | Not obtained; its displacement energy has derivative restoring terms |
| Loss of condensation makes a nonempty released density completely inert | Refuted for the same density operator in the passive continuum regime; explicit normal-gas countercheck |
| Density sum rule alone forbids every possible extra-force switch | Not claimed and does not follow |
| Existing nodal potential is automatically selected by scalar binding | No such source/occupation vertex or state relation is supplied |
| Physical tether/release polarization gate and memory closure | Incomplete; needs a derived common operator/state map and dynamics |

Nearest-prior distinction: `micro_response/DERIVATION.md` already computed
dilute amplitude kernels and the static inverse-divergence mismatch. This
note adds the global homogeneous branch classification, the retained
common Goldstone action at non-negligible source fraction, and the
local-charge spectral-moment test with its explicit finite-lattice
regulator qualification. Those tests do not rely on the old finite-gap
analyticity argument. General condensate hydrodynamics and spectral
moments are not claimed new to physics.

Open continuations include actual finite-host/nonuniform phase structure,
finite-temperature distributions, singular limits, and a specified
force-sector state relation. They are not declared exhausted or
impossible. Their resumption condition is an explicit shared-field
operator or constitutive derivation, not a fitted phase selector or an
assumed condensate-to-`P` equality. Repeating a vacuum-versus-gas density
change does not address S4's retained released mass.

Verification is direct algebra, completion of squares, phase variation,
operator commutators and spectral expansion. No numerical simulation,
symbolic package, fit or scientific program was run. This is author
analytic self-review, with a separate reconstruction needed to certify
the exact file scope; it is not an all-orders phase theorem or a
relativistic material-frame completion.
