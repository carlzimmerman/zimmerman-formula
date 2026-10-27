from pathlib import Path
import json,hashlib,re
out=Path('sol61_push/framework_certification_2026_10_12/assumptions'); regpath=out/'assumption_register.json'; reg=json.loads(regpath.read_text()); entries={x['id']:x for x in reg['entries']}; sources={x['path']:x for x in reg['source_snapshots']}
nodes=[]; edges=[]
def ref(path,needle):
 b=Path(path).read_bytes(); text=b.decode(); hits=[i+1 for i,l in enumerate(text.splitlines()) if needle in l]; assert hits,(path,needle)
 sources[path]={'path':path,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'lines':len(text.splitlines())}
 return {'path':path,'line':hits[0],'sha256':sources[path]['sha256'],'excerpt':text.splitlines()[hits[0]-1]}
def refs(i): return entries[i]['sources']
def node(i,scope,assertion,kind,attainment,status,postulates,locs,earliest=''):
 nodes.append(dict(id=i,scope=scope,assertion=assertion,gate_kind=kind,attainment_from_current_record=attainment,current_status=status,v2_postulates=postulates,sources=locs,earliest_missing_implication=earliest))
def edge(i,fr,to,arrow,status,missing,locs): edges.append(dict(id=i,from_nodes=fr,to_node=to,implication=arrow,status=status,missing_input=missing,sources=locs))
EQ='achievable from current supplied equations'; MISS='needs a missing equation'; WAIT='pending measurement'
P='axiomatic phenomenology'; D='derived classical mechanism'; T='stronger theory of everything'
for n in range(1,10):
 i='A'+str(n); node('POSTULATE-'+i,P,entries[i]['claim'],'postulate declaration',EQ,'explicit premise; not certified as a fact about nature',[i],refs(i))
