import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json,math,time,resource
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.linalg import eigh,null_space
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from pressure_scan import cw
from gaugino_threshold import build_model,ext_basis,threshold,summarize
mp.mp.dps=100
Z=mp.mpf('7.3671437212785083116194');MP=mp.mpf('2.435e18');E=mp.mpf('.003');DE=mp.mpf('2.52e-47');T=mp.mpf('1.160043920237347');S=mp.log(T)
DATA=json.load(open(HERE/'run_coefficients/result.json'));DOMAIN=list(map(mp.mpf,map(str,DATA['domain'])))
F0=1/mp.sqrt(31);A0=mp.sqrt(2/(31*E));X0=Z/mp.sqrt(31*E)

def cf(k,s,n):
 co=list(map(lambda x:mp.mpf(str(x)),DATA['fits'][str(n)][k]));x=(2*s-sum(DOMAIN))/(DOMAIN[1]-DOMAIN[0]);v0=mp.mpf(1);v1=x;ans=co[0]+co[1]*x
 for a in co[2:]:v0,v1=v1,2*x*v1-v0;ans+=a*v1
 return ans*(E/mp.mpf(str(DATA['e0'])))**mp.mpf(str(DATA['powers'][k]))

def one(s):return cw(X0*mp.exp(s),E,E,mp.sqrt(mp.mpf(29)/200)*E)

def sg(s,u,v,p,y,theta=mp.mpf(0),c=mp.mpf(0),d=mp.mpf(0),parts=False):
 x=X0*mp.exp(s);a=A0+u+1j*c;b=x+v+1j*d;et=mp.exp(1j*theta);wraw=et*(x-15*E*x*a*a+15*E*a*a*b);w=p*y+wraw;k=x*x+30*abs(a)**2+30*abs(b)**2
 dx=1-15*E*a*a+x/et*w/p**2;da=1j*a*et*E*(x-b)-1j*a.conjugate()*w/p**2;db=E*a*a/2+b.conjugate()/et*w/p**2;fn=abs(dx)**2+30*abs(da)**2+30*abs(db)**2
 val=mp.exp(k/p**2)*(fn-3*abs(w)**2/p**2)
 return (mp.re(val),k,w,fn) if parts else mp.re(val)

def potential(s,u,v,p,y,n):return sg(s,u,v,p,y)+one(s)+cf('ja',s,n)*u+cf('jb',s,n)*v+cf('U2diag',s,n)

def normals(s,p,y,n,guess=None):
 x=X0*mp.exp(s)
 if guess is None:guess=(-cf('ja',s,n)/(120*E),-cf('jb',s,n)/(120*E/31))
 return mp.findroot(lambda u,v:(mp.diff(lambda z:sg(s,z,v,p,y),u)+cf('ja',s,n),mp.diff(lambda z:sg(s,u,z,p,y),v)+cf('jb',s,n)),guess,tol=mp.mpf('1e-90'),maxsteps=30)

def phase(s,u,v,p,y):
 f=lambda th,c,d:sg(s,u,v,p,y,th,c,d)
 B=mp.diff(lambda t:f(t,0,0),mp.mpf(0),2)
 H=mp.matrix([[mp.diff(lambda c: f(0,c,0),0,2),mp.diff(lambda c:mp.diff(lambda d:f(0,c,d),0),0)],[0,mp.diff(lambda d:f(0,0,d),0,2)]]);H[1,0]=H[0,1]
 C=mp.matrix([mp.diff(lambda t:mp.diff(lambda c:f(t,c,0),0),0),mp.diff(lambda t:mp.diff(lambda d:f(t,0,d),0),0)])
 z=-mp.lu_solve(H,C);Bred=B+(C.T*z)[0];x=X0*mp.exp(s);b=x+v
 Ft=x*x+30*z[0]**2+30*(b+z[1])**2
 return Bred,Ft,z

def stencil(f,s,h):
 z=[f(s+j*h) for j in (-2,-1,0,1,2)]
 return z[2],(z[0]-8*z[1]+8*z[3]-z[4])/(12*h),(-z[0]+16*z[1]-30*z[2]+16*z[3]-z[4])/(12*h*h)

