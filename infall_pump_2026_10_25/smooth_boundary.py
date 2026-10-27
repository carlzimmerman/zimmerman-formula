"""Separate conversion-front motion from actual material redistribution."""
import argparse,json
from pathlib import Path
import numpy as np
from live_collocated import Collocated
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);rows=[]
for name in ['run_smooth_infall']:
 root=Path('infall_pump_2026_10_25')/name;s=np.load(root/'state.npz');a,x,p,c,v=[s[k] for k in ['a','alpha','carrier_p','chi','pi']];mass=np.sum(abs(a)**2,axis=0);mt=abs(a[0])**2;q=mt/mass
 extra,source,bulk,conv,U,Gamma=m.transfer(a,x,c);psi=a/np.sqrt(m.vol);jt=m.k/m.sigma*m.w*np.imag(np.conj(psi[0,:-1])*U*psi[0,1:]);jf=m.k/m.sigma*m.w*np.imag(np.conj(psi[1,:-1])*psi[1,1:])
 def divergence(j):return np.r_[-j[0],j[:-1]-j[1:],j[-1]]
 tT=divergence(jt);tM=divergence(jt+jf);qconv=Gamma/mass;qtrans=(tT-q*tM)/mass;qdot=qconv+qtrans
 mu=m.pot(a,x,True)[1];u=m.enclosed(mt);omega=p/m.Z(a);mu[0]-=(2/np.pi)**2*m.ell2/m.c**2*m.transpose(.5*m.vol*omega**2*m.f(u)[3]);mu[0]+=extra
 H=(m.kd+mu)*a+m.J*m.alignment(a,x,c);H[0,:-1]+=m.ko*U*a[0,1:];H[0,1:]+=m.ko*np.conj(U)*a[0,:-1];H[1,:-1]+=m.ko*a[1,1:];H[1,1:]+=m.ko*a[1,:-1];ad=-1j*H/m.sigma;md=2*np.real(np.conj(a)*ad);qd=(md[0]-q*np.sum(md,axis=0))/mass
 cross=np.flatnonzero((q[:-1]-.5)*(q[1:]-.5)<0);i=cross[-1];dr=(m.r[i+1]-m.r[i])*m.rm;dq=q[i+1]-q[i];partial=np.array([dr*(.5-q[i+1])/dq**2,-dr*(.5-q[i])/dq**2]);Rdot=float(partial@qdot[i:i+2]/m.tdyn);Rconv=float(partial@qconv[i:i+2]/m.tdyn);Rtrans=float(partial@qtrans[i:i+2]/m.tdyn)
 def radius(a):
  z=abs(a[0])**2/np.sum(abs(a)**2,axis=0)
  return float(m.r[i]*m.rm+(.5-z[i])*dr/(z[i+1]-z[i]))
 fd=[]
 for eps in [1e-6,1e-7,1e-8]:fd.append({'epsilon_dimensionless_time':eps,'Rdot_kpc_Myr':(radius(a+eps*ad)-radius(a-eps*ad))/(2*eps*m.tdyn)})
 result=json.loads((root/'results.json').read_text());rows.append({'run':name,'time_Myr':result['completed_time_Myr'],'boundary_kpc':radius(a),'boundary_velocity_kpc_Myr':Rdot,'conversion_contribution_kpc_Myr':Rconv,'transport_contribution_kpc_Myr':Rtrans,'mass_continuity_scaled_error':float(np.max(abs(md[0]-(tT+Gamma)))/max(1.,np.max(abs(md[0])))),'fraction_evolution_scaled_error':float(np.max(abs(qdot-qd))/max(1.,np.max(abs(qd)))),'finite_difference_checks':fd})
Path(args.output).write_text(json.dumps({'cases':rows,'derivation':'q_t=[Gamma-div jT+q div(jT+jF)]/rho. Differentiate the actual discrete q=.5 crossing, using all original covariant currents. A conversion-front velocity is not mass infall or a restoring-force measurement.'},indent=2)+'\n');print(json.dumps(rows,indent=2))
