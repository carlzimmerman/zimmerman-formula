export const meta = {
  name: 'collective-efe-cluster-mond',
  description: "Carl's idea: in a cluster, the member galaxies' long-range deep-MOND fields (1/r, reaching toward the horizon) OVERLAP, so the collective/clumpy nonlinear-MOND field could give the whole region more binding (a region-wide collective EFE) than the smooth-baryon estimate -- closing part of the cluster residual with NO new mass. Three routes: discrete-clumpy-vs-smooth total phantom; the collective inter-galaxy EFE field; the long-range overlapping tails. Both ways, four gates, quarantine.",
  phases: [
    { title: 'Compute', detail: 'discrete-clumpy vs smooth total phantom (does clumpiness change the TOTAL?); the collective inter-galaxy EFE field; the long-range overlapping 1/r tails' },
    { title: 'Verify', detail: 'adversarial: does the collective effect ADD net cluster mass or just redistribute it? sub-additivity vs overlap; EFE sign; galaxy-veto' },
    { title: 'Synthesize', detail: 'is the collective/clumpy nonlinear-MOND effect real, and does it close part of the ~30-49% residual no-particle' },
  ],
}

const FRAMEWORK = `
THE FRAMEWORK (Zimmerman) + the cluster standing (READ: CLUSTER_CORE_SHAPE_A2029_2026-06-20.md, CLUSTER_STACK_
AND_DECISIVE_TEST_2026-06-20.md, CLUSTER_RESIDUAL_CLOSURE_2026-06-19.md, GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15.md,
project memory). a0=c^2 sqrt(Lambda/32pi)=9.36e-11, modified-INERTIA MOND, g_obs=sqrt(g_bar^2+g_bar*a0); the
deep-MOND field of an isolated mass falls as g~sqrt(G M a0)/r (1/r, NOT 1/r^2), so a galaxy's MOND influence
reaches far -- out to the EFE transition where it meets the external (cluster/cosmic) field at g_ext~a0. The
cluster-core residual is GAS-TRACKING, ~50-71% no-particle covered (relaxed), ~30-49% irreducible shared MOND
gap. The dark sector is the framework's OWN field, NO new particle (Carl's #1 ask).

CARL'S IDEA (take it SERIOUSLY, compute it, do NOT high-priest-dismiss): in a relaxed cluster the MEMBER
GALAXIES sit near each other; each galaxy's long-range 1/r deep-MOND field reaches out toward the horizon; the
fields of the many galaxies OVERLAP in the inter-galaxy medium; does that overlapping COLLECTIVE field give the
WHOLE AREA an enhanced acceleration / a region-wide collective EFE -- adding cluster binding (extra effective
gravitating mass) that the SMOOTH-baryon cluster-MOND estimate MISSES, with NO new mass? If real, it could
close part of the ~30-49% residual no-particle.

THE HONEST PHYSICS to resolve BOTH WAYS (compute, do not assert): (1) MOND nonlinearity is SUB-ADDITIVE at
large r: for two masses M, the deep-MOND field at distance is ~sqrt(2M) NOT 2*sqrt(M) -- the collective field
is LESS than the sum of individual fields, working AGAINST extra mass. (2) The MOND "enclosed-mass" property
(AQUAL/QUMOND, spherical): the TOTAL phantom mass within a radius is set by the TOTAL enclosed BARYONIC mass,
INDEPENDENT of how clumpy the baryons are -- so discrete-vs-smooth changes WHERE the phantom is (more near
galaxies) but maybe NOT the TOTAL -> would NOT close the residual. (3) BUT: non-spherical/discrete corrections,
the inter-galaxy phantom density, and the COLLECTIVE EFE are genuinely untested; the banked EFE-on-galaxies
finding is that the external field DECREASES a member's INTERNAL boost (wrong sign for the members), but the
collective field SOURCING the inter-galaxy potential is a different question. (4) the standard cluster-MOND
residual calc ALREADY uses the TOTAL baryon distribution -> is Carl's collective effect already in it, or is
there an extra clumpy/overlap term it misses?

THE FOUR GATES: G1 SUFFICIENCY (close part of the ~30-49% residual at a0=9.36e-11), G2 GALAXY-VETO (NOT break
the SPARC RAR), G3 NO-NEW-PARTICLE (own field / pure MOND nonlinearity), G4 DATA. QUARANTINE: a0/Z/kappa never
asserted derived. BOTH-WAYS (#1 rule): Carl's idea is physically motivated -- hunt it HARD with a real QUMOND/
AQUAL computation (NOT high-priest dismissal); concede honestly if the enclosed-mass theorem / sub-additivity
kills it (NOT manufactured). WebSearch/WebFetch the MOND cluster-clumpiness + EFE literature (Milgrom, Famaey-
McGaugh review, the discrete-MOND-N-body work); sympy/numpy with a realistic cluster galaxy distribution.
`

