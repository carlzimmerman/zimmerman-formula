"""Assemble documentary tables from pinned lane evidence; no physics is rerun."""
import json, re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
req={
'C01':'One parent action and force/source ledger',
'C02':'Formed state, abundance and lifetime',
'C03':'Health, stability and multistream/vacuum completion',
'C04':'Cold total stress and cosmology',
'C05':'Derived scales and normalizations',
'C06':'Galaxy normalization and trends jointly',
'C07':'Dwarfs and required response ordering',
'C08':'Cluster radial profile on measured gas',
'C09':'Lensing, Milky Way and DiskMass',
'C10':'Retained radial response to baryonic evolution',
'C11':'Physical state/environment selection',
'C12':'Reciprocal transfer and finite budgets'}
rows=[]
for name in ['foundational','observational','audit','coordinator']:
 rows.extend(json.loads((HERE/f'{name}_rows.json').read_text()))
sources=[r for p in sorted((HERE/'inputs').glob('*/SOURCES.json')) for r in json.loads(p.read_text())]
source_by_id={r['id']:r for r in sources}
row_by_id={r['id']:r for r in rows}
(HERE/'lane_matrix.json').write_text(json.dumps({'schema_version':1,'requirements':req,'rows':rows},indent=2)+'\n')
(HERE/'sources.json').write_text(json.dumps(sources,indent=2)+'\n')
def esc(x):return str(x).replace('|','\\|').replace('\n',' ')
def ref(ids):return ', '.join(f'[{i}](LANE_MATRIX.md#{i.lower()})'for i in ids)
def srcref(ids):return ', '.join(f'[{source_by_id[i]["source_path"]}]({source_by_id[i]["snapshot_path"]})' for i in ids)
text=['# Lane evidence matrix','',f'{len(rows)} scoped records. These are obligations and evidence fragments, not independent statistical votes. Eleven IDX records are summary-only family coverage. Status and scope must be read together. No row claims a complete theory pass.','',
'Each source link opens an immutable capture; its original path and SHA-256 are in [sources.json](sources.json). Internal links in captured reports retain their original repository context.','']
for r in rows:
 text += [f'## {r["id"]}', '',f'**{r["name"]}** — `{r["status"]}`. Parent: {r["parent"]}.', '',r['result'],'',f'**Obstruction:** {r["obstruction"]}', '',f'**Scope:** {r["scope"]}', '',f'**Obligations:** {", ".join(r["requirements"])}. **Aliases:** {", ".join(r["aliases"]) or "none"}.','',f'**Evidence:** {srcref(r["sources"])}','']
(HERE/'LANE_MATRIX.md').write_text('\n'.join(text))
text=['# Non-repetition register','','A continuation is new only if it addresses the named missing implication or changes a physical premise explicitly. New names, parameter sweeps, higher precision without an unresolved numerical question, and recombining mismatched passes do not qualify. Pending owned experiments are not fresh routes.','','| Record | Completed or blocked operation: do not repeat | Genuinely new obligation |','|---|---|---|']
for r in rows:text.append(f'| {ref([r["id"]])} | {esc(r["nonrepeat"])} | {esc(r["next_new_step"])} |')
(HERE/'NON_REPETITION.md').write_text('\n'.join(text)+'\n')
# Each matrix cell is a coarse documentary judgment, never an aggregate grade.
architectures=[]
def arch(i,name,parent,evidence,overrides,changes,verdict):
 cells={k:{'status':'open','note':'No completed same-parent demonstration of this obligation in the reviewed record.','evidence':evidence}for k in req}
 for k,(s,n,ev) in overrides.items():cells[k]={'status':s,'note':n,'evidence':ev or evidence}
 architectures.append(dict(id=i,name=name,parent=parent,evidence=evidence,cells=cells,changed_assumptions=changes,verdict=verdict))
