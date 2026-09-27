#!/usr/bin/env python3
"""Exact nonlinear inhomogeneous lapse data and numerical spectral refinement."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    x,eps,b,ell,q,Lam,r0=s.symbols('x eps b ell q Lambda rho0',real=True)
    y=s.exp(eps*s.cos(x));S=2*s.log(y)
    A=4*b*eps*s.cos(x)-4*b*eps**2*s.sin(x)**2
    checks={}
    def exact(name,expr):
        val=s.simplify(s.expand_trig(expr));assert val==0,(name,val);checks[name]=str(val)
    exact('lapse_equation',4*b*s.diff(y,x,2)+A*y)
    exact('lapse_log_constraint',A+b*(s.diff(S,x)**2+2*s.diff(S,x,2)))
    rho=r0+A
    exact('matter_and_fixed_trace_data',(-ell*q*q+Lam+rho).subs(q*q,(Lam+r0)/ell)-A)
    f=s.Function('f')(x)
    exact('ground_state_energy_factorization',s.diff(y*f,x)**2+s.diff(y,x,2)/y*(y*f)**2-y*y*s.diff(f,x)**2-s.diff(y*f*f*s.diff(y,x),x))
    A0=s.Function('A')(x);yy=s.Function('y')(x)
    density=yy**2*A0-4*b*s.diff(yy,x)**2
    EL=s.diff(density,yy)-s.diff(s.diff(density,s.diff(yy,x)),x)
    exact('actual_lapse_variation',EL-2*(A0*yy+4*b*s.diff(yy,x,2)))
    # Momentum constraint: pi^{ij}=q sqrt(h) h^{ij}/3 with flat h and constant q;
    # matter at rest and vanishing traceless momentum give Di pi^{ij}=0.
    vals={'b':.2,'ell':.1,'Lambda':.7,'rho0':.5,'eps':.1}
    assert vals['rho0']>4*vals['b']*(abs(vals['eps'])+vals['eps']**2)
    qv=-np.sqrt((vals['Lambda']+vals['rho0'])/vals['ell'])
    gap_lower=4*vals['b']*np.exp(-4*abs(vals['eps']))
    rows=[]
    for n in [64,128,256,512]:
        xx=2*np.pi*np.arange(n)/n;dx=2*np.pi/n
        yv=np.exp(vals['eps']*np.cos(xx))
        av=4*vals['b']*vals['eps']*np.cos(xx)-4*vals['b']*vals['eps']**2*np.sin(xx)**2
        lap=diags([np.ones(n-1),-2*np.ones(n),np.ones(n-1)],[-1,0,1],format='lil')/dx**2
        lap[0,n-1]=lap[n-1,0]=1/dx**2;lap=lap.tocsr()
        op=-4*vals['b']*lap-diags(av)
        ev,vec=eigsh(op,k=3,which='SA',tol=1e-11,v0=np.ones(n))
        order=np.argsort(ev);ev=ev[order];vec=vec[:,order]
        ground=vec[:,0]*np.sign(np.sum(vec[:,0]));ground/=np.sqrt(np.mean(ground**2))
        yn=yv/np.sqrt(np.mean(yv*yv))
        assert np.min(ground)>0 and ev[1]>gap_lower*.99
        rows.append({'n':n,'eigenvalues':ev.tolist(),'ground_state_max_error':float(np.max(np.abs(ground-yn))),
                     'continuous_lapse_discrete_residual_max':float(np.max(np.abs(op@yv))),
                     'matter_density_min':float(np.min(vals['rho0']+av)),
                     'lapse_min':float(np.min(yv*yv)),'lapse_max':float(np.max(yv*yv))})
    for old,new in zip(rows,rows[1:]):
        assert new['continuous_lapse_discrete_residual_max']<.26*old['continuous_lapse_discrete_residual_max']
        assert new['ground_state_max_error']<.27*old['ground_state_max_error']
    assert abs(rows[-1]['eigenvalues'][0])<1e-7
    # Fixed action, genuinely prescribed nonconstant positive source: solve the
    # global constraint by changing initial trace momentum, not Lambda/ell/b.
    n=256;xx=2*np.pi*np.arange(n)/n;dx=2*np.pi/n
    lap=diags([np.ones(n-1),-2*np.ones(n),np.ones(n-1)],[-1,0,1],format='lil')/dx**2
    lap[0,n-1]=lap[n-1,0]=1/dx**2;lap=lap.tocsr()
    supplied_rho=.5*(1+.4*np.cos(xx)+.2*np.sin(2*xx))
    op0=-4*vals['b']*lap-diags(vals['Lambda']+supplied_rho)
    ev,vec=eigsh(op0,k=2,which='SA',tol=1e-12,v0=np.ones(n));ind=np.argsort(ev);ev=ev[ind];vec=vec[:,ind]
    qp=-np.sqrt(-ev[0]/vals['ell']);yp=vec[:,0]*np.sign(np.sum(vec[:,0]));yp/=np.sqrt(np.mean(yp*yp))
    residual=float(np.max(np.abs((op0+diags(np.full(n,vals['ell']*qp*qp)))@yp)))
    assert ev[0]<0 and np.min(yp)>0 and residual<1e-9
    out={'symbolic_checks':checks,'fixed_action_parameters':vals,'exact_family_q':qv,
         'proper_barred_expansion_rate':-vals['ell']*qv,'analytic_gap_lower':gap_lower,
         'refinement':rows,'prescribed_source_numerical_control':{'n':n,'q':float(qp),'lapse_min':float(np.min(yp*yp)),
             'groundvalue_before_q_adjustment':float(ev[0]),'positive_gap':float(ev[1]-ev[0]),'residual':residual},
         'non_claims':['No proof that these data have a globally regular nonlinear evolution',
             'No completed full Dirac chain or classification of scalar as allowed matter/clock',
             'No noncompact-leaf spectral-gap claim','No MOND or pin-transition certificate for this modified cosmological sector']}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'symbolic_checks':len(checks),'refinement_cases':len(rows),'passed':True,'groundvalue_last':rows[-1]['eigenvalues'][0]}))

if __name__=='__main__':main()
