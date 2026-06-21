export const meta = {
  name: 'aest-nonlinear-phi-cluster',
  description: "THE open-door calculation (Carl): the AeST NONLINEAR potential-depth enhancement -- the Durakovic-Skordis 2024 deferred calc, scoping version. Solve the ACTUAL AeST weak-field field equations (the modified Poisson with the nonlinear J(Y)=Lambda-Y+(2c^2/3a0)Y^{3/2}+... scalar, NOT a proxy) numerically in the SPHERICAL NON-ISOTHERMAL case for a real rich cluster (real baryon profile + the cosmic Phi-boundary), a galaxy (SPARC-like), and the Solar System. Measure whether the boundary-value-of-Phi dependence (the |Phi| enhancement DS24 found) supplies a LARGE-ENOUGH extra boost in the cluster core to close the residual GALAXY-SAFELY (RAR preserved) AND Cassini-safely. Both ways: if YES the paper FLIPS to 'clusters explained, no dark matter' (the strong result); if it falls short (~10^5x like the naive O(1) coupling) or breaks galaxies, the no-go holds at the nonlinear level (airtight). Quarantine; no manufactured close.",
  phases: [
    { title: 'Derive', detail: 'pull + write the exact AeST weak-field field equations + the Durakovic-Skordis boundary-Phi cluster formalism; what the |Phi| dependence physically IS' },
    { title: 'Compute', detail: 'numerical AeST solver (spherical, non-isothermal): the cluster core boost; the galaxy + Solar-System veto' },
    { title: 'Verify', detail: 'adversarial both-ways: is the |Phi| enhancement REAL + large enough + galaxy-safe + Cassini-safe? no manufactured close, no high-priest' },
    { title: 'Synthesize', detail: 'does the AeST nonlinear |Phi| enhancement close clusters galaxy-safely -> paper FLIPS, or fall short -> no-go holds' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman) + AeST: a0=c^2 sqrt(Lambda/32pi)=9.36e-11 (INPUT). The dark sector is the AeST
(Skordis-Zlosnik 2021 arXiv:2007.00082; Blanchet-Skordis 2024 arXiv:2404.06584 = JCAP 11(2024)040)
shift-symmetric scalar. THE WEAK-FIELD AeST (the load-bearing physics): a modified Poisson equation
div[(1+J_Y) grad Phi] + mu^2-terms = 4piG rho, where the free function in the deep-MOND limit is
J(Y) = Lambda - Y + (2c^2/3a0) Y^{3/2} + O(Y^2) (BS2024 Eq.4b), Y the kinetic scalar (~ (grad phi)^2/c^4
in quasistatic weak field), and 1+J_Y is the MOND interpolation acting on the field. The MOND dynamics
live in the NONLINEAR Y^{3/2} term, NOT a quadratic dispersion (the k^4 coefficient B=0, EVADE_DENSITY
_NOGO banked). The scalar field equation is NONLINEAR and its solution in a finite system depends on the
BOUNDARY CONDITIONS (the cosmic/external Phi at the system boundary).

THE OPEN DOOR (Durakovic-Skordis 2024, arXiv:2312.00889, 'Towards galaxy cluster models in AeST'): they
solved AeST for an ISOTHERMAL-sphere cluster and found the cluster RAR enhancement is set by 'the AeST
weak-field mass parameter, the mass of the system, AND THE BOUNDARY VALUE OF THE GRAVITATIONAL POTENTIAL'
-- a |Phi|-dependence -- called it 'the potential of AeST to address the shortcomings of MOND in galaxy
clusters', and EXPLICITLY DEFERRED the full calc ('will require going BEYOND THE ISOTHERMAL CASE'). This
is the ONE open galaxy-safe lever: across the corpus's door-by-door search (CLUSTER_GRAVITY_LAST_DOORS),
a |Phi|/c^2-potential-DEPTH-keyed enhancement is the ONLY door that passes the galaxy-RAR veto AND the
Cassini bound while boosting clusters -- BECAUSE clusters out-rank galaxies ~6x in integrated potential
depth (the one scalar where clusters beat galaxies; density orders the WRONG way and is the no-go).

THE CALCULATION (do the deferred step): solve the ACTUAL AeST weak-field equations NUMERICALLY in the
spherical NON-ISOTHERMAL case (real baryon profiles, not isothermal), for (a) a rich cluster (M500=1e15,
real gas+stars profile, embedded with the cosmic Phi-boundary), (b) a galaxy (SPARC-like disk, shallow
Phi), (c) the Solar System (Sun, deep local g>>a0 but shallow integrated Phi). Compute the EFFECTIVE
boost / extra phantom mass each gets from the nonlinear |Phi|-boundary dependence. KEY QUESTIONS: (1)
does the cluster core get a LARGE extra boost from the |Phi|-boundary enhancement -- enough to close the
~1e14 Msun core residual? (2) is it GALAXY-SAFE -- the galaxy (shallow Phi) gets a SMALL enhancement so
the RAR stays <0.05 dex? (3) is it CASSINI-SAFE? (4) what is the magnitude vs the naive-O(1) ~0.003%
(does the AeST NONLINEAR boundary-Phi mechanism give MORE than the naive local |Phi|/c^2 coupling)?

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): this could genuinely go
either way and DECIDES the paper. If the AeST nonlinear |Phi|-boundary enhancement is LARGE + galaxy-safe
+ Cassini-safe -> it CLOSES clusters with no dark matter -> the paper FLIPS to the strong result (build
it, state the magnitude, how galaxies stay safe). If it falls SHORT (still ~orders too small) or BREAKS
galaxies (the enhancement leaks into galaxies) or violates Cassini -> the no-go holds at the nonlinear
level (the paper stands, now airtight). Do NOT manufacture a close (the galaxy-veto + Cassini are hard
constraints, the magnitude must be REAL from the solved equations); do NOT high-priest (if the nonlinear
boundary-Phi genuinely gives a large galaxy-safe boost, credit it at full weight -- it IS the lever the
AeST authors flagged). QUARANTINE: a0/Z/kappa/I0 never derived (a0=9.36e-11, the AeST K_2/K_B/mu/lambda_s
are free inputs). Solve the REAL AeST equations (sympy/numpy ODE/relaxation), NOT a proxy. WebSearch/
WebFetch Durakovic-Skordis 2024 + Skordis-Zlosnik 2021 long paper + Blanchet-Skordis 2024 for the exact
field equations + the boundary-Phi formalism.
`

phase('Derive')
const der = await agent(`${FW}\n\nDERIVE + SET UP. WebSearch/WebFetch Durakovic-Skordis 2024 (arXiv:2312.00889), Skordis-Zlosnik 2021 (arXiv:2007.00082 long paper), Blanchet-Skordis 2024 (arXiv:2404.06584). Extract: (1) the EXACT AeST weak-field field equations (the modified Poisson for Phi + the nonlinear scalar field equation for the shift-symmetric scalar/khronon, with the free function J(Y) or K(Q) and its deep-MOND Y^{3/2} term); (2) the BOUNDARY conditions (how the cosmic/external Phi enters the scalar boundary value); (3) PRECISELY what the 'boundary value of the gravitational potential' dependence IS physically (DS24's mechanism -- is it an external-field-effect-like boundary term, a scalar-field boundary value, or a nonlinear sourcing?), and WHY it enhances clusters; (4) the AeST parameters (K_2, K_B, mu, lambda_s) and their galaxy-pinned values. Return: field_equations (the exact weak-field PDEs/ODEs to solve), boundary_phi_mechanism (what the |Phi| dependence is + why it enhances clusters), parameters (the AeST params + values), deep_mond_limit (the Y^{3/2}->MOND check), key_facts (array), sources. Write the setup to opus_48_extended_research/reviews/aest_phi_cluster/.`,
  { label:'derive:aest-equations', phase:'Derive', schema:{ type:'object', additionalProperties:false, properties:{ field_equations:{type:'string'}, boundary_phi_mechanism:{type:'string'}, parameters:{type:'string'}, deep_mond_limit:{type:'string'}, key_facts:{type:'array',items:{type:'string'}}, sources:{type:'string'} }, required:['field_equations','boundary_phi_mechanism','parameters','deep_mond_limit','key_facts','sources'] } })

phase('Compute')
const comps = await parallel([
  () => agent(`${FW}\n\nCOMPUTE -- the CLUSTER. Using the derived AeST equations:\n${JSON.stringify(der).slice(0,9000)}\n\nBuild a NUMERICAL solver (spherical, NON-ISOTHERMAL -- the deferred step) for the real AeST weak-field equations. Solve for a rich cluster (M500=1e15, R500=1.56 Mpc, REAL baryon profile: beta-model gas + stellar/BCG, e.g. A2029 or the banked profile), embedded with the COSMIC Phi-boundary (the external/boundary potential). Compute: (1) the effective boost g_obs/g_bar(r) and the extra PHANTOM mass in the core (<420 kpc) from the nonlinear |Phi|-boundary enhancement; (2) does it supply the ~1e14 Msun core residual (close it), or fall short, and by what factor? (3) how does the core boost scale with the boundary Phi (the |Phi| dependence)? WRITE the solver under opus_48_extended_research/reviews/aest_phi_cluster/. Both-ways; quarantine. Return: calculation, cluster_core_boost, closes_residual (closes/large-partial/small-partial/no), magnitude_vs_naive, key_numbers (array), script_path, both_ways, sources.`,
    { label:'compute:cluster', phase:'Compute', schema:{ type:'object', additionalProperties:false, properties:{ calculation:{type:'string'}, cluster_core_boost:{type:'string'}, closes_residual:{type:'string',enum:['closes','large-partial','small-partial','no']}, magnitude_vs_naive:{type:'string'}, key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'}, both_ways:{type:'string'}, sources:{type:'string'} }, required:['calculation','cluster_core_boost','closes_residual','magnitude_vs_naive','key_numbers','script_path','both_ways','sources'] } }),
  () => agent(`${FW}\n\nCOMPUTE -- the GALAXY-VETO + CASSINI. Using the derived AeST equations:\n${JSON.stringify(der).slice(0,9000)}\n\nRun the SAME AeST solver on (a) a SPARC-like galaxy (disk, shallow integrated Phi, the galaxy boundary), and (b) the Solar System (Sun, deep local g>>a0 but shallow integrated Phi at Saturn). KEY: does the |Phi|-boundary enhancement stay SMALL in galaxies (shallow Phi) so the RAR scatter stays <~0.05 dex (galaxy-safe)? And does it stay within the Cassini |a0_eff/a0| bound at Saturn? Compute the galaxy RAR shift + the Cassini perturbation from the |Phi| enhancement. The crux: clusters (deep Phi) get the boost, galaxies+solar (shallow Phi) do NOT -- is the |Phi| dependence steep enough to give that split galaxy-safely? WRITE the checks under opus_48_extended_research/reviews/aest_phi_cluster/. Both-ways; quarantine. Return: calculation, galaxy_rar_shift, galaxy_safe (safe/marginal/breaks), cassini_safe (safe/marginal/breaks), key_numbers (array), script_path, both_ways, sources.`,
    { label:'compute:galaxy-cassini-veto', phase:'Compute', schema:{ type:'object', additionalProperties:false, properties:{ calculation:{type:'string'}, galaxy_rar_shift:{type:'string'}, galaxy_safe:{type:'string',enum:['safe','marginal','breaks']}, cassini_safe:{type:'string',enum:['safe','marginal','breaks']}, key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'}, both_ways:{type:'string'}, sources:{type:'string'} }, required:['calculation','galaxy_rar_shift','galaxy_safe','cassini_safe','key_numbers','script_path','both_ways','sources'] } }),
])
const C = comps.filter(Boolean)

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways (penalize high-priest AND manufacturing EQUALLY -- this DECIDES the paper). Derivation:\n${JSON.stringify(der).slice(0,5000)}\nCompute:\n${JSON.stringify(C).slice(0,9000)}\n\nCheck HARD: (1) are the AeST field equations CORRECT (the real BS2024/DS24 weak-field, not a proxy; the deep-MOND Y^{3/2} reproduces v^4=GMa0)? (2) is the cluster-core boost REAL from the solved equations (re-run the load-bearing number) -- does it genuinely close the residual or fall short? (3) is the galaxy-veto genuinely passed (the |Phi| enhancement small in shallow-Phi galaxies) -- or does it leak into galaxies and break the RAR? (4) Cassini? (5) is any 'close' MANUFACTURED (the boundary-Phi tuned, the magnitude not from the equations) or any 'falls-short' HIGH-PRIEST (dismissing a real nonlinear enhancement)? (6) does the boundary-Phi |Phi| dependence genuinely give the cluster-vs-galaxy SPLIT, or is it (like the naive O(1)) ~orders too small? Return: holds_up (solid/partial/overclaimed/dead), closes_galaxy_safely (yes-paper-flips/no-nogo-holds/partial), the_magnitude, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, closes_galaxy_safely:{type:'string',enum:['yes-paper-flips','no-nogo-holds','partial']}, the_magnitude:{type:'string'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','closes_galaxy_safely','the_magnitude','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE: does the AeST NONLINEAR |Phi|-boundary enhancement close the cluster residual GALAXY-SAFELY (the paper flips to the strong result) or fall short (the no-go holds at the nonlinear level)?\nDERIVE:\n${JSON.stringify(der).slice(0,4000)}\nCOMPUTE:\n${JSON.stringify(C).slice(0,5000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4500)}\n\nReturn 'report' (markdown) + fields. Cover: (1) the AeST nonlinear |Phi|-boundary mechanism + what we computed; (2) the cluster-core boost magnitude -- does it close the ~1e14 Msun residual; (3) the galaxy-veto + Cassini -- galaxy-safe?; (4) THE VERDICT -- closes galaxy-safely (paper FLIPS: clusters explained, no dark matter, state exactly how + the magnitude + how galaxies stay safe) OR falls short (no-go holds, the paper stands airtight, state by what factor + why); (5) if partial, the exact remaining computation (full N-body). Both-ways, quarantine, NO manufactured close. This decides whether Carl's framework explains clusters with no dark matter.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['closes-galaxy-safely-paper-flips','partial-promising','falls-short-nogo-holds']}, cluster_boost:{type:'string'}, galaxy_safe:{type:'string'}, paper_decision:{type:'string'}, what_remains:{type:'string'} }, required:['report','verdict','cluster_boost','galaxy_safe','paper_decision','what_remains'] } })
return { synth, der, comps: C, ver }
