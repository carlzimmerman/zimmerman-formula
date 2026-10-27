"""Pole-free pair conversion and an isolated expanding MB gas comparison.

Production is NOT solved: the initial weighted yield and kinetic temperature
are specified. Fast 1<->2 chemical equilibrium is imposed and then audited.
The pair channel is evolved with reciprocal energy/number moments. An
instantaneous-neutrino-decoupling free-gas background is a declared input.
"""
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.interpolate import PchipInterpolator
from scipy.special import kve, roots_genlaguerre, roots_laguerre

out=Path(sys.argv[1]); assert out.is_dir()
base=Path(__file__).parent
previous=json.loads((base/'thermal_charge_run_002/results.json').read_text())
parameters=next(row['parameters'] for row in previous['phase_rows'] if row['parameters']['m']==.002)
m,M,g=parameters['m'],parameters['M'],parameters['g']
delta=M-2*m
mpl=1.2209e19
yield_total=.12/(2.742e8*m)
checks=[]
def check(name,value):
    checks.append({'name':name,'passed':bool(value)})
    assert value,name

# Exact angular denominator identity for Phi Phi* -> X X*.
for ss,mm,MM in ((F(100),F(1),F(4)),(F(30),F(1,4),F(2)),(F(1000),F(3),F(12))):
    # mm=m^2, MM=M^2, A=s/2-M^2, B^2=(s-4m^2)(s-4M^2)/4.
    aa=ss/2-MM; bb2=(ss-4*mm)*(ss-4*MM)/4
    check('pair denominator identity '+str((ss,mm,MM)),aa*aa-bb2==MM*MM+mm*(ss-4*MM)>0)

def pair_sigma(s,reverse=False):
    excess=s-4*M*M
    if excess<=0: return 0.
    ratio=math.sqrt((s-4*m*m)/excess)
    return g**4/(math.pi*s)*(ratio if reverse else 1/ratio)/(M**4+m*m*excess)

zn,zw=roots_laguerre(192)
for factor in (1.0001,1.1,2.,10.,100.):
    ss=4*M*M*factor
    pp=math.sqrt(ss/4-m*m); px=math.sqrt(ss/4-M*M)
    def angle(z):
        tt=m*m+M*M-ss/2+2*pp*px*z
        return 16*g**4/(tt-m*m)**2
    independent=quad(angle,-1,1,epsabs=1e-60,epsrel=2e-11)[0]/(32*math.pi*ss)*px/pp
    check('pair cross section angular check '+str(factor),abs(independent/pair_sigma(ss)-1)<1e-9)
    check('pair cross section detailed balance '+str(factor),
          abs(pair_sigma(ss)*(ss-4*m*m)/(pair_sigma(ss,True)*(ss-4*M*M))-1)<1e-13)

sigma_v_zero=g**4*math.sqrt(1-m*m/(M*M))/(2*math.pi*M**6)

class Rates:
    def __init__(self,n):
        self.nodes,self.weights=roots_genlaguerre(n,.5)
        self.enodes,self.eweights=roots_laguerre(n)
    def pair_reverse(self,T):
        x=M/T
        if x>1e7: return sigma_v_zero
        y=self.nodes
        ds=4*M*T*y+T*T*y*y
        ss=4*M*M+ds
        # Generalized Laguerre weight sqrt(y) exp(-y) removes the
        # threshold square root. Bessels are exponentially scaled.
        values=np.sqrt((ss-4*m*m)*(4*M*T+T*T*y))/(M**4+m*m*ds)*kve(1,2*x+y)
        return float(g**4*np.dot(self.weights,values)/(4*math.pi*M**4*kve(2,x)**2))
    def elastic_lower(self,T):
        # Opposite-charge sigma(s)>=lambda_floor^2/(pi s), no pole.
        x=m/T; y=self.enodes
        ds=4*m*T*y+T*T*y*y
        lf=parameters['total']-g*g/(M*M)
        return float(lf*lf*np.dot(self.eweights,ds*kve(1,2*x+y))/(4*math.pi*m**4*kve(2,x)**2))