node('P-conditional-algebra',P,'The 18 exact Lean statements follow from their explicit premises','formal implication',EQ,'existing source-matched kernel compilation report', ['A1','A2','A7'],refs('LEAN-scale_squared'))
node('P-implementation-correspondence',P,'Analytic nu and tabulated repaired implementation agree to a declared domain/error bound','implementation theorem',EQ,'not formalized; finite table and code are available',['A2'],refs('A2-implementation'),'Exact analytic definition/domain of repaired nu plus grid/interpolation/error theorem; available implementation allows bounded certification, not universal identity.')
node('P-profile-reconstruction',P,'For each declared source/nu and supply, reconstruct spherical enclosed cold mass and declared edge bound','formal implication',EQ,'conditional target and radius algebra already certified',['A2','A6','A7'],refs('LEAN-target_mass_unique'))
node('P-prescribed-drift-IVP',P,'Existing masked prescribed drift admits nonnegative conserved solutions with stated initial/boundary data','PDE theorem',MISS,'not certified; phase/boundary switch regularity and receiver are unspecified',['A2','A5','A6'],refs('O-selector'),'Specify regularity/domain/boundary flux and actual mask/phase evolution before proving an initial-value problem.')
node('P-empirical-summary',P,'Existing postulated-law observations are correctly labelled conditional and finite','evidence scope',EQ,'already audited; no universal empirical truth proof',['A1','A2','A3','A5','A6','A7','A8','A9'],refs('E-raw-gates'))
node('P-independent-cosmology',P,'Predict cosmological observations without inherited Lambda-CDM functions','physical prediction',MISS,'not supplied',['A1','A3','A4','A5','A6','A7','A9'],refs('O-cosmology'),'Axiomatically specifying an acceleration law does not define background/linear perturbation evolution.')
# All exact frozen CFG678 gates, including correction-forward C2 and A5.
p678='campaign_fresh_gravity/CFG678_one_action_contract/FROZEN_CRITERIA.md'; s678='campaign_fresh_gravity/CFG678_one_action_contract/SCORECARD.md'
map678={
'A1':(['A7'],MISS,'varied dynamics and constraint/kinetic matrices'),
'A2':(['A7'],MISS,'principal symbol for full coupled equations'),
'A3':(['A5','A6','A7'],MISS,'complete PDE, constraints and admissible initial/boundary domain'),
'A4':(['A7'],MISS,'specified action/couplings and strong-coupling calculation'),
'A5':(['A7'],MISS,'common metric action/tensor characteristics'),
'A6':(['A7'],MISS,'full field equations and black-hole exterior solutions'),
'A7':(['A7'],MISS,'specified quantum/UV action and radiative analysis'),
'B1':(['A5','A6'],MISS,'bound/phase selector from variation with reaction'),
'B2':(['A1','A4'],MISS,'non-postulated vacuum tie with constrained degree count'),
'B3':(['A3','A5','A6','A7'],MISS,'cold sector, receiver and lensing stress from same action'),
'C1':(['A2','A7'],MISS,'same-action screened weak-field solution; existing filtered chassis is conditional'),
'C2':(['A1','A2'],EQ,'current law can run existing SPARC harness; not proof of mechanism'),
'C3':(['A2','A3','A5','A6','A7','A9'],EQ,'current phenomenology can be scored, with empirical mass/calibration/supply inputs explicit'),
'C4':(['A2','A3','A6','A7'],MISS,'derive finite-supply outer mass/lensing profile; observed upper bound exists but prediction was not frozen'),
'D1':(['A1','A4','A5'],MISS,'zero-field/full background reduction with actual switch'),
'D2':(['A3','A5','A6','A7','A9'],MISS,'independent background/perturbations/transport and scorer support; historical conditional simulations remain valid records'),
'D3':(['A1','A4'],WAIT,'future held-out redshift observations; no Lean replacement'),
'E1':(['A1'],MISS,'selection principle producing kappa'),
'E2':([],MISS,'unitary quantum completion'),
'E3':([],MISS,'quantum/SM structure derivation')}
for i,(axioms,att,missing) in map678.items():
 loc=ref(p678,'| '+i+' |'); exact=loc['excerpt'].split('|'); scope=T if i.startswith('E') or i=='A7' else D
 node('CFG678-'+i,scope,exact[2].strip()+'; frozen line: '+exact[3].strip(),'source-contract gate',att,'pending observation' if att==WAIT else ('conditionally evaluable from present prescription' if att==EQ else 'unresolved for current framework action'),axioms,[loc],missing)
# CFG679 rules and every M/S/data gate.
p679='campaign_fresh_gravity/CFG679_mechanism_contract/FROZEN_CRITERIA.md'; p2='campaign_fresh_gravity/CFG679_mechanism_contract/PART2_FROZEN_CRITERIA.md'
for i,needle in [('R0','**R0. No target in.**'),('R1','**R1. Constants.**'),('R2','**R2. No new thresholds.**'),('R3','**R3. One action.**')]:
 att=MISS if i in ['R0','R3'] else EQ
 node('CFG679-'+i,D,ref(p679,needle)['excerpt'].strip(),'candidate admission',att,'FAIL current target-in prescription' if i=='R0' else ('missing action' if i=='R3' else 'current contract is available'),['A2','A5','A6'] if i in ['R0','R3'] else [],[ref(p679,needle)],'independently derived law-generating dynamics' if i=='R0' else ('complete varied action' if i=='R3' else 'prospective candidate declarations; do not silently change historical gates'))
