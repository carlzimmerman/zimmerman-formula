#!/usr/bin/env python3
"""C-H compact de Sitter diagnostic; no nonlinear/PPN closure certificate.

All ranks/counts are calculated. The reduced zero-field action requires the
directional variational argument in REPORT.md; finite minimizations check it.
"""
import argparse
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import time

import numpy as np
import scipy
from scipy.optimize import minimize
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
KERNEL_PATH = HERE.parent/'two_body_frequency_2026'/'binary_frequency.py'
spec = importlib.util.spec_from_file_location('binary_kernel', KERNEL_PATH)
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)


@lru_cache(None)
def background_check():
    t = sp.symbols('t', real=True)
    H,Lambda = sp.symbols('H Lambda',positive=True)
    A,N = sp.Function('A')(t),sp.Function('N')(t)
    L = -6*A*sp.diff(A,t)**2/N-2*Lambda*N*A**3
    en = sp.diff(L,N)
    ea = sp.diff(L,A)-sp.diff(sp.diff(L,sp.diff(A,t)),t)
    subs = {N:1,sp.diff(N,t):0,A:sp.exp(H*t),
            sp.diff(A,t):H*sp.exp(H*t),sp.diff(A,t,2):H**2*sp.exp(H*t)}
    rows = [sp.simplify(e.subs(subs).subs(Lambda,3*H**2)) for e in (en,ea)]
    y=sp.symbols('y',positive=True)
    s=y*(1-sp.exp(-y))
    q=2-2*(1+y)*sp.exp(-y)-y*y*sp.exp(-2*y)
    return dict(lapse_equation=en,scale_equation=ea,residuals=rows,
                aux_first_variation_limit=sp.limit(y*sp.exp(-y),y,0,dir='+'),
                aux_tangent_limit=sp.limit(y/s-1,y,0,dir='+'),
                q_power_limit=sp.limit(q/s**sp.Rational(3,2),y,0,dir='+'),
                wrong_hubble_residual=sp.simplify(en.subs(subs).subs(Lambda,H**2)))


@lru_cache(None)
def scalar_action():
    A,H,k = sp.symbols('A H k',positive=True)
    z,n,b,d = sp.symbols('zeta n b zeta_dot',real=True)
    ep,C,S = sp.symbols('eps cosine sine',real=True)
    # h_ij=A^2 exp(2 eps z cos(kx)) delta_ij; N=exp(eps n cos(kx));
    # N^x=eps b sin(kx). K^i_j=diag(q-B,q,q)/N.
    q = H+ep*d*C+ep**2*k*b*z*S**2
    B = ep*k*b*C
    extrinsic = A**3*sp.exp(ep*(3*z-n)*C)*(-6*q*q+4*q*B)
    curvature = A*sp.exp(ep*(z+n)*C)*(4*ep*k*k*z*C-2*ep**2*k*k*z*z*S**2)
    cosmological = -6*H**2*A**3*sp.exp(ep*(3*z+n)*C)
    # This is derived by eliminating U at zero field, not q''(0)=constant.
    auxiliary = 2*A*sp.exp(ep*(z+n)*C)*ep**2*k*k*n*n*S**2
    coeff = sp.expand(sp.diff(extrinsic+curvature+cosmological+auxiliary,ep,2).subs(ep,0)/2)
    raw = sp.simplify(coeff.subs({C**2:sp.Rational(1,2),S**2:sp.Rational(1,2)}))
    boundary = -9*H*A**3*z*z
    boundary_dt = sp.diff(boundary,A)*H*A+sp.diff(boundary,z)*d
    L = sp.factor(raw-boundary_dt)
    aux_coeff=sp.expand(sp.diff(auxiliary,ep,2).subs(ep,0)/2).subs(S*S,sp.Rational(1,2))
    return dict(A=A,H=H,k=k,z=z,n=n,b=b,d=d,raw=raw,boundary_dt=boundary_dt,L=L,aux_L=aux_coeff)


def poisson(f,g,coords,momenta):
    return sp.simplify(sum(sp.diff(f,q)*sp.diff(g,p)-sp.diff(f,p)*sp.diff(g,q)
                           for q,p in zip(coords,momenta)))


