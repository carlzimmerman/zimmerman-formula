#!/usr/bin/env python3
"""Unfolded affine-conformal static inverse: z=X' is retained as a state.

Solve the actual three equations before dividing by the radial pressure slope.
The determinant is computed, not supplied; this is an ODE inversion matrix,
NOT the canonical Poisson-bracket matrix or a DOF certificate.
"""
import json
import numpy as np
import conformal_inverse as c


def coefficients(eps,y,X,U,z,sigma):
    a=c.metric(eps,y);r,g,gr,B,Br=[a[k] for k in ('r','g','gr','B','Br')]
    F=(1+sigma*X)/2;f=sigma/2;K=3*f*f/(2*F);Kx=-3*f**3/(2*F*F)
    aa=g+2/r;N=2*f*z*aa+K*z*z;P=N/B
    Pz=(2*f*aa+2*K*z)/B
    p=np.sqrt(B*U);Z=U/X-r*g;Cj=2*X*Z/(p*r)
    explicitX=Kx*z*z/B
    explicitr=(-4*f*z*B/r**2-2*g*N)/B**2
    explicitg=(2*f*z*B-2*r*N)/B**2
    R0=explicitX*z+explicitr+explicitg*gr
    Achi=f*(a['rho']-2*a['pt'])-Kx*z*z/B-2*K*(g-Br/(2*B)+2/r)*z/B
    Lbase=2*F*a['rho']+P-2*f*(2/r-Br/(2*B))*z/B+K*z*z/B
    matrix=np.array([[Pz,-z,0],[-2*K/B,1,-Cj],[2*f/B,0,2*X*z/p]])
    zr,px,gx=np.linalg.solve(matrix,np.array([-R0,-Achi,Lbase]))
    return dict(**a,X=X,U=U,P=P,F=F,Fx=f,K=K,Kx=Kx,z=z,zr=zr,PX=px,GX=gx,
                current_factor=Cj,Echi=Achi-2*K*zr/B,matrix=matrix,
                h=f*z/F,D=1+r*f*z/(2*F),pressure_slope=Pz)


def action_curvatures(eps,y,X,U,z,sigma):
    a=coefficients(eps,y,X,U,z,sigma)
    point=np.array([y,X,U,z]);tangent=np.array([1/a['ry'],z,
        -2*a['g']*(2*X+U)-2*z,a['zr']])
    derivatives=np.zeros(2);step=1e-25
    for i in range(4):
        varied=point.astype(complex);varied[i]+=1j*step
        b=coefficients(eps,*varied,sigma)
        derivatives+=np.imag([b['PX'],b['GX']])/step*tangent[i]
    return a,derivatives[0]/z,derivatives[1]/z


def inspect(eps,y,X,U,z,sigma):
    a,pxx,gxx=action_curvatures(eps,y,X,U,z,sigma)
    return c.inspect_coefficients(a,pxx,gxx,sigma)


def main():
    eps,y,sigma=1e-6,.1,.1;X,U,P=c.initial(eps,y,sigma,.25,1.5)
    a=c.coefficients(eps,y,X,U,P,sigma)
    fold=-2*a['F']*(a['g']+2/a['r'])/(3*a['Fx'])
    print('GRADIENT_CHART='+json.dumps(dict(regular=inspect(eps,y,X,U,a['z'],sigma),
        fold=inspect(eps,y,X,U,fold,sigma)),allow_nan=False))
    return 0


if __name__=='__main__':raise SystemExit(main())
