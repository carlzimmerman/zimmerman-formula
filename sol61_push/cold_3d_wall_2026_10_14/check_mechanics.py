import sys,json
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(n,v):
 vv=s.simplify(v);assert vv==0,(n,vv);checks.append(n)
t,x,y,z=s.symbols('t x y z',real=True);coords=(t,x,y,z);V=s.symbols('V',real=True);f=s.Function('s')(x,y,z);b=V*f
geo=json.loads(Path('sol61_push/cold_3d_wall_2026_10_14/geometry_run_v2/calculation/results.json').read_text());names=['B','px','py','pz','hxx','hyy','hzz','hxy','hxz','hyz'];sym={n:s.Symbol(n,real=True) for n in names};R=s.sympify(geo['normal_Ricci'],locals=sym)
values=[b,s.diff(b,x),s.diff(b,y),s.diff(b,z),s.diff(b,x,x),s.diff(b,y,y),s.diff(b,z,z),s.diff(b,x,y),s.diff(b,x,z),s.diff(b,y,z)];R=R.subs(dict(zip(sym.values(),values)),simultaneous=True)
frame=s.eye(4);frame[3,0]=-b;invframe=frame.inv();Rcoord=invframe.T*R*invframe
metric=s.Matrix([[-1+b*b,0,0,b],[0,1,0,0],[0,0,1,0],[b,0,0,1]]);gi=metric.inv()
forcecontract=s.simplify(sum(gi[a,c]*s.diff(Rcoord[a,c],V) for a in range(4) for c in range(4)))
expected=V*(s.diff(f*f,x,2)+s.diff(f*f,y,2)+4*s.diff(f*f,z,2))/2
zero('controllerRicciparametertadpole',forcecontract-expected)
zero('planarcontrolspecialization',forcecontract.subs({s.diff(f,y):0,s.diff(f,z):0,s.diff(f,y,2):0,s.diff(f,z,2):0})-V*(f*s.diff(f,x,2)+s.diff(f,x)**2))
# Actualflatcabinmetricaftertime-dependentcoordinatechange; no inferenceaboutwall.
X=s.Function('X')(t);vel=s.diff(X,t)
g=s.Matrix([[-1+vel**2,0,0,-vel],[0,1,0,0],[0,0,1,0],[-vel,0,0,1]]);ginv=g.inv()
Ga=[[[s.simplify(sum(ginv[a,d]*(s.diff(g[d,c],coords[j])+s.diff(g[d,j],coords[c])-s.diff(g[j,c],coords[d])) for d in range(4))/2) for c in range(4)] for j in range(4)] for a in range(4)]
U=s.Matrix([1,0,0,vel])
zero('cabinpropernormalization',(U.T*g*U)[0]+1)
for a in range(4):zero('testcabinworldlinegeodesic '+str(a),s.diff(U[a],t)+sum(Ga[a][j][k]*U[j]*U[k] for j in range(4) for k in range(4)))
# SpatialflatADMsurfaceintegrand, independentofunitarytimeenergyclaim.
gamma=s.eye(3)
for i in range(3):zero('GRmetricADMenergyintegrand '+str(i),sum(s.diff(gamma[i,j],coords[j+1])-s.diff(gamma[j,j],coords[i+1]) for j in range(3)))
result={'claim':'C3W-003','checks_passed':len(checks),'controller_tadpole_contraction':str(forcecontract),'required_controller_Uprime':'-Mp² V/4*(dx²+dy²+4dz²)s², pointwise; V-onlypotentialgenericallyinsufficient','cabin':'flatinteriorcomovingworldlineisgeodesicandmovesZ=X(t) inlabchart; wallgenerationnotderived','ADMcaveat':'GRgeometricmetricchargeszero; modifiedtheorycanonicalbackgroundenergyandfinitehardwarebudgetnotderived','scope':'Necessarymechanicalrequirementsandkinematics, not autonomouscontrol/physicalcarrier/propulsionproof'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
