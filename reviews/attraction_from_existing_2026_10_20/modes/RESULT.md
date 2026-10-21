# Existing modes: an exchange attraction and the missing conversion operator

20 October 2026. Initial observed HEAD:
`b10ed68d6bbc90744c5aa77ae7c702c2898507c1`. Read-only source comparisons
and actual working-byte hashes are in `source_hashes.json`. This lane writes
only this directory; no scientific numerical run was performed.

**Normalized claim and verdict — incomplete, with the smallest missing
implication.** An already declared, stable daughter phonon bath gives a
calculable attractive contribution between two occupied fragmented scalar
modes. It needs no new microscopic coupling or fitted `J`; its amplitude
still depends on the physical bath state and orbital shapes. The
contribution needed by the memory question is the interaction between two
*free-to-tethered changes*, not between two added scalar particles. The
existing equations do not identify those changes with two physical scalar
states or fix their bath matrix elements. For a conversion that merely
relabels a co-located density, the phonon contribution is exactly zero.
The finite memory criterion is therefore not closed by this route.

## 1. Raw equations, hypotheses, and distinctions

The exact local inputs used here are:

| Input | Raw locator | Content used |
|---|---|---|
| Original carrier | `MASTER_COLD_ENERGY_EQUATIONS.md:67-117` | charge-one `Phi`, charge-two `X`; positive-square potential; NR `psi,b`; positive residual contact |
| Matched daughter contact and retained source | `micro_response/DERIVATION.md:11-80` | `g2=lambda_rep/(2m^2)>0`; source exchange and its matching correction |
| Existing bath vertex | `occupied_landscape/LANDSCAPE.md:490-531` | `E_q`, density amplitude, conditional fragmented-mode coupling `gamma=2g2`, stable-patch restriction |
| Existing occupied spatial dimer | `occupied_landscape/LANDSCAPE.md:293-378` | four Fock sectors; actual contact/Newtonian pair interaction; conditional loading law |
| Separate real-mediator host | `MEDIATOR_COMPLETION_AND_VALIDITY.tex`, sections 2-3; `micro_response/DERIVATION.md:105-124,220-301` | `Psi,chi` host, its existing attractive quartic and stabilizing higher terms |
| Existing fermion force sector | `MASTER_COLD_ENERGY_EQUATIONS.md:201-259`; `NODAL_RING_ORIGIN.md:45-92` | `P`-fermion mass vertex; counterterm and determinant conventions; absence of a carrier identification |
| Counted conversion criterion | `memory/RESULT.md`, sections 2-3 | canonical conversion energy `H`; multiplicities `(1,4,2)`; threshold below |
| Reciprocal mechanics | `reciprocity/SOURCE_RESPONSE.md:34-58,103-141` | count gravity once; tether self counterterm; reciprocal source variations |

Paths are expanded in `source_hashes.json`. Natural units are used. Here
`n_i=0,1` denotes occupation of a declared localized, number-isolated mode,
not the original carrier Noether charge density or the canonical tether
fraction. `gamma` below is the derived projection coefficient `2g2`, not an
adjustable new coupling. Static occupations, a dilute bath, orthogonal modes,
negligible number-changing terms, and weak bath deformation are hypotheses,
as they already were in the source. A supported finite patch must have a
positive retained bath Hessian. Infinite homogeneous self-gravitating matter
does not satisfy this requirement in its infrared.

The dependency graph is

`original contact -> conditional fragmented-mode density vertex -> stable
harmonic bath -> exchange double difference` (derived below), followed by

`physical free/tether states -> their density/source changes -> complete
sector energies -> memory inequality -> physical transition/lifetime`.

The second chain has missing internal inputs, not an external theorem gap.
An orbital tunneling gap within a captured `N_pair=1` dimer is a different
quantity from a free/tether occupation barrier.

## 2. Eliminate the bath actually coupled in the source

For a finite set of stable bath modes with `E_nu>0`, the retained static
Hamiltonian has the form

\[
 H=E_{\rm loc}(n_1,n_2)+\sum_\nu E_\nu b_\nu^\dagger b_\nu
   +\sum_\nu(C_\nu b_\nu^\dagger+C_\nu^*b_\nu),\qquad
 C_\nu=n_1g_{1\nu}+n_2g_{2\nu}.
 \tag{1}
\]

Completing each square gives, exactly for (1),

\[
 H=E_{\rm loc}-\sum_\nu {|C_\nu|^2\over E_\nu}
   +\sum_\nu E_\nu
   (b_\nu^\dagger+C_\nu^*/E_\nu)(b_\nu+C_\nu/E_\nu).
 \tag{2}
\]

