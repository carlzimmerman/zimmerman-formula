from pathlib import Path
import json,numpy as np
from astropy.io import fits
P=Path(__file__).resolve().parent;I=P.parent/'inputs';c=json.loads((I/'results/coolest.json').read_text());v=lambda p,k:p[k]['point_estimate']['value'];p=c['lensing_entities'][0]['mass_model'][0]['parameters'];q=v(p,'q');phi=np.deg2rad(v(p,'phi'));theta=v(p,'theta_E');cx=v(p,'center_x');cy=v(p,'center_y');g=c['lensing_entities'][2]['mass_model'][0]['parameters'];gam=v(g,'gamma_ext');gp=np.deg2rad(v(g,'phi_ext'));h=fits.open(I/'results/deflections.fits');ay=h[1].data;ax=h[2].data;iy,ix=np.indices(ax.shape);X=(ix-50.5)*.1;N=(iy-50.5)*.1;Y=-N;valid=np.hypot(X-cx,N-cy)>.4;results=[]
# Work in sky north/west frame; COOLEST angles may be relative to either axis.
for ang in [phi,-phi,np.pi/2+phi,np.pi/2-phi]:
 dx=X-cx;dy=N-cy;xr=np.cos(ang)*dx+np.sin(ang)*dy;yr=-np.sin(ang)*dx+np.cos(ang)*dy;psi=np.sqrt(q*q*xr*xr+yr*yr);f=np.sqrt(1-q*q);arx=q/f*np.arctan(f*xr/psi);ary=q/f*np.arctanh(f*yr/psi);sx=np.cos(ang)*arx-np.sin(ang)*ary;sn=np.sin(ang)*arx+np.cos(ang)*ary
 for ga in [gp,-gp,np.pi/2+gp,np.pi/2-gp]:
  g1=gam*np.cos(2*ga);g2=gam*np.sin(2*ga);shx=g1*X+g2*N;shn=g2*X-g1*N
  for fac in [theta/np.sqrt(q),2*theta/(1+q),theta]:
   ex=fac*sx+shx;en=fac*sn+shn;err=np.sqrt(np.mean(((ex-ax)**2+(en+ay)**2)[valid]));results.append({'mass_phi_rad':float(ang),'shear_phi_rad':float(ga),'b':float(fac),'rms_vector_arcsec':float(err)})
results.sort(key=lambda x:x['rms_vector_arcsec']);(P/'deflection_tests.json').write_text(json.dumps(results,indent=2)+'\n');print(results[:5])
