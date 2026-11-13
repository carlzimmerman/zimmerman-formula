"""Independent raw-band Sersic-shape fits with explicit masking limitations.
PSF-convolved pixel integrals; central pixels use angular/incomplete-gamma
integration rather than point sampling of a high-n cusp. No catalogue shape
prior is applied. Gaussian diagonal RMS weights remain conditional.
"""
import argparse,json,time,sys
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.special import gammaincinv,gammainc,gammaln,erf
from scipy.signal import fftconvolve
from scipy.ndimage import binary_dilation
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astropy.io import fits
ROOT=Path(__file__).resolve().parents[2]
INPUT=ROOT/'euclid_for_j0332_fit_2026_11_13/inputs'
DATA=INPUT/'dataset/Tile102034383RA0532498193624DECNEG0359643115588.fits'
BANDS=['VIS','NIR_Y','NIR_J','NIR_H']
PIX=.1
# Parameter order: x_west,y_north,ln(Re_major/arcsec),ln(n),q,PA_from_west.
LOW=np.array([-1.,-1.,np.log(.12),np.log(.4),.2,-np.pi])
HIGH=np.array([1.,1.,np.log(10.),np.log(12.),1.,np.pi])
NODES={k:np.polynomial.legendre.leggauss(k) for k in [3,6,8,16,24,48]}


class Renderer:
 def __init__(self,psf,shape=(100,100),fine=False):
  self.psf=np.asarray(psf,float)/np.sum(psf);self.shape=shape;self.pad=max(self.psf.shape)//2+1;self.fine=fine
  yy,xx=np.indices((shape[0]+2*self.pad,shape[1]+2*self.pad));self.X=(xx-self.pad-(shape[1]-1)/2)*PIX;self.Y=(yy-self.pad-(shape[0]-1)/2)*PIX
 def render(self,p):
  cx,cy,lr,ln,q,phi=p;re,n=np.exp(lr),np.exp(ln);co,si=np.cos(phi),np.sin(phi);b=gammaincinv(2*n,.5)
  norm=np.exp(2*n*np.log(b)-np.log(2*np.pi*q*n)-2*lr-gammaln(2*n))
  def surface(x,y):
   dx,dy=x-cx,y-cy;u=co*dx+si*dy;v=-si*dx+co*dy;r=np.sqrt(u*u+(v/q)**2)
   return norm*np.exp(-b*(r/re)**(1/n))
  def integrate(x,y,order):
   z,w=NODES[order];out=np.zeros_like(x)
   for a,wa in zip(z,w):
    for bb,wb in zip(z,w):out+=wa*wb*surface(x+a*PIX/2,y+bb*PIX/2)
   return out*PIX**2/4
  vals=integrate(self.X,self.Y,6 if self.fine else 3)
  inner=(self.X-cx)**2+(self.Y-cy)**2<.8**2
  vals[inner]=integrate(self.X[inner],self.Y[inner],16 if self.fine else 8)
  # A central 3x3 pixel block is integrated by exact radial gamma primitive
  # and Gaussian angular quadrature over each rectangle corner's two wedges.
  ix=int(round(cx/PIX+(self.shape[1]-1)/2))+self.pad
  iy=int(round(cy/PIX+(self.shape[0]-1)/2))+self.pad
  rows=np.arange(iy-1,iy+2);cols=np.arange(ix-1,ix+2)
  xs=(np.arange(ix-1,ix+3)-self.pad-self.shape[1]/2)*PIX-cx
  ys=(np.arange(iy-1,iy+3)-self.pad-self.shape[0]/2)*PIX-cy
  z,w=NODES[48 if self.fine else 24]
  def corner(x,y):
   if abs(x)<1e-15 or abs(y)<1e-15:return 0.
   ax,ay=abs(x),abs(y);sx,sy=np.sign(x),np.sign(y);split=np.arctan2(ay,ax);total=0.
   for left,right,edge in [(0.,split,'x'),(split,np.pi/2,'y')]:
    t=(right-left)*(z+1)/2+left;ct=sx*np.cos(t);st=sy*np.sin(t)
    ell2=(co*ct+si*st)**2+(-si*ct+co*st)**2/q**2
    rad=ax/np.cos(t) if edge=='x' else ay/np.sin(t)
    arg=b*(rad*np.sqrt(ell2)/re)**(1/n)
    total+=(right-left)/2*np.sum(w*gammainc(2*n,arg)/(2*np.pi*q*ell2))
   return sx*sy*total
  corners=np.array([[corner(x,y) for x in xs] for y in ys])
  vals[np.ix_(rows,cols)]=corners[1:,1:]-corners[:-1,1:]-corners[1:,:-1]+corners[:-1,:-1]
  conv=fftconvolve(vals,self.psf,mode='same')
  return conv[self.pad:self.pad+self.shape[0],self.pad:self.pad+self.shape[1]]


