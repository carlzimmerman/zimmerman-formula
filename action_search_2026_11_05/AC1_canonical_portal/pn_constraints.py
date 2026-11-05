import argparse,json,itertools
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
rows=[];checks={}
k1,k2,k3,u1,u2,g,w=s.symbols('k1 k2 k3 u1 u2 g w',real=True)
K=s.Matrix([[k1,k2],[k2,k3]]);U=s.diag(u1,u2);G=s.Matrix([[0,g],[-g,0]])
poly=s.expand((U-w*w*K-s.I*w*G).det())
checks['frequency_polynomial']=s.simplify(poly-((k1*k3-k2*k2)*w**4-(k1*u2+k3*u1+g*g)*w*w+u1*u2))==0
for ss,ang,kk,gg,vv,mu_fraction in itertools.product(['.1','1','100'],[0,1,2],[1,100],[0,1],[0,1],[0,1]):
 vals=[]
 for prec in [40,80]:
  with mp.workdps(prec):
   z=mp.mpf(ss);theta=mp.pi*ang/4;k=mp.mpf(kk);gam=mp.mpf(gg);v=mp.mpf(vv)
   n=mp.matrix([mp.sin(theta),0,mp.cos(theta)]);kv=k*n
   D=mp.diag([1+z,1+z,(1+z)**2])+gam*kv*kv.T;Di=D**-1
   Q=(n.T*Di*n)[0];mu=mu_fraction*mp.mpf('.1')*k*k*(1-Q);delta=k*k*(1-Q)-mu
   C=mp.zeros(4);C[0,0]=-k*k+mu
   B=mp.zeros(4,2);B[0,0]=-v;B[0,1]=-mu
   E=mp.zeros(4,2);E[0,0]=-mp.mpf('.3');E[3,0]=-mp.mpf('.2')
   for i in range(3):
    C[0,i+1]=C[i+1,0]=kv[i];B[i+1,1]=-kv[i]
    for j in range(3):C[i+1,j+1]=-D[i,j]
   Ci=C**-1;Kin=mp.diag([1,mu])-B.T*Ci*B;Rot=-B.T*Ci*E;Mass=mp.diag([k*k+1,k*k])+E.T*Ci*E
   Ka=mp.matrix([[1+v*v/delta,v*(mu+k*k*Q)/delta],[v*(mu+k*k*Q)/delta,k*k*(mu+k*k*Q)/delta]])
   qa=(n.T*Di*mp.matrix([0,0,1]))[0]
   Ua=k*k+1-mp.mpf('.2')**2*Di[2,2]-(mp.mpf('.3')+mp.mpf('.2')*k*qa)**2/delta
   err=max(abs(Kin[i,j]-Ka[i,j])/(1+abs(Kin[i,j])) for i in range(2) for j in range(2))
   err=max(err,abs(Ua-Mass[0,0])/(1+abs(Ua)))
   det=mp.det(Kin);want=(k*k+v*v)*(mu+k*k*Q)/delta
   err=max(err,abs(det-want)/(1+abs(want)))
   anti=(Rot-Rot.T)[0,1];coef=Kin[0,0]*Mass[1,1]+Kin[1,1]*Mass[0,0]+anti*anti
   disc=coef*coef-4*det*mp.det(Mass)
   roots=[(coef+sign*mp.sqrt(disc))/(2*det) for sign in [-1,1]]
   # Independent direct determinant evaluation at the two candidate frequencies.
   root_error=max(abs(mp.det(Mass-x*Kin-mp.j*mp.sqrt(x)*(Rot-Rot.T)))/(1+abs(coef*x)+abs(det*x*x)) for x in roots)
   vals.append([Kin[0,0],Kin[1,1],det,Mass[0,0]])
   # Mutant flips sign of delta while mu remains positive.
   mut_mu=2*k*k*(1-Q);mut_det=(k*k+v*v)*(mut_mu+k*k*Q)/(k*k*(1-Q)-mut_mu)
   if prec==80:
    rows.append(dict(s=float(z),angle_pi_over_4=ang,k=kk,gamma=gg,v=vv,mu_fraction=.1*mu_fraction,formula_error=float(err),precision_error=float(max(abs(a-b)/(1+abs(a)) for a,b in zip(vals[1],vals[0]))),K_positive=bool(Kin[0,0]>0 and det>0),U11=float(Mass[0,0]),squared_frequencies=[float(mp.re(x)) for x in roots],root_error=float(root_error),mutant_det_negative=bool(mut_det<0),sign_prediction=bool(all(mp.re(x)>0 for x in roots) if Mass[0,0]>0 else mp.re(roots[0]*roots[1])<0)))
checks.update(count=len(rows)==144,formula=all(x['formula_error']<1e-25 for x in rows),precision=all(x['precision_error']<1e-25 for x in rows),positive_K=all(x['K_positive'] for x in rows),negative_control=all(x['mutant_det_negative'] for x in rows),spectrum=all(x['sign_prediction'] and x['root_error']<1e-25 for x in rows))
# Exact negative-mass control: K=I, U=diag(-1,1), G12=1.
mut_poly=poly.subs({k1:1,k2:0,k3:1,u1:-1,u2:1,g:1})
checks['negative_mass_control']=s.expand(mut_poly-(w**4-w**2-1))==0
# Decoupled known answer for the complete conditional two-coordinate model.
Q0,kk0,mm0,rr0=s.symbols('Q0 kk0 mm0 rr0',positive=True)
dec=poly.subs({k1:1,k2:0,k3:kk0**2*Q0/(1-Q0),u1:kk0**2+mm0,u2:rr0*kk0**2,g:0})
checks['decoupled_known_answer']=s.simplify(dec-kk0**2*Q0/(1-Q0)*(w**2-kk0**2-mm0)*(w**2-rr0*(1-Q0)/Q0))==0
R=dict(checks=checks,rows=rows,scope='Conditional frozen PN model; no on-shell full-action health claim.')
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(R,indent=2));print(json.dumps(dict(checks=checks,positive_U=sum(x['U11']>0 for x in rows),negative_U=sum(x['U11']<0 for x in rows)),indent=2));assert all(checks.values())
