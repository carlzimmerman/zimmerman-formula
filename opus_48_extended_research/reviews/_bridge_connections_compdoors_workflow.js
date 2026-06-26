export const meta = {
  name: 'bridge-connections-computational-doors',
  description: 'Deep review of the CEICO/modified-gravity/Lorentz-violation/dS-QFT peoples INTELLECTUAL + collaboration CONNECTIONS, mapped onto the framework gaps, then distilled into concrete RUNNABLE COMPUTATIONAL DOORS (sympy/CAMB/SPARC/positivity-integral analyses we can actually execute in-repo). Both ways, quarantine held.',
  phases: [
    { title: 'Connect', detail: 'five connection-webs: ghost-condensate lineage (Horava->Mukohyama->Vikman->AeST); positivity/causality (Creminelli/Blas); dS-QFT/SO(4,1) gate (Sengor/Anninos/Kiritsis); MOND-Lagrangian completions (Seraille/Woodard/Blanchet); Lambda-CC + DESI (Padilla/Saltas/Koivisto)' },
    { title: 'Doors', detail: 'turn each webs best lead into a CONCRETE computational protocol: the calc, the tool, the input data, the both-ways outcome, the effort, where it lands in-repo' },
    { title: 'Confront', detail: 'adversarial: is the door genuinely RUNNABLE with our tools, does it TEST a real gap, or is it vaporware/already-done?' },
    { title: 'Synthesize', detail: 'the connection map + the RANKED computational-door list (impact x feasibility) = the deliverable' },
  ],
}

const FRAMEWORK = `
THE FRAMEWORK (Zimmerman) + this sessions banked results (read GHOST_CONDENSATE_2026-06-19.md,
GHOST_CONDENSATE_CONSEQUENCES_2026-06-19.md, AEST_EMBEDDING_2026-06-19.md, DARK_MATTER_ILLUSION_2026-06-19.md;
also read any notes under opus_48_extended_research/reviews/bridge_scout/ IF PRESENT -- a parallel scout is
populating it). a0=c^2 sqrt(Lambda/32pi)=9.36e-11, modified-INERTIA MOND from de Sitter-Unruh; the dark
sector = ONE scalar phi (Y-mode -> a0 MOND, Q-mode -> cold a^-3 dust), PROVEN structurally a GHOST
CONDENSATE (ACLM 2004), embedded in AeST (Skordis-Zlosnik 2021). Preferred-frame / Lorentz-violating
(forced by a covariant-Cassini-safe-MOND-lensing no-go) -> an SME background.

THE OPEN GAPS:
 GAP-1 the Q-sector kinetic term P(X)/K(Q)=mu^2(Q-1)^2 is POSTULATED (ghost-condensate wrong-sign-then-
   stabilized minimum), not derived -> FOUNDED-not-DERIVED. Need a first-principles ORIGIN.
 GAP-2 the SO(4,1) dS-vacuum GATE: induction of the preferred-frame term failed (dS vacuum too symmetric);
   the condensate EVADES via a background but does not DERIVE. Need a dS-QFT / emergent route to CLOSE it.
 GAP-3 a0=c^2 sqrt(Lambda/32pi): forced in FORM, coefficient (kappa=1/2, Z=sqrt(32pi/3)) a free input.
 GAP-4 the dark-matter AMOUNT Omega_dm=I0 (off-minimum displacement) is a free shift-charge IC.
 GAP-5 covariant Cassini-safe MOND LENSING forbidden -> framework lensing is preferred-frame phenomenology.

THE PEOPLE + THEIR KNOWN CONNECTIONS (the web to map -- verify + extend with WebSearch/INSPIRE):
 - Ghost-condensate LINEAGE: Petr HORAVA (Horava gravity = a preferred foliation; "Shift Symmetries in
   Quantum Gravity of the Ricci Flow" 2025-26 -- shift symmetry IS the ghost-condensate symmetry) ->
   Arkani-Hamed-Cheng-Luty-MUKOHYAMA 2004 (Mukohyama = the M in ACLM; ghost condensate AS dark matter;
   "Minimalism in modified gravity"/MMG; Horava cosmology) -> Alex VIKMAN (CEICO; k-essence, derivative
   VEVs, "Phantom of the Cosmological Time-Crystals" = condensates breaking time-translation) -> AeST
   K(Q) (SKORDIS-ZLOSNIK identify K(Q) as a ghost condensate). This chain is the GAP-1/2 spine.
 - POSITIVITY / CAUSALITY: Paolo CREMINELLI ("Positivity Constraints on Lorentz-breaking EFTs" 2024;
   Ghost-Inflation co-author) + Diego BLAS / Sergey SIBIRYAKOV (khronometric causality) + de Rham-Tolley
   positivity program. Tests whether the frameworks wrong-sign-then-stabilized P(X) PASSES or is KILLED.
 - dS-QFT / the GATE: Gizem SENGOR (de Sitter SO(4,1) group representations; "Ladder Operators of the de
   Sitter algebra"; "Unitarity at the Late-Time Boundary of dS") + Dionysios ANNINOS (dS horizons, sphere
   partition functions) + Elias KIRITSIS ("Emergent gravity from Hidden sectors").
 - MOND-LAGRANGIAN completions: Emeric SERAILLE (non-Abelian Yang-Mills graviphoton MOND, 2025) + Richard
   WOODARD (nonlocal-metric MOND) + Luc BLANCHET (dipolar dark matter / gravitational polarization).
 - LAMBDA / CC + DESI: Tony PADILLA (sequestering the CC) + Ippocratis SALTAS (CEICO; unimodular gravity,
   CC) + Jose BELTRAN JIMENEZ / Tomi KOIVISTO (teleparallel/affine) + Rodrigo CALDERON (CEICO; DESI w(z)).

THE DELIVERABLE Carl asked for: "deep review of these people + their connections, and see what DOORS we can
open to do COMPUTATIONAL ANALYSIS on." So the OUTPUT must be CONCRETE RUNNABLE computations -- things we
can actually execute in-repo with sympy / numpy / CAMB-or-CLASS / the SPARC data / explicit positivity or
dispersion-relation integrals -- each tied to a person/connection and a gap, with a both-ways outcome.
A "door" that is just "read more papers" does NOT count; a door must be a CALCULATION with a definite
PASS/KILL or NUMBER as output.

QUARANTINE: a0/Z/kappa/I0 never asserted derived. A computational door must be HONESTLY runnable (state the
tool, the input, the both-ways outcomes) -- not vaporware, not already-banked. BOTH-WAYS (#1 rule): a door
whose likely outcome is a KILL (e.g. positivity rules out the P(X)) is as valuable as one that bridges --
report both. Penalize a manufactured bridge and a reflexive dismissal EQUALLY. Use WebSearch/WebFetch
(arXiv, INSPIRE) to verify connections + methods; cite arXiv IDs.
`

