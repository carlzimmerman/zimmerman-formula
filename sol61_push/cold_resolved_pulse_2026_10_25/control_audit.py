import hashlib,json,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];out=ROOT/sys.argv[1];rows=[]
for name in ['equivalence','free_control','partition_control','checkpoint_control','gauss_control','flux_control','poisson_control','memory_control','support_screen']:
 q=subprocess.run([sys.executable,str(P/(name+'.py'))],text=True,capture_output=True,check=True);d=json.loads(q.stdout);f=out/(name+'.json');f.write_text(q.stdout);rows.append(dict(control=name,status='completed assertions passed',output_sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
(out/'checks.json').write_text(json.dumps(dict(scope='finite deterministic/seeded controls only, not galaxy closure',controls=rows),indent=2)+'\n');print(len(rows),'finite controls passed')