P='partial';F='failed_on_record';D='fitted';O='open';N='not_applicable';Q='pending';X='excluded_as_stated'
arch('A01','Adopted no-floor native N','Native zoom/cold-profile phenomenology plus separate law',['OBS-NR2','OBS-NF1','OBS-LC1','OBS-ZN4','SYN09'],{
'C02':(P,'Native collisionless zooms exist; imposed core shape, mass assignment and field production are not derived.',[]),
'C05':(D,'Core shape and empirical mass line remain inputs; removing the floor is not deriving them.',[]),
'C06':(F,'Median normalization does not remove mass/brightness trends; full response breaks normalization.',['OBS-NR2','OBS-NR3']),
'C07':(F,'Dwarf/mass-extrapolation failures remain within the stated profile and mass map.',['OBS-ND1']),
'C08':(F,'Measured-gas outer keys fail; worst-key data audit remains pending.',['OBS-ZN4','AUD04']),
'C09':(F,'Local-mass and lensing issues remain on their own measured/reduction assumptions.',['OBS-RF1','OBS-BL1','OBS-UR3']),
'C10':(F,'Live smooth loading contracts rather than supplying the needed regulator; co-assembly pending.',['OBS-LC1','OBS-PZ1']),
},'No automatic PN28 or X48 mechanism substitution.','Not a joint survivor in its tested form; baseline requirements are conditional on its mass/profile mapping.')
arch('A02','Acceleration law alone','Executed S law; distinct from B certification and closed v3s completion',['AUD06','AUD07','AUD01'],{
'C05':(D,'kappa and relevant normalization not derived.',['AUD08','SYN09']),
'C06':(P,'Useful SPARC normalization/brightness behavior, not every galaxy or a parent-action result.',['AUD01']),
'C07':(F,'IC1613 tension persists, subject to inclination/systematic scope.',['OBS-RF2']),
'C08':(F,'Baryons plus the law leave cluster core/radial deficits.',['AUD01']),
'C09':(F,'Relative lensing advantage is not absolute adequacy; local vertical-force tension.',['AUD01','OBS-BL1']),
'C10':(N,'No additional cold-core state in the law-only hypothesis; cannot supply that requested mechanism.',[]),
'C12':(N,'No proposed cold transfer channel in the law-only hypothesis.',[]),
},'Would need a specified healthy completion and extra state to claim the full mechanism.','Useful empirical comparator, not a complete cold-field architecture.')
arch('A03','RM2 fitted response family','Native N with imposed mass-dependent response',['OBS-RM2','OBS-RM1'],{
'C05':(D,'Three fitted response parameters are not selected from a parent.',[]),
'C06':(D,'Six cells clear the specified five gates; this is a fitted subset.',[]),
'C07':(P,'Only the covered dwarf/ordering gates; independent dwarf closure not established.',[]),
'C08':(F,'12/15 cluster keys and adverse X-COP residuals.',[]),
'C10':(D,'Required weak response is inserted rather than evolved.',[]),
'C11':(D,'Mass trend is an inferred requirement, not physical selection.',[]),
},'A response derivation would replace fitted inputs and require complete regrading.','Requirement map, not a surviving mechanism.')
arch('A04','Corrected CSM1 core/switch','Older floored same-core selector with fitted L and basin postulate',['SYN01','SYN02'],{
'C05':(D,'One L is fitted; kappa and basin assignment remain unproved.',[]),
'C06':(P,'Registered canonical levels pass this gate, not all footings/objects.',[]),
'C07':(F,'Fixed alternate-UFD two-branch construction fails all positive L.',[]),
'C08':(P,'Registered calibration cluster keys pass; not a dynamical parent.',[]),
'C09':(F,'Primary levels fail lensing; sole refit instead fails groups.',[]),
'C11':(D,'Same-core bookkeeping is fixed but basin selection remains postulated.',[]),
},'An older floor architecture cannot be relabeled the adopted no-floor N.','Tested joint calibrations fail; remaining canonical L interval is not evidence of success.')
arch('A05','Dilute PN28 / FR01 / DR01','Dispersion-coupled scalar plus kinetic distribution, chosen waterbag; DR01 fast-scalar limit',['FND16','FND19','FND22','FND25','FND27'],{
'C01':(P,'Explicit reciprocal parent on its declared domain; not a vacuum/micro/galaxy-law completion.',['FND16','FND20']),
'C02':(O,'Waterbag and parameters selected; no formation/abundance prediction.',['FND20']),
'C03':(P,'Dilute finite screens pass; dense states have energy saddles, vacuum boundary unclosed.',['FND21','FND22','FND20']),
'C04':(O,'Cold total stress, cosmological population and B/V relation not supplied.',['FND18','FND20']),
'C05':(O,'Potential shape and B/V normalization independent.',['FND17','FND18']),
'C10':(O,'Static contraction is adverse; linear l=2 work has no completed l=0 regulation.',['FND23','FND27']),
'C12':(P,'Finite prescribed-pulse work/torque are controlled; live driver depletion uncomputed.',['FND25','FND26']),
},'Cannot inherit N observational fits or X48 heat flux by adding them.','Best ready continuation of a demonstrated reciprocal response, not a verified contraction cure.')
arch('A06','X48 entropy-memory transport','Phenomenological nonbarotropic Newtonian material law, fixed tested coefficients',['FND48','FND49','FND50','FND51','FND52','FND53'],{
'C01':(P,'Conserving semidiscrete mechanical/heat ledger; no microscopic covariant parent.',['FND48','FND50','FND53']),
'C02':(P,'Specified virgin sphere settles at N32–256; cosmological formation/abundance open.',['FND50']),
'C03':(P,'Scoped radial/core health and finite relaxation; uniform startup/3D/vacuum completion open.',['FND48','FND51','FND52']),
'C04':(O,'Quiet-domain inactivity is conditional; actual forest/cosmological history and total stress ungraded.',['FND53']),
'C05':(O,'a0 stress normalization and additional material scales are supplied, not derived.',['FND53']),
'C10':(P,'Same-pressure static cores resist smooth loading but still shrink; evolved baryonic response open.',['FND49','FND50']),
'C11':(P,'Explicit density/compression/entropy gates define selection, but observed populations not shown to occupy them.',['FND48','FND53']),
'C12':(P,'Internal transport returns mechanical work to heat; responsive baryon budgets absent.',['FND48','FND50']),
},'Separate experimental model: neither adopting N again nor deriving the a0 cold stress.','Strongest reviewed finite core-formation prototype; the parent realization and cross-system gates remain open.')
arch('A07','TP04 neutral cold state','Rigid microscopic neutral photino with independent scales and stipulated relic state',['FND34','FND37','FND38','FND39','FND40','FND41'],{
'C01':(P,'Concrete rigid microscopic calculation; gravity/vacuum/portal completion absent.',[]),
'C02':(P,'Named leading loss channels bounded; production and abundance assumed.',[]),
'C03':(P,'Finite retained-order particle stability evidence; omitted channels and embedding remain.',[]),
'C04':(P,'Stipulated FD travel can be cold; no full cosmological history and raw vacuum huge.',[]),
'C05':(O,'Independent mu/e/m and vacuum adjustment; tested rawV0=DE version fails.',['FND40','FND41']),
},'A cold particle branch is outside the standing field-only objective; not excluded as physics in general.','Conditional microscopic progress, not an eligible all-lane field mechanism or a galaxy repair.')
arch('A08','Tested single-barotrope subclasses','BOLTZ1 RF5 reconstruction / quadratic P(X) subclasses',['FND43','FND44','FND45'],{
'C01':(P,'Specified single-field effective action in tested classes.',[]),
'C03':(F,'Reconstructed RF5 release violates health in the stated class; dust multistream completion absent.',[]),
'C04':(P,'Pressureless timing limit works conditionally; does not realize healthy late turn-on.',[]),
'C05':(F,'Quadratic pressure-support scale is tiny rather than kpc under its stated bound; not every barotrope.',['FND45']),
'C10':(O,'No completed matched baryonic-response evolution in these barotrope subclasses.',[]),
},'Independent entropy/memory variables leave this single-barotrope hypothesis and need their own completion.','Scoped obstruction; not a no-go theorem for nonbarotropic field transport.')
arch('A09','Common-parent history-dependent transport target','A proposed mapping to one parent, not a constructed hybrid',['AUD12','FND48','FND50','FND53','FND16','FND18','FND27'],{},
'Must derive or explicitly reject the memory variables, transport law, scales, cold stress and physical gates from a named parent. Adding them by hand fails this route.',
'No demonstrated cell is inherited. This is the prioritized missing intersection, not a ninth established model.')
(HERE/'architecture_matrix.json').write_text(json.dumps({'requirements':req,'cell_statuses':{'partial':'Some named sub-obligations supported, not full pass','failed_on_record':'Adverse result with the stated model/data scope','fitted':'Chosen or fitted input, not prediction','open':'Uncomputed or not demonstrated in this parent','pending':'Owned result not finalized','not_applicable':'Not supplied by this candidate; does not erase project obligation','excluded_as_stated':'Analytical obstruction with explicit premises'},'architectures':architectures},indent=2)+'\n')
label={P:'Partial',F:'Fails*',D:'Fit',O:'Open',Q:'Pending',N:'—',X:'Excluded*'}
text=['# Candidate compatibility matrix','','**No reviewed candidate has a demonstrated full intersection.** “Partial” is not a pass; “Fails*” carries the model/data scope in the cell details. Columns are obligations, not equally weighted scores. The last row is an unbuilt target and deliberately inherits no passes.','','| Candidate | '+' | '.join(req)+' |','|---|'+'---|'*len(req)]
for a in architectures:text.append('| '+a['name']+' | '+' | '.join(label[a['cells'][k]['status']]for k in req)+' |')
text+=['','| Obligation | Meaning |','|---|---|']+[f'| {k} | {v} |'for k,v in req.items()]
for a in architectures:
 text += ['',f'## {a["id"]}: {a["name"]}','',a['verdict'],'',f'**Premises:** {a["parent"]}. {a["changed_assumptions"]}','','| Obligation | Status and scope | Evidence |','|---|---|---|']
 for k,c in a['cells'].items():text.append(f'| {k} | **{label[c["status"]]}:** {esc(c["note"])} | {ref(c["evidence"])} |')
