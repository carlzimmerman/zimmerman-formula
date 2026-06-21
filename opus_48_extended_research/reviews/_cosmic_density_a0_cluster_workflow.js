export const meta = {
  name: 'cosmic-density-a0-cluster',
  description: "Carl's possibly-untested route: a0 set by the LARGE-SCALE COSMIC-WEB / ambient density (NOT the local matter density of ROUTE_E, which is killed). a0=(c/2)sqrt(G(rho_DE + rho_ambient)); clusters sit in ~5-100x overdense cosmic-web regions, so a0 ~sqrt(rho) is enhanced there -> bigger boost -> could close the residual. This survives the 3 ROUTE_E kills BETTER: (1) the smoothing scale = the cosmic-web correlation length ~5-10 Mpc (a NATURAL scale, not the tuned ~Mpc ROUTE_E couldn't derive); (2) a slowly-varying BACKGROUND density (like rho_DE), not a local EP-violating source; (3) ENVIRONMENTAL, not the per-galaxy density the 10.5sigma SPARC null killed. THE SHARP TEST: member galaxies obey the RAR -> if a0 is environment-enhanced, cluster member galaxies (in the SAME overdensity) must show the enhanced a0 -> do they (cluster vs field RAR), or the same a0? Both ways: viable cosmic-density route or joins the killed/descriptive set. Quarantine.",
  phases: [
    { title: 'Compute', detail: 'three routes: the cosmic-web-density a0 mechanism+magnitude; the member-galaxy sharp test; the distinction from ROUTE_E (does it survive the 3 kills?)' },
    { title: 'Verify', detail: 'adversarial both-ways: natural scale or smuggled-tune? member-galaxy RAR consistent or excluded? genuinely distinct from ROUTE_E or the same kill?' },
    { title: 'Synthesize', detail: 'is the cosmic-density route viable (closes clusters galaxy-safely) or does it join the killed/descriptive set' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = 9.36e-11 (INPUT). a0 is set
by a DENSITY (the dark-energy density rho_DE) via the dS-Unruh mechanism. CLUSTER residual: clusters
need ~x2 more gravitating mass than baryons+the MOND boost; the published no-go (Zenodo 10.5281/zenodo.
20779562) shows the AeST field HAS the mass (1.46x) but cannot deploy it galaxy-safely-AND-predictively.

CARL'S ROUTE (engage genuinely -- it is PARTLY DISTINCT from what was killed): a0 enhanced by the
LARGE-SCALE COSMIC-WEB / AMBIENT density the cluster sits IN. a0 = (c/2) sqrt(G (rho_DE + rho_ambient)),
where rho_ambient is the cosmic-web density smoothed on the correlation length ~5-10 Mpc. Clusters live
in ~5-100x overdense regions, so a0 ~ sqrt(rho) is enhanced -> bigger MOND boost -> could close the
residual with NO new mass.

WHAT WAS ALREADY KILLED (do NOT conflate -- the new route survives these BETTER): ROUTE_E (banked
ROUTE_E_DENSITY_A0_CLOSED_FALSIFIER + CLUSTER_GRAVITY_LAST_DOORS) = a0=(c/2)sqrt(G rho_LOCAL), the LOCAL
MATTER density, per-galaxy/per-cluster. Killed 3 ways: (i) the ~Mpc smoothing scale is a TUNED input the
dS-Unruh foundation does not supply (framework-native lengths are Gpc/1-Mpc-CMB/system-tracking); (ii)
the EQUIVALENCE PRINCIPLE forbids a local-matter a0 floor (Luo 2026 a_T=a_pr+a_bg additive; the floor is
uniform-in-space Lambda); (iii) the SPARC environment null excludes the per-galaxy coupling at ~10.5sigma.

WHY THE COSMIC-WEB VERSION MAY SURVIVE (the genuine distinction to test): (1) the smoothing scale = the
cosmic-web correlation length ~5-10 Mpc, a NATURAL scale (the LSS correlation length / the BAO-ish scale),
NOT the un-derivable ~Mpc; (2) rho_ambient is a slowly-varying BACKGROUND (like rho_DE), so a falling
test particle sees it as a near-uniform background -> the EP objection is WEAKER (it is not a local source);
(3) it is an ENVIRONMENTAL (large-scale) dependence, which the PER-GALAXY SPARC null does NOT directly
test. BUT the magnitude is scale-critical: a0~6x (to close via a0) needs rho~36x; the cosmic-web at ~10 Mpc
is only ~5-10x overdense (a0~x3), at ~1-2 Mpc ~50-150x (a0~x7-12, enough) -- so the answer RIDES the
smoothing scale again (the ~10 Mpc natural scale may be too small; the ~Mpc enough but ad hoc).

THE SHARP TEST (member galaxies obey the framework's MOND -- they ARE on the RAR): if a0 is enhanced by
the cluster's overdense COSMIC-WEB ENVIRONMENT, the MEMBER GALAXIES (sitting in the SAME overdensity) must
show the SAME enhanced a0 -> the cluster-galaxy RAR would be SHIFTED vs field galaxies. Do cluster member
galaxies show an enhanced a0 (cluster RAR vs field RAR), or the SAME a0 (which would EXCLUDE the
environmental enhancement, like the SPARC null killed ROUTE_E)?

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): this is Carl's genuine idea
and is PARTLY DISTINCT from the killed ROUTE_E -- engage it at full weight, compute the magnitude on the
NATURAL cosmic-web scale, run the member-galaxy sharp test honestly. If the cosmic-web a0 closes the
cluster (at a natural scale) AND the member-galaxy RAR is consistent (the boost is there but below the
member-galaxy sensitivity, or the members DO show it) -> VIABLE, a real route (credit it). If the natural
scale is too small (a0 enhancement insufficient) OR the member galaxies show the SAME a0 (excluding the
environmental boost) OR it collapses back to ROUTE_E's tuned-scale problem -> it joins the killed set
(report straight). Do NOT manufacture viability by smuggling the ~Mpc tuned scale back in; do NOT
high-priest by conflating it with ROUTE_E without testing the distinction. QUARANTINE: a0/Z/kappa never
derived. Real SPARC + cluster-galaxy data; cosmic-web overdensity from LSS (the 2-pt correlation /
the cluster environment). sympy/numpy; WebSearch the cluster-galaxy RAR + the cosmic-web density-a0 +
environmental-MOND literature.
`

const SCH = (extra) => ({ type:'object', additionalProperties:false, properties: Object.assign({
  route:{type:'string'}, finding:{type:'string'},
  verdict:{type:'string', enum:['viable-closes-galaxy-safe','partial','excluded-joins-killed','n/a']},
  key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'},
  both_ways:{type:'string'}, sources:{type:'string'} }, extra),
  required:['route','finding','verdict','key_numbers','both_ways','sources'] })

const ROUTES = [
  { key:'cosmic_web_a0_magnitude', p:`ROUTE 1 -- the COSMIC-WEB a0 mechanism + MAGNITUDE. (1) Compute a0 = (c/2)sqrt(G(rho_DE + rho_ambient)) with rho_ambient the cosmic-web density smoothed on the NATURAL correlation length (~5-10 Mpc, the LSS 2-pt correlation length / the turnaround scale). (2) At cluster locations (overdensity ~5-100x depending on scale), what a0 enhancement results -- and does it give the ~x6 boost needed to close the residual? (3) Is the cosmic-web scale GENUINELY natural (the LSS correlation length, derivable) or does closing REQUIRE smuggling back the ~Mpc tuned scale (= ROUTE_E)? (4) Both-ways: a0 enhancement at ~10 Mpc (~x3, maybe too small) vs ~1-2 Mpc (~x7-12, enough but ad hoc) -- which scale, and is it natural? sympy/numpy.` },
  { key:'member_galaxy_sharp_test', p:`ROUTE 2 -- the MEMBER-GALAXY sharp test (the blade). Member galaxies obey the framework's RAR. IF a0 is enhanced by the cluster's overdense cosmic-web environment, the MEMBER galaxies (in the SAME overdensity) must show the enhanced a0 -> the cluster-galaxy RAR shifts vs field. WebSearch/WebFetch + compute: (1) do cluster member galaxies show an ENHANCED a0 vs field galaxies (the cluster-RAR vs field-RAR literature -- Chae, Freundlich, the EFE-in-clusters work)? (2) what enhancement would the cosmic-density route PREDICT for member galaxies, and is it consistent with the data or EXCLUDED (like the SPARC null killed ROUTE_E)? (3) is there a window where the boost is real in the cluster CORE but below the member-galaxy sensitivity? Both-ways -- the sharp test that decides the route.` },
  { key:'distinct_from_routeE', p:`ROUTE 3 -- is it GENUINELY DISTINCT from the killed ROUTE_E? Test the 3 ROUTE_E kills against the cosmic-web version: (i) SMOOTHING SCALE -- is the cosmic-web correlation length (~5-10 Mpc) genuinely derivable/natural (vs ROUTE_E's un-derivable ~Mpc), or does closing need the tuned ~Mpc? (ii) EQUIVALENCE PRINCIPLE -- does a slowly-varying large-scale BACKGROUND rho_ambient evade the EP objection (Luo 2026 a_T=a_pr+a_bg) that killed the local-matter floor, or does it still violate it? (iii) SPARC null -- the 10.5sigma was per-GALAXY density; does the cosmic-web ENVIRONMENTAL version evade it (and what does the environmental EFE/wide-binary data say)? Verdict: genuinely distinct + surviving, or the same kill re-dressed. Both-ways.` },
]

phase('Compute')
const builds = await parallel(ROUTES.map(r => () =>
  agent(`${FW}\n\n${r.p}\n\nWRITE a script under opus_48_extended_research/reviews/cosmic_density_a0/. Return the structured object with REAL numbers. Both-ways (Carl's idea is partly-distinct -- engage at full weight; concede honestly if it joins the killed set); quarantine.`,
    { label:`compute:${r.key}`, phase:'Compute', schema: SCH({}) })
))
const B = builds.filter(Boolean)

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways (penalize high-priest AND manufacturing EQUALLY). The three routes:\n${JSON.stringify(B).slice(0,12000)}\n\nCheck HARD: (1) the cosmic-web SCALE -- is the magnitude that closes the cluster genuinely at a NATURAL scale (~5-10 Mpc LSS correlation length), or does it secretly need the ~Mpc tuned scale (= ROUTE_E re-dressed = manufactured viability)? (2) the MEMBER-GALAXY test -- do cluster galaxies show the predicted enhanced a0, or the SAME a0 (excluding it)? re-check the cluster-RAR-vs-field data. (3) the EP + SPARC-null distinction -- does the cosmic-web version GENUINELY evade the ROUTE_E kills, or is the 'distinction' illusory? (4) is any 'viable' MANUFACTURED (smuggled tuned scale / ignored member-galaxy exclusion) or any 'excluded' HIGH-PRIEST (conflating with ROUTE_E without the test)? Return: holds_up (solid/partial/overclaimed/dead), route_verdict (viable/partial/excluded), the_deciding_factor, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, route_verdict:{type:'string',enum:['viable','partial','excluded']}, the_deciding_factor:{type:'string'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','route_verdict','the_deciding_factor','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE: is Carl's COSMIC-DENSITY (large-scale cosmic-web ambient density) a0 route a VIABLE galaxy-safe cluster closure, or does it join the killed/descriptive set?\nROUTES:\n${JSON.stringify(B).slice(0,8000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4500)}\n\nReturn 'report' (markdown) + fields. Cover: (1) the cosmic-web a0 mechanism + whether it closes the cluster at a NATURAL scale; (2) the MEMBER-GALAXY sharp test -- consistent (viable) or excluded; (3) is it GENUINELY distinct from the killed ROUTE_E (survives the smoothing-scale/EP/SPARC kills) or the same kill; (4) THE VERDICT -- viable (a real route, credit Carl's instinct, name what closes it + the test) OR excluded/joins-killed (state exactly which kill bites: the scale, the member galaxies, or the EP); (5) honest -- Carl's instinct that a0 is a DENSITY scale is right; the question is whether the ENVIRONMENTAL version evades the local-version kills. Both-ways, quarantine, NO manufactured viability, NO high-priest dismissal.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['viable-cosmic-density-closes','partial-promising','excluded-joins-killed']}, the_deciding_factor:{type:'string'}, member_galaxy_test:{type:'string'}, distinct_from_routeE:{type:'string'} }, required:['report','verdict','the_deciding_factor','member_galaxy_test','distinct_from_routeE'] } })
return { synth, builds: B, ver }
