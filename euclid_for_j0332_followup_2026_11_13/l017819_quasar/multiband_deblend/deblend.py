"""Fixed-SIE/light multiband deblend audit; all photometry in microJy.
No stellar-population or physical-mass inference.
"""
import sys,json,csv,time,argparse
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy import sparse,linalg,optimize
from scipy.signal import fftconvolve
from astropy.io import fits
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parent;T=B.parent
sys.path.insert(0,str(T/'host_control'));from fit_host_v4 import Host,Renderer,point
X,N=np.meshgrid((np.arange(100)-49.5)*.1,(np.arange(100)-49.5)*.1)

def source_matrix(fn,center,psf,dx,dn,ns=21,h=.06,ss=2):
 rows=[];cols=[];vals=[];foot=np.zeros((100,100))
 for i in range(ss):
  for j in range(ss):
   xx=X-dx+((j+.5)/ss-.5)*.1;nn=N-dn+((i+.5)/ss-.5)*.1;ax,an=fn(xx,nn);u=(xx-ax-center[0])/h+(ns-1)/2;v=(nn-an-center[1])/h+(ns-1)/2;ix=np.floor(u).astype(int);iy=np.floor(v).astype(int);fx=u-ix;fy=v-iy;foot+=((u>=0)&(u<=ns-1)&(v>=0)&(v<=ns-1))/ss**2
   for a,b,w in [(0,0,(1-fx)*(1-fy)),(1,0,fx*(1-fy)),(0,1,(1-fx)*fy),(1,1,fx*fy)]:
    cx=ix+a;cy=iy+b;ok=(cx>=0)&(cx<ns)&(cy>=0)&(cy<ns);rows.append(np.flatnonzero(ok));cols.append(cy[ok]*ns+cx[ok]);vals.append(w[ok]/ss**2)
 A=sparse.coo_matrix((np.concatenate(vals),(np.concatenate(rows),np.concatenate(cols))),shape=(10000,ns*ns)).toarray().reshape(100,100,ns*ns)
 return fftconvolve(A,psf[:,:,None],mode='same',axes=(0,1)).reshape(10000,ns*ns),foot

def linear_fit(D,y,noise,R,logdetR,host=True):
 W=D/noise[:,None];z=y/noise;H0=W.T@W;rhs=W.T@z;n=R.shape[0] if host else 0
 def ev(reg,detail=False):
  Q=linalg.block_diag(np.exp(reg)*R,np.diag([1e-8]*3+[.01])) if host else np.diag([1e-8]*3+[.01]);cf=linalg.cho_factor(H0+Q,lower=True);c=linalg.cho_solve(cf,rhs);res=z-W@c;chi=float(res@res);pen=float(c@Q@c);ldh=2*np.log(np.diag(cf[0])).sum();ldq=(n*reg+logdetR if host else 0)+3*np.log(1e-8)+np.log(.01);score=-.5*(chi+pen+ldh-ldq)
  r={'score':float(score),'chi2':chi,'prior_penalty':pen,'log_source_precision':float(reg),'lens_A_B_sky_microJy':c[-4:].tolist(),'positive_foreground':bool(c[-4]>0),'positive_both_quasars':bool(np.all(c[-3:-1]>0))}
  if detail:
   r['model']=D@c;r['coef']=c
   if host:
    std=np.sqrt(np.maximum(np.diag(linalg.cho_solve(cf,np.eye(n+4)))[:n],0));s=c[:n];edge=np.ones((21,21),bool);edge[1:-1,1:-1]=False;r.update(negative_source_fraction=float(np.mean(s<0)),source_nodes_negative_beyond_3sigma=int(np.sum(s < -3*std)),source_edge_abs_fraction=float(abs(s.reshape(21,21)[edge]).sum()/max(abs(s).sum(),1e-30)))
  return r
 if host:opt=optimize.minimize_scalar(lambda z:-ev(z)['score'],bounds=(-12,18),method='bounded',options={'xatol':.08});return ev(opt.x,True)
 return ev(0,True)

