"""Bounded native-pixel DESI absorption-line diagnostic, not a pPXF reproduction.

Forward models the supplied DESI resolution operator, retaining negative entries.
E-MILES air wavelengths are converted to vacuum. A local Gaussian variance
correction removes the intrinsic template LSF before the DESI LSF is applied.
This approximation is benchmarked with analytic lines and a sampling control.
"""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[key] = "1"
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/forj0332-mpl-cache")
import argparse, importlib.util, json, time
from pathlib import Path
from functools import lru_cache
import numpy as np
from scipy import sparse
from scipy.optimize import nnls, minimize, minimize_scalar
from scipy.special import ndtr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = 299792.458
Z = 0.3202209572
HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
ROOT = HERE.parents[2]
TEMPLATE = ROOT / "_external_data/lam2_templates_2026_11_03/spectra_emiles_9.0.npz"

def air_to_vac(air):
    vac = np.asarray(air, dtype=float).copy()
    for _ in range(4):
        s2 = (1e4/vac)**2
        vac = air*(1 + 0.0000834254 + 0.02406147/(130-s2) + 0.00015998/(38.9-s2))
    return vac

def broadening_matrix(lam, sigma, template_fwhm, half=70):
    # Local wavelength quadrature of a Gaussian LOSVD, with intrinsic-template
    # Gaussian variance subtracted. The relative width changes slowly in lambda.
    intrinsic = np.broadcast_to(template_fwhm, lam.shape)/2.354820045
    width2 = (lam*sigma/C)**2 - intrinsic**2
    if np.any(width2 <= 0):
        raise ValueError("stellar broadening below template resolution")
    width = np.sqrt(width2)
    rows = np.repeat(np.arange(len(lam)), 2*half+1)
    cols = (np.arange(len(lam))[:,None] + np.arange(-half, half+1)).ravel()
    valid = (cols >= 0) & (cols < len(lam))
    rows, cols = rows[valid], cols[valid]
    values = np.exp(-.5*((lam[cols]-lam[rows])/width[rows])**2)*np.gradient(lam)[cols]
    values /= np.bincount(rows, weights=values, minlength=len(lam))[rows]
    return sparse.csr_matrix((values, (rows,cols)), shape=(len(lam),len(lam)))

class Engine:
    def __init__(self, refine=1):
        raw = np.load(PARENT/'desi_spectrum/target_coadd.npz')
        self.raw = raw
        t = np.load(TEMPLATE)
        ages = [12,14,16,18,20,22]  # 1,1.58,2.51,3.98,6.31,10 Gyr
        metals = [2,3,4,5]
        self.labels = [(float(t['ages'][a]),float(t['metals'][m])) for a in ages for m in metals]
        cut = (t['lam'] > 3600) & (t['lam'] < 5750)
        air = t['lam'][cut]
        self.lam = air_to_vac(air)
        self.fwhm = t['fwhm'][cut]*np.gradient(self.lam)/np.gradient(air)
        self.templates = np.stack([t['templates'][cut,a,m] for a in ages for m in metals],axis=1)
        self.templates /= np.median(self.templates[(self.lam>5000)&(self.lam<5500)],axis=0)
        if refine > 1:
            finer = np.linspace(self.lam[0],self.lam[-1],(len(self.lam)-1)*refine+1)
            self.templates = np.stack([np.interp(finer,self.lam,x) for x in self.templates.T],axis=1)
            self.fwhm = np.interp(finer,self.lam,self.fwhm)
            self.lam = finer
        self.refine = refine
        self.bands = {}
        for b in 'BR':
            w = raw[b+'_WAVELENGTH'].astype(float)
            data = raw[b+'_RESOLUTION'][0].astype(float)
            R = sparse.dia_matrix((data,np.arange(5,-6,-1)),shape=(len(w),len(w))).tocsr()
            self.bands[b] = dict(w=w, flux=raw[b+'_FLUX'][0].astype(float),
                ivar=raw[b+'_IVAR'][0].astype(float), mask=raw[b+'_MASK'][0],R=R)

    @lru_cache(maxsize=96)
    def broaden(self,sigma):
        return broadening_matrix(self.lam,sigma,self.fwhm,70*self.refine) @ self.templates

    def design(self,sigma,velocity):
        broad = self.broaden(float(sigma))
        out = {}
        for b,d in self.bands.items():
            x = d['w']/(1+Z)*np.exp(-velocity/C)
            ix = np.searchsorted(self.lam,x)-1
            ix = np.clip(ix,0,len(self.lam)-2)
            fraction = np.clip((x-self.lam[ix])/(self.lam[ix+1]-self.lam[ix]),0,1)
            interp = broad[ix]*(1-fraction[:,None])+broad[ix+1]*fraction[:,None]
            out[b] = d['R'] @ interp
        return out

