export const meta = {
  name: 'cluster-gravity-remaining-doors',
  description: 'The LAST genuinely-untried theory doors to close cluster-core gravity (the closure doors are near-exhausted; gas-tracking confirmed on 2 clusters; no third no-particle ingredient found). Four fresh angles NOT in the killed-list: (A) potential-DEPTH-keyed (Phi/c^2) galaxy-safe boost; (B) full relativistic non-static (merging-cluster) lensing; (C) multi-field / extended no-particle dark sector; (D) deep 2025-2026 mechanism sweep. Both ways, four gates, honest prior = likely confirms the ceiling.',
  phases: [
    { title: 'Hunt', detail: 'four genuinely-untried doors: depth-keyed boost; relativistic dynamic lensing; multi-field dark sector; fresh-mechanism sweep' },
    { title: 'Verify', detail: 'adversarial four gates: closes the core? galaxy-safe? no new particle? Cassini/data-safe?' },
    { title: 'Synthesize', detail: 'is there ANY untried door that closes the residual, or is the ~30-49% shared gap genuinely irreducible' },
  ],
}

const FRAMEWORK = `
THE FRAMEWORK (Zimmerman) + the FULL banked cluster standing as of 2026-06-20 (READ: CLUSTER_CORE_SHAPE_A2029_
2026-06-20.md, CLUSTER_CORE_SHAPE_RXJ1347_2026-06-20.md, CLUSTER_STACK_AND_DECISIVE_TEST_2026-06-20.md,
CLUSTER_CLOSURE_HUNT2_2026-06-20.md, CLUSTER_RESIDUAL_CLOSURE_2026-06-19.md, project memory). a0=c^2 sqrt(
Lambda/32pi)=9.36e-11, modified-INERTIA MOND, g_obs=sqrt(g_bar^2+g_bar*a0); dark sector = the framework's OWN
collisionless ghost-condensate field (NO new particle is the goal).

THE STANDING (honest, do NOT re-litigate): the cluster-core residual is GAS-TRACKING (confirmed on a merger
RX J1347 AND a relaxed XRISM cluster A2029; inner log-slope +1.81, M_res/M_star RISES outward). The
no-new-particle stack covers ~50-71% (relaxed) to ~45% (gas-tracking) of the core via MOND-on-gas + the field's
own ~17-20% Y-Q boost; the **~30-49% remainder is the irreducible shared MOND-cluster gap** (the framework's
MI == AeST modified-gravity to machine precision -> generic to the whole relativistic-MOND family). The
no-particle CLOSURE doors are NEARLY EXHAUSTED.

ALREADY KILLED / EXHAUSTED -- DO NOT RE-RUN: density-a0 floor (breaks galaxies, 222-406x SPARC, 0.38 dex); MI
non-adiabatic mean-mass (apocenter a->0 singularity); dS-Unruh environmental term (wrong sign); keV/eV sterile
(squeezed shut 2.7x m_th gap + 2026 N-body >5sigma + MicroBooNE); ghost-condensate accumulation (shift symmetry
-> no chameleon, Ward identity -> no Y->Q sourcing); known-physics (min-nu TG-forbidden, baryons ~7%, ~8.6%);
IGIMF stellar remnants (shape-closed by the gas-tracking data); the FINAL-DOOR third-ingredient check (AeST
lensing-vs-dynamics slip STRUCTURALLY DEAD lensing==dynamics s=1; non-equilibrium WRONG-SIGN; ICL SUBSUMED;
EFE WRONG-SIGN). The full-AeST Y-Q field boost (~17-20%) is REAL and already in the stack.

THE GENUINELY-UNTRIED DOORS (this workflow -- the LAST ones; honest prior = likely confirm the ~30-49% gap is
irreducible, but they are NOT in the killed-list and deserve a real both-ways hunt): see the routes.

THE FOUR GATES (a closure must pass all): G1 SUFFICIENCY (close the ~30-49% residual at a0=9.36e-11), G2
GALAXY-VETO (NOT break the SPARC RAR, <~0.13 dex), G3 NO-NEW-PARTICLE (own field / known physics, not a new
species), G4 DATA (eRASS1/CLASH/XRISM/Cassini/solar-system/LSS). QUARANTINE: a0/Z/kappa/I0 never asserted
derived. BOTH-WAYS (#1 rule): hunt HARD for a real closure (do NOT reflexively dismiss -- Carl penalizes
high-priest behavior), AND concede honestly if a door breaks a gate (do NOT manufacture). Use real data
(eRASS1, SPARC, the A2029/RXJ1347 profiles), sympy/numpy, WebSearch/WebFetch the 2024-2026 lit.
`

