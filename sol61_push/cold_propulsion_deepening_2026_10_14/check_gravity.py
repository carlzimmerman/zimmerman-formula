import json
import sys
from pathlib import Path
import sympy as s

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(name,expr):
    value=s.simplify(expr)
    assert value==0,(name,value)
    checks.append(name)

# Independent EH quadratic bulk action, from the linear connection.
t,z=s.symbols('t z',real=True);xx,yy=s.symbols('x y');coords=(t,xx,yy,z)
aa=s.Function('alpha')(t,z);nn=s.Function('N')(t,z)
zz=s.Function('zeta')(t,z);ee=s.Function('e')(t,z)
pert=s.Matrix([[-2*aa,0,0,nn],[0,2*zz,0,0],[0,0,2*zz,0],[nn,0,0,2*(zz+ee)]])
eta=s.diag(-1,1,1,1)
Ga=[[[sum(eta[a,d]*(s.diff(pert[d,c],coords[b])+s.diff(pert[d,b],coords[c])-s.diff(pert[b,c],coords[d])) for d in range(4))/2 for c in range(4)] for b in range(4)] for a in range(4)]
LEH=s.expand(sum(eta[mu,nu]*sum(Ga[a][mu][bb]*Ga[bb][nu][a]-Ga[a][mu][nu]*Ga[bb][a][bb] for a in range(4) for bb in range(4)) for mu in range(4) for nu in range(4))/2)
LADM=-3*s.diff(zz,t)**2-2*s.diff(zz,t)*s.diff(ee,t)+2*s.diff(zz,t)*s.diff(nn,z)+s.diff(zz,z)**2+2*s.diff(aa,z)*s.diff(zz,z)
diff=s.expand(LEH-LADM)
for f in (aa,nn,zz,ee):
    EL=s.diff(diff,f)-s.diff(s.diff(diff,s.diff(f,t)),t)-s.diff(s.diff(diff,s.diff(f,z)),z)
    zero('independent EH scalar Euler derivative '+str(f),EL)

q,r,Kc,L,mu=s.symbols('q r Kc L mu',positive=True)
Z,E,zd,ed,al,b=s.symbols('Z E zd ed alpha b',real=True)
lag=-3*zd*zd-2*zd*ed+2*zd*b+q*Z*Z+2*q*al*Z-r*(3*zd+ed-b)**2/2+r*Kc*al*al/2+r*L*b*b/(2*q)-r*mu*(3*Z*Z+2*Z*E+E*E)
asol=s.solve(s.diff(lag,al),al)[0];bsol=s.solve(s.diff(lag,b),b)[0]
red=s.factor(lag.subs({al:asol,b:bsol}))
zero('lapse constraint',s.diff(lag,al).subs(al,asol))
zero('shift constraint',s.diff(lag,b).subs(b,bsol))
K=s.hessian(red,(zd,ed)).applyfunc(s.factor)
G=(-s.hessian(red,(Z,E))).applyfunc(s.factor)
Kt=s.Matrix([[((4/r+6)*q+(6+9*r)*L)/(q-L),(2+3*r)*L/(q-L)],[(2+3*r)*L/(q-L),r*L/(q-L)]])
Gt=s.Matrix([[-2*q+4*q*q/(r*Kc)+6*r*mu,2*r*mu],[2*r*mu,2*r*mu]])
for i in range(2):
    for j in range(i,2):
        zero('reduced scalar K '+str((i,j)),K[i,j]-Kt[i,j])
        zero('reduced scalar G '+str((i,j)),G[i,j]-Gt[i,j])
detK=s.factor(K.det());detG=s.factor(G.det())
zero('scalar kinetic determinant',detK-L*(4+6*r)/(q-L))
criterion=2*q*q/(r*Kc)-q+2*r*mu
zero('scalar potential determinant',detG-4*r*mu*criterion)

# Independent transverse vector shift elimination, same unitary-gauge action.
vd,shift,V=s.symbols('vd shift V',real=True)
lv=(vd-shift)**2/4+r*L*shift**2/(2*q)-r*mu*V**2/2
vs=s.solve(s.diff(lv,shift),shift)[0];lvr=s.factor(lv.subs(shift,vs))
kv=s.factor(s.diff(lvr,vd,2));gv=s.factor(-s.diff(lvr,V,2))
zero('vector kinetic',kv-r*L/(q+2*r*L))
zero('vector frequency',gv/kv-(mu*q/L+2*r*mu))
# One transverse-traceless off-diagonal amplitude has EH kinetic1/4.
ht,hd=s.symbols('ht hd',real=True)
lt=hd*hd/4-q*ht*ht/4-r*mu*ht*ht/2
zero('tensor frequency',-s.diff(lt,ht,2)/s.diff(lt,hd,2)-(q+2*r*mu))

