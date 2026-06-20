export const meta = {
  name: 'bullet-cluster-mond-edition',
  description: 'The EXACT calculation of the Bullet Cluster (1E 0657-558) + the Princeton/Burrows "87% dark" cluster mass-budget, in the framework MODIFIED-INERTIA MOND edition. Four routes (the lensing-gas OFFSET; the AMPLITUDE residual; the collision VELOCITY; the mass-budget rebuttal) -> verify -> a both-ways "framework edition" doc that engages the real physics (NOT high-priest, NOT manufactured), citing the Princeton slide.',
  phases: [
    { title: 'Compute', detail: 'the OFFSET (collisionless field tracks galaxies); the AMPLITUDE residual at the peaks; the ~4700 km/s velocity (MOND-favorable?); the Princeton mass-budget "87% dark" rebuttal' },
    { title: 'Verify', detail: 'adversarial: offset genuinely reproduced or hand-waved? amplitude residual honest? velocity claim real? no manufactured win, no high-priest dismissal' },
    { title: 'Synthesize', detail: 'the Bullet-in-framework-MOND doc with EXACT calculations + the Princeton citation' },
  ],
}

const FRAMEWORK = `
THE FRAMEWORK (Zimmerman) + the banked Bullet/cluster standing (READ: BULLET_CLUSTER_GEOMETRIC_MODEL_2026-06-19.md,
ROUTE3_BULLET_OFFSET_LENSING_2026-06-15.md, CLUSTER_CORE_SHAPE_RXJ1347_2026-06-20.md, CLUSTER_STACK_AND_DECISIVE_
TEST_2026-06-20.md, DARK_MATTER_ILLUSION_2026-06-19.md, project memory). a0=c^2 sqrt(Lambda/32pi)=9.36e-11,
modified-INERTIA MOND, g_obs=sqrt(g_bar^2+g_bar*a0). CRUCIAL: the framework's dark sector is its OWN ghost-
condensate scalar field -- the Q-mode is a w=0 COLLISIONLESS a^-3 cold "dust" (the cosmic dark-matter budget),
NOT a new particle and NOT the gas. It is a MODE of gravity, but it clusters and free-streams through collisions
like CDM does (collisionless).

THE PRINCETON SLIDE (Burrows ASTRO 204, galaxy.cluster.pdf, "Evidence for Dark Matter"): for a typical rich
cluster M=1e15 Msun, mass in hot gas ~11%, mass in stars ~2%, "the rest of the mass is dark!" (~87%). Plus the
VIRIAL argument (sigma_v -> Newtonian virial mass >> baryons) and the LENSING argument (kappa -> total mass >>
baryons). This is the cluster mass-DISCREPANCY argument.

THE BULLET CLUSTER (1E 0657-558, Clowe+2006 ApJ 648 L109): a merging pair; the weak-lensing convergence kappa
peaks are OFFSET (~8-sigma) from the X-ray GAS peaks and instead sit on the GALAXIES. The Clowe "direct empirical
proof of dark matter" argument: the GAS is the DOMINANT baryon (~5-6x the stellar mass), so in a baryons-only
modified gravity the lensing should follow the GAS -> but it follows the galaxies -> a collisionless dark
component is required.

THE FRAMEWORK'S MOND EDITION (the both-ways physics to compute, NOT high-priest, NOT manufactured):
 1. THE OFFSET is NOT evidence against the framework. The Bullet offset shows the dominant gravitating mass is
    COLLISIONLESS (tracks the galaxies, not the collisional gas). The framework's OWN ghost-condensate dust IS
    collisionless -> in the merger it passes through with the galaxies, so the lensing peaks at the galaxies,
    offset from the gas -- REPRODUCED with the framework's own field, NO new particle. (Plus the galaxies' own
    baryons + their MOND phantom track the galaxies.) The offset is a both-ways NEUTRAL/REPRODUCED result, the
    same way CDM reproduces it -- except the collisionless component is a mode of the framework's gravity sector.
 2. THE REAL Bullet issue is the AMPLITUDE: MOND from the visible baryons (galaxies + the small gas at the peak)
    under-predicts the lensing kappa at the peaks by ~factor 2-3 -> the framework's collisionless field must
    supply the residual = THE SHARED MOND CLUSTER-CORE PROBLEM (banked this session: the no-particle stack
    covers ~45% (gas-tracking, RX J1347 data) to ~54-65% (galaxy-tracking) of the core; the rest is the shared
    gap; classically Angus-Famaey-Zhao 2006 used ~2 eV neutrinos -- a particle the framework replaces with its
    own field, partially).
 3. THE COLLISION VELOCITY ~4700 km/s (gas shock; subcluster ~2700-3100 km/s) is MOND-FAVORABLE (Angus & McGaugh
    2008): MOND's stronger long-range force accelerates the infall, making the high velocity NATURAL where it is
    a ~tail event for LCDM. Compute the infall velocity MOND vs LCDM.
 4. THE PRINCETON "87% dark" mass-budget: in the framework the Newtonian-inferred "missing mass" is LARGELY the
    MOND BOOST of the visible baryons (the dynamical/lensing mass = baryons x the MOND enhancement, NOT a
    particle). Compute the exact accounting: how much of "87% dark" is the MOND boost vs the residual field vs
    the irreducible shared gap.

THE EXACT CALCULATIONS to produce (real Bullet + cluster data, sympy/numpy): the MOND lensing convergence
kappa(x) at the main + bullet peaks from each component; the predicted vs observed peak amplitude + the residual
factor; the geometric offset; the infall velocity MOND vs LCDM; the mass-budget accounting (MOND-boost vs field
vs gap) for the Princeton 1e15 cluster.

QUARANTINE: a0/Z/kappa never asserted derived; the residual field amplitude (I0) is FREE. BOTH-WAYS (#1 rule):
do NOT be a high priest ("the Bullet is proof of a dark particle" -- FALSE, the offset is reproduced by the
framework's collisionless field); do NOT manufacture ("MOND debunks the Bullet" -- FALSE, the amplitude residual
is real and shared). Credit the offset-reproduction + the favorable velocity at full weight; concede the
amplitude residual (the shared cluster problem) at full weight. Use REAL data (Clowe+2006, Markevitch+2002,
Angus-Famaey-Zhao 2006, Angus-McGaugh 2008); cite. The deliverable engages the Princeton slide's actual claims.
`

