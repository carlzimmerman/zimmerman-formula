export const meta = {
  name: 'rar-shape-lensing',
  description: "Test the framework's DISTINCTIVE interpolation SHAPE (the dS-Unruh nu=sqrt(1+a0/g), g_obs=sqrt(g_bar^2+g_bar*a0)) against the GLOBAL radial-acceleration relation -- the SPARC dynamical RAR PLUS the weak-lensing RAR (Brouwer+2021 KiDS + 2024-2026 DES/HSC/Euclid), which extends ~2-3 decades BELOW where rotation curves reach (g<<a0, deep-MOND) and tests the functional FORM far more stringently. The a0 VALUE is non-diagnostic (banked); the SHAPE is a sharp falsifiable prediction. Does dS-Unruh nu fit the global RAR as well as / better than / worse than McGaugh-nu and simple-mu, and does the lensing deep-MOND tail confirm or break it? Both-ways, framework footing, quarantine.",
  phases: [
    { title: 'Pull', detail: 'the weak-lensing RAR data (Brouwer+2021 KiDS + 2024-2026 DES/HSC/Euclid) + the SPARC dynamical RAR + the candidate interpolations' },
    { title: 'Compute', detail: 'fit dS-Unruh nu vs McGaugh-nu vs simple-mu to the global (dynamics+lensing) RAR; the deep-MOND tail; scatter, slope, saturation' },
    { title: 'Verify', detail: 'adversarial: is dS-Unruh favored/disfavored, the lensing no-slip assumption, the deep-MOND extrapolation, a0-vs-shape degeneracy' },
    { title: 'Synthesize', detail: 'does the framework SHAPE survive the global RAR; distinctive signature; what settles it' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0=c^2 sqrt(Lambda/32pi)=9.36e-11, MODIFIED-INERTIA MOND. The framework's OWN
interpolation is the dS-Unruh form g_obs=sqrt(g_bar^2+g_bar*a0), i.e. nu(g_bar)=g_obs/g_bar=
sqrt(1+a0/g_bar), or in McGaugh's y=g_obs variable a SPECIFIC shape. This is DIFFERENT from McGaugh's
nu_e=1/(1-exp(-sqrt(g/a0))) (the standard RAR fit) and from the simple-mu (mu=x/(1+x)). The a0 VALUE
is non-diagnostic (banked: RAR optimum a0 spans 7.5e-11..1.8e-10 across interpolation x M/L choices,
penalty <=2%, 9.36e-11 within 0.5% of optimal on the framework's OWN nu -- so the a0 value cannot be
used to confirm/deny the framework). BUT the SHAPE of the dS-Unruh interpolation is a DISTINCTIVE,
falsifiable functional-form prediction, and the place it is tested hardest is the DEEP-MOND regime
g<<a0, which ROTATION CURVES barely reach (SPARC bottoms out ~g~0.1 a0) but GALAXY-GALAXY WEAK LENSING
reaches ~2-3 decades lower (g~1e-2 to 1e-3 a0, out to ~Mpc). Brouwer+2021 (arXiv:2106.11677, KiDS-1000)
measured the LENSING RAR out to g~1e-12 m/s^2 and found it consistent with the dynamical a0 + the
deep-MOND sqrt(g_bar a0) slope -- a clean extension. The framework predicts (AeST no-slip, banked) the
LENSING mass = the dynamical mass, so the lensing RAR should follow the SAME dS-Unruh g_obs at the
SAME a0.

THE JOB (both-ways): (1) fit the dS-Unruh nu vs McGaugh-nu vs simple-mu to the GLOBAL RAR = SPARC
dynamical (real_research/data/sparc_data, Ups=0.70) + the weak-lensing RAR (Brouwer+2021 + any 2024-26
DES/HSC/Euclid lensing-RAR); (2) in the DEEP-MOND tail (g<<a0) where the shapes DIVERGE most and the
lensing data lives, is dS-Unruh FAVORED, DISFAVORED, or INDISTINGUISHABLE vs the standard
interpolations? (3) does the lensing RAR a0 MATCH the dynamical a0 (the framework's no-slip
prediction)? (4) is there a DISTINCTIVE dS-Unruh signature (e.g. the high-g approach to Newton, the
transition curvature, the deep-MOND normalization) the data can see? BOTH-WAYS (Carl #1: do NOT
manufacture a shape-win; do NOT high-priest a real shape-tension; report convention-robustly, run on
the framework's OWN nu but show the spread vs McGaugh/simple). QUARANTINE a0/Z/kappa never derived
(a0=9.36e-11 INPUT). sympy/numpy on REAL SPARC + the published lensing-RAR points. WebSearch/WebFetch
Brouwer+2021 + 2024-2026 lensing-RAR updates for the data points + errors.
`

const PULL_SCHEMA = { type:'object', additionalProperties:false, properties:{
  topic:{type:'string'},
  lensing_rar_points:{type:'array', items:{type:'string'}, description:'the (g_bar, g_obs) lensing-RAR data points + errors + g-range, from Brouwer+2021 and any 2024-26 update'},
  interpolations:{type:'string', description:'the dS-Unruh, McGaugh, simple-mu functional forms + where they diverge'},
  deep_mond_reach:{type:'string', description:'how low in g/a0 the lensing RAR reaches vs SPARC rotation curves'},
  key_facts:{type:'array', items:{type:'string'}},
  sources:{type:'string'} },
  required:['topic','lensing_rar_points','interpolations','deep_mond_reach','key_facts','sources'] }

const COMP_SCHEMA = { type:'object', additionalProperties:false, properties:{
  calculation:{type:'string'},
  dsunruh_vs_alternatives:{type:'string', enum:['dsunruh-favored','indistinguishable','dsunruh-disfavored','data-too-noisy']},
  lensing_a0_matches_dynamical:{type:'string'},
  deep_mond_verdict:{type:'string', description:'does the lensing deep-MOND tail confirm or break the dS-Unruh shape'},
  distinctive_signature:{type:'string'},
  key_numbers:{type:'array', items:{type:'string'}},
  script_path:{type:'string'}, both_ways:{type:'string'}, sources:{type:'string'} },
  required:['calculation','dsunruh_vs_alternatives','lensing_a0_matches_dynamical','deep_mond_verdict','distinctive_signature','key_numbers','script_path','both_ways','sources'] }

phase('Pull')
const pulls = await parallel([
  () => agent(`${FW}\n\nPULL #1 -- the WEAK-LENSING RAR data. WebSearch/WebFetch Brouwer, Visser, Dvornik, Hoekstra et al. 2021 (arXiv:2106.11677, KiDS-1000 GGL RAR) -- extract the measured (g_bar, g_obs) lensing-RAR points, errors, the g-range reached (down to ~1e-12 m/s^2), the fitted a0 and the deep-MOND slope. Plus any 2024-2026 lensing-RAR update (DES Y3, HSC, Euclid Q1, KiDS-Legacy). And the interpolation forms: dS-Unruh g_obs=sqrt(g_bar^2+g_bar*a0), McGaugh nu_e=1/(1-exp(-sqrt(g/a0))), simple-mu -- and WHERE they diverge (the deep-MOND normalization + the transition). Return the structured object.`,
    { label:'pull:lensing-rar', phase:'Pull', schema: PULL_SCHEMA }),
  () => agent(`${FW}\n\nPULL #2 -- the SPARC dynamical RAR + the framework's no-slip lensing prediction. Confirm: (a) the SPARC RAR (real_research/data/sparc_data) g-range, the McGaugh+2016 a0=1.2e-10/scatter 0.13 dex baseline, and the framework's dS-Unruh fit (banked: optimum ~1.0e-10, 9.36e-11 within 0.5%); (b) the framework's AeST no-slip prediction that LENSING mass = DYNAMICAL mass (so the lensing RAR must follow the SAME g_obs at the SAME a0 -- a genuine cross-channel test); (c) where dS-Unruh and McGaugh's nu_e differ in the DEEP-MOND tail (the normalization constant of g_obs=sqrt(g_bar a0)) -- do they predict the SAME deep-MOND asymptote or different? Return the structured object.`,
    { label:'pull:sparc-noslip', phase:'Pull', schema: PULL_SCHEMA }),
])
const P = pulls.filter(Boolean)

phase('Compute')
const comp = await agent(`${FW}\n\nCOMPUTE. Using:\n${JSON.stringify(P).slice(0,10000)}\n\n(1) Build the GLOBAL RAR = SPARC dynamical points (real data, Ups=0.70) + the Brouwer+2021 lensing-RAR points (+ any 2024-26). (2) Fit/overlay the dS-Unruh g_obs=sqrt(g_bar^2+g_bar*a0) [a0=9.36e-11], McGaugh nu_e, and simple-mu. (3) In the DEEP-MOND tail (g<<a0, the lensing regime) where the shapes diverge most: compute the residuals/scatter of EACH interpolation vs the lensing points -- is dS-Unruh FAVORED, INDISTINGUISHABLE, or DISFAVORED? (4) Does the lensing-RAR a0 MATCH the dynamical a0 (the no-slip cross-channel test)? (5) Is there a DISTINCTIVE dS-Unruh signature the global data can see (the deep-MOND normalization sqrt(g_bar a0) is interpolation-INDEPENDENT, so the discriminating power is in the TRANSITION + high-g -- quantify)? WRITE a script under opus_48_extended_research/reviews/rar_shape/. Both-ways; quarantine. Return the structured object with REAL numbers.`,
  { label:'compute:rar-shape', phase:'Compute', schema: COMP_SCHEMA })

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways. Prior:\n${JSON.stringify(comp).slice(0,9000)}\n\nCheck: (1) the deep-MOND asymptote g_obs->sqrt(g_bar a0) is interpolation-INDEPENDENT -- so does the lensing tail actually DISCRIMINATE dS-Unruh from McGaugh, or only test the SHARED deep-MOND limit + a0? (Be honest: if the discriminating power is weak, say so -- do not manufacture a shape-win.) (2) is the no-slip lensing-a0=dynamical-a0 match real or assumed? (3) is dS-Unruh genuinely favored/disfavored, or indistinguishable within errors? (4) a0-vs-shape degeneracy -- can a shape difference be reabsorbed by shifting a0? (5) re-run the load-bearing scatter comparison. Return: holds_up (solid/partial/overclaimed/dead), honest_shape_verdict, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, honest_shape_verdict:{type:'string'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','honest_shape_verdict','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE the RAR-shape / lensing front.\nCOMPUTE:\n${JSON.stringify(comp).slice(0,5000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4000)}\n\nReturn 'report' (markdown) + fields. Cover: does the framework's dS-Unruh SHAPE survive the global (dynamics+lensing) RAR; is it distinguishable from McGaugh/simple-mu (honestly -- the deep-MOND asymptote is shared, so where is the real discriminating power); does the lensing a0 match the dynamical a0 (no-slip); the distinctive signature if any; what would settle it (Euclid/Rubin precision lensing-RAR). Both-ways, quarantine, convention-honest.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string', enum:['shape-survives-distinctive','shape-survives-indistinguishable','shape-tension','data-too-noisy']}, lensing_a0_match:{type:'string'}, discriminating_power:{type:'string'}, what_settles_it:{type:'string'} }, required:['report','verdict','lensing_a0_match','discriminating_power','what_settles_it'] } })
return { synth, comp, ver, pulls: P }
