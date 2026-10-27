from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path.cwd(); OUT=ROOT/'sol61_push/framework_certification_2026_10_12/assumptions'
T='campaign_fresh_gravity/THEORY_v2_CANDIDATE_2026-10-12.md'
J='campaign_fresh_gravity/MECHANISM_JOINT_2026-10-12.md'
C678='campaign_fresh_gravity/CFG678_one_action_contract/FROZEN_CRITERIA.md'
S678='campaign_fresh_gravity/CFG678_one_action_contract/SCORECARD.md'
C679='campaign_fresh_gravity/CFG679_mechanism_contract/FROZEN_CRITERIA.md'
P679='campaign_fresh_gravity/CFG679_mechanism_contract/PART2_FROZEN_CRITERIA.md'
S679='campaign_fresh_gravity/CFG679_mechanism_contract/PART2_SCORECARD.md'
L='sol61_push/gravity_architecture_lean_2026_10_12/Architecture.lean'
R='sol61_push/gravity_architecture_lean_2026_10_12/README.md'
A='sol61_push/lcdm_dependency_audit_2026_10_12/RESULT.txt'
PM='campaign_fresh_gravity/CFG596_lean_pm_1024/cfg596_pm.py'
SC='campaign_fresh_gravity/CFG592_cosmic_shear_likelihood/cfg592_native.py'
CL='campaign_fresh_gravity/CFG637_derived_reservoir/cfg637_lib.py'
sources={}; entries=[]
def read(p):
 b=(ROOT/p).read_bytes(); text=b.decode(); sources[p]={'path':p,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'lines':len(text.splitlines())}; return text
texts={p:read(p) for p in [T,J,C678,S678,C679,P679,S679,L,R,A,PM,SC,CL,'sol61_push/gravity_architecture_lean_2026_10_12/run/results.json','sol61_push/gravity_architecture_lean_2026_10_12/run/manifest.json','sol61_push/gravity_architecture_lean_2026_10_12/contract.json']}
def loc(p,needle):
 lines=texts[p].splitlines(); hits=[i+1 for i,s in enumerate(lines) if needle in s]; assert hits,(p,needle)
 return {'path':p,'line':hits[0],'matching_lines':hits,'sha256':sources[p]['sha256'],'excerpt':lines[hits[0]-1]}
def add(i,cat,claim,status,refs,depends=None,limit=''):
 entries.append({'id':i,'classification':cat,'claim':claim,'status':status,'sources':[loc(*x) for x in refs],'dependencies':depends or [],'certification_limit':limit})
FP='framework postulate'; M='independently proved math'; E='empirical input'; B='borrowed ΛCDM/standard MOND'; O='open dynamical obligation'
# The current candidate has nine expressly named axioms. Each remains a premise.
for i,needle,claim in [
 ('A1','| A1 |','a0 = kappa c sqrt(G rho_DE), kappa=1/2, two separate acceleration footings'),
 ('A2','| A2 |','g=nu_mono(gN/a0) gN; repaired empirical interpolation and monotonic tail'),
 ('A3','| A3 |','Cold gravity-only collisionless component; q=Omega_c/Omega_b=5.364; no added particle species'),
 ('A4','| A4 |','a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE(0))'),
 ('A5','| **A5 (new)** |','Law target is sourced by own condensed stars and cold gas, excluding hot baryons'),
 ('A6','| **A6 (new)** |','Supply is per host catchment; no pooling across overlapping catchments'),
 ('A7','| A7 |','Ordinary gravity responds to all real gravitating mass'),
 ('A8','| A8 |','No external-field effect on internal dynamics'),
 ('A9','| A9 |','Baryons missing from halo census are expelled')]:
 add(i,FP,claim,'assumed in current candidate',[(T,needle)],limit='Formalizing this as a hypothesis proves only conditional implications; evidence/derivation is recorded separately.')
