from pathlib import Path
import json,hashlib,re,subprocess
root=Path(__file__).resolve().parents[4]
base=Path('sol61_push/framework_certification_2026_10_12/nonspherical_flux');p=root/base/'formal'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
origin=Path('sol61_push/framework_certification_2026_10_12/nonspherical_admission/formal/Nonspherical.lean')
assert sha(root/origin)==sha(p/'Nonspherical.lean')=='93325e1824f0a6ddb346010a2670b2003b9d38bcbc7e12fc2dd669ba6a6544cb'
admit=json.loads((root/base/'admission/PINNED_INPUTS.json').read_text())
files=[base/'admission'/x for x in ['DERIVATION.txt','MAPPING_REGISTER.json','ADMISSION_CLOSURE.txt','PINNED_INPUTS.json','verification.json']]
files += [Path(x['source']) for x in admit['sources']]
files += [origin,Path('sol61_push/framework_certification_2026_10_12/nonspherical_admission/formal/CORRESPONDENCE.txt')]
files += [Path('fable_independent_2026/lean_2026')/x for x in ['lean-toolchain','lakefile.toml','lake-manifest.json']]
items=[]
for f in dict.fromkeys(files):
 dest=p/'inputs'/f;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((root/f).read_bytes());items.append(dict(source=str(f),snapshot=str(Path('inputs')/f),sha256=sha(root/f),matches_source=True))
status='kernel checked actual 3D Euclidean-norm weighted source flux; raw target meaning/host applicability remains conditional, no framework closure'
dep=dict(module='Nonspherical',source='Nonspherical.lean',source_sha256=sha(p/'Nonspherical.lean'),compiled='build/Nonspherical.olean',compiled_sha256=sha(p/'build/Nonspherical.olean'),origin=str(origin),archive_matches_origin=True,original_checked_module='FrameworkNonspherical',dependency_compile_log='dependency_compile.log',dependency_compile_log_sha256=sha(p/'dependency_compile.log'),dependency_compile_exit_code=0)
pin=dict(checkpoint='FRAMEWORK-CERT-NONSPHERICAL-2026-10-13',model_status=status,observed_live_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),dependency=dep,inputs=items)
(p/'PINNED_INPUTS.json').write_text(json.dumps(pin,indent=2)+'\n')
s=(p/'FullFlux.lean').read_text();entries=[]
for m in re.finditer(r'^theorem (\w+)',s,re.M):
 stmt=s[m.start():s.index(':= by',m.start())].rstrip();entries.append(dict(name='FrameworkNonsphericalFlux.'+m.group(1),line=s[:m.start()].count('\n')+1,exact_statement=stmt,statement_sha256=hashlib.sha256(stmt.encode()).hexdigest(),axioms=['propext','Classical.choice','Quot.sound'],status='kernel-checked actual source/norm/flux calculus; physical admission limits explicit',English_review='nonspherical_flux/formal/CORRESPONDENCE.txt'))
controls=[]
for name in ['FalseKernelIncreasing','FalseActualTargetNonnegative']:
 controls.append(dict(source=str(base/'formal'/(name+'.lean')),source_sha256=sha(p/(name+'.lean')),log=str(base/'formal'/(name+'.log')),log_sha256=sha(p/(name+'.log')),exit_code=1,expected_failure='final mathematical False; no import/type/syntax failure'))
record=dict(namespace='FrameworkNonsphericalFlux',source=str(base/'formal/FullFlux.lean'),source_sha256=sha(p/'FullFlux.lean'),main_log=str(base/'formal/compile.log'),main_log_sha256=sha(p/'compile.log'),theorem_count=len(entries),entries=entries,model_status=status,checkpoint=pin['checkpoint'],imports=['Mathlib','Nonspherical (checked own source dependency)'],main_exit_code=0,own_source_dependency=dict(path=str(base/'formal/Nonspherical.lean'),sha256=dep['source_sha256'],original_checked_module='FrameworkNonspherical',reproduction='nonspherical_flux/formal/REPRODUCE.txt'),PINNED_INPUTS=dict(path=str(base/'formal/PINNED_INPUTS.json'),sha256=sha(p/'PINNED_INPUTS.json')),correspondence=dict(path=str(base/'formal/CORRESPONDENCE.txt'),sha256=sha(p/'CORRESPONDENCE.txt')),independent_review_status='ten theorem bodies independently reconstructed; final frozen metadata audit pending',historical_builds=[dict(accepted=False,source=str(base/'formal/build_history'/('attempt_'+n+'.source.txt')),log=str(base/'formal/build_history'/('attempt_'+n+'.log')),exit_code=1) for n in ['01','02']],prior_accepted_checkpoints=[dict(source=str(base/'formal/build_history'/('accepted_'+n+'.source.txt')),log=str(base/'formal/build_history'/('accepted_'+n+'.log')),exit_code=0,theorem_count=c,final=False) for n,c in [('eight',8),('nine',9)]],false_controls=controls,ambient_context='Real scalar coordinates; actual Euclidean sqrt(gx²+gy²+gz²), fixed a0 during differentiation, source M=G*m_b; exact complete source/hypotheses recorded.')
(p/'module_record.json').write_text(json.dumps(record,indent=2)+'\n')
lean=root/'fable_independent_2026/lean_2026'
(p/'REPRODUCE.txt').write_text('cd '+str(lean)+'\nlake env lean --root='+str(p)+' -o '+str(p/'build/Nonspherical.olean')+' '+str(p/'Nonspherical.lean')+'\n# Dependency expected exit0 with nine standard reports; source byte matches original checked FrameworkNonspherical.\nLEAN_PATH='+str(p/'build')+' lake env lean '+str(p/'FullFlux.lean')+'\n# Main expected exit0, ten standard axiom reports.\nLEAN_PATH='+str(p/'build')+' lake env lean '+str(p/'FalseKernelIncreasing.lean')+'\nLEAN_PATH='+str(p/'build')+' lake env lean '+str(p/'FalseActualTargetNonnegative.lean')+'\n# Both expected exit1 only mathematical False. No numeric computation rerun needed.\n# Source, statement, log, binary and input hashes in module_record and PINNED_INPUTS.\n')
assert len(entries)==10
for file,count in [('compile.log',10),('dependency_compile.log',9)]:
 log=(p/file).read_text();assert log.count('depends on axioms:')==count and 'error:' not in log and 'sorryAx' not in log and 'warning:' not in log
for c in controls:
 log=(root/c['log']).read_text();assert '⊢ False' in log and log.count('error:')==1
for x in items:assert sha(p/x['snapshot'])==x['sha256']
print(json.dumps({k:record[k] for k in ['source_sha256','main_log_sha256','theorem_count']}))
