#!/usr/bin/env python3
"""Actual static inverse for affine conformal DHOST, including TOTAL current.

F=(1+sigma X)/2, B=1+2rg. The action's radial equation fixes X'; its derivative,
total current and lapse equation determine X'', P_X and G_X. Curvatures of P/G
are total derivatives of those solved functions, never health controls.
"""
import json
import numpy as np
import triple_seed as inherited
j=inherited.j


def metric(eps,y):
    mu=-np.expm1(-y); lam=mu+y*np.exp(-y)
    r=eps/np.sqrt(y*mu);ry=-r*lam/(2*y*mu);yr=1/ry
    B=1/(1-2*r*y);Br=2*(y+r*yr)*B*B
    g=y*B;gr=yr*B+y*Br
    rho=4*y*y*np.exp(-y)/(r*lam)
    pr=((1/B-1)/r+2*g/B)/r
    pt=(gr+g*g-g*Br/(2*B)+(g-Br/(2*B))/r)/B
    return dict(y=y,r=r,ry=ry,g=g,gr=gr,B=B,Br=Br,rho=rho,pr=pr,pt=pt)


def pressure_from_gradient(eps,y,X,z,sigma):
    a=metric(eps,y);r,g,B=a['r'],a['g'],a['B']
    F=(1+sigma*X)/2;Fx=sigma/2
    return (2*Fx*z*(g+2/r)+1.5*Fx*Fx*z*z/F)/B


def coefficients(eps,y,X,U,P,sigma):
    a=metric(eps,y);r,g,gr,B,Br=[a[k] for k in ('r','g','gr','B','Br')]
    F=(1+sigma*X)/2;Fx=sigma/2;K=3*Fx*Fx/(2*F);Kx=-3*Fx**3/(2*F*F)
    aa=g+2/r;radical=np.sqrt(aa*aa+1.5*B*P/F)
    z=B*P/(Fx*(aa+radical))  # GR-connected quadratic root, stable at small P.
    N=2*Fx*z*aa+1.5*Fx*Fx*z*z/F
    Pz=(2*Fx*aa+3*Fx*Fx*z/F)/B
    PexplicitX=-1.5*Fx**3*z*z/(F*F*B)
    Pexplicitr=(-4*Fx*z*B/(r*r)-2*g*N)/(B*B)
    Pexplicitg=(2*Fx*z*B-2*r*N)/(B*B)
    offset=-(PexplicitX*z+Pexplicitr+Pexplicitg*gr)/Pz
    slope=z/Pz  # z'=offset+slope*P_X from preservation of radial equation.
    p=np.sqrt(B*U);Z=U/X-r*g
    current_factor=2*X*Z/(p*r)
    scalar_curvature=a['rho']-2*a['pt']  # pr_geom=0 identically for B=1+2rg.
    e0=Fx*scalar_curvature-Kx*z*z/B-2*K*(offset+(g-Br/(2*B)+2/r)*z)/B
    e1=-2*K*slope/B
    l0=2*F*a['rho']+P-2*Fx*(offset+(2/r-Br/(2*B))*z)/B+K*z*z/B
    l1=-2*Fx*slope/B
    matrix=np.array([[1+e1,-current_factor],[-l1,2*X*z/p]])
    px,gx=np.linalg.solve(matrix,np.array([-e0,l0]))
    zr=offset+slope*px
    return dict(**a,X=X,U=U,P=P,F=F,Fx=Fx,K=K,Kx=Kx,z=z,zr=zr,PX=px,GX=gx,
                current_factor=current_factor,Echi=e0+e1*px,matrix=matrix,
                h=Fx*z/F,D=1+r*Fx*z/(2*F))


def action_curvatures(eps,y,X,U,P,sigma):
    a=coefficients(eps,y,X,U,P,sigma)
    # Differentiate with respect to (y,X,U,P) along the actual radial flow.
    point=np.array([y,X,U,P]);tangent=np.array([1/a['ry'],a['z'],
        -2*a['g']*(2*X+U)-2*a['z'],a['PX']*a['z']])
    derivatives=np.zeros(2);step=1e-25
    for i in range(4):
        varied=point.astype(complex);varied[i]+=1j*step
        b=coefficients(eps,*varied,sigma)
        derivatives+=np.imag([b['PX'],b['GX']])/step*tangent[i]
    return a,derivatives[0]/a['z'],derivatives[1]/a['z']


def inspect(eps,y,X,U,P,sigma):
    a,pxx,gxx=action_curvatures(eps,y,X,U,P,sigma)
    return inspect_coefficients(a,pxx,gxx,sigma)


