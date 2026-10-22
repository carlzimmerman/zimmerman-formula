# Failed estimates and excluded extrapolations

These are failures of estimates or scope, not counterexamples to the coupled
compression problem. The successful local construction is in DERIVATION.md.

1. **Retaining the entire fast packet in a global speed estimate.** The full
   packet gives speed O(N). Over an edge time N^-7/2 the corresponding
   conservative displacement is O(N^-5/2), exceeding the edge buffer
   O(N^-7/2) by O(N). It cannot protect these strips. The successful route
   constructs an auxiliary bounded extension that agrees on the outer strip,
   then proves one-sided characteristic uniqueness against any classical
   whole branch. Simply deleting the core without that argument would fail.

2. **Importing FGF048's coefficient or time.** An existing kappa N^-4 lower
   bound says nothing about B_* N^-4 when B_*>kappa. The altered local norms
   are essential: A0=O(P), H0=O(P^2), P=N^7/2, giving a new k_edge/P time.
   No substitution kappa:=B_* is made.

3. **Using the Lipschitz seminorm as the lifespan denominator.** A crude
   estimate t<=const/H0 gives N^-7 and fails to reach N^-4. The complete
   derivative-Lipschitz estimate is linear in H, with growth coefficient
   O(P), so H<=C P^2 on k/P. A generic finite-N start may be much shorter;
   endpoint traces/restarts extend it through the uniform interval.

4. **Dropping pressure or dividing through a speed gap.** Global
   |v-b|>delta is false at the stated initial roots; acoustic gaps also
   vanish. Momentum yields r,s transport with fixed sound speed and force,
   not a density-free pressureless evolution. The proof uses neither
   reciprocal gap nor frozen Q fields, so these obstructions do not enter.

5. **Claiming vanishing force-gradient change at the entire edge horizon.**
   The derived bound is O(theta+P^2 theta^2). At theta=k/P its second term
   is O(k^2), not o_N(1). At theta=B_* N^-4 it is O(N^-1). The shorter
   comparison time supplies the sharper asymptotic, and the two statements
   are kept distinct.

6. **Claiming all acoustic coincidences lie in edge strips.** Within the
   positive-velocity packet, all initial intersections have
   v in {b,b+c,b-c,c-b} with positive RHS and are covered. However v=0 and
   b0=c in the exterior is also an acoustic coincidence and need not occur
   near either edge. The background hypotheses do not exclude it. The
   theorem explicitly covers the guaranteed v=b and v=b+c roots and every
   positive-velocity initial packet root, retaining this exterior exception.

7. **Promoting local budgets to a full-cone supremum.** Two strips cover
   only a small part of the original cone. The actual bound
   integral sup_edge(-g_x)_+=O(N^-4) does not estimate the omitted core or
   newly formed resonance locations. No sum of two edge suprema bounds a
   supremum over an uncovered domain. Full matching remains a separate gap.

No mathematical executable experiment failed; none was run. Administrative
hash/JSON verification is separate from the proof.
