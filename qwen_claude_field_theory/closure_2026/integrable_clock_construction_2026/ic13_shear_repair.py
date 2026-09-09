#!/usr/bin/env python3
"""Constructive shear kinetic repair and actual scalar quadratic screen."""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import ic10_transition as activation
import ic12_combined_transition as combined


def coefficients(point):
    bg=combined.jets(point)
    r,eta=bg['r'],bg['eta']
    complement=activation.activation_complement(r)
    d=eta*complement
    if d==0:
        v=mp.mpf(0)
    else:
        distance=(r*r-1)**2
        left,right=mp.mpf(1)/4-distance,distance-mp.mpf(1)/16
        dd,ddd=4*r*(r*r-1),12*r*r-4
        L1=(1/left**2+1/right**2)*dd
        L2=(2/left**3-2/right**3)*dd**2+(1/left**2+1/right**2)*ddd
        T=(1-2*eta)*L1**2-L2
        v=bg['E']*(1/bg['J']-1)*(4*r*L1-r*r*T)/12-bg['B']*bg['E']**2*T/36
    shift=6/bg['E']*d*(1+v*v)
    As=bg['A']+shift
    return dict(E=bg['E'],A=bg['A'],As=As,deltaA=shift,d=d,v=v,
                old_UV=d*v,new_UV=d*(1+v+v*v),c=mp.exp(point[2]*point[1])/As)


@lru_cache(None)
def witness():
    return combined.continuation(220)[0][-1]


def raw_homogeneous(volume,l1,l2,l3,xi,u):
    V=mp.exp(volume)
    rho=(l1+l2+l3)/V
    tf2=l1*l1+l2*l2+l3*l3-(l1+l2+l3)**2/3
    c=coefficients([rho,xi,u])
    return V*combined.raw_density(rho,xi,u)+2*c['E']*c['As']*tf2/V


def homogeneous_hessian(point,volume=0):
    bg=combined.jets(point)
    rho=point[0]
    V=mp.exp(volume)
    h,g,H=bg['h'],bg['gradient'],bg['hessian']
    c=coefficients(point)
    K=2*c['E']*c['As']
    result=mp.matrix(6,6)
    result[0,0]=V*(h-rho*g[0]+rho*rho*H[0,0])
    for i in range(3):
        result[0,i+1]=result[i+1,0]=-rho*H[0,0]
        for j in range(3):
            result[i+1,j+1]=(H[0,0]+2*K*(int(i==j)-mp.mpf(1)/3))/V
        for j in range(2):
            result[i+1,j+4]=result[j+4,i+1]=H[0,j+1]
    for i in range(2):
        result[0,i+4]=result[i+4,0]=V*(g[i+1]-rho*H[0,i+1])
        for j in range(2):
            result[i+4,j+4]=V*H[i+1,j+1]
    return result


def curvature_derivatives(point):
    f=lambda rho,xi,u:coefficients([rho,xi,u])['c']
    return [f(*point)]+[mp.diff(f,tuple(point),tuple(int(k==i) for k in range(3))) for i in range(3)]


