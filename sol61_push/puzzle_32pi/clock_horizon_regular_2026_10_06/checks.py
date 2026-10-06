import argparse,json
from pathlib import Path
import sympy as s
import mpmath as mp
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--insert-horizon-factor',action='store_true');p.add_argument('--drop-response-rank',action='store_true');args=p.parse_args()
r,M,A,H,c=s.symbols('r M A H c',positive=True);n=s.symbols('n',integer=True,positive=True);kap=s.symbols('kap',real=True)
N,B,V=[s.Function(x)(r) for x in ['N','B','V']];d=lambda x:s.diff(x,r);g=d(N)/(N*B);lam=(n-1)/(2*(n-2));C=M*(n-1)/2;b=2*c/(n*H)
Q=kap*g*g-2*g**3/(3*A)
L=C*((n-2)*N*r**(n-3)*(B+1/B)+2*d(N)*r**(n-2)/B-r**(n-2)*V**2*(d(B)/N+B*d(N)/N**2))+N*B*r**(n-1)*(2*c*s.log(N)-n*(n-1)*M*H**2/2+M*lam*Q)-b*B*r**(n-1)*V*d(N)/N
el=lambda z:s.diff(L,z)-d(s.diff(L,d(z)))
E=[s.simplify(el(z)) for z in [V,B,N]];unknowns=[d(B),d(V),s.diff(N,r,2)]
matrix=s.Matrix([[s.simplify(s.diff(e,u)) for u in unknowns] for e in E]);qgg=2*kap-4*g/A
det=s.factor(matrix.det());want=M**3*(n-1)**2*lam*r**(3*n-5)*V**2*qgg/(N**3*B)
checks=[]
def ck(name,ok):checks.append({'name':name,'passed':bool(ok)})
ck('shift_is_first_triangular_row',matrix[0,1]==0 and matrix[0,2]==0)
ck('radial_has_no_lapse_second_derivative',matrix[1,2]==0)
ck('shift_derivative_coefficient',s.simplify(matrix[0,0]+M*(n-1)*r**(n-2)*V/N)==0)
ck('radial_shift_derivative_coefficient',s.simplify(matrix[1,1]-M*(n-1)*r**(n-2)*V/N)==0)
ck('response_lapse_rank',s.simplify(matrix[2,2]-(-M*lam*r**(n-1)*qgg/(N*B) if not args.drop_response_rank else 0))==0)
ck('general_dimension_determinant',s.simplify(det-want)==0)
hdet=M**3*(n-1)**2*lam*r**(3*n-5)*qgg/(N*B**3)
claimed=want*(N*N-B*B*V*V) if args.insert_horizon_factor else want
ck('horizon_determinant_nonzero_formula',s.simplify(claimed.subs(V,-N/B)-hdet)==0)
mp.mp.dps=50;rows=[]
for aval in ['.25','.5','1','2','4']:
 aa=mp.mpf(aval);P=aa/100;kk=mp.mpf('.99');ss=mp.sqrt(P*P+aa*aa/4);wa=ss-aa/2
 W=(P*ss+aa*aa/4*mp.asinh(2*P/aa))/2-aa*P/2
 q=kk*P*P-2*W;qp=2*(kk*P-wa);qpp=2*(kk-P/ss);J=q-P*qp
 bp=-P/2;vp=-1-3*P/2+J/2;fp=2*P-2*bp+2*vp
 # Original four-dimensional shift and radial EL at N=B=M=H=r=1,V=-1,c=1.5.
 ev=-2*(-1)*(bp+P)-P
 eb=1-(1+2*P)+(1-2*vp)-2*P+(-3+q-P*qp)+P
 ck('actual_P2_shift_'+aval,abs(ev)<mp.mpf('1e-45'))
 ck('actual_P2_radial_'+aval,abs(eb)<mp.mpf('1e-45'))
 ck('simple_horizon_'+aval,fp< -2 and qpp>0)
 rows.append({'A':aval,'P':str(P),'Qgg':str(qpp),'Fprime':str(fp),'surface_gravity':str(abs(fp)/2)})
out={'checks':checks,'summary':{'passed':sum(x['passed'] for x in checks),'total':len(checks)},'symbolic_determinant':str(det),'actual_P2_horizon_family':rows,'scope':'Local vacuum crossing; no global source/cosmology matching or full kinetic health'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']));raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
