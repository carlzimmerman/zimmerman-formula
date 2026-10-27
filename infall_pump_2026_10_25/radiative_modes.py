"""Outgoing radial characteristics remove the static Coulomb tail.

For source-free r>R, u=r*chi obeys u_tt-c^2 u_rr=0. The positive energies
1/4 integral(u_t -/+ c u_r)^2 dr distinguish outgoing/incoming radiation.
The original radial field energy adds the boundary term -c^2[u^2/r]/2.
Windowed spectral band fractions are diagnostics, not exact finite-time spectra.
"""
import numpy as np

def decompose(r,chi,pi,c,tdyn,lower,upper):
 mask=(r>=lower)&(r<=upper);rr=r[mask];u=rr*chi[mask];ut=rr*pi[mask];dr=float(np.mean(np.diff(rr)));ur=np.gradient(u,dr,edge_order=2);out=ut-c*ur;inc=ut+c*ur
 Eout=float(.25*np.trapz(out*out,rr));Ein=float(.25*np.trapz(inc*inc,rr));boundary=float(-.5*c*c*(u[-1]**2/rr[-1]-u[0]**2/rr[0]))
 # Include the whole source-free interval with two windows to expose leakage.
 bands=[]
 for trim in [0.,.1]:
  lo=int(len(rr)*trim);sig=out[lo:];win=np.hanning(len(sig));sp=np.fft.rfft(win*sig);omega=c*2*np.pi*np.fft.rfftfreq(len(sig),dr)/tdyn;power=abs(sp)**2;power[1:-1]*=2;den=np.sum(power)
  bands.append({'inner_trim_fraction':trim,'frequency_resolution_rad_Myr':float(omega[1]),'windowed_fraction_above1_rad_Myr':float(np.sum(power[omega>1])/den) if den else 0.,'windowed_fraction_above10_rad_Myr':float(np.sum(power[omega>10])/den) if den else 0.,'peak_rad_Myr':float(omega[np.argmax(power)]) if den else 0.})
 return {'outgoing_characteristic_energy':Eout,'incoming_characteristic_energy':Ein,'incoming_fraction':Ein/(Eout+Ein) if Eout+Ein else 0.,'reactive_boundary_energy':boundary,'reconstructed_radial_field_energy':Eout+Ein+boundary,'windowed_spectra':bands,'number_of_cells':len(rr),'lower_radius_dimensionless':float(rr[0]),'upper_radius_dimensionless':float(rr[-1])}