class Fit:
    def __init__(self,engine,config,synthetic=None):
        self.engine,self.config = engine,config
        self.indices = [j for j,(a,m) in enumerate(engine.labels) if a>=config.get('age_min',0)]
        self.blocks,self.slices = [],{}
        ys,weights,Ps = [],[],[]
        start=0
        for b,lo,hi in config['windows']:
            d=engine.bands[b];w=d['w'];rest=w/(1+Z)
            good=(rest>=lo)&(rest<=hi)&(d['ivar']>0)&(d['mask']==0)&np.isfinite(d['flux'])
            # Foreground narrow emission and strong terrestrial sky residuals.
            for line in [4862.68,4960.30,5008.24]:
                good &= np.abs(rest-line)>10
            for line in [5577.34,6300.30,6363.78]:
                good &= np.abs(w-line)>6
            if 'mgii_halfwidth' in config:
                good &= np.abs(w-2799.12*2.210)>config['mgii_halfwidth']
            x=2*(rest[good]-lo)/(hi-lo)-1
            P=np.polynomial.legendre.legvander(x,config['degree'])
            y=d['flux'][good] if synthetic is None else synthetic[b][good]
            self.blocks.append((b,good));self.slices[b]=slice(start,start+len(y));start+=len(y)
            ys.append(y);weights.append(np.sqrt(d['ivar'][good]));Ps.append(P)
        self.y=np.concatenate(ys);self.weight=np.concatenate(weights)
        self.P=sparse.block_diag(Ps).toarray()
        self.Q=np.linalg.qr(self.P*self.weight[:,None],mode='reduced')[0]
        self.yw=self.y*self.weight
        self.yp=self.yw-self.Q@(self.Q.T@self.yw)
        self.count=0

    def evaluate(self,params,detail=False):
        sigma,velocity=params
        if not(100 <= sigma <= 450 and -300 <= velocity <= 300):
            return 1e15+1e8*((sigma-275)**2+velocity**2)
        full=self.engine.design(float(sigma),float(velocity))
        A=np.vstack([full[b][good][:,self.indices] for b,good in self.blocks])
        Aw=A*self.weight[:,None]
        Ap=Aw-self.Q@(self.Q.T@Aw)
        coeff,norm=nnls(Ap,self.yp,maxiter=1000)
        self.count+=1
        chi2=float(norm*norm)
        if not detail:return chi2
        poly=np.linalg.lstsq(self.P*self.weight[:,None],self.yw-Aw@coeff,rcond=None)[0]
        model=A@coeff+self.P@poly
        return dict(chi2=chi2,model=model,stellar=A@coeff,coeff=coeff,poly=poly,
            sigma=float(sigma),velocity=float(velocity),ngood=len(self.y),active_templates=int((coeff>1e-7).sum()))

