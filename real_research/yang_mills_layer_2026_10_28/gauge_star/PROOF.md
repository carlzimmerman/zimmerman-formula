# A gauge-star upper bound on kinematic discarded coercivity

Date: 2026-10-28. Candidate by the root investigator. This is a scope test
for a proposed layer theorem, not a counterexample to a physical mass gap.
No novelty claim is made.

Use the actual finite-volume vacuum and Casimir metric of
`../../papers/yang_mills_bounds_2026/sections/vacuum.tex`. Assume the full
vertex gauge group preserves the boundary conditions. Write t=x/(2a),
dmu=psi² dU, and k[f]=t integral sum_l |grad_l f|² dmu.

Let F contain every link incident to a vertex v, and let l be a link from
v to a distinct vertex. Let P=E_mu[.|all links outside F] and Q=I-P.
Define D_F by restricting the full ground form to ran Q. Then on the full
kinematic Hilbert space

    inf spec(D_F) <= t C_F = x(N²−1)/(4aN).                  (G1)

This holds at every coupling and every finite volume with the stated gauge
symmetry. The test function is gauge charged, so G1 does NOT give an upper
bound on the gauge-invariant physical discarded spectrum.

## Proof

Take a nonzero fundamental matrix coefficient f(U)=(U_l)_{ij}. A gauge
transformation only at v leaves every exterior link fixed. The conditional
law on F is invariant under this transformation, because dmu is invariant.
Averaging f over this vertex SU(N) action gives zero, whether v is the
source or target of l: the fundamental representation has no invariant
vector. Thus Pf=0 and f belongs to ran Q.

The one-link marginal of any fully gauge-invariant probability measure on
these link variables is Haar, provided l has distinct endpoints. Gauge
transformations at one endpoint imply invariance under left (or right)
translations of U_l, and normalized Haar is the unique such probability.
Consequently ||f||²=1/N>0. Only derivatives on l occur, and the fundamental
Casimir identity gives

    integral sum_alpha |X_(l,alpha) f|² dmu
       = integral_SU(N) sum_alpha |X_alpha U_ij|² dU
       = C_F integral_SU(N) |U_ij|² dU = C_F/N.

Hence k[f]/||f||²=t C_F, proving G1 by the variational principle.
All functions are smooth, so no operator-domain assumption is needed.

## Forest marginals and the physical restriction

More generally, the marginal on any set of links forming a forest is
product Haar. On a forest, vertex gauge transformations act transitively
on link assignments: fix the group element at a root of each component
and solve recursively along its edges. The invariant probability on that
compact homogeneous space is unique and product Haar is invariant.
The actual vacuum marginal has this invariance, hence equals product Haar.

The only gauge-invariant functions of forest links alone are constants,
by the same transitivity. A retained forest therefore does not supply a
nontrivial terminal physical excitation sector just because its kinematic
Galerkin form has the Haar gap.

If a proposal requires D_F>=c/a for all x approaching zero, with c>0
independent of x, on the entire kinematic space and with F containing a
full vertex star, G1 refutes it. A proposed lower bound of order x/a is
compatible with G1. Restricting to physical functions removes this test,
so a physical layer theorem must explicitly specify that restriction.
Gauge-star geometry, boundary gauge symmetry and distinct link endpoints
are essential hypotheses of this statement.
