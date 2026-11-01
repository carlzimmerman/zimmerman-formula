import sys,math,numpy as np
from astropy.io import fits
from astropy.wcs import WCS
f=sys.argv[1]; h=fits.open(f,memmap=True)[0]; H=h.header; d=h.data[0] if h.data.ndim==4 else h.data
nz=d.shape[0]; nu=H['CRVAL3']+(np.arange(nz)+1-H['CRPIX3'])*H['CDELT3']; print('BUNIT',H.get('BUNIT'),'shape',d.shape,'CASAMBM' in H)
NU=345.796e9/3.52455; v=(NU-nu)/NU*299792.458; dv=abs(v[1]-v[0]); print('dv',dv,'v range',v[0],v[-1])
ny,nx=d.shape[1:]; c=nx//2; pix=abs(H['CDELT2'])*3600
yy,xx=np.indices((ny,nx)); r=np.hypot(xx-c,yy-c)*pix
for rin,rout in((2,4),(4,8),(8,14),(14,20)):
    m=(r>rin)&(r<rout); vals=[]
    for k in np.linspace(5,nz-6,40).astype(int):
        if abs(v[k])<700: continue
        x=d[k][m]; x=x[np.isfinite(x)]
        if x.size: vals.append(1.4826*np.median(abs(x-np.median(x))))
    print('r',rin,rout,'rms/ch mJy',round(1e3*np.median(vals),3) if vals else None)
# spectral scaling off source
sub=np.nan_to_num(d[:,c-40:c+40,c+60:c+140].astype(np.float32)); sel=np.abs(v)>700; sub=sub[sel]
for b in (1,2,5,10,20):
    n=sub.shape[0]//b; s=sub[:n*b].reshape(n,b,*sub.shape[1:]).mean(axis=1); print('bin',b,'dv',round(b*dv),'rms mJy',round(1e3*1.4826*np.median(abs(s-np.median(s))),3),'-> per 10 km/s if sqrt',round(1e3*1.4826*np.median(abs(s-np.median(s)))*math.sqrt(b*dv/10),3))
# integrated spectrum on-source: aperture 1 arcsec radius
m=r<=1.0; bp=1.133*H['BMAJ']*H['BMIN']/abs(H['CDELT1']*H['CDELT2']); spec=np.array([np.nansum(d[k][m]) for k in range(nz)])/bp
cont=np.median(spec[np.abs(v)>700]); sp=spec-cont; sel=np.abs(v)<=900
n=int(50/dv); sm=np.convolve(sp,np.ones(n)/n,'same')
pk=sm[sel].max(); vv=v[sel]; ab=vv[sm[sel]>=pk/2]; print('smoothed peak mJy',round(pk*1e3,2),'half-max extent km/s',round(ab.min()),round(ab.max()),'width',round(ab.max()-ab.min()))
print('int flux 1" +-500',round(float(np.sum(sp[np.abs(v)<=500])*dv),3),'centroid',round(float((np.clip(sp[np.abs(v)<=500],0,None)*v[np.abs(v)<=500]).sum()/np.clip(sp[np.abs(v)<=500],0,None).sum())))
for a in range(-600,600,100):
    w=(v>=a)&(v<a+100); print(a,round(float(np.mean(sp[w]))*1e3,2),end=' | ')
print()
