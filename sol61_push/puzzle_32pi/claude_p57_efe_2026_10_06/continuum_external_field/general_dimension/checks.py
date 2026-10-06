"""General spatial dimension n>=3 continuum quadrupole moment bridge."""
import argparse,json,pathlib,sympy as s,mpmath as m
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--control',choices=['none','normalization','blind','wrong_index'],default='none');args=pa.parse_args();checks=[]
def ck(n,b,d=None):checks.append(dict(name=n,passed=bool(b),detail=d))
def zero(n,e):e=s.simplify(e);ck(n,e==0,str(e))
n,p,xi,t,e=s.symbols('n p xi t e',real=True);theta=s.symbols('theta',real=True)
H=n*t*(xi*xi-1/n)+e*xi*((n+2)*xi*xi-3);old=e*(3*xi-5*xi**3)+t*(1-3*xi*xi)
zero('n3_H_matches_negative_parent',H.subs(n,3)+old)
# Angular projection normalization from exact sphere moments.
Nnorm=3/(n*(n+2))-1/n**2
zero('angular_STF_norm',Nnorm-2*(n-1)/(n*n*(n+2)))
G=s.sin(theta)**(n-1)*((n+2)*s.cos(theta)**2-1)
zero('angular_integration_by_parts',(n-1)*((n+2)*s.cos(theta)**2-1)-2*(n+2)*s.sin(theta)**2-(n+1)*((n+2)*s.cos(theta)**2-3))
ratio=n*(n+1)/((n+1)**2-p*p)
zero('angular_J_recurrence_reduction',(n+1+p)/(n+1)*((n+1)-(n+2)*ratio)-(1-p*p)/(n+1-p))
# Mellin index: external integral exponent s-1 and kernel y^p yield vacuumy.
ss=s.symbols('ss');zero('required_moment_index',(ss+p).subs(ss,1-p)-1)
m.mp.dps=65
Omega=lambda j:2*m.pi**((j+1)/2)/m.gamma((j+1)/2)
def cn(n):return n*n*Omega(n-2)/((n-1)**2*Omega(n-1))
def K(n):
 p=m.mpf(1)/(n-1)
 return m.pi**2*(1-p*p)*m.gamma(n)/(2**n*(n+1-p)*m.cos(m.pi*p/2)*m.gamma((n+1+p)/2)*m.gamma((n+1-p)/2))
def Jrec(mm,p):
 if mm%2==0:out=(1-m.cos(m.pi*p))/p;start=2
 else:out=m.sin(m.pi*p)/(1-p*p);start=3
 for k in range(start,mm+1,2):out*=k*(k-1)/(k*k-p*p)
 return out
rows=[]
for nn in range(3,13):
 pp=m.mpf(1)/(nn-1)
 J=m.quad(lambda theta:m.sin(theta)**(nn-1)*m.sin(pp*theta),[0,m.pi/2,m.pi]);kr=m.pi*(1-pp*pp)/(nn+1-pp)/m.sin(m.pi*pp)*J
 ck('angular_quadrature_K_n'+str(nn),abs((kr-K(nn))/K(nn))<m.mpf('1e-55'),str(kr))
 ck('integer_J_recurrence_n'+str(nn),abs((J-Jrec(nn-1,pp))/J)<m.mpf('1e-55'))
 rows.append(dict(n=nn,p=str(pp),K=str(K(nn)),normalization=str(cn(nn)),continuum_coefficient=str(cn(nn)*K(nn))))
ck('n3_K_exact_match',abs(K(3)-8*m.pi/35)<m.mpf('1e-55'))
ck('n3_physical_coefficient',abs(cn(3)*K(3)-9*m.pi/35)<m.mpf('1e-55'))
ck('n4_rational_coefficient',abs(cn(4)*K(4)-m.mpf(18)/35)<m.mpf('1e-55'))
# Independently integrate the rho Mellin factors before performing angular reduction.
for pp,xx in [(m.mpf('.5'),m.mpf('-.7')),(m.mpf(1)/3,m.mpf('.2')),(m.mpf(1)/7,m.mpf('.8'))]:
 th=m.acos(xx)
 for a in [pp,1+pp]:
  direct=m.quad(lambda rho:rho**(a-1)/(1+rho*rho+2*xx*rho),[0,1,m.inf]);formula=m.pi*m.sin((1-a)*th)/(m.sin(m.pi*a)*m.sin(th))
  # Near-zero slow Mellin integrability entails finite quadrature accuracy at small p.
  ck('rho_Mellin_factor_p'+str(pp)+'_a'+str(a),abs((direct-formula)/formula)<m.mpf('1e-8'),str(abs((direct-formula)/formula)))
# Full generalized weight exact n3 correspondence at both sides of q1.
def Fn(nn,q):
 pp=m.mpf(1)/(nn-1);h=m.mpf(nn-3)/2
 def raw(tt):
  xx=(1-q*q-tt*tt)/(2*q*tt)
  angular=max(m.mpf(0),1-xx*xx)**h
  return tt**(pp-2)/q*(nn*tt*(xx*xx-m.mpf(1)/nn)+q*xx*((nn+2)*xx*xx-3))*angular
 return m.quad(raw,[abs(1-q),(abs(1-q)+1+q)/2,1+q])
def oldF(q):
 P=2*q**3+q*q+6*q+12;R=-2*q**3+q*q-6*q+12
 return -m.mpf(2)/(35*q**3)*(P/m.sqrt(1+q)-m.sign(1-q)*R/m.sqrt(abs(1-q)))
for q in [m.mpf('.2'),m.mpf('1.5'),m.mpf(5)]:ck('n3_full_branch_weight_'+str(q),abs(Fn(3,q)+2*oldF(q))<m.mpf('1e-55'))
# Endpoint asymptotic checks illustrate derived O estimates without proving all n numerically.
endpoints=[]
for nn in [3,4,6]:
 pp=m.mpf(1)/(nn-1);h=m.mpf(nn-3)/2
 shell=(nn-1)*(1+pp)/(2*(nn+1-pp))*m.beta(1-pp/2,(nn-1)/2)
 qq=m.mpf('1.000001');scaled=Fn(nn,qq)*(qq-1)**(1-pp)
 ck('shell_coefficient_n'+str(nn),abs(scaled-shell)/shell<m.mpf('.01'),str(scaled))
 endpoints.append(dict(n=nn,shell_coefficient=str(shell),small_q_power=2,large_q_upper_power=str(pp-nn-1),shell_power=str(pp-1)))
if args.control=='normalization':ck('CONTROL_wrong_n3_hessian_factor',abs(cn(3)*K(3)-9*m.pi/70)<m.mpf('1e-55'))
if args.control=='blind':ck('CONTROL_vacuum_blind',K(4)==0)
if args.control=='wrong_index':ck('CONTROL_use_n3_index_for_all_n',m.mpf('.5')+m.mpf(1)/3==1)
result=dict(passed=all(c['passed'] for c in checks),checks=checks,dimensions=rows,endpoint_checks=endpoints,formula='int e^(-p) Q_n(e)de=(a0/rM)c_n K_n int y f(y)dy, p=1/(n-1)',scope='Universal integer n>=3 proof is analytic; bounded computations n3..12 only',precision_digits=65,not_interval_certified=True,control=args.control,non_claims=['No physical all-e dataset','No 32pi selector','No covariant vacuum dictionary','No full-kernel inversion','No n2 extension'])
pth=pathlib.Path(args.output);pth.parent.mkdir(parents=True,exist_ok=True);pth.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[c['name'] for c in checks if not c['passed']])));raise SystemExit(0 if result['passed'] else 1)
