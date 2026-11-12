import pathlib,json,sys,math
import numpy as np
from scipy.optimize import least_squares
root=pathlib.Path(__file__).parent;cfg=json.loads((root/'selection.json').read_text());name=sys.argv[1];out=root/sys.argv[2];out.mkdir(exist_ok=True)
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
x=np.log(rp/Rd);nodes=np.log([.3,1,3,10]);externalnodes=nodes[[0,2,3]]
L10=np.log(10);kpc=3.085677581491367e19;star=.5*Vd*Vd*1e6/(R*kpc);gas=np.sign(Vg)*Vg*Vg*1e6/(R*kpc);a0=cfg['a0']
def truthshape(x,typ):
 if typ=='bend':return L10*.08*np.tanh(x/.8)
 if typ=='bump':return L10*.10*(np.exp(-(x-np.log(2))**2/(2*.45**2))-np.exp(-np.log(2)**2/(2*.45**2)))
 return L10*.06*.25*(np.logaddexp(0,(x-.3)/.25)-np.logaddexp(0,-.3/.25))
def basis(xx,kind):
 if kind=='one_power':return np.array(xx)[:,None]
 mat=[]
 for j in [0,2,3]:
  vals=np.zeros(4);vals[j]=1;mat.append(np.interp(xx,nodes,vals))
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

def fit(kind,truth,popmean,sigpop,fixedT=None,start=None):
 nb=bs[kind].shape[1];n=4+nb;lo,hi=bounds(kind);free=[j for j in range(n) if not(fixedT is not None and j==2)];fixed=np.zeros(n);fixed[2]=0 if fixedT is None else fixedT
 def expand(z):
  p=fixed.copy();p[free]=z;return p
 def fun(z):
  p=expand(z);v=predict(p,kind);pieces=[(v-truth)/eV,np.array([p[-1]/sigi])]
  if sigpop is not None:pieces.append((be[kind]@p[3:3+nb]-popmean)/(sigpop*L10))
  return np.concatenate(pieces)
 def jac(z):
  p=expand(z);v,J=predict(p,kind,True);parts=[J/eV[:,None]];ji=np.zeros((1,n));ji[0,-1]=1/sigi;parts.append(ji)
  if sigpop is not None:
   jj=np.zeros((3,n));jj[:,3:3+nb]=be[kind]/(sigpop*L10);parts.append(jj)
  return np.vstack(parts)[:,free]
 starts=[]
 if start is not None:starts=[np.asarray(start)]
 else:
  for tt in cfg['starts_logT']:
   p=np.zeros(n);p[2]=tt;starts.append(p)
 opts=[]
 for st in starts:
  zz=np.clip(st[free],lo[free]+1e-8,hi[free]-1e-8);opts.append(least_squares(fun,zz,jac=jac,bounds=(lo[free],hi[free]),ftol=1e-10,xtol=1e-10,gtol=1e-8,max_nfev=400))
 best=min(opts,key=lambda o:o.fun@o.fun);p=expand(best.x);v=predict(p,kind)
 return dict(params=p.tolist(),objective=float(best.fun@best.fun),data_power=float(np.sum(((v-truth)/eV)**2)),population_power=0 if sigpop is None else float(np.sum(((be[kind]@p[3:3+nb]-popmean)/(sigpop*L10))**2)),inclination_power=float((p[-1]/sigi)**2),log10T_bias=float(p[2]/L10),success=bool(best.success),nfev=int(best.nfev),active_bounds=bool(np.any(best.active_mask!=0)),multistart_objective_spread=float(max(o.fun@o.fun for o in opts)-min(o.fun@o.fun for o in opts)),max_fractional_velocity_residual=float(np.max(np.abs(v/truth-1))))

rows=[];profiles=[];checks={};bench=[]
# Derivative check away from zero shape.
for kind in cfg['inverse_shapes']:
 p=np.zeros(4+bs[kind].shape[1]);p[3:3+bs[kind].shape[1]]=.01
 _,J=predict(p,kind,True);errs=[]
 for j in range(len(p)):
  pp=p.copy();pm=p.copy();pp[j]+=1e-6;pm[j]-=1e-6;fd=(predict(pp,kind)-predict(pm,kind))/(2e-6);errs.append(float(np.max(np.abs(fd-J[:,j]))/(1+np.max(np.abs(fd)))))
 checks[kind+'_jacobian']=max(errs)<1e-7;bench.append(dict(kind=kind,max_scaled_jacobian_error=max(errs)))
