"""Execute isolated production-source fragments on synthetic audit fixtures.
These fixtures test logical guarantees, not actual survey predictions.
"""
import ast
import json
from pathlib import Path
import textwrap
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / 'campaign_fresh_gravity/CFG592_cosmic_shear_likelihood/cfg592_native.py'
MAIN = ROOT / 'campaign_fresh_gravity/CFG650_theory_v2_combined_pm/cfg650_native.py'
fn = next(n for n in ast.parse(LIB.read_text()).body
          if isinstance(n, ast.FunctionDef) and n.name == 'support_mask')
# One redshift node, two multipoles, one bin pair. k=1 is supported, k=2 is not.
# Kernel/Hankel weights are positive and unity; nuisance shift is zero.
ns = {'np':np, 'BG':{'PM':(np.array([1.]),)}, 'LN':np.array([.5, 1.5]),
      'nuis_spec':lambda *args: (None,None,None,lambda _: {'dz':[0.]},None),
      'kernels':lambda *args: (np.ones((1,1)),np.ones((1,1)),np.ones(1))}
exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(LIB),'exec'),ns)
s={'pairs':[(1,1)], 'Ap':np.ones((1,2)), 'Am':np.ones((1,2)),
   'isp_all':np.array([True]), 'ip_all':np.array([0]), 'ia_all':np.array([0])}
run={'k_lo':.5,'k_hi':1.5}
f0=float(ns['support_mask'](s,run,np.array([[19.],[1.]]))[0])
ff=float(ns['support_mask'](s,run,np.array([[19.],[100.]]))[0])
assert np.isclose(f0,19/20) and f0>=.9
assert np.isclose(ff,19/119) and ff<.9

source=MAIN.read_text()
begin=source.index('        t_ok = TOWN.get(')
end=source.index('        pS = ',begin)
gate=textwrap.dedent(source[begin:end])
start=source.index('        if "EXCLUDED" in cl: VER[foot]')
stop=source.index('    RESULT["verdict_per_footing"]',start)
summary=textwrap.dedent(source[start:stop])
results=[]
for name,town in [('missing',{}),('failed',{'fixture':{'test':False}}),('passed',{'fixture':{'test':True}})]:
    env={'TOWN':town,'run':{'name':'fixture'},'sn':'test','r':{},
         'cls':'CONSISTENT','cls_noIA':'CONSISTENT'}
    exec(compile(gate,str(MAIN),'exec'),env)
    survey={**env['r'],'class':env['cls']}
    final={'cl':[env['cls']],'VER':{},'foot':'canonical', 'r':{'surveys':{'test':survey}}}
    exec(compile(summary,str(MAIN),'exec'),final)
    results.append({'case':name,'survey_class':env['cls'],
                    'metadata':env['r'],'verdict':final['VER']['canonical']})
assert results[0]['survey_class']=='CONSISTENT'
assert results[0]['verdict'].startswith('PASS') and 'PROVISIONAL' in results[0]['verdict']
assert results[1]['survey_class']=='NOT DIAGNOSTIC'
assert results[1]['verdict']=='NOT DIAGNOSTIC'
assert results[2]['verdict']=='PASS (shear side, this footing)'

# A high supported fraction of an absolute integrand is not a relative-error
# bound on its signed integral: supported signed sum=+1, omitted sum=-1.
# Supported absolute contributions 100 and 99 give 199/200=99.5% support.
assert (100+99)/(100+99+1) == .995
assert 100-99-1 == 0

result={'support':{'control_fraction':f0,'candidate_fraction':ff,
                  'candidate_to_control_outside_ratio':100.,'inside_ratio':1.},
        'gate_cases':results,
        'signed_integral_example':{'supported_absolute':199,'outside_absolute':1,
                                   'supported_signed':1,'full_signed':0},
        'scope':'Synthetic source-fragment tests. No survey rerun, no claim actual cuts fail.',
        'source_lines':{'support_mask':fn.lineno,
                        'gate':source[:begin].count('\n')+1,
                        'verdict':source[:start].count('\n')+1}}
Path(__file__).with_name('support_gate_run').joinpath('result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
