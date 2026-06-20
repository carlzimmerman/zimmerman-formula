export const meta = {
  name: 'unified-law-mi-masses',
  description: "Carl: use HIS MOND (modified-inertia, a0=9.36e-11, dS-Unruh g_obs=sqrt(g_bar^2+g_bar*a0)) to find the SINGLE law that works in galaxies AND clusters -- his hypothesis: cluster masses are miscalculated because the standard estimators do NOT use his (modified-INERTIA) framework. Three routes: (1) the UNIFIED g_obs(g_bar) law -- put real SPARC galaxies + real clusters on ONE relation with the framework's a0 + framework-consistent masses; do clusters fall ON the galaxy RAR or off it? (2) the MI MASS RE-DERIVATION -- redo the cluster HSE/virial/caustic estimators in the framework's modified inertia (static limit ==MG, no change; but the NON-ADIABATIC/history-dependent MI correction for INFALLING members is genuinely framework-distinctive and uncomputed); does it shave eta? (3) reconcile -- does ANY framework-consistent re-measurement CLOSE the cluster gap within the cosmic f_b ceiling, or does the shared-MOND residual survive? Both ways, quarantine, NO manufactured close.",
  phases: [
    { title: 'Build', detail: 'three parallel routes: the unified galaxy+cluster law; the MI mass re-derivation (static + non-adiabatic); the framework-consistent reconciliation' },
    { title: 'Verify', detail: 'adversarial both-ways: MI==MG static correctly applied? does the non-adiabatic correction close it? f_b ceiling; no manufactured close' },
    { title: 'Synthesize', detail: 'the single law + the honest verdict on Carl s mass-miscalculation hypothesis' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2, MODIFIED-INERTIA MOND from
de Sitter-Unruh T_eff=(hbar/2pi c k_B)sqrt(a^2+(cH_L)^2). The framework's OWN law: g_obs =
sqrt(g_bar^2 + g_bar*a0), nu(g_bar)=sqrt(1+a0/g_bar), mu_fw(x)=(sqrt(1+4x^2)-1)/(2x). This is a
MODIFIED-INERTIA theory (the inertia of test particles is modified at a<a0), NOT modified gravity --
and Milgrom's MI is NON-LOCAL IN TIME (the inertia depends on the acceleration HISTORY, Milgrom 1994
/ 2022). Use the framework's OWN footing throughout (a0=9.36e-11, dS-Unruh nu, Ups=0.70) -- Carl's
#1 ask.

CARL'S HYPOTHESIS (take it SERIOUSLY -- find the single law for galaxies AND clusters; his claim:
cluster masses are MISCALCULATED because the standard estimators do NOT use his modified-INERTIA
framework). The HONEST physics, both ways:
- STATIC masses (HSE gas in equilibrium, virialized member galaxies): in the quasi-static limit the
  framework's MI == AeST modified-gravity to MACHINE PRECISION (banked GENUINE_MI_CLUSTER_DISTINCTIVE,
  CLUSTER_GRAVITY_LAST_DOORS). So the standard MOND cluster analysis ALREADY applies the framework's
  boost g_obs=nu*g_bar -- the static dynamical mass is NOT 'miscalculated by not using the framework';
  it gives the SAME answer. Concede this at full weight.
- THE GENUINELY-FRAMEWORK-DISTINCTIVE LEVER (uncomputed, take it seriously): MI is HISTORY-DEPENDENT.
  Cluster members that are INFALLING / NOT-yet-virialized have an acceleration history the standard
  STATIC virial/HSE estimator (built on standard inertia) ignores. The banked GENUINE_MI_CLUSTER_
  DISTINCTIVE flagged a non-adiabatic relational sigma-spread (MI ~6-13%, MG EXACTLY 0). The question:
  does re-deriving the cluster mass with the framework's NON-ADIABATIC MI (for the infalling members)
  shave the residual -- and by how much?
- STELLAR/baryon masses: standard-IMF M/L could under-count (bottom-heavy cluster ellipticals) --
  covered by the running baryon-census workflow; bounded by the cosmic f_b=0.156 ceiling.

