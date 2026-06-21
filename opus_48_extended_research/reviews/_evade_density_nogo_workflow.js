export const meta = {
  name: 'evade-density-nogo',
  description: "Carl: before publishing the density-ordering no-go, find the literature calculation/mechanism by which the AeST/ghost-condensate dark sector clusters in cluster cores while staying SMOOTH in galaxies (evading the no-go), so the framework deploys the cluster mass GALAXY-SAFELY = explains clusters with no new particle AND keeps the RAR. The candidate loophole the no-go may have missed: the ghost condensate's k^4 dispersion (Arkani-Hamed-Cheng-Luty-Mukohyama 2004) sets a FINITE, SCALE-dependent Jeans scale -- if it sits BETWEEN galaxy (~kpc) and cluster (~Mpc) scales, the field clusters by SCALE (clusters yes, galaxies no), sidestepping the density-ordering argument. FOUR routes: (A) the actual AeST/ghost-condensate cluster + structure-formation predictions in the literature; (B) the k^4 Jeans / scale-dependent clustering mechanism (re-check the B=0 claim rigorously); (C) the broader scale-dependent-DM-clustering literature (warm/fuzzy/SIDM/cluster-scale); (D) reconcile -- does a REAL mechanism evade the no-go? Both ways: if YES build it (overturns the no-go, clusters explained galaxy-safely); if NO the no-go stands. Quarantine.",
  phases: [
    { title: 'Hunt', detail: 'four parallel routes: AeST cluster predictions; the k^4/mu Jeans-scale mechanism; the broader scale-dependent-clustering literature; the reconciliation' },
    { title: 'Verify', detail: 'adversarial both-ways: is the k^4 Jeans scale REALLY between galaxy and cluster scales? is B=0 really 0? does the mechanism preserve the CMB fit AND the RAR? no manufactured evasion, no high-priest dismissal' },
    { title: 'Synthesize', detail: 'is the no-go evaded (build the galaxy-safe cluster mechanism) or confirmed (it stands) -- the verdict that decides the paper' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0=c^2 sqrt(Lambda/32pi)=9.36e-11, modified-INERTIA dS-Unruh MOND (a LAW in
galaxies, RAR 0.110 dex). Dark sector = the AeST (Skordis-Zlosnik 2021, arXiv:2007.00082; Blanchet-
Skordis 2024, arXiv:2404.06584) ghost-condensate Q-mode: a w=0, rho~a^-3 COLD MODE of the gravity
field (NOT a particle); K(Q)=mu^2(Q-1)^2 (a ghost condensate per Arkani-Hamed-Cheng-Luty-Mukohyama
2004, hep-th/0312099); I0~Omega_dm FREE. It is CDM-degenerate on the CMB/P(k) (fits the Planck 3rd
acoustic peak).

THE NO-GO TO EVADE (banked CLUSTER_RESIDUAL_EXPLAIN_2026-06-20, this session's draft paper): the
Q-mode's Omega_dm-worth cold density ARITHMETICALLY covers the cluster core (1.46x, zero tuning) -- the
abundance is THERE. BUT the density-ordering argument says it cannot deploy galaxy-safely: if cs^2->0
sub-horizon (the property that fits the CMB 3rd peak), the Jeans length ->0 and growth is gated only by
rho>mu^2/4piG; galaxy disks are ~3.7x DENSER than cluster cores, so the field clumps MORE in galaxies,
injecting +0.12-0.23 dex into the RAR (floor 0.11-0.14) = BREAKS the galaxy law. Conclusion (the paper):
the field IS the cluster dark matter but cannot be galaxy-safe AND cluster-clumpy => 'no dark matter'
forfeited.

CARL'S CHALLENGE (the RIGHT move against a no-go -- find the loophole BEFORE publishing): find the
literature calculation/mechanism by which the field clusters in CLUSTER cores while staying SMOOTH in
GALAXIES. THE CANDIDATE LOOPHOLE the no-go MAY HAVE MISSED: a ghost condensate is NOT just cs^2->0 --
it has a k^4 DISPERSION omega^2 ~ cs^2 k^2 + (k^4 / M^2) (Arkani-Hamed et al 2004). The k^4 term sets a
FINITE, SCALE-dependent Jeans scale: at small k (CMB/large scales) cs^2->0 dominates (CDM-like, fits
the 3rd peak); at large k (small scales) the k^4 term stabilizes (no clustering below the Jeans scale).
If that Jeans scale sits BETWEEN galaxy (~kpc) and cluster (~Mpc) scales, the field clusters at CLUSTER
scales (k below Jeans) but is SMOOTHED at GALAXY scales (k above Jeans) -- it orders by SCALE, not
density, SIDESTEPPING the 'galaxies are denser' argument entirely. THIS is the evasion to test.
THE CATCH (test honestly): banked Door-A pin flagged the REAL AeST k^4 coefficient as possibly B=0
(Blanchet-Skordis Sec 6.2) -- if B=0 there is no k^4 Jeans scale and the no-go stands. Re-check B=0
RIGOROUSLY (is it 0 at all scales/regimes, or scale/background-dependent?). Also: the mu mass term
(finite screening scale mu^-1~Mpc) -- does IT give a helpful scale-dependent clustering?

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): hunt the evasion HARD (it
is a genuine physics loophole + Carl's explicit goal) -- if a REAL mechanism (k^4 Jeans scale in-window,
the mu screening, an actual AeST cluster calc) clusters in clusters AND preserves galaxies AND the CMB
fit, BUILD it (it OVERTURNS the no-go -> clusters explained galaxy-safely -> the paper becomes the strong
result); if the evasion FAILS (B=0, the Jeans scale out-of-window, the CMB forces cs^2->0 everywhere),
report the no-go STANDS honestly (do NOT manufacture a loophole). QUARANTINE: a0/Z/kappa/I0 never
derived. WebSearch/WebFetch the AeST + ghost-condensate + scale-dependent-DM literature HARD (Skordis,
Zlosnik, Blanchet, Verwayen, Durakovic, Arkani-Hamed, Mukohyama, Hwang-Noh, the AeST structure-formation
+ halo papers); sympy/numpy for the k^4 Jeans scale + the dispersion.
`

const SCH = (extra) => ({ type:'object', additionalProperties:false, properties: Object.assign({
  route:{type:'string'}, finding:{type:'string'},
  evades_nogo:{type:'string', enum:['yes-galaxy-safe-cluster-clumpy','partial','no-nogo-stands','n/a']},
  key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'},
  both_ways:{type:'string'}, sources:{type:'string'} }, extra),
  required:['route','finding','evades_nogo','key_numbers','both_ways','sources'] })

const ROUTES = [
  { key:'aest_cluster_lit', p:`ROUTE A -- the ACTUAL AeST / ghost-condensate CLUSTER + structure-formation predictions in the literature. WebSearch/WebFetch HARD: have Skordis, Zlosnik, Blanchet, Verwayen, Durakovic, or others COMPUTED what the AeST dark sector predicts for the field's clustering in GALAXIES vs CLUSTERS / in collapsed halos? (Skordis-Zlosnik 2021 PRL + long paper; Blanchet-Skordis 2024 2404.06584; Verwayen-Skordis-Zlosnik 2024; any AeST N-body / halo / non-linear structure paper; the AeST cluster-lensing predictions.) Does ANY of their computed results show the field clustering in clusters while staying galaxy-safe (a scale-dependent or environment-dependent clustering)? Or do they ALSO find the cluster residual (the shared gap)? Return the structured object -- what have the AeST authors actually shown about cluster vs galaxy clustering?` },
  { key:'k4_jeans_mechanism', p:`ROUTE B -- the k^4 JEANS / scale-dependent clustering mechanism (THE candidate loophole). (1) Derive the ghost-condensate dispersion omega^2 = cs^2 k^2 + B k^4/M^2 (+ the mu mass term) from the AeST quadratic action (Blanchet-Skordis 2024 Sec 6 / Skordis-Zlosnik). (2) RE-CHECK the B=0 claim RIGOROUSLY: is the k^4 coefficient B genuinely ZERO at all scales/backgrounds, or is it non-zero / scale-dependent / background-dependent (it may vanish only in a special limit)? Compute B. (3) IF B != 0: compute the k^4 JEANS SCALE lambda_J(rho) -- does it sit BETWEEN galaxy (~kpc) and cluster (~Mpc) scales, so the field clusters at cluster scales but is smoothed at galaxy scales (galaxy-safe AND cluster-clumpy by SCALE)? (4) Does this PRESERVE the CMB fit (cs^2->0 at large scales/small k) AND the RAR (smooth at galaxy scales)? (5) the mu mass term: does it add a helpful scale-dependent screening? sympy/numpy. THE decisive route -- compute whether the k^4 Jeans scale evades the no-go. Both ways.` },
  { key:'scale_dependent_dm_lit', p:`ROUTE C -- the BROADER scale-dependent-DM-clustering literature. WebSearch/WebFetch: mechanisms by which a dark sector clusters in CLUSTERS but NOT in GALAXIES (the opposite of warm/fuzzy DM which suppress SMALL scales = galaxies, which is the RIGHT direction here!): (1) warm dark matter (free-streaming cutoff suppresses sub-galactic = could keep galaxies smooth); (2) fuzzy / ultralight DM (de Broglie / quantum-pressure Jeans scale ~kpc-Mpc, scale-dependent); (3) self-interacting DM (cores in clusters); (4) any 'cluster-scale dark matter' / scale-dependent-clustering model. For EACH: the characteristic scale, and whether it gives the galaxy-safe-cluster-clumpy split -- AND whether the AeST ghost-condensate Q-mode can REALIZE that scale (does its effective Jeans/free-streaming scale match)? Return the structured object -- is there a known mechanism the AeST field could embody?` },
  { key:'reconcile_evasion', p:`ROUTE D -- the RECONCILIATION. Given the AeST cluster lit (A), the k^4 Jeans mechanism (B), and the broader scale-dependent literature (C): is there a REAL, self-consistent mechanism by which the framework's dark sector clusters in cluster cores (~Mpc) while staying smooth in galaxy disks (~kpc), preserving BOTH the CMB 3rd-peak fit AND the galaxy RAR? Build the best candidate: what is the required Jeans/free-streaming scale, can AeST produce it (k^4 B, mu, the field dynamics), and does it close the cluster residual galaxy-safely? Both ways -- if it works, state EXACTLY the mechanism + scale + how it overturns the no-go; if it fails, state EXACTLY why (B=0, scale out-of-window, CMB forces cs^2->0). Quantify. This decides whether the paper is the no-go or the galaxy-safe-solution.` },
]

phase('Hunt')
const hunts = await parallel(ROUTES.map(r => () =>
  agent(`${FW}\n\n${r.p}\n\nWRITE a script under opus_48_extended_research/reviews/evade_nogo/ where it computes. Return the structured object with REAL numbers. Hunt the evasion HARD (Carl's goal) but both-ways (no manufactured loophole); quarantine.`,
    { label:`hunt:${r.key}`, phase:'Hunt', schema: SCH({}) })
))
const H = hunts.filter(Boolean)

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways (penalize high-priest AND manufacturing EQUALLY). The four routes:\n${JSON.stringify(H).slice(0,13000)}\n\nCheck HARD, this DECIDES the paper: (1) the k^4 Jeans scale -- is B genuinely non-zero (re-derive from the AeST action; the banked Door-A pin said B=0 -- is that right or is B scale/background-dependent)? IF B!=0, is the Jeans scale REALLY between galaxy (~kpc) and cluster (~Mpc) scales, or out-of-window (sub-kpc = CDM-degenerate = clusters galaxies too; or super-Mpc = clusters nothing)? (2) does the mechanism PRESERVE the CMB fit (cs^2->0 at small k) -- or does a finite k^4/cs at galaxy scales spoil the 3rd peak? (3) does it PRESERVE the RAR (genuinely smooth at galaxy scales, <0.05 dex)? (4) do the AeST authors' OWN computed results support or refute the galaxy-safe clustering? (5) is any 'evasion' MANUFACTURED (a Jeans scale tuned to the window without a mechanism) or any 'no-go-stands' HIGH-PRIEST (dismissing a real k^4 scale)? Return: holds_up (solid/partial/overclaimed/dead), nogo_evaded_or_stands (evaded/partial/stands), the_mechanism (if any), galaxy_safe_and_cmb_safe (bool), high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, nogo_evaded_or_stands:{type:'string',enum:['evaded','partial','stands']}, the_mechanism:{type:'string'}, galaxy_safe_and_cmb_safe:{type:'boolean'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','nogo_evaded_or_stands','the_mechanism','galaxy_safe_and_cmb_safe','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE: is the density-ordering no-go EVADED (the field can be galaxy-safe AND cluster-clumpy via a real mechanism) or does it STAND? This decides the paper.\nROUTES:\n${JSON.stringify(H).slice(0,9000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4500)}\n\nReturn 'report' (markdown) + fields. Cover: (1) the k^4 Jeans mechanism -- is B!=0 and the Jeans scale in-window (galaxy-safe + cluster-clumpy + CMB-safe)? (2) what the AeST authors' own results show; (3) the broader scale-dependent-DM mechanisms and whether AeST realizes one; (4) THE VERDICT -- evaded (build the mechanism: the scale, how it closes clusters galaxy-safely, how the paper changes to the STRONG result) or stands (the no-go is confirmed, the paper stands, the field IS relocated DM); (5) if partial, the exact open computation that would settle it. Both-ways, quarantine, NO manufactured evasion. This is the load-bearing result for whether Carl's framework explains clusters with no dark matter.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['nogo-evaded-clusters-galaxy-safe','partial-promising-open','nogo-stands-confirmed']}, the_mechanism:{type:'string'}, jeans_scale:{type:'string'}, paper_changes:{type:'string'}, what_settles_it:{type:'string'} }, required:['report','verdict','the_mechanism','jeans_scale','paper_changes','what_settles_it'] } })
return { synth, hunts: H, ver }
