"""Bounded microscopic/transport diagnostic; not a galaxy formation simulation."""
import argparse
import json
import numpy as np
from scipy.integrate import solve_ivp


def force_energy(x, mass, charge, h):
    delta = x[:, None, :] - x[None, :, :]
    r2 = np.sum(delta*delta, axis=2) + h*h
    np.fill_diagonal(r2, np.inf)
    coeff = charge[:, None]*charge[None, :] - mass[:, None]*mass[None, :]
    force = np.sum((coeff/r2**1.5)[:, :, None]*delta, axis=1)
    return force, .5*np.sum(coeff/np.sqrt(r2))


def initial(seed, spin, prepared, h, N=12):
    rng = np.random.default_rng(seed)
    eps, eta = .1, 5.364
    mass = np.repeat([1/N, eta/(N*(1+eps)), eps*eta/(N*(1+eps))], N)
    charge = np.repeat([0., mass[N], -mass[N]], N)
    x = rng.normal(size=(3*N, 3))*.6
    if prepared:
        x[2*N:] = x[N:2*N] + .08*rng.normal(size=(N, 3))
    x -= np.sum(mass[:, None]*x, axis=0)/sum(mass)
    v = rng.normal(size=x.shape)
    v -= np.sum(mass[:, None]*v, axis=0)/sum(mass)
    rot = np.column_stack((-x[:, 1], x[:, 0], np.zeros(3*N)))
    # Orthogonalize random component against rotation in the mass metric.
    v -= rot*np.sum(mass[:, None]*v*rot)/np.sum(mass[:, None]*rot*rot)
    v /= np.sqrt(np.sum(mass[:, None]*v*v))
    rot /= np.sqrt(np.sum(mass[:, None]*rot*rot))
    v = np.sqrt(1-spin)*v + np.sqrt(spin)*rot
    _, U = force_energy(x, mass, charge, h)
    v *= np.sqrt(.7*abs(U))
    return x, v, mass, charge


def diagnostics(x, v, mass, charge, h):
    N = len(mass)//3
    dr = x[N:2*N, None, :] - x[None, 2*N:, :]
    dist = np.linalg.norm(dr, axis=2)
    near = np.argmin(dist, axis=1)
    back = np.argmin(dist, axis=0)
    count = 0
    for i, j in enumerate(near):
        mu = mass[N+i]*mass[2*N+j]/(mass[N+i]+mass[2*N+j])
        energy = .5*mu*np.sum((v[N+i]-v[2*N+j])**2)
        energy += (charge[N+i]*charge[2*N+j]-mass[N+i]*mass[2*N+j])/np.sqrt(dist[i,j]**2+h*h)
        count += int(back[j] == i and energy < 0)
    center = np.average(x[:N], axis=0, weights=mass[:N])
    rad = np.linalg.norm(x-center, axis=1)
    inner = rad < 1
    cov = (x[:N]-center).T @ (x[:N]-center)/N
    eig = np.linalg.eigvalsh(cov)
    return dict(neutral_pair_fraction=count/N,
                inner_positive_count=int(sum(inner[N:2*N])),
                inner_negative_count=int(sum(inner[2*N:])),
                inner_dark_mass=float(np.sum(mass[N:]*inner[N:])),
                baryon_axis_ratio=float(np.sqrt(max(0,eig[0])/eig[-1])))