def physical(p):
 x,y,lr,ln,q,phi=p
 return dict(center_west_arcsec=float(x),center_north_arcsec=float(y),Re_major_arcsec=float(np.exp(lr)),Re_geometric_mean_arcsec=float(np.exp(lr)*np.sqrt(q)),n=float(np.exp(ln)),q=float(q),PA_from_west_deg=float(np.rad2deg(phi)%180))


def fit(data,noise,mask,renderer,start,fixed=None,max_nfev=150):
 fixed={} if fixed is None else dict(fixed);free=np.array([i for i in range(6) if i not in fixed]);p0=np.clip(np.asarray(start,float),LOW+1e-7,HIGH-1e-7)
 for i,v in fixed.items():p0[i]=v
 yy=data[mask];ww=1/noise[mask];last={}
 def unpack(z):p=p0.copy();p[free]=z;return p
 def evaluate(p):
  unit=renderer.render(p);a=unit[mask]*ww;c=ww;y=yy*ww
  H=np.array([[a@a,a@c],[a@c,c@c]]);coef=np.linalg.solve(H,np.array([a@y,c@y]))
  if coef[0]<=0:coef=np.array([0.,(c@y)/(c@c)])
  model=coef[0]*unit+coef[1];res=(model[mask]-yy)*ww
  last.update(p=p.copy(),coef=coef,model=model,res=res)
  return res
 opt=least_squares(lambda z:evaluate(unpack(z)),p0[free],bounds=(LOW[free],HIGH[free]),x_scale='jac',diff_step=2e-4,
                   ftol=2e-7,xtol=2e-7,gtol=2e-6,max_nfev=max_nfev)
 p=unpack(opt.x);res=evaluate(p);covsmall=np.linalg.pinv(opt.jac.T@opt.jac,rcond=1e-11)
 cov=np.zeros((6,6));cov[np.ix_(free,free)]=covsmall
 pars=physical(p)
 return dict(parameters=p.tolist(),physical=pars,amplitude_total_native=float(last['coef'][0]),sky_native=float(last['coef'][1]),
             chi2=float(res@res),n_pixels=int(mask.sum()),dof=int(mask.sum()-len(free)-2),success=bool(opt.success),message=str(opt.message),nfev=opt.nfev,
             fixed={str(i):v for i,v in fixed.items()},covariance_shape_coordinates=cov.tolist(),
             shape_bound_distances=np.minimum(p-LOW,HIGH-p).tolist(),model=last['model'],mask=mask)


def compact(r):return {k:v for k,v in r.items() if k not in ['model','mask']}


