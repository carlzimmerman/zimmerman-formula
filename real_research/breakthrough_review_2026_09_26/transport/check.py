#!/usr/bin/env python3
"""Exact transverse energy bridge and bounded self-gravitating resonance passage."""
import argparse,json,math,time
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
checks={}
def exact(name,x):
    x=sp.factor(x);assert x==0,(name,x);checks[name]='exact zero'
def yes(name,x):
    assert bool(x),name;checks[name]=True

# Exact equations use real canonical phi=(phi1,phi2), chi=(chi1,chi2), and s.
f1,f2,b1,b2,c1,c2,s,w1,w2,ws,H,p,g,m,mu,M,eps,Hd=sp.symbols(
    'f1 f2 b1 b2 c1 c2 s w1 w2 ws H p g m mu M eps Hd',real=True)
q1=c1+g*s*f1;q2=c2+g*s*f2
energy=(w1*w1+w2*w2+ws*ws+p*p*(c1*c1+c2*c2+s*s)
        +m*m*(q1*q1+q2*q2)+mu*mu*s*s)/2
coords=[c1,c2,s];vel=[w1,w2,ws]
forces=[-3*H*vel[i]-sp.diff(energy,coords[i]) for i in range(3)]
edot=sum(sp.diff(energy,coords[i])*vel[i]+sp.diff(energy,vel[i])*forces[i]
         for i in range(3))+sp.diff(energy,p)*(-H*p)+sp.diff(energy,f1)*b1+sp.diff(energy,f2)*b2
work=g*m*m*s*(q1*b1+q2*b2)
exact('exact physical transverse energy identity',edot+3*H*sum(v*v for v in vel)
      +H*p*p*sum(x*x for x in coords)-work)
charge=c2*w1-c1*w2
qdot=sum(sp.diff(charge,coords[i])*vel[i]+sp.diff(charge,vel[i])*forces[i] for i in range(3))
source=g*m*m*s*(c1*f2-c2*f1)
exact('exact light-component expanding continuity',qdot+3*H*charge-source)
exact('Young work bound square completion',(m*m*q1*q1+mu*mu*s*s)/2-m*mu*s*q1-(m*q1-mu*s)**2/2)
# Background pump Lyapunov identity; Hdot remains explicit and nonpositive.
Ep=(b1*b1+b2*b2+M*M*(f1*f1+f2*f2))/2
Ly=Ep+eps*(f1*b1+f2*b2)+sp.Rational(3,2)*eps*H*(f1*f1+f2*f2)
Ld=sum(sp.diff(Ly,x)*v for x,v in [(f1,b1),(f2,b2),(b1,-3*H*b1-M*M*f1),
                                  (b2,-3*H*b2-M*M*f2),(H,Hd)])
exact('pump exponential Lyapunov identity',Ld+(3*H-eps)*(b1*b1+b2*b2)
      +eps*(M*M-sp.Rational(3,2)*Hd)*(f1*f1+f2*f2))
# Leading adiabatic redshift sweep (h denotes gamma*m^2*|Psi|).
hh,wc,wr=sp.symbols('h wc wr',positive=True)
adiabatic_slope=H*(p*p*(1/wc+1/wr)+3*hh*hh/(m*m*wr))
exact('adiabatic detuning redshift identity',adiabatic_slope
      -H*p*p/wc-(H*p*p+3*H*hh*hh/(m*m))/wr)
aa,kk,mm,hhub=sp.symbols('a k mass H0',positive=True)
primitive=-(sp.sqrt(mm*mm+(kk/aa)**2)-mm)/(hhub*kk)
exact('massive group-ray horizon primitive',sp.diff(primitive,aa)
      -kk/(hhub*aa**2*sp.sqrt(mm*mm*aa*aa+kk*kk)))

parameters=dict(M=3.,m=1.,mu=.5,gamma=.2,V0=.01,A=1.,k=1.6,a_end=2.)
MM=parameters['M'];mm=parameters['m'];uu=parameters['mu'];gg=parameters['gamma']
vv=parameters['V0'];amp=parameters['A'];kk=parameters['k']
J=np.block([[np.zeros((3,3)),np.eye(3)],[-np.eye(3),np.zeros((3,3))]])
Qchi=np.zeros((6,6));Qchi[1,3]=Qchi[3,1]=.5;Qchi[0,4]=Qchi[4,0]=-.5

