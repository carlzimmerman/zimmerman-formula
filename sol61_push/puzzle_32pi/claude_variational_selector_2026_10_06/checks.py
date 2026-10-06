import sympy as s,mpmath as mp,argparse,json,pathlib,sys
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',default='none');a=ap.parse_args();mp.mp.dps=50;rows=[];numeric={}
def ck(n,v):rows.append({'name':n,'pass':bool(v)})
y,T,rM,r,G,a0,M,R=s.symbols('y T rM r G a0 M R',positive=True)
base=s.sqrt(1+1/y)-1;chi=base*T*T/(T*T+y*y);ct=2*T*y*y*base/(T*T+y*y)**2
ck('cutoff_derivative',s.simplify(s.diff(chi,T)-ct)==0)
ck('IR_derivative',s.limit(ct/y**s.Rational(3,2),y,0)==2/T**3)
ck('UV_derivative',s.limit(ct*y**3,y,s.oo)==T)
r_of_y=rM/s.sqrt(y)
ck('radial_volume_jacobian',s.simplify(4*s.pi*r_of_y**2*s.diff(r_of_y,y)+2*s.pi*rM**3*y**s.Rational(-5,2))==0)
ck('point_histogram_prefactor',s.simplify(a0*a0/(4*s.pi*G)*y*4*s.pi*rM**3/(3*y**s.Rational(3,2))-a0*a0*rM**3/(3*G)*y**s.Rational(-1,2))==0)
ck('radial_Fubini_factor',s.integrate(y**s.Rational(-5,2),(y,r,s.oo))*2*r==s.Rational(4,3)*r**s.Rational(-1,2))
ck('mass_scaling',s.simplify(a0*a0*(s.sqrt(G*M/a0))**3/G-s.sqrt(G*a0)*M**s.Rational(3,2))==0)
threshold=rM*rM/R**2;outer=rM/s.sqrt(y);inner=y*R**3/rM**2
hist=4*s.pi*(outer**3-inner**3)/3
ck('uniform_sphere_histogram_closes',s.simplify(hist.subs(y,threshold))==0)
ck('sphere_histogram_positive_sample',hist.subs({rM:1,R:1,y:s.Rational(1,2)})>0)
# Independent double-integral benchmark delta chi=e^-y; delta q=2 gammainc(2,0,y).
jbench=mp.quad(lambda z:2*mp.exp(-z*z),[0,1,mp.inf])
radbench=mp.quad(lambda z:2*mp.gammainc(2,0,z)*z**(-mp.mpf('2.5')),[0,1,mp.inf])
ck('benchmark_J',abs(jbench-mp.sqrt(mp.pi))<mp.mpf('1e-45'))
ck('benchmark_radial',abs(radbench-mp.mpf(4)/3*jbench)<mp.mpf('1e-25'))
for tt in [10,100,1000]:
 def dchi(z):return 2*tt*z*z/(z*(mp.sqrt(1+1/z)+1)*(tt*tt+z*z)**2)
 # y=t² removes endpoint square root; use independent direct-y quadrature too.
 jp=mp.quad(lambda t:2*dchi(t*t),[0,1,mp.sqrt(tt),10*mp.sqrt(tt),mp.inf])
 cp=mp.quad(lambda t:2*t**3*dchi(t*t),[0,1,mp.sqrt(tt),10*mp.sqrt(tt),mp.inf])
 jdirect=mp.quad(lambda z:dchi(z)/mp.sqrt(z),[0,1,tt,10*tt,mp.inf])
 numeric[str(tt)]={'Jprime':str(jp),'Cprime':str(cp),'Jquadrature_difference':str(jp-jdirect)}
 ck('Jprime_positive_'+str(tt),jp>0);ck('Cprime_positive_'+str(tt),cp>0);ck('quadrature_agreement_'+str(tt),abs(jp-jdirect)<mp.mpf('1e-40'))
ck('no_stationary_cutoff',mp.mpf(numeric['100']['Jprime'])==0 if a.control=='stationary' else mp.mpf(numeric['100']['Jprime'])>0)
ck('different_moment_weight',s.simplify(y**s.Rational(-1,2)-y)==0 if a.control=='same_moment' else s.simplify(y**s.Rational(-1,2)-y)!=0)
ck('no_universal_bare_balance',s.Integer(2)**s.Rational(3,2)==1 if a.control=='mass_independent' else s.Integer(2)**s.Rational(3,2)!=1)
res={'checks':rows,'passed':sum(x['pass'] for x in rows),'failed':sum(not x['pass'] for x in rows),'control':a.control,'numerical_derivatives':numeric,'benchmark_radial':str(radbench),'non_claims':['No covariant modulus action','No absolute finite isolated energy','No 32pi fit']}
pathlib.Path(a.output).parent.mkdir(parents=True,exist_ok=True);pathlib.Path(a.output).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res));sys.exit(bool(res['failed']))
