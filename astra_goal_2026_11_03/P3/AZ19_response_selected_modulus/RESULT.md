# AZ19 — FAIL response-driven normalization selection

κ = ½ FITTED; not theory closed

This is a new candidate mechanism test, not a rerun of PD07 or the old symmetry audit: allow the response action itself to stabilize a dynamical b, without a hand-selected restoring potential. The mechanism fails its necessary local equilibrium test. Both footings give the same symbolic conclusion; no numerical density or measured acceleration normalization was used.

## Equations and physical outcome

For E=(1-chi²)g²+s²U(chi)/b², U=2ln chi-4chi+chi²+C, simultaneous stationary variation gives

E_chi=-2chi g²+s²U'(chi)/b²=0,
E_b=-2s²U(chi)/b³=0,
U'=2(1-chi)²/chi.

On0<chi<1, the first equation yields chi=s/(s+bg). The second imposes U(chi)=0. Because U is strictly increasing on this interval, its root chi_C is fixed by the unselected vacuum constant C, independent of g. Such a root exists precisely for C>3: U tends to negative infinity at zero, and U(1)=C-3. Consequently

b_star(g)=s(1-chi_C)/(chi_C g),
mu_star=1-chi_C².

The selected b depends inversely on the local source acceleration. Eliminating both stationary variables leaves a constant mu, so the response has a rescaled Newtonian coupling rather than the required low-acceleration nonlinear law. Changing C selects a different constant response; it does not restore a universal physical b. This is not a scan over C or a fit to a desired value.

At C=3 the root is chi=1, incompatible with g>0 and finite positive b. At C<3 no physical root exists. In the g=0 vacuum limit, chi=1 and finite stationary b requires C=3; then the potential is flat in b, so every positive b remains allowed. The mechanism therefore fails both the vacuum selector and the nonzero-source universal-normalization requirement. No positive kinetic coefficient Zb changes these constant-patch stationarity equations.

## Stability distinction

Do not reject the source branch merely because the full (chi,b) Hessian is indefinite: chi is auxiliary, not a propagating mode in this candidate. On the joint branch,

E_chichi=-4s²(1-chi)/(b²chi²), E_bb=0,
E_bb-E_bchi²/E_chichi=4s²(1-chi)³/b⁴>0.

Thus, with positive b kinetic term and chi constrained, the local reduced b potential has positive curvature. The failure is not failure to find an attractive stationary response: its stable value is environment dependent and destroys the desired force law. Full covariant/dynamical stability is not established by this reduced curvature.

## Verification and scope

All ten symbolic/formal controls pass. Sympy checks the unreduced variations, the chi branch, the reduced-derivative chain rule, monotonicity and Schur curvature. The omitted-b-variation MUTATE is detected because d(E_b)/dC=-2s²/b³ is nonzero. Lean certifies exact rational branch witnesses with the same s,t but different source g and different b; holding b fixed after changing the source is rejected. Four accepted theorems print only standard Lean axioms. The formal scope is these branch controls, not a fully formalized variational or cosmological proof.

The first Lean invocation could not synthesize decidability through an opaque Prop definition and the initial result is preserved as NO VERDICT in initial_results.json with initial_Certificate.lean/log. Replacing the definition by a transparent abbreviation fixes elaboration without changing its proposition. The final accepted log has no sorryAx. Criteria and physical equations were not changed.

No physical kappa was derived. C and Zb remain unspecified/FITTED if assigned; no target-centered potential, new particle species or cold sector was adopted. Spatial-gradient, nonlocal or time-dependent mechanisms are not excluded by this local test. A successful next mechanism must select the physical normalization in the vacuum while resisting source-induced displacement; simply making the existing constant dynamical does neither. Source-independent stabilization must follow from additional justified dynamics, not an inserted minimum at1. Nothing has been pushed.
