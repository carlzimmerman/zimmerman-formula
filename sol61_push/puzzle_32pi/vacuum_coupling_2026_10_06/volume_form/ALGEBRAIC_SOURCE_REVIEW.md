# Independent review: conserved algebraic source classification

Verdict: the all-first-jet classification and its general-d measured-force
normalization are correct under the stated open-domain, symmetry, C1 and
conservation quantifiers. No blocking algebraic error was found. This is
stronger than a trace-projector counterexample but remains a scoped statement
about a source-only map, not all physical matter actions or added fields.

Reviewed SHA256:

- `algebraic_source/REPORT.md`: `91864eaa19d5f8de4ffd3ceca9f5863a5e8683b7fe8e02219108cbe6d9647b3b`
- `algebraic_source/checks.py`: `061bd442aaa24f113b9cbfd815e39c21a8c9b5c06ec664d20b18593d40c5ab94`

Both are below `sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/`.
This review reconstructed the proof; finite check counts are not its basis.
No peer code was executed or peer file changed.

At a normal-coordinate point, B maps a tuple of symmetric first derivatives
to its contracted divergence. B is onto: the first row of S_0 can realize
any vector, and its symmetry places no restriction on that row. The map
B(Id tensor DH) annihilates ker B by the hypothesis, hence factors uniquely
as L B. Restricting to a derivative tuple with one nonzero S_mu gives
DH(S)=S L^T for every symmetric S. Requiring symmetric output says
S L^T=L S. S=I gives a symmetric L, and commuting with all diagonal and
elementary symmetric off-diagonal matrices forces L=aI. This argument uses
arbitrary coordinate tensors, not a positive Euclidean spacetime metric.
It therefore works in the declared Lorentz normal frame.

The C1 integrability argument is sufficient: on a coordinate box, each output
coordinate depends on its corresponding stress coordinate alone because all
other partial derivatives vanish. Two independently variable stress
coordinates force their identical diagonal derivative a(T) to be constant
on that box. With dimension Sym^2>=2 and a connected open domain, these local
constants agree globally. Thus H=aT+B_0. Local Lorentz equivariance makes B_0
proportional to g. Even if the domain is not globally invariant, openness
permits small Lorentz transformations near each point; full infinitesimal
equivariance suffices for that invariant-tensor conclusion. Necessity and
sufficiency are correctly established. In spacetime d=1, the stated exception
is appropriate because conserved stress has no varying local jet.

The quantifier cannot be dropped: every formal conserved first jet is
realized by a local affine Minkowski tensor, but not necessarily by one
specified matter model coupled to its own gravity. The report explicitly
separates these statements. A fixed-trace radiation sector, pure constant
vacuum or lower-dimensional perfect-fluid stress manifold does not establish
the open-domain theorem by itself. Continuity from a connected open matter
domain to its vacuum boundary is an additional premise; disjoint sector
prescriptions evade that premise and need their own action/conservation audit.

The dust counterjet partial_1 T^00=1 is directly conserved in the normal
frame, while its trace derivative is -1. Thus T-(trace T)g/d has divergence
+1/d in direction 1. This is also a physically realizable local static
pressureless density pattern in Minkowski space, even though no sourced
self-gravitating stationary solution has been constructed by this witness.
It verifies the projector failure within a familiar restricted stress class.

For G+Lambda(x)g=aT+b(trace T)g with conserved T, Bianchi indeed enforces
Lambda=b trace T+Lambda_0. Substitution restores G+Lambda_0 g=aT. The
corresponding trace-free reconstruction follows from
partial[(d-2)R/2+a trace T]=0; choosing its constant dLambda_0 gives the
same Einstein equation. It removes an independently unequal trace coupling
while preserving free integration/boundary data. It does not classify an
arbitrary tensor-valued nonlinear compensator or furnish its exact-divergence
integrability; the report correctly leaves those hypotheses separate.

Finally, Einstein trace reversal gives
R_00=kappa_d rho_m c^2(d-3)/(d-2). Matching to
R_00=Laplace Phi/c^2 and Laplace Phi=Omega_(d-2)G_N rho_m yields
kappa_d=(d-2)Omega_(d-2)G_N/[(d-3)c^4]. Differentiating the supplied Tangherlini
potential gives the same factor. In d=4 it is 8piG_N/c^4; d=3 pressureless
force calibration degenerates and is correctly excluded from that formula.
The vacuum geometric coefficient kappa_d rho_E and scalar curvature
2d Lambda_eff/(d-2) are not interchanged. This calibration assumes the stated
universal Einstein source with no additional force sector; a scalar fifth
force would require the separate source conversion used in the volume report.

At fixed theory/boundary parameters an affine source can subtract one vacuum
height through b but cannot alter its slope relative to dust. Changing the
integration constant with a changed vacuum height is a different boundary
prescription. No acceleration scale or target coefficient follows. This
review supports the report's scoped obstruction without extending it to a
selective vacuum mechanism with extra species, derivatives or exchanges.
