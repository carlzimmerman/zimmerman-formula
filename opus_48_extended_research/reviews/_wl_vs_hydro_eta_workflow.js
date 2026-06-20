export const meta = {
  name: 'wl-vs-hydro-eta-proxy',
  description: "The next lever XRISM handed us: the cluster residual MAGNITUDE is now a weak-lensing-vs-hydrostatic MASS-PROXY question on RELAXED clusters, not a turbulence question. Pin the REAL relaxed-cluster WL/HSE (and dynamical/caustic) mass ratio from the consensus literature, compute the framework eta(R500) on each proxy, and decide both-ways: does the best-supported proxy + the framework's Y-Q field CLOSE the cluster residual (hydro branch ~1.0-1.5 -> near-no-gap, the 'solved' case) or leave a REAL shared-MOND gap (WL branch ~2.33)? LOAD-BEARING both-ways check: the consensus hydrostatic bias is only ~25-35% (eta_hydro~1.8), NOT the WL/HSE~2.1 (eta~1.1) the XRISM synth leaned on — pin the real number, do not manufacture the collapse, do not high-priest the gap.",
  phases: [
    { title: 'Pull', detail: 'real relaxed-cluster WL-vs-X-ray/hydrostatic mass-ratio literature + an independent dynamical/caustic 3rd proxy' },
    { title: 'Compute', detail: 'framework eta(R500) on each mass proxy; which branch the relaxed-cluster data supports; does Y-Q field + best proxy close it' },
    { title: 'Verify', detail: 'adversarial: is WL/HSE~2.1 over-stated vs the ~30% consensus bias? is the close manufactured or the gap high-priested?' },
    { title: 'Synthesize', detail: 'the honest verdict: cluster residual CLOSED (hydro+Y-Q) or REAL shared gap (WL), and which the data favors' },
  ],
}

const FRAMEWORK = `
FRAMEWORK (Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2, modified-INERTIA MOND, the
framework's OWN dS-Unruh interpolation g_obs = sqrt(g_bar^2 + g_bar*a0) (NOT McGaugh's nu, NOT
simple-mu, NOT canonical a0=1.2e-10 -- Carl's #1 ask). eta(R500) = M_dyn/M_bar (cluster mass
discrepancy). Banked baseline: real eRASS1 (N=9830, WL-calibrated M500, median z=0.298, median
g/a0=0.481) gives eta(R500) = 2.334 framework / 2.073 canonical. No-particle: the framework's own
Y-Q (AeST ghost-condensate) field covers ~17-20% of the residual with NO new particle; the rest is
the shared relativistic-MOND core gap (framework MI == AeST-MG to machine precision in the core --
NOT framework-distinctive, NOT a referee-proof kill).

WHERE WE ARE (READ: XRISM_ETA_PINNING_2026-06-20.md, CLUSTER_GRAVITY_LAST_DOORS_2026-06-20.md, the
cluster memory): XRISM just SHUT the disequilibrium-via-turbulence escape (relaxed clusters are
quiescent, f_nt~2-4%, far below the 44-57% a collapse needs; and non-thermal pressure RAISES a
thermal eta, it cannot lower it -- the sign was inverted in the turbulence lever). So the residual's
MAGNITUDE is now set by a DIFFERENT axis: the WL-vs-HYDRO MASS-PROXY disagreement. The eRASS1 eta=2.33
uses WEAK-LENSING-calibrated masses; the thermal-HYDROSTATIC mass is lower. The two branches:
- WL branch: eta(R500) ~ 2.33 -> residual REAL, shared-MOND gap survives.
- HYDRO branch: eta(R500) ~ 2.33 / (WL/HSE) -> if WL/HSE is large, eta drops toward ~1.0-1.5, where
  the framework's Y-Q field (17-20%) + the lower baseline can plausibly CLOSE the residual (no gap).

THE LOAD-BEARING BOTH-WAYS QUESTION (Carl's #1 rule -- penalize high-priest AND manufacturing EQUALLY):
WHAT IS THE REAL RELAXED-CLUSTER WL/HSE MASS RATIO? The XRISM synth leaned on Li+2024's WL/HSE~2.1
(=> eta_hydro~1.1, near-closed). BUT the CONSENSUS hydrostatic bias is only (1-b)~0.7-0.85, i.e.
WL/HSE ~ 1.2-1.4 (~25-35%), NOT 2.1 -- which would give eta_hydro ~ 1.7-1.9, a STILL-REAL gap the
Y-Q field does NOT close. A WL/HSE~2.1 is anomalously large (2x the standard bias) and may be sample-
specific or a WL over-estimate (projection/triaxiality, Grandis+2024) OR a real large bias. PIN THE
REAL NUMBER from the consensus relaxed-cluster literature (CCCP/Hoekstra, X-COP/Eckert, LoCuSS/Smith,
CLASH/Umetsu, HSC, WtG/Applegate, Lovisari, Sereno, Planck 1-b, the SZ-vs-WL "sigma8 tension" bias).
Use an INDEPENDENT 3rd proxy too (dynamical/caustic/galaxy-sigma masses) to break the WL-vs-X-ray tie.

DECISION: (A) if the real relaxed WL/HSE ~ 1.2-1.4 (consensus bias) => eta_hydro ~ 1.7-1.9 => the
residual is REAL and the Y-Q field does NOT close it (shared-MOND gap stands, ~half-covered). (B) if
the real relaxed WL/HSE is genuinely large (~1.8-2.1, the WL masses over-estimated) => eta_hydro ~
1.1-1.3 => Y-Q field CLOSES it (cluster problem solved, no gap). Report the honest branch. Do NOT
manufacture B by quoting Li+2024's 2.1 if the consensus is 1.3; do NOT high-priest A by ignoring real
evidence of WL over-estimation. QUARANTINE: a0/Z/kappa never asserted derived; a0=9.36e-11 input only.
`

