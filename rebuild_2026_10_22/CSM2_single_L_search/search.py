#!/usr/bin/env python3
"""Necessary group/lens tests only, reusing the audited CSM1 corrected scorer."""
import argparse
import contextlib
import io
import json
import pathlib
import sys
import time

DRIVER_FILE = pathlib.Path(__file__).resolve()
PROGRAM_DIR = DRIVER_FILE.parent
PROJECT = PROGRAM_DIR.parents[1]
REPLAY = PROJECT/'rebuild_2026_10_22/CSM1_consistent_core_switch/calibration/calibrate_replay.py'
REFERENCE = REPLAY.parent/'run_003_audited/results.json'
frozen_levels = [2.5205071316768617,2.625,2.75,2.875,3.,3.125,3.25,3.375,3.5,3.625,3.75,3.9,4.,4.5,5.]
parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parsed = parser.parse_args()
SAVED_OUTPUT = pathlib.Path(parsed.output).resolve()
SAVED_OUTPUT.mkdir(parents=True,exist_ok=True)
original = REPLAY.read_text()
prefix = original[:original.index("RESULT=dict(assertion_tested=")]
anchor = ' # preserve transformed source as an executed artifact, not as an overwrite of any old lane'
assert prefix.count(anchor) == 1
injection = ''' if 'x43_collapse_core.py' in str(src_path):
  # Identify the exact final scoring loop, after all definitions and self-tests.
  marker = '\\nfor f in FEET:\\n    P(f"\\\\n=== ['
  assert src.count(marker) == 1, ('group-only marker',src.count(marker))
  src = src[:src.index(marker)] + '\\nfor f in FEET:\\n    RES["footings"][f] = dict(groups=grade_groups(f))\\n'
'''
prefix = prefix.replace(anchor,injection+anchor)
(SAVED_OUTPUT/'executed_helper_prefix.py').write_text(prefix)
saved_argv = sys.argv
sys.argv=[str(REPLAY),'--output',str(SAVED_OUTPUT),'--reference',str(REFERENCE),'--skip-baseline']
__file__ = str(REPLAY)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(prefix,str(REPLAY),'exec'),globals())
__file__ = str(DRIVER_FILE)
sys.argv = saved_argv
read(DRIVER_FILE)
read(PROGRAM_DIR/'TARGET.md')
RESULT2 = dict(scope='Finite necessary-constraint search, no continuous-L exclusion',levels={},checks={},inputs={})


def save():
    RESULT2['inputs'] = dict(INPUTS)
    dump(RESULT2,'results.json')


def groups_at(level):
    data = child_call('x43','on',f'shpS9_L{level:.17g}_B','corrected')
    return data,{f:data['result'][0]['footings'][f]['groups'] for f in FEET}


if __name__ == '__main__':
    control,g = groups_at(3.75)
    baseline = REF['levels']['3.75']['grade']
    RESULT2['checks']['group_reduction_reproduces_full_CSM1'] = all(
        g[f] == baseline[f]['own']['groups'] for f in FEET)
    lens_control = child_call('x53','on','shpS9_L3.75','corrected')
    RESULT2['checks']['lens_reproduces_CSM1'] = all(abs(
        lens_control['result'][f]['all']['H2H']['chi2']-baseline[f]['lensing']['ENV2H'])<1e-8 for f in FEET)
    RESULT2['baseline']=dict(groups=control,lens=lens_control)
    save()
    assert all(RESULT2['checks'].values()),'Reduced scorer baseline failed'
    for level in frozen_levels:
        raw,gr=groups_at(level)
        cell=dict(groups=gr,group_raw=raw)
        if gr['canonical']['PASS']:
            lens=child_call('x53','on',f'shpS9_L{level:.17g}','corrected')
            cell['lens_raw']=lens
            cell['lens_delta_law']={f:lens['result'][f]['all']['H2H']['chi2']-lens['result'][f]['all']['L2H']['chi2'] for f in FEET}
            cell['canonical_survives_necessary_tests']=cell['lens_delta_law']['canonical']<=9
        else:
            cell['canonical_survives_necessary_tests']=False
            cell['lensing_skipped']='Canonical groups fail unchanged necessary criterion'
        RESULT2['levels'][repr(level)]=cell
        save()
        print('LEVEL',level,'groupsZ',gr['canonical']['Z'],'lens',cell.get('lens_delta_law'),
              'candidate',cell['canonical_survives_necessary_tests'],flush=True)
    RESULT2['checks']['all_levels_covered']=len(RESULT2['levels'])==len(frozen_levels)
    RESULT2['checks']['normal_flags_correct']=all(
        all(q['expected']==q['actual'] for q in c['group_raw']['flags']) and
        all(q['expected']==q['actual'] for q in c.get('lens_raw',{}).get('flags',[]))
        for c in RESULT2['levels'].values())
    RESULT2['checks']['inputs_stable']=all(hashp(p)==h for p,h in INPUTS.items())
    RESULT2['rss_GB']=max(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)/1e9
    RESULT2['checks']['rss_under_1GB']=RESULT2['rss_GB']<1
    save()
    assert all(RESULT2['checks'].values())
