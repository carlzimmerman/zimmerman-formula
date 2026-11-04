"""CT09 leading microscopic charged-fermion -> charged-scalar + gaugino source.

Rigid physical tree bases; exact finite-splitting one-loop unbroken gaugino
mass is inserted in final-state kinematics. This is not a SUGRA 1PI matching.
"""
import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import json,math,time,resource,platform
from functools import lru_cache
import numpy as np
import scipy
from scipy.linalg import eigh
from scipy.optimize import brentq
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis,threshold,summarize
E=.003;G=math.sqrt(29/200)*E;Q2=5/12;XI=.02;GSM=106.75;MP=2.435e18
ZETA3=1.202056903159594;RHO_DM_S=.44e-9;T0=2.3486541805581e-13;GS0=3.909
KIN=ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json'


def adapt(basis,values,charge,zero_unitary=False):
    out=basis.copy();used=np.zeros(len(values),bool)
    for i,val in enumerate(values):
        if used[i]:continue
        ids=np.where(abs(values-val)<1e-11*max(1,abs(val)))[0]
        used[ids]=True;old=out[:,ids];c=old.conj().T@charge@old
        _,rot=eigh(c if zero_unitary and abs(val)<1e-12 else c.real)
        out[:,ids]=old@rot
    return out


def width(M,m,s,y):
    """One real scalar and distinct Majorana daughter, parent spin averaged.

    L=-1/2 y_ij S psi_i psi_j+h.c.  Charged Dirac result is obtained by
    averaging its degenerate Takagi parents, summing physical real scalars.
    """
    if M<=m+s:return np.zeros_like(abs(y)**2)
    lam=(M-s-m)*(M+s+m)*(M-s+m)*(M+s-m)
    amp=abs(y)**2*(M*M+m*m-s*s)+2*(y*y).real*M*m
    return math.sqrt(max(0,lam))/(16*math.pi*M**3)*amp


def scalar_width(S,M,m,y):
    """One real scalar -> two distinct Majorana fermions, sum spin states."""
    if S<=M+m:return np.zeros_like(abs(y)**2)
    lam=(S-M-m)*(S+M+m)*(S-M+m)*(S+M-m)
    amp=abs(y)**2*(S*S-M*M-m*m)-2*(y*y).real*M*m
    return math.sqrt(max(0,lam))/(8*math.pi*S**3)*amp


