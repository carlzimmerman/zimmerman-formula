"""Local mass-continuity defect of the truncated angular potential, on saved fields."""
import pathlib,json,hashlib,datetime,platform,resource,numpy as np,scipy
from angular_half import Angular,SHT
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];C10=P.parent/'cold_moving_cores_2026_10_24';files=[pathlib.Path(__file__),P/'angular_half.py',P/'CONTRACT.md'];tags=['draco_track','sextans_track']
for tag in tags:files.extend([C10/'runs'/f'{tag}.json',C10/'runs'/f'{tag}_fields.npz',C10/'runs'/f'{tag}_tracking.json'])
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
files.extend([P.parent/'cold_envelope_formation_2026_10_24/runs/draco_escape_long_fields.npz',P.parent/'cold_envelope_formation_2026_10_24/runs/sextans_escape_long_fields.npz']);before=hashes();start=datetime.datetime.now(datetime.timezone.utc).isoformat();rows=[]
for tag in tags:
 q=json.loads((C10/'runs'/f'{tag}.json').read_text());z=np.load(C10/'runs'/f'{tag}_fields.npz');tr=json.loads((C10/'runs'/f'{tag}_tracking.json').read_text());r=z['r'];w=z['w'];L=q['parameters']['lmax'];M=q['parameters']['mmax'];eta=q['physical']['eta_code'];R=q['physical']['Runit_pc'];V=q['physical']['Vunit_kms'];base=Angular(L,M,r,w)
 for key,hh in [('initial',tr['history'][0]),('final',tr['history'][-1])]:
  # NPZ initial is original t0, not the resumed t120 field. Load actual parent for t120.
  if key=='initial':
   parent=P.parent/'cold_envelope_formation_2026_10_24/runs'/('draco_escape_long_fields.npz' if tag.startswith('draco') else 'sextans_escape_long_fields.npz');v=np.load(parent)['final']
  else:v=z['final']
  # Evaluate on oversampled angular grid, retaining exactly the original field projection.
  nt=4*L+4;nf=8*M+8;field=SHT(L,M,nt,nf);dens=SHT(2*L,2*M,nt,nf);cr=np.empty((len(r),dens.nm),complex)
  for lo in range(0,len(r),32):
   sl=slice(lo,min(lo+32,len(r)));va=field.forward(v[sl]);cr[sl]=dens.back(abs(va)**2/(w[sl]*r[sl]**2)[:,None,None])
  co=base.green(cr);globalS=absS=coreS=coreabs=coremass=residual2=force2=0.;center=np.array(hh['aperture_COM_code']);mu,phi=np.meshgrid(field.mu,np.arange(nf)*np.pi/nf,indexing='ij');unit=np.stack([np.sqrt(1-mu*mu)*np.cos(phi),np.sqrt(1-mu*mu)*np.sin(phi),mu],axis=-1)
  for lo in range(0,len(r),32):
   sl=slice(lo,min(lo+32,len(r)));va=field.forward(v[sl]);pa=dens.forward(co[sl]).real;force=pa*va;pvp=field.forward(field.back(force));S=2/eta*np.imag(va.conj()*pvp);mask=np.linalg.norm(r[sl,None,None,None]*unit[None,:,:,:]-center,axis=-1)<1;partner=np.linalg.norm(r[sl,None,None,None]*unit[None,:,:,:]*np.array([-1,-1,1])-center,axis=-1)<1;fraction=.5*(mask+partner.astype(float));globalS+=np.sum(field.integral(S));absS+=np.sum(field.integral(abs(S)));coreS+=np.sum(field.integral(S*fraction));coreabs+=np.sum(field.integral(abs(S)*fraction));coremass+=np.sum(field.integral(abs(va)**2*fraction));residual2+=np.sum(field.integral(abs(force-pvp)**2));force2+=np.sum(field.integral(abs(force)**2))
  row=dict(tag=tag,state=key,t=hh['t'],global_mass_source_per_code_time=float(globalS),absolute_local_mass_source_per_code_time=float(absS),absolute_source_fraction_of_remaining_mass_per_code_time=float(absS/np.sum(abs(v)**2)),core_mass_code=float(coremass),core_net_projection_source_per_code_time=float(coreS),core_absolute_projection_source_fraction_per_code_time=float(coreabs/coremass),angular_H_residual_norm_over_eta=float(np.sqrt(residual2)/eta),relative_angular_potential_residual_norm=float(np.sqrt(residual2/force2)),scope='instantaneous angular projection only; radial finite-current defect additional; labels advected with j/rho alone miss this source');rows.append(row);print(row,flush=True)
# Parent files discovered in fixed deterministic loop are now independently pinned after their use;
# state this limitation rather than invent a prior hash. Other declared inputs before/after are compared.
after={k:hashlib.sha256((ROOT/k).read_bytes()).hexdigest() for k in before};assert before==after
(P/'projection_audit_v2.json').write_text(json.dumps(dict(started_utc=start,software=dict(Python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),source_hashes_before=before,source_hashes_after=after,parent_fields_after={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.name.endswith('long_fields.npz')},results=rows,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
