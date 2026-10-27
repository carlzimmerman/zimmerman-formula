"""Do not call a coarse exterior a fast open bath without bandwidth checks."""
import argparse,json
from pathlib import Path
import numpy as np
from dynamics import model,load
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();m=model();z=load('sustained_transport_2026_10_26/run_continue_second/state.npz');rows=[]
for lo,hi in [(100,300),(500,3500)]:
 mask=(m.wr*m.rm>lo)&(m.wr*m.rm<hi);r=m.wr[mask];h=float(np.mean(np.diff(r)));assert np.max(abs(np.diff(r)-h))<1e-9*h;u=r*z[3][mask];ut=r*z[4][mask];out=(ut[:-1]+ut[1:])/2-m.c*np.diff(u)/h;inc=(ut[:-1]+ut[1:])/2+m.c*np.diff(u)/h
 k=2*np.pi*np.fft.rfftfreq(len(out),h);omega=2*m.c/h*np.sin(k*h/2)/m.tdyn;power=abs(np.fft.rfft(np.hanning(len(out))*out))**2;power[1:-1]*=2
 rows.append({'annulus_kpc':[lo,hi],'spacing_kpc':h*m.rm,'radial_wave_discrete_frequency_ceiling_rad_Myr':2*m.c/h/m.tdyn,'outgoing_characteristic_energy':float(h/4*np.sum(out*out)),'incoming_characteristic_energy':float(h/4*np.sum(inc*inc)),'windowed_fraction_above100_rad_Myr':float(np.sum(power[omega>100])/np.sum(power)),'windowed_fraction_above300_rad_Myr':float(np.sum(power[omega>300])/np.sum(power)),'windowed_fraction_above450_rad_Myr':float(np.sum(power[omega>450])/np.sum(power)),'window_frequency_resolution_rad_Myr':float(omega[1])})
res={'wave_speed_kpc_Myr':m.c*m.rm/m.tdyn,'outer_2kpc_grid_ceiling_rad_Myr':2*m.c*m.rm/(2*m.tdyn),'cases':rows,'limitation':'A 2-kpc exterior cannot propagate arbitrary ~500-rad/Myr carrier-frequency waves. Windowed snapshot fractions only assess present radial content. Future claims of fast-mode escape require exterior-grid refinement; no universal fast open-bath claim is made.'};Path(args.output).write_text(json.dumps(res,indent=2)+'\n');print(res)