for typ in cfg['truth_shapes']:
 source=(H@np.exp(truthshape(x,typ)))/g0;S=star*source+gas;g=(S+np.sqrt(S*S+4*S*a0))/2;base=np.sqrt(R*kpc*g)/1000;pm=truthshape(externalnodes,typ)
 for bias in cfg['inclination_truth_offsets_deg']:
  truth=base*np.sin(inc0+np.deg2rad(bias))/np.sin(inc0)
  for kind in cfg['inverse_shapes']:
   for sig in cfg['external_relative_population_contrast_errors_dex']:
    row=fit(kind,truth,pm,sig);row.update(name=name,truth_shape=typ,inclination_truth_offset_deg=bias,inverse_shape=kind,population_sigma_dex=sig,inclination_exact_scale_bias_dex=float(2*np.log10(np.sin(inc0+np.deg2rad(bias))/np.sin(inc0))))
    if kind=='three_relative_knots' and bias==0:
     probes=[]
     for delta in [-.05,.05]:
      ff=fit(kind,truth,pm,sig,fixedT=L10*delta,start=row['params']);probes.append(dict(log10T_fixed=delta,delta_objective=ff['objective']-row['objective'],success=ff['success'],active_bounds=ff['active_bounds']))
     row['true_plusminus_0_05_profile_probes']=probes
    rows.append(row)
  if bias==0 and typ=='bump':
   for sig in cfg['external_relative_population_contrast_errors_dex']:
    nominal=next(r for r in rows if r['truth_shape']==typ and r['inclination_truth_offset_deg']==0 and r['inverse_shape']=='three_relative_knots' and r['population_sigma_dex']==sig)
    curve=[];st=nominal['params']
    for dex in np.linspace(-.30,.30,25):
     ff=fit('three_relative_knots',truth,pm,sig,fixedT=L10*dex,start=st);st=ff['params'];curve.append(dict(log10T_fixed=float(dex),delta_objective=float(ff['objective']-nominal['objective']),success=ff['success'],active_bounds=ff['active_bounds']))
    selected=[p['log10T_fixed'] for p in curve if p['delta_objective']<=1]
    profiles.append(dict(name=name,truth_shape=typ,population_sigma_dex=sig,inverse_shape='three_relative_knots',best_log10T_bias=nominal['log10T_bias'],nominal_delta1_grid_interval=None if not selected else [min(selected),max(selected)],interval_hits_grid_edge=bool(selected and(min(selected)==-.3 or max(selected)==.3)),curve=curve))
checks['all_fitted_best_optimizers_succeeded']=all(x['success'] for x in rows)
checks['all_profile_optimizers_succeeded']=all(p['success'] for x in profiles for p in x['curve']) and all(p['success'] for x in rows for p in x.get('true_plusminus_0_05_profile_probes',[]))
checks['profile_not_below_recorded_best_by_more_1e_5']=all(p['delta_objective']>=-1e-5 for x in profiles for p in x['curve'])
checks['expected48_fullcases']=len(rows)==48
summary=[]
for kind in cfg['inverse_shapes']:
 for sig in cfg['external_relative_population_contrast_errors_dex']:
  for bias in cfg['inclination_truth_offsets_deg']:
   rr=[r for r in rows if r['inverse_shape']==kind and r['population_sigma_dex']==sig and r['inclination_truth_offset_deg']==bias]
   summary.append(dict(inverse_shape=kind,population_sigma_dex=sig,inclination_truth_offset_deg=bias,max_abs_log10T_bias=float(max(abs(r['log10T_bias']) for r in rr)),biases_by_truth={r['truth_shape']:r['log10T_bias'] for r in rr},max_data_power=max(r['data_power'] for r in rr),any_bounds=any(r['active_bounds'] for r in rr)))
res=dict(name=name,assertion_tested='Finite adversarial source-profile family,profiled nonlinear inverse and hypothetical independentpopulationcontrast precision;not observationalvalidation or globalfunctionminimax.',selection=cfg,geometry=dict(distance_Mpc=D,inclination_deg=inc,inclination_error_deg=si,Rd_kpc=Rd,rows=len(R)),checks=checks,all_checks=all(checks.values()),derivative_benchmarks=bench,full_fit_rows=rows,profile_curves=profiles,summary=summary,nonclaims=['No Euclid colors-to-IMF calibration','No independent real population measurements','Same softened Newtonian geometry but truthshape differs frominversefamily','No AQUAL disk solution','No measured covariance or 2Dvelocity/lightdeprojection response','Finite-family minimaxonly'])
(out/'results.json').write_text(json.dumps(res,indent=2));print(name,'allchecks',res['all_checks'],'fullcases',len(rows),'profilecurves',len(profiles))
for x in summary:
 if x['inclination_truth_offset_deg']==0:print(x['inverse_shape'],x['population_sigma_dex'],'maxbias',round(x['max_abs_log10T_bias'],5),'data_power',round(x['max_data_power'],3))
if not res['all_checks']:raise SystemExit(1)
