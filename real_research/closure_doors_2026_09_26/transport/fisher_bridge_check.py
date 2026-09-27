#!/usr/bin/env python3
"""Local same-pair Fisher/Madelung bridge and exact two-mode propagation.

The bridge is asserted only on rho>0. Exact free waves test U=0, not the full
bounded-DBI nonlinear wave equation. At nodes, wave regularity does not imply
a regular globally defined clock. No quantum-particle ontology is assumed.
"""
import argparse
import json
import math
import pathlib
import platform
import time

import numpy as np
import sympy as s


def symbolic_checks():
    rho, D = s.symbols("rho D", positive=True)
    phi, rx, px, rt, pt = s.symbols("phi rho_x phi_x rho_t phi_t", real=True)
    q = s.sqrt(rho) * s.cos(phi / D)
    p = s.sqrt(rho) * s.sin(phi / D)
    qt = s.diff(q, rho) * rt + s.diff(q, phi) * pt
    pp_t = s.diff(p, rho) * rt + s.diff(p, phi) * pt
    qx = s.diff(q, rho) * rx + s.diff(q, phi) * px
    pp_x = s.diff(p, rho) * rx + s.diff(p, phi) * px
    canonical = s.trigsimp(D * (p * qt - q * pp_t))
    assert s.simplify(canonical + rho * pt) == 0
    gradient = s.trigsimp(D**2 * (qx**2 + pp_x**2) / 2)
    assert s.simplify(gradient - rho * px**2 / 2 - D**2 * rx**2 / (8 * rho)) == 0
    jac = s.trigsimp(s.diff(q, rho) * s.diff(p, phi) - s.diff(q, phi) * s.diff(p, rho))
    assert s.simplify(jac - 1 / (2 * D)) == 0
    A, B, k, x, t = s.symbols("A B k x t", real=True)
    # Common time phase cancels in rho, j and spatial kinetic energy.
    qr = (A + B) * s.cos(k * x)
    pr = (A - B) * s.sin(k * x)
    density = s.trigsimp(qr**2 + pr**2)
    density_formula = A**2 + B**2 + 2 * A * B * s.cos(2*k*x)
    assert s.trigsimp(s.expand_trig(density - density_formula)) == 0
    current = s.trigsimp(D * (qr * s.diff(pr,x) - pr * s.diff(qr,x)))
    assert s.simplify(current - D*k*(A**2-B**2)) == 0
    kinetic = s.trigsimp(D**2*(s.diff(qr,x)**2+s.diff(pr,x)**2)/2)
    kinetic_formula = D**2*k**2*(A**2+B**2-2*A*B*s.cos(2*k*x))/2
    assert s.trigsimp(s.expand_trig(kinetic-kinetic_formula)) == 0
    # At destructive interference and A>B: velocity blows up as B increases to A.
    assert s.factor(D*k*(A**2-B**2)/(A-B)**2 - D*k*(A+B)/(A-B)) == 0
    wave = s.exp(-s.I*D*k**2*t/2)*(A*s.exp(s.I*k*x)+B*s.exp(-s.I*k*x))
    assert s.simplify(s.I*D*s.diff(wave,t)+D**2*s.diff(wave,x,2)/2) == 0
    omega = D*k**2/2
    assert s.diff(omega,k) == D*k
    return dict(count=9,canonical_term=str(canonical),gradient_energy=str(gradient),
                canonical_chart_jacobian=str(jac),density=str(density_formula),
                current=str(current),kinetic_density=str(kinetic_formula),
                free_wave_PDE="iD Psi_t=-(D^2/2) Psi_xx",group_speed="D*k (unbounded as k increases)")