rate64,rate128=Rates(64),Rates(128)
rate_comparisons=[]
for T in np.geomspace(m*1e-5,m*10,25):
    a,b=rate64.pair_reverse(T),rate128.pair_reverse(T)
    check('thermal pair rate quadrature T='+str(T),abs(a/b-1)<2e-6)
    rate_comparisons.append({'T_dark_GeV':float(T),'sigma_v_GeVminus2':a,'relative_refinement':a/b-1})
check('thermal pair rate NR limit',abs(rate128.pair_reverse(m*1e-6)/sigma_v_zero-1)<1e-5)

# Specified photon/electron/neutrino radiation background; SM entropy is
# conserved, neutrinos decouple instantly at visible 2 MeV. No QCD era.
me=.00051099895
def electromagnetic(T):
    yy=me/T
    energy=np.sqrt(zn*zn+yy*yy)
    stat=np.exp(zn-energy)/(1+np.exp(-energy))
    rho_e=4*T**4/(2*math.pi**2)*float(np.dot(zw,zn**2*energy*stat))
    p_e=4*T**4/(6*math.pi**2)*float(np.dot(zw,zn**4/energy*stat))
    rho_g=math.pi**2/15*T**4
    return rho_g+rho_e,(4*rho_g/3+rho_e+p_e)/T
def neutrinos(T): return 7*math.pi**2/40*T**4,7*math.pi**2/30*T**3

Ti,Tend,Tdec=.01,1e-6,.002
s0=electromagnetic(Ti)[1]+neutrinos(Ti)[1]
sdec_em=electromagnetic(Tdec)[1]
adec=(s0/(sdec_em+neutrinos(Tdec)[1]))**(1/3)
table=[]
for T in np.geomspace(Ti,Tend,500):
    rem,sem=electromagnetic(T)
    if T>=Tdec:
        a=(s0/(sem+neutrinos(T)[1]))**(1/3);Tnu=T
    else:
        a=adec*(sdec_em/sem)**(1/3);Tnu=Tdec*adec/a
    rnu,snu=neutrinos(Tnu)
    check('background entropy '+str(T),abs((sem+snu)*a**3/s0-1)<2e-13)
    hh=math.sqrt(8*math.pi*(rem+rnu)/(3*mpl*mpl))
    table.append((math.log(a),math.log(hh),math.log(T),math.log(Tnu)))
table=np.array(table)
H_of=PchipInterpolator(table[:,0],table[:,1]);Tv_of=PchipInterpolator(table[:,0],table[:,2])
Lend=float(table[-1,0])

def kinetic_energy_cv(mass,T):
    v=T/mass
    if v<.01:
        kin=mass*(1.5*v+15/8*v*v-15/8*v**3+135/128*v**4+45/32*v**5)
        cv=1.5+15/4*v-45/8*v*v+135/32*v**3+225/32*v**4
        return kin,cv
    x=mass/T
    rr=float(kve(1,x)/kve(2,x))
    derivative=rr*rr-float(kve(0,x)/kve(2,x))+rr/x
    return mass*(rr-1)+3*T,3-x*x*derivative

def thermo(w,T):
    aa=m*m*T*float(kve(2,m/T))/(2*math.pi**2)
    bb=M*M*T*float(kve(2,M/T))/(2*math.pi**2)*math.exp(-min(delta/T,750))
    y=2*w/(aa+math.sqrt(aa*aa+8*bb*w))
    n,b=aa*y,bb*y*y
    kphi,cvphi=kinetic_energy_cv(m,T)
    kx0,cvx=kinetic_energy_cv(M,T);kx=delta+kx0
    ke=n*kphi+b*kx
    press=(n+b)*T
    denom=n+4*b
    kw=(n*kphi+2*b*kx)/denom
    kt=n*cvphi+b*cvx+n*b*(2*kphi-kx)**2/(denom*T*T)
    return dict(n=n,b=b,y=y,kphi=kphi,kx=kx,ke=ke,pressure=press,kw=kw,kt=kt)

