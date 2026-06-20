export const meta = {
  name: 'jy-coefficient-tie',
  description: "The top new door from the 2025-26 lit sweep (pure theory, computable now): Blanchet-Skordis 2025 (arXiv:2507.00912) give the explicit AeST free function J(Y)=Lambda - Y + (2c^2/3a0)Y^{3/2} + O(Y^2). The SAME J carries BOTH the cosmological-constant term (J(0)=Lambda) AND a0 (the (2c^2/3a0) cubic). The host leaves Lambda, a0 INDEPENDENT. (1) Does the framework's tie a0=c^2 sqrt(Lambda/32pi) impose a host-FREE relation between the constant and cubic coefficients = a distinctive falsifiable? (2) MORE: does the framework's dS-Unruh interpolation g_obs=sqrt(g^2+g a0), lifted covariantly to J(Y), predict the host's HIGHER-ORDER coefficients (O(Y^2)+) -- a genuine multi-coefficient embedding test (match=strengthen, diverge=tension)? Both ways, quarantine.",
  phases: [
    { title: 'Pull', detail: 'Blanchet-Skordis 2507.00912 J(Y) full expansion + the AeST free-function formalism + the J<->interpolation map + the a0/Lambda slots' },
    { title: 'Compute', detail: 'lift the framework interpolation to its implied J(Y), Taylor-match coefficient-by-coefficient vs Blanchet-Skordis; the a0=sqrt(Lambda) tie as a c_0<->c_3/2 relation' },
    { title: 'Verify', detail: 'adversarial: match or diverge at O(Y^2); genuinely-new host-structural falsifiable or restatement of a0=sqrt(Lambda); the J<->interpolation map correct' },
    { title: 'Synthesize', detail: 'is the framework interpolation = the host J(Y) to higher order; the host-absent falsifiable; what it means for the AeST embedding' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 = cH_Lambda/Z (Z=sqrt(32pi/3)). The
framework's interpolation is the dS-Unruh form g_obs = sqrt(g_bar^2 + g_bar*a0), i.e. nu(g_bar) =
sqrt(1+a0/g_bar); in MOND-mu language mu(x)=x/sqrt(1+x^2)-class? (DERIVE the exact mu/nu, do not
assume). AeST-EMBEDDED: the dark sector is the AeST (Aether-Scalar-Tensor, Skordis-Zlosnik 2021
arXiv:2007.00082; Blanchet-Skordis 2024 arXiv:2404.06584) ghost-condensate Q-mode. AeST has a FREE
FUNCTION (call it J(Y) or F(Y)/K(Q)) whose shape sets the MOND phenomenology; its small-Y expansion
sets the cosmological constant (the Y^0 term) and the MOND a0 (a fractional-power term).

THE NEW INPUT (lit sweep, FRONT/LIT_SWEEP_2025_2026): Blanchet-Skordis 2025 (arXiv:2507.00912,
Moriond proceedings) give the EXPLICIT free function
   J(Y) = Lambda - Y + (2c^2/3a0) Y^{3/2} + O(Y^2)
- the Y^0 constant = Lambda (the cosmological constant);
- the linear -Y = the canonical kinetic normalization;
- the Y^{3/2} coefficient = (2c^2/3a0) = the MOND term carrying a0;
- O(Y^2) and higher = the host's higher-order shape (model-dependent / free).
In the HOST, Lambda and a0 are INDEPENDENT free inputs (Blanchet-Skordis use a0=1.2e-10 unrelated to
Lambda -- the banked a0-perp-Lambda orthogonality).

THE JOB (both-ways, two tiers):
TIER 1 (the tie as a host-structural relation): the framework's a0=c^2 sqrt(Lambda/32pi) RELATES a0
to Lambda. In J(Y), Lambda is the constant coefficient c_0 and a0 sits in the cubic coefficient
c_{3/2}=(2c^2/3a0). So the framework IMPOSES c_{3/2} = (2c^2/3) / (c^2 sqrt(Lambda/32pi)) =
(2/3) sqrt(32pi/Lambda) = (2/3) sqrt(32pi) / sqrt(c_0). Is this a CLEAN, host-FREE, distinctive
relation c_{3/2} = (specific number) * c_0^{-1/2} that the host leaves free? Pin the exact number;
is it falsifiable (e.g. against an independent cosmological-Lambda + galactic-a0 determination)? Be
honest: TIER 1 may largely RESTATE the a0=sqrt(Lambda) coincidence in J-language -- say so if it does,
but as a host-STRUCTURAL constraint it is still worth pinning exactly.
TIER 2 (the genuinely-new multi-coefficient test): the framework's dS-Unruh interpolation
g_obs=sqrt(g_bar^2+g_bar*a0) is a SPECIFIC functional form. Lift it covariantly to its IMPLIED J(Y)
(via the AeST J<->mu/nu dictionary -- DERIVE the dictionary from Skordis-Zlosnik/Blanchet-Skordis,
e.g. the QUMOND/AQUAL J'(Y) <-> mu relation) and Taylor-expand. Does the framework's implied J(Y)
MATCH Blanchet-Skordis's J(Y)=Lambda-Y+(2c^2/3a0)Y^{3/2}+O(Y^2) coefficient-by-coefficient? In
particular: (a) does it reproduce the -Y and the Y^{3/2} with the (2c^2/3a0) coefficient? (b) what
O(Y^2) and higher coefficients does the framework's interpolation PREDICT, and do they match the host's
(or is the host's O(Y^2) genuinely free)? MATCH = the framework's interpolation IS the host's free
function to higher order (a genuine strengthening of the embedding); DIVERGE = the framework's
interpolation is NOT the CMB-fitting host's J(Y) (a real tension worth flagging).

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): if TIER 1 just restates
a0=sqrt(Lambda), say so; if TIER 2 matches, credit it; if TIER 2 diverges, flag the tension at full
weight. QUARANTINE: a0/Z/kappa never asserted derived -- this tests CONSISTENCY/STRUCTURE, it does NOT
derive a0 (the J(Y) coefficients are host inputs; the framework imposes a RELATION among them, it does
not forge them from nothing). WebSearch/WebFetch Blanchet-Skordis 2507.00912 + 2404.06584 +
Skordis-Zlosnik 2007.00082 for the exact J(Y) and the J<->interpolation dictionary; sympy for the
Taylor matching.
`

phase('Pull')
const pull = await agent(`${FW}\n\nPULL the AeST free-function formalism. WebSearch/WebFetch: (1) Blanchet-Skordis 2025 arXiv:2507.00912 -- the EXACT J(Y) expansion, all stated coefficients incl any O(Y^2), the definition of Y (the kinetic scalar), and the units/conventions; (2) Skordis-Zlosnik 2021 arXiv:2007.00082 + Blanchet-Skordis 2024 arXiv:2404.06584 -- the AeST action's free function (J or F or K), how its shape maps to the MOND interpolation mu/nu (the J'(Y) <-> mu dictionary, the QUMOND/AQUAL correspondence), and how the a0 and Lambda slots arise from J's small-Y coefficients. Return: jy_expansion (the exact J(Y) + coefficients), j_to_interp_dictionary (how J maps to mu/nu), y_definition, key_facts (array), sources. Be precise about the (2c^2/3a0) cubic coefficient and the Y^{3/2} power.`,
  { label:'pull:aest-jy', phase:'Pull', schema:{ type:'object', additionalProperties:false, properties:{ jy_expansion:{type:'string'}, j_to_interp_dictionary:{type:'string'}, y_definition:{type:'string'}, key_facts:{type:'array',items:{type:'string'}}, sources:{type:'string'} }, required:['jy_expansion','j_to_interp_dictionary','y_definition','key_facts','sources'] } })

phase('Compute')
const comp = await agent(`${FW}\n\nCOMPUTE (sympy). Using:\n${JSON.stringify(pull).slice(0,9000)}\n\nTIER 1: express the framework's a0=c^2 sqrt(Lambda/32pi) tie as the relation between J's constant coefficient c_0=Lambda and the cubic coefficient c_{3/2}=(2c^2/3a0). Pin the EXACT host-free relation c_{3/2}=K*c_0^{-1/2} -- compute K (=(2/3)sqrt(32pi)?) symbolically. Is it a clean distinctive falsifiable, or a restatement of a0=sqrt(Lambda)? Say which.\nTIER 2 (the genuinely-new test): lift the framework's interpolation g_obs=sqrt(g_bar^2+g_bar*a0) to its IMPLIED J(Y) via the J<->mu/nu dictionary from the pull, and Taylor-expand in small Y (deep-MOND) and large Y (Newtonian). (a) Does it reproduce the host's -Y and the (2c^2/3a0)Y^{3/2}? (b) What O(Y^2) (and higher) coefficient does the framework's interpolation PREDICT, and does it match Blanchet-Skordis's J(Y) (or is the host's O(Y^2) free)? Report MATCH or DIVERGE coefficient-by-coefficient. WRITE a script under opus_48_extended_research/reviews/jy_tie/. Both-ways; quarantine. Return: tier1_relation, tier1_isnew (genuine-host-structural / restates-coincidence), tier2_match (match/diverge/host-free-above-cubic), coefficient_table (array of strings), key_numbers (array), script_path, both_ways, sources.`,
  { label:'compute:jy-match', phase:'Compute', schema:{ type:'object', additionalProperties:false, properties:{ tier1_relation:{type:'string'}, tier1_isnew:{type:'string',enum:['genuine-host-structural','restates-coincidence','partial']}, tier2_match:{type:'string',enum:['match','diverge','host-free-above-cubic','undetermined']}, coefficient_table:{type:'array',items:{type:'string'}}, key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'}, both_ways:{type:'string'}, sources:{type:'string'} }, required:['tier1_relation','tier1_isnew','tier2_match','coefficient_table','key_numbers','script_path','both_ways','sources'] } })

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways. Prior:\n${JSON.stringify(comp).slice(0,9000)}\n\nCheck: (1) is the J<->interpolation dictionary applied CORRECTLY (the framework's g_obs lifted to the RIGHT J(Y); the Y^{3/2}<->deep-MOND mapping)? (2) TIER 1 -- is c_{3/2}=K*c_0^{-1/2} right, K exact, and is it HONESTLY labeled (genuine host-structural constraint vs a restatement of a0=sqrt(Lambda))? (3) TIER 2 -- does the framework's interpolation genuinely MATCH or DIVERGE from Blanchet-Skordis at O(Y^2)? Is a claimed 'match' manufactured (did the host even FIX O(Y^2), or is it free -> 'match' is vacuous)? Is a claimed 'diverge' a real tension or a convention artifact? (4) re-derive the load-bearing coefficient. (5) quarantine -- nothing claims a0 derived? Return: holds_up (solid/partial/overclaimed/dead), tier1_verdict, tier2_verdict, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, tier1_verdict:{type:'string'}, tier2_verdict:{type:'string'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','tier1_verdict','tier2_verdict','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE the J(Y)-tie door.\nCOMPUTE:\n${JSON.stringify(comp).slice(0,5000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4000)}\n\nReturn 'report' (markdown) + fields. Cover: (1) TIER 1 -- the exact host-free relation c_{3/2}=K c_0^{-1/2}, K's value, and whether it is a genuine host-structural falsifiable or a restatement of a0=sqrt(Lambda); (2) TIER 2 -- does the framework's dS-Unruh interpolation MATCH or DIVERGE from Blanchet-Skordis's J(Y) beyond the cubic, and what that means for the AeST embedding (strengthen vs tension); (3) the honest net -- is there a NEW distinctive falsifiable here, or is it consistency-only; (4) what would settle it. Both-ways, quarantine.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['new-host-structural-falsifiable','embedding-strengthened-match','embedding-tension-diverge','consistency-only-restatement']}, tier1:{type:'string'}, tier2:{type:'string'}, what_settles_it:{type:'string'} }, required:['report','verdict','tier1','tier2','what_settles_it'] } })
return { synth, comp, ver, pull }