def inspect_coefficients(a,pxx,gxx,sigma):
    y,X,U,P=[a[k] for k in ('y','X','U','P')]
    r,g,B,Br,F,Fx,K,Kx,z,zr,px,gx=[a[k] for k in
        ('r','g','B','Br','F','Fx','K','Kx','z','zr','PX','GX')]
    if min(X,U,F,B,a['D'])<=0 or z==0:raise ValueError('outside regular affine conformal chart')
    p=np.sqrt(B*U);invA=2*X+U;Ur=-2*g*invA-2*z
    pp=p*(Br/B+Ur/U)/2
    boxphi=(pp+(g-Br/(2*B)+2/r)*p)/B
    currentK=(px-gx*boxphi)*p/B-gx*z/B
    currentF=p*a['Echi']/B
    boxF=Fx*(zr+(g-Br/(2*B)+2/r)*z)/B
    kineticX=K*z*z/B
    # Assemble the angular metric component directly from the variation.
    # Its vanishing follows algebraically from radial preservation, density and
    # total current (structure audit): a cross-check, NOT another independent gate.
    pt_pred=(P+gx*p*z/B-2*(boxF-Fx*z/(B*r))+kineticX)/(2*F)
    rho_pred=(2*Fx*(zr+(2/r-Br/(2*B))*z)/B-kineticX+2*X*gx*z/p-P)/(2*F)
    pr_pred=(P-2*(g+2/r)*Fx*z/B-kineticX)/(2*F)
    scale=max(abs(a['rho']),abs(a['pt']),abs(P),1e-200)
    err=max(abs(pt_pred-a['pt']),abs(rho_pred-a['rho']),abs(pr_pred))/scale
    # Invertible Einstein-frame dictionary: same original coupled principal
    # expression, but transformed coefficients and background, NOT old C.
    C=2*F;ptilde=P/(C*C)
    px_t=px-2*sigma*P/C
    pxx_t=C*C*pxx-2*sigma*C*px+2*sigma*sigma*P
    gx_t=C*gx;gxx_t=C**3*gxx+sigma*C*C*gx
    h=a['h'];D=a['D']
    H=np.array([[-(g+h/2)*p/(C*B),(g+h/2)*np.sqrt(invA/B)/C,0,0],
                [(g+h/2)*np.sqrt(invA/B)/C,(pp-(Br/B+h)*p/2)/(C*B),0,0],
                [0,0,p*D/(C*B*r),0],[0,0,0,p*D/(C*B*r)]])
    v=[-np.sqrt(invA/C),np.sqrt(U/C),0,0]
    M,_=j.source.evaluator()(1,gx_t,gxx_t,ptilde,px_t,pxx_t,*v,*[H[i,k] for i in range(4) for k in range(i,4)])
    k,cross,radial,angular=M[0,0],M[0,1],M[1,1],M[2,2]
    ts=[0.,1.]
    if radial>angular and 0<abs(cross)/(radial-angular)<1:ts.append(abs(cross)/(radial-angular))
    margin=min(k+angular-2*abs(cross)*t+(radial-angular)*t*t for t in ts)
    bounded=bool(k>0 and radial<0 and angular<0)
    causal=bool(bounded and k>abs(cross) and margin>0)
    result=dict(y=y,X=X,U=U,P=P,sigma=sigma,PX=float(px),PXX=float(pxx),GX=float(gx),GXX=float(gxx),
        z=float(z),zr=float(zr),matrix_det=float(np.linalg.det(a['matrix'])),
        relative_metric_error=float(err),relative_total_current_error=float(abs(currentK+currentF)/max(abs(currentK)+abs(currentF),1e-200)),
        kinetic=float(k),radial=float(radial),angular=float(angular),cross=float(cross),light_margin=float(margin),
        EF_bounded=bounded,EF_strict_cone=causal,
        scope='Einstein-frame local scalar diagnostic under invertible affine conformal dictionary; no full physical nonlinear stability certificate')
    json.dumps(result,allow_nan=False)
    return result


def initial(eps,y,sigma,b,d):
    a=metric(eps,y);X=.5;U=b*X*a['r']*a['g'];z=-d*a['g']
    P=pressure_from_gradient(eps,y,X,z,sigma)
    return X,U,P


def scan():
    rows=[];eps=1e-6
    for y in (.1,1.,2.,10.,20.):
        for sigma in (1e-6,1e-3,.1,1.):
            for b in (.25,.75,1.25,4.):
                for d in (.5,1.,1.5,2.):
                    try:
                        row=inspect(eps,y,*initial(eps,y,sigma,b,d),sigma)
                        row.update(bscale=b,dscale=d);rows.append(row)
                    except (ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:
                        rows.append(dict(y=y,sigma=sigma,bscale=b,dscale=d,error=str(exc)))
    return rows


def main():
    rows=scan()
    print('CONFORMAL_SCAN='+json.dumps(dict(rows=rows,attempts=len(rows),
        bounded=sum(r.get('EF_bounded',False) for r in rows),causal=sum(r.get('EF_strict_cone',False) for r in rows))))
    return 0


if __name__=='__main__':raise SystemExit(main())
