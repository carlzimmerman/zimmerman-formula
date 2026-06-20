export const meta = {
  name: 'front-gaia-widebinary',
  description: "FRONT B: the Gaia wide-binary test (a0-VALUE + the MOND PREMISE). Pin the EXACT framework modified-INERTIA prediction for the wide-binary gravity anomaly (the Milgrom-2022 theta-factor EFE -> the most-Newtonian boost gamma_g~1.05-1.10, a0-degenerate), confront with the LATEST 2024-2026 wide-binary results (Chae, Hernandez, Banik/Pittordis, the contested claims both ways), and pin what Gaia DR4 (~Dec 2026) will actually show: tests the PREMISE (~0.5-1.4 sigma) + the a0-VALUE (excludes regular-MOND 4.5 sigma). Is the framework's MI prediction distinct from Newton AND from regular-MOND? Both ways, quarantine.",
  phases: [
    { title: 'Pull', detail: 'latest 2024-2026 wide-binary gravity results (Chae, Hernandez, Banik-Pittordis, El-Badry contamination), DR3 vs DR4 status' },
    { title: 'Compute', detail: 'exact framework MI (theta-factor EFE) wide-binary prediction at a0=9.36e-11; vs Newton, vs regular-MOND; the DR4 discriminating power' },
    { title: 'Verify', detail: 'adversarial: a0-degeneracy, the gamma~1.137-vs-1.05 MI-vs-MG split, contamination/eccentricity systematics, the sigma claims both ways' },
    { title: 'Synthesize', detail: 'what DR4 tests + when; is the framework distinctive; favored/disfavored/live; what settles it' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0=c^2 sqrt(Lambda/32pi)=9.36e-11, MODIFIED-INERTIA MOND from dS-Unruh,
g_obs=sqrt(g_bar^2+g_bar*a0). Wide binaries (separations ~2k-30k AU) probe internal accelerations
~a0 -- a clean MOND-vs-Newton test in the solar neighborhood, in the EXTERNAL galactic field
(g_ext~1.8 a0), so the EFE matters.

BANKED STANDING (verify + sharpen, both-ways -- READ project_honest_lcdm_stress_standing + the
EMPIRICAL_PROGRAM notes): the wide-binary boost gamma=1.137 (Chae) is the MODIFIED-GRAVITY (AQUAL/
QUMOND) value; the framework's MODIFIED-INERTIA EFE (Milgrom-2022 theta-factor) predicts the
MOST-NEWTONIAN boost gamma_g~1.05-1.10 -- a theta(0)-FAMILY, a0-DEGENERATE. Gaia DR4 (~Dec 2026)
tests only the PREMISE (is there ANY boost: ~0.5-1.4 sigma in DR4) + the a0-VALUE (excludes
regular-MOND 4.5 sigma). The sharp MI-vs-MG discriminator is NOT wide binaries (the ~5% MI-vs-MG gap
is below the DR4 floor + a0-degenerate) -- it is CASSINI s^TX. So wide binaries test the framework's
PREMISE + a0-value, not its MI-vs-MG distinctiveness. The field is HOT + CONTESTED: Chae 2023-2024
claims a MOND-positive boost; Banik-Pittordis-Sutherland + Hernandez + El-Badry dispute it on
eccentricity/contamination/LOS systematics.

THE JOB: (1) pin the EXACT framework MI prediction (the theta-factor EFE boost gamma_g, the
acceleration-plane curve) at a0=9.36e-11; (2) confront with the LATEST 2024-2026 wide-binary results
(Chae, Hernandez, Banik-Pittordis, Cookson/Manchanda, the 2025-26 updates) -- which way do they
point, and how contested; (3) what will Gaia DR4 actually show + when (~Dec 2026): the PREMISE sigma,
the a0-value exclusion of regular-MOND; (4) is the framework's MI prediction DISTINCT from Newton
(yes) AND from regular-MOND (the gamma~1.05 vs 1.137 split -- below DR4 floor?); (5) KEEP OPENING
DOORS: is there a wide-binary observable (eccentricity distribution, the deep-EFE regime, triples)
that COULD distinguish MI from MG before Cassini? BOTH-WAYS (penalize high-priest AND manufacturing);
QUARANTINE a0/Z/kappa never derived (a0=9.36e-11 INPUT). WebSearch/WebFetch 2024-2026; sympy/numpy
for the EFE curve. Data-gated -- "solved" = the exact DR4 discriminating power + timeline pinned, OR
current data decides the premise.
`

const SCH = (extra) => ({ type:'object', additionalProperties:false, properties: Object.assign({
  finding:{type:'string'}, key_numbers:{type:'array',items:{type:'string'}},
  direction:{type:'string',enum:['mond-positive','newtonian-null','contested','data-gated','n/a']},
  both_ways:{type:'string'}, sources:{type:'string'}, script_path:{type:'string'} }, extra),
  required:['finding','key_numbers','direction','both_ways','sources'] })

phase('Pull')
const pulls = await parallel([
  () => agent(`${FW}\n\nPULL #1 -- the LATEST wide-binary gravity results 2024-2026. WebSearch/WebFetch: Chae 2023 (ApJ 952 128) + Chae 2024 updates; Hernandez 2023-2024 (the LOS/null claims); Banik-Pittordis-Sutherland-Famaey 2024 (the eccentricity-marginalized null/MOND); El-Badry contamination; Cookson, Manchanda, Loeb, Hubert 2025-26; the Gaia DR3 vs DR4 status. For EACH: the claimed boost gamma (or null), the sigma, the key systematic (eccentricity prior, contamination, LOS velocities, undetected tertiaries), and which way it points. Return the structured object -- honest on how CONTESTED it is.`,
    { label:'pull:widebinary-results', phase:'Pull', schema: SCH({}) }),
  () => agent(`${FW}\n\nPULL #2 -- the MI-vs-MG wide-binary theory + DR4 forecast. WebSearch/WebFetch + banked: (a) the Milgrom-2022 modified-INERTIA EFE theta-factor and why MI gives the MOST-Newtonian boost gamma_g~1.05-1.10 vs MG/AQUAL gamma~1.137-1.2; (b) the a0-degeneracy of the boost; (c) what Gaia DR4 (~Dec 2026, ~30x more astrometry, RVs) will deliver for the wide-binary test -- the premise sigma, the regular-MOND exclusion; (d) is the gamma~1.05-vs-1.137 MI-vs-MG split above or below the DR4 measurement floor? Return the structured object.`,
    { label:'pull:mi-mg-dr4', phase:'Pull', schema: SCH({}) }),
])
const P = pulls.filter(Boolean)

