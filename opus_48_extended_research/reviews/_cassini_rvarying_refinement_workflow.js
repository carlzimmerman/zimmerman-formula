export const meta = {
  name: 'cassini-rvarying-refinement',
  description: "The one open COMPUTATIONAL door on the framework's tightest test (Cassini s^TX, margin ~1.5x). The Hees-2016 bound assumes a CONSTANT preferred-frame background s_bar; the framework's induced s_bar = (a0/2|a|)(uu)_traceless VARIES around each orbit as ~r^2 (since |a|=GM/r^2). Derive the r-varying integrand through the Hees secular-drift perturbation kernel (Eq.19), do the orbit integral, and compute whether the CORRECTED effective margin is TIGHTER (toward excluded) or LOOSER (toward safe) than the 'evaluate-at-a' ~1.5x. Both-ways: it can genuinely go either way (O(1) kernel weighting). Quarantine a0=9.36e-11 INPUT.",
  phases: [
    { title: 'Pull', detail: 'the Hees-2016 secular orbital-element-drift formalism (Eq.19 perturbation kernel) for s_munu, and which r-power weights the secular Omega/omega drift' },
    { title: 'Compute', detail: 'the r-varying s_bar~r^2 through the secular integrand; orbit-average vs evaluate-at-a; the corrected effective margin per planet' },
    { title: 'Verify', detail: 'adversarial: kernel sign/power, is it tighter or looser, does Saturn stay the worst corner, the O(1) either-way claim' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0=c^2 sqrt(Lambda/32pi)=9.36e-11, modified-INERTIA MOND, PROVEN preferred-frame.
THE INDUCED SME COEFFICIENT (banked FRONT_CASSINI_STX_2026-06-20.md, verified this session): the
preferred frame induces a gravity-sector spurion s_bar^{munu} = (a0/2|a|)(u^mu u^nu)_traceless, with
the leading observable s^TX = (a0/2|a|)*beta_cmb*n_X (O(beta) DIPOLE). Since |a|=GM/r^2 for a body at
distance r, the magnitude a0/2|a| = a0 r^2/(2GM) GROWS as r^2 -- so s_bar is NOT constant around an
orbit, it VARIES as ~r^2. Predicted |s^TX|: 8.68e-10 at Saturn-a (worst, lowest-a well-tracked body)
to 1.42e-12 at Mercury-a; sign NEGATIVE (CMB apex).

THE TIGHTEST BOUND (K-R Data Tables v19, Jan 2026): s_bar^TX = (-0.2 +/- 1.3)e-9 [combined fit, Hees
2016]. The "evaluate-at-a" margin = 8.68e-10 / 1.3e-9 = ~1.5x at the Saturn-a worst corner (0.67sigma
inside), 59-918x inner-planet-weighted. STATUS = LIVE/FALSIFIABLE.

THE OPEN REFINEMENT (this workflow -- the one remaining computational door): the Hees-2016 bound is
derived from the SECULAR drift of orbital elements (node Omega, perihelion omega, etc.) under a
CONSTANT s_munu background, via a perturbation integral over the orbit (Hees Eq.19 and the associated
secular-rate expressions). The framework's s_bar VARIES as ~r^2 around the orbit. So "evaluate s_bar
at the semi-major axis a" is an APPROXIMATION. The CORRECT procedure: insert s_bar(r) = (a0 r^2/2GM)*
(geometry) into the Hees secular integrand and orbit-average against the perturbation KERNEL (which r
dominates the secular Omega/omega drift -- aphelion r^2 is large but the kernel weighting may favor
perihelion). THE QUESTION: does the r-varying treatment make the framework's EFFECTIVE bound (and so
the margin) TIGHTER (toward excluded) or LOOSER (toward safe) than the ~1.5x "evaluate-at-a" value,
and by how much? The banked estimate: orbit-averaged <r^2> inflates magnitude by only +0.5-6% (so
"evaluate at a" slightly UNDER-estimates -> margin shrinks slightly), BUT the perturbation-kernel
weighting is a genuine O(1) uncertainty in EITHER direction -- this workflow resolves it.

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): it can genuinely go
either way; report the honest direction + magnitude. If the r-varying treatment TIGHTENS the margin
toward ~1x, say so (the framework's distinctive test is nearly excluded at the worst corner); if it
LOOSENS toward ~3-6x, say so (more comfortable). QUARANTINE a0/Z/kappa never derived (a0=9.36e-11
INPUT). WebSearch/WebFetch Hees 2016 (arXiv:1509.06868 / PRD 92 064049) + Bailey-Kostelecky 2006 for
the secular-rate formulas; sympy/numpy for the orbit integral with real planetary elements (a, e per
planet). This SHARPENS a LIVE/FALSIFIABLE verdict -- it is not expected to flip live<->excluded, but
it pins the worst-corner margin rigorously.
`

phase('Pull')
const pull = await agent(`${FW}\n\nPULL the Hees-2016 secular-drift formalism. WebSearch/WebFetch Hees, Bailey, Bourgoin, Le Poncin-Lafitte, Bouquillon, Francou, Lambert 2016 "Testing Lorentz symmetry with planetary orbital dynamics" (arXiv:1509.06868, PRD 92 064049) + Bailey-Kostelecky 2006 (gr-qc/0603030). Extract: (1) the secular rates of the orbital elements (d<Omega>/dt, d<omega>/dt, ...) as functions of s_munu and the orbital elements (a, e, i, ...); (2) the perturbation INTEGRAND / kernel over the true or eccentric anomaly -- which power of r (or a(1-e cos E)) weights the secular drift; (3) how the combined s^TX bound (1.3e-9) is built from which planets/elements. Return: formalism (the secular-rate formulas + the r-dependence of the kernel), key_facts (array), r_power_in_kernel (which r-power dominates the secular Omega/omega integrand), sources.`,
  { label:'pull:hees-formalism', phase:'Pull', schema:{ type:'object', additionalProperties:false, properties:{ formalism:{type:'string'}, key_facts:{type:'array',items:{type:'string'}}, r_power_in_kernel:{type:'string'}, sources:{type:'string'} }, required:['formalism','key_facts','r_power_in_kernel','sources'] } })

phase('Compute')
const comp = await agent(`${FW}\n\nCOMPUTE the r-varying correction. Using the Hees formalism:\n${JSON.stringify(pull).slice(0,8000)}\n\n(1) Write s_bar(r) = (a0 r^2 / 2GM) * (the geometric uu-traceless + beta_cmb*n_X projection) -- the s^TX component varying as r^2. (2) Insert into the Hees secular-drift integrand and orbit-average against the perturbation kernel over the eccentric/true anomaly, per planet (use real a, e: Mercury a=0.387 e=0.206, Earth 1.0/0.017, Mars 1.524/0.093, Saturn 9.54/0.054). (3) Compare the orbit-correct EFFECTIVE s^TX that the secular drift constrains vs the "evaluate-at-a" value 8.68e-10 (Saturn). (4) Compute the CORRECTED margin per planet and identify the worst corner. Is it TIGHTER (toward ~1x, nearly excluded) or LOOSER (toward ~3-6x, comfortable) than ~1.5x? By what factor? Does Saturn stay the worst corner, or does a high-e body (Mercury, Mars) become binding once the r^2 weighting is applied? WRITE a script under opus_48_extended_research/reviews/front_cassini/. Both-ways; quarantine. Return: calculation, corrected_margin, direction (tighter/looser/same), worst_corner, key_numbers (array), script_path, both_ways, sources.`,
  { label:'compute:rvarying', phase:'Compute', schema:{ type:'object', additionalProperties:false, properties:{ calculation:{type:'string'}, corrected_margin:{type:'string'}, direction:{type:'string',enum:['tighter','looser','same','either-way-unresolved']}, worst_corner:{type:'string'}, key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'}, both_ways:{type:'string'}, sources:{type:'string'} }, required:['calculation','corrected_margin','direction','worst_corner','key_numbers','script_path','both_ways','sources'] } })

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways. Prior:\n${JSON.stringify(comp).slice(0,8000)}\n\nCheck: (1) the r-power in the kernel -- is the s_bar~r^2 inserted into the RIGHT secular integrand (Omega/omega rates), and is the orbit-average against the correct kernel weight (not just <r^2>=a^2(1+3e^2/2))? (2) the SIGN/direction -- tighter or looser, and is it honest (not high-priested to excluded, not manufactured to safe)? (3) does the worst corner stay Saturn, or does a high-e body bind? (4) re-run the load-bearing orbit integral for the worst planet. (5) is the final margin LIVE still (not flipped to excluded by an over-aggressive kernel)? Return: holds_up (solid/partial/overclaimed/dead), corrected_margin_final, direction_final, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, corrected_margin_final:{type:'string'}, direction_final:{type:'string'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','corrected_margin_final','direction_final','high_priest_or_manufactured','skeptic_findings','corrected'] } })

return { pull, comp, ver }
