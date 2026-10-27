# Compact-surplus checkpoint CS-20261022

Base Git ee621a0898f98a9f4e2200b3daa5cf7f11c4ee5a; predecessor reciprocal_field_2026_10_22. Owner: this chat; write scope: this directory. Original target (dwarfs + clusters + growth + rotation from one action) remains open. This checkpoint supersedes “compact exterior untested,” not the canonical theory or unrelated work.

Read RESULT.md and AUDIT.md. Main new information:
- 16 cold core interiors match to decaying vacuum polarization. The cold edge is a finite density jump, centre an integrable cusp. No stability or smooth-boundary completion has been proved.
- Vacuum has e>0 but rho_c=0 because div P=-e. Old positive-surplus radius language must be restricted to the occupied equations. The actual cold edge lies before their first zero.
- Total cold mass M0 x²y (subtract baryons when present); M0=a0 ell0²/G. Cold mass is a free conserved inventory, not selected by matching.
- Conditional exterior lensing DeltaSigma=Mc/(pi R²); no independent polarization Poisson source.
- One fitted compact dwarf core: canonical Mc=1.095e7 solar masses, edge321.5pc; alternate9.250e6,293.0pc. Generous law-plus-core summary statistics survive dwarf and rotating-dwarf checks. This addition is NOT a global nonlinear action solution.
- Cached cluster test: centred compact mass fitted to MID badly overpredicts INNER. Even preserving PL baseline, common5.028e13 solar masses gives INNER observed/model .329 and OUTER .833. Gas scaling does not repair it. Actual PN+core performs worse.
- Homogeneous-fluid growth benchmark unchanged by parameter choice; core formation/collective response uncomputed. Compact-only vacuum exterior is Keplerian, not an extended flat-curve halo.

Route dispositions:
1. Central compact core as cluster excess: fails the scoped canonical, centred shape diagnostic for common/gas-scaled mass. Retuning the unresolved interior cannot change its point-mass exterior. Do not repeat that fit unchanged.
2. Compact dwarf component: survives conditional compatibility, unselected and stability unproved. Next physical discriminator is a fixed-inventory core embedded in an occupied extended halo with dynamical baryons; superposition is not available. Must derive interface/environment matching anew, not reuse vacuum exterior in a halo.
3. Extended population of moving compact cores: open, deferred because it requires a kinetic/distribution and formation model absent from this action reduction. It changes the spatial premise of the cluster test. Needed: derive conserved core inventory, distribution, transport/capture and collective cosmological response from one model before fitting a cluster-only profile. Could behave as conventional clumped cold matter; that does not itself derive the galaxy law.
4. Finite-gradient regularization, stability spectrum and metric completion: open. Need a smooth interface/centre and radial/nonradial stability at fixed mass; positive field energy alone is insufficient. Lensing is conditional until a second metric potential and photon coupling are supplied.

Reproduce from repo root:
    python3 sol61_push/compact_surplus_2026_10_22/checks.py --output /tmp/compact_checks.json
    python3 sol61_push/compact_surplus_2026_10_22/cluster_checks.py --output /tmp/compact_cluster.json
    python3 sol61_push/compact_surplus_2026_10_22/dwarf_checks.py --output /tmp/compact_dwarf.json
    MPLCONFIGDIR=/tmp/compact_surplus_mpl python3 sol61_push/compact_surplus_2026_10_22/plot.py
Use bounded runner contracts for provenance. Current runs: run, cluster_run, dwarf_run2. dwarf_run is historical failed-count evidence, not current-source evidence. No running jobs remain. Inputs/results/derivations are indexed by CHECKPOINT_SHA256.json. Self-review only.
