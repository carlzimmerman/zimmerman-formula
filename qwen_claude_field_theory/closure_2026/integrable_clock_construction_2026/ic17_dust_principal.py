#!/usr/bin/env python3
"""IC17 plus physical irrotational dust: bounded two-field principal audit."""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
import ic17_baryon_background as background


@lru_cache(None)
def identities():
    # An arbitrary second jet of P suffices for every Hessian below.
    v,t,v0,t0,z,lam,W=s.symbols('v t v0 t0 z lam W',positive=True)
    PS,Pw,PSS,B,C=s.symbols('PS Pw PSS B C',real=True)
    ds=-s.log(v/v0)
    jet=lambda dw:PS*ds+Pw*dw+PSS*ds**2/2+C*ds*dw+B*dw**2/2
    reduced=jet(s.log(t/t0))
    K=s.hessian(reduced,(v,t)).subs({v:v0,t:t0})
    expected=s.Matrix([[(PSS+PS)/v0**2,-C/(v0*t0)],
                       [-C/(v0*t0),(B-Pw)/t0**2]])
    raw=jet(W)+lam*(t*t-z*s.exp(2*W))/2
    point={v:v0,t:t0,W:0}
    Lvv=s.hessian(raw,(v,t)).subs(point)
    Lqq=s.hessian(raw,(W,lam)).subs(point)
    Lqv=s.Matrix([[s.diff(raw,q,x) for x in (v,t)] for q in (W,lam)]).subs(point)
    A=(Lqq-Lqv*Lvv.inv()*Lqv.T).subs(t0**2,z).subs(lam,Pw/z)
    target=s.Matrix([[B-2*Pw-C*C/(PSS+PS),-z],[-z,-z*z/Pw]])
    checks={f'velocity_hessian_{i}':s.simplify(x) for i,x in enumerate(K-expected)}
    checks.update({f'canonical_schur_{i}':s.simplify(x) for i,x in enumerate(A-target)})
    checks['auxiliary_determinant']=s.simplify(A.det()+z*z/Pw*(B-Pw-C*C/(PSS+PS)))
    # Covariant first derivatives give the spatial matrix at a comoving state.
    X,Y=s.symbols('X Y',positive=True)
    effective=jet(s.log(2*Y)/2-s.log(t0)).subs(v,s.sqrt(2*X))
    pointXY={X:v0*v0/2,Y:t0*t0/2}
    checks['gradient_clock']=s.simplify(s.diff(effective,X).subs(pointXY)+PS/v0**2)
    checks['gradient_dust']=s.simplify(s.diff(effective,Y).subs(pointXY)-Pw/t0**2)
    checks['covariant_XX']=s.simplify(s.diff(effective,X,2).subs(pointXY)-(PSS+2*PS)/v0**4)
    checks['covariant_XY']=s.simplify(s.diff(effective,X,Y).subs(pointXY)+C/(v0*v0*t0*t0))
    checks['covariant_YY']=s.simplify(s.diff(effective,Y,2).subs(pointXY)-(B-2*Pw)/t0**4)
    x,y,zcoord=s.symbols('x y zcoord',real=True)
    H=s.Function('H')(x)
    extrinsic=s.eye(3)*H
    checks['ADM_hamiltonian']=s.simplify(s.trace(extrinsic)**2-s.trace(extrinsic*extrinsic)-6*H*H)
    divergence=sum(s.diff(extrinsic[j,0],coord) for j,coord in enumerate((x,y,zcoord)))
    checks['ADM_momentum']=s.simplify(divergence-s.diff(s.trace(extrinsic),x)+2*s.diff(H,x))
    return checks


