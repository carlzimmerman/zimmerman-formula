import argparse,json,sys,importlib.util
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from scipy.special import zeta
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','today_normalization','Saha_is_last_scattering','number_is_effective_density'],default='none');args=ap.parse_args();checks=[];records=[]
def ck(n,b,detail=None):checks.append(dict(name=n,passed=bool(b),detail=detail))
def eq(n,e):e=s.simplify(e);ck(n,e==0,str(e))
# Exact SI h,k,c,e; CODATA2022 me,mp,Rinf. Binding is declared leading reduced-mass Coulomb.
h=6.62607015e-34;kb=1.380649e-23;c=299792458.;ev=1.602176634e-19;me=9.1093837139e-31;mp=1.67262192595e-27;Rinf=10973731.568157
chi=h*c*Rinf/(1+me/mp);T0=2.7255;eta=6.1e-10
ng=lambda T:16*np.pi*zeta(3)*(kb*T/(h*c))**3
rhog=lambda T:8*np.pi**5*(kb*T)**4/(15*h**3*c**3) # photon energy J/m3
Tstar=eta*mp*c*c*ng(1)/(100*rhog(1))
def logS(T):return 1.5*np.log(2*np.pi*me*kb*T/(h*h))-chi/(kb*T)-np.log(eta*ng(T))
def xe(T):
 L=logS(T)
 if L<0:return 2*np.exp(L/2)/(np.exp(L/2)+np.sqrt(np.exp(L)+4))
 return 2/(1+np.sqrt(1+4*np.exp(-L)))
milestones=[]
for x in [.9,.5,.1]:
 T=brentq(lambda T:logS(T)-np.log(x*x/(1-x)),2000,6000,xtol=1e-9);theta=chi/(kb*T);slope=x*(1-x)/(2-x)*(1.5-theta)
 ck('Saha_root_'+str(x),abs(xe(T)-x)<1e-11)
 milestones.append(dict(x_e=x,T_K=T,theta=theta,physical_a=T0/T,dx_dln_a=slope,relative_tracking_requirement=abs(slope)/x))
