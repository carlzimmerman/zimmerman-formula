import pathlib,json,sys,math,csv
import numpy as np
r=pathlib.Path(__file__).parent;out=r/sys.argv[1];out.mkdir(exist_ok=True);cfg=json.loads((r/'selection.json').read_text());meta={};names={p.stem.replace('_rotmod','') for p in (r/'inputs/rotmod').glob('*_rotmod.dat')}
for line in (r/'inputs/SPARC_Lelli2016c.mrt').read_text().splitlines():
 t=line.split()
 if t and t[0] in names:meta[t[0]]=dict(distance_Mpc=float(t[2]),inclination_deg=float(t[5]),inclination_error_deg=float(t[6]),quality=int(t[17]))
rows=[];exclusions=[];row_exclusions=[];kpc=3.085677581491367e19;a0=cfg['a0_m_s2']
for p in sorted((r/'inputs/rotmod').glob('*_rotmod.dat')):
 name=p.stem.replace('_rotmod','')
 try:
  raw=np.atleast_2d(np.loadtxt(p))
  if raw.shape[1]<6:raise ValueError('fewer than6columns')
 except Exception as e:exclusions.append(dict(name=name,reason='parse_failure',detail=str(e)));continue
 mask=np.isfinite(raw[:,:6]).all(axis=1)&(raw[:,0]>0)&(raw[:,1]>0)&(raw[:,2]>0)
 bad=int((~mask).sum());d=raw[mask]
 if len(d)<2:exclusions.append(dict(name=name,reason='fewer_than_two_valid_rows',rows=len(d)));continue
 R,V,eV,Vg,Vd,Vb=d[:,:6].T;sgas=np.sign(Vg)*Vg**2*1e6/(R*kpc);sd=.5*Vd**2*1e6/(R*kpc);sb=.7*Vb**2*1e6/(R*kpc);S=sgas+sd+sb;positive=S>0
 badsrc=int((~positive).sum());R,V,eV,sgas,sd,sb,S=[x[positive] for x in [R,V,eV,sgas,sd,sb,S]]
 row_exclusions.append(dict(name=name,raw_rows=len(raw),invalid_measurement_rows=bad,nonpositive_source_rows=badsrc,used_rows=len(R)))
 if len(R)<2:exclusions.append(dict(name=name,reason='fewer_than_two_positive_source_rows',rows=len(R)));continue
 Y=S/a0;fg=sgas/S;g=(S+np.sqrt(S*S+4*S*a0))/2;t=a0/(g+2*a0);ad=(1-t)*sd/S;ab=(1-t)*sb/S;err=2*eV/V
 cols=[np.ones(len(R)),ad];components=['amplitude','disk_to_gas']
 if np.any(sb>0):cols.append(ab);components.append('bulge_to_gas')
 N=np.column_stack(cols);X=N/err[:,None];target=t/err;coef=np.linalg.lstsq(X,target,rcond=1e-12)[0];res=target-X@coef;I=float(res@res);rank=int(np.linalg.matrix_rank(X,tol=np.linalg.norm(X,2)*1e-12))
 overlap=(fg>.5)&(Y>.3)&(Y<3);count=int(overlap.sum());radialspan=0. if count<2 else float(np.log10(R[overlap].max()/R[overlap].min()));tspan=0. if count<2 else float(np.ptp(t[overlap]));meets=count>=3 and radialspan>=.3 and tspan>=.05
 row=dict(name=name,valid_rows=len(R),has_bulge=bool(np.any(sb>0)),nuisance_columns=components,nuisance_rank=rank,ideal_information=I,ideal_sigma_log10S=None if I<=1e-20 else float(1/(np.log(10)*np.sqrt(I))),ideal_information_exceeds_0_05dex_1se=bool(I>=1/(np.log(10)*.05)**2),gas_dominated_rows=int((fg>.5).sum()),transition_rows=int(((Y>.3)&(Y<3)).sum()),gas_transition_rows=count,gas_transition_log_radius_span=radialspan,gas_transition_t_span=tspan,meets_illustrative_coverage=meets,overlap_radii_kpc=R[overlap].tolist(),gbar_over_a0_range=[float(Y.min()),float(Y.max())],gas_fraction_range=[float(fg.min()),float(fg.max())],metadata=meta.get(name),radius_range_kpc=[float(R.min()),float(R.max())])
 rows.append(row)
rows.sort(key=lambda x:(-x['ideal_information'],x['name']));coverage=sorted([x for x in rows if x['meets_illustrative_coverage']],key=lambda x:-x['ideal_information']);anyoverlap=sorted([x for x in rows if x['gas_transition_rows']>0],key=lambda x:-x['ideal_information'])
res=dict(assertion_tested='AllcopiedlocalSPARCrotmodtemplates;coverageandknown-templateprojectedquotientinformationonly;nolawresidualfitted.',selection=cfg,denominator=dict(input_rotmod_files=len(names),parsed_and_scored=len(rows),excluded_galaxies=len(exclusions),catalogue_metadata_matches=sum(x['metadata'] is not None for x in rows),total_raw_rows=sum(x['raw_rows'] for x in row_exclusions),total_scored_rows=sum(x['used_rows'] for x in row_exclusions)),exclusions=exclusions,row_exclusions=row_exclusions,coverage_counts=dict(any_gas_transition_overlap=len(anyoverlap),meets_predeclared_radial_variation=len(coverage),ideal_information_over_0_05dex_threshold=sum(x['ideal_information_exceeds_0_05dex_1se'] for x in rows),both_coverage_and_information=sum(x['ideal_information_exceeds_0_05dex_1se'] for x in coverage)),all_ranked_rows=rows,coverage_ranked_names=[x['name'] for x in coverage],nonclaims=['No agreementrankorobservedresidualfit','Metadataquality/inclinationdescriptiveonly','Known-source-shapeFisherupperinformation;notachievedprecision','No externalfield,pressure,warp,covarianceorIMFgradientmodel','NoactualEuclidfollowupselectionorheldoutscience'])
(out/'results.json').write_text(json.dumps(res,indent=2));fields=['name','valid_rows','has_bulge','ideal_information','ideal_sigma_log10S','gas_transition_rows','gas_transition_log_radius_span','gas_transition_t_span','meets_illustrative_coverage'];
with (out/'ranked.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:x[k] for k in fields} for x in rows)
print(json.dumps(res['denominator']));print(json.dumps(res['coverage_counts']));print('COVERAGE',res['coverage_ranked_names']);print('TOPINFO',[(x['name'],round(x['ideal_information'],2),x['gas_transition_rows'],x['meets_illustrative_coverage']) for x in rows[:10]])
assert len(names)==cfg['expected_rotmod_files'] and len(rows)+len(exclusions)==len(names)
