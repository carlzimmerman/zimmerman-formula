#!/usr/bin/env python3
"""Freeze metadata for this proof-only run; writes only this run directory."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[5]
REL = str(RUN.relative_to(ROOT))
TASK = 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-055.md'
FRAMEWORK = 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/FRAMEWORK_AND_EXECUTION.md'
CONTRACT = 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    path = RUN / name
    assert path.parent == RUN
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


ancestry = dict(re.findall(r'`([^`]+)` SHA256 `([a-f0-9]{64})`',
                          (ROOT / TASK).read_text()))
assert len(ancestry) == 10
for path, expected in ancestry.items():
    assert digest(ROOT / path) == expected
extra = [TASK, FRAMEWORK, CONTRACT,
 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-051/fgf051_run_001/DERIVATION.md',
 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-054/fgf054_run_001/input_pins.json',
 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-054/fgf054_run_001/verify_metadata.py']
inputs = dict(ancestry)
inputs.update({path: digest(ROOT / path) for path in extra})
assert inputs[extra[3]] == '37a88c86cd0ba56c1d30e10d79a68fda0dc2160313ae976712ab39f470418ac3'
old = json.loads((ROOT / 'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-054/fgf054_run_001/result.json').read_text())
for p in extra[4:]:
    assert inputs[p] == old['artifacts_sha256'][p]
write('input_pins.json', {
 'schema_version': 1, 'ancestry_count': 10,
 'verified_before_ancestry_source_use': True,
 'additional_local_construction_pin': extra[3],
 'additional_pin_note': 'FGF051 bytes checked before its read; its expected hash is also authenticated in the pinned FGF054 result. FGF054 input manifest and old verifier cross-checked against that result during final metadata review.',
 'input_sha256': inputs})
now = datetime.now(timezone.utc).isoformat()
stat = RUN.stat()
started = datetime.fromtimestamp(getattr(stat, 'st_birthtime', stat.st_ctime), timezone.utc).isoformat()
checks = [
 ('ancestry', 'ten of ten expected SHA256 pins matched before source use'),
 ('source_chart', 'all density, pressure, h_chi, scale response and restoring terms retained'),
 ('field_background', 'dz initial zero; exact (3.4) uses only background gradient; dz<=Af t'),
 ('exterior_fluid', 'actual acoustic wedge containment and exact advective source give u±=O(e^2)'),
 ('capacity_signs', 'two derivations give Delta prime = 4e j(A)-P'),
 ('remainder_orders', 'bulk e^3, pressure e^4, kinetic stress e^6, mass influx e^4 against mu e^2'),
 ('field_fluxes', 'nonzero field stress and both energy fluxes retained in exact balances'),
 ('speed_density', 'actual |v|<=V+Ee<Vmax; positive epsilon-uniform density and chart margins'),
 ('lower_domain', 'fresh fixed-V C1,1 start/trace/restart and restriction to identical K_e'),
 ('zero_velocity', 'exact H satisfies all equations, zero flux and no positive capacity margin'),
 ('framework', 'both normalizations, separate fixed histories, Q/MOND source and scope retained'),
 ('self_review', 'no internal gap found for precise bounded claim; not independent review')]
base_names = ['DERIVATION.md','FAILED_ROUTES.md','SELF_REVIEW.md','input_pins.json',
              'verify_metadata.py','freeze_metadata.py']
base_artifacts = {REL+'/'+name: digest(RUN/name) for name in base_names}
commands = [['python', REL+'/freeze_metadata.py'], ['python', REL+'/verify_metadata.py']]
write('manifest.json', {
 'schema_version': 1, 'task_id': 'FGF055', 'run_id':'fgf055_run_001',
 'input_sha256':inputs, 'artifacts_sha256':base_artifacts,
 'environment': {'python': sys.version, 'executable':sys.executable,
                 'platform':platform.platform(), 'cwd':str(ROOT)},
 'commands':commands,
 'proof_only':True, 'mathematical_computation_count':0,
 'no_raw_numerical_results':'No mathematical executable calculation or simulation was run. Raw mathematical output is DERIVATION.md.',
 'timestamp_scope':'started_utc is output directory creation time (artifact run); source inspection began earlier and was not separately wall-timed.',
 'metadata_verifier_inspection':'Author inspected verify_metadata.py source: read_bytes/read_text/hash/json/assert/print only; no writes, subprocesses, network or scientific computation.',
 'execution_note':'Proof reasoning has no numerical process. Metadata commands use existing Python standard library; no CPU/memory/thread/wall cap is claimed for the proof.'})
artifacts = dict(base_artifacts)
artifacts[REL+'/manifest.json'] = digest(RUN/'manifest.json')
result = {
 'task_id':'FGF055', 'task_sha256':inputs[TASK], 'run_id':'fgf055_run_001',
 'worker':{'agent':'/root/fgf055_author','execution_id':'fgf055_run_001','model':'inherited parent model; exact backend model identifier not exposed to this worker'},
 'started_utc':started, 'finished_utc':now,
 'outcome':'supports_scoped_claim',
 'acceptance_state':'unreviewed', 'orchestrator_review_required':True,
 'exact_claim':'For every fixed positive coefficient/compatible smooth hydrostatic tuple with Vmax>15cs/2, fixed 15cs/2<V<Vmax and 15/2<B<Bcap<V/cs, sufficiently small epsilon admits positive compatible exact-C1,1-packet evolution on the explicitly contained K_e through kappa epsilon/V, but no positive C1 solution on the same K_e survives through B epsilon/V. On existing prefixes: actual field-background perturbation O(epsilon), exterior fluid deviations at +/-2epsilon O(epsilon^2), epsilon-uniform positive density/field margins and |v|<Vmax. All finite fixed Q/scale speeds allowed without a field-speed<V inequality.',
 'new_assumptions':['Sufficient conditional acoustic parameter cell Vmax>15cs/2 with fixed V and strict B,Bcap margins; not an authenticated numerical physical tuple.','The upper implication concerns positive C1 solutions on a neighborhood of the closed contained cone; no maximal-germ equivalence is claimed.'],
 'input_sha256':inputs, 'artifacts_sha256':artifacts,
 'commands':commands,
 'commands_scope':'Only metadata replay commands listed; mathematical commands are empty because this is a proof-only task. Source inspections and artifact text writes are not mathematical experiments.',
 'execution_bounds':{'mathematical_processes':0,'requested_numerical_wall_seconds':120,
  'requested_numeric_library_threads':1,'actual_numerical_bounds':'not applicable; no numerical process launched',
  'proof_wall_cap':'not claimed','cpu_cap':'not enforced or claimed','memory_cap':'not enforced or claimed',
  'metadata':'Read-only SHA256/schema verifier; metadata is not scientific validation. No numeric libraries, logs or raw scientific arrays generated.'},
 'checks':[{'name':n,'observed':o,'tolerance':'exact analytic proof / exact byte comparison, not floating point','status':'passed_author_check'} for n,o in checks],
 'tested_domain':{'type':'exact_analytic','parameter_domain':'all fixed positive coefficients and compatible smooth H with g0,rho>0 satisfying acoustic cell',
  'epsilon_domain':'0<epsilon<L e0, with e0 the finite positive minimum of Section 8 constraints',
  'time_domain':'actual prefixes to Bcap epsilon/V; lower existence kappa epsilon/V; upper contradiction B epsilon/V',
  'spatial_domain':'X in [-(3+S Bcap/V)e+St,(3+S Bcap/V)e-St], contained in original fixed patch',
  'units':'fixed L,u,nref reference units; restored physical time epsilon/V',
  'samples':0,'seed':None,'exclusions':'No coefficient-uniform limit, evolving reference, weak/shock classification, physical calibration, or maximal-endpoint theorem'},
 'failed_attempts':[{'path':REL+'/FAILED_ROUTES.md','cause':'Invalid stationary-collar, gradient, source-centering, flux-deletion and old-rescaling transfers rejected analytically; no PDE counterexample inferred.'}],
 'limitations':'Unreviewed analytic author result only. No authenticated physical tuple, global/maximal-germ theorem, endpoint classification, low-Mach bound, physical metric/photon/two-DOF completion, criterion B, empirical calibration, cosmology, or novelty conclusion. Constants may be arbitrarily poor for fast fixed fields. Failure of the sufficient acoustic cell is not a PDE counterexample.',
 'next_unresolved_implication':'No internal missing implication identified in the precise bounded cone theorem by author self-review. Promotion requires a separate independent audit pinning raw proof/result hashes, particularly the actual-background subtraction, exterior-wedge bootstrap, flux identity and fresh same-domain lower construction.',
 'suggested_followup':'Independent raw-proof audit of DERIVATION Sections 3--7 with this frozen proof/result pair; do not demand an out-of-scope maximal-germ/endpoint theorem.',
 'mathematical_computation_count':0,
 'metadata_verifier':'verify_metadata.py is inspected read-only metadata, not mathematical evidence',
 'no_stage42_root_reviewer_exposure':True}
write('result.json', result)
freeze = dict(artifacts)
freeze[REL+'/result.json']=digest(RUN/'result.json')
write('FREEZE.json',{'schema_version':1,'sha256':freeze,
 'note':'FREEZE.json excluded from self-referential hash mapping; exact inventory replayed by read-only verifier.'})
print('Frozen unreviewed proof-only author candidate.')
print('DERIVATION_SHA256='+digest(RUN/'DERIVATION.md'))
print('RESULT_SHA256='+digest(RUN/'result.json'))