The terms `-n_i^2 sum |g_i|^2/E` are the one-mode dressing self energies.
For hard-core occupations `n_i^2=n_i` they shift the one-site energy. They
cancel in `E11-E10-E01+E00`. The actual cross contribution is

\[
 \boxed{U_{12}^{\rm ex}=-2\sum_\nu
        {\operatorname{Re}(g_{1\nu}^*g_{2\nu})\over E_\nu}.}
 \tag{3}
\]

Its factor 2 is fixed by the cross term of the square. It is not a new
susceptibility added to the original Hamiltonian. The free energy of the
displaced harmonic oscillators has the same shift at any fixed bath
temperature if their frequencies are occupation independent. Frequency
changes and anharmonic bath corrections are additional contributions when
that approximation fails. If particle exchange makes the sectors nonstatic,
the displacement also dresses the hopping/exchange operator; (3) alone is
then an adiabatic sector-energy result, not an exact full spectrum.

For the source's local homogeneous approximation, normalized localized
number densities `rho_i(x)` give

\[
 g_{i\boldsymbol q}=\gamma\sqrt{n_0\over V}
       \sqrt{\epsilon_q\over E_q}\,\rho_i(\boldsymbol q),\qquad
 E_q^2=\epsilon_q(\epsilon_q+2g_2n_0),\quad
 \epsilon_q={q^2\over2m},\quad\gamma=2g_2.
 \tag{4}
\]

Here the transform includes the packet's position and shape. Consequently

\[
 U_{12}^{\rm ex}=-2\gamma^2n_0\int {d^3q\over(2\pi)^3}
 {\operatorname{Re}[\rho_1(q)^*\rho_2(q)]\over
                     \epsilon_q+2g_2n_0}.
 \tag{5}
\]

For two point packets at distinct positions separated by `r>0`, the
formal infinite homogeneous contact-Bogoliubov control is

\[
 \boxed{U_{12}^{\rm ex}(r)=
       -{m\gamma^2n_0\over\pi r}e^{-\kappa_B r},\qquad
       \kappa_B^2=4mg_2n_0.}
 \tag{6}
\]

This uses `int d^3q/(2pi)^3 exp(iq.r)/(q^2+kappa_B^2)
=exp(-kappa_B r)/(4pi r)`. Equivalently, for resolved nonnegative packets,

\[
 U_{12}^{\rm ex}=-{m\gamma^2n_0\over\pi}
  \iint dx\,dy\,\rho_1(x)\rho_2(y)
          {e^{-\kappa_B|x-y|}\over|x-y|}\le0.
 \tag{7}
\]

Resolved packet forms regulate their self energies. A point-packet self
energy is ultraviolet divergent and must not be assigned a finite binding
bias without a matching prescription. The cross potential at nonzero `r`
has no such point self divergence. In a fixed-charge finite bath the exact
number zero mode is constrained; use the supported nonzero-mode sum in
(3), not an unconstrained `q=0` compressibility.

Equations (6)-(7) are local comparison formulas. Integrating their formal
continuum over all momenta does not establish a stable self-gravitating
patch: the actual lowest modes, boundaries, recoil, and source overlaps
must replace it. A truncation to a stable momentum window does not retain
the strictly positive real-space Yukawa kernel or guarantee the pair sign.
The finite-mode formula (3) remains the relevant test. Higher phonon orders
can also dominate a tiny exponential tail at very large separation.

For the fixed finite hard-core domain and finite regulated sums, (2) is
bounded below whenever `E_loc` is finite. Extending its negative quadratic
shift to unlimited local occupations is unjustified. Full same-species
stability also requires the original contact, number constraints, bath
backreaction, and all allowed mode-conversion terms. In particular the
`gamma=2g2` fragmented projection cannot be used for a coherent deformation
of one condensate in place of its full Bogoliubov Hessian.

## 3. Replace added occupations by actual conversion changes

For a closed site containing one original particle in either a free orbital
`f_i` or a tethered orbital `t_i`, the existing density vertex couples to

\[
 \rho_i(x)=\rho_{f_i}(x)+n_i\Delta\rho_i(x),\quad
 \Delta\rho_i=\rho_{t_i}-\rho_{f_i},\quad
 \int\Delta\rho_i=0.
 \tag{8}
\]

This is a conditional dictionary, not the assertion that the project has
derived these orbitals, their material sites, or their free/tether mechanics.
It preserves the charge-one inventory. The bath displacement is now
`C=C0+n1 Delta g1+n2 Delta g2`. Direct evaluation of the four sectors gives

