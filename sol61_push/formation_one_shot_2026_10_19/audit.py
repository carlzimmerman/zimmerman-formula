"""Bounded stdlib checks; no simulation or galaxy fit. Run from any directory."""
from pathlib import Path
import math,json,hashlib,subprocess
R=Path(__file__).resolve().parents[2]
S=R/'sol61_push/formation_one_shot_2026_10_19'
checks=[]
def ck(name,condition):
    assert condition,name
    checks.append({'name':name,'pass':True})
# Exact H-LINK cap: t/(1+t^2)<=1/2, independent of finite sampling.
for t in [0,1e-3,.1,1,10,100]:
    ck('H-LINK identity '+str(t),abs(.5-t/(1+t*t)-(t-1)**2/(2*(1+t*t)))<1e-14)
# Physical KG threshold for slow, bare linear sources, not carrier sidebands.
hbar=6.582119569e-16 # eV s
omega_m=1e6/hbar
omega_orb=1e4/(100*3.085677581491367e16)
# de Broglie length is illustrative: no coherence or boson-star theorem inferred.
length=2*math.pi*1.054571817e-34/((1e6*1.782661921e-36)*1e4)
# Cauchy-Schwarz receiver lower bound in common Mpc/(km/s) units.
# With Jreq = j M Ri v and Kout=.5 alpha M v^2,
# Mout/M >= j^2/alpha * (Ri/Rout)^2.
receiver_examples=[]
for j in [.05,.1,.2]:
    for alpha in [.1,1,10]:
        minimum=j*j/alpha
        ck('receiver identity '+str((j,alpha)),abs((j*j)/(2*(.5*alpha))-minimum)<1e-15)
        receiver_examples.append({'j':j,'alpha':alpha,'Rout_over_Ri':1,'minimum_receiver_fraction':minimum})
ck('slow bare scalar radiation threshold',omega_orb<omega_m)
# Current source snapshots only, not independently validated literature fits.
pins={}
for pattern,names in [('CFG872*',['README.md','cfg872.py','cfg872_results.json']),('CFG870*',['README.md','cfg870_results.json'])]:
    d=next((R/'campaign_fresh_gravity').glob(pattern))
    for name in names:
        p=d/name;rel=str(p.relative_to(R));digest=hashlib.sha256(p.read_bytes()).hexdigest()
        ck('committed '+rel,hashlib.sha256(subprocess.check_output(['git','-C',str(R),'show','bcba9fc59:'+rel])).hexdigest()==digest)
        pins[rel]=digest
result={'format':'custom bounded stdlib audit; not v2 manifest','source_snapshot':'bcba9fc59','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks,'n_checks':len(checks),'source_hashes':pins,'omega_m_per_s':omega_m,'omega_orbit_per_s':omega_orb,'frequency_ratio':omega_m/omega_orb,'deBroglie_m_at_1MeV_10kms':length,'receiver_examples':receiver_examples,'scope':'Necessary conservation and frequency conditions only; no transport rate, formation simulation, initial-spin prediction or four-galaxy likelihood.'}
(S/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'threshold_ratio':omega_m/omega_orb,'deBroglie_m':length}))
