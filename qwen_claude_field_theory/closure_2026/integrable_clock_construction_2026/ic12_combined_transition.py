#!/usr/bin/env python3
"""Combined activated convex pressure and IC11 spatial/tensor correction.

Actual homogeneous roots and all activation jets are recomputed. No matter
reshaping is included and full closure remains open regardless of the scan.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
import ic10_transition as original
import ic11_clock_pressure as pressure
import ic11_transition_completion as spatial


@lru_cache(None)
def build():
    old=original.build()
    rho,xi,u=variables=old['variables']
    S=(2-u)*xi
    B=s.Rational(5,64)*s.exp(-31*S)
    delta=old['delta']-B
    data=[]
    for expression in (old['base'],delta,old['r']):
        data.extend([expression]+[s.diff(expression,x) for x in variables]+list(s.hessian(expression,variables)))
    return dict(evaluate=s.lambdify(variables,s.Matrix(data+[old['E'],old['J'],old['Z'],B]),'mpmath',cse=True),
                raw=s.lambdify(variables,(old['base'],delta,old['r']),'mpmath',cse=True))


def raw_density(rho,xi,u):
    base,delta,r=build()['raw'](rho,xi,u)
    return base+original.activation_value(r)*delta


def jets(point):
    values=build()['evaluate'](*point)
    parts=[]
    for offset in (0,13,26):
        parts.append((values[offset],mp.matrix(values[offset+1:offset+4]),
                      mp.matrix([[values[offset+4+3*i+j] for j in range(3)] for i in range(3)])))
    (h0,g0,H0),(delta,gd,Hd),(r,gr,Hr)=parts
    eta,eta1,eta2=original.activation(r)
    h=h0+eta*delta
    gradient=g0+eta*gd+eta1*delta*gr
    Hessian=H0+eta*Hd+eta1*(gr*gd.T+gd*gr.T+delta*Hr)+eta2*delta*gr*gr.T
    E,J,Z,B=values[39:43]
    return dict(point=list(point),h=h,gradient=gradient,hessian=Hessian,auxiliary=Hessian[1:3,1:3],
                eta=eta,eta1=eta1,eta2=eta2,r=r,E=E,J=J,Z=Z,B=B,
                A=1+eta*(1/J-1),C=1+eta*(J-1)+original.activation_complement(r)*Z)


def at_point(point):
    bg=jets(list(map(mp.mpf,point)))
    rho,xi,u=bg['point']
    h,g,H,M=bg['h'],bg['gradient'],bg['hessian'],bg['auxiliary']
    rhodot,logVdot=-3*h/2,3*g[0]/2
    qdot=-(M**-1)*(H[1:3,0]*rhodot+logVdot*g[1:3,:])
    wdot=(u-1)*qdot[0]+xi*qdot[1]
    Dirac=mp.matrix(4,4)
    Dirac[:2,2:4],Dirac[2:4,:2]=-M,M
    omega=mp.mpf(3)/2*(g[1]*H[0,2]-H[0,1]*g[2])
    Dirac[2,3],Dirac[3,2]=omega,-omega
    singular_values=list(mp.svd(Dirac,compute_uv=False))
    bg.update(rhodot=rhodot,logVdot=logVdot,qdot=qdot,
              physical_H=mp.exp(-xi)*(g[0]/2+wdot),dirac_matrix=Dirac,
              dirac_singular_values=singular_values,
              dirac_rank=sum(v>mp.mpf('1e-35')*max(singular_values) for v in singular_values),
              preservation_residual=logVdot*g[1:3,:]+H[1:3,0]*rhodot+M*qdot)
    corrected=spatial.at_background(bg)
    # B=exp(S) f(S) has no rho dependence at fixed (xi,u).
    identity=(-bg['E']*(1/bg['J']-1)*(4*bg['r']*bg['eta1']+bg['r']**2*bg['eta2'])/12
              -bg['B']*bg['E']**2*bg['eta2']/36)
    bg.update(G=corrected['G'],W=corrected['W'],
              tensor_speed_squared=corrected['tensor_speed_squared'],
              positive_auxiliary_poles=corrected['positive_auxiliary_poles'],
              scalar_UV_kinetic=corrected['scalar_UV_kinetic'],scalar_UV_identity=identity)
    return bg


def continuation(last_step=500,start_S='.2'):
    S=mp.mpf(start_S)
    start=pressure.state(S)
    if not start['admissible']:
        raise ValueError('Initial pressure state is outside its healthy activation plateau')
    rho0=-3*mp.exp(-mp.mpf(1)/6)*start['H']
    seed=[S+start['w'],start['u']]
    states=[]
    for step in range(last_step+1):
        rho=rho0+mp.mpf(step)/1000
        try:
            equations=lambda xi,u: tuple(jets([rho,xi,u])['gradient'][1:3,:])
            jacobian=lambda xi,u: jets([rho,xi,u])['auxiliary']
            xi,u=mp.findroot(equations,tuple(seed),J=jacobian,tol=mp.power(10,-mp.mp.dps+10))
            if not 0<u<1:
                raise ValueError('Root left the allowed 0<u<1 chart')
            bg=at_point([rho,xi,u])
            bg['step']=step
            states.append(bg)
            seed=[xi,u]
        except (ValueError,ZeroDivisionError) as error:
            return states,dict(step=step,rho=mp.nstr(rho,30),error=str(error))
    return states,None


def report():
    mp.mp.dps=60
    states,failure=continuation()
    nstr=lambda x:mp.nstr(x,24)
    rows=[]
    for bg in states:
        rows.append(dict(step=bg['step'],point=list(map(nstr,bg['point'])),
                         **{key:nstr(bg[key]) for key in ('eta','r','h','rhodot','physical_H','tensor_speed_squared','scalar_UV_kinetic')},
                         auxiliary_eigenvalues=list(map(nstr,mp.eigsy(bg['auxiliary'],eigvals_only=True))),
                         auxiliary_matrix=[[nstr(bg['auxiliary'][i,j]) for j in range(2)] for i in range(2)],
                         dirac_matrix=[[nstr(bg['dirac_matrix'][i,j]) for j in range(4)] for i in range(4)],
                         dirac_singular_values=list(map(nstr,bg['dirac_singular_values'])),dirac_rank=bg['dirac_rank'],
                         minimum_W_eigenvalue=nstr(min(mp.eigsy(bg['W'],eigvals_only=True))),
                         positive_auxiliary_k_squared_poles=list(map(nstr,bg['positive_auxiliary_poles'])),
                         scalar_UV_identity_residual=nstr(abs(bg['scalar_UV_kinetic']-bg['scalar_UV_identity'])),
                         constraint_residual=nstr(mp.norm(bg['gradient'][1:3,:])),
                         preservation_residual=nstr(mp.norm(bg['preservation_residual']))))
    negative=[bg['step'] for bg in states if bg['scalar_UV_kinetic'] < -mp.mpf('1e-30')]
    return dict(candidate='IC12 combined activated convex pressure plus tensor/auxiliary repair',
                full_theory='OPEN',start_S='.2',rho_step='.001',requested_last_step=500,
                root_failure=failure,first_negative_UV_step=negative[0] if negative else None,
                continuation=rows,
                nonclaims=['Finite vacuum family, no interval certification',
                           'Homogeneous Dirac rank is not a full field-theory degree-of-freedom count',
                           'No balanced matter reshaping or matter-coupled characteristic analysis'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args()
    print(json.dumps(report(),indent=2))
    raise SystemExit(2 if args.require_full_closure else 0)
