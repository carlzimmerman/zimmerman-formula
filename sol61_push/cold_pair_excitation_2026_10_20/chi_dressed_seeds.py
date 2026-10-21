"""Distinct quasistatic-chi Cauchy preparation; NO evolution or cooling.

All charged fields/momenta are unchanged. Chi minimizes its static discrete
configuration energy at fixed Psi, and chidot is the instantaneous tangent.
"""
from pathlib import Path
import ast,hashlib,json,math,resource,struct,sys
import numpy as np
from pair_projection import analyze_snapshot,read_snapshot

ROOT=Path(__file__).resolve().parents[2]
raw_dir,mode_path,profile_path,out=map(Path,sys.argv[1:5])
P=json.loads((ROOT/'sol61_push/cold_completion_2026_10_20/run_001/results.json').read_text())['parameters']
with np.load(mode_path) as m:Qref=float(m['Q']);om=float(m['omega'])
baseline=np.asarray(read_snapshot(raw_dir/'clean_Y20_K0.bin')['fields']).copy()
fifty=np.asarray(read_snapshot(raw_dir/'clean_Y20_K50.bin')['fields']).copy()
unit=(fifty-baseline)/math.sqrt(50.)
snapshot=read_snapshot(raw_dir/'clean_Y20_K0.bin')
Nr,Nz,dx=snapshot['Nr'],snapshot['Nz'],snapshot['dx'];rho=snapshot['rho'];zz=snapshot['z']
assert (Nr,Nz,dx)==(188,480,.75)
radius=np.sqrt(rho[None,:]**2+zz[:,None]**2);volume=2*math.pi*rho[None,:]*dx*dx
M=P['M_chi'];a=P['a'];indices=[0,1,2,3,5,6,7,8]

# Reuse the pinned, independently C-stencil-audited diagnostics function only;
# do not execute the previous constructor's top-level script or any evolution.
old_source=ROOT/'sol61_push/cold_pair_excitation_2026_10_20/clean_mode_seeds.py'
tree=ast.parse(old_source.read_text())
definition=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='diagnostics')
environment=dict(np=np,math=math,P=P,Nr=Nr,Nz=Nz,dx=dx,rho=rho,radius=radius)
exec(compile(ast.Module(body=[definition],type_ignores=[]),str(old_source),'exec'),environment)
diagnostics=environment['diagnostics']

def lap(field):
    i=np.arange(Nr)[None,:]
    rp=np.column_stack([field[:,1:],-field[:,-1]])
    rm=np.column_stack([field[:,0],field[:,:-1]])
    zp=np.row_stack([field[1:],-field[-1]])
    zm=np.row_stack([-field[0],field[:-1]])
    return (((i+1)*(rp-field)-i*(field-rm))/(i+.5)+zp+zm-2*field)/(dx*dx)

def solve_chi(raw):
    I=raw[0]**2+raw[1]**2
    source=a*I;h=raw[4].copy();history=[]
    for it in range(33):
        residual=-lap(h)+M*M*h-3*M*h*h/8+h**3+source
        error=float(np.max(abs(residual)));scaled=error/max(1.,float(np.max(abs(source))))
        contraction=(8/dx**2+float(np.max(abs(.75*M*h-3*h*h))))/(M*M)
        history.append({'updates':it,'residual_max_abs':error,'residual_max_scaled':scaled,
                        'h_min':float(h.min()),'h_max':float(h.max()),'local_supnorm_contraction_bound':contraction})
        if error<1e-8 and scaled<1e-11:break
        if it==32:raise RuntimeError('chi static cap32 reached: '+json.dumps(history))
        h=(lap(h)+3*M*h*h/8-h**3-source)/(M*M)
    Idot=2*(raw[0]*raw[5]+raw[1]*raw[6]);velocity=raw[9].copy();vhist=[]
    U2=M*M-.75*M*h+3*h*h
    for it in range(33):
        residual=-lap(velocity)+U2*velocity+a*Idot
        error=float(np.max(abs(residual)));scaled=error/max(1.,float(np.max(abs(a*Idot))))
        vhist.append({'updates':it,'residual_max_abs':error,'residual_max_scaled':scaled})
        if error<1e-8 and scaled<1e-11:break
        if it==32:raise RuntimeError('chi tangent cap32 reached: '+json.dumps(vhist))
        velocity=(lap(velocity)+(M*M-U2)*velocity-a*Idot)/(M*M)
    return h,velocity,history,vhist,Idot

