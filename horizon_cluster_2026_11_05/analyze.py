"""HC-002/003: bounded scales, collective flux, and exploratory observations.
Run via the computation-audit runner; final positional argument is output directory.
All statistical results are descriptive, NOT selection-corrected causal inference.
"""
import csv, json, math, os, sys
from pathlib import Path
import numpy as np
import scipy
from scipy import stats
from numpy.polynomial.legendre import leggauss
import sympy as sp

BASE=Path(__file__).resolve().parent
OUT=Path(sys.argv[1]); OUT.mkdir(parents=True,exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(BASE/'.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
G=6.67430e-11; C=299792458.; MS=1.98847e30
PC=3.085677581491367e16; KPC=1000*PC; AU=149597870700.
LY=9460730472580800.; YEAR=31557600.; LAM=1.09e-52; A0=1.2e-10
RNG=np.random.default_rng(32005)
checks=[]
def check(label,condition):
    assert condition,label
    checks.append(label)
def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
def csvout(name,rows):
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def ols(X,y):
    X=np.asarray(X,float); y=np.asarray(y,float)
    b=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@b
    h=np.einsum('ij,ji->i',X,np.linalg.pinv(X))
    return {'n':len(y),'coefficients':b.tolist(),'rms_dex':float(np.sqrt(np.mean(e*e))),
            'loocv_rmse_dex':float(np.sqrt(np.mean((e/(1-h))**2)))},e
def boot_slope(x,y,B=2000):
    slopes=[]
    for _ in range(B):
        ix=RNG.integers(0,len(y),len(y));xx=x[ix];yy=y[ix]
        if np.std(xx)>0:slopes.append(float(np.cov(xx,yy,ddof=0)[0,1]/np.var(xx)))
    return np.quantile(slopes,[.025,.5,.975]).tolist()

# Exact structural checks independently constrain numerical implementation.
m,r,c,g,a,L=sp.symbols('m r c g a L',positive=True)
rs=2*g*m/c**2
check('MOND radius geometric-mean identity',sp.simplify(g*m/a-rs*(c**2/a)/2)==0)
check('Kottler stationary radius',sp.simplify((g*m/r**2-L*c**2*r/3).subs(r,(3*g*m/(L*c**2))**sp.Rational(1,3)))==0)
x=sp.symbols('x',positive=True)
check('quadrature radial response concave',sp.simplify(sp.diff(sp.sqrt(x*x+a*x),x,2)+a*a/(4*(x*x+a*x)**sp.Rational(3,2)))==0)
check('simple radial response concave',sp.simplify(sp.diff((x+sp.sqrt(x*x+4*a*x))/2,x,2)+2*a*a/(x*x+4*a*x)**sp.Rational(3,2))==0)

data=json.loads((BASE/'data/galaxies.json').read_text())['rows']
check('104 unique published entries',len(data)==104 and len({q['name'] for q in data})==104)
check('two missing spheroid radii',sum(q['Re_sph_kpc'] is None for q in data)==2)
check('one marked upper limit',sum(q['upper_limit'] for q in data)==1)
byname={q['name']:q for q in data}
check('M87 source spot check',byname['NGC 4486']['logMBH']==9.81 and byname['NGC 4486']['Re_sph_kpc']==7.06)
check('Andromeda source spot check',byname['NGC 0224']['logMBH']==8.15 and byname['NGC 0224']['Re_sph_kpc']==.69)
derived=[]
for q in data:
    M=10**q['logMBH']*MS; rs_=2*G*M/C**2; R=q['Re_sph_kpc']
    d=dict(q,rs_pc=rs_/PC,horizon_diameter_AU=2*rs_/AU,
      areaLambda=4*math.pi*rs_**2*LAM,kappa_m_s2=C**2/(2*rs_),
      rM_kpc=math.sqrt(G*M/A0)/KPC,
      BH_to_total_stellar_mass=10**(q['logMBH']-q['logMgal']),
      rs_over_Re=None if R is None else rs_/(R*KPC))
    for Rk in [1,10,100,1000]:d[f'vBH_at_{Rk}kpc_km_s']=math.sqrt(G*M/(Rk*KPC))/1000
    derived.append(d)
csvout('galaxy_scales.csv',derived)
valid=[q for q in derived if q['Re_sph_kpc'] is not None and not q['upper_limit']]
clean=[q for q in valid if not q['author_excluded']]
size_stats={}
for label,rows in [('all_sizes',valid),('author_clean',clean)]+[(t,[q for q in clean if q['type']==t]) for t in ['E','ES/S0','S']]:
    xx=np.log10([q['Re_sph_kpc'] for q in rows]); yy=np.array([q['logMBH'] for q in rows])
    fit,_=ols(np.c_[np.ones(len(xx)),xx],yy)
    fixed=yy-xx;fit['constant_size_ratio_rms_dex']=float(np.std(fixed))
    fit['slope_bootstrap_95pct']=boot_slope(xx,yy)
    fit['spearman_rho']=float(stats.spearmanr(xx,yy).statistic)
    fit['log10_rs_over_Re_range']=[float(np.log10(min(q['rs_over_Re'] for q in rows))),float(np.log10(max(q['rs_over_Re'] for q in rows)))]
    size_stats[label]=fit
xx=np.log10([q['Re_sph_kpc'] for q in clean]);yy=np.array([q['logMBH'] for q in clean])
mass=np.array([q['logMsph'] for q in clean]);morph=np.array([[q['type']=='E',q['type']=='S'] for q in clean],float)
X0=np.c_[np.ones(len(yy)),mass-11,morph];X1=np.c_[X0,xx]
size_stats['host_mass_morphology'],e0=ols(X0,yy)
size_stats['host_mass_morphology_size'],e1=ols(X1,yy)
_,xr=ols(X0,xx)
size_stats['partial_size_r']=float(stats.pearsonr(xr,e0).statistic)
# Leave-one-object-out coefficient sensitivity and measurement perturbation sensitivity.
size_stats['size_coefficient_leave_one_out_range']=[float(v) for v in np.quantile([np.linalg.lstsq(np.delete(X1,i,0),np.delete(yy,i),rcond=None)[0][-1] for i in range(len(yy))],[0,1])]
pert=[]
for _ in range(1000):
    # This is a sensitivity envelope, not EIV inference; distance covariances unavailable.
    yp=yy+RNG.normal(size=len(yy))*np.array([q['err_logMBH'] for q in clean])
    xp=xx+RNG.normal(0,.10,len(xx)) # declared assumed size systematic
    mp=mass+RNG.normal(size=len(yy))*np.array([q['err_logMsph'] for q in clean])
    pert.append(np.linalg.lstsq(np.c_[np.ones(len(yy)),mp-11,morph,xp],yp,rcond=None)[0][-1])
size_stats['size_coefficient_sensitivity_95pct_assumed_0p1dex_size']=np.quantile(pert,[.025,.5,.975]).tolist()
dump('size_statistics.json',size_stats)

# Horizon bounds and independent-input scans.
puzzle_r=math.sqrt(8*math.pi/LAM); dS=math.sqrt(3/LAM)
spins=np.linspace(0,1,1001);kerr=(1+np.sqrt(1-spins*spins))/2
check('Kerr cannot increase Schwarzschild area',np.all((kerr>=.5)&(kerr<=1)))
fidmass=1e15*MS;full_rs=2*G*fidmass/C**2
scales={'aLambda':C**2*math.sqrt(LAM/(32*math.pi)), 'a0_independent':A0,
 'puzzle_radius_Gly':puzzle_r/LY/1e9,'puzzle_mass_Msun':puzzle_r*C**2/(2*G*MS),
 'puzzle_radius_over_dS':puzzle_r/dS,'puzzle_mass_over_Nariai':puzzle_r*C**2/(2*G)/(C**2/(3*G*math.sqrt(LAM))),
 'all_1e15_Msun_in_one_BH_A_Lambda':4*math.pi*full_rs**2*LAM,
 'cluster_1e15_Msun_1Mpc_compactness':full_rs/(1000*KPC),
 'sample_areaLambda_range':[min(q['areaLambda'] for q in derived if not q['upper_limit']),max(q['areaLambda'] for q in derived if not q['upper_limit'])],
 'kerr_area_ratio_range':[float(kerr.min()),float(kerr.max())],
 'independent_a0_Lambda_grid':[]}
for la in [.5e-52,1.09e-52,2e-52]:
    for ac in [.8e-10,1.2e-10,1.6e-10]:
        scales['independent_a0_Lambda_grid'].append({'Lambda':la,'a0':ac,'constructed_A_Lambda':math.pi*C**4/ac**2*la})
for n in [1,10,100,1000]:
    # Area sum at fixed total mass: exact ratio 1/N for equal masses.
    check(f'fixed-total-mass area sum N={n}',math.isclose(n*(fidmass/n)**2/fidmass**2,1/n))
dump('horizon_bounds.json',scales)

# Interaction grid: explicit illustrative inputs, not a fit to an actual cluster.
interactions=[]
for mbh in [1e6,1e8,1e10]:
 for host in [1e10,1e11,1e12]:
  for dk in [10,100,1000]:
   dist=dk*KPC; bh=mbh*MS;mh=host*MS
   acc=G*bh/dist**2; host_acc=G*mh/dist**2
   interactions.append({'MBH_Msun':mbh,'Mhost_Msun':host,'separation_kpc':dk,
    'gBH':acc,'gHost':host_acc,'BH_host_force_ratio':acc/host_acc,
    'gLambda_outward':LAM*C**2*dist/3,
    'BH_pair_escape_km_s':math.sqrt(4*G*bh/dist)/1000,
    'BH_pair_circular_period_Gyr':2*math.pi*math.sqrt(dist**3/(2*G*bh))/YEAR/1e9,
    'BH_tidal_gradient_s2':2*G*bh/dist**3,
    'BH_Kottler_turnaround_kpc':(3*G*bh/(LAM*C**2))**(1/3)/KPC})
check('27 interaction cases (3 masses x 3 hosts x 3 separations)',len(interactions)==27)
csvout('interaction_grid.csv',interactions)

# Surface-flux QUMOND integral: two equal point masses inside a spherical boundary.
# Unit R, total GM=1. z positions ±offset; all outward normal field components positive.
def nu(y,kernel):
    if kernel=='quadrature':return np.sqrt(1+1/y)
    if kernel=='simple':return .5+np.sqrt(.25+1/y)
    return np.ones_like(y)
def flux(offset,y,n,kernel):
    z,w=leggauss(n);st=np.sqrt(1-z*z);gr=np.zeros_like(z);gt=np.zeros_like(z)
    # Field in cylindrical coordinates; dot with radial/meridional unit vectors.
    for pos in [-offset,offset]:
        d2=1+pos*pos-2*pos*z
        gr+=.5*(1-pos*z)/d2**1.5
        gt+=.5*pos*st/d2**1.5
    norm=np.hypot(gr,gt)
    return float(np.dot(w,nu(y*norm,kernel)*gr)/2)
flux_rows=[]
for kernel in ['newton','quadrature','simple']:
 for y in [.01,1.,100.]:
  for offset in [0,.1,.3,.6,.9]:
   vals=[flux(offset,y,n,kernel) for n in [64,128,256]]
   smooth=float(nu(np.array([y]),kernel)[0])
   check(f'flux convergence {kernel},{y},{offset}',abs(vals[-1]-vals[-2])<1e-7*abs(vals[-1]))
   if kernel=='newton':check(f'Newton Gauss {y},{offset}',abs(vals[-1]-1)<1e-10)
   else:check(f'no excess enclosing flux {kernel},{y},{offset}',vals[-1]<=smooth+1e-10)
   flux_rows.append({'kernel':kernel,'y_boundary':y,'offset_over_R':offset,
      'apparent_mass_ratio_to_smooth':vals[-1]/smooth,
      'phantom_mass_ratio_to_smooth':None if kernel=='newton' else (vals[-1]-1)/(smooth-1),
      'convergence_delta':abs(vals[-1]-vals[-2])})
check('45 flux configurations',len(flux_rows)==45)
csvout('collective_flux.csv',flux_rows)

# Energy availability envelope: ε includes conversion AND coupling; M_acc parameter explicit.
feedback=[]
for Macc in [1e8,1e9,1e10]:
 for eps in [1e-4,1e-3,1e-2,.1]:
  for Mgas,T in [(1e12,1),(1e13,3),(1e14,5)]:
   eth=1.5*(Mgas*MS/(.6*1.67262192369e-27))*(T*1.602176634e-16)
   en=eps*Macc*MS*C**2
   feedback.append({'Macc_Msun':Macc,'net_coupling_efficiency':eps,'Mgas_Msun':Mgas,
     'kT_keV':T,'energy_J':en,'thermal_energy_J':eth,'energy_over_thermal':en/eth})
csvout('feedback_budget.csv',feedback)

# Independent 85-system hot-halo sample: retain its own mass and radius conventions.
gp=json.loads((BASE/'data/gaspari.json').read_text())
opt=gp['optical_table'];hot=gp['xray_table'];hotmap={q['name']:q for q in hot}
check('85 matched Gaspari objects',len(opt)==85 and set(hotmap)=={q['name'] for q in opt})
gasrows=[dict(q,**{k:v for k,v in hotmap[q['name']].items() if k not in ['name','refs']}) for q in opt]
def canonical(name):
    if name.startswith('N') and name[1:].isdigit():return 'NGC '+name[1:].zfill(4)
    if name.startswith('IC') and name[2:].isdigit():return 'IC '+str(int(name[2:]))
    return name
matches=[]
for q in gasrows:
    M=10**q['logMBH']*MS;sig=10**q['logSigma']*1000
    q['r_influence_pc']=G*M/sig**2/PC
    key=canonical(q['name'])
    if key in byname:
        s=byname[key]
        matches.append({'name':key,'gaspari_name':q['name'],'environment':q['environment'],
          'delta_logMBH_size_minus_gaspari':s['logMBH']-q['logMBH'],
          'Re_sph_kpc':s['Re_sph_kpc'],'Re_opt_kpc':10**q['logRe_opt_kpc'],
          'r_influence_pc':q['r_influence_pc']})
csvout('sample_crossmatch.csv',matches)
csvout('gaspari_derived.csv',gasrows)
gstats={'crossmatch_count':len(matches),'models':{},'environment_counts':{}}
for q in gasrows:
    env=q['environment'].split(':')[0]
    gstats['environment_counts'][env]=gstats['environment_counts'].get(env,0)+1
yy=np.array([q['logMBH'] for q in gasrows]);n=len(yy)
columns={k:np.array([q[k] for q in gasrows],float) for k in ['logTx_g','logTx_c','logSigma','logLK','logRe_opt_kpc']}
check('hot predictors finite',all(np.isfinite(v).all() for v in columns.values()))
for key,v in columns.items():
    fit,_=ols(np.c_[np.ones(n),v],yy)
    fit['slope_bootstrap_95pct']=boot_slope(v,yy)
    gstats['models'][key]=fit
X=np.c_[np.ones(n),columns['logSigma'],columns['logLK'],columns['logRe_opt_kpc']]
gstats['models']['optical_baseline'],res=ols(X,yy)
gstats['models']['optical_plus_Tx_g'],_=ols(np.c_[X,columns['logTx_g']],yy)
_,txres=ols(X,columns['logTx_g'])
observed=float(stats.pearsonr(res,txres).statistic)
null=np.array([np.corrcoef(res,RNG.permutation(txres))[0,1] for _ in range(5000)])
gstats['temperature_partial_r']=observed
gstats['temperature_partial_permutation_p_exploratory']=(1+int(np.sum(np.abs(null)>=abs(observed))))/5001
gstats['temperature_partial_r_leave_one_out_range']=[float(v) for v in np.quantile([np.corrcoef(np.delete(res,i),np.delete(txres,i))[0,1] for i in range(n)],[0,1])]
gstats['r_influence_pc_range']=[min(q['r_influence_pc'] for q in gasrows),max(q['r_influence_pc'] for q in gasrows)]
dump('hot_halo_statistics.json',gstats)

fig,axs=plt.subplots(1,3,figsize=(16,4.8),layout='constrained')
colors={'E':'#8e44ad','ES/S0':'#d98e04','S':'#147d92'}
for kind,col in colors.items():
    subset=[q for q in clean if q['type']==kind]
    axs[0].scatter([q['Re_sph_kpc'] for q in subset],[10**q['logMBH'] for q in subset],label=kind,c=col,s=22,alpha=.8)
axs[0].set(xscale='log',yscale='log',xlabel='Spheroid half-light radius (kpc)',ylabel='Black-hole mass (solar masses)',title='Size and BH mass: morphology matters');axs[0].legend()
axs[1].scatter(10**columns['logTx_g'],10**yy,s=20,c='#315e9e',alpha=.7)
axs[1].set(xscale='log',yscale='log',xlabel='Galactic hot-gas temperature (keV)',ylabel='Black-hole mass (solar masses)',title='Published hot-halo sample (85 systems)')
for y in [.01,1,100]:
    sub=[q for q in flux_rows if q['kernel']=='quadrature' and q['y_boundary']==y]
    axs[2].plot([q['offset_over_R'] for q in sub],[q['apparent_mass_ratio_to_smooth'] for q in sub],'o-',label=f'gN/a0={y:g}')
axs[2].axhline(1,color='gray',linestyle='--');axs[2].set(xlabel='Clump offset / enclosing radius',ylabel='Enclosed apparent mass / smooth',title='Two-clump gravity: redistribution');axs[2].legend()
fig.savefig(OUT/'overview.png',dpi=180);plt.close(fig)
dump('checks.json',{'checks':checks,'count':len(checks),'seed':32005,
 'nonclaims':['No independent dynamical/lensing discrepancy measured here','No causal claim','No 32pi derivation','No selection-corrected regression','No new relativistic field equation']})
print(json.dumps({'checks':len(checks),'sample_rows':len(data),'size_clean':len(clean),
 'size_slope':size_stats['author_clean']['coefficients'][1],
 'hot_partial_r':observed,'crossmatch':len(matches),'horizon_max':scales['sample_areaLambda_range'][1]},indent=2))
