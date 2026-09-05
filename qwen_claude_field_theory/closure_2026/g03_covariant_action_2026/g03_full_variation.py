#!/usr/bin/env python3
"""Full localized C-H variations and an exact cylindrical electrovacuum branch.

No PPN or DOF value is supplied. The cylinder extends the former closed-leaf
domain explicitly; it is not a Galactic background or a global torus solution.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import platform
import subprocess
import sys
import time

import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as sp
from g03_action_gate import kernel

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def derivative(f,axis=-1):
    n=f.shape[axis]
    k=np.fft.fftfreq(n,1/n)
    shape=[1]*f.ndim
    shape[axis]=n
    return np.fft.ifft(1j*k.reshape(shape)*np.fft.fft(f,axis=axis),axis=axis).real


def clock_variation(nsize):
    """Off-shell clock variation in 1+1 flat space, spectator directions constant.

    The local action after spatial integration by parts is differentiated,
    including all acceleration and induced-projector dependence.
    """
    t,x=np.meshgrid(np.arange(nsize)*2*np.pi/nsize,np.arange(nsize)*2*np.pi/nsize,indexing='ij')
    tau_t=1+.06*np.cos(t)*np.cos(x)
    tau_x=-.06*np.sin(t)*np.sin(x)
    chi=.07*np.cos(2*t)*np.sin(x)+.03*np.sin(t)*np.cos(2*x)
    chi_t=derivative(chi,0)
    chi_x=derivative(chi,1)
    gradU=np.stack([-.13*np.sin(x)*np.sin(t), .8+.13*np.cos(x)*np.cos(t)])
    nodes,weights=np.polynomial.legendre.leggauss(8)
    zs=(nodes+1)*.15
    weights=weights*.15
    Ws=[]
    for z,weight in zip(zs,weights):
        wt=-.12*np.sin(x)*np.sin(t)+z*.09*np.cos(2*x)*np.cos(t)-z*z*.08*np.sin(x)*np.sin(2*t)
        wx=.8+.12*np.cos(x)*np.cos(t)-z*.18*np.sin(2*x)*np.sin(t)+z*z*.04*np.cos(x)*np.cos(2*t)
        wz=.09*np.cos(2*x)*np.sin(t)+2*z*.04*np.sin(x)*np.cos(2*t)
        ell=.12+.15*np.cos(x)*np.sin(t)*(1+.2*z)+.08*np.sin(2*x)*np.cos(2*t)
        lt=.15*np.cos(x)*np.cos(t)*(1+.2*z)-.16*np.sin(2*x)*np.sin(2*t)
        lx=-.15*np.sin(x)*np.sin(t)*(1+.2*z)+.16*np.cos(2*x)*np.cos(2*t)
        Ws.append((weight,np.stack([wt,wx]),wz,ell,np.stack([lt,lx])))
    z=.3
    gradB=np.stack([-.12*np.sin(x)*np.sin(t)+z*.09*np.cos(2*x)*np.cos(t)-z*z*.08*np.sin(x)*np.sin(2*t),
                    .8+.12*np.cos(x)*np.cos(t)-z*.18*np.sin(2*x)*np.sin(t)+z*z*.04*np.cos(x)*np.cos(2*t)])
    metric=np.diag([-1.,1.])
    def geometry(tt,tx):
        sqrtX=np.sqrt(tt*tt-tx*tx)
        ndn=np.stack([-tt/sqrtX,-tx/sqrtX])
        nup=np.stack([-ndn[0],ndn[1]])
        hh=metric[:,:,None,None]+np.einsum('i...,j...->ij...',nup,nup)
        acov=np.stack([nup[0]*derivative(ndn[i],0)+nup[1]*derivative(ndn[i],1) for i in range(2)])
        return sqrtX,ndn,nup,hh,acov
    def hdot(hh,p,q):
        return np.einsum('ij...,i...,j...->...',hh,p,q)
    def gdot(p,q):
        return -p[0]*q[0]+p[1]*q[1]
    def energy(tt,tx):
        _,ndn,nup,hh,acov=geometry(tt,tx)
        pb2=hdot(hh,gradB,gradB)
        q,_=kernel(np.sqrt(pb2))
        L=2*hdot(hh,gradU,gradU)-4*gdot(acov,gradU)+2*gdot(acov,acov)+2*q
        for weight,gW,wz,ell,gL in Ws:
            L +=weight*(ell*wz+hdot(hh,gL,gW)+ell*gdot(acov,gW))
        return float(np.mean(L))
    sqrtX,ndn,nup,hh,acov=geometry(tau_t,tau_x)
    pb=np.sqrt(hdot(hh,gradB,gradB))
    _,fb=kernel(pb)
    qp=fb/pb
    dotU=np.einsum('i...,i...->...',nup,gradU)
    dotB=np.einsum('i...,i...->...',nup,gradB)
    current=4*dotU*gradU+4*qp*dotB*gradB
    avec=-4*gradU+4*acov
    for weight,gW,wz,ell,gL in Ws:
        avec +=weight*ell*gW
        dotW=np.einsum('i...,i...->...',nup,gW)
        dotL=np.einsum('i...,i...->...',nup,gL)
        current +=weight*(dotL*gW+dotW*gL)
    aup=np.stack([-avec[0],avec[1]])
    for mu in range(2):
        current[mu] +=sum(aup[rho]*derivative(ndn[rho],mu) for rho in range(2))
        current[mu] -=derivative(nup[0]*avec[mu],0)+derivative(nup[1]*avec[mu],1)
    projected=np.einsum('ij...,j...->i...',hh,current)/sqrtX
    Eclock=derivative(projected[0],0)+derivative(projected[1],1)
    analytic=float(np.mean(Eclock*chi))
    step=2e-5
    finite=(energy(tau_t+step*chi_t,tau_x+step*chi_x)-energy(tau_t-step*chi_t,tau_x-step*chi_x))/(2*step)
    return dict(grid=nsize,analytic=analytic,finite_difference=finite,error=abs(analytic-finite),
                unit_error=float(np.max(abs(-nup[0]**2+nup[1]**2+1))))


def metric_variation(nsize):
    """Off-shell lapse and spatial-trace variations, including heat stress."""
    x=np.arange(nsize)*2*np.pi/nsize
    eta=.12*np.sin(x)+.08*np.cos(2*x)
    w=.11*np.cos(x)+.05*np.sin(2*x)
    direction=.17*np.sin(2*x)+.08*np.cos(3*x)
    U=.8*x+.14*np.sin(x)
    Up=.8+.14*np.cos(x)
    nodes,weights=np.polynomial.legendre.leggauss(12)
    zs=(nodes+1)*.15
    weights=weights*.15
    fields=[]
    for z,weight in zip(zs,weights):
        W=.8*x+.12*np.sin(x)+z*.07*np.cos(2*x)
        Wp=.8+.12*np.cos(x)-z*.14*np.sin(2*x)
        Wz=.07*np.cos(2*x)
        ell=.17+.12*np.sin(x)*(1+.2*z)
        fields.append((weight,Wp,Wz,ell,derivative(ell)))
    W0=.8*x+.12*np.sin(x)
    Wbp=.8+.12*np.cos(x)-.3*.14*np.sin(2*x)
    lm=.13*np.cos(x)
    def terms(nn,ww):
        N=np.exp(nn)
        volume=np.exp(3*ww)
        a=derivative(nn)
        V=Up-a
        inv=np.exp(-2*ww)
        p=np.sqrt(inv)*Wbp
        q,f=kernel(p)
        L=2*inv*V*V+2*q+lm*(W0-U)
        cross=np.zeros(nsize)
        defect=np.zeros(nsize)
        for weight,Wp,Wz,ell,ellp in fields:
            cc=inv*(ellp+ell*a)*Wp
            L +=weight*(ell*Wz+cc)
            cross +=weight*cc
            lap=inv*(derivative(Wp)+derivative(ww)*Wp)
            defect +=weight*ell*(Wz-lap)
        divV=derivative(np.exp(ww)*V)/volume
        H=2*inv*V*V+4*inv*V*a+4*divV+2*q+defect+lm*(W0-U)
        traceP=1.5*L-2*inv*V*V-2*f*p-cross
        return float(np.mean(N*volume*L)),N*volume,H,traceP,cross
    E,weight,H,traceP,cross=terms(eta,w)
    step=2e-5
    fdN=(terms(eta+step*direction,w)[0]-terms(eta-step*direction,w)[0])/(2*step)
    fdh=(terms(eta,w+step*direction)[0]-terms(eta,w-step*direction)[0])/(2*step)
    analyticN=float(np.mean(weight*H*direction))
    analytich=float(np.mean(weight*2*traceP*direction))
    wrongh=float(np.mean(weight*2*(traceP+cross)*direction))
    return dict(grid=nsize,lapse_error=abs(fdN-analyticN),metric_trace_error=abs(fdh-analytich),
                omitted_heat_stress_error=abs(fdh-wrongh))


def background(y,xi_alpha=.2,Lambda=.03):
    """alpha=1; solve the lower root, without assigning a solution flag."""
    s=y*(-math.expm1(-y))
    f=y*math.exp(-y)
    q=float(kernel(np.array([s]))[0][0])
    b=xi_alpha**2/2
    fun=lambda a:a-s-f*math.exp(b*a*a)
    grid=np.linspace(y,max(3*y,3),1001)
    crossings=[(left,right) for left,right in zip(grid[:-1],grid[1:]) if fun(left)*fun(right)<0]
    if not crossings:
        raise RuntimeError('No bracketed lower background root in declared search interval')
    a=brentq(fun,*crossings[0],xtol=1e-14)
    E=math.exp(b*a*a)
    V=s-a
    eps=a*a-s*s-q
    transverse=V*V+q+2*s*f*math.expm1(b*a*a)
    invR2=a*a+2*Lambda-2*(q-s*f)
    rho=a*a+Lambda-transverse # includes kappa=8 pi G/c^4
    return dict(y=y,s=s,f=f,q=q,b=b,xi_alpha=xi_alpha,Lambda=Lambda,a=a,E=E,V=V,
                eps=eps,Pparallel=-eps,Pperp=transverse,invR2=invR2,rho_em=rho,
                tangent=1/(1+(y-1)*math.exp(-y))-1,
                auxiliary_residual=-4*a*V-4*a*f*E,
                normal_residual=invR2-Lambda-eps-rho,
                radial_residual=-invR2+Lambda+eps+rho,
                angular_residual=a*a+Lambda-transverse-rho)


def cylinder_linear(bkg,k,u,n,zeta=1,conserved_source=False,quadrature_stress=False):
    """Full localized *linear constraints*, not a principal-symbol truncation.

    Includes curvature, lapse weighting, W's metric variation, and the entire
    auxiliary-coordinate multiplier transport on the exact cylinder.
    """
    a,p,f,ell,b=[bkg[key] for key in ('a','s','f','tangent','b')]
    V=bkg['V']
    sigma=np.exp(-b*k*k)
    wb=sigma*u+2j*p*zeta*(-np.expm1(-b*k*k))/k
    lb=4*((a+1j*k)*ell*1j*k*wb+1j*k*f*(n+2*zeta))
    M=(a+1j*k)**2
    dM=M-a*a
    B=dM*n+2j*k*a*zeta
    l0=np.exp(M*b)*lb+4*a*f*np.exp(a*a*b)*B*np.expm1(dM*b)/dM
    eu=-4*((a+1j*k)*1j*k*(u-n)+1j*k*V*(n+2*zeta))-l0
    dH=4*(p*1j*k*(u-n)+V*1j*k*n-k*k*(u-n)+2j*k*V*zeta+f*1j*k*wb)
    eN=4*(k*k-bkg['invR2'])*zeta+dH+8*bkg['rho_em']*zeta
    if conserved_source:
        eN -=4*(k*k+a*a)*zeta
    # Independent xx metric-equation check with the full multiplier stress.
    Ibase=4*f/a*np.expm1(a*a*b)
    iw0=-np.expm1(-a*a*b)/(a*a)
    iw1=-np.expm1(-(a*a+k*k)*b)/(a*a+k*k)
    Iw=4*a*f*np.exp(a*a*b)*(u*iw1+2j*p*zeta*(iw0-iw1)/k)
    Im=np.expm1(M*b)/M
    Il=lb*Im+B*4*a*f/dM*(Im-np.expm1(a*a*b)/(a*a))
    integralCross=(a+1j*k)*p*Il+a*1j*k*Iw+p*1j*k*n*Ibase
    integralL=-k*k*Iw+2j*k*p*zeta*Ibase+integralCross
    if quadrature_stress:
        nodes,weights=np.polynomial.legendre.leggauss(64)
        zs=(nodes+1)*b/2
        weights=weights*b/2
        integralL=0j
        integralCross=0j
        for z,weight in zip(zs,weights):
            sig=np.exp(-k*k*z)
            ww=sig*u+2j*p*zeta*(-np.expm1(-k*k*z))/k
            wz=-k*k*sig*u+2j*k*p*zeta*sig
            Lbar=4*a*f*np.exp(a*a*(b-z))
            LL=np.exp(M*(b-z))*lb+B*Lbar*np.expm1(dM*(b-z))/dM
            cross=(a+1j*k)*p*LL+a*Lbar*1j*k*ww+Lbar*p*1j*k*n
            integralL +=weight*(Lbar*wz+cross)
            integralCross +=weight*cross
    dL=4*V*1j*k*(u-n)+4*f*1j*k*wb+integralL
    dPxx=.5*dL-4*V*1j*k*(u-n)-2*(ell*p+f)*1j*k*wb-integralCross
    exx=(2j*a*k+2*bkg['invR2'])*zeta-dPxx-4*bkg['rho_em']*zeta
    if conserved_source:
        exx -=2*(1j*a*k-a*a)*zeta
    deps=-dH/2
    charge=deps+2*(bkg['eps']+bkg['Pperp'])*zeta
    if conserved_source:
        charge -=2*(k*k+a*a)*zeta
    return np.array([eu,eN]),dict(radial_equation_residual=exx,delta_eps=deps,charge=charge,
                                delta_Pperp=.5*dL,delta_Pparallel=dPxx)


def main():
    started=time.time()
    records=[]
    results={}
    def check(name,ok,value):
        records.append(dict(name=name,passed=bool(ok),evidence=value))
        print(f'[{"ok" if ok else "FAIL"}] {len(records)} {name}: {value}',flush=True)
    clocks=[clock_variation(n) for n in (32,48)]
    check('complete off-shell clock current',all(r['error']<2e-8 for r in clocks),clocks)
    metrics=[metric_variation(n) for n in (32,48)]
    check('full lapse and spatial heat stress',
          all(r['lapse_error']<2e-8 and r['metric_trace_error']<2e-8 and r['omitted_heat_stress_error']>1e-4 for r in metrics),metrics)
    results.update(clock_variation=clocks,metric_variation=metrics)

    a,R=sp.symbols('a R',positive=True)
    tt,xx,theta,azimuth=coords=sp.symbols('t x theta azimuth',real=True)
    g=sp.diag(-sp.exp(2*a*xx),1,R**2,R**2*sp.sin(theta)**2)
    gi=g.inv()
    Gamma=[[[sp.simplify(sum(gi[i,l]*(sp.diff(g[l,j],coords[k])+sp.diff(g[l,k],coords[j])-sp.diff(g[j,k],coords[l])) for l in range(4))/2)
             for k in range(4)] for j in range(4)] for i in range(4)]
    Ric=sp.Matrix(4,4,lambda i,j:sp.simplify(sum(sp.diff(Gamma[k][i][j],coords[k])-sp.diff(Gamma[k][i][k],coords[j])+
          sum(Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k] for l in range(4)) for k in range(4))))
    scalar=sp.simplify(sum(gi[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
    Einstein=sp.simplify(Ric-g*scalar/2)
    check('exact product background geometry',
          sp.simplify(Einstein[0,0]*sp.exp(-2*a*xx)-1/R**2)==0
          and sp.simplify(Einstein[1,1]+1/R**2)==0
          and sp.simplify(Einstein[2,2]/R**2-a*a)==0,
          dict(Ricci_scalar=str(scalar),Gnn=str(sp.simplify(Einstein[0,0]*sp.exp(-2*a*xx))),Gxx=str(Einstein[1,1])))
    electric=sp.symbols('electric',real=True)
    # sqrt(-g) F^{xt}=R^2 sin(theta) E for F_tx=N E.
    maxwell=sp.diff(sp.exp(a*xx)*R**2*sp.sin(theta)*electric*sp.exp(-a*xx),xx)
    check('source-free Maxwell background',maxwell==0,'constant orthonormal electric field along the cylinder')

    bkgs=[background(y) for y in (.8,1.,2.056919939710967,2.478129439536846)]
    check('nonzero exact C-H electrovacuum backgrounds',
          all(max(abs(r[key]) for key in ('auxiliary_residual','normal_residual','radial_residual','angular_residual'))<1e-11
              and r['rho_em']>0 and r['invR2']>0 for r in bkgs),
          [dict(y=r['y'],a=r['a'],R=r['invR2']**-.5,rho_em=r['rho_em'],epsilon=r['eps']) for r in bkgs])
    rows=[]
    for bkg in bkgs:
        for k in (.2,.7,2.,7.,15.):
            e0,_=cylinder_linear(bkg,k,0,0)
            eU,_=cylinder_linear(bkg,k,1,0)
            eN,_=cylinder_linear(bkg,k,0,1)
            matrix=np.column_stack([eU-e0,eN-e0])
            u,n=np.linalg.solve(matrix,-e0)
            residual,extra=cylinder_linear(bkg,k,u,n)
            singular=np.linalg.svd(matrix,compute_uv=False)
            row=dict(y=bkg['y'],k=k,condition_number=float(singular[0]/singular[-1]),
                     normalized_constraint_residual=float(np.linalg.norm(residual)/(1+np.linalg.norm(e0))),
                     normalized_radial_residual=float(abs(extra['radial_equation_residual'])/(1+k*k)),
                     normalized_charge_error=float(abs(extra['charge']-2*(k*k+bkg['a']**2))/(1+k*k)),
                     charge_real=float(extra['charge'].real),charge_imag=float(extra['charge'].imag),
                     lapse_response=[float(n.real),float(n.imag)],U_response=[float(u.real),float(u.imag)])
            rows.append(row)
    check('full constraints admit nonzero scalar charge',
          all(r['normalized_constraint_residual']<2e-10 and r['charge_real']>0 for r in rows),
          dict(cases=len(rows),max_constraint_residual=max(r['normalized_constraint_residual'] for r in rows),
               largest_condition_number=max(r['condition_number'] for r in rows)))
    check('independent radial equation includes heat stress',
          all(r['normalized_radial_residual']<2e-9 for r in rows),
          dict(max_residual=max(r['normalized_radial_residual'] for r in rows)))
    check('gauge-invariant conserved scalar charge',
          all(r['normalized_charge_error']<2e-9 for r in rows),
          'delta C = delta epsilon + 2(epsilon+Pperp) zeta = 2(k^2+a^2) zeta; dot C=0')
    homogeneous=[dict(y=r['y'],fixed_charge_radius_coefficient=4*(2*r['rho_em']-r['invR2'])) for r in bkgs]
    check('k=0 handled without inverting singular lapse/U block',
          all(abs(r['fixed_charge_radius_coefficient'])>1e-6 for r in homogeneous),homogeneous)
    # A scalar charge is not a count: constraints could change on other branches.
    results.update(backgrounds=bkgs,constraint_responses=rows,k0=homogeneous)
    failed=[r['name'] for r in records if not r['passed']]
    payload=dict(date=datetime.now(timezone.utc).isoformat(),checks=records,results=results,
                 failed_checks=failed,status='OPEN' if not failed else 'OPEN_WITH_FAILED_DIAGNOSTIC',
                 strongest_result='Exact varied clock/metric equations and a conserved nonzero scalar charge on an exact cylindrical electrovacuum branch, subject to numerical checks.',
                 remaining=['full retarded curvature response with dynamically admissible localized matter sources',
                            'generic branch health and independent physical-time data count',
                            'closed-leaf and zero-gradient branches'])
    path=HERE/'full_variation_results.json'
    path.write_text(json.dumps(payload,indent=2)+'\n')
    rc=int(bool(failed))
    sources=[HERE/'g03_full_variation.py',HERE/'g03_action_gate.py',HERE/'ACTION.md']
    if (HERE/'FULL_VARIATION.md').exists(): sources.append(HERE/'FULL_VARIATION.md')
    manifest=dict(schema_version=1,claim_id='C-H-full-variation-cylinder-charge',
        repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                        dirty=bool(subprocess.check_output(['git','status','--porcelain'],text=True))),
        command='python3 '+str((HERE/'g03_full_variation.py').relative_to(ROOT)),
        environment=dict(software=[platform.python_version(),'numpy '+np.__version__,'scipy '+scipy.__version__,'sympy '+sp.__version__],hardware=platform.platform()),
        mathematics=dict(assertion_tested='Full off-shell variations, exact electrovacuum branch, linearized constraints with heat stress',
                         coefficient_domain='exact SymPy and float64/complex128',conventions='(-+++), alpha=1, cylindrical R x S^2 domain extension',
                         inputs=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sources],
                         bounds=dict(clock_grids=[32,48],xi_alpha=.2,Lambda=.03,wavenumbers=[.2,.7,2,7,15],diffusion_nodes=64),
                         non_claims=['generic DOF count','no ghosts','causality clearance','PPN','Galactic background','T-A closure']),
        randomness=dict(used=False,generator='',seed=None),
        run=dict(started_at=datetime.fromtimestamp(started,timezone.utc).isoformat(),runtime_seconds=time.time()-started,exit_status=rc),
        outputs=[dict(path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest())],
        checks=records,result=payload['status'],residual_risks=payload['remaining'])
    (HERE/'full_variation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'{len(records)-len(failed)}/{len(records)} checks; status={payload["status"]}; rc={rc}')
    return rc


if __name__=='__main__':
    sys.exit(main())
