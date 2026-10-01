"""Sequential reproductions in a repo-layout mirror; writes confined to this lane."""
import os,sys,pathlib,shutil,json,subprocess,time,hashlib,datetime,platform
ROOT=pathlib.Path(__file__).resolve().parents[3]
HERE=pathlib.Path(__file__).resolve().parent
MIRROR=HERE/'mirror'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
MIRROR.mkdir(exist_ok=True)
for p in ROOT.iterdir():
    q=MIRROR/p.name
    if p.name=='campaign_fresh_gravity': continue
    if not q.exists(): q.symlink_to(p,target_is_directory=p.is_dir())
LANE=MIRROR/'campaign_fresh_gravity'; LANE.mkdir(exist_ok=True)
for p in (ROOT/'campaign_fresh_gravity').iterdir():
    q=LANE/p.name
    owned=p.name.startswith(('CFG2_','CFG3_','CFG5_'))
    if owned and p.suffix=='.py': shutil.copy2(p,q)
    elif not owned and not q.exists(): q.symlink_to(p)
SOURCES={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'campaign_fresh_gravity').glob('CFG[235]*') if p.is_file()}
(HERE/'source_inventory.json').write_text(json.dumps({'base':'48905ae11213afcb9ff1b7726530bb5dd1933fe3','sources':SOURCES},indent=2))
scripts=sys.argv[1:] or ['CFG2_A_principle','CFG2_B_galaxies','CFG3_principle','CFG3_sparc','CFG3_solar_system','CFG3_kids','CFG3_web_lensing','CFG5_1_principle','CFG5_2_collapse','CFG5_3_sparc']
for slug in scripts:
    for mut in (1,0):
        name=slug+('_MUTATE' if mut else '')
        meta=HERE/'runs'/name; meta.mkdir(parents=True,exist_ok=True)
        env=dict(os.environ,MUTATE=str(mut),PYTHONDONTWRITEBYTECODE='1')
        for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS']: env[k]='1'
        argv=[sys.executable,str(HERE/'record_child.py'),str(LANE/(slug+'.py')),str(meta/'reads.json')]
        t=time.monotonic(); started=datetime.datetime.now(datetime.timezone.utc).isoformat()
        print('START',name,started,flush=True)
        with (meta/'stdout.txt').open('w') as out,(meta/'stderr.txt').open('w') as err:
            try: rc=subprocess.run(argv,cwd=MIRROR,env=env,stdout=out,stderr=err,timeout=900).returncode
            except subprocess.TimeoutExpired: rc=124
        result=LANE/(slug+'_results'+('_MUTATE' if mut else '')+'.json')
        output={str(p.relative_to(HERE)):sha(p) for p in [meta/'stdout.txt',meta/'stderr.txt',result] if p.exists()}
        j={'argv':argv,'started':started,'runtime':time.monotonic()-t,'exit_status':rc,'mutation':bool(mut),'result_exists':result.exists(),'outputs':output,'source_inventory':'source_inventory.json','python':sys.version,'machine':platform.platform(),'thread_cap':'cooperative 1; source harness may override to 2','timeout':900}
        if result.exists():j['scientific_summary']=json.loads(result.read_text()).get('summary')
        (meta/'execution.json').write_text(json.dumps(j,indent=2))
        print('END',name,'rc',rc,'runtime',round(j['runtime'],2),'results',j['result_exists'],flush=True)
