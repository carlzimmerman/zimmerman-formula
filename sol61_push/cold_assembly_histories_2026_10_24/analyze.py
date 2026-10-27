"""Audit history response, paid work and an optimistic library bound."""
import json,math,hashlib
from pathlib import Path
import numpy as np

b=Path(__file__).parent
tags=['quiet','early','late','slow','early_pad']
runs={t:json.loads((b/'runs'/(t+'.json')).read_text()) for t in tags}
quiet=runs['quiet'];checks={};summary={}
for tag,d in runs.items():
    i,f=d['initial'],d['final']
    checks[tag+'_mass_book']=abs(f['M']+f['removed']['M']-i['M'])<1e-8
    checks[tag+'_energy_work_book']=abs(d['E_residual'])<.01
    checks[tag+'_zero_source_mass_creation']=all(h['M']<=i['M']+1e-8 for h in d['history'])
    jr=d['late_star_rhalf_over_frozen']/quiet['late_star_rhalf_over_frozen']
    kr=d['late_star_sigma_over_frozen']/quiet['late_star_sigma_over_frozen']
    rmax=max(h['stars']['rmax'] for h in d['history'])
    fmax=max(h['stars_frozen']['rmax'] for h in d['history'])
    summary[tag]={'parameters':d['parameters'],'central_mass_fraction':f['M_inner'],
        'retained_mass_fraction':f['M'],'removed_mass_fraction':f['removed']['M'],
        'inner_specific_spin_ratio':d['inner_specific_spin_ratio'],'work':d['external_work'],
        'E_ledger_relative':d['E_residual'],'J_ledger_relative':d['J_residual'],
        'star_variance_relative_quiet':kr,'star_halfmass_relative_quiet':jr,
        'stellar_response_flag':abs(kr-1)>.1 or abs(jr-1)>.1,
        'star_max_radius':rmax,'frozen_star_max_radius':fmax,
        'stars_stay_inside_margin':max(rmax,fmax)<d['parameters']['L']/2-2,
        'gates':d['gates'],'peak_rss_bytes_macos':d['peak_rss_bytes_macos']}
checks['quiet_work_zero']=quiet['external_work']==0
assert all(checks.values()),checks

# Extremely optimistic old-stock library test, not a predicted history assignment.
# All absorber losses are allowed to be anywhere outside its onset r=12.
# If Sextans needs that lost material, its aperture must be >=12. The larger
# M*R arguments then encompass the ENTIRE retained simulation field of the others.
source=Path('campaign_fresh_gravity/CFG918_dwarf_receiver_capacity/cfg918_results.json')
ref=json.loads(source.read_text())
max_ret=max(d['final']['M'] for d in runs.values())
min_ret=min(d['final']['M'] for d in runs.values())
max_radius=max(math.sqrt(3)*d['parameters']['L']/2 for d in runs.values())
library=[]
for foot in ['canonical','alt']:
    r=ref['results'][foot]['B0'];sx=r['Sextans']['base']
    need_boundary=sx['F']>max_ret
    for name in ['Fornax','Leo I']:
        other=r[name]['base'];rank=other['Mrem']*other['R']/(sx['Mrem']*sx['R'])
        entire=rank*12>max_radius
        library.append({'footing':foot,'other_dwarf':name,
          'Sextans_target_exceeds_any_retained_mass':need_boundary,
          'other_aperture_lower_bound_code':rank*12,
          'maximum_field_radius_code':max_radius,'other_encloses_all_retained':entire,
          'minimum_retained_cold_fraction':min_ret,'required_other_fraction':other['F'],
          'minimum_cold_over_required_factor':min_ret/other['F'],
          'conditional_library_incompatible':bool(need_boundary and entire and min_ret>other['F'])})

result={'runs':summary,'checks':checks,'library_bound':library,
        'library_assumptions':'Common physical eta, simulation mass units tied to older remaining stocks, exact saved dimensionless history library, same final evolutionary stage, cold Gaussian/wave scaling; allow arbitrary per-dwarf history choices as an optimistic non-predictive diagnostic. Treat removed material as outside r=12 at the final epoch, with no return inside; physical escape and return are unproved. Histories and a0-code tracer responses are not mapped to observed physical times/stellar sizes.',
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'not_tested':['data-derived gas histories','live baryon hydrodynamics/recoil','observed stellar heating','newer Sextans likelihood','covariance/cosmology','all assembly histories']}
(b/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'runs':summary,'library_bound':library},indent=2))
