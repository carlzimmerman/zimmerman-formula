#!/usr/bin/env python3
"""Same IC17 action with conserved comoving dust; bounded clock/background probe."""
import argparse
import json
import mpmath as mp
import ic17_pole_clock as action


def raw(S,w,b,epsilon=action.EPSILON):
    S,w,b,epsilon=map(mp.mpf,(S,w,b,epsilon))
    return action.build()['evaluate'](S,w,epsilon)[0]-b*mp.exp(w)


def _coordinate(S,tau):
    u=mp.sqrt(-mp.expm1(-tau))
    a=mp.exp(-tau)/(1+u)
    w=-S*a/(1+a)
    if not 0<(S+2*w)/(S+w)<1:
        raise ValueError('Direct constitutive evaluator cannot resolve this chart point; increase precision')
    return u,w


def root(S,k,epsilon):
    evaluate=action.build()['evaluate']
    def equation(tau):
        _,w=_coordinate(S,tau)
        P,Pw,PS,B,C,PSS=evaluate(S,w,epsilon)
        return Pw+k*mp.exp(w+S)*PS
    lo,hi=mp.mpf('1e-20'),mp.mpf(1)
    if equation(lo)>=0:
        raise ValueError('Lower bracket does not select the stated dust branch')
    for _ in range(32):
        if equation(hi)>0:
            break
        hi*=2
    else:
        raise ValueError('No upper dust-root bracket located within the bounded search')
    tau=mp.findroot(equation,(lo,hi),solver='bisect',
                    tol=mp.power(10,-mp.mp.dps+12),maxsteps=5*mp.mp.dps)
    return (tau,)+_coordinate(S,tau)


def state(S,k='.2',epsilon=action.EPSILON):
    S,k,epsilon=map(mp.mpf,(S,k,epsilon))
    if S<=0 or k<0 or epsilon<=0:
        raise ValueError('Require S>0, k>=0, epsilon>0')
    tau,u,w=root(S,k,epsilon)
    P,Pw,PS,B,C,PSS=action.build()['evaluate'](S,w,epsilon)
    X=mp.exp(-2*S)/2
    charge=-PS*mp.exp(S)
    b=k*charge
    if charge<=0:
        raise ValueError('Root has nonpositive clock charge and does not realize the requested dust data')
    dust_source=b*mp.exp(w)
    Lww=B-dust_source
    Qbare=(PSS+PS)/(2*X)
    Q=(PSS+PS-C*C/Lww)/(2*X)
    FX=-PS/(2*X)
    Acan=Lww-C*C/(PSS+PS)
    bracket=mp.matrix([[0,Acan],[-Acan,0]])
    singular=list(mp.svd(bracket,compute_uv=False))
    rank=sum(value>mp.mpf('1e-45') for value in singular)
    rho=-PS-P+dust_source
    H=mp.sqrt(rho/(3*mp.exp(-mp.mpf(1)/6))) if rho>0 else mp.nan
    flow_matrix=mp.matrix([[PSS+PS,C],[C,Lww]])
    Sdot,wdot=flow_matrix**-1*mp.matrix([-3*H*PS,-3*H*dust_source])
    bdot=-3*H*b
    charge_dot=-mp.exp(S)*((PSS+PS)*Sdot+C*wdot)
    physical_H=mp.exp(-w)*(H+wdot)
    r=mp.exp(S-2*w-mp.mpf(1)/6)*H
    GS=C+k*mp.exp(w+S)*(PSS+PS)
    Gw=B+k*mp.exp(w+S)*(C+PS)
    wS=-GS/Gw
    healthy=bool(FX>0 and Q>=FX and Qbare>0 and Acan!=0 and rho>0 and physical_H>0)
    return dict(S=S,k=k,epsilon=epsilon,tau=tau,u=u,w=w,X=X,P=P,PS=PS,
                b=b,clock_charge_density=charge,constraint=Pw-dust_source,
                Lww=Lww,FX=FX,Qbare=Qbare,Q=Q,clock_speed_squared=FX/Q,
                auxiliary_schur=Acan,auxiliary_bracket=bracket,
                auxiliary_singular_values=singular,computed_auxiliary_rank=rank,
                canonical_identity_residual=Acan-Lww*Q/Qbare,
                clock_energy=-PS-P,dust_energy=dust_source,energy=rho,
                H=H,physical_H=physical_H,activation_r=r,eta=action.eta_up(r),
                Sdot=Sdot,wdot=wdot,bdot=bdot,wS=wS,charge_path_Gw=Gw,
                clock_charge_flow_residual=charge_dot+3*H*charge,
                auxiliary_flow_residual=C*Sdot+Lww*wdot-mp.exp(w)*bdot,
                friedmann_residual=3*mp.exp(-mp.mpf(1)/6)*H*H-rho,
                healthy_clock_probe=healthy,full_dust_characteristics_checked=False)


