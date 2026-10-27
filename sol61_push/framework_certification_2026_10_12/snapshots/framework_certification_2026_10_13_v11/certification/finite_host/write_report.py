from pathlib import Path
import json,hashlib
here=Path(__file__).resolve().parent
c=json.loads((here/'comparison_run/results.json').read_text()); a=json.loads((here/'run_N32/results.json').read_text()); b=json.loads((here/'run_N64/results.json').read_text()); manifests={name:json.loads((here/name/'manifest.json').read_text()) for name in ['run_N32','run_N64','comparison_run']}
rows=b['rows']; worst=max(r['represented_residual'] for r in a['rows']+b['rows']);checks=a['checks']+b['checks']+c['checks']
report=f'''FINITE HOST: THE DECLARED NONLOCAL CANDIDATE DOES NOT RETAIN ITS SATELLITE RESPONSE
12 October 2026. Scope: a bounded continuation, independently assigned agent;
same model/source family and compiler ecosystem, not an independent external referee.
Primary verdict: implementation and finite assertion verified in the stated range.
Scientific verdict: {c['verdict']}.

Result
------
At fixed L=16, a finite displaced host changes the candidate's incremental
satellite internal field by {100*a['primary_vector_nonadditivity']:.4f}% on N32 and
{100*b['primary_vector_nonadditivity']:.4f}% on N64, compared with the predeclared 5% gate.
The radial metrics are {100*a['radial_nonadditivity']:.4f}% and {100*b['radial_nonadditivity']:.4f}%.
All numerical/control/fidelity checks pass. This is a finite periodic result for
one prescribed satellite/host pair; it rejects this candidate's claimed own-source
independence for that pair, not every framework completion or nonlocal action.

Frozen experiment
-----------------
FROZEN_CRITERIA.txt and both contracts were written before either new solve.
The inherited static action is, in units C=a0=1,
 E[Phi]=int[|grad Phi|^2/2+ec(|P_L grad Phi|)+rho_b Phi]dx,
 P_L(k)=1-exp(-k^2 L^2/2), ec'(g)=B(g)-g.
The OUTER P_L in the variational flux is retained. The repaired table is extracted
by AST whitelist from CFG596's kernel assignments/functions. Background, Planck
parameters, transfer functions, galaxy laws used as comparators and PM engines
are not executed/imported. The kernel itself is explicitly inverse-designed from
the framework's adopted acceleration law: this route still FAILS target-free R0.
L remains an undetermined effective input, not a microphysical prediction.

Box64, fixed L16, satellite Gaussian width2 and mass4*pi at the origin;
host Gaussian width4 and mass400*pi at (16,0,0), periodic minimum-image distance.
Positive profiles are discretely normalized; their means are subtracted to
satisfy the periodic source constraint. N32 and N64 are the only tested grids.
For each grid the satellite, host and combined static solutions are optimized.
No parameter was changed after seeing the coarse result.

What is actually compared
-------------------------
Let q_s, q_h, q_sh be the gradient fields in those three solves and
center(q)=q-q(0). The observable surrogate on 4<=r<=8 is
 ||center(q_sh-q_h)-center(q_s)||_2 / ||center(q_s)||_2.
Physical acceleration has the opposite sign; the norm comparison is unchanged.
Subtracting the separately SOLVED host-only field removes its full tidal field,
not only a uniform acceleration. The zero-nonlinear-response control performs
this same subtraction and yields {next(x['value'] for x in b['checks'] if x['name'].startswith('linear source')):.3e} relative error on N64.
Thus the 66.8% discrepancy is nonlinear source/environment nonadditivity. It is
not an unsubtracted ordinary host tide. This source-superposition diagnostic
nevertheless does not describe a real satellite's deformation, or demand that
physical orbits ignore host tides. No live satellite dynamics are simulated.

Uniform versus nonuniform environments
-------------------------------------
An added constant gradient is annihilated by P_L, so it changes neither nonlinear
response nor variational residual. Every grid's three residual-invariance checks
pass at <4e-15; a separate check also annihilates the actual host-center gradient.
The finite host has spatially varying/tidal modes: on N64 its centered field norm
in the diagnostic region is {b['host_tidal_L2_over_satellite_internal_L2']:.4f} times the satellite internal norm, and
its filtered field norm is {b['host_filtered_L2_over_satellite_internal_L2']:.4f} times that norm.
The host-center gradient is {b['host_center_gradient']}; its central Jacobian is
{b['host_center_gradient_jacobian']}.
The filter removes k=0 exactly, but cannot remove arbitrary finite-k host modes
without also suppressing corresponding internal modes. This example is the
previously unresolved finite-host discriminator; the old uniform-field success
remains valid, with its original narrow interpretation.

Numerical fidelity and invariant checks
--------------------------------------
Worst represented-source Poisson residual over all six solves: {worst:.3e},
against 1e-3. Directional variation errors: all <1e-4. Mass normalization,
zero-integral effective contrast, constant-gradient invariance and linear
source-subtraction controls all pass. Both-grid optimizer statuses are successful.
Matched-point coarse/fine baseline-field difference: {100*c['checks'][0]['value']:.4f}%.
Matched-point incremental-field difference: {100*c['checks'][1]['value']:.4f}%.
Primary metric grid difference: {100*c['checks'][2]['value']:.4f} percentage points.
These pass the frozen 3% fidelity lines and are far smaller than the failed
5% host-independence threshold. They are sensitivity checks, not rigorous
continuum error bounds or proof of uniqueness of the optimized PDE solution.
The even-grid Nyquist derivative null modes are explicitly projected. Coarse
satellite omitted-source fraction is {a['rows'][0]['source_null_fraction']:.3e}; fine
satellite fraction {b['rows'][0]['source_null_fraction']:.3e}. Fine combined fraction
{b['rows'][2]['source_null_fraction']:.3e}. These restrictions are recorded rather than hidden.

Positive mass and signed-source limitation
-----------------------------------------
rho_eff=div P_L p is periodic and integrates to zero. Every nonzero solved
contrast has both signs. N64 extrema and positive/negative integrals:
'''
for r in rows:
 report+=f" {r['name']}: min={r['rho_eff_min']:.8g}, max={r['rho_eff_max']:.8g}; positive integral={r['rho_eff_positive_integral']:.8g}, negative magnitude={r['rho_eff_negative_integral']:.8g}.\n"
