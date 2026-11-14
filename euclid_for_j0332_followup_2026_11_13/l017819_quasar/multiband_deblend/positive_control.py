"""Convex nonnegativehost/lens/quasars MAP sensitivity at frozenGaussianprecision.
Not a positivity-constrained evidence and no precision reoptimization.
"""
import sys,json,time,argparse
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy import linalg,optimize
from astropy.io import fits
from deblend import B,T,X,N,Host,Renderer,point,source_matrix

def main(output):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);t=time.time();old=json.loads((B/'run_01/result.json').read_text());obj=Host();hd=fits.open(next((T/'inputs/dataset').glob('Tile*.fits')));art=fits.getdata(T/'inputs/dataset/segmentation/artefact_binary.fits')>0;mask0=(np.hypot(X+.15,N-.05)<3)&~art;records=[]
 for row in old['records']:
  c=row['chosen'];p=np.array(json.loads((T/'host_control'/row['fixture']/'result.json').read_text())['chosen']['params']);fn,_=obj.rays(p);lp=obj.startlight.copy();lp[2:6]=p[:4];dx,dn=c['offset_west_north_arcsec'];lp[:2]+=[dx,dn];band=row['band'];fac=old['calibration'][band]['microJy_per_native_unit'];data=hd[band+'_BGSUB'].data.astype(float)*fac;noise=hd[band+'_RMS'].data.astype(float)*fac;ps=hd[band+'_PSF'].data.astype(float);ps/=ps.sum();mask=mask0&np.isfinite(data)&np.isfinite(noise)&(noise>0);host,_=source_matrix(fn,obj.center,ps,dx,dn);lens=Renderer(ps).render(lp);pa=point(ps,*(obj.A+[dx,dn]));pb=point(ps,*(obj.C+[dx,dn]));D=np.column_stack([host[mask.ravel()],lens[mask],pa[mask],pb[mask],np.ones(mask.sum())]);W=D/noise[mask,None];y=data[mask]/noise[mask];U=linalg.block_diag(np.exp(c['log_source_precision']/2)*linalg.cholesky(obj.R,lower=False),np.diag([1e-4]*3+[.1]));A=np.vstack([W,U]);z=np.r_[y,np.zeros(U.shape[0])];lower=np.r_[np.zeros(444),-np.inf];opt=optimize.lsq_linear(A,z,bounds=(lower,np.full(445,np.inf)),method='bvls',tol=1e-8,max_iter=250);coef=opt.x;res=y-W@coef;flux=float(coef[-4]*c['aperture_fraction']);r={'fixture':row['fixture'],'band':band,'success':bool(opt.success),'status':int(opt.status),'message':str(opt.message),'iterations':int(opt.nit),'optimality':float(opt.optimality),'chi2':float(res@res),'delta_chi2_from_Gaussian':float(res@res-c['chi2']),'foreground_aperture_microJy':flux,'ratio_to_catalogue':flux/row['catalogue_lens_flux_microJy'],'ratio_to_Gaussian_foreground':flux/c['foreground_aperture_microJy'],'lens_A_B_sky_microJy':coef[-4:].tolist(),'host_nodes_at_lower_bound':int(np.sum(coef[:441]<1e-10)),'frozen_log_source_precision':c['log_source_precision'],'offset':c['offset_fixture']};records.append(r);print(json.dumps(r),flush=True);(out/'progress.json').write_text(json.dumps({'seconds':time.time()-t,'records':records},indent=2))
 (out/'result.json').write_text(json.dumps({'assertion_tested':'18 convexnonnegativehost/lens/quasar MAPcontrols atfixedpriorprecision/geometry/offset','seconds':time.time()-t,'records':records,'non_claims':['No positivemarginalevidence or recalibrateduncertainty','Sourceprecision/geometrynotreoptimizedunderpositivity','A nonnegativehostfit maystillcontainincorrectforegroundmodel or sourceidentity']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
