"""Convert observed producer records to v2 evidence; preserve missing observations explicitly."""
import pathlib,json,hashlib,datetime,subprocess
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];D=P/'run_manifests';D.mkdir(exist_ok=True);records=[];missing=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in sorted((P/'runs').glob('*.json')):
 q=json.loads(f.read_text())
 if 'parameters' not in q:continue
 a=q['parameters'];tag=a['tag']
 if 'started_utc' not in q:missing.append(dict(tag=tag,missing=['UTC start','producer software versions'],scope='untimed first preflight retained; do not invent a v2 execution record'));continue
 before=q['source_hashes_before'];after=q['source_hashes_after'];assert before==after
 for path,h in before.items():assert sha(ROOT/path)==h
 script=next(iter(before));cmd=['python3',script,'--galaxy',a['galaxy'],'--tag',tag]
 if a.get('initial_from'):cmd+=['--initial-from',a['initial_from']]
 if a.get('resume'):cmd+=['--resume',a['resume']]
 cmd+=['--nr',str(a['nr']),'--lmax',str(a['lmax']),'--mmax',str(a['mmax']),'--T',str(int(a['T']))]
 if 'preflight' not in tag:
  cmd+=['--dt','.02' if 'material' in tag else '.01']
  if 'material' in tag:cmd+=['--gas','none','--substeps',str(a['substeps'])]
  else:cmd+=['--wall-seconds','600']
 outputs=[f,P/'runs'/f'{tag}_fields.npz']
 if 'material' in tag:outputs.extend([P/'runs'/f'{tag}_labels.json',P/'runs'/f'{tag}_labels.npz'])
 output_names=[str(z.relative_to(ROOT)) for z in outputs];h=q['history'][-1];manifest=dict(schema_version=2,claim_id='CCT011_'+tag,repository=dict(commit=q['revision'],dirty=True),command=cmd,environment=dict(software=[dict(name=k,version=v) for k,v in q['software'].items()],hardware='not recorded by producer; local host is described by the final audit'),mathematics=dict(assertion_tested='Execute the saved finite assembly or passive material-current diagnostic; record termination and numerical gates, not a physical four-dwarf pass',coefficient_domain='complex128 and float64',conventions='CCT011 CONTRACT and MATERIAL_PROTOCOL; one cold Poisson source; tags never source gravity',inputs=['Pinned source/data files and exact saved parents'],bounds=a,non_claims=['No completed physical formation from a stopped pilot','No validated material survival from current labels','No complete action/cosmology or v3 bridge']),randomness=dict(used='material' in tag,generator='NumPy PCG64 (mass labels11011; stars1010)' if 'material' in tag else '',seed=11011 if 'material' in tag else None),run=dict(started_at=q['started_utc'],runtime_seconds=q['seconds'],exit_status=0,status='completed',resource_limits=dict(memory_bytes=None,cpu_seconds=None,max_cores=None,max_threads=1)),outputs=[dict(path=str(z.relative_to(ROOT)),sha256=sha(z),kind='result') for z in outputs],checks=[dict(name='producer before/after pins',status='passed'),dict(name='scientific producer termination',status=q['status'])],result=q['status']+'; this is process execution status, not theory or four-dwarf closure',residual_risks=['UTC start is the producer module timestamp; runtime_seconds is the producer internal timed interval, not a full-process wall measurement','Git revision was sampled at output creation, not necessarily start','Original argv reconstructed from the commands actually issued in this session; producer stored parsed parameters, not argv','Output hashes recorded during this reconciliation; raw before/after source hashes were observed by producer','Threads requested through BLAS/OMP environment; no external hard memory/CPU cap was enforced; RSS is sampled before terminal serialization','Material labels omit the finite local angular-projection source; assembly pilots stop unresolved; review RESULT'],input_artifacts=[dict(path=k,sha256=v,sha256_after=after[k]) for k,v in before.items()],declared_results=output_names,recording=dict(recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),builder_sha256=sha(pathlib.Path(__file__))))
 dest=D/(tag+'.json');dest.write_text(json.dumps(manifest,indent=2)+'\n');records.append(str(dest.relative_to(ROOT)))
(P/'run_record_index.json').write_text(json.dumps(dict(recorded_manifests=records,missing_observations=missing),indent=2)+'\n');print(len(records),'typed records; omitted',missing)
