export const meta = {
  name: 'aest-collapse-phase-pinning',
  description: "THE one open door (Carl): does DYNAMICAL structure formation pin the AeST oscillation phase / chi_infty that the STATIC boundary-value solve left free? The static spherical solve (wn6n716aa) found the nonlinear +mu^2*Phi cluster boost is real+big+galaxy-safe but DESCRIPTIVE (the boundary admits eta from -3 to +4; the natural value is a deficit). The question the static BVP cannot answer: in a cluster that COLLAPSES from cosmological initial conditions through turnaround, does the time-evolution DYNAMICALLY SELECT a unique phase (a boost universally -> door reopens, clusters close galaxy-safely-AND-predictively) or leave it free / select the deficit (no-go holds dynamically)? SCOPING version = a spherical-collapse-through-turnaround AeST solve (1+1D, radius x time), NOT a full 3D N-body (that is research-group-scale). Both ways, quarantine, no manufactured pin.",
  phases: [
    { title: 'Derive', detail: 'pull the AeST time-dependent / cosmological-perturbation + collapse equations; set up the spherical-collapse-with-AeST formalism + the initial conditions' },
    { title: 'Compute', detail: 'numerical spherical collapse through turnaround with the AeST field solved each step; does chi_infty / the phase dynamically converge to a unique value?' },
    { title: 'Verify', detail: 'adversarial both-ways: is the dynamical phase-selection real + universal (boost) + galaxy-safe, or IC-dependent / deficit / unpinned? no manufactured pin' },
    { title: 'Synthesize', detail: 'does dynamics pin the phase (door reopens, follow-up paper) or not (no-go holds dynamically); + the honest scope vs a full 3D N-body' },
  ],
}

const FW = `
FRAMEWORK + AeST: a0=c^2 sqrt(Lambda/32pi)=9.36e-11 (INPUT). Dark sector = the AeST (Skordis-Zlosnik
2021 arXiv:2007.00082; Blanchet-Skordis 2024 arXiv:2404.06584) shift-symmetric scalar. THE STATIC
RESULT (banked AEST_NONLINEAR_PHI_CLUSTER_2026-06-20, published paper Zenodo 10.5281/zenodo.20779562):
the nonlinear weak-field +mu^2*Phi Helmholtz mass term (DS24 Eq2.40/BS24 Eq3.21) breaks shift-invariance
so the asymptotic level chi_infty becomes physical and feeds a phantom source; the cluster-core boost is
REAL (~1e5x the naive coupling, reaching 28-100% of the residual) and GALAXY+CASSINI-safe -- BUT
DESCRIPTIVE not predictive: the Helmholtz oscillation PHASE sets the boost, the SAME cosmological
chi_infty admits eta(R500) from -3.12 to +3.97 (5 dPhi0 roots), the NATURAL untuned boundary gives a
DEFICIT (eta=-1.54), and the universal value breaks galaxies (+0.275 dex). The static boundary-value
problem leaves chi_infty / the phase FREE.

THE OPEN DOOR (the published paper's one un-closed branch, the AeST authors' DS24 deferred all the way):
does DYNAMICAL structure formation PIN the phase the static BVP leaves free? A real cluster does not
appear with a static boundary -- it COLLAPSES from cosmological initial conditions, turns around, and
virializes. The time-dependent AeST field is sourced by the evolving density and the collapse history;
the oscillation phase / chi_infty at virialization is then an OUTPUT of the dynamics, not a free input.
THE QUESTION: does the collapse dynamically SELECT a unique phase -- and if so, is it a BOOST phase,
UNIVERSALLY (independent of cluster mass / IC), and GALAXY-SAFE? If yes -> the door REOPENS: clusters
close with no dark matter, galaxy-safely AND predictively (a follow-up paper, the strong result). If
the phase is IC-dependent / converges to the deficit / stays unpinned -> the no-go holds DYNAMICALLY too
(the static result confirmed).

THE SCOPING (be HONEST about it): a FULL 3D cosmological AeST N-body is research-group-scale and NOT
producible here. The tractable, load-bearing version: a SPHERICAL-COLLAPSE-through-turnaround AeST solve
(1+1D: radius x time) -- a spherical overdensity evolved from cosmological ICs through turnaround and
virialization, with the AeST weak-field/khronon field solved at each time step, tracking whether the
oscillation phase / chi_infty CONVERGES to a unique value as the system virializes. This is the standard
spherical-collapse reduction of structure formation, plus the AeST field -- it directly tests the
phase-pinning question the static BVP cannot, and is the honest next step beyond wn6n716aa.

BOTH-WAYS (Carl #1 rule -- penalize high-priest AND manufacturing EQUALLY): this could genuinely reopen
the door (the strong result Carl wants) or confirm the no-go dynamically. If the collapse pins a boost
phase universally + galaxy-safely, BUILD it at full weight (state the selected phase, the magnitude, the
universality, the galaxy-veto). If it does NOT (phase IC-dependent, deficit-selected, or the galaxy
collapse ALSO pins a boost = breaks the RAR), report the no-go holds. Do NOT manufacture a pin (the
selected phase must come from the solved collapse dynamics, robust to ICs); do NOT high-priest (if the
dynamics genuinely select a boost, credit it). QUARANTINE: a0/Z/kappa/I0 never derived. Solve the REAL
AeST collapse equations (numpy/scipy time-dependent ODE/PDE), NOT a proxy. WebSearch/WebFetch
Skordis-Zlosnik 2021 (cosmological perturbations), Blanchet-Skordis 2024, Verwayen-Skordis-Boehm 2024
(time-dependent oscillatory r_C), Durakovic-Skordis 2024, + spherical-collapse-in-MOND (Sanders,
Nusser) for the collapse formalism.
`

