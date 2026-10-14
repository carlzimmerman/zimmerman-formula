import json,sys,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
src=json.loads(Path('sol61_push/claude_bh_followthrough_2026_10_14/run_v1/results.json').read_text())
p=src['primary'];Xi=p['Xi_shot'];B0=p['Omega_b_projected'];C=p['Omega_c_projected'];ai=1/9
rhoref=src['assigned_rho_crit_ref_Msun_Mpc3'];Href=70/3.0857e19*3.156e7
Hsi=Href/3.156e7;cfac=299792458/Hsi/3.0856775814913673e25
checks=[]
def ck(n,v):
 checks.append({'name':n,'ok':bool(v)})
 if not bool(v):raise AssertionError(n)
def rhs(a,y):
 B,V=y;E=math.sqrt((B+C)/a**3+V)
 psi=.015*a**(-2.7)/(1+(1/(2.9*a))**5.6)
 j=Xi*psi/(rhoref*Href*E)
 return [-j/a,j/a**4]
# Independent coordinate a and DOP853, rather than N and RK45 in canonical run.
so=solve_ivp(rhs,(ai,1e4),[B0,0.],method='DOP853',rtol=2e-12,atol=1e-14,dense_output=True)
ck('independent scale-factor ODE',so.success)
def E(a):
 B,V=so.sol(a);return math.sqrt((B+C)/a**3+V)
Vinf=so.y[1,-1]
def radius(a):
 if a<1:
  integral=quad(lambda aa:1/(aa*aa*E(aa)),a,1,epsabs=1e-11,epsrel=1e-11)[0]
 else:integral=0
 integral+=quad(lambda aa:1/(aa*aa*E(aa)),max(1,a),1e4,epsabs=1e-11,epsrel=1e-11,limit=300)[0]
 return a*(integral+1/(1e4*math.sqrt(Vinf)))
ck('independent present flatness',abs(E(1)-1)<1e-9)
rows=[]
for old in p['rows']:
 a=1/(1+old['z']);RR=radius(a);err=abs(RR*cfac/old['R_event_Gpc']-1)
 ck('independent horizon integral z='+str(old['z']),err<1e-8)
 # Derivative check of dR/d ln a = R - 1/E at fixed future history.
 h=1e-5;der=(radius(a*math.exp(h))-radius(a*math.exp(-h)))/(2*h)
 ck('horizon evolution identity z='+str(old['z']),abs(der-(RR-1/E(a)))<1e-8)
 ck('event radius exceeds Hubble radius z='+str(old['z']),RR*E(a)>1)
 rows.append({'z':old['z'],'R_event_Gpc':RR*cfac,'relative_error':err,'H_over_Href':E(a),'horizon_derivative_dR_d_lna':der})
ck('pure de Sitter horizon integral',abs(quad(lambda aa:1/aa**2,1,1e4,epsabs=1e-12)[0]+1e-4-1)<1e-10)
result={'passed':len(checks),'checks':checks,'independent_rows':rows,'event_radius_Gpc_at_first_light':radius(ai)*cfac,'V_at_first_light':0,'horizon_branch_a0_at_first_light_over_today':radius(1)/radius(ai),'proof_scope':'Positive conserved dust plus sourced pure vacuum has Hdot=-4piG rho_m <=0. Finite future event horizon then satisfies R>=c/H and Rdot>=0. Vacuum production gives Vdot>=0, so sqrt(V) and1/R have opposite time trends.','interpretation':'Independent coordinate, integrator and horizon evolution checks; not a microphysical BH or full perturbation model.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
