"""Actual canonical4P->brokenVV width matrices and corrected-history coverage."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
from pathlib import Path
import json,time,math,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/neutral_loop'))
from loop import build
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from network import adapt,DCOEF,T,table
from coverage import coverage
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/integration'))
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit

def physical_scalar_basis(d):
    R=d['R'];ry=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),R);q=ry@ry;QS=np.block([[q.real,-q.imag],[q.imag,q.real]])
    V=np.diag([2,2,2,-3,-3]);un=[a for a,t in enumerate(T) if np.max(abs(t@V-V@t))<1e-12]
    c=np.einsum('aij,ajk->ik',R[un],R[un]);CS=np.block([[c.real,-c.imag],[c.imag,c.real]])
    O=adapt(d['O'],d['mS2'],QS);return adapt(O,d['mS2']+np.einsum('ia,ia->a',O,QS@O).real,CS)

def vv_width(K,mv,M):
    out=np.zeros((len(K),len(K)));rows=[]
    for i in range(len(mv)):
        if mv[i]<=1e-10:continue
        for j in range(i,len(mv)):
            if mv[j]<=1e-10 or M<=mv[i]+mv[j]:continue
            a,b=mv[i]/M,mv[j]/M;phase=math.sqrt((1-(a+b)**2)*(1-(a-b)**2))
            polar=2+(M*M-mv[i]**2-mv[j]**2)**2/(4*mv[i]**2*mv[j]**2)
            coefficient=phase*polar/(16*math.pi*M*(1+int(i==j)))
            v=K[:,i,j];mat=coefficient*np.outer(v,v);out+=mat
            rows.append(dict(i=i,j=j,m1=float(mv[i]),m2=float(mv[j]),polarization_factor=polar,
                             symmetry_factor=1/(1+int(i==j)),trace_width=float(np.trace(mat))))
    return out,rows

def other_width(cube,yuk,ms,mf,physical,P,M):
    z=ms/M;ri=z[:,None]**2;rj=z[None,:]**2;phase=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));allowed=(z[:,None]+z[None,:]<1-1e-12)&physical[:,None]&physical[None,:]
    c=cube[P];SS=np.einsum('aij,bij,ij->ab',c,c,phase*allowed,optimize=True)/(32*math.pi*M)
    z=mf/M;ri=z[:,None]**2;rj=z[None,:]**2;phase=np.sqrt(np.maximum(0,(1-ri-rj)**2-4*ri*rj));allowed=z[:,None]+z[None,:]<1-1e-12;y=yuk[:,:,P].transpose(2,0,1)
    FF=M/(16*math.pi)*(np.einsum('aij,bij,ij->ab',y,y.conj(),phase*allowed*(1-ri-rj),optimize=True).real-2*np.einsum('aij,bij,ij->ab',y,y,phase*allowed*z[:,None]*z[None,:],optimize=True).real)
    return SS,FF

def polarization_check(M,m1,m2):
    p=math.sqrt((M-m1-m2)*(M+m1+m2)*(M-m1+m2)*(M+m1-m2))/(2*M);E1=math.sqrt(m1*m1+p*p);E2=math.sqrt(m2*m2+p*p)
    e1=np.asarray([[0,1,0,0],[0,0,1,0],[p/m1,0,0,E1/m1]],float)
    e2=np.asarray([[0,1,0,0],[0,0,1,0],[p/m2,0,0,-E2/m2]],float);metric=np.diag([1.,-1.,-1.,-1.])
    direct=float(np.sum((e1@metric@e2.T)**2));closed=2+(M*M-m1*m1-m2*m2)**2/(4*m1*m1*m2*m2)
    return dict(explicit=direct,closed=closed,relative_error=abs(direct/closed-1))

def case(x):
    d,s,cube,yuk,K,qs,qf,qv,ms,mf,mv,physical,gold,controls,beta=build(float(x),.003)
    P=[i for i in range(98) if physical[i] and not s['charged'][i] and abs(ms[i]-math.sqrt(.006))<1e-8]
    parent=next(g for g in s['groups'] if set(P)<=set(g['indices']));M=float(np.mean(ms[P]));massive=np.flatnonzero(mv>1e-10);Kv=K[P]
    Gamma,pairs=vv_width(Kv,mv,M);SS,FF=other_width(cube,yuk,ms,mf,physical,P,M);other=SS+FF
    # Independent reference uses the grouped physical tree operator.
    net=table(float(x),derivative=False);ref=sum(np.asarray(v) for v in net['singlet_channel_Gamma'].values())
    reference_error=float(np.linalg.norm(other-ref)/np.linalg.norm(ref))
    O=physical_scalar_basis(d);physical_ids=np.flatnonzero(physical);dominant=int(physical_ids[np.argmax(np.max(abs(K[physical_ids]),axis=(1,2)))])
    derivative_ids=P+[dominant];directions=d['E']@O[:,derivative_ids];eps=1e-3;finite=[]
    for a in range(len(derivative_ids)):
        def massmatrix(z):
            rz=np.einsum('aij,j->ai',d['R'],z);return 2*d['g']**2*(rz.conj()@rz.T).real
        derivative=(massmatrix(d['z']+eps*directions[:,a])-massmatrix(d['z']-eps*directions[:,a]))/(2*eps)
        finite.append(d['Ov'].T@derivative@d['Ov'])
    fd_error=float(np.max(abs(np.asarray(finite)-K[derivative_ids])));fd_scale=max(float(np.max(abs(K))),1e-300)
    # Rotate all12 degenerate massive real vectors and the4 parents.
    rng=np.random.default_rng(20261104);RP=np.linalg.qr(rng.normal(size=(4,4)))[0];RV=np.eye(len(mv));rv=np.linalg.qr(rng.normal(size=(len(massive),len(massive))))[0];RV[np.ix_(massive,massive)]=rv
    KP=np.einsum('ab,aij->bij',RP,Kv,optimize=True);KR=np.einsum('ik,akl,lj->aij',RV.T,KP,RV,optimize=True)
    comparison_scale=max(float(np.linalg.norm(Gamma)),float(np.linalg.norm(other))*1e-12,1e-30)
    rotated,_=vv_width(KR,mv,M);target=RP.T@Gamma@RP;rotation_error=float(np.linalg.norm(rotated-target)/comparison_scale)
    # A singlet's real vector block must be proportional to identity.
    block=Kv[:,massive][:,:,massive];c=np.trace(block,axis1=1,axis2=2)/len(massive)
    singlet_residual=float(np.linalg.norm(block-c[:,None,None]*np.eye(len(massive)))/max(np.linalg.norm(block),fd_scale))
    ident=np.zeros((4,4));complex_total=np.zeros((4,4));pol=None
    if M>2*float(max(mv)):
        m=float(np.mean(mv[massive]));r=m*m/M**2;coef=M**3/(128*math.pi*m**4)*math.sqrt(1-4*r)*(1-4*r+12*r*r)
        ident=len(massive)*coef*np.outer(c,c)
        # Six charged complex vectors: each distinct V+V- width is twice one
        # identical real component, giving exactly the same physical count.
        complex_total=(len(massive)/2)*(2*coef)*np.outer(c,c)
        pol=polarization_check(M,m,m)
    special_error=float(np.linalg.norm(ident-Gamma)/comparison_scale)
    complex_error=float(np.linalg.norm(complex_total-Gamma)/comparison_scale)
    ev,V=np.linalg.eigh(other);invsqrt=(V*(1/np.sqrt(ev))[None,:])@V.T;relative_eigs=np.linalg.eigvalsh(invsqrt@Gamma@invsqrt)
    # Gauge Ward normalization compares the canonical Goldstone cubic.
    cg=np.einsum('aij,ip,jq->apq',cube[P],gold,gold,optimize=True)
    ward_target=M*M*block/(2*mv[massive,None]*mv[None,massive]);ward_error=float(np.max(abs(cg-ward_target)))
    return dict(x=float(x),parent_id=parent['id'],parent_indices=P,parent_mass=M,massive_vector_count=len(massive),
        massive_vector_mass_range=[float(min(mv[massive])),float(max(mv[massive]))],VV_kinematically_open=bool(M>2*float(min(mv[massive]))),
        K_parent_broken_vector=block.tolist(),K_singlet_identity_coefficients=c.tolist(),Gamma_VV=Gamma.tolist(),Gamma_SSS=SS.tolist(),Gamma_FFS=FF.tolist(),
        Gamma_VV_eigenvalues=np.linalg.eigvalsh(Gamma).tolist(),Gamma_other_eigenvalues=ev.tolist(),Gamma_total_eigenvalues=np.linalg.eigvalsh(other+Gamma).tolist(),
        average_Gamma_VV=float(np.trace(Gamma)/4),average_Gamma_other=float(np.trace(other)/4),
        VV_over_other_trace=float(np.trace(Gamma)/np.trace(other)),relative_width_form_eigenvalues=relative_eigs.tolist(),
        finite_derivative_absolute_error=fd_error,finite_derivative_scaled_error=fd_error/fd_scale,finite_derivative_scalar_indices=derivative_ids,
        P_K_over_global_K=float(np.max(abs(Kv)))/fd_scale,width_comparison_scale=comparison_scale,
        vector_parent_basis_covariance_relative=rotation_error,singlet_vector_identity_relative=singlet_residual,
        identical_special_formula_relative=special_error,real_vs_complex_count_relative=complex_error,
        polarization_control=pol,other_width_reference_relative=reference_error,Goldstone_Ward_absolute_error=ward_error,
        open_vector_pairs=pairs,source_controls=controls)

def coverage_case():
    path=ROOT/'reviews/collision_completion_2026_11_04/history/run_advance002/result.json';r=json.loads(path.read_text());m=json.loads((path.parent/'manifest.json').read_text());assert m['run']['status']=='completed' and all(r['checks'].values())
    state=r['state'];q=np.asarray(r['case']['q']);W=np.asarray(r['case']['W']);bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');model=GenericOrbit(bg,q,W,8);model.J0=state['J0'];model.last_x=state['xmid'];Y=np.asarray(state['Y']);f=Y/model.measure;N=state['N'];t=.004657258204883617*math.exp(-N)
    orbit=model.orbit(N,Y,J=state['J']);rows=[]
    for x,w in zip(orbit['xs'],orbit['weights']):
        data=bg.at(float(x));c=coverage(data,t,q,W,f);c.update(x=float(x),weight=float(w),m_vector=data['m_vector']);rows.append(c)
    h=r['case']['history'][-1]
    return dict(input=str(path.relative_to(ROOT)),N=N,xmid=state['xmid'],q_nodes=len(q),phase_nodes=len(rows),cases=rows,
        reconstructed_turningpoints=[orbit['x_inner'],orbit['x_outer']],recorded_turningpoints=[h['x_inner'],h['x_outer']],
        turningpoint_error=max(abs(orbit['x_inner']-h['x_inner']),abs(orbit['x_outer']-h['x_outer'])),
        phase_averaged_eligible_number_fraction=float(sum(z['weight']*z['number_fraction'] for z in rows)),
        phase_averaged_eligible_energy_fraction=float(sum(z['weight']*z['energy_fraction'] for z in rows)),
        maximum_eligible_number_fraction=max(z['number_fraction'] for z in rows),maximum_eligible_energy_fraction=max(z['energy_fraction'] for z in rows),
        scope='Existing conservative V+S/F kinematic eligibility on actual corrected historyY and eight-phase orbit. These fractions are not omitted rates or an abundance correction. Actual VV4parent widths are separate.')

def normalization_controls():
    rows=[]
    for mass in (.02,.2,.49):
        M=1.;c=.003;r=mass*mass
        gamma,_=vv_width(np.asarray([[[c]]]),np.asarray([mass]),M)
        special=c*c*M**3/(128*math.pi*mass**4)*math.sqrt(1-4*r)*(1-4*r+12*r*r)
        two,_=vv_width(np.asarray([c*np.eye(2)]),np.asarray([mass,mass]),M)
        pol=polarization_check(M,mass,mass)
        rows.append(dict(M=M,m_vector=mass,c=c,one_real_width=float(gamma[0,0]),special_width=special,
                         special_relative=abs(gamma[0,0]/special-1),two_real_over_one_complex=two[0,0]/(2*special),polarization_relative=pol['relative_error']))
    # A distinct unequal-mass pair uses no identical-state half.
    pol=polarization_check(.1,.02,.03)
    return dict(identical_real_and_complex=rows,unequal_mass_polarization=pol)

def main(out):
    start=time.monotonic();pole=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_pole002/result.json').read_text())
    corrected=json.loads((ROOT/'reviews/collision_completion_2026_11_04/history/run_advance002/result.json').read_text())
    rows=[case(x) for x in (3.82758980160111,4.078635719944046,float(corrected['state']['xmid']),pole['xpole'])];cov=coverage_case();normal=normalization_controls()
    checks=dict(twelve_real_vectors=all(r['massive_vector_count']==12 for r in rows),actual_four_parents=all(r['parent_id']=='S1_1' and len(r['parent_indices'])==4 for r in rows),
        positive_width=all(min(r['Gamma_VV_eigenvalues'])>-1e-18 for r in rows),other_width_reference=all(r['other_width_reference_relative']<1e-10 for r in rows),
        canonical_derivative=all(r['finite_derivative_scaled_error']<1e-7 for r in rows),basis_covariance=all(r['vector_parent_basis_covariance_relative']<1e-9 for r in rows),
        singlet_covariance=all(r['singlet_vector_identity_relative']<1e-9 for r in rows),special_formula=all(r['identical_special_formula_relative']<1e-9 and r['real_vs_complex_count_relative']<1e-9 for r in rows),
        polarizations=all(r['polarization_control'] is None or r['polarization_control']['relative_error']<1e-12 for r in rows),Goldstone_Ward=all(r['Goldstone_Ward_absolute_error']<1e-10 for r in rows),
        independent_special_normalization=all(r['special_relative']<1e-12 and abs(r['two_real_over_one_complex']-1)<1e-12 and r['polarization_relative']<1e-12 for r in normal['identical_real_and_complex']) and normal['unequal_mass_polarization']['relative_error']<1e-12,
        cold_on_shell_closed=not rows[-1]['VV_kinematically_open'] and rows[-1]['average_Gamma_VV']==0,
        coverage_fractions=all(0<=z['number_fraction']<=1 and 0<=z['energy_fraction']<=1 for z in cov['cases']),corrected_orbit_reconstruction=cov['turningpoint_error']<1e-8)
    result=dict(claim_id='CC10_ACTUAL_FOUR_SINGLET_BROKEN_VECTOR_PAIR_PROBE',checks={k:bool(v) for k,v in checks.items()},cases=rows,corrected_history_coverage=cov,normalization_controls=normal,
        scope='Actual canonical tree4parent->12realbroken-vectorpair width matrices and existing kinematic coverage only. No occupiedvectorbath, inversevectornetwork, V+S/Fwidths, offshellvectorchannels or fullcascade/history recomputation.',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=result['checks'],rows=[{k:r[k] for k in ('x','parent_indices','massive_vector_mass_range','VV_kinematically_open','average_Gamma_VV','average_Gamma_other','VV_over_other_trace','relative_width_form_eigenvalues')} for r in rows],coverage={k:cov[k] for k in ('phase_averaged_eligible_number_fraction','phase_averaged_eligible_energy_fraction','maximum_eligible_number_fraction','maximum_eligible_energy_fraction')},runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