add('E-kappa',E,'kappa=1/2 is a fitted choice; cited CFG493 estimate is 0.42 +/-0.10','reported fit; raw likelihood not rerun',[(T,'κ FITTED'),(J,'**INPUT**, κ fitted')],['A1'])
add('E-footings',E,'Both acceleration footings 9.36e-11 and 1.13e-10 m/s^2 are evaluated separately','declared input',[(C679,'Both footings')],['A1'])
add('B-abundance',B,'q is imported from omega_c/omega_b=0.1200/0.02237 in a Planck cosmological fit; not model-independent measured abundance','confirmed source/code dependency',[(A,'ratio q=omega_c/omega_b'),(CL,'h = 0.6736; OM_B')],['A3'], 'No fresh check of the primary external paper in this bounded source audit.')
add('B-background',B,'Flat Lambda background E(a)=sqrt(Om/a^3+OL), h=0.6736, omega_b=0.02237, omega_c=0.1200 enter PM dynamics','confirmed current code dependency',[(PM,'h = 0.6736'),(PM,'E = lambda a:')])
add('B-spectrum',B,'EH transfer, ns=0.965, sigma8=0.811 input normalization and Dgrow backscaling set initial conditions','confirmed current code dependency',[(PM,'NS, SIG8 ='),(PM,'def T_eh'),(PM,'_PK *= SIG8'),(PM,'Di = Dgrow(AI)')],['B-background'])
add('B-supply',B,'Turnaround shell table, retention function and fixed 0.315/0.674 catchment geometry drive supply','confirmed current code dependency',[(A,'imports cfg361_delta_ta_table.json'),(PM,'def fret_of'),(PM,'def M_ta'),(PM,'Mbn = fr * FB')],['B-background','B-abundance','A6'])
add('B-scorer',B,'Native scorer continues unmeasured k/z regions with EH/Dgrow and inherited background distances and lensing Om','confirmed continuation code plus audited geometry provenance',[(SC,'def T_eh'),(SC,'Pm[:, j] = np.exp'),(A,"BG['PM'] fixes")],['B-background','B-spectrum'])
add('B-model-comparators',B,'HMcode/BAHAMAS/Tinker/Duffy/Moster/NFW-based lanes remain context only, equally for apparent success and failure','audit restriction',[(A,'Older HMcode/BAHAMAS/Tinker/Duffy/Moster/NFW')])
add('B-MOND-scope',B,'AQUAL, AeST, superfluid, dipolar and modified-inertia assumptions occur in tested comparator classes; they are not premises deriving framework A2 or A8','comparator only; standard MOND EFE is explicitly rejected by A8',[(S679,'AeST / single-metric'),(S679,'Superfluid phonons'),(S678,'strict AQUAL fails')],['A2','A8'],'Shared deep-law algebra is adopted as framework A2. Removing standard MOND assumptions does not derive the adopted interpolation.')
add('E-raw-gates',E,'SPARC/KiDS/Cassini/GW/cluster observations and analysis likelihoods are empirical inputs, not theorem conclusions','reported existing lanes; no raw reanalysis here',[(C679,'| M3a |'),(C679,'| M3c |'),(C679,'| C3 |'),(S678,'| C2 SPARC |')])
add('E-age-bound',E,'t_settle<=13.8 Gyr is a declared physical bound; framework age must be derived or independently inferred to remove inherited cosmology','conditional physical input',[(C679,'| M1b |')],['B-background'])
add('E-census-phase',E,'Census floor, assumed gas profile/cooling closure and per-system retention drive candidate phase/supply tests','conditional analysis inputs',[(A,'It still inherits PM cosmology/supply'),(A,'self-similar core growth, per-system catchment')],['A5','A6','A9'])
add('G-one-action',FP,'Each gate must follow from variation of one action; hand masks and ties do not count as a pass','frozen admission rule',[(C678,'An action, not a recipe'),(C679,'**R3. One action.**')])
add('G-no-target',FP,'Selector admission excludes target-in and law-shaped free functional forms','frozen R0 criterion',[(C679,'**R0. No target in.**'),(P679,'an input scores FAIL')]) if 'an input scores FAIL' in texts[P679] else add('G-no-target',FP,'Selector admission excludes target-in and law-shaped free functional forms','frozen R0 criterion',[(C679,'**R0. No target in.**'),(P679,'its source says so')])
add('G-constants',FP,'At most one universal new constant declared before scoring; G,c,a0 or rho_DE and baryons allowed; no per-system constant','frozen R1 criterion',[(C679,'**R1. Constants.**')])
add('O-selector',O,'Supply non-target-derived evolution with law profile as attractor for declared non-law initial states and both footings','missing; current settling fails R0',[(C679,'| M1a |'),(S679,'| K1 class-A settling |'),(T,'**Settling drift**')],['A2','A5','A6','G-no-target','G-one-action'],'Do not promote a stationary solution or imposed target to a derived attractor.')
add('O-bound-switch',O,'Derive bound/condensed switch and reciprocal baryon reaction from same action','missing construction',[(S678,'| B1 switch from variation |'),(T,'**Settling drift**')],['A5','A6','G-one-action'])
add('O-receiver',O,'Named field in same action permits signed energy exchange, balances momentum and produces transport/receiver conservation identity','missing; ghost-condensate is only sketch',[(C679,'| M2a |'),(C679,'| M2b |'),(T,'**Energy hand-off**'),(J,'signed exchange')],['G-one-action'])
add('O-health',O,'Full coupled equations are ghost-free, hyperbolic, nonlinearly well posed in stated domain, and sufficiently weakly coupled','unproved for candidate B; fixed-source energy positivity insufficient',[(C678,'| A1 |'),(C678,'| A2 |'),(C678,'| A3 |'),(S678,'| A1 ghost / order |'),(S679,'δ²H ≥ 0')],['G-one-action'])
add('O-lensing',O,'Same metric produces gravitational/lensing response and c_T=1 while meeting Cassini; no separate non-lensing force completion','missing coupled construction',[(C679,'| M3a |'),(C679,'| M3b |'),(C679,'| M3c |'),(S679,'| K3 non-lensing response')],['A7','O-health'])
add('O-normalization',O,'Derive kappa, vacuum tie, abundance and selector coefficients, rather than fitting or imposing them','missing derivation',[(J,'**(a) Coefficients.**'),(T,'Ω_c/Ω_b = 5.364 and κ = ½'),(C678,'| E1 |')],['A1','A3'])
add('O-cosmology',O,'Derive background and linear perturbation closure from same equations and infer initial inputs from observations within that framework','missing framework-only cosmology',[(A,'Under that same law derive background'),(A,'cosmological perturbation'),(T,'inherited ΛCDM initial conditions')],['O-selector','O-receiver','O-health'])
add('O-data',O,'New completion must pass early types and native growth, not merely formalize existing failing candidate; retained successes/failures both conditional on shared inputs','not established; frozen data failures apply to tested constructions',[(S678,'Any new action must'),(C679,'**MECHANISM WITHOUT DATA**'),(A,'downgrade symmetrically')],['O-cosmology','E-raw-gates'])
add('O-pending',O,'Redshift/Gaia held-out predictions require future observations; pending gates cannot be certified now','pending future empirical checks',[(T,'Gaia DR4'),(C679,'| D3 |'),(C679,'S8 (which may be PENDING)')],['A4','A8'],'CFG679 provisional pass explicitly permits S8 pending; that is not whole-theory empirical completion.')
add('O-TOE',O,'Quantum completion, radiative stability, Standard-Model structure and black-hole/global gravity are beyond current certificate','declared/unformalized',[(C678,'| E2 |'),(C678,'| E3 |'),(R,'A complete account of gravity')])
add('A2-implementation',FP,'PM interpolation is a tabulated repaired kernel: DELTA=0.05, log10(y) grid [-12,12] with 240001 nodes, clipped derivative, trapezoidal integration, interpolation and y floor 1e-12','implemented phenomenology, not analytic interpolation certificate',[(PM,'Y_P = brentq'),(PM,'LYG = np.linspace'),(PM,'DH_MONO ='),(PM,'H_MONO ='),(PM,'y = np.maximum(np.asarray')],['A2'],'These choices are additional numerical/interpolation inputs and require domain/error specification before a granular Lean computation certificate.')
add('A7-gravity-normalization',FP,'Newtonian spherical enclosed-mass force and Lambda=8 pi G rho_DE/c^2 relation are explicit gravity conventions/hypotheses in Lean, not derived relativistic geometry','conditional adopted gravity',[(L,'hΛ : Λ ='),(L,'hforce : G * (Mb + Mc)'),(R,'The Einstein equations')],['A7'])
# Exact statements, not merely English theorem names, preserve every explicit premise.
lean=texts[L]
for match in re.finditer(r'^theorem (\w+)([\s\S]*?) := by',lean,re.M):
 name=match.group(1); statement=('theorem '+name+match.group(2)).strip()
 add('LEAN-'+name,M,statement,'existing kernel certificate conditional on explicit premises',[(L,'theorem '+name+' '),(R,'All mathematical variables')],limit='Mathematical kernel independence from extra physics axioms; not independent scientific audit. Existing run records inspected, compiler not rerun by this bounded assumption agent.')