checks=[];rows=[]
def ck(name,value):checks.append({'name':name,'pass':bool(value)})
dressed_baseline=None
for K in [0.,1.,50.,500.]:
    if K==1.:
        raw=baseline+unit
        raw_provenance='Explicit linear interpolation of raw K0/K50 fields and momenta at nominal coordinate1; no new normal-mode assumption.'
    else:
        raw=np.asarray(read_snapshot(raw_dir/f'clean_Y20_K{int(K)}.bin')['fields']).copy()
        raw_provenance='Exact immutable raw seed input.'
    olddiag=diagnostics(raw)
    h,hdot,history,vhist,Idot=solve_chi(raw)
    dressed=raw.copy();dressed[4]=h;dressed[9]=hdot
    ck(f'K{K} charged arrays byte-identical',np.array_equal(raw[indices],dressed[indices]))
    ck(f'K{K} all finite',np.all(np.isfinite(dressed)))
    ck(f'K{K} static residual absolute',history[-1]['residual_max_abs']<1e-8)
    ck(f'K{K} static residual scaled',history[-1]['residual_max_scaled']<1e-11)
    ck(f'K{K} tangent residual absolute',vhist[-1]['residual_max_abs']<1e-8)
    ck(f'K{K} tangent residual scaled',vhist[-1]['residual_max_scaled']<1e-11)
    ck(f'K{K} actual iteration contraction bound below1',max(t['local_supnorm_contraction_bound'] for t in history)<1)
    ck(f'K{K} positive convex U2 floor',float(np.min(M*M-.75*M*h+3*h*h))>=61*M*M/64)
    newdiag=diagnostics(dressed)
    ck(f'K{K} charge exactly unchanged',newdiag['Q_discrete']==olddiag['Q_discrete'])
    ck(f'K{K} energy not increased by preparation',newdiag['E_discrete_laplacian']<=olddiag['E_discrete_laplacian']+1e-10*abs(olddiag['E_discrete_laplacian']))
    ck(f'K{K} positive-face energy identity',newdiag['E_face_vs_laplacian_relative']<1e-10)
    ck(f'K{K} zero net Pz',abs(newdiag['Pz_discrete'])/newdiag['E_discrete_laplacian']<1e-10)
    # An independent energy variation at the RAW off-minimum configuration
    # checks the residual sign against the complete same-grid energy functional.
    directional=None
    if K in [50.,500.]:
        direction=raw[4]-h;direction/=np.max(abs(direction));eps=1e-6
        plus=raw.copy();minus=raw.copy();plus[4]+=eps*direction;minus[4]-=eps*direction
        finite=(diagnostics(plus)['E_discrete_laplacian']-diagnostics(minus)['E_discrete_laplacian'])/(2*eps)
        residual=-lap(raw[4])+M*M*raw[4]-3*M*raw[4]**2/8+raw[4]**3+a*(raw[0]**2+raw[1]**2)
        predicted=float(np.sum(volume*residual*direction))
        relative=abs(finite-predicted)/max(abs(predicted),1.)
        ck(f'K{K} residual is independent energy gradient',relative<1e-5)
        directional={'finite_difference':finite,'residual_prediction':predicted,'relative_difference':relative,'epsilon':eps}
    name=f'dressed_Y20_K{int(K)}.bin';path=out/name
    with path.open('wb') as stream:
        stream.write(struct.pack('<8siidd',b'CEPAIR1\0',Nr,Nz,dx,0.));dressed.astype('<f8').tofile(stream)
    ck(f'K{K} snapshot roundtrip exact',np.array_equal(read_snapshot(path)['fields'],dressed))
    fixed=analyze_snapshot(path,mode_path,profile_path,Qref=Qref,carrier_frequency=om,carrier_phase=0.)
    fitted=analyze_snapshot(path,mode_path,profile_path,Qref=Qref)
    if K==0.:dressed_baseline=newdiag
    excess=newdiag['E_discrete_laplacian']-dressed_baseline['E_discrete_laplacian']-om*(newdiag['Q_discrete']-dressed_baseline['Q_discrete'])
    row={'nominal_K':K,'Q_actual':newdiag['Q_discrete'],'E_laplacian':newdiag['E_discrete_laplacian'],
         'snapshot_file':name,'raw_provenance':raw_provenance,
         'raw_diagnostics':olddiag,'dressed_diagnostics':newdiag,
         'energy_change_from_distinct_preparation':newdiag['E_discrete_laplacian']-olddiag['E_discrete_laplacian'],
         'actual_Delta_E_minus_omega_Delta_Q_from_dressed_K0':excess,
         'static_history':history,'tangent_history':vhist,'Idot_max_abs':float(np.max(abs(Idot))),
         'energy_gradient_control':directional,'reference_frame_projection':fixed,'fitted_carrier_projection':fitted}
    rows.append(row)
    print(json.dumps({'Knom':K,'Q':row['Q_actual'],'E':row['E_laplacian'],'DeltaKactual':excess,
                      'projectedK':fixed['conditional_K_coordinate'],'chi_updates':history[-1]['updates'],
                      'tangent_updates':vhist[-1]['updates']}),flush=True)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;ck('measured RSS below1GB',rss<1_000_000_000)
size=sum(p.stat().st_size for p in out.iterdir() if p.is_file());ck('retained outputs below1GB',size<1_000_000_000)
result={'scope':'Distinct quasistatic-chi initial preparation only; NO dynamics, cooling history or nonlinear periodic solution.',
        'parameters':P,'reference_Q':Qref,'reference_omega':om,'geometry':{'Nr':Nr,'Nz':Nz,'dx':dx},
        'equations':'(-Lap+Uprime)chi=-a|Psi|²; (-Lap+U2)chidot=-a*2Re(Psi*Psidot)',
        'charged_fields':'All eight Psi/X field/momentum arrays unchanged byte-for-byte from each raw seed; neutral chi/chidot replaced only.',
        'diagnostics_source_sha256':hashlib.sha256(old_source.read_bytes()).hexdigest(),
        'rows':rows,'checks':checks,'n_checks':len(checks),'all_checks_pass':all(c['pass'] for c in checks),
        'peak_rss_bytes_macos':rss,'retained_output_bytes_before_result':size,
        'non_claims':['Energy difference is between preparations, NOT energy radiated or physical cooling',
                      'Total boundQ not adjusted to136000','No static adjustment of Psi/X, corrected nonlinear Omega or full DC solution',
                      'No measured softening, persistent mode excitation, capture or dwarf sufficiency']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
