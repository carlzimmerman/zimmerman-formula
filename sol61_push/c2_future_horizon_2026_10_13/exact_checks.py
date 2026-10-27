"""Conditional horizon/EF identities and exact vacuum Hamiltonian controls."""
import argparse,json
from pathlib import Path
import sympy as s

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
OUT=Path(ap.parse_args().output);checks=[]
def eq(name,e):
 e=s.simplify(e);assert e==0,(name,e)
 checks.append({'name':name,'passed':True})
def ne(name,e):
 e=s.factor(e);assert e!=0,name
 checks.append({'name':name,'passed':True,'residual':str(e)})

Q,E,S,b=s.symbols('Q E S B',positive=True)
relation=E**2-S**2
ginv=s.Matrix([[0,1],[1,-b]])
qp=s.Matrix([Q*E,Q/(E+S)])
qm=s.Matrix([Q*E,Q*(E+S)/b])
eq('outgoing_phase_rationalization',((E-S)/b-1/(E+S)).subs(b,relation))
eq('outgoing_phase_constant_norm',((qp.T*ginv*qp)[0]-Q**2).subs(b,relation))
eq('incoming_phase_constant_norm',((qm.T*ginv*qm)[0]-Q**2).subs(b,relation))
eq('outgoing_horizon_radial_covector',qp[1].subs(S,E)-Q/(2*E))
eq('outgoing_horizon_radial_flow',(ginv*qp/Q)[1].subs(b,relation).subs(S,E)-E)
eq('outgoing_horizon_null_flow',(ginv*qp/Q)[0].subs(S,E)-1/(2*E))
eq('incoming_pole_residue',(b*qm[1]).subs(S,E)-2*Q*E)
eq('incoming_observer_relative_boost',((qm.T*(ginv*qp/Q))[0]/Q-(2*E**2/b-1)).subs(b,relation))
ne('norm_only_does_not_detect_phase_pole',2*Q*E)
ne('bifurcation_K_zero_contradiction',Q*E)

u,r,th,ph=s.symbols('u r th ph',real=True)
beta=s.Function('beta')(u,r);B=s.Function('B')(u,r)
co=[u,r,th,ph]
g=s.Matrix([[s.exp(2*beta)*B,s.exp(beta),0,0],[s.exp(beta),0,0,0],[0,0,-r**2,0],[0,0,0,-r**2*s.sin(th)**2]])
inv=g.inv();gam={}
for i in range(4):
 for j in range(4):
  for k in range(4):
   v=s.simplify(sum(inv[i,l]*(s.diff(g[l,k],co[j])+s.diff(g[l,j],co[k])-s.diff(g[j,k],co[l])) for l in range(4))/2)
   if v!=0:gam[i,j,k]=v
def C(i,j,k):return gam.get((i,j,k),s.S.Zero)
def ric(i,j):return s.simplify(sum(s.diff(C(k,i,j),co[k])-s.diff(C(k,i,k),co[j])+sum(C(k,k,l)*C(l,i,j)-C(k,j,l)*C(l,i,k) for l in range(4)) for k in range(4)))
Ric=s.zeros(4)
for i,j in [(0,0),(0,1),(1,0),(1,1),(2,2),(3,3)]:Ric[i,j]=ric(i,j)
scalar=s.simplify(s.trace(inv*Ric));Gcov=Ric-g*scalar/2;Gmix=inv*Gcov
Guu=s.simplify(Gmix[0,0]);Gru=s.simplify(Gmix[1,0]);Grr=s.simplify(Gcov[1,1]);Gang=s.simplify(Gmix[2,2])
eq('general_EF_mass_radial',Guu-((1-B)/r**2-s.diff(B,r)/r))
eq('general_EF_mass_time',Gru-s.diff(B,u)/r)
eq('general_EF_beta_radial',Grr-2*s.diff(beta,r)/r)
ang=s.Function('e')(u,r);res=s.diag(0,0,ang,ang)
div=sum(s.diff(res[mu,1],co[mu])+sum(C(mu,mu,la)*res[la,1]-C(la,mu,1)*res[mu,la] for la in range(4)) for mu in range(4))
eq('angular_Bianchi_closure',div+2*ang/r)

G,a,X0=s.symbols('G a X0',positive=True)
bb=s.Function('b')(r);sv=s.Function('S')(r);chi=s.Function('chi')(u,r)
dm=s.Function('dm')(u,r);dbeta=s.Function('dbeta')(u,r)
ct=-(E+sv)*(sv*s.diff(chi,r)+(2*sv/r+s.diff(sv,r))*chi)
mr=8*s.pi*a*X0*E*r**2*chi/(E+sv)
mt=-8*s.pi*a*X0*E*r**2*sv*chi
betar=8*s.pi*G*a*X0*r*chi/(E+sv)**2
eq('mass_integrability',s.diff(mr,u).subs(s.diff(chi,u),ct)-s.diff(mt,r))
eq('linear_EF_radial_Einstein',2*G*mr/r**2-8*s.pi*G*2*a*X0*chi*E/(E+sv))
eq('linear_EF_time_Einstein',-2*G*mt/r**2-8*s.pi*G*2*a*X0*chi*E*sv)
eq('linear_EF_rr_Einstein',2*betar/r-8*s.pi*G*2*a*X0*chi/(E+sv)**2)
eq('linear_constraints_horizon_beta',betar.subs(sv,E)-2*s.pi*G*a*X0*r*chi/E**2)
eq('linear_constraints_horizon_mass',mr.subs(sv,E)-4*s.pi*a*X0*r**2*chi)