def diagnostics_for_background(state,P):
    phi=state[:2];v=state[2:4];hub=state[4];al=state[5];mom=kk*math.exp(-al)
    hd=-float(v@v)/(2*P*P)
    hdd=(3*hub*float(v@v)+MM*MM*float(phi@v))/(P*P)
    d=1.5*hd+2.25*hub*hub;dd=1.5*hdd+4.5*hub*hd
    radius2=float(phi@phi);hh=gg*mm*mm*math.sqrt(radius2/2)
    hhprime=hh*float(phi@v)/radius2
    omega=(phi[1]*v[0]-phi[0]*v[1])/radius2
    omegaprime=omega*(-3*hub-2*float(phi@v)/radius2)
    wc=math.sqrt(mm*mm+mom*mom-d)
    wr=math.sqrt(uu*uu+mom*mom-d+2*hh*hh/(mm*mm))
    delta=omega-wc-wr;coupling=hh/(2*math.sqrt(wc*wr))
    dprime=omegaprime+(2*hub*mom*mom+dd)/(2*wc)+(2*hub*mom*mom+dd-4*hh*hhprime/(mm*mm))/(2*wr)
    return dict(p=mom,H=hub,Hdot=hd,d=d,h=hh,omega_pump=omega,omega_chi=wc,
                omega_s=wr,delta=delta,coupling=coupling,delta_dot=dprime)