phase('Compute')
const comp = await agent(`${FW}\n\nCOMPUTE. Using:\n${JSON.stringify(P).slice(0,9000)}\n\n(1) Pin the EXACT framework MI prediction: the theta-factor EFE boost gamma_g(a0=9.36e-11) and the wide-binary acceleration-plane curve, vs Newton (gamma=1) and vs regular-MOND-MG (gamma~1.137). (2) Where does the framework sit vs the LATEST data -- favored/disfavored/consistent? (3) The DR4 discriminating power: the PREMISE sigma + the regular-MOND a0-value exclusion sigma. (4) Is the gamma~1.05-vs-1.137 split resolvable by DR4 or below floor? WRITE a script under opus_48_extended_research/reviews/front_gaia/. Both-ways; quarantine. Return the structured object with REAL numbers.`,
  { label:'compute:wb', phase:'Compute', schema: SCH({ dr4_power:{type:'string'}, distinct_from_regular_mond:{type:'string'} }) })

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways. Prior:\n${JSON.stringify(comp).slice(0,8000)}\n\nCheck: (1) is the framework's gamma_g~1.05-1.10 MI prediction right (the theta(0)-family, a0-degenerate)? (2) is the a0-value exclusion of regular-MOND (4.5 sigma) honest given the contested data? (3) are the contamination/eccentricity systematics fairly weighted (Chae-positive vs Banik/Hernandez-null)? (4) is "DR4 tests premise not MI-vs-MG" correct (the 5% split below floor)? (5) high-priest (dismiss a real boost) or manufactured (claim DR4 confirms the framework)? Return holds_up, honest_direction, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, honest_direction:{type:'string'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','honest_direction','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE the Gaia wide-binary front.\nCOMPUTE:\n${JSON.stringify(comp).slice(0,5000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4000)}\n\nReturn 'report' (markdown) + fields. Cover: the exact framework MI prediction; where the latest data points (contested?); what DR4 tests (premise + a0-value) and when; is the framework distinct from Newton AND regular-MOND; any door to discriminate MI-vs-MG via wide binaries before Cassini; what settles it. Both-ways, quarantine.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, status:{type:'string',enum:['framework-favored','contested-live','disfavored','data-gated-dr4']}, dr4_tests:{type:'string'}, timeline:{type:'string'}, distinct_from_regular_mond:{type:'string'}, what_settles_it:{type:'string'} }, required:['report','status','dr4_tests','timeline','distinct_from_regular_mond','what_settles_it'] } })
return { synth, comp, ver, pulls: P }