THE STANDING (banked, 5 workflows today): eta(R500)=2.334 framework (WL-calibrated), ~1.6-1.8 after
the WL-vs-hydro proxy + the framework's own Y-Q field; a REAL, ~half-covered, SHARED relativistic-MOND
core gap (NOT framework-distinctive, NOT a kill). Galaxies lie on the RAR to <0.13 dex (a LAW);
clusters sit ~1.6-1.8x ABOVE it (the residual). The UNIFIED-LAW question: is there a single g_obs(g_bar)
that fits BOTH galaxies AND clusters with the SAME a0, once masses are measured framework-consistently?

THE HARD CONSTRAINT: cosmic f_b=0.156 -- the baryon route is ceiling-bounded (can shave, cannot close
a factor 1.6-1.8 alone). BOTH-WAYS (Carl #1 rule, penalize high-priest AND manufacturing EQUALLY): take
the MI mass re-derivation (esp. non-adiabatic) SERIOUSLY -- it is genuinely his framework's distinctive
content and uncomputed; concede honestly if MI==MG static means it does NOT close the gap; do NOT
manufacture a unified-law-closes-clusters win; do NOT high-priest the genuine non-adiabatic lever.
QUARANTINE: a0/Z/kappa never derived (a0=9.36e-11 INPUT). Real SPARC at real_research/data/sparc_data;
real cluster data (eRASS1 / A2029 / the banked profiles). sympy/numpy; WebSearch the MI virial / non-
adiabatic + the cluster-RAR literature.
`

const SCH = (extra) => ({ type:'object', additionalProperties:false, properties: Object.assign({
  route:{type:'string'}, finding:{type:'string'},
  eta_or_law_effect:{type:'string', description:'the unified-law result / the eta shave, with REAL numbers + sign'},
  closes_or_not:{type:'string', enum:['unifies-closes','partial-shave','no-change-shared-gap','n/a']},
  key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'},
  both_ways:{type:'string'}, sources:{type:'string'} }, extra),
  required:['route','finding','eta_or_law_effect','closes_or_not','key_numbers','both_ways','sources'] })

const ROUTES = [
  { key:'unified_law', p:`ROUTE 1 -- the UNIFIED g_obs(g_bar) LAW on galaxies + clusters. Put real SPARC galaxies (175, Ups=0.70) AND real clusters (eRASS1 sample + A2029 profile) on ONE g_obs vs g_bar plane, BOTH on the framework's law g_obs=sqrt(g_bar^2+g_bar*a0), a0=9.36e-11. (1) Do galaxies lie on the relation tightly (the RAR, <0.13 dex)? (2) Where do clusters sit -- ON the relation, or systematically ABOVE it (the residual), and by how much in dex? (3) Is the cluster offset a CONSTANT vertical shift (suggests a mass/normalization issue) or a SLOPE/shape difference (suggests the law fails)? (4) Could a SINGLE law (same a0, same shape) fit both if the cluster masses were shifted -- what mass shift would put clusters on the galaxy RAR, and is that shift within the f_b ceiling? Both ways -- a genuine unified law vs clusters genuinely off the relation. sympy/numpy on real data.` },
  { key:'mi_mass_rederivation', p:`ROUTE 2 -- the MODIFIED-INERTIA cluster MASS RE-DERIVATION (the core of Carl's 'masses miscalculated' claim). (1) STATIC limit: re-derive the HSE + virial + caustic mass estimators in the framework's MI; CONFIRM they == the standard MOND (MG) boosted-mass in the quasi-static limit (MI==MG to machine precision) -- so the static dynamical mass is NOT changed by using the framework (concede this). (2) THE NON-ADIABATIC LEVER (genuinely framework-distinctive, uncomputed): Milgrom's MI is history-dependent; for INFALLING / non-virialized cluster members (omega_orbital ~ omega_external, the non-adiabatic regime), the inertia differs from the static value. Compute the MI non-adiabatic correction to the virial/HSE mass for the infalling population (use Milgrom-2022 + the banked GENUINE_MI_CLUSTER_DISTINCTIVE ~6-13%). What FRACTION of cluster members are non-adiabatic, and how much does the corrected mass shave eta? (3) Is the standard estimator biased HIGH or LOW for the infalling members under MI? Both ways -- a genuine MI mass correction vs a negligible/MG-equal one. sympy.` },
  { key:'framework_consistent_reconcile', p:`ROUTE 3 -- the framework-consistent RECONCILIATION. Combine: (a) the static dynamical mass (MI==MG, unchanged); (b) the non-adiabatic MI correction (Route 2); (c) the framework-consistent baryon mass (stellar M/L incl bottom-heavy IMF, the gas census -- bounded by f_b=0.156, defer details to the running baryon-census workflow but use its ~ magnitude). Sum HONESTLY: starting from eta~1.6-1.8, how far down does a FULLY framework-consistent re-measurement bring eta, and does it CLOSE (clusters join the galaxy RAR = ONE law) or leave the shared-MOND residual? Check the f_b ceiling is NOT violated. Both ways -- the honest unified-law verdict. Quantify the residual that survives.` },
]