def run(seed, spin, prepared, h=.08, rtol=1e-8, duration=2.):
    x, v, mass, charge = initial(seed, spin, prepared, h)
    n = len(mass)
    def rhs(t, state):
        xx, vv = state[:3*n].reshape(n,3), state[3*n:].reshape(n,3)
        force, _ = force_energy(xx, mass, charge, h)
        return np.r_[vv.ravel(), (force/mass[:,None]).ravel()]
    sol = solve_ivp(rhs, (0,duration), np.r_[x.ravel(),v.ravel()], method='DOP853',
                    rtol=rtol, atol=rtol*.01, t_eval=np.linspace(0,duration,81))
    if not sol.success:
        raise RuntimeError(sol.message)
    energies, momenta, angular = [], [], []
    for state in sol.y.T:
        xx, vv = state[:3*n].reshape(n,3), state[3*n:].reshape(n,3)
        _, U = force_energy(xx,mass,charge,h)
        energies.append(.5*np.sum(mass[:,None]*vv*vv)+U)
        momenta.append(np.sum(mass[:,None]*vv,axis=0))
        angular.append(np.sum(mass[:,None]*np.cross(xx,vv),axis=0))
    E = np.array(energies)
    result = dict(seed=seed,spin=spin,prepared=prepared,softening=h,rtol=rtol,
                  duration=duration,particles=n,nfev=sol.nfev,
                  initial=diagnostics(x,v,mass,charge,h),
                  final=diagnostics(xx,vv,mass,charge,h),
                  max_relative_energy_drift=float(np.max(abs(E-E[0]))/abs(E[0]),
                  max_momentum_drift=float(np.max(np.linalg.norm(np.array(momenta)-momenta[0],axis=1))),
                  max_angular_momentum_drift=float(np.max(np.linalg.norm(np.array(angular)-angular[0],axis=1))))
    return result, sol.y[:,-1]


def checks():
    x,v,m,q=initial(41,.5,False,.08)
    F,U=force_energy(x,m,q,.08)
    step=1e-5
    numerical=np.zeros_like(F)
    for i in range(len(m)):
        for j in range(3):
            xp,xm=x.copy(),x.copy()
            xp[i,j]+=step; xm[i,j]-=step
            numerical[i,j]=-(force_energy(xp,m,q,.08)[1]-force_energy(xm,m,q,.08)[1])/(2*step)
    force_error=float(np.linalg.norm(F-numerical)/np.linalg.norm(F))
    assert force_error < 1e-7
    assert np.linalg.norm(F.sum(axis=0)) < 1e-12
    # Independent two-body circular orbit for the same softened Hamiltonian.
    m=np.ones(2);q=np.zeros(2);h=.08;r=1.
    omega=np.sqrt(2/(r*r+h*h)**1.5)
    state=np.array([-.5,0,0,.5,0,0,0,-omega*.5,0,0,omega*.5,0])
    def rhs(t,y):
        f,_=force_energy(y[:6].reshape(2,3),m,q,h)
        return np.r_[y[6:],f.ravel()]
    sol=solve_ivp(rhs,(0,2*np.pi/omega),state,method='DOP853',rtol=1e-11,atol=1e-13)
    orbit_error=float(np.linalg.norm(sol.y[:,-1]-state))
    assert orbit_error < 1e-8
    return dict(force_finite_difference_relative_error=force_error,
                circular_orbit_return_error=orbit_error)


def spectrum():
    ns=np.arange(2,201,dtype=float)
    delta=.5*(1-1/ns**2)
    f=np.exp(np.log(256/3)+5*np.log(ns)+(2*ns-4)*np.log(ns-1)-(2*ns+4)*np.log(ns+1))
    assert abs(f[0]-8192/19683)<1e-14
    m,eps,K=1.,.1,1.
    z=np.array([1.,-1/np.sqrt(eps)])
    rows=[]
    for k in [0.,1e-4,.01,.1,1.,np.pi]:
        off=-K*(1+np.exp(-1j*k))/np.sqrt(eps)
        D=np.array([[2*K,off],[off.conjugate(),2*K/eps]])
        eig,e=np.linalg.eigh(D)
        coupling=abs(z@e)**2
        rows.append(dict(k=float(k),omega=np.sqrt(np.maximum(eig,0)).tolist(),
                         dipole_numerator=coupling.tolist()))
    assert rows[0]['dipole_numerator'][0] < 1e-24
    assert abs(rows[0]['omega'][1]**2-22)<1e-12
    return dict(ground_gap_over_binding=float(delta[0]/.5),
                bound_oscillator_strength_sum_through_n200=float(sum(f)),
                lyman_alpha_oscillator_strength=float(f[0]),
                minimum_gap_with_nonzero_ground_dipole=float(delta[0]),
                chain_modes=rows)


def main(output):
    result=dict(checks=checks(),spectrum=spectrum(),runs=[],refinement=[])
    for seed in [17,29]:
        for spin in [0.,.5,.9]:
            for prepared in [False,True]:
                row,state=run(seed,spin,prepared)
                result['runs'].append(row)
    for h in [.04,.08,.16]:
        coarse,a=run(17,.9,False,h,1e-8)
        fine,b=run(17,.9,False,h,1e-10)
        result['refinement'].append(dict(coarse=coarse,fine=fine,
            final_state_relative_difference=float(np.linalg.norm(a-b)/np.linalg.norm(b))))
    # These are scale mappings only, not four independent integrations.
    G=4.30091e-6
    result['physical_scale_mappings']=[dict(Mb=M,b=b,acceleration_unit=G*M/b**2,
        dynamical_time_kpc_per_kms=np.sqrt(b**3/(G*M)))
        for M,b in [(3e5,.3),(1e8,1),(6e10,3),(1e14,300)]]
    with open(output,'w') as out: json.dump(result,out,indent=2,allow_nan=False)
    print(json.dumps(dict(runs=len(result['runs']),refinement_runs=6,
         max_energy_error=max(r['max_relative_energy_drift'] for r in result['runs']),
         checks=result['checks'])))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    main(p.parse_args().output)