def profiles(data,noise,mask,renderer,best):
 p=np.array(best['parameters']);C=np.array(best['covariance_shape_coordinates'])[np.ix_([3,2],[3,2])]
 # Log n/Re plane; profile all other nonlinear and linear nuisance parameters.
 eig,vec=np.linalg.eigh(C);eig=np.maximum(eig,1e-10);L=vec@np.diag(np.sqrt(eig))
 rows=[];extent=3.;previous=p.copy()
 for u in np.linspace(-extent,extent,7):
  for v in np.linspace(-extent,extent,7):
   d=L@np.array([u,v]);ln,lr=p[3]+d[0],p[2]+d[1]
   if not LOW[3]<ln<HIGH[3] or not LOW[2]<lr<HIGH[2]:
    rows.append({'u':float(u),'v':float(v),'outside_parameter_bounds':True});continue
   r=fit(data,noise,mask,renderer,previous,fixed={2:lr,3:ln},max_nfev=70)
   previous=np.array(r['parameters']);rows.append({'u':float(u),'v':float(v),'ln_n':float(ln),'ln_Re_major':float(lr),
       'n':float(np.exp(ln)),'Re_major_arcsec':float(np.exp(lr)),'chi2':r['chi2'],'delta_chi2':r['chi2']-best['chi2'],'success':r['success'],'nfev':r['nfev']})
 valid=[r for r in rows if not r.get('outside_parameter_bounds') and r['delta_chi2']<12]
 if len(valid)>=6:
  xy=np.array([[r['ln_n']-p[3],r['ln_Re_major']-p[2]] for r in valid]);values=np.array([r['delta_chi2'] for r in valid])
  design=np.column_stack([xy[:,0]**2,2*xy[:,0]*xy[:,1],xy[:,1]**2,xy[:,0],xy[:,1],np.ones(len(xy))])
  coef=np.linalg.lstsq(design,values,rcond=None)[0];H=np.array([[coef[0],coef[1]],[coef[1],coef[2]]]);cp=np.linalg.pinv(H)
  corr=cp[0,1]/np.sqrt(abs(cp[0,0]*cp[1,1]));rms=np.sqrt(np.mean((design@coef-values)**2))
  prof={'covariance_log_n_log_Re_from_profile_quadratic':cp.tolist(),'correlation_log_n_log_Re':float(corr),'profile_quadratic_RMS_delta_chi2':float(rms),'quadratic_eigenvalues':np.linalg.eigvalsh(H).tolist()}
 else:prof={'profile_quadratic_unavailable':'too few in-bounds points'}
 return {'rows':rows,'coordinate_order':['ln_n','ln_Re_major'],'initial_local_covariance':C.tolist(),**prof}


