"""Read-only FN6 engines. Only explicit definition/initialization slices execute."""
import ast
import hashlib
import importlib.util
import os
from pathlib import Path
import sys
sys.dont_write_bytecode=True
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
    os.environ[key]='1'
ROOT=Path(__file__).resolve().parents[2]
FN6=ROOT/'finish_2026_11_04/FN6_powerlaw_screening'
FN1B=ROOT/'finish_2026_11_04/FN1_action_call/FN1b_fixed_length_static'

def hashes():
    paths=[FN6/'fn6_small.py',FN6/'fn6_mw.py',FN1B/'vendor_kt33/mw_reciprocal.py',FN1B/'vendor_kt33/cassini_v2.py']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def small():
    p=FN6/'fn6_small.py'
    tree=ast.parse(p.read_text(),filename=str(p))
    stop=next(n.lineno for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=='KP == 0 and (not MUT)')
    nodes=[n for n in tree.body if n.lineno<stop]
    nodes += [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_point']
    nodes += [n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ORDER' for t in n.targets)]
    ns={'__file__':str(p),'__name__':'az43_fn6_small'}
    argv=sys.argv
    try:
        sys.argv=[str(p),'--part','1/1']
        exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
    finally:
        sys.argv=argv
    return ns

def mw():
    sys.path.insert(0,str(ROOT/'rebuild_2026_10_22/UX5_mw_stellar_mass'))
    import ux5_core
    p=FN1B/'vendor_kt33/mw_reciprocal.py'
    spec=importlib.util.spec_from_file_location('az43_mw_reciprocal',p)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def local_cells():
    import itertools
    for sb,mbb,rd,ht,hk,fk in itertools.product([48.8,50.5,52.2],[2e10,2.06e10,2.12e10],
            [2.6-1/12,2.6,2.6+1/12],[.325,.3375,.35],[.99,1.035,1.08],[.305,.3275,.35]):
        yield dict(box='BV2',sb=sb,mbb=mbb,rd=rd,ht=ht,hk=hk,fk=fk,rdk=2.)

def points():
    from fractions import Fraction
    pp=[Fraction(1,4)+i*Fraction(1,40) for i in range(11)]
    ll=sorted(set([Fraction(1)+i*Fraction(1,4) for i in range(9)]+[Fraction(s) for s in ['1.450','1.475','1.525','1.550']]))
    return [(float(p),float(l)) for p in pp for l in ll]
