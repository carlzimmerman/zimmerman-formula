"""Pressure matching selects MOND radius for P_ext=P_cap, not the CFG4 edge."""
import os,json,math,pathlib,sys
G=6.67430e-11;MS=1.98892e30;KPC=3.0856775814913673e19
MUT=os.environ.get('MUTATE')=='1';rows=[];checks={}
for footing,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 for Mb in [1e9,1e10,1e11]:
  rm=math.sqrt(G*Mb*MS/a0);Pc=a0*a0/(8*math.pi*G);rta=500*KPC
  # MUTATE falsely identifies a CFG4-scale boundary with the P_cap pressure-matching boundary.
  re=.4*rta if MUT else rm
  P=lambda r:a0*Mb*MS/(8*math.pi*r*r)
  residual=P(re)/Pc-1
  req=[{'xe':x,'Pext_over_Pcap':P(x*rta)/Pc} for x in [.31,.4,.48]]
  rows.append({'footing':footing,'Mb_Msun':Mb,'rM_kpc':rm/KPC,'candidate_re_kpc':re/KPC,'pressure_match_residual':residual,'required_pressure_for_CFG4_window':req,'finite_zero_pressure_match':False})
checks['vacuum_scale_pressure_matches_only_rM']={'passed':max(abs(r['pressure_match_residual']) for r in rows)<1e-12,'value':max(abs(r['pressure_match_residual']) for r in rows)}
checks['CFG4_scale_requires_lower_environment_pressure']={'passed':all(d['Pext_over_Pcap']<.01 for r in rows for d in r['required_pressure_for_CFG4_window']),'value':max(d['Pext_over_Pcap'] for r in rows for d in r['required_pressure_for_CFG4_window'])}
out={'checks':checks,'rows':rows,'assumptions':['point baryons; weak-field hydrostatics','500 kpc turnaround radius is an illustration, not a universal halo prediction','positive vacuum stress scale proposed as external pressure; not the negative equation-of-state pressure of a cosmological constant'],'kappa':'1/2 fitted'}
p=pathlib.Path(os.environ.get('BOUNDARY_OUTPUT',str(pathlib.Path(__file__).with_name('boundary_results'+('_MUTATE' if MUT else '')+'.json'))));p.write_text(json.dumps(out,indent=2))
for k,v in checks.items():print('PASS' if v['passed'] else 'FAIL',k,v['value'])
sys.exit(0 if all(v['passed'] for v in checks.values()) else 1)
