# KT40: equations, mechanism, and a decisive dynamics check

User asks to figure out equations, answers and mechanism after KT39's
p=9/8, ell=3kpc MW/Cassini witness, strict vertical failure and dwarf deficit.
Starting checkpoint: KT39 README, RESULTS, VERIFICATION and frozen source
hashes; Git HEAD e7f1ac9ca025031f5ec15679645913b10f66f4ad (shared dirty repository).

Target: derive the complete nonrelativistic field equations, explain which
response terms produce the measured results, determine the screening scale,
and test whether the response supplies sensible matter dynamics. A derived
phenomenological mechanism is weaker than a fundamental derivation of p,
ell,a0 or a relativistic theory; no such completion is assumed.

Four disjoint work scopes:
- root mw/: decompose Newton, A and B potentials for both frozen MW witnesses;
  evaluate local tidal susceptibilities on the actual baryon backgrounds;
- mechanism_scaling scaling/: analytic screening scales and point/Solar/dwarf
  asymptotics, verified against the fixed model;
- mechanism_dynamics dynamics/: derive continuity/Euler dispersion and give
  a decisive signed mathematical conclusion with exact hypotheses;
- mechanism_dwarf_efe efe/: derive/test the full-action scalar virial under
  a constant auxiliary external gradient, then run specified dwarf diagnostics.

Fixed scientific input: p=9/8, ell=3kpc, original a0 footings, baryons,
observational cuts and Solar constants. No new fits. External-field samples
are labeled diagnostics, not fitted satellite environments or LOS predictions.
Numerical experiments require pinned inputs, bounded runner contracts and
independent identities/refinement. New dynamics conclusions must distinguish
pressureless fluid, finite-pressure, collisionless and relativistic claims.
No old scientific artifact is changed. Status: mechanism checkpoint completed.
The field equations, screening scales, external-field compression stress and
conditional dynamical obstruction are derived. The fixed candidate has
outward-force and negative-virial numerical witnesses under the stated matter
assumptions. A fundamental mechanism or a viable replacement is not derived;
README and RESULTS record the exact remaining obligations and evidence scope.
