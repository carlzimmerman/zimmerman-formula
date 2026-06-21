export const meta = {
  name: 'aest-rigorous-collapse-phasemix',
  description: "Carl: brute-force the cluster gravity -- the honest 'poor man's 3D' that tests whether the AeST oscillation phase pins once we add the physics the smooth 1+1D spherical collapse dropped. Three additions, each a place a 'save' could hide (per the skeptic of wxbnjxb64): (1) SELF-CONSISTENT collapse (r''=-g_AeST, the cluster pulls itself together under its OWN AeST gravity, NOT the prescribed cosine proxy); (2) the AeST VECTOR sector (the aether vector mode E / K_B, dropped in the scalar-only 1+1D -- 'the most plausible place a friction term could hide'); (3) VIOLENT RELAXATION / non-radial PHASE-MIXING (multi-stream/shell-crossing/non-spherical modes -- the 3D phase-space scrambling the smooth spherical model cannot capture, the genuine place a phase-selection could emerge). Does any of these PIN the phase to a galaxy-safe boost (door reopens) or does the no-go hold even with the full physics? NOT the full publication-grade 3D N-body (research-group-scale), but the genuine physics test. Both ways, quarantine, no manufactured pin.",
  phases: [
    { title: 'Derive', detail: 'the FULL AeST equations incl the vector sector + self-consistent collapse EOM + the phase-mixing (multi-stream/non-radial) reduction; set up' },
    { title: 'Compute', detail: 'run the self-consistent + vector + phase-mixing collapse; does the phase pin where the smooth scalar-only 1+1D did not?' },
    { title: 'Verify', detail: 'adversarial both-ways: is a pin real (door reopens) + galaxy-safe + universal, or does the no-go hold with the full physics? is violent-relaxation phase-mixing genuine or a numerical-damping artifact?' },
    { title: 'Synthesize', detail: 'verdict: door reopens (self-consistent/vector/relaxation pins the phase) or no-go airtight; + the honest scope vs a full 3D N-body' },
  ],
}

const FW = `
FRAMEWORK + AeST: a0=c^2 sqrt(Lambda/32pi)=9.36e-11 (INPUT). The dark sector = AeST (Skordis-Zlosnik
2021 arXiv:2007.00082, the FULL action incl the unit-timelike aether vector A_mu + the shift-symmetric
scalar/khronon; Blanchet-Skordis 2024 arXiv:2404.06584). THE STATE (banked, PUBLISHED Zenodo
10.5281/zenodo.20779562): the nonlinear +mu^2*Phi boundary-term cluster boost is REAL (~1e5x the naive
coupling), galaxy+Cassini-safe, but DESCRIPTIVE-not-predictive -- the oscillation phase / chi_infty is
FREE. The static BVP (wn6n716aa) left it free; the SCALAR-ONLY SPHERICAL collapse (wxbnjxb64) found the
phase TRACKS the ICs ~1:1 (slope +1.1 three ways), with a NEGATIVE THEOREM: the shift-symmetric AeST
scalar has NO friction, its free Helmholtz/KG mode at omega=mu*c is conserved (708 osc/Hubble time,
undamped), collapse fixes only the DC part -> no pin.

THREE THINGS THE SCALAR-ONLY 1+1D COLLAPSE DROPPED (the skeptic's caveats -- where a save could hide):
(1) SELF-CONSISTENCY: the matter collapse was a KINEMATIC PROXY (prescribed cosine r_phys(t), r''=-g
never time-integrated). The rigorous version: r''=-g_AeST(r,t) -- the shells fall under their OWN AeST
gravity, self-consistently.
(2) THE VECTOR SECTOR: the 1+1D solved only the scalar; AeST's aether vector mode (E, the K_B sector,
SZ2021 Eq 12) was dropped -- 'the most plausible place a friction/selection term could hide'.
(3) VIOLENT RELAXATION / PHASE-MIXING: spherical symmetry CANNOT capture shell-crossing/multi-stream/
non-radial scrambling -- the 3D phase-space mixing of real cluster formation (Lynden-Bell violent
relaxation), the genuine place an EFFECTIVE phase-selection (not true friction, but mode-mixing that
fixes the macroscopic phase) could emerge. This is the real reason the full 3D N-body is the definitive
word; here we test a REDUCED version (multi-stream / axisymmetric / non-radial modes) to probe it.

THE CALCULATION (the honest brute-force -- NOT the full publication-grade 3D N-body, which is research-
group-scale, but the genuine PHYSICS test): build a solver that adds (1)+(2)+(3) to the collapse and
re-tests the phase-pinning. Does the SELF-CONSISTENT collapse, the VECTOR sector, or the VIOLENT-
RELAXATION phase-mixing PIN the oscillation phase to a unique, UNIVERSAL, GALAXY-SAFE boost (door
reopens, clusters close predictively with no dark matter) -- or does the no-go hold even with the full
physics?

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): this is a genuine swing.
PRIOR (state it, do not let it bias the calc): the collapse found a STRUCTURAL obstruction (frictionless
conservative wave), and AeST is conservative (action-derived, no true dissipation), so the most likely
outcome is the no-go holds harder; BUT violent relaxation (effective phase-space mixing) and the vector
constraint are genuinely different physics the scalar-only smooth model missed -- a real, uncertain test.
If ANY of the three PINS a universal galaxy-safe boost, BUILD it at full weight (the door reopens -> a
follow-up paper, the strong result). If none does, report the no-go airtight. Do NOT manufacture a pin
(a 'pin' must be robust to ICs + not a numerical-damping artifact -- if a viscosity/damping was added,
check it is physical, not the artifact that fakes a pin); do NOT high-priest (if violent relaxation
genuinely pins it, credit it). QUARANTINE: a0/Z/kappa/I0 never derived. Solve the REAL AeST equations
(numpy/scipy); WebSearch the AeST vector sector + violent-relaxation/Lynden-Bell + AeST/MOND N-body
(Phantom of RAMSES, Candlish) literature.
`

