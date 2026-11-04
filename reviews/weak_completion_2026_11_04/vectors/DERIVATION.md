# Canonical vector transport and cold Coulomb completion

All dimensional quantities use μ; physical time is τ=μt. Number cells are
`Y_i=g_s W_i f_i/(2π²)`, with physical density `T_c³ Y_i`. The scalar kinetic
coefficient62 and the physical initial packet are inherited from the common
contract. No radiative terminal replacement is made.

## Canonical vertices and physical degrees of freedom

`basis.py` reconstructs the exact charge/Casimir-adapted scalar and Takagi
fermion bases of the frozen model at each x. If R_A are the canonical Hermitian
SU(5) generators, tr(t_A t_B)=δ_AB/2, and V diagonalizes the real gauge mass
matrix, then the full24 currents are

- `Q_S^I=Oᵀ real_generator(Σ_A V_AI R_A) O`;
- `Q_F^I=U† diag(R^I,R^I_adjoint) U`;
- `K_aIJ=∂ M²_V,IJ/∂S_a`.

The real scalar current vertex is `-ig Q_S`, and the Weyl current is `g Q_F`.
The canonical mass interaction is `V_I M²_IJ(S) V_J/2`, giving vertex
`iK_aIJ g_μν`. Twelve charged Goldstone tangent columns are projected out of
the scalar gas. The Ward tests compare the full cubic Goldstone projection to
`g(m_a²−m_b²) Im(Q_S)/m_V` and the Yukawa projection to
`g(m_i Q_F,ij + m_j Q_F,ij*)/m_V`, allowing the common tangent phase. They pass
at the recorded table points. Loop-corrected gaugino masses in the common
background supply the event thresholds; the vertices and Ward tests are tree
quantities. This is the same leading-vertex/matched-mass convention as the
frozen S/F source, rather than a loop vertex completion.

The gas has thirty groups. The new vector groups are `Vc_L` (12 states),
`Vc_T` (24 states), `V8_T` (16), `V3_T` (6), `V1_T` (2), all bosonic.
`Vc_L/T` have `m_V²=25g²[2/(31e)+x²]` and derivative `50g²x`; the other three
have zero tree mass. Root's frozen `integration/common.py` supplies these same
masses to gas energies, forces, and event kinematics.

## Spin-resolved amplitudes

Metric is (+---). All polarizations obey ε·k=0, ε·ε*=-1. L/T refer to helicity
relative to the physical momentum in the cosmological frame. T averages the
two initial helicities and sums the two outgoing helicities. There is no
average over three massive-vector polarizations in transport.

For each raw group block, set `A=g² Σ|Q|²/n_parent` and
`B=g² Σ Re(Q²)/n_parent`. Parent Weyl multiplicity excludes its two spins,
since the fermion amplitude already averages them. Vector-parent division is
by12 real colour columns, since a specified L or T parent is used. Same-group
scalar or Majorana final pairs divide the ordered raw block by2.

The squared amplitudes used by `rates_v2.py` are:

- `S(P)→S(k)+V(q)`: `4A |P·ε(q)|²`;
- `V(P)→S(k1)S(k2)`: `A |ε(P)·(k1−k2)|²`;
- `F(P)→F(k)+V(q)`: `2[A(2|P·ε(q)|²+k·P)+B M m]` per polarization;
- `V(P)→F(k1)F(k2)`: `4[A(k1·k2−2|ε(P)·k1|²)−B m1m2]`;
- `S→VV`: `Σ K² |ε1*·ε2*|²/n_parent`, with the unordered identical-state
  factor. LL and TT have factor1/2; LT has factor1.

The differential rest rate is `dΓ/dz=β |M|²/(32π M)`. The event rate has the
additional exact `M/E_parent` time dilation. The current of two Majorana modes
has vector coefficient `i Im(Q)` and axial coefficient `−Re(Q)`; their parity
asymmetry vanishes. Independent Dirac traces check both equal T helicities and
the above signs and factors to floating point precision. Matter spins remain
unpolarized and the isotropic one-particle vector density is diagonal in L/T;
this is a molecular-chaos closure, not a claim that daughter spin correlations
are absent in an individual decay.

Full daughter four-vectors are boosted before evaluating their L/T projectors.
For `S→SV` and `F→FV`, the stable projection uses
`Σ_L,T |P·ε|²=M² p_*²/m_V²`; subtracting the T projection avoids cancellation
near a protected threshold. Boost tests sum L/T and recover the same inclusive
rest width at P=0,.04,.2.

Absolute benchmarks are `Γ(V→one Weyl)=g²q²M/(24π)`,
`Γ(V→one Dirac)=g²q²M/(12π)`, and
`Γ(V→one complex scalar)=g²q²M/(48π)` for massless daughters. The SVV
normalization agrees with the independently checked identical-real-vector
formula `K² M³ sqrt(1−4r)(1−4r+12r²)/(128πm_V⁴)`.

## Finite collision representation

