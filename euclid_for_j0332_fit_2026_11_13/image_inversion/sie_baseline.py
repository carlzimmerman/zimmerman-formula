from pathlib import Path
import numpy as np,json
P=Path(__file__).resolve().parent;I=P.parent/'inputs';c=json.loads((I/'results/coolest.json').read_text());p=c['lensing_entities'][0]['mass_model'][0]['parameters'];v=lambda p,k:p[k]['point_estimate']['value'];q=v(p,'q');a=np.pi/2+np.deg2rad(v(p,'phi'));cx=v(p,'center_x');cn=v(p,'center_y');b=v(p,'theta_E')/np.sqrt(q);g=c['lensing_entities'][2]['mass_model'][0]['parameters'];gg=v(g,'gamma_ext');ag=np.pi/2+np.deg2rad(v(g,'phi_ext'));g1=gg*np.cos(2*ag);g2=gg*np.sin(2*ag)
def sie(X,N):
 dx=X-cx;dy=N-cn;u=np.cos(a)*dx+np.sin(a)*dy;vv=-np.sin(a)*dx+np.cos(a)*dy;f=np.sqrt(1-q*q);psi=np.sqrt(q*q*u*u+vv*vv);au=b*q/f*np.arctan(f*u/psi);av=b*q/f*np.arctanh(f*vv/psi);return np.cos(a)*au-np.sin(a)*av+g1*X+g2*N,np.sin(a)*au+np.cos(a)*av+g2*X-g1*N