phase('Derive')
const der = await agent(`${FW}\n\nDERIVE + SET UP the spherical-collapse-with-AeST formalism. WebSearch/WebFetch the AeST cosmological-perturbation + time-dependent field equations (SZ2021 long paper; BS2024; Verwayen-Skordis-Boehm 2024 for the time-dependent oscillatory scalar) + the spherical-collapse-in-MOND formalism (Sanders 2001, Nusser 2002). Set up: (1) the spherical collapse of an overdensity from cosmological ICs through turnaround + virialization (the shell/fluid equations, Hubble drag, the MOND-boosted infall); (2) the AeST weak-field/khronon field equation solved at each time step (the +mu^2*Phi Helmholtz term sourced by the evolving rho), and HOW the asymptotic level chi_infty / the oscillation phase is determined by the time-dependent solution + the cosmological boundary (Phi(infinity,t)=cosmic); (3) the diagnostic: track chi_infty / the phase as the system virializes -- does it converge to a unique value? Return: collapse_equations, aest_field_in_collapse, phase_diagnostic (how chi_infty is read off the dynamical solution), initial_conditions, key_facts (array), sources. Write the setup under opus_48_extended_research/reviews/aest_collapse/.`,
  { label:'derive:collapse-aest', phase:'Derive', schema:{ type:'object', additionalProperties:false, properties:{ collapse_equations:{type:'string'}, aest_field_in_collapse:{type:'string'}, phase_diagnostic:{type:'string'}, initial_conditions:{type:'string'}, key_facts:{type:'array',items:{type:'string'}}, sources:{type:'string'} }, required:['collapse_equations','aest_field_in_collapse','phase_diagnostic','initial_conditions','key_facts','sources'] } })

phase('Compute')
const comp = await agent(`${FW}\n\nCOMPUTE the spherical collapse through turnaround. Using:\n${JSON.stringify(der).slice(0,9000)}\n\nBuild a NUMERICAL spherical-collapse solver (1+1D, radius x time): evolve a spherical cluster-scale overdensity from cosmological ICs (z~10-30) through turnaround (z~0.5-1) to virialization, solving the AeST +mu^2*Phi field at each time step with the cosmological boundary Phi(infinity,t). Track: (1) does the oscillation phase / chi_infty CONVERGE to a unique value as the system virializes (the dynamical pinning), or stay free/IC-dependent? (2) if it converges, is it a BOOST phase (eta>1, closing the residual) or the DEFICIT (eta<1)? (3) is the selected phase UNIVERSAL -- robust to the IC amplitude / cluster mass / collapse epoch (run 3-5 ICs)? (4) CRUCIAL galaxy check: run the SAME collapse for a GALAXY-scale overdensity -- does it ALSO pin a boost (which would break the RAR), or stay galaxy-safe? WRITE the solver under opus_48_extended_research/reviews/aest_collapse/. Both-ways; quarantine. Return: calculation, phase_pinned (unique-boost/unique-deficit/IC-dependent/unpinned), cluster_eta_dynamical, universal (yes/no/partial), galaxy_safe (safe/breaks/n_a), key_numbers (array), script_path, both_ways, sources.`,
  { label:'compute:collapse', phase:'Compute', schema:{ type:'object', additionalProperties:false, properties:{ calculation:{type:'string'}, phase_pinned:{type:'string',enum:['unique-boost','unique-deficit','IC-dependent','unpinned']}, cluster_eta_dynamical:{type:'string'}, universal:{type:'string',enum:['yes','no','partial']}, galaxy_safe:{type:'string',enum:['safe','breaks','n_a']}, key_numbers:{type:'array',items:{type:'string'}}, script_path:{type:'string'}, both_ways:{type:'string'}, sources:{type:'string'} }, required:['calculation','phase_pinned','cluster_eta_dynamical','universal','galaxy_safe','key_numbers','script_path','both_ways','sources'] } })

