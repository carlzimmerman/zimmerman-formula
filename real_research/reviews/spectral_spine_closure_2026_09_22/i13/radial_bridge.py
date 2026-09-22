#!/usr/bin/env python3
"""Radial Rayleigh--Ritz benchmarks; no MESA data and no fitted PN factor.

Run: python3 radial_bridge.py --output results.json
G=rho_c=alpha=1, n=3 Pc=pi, c^2=pi/s. The rho convention is
energy-density/c^2 in the TOV equations; internal energy is not added.
Results use binary64, adaptive ODE integration and Gaussian quadrature.
They are numerical evidence, not interval-certified enclosures.
"""
import argparse
import json
from fractions import Fraction
import platform
from dataclasses import dataclass
from math import pi
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp, quad
from scipy.linalg import eigh
from numpy.polynomial.legendre import leggauss


@dataclass
class Polytrope:
    s: float
    radius: float
    mass: float
    solution: object

    @classmethod
    def solve(cls, s=0.0, rtol=2e-12, max_step=0.02):
        r0 = 1e-7
        central_slope = (1+s)*(1/3+s)
        def ode(r, y):
            theta, v = y
            t = max(theta, 0.0)
            dt = -(1+s*t)*(v+s*r**3*t**4)/(r*r*(1-8*s*v/r))
            return [dt, r*r*t**3]
        def surface(r, y):
            return y[0]
        surface.terminal = True
        surface.direction = -1
        solution = solve_ivp(ode, [r0, 20],
                             [1-central_slope*r0*r0/2, r0**3/3],
                             rtol=rtol, atol=rtol/100, max_step=max_step,
                             events=surface, dense_output=True)
        if not solution.success or len(solution.t_events[0]) != 1:
            raise RuntimeError('Failed to locate the stellar surface')
        radius = solution.t_events[0][0]
        mass = 4*pi*solution.y_events[0][0][1]
        return cls(s, radius, mass, solution)

    def profile(self, r):
        theta, v = self.solution.sol(np.asarray(r).reshape(-1)).reshape((2,) + np.asarray(r).shape)
        theta = np.maximum(theta, 0)
        p, rho, m = pi*theta**4, theta**3, 4*pi*v
        if self.s == 0:
            zero = np.zeros_like(r)
            return p, rho, m, zero, zero, zero, zero, zero
        invc2 = self.s/pi
        h = 1-2*m*invc2/r
        b = -.5*np.log(h)
        a = .5*np.log(1-2*self.mass*invc2/self.radius)-4*np.log1p(self.s*theta)
        ap = invc2*(m+4*pi*r**3*p*invc2)/(r*r*h)
        bp = invc2*(4*pi*r*r*rho-m/r)/ (r*h)
        return p, rho, m, a, b, ap, bp, np.full_like(r, invc2)

    @property
    def compactness(self):
        return 2*self.mass*self.s/(pi*self.radius)


def uniform_profile(r):
    p = (2*pi/3)*(1-r*r)
    rho = np.ones_like(r)
    m = 4*pi*r**3/3
    zero = np.zeros_like(r)
    return p, rho, m, zero, zero, zero, zero, zero


