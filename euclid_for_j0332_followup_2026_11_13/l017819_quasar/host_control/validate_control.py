import sys,json,argparse,numpy as np
from pathlib import Path
from scipy.signal import fftconvolve
from scipy.optimize import minimize_scalar
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B));from fit_host_v2 import Host,sie_deflection
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
r=json.loads((B/'run_02/result.json').read_text());v=np.array(r['chosen']['params']);obj=Host();base=obj.run(v,True)
x=np.array([.4,-.7,.5]);y=np.array([.8,.4,-.1]);a,b=sie_deflection(x,y,.8,.9999999,0,0,0,0,0);sphere=.8*np.stack([x,y])/np.hypot(x,y);sphereerr=float(np.max(abs(np.stack([a,b])-sphere)));assert sphereerr<1e-6
# Independent FFT convolution check of sparse imagePSF matrix on deterministic nontrivial image.
ii,jj=np.indices((100,100));test=np.sin(ii*.3)*np.cos(jj*.2);conv=(obj.P@test.ravel()).reshape(100,100);fft=fftconvolve(test,obj.psf,mode='same');err=float(np.max(abs(conv-fft)));assert err<1e-12
# Reconstruct a positivehost synthetic image in sameforwardbasis; fixedgeometry posterior residual check.
n=obj.ns**2;sy,sx=np.indices((obj.ns,obj.ns));source=.15*np.exp(-((sx-8)**2+(sy-8)**2)/8);lp=obj.startlight.copy();lp[2:6]=v[:4];lens=obj.renderer.render(lp);D=np.column_stack([obj.B,lens[obj.mask],obj.points[0,obj.mask],obj.points[1,obj.mask],np.ones(obj.mask.sum())]);truth=np.r_[source.ravel(),200,38,19,.001];synthetic=D@truth;obj.data=obj.data.copy();obj.data[obj.mask]=synthetic;obj.noise=obj.noise.copy();obj.noise[obj.mask]=1e-4;syn=obj.run(v);assert syn['chi2']/obj.mask.sum()<1e-3
checks=[]
for ns,h,ss in [(17,.06,2),(21,.06,1),(21,.045,2)]:
 z=Host(ns,h);z.ss=ss
 opt=minimize_scalar(lambda reg:-z.run(np.r_[v[:7],reg])['score'],bounds=(-2,13),method='bounded',options={'xatol':.05});rr=z.run(np.r_[v[:7],opt.x]);rr['supersample']=ss;checks.append(rr)
record={'purpose':'Exactforwardimplementation checks and fixedgeometrysourceprecision/sampling sensitivity, notfullfit validation','SISlimit_max_arcsec_error':sphereerr,'sparsePSF_vsFFT_max_absolute_error':err,'synthetic_sameforward_fixedgeometry_chi2':syn['chi2'],'synthetic_pixels':syn['mask_pixels'],'synthetic_non_claim':'NoindependentPSF/noise/modelmismatch recovery or nonlinearparameter recovery','source_sampling_regoptimized_checks':checks};(out/'result.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
