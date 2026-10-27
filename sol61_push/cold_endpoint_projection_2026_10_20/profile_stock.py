"""Reported C-profile stock ceiling; this is not arbitrary-profile closure."""
from pathlib import Path
import json,math,sys,resource
B=Path(__file__).resolve().parent
d=json.loads((B/'inputs/cfg918_results.json').read_text());p=json.loads((B/'run_002/results.json').read_text());rows=[];checks=[]
for r in p['rows']:
 n=r['name'];b=d['results']['canonical']['B0'][n]['base'];v=r['apertures']['global']['sigma2_contributions_kms2'];base=v['stars']+v['tether'];coef=v['core']/b['Mx'];required=max(0.,(b['sig']**2-base)/coef);maximum=base+coef*b['Mrem']
 R=b['R'];kR=d['constants']['G']/(3*b['a'])*(1+(R/b['a'])**2)**(-1.5)
 ok=coef>=kR and (r['endpoint_rA_pc']>=R or v['A']==0) and r['endpoint_rB_pc']>=R
 checks.append({'name':n+' global C core more efficient than all allowed outer shells','pass':bool(ok)});assert ok
 ok=maximum>=r['apertures']['global']['sigma_stars_kms']**2*(1-1e-12);checks.append({'name':n+' all-stock C ceiling bounds selected endpoint','pass':bool(ok)});assert ok
 rows.append({'name':n,'fixed_C_core_minimum_mass_if_global_observation_Msun':required,'available_free_stock_Msun':b['Mrem'],'minimum_over_stock':required/b['Mrem'],'global_sigma_max_all_free_stock_in_C_kms':math.sqrt(maximum),'catalogue_sigma_kms':b['sig'],'stock_gate_passes_central_value_global_C_family':required<=b['Mrem'],'baseline_only_Re_sigma_kms':math.sqrt(sum(r['apertures']['Re']['sigma2_contributions_kms2'][k] for k in ['stars','tether']))})
r={'rows':rows,'checks':checks,'n_checks':len(checks),'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'If catalogue sigma is whole Plummer moment, C-profile core plus nonnegative receiver shells at r>=R. Source stellar/tether fields fixed. Whole available free stock can go to core; no E/J requirement imposed. No arbitrary-profile, aperture, uncertainty or dynamic exclusion.'};Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