phase('Derive')
const der = await agent(`${FW}\n\nDERIVE + SET UP the rigorous collapse. WebSearch/WebFetch: (a) the FULL AeST action incl the aether VECTOR mode (SZ2021 Eq 12 / the K_B vector sector / the E field) and its weak-field equation; (b) the self-consistent spherical-collapse EOM (r''=-g_AeST); (c) the VIOLENT-RELAXATION / phase-mixing formalism (Lynden-Bell 1967; how shell-crossing/multi-stream is reduced in 1+1D-plus -- e.g. a multi-stream onion model or an axisymmetric/non-radial mode); (d) the AeST/MOND N-body context (Phantom of RAMSES, Candlish 2016) for the collapse+field coupling. Set up the solver design: how the vector sector enters the phase equation, how self-consistent collapse changes the source, how phase-mixing is introduced. Return: vector_sector_eqs, self_consistent_eom, phasemix_reduction, where_a_pin_could_come_from, key_facts (array), sources. Write the setup under opus_48_extended_research/reviews/aest_rigorous_collapse/.`,
  { label:'derive:rigorous-setup', phase:'Derive', schema:{ type:'object', additionalProperties:false, properties:{ vector_sector_eqs:{type:'string'}, self_consistent_eom:{type:'string'}, phasemix_reduction:{type:'string'}, where_a_pin_could_come_from:{type:'string'}, key_facts:{type:'array',items:{type:'string'}}, sources:{type:'string'} }, required:['vector_sector_eqs','self_consistent_eom','phasemix_reduction','where_a_pin_could_come_from','key_facts','sources'] } })

