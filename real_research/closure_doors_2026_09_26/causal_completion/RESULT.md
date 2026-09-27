# A causal completion of positive fourth-order dispersion, with its field cost

The concave-curvature gate repair produces a healthy-sign term
ω²=s k²+d4 k⁴, with d4>0. Used at arbitrarily high frequency that truncated
equation has no finite metric cone. Here is an explicit local completion that
removes that problem. It is a new quadratic construction, not a completed
embedding of the gate in the gravitational action.

## Local two-field construction

For real fields z,χ in Minkowski space, c=1, take m²>0 and real g≠0:

    L = ½[ż²−|∇z|²+χ̇²−|∇χ|²−m²χ²] + gχż.

The momenta are pz=ż+gχ, pχ=χ̇. The velocity Hessian is the identity;
there are **two independent scalar canonical pairs**. The Hamiltonian is

    H = ½[(pz−gχ)²+pχ²+|∇z|²+|∇χ|²+m²χ²] ≥ 0.

The field equations are z̈−Δz+gχ̇=0 and χ̈−Δχ+m²χ−gż=0. Thus both
principal wave operators use the same unit-speed metric cone. More directly,
the physical energy density

    h = ½[ż²+χ̇²+|∇z|²+|∇χ|²+m²χ²]

obeys ∂t h+∇·F=0 with F=−ż∇z−χ̇∇χ: the two gyroscopic terms cancel.
For a unit normal n, |F·n|≤h follows from 2|ab|≤a²+b². Integrating this
identity on the exterior of an expanding unit-speed cone proves that smooth
compactly supported initial data cannot carry energy outside that cone. This
is a continuum energy argument; the associated finite real inequalities and
dispersion identities are the limited Lean bridges, not a Lean PDE proof.

Writing A=m²+g², the dispersion relation is

    (ω²−k²)(ω²−k²−m²)−g²ω²=0,
    ω²± = k²+A/2 ± ½√(A²+4g²k²).

Their sum is 2k²+A>0 and product k²(k²+m²)>0 for k≠0, hence both
frequencies squared are positive. The light branch has the expansion

    ω²− = (m²/A)k² + (g⁴/A³)k⁴ + O(k⁶).

Every prescribed 0<s<1 and d4>0 can be matched by

    A=(1−s)²/d4,  m²=sA,  g²=(1−s)A.

No cutoff is hidden: the full two-field equations, rather than their truncated
expansion, have the finite propagation cone. This makes the positive k⁴ term
compatible with a causal local theory at quadratic level. It does not show
that these two fields have the required metric coupling or static response.

## Removing the second time derivative reopens an instantaneous channel

Delete χ̇²/2 while retaining its spatial gradient. The χ equation becomes
(m²−Δ)χ=gż. Eliminating this elliptic field gives a positive inertia factor
1+g²/(m²+k²), and

    ω² = k²(m²+k²)/(m²+g²+k²).

Despite the limiting phase speed one, this is not a finite-propagation repair.
For A=m²+g², the equation for the initial acceleration is

    z̈ = Δz − g²(A−Δ)⁻¹Δz
       = Δz + g²z − g²A(A−Δ)⁻¹z.

Take a smooth compactly supported nonnegative nonzero initial z0, with zero
initial velocity. Outside its support,
z̈(0,x)=−g²A(A−Δ)⁻¹z0(x)<0, because the Yukawa Green function is strictly
positive. In one dimension that Green function is e^(−√A|x|)/(2√A).
Thus an acceleration tail exists immediately outside the initial support.
This argument concerns the scalar field of this explicit model; no
gauge-invariant gravitational identification is presumed. Its high-k group
velocity also approaches one from above, with
lim k²(vg−1)=g²/2. The direct acceleration argument, rather than group speed
alone, establishes the nonlocal response.

## Implication for the open construction

The local completion is a constructive option if a second independently
healthy matter/amplitude field is explicitly allowed and justified. A change
of variables alone cannot turn its rank-two velocity Hessian into one
canonical scalar pair. The strict one-clock branch must instead produce a
different constraint structure and independently pass the conserved-source
response test. Removing a kinetic term is not sufficient.

Nothing here identifies either field with dark-matter particles. The open
questions are field classification, independent initial data, physical metric
coupling, and compatibility with the exact static exponential law. The same
fields and couplings must be used in the gate, cosmology and PPN calculations.

`run1` contains 20 exact checks of the Hamiltonian, roots, low-k matching,
principal polynomial, elliptic reduction and Yukawa identity. All passed with
Python 3.9.6 and SymPy 1.14.0 under a bounded run. The energy-domain-of-dependence
argument above is analytic; the script is not a substitute for it.
