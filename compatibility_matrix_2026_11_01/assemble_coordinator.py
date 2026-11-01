"""Capture coordinator-owned documentary evidence; no scientific calculation."""
import json
from pathlib import Path
from capture_source import capture
HERE=Path(__file__).resolve().parent
S={}
for key,path in {
 'CSM':'rebuild_2026_10_22/CSM1_consistent_core_switch/README.md',
 'CSMf':'rebuild_2026_10_22/CSM1_consistent_core_switch/feasibility/README.md',
 'SL1':'rebuild_2026_10_22/SL1_symbolic_law_search/README.md',
 'SL2':'rebuild_2026_10_22/SL2_inverse_core_ratio/README.md',
 'INV':'rebuild_2026_10_22/SL2_inverse_core_ratio/INVENTORY_2026-11-01.md',
 'CM1':'rebuild_2026_10_22/CM1_outflow_coupling/README.md',
 'BH1':'rebuild_2026_10_22/BH1_cluster_bh_coupling/README.md',
 'CL5':'rebuild_2026_10_22/CL5_agn_gas_cycles/README.md',
 'OC1':'rebuild_2026_10_22/OC1_one_coupling/README.md',
 'OWNER':'rebuild_2026_10_22/OWNER_DECISION_2026-10-31_NO_FLOOR.md',
 'QUEUE':'rebuild_2026_10_22/QUEUE_ROADMAP_2026-11-01.md',
}.items(): S[key]=capture(path,'coordinator')['id']
rows=[]
def add(i,name,parent,status,result,obstruction,scope,req,nonrepeat,nextstep,sources,aliases):
 rows.append(dict(id=i,name=name,family='cross_lane_coordinator',parent=parent,status=status,result=result,obstruction=obstruction,scope=scope,requirements=req.split(),nonrepeat=nonrepeat,next_new_step=nextstep,sources=[S[x]for x in sources.split()],aliases=aliases))
add('SYN01','Corrected same-core switch fails registered joint calibrations','CSM1: same mass-dependent core column and selector, inherited floor/basin/core assumptions','finite_failure',
 'At L=3.75,3.9,4 canonical SPARC/groups/clusters pass but lensing delta-chi2 against the law is +415.28,+420.31,+423.23. The sole refit L=2.5090648745652686 passes lensing but groups fail Z=+2.62192.',
 'Moving the switch by the sole L also changes core amplitudes; the old switch pass cannot be preserved while using a different core L.',
 'Finite registered levels and one predeclared refit, not all canonical L. This is an older floored architecture, not the adopted no-floor N.',
 'C01 C05 C06 C08 C09 C11','Do not present a consistent two-state core/switch or the L-only challenge as new.',
 'A genuinely changed selector derived from a parent must be graded with its own core amplitudes; no automatic extra L scan.','CSM CSMf',['CSM1','CL3','BS1'])
add('SYN02','Corrected switch has a scoped exhaustive alternate-UFD obstruction','Fixed alternate footing, X51 profiles and shared Local Group selector','scoped_obstruction',
 'The two exhaustive UFD branch values are Z=-2.775 halo and +4.874 law; both fail the fixed cut for every positive L.',
 'L changes only one common branch flag for these 31 members, not the branch profiles.',
 'Fixed profile/error/membership/basin construction only. Canonical necessary interval 2.480712<L<=5.006831 is neither excluded nor sufficient.',
 'C07 C11','Do not search more L values as a cure for this unchanged alternate UFD class.',
 'Change a physical profile or state assignment and justify it independently, then regrade all constraints.','CSMf',['CSM1 alternate UFD'])
add('SYN03','Symbolic response search found no allowed survivor','SL1 finite expression grammar on NR1 PRIMARY','finite_failure',
 '935 exact-regraded SPEC training hits and 20 NATIVE expressions produce zero survivors; SPEC hits all depend on a0 and violate the declared search rule.',
 'Training selection is not physics; holdouts remove hits and the best NATIVE response multiplier is physically excessive.',
 'Grammar size <=8, fixed leaves/inputs and control strength. Not impossibility of all functional forms; NR1 anchoring is inherited.',
 'C05 C06 C08 C11','Do not rename an algebraic multiplier search a derived mechanism or claim these bounds exclude all rules.',
 'Derive a response from state evolution; a new data reduction alone is an audit, not a newly discovered mechanism.','SL1',['SL1'])
add('SYN04','Inverse required response disagrees across scales','SL2 native-profile inversion and virial-energy ansatz','finite_failure',
 'A_req is near 0.8 on SPARC, below 0.96 in groups, 1.22–1.80 in clusters; tested virial response and a universal energy fraction fail. A crossing at 10^12 is not supported.',
 'One multiplicative repair does not supply the required radial and population behavior; inferred targets inherit mass mapping and profiles.',
 'Post-result A~0.8 clue is not independent support and does not fix LITTLE THINGS. No universal theorem on all mass-dependent laws.',
 'C05 C06 C07 C08 C11 C12','Do not rerun the same virial scaling or relabel A~0.8 as a new prediction.',
 'Predict mass redistribution and response ordering from a conserving state model; re-evaluate its own observables.','SL2',['SL2','CR2','UR1'])