@lru_cache(None)
def dirac_sector():
    r=scalar_action()
    A,H,k,z,n,b,d=[r[key] for key in ('A','H','k','z','n','b','d')]
    E,ed,nd,bd=sp.symbols('E E_dot n_dot b_dot',real=True)
    p,pn,pb,pE=sp.symbols('p_zeta p_n p_b p_E',real=True)
    ln,lb=sp.symbols('lambda_n lambda_b',real=True)
    # Spatial pullback x -> x+eps E(t) sin(kx) restores the scalar coordinate
    # degree of freedom: b -> b-E_dot. No spatial gauge constraint is dropped.
    L=r['L'].subs(b,b-ed)
    coords=[z,n,b,E]; momenta=[p,pn,pb,pE]; velocities=[d,nd,bd,ed]
    vh=sp.hessian(L,velocities)
    primary=[mom-sp.diff(L,vel) for mom,vel in zip(momenta,velocities)
             if sp.diff(L,vel)==0]
    legendre=sp.solve([p-sp.diff(L,d),pE-sp.diff(L,ed)],[d,ed],dict=True)[0]
    hc=sp.factor((p*d+pE*ed-L).subs(legendre))
    secondary=[poisson(c,hc,coords,momenta) for c in primary]
    constraints=primary+secondary
    surface=sp.solve(secondary,[n,pE],dict=True)[0]
    surface.update({pn:0,pb:0})
    pbmat=sp.Matrix([[poisson(f,g,coords,momenta).subs(surface)
                      for g in constraints] for f in constraints])
    second=int(pbmat.rank()); first=len(constraints)-second
    total=hc+ln*pn+lb*pb
    preservation=[sp.simplify((sp.diff(c,A)*H*A+poisson(c,total,coords,momenta)).subs(surface))
                  for c in constraints]
    mult=sp.solve(preservation,[ln,lb],dict=True)[0]
    residuals=[sp.simplify(v.subs(mult)) for v in preservation]
    # Independent elimination in the Lagrangian, and a second time boundary.
    on_constraints=sp.simplify(r['L'].subs(n,d/H))
    F=A*k*k*z*z/H
    Fdt=sp.diff(F,A)*H*A+sp.diff(F,z)*d
    reduced=sp.factor(on_constraints-Fdt)
    dd=sp.symbols('zeta_ddot',real=True)
    kin=sp.hessian(reduced,[d])
    el=sp.simplify(sp.diff(sp.diff(reduced,d),A)*H*A+
                   sp.diff(sp.diff(reduced,d),d)*dd-sp.diff(reduced,z))
    # Average cos^2=1/2 and epsilon=-H_aux/2 cancel their two factors here.
    charge=sp.simplify((-sp.diff(r['aux_L'],n)/A**3).subs(n,d/H))
    charge_conservation=sp.diff(charge,A)*H*A+sp.diff(charge,d)*dd+3*H*charge
    return dict(parameters=[A,H,k],velocity_hessian=vh,velocity_rank=int(vh.rank()),
                Hamiltonian=hc,primary=primary,secondary=secondary,constraints=constraints,
                PB=pbmat,second_class=second,first_class=first,
                dof=sp.Rational(2*len(coords)-2*first-second,2),
                multipliers=mult,preservation_residuals=residuals,
                reduced_action=reduced,reduced_kinetic_hessian=kin,
                gr_reduced_action=sp.simplify(reduced-r['aux_L'].subs(n,d/H)),
                reduced_eom_residual=sp.simplify(el/kin[0,0]-(dd+H*d)),
                clock_density=charge,
                clock_conservation_residual=sp.simplify(charge_conservation.subs(dd,-H*d)),
                spatial_gauge='E->E+eta, b->b+eta_dot; clock tau=t')


