"""CE-FM-082B: energy bookkeeping for a conditional thin-wall fusion channel."""
import math,json,sys
from pathlib import Path
checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
rows=[]
for q1,q2 in [(1.,1.),(10.,10.),(1e4,1e4),(1.,100.)]:
 # E_rest(Q)=omega Q+alpha Q^(2/3); alpha=1 chosen only as a unit.
 release=q1**(2/3)+q2**(2/3)-(q1+q2)**(2/3);Ki=.01*release
 ck(str((q1,q2))+' fusion is exothermic at positive surface tension',release>0)
 for f in [0.,.5,1.]:
  escaped=release+f*Ki;Kf=Ki+release-escaped
  ck(str((q1,q2,f))+' energy balance',abs(Kf-(1-f)*Ki)<1e-10*release)
 rows.append({'Q1':q1,'Q2':q2,'surface_release_in_alpha_units':release,'relative_kinetic_energy_test':Ki,'radiation_at_release_alone_removes_no_orbital_energy':True})
ck('equal-lump release fraction',abs((2-2**(2/3))/2-(1-2**(-1/3)))<1e-15)
# Escaping only a fraction of surface release can heat the surviving halo.
release=2-2**(2/3);Ki=.01*release;Kf=Ki+release-.5*release;ck('partial radiation can heat rather than cool',Kf>Ki)
r={'claim_id':'CE-FM-082B','n_checks':len(checks),'all_pass':all(x['pass'] for x in checks),'checks':checks,'rows':rows,'scope':'Conditional thin-wall droplet rest energy with positive tension, no microscopic collision solution. Cooling of orbital energy requires escaping energy beyond released rest binding; rates and vacuum radiation channels remain unverified.'}
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'checks':len(checks),'equal_lump_surface_release_fraction':1-2**(-1/3)}))
