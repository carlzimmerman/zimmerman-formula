from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent
p1,p2,x1,x2,k,c=s.symbols('p1 p2 x1 x2 k c',real=True)
Om2=c*c*k*k
E=(p1*p1+p2*p2+Om2*(x1*x1+x2*x2))/2
P=-k*(p1*x2-p2*x1)
square=(p1*p1+p2*p2-Om2*(x1*x1+x2*x2))**2/4+Om2*(p1*x1+p2*x2)**2
assert s.expand(E*E-c*c*P*P-square)==0
eps,q=s.symbols('epsilon q',positive=True)
b=s.Matrix([-1,-1,1,1])
v=s.Matrix([0,eps,-2*eps,eps])
D=s.simplify(sum(b[i]*v[i]**2/2 for i in range(4)))
pb=s.simplify((b.T*v)[0])
assert D==2*eps**2 and pb==-2*eps
f0=s.Matrix([2,2,1,1]);f=f0+b*q
affprod=s.expand(f[0]*f[1]-f[2]*f[3])
eq=s.solve(affprod,q);assert eq==[s.Rational(1,2)]
qe=eq[0]
rows=[]
for e in [s.Rational(1,100),s.Rational(1,1000),s.Rational(1,10000)]:
    de=D.subs(eps,e);pe=abs(pb.subs(eps,e))
    minimum_r=s.simplify((de+pe)/de)
    for r in [1,4,8]:
        H0=r*de*qe
        cap=s.simplify(H0/(de+pe))
        fraction=s.simplify(cap/qe)
        assert fraction<s.Integer(1)
        assert s.simplify(fraction-r*e/(1+e))==0
        rows.append({'epsilon':str(e),'capacity_ratio_to_equilibrium_cold_cost':r,
                     'q_equilibrium':str(qe),'necessary_q_cap':str(cap),
                     'max_equilibrium_fraction':float(fraction),
                     'minimum_capacity_ratio_for_equilibrium':str(minimum_r)})
neutral=s.Matrix([-eps,eps,-2*eps,2*eps])
assert (b.T*neutral)[0]==0
assert s.simplify(sum(b[i]*neutral[i]**2/2 for i in range(4)))==3*eps**2
result={'exact':{'receiver_energy_momentum_sum_of_squares':True,
                 'cold_D':str(D),'cold_momentum_increment':str(pb),
                 'reaction_product_root':str(qe),'momentum_neutral_control':True},
        'rows':rows,
        'scope':'Necessary field-excitation budget with all recoil carried by this massless receiver; not sufficient reachability or a universal dark-sector exclusion.'}
HERE.joinpath('capacity_run/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