def gauginos(s):
 x=float(X0*mp.exp(s));e=float(E);g=math.sqrt(29/200)*e;data=build_model(x,e,e,g,vertices=False);ext,labels=ext_basis(data);out,_=summarize(threshold(data,ext),labels)
 return {k:mp.mpf(str(v['signed_mass'])) for k,v in out.items()}

def solve(n):
 leading=31*mp.sqrt(3)*MP*E**mp.mpf('2.5')/(4*Z)*mp.diff(lambda t:cw(X0*t,E,E,mp.sqrt(mp.mpf(29)/200)*E)/E**2,T)
 y0=F0/mp.sqrt(3);p0=MP/leading;j0=cf('ja',S,n);j1=cf('jb',S,n);x=X0*mp.exp(S)
 def eq(U,V,Y,K):
  u=U*A0;v=V*x;p=p0/K;y=y0*Y
  f=lambda ss,uu,vv:potential(ss,uu,vv,p,y,n)
  return (mp.diff(lambda uu:f(S,uu,v),u)*A0/E**2,mp.diff(lambda vv:f(S,u,vv),v)*x/E**2,(f(S,u,v)-DE/(leading*K)**4)/E**2,mp.diff(lambda ss:f(ss,u,v),S)/(E**2*mp.mpf('1e-5')))
 guess=(-j0/(120*E)/A0,-j1/(120*E/31)/x,mp.mpf(1),mp.mpf(1))
 U,V,Y,K=mp.findroot(eq,guess,tol=mp.mpf('1e-85'),maxsteps=35);u=U*A0;v=V*x;mu=leading*K;p=p0/K;y=y0*Y
 residual=eq(U,V,Y,K);tree,k,w,fn=sg(S,u,v,p,y,parts=True);mass32=mu*mp.exp(k/(2*p*p))*abs(w)/p**2;F=mu*mu*mp.exp(k/(2*p*p))*mp.sqrt(fn)
 vals={};sols={}
 def get(s):
  key=mp.nstr(s,110)
  if key not in sols:sols[key]=normals(s,p,y,n,(u,v))
  return sols[key]
 def red(s):uu,vv=get(s);return potential(s,uu,vv,p,y,n)
 def bfun(s):uu,vv=get(s);return X0*mp.exp(s)+vv
 def afun(s):uu,vv=get(s);return A0+uu
 def Bfun(s):uu,vv=get(s);return phase(s,uu,vv,p,y)[0]
 def Ffun(s):uu,vv=get(s);return phase(s,uu,vv,p,y)[1]+cf('kgraph',s,n)
 rows=[]
 for hh in ('.005','.0025'):
  h=mp.mpf(hh);_,Vr,Vrr=stencil(red,S,h);_,bs,_=stencil(bfun,S,h);_,aas,_=stencil(afun,S,h);B,Bs,_=stencil(Bfun,S,h);FF,Fs,_=stencil(Ffun,S,h)
  AA=x*x+30*bs*bs+30*aas*aas+cf('rgraph',S,n);ms2=mu*mu*Vrr/(2*AA);ma2=mu*mu*B/(2*FF);ms=mp.sqrt(ms2);ma=mp.sqrt(ma2)
  # physical on-shell sigma-aa amplitude from derivative and potential vertices
  gphys=(Fs/(2*FF)*(ms2-2*ma2)+mu*mu*Bs/(2*FF))/mp.sqrt(2*AA)/mu
  R=mu*mp.sqrt(31)*x;gam=gphys*gphys/(32*mp.pi*ms)*mp.sqrt(1-4*ma2/ms2) if ms2>4*ma2 else mp.mpf(0)
  rows.append(dict(h=float(h),m_sigma_GeV=float(ms),m_phase_GeV=float(ma),phase_pair_open=bool(ms2>4*ma2),A_over_R2=float(AA/(31*x*x)),F_over_R2=float(FF/(31*x*x)),potential_slope_dimensionless=float(Vr),potential_curvature_dimensionless=float(Vrr),phase_curvature_dimensionless=float(B),g_sigma_aa_GeV=float(gphys),Gamma_sigma_aa_GeV=float(gam),phase_over_radial=float(ma/ms),metric_A_dimensionless=float(AA),metric_F_dimensionless=float(FF),F_s_over_F=float(Fs/FF),B_s_over_B=float(Bs/B)))
 masses=gauginos(S);slopes={}
 for hh in ('.005','.0025'):
  h=mp.mpf(hh);mv=[gauginos(S+j*h) for j in (-2,-1,0,1,2)]
  slopes[hh]={key:float((mv[0][key]-8*mv[1][key]+8*mv[3][key]-mv[4][key])/(12*h*masses[key])) for key in masses}
 phase_info=phase(S,u,v,p,y)
 result=dict(nodes=n,e=float(E),t=float(T),mu_GeV=float(mu),R_GeV=float(mu*mp.sqrt(31)*x),X_GeV=float(mu*x),W0_GeV3=mp.nstr(p*y*mu**3,45),W0_over_leading=float(p*y/(p0*y0)),m32_GeV=float(mass32),F_tree_SUGRA_GeV2=float(F),W0_fractional_DE_tuning=mp.nstr(DE/(6*abs(w)*p*y*mp.exp(k/p**2)/p**2*mu**4),25),a_relative_shift=float(U),b_relative_shift=float(V),a0_dimensionless=float(A0),a_dimensionless=float(A0+u),b_dimensionless=float(x+v),p_dimensionless=mp.nstr(p,45),y_dimensionless=mp.nstr(y,45),u_dimensionless=mp.nstr(u,45),v_dimensionless=mp.nstr(v,45),root_equation_max_scaled_residual=mp.nstr(max(abs(r) for r in residual),12),physical_net_V_GeV4=mp.nstr(potential(S,u,v,p,y,n)*mu**4,35),target_net_V_GeV4=mp.nstr(DE,10),loop_CW=float(one(S)),loop_V2_diagrams=float(cf('U2diag',S,n)),CW_normal_energy=float(cf('ja',S,n)*u+cf('jb',S,n)*v),tree_V=float(tree),rows=rows,gauginos_GeV={k:float(v*mu) for k,v in masses.items()},gaugino_log_slopes=slopes,phase_normal_response=list(map(float,phase_info[2])),R_over_Mp=float(mu*mp.sqrt(31)*x/MP))
 return result