def assemble(profile, radius, gamma, cells=128, order=8, raw=False):
    """Continuous piecewise-linear eta=xi/r; natural surface condition.

    The derivative cross term is assembled symmetrically. Endpoints are
    never quadrature nodes. No artificial Dirichlet condition at the surface.
    'raw' independently assembles the unsubtracted GR variational form.
    """
    gx, gw = leggauss(order)
    edges = np.linspace(0, radius, cells+1)
    r = (edges[:-1,None]+edges[1:,None])/2 + np.diff(edges)[:,None]*gx/2
    weights = np.diff(edges)[:,None]*gw/2
    shape = np.array([(1-gx)/2, (1+gx)/2])
    deriv = np.stack([-1/np.diff(edges), 1/np.diff(edges)], axis=1)
    p, rho, m, a, b, ap, bp, invc2 = profile(r)
    g = np.broadcast_to(gamma(r) if callable(gamma) else gamma, r.shape)
    emetric = np.exp(a+b)
    inertia = np.exp(-a+3*b)*(rho+p*invc2)*r**4
    leading = emetric*g*p*r**4
    if raw:
        cross = emetric*g*p*r**3*(3-r*ap)
        # Hydrostatic P'=-(rho+P/c²)*(m+4 pi r³P/c²)/(r²h).
        gravity = (m+4*pi*r**3*p*invc2)/(r*r*(1-2*m*invc2/r))
        pp = -(rho+p*invc2)*gravity
        pressure_square_term = (rho+p*invc2)*gravity**2*invc2
        pot = emetric*(g*p*r*r*(3-r*ap)**2+4*pp*r**3
              +8*pi*np.exp(2*b)*p*(rho+p*invc2)*invc2*r**4
              -pressure_square_term*r**4)
    else:
        kernel = 3*g-4
        cross = emetric*p*r**3*(kernel-g*r*ap)
        # rho*c²*ap² rewritten without 0*infinity at the Newtonian face.
        gravity = (m+4*pi*r**3*p*invc2)/(r*r*(1-2*m*invc2/r))
        pot = emetric*(3*kernel*p*r*r-(6*g+2)*p*r**3*ap
              -2*p*r**3*bp+(g-1)*p*r**4*ap**2
              -rho*r**4*invc2*gravity**2)
    stiff = np.zeros((cells+1,cells+1))
    mass = np.zeros_like(stiff)
    for i in range(2):
        for j in range(2):
            ni,nj=shape[i][None,:],shape[j][None,:]
            di,dj=deriv[:,i,None],deriv[:,j,None]
            kij=np.sum(weights*(leading*di*dj+cross*(di*nj+ni*dj)+pot*ni*nj),axis=1)
            mij=np.sum(weights*inertia*ni*nj,axis=1)
            ii=np.arange(cells)+i; jj=np.arange(cells)+j
            stiff[ii,jj]+=kij;mass[ii,jj]+=mij
    return stiff,mass


def modes(profile, radius, gamma, cells):
    k,m = assemble(profile,radius,gamma,cells)
    val = float(eigh(k,m,subset_by_index=[0,0],eigvals_only=True)[0])
    ones=np.ones(cells+1)
    hom=float((ones@k@ones)/(ones@m@ones))
    return val,hom


def critical_gamma(poly,cells):
    k,m = assemble(poly.profile,poly.radius,4/3,cells)
    kplus,_ = assemble(poly.profile,poly.radius,4/3+1,cells)
    derivative=kplus-k
    shift = float(eigh(k,derivative,subset_by_index=[0,0],eigvals_only=True)[0])
    ones=np.ones(cells+1)
    trial=4/3-float(ones@k@ones)/float(ones@derivative@ones)
    return 4/3-shift,trial


