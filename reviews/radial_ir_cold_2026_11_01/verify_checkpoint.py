"""TP04 current-input provenance and interpretation guards, no science reruns."""
import ast,datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def validate(p):
    r=subprocess.run([sys.executable,str(VALIDATOR),str(p),'--root',str(ROOT)],capture_output=True,text=True)
    return r.returncode,(r.stdout+r.stderr).strip()


def main():
    hashes={}
    for p in HERE.rglob('*'):
        if p.is_file():hashes.setdefault(sha(p),[]).append(p)
    records=[];completed=failed=0
    for p in sorted(HERE.rglob('manifest.json')):
        m=json.loads(p.read_text());status=m['run']['status'];code,output=validate(p);archived=[]
        for a in m['input_artifacts']:
            original=ROOT/a['path']
            if original.exists() and sha(original)==a['sha256']:continue
            assert status=='failed' and a['sha256'] in hashes,(p,a)
            archived.append(dict(original_path=a['path'],identical_historical_bytes=str(hashes[a['sha256']][0].relative_to(ROOT))))
        for a in m['outputs']:assert sha(ROOT/a['path'])==a['sha256'],(p,a)
        if status=='completed':
            assert code==0,(p,output)
            rp=p.parent/'result.json'
            if rp.exists():
                r=json.loads(rp.read_text())
                assert all(v for v in r.get('checks',{}).values() if isinstance(v,bool)),(p,r.get('checks'))
            completed+=1
        else:
            assert status=='failed',status;failed+=1
        records.append(dict(path=str(p.relative_to(HERE)),sha256=sha(p),status=status,current_hash_validation_exit=code,validator_output=output,historical_inputs=archived))
    assert completed>=16 and failed==3,(completed,failed)
    prior=[]
    for dirname,expected in [('quantum_matching_2026_11_01',15),('finite_matching_2026_11_01',10)]:
        base=ROOT/'reviews'/dirname;count=0
        for p in sorted(base.rglob('manifest.json')):
            m=json.loads(p.read_text())
            if m['run']['status']!='completed':continue
            code,output=validate(p);assert code==0,(p,output);count+=1
        assert count==expected,(dirname,count)
        old=json.loads((base/'VERIFICATION.json').read_text())
        for a in old['review_pins']:assert sha(base/a['path'])==a['sha256'],a
        prior.append(dict(checkpoint=dirname,completed_current_manifests=count,verification_sha256=sha(base/'VERIFICATION.json')))
    old=ROOT/'reviews/three_priorities_2026_11_01'
    for a in json.loads((old/'INPUT_SNAPSHOT.json').read_text())['inputs']:
        assert sha(ROOT/a['snapshot'])==a['sha256']
        if not a['path'].startswith('covariant_push_'):assert sha(ROOT/a['path'])==a['sha256'],a
    for a in json.loads((old/'law_dictionary/EDIT_RECORD.json').read_text())['files']:
        assert sha(ROOT/a['path'])==a['after_sha256'],a
    for a in json.loads((old/'VERIFICATION.json').read_text())['review_pins']:
        assert sha(old/a['path'])==a['sha256'],a
    # Inventory records may deliberately cover only a frozen subroute; later
    # addenda are pinned by this coordinator record rather than appended to them.
    inventory_count=0
    for p in HERE.rglob('ARTIFACTS.sha256'):
        for line in p.read_text().splitlines():
            if not line.strip():continue
            h,rel=line.split(None,1);target=ROOT/rel.strip()
            assert sha(target)==h,(p,rel);inventory_count+=1
    syntax=0
    for p in HERE.rglob('*.py'):ast.parse(p.read_text(),filename=str(p));syntax+=1
    loss=json.loads((HERE/'run_loss_v2/result.json').read_text());assert loss['all_checks_pass']
    assert float(loss['bounds']['lifetime_lower_s'])>1e20
    assert float(loss['bounds']['survival_lower_over_13p8Gyr'])>.99
    assert loss['cold_distribution']['m_GeV']==.001 and loss['cold_distribution']['e']==.003
    assert loss['cold_distribution']['relic_dynamics']['free_streaming_Mpc']<.001
    units=json.loads((HERE/'run_units/result.json').read_text());assert units['all_checks_pass']
    assert all(x['DE_fixed_radial_amplitude']>1 for x in units['radial_necessary_windows'])
    assert all(x['growth_over_H0']>1e15 for x in units['phase_helicity_growth'])
    links=0
    for p in HERE.rglob('*.md'):
        prose=re.sub(r'```[\s\S]*?```','',p.read_text())
        prose='\n'.join(l for l in prose.splitlines() if not l.startswith(('    ','\t')))
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',prose):
            if target.startswith(('http:','https:','#')):continue
            dest=(p.parent/target.split('#')[0]).resolve()
            assert dest.exists() or dest==HERE/'VERIFICATION.json',(p,target)
            links+=1
    reviews=[p for p in HERE.rglob('*.md') if 'inputs_historical' not in p.parts]
    data=dict(checkpoint='TP04',verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),base_head='27a0d27db1c343e1752698da36aa300398214689',
              assessment_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
              completed_v2_records=completed,preserved_failed_v2_records=failed,records=records,prior_checkpoints=prior,
              TP01_sources_reviews_and_law_corrections_unchanged=True,subroute_inventory_hashes_checked=inventory_count,python_sources_parsed=syntax,local_links_checked=links,
              review_pins=[dict(path=str(p.relative_to(HERE)),sha256=sha(p)) for p in sorted(reviews)],
              artifact_pins=[dict(path=str(p.relative_to(HERE)),sha256=sha(p)) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'VERIFICATION.json'],
              validator_sha256=sha(VALIDATOR),
              interpretation_guards=dict(cold_point_is_conditional=True,leading_loss_is_not_all_orders_total=True,FD_initial_state_not_production=True,raw_DE_vacuum_variant_distinct=True,helicity_growth_not_fractional_lifetime=True),
              scoped_supersessions=[dict(original='cold_states/run_001',preferred='cold_states/run_002',reason='Physical charged-gap diagnostic excludes gauge Goldstones; other tree decay evidence retained'),
                                   dict(original='cold_states/run_four_fermion',preferred='cold_states/run_four_fermion_v2',reason='Amplitude-safe interference and actual benchmark slope checks'),
                                   dict(original='run_loss',preferred='run_loss_v2',reason='Explicit amplitude-safe decay/collision composition and final collision classes'),
                                   dict(original='radial/run_floquet weak-crossing diagnostic',preferred='radial/run_floquet_endpoints',reason='Longer formation-length endpoints before weak-asymptotic occupation claim')],
              no_Git_queue_or_prior_science_mutation_by_TP04=True,no_production_or_external_job_started=True)
    (HERE/'VERIFICATION.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:data[k] for k in ['completed_v2_records','preserved_failed_v2_records','subroute_inventory_hashes_checked','python_sources_parsed','local_links_checked']},indent=2))

if __name__=='__main__':main()
