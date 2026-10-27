"""CE-FM-056: conversion clock and source-perturbation scope; no scorer run."""
import sys,json,math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
b=Path('campaign_fresh_gravity/CFG780_s8_cold_conversion')
stored=json.loads((b/'cfg780_results.json').read_text())
checks=[]
def ck(name,v):
    assert v,name
    checks.append(name)
a,H=sp.symbols('a H',positive=True)
# N=ln(a), adot=aH => dN/dt=H.
ck('proper time per log scale',sp.simplify((1/a)*(a*H)-H)==0)
B=.0484;C=.2596;OM=B+C;amount=C*(1-.894)
psi=lambda aa:.015*aa**(-2.7)/(1+(1/(2.9*aa))**5.6)
def calc(n,clock,conversion=True):
    aa=np.exp(np.linspace(math.log(1/9),0,n)); nn=np.log(aa)
    Er=np.sqrt(OM/aa**3+1-OM)
    rate=psi(aa)/Er/(aa if clock=='source_extra_1_over_a' else 1)
    cum=np.r_[0,np.cumsum(.5*(rate[1:]+rate[:-1])*np.diff(nn))];F=cum/cum[-1]
    lossamount=amount if conversion else 0
    matter=OM-lossamount*F
    loss=-np.gradient(matter,nn)
    vv=np.r_[0,np.cumsum(.5*(loss[1:]*aa[1:]**-3+loss[:-1]*aa[:-1]**-3)*np.diff(nn))]
    vv+=1-matter[-1]-vv[-1]
    EE=np.sqrt(matter/aa**3+vv)
    def growth(E,m):
        dl=np.gradient(np.log(E),nn);oo=m/aa**3/E**2
        sol=solve_ivp(lambda t,y:[y[1],-(2+np.interp(t,nn,dl))*y[1]+1.5*np.interp(t,nn,oo)*y[0]],(nn[0],0),[aa[0],aa[0]],rtol=1e-10,atol=1e-14,t_eval=nn)
        ck('background growth solver '+str((n,clock,conversion)),sol.success)
        return sol.y[0]
    gg=growth(EE,matter)/growth(Er,np.full(n,OM))
    return {'clock':clock,'grid':n,'g0':float(gg[-1]),'g05':float(np.interp(math.log(1/1.5),nn,gg)),'g1':float(np.interp(math.log(.5),nn,gg)),'V_start':float(vv[0]),'V_end':float(vv[-1]),'E_today':float(EE[-1]),'produced_vacuum':float(vv[-1]-vv[0]),'fraction_converted_by_z1':float(np.interp(math.log(.5),nn,F))}
old=calc(4001,'source_extra_1_over_a');new=calc(4001,'proper_time');fine=calc(8001,'proper_time');zero=calc(4001,'proper_time',False)
pr=stored['growth']['primary (cold-only, survival 0.894)']
for f in ['g0','g05','g1']:ck('source growth reproduced '+f,abs(old[f]-pr[f])<2e-7)
ck('zero conversion control',abs(zero['g0']-1)<1e-8)
for f in ['g0','g05','g1']:ck('proper-clock resolution '+f,abs(new[f]-fine[f])<2e-6)
for job in ['T12','T1x']:
    for tag,lab in [('unscaled','unscaled'),('primary','primary (cold-only, survival 0.894)'),('half','half amount (0.947)'),('proportional','proportional (eta 5.364, survival 0.911)')]:
        suffix='_T12' if job=='T12' else ''
        raw=json.loads((b/('rescore_'+job+'_'+tag+suffix+'.json')).read_text())
        for name,v in stored['rescore'][job+'|'+lab].items():
            fits=raw['runs'][name]['surveys']['KiDS']['fits']['IA']
            for field,key in [('chi2_F','F'),('chi2_S0','S0')]:ck('raw score '+job+' '+tag+' '+field,abs(v[field]-fits[key]['chi2'])<1e-10)
            ck('score difference '+job+' '+tag,abs(v['dchi2']-(v['chi2_F']-v['chi2_S0']))<1e-10)
# Perturbation source closure for one dust stock. delta_dot=-theta+q delta-S,
# S=deltaQ/rho; theta_dot=-2Htheta-Agrav delta, no extra momentum force.
t=sp.symbols('t',real=True);d=sp.Function('delta')(t);q=sp.Function('q')(t);S=sp.Function('S')(t)
HH,Ag=sp.symbols('H Agrav',positive=True)
theta=q*d-S-sp.diff(d,t)
expr=sp.expand(sp.diff(theta,t)+2*HH*theta+Ag*d)
expected=-sp.diff(d,t,2)+(q-2*HH)*sp.diff(d,t)+(sp.diff(q,t)+2*HH*q+Ag)*d-sp.diff(S,t)-2*HH*S
ck('general dust transfer equation',sp.simplify(expr-expected)==0)
ck('local per-mass transfer cancels',sp.simplify(expr.subs(S,q*d).doit()+sp.diff(d,t,2)+2*HH*sp.diff(d,t)-Ag*d)==0)
r=stored['rescore'];before=r['T1x|unscaled']['L100_N1024_canonical'];after=r['T1x|primary (cold-only, survival 0.894)']['L100_N1024_canonical']
cost=(after['chi2_F']-before['chi2_F'])/(-before['dchi2'])
res={'claim_id':'CE-FM-056','checks_passed':len(checks),'checks':checks,'source_clock':old,'proper_clock':new,'proper_clock_refined':fine,'zero_conversion':zero,'stored_T1x_gain_fraction_lost':cost,'stored_T1x_before':before,'stored_T1x_after':after,'scope':'Background clock countercontrol and raw JSON reconciliation only; no new shear likelihood, native simulation, source perturbation model or observational verdict.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