@lru_cache(None)
def homogeneous_sector():
    A,H=sp.symbols('A H',positive=True)
    z,n,d,p,pn=sp.symbols('zeta n zeta_dot p_zeta p_n',real=True)
    L=-6*A**3*(d-H*n)**2  # constant mode: no cosine-average factor of 1/2.
    velocity=sp.solve(p-sp.diff(L,d),d)[0]
    hc=sp.factor((p*d-L).subs(d,velocity))
    primary=pn
    secondary=poisson(primary,hc,[z,n],[p,pn])
    cs=[primary,secondary]
    matrix=sp.Matrix([[poisson(f,g,[z,n],[p,pn]) for g in cs] for f in cs])
    residual=[sp.simplify((sp.diff(c,A)*H*A+poisson(c,hc,[z,n],[p,pn])).subs({p:0,pn:0})) for c in cs]
    sc=int(matrix.rank()); fc=len(cs)-sc
    lapse_solution=sp.solve(sp.diff(L,n),n)[0]
    return dict(Hamiltonian=hc,constraints=cs,PB=matrix,first_class=fc,second_class=sc,
                reduced_action=sp.simplify(L.subs(n,lapse_solution)),
                dof=sp.Rational(4-2*fc-sc,2),preservation_residuals=residual,velocity=d)


@lru_cache(None)
def vector_sector():
    A,k=sp.symbols('A k',positive=True)
    E,b,ed,p,pb=sp.symbols('E_v b_v E_v_dot p_Ev p_bv',real=True)
    # One transverse polarization: averaged off-diagonal K_ij K^ij.
    kmat=sp.Matrix([[0,0,k*(b-ed)/2],[0,0,0],[k*(b-ed)/2,0,0]])
    L=sp.simplify(A**3*sp.trace(kmat*kmat)/2)
    vel=sp.solve(p-sp.diff(L,ed),ed)[0]
    hc=sp.factor((p*ed-L).subs(ed,vel))
    cs=[pb,poisson(pb,hc,[E,b],[p,pb])]
    matrix=sp.Matrix([[poisson(f,g,[E,b],[p,pb]) for g in cs] for f in cs])
    sc=int(matrix.rank()); fc=len(cs)-sc
    shift_solution=sp.solve(sp.diff(L,b),b)[0]
    return dict(L=L,Hamiltonian=hc,constraints=cs,PB=matrix,first_class=fc,second_class=sc,
                reduced_action=sp.simplify(L.subs(b,shift_solution)),
                dof=sp.Rational(4-2*fc-sc,2),velocity=ed,
                preservation_residuals=[poisson(c,hc,[E,b],[p,pb]).subs({p:0,pb:0}) for c in cs])


@lru_cache(None)
def tensor_sector():
    A,H,k=sp.symbols('A H k',positive=True)
    x1,x2,x3=sp.symbols('x1 x2 x3',real=True)
    w=sp.Function('w')(x3)
    coords=[x1,x2,x3]
    h=sp.diag(A*A*sp.exp(w),A*A*sp.exp(-w),A*A)
    hi=h.inv()
    gam=[[[sp.simplify(sum(hi[i,l]*(sp.diff(h[l,j],coords[m])+sp.diff(h[l,m],coords[j])-
             sp.diff(h[j,m],coords[l])) for l in range(3))/2) for m in range(3)] for j in range(3)] for i in range(3)]
    ric=sp.Matrix(3,3,lambda i,j:sum(sp.diff(gam[l][i][j],coords[l])-sp.diff(gam[l][i][l],coords[j])+
              sum(gam[l][l][m]*gam[m][i][j]-gam[l][j][m]*gam[m][i][l] for m in range(3)) for l in range(3)))
    R=sp.simplify(sum(hi[i,j]*ric[i,j] for i in range(3) for j in range(3)))
    hmode,hd,C=sp.symbols('h h_dot cosine',real=True)
    K=sp.diag(H+hd*C/2,H-hd*C/2,H)
    kinetic=sp.expand(A**3*(sp.trace(K*K)-sp.trace(K)**2+6*H*H)).subs(C*C,sp.Rational(1,2))
    gradient=sp.simplify(A**3*R.subs(sp.diff(w,x3)**2,k*k*hmode*hmode/2))
    coeff=sp.diff(kinetic,hd,2)/2
    speed=sp.simplify(-sp.diff(gradient,hmode,2)/2/coeff*A*A/(k*k))
    h11,h22,h33,h12,h13,h23=sp.symbols('h11 h22 h33 h12 h13 h23')
    tt_conditions=sp.Matrix([k*h13,k*h23,k*h33,h11+h22+h33])
    rank=tt_conditions.jacobian([h11,h22,h33,h12,h13,h23]).rank()
    return dict(spatial_R=R,L=kinetic+gradient,kinetic=coeff,speed_squared=speed,
                tensor_polarizations=len([h11,h22,h33,h12,h13,h23])-rank)


