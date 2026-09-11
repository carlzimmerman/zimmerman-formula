#!/usr/bin/env python3
"""Conserved baryon initial-value response; two physical potentials, no MOND input.

The scalar/metric perturbations are O(epsilon). A Gaussian transform is a linear
spherical benchmark, not a finite-mass nonlinear galaxy or measured G_N.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import simpson, solve_ivp
from scipy.special import erf, expit, spherical_jn
import sympy as s
from source import derive, load, HERE


def gaussian_newton_force(radius, width, mass, G):
    z=radius/(math.sqrt(2)*width)
    enclosed=erf(z)-2*z/math.sqrt(math.pi)*math.exp(-z*z)
    return G*mass*enclosed/radius**2


def radial_force(k, potential, radius, width, mass):
    # d j0(kr)/dr=-k j1(kr); Fourier inverse convention (2pi)^-3.
    f=-mass*k**4*potential*np.exp(-k*k*width*width/2)*spherical_jn(1,k*radius)/(2*np.pi**2)
    return float(simpson(f,x=np.log(k)))


def run(modes=129):
    if modes<17 or modes%2!=1:raise ValueError('use an odd mode count >=17')
    facts,c=derive()
    if not all(facts['checks'].values()):raise AssertionError('source variation failed')
    order=('a','H','q','M','gamma','k','A','U','B0','qd')
    args=[c[v] for v in order]
    k,C,z,u,ud=[c[v] for v in ('k','C','z','u','ud')]
    parts=[c['pre_zeta_kinetic'],c['velocity_mixing'],c['field_mixing'],c['constraint'],
           c['raw_mixed'],c['raw_potential'],c['fz']/C,
           -c['Qmix']/2,-c['nu']/2,
           *[s.diff(c['T'],v) for v in (z,u,ud,C)],
           c['Qmix'],c['phi_z'],c['phi_u']]
    fn=s.lambdify(args,parts,'numpy',cse=True)
    profile_facts,rhs=load('source_profile',HERE.parent/'nonlinear_transport/stationary.py').symbolic()
    def background_ode(x,y):
        return rhs(math.exp(y[0]),expit(y[1]),1/(1+7*math.exp(3*x)))
    def make_profile(method,rtol,atol):
        out=[]
        for end in (-1.05,.05):
            sol=solve_ivp(background_ode,(0,end),[math.log(.1),0.],method=method,
                          rtol=rtol,atol=atol,dense_output=True)
            if not sol.success:raise AssertionError(sol.message)
            out.append(sol)
        return out
    profile=make_profile('DOP853',2e-13,2e-14)
    profile_check=make_profile('Radau',2e-12,2e-13)
    profile_error=max(float(np.max(np.abs(profile[int(x>=0)].sol(x)-profile_check[int(x>=0)].sol(x)))) for x in np.linspace(-1.,.01,19))
    if profile_error>1e-8:raise AssertionError('background integrators disagree')
    # Domain is explicit: k=0 is NOT inferred from this inverse.
    kval=np.geomspace(.01,800.,modes)
    def algebra(x,lm,lv,gamma):
        # Analytic coefficient map: complex arguments are intentional for exact
        # directional differentiation along the action-derived background ODE.
        a=np.exp(x);m=np.exp(lm);v=1/(1+np.exp(-lv))
        q=1/(1+m);A=.1/a**3;U=m*q*A;H=np.sqrt((.7+A)/3)
        B0=A/q*(1+2/m);qd=-3*A*H*v/B0-q*U/(2*H)
        raw=[np.broadcast_to(np.asarray(p),kval.shape) for p in fn(a,H,q,1.,gamma,kval,A,U,B0,qd)]
        A0,J,E,D,Braw,Craw,fz,fv0,fu0,Tz,Tu,Tv,TC,Qmix,pz,pu=raw
        Af=A0-J*J/D;Bf=Braw-J*E/D;Cf=Craw-E*E/D
        fv=fv0-J*fz/D;fu=fu0-E*fz/D
        return dict(a=a,H=H,q=q,A0=A0,J=J,E=E,D=D,Af=Af,Bf=Bf,Cf=Cf,
                    fv=fv,fu=fu,fz=fz,Tz=Tz,Tu=Tu,Tv=Tv,TC=TC,Qmix=Qmix,pz=pz,pu=pu)
    def coeff(x,gamma,back=profile):
        lm,lv=back[int(x>=0)].sol(x)
        p=algebra(x,lm,lv,gamma)
        if not (np.all(np.isfinite(p['Af'])) and np.all(p['Af']>0) and np.all(p['D']<0)):
            raise AssertionError('reduction left tested regular sign domain')
        return p

    rows=[]
    for gamma in (0.,1e-6):
        initial=coeff(-1.,gamma)
        scale=initial['Af']*initial['H']
        y0=np.vstack([np.zeros(modes),initial['fv']/scale]).ravel()
        def field_ode(x,y,back=profile):
            p=coeff(x,gamma,back);uv,ps=y.reshape(2,modes)
            velocity=(scale*ps-p['Bf']*uv-p['fv'])/p['Af']
            pdot=p['Bf']*velocity+p['Cf']*uv+p['fu']
            return np.vstack([velocity/p['H'],pdot/(scale*p['H'])]).ravel()
        solutions=[]
        # Radau has dense Jacobian by default: explicitly give independent 2x2
        # mode blocks, keeping resource use proportional to mode count.
        from scipy.sparse import bmat, diags
        def jac(x,y):
            p=coeff(x,gamma,profile_check)
            f11=-p['Bf']/p['Af']/p['H'];f12=scale/p['Af']/p['H']
            f21=(p['Cf']-p['Bf']**2/p['Af'])/(scale*p['H'])
            return bmat([[diags(f11),diags(f12)],[diags(f21),diags(-f11)]],format='csc')
        for method,tol,back in [('DOP853',2e-11,profile),('Radau',3e-11,profile_check)]:
            extra=dict(jac=jac) if method=='Radau' else {}
            sol=solve_ivp(lambda x,y:field_ode(x,y,back),(-1.,.01),y0,method=method,
                          rtol=tol,atol=tol*1e-3,dense_output=True,**extra)
            if not sol.success:raise AssertionError(sol.message)
            solutions.append((sol,back,method))
        metrics=[]
        for sol,back,method in solutions:
            def local_fields(primitives,state):
                x,lm,lv=primitives;p=algebra(x,lm,lv,gamma)
                uv,ps=state.reshape(2,modes)
                velocity=(scale*ps-p['Bf']*uv-p['fv'])/p['Af']
                zv=-(p['J']*velocity+p['E']*uv+p['fz'])/p['D']
                Tv=p['Tz']*zv+p['Tu']*uv+p['Tv']*velocity+p['TC']
                return p,uv,velocity,zv,Tv
            def fields(x):
                lm,lv=back[int(x>=0)].sol(x)
                return local_fields(np.array([x,lm,lv]),sol.sol(x))
            samples=[]
            for x in (-.7,-.35,0.):
                p,uv,vel,zv,Tv=fields(x)
                psi=p['H']*(p['Qmix']*uv-Tv)
                lm,lv=back[int(x>=0)].sol(x)
                primitive=np.array([x,lm,lv]);ydot=field_ode(x,sol.sol(x),back)*p['H']
                direction=p['H']*np.array([1.,*background_ode(x,[lm,lv])])
                phis=[]
                for h in (1e-16,1e-20,1e-24):
                    td=np.imag(local_fields(primitive+1j*h*direction,sol.sol(x)+1j*h*ydot)[4])/h
                    phis.append(p['pz']*zv+p['pu']*uv+td)
                norm=np.maximum(np.maximum(abs(psi),abs(phis[-1])),1e-15)
                refinement=float(np.max(abs(phis[-1]-phis[-2])/norm))
                slip=float(np.max(abs(phis[-1]-psi)/norm))
                fd=[]
                for h in (.004,.002):
                    td=(-fields(x+2*h)[4]+8*fields(x+h)[4]-8*fields(x-h)[4]+fields(x-2*h)[4])/(12*h)*p['H']
                    fd.append(float(np.max(abs(p['pz']*zv+p['pu']*uv+td-phis[-1])/norm)))
                samples.append(dict(ln_a=x,Phi=phis[-1].tolist(),Psi=psi.tolist(),
                    derivative_refinement=refinement,finite_difference_comparison=fd,slip_relative=slip))
            metrics.append(dict(method=method,nfev=sol.nfev,samples=samples))
        pv=np.array(metrics[0]['samples'][-1]['Phi']);pc=np.array(metrics[1]['samples'][-1]['Phi'])
        psiv=np.array(metrics[0]['samples'][-1]['Psi'])
        agreement=float(np.max(abs(pv-pc)/np.maximum(np.maximum(abs(pv),abs(pc)),1e-15)))
        # Reconstruct two mass/size-scaled Gaussians at matched enclosed g_bare.
        pairs=[]
        for width in (.02,.04,.08):
            radius=3*width;mass=1e-8;Gbare=1/(8*np.pi)
            g1=radial_force(kval,pv,radius,width,mass)
            g2=radial_force(kval,pv,2*radius,2*width,4*mass)
            lens1=radial_force(kval,(pv+psiv)/2,radius,width,mass)
            bare=gaussian_newton_force(radius,width,mass,Gbare)
            pairs.append(dict(width=width,radius=radius,test_source_mass=mass,
                g_M_r=g1,g_4M_2r=g2,matched_acceleration_ratio=g2/g1,
                force_over_bare_Einstein= g1/bare,lensing_force_over_dynamic=lens1/g1,
                same_radius_four_mass_ratio=radial_force(kval,pv,radius,width,4*mass)/g1))
        rows.append(dict(gamma=gamma,integrator_comparison=agreement,integrators=metrics,
                         matched_source_pairs=pairs))
        print(json.dumps(dict(gamma=gamma,modes=modes,integrator_comparison=agreement,
              max_slip=max(v['slip_relative'] for m in metrics for v in m['samples']),
              matched_pairs=pairs)),flush=True)
    result=dict(mode_grid=kval.tolist(),modes=modes,profile_comparison=profile_error,
        source_derivation_checks=facts['checks'],results=rows,
        conventions='a(final)=1, M2=Qc=1, I=.1, Lambda=.7, m(1)=.1, v(1)=.5; C=1 response kernels; Fourier inverse (2pi)^-3',
        physical_initial_data='u=udot=0 at ln(a)=-1; p=fv, no source-specific free clock charge',
        non_claims=['Linear response only; masses in radial transform rescale a derivative, not a nonlinear solution.',
        'Force/bare-Einstein ratio is not an independently measured Solar-System Newton constant.',
        'No action coefficient, a0, exponential kernel, or primordial-data prescription is derived.',
        'No CMB, finite-mass dust evolution, nonlinear stability or galaxy likelihood.',
        'Independent ODE/stencil agreement is not a rigorous interval error bound.',
        'Linear scaling by four cannot on its own exclude a singular/nonperturbative MOND branch.'],
        full_theory_status='OPEN')
    result['numerical_checks'] = dict(
        independent_ODE_agreement=all(row['integrator_comparison']<1e-7 for row in rows),
        independent_metric_no_slip=all(v['slip_relative']<1e-7 for row in rows for m in row['integrators'] for v in m['samples']),
        complex_step_refinement=all(v['derivative_refinement']<1e-8 for row in rows for m in row['integrators'] for v in m['samples']))
    if not all(result['numerical_checks'].values()):raise AssertionError(result['numerical_checks'])
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--modes',type=int,default=129)
    p.add_argument('--refine',action='store_true',help='also run 2n-1 and 4n-3 modes with cached symbolic derivation')
    p.add_argument('--result-file',type=Path);args=p.parse_args()
    result=run(args.modes)
    if args.refine:
        runs=[result,run(2*args.modes-1),run(4*args.modes-3)]
        differences=[]
        for coarse,fine in zip(runs,runs[1:]):
            errors=[]
            for a,b in zip(coarse['results'],fine['results']):
                for x,y in zip(a['matched_source_pairs'],b['matched_source_pairs']):
                    errors.extend(abs(x[key]/y[key]-1) for key in ('g_M_r','g_4M_2r','matched_acceleration_ratio'))
            differences.append(dict(coarse_modes=coarse['modes'],fine_modes=fine['modes'],max_relative_difference=max(errors)))
        if differences[-1]['max_relative_difference']>1e-6:raise AssertionError('radial quadrature not converged')
        result=dict(runs=runs,radial_refinement=differences,full_theory_status='OPEN')
        print(json.dumps(dict(radial_refinement=differences)),flush=True)
    if args.result_file:args.result_file.write_text(json.dumps(result,indent=2)+'\n')
