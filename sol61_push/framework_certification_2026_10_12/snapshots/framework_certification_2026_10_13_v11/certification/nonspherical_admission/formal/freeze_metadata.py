from pathlib import Path
import json,hashlib,re,subprocess
root=Path(__file__).resolve().parents[4]
base=Path('sol61_push/framework_certification_2026_10_12/nonspherical_admission'); p=root/base/'formal'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
assert (root/base/'DERIVATION.txt').exists() and (root/base/'RESULT.txt').exists()
files=[base/x for x in ['FROZEN_CRITERIA.txt','INTERPRETATION_REGISTER.json','DERIVATION.txt','RESULT.txt','checks.py','contract.json','INPUTS.json','run/results.json']]
if (root/base/'verification.json').exists():files.append(base/'verification.json')
files += [Path(x['source']) for x in json.loads((root/base/'INPUTS.json').read_text())['sources']]
files += [Path('fable_independent_2026/lean_2026')/x for x in ['lean-toolchain','lakefile.toml','lake-manifest.json']]
items=[]
for f in files:
 dest=p/'inputs'/f;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((root/f).read_bytes());items.append(dict(source=str(f),snapshot=str(Path('inputs')/f),sha256=sha(root/f),matches_source=True))
status='supplied reconciled A2/A5 low-branch calculus and two-source slices; full 3D norm-weighted divergence correspondence remains analytic' 
pin=dict(checkpoint='FRAMEWORK-CERT-METRIC-ACTION-2026-10-13',model_status=status,observed_live_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),inputs=items)
(p/'PINNED_INPUTS.json').write_text(json.dumps(pin,indent=2)+'\n')
s=(p/'Nonspherical.lean').read_text();entries=[]
for m in re.finditer(r'^theorem (\w+)',s,re.M):
 stmt=s[m.start():s.index(':= by',m.start())].rstrip();entries.append(dict(name='FrameworkNonspherical.'+m.group(1),line=s[:m.start()].count('\n')+1,exact_statement=stmt,statement_sha256=hashlib.sha256(stmt.encode()).hexdigest(),axioms=['propext','Classical.choice','Quot.sound'],status='kernel-checked explicit kernel/source calculus; full target-divergence identification not Lean proved',English_review='nonspherical_admission/formal/CORRESPONDENCE.txt'))
controls=[]
for name in ['FalseNuIncreasing','FalseEverywhereRising']:
 controls.append(dict(source=str(base/'formal'/(name+'.lean')),source_sha256=sha(p/(name+'.lean')),log=str(base/'formal'/(name+'.log')),log_sha256=sha(p/(name+'.log')),exit_code=1,expected_failure='final mathematical False; no import/type/syntax failure'))
rec=dict(namespace='FrameworkNonspherical',source=str(base/'formal/Nonspherical.lean'),source_sha256=sha(p/'Nonspherical.lean'),main_log=str(base/'formal/compile.log'),main_log_sha256=sha(p/'compile.log'),theorem_count=len(entries),entries=entries,model_status=status,checkpoint=pin['checkpoint'],imports=['Mathlib'],main_exit_code=0,PINNED_INPUTS=dict(path=str(base/'formal/PINNED_INPUTS.json'),sha256=sha(p/'PINNED_INPUTS.json')),correspondence=dict(path=str(base/'formal/CORRESPONDENCE.txt'),sha256=sha(p/'CORRESPONDENCE.txt')),independent_review_status='pending frozen metadata review; nine theorem bodies independently reviewed',historical_builds=[dict(accepted=False,source=str(base/'formal/build_history'/('attempt_'+n+'.source.txt')),log=str(base/'formal/build_history'/('attempt_'+n+'.log')),exit_code=1) for n in ['01','02','03','04','05']],false_controls=controls)
(p/'module_record.json').write_text(json.dumps(rec,indent=2)+'\n')
(p/'REPRODUCE.txt').write_text('cd '+str(root/'fable_independent_2026/lean_2026')+'\nlake env lean '+str(p/'Nonspherical.lean')+'\n# Expected exit0 and nine standard axiom reports.\nlake env lean '+str(p/'FalseNuIncreasing.lean')+'\nlake env lean '+str(p/'FalseEverywhereRising.lean')+'\n# Both expected exit1, final goal False.\n# No separate formal symbolic run; producer mixed42 evidence is pinned.\n')
assert len(entries)==9
log=(p/'compile.log').read_text();assert log.count('depends on axioms:')==9 and 'error:' not in log and 'sorryAx' not in log
for c in controls:assert '⊢ False' in (root/c['log']).read_text()
print(json.dumps({k:rec[k] for k in ['source_sha256','main_log_sha256','theorem_count']}))
