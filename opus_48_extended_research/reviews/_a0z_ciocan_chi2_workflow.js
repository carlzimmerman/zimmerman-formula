export const meta = {
  name: 'a0z-ciocan-chi2',
  description: "Put a real sigma-number on the framework's STRONGEST live challenge: the Ciocan/MUSE-DARK III (arXiv:2604.22613) measured a0 RISING ~30sigma (a0(z)~1.0+1.59z x10^-10). We call it 'non-diagnostic' qualitatively; this quantifies it. chi^2 of the three a0(z) branches (framework declining sqrt(rho_DE); flat; rising cH/E(z)) vs Ciocan's BINNED a0(z), under three marginalizations: (a) raw, (b) absolute z=0 normalization marginalized (Ciocan's a0 sits ~2x above 1.2e-10 even at low-z = an M/L signature), (c) the M/L + LCDM baryon-assembly drift (Magneticum ~x3 with NO fundamental a0) marginalized. Does the SLOPE exclude the declining branch after marginalization, or collapse to non-diagnostic? Both ways, quarantine.",
  phases: [
    { title: 'Pull', detail: "Ciocan MUSE-DARK III binned a0(z) points+errors, the M/L+assembly systematic, the Magneticum LCDM-a0-drift baseline" },
    { title: 'Compute', detail: 'chi^2 of the 3 branches vs binned a0(z) under raw / normalization-marginalized / systematic-marginalized; the sigma-exclusion of declining' },
    { title: 'Verify', detail: 'adversarial: is the exclusion real (slope) or non-diagnostic (normalization+drift); the binned errors; the marginalization honesty' },
    { title: 'Synthesize', detail: 'the sigma-number + verdict: real tension vs earned non-diagnostic' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0=c^2 sqrt(Lambda/32pi)=9.36e-11=cH_Lambda/Z. a0(z) on the framework's OWN
DECLINING sqrt(rho_DE) branch: a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE(0)) -- with DESI evolving-DE it has a
+6% bump @z~0.4 then declines (a0(z=1)~1.01, a0(z=3)~0.74). The RIVAL rising branch cH/E(z)=
sqrt(Om(1+z)^3+OL) RISES (a0(z=1)~1.78). a0(z=0)=9.36e-11 is a multiplicative INPUT (quarantine: only
the SHAPE is predicted; kappa/c/Z/interp cancel in the ratio).

THE CHALLENGE (the strongest live pressure -- READ FRONT_A0Z_DESI_2026-06-20 + project_a0z_muse_
confrontation): Ciocan et al., MUSE-DARK III, A&A 709 L16 / arXiv:2604.22613 (79 star-forming
galaxies, 0.33<z<1.44) measure a0 RISING ~30sigma: a0(z) ~ (1.0 + 1.59 z) x 10^-10 m/s^2 (so
a0(z~1)~2.59e-10 ~2.8x the framework, and the framework's DECLINING branch goes the WRONG SIGN). The
banked qualitative read: NON-DIAGNOSTIC at the systematic floor because (i) Ciocan's ABSOLUTE a0 sits
~2x above the empirical 1.2e-10 even at LOW z (an M/L / aperture normalization signature -- not a z-
evolution), (ii) the authors attribute the RISE to baryon-fraction/assembly, and LCDM with NO
fundamental a0 reproduces a rising apparent-a0 (Magneticum, Mayer+2023 arXiv:2206.04333, ~x3 to z=2.3),
(iii) a fitted a0 != a fundamental a0.

THE JOB (quantify the qualitative): compute the chi^2 / sigma-exclusion of EACH a0(z) branch
(framework-declining, flat, rising-cH) against Ciocan's BINNED a0(z) measurements, under THREE
treatments: (a) RAW (absolute a0 + slope); (b) NORMALIZATION-MARGINALIZED (free a0(z=0) offset -- test
only the SHAPE/slope, since the absolute offset is an M/L signature); (c) SYSTEMATIC-MARGINALIZED (also
marginalize the M/L + LCDM-assembly drift, i.e. add the Magneticum-class apparent-a0-rise as a nuisance
that ANY model inherits). KEY QUESTION: after (b)/(c), does the SLOPE da0/dz still exclude the
framework's flat/declining branch, and at how many sigma? Branch (b) is the honest test: does MUSE's
rising SLOPE survive marginalizing the absolute normalization? If yes (slope robustly rising even with
free offset), it is a REAL tension with the framework's flat/declining shape -- surface it at full
weight. If the slope-exclusion collapses once the normalization + the LCDM-shared assembly drift are
marginalized, 'non-diagnostic' is EARNED -- state the residual sigma.

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): do NOT manufacture 'non-
diagnostic' by over-marginalizing; do NOT high-priest a real slope-tension away. Report the sigma in
each treatment honestly. The framework's flat/declining branch genuinely DISAGREES with a robust rising
SLOPE -- if MUSE's slope is robust, say the framework's a0(z) is in TENSION (dissolving only if w->-1
flattens it or the slope is systematic). QUARANTINE: a0/Z/kappa never derived; a0(0) is an INPUT, so
the NORMALIZATION-marginalized (shape-only) test is the FAIR one. WebSearch/WebFetch Ciocan 2604.22613
for the binned a0(z) points + errors; sympy/numpy for the chi^2.
`

phase('Pull')
const pull = await agent(`${FW}\n\nPULL the data. WebSearch/WebFetch Ciocan et al. MUSE-DARK III (arXiv:2604.22613, A&A 709 L16): extract the BINNED a0(z) measurements -- the z-bins, the central a0 per bin, the error bars, the fitted slope (1.59e-10/z) + its error, the number of galaxies, the absolute a0(z=0) intercept (~1.0e-10?), and HOW they derive a0 (RAR-fit at fixed baryons / M-L assumption / pressure support). Plus the Magneticum LCDM-a0-drift baseline (Mayer+2023 arXiv:2206.04333: apparent a0 rises ~x? to z=2.3 with NO fundamental a0) for the systematic nuisance. And confirm the framework's branch values: a0(z)/a0(0) declining (DESI w0wa: ~1.06@z0.4, ~1.01@z1, ~0.74@z3) vs rising-cH (~1.24@z0.4, ~1.78@z1). Return: binned_points (array of 'z: a0+/-err'), slope_fit, normalization_intercept, derivation_method, magneticum_drift, framework_branch_values, sources.`,
  { label:'pull:ciocan-data', phase:'Pull', schema:{ type:'object', additionalProperties:false, properties:{ binned_points:{type:'array',items:{type:'string'}}, slope_fit:{type:'string'}, normalization_intercept:{type:'string'}, derivation_method:{type:'string'}, magneticum_drift:{type:'string'}, framework_branch_values:{type:'string'}, sources:{type:'string'} }, required:['binned_points','slope_fit','normalization_intercept','derivation_method','magneticum_drift','framework_branch_values','sources'] } })

phase('Compute')
const comp = await agent(`${FW}\n\nCOMPUTE the chi^2 / sigma. Using:\n${JSON.stringify(pull).slice(0,9000)}\n\nFor EACH branch (framework-declining sqrt(rho_DE), flat a0=const, rising-cH/E(z)) compute chi^2 vs Ciocan's binned a0(z) under THREE treatments: (a) RAW -- absolute a0(z)=9.36e-11 x branch-ratio vs the binned points; (b) NORMALIZATION-MARGINALIZED -- minimize chi^2 over a free a0(z=0) offset (test only the SHAPE/slope; this is the FAIR test since a0(0) is a framework INPUT); (c) SYSTEMATIC-MARGINALIZED -- additionally subtract/marginalize the Magneticum LCDM-assembly apparent-a0-drift as a nuisance every model inherits. Report the sigma-exclusion of the framework's flat/declining branch in EACH treatment. KEY: in (b), does MUSE's rising SLOPE still exclude the flat/declining shape, and at how many sigma? Does (c) collapse it? WRITE a script under opus_48_extended_research/reviews/a0z_ciocan/. Both-ways; quarantine. Return: calculation, sigma_raw, sigma_norm_marginalized, sigma_systematic_marginalized, slope_survives_marginalization (yes-real-tension/no-non-diagnostic/partial), key_numbers (array), script_path, both_ways, sources.`,
  { label:'compute:chi2', phase:'Compute', schema:{ type:'object', additionalProperties:false, properties:{ calculation:{type:'string'}, sigma_raw:{type:'string'}, sigma_norm_marginalized:{type:'string'}, sigma_systematic_marginalized:{type:'string'}, slope_survives_marginalization:{type:'string',enum:['yes-real-tension','no-non-diagnostic','partial']}, key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'}, both_ways:{type:'string'}, sources:{type:'string'} }, required:['calculation','sigma_raw','sigma_norm_marginalized','sigma_systematic_marginalized','slope_survives_marginalization','key_numbers','script_path','both_ways','sources'] } })

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways. Prior:\n${JSON.stringify(comp).slice(0,9000)}\n\nCheck: (1) is the NORMALIZATION-marginalized (shape-only) test the FAIR one (a0(0) is a framework INPUT, so the absolute offset must be free)? (2) does MUSE's rising SLOPE genuinely survive marginalizing the offset -- i.e. is there a real >2-3sigma slope-tension with the framework's flat/declining shape, or does it collapse? (3) is the systematic-marginalized (Magneticum) nuisance applied HONESTLY (not over-subtracted to manufacture non-diagnostic; not ignored to manufacture a kill)? (4) the binned errors + the 30sigma slope claim -- is the chi^2 using the real errors? (5) re-run the load-bearing chi^2 for the declining branch under treatment (b). Return: holds_up (solid/partial/overclaimed/dead), honest_sigma, real_tension_or_nondiagnostic, high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, honest_sigma:{type:'string'}, real_tension_or_nondiagnostic:{type:'string'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','honest_sigma','real_tension_or_nondiagnostic','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE: how many sigma does Ciocan/MUSE actually exclude the framework's a0(z) shape, marginalized honestly?\nCOMPUTE:\n${JSON.stringify(comp).slice(0,5000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4000)}\n\nReturn 'report' (markdown) + fields. Cover: the sigma-exclusion of the declining branch under raw / normalization-marginalized / systematic-marginalized; whether the rising SLOPE is a REAL tension (>~2-3sigma after marginalizing the offset) or EARNED non-diagnostic (collapses); what it means for Front C (the a0(z) hostage); whether w->-1 or DESI DR3 changes it; what would settle it. Both-ways, quarantine, footing-honest (a0(0) is an INPUT so the shape-only test is the fair one).`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['real-tension-slope-survives','earned-non-diagnostic','genuinely-bracketed','partial']}, honest_sigma:{type:'string'}, impact_on_front_c:{type:'string'}, what_settles_it:{type:'string'} }, required:['report','verdict','honest_sigma','impact_on_front_c','what_settles_it'] } })
return { synth, comp, ver, pull }