mm={
'M1a':(['A2','A5','A6'],MISS,'target-free attractor and independently declared non-law initial states'),
'M1b':(['A1','A3','A4'],MISS,'derived physical rate/capacity and framework age; 13.8 Gyr remains a stated input'),
'M1c':(['A3','A7'],MISS,'full coupled principal symbol and bounded high-k proof'),
'M2a':(['A5','A6','A7','A9'],MISS,'same-action stress tensors/reactions and exact Noether identity'),
'M2b':(['A3','A4','A5'],MISS,'named receiver field plus signed energy/current equations'),
'M3a':(['A2','A3','A7'],MISS,'candidate own lensing response from same dynamics; raw datasets exist'),
'M3b':(['A7'],MISS,'common photon/tensor metric characteristics'),
'M3c':(['A2','A7'],MISS,'same-action Solar-System screening and Cassini observable'),
'C3':(['A2','A3','A5','A6','A7','A9'],EQ,'existing prescribed model can be scored; mechanism cannot count a pass without own action'),
'D2':(['A3','A5','A6','A7','A9'],MISS,'independent cosmology and nonlinear prediction'),
'D3':(['A1','A4'],WAIT,'unreleased redshift measurement')}
for i,(axioms,att,missing) in mm.items():
 loc=ref(p679,'| '+i+' |'); parts=loc['excerpt'].split('|')
 node('CFG679-'+i,D,parts[2].strip()+'; frozen line: '+parts[3].strip(),'source-contract gate',att,'pending measurement' if att==WAIT else 'not passed for any full supplied action',axioms,[loc],missing)
pj='campaign_fresh_gravity/MECHANISM_JOINT_2026-10-12.md'
ss={1:['A1','A4'],2:['A5','A6','A8'],3:['A5','A6'],4:['A3','A7'],5:['A2'],6:['A2','A3'],7:['A3','A4'],8:['A3','A5'],9:['A2','A3']}
for n,axioms in ss.items():
 i='S'+str(n); loc=ref(pj,'| '+i+' |'); att=WAIT if n==8 else MISS
 node('CFG679-'+i,D,loc['excerpt'],'selector source requirement',att,'S8 source says pending mergers; other S properties may hold by postulate but are not derived mechanism passes',axioms,[loc], 'merger observations/completed declared lane; timing still needs equations' if n==8 else 'same-action candidate deriving property; assigning postulate is not derivation')