def auxiliary_problem(amplitude,width,modes,npoints):
    x=(np.arange(npoints)+.5)*2*np.pi/npoints
    j=np.arange(1,modes+1)
    D=-j[None,:]*np.sin(x[:,None]*j[None,:])
    SD=D*np.exp(-.5*width*width*j*j)[None,:]
    lapse=np.exp(amplitude*np.cos(x)); acc=-amplitude*np.sin(x)
    baseline=float(np.mean(lapse*2*acc*acc))
    def value_gradient(v):
        u=amplitude*amplitude*(D@v)
        w=amplitude*amplitude*(SD@v)
        q=kernel.dual_q_array(np.abs(w))
        f=kernel.flux(w[:,None])[:,0]
        correction=np.mean(lapse*(2*u*u-4*u*acc+2*q))/amplitude**3
        grad=4/amplitude*np.mean(lapse[:,None]*((u-acc)[:,None]*D+f[:,None]*SD),axis=0)
        return float(correction),grad
    return value_gradient,baseline


def auxiliary_gradient_check():
    f,_=auxiliary_problem(.01,.3,4,192)
    v=np.array([.3,-.07,.05,.03]); direction=np.array([.2,.6,-.1,.4])
    h=1e-6
    analytic=float(f(v)[1]@direction)
    difference=(f(v+h*direction)[0]-f(v-h*direction)[0])/(2*h)
    return dict(analytic=analytic,finite_difference=difference,
                relative_error=abs(analytic-difference)/max(abs(analytic),abs(difference),1e-12))


def auxiliary_minimum(amplitude,width,modes,npoints):
    f,baseline=auxiliary_problem(amplitude,width,modes,npoints)
    result=minimize(f,np.zeros(modes),jac=True,method='BFGS',
                    options=dict(gtol=1e-9,maxiter=1500))
    value,grad=f(result.x)
    return dict(amplitude=amplitude,width=width,modes=modes,npoints=npoints,
                optimizer_success=bool(result.success),optimizer_message=str(result.message),
                iterations=int(result.nit),scaled_gradient_norm=float(np.linalg.norm(grad)),
                value_ratio=float(1+amplitude**3*value/baseline),
                scaled_U_coefficients=result.x.tolist())