add('SYN05','Supernova energy budget does not supply a sufficient gravity channel','CM1 prescribed spherical gas cycles in one galaxy','finite_failure',
 'At measured gas R=0.932 after 40 cycles versus needed <=0.817; gas lifting costs 0.763 of the SN budget. All-baryon bound reaches R=0.293 but costs 3.611 budgets.',
 'Only about 0.4% of lifting energy reaches the cold component in this history; core energy need is not channel cost.',
 'One halo/seed, prescribed histories and present gas; A1 corrects an invalid original control. Gas-richer past not excluded.',
 'C10 C12','Do not repeat an energy-available calculation as evidence the measured-gas channel works.',
 'A quantitatively distinct and independently justified history/channel with reciprocal work accounting.','CM1',['CM1','BE1','CM2','CM3'])
add('SYN06','Black-hole gravity channel remains insufficient in tested geometries','BH1 spherical closed-box cluster/group gas cycles','finite_failure',
 'Best capped R=0.986/0.917 versus limits .845/.809; tested uncapped hot-gas route reaches .948/.917.',
 'Gas geometry and movable central load limit transfer even with an ample energy reservoir.',
 'Provisional baryons, one halo/seed per mass, finite core readout; non-gravitational coupling and gas-rich assembly not tested.',
 'C08 C10 C12','Do not infer a working mechanism from BH energy alone or claim all AGN histories excluded.',
 'Specify new spatial coupling/history with measured load and evaluate actual response.','BH1',['BH1','BH2','CL4'])
add('SYN07','AGN gas cycles remain short after fair-control correction','CL5 formed halo plus stipulated gas cycles','finite_failure',
 'Original ceiling R~1.025 uses a mismatched static gas control; same-gas comparison softens to R~.91–.95, still short of .81–.85 needs. Midcycle dips do not persist.',
 'Transient or control-dependent softness is not retained core regulation; stipulated target softening also leaves within-SPARC tensions.',
 'Same-gas correction is post-result. Finite spherical one-seed experiment with provisional inputs and old core targets, not every cluster history.',
 'C06 C08 C10 C12','Do not quote the original control as the sole failure or a favorable cycle phase as a durable rescue.',
 'Paired equal-baryon controls and persistent radial observables in any new parent.','CL5',['CL5','SH1','RF6'])
add('SYN08','One dissipation fraction is not a common channel','OC1 bookkeeping on old core targets','finite_failure',
 'One fraction of all dissipation needs galaxy .00128 versus cluster .078 (ratio 61 canonical); separate SN/BH source bands overlap but do not supply a selector.',
 'Source choice and mass trend matter; overlap of two budget fractions is not one physical transfer law.',
 'Old floored/c_f targets and provisional source budgets; not a universal factor-61 exclusion. Current outer-cluster deficit is a different problem.',
 'C08 C10 C11 C12','Do not transfer the old numerical efficiency target to PN28 or count budget overlap as a derived common coupling.',
 'Derive source-dependent coupling and radial work using the current common parent.','OC1',['OC1'])
add('SYN09','Adopted model and permitted synthesis are distinct from older labels','Owner no-floor N decision and current queue','data_audit',
 'The Oct31 adopted N removes the a0 floor from the cold sector and separates the acceleration law; the Nov1 queue stops T derivation and lets already-frozen HB1/M3A1 work finish.',
 'Experimental PN28/X48 constructions are separate candidate models; none inherits N grades or owner adoption. A new synthesis is not authorization to restart every closed program.',
 'Provenance/authorization boundary. Present user explicitly authorizes this compatibility synthesis and push.',
 'C01 C05 C11','Do not resurrect the removed floor silently or reopen T scans to fill an empty matrix cell.',
 'State altered premises openly; require a common derivation before upgrading a candidate.','OWNER QUEUE',['NF1 owner decision','queue stop'])