def fit_one(engine,config,out,profile=True,synthetic=None):
    f=Fit(engine,config,synthetic)
    # Both widely separated literature values are starting points, not priors.
    opts=[minimize(f.evaluate,[s,0.],method='Nelder-Mead',options={'maxiter':110,'xatol':.08,'fatol':.0001}) for s in [220.,320.]]
    opt=min(opts,key=lambda x:x.fun)
    best=f.evaluate(opt.x,True)
    grid=np.array(sorted(set(list(np.arange(100.,451.,25.))+[222.26,284.418,317.619,float(opt.x[0])]))) if profile else np.array([opt.x[0]])
    prof=[]
    for sigma in grid:
        v=minimize_scalar(lambda v:f.evaluate([sigma,v]),bounds=(-220,220),method='bounded',options={'xatol':.3,'maxiter':30})
        prof.append([float(sigma),float(v.x),float(v.fun)])
    prof=np.array(prof)
    # Linear interpolation of grid crossings is a descriptive diagnostic, not a
    # calibrated marginal credible interval or a complete systematic uncertainty.
    deltas=prof[:,2]-best['chi2']
    intervals={}
    for threshold in [1.,4.]:
        left=right=None
        for j in range(len(grid)-1):
            if (deltas[j]-threshold)*(deltas[j+1]-threshold)<0:
                crossing=float(grid[j]+(threshold-deltas[j])*(grid[j+1]-grid[j])/(deltas[j+1]-deltas[j]))
                if crossing<best['sigma']:left=crossing
                else:right=crossing
        intervals[str(threshold)]=[left,right]
    record={k:v for k,v in best.items() if k not in ('model','stellar','coeff','poly')}
    record.update(config=config,evaluations=f.count,optimizer_success=[bool(o.success) for o in opts],
        optima=[dict(sigma=float(o.x[0]),velocity=float(o.x[1]),chi2=float(o.fun)) for o in opts],
        chi2_per_pixel=best['chi2']/len(f.y),profile=prof.tolist(),delta_chi2_intervals_linear_grid=intervals,
        template_weights=[dict(age_Gyr=engine.labels[j][0],metallicity=engine.labels[j][1],weight=float(v)) for j,v in zip(f.indices,best['coeff'])],
        additive_polynomial=best['poly'].tolist())
    arrays={'flux':f.y,'weight':f.weight,'best_model':best['model'],'stellar_component':best['stellar'],'profile':prof}
    arrays['wave']=np.concatenate([engine.bands[b]['w'][good] for b,good in f.blocks])
    arrays['band']=np.concatenate([np.full(good.sum(),b) for b,good in f.blocks])
    np.savez_compressed(out/(config['name']+'_model.npz'),**arrays)
    (out/(config['name']+'.json')).write_text(json.dumps(record,indent=2))
    print(config['name'],record['sigma'],record['velocity'],record['chi2_per_pixel'],intervals,flush=True)
    return record

