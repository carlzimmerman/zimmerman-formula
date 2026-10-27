import sympy as s,json,sys
from pathlib import Path
coords=s.symbols('t x y z',real=True);t=coords[0];f=s.Function('sigma')(t)
factor=s.exp(2*f);sign=[1,-1,-1,-1];g=s.diag(*[q*factor for q in sign]);gi=s.diag(*[q/factor for q in sign])
checks=[]
def eq(n,x,y=0):
 z=s.simplify(x-y);assert z==0,(n,z);checks.append(n)
Gamma={}
for c in range(4):
 for a in range(4):
  for b in range(4):
   Gamma[c,a,b]=s.simplify(sum(gi[c,d]*(s.diff(g[d,b],coords[a])+s.diff(g[d,a],coords[b])-s.diff(g[a,b],coords[d]))/2 for d in range(4)))
Ric={}
for a in range(4):
 for b in range(4):
  Ric[a,b]=s.simplify(sum(s.diff(Gamma[c,a,b],coords[c])-s.diff(Gamma[c,a,c],coords[b])+sum(Gamma[c,c,d]*Gamma[d,a,b]-Gamma[c,b,d]*Gamma[d,a,c] for d in range(4)) for c in range(4)))
eq('actual_Ricci_time',Ric[0,0],-3*s.diff(f,t,2))
for j in range(1,4):eq('actual_Ricci_space_'+str(j),Ric[j,j],s.diff(f,t,2)+2*s.diff(f,t)**2)
assert all(Ric[a,b]==0 for a in range(4) for b in range(4) if a!=b);checks.append('actual_Ricci_offdiagonal_zero')
R=s.simplify(sum(gi[a,b]*Ric[a,b] for a in range(4) for b in range(4)))
eq('actual_scalar_curvature',R,-6*s.exp(-2*f)*(s.diff(f,t,2)+s.diff(f,t)**2))
eq('actual_metric_determinant',s.det(g),-s.exp(8*f))
volume=s.exp(4*f) # positive real exponential square root of -det(g).
eq('volume_square_matches_determinant',volume**2,-s.det(g))
L=s.simplify(volume*R**2)
eq('actual_curvature_square_density',L,36*(s.diff(f,t,2)+s.diff(f,t)**2)**2)
q0,q1,q2,q3,q4=s.symbols('q0 q1 q2 q3 q4',real=True)
jet={f:q0,s.diff(f,t):q1,s.diff(f,t,2):q2,s.diff(f,t,3):q3,s.diff(f,t,4):q4}
Lj=s.simplify(L.subs(jet,simultaneous=True))
def Dt(expr):return s.expand(s.diff(expr,q0)*q1+s.diff(expr,q1)*q2+s.diff(expr,q2)*q3+s.diff(expr,q3)*q4)
EL=s.factor(s.diff(Lj,q0)-Dt(s.diff(Lj,q1))+Dt(Dt(s.diff(Lj,q2))))
eq('restricted_curvature_squared_EL',EL,72*(q4-6*q1**2*q2))
eq('nonzero_actual_fourth_order_coefficient',s.diff(EL,q4),72)
assert not Lj.has(q3,q4);checks.append('density_only_metric_secondjet')
# Independent EH conformal order control; no choice of EH as physical action.
LEH=s.simplify(volume*R);LEHj=LEH.subs(jet,simultaneous=True)
eq('EH_boundary_split',LEH,-6*s.diff(s.exp(2*f)*s.diff(f,t),t)+6*s.exp(2*f)*s.diff(f,t)**2)
EEH=s.simplify(s.diff(LEHj,q0)-Dt(s.diff(LEHj,q1))+Dt(Dt(s.diff(LEHj,q2))))
eq('EH_restricted_second_order_EL',EEH,-12*s.exp(2*q0)*(q2+q1**2))
eq('EH_has_no_fourth_order_coefficient',s.diff(EEH,q4))
assert EL.has(q4);checks.append('curvature_square_violates_secondjet_equation_class')
result={'all_passed':True,'count':len(checks),'checks':checks,'actual_R':str(R),'curvature_square_EL':str(EL),'scope':'Actualconformalmetric curvature/variation derivativeorder discriminator; no fR/Einsteinaction adoption or health/fieldsolution'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
