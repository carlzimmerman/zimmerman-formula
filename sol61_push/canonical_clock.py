import argparse
import json
import sympy as s

checks=[]
def check(name,condition): checks.append({'name':name,'passed':bool(condition)})
lam,eta,kappa,ms,k=s.symbols('lambda eta kappa Mstar k',positive=True)
zd,shift,z,n=s.symbols('zeta_dot laplacian_shift zeta lapse',real=True)
kin=3*(1-3*lam)*zd**2+2*(3*lam-1)*zd*shift+(1-lam)*shift**2
shift_solution=s.solve(s.diff(kin,shift),shift)[0]
reduced_kin=s.factor(kin.subs(shift,shift_solution))
ak=2*(3*lam-1)/(lam-1)
check('shift reduction',s.simplify(reduced_kin-ak*zd**2)==0)
spatial=k*k*(2*z*z+4*n*z+eta*n*n)-16*kappa*k**4*z*z/ms**2
n_solution=s.solve(s.diff(spatial,n),n)[0]
reduced_spatial=s.factor(spatial.subs(n,n_solution))
check('lapse reduction',s.simplify(reduced_spatial-((2-4/eta)*k*k-16*kappa*k**4/ms**2)*z*z)==0)
check('critical second-gradient cancellation',s.simplify(reduced_spatial.subs({eta:2,kappa:0}))==0)
omega2=s.simplify(-reduced_spatial/(ak*z*z))
check('critical fourth-gradient dispersion',s.simplify(omega2.subs(eta,2)-8*kappa*(lam-1)/(3*lam-1)*k**4/ms**2)==0)

M2,G,A,B,Z,q,P,ac,Kc=s.symbols('M2 G A B Z q P acceleration Kcoupling',positive=True)
lp=2*M2*(P*ac-P*P/2)-Kc*q*P**3
check('polarization stationarity',s.simplify(s.diff(lp,P)-(2*M2*(ac-P)-3*Kc*q*P**2))==0)
check('critical lapse coefficient from quadratic auxiliary field',s.simplify(lp.subs({Kc:0,P:ac})-M2*ac**2)==0)
U=A/q**2+B*q*q
q0=(A/B)**s.Rational(1,4)
U0=2*s.sqrt(A*B)
check('canonical density vacuum equation',s.simplify(s.diff(U,q).subs(q,q0))==0)
check('positive canonical density mass',s.simplify(s.diff(U,q,2).subs(q,q0)/Z-8*B/Z)==0)
N,a,ad=s.symbols('N a a_dot',positive=True)
background=-s.Rational(3,2)*M2*(3*lam-1)*a*ad**2/N-N*a**3*U0
constraint=s.diff(background,N).subs(N,1)
H2=s.solve(constraint,ad**2)[0]/a**2
check('background lapse constraint',s.simplify(H2-2*U0/(3*M2*(3*lam-1)))==0)
check('background scale factor equation same constraint',s.simplify((s.diff(s.diff(background,ad),a)*ad+s.diff(s.diff(background,ad),ad)*(ad**2/a)-s.diff(background,a)).subs(N,1).subs(ad**2,a**2*H2))==0)
Lambda=s.simplify(3*H2.subs(M2,1/(8*s.pi*G)))
check('geometric de Sitter Lambda',s.simplify(Lambda-16*s.pi*G*U0/(3*lam-1))==0)
a0bare=1/(12*s.pi*G*Kc*q0)
D=s.symbols('D',positive=True)
D3=(12*s.pi*G)**3*2*A*Kc*Kc
Cbare=s.simplify(Lambda/a0bare**2)
check('corrected bare coefficient bridge',s.simplify(Cbare-4*D3/(3*(3*lam-1)))==0)
check('Newton calibrated bridge',s.simplify((4*D**3/(3*(3*lam-1)))/(D/(1+D))**2-4*D*(1+D)**2/(3*(3*lam-1)))==0)

u,amp,a0,d=s.symbols('inverse_radius amplitude a0 correction',positive=True)
field=amp*u+d*u*u
def dr(expr): return -u*u*s.diff(expr,u)
lap_phi=dr(field)+2*u*field
current=(field**2/a0-8*kappa/ms**2*dr(lap_phi))/u**2
linear_coefficient=s.expand(current).coeff(u,1)
check('far-tail correction cancels first inverse-radius current',s.simplify(linear_coefficient.subs(d,-8*kappa*a0/ms**2))==0)

rows=[]
for lv in (1.1,2.,5.):
    for cv in (0.1,1.):
        values=[]
        for kv in (0.01,0.1):
            w2=float(omega2.subs({lam:lv,kappa:cv,ms:1,k:kv,eta:2}))
            values.append(w2)
        check('positive sampled principal dispersion '+str((lv,cv)),all(w>0 for w in values))
        rows.append({'lambda':lv,'kappa':cv,'k':[0.01,0.1],'omega_squared':values})
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
result={'passed':all(c['passed'] for c in checks),'checks':checks,'principal_dispersion_samples':rows}
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
raise SystemExit(0 if result['passed'] else 1)