(HERE/'ARCHITECTURES.md').write_text('\n'.join(text)+'\n')
# Index all immediate rebuild directories. Directory presence is inventory, not evidence of a verdict.
inventory=[]
for d in sorted((ROOT/'rebuild_2026_10_22').iterdir()):
 if not d.is_dir() or d.name.startswith('.'):continue
 prefix=str(d.relative_to(ROOT))+'/'
 ids=[s['id']for s in sources if s['source_path'].startswith(prefix)]
 linked=[r['id']for r in rows if set(r['sources']) & set(ids)]
 aliases=[r['id']for r in rows if r.get('coverage_level')=='index_summary_only' and any(d.name==x or d.name.startswith(x+'_')for x in r['aliases'])]
 inventory.append({'path':str(d.relative_to(ROOT)),'coverage':'direct_source_capture'if ids else 'indexed_family_only'if aliases else 'not_individually_assessed','rows':linked or aliases,'source_ids':ids})
(HERE/'coverage_inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
counts={k:sum(x['coverage']==k for x in inventory)for k in ('direct_source_capture','indexed_family_only','not_individually_assessed')}
text=['# Evidence coverage','','This matrix covers all major mechanism families identified in the current failure inventory and current response/microscopic/entropy-transport continuations. It does **not** represent a fresh audit of every experiment in the repository. Direct evidence means a report or result was read and pinned, not that its science was rerun. Full-path source records disambiguate colliding lane names.','',f'- {len(rows)} scoped lane/claim records, including 11 expressly summary-only historical family records.',f'- {len(sources)} pinned captures ({len(set(s["source_path"]for s in sources))} distinct original paths).',f'- Rebuild directory inventory: {len(inventory)} immediate directories; {counts["direct_source_capture"]} have direct source captures, {counts["indexed_family_only"]} additional directories map to indexed families, {counts["not_individually_assessed"]} are not individually assessed. Directory counts include support/audit areas and are not a count of independent mechanisms.','',
'Unassessed directories carry no failure or success weight. The old inventory itself had about 90 opened reports among about 330 lanes, with further title-only/brief entries; its assertions retain those limits. Current directly captured reports supersede stale titles and the inventory where identified. Claims of global uniqueness or a mathematically optimal winner would require broader review and are not made.','',
'## Coverage maps','','- [Foundational](FOUNDATIONAL_COVERAGE.md)','- [Observational](OBSERVATIONAL_COVERAGE.md)','- [Validity and model identity](AUDIT_COVERAGE.md)','- [Coordinator and older families](COORDINATOR_COVERAGE.md)','- [Every immediate rebuild directory](coverage_inventory.json)','- [All source paths and hashes](sources.json)','','## Concurrent evidence','','HB1, M3A1, FG1, PZ1 and DR8-B are pending as of the pinned evidence. A filename or a passing initializer is not a final scientific grade. Original source drift is reported by validate.py; captures are never silently refreshed during validation.','',
'No external novelty claim, full mathematical-proof audit, new likelihood comparison, new simulation, or exhaustive review of unrelated Standard Model/particle experiments is part of CM01. The route ranking is a reasoned priority for this core-mechanism objective, not a probability of ultimate success.']
(HERE/'COVERAGE.md').write_text('\n'.join(text)+'\n')
print(json.dumps({'rows':len(rows),'sources':len(sources),'architectures':len(architectures),'directory_inventory':counts}))