def plain(value):
    if isinstance(value,dict): return {str(k):plain(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [plain(v) for v in value]
    if isinstance(value,sp.MatrixBase): return [[str(v) for v in row] for row in value.tolist()]
    if isinstance(value,sp.Basic): return str(value)
    return value


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=HERE)
    parser.add_argument('--require-closed',action='store_true')
    args=parser.parse_args()
    start=time.time(); checks=[]
    def check(name,passed):
        checks.append(dict(name=name,passed=bool(passed)))
        print(f'[{"PASS" if passed else "FAIL"}] {name}',flush=True)
    bg=background_check(); scalar=scalar_action(); dc=dirac_sector()
    zero=homogeneous_sector(); vector=vector_sector(); tensor=tensor_sector()
    check('varied compact expanding vacuum background',all(v==0 for v in bg['residuals']) and bg['wrong_hubble_residual']!=0)
    check('zero-field kernel has vanishing first derivative but divergent tangent',
          bg['aux_first_variation_limit']==0 and bg['aux_tangent_limit']==sp.oo and bg['q_power_limit']==sp.Rational(4,3))
    check('scalar ADM expansion with time boundaries',sp.simplify(scalar['raw']-scalar['boundary_dt']-scalar['L'])==0)
    check('Dirac preservation closes with computed multipliers',all(v==0 for v in dc['preservation_residuals']))
    check('Dirac count agrees with independently reduced kinetic rank',dc['dof']==dc['reduced_kinetic_hessian'].rank())
    check('removing the auxiliary term recovers the empty GR scalar action',dc['gr_reduced_action']==0)
    check('positive reduced kinetic coefficient and dust-like clock evolution',
          dc['reduced_kinetic_hessian'][0,0].is_positive and dc['reduced_eom_residual']==0 and dc['clock_conservation_residual']==0)
    check('homogeneous and vector chains preserve separately',
          all(v==0 for v in zero['preservation_residuals']+vector['preservation_residuals']))
    check('tensor speed and kinetic energy from ADM curvature',tensor['speed_squared']==1 and tensor['kinetic'].is_positive)
    gradient=auxiliary_gradient_check()
    check('nonlinear auxiliary functional differentiated independently',gradient['relative_error']<2e-6)
    rows=[auxiliary_minimum(eps,width,modes,192) for width in (.2,.5)
          for modes in (4,8) for eps in (.02,.01,.005,.0025)]
    check('nonlinear auxiliary solves have resolved stationary residuals',
          all(r['scaled_gradient_norm']<2e-5 and 0<r['value_ratio']<1 for r in rows))
    check('fixed-direction zero-field limit approaches lapse-gradient action',
          all(rows[i+3]['value_ratio']>rows[i+2]['value_ratio']>rows[i+1]['value_ratio']>rows[i]['value_ratio'] for i in range(0,len(rows),4)))
    refined=auxiliary_minimum(.005,.2,4,384)
    comparison=next(r for r in rows if r['amplitude']==.005 and r['width']==.2 and r['modes']==4)
    check('auxiliary quadrature refinement',abs(refined['value_ratio']-comparison['value_ratio'])<2e-5)
    data=dict(background=plain(bg),scalar_ADM=plain(scalar),dirac=plain(dc),
              homogeneous=plain(zero),vector=plain(vector),tensor=plain(tensor),
              auxiliary_gradient=gradient,auxiliary_runs=rows,auxiliary_refinement=refined,
              checks=checks,theory_status='OPEN',
              scope='Compact de Sitter, fixed smooth zero-field directions, reduced quadratic action. No nonlinear Dirac or generic-health certificate.')
    args.output_dir.mkdir(parents=True,exist_ok=True)
    result=args.output_dir/'results.json'
    result.write_text(json.dumps(data,indent=2)+'\n')
    failed=any(not r['passed'] for r in checks)
    rc=1 if failed else (2 if args.require_closed else 0)
    sources=[HERE/'flrw_gate.py',HERE/'test_flrw_gate.py',HERE/'CONTRACT.md',HERE/'REPORT.md',KERNEL_PATH,
             HERE.parent/'g03_covariant_action_2026'/'ACTION.md',
             HERE.parent/'g03_covariant_action_2026'/'FULL_VARIATION.md']
    manifest=dict(schema_version=1,claim_id='C-H-compact-de-Sitter-reduced-scalar',
        repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                        dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True))),
        command='python3 -B '+str((HERE/'flrw_gate.py').relative_to(ROOT))+(' --require-closed' if args.require_closed else '')+
                (' --output-dir <output-directory>' if args.output_dir!=HERE else ''),
        environment=dict(software=[platform.python_version(),'numpy '+np.__version__,'scipy '+scipy.__version__,'sympy '+sp.__version__],hardware=platform.machine()),
        mathematics=dict(assertion_tested=data['scope'],coefficient_domain='exact SymPy; float64 nonlinear minimization',
            conventions='c=1, positive overall action prefactor suppressed; H>0, A>0, k>0 unless homogeneous',
            inputs=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sources],
            bounds=dict(widths=[.2,.5],modes=[4,8],nodes=[192,384],amplitudes=[.02,.01,.005,.0025]),
            non_claims=['full nonlinear Dirac count','uniform joint zero-field/high-k limit','nonlinear clock health','PPN','strict AQUAL completion','empirical discovery']),
        randomness=dict(used=False,generator='',seed=None),
        run=dict(started_at=datetime.fromtimestamp(start,timezone.utc).isoformat(),runtime_seconds=time.time()-start,exit_status=rc),
        outputs=[dict(path=str(result.relative_to(ROOT)) if result.is_relative_to(ROOT) else result.name,
                      sha256=hashlib.sha256(result.read_bytes()).hexdigest())],
        checks=checks,result='OPEN' if not failed else 'FAILED_DIAGNOSTIC',
        residual_risks=['directional quadratic limit does not prove nonlinear well-posedness','clock scalar must be explicitly counted'])
    (args.output_dir/'computation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('computed scalar DOF:',dc['dof'],'; FC:',dc['first_class'],'; SC:',dc['second_class'])
    print('G03=OPEN; exit',rc)
    return rc


if __name__=='__main__':
    raise SystemExit(main())
