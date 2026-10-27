"""CE-FM-065: cached prediction/raw-stack score audit, no dynamical run."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.stats import chi2
b=Path('sol61_push/cold_final_mile_2026_10_13');d=b/'relic_score_inputs';saved=json.loads((d/'cfg777_results.json').read_text());checks=[]
def ck(name,x):
 checks.append({'name':name,'pass':bool(x)})
 if not x:raise AssertionError(name)
p=(1+10**(.12-3.62*(math.log10(2.5)-.66)**2-.35*(10.8-10.7)))/.9
ck('provisional p arithmetic',abs(p-saved['p_tacconi'])<1e-14)
# Trusted project-local cached object arrays, copied and hash-stamped; no imports
# of the scientific source or execution of its model-generating code.
ER=np.load(d/'erass.npy',allow_pickle=True);AC=np.load(d/'accept.npy',allow_pickle=True)
raw=np.load(d/'cfg687_percluster.npz',allow_pickle=False);cl=json.loads((d/'cfg686_results.json').read_text())['clusters']
ck('eRASS prediction/data alignment',len(ER)==len(raw['D'])==318);ck('ACCEPT alignment',len(AC)==len(cl)==8)
W=np.where(raw['E']>0,1/raw['E']**2,0);D=raw['D'];n=len(ER);patch=np.empty(n,int);patch[np.argsort(raw['ra'])]=np.arange(n)*30//n
bands={'INNER':[0,1,2],'MID':[3,4,5],'OUTER':[6,7]}
R={};A={};E={}
for key,old in saved['T_R'].items():
 pred=np.array([v[key]['base']+v[key]['res'] for v in ER]);vals={}
 for lab,j in bands.items():
  numer=np.sum(W[:,j]*D[:,j],axis=1);denom=np.sum(W[:,j]*pred[:,j],axis=1)
  mean=numer.sum()/denom.sum();reps=np.array([numer[patch!=i].sum()/denom[patch!=i].sum() for i in range(30)])
  sig=np.sqrt(29/30*np.sum((reps-reps.mean())**2));vals[lab]=[float(mean),float(sig)]
  ck('eRASS band '+key+lab,np.allclose(vals[lab],old['A'][lab],rtol=1e-11,atol=1e-12))
 ok=abs((vals['MID'][0]-1)/vals['MID'][1])<2 and abs((vals['OUTER'][0]-1)/vals['OUTER'][1])<2
 ck('eRASS class '+key,ok==old['pass_']);R[key]={'A':vals,'pass_':bool(ok)}
Da=np.nan_to_num(np.array([v['dsig'] for v in cl]));Ea=np.array([v['err'] for v in cl]);Wa=np.where(np.isfinite(Ea)&(Ea>0),1/Ea**2,0)
boot=np.random.default_rng(1).integers(0,8,size=(1000,8))
for key,old in saved['T_A'].items():
 pred=np.array([v[key]['base']+v[key]['res'] for v in AC]);vals={}
 for lab,j in bands.items():
  numer=np.sum(Wa[:,j]*Da[:,j],axis=1);denom=np.sum(Wa[:,j]*pred[:,j],axis=1)
  mean=numer.sum()/denom.sum();rep=numer[boot].sum(1)/denom[boot].sum(1);sig=float(np.nanstd(rep));vals[lab]=[float(mean),sig]
  ck('ACCEPT band '+key+lab,np.allclose(vals[lab],old['A'][lab],rtol=1e-11,atol=1e-12))
 ok=abs((vals['OUTER'][0]-1)/vals['OUTER'][1])<2;ck('ACCEPT class '+key,ok==old['pass_']);A[key]={'A':vals,'pass_':bool(ok)}
i=np.load(d/'cfg652_inputs.npz',allow_pickle=False);obs=np.load(d/'cfg652_esd.npz',allow_pickle=False);models=np.load(d/'efeds_models.npz',allow_pickle=False)
keep=i['Mcond']>0;g={k:obs[k][keep] for k in ['WG','WW','NN','pg']};rand={k:obs[k] for k in ['rWG','rWW','rNN','pr']};ng=int(keep.sum());nr=len(rand['pr'])
ck('eFEDS selected131',ng==131)
def profile(gs,rs):
 wg=g['WW'][gs].sum(0);wr=rand['rWW'][rs].sum(0)
 signal=g['WG'][gs].sum(0)/wg;reference=rand['rWG'][rs].sum(0)/wr
 boost=(g['NN'][gs].sum(0)/max(gs.sum(),1))/(rand['rNN'][rs].sum(0)/max(rs.sum(),1))
 return boost*signal-reference
rb=np.geomspace(30,3000,13);rc=np.sqrt(rb[:-1]*rb[1:]);use=(rc>=50)&(rc<=1000);nb=int(use.sum())
allg=np.ones(ng,bool);allr=np.ones(nr,bool);data=profile(allg,allr)[use]
jk=np.array([profile(g['pg']!=k,rand['pr']!=k)[use] for k in range(30)]);center=jk-jk.mean(0);cov=29/30*center.T@center
ck('eFEDS covariance PD',np.linalg.eigvalsh(cov).min()>0);hart=(30-nb-2)/29;inv=np.linalg.inv(cov)*hart
for key,old in saved['T_E'].items():
 pred=models[key.replace('|','__')][keep];mean=(g['WW']*pred).sum(0)/g['WW'].sum(0);res=data-mean[use];score=float(res@inv@res);pv=float(chi2.sf(score,nb))
 ck('eFEDS raw score '+key,np.isclose(score,old['chi2'],rtol=1e-11));ck('eFEDS p '+key,np.isclose(pv,old['p'],rtol=1e-11));ck('eFEDS class '+key,(pv>=.01)==old['pass_']);E[key]={'chi2':score,'p':pv,'pass_':bool(pv>=.01)}
primary={};pk=f'{p:.4f}'
for kern in ['s','mono']:
 primary[kern]={}
 for foot in ['canonical','alt']:
  key=f'{kern}|{foot}|p{pk}';passes=sum([R[key]['pass_'],A[key]['pass_'],E[key]['pass_']]);primary[kern][foot]=passes
  ck('primary all-three fail '+key,passes==0)
 ck('saved kernel failure '+kern,saved['verdict'][kern]=='FAIL')
result={'claim_id':'CE-FM-065','n_checks':len(checks),'all_pass':all(v['pass'] for v in checks),'checks':checks,'primary_pass_counts':primary,'eRASS_cached_replay':R,'ACCEPT_cached_replay':A,'eFEDS_cached_replay':E,'eFEDS_dof':nb,'eFEDS_hartlap':hart,'scope':'Independent cached-score arithmetic/stack replay, not regenerated predictions, stage source certification, raw-source calibration, or a test of all relic mechanisms/early-type lenses. Provisional Tacconi coefficients not externally verified.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'all_pass':result['all_pass'],'primary_pass_counts':primary}))
