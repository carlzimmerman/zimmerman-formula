#!/usr/bin/env python3
"""Action-derived P_XX freedom, not a fitted sound-speed matrix.

On a static zero-current inverse, varying P_XX at fixed background and
P,P_X varies G_XX by (G_X/P_X)*delta P_XX. Differentiate the existing
covariant principal symbol to find the actual accessible matrix pencil.
"""
import importlib.util
import json
from pathlib import Path
import sympy as s

spec=importlib.util.spec_from_file_location('pressure',Path(__file__).with_name('shared_pressure.py'))
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)


def derive():
    a=source.model.principal_template()
    B,p,v,g,r=s.symbols('B p v g r',positive=True)
    h,P,PX=s.symbols('h P PX',real=True)
    X=(v*v-p*p/B)/2
    GX=-PX*p/(2*X*g-2*p*p/(B*r))
    H=s.Matrix([[-g*p/B,v*g/s.sqrt(B),0,0],
                [v*g/s.sqrt(B),h,0,0],[0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
    subs={a['G1']:GX,a['P']:P,a['P1']:PX}
    subs.update(dict(zip(a['v'],[-v,p/s.sqrt(B),0,0])))
    subs.update({a['H'][i,j]:H[i,j] for i in range(4) for j in range(i,4)})
    slope=(a['M'].diff(a['P2'])+a['M'].diff(a['G2'])*a['G1']/a['P1'])
    slope=slope.subs(subs,simultaneous=True).applyfunc(s.factor)
    stress=a['T'].subs(subs,simultaneous=True).applyfunc(s.factor)
    beta=p*p/(2*B*X);E=s.factor(stress[0,0]+P)
    residuals=[s.factor(PX*slope[0,0]-E),s.factor(PX*slope[2,2]-(stress[2,2]-P)),
               s.factor(stress[2,2]-P-beta*E),s.factor(stress[1,1]-P)]
    residuals.extend(s.factor(slope[i,j]) for i,j in ((0,1),(1,1),(0,2),(0,3),(1,2),(1,3),(2,3)))
    # Recompute without dividing by P_X or Z. This is the chart that actually
    # reaches P_X=Z=0; an old-chart limit alone would not establish regularity.
    L=s.symbols('L',nonzero=True);Z=p*p/(B*X)-r*g
    regular_subs=dict(subs);regular_subs[a['G1']]=p*L
    regular_subs[a['P1']]=2*X*L*Z/r
    regular=(a['M'].diff(a['P2'])*2*X*Z/r+a['M'].diff(a['G2'])*p)
    regular=regular.subs(regular_subs,simultaneous=True).applyfunc(s.factor)
    Treg=a['T'].subs(regular_subs,simultaneous=True).applyfunc(s.factor)
    Ereg=s.factor(Treg[0,0]+P)
    regular_res=[s.factor(L*regular[0,0]-Ereg),s.factor(L*regular[2,2]-beta*Ereg),
                 s.factor(regular[0,0]-regular[2,2]/beta),regular[0,1],regular[1,1]]
    return dict(X=X,beta=beta,enthalpy=E,actual_slope_matrix=slope,
                slope_residuals=residuals,invariant_derivative=s.factor(slope[0,0]-slope[2,2]/beta),
                regular_slope_matrix=regular,regular_slope_residuals=regular_res,
                domain='timelike X>0; p nonzero; P_X nonzero; finite zero-current G_X; exclude singular denominators',
                scope='Local jet accessibility only; integrability across radii and masses remains required')


def main():
    a=derive();print(json.dumps({k:str(v) for k,v in a.items()},indent=2))
    return 0 if all(x==0 for x in a['slope_residuals']+a['regular_slope_residuals']) and a['invariant_derivative']==0 else 1


if __name__=='__main__':raise SystemExit(main())