node('D-quantitative-microphysical-selection',D,'Vacuum normalization, criticality/kernel/cubic and abundance coefficients have independent origins','physical derivation',MISS,'none supplied',['A1','A2','A3'],refs('O-normalization'))
node('D-autonomous-phase',D,'Hot/condensed phase state and own catchment follow autonomous conserved evolution','physical derivation',MISS,'missing W_int/phase/thermal/boundary dynamics',['A5','A6','A9'],refs('E-census-phase'))
node('D-independent-background',D,'Full framework background/linear perturbations and initial spectrum follow specified evolution','physical derivation',MISS,'borrowed chain currently used',['A1','A3','A4','A7'],refs('O-cosmology'))
node('TOE-closed',T,'Derived classical mechanism, selected constants, quantum gravity/radiative control and Standard-Model structure with predictions','aggregate source-contract conjunction',MISS,'declared research goal, not achieved',[],refs('O-TOE'))
# Dependencies are explicit proof arrows, not loose tasks.
for n in range(1,10): edge('postulate-'+str(n),['POSTULATE-A'+str(n)],'P-empirical-summary','Treat A'+str(n)+' as an explicit physical premise, not a Lean consequence','available conditional premise','',refs('A'+str(n)))
edge('arrow-scale-not-selection',['POSTULATE-A1','P-conditional-algebra'],'D-quantitative-microphysical-selection','a0=kappa c sqrt(G rho_DE) -> unique kappa and abundance','unresolved','Additional selection equation/principle; coefficient_family explicitly permits arbitrary kappa',refs('LEAN-coefficient_family'))
edge('arrow-target-not-selector',['POSTULATE-A2','POSTULATE-A5','P-profile-reconstruction'],'CFG679-R0','Reconstructed target -> independently generated evolution/profile attractor','unresolved','No target-free action/operator supplied; inserting rho_ph violates R0',refs('O-selector'))
edge('arrow-phase-not-dynamics',['POSTULATE-A5','POSTULATE-A9'],'D-autonomous-phase','Separate condensed source postulate -> autonomous phase conversion and its conserved interaction','unresolved','Chosen W_int and Gamma/thermal stress law are missing',refs('O-bound-switch'))
edge('arrow-ownership-not-current',['POSTULATE-A6'],'CFG678-B1','Per-host supply label -> dynamically formed catchments/ownership and reciprocal forces','unresolved','Bound-system ownership/current law and reactions',refs('O-bound-switch'))
edge('arrow-conservation-not-receiver',['P-conditional-algebra'],'CFG679-M2b','Algebraic Q+(-Q)=0 -> actual receiver field permitting both signs','unresolved','Named field/action and its energy and momentum equations',refs('O-receiver'))
edge('arrow-convex-not-gravitating',['P-conditional-algebra'],'CFG679-M1c','Fixed-source response-energy positivity -> full live-matter PDE health','unresolved','Coupled action, constraints, principal symbol and initial-value domain',refs('O-health'))
edge('arrow-gravitates-not-metric',['POSTULATE-A7'],'CFG679-M3b','Real mass gravitational convention -> same metric photon/tensor propagation','unresolved','Covariant metric/matter equations and characteristics',refs('O-lensing'))
edge('arrow-law-not-cosmology',['POSTULATE-A1','POSTULATE-A3','POSTULATE-A4'],'D-independent-background','Scale, abundance and redshift postulates -> unique expansion/linear transfer/initial conditions','unresolved','Background/perturbation closure and independent parameter inference',refs('O-cosmology'))
edge('arrow-future-data-not-proof',['POSTULATE-A4'],'CFG679-D3','Sealed flat-a0 prediction -> confirmation by future measurement','pending measurement','Actual held-out data; no formal theorem substitutes for observation',refs('O-pending'))
edge('arrow-classical-not-toe',['CFG679-R0','CFG679-R3','CFG679-M1c','CFG679-M2b','D-independent-background'],'TOE-closed','Classical completion -> quantum and Standard-Model derivation','unresolved','Quantum action/UV/unitarity and SM selection equations',refs('O-TOE'))
# Three distinct existing continuations. These are preparation, no new candidate physics.
nl='sol61_push/nonlocal_response_2026_10_12/RESULT.txt'; rf='sol61_push/metric_polarization_2026_10_12/REFERENCE_FIELD_RESULT.md'; pa='sol61_push/polarization_assembly_2026_10_12/RESULT.txt'; ph='sol61_push/phase_source_closure_2026_10_12/RESULT.txt'
routes=[
{'id':'ROUTE-spatial-nonlocal-environment','existing_continuation':'sol61_push/nonlocal_response_2026_10_12','material_difference':'Spatial variational filter annihilates uniform gradients; no adaptive reference-field dynamics or receiver-channel lift.','target_gates':['CFG679-S2','CFG679-S3','CFG678-B1'],'cheapest_discriminator':'Use the existing fixed-L periodic experiment with a displaced finite host source; compare the satellite internal-force profile with host absent/present at the same declared L and unchanged parameters. A uniform-gradient repeat is insufficient. Declare spatial profile, tidal gradient and tolerance prospectively.','available_equations':True,'earliest_missing_equation':'Kernel is inverse-designed from nu, L is not derived; no causal realization/conserved positive cold-mass current. A successful host test still fails R0 derivation.','no_escalation_rule':'No galaxy fit or production PM run until finite-host sensitivity, boundary and positive-mass interpretation are resolved.','sources':[ref(nl,'add a displaced finite source'),ref(nl,'The kernel is inverse-designed'),ref(nl,'integral rho_eff=0')]},
{'id':'ROUTE-adaptive-reference-boundary','existing_continuation':'sol61_push/metric_polarization_2026_10_12','material_difference':'Additional adaptive reference vector changes constitutive energy and cancels uniform fields dynamically; test its long-wavelength boundary tradeoff rather than static spatial filtering.','target_gates':['CFG679-S2','CFG679-S3','CFG679-M3a','CFG679-M1c'],'cheapest_discriminator':'Before a new solve, impose the existing exact radial sum equation -L_r(gamma q+K_R s)=GM/r^2 on any proposed finite cosmological boundary. Check whether derived matching removes the constant-force branch with universal physical coefficients and preserves the internal shift symmetry. No new boundary model is supplied; the immediate cheapest result is an admission/no-go calculation of a SPECIFIED matching law.','available_equations':True,'earliest_missing_equation':'Actual cosmological boundary or regular reference-sector action. Quadratic isolated tail already fails; p=3/2 repair has M^2 correction and singular vacuum.','no_escalation_rule':'Do not repeat uniform-field tests or fit free stiffness/boundary separately by galaxy. Still R0-SHAPED until coefficients/action independently derived.','sources':[ref(rf,'The spherical cost is exact'),ref(rf,'The next substantive question'),ref(rf,'V_\\infty^2')]},
{'id':'ROUTE-autonomous-source-assembly','existing_continuation':'sol61_push/polarization_assembly_2026_10_12 plus phase_source_closure_2026_10_12','material_difference':'Source assembly, cooling/phase information and baryon feedback are the selection hypothesis; replace prescribed source trajectory instead of adding filter or reference field. Excludes constructing any kinetic receiver/Hamiltonian bracket.','target_gates':['D-autonomous-phase','CFG678-B1','CFG679-M1a','CFG679-M2a'],'cheapest_discriminator':'Apply the existing exact same-total-density hot/condensed phase-pair discriminator to the candidate source representation and expose the prescribed a(t) dependency. Then require an existing documented stress/cooling/source law that predicts a(t); if absent, stop at that exact missing equation. The known zero-field contraction result provides a comparator, not autonomous formation.','available_equations':False,'earliest_missing_equation':'Autonomous baryon continuity/momentum/thermal stress or cooling equation and phase law. Existing contraction is prescribed, inverse-designed W and scalar response do not satisfy R0 or relativistic lensing.','no_escalation_rule':'Do not relabel source work as total conservation; no arbitrary drag/schedule, no receiver-lift duplication, no full halo run before actual source closure is supplied.','sources':[ref(pa,'Next decisive route'),ref(pa,'W was inverse-designed'),ref(ph,'Route 1: exact phase-information'),ref(ph,'W_int must')]}]
# Connect every source gate to its actual adopted premises and to the scoped contract conjunction.
for nd in list(nodes):
 if nd['id'].startswith('POSTULATE-') or not nd['v2_postulates']: continue
 edge('premises-'+nd['id'],['POSTULATE-'+a for a in nd['v2_postulates']],nd['id'],'Explicit postulates identify dependency only; they do not discharge a derivation or measurement gate','dependency only','',nd['sources'])
