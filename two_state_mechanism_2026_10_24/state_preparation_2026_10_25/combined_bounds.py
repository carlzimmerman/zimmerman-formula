import argparse,json,math
G=6.67430e-11;HBAR=1.054571817e-34;C=299792458.;EVKG=1.602176634e-19/C**2
MSUN=1.98847e30;PC=3.085677581491367e16;A0=9.3603e-11;ETA=5.364;NU=8
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
rows=[];checks=[]
for name,chi,lam in [('bare',11.220184543019636,0.),('static_fit',138.62249546824629,.3875)]:
 f=chi/(1+chi);delta=1-lam
 for label,mb,b in [('small_dwarf',3e5,.3),('large_dwarf',1e8,1),('disk',6e10,3),('cluster',1e14,300)]:
  rho=3*ETA*mb*MSUN/(4*math.pi*(b*1000*PC)**3)
  for eps in [.1,1e-8]:
   ell0=(1+eps)*f*f*A0/(8*math.pi*G*rho);ell=ell0/delta
   mmax=HBAR*C*delta**2/(f*A0*ell**2)
   mmin=(6*math.pi**2*HBAR**3*rho/(NU*C**3))**.25/(1+eps)
   mtrk=HBAR/(2*f*A0*ell)*math.sqrt(12*math.pi*G*rho/(eps*f)) if lam==0 else None
   # Verify all eliminated identities at the current mass ceiling.
   beta=math.sqrt(4*math.pi*G*(1+chi));dipole=beta*mmax*ell
   cutoff=f*A0*mmax*ell/delta**2;n=rho/((1+eps)*mmax)
   chibare=2*n*dipole*dipole/cutoff
   assert abs(chibare/(delta*chi)-1)<2e-14
   assert abs(cutoff*ell/(HBAR*C)-1)<2e-14
   # Verify phase-space capacity exactly at the lower mass bound.
   M=(1+eps)*mmin;capacity=NU*(M*C/HBAR)**3/(6*math.pi**2)
   assert abs(capacity/(rho/M)-1)<2e-14
   rows.append(dict(model=name,profile=label,chi_effective=chi,lambda_interaction=lam,epsilon=eps,
    density_kg_m3=rho,dipole_length_pc=ell/PC,current_mass_upper_eV=mmax/EVKG,
    fermi_mass_lower_eV=mmin/EVKG,canonical_TRK_mass_upper_eV=None if mtrk is None else mtrk/EVKG,
    lower_over_upper=mmin/mmax,nonempty_mass_interval=bool(mmin<=mmax)))
# Test the analytic density and critical-coupling scalings independently as ratios.
for r in [1.,.1,.001]:
 for delta in [1.,.5,.1]:
  rho=r;f=.9;eps=.1;ell0=(1+eps)*f*f*A0/(8*math.pi*G*rho)
  ell=ell0/delta;mmax=HBAR*C*delta**2/(f*A0*ell**2)
  ellbase=(1+eps)*f*f*A0/(8*math.pi*G)
  base=HBAR*C/(f*A0*ellbase**2)
  assert abs(mmax/base/(r*r*delta**4)-1)<1e-13
  checks.append(dict(density_ratio=r,delta=delta,current_mass_ratio=mmax/base))
with open(a.output,'w') as out:json.dump(dict(rows=rows,scaling_checks=checks),out,indent=2,allow_nan=False)
print(json.dumps(dict(compatible_cases=sum(r['nonempty_mass_interval'] for r in rows),cases=len(rows),disk=[r for r in rows if r['profile']=='disk'])))
