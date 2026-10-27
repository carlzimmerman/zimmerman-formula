"""CE089C: minimum compact initial mass to retain the required aperture mass."""
from pathlib import Path
import json,math,sys
b=Path('sol61_push');r=json.loads((b/'early_dense_assembly_2026_10_19/run_001/results.json').read_text());d={x['name']:x for x in r['rows']};o={x['name']:x for x in json.loads((b/'cold_final_mile_2026_10_13/run_086_v2/results.json').read_text())['dwarfs']};G,MS,PC,A0=6.674e-11,1.989e30,3.0857e16,9.3603e-11;rows=[];checks=[]
def F(x,a):return x**3/(x*x+a*a)**1.5
for name,a in [('Draco',70),('Sextans',25)]:
 stock=d[name]['remaining_stock_Msun']*MS;need=d[name]['target_mass_inside_R_Msun']*MS;R=o[name]['R_pc']*PC;a*=PC
 for host in [6e10,8e10]:
  for peri in [5,10,20,50,100]:
   rp=peri*1000*PC;s=math.sqrt(G*host*MS/A0)/rp;g=G*host*MS/rp**2/(-math.expm1(-s));T=g/rp*(3-s/math.expm1(s));M0=need/F(R,a);rj=(G*M0/T)**(1/3);rt=math.sqrt(max(0,rj*rj-a*a))
   if rt<R:
    rt=(G*need/T)**(1/3);M0=need/F(rt,a)
   bound=M0*F(rt,a);inside=M0*F(min(R,rt),a);ok=abs(inside/need-1)<1e-12;checks.append({'name':str((name,host,peri))+' required inner mass','pass':ok});assert ok
   rows.append({'name':name,'b_pc':a/PC,'host_Msun':host,'peri_kpc':peri,'minimum_initial_compact_fraction_of_available_stock':M0/stock,'retained_compact_fraction_after_tide':bound/stock,'rt_pc':rt/PC,'stock_feasible':M0<=stock})
out={'claim_id':'CE-FM-089C','n_checks':len(checks),'checks':checks,'all_pass':True,'rows':rows,'scope':'Static circularized tidal truncation minimum core normalization; aperture-mass fit only, not kinematic/dynamical fit or actual pericentre.'};Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps([x for x in rows if x['host_Msun']==6e10],indent=1))
