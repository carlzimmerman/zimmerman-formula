# Checkpoint: fixed-coupling stability across four scale references

2026-09-30, 10:28 UTC pass. Parent: [stage fifteen](../stage_15/README.md).
FGF030 replaces the rescaled illustrative family of FGF027 with one fixed set
of physical couplings, initial data and interval length. It proves a uniform
conditional stability result for the diagnostic Q wall model. The physical
gravity theory and its empirical adequacy remain open.

## What is held fixed and what changes

Anchor a_c=9.3619e-11 m/s², c_s=10^6 m/s and L_c=c_s²/a_c.
Hold J=c_s^4, S0=a_c², K=c²/c_s², v_chi=c_s, the left physical source
flux/density/scale data, and the full length L_c/100 fixed. The only changing
reference is a_ref: either registered a0, or that a0 times E(1), where
E(1)²=641/200. The physical clock and field units remain anchored at a_c.

In these units the local constitutive scale is a=alpha exp(chi), with
alpha=a_ref/a_c. All four choices lie in [1,11/5]. They are four separate
stationary comparisons, including two frozen-H references. This does not
evolve the system between redshifts or identify different vacuum densities.
Right wall values and background mass are induced by each solution and need
not match between members. Perturbations conserve mass within each member.

## Checked continuum statement

An analytic compact-box argument encloses the full hydrostatic IVP through
D=.01 for every alpha in [1,11/5], not merely the four listed choices.
Every solution reaches its first scale-gradient turn before the same fixed
physical endpoint. The worker's common turn bracket is (1/23000,1/250),
and its remaining post-turn length exceeds 3/500, in anchor length units.
Root's separately derived bracket is (1/22700,1/190). Both are enclosures;
neither gives the individual turn locations or says those locations coincide.

The original coupled fluid, scalar-potential and scale quadratic forms are
retained, including both field kinetic terms and the fixed-wall boundary
conditions. Root obtains

    Q2 >= (2/5)||u'||² - 11||u||²,
    inf Q2/N >= 359890/11 > 32700.

Thus a common physical squared-frequency lower bound is

    omega_min² >= (359890/11)(a_c/c_s)²
               = 2.86751098279e-28 s^-2 (rounded).

The author's independently chosen coarse bounds give 224850/11 > 20400
in the same dimensionless units. Root's stronger estimate uses sharper
constitutive derivative bounds. These are compatible sufficient bounds,
not competing measured spectra. The shared physical factor is (a_c/c_s)²
for all cases; using a_ref in that factor would change the fixed clock.

## Evidence and limits

The author and root each chose their coefficient bounds independently before
reading the other's new derivation. A separate auditor froze the fixed-unit
derivation before inspecting those proofs. Another agent audited root's full
argument and code. Two bounded exact-rational certificates check arithmetic;
the analytic enclosure and energy arguments establish the continuum claim.
No ODE orbit, mesh eigenvalues or empirical likelihood was produced.

The alpha=1 equations recover the earlier anchor case. Negative controls
reject setting alpha=1 for the other references, retuning S0 to a_ref²,
changing the length/time units, overspending derivative stiffness and dropping
boundary terms outside the stated domain. Failure of the large-domain
sufficient bound is not a physical instability finding.

This remains a strong short-domain, fixed-wall result with chosen parameters.
It does not justify those parameters, arbitrary boundary data, free surfaces,
nonlinear or three-dimensional stability, RAR/M extension, filtered MONO,
physical metric/photon coupling or the required gravitational degree count.
Actual local a still varies, so literal constant-vacuum identification remains
unresolved. MOND source flux is retained; no missing-mass calculation is made.

- [Root uniform proof](fixed_units/ROOT_DERIVATION.md)
- [Root rational certificate](fixed_units/run_001/results.json)
- [Root proof audit](fixed_units/INDEPENDENT_AUDIT.md)
- [Independent unit and worker audit](independent_audit/INDEPENDENT_AUDIT.md)
- [Scoped reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-030_RECONCILIATION.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)

FGF032 next addresses the exact energy accounting if a stationary reference
is replaced by a prescribed time-dependent one. It must distinguish a genuine
change in the action from a mere change of scale-field coordinates and preserve
the previously recorded H-history obstruction. FGF031 remains ready for a
conditional instrument-response error certificate. No more stable short-slab
examples are needed on the unchanged premise. AS228 repair remains with its
primary owner; no completed physical metric repair is inferred.