def state(S,k='.2'):
    bg=background.state(S,k)
    P,Pw,PS,B,C,PSS=background.action.build()['evaluate'](bg['S'],bg['w'],bg['epsilon'])
    X,z=bg['X'],mp.exp(2*bg['w'])
    Y=z/2
    lam=Pw/z
    K=mp.matrix([[(PSS+PS)/(2*X),-C/(2*mp.sqrt(X*Y))],
                 [-C/(2*mp.sqrt(X*Y)),(B-Pw)/(2*Y)]])
    D=mp.matrix([[-PS/(2*X),0],[0,Pw/(2*Y)]])
    KmD=K-D
    kminors=[K[0,0],mp.det(K)]
    margin=[KmD[0,0],mp.det(KmD)]
    positive=all(v>0 for v in kminors)
    if positive:
        inverse=mp.cholesky(K)**-1
        speeds=list(mp.eigsy(inverse*D*inverse.T,eigvals_only=True))
    else:
        speeds=list(mp.eig(K**-1*D,left=False,right=False))
    A=mp.matrix([[B-2*Pw-C*C/(PSS+PS),-z],[-z,-z/lam]])
    bracket=mp.zeros(4)
    for i in range(2):
        for j in range(2):
            bracket[i,j+2]=-A[i,j]
            bracket[i+2,j]=A[i,j]
    singular=list(mp.svd(bracket,compute_uv=False))
    rank=sum(value>mp.mpf('1e-45') for value in singular)
    determinant=-z/lam*(B-Pw-C*C/(PSS+PS))
    normalized_constraint=abs(bg['constraint'])/(1+abs(Pw))
    det_residual=abs(mp.det(A)-determinant)/(1+abs(determinant))
    admissible=bool(lam>0 and 0<bg['u']<1 and X>0 and Y>0 and bg['eta']==1
                    and bg['physical_H']>0 and positive and all(v>0 for v in margin)
                    and all(mp.im(v)==0 and 0<mp.re(v)<1 for v in speeds)
                    and rank==4 and normalized_constraint<mp.mpf('1e-45')
                    and det_residual<mp.mpf('1e-45'))
    return dict(S=bg['S'],k=bg['k'],w=bg['w'],u=bg['u'],X=X,Y=Y,lambda_dust=lam,
                eta=bg['eta'],physical_H=bg['physical_H'],K=K,D=D,
                K_principal_minors=kminors,K_minus_D_principal_minors=margin,
                speed_squared=speeds,auxiliary_A=A,auxiliary_determinant=mp.det(A),
                auxiliary_singular_values=singular,auxiliary_rank=rank,
                relative_constraint_residual=normalized_constraint,
                determinant_identity_residual=det_residual,admissible=admissible)


def compact(row):
    return {key:(value.tolist() if isinstance(value,mp.matrix) else value)
            for key,value in row.items()}


def relative_flow(S='.1',velocity='.1',k='.2'):
    """Frozen local state with fixed invariant X,Y; see local_constraint_witness."""
    velocity=mp.mpf(velocity)
    if abs(velocity)>=1:
        raise ValueError('Dust relative speed must have magnitude below one')
    bg=background.state(S,k)
    P,Pw,PS,B,C,PSS=background.action.build()['evaluate'](bg['S'],bg['w'],bg['epsilon'])
    X,Y=bg['X'],mp.exp(2*bg['w'])/2
    D=mp.diag([-PS/(2*X),Pw/(2*Y)])
    Hess=mp.matrix([[(PSS+2*PS)/(4*X*X),-C/(4*X*Y)],
                    [-C/(4*X*Y),(B-2*Pw)/(4*Y*Y)]])
    velocities=mp.matrix([mp.sqrt(2*X),mp.sqrt(2*Y/(1-velocity*velocity))])
    Ktime=D+mp.matrix([[Hess[i,j]*velocities[i]*velocities[j] for j in range(2)] for i in range(2)])
    def symbol(c):
        d=[velocities[0]*c,velocities[1]*(c-velocity)]
        return (1-c*c)*D-mp.matrix([[Hess[i,j]*d[i]*d[j] for j in range(2)] for i in range(2)])
    coefficients=list(reversed(mp.taylor(lambda c:mp.det(symbol(c)),0,4)))
    roots=mp.polyroots(coefficients,maxsteps=2000,extraprec=100,error=False)
    residual=max(abs(mp.det(symbol(c)))/(1+sum(abs(x)**2 for x in symbol(c))) for c in roots)
    complex_count=sum(abs(mp.im(c))>mp.mpf('1e-40') for c in roots)
    return dict(S=bg['S'],relative_velocity=velocity,invariant_X=X,invariant_Y=Y,
                roots=roots,polynomial_coefficients=coefficients,
                complex_root_count=complex_count,hyperbolic=complex_count==0,
                maximum_normalized_determinant_residual=residual,
                time_kinetic_principal_minors=[Ktime[0,0],mp.det(Ktime)],
                time_kinetic_positive=bool(Ktime[0,0]>0 and mp.det(Ktime)>0),
                full_constraint_background_established=False)


