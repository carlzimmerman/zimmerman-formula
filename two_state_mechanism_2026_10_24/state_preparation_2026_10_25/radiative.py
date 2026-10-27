import argparse,json,math
G=6.67430e-11;HBAR=1.054571817e-34;C=299792458.;EV=1.602176634e-19
MSUN=1.98847e30;PC=3.085677581491367e16;YEAR=31557600.
CHI=11.220184543019636;F=CHI/(1+CHI);A0=9.3603e-11;ETA=5.364
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
rows=[]
for label,mb,b in [('small_dwarf',3e5,.3),('large_dwarf',1e8,1),('disk',6e10,3),('cluster',1e14,300)]:
 rho=3*ETA*mb*MSUN/(4*math.pi*(b*1000*PC)**3)
 for eps in [.1,1e-8]:
  ell=(1+eps)*F*F*A0/(8*math.pi*G*rho)
  for zeta in [.1,.03]:
   t=1e10*YEAR
   mmin=math.sqrt(3*HBAR*ell/(4*(1+CHI)*G*zeta**3*t))
   masses=[]
   for mev in [1e-22,1.,1e3,1e9,1e12]:
    m=mev*EV/C**2;omega=zeta*C/ell;q2=4*math.pi*G*(1+CHI)*m*m
    direct=omega**3*q2*ell*ell/(3*math.pi*HBAR*C**3)
    reduced=4*(1+CHI)*G*m*m*zeta**3/(3*HBAR*ell)
    assert abs(direct/reduced-1)<1e-12
    masses.append(dict(mass_eV=mev,maximum_vacuum_rate_s=direct,minimum_lifetime_years=1/(direct*YEAR)))
   rows.append(dict(profile=label,epsilon=eps,zeta=zeta,density_kg_m3=rho,
    minimum_dipole_length_pc=ell/PC,minimum_emitter_mass_kg=mmin,minimum_emitter_mass_eV=mmin*C*C/EV,
    mass_examples=masses))
with open(a.output,'w') as f:json.dump(dict(rows=rows),f,indent=2,allow_nan=False)
print(json.dumps([r for r in rows if r['profile']=='disk' and r['epsilon']==.1]))
