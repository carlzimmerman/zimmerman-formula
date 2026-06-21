export const meta = {
  name: 'real-research-cluster-leads',
  description: "Carl: what does real_research/ (the ORIGINAL framework corpus, pre-opus_48) say about galaxy clusters, and is there an UNEXPLOITED lead there to push the cluster work forward, or have we hit the final frontier? Deep-read the real_research cluster corpus (AEST_MASS_SCALE_two_doors, the theta-coupling/locality line, the eta-derivation attempts, the density-a0 HIS_FORMULA, CORRECTION_NO_DARK_MATTER, FRAMEWORK_EMPIRICAL_STANDING) and CROSS-ASSESS against what opus_48 already EXHAUSTED today (the field-clustering no-go, the |Phi| static+collapse descriptive-not-predictive, the baryon census, the doors hunt, XRISM, WL-hydro). Both-ways: name a GENUINELY-new live lead if one exists (the calc to run), or confirm the final frontier (the cluster theory program is complete; only observational eta + the long-shot 3D N-body remain). NO manufactured lead, NO high-priest dismissal.",
  phases: [
    { title: 'Read', detail: 'three parallel deep-reads of the real_research cluster corpus: the AeST-mass-scale/theta-coupling theory line; the eta-derivation/density-a0 phenomenology; the empirical-standing/no-dark-matter line' },
    { title: 'Synthesize', detail: 'cross-assess vs the opus_48 exhausted leads -> a live unexploited lead (name the calc) or the final frontier' },
  ],
}

const FW = `
FRAMEWORK (Zimmerman): a0=c^2 sqrt(Lambda/32pi)=9.36e-11 (INPUT), modified-INERTIA dS-Unruh MOND,
AeST-embedded dark sector. THE TASK: assess whether real_research/ (Carl's ORIGINAL framework corpus,
written before today's opus_48 cluster deep-dives) contains an UNEXPLOITED cluster lead, or whether the
cluster program has hit the final frontier.

WHAT opus_48 ALREADY EXHAUSTED TODAY (the baseline -- do NOT re-propose these as 'new'): (1) no-particle
THEORY hunt EXHAUSTED (no door clears all 4 gates; the |Phi|/c^2-depth-keyed boost is the near-miss,
fails naturalness); (2) the field-clustering no-go (the AeST Q-mode HAS the cluster mass 1.46x but
CANNOT be galaxy-safe AND cluster-clumpy -- density-ordering + cs^2->0, B=0 verbatim; PUBLISHED Zenodo
10.5281/zenodo.20779562); (3) the AeST nonlinear +mu^2*Phi boundary-term |Phi| enhancement -- COMPUTED
(the Durakovic-Skordis deferred calc), REAL+big+galaxy-safe but DESCRIPTIVE-not-predictive (the
oscillation phase is free; the static BVP and the dynamical SPHERICAL COLLAPSE both leave it
IC-dependent -- the collapse just landed: phase TRACKS the ICs, slope ~1.1, NO pin); (4) baryon census
(shaves ~36%, f_b ceiling); (5) WL-vs-hydro mass proxy (consensus ~1.23, core robust ~1.03); (6) XRISM
turbulence (shut); (7) time-domain/formation MI (wrong-signed); (8) neutrinos (KATRIN/DESI excluded).
The remaining open: the FULL 3D cosmological AeST N-body (a long shot, the spherical collapse points
against), and the OBSERVATIONAL eta magnitude.

THE JOB: deep-read the assigned real_research cluster files. For each idea/mechanism found, classify:
(a) ALREADY-ABSORBED -- opus_48 already did/superseded it (say which); (b) GENUINELY-UNEXPLOITED -- a
mechanism/derivation real_research tried that opus_48 did NOT, that could push clusters forward (name
the exact calc to run); (c) SUPERSEDED-WRONG -- real_research tried it and it's since been refuted.
Pay special attention to: the AeST mass-scale 'two doors' (is there a SECOND door not yet tried?); the
'theta-coupling / theta-profile / strained-horizon-Wald-theta' line (is theta a distinct cluster
mechanism -- a locality/geometric coupling -- opus_48 has NOT tested?); the eta-derivation attempts
(did real_research find an eta derivation opus_48 missed?); the density-a0 'HIS FORMULA' (Carl's own
cluster density-a0 -- still live?).

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): if a GENUINE unexploited
lead exists, name it + the calc at full weight (Carl wants to push forward); if everything is
absorbed/superseded, confirm the FINAL FRONTIER honestly (do NOT manufacture a lead to please).
QUARANTINE: a0/Z/kappa/I0 never derived. Read the REAL files; cite exact filenames + what they say.
`

