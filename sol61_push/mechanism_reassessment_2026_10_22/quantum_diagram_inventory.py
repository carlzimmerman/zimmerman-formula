"""Exact Wick-contraction inventory for selected unshifted complex-action terms.
Counts carry no contour phases. NOT a derived numerical self-energy solver.
"""
from itertools import permutations,combinations
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json,sys,math
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
def connected(n,edges,removed=()):
 reach={0}
 for _ in range(n):
  before=len(reach)
  for i,(_,a,b) in enumerate(edges):
   if i in removed:continue
   if a in reach or b in reach:reach.update((a,b))
  if len(reach)==before:break
 return len(reach)==n
rows=[]
for ng,nl in [(0,1),(1,0),(0,2),(1,1),(2,0),(0,3),(1,2),(2,1),(3,0),(0,4)]:
 # g+ vertices X* Phi Phi; g- conjugate; quartic vertices Phi^2 Phi*^2.
 plus=list(range(ng));minus=list(range(ng,2*ng));quart=list(range(2*ng,2*ng+nl));nv=2*ng+nl
 phi_plus=[v for v in plus+quart for _ in range(2)];phi_minus=[v for v in minus+quart for _ in range(2)]
 # Repeated labels in permutations intentionally count distinguishable Wick legs.
 graphs=Counter()
 for pm in permutations(phi_minus):
  phi_edges=[('p',a,b) for a,b in zip(phi_plus,pm)]
  for xm in permutations(minus):
   edges=tuple(sorted(phi_edges+[('x',a,b) for a,b in zip(plus,xm)]));graphs[edges]+=1
 total=sum(graphs.values());expected=math.factorial(len(phi_plus))*math.factorial(ng)
 assert total==expected
 skeleton=[];conn=0;count2pi=0
 for edges,mult in graphs.items():
  if not connected(nv,edges):continue
  conn+=mult
  if any(not connected(nv,edges,cut) for size in (1,2) for cut in combinations(range(len(edges)),size)):continue
  count2pi+=mult
  skeleton.append(dict(directed_edges=edges,wick_multiplicity=mult,expansion_weight=str(Fraction(mult,math.factorial(ng)**2*math.factorial(nl)))))
 rows.append(dict(cubic_each_sign=ng,quartic_vertices=nl,vertices=nv,internal_edges=3*ng+2*nl,vacuum_loops=ng+nl+1,total_Wick_contractions=total,expected_Wick_contractions=expected,connected_contractions=conn,two_particle_irreducible_contractions=count2pi,sum_positive_combinatorial_weight=str(Fraction(count2pi,math.factorial(ng)**2*math.factorial(nl))),labeled_skeletons=skeleton))
 print(ng,nl,count2pi,flush=True)
checks=dict(total_counts=all(r['total_Wick_contractions']==r['expected_Wick_contractions'] for r in rows),quartic_double_bubble=rows[0]['sum_positive_combinatorial_weight']=='2',cubic_sunset=rows[1]['sum_positive_combinatorial_weight']=='2',quartic_basketball=rows[2]['sum_positive_combinatorial_weight']=='2',absorption_orders_four_loop=all(r['vacuum_loops']==4 for r in rows if (r['cubic_each_sign'],r['quartic_vertices']) in [(1,2),(2,1),(3,0)]),contact_four_to_two_five_loop=rows[-1]['vacuum_loops']==5)
out=dict(checks=checks,all_pass=all(checks.values()),inventory=rows,scope='Exact selected Wick-graph combinatorics with unshifted vertices and normal charge-conserving propagators. Not full broken/coherent-background 2PI functional, contour signs, anomalous propagators, counterterms, or time evolution. Not every perturbative cut requires a new 2PI skeleton; dressing generates reducible pieces.')
(O/'results.json').write_text(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