phase('Verify')
const ver = await agent(`${FW}\n\nSKEPTIC, both-ways (this decides whether the door reopens). Derivation:\n${JSON.stringify(der).slice(0,4500)}\nCompute:\n${JSON.stringify(comp).slice(0,8000)}\n\nCheck HARD: (1) is the collapse+AeST solver CORRECT (real spherical-collapse + the real AeST +mu^2*Phi field, not a proxy; MOND-boosted infall right)? (2) does the phase GENUINELY converge dynamically, or is the 'pinning' an artifact of the ICs / the boundary treatment / numerical damping? re-run the load-bearing convergence. (3) if a boost is pinned -- is it UNIVERSAL (robust to IC amplitude/mass/epoch) or tuned? (4) the GALAXY check -- does the galaxy-scale collapse ALSO pin a boost (breaking the RAR)? this is the kill if so. (5) is any 'door reopens' MANUFACTURED (a pin that isn't robust) or any 'no-go holds' HIGH-PRIEST (dismissing a real dynamical selection)? (6) honest scope: does the spherical-collapse scoping genuinely settle it, or does it still need the full 3D N-body? Return: holds_up (solid/partial/overclaimed/dead), door_reopens (yes-clusters-close/no-nogo-holds/partial-needs-3d), the_pinned_phase, galaxy_safe_dynamical (bool), high_priest_or_manufactured, skeptic_findings, corrected.`,
  { label:'verify', phase:'Verify', schema:{ type:'object', additionalProperties:false, properties:{ holds_up:{type:'string',enum:['solid','partial','overclaimed','dead']}, door_reopens:{type:'string',enum:['yes-clusters-close','no-nogo-holds','partial-needs-3d']}, the_pinned_phase:{type:'string'}, galaxy_safe_dynamical:{type:'boolean'}, high_priest_or_manufactured:{type:'string'}, skeptic_findings:{type:'string'}, corrected:{type:'string'} }, required:['holds_up','door_reopens','the_pinned_phase','galaxy_safe_dynamical','high_priest_or_manufactured','skeptic_findings','corrected'] } })

phase('Synthesize')
const synth = await agent(`${FW}\n\nSYNTHESIZE: does DYNAMICAL collapse pin the AeST oscillation phase -> the cluster door REOPENS (clusters close galaxy-safely AND predictively), or does the no-go hold dynamically?\nDERIVE:\n${JSON.stringify(der).slice(0,4000)}\nCOMPUTE:\n${JSON.stringify(comp).slice(0,5000)}\nVERDICT:\n${JSON.stringify(ver).slice(0,4500)}\n\nReturn 'report' (markdown) + fields. Cover: (1) the spherical-collapse-with-AeST setup + what we computed; (2) does the collapse PIN the phase -- unique boost (door reopens), deficit, or IC-dependent/unpinned; (3) is it UNIVERSAL + GALAXY-SAFE (the galaxy collapse must NOT also pin a boost); (4) THE VERDICT -- door reopens (clusters explained galaxy-safely AND predictively = the strong result, a follow-up paper; state the pinned phase + magnitude + universality) OR no-go holds dynamically (the published paper stands; state why the phase isn't pinned to a universal galaxy-safe boost); (5) the HONEST SCOPE -- whether the spherical-collapse scoping settles it or the full 3D cosmological N-body is still needed (and what it would add). Both-ways, quarantine, NO manufactured pin. This is the decisive open computation for whether the framework explains clusters with no dark matter.`,
  { label:'synthesize', phase:'Synthesize', schema:{ type:'object', additionalProperties:false, properties:{ report:{type:'string'}, verdict:{type:'string',enum:['door-reopens-clusters-close','no-go-holds-dynamically','partial-needs-full-3d-nbody']}, pinned_phase:{type:'string'}, galaxy_safe:{type:'string'}, paper_implication:{type:'string'}, honest_scope:{type:'string'} }, required:['report','verdict','pinned_phase','galaxy_safe','paper_implication','honest_scope'] } })
return { synth, der, comp, ver }
