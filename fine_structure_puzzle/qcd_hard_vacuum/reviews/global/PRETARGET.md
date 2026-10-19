# Independent pretarget derivation

Created 2026-10-19 17:52 UTC, before opening global_qcd/ or
coordinator/sea_hodge/ proof, code, verdict, or results. Reviewer is the fresh
subagent /root/global_independent_review. Task definitions and target-freeze
hashes were supplied by the coordinator; those hashes are metadata exposure,
not mathematical target exposure. No prior review or author calculation has
been read. Base is FSP009; prospective new packet is FSP010. This is a focused
independent proof audit, with possible subsequent exact finite checks.

## Definitions and counts

K_n is the cubical boundary of [0,n]^5, n a positive integer. The number of
k-cells, 0 <= k <= 4, is C(5,k)n^k[(n+1)^(5-k)-(n-1)^(5-k)]. Thus

N0=10n^4+20n^2+2; N1=40n^4+40n^2; N2=60n^4+20n^2;
N3=40n^4; N4=10n^4. The alternating sum is 2, and K_n is S^4.

## Pure normalized-Haar Wilson coefficient

The action in exp is (beta/6) sum_p(Tr U_p+Tr U_p^dagger). A single
unoriented cube boundary has six distinct plaquettes. For either coherent
orientation, every edge has one fundamental and one antifundamental factor.
Haar integration gives 3^(V-E)=3^(8-12)=1/81. Two orientations therefore give
2(beta/6)^6/81 = beta^6/1889568 per 3-cell in log Z. Consequently the first
connected contribution involving more than one plaquette is
N3 beta^6/1889568. W=-log Z reverses that sign. Local one-plaquette cumulants,
including the SU(3) order-three determinant invariant, must be separated.

Completeness at this order does NOT follow from a blanket mod-2 support rule.
SU(3) has integral UUU = epsilon epsilon/6, so three equally directed factors
at a link are possible. The following geometric argument controls the needed
order without denying those invariants. Any set of distinct squares with no
free edge contains at least six squares. Choose an axis mu in one square and
a slab containing mu-directed squares. Their transverse edges form a finite
simple cubical graph in which every vertex has degree at least two, because
the corresponding mu-link otherwise is free. Such a graph has at least four
edges (it is bipartite and has no multiple edges). Thus there are at least
four mu-directed squares. At the bottom and top of the entire mu-directed
support, a transverse edge has only one incident mu-directed square and
needs a square not containing mu; these two caps lie in different layers.
There are therefore at least six squares. Equality forces a four-edge square
in one slab and one square at each endpoint: precisely an elementary cube
boundary. Its six squares are in K_n only when the corresponding 3-cell is
in K_n. This is automatic by examining an inactive coordinate fixed at a
boundary value; if no inactive coordinate is fixed at a boundary, all six
faces cannot lie in the boundary of [0,n]^5.

At total Taylor degree <= 6, a support with a free edge can be integrated in
that edge. All insertions on its sole plaquette form a class function of U_p;
the result is its one-plaquette Haar moment, independent of all other links.
This removes the plaquette and factorizes the moment. Such terms cannot
produce a connected cumulant with other distinct plaquettes. A nonlocal
connected degree-six support therefore has six distinct squares, each once,
and is a cube. Every cube edge has two insertions, hence Haar survival forces
opposite orientations. No triple-link invariant occurs at degree six on that
support. Branched invariant networks may appear at later orders; this
argument makes no all-orders mod-2 assertion.

## Charged hopping / photon coefficient

Here D_f=1-kappa H_f is EXACTLY the graph matrix in the task: one-component,
integer determinant power for each supplied flavor, forward eta_mu U exp(i e
q_f A), reverse minus its Hermitian conjugate. There is no assumed continuum
spin connection or admitted four-dimensional spinor/taste interpretation.
The ambient-coordinate eta product around any coordinate square is -1.
The two reverse steps have positive product. Thus the nonbacktracking
plaquette part of Tr H_f^4 is
-4[Tr U_p exp(i e q_f F_p)+Tr U_p^dagger exp(-i e q_f F_p)].
The 1/4 in log det gives +kappa^4 times the bracket in log det.
The two-point Haar identity integral Tr U Tr U^dagger=1 then gives

  [beta kappa^4] log Z(A) = (1/3) sum_f sum_p w_p cos(e q_f F_p).

Let u=e^2, d=d1, W=diag(w_p)>0, L=d^T W d, and remove the gauge/null
space with a photon normalization independent of u. Its covariance on exact
field strengths is C=d L^+ d^T. Photon integration of the cosine is
exp(-u q_f^2 C_pp/2). Therefore the unconditioned full W=-log Z obeys

  [u beta kappa^4] W = (sum_f q_f^2)/6 * sum_p w_p C_pp
                     = (sum_f q_f^2)/6 * rank(d1)
                     = (sum_f q_f^2)/6 * (30n^4+20n^2-1).

Equivalently P=W^(1/2)d L^+ d^T W^(1/2) is the orthogonal projector onto
im(W^(1/2)d), and tr P=rank d. The rank follows from H1(K_n;R)=0 and
connectedness: rank d1=N1-N0+1. At n=1 it is 49. For unit weights, C=P.
At beta=0 the charged plaquette has zero color mean, so the displayed
charged response requires the mixed beta term. A pure-gauge Wilson log Z
coefficient is not this electromagnetic response.

The derivative of the determinant must preserve both current-current and
contact/seagull terms. Expanding the complete gauge-invariant loop cosine
already includes their sum; adding a separate contact term double-counts.
One cannot insert a flat-space Wilson spin trace into this graph definition.
An integer number of these determinants is well-defined; a physical taste
root, curved Dirac operator, or continuum light-flavor identification requires
separate input and cannot be inferred here.

## Scope pinned before target exposure

These statements concern a fixed, finite cubical complex with positive photon
weights, normalized Gaussian gauge removal, strong color coupling and a
convergent heavy-hopping expansion where justified. A Taylor coefficient is
exact as a formal derivative on this fixed model. It supplies neither a
continuum QCD limit nor physical light-quark vacuum polarization without a
controlled continuum/renormalization/mass/geometry bridge. The polyhedral
boundary has curvature concentrated on strata and is not automatically a
smooth round S4. A finite-order correction, even with a local remainder bound,
cannot establish a global no-go theorem for an arbitrary all-orders physical
A, nor evaluate physical A, R, or alpha.

External source authentication and the author code/range/remainder audit remain
to be performed. The arguments above are independent analytic derivations;
their numerical constants have not yet been checked by execution.
