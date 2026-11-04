"""Finite plane-wave first-variation check; not a dynamical stability test."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import law


def run():
    phase=2*np.pi*np.arange(512)/512
    rows=[];backgrounds=[]
    for eta in (2.48,2.05):
        nu=float(law.Qprime(eta*eta))
        nud=-1/(eta*eta*math.sqrt(1+4/eta))
        gap=float(law.R(eta*eta))-nu
        background=dict(eta=eta,nu=nu,nuprime=nud,R=float(law.R(eta*eta)),R_minus_nu=gap,orientations=[])
        for cos2 in (0.,.5,1.):
            direction=np.array([math.sqrt(1-cos2),0.,math.sqrt(cos2)])
            U=nu+eta*nud*cos2
            kc=math.sqrt(U/gap)
            background['orientations'].append(dict(cos2=cos2,U=U,kcrit_times_ell=kc,wavelength_over_ell=2*math.pi/kc))
            for ratio in (.5,1.,2.):
                k=ratio*kc  # ell=a0=1, so the tested k equals k*ell.
                exact=U-gap*k*k
                for eps in (1e-4,1e-5,1e-6):
                    perturb_g=-np.sin(phase)[:,None]*direction[None,:]/k
                    perturb_H=-np.cos(phase)[:,None,None]*np.outer(direction,direction)[None,:,:]
                    base=np.broadcast_to(np.array([0.,0.,eta]),perturb_g.shape)
                    plus=law.tensor_terms(base+eps*perturb_g,eps*perturb_H,1.)
                    minus=law.tensor_terms(base-eps*perturb_g,-eps*perturb_H,1.)
                    dA=(plus['A']-minus['A'])/(2*eps)
                    dB=(plus['B']-minus['B'])/(2*eps)
                    Asin=2*np.mean((dA@direction)*np.sin(phase))
                    Bcos=2*np.mean(np.einsum('i,nij,j->n',direction,dB,direction)*np.cos(phase))
                    # Delta(delta psi)=-cos(phase). The two response-source
                    # amplitudes are k*Asin and k^2*Bcos, respectively.
                    measured=1-k*Asin-k*k*Bcos
                    error=abs(measured-exact)/max(1.,abs(exact))
                    rows.append(dict(eta=eta,cos2=cos2,k_over_kcrit=ratio,k_times_ell=k,epsilon=eps,
                                     transfer_exact=exact,transfer_measured=float(measured),scaled_error=float(error)))
        backgrounds.append(background)
    maximum=max(row['scaled_error'] for row in rows)
    return dict(backgrounds=backgrounds,rows=rows,maximum_scaled_error=maximum,
                all_checks_pass=maximum<1e-6,
                qualification='54 finite central first-variation plane-wave checks; analytic result applies to constant nonzero gradient and zero background Hessian; no dynamic stability conclusion')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    result=run();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ('backgrounds','maximum_scaled_error','all_checks_pass')},indent=2))
    if not result['all_checks_pass']:raise SystemExit(1)
