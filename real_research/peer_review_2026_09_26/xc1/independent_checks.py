"""Bounded, independently derived XC1 checks; writes only beside this file."""
import json
import math
from pathlib import Path

import numpy as np
import scipy.optimize as opt
import sympy as s

ROOT = Path(__file__).resolve().parent
out = {}

# Exact 1+1-dimensional reduction of n=-d(t+pi)/sqrt(X), using its rapidity.
# This is a genuine subset of the 3+1 flat-space jets, not a copied target.
e, pt, px, htt, htx, hxx, al, c2 = s.symbols("e pt px htt htx hxx alpha c2")
X = (1 + e * pt)**2 - e**2 * px**2
An = ((1 + e*pt)*e*px*e*htt
      - ((1+e*pt)**2+e**2*px**2)*e*htx
      + e*px*(1+e*pt)*e*hxx)
Kn = -e**2*px**2*e*htt + 2*(1+e*pt)*e*px*e*htx - (1+e*pt)**2*e*hxx
L = s.series((al*An**2-c2*Kn**2)/X**3,e,0,5).removeO().expand()
target2 = al*htx**2-c2*hxx**2
target3 = 2*c2*hxx*(2*px*htx+pt*hxx)-2*al*(htt*px*htx+pt*htx**2+htx*hxx*px)
assert s.expand(L.coeff(e,2)-target2)==0
assert s.expand(L.coeff(e,3)-target3)==0
fields = [pt,px,htt,htx,hxx]
timecount = [1,0,2,1,0]
derivativecount = [1,1,2,2,2]
classes = set()
for F in (3,4):
    for coupling, expr in [("alpha",L.coeff(e,F).coeff(al)),("c2",L.coeff(e,F).coeff(c2))]:
        for powers,coefficient in s.Poly(expr,*fields).terms():
            nt=sum(a*b for a,b in zip(powers,timecount))
            nd=sum(a*b for a,b in zip(powers,derivativecount))
            j=int(coupling=="c2")
            exponent=s.Rational(2*j+nt-s.Rational(F,2)-1,4-nd)
            classes.add((F,coupling,nt,nd,str(exponent)))
out["flat_1plus1"]={"quadratic":str(target2),"cubic":str(target3),"quartic":str(L.coeff(e,4)),"classes":sorted(classes)}
assert {x[-1] for x in classes}=={"3/2","1/2","-1/2"}

# Exact heat-operator derivative on a compact flat T^3 under
# h_ij(eps)=exp(2 eps sigma)delta_ij. In d=3,
# delta Delta=-2 sigma Delta+grad sigma.grad.
# For input q and output p, delta Delta_pq=(3 q^2-p.q)sigma_(p-q).
# The spectral divided difference follows directly by integrating Duhamel.
bp,bq,b=s.symbols("p2 q2 b",positive=True)
t=s.symbols("t",real=True)
integrated=s.integrate(s.exp(-(b-t)*bp-t*bq),(t,0,b))
out["heat_frechet"]={"integral":str(integrated),"rows":[]}
for K in [10,20,50,100]:
    # Real cos((K-1)x) metric perturbation and cos(Kx) scalar input;
    # output cos(x) remains nonzero, so its gradient survives in q.
    coefficient=0.5*(3*K*K-K)*(math.exp(-0.5)-math.exp(-0.5*K*K))/(K*K-1)
    out["heat_frechet"]["rows"].append({"K":K,"b":0.5,"soft_cos_x_coefficient":coefficient,"naive_hard_leg_factor":math.exp(-0.5*K*K)})
out["heat_frechet"]["limit_K_infinity"]=1.5*math.exp(-0.5)

# Smooth analytical branches underlying the numerical nu_mono construction.
y=s.symbols("y",positive=True)
h=y/(s.exp(s.sqrt(y))-1)
hp=s.lambdify(y,s.diff(h,y),"numpy")
hpp=s.lambdify(y,s.diff(h,y,2),"numpy")
hf=s.lambdify(y,h,"numpy")
yp=opt.brentq(hp,1,5,xtol=1e-14)
peak=float(hf(yp))
floor=lambda yy:0.05*peak/(yy+yp)
ys=opt.brentq(lambda yy:hp(yy)-floor(yy),1,yp,xtol=1e-14)
out["mono_splice"]={"y_peak":yp,"h_peak":peak,"y_splice":ys,"CL_at_splice":floor(ys),"CLprime_from_RAR":float(hpp(ys)),"CLprime_from_floor":-0.05*peak/(ys+yp)**2}

# A8's fixed-filter direct cubic, with the SAME decoupling canonical
# prescription as A6, but alpha_eff(k), c_s(k), and U elimination restored.
# This is a diagnostic of that approximation, not a reduced full-action amplitude.
inputs=json.loads((ROOT/"snapshots/L340_filtered_khronon_completion_results.json").read_text())
ac=inputs["numbers"]["P1"]["alpha_c_min"]
caps=json.loads((ROOT/"snapshots/L350_chk_cosmological_G_gate_results.json").read_text())
c2v=min(round(float(row["c2_ceiling"]),6) for row in caps["numbers"]["G2"]["rows"] if row.get("c2_ceiling") is not None and np.isfinite(float(row["c2_ceiling"])))
M=2.435e18
am=9.3619e-11/(2.99792458e8)**2*1.973269804e-16
xi=0.031*3.0856775814913673e16/1.973269804e-16
rows=[]
for yy in [0.01,0.1,0.5,1.,2.]:
    C0=float(hp(yy)); Cp=abs(float(hpp(yy)))
    def params(xx):
        C=C0*math.exp(-xx)
        ae=ac+2*C/(1+C)
        # Exact sound speed of the frozen ADM block with alpha_eff.
        cs=math.sqrt(c2v*(2-ae)/(ae*(2+3*c2v)))
        g=Cp*math.exp(-1.5*xx)/(3*am*(1+C)**3)
        return ae,cs,g
    def strength(xx):
        ae,cs,g=params(xx)
        return xx/xi**2*g*math.sqrt(cs)/(M*ae**1.5)
    res=opt.minimize_scalar(lambda xx:-strength(xx),bounds=(0,100),method="bounded")
    ae0,cs0,g0=params(0)
    km0=math.sqrt(M*ae0**1.5/(g0*math.sqrt(cs0)))
    naive=2/(3*math.e)/(xi*km0)**2
    rows.append({"y":yy,"x_peak":float(res.x),"direct_cubic_max_with_running_normalization":float(-res.fun),"A8_same_y_fixed_normalization":naive,"ratio":float(-res.fun/naive)})
out["direct_cubic_normalization_diagnostic"]={"alpha_c":ac,"c2":c2v,"xi_pc":0.031,"rows":rows,"scope":"Frozen direct longitudinal cubic plus decoupling-style normalization; no constraints or omitted metric/filter vertices integrated."}

result=ROOT/"run/results.json"
result.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