const CONNECT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    web: { type: 'string' },
    connection_chain: { type: 'string', description: 'the intellectual/collaboration lineage: who built on whom, which ideas chain to the framework, with arXiv IDs' },
    key_papers: { type: 'array', items: { type: 'object', additionalProperties: false,
      properties: { author:{type:'string'}, title:{type:'string'}, arxiv:{type:'string'}, relevance:{type:'string'} },
      required:['author','title','arxiv','relevance'] } },
    computational_doors: { type: 'array', items: { type: 'object', additionalProperties: false,
      properties: {
        door: { type:'string' },
        gap: { type:'string', description:'GAP-1..GAP-5' },
        what_to_compute: { type:'string', description:'the actual calculation, concretely' },
        tool: { type:'string', description:'sympy / numpy / CAMB / CLASS / SPARC-fit / positivity-integral / group-theory' },
        inputs: { type:'string', description:'data/equations needed; whether in-repo or to be pulled' },
        bothways_outcome: { type:'string', description:'what a PASS vs a KILL/null would each mean' },
        feasibility: { type:'string', enum:['ready-now','needs-setup','hard'] },
        impact: { type:'string', enum:['high','medium','low'] },
      },
      required:['door','gap','what_to_compute','tool','inputs','bothways_outcome','feasibility','impact'] } },
    honest_caveats: { type: 'string' },
    sources: { type: 'string' },
  },
  required: ['web','connection_chain','key_papers','computational_doors','honest_caveats','sources'],
}

const DOOR_VERDICT = {
  type: 'object', additionalProperties: false,
  properties: {
    web: { type: 'string' },
    best_door: { type: 'string', description: 'the single most worth-running computational door from this web' },
    protocol: { type: 'string', description: 'concrete step-by-step recipe to run it (tool, inputs, equations, what to output)' },
    genuinely_runnable: { type: 'boolean' },
    tests_a_real_gap: { type: 'boolean' },
    likely_outcome: { type: 'string', enum: ['likely-bridge','likely-kill','genuinely-open','probably-null'] },
    skeptic_findings: { type: 'string' },
    corrected: { type: 'string' },
  },
  required: ['web','best_door','protocol','genuinely_runnable','tests_a_real_gap','likely_outcome','skeptic_findings','corrected'],
}