\[
 \boxed{U_{\rm conv}^{\rm ex}=-2\sum_\nu
 {\operatorname{Re}(\Delta g_{1\nu}^*\Delta g_{2\nu})\over E_\nu},}
 \quad
 \Delta g_{i q}=\gamma\sqrt{n_0/V}\sqrt{\epsilon_q/E_q}
                  \Delta\rho_i(q).
 \tag{9}
\]

All baseline shifts, linear terms, and one-site self energies cancel. Using
only `rho_t`, omitting the free particle from each reference state, produces
(5) instead of (9) and answers the wrong question. The signed changes in
(8) make the sign in (9) indefinite. Identical change sources have a
negative cross shift; opposite change sources have a positive cross shift.
For different sites the actual overlaps decide. Equal conserved charge
also forces `Delta rho_i(q=0)=0` rather than a bath monopole.

There is a sharp scoped obstruction:

\[
 \rho_{t_i}(x)=\rho_{f_i}(x)\ \text{pointwise}
 \quad\Longrightarrow\quad\Delta g_{i\nu}=0
 \quad\Longrightarrow\quad U_{\rm conv}^{\rm ex}=0.
 \tag{10}
\]

Thus an already coupled *density bath* cannot distinguish a co-located
free/tether label conversion with identical density. This statement covers
the retained linear density vertex; equal one-body densities by themselves
do not equate different two-body correlations or prove an all-orders
Hamiltonian theorem. A true internal label with a new species-selective
phonon coupling would be an added operator, forbidden in this attempt.

The dimensionless diagnostic `sum |Delta g_i/E|^2` measures the bath's
coherent displacement in a given mode basis; small local depletion and
negligible omitted mode mixing must be checked in the physical state.
Choosing a soft `E_nu` to increase (9) without checking these conditions is
not a controlled parameter-free enhancement.

## 4. The counted memory test, with no fitted J

For exchange-symmetric sites let `E0=E00`, `E1=E10=E01`, `E2=E11` be the
*complete* sector energies in the same fixed-inventory environment. The
three-state multiplicities in the memory source are `(1,4,2)`. At endpoint
coexistence the exact intermediate weight is

\[
 w_1=2\sqrt2\exp\!\left[{U_{\rm pair}\over2\theta}\right],
 \quad U_{\rm pair}=E_2-2E_1+E_0,\quad\theta>0.
\]

Both endpoints are strict occupancy maxima precisely when

\[
 \boxed{U_{\rm pair}<-3\theta\ln2.}\tag{11}
\]

For unequal sites use `E11-E10-E01+E00` as the interaction invariant, but
the displayed three-state counting and coexistence reduction need their
own bias/degeneracy calculation; symmetry is not automatic.

Within the memory source's *co-located fixed-shell* control, the canonical
conversion cost has

\[
 \Delta^2H=H(2)-2H(1)+H(0)>Gm^2/r>0.
 \tag{12}
\]

After counting each interaction once, a conditional phonon proposal would
have to establish, in that same geometry,

\[
 2\sum_\nu{\operatorname{Re}(\Delta g_{1\nu}^*\Delta g_{2\nu})\over E_\nu}
 >\Delta^2H+U_{\rm other}+3\theta\ln2,\tag{13}
\]

where `U_other` is the remaining non-overlapping microscopic sector
curvature, including actual contact and deformation terms. This notation
introduces no new tunable interaction. In the density-preserving control
(10), the left side is zero: the phonon route fails to pay even the positive
canonical cost, before the entropy price is included.

For a spatial change, the canonical source profiles and their energy must
be recomputed in all four sectors; it is not legitimate to attach the shell
`H(n;r)` unchanged to arbitrarily different scalar orbitals. The recent
reciprocal energy already counts Newtonian pair gravity and the critical
`+T^2` self cancellation. Adding another `-Gm^2/r` as an independent latch
term double-counts that part of the energy. The remainder `W_rem` also has
to be varied, along with any occupation-induced bath/host deformation.
One-body binding shifts can set a coexistence bias but cancel from (11).
Long-lived memory still needs the actual transition operator and a finite
release/capture time, not just an attractive energy double difference.

The source's spatial dimer `V_LR~-Gm^2/r` compares one versus two scalars
inside a two-center host. Its `N_pair=1` gap is an internal tunneling gap;
its `V_LR+2J` loading window is a charge-sector condition. It does not
provide the closed two-site free/tether states required by (8)-(13).

## 5. Why other existing exchanges do not supply the missing vertex