const HUNT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    route: { type: 'string' },
    mechanism: { type: 'string', description: 'the actual closure attempt with equations + numbers' },
    closes_residual: { type: 'string', enum: ['closes','partial','insufficient','no'] },
    galaxy_veto: { type: 'string', enum: ['safe','marginal','breaks','n/a'] },
    cassini_solar: { type: 'string', enum: ['safe','tension','fails','n/a'] },
    new_particle: { type: 'string', enum: ['none-own-field','known-physics','relocates','new-particle','n/a'] },
    key_numbers: { type: 'array', items: { type: 'string' } },
    script_path: { type: 'string' },
    honest_caveats: { type: 'string' },
    sources: { type: 'string' },
  },
  required: ['route','mechanism','closes_residual','galaxy_veto','cassini_solar','new_particle','key_numbers','script_path','honest_caveats','sources'],
}

const VERDICT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: { route:{type:'string'}, holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']},
    passes_all_gates:{type:'boolean'}, which_gate_fails:{type:'string'},
    high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} },
  required: ['route','holds_up','passes_all_gates','which_gate_fails','high_priest_or_manufactured','skeptic_findings','corrected'],
}

const ROUTES = [
  { key: 'depth_keyed_boost', prompt: `ROUTE A -- POTENTIAL-DEPTH-keyed (Phi/c^2) galaxy-safe boost (the natural complement to the FAILED
density-keying; the most promising untried). Clusters out-rank galaxies in EXACTLY one thing: potential DEPTH
(Phi/c^2 ~ 5e-5 in cluster cores vs ~1e-6 in galaxy disks vs ~1e-6 in the solar system but at HIGH
acceleration). The density-a0 floor BROKE galaxies because galaxies are DENSER than clusters. TEST a
modification keyed on Phi/c^2 (or the dimensionless g*R/c^2, or the compactness) -- NOT density -- that BOOSTS
the MOND/lensing in deep potentials (clusters) while leaving shallow-Phi galaxy disks UNTOUCHED. (a) Construct
the Phi-keyed interpolation/extra-term; (b) compute the cluster-core boost it gives (does it reach the ~30-49%
residual?); (c) the GALAXY-VETO: galaxies have shallow Phi -> is the SPARC RAR untouched? (d) the SOLAR-SYSTEM/
CASSINI veto: the Sun's surface Phi/c^2~2e-6 is shallow but Phi at the solar CENTER / a neutron star is deep --
does a Phi-keyed term violate Cassini |gamma-1|<2e-5 or pulsar/BBN? The banked claim "any depth-keyed floor is
~10^5 too weak" was a specific FLOOR -- test a full INTERPOLATION/running. Both ways: a genuine galaxy-safe +
Cassini-safe depth-keyed cluster boost would be the real win; concede if it breaks a gate. sympy/numpy, real
SPARC + cluster Phi.` },
  { key: 'relativistic_dynamic_lensing', prompt: `ROUTE B -- FULL relativistic / NON-STATIC lensing (the quasi-static estimate drops terms). The banked cluster
residual + the RX J1347/A2029 reads used QUASI-STATIC MOND lensing. In full relativistic AeST, a NON-STATIC /
merging cluster has extra metric terms: the gravitomagnetic zeta_i sector, the time-dependent O(c^-2) pieces of
the ij Einstein eq, and the velocity-dependent lensing of moving mass. (a) Does a MERGING cluster (Bullet,
RX J1347) get EXTRA lensing convergence from these non-static terms beyond the quasi-static MOND -- enough to
source part of the residual WITHOUT extra mass? (b) Estimate the magnitude: the v/c of the cluster merger
~0.015, so gravitomagnetic ~ (v/c)^2 ~ 2e-4 -- is that enough, or negligible? (c) Does it apply to RELAXED
clusters (A2029, low v) -- probably NOT, which is why A2029 still undershoots. Both ways -- a genuine non-static
lensing enhancement (helps mergers) vs negligible (v/c)^2 (the honest likely null). WebFetch the AeST lensing
sector (Blanchet-Skordis 2404.06584 the zeta_i/3.12 sector). sympy.` },
  { key: 'multifield_dark_sector', prompt: `ROUTE C -- MULTI-FIELD / extended no-particle dark sector. The framework is ONE scalar (the ghost condensate).
TEST whether a SECOND gravitational field (still NO particle -- a second scalar, a bimetric/massive-graviton
partner, or a vector) could cluster MORE in deep cluster cores than the single ghost-condensate dust, closing
the residual while staying galaxy-safe. (a) Does AeST's AETHER VECTOR A_mu (already in the theory!) source
extra core mass via its own field equation in a deep potential, beyond the K(Q) dust? (b) Could a second
shift-symmetric scalar with a DIFFERENT (cluster-clustering) mass scale add core mass? (c) the honest cost:
this RELOCATES the postulate (a second field is new structure the framework doesn't derive) but stays
no-PARTICLE. Does any multi-field extension reach the residual + pass the galaxy-veto + Cassini + the CMB? Both
ways -- a genuine no-particle multi-field closure (relocating but particle-free) vs it just re-imports the same
free amplitude / breaks a gate. sympy + the AeST aether sector.` },
  { key: 'fresh_mechanism_sweep', prompt: `ROUTE D -- DEEP 2025-2026 fresh-mechanism sweep (anything genuinely-new the banked work missed). WebSearch/
WebFetch broadly for 2025-2026 work closing the relativistic-MOND / modified-gravity cluster-core mass problem
that is NOT in the killed-list (density-a0, sterile-nu, IGIMF, MI-mean-mass): e.g. superfluid-DM cluster cores
(Berezhiani-Khoury phonon/coherence in deep potentials), Blanchet dipolar-DM clusters, Verlinde-emergent
cluster mass, a new AeST cluster solution, khronometric/Horava cluster effects, the 2026 Bullet/cluster papers
(arXiv:2605.10022, 2602.06082 already noted), any "MONDian baryonic feedback" or "modified-gravity + minimal
known component" combo. For each candidate: does it pass the four gates G1-G4 on the framework's footing? Both
ways -- report a genuine NEW lead the banked work missed, OR confirm the 2025-2026 literature offers no escape.
Cite arXiv IDs. Be the completeness critic.` },
]

