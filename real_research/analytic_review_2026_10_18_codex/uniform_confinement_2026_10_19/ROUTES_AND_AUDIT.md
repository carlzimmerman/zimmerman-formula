# Confinement routes and the remaining propagation problem

19 October 2026. Checkpoint ZAR-2026-10-19-06. Parent checkpoint ZAR-2026-10-19-05. The Git HEAD observed when this work began was cae9f37df33fa8860c3cfa99ad682d366b11ad8b. Concurrent work may advance HEAD; ancestry and inputs are pinned separately in CHECKPOINT.json. No commit or old artifact is changed by this checkpoint.

## Target and evidence contract

The target is one finite time-independent radius containing the entire perturbed halo, retaining the same equations, nonlinear radial stability, controlled law and nonzero radial dispersion. A solution conditional on an explicit all-time work or launch estimate is useful but does not establish propagation of that estimate from initial data. A condition identical to assuming bounded support is not counted as a new initial-data theorem. No global weakest condition can be asserted merely by choosing one sufficient certificate.

The existing open perturbation class admits actual smooth canonical escape. The present work does not rerun that failed unrestricted theorem. It asks which weaker support-level information would close the characteristic proof, and which part of that information can be obtained from conserved masses and the established Lyapunov norm.

| Claim | Exact result | Evidence |
|---|---|---|
| ZAR-C1 | Common negative outgoing launch margin gives explicit all-time support bound; target-R sufficient and necessary caps form a quantified sandwich | EXTERIOR_LAUNCH_CRITERION.md; conditional on N2/N3 and the stated launch hypothesis |
| ZAR-C2 | Signed characteristic potential work gives exact criterion for a maintained negative energy gap; current-only positive-work budget suffices | BINDING_WORK_AND_CURRENTS.md; exact identity and conditional confinement theorem |
| ZAR-C3 | A finite boundary is certified by a strictly smaller relative-potential work budget using currents only inside it | BINDING_WORK_AND_CURRENTS.md; individual first-hit argument |
| ZAR-C4 | Confinement restrictions preserve old stability/law/pressure bounds; fixed-resolution dispersion has an all-time positive lower bound | WARMTH_AND_SCOPE.md; named N2/N3/N4 inputs and direct moment inequalities |
| ZAR-C5 | Arbitrarily small time-dependent Kepler force error can pump a fixed initially bound tracer to escape | Exact prescribed-field construction below; not a self-consistent Vlasov counterexample |

## Three executed routes

The energy-work route began with a negative actual-energy gap. Its uncertain implication was whether initial binding propagates. The exact derivative dE/dt=partial_t Phi shows the needed work term. Signed characteristic work below the reserve proves the claim; positive Eulerian work supplies a stronger scalar certificate. Relative potential work improves this for a selected finite boundary. The conditional theorem is complete, but its initial-data propagation leaf is open.

The current route derives partial_t Phi from partial_t M=-j, retaining the tethered/free cancellation. The old Lyapunov norm bounds each work rate by C epsilon. Integrating only gives C epsilon t. Fixed-radius current primitives are bounded by continuity, but particles move between radii, so that observation does not control their accumulated work. This route establishes a precise missing estimate rather than an all-time propagation theorem.

The exterior support route uses the small total exterior mass supplied by nonlinear stability to make two autonomous cubic comparison potentials. A large fixed sphere has strictly inward radial acceleration outside it, so every possible new outer excursion is checked at an outward passage. This gives an explicit uniform bound, a necessary comparison threshold and an O(epsilon) uncertainty between them. It avoids imposing an energy bound throughout the core, but recurrent launch speeds remain a dynamical hypothesis.

No fourth invariant compact nonstationary class has been established by the shell theorem or the force bounds. Stationary equilibria satisfy the work conditions and retain warmth, but that does not provide a nonstationary neighborhood. Homologous breathing is not derived: point attraction, mass-dependent attraction, angular momentum and cubic response scale differently. No special pulsating ansatz is used as a proof leaf.

## Why a small force error does not bound accumulated work