sq=s.symbols('omega2',real=True)
poly=s.Poly(s.factor((sq*K-G).det()),sq)
acoef=poly.coeff_monomial(sq**2);bcoef=-poly.coeff_monomial(sq);ccoef=poly.coeff_monomial(1)
zero('frequency polynomial leading coefficient',acoef-detK)
zero('frequency polynomial constant',ccoef-detG)
zero('full frozen scalar sum recovered as gravity decouples',s.limit(bcoef/acoef,r,0)-(q*q/Kc+2*mu*q/L))
zero('full frozen scalar product recovered as gravity decouples',s.limit(ccoef/acoef,r,0)-2*mu*q*q*(q-L)/(Kc*L))
# Exact roots of the potential criterion as r-boundaries at fixed q.
rminus=q*(1-s.sqrt(1-16*mu/Kc))/(4*mu)
rplus=q*(1+s.sqrt(1-16*mu/Kc))/(4*mu)
for label,rr in [('small',rminus),('large',rplus)]:zero('potential r root '+label,criterion.subs(r,rr))

pars={Kc:s.Integer(10)**12,L:s.Integer(100),mu:s.Integer(2)}
rows=[]
for rr in (s.Rational(1,10**14),s.Rational(1,10**10),s.Rational(1,10**6),s.Integer(1),s.Integer(10)**5):
    for qq in (1,50,99,103,1000,100000):
        pp={**pars,r:rr,q:s.Integer(qq)}
        kd=detK.subs(pp);pot=criterion.subs(pp)
        ghost=kd<0
        if qq<100:
            assert ghost
        else:
            assert K[0,0].subs(pp)>0 and K[1,1].subs(pp)>0 and kd>0
        checks.append('exact scalar classification '+str((rr,qq)))
        rows.append({'r':str(rr),'q':qq,'negative_scalar_kinetic_mode':bool(ghost),'positive_scalar_potential':bool(pot>0),'healthy_quadratic_exterior_modes':bool(not ghost and pot>0)})

# Stable display points: use50digit exact-polynomial evaluation and analytic
# derivative of its roots rather than ill-conditioned binary64 K inversion.
freqrows=[]
for rr in (s.Rational(1,10**14),s.Integer(10)**5):
    for qq in (103,1000,100000):
        pp={**pars,r:rr,q:s.Integer(qq)}
        A=s.N(acoef.subs(pp),50);B=s.N(bcoef.subs(pp),50);C=s.N(ccoef.subs(pp),50)
        dis=s.sqrt(B*B-4*A*C)
        big=(B+dis)/(2*A);small=C/(A*big)
        assert big>0 and small>0
        speeds=[]
        for val in (small,big):
            dp=s.N((s.diff(acoef,q)*sq*sq-s.diff(bcoef,q)*sq+s.diff(ccoef,q)).subs(pp).subs(sq,val),50)
            ds=-dp/(2*A*val-B)
            speed=s.N(s.sqrt(qq)*ds/s.sqrt(val),30)
            speeds.append(float(speed))
            residue=s.N(A*val*val-B*val+C,35)
            assert abs(residue)<s.Float('1e-20')*max(1,abs(C))
        checks.append('stable exterior scalar frequencies '+str((rr,qq)))
        freqrows.append({'r':str(rr),'q':qq,'scalar_omega2_D':[str(s.N(small,18)),str(s.N(big,18))],'scalar_group_speeds_c':speeds})

weak=s.N(rminus.subs({**pars,q:103}),25)
strong=s.N(rplus.subs({**pars,q:100000}),25)
result={'claim':'CPD-G001','checks_passed':len(checks),'K':str(K),'G':str(G),'detK':str(detK),'detG':str(detG),'weak_r_upper_whole_prior_band':str(weak),'strong_r_lower_whole_prior_band':str(strong),'tensor_omega2_D':str(q+2*r*mu),'vector_omega2_D':str(mu*q/L+2*r*mu),'classifications':rows,'stable_scalar_examples':freqrows,'verdict':'Original unconfined constant-h prototype has a reduced negative-kinetic scalar for every0<q<L. The prior frozen matter band does not establish full physical stability. Exterior finite-band healthy regions exist but do not remove the IR mode.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
