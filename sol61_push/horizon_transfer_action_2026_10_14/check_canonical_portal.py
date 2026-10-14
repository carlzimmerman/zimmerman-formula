import sys,json,math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
checks=[]
def ck(n,v):
 checks.append({'name':n,'ok':bool(v)})
 if not bool(v):raise AssertionError(n)
def ze(n,e):ck(n,s.simplify(e)==0)
e,O,g,gp,ps,Y,E=s.symbols('epsilon Omega g gprime psi_slope Y E',real=True)
p2=3*e*O;r=(g-3+3*O)/2
UN=Y*(-3*g+s.Rational(3,2)*e*(g-3))
UNN=Y*(-3*(gp+g*(g-3))+s.Rational(3,2)*e*((g-3)**2+gp))
Upp=(UNN-r*UN)/p2
matter=3*(1-e)*Y*(gp+g*g-r*g)/p2
meff=s.factor((Upp+matter)*O/Y)
target=3*g/e+g*g/4-(ps/2+3)*g+s.Rational(9,4)*(1+O)
ze('effective scalar mass closed form',meff.subs(gp,g*(ps+s.Rational(3,2)*O-g))-target)
ph=s.symbols('phi_prime',positive=True)
KG=(((g-3)/2+3)*ph+UN/(ph*E**2)+g/ph*3*(1-e)*Y/E**2)*ph
ze('canonical scalar equation on reconstructed history',s.expand(KG).subs(ph**2,3*e*O).subs(Y,O*E**2))
ze('same Friedmann density',(1-e)*Y+(e*Y/2)+(s.symbols('V')+e*Y/2)-(Y+s.symbols('V')))
ze('same pressure',e*Y/2-(s.symbols('V')+e*Y/2)+s.symbols('V'))

src=json.loads(Path('sol61_push/claude_bh_followthrough_2026_10_14/run_v1/results.json').read_text())
base=src['primary'];Xi=base['Xi_shot'];B0=base['Omega_b_projected'];Cold=base['Omega_c_projected']
rhoref=src['assigned_rho_crit_ref_Msun_Mpc3'];Href=70/3.0857e19*3.156e7
def psi(N):
 a=math.exp(N);return .015*a**(-2.7)/(1+(1/(2.9*a))**5.6)
def rhs(N,y):
 B,V,F=y;M=B+Cold;Y=M*math.exp(-3*N);E=math.sqrt(Y+V)
 J=Xi*psi(N)/(rhoref*Href*E)
 return [-J,J*math.exp(-3*N),math.sqrt(3*Y/E**2)]
so=solve_ivp(rhs,(-math.log(9),.1),[B0,0.,0.],method='DOP853',rtol=1e-12,atol=1e-14,dense_output=True,max_step=.05)
ck('canonical background coordinate solve',so.success)
def point(N,eps):
 B,V,Fhat=so.sol(N);M=B+Cold;Y=M*math.exp(-3*N);E2=Y+V;Om=Y/E2
 J=Xi*psi(N)/(rhoref*Href*math.sqrt(E2));gg=-J/M
 bs=(math.exp(-N)/2.9)**5.6;pp=-2.7+5.6*bs/(1+bs);gn=gg*(pp+1.5*Om-gg)
 phN=math.sqrt(3*eps*Om);rat=(gg-3+3*Om)/2
 U=3*V+1.5*eps*Y;Un=Y*(-3*gg+1.5*eps*(gg-3))
 Unn=Y*(-3*(gn+gg*(gg-3))+1.5*eps*((gg-3)**2+gn))
 Upp=(Unn-rat*Un)/(phN*phN)
 Fc=(1-eps)*M-B0;Fci=(1-eps)*(B0+Cold)-B0
 gc=(1-eps)*M*gg/Fc;bet=gc/phN
 Acpp=((1-eps)*M*(gn+gg*gg-rat*gg)/Fc)/(phN*phN)
 rho_c=3*Fc*math.exp(-3*N)
 me2=(Upp+rho_c*Acpp)/E2
 form=3*gg/eps+gg*gg/4-(pp/2+3)*gg+2.25*(1+Om)
 kg=((gg-3)/2+3)*phN+Un/(phN*E2)+bet*rho_c/E2
 return {'phi':math.sqrt(eps)*Fhat,'U':U,'Uphi':Un/phN,'Upp':Upp,'A_c':Fc/Fci,'beta_c':bet,'rho_c':rho_c,'H2':E2,'m_eff2_over_H2':me2,'mass_formula':form,'KG_residual_over_H2':kg,'w_phi_plus1':eps*Y/(V+eps*Y),'fifth_force_over_gravity_unscreened_cold_cold':2*bet*bet,'g_total_mass':gg,'g_cold_mass':gc,'Omega_target_matter':Om,'A_c_phiphi_over_A':Acpp,'source_e_folds':-gc}
rows=[]
for eps in [1e-5,.0001,.001,.01,.05,.1,.3]:
 for z in [0,.5,1,2,3]:
  N=-math.log1p(z);p=point(N,eps)
  ck('exact scalar EOM '+str((eps,z)),abs(p['KG_residual_over_H2'])<1e-9)
  ck('effective mass formula '+str((eps,z)),abs(p['m_eff2_over_H2']-p['mass_formula'])<1e-7)
  ck('positive dust and coupling factor '+str((eps,z)),p['rho_c']>0 and p['A_c']>0)
  if eps in [.001,.1] and z in [0,2]:
   step=1e-5;lo=point(N-step,eps);hi=point(N+step,eps)
   upp_fd=(hi['Uphi']-lo['Uphi'])/(hi['phi']-lo['phi'])
   ck('independent potential derivative '+str((eps,z)),abs(upp_fd-p['Upp'])/max(1,abs(p['Upp']))<1e-6)
  growth=[]
  for kH in [10,100,1000]:
   damp=2+p['g_cold_mass'];mass=p['m_eff2_over_H2'];Bforce=p['beta_c']**2*p['rho_c']/p['H2'];kk=kH*kH
   roots=np.roots([1,damp+3,kk+mass+3*damp,damp*(kk+mass),-Bforce*kk])
   growth.append({'k_over_H':kH,'max_frozen_growth_over_H':float(max(roots.real))})
  rows.append({'epsilon':eps,'z':z,**p,'frozen_cold_scalar_growth':growth})
ck('small-kinetic reconstruction has fast source-block growth',any(r['epsilon']==.001 and r['z']==2 and r['frozen_cold_scalar_growth'][0]['max_frozen_growth_over_H']>5 for r in rows))
result={'passed':len(checks),'checks':checks,'rows':rows,'interpretation':'Explicit inverse-designed canonical scalar plus cold-only conformal mass portal in Einstein frame, baryons minimally coupled. Exact assigned H reproduced after stated kinetic/dust reallocation. Positive kinetic energy is not a full stability claim; nonzero GB and the tether energy are separate additions, not silently included. Frozen scalar/cold growth omits metric and existing tether support.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