const COMP_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    route: { type: 'string' },
    calculation: { type: 'string', description: 'the actual QUMOND/AQUAL calc with equations + real numbers' },
    collective_effect: { type: 'string', enum: ['adds-net-mass','redistributes-only','sub-additive-reduces','negligible','n/a'] },
    closes_residual: { type: 'string', enum: ['closes','partial','insufficient','no'] },
    galaxy_veto: { type: 'string', enum: ['safe','marginal','breaks','n/a'] },
    key_numbers: { type: 'array', items: { type: 'string' } },
    script_path: { type: 'string' },
    honest_caveats: { type: 'string' },
    sources: { type: 'string' },
  },
  required: ['route','calculation','collective_effect','closes_residual','galaxy_veto','key_numbers','script_path','honest_caveats','sources'],
}

const VERDICT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: { route:{type:'string'}, holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']},
    adds_real_cluster_mass:{type:'boolean'}, high_priest_or_manufactured:{type:'string'},
    skeptic_findings:{type:'string'}, corrected:{type:'string'} },
  required: ['route','holds_up','adds_real_cluster_mass','high_priest_or_manufactured','skeptic_findings','corrected'],
}

const ROUTES = [
  { key: 'clumpy_vs_smooth', prompt: `ROUTE 1 -- DISCRETE-CLUMPY vs SMOOTH total phantom (the crux of Carl's idea). Model a rich cluster TWO ways
at a0=9.36e-11: (a) the member galaxies as N DISCRETE deep-MOND clumps (a realistic luminosity function,
~hundreds of galaxies + their positions) + the smooth ICM gas; (b) the SAME total baryonic mass as a SMOOTH
distribution. Compute the QUMOND phantom density rho_ph = -(1/4piG) div[(nu-1) grad Phi_N] for BOTH and the
TOTAL phantom mass M_ph(<r) within the core (~420 kpc). KEY QUESTION: does the DISCRETE-clumpy total phantom
EXCEED the smooth total (Carl's collective overlap adds mass), or is the TOTAL the SAME (the MOND enclosed-mass
property -- clumpiness only changes WHERE the phantom is)? Quantify the difference. The deep-MOND sub-additivity
sqrt(2M)<2sqrt(M) and the enclosed-mass theorem both suggest the total is ~baryon-set, but COMPUTE it with a
real clumpy distribution + the non-spherical corrections. Both ways -- a genuine clumpy-adds-mass result (closes
part of the residual no-particle) vs redistributes-only (the honest likely null). sympy/numpy + real cluster
galaxy distribution. Do NOT high-priest-dismiss; do NOT manufacture.` },
  { key: 'collective_efe', prompt: `ROUTE 2 -- the COLLECTIVE inter-galaxy EFE field (Carl's "the whole area gets more EFE"). Each member galaxy
sources a deep-MOND field; in the inter-galaxy medium these OVERLAP. Compute the COLLECTIVE acceleration field
in the inter-galaxy space of a relaxed cluster (sum/QUMOND-combine the member galaxies' fields). (a) Does the
overlapping collective field create a region-wide enhanced "external field" that ADDS to the cluster's binding
/ total gravitating mass? (b) Or, per the banked EFE finding, does the external field on each member DECREASE
its internal MOND boost (wrong sign for the members)? Resolve the SIGN: collective field SOURCING the
inter-galaxy potential (could add binding) vs EFE SUPPRESSING member internal dynamics (subtracts). (c) Is the
collective inter-galaxy g_ext above or below a0 (deep-MOND vs Newtonian regime)? Quantify the net effect on the
cluster total mass. Both ways -- a genuine collective-binding enhancement vs an EFE-suppression / wash. sympy +
real cluster member field. The banked EFE-on-galaxies result is g_int/a0~0.22-0.34 > g_ext -> EFE decreases the
boost; does the COLLECTIVE (region-wide) picture differ?` },
  { key: 'longrange_horizon', prompt: `ROUTE 3 -- the LONG-RANGE / "reaches to the horizon" overlapping tails. Carl: a galaxy's outer acceleration
reaches far. In deep-MOND an isolated galaxy's field g~sqrt(G M a0)/r extends out to the MOND radius / the EFE
transition (where g~g_ext~a0). Compute: how far does a member galaxy's deep-MOND field reach in a cluster
(before the cluster external field cuts it off)? Do the overlapping 1/r tails of N galaxies create a collective
POTENTIAL in the cluster that is DEEPER than the smooth estimate -- a region-wide acceleration floor that adds
binding? Quantify vs the sub-additivity (sqrt(sum) < sum sqrt). ALSO: is there a connection to the dS-Unruh /
horizon a0-floor -- does the COLLECTIVE field of the ensemble reaching toward the de Sitter scale add a
region-wide a0-class floor (the framework's distinctive content)? Both ways -- a genuine long-range collective
deepening vs sub-additive wash. sympy/numpy. Engage Carl's "to the horizon" framing precisely.` },
]

