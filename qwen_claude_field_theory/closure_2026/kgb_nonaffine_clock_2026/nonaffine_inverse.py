#!/usr/bin/env python3
"""Fixed quadratic-F clock action: general static inverse and derived jets.

F(X)=F0+f0*(X-X0)+j0*(X-X0)^2/2 is ONE specified coupling. P and G are
reconstructed from the radial equations; their curvatures are total derivatives.
No particle dark matter, assigned principal rank, PPN values, or DOF counts.
"""
import json
from pathlib import Path
import sys
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]/'kgb_mass_compatibility_2026'))
import conformal_inverse as old


def coefficients(eps,y,X,U,z,j0=0.,F0=.525,f0=.05,X0=.5):
    a=old.metric(eps,y);r,g,gr,B,Br=[a[k] for k in ('r','g','gr','B','Br')]
    dx=X-X0;F=F0+f0*dx+j0*dx*dx/2;f=f0+j0*dx;j=j0
    K=3*f*f/(2*F);Kx=3*f*j/F-3*f**3/(2*F*F)
    aa=g+2/r;N=2*f*z*aa+K*z*z;P=N/B
    Pz=(2*f*aa+2*K*z)/B;p=np.sqrt(B*U)
    Cj=2*X*(U/X-r*g)/(p*r)
    explicitX=(2*j*z*aa+Kx*z*z)/B
    explicitr=(-4*f*z*B/r**2-2*g*N)/B**2
    explicitg=(2*f*z*B-2*r*N)/B**2
    R0=explicitX*z+explicitr+explicitg*gr
    Achi=f*(a['rho']-2*a['pt'])-Kx*z*z/B-2*K*(g-Br/(2*B)+2/r)*z/B
    Lbase=2*F*a['rho']+P-2*f*(2/r-Br/(2*B))*z/B+(K-2*j)*z*z/B
    matrix=np.array([[Pz,-z,0],[-2*K/B,1,-Cj],[2*f/B,0,2*X*z/p]])
    zr,px,gx=np.linalg.solve(matrix,np.array([-R0,-Achi,Lbase]))
    return dict(**a,X=X,U=U,P=P,F=F,f=f,j=j,K=K,Kx=Kx,z=z,zr=zr,PX=px,GX=gx,
                Echi=Achi-2*K*zr/B,matrix=matrix,
                h=f*z/F,Dcoord=1+r*f*z/(2*F),Dfield=2*(F-X*f))


def action_curvatures(eps,y,X,U,z,**kwargs):
    a=coefficients(eps,y,X,U,z,**kwargs)
    point=np.array([y,X,U,z]);v=np.array([1/a['ry'],z,-2*a['g']*(2*X+U)-2*z,a['zr']])
    h=1e-25;out=np.zeros(2)
    for i in range(4):
        q=point.astype(complex);q[i]+=1j*h
        b=coefficients(eps,*q,**kwargs)
        out+=np.imag([b['PX'],b['GX']])/h*v[i]
    return a,out[0]/z,out[1]/z


def background(a):
    B,U,X,g,z,Br=[a[k] for k in ('B','U','X','g','z','Br')]
    p=np.sqrt(B*U);Q=2*X+U;Ur=-2*g*Q-2*z
    pp=p*(Br/B+Ur/U)/2
    return p,Q,pp


def physical_residual(a):
    r,g,B,Br,F,f,j,K,z,zr,P,px,gx=[a[k] for k in
        ('r','g','B','Br','F','f','j','K','z','zr','P','PX','GX')]
    p,Q,pp=background(a);X=a['X']
    boxphi=(pp+(g-Br/(2*B)+2/r)*p)/B
    terms=np.array([px*p/B,-gx*boxphi*p/B,-gx*z/B,p*a['Echi']/B])
    boxF=(f*(zr+(g-Br/(2*B)+2/r)*z)+j*z*z)/B
    pt=(P+gx*p*z/B-2*(boxF-f*z/(B*r))+K*z*z/B)/(2*F)
    rho=(2*(f*(zr+(2/r-Br/(2*B))*z)+j*z*z)/B-K*z*z/B+2*X*gx*z/p-P)/(2*F)
    pr=(P-2*(g+2/r)*f*z/B-K*z*z/B)/(2*F)
    scale=max(abs(a['rho']),abs(a['pt']),abs(P),1e-200)
    return dict(metric=float(max(abs(pt-a['pt']),abs(rho-a['rho']),abs(pr))/scale),
                current=float(abs(sum(terms))/sum(abs(terms))))


