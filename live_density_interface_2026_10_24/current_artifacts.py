import argparse,json,runpy,shutil,hashlib
from pathlib import Path
import numpy as np
import torch
from stable_compatible import Stable
from joint import T

def checks():
    m=Stable(n=24,k=0,tau=0,beta=20,K=3);v=m.start(scale=8);v[m.n:]=np.linspace(.7,.2,m.n);E,g=m.direct(v);mass=v[:m.n];x=v[m.n:];q=np.sin(np.pi*x/2)**2;hp=np.pi/2*np.sin(np.pi*x)
    mut=g[:m.n]+(1-q)*g[m.n:]/(mass*hp);muf=g[:m.n]-q*g[m.n:]/(mass*hp);d=mass*np.cos(np.arange(m.n));d-=sum(d)/m.n;d*=1e-4;eps=1e-5;out={}
    for name,mu in [('T',mut),('F',muf)]:
        es=[]
        for sign in [1,-1]:
            mm=mass+sign*eps*d;tt=mass*q+(sign*eps*d if name=='T' else 0);xx=2/np.pi*np.arcsin(np.sqrt(tt/mm));es.append(m.direct(np.r_[mm,xx])[0])
        er=abs((es[0]-es[1])/(2*eps)-mu@d)/max(abs(mu@d),1);out[name+'_mass_transfer_error']=er;assert er<1e-7
    z=T(np.log(mass));zero=torch.zeros(m.n,requires_grad=True);H=torch.autograd.functional.hessian(lambda x:m.energy(z,x),zero).detach().numpy();hf=2.5*m.K*(mass/m.vol.numpy())**(2/3);target=-np.pi**2/2*np.diag(mass*hf)
    er=np.linalg.norm(H-target)/np.linalg.norm(target);out['all_F_seed_Hessian_relative_error']=float(er);assert er<1e-10
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();p=Path(__file__).parent;dest=Path(a.output)
    result=dict(checks=checks(),source_hashes={},states=[])
    for name in ['run_stable/results.json','run_stable_recovery/results.json']:result['source_hashes'][name]=hashlib.sha256((p/name).read_bytes()).hexdigest()
    data=json.loads((p/'run_stable_recovery/results.json').read_text())
    for kind,rows in data.items():
        for r in rows:result['states'].append(dict(kind=kind,**{k:r[k] for k in ['interpolated_crossings_kpc','displacement_kpc','front_change_kpc','energy_difference','law_windows_dex','density_KKT_max','qouter'] if k in r}))
    (p/'current_assessment.json').write_text(json.dumps(result,indent=2)+'\n')
    runpy.run_path(str(p/'plot_current.py'))
    for name in ['current_assessment.json','current_result.png']:shutil.copy2(p/name,dest.parent/name)
    dest.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