def run(P):
    initial_H=math.sqrt((2*MM*MM*amp*amp+vv)/(3*P*P-2.25*amp*amp))
    bg0=np.array([math.sqrt(2)*amp,0,-1.5*initial_H*math.sqrt(2)*amp,
                  -MM*math.sqrt(2)*amp,initial_H,0.])
    # Two exact 6x6 transverse propagators: coupled and zero-coupling control.
    y0=np.concatenate([bg0,np.eye(6).ravel(),np.eye(6).ravel(),np.array([0.])])
    def rhs(t,Y):
        phi=Y[:2];v=Y[2:4];hub=Y[4];al=Y[5]
        hd=-float(v@v)/(2*P*P);p2=kk*kk*math.exp(-2*al);d=1.5*hd+2.25*hub*hub
        out=np.empty_like(Y);out[:2]=v;out[2:4]=-3*hub*v-MM*MM*phi
        out[4]=hd;out[5]=hub
        for index,coupling in enumerate([gg,0.]):
            K=np.diag([mm*mm+p2-d,mm*mm+p2-d,uu*uu+p2-d+coupling*coupling*mm*mm*float(phi@phi)])
            K[:2,2]=coupling*mm*mm*phi;K[2,:2]=coupling*mm*mm*phi
            start=6+36*index;F=Y[start:start+36].reshape(6,6)
            out[start:start+18]=F[3:].ravel()
            out[start+18:start+36]=(-K@F[:3]).ravel()
        out[-1]=abs(gg)*mm/uu*float(np.linalg.norm(v))
        return out
    def endpoint(t,Y):return Y[5]-math.log(parameters['a_end'])
    endpoint.terminal=True;endpoint.direction=1
    start=time.perf_counter()
    sol=solve_ivp(rhs,[0,2e3*(P/1000.)],y0,method='DOP853',rtol=2e-10,atol=2e-12,
                  max_step=.25,dense_output=True,events=endpoint)
    yes('self-consistent background reaches a=2 P'+str(P),sol.success and len(sol.t_events[0])==1)
    T=float(sol.t_events[0][0]);times=np.linspace(0,T,3001);Y=sol.sol(times)
    bg=Y[:6];E=.5*np.sum(bg[2:4]**2,axis=0)+.5*MM*MM*np.sum(bg[:2]**2,axis=0)
    C=3*P*P*bg[4]**2-E-vv
    Q=np.exp(3*bg[5])*(bg[1]*bg[2]-bg[0]*bg[3])
    cerror=float(np.max(np.abs(C))/(E[0]+vv));qerror=float(np.max(np.abs(Q/Q[0]-1)))
    yes('background Friedmann constraint P'+str(P),cerror<1e-7)
    yes('background comoving pump charge P'+str(P),qerror<1e-7)
    omega0=np.array([math.sqrt(mm*mm+kk*kk)]*2+[math.sqrt(uu*uu+kk*kk)])
    pf=kk/parameters['a_end'];omegaf=np.array([math.sqrt(mm*mm+pf*pf)]*2+[math.sqrt(uu*uu+pf*pf)])
    W0=np.diag(np.r_[omega0,1/omega0]);Wf=np.diag(np.r_[omegaf,1/omegaf])
    W0invhalf=np.diag(1/np.sqrt(np.diag(W0)))
    neutral=np.zeros((6,2));neutral[2,0]=math.sqrt(2/omega0[2]);neutral[5,1]=math.sqrt(2*omega0[2])
    results={}
    for index,label in enumerate(['coupled','uncoupled']):
        F=Y[6+36*index:6+36*(index+1),-1].reshape(6,6)
        actionmatrix=W0invhalf@F.T@Wf@F@W0invhalf
        actiongain=float(np.linalg.eigvalsh(actionmatrix)[-1])
        symerror=float(np.max(np.abs(F.T@J@F-J)))
        charges=np.linalg.eigvalsh(neutral.T@F.T@Qchi@F@neutral)
        results[label]=dict(max_reference_action_gain=actiongain,
                            max_reference_amplitude_gain=math.sqrt(actiongain),
                            symplectic_error=symerror,
                            neutral_unit_action_final_comoving_charge_range=charges.tolist())
        yes(label+' symplectic propagator P'+str(P),symerror<2e-6)
    yes('zero coupling creates no light charge P'+str(P),
        np.max(np.abs(results['uncoupled']['neutral_unit_action_final_comoving_charge_range']))==0)
    yes('uncoupled action stays near adiabatic normalization P'+str(P),results['uncoupled']['max_reference_action_gain']<1.03)
    # Exact physical energy metric from rescaled (X,Xdot) coordinates.
    def energy_metric(state):
        phi=state[:2];hub=state[4];al=state[5];p2=kk*kk*math.exp(-2*al)
        K=np.diag([mm*mm+p2,mm*mm+p2,uu*uu+p2+gg*gg*mm*mm*float(phi@phi)])
        K[:2,2]=gg*mm*mm*phi;K[2,:2]=gg*mm*mm*phi
        return math.exp(-3*al)*np.block([[K+2.25*hub*hub*np.eye(3),-1.5*hub*np.eye(3)],[-1.5*hub*np.eye(3),np.eye(3)]])
    G0=energy_metric(bg0);eig,vec=np.linalg.eigh(G0);inv=(vec/np.sqrt(eig))@vec.T
    F=Y[6:42,-1].reshape(6,6)
    physicalgain=float(np.linalg.eigvalsh(inv@F.T@energy_metric(bg[:,-1])@F@inv)[-1])
    envelope=float(Y[-1,-1])
    yes('rigorous finite-time energy envelope P'+str(P),math.log(physicalgain)<=envelope+1e-8)
    ds=[diagnostics_for_background(col,P) for col in bg.T]
    delta=np.array([x['delta'] for x in ds])
    brackets=[(times[i],times[i+1]) for i in range(len(times)-1) if delta[i]<0<=delta[i+1]]
    yes('one resolved resonance passage P'+str(P),len(brackets)==1)
    crossing=brentq(lambda t:diagnostics_for_background(sol.sol(t)[:6],P)['delta'],*brackets[0],xtol=1e-11)
    cross=diagnostics_for_background(sol.sol(crossing)[:6],P)
    def edge(t,sign):
        d=diagnostics_for_background(sol.sol(t)[:6],P);return d['delta']+sign*2*d['coupling']
    tin=brentq(lambda t:edge(t,1),0,crossing)
    tout=brentq(lambda t:edge(t,-1),crossing,T)
    def integrand(t):
        d=diagnostics_for_background(sol.sol(t)[:6],P)
        return math.sqrt(max(0,d['coupling']**2-d['delta']**2/4))
    exponent,error=quad(integrand,tin,tout,epsabs=1e-9,epsrel=1e-8,limit=100)
    sweep_adiabatic=cross['H']*(cross['p']**2*(1/cross['omega_chi']+1/cross['omega_s'])
                     +3*cross['h']**2/(mm*mm*cross['omega_s']))
    cross.update(time=crossing,scale_factor=math.exp(sol.sol(crossing)[5]),
                 peak_growth_over_H=cross['coupling']/cross['H'],
                 local_passage_exponent=math.pi*cross['coupling']**2/abs(cross['delta_dot']),
                 adiabatic_delta_dot=sweep_adiabatic,
                 integrated_RWA_unstable_exponent=exponent,
                 exponent_quadrature_error=error,RWA_band_times=[tin,tout])
    return dict(Mpl=P,initial_H=initial_H,end_time=T,runtime_seconds=time.perf_counter()-start,
                function_evaluations=sol.nfev,constraint_error_initial_relative=cerror,
                pump_comoving_charge_error=qerror,propagators=results,
                exact_max_physical_energy_gain=physicalgain,rigorous_log_energy_gain_upper_bound=envelope,
                crossing=cross)

rows=[run(100.),run(1000.)]
yes('tenfold gravity time scale changes passage amplification',
    rows[1]['propagators']['coupled']['max_reference_action_gain']>
    5*rows[0]['propagators']['coupled']['max_reference_action_gain'])
yes('growth faster than H is insufficient for large passage exponent',
    rows[0]['crossing']['peak_growth_over_H']>1 and rows[0]['crossing']['integrated_RWA_unstable_exponent']<.5)
output=dict(result='accepted bounded expanding-resonance and exact energy-bridge audit',
            check_count=len(checks),checks=checks,parameters=parameters,runs=rows,
            non_claims=[
                'Exact transverse linearization around a self-consistent nonlinear pump, not finite-amplitude depletion',
                'Reference action singular-value gain is a specified norm, not a halo clearing fraction',
                'RWA passage exponent is an approximation and not equated to exact coherent norm gain',
                'No measured mass, Hubble ratio, initial charge or cosmological abundance is fitted',
                'No whole-theory nonlinear or host scalar/tensor stability claim',
                'Physical dilution is distinct from boundary flux; no outgoing packet simulated'
            ])
Path(args.output).write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
