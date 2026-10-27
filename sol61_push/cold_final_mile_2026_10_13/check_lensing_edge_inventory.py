"""CE-FM-061: independent projection/covariance check and finite-stock lensing bound."""
import sys,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import ellipk
b=Path('campaign_fresh_gravity/CFG801_settled_edge_vs_kids')
d=Path('real_research/data/lensing_rar/brouwer2021_rar')
checks=[]
def ck(n,v):
    assert v,n
    checks.append(n)
raw=[np.loadtxt(d/f'Fig-3_Lensing-rotation-curves_Massbin-{i}.txt') for i in range(1,5)]
radii=np.array([r[:,0] for r in raw]);Y=np.concatenate([r[:,1]/r[:,4] for r in raw])
c=np.loadtxt(d/'Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt');keys=sorted(set(c[:,0]));C=np.zeros((60,60))
for row in c:
    i=keys.index(row[0])*15+int(np.argmin(abs(radii[0]-row[2])))
    j=keys.index(row[1])*15+int(np.argmin(abs(radii[0]-row[3])))
    C[i,j]=row[4]/row[6]
ck('full covariance symmetric',np.max(abs(C-C.T))<1e-10)
ck('full covariance positive definite',np.linalg.eigvalsh(C).min()>0)
reported_err=np.concatenate([r[:,3]/r[:,4] for r in raw])
ck('bias-corrected diagonal uncertainties',np.max(abs(np.sqrt(C.diagonal())/reported_err-1))<1e-4)
sup=5.364;edge=math.sqrt(sup*(1+sup))
rho=lambda r:1/(2*math.pi*r*math.sqrt(1+4*r*r))
Mp=lambda r:2*r/math.sqrt(1+4*r*r)
M=lambda r:(math.sqrt(1+4*r*r)-1)/2
# Evaluate each aperture directly, independent of source's700-point cumulative grid.
def esd(x,trunc):
    if trunc and x>=edge:return (sup+1)/(math.pi*x*x)
    if trunc:
        sig=2*quad(lambda z:rho(math.hypot(x,z)),0,math.sqrt(edge*edge-x*x),epsabs=1e-11,epsrel=1e-10)[0]
        top=edge
    else:
        sig=ellipk(1/(1+4*x*x))/(math.pi*math.sqrt(1+4*x*x));top=np.inf
    mc=M(x)+quad(lambda r:Mp(r)*(x/r)**2/(1+math.sqrt(max(0,1-(x/r)**2))),x,top,epsabs=1e-11,epsrel=1e-10)[0]
    return mc/(math.pi*x*x)-sig+1/(math.pi*x*x)
for xx in [.5,1,5]:
    sigq=2*quad(lambda z:rho(math.hypot(xx,z)),0,np.inf,epsabs=1e-12)[0]
    sige=ellipk(1/(1+4*xx*xx))/(math.pi*math.sqrt(1+4*xx*xx))
    ck('infinite Abel elliptic crosscheck '+str(xx),abs(sigq-sige)<1e-10)
for xx in [edge,10,20]:ck('exterior total mass bound equality '+str(xx),esd(xx,True)==(sup+1)/(math.pi*xx*xx))
summary=[]
for foot,a0si in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
    rec=json.loads((b/('cfg801_results'+('_alt' if foot=='alt' else '')+'.json')).read_text())
    a0=a0si*3.0857e16/1e6;G=4.30091e-3
    for scope,idx in [('primary R<=0.31 Mpc',np.where(radii[0]<=.31)[0]),('all radii',np.arange(15))]:
        sel=np.concatenate([idx+15*j for j in range(4)]);cc=C[np.ix_(sel,sel)]
        result={}
        for trunc,key in [(True,'edge'),(False,'noedge')]:
            masses=rec[scope]['logMb_'+key];pred=[]
            for j in range(4):
                mass=10**masses[j];rM=math.sqrt(G*mass/a0)
                pred.extend([mass/rM**2*esd(R*1e6/rM,trunc) for R in radii[j,idx]])
            rr=Y[sel]-pred;val=float(rr@np.linalg.solve(cc,rr));old=rec[scope]['chi2_'+key]
            ck('independent score '+foot+' '+scope+' '+key,abs(val-old)<3)
            result[key]={'chi2_at_reported_profiled_masses':val,'stored_chi2':old,'projection_difference':val-old}
        result['dchi2']=result['edge']['chi2_at_reported_profiled_masses']-result['noedge']['chi2_at_reported_profiled_masses']
        ck('edge loses decisively in same comparison '+foot+' '+scope,result['dchi2']>9)
        result.update(footing=foot,scope=scope,n=len(sel));summary.append(result)
# Model-independent inequality: Sigma>=0, M_cyl<=M_total => DeltaSigma<=M_total/(piR^2).
# These are pointwise data-level diagnostics, NOT simultaneous confidence intervals.
nom=[10.14,10.57,10.78,10.96] # authenticated B21 mean stars+cold gas, not source Z stellar-only numbers
bounds=[]
for j in range(4):
    for cutoff in [.3,.31]:
        i=int(np.where(radii[j]<=cutoff)[0][-1]);R=radii[j,i]*1e6;y=Y[15*j+i];sig=math.sqrt(C[15*j+i,15*j+i])
        minimum=math.pi*R*R*y;low=math.pi*R*R*(y-sig)
        bounds.append({'bin':j+1,'cutoff_Mpc':cutoff,'R_Mpc':R/1e6,'ESD':y,'diagonal_sigma':sig,'nominal_projected_total_mass_lower_bound_Msun':minimum,'one_sigma_lower_ESD_mass_diagnostic_Msun':low,'B21_mean_stars_coldgas_logmass':nom[j],'nominal_minimum_Mb_if_stock_ratio5p364':minimum/(1+sup),'nominal_minimum_over_reference_total_stock':minimum/((1+sup)*10**nom[j])})
res={'claim_id':'CE-FM-061','checks_passed':len(checks),'checks':checks,'independent_projection_scores':summary,'finite_inventory_pointwise_diagnostics':bounds,'scope':'Scores evaluated at published grid-profiled masses, not reoptimized; same declared point-mass/stack model. No universal disk/S4 exclusion or new confidence calibration.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
