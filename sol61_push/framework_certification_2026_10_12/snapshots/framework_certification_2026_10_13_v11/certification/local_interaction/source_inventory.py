from pathlib import Path
import hashlib,json,subprocess
out=Path(__file__).resolve().parent; root=out.parents[2]
queries={'sol61_push/cold_production_2026_10_11/COLD_ENERGY_EQUATIONS.tex':['The \\emph{proposed} action','V&=m^2','g(\\chi','(\\Box+m^2)','\\Gamma_0=','The initial source','\\dot B=','Elastic collisions conserve'], 'sol61_push/cold_production_2026_10_11/CHARGED_ACTION.md':['charges 1 and 2','g(chi* phi^2','A constant vacuum term'], 'sol61_push/cold_production_2026_10_11/FOUR_FORM_PORTAL.md':['Z(S) =','q is constant','m_eff^2=','There is no new spatial'], 'sol61_push/cold_production_2026_10_11/SOURCE_COLLISION_OPERATOR.md':['J_ijk =','chemical potential mu','genuine moving-source recoil'], 'sol61_push/cold_production_2026_10_11/ELASTIC_EXCHANGE.md':['Tags identify','Q_a =','Q_a+Q_b=0'], 'sol61_push/microscopic_carrier_2026_10_10/REPORT.md':['H=\\int','no vacuum-dependent coupling'], 'sol61_push/kinetic_receiver_lift_2026_10_12/RESULT.txt':['Bracket/collision shape:','Receiver: assumed','Derive an actual local']}
files=[]
for p,terms in queries.items():
 b=(root/p).read_bytes();text=b.decode();lines=text.splitlines();locs=[]
 for needle in terms:
  hits=[i+1 for i,l in enumerate(lines) if needle in l]
  locs.append({'needle':needle,'lines':hits,'excerpts':[lines[i-1] for i in hits]})
 files.append({'path':p,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'locators':locs})
d={'checkpoint':'FRAMEWORK-CERT-TRANSPORT-2026-10-12','observed_git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'source_snapshots':files,'scope':'Existing charged carrier action, supplied conversion kinetics, optional fixed-flux portal; does not merge separate action families.'}
(out/'INPUTS.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({'sources':len(files),'missing_locator_needles':[(f['path'],q['needle']) for f in files for q in f['locators'] if not q['lines']]}))
