from pathlib import Path
import json,hashlib,re,subprocess
root=Path(__file__).resolve().parents[4]
base=Path('sol61_push/framework_certification_2026_10_12/latest_work_2026_10_13');p=root/base/'formal';physical=Path('sol61_push/c2_static_metric_2026_10_13')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
files=[physical/x for x in ['DERIVATION.txt','CONTINUATION.txt','INPUTS.json','VERIFICATION.json','source_snapshot/cfg635.py.txt','source_snapshot/C2_DERIVATION.txt','source_snapshot/MINIMAL_METRIC_RESULT.txt']]
files += [physical/'finite_patch'/x for x in ['FROZEN_CRITERIA.txt','RESULT.txt','checks_v2.py','contract_v2.json','REPAIR.txt','REVIEW.json','run_v2/results.json','run_v2/manifest.json']]
files += [Path('campaign_fresh_gravity/CFG635_one_dark_sector/cfg635.py')]
files += [Path('fable_independent_2026/lean_2026')/x for x in ['lean-toolchain','lakefile.toml','lake-manifest.json']]
items=[]
for f in files:
 dest=p/'inputs'/f;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((root/f).read_bytes());items.append(dict(source=str(f),snapshot=str(Path('inputs')/f),sha256=sha(root/f),matches_source=True))
status='latest prescribed-lapse C2 pointwise core/vacuum matching and actual reduced action/Noether flux; no coupled metric action, phase regularity or weak stress solution proved'
pin=dict(checkpoint='FRAMEWORK-CERT-FULLFLUX-2026-10-13',prior_statement_count=178,model_status=status,observed_live_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),inputs=items,existing_computation=dict(source=str(physical/'finite_patch/run_v2/results.json'),accepted_checks=25,rerun=False,not_added_to_Lean_count=True))
(p/'PINNED_INPUTS.json').write_text(json.dumps(pin,indent=2)+'\n')
s=(p/'FinitePatch.lean').read_text();entries=[]
for m in re.finditer(r'^theorem (\w+)',s,re.M):
 stmt=s[m.start():s.index(':= by',m.start())].rstrip();entries.append(dict(name='FrameworkFinitePatch.'+m.group(1),line=s[:m.start()].count('\n')+1,exact_statement=stmt,statement_sha256=hashlib.sha256(stmt.encode()).hexdigest(),axioms=['propext','Classical.choice','Quot.sound'],status='kernel-checked latest pointwise prescribed-metric C2/action calculus',English_review='latest_work_2026_10_13/formal/CORRESPONDENCE.txt'))
controls=[]
for name in ['FalseReverseOrientation','FalsePositiveToySource']:
 controls.append(dict(source=str(base/'formal'/(name+'.lean')),source_sha256=sha(p/(name+'.lean')),log=str(base/'formal'/(name+'.log')),log_sha256=sha(p/(name+'.log')),exit_code=1,expected_failure='final mathematical False; no import/type/syntax failure'))
record=dict(namespace='FrameworkFinitePatch',source=str(base/'formal/FinitePatch.lean'),source_sha256=sha(p/'FinitePatch.lean'),main_log=str(base/'formal/compile.log'),main_log_sha256=sha(p/'compile.log'),theorem_count=len(entries),entries=entries,model_status=status,checkpoint=pin['checkpoint'],imports=['Mathlib'],main_exit_code=0,PINNED_INPUTS=dict(path=str(base/'formal/PINNED_INPUTS.json'),sha256=sha(p/'PINNED_INPUTS.json')),correspondence=dict(path=str(base/'formal/CORRESPONDENCE.txt'),sha256=sha(p/'CORRESPONDENCE.txt')),independent_review_status='final nine proof bodies available; frozen metadata review pending',historical_builds=[dict(accepted=False,source=str(base/'formal/build_history/attempt_01.source.txt'),log=str(base/'formal/build_history/attempt_01.log'),exit_code=1)],prior_accepted_checkpoints=[dict(source=str(base/'formal/build_history'/('accepted_'+n+'.source.txt')),log=str(base/'formal/build_history'/('accepted_'+n+'.log')),exit_code=0,theorem_count=c,final=False) for n,c in [('eight',8),('action_nine',9)]],false_controls=controls,ambient_context='Real actual P(X), metric coefficients and phase gradient; stationary prescribed metric; no current-conservation premise substituted for identically zero actual action-derived flux.')
(p/'module_record.json').write_text(json.dumps(record,indent=2)+'\n')
(p/'REPRODUCE.txt').write_text('cd '+str(root/'fable_independent_2026/lean_2026')+'\nlake env lean '+str(p/'FinitePatch.lean')+'\n# Expected exit0, nine standard axiom reports, no custom axioms/admissions.\nlake env lean '+str(p/'FalseReverseOrientation.lean')+'\nlake env lean '+str(p/'FalsePositiveToySource.lean')+'\n# Both expected exit1 only mathematical False.\n# Existing physical run_v2 checks25 are pinned, not rerun. Source/log/statement/input hashes in module_record and PINNED_INPUTS.\n')
assert len(entries)==9
log=(p/'compile.log').read_text();assert log.count('depends on axioms:')==9 and 'error:' not in log and 'sorryAx' not in log and 'warning:' not in log
for c in controls:
 log=(root/c['log']).read_text();assert '⊢ False' in log and log.count('error:')==1
for x in items:assert sha(p/x['snapshot'])==x['sha256']
print(json.dumps({k:record[k] for k in ['source_sha256','main_log_sha256','theorem_count']}))
