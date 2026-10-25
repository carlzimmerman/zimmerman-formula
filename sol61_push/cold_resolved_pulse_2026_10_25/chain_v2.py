"""Sequential same-resolution checkpoint segments; never resume an accuracy failure."""
import argparse,datetime,json,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--galaxy',default='draco');p.add_argument('--ne',type=int,default=256);p.add_argument('--nt',type=int,default=40);p.add_argument('--nf',type=int,default=64);p.add_argument('--dt',type=float,default=.02);p.add_argument('--T',type=float,default=20);p.add_argument('--wall',type=float,default=240);p.add_argument('--prefix',default='draco_joint');a=p.parse_args();previous=None;last=0;rows=[]
for i in range(1,9):
 tag=a.prefix+'_s%02d'%i;cmd=[sys.executable,str(P/'evolve_v2.py'),'--galaxy',a.galaxy,'--ne',str(a.ne),'--nt',str(a.nt),'--nf',str(a.nf),'--dt',str(a.dt),'--T',str(a.T),'--wall',str(a.wall),'--tag',tag]
 if previous:cmd+=['--resume',previous]
 print(datetime.datetime.now(datetime.timezone.utc).isoformat(),'start',tag,flush=True)
 (P/'runs').mkdir(exist_ok=True)
 with (P/'runs'/(tag+'.stdout')).open('w') as log:q=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 if q.returncode:print('producer failed',q.returncode,flush=True);raise SystemExit(q.returncode)
 d=json.loads((P/'runs'/(tag+'.json')).read_text());t=d['history'][-1]['t'];rows.append(dict(tag=tag,T=t,status=d['status'],peak_RSS_bytes=d['peak_RSS_bytes']));(P/(a.prefix+'_chain.json')).write_text(json.dumps(dict(parameters=vars(a),segments=rows),indent=2)+'\n');print(rows[-1],flush=True)
 if t<=last or d['status'] not in ['stopped soft wall budget','stopped memory headroom'] or t>=a.T:break
 previous=tag;last=t

state='target reached' if rows and rows[-1]['T']>=a.T and rows[-1]['status']=='finished requested finite interval' else ('incomplete resource limit' if rows and rows[-1]['status'] in ['stopped soft wall budget','stopped memory headroom'] else 'stopped accuracy/error')
(P/(a.prefix+'_chain_verdict.json')).write_text(json.dumps(dict(state=state,parameters=vars(a),segments=rows),indent=2)+'\n');print(state,flush=True)
if state!='target reached':raise SystemExit(2)