const WEBS = [
  { key: 'ghost_condensate_lineage', prompt: `WEB 1 -- the GHOST-CONDENSATE LINEAGE (GAP-1/2, the spine). Map the connection chain Horava (Horava
gravity, "Shift Symmetries in Quantum Gravity of the Ricci Flow") -> ACLM/Mukohyama (ghost condensate +
ghost-condensate-as-dark-matter + Minimal Modified Gravity) -> Vikman (k-essence, derivative VEVs,
time-crystals) -> AeST K(Q). Who cites/builds on whom; do Horava-gravity shift symmetry + Mukohyama MMG
give a UV ORIGIN or a foliation-based derivation of the ghost-condensate kinetic term the framework
postulates? COMPUTATIONAL DOORS to propose: e.g. (a) derive K(Q)=mu^2(Q-1)^2 (or its dispersion
omega^2~k^4/M^2) from a Horava/shift-symmetric/khronometric UV action via sympy; (b) match the frameworks
P(X) bilinear coefficients to Mukohyama MMG / Horava-gravity dispersion relations and check consistency;
(c) compute whether Vikmans time-crystal/k-essence stability conditions are SATISFIED by the frameworks
K(Q). Be concrete -- each door = a sympy/numpy calc with a definite output.` },
  { key: 'positivity_causality', prompt: `WEB 2 -- POSITIVITY / CAUSALITY (GAP-1, the potential KILL). Creminelli "Positivity Constraints on
Lorentz-breaking EFTs" (2024) + Blas-Sibiryakov khronometric causality + de Rham-Tolley positivity bounds.
The frameworks K(Q)=mu^2(Q-1)^2 is a WRONG-SIGN-then-stabilized P(X) (a ghost condensate) -- exactly the
kind of Lorentz-breaking EFT these positivity/causality programs constrain. COMPUTATIONAL DOOR (likely the
HIGHEST-VALUE, cleanest PASS/KILL): set up the explicit positivity-bound / causality (sub/super-luminal
sound-speed, analyticity dispersion-relation) test on the frameworks P(X) around the condensate background
and DETERMINE whether it PASSES or is EXCLUDED. Specify the exact inequalities (c_s^2 sign, the s-channel
dispersion integral, the Creminelli LV positivity conditions), the inputs (P(X) coefficients = time
P(X0)+2X0 P'', space -P(X0) from the banked ghost_condensate calc), and the both-ways outcome (PASS = a
real consistency WIN credited; KILL = the postulated P(X) is ruled out, a major honest finding). This door
should be runnable NOW in sympy/numpy. Verify Creminellis exact conditions via the arXiv paper.` },
  { key: 'dsqft_so41_gate', prompt: `WEB 3 -- dS-QFT / the SO(4,1) GATE (GAP-2). Sengor (de Sitter SO(4,1) group representations, ladder
operators, late-time-boundary unitarity) + Anninos (dS horizons, sphere partition functions) + Kiritsis
(emergent gravity from hidden sectors). The gate: the dS vacuum is SO(4,1)-invariant so it induces no
preferred-frame term. COMPUTATIONAL DOORS: (a) decompose the frameworks preferred-frame/aether term (u^mu,
the timelike condensate gradient) into SO(4,1) irreps using Sengors dS-algebra ladder-operator machinery --
is there a (e.g. discrete-series / principal-series) rep that a condensate background selects, giving a
group-theoretic statement of the gate-evasion? (b) compute whether an emergent-gravity-from-hidden-sector
(Kiritsis) construction could induce the frame at the boundary. Specify the group-theory/sympy calc and the
both-ways outcome (a rep-theoretic derivation of the frame = closing GAP-2; nothing = gate stays evaded-not-
closed). Concrete computations only.` },
  { key: 'mond_lagrangian', prompt: `WEB 4 -- MOND-LAGRANGIAN COMPLETIONS (GAP-1/5). Seraille (non-Abelian Yang-Mills graviphoton MOND, 2025)
+ Woodard (nonlocal-metric MOND) + Blanchet (dipolar DM / gravitational polarization). Each is a covariant
field theory whose weak-field limit is MOND. COMPUTATIONAL DOORS: (a) take Serailles graviphoton action (or
Woodards nonlocal kernel) and compute its predicted MOND acceleration scale -- does it reproduce
a0=c^2 sqrt(Lambda/32pi), and does its low-energy field map onto the frameworks ghost-condensate phi
(GAP-1)? (b) compute the LENSING (light bending) these completions predict and compare to the frameworks
preferred-frame lensing slip gamma=2 sqrt(1+a0/g)-1 -- does any give covariant Cassini-safe lensing the
framework lacks (GAP-5)? Specify the sympy weak-field expansion + the both-ways outcome. Be strict: a
phenomenological match is not a derivation.` },
  { key: 'lambda_cc_desi', prompt: `WEB 5 -- LAMBDA / CC + DESI (GAP-3/4 + the a0(z) hostage). Padilla (sequestering the cosmological constant)
+ Saltas (unimodular gravity, CC) + Beltran Jimenez/Koivisto (teleparallel/affine) + Calderon (DESI w(z)).
COMPUTATIONAL DOORS: (a) does the sequestering/unimodular global constraint FIX the a0<->Lambda coefficient
kappa (GAP-3) -- set up the global-constraint equation and see if it pins kappa=1/2 or leaves it free
(quarantine: likely free, but test it); (b) the a0(z) DESI confrontation -- using the existing repo tooling
(a0z_desi_figure.py, the declining sqrt(rho_DE) reading, DESI DR2 w0=-0.752 wa=-0.86), compute the SHARPEST
falsifiable a0(z) prediction + its current data status (the framework live front); (c) any teleparallel/
affine route to a preferred-frame MOND. Specify each calc + both-ways outcome. Some of these are ready-now
in-repo.` },
]