const PULL_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    topic: { type: 'string' },
    samples: { type: 'array', items: { type: 'object', additionalProperties: false, properties: {
      name: { type: 'string', description: 'sample/program (CCCP, X-COP, LoCuSS, CLASH, etc.)' },
      mass_ratio: { type: 'string', description: 'WL/HSE (or the relevant proxy ratio) at R500, relaxed subsample, with error' },
      relaxed_selection: { type: 'string' },
      systematics_note: { type: 'string', description: 'projection/triaxiality/concentration/scatter caveats; is the ratio a real bias or a WL over-estimate?' },
      reference: { type: 'string' },
    }, required: ['name','mass_ratio','relaxed_selection','systematics_note','reference'] } },
    consensus_WL_HSE_ratio: { type: 'string', description: 'the honest consensus relaxed-cluster WL/HSE ratio at R500 with its spread' },
    third_proxy: { type: 'string', description: 'dynamical/caustic/galaxy-sigma mass cross-check, if available' },
    summary_findings: { type: 'string' },
    sources: { type: 'string' },
  },
  required: ['topic','samples','consensus_WL_HSE_ratio','third_proxy','summary_findings','sources'],
}

const COMP_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    calculation: { type: 'string' },
    eta_WL_branch: { type: 'string' },
    eta_hydro_branch: { type: 'string' },
    favored_branch: { type: 'string', enum: ['hydro-closes-no-gap','wl-real-gap','bracketed-undetermined','partial'] },
    yq_field_closes: { type: 'string', enum: ['yes-cluster-solved','no-real-gap-stands','depends-on-proxy'] },
    key_numbers: { type: 'array', items: { type: 'string' } },
    script_path: { type: 'string' },
    both_ways: { type: 'string' },
    sources: { type: 'string' },
  },
  required: ['calculation','eta_WL_branch','eta_hydro_branch','favored_branch','yq_field_closes','key_numbers','script_path','both_ways','sources'],
}

phase('Pull')
const pulls = await parallel([
  () => agent(
`${FRAMEWORK}\n\nPULL #1 -- the RELAXED-CLUSTER WL-vs-X-ray/HYDROSTATIC mass ratio. WebSearch/WebFetch the consensus literature on M_WL/M_HSE (and the hydrostatic bias 1-b) at R500 for RELAXED clusters: CCCP/Hoekstra+2015, X-COP/Eckert+2019 + Ettori+2019, LoCuSS/Smith+Mulroy, CLASH/Umetsu+2016 + Donahue+2014, WtG/Applegate+2016, HSC/Miyatake, Lovisari+2020, Sereno+Ettori (LC2), Planck SZ 1-b, the SZ-vs-WL sigma8-tension bias, and Li+2024 (the WL/HSE~2.1 the XRISM synth used). For EACH: the WL/HSE ratio at R500 on the relaxed subsample + error + the systematics (is the ratio a REAL hydrostatic bias, or a WL OVER-estimate from projection/triaxiality/concentration, Grandis+2024?). Then give the HONEST CONSENSUS relaxed WL/HSE ratio + spread. Be careful: the standard hydrostatic bias is only ~25-35% (WL/HSE~1.2-1.4); a WL/HSE~2.1 is anomalous and needs justification. Return the structured object.`,
    { label: 'pull:wl-hse-ratio', phase: 'Pull', schema: PULL_SCHEMA }
  ),
  () => agent(
`${FRAMEWORK}\n\nPULL #2 -- the INDEPENDENT 3rd MASS PROXY (break the WL-vs-X-ray tie). WebSearch/WebFetch dynamical/kinematic cluster masses that are INDEPENDENT of both WL and X-ray-HSE: galaxy velocity-dispersion (virial) masses, CAUSTIC masses (Diaferio/Rines, HeCS, CIRS), phase-space/Jeans masses, and any splashback-radius masses. For relaxed clusters, how do these DYNAMICAL masses compare to the WL masses and to the X-ray-HSE masses at R500? Which proxy do they side with -- the high (WL) or the low (HSE)? Also pull: does the framework's own MOND/MI prediction for the GALAXY velocity dispersions in clusters (the banked member-sigma work) bear on which mass is right? Return the structured object (use the samples array for the dynamical-mass comparisons).`,
    { label: 'pull:dynamical-3rd-proxy', phase: 'Pull', schema: PULL_SCHEMA }
  ),
])
const pullData = pulls.filter(Boolean)

