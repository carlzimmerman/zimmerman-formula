export const meta = {
  name: 'cluster-residual-explain',
  description: "Carl: the cluster residual is REAL and CANNOT be left unexplained -- find the creative solution (no new particle; the framework's OWN ghost-condensate field IS allowed, it is a mode of gravity). Generative + both-ways. FOUR routes: (1) FIELD-CLUSTERING centerpiece -- does the AeST ghost-condensate Q-mode (CDM-degenerate on CMB/large scales = Omega_dm worth) cluster in the cluster CORE to provide the residual, while staying sub-dominant in GALAXIES (preserving the RAR)? the banked work only credited ~17-20% (the Y-Q boost), NOT the full CDM-like clustering; (2) TIME-DOMAIN / FORMATION-EPOCH MI -- the full non-quasi-static multi-frequency modified inertia (banked-flagged uncomputed) + cluster formed when a0 was different; (3) DEEP 2024-2026 LITERATURE -- EMOND, neutrinos-latest, Famaey/Skordis/Blanchet/Durakovic cluster work, screening, environment-a0, ANY creative idea; (4) BRUTE-FORCE COMBINATION -- the best stack that genuinely closes. Quarantine; both-ways (find the real explanation, do NOT manufacture).",
  phases: [
    { title: 'Hunt', detail: 'four parallel creative routes: field-clustering; time-domain/formation MI; deep literature; brute-force combination' },
    { title: 'Verify', detail: 'adversarial both-ways: does the field-clustering preserve the galaxy RAR while closing clusters? is any close manufactured? the galaxy-veto' },
    { title: 'Synthesize', detail: 'the most promising EXPLANATION -- build it, both-ways; is the tension explained or does it need a specific named ingredient' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 (a LAW in galaxies, RAR 0.110 dex on the
framework footing, BEATS regular-MOND; banked A0_LAW_OF_NATURE). MODIFIED-INERTIA MOND, dS-Unruh
g_obs=sqrt(g_bar^2+g_bar*a0). The framework's DARK SECTOR = the AeST (Skordis-Zlosnik 2021) ghost-
condensate Q-mode -- a w=0, a^-3 COLD component, a MODE of the gravity field (NOT a new particle).
Banked (project_ghost_condensate_dark_sector): the Q-mode is CDM-DEGENERATE on P(k)/CMB-lensing/ISW/
S8; SZ21 fit full Planck+P(k); I0 ~ Omega_dm and FREE. So the framework HAS a cold, clustering,
Omega_dm-worth dark sector that is a gravity mode, not a particle.

THE TENSION (must NOT leave unexplained -- Carl): clusters need ~x2 more gravitating mass than
baryons + the pure MOND boost provides; eta(R500)~1.6-2.4, concentrated in the core. Banked (5+
workflows today): NOT a baryon-census artifact (f_b ceiling), NOT a static-mass mis-measurement
(MI==MG to 1e-16), NOT turbulence (XRISM), NOT a WL-vs-hydro proxy alone (~20%). The framework's
Y-Q field was credited ~17-20% of the residual. The galaxies lie on the a0 LAW; clusters sit x1.9-2.4
ABOVE it (a CONSTANT vertical shift on resolved A2029 = a mass/normalization issue, NOT a law-shape
failure). The whole MOND family shares this (Sanders x6-implied-a0). SOMETHING accounts for the extra
cluster mass -- FIND IT.

THE CENTERPIECE IDEA (Route 1, the strongest no-particle candidate): the AeST ghost condensate is
CDM-DEGENERATE on large scales -- so it CLUSTERS like CDM. In GALAXIES it must stay smooth/sub-dominant
(else it spoils the tight RAR). In CLUSTERS (deeper potential, larger scale) it should cluster MORE.
The banked ~17-20% may UNDER-count its full CDM-like clustering. THE QUESTION: does the Q-mode cluster
ENOUGH in the cluster core to provide the residual (the field IS the cluster dark matter, like CDM,
no particle), while staying sub-dominant in galaxies (preserving the RAR)? This is how AeST is DESIGNED
to work (MOND galaxies + a CDM-like gravity-mode dark sector). Compute the Q-mode's ACTUAL clustering
profile in a cluster vs a galaxy. If it works, the 'residual' is the field doing its job -- NO tension.

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): be CREATIVE and GENERATIVE
(Carl: 'there IS an explanation, keep going, brute force it if we need to') -- draw from all ideas,
combine them, BUILD the best candidate; BUT do NOT manufacture a close (the field-clustering must
ALSO preserve the galaxy RAR -- the galaxy-veto is the hard constraint; if enough clustering to close
clusters spoils galaxies, say so). QUARANTINE: a0/Z/kappa/I0 never asserted derived (a0=9.36e-11
INPUT, I0 free). NO new fundamental particle (the framework's own field is allowed). Real data (eRASS1,
A2029, SPARC); WebSearch/WebFetch the 2024-2026 cluster-MOND + AeST-clustering literature; sympy/numpy.
`

const SCH = (extra) => ({ type:'object', additionalProperties:false, properties: Object.assign({
  route:{type:'string'}, idea:{type:'string'},
  closes_residual:{type:'string', enum:['closes','large-partial','small-partial','no','n/a']},
  galaxy_veto:{type:'string', enum:['safe','marginal','breaks','n/a'], description:'does it preserve the galaxy RAR'},
  key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'},
  both_ways:{type:'string'}, sources:{type:'string'} }, extra),
  required:['route','idea','closes_residual','galaxy_veto','key_numbers','both_ways','sources'] })

const ROUTES = [
  { key:'field_clustering', p:`ROUTE 1 -- THE CENTERPIECE: does the AeST ghost-condensate Q-mode CLUSTER in the cluster core to provide the residual, while staying sub-dominant in galaxies? (1) The Q-mode is CDM-degenerate (w=0, a^-3, Omega_dm worth) -- compute its DENSITY PROFILE in a cluster potential vs a galaxy potential (the AeST field equations / the Jeans scale / the k^4 dispersion from SZ21 + Blanchet-Skordis 2404.06584). (2) KEY: how much does it cluster in the cluster CORE (<R500) -- does it provide the ~x2 residual (the field IS the cluster dark matter), and is that MORE than the banked ~17-20%? (3) THE GALAXY-VETO (hard constraint): does the SAME field stay smooth/sub-dominant in galaxies (so the tight RAR survives)? compute the field's galaxy-scale contribution -- is it <~5% (RAR-safe)? (4) the transition: WHY does it cluster in clusters but not galaxies (the Jeans/scale/density threshold)? If it closes clusters AND preserves galaxies, the 'residual' is the field doing its designed job = NO tension. Both ways -- a genuine clustering solution vs a galaxy-RAR-spoiling over-clustering. sympy/numpy + real cluster+galaxy profiles. THE most promising no-particle route.` },
  { key:'timedomain_formation_mi', p:`ROUTE 2 -- TIME-DOMAIN / FORMATION-EPOCH modified inertia. (1) The framework's MI is NON-LOCAL IN TIME (Milgrom 1994/2022); the quasi-static limit (MI==MG) was banked as 'licensed by Eq.55-57 but the general multi-frequency case OBSTRUCTED by Eq.33' = UNCOMPUTED. Compute the FULL multi-frequency MI response in a CLUSTER (the cluster potential built up over collapse, the members' multi-frequency orbits) -- does the non-quasi-static MI give a LARGER effective gravitating mass than the static MI==MG estimate? (2) FORMATION-EPOCH: clusters virialized at z~0.5-2 when a0 may have been different (the a0(z) thread); if the cluster's deep-MOND structure was SET at formation (higher a0 if rising, the MUSE reading), the boost could be larger -- compute. (3) does either give a genuine cluster shave the static calc misses? Both ways -- credit a real time-domain effect, concede if it's the banked small non-adiabatic ~0.1-3%. sympy.` },
  { key:'deep_literature', p:`ROUTE 3 -- DEEP 2024-2026 LITERATURE sweep for cluster-residual EXPLANATIONS. WebSearch/WebFetch HARD: (1) EMOND / extended-MOND (Zhao-Famaey, the potential-dependent a0); (2) neutrinos in MOND -- the LATEST bounds (KATRIN 2024-26, the 11 eV sterile, the 1.5 eV active) -- is ANY neutrino mass still viable for the cluster residual? (3) the Famaey/Skordis/Blanchet/Durakovic/Kashlinsky 2024-26 cluster-MOND work -- how do THEY explain the cluster residual? (4) AeST-specific cluster predictions (does SZ21/Blanchet-Skordis predict the cluster residual via field clustering?); (5) ANY creative idea -- screening, a 2nd scale, the cosmic-web EFE, modified gas physics, the lensing-vs-dynamics split. What is genuinely NEW + could explain it? Return the structured object with the best candidate(s) + whether each is no-particle + galaxy-safe.` },
  { key:'bruteforce_combination', p:`ROUTE 4 -- BRUTE-FORCE COMBINATION (Carl: 'we can brute force it'). Given the pieces -- field clustering (Route 1), time-domain/formation MI (Route 2), bounded baryons (IMF/ICL ~3-8%, banked), the non-adiabatic sigma-spread, the WL-vs-hydro proxy -- compute the BEST COMBINATION that gets closest to closing eta from ~1.6-2.4 to ~1, WITHOUT (a) a new particle, (b) violating the f_b ceiling for the baryon part, (c) spoiling the galaxy RAR. How close does the honest stack get? Is there a combination that genuinely CLOSES it, and is each ingredient at a defensible magnitude (not max-stacked)? Both ways -- the honest best stack, flag any double-counting (the a0-degenerate parts standard MOND already applies). Quantify the surviving residual.` },
]

phase('Hunt')
const hunts = await parallel(ROUTES.map(r => () =>
  agent(`${FW}\n\n${r.p}\n\nWRITE a script under opus_48_extended_research/reviews/cluster_explain/. Return the structured object with REAL numbers. Be CREATIVE + GENERATIVE (find the explanation), both-ways (galaxy-veto is the hard constraint; no manufactured close); quarantine.`,
    { label:`hunt:${r.key}`, phase:'Hunt', schema: SCH({}) })
))
const H = hunts.filter(Boolean)

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways (penalize high-priest AND manufacturing EQUALLY). The four routes:\n${JSON.stringify(H).slice(0,13000)}\n\nCheck HARD, with the GALAXY-VETO as the hard constraint: (1) the FIELD-CLUSTERING centerpiece -- does the Q-mode genuinely cluster enough in the cluster core to close the residual, AND stay sub-dominant in galaxies (preserve the RAR <~5%)? Or does enough cluster-clustering SPOIL the galaxy RAR (the killer)? Re-run the field's galaxy-vs-cluster contribution. (2) is any 'close' MANUFACTURED (over-clustering, max-stacking, double-counting the a0-degenerate boost)? (3) is the time-domain MI genuinely bigger than the banked ~0.1-3%? (4) are the literature candidates no-particle + galaxy-safe? (5) does the brute-force combination honestly close, and at defensible magnitudes? (6) re-run the load-bearing number per route. Return: holds_up (solid/partial/overclaimed/dead), best_explanation, does_it_close (closes/large-partial/small-partial/no), galaxy_veto_survives (bool), high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, best_explanation:{type:'string'}, does_it_close:{type:'string',enum:['closes','large-partial','small-partial','no']}, galaxy_veto_survives:{type:'boolean'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','best_explanation','does_it_close','galaxy_veto_survives','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE: the most promising EXPLANATION for the cluster residual (Carl: it CANNOT be left unexplained).\nROUTES:\n${JSON.stringify(H).slice(0,9000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4500)}\n\nReturn 'report' (markdown) + fields. Cover: (1) THE FIELD-CLUSTERING centerpiece -- does the AeST Q-mode cluster enough to provide the residual while preserving the galaxy RAR; is the 'residual' the field doing its designed job (NO tension) or does over-clustering spoil galaxies; (2) the other routes (time-domain MI, literature, brute-force) -- what genuinely helps; (3) THE BEST EXPLANATION -- build it: is there a creative, no-particle, galaxy-safe solution that closes/largely-closes the residual, and at what cost/assumption; (4) if it does NOT fully close, the honest SMALLEST remaining ingredient + what would confirm it; (5) the verdict for Carl -- the explanation, both-ways, no manufactured close. Quarantine.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['field-clustering-explains-no-tension','creative-solution-largely-closes','partial-best-candidate-named','genuinely-open-shared-gap']}, best_explanation:{type:'string'}, galaxy_veto:{type:'string'}, residual_after:{type:'string'}, what_confirms_it:{type:'string'} }, required:['report','verdict','best_explanation','galaxy_veto','residual_after','what_confirms_it'] } })
return { synth, hunts: H, ver }