def main(output):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);start=time.time();obj=Host();info=json.loads((T/'inputs/dataset/info.json').read_text());ap=(X-info['mask_centre'][1])**2+(N+info['mask_centre'][0])**2<info['mask_radius']**2;art=fits.getdata(T/'inputs/dataset/segmentation/artefact_binary.fits')>0;fitmask=(np.hypot(X+.15,N-.05)<3)&~art
 cat={r['waveband']:r for r in csv.DictReader(open(T/'inputs/results/magnitudes.csv'))};offsets={r['waveband']:r for r in csv.DictReader(open(T/'inputs/results/astrometric_offsets.csv'))};hd=fits.open(next((T/'inputs/dataset').glob('Tile*.fits')));pre=fits.open(T/'inputs/results/pre_psf.fits');results=[];saved={};cal={};fig,axes=plt.subplots(3,3,figsize=(14,11));bands=[z.name[:-6] for z in hd if z.name.endswith('_BGSUB')];assert len(bands)==9
 # Exact continuous-boundary/coordinate control of independently built source operator.
 fn,_=obj.rays(np.array(json.loads((T/'host_control/run_04/result.json').read_text())['chosen']['params']));test,_=source_matrix(fn,obj.center,obj.psf,0,0);obj.operator(fn);err=float(np.max(abs(test-obj.fullB.toarray())));assert err<1e-12
 for fixrun in ['run_04','run_03']:
  f=json.loads((T/'host_control'/fixrun/'result.json').read_text())['chosen'];p=np.array(f['params']);lp=obj.startlight.copy();lp[2:6]=p[:4];fn,shear=obj.rays(p);center=obj.center
  for ib,band in enumerate(bands):
   key=band.lower();data=hd[band+'_BGSUB'].data.astype(float);noise=hd[band+'_RMS'].data.astype(float);zp=float(hd[band+'_BGSUB'].header['MAGZERO']);factor=10**((23.9-zp)/2.5);data*=factor;noise*=factor;ps=hd[band+'_PSF'].data.astype(float);rawsum=ps.sum();ps/=rawsum;mask=fitmask&np.isfinite(data)&np.isfinite(noise)&(noise>0);old=cat[key];off=offsets.get(key,{});dx=float(off.get('grid_offset_x',0));dn=-float(off.get('grid_offset_y',0));choices=[('zero',0.,0.)]
   if abs(dx)+abs(dn)>1e-7:choices += [('catalog_sign',dx,dn),('opposite_sign',-dx,-dn)]
   variants=[]
   for label,xx,nn in choices:
    host,foot=source_matrix(fn,center,ps,xx,nn);shiftlp=lp.copy();shiftlp[:2]+=[xx,nn];lens=Renderer(ps).render(shiftlp);pa=point(ps,*(obj.A+[xx,nn]));pb=point(ps,*(obj.C+[xx,nn]));D=np.column_stack([host[mask.ravel()],lens[mask],pa[mask],pb[mask],np.ones(mask.sum())]);r=linear_fit(D,data[mask],noise[mask],obj.R,obj.logdetR);control=linear_fit(D[:,-4:],data[mask],noise[mask],obj.R,obj.logdetR,False)
    intrinsic=Renderer(np.ones((1,1)),fine=True).render(shiftlp);fraction=float(intrinsic[ap].sum());r.update(offset_fixture=label,offset_west_north_arcsec=[xx,nn],aperture_fraction=fraction,foreground_aperture_microJy=float(r['lens_A_B_sky_microJy'][0]*fraction),point_only_foreground_aperture_microJy=float(control['lens_A_B_sky_microJy'][0]*fraction),point_only_chi2=control['chi2'],point_only_positive_foreground=control['positive_foreground'],source_footprint_fraction=float(foot[mask].mean()))
    variants.append(r)
   # Prefer validpositiveforeground; preserveeveryalternative.
   usable=[r for r in variants if r['positive_foreground']];chosen=max(usable or variants,key=lambda r:r['score']);catalogflux=float(old['lens_flux']);releasedmap=float(pre[band+'_GALAXY_0'].data[ap].sum()*factor);chosen.update(foreground_ratio_to_catalogue=chosen['foreground_aperture_microJy']/catalogflux)
   row={'fixture':fixrun,'band':band,'catalogue_lens_flux_microJy':catalogflux,'catalogue_max_lh_microJy':float(old['lens_flux_max_lh']),'released_prePSF_sum_same_aperture_microJy':releasedmap,'released_map_to_catalogue_ratio':releasedmap/catalogflux,'n_pixels':int(mask.sum()),'chosen':{k:v for k,v in chosen.items() if k not in ['model','coef']},'offset_variants':[{k:v for k,v in r.items() if k not in ['model','coef']} for r in variants]};results.append(row);cal[band]={'MAGZERO':zp,'BUNIT':hd[band+'_BGSUB'].header.get('BUNIT'),'microJy_per_native_unit':factor,'PSF_shape':list(ps.shape),'raw_PSF_sum':float(rawsum),'actual_aperture_pixels':int(ap.sum())};saved[fixrun+'_'+band+'_model_valid']=chosen['model'];saved[fixrun+'_'+band+'_coef']=chosen['coef']
   if fixrun=='run_04':
    ax=axes.flat[ib];model=np.full((100,100),np.nan);model[mask]=chosen['model'];ax.imshow(np.where(mask,(data-model)/noise,np.nan),origin='lower',vmin=-4,vmax=4,cmap='RdBu_r');ax.set_xlim(20,80);ax.set_ylim(20,80);ax.set_title(band+' residual/RMS; F/Fcat={:.2f}'.format(chosen['foreground_ratio_to_catalogue']))
   print(json.dumps({'fixture':fixrun,'band':band,'foreground_aperture_microJy':chosen['foreground_aperture_microJy'],'ratio':chosen['foreground_ratio_to_catalogue'],'positive':chosen['positive_foreground'],'offset':chosen['offset_fixture'],'chi2':chosen['chi2']}),flush=True);(out/'progress.json').write_text(json.dumps({'seconds':time.time()-start,'completed':results,'calibration':cal},indent=2))
 result={'assertion_tested':'Nineband fixedSIE/light conditionaldeblend with actualPSFs,freequasar/hostcolors andfiniteaperturecomparison','seconds':time.time()-start,'independent_source_operator_vs_reference_max_error':err,'records':results,'calibration':cal,'source_grid':{'ns':21,'step_arcsec':.06,'supersample':2},'non_claims':['No newstellarSED/IMF/massestimate','FixedSIE/lightfixturesareconditionalnotindependentprofiledata','SourceGaussiannegativity/finitecoverage anddiagonalnoise remainassumptions','Offsetsignsearchedasdiscretesensitivitynotastrometrictruth']};(out/'result.json').write_text(json.dumps(result,indent=2));np.savez_compressed(out/'models.npz',**saved);fig.tight_layout();fig.savefig(out/'nineband_residuals.png',dpi=150)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