# Bounded no-go evidence is not a universal exclusion.
add('M-restricted-stress',O,'Reported local first-order spherical {G,a0} stress obstruction and fixed-source convex construction','source-reported mathematical result, not independently rederived here',[(J,'**DERIVED NO-GO**'),(J,'**CONSTRUCTION**')],['A2'],'Restricted class only. This record is not a kernel certificate of CFG660/661 nor an exhaustive uniqueness theorem.')
add('O-uniqueness',O,'Claim that CFG541/544/638 are forced equations requires an exhaustive admissible-class uniqueness theorem','unsupported universal inference in synthesis',[(J,'are the forced form'),(J,'not a missing calculation inside known physics'),(S679,'4 of 15')],['O-selector'],'A finite catalogue with no successful entry does not prove that all allowed microphysics are impossible or that the tested settling operator is unique.')
result={'schema_version':1,'checkpoint':'FRAMEWORK-CERT-2026-10-12','base_git':'8cef73ea7d01e20f1d08f435ad621b739f8eb3cc','observed_git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'scope':'Snapshot audit of named current framework, contracts and existing targeted Lean package; no new cosmological fit or raw-data run','primary_verdict':'incomplete, with the smallest missing implication','categories':[FP,M,E,B,O],'source_snapshots':list(sources.values()),'entries':entries,'claim_count':len(entries),'symmetry_rule':'Every observational success or failure using borrowed background/IC/supply/scorer inputs remains conditional on them. Neither noticing dependence nor matched control subtraction establishes rescue or universal exclusion.'}
(OUT/'assumption_register.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'records':len(entries),'sources':len(sources),'lean_records':sum(e['id'].startswith('LEAN-') for e in entries),'output':str(OUT/'assumption_register.json')}))