def pencil(bg,k,curvature_square=False,volume=0,zscale=0):
    point=bg['point']
    rho,xi,u=point
    V=mp.exp(volume)
    transform=mp.matrix(6,4)
    # Columns (zeta,p_zeta,delta xi,delta u); actual shift equation first.
    transform[0,0]=2
    transform[1,1]=transform[2,1]=mp.mpf(1)/4
    transform[3,0]=2*rho*V/3
    transform[4,2]=transform[5,3]=1
    H0=transform.T*homogeneous_hessian(point,volume)*transform
    c,cr,cxi,cu=curvature_derivatives(point)
    factor=V*mp.exp(-2*zscale)
    deltaC=mp.matrix([factor*(2*c-4*rho*cr/3),factor*cr/(2*V),factor*cxi,factor*cu])
    G=mp.matrix(4,4)
    G[0,0]=6*factor*c
    for i in range(4):
        G[0,i]-=2*deltaC[i]
        G[i,0]-=2*deltaC[i]
    W=activation.spatial_gradient(point)['W']
    eta=activation.activation(-rho*mp.exp((4-3*u)*xi)/3)[0]
    W+=eta*(1+sum(W[i,j]**2 for i in range(2) for j in range(2)))*mp.eye(2)
    complement=activation.activation_complement(-rho*mp.exp((4-3*u)*xi)/3)
    G[2:4,2:4]=-2*factor*complement*mp.exp(u*xi)*W
    total=H0+k*k*G
    dR=mp.mpf(0)
    if curvature_square:
        a=coefficients(point)['new_UV']
        if a<=0:
            raise ValueError('Curvature-square chart requires strictly positive full-rank UV kinetic')
        dR=cr*cr/(32*a)
        total[0,0]+=32*V*mp.exp(-4*zscale)*dR*k**4
    Q=total[2:4,2:4]
    mix=total[:2,2:4]
    response=-(Q**-1)*mix.T
    reduced=total[:2,:2]+mix*response
    omega2=mp.det(reduced)
    return dict(total=total,reduced=reduced,auxiliary=Q,auxiliary_EL_residual=Q*response+mix.T,
                curvature_rho=cr,curvature_square_coefficient=dR,
                frozen_omega_squared=omega2,
                frozen_growth=mp.sqrt(-omega2) if omega2<0 else mp.mpf(0))


def evolving_scalar(bg,k,curvature_square=False):
    R=pencil(bg,k,curvature_square)['reduced']
    tangent=[bg['rhodot'],*list(bg['qdot'])]
    vdot=bg['logVdot']
    def shifted(t):
        point=[q+t*v for q,v in zip(bg['point'],tangent)]
        return pencil(dict(point=point),k,curvature_square,t*vdot,t*vdot/3)['reduced']
    Adot=mp.diff(lambda t:shifted(t)[1,1],mp.mpf(0))
    Bdot=mp.diff(lambda t:shifted(t)[0,1],mp.mpf(0))
    A,B,C=R[1,1],R[0,1],R[0,0]
    omega2=A*C-B*B-Bdot+Adot*B/A
    light=mp.exp(2*(2-bg['point'][2])*bg['point'][1])
    return dict(omega_squared=omega2,speed_squared=omega2/(k*k*light),
                friction=-Adot/A,Adot=Adot,Bdot=Bdot)


def report():
    mp.mp.dps=60
    bg=witness()
    c=coefficients(bg['point'])
    serialize=lambda x:mp.nstr(x,28)
    rows=[]
    for square in (False,True):
        for k in map(mp.mpf,('10','1000','100000')):
            result=pencil(bg,k,square)
            flow=evolving_scalar(bg,k,square)
            rows.append(dict(curvature_square=square,k=serialize(k),
                             reduced=[[serialize(result['reduced'][i,j]) for j in range(2)] for i in range(2)],
                             **{key:serialize(result[key]) for key in ('curvature_rho','curvature_square_coefficient','frozen_omega_squared','frozen_growth')},
                             evolving={key:serialize(value) for key,value in flow.items()},
                             auxiliary_residual=serialize(mp.norm(result['auxiliary_EL_residual']))))
    return dict(candidate='IC13 explicit shear UV repair plus optional local curvature square',full_theory='OPEN',
                background_n=220,point=list(map(serialize,bg['point'])),coefficients={key:serialize(v) for key,v in c.items()},
                scalar_dispersion=rows,
                nonclaims=['One actual IC12 vacuum background, no full-branch stability theorem',
                           'Curvature-square addition defined on the strictly positive UV-kinetic chart',
                           'No full field Dirac closure or matter-coupled characteristic certificate'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args()
    print(json.dumps(report(),indent=2))
    raise SystemExit(2 if args.require_full_closure else 0)
