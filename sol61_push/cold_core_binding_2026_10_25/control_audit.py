import hashlib,json,pathlib,subprocess,sys
Q=pathlib.Path(__file__).resolve().parent;ROOT=Q.parents[1];out=ROOT/sys.argv[1];rows=[]
for name in ['controls','phase_controls','phase_random_control','assembly_controls','assembly_cross_control']:
 q=subprocess.run([sys.executable,str(Q/(name+'.py'))],text=True,capture_output=True,check=True);json.loads(q.stdout);f=out/(name+'.json');f.write_text(q.stdout);rows.append(dict(control=name,status='completed assertions passed',sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
(out/'checks.json').write_text(json.dumps(dict(scope='five finite control programs only, not astronomical closure',controls=rows),indent=2)+'\n');print('5 control programs passed')
