"""Classify full tree charged modes; check a necessary producer number budget."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis,threshold,summarize
Z0=7.367143721278508


def classify(t,mu):
    e=.003;g=math.sqrt(29/200)*e
    X=t*Z0/math.sqrt(31*e)
    data=build_model(X,e,e,g,vertices=False)
    ext,C=ext_basis(data)
    index=np.where(abs(C)<1e-7)[0]
    assert len(index)==1
    weights=ext[49:,index[0]].real
    Q=np.einsum('a,aij->ij',weights,data['R'])
    Qadj=np.einsum('a,aij->ij',weights,data['R'][:,1:25,1:25])
    QF=np.zeros((73,73),complex);QF[:49,:49]=Q;QF[49:,49:]=Qadj
    qF=np.einsum('ia,ij,ja->a',data['U'].conj(),QF@QF,data['U']).real
    generator=np.block([[-Q.imag,-Q.real],[Q.real,-Q.imag]])
    qS=np.diag(data['O'].T@(-generator@generator)@data['O'])
    qV=np.diag(data['Ov'].T@(Qadj@Qadj).real@data['Ov'])
    scale=max(data['mS2'].max(),data['mF2'].max(),data['mV2'].max())
    sf=(qS>1e-5)&(data['mS2']>1e-10*scale)
    ff=qF>1e-5;vf=qV>1e-5
    S=mu*np.sqrt(data['mS2'][sf]);F=mu*data['mF'][ff];V=mu*np.sqrt(data['mV2'][vf])
    scalar=min(S);fermion=min(F);vector=min(V)
    groups,_=summarize(threshold(data,ext),C)
    chi=mu*groups['U1']['signed_mass']
    positiveF=F[F>mu*math.sqrt(1e-10*scale)]
    return dict(t=t,mu_GeV=mu,charged_scalar_real_count=int(round(sum(qS[sf])/(5/12))),
                charged_Weyl_count=int(round(sum(qF[ff])/(5/12))),charged_vector_real_count=int(round(sum(qV[vf])/(5/12))),
                charged_zero_Weyl_count=int(round(sum(qF[(qF>1e-5)&(data['mF2']<=1e-10*scale)])/(5/12))),
                min_charged_scalar_GeV=float(scalar),min_charged_Weyl_GeV=float(fermion),
                min_positive_charged_Weyl_GeV=float(min(positiveF)),min_charged_vector_GeV=float(vector),
                photino_GeV=float(chi),lightest_kind=min(('scalar','fermion','vector'),key=lambda k:dict(scalar=scalar,fermion=fermion,vector=vector)[k]),
                lightest_charged_GeV=float(min(scalar,fermion,vector)),
                max_charge_squared_error=float(max(abs(np.linalg.eigvalsh(QF@QF)-np.round(np.linalg.eigvalsh(QF@QF)/(5/12))*(5/12)))))


def main(out):
    start=time.monotonic()
    canon=json.loads((HERE/'canonical/run_highprecision/result.json').read_text())['export']['parameters']
    # Protected finite scalar coordinates are pinned; masses here use the
    # leading tree valley at that radius, not an unsupported gravity pole.
    cases=[dict(name='canonical',**classify(float(canon['t']),float(canon['mu']))),
           dict(name='protected',**classify(1.02656394539939,18170662.111498855)),
           dict(name='origin_control',**classify(0.,1.))]
    for row in cases[:2]:
        row['charged_mass_over_photino']=row['lightest_charged_GeV']/row['photino_GeV']
        row['maximum_charged_number_per_photino_for_10percent_rest_density']=.1/row['charged_mass_over_photino']
    checks={
        '36charged_physical_scalar_reals':all(r['charged_scalar_real_count']==36 for r in cases),
        '36charged_Weyls':all(r['charged_Weyl_count']==36 for r in cases),
        '12charged_vector_reals':all(r['charged_vector_real_count']==12 for r in cases),
        'origin_has12charged_zero_Weyls':cases[-1]['charged_zero_Weyl_count']==12,
        'outer_nocharged_zero_Weyls':all(r['charged_zero_Weyl_count']==0 for r in cases[:2]),
        'generator_charge_normalization':max(r['max_charge_squared_error'] for r in cases)<1e-12,
        'heavycompanion_number_obligation':all(r['charged_mass_over_photino']>1e8 for r in cases[:2]),
    }
    result=dict(claim_id='TP06_EXACT_CHARGED_RELIC_OBLIGATION',checks=checks,cases=cases,
                scope='Fulltreechargeclassification at2finiteactionradii andorigin. Exactsingleparticlechargeconservation; producer-specificnumberratio only. Noannihilationorcompletecosmologicalexclusion.',
                runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