def spectral_case(N,A,B,k,D):
    L=2*np.pi;dx=L/N;x=np.arange(N)*dx;wave_numbers=np.fft.fftfreq(N,d=dx)*2*np.pi
    initial=A*np.exp(1j*k*x)+B*np.exp(-1j*k*x)
    initial_f=np.fft.fft(initial)
    mass_exact=L*(A*A+B*B)
    energy_exact=L*D*D*k*k*(A*A+B*B)/2
    max_wave_error=max_mass_error=max_energy_error=max_fisher_error=0.
    rho_min=float('inf')
    for t in (0.,.125,1.234):
        psi=np.fft.ifft(initial_f*np.exp(-.5j*D*wave_numbers**2*t))
        exact=initial*np.exp(-.5j*D*k*k*t)
        grad=np.fft.ifft(1j*wave_numbers*np.fft.fft(psi))
        rho=abs(psi)**2
        rho_min=min(rho_min,float(rho.min()))
        current=D*np.imag(np.conj(psi)*grad)
        rho_x=2*np.real(np.conj(psi)*grad)
        energy_density=.5*D*D*abs(grad)**2
        mask=rho>1e-20
        fisher=.5*current[mask]**2/rho[mask]+D*D*rho_x[mask]**2/(8*rho[mask])
        max_fisher_error=max(max_fisher_error,float(np.max(abs(fisher-energy_density[mask]))))
        max_wave_error=max(max_wave_error,float(np.max(abs(psi-exact))))
        max_mass_error=max(max_mass_error,abs(float(dx*np.sum(rho))/mass_exact-1))
        max_energy_error=max(max_energy_error,abs(float(dx*np.sum(energy_density))/energy_exact-1))
    finite_diff_grad=(np.roll(initial,-1)-np.roll(initial,1))/(2*dx)
    fd_energy=float(.5*D*D*dx*np.sum(abs(finite_diff_grad)**2))
    return dict(N=N,A=A,B=B,k=k,D=D,times=[0,.125,1.234],
                maximum_wave_linf=max_wave_error,mass_relative_error=max_mass_error,
                energy_relative_error=max_energy_error,positive_chart_energy_identity_linf=max_fisher_error,
                minimum_sampled_density=rho_min,exact_minimum_density=(A-B)**2,
                finite_difference_energy_relative_error=abs(fd_energy/energy_exact-1),
                phase_chart_valid_everywhere=A!=B,
                exact_node_example="x=pi/(2k); every time" if A==B else None)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    start=time.monotonic();symbolic=symbolic_checks()
    rows=[spectral_case(N,1.,B,3.,.2) for B in (.6,1.) for N in (96,192,384,768)]
    assert max(r['maximum_wave_linf'] for r in rows)<1e-12
    assert max(r['mass_relative_error'] for r in rows)<1e-12
    assert max(r['energy_relative_error'] for r in rows)<1e-12
    assert max(r['positive_chart_energy_identity_linf'] for r in rows)<1e-11
    orders=[]
    for B in (.6,1.):
        group=[r for r in rows if r['B']==B]
        o=[math.log(group[i]['finite_difference_energy_relative_error']/group[i+1]['finite_difference_energy_relative_error'],2) for i in range(3)]
        assert min(o)>1.97
        orders.append(dict(B=B,orders=o))
    contrast=[dict(B=B,minimum_density=(1-B)**2,
                   maximum_phase_velocity=.2*3*(1+B)/(1-B)) for B in (.6,.9,.99,.999)]
    out=dict(result="Local canonical bridge verified; exact free-wave crossing state is regular while equal-amplitude phase has nodes",
             symbolic=symbolic,exact_two_mode_cases=rows,finite_difference_energy_orders=orders,
             approaching_equal_amplitude=contrast,
             clock_condition="With a fixed added clock rate Q0, timelikeness must be checked separately against phase gradients; maximum velocity diverges as B approaches A",
             topology="On a periodic spatial circle, node-free A>B states also have phase winding k; a periodic real clock needs a separate global lift. On the line the phase lift exists locally away from nodes.",
             non_claims=["Free exact solution uses U=0 and does not verify nonlinear DBI-wave scattering", "Canonical equivalence is only on rho>0; origin/nodes change the admissible field domain", "No quantum-particle ontology follows from this classical transformation", "Schrodinger high-k dispersion has no fundamental finite propagation cone", "No covariant nonlinear gravitational completion or global timelike foliation is proved"],
             software=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),
             runtime_seconds=time.monotonic()-start)
    path=pathlib.Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(result=out['result'],runtime_seconds=out['runtime_seconds'],
                         max_wave_error=max(r['maximum_wave_linf'] for r in rows),
                         max_energy_error=max(r['energy_relative_error'] for r in rows),
                         finite_difference_energy_orders=orders,
                         approaching_equal_amplitude=contrast),indent=2))


if __name__=='__main__':main()