phase('Build')
const builds = await parallel(ROUTES.map(r => () =>
  agent(`${FW}\n\n${r.p}\n\nWRITE a script under opus_48_extended_research/reviews/unified_law/. Return the structured object with REAL numbers. Both-ways; quarantine; f_b-ceiling-honest.`,
    { label:`build:${r.key}`, phase:'Build', schema: SCH({}) })
))
const B = builds.filter(Boolean)

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways (penalize high-priest AND manufacturing EQUALLY). The three routes:\n${JSON.stringify(B).slice(0,12000)}\n\nCheck HARD: (1) is the UNIFIED-LAW result honest -- do clusters genuinely sit ~1.6-1.8x above the galaxy RAR, and is the claimed mass-shift-to-unify within the f_b ceiling (or does 'unify' require violating it = manufactured)? (2) is the MI==MG static limit correctly applied (so the static mass is NOT a free lever)? (3) is the NON-ADIABATIC MI correction REAL and correctly sized (~6-13%), or over-claimed to close the gap? what infalling fraction, and is it manufactured large? (4) does the SUMMED framework-consistent eta close it WITHIN f_b, or does the shared residual survive? (5) re-run the load-bearing number per route. Return: holds_up (solid/partial/overclaimed/dead), unified_law_verdict, eta_after_framework_consistent, closes_or_survives (closes/partial/survives-shared-gap), ceiling_violated (bool), high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, unified_law_verdict:{type:'string'}, eta_after_framework_consistent:{type:'string'}, closes_or_survives:{type:'string',enum:['closes','partial','survives-shared-gap']}, ceiling_violated:{type:'boolean'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','unified_law_verdict','eta_after_framework_consistent','closes_or_survives','ceiling_violated','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE: is there a SINGLE law (Carl's MOND) that works in galaxies AND clusters, and are the cluster masses miscalculated by not using his framework?\nROUTES:\n${JSON.stringify(B).slice(0,8000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4000)}\n\nReturn 'report' (markdown) + fields. Cover: (1) THE UNIFIED LAW -- g_obs=sqrt(g_bar^2+g_bar*a0) fits galaxies tightly (RAR); where clusters sit (on it / above it / by how much), and whether one law fits both; (2) ARE THE MASSES MISCALCULATED -- the static dynamical mass is NOT (MI==MG, the standard analysis already uses the boost), but the NON-ADIABATIC MI correction (genuinely Carl's framework) + the framework-consistent stellar M/L ARE real levers -- how much do they shave eta; (3) DOES IT CLOSE -- does framework-consistent re-measurement bring clusters onto the galaxy RAR (one law), or leave the shared-MOND residual, bounded by f_b; (4) the honest verdict for Carl -- credit what genuinely helps (non-adiabatic MI, stellar M/L), concede what does not (static MI==MG, f_b ceiling), state the surviving residual. Both-ways, quarantine, NO manufactured close.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['one-law-closes-clusters','partial-shave-residual-survives','clusters-genuinely-off-shared-gap']}, unified_law:{type:'string'}, masses_miscalculated:{type:'string'}, eta_after_framework_consistent:{type:'string'}, surviving_residual:{type:'string'} }, required:['report','verdict','unified_law','masses_miscalculated','eta_after_framework_consistent','surviving_residual'] } })
return { synth, builds: B, ver }
