"""Independent checks on modified component diagnostics and a local coldness ceiling."""
import json,sys
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent; O=P/sys.argv[1]; O.mkdir(exist_ok=True)
rows={}; checks={}
for run in ['late_conversion_probe_run','late_conversion_refine_run','late_conversion_96_run']:
    p=P/run/'results.json'
    if not p.exists(): continue
    result=json.loads(p.read_text())
    for name,c in result['cases'].items():
        h=np.genfromtxt(P/run/(name+'.csv'),delimiter=',',names=True)
        ec=h['phi_gradient']+h['phi_kinetic_physical']+h['phi_potential']+h['X_kinetic']+h['X_gradient']+h['X_potential']+h['interaction']
        err=float(np.max(abs(ec-h['Econf']))/h['Econf'][0]);checks[run+'/'+name+'_component_sum']=err<1e-12
        # Reconstruct final Hamiltonian independently from full saved arrays.
        raw=np.fromfile(P/run/(name+'_initial.bin'),dtype='<f8'); n=int(raw[0]);L,dt,end,b,mp,mx,cc,quart=raw[1:9]
        q,v=np.fromfile(P/run/(name+'_final.bin'),dtype='<f8').reshape(2,4,n,n,n)
        r=q[0]**2+q[1]**2; pot=.5*mp**2*r+.5*mx**2*(q[2]**2+q[3]**2)+.25*r*r+cc*(q[2]*(q[0]**2-q[1]**2)+2*q[3]*q[0]*q[1])
        ep=float(np.mean(pot+.5*np.sum(v*v,axis=0)))
        ep+=sum(.5*np.mean(np.sum((np.roll(q,1,axis=d)-q)**2,axis=0))/(L/n)**2 for d in (1,2,3))
        checks[run+'/'+name+'_independent_final_E']=abs(ep-h['Econf'][-1])/abs(ep)<1e-12
        # Free-mode occupation proxy; meaningful only for weakly interacting high-k modes.
        fq=np.fft.fftn(q[:2],axes=(1,2,3))/n**3;fv=np.fft.fftn(v[:2],axes=(1,2,3))/n**3
        ki=2*np.pi*np.fft.fftfreq(n,d=L/n);kg=np.meshgrid(ki,ki,ki,indexing='ij');k2=sum(4*np.sin(x*L/n/2)**2/(L/n)**2 for x in kg)
        omega=np.sqrt(k2+mp*mp);efree=.5*np.sum(abs(fv)**2+omega**2*abs(fq)**2,axis=0)
        occupation=L**3/.00881292*efree/(2*omega)
        rows[run+'/'+name]={'component_relative_error':err,'independent_final_E':ep,'free_energy_fraction_with_occupation_proxy_below_1':float(efree[occupation<1].sum()/efree.sum()),'free_energy_fraction_with_occupation_proxy_below_10':float(efree[occupation<10].sum()/efree.sum()),'occupation_scope':'Free-mode, two-real-component average; not a self-consistent quasiparticle spectrum or vacuum-subtracted quantum measurement.'}
# Analytic benchmark numbers: these are conditional ceilings and free redshift only.
s=json.loads((P/'screening_exit_bound_v2_run/results.json').read_text());a=s['probe']['a'];A=s['probe']['X_envelope_GeV']
m=.001;M=2*m*np.sqrt(1+.02**2);g=2.168e-6;lam=.00881292;H=1.3445177278709404e10/a**2
T=(90/(np.pi**2*106.75))**.25*np.sqrt(2.435e18*H); entropy=2*np.pi**2/45*106.75*T**3
rho=M*M*A*A; Gamma=g*g/(8*np.pi*M)*np.sqrt(1-4*m*m/(M*M))
scales={'T_visible_GeV':T,'s_visible_GeV3':entropy,'rhoX_GeV4':rho,'all_X_vacuum_daughters_Y_if_number_preserved':2*rho/M/entropy,'target_Y':4.37e-7,'first_valley_depth_fraction':g*g/(lam*M*M),'four_cycles_Hdt':H*8*np.pi/M,'four_cycles_Gamma_dt':Gamma*8*np.pi/M,'crossing_nonadiabatic_scale_GeV':(2*g*A*M)**(1/3),'p_at_visible_0p8eV_over_p_at_probe':(.8e-9/T)*(3.91/106.75)**(1/3)}
# Exact instantaneous energy identity: dEX/dt=-c <xdot(f1^2-f2^2)+2 ydot f1 f2>.
# Finite-difference gradient check at a generic small 2^3 configuration.
rng=np.random.default_rng(91);q=rng.normal(size=(4,2,2,2));v=rng.normal(size=q.shape);cc=.003;mp=.02;mx=.04
f,h,x,y=q;r=f*f+h*h
U=lambda z:np.mean(.5*mp*mp*(z[0]**2+z[1]**2)+.5*mx*mx*(z[2]**2+z[3]**2)+.25*(z[0]**2+z[1]**2)**2+cc*(z[2]*(z[0]**2-z[1]**2)+2*z[3]*z[0]*z[1]))
grad=np.array([mp*mp*f+r*f+2*cc*(x*f+y*h),mp*mp*h+r*h+2*cc*(-x*h+y*f),mx*mx*x+cc*(f*f-h*h),mx*mx*y+2*cc*f*h])
fd=(U(q+1e-5*v)-U(q-1e-5*v))/(2e-5); exact=np.mean(np.sum(grad*v,axis=0));checks['potential_directional_gradient']=abs(fd-exact)<1e-7
ann=json.loads((P/'highH_annihilation_gate_run/results.json').read_text())
anchor=ann['counterfactual_reservoir_anchors'][2]
window=[]
for mu_ratio in [.6,.75,.95]:
    phase=np.sqrt(1-mu_ratio**2)/np.sqrt(1-m*m/M**2)
    window.append({'mPhi_effective_over_M':mu_ratio,'single_X_decay_closed':True,'pair_conversion_open':True,'Born_Gamma_over_H':anchor['Gamma_ann_over_H']*phase})
# Conditional late dilute NR sink, only after a hypothesized surviving daughter gas exists.
factor=np.sqrt(M*M/m**2-1)/.002
nlate=anchor['nX_total_GeV3']*(1-anchor['forward_only_X_survival_fraction'])/factor**3
Hlate=anchor['H_GeV']/factor**2
C=json.loads((P/'neutral_four_to_two_v2_run/results.json').read_text())['loss_coefficient_GeV_minus8']
late={'expansion_after_instant_pair_release':factor,'p_over_m':.002,'n_GeV3':nlate,'H_GeV':Hlate,'threshold_4to2_Gamma_over_H':C*nlate**3/Hlate,'forward_late_fractional_loss':-np.expm1(-np.log1p(3*C*nlate**3/(7*Hlate))/3),'scope':'Conditional balanced incoherent narrow cold daughter gas after uncomputed earlier conversion/cooling. Uses saved threshold coefficient; no bound on earlier hot losses.'}
checks['pair_open_single_closed']=all(.5<x['mPhi_effective_over_M']<1 for x in window)
out={'pair_conversion_window':window,'conditional_late_cold_sink':late,'checks':{k:bool(v) for k,v in checks.items()},'all_pass':bool(all(checks.values())),'independent_diagnostics':rows,'conditional_scales':scales,'scope':'No conversion rate extrapolation; all-X daughters is counterfactual number-preserving decay yield, not calculated survival. Cooling factor only after interactions cease.'}
(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