phase('Compute')
const comp = await agent(
`${FRAMEWORK}\n\nCOMPUTE. Using the pulled mass-proxy data:\n${JSON.stringify(pullData).slice(0,11000)}\n\n(1) Pin the REAL relaxed-cluster mass-proxy bracket (WL high vs HSE low, with the 3rd dynamical proxy breaking the tie). (2) Compute the framework eta(R500) = M_dyn/M_bar on EACH proxy (WL branch ~2.33; hydro branch = 2.33/(WL/HSE)). USE THE CONSENSUS WL/HSE, not the most-favorable. (3) Apply the framework's Y-Q field (17-20% no-particle) to EACH branch: does eta drop to ~1.0 (CLOSED, cluster problem solved) or stay >1.3 (real shared gap)? KEY: if the consensus WL/HSE~1.2-1.4, eta_hydro~1.7-1.9 and the Y-Q field does NOT close it (real gap); if WL/HSE is genuinely ~1.8-2.1 (WL over-estimated), eta_hydro~1.1-1.3 and the Y-Q field DOES close it (solved). Report the honest branch the DATA favors. Both ways -- a genuine close (the dynamical 3rd proxy siding with HSE + WL over-estimate evidence) vs a real gap (consensus ~30% bias only). WRITE a script under opus_48_extended_research/reviews/wl_hydro_eta/. Return the structured object with REAL numbers. Do NOT manufacture the close by cherry-picking Li+2024's 2.1; do NOT high-priest the gap by ignoring real WL-over-estimate evidence.`,
  { label: 'compute:eta-by-proxy', phase: 'Compute', schema: COMP_SCHEMA }
)

phase('Verify')
const verdict = await agent(
`${FRAMEWORK}\n\nSKEPTIC. Prior compute:\n${JSON.stringify(comp).slice(0,9000)}\n\nBOTH WAYS, adversarial (penalize high-priest AND manufacturing EQUALLY). (1) Is the consensus WL/HSE ratio HONEST, or was Li+2024's anomalous ~2.1 used to manufacture the close? Re-pull the consensus (CCCP/X-COP/LoCuSS give ~1.2-1.4 for the relaxed hydrostatic bias). (2) Conversely, is there REAL evidence WL over-estimates relaxed-cluster masses (projection/triaxiality, Grandis+2024) that a high-priest would ignore? (3) Does the 3rd dynamical proxy actually break the tie, or is it being over-read? (4) Re-derive the framework eta on the CONSENSUS ratio and check whether the Y-Q field closes it. (5) Is the Y-Q field 17-20% coverage itself robust? Return: holds_up (solid/partial/overclaimed/dead), the_honest_branch, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label: 'verify', phase: 'Verify', schema: { type:'object', additionalProperties:false, properties:{
    holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']},
    the_honest_branch:{type:'string'}, high_priest_or_manufactured:{type:'string'},
    skeptic_findings:{type:'string'}, corrected:{type:'string'} },
    required:['holds_up','the_honest_branch','high_priest_or_manufactured','skeptic_findings','corrected'] } }
)

phase('Synthesize')
const synth = await agent(
`${FRAMEWORK}\n\nSYNTHESIZE: on the REAL relaxed-cluster mass-proxy evidence, is the framework cluster residual CLOSED (hydro branch + Y-Q field, no gap = the cluster problem solved with no new particle) or a REAL shared-MOND gap (WL branch)?\n\nPULLS:\n${JSON.stringify(pullData).slice(0,6000)}\nCOMPUTE:\n${JSON.stringify(comp).slice(0,5000)}\nVERDICT:\n${JSON.stringify(verdict).slice(0,4000)}\n\nReturn 'report' (markdown) + structured fields. Cover: (1) the honest consensus relaxed-cluster WL/HSE ratio + what the 3rd dynamical proxy says; (2) the framework eta(R500) on each branch; (3) does the Y-Q field close it on the favored branch; (4) the BOTH-WAYS verdict -- solved (no gap) or real shared gap, and the honest uncertainty; (5) what would settle it definitively. Hold quarantine + both-ways: this is the decisive magnitude lever -- neither manufacture a solve nor high-priest a gap.`,
  { label: 'synthesize', phase: 'Synthesize', schema: { type:'object', additionalProperties:false, properties:{
    report:{type:'string'}, verdict:{type:'string', enum:['cluster-residual-closed-no-gap','real-shared-mond-gap','bracketed-genuinely-uncertain','partial-closed']},
    consensus_ratio:{type:'string'}, eta_favored:{type:'string'}, solved_or_gap:{type:'string'}, what_would_settle:{type:'string'} },
    required:['report','verdict','consensus_ratio','eta_favored','solved_or_gap','what_would_settle'] } }
)
return { synth, comp, verdict, pulls: pullData }
