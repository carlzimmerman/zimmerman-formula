"""CE-FM-058: archival sensitivity arithmetic and phase-transfer identifiability."""
import csv,json,sys,math
from pathlib import Path
import sympy as s
b=Path('campaign_fresh_gravity/CFG798_herschel_hifi_dish')
a=json.loads((b/'cfg798_results.json').read_text());rows=list(csv.DictReader((b/'cfg798_matches.csv').open()))
checks=[]
def ck(n,v):
    assert v,n
    checks.append(n)
c=2.99792458e8;kb=1.380649e-23;rho=.01*1.989e30/(3.0857e16)**3
hours={};counts={}
for nu in ['541.7','595.5']:
    counts[nu]=len([r for r in rows if r['target_GHz']==nu])
    for tier in ['A','B']:
        hh=sum(float(r['t_int_h']) for r in rows if r['target_GHz']==nu and r['tier']==tier)
        hours[nu+'|'+tier]=hh
        ck('hours '+nu+' '+tier,math.isclose(hh,a['hours'][nu+'|'+tier],abs_tol=1e-12))
    hours[nu+'|A+B']=hours[nu+'|A']+hours[nu+'|B']
for key,entry in a['reach'].items():
    nu,tier,T=key.split('|');hh=hours[nu+'|'+tier];Temp=float(T[1:])
    for sk,val in entry.items():
        if hh==0:ck('zero useful hours '+key+' '+sk,math.isinf(val));continue
        Pc=(2/3)*rho*c**3*9.6/float(sk[1:])
        sigma=kb*(2*Temp)*math.sqrt(1.1e6/(hh*3600))
        expected=math.sqrt(5/((Pc/2)/sigma*math.sqrt(2)))
        ck('radiometer cell '+key+' '+sk,math.isclose(expected,val,rel_tol=3e-14))
# Equal phase response is an exact null of differential measurements.
ABBA=s.Matrix([[-s.Rational(1,2),s.Rational(1,2),s.Rational(1,2),-s.Rational(1,2)]])
common=s.ones(4,1)
ck('ABBA common response annihilated',ABBA*common==s.zeros(1,1))
ck('arbitrary linear postprocessing cannot recover common mode',s.Matrix([[2],[3]])*ABBA*common==s.zeros(2,1))
aR,aS=s.symbols('a_ref a_science',real=True)
resp=s.Matrix([aR,aS,aS,aR])
ck('phase-dependent response is science minus reference',s.simplify((ABBA*resp)[0]-(aS-aR))==0)
ck('post-subtraction unit injection is not physical-transfer test',(ABBA*common)[0]==0 and s.Integer(1)!=0)
# Local polynomial background can retain independent narrow-line direction;
# an arbitrary per-channel nuisance instead contains the entire line space.
ck('free per-channel background degenerates signal',s.eye(3).rank()==s.eye(3).row_join(s.Matrix([0,1,0])).rank())
base=a['reach']['541.7|A+B|T150']['S50']
fractions=[1,1e-2,1e-4,1e-6]
controlled=[{'retained_power_fraction':f,'eps_min':base/math.sqrt(f)} for f in fractions]
res={'claim_id':'CE-FM-058','checks_passed':len(checks),'checks':checks,'recorded_csv_counts':counts,'recorded_csv_hours':hours,'conditional_primary_eps':base,'minimum_relative_power_transfer_for_eps4e_9_at_fixed_noise':(base/4e-9)**2,'phase_transfer_controls':controlled,'scope':'Recorded CSV and supplied radiometer approximation only; primary pipeline documents checked separately. No spectra downloaded or archive-sensitivity measurement/whole-theory null test.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