const COMP_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    route: { type: 'string' },
    calculation: { type: 'string', description: 'the actual exact calc with equations + real numbers' },
    framework_result: { type: 'string', enum: ['reproduces','partial','favorable','residual-shared','fails'] },
    key_numbers: { type: 'array', items: { type: 'string' } },
    script_path: { type: 'string' },
    both_ways: { type: 'string', description: 'what is credited AND what is conceded' },
    sources: { type: 'string' },
  },
  required: ['route','calculation','framework_result','key_numbers','script_path','both_ways','sources'],
}

const VERDICT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: { route:{type:'string'}, holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']},
    high_priest_or_manufactured:{type:'string', description:'is the prior agent being a high priest OR manufacturing? both-ways check'},
    skeptic_findings:{type:'string'}, corrected:{type:'string'} },
  required: ['route','holds_up','high_priest_or_manufactured','skeptic_findings','corrected'],
}

const ROUTES = [
  { key: 'the_offset', prompt: `ROUTE 1 -- THE OFFSET (Clowe's "direct empirical proof of dark matter"). Compute the framework's MOND lensing
convergence kappa at the Bullet's main + bullet subcluster peaks. Show EXACTLY why the lensing peaks at the
GALAXIES, offset from the X-ray GAS: the framework's COLLISIONLESS ghost-condensate dust (its own field, NO
particle) passes through the collision WITH the galaxies, while the collisional gas lags. Compute the geometric
offset (the gas-vs-lensing peak separation ~few hundred kpc) and show the framework reproduces it the SAME way
CDM does -- a collisionless component tracking the galaxies. ADDRESS the Clowe argument head-on: the gas is the
DOMINANT baryon (~5-6x stars), so a NAIVE baryons-only MOND would weight the lensing toward the gas -> the
resolution is that the framework's collisionless FIELD (not the gas) carries the dominant gravitating mass at
the peaks. Both ways: the offset is REPRODUCED (no particle, not a kill) BUT it does require the field's
collisionless residual at the peaks (route 2). Real data: Clowe+2006 kappa map, the peak positions, the gas
vs galaxy masses. sympy/numpy; do NOT be a high priest, do NOT manufacture.` },
  { key: 'the_amplitude', prompt: `ROUTE 2 -- THE AMPLITUDE residual (the REAL Bullet issue). Compute the MOND lensing kappa at the Bullet peaks
from the VISIBLE baryons only (galaxies' stars + the gas at/near the peak) with g_obs=sqrt(g_bar^2+g_bar*a0) at
a0=9.36e-11, and compare to the OBSERVED lensing kappa (Clowe+2006). What is the residual factor -- how much
extra collisionless mass must the framework's field supply at the peaks? Connect to the session's banked
result: the no-particle stack covers ~45-65% of the cluster-core residual (RX J1347 gas-tracking ~45%; the
field's own ~17-20% Y-Q boost; IGIMF remnants). So at the Bullet peaks the framework's field covers ~part, the
rest is the shared MOND cluster gap (classically Angus-Famaey-Zhao 2006 needed ~2 eV neutrinos). Quantify the
residual and how much the framework's field + baryons cover. Both ways -- the residual is REAL and SHARED
(concede), but it is the framework's own field not a new WIMP (credit). Real Bullet lensing + baryon masses.` },
  { key: 'the_velocity', prompt: `ROUTE 3 -- THE COLLISION VELOCITY (the MOND-favorable card). The Bullet's gas shock velocity is ~4700 km/s
(Markevitch+2002); the subcluster infall ~2700-3100 km/s. Compute the infall velocity in the framework's MOND
vs LCDM: MOND's stronger long-range force (g ~ sqrt(G M a0)/r in deep-MOND) accelerates the two subclusters'
mutual infall from turnaround, giving a HIGHER pairwise velocity than LCDM's 1/r^2 for the same masses. Show
the framework predicts a velocity consistent with the observed high value where LCDM finds it a ~1-in-(large)
tail event (the banked LCDM "Bullet too fast" tension; Lee-Komatsu, Kraljic-Sarkar). WebFetch Angus & McGaugh
2008 (arXiv:0712.3170) + the LCDM bullet-velocity-tension papers. Both ways -- a genuine MOND-favorable result
(credit) without overclaiming (the velocity systematics + the gas-vs-DM-velocity distinction are real). sympy.` },
  { key: 'mass_budget', prompt: `ROUTE 4 -- the PRINCETON "87% dark" mass-budget rebuttal (the slide's actual argument). For the Princeton
M=1e15 Msun cluster (gas ~11%, stars ~2%, "87% dark"): compute EXACTLY how the framework re-reads the "87%
dark". The Newtonian virial/lensing mass = baryons x the MOND BOOST (the dynamical mass an observer infers
Newtonianly is g_obs/g_bar x the true baryonic mass). Compute the MOND boost in the cluster core (g_bar~a0
regime -> boost ~factor 2-3) and show how much of the "87% dark" is (i) the MOND enhancement of the VISIBLE
baryons (NOT a particle), (ii) the framework's collisionless field (the residual it covers), (iii) the
irreducible shared gap. The honest accounting: "87% dark particle" is WRONG (conflates the MOND boost with a
particle); the real split is ~[MOND boost] + [field] + [shared gap]. Quantify each fraction. Both ways --
credit the large MOND-boost re-reading (most of the "dark" is not a particle), concede the residual gap. sympy.` },
]