phase('Compute')
const out = await pipeline(
  ROUTES,
  (r) => agent(
`${FRAMEWORK}\n\nROUTE (key "${r.key}"):\n${r.prompt}\n\nRead the banked cluster + EFE ledgers; WebSearch/WebFetch the MOND clumpiness/EFE literature (Milgrom, Famaey-McGaugh 2012 review, discrete-MOND N-body). WRITE scripts under opus_48_extended_research/reviews/collective_efe/. Return the structured object with REAL numbers. Both-ways + quarantine: take Carl's idea SERIOUSLY (real QUMOND/AQUAL calc, NOT high-priest dismissal); concede honestly if sub-additivity / the enclosed-mass theorem kills it (NOT manufactured).`,
    { label: `compute:${r.key}`, phase: 'Compute', schema: COMP_SCHEMA }
  ).then(x => ({ key: r.key, comp: x })),
  (d) => agent(
`${FRAMEWORK}\n\nSKEPTIC for route "${d.key}". Prior:\n${JSON.stringify(d.comp).slice(0,6500)}\n\nBOTH WAYS, adversarial -- check for BOTH high-priest dismissal AND manufacturing. Does the collective/clumpy effect ADD NET cluster mass (G1) or just REDISTRIBUTE it (the enclosed-mass theorem)? Re-run the load-bearing QUMOND number. Is the sub-additivity sqrt(sum)<sum-sqrt correctly applied? Is the EFE sign right (does the collective field ADD binding or SUPPRESS members)? Does it pass the GALAXY-VETO? Try hardest to BREAK a manufactured collective enhancement AND to RESCUE a genuine one (Carl's idea deserves the rescue attempt). Return the verdict.`,
    { label: `verify:${d.key}`, phase: 'Verify', schema: VERDICT_SCHEMA }
  ).then(v => ({ ...d, verdict: v }))
)

phase('Synthesize')
const synth = await agent(
`${FRAMEWORK}\n\nSYNTHESIZE Carl's collective-EFE / clumpy-nonlinear-MOND cluster idea.\n\nROUTES + VERDICTS:\n${JSON.stringify(out).slice(0,12000)}\n\nReturn 'report' (markdown), written so Carl can see his idea taken seriously and computed: (1) the DISCRETE-CLUMPY vs SMOOTH result -- does galaxy clumpiness add NET cluster phantom mass, or does the MOND enclosed-mass theorem pin the total to the baryons (redistribute-only); (2) the COLLECTIVE inter-galaxy EFE -- does the overlapping field ADD binding or does the EFE SUPPRESS the members (the sign); (3) the LONG-RANGE overlapping-tails / "to the horizon" result -- collective deepening vs sub-additive wash; (4) the honest VERDICT on Carl's idea -- is it a real effect that closes part of the ~30-49% residual no-particle, or does sub-additivity + the enclosed-mass theorem make it redistribute-only (no net mass); (5) if it fails, EXACTLY why (the physics), and whether any piece survives. Hold quarantine + both-ways; Carl's idea is physically motivated -- credit any genuine effect at full weight, concede honestly if it's redistribute-only; NOT high-priest, NOT manufactured.`,
  { label: 'synthesize', phase: 'Synthesize', schema: { type:'object', additionalProperties:false, properties:{
    report:{type:'string'}, verdict:{type:'string', enum:['real-adds-mass','partial','redistributes-only-no-net-mass','negligible']},
    clumpy_result:{type:'string'}, efe_sign:{type:'string'}, closes_residual:{type:'string'}, where_it_stops:{type:'string'} },
    required:['report','verdict','clumpy_result','efe_sign','closes_residual','where_it_stops'] } }
)
return { synth, out }
