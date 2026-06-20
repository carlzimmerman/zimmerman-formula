export const meta = {
  name: 'front-cassini-stx',
  description: "FRONT A (the framework-DISTINCTIVE near-term test): the preferred-frame SME s^TX boost dipole. The framework is PROVEN preferred-frame (the lensing no-go) -> a preferred frame IS an SME background -> the same a0/|a| that makes it MOND induces a computable gravitational s_munu. Sharpen the EXACT s^TX prediction + its margin vs the LATEST (2024-2026) planetary-ephemeris Lorentz-violation bounds (INPOP/Cassini/BepiColombo/MESSENGER/lunar-laser), settle whether it is already falsified / live / safe, and pin the DECISIVE test + timeline. Keep opening doors: the distinctive 0.12% CMB-dipole anisotropy at a~a0 is UNTESTED -- is there a sharper distinctive observable? Both ways, quarantine.",
  phases: [
    { title: 'Pull', detail: 'latest 2024-2026 planetary-ephemeris + gravity-sector SME/LV bounds (s_munu, alpha-PPN, INPOP/Cassini/BepiColombo)' },
    { title: 'Compute', detail: 'exact s^TX boost-dipole prediction on the framework footing; margin vs the tightest bound; the CPT-even theorem; the untested CMB-dipole anisotropy door' },
    { title: 'Verify', detail: 'adversarial: channel-match (dipole-vs-spatial), beta-suppression, sector (gravity vs matter), the 9.6x margin' },
    { title: 'Synthesize', detail: 'falsified / live / safe? the decisive test + timeline; the sharpest distinctive observable' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0=c^2 sqrt(Lambda/32pi)=9.36e-11, modified-INERTIA MOND from dS-Unruh
T_eff=(hbar/2pi c k_B) sqrt(a^2+(cH_Lambda)^2). PROVEN preferred-frame (tonight's covariant
Cassini-safe-lensing NO-GO: diff-invariance + c_T=c + ghost-freedom FORBID covariant MOND lensing ->
the framework's lensing MUST be preferred-frame/Lorentz-violating). THE BRIDGE (banked, READ
project_sme_lorentz_bridge + S_TENSOR_SME_COMPONENT_LEDGER + the SM_BRIDGE_SME_LORENTZ reviews): a
preferred frame IS a Standard-Model-Extension (SME) background, so the same a0/|a| that makes it MOND
INDUCES a computable gravitational s_munu coefficient + a falsifiable CPT-EVEN-ONLY theorem (LV but
CPT-preserving; k_AF=0 bites at hbar H0 ~150x above the photon bound) + Sanders->PPN.

BANKED STANDING (verify, sharpen, both-ways -- do NOT just restate): the component-by-component calc
gives the framework PASSING every named gravity-sector bound (LLR/INPOP-Cassini/atom-interf/pulsar/
GPB/VLBI); the single tightest = s^TX BOOST DIPOLE vs INPOP/Cassini ~8.3e-9, margin ~9.6x conservative
(Saturn) to ~hundreds typical -> LIVE/falsifiable, NOT excluded. Tensor structure: s^TT O(1)
absorbable, s^TJ dipole O(beta), s^<JK> quad O(beta^2), trace=0, NO O(1) un-beta-suppressed
anisotropic observable (SO(3)-irrep + trajectory-independence). Sector robustly GRAVITY s_bar (the
matter-c_munu "15-order kill" is a verified MIS-MAP, killed by universal-coupling differential
cancellation). DO NOT cite "alpha2 ~1e-8/LIVE" (double-count) -- alpha2_MI~1e-13, ~1e6x SAFE; s^TX is
the live test, UNTIED from alpha2. The DISTINCTIVE 0.12% CMB-dipole anisotropy at a~a0 stays UNTESTED.

THE JOB: (1) sharpen the EXACT s^TX prediction (magnitude + sign + which projection) on the framework
footing; (2) confront it with the LATEST 2024-2026 planetary-ephemeris + gravity-sector LV bounds
(INPOP21/INPOP19a Cassini, BepiColombo/MESSENGER, lunar-laser, pulsar-timing, the SME data tables
Kostelecky-Russell update) -- is the margin still ~9.6x or has new data moved it? (3) is it FALSIFIED,
LIVE, or SAFE, and what is the DECISIVE test + timeline (~2028-32 analysis-limited)? (4) KEEP OPENING
DOORS: is the 0.12% CMB-dipole anisotropy at a~a0 a sharper/cleaner distinctive test? any other
un-beta-suppressed distinctive observable? BOTH-WAYS (Carl #1 rule -- penalize high-priest AND
manufacturing EQUALLY); QUARANTINE a0/Z/kappa never derived (a0=9.36e-11 INPUT). WebSearch/WebFetch
the 2024-2026 literature; sympy where it sharpens. This front is data-gated -- "solved" = the exact
decisive test + timeline pinned, OR current data already decides it.
`

const SCH = (extra) => ({ type:'object', additionalProperties:false, properties: Object.assign({
  finding:{type:'string'}, key_numbers:{type:'array',items:{type:'string'}},
  status:{type:'string',enum:['falsified','live-falsifiable','safe','data-gated','n/a']},
  both_ways:{type:'string'}, sources:{type:'string'}, script_path:{type:'string'} }, extra),
  required:['finding','key_numbers','status','both_ways','sources'] })

phase('Pull')
const pulls = await parallel([
  () => agent(`${FW}\n\nPULL #1 -- LATEST gravity-sector SME / Lorentz-violation bounds 2024-2026. WebSearch/WebFetch: the SME gravity-sector coefficient bounds s_munu, s^TX/s^TJ/s^<JK>, alpha-PPN (alpha1, alpha2), from planetary ephemerides (INPOP21a, EPM, Cassini), BepiColombo/MESSENGER, lunar-laser-ranging, pulsar timing, atom interferometry, and the Kostelecky-Russell "Data Tables for Lorentz and CPT Violation" latest update. Extract the TIGHTEST bound on each s_munu component + its source + year. Has anything tightened the s^TX bound below ~8.3e-9 since the banked work? Return the structured object.`,
    { label:'pull:sme-bounds', phase:'Pull', schema: SCH({}) }),
  () => agent(`${FW}\n\nPULL #2 -- the framework's s^TX DERIVATION chain + the CMB-dipole-anisotropy door. WebSearch/WebFetch + read the banked reviews to confirm: (a) the Sanders->PPN map + the s_bar = (a0/|a|)-class induced coefficient; (b) the CPT-even-only theorem (why k_AF=0, where it bites); (c) the boost-dipole channel (s^TX ~ O(beta) with beta=v/c the solar-system boost ~1e-3 to 1e-4). And the DOOR: the distinctive 0.12% anisotropy in the CMB-frame at a~a0 -- where would it show (galaxy outskirts at a~a0, the CMB dipole direction), is it cleaner than the planetary s^TX, and what instrument could see it? Return the structured object.`,
    { label:'pull:derivation-cmb-door', phase:'Pull', schema: SCH({}) }),
])
const P = pulls.filter(Boolean)

