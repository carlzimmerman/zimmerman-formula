"""Reconcile accepted computation/compiler records and target versions.

Does not rerun the science jobs or turn execution success into a physics proof.
"""
import datetime,hashlib,json,pathlib,re,subprocess
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[1]
ALLOWED={'propext','Classical.choice','Quot.sound'}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
records=[]
for name in ['newton_normalization','filtered_zero_field','spectral_lapse']:
    records.append(json.loads((BASE/name/'lean_attempt1_record.json').read_text()))
for name in ['lean_record.json','clock_lean_record.json']:
    d=json.loads((BASE/'ic27_bridge'/name).read_text())
    records.append(dict(file=d['source'],sha256=d['source_sha256'],command=d['command'],
                        cwd=d['cwd'],exit_code=d['exit_code'],log=d['log'],log_sha256=d['log_sha256']))
d=json.loads((BASE/'lapse_kinetic/run_lean_001/results.json').read_text())
assert d['passed']
records.append(dict(file=d['source'],sha256=d['source_sha256'],command=d['child_command'],
                    cwd=str(ROOT/'fable_independent_2026/lean_2026'),exit_code=d['returncode'],
                    log=str((BASE/'lapse_kinetic/run_lean_001/stdout.txt').relative_to(ROOT))))
count=0
for record in records:
    assert record['exit_code']==0
    src=ROOT/record['file'];log=ROOT/record['log']
    assert digest(src)==record['sha256'],('source drift',src)
    if 'log_sha256' in record:assert digest(log)==record['log_sha256'],('log drift',log)
    st=src.read_text();lt=log.read_text()
    assert 'error:' not in lt and 'sorryAx' not in lt
    ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",lt)
    printed=re.findall(r'^#print axioms ([A-Za-z0-9_.]+)',st,flags=re.M)
    assert {n.rsplit('.',1)[-1]for n,_ in ax}=={n.rsplit('.',1)[-1]for n in printed}
    assert len(ax)==len(printed)>0
    stripped=re.sub(r'/-.*?-/', '',st,flags=re.S)
    stripped=re.sub(r'--[^\n]*','',stripped)
    assert not re.search(r'\b(sorry|admit)\b|^\s*axiom\s',stripped,flags=re.M)
    record['axioms']={n:[v.strip()for v in vals.split(',')if v.strip()]for n,vals in ax}
    assert all(set(v)<=ALLOWED for v in record['axioms'].values())
    record['log_sha256']=digest(log);count+=len(ax)
versions=json.loads((BASE/'target_versions.json').read_text())
assert digest(BASE/'snapshots/FRIED_CHICKEN_SPEC.start.md')==versions['start_spec_sha256']
assert digest(BASE/'snapshots/FRIED_CHICKEN_SPEC.9092fc0fd.md')==versions['amended_spec_sha256']
spec=ROOT/'qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md'
assert digest(spec)==versions['amended_spec_sha256'], 'Further target change needs explicit reconciliation'
manifest={'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'scope':'Recorded compiler evidence, unchanged hashes and allowed axioms; no full gravity certificate',
          'theorem_count':count,'certificates':records,'target_versions':versions,
          'lean_version':subprocess.check_output(['/opt/homebrew/bin/lean','--version'],text=True).strip(),
          'mathlib_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT/'fable_independent_2026/lean_2026/.lake/packages/mathlib',text=True).strip(),
          'repository_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}
(BASE/'lean_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
runs=['newton_normalization/run2','lapse_kinetic/run_lapse_004','lapse_kinetic/run_ppn_gyro_001',
      'lapse_kinetic/run_integrated_001','lapse_kinetic/run_offshell_001','lapse_kinetic/run_lean_001',
      'lapse_kinetic/run_spectral_reduction_002',
      'covariant_clock/run1','covariant_clock/interface_run1','ic27_bridge/run_002',
      'filtered_zero_field/run1','spectral_lapse/run1']
validator=pathlib.Path.home()/'.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py'
checks=[]
for run in runs:
    p=BASE/run/'manifest.json'
    r=subprocess.run(['python3',str(validator),str(p),'--root',str(ROOT)],capture_output=True,text=True)
    checks.append({'manifest':str(p.relative_to(ROOT)),'manifest_sha256':digest(p),
                   'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
(BASE/'computation_validation.json').write_text(json.dumps(checks,indent=2)+'\n')
assert all(x['exit_code']==0 for x in checks),checks
print(json.dumps({'Lean_files':len(records),'Lean_theorems':count,'accepted_manifests':len(checks),
                  'target_revision_reconciled':True,'full_theory':'OPEN'}))
