export const meta = {
  name: 'lit-sweep-2025-2026',
  description: "Comprehensive 2025-2026 literature sweep across every sub-field bearing on the framework (a0=c^2 sqrt(Lambda/32pi) modified-inertia dS-Unruh MOND, AeST-embedded). Multi-modal parallel: (A) AeST/relativistic-MOND theory; (B) MOND galaxy/RAR/BTFR observational tests; (C) cluster/lensing tests; (D) wide-binary/solar-system/dwarf/Local-Group; (E) DESI/dark-energy/a0-Lambda-coincidence/emergent-gravity; (F) DIRECT challenges + falsification claims. Synthesis: what is NEW that CONFIRMS / CHALLENGES / SHARPENS the framework, and the top newly-opened COMPUTABLE doors. Both-ways, quarantine.",
  phases: [
    { title: 'Sweep', detail: 'six parallel sub-field sweeps of 2025-2026 literature' },
    { title: 'Synthesize', detail: 'what is new that confirms/challenges/sharpens + the top computable doors it opens' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 = cH_Lambda/Z (Z=sqrt(32pi/3)=5.7888),
MODIFIED-INERTIA MOND from de Sitter-Unruh T_eff=(hbar/2pi c k_B)sqrt(a^2+(cH_Lambda)^2) (Deser-Levin),
interpolation g_obs=sqrt(g_bar^2+g_bar*a0). AeST-EMBEDDED (Skordis-Zlosnik 2021 arXiv:2007.00082; the
dark sector = the AeST ghost-condensate Q-mode, no new particle). STANDING (banked): theory program
CLOSED (a0 value provably unforceable/one-parameter EFT, dS-Unruh mechanism real, AeST host real);
the live frontier is EMPIRICAL + data-gated -- three framework-distinctive fronts: a0(z)/DESI
(ALIVE-FAVORED, DESI evolving-DE 3-4sigma), Cassini s^TX (LIVE ~1.5x), Gaia wide-binary (data-gated
DR4 Dec 2026, framework MI gamma~1.09 = most-Newtonian). Clusters = REAL shared-MOND gap (~half-covered
by the own field, NOT framework-distinctive, NOT a kill). Particle/mass sector WALLED (Koide relabel-
only). S8 neutral-by-theorem. Quarantine: a0/Z/kappa/I0 never asserted derived.

THE JOB: sweep the 2025-2026 literature in your assigned sub-field for anything that CONFIRMS,
CHALLENGES, SHARPENS, or OPENS A NEW DOOR for the framework. Prioritize PRIMARY 2025-2026 results
(arXiv, journals). For each genuinely-relevant item: what it is, which framework claim it bears on,
which direction (confirm/challenge/sharpen/new-door), and whether it opens a COMPUTABLE next step.
BOTH-WAYS (Carl #1 rule -- report challenges at full weight, do NOT cherry-pick confirmations, do NOT
high-priest-dismiss real tensions); QUARANTINE. Be HONEST about what is genuinely new vs already
banked. WebSearch/WebFetch extensively. This is RECON -- surface the leads, do not over-claim.
`

const SCH = { type:'object', additionalProperties:false, properties:{
  subfield:{type:'string'},
  items:{ type:'array', items:{ type:'object', additionalProperties:false, properties:{
    paper:{type:'string', description:'authors, title, arXiv/journal, 2025-2026'},
    bears_on:{type:'string', description:'which framework claim'},
    direction:{type:'string', enum:['confirms','challenges','sharpens','new-door','context']},
    computable_door:{type:'string', description:'the concrete next calculation it opens, or "none"'},
    note:{type:'string'} },
    required:['paper','bears_on','direction','computable_door','note'] } },
  headline:{type:'string', description:'the single most important new thing in this sub-field'},
  sources:{type:'string'} },
  required:['subfield','items','headline','sources'] }

const FIELDS = [
  { key:'aest-theory', p:`SUB-FIELD A -- AeST / relativistic-MOND THEORY 2025-2026. Skordis-Zlosnik-Verwayen-Blanchet-Bekenstein-line developments; new relativistic-MOND actions; ghost-condensate / khronon / aether-scalar-tensor; the k^4 Jeans / positivity / stability work; any new derivation or constraint on the AeST free function K(Q) or the a0 normalization; modified-inertia formalisms (Milgrom 2022+). What is NEW in the theory the framework is embedded in?` },
  { key:'galaxy-rar-btfr', p:`SUB-FIELD B -- MOND GALAXY / RAR / BTFR observational tests 2025-2026. New SPARC analyses; the radial-acceleration relation a0 + scatter + shape; the BTFR slope/normalization; high-z rotation curves (JWST/ALMA discs, the a0(z) question); the interpolation-function shape; any RAR result that bears on a0=9.36e-11 or the dS-Unruh shape. Both ways -- confirmations AND tensions.` },
  { key:'cluster-lensing', p:`SUB-FIELD C -- CLUSTER + LENSING tests 2025-2026. Cluster RAR / eta(R500); XRISM velocity follow-ups; the WL-vs-hydro mass-proxy / sigma8-tension; weak-lensing RAR (KiDS/DES/HSC/Euclid, Brouwer-line); the Bullet/merging-cluster residual; any new cluster MOND result. Does anything move the shared-MOND cluster gap or the lensing RAR a0?` },
  { key:'widebinary-dwarf-ss', p:`SUB-FIELD D -- WIDE-BINARY + SOLAR-SYSTEM + DWARF + LOCAL GROUP 2025-2026. The Chae/Hernandez/Banik/Saad-Ting wide-binary debate latest; Gaia DR4 forecasts; dwarf-spheroidal velocity dispersions + the EFE; ultra-faint dwarfs (JWST/DES); UDGs (DF2/DF4-type "no dark matter" galaxies); solar-system / planetary-ephemeris Lorentz-violation (the s^TX channel). Framework-distinctive MI EFE tests.` },
  { key:'desi-de-emergent', p:`SUB-FIELD E -- DESI / DARK-ENERGY / a0-Lambda-COINCIDENCE / EMERGENT-GRAVITY 2025-2026. DESI DR2 evolving-DE (w0-wa) follow-ups + the phantom-divide crossing; any a0 prop sqrt(Lambda) or a0=cH/Z-class coincidence paper; emergent/entropic gravity (Verlinde-line, Padmanabhan-line, holographic); de Sitter / horizon-thermodynamics; the cosmological-constant-MOND link. Does the latest DE data sharpen the a0(z) hostage?` },
  { key:'challenges-falsification', p:`SUB-FIELD F -- DIRECT CHALLENGES + FALSIFICATION CLAIMS 2025-2026. Papers claiming to FALSIFY MOND or modified-inertia or a0=sqrt(Lambda)-class models; strong-lensing time-delay / GW-EM (c_T=c) constraints on relativistic MOND; structure-growth / S8 / CMB challenges; any "MOND fails X" 2025-2026 result. Report these at FULL WEIGHT (Carl penalizes high-priesting AND manufacturing equally) -- what genuinely threatens the framework?` },
]

phase('Sweep')
const sweeps = await parallel(FIELDS.map(f => () =>
  agent(`${FW}\n\n${f.p}\n\nReturn the structured object. WebSearch/WebFetch hard for PRIMARY 2025-2026 sources.`,
    { label:`sweep:${f.key}`, phase:'Sweep', schema: SCH })
))
const S = sweeps.filter(Boolean)

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE the 2025-2026 literature sweep.\n\nSIX SUB-FIELD SWEEPS:\n${JSON.stringify(S).slice(0,16000)}\n\nReturn 'report' (markdown) + fields. Cover: (1) what is genuinely NEW (not already banked) that CONFIRMS the framework; (2) what CHALLENGES it (full weight -- any real threat?); (3) what SHARPENS a prediction; (4) the TOP 3-5 newly-opened COMPUTABLE doors (concrete next calculations), ranked by value; (5) the honest net effect on the standing. Both-ways, quarantine, NO over-claim. Separate genuinely-new from re-confirmation.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{
    report:{type:'string'},
    net_effect:{type:'string', enum:['standing-strengthened','standing-unchanged','standing-challenged','mixed']},
    top_confirms:{type:'string'}, top_challenges:{type:'string'},
    top_computable_doors:{ type:'array', items:{type:'string'} },
    biggest_new_thing:{type:'string'} },
    required:['report','net_effect','top_confirms','top_challenges','top_computable_doors','biggest_new_thing'] } })
return { synth, sweeps: S }