@lru_cache(None)
def atx(x):
    x=float(x);d=build_model(x,E,E,G,vertices=False);ext,C=ext_basis(d)
    i1=np.where(abs(C)<1e-8)[0];assert len(i1)==1
    w=ext[49:,i1[0]].real
    Q=np.einsum('p,pki->ki',w,d['R']);qq=Q@Q
    QF=np.zeros((73,73),complex);QF[:49,:49]=qq;QF[49:,49:]=qq[1:25,1:25]
    CS=np.block([[qq.real,-qq.imag],[qq.imag,qq.real]])
    O=adapt(d['O'],d['mS2'],CS);U=adapt(d['U'],d['mF'],QF,True)
    qs=np.einsum('ia,ia->a',O,CS@O).real
    qf=np.einsum('ia,ia->a',U.conj(),QF@U).real
    charged=np.where(qf>.1)[0];mF=d['mF'];M=float(min(mF[charged]))
    light=charged[abs(mF[charged]-M)<1e-9];assert len(light)==12
    mS=np.sqrt(np.maximum(d['mS2'],0));physical=(qs>.1)&(d['mS2']>1e-14)
    S=float(min(mS[physical]));Em=d['E']@O
    # The external gauginos have no chiral tree component. Their only leading
    # renormalizable vertex is -sqrt(2) g phi^* T psi lambda. No spurious
    # gaugino part of the parent is inserted into a chiral gauge vertex.
    yy=math.sqrt(2)*G*np.einsum('pe,ka,pki,iu->eua',ext[49:,:],Em.conj(),d['R'],U[:49,light],optimize=True)
    groups,_=summarize(threshold(d,ext),C)
    subgroup={0:'U1',2:'SU2',3:'SU3'}
    widths={};massless={};reverse={};partial=[];reverse_scalar_groups=[]
    # At x=0 two distinct 12-real scalar branches coincide exactly. Average
    # the entire lowest mass block there; away from origin its size is 12.
    smin_ids=np.where(physical&(abs(mS-S)<1e-8))[0];assert len(smin_ids) in (12,24),(x,S,len(smin_ids))
    for cas,name in subgroup.items():
        ids=np.where(abs(C-cas)<1e-8)[0];signed=groups[name]['signed_mass'];mc=abs(signed)
        y=yy[ids]*(1 if signed>=0 else 1j)
        wf=np.zeros((len(ids),12,98));w0=wf.copy()
        for a in np.where(physical)[0]:
            wf[:,:,a]=width(M,mc,float(mS[a]),y[:,:,a]);w0[:,:,a]=width(M,0.,float(mS[a]),y[:,:,a])
        widths[name]=float(wf.sum()/12);massless[name]=float(w0.sum()/12)
        reverse[name]=float(sum(scalar_width(float(mS[a]),M,mc,y[:,:,a]).sum() for a in smin_ids)/len(smin_ids))
        if name=='U1':
            perparent=wf.sum(axis=(0,2));pmin=[];pmean=[]
            for a in np.where(physical)[0]:
                wa=float(wf[:,:,a].sum()/12)
                if wa>1e-30:
                    s=float(mS[a]);p=math.sqrt(max(0,(M-s-mc)*(M+s+mc)*(M-s+mc)*(M+s-mc)))/(2*M)
                    partial.append(dict(scalar_index=int(a),mass_over_mu=s,width_over_mu=wa,pstar_over_mu=p,yukawa_norm2_sum_parents=float(np.sum(abs(y[:,:,a])**2))))
    qnorm=float(np.sum(abs(yy[i1[0]])**2)/12)
    chiral=float(np.sum(abs(U[:49,light])**2)/12)
    expected=2*G*G*Q2*chiral
    # Independent analytic 3x3 middle branch and normalized parent projector.
    a=math.sqrt(2/(31*E));small=np.array([[E*x/2,-E*a/2,5*G*a],[-E*a/2,0,5*G*x],[5*G*a,5*G*x,0.]])
    vals,vec=eigh(small);mi=int(np.argmin(abs(vals)));analytic=abs(float(vals[mi]))
    total=sum(widths.values());wchi=widths['U1']
    pstar=sum(p['width_over_mu']*p['pstar_over_mu'] for p in partial)/wchi if wchi else None
    return dict(x=x,light_fermion_over_mu=M,lightest_scalar_over_mu=S,gauginos_over_mu={k:abs(v['signed_mass']) for k,v in groups.items()},
        widths_over_mu=widths,massless_widths_over_mu=massless,gauge_channels_total_over_mu=total,
        reverse_lightest_scalar_widths_over_mu=reverse,reverse_gauge_channels_total_over_mu=sum(reverse.values()),lightest_scalar_real_count=len(smin_ids),
        reverse_mean_photino_pstar_over_mu=math.sqrt(max(0,(S-M-groups['U1']['signed_mass'])*(S+M+groups['U1']['signed_mass'])*(S-M+groups['U1']['signed_mass'])*(S+M-groups['U1']['signed_mass'])))/(2*S) if S>M+abs(groups['U1']['signed_mass']) else None,
        photino_branching_upper_given_gauge_channels=wchi/total if total else None,
        mean_photino_pstar_over_mu=pstar,charged_scalar_daughters=partial,
        checks=dict(light_Weyls=len(light),physical_charged_scalar_reals=int(sum(physical)),
        Takagi_error=float(np.max(abs(U.T@d['MF']@U-np.diag(mF)))),
        charge_error=float(np.max(abs(U[:,light].conj().T@QF@U[:,light]-np.eye(12)*Q2))),
        projection_sum_relative_error=abs(qnorm/expected-1),parent_chiral_probability=chiral,
        parent_chiral_vs_3x3_error=abs(chiral-(1-vec[2,mi]**2)),
        light_mass_vs_3x3_error=abs(M-analytic),
        massless_Casimir_ratio_error=max((abs(massless[k]/massless['U1']-v) for k,v in [('SU2',1.8),('SU3',3.2)]),default=0) if massless['U1']>0 else 0))


