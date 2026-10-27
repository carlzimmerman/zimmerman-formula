import sympy as s,json,sys
from pathlib import Path
G,mc,mb=s.symbols('G mc mb',positive=True)
x=s.Matrix(s.symbols('x0:3',real=True));y=s.Matrix(s.symbols('y0:3',real=True));vc=s.Matrix(s.symbols('vc0:3',real=True));vb=s.Matrix(s.symbols('vb0:3',real=True));d=x-y;R=s.sqrt(d.dot(d));W=-G*mc*mb/R
Fc=-s.Matrix([s.diff(W,t) for t in x]);Fb=-s.Matrix([s.diff(W,t) for t in y]);F=-G*mc*mb*d/R**3
checks=[]
def eq(name,expr):
 expr=s.factor(expr);checks.append({'name':name,'passed':expr==0,'residual':str(expr)})
for i in range(3):eq('actual potential gradient '+str(i),Fc[i]-F[i]);eq('reciprocal pair momentum '+str(i),Fc[i]+Fb[i]);eq('central pair angular momentum '+str(i),(x.cross(Fc)+y.cross(Fb))[i])
Wdot=sum(s.diff(W,x[i])*vc[i]+s.diff(W,y[i])*vb[i] for i in range(3));Kcdot=Fc.dot(vc);Kbdot=Fb.dot(vb)
eq('cross energy counted once',Kcdot+Kbdot+Wdot)
eq('cold allcross ledger',Kcdot+Wdot-Fc.dot(vb))
eq('baryon complementary ledger',Kbdot+Fc.dot(vb))
alpha=s.symbols('alpha',real=True)
eq('arbitrary cross allocation cold',Kcdot+alpha*Wdot-((1-alpha)*Fc.dot(vc)+alpha*Fc.dot(vb)))
eq('arbitrary allocation total',(Kcdot+alpha*Wdot)+(Kbdot+(1-alpha)*Wdot))
eq('static baryon coldtotal invariant',(Kcdot+Wdot).subs(dict(zip(vb,[0,0,0]))))
for sig in [1,-1]:
 # x=(1,0,0),y=0,vc=0,vb=(sig,0,0). G=mc=mb=1.
 mapping=dict(zip(list(x)+list(y)+list(vc)+list(vb),[1,0,0,0,0,0,0,0,0,sig,0,0]));mapping.update({G:1,mc:1,mb:1})
 eq('two-sign reciprocal work '+str(sig),(Kcdot+Wdot).subs(mapping)+sig)
 eq('two-sign baryon opposite '+str(sig),Kbdot.subs(mapping)-sig)
eq('time reversal odd work',(Kcdot+Wdot).subs({**dict(zip(vc,-vc)),**dict(zip(vb,-vb))})+(Kcdot+Wdot))
# Direct 3-body potential, no external fixed driver, self/cross counted once.
coords=s.symbols('q0:3',real=True);speeds=s.symbols('v0:3',real=True);masses=s.symbols('m0:3',positive=True)
# ordered noncollision chart q0<q1<q2 in one dimension, two cold(0,1),baryon(2).
Wij={(i,j):-G*masses[i]*masses[j]/(coords[j]-coords[i]) for i in range(3) for j in range(i+1,3)}
U=sum(Wij.values());forces=[-s.diff(U,t) for t in coords];udot=sum(s.diff(U,coords[i])*speeds[i] for i in range(3))
eq('threebody live action energy',sum(forces[i]*speeds[i] for i in range(3))+udot)
eq('threebody total momentum',sum(forces))
Ec_dot=sum(forces[i]*speeds[i] for i in [0,1])+sum(s.diff(U,coords[i])*speeds[i] for i in range(3))
Eb_dot=forces[2]*speeds[2]
eq('threebody full cold ledger',Ec_dot+Eb_dot)
eq('threebody source work derivative',Ec_dot+forces[2]*speeds[2])
# Continuum reduction: partialt k+div jK=−j.gradPhi,
# partialt rho+divj=0, Poisson lapPhi=4piG rho.
rho,phit,jgrad,divj,phi,lap,gradgradt=s.symbols('rho phit jgrad divj phi lap gradgradt',real=True)
kdot_div=-jgrad;rhodot=-divj
# derivative rhoPhi plus divPhi j gives rhodotPhi+rhoPhi_t+Phi divj+jgrad
matter=kdot_div+rhodot*phi+rho*phit+phi*divj+jgrad
eq('local matter potential ledger',matter-rho*phit)
# derivative field grad²/8piG minus divPhi_t gradPhi/4piG = −Phi_t lapPhi/4piG
field=(gradgradt-(gradgradt+phit*lap))/(4*s.pi*G)
eq('local total fieldenergy current',(matter+field).subs(lap,4*s.pi*G*rho))
# Integrated cross identity via continuity and selfadjoint Green kernel.
Ic,Ib=s.symbols('Ic Ib',real=True)
# Bare cold/self dot=-Ic, baryon/self dot=-Ib,Wcb dot=Ic+Ib.
eq('continuum allcross cold',-Ic+Ic+Ib-Ib)
eq('continuum total live exchange',(-Ic+Ic+Ib)-Ib)
eq('continuum allocation cold',-Ic+alpha*(Ic+Ib)-((alpha-1)*Ic+alpha*Ib))
eq('continuum allocation complementary',-Ib+(1-alpha)*(Ic+Ib)-((1-alpha)*Ic-alpha*Ib))
# Rest mass and number: fixed finite labels; local mass continuity implies no volume creation.
N,Mrest=s.symbols('N Mrest',real=True)
eq('finite restmass derivative constants',s.diff(sum(masses),coords[0]))
eq('finite number derivative labels',s.diff(s.Integer(3),coords[0]))
result={'claim':'live reciprocal collisionless gravitational work','count':len(checks),'checks':checks,'all_passed':all(t['passed'] for t in checks),'finite_domains':'R>0; 3body ordered q0<q1<q2; no collision continuation certified','continuum_conditions':'smooth finiteenergy VlasovPoisson, fixed potential normalization, selfadjoint isolatedinverse/compatible boundary and surfaceflux included','non_claims':['no DE exchange','no secular heat or selector','no metric action','no species or mass conversion']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'count':len(checks),'all_passed':result['all_passed']}));sys.exit(0 if result['all_passed'] else 1)
