"""Bounded source/cache audit; never runs or rewrites L291's output files."""
from pathlib import Path
import json
import pickle
import sys
import sympy as sp

base=Path('real_research/reviews/coherence_audit_2026_09_20/carrier_action')
O,S=pickle.load((base/'L291_cache_snapshot.pkl').open('rb'))
O=[sp.sympify(e) for e in O]
S={k:([sp.sympify(e) for e in v] if k=='amps' else sp.sympify(v)) for k,v in S.items()}
t,a,Qb,k,KB,beta,xi=[S[n] for n in ('t','a','Qb','k','KB','beta','xi')]
psi,bb,phi,tt,pp,cc=S['amps']
subs={Qb:0,sp.diff(Qb,t):0,S['F0']:0,S['F1']:0,S['F2']:0,xi:0}
E=[sp.simplify(e.subs(subs).doit()) for e in O]
scalar_target=2*(2-KB)*k**2*sp.sqrt(a**6)/a**2*(psi-sp.diff(tt,t)-beta*pp)
assert sp.simplify(E[4]-scalar_target)==0
assert E[3].has(sp.diff(pp,t))
assert not E[4].has(sp.diff(pp,t))
assert isinstance(S['G1'],sp.Symbol) and isinstance(S['G2'],sp.Symbol)
assert not any(e.has(sp.Derivative(S['G1'],t)) for e in O)
results=json.loads(Path('real_research/clock_2026/L291_frw_ymod_carrier_results.json').read_text())
report={
  'cache_provenance':'Pinned snapshot of /tmp/L291_frw_odes_chi.pkl; not a fresh complete builder run.',
  'actual_equation_order':['lapse','momentum','trace','clock','scalar','chi'],
  'cold_scalar_equation':str(sp.factor(E[4])),
  'cold_scalar_constraint':'P=(Psi-Tdot)/beta for k!=0, a>0, beta!=0, KB!=2',
  'clock_contains_Pdot':E[3].has(sp.diff(pp,t)),
  'scalar_contains_Pdot':E[4].has(sp.diff(pp,t)),
  'G1_type':type(S['G1']).__name__,
  'G2_type':type(S['G2']).__name__,
  'coefficient_derivatives_present':False,
  'source_reduction_uses_wrong_index':{'lines':'L291:76,96','source':'Eq[3]','actual':'clock, not scalar'},
  'test_threshold_errors':{
    'V2':'line167 compares an eigenvalue already divided by H against 10 H, not 10.',
    'V3':'line175 allows 0.3*0.52*3 = 0.468 absolute difference, a 90% rather than 30% tolerance.',
    'V4':'lines197-207 use Euclidean state norm instead of density contrast and require only growth_ratio<6, with no lower bound.'},
  'source_output_snapshot':{
    'all_scanned_growth_rates_zero':all(v['max_re_per_efold']==0 for row in results['eigen_scan'].values() for v in row.values()),
    'late_growth':results['late_growth']},
  'claim_scope':'Source and cached symbolic-equation audit; no coupled reduced-system integration certified.'}
Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
