"""Necessary ordering test for one fixed-eta homologous wave profile."""
import json,hashlib
from pathlib import Path

b=Path(__file__).parent
source=Path('campaign_fresh_gravity/CFG918_dwarf_receiver_capacity/cfg918_results.json')
data=json.loads(source.read_text())
rows=[];contradictions=[]
for foot in ['canonical','alt']:
    ref=data['results'][foot]['B0']
    for name in ['Draco','Sextans','Fornax','Leo I']:
        r=ref[name]['base']
        rows.append({'footing':foot,'dwarf':name,'M_stock':r['Mrem'],'R_aperture_pc':r['R'],
                     'required_fraction':r['F'],'M_stock_times_R':r['Mrem']*r['R']})
    sx=ref['Sextans']['base']
    for name in ['Fornax','Leo I']:
        r=ref[name]['base']
        rank=(r['Mrem']*r['R'])/(sx['Mrem']*sx['R'])
        assert rank>1 and r['F']<sx['F']
        contradictions.append({'footing':foot,'pair':['Sextans',name],
            'aperture_argument_ratio':rank,'required_fraction_Sextans':sx['F'],
            'required_fraction_other':r['F'],
            'cold_mass_minimum_if_Sextans_met':sx['F']*r['Mrem'],
            'minimum_to_required_cold_mass_ratio':sx['F']/r['F'],
            'necessary_stock_upper_for_reversed_rank':sx['Mrem']*sx['R']/r['R']})
# Adversarial controls: reverse target ordering or reverse the aperture rank.
def conflict(x1,F1,x2,F2):return x2>x1 and F2<F1
controls={'actual_conflict':conflict(1,.99,2,.02),
          'monotone_targets_not_rejected':not conflict(1,.02,2,.99),
          'reversed_arguments_not_rejected':not conflict(2,.99,1,.02)}
assert all(controls.values())
result={'claim':'A common nonnegative cumulative radial profile with universal eta and stock-fixed wave similarity scaling cannot meet the older four-dwarf central fractions',
        'derivation':'Li=eta_phys^2/(eta_code^2 G Mi); xi=Ri/Li proportional Mi Ri; F(x) is nondecreasing. A common retained fraction is included in F, not separately fitted.',
        'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'rows':rows,'contradictions':contradictions,'controls':controls,
        'scope':'Conditional central-value homology obstruction only. Fixed older stock/baseline; not uncertainty-aware, newer Sextans likelihood, general nonhomologous field evolution, or all-action no-go.'}
(b/'homology_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(contradictions,indent=2))
