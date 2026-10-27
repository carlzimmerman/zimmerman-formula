from pathlib import Path
import json,sys,sympy as s
DEST=Path(sys.argv[1]);checks=[]
def z(name,expr):
 residual=s.simplify(s.expand(expr));checks.append({'name':name,'passed':residual==0,'residual':str(residual)})
def yes(name,c):checks.append({'name':name,'passed':bool(c),'condition':str(c)})
g,m,a,b,lam=s.symbols('g m a b lambda_total',positive=True,real=True);v,w=s.symbols('v w',real=True)
phi,phic,chi,chic,pdot,pcdot,cdot,ccdot=s.symbols('phi phic chi chic phidot phicdot chidot chicdot')
Vi=g*(chic*phi**2+chi*phic**2)
Wphi=-(pcdot*s.diff(Vi,phic)+pdot*s.diff(Vi,phi));Wchi=-(ccdot*s.diff(Vi,chic)+cdot*s.diff(Vi,chi))
store=s.diff(Vi,phi)*pdot+s.diff(Vi,phic)*pcdot+s.diff(Vi,chi)*cdot+s.diff(Vi,chic)*ccdot
z('component work plus interaction storage conserved',Wphi+Wchi+store)
state={phi:a,phic:a,chi:b,chic:b,pdot:v-s.I*m*a,pcdot:v+s.I*m*a,cdot:w-2*s.I*m*b,ccdot:w+2*s.I*m*b}
q=s.I*(phic*pdot-phi*pcdot)+2*s.I*(chic*cdot-chi*ccdot)
Q=s.simplify(q.subs(state));z('positive-charge snapshot exact convention',Q-(2*m*a*a+8*m*b*b));yes('nonzero positive U1 charge',Q.is_positive)
qphi=s.simplify(Wphi.subs(state));qchi=s.simplify(Wchi.subs(state));storage=s.simplify(store.subs(state))
z('actual daughter energy work rate',qphi+4*g*a*b*v)
z('actual source energy work rate',qchi+2*g*a*a*w)
z('actual stored-interaction rate',storage-(4*g*a*b*v+2*g*a*a*w))
zero_store={w:-2*b*v/a};z('momentum-neutral zero-storage snapshot',storage.subs(zero_store));z('equal-opposite component exchange at this snapshot',(qphi+qchi).subs(zero_store))
vpos=s.symbols('vpositive',positive=True)
yes('export from daughter for positive radial velocity',s.simplify(qphi.subs(v,vpos)).is_negative)
yes('import to daughter for opposite radial velocity',s.simplify(qphi.subs(v,-vpos)).is_positive)
yes('generic omitted storage mutation detected',s.simplify(qphi+qchi)!=0)
# Number/rest-mass bookkeeping of the already supplied on-shell reaction.
M,J=s.symbols('M J',real=True);delta=s.symbols('gap',positive=True)
z('charge invariant of source decay',J+J+2*(-J))
z('rest-mass sum changes by gap',(m*J+m*J-M*J).subs(M,2*m+delta)+delta*J)
yes('daughter number alone is not conserved',s.simplify(2*J)!=0)
# Homogeneous fields have zero T0i at this instant for arbitrary time velocities.
dphi,dc=s.symbols('gradphi gradchi');mom=-(pcdot*dphi+pdot*s.conjugate(dphi)+ccdot*dc+cdot*s.conjugate(dc));z('homogeneous physical momentum zero',mom.subs({dphi:0,dc:0}))
out={'checks':checks,'all_passed':all(x['passed'] for x in checks),'component_work':{'daughter':str(qphi),'source':str(qchi),'interaction_storage':str(storage)},'positive_charge':str(Q),'zero_storage_snapshot':'w=-2b v/a at one instant only','rest_mass_sum_derivative':'(2m-M)J=-gap J, while weighted U1 charge remains conserved','scope':'Exact classical instantaneous component exchange of existing trilinear interaction in homogeneous finite periodic initial data. No quantum assumptions, new action, relaxation rate or selector.'};(DEST/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['all_passed']
