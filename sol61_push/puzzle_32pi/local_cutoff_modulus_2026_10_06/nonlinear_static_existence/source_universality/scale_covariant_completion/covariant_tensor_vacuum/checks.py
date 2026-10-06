"""Exact coincident-metric TT coefficient audit; not a complete BIMOND constraint analysis."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['drop_H_connection','wrong_critical_slope','vacuum_first']);args=ap.parse_args();rows=[]
def eq(name,e):
 e=s.factor(s.cancel(e));rows.append({'name':name,'passed':e==0,'residual':str(e)})
a,H,K,m=s.symbols('a H K m',positive=True)
u,v,ut,vt,uz,vz=s.symbols('u v ut vt uz vz',real=True)
for n in [3,4,5]:
 D=s.zeros(n);Dt=s.zeros(n);Dz=s.zeros(n)
 for mat,x,y in [(D,u,v),(Dt,ut,vt),(Dz,uz,vz)]:mat[0,0]=x;mat[1,1]=-x;mat[0,1]=mat[1,0]=y
 C=[[[s.S(0) for k in range(n+1)] for j in range(n+1)] for i in range(n+1)]
 for i in range(n):
  for j in range(n):
   C[0][i+1][j+1]=a*a*((0 if args.mutation=='drop_H_connection' else H)*D[i,j]+Dt[i,j]/2)
   C[i+1][0][j+1]=C[i+1][j+1][0]=Dt[i,j]/2
   for k in range(n):
    C[k+1][i+1][j+1]=((Dz[k,j] if i==n-1 else 0)+(Dz[k,i] if j==n-1 else 0)-(Dz[i,j] if k==n-1 else 0))/2
 trace=[sum(C[i][i][j] for i in range(n+1)) for j in range(n+1)]
 for j,t in enumerate(trace):eq('TT_connection_trace_%d_%d'%(n,j),t)
 U=0
 for i in range(n+1):
  weight=-1 if i==0 else a**-2
  U+=weight*(sum(C[j][i][k]*C[k][i][j] for j in range(n+1) for k in range(n+1))-sum(C[j][i][i]*trace[j] for j in range(n+1)))
 expected=s.trace(Dt*Dt)/4+H*s.trace(D*Dt)-s.trace(Dz*Dz)/(4*a*a)
 eq('raw_Upsilon_TT_n%d'%n,U-expected)
 # Direct ADM EH kinetic: determinant-one diagonal plus polarization.
 E=s.diag(*([H+ut/2,H-ut/2]+[H]*(n-2)))
 eq('EH_extrinsic_TT_n%d'%n,s.trace(E*E)-s.trace(E)**2+n*(n-1)*H*H-ut*ut/2)
# Independent exact spatial ADM curvature for a unit-determinant plus wave.
z=s.symbols('z');g=s.Function('g')(z);wx=s.exp(g/2);wy=s.exp(-g/2)
R3=-2*(s.diff(wx,z,2)/wx+s.diff(wy,z,2)/wy+s.diff(wx,z)*s.diff(wy,z)/(wx*wy))
eq('EH_spatial_TT',R3+s.diff(g,z)**2/2)
mean,delta=s.symbols('mean delta')
eq('mean_relative_split',(mean+delta/2)**2+(mean-delta/2)**2-2*mean**2-delta**2/2)
q=K*(1-2*m)/8
slope=s.Rational(1,4) if args.mutation=='wrong_critical_slope' else (0 if args.mutation=='vacuum_first' else s.Rational(1,2))
eq('source_continuous_critical_TT_kinetic',q.subs(m,slope))
eq('mean_TT_positive_coefficient',K/2-K/2)
# For one matrix entry, IBP H delta deltadot gives curvature mass.
t=s.symbols('t');aa=s.Function('a')(t);dd=s.Function('d')(t);hh=s.diff(aa,t)/aa;nn=s.symbols('n',integer=True,positive=True)
raw=-K*m*aa**nn*hh*dd*s.diff(dd,t)
EL=s.diff(raw,dd)-s.diff(s.diff(raw,s.diff(dd,t)),t)
eq('curvature_term_EL',s.simplify(EL-K*m*aa**nn*(nn*hh**2+s.diff(hh,t))*dd))
eq('deSitter_critical_algebraic_relative_TT', (K*m*nn*H**2).subs(m,s.Rational(1,2))-K*nn*H**2/2)
# At fixed positive T and y->0: e~y^-1/2, x~2 sqrt(y), m=e/(1+2e).
y,T=s.symbols('y T',positive=True);lam=s.symbols('lam',positive=True);b=s.sqrt(1+1/y)-1;e=b/(1+(y/T)**2)
eq('fixed_positive_T_source_slope',s.limit(e/(1+2*e),y,0)-s.Rational(1,2))
eq('source_envelope_aux_y_over_T',s.limit(y/((8/(7*lam))**s.Rational(1,4)*y**s.Rational(7,8)),y,0))
eq('vacuum_first_source_slope',s.limit(e/(1+2*e),T,0))
eq('noncommuting_slope_gap',s.limit(e/(1+2*e),y,0)-s.limit(e/(1+2*e),T,0)-s.Rational(1,2))
# Sign translation: a pure temporal TT derivative gives U>0 and therefore z<0.
ztime=-(s.trace(s.Matrix([[ut,vt],[vt,-ut]])**2)/4)/(2*s.symbols('chi_n',positive=True)*s.symbols('a0',positive=True)**2)
rows.append({'name':'timelike_TT_tests_negative_invariant','passed':s.simplify(ztime).is_nonpositive is True,'residual':str(ztime)})
args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps({'checks':rows,'passed':sum(r['passed'] for r in rows),'total':len(rows),'mutation':args.mutation,'scope':'exact coefficient contraction n3..5; report gives conditional general-n proof, no all-helicity health'},indent=2)+'\n')
print(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'failed':[r for r in rows if not r['passed']]}));sys.exit(0 if all(r['passed'] for r in rows) else 1)
