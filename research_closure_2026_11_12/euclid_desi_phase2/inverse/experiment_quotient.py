import pathlib,json,sys,math
import numpy as np
from scipy.optimize import least_squares
root=pathlib.Path(__file__).parent;cfg=json.loads((root/'selection_quotient.json').read_text());name=sys.argv[1];out=root/sys.argv[2];out.mkdir(exist_ok=True)
assert name in cfg['targets']
dat=np.loadtxt(root/f'inputs/{name}_rotmod.dat');dat=dat[(dat[:,0]>0)&(dat[:,1]>0)&(dat[:,2]>0)];dat=dat[np.argsort(dat[:,0])];R,V,eV,Vg,Vd,Vbul,SB=dat[:,:7].T;assert np.all(Vbul==0)
for line in (root/'inputs/SPARC_Lelli2016c.mrt').read_text().splitlines():
 t=line.split()
 if t and t[0]==name:D,inc,si,Rd=float(t[2]),float(t[5]),float(t[6]),float(t[11])
inc0=np.deg2rad(inc);sigi=np.deg2rad(si);nr=1024;nphi=256;rmax=max(R)*2;rp=(np.arange(nr)+.5)*rmax/nr;dr=rmax/nr
rr=R[SB>0];ll=np.log(SB[SB>0]);sl=(ll[-1]-ll[-2])/(rr[-1]-rr[-2]);sl=sl if sl<0 else -1/Rd
lns=np.interp(rp,rr,ll,left=ll[0],right=ll[-1]);tail=rp>rr[-1];lns[tail]=ll[-1]+sl*(rp[tail]-rr[-1]);Sigma=np.exp(lns);phi=(np.arange(nphi)+.5)*2*np.pi/nphi;co=np.cos(phi)[None,:];rpr=rp[:,None];h=.1*Rd;wt=rp*Sigma*dr*2*np.pi/nphi
H=[]
for r in R:H.append(((r-rpr*co)/(r*r+rpr*rpr-2*r*rpr*co+h*h)**1.5).sum(axis=1)*wt)
H=np.array(H);g0=H@np.ones(nr);assert np.all(g0>0)
x=np.log(rp/Rd);nodes=np.log(cfg["knots_R_over_Rd"]);anchor=int(np.flatnonzero(nodes==0)[0]);external_index=[j for j in range(len(nodes)) if j!=anchor];externalnodes=nodes[external_index];population_chol=np.linalg.cholesky(np.eye(len(external_index))+np.ones((len(external_index),len(external_index))))
L10=np.log(10);kpc=3.085677581491367e19;star=.5*Vd*Vd*1e6/(R*kpc);gas=np.sign(Vg)*Vg*Vg*1e6/(R*kpc);a0=cfg['a0']
def truthshape(x,typ):
 if typ=='bend':return L10*.08*np.tanh(x/.8)
 if typ=='bump':return L10*.10*(np.exp(-(x-np.log(2))**2/(2*.45**2))-np.exp(-np.log(2)**2/(2*.45**2)))
 return L10*.06*.25*(np.logaddexp(0,(x-.3)/.25)-np.logaddexp(0,-.3/.25))
def basis(xx,kind):
 if kind=='one_power':return np.array(xx)[:,None]
 mat=[]
 for j in external_index:
  vals=np.zeros(len(nodes));vals[j]=1;mat.append(np.interp(xx,nodes,vals))
 return np.array(mat).T
bs={k:basis(x,k) for k in cfg['inverse_shapes']};be={k:basis(externalnodes,k) for k in cfg['inverse_shapes']}