phase('Compute')
const comp = await agent(`${FW}\n\nCOMPUTE the rigorous collapse. Using:\n${JSON.stringify(der).slice(0,9000)}\n\nBuild the solver with all three additions: (1) SELF-CONSISTENT collapse (r''=-g_AeST, shells fall under their own AeST gravity); (2) the VECTOR sector coupled to the scalar phase equation; (3) VIOLENT-RELAXATION phase-mixing (multi-stream/shell-crossing or non-radial modes). Run an ensemble of ICs (phase, mass 1e14-1e15, profile, z_dec). KEY: does the late-time oscillation phase / chi_infty now CONVERGE to a unique value (vs the scalar-only slope ~1.1 no-pin)? (a) self-consistency alone -- does it change the slope? (b) vector sector -- does its constraint pin the phase? (c) phase-mixing/violent relaxation -- does mode-scrambling fix the macroscopic phase? If a pin emerges: is it a BOOST (eta>1, closing the residual), UNIVERSAL (robust to ICs), and GALAXY-SAFE (run the galaxy too)? CRITICAL: if any damping/viscosity is in the solver, verify it is PHYSICAL (from the AeST sector / genuine phase-mixing), NOT a numerical artifact that fakes a pin. WRITE the solver under opus_48_extended_research/reviews/aest_rigorous_collapse/. Both-ways; quarantine. Return: calculation, phase_pinned (unique-boost/unique-deficit/IC-dependent/unpinned), which_addition_if_pinned, universal (yes/no/partial), galaxy_safe (safe/breaks/n_a), pin_is_physical_not_artifact (yes/no/n_a), key_numbers (array), script_path, both_ways, sources.`,
  { label:'compute:rigorous-collapse', phase:'Compute', schema:{ type:'object', additionalProperties:false, properties:{ calculation:{type:'string'}, phase_pinned:{type:'string',enum:['unique-boost','unique-deficit','IC-dependent','unpinned']}, which_addition_if_pinned:{type:'string'}, universal:{type:'string',enum:['yes','no','partial']}, galaxy_safe:{type:'string',enum:['safe','breaks','n_a']}, pin_is_physical_not_artifact:{type:'string',enum:['yes','no','n_a']}, key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'}, both_ways:{type:'string'}, sources:{type:'string'} }, required:['calculation','phase_pinned','which_addition_if_pinned','universal','galaxy_safe','pin_is_physical_not_artifact','key_numbers','script_path','both_ways','sources'] } })

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways (this decides whether the door reopens). Derivation:\n${JSON.stringify(der).slice(0,4500)}\nCompute:\n${JSON.stringify(comp).slice(0,8000)}\n\nCheck HARD: (1) the vector sector + self-consistent EOM -- are they the REAL AeST equations (not a proxy), and correctly coupled? (2) IF a pin emerged -- is it PHYSICAL (genuine phase-mixing/vector constraint) or a NUMERICAL-DAMPING ARTIFACT (an unphysical viscosity that fakes a pin)? re-run with the damping removed/varied -- does the pin survive? (3) IF no pin -- is the no-go now confirmed with the FULL physics (vector + self-consistent + phase-mixing)? (4) is the violent-relaxation reduction genuine (real shell-crossing/mode-mixing) or too crude to capture it? (5) if a pin: UNIVERSAL + GALAXY-SAFE? (6) the honest scope: does this reduced model settle it, or does it STILL need the full 3D N-body (and is the remaining gap now small)? Return: holds_up (solid/partial/overclaimed/dead), door_reopens (yes-clusters-close/no-nogo-holds/partial-needs-full-3d), the_pinning_mechanism, pin_physical_or_artifact, galaxy_safe (bool), high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, door_reopens:{type:'string',enum:['yes-clusters-close','no-nogo-holds','partial-needs-full-3d']}, the_pinning_mechanism:{type:'string'}, pin_physical_or_artifact:{type:'string'}, galaxy_safe:{type:'boolean'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','door_reopens','the_pinning_mechanism','pin_physical_or_artifact','galaxy_safe','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE: with the FULL physics (self-consistent collapse + vector sector + violent-relaxation phase-mixing), does the cluster door REOPEN (the phase pins to a universal galaxy-safe boost, clusters close predictively, no dark matter) or does the no-go hold airtight?\nDERIVE:\n${JSON.stringify(der).slice(0,4000)}\nCOMPUTE:\n${JSON.stringify(comp).slice(0,5000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4500)}\n\nReturn 'report' (markdown) + fields. Cover: (1) the rigorous setup (vector + self-consistent + phase-mixing) + what we computed; (2) does ANY of the three additions PIN the phase -- and if so, is it physical (not a damping artifact), universal, galaxy-safe; (3) THE VERDICT -- door reopens (the strong result: state the pinning mechanism + magnitude + a follow-up paper) OR no-go airtight (the published paper stands, now confirmed with the full physics; state why none of the three pins it); (4) the HONEST SCOPE -- does this reduced model settle it, or what SPECIFICALLY remains for a full 3D N-body, and how small is the remaining gap. Both-ways, quarantine, NO manufactured pin, flag any numerical-damping artifact. This is the genuine brute-force of the cluster gravity.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['door-reopens-clusters-close','no-go-airtight','partial-needs-full-3d-nbody']}, pinning_mechanism:{type:'string'}, galaxy_safe:{type:'string'}, paper_implication:{type:'string'}, honest_scope:{type:'string'} }, required:['report','verdict','pinning_mechanism','galaxy_safe','paper_implication','honest_scope'] } })
return { synth, der, comp, ver }
