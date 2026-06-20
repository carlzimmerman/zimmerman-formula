export const meta = {
  name: 'xrism-eta-pinning',
  description: "The program's own identified sharpest live lever: pin the cluster MOND residual MAGNITUDE with the REAL XRISM (Resolve) cluster bulk/turbulent-velocity data published 2024-2026. The eRASS1 eta(R500)=2.33 assumes hydrostatic equilibrium; XRISM directly measures the non-thermal pressure that would inflate the apparent residual. Pull the real XRISM velocity sample -> apply the non-thermal HSE correction -> re-derive eta(R500) on the framework's dS-Unruh footing (a0=9.36e-11) -> both-ways verdict: does the residual collapse toward ~1.0-1.3 (framework's own field covers it, no gap) or stay ~2.0-2.3 (real shared-MOND gap)? Decisive either way.",
  phases: [
    { title: 'Pull', detail: 'real XRISM/Resolve cluster velocity measurements 2024-2026 + the HSE-bias / non-thermal-pressure baseline' },
    { title: 'Compute', detail: 'assemble the XRISM relaxed-cluster sample, apply the non-thermal correction, re-derive eta(R500) on the framework footing, both ways' },
    { title: 'Verify', detail: 'adversarial: correction applied right? sample representative? not manufactured-down, not high-priest-up' },
    { title: 'Synthesize', detail: 'the honest verdict on what XRISM-to-date says about the residual MAGNITUDE + the decision tree' },
  ],
}

const FRAMEWORK = `
FRAMEWORK (Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2, modified-INERTIA MOND, the
framework's OWN dS-Unruh interpolation g_obs = sqrt(g_bar^2 + g_bar*a0) (NOT McGaugh's nu, NOT
simple-mu, NOT canonical a0=1.2e-10 -- Carl's #1 ask, use the framework's own footing). eta(R500)
= M_dyn/M_bar (the cluster mass discrepancy). The banked standing (READ the memory + reviews):
real eRASS1 (N=9830) median eta(R500) = 2.33 on the framework's OWN dS-Unruh interp (eta-worst,
+13% surcharge for the lower a0; canonical a0 -> 2.07). The deficit is CENTRAL + soft (dies to ~1
by 2-3 Mpc). No-particle coverage ~50-71% (relaxed A2029, MOND-on-gas), ~30-49% irreducible SHARED
relativistic-MOND gap. The framework's MI == AeST modified-gravity to machine precision in the core,
so the gap is common to the WHOLE MOND family, NOT framework-specific, and NOT a referee-proof kill.

THE LEVER (the program's own identified sharpest live test -- CLUSTER_GRAVITY_LAST_DOORS_2026-06-20.md,
DOORS_RUN_RESULTS): the eRASS1 eta=2.33 assumes HYDROSTATIC EQUILIBRIUM (the X-ray gas pressure
balances gravity, thermal-only). If clusters carry significant NON-THERMAL pressure (bulk flows +
turbulence), the true HSE mass is UNDER-estimated by the thermal-only calc, which INFLATES the
apparent MOND residual. P_nt/P_tot ~ 10-25% in sims (Nelson, Lau, Angelinelli). XRISM (X-ray Imaging
and Spectroscopy Mission, Resolve microcalorimeter, launched Sept 2023) is the FIRST instrument to
DIRECTLY measure the gas line-of-sight velocity dispersion (turbulence) + bulk velocity in clusters
at eV resolution. It collapses the eta(R500) equilibrium bracket (1.0, 2.33) toward its TRUE value.
SURPRISE so far: XRISM has found cluster cores SURPRISINGLY QUIESCENT (Centaurus, Coma low
turbulence, P_nt ~ few %) -- which, if it holds, means the HSE mass is RELIABLE and the residual is
REAL (and shared-MOND), NOT a disequilibrium artifact.

THE BOTH-WAYS DECISION (Carl's #1 rule -- verify a "fails/works" claim equally; penalize high-priest
AND manufacturing EQUALLY): (A) if the XRISM-measured P_nt is LARGE enough that the corrected
eta(R500) drops toward ~1.0-1.3, the "residual" is mostly a disequilibrium artifact -> the framework's
OWN Y-Q field (~17-20%) covers what's left -> NO irreducible gap (a WIN, report at full weight). (B)
if XRISM confirms LOW turbulence (P_nt ~ few %), the HSE mass is reliable -> eta stays ~2.0-2.3 -> the
residual is REAL and CONFIRMED shared-MOND (NOT framework-distinctive, NOT a kill -- the whole MOND
family inherits it; report straight). Either way is decisive and publishable. Do NOT manufacture a
collapse; do NOT high-priest a real residual. QUARANTINE: a0/Z/kappa never asserted derived.
`

