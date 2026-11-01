"""Finite spectrum/arithmetic evaluation of DERIVATION.md's hard-loop bound."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,math,resource
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;PARENT=HERE.parents[1];ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE.parent))
from gaugino_threshold import build_model,ext_basis,Z0

def run(path):
    e=.003;g=math.sqrt(29/200)*e;L=16*math.pi**2
    d=build_model(Z0/math.sqrt(31*e),e,e,g,vertices=False)
    ext,Cas=ext_basis(d);iy=int(np.where(abs(Cas)<1e-7)[0][0]);cy=ext[49:,iy].real
    Q=np.einsum('a,aij->ij',cy,d['R']);adjQ=Q[1:25,1:25]
    Jr=np.block([[-Q.imag,-Q.real],[Q.real,-Q.imag]])
    rz=np.einsum('aij,j->ai',d['R'],d['z'])
    Gold=math.sqrt(2)*np.concatenate([-rz.imag,rz.real],axis=1).T
    Hxi=d['H']+g*g*Gold@Gold.T
    ms,O=eigh(Hxi);ms[abs(ms)<2e-11*max(abs(ms))]=0
    RF=np.zeros((73,73),complex);RF[:49,:49]=Q;RF[49:,49:]=adjQ
    cs=np.linalg.norm(Jr@O,axis=0)>1e-8
    cf=np.linalg.norm(RF@d['U'],axis=0)>1e-8
    cv=np.linalg.norm(adjQ@d['Ov'],axis=0)>1e-8
    Mhat=min(math.sqrt(min(ms[cs])),min(d['mF'][cf]),math.sqrt(min(d['mV2'][cv])))
    Mmax=max(math.sqrt(max(ms)),max(d['mF']),math.sqrt(max(d['mV2'])))
    ratio=Mmax/Mhat
    op=max(np.linalg.norm(r[1:25,1:25],2) for r in d['R'])
    casimir=np.einsum('aij,ajk->ik',d['R'][:,1:25,1:25],d['R'][:,1:25,1:25])
    scalar_yukawa_sum=2*g*g*float(np.trace(Q@Q).real)
    vector_current_sum=g*g*float(cy@casimir.real@cy)
    # Static representation identities, not fitted Wilson coefficients.
    checks={'charged_counts':(int(sum(cs)),int(sum(cf)),int(sum(cv)))==(48,36,12),
            'positive_charged_resolvents':min(ms[cs])>0 and min(d['mF'][cf])>0 and min(d['mV2'][cv])>0,
            'mass_ratio_below_100':ratio<100,
            'full_bundle_below_512':98+4*24+4*73<512,
            'adjoint_Casimir5':np.max(abs(casimir-5*np.eye(24)))<1e-12,
            'generator_norm_below_sqrt5':op<math.sqrt(5),
            'scalar_external_gaugino_Frobenius20':abs(scalar_yukawa_sum/(20*g*g)-1)<1e-12,
            'vector_external_gaugino_Frobenius5':abs(vector_current_sum/(5*g*g)-1)<1e-12}
    # All numerical constants below were fixed in the written pre-run proof.
    kappa=100.;Y=32*g*math.sqrt(5);B=32*g*math.sqrt(5)*(1+kappa);S=64*g*g*5
    Bloop=2*64*512*256*4/(15*L)*Y*Y*max(B*B,S)
    c7max=512*Bloop
    units=json.loads((PARENT/'run_units/result.json').read_text())
    m=.001;mu=m/(units['photino_mass_coefficient']*e**2.5);M=mu*Mhat
    GammaG=31*m**5/(16*math.pi*mu**4);factor=m**7/(256*math.pi**3*M**6)
    GammaHard=c7max*c7max*factor;hbar=units['constants']['hbar_GeV_s'];age=units['constants']['required_lifetime_s']
    c7age=math.sqrt((hbar/age-GammaG)/factor)
    c799=math.sqrt((-math.log(.99)*hbar/age-GammaG)/factor)
    survival=math.exp(-(GammaG+GammaHard)*age/hbar)
    checks.update({'external_momentum_ratio_below_2e_9':m/M<2e-9,
                   'hard_bound_below_Goldstino_partial':GammaHard<GammaG,
                   'retained_channel_survival_above_99percent':survival>.99,
                   'c7_bound_below_age_budget':c7max<c7age})
    out={'claim_id':'TP04-HARD-ONELOOP-MAJORANT','checks':{k:bool(v) for k,v in checks.items()},
         'spectrum':{'e':e,'g':g,'charged_counts':[int(sum(cs)),int(sum(cf)),int(sum(cv))],
                     'Mcharged_hat_xi1':Mhat,'Mmax_hat':Mmax,'actual_mass_ratio':ratio,'kappa_envelope':kappa,
                     'max_generator_operator_norm':float(op),'scalar_yukawa_Frobenius_squared':scalar_yukawa_sum,'vector_current_Frobenius_squared':vector_current_sum},
         'majorant':{'Y':Y,'B':B,'S':S,'Bloop':Bloop,'inclusive_c7_effective_upper':c7max},
         'benchmark':{'m_GeV':m,'mu_GeV':mu,'Mcharged_GeV':M,'m_over_M':m/M,'Gamma_Goldstino_partial_GeV':GammaG,
                      'Gamma_hard_upper_GeV':GammaHard,'hard_bound_over_Goldstino':GammaHard/GammaG,
                      'c7_age_budget':c7age,'c7_99percent_budget':c799,'retained_channel_survival_lower':survival},
         'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'scope':'Analytic norm bound for leading one-loop hard two-vector transition class only; not all-orders total width.'}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(out['checks'].values()),out['checks']
if __name__=='__main__':run(sys.argv[1])
