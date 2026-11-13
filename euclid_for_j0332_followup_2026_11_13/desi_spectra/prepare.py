from pathlib import Path
import json,re,base64,gzip,hashlib,numpy as np
P=Path(__file__).resolve().parent;old=P.parents[1]/'euclid_for_j0332_fit_2026_11_13/desi_crossmatch/spectrum_search';template=(old/'search.py').read_text();contract=json.loads((old/'contract.json').read_text())
def decode(x):
 if isinstance(x,dict) and x.get('type')=='ndarray':
  if isinstance(x['array'],list):return np.array(x['array'])
  raw=base64.b64decode(x['array']['data']);raw=gzip.decompress(raw) if raw[:2]==b'\x1f\x8b' else raw;return np.frombuffer(raw,dtype=np.dtype(x['dtype']).newbyteorder('<')).reshape(x['shape'])
 return x
for D in sorted(P.glob('EUCL-*')):
 j=json.loads(re.search(r'<script type="application/json"[^>]*>(.*?)</script>',(D/'viewer.html').read_text(),re.S).group(1));arrays={};model={};meta={}
 def walk(o):
  if isinstance(o,dict):
   if o.get('name')=='ColumnDataSource' and 'data' in o.get('attributes',{}):
    a=o['attributes'];d=dict(a['data'].get('entries',[]));band=a.get('name')
    if band in ['b','r','z']:
     for k in ['origwave','origflux0','orignoise0']:arrays[band+'_'+k]=decode(d[k])
    if 'origwave' in d and 'origflux0' in d and 'orignoise0' not in d:model.update(model_wave=decode(d['origwave']),model_flux=decode(d['origflux0']))
    if 'TARGETID' in d and 'Z' in d:
     for k,v in d.items():
      v=decode(v);meta[k]=v.tolist() if hasattr(v,'tolist') else v
   for v in o.values():walk(v)
  elif isinstance(o,list):
   for v in o:walk(v)
 walk(j);pr=json.loads((D/'fetch_provenance.json').read_text());assert str(meta['TARGETID'][0])==str(pr['catalogue_row']['TARGETID']);zl=float(meta['Z'][0]);print('viewer/catalogue',meta['TARGETID'],zl,pr['catalogue_row']['Z']);assert abs(zl-float(pr['catalogue_row']['Z']))<1e-4
 np.savez_compressed(D/'spectrum.npz',**arrays);np.savez_compressed(D/'model.npz',**model);(D/'metadata.json').write_text(json.dumps(meta,indent=2));C=contract.copy();C['foreground_z']=zl;C['search_z_min']=round(zl+.01,6);(D/'contract.json').write_text(json.dumps(C,indent=2))
 s=template.replace("I=P.parent;s=np.load(I/'L015780_viewer_spectrum.npz');m=np.load(P/'redrock_viewer_model.npz')","I=P;s=np.load(I/'spectrum.npz');m=np.load(P/'model.npz')").replace('zs=np.arange(.44,1.600001,.0002)',"zs=np.arange(C['search_z_min'],C['search_z_max']+.000001,C['dz'])").replace("I/'L015780_viewer_spectrum.npz'","I/'spectrum.npz'").replace("I/'target_spectrum_page.html'","I/'viewer.html'").replace("P/'redrock_viewer_model.npz'","P/'model.npz'")
 (D/'search.py').write_text(s)
 rel=lambda f:str(f.relative_to(P.parents[1]));arts=[D/'search.py',D/'contract.json',D/'spectrum.npz',D/'model.npz',D/'viewer.html'];bc=dict(claim_id=D.name+'_SOURCE_MULTIPLET_SCREEN',mathematics=dict(assertion_tested='Count redshift/width peaks satisfying predeclared>=3independentgroups SNR>=3 and strongest>=5 in foregroundsubtracted viewer spectrum',coefficient_domain='float64',conventions='VacuumA,positiveemission,fixedOIIIratio,Gaussianwidths;foregroundzfromthisTARGETID,notreusedfromanotherlens',inputs=['Actual individualDESIviewerflux/noise','EmbeddedRedrockmodel','Target-specificpredeclaredcontract'],bounds={'z_min':C['search_z_min'],'z_max':1.6,'dz':.0002,'sigma_A':[1.5,2.5,4.0],'null_realizations':100},non_claims=['No verifiedsourcezfromsingleline','No sourceabsence/detectionlimitassertion','No calibrated falsealarmprobability','No highzLya search']),execution_artifacts=[rel(f) for f in arts],software=[dict(name='Python',version='3.9.6'),dict(name='numpy',version='1.26.4'),dict(name='scipy',version='1.13.1')],randomness=dict(used=True,generator='numpy.default_rng PCG64',seed=7419));(D/'bounded_contract.json').write_text(json.dumps(bc,indent=2));print(D.name,'zl',zl,'zmin',C['search_z_min'])