const PULL_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    topic: { type: 'string' },
    clusters: { type: 'array', items: { type: 'object', additionalProperties: false, properties: {
      name: { type: 'string' },
      relaxed_or_merging: { type: 'string' },
      sigma_turb_kms: { type: 'string', description: 'measured turbulent LOS velocity dispersion + radius/region + error' },
      v_bulk_kms: { type: 'string' },
      P_nt_fraction: { type: 'string', description: 'non-thermal pressure fraction if reported or derivable' },
      reference: { type: 'string', description: 'arXiv id / journal, 2024-2026' },
    }, required: ['name','relaxed_or_merging','sigma_turb_kms','v_bulk_kms','P_nt_fraction','reference'] } },
    summary_findings: { type: 'string' },
    data_completeness: { type: 'string', description: 'honest assessment of how much usable XRISM cluster-velocity data exists to date' },
    sources: { type: 'string' },
  },
  required: ['topic','clusters','summary_findings','data_completeness','sources'],
}

const COMP_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    calculation: { type: 'string', description: 'the actual non-thermal HSE correction + framework eta(R500) re-derivation with real numbers' },
    eta_corrected: { type: 'string', description: 'the corrected eta(R500) range on the framework footing after the XRISM non-thermal correction' },
    direction: { type: 'string', enum: ['collapses-to-1.0-1.3-no-gap','partial-reduction','stays-high-2.0-2.3-real-gap','data-too-thin'] },
    residual_real_or_artifact: { type: 'string', enum: ['mostly-real-shared','mostly-disequilibrium-artifact','mixed','undetermined'] },
    key_numbers: { type: 'array', items: { type: 'string' } },
    script_path: { type: 'string' },
    both_ways: { type: 'string' },
    sources: { type: 'string' },
  },
  required: ['calculation','eta_corrected','direction','residual_real_or_artifact','key_numbers','script_path','both_ways','sources'],
}

phase('Pull')
const pulls = await parallel([
  () => agent(
`${FRAMEWORK}\n\nPULL #1 -- the PRIMARY DATA. Do a thorough WebSearch/WebFetch sweep of ALL published XRISM (Resolve) galaxy-CLUSTER velocity measurements 2024-2026: Centaurus (A3526), Coma, Virgo/M87, A2029, Perseus, Ophiuchus, Abell 2319, Hydra A, Abell 2256, Cygnus A, and any others. For EACH, extract the measured turbulent LOS velocity dispersion sigma_turb, bulk velocity v_bulk, the region/radius, relaxed-vs-merging classification, and the non-thermal pressure fraction P_nt/P_tot (reported or derivable as P_nt/P_th ~ (sigma_turb/c_s)^2-ish, or rho*sigma^2 vs thermal). Be HONEST about data completeness -- XRISM launched Sept 2023, PV 2024, GO cycle-1 2024-2025, so the sample may be thin. Return the structured object. Focus on RELAXED cool-core clusters (the eta-pinning targets).`,
    { label: 'pull:xrism-velocities', phase: 'Pull', schema: PULL_SCHEMA }
  ),
  () => agent(
`${FRAMEWORK}\n\nPULL #2 -- the BASELINE for the correction. WebSearch/WebFetch: (a) the non-thermal-pressure / HSE-mass-bias literature (Nelson+2014, Lau+2009/2013, Angelinelli+2020, Eckert+2019 X-COP, Pratt+2019 review) -- what P_nt/P_tot fraction at R500 do sims+data give, and how much does it bias the HSE mass / inflate the apparent MOND residual? (b) the eROSITA eRASS1 + CLASH/X-COP eta(R500) baseline the framework uses (the banked 2.33). (c) how the non-thermal correction maps to eta: M_HSE_thermal = M_true*(1 - P_nt/P_tot), so correcting RAISES M_bar's apparent partner... actually RAISES M_dyn estimate? Resolve the direction CAREFULLY: non-thermal pressure means thermal-only HSE UNDER-estimates the true mass, so the TRUE M_dyn is HIGHER than the thermal HSE -> the apparent eta (using thermal HSE) is an UNDER-estimate of the true discrepancy? OR does adding the non-thermal support to the mass budget mean less GRAVITY is needed -> lower eta? Get the sign EXACTLY right and state it. Return the structured object (use the clusters array loosely for any velocity data you find, else focus summary_findings on the correction physics + sign).`,
    { label: 'pull:hse-bias-baseline', phase: 'Pull', schema: PULL_SCHEMA }
  ),
])
const pullData = pulls.filter(Boolean)