phase('Compute')
const out = await pipeline(
  ROUTES,
  (r) => agent(
`${FRAMEWORK}\n\nROUTE (key "${r.key}"):\n${r.prompt}\n\nRead the banked BULLET_CLUSTER_GEOMETRIC_MODEL + the session cluster ledgers; WebSearch/WebFetch Clowe+2006, Markevitch+2002, Angus-Famaey-Zhao 2006 (astro-ph/0609125), Angus-McGaugh 2008. WRITE scripts under opus_48_extended_research/reviews/bullet_mond/. Return the structured object with REAL numbers + EXACT equations. Both-ways + quarantine: NOT high-priest, NOT manufactured; the Princeton slide's claim engaged head-on.`,
    { label: `compute:${r.key}`, phase: 'Compute', schema: COMP_SCHEMA }
  ).then(x => ({ key: r.key, comp: x })),
  (d) => agent(
`${FRAMEWORK}\n\nSKEPTIC for route "${d.key}". Prior:\n${JSON.stringify(d.comp).slice(0,6500)}\n\nBOTH WAYS, adversarial -- check for BOTH high-priest dismissal AND manufacturing. Is the offset GENUINELY reproduced (collisionless field tracks galaxies) or hand-waved? Is the amplitude residual honestly conceded (the shared gap, not hidden)? Is the velocity claim real (not overclaimed)? Is the mass-budget re-reading correct (MOND boost vs particle)? Re-run the load-bearing number. Name if the prior agent is being a high priest OR manufacturing. Return the verdict.`,
    { label: `verify:${d.key}`, phase: 'Verify', schema: VERDICT_SCHEMA }
  ).then(v => ({ ...d, verdict: v }))
)