def main(path):
 start=time.monotonic();points=[]
 for n in (21,29):
  point=solve(n);points.append(point);print(json.dumps({k:point[k] for k in ('nodes','mu_GeV','R_GeV','m32_GeV','gauginos_GeV','rows')}),flush=True)
 p=points[-1];convergence={k:abs(p[k]/points[0][k]-1) for k in ('mu_GeV','R_GeV','m32_GeV')};convergence['radial_mass_last_stencil']=abs(p['rows'][-1]['m_sigma_GeV']/p['rows'][-2]['m_sigma_GeV']-1);convergence['radial_mass_nodes']=abs(p['rows'][-1]['m_sigma_GeV']/points[0]['rows'][-1]['m_sigma_GeV']-1)
 checks=dict(small_field=p['R_over_Mp']<1e-9,positive_light_masses=all(r['m_sigma_GeV']>0 and r['m_phase_GeV']>0 for pt in points for r in pt['rows']),phase_closed=all(not r['phase_pair_open'] for pt in points for r in pt['rows']),converged=max(convergence.values())<1e-6,DE_tuning=abs(mp.mpf(p['physical_net_V_GeV4'])/DE-1)<mp.mpf('1e-15'))
 out=dict(claim_id='CANONICAL_FINITE_STATIONARY_CANDIDATE',checks=checks,points=points,convergence=convergence,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Exact microscopic tree SUGRA with linear CW normal sources plus unreduced rigid two-loop diagrams; fixed Landau component metric; not a full loop super-Higgs or gravitational threshold certificate')
 Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('checks','convergence','runtime_seconds','peak_rss_bytes_macos')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