def benchmarks(engine):
    spec=importlib.util.spec_from_file_location('desi_resolution_cached',HERE/'inputs/desispec_resolution.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    checks={}
    for b,d in engine.bands.items():
        data=engine.raw[b+'_RESOLUTION'][0].astype(float);R=d['R'];w=d['w']
        official=module.Resolution(data).tocsr()
        assert (R-official).nnz==0
        vector=np.sin(np.arange(len(w))*.011)
        manual=np.zeros_like(vector)
        for k,offset in enumerate(range(5,-6,-1)):
            j=np.arange(len(w));i=j-offset;m=(i>=0)&(i<len(w))
            manual[i[m]]+=data[k,j[m]]*vector[j[m]]
        error=float(np.max(np.abs(manual-R@vector)))
        assert error<1e-12
        cols=[]
        for lam0 in [5200,5600,6800,7050]:
            if w[0]<lam0<w[-1]:
                j=np.argmin(abs(w-lam0));col=R[:,j].toarray().ravel();s=col.sum();mean=(col*w).sum()/s
                variance=(col*(w-mean)**2).sum()/s
                cols.append(dict(wave=float(w[j]),sum=float(s),mean_offset_A=float(mean-w[j]),moment_sigma_A=float(np.sqrt(max(0,variance)))))
        checks[b]=dict(official_matrix_exact=True,manual_max_abs_error=error,negative_entries=int((data<0).sum()),
            interior_row_sum_quantiles=np.quantile(np.asarray(R.sum(axis=1)).ravel()[10:-10],[0,.5,1]).tolist(),impulse_columns=cols)
    lines=[]
    for step in [.9,.3]:
        lam=np.arange(3750.,5550.,step)
        for sigma in [150.,222.26,320.]:
            operator=broadening_matrix(lam,sigma,np.full(len(lam),2.51),int(65/step))
            for center in [3950.,4300.,5175.]:
                intrinsic=2.51/2.354820045
                original=np.exp(-.5*((lam-center)/intrinsic)**2)/(intrinsic*np.sqrt(2*np.pi))
                broadened=operator@original
                area=np.trapz(broadened,lam);mu=np.trapz(lam*broadened,lam)/area
                var=np.trapz((lam-mu)**2*broadened,lam)/area
                recovered=np.sqrt(var)*C/center
                lines.append(dict(step_A=step,input_sigma=sigma,line_A=center,recovered_sigma=float(recovered),error_kms=float(recovered-sigma),area=float(area)))
    assert max(abs(x['error_kms']) for x in lines)<1.
    return dict(resolution=checks,analytic_gaussian_line_broadening=lines,template_labels=engine.labels,
        template_air_to_vac_offset_kms=np.quantile(C*np.log(engine.lam/np.interp(engine.lam,engine.lam,engine.lam/1.00028)),[0,.5,1]).tolist())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    e=Engine();checks=benchmarks(e)
    base={'windows':[['B',3800,4380],['R',4950,5500]],'degree':4}
    configs=[dict(base,name='primary_split'),dict(base,name='poly6',degree=6),
        dict(base,name='blue_only',windows=[['B',3800,4380]]),
        dict(base,name='red_only',windows=[['R',4950,5500]]),
        dict(base,name='broad_window',windows=[['B',3800,4380],['R',4400,5500]],degree=6,mgii_halfwidth=200),
        dict(base,name='old_templates',age_min=3.)]
    # A known mixture with smooth additive light tests finite identifiability and
    # optimizer recovery. It is explicitly an internal injection, not independent
    # astrophysical validation.
    truth=[250.,37.];design=e.design(*truth)
    synthetic={b:.7*A[:,13]+.3*A[:,22]+.8+.00005*(e.bands[b]['w']-6000) for b,A in design.items()}
    injected=fit_one(e,dict(base,name='noiseless_injection'),out,False,synthetic)
    checks['noiseless_injection']={k:injected[k] for k in ('sigma','velocity','chi2','ngood')}
    assert abs(injected['sigma']-truth[0])<.3 and abs(injected['velocity']-truth[1])<.3
    results=[]
    for cfg in configs:results.append(fit_one(e,cfg,out))
    # The .3A interpolation control checks sensitivity to numerical quadrature;
    # it does not manufacture independent high-resolution template information.
    ef=Engine(refine=3)
    refined=fit_one(ef,dict(base,name='sampling_0p3A'),out,False)
    checks['sampling_refinement']={k:refined[k] for k in ('sigma','velocity','chi2')}
    checks['sampling_refinement']['delta_sigma_kms']=refined['sigma']-results[0]['sigma']
    record=dict(target='L017819 / SDSS J1524+4409',targetid=39633153882587315,z_lens=Z,z_source=1.210,
        method='native-pixel exact DESI resolution; locally variance-corrected Gaussian stellar LOSVD; nonnegative E-MILES mixtures plus additive polynomials',
        checks=checks,results=results,elapsed_seconds=time.monotonic()-start,
        limitations=['Conditional diagonal pipeline noise, no calibrated full uncertainty',
        'Quasar continuum represented by additive polynomials, not physical quasar/FeII templates',
        'No aperture correction, rotation separation, Jeans inference, or new stellar mass',
        'Same DESI photons as literature/pipeline; differences are method controls, not independent measurements',
        'Template-LSF subtraction uses a local Gaussian approximation, validated only at stated lines and bounds'])
    (out/'result.json').write_text(json.dumps(record,indent=2))
    fig,axes=plt.subplots(3,1,figsize=(12,10),constrained_layout=True)
    for r in results:
        p=np.array(r['profile']);axes[0].plot(p[:,0],p[:,2]-r['chi2'],label=r['config']['name'])
    axes[0].set(xlim=(100,450),ylim=(0,20),xlabel='Stellar dispersion (km/s)',ylabel='Profile delta chi-square')
    axes[0].axhline(1,color='grey',lw=.7);axes[0].axhline(4,color='grey',lw=.7);axes[0].legend(ncol=3,fontsize=8)
    for value,color,label in [(222.26,'tab:blue','Guo'),(284.418,'tab:orange','FastSpec v3'),(317.619,'tab:red','FastSpec v2')]:
        axes[0].axvline(value,color=color,ls=':',lw=1)
    d=np.load(out/'primary_split_model.npz')
    for ax,b in zip(axes[1:],'BR'):
        m=d['band']==b;w=d['wave'][m];f=d['flux'][m];model=d['best_model'][m]
        ax.plot(w,f,c='grey',lw=.6,label='DESI native pixels');ax.plot(w,model,c='tab:red',lw=1,label='Best conditional stellar + polynomial model')
        ax.fill_between(w,model-1/d['weight'][m],model+1/d['weight'][m],color='tab:red',alpha=.15)
        ax.set(xlabel='Observed vacuum wavelength (Angstrom)',ylabel='Flux (native DESI units)',title=b+' absorption window');ax.legend(fontsize=8)
    fig.savefig(out/'dispersion_audit.png',dpi=150);plt.close(fig)

if __name__=='__main__':main()