def report(samples=51):
    if samples<2:
        raise ValueError('Require at least two samples')
    mp.mp.dps=70
    rows=[state(mp.exp(mp.log(mp.mpf('1e-8'))+
                      (mp.log(mp.mpf('.1'))-mp.log(mp.mpf('1e-8')))*i/(samples-1)))
          for i in range(samples)]
    fields=('S','tau','u','w','b','clock_charge_density','constraint','Lww','FX','Qbare','Q',
            'clock_speed_squared','auxiliary_schur','computed_auxiliary_rank','physical_H',
            'activation_r','eta','Sdot','wdot','wS','charge_path_Gw','healthy_clock_probe')
    compact=lambda bg:{k:bg[k] for k in fields}
    return dict(candidate='IC17 same-action conserved pressureless baryon background',
                full_theory='OPEN',k='.2',epsilon=action.EPSILON,
                requested_witnesses=[compact(state(S)) for S in ('.1','.01','1e-4','1e-8')],
                scan=dict(samples=samples,S_min='1e-8',S_max='.1',interval_certified=False,
                          unhealthy_clock_probes=sum(not r['healthy_clock_probe'] or r['eta']!=1 for r in rows),
                          minimum_FX=min(r['FX'] for r in rows),minimum_Q=min(r['Q'] for r in rows),
                          minimum_auxiliary_schur=min(r['auxiliary_schur'] for r in rows),
                          minimum_charge_path_Gw=min(r['charge_path_Gw'] for r in rows),
                          minimum_physical_H=min(r['physical_H'] for r in rows),
                          maximum_constraint_residual=max(abs(r['constraint']) for r in rows),
                          maximum_relative_charge_flow_residual=max(abs(r['clock_charge_flow_residual'])/(1+r['H']*r['clock_charge_density']) for r in rows),
                          maximum_relative_auxiliary_flow_residual=max(abs(r['auxiliary_flow_residual'])/(1+r['H']*r['b']) for r in rows),
                          computed_auxiliary_ranks=sorted(set(r['computed_auxiliary_rank'] for r in rows)),
                          rows=list(map(compact,rows))),
                nonclaims=['Clock probe excludes dust density and velocity perturbations',
                           'No radiation, recombination, CMB fit, or complete cosmological history',
                           'Finite direct constitutive evaluation stops before the unresolved u=1 precision boundary',
                           'No continuous interval certificate, strong-coupling, sourced MOND, or full transition certificate'])


def completion_status(result,require_full_closure=False):
    scan=result['scan']
    if (scan['unhealthy_clock_probes'] or
            scan['maximum_constraint_residual']>=mp.mpf('1e-35') or
            scan['maximum_relative_charge_flow_residual']>=mp.mpf('1e-50') or
            scan['maximum_relative_auxiliary_flow_residual']>=mp.mpf('1e-50')):
        return 1
    return 2 if require_full_closure else 0


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args(argv)
    result=report()
    print(json.dumps(result,indent=2,default=lambda value:mp.nstr(value,30)))
    return completion_status(result,args.require_full_closure)


if __name__=='__main__':
    raise SystemExit(main())
