#!/usr/bin/env python3
"""Independent high-precision midpoint-exponential propagator.

Same IC25 charge-profile action and interpolated background; different time
integration and arithmetic. Resolves determinant conditioning, not the theory.
"""
import argparse
import json
import mpmath as mp
import ic25_coupled as base


def propagate(history,k2_initial=100,steps=160,dps=60):
    with mp.workdps(dps):
        end=mp.mpf(history['Q_end']);step=end/steps
        first=base.completed_at(history,0);last=base.completed_at(history,end)
        q0=base.prior.quadratic(first,k2_initial);R=mp.cholesky(q0['A']).T
        n=R.rows;dim=2*n;di=mp.diag([mp.mpf('.5')]+[1]*(n-1));zero=mp.zeros(n)
        def convert(row,k):
            q=base.prior.quadratic(row,k);T=mp.zeros(dim)
            X=R*2*di*q['L']/first['Qdot'];P=R*2*di*q['K']/first['Qdot']
            for i in range(n):
                for j in range(n):T[i,j]=R[i,j];T[i+n,j]=X[i,j];T[i+n,j+n]=P[i,j]
            return T
        T0=convert(first,k2_initial);Tend=convert(last,mp.mpf(k2_initial)*mp.exp(-2*end))
        F=mp.eye(dim)
        for j in range(steps):
            Q=(j+mp.mpf('.5'))*step;row=base.completed_at(history,Q)
            G=base.hamiltonian_generator(row,mp.mpf(k2_initial)*mp.exp(-2*Q))/row['Qdot']
            F=mp.expm(G*step)*F
        actual=mp.det(F);prediction=mp.exp(-3*n*end)
        transfer=Tend*F*(T0**-1);sv=list(mp.svd(transfer,compute_uv=False))
        return dict(steps=steps,dps=dps,Q_end=end,k2_initial=k2_initial,singular_values=sv,
            determinant=actual,volume_prediction=prediction,relative_volume_error=abs(actual/prediction-1),
            weighted_transfer=transfer.tolist(),norm='Same initial kinetic norm as IC25; Cholesky and symmetric square roots differ by an orthogonal map')


def report():
    h=base.evolve(1,max_step=.005,rtol=1e-12,profile='charge')
    coarse=propagate(h,100,160);fine=propagate(h,100,320)
    with mp.workdps(60):
        relative=abs(coarse['singular_values'][0]/fine['singular_values'][0]-1)
        checks=dict(volume_restored=fine['relative_volume_error']<mp.mpf('1e-30'),
                    amplification_step_agreement=relative<mp.mpf('.02'))
    return dict(full_theory='OPEN',checks=checks,coarse=coarse,fine=fine,
        relative_largest_amplification_difference=relative,
        nonclaims=['Finite-time amplification in a stated norm; not a universal nonlinear instability proof',
          'Background remains a double-precision interpolated trajectory',
          'A successful numerical cross-check does NOT repair the large growth'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--require-full-closure',action='store_true');args=p.parse_args()
    out=report();print(json.dumps(out,default=base.prior.serial,indent=2))
    raise SystemExit(1 if not all(out['checks'].values()) else 2 if args.require_full_closure else 0)