report+=f'''
For the combined state a hypothetical uniform cold background must be at least
{rows[2]['minimum_hypothetical_positive_background']:.8g} in these density units just to offset the most negative
sampled contrast. No such background, abundance, transport/current, reservoir or
covariant metric is derived. Assigning this floor would be another input. A
positive baryonic Gaussian does not make the response an everywhere nonnegative
extra material density. This limitation is structural for this periodic contrast
representation; it does not exclude a separately specified positive background.

Execution and provenance
------------------------
Exactly three bounded runner invocations: two solver runs (wall cap90 seconds,
CPU85 seconds each) and one comparison run (wall30/CPU25). One process and one
cooperative numerical-library thread per invocation; no production simulation.
'''
for name,m in manifests.items():
 report+=f" {name}: schema v{m['schema_version']}, status={m['run']['status']}, runtime={m['run']['runtime_seconds']:.4f}s, Git={m['repository']['commit']}, dirty={m['repository']['dirty']}.\n"
report+='''
The computation-audit manifest validator was executed against the repository
root for all three records; each returned 'valid evidence record; mathematical
interpretation requires review'. Input/output hashes and actual argv are in the
manifests. Source hashes before and after match, including original calculate.py
and its contract. Original nonlocal evidence and all assumptions files remain
unchanged by this agent. Only finite_host/ received writes.

Self-audit and exact next gap
----------------------------
The implementation retains the original functional variation, Fourier-adjoint
operators, squared-field norm, response sign and positive source normalization.
Energy and variational gradients both include the cell volume. Effective-source
sign matches div P_L p. Gauge/Nyquist modes are not silently used as measured
source support. Comparison uses identical physical profiles and fixed L across
grids; the two grids change discretization rather than a physical coefficient.
No claim of global novelty, empirical preference, independence from the adopted
law, cold-mass identification, relativistic causality, lensing, attractor or TOE.

The exact unresolved physical step is a target-free causal mechanism that derives
an environmental/internal separation and positive conserved mass current without
per-host fitted lengths or labels. The tested Gaussian filter only guarantees
uniform-field blindness. Repeating its uniform test cannot restore finite-host
independence. This declared static route fails its next gate and should not be
escalated to a data fit or large settling simulation. A genuinely different
specified selector/boundary model would require a new prospective contract;
none has been invented here.
'''
(here/'RESULT.txt').write_text(report)
validation={'manifest_schema_version':2,'manifest_count':3,'all_completed':all(m['run']['status']=='completed' for m in manifests.values()),'all_numerical_controls_pass':all(x['passed'] for x in checks),'declared_physical_gate_pass':False,'primary_metric_N64':b['primary_vector_nonadditivity'],'checks_count':len(checks),'source_integrity_verified_by_manifest_validator':True,'scientific_scope':'Finite periodic host nonadditivity; mathematical/physical interpretation remains conditional','report_sha256':hashlib.sha256(report.encode()).hexdigest()}
(here/'verification.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps(validation))
