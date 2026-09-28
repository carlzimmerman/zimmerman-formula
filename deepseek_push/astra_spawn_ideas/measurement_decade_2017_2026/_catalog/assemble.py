"""Render authored work orders. Does not dispatch agents or execute physics."""
from pathlib import Path
import json,hashlib,re,datetime
HERE=Path(__file__).resolve().parent
OUT=HERE.parent
BASE=OUT.parent
ROOT=BASE.parents[1]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def dump(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def link(p,fromdir):
 import os
 return os.path.relpath(p,fromdir)
def slug(s): return re.sub('[^a-z0-9]+','_',s.lower()).strip('_')[:130].rstrip('_')
sources=[];tasks=[]
for year in range(2017,2027):
 ss=json.loads((HERE/f'{year}_sources.json').read_text());tt=json.loads((HERE/f'{year}_tasks.json').read_text())
 assert len(ss)>=10 and len(tt)==250,(year,len(ss),len(tt))
 sources.extend(ss);tasks.extend(tt)
by_source={s['source_id']:s for s in sources}
assert len(by_source)==len(sources)
assert len({t['id'] for t in tasks})==2500
pinned_paths=['STANDING.md','qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md',
 'real_research/breakthrough_review_2026_09_26/README.md','real_research/common_action_2026_09_26/README.md',
 'deepseek_push/astra_spawn_ideas/FRAMEWORK_CONTRACT.md',
 'deepseek_push/astra_spawn_ideas/FIRST_PRINCIPLES_AND_BRANCHING.md',
 'deepseek_push/astra_spawn_ideas/ORCHESTRATOR.md',
 'deepseek_push/astra_spawn_ideas/measurement_decade_2017_2026/DISPATCH.md',
 'deepseek_push/astra_spawn_ideas/measurement_decade_2017_2026/RESULT_CONTRACT.json']
pinned={p:digest(ROOT/p) for p in pinned_paths}
dump(OUT/'FRAMEWORK_SOURCES.json',{'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Actual local bytes, including concurrent uncommitted changes. Task execution must review freshness; catalog assembly is not acceptance of every source claim.','sources':pinned})
dump(OUT/'sources.json',{'cutoff':'2026-09-27','year_rule':'First public measurement report or actual data release; observation epoch is separate.','verification_scope':'Primary report/release metadata and reported observables; payloads not audited unless explicitly stated. Hashes below identify authored source records, not remote webpage bytes.','sources':[{**s,'record_sha256':canonical(s)} for s in sources]})
framework='''Use the [core framework contract](../../FRAMEWORK_CONTRACT.md), current [standing](../../../../STANDING.md), and the [amended thirteen-gate specification](../../../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md). The amendment overrides historical targets. Pin the same action, physical metric, matter coupling, source/state domain, boundary conditions and parameter cell throughout. Read the pinned source list below before selecting a candidate; this card does not assert that any current candidate is closed.

The scale relation is `a0=(c/2)*sqrt(G_N*rho_Lambda)` with vacuum **mass density** in kg/m³; `kappa=1/2` is adopted unless independently derived. Evaluate dimensional examples separately at canonical `a0=9.3619e-11 m/s²` and alternative `1.1279e-10 m/s²`. Changing a0 with fixed kappa changes rho_Lambda. Keep measured `G_N`, action `G_E` and cosmological coupling distinct: `Lambda_eff=32*pi*(G_E/G_N)*a0²/c⁴`. If V0 denotes SI vacuum energy density, `a0²=G_N*V0/4` and `H_vac²=8*pi*G_E*V0/(3*c²)` under the stated vacuum-background assumptions.

The operative branch is **filtered MONO**, not an interchangeable scalar fit. Let `B=g_bar`, `y=B/a0`, `h_RAR=y*(nu_RAR-1)`, `nu_RAR=1/(1-exp(-sqrt(y)))`; use `h'_mono=max(h'_RAR,0.05*h_p/(y+y_p))`, with the specified continuous join. Rounded landmarks `y_star≈2.3374`, `y_p≈2.5396` are not exact roots. The filter is `S=exp(xi²*Delta/2)`; its adjoint depends on metric, measure and boundary domain. Derive the field/metric observation map before evaluating data. `r>>xi` can justify a controlled approximation, not exact equality with `xi=0`.

Comparison laws `Q: g²=B²+a0*B`, `RAR: g=B*nu_RAR(B/a0)`, and `MU2: [1-(1+g/(2*a0))^-2]*g=B` are distinct; historical EXP is separate. Never silently substitute them for filtered MONO or assume spherical identities hold for arbitrary sources. Use criterion **B** with a consistent preferred foliation and well-posed mixed problem, not an unproved blanket speed requirement. Count gravitational and permitted matter modes separately. No unannounced particle species, per-object force correction or quantum completion. A published GR/LambdaCDM posterior is a conditional derived product until translated.

The thirteen gates cover: static MONO; gravitational modes; both potentials/lensing; PPN; matter conservation; tensor sector; stability/criterion B; expanding cosmology; zero-field limits; Newton/GR and measured G; one physical metric; prescribed RAR/MONO segment; and the a0–vacuum relation. Successful observation-level evidence supplies only its stated edge in this common-action dependency graph.'''
for t in tasks:
 s=by_source[t['source_id']];year=t['year'];folder=OUT/str(year);folder.mkdir(exist_ok=True)
 filename=f"{t['id']}_{slug(t['title'])}.md"
 p=folder/filename
 deps=', '.join(t['depends_on']) or 'No predeclared seed-ID dependency. Discover and register the exact theory/data dependencies before execution; this does not imply the observation map already exists.'
 sections=[f"# {t['id']} — {t['title']}",f"**Year:** {year} · **Source:** {s['source_id']} · **Kind:** {t['kind']} · **Priority:** {t['priority']}\n\nStatus: authored work order, not an execution receipt or scientific result.",
 '## Dated measurement anchor',f"[{s['title']}]({s['primary_url']}) — {s['authors_or_collaboration']}. Identifier: `{s['identifier']}`.\n\nDated report/release anchor: **{s['report_date']}** ({s['date_precision']} precision). Date basis: {s['date_basis']}. Version: {s['version']}. Observations: {s['observation_epoch']}.\n\nReported measurement: {s['measurement']}\n\nData availability: {s['data_access']}\n\nVerification scope: {s['verification']} Locator: {s['source_locator']}. Checked {s['checked_on']}. These metadata authenticate an anchor; the proposed calculations below are original work orders and are not claims made by its authors.\n\nSource-record SHA-256: `{canonical(s)}` (metadata only; hash acquired payloads separately).",
 '## Core framework and first-principles footing',framework,
 '## Principle and exact mathematical target',t['principle'],f"Mathematical starting relation/estimand:\n\n```text\n{t['math']}\n```\n\nDefine every symbol, units, sign, domain and approximation before use. Treat schematic formulas as obligations to derive, not established framework theorems.",
 '## Measurement inputs and unique new information',t['measurement_input'],t['new_information'],
 '## Ordered execution', '\n'.join(f'{i}. {v}' for i,v in enumerate(t['steps'],1)),
 '## Falsifiable controls','\n'.join(f'- {v}' for v in t['controls']),
 'A negative control is deliberately wrong. Show why it should fail in the stated domain. If the actual data cannot distinguish it, report limited identifiability; do not fabricate rejection or declare the correct model false. Predeclare tolerances and preserve failed controls.',
 '## First-principles obligation and closure bridge',t['first_principles'],t['closure_bridge'],
 'Separate primitive assumptions, measured calibrations, boundary/initial data, derived consequences and unresolved implications. Any worker may pursue a complete same-action witness through the [closure template](../../CLOSURE_WITNESS_TEMPLATE.md), but independent review of all gates is required. A fit or successful numerical example is not a derivation of the action, coefficient or vacuum scale.',
 '## Required output and completion condition',t['deliverable'],
 f"Write the actual result and artifacts under `measurement_decade_2017_2026/results/{t['id']}/<unique-run-id>/`. Use [RESULT_CONTRACT.json](../RESULT_CONTRACT.json), including actual model identity, exact claim, execution/acceptance status, source/data/artifact hashes, equations, controls, tested range, overlap treatment, failed routes and next missing implication. A symbolic proof-only result needs its raw derivation and independent review. An unavailable dataset produces a precise blocked inference, not a synthetic substitute. A record is review-ready only when every field is supplied or explicitly marked not applicable with a reason.",
 '## Reuse, overlap and prerequisites',f"Declared dependencies: {deps}",t['overlap_handling'],
 'Before claiming work, search both seed manifests, child registries and live AS/MY/FGF claims/results. Reuse an existing generic theorem or active owner. New title/year alone is not novelty. Shared objects, pixels, events, calibrations or simulations need a joint covariance, conditional increment, or separate alternative analysis; do not multiply dependent evidence.',
 '## Finding-driven continuation', '\n'.join(f'{i}. **{label}:** {v}' for i,(label,v) in enumerate(zip(['Promising result','Independent bridge','Failure or obstruction'],t['continuation']),1)),
 f"These are candidate branches, not preapproved scientific conclusions. A child must cite an actual parent result and evidence hashes, name its new equation/estimand, closest existing task, substantive difference, controls, prerequisites and finite resources. Use `{t['id']}.C01` etc. with a unique claim and write scope; descendants remain provisional until reviewed. At most two live children per parent and two levels before orchestrator reconciliation; later reviewed waves may continue. Follow [DISPATCH.md](../DISPATCH.md) and the [first-principles protocol](../../FIRST_PRINCIPLES_AND_BRANCHING.md). If no runner is available, return a ready child specification without claiming it ran.",
 '## Pinned local base', '\n'.join(f'- [{q}]({link(ROOT/q,folder)}): `{h}`' for q,h in pinned.items())]
 content='\n\n'.join(sections)+'\n'
 p.write_text(content)
 t.update(path=f'{year}/{filename}',task_sha256=digest(p),source_record_sha256=canonical(s),scientific_fingerprint=canonical({k:t[k] for k in ['source_id','principle','math','deliverable','new_information']}))
# Do not remove any old file automatically; validator detects unexpected stale renderings.
dump(OUT/'manifest.json',{'schema_version':1,'status':'authored_seed_specifications','cutoff':'2026-09-27','task_count':len(tasks),'years':list(range(2017,2027)),'per_year':250,'source_count':len(sources),'tasks':tasks})
index=['# Measurement-decade task index','2,500 additional individual work orders; 250 per year. [Source ledger](SOURCES.md) · [Dispatch](DISPATCH.md) · [Original 2,000](../INDEX.md).\n\nEach link opens a separate task file. These are specifications, not completed calculations.']
source_lines=['# Dated primary-source ledger','100 report/release anchors. Each supports 25 distinct proposed work orders; this is not a list of 2,500 independent datasets. Report dates and observation epochs differ. All sources were checked on 2026-09-27; exact payload availability and full likelihood inspection are stated per source. [Machine-readable records](sources.json).']
for year in reversed(range(2017,2027)):
 index.extend([f'\n## {year} — 250 tasks','', '| ID | Source | Task |','|---|---|---|'])
 source_lines.append(f'## {year}')
 yt=[t for t in tasks if t['year']==year]
 yi=[f'# {year}: 250 task files','[Full decade index](../INDEX.md) · [Source ledger](../SOURCES.md)']
 for t in yt:
  index.append(f"| {t['id']} | {t['source_id']} | [{t['title'].replace('|','/')} ]({t['path']}) |")
  yi.append(f"- [{t['id']} — {t['title']}]({Path(t['path']).name})")
 (OUT/str(year)/'INDEX.md').write_text('\n\n'.join(yi)+'\n')
 for s in [s for s in sources if s['year']==year]:
  source_lines.extend([f"### {s['source_id']} — {s['title']}",f"[{s['identifier']}]({s['primary_url']}) · {s['authors_or_collaboration']}",f"**Report/release:** {s['report_date']} ({s['date_precision']}). {s['date_basis']}. **Version:** {s['version']}.",f"**Observation epoch:** {s['observation_epoch']}",f"**Measured:** {s['measurement']}",f"**Access:** {s['data_access']}",f"**Verification:** {s['verification']} **Locator:** {s['source_locator']}",f"**Overlap family:** `{s['overlap_family']}`. Discovery queries: "+'; '.join(s['search_queries'])])
(OUT/'INDEX.md').write_text('\n'.join(index)+'\n')
(OUT/'SOURCES.md').write_text('\n\n'.join(source_lines)+'\n')
print(json.dumps({'rendered_tasks':len(tasks),'sources':len(sources),'years':10,'pinned_local_files':len(pinned)}))
