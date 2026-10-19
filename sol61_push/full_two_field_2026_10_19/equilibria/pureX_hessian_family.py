"""Adapt one independently solved pure-X profile; four fixed full-ADM Hessians."""
import argparse,json,math,subprocess,sys
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--outdir',required=True);a=p.parse_args();c=json.loads(Path(a.contract).read_text());out=Path(a.outdir);d=np.load(c['source_profile'])
r=d['r'];mu=d['mass_G'];N=np.ones_like(r);N[1:]=1-2*mu[1:]/r[1:];G=1/(4*math.pi);M=1.;u=.02;m=M/(2*math.sqrt(1+u*u));lam=.01;Delta=M*M-4*m*m;g=math.sqrt(Delta*lam/3);w=float(d['omega_X'])/2
np.savez(out/'pureX_adapted.npz',r=r,f=np.zeros_like(r),fp=np.zeros_like(r),h=d['h'],hp=d['hp'],alpha=np.exp(d['logalpha']),a=1/np.sqrt(N),G=G,m=m,M=M,g=g,lambda_total=lam,omega=w)
records=[]
for case in c['cases']:
 name=case['name'];res=out/(name+'.json');argv=[sys.executable,str(Path(__file__).parent/'hessian_frozen.py'),'--profile',str(out/'pureX_adapted.npz'),'--R',str(case['R']),'--dx',str(case['dx']),'--basis',str(case['B']),'--result',str(res)]
 q=subprocess.run(argv,capture_output=True,text=True,timeout=30);(out/(name+'_solver.txt')).write_text(q.stdout+'\nSTDERR\n'+q.stderr)
 if q.returncode:raise RuntimeError((q.returncode,q.stdout,q.stderr))
 records.append(json.loads(res.read_text()))
(out/'results.json').write_text(json.dumps(dict(status='completed',parameters=dict(G=G,m=m,M=M,g=g,lambda_total=lam,lambda_rep=2*lam/3,omega=w),cases=c['cases'],records=records,non_claims=c['mathematics']['non_claims']),indent=2)+'\n')
print('Completed',len(records),'pure-X finite-Galerkin full-ADM Hessians.')
