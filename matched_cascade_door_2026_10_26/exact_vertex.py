"""Cubic vertex of the finite-M canonical parent, not just tracking truncation."""
import argparse,itertools,json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from spectrum import P,parameters,exact_omega,vertex as reduced_vertex,resonance

def mode(k,length):
    k=np.asarray(k,float);K=k@k
    rho,c,g,alpha,ell,M,lam=parameters(length);h=M*np.sqrt(alpha)
    w,res=exact_omega(k,length);C=c*c*K;x=w*w
    b=g/(1+(C-x)/(M*M)-alpha*rho*rho*x/(C-x))
    # b means h delta_s / delta_rho; use it to avoid large-h conditioning.
    Scoef=b/h if np.isfinite(h) else 0.
    inertia=1/(rho*K)+Scoef*Scoef+rho*rho*b*b*C/(C-x)**2
    A=1/np.sqrt(2*w*inertia)
    return {'w':w,'A':A,'phi':-1j*w*A/(rho*K),'b':b*A,
      'chi':1j*w*rho*b*A/(C-x),'chit':x*rho*b*A/(C-x),
      's':Scoef*A,'ps':-1j*w*Scoef*A,'Pchi':rho*b*A*C/(C-x),
      'H_s':rho*b*A,'residual':res,'norm':2*w*A*A*inertia}

def exact_resonance(q,length):
    target=2*mode([q,0,0],length)['w']
    fun=lambda z:mode([q*(1+z),q*np.sqrt(1-z*z),0],length)['w']-target
    z=brentq(fun,-.99,.999999,xtol=1e-14)
    return np.array([q,0.,0.]),np.array([q*z,q*np.sqrt(1-z*z),0.])

def full_vertex(k1,k2,length,volume):
    ks=[np.asarray(k1),np.asarray(k2),np.asarray(k1)+np.asarray(k2)]
    modes=[mode(k,length) for k in ks];sign=[1,1,-1];mom=[sign[i]*ks[i] for i in range(3)]
    rho=P['rho'];n=np.array([m['A'] for m in modes]);b=np.array([m['b'] for m in modes]);ct=np.array([m['chit'] for m in modes])
    phi=np.array([m['phi'] if i<2 else m['phi'].conjugate() for i,m in enumerate(modes)])
    chi=np.array([m['chi'] if i<2 else m['chi'].conjugate() for i,m in enumerate(modes)])
    terms=dict(velocity=0j,quantum=0j,spatial_current=0j,temporal_current=0j)
    for i,j,l in itertools.permutations(range(3)):
        dot=mom[j]@mom[l]
        terms['velocity']+=-.5*n[i]*dot*phi[j]*phi[l]
        terms['quantum']+=P['kappa']/(8*rho*rho)*n[i]*dot*n[j]*n[l]
        terms['spatial_current']+=rho*b[i]*dot*phi[j]*chi[l]
        terms['temporal_current']-=n[i]*b[j]*ct[l]
    terms={k:float(np.real(v)/np.sqrt(volume)) for k,v in terms.items()}
    return sum(terms.values()),terms,modes

def derivative_audit(length,q):
    # Independent mixed derivative of the actual canonical squares, using an
    # oblique periodic cell: phases theta1,theta2 and physical vectors k1,k2.
    import torch
    torch.set_num_threads(1)
    k1,k2=exact_resonance(q,length);ks=[k1,k2,k1+k2];vol=(4*np.pi/q)**3/3
    predicted,terms,modes=full_vertex(k1,k2,length,vol)
    theta=np.arange(9)*2*np.pi/9;t1,t2=np.meshgrid(theta,theta,indexing='ij');phases=[t1,t2,t1+t2]
    scalar={s:[] for s in ['n','b','s','ps','Pchi','H_s']};grad={s:[] for s in ['n','phi','chi','s']}
    for k,m,phase in zip(ks,modes,phases):
        wave=np.exp(1j*phase)/np.sqrt(vol)
        for key in scalar:scalar[key].append(2*np.real((m['A'] if key=='n' else m[key])*wave))
        for key in grad:grad[key].append(2*np.real(1j*wave[...,None]*k*(m['A'] if key=='n' else m[key])))
    e=torch.zeros(3,dtype=torch.float64,requires_grad=True)
    vals={s:torch.einsum('i,ixy->xy',e,torch.tensor(np.array(v))) for s,v in scalar.items()}
    gs={s:torch.einsum('i,ixya->xya',e,torch.tensor(np.array(v))) for s,v in grad.items()}
    rho,c,g,alpha,ell,M,lam=parameters(length);rr=rho+vals['n']
    velocity=gs['phi']-vals['b'][...,None]*gs['chi']
    # Every parent contribution retained except density-only nonlocal response,
    # whose transverse cubic derivative vanishes. Its quadratic gap is in mode().
    H=.5*rr*torch.sum(velocity**2,dim=-1)+P['kappa']/(8*rr)*torch.sum(gs['n']**2,dim=-1)
    H+=.5*(vals['Pchi']-vals['H_s']-vals['b']*vals['n'])**2
    H+=.5*c*c*(torch.sum(gs['chi']**2,dim=-1)+torch.sum(gs['s']**2,dim=-1))+.5*vals['ps']**2
    H+=.5*M*M*(vals['s']-lam*vals['n'])**2
    expr=vol*H.mean();d=torch.autograd.grad(expr,e,create_graph=True)[0][0];d=torch.autograd.grad(d,e,create_graph=True)[0][1];measured=float(torch.autograd.grad(d,e)[0][2])
    error=abs(measured-2*predicted)/max(abs(2*predicted),1e-12)
    assert error<2e-10
    return {'length_pc':length,'q':q,'predicted_mixed_third':2*predicted,'automatic_mixed_third':measured,'relative_error':error}

def run(out):
    rows=[]
    for q in [40.,80.,160.,320.]:
      vol=(4*np.pi/q)**3/3
      for length in [.01,.1,1.]:
        k1,k2=exact_resonance(q,length);V,terms,m=full_vertex(k1,k2,length,vol)
        red=reduced_vertex(*resonance(q,length),length,vol)
        N=.05**2*P['rho']**2*vol/(64*m[0]['A']**2)
        rows.append({'q':q,'length_pc':length,'vertex':V,'parts':terms,'frequency_per_Myr':[v['w']/P['tdyn_Myr'] for v in m],
          'resonance_residual_relative':abs(m[2]['w']-m[0]['w']-m[1]['w'])/m[2]['w'],
          'reduced_vertex_relative_error':abs(V-red['V'])/abs(V),'weak_mode_coupling_per_Myr':abs(V)*np.sqrt(N)/P['tdyn_Myr'],
          'max_dispersion_residual':max(v['residual'] for v in m),'max_normalization_error':max(abs(v['norm']-1) for v in m)})
    audits=[derivative_audit(length,q) for length,q in [(.01,80),(.1,80),(.1,320),(1.,80)]]
    result={'rows':rows,'independent_canonical_square_audits':audits,'scope':'Exact cubic Taylor coefficient and exact quadratic polarizations of the specified homogeneous transverse pure-T finite-M parent. Local 3D continuation inherited from earlier lane; no mean-flow feeding, quantum occupation prescription, radiation escape or global formation.'}
    assert max(r['resonance_residual_relative'] for r in rows)<1e-12
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);run(a.parse_args().output)
