"""Honest legacy-v1 captures: fresh tiny controls, retrospective bounded benchmarks."""
from pathlib import Path
import sys,subprocess,os,time,json,datetime,hashlib,platform
P=Path(__file__).resolve().parent;repo=P.parents[3];turn=P.parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def record(folder,kind,mut=False):
    here=turn/folder
    if kind=='controls':
        script='control.py' if folder=='kick_moments' else 'controls.py';stem='control' if folder=='kick_moments' else 'controls';out=here/(stem+('_mutation' if mut else '_main')+'.json')
        env=os.environ.copy();env['PYTHONPATH']=str(turn/'kick_moments');env['PYTHONDONTWRITEBYTECODE']='1'
        if mut:env['MUTATE']='1'
        else:env.pop('MUTATE',None)
        started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
        done=subprocess.run([sys.executable,str(here/script)],env=env,capture_output=True,text=True);runtime=time.monotonic()-t;code=done.returncode
        label='controls_mutation' if mut else 'controls_main';(here/(label+'.stdout.txt')).write_text(done.stdout);(here/(label+'.stderr.txt')).write_text(done.stderr)
        j=json.loads(out.read_text());checks=[dict(name=k,passed=v) for k,v in j['checks'].items()];art=[out,here/(label+'.stdout.txt'),here/(label+'.stderr.txt')]
        limits={'angular_quadrature':'32x64 for exact-kick controls','event_examples':'turnaround .37, pressure .63; harmonic20/40/80 steps','timeout':'tiny deterministic run, no enforced subprocess timeout'};risks=['Legacyv1 capture does not enforce resources','Controls establish only their explicit finite/model scope'];command=[sys.executable,str((here/script).relative_to(repo))]
    else:
        label='benchmark';out=here/'results.json';j=json.loads(out.read_text());runtime=j['runtime_seconds'];code=0;started=datetime.datetime.fromtimestamp(out.stat().st_mtime-runtime,datetime.timezone.utc).isoformat();art=[out,here/'benchmark.out',here/'benchmark.err',here/'comparisons.json']
        checks=[dict(name='all requested bounded runs completed',passed=len(j['runs'])==(28 if folder=='kick_moments' else 12))]
        if folder=='event_integrator':checks += [dict(name=k,passed=v) for k,v in json.loads((here/'comparisons.json').read_text())['checks'].items()]
        limits={'runs':len(j['runs']),'N':[600,1000,2000] if folder=='kick_moments' else[80,600,1000],'eta':[.03,.015],'sequential':True,'aggregate_guard_seconds':480 if folder=='kick_moments' else 320,'per_run_guard_seconds':None if folder=='kick_moments' else 48,'event_maxsteps':None if folder=='kick_moments' else 100000,'scope':'no cooling, constant spin.25, M0=1e12, botha0footings'}
        risks=['Legacyv1 retrospective capture; started_at estimated as result file mtime minus recordedruntime, not an original process timestamp','No resource enforcement is supplied by this manifest; explicit cooperative guards are in benchmark.py and eventengine','No continuum convergence, causal action or stability from exit0'];command=[sys.executable,str((here/'benchmark.py').relative_to(repo))];script='benchmark.py'
    inputs=[here/script,here/('exact_moments.py' if folder=='kick_moments' else'event_step.py')]
    if kind=='benchmark':inputs+=[here/('engine_exact.py' if folder=='kick_moments' else'engine_events.py'),turn/'kick_moments/exact_moments.py',turn.parent/'collapse/mirror/campaign_fresh_gravity/CFG5_common.py']
    manifest={'schema_version':1,'claim_id':folder+'/'+label,'repository':{'commit':'48905ae11213afcb9ff1b7726530bb5dd1933fe3','dirty':True},'command':command,'environment':{'software':[sys.version,'numpy1.26.2','CLASS3.3.4.0 for benchmark, local build'],'hardware':platform.platform()},'mathematics':{'assertion_tested':'Exact isotropic kick integral controls or bounded event-localized shell numerical audit; failures retained','coefficient_domain':'float64','conventions':'source units kpc,km/s; kappa1/2 fitted; no-cooling constant spin benchmark','inputs':[str(f.relative_to(repo)) for f in inputs],'input_sha256':{str(f.relative_to(repo)):sha(f) for f in inputs},'bounds':limits,'non_claims':['No full-action completion','No numerical convergence claim from boundedgrid']},'randomness':{'used':False,'generator':'none; inherited RNG initialization has no draws','seed':None},'run':{'started_at':started,'runtime_seconds':runtime,'exit_status':code},'outputs':[{'path':str(f.relative_to(repo)),'sha256':sha(f)} for f in art],'checks':checks,'result':('Mutation failed named event/moment checks' if mut else 'Bounded outputs recorded; scientific failures and scope retained'),'residual_risks':risks}
    target=here/(label+'_manifest.json');target.write_text(json.dumps(manifest,indent=2)+'\n');print(target.relative_to(repo))
for folder in ['kick_moments','event_integrator']:
 for mut in [False,True]:record(folder,'controls',mut)
 record(folder,'benchmark')