def inspect(eps,y,X,U,z,**kwargs):
    a,pxx,gxx=action_curvatures(eps,y,X,U,z,**kwargs)
    F,f,j,B,r,g,P,px,gx=[a[k] for k in ('F','f','j','B','r','g','P','PX','GX')]
    C,C1,C2=2*F,2*f,2*j;D=C-X*C1
    if min(F,X,U,B,a['Dcoord'])<=0 or D==0 or f==0 or z==0:
        raise ValueError('outside regular timelike non-affine chart')
    Pt=P/C**2;P1=(px-2*C1*P/C)/D
    P2=(C*C*D*pxx+C*(C*X*C2-2*C1*D)*px+2*(C1*C1*D-C*C*C2)*P)/D**3
    G1=C*gx/D;G2=C*C*((C*gxx+C1*gx)*D+C*X*C2*gx)/D**3
    p,Q,pp=background(a);h=a['h'];Br=a['Br'];Dc=a['Dcoord']
    H=np.array([[-(g+h/2)*p/(C*B),(g+h/2)*np.sqrt(Q/B)/C,0,0],
                [(g+h/2)*np.sqrt(Q/B)/C,(pp-(Br/B+h)*p/2)/(C*B),0,0],
                [0,0,p*Dc/(C*B*r),0],[0,0,0,p*Dc/(C*B*r)]])
    v=[-np.sqrt(Q/C),np.sqrt(U/C),0,0]
    M,T=old.j.source.evaluator()(1,G1,G2,Pt,P1,P2,*v,*[H[i,k] for i in range(4) for k in range(i,4)])
    k,cross,radial,angular=[M[i,l] for i,l in ((0,0),(0,1),(1,1),(2,2))]
    points=[0.,1.]
    if radial>angular and 0<abs(cross)/(radial-angular)<1:points.append(abs(cross)/(radial-angular))
    margin=min(k+angular-2*abs(cross)*t+(radial-angular)*t*t for t in points)
    bounded=bool(k>0 and radial<0 and angular<0)
    result=dict(y=y,X=X,U=U,z=z,F=F,f=f,j=j,Dfield=D,P=P,PX=px,GX=gx,PXX=pxx,GXX=gxx,
        kinetic=float(k),cross=float(cross),radial=float(radial),angular=float(angular),light_margin=float(margin),
        bounded_EF=bounded,strict_EF=bool(bounded and k>abs(cross) and margin>0),
        residual=physical_residual(a),inverse_determinant=float(np.linalg.det(a['matrix'])),
        scope='Vacuum local EF diagnostic for supplied F-jet and inverse-derived P/G jets; not full theory')
    json.dumps(result,allow_nan=False)
    return result


def main():
    rows=[];eps=1e-6
    for y in (.1,1.,2.,10.):
        for b in (.25,.75,1.25,4.):
            X,U,_=old.initial(eps,y,.1,b,1.5);z=-1.5*old.metric(eps,y)['g']
            for ratio in (-20,-5,-1,-.2,0,.2,1,5,20):
                row=inspect(eps,y,X,U,z,j0=ratio*.05/eps)
                row.update(bscale=b,curvature_ratio=ratio);rows.append(row)
    print('QUADRATIC_F_SCAN='+json.dumps(dict(rows=rows,attempts=len(rows),
        healthy=sum(r['strict_EF'] for r in rows))))
    return 0


if __name__=='__main__':raise SystemExit(main())