The frozen `transport_v3.py` combines the exact-angle S/F backend with positive
vector Gauss quadrature on every pair of daughter-energy stencil intervals.
Each event has one parent and four daughter stencil entries, weights summing
to one for each daughter. All stencils use *the same common background
energies* as the gas. The geometric products of f and 1±f satisfy quantum
detailed balance exactly when `log[f/(1±f)]` is affine in energy and conserved
charges. The event stoichiometry conserves energy; its affinity times flux is
nonnegative, proving the finite H theorem. The imported exact-moment algebra
is used with zero angular slope for each positive quadrature node. An
independent availability array preserves sub-ulp fermion holes.

Massless-vector VSS/VFF currents commute their matter masses. Mixed physical
SVV broken/unbroken blocks vanish. The one-broken/two-unbroken VVV tensor
vanishes by the unbroken algebra; other VVV cuts are closed or at threshold.
Thus all three unbroken vector populations have zero tree1↔2 source here.
Loop radiation is a separate matched channel, not included by calling a
massive neutral daughter radiation.

The frozen table `run_table003/result.json` covers x=.1..100, with .05 spacing
below1, .125 spacing from1..6.5 and declared wider cold intervals. Convex
linear interpolation is applied to A,B,K²; exact common masses determine all
thresholds. At x3.8632233 the total width-integrand interpolation L1 error is
3.84e-5. A tiny nearly vanishing channel has38% relative error, so the small
total error does not establish channelwise relative precision. Zero-valued
interpolated metadata channels must be filtered by width>0 in charge or
eligibility statements; their collision coefficients are exactly zero.

## Coulomb discriminator

The separate `coulomb/` leaf uses the actual CT09 late scalar packets and
CC10 changing-memory shapes, with physical scalar occupation
`f_physical=2 f_number_normalization` and twelve real scalar modes. No RMS
velocity substitutes for the relative distribution. For isotropic positive f,
static electric screening is evaluated by integration by parts:

`m_D,a² = g² g_s C_r,a/d_A /(2π²) ∫dp f(p)[E+p²/E]`.

The actual matrix traces give SU3, SU2, U1 squared-charge factors
`2/9,3/16,25/144`, totaling7/12. The corresponding scalar screening
multipliers are2,3,5. For Yukawa-screened Born scattering, with reduced mass
m/2 and R=4μ_red²v_rel²/m_D²,

`σ_T = 2πα² C/(μ_red² v_rel⁴) [log(1+R)−R/(1+R)]`.

The relative-speed density is obtained from the exact radial convolution of
the recorded piecewise-constant f, and integrated through the screening scale
on logarithmic relative momentum. Diffusion is also independently integrated
with the tag and partner momenta and their relative angle. The second angular
moment is retained for radial diffusion. Bose corrections are bounded by the
actual tiny occupation; the source has no populated charged fermions.

The low-relative-speed region α_eff/v_rel>1 contributes up to22% of the
reported Born *rate*, which is not promoted as a controlled total rate. Its
Born contribution to momentum diffusion is only ~2.4e-6. Dominant momentum
diffusion is in the weak-Born regime. Dynamic screening, identical-exchange
and contact finite-log corrections, nonperturbative low-speed scattering, and
other populated baths are explicit remaining precision limitations.

The new binary builder uses the canonical scalar direct-t matrix element
`|M|²=g⁴ C[2(s−2m²)+t]²/(t−m_D²)²`, exact CM boosts, and positive quadrature
split at daughter kinetic-energy stencils and log(Q²+m_D,min²) intervals.
Projection uses `K=p²/(E+m)` to avoid cold rest-energy subtraction.
Conservation of K and particle number implies conservation of full E.
For a domain integrating every incoming pair and its reverse, reversible
flux F−R has an extra orientation factor1/2: the unordered incoming coefficients
are1/2 for i<j and1/4 for i=j. Without this factor the continuum collision
operator would be doubled. Root supplies the generic six-index binary quantum
backend, including stable affinity differences and chunked Jacobians.

## Why self-scattering can refill holes while barely changing pressure

For one massive species let `k_i=E_i−m`, `N=ΣY_i`, and `Ktot=ΣY_i k_i`.
The following are exact, before multiplying by physical density `T_c³`:

`P = [2 Ktot − ΣY_i k_i²/E_i]/3`,

`F = m' [N − Ktot/m + ΣY_i k_i²/(m E_i)]`.

The elastic operator conserves N and Ktot. Therefore it preserves the leading
nonrelativistic pressure and rest-mass force even when the radial shape
changes. Only the displayed higher moments can change them at fixed mass and
time. In `run_elastic_relax001`, a2.14% number-weighted shape change gives only
~1.7e-11 relative pressure change and ~5.8e-14 relative force change. This is
not a reason to omit elastic scattering: the redistributed shape enters the
resonant chemical kernel and hence future charged loss, neutral production,
and field support. The separate cold-window comparison measures that effect.

