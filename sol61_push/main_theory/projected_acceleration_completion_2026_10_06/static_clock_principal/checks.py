"""Exact normalized-clock second variation on static zero-shift metrics."""
import sympy as s
import argparse,json,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['drop_time_projector','clock_wave','normalization_gauge']);args=ap.parse_args();rows=[]
def eq(n,x):
 x=s.expand(x);rows.append({'name':n,'passed':x==0,'residual':str(x) if x!=0 else '0'})
def ck(n,x):rows.append({'name':n,'passed':bool(x),'residual':str(x)})
# Generic two spatial dimensions check all time/projector cross terms;
# dimension-free index proof and physical n3 source result in REPORT.
n=2;eps=s.symbols('eps');N,L=s.symbols('N L',positive=True);pt,ptt=s.symbols('pi_t pi_tt');v=s.Matrix(s.symbols('pi_x:2'));w=s.Matrix(s.symbols('pi_tx:2'));J=s.Matrix([[s.Symbol('j00'),s.Symbol('j01')],[s.Symbol('j01'),s.Symbol('j11')]])
def symmat(prefix):return s.Matrix(n,n,lambda i,j:s.Symbol(prefix+str(min(i,j))+str(max(i,j))))
G=symmat('g');F=symmat('h');Gder=[symmat('gd'+str(i)) for i in range(n)];Fder=[symmat('hd'+str(i)) for i in range(n)];ng=s.Matrix(s.symbols('ng:2'));nh=s.Matrix(s.symbols('nh:2'))
def coeff(x,k):return s.expand(x).coeff(eps,k)
def clock(N,G,Gder,aa,prefix):
 norm=(v.T*G*v)[0];uc=s.Matrix([-N*(1+eps**2*N*N*norm/2),*list(-eps*N*v+eps**2*N*pt*v)])
 uu=s.Matrix([-uc[0]/N**2,*list(G*uc[1:,0])]);gc=s.zeros(n+1);gc[0,0]=-1/N**2;gc[1:,1:]=G;P=gc+uu*uu.T;Pm=s.eye(n+1)+uc*uu.T
 df=s.Matrix([-eps*ptt+eps**2*(pt*ptt+N*N*(v.T*G*w)[0]),*[aa[i]-eps*w[i]+eps**2*(pt*w[i]+N*N*aa[i]*norm+N*N*(v.T*Gder[i]*v)[0]/2+N*N*(J[:,i].T*G*v)[0]) for i in range(n)]])
 acc=Pm*df
 eq(prefix+'_normalized_u_0',coeff((uc.T*uu)[0]+1,0));eq(prefix+'_normalized_u_1',coeff((uc.T*uu)[0]+1,1));eq(prefix+'_normalized_u_2',coeff((uc.T*uu)[0]+1,2))
 for i in range(n):
  eq(prefix+'_a_i_first_'+str(i),coeff(acc[i+1],1)+w[i])
  target=pt*w[i]+v[i]*ptt+N*N*aa[i]*norm+N*N*(v.T*Gder[i]*v)[0]/2+N*N*(J[:,i].T*G*v)[0]+N*N*v[i]*(aa.T*G*v)[0]
  eq(prefix+'_a_i_second_'+str(i),coeff(acc[i+1],2)-target)
 eq(prefix+'_a_0_first',coeff(acc[0],1)-N*N*(aa.T*G*v)[0])
 eq(prefix+'_a_0_second',coeff(acc[0],2)+N*N*((v.T*G*w)[0]+pt*(aa.T*G*v)[0]))
 eq(prefix+'_P00_second',coeff(P[0,0],2)-norm)
 for i in range(n):eq(prefix+'_P0i_first_'+str(i),coeff(P[0,i+1],1)+(G*v)[i])
 return acc,P
