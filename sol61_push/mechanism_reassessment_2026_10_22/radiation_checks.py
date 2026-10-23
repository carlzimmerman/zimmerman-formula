"""Variational interface scattering for the reduced mixed scalar, not a galaxy."""
import numpy as np
import math,json,sys
from pathlib import Path
B=eta=gamma=1.
mutate='--mutate' in sys.argv

def modes(omega,h):
 a=h-eta*omega*omega
 disc=math.sqrt(a*a+4*gamma*B*omega*omega)
 # Avoid cancellation in the small positive root.
 k2=2*B*omega*omega/(disc+a) if a>=0 else (disc-a)/(2*gamma)
 kap2=(disc+a)/(2*gamma) if a>=0 else 2*B*omega*omega/(disc-a)
 return math.sqrt(k2),math.sqrt(kap2)

def vector(lam,omega,h):
 # sigma, sigma_x, bending moment, variational shear.
 return np.array([1,lam,gamma*lam**2,gamma*lam**3+(eta*omega*omega-h)*lam],complex)

def flux(k,omega,h):
 return omega*k*(h+2*gamma*k*k-eta*omega*omega)/2

def scatter(omega,hL,hR):
 kl,al=modes(omega,hL);kr,ar=modes(omega,hR)
 krout=-kr if mutate and hL != hR else kr
 inc=vector(1j*kl,omega,hL)
 cols=[vector(-1j*kl,omega,hL),vector(al,omega,hL),-vector(1j*krout,omega,hR),-vector(-ar,omega,hR)]
 mat=np.column_stack(cols)
 # Row scaling retains all four variational boundary conditions at small omega.
 scale=np.maximum(np.max(np.abs(mat),axis=1),np.abs(inc))
 sol=np.linalg.solve(mat/scale[:,None],-inc/scale)
 refl,evL,trans,evR=sol
 f0=flux(kl,omega,hL)
 R=abs(refl)**2;T=flux(krout,omega,hR)*abs(trans)**2/f0
 res=np.max(np.abs(mat@sol+inc)/scale)
 return {'omega':omega,'k_left':kl,'k_right':kr,'kappa_left':al,'kappa_right':ar,
 'R':float(R),'T_signed':float(T),'flux_residual':float(abs(1-R-T)),
 'matching_residual':float(res),'outgoing_right':krout>0,
 'transmitted_amplitude_abs':float(abs(trans))}
rows=[scatter(10.**e,1.,0.) for e in range(-6,3)]
control=[scatter(w,1.,1.) for w in [1e-5,1.,100.]]
checks={
 'positive_propagating_root':all(row['k_left']>0 and row['k_right']>0 for row in rows),
 'decaying_evanescent_root':all(row['kappa_left']>0 and row['kappa_right']>0 for row in rows),
 'four_matching_conditions':max(r['matching_residual'] for r in rows+control)<1e-10,
 'energy_flux_conservation':max(r['flux_residual'] for r in rows+control)<1e-9,
 'outgoing_right':all(r['outgoing_right'] for r in rows+control),
 'nonnegative_transmission':all(r['T_signed']>=0 for r in rows+control),
 'identical_media':max(abs(r['T_signed']-1)+r['R'] for r in control)<1e-9,
 'low_frequency_sqrt_law':max(abs(r['T_signed']/(4*math.sqrt(r['omega']))-1) for r in rows[:2])<.02,
}
# Polynomial root and group-velocity flux identity, separately evaluated.
errors=[];vg_errors=[]
for h in [0.,1.]:
 for w in [1e-6,.01,1.,100.]:
  k,al=modes(w,h)
  for z in [k*k,-al*al]:
   terms=[gamma*z*z,(h-eta*w*w)*z,-B*w*w]
   errors.append(abs(sum(terms))/max(abs(t) for t in terms))
  vg=k*(h+2*gamma*k*k-eta*w*w)/(w*(B+eta*k*k))
  vg_errors.append(abs(flux(k,w,h)-vg*w*w*(B+eta*k*k)/2)/flux(k,w,h))
checks['dispersion_polynomial']=max(errors)<1e-12
checks['flux_equals_group_velocity_energy']=max(vg_errors)<1e-12
result={'checks':checks,'all_pass':all(checks.values()),'rows':rows,'identical_media':control,'max_polynomial_relative_residual':max(errors),'mutated':mutate,'scope':'dimensionless planar step; no galaxy profile or source power'}
p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n')
for name,ok in checks.items():print(name,'PASS' if ok else 'FAIL')
for row in rows:print('omega',row['omega'],'T',row['T_signed'],'R',row['R'])
print('COMPLETE',sum(checks.values()),'/',len(checks))
sys.exit(0 if all(checks.values()) else 1)
