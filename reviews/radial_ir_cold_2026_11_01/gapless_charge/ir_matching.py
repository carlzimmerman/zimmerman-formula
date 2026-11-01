"""Full finite-splitting one-loop threshold logs and conditional IR scales."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
import math,json,resource
from gaugino_threshold import build_model,ext_basis,Z0,L

def matching(data,ext,C,Q0):
    R=data['R'];n=len(data['z']);nf=len(data['mF']);O=data['O'];U=data['U'];ms=data['mS2'];mf=data['mF']
    RF=np.zeros((24,nf,nf),complex);RF[:,:n,:n]=R;RF[:,n:,n:]=R[:,1:25,1:25]
    Qr=np.r_[1.,-np.ones(24),np.ones(24),np.ones(24)]
    out={}
    for c,name in [(3,'SU3'),(2,'SU2'),(0,'U1')]:
        u=int(np.where(abs(C-c)<1e-7)[0][0]);coef=ext[n:,u].real
        rep=np.einsum('a,aij->ij',coef,R);repF=np.einsum('a,aij->ij',coef,RF)
        Jr=np.block([[-rep.imag,-rep.real],[rep.real,-rep.imag]])
        Jm=O.T@Jr@O;ws=np.sum(Jm**2,axis=1)/6
        G=U.conj().T@repF@U;wf=np.sum(abs(G)**2,axis=1)*2/3
        ps=ms>0;pf=mf>0;TX=5-c;mv=math.sqrt(max(data['mV2']))
        logs=float(np.dot(ws[ps],np.log(Q0/np.sqrt(ms[ps])))+np.dot(wf[pf],np.log(Q0/mf[pf]))-3.5*TX*math.log(Q0/mv))
        weights=float(sum(ws[ps])+sum(wf[pf])-3.5*TX)
        anomaly=float(np.trace(np.diag(Qr)@repF@repF).real)
        out[name]={'C':c,'T_coset':TX,'heavy_beta_weight':weights,'R_anomaly':anomaly,
                   'threshold_delta_inverse_g2':logs/(8*math.pi**2),
                   'massless_scalar_weight':float(sum(ws[~ps])),
                   'massless_fermion_weight':float(sum(wf[~pf]))}
    return out

def run(path):
    prior=json.loads((Path(__file__).parent/'run_003/result.json').read_text());cases=[];checks={}
    for e in [.01,.03,.0001]:
        X=Z0/math.sqrt(31*e);g=math.sqrt(29/200)*e;Q0=math.sqrt(e*(1+Z0**2)/31)
        data=build_model(X,e,e,g,vertices=False);ext,C=ext_basis(data);mt=matching(data,ext,C,Q0)
        masses=next(x['groups'] for x in prior['cases'] if x['e']==e and x['r']==1.)
        for name,item in mt.items():
            c=item['C'];ml=abs(masses[name]['signed_mass']);iq=1/g**2+item['threshold_delta_inverse_g2']
            im=iq+3*c/(8*math.pi**2)*math.log(ml/Q0)
            item.update(m_lambda_over_mu=ml,inverse_g2_at_Q0_below_heavies=iq,inverse_g2_at_m_lambda=im,
                        alpha_at_m_lambda=1/(4*math.pi*im))
            if c:
                item['log10_LambdaYM_over_mu']=(math.log(ml)-8*math.pi**2*im/((11/3)*c))/math.log(10)
                item['log10_LambdaSYM_formal_over_mu']=(math.log(Q0)-8*math.pi**2*iq/(3*c))/math.log(10)
                # Alpha(T) must subsequently be run within Lambda<<T<<m_lambda.
                # This coefficient at m_lambda is a reference, not a selected T.
                alpha=item['alpha_at_m_lambda']
                item['thermal_reference_drift_per_unknown_kappa_tau_cubed']=25*e/(4*Z0**2)*alpha**5*math.log(1/alpha)
            checks['heavy_weight_'+name+'_'+str(e)]=abs(item['heavy_beta_weight']-{'SU3':4,'SU2':1,'U1':-5}[name])<2e-8
            checks['R_anomaly_'+name+'_'+str(e)]=abs(item['R_anomaly']-5)<2e-10
            checks['positive_IR_inverse_'+name+'_'+str(e)]=im>0
        g1sq=1/mt['U1']['inverse_g2_at_Q0_below_heavies'];kappa=5*g1sq/(8*math.pi**2)
        # Work in omega=1 units. All k and growth then quote /|omega|.
        opt=minimize_scalar(lambda k:-(max(0,kappa*k-k*k))**.5,bounds=(0,kappa),method='bounded',options={'xatol':kappa*1e-10})
        growth=kappa/2;direct=-opt.fun
        sigma=10*kappa;damped=(math.sqrt(sigma*sigma+kappa*kappa)-sigma)/2
        checks['helicity_extremum_'+str(e)]=abs(direct/growth-1)<1e-9
        checks['conductivity_equation_'+str(e)]=abs((damped*damped+sigma*damped-kappa*kappa/4)/(kappa*kappa))<1e-12
        cases.append({'e':e,'X':X,'Q0_over_mu':Q0,'groups':mt,
                      'helicity':{'k_band_max_over_absomega':kappa,'growth_max_over_absomega':growth,
                                  'damped_growth_sigma_10kappa_over_absomega':damped}})
    checks={k:bool(v) for k,v in checks.items()}
    result={'claim_id':'TP04-IR-ANOMALY','checks':checks,'cases':cases,
            'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'One-loop decoupling logs and formal IR scales; no nonperturbative rate or gap certificate.'}
    Path(path).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks

if __name__=='__main__':run(sys.argv[1])