phase('Synthesize')
const synth = await agent(
`${FRAMEWORK}\n\nSYNTHESIZE: the Bullet Cluster + the Princeton "87% dark" in the framework's MOND edition.\n\nROUTES + VERDICTS:\n${JSON.stringify(out).slice(0,13000)}\n\nReturn 'report' (markdown) = a clear, calculation-backed "FRAMEWORK EDITION" that a student could read alongside the Princeton slide: (1) THE OFFSET -- the exact MOND calc showing the lensing peaks at the galaxies (the framework's collisionless field + galaxy baryons), offset from the gas, REPRODUCED with no new particle (the same way CDM does, but a mode of gravity); engage Clowe's "proof of dark matter" head-on. (2) THE AMPLITUDE -- the residual factor at the peaks, how much the framework's field + baryons cover (~the session's 45-65%), the shared MOND gap honestly conceded. (3) THE VELOCITY -- the ~4700 km/s in MOND vs LCDM, the MOND-favorable result. (4) THE "87% dark" -- the exact re-reading: how much is the MOND boost of visible baryons (NOT a particle), the field, the gap. (5) THE HONEST BOTTOM LINE -- the Bullet is NOT proof of a dark particle (the offset is reproduced by the framework's collisionless field + the velocity is MOND-favorable), but the amplitude residual is the real, shared MOND cluster problem. Cite the Princeton slide (Burrows ASTRO 204) + the real papers. Hold quarantine + both-ways: NOT high-priest, NOT manufactured.`,
  { label: 'synthesize', phase: 'Synthesize', schema: { type:'object', additionalProperties:false, properties:{
    report:{type:'string'}, offset_verdict:{type:'string'}, amplitude_verdict:{type:'string'}, velocity_verdict:{type:'string'},
    mass_budget_split:{type:'string'}, honest_bottom_line:{type:'string'} },
    required:['report','offset_verdict','amplitude_verdict','velocity_verdict','mass_budget_split','honest_bottom_line'] } }
)
return { synth, out }