# Regular background geodesic and conserved scalar dust source.
bg=s.Matrix([[bb,1,0,0],[1,0,0,0],[0,0,-r**2,0],[0,0,0,-r**2*s.sin(th)**2]])
bgi=bg.inv();bgc={}
for i in range(4):
 for j in range(4):
  for k in range(4):
   v=s.simplify(sum(bgi[i,l]*(s.diff(bg[l,k],co[j])+s.diff(bg[l,j],co[k])-s.diff(bg[j,k],co[l])) for l in range(4))/2)
   if v!=0:bgc[i,j,k]=v
def BC(i,j,k):return bgc.get((i,j,k),s.S.Zero)
Uv=s.Matrix([1/(E+sv),sv,0,0]);Uc=s.Matrix([E,1/(E+sv),0,0])
def red(e):
 e=e.subs(s.diff(chi,u),ct).subs(s.diff(sv,r),-s.diff(bb,r)/(2*sv)).subs(bb,E**2-sv**2)
 return s.factor(s.together(e))
eq('regular_unit_flow',red((Uv.T*bg*Uv)[0]-1))
for i in [0,1]:
 acc=sum(Uv[j]*s.diff(Uv[i],co[j]) for j in range(4))+sum(BC(i,j,k)*Uv[j]*Uv[k] for j in range(4) for k in range(4))
 eq('regular_geodesic_'+str(i),red(acc))
source=2*a*X0*chi*(Uv*Uc.T)
for nu in [0,1]:
 div=sum(s.diff(source[mu,nu],co[mu])+sum(BC(mu,mu,la)*source[la,nu]-BC(la,mu,nu)*source[mu,la] for la in range(4)) for mu in range(4))
 eq('regular_source_conservation_'+str(nu),red(div))
piu,pir=s.symbols('piu pir');Qv=s.sqrt(2*X0)
deltaB=-2*G*dm/r
h=s.Matrix([[deltaB+2*bb*dbeta,dbeta],[dbeta,0]])
qq=Qv*s.Matrix([1/(E+sv),sv]);hpart=(qq.T*h*qq)[0]/2
force=(E+sv)*chi/Qv+Qv*E*dbeta-Qv*G*dm/(r*(E+sv))
eq('regular_phase_reconstruction',red((Qv*(piu/(E+sv)+sv*pir)-hpart-chi).subs(piu,force-sv*(E+sv)*pir)))
ne('omitted_metric_phase_term_detected',red(-hpart))

# Exact vacuum Hamilton-Jacobi controls on the original static patch.
x,p,Ns,Bs=s.symbols('x p N B',positive=True)
calH=Ns*s.sqrt(1+Bs*p**2)
eq('vacuum_Hpp',s.diff(calH,p,2)-Ns*Bs/(1+Bs*p**2)**s.Rational(3,2))
Hxx,Hxp,Hpp=s.symbols('Hxx Hxp Hpp',real=True)
A=s.Matrix([[-Hxp,-Hpp],[Hxx,Hxp]]);Omega=s.Matrix([[0,1],[-1,0]])
eq('Hamilton_variational_symplectic',(A.T*Omega+Omega*A).norm())
Hr,Hp=s.symbols('Hr Hp',real=True)
eq('Hamilton_energy_conservation',Hr*(-Hp)+Hp*Hr)
M11,M12,M21,M22,pprime=s.symbols('M11 M12 M21 M22 pprime',real=True)
proj=M11+M12*pprime;momentum=M21+M22*pprime
eq('Jacobian_fold_keeps_momentum',M11*momentum-M21*proj-(M11*M22-M12*M21)*pprime)
# More directly an invertible M cannot annihilate vector(1,pprime).
eq('fold_invertibility_identity',M22*proj-M12*momentum-(M11*M22-M12*M21))
tt,large,hpp=s.symbols('t A hpp',positive=True)
eq('projection_caustic_leading_sign',(1-hpp*large*tt).subs(tt,2/(hpp*large))+1)
z=s.symbols('z',real=True);cut=1-10*z**3+15*z**4-6*z**5
eq('quintic_cut_derivative',s.diff(cut,z)+30*z**2*(1-z)**2)
eq('quintic_cut_max_derivative',30*s.Rational(1,4)**2/s.Rational(15,100)-s.Rational(25,2))
OUT.write_text(json.dumps({'all_passed':True,'count':len(checks),'checks':checks,'general_EF_angular_Einstein':str(Gang),'scope':'conditional exact identities and controls; nonlinear lifespan proof is separate; no quantum/TOE certification'},indent=2)+'\n')
print(json.dumps({'all_passed':True,'count':len(checks)}))