GammaX=g*g/(8*math.pi*M)*math.sqrt(1-4*m*m/(M*M))
def evolve(initial_ratio,enabled,rr,rtol):
    def evaluate(l,variables):
        Y=yield_total*math.exp(float(variables[0]));T=m*math.exp(float(variables[1]))
        entropy=s0*math.exp(-3*l);w=Y*entropy/2;H=math.exp(float(H_of(l)))
        st=thermo(w,T);n,b,y=st['n'],st['b'],st['y']
        # P=gamma_eq(zPhi^2-zX^2); zX=zPhi^2 from fast decays.
        # Exponentially scaled densities avoid cancellation at T<<m.
        if enabled and b>0:
            B=b/(y*y)
            P=B*B*rr.pair_reverse(T)*y*y*(math.exp(-min(2*m/T,750))-y*y)
        else: P=0.
        dlnY=P/(H*w)
        dT=(-3*st['pressure']+3*n*b/(n+4*b)*(st['kx']-2*st['kphi'])
            -P/H*(m+st['kw']))/st['kt']
        return np.array([dlnY,dT/T]),(Y,T,w,H,P,st)
    sol=solve_ivp(lambda l,q:evaluate(l,q)[0],(0,Lend),(0,math.log(initial_ratio)),
                  method='Radau',rtol=rtol,atol=rtol*.03,dense_output=True,max_step=.12)
    check('ODE success ratio=%g pair=%s'%(initial_ratio,enabled),sol.success)
    logs=np.linspace(0,Lend,401)
    samples=[]
    for l in logs:
        deriv,(Y,T,w,H,P,st)=evaluate(l,sol.sol(l))
        elastic=st['n']*rr.elastic_lower(T)/H
        decay=GammaX*float(kve(1,M/T)/kve(2,M/T))/H
        speed_scale=1+abs(float(deriv[0]))+abs(float(deriv[1]))
        samples.append(dict(log_a=float(l),T_visible_GeV=math.exp(float(Tv_of(l))),
                 T_dark_GeV=T,Y_weighted_total=Y,weighted_yield_ratio=Y/yield_total,
                 source_fraction_of_weighted_count=2*st['b']/w,
                 maximum_MB_occupation=st['y'],elastic_lower_over_H=elastic,
                 decay_over_H=decay,elastic_over_evolution_rate=elastic/speed_scale,
                 decay_over_evolution_rate=decay/speed_scale,
                 w_pressure=st['pressure']/(m*w+st['ke']),P_over_Hw=P/(H*w),
                 entropy_per_sign=st['ke']/T+st['n']+st['b']-w*math.log(st['y']),
                 comoving_entropy_production_per_log_a=-math.exp(3*l)*(math.log(st['y'])+m/T)*P/H))
    first=evaluate(0,sol.sol(0))[1];last=evaluate(Lend,sol.sol(Lend))[1]
    u0=m*first[2]+first[5]['ke'];uend=m*last[2]+last[5]['ke']
    work=quad(lambda l:3*math.exp(3*l)*evaluate(l,sol.sol(l))[1][5]['pressure'],
              0,Lend,epsabs=u0*1e-10,epsrel=2e-7,limit=200)[0]
    energy_residual=(math.exp(3*Lend)*uend-u0+work)/u0
    number=quad(lambda l:math.exp(3*l)*evaluate(l,sol.sol(l))[1][4]/evaluate(l,sol.sol(l))[1][3],
                0,Lend,epsabs=first[2]*1e-10,epsrel=2e-7,limit=200)[0]
    number_residual=(last[2]*math.exp(3*Lend)-first[2]-number)/first[2]
    entropy_initial=samples[0]['entropy_per_sign']
    entropy_final=samples[-1]['entropy_per_sign']*math.exp(3*Lend)
    def entropy_source(l):
        _,(Y,T,w,H,P,st)=evaluate(l,sol.sol(l))
        return -math.exp(3*l)*(math.log(st['y'])+m/T)*P/H
    entropy_gain=quad(entropy_source,0,Lend,epsabs=entropy_initial*1e-10,epsrel=2e-7,limit=200)[0]
    entropy_residual=(entropy_final-entropy_initial-entropy_gain)/entropy_initial
    check('entropy-production invariant ratio=%g pair=%s'%(initial_ratio,enabled),abs(entropy_residual)<3e-6)
    check('nonnegative collision entropy production ratio=%g pair=%s'%(initial_ratio,enabled),
          min(s['comoving_entropy_production_per_log_a'] for s in samples)>-entropy_initial*1e-12)
    check('energy-work invariant ratio=%g pair=%s'%(initial_ratio,enabled),abs(energy_residual)<3e-6)
    check('weighted number invariant ratio=%g pair=%s'%(initial_ratio,enabled),abs(number_residual)<3e-6)
    if not enabled:
        check('weighted yield fixed with pair off ratio=%g'%initial_ratio,abs(last[0]/first[0]-1)<1e-12)
    return dict(initial_Tdark_over_m=initial_ratio,pair_enabled=enabled,
                final_yield_ratio=last[0]/yield_total,final_T_dark_GeV=last[1],
                initial_energy_ceiling_on_yield_ratio=u0/(m*first[2]),
                peak_yield_ratio=max(x['weighted_yield_ratio'] for x in samples),
                final_comoving_entropy_ratio=entropy_final/entropy_initial,
                entropy_production_relative_residual=entropy_residual,
                energy_work_relative_residual=energy_residual,weighted_number_relative_residual=number_residual,
                max_MB_occupation=max(x['maximum_MB_occupation'] for x in samples),
                min_elastic_over_evolution_rate=min(x['elastic_over_evolution_rate'] for x in samples),
                min_decay_over_evolution_rate=min(x['decay_over_evolution_rate'] for x in samples),
                nfev=sol.nfev,samples=samples)

