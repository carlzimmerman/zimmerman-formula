#!/usr/bin/env python3
"""Explicit shear-without-vorticity witness; no observational remeasurement."""
import argparse,json,math
from pathlib import Path
import numpy as np
import audit_inputs as A

def velocity(position,alpha):
    x,y,z=np.asarray(position,float)
    return np.array([alpha*z,0.,x])

def gradient(position,alpha,h):
    basis=np.eye(3)
    return np.column_stack([(velocity(np.asarray(position)+h*e,alpha)-velocity(np.asarray(position)-h*e,alpha))/(2*h) for e in basis])

def curl_from_gradient(grad):return np.array([grad[2,1]-grad[1,2],grad[0,2]-grad[2,0],grad[1,0]-grad[0,1]])
def angular_rate(grad,mutate=False):
    return float(np.linalg.norm(grad)/math.sqrt(2)) if mutate else float(np.linalg.norm(curl_from_gradient(grad))/2)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mutate',action='store_true');args=parser.parse_args();checks=[];witnesses=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    positions=[np.array(p,float) for p in [[0,0,0],[17,-11,4],[-13,8,-9]]]
    sky=[np.array([x,0.,0.]) for x in [-30,-10,0,10,30]]
    polygon=[np.array(p,float) for p in [[-1,0,-1],[1,0,-1],[1,0,1],[-1,0,1],[-1,0,-1]]]
    for alpha in [-1.,1.,3.]:
        exact=np.array([[0.,0.,alpha],[0.,0.,0.],[1.,0.,0.]])
        analytic_curl=np.array([0.,alpha-1.,0.]);rates=[];grads=[]
        for h in [1.,.5]:
            rung=[gradient(position,alpha,h) for position in positions];error=max(float(np.max(abs(g-exact))) for g in rung)
            check('gradient_'+str(alpha)+'_'+str(h),error<=1e-12,error)
            rates.append([angular_rate(g,args.mutate) for g in rung]);grads.append(rung)
        check('rung_pair_'+str(alpha),np.max(abs(np.array(rates[0])-rates[1]))<=1e-12)
        check('curl_components_'+str(alpha),np.max(abs(curl_from_gradient(exact)-analytic_curl))<=1e-12)
        circulation=sum(float(np.dot(.5*(velocity(p,alpha)+velocity(q,alpha)),q-p)) for p,q in zip(polygon,polygon[1:]))
        check('oriented_circulation_'+str(alpha),abs(circulation-4*(1-alpha))<=1e-12,circulation)
        projected=[velocity(p,alpha).tolist() for p in sky]
        check('same_observed_map_'+str(alpha),projected==[velocity(p,1.).tolist() for p in sky])
        witnesses.append(dict(alpha=alpha,gradient=exact.tolist(),antisymmetric=(.5*(exact-exact.T)).tolist(),
            symmetric=(.5*(exact+exact.T)).tolist(),analytic_curl=analytic_curl.tolist(),inferred_angular_rate_over_gamma=angular_rate(exact,args.mutate),
            analytic_angular_rate_over_gamma=abs(alpha-1)/2,projected_velocity=projected,rung_rates=rates,circulation=circulation))
    strain=witnesses[1];rigid=witnesses[0]
    check('rigid_rotation_known_answer',abs(rigid['inferred_angular_rate_over_gamma']-1)<=1e-12)
    check('pure_strain_zero_vorticity',strain['inferred_angular_rate_over_gamma']<=1e-12)
    counterexample=any(w['gradient'][2][0]!=0 and w['inferred_angular_rate_over_gamma']==0 for w in witnesses)
    check('known_counterexample_recognized',counterexample)
    # Conditional evaluation of the OLD illustrative numbers; not new data.
    gamma=150e3/(60*3.0856775814913673e19);c=299792458.;feet={}
    for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
        rows=[]
        for multiplier in [1,2,4]:
            scale=multiplier*a0/c
            old=-(.5*gamma/scale)**2
            witness_logs=[-(w['inferred_angular_rate_over_gamma']*gamma/scale)**2 for w in witnesses]
            rows.append(dict(multiplier=multiplier,omega_star_s_inv=scale,old_assumed_logF=old,
                witness_logF=witness_logs,witness_active=[x>=math.log(.5) for x in witness_logs]))
        check(foot+'_irrotational_F_one',all(row['witness_logF'][1]==0 for row in rows))
        feet[foot]=dict(a0=a0,rows=rows,scope='Conditional transfer only; no actual cluster vorticity inferred')
    valid=all(x['passed'] for x in checks)
    obj=dict(label='FAIL: projected gradient alone does not imply a positive vorticity floor' if valid and counterexample else 'UNDECIDED: audit controls failed',
        mutate=args.mutate,checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),witnesses=witnesses,
        footings=feet,gamma_s_inv=gamma,source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),A.HERE/'FROZEN_KINEMATICS.md',A.ROOT/'rebuild_2026_10_22/FA1_fresh_action/I2_vorticity/FROZEN_CRITERIA.md']},
        scope='Kinematic implication audit; does not determine actual cluster flow, rescue I2, or change original FA1 records; retired sector, adopts nothing; kappa=1/2 FITTED; not theory closed')
    A.atomic(A.HERE/('mutate/kinematics.json' if args.mutate else 'kinematics.json'),obj)
    print(json.dumps(dict(label=obj['label'],passed=obj['passed'],total=obj['total'],failed=[x['name'] for x in checks if not x['passed']]),indent=2))
    return int(not valid)
if __name__=='__main__':raise SystemExit(main())
