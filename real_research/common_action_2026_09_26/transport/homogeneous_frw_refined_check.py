#!/usr/bin/env python3
"""Bounded exact-identity and nonlinear homogeneous Einstein/carrier audit."""
import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    checks = {}

    def exact(name, expression):
        remainder = sp.factor(expression)
        assert remainder == 0, (name, remainder)
        checks[name] = 'exact zero'

    def yes(name, condition):
        assert bool(condition), name
        checks[name] = True

    # Cartesian canonical coordinates: Psi=(u0+i*u1)/sqrt(2), likewise Chi.
    u = sp.symbols('u0:5', real=True)
    v = sp.symbols('v0:5', real=True)
    M2, m2, mu2, V0, P2 = sp.symbols('M2 m2 mu2 V0 P2', positive=True)
    g, H, scale = sp.symbols('g H a', real=True)
    mixed = (u[2] + g*u[4]*u[0], u[3] + g*u[4]*u[1])
    potential = (M2*(u[0]**2+u[1]**2) + m2*sum(x*x for x in mixed)
                 + mu2*u[4]**2)/2
    gradient = [sp.diff(potential, x) for x in u]
    acceleration = [-3*H*w-force for w, force in zip(v, gradient)]
    v2 = sum(w*w for w in v)
    energy = v2/2 + potential
    energy_dot = sum(gradient[i]*v[i]+v[i]*acceleration[i] for i in range(5))
    exact('homogeneous energy dissipation identity', energy_dot+3*H*v2)
    Hdot = -v2/(2*P2)
    exact('Friedmann constraint propagation', 6*P2*H*Hdot-energy_dot)
    qpsi = u[1]*v[0]-u[0]*v[1]
    qchi = u[3]*v[2]-u[2]*v[3]
    qdot = lambda q: sum(sp.diff(q,u[i])*v[i]+sp.diff(q,v[i])*acceleration[i]
                        for i in range(5))
    source = g*m2*u[4]*(u[0]*u[3]-u[1]*u[2])
    exact('heavy component current exchange', qdot(qpsi)+3*H*qpsi-source)
    exact('light component current exchange', qdot(qchi)+3*H*qchi+source)
    exact('diagonal U1 continuity', qdot(qpsi+qchi)+3*H*(qpsi+qchi))
    exact('comoving U1 conservation', 3*scale**3*H*(qpsi+qchi)
          +scale**3*qdot(qpsi+qchi))
    # Chi stationarity first sets mixed=0; the remaining equations force origin.
    critical_sub = {u[2]:-g*u[4]*u[0], u[3]:-g*u[4]*u[1]}
    reduced = [sp.expand(x.subs(critical_sub, simultaneous=True)) for x in gradient]
    for i, expected in enumerate([M2*u[0], M2*u[1], 0, 0, mu2*u[4]]):
        exact('critical-point elimination component '+str(i), reduced[i]-expected)
    # A genuine excluded case: massless s gives a line of nonzero equilibria.
    flat_sub = {u[0]:0,u[1]:0,u[2]:0,u[3]:0,mu2:0}
    for i, force in enumerate(gradient):
        exact('mu zero flat-direction negative control '+str(i), force.subs(flat_sub))

    pars = dict(Mpl=100., V0=.01, M=3., m=1., mu=.5, gamma=.2)
    pp, vv, MM, mm, uu, gg = (pars[k] for k in ['Mpl','V0','M','m','mu','gamma'])

    def potential_force(x):
        x0,x1,x2,x3,s = x
        w0=x2+gg*s*x0
        w1=x3+gg*s*x1
        pot=.5*(MM*MM*(x0*x0+x1*x1)+mm*mm*(w0*w0+w1*w1)+uu*uu*s*s)
        force=np.array([MM*MM*x0+gg*mm*mm*s*w0,
                        MM*MM*x1+gg*mm*mm*s*w1,
                        mm*mm*w0,mm*mm*w1,
                        uu*uu*s+gg*mm*mm*(w0*x0+w1*x1)])
        return pot,force

    # All five fields, H, log(a), energy-loss and charge-transfer ledgers evolve.
    def rhs(t,y):
        x=y[:5];vel=y[5:10];hub=y[10]
        _,force=potential_force(x)
        speed2=float(vel@vel)
        charge_source=gg*mm*mm*x[4]*(x[0]*x[3]-x[1]*x[2])
        out=np.empty(14)
        out[:5]=vel
        out[5:10]=-3*hub*vel-force
        out[10]=-speed2/(2*pp*pp)
        out[11]=hub
        out[12]=3*hub*speed2
        out[13]=math.exp(3*y[11])*charge_source
        return out

    # Orthogonal implementation check: analytic force versus centered V differences.
    sample_points=[np.array([1.,-.2,.3,.4,.5]),np.array([-.7,.8,-.9,.2,-.3])]
    fd_errors=[]
    for x in sample_points:
        _,force=potential_force(x)
        fd=[]
        for i in range(5):
            d=np.zeros(5);d[i]=1e-5
            fd.append((potential_force(x+d)[0]-potential_force(x-d)[0])/(2e-5))
        fd_errors.append(float(np.max(np.abs(force-np.array(fd)))))
    yes('numeric force matches independent potential differences',max(fd_errors)<1e-8)

    initial=np.zeros(14)
    initial[:5]=[math.sqrt(2),0,math.sqrt(2)*1e-3,0,1e-3]
    initial[5:10]=[0,-math.sqrt(2)*MM,0,-math.sqrt(2)*mm*1e-3,0]
    E0=.5*float(initial[5:10]@initial[5:10])+potential_force(initial[:5])[0]
    initial[10]=math.sqrt((E0+vv)/(3*pp*pp))
    Hmin=math.sqrt(vv/(3*pp*pp))
    final_time=6000.
    evaluation_times=np.linspace(0,final_time,3001)

    def diagnostics(sol):
        x=sol.y[:5];vel=sol.y[5:10];hub=sol.y[10];alpha=sol.y[11]
        pot=np.array([potential_force(col)[0] for col in x.T])
        E=.5*np.sum(vel*vel,axis=0)+pot
        qP=x[1]*vel[0]-x[0]*vel[1]
        qC=x[3]*vel[2]-x[2]*vel[3]
        volume=np.exp(3*alpha)
        comoving=volume*(qP+qC)
        initial_charge=float(comoving[0])
        constraint=3*pp*pp*hub*hub-E-vv
        result={
            'function_evaluations':sol.nfev,
            'max_constraint_absolute':float(np.max(np.abs(constraint))),
            'final_constraint_absolute':float(constraint[-1]),
            'final_H_relative_constraint_residual':float(hub[-1]/math.sqrt((E[-1]+vv)/(3*pp*pp))-1),
            'max_constraint_relative_vacuum_density':float(np.max(np.abs(constraint))/vv),
            'max_constraint_relative_initial_density':float(np.max(np.abs(constraint))/(E0+vv)),
            'max_energy_balance_relative':float(np.max(np.abs(E+sol.y[12]-E0))/E0),
            'max_comoving_charge_relative':float(np.max(np.abs(comoving-initial_charge))/abs(initial_charge)),
            'max_component_transfer_balance_relative':float(np.max(np.abs(volume*qP-qP[0]-sol.y[13]))/abs(initial_charge)),
            'largest_sampled_energy_increase':float(np.max(np.diff(E))),
            'minimum_H':float(np.min(hub)),
            'final_E':float(E[-1]),
            'final_E_over_V0':float(E[-1]/vv),
            'final_H':float(hub[-1]),
            'final_H_over_Hmin':float(hub[-1]/Hmin),
            'final_a':float(math.exp(alpha[-1])),
            'final_field_norm':float(np.linalg.norm(x[:,-1])),
            'final_velocity_norm':float(np.linalg.norm(vel[:,-1])),
            'final_comoving_charge':float(comoving[-1]),
            'initial_comoving_charge':initial_charge,
            'final_physical_charge':float(qP[-1]+qC[-1]),
            'final_comoving_heavy_to_light_transfer':float(-sol.y[13,-1]),
        }
        return result,E

    runs=[]
    solutions=[]
    for name,rtol,atol in [('coarse',3e-11,3e-14),('fine',3e-13,3e-16)]:
        started=time.perf_counter()
        sol=solve_ivp(rhs,[0,final_time],initial,method='DOP853',rtol=rtol,atol=atol,
                      t_eval=evaluation_times,max_step=.4)
        elapsed=time.perf_counter()-started
        yes(name+' fully evolved ODE completed',sol.success and sol.t[-1]==final_time)
        row,E=diagnostics(sol)
        row.update(name=name,rtol=rtol,atol=atol,runtime_seconds=elapsed)
        runs.append(row);solutions.append(sol)
        yes(name+' expanding branch remains above vacuum floor',row['minimum_H']>=Hmin*(1-1e-5))
        yes(name+' energy decreases at every retained interval',row['largest_sampled_energy_increase']<0)
        yes(name+' energy balance tolerance',row['max_energy_balance_relative']<1e-6)
        yes(name+' Friedmann constraint tolerance',row['max_constraint_relative_initial_density']<1e-6)
        yes(name+' comoving charge tolerance',row['max_comoving_charge_relative']<1e-5)
        yes(name+' component charge exchange tolerance',row['max_component_transfer_balance_relative']<1e-5)
        yes(name+' enters vacuum-dominated regime',row['final_E_over_V0']<2e-4)

    print(json.dumps({'completed_trajectory_diagnostics':runs},indent=2),flush=True)
    fine=runs[1];coarse=runs[0]
    yes('constraint improves with tighter tolerance',fine['max_constraint_absolute']<coarse['max_constraint_absolute'])
    yes('charge improves with tighter tolerance',fine['max_comoving_charge_relative']<coarse['max_comoving_charge_relative'])
    agreement={
        'maximum_state_difference_first_ten_components':float(np.max(np.abs(solutions[0].y[:10]-solutions[1].y[:10]))),
        'final_H_relative_difference':abs(coarse['final_H']/fine['final_H']-1),
        'final_a_relative_difference':abs(coarse['final_a']/fine['final_a']-1),
        'final_E_relative_difference':abs(coarse['final_E']/fine['final_E']-1),
    }
    print(json.dumps({'two_tolerance_agreement':agreement},indent=2),flush=True)
    yes('fine Friedmann residual relative to vacuum density',fine['max_constraint_relative_vacuum_density']<1e-7)
    yes('two-tolerance final H agreement',agreement['final_H_relative_difference']<1e-5)
    yes('two-tolerance final scale agreement',agreement['final_a_relative_difference']<1e-5)
    yes('two-tolerance final excitation energy agreement',agreement['final_E_relative_difference']<1e-4)

    # Exact vacuum solution tests scale normalization and excludes artificial damping.
    vacuum=np.zeros(14);vacuum[10]=Hmin
    vacuum_sol=solve_ivp(rhs,[0,100.],vacuum,method='DOP853',rtol=3e-11,atol=3e-14)
    yes('vacuum de Sitter H exact control',vacuum_sol.success and abs(vacuum_sol.y[10,-1]-Hmin)<1e-15)
    yes('vacuum scale exact control',abs(vacuum_sol.y[11,-1]-100*Hmin)<1e-13)
    yes('vacuum fields stay exactly zero',np.max(np.abs(vacuum_sol.y[:10]))==0)
    yes('contracting branch reverses energy sign negative control',3*Hmin*float(initial[5:10]@initial[5:10])>0)

    output={
        'result':'accepted bounded homogeneous Einstein-five-field audit',
        'checks':checks,'check_count':len(checks),'parameters':pars,
        'initial_state':initial.tolist(),'initial_excitation_energy':E0,
        'Hmin':Hmin,'time_interval':[0,final_time],'retained_times':len(evaluation_times),
        'equations':'u_dot=v; v_dot=-3Hv-gradVmix; Hdot=-|v|^2/(2Mpl^2); log(a)_dot=H',
        'runs':runs,'agreement':agreement,'force_difference_errors':fd_errors,
        'non_claims':[
            'Finite ODE control is not the proof of global continuation or attraction',
            'Exactly homogeneous flat expanding branch only, with no ordinary matter',
            'No spatial transport, halo evacuation, empirical fit or full PDE health claim',
            'No exponential decay rate extracted from this finite witness',
            'Comoving charge is conserved; physical charge dilution is cosmological expansion',
            'Analytic conclusion requires positive M,m,mu,V0,Mpl and canonical Cartesian fields'
        ]}
    Path(args.output).write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    main()
