import sys,json,pathlib
import sympy as s
u=s.symbols('u',positive=True); A,B,K,cd,cp,cv,Av=s.symbols('A B K cd cp cv Av',real=True)
Q=s.Function('Q')(u); F=s.Function('F')(u)
L3=lambda f:s.expand(f-u*s.diff(f,u)/3)
L6=lambda f:s.expand(f-u*s.diff(f,u)/6)
checks={};details={}
def zero(name,x):
 checks[name]=bool(s.simplify(x)==0)
 if not checks[name]:raise AssertionError((name,s.simplify(x)))
zero('pressure_operator_radiation_curvature',L3(F-A*u**3-B*u**4-K*u**2)-(L3(F)+B*u**4/3-K*u**2/3))
zero('potential_operator_components',L6(F-A*u**3-B*u**4-K*u**2)-(L6(F)-A*u**3/2-B*u**4/3-2*K*u**2/3))
zero('pressure_integrating_factor',s.diff(F/u**3,u)+3*L3(F)/u**4)
zero('potential_integrating_factor',s.diff(F/u**6,u)+6*L6(F)/u**7)
zero('density_pressure_ode',L3(A*u**3+cd*Q)-cp*Q-((cd-cp)*Q-cd*u*s.diff(Q,u)/3))
zero('density_potential_ode',L6(A*u**3+cd*Q)-Av*u**3/2-cv*Q-((A-Av)*u**3/2+(cd-cv)*Q-cd*u*s.diff(Q,u)/6))
zero('pressure_potential_implies_density',2*(L6(F)-Av*u**3/2)-L3(F)-(F-Av*u**3))
for power in [s.Rational(0),s.Rational(1),s.Rational(2),s.Rational(5,2),s.Rational(-1)]:
 q=u**power;f=A*u**3+q
 zero('power_pressure_'+str(power),L3(f)-(1-power/3)*q)
 zero('power_potential_'+str(power),L6(f)-A*u**3/2-(1-power/6)*q)
 zero('power_kinetic_'+str(power),q-L6(q)-power*q/6)
# Density/potential overlap with different conserved matter splits, positive branches.
q=u+u**3/10;f=u+u**3/2;ad=s.Rational(2,5);av=s.Rational(1,3);cv0=s.Rational(5,6)
xd=s.simplify(f-ad*u**3);xv=s.simplify(f-av*u**3)
zero('positive_mixture_density',xd-q)
zero('positive_mixture_potential',L6(xv)-cv0*q)
zero('mixture_pressure_is_2u_over3',L3(f)-2*u/3)
ratio=s.simplify(L3(f)/q)
zero('mixture_ratio_derivative',s.diff(ratio,u)+40*u/(3*(u**2+10)**2))
checks['mixture_pressure_not_constant']=bool(s.diff(ratio,u)!=0)
checks['positive_mixture_branches']=all(bool(expr.is_positive) for expr in [xd,xv,L6(xv),xv-L6(xv),L3(xd),L3(xv)])
assert checks['positive_mixture_branches']
details['mixture']={k:str(v) for k,v in dict(Q=q,F=f,A_density=ad,A_potential=av,C_potential=cv0,negative_pressure=L3(f),pressure_to_Q=ratio,potential_kinetic=xv-L6(xv)).items()}
# Resonant density/potential overlap s=3, not negative pressure.
d=s.Rational(1,10);qr=u**3*(1+d*s.log(u));ar=s.Rational(2,5);avr=ar-d/3;fr=ar*u**3+qr
zero('resonant_density_potential',L6(fr-avr*u**3)-qr/2)
zero('resonant_negative_pressure_sign',L3(fr)+d*u**3/3)
# Derivative-free exact nulls on four specified synthetic nodes.
nodes=[s.Integer(i) for i in [1,2,3,4]]
intervals=list(zip(nodes[:-1],nodes[1:]))
f_nodes=[f.subs(u,x) for x in nodes];q_nodes=[q.subs(u,x) for x in nodes]
density_det=s.det(s.Matrix([[x**3,y,z] for x,y,z in zip(nodes,q_nodes,f_nodes)] )[:3,:])
zero('mixture_density_three_node_determinant',density_det)
rows=[];pressure=[]
for a,b in intervals:
 ip=s.integrate(q/u**4,(u,a,b));iv=s.integrate(q/u**7,(u,a,b))
 dp=f.subs(u,b)/b**3-f.subs(u,a)/a**3
 dv=f.subs(u,b)/b**6-f.subs(u,a)/a**6
 xm=b**-3-a**-3
 zero('mixture_potential_interval_'+str(a),dv-av*xm+6*cv0*iv)
 rows.append([dv,xm,iv]);pressure.append((dp,ip))
zero('mixture_potential_interval_determinant',s.det(s.Matrix(rows)))
pnull=s.simplify(pressure[0][0]*pressure[1][1]-pressure[1][0]*pressure[0][1])
checks['mixture_pressure_interval_rejects_exactly']=bool(abs(float(s.N(pnull,50)))>1e-8)
details['pressure_interval_null']={'exact':str(pnull),'50_digit':str(s.N(pnull,50))}
# Pure-power test satisfies pressure interval null.
q0=u;f0=A*u**3+q0;pr=[]
for a,b in intervals:
 ip=s.integrate(q0/u**4,(u,a,b));dp=f0.subs(u,b)/b**3-f0.subs(u,a)/a**3
 zero('pure_power_pressure_interval_'+str(a),dp+2*ip);pr.append((dp,ip))
zero('pure_power_pressure_two_interval_null',pr[0][0]*pr[1][1]-pr[1][0]*pr[0][1])
# Rank-collapse witness for density: Q proportional u^3.
zero('dust_Q_density_rank_collapse',s.det(s.Matrix([[x**3,2*x**3,1] for x in nodes[:3]])))
assert all(checks.values())
out=pathlib.Path(sys.argv[1]);out.mkdir(exist_ok=True)
(out/'results.json').write_text(json.dumps({'assertion_tested':'Exact scoped symbolic identities and specified synthetic counterexamples, not observations','check_count':len(checks),'all_checks_pass':all(checks.values()),'checks':checks,'details':details},indent=2))
print('checks',len(checks),'all_pass',all(checks.values()));print('pressure interval null',s.N(pnull,12))
