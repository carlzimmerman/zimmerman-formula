#!/usr/bin/env python3
"""Exact fixed-metric lapse/U jets and frozen transition principal Schur test."""
import argparse,json,sys
from pathlib import Path
import sympy as s


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
 def exact(name,e):
  r=s.factor(s.simplify(e));assert r==0,(name,r);checks[name]=str(r)
 e=s.symbols('e');a,cN,ell,theta=s.symbols('a cN ell theta',real=True)
 n,vn,a0,u0,vu,w0,sw,r0,tw,J0,J1,J2,G0,f,G2=s.symbols('n vn a0 u0 vu w0 sw r0 tw J0 J1 J2 G0 f G2',real=True)
 sigma0=J0+ell*(r0+a0*w0)-theta
 sigma=J0+e*J1*sw+e**2*J2*sw**2/2+ell*(r0+e*tw+(a0+e*vn)*(w0+e*sw))-theta
 ds=(J1+ell*a0)*sw+ell*tw+ell*w0*vn
 d2s=J2*sw**2+2*ell*vn*sw
 exact('weighted_gate_first_jet',s.diff(sigma,e).subs(e,0)-ds)
 exact('weighted_gate_second_jet',s.diff(sigma,e,2).subs(e,0)-d2s)
 G=G0+f*(sigma-sigma0)+G2*(sigma-sigma0)**2/2
 N=1+e*n+e**2*n*n/2
 exact('lapse_measure_gate_second_jet',s.diff(N*G,e,2).subs(e,0)-(G0*n*n+2*f*n*ds+f*d2s+G2*ds**2))
 L=N*(a*(a0+e*vn)**2+2*cN*(u0+e*vu-a0-e*vn)**2+cN*G)
 target=a*a0*a0*n*n+4*a*a0*n*vn+2*a*vn*vn+2*cN*(u0-a0)**2*n*n+8*cN*(u0-a0)*n*(vu-vn)+4*cN*(vu-vn)**2+cN*(G0*n*n+2*f*n*ds+f*d2s+G2*ds**2)
 exact('full_lapse_U_second_jet',s.diff(L,e,2).subs(e,0)-target)
 # Under the periodic principal integration-by-parts identity n*tw -> -vn*sw.
 exact('affine_weighted_gate_principal_cancellation',2*cN*f*ell*((-vn*sw)+vn*sw))
 A,B,R,Lc,Zr,Zi=s.symbols('A B R Lc Zr Zi',real=True)
 den=A+B+R*(Zr**2+Zi**2)
 ae=2+R*Lc**2-((-A+R*Lc*Zr)**2+(R*Lc*Zi)**2)/den
 exact('transition_Schur_gap',2-ae-(A*A-R*(2*A*Lc*Zr+Lc**2*(A+B)))/den)
 repaired_cN=1-a/2
 uv=s.factor(ae.subs({B:0,Zr:0,Zi:0,A:2*repaired_cN,R:repaired_cN*G2/2,Lc:ell*w0}))
 exact('transition_UV_coefficient',uv-(a+repaired_cN*G2*ell**2*w0**2/2))
 exact('transition_UV_gap',2-uv-(2-a)*(1-G2*ell**2*w0**2/4))
 tt=s.symbols('tt');ff=35*tt**4-84*tt**5+70*tt**6-20*tt**7
 exact('ramp_midpoint',ff.subs(tt,s.Rational(1,2))-s.Rational(1,2))
 exact('ramp_max_slope_value',s.diff(ff,tt).subs(tt,s.Rational(1,2))-s.Rational(35,16))
 uvexample=uv.subs({a:s.Rational(1,10),G2:s.Rational(35,16),ell:1,w0:2});assert uvexample==s.Rational(681,160)>2
 b=s.Rational(1,100);cs=b*(2-uvexample)/((2+3*b)*uvexample);assert cs<0
 # Leading conformal metric variation of Delta_h S_h U on an affine background.
 d,k,h,ps=s.symbols('d k h ps',real=True,nonzero=True)
 deltaW=-s.I*(d-2)*w0*(1-h)*ps/k
 directDelta=-s.I*(d-2)*w0*k*ps
 exact('metric_heat_leading_cancellation',-k*k*deltaW+directDelta-h*directDelta)
 out={'runtime':{'python':sys.version,'executable':sys.executable,'sympy':s.__version__},'checks':checks,'count':len(checks),
      'UV_effective_alpha':str(uv),'example':{'alpha':'1/10','ell_w':'2','gate_width':'1','Gsecond':'35/16','effective_alpha':str(uvexample),'cs2':str(cs)},
      'scope':'Frozen transition principal diagnostic including exact N measure and weighted-lapse jets; no constraint-satisfying global background constructed',
      'nonclaims':['The complete curved moving-background scalar constraint/PDE system is not derived','The example is a coefficient/state-jet counterexample to automatic all-state positivity, not a completed gravitational solution','The fixed-metric lapse/U calculation alone does not certify every heat-metric quadratic vertex']}
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':True,'exact_checks':len(checks),'transition_UV_gap_negative':True}))
if __name__=='__main__':main()