# Indexed families ensure older lanes are represented without pretending they were all freshly audited.
families=[
 ('IDX01','Core shapes and outer tails','X68 X69 X70_soft_floor TL1 GC3 GX1 X40 X40b IJ1 X44 X45 SC1 CS2 OS1','C05 C06 C08','Profile/tail repairs trade core and outskirts grades; free choices do not derive a core.','Review a changed dynamical profile, not another inherited static shape.'),
 ('IDX02','Acceleration floors and phase-space caps','X65 X66 X67 X47 X50 PS1 PS2 DF1 DW1 X28 X25_floor MF1 X56','C01 C03 C05 C10','Several tested floors/caps fail or are nondiagnostic; scalar thresholds are not constitutive stress or a transport law.','An explicit stress, source and transport completion is necessary.'),
 ('IDX03','Mass, environment and formation switches','J1 X19 X58 X59 X62 X61 X31 CFG914 CFG919 CFG921 CFG928 DT1 CF1 CF2 CL1 CL2 CL3 BS1 HO1 HO2 X57 X60','C05 C07 C09 C11','Tested selectors fail ordering/holdouts or remain conditional; not proof all state selection impossible.','Use dynamical state variables, and account for previous CSM1 directly.'),
 ('IDX04','Exchange, late conversion and two-phase rules','X37 X54 X23 X24b X29 DH1 CFG958 X34 RF5 PH1 M1 M5 X26 X30 CFG930 CFG932 CFG965 CFG949 CFG959 CFG915 CFG913','C02 C03 C04 C11 C12','Late release, simple conversion or population labels collide with timing, stress or lensing assumptions; several are fragile/undetermined.','Check completed BOLTZ1/TP04 before proposing another cold-state calculation.'),
 ('IDX05','Earlier baryon response and gas mechanisms','X39 CN1 LC1 OP3 SH1 AE1 BC1 GT1 DS1 NM1 X52 X51 CFG934 CFG937','C06 C07 C08 C10 C11 C12','Full contraction damages galaxy fits; energy availability and current gas do not supply selective regulation.','Retain paired controls, force ledger and mass/environment ordering.'),
 ('IDX06','Halo mass maps and retention','X55 AM1 X76 MA1 G2 OP1','C02 C06 C07 C08 C09 C11','Different probes demand incompatible repairs to a fixed empirical mass mapping; dwarf extrapolations are especially conditional.','Derive or independently constrain assignment instead of changing it by probe.'),
 ('IDX07','Native concentration, resolution and boundaries','X48 X74 NL1 FP2 CE1 A5 X76_cf UV1 VB1 ZN4 X77 X80 X81 AQ1','C02 C05 C06 C08','Some concentration verdicts used estimator artifacts; later convergence and boundary audits qualify them.','Use corrected native profiles and matching mass definitions, not obsolete cf numbers.'),
 ('IDX08','Gas scale, baryon census and outer-systematics','GS4 GS5 GX2 CFG922 CFG929 NU1 HL2 CFG967 X2 X30 GA1 DY1 AP1 FM1 HG2','C08 C09','Gas rescaling is constrained; HSE and shear are distinct, and some hot/cold sign statistics are conditioning artifacts.','Keep M3A1/HB1 pending and regrade only after data/harness validity.'),
 ('IDX09','Lensing and circumgalactic material','GH2 GH3 GH4 GH5 GH6 GH7 GH8 GH9 GH10 GH11 RF4 KN1 UN1 UN2 X79 ZT5 SI1 SI2 SI3 SC2','C08 C09 C11','Relative shape advantages are not absolute fits; stellar-mass, clone and two-halo ambiguities remain.','Preserve measurement-specific assumptions; no automatic mechanism pass from an audit.'),
 ('IDX10','Carrier, abundance and coefficient derivations','QC1 CR1 CR2 X1 CFG893 CFG897 CFG898 CFG899 CFG900 CFG901 CFG902 CFG903 CFG904 CFG905 CFG906 CFG907 CFG908 CFG909 CFG910 CFG911 DSF-21 GF2 CA1','C01 C02 C04 C05','No reported derivation of abundance or kappa closes the parent; many coefficient claims restate assumptions.','Use latest TP01–04 and a genuinely new matching or production implication.'),
 ('IDX11','Older covariant alternatives and strong tests','v3s AeST-H2 MOG-X9 K1 Q7 CFG938 CFG944 CFG945 CFG946 CFG947 CFG948 CFG950 CFG951 CFG952 CFG953 CFG954 D7d X15 X16 CFG740','C01 C03 C04 C05 C09','Inventory reports failures/partial results but expressly did not re-read these sources; screening conclusions are family-specific.','Do not treat title-level closure or a different-law theorem as universal.'),
]
for i,name,alias,req,finding,new in families:
 add(i,name,'Heterogeneous historical families indexed by SL2; see full-path inventory for ID collisions','data_audit',finding,
 'Summary coverage only: source inventory mixes directly read JSON, README and brief/title evidence. This row supplies no new analytical exclusion.',
 'Indexed family, not a fresh lane-by-lane replication. Resolve overloaded IDs using full source paths before execution.',req,
 'Do not repeat indexed operations without first inspecting their exact completed contract and corrected latest result.',new,'INV',alias.split())
 rows[-1]['coverage_level']='index_summary_only'
(HERE/'coordinator_rows.json').write_text(json.dumps(rows,indent=2)+'\n')
(HERE/'COORDINATOR_COVERAGE.md').write_text('''# Coordinator coverage\n\nNine directly read records cover the corrected CSM1 switch, its exhaustive scoped dwarf obstruction, SL1/SL2, energy versus actual transfer (CM1/BH1/CL5/OC1), and owner/model provenance. Eleven additional indexed family records preserve the older inventory's coverage and limitations; they are not new physical failures or passes. The pinned inventory expressly reports about 90 opened reports among about 330 lanes and flags ID collisions and brief-only assertions. Direct newer reports in the other fragments supersede older index numbers. CM01 makes no claim that all historical code or all unrelated particle/SM/cosmology experiments were re-audited.\n\nAll inputs are immutable snapshots. Original repository-relative paths and hashes are in inputs/coordinator/SOURCES.json. Snapshots are documentary evidence: old relative links inside them retain their original context and are not rewritten.\n''')
print(json.dumps({'coordinator_rows':len(rows),'sources':len(S)}))
