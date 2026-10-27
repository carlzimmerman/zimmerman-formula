"""CE-FM-062: bounded source-function calibration controls, no archive rerun."""
import ast, copy, json, sys
from pathlib import Path
import numpy as np
P=Path('campaign_fresh_gravity/CFG799_hifi_totalpower_search')
source=(P/'cfg799.py').read_text()
ns={'np':np}
names={'legendre_design','gauss','_mad','anchor_ds','anchor','build_spectra','fit_one','eps_of','a_of_eps'}
# Only constants and named pure functions; never execute module imports/main/load.
tree=ast.parse(source)
const={'NU_T','NU_2','H2O','FWHM','SIG_G','HALF','EDGE','OFFS','kB','c','MSUN','PC','RHO','AREA','S_LIST'}
nodes=[]
for n in tree.body:
 if isinstance(n,ast.FunctionDef) and n.name in names:nodes.append(n)
 elif isinstance(n,ast.Assign):
  identifiers={z.id for t in n.targets for z in ast.walk(t) if isinstance(z,ast.Name)}
  if identifiers and identifiers <= const:nodes.append(n)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(P/'cfg799.py'),'exec'),ns)
checks=[]
def ck(name,ok):
 checks.append({'name':name,'pass':bool(ok)})
 if not ok:raise AssertionError(name)
real=json.loads((P/'cfg799_results.json').read_text())
mut=json.loads((P/'cfg799_results_MUTATE.json').read_text())
for key,r in real['main'].items():
 ck(key+' z arithmetic',np.isclose(r['z'],r['a']/r['sig'],rtol=1e-12))
 ck(key+' a95 arithmetic',np.isclose(r['a95'],max(r['a'],0)+1.645*r['sig'],rtol=1e-12))
 for S in ns['S_LIST']:
  e=ns['eps_of'](r['a95'],S)
  ck(key+' eps S'+str(S),np.isclose(e,r['eps95']['S'+str(int(S))],rtol=1e-12))
  ck(key+' inverse S'+str(S),np.isclose(ns['a_of_eps'](e,S),r['a95'],rtol=1e-12))
ck('reported null and subthreshold secondary',real['class']=='NULL' and real['main']['nu_2']['z']<5)
ck('mutate amplitude is ten saved sigma',np.isclose(mut['A_mut'],10*real['main']['nu_t']['sig']))
# One deterministic four-subband dataset; all numbers synthetic counts/rates/K.
x=np.linspace(4881.5,5118.5,1976); profile=ns['gauss'](x-5000.)
IF=np.tile(x,(4,1)); flags=np.zeros_like(IF,dtype=int)
tS=2.5; JH=300.; JC=50.; H=np.full_like(IF,3000.); C=np.full_like(IF,1000.)
G=(JH-JC)/(H-C)
Tref=np.tile(80.+.01*(x-5000)+.02*np.sin(x*1.37),(4,1))
Ton=Tref+np.tile(2.+np.sin((x-5000)/13.),(4,1))
Non=tS*(C+(Ton-JC)/G); Nref=tS*(C+(Tref-JC)/G)
d={'pol':'h','ds':1,'lo':535.664,'nsky':4.,'non':2.,'nref':2.,'JH':JH,'JC':JC,
   'H':H,'C':C,'Nall':(Non+Nref)/2,'Nref':Nref,'L1':Ton-Tref,'IF':IF,'flag':flags}
o={'ds':[d]}; a=ns['anchor'](o); base=ns['build_spectra']('synthetic',o,a['tS'])[0]
ck('synthetic anchor',a['ok'] and np.isclose(a['tS'],tS,atol=1e-12))
A=0.1; u=np.tile(A*profile,(4,1))/G
responses={}
for label,ks,kh,kc in [('sky_only',1.,0.,0.),('common_sky_load',1.,1.,1.),('one_percent_differential',1.,.99,.99)]:
 od=copy.deepcopy(o); z=od['ds'][0]
 z['Nall']+=tS*ks*u;z['Nref']+=tS*ks*u;z['H']+=kh*u;z['C']+=kc*u
 anc=ns['anchor'](od); sp=ns['build_spectra']('synthetic',od,anc['tS'])[0]
 ck(label+' anchor unchanged',anc['ok'] and np.isclose(anc['tS'],tS,atol=1e-11))
 ck(label+' L1 unchanged',np.array_equal(sp['L1'],base['L1']))
 delta=sp['Tall']-base['Tall']; target=(ks-kc)*A*np.tile(profile,(4,1))
 ck(label+' exact calibrated increment',np.max(np.abs(delta-target))<1e-10)
 fit=ns['fit_one'](x,delta[0],flags[0],5000.)
 responses[label]=fit[0]/A
 ck(label+' fitted transfer',abs(responses[label]-(ks-kc))<1e-10)
 ck(label+' REF calibrated increment',np.max(np.abs(sp['Tref']-base['Tref']-target))<1e-10)
# Unequal load response: exact finite rational formula and linearized derivative.
s=d['Nall']/tS;ks,kh,kc=1.,.7,.2
cal=lambda u:JC+(JH-JC)*(s-C+(ks-kc)*u)/(H-C+(kh-kc)*u)
small=np.full_like(IF,1e-3)
lin=G*(ks-kc-(s-C)/(H-C)*(kh-kc))
ck('unequal-load derivative',np.max(np.abs((cal(small)-cal(-small))/(2e-3)-lin))<1e-9)
# Actual fitter injects an exact design column, independent of raw/calibration transfer.
r0=ns['fit_one'](x,base['Tall'][0],flags[0],5000.)
r1=ns['fit_one'](x,base['Tall'][0],flags[0],5000.,inject=A)
ck('postcal injection unity by linearity',abs((r1[0]-r0[0])/A-1)<1e-10)
ck('postcal residual error unchanged',np.isclose(r0[1],r1[1],rtol=1e-10))
eps=real['main']['nu_t']['eps95']['S50'];window=4e-9
threshold=(eps/window)**2
ck('saved converter amplitude inverse',np.isclose(ns['a_of_eps'](window,50),real['converter_tier']['S50']['A_conv_K']))
ck('differential-power threshold',np.isclose(real['main']['nu_t']['a95']/real['converter_tier']['S50']['A_conv_K'],threshold))
# Source location checks guard claims about MUT/C1 ordering.
ck('MUT after build and anchor',source.index('if MUT:',source.index('def main'))>source.index('spectra += build_spectra'))
ck('MUT targets calibrated spectra', 'for key in ("Tall", "Tref"):' in source)
result={'claim_id':'CE-FM-062','kind':'self-review bounded calibration-transfer audit; synthetic arrays, not original raw-data rerun',
 'checks':checks,'n_checks':len(checks),'all_pass':all(c['pass'] for c in checks),
 'saved_main':real['main'],'fitted_transfers':responses,
 'S50_conditional_eps95':eps,'minimum_positive_power_transfer_to_reach_4e-9':threshold,
 'conditional_eps95_if_tau_0p01':eps/np.sqrt(.01),'conditional_eps95_if_tau_0p0001':eps/np.sqrt(.0001),
 'scope':'Exact cancellation for identical additive sky/hot/cold count-rate line. Does not establish that physical mirror conversion has those responses. Conditional epsilon bound requires independently supported positive phase response and stated noise/profile/geometry. Raw archive fit NOT independently reproduced.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_pass':result['all_pass'],'transfers':responses,'tau_min':threshold}))