phase('Compute')
const comp = await agent(`${FW}\n\nCOMPUTE. Using:\n${JSON.stringify(P).slice(0,9000)}\n\n(1) Pin the EXACT s^TX boost-dipole prediction (magnitude, sign, projection) on the framework footing. (2) Compute the margin vs the LATEST tightest bound -- is it still ~9.6x (Saturn-conservative) to ~hundreds (typical), or has 2024-26 data moved it? (3) Re-derive the CPT-even-only theorem's bite (k_AF=0 at ~150x the photon bound). (4) Quantify the 0.12% CMB-dipole anisotropy at a~a0 as a distinct test. WRITE a script under opus_48_extended_research/reviews/front_cassini/. Both-ways; quarantine. Return the structured object with REAL numbers + status.`,
  { label:'compute:stx', phase:'Compute', schema: SCH({ margin:{type:'string'}, decisive_test:{type:'string'} }) })

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways. Prior:\n${JSON.stringify(comp).slice(0,8000)}\n\nCheck: (1) channel-match -- is s^TX a DIPOLE compared to a DIPOLE bound (not a spatial/isotropic mismatch)? (2) beta-suppression correct (O(beta), beta=solar-system boost)? (3) sector GRAVITY not matter (the universal-coupling cancellation)? (4) re-run the margin vs the tightest 2024-26 bound -- is "9.6x live" honest, not high-priested-to-excluded nor manufactured-to-safe? (5) is the CMB-dipole-anisotropy door real or a mirage? Return holds_up (solid/partial/overclaimed/dead), honest_status, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, honest_status:{type:'string'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','honest_status','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE the Cassini s^TX front.\nCOMPUTE:\n${JSON.stringify(comp).slice(0,5000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4000)}\n\nReturn 'report' (markdown) + fields. Cover: the exact s^TX prediction + current margin; falsified/live/safe; the DECISIVE test + timeline; the sharpest distinctive observable (planetary s^TX vs CMB-dipole anisotropy); what would settle it. Both-ways, quarantine.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, status:{type:'string',enum:['falsified','live-falsifiable','safe','data-gated']}, margin:{type:'string'}, decisive_test:{type:'string'}, timeline:{type:'string'}, sharpest_observable:{type:'string'} }, required:['report','status','margin','decisive_test','timeline','sharpest_observable'] } })
return { synth, comp, ver, pulls: P }
