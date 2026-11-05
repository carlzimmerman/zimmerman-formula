#!/usr/bin/env python3
"""Frozen AZ45 population statistics; does not infer missing cube-fit outcomes."""
import math
import numpy as np
Z=np.array([.6,1.,1.4])
WEIGHTS=(Z-Z.mean())/np.sum((Z-Z.mean())**2)
def slope(means):
    """OLS with an intercept on three equally weighted bin means."""
    a=np.asarray(means,float)
    if a.shape[-1]!=3:raise ValueError('Three redshift thirds required')
    return np.sum(a*WEIGHTS,axis=-1)

def slope_variance(within_variances,per_third):
    if per_third<2:raise ValueError('Sample variance requires at least two per third')
    return np.sum(np.asarray(within_variances,float)*(WEIGHTS**2),axis=-1)/per_third

def resample(residuals,total,draws,seed):
    """Four templates per third, each equally represented; three saved replicates.

    Increasing draws preserves an identical RNG prefix. Returned variance is
    the within-third sampling estimate, before adding any trend floor.
    """
    a=np.asarray(residuals,float)
    if a.shape!=(3,4,3) or not np.all(np.isfinite(a)):
        raise ValueError('All36 finite recoveries are required, without imputation')
    if total not in [36,72,144,288,576,1152] or draws<1:
        raise ValueError('Outside the frozen population grid')
    rng=np.random.default_rng(np.random.SeedSequence(seed));per_template=total//12
    indices=rng.integers(0,3,size=(draws,3,4,per_template))
    selected=a[np.arange(3)[None,:,None,None],np.arange(4)[None,None,:,None],indices]
    samples=selected.reshape(draws,3,total//3)
    means=samples.mean(axis=2);variances=samples.var(axis=2,ddof=1)
    return slope(means),slope_variance(variances,total//3)

def detect(slopes,variances,floor):
    if floor not in [0,.10,.20]:raise ValueError('Outside the frozen systematic floors')
    return np.asarray(slopes)>3*np.sqrt(np.asarray(variances)+floor**2)

def wilson(successes,trials):
    if not 0<=successes<=trials or trials<1:raise ValueError('Invalid binomial counts')
    z=1.959963984540054;p=successes/trials;d=1+z*z/trials
    centre=(p+z*z/(2*trials))/d
    half=z*math.sqrt(p*(1-p)/trials+z*z/(4*trials*trials))/d
    return (0. if successes==0 else max(0.,centre-half),
            1. if successes==trials else min(1.,centre+half))

def rates(flat,rise,total,snr,foot_index,hi_index):
    """Both Monte Carlo rungs and all floors; calibration must be checked outside."""
    seed=[20261105,4500,snr,total,foot_index,hi_index]
    fs,fv=resample(flat,total,1024,seed);rs,rv=resample(rise,total,1024,seed)
    result=[]
    for floor in [0,.10,.20]:
        pair=[]
        for count in [512,1024]:
            f=int(detect(fs[:count],fv[:count],floor).sum())
            r=int(detect(rs[:count],rv[:count],floor).sum())
            fi=wilson(f,count);ri=wilson(r,count)
            pair.append(dict(resamples=count,false_positive=f/count,power=r/count,
                             false_positive_Wilson95=list(fi),power_Wilson95=list(ri),
                             power_gate=bool(ri[0]>=.80 and fi[1]<=.05)))
        converged=(abs(pair[0]['power']-pair[1]['power'])<=.03 and
                   abs(pair[0]['false_positive']-pair[1]['false_positive'])<=.03 and
                   pair[0]['power_gate']==pair[1]['power_gate'])
        result.append(dict(total=total,systematic_floor=floor,rungs=pair,converged=converged))
    return result