const FILES_A = "AEST_MASS_SCALE_two_doors.md, reviews/GEOMETRIC_ACTION_theta_coupling.md, reviews/theta_3H_coupling.py, reviews/aest_locality_theta_profile.py, reviews/strained_horizon_wald_theta.py, TOE_EMERGENT_HORIZON.md, THE_EVENT_HORIZON_DOOR.md";
const FILES_B = "reviews/eta_derivation_attempt.md, reviews/eta_rigorous_research.md, reviews/ETA_LOCAL_RIGOROUS.md, reviews/eta_local_bruning_seeley.py, reviews/eta_invariant_reality_check.py, reviews/cluster_a0_from_density_HIS_FORMULA.py, reviews/cluster_residual_evolution.py, reviews/clusters_eta_audit.py, A0_DENSITY_EMPIRICAL_EVIDENCE.md";
const FILES_C = "FRAMEWORK_EMPIRICAL_STANDING.md, CORRECTION_NO_DARK_MATTER_2026-06-06.md, FALSIFICATION_MATRIX.md, OFFENSIVE_FOUR_FRONTS_2026-06-06.md, OPEN_DOORS_AGENT_SWEEP_2026-06-05.md, CONSISTENCY_STRESS_TESTS.md, ULTRATHINK_REDTEAM.md, reviews/project_cluster_evolving_a0.py, reviews/project16_clusters.py";

const SCH = { type:'object', additionalProperties:false, properties:{
  route:{type:'string'},
  ideas:{ type:'array', items:{ type:'object', additionalProperties:false, properties:{
    mechanism:{type:'string'}, file:{type:'string'},
    status:{type:'string', enum:['already-absorbed','genuinely-unexploited','superseded-wrong']},
    the_calc_if_lead:{type:'string', description:'if genuinely-unexploited, the exact calc to run; else "n/a"'},
    note:{type:'string'} },
    required:['mechanism','file','status','the_calc_if_lead','note'] } },
  best_lead:{type:'string', description:'the single most promising genuinely-unexploited lead, or "none -- final frontier"'},
  sources:{type:'string'} },
  required:['route','ideas','best_lead','sources'] };

phase('Read')
const reads = await parallel([
  () => agent(`${FW}\n\nREAD ROUTE A -- the AeST-mass-scale + theta-coupling/horizon THEORY line. Deep-read: ${FILES_A}. What cluster mechanisms do they contain? Is the AeST mass-scale 'two doors' a SECOND door opus_48 did NOT try (opus_48 did the +mu^2*Phi boundary term + the collapse phase-pin)? Is the 'theta-coupling / theta-profile / strained-horizon-Wald-theta' a DISTINCT cluster mechanism (a locality/geometric/horizon coupling) opus_48 has NOT tested? Classify each. Return the structured object.`,
    { label:'read:aest-theta-theory', phase:'Read', schema: SCH }),
  () => agent(`${FW}\n\nREAD ROUTE B -- the eta-derivation + density-a0 PHENOMENOLOGY line. Deep-read: ${FILES_B}. Did real_research find an eta(R500) DERIVATION or a density-a0 cluster mechanism ('HIS FORMULA') that opus_48 did NOT absorb? Is any of it a live lead (a calc that closes/shaves the residual opus_48 missed)? Classify each. Return the structured object.`,
    { label:'read:eta-density-pheno', phase:'Read', schema: SCH }),
  () => agent(`${FW}\n\nREAD ROUTE C -- the empirical-standing + no-dark-matter + falsification line. Deep-read: ${FILES_C}. What is the original framework's stated cluster standing + the 'CORRECTION_NO_DARK_MATTER' content? Do the OPEN_DOORS / OFFENSIVE_FOUR_FRONTS / REDTEAM docs list a cluster door opus_48 did NOT try? Any unexploited lead? Classify each. Return the structured object.`,
    { label:'read:standing-nodm-falsif', phase:'Read', schema: SCH }),
])
const R = reads.filter(Boolean)

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE: does real_research contain a GENUINELY-unexploited cluster lead to push forward, or is this the final frontier?\n\nTHREE READS:\n${JSON.stringify(R).slice(0,14000)}\n\nReturn 'report' (markdown) + fields. Cover: (1) what real_research says about clusters (the mechanisms it tried); (2) for each, ALREADY-ABSORBED vs GENUINELY-UNEXPLOITED vs SUPERSEDED -- cross-checked against the opus_48 exhausted baseline; (3) THE VERDICT -- is there a single genuinely-unexploited lead (name it + the exact calc to run + why opus_48 missed it), or is this the FINAL FRONTIER (the cluster theory program is complete; only observational eta + the long-shot 3D N-body remain)? (4) if a lead exists, how promising honestly (and the prior -- most leads end up absorbed/naturalness-blocked). Both-ways, quarantine, NO manufactured lead, NO high-priest dismissal.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{
    report:{type:'string'},
    verdict:{type:'string', enum:['live-unexploited-lead','final-frontier-confirmed','partial-lead-low-prior']},
    best_lead:{type:'string'}, the_calc:{type:'string'}, why_opus48_missed_it:{type:'string'},
    final_frontier_status:{type:'string'} },
    required:['report','verdict','best_lead','the_calc','why_opus48_missed_it','final_frontier_status'] } })
return { synth, reads: R }
