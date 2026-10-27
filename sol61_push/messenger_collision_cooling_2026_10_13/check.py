"""NR elastic cooling against prescribed stationary messenger targets."""
import json,sys,math
from pathlib import Path
import sympy as s
import numpy as np
m,M,v,x=s.symbols('m M v x',positive=True)
checks=[]
def test(name,t):
 checks.append({'name':name,'passed':bool(t)});assert t,name
# CM postcollision relative velocity has magnitude v and scattering cosine x.
vp2=v*v*(m*m+M*M+2*m*M*x)/(m+M)**2
vs2=2*m*m*v*v*(1-x)/(m+M)**2
before=m*v*v/2;after=m*vp2/2+M*vs2/2
test('two-body energy conservation',s.simplify(before-after)==0)
f=s.simplify(1-s.integrate(vp2/v**2,(x,-1,1))/2)
test('mean fractional energy loss',s.simplify(f-2*m*M/(m+M)**2)==0)
# Independent explicit vector collision over angles and mass ratios.
for ratio in [1,10,100]:
 for cosine in [-1,-.5,0,.5,1]:
  mm=1.;MM=float(ratio);initial=np.array([0.,0.,1.]);cm=initial*mm/(mm+MM)
  rel=np.array([math.sqrt(1-cosine*cosine),0.,cosine])
  p=cm+MM/(mm+MM)*rel;z=cm-mm/(mm+MM)*rel
  test('vector conservation '+str((ratio,cosine)),np.linalg.norm(mm*p+MM*z-initial)<1e-12 and abs(mm*np.dot(p,p)+MM*np.dot(z,z)-1)<1e-12)
# Exact angular moments; events are independent and targets reset to zero velocity.
rows=[];mv=1e6;h=1.;hc=1.973269804e-7;c=299792458.;ev=1.602176634e-19;alpha=1/137.035999084
for mass in [1e7,1e8,1e9]:
 sig=h*h/(16*math.pi*(mv+mass)**2)*hc*hc
 fraction=2*mv*mass/(mv+mass)**2
 C=-alpha*h/(48*math.pi*mass*mass)
 ann=2*C*C*mv*mv/math.pi*hc*hc*c
 n=1e25;K=1.;speed=c*math.sqrt(2*K/mv)
 collision=n*sig*speed;events=math.ceil(math.log(.01)/math.log1p(-fraction))
 rows.append({'mass_M_eV':mass,'sigma_m2':sig,'energy_loss_fraction_per_event':fraction,'events_for_mean_K_below_1pct':events,'mean_energy_ratio_after_events':(1-fraction)**events,'nS_m3':n,'mean_free_path_m':1/(n*sig),'collision_rate_initial_s_inv':collision,'initial_fractional_cooling_rate_s_inv':fraction*collision,'one_cm_straight_path_optical_depth':n*sig*.01,'required_nS_over_nopposite_for_initial_cooling_equal_annihilation':ann/(fraction*sig*speed),'reservoir_charge_density_C_m3':ev*n,'mean_field_repulsion_eV':h*n*hc**3/(4*mv*mass)})
 test('collision count '+str(mass),rows[-1]['mean_energy_ratio_after_events']<=.01 and (1-fraction)**(events-1)>.01)
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'energy_loss_fraction':str(f),'rows':rows,'non_claims':['Stationary dilute targets; no actual charged plasma or cold bath','Collision-count mean is not a residence-time calculation','No trap, capture, bath production, heat removal or experimental viability']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(rows,indent=2))