def run():
    checks=[]
    def require(name,passed):
        checks.append({'name':name,'passed':bool(passed)})
        if not passed:
            raise AssertionError(name)
    # Analytic uniform-density fundamental eta=1 has exact omega²=K GM/R³.
    uniform=[]
    for gamma in [1.2,4/3,5/3]:
        value,trial=modes(uniform_profile,1,gamma,96)
        expected=(3*gamma-4)*4*pi/3
        uniform.append(dict(gamma=gamma,ritz=value,trial=trial,exact=expected))
        require('uniform exact mode gamma='+str(gamma),abs(value-expected)<2e-8)
        require('uniform exact trial gamma='+str(gamma),abs(trial-expected)<2e-10)
    # Exact rational coefficient after factoring out pi² in H and pi in W.
    uniform_H_over_pi2 = Fraction(128,315)+Fraction(96,315)+Fraction(80,315)
    uniform_pn = uniform_H_over_pi2/(18*Fraction(4,3)*Fraction(4,45))
    require("uniform exact PN coefficient 19/42",uniform_pn == Fraction(19,42))
    poly=Polytrope.solve()
    def scalar(r):
        p,rho,m,*_=poly.profile(np.asarray(r))
        return float(p),float(rho),float(m)
    w=quad(lambda r:scalar(r)[0]*r*r,0,poly.radius,epsabs=1e-10,epsrel=1e-11)[0]
    h=quad(lambda r:8*scalar(r)[0]*scalar(r)[2]*r
           +8*pi*scalar(r)[0]*scalar(r)[1]*r**4+scalar(r)[1]*scalar(r)[2]**2,
           0,poly.radius,epsabs=1e-10,epsrel=1e-11)[0]
    pn_coefficient=h*poly.radius/(18*poly.mass*w)
    require('Lane Emden radius',abs(poly.radius-6.896848619)<2e-8)
    require('Lane Emden mass moment',abs(poly.mass/(4*pi)-2.018235951)<2e-8)
    require('independent PN coefficient rounds to Saio 1.1245',abs(pn_coefficient-1.1245)<5e-5)
    newton=[]
    for cells in [32,64,128,256]:
        value,trial=modes(poly.profile,poly.radius,1.5,cells)
        newton.append(dict(cells=cells,ritz=value,trial=trial,
                           relative_trial_excess=trial/value-1))
    require('homologous trial strictly above n3 eigenvalue approximation',newton[-1]['trial']>1.01*newton[-1]['ritz'])
    require('nested Ritz spaces decrease eigenvalue',all(a['ritz']>=b['ritz']-1e-10 for a,b in zip(newton,newton[1:])))
    value,trial=modes(poly.profile,poly.radius,4/3,128)
    require('n3 radiation Newtonian zero mode',abs(value)<1e-9 and abs(trial)<1e-10)
    pn=[]
    for s in [1e-3,3e-4,1e-4,3e-5]:
        star=Polytrope.solve(s)
        critical,hom=critical_gamma(star,128)
        pn.append(dict(s=s,x=star.compactness,critical_gamma=critical,
                       trial_critical_gamma=hom,
                       onset_slope=(critical-4/3)/star.compactness,
                       trial_slope=(hom-4/3)/star.compactness))
    require('full GR weak field onset approaches PN coefficient',abs(pn[-1]['onset_slope']-pn_coefficient)<1e-3)
    # Positive homology trial together with a negative admissible Ritz trial.
    star=Polytrope.solve(.001)
    critical,hom=critical_gamma(star,256)
    gamma=(critical+hom)/2
    value,trial=modes(star.profile,star.radius,gamma,256)
    require('positive homology trial does not imply stability',trial>1e-7 and value<-1e-7)
    failure=dict(s=star.s,x=star.compactness,gamma=gamma,ritz=value,trial=trial,
                 critical_gamma_256=critical,trial_critical_gamma=hom)
    kr,mr=assemble(star.profile,star.radius,gamma,128,raw=True)
    ks,ms=assemble(star.profile,star.radius,gamma,128,raw=False)
    raw_difference=float(np.max(np.abs(kr-ks)))
    require('unsubtracted and stabilized GR forms agree',raw_difference<2e-7)
    refinement=[]
    for cells in [64,128,256]:
        c,t=critical_gamma(star,cells)
        refinement.append(dict(cells=cells,critical_gamma=c,trial_critical_gamma=t))
    require('critical gamma grid refinement',abs(refinement[-1]['critical_gamma']-refinement[-2]['critical_gamma'])<2e-8)
    return dict(status='PASS',arithmetic='IEEE754 binary64; not rigorous interval bounds',
                software=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
                checks=checks,uniform=uniform,newtonian_n3=newton,
                uniform_exact_pn_coefficient=str(uniform_pn),
                lane_emden=dict(radius=poly.radius,mass_moment=poly.mass/(4*pi)),
                pn_integrals=dict(Wgr=w,H=h,delta_gamma_per_compactness=pn_coefficient,
                                  I13_Cgr=3*pn_coefficient),
                weak_field=pn,positive_trial_counterexample=failure,
                critical_refinement=refinement,raw_form_max_matrix_difference=raw_difference)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