**Original charge-two source.** The NR source vertex is
`c3(b^*psi^2+b psi^{*2})`, conserving
`Q=int(|psi|^2+2|b|^2)`. Its attractive virtual shift is already contained
in `k_eff=k_c-c3^2/delta`. The negative-frequency source matching further
changes `k_c` by `-g_c^2/[8m^2 M(M+2m)]`, leaving the dilute matched contact
`g2=lambda_rep/(2m^2)>0`. Keeping only its attractive diagram and adding it
to the already matched `g2` double counts exchange and discards the
positive-square contact. At finite momentum in this static dilute kernel,
`-c3^2/(delta+q^2/(2M))` is least negative at larger `q`, so it does not
overturn the stated positive zero-momentum residual there. Near the real
conversion resonance, virtual-only elimination is invalid; a real `X`
stock is charge two and mass approximately `2m`, not a free/tether label
of one daughter. No conclusion about all finite-density phases is asserted.

**Separate real-mediator host.** Its *existing* `2M chi |Psi|^2` coupling
gives `lambda_eff=lambda_Psi-a^2/(2M^2)=-m_h/M` in the stated mass units,
with a positive sextic and an exact positive full potential. This is a real
attractive and stable particle-model construction. It was explicitly
declared separate from `Phi,X`, and its own charge-one `Psi` inventory and
mass do not supply a canonical tether/free dictionary. Reidentifying it
with the carrier or choosing two lattice sites for its first-order density
phase would be an extra physical bridge. Its existing bulk phase is not a
derived finite binding latch or release kernel.

**Nodal-ring fermions and collective P mode.** The raw fermions couple to
`h P_j Gamma_(j+2)`, and the force scalar to `q_b rho_b varphi`. The source
does not contain `n_t P`, `n_t Psi_F^dagger Gamma Psi_F`, a scalar-density
portal to these fermions, or an operator identifying a carrier occupation
with the vector `P`. Thus one cannot use a fermion susceptibility as a new
occupation coupling. The filled-band energy already generates the cubic
`Ah^3|P|^3/3` after a specified quadratic subtraction. Retaining those
fermions and adding that same cubic/determinant again is double counting.
Changing their occupation or subtraction changes the constitutive law and
must enter the same complete energy. Positive collective spectral weight
can establish passivity of a supplied vertex; it does not create the absent
occupation vertex or select its source symmetry.

Minimal gravity couples to the complete mass/energy source, not a chosen
subsystem dipole. The existing landscape source includes host recoil and
has zero uniform mass dipole. Neither a new uniform-gravity dipole vertex
nor a baryon phase monopole can be imported: the original scalar `U(1)`
has a source-free continuity equation. A scalar free/tether subdivision
would need to preserve that charge and its mass/source accounting.

## 6. Obligation matrix and exact close-out requirements

| Obligation | Status |
|---|---|
| Existing contact yields a fixed fragmented-mode phonon vertex | Conditional on the source's declared state/projection |
| Stable harmonic exchange shift, including factor 2 and self energies | Passed analytically for (1) |
| Nonpositive Yukawa exchange between added nonnegative packet densities | Passed in the formal homogeneous contact-Bogoliubov control only |
| Attractive exchange between actual free/tether changes | Conditional on their missing matrix elements; sign indefinite in (9) |
| Co-located density-label conversion acquires phonon attraction | Refuted for the retained density vertex by (10) |
| Original source exchange gives an uncounted attractive dilute contact | Refuted within the matched dilute kernel |
| Existing fermions have an occupation vertex to the original carrier | Not established in the inspected raw equations |
| Exact finite memory inequality (11) is satisfied | Not established; fails for the density-preserving phonon control with positive canonical curvature |
| Positive stable full geometry, inventory, source work, and lifetime | Not established by these static reductions |

The cheapest physical next check is not a new fitted `J`: specify two
orthogonal original-scalar free/tether orbital pairs in one supported live
host, with a conserved inventory and a justified fragmented-mode regime.
Compute their four *complete* sector energies and the existing bath
overlaps, including the host's reciprocal work and the counterterm once.
Then apply (11), check the positive bath Hessian and small deformations,
and derive capture/release matrix elements from the same Hamiltonian.
No such state specification was supplied by the inspected inputs, so no
numerical coefficient, memory lifetime, or empirical pass is inferred here.

Nearest prior overlap is established condensate-mediated impurity
interactions; see `LITERATURE.md`. This report claims a scoped application
and a missing dictionary, not a new general exchange mechanism or global
novelty. Review provenance: author analytical self-review of the displayed
derivation, plus direct source checks. `EXCHANGE_AUDIT.md` records a fresh
sibling-agent reconstruction of the oscillator factor, Fourier coefficient,
range, and conversion subtraction only; it is not an independent audit of
the whole physical argument.