ck('half_temperature_well_below_binding',milestones[1]['theta']>40)
# Exact calibration plus local equilibrium tracking derivative.
bf,pf,T,Sx,X,theta,alpha,n,C=s.symbols('fb fg T S x theta alpha n C',positive=True)
star=s.symbols('Tstar',positive=True);eq('number_energy_calibration',(bf-pf*star/T).subs(T,star*pf/bf))
# Photon meanenergy=pi4/(30zeta3) kT; source fractions therefore Tref=Tstar fg/fb.
bare=eta*mp*c*c*ng(T0)/rhog(T0)/100
ck('today_allphotons_exceeds_totaldust',bare>1,bare)
q=s.symbols('q',positive=True);Saha=X**2/(1-X)
slope=X*(1-X)/(2-X)*(s.Rational(3,2)-theta)
eq('exact_Saha_tracking_derivative',(2/X+1/(1-X))*slope-(s.Rational(3,2)-theta))
R=alpha*n*(X**2-Sx*(1-X));eq('equilibrium_relaxation',s.diff(R,X).subs(Sx,Saha)-alpha*n*(2*X+Saha))
eq('rate_prefactor_derivative_at_equilibrium',R.subs(Sx,Saha))
Cx=s.Function('C')(X);eq('full_relaxation_with_x_dependent_escape',s.diff(Cx*R,X).subs(Sx,Saha)-Cx*alpha*n*(2*X+Saha))
base=Path(__file__).resolve().parent.parent/'curvature_carrier_radiation_matching_2026_10_06/self_consistent_history'
sp=importlib.util.spec_from_file_location('actual_bg',base/'equations.py');bg=importlib.util.module_from_spec(sp);sp.loader.exec_module(bg)
prior=json.loads((base/'runs/history_main_a/results.json').read_text());guards={int(r['xi']):np.exp(r['endpoint_x']) for r in prior['runs'] if r['method']=='DOP853' and r['rtol']==3e-10}
for fb,fg in [(1.,1.),(.16,.6)]:
 Tref=Tstar*fg/fb;a_ref=T0/Tref;targets=np.array([Tref/r['T_K'] for r in milestones]);cal=eta*mp*c*c*ng(Tref)/(100*rhog(Tref)/fg)
 ck(f'fraction_calibration_{fb}_{fg}',abs(cal/fb-1)<1e-12)
 for xi in [100,1000]:
  admitted=bool(min(targets)>guards[xi] and max(targets)<=1);upper=min(r['T_K'] for r in milestones)/Tstar;threshold=guards[xi]*max(r['T_K'] for r in milestones)/Tstar
  ck(f'exact_admission_inequality_{xi}_{fb}_{fg}',admitted==(threshold<fg/fb<=upper))
  rec=dict(xi=xi,fb=fb,fg=fg,Tref_K=Tref,physical_a_at_model1=a_ref,model_guard=guards[xi],physical_guard=a_ref*guards[xi],max_admitted_temperature=Tref/guards[xi],required_fg_over_fb=threshold,maximum_fg_over_fb=upper,all_Saha_milestones_before_guard=admitted,model_milestones=targets.tolist())
  if admitted:
   b0=bg.initial(xi);u0=bg.quantities(0,b0,xi);calls=[0]
   def fun(x,b):
    calls[0]+=1
    if calls[0]>15000:raise RuntimeError('declared RHS cap15000')
    return bg.rhs(x,b,xi)
   sol=solve_ivp(fun,(0,np.log(min(targets))),b0,method='DOP853',rtol=3e-10,atol=3e-15,t_eval=np.log(targets[::-1]))
   ck(f'background_integration_{xi}_{fb}_{fg}',sol.success and sol.nfev<15000,sol.nfev)
   vals=[bg.quantities(x,b,xi) for x,b in zip(sol.t,sol.y.T)];ck(f'positive_F_at_remapped_atoms_{xi}_{fb}_{fg}',min(v['F'] for v in vals)>0)
   ck(f'charge_at_remapped_atoms_{xi}_{fb}_{fg}',max(abs(v['Q']/u0['Q']-1) for v in vals)<1e-6)
   ck(f'constraint_at_remapped_atoms_{xi}_{fb}_{fg}',max(abs(v['friedmann'])/v['friedmann_scale'] for v in vals)<1e-12)
   rec['actual_background_nodes']=[dict(model_a=float(np.exp(x)),T_K=Tref/np.exp(x),F=float(v['F']),H_model=float(v['H']),carrier_EH_fraction=float(v['rho_carrier']/(3*v['H']**2))) for x,v in zip(sol.t,vals)]
  records.append(rec)
if args.control=='today_normalization':ck('false_present_allphotons_allbaryons_matching',bare<=1)
if args.control=='Saha_is_last_scattering':
 # Pure equilibrium algebra cannot yield opacity without supplied H/atomicrate inputs.
 H,ne,sigma=s.symbols('H ne sigma',positive=True);ck('false_opacity_independent_H',s.diff(ne*sigma/H,H)==0)
if args.control=='number_is_effective_density':
 # Fixed atomic current cannot be replaced by independent carrier effective stress.
 extra=s.symbols('extra');eq('false_atomic_density_replacement',s.diff(s.log(n+extra),extra))
out=dict(passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,constants=dict(T0=T0,eta=eta,chi_eV=chi/ev,me_kg=me,mp_kg=mp,Tstar_K=Tstar,today_required_fb_if_fg1=bare),milestones=milestones,records=records,control=args.control,scope='conditional Saha/current calibration and remapped admitted background nodes; no lastscattering/kinetic solver')
p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2));print(json.dumps(dict(passed=out['passed'],total=out['total'],failed=[r for r in checks if not r['passed']],constants=out['constants'],milestones=milestones,records=records)));sys.exit(out['passed']!=out['total'])
