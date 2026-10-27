# Focused review of the charge-even NR current addendum

Target: `../density_duality/EMERGENT_POSITIVE_CURRENT.md`, final SHA-256
`69dc1d9495e7ee7cd6a9733efc2ddc63e75750f8f0a2864843be46cb273023e1`.
Scope: A1–A11 normalization, symmetries, conversion signs, two-current dual
and the process table/number-defect hierarchy. This does not review a
hard-loss rate or certify an actual population/relaxation hierarchy.

Normalized claim: the *specified conservative canonical four-envelope NR
theory* has two positive weighted constituent-number currents. Their sum
supplies a positive charge-even reference density, even when their
difference vanishes. Applying this approximate conservation to the full
relativistic theory requires the separately stated control of discarded
terms and real hard-mode number loss.

Primary verdict: **proved as written**, within the stated retained NR
theory and conditional application domain. No remaining actionable issue
was found after the source-frequency clarification described below. This
is a restricted conservation/duality construction, not proof that the full
microscopic neutral bath has an exact positive conserved mass current.

1. **A1–A2 order of reduction.** Independently expanding the direct 2m
   source carrier gives symplectic coefficient `2m/M` and mass term
   `-(M²-4m²)|b|²/(2M)`. The earlier implicit direct-substitution reading
   was therefore insufficient. The final text now first reduces at the
   physical frequencies ±M, then makes `beta=exp(i delta t)b`, producing
   the canonical symplectic term minus `delta |b|²`. Its stated discarded
   remainder is exactly `|dot b+i delta b|²/(2M)`. Expansion of this square
   recovers both the `-delta/M` symplectic change and `+delta²/(2M)` mass
   correction. The root independently identified this issue; this reviewer
   reconstructed it separately before reading the final correction.

2. **A3–A6 coefficients and signs.** Time averaging the quartic gives
   `lambda_tot(n_+²+n_-²+4n_+n_-)/(4m²)`. The retained cubic coefficient is
   `g/(2m sqrt(2M))`. Independent angles act with constituent weights one
   and two; the original signed symmetry is the opposite-angle subgroup.
   The Schrödinger equations give exactly `dot n+div j=2R` and
   `dot nb+div jb=-R` with the displayed
   `R=2c3 Im(b psi*²)`. Thus each `n+2nb` is conserved in this retained
   theory. The equal-angle sum is an emergent envelope symmetry, not an
   additional exact local transformation of the original Phi/X fields.

3. **A7–A8 dictionary.** Algebraically
   `rho_rest=m J_N^0+delta(nb+ + nb-)`; the residue's continuity source is
   `-delta(R+ + R-)`. The bound `delta nb_total/rho_rest≤delta/M` is exact
   for the *canonical NR quasiparticle rest-population inventory*, since
   `rho_rest≥M nb_total`. It is not a bound on complete relativistic
   gravitational density accuracy. The final paragraph explicitly states
   this limitation and warns that omitted soft-frequency, kinetic and
   interaction corrections can exceed `1.9994e-4`.

4. **A9–A11 flux dual.** Varying J gives
   `J-2ell=n grad theta/m`. Varying ell then gives
   `ell=nb(2grad theta+grad chi)/M`. Substitution recovers both physical
   phase-gradient energies and their canonical time terms. Varying each
   theta gives its own continuity equation. The two-form component
   normalization consequently gives
   `m(J_+^0+J_-^0)=div[m epsilon(B_++B_-)/2]`. Positive phase-chart domains,
   relative conversion phases and counterflow are retained. No one-fluid
   reduction is inferred from the sum alone. Independent two-form gauge
   freedom still prevents assigning a bare local W of their summed dual
   potential without new physical matching.

5. **Hard-loss table and hierarchy.** Full weighted-count changes are
   correctly `-2,-2,-4` for the three displayed processes. If the daughters
   are hard and excluded from the envelope inventory, every displayed
   soft-count change is `-4`. At source-pair threshold outgoing daughter
   energy M and momentum `sqrt(M²-m²)` follow from two-body kinematics.
   The two-source channel is a density-quadratic process, so dilution alone
   does not suppress it relative to another two-body rate. The addendum
   explicitly requires a computed state-dependent defect bound, keeps
   signed-charge/energy receivers, and claims no established hierarchy.

Evidence/provenance: inspected the displayed derivation and finite
15-assertion scope, and ran the documented validator on
`../density_duality/run_emergent_001/manifest.json`; it returned a valid
completed evidence record. No new numerical run was needed. Separate
reviewer and author share model/project context; agreement does not itself
prove the algebra or establish external physical evidence. The main
exchange report and previously audited current-duality note were unchanged.