node('CFG679-MECHANISM-PASSES',D,'Exact frozen mechanism conjunction; all M, S except S8, C3 and D2 must pass, subject to admission rules','aggregate source-contract conjunction',MISS,'not met',['A1','A2','A3','A4','A5','A6','A7','A8','A9'],[ref(p679,'**MECHANISM PASSES**')],'At least R0/R3 and M dynamical equations missing; provisional S8 allowance is not full closure.')
required679=['CFG679-'+i for i in ['R0','R1','R2','R3','M1a','M1b','M1c','M2a','M2b','M3a','M3b','M3c','S1','S2','S3','S4','S5','S6','S7','S9','C3','D2']]
edge('mechanism-conjunction',required679,'CFG679-MECHANISM-PASSES','All named required gates PASS on both footings; S8 may remain PENDING only under this exact narrower contract','unresolved','Unpassed gate conjunction; pending S8 is explicitly excluded from this proof conjunction',[ref(p679,'**MECHANISM PASSES**')])
node('CFG678-CLASSICAL-SOURCE-CONTRACT',D,'All CFG678 structure/B/C/D gates with their original conditional/declared/pending labels; stronger than conditional algebra','aggregate source-contract conjunction',MISS,'no candidate action passes',[],[ref(s678,'**No candidate passes')],'Missing action and empirical derivations; pending D3 is not a mathematical leaf.')
edge('classical-source-contract-conjunction',['CFG678-'+i for i in map678 if not i.startswith('E')],'CFG678-CLASSICAL-SOURCE-CONTRACT','Required structural and observational obligations evaluated under frozen lines; pending/declared cannot silently become passes','unresolved','Unresolved varied equations plus pending measurement and A7 radiative obligation',[ref(s678,'**No candidate passes')])
edge('toe-conjunction',['CFG679-MECHANISM-PASSES','CFG678-CLASSICAL-SOURCE-CONTRACT','CFG678-E1','CFG678-E2','CFG678-E3'],'TOE-closed','Actual classical success plus all declared stronger E gates -> stated broader closure target','unresolved','The source record does not supply those equations or measurements',refs('O-TOE'))

