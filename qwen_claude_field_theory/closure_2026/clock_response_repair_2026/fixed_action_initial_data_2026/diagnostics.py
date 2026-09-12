#!/usr/bin/env python3
"""Independent diagnostics of archived early-clock samples; no new evolution."""
import argparse
import json
from pathlib import Path
import numpy as np
from initial_data import FrozenBackground
from transfer_evolve import mode_system


def ratios(charge,baryon_charge,radiation_charge):
    return dict(chi_over_baryon=charge/baryon_charge,
                chi_over_radiation_power=charge/radiation_charge**.75,
                baryon_over_radiation_power=baryon_charge/radiation_charge**.75)


def diagnose(path):
    bg=FrozenBackground()
    archive=json.loads(path.read_text())
    branches=[]
    for branch in archive['continuations']:
        rows=[]
        for point in branch['samples']:
            physical=[point[k] for k in ('a','H','q','tau','baryon','radiation')]
            v,matrix,_,_=bg.evaluate(physical,extended=True)
            coeff=bg.model.background(point['tau'])
            qb,U,d,Hb,_=coeff['raw'][:5]
            qb1,U1,d1,Hb1,_=coeff['raw'][5:10]
            q,H,g=v['q'],v['H'],v['gamma']
            relative=1-2*d*q*q/U
            reference=1-2*d*qb*qb/U
            ratio_rate=d1/U-d*U1/U**2
            relative_rate=-2*q*q*ratio_rate
            reference_rate=-2*qb*qb*ratio_rate-4*d*qb*qb1/U
            rho_direct=(U/relative+U/2*np.log(relative/reference)
                        +3*g*qb*Hb*(q*q+qb*qb)-6*g*H*q**3)
            pt_direct=(-U1/2*np.log(relative/reference)
                       -U/2*(relative_rate/relative-reference_rate/reference)
                       +3*g*((qb1*Hb+qb*Hb1)*(q*q-qb*qb)-2*qb*qb*Hb*qb1))
            W_direct=U-2*g*qb*qb*qb1
            H_direct=(pt_direct-U1)/(3*W_direct)
            spectra=[]
            for mode in point['high_k']:
                k=mode['k'];operator,*_=mode_system(v,k);frequency=k/v['a']
                scales=np.array([1.,frequency,1.,frequency,1.,max(v['rho'],1.)*frequency])
                balanced=operator*scales[None,:]/scales[:,None]/frequency
                values,vectors=np.linalg.eig(balanced)
                residual=np.linalg.norm(balanced@vectors-vectors*values[None,:])
                denominator=1+np.linalg.norm(balanced)*np.linalg.norm(vectors)
                spectra.append(dict(k=k,clock_cs2=mode['clock_cs2'],
                                    eigenvector_condition=float(np.linalg.cond(vectors)),
                                    scaled_eigen_residual=float(residual/denominator),
                                    balanced_operator_norm=float(np.linalg.norm(balanced))))
            D=2*q*q*v['WY']/v['W']
            B=2*v['PX']+4*q*q*v['PXX']
            general=(2*v['PX']*(1-D)-2*v['sbar']*v['WY'])/(B*(1-D))
            rows.append(dict(loga=point['loga'],background_determinant=float(np.linalg.det(matrix)),
                             background_condition=float(np.linalg.cond(matrix)),
                             relative_logarithm_margin=point['relative_logarithm_margin'],
                             clock_rate=v['sbar'],clock_cs2=point['clock_cs2'],
                             closure_gamma0_formula=point['gamma0_formula'],
                             general_gamma0_formula=float(general),
                             spectra=spectra,
                             direct_density_relative_difference=float(abs(rho_direct-point['stress']['rho_clock'])/(1+abs(rho_direct))),
                             direct_clock_H_relative_difference=float(abs(H_direct-H)/(1+abs(H)))))
        p=branch['samples'][0]
        branches.append(dict(initial=branch['initial'],direction=branch['direction'],
                             outcome=branch['outcome'],rows=rows,
                             conserved_ratios=ratios(p['scalar_charge'],p['baryon'],p['radiation'])))
    old_path=Path(__file__).resolve().parent.parent/'cosmological_bridge_2026/radiation_002/result.json'
    old=json.loads(old_path.read_text())['samples'][0]
    return dict(source=str(path),branches=branches,
                old_branch_conserved_ratios=ratios(old['scalar_charge'],old['rho_baryon'],old['rho_radiation']),
                condition_convention='Eigenvector condition of similarity-balanced operator: coordinate dependent sensitivity diagnostic, not rigorous interval eigenvalue error.',
                gamma0_scope='Both analytic formulas neglect explicit cubic principal terms; evaluated on the finite-gamma background only as approximate cross-checks, not substituted for its actual operator.',
                non_claims=['No UV completion follows from larger finite k','No continuation beyond logged bounds',
                            'No claim of exact kinetic nullity or physical DOF number'])


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args()
    result=diagnose(args.source)
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='branches'},indent=2))
    for branch in result['branches']:
        print(json.dumps(dict(direction=branch['direction'],initial=branch['initial'],
                              last=branch['rows'][-1]),indent=2))
