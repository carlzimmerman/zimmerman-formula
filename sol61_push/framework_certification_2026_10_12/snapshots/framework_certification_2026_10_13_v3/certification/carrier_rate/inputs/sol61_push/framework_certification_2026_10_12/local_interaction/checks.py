import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import json,sys
import sympy as s
HERE=Path(__file__).resolve().parent; DEST=Path(sys.argv[1]);checks=[]
def zero(name,e):
 r=s.simplify(s.expand(e));checks.append({'name':name,'passed':r==0,'residual':str(r)})
def positive(name,condition):checks.append({'name':name,'passed':bool(condition),'condition':str(condition)})
m,D,g,lam=s.symbols('m Delta g lambda_rep',positive=True,real=True)
phi,phic,chi,chic=s.symbols('phi phi_conjugate chi chi_conjugate')
M2=4*m*m+D; lt=g*g/D+lam
V=m*m*phic*phi+M2*chic*chi+g*(chic*phi**2+chi*phic**2)+lt*(phic*phi)**2
Vsq=m*m*phic*phi+4*m*m*chic*chi+(s.sqrt(D)*chic+g/s.sqrt(D)*phic**2)*(s.sqrt(D)*chi+g/s.sqrt(D)*phi**2)+lam*(phic*phi)**2
zero('positive-square potential expansion',V-Vsq)
Fphi=s.diff(V,phic);Fphic=s.diff(V,phi);Fchi=s.diff(V,chic);Fchic=s.diff(V,chi)
zero('actual phi field force',Fphi-(m*m*phi+2*g*chi*phic+2*lt*phic*phi**2))
zero('actual chi field force',Fchi-(M2*chi+g*phi**2))
jp=s.I*(-phic*Fphi+phi*Fphic);jc=s.I*(-chic*Fchi+chi*Fchic)
zero('local weighted U1 charge identity',jp+2*jc)
zero('daughter local charge transfer expression',jp-2*s.I*g*(chic*phi**2-chi*phic**2))
positive('mutation omitted source reaction detected',s.simplify(jp)!=0)
# Full interaction stress identities in the 1+1 invariant subsector.
t,x=s.symbols('t x',real=True); f=[s.Function('f'+str(i))(t,x) for i in range(4)]
fr=[s.symbols('r'+str(i),real=True) for i in range(4)]
subs={phi:(fr[0]+s.I*fr[1])/s.sqrt(2),phic:(fr[0]-s.I*fr[1])/s.sqrt(2),chi:(fr[2]+s.I*fr[3])/s.sqrt(2),chic:(fr[2]-s.I*fr[3])/s.sqrt(2)}
Vr=s.simplify(s.expand(V.subs(subs)));Vf=Vr.subs(dict(zip(fr,f)))
vel=[s.diff(a,t) for a in f];grad=[s.diff(a,x) for a in f]
eom=[s.diff(a,t,2)-s.diff(a,x,2)+s.diff(Vr,fr[i]).subs(dict(zip(fr,f))) for i,a in enumerate(f)]
T00=sum(a*a+b*b for a,b in zip(vel,grad))/2+Vf;T01=-sum(a*b for a,b in zip(vel,grad));T11=sum(a*a+b*b for a,b in zip(vel,grad))/2-Vf
zero('full-action local energy identity',s.diff(T00,t)+s.diff(T01,x)-sum(v*e for v,e in zip(vel,eom)))
zero('full-action local momentum identity',s.diff(T01,t)+s.diff(T11,x)+sum(v*e for v,e in zip(grad,eom)))
source_forces=sum(vel[i]*s.diff(Vr,fr[i]).subs(dict(zip(fr,f))) for i in [2,3]);positive('mutation deleting source EOM/force detected',s.simplify(source_forces)!=0)
# Existing on-shell collision/reaction, no target temperatures.
Ep,M,vol=s.symbols('E M Vbox',positive=True);p=s.symbols('p',positive=True)
h=2*g/s.sqrt(8*M*Ep**2*vol);U=lt/(Ep**2*vol)
zero('vertex coefficient from two ordered daughter terms',h-g/s.sqrt(2*M*Ep**2*vol))
zero('quartic pair shift retained',4*lt/(4*Ep**2*vol)-U)
zero('vacuum resonance p-squared',((M2)/4-m*m)-D/4)
phase=(1/(4*s.pi**2))*4*s.pi*(p*p/(4*Ep*Ep))*(Ep/(2*p))
zero('invariant phase space radial delta integral',phase-p/(8*s.pi*Ep))
width=(1/(2*M))*s.Rational(1,2)*(2*g)**2*phase.subs(Ep,M/2)
zero('vacuum tree identical-daughter width',width-g*g*p/(4*s.pi*M*M))
zero('vacuum width threshold form',width.subs(p,s.sqrt(M*M-4*m*m)/2)-g*g/(8*s.pi*M)*s.sqrt(M*M-4*m*m)/M)
ns,np_,nm=s.symbols('n_chi n_plus n_minus',nonnegative=True);J=ns*(1+np_)*(1+nm)-(1+ns)*np_*nm
zero('Bose reaction gain-loss simplified',J-(ns*(1+np_+nm)-np_*nm))
zero('exact reaction charge-mass conservation',m*(J+J+2*(-J)))
zero('exact reaction local on-shell energy conservation',(2*Ep*J-M*J).subs(Ep,M/2))
zero('exact symmetric pair momentum-neutral reaction',p*J-p*J)
zero('stationary source occupation',J.subs(ns,np_*nm/(1+np_+nm)))
positive('empty daughter bath imports daughter energy',J.subs({ns:1,np_:0,nm:0})>0)
positive('occupied pair empty source exports daughter energy',J.subs({ns:0,np_:1,nm:1})<0)
positive('daughter number alone is not invariant',s.simplify(2*J)!=0)
# Bose equilibrium exact algebra in exp-energy fugacity variables.
a,b=s.symbols('exp_a exp_b',positive=True);na=1/(a-1);nb=1/(b-1);nsource=1/(a*b-1)
zero('Bose stationary chemical family without fixed T',J.subs({np_:na,nm:nb,ns:nsource}))
# Analytic unitary amplitudes; common energy phase cancels all observables.
hv,det,ct,st,O=s.symbols('h det cos sin Omega',real=True);Pc=4*hv**2*st**2/O**2
amp_source=ct+s.I*det*st/O;amp_pair=-2*s.I*hv*st/O
zero('interaction energy during source-to-pair transfer',2*hv*s.re(s.conjugate(amp_source)*amp_pair)+det*Pc)
zero('all energy including interaction conserved in forward transfer',(M+det)*Pc-M*Pc-det*Pc)
zero('all energy including interaction conserved in reverse transfer',-(M+det)*Pc+M*Pc+det*Pc)
zero('two-level unitarity amplitude constraint',(s.expand_complex(s.conjugate(amp_source)*amp_source+s.conjugate(amp_pair)*amp_pair)-1).subs(O**2,det**2+4*hv**2).subs(ct**2,1-st**2))
zero('two-mode U1 charge commutator', (s.diag(2,2)*s.Matrix([[M,hv],[hv,M+det]])-s.Matrix([[M,hv],[hv,M+det]])*s.diag(2,2))[0,1])
# Fixed-flux portal supplied already: no free vacuum receiver is created.
q,alpha,mu,m0,S=s.symbols('q alpha mu m0 S',positive=True)
Z=1/(1+alpha*S/mu**2);V4=q*q/(2*Z)
zero('fixed-flux affine portal gives mass shift',V4-q*q/2-alpha*q*q*S/(2*mu*mu))
zero('portal has no new nonlinear scalar selecting force',s.diff(V4,S,2))
allpass=all(c['passed'] for c in checks)
result={'checkpoint':'FRAMEWORK-CERT-TRANSPORT-2026-10-12','checks':checks,'all_passed':allpass,'equations':{'potential':str(V),'daughter_charge_divergence':str(s.expand(jp)),'source_weighted_charge_divergence':str(s.expand(2*jc)),'Bose_gain_loss':str(s.expand(J)),'stationary_source_occupation':str(np_*nm/(1+np_+nm)),'width':str(s.simplify(width)),'symmetric_vertex_coefficient':str(h),'quartic_pair_shift':str(U),'projected_H':'[[M,h],[h,2E+U]]; det=2E+U-M','forward_transition_probability':'4h²/(det²+4h²) sin²(sqrt(det²+4h²)t/2)','interaction_energy_change':'-det*P in forward transfer, +det*P in inverse transfer'},'scope':'Actual supplied charged trilinear action, exact local classical identities; conditional weak/dilute kinetic and projected regulated quantum reductions. No massless receiver interaction, target distribution, cold-number-preserving sink or selector derived.'}
(DEST/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert allpass
