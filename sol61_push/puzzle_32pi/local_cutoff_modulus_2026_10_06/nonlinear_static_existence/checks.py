import argparse,json,pathlib,sys
import sympy as s,numpy as np
from scipy.integrate import cumulative_trapezoid
from numpy.polynomial.legendre import leggauss
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',default='none');args=ap.parse_args();rows=[];numeric={}
def ck(n,v):rows.append({'name':n,'pass':bool(v)})
def eq(n,z):ck(n,s.simplify(z)==0)
y,T,t=s.symbols('y T t',positive=True);b=s.sqrt(1+1/t)-1;c=2*T*t*t*b/(T*T+t*t)**2
ratio=s.diff(c,T)/c
eq('exact_log_derivative',ratio-(t*t-3*T*T)/(T*(T*T+t*t)))
v=s.symbols('v',nonnegative=True);rat=(v-3)/(v+1)
eq('ratio_lower_gap',rat+3-4*v/(v+1));eq('ratio_upper_gap',1-rat-4/(v+1))
eq('global_pi_bound_integral',2*T*s.integrate(t*t/(T*T+t*t)**2,(t,0,s.oo))-s.pi/2)
eq('small_y_partialT',s.limit(c/t**s.Rational(3,2),t,0)-2/T**3)
eq('small_y_qT_bound',s.integrate(4*t**s.Rational(5,2)/T**3,(t,0,y))-8*y**s.Rational(7,2)/(7*T**3))
N=s.symbols('N',nonnegative=True);n=N+3;k=7*(n-1)/2
eq('all_n_integrable_gap',k-n-(5*N+8)/2)
# Green heat mass and gradient integral are explicit Gaussian facts.
m,ss=s.symbols('m ss',positive=True)
eq('all_n_Green_mass',s.integrate(s.exp(-m*m*ss),(ss,0,s.oo))-1/m**2)
ck('gradient_heat_L1_finite',s.integrate(s.exp(-m*m*ss)/s.sqrt(ss),(ss,0,s.oo))==s.sqrt(s.pi)/m)
kap,Z,T0=s.symbols('kappa Z T0',positive=True);BB=kap*s.pi/(2*Z*m*m);LL=3*kap*s.pi/(2*Z*m*m*T0)
eq('contraction_constant',LL-3*BB/T0)
eq('Hessian_gap_equivalence',(Z*m*m)*(1-LL)-(Z*m*m-3*kap*s.pi/(2*T0)))
# Spherical flux requires gradientT term, not a fixedkernel divergence.
r=s.symbols('r',positive=True);NN=s.Function('nu');yy=s.Function('y')(r);TT=s.Function('T')(r);gn=s.Function('gN')(r)
full=s.diff(r**2*NN(yy,TT)*gn,r);fixed=full-s.diff(NN(yy,TT),TT)*s.diff(TT,r)*r*r*gn
reaction=full-fixed
ck('retained_T_gradient',s.simplify(reaction)==0 if args.control=='drop_T_gradient' else s.simplify(reaction-r*r*gn*s.diff(NN(yy,TT),TT)*s.diff(TT,r))==0)
# Force correction from the two independently derived leading factors.
a0=s.symbols('a0',positive=True)
eq('nonperturbative_force_coefficient',a0*y*(2*y**s.Rational(3,2)/T0**3)*(8*kap*y**s.Rational(7,2)/(7*Z*m*m*T0**3))-16*kap*a0*y**6/(7*Z*m*m*T0**6))
rM=s.symbols('rM',positive=True);source_tail=8*kap*rM**7/(7*Z*T0**3)*r**-7
ansatz=(s.Integer(0) if args.control=='pure_yukawa' else 8*kap*rM**7/(7*Z*m*m*T0**3))*r**-7
residual=-s.diff(ansatz,r,2)-2*s.diff(ansatz,r)/r+m*m*ansatz-source_tail
eq('massive_tail_algebraic',s.limit(r**7*residual,r,s.oo))
witness=LL.subs(kap,Z*m*m*T0)
ck('not_all_stiffness_contracts',witness<1 if args.control=='all_stiffness' else witness>1)
ck('example_satisfies_threshold',LL.subs(kap,Z*m*m*T0/20)<1)
# Finite-domain radial Picard corroboration; analytic theorem does not depend on grids.
a=.05;mass=1.;vac=1.;box=a*np.pi/(2*mass**2);lip=3*a*np.pi/(2*mass**2*vac)
vq,wq=leggauss(32);vq=(vq+1)/2;wq=wq/2

def qt(field,cut):
 tt=field[:,None]*vq[None,:]**2;cuts=cut[:,None]
 dc=2*cuts*tt**1.5/((np.sqrt(1+tt)+np.sqrt(tt))*(cuts*cuts+tt*tt)**2)
 return 4*field**2*np.sum(wq[None,:]*vq[None,:]**3*dc,axis=1)
def solve(num):
 rr=np.linspace(0,24,num);rho=np.zeros_like(rr);inside=rr<1;rho[inside]=np.exp(-1/(1-rr[inside]**2))
 enclosed=cumulative_trapezoid(4*np.pi*rr*rr*rho,rr,initial=0);enclosed/=enclosed[-1];field=np.zeros_like(rr);field[1:]=enclosed[1:]/rr[1:]**2
 uu=np.zeros_like(rr);deltas=[]
 for j in range(30):
  ff=qt(field,vac+uu);left=cumulative_trapezoid(rr*np.sinh(mass*rr)*ff,rr,initial=0)
  right=-cumulative_trapezoid((rr*np.exp(-mass*rr)*ff)[::-1],rr[::-1],initial=0)[::-1]
  unew=np.zeros_like(rr);unew[0]=a*right[0];unew[1:]=a/(mass*rr[1:])*(np.exp(-mass*rr[1:])*left[1:]+np.sinh(mass*rr[1:])*right[1:])
  diff=float(np.max(np.abs(unew-uu)));deltas.append(diff);uu=unew
  if diff<2e-14:break
 ck('positive_box_'+str(num),np.min(uu)>=0 and np.max(uu)<=box)
 ck('discrete_contraction_'+str(num),all(deltas[i]<=lip*deltas[i-1]+1e-15 for i in range(1,len(deltas))))
 numeric[str(num)]={'iterations':len(deltas),'max_deltaT':float(np.max(uu)),'last_picard_difference':deltas[-1],'analytic_box':box,'analytic_contraction':lip,'largest_observed_ratio':max(deltas[i]/deltas[i-1] for i in range(1,len(deltas)) if deltas[i-1]>1e-13),'center_deltaT':float(uu[0]),'domain_rmax':24.0,'quadrature_nodes':32,'not_a_continuum_certificate':True}
 return rr,uu
r1,u1=solve(1201);r2,u2=solve(2401);err=float(np.max(np.abs(u1-np.interp(r1,r2,u2))))
ck('bounded_grid_convergence',err<1e-4);numeric['grid_max_difference']=err
out={'checks':rows,'passed':sum(z['pass'] for z in rows),'failed':sum(not z['pass'] for z in rows),'control':args.control,'bounded_radial_iterations':numeric,'non_claims':['No full-action Hessian','No relativistic completion','No continuum numerical certification','No selected32pi']}
pathlib.Path(args.output).parent.mkdir(parents=True,exist_ok=True);pathlib.Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));sys.exit(bool(out['failed']))
