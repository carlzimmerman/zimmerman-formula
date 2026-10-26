# Continue the physical join, not a galaxy claim

Start with README.md, DERIVATION.md, AUDIT.md and run_audit/results.json.
No physical DR rates, branching, photon trajectory or galaxy separation yet.

Resolved: signed pure-target Q CSFs can be decoded from CONGEN and original
Molden orbitals. `qmap.load` returns mol,C,ci; `transform` maps them into the
larger nuclear electronic basis. Elementwise H checks confirm relative signs.
This is stronger than the previous eigenvalue-only comparison. The old capture
space embeds exactly but remains physically incomplete.

Resolved in part: fourth-order neutral propagation, paired-site coupled lead,
and fixed inner wall substantially improve mesh behavior. The old Rmin=.5 wall
contaminated small inelastic probabilities. Deeper-wall .1/.05 checks agree much
better. Electronic basis and exterior still need convergence; do not recycle
neutral reflection probabilities as recombination.

New backend `feshbach_v2.eliminate(E,Hp,V,B,L)` computes Sigma and source from one
retarded P resolvent. The executed physical-input test includes nuclear motion
only in an explicitly separable frozen-R2 Hamiltonian, four bound ionic modes.
Its open thresholds differ from a local electronic-width approximation. It has
no nuclear product continuum, so cannot give DR. Keep this exact distinction.

Next substantive work:
1. Recover/generate P electronic overlap matrices across R, including the
   orthogonalized B-spline continuum and target orbitals. Q mapping is now solved;
   P mapping and relative entrance-channel phase still are not. Do not use identity
   P overlap merely because dimensions match. UKRmol orbital transformation data
   may allow this; inspect source/GBTO data rather than inventing it.
2. Generate capture in a compatible diffuse basis and sufficient R/E grid. Original
   template assumes target counts [5,2,2,0,5,2,2,0], eighteen target states and
   Qdim42. A larger basis requires consistent CONGEN shells, target SCATCI counts,
   DENPROP lists, scattering ntgtf/ntgts and SWINTERF energy-order mapping. Also
   check diffuse-target tails at the electron boundary; radius20 may not suffice.
3. Put nuclear kinetic/overlap terms inside the global P resolvent. Keep real shifts,
   closed ionic states, open ionic dissociation above threshold, and source phase.
   Use the existing Schur/backend checks; add product-lead flux. Full geometry
   dependence is the missing step beyond the frozen benchmark.
4. Resolve radial/electronic/exterior/rotational/finite-mass convergence and assign
   actual atomic product states, then thermal rates and inverse detailed balance.
5. Only then feed product-resolved rates into spectral photons. Present photon
   conservation checks are specified-event tests, not a physical trajectory.

Source: PRA109052806(2024), verified again during this stage. Its nonlocal
rovibrational kernel motivates a method; its HD+ rates are not our mass100 data.
No new phenomenological physical parameter or galaxy-type switch was added.
