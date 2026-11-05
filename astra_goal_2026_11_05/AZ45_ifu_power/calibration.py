#!/usr/bin/env python3
"""AZ45 calibration gates; exact frozen tolerances, no imputation or fit pruning."""
import numpy as np
import population as P

def calibrate(noisy,noiseless,all_resolved):
    # noisy: rung, flat/rise/mutate, z third, template within third, replicate.
    # noiseless: rung, template, reference/double/plus.01/minus.01/plus.005/minus.005.
    n=np.asarray(noisy,float);l=np.asarray(noiseless,float)
    if n.shape!=(2,3,3,4,3) or l.shape!=(2,12,6):raise ValueError('Complete frozen cell required')
    if not np.all(np.isfinite(n)) or not np.all(np.isfinite(l)):raise ValueError('Finite fitted residuals required')
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    check('all_fits_resolved',all_resolved)
    check('noisy_delta_resolution',np.max(abs(n[0]-n[1]))<=.01,float(np.max(abs(n[0]-n[1]))))
    check('noiseless_delta_resolution',np.max(abs(l[0]-l[1]))<=.01,float(np.max(abs(l[0]-l[1]))))
    lever=l[:,:,1]-l[:,:,0]
    deriv1=(l[:,:,2]-l[:,:,3])/.02;deriv2=(l[:,:,4]-l[:,:,5])/.01
    check('local_lever_step_convergence',np.max(abs(deriv1-deriv2))<=.02,float(np.max(abs(deriv1-deriv2))))
    results=[];flags=[];slopes=[]
    for rung in range(2):
        means=n[rung].mean(axis=(2,3));medians=np.median(n[rung].reshape(3,3,12),axis=2)
        ss=P.slope(means);slopes.append(ss)
        correction=np.median((n[rung,2]-n[rung,0]-lever[rung].reshape(3,4,1)).reshape(3,12),axis=1)
        f=[*list(abs(medians[0])<=.07),bool(abs(ss[0])<=.10),bool(abs(ss[1]-.60)<=.10),
           *list(abs(correction)<=.07),bool(np.any(abs(medians[2])>.07))]
        flags.append(f)
        for third in range(3):
            check(f'r{rung+1}_flat_bias_z{third}',f[third],float(medians[0,third]))
            check(f'r{rung+1}_mutation_lever_z{third}',f[5+third],float(correction[third]))
        check(f'r{rung+1}_flat_slope',f[3],float(ss[0]))
        check(f'r{rung+1}_rise_slope',f[4],float(ss[1]))
        check(f'r{rung+1}_mutation_bites',f[8],medians[2].tolist())
        results.append(dict(rung=rung+1,bin_means=means.tolist(),bin_medians=medians.tolist(),slopes=ss.tolist(),
                            mutation_shift_minus_lever=correction.tolist(),double_levers=lever[rung].tolist(),
                            local_derivative_step01=deriv1[rung].tolist(),local_derivative_step005=deriv2[rung].tolist()))
    check('population_slope_resolution',np.max(abs(slopes[0]-slopes[1]))<=.02,float(np.max(abs(slopes[0]-slopes[1]))))
    check('recovery_gate_flags_unchanged',flags[0]==flags[1])
    return dict(passed=all(c['passed'] for c in checks),checks=checks,rungs=results)