phase('Hunt')
const out = await pipeline(
  ROUTES,
  (r) => agent(
`${FRAMEWORK}\n\nROUTE (key "${r.key}"):\n${r.prompt}\n\nRead the banked cluster ledgers; use real eRASS1 + SPARC; WebSearch/WebFetch the cited papers. WRITE scripts under opus_48_extended_research/reviews/cluster_doors3/. Return the structured object with REAL numbers + which gates G1-G4 pass/fail. Both-ways + quarantine: hunt HARD (do NOT be a high priest), concede honestly if a gate fails (do NOT manufacture).`,
    { label: `hunt:${r.key}`, phase: 'Hunt', schema: HUNT_SCHEMA }
  ).then(x => ({ key: r.key, hunt: x })),
  (d) => agent(
`${FRAMEWORK}\n\nSKEPTIC for route "${d.key}". Prior:\n${JSON.stringify(d.hunt).slice(0,6500)}\n\nBOTH WAYS, adversarial -- check for BOTH high-priest dismissal AND manufacturing. Does it pass ALL FOUR gates (G1 sufficiency, G2 galaxy-veto, G3 no-new-particle, G4 Cassini/data)? Re-run the load-bearing number. For the depth-keyed route especially: does the Phi-keyed term ACTUALLY leave galaxies untouched AND pass Cassini, or does it break one? Name which gate fails. Try hardest to BREAK a manufactured closure AND to RESCUE a genuine one (don't reflexively dismiss). Return the verdict.`,
    { label: `verify:${d.key}`, phase: 'Verify', schema: VERDICT_SCHEMA }
  ).then(v => ({ ...d, verdict: v }))
)

phase('Synthesize')
const synth = await agent(
`${FRAMEWORK}\n\nSYNTHESIZE the last cluster-gravity doors.\n\nROUTES + VERDICTS:\n${JSON.stringify(out).slice(0,13000)}\n\nReturn 'report' (markdown): (1) did ANY of the four untried doors pass all four gates (a genuine closure of the ~30-49% residual) -- if yes, which + how; (2) the BEST route + how far it got + which gate it fails; (3) the DEPTH-KEYED verdict specifically (route A, the most promising) -- can a Phi/c^2-keyed term boost clusters while staying galaxy-safe AND Cassini-safe, or does it break a gate; (4) the honest FINAL cluster-gravity standing -- is the ~30-49% shared MOND gap genuinely IRREDUCIBLE now (all doors exhausted), or is there a live lead; and the single sharpest remaining option (theory or observation). Hold quarantine + both-ways; a genuine closure is the prize, an honest "irreducible shared gap, doors exhausted" is the likely truth -- report whichever the calc gives; NOT high-priest, NOT manufactured.`,
  { label: 'synthesize', phase: 'Synthesize', schema: { type:'object', additionalProperties:false, properties:{
    report:{type:'string'}, any_closure:{type:'string', enum:['yes-genuine','partial','no-irreducible-gap']},
    depth_keyed_verdict:{type:'string'}, best_route:{type:'string'}, sharpest_remaining:{type:'string'}, where_it_stops:{type:'string'} },
    required:['report','any_closure','depth_keyed_verdict','best_route','sharpest_remaining','where_it_stops'] } }
)
return { synth, out }
