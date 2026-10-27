"""Explicit auxiliary-action prototype linking flux vacuum and cubic force.

Derived equations and conditions are in PLANCK_SCALED_FLUX_LINK.tex.
No covariant microscopic band/frame completion or physical halo fit.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np
import sympy as sy
from scipy.integrate import quad
from scipy.optimize import brentq

out=Path(sys.argv[1]);assert out.is_dir();checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name

s,sref,Q,p,alpha,n=sy.symbols('s sref Q p alpha n',positive=True)
Tavg,Ravg,DF=sy.symbols('Tavg Ravg DF',real=True)
V=Q**2*(s/sref)**n/2
W=alpha*p**3/Q
Lambda=Tavg/4+s*Ravg/4-V
Rsolution=2*sy.diff(V,s)+4*DF/s
combined=sy.simplify((Lambda+V).subs(Ravg,Rsolution))
check('full trace and Planck variation elimination',sy.simplify(combined-(Tavg/4+s*sy.diff(V,s)/2+DF))==0)
check('power law residual coefficient',sy.simplify(s*sy.diff(V,s)/2-n*V/2)==0)
check('Planck squared power retains flux energy',sy.simplify((s*sy.diff(V,s)/2-V).subs(n,2))==0)
check('unscaled flux erased by projection',sy.diff(V.subs(n,0),s)==0)

Evac,tauavg,tau=sy.symbols('Evac tauavg tau',real=True)
Lv=combined.subs(Tavg,-4*Evac+tauavg)-V
metric_rhs=sy.simplify(tau-Evac-(Lv+V))
check('matter vacuum cancels after full auxiliary variation',sy.simplify(metric_rhs-(tau-tauavg/4-n*V/2-DF))==0)
Efun=sy.Function('E')(Q)
f=sy.diff(V+W+Efun,Q)
check('Q dependent vacuum derivative retained',sy.simplify(f-sy.diff(V+W,Q)-sy.diff(Efun,Q))==0)

Vfixed=V.subs(n,2)+W
HQp=sy.hessian(Vfixed,(Q,p))
det=sy.factor(HQp.det())
check('joint flux polarization determinant',sy.simplify(det-(6*alpha*p*(s/sref)**2/Q+3*alpha**2*p**4/Q**4))==0)
check('positive electric Legendre curvature',sy.simplify(sy.diff(Vfixed,Q,2)-((s/sref)**2+2*alpha*p**3/Q**3))==0)

dual=[]
for qval in (.1,1.,10.):
    for pval in (0.,.1,1.,10.):
        electric=qval-pval**3/qval**2
        recover=brentq(lambda qq:qq-pval**3/qq**2-electric,1e-10,max(100.,qval*100),xtol=1e-13,rtol=2e-14)
        check('Legendre inverse '+str((qval,pval)),abs(recover/qval-1)<1e-10)
        H=np.array([[1+2*pval**3/qval**3,-3*pval*pval/qval**2],[-3*pval*pval/qval**2,6*pval/qval]])
        check('sampled auxiliary convexity '+str((qval,pval)),np.linalg.eigvalsh(H)[0]>=-1e-13)
        dual.append(dict(Q=qval,p=pval,electric_field_strength=electric,recovered_Q=recover))

# Fixed flat-background scalar force equation from the same W, with the
# ordinary 1/r^2 piece retained and the 1/r coefficient separately stated.
C=1.;qb=1.;G=1.;kappa_target=.5
Gscalar=qb*qb/(4*math.pi*C)
GEinstein=G-Gscalar
check('positive Einstein coefficient after Newtonian force calibration',GEinstein>0)
s_reference=1/(8*math.pi*GEinstein)
aa=qb**3/(6*math.sqrt(2)*math.pi*C**3*G**1.5*kappa_target)
force=[]
for qval in (.1,1.,10.):
    for mass in (.1,1.,10.):
        radius=100.;D=qb*mass/(4*math.pi*radius**2)
        coefficient=math.sqrt(qb*mass*qval/(12*math.pi*C*aa))
        exact=coefficient/radius
        value=brentq(lambda pp:3*aa*pp*pp/qval-D/C,0.,max(1.,10*exact),xtol=1e-14)
        check('sourced local force root '+str((qval,mass)),abs(value/exact-1)<1e-9)
        v4_per_mass=(qb*coefficient/C)**2/mass
        a0=v4_per_mass/G
        vacuum=qval*qval/2
        kappa=a0/math.sqrt(G*vacuum)
        check('flux independent calibrated kappa '+str((qval,mass)),abs(kappa/kappa_target-1)<1e-13)
        energy=quad(lambda r:4*math.pi*r*r*aa*(coefficient/r)**3/qval,10.,1000.,epsabs=1e-12)[0]
        logenergy=4*math.pi*aa*coefficient**3/qval*math.log(100.)
        check('logarithmic excess force energy '+str((qval,mass)),abs(energy/logenergy-1)<1e-12)
        force.append(dict(Q=qval,baryon_mass=mass,alpha=aa,flux_vacuum=qval*qval/2,
            p_radius_coefficient=coefficient,v4_per_mass=v4_per_mass,kappa_calibrated=kappa,
            force_field_excess_energy_r10_to1000=energy))

# A normalized late de Sitter dust-average example, not native cosmology.
averages=[]
for duration in (1.,3.,10.):
    volume=math.expm1(3*duration)/3
    trace_average=-duration/volume
    independent=quad(lambda t:1.,0,duration)[0]/volume
    check('late de Sitter average '+str(duration),abs(trace_average+independent)<1e-14)
    averages.append(dict(H_times_duration=duration,dust_trace_average_over_initial_density=trace_average))
result=dict(action='Integral sqrt(-g)[s R/2-Lambda-Vn(s,Q)+Lm(g,psi,Q)] + f(Lambda/mu^4)F_Lambda + fhat(s/sref)F_s + Q F_Q, fixed-Q boundary Legendre term',
    Vn='Q^2(s/sref)^n/2',selected_power=2,
    matter_hypothesis='Lm independent of Lambda and s explicitly; covariant regulated matter and frame required; Q dependence allowed and retained in Q equation',
    projected_equation='s G = T-<trT>identity/4-[s d_s Vn/2+Delta_F]identity',
    physical_residual='n Vn/2+Delta_F+<tr(tau)>/4',
    checks=checks,dual_rows=dual,force_rows=force,late_average_rows=averages,
    Newtonian_dictionary=dict(G_lab=G,G_scalar=Gscalar,G_Einstein=GEinstein,s=s_reference,s_ref=s_reference,
        hypothesis='Unscreened static baryon coupling; scalar 1/r^2 force included once; no physical PPN/lensing fit claimed'),
    non_claims=['No predicted Q, kappa or auxiliary flux/history data','Choice W=alpha p^3/Q is a new functional input, not a microscopic derivation','No fixed-flux global solution, full RG/curvature/graviton protection, metric/interface modes or finite halo','Covariant preferred-frame matter and cold carrier-to-response matching remain open','No global novelty or full theory closure'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(controls=len(checks),dual_rows=dual,force_rows=force,late_average_rows=averages),indent=2))
