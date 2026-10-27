"""Specified local pure-T finite-mediator reduction; no galaxy evolution."""
import argparse, itertools, json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

BASE = Path(__file__).resolve().parent
P = json.loads((BASE/'parameters.json').read_text())

def parameters(length_pc):
    rho,c,g,alpha = (P[k] for k in ['rho','c','g2','alpha'])
    ell=length_pc/1000/P['rm_kpc']
    M=c/ell if ell else np.inf
    lam=g/(M*np.sqrt(alpha))
    return rho,c,g,alpha,ell,M,lam

def omega(k,length_pc):
    k=np.asarray(k,float); kk=k@k
    rho,c,g,alpha,ell,M,lam=parameters(length_pc)
    eta=g*g*rho**3/c**2
    gap=rho*((1/(1-P['u'])-1)+(1/(1-P['u'])**2-1/(1-P['u']))*k[2]**2/kk)
    bare=gap+P['kappa']*kk*kk/4
    inertia=(1+eta)/(rho*kk)+lam*lam
    stiffness=bare/(rho*kk)+c*c*lam*lam*kk
    om=np.sqrt(stiffness/inertia)
    return om,1/np.sqrt(2*om*inertia),bare

def exact_omega(k,length_pc):
    # Exact local three-field quadratic determinant after eliminating phase.
    # This cancellation-free Schur form avoids subtracting M^2 lambda^2 terms.
    k=np.asarray(k,float);kk=k@k
    rho,c,g,alpha,ell,M,lam=parameters(length_pc)
    approx,_,bare=omega(k,length_pc);C=c*c*kk;a=alpha*rho*rho
    def D(x):
        den=(C-x)*(1+(C-x)/(M*M))-a*x
        return bare-x+rho*kk*(lam*lam*(C-x)**2-g*g*rho*rho*x)/den
    root=brentq(D,0.,min(4*approx*approx,C/(1+a)*.9),xtol=1e-10,rtol=2e-14)
    return np.sqrt(root),abs(D(root))/bare

def resonance(q,length_pc):
    target=2*omega([q,0,0],length_pc)[0]
    def mismatch(z):return omega([q*(1+z),q*np.sqrt(1-z*z),0],length_pc)[0]-target
    z=brentq(mismatch,-.99,.999999,xtol=1e-14)
    return np.array([q,0.,0.]),np.array([q*z,q*np.sqrt(1-z*z),0.])

def vertex(k1,k2,length_pc,volume):
    rho,c,g,alpha,ell,M,lam=parameters(length_pc)
    eta=g*g*rho**3/c**2
    ks=[np.asarray(k1),np.asarray(k2),np.asarray(k1)+np.asarray(k2)]
    oa=[omega(k,length_pc) for k in ks];om=np.array([z[0] for z in oa]);A=np.array([z[1] for z in oa]);sq=np.array([k@k for k in ks]);B=om*A/(rho*sq)
    d12=ks[0]@ks[1];d13=ks[0]@ks[2];d23=ks[1]@ks[2]
    vel=A[0]*B[1]*B[2]*d23+A[1]*B[0]*B[2]*d13+A[2]*B[0]*B[1]*d12
    quant=-P['kappa']*np.prod(A)/(4*rho*rho)*(d23+d13-d12)
    mom=[ks[0],ks[1],-ks[2]];sign=[1,1,-1]
    summation=sum(sign[i]*sign[l]*om[i]*om[l]*(2+mom[i]@mom[l]/sq[l])/sq[i] for i,j,l in itertools.permutations(range(3)))
    added=eta*np.prod(A)*summation/(rho*rho)
    # transverse modes: nonlocal response cubic is zero; quadratic gap retained.
    assert all(k[2]==0 for k in ks)
    return {'omega':om,'A':A,'V':(vel+quant+added)/np.sqrt(volume),'velocity':vel/np.sqrt(volume),'quantum':quant/np.sqrt(volume),'inertia':added/np.sqrt(volume)}

def run(out):
    rows=[]
    for q in [40.,80.,160.,320.]:
      vol=(4*np.pi/q)**3/3
      for length in [0.,.01,.1,1.]:
        k1,k2=resonance(q,length);v=vertex(k1,k2,length,vol)
        rho,c,g,alpha,ell,M,lam=parameters(length)
        exact=np.array([exact_omega(k,length)[0] for k in [k1,k2,k1+k2]])
        N=.05**2*rho*rho*vol/(64*v['A'][0]**2)
        rows.append({'q':q,'length_pc':length,'eta':g*g*rho**3/c**2,'alpha_rho_squared':alpha*rho*rho,
          'relative_added_gradient_stiffness':4*rho*c*c*lam*lam/P['kappa'],
          'frequency_per_Myr':(v['omega']/P['tdyn_Myr']).tolist(),
          'exact_frequency_per_Myr':(exact/P['tdyn_Myr']).tolist(),
          'frequency_relative_error':float(np.max(abs(exact-v['omega'])/exact)),
          'exact_resonance_mismatch_per_Myr':float((exact[2]-exact[0]-exact[1])/P['tdyn_Myr']),
          'angle_degrees':float(np.degrees(np.arccos(k1@k2/q**2))),
          'vertex':float(v['V']),'vertex_parts':{s:float(v[s]) for s in ['velocity','quantum','inertia']},
          'weak_mode_coupling_per_Myr':float(abs(v['V'])*np.sqrt(N)/P['tdyn_Myr']),
          'max_kell':float(np.linalg.norm(k1+k2)*ell),
          'max_scalar_retardation_parameter':float(max((1+alpha*rho*rho)*o*o/(c*c*(k@k)) for k,o in zip([k1,k2,k1+k2],v['omega']))),
          'static_scope':'1 pc failed inherited static target' if length==1 else '0 denotes old-action limit; .01 and .1 pc passed inherited static test'})
    old=json.loads(Path('nonlinear_cascade_2026_10_25/run_cc_mode_wave/results.json').read_text())
    base=next(r for r in rows if r['q']==80 and r['length_pc']==0)
    assert abs(base['vertex']/old['vertex']['real']-1)<1e-10
    assert np.max(abs(np.array(base['frequency_per_Myr'])/old['frequencies_per_Myr']-1))<1e-10
    zeros=[]
    for q in [40.,80.,160.,320.]:
      vol=(4*np.pi/q)**3/3
      fn=lambda length:vertex(*resonance(q,length),length,vol)['V']
      if fn(.01)*fn(1)<0:
        length=brentq(fn,.01,1,xtol=1e-13)
        zeros.append({'q':q,'zero_length_pc':length,'vertex_residual':float(fn(length))})
    result={'rows':rows,'cancellation_points':zeros,'old_model_reproduction_pass':True,
      'scope':'Local homogeneous pure-T transverse weak modes; leading quasistatic stationary metric plus tracking-density gradient and kinetic terms. Exact quadratic parent comparison tests frequencies, NOT omitted cubic dynamic corrections. No actual occupations, cooling, galaxy evolution or global causality.'}
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);run(a.parse_args().output)
