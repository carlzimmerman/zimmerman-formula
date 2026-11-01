"""TP03 provenance checks and explicit pressure interpretation guards."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def validate(path):
    p=subprocess.run([sys.executable,str(VALIDATOR),str(path),'--root',str(ROOT)],capture_output=True,text=True)
    return p.returncode,(p.stdout+p.stderr).strip()


def main():
    archive={digest(p):str(p.relative_to(ROOT)) for p in (HERE/'two_loop/inputs_initial').rglob('*') if p.is_file()}
    records=[];completed=0;failed=0
    for p in sorted(HERE.rglob('manifest.json')):
        m=json.loads(p.read_text());status=m['run']['status'];code,output=validate(p)
        changed=[]
        for a in m['input_artifacts']:
            current=ROOT/a['path']
            if current.is_file() and digest(current)==a['sha256']:continue
            assert status=='failed' and a['sha256'] in archive,(p,a)
            changed.append(dict(original_path=a['path'],archived_identical_bytes=archive[a['sha256']]))
        for a in m['outputs']:
            assert digest(ROOT/a['path'])==a['sha256'],(p,a)
        if status=='completed':
            assert code==0,(p,output)
            result=p.parent/'result.json'
            if result.exists():
                rr=json.loads(result.read_text());checks=rr.get('checks',{})
                assert all(v for v in checks.values() if isinstance(v,bool)),(p,checks)
            completed+=1
        else:
            assert status=='failed',status
            assert str(p.relative_to(HERE)) in ['two_loop/run_builder/manifest.json','run_current_pullback/manifest.json']
            failed+=1
        records.append(dict(path=str(p.relative_to(HERE)),sha256=digest(p),status=status,current_hash_validation_exit=code,validator_output=output,archived_inputs=changed))
    assert completed>=9 and failed==2,(completed,failed)
    old=ROOT/'reviews/quantum_matching_2026_11_01';oldrecords=[]
    for p in sorted(old.rglob('manifest.json')):
        code,output=validate(p);assert code==0,(p,output)
        oldrecords.append(str(p.relative_to(ROOT)))
    assert len(oldrecords)==15
    oldverification=json.loads((old/'VERIFICATION.json').read_text())
    for a in oldverification['review_pins']:
        assert digest(old/a['path'])==a['sha256'],a
    previous=ROOT/'reviews/three_priorities_2026_11_01'
    snap=json.loads((previous/'INPUT_SNAPSHOT.json').read_text())
    for a in snap['inputs']:
        assert digest(ROOT/a['snapshot'])==a['sha256']
        if not a['path'].startswith('covariant_push_'):
            assert digest(ROOT/a['path'])==a['sha256'],a
    edits=json.loads((previous/'law_dictionary/EDIT_RECORD.json').read_text())['files']
    for a in edits:assert digest(ROOT/a['path'])==a['after_sha256'],a
    for a in json.loads((previous/'VERIFICATION.json').read_text())['review_pins']:
        assert digest(previous/a['path'])==a['sha256'],a

    r=json.loads((HERE/'run_pressure/result.json').read_text())
    assert r['all_checks_pass'] and len(r['cases'])==48
    selected=[]
    for c in r['cases']:
        assert c['boundary']['w_ex']>.5
        assert c['samples'][2]['X_over_min']==1.2 and c['samples'][2]['cs2_IR']>0
        assert c['samples'][3]['X_over_min']==1.3 and c['samples'][3]['cs2_IR']<0
        if c['scheme']=='finite_matched' and c['interpolation_nodes']==29 and c['stencil_h']==.0025:
            selected.append({k:c[k] for k in ['e','boundary_ratio','X_min_over_one_loop','boundary']})
    assert len(selected)==2
    links=0
    for p in HERE.rglob('*.md'):
        prose=re.sub(r'```[\s\S]*?```','',p.read_text())
        prose='\n'.join(s for s in prose.splitlines() if not s.startswith(('    ','\t')))
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',prose):
            if target.startswith(('http:','https:','#')):continue
            local=(p.parent/target.split('#')[0]).resolve()
            assert local.exists() or local==HERE/'VERIFICATION.json',(p,target)
            links+=1
    reviews=[p for p in HERE.rglob('*.md') if 'inputs_initial' not in p.parts]
    out=dict(checkpoint='TP03',verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             base_head='7b1880de2caded85da4b8c34d84b5dc6c005650e',assessment_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
             completed_v2_records=completed,preserved_failed_v2_records=failed,records=records,
             previous_TP02_completed_manifests_revalidated=len(oldrecords),previous_TP01_sources_reviews_and_law_corrections_preserved=True,
             pressure_cases=48,selected_finite_matched_cases=selected,native_1p2_positive_1p3_negative_guard=True,
             local_links_checked=links,review_pins=[dict(path=str(p.relative_to(HERE)),sha256=digest(p)) for p in sorted(reviews)],
             scope='Finite vacuum and local angular-current matching at the stated fixed weak trial inputs; not full radial, higher-derivative, state/lifetime, nonperturbative IR or gravity completion.',
             no_Git_or_queue_mutation_by_TP03=True,no_production_or_external_job_started=True)
    (HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['completed_v2_records','preserved_failed_v2_records','previous_TP02_completed_manifests_revalidated','pressure_cases','local_links_checked']},indent=2))

if __name__=='__main__':main()
