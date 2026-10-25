import pathlib,sys,subprocess,json,numpy as np
P=pathlib.Path(__file__).resolve().parent;L=P.parent/'cold_lens_phase_2026_10_25';out=pathlib.Path(sys.argv[1]);commands=[]
def compare(a,b):
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:compare(a[k],b[k])
 elif isinstance(a,list):
  assert len(a)==len(b)
  for x,y in zip(a,b):compare(x,y)
 elif isinstance(a,(str,bool)):assert a==b
 else:np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-13)
for script,target,reference in [(L/'benchmark_v2.py','lens_benchmark.json',L/'benchmark_refined.json'),(P/'benchmark_v2.py','adaptive_benchmark.json',P/'benchmark_refined.json'),(P/'conservation_v2.py','conservation.json',P/'conservation_verified.json')]:
 cmd=[sys.executable,str(script),str(out/target)];commands.append(cmd);r=subprocess.run(cmd,capture_output=True,text=True)
 assert r.returncode==0,(r.stdout,r.stderr)
 compare(json.loads((out/target).read_text()),json.loads(reference.read_text()))
cmd=[sys.executable,str(P/'audit.py'),str(out/'result.json')];commands.append(cmd);subprocess.run(cmd,check=True)
(out/'child_commands.json').write_text(json.dumps(commands,indent=2)+'\n')
