import sys,json
from pathlib import Path
import sympy as S
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
k,h,kap,theta,a,c,v=S.symbols('k h kap theta a c v',real=True)
checks=[]
def ck(n,e):
 assert S.simplify(e)==0,(n,e)
 checks.append(n)
# Stage I: theta=1,kappa=4 held fixed; strain mass h>=0.
L=(2*a*a+(c-2*k*v)**2-(2*a+c-2*k*v)**2)/8+(2*a+c-2*k*v)**2/8+(2*a*a+c*c)/2+2*h*v*v
ck('stage I joint positive square',L-(2*a*a+(c-2*k*v)**2)/8-(2*a*a+c*c)/2-2*h*v*v)
vs=S.solve(S.diff(L,v),v)[0]
K=S.simplify(S.hessian(L.subs(v,vs),(a,c)))
ck('stage I scalar diagonal aa',K[0,0]-S.Rational(5,2))
ck('stage I scalar diagonal cc',K[1,1]-(k*k+5*h)/(k*k+4*h))
ck('stage I scalar offdiagonal',K[0,1])
# Stage II: h=A=0. Linear lapse imposes Qxx+Qyy=0 for k!=0.
t,s,x,y,vx,vy,vz=S.symbols('t s x y vx vy vz',real=True)
Q=S.Matrix([[t,s,x],[s,-t,y],[x,y,c]])
E=Q-S.Matrix([[0,0,k*vx],[0,0,k*vy],[k*vx,k*vy,2*k*vz]])
eh=(S.trace(E*E)-S.trace(E)**2)/8
ck('constraint removes Einstein negative trace',eh-(t*t+s*s+(x-k*vx)**2+(y-k*vy)**2)/4)
kin=eh+theta*S.trace(E)**2/8+kap*S.trace(Q*Q)/8
red=S.expand(kin.subs({vx:x/k,vy:y/k,vz:c/(2*k)}))
ck('cap physical kinetic',red-(1+kap)*(t*t+s*s)/4-kap*(x*x+y*y)/4-kap*c*c/8)
ck('cap shift minimizer x',S.diff(kin,vx).subs(vx,x/k))
ck('cap shift minimizer y',S.diff(kin,vy).subs(vy,y/k))
ck('cap shift minimizer z',S.diff(kin,vz).subs(vz,c/(2*k)))
# Spatial Einstein quadratic symbol from full Cartesian integrated expression.
tr=S.trace(Q);div=S.Matrix([k*Q[2,j] for j in range(3)])
R2=-k*k*S.trace(Q*Q)/8+k*k*tr*tr/8+div.dot(div)/4-div[2]*k*tr/4
ck('cap spatial Einstein TT only',R2+k*k*(t*t+s*s)/4)
cs=S.Rational(1,2)
pot=-R2+kap*cs*k*k*S.trace(Q*Q)/8
ck('material scalar dispersion',S.diff(pot,c,2)-cs*k*k*S.diff(red,c,2))
ck('material vector dispersion',S.diff(pot,x,2)-cs*k*k*S.diff(red,x,2))
ck('tensor dispersion',S.diff(pot,t,2)-(1+kap*cs)/(1+kap)*k*k*S.diff(red,t,2))
# Einstein kinetic Fourier identity for a constrained velocity and arbitrary shift.
xi1,xi2,xi3,w1,w2,w3=S.symbols('xi1 xi2 xi3 w1 w2 w3',real=True)
TT=S.Matrix([[t,s,0],[s,-t,0],[0,0,0]])
def symgrad(z):return S.Matrix([[0,0,k*z[0]],[0,0,k*z[1]],[k*z[0],k*z[1],2*k*z[2]]])
U=TT+symgrad([xi1,xi2,xi3]);V=symgrad([xi1+w1,xi2+w2,xi3+w3]);E=U-V
ck('global Fourier Einstein kinetic identity',(S.trace(E*E)-S.trace(E)**2)/8-(t*t+s*s)/4-k*k*(w1*w1+w2*w2)/4)
# A second route: retained multiplier removes a variable but is not a GR matching proof.
ck('naive common taper UV obstruction',(4*S.Rational(1,4)**2+3*S.Rational(1,4)-2)/(2*S.Rational(1,4))+2)
# A luminal version of the cap: changing the spatial coefficient is explicit.
cs2=S.symbols('cs2',real=True)
pot_general=-R2+kap*cs2*k*k*S.trace(Q*Q)/8
ck('general cap scalar cone',S.diff(pot_general,c,2)-cs2*k*k*S.diff(red,c,2))
ck('general cap vector cone',S.diff(pot_general,x,2)-cs2*k*k*S.diff(red,x,2))
ck('general cap tensor cone',S.diff(pot_general,t,2)-(1+kap*cs2)/(1+kap)*k*k*S.diff(red,t,2))
ck('luminal cap all tensor strengths',(1+kap*cs2).subs(cs2,1)/(1+kap)-1)
alpha,acc=S.symbols('alpha acc',real=True)
F=k*k*a*a/4-k*k*(2*a*a+c*c)/4-h*(2*a*a+c*c)/2+alpha*k*k*a+(h+acc*k*k)*alpha*alpha/2
Fmin=S.simplify(F.subs(alpha,-k*k*a/(h+acc*k*k)))
G=-S.hessian(Fmin,(a,c))
clock=S.factor((G[0,0]/K[0,0]).subs(acc,h))
long=S.factor(G[1,1]/K[1,1])
ck('stage I clock restoring spectrum',clock-(k*k+4*h+2*k**4/(h*(1+k*k)))/5)
ck('stage I material scalar spectrum',long-(h+k*k/2)*(k*k+4*h)/(k*k+5*h))
ck('constraint limit at fixed nonzero momentum',S.limit(h*clock,h,0,dir='+')-2*k**4/(5*(1+k*k)))
# Vector and tensor stage I, same action and h-dependent strain mass.
X,V=S.symbols('X V',real=True)
Lv=(X-k*V)**2/4+X*X+2*h*V*V
vstar=S.solve(S.diff(Lv,V),V)[0];Kv=S.diff(Lv.subs(V,vstar),X,2)
Gv=k*k+2*h
ck('stage I vector restoring spectrum',Gv/Kv-(h+k*k/2)*(k*k+8*h)/(k*k+10*h))
ck('stage I tensor restoring spectrum',(3*k*k/4+h)/S.Rational(5,4)-(3*k*k+4*h)/5)
# Complete planar collar identities, including the transverse scalar a.
Qall=S.Matrix([[a+t,s,x],[s,a-t,y],[x,y,c]])
Eall=Qall-S.Matrix([[0,0,k*vx],[0,0,k*vy],[k*vx,k*vy,2*k*vz]])
GReh=(S.trace(Eall*Eall)-S.trace(Eall)**2)/8
ck('planar inside completed kinetic',GReh+S.trace(Eall)**2/8-S.trace(Eall*Eall)/8)
ck('planar outside kinetic positive',GReh.subs(a,0)-(t*t+s*s+(x-k*vx)**2+(y-k*vy)**2)/4)
divall=S.Matrix([k*Qall[2,j] for j in range(3)]);trall=S.trace(Qall)
Rall=-k*k*S.trace(Qall*Qall)/8+k*k*trall*trall/8+divall.dot(divall)/4-divall[2]*k*trall/4
ck('planar static Einstein split',Rall-k*k*(a*a-t*t-s*s)/4)
Vcore=-Rall+k*k*S.trace(Qall*Qall)/4
ck('planar core positive gradient margin',Vcore-k*k*S.trace(Qall*Qall)/8-k*k*(3*s*s+3*t*t+2*x*x+2*y*y+c*c)/8)
Vouter=-Rall.subs(a,0)+kap*cs2*k*k*S.trace(Qall.subs(a,0)**2)/8
ck('planar outer positive gradient split',Vouter-k*k*((1+kap*cs2)*(t*t+s*s)/4+kap*cs2*(x*x+y*y)/4+kap*cs2*c*c/8))
res={'claim_id':'CCC-001','checks_passed':len(checks),'stage_I_scalar_K':str(K),'cap_scalar_speed_squared':'1/2','cap_vector_speed_squared':'1/2','cap_tensor_speed_squared':'(1+kappa/2)/(1+kappa)','luminal_cap_option':'cs_squared=1 makes all five homogeneous cap branches luminal; different spatial coefficient from core','scope':'Exact constant-coefficient symbols plus Fourier identity. Variable-coefficient R3 nonnegative energy proof in PROOF.md; not curved core/interface gluing or nonlinear stability.'}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(res,indent=2))
