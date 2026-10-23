"""Conditional thermal branch, with fast X<->Phi Phi chemical equilibrium.
No claim that the saved coherent source reaches this branch. MB kinetic
closure and partial collision network are explicit approximation choices.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.special import kve,kv
from scipy.interpolate import PchipInterpolator
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
m=.001;M=2*m*np.sqrt(1+.02**2);g=2.168e-6;lam=.00881292;delta=M-2*m
rates=json.loads((P/'thermal_recycling_rates_run/results.json').read_text());rr=rates['rates'];theta=np.array([r['T_over_m'] for r in rr]);cp=PchipInterpolator(np.log(theta),np.log([r['C_contact'] for r in rr]));sp=PchipInterpolator(np.log(theta),np.log([r['pair_sigma_v'] for r in rr]))
sv0=rates['pair_threshold'];C0=rates['contact_threshold']

def rate(T):
 t=T/m
 if t<theta[0]:
  # Smooth NR extension of the contact-only kernel, not the full-tree resonance.
  C=C0*np.exp((np.log(rr[0]['C_contact']/C0))*t/theta[0]);sv=sv0*np.exp(np.log(rr[0]['pair_sigma_v']/sv0)*t/theta[0])
 else:C=np.exp(cp(np.log(t)));sv=np.exp(sp(np.log(t)))
 return float(C),float(sv)

def species(T,eta,ma,q):
 x=ma/T;gap=ma-q*m;z=q*eta-gap/T
 n=ma*ma*T/np.pi**2*kve(2,x)*np.exp(z)
 if x>100:
  # Mean kinetic energy and derivative through O((T/m)^3).
  kin=1.5*T+15*T*T/(8*ma)-15*T**3/(8*ma*ma)
  dedT=1.5+15*T/(4*ma)-45*T*T/(8*ma*ma)
 else:
  ratio=kve(1,x)/kve(2,x); kin=ma*(ratio-1)+3*T
  # d(K1/K2)/dx from exact Bessel recurrences.
  rprime=-.5*(1+kve(0,x)/kve(2,x))+.5*ratio*(ratio+kve(3,x)/kve(2,x))
  dedT=3-x*x*rprime
 e=gap+kin
 return n,e,dedT

def state(T,eta):
 n,k,d=species(T,eta,m,1);nx,kx,dx=species(T,eta,M,2)
 W=n+2*nx;U=n*k+nx*kx;pr=T*(n+nx)
 J=np.array([[(n*k+2*nx*kx)/T,n+4*nx], [n*(k*k/T+T*d)+nx*(kx*kx/T+T*dx),n*k+2*nx*kx]])
 return n,nx,W,U,pr,J

# Exact BE chemical-equilibrium energy and entropy for initial energy matching.
def be(T):
 rho=0.;press=0.
 for ma in [m,M]:
  x=ma/T
  fun=lambda y:np.sqrt(y*y+x*x)
  rho+=T**4/np.pi**2*quad(lambda y:y*y*fun(y)/np.expm1(fun(y)),0,80,epsabs=1e-9,epsrel=1e-9)[0]
  press+=T**4/(3*np.pi**2)*quad(lambda y:y**4/fun(y)/np.expm1(fun(y)),0,80,epsabs=1e-9,epsrel=1e-9)[0]
 return rho,(rho+press)/T

source=json.loads((P/'highH_annihilation_gate_run/results.json').read_text())
anchor=source['counterfactual_reservoir_anchors'][2];Hanchor=anchor['H_GeV'];rhoanchor=anchor['rhoX_GeV4']
Tinit=brentq(lambda T:be(T)[0]-rhoanchor, m/10,10*m,xtol=1e-15);Sanchor=be(Tinit)[1]
# Match entropy into the MB late kinetic branch at T=m/2; this is a closure switch.
Ts=m/2;etas=-m/Ts;n,nx,W,U,pr,J=state(Ts,etas);Sstart=(m*W+U+pr)/Ts
astart=(Sanchor/Sstart)**(1/3);Hs=Hanchor/astart**2
visT=(90/(np.pi**2*106.75))**.25*np.sqrt(2.435e18*Hs);svis=2*np.pi**2/45*106.75*visT**3
Gamma=g*g/(8*np.pi*M)*np.sqrt(1-4*m*m/M**2)

def evolve(name,pc=1.,cc=1.,rtol=2e-7):
 calls=[0]
 def rhs(N,y):
  T=m*np.exp(y[0]);eta=y[1];n,nx,W,U,pr,J=state(T,eta);H=Hs*np.exp(-2*N);C,sv=rate(T)
  alpha=eta+m/T
  balance=-np.expm1(-2*alpha)
  R=(pc*.5*sv*nx*nx+cc*C*n**4)*balance
  # W is lost; its rest energy heats the remaining particles, conserving rho.
  rhs=np.array([-3*W-R/H,-3*(U+pr)+m*R/H])
  return np.linalg.solve(J,rhs)
 def done(N,y):return y[0]-np.log(1e-5)
 done.terminal=True;done.direction=-1
 sol=solve_ivp(rhs,(0,30),[np.log(Ts/m),etas],method='Radau',rtol=rtol,atol=[rtol*.01,rtol*.01],events=done,dense_output=True,max_step=.12)
 if not sol.success or len(sol.t_events[0])!=1:raise RuntimeError(sol.message)
 Ns=np.linspace(0,sol.t[-1],1201);ys=sol.sol(Ns);arr=[];maxBose=0;maxmass=0;minGamma=1e300
 for N,y in zip(Ns,ys.T):
  T=m*np.exp(y[0]);eta=y[1];n,nx,W,U,pr,J=state(T,eta);C,sv=rate(T);H=Hs*np.exp(-2*N);alpha=eta+m/T;f0=1/np.expm1(-eta)
  mass=2*lam*n*kve(1,m/T)/(m*kve(2,m/T));maxmass=max(maxmass,mass/(m*m*.02**2));maxBose=max(maxBose,f0);minGamma=min(minGamma,Gamma/H)
  Rpair=pc*.5*sv*nx*nx*(-np.expm1(-2*alpha));R4=cc*C*n**4*(-np.expm1(-2*alpha))
  deriv=rhs(N,y);drho=np.dot(J[1]+m*J[0],deriv);energyres=abs(drho+3*(m*W+U+pr))/(3*(m*W+U+pr))
  arr.append([N,T,eta,n,nx,W*np.exp(3*N)/svis,(Rpair+R4)/(H*W),Rpair/(H*W),R4/(H*W),energyres])
 arr=np.array(arr);np.savetxt(O/(name+'.csv'),arr,delimiter=',',header='N,T,eta,nPhi,nX,Yweighted,Gamma_net_over_H,pair_net_over_H,quartic_net_over_H,energy_residual',comments='')
 # At this endpoint X is negligible; use NR Maxwell moment for free cooling thereafter.
 N=Ns[-1];T=arr[-1,1];visible=visT*np.exp(-N)
 v_eq=np.sqrt(3*T/m)*(.8e-9/visible)*(3.91/106.75)**(1/3)
 row={'pair_multiplier':pc,'contact_multiplier':cc,'rtol':rtol,'Y_initial':float(arr[0,5]),'Y_final':float(arr[-1,5]),'fraction_initial_weighted_number':float(arr[-1,5]/arr[0,5]),'target_fraction':float(arr[-1,5]/4.37e-7),'final_X_weighted_fraction':float(2*arr[-1,4]/(arr[-1,3]+2*arr[-1,4])),'max_energy_equation_residual':float(arr[:,9].max()),'max_BE_zero_mode_occupation_diagnostic':float(maxBose),'max_Hartree_shift_over_decay_gap':float(maxmass),'min_vacuum_Gamma_over_H':float(minGamma),'final_N':float(N),'final_visible_T_GeV_constant_gstar':float(visible),'collisionless_rms_v_at_0p8eV':float(v_eq),'final_net_loss_over_H':float(arr[-1,6])}
 print(name,json.dumps(row),flush=True);return row
cases={}
for name,p,c,tol in [('full',1,1,2e-7),('fine',1,1,3e-8),('no_pair',0,1,2e-7),('no_direct4',1,0,2e-7),('contact10',1,10,2e-7),('contact0p1',1,.1,2e-7),('pair_half',.5,1,2e-7),('pair_twice',2,1,2e-7),('no_loss',0,0,2e-7)]:cases[name]=evolve(name,p,c,tol)
checks={'energy_equation':all(v['max_energy_equation_residual']<1e-9 for v in cases.values()),'refined_yield':abs(cases['fine']['Y_final']/cases['full']['Y_final']-1)<1e-4,'no_loss_number_conserved':abs(cases['no_loss']['fraction_initial_weighted_number']-1)<1e-4,'decay_open_Hartree_diagnostic':all(v['max_Hartree_shift_over_decay_gap']<1 for v in cases.values()),'final_X_negligible':all(v['final_X_weighted_fraction']<1e-10 for v in cases.values())}
out={'checks':{k:bool(v) for k,v in checks.items()},'all_pass':bool(all(checks.values())),'initial_BE_temperature_GeV':Tinit,'initial_dark_entropy_GeV3':Sanchor,'kinetic_start_a_over_anchor':astart,'kinetic_start_H_GeV':Hs,'cases':cases,'scope':'Conditional internally equilibrated source-energy branch. MB moment closure, rapid decay chemical equilibrium, inverse pair and inverse contact 2-to-4 via detailed balance. Missing thermalization derivation, full Bose collision terms, nonresonant cubic/RIS-complete higher reactions, coherent dynamics and realistic gstar. NOT full high-H surviving yield.'}
(O/'results.json').write_text(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
