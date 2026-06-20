export const meta = {
  name: 'front-a0z-desi',
  description: "FRONT C: the a0(z) hostage. The framework predicts a0(z)=cH_Lambda/Z tracking the DECLINING sqrt(rho_DE) branch -> a +6% phantom-divide bump @z=0.405, -26% @z=3, a BTFR-sign test. It is the framework's HOSTAGE to dark energy: distinctive IFF w!=-1 (evolving DE), but DISSOLVES to degenerate-with-MOND if w->-1. Confront with the LATEST 2024-2026 DESI (DR1/DR2 BAO w0-wa evolving-DE) + the MUSE-DARK a0(z) measurements (Ciocan 2026, RISING-contested) -> is the framework's declining branch ALIVE, DEAD, or CONTESTED given the current evolving-DE signal? Both ways, quarantine.",
  phases: [
    { title: 'Pull', detail: 'latest 2024-2026 DESI DR1/DR2 w0-wa evolving-DE + the MUSE-DARK / intermediate-z a0(z) measurements' },
    { title: 'Compute', detail: 'the framework a0(z) prediction (declining sqrt(rho_DE)) vs the DESI w(z); the +6% bump / -26% @z=3 / BTFR-sign; alive/dead/contested' },
    { title: 'Verify', detail: 'adversarial: the declining-vs-rising branch, w->-1 dissolution, the footing (rho_DE vs rho_total), the MUSE-DARK reading' },
    { title: 'Synthesize', detail: 'is the hostage alive given DESI evolving-DE; the decisive test (DR3 gate 2026-27, ELT) + timeline' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0=c^2 sqrt(Lambda/32pi)=9.36e-11 = cH_Lambda/Z, Z=sqrt(32pi/3)=5.7888. The
canonical reading: a0 tracks rho_DE (the pure-Lambda density), so a0(z) DECLINES as sqrt(rho_DE(z))
if dark energy evolves. THE HOSTAGE (READ project_a0z_muse_confrontation + the a0(z) paper Zenodo
10.5281/zenodo.20737162 + reference_published_papers_live_frontier): the framework is distinctive
ONLY IF w!=-1 (evolving DE) -- then a0(z) has a +6% PHANTOM-DIVIDE BUMP @z~0.405 and declines -26%
by z=3, giving a high-z BTFR-SIGN test (discs ~-7% in V below the z=0 BTFR). IF w->-1 (cosmological
constant), a0(z) is flat and the framework DEGENERATES to standard MOND -- the distinctive content
DISSOLVES. The rival branch: a0(z) prop cH/E(z)=sqrt(Omega_m(1+z)^3+Omega_Lambda) RISES with z (the
total-density footing) -- this is the CONTESTED reading. MUSE-DARK III (Ciocan 2026, NOT Mercier)
measures a0 RISING -> the canonical declining reading is WEAKENED + CONTESTED (LCDM-degenerate,
non-diagnostic), NOT falsified; "MUSE confirms rising" was RETRACTED. The footing matters:
rho_total/cH0 -> 1.13e-10 vs canonical rho_DE/cH_Lambda -> 9.36e-11.

THE JOB: (1) pin the framework a0(z) prediction on its OWN footing (declining sqrt(rho_DE), the +6%
bump @z=0.405, -26% @z=3); (2) confront with the LATEST 2024-2026 DESI w0-wa (DR1 2024 + DR2 2025
BAO -- the evolving-DE signal w0>-1, wa<0 that has been strengthening; does the DESI w(z) MATCH the
framework's declining-rho_DE curve?); (3) confront with the MUSE-DARK / intermediate-z a0(z) data
(Ciocan rising-contested) -- declining vs rising, both ways; (4) is the hostage ALIVE (DESI evolving-DE
gives the framework a distinctive, currently-favored prediction), DEAD (w->-1), or CONTESTED
(non-diagnostic now); (5) the DECISIVE test + timeline (DESI DR3 gate 2026-27, ELT/HARMONI + JWST
high-z BTFR early-mid 2030s); (6) KEEP OPENING DOORS: does the DESI evolving-DE w(z) actually PREDICT
the framework's a0(z) curve (a genuine cross-check), or is the BTFR-sign the only clean handle?
BOTH-WAYS (Carl #1 rule -- the a0(z) branch is exactly where convention artifacts bite; run it on the
framework's OWN declining sqrt(rho_DE), NOT the rival rising branch, but report the spread);
QUARANTINE a0/Z/kappa never derived (a0=9.36e-11 INPUT). WebSearch/WebFetch 2024-2026; sympy/numpy
for a0(z). Data-gated -- "solved" = alive/dead/contested settled on current data + the decisive
test+timeline pinned.
`

const SCH = (extra) => ({ type:'object', additionalProperties:false, properties: Object.assign({
  finding:{type:'string'}, key_numbers:{type:'array',items:{type:'string'}},
  status:{type:'string',enum:['alive-favored','contested-nondiagnostic','dead-dissolved','data-gated','n/a']},
  both_ways:{type:'string'}, sources:{type:'string'}, script_path:{type:'string'} }, extra),
  required:['finding','key_numbers','status','both_ways','sources'] })

phase('Pull')
const pulls = await parallel([
  () => agent(`${FW}\n\nPULL #1 -- the LATEST DESI evolving-dark-energy result 2024-2026. WebSearch/WebFetch: DESI DR1 (2024, arXiv:2404.03002) + DESI DR2 BAO (2025) w0-wa CPL fits -- the central w0, wa, the sigma of the evolving-DE (w!=-1) preference, the combination with CMB+SNe (Pantheon+/Union3/DES5yr). How strong is the w!=-1 signal now (2-4 sigma)? Does w(z) cross -1 (phantom divide) near z~0.4? Extract the w(z) curve. Return the structured object -- this sets whether the framework's hostage is alive.`,
    { label:'pull:desi-w0wa', phase:'Pull', schema: SCH({}) }),
  () => agent(`${FW}\n\nPULL #2 -- the direct a0(z) measurements + the framework's branch. WebSearch/WebFetch: MUSE-DARK III (Ciocan 2026) a0(z) rising claim; any intermediate-z RAR/BTFR a0(z) (high-z rotation curves, JWST/ALMA discs, the Mercier vs Ciocan readings); the high-z BTFR offset literature. And confirm the framework's OWN branch: a0(z)=cH_Lambda/Z with rho_DE(z) declining if w evolves -> the +6% bump @z=0.405 + -26% @z=3 + the -7% BTFR-V offset. How do the direct a0(z) data (rising-contested) sit vs the framework's declining branch? Return the structured object, honest both ways.`,
    { label:'pull:a0z-musedark', phase:'Pull', schema: SCH({}) }),
])
const P = pulls.filter(Boolean)

phase('Compute')
const comp = await agent(`${FW}\n\nCOMPUTE. Using:\n${JSON.stringify(P).slice(0,9000)}\n\n(1) Compute the framework a0(z) on its OWN footing (a0(z)=cH_Lambda/Z, rho_DE(z) from the DESI w0-wa) -- the +6% bump @z=0.405, the -26% @z=3, the BTFR-V offset. (2) Does the DESI evolving-DE w(z) curve PRODUCE the framework's predicted a0(z) (a genuine cross-check)? (3) Where do the direct a0(z) data (Ciocan rising) sit vs the framework's declining branch -- consistent within errors, or in tension? (4) ALIVE (DESI evolving-DE -> distinctive favored prediction), DEAD (w->-1), or CONTESTED (non-diagnostic)? Run it BOTH WAYS (declining sqrt(rho_DE) AND the rival rising cH/E(z)) and show the spread. WRITE a script under opus_48_extended_research/reviews/front_a0z/. Quarantine. Return the structured object with REAL numbers.`,
  { label:'compute:a0z', phase:'Compute', schema: SCH({ desi_matches_framework:{type:'string'}, decisive_test:{type:'string'} }) })

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways (the a0(z) branch is exactly where convention artifacts bite -- check footing HARD). Prior:\n${JSON.stringify(comp).slice(0,8000)}\n\nCheck: (1) the FOOTING -- declining rho_DE/cH_Lambda (9.36e-11) vs rising rho_total/cH0 (1.13e-10): is the framework's OWN declining branch used, with the spread shown? (2) does DESI w(z) genuinely match the framework a0(z), or is that manufactured? (3) is the Ciocan rising reading fairly weighted (contested, LCDM-degenerate) -- not high-priested away, not over-claimed? (4) the w->-1 dissolution -- is the hostage honestly conditional? (5) the BTFR-sign -- is it really the clean handle? Return holds_up, honest_status, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, honest_status:{type:'string'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','honest_status','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE the a0(z)/DESI hostage front.\nCOMPUTE:\n${JSON.stringify(comp).slice(0,5000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4000)}\n\nReturn 'report' (markdown) + fields. Cover: the framework a0(z) prediction (own footing + spread); does DESI evolving-DE make the hostage ALIVE/favored; the direct a0(z) (Ciocan rising) tension both ways; alive/dead/contested verdict; the DECISIVE test (DR3 gate 2026-27, BTFR-sign, ELT) + timeline; whether DESI w(z) is a genuine cross-check. Both-ways, quarantine, footing-honest.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, status:{type:'string',enum:['alive-favored','contested-nondiagnostic','dead-dissolved','data-gated']}, desi_cross_check:{type:'string'}, decisive_test:{type:'string'}, timeline:{type:'string'} }, required:['report','status','desi_cross_check','decisive_test','timeline'] } })
return { synth, comp, ver, pulls: P }