def predict(p,kind,jac=False):
 B=bs[kind];nb=B.shape[1];shape=p[3:3+nb];di=p[-1];ss=np.exp(B@shape);gs=(H@ss)/g0;Sstar=np.exp(p[0])*star*gs;Sgas=np.exp(p[1])*gas;S=Sstar+Sgas;a=a0*np.exp(p[2])
 if np.any(S<=0):raise ValueError('nonpositive sourcefield')
 g=(S+np.sqrt(S*S+4*S*a))/2;pred=np.sqrt(R*kpc*g)/1000*np.sin(inc0+di)/np.sin(inc0)
 if not jac:return pred
 tt=a/(g+2*a);ab=1-tt;J=np.empty((len(R),len(p)));J[:,0]=pred*.5*ab*Sstar/S;J[:,1]=pred*.5*ab*Sgas/S;J[:,2]=pred*.5*tt
 dgs=(H@(ss[:,None]*B))/g0[:,None]
 J[:,3:3+nb]=pred[:,None]*.5*ab[:,None]*(np.exp(p[0])*star/S)[:,None]*dgs
 J[:,-1]=pred/np.tan(inc0+di)
 return pred,J

def bounds(kind):
 nb=bs[kind].shape[1];b=.5 if kind=='one_power' else .5*L10
 return np.array([-2,-2,-2]+[-b]*nb+[-np.deg2rad(12)]),np.array([2,2,2]+[b]*nb+[np.deg2rad(12)])

kind='dense_relative_knots';nb=bs[kind].shape[1]
def expand(z,fixedq=None):
 if fixedq is None:ls,lg,q=z[:3];shape=z[3:]
 else:ls,lg=z[:2];q=fixedq;shape=z[2:]
 return np.r_[ls,lg,lg+q,shape,0.]
def fitq(truth,popmean,sigpop,fixedq=None,start=None):
 n=3+nb if fixedq is None else 2+nb
 def fun(z):
  p=expand(z,fixedq);pieces=[(predict(p,kind)-truth)/eV]
  if sigpop is not None:pieces.append(np.linalg.solve(population_chol,(be[kind]@p[3:3+nb]-popmean)/(sigpop*L10)))
  return np.concatenate(pieces)
 def jac(z):
  p=expand(z,fixedq);v,J=predict(p,kind,True);jj=np.column_stack([J[:,0],J[:,1]+J[:,2],J[:,2],J[:,3:3+nb]]) if fixedq is None else np.column_stack([J[:,0],J[:,1]+J[:,2],J[:,3:3+nb]])
  pieces=[jj/eV[:,None]]
  if sigpop is not None:
   jp=np.zeros((len(external_index),n));jp[:,(3 if fixedq is None else 2):]=np.linalg.solve(population_chol,be[kind]/(sigpop*L10));pieces.append(jp)
  return np.vstack(pieces)
 lo=np.array([-3,-3]+([-L10] if fixedq is None else [])+[-.5*L10]*nb);hi=-lo
 starts=[]
 if start is not None:
  st=np.array(start);starts=[st if fixedq is None else np.r_[st[:2],st[3:]]]
 else:
  for q in [-.2,0,.2]:starts.append(np.r_[0.,0.,q,np.zeros(nb)] if fixedq is None else np.zeros(n))
 opts=[least_squares(fun,np.clip(st,lo+1e-8,hi-1e-8),jac=jac,bounds=(lo,hi),ftol=1e-10,xtol=1e-10,gtol=1e-8,max_nfev=500) for st in starts]
 best=min(opts,key=lambda o:o.fun@o.fun);p=expand(best.x,fixedq);q=p[2]-p[1];z=np.r_[best.x[:2],q,best.x[3:]] if fixedq is None else np.r_[best.x[:2],q,best.x[2:]]
 return dict(parameters=z.tolist(),full_parameters=p.tolist(),objective=float(best.fun@best.fun),data_power=float(np.sum(((predict(p,kind)-truth)/eV)**2)),log10S_bias=float(q/L10),log10T_gauge_value=float(p[2]/L10),log10Agas_gauge_value=float(p[1]/L10),success=bool(best.success),active_bounds=bool(np.any(best.active_mask)),multistart_spread=float(max(o.fun@o.fun for o in opts)-min(o.fun@o.fun for o in opts)))
