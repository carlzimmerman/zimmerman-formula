export const meta = {
  name: 'a0-law-of-nature',
  description: "Build the HONEST, referee-proof case that a0=c^2 sqrt(Lambda/32pi)=9.36e-11 is a LAW OF NATURE -- with real Python on real SPARC data. Four routes: (1) the RAR as an EMPIRICAL LAW (near-zero intrinsic scatter, a0 universal across galaxy mass/type/gas-fraction, 'too tight' for LCDM); (2) the BTFR as a LAW (slope-4, near-zero scatter, normalization->a0); (3) the FORM structurally FORCED (4 mechanisms force a0 prop c^2 sqrt(Lambda); the sqrt(8pi/3) kernel incl half-integer pi; the dS-Unruh interpolation); (4) the COSMIC COINCIDENCE a0~c sqrt(Lambda)~cH0 quantified (FDR, structural). The HONEST BOUNDARY (both-ways, quarantine): it is a ONE-PARAMETER law (Lambda input + kappa=1/2, value NOT derived parameter-free) -- a geometric constant like G/alpha, not a zero-parameter derivation; clusters a real bounded shared-MOND tension, not a law violation.",
  phases: [
    { title: 'Build', detail: 'four parallel routes: RAR-law, BTFR-law, forced-form, cosmic-coincidence -- real Python, real SPARC' },
    { title: 'Verify', detail: 'adversarial both-ways: is the law-of-nature case genuine or overclaimed; hold the quarantine (value not derived)' },
    { title: 'Synthesize', detail: 'the honest law-of-nature thesis + the cluster connection + the one-parameter boundary' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = cH_Lambda/Z = 9.36e-11 m/s^2,
Z=sqrt(32pi/3)=5.7888. MODIFIED-INERTIA MOND from de Sitter-Unruh T_eff=(hbar/2pi c k_B)sqrt(a^2+(cH_L)^2)
(Deser-Levin), interpolation mu_fw(x)=(sqrt(1+4x^2)-1)/(2x), g_obs=sqrt(g_bar^2+g_bar*a0). The published
paper (DESITTER_GAUGE_MOND_SCALE.md): the deep-MOND FORM a0 prop c^2 sqrt(Lambda) is OVER-DETERMINED --
an FDR-controlled audit certifies FOUR structurally-independent mechanisms force it; the gravitational
route fixes the kernel sqrt(8pi/3) INCLUDING the half-integer power of pi that no curvature-free thermal
route produces, leaving the residual as ONE O(1) number kappa=1/2 (a0 = half the free-fall accel at the
dark-energy density). Independently re-derived by Luo 2026 (arXiv:2602.14515, same dS-Unruh T_eff).

THE TASK (Carl: "why my framework and MOND scaling value IS a law of nature" -- build the HONEST,
referee-proof case with REAL Python on REAL data): a0 is a LAW OF NATURE in the defensible sense --
(A) EMPIRICALLY UNIVERSAL (the RAR/BTFR are law-like: near-zero intrinsic scatter, a0 invariant across
galaxy properties, independent of formation history -- the signature of a law, not a fitted halo); (B)
its FORM is structurally FORCED (de Sitter geometry, 4 mechanisms, the sqrt(8pi/3) kernel); (C) it ties
galaxies to the cosmological constant via a near-exact STRUCTURAL coincidence (a0~c sqrt(Lambda)~cH0).

THE HONEST BOUNDARY (BOTH-WAYS -- Carl's #1 rule, penalize high-priest AND manufacturing EQUALLY; this
is the line that makes the claim referee-proof): a0 is a ONE-PARAMETER law -- the VALUE takes Lambda as
an INPUT and kappa=1/2 as the one O(1) number (provably UNFORCEABLE -- banked KAPPA_FORCING_DOOR_CLOSED).
It is a constant of nature like G, alpha, Lambda -- whose FORM is forced and whose VALUE is set by ONE
cosmological input -- NOT a zero-parameter derivation. DO NOT claim a0/Z/kappa are derived from nothing
(quarantine). DO NOT claim the framework is a completed TOE (it is "an effective theory at a frontier").
The genuine law-of-nature case is: empirical universality + forced form + structural coincidence + one
input -- that is a STRONG, true claim; the manufactured version (parameter-free derivation) is FALSE and
must be refused. Make the strong TRUE case; refuse the false one.

DATA: real SPARC rotation curves at real_research/data/sparc_data (175 galaxies, Ups=0.70 framework
footing -- USE THE FRAMEWORK'S OWN dS-Unruh interpolation, Carl's #1 ask). Quarantine: a0=9.36e-11 INPUT.
WebSearch/WebFetch the RAR/BTFR universality + the "too-tight RAR for LCDM" literature (McGaugh, Lelli,
Desmond, Keller-Wadsley, Stiskalek). sympy/numpy.
`

const SCH = (extra) => ({ type:'object', additionalProperties:false, properties: Object.assign({
  route:{type:'string'}, finding:{type:'string'},
  law_strength:{type:'string', description:'how law-like, with the real numbers (scatter, universality, forcing)'},
  key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'},
  honest_boundary:{type:'string', description:'what this route does NOT prove (the quarantine line)'},
  sources:{type:'string'} }, extra),
  required:['route','finding','law_strength','key_numbers','honest_boundary','sources'] })

const ROUTES = [
  { key:'rar_law', p:`ROUTE 1 -- the RAR as an EMPIRICAL LAW (real SPARC, framework dS-Unruh nu, Ups=0.70). Compute: (1) the ORTHOGONAL INTRINSIC scatter of the RAR -- is it consistent with the observational-error floor (i.e. ~ZERO intrinsic, the signature of a law)? Decompose total (~0.13 dex) into error + intrinsic. (2) UNIVERSALITY: bin SPARC by stellar mass, gas fraction, surface brightness, morphology/type -- does the best-fit a0 VARY across bins? A law => a0 invariant. Quantify the variation + its significance. (3) The LCDM comparison: LCDM predicts RAR scatter from halo concentration + formation history (~0.2-0.3 dex expected); the observed ~0.13 dex is "too tight" -- quantify how many sigma the observed scatter is BELOW the LCDM expectation (the law-like-ness that challenges LCDM). Both ways -- is a0 genuinely universal, or does it drift with galaxy property?` },
  { key:'btfr_law', p:`ROUTE 2 -- the BTFR as a LAW (real SPARC). Compute: (1) the BTFR slope M_bar prop V^x -- is x=4 (MOND/framework) vs 3 (LCDM)? Fit on SPARC, with error. (2) the SCATTER -- is the BTFR near-zero intrinsic scatter (one of the tightest known scaling relations)? (3) the NORMALIZATION -> a0: M_bar = V^4/(G a0), so the BTFR zero-point GIVES a0; what a0 does the SPARC BTFR normalization imply, and is it consistent with 9.36e-11? (4) is the slope EXACTLY 4 (a law) or a fitted power? Both ways. The BTFR as an independent law-like determination of a0.` },
  { key:'forced_form', p:`ROUTE 3 -- the FORM is structurally FORCED (verify the published content, do NOT re-derive from scratch; confirm + sharpen). (1) the FOUR mechanisms that force a0 prop c^2 sqrt(Lambda) (the FDR-audited count from DESITTER_GAUGE_MOND_SCALE.md -- name + verify each); (2) the sqrt(8pi/3) kernel INCLUDING the half-integer power of pi -- why the gravitational route fixes it and no curvature-free thermal route does (sympy the kernel); (3) the dS-Unruh interpolation mu_fw(x)=(sqrt(1+4x^2)-1)/(2x) reproducing flat rotation curves + v^4=GMa0 (sympy); (4) THE HONEST BOUNDARY: the VALUE needs Lambda (input) + kappa=1/2 (the one O(1), provably unforceable). State clearly: the FORM is forced (law-like), the VALUE is one-parameter (NOT derived). Both ways -- credit the forcing, hold the quarantine.` },
  { key:'cosmic_coincidence', p:`ROUTE 4 -- the COSMIC COINCIDENCE quantified (why it is a law, not an accident). (1) compute a0 vs c sqrt(Lambda) vs cH0 vs cH0/2pi -- the precise ratios + how close (the framework's 9.36e-11 vs the measured galactic a0~1.2e-10 vs c sqrt(Lambda) vs cH0); (2) the FDR / chance probability: how unlikely is the a0~c sqrt(Lambda)~cH0 triple coincidence by chance across the plausible acceleration scales (the paper's FDR audit -- reproduce); (3) the STRUCTURAL explanation: a0 = the de Sitter curvature scale, so the coincidence is CAUSAL (dS-Unruh) not accidental -- the law TIES galactic dynamics to the cosmological constant; (4) does the coincidence survive the a0 uncertainty + the Lambda value? Both ways -- is it a genuine structural law or a numerological near-miss?` },
]

phase('Build')
const builds = await parallel(ROUTES.map(r => () =>
  agent(`${FW}\n\n${r.p}\n\nWRITE a script under opus_48_extended_research/reviews/a0_law/. Return the structured object with REAL numbers. Both-ways; hold the quarantine.`,
    { label:`build:${r.key}`, phase:'Build', schema: SCH({}) })
))
const B = builds.filter(Boolean)

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways (this is the referee). The four routes:\n${JSON.stringify(B).slice(0,12000)}\n\nCheck HARD, penalizing high-priest AND manufacturing EQUALLY: (1) is the RAR intrinsic-scatter ~zero claim real (not an artifact of the error model)? is a0 genuinely universal across bins, or does it drift? (2) is the BTFR slope genuinely ~4 and the normalization genuinely giving a0~9.36e-11? (3) is the "4 mechanisms force the form" honest (or are some weak/overlapping)? is the kernel sqrt(8pi/3) genuinely gravitational? (4) is the coincidence genuinely structural (FDR-robust) or numerological? (5) THE KEY LINE: does any route OVERCLAIM a parameter-free derivation (manufacturing)? does the synthesis honestly state it is a ONE-PARAMETER law (Lambda + kappa)? (6) re-run a load-bearing number per route. Return: holds_up (solid/partial/overclaimed/dead), law_of_nature_verdict (the honest strength), overclaim_flags, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, law_of_nature_verdict:{type:'string'}, overclaim_flags:{type:'string'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','law_of_nature_verdict','overclaim_flags','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE the HONEST "a0 is a law of nature" thesis (referee-proof, for Carl).\nBUILDS:\n${JSON.stringify(B).slice(0,8000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4000)}\n\nReturn 'report' (markdown, paper-quality) + fields. Structure: (1) THE EMPIRICAL CASE -- the RAR + BTFR are law-like (near-zero intrinsic scatter, a0 universal across galaxy properties, 'too tight' for LCDM) -- the real numbers; (2) THE STRUCTURAL CASE -- the form a0=c^2 sqrt(Lambda/32pi) is forced (4 mechanisms, the sqrt(8pi/3) kernel, dS-Unruh); (3) THE COINCIDENCE -- a0~c sqrt(Lambda)~cH0 is structural not accidental; (4) THE HONEST BOUNDARY -- it is a ONE-PARAMETER law (Lambda input + kappa=1/2, value NOT derived parameter-free), a constant of nature like G/alpha/Lambda, NOT a TOE; (5) THE CLUSTER CONNECTION -- if a0 is THIS law-like in galaxies (RAR <0.13 dex), the cluster residual is a real BOUNDED SHARED-MOND tension pointing to cluster-specific physics/measurement (the running measurement audit), NOT a violation of the law. The honest bottom line: a0 is a law-like geometric constant of nature with one cosmological input -- a strong TRUE claim, neither high-priested nor manufactured into a parameter-free derivation. Both-ways, quarantine.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['law-like-geometric-constant-one-input','strong-but-overclaimed','suggestive-not-law']}, empirical_strength:{type:'string'}, the_honest_boundary:{type:'string'}, cluster_connection:{type:'string'} }, required:['report','verdict','empirical_strength','the_honest_boundary','cluster_connection'] } })
return { synth, builds: B, ver }