The cold2→2 gauge-annihilation probe derives the canonical scalar seagull
threshold factor `C_ann=13/4`, so
`σv=g⁴(13/4)/(32πm²)`. The pair-colour potential eigenvalues are
`(−2.5,−1.5,−1,0)` with multiplicities `(1,3,8,24)` and annihilation traces
`(14,15,40,48)`. Coulomb Sommerfeld factors are averaged over the actual
relative-speed distribution with these annihilation weights. Their averages
are1.00030..1.00300 in the tested cold packets; the chemical gauge-annihilation
rate/H is3.33e-13 initially and2.64e-15 at the memory endpoint. This finite
window test does not assume Born behavior at arbitrarily late velocities.
Screened bound states, shallow resonances and radiative formation require
separate treatment if the future distribution enters that regime.

## Charged-current opacity of late hot photinos

Gauge neutrality does not remove the tree χ+C↔F current. The pole masses used
in the test are MC=.0387298334621μ, MF0=.0393289733363μ and
mχ=5.2365374e-11μ. The actual current-projected partial width is
Γ(Fc_0→Sc_0χ)=3.8894719e-13μ, with p*=.0005945762083μ. A scalar target at rest
absorbs a photino at

`Eres=(MF²−MC²−mχ²)/(2MC)`, `pres=(MF/MC)p*`.

Here Eres=.0006037741388μ. The two heavier charged fermions have resonances
.25910μ and.26378μ, beyond the whole fixed neutral-parent packet's energy.
The checked S8/S3 loop channels produce rest-frame χ energies.00132296μ and
.00505253μ. Boosted birth energies change the crossing time; they do not exceed
the uniform narrow-line opacity envelope evaluated from the actual C history.

For an unpolarized target and χ, the inverse amplitude sum is
`|M|²_in=(gF/(gC gχ)) |M|²_decay`, with ratio24/(12×2)=1. The decay relation is
`|M|²_decay=8π MF² Γin/p*`. The inverse one-body phase measure is
`2πδ(s−MF²)`, and `s=MC²+mχ²+2MC Eχ`. Along cosmological redshift,
`dEχ/dt=−H pχ²/Eχ`. Integrating the delta function therefore gives exactly

`τ_line=2π² [gF/(gC gχ)] nC Γin/(H p*³)`

in the rest-target limit, including nonzero mχ. An independent narrow
Breit–Wigner area integration checks this factor to6e-15. Target mean v² is
below7.35e-7, so the NR/Doppler qualification is explicit. The tested cold
histories give τ≤.0006626103 even though Γin/H is5.5e5..5.5e7. A large width/H
is consequently not an optical depth for a particle crossing a narrow line.
The quoted probability counts every formation, even a subsequent F decay that
returns χ, making it conservative for photino removal. Early warm seeds are
not assumed to survive.

The off-resonant estimate uses the actual U1 Yukawa norms, both charged-fermion
exchange diagrams and a spinor/operator-norm bound outside a broad10% resonance
band. The integrated estimate is≤1.72e-9 on the named paths. Future columns
hold the pole fixed and bound comoving C by its last value; they are conditional
extrapolations, not a new cosmological solution.

## Warm gauge-annihilation estimates

The warm records use the actual full30 population after the finite vector
control. The rate denominator is the number of *charged carriers*; corrected
002 records supersede the earlier all-gas normalization.

For scalar annihilation to unbroken gauge pairs, the contact, t, u and s
matrix norms obey a pointwise triangle bound. With d=6 and Ctot=5/2,
`Σ||{Ta,Tb}||²=117`, `Σ||TaTb||²=37.5`, and `Σ||[Ta,Tb]||²=33`.
The scalar exchange kinematic coefficients are bounded by4, the s coefficient
by1, and each massless transverse polarization contraction by1. Summing four
polarization pairs and the unordered-gauge factor gives the conservative
squared-amplitude bound `300g⁴`. Hence
`σv_Moller ≤300g⁴/(32πE1E2)` for the scalar current process.

For charged fermions, positive Dirac spin traces are evaluated for each t/u/s
diagram and bounded using three times the sum of their squared norms. The
canonical colour factors are25/24 for each ordered product and11/12 for the
commutator. Positive CM-angle quadrature, actual pair distributions, refinement
and5% inflation are recorded. For massive-vector annihilation the three
Yang–Mills exchange contributions and three quartic colour terms are bounded
by six times their separate squared norms, using the unitary-gauge massive
propagator. The full3×3 incoming spin sum bounds any boosted L/T density;
no unpolarized closure is assumed for this bound. Actual angular quadrature
and10% inflation are reported. Scalar resonances already represented as
inverse1↔2 paths are not double-counted as separate gauge annihilation.

The resulting finite-packet estimates for fractional charged loss/H are
≤.000358 scalar, ≤.000244 fermion, and≤1.52e-8 massive vector. They are
diagram-norm estimates on tested positive quadratures, not exact-interference
cross sections or an all-epoch annihilation proof.
