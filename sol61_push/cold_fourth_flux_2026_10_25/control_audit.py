import json,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;out={}
for name in ['benchmark','free_control_v2','finite_control']:
 q=subprocess.run([sys.executable,str(P/(name+'.py'))],check=True,text=True,capture_output=True);out[name]=json.loads(q.stdout)
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print('3 independent bounded controls passed')
