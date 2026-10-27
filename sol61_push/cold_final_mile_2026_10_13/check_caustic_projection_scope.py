"""CE-FM-071: source case-capture trace and nonlocal caustic projection."""
import ast,json,math,sys
from pathlib import Path
from scipy.integrate import quad
import numpy as np
p=Path('campaign_fresh_gravity/CFG819_splashback_derivation');s818=Path('campaign_fresh_gravity/CFG818_unrelaxed_free_placement/cfg818.py').read_text();s819=(p/'derive_rsp.py').read_text();checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
# Evaluate ONLY the pure CASES list expression, never module imports/definitions.
tree=ast.parse(s818);node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CASES' for t in n.targets));cases=eval(compile(ast.Expression(node.value),'CASES','eval'),{'FEET':('canonical','alt')})
lastEX=[c for c in cases if c[2]=='EX'][-1]
ck('last EX is mono alt not primary',lastEX==('mono','alt','EX'))
ck('ALL follows last EX',cases[-1]==('s','canonical','ALL'))
ck('EX swaps InfallSnap only', 'L.Infall = InfallSnap' in s818 and 'L.Infall = _orig' in s818)
ck('ALL uses original derive', '(derive_ex if variant == "EX" else L.derive)' in s818)
ck('probe overwrites single untagged slot','cap["I"] = self' in s819 and 'I = cap["I"]' in s819)
ck('all-case cluster call is used','G["cluster_runs"](Mg, 0.2, z, R5 * 1000.0)' in s819)
ck('reported no-free light and two other radii',all(x in (p/'derive_rsp.out').read_text() for x in ['no free mass','r_sp = 0.17','r_sp = 0.43']))
# Exact spherical thin-shell kernel (pc^-2 per Msun); R=a singular excluded.
def K(R,a):
 if R>a:return 1/(math.pi*R*R)
 if R==a:raise ValueError('ideal shell singular at tangent')
 y=math.sqrt(1-(R/a)**2);one=(R/a)**2/(1+y)
 return -one*one/(2*math.pi*R*R*y)
edges=np.geomspace(.15,3.,9);midcent=np.sqrt(edges[:-1]*edges[1:])[3:6]
ck('actual MID edges bracket source nominal interval',edges[3]<.48 and edges[6]>1.24)
rows=[]
for aM in [.17,.43]:
 lo,hi=.95*aM*1e6,1.05*aM*1e6
 for RM in midcent:
  R=RM*1e6;point=1/(math.pi*R*R)
  ck('entire finite caustic inside projected aperture '+str(aM)+str(RM),R>hi)
  thin=K(R,aM*1e6);layer=quad(lambda aa:K(R,aa),lo,hi)[0]/(hi-lo)
  ck('positive thin caustic MID response '+str(aM)+str(RM),thin>0 and abs(thin/point-1)<1e-12)
  ck('finite-width layer same point-mass tail '+str(aM)+str(RM),abs(layer/point-1)<1e-12)
  old=quad(lambda aa:K(R,aa),1.9e6,2.1e6)[0]/.2e6
  ck('fixed-stock inward redistribution boosts MID '+str(aM)+str(RM),old<0 and layer-old>0)
  rows.append({'inner_caustic_radius_Mpc':aM,'projected_R_Mpc':float(RM),'thin_or_narrow_layer_ESD_per_Msun_pcminus2':thin,'ESD_per_1e13Msun':thin*1e13,'delta_ESD_if_1e13Msun_moved_from1p9_to2p1Mpc_layer':(layer-old)*1e13})
# At a projected radius interior to either caustic, its contribution is negative;
# near and beyond the layer the sign changes. This constrains simultaneous fit.
for aM in [.17,.43]:ck('inner negative sign '+str(aM),K(.15e6,aM*1e6)<0)
result={'claim_id':'CE-FM-071','n_checks':len(checks),'all_pass':all(z['pass'] for z in checks),'checks':checks,'source_cases':cases,'last_captured_EX_case':lastEX,'primary_case':['s','canonical','EX'],'actual_MID_edges_Mpc':[float(edges[3]),float(edges[6])],'projection_countercontrols':rows,'scope':'Source-control-flow and exact lensing geometry only; no actual free-profile/lensing score, caustic mass, orbit convergence or physical inward-redistribution mechanism derived. Official source outcome remains recorded.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'all_pass':result['all_pass'],'lastEX':lastEX,'rows':rows}))