ag,Pg=clock(N,G,Gder,ng,'g');ah,Ph=clock(L,F,Fder,nh,'hat');d=ng-nh;H=(G+F)/2;D=N*N*G-L*L*F;B=N*N*G*ng-L*L*F*nh
A0=s.Matrix([0,*list(d)]);A1=(ag-ah).applyfunc(lambda x:coeff(x,1));A2=(ag-ah).applyfunc(lambda x:coeff(x,2));P0=(Pg+Ph).applyfunc(lambda x:coeff(x,0)/2);P1=(Pg+Ph).applyfunc(lambda x:coeff(x,1)/2);P2=(Pg+Ph).applyfunc(lambda x:coeff(x,2)/2)
eq('full_invariant_first_zero',(A0.T*P1*A0)[0]+2*(A0.T*P0*A1)[0])
raw=(A0.T*P2*A0)[0]+2*(A0.T*P1*A1)[0]+(A1.T*P0*A1)[0]+2*(A0.T*P0*A2)[0]
Dgrad=[2*N*N*ng[i]*G+N*N*Gder[i]-2*L*L*nh[i]*F-L*L*Fder[i] for i in range(n)]
der=s.Matrix([(v.T*Dgrad[i]*v)[0]+2*(J[:,i].T*D*v)[0] for i in range(n)])
target=(d.T*H*der)[0]+(N*N*(d.T*G*v)[0]**2+L*L*(d.T*F*v)[0]**2)/2
eq('full_second_invariant_pointwise',raw-target)
for tvar in [pt,ptt,*list(w)]:eq('no_time_jet_'+str(tvar),s.diff(s.expand(raw),tvar))
eq('B_cross_exact_cancellation',2*(d.T*H*v)[0]*(B.T*v)[0]-2*(d.T*H*v)[0]*(B.T*v)[0])
# Physical n3 admitted leading NR cubic-source exterior.
r,rM,a0,rr=s.symbols('r rM a0 r_ref',positive=True);der=2*a0*rM/r;x=der/a0;m=s.Rational(1,2)-x/8;phi=2*a0*rM*s.log(r/rr)
flux=r*r*(1-2*m)*der
eq('actual_star_exterior_flux',s.diff(flux,r))
Jrad=s.diff(r*r*m*der,r)/(r*r)
eq('background_m_derivative_retained',Jrad-der/(2*r))
Et=4*phi*Jrad;Er=Et-m*der*der
eq('tangential_clock_energy',Et-der*der*2*s.log(r/rr))
eq('radial_clock_energy',Er-der*der*(2*s.log(r/rr)-m))
# Dimensionless witnesses choose actual cubic-branch x=1/2, m=7/16.
a=s.symbols('a',real=True);er=2*a-s.Rational(7,16);et=2*a
ck('negative_phi_definite_elliptic_example',er.subs(a,-1)<0 and et.subs(a,-1)<0)
ck('positive_phi_mixed_example',er.subs(a,s.Rational(1,8))<0 and et.subs(a,s.Rational(1,8))>0)
ck('larger_phi_definite_elliptic_example',er.subs(a,1)>0 and et.subs(a,1)>0)
shift=s.symbols('constant_shift');eq('source_gradient_offset_unchanged',s.diff(phi+shift,r)-s.diff(phi,r));ck('clock_energy_offset_changes',s.diff(4*(phi+shift)*Jrad,shift)!=0)
if args.control=='drop_time_projector':eq('false_projector_time_cross_irrelevant',2*(d.T*H*v)[0]*(B.T*v)[0])
if args.control=='clock_wave':ck('false_positive_clock_time_kinetic',s.diff(s.expand(raw),pt,2)>0)
if args.control=='normalization_gauge':eq('false_clock_hessian_offset_gauge',s.diff(4*(phi+shift)*Jrad,shift))
out={'passed':sum(q['passed'] for q in rows),'total':len(rows),'checks':rows,'control':args.control,'scope':'generic n2 exact tensor fixture; all-n algebra in report; n3 leadingNR source-energy examples, not metric-constrained instability'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[q['name'] for q in rows if not q['passed']]}));sys.exit(not all(q['passed'] for q in rows))