Consider only the prescribed tracer equation

\[
\ddot r=L/r^3-k(t)/r^2,\qquad
k_\pm=k_0\pm\delta,\quad0<\delta<k_0/4.
\]

Start at p_0=L/k_0, v=0. Use k_- on outward legs and k_+ on inward legs, switching at each turning point. The first acceleration is outward and the initial instantaneous energy is

\[
E_{\rm in}=-k_0^2/(2L)+\delta k_0/L
\le-k_0^2/(4L).
\]

The initial binding gap is fixed independently of how small delta is. A Kepler leg with pericenter p_n and apocenter a_n satisfies the turning-point identity

\[
1/a_n=2k_-/L-1/p_n.
\]

After switching to the stronger inward force, the next pericenter obeys

\[
\boxed{1/p_{n+1}=1/p_n+4\delta/L.}
\tag{29}
\]

Choose delta away from the isolated values giving exact equality at the escape threshold. After finitely many cycles, 1/p_n>2k_-/L, and the next weak-force outward leg has positive Kepler energy. Freeze k=k_- thereafter; that particle escapes. All preceding pericenters remain above L/(2k_+), and |a(t,r)-a_ref(r)|<=delta/r^2. The finitely many switches can be smoothed in time: on a finite interval reaching a strictly positive final outgoing energy, continuous dependence on the bounded force perturbation follows from the ordinary characteristic Gronwall estimate away from r=0. The final positive energy persists and the later static weak force gives escape.

This is a prescribed-field example. Its source does not solve the two-population kinetic equations. It refutes a propagation argument relying only on the initial gap and uniform force error; it does not refute confinement for uniformly initially bound, sufficiently small canonical perturbations in the actual self-consistent model.

There is also an exact self-consistent local check: a small outward canonical shear has j_i(0,r)=alpha chi(r)mu_i^0(r)>=0, while the initial energy gap survives for small alpha. Equation (11) then gives partial_t Phi_f>0 below the sheared layer. Thus individual energies can increase even in that initially bound class. This proves failure of energy conservation, not eventual escape or failure of every smaller maintained gap.

## Scope and next mathematical step

The user-requested all-time confinement is now proved under either the explicit recurring launch hypothesis or one of the stated accumulated-work hypotheses. Finding a globally weakest initial-data condition, or deriving those dynamical hypotheses for a nonstationary initial neighborhood, remains open. This distinction is retained in the theorem statements and README.

The next substantive route is a self-consistent bound on the signed orbit-to-orbit energy transfer at the outgoing sphere, preferably allowing cancellation rather than absolute current integrability. An orbital normal form or a propagated phase-space barrier would have to control the resonant secular term uniformly over the occupied L and energy range, including the flat outer cutoff. A mere assumption of damping, nonresonance, initial evenness, or small canonical maps is not a proved input. Those continuations are deferred with this specific missing implication; the route is open, not exhausted or refuted.

The old escape construction does not settle the uniform-initial-gap subclass. The prescribed pump does not settle it either. Conversely, adding a maintained negative gap without proving its propagation is a conditional theorem, not a completed initial-data proof. Exact density-law preservation and an all-time pointwise dispersion floor also remain distinct from the controlled cumulative law and fixed-resolution warmth proved here.

## Review provenance

Three read-only route agents independently developed the work, current and exterior/invariant alternatives from checkpoint 05. Their returned input hashes match NONLINEAR_FLOW.md and LAW_DISPERSION_BOUNDARY.md. Their conclusions were reconciled by direct characteristic and current derivations in this checkpoint; agent agreement is not treated as proof evidence.

The final artifact reviews and exact reviewed hashes are recorded in CHECKPOINT.json. The proof leaves are the displayed internal derivations and named earlier results. No external confinement theorem, scientific calculation or empirical inference is used. A separate proofreading pass is confined to the five new Markdown artifacts.

Only the new uniform_confinement_2026_10_19 directory is writable scope for this work. Claude's jobs, processes, calculations, prior checkpoints and other concurrently edited files are not inspected or changed.
