#!/usr/bin/env python3
"""Independent 60-digit local check; does not certify the floating ODE trajectory."""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

spec=importlib.util.spec_from_file_location('pressure',Path(__file__).with_name('shared_pressure.py'))
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)


@lru_cache(None)
def evaluator():
    a=source.model.principal_template()
    args=[a['m'],a['G1'],a['G2'],a['P'],a['P1'],a['P2']]+list(a['v'])+[a['H'][i,j] for i in range(4) for j in range(i,4)]
    return s.lambdify(args,(a['M'],a['T']),'mpmath',cse=True)


def check(epsilon,y,u,z,k,dps=60,pressure=None,pxx=0):
    with mp.workdps(dps):
        eps,y,u,z,k=map(mp.mpf,(epsilon,y,u,z,k))
        # Differentiate r(y) and the imposed metric with automatic arbitrary-
        # precision differentiation rather than reusing the float derivatives.
        radius=lambda a:eps/mp.sqrt(a*(-mp.expm1(-a)))
        rg=lambda a:radius(a)*a/(1-2*radius(a)*a)
        r=radius(y);ry=mp.diff(radius,y);g=rg(y)/r
        gr=mp.diff(lambda a:rg(a)/radius(a),y)/ry
        T=1+2*r*g;Tr=2*g+2*r*gr
        invA=mp.exp(-eps*u);X=(mp.mpf('.5')-eps*z)*invA;U=invA-2*X
        P=k*(X-mp.mpf('.5')) if pressure is None else mp.mpf(pressure)
        PX=k;PXX=mp.mpf(pxx);B=T/(1+r*r*P);Z=U/X-r*g
        # Direct geometric expression, deliberately keeping cancellations.
        Br_partial=Tr/(1+r*r*P)-2*r*P*T/(1+r*r*P)**2
        E0=(1-1/B)/r**2+Br_partial/(B*B*r)+P
        Xr=Z*E0/(r*PX*(1+Z/T));p=mp.sqrt(B*U)
        Br=Br_partial-T*r*r*PX*Xr/(1+r*r*P)**2
        Ur=-2*g*invA-2*Xr;pr=p*(Br/B+Ur/U)/2
        Zr=-(invA/X)*(2*g+Xr/X)-g-r*gr
        GX=PX*p*r/(2*X*Z);GXX=GX*((pr/p+1/r-Xr/X-Zr/Z)/Xr+PXX/PX)
        H=mp.matrix([[-g*p/B,g*mp.sqrt(invA/B),0,0],
                     [g*mp.sqrt(invA/B),(pr-Br*p/(2*B))/B,0,0],
                     [0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
        v=[-mp.sqrt(invA),p/mp.sqrt(B),0,0]
        C,stress=evaluator()(1,GX,GXX,P,PX,PXX,*v,*[H[i,j] for i in range(4) for j in range(i,4)])
        rho=(1-1/B)/r**2+Br/(B*B*r)
        # Independent angular Einstein component, not stress conservation.
        pt=(gr+g*g-g*Br/(2*B)+(g-Br/(2*B))/r)/B
        scale=max(abs(rho),abs(P),abs(pt))
        err=max(abs(stress[0,0]-rho),abs(stress[1,1]-P),abs(stress[2,2]-pt),abs(stress[0,1]))/scale
        disc=C[0,1]**2-C[0,0]*C[1,1]
        beta=U/(2*X)
        return dict(relative_stress_error=err,kinetic=C[0,0],radial_discriminant=disc,
                    angular=C[2,2],rho=rho,pressure=P,
                    cross=C[0,1],radial=C[1,1],beta=beta,invariant=C[0,0]-C[2,2]/beta,
                    healthy=bool(C[0,0]>0 and disc>0 and C[2,2]<0),dps=dps)


def main():
    row=check('1e-6','20','-15.610882545637942','.2795108412451867','10000')
    print(json.dumps({k:v if isinstance(v,(bool,int)) else mp.nstr(v,40) for k,v in row.items()},indent=2))
    spec=importlib.util.spec_from_file_location('steering',Path(__file__).with_name('jet_steering.py'))
    steering=importlib.util.module_from_spec(spec);spec.loader.exec_module(steering)
    choice=steering.choose(1e-6,20.,0.,.5,0.,1.)
    repaired=check('1e-6','20','0','.5','1',pressure='0',pxx=str(choice['PXX']))
    print('CONSTRUCTED_LOCAL_JET='+json.dumps({k:v if isinstance(v,(bool,int)) else mp.nstr(v,40) for k,v in repaired.items()}))
    return 0 if max(row['relative_stress_error'],repaired['relative_stress_error'])<mp.mpf('1e-35') else 1


if __name__=='__main__':raise SystemExit(main())
