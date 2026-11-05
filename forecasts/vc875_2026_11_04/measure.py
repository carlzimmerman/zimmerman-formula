"""Public compact-array VC875 cube: continuum-subtracted moment0 exponential fit.
Conditional morphology approximation; not a mass map or full 3D kinematic fit.
"""
import json,sys
from pathlib import Path
import numpy as np
from astropy.io import fits
from scipy.ndimage import gaussian_filter
from scipy.optimize import least_squares
from scipy.integrate import quad
p=Path(__file__).resolve().parent;out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
f=next((p/'inputs').glob('*spw25.cube.I.pbcor.fits'))
h=fits.getheader(f);cube=np.squeeze(fits.getdata(f));pb=np.squeeze(fits.getdata(str(f).replace('pbcor.fits','pb.fits.gz')))
freq=h['CRVAL3']+(np.arange(len(cube))+1-h['CRPIX3'])*h['CDELT3'];nu=1900.5369e9/(1+4.5505)
v=299792.458*(nu-freq)/nu;dv=abs(v[1]-v[0]);pix=abs(h['CDELT1'])*3600
y,x=np.indices(cube.shape[1:]);r=np.hypot(x-250,y-250)*pix
off=abs(v)>400;line=abs(v)<260
baseline=np.nanmean(cube[off],axis=0);mom=np.nansum(cube[line]-baseline,axis=0)*dv
beam=1.1331*h['BMAJ']*h['BMIN']*3600**2;bp=beam/pix**2
noise=float(np.nanmedian(np.nanstd((cube*pb)[:,(r>3)&(r<5)],axis=1)))
mnoise=float(np.nanstd(mom[(r>3)&(r<5)]))
flux={str(rad):float(np.nansum(mom[r<rad])/bp) for rad in [1,1.5,2,2.5]}
sl=np.s_[215:286,215:286];data=mom[sl];xx=(x[sl]-250)*pix;yy=(y[sl]-250)*pix
sigbeam=np.sqrt(h['BMAJ']*h['BMIN'])*3600/2.35482/pix
def model(a):
 F,rd,q,pa,dx,dy,bg=a;ang=np.deg2rad(pa)
 major=(xx-dx)*np.sin(ang)+(yy-dy)*np.cos(ang)
 minor=(xx-dx)*np.cos(ang)-(yy-dy)*np.sin(ang)
 rad=np.sqrt(major**2+(minor/q)**2)
 im=F/(2*np.pi*rd**2*q)*np.exp(-rad/rd)*beam
 return gaussian_filter(im,sigbeam)+bg
fits_=[least_squares(lambda a:((model(a)-data)/mnoise).ravel(),[3,.3,.65,pa,0,0,0],bounds=([.1,.03,.2,0,-.4,-.4,-.1],[10,1.5,1,180,.4,.4,.1]),max_nfev=300) for pa in [40,100,147]]
best=min(fits_,key=lambda a:sum(a.fun*a.fun));F,rd,q,pa,dx,dy,bg=best.x
z=4.5505;dc=299792.458/68.56427*quad(lambda z:1/np.sqrt(.2976016*(1+z)**3+1-.2976016),0,z)[0]
scale=dc/(1+z)*1000/206264.806;dl=dc*(1+z)
result=dict(z=z,kpc_per_arcsec=scale,dl_mpc=dl,flux_apertures_Jykms=flux,fit_flux=float(F),fit_Re_arcsec=float(rd*1.678),fit_Re_kpc=float(rd*1.678*scale),fit_axis_ratio=float(q),fit_sky_PA_deg=float((180-pa)%180),fit_center_pixel_axes_arcsec=[float(dx),float(dy)],fit_background=float(bg),fit_success=bool(best.success),fit_residual_rms=float(np.std(model(best.x)-data)),moment_noise_Jykmsbeam=mnoise,noise_Jybeam_per_channel=noise,channel_width_kms=dv,noise_mJybeam_10kms=noise*1000*np.sqrt(dv/10),beam_arcsec=[h['BMAJ']*3600,h['BMIN']*3600],line_window_kms=260,continuum_window_min_kms=400,L_CII_aperture=1.04e-3*flux['1.5']*(nu/1e9)*dl**2)
(out/'measurement.json').write_text(json.dumps(result,indent=2));np.savez_compressed(out/'moment_maps.npz',data=data,model=model(best.x),residual=data-model(best.x),x_arcsec=xx,y_arcsec=yy)
print(json.dumps(result,indent=2));assert best.success and F>0 and noise>0