runs=[]
for ratio in (.3,1.,3.):
    runs.append(evolve(ratio,True,rate64,2e-7))
    runs.append(evolve(ratio,False,rate64,2e-7))
refined=evolve(.3,True,rate128,2e-9)
check('ODE and rate joint refinement yield',abs(refined['final_yield_ratio']/runs[0]['final_yield_ratio']-1)<2e-5)
check('ODE and rate joint refinement temperature',abs(refined['final_T_dark_GeV']/runs[0]['final_T_dark_GeV']-1)<2e-5)
for r in runs:
    # A failed physical-closure diagnostic is a result, not a numerical
    # solver bug. Keep the ORIGINAL thresholds and report failures.
    r['reduced_model_scope_gates']={
        'MB_occupation_below_0p02':r['max_MB_occupation']<.02,
        'source_decay_over_evolution_above_1e5':r['min_decay_over_evolution_rate']>1e5,
        'elastic_lower_over_evolution_above_10':r['min_elastic_over_evolution_rate']>10}
    check('positive energy ceiling ratio=%g pair=%s'%(r['initial_Tdark_over_m'],r['pair_enabled']),
          r['peak_yield_ratio'] <= r['initial_energy_ceiling_on_yield_ratio']*(1+1e-7))

result=dict(verdict='Energy-conserving partial-equilibrium expanding-gas comparison; pair conversion included explicitly, physical production and full collision hierarchy remain open',
    parameters=parameters,initial_total_weighted_yield=yield_total,
    initial_visible_temperature_GeV=Ti,final_visible_temperature_GeV=Tend,
    background='photon/electron ideal gas plus three massless neutrinos; instantaneous decoupling at 2 MeV; radiation H; visible entropy conserved',
    sigma_v_XXbar_to_PhibarPhi_zero_GeVminus2=sigma_v_zero,
    rate_refinement=rate_comparisons,runs=runs,refined_run=refined,checks=checks,
    failed_scope_gates=[dict(initial_Tdark_over_m=r['initial_Tdark_over_m'],pair_enabled=r['pair_enabled'],
                            gate=k) for r in runs for k,v in r['reduced_model_scope_gates'].items() if not v],
    non_claims=['Initial yield and temperature are specified, not a completed Higgs production solution',
       'Fast common MB kinetic state and source partial chemical equilibrium are asymptotic closures, with timescale diagnostics rather than full momentum verification',
       'No full Bose statistics, medium masses, all irreducible multiparticle channels or RIS-subtracted finite-momentum hierarchy',
       'No observational relic/coldness or galaxy/gravity closure established','No global novelty claim'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({**{k:v for k,v in result.items() if k not in ('runs','refined_run','checks','rate_refinement')},
                  'run_summaries':[{k:v for k,v in r.items() if k!='samples'} for r in runs],
                  'refined_summary':{k:v for k,v in refined.items() if k!='samples'}},indent=2))
print('All %d bounded controls passed.'%len(checks))