phase('Compute')
const comp = await agent(
`${FRAMEWORK}\n\nCOMPUTE. Using the pulled XRISM velocity data + the HSE-bias baseline:\n${JSON.stringify(pullData).slice(0,11000)}\n\nAssemble the XRISM RELAXED-cluster sample. For each cluster with usable data: (1) compute the non-thermal pressure fraction P_nt/P_tot from the measured sigma_turb (P_nt = rho_gas*sigma_turb^2, P_th = n*k*T -> fraction); (2) apply the HSE correction to get the TRUE dynamical mass M_dyn (get the SIGN right -- non-thermal support means thermal-only HSE under-estimates the true gravitating mass, so M_dyn_true = M_HSE_thermal/(1 - P_nt/P_tot)); (3) re-derive eta(R500) = M_dyn/M_bar on the framework's OWN dS-Unruh footing (a0=9.36e-11) BEFORE and AFTER the correction. KEY QUESTION: does the XRISM-corrected eta(R500) COLLAPSE toward ~1.0-1.3 (framework's own ~17-20% field covers it -> NO irreducible gap) or STAY ~2.0-2.3 (the HSE was reliable -> the residual is REAL and shared-MOND)? Both ways -- a genuine collapse (WIN) vs a confirmed real residual (shared-MOND, not a kill). If the XRISM turbulence is genuinely LOW (P_nt ~ few %), the correction is SMALL and eta stays high = the residual is real -- report that straight, do NOT manufacture a collapse. WRITE a script under opus_48_extended_research/reviews/xrism_eta/. Return the structured object with REAL numbers.`,
  { label: 'compute:eta-correction', phase: 'Compute', schema: COMP_SCHEMA }
)

phase('Verify')
const verdict = await agent(
`${FRAMEWORK}\n\nSKEPTIC. Prior compute:\n${JSON.stringify(comp).slice(0,9000)}\n\nBOTH WAYS, adversarial (penalize high-priest AND manufacturing EQUALLY). (1) Is the non-thermal correction SIGN right (does P_nt RAISE or LOWER the true M_dyn, and does that raise or lower eta)? Re-derive it from first principles (the HSE equation with thermal + non-thermal pressure). (2) Is the XRISM sample REPRESENTATIVE (cores only? R500 reach? relaxed selection?) -- XRISM measures the CORE turbulence but eta(R500) needs the pressure at R500, which may differ (turbulence often RISES outward). Flag if the core P_nt is being wrongly extrapolated to R500. (3) Is any "collapse to 1.0-1.3" MANUFACTURED (too-large P_nt, wrong extrapolation) or any "stays high" HIGH-PRIEST (ignoring real non-thermal support)? (4) Re-run the load-bearing number. Return a verdict: holds_up (solid/partial/overclaimed/dead), the_honest_direction, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label: 'verify', phase: 'Verify', schema: { type:'object', additionalProperties:false, properties:{
    holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']},
    the_honest_direction:{type:'string'}, high_priest_or_manufactured:{type:'string'},
    skeptic_findings:{type:'string'}, corrected:{type:'string'} },
    required:['holds_up','the_honest_direction','high_priest_or_manufactured','skeptic_findings','corrected'] } }
)

phase('Synthesize')
const synth = await agent(
`${FRAMEWORK}\n\nSYNTHESIZE: what does the REAL XRISM cluster-velocity data published to date say about the cluster MOND residual MAGNITUDE on the framework's footing?\n\nPULLS:\n${JSON.stringify(pullData).slice(0,6000)}\n\nCOMPUTE:\n${JSON.stringify(comp).slice(0,5000)}\n\nVERDICT:\n${JSON.stringify(verdict).slice(0,4000)}\n\nReturn 'report' (markdown) + the structured fields. Cover: (1) what XRISM has actually measured to date (the sample + its limits -- be honest if thin); (2) the non-thermal correction + its SIGN, settled; (3) the corrected eta(R500) on the framework footing, before/after; (4) the BOTH-WAYS verdict -- does XRISM-to-date COLLAPSE the residual (no gap, a win) or CONFIRM it real (shared-MOND, not a kill)?; (5) what's still needed (which clusters, what R500 reach) to fully settle it. Hold quarantine + both-ways; this is the program's decisive observational lever -- report the honest direction, neither manufactured-down nor high-priest-up.`,
  { label: 'synthesize', phase: 'Synthesize', schema: { type:'object', additionalProperties:false, properties:{
    report:{type:'string'}, verdict:{type:'string', enum:['residual-collapses-no-gap','residual-confirmed-real-shared','data-too-thin-to-settle','partial-reduction']},
    eta_after_xrism:{type:'string'}, what_xrism_measured:{type:'string'}, still_needed:{type:'string'} },
    required:['report','verdict','eta_after_xrism','what_xrism_measured','still_needed'] } }
)
return { synth, comp, verdict, pulls: pullData }
