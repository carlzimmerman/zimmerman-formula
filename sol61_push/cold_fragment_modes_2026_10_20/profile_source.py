"""Regenerate the pinned stationary branch without executing source top level.

Only the two named function definitions are loaded from the local audited
common_action source. Parameters are read from its pinned completed result.
The caller declares both files as execution dependencies.
"""
from pathlib import Path
import ast, math, time, json
import numpy as np
from scipy.integrate import simpson, solve_bvp

ROOT=Path(__file__).resolve().parents[2]
PRIOR=ROOT/'sol61_push/cold_completion_2026_10_20'
P=json.loads((PRIOR/'run_001/results.json').read_text())['parameters']

def regenerate(Q,L=60.,tol=1e-8):
    tree=ast.parse((PRIOR/'common_action.py').read_text())
    defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('check','solve')]
    assert {n.name for n in defs}=={'check','solve'}
    env={'np':np,'math':math,'time':time,'json':json,'simpson':simpson,'solve_bvp':solve_bvp,
         'M':P['M_chi'],'a':P['a'],'g':P['g'],'MX2':P['MX2'],'lam':P['lambda'],
         'rows':[],'checks':[]}
    exec(compile(ast.Module(body=defs,type_ignores=[]),'pinned_stationary_definitions','exec'),env)
    s,row=env['solve'](float(Q),float(L),1000,tol)
    assert all(q['pass'] for q in env['checks']),env['checks']
    assert s.status==0
    return s,row