def local_constraint_witness(S='.1',velocity='.1',k='.2'):
    """Point and regularity data for a local ADM constraint ODE, not evolution."""
    v=mp.mpf(velocity)
    if abs(v)>=1:
        raise ValueError('Require subluminal physical dust relative velocity')
    bg=background.state(S,k)
    P,Pw,PS,B,C,PSS=background.action.build()['evaluate'](bg['S'],bg['w'],bg['epsilon'])
    X,z=bg['X'],mp.exp(2*bg['w'])
    Y=z/2
    gamma2=1/(1-v*v)
    PX,PY=-PS/(2*X),Pw/(2*Y)
    PXX,PXY=(PSS+2*PS)/(4*X*X),-C/(4*X*Y)
    rho=2*X*PX+2*Y*gamma2*PY-P
    j=2*Y*gamma2*v*PY  # T_ni, without the alternative minus sign in ADM j_i.
    rhoX=PX+2*X*PXX+2*Y*gamma2*PXY
    mstar=mp.exp(-mp.mpf(1)/6)
    H=mp.sqrt(rho/(3*mstar))
    Hprime=-j/(2*mstar)
    Xprime=6*mstar*H*Hprime/rhoX
    r=mp.exp(bg['S']-2*bg['w']-mp.mpf(1)/6)*H
    lam=Pw/z
    regular=bool(rho>0 and rhoX!=0 and X>0 and 0<bg['u']<1
                 and Y>0 and lam>0 and r*r>mp.mpf(3)/4)
    return dict(S=bg['S'],relative_velocity=v,rho=rho,rho_X=rhoX,T_ni=j,
                H=H,Hprime=Hprime,Xprime=Xprime,activation_r_squared=r*r,
                lambda_dust=lam,local_patch_regular=regular,
                hamiltonian_residual=6*H*H-2*rho/mstar,
                momentum_residual=-2*Hprime-j/mstar,
                differentiated_hamiltonian_residual=6*mstar*H*Hprime-rhoX*Xprime,
                global_constraint_solution_established=False,
                evolution_solution_established=False)


def report(samples=51):
    if samples<2:
        raise ValueError('Require at least two samples')
    mp.mp.dps=70
    rows=[state(mp.exp(mp.log(mp.mpf('1e-8'))+
                      (mp.log(mp.mpf('.1'))-mp.log(mp.mpf('1e-8')))*i/(samples-1)))
          for i in range(samples)]
    aligned,boosted=relative_flow(velocity='0'),relative_flow()
    local=local_constraint_witness()
    checks={key:value==0 for key,value in identities().items()}
    checks.update(aligned_roots_real=aligned['complex_root_count']==0,
                  relative_flow_counterexample_reproduced=boosted['complex_root_count']==2,
                  relative_flow_positive_time_kinetic=boosted['time_kinetic_positive'],
                  characteristic_residuals=all(row['maximum_normalized_determinant_residual']<mp.mpf('1e-55')
                                               for row in (aligned,boosted)),
                  local_constraint_patch_regular=local['local_patch_regular'],
                  local_constraint_residuals=all(abs(local[key])<mp.mpf('1e-55') for key in
                      ('hamiltonian_residual','momentum_residual','differentiated_hamiltonian_residual')))
    return dict(candidate='Same IC17 action with covariant physical irrotational dust',
                full_theory='OPEN',precision_digits=70,k='.2',epsilon=background.action.EPSILON,
                matter_cone_status='FAIL at a relative-flow principal point admitting a regular local ADM constraint patch',
                checks=checks,relative_flow_controls=[aligned,boosted],local_constraint_patch=local,
                scan=dict(samples=samples,S_min='1e-8',S_max='.1',interval_certified=False,
                          failed_samples=sum(not row['admissible'] for row in rows),
                          minimum_speed_squared=min(min(row['speed_squared']) for row in rows),
                          maximum_speed_squared=max(max(row['speed_squared']) for row in rows),
                          minimum_K_determinant=min(row['K_principal_minors'][1] for row in rows),
                          minimum_K_minus_D_determinant=min(row['K_minus_D_principal_minors'][1] for row in rows),
                          computed_auxiliary_ranks=sorted(set(row['auxiliary_rank'] for row in rows)),
                          rows=list(map(compact,rows))),
                nonclaims=['Comoving homogeneous two-scalar principal symbol, not a global spatial Dirac analysis',
                           'Local ADM constraint patch is not a global initial-data or evolution solution',
                           'No radiation, vorticity, dust caustics, or non-comoving cone certificate',
                           'No interval theorem, transition, strong-coupling, MOND, or complete cosmology closure'])


def completion_status(result,require_full_closure=False):
    if not result['checks'] or not all(result['checks'].values()) or result['scan']['failed_samples']:
        return 1
    return 2 if require_full_closure else 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args()
    result=report()
    print(json.dumps(result,indent=2,default=lambda x:mp.nstr(x,30)))
    return completion_status(result,args.require_full_closure)


if __name__=='__main__':
    raise SystemExit(main())
