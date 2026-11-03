"""Coverage accounting only; no observational grading or inherited pass claims."""
import json
from pathlib import Path
root=Path(__file__).resolve().parent;repo=root.parent
source=repo/'rebuild_2026_10_22/RQ3_acceptance_v2/row_marks.json'
ids=json.loads(source.read_text())['all_rows'];assert len(ids)==99 and len(set(ids))==99
group=lambda k:'A23' if k in ['A23a','A23b'] else ('A26' if k in ['A26a','A26b','A26c'] else k)
groups=sorted(set(map(group,ids)));assert len(groups)==96
candidates=[('Newtonian tidal Gaussian','AZ1',['kappa=0.5 FITTED'],'FAIL (inherited external-field conditional)'),('Prescribed conservative filter','AZ2/AZ8',['kappa=0.5 FITTED','physical D function and scales unspecified; FITTED if selected'],'NO VERDICT (operator only; plug-in action fails)'),('Centred gas transport','AZ3',['kappa=0.5 FITTED','physical amplitude and width unspecified; FITTED if selected'],'FAIL (single-clump displacement only)'),('Quartic shear','AZ4',['kappa=0.5 FITTED','lambda unspecified dimensionful: FITTED','quartic operator choice posited, counted model choice'],'FAIL (universal local contraction cure only)'),('Compression energy','AZ7',['kappa=0.5 FITTED','C unspecified: FITTED','p=2 posited operator choice; FITTED if selected as physical free exponent'],'FAIL (reduced mechanics only)'),('First resolvent','AZ9',['kappa=0.5 FITTED','n=1 family choice posited'],'NO VERDICT (convergence)'),('Squared resolvent','AZ10/AZ11',['kappa=0.5 FITTED','n=2 minimally regular integer within posited family; family choice not derived'],'NO VERDICT on full model; partial Cassini PASS and planetary diagnostic FAIL')]
out={'disclaimer':'κ = ½ FITTED; not theory closed','rq3_provenance':{'path':str(source.relative_to(repo)),'expanded_ids':99,'original_groups':96,'note':'The prose still says 96 after splitting A23 and A26. Report both, without editing source.'},'rule':'Credit only a whole row on BOTH footings for the SAME candidate. Algebra controls and conditional subgates earn zero. Zero credit is not a fail on uncomputed rows.','candidates':[]}
for name,lanes,free,status in candidates:
    empty=lambda:{'canonical':'NOT EVALUABLE','alt':'NOT EVALUABLE','both_footings_credited':False}
    rr={str(i):empty() for i in range(1,13)};rq={i:empty() for i in ids}
    if name=='Squared resolvent':
        for rid,note in [('C2','AZ10 reduced Cassini PASS: 0.104499678616 / 0.266319165200 ceiling; full field action absent'),('C1','AZ11 direct-radius diagnostic FAIL: Saturn Z 4.631128824608404 / 7.5129964361919415; full orbit interpretation restricted before result')]:
            rq[rid]={'canonical':'NO VERDICT','alt':'NO VERDICT','both_footings_credited':False,'partial_gate':note}
    rg={g:{'member_ids':[i for i in ids if group(i)==g],'both_footings_credited':all(rq[i]['both_footings_credited'] for i in ids if group(i)==g)} for g in groups}
    out['candidates'].append({'candidate':name,'lanes':lanes,'rank_by_certified_coverage':1,'scope_status':status,'free_numbers':free,'requirements_both_count':sum(q['both_footings_credited'] for q in rr.values()),'rq3_expanded_both_count':sum(q['both_footings_credited'] for q in rq.values()),'rq3_grouped_both_count':sum(q['both_footings_credited'] for q in rg.values()),'requirement_rows':rr,'rq3_expanded_rows':rq,'rq3_grouped_rows':rg})
(root/'coverage.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('7 constructions: 12 requirement rows, 96 grouped / 99 expanded RQ3 rows each; zero certified joint-footing coverage.')
