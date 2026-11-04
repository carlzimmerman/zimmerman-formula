"""Checked local pole decays and their inverses on the common number grid.

Only the fixed pole packet is supported. Rep-averaged isotropic scalar decays
use their inclusive component widths, with actual group degeneracies in the
number measure. Daughters and Pauli/Bose factors are retained. No time history
or irreversible radiation replacement is implied by this factory.
"""
import json
import sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from angular_fast import exact_events_fast

POLE=25.4000254000381
NAME={'chi':'F1_1','lambda8':'F8_0','lambda2':'F3_0',
      'g3':'V8_T','g2':'V3_T','gY':'V1_T'}

def pole_events(data,t,q,W,packet=None):
    if abs(float(data['x'])-POLE)>1e-7:
        raise ValueError('Only the checked fixed pole packet is implemented')
    if packet is None:
        packet=json.loads((ROOT/'reviews/weak_completion_2026_11_04/decay/INTERFACE.json').read_text())
    groups=[dict(g) for g in data['groups']]
    by={g['id']:i for i,g in enumerate(groups)}
    if len(groups)!=30:
        raise ValueError('Requires the common30-group background')
    deviations={}
    channels=[]
    for parent in packet['parents']:
        expected=parent['parent_mass_GeV']/2e6
        found=groups[by[parent['id']]]['mass']
        deviations[parent['id']]=abs(found/expected-1)
        if deviations[parent['id']]>1e-5:
            raise ValueError('Parent mass is outside the local packet tolerance')
        for channel in parent['channels']:
            channels.append(dict(parent=parent['id'],
                daughters=[NAME[name] for name in channel['daughters']],
                width=channel['width_mu'],kind='checked_loop_pole'))
    local=dict(data,groups=groups,channels=channels)
    # No current-source replacement: this factory contains precisely the
    # checked loop channels. Quantum statistics are fixed for vector groups.
    out=exact_events_fast(local,t,q,W,source=None)
    out.eta=np.repeat([1 if g['kind'] in ('S','V') else -1 for g in groups],len(q))
    out.packet_mass_relative_deviations=deviations
    return out
