"""Positive radial characteristics with an exact uniform-grid energy identity."""
import numpy as np

def decompose(r,chi,pi,c,tdyn,lower,upper,gauge_offset=0.):
 # Use the KNOWN retarded initial gauge, not a finite-radius1/r tail value.
 offset=float(gauge_offset);chi=chi-offset;mask=(r>=lower)&(r<=upper);rr=r[mask];cc=chi[mask];pp=pi[mask];u=rr*cc;ut=rr*pp;h=float(np.mean(np.diff(rr)))
 assert np.max(abs(np.diff(rr)-h))<1e-9*h
 du=np.diff(u)/h;tm=(ut[1:]+ut[:-1])/2;out=tm-c*du;inc=tm+c*du
 Eout=float(.25*h*np.sum(out*out));Ein=float(.25*h*np.sum(inc*inc));boundary=float(-.5*c*c*(u[-1]**2/rr[-1]-u[0]**2/rr[0]))
 correction=float(h/8*np.sum(np.diff(ut)**2)+h**3/48*np.sum(pp[:-1]**2+pp[1:]**2)+c*c*h/8*np.sum(np.diff(cc)**2))
 # The actual finite-volume radial energy, with half weights at interval ends.
 kinetic=float(h/4*np.sum((rr[:-1]**2+h*h/12)*pp[:-1]**2+(rr[1:]**2+h*h/12)*pp[1:]**2));gradient=float(.5*c*c*np.sum(((rr[1:]+rr[:-1])/2)**2/h*np.diff(cc)**2));physical=kinetic+gradient
 resolved=Eout+Ein>1e-20*max(abs(boundary),physical,1e-100);bands=[]
 for trim in [0.,.1]:
  if not resolved:bands.append({'inner_trim_fraction':trim,'status':'below_numerical_radiation_floor'});continue
  lo=int(len(out)*trim);sig=out[lo:];win=np.hanning(len(sig));sp=np.fft.rfft(win*sig);omega=c*2*np.pi*np.fft.rfftfreq(len(sig),h)/tdyn;power=abs(sp)**2;power[1:-1]*=2;den=np.sum(power)
  bands.append({'inner_trim_fraction':trim,'status':'finite_window_proxy','frequency_resolution_rad_Myr':float(omega[1]),'windowed_fraction_above1_rad_Myr':float(np.sum(power[omega>1])/den) if den else 0.,'windowed_fraction_above10_rad_Myr':float(np.sum(power[omega>10])/den) if den else 0.,'peak_rad_Myr':float(omega[np.argmax(power)]) if den else 0.})
 return {'outgoing_characteristic_energy':Eout,'incoming_characteristic_energy':Ein,'incoming_fraction':Ein/(Eout+Ein) if resolved else None,'reactive_boundary_energy':boundary,'positive_finite_grid_correction':correction,'physical_segment_energy':physical,'decomposition_identity_error':physical-Eout-Ein-boundary-correction,'windowed_spectra':bands,'outer_gauge_offset':offset,'number_of_cells':len(rr),'lower_radius_dimensionless':float(rr[0]),'upper_radius_dimensionless':float(rr[-1])}
