"""Authenticate saved CCT011 evidence and independently check one-source gravity."""
import pathlib,json,hashlib,sys,platform,resource,numpy as np,scipy,sympy
from angular_half import Angular,SHT
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];C10=P.parent/'cold_moving_cores_2026_10_24';out=pathlib.Path(sys.argv[1]);pin_count=0
for f in list((P/'runs').glob('*.json'))+[P/'analysis.json',P/'projection_audit_v2.json',P/'phase_factored_benchmark.json',P/'phase_benchmark_001/result.json']:
 q=json.loads(f.read_text());a=q.get('source_hashes_before',q.get('inputs_before'));b=q.get('source_hashes_after',q.get('inputs_after'))
 if a is None:continue
 assert a==b,(f,'before/after')
 for k,h in a.items():
  file=ROOT/k
  if not file.is_file():file=P/k
  assert hashlib.sha256(file.read_bytes()).hexdigest()==h,(f,k);pin_count+=1
analysis=json.loads((P/'analysis.json').read_text());field_checks=[]
for name in ['draco','sextans']:
 ref=np.load(C10/'runs'/f'{name}_track_fields.npz')['final']
 for step in [2,4]:
  tag=f'{name}_material_s{step}';q=json.loads((P/'runs'/f'{tag}.json').read_text());z=np.load(P/'runs'/f'{tag}_fields.npz');v=z['final'];diff=float(np.linalg.norm(v-ref)/np.linalg.norm(ref));assert diff<1e-12;h=q['history'][-1];assert abs(h['M_residual'])<1e-8 and abs(h['E_residual'])<.01 and abs(h['J_residual'])<.01;assert abs(np.sum(abs(v)**2)-h['M'])<1e-12;field_checks.append(dict(tag=tag,relative_difference_from_no_label_cold_field=diff,M_E_Jz_gates_pass=True))
 # Independently integrate the field in the stellar aperture by dense angular quadrature.
 row=next(z for z in analysis['material'] if z['tag']==f'{name}_material_s4');q=json.loads((P/'runs'/f'{name}_material_s4.json').read_text());zz=np.load(P/'runs'/f'{name}_material_s4_fields.npz');r=zz['r'];v=zz['final'];L=q['parameters']['lmax'];M=q['parameters']['mmax'];sht=SHT(L,M,4*L+4,8*M+8);mu,phi=np.meshgrid(sht.mu,np.arange(sht.nphi)*np.pi/sht.nphi,indexing='ij');unit=np.stack([np.sqrt(1-mu*mu)*np.cos(phi),np.sqrt(1-mu*mu)*np.sin(phi),mu],axis=-1);center=np.array(row['final']['stellar_COM_pc'])/q['physical']['Runit_pc'];mass=0.
 for lo in range(0,len(r),32):
  sl=slice(lo,min(lo+32,len(r)));xyz=r[sl,None,None,None]*unit[None,:,:,:];mask=np.linalg.norm(xyz-center,axis=-1)<1;partner=np.linalg.norm(xyz*np.array([-1,-1,1])-center,axis=-1)<1;mass+=np.sum(sht.integral(abs(sht.forward(v[sl]))**2*.5*(mask+partner.astype(float))))
 mass*=q['physical']['Munit_Msun'];rel=mass/row['actual_total_cold_mass_within_Rstar_of_stars_Msun']-1;assert abs(rel)<.1;row['independent_angular_quadrature_relative_mass_difference']=float(rel)
assert analysis['material'][0]['tagged_mass_over_actual_total_mass']>1.1
for x in analysis['material']:assert x['tag_substep_retention_absolute_difference']<=1/512
for x in analysis['controls']:assert 'angular cutoff' in x['status'] and x['stopped_at_code_t']<x['requested_endpoint_code_t'] and abs(x['energy_residual'])<.01 and abs(x['Jz_residual'])<.01
for name in ['fornax','leoi']:
 a=np.load(P/'runs'/f'{name}_matched_L8_fields.npz');b=np.load(P/'runs'/f'{name}_fixed_initial_L12M8_fields.npz');pad=np.zeros_like(b['initial']);lm=[tuple(x) for x in b['lm']]
 for j,lmm in enumerate(a['lm']):pad[:,lm.index(tuple(lmm))]=a['initial'][:,j]
 assert np.array_equal(pad,b['initial'])
for rec in json.loads((P/'run_record_index.json').read_text())['recorded_manifests']:
 q=json.loads((ROOT/rec).read_text());assert q['run']['status']=='completed'
 for x in q['input_artifacts']:assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256']==x['sha256_after']
 for x in q['outputs']:assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256']
# Independent finite spherical Green sum and deliberate doubled-source mutation.
r=np.geomspace(.03,16,64);w=np.gradient(r);a=Angular(4,4,r,w);v=np.zeros((len(r),a.field.nm),complex);v[:,0]=np.sqrt(w)*r*np.exp(-r*r/2);v/=np.linalg.norm(v);pa,co,W=a.potential(v);shell=np.sum(abs(v)**2,axis=1);manual=-(1/np.maximum(r[:,None],r[None,:]))@shell;phi=co[:,0].real/np.sqrt(4*np.pi);green_error=float(np.max(abs(phi-manual)));assert green_error<1e-12;pd,cd,Wd=a.potential(np.sqrt(2)*v);doubling_error=float(np.max(abs(cd-2*co)));assert doubling_error<1e-12 and abs(Wd-4*W)<1e-12;mutation=float(np.linalg.norm(cd[:,0].real/np.sqrt(4*np.pi)-manual)/np.linalg.norm(manual));assert mutation>.5
proj=json.loads((P/'projection_audit_v2.json').read_text());assert all(abs(z['global_mass_source_per_code_time'])<1e-12 and z['absolute_local_mass_source_per_code_time']>0 for z in proj['results']);toy=json.loads((P/'phase_benchmark_001/result.json').read_text());assert toy['unresolved_direct_control_rejected'];assert max(z['relative_amplitude_error'] for z in toy['results'])<1e-7;assert json.loads((P/'phase_identity_check.json').read_text())['symbolic_residual']=='0'
result=dict(status='saved finite results and scoped benchmarks verified; material survival NOT validated and final four-dwarf controls INCONCLUSIVE',audited_pin_instances=pin_count,field_checks=field_checks,material_results=analysis['material'],fixed_incoming_waves_exact=True,assembly_endpoint_status='all six pilots stopped unresolved',one_source_gravity_check=dict(direct_Green_max_error=green_error,doubled_source_linearity_error=doubling_error,deliberate_doubled_source_relative_error=mutation,mutation_rejected=True),projection_local_continuity_claim='refuted for the finite angular projection; continuum claim remains restricted as in MECHANISM_AUDIT',phase_prototype_status='finite1D constant-carrier benchmark verified, not a galaxy solver',software=dict(Python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=sympy.__version__),peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,nonclaims=['No fresh cold/star dynamics executed by this audit','No3D variable-phase or local conservative galaxy solver','No physical overboost exclusion from early unresolved pilots','No actual live-star lifetime test or full theory completion'])
out.write_text(json.dumps(result,indent=2)+'\n');print(out)
