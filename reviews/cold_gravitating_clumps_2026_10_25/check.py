import argparse,json,math
from pathlib import Path
import sympy as S
from scipy.optimize import brentq
from scipy.integrate import quad

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 q=S.symbols('q',real=True);q0=2*S.asin(S.sqrt(S.Rational(1,6)));U=10*(1/S.cos(q/2)**2-S.Rational(6,5))**2
 m2=S.simplify(S.diff(U,q,2).subs(q,q0));aa=S.simplify(S.diff(U,q,3).subs(q,q0)/2);bb=S.simplify(S.diff(U,q,4).subs(q,q0)/6)
 geff=S.simplify(bb-(0 if a.mutate else S.Rational(10,9)*aa**2/m2));coefficient=float(3*geff/(8*m2*m2));qvac=float(q0)
 def pot(q):return 10*(1/math.cos(q/2)**2-1.2)**2
 controls=[]
 for E in [1e-4,3e-5,1e-5]:
  lo=brentq(lambda q:pot(q)-E,0,qvac,xtol=1e-14);hi=brentq(lambda q:pot(q)-E,qvac,2.,xtol=1e-14)
  mid=(hi+lo)/2;half=(hi-lo)/2
  def integrand(t,j):
   q=mid+half*math.sin(t);diff=E-pot(q);assert diff>0
   wt=half*math.cos(t)/math.sqrt(2*diff)
   return wt*(diff if j else 1)
  norm=quad(lambda t:integrand(t,0),-math.pi/2,math.pi/2,epsabs=1e-10,epsrel=1e-10)[0]
  kin=quad(lambda t:integrand(t,1),-math.pi/2,math.pi/2,epsabs=1e-14,epsrel=1e-10)[0]/norm
  measured=(2*kin/E-1)/E
  assert abs(measured/coefficient-1)<.01,('normal-form coefficient',E,measured,coefficient)
  controls.append(dict(E=E,measured_w_over_E=measured,relative_error=abs(measured/coefficient-1)))
 # Gaussian radial Hessian with cosmological term, evaluated at stationarity.
 x,mu,zeta=S.symbols('x mu zeta',positive=True)
 energy=x**-2-mu/x-mu/(3*x**3)-zeta*x*x
 stationary_mu=2*x*(1+zeta*x**4)/(1+x*x)
 hessian=S.factor(S.diff(energy,x,2).subs(mu,stationary_mu))
 expected=2*(x*x-1-zeta*x**4*(3*x*x+5))/(x**4*(x*x+1))
 assert S.simplify(hessian-expected)==0
 y=S.symbols('y',positive=True);bound=(y-1)/(y*y*(3*y+5));assert S.simplify(S.diff(bound,y).subs(y,S.Rational(5,3)))==0
 assert bound.subs(y,S.Rational(5,3))==S.Rational(3,125)
 G=6.67430e-11;C=299792458.;PC=3.085677581491367e16;MS=1.98847e30;HJ=1.8e-18;f=5/6;HE=HJ/math.sqrt(f)
 Dmass=.75*3*HJ*HJ/(8*math.pi*G);eta=1500*PC*1000*math.sqrt(f)
 K=coefficient*C*C/Dmass
 A=3*eta*eta/4;b=1/math.sqrt(2*math.pi);cc=(2*math.pi)**(-1.5)
 Mcrit=A/math.sqrt(3*b*cc*G*abs(K));Rcrit=A/(b*G*Mcrit)
 zet=.75*HE*HE*Rcrit**4/A
 rho0=Mcrit/(math.pi**1.5*Rcrit**3)
 req=json.load(open('reviews/cold_rapid_assembly_2026_10_25/run/result.json'))['cluster_mass_requirements']
 counts=[r['Mc_R500_Msun']/(Mcrit/MS) for r in req]
 summary=dict(m2=float(m2),cubic_force=float(aa),bare_quartic_force=float(bb),effective_quartic=float(geff),w_over_E_coefficient=coefficient,eta_E_pc_kms=eta/PC/1000,K_SI=K,Mcrit_Msun=Mcrit/MS,Rcrit_pc=Rcrit/PC,turnaround_pc=(G*Mcrit/HE**2)**(1/3)/PC,horizon_pc=C/HE/PC,dynamical_time_years=math.sqrt(Rcrit**3/(G*Mcrit))/(365.25*86400),H_times_dynamical_time=HE*math.sqrt(Rcrit**3/(G*Mcrit)),gaussian_central_energy_over_D=rho0/Dmass,zeta=zet,zeta_minimum_existence_upper_bound=3/125,hypothetical_object_count_range=[min(counts),max(counts)],mass_requirements=len(req))
 result=dict(scope='Dilute Gaussian variational branch, not full relativistic real-scalar stars',summary=summary,oscillator_checks=controls,stationary_hessian=str(hessian))
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
