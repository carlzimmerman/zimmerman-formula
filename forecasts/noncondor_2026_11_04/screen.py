"""Fixed PAPER66 conditional signal/precision screen, not a target detection forecast."""
import csv,json,math,sys
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
here=Path(__file__).resolve().parent
A0=9.3603e-11;KPC=3.0857e19;G=4.30091e-6
def ratio(z):
    a=1/(1+z)
    return math.sqrt(a**(-3*(1-.838-.62))*math.exp(1.86*(1-a)))
def g(y,r):return (y+math.sqrt(y*y+4*y*r))/2
def v(y,r,R):return math.sqrt(g(y,r)*A0*R*KPC)/1000
rows=[]
for z in [1.5,4.5505,4.567,7.]:
 for R in [3.,5.,7.5,10.,15.]:
  for y in [.1,.3,1.,3.,10.]:
   r=ratio(z);vf=v(y,r,R);vm=v(y,1,R)
   # Exact inverse: baryon acceleration required by constant-a0 MOND to reproduce F-DESI.
   gf=g(y,r);ymatch=gf*gf/(gf+1)
   eps=1e-5
   sens=(math.log(v(y*math.exp(eps),r,R))-math.log(v(y*math.exp(-eps),r,R)))/(2*eps)
   loggap=math.log(vm/vf);precision=loggap/3
   qmax=math.sqrt(max(0,precision**2-.01**2))/sens
   rows.append(dict(z=z,R_kpc=R,gN_over_a00=y,a0_ratio=r,V_FDESI=vf,V_MOND=vm,delta_kms=vm-vf,velocity_only_sigma_3=(vm-vf)/3,required_gN_relative_sigma_if_velocity_1pct=qmax,MOND_matching_baryon_factor=ymatch/y,MOND_matching_mass_shift_dex=math.log10(ymatch/y),spherical_equivalent_baryon_mass=y*A0/(1e6/KPC)*R**2/G))
checks=dict(local_ratio=ratio(0)==1,inverse_max_error=max(abs(g(g(y,ratio(z))**2/(g(y,ratio(z))+1),1)-g(y,ratio(z))) for z in [1.5,4.55,7] for y in [.1,.3,1,3,10])<1e-12,ceiling=all(1-x['V_FDESI']/x['V_MOND'] <= 1-x['a0_ratio']**.25+1e-12 for x in rows),coverage=len(rows)==100)
with open(out/'grid.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
pids=['2022.1.01118.S','2023.1.00835.S','2025.1.00827.S','2025.1.00182.S','2024.1.01042.S','2025.1.00942.S']
inventory=[];seen=set()
for d in csv.DictReader(open(here/'archive_dynamics.csv')):
 if d['proposal_id'] not in pids or d['target_name'].startswith('J'):continue
 key=(d['target_name'],d['obs_id'].split('.source')[0])
 if key in seen:continue
 seen.add(key);t=datetime.fromisoformat(d['obs_release_date']).replace(tzinfo=timezone.utc)
 inventory.append(dict(target=key[0],unit=key[1],project=d['proposal_id'],beam_arcsec=float(d['s_resolution']),release_UTC=t.isoformat() if t.year<3000 else None,release_Eastern=t.astimezone(ZoneInfo('America/New_York')).isoformat() if t.year<3000 else None,abstract=d['proposal_abstract']))
(out/'inventory.json').write_text(json.dumps(inventory,indent=2))
summary=dict(checks=checks,ratios={str(z):dict(a0_ratio=ratio(z),maximum_speed_difference=1-ratio(z)**.25,log10_a0_ratio=math.log10(ratio(z))) for z in [1.5,4.5505,4.567,7.]})
(out/'results.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
assert all(checks.values())