def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);starttime=time.monotonic();archive={};results=[];diagnostics={}
 source=fits.getdata(INPUT/'dataset/segmentation/source_binary.fits')>0;artifact=fits.getdata(INPUT/'dataset/segmentation/artefact_binary.fits')>0
 yy,xx=np.indices(source.shape);X=(xx-49.5)*PIX;Y=(yy-49.5)*PIX
 cat=json.loads((INPUT/'results/coolest_sersic.json').read_text())['lensing_entities'][0]['light_model'][0]['parameters'];get=lambda k:cat[k]['point_estimate']['value']
 initial=np.array([get('center_x'),get('center_y'),np.log(get('theta_eff')/np.sqrt(get('q'))),np.log(get('n')),get('q'),np.pi/2+np.deg2rad(get('phi'))])
 radius=np.hypot(X-initial[0],Y-initial[1]);aperture=radius<4.5
 # Analytic Gaussian-profile/PSF convolution benchmark, independent erf image.
 gp=.18;sig=.35;z=np.arange(-15,16)*PIX;gx,gy=np.meshgrid(z,z);psfg=np.exp(-(gx*gx+gy*gy)/(2*gp*gp));psfg/=psfg.sum()
 pg=np.array([-.173,-.267,np.log(sig*np.sqrt(2*np.log(2))),np.log(.5),1.,.4]);gauss=Renderer(psfg).render(pg)
 se=np.sqrt(sig*sig+gp*gp);cx,cy=pg[:2]
 exact=.25*(erf((X-cx+PIX/2)/(np.sqrt(2)*se))-erf((X-cx-PIX/2)/(np.sqrt(2)*se)))*(erf((Y-cy+PIX/2)/(np.sqrt(2)*se))-erf((Y-cy-PIX/2)/(np.sqrt(2)*se)))
 err=float(np.max(abs(gauss-exact))/np.max(exact));assert err<1e-5
 diagnostics['gaussian_PSF_convolution_peak_normalized_max_error']=err
 with fits.open(DATA) as hd,fits.open(INPUT/'results/model.fits') as modelhd:
  for band in BANDS:
   data=np.array(hd[band+'_BGSUB'].data,float);noise=np.array(hd[band+'_RMS'].data,float);psf=np.array(hd[band+'_PSF'].data,float)
   rawsum=float(psf.sum());renderer=Renderer(psf);fine=Renderer(psf,fine=True);valid=aperture&np.isfinite(data)&np.isfinite(noise)&(noise>0)
   bad=source|artifact;positive=np.maximum(psf,0.);positive/=positive.sum();overlap=fftconvolve(bad.astype(float),positive,mode='same')
   masks={f'dilation{d}':valid&~binary_dilation(bad,iterations=d) for d in [1,2,3]}
   masks['halo003']=valid&~bad&(overlap<.03);masks['halo001']=valid&~bad&(overlap<.01)
   masks['source_subtracted']=valid&~binary_dilation(artifact,iterations=2)
   template=np.array(modelhd[band+'_GALAXY_1'].data,float)
   diag={'native_BUNIT':hd[band+'_BGSUB'].header.get('BUNIT'),'MAGZERO':hd[band+'_BGSUB'].header.get('MAGZERO'),'pixel_scale_arcsec':PIX,
         'PSF_raw_sum':rawsum,'PSF_min':float(psf.min()),'PSF_FWHM_arcsec':float(hd[band+'_PSF'].header['FWHM']),
         'mask_counts':{name:{'total':int(m.sum()),'inside_05arcsec':int(np.sum(m&(radius<.5))),'inside_1arcsec':int(np.sum(m&(radius<1)))} for name,m in masks.items()},
         'full_PSF_support_mask_counts':{'total':int(np.sum(valid&~bad&(overlap<1e-8))),'inside_2arcsec':int(np.sum(valid&~bad&(overlap<1e-8)&(radius<2)))}}
   archive[band+'_data']=data;archive[band+'_noise']=noise;archive[band+'_source_template']=template;archive[band+'_PSF_overlap']=overlap
   # Synthetic recovery uses a finer numerical generator, real band PSF and actual masked geometry.
   truth=np.array([-.173,-.267,np.log(.9),np.log(4.2),.72,.7]);synthetic=fine.render(truth)+.0001
   synstart=np.array([-.22,-.3,np.log(1.3),np.log(2.),.85,1.])
   syn=fit(synthetic,np.full_like(noise,1e-4),masks['dilation2'],renderer,synstart,max_nfev=180)
   synerr=np.array(syn['parameters'])-truth
   diag['synthetic_noiseless_recovery']={'truth':physical(truth),'fit':compact(syn),'shape_coordinate_error':synerr.tolist()}
   assert syn['success'] and max(abs(synerr[:2]))<.002 and max(abs(synerr[2:]))<.015
   bandfits={}
   for name,mask in masks.items():
    used=data-template if name=='source_subtracted' else data
    starts=[initial, np.array([*initial[:3],np.log(3.),.8,initial[5]])]
    fitted=[fit(used,noise,mask,renderer,p,max_nfev=180) for p in starts]
    best=min(fitted,key=lambda r:r['chi2']);best['all_start_solutions']=[{'parameters':r['parameters'],'chi2':r['chi2'],'success':r['success']} for r in fitted]
    best.update(band=band,mask_name=name,source_subtraction_conditional=name=='source_subtracted',PSF_overlap_threshold=.03 if name=='halo003' else (.01 if name=='halo001' else None))
    exact_model=best['amplitude_total_native']*fine.render(np.array(best['parameters']))+best['sky_native']
    numerical=(exact_model-best['model'])[mask]/noise[mask]
    best['integration_convergence']={'max_abs_pixel_difference_in_RMS':float(np.max(abs(numerical))), 'RMS_pixel_difference_in_RMS':float(np.sqrt(np.mean(numerical*numerical))),'delta_chi2_at_fixed_parameters':float(np.sum(((exact_model[mask]-used[mask])/noise[mask])**2)-best['chi2'])}
    archive[band+'_'+name+'_model']=best['model'];archive[band+'_'+name+'_mask']=mask
    results.append(compact(best));bandfits[name]=best
    print(json.dumps({'band':band,'mask':name,'physical':best['physical'],'chi2':best['chi2'],'pixels':best['n_pixels'],'success':best['success'],'numerics':best['integration_convergence']}),flush=True)
    (out/'progress.json').write_text(json.dumps({'fits':results,'diagnostics':diagnostics},indent=2)+'\n')
   control=fit(data,noise,masks['dilation2'],renderer,np.array(bandfits['dilation2']['parameters']),fixed={3:np.log(4.)},max_nfev=180)
   diag['fixed_n4_control']=compact(control)
   diag['profile_dilation2']=profiles(data,noise,masks['dilation2'],renderer,bandfits['dilation2'])
   diagnostics[band]=diag
   (out/'progress.json').write_text(json.dumps({'fits':results,'diagnostics':diagnostics},indent=2)+'\n')
   print('COMPLETED_BAND',band,flush=True)
 result={'assertion_tested':'Independent free raw-band elliptical Sersic lens-light fits in VIS/Y/J/H with source/artefact masking controls and conditional source-subtraction alternative; finite integration/synthetic benchmarks and n-Re joint profile diagnostics.',
         'parameter_order':['center_west_arcsec','center_north_arcsec','ln_Re_major_arcsec','ln_n','axis_ratio_q','PA_from_west_radians'],
         'fit_bounds':{'lower':LOW.tolist(),'upper':HIGH.tolist()},'fits':results,'diagnostics':diagnostics,'seconds':time.monotonic()-starttime,
         'non_claims':['No catalogue non-VIS fixed shape is used as an independent measurement.','Only numerical starting values come from catalogue VIS shape; no published n/Re priors are imposed.','Dilation1-3pixel masks do not remove all broad NIR PSF spillover.','Halo thresholds constrain geometric PSF overlap of segmentation, not an exact source-flux contamination bound.','The source-subtracted alternative is conditional on the released model and is secondary.','Diagonal released RMS and ignored resampling correlations mean profile intervals are conditional statistical diagnostics.','Single Sersic light shape does not measure a stellar M/L gradient or an AQUAL mass profile by itself.','Total-flux amplitudes extrapolate the model beyond the aperture; do not equate them to independent SED mass constraints.']}
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');np.savez_compressed(out/'models_masks.npz',**archive)
 fig,axes=plt.subplots(3,4,figsize=(14,10),constrained_layout=True)
 for j,band in enumerate(BANDS):
  row=next(r for r in results if r['band']==band and r['mask_name']=='dilation2');data=archive[band+'_data'];model=archive[band+'_dilation2_model'];mask=archive[band+'_dilation2_mask'];noise=archive[band+'_noise'];vmax=np.percentile(data[mask],99)
  axes[0,j].imshow(np.arcsinh(data/max(vmax/10,1e-10)),origin='lower',extent=[-5,5,-5,5],cmap='magma');axes[0,j].contour(X,Y,mask,levels=[.5],colors='cyan',linewidths=.5)
  axes[1,j].imshow(np.arcsinh(model/max(vmax/10,1e-10)),origin='lower',extent=[-5,5,-5,5],cmap='magma')
  im=axes[2,j].imshow(np.where(mask,(data-model)/noise,np.nan),origin='lower',extent=[-5,5,-5,5],cmap='RdBu_r',vmin=-4,vmax=4)
  axes[0,j].set_title(band+' data + fit mask');axes[1,j].set_title(f"n={row['physical']['n']:.2f}, Re_major={row['physical']['Re_major_arcsec']:.2f} arcsec");axes[2,j].set_title('Masked residual / RMS');fig.colorbar(im,ax=axes[2,j],shrink=.7)
  for ax in axes[:,j]:ax.set_xlabel('West (arcsec)');ax.set_ylabel('North (arcsec)')
 fig.savefig(out/'raw_band_fits.png',dpi=160);plt.close(fig)
 fig,axes=plt.subplots(1,2,figsize=(12,5),constrained_layout=True)
 markers={'dilation1':'o','dilation2':'s','dilation3':'^','halo003':'D','halo001':'x','source_subtracted':'*'}
 for j,band in enumerate(BANDS):
  color=f'C{j}'
  for r in results:
   if r['band']==band:axes[0].scatter(r['physical']['n'],r['physical']['Re_major_arcsec'],color=color,marker=markers[r['mask_name']],s=65,label=band+' '+r['mask_name'])
  prof=diagnostics[band]['profile_dilation2'];rows=[x for x in prof['rows'] if not x.get('outside_parameter_bounds')]
  if len(rows)>=6:
   axes[1].tricontour([x['n'] for x in rows],[x['Re_major_arcsec'] for x in rows],[x['delta_chi2'] for x in rows],levels=[2.3,6.17],colors=color)
   axes[1].plot([],[],color=color,label=band)
 axes[0].set_xlabel('Sersic n');axes[0].set_ylabel('Major-axis Re (arcsec)');axes[0].set_title('Mask/source-subtraction dependence');axes[0].legend(fontsize=6,ncol=2)
 axes[1].set_xlabel('Sersic n');axes[1].set_ylabel('Major-axis Re (arcsec)');axes[1].set_title('Joint profile Δchi²=2.3,6.17; dilation2');axes[1].legend()
 fig.savefig(out/'shape_profiles.png',dpi=170);plt.close(fig)
 print(json.dumps({'seconds':result['seconds'],'n_fits':len(results),'gaussian_check':err}),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
