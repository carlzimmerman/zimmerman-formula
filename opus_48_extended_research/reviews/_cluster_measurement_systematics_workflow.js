export const meta = {
  name: 'cluster-measurement-systematics',
  description: "Carl's question: what about the galaxy-cluster MEASUREMENTS is wrong, such that the ~1.6-1.8 residual (after the framework's own field) is an artifact? Two escapes already shut (XRISM turbulence; WL-vs-hydro ~20% bias). This audits the UN-examined side: the BARYON CENSUS (the DENOMINATOR of eta=M_dyn/M_bar). Candidates: bottom-heavy IMF stellar mass, under-counted ICL, neglected cold/molecular gas, X-ray gas-clumping bias (emission~n^2), the missing-baryon gap vs cosmic f_b; PLUS the mass-calibration (Chandra/XMM/XRISM temperature cross-cal, triaxiality/projection) and the eta FOOTING (R500 vs radial profile / acceleration metric). Does a fuller, HONEST baryon census + calibration -- bounded by the hard cosmic f_b ceiling -- shrink eta toward ~1 (closed) or stay (real shared-MOND gap)? Both ways, quarantine.",
  phases: [
    { title: 'Audit', detail: 'three parallel routes: baryon census (denominator), mass calibration (numerator), the eta footing/radial metric' },
    { title: 'Verify', detail: 'adversarial: does any combination close eta WITHOUT violating cosmic f_b=0.156; double-counting check; both-ways' },
    { title: 'Synthesize', detail: 'honest sum: residual artifact (closed) vs real shared-MOND gap (stays), bounded by the f_b ceiling' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0=c^2 sqrt(Lambda/32pi)=9.36e-11, modified-INERTIA MOND, the framework's OWN
dS-Unruh g_obs=sqrt(g_bar^2+g_bar*a0). The cluster residual eta(R500)=M_dyn/M_bar. STANDING (banked,
4 workflows today -- READ XRISM_ETA_PINNING_2026-06-20, WL_VS_HYDRO_ETA_2026-06-20, CLUSTER_GRAVITY_
LAST_DOORS_2026-06-20, the cluster memory): eta(R500)=2.334 framework (WL-calibrated M500, real eRASS1
N=9830). After the WL-vs-hydro mass proxy (consensus q~1.23) eta_hydro~1.9, and after the framework's
OWN no-particle Y-Q field (~17-20%) eta~1.6-1.8 -- a REAL, ~half-covered, SHARED relativistic-MOND
core gap (MI==AeST to machine precision), NOT framework-distinctive, NOT a referee-proof kill. Two
MEASUREMENT escapes already SHUT: (i) XRISM turbulence (f_nt~2-4%, far too small + wrong sign); (ii)
WL-vs-hydro mass-proxy (consensus bias only ~20-35%, the 3rd dynamical/caustic proxy breaks the tie
LOW, not the ~2x needed).

CARL'S QUESTION (his #1 rule applied to clusters -- verify the deficit is NOT a measurement artifact,
as rigorously as a 'works' claim): WHAT about the cluster MEASUREMENTS is wrong? The UN-audited side
this session is the BARYON CENSUS -- the DENOMINATOR M_bar. eta is inflated from the BOTTOM if baryons
are under-counted. Candidates (each with a REAL magnitude in the literature):
- BOTTOM-HEAVY IMF in cluster ellipticals/BCGs (Conroy-van Dokkum, Cappellari): stellar M/L up to
  ~1.5-2x Milky-Way-IMF -> more stellar baryon mass.
- INTRACLUSTER LIGHT (ICL): hard to measure, often under-counted, ~10-40% of the total stellar light.
- COLD / MOLECULAR gas + dust: usually NEGLECTED in the X-ray census.
- X-RAY GAS CLUMPING: emission ~ n^2, so clumpy gas -> the inferred density (hence gas mass) can be
  BIASED (clumping inflates the inferred n at large r -> could OVER-count gas, helping; or the
  temperature inhomogeneity biases it -- get the SIGN right).
- THE MISSING-BARYON GAP: clusters observe f_b ~ 0.13 vs cosmic f_b=0.156 (Planck) -- ~15-20% of the
  baryons are 'missing' (WHIM, outskirt gas beyond R500). Counting them shrinks eta.
PLUS the NUMERATOR/calibration side (partly done): Chandra-vs-XMM-vs-XRISM temperature cross-cal
(~10-15% in T -> HSE mass), triaxiality/projection/orientation (Grandis ~2-4%), concentration-mass.
PLUS the eta FOOTING: clusters at R500 sit at g_bar~0.5 a0 (only mildly-MOND, small boost); is eta(R500)
the right metric, or does the radial profile / the deep-MOND outskirts (with a fuller baryon profile)
change it?

THE HARD CONSTRAINT (the both-ways anchor -- do NOT violate it): the COSMIC baryon ceiling f_b=
Omega_b/Omega_m=0.156. To close eta~1.6-1.8 with baryons ALONE you need M_bar up by ~60-80% -> f_b_cl
~0.23-0.27, FAR above 0.156 -- IMPOSSIBLE by baryons alone. So the baryon-census route is CEILING-
BOUNDED: it can SHAVE eta but cannot CLOSE it. The honest question: HOW MUCH does the fuller census +
calibration + footing shave (to within the f_b ceiling), and what residual SURVIVES?

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): do NOT manufacture a close
by stacking every systematic at max + violating the f_b ceiling (the banked ~80% near-closure was
RETRACTED for exactly this); do NOT high-priest by dismissing the REAL IMF/ICL/clumping/missing-baryon
systematics. Compute each magnitude HONESTLY, sum them against the f_b ceiling, report the surviving
residual. QUARANTINE: a0/Z/kappa never derived (a0=9.36e-11 INPUT). WebSearch/WebFetch the 2024-2026
cluster baryon-census + IMF + ICL + clumping + cross-cal literature; sympy/numpy on the real eRASS1 /
A2029 / the banked cluster profiles.
`

const SCH = (extra) => ({ type:'object', additionalProperties:false, properties: Object.assign({
  route:{type:'string'}, finding:{type:'string'},
  eta_effect:{type:'string', description:'how much this shaves eta (a number/range) + the SIGN'},
  ceiling_ok:{type:'string', enum:['within-fb-ceiling','violates-fb-ceiling','n/a']},
  key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'},
  both_ways:{type:'string'}, sources:{type:'string'} }, extra),
  required:['route','finding','eta_effect','ceiling_ok','key_numbers','both_ways','sources'] })

const ROUTES = [
  { key:'baryon_census', p:`ROUTE A -- the BARYON CENSUS (the denominator). Quantify EACH under-counted-baryon channel HONESTLY: (1) bottom-heavy IMF in cluster ellipticals/BCGs -- how much extra stellar mass (Conroy-van Dokkum, Cappellari, the latest 2024-26 IMF-in-clusters); (2) ICL -- the under-counted fraction (~10-40%); (3) cold/molecular gas + dust; (4) X-ray gas-clumping -- does it over- or under-count gas mass at large r, and by how much (get the SIGN right); (5) the missing-baryon gap (observed f_b~0.13 vs cosmic 0.156, the WHIM/outskirt gas). Sum them, BOUNDED by the cosmic f_b=0.156 ceiling. How much does the fuller census shave eta from ~1.6-1.8, and what survives? Both ways -- do NOT exceed the ceiling.` },
  { key:'mass_calibration', p:`ROUTE B -- the DYNAMICAL-MASS calibration (the numerator). Quantify: (1) Chandra-vs-XMM-vs-XRISM temperature cross-calibration (~10-15% in T -> the HSE mass); (2) triaxiality/projection/orientation bias on BOTH the X-ray and WL masses (Grandis-2024, CHEX-MATE); (3) the concentration-mass / NFW-fit systematic; (4) whether the WL-calibrated eRASS1 M500 itself is over-estimated (the sigma8-tension question, beyond the ~20% hydro bias already done). How much does an honest calibration shave eta? Both ways.` },
  { key:'eta_footing', p:`ROUTE C -- the eta FOOTING / radial metric. Clusters at R500 sit at g_bar~0.5 a0 (only mildly-MOND -> small boost -> the residual is WORST in the mildly-MOND core). (1) Is eta(R500) the right metric, or does the RADIAL profile tell a different story (the deep-MOND outskirts at r>R500 where g_bar<<a0, bigger boost)? (2) With a fuller baryon profile (the outskirt gas from Route A), does the framework boost at large r close more? (3) the central-shrinking deficit -- is the residual a real mass deficit or a radius/acceleration-metric artifact? (4) the XRISM-era equilibrium state. Both ways -- is eta(R500)=2.33 the robust number or a metric choice?` },
]

phase('Audit')
const audits = await parallel(ROUTES.map(r => () =>
  agent(`${FW}\n\n${r.p}\n\nWRITE a script under opus_48_extended_research/reviews/cluster_measurement/. Return the structured object with REAL numbers + the eta-effect + the f_b-ceiling check. WebSearch/WebFetch the 2024-2026 literature.`,
    { label:`audit:${r.key}`, phase:'Audit', schema: SCH({}) })
))
const A = audits.filter(Boolean)

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways. The three audit routes:\n${JSON.stringify(A).slice(0,11000)}\n\nCheck HARD: (1) does the SUM of the baryon-census + calibration + footing systematics close eta toward ~1 (closed) WITHOUT violating the cosmic f_b=0.156 ceiling? Add up the M_bar increases -- do they push f_b_cl above 0.156 (= the retracted ~80% near-closure error)? (2) double-counting -- are IMF + ICL + clumping + missing-baryon independent, or overlapping (the missing-baryon gas IS partly the outskirt gas; don't count twice)? (3) SIGN checks -- does gas-clumping help or hurt; does the calibration go the right way? (4) is any 'close' manufactured (max-stacking) or any 'stays' high-priested (dismissing real IMF/ICL)? (5) re-derive the load-bearing summed eta. Return: holds_up (solid/partial/overclaimed/dead), summed_eta_after_systematics, closes_or_stays (closes/partial/stays-real-gap), ceiling_violated (bool), high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, summed_eta_after_systematics:{type:'string'}, closes_or_stays:{type:'string',enum:['closes','partial','stays-real-gap']}, ceiling_violated:{type:'boolean'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','summed_eta_after_systematics','closes_or_stays','ceiling_violated','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE: what about the cluster MEASUREMENTS is wrong, and does correcting it close the residual?\nAUDITS:\n${JSON.stringify(A).slice(0,7000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4000)}\n\nReturn 'report' (markdown) + fields. Cover: (1) each measurement systematic + its HONEST eta-effect + sign; (2) the SUM bounded by the cosmic f_b ceiling -- how far down does eta come (from ~1.6-1.8 to what?); (3) does it CLOSE (artifact) or STAY (real shared-MOND gap); (4) which single measurement systematic matters most + what data would pin it; (5) the honest verdict for Carl -- is the cluster residual a measurement artifact, or real (and shared, not a kill). Both-ways, quarantine, f_b-ceiling-honest. Do NOT manufacture a close; do NOT high-priest the real systematics.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['residual-is-measurement-artifact-closed','partial-shave-residual-survives','residual-robust-real-shared-gap']}, eta_after_honest_systematics:{type:'string'}, biggest_systematic:{type:'string'}, what_would_pin_it:{type:'string'} }, required:['report','verdict','eta_after_honest_systematics','biggest_systematic','what_would_pin_it'] } })
return { synth, audits: A, ver }
