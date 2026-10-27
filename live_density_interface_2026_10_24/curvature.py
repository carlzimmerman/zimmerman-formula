"""LD-9: joint variational checks and density-relaxed local wall curvature."""
import argparse,json
from pathlib import Path
import numpy as np
import torch
from scipy.linalg import null_space,eigvalsh
from joint import T
from warm import Warm

def checks():
    m=Warm(n=24,k=120,tau=1,K=3);v=m.start(scale=4);v[m.n:]=np.linspace(.7,.2,m.n);v[:m.n]=np.maximum(v[:m.n],1e-4);v[:m.n]*=5.364/sum(v[:m.n])
    E,g=m.direct(v);mass=v[:m.n];x=v[m.n:];q=np.sin(np.pi*x/2)**2;hp=np.pi/2*np.sin(np.pi*x);mut=g[:m.n]+(1-q)*g[m.n:]/(mass*hp);muf=g[:m.n]-q*g[m.n:]/(mass*hp)
    d=mass*np.cos(np.arange(m.n));d-=sum(d)/m.n;d*=1e-3;eps=1e-6;out={}
    for species,mu in [('T',mut),('F',muf)]:
        es=[]
        for sign in [1,-1]:
            mm=mass+sign*eps*d;tt=mass*q+(sign*eps*d if species=='T' else 0);xx=2/np.pi*np.arcsin(np.sqrt(tt/mm));es.append(m.direct(np.r_[mm,xx])[0])
        err=abs((es[0]-es[1])/(2*eps)-mu@d)/max(abs(mu@d),1);out[species+'_transfer_gradient_error']=err;assert err<1e-6
    a=T(v).requires_grad_(True);H=torch.autograd.functional.hessian(lambda y:m.energy(torch.log(y[:m.n]),y[m.n:]),a).detach().numpy();dd=np.sin(np.arange(2*m.n)+.6);dd[:m.n]*=1e-5
    gp=m.direct(v+eps*dd)[1];gm=m.direct(v-eps*dd)[1];err=np.linalg.norm((gp-gm)/(2*eps)-H@dd)/max(np.linalg.norm(H@dd),1);out['hessian_directional_error']=float(err);assert err<1e-6
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();old=json.loads(Path(__file__).with_name('run_warm').joinpath('results.json').read_text())['runs'];out=dict(checks=checks(),runs=[])
    for r in old[:2]:
        m=Warm(n=r['n'],domain=2,beta=1000,k=120,tau=1,K=3);v=np.r_[r['mass'],r['v'][m.n:]];y=T(v).requires_grad_(True)
        H=torch.autograd.functional.hessian(lambda yy:m.energy(torch.log(yy[:m.n]),yy[m.n:]),y).detach().numpy();H=(H+H.T)/2
        active=np.array(r['mass'])>1e-7;P=np.zeros((m.n,sum(active)-1));P[active,:]=null_space(np.ones((1,sum(active))))
        Hmm=P.T@H[:m.n,:m.n]@P;Hmx=P.T@H[:m.n,m.n:];Hxx=H[m.n:,m.n:];ev=float(eigvalsh(Hmm,subset_by_index=[0,0])[0]);mode=-np.gradient(v[m.n:],r['r'],edge_order=2)
        row=dict(n=m.n,active_mass_cells=int(sum(active)),density_eigenvalue=ev,frozen_density_translation_curvature=float(mode@Hxx@mode),units='Eunit/kpc^2; finite-grid diagnostic, not recovery')
        if ev>0:
            relaxed=Hxx-Hmx.T@np.linalg.solve(Hmm,Hmx);row['relaxed_translation_curvature']=float(mode@relaxed@mode);row['relaxed_phase_min_eigenvalue']=float(eigvalsh(relaxed,subset_by_index=[0,0])[0])
        out['runs'].append(row)
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
