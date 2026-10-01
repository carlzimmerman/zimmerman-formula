"""Independent controls of finite-neighbour stress, extended-baryon pressure, and semigroup uniqueness."""
import numpy as np, json, os, pathlib, sys
MUT=os.environ.get('MUTATE')=='1'; checks={}
def ck(k,b,v):checks[k]={'passed':bool(b),'value':v}
def stress(N,nb,multi=False,detrend=False):
    r=np.linspace(.8,1.2,N);v=-r.copy();m=np.full(N,1/N)
    if multi:
        r=np.repeat(r,2);v=np.repeat(v,2)+np.tile([-.5,.5],N);m=np.repeat(m/2,2)
    c=len(r)//2; ids=slice(c-nb,c+nb+1);R=r[ids];V=v[ids];M=m[ids]
    if detrend:
        a,b=np.polyfit(R,V,1,w=np.sqrt(M)); V=V-a*R-b
    var=np.sum(M*V*V)-np.sum(M*V)**2/np.sum(M)
    vol=4*np.pi/3*(R[-1]**3-R[0]**3)
    return float(var/(3*vol))
raw600=stress(600,24);raw1200=stress(1200,24);fixed=stress(1200,48)
clean600=stress(600,24,detrend=not MUT)
true_multi=stress(600,48,multi=True,detrend=True)
ck('raw_single_stream_contamination',raw600>0 and raw1200>0,{'N600':raw600,'N1200':raw1200})
ck('fixed_neighbour_resolution_scaling',abs(raw1200/raw600-.25)<.02,raw1200/raw600)
ck('fixed_fraction_resolves_same_stress',abs(fixed/raw600-1)<.04,fixed/raw600)
ck('affine_detrending_removes_single_stream_stress',abs(clean600)<1e-20,clean600)
ck('affine_detrending_retains_counterstream_stress',true_multi>100*raw600,true_multi)
# Direct dimensionless residual for n=3, G=a0=K=1. Clipped dark growth gives rho=0, but prescribed P'=1/(8pi).
r=1.;n=3.;gb=r**(n-2);Pprime=(n-2)*r**(n-3)/(8*np.pi)
rho_clipped=max(-(n-2)*r**(n-3),0)/(8*np.pi*gb)
ck('clipped_F_not_hydrostatic_P_law',abs(Pprime+rho_clipped*gb)>0.03,{'Pprime_plus_rhog':Pprime+rho_clipped*gb,'rho_clipped':rho_clipped})
# phi_t(k)=exp[t (exp(-k²/2)-1)] is the characteristic function of a Poisson( t ) number of N(0,I) jumps.
k=np.linspace(0,3,301);phi=lambda t:np.exp(t*(np.exp(-k*k/2)-1))
ck('nonGaussian_semigroup',np.max(abs(phi(.4)*phi(.7)-phi(1.1)))<1e-15,float(np.max(abs(phi(.4)*phi(.7)-phi(1.1)))))
# finite per-coordinate variance = t; fourth cumulant = 3t, contrasting a Gaussian's zero.
ck('finite_variance_is_not_heat_uniqueness',np.max(abs(phi(1)-np.exp(-k*k/2)))>.2,{'variance_per_coordinate':1,'fourth_cumulant':3,'max_gaussian_difference':float(np.max(abs(phi(1)-np.exp(-k*k/2))))})
out={'mutation':MUT,'checks':checks,'scope':'Affine monokinetic and symmetric two-stream synthetic data; no claim of a general stress estimator or engine repair'}
p=pathlib.Path(os.environ.get('STRUCTURAL_OUTPUT',str(pathlib.Path(__file__).with_name('structural_results'+('_MUTATE' if MUT else '')+'.json'))));p.write_text(json.dumps(out,indent=2))
for k,v in checks.items():print('PASS' if v['passed'] else 'FAIL',k,v['value'])
sys.exit(0 if all(v['passed'] for v in checks.values()) else 1)