def momentum_source(row,t,mu,mc):
    """Instantaneous unblocked rate source and all-parent prompt moments.

    Conditional f_F(p)=FD(p/Tc), isotropic unpolarized parent, mchi=0 in
    boost only. Exact mchi is already retained in rest-frame phase space.
    """
    if row['mean_photino_pstar_over_mu'] is None:return None
    M=row['light_fermion_over_mu'];pstar=row['mean_photino_pstar_over_mu']
    f=lambda z:1/(math.exp(z)+1)
    N=quad(lambda z:z*z*f(z),0,65,epsabs=1e-12)[0]
    dil=quad(lambda z:z*z*f(z)*M/math.sqrt(M*M+(t*z)**2),0,65,epsabs=1e-12)[0]/N
    gam=quad(lambda z:z*z*f(z)*math.sqrt(M*M+(t*z)**2)/M,0,65,epsabs=1e-12)[0]/N
    rate_p=pstar/dil;prompt_p=pstar*gam
    to_p0=XI/t*T0*(GS0/GSM)**(1/3)
    return dict(time_dilation_mean=dil,mean_parent_gamma=gam,
        mean_p_source_over_TSM=rate_p*XI/t,mean_p_prompt_over_TSM=prompt_p*XI/t,
        mean_v0_source=rate_p*to_p0/mc,mean_v0_prompt=prompt_p*to_p0/mc,
        daughter_mass_neglected_only_in_boost_relative_scale=mc/(max(pstar*mu,1e-300)),
        source_scope='Fixed background and fixed frozen FD occupation. No abundance/backreaction solution; source spin averaged, vacuum width, no inverse or Pauli factors.')


