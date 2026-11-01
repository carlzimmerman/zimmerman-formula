# A deliberately loose bound on the leading hard dimension-seven channel

This is an independent analytical majorant, to be reviewed separately from
the author's exact decay vertices. Let M be the minimum mass in the residual
U1-charged heavy block, in ordinary Feynman R_xi=1 gauge, and let kappa bound
every mass entering a trilinear Higgs/vector mixing by Mmax/M. We take
kappa<=100, much looser than the actual hierarchy. All external states are
normalized unbroken gauge generators; all polarizations have unit norm.

## Topology and scope

There is no renormalizable vertex with two external gauginos: their cubic
couplings have one internal charged boson and one internal charged fermion.
An unbroken external gauge field or gaugino carries zero residual U1 charge.
Consequently a one-loop cycle containing the external photino carries a
nonzero conserved U1 charge on every internal edge. All its edges are
massive, including Feynman-gauge Goldstones. The massless Landau Goldstones
are not assigned a positive mass by hand; the calculation is in xi=1.

Package the quadratic heavy fluctuations as real scalars/vectors and
four-component fermions. Their one-loop effective action is the appropriate
supertrace log. The two external fermions enter as off-diagonal boson/fermion
insertions. Each external gauge field enters either a trilinear insertion,
or the two enter a single bosonic seagull. Thus the only one-loop words are
four-insertion boxes and three-insertion seagull triangles. All S/F/V
internal types and scalar/vector mixing are blocks of these operators;
they are not omitted diagram classes or extra species sums.

Differentiating the fourth log term has at most4!=24 ordered words, and
the third at most3!=6, even before their cyclic/symmetry factors. We bound
the combined word count by64. Nambu/Majorana directions are included in
the fermion bundle, so no second charge-conjugate graph count is needed.
The complete bundles have194 bosonic components (98+4×24) and292 fermionic
components (4×73); an absolute supertrace is bounded by512 times the product
of operator norms. Restricting to charged fields can only reduce it.

Ghosts have no external-gaugino trilinear and cannot lie on such a cycle.
In linear Feynman gauge they therefore supply no extra fermion-transition
topology. A1PI-to-S-matrix reduction does not add a lower tree process:
the transpose involution forbids the entire one-field-strength transition
functional, including its off-shell derivative variants; LSZ multiplies a
vanishing tree transition. A neutral adjoint-scalar exchange would require
both a loop-generated chi-lambda-scalar vertex and a loop-generated
scalar-two-unbroken-vector vertex, since the corresponding tree vertices
vanish. Such exchange begins at two loops and is outside this bound.

## Vertex envelopes from the raw canonical action

For a normalized external generator, Tr_adj R²=5 and hence ||R||<=sqrt5.
Mass-basis rotations preserve operator/Frobenius norms. The raw external
gaugino scalar/Weyl Yukawa satisfies sum|y|²=20g² (two adjoints); the
gaugino/vector current satisfies sum|G|²=5g² before four Lorentz components.
Thus their combined boson-to-fermion insertion, per external spinor of unit
norm, is safely bounded by

    Y=32g sqrt5.

The factor32 exceeds the combined Frobenius bound and covers the real/
complex and four-component embeddings; no inverse eigenvalue or small-F
expansion occurs at a vertex. Further external-vector vertices obey

    ||V_F||<=8g sqrt5,
    ||V_B(k)||<=B r,  ||partial_p V_B||<=B,
    B=32g sqrt5(1+kappa), r=sqrt(k_E²+M²),
    ||V_BB||<=S=64g²×5.

These follow directly from the covariant kinetic terms. A scalar current
has momentum factor2k+p; the Yang–Mills three-vector current has three
metric/momentum terms, bounded by4|k| at p=0. The scalar/vector Higgs mixing
is a block of g R_ext times the vertical gauge map C, with
||C||=M_V,max, and so is bounded by a constant times g sqrt5 Mmax. Combining
these blocks and allowing momentum-routing factors is below the displayed
32(1+kappa) envelope. The gauge seagulls are sums of at most a few products
of two generators and Euclidean metrics;64g²×5 overcounts both scalar and
four-vector seagulls. Linear gauge fixing adds no higher-valence fermionic
vertex. These envelopes cover VVS transitions, not only scalar and fermion
loops with diagonal gauge vertices.

## Propagator derivatives and the convergent integral

At zero external momentum a Euclidean scalar/Feynman-vector resolvent D
and a four-component massive-fermion resolvent S satisfy

    ||D||<=r^(−2), ||partial D||<=2r^(−3),
    ||partial²D||<=10r^(−4),
    ||S||<=r^(−1), ||partial S||<=r^(−2),
    ||partial²S||<=2r^(−3).

The fermion inequalities follow from S=(i gamma.k+m)^(-1),
S†S=1/(k²+m²), and differentiating the inverse. The bosonic inequalities
follow by differentiating1/(k²+m²). They hold for arbitrary positive
splittings; the common lower gap M is the only denominator input.

With two fermion insertions a box has n_B+n_F=4 and n_B−1 bosonic gauge
vertices. Its undifferentiated norm therefore scales as
r^(−2n_B−n_F+n_B−1)=r^(−5). A triangle has two boson and one fermion
propagators and the same r^(−5) bound. Two external momentum derivatives
give at most256 r^(−7) times the vertex product. To see the constant is
conservative, the largest first-derivative coefficient sum is9, and the
sum of single-factor second-derivative constants is at most32. Their
Leibniz sum is below32+9²=113;256 covers all choices and routing signs.
The first derivative of a bosonic gauge vertex is included; its second
derivative vanishes. The exact positive radial integral is

    integral d⁴k/(2pi)⁴ r^(−7)=4/[15(16pi²)M³].

Denote L=16pi² and define the dimensionless amputated coefficient bound

    B_loop=2×64×512×256×4/(15L)×Y²×max(B²,S).

The prefactor2 conservatively covers continuation to physical external
momenta: the largest external momentum is at most order m_chi, and
m_chi/M is below2e−9. Each denominator shift is uniformly below order
m_chi/M relative to its Euclidean denominator, so its Neumann-series
bound and the finite polynomial numerators change this finite set of
derivative bounds by much less than2. No heavy threshold is crossed.

Gauge invariance and the C-forbidden one-field-strength functional remove
the lower momentum terms. The leading allowed two-field-strength
coefficient is therefore bounded by B_loop/M³. This is an upper norm bound,
not a signed matching coefficient or a claim that the physical amplitude
saturates it.

## Inclusive phase space

Two external spinors have norm product at most2m_chi. Two physical gauge
momenta have Euclidean norm product at most2m_chi². The amplitude for any
fixed spin/color/polarization is consequently bounded by

    |Amplitude|<=4 B_loop m_chi³/M³.

Overcount all light fermion labels, spin states, gauge colors and physical
polarizations by32768 (13×12²×2×2²<32768); discard the initial-spin average
and identical-boson suppression. The massless three-body volume is
Phi3=m_chi²/(256pi³); using it also overcounts massive final gauginos.
It follows that

    Gamma_hard <= (512 B_loop)² m_chi⁷/(256pi³ M⁶).

Thus c7_eff<=512 B_loop in the cold-state author's inclusive convention.
This includes all leading hard chi1->light gaugino+two-vector transitions
of the stated one-loop class. It does not establish an all-orders total
width: higher-loop exchange, higher-body soft/Ward radiation, and possible
nonperturbative/UV symmetry violation remain separate. It closes an explicit
leading Wilson-coefficient obligation if the numerical hierarchy and this
proof's finite coverage are independently verified.