rows=[];profiles=[];checks={}
# Quotient-model Jacobian check, including the chain d/dlngas = Jgas+JT.
z=np.r_[.01,-.02,.03,np.full(nb,.01)];p=expand(z);v,J=predict(p,kind,True);JJ=np.column_stack([J[:,0],J[:,1]+J[:,2],J[:,2],J[:,3:3+nb]]);dif=[]
for j in range(len(z)):
 pp=z.copy();mm=z.copy();pp[j]+=1e-6;mm[j]-=1e-6;fd=(predict(expand(pp),kind)-predict(expand(mm),kind))/(2e-6);dif.append(float(np.max(np.abs(fd-JJ[:,j]))/(1+np.max(np.abs(fd)))))
checks['quotient_jacobian']=max(dif)<1e-7
# Exact global source/T rescaling plus inclination adjustment leaves velocities and S invariant.
p0=np.zeros(4+nb);p1=p0.copy();lam=1.1;p1[:3]=np.log(lam);p1[-1]=np.arcsin(np.sin(inc0)/np.sqrt(lam))-inc0
checks['velocity_only_null']=bool(np.max(np.abs(predict(p0,kind)/predict(p1,kind)-1))<1e-12 and p1[2]-p1[1]==0)
for typ in cfg['truth_shapes']:
 source=(H@np.exp(truthshape(x,typ)))/g0;S=star*source+gas;g=(S+np.sqrt(S*S+4*S*a0))/2;base=np.sqrt(R*kpc*g)/1000;pm=truthshape(externalnodes,typ)
 for bias in cfg['inclination_truth_offsets_deg']:
  truth=base*np.sin(inc0+np.deg2rad(bias))/np.sin(inc0)
  for sig in cfg['external_relative_population_contrast_errors_dex']:
   row=fitq(truth,pm,sig);row.update(name=name,truth_shape=typ,inclination_truth_offset_deg=bias,population_sigma_dex=sig)
   if bias==0:
    probes=[]
    for delta in [-.05,.05]:
     f=fitq(truth,pm,sig,fixedq=L10*delta,start=row['parameters']);probes.append(dict(log10S_fixed=delta,delta_objective=f['objective']-row['objective'],success=f['success'],active_bounds=f['active_bounds']))
    row['true_plusminus_0_05_probes']=probes
   rows.append(row)
   if bias==0 and typ=='bump':
    curve=[];st=row['parameters']
    for dex in np.linspace(-.5,.5,41):
     f=fitq(truth,pm,sig,fixedq=L10*dex,start=st);st=f['parameters'];curve.append(dict(log10S_fixed=float(dex),delta_objective=f['objective']-row['objective'],success=f['success'],active_bounds=f['active_bounds']))
    pts=[p['log10S_fixed'] for p in curve if p['delta_objective']<=1];profiles.append(dict(name=name,population_sigma_dex=sig,best_log10S_bias=row['log10S_bias'],nominal_delta1_grid_interval=None if not pts else[min(pts),max(pts)],interval_hits_grid_edge=bool(pts and(min(pts)==-.5 or max(pts)==.5)),curve=curve))
checks['all_best_success']=all(r['success'] for r in rows);checks['all_profile_success']=all(p['success'] for r in rows for p in r.get('true_plusminus_0_05_probes',[])) and all(p['success'] for r in profiles for p in r['curve']);checks['profiles_not_below_best']=all(p['delta_objective']>=-1e-5 for r in profiles for p in r['curve']);checks['expected18_cases']=len(rows)==18
res=dict(name=name,assertion_tested='DirectquotientS=T/AgasnonlinearprofilewithnoinclinationorabsoluteAgasprior;fixedi isgaugeforvelocity-onlyprojection,notmeasuredgeometry.',selection=cfg,checks=checks,all_checks=all(checks.values()),max_scaled_jacobian_error=max(dif),full_fit_rows=rows,profile_curves=profiles)
(out/'results.json').write_text(json.dumps(res,indent=2));print(name,'allchecks',res['all_checks'])
for p in profiles:print('pop',p['population_sigma_dex'],'biasS',round(p['best_log10S_bias'],6),'profileinterval',p['nominal_delta1_grid_interval'],'truncated',p['interval_hits_grid_edge'])
if not res['all_checks']:raise SystemExit(1)
