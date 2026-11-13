#!/usr/bin/env python3
"""Independent exact derivatives of the NR action, Hamiltonian and linear mode."""
import argparse,json
from pathlib import Path
import sympy as s


def main(output):
    st,sx,phi,P,Pi,C,pc,gamma,w,n=s.symbols('st sx phi P Pi C pc gamma w n',nonzero=True)
    X=st-phi-sx*sx/2
    # A nontrivial generic polynomial gate tests both mixed and Pi derivatives.
    alpha,beta=s.symbols('alpha beta')
    S=1+alpha*Pi+beta*Pi*Pi
    H=C*X*X*S
    L=H+X*Pi-w*P*P/2-gamma*Pi*Pi/2
    N=2*C*X*S+Pi
    checks={}
    def exact(name,expr):checks[name]=s.simplify(expr)==0
    exact('clock_time_momentum_is_charge',s.diff(L,st)-N)
    exact('clock_space_momentum_is_charge_velocity',s.diff(L,sx)+N*sx)
    exact('potential_source_is_charge',s.diff(L,phi)+N)
    exact('polarization_divergence_momentum',s.diff(L,Pi)-(X+C*X*X*s.diff(S,Pi)-gamma*Pi))
    exact('polarization_algebraic_derivative',s.diff(L,P)+w*P)
    # Legendre transform with respect to the clock offset, independently of code.
    clock=(n-Pi)/(2*C*S)
    energy=(n-Pi)**2/(4*C*S)+w*P*P/2+gamma*Pi*Pi/2
    exact('energy_n_derivative_is_clock_offset',s.diff(energy,n)-clock)
    exact('energy_Pi_derivative_is_negative_chemical_potential',s.diff(energy,Pi)+clock+C*clock*clock*s.diff(S,Pi)-gamma*Pi)
    # General Hessian of Legendre-reduced H, without selecting a gate.
    A,b,D,k,K,n0=s.symbols('A b D k K n0',nonzero=True);c=1+b
    enn=1/A;enp=-c/A;epp=c*c/A-D
    pressure=s.factor(enn-enp**2/(epp+w/k**2))
    claimed=(w-D*k*k)/(A*w+(c*c-A*D)*k*k)
    exact('eliminated_Hamiltonian_hessian',pressure-claimed)
    omega2=n0*(k*k*claimed-K)
    ungated=s.factor(omega2.subs({b:0,D:0,w:K}))
    exact('ungated_pressure_gravity_cancellation',ungated+n0*A*K*K/(A*K+k*k))
    # Exponential gate derivative used by the numerical Newton solver.
    Se=s.exp(-Pi/pc);xx=(n-Pi)/(2*C*Se)
    chem=xx+C*xx*xx*s.diff(Se,Pi)
    dclaimed=s.exp(Pi/pc)/(2*C)*(-1+2*(n-Pi)/pc-(n-Pi)**2/(2*pc*pc))
    exact('Newton_constraint_jacobian',s.diff(chem,Pi)-dclaimed)
    # Mutation witnesses: dropping gate coupling or using ungated charge fails.
    point={st:s.Rational(1,10),sx:s.Rational(1,20),phi:s.Rational(1,100),Pi:s.Rational(1,5),C:2,alpha:3,beta:1,gamma:1}
    checks['omit_HPi_mutation_rejected']=s.simplify((C*X*X*s.diff(S,Pi)).subs(point))!=0
    checks['ungated_charge_mutation_rejected']=s.simplify((N-(2*C*X+Pi)).subs(point))!=0
    # Compare accepted finite runs on common space-time sampling.
    import numpy as np
    p=Path(__file__).parent;lo=np.load(p/'nr32/trajectory.npz');hi=np.load(p/'nr64/trajectory.npz')
    difference=float(np.max(np.abs(lo['n']-hi['n'][:,::2])))
    checks['two_grid_density_difference_under_2e_minus_8']=difference<2e-8
    family=json.loads((p/'charge_family/results.json').read_text());normal=json.loads((p/'nr64/results.json').read_text())
    checks['distinct_global_initial_charges_remain_distinct']=abs(family['charge_total_final']/normal['charge_total_final']-1.3)<1e-13
    result={'checks':checks,'all_pass':all(checks.values()),'count':len(checks),
            'max_common_grid_density_difference':difference,'pressure_response':str(claimed),
            'omega_squared':str(omega2),'ungated_omega_squared':str(ungated),
            'scope':'Exact symbolic identities plus finite accepted-run comparison, not full relativistic perturbations'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_pass']


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