phase('Connect')
const out = await pipeline(
  WEBS,
  (w) => agent(
`${FRAMEWORK}\n\nWEB REVIEW (web "${w.key}"):\n${w.prompt}\n\nUse WebSearch/WebFetch (arXiv, INSPIRE-HEP) to verify the connections + the exact methods/conditions; cite arXiv IDs. Read banked GHOST_CONDENSATE_2026-06-19.md (+ ghost_condensate/ for the P(X) bilinear coefficients) and any bridge_scout/ notes. WRITE your connection-map + door notes under opus_48_extended_research/reviews/bridge_doors/. Return the structured object -- emphasize CONCRETE RUNNABLE computational doors (calc + tool + inputs + both-ways outcome), not reading lists. Both-ways + quarantine.`,
    { label: `connect:${w.key}`, phase: 'Connect', schema: CONNECT_SCHEMA }
  ).then(r => ({ key: w.key, connect: r })),
  (d) => agent(
`${FRAMEWORK}\n\nSKEPTIC + DOOR-REFINER for web "${d.key}". Prior agent returned:\n${JSON.stringify(d.connect).slice(0,7000)}\n\nBOTH WAYS. Pick the SINGLE best computational door from this web and (1) verify it is GENUINELY RUNNABLE with our tools (sympy/numpy/CAMB/SPARC/positivity-integral) -- if it needs a method, confirm the method exists (WebSearch the arXiv); (2) verify it TESTS A REAL GAP (not already-banked, not vaporware); (3) write a CONCRETE step-by-step PROTOCOL to run it (tool, inputs, the exact equations/inequalities, what number/verdict it outputs); (4) state the LIKELY OUTCOME honestly (likely-bridge / likely-kill / genuinely-open / probably-null) -- a likely-KILL (e.g. positivity excludes the P(X)) is HIGH value, say so. Demote any vaporware door; rescue any real one. Return the verdict.`,
    { label: `confront:${d.key}`, phase: 'Confront', schema: DOOR_VERDICT }
  ).then(v => ({ ...d, verdict: v }))
)

phase('Synthesize')
const synth = await agent(
`${FRAMEWORK}\n\nSYNTHESIZE the deep review.\n\nWEBS + REFINED DOORS:\n${JSON.stringify(out).slice(0,13000)}\n\nReturn 'report' (markdown): (1) THE CONNECTION MAP -- a tight narrative of how these people/ideas connect to the framework, organized by the spine (ghost-condensate lineage Horava->Mukohyama->Vikman->AeST), the positivity test, the dS-gate, the MOND-Lagrangians, and the Lambda/CC side; name the load-bearing papers (arXiv IDs). (2) THE RANKED COMPUTATIONAL-DOOR LIST -- the deliverable: every genuinely-runnable door ranked by impact x feasibility, each as: NAME | gap | what-to-compute | tool | inputs | both-ways outcome | effort. Put the cleanest PASS/KILL doors (likely the Creminelli positivity test on P(X), and the Horava/Mukohyama K(Q)-derivation) at the top. (3) THE TOP 3 to run FIRST and why. (4) Honest standing -- which doors could actually CLOSE a gap vs which are consistency checks. Hold quarantine + both-ways; a likely-KILL door is as valuable as a bridge; no dark-matter-particle doors.`,
  { label: 'synthesize', phase: 'Synthesize', schema: { type:'object', additionalProperties:false, properties:{
    report:{type:'string'}, connection_map:{type:'string'}, ranked_doors:{type:'string'}, top3_to_run:{type:'string'},
    highest_value_door:{type:'string'}, where_it_stops:{type:'string'} },
    required:['report','connection_map','ranked_doors','top3_to_run','highest_value_door','where_it_stops'] } }
)
return { synth, out }