# exact scope conjunctions make phenomenological/theory distinction explicit.
scopes=[{'id':P,'meaning':'Certifies conditional definitions, algebra, specified numerical implementation and finite evidence scope under A1-A9. Does not derive the postulates or certify they describe nature.','current_reachable_nodes':['P-conditional-algebra','P-profile-reconstruction','P-implementation-correspondence','P-empirical-summary'],'currently_unreachable_nodes':['P-prescribed-drift-IVP','P-independent-cosmology']}, {'id':D,'meaning':'CFG678 structural/B/C/D and CFG679 admission/M/S/data conjunction. Properties merely imposed by A1-A9 do not pass derivation gates.','contract_allowance':'CFG679 permits S8 PENDING for its narrower mechanism verdict. That allowance does not convert S8 into a proof or justify whole-theory completion.','not_a_guarantee':'A fully specified admissible action can still fail data.'},{'id':T,'meaning':'Adds CFG678 E1-E3 plus radiative/quantum/SM obligations; not supplied by a classical receiver component.'}]
result=dict(schema_version=1,claim_id='FRAMEWORK-CERT-2026-10-12-SOURCE-CLOSURE-GRAPH',scope='Source-contract graph only, not root aggregate verdict or closure certificate',parent_assumption_register_sha256=hashlib.sha256(regpath.read_bytes()).hexdigest(),attainment_enum=[EQ,MISS,WAIT],scope_definitions=scopes,nodes=nodes,edges=edges,unresolved_arrows=[e['id'] for e in edges if e['status']=='unresolved'],earliest_unresolved_arrows=[e['id'] for e in edges if e['status']=='unresolved' and e['id'].startswith('arrow-') and e['id']!='arrow-classical-not-toe'],pending_measurement_arrows=[e['id'] for e in edges if e['status']=='pending measurement'],next_routes=routes,route_exclusions=['No kinetic_receiver_lift work','No Hamiltonian/GENERIC/channel lift work','No new physical ansatz invented in this preparation','No active simulations started/stopped/modified'],source_snapshots=list(sources.values()),symmetry_rule=reg['symmetry_rule'],measurement_rule='Pending or future empirical measurements can never be converted into Lean proofs. Mathematical predictions and measurement acceptance are separate leaves.')
(out/'closure_gate_graph.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
# Mechanical completeness/integrity checks, preserving earlier audit and its integrity file.
assert len(map678)==20
assert all('POSTULATE-A'+str(n) in {x['id'] for x in nodes} for n in range(1,10))
assert len({x['id'] for x in nodes})==len(nodes)
assert all(x['attainment_from_current_record'] in result['attainment_enum'] for x in nodes)
assert all(all(f in {n['id'] for n in nodes} for f in e['from_nodes']) and e['to_node'] in {n['id'] for n in nodes} for e in edges)
for s in result['source_snapshots']: assert hashlib.sha256(Path(s['path']).read_bytes()).hexdigest()==s['sha256'],s['path']
print(json.dumps({'nodes':len(nodes),'edges':len(edges),'routes':len(routes),'source_snapshots':len(sources),'CFG678_gates':len(map678),'all_structural_checks_pass':True}))
