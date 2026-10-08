"""Bounded checks of three conditional derivation chains; no data fitting."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.linalg import eigvalsh

parser=argparse.ArgumentParser()
parser.add_argument("--output",required=True)
parser.add_argument("--mutate",choices=["none","filter","memory"],default="none")
args=parser.parse_args()
checks=[]
def check(label,condition):
    checks.append({"label":label,"pass":bool(condition)})

def hr(y):
    if y==0: return 0.
    return y/math.expm1(math.sqrt(y))
def hpr(y):
    r=math.sqrt(y); e=math.expm1(r)
    return 1/e-r*(e+1)/(2*e*e)
yp=brentq(hpr,1.,4.,xtol=1e-14)
hp=hr(yp); d=.05; b=d*hp
ys=brentq(lambda y:hpr(y)-b/(y+yp),1.,yp,xtol=1e-14)
hs=hr(ys)
def h(y):
    return hr(y) if y<=ys else hs+b*math.log((y+yp)/(ys+yp))
def dh(y):
    return hpr(y) if y<=ys else b/(y+yp)
def H(y):
    # sqrt substitution removes the integrable deep-limit derivative singularity.
    cut=min(y,ys)
    q=quad(lambda r:2*r*hr(r*r),0,math.sqrt(cut),epsabs=1e-12,epsrel=1e-12)[0]
    if y>ys:
        q+=hs*(y-ys)+b*((y+yp)*math.log((y+yp)/(ys+yp))-(y-ys))
    return q
def T(y): return 2*H(y)-y*h(y)

check("MONO derivative join",abs(hpr(ys)-b/(ys+yp))<1e-12)
source_rows=[]
for y in [.0001,.01,.1,1.,ys,3.,10.,100.]:
    step=1e-5
    # d/dlambda [exp(2lambda) H(y exp(-lambda))]
    fd=(math.exp(2*step)*H(y*math.exp(-step))-math.exp(-2*step)*H(y*math.exp(step)))/(2*step)
    check(f"scale derivative y={y}",abs(fd-T(y))<2e-7*max(T(y),1e-8))
    check(f"source and source slope y={y}",T(y)>0 and h(y)-y*dh(y)>0)
    source_rows.append({"y":y,"T_over_a_squared":T(y),"source_slope":h(y)-y*dh(y)})

heat_rows=[]
def evaluate(t,a,n):
    x=2*np.pi*np.arange(n)/n
    v=3+.9*np.exp(-t)*np.cos(x)+.4*np.exp(-4*t)*np.sin(2*x)
    vx=-.9*np.exp(-t)*np.sin(x)+.8*np.exp(-4*t)*np.cos(2*x)
    vt=-.9*np.exp(-t)*np.cos(x)-1.6*np.exp(-4*t)*np.sin(2*x)
    energy=np.mean([a*a*H(float(z/a)) for z in v])
    source=np.mean([a*a*T(float(z/a)) for z in v])
    diss=np.mean([dh(float(z/a))*w*w for z,w in zip(v,vx)])
    direct=np.mean([a*h(float(z/a))*w for z,w in zip(v,vt)])
    return energy,source,diss,direct
for t in [.03,.2,.8]:
    fine=evaluate(t,1.,2048); coarse=evaluate(t,1.,1024)
    check(f"heat resolution t={t}",max(abs(x-y) for x,y in zip(fine,coarse))<2e-7)
    E,Q,D,direct=fine
    check(f"heat integration by parts t={t}",abs(direct+D)<2e-7)
    step=1e-4
    plus=evaluate(t*math.exp(-2*step),math.exp(step),2048)[0]
    minus=evaluate(t*math.exp(2*step),math.exp(-step),2048)[0]
    fd=(plus-minus)/(2*step)
    predicted=Q if args.mutate=="filter" else Q+2*t*D
    check(f"joint inverse scale derivative t={t}",abs(fd-predicted)<3e-7)
    heat_rows.append({"heat_time":t,"mean_energy":E,"mean_scale_source":Q,
                      "mean_heat_dissipation":D,"joint_scale_derivative":fd})
check("heat energy decreases",all(heat_rows[j]["mean_energy"]>heat_rows[j+1]["mean_energy"] for j in [0,1]))

# Finite oscillator realization of the conditional FGF033 abstract Hessian.
omega=np.array([2.,5.]); g=np.array([.6,.8]); I=1.
S=float(np.sum(g*g/(omega*omega))); S2=float(np.sum(g*g/(omega**4)))
spectral_rows=[]
for stiffness in [.5,2.,6.]:
    matrix=np.block([[np.diag(omega*omega),g[:,None]],[g[None,:],np.array([[stiffness]])]])
    eigen=eigvalsh(matrix)
    def den(z): return stiffness-I*z-np.sum(g*g/(omega*omega-z))
    root=brentq(den,0,min(omega**2)-1e-9)
    low=((stiffness+I*omega[0]**2)-math.sqrt((stiffness+I*omega[0]**2)**2-4*I*omega[0]**2*(stiffness-S)))/(2*I)
    check(f"Schur pole equals full eigenvalue k={stiffness}",abs(root-eigen[0])<1e-11)
    check(f"slow mode bounds k={stiffness}",low<=root+1e-12 and root<min((stiffness-S)/I,omega[0]**2))
    spectral_rows.append({"stiffness":stiffness,"Schur_margin":stiffness-S,"lowest_squared_frequency":root,"lower_bound":low,"upper_bound":min((stiffness-S)/I,omega[0]**2)})
    check(f"interlacing k={stiffness}",eigen[0]<4<eigen[1]<25<eigen[2])
for tau in [.2,1.,2.]:
    lam=lambda t:math.sin(.7*t)+.2
    dl=lambda t:.7*math.cos(.7*t)
    original=sum(gg*gg*quad(lambda ss:math.sin(ww*(tau-ss))/ww*lam(ss),0,tau,epsabs=1e-12)[0] for ww,gg in zip(omega,g))
    memory=sum(gg*gg/(ww*ww)*quad(lambda ss:math.cos(ww*(tau-ss))*dl(ss),0,tau,epsabs=1e-12)[0] for ww,gg in zip(omega,g))
    initial=sum(gg*gg/(ww*ww)*math.cos(ww*tau)*lam(0) for ww,gg in zip(omega,g))
    reconstructed=S*lam(tau)-memory-(0 if args.mutate=="memory" else initial)
    check(f"causal memory integration identity t={tau}",abs(original-reconstructed)<1e-11)
check("equal-mass annular source merger factor",abs((2.**1.5)/(1.+1.)-math.sqrt(2))<1e-14)

out={"scope":"Conditional MONO scale/heat identities and FGF033 linear diagnostic memory; not physical theory closure",
     "mutation":args.mutate,"passed":sum(c["pass"] for c in checks),"total":len(checks),
     "joins":{"y_peak":yp,"y_star":ys,"h_peak":hp},"source_rows":source_rows,
     "heat_rows":heat_rows,"spectral_rows":spectral_rows,"static_susceptibility":S,
     "inertial_correction":S2,"checks":checks}
Path(args.output).write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:out[k] for k in ["passed","total","joins","heat_rows","spectral_rows"]},indent=2))
print("FAILED",[c["label"] for c in checks if not c["pass"]])
raise SystemExit(0 if all(c["pass"] for c in checks) else 1)
