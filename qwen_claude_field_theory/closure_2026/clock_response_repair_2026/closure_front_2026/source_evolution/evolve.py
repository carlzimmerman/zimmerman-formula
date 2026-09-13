#!/usr/bin/env python3
"""Finite-time conserved linear response of the UNCHANGED reconstructed action.

M2=1 units. The signed, zero-background-density probe is not a galaxy.
No fitted response law, background replacement, or assigned slip parameter.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
CONSTITUTIVE = HERE.parents[1]/'nonlinear_evolution_2026/constitutive.py'
spec = importlib.util.spec_from_file_location('frozen_constitutive', CONSTITUTIVE)
constitutive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(constitutive)
Model = constitutive.Model


def coefficients(model, t, k, amplitude):
    if k <= 0 or not np.isfinite(k):
        raise ValueError('this reduction requires finite k>0; k=0 has a different shift constraint')
    b = model.background(float(t))
    a, q, H = (b[x] for x in ('a', 'q', 'H'))
    j = model.jets(float(t), q*q, 0.)
    gamma = model.gamma
    r = k*k/(a*a)
    rho = amplitude/a**3
    Theta = H+gamma*q**3
    Sigma = q*q*j['P_X']+2*q**4*j['P_XX']-3*H*H-12*gamma*H*q**3
    W = j['W']
    C = W-2*q*q*j['W_Y']
    D = j['P_t']-j['V_t']-2*q*q*j['P_Xt']
    E = j['P_tt']-j['V_tt']-3*H*j['W_t']
    if Theta == 0:
        raise ValueError('singular lapse/shift block')
    J = (Sigma*W+D*Theta)/Theta**2
    R = W/Theta
    f = rho*W/(2*Theta)
    den = C*r-E-D*W/Theta-Sigma*W*W/(2*Theta**2)
    if den == 0:
        raise ValueError('singular clock block; no divided evolution is valid')
    K0 = 6+2*Sigma/Theta**2
    A = K0+J*J/den
    B = 2*r/Theta+J*R*r/den
    Ce = 2*r+R*R*r*r/den
    F = -rho/Theta-J*f/den
    S = -R*r*f/den
    if A == 0:
        raise ValueError('singular effective kinetic block')
    result = dict(a=a,q=q,H=H,r=r,rho=rho,Theta=Theta,Sigma=Sigma,W=W,C=C,D=D,E=E,
                  J=J,R=R,f=f,den=den,K0=K0,A=A,B=B,Ce=Ce,F=F,S=S)
    if not all(np.isfinite(x) for x in result.values()):
        raise FloatingPointError('nonfinite action coefficient')
    return result


def rhs(t, state, model, k, amplitude):
    c = coefficients(model, t, k, amplitude)
    z, p = state
    v = (p/c['a']**3-c['B']*z-c['F'])/c['A']
    pd = c['a']**3*(c['B']*v+c['Ce']*z+c['S'])
    return np.array([v, pd])


def initial_state(model, k, amplitude, z=0., zdot=0.):
    c = coefficients(model, 0., k, amplitude)
    return np.array([z, c['a']**3*(c['A']*zdot+c['B']*z+c['F'])])


def fields(t, state, model, k, amplitude):
    c = coefficients(model, t, k, amplitude)
    z, p = state
    v, pdot = rhs(t, state, model, k, amplitude)
    sigma = (c['J']*v+c['R']*c['r']*z-c['f'])/c['den']
    n = (v+c['W']*sigma/2)/c['Theta']
    lap = (3*c['Theta']*v+c['Sigma']*n+c['r']*z+c['D']*sigma/2-c['rho']/2)/c['Theta']
    # Momentum from the original, uneliminated action: p=2*a^3*LapB.
    # Its relation to the lapse reconstruction is checked, not imposed there.
    u = -lap/c['r']
    udot = -pdot/(2*c['a']**3*c['r'])+c['H']*p/(2*c['a']**3*c['r'])
    Phi = n+udot
    Psi = -z-c['H']*u
    return dict(n=n,sigma=sigma,LapB=lap,u=u,udot=udot,Phi=Phi,Psi=Psi,zdot=v,pdot=pdot)


def integrate(model, k, amplitude, method='DOP853', rtol=1e-10, max_step=np.inf,
              initial=None):
    y0 = initial_state(model, k, amplitude) if initial is None else np.asarray(initial)
    scale = max(abs(amplitude), float(np.max(np.abs(y0))), 1e-30)
    sol = solve_ivp(lambda t,y: rhs(t,y,model,k,amplitude), (0., model.tmax), y0,
                    method=method, rtol=rtol, atol=rtol*scale*1e-3,
                    dense_output=True, max_step=max_step,
                    first_step=min(model.tmax/100, 1e-4, max_step))
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def shifted_coefficients(model, t, k, amplitude):
    """Subtract d[a^3(h*z^2/2+g*z)]/dt; retain its time derivatives."""
    c = coefficients(model,t,k,amplitude)
    b = model.background(float(t))
    td = b['Hdot']+3*model.gamma*c['q']**2*b['qdot']
    theta = c['Theta']
    bt = c['J']*c['R']*c['r']/c['den']
    ft = -c['J']*c['f']/c['den']
    ct = 2*c['r']*((theta-c['H'])/theta+td/theta**2)+c['R']**2*c['r']**2/c['den']
    st = c['S']-c['rho']*td/theta**2
    return c,bt,ft,ct,st


def integrate_shifted(model, k, amplitude, method='DOP853', rtol=1e-10, max_step=np.inf):
    """Integrate well-conditioned momentum w and return ORIGINAL canonical (z,p).

    h=2r/Theta, g=-rho/Theta, w=p-a^3(h*z+g). This changes no field equation.
    The physical source density always remains amplitude/a^3.
    """
    def flow(t,state):
        c,bt,ft,ct,st=shifted_coefficients(model,t,k,amplitude)
        z,w=state
        v=(w/c['a']**3-bt*z-ft)/c['A']
        return np.array([v,c['a']**3*(bt*v+ct*z+st)])
    c,bt,ft,ct,st=shifted_coefficients(model,0.,k,amplitude)
    initial=[0.,c['a']**3*ft]
    sol=solve_ivp(flow,(0.,model.tmax),initial,method=method,rtol=rtol,
                  atol=rtol*max(abs(amplitude),1e-30)*1e-3,dense_output=True,
                  first_step=min(model.tmax/100,1e-4,max_step),max_step=max_step)
    if not sol.success:
        raise RuntimeError(sol.message)
    shifted_dense=sol.sol
    def reconstruct(t):
        if np.ndim(t):
            return np.array([reconstruct(float(tt)) for tt in t]).T
        z,w=shifted_dense(t)
        c=coefficients(model,t,k,amplitude)
        p=w+c['a']**3*(2*c['r']*z/c['Theta']-c['rho']/c['Theta'])
        return np.array([z,p])
    sol.sol=reconstruct
    sol.y=reconstruct(sol.t)
    return sol


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tmax', type=float, default=4.)
    parser.add_argument('--k', type=float, nargs='+', default=[.3,1.,3.,10.,30.,100.])
    parser.add_argument('--gamma', type=float, default=1e-6)
    parser.add_argument('--amplitude', type=float, default=1e-7)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    model = Model(args.tmax, args.gamma)
    rows=[]
    for k in args.k:
        sol = integrate_shifted(model,k,args.amplitude)
        vals=[]
        for t in np.linspace(0.,args.tmax,17):
            c=coefficients(model,t,k,args.amplitude)
            f=fields(t,sol.sol(t),model,k,args.amplitude)
            vals.append(dict(t=float(t),a=float(c['a']),zeta=float(sol.sol(t)[0]),
                             Phi=float(f['Phi']),Psi=float(f['Psi']),
                             response=-2*c['r']*f['Phi']/c['rho'],
                             A=float(c['A']),den=float(c['den'])))
        rows.append(dict(k=k,nfev=sol.nfev,samples=vals))
    result=dict(scope='Finite-time signed dust probe; fixed action and constrained zero-dynamical IC',
                theory_status='OPEN',gamma=args.gamma,amplitude=args.amplitude,rows=rows)
    payload=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload,end='')


if __name__ == '__main__':
    main()