def main(out):
    start=time.monotonic();old=json.loads(KIN.read_text());packets=old['points']
    grid=[0.,.184443,.26895,1.,2.,3.,5.,7.5,10.,15.,20.,25.,30.,50.,100.,200.]
    # Finite diagnostic crossing of the lightest physical scalar and light F.
    root=brentq(lambda x:atx(x)['light_fermion_over_mu']-atx(x)['lightest_scalar_over_mu']-atx(x)['gauginos_over_mu']['U1'],1.,10.,xtol=2e-11)
    grid.extend([root-1e-4,root+1e-4,root+.01,root+.1])
    table=[atx(float(x)) for x in sorted(set(grid))]
    Y0=135*ZETA3*24/(8*math.pi**4*GSM)*XI**3
    cases=[];conditional=[]
    for packet in packets:
        kind=packet['kind'];mu=packet['mu_GeV'];vac=atx(float(packet['xvac']));mc=vac['gauginos_over_mu']['U1']*mu;ms=vac['lightest_scalar_over_mu']*mu
        Ydm=RHO_DM_S/mc;B=vac['photino_branching_upper_given_gauge_channels']
        cases.append(dict(kind=kind,mu_GeV=mu,x_vacuum=packet['xvac'],vacuum=vac,
            photino_GeV=mc,stable_charged_scalar_GeV=ms,initial_charged_yield=Y0,
            target_photino_yield=Ydm,one_pass_DM_fraction_branching_one=Y0/Ydm,
            one_pass_DM_fraction_using_gauge_branching_upper=Y0*B/Ydm,
            minimum_one_pass_initial_yield_for_DM=Ydm/B,
            charged_yield_gate=.1*RHO_DM_S/ms,
            required_remaining_companions_per_photino=.1*mc/ms,
            one_pass_companion_fraction_gate=(.1*RHO_DM_S/ms)/Y0))
        for t in [.004,.003,.002,.001,.00064]:
            branch=min((p for p in packet['branches'] if p['mode']=='frozen_only'),key=lambda p:abs(p['t']-t))
            minima=[p for p in branch['extrema'] if p['minimum']]
            assert len(minima)==1
            x=minima[0]['x'];r=atx(float(x));H=math.sqrt(math.pi**2*GSM/90)*(t*mu/XI)**2/MP
            mcnow=r['gauginos_over_mu']['U1']*mu
            conditional.append(dict(kind=kind,t=t,x=x,source=r,width_chi_GeV=r['widths_over_mu']['U1']*mu,
                Gamma_chi_over_H=r['widths_over_mu']['U1']*mu/H,
                Gamma_chi_over_origin_roll=r['widths_over_mu']['U1']/1.825e-6,
                Gamma_S_to_F_chi_over_origin_roll=r['reverse_lightest_scalar_widths_over_mu']['U1']/1.825e-6,
                Gamma_S_to_F_all_gauginos_over_origin_roll=r['reverse_gauge_channels_total_over_mu']/1.825e-6,
                momentum=momentum_source(r,t,mu,mc)))
    # Analytic width normalization: a single chiral Dirac-to-complex-scalar
    # vertex h projects to four y=h/2 real/Takagi terms; per parent sum=h²/2.
    h=.2;M=3.;s=.7
    got=float(sum(width(M,0.,s,np.array([h/2,1j*h/2]))))
    known=h*h*M/(32*math.pi)*(1-s*s/M**2)**2
    checks=dict(all_12_light_Weyls=all(r['checks']['light_Weyls']==12 for r in table),
        all_36_charged_scalar_reals=all(r['checks']['physical_charged_scalar_reals']==36 for r in table),
        adapted_Takagi=max(r['checks']['Takagi_error'] for r in table)<1e-9,
        exact_charge=max(r['checks']['charge_error'] for r in table)<1e-10,
        vertex_completeness=max(r['checks']['projection_sum_relative_error'] for r in table)<1e-9,
        independent_3x3_mass=max(r['checks']['light_mass_vs_3x3_error'] for r in table)<1e-10,
        independent_3x3_chiral_probability=max(r['checks']['parent_chiral_vs_3x3_error'] for r in table)<1e-8,
        Casimir_ratio=max(r['checks']['massless_Casimir_ratio_error'] for r in table)<1e-8,
        normalization_Dirac_chiral=abs(got/known-1)<1e-13,
        threshold_bracket=atx(root-1e-4)['widths_over_mu']['U1']==0 and atx(root+1e-4)['widths_over_mu']['U1']>0,
        nonnegative_widths=all(min(r['widths_over_mu'].values())>=0 for r in table))
    result=dict(claim_id='CT09_CHARGED_TO_PHOTINO_SOURCE',checks=checks,threshold_x=root,
        threshold_residual=atx(root)['light_fermion_over_mu']-atx(root)['lightest_scalar_over_mu']-atx(root)['gauginos_over_mu']['U1'],
        grid=table,vacua=cases,conditional_stationary_examples=conditional,
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Leading rigid gauge vertex and physical tree charged states; exact finite one-loop gaugino masses in phase space. No SUGRA transverse neutral 1PI matching, all-channel cascade/annihilation closure, source abundance solution, or one-pass bound on histories that regenerate charged fermions.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=checks,threshold_x=root,initial_Y=Y0,vacua=[{k:v for k,v in c.items() if k!='vacuum'} for c in cases],conditional=[{k:v for k,v in c.items() if k!='source'} for c in conditional],runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes']),indent=2))
    assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
