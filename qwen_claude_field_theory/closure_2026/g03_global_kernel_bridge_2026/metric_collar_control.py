"""Finite signed-source control of the full static-background initial jet.

The conservative rectangular SVD nullspace never promotes a small singular
value to an exact zero. Results concern the computed initial and fifth wall
jets only; they do not establish all-order wall compatibility or evolution.
"""
import argparse
import json
from pathlib import Path
import platform
import time

import numpy as np
import scipy
from scipy.integrate import solve_ivp, simpson
import sympy as s

from metric_initial_response import operators
from metric_static_background import solve_background, curved_matter_jets
from metric_wall_jets import derive_wall


CENTERS = np.array([-.72, -.59, -.46, -.33, -.20, .20, .33, .46, .59, .72])
WIDTH = .048


def basis_values(x):
    """Ten C-infinity bumps; observer |x|<.15 and walls |x|>.8 are empty."""
    z = (float(x)-CENTERS)/WIDTH
    out = np.zeros(len(CENTERS))
    mask = abs(z) < 1
    out[mask] = np.exp(1-1/(1-z[mask]**2))
    return out


def control(y0, ratio, L):
    d, coeff, _ = operators()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp = d['symbols']
    chi = (1-y0)*np.exp(-y0)
    if chi == 0:
        raise ValueError('The selected scaling excludes chi=0')
    seed = solve_background(y0, ratio, L)['seed']
    rhs = s.lambdify((u,b), d['rhs'].subs({a0:1, Lam:ratio}), 'numpy')
    def bgflow(x, Y):
        return L*np.array([Y[2],Y[3],*np.asarray(rhs(*Y[2:]),float).reshape(2)])
    background = [solve_ivp(bgflow, (0,sign), seed, method='DOP853',
        rtol=2e-13, atol=2e-15, max_step=1/64, dense_output=True) for sign in [-1,1]]
    if not all(sol.success for sol in background):
        raise RuntimeError('Background integration failed')
    cf = s.lambdify((N,A,u,b,up,bp), coeff.subs({a0:1,Lam:ratio}), 'numpy')
    forcing = -float(s.sympify(curved_matter_jets()['proper_time_stress_acceleration_coefficient']))
    def values(x):
        lnN,lnA,uu,bb = background[0 if x < 0 else 1].sol(x)
        upp,bpp = np.asarray(rhs(uu,bb),float).reshape(2)
        nn,aa = np.exp(lnN),np.exp(lnA)
        C = np.asarray(cf(nn,aa,uu,bb,upp,bpp),float)
        C *= np.array([L**2,L,1,L**2/chi,L/chi,1/chi])
        C[1,:] *= chi
        return nn,aa,uu,bb,upp,bpp,C

    def integrate(source_weights, method, rtol, atol, step):
        # One simultaneous solve for every source plus all three homogeneous
        # columns: initial Z0', initial Z2', and scaled c=chi*c.
        count = source_weights.shape[1]
        columns = count+3
        initial = np.zeros((5,columns))
        initial[1,count] = 1
        initial[3,count+1] = 1
        global_c = np.zeros(columns); global_c[-1] = 1
        def flow(x, flat):
            Y = flat.reshape(5,columns)
            nn,aa,_,_,_,_,C = values(x)
            source = np.zeros(columns)
            source[:count] = basis_values(x)@source_weights
            target = np.zeros((2,columns))
            target[1] = chi*forcing*nn**2*source+2*global_c/nn
            low = C[:,[0,1,3,4]]@Y[[0,1,2,3]]
            second = np.linalg.solve(C[:,[2,5]],target-low)
            return np.vstack([Y[1],second[0],Y[3],second[1],aa**2*Y[0]]).reshape(-1)
        sol = solve_ivp(flow,(-1,1),initial.reshape(-1),method=method,
            rtol=rtol,atol=atol,max_step=step,dense_output=True)
        if not sol.success:
            raise RuntimeError('Fundamental response integration failed: '+sol.message)
        endpoint = sol.y[:,-1].reshape(5,columns)
        matching = endpoint[[0,2,4],count:]
        weights = np.linalg.solve(matching,-endpoint[[0,2,4],:count])
        def dense(x):
            raw = sol.sol(x)
            shape = np.shape(x)
            Y = raw.reshape((5,columns)+shape)
            return Y[:,:count]+np.einsum('ij...,jk->ik...',Y[:,count:],weights)
        return dense,weights,matching,sol.nfev

    design, matching_weights, matching, design_nfev = integrate(
        np.eye(len(CENTERS)), 'DOP853', 5e-13, 3e-15, 1/96)
    ends = design(np.array([-1.,1.]))
    control_map = np.vstack([matching_weights[2]/chi,
        L*ends[1,:,0],L*ends[3,:,0]/chi,L*ends[1,:,1],L*ends[3,:,1]/chi])
    scales = np.linalg.norm(control_map,axis=1)
    if np.any(scales == 0):
        raise RuntimeError('Zero control row requires a different explicitly documented scaling')
    equilibrated = control_map/scales[:,None]
    _,singular,Vh = np.linalg.svd(equilibrated,full_matrices=True)
    # The last n-m vectors exist for EVERY m-by-n matrix, regardless of rank.
    # Never add threshold-selected nearly-null directions to this subspace.
    conservative = Vh[equilibrated.shape[0]:].T
    signal = design(0.)[0,:]
    weights = conservative@(conservative.T@signal)
    if np.max(abs(weights)) == 0:
        raise RuntimeError('Guaranteed rectangular nullspace contains no observer signal')
    weights /= np.max(abs(weights))
    selected_residual = np.linalg.norm(equilibrated@weights)/(
        np.linalg.norm(equilibrated)*np.linalg.norm(weights))
    augmented = np.vstack([equilibrated,signal/np.linalg.norm(signal)])
    warnings = []
    if singular[-1] < 1e-8*singular[0]:
        warnings.append('Control rows are nearly dependent; small singular values are reported, '
                        'not treated as exact zeros. Independent reintegration is required.')
    rank = int(np.linalg.matrix_rank(equilibrated))
    if rank < len(scales):
        warnings.append('Floating-point rank is below five; only the guaranteed n-minus-five '
                        'nullspace was used. This is not an exact rank certificate.')

    coarse,coarse_weights,_,coarse_nfev = integrate(weights[:,None],
        'RK45',2e-10,2e-13,1/128)
    fine,fine_weights,_,fine_nfev = integrate(weights[:,None],
        'DOP853',2e-13,3e-15,1/144)
    grid = np.linspace(-1,1,2001)
    Y = fine(grid)[:,0,:]; coarse_Y = coarse(grid)[:,0,:]
    design_Y = np.einsum('ikj,k->ij',design(grid),weights)
    geometry = np.array([values(x)[:6] for x in grid])
    nn,aa = geometry[:,0],geometry[:,1]
    curvature = -3*L**2*Y[0]/nn**2
    curvature_coarse = -3*L**2*coarse_Y[0]/nn**2
    source = np.array([basis_values(x)@weights for x in grid])
    peak = np.max(abs(curvature)); state_peak = np.max(abs(Y),axis=1)
    observer = float(-3*L**2*fine(0.)[0,0]/values(0.)[0]**2)
    error = max(np.max(abs(curvature-curvature_coarse)),
                np.max(abs(curvature+3*L**2*design_Y[0]/nn**2)))
    if peak == 0:
        raise RuntimeError('No resolved curvature response')
    collar = abs(grid) >= .8
    collar_tail = max(np.max(abs(Y[i,collar]))/max(state_peak[i],1e-300) for i in [0,2])
    scaled_c = float(fine_weights[2,0]); physical_c = scaled_c/chi
    reintegrated_control = np.array([physical_c,L*Y[1,0],L*Y[3,0]/chi,
                                    L*Y[1,-1],L*Y[3,-1]/chi])
    reintegrated_residual = np.linalg.norm(reintegrated_control/scales)/(
        np.linalg.norm(equilibrated)*np.linalg.norm(weights))
    def combined_flow(x, state):
        n,a,_,_,_,_,C = values(x)
        target = np.array([0.,chi*forcing*n*n*(basis_values(x)@weights)+2*scaled_c/n])
        second = np.linalg.solve(C[:,[2,5]],target-C[:,[0,1,3,4]]@state[[0,1,2,3]])
        return np.array([state[1],second[0],state[3],second[1],a*a*state[0]])
    dx = 1e-5; residuals = []
    for x in np.linspace(-.99,.99,161):
        derivative = (fine(x+dx)[:,0]-fine(x-dx)[:,0])/(2*dx)
        predicted = combined_flow(x,fine(x)[:,0])
        residuals.append(np.max(abs(derivative-predicted)/(1+abs(predicted))))
    _,_,wall_expression,_ = derive_wall()
    wp,vp = s.symbols('wp vp'); cc = s.symbols('c',real=True)
    wall_fn = s.lambdify((N,A,u,b,up,bp,wp,vp,cc),
        wall_expression.subs({a0:1,Lam:ratio}),'numpy')
    wall_jets = []
    for x in [-1.,1.]:
        n,a,uu,bb,upp,bpp,_ = values(x); state = fine(x)[:,0]
        wall_jets.append(float(wall_fn(n,a,uu,bb,upp,bpp,
            L*state[1],L*state[3]/chi,physical_c)))
    wall_relative = max(abs(np.array(wall_jets)))/max(state_peak[0],1e-300)
    mean = abs(simpson(aa**2*Y[0],x=grid))/(2*max(state_peak[0],1e-300))
    relative_error = error/peak
    boundary_error = np.max(abs(Y[[0,2,4]][:,[0,-1]]))
    gates = {
        'rectangular nullspace residual': selected_residual < 1e-10,
        'independent five-component control': reintegrated_residual < 1e-5,
        'signed source': min(source) < 0 < max(source),
        'observer signal resolution': abs(observer)/max(error,1e-300) > 100,
        'observer fraction of peak': abs(observer)/peak > 1e-3,
        'source-free collar tails': collar_tail < 1e-5,
        'independent integration refinement': relative_error < 1e-5,
        'weighted mean': mean < 1e-6,
        'finite-difference ODE residual': max(residuals) < 1e-5,
        'fifth wall jet': wall_relative < 1e-5,
        'Dirichlet and integrated mean endpoints': boundary_error < 1e-9,
    }
    gates = {name: bool(value) for name,value in gates.items()}
    passed = all(gates.values())
    if not passed:
        warnings.append('At least one finite-resolution gate failed; no successful collar '
                        'control is claimed for this case.')
    return dict(y0=y0,Lambda_over_a0_squared=ratio,L=L,chi=chi,
        control_shape=list(control_map.shape),physical_control_map=control_map.tolist(),
        control_row_scales=scales.tolist(),control_singular_values=singular.tolist(),
        raw_control_singular_values=np.linalg.svd(control_map,compute_uv=False).tolist(),
        computed_control_rank=rank,computed_augmented_rank=int(np.linalg.matrix_rank(augmented)),
        augmented_singular_values=np.linalg.svd(augmented,compute_uv=False).tolist(),
        conservative_nullity=conservative.shape[1],source_weights=weights.tolist(),
        selected_control_relative_residual=float(selected_residual),
        independently_reintegrated_global_c=float(physical_c),
        independently_reintegrated_control=reintegrated_control.tolist(),
        reintegrated_control_scaled_residual=float(reintegrated_residual),
        matching_condition_number=float(np.linalg.cond(matching)),
        source_minimum=float(min(source)),source_maximum=float(max(source)),
        observer_curvature=observer,peak_curvature=float(peak),
        observer_to_peak_ratio=float(abs(observer)/peak),
        observer_resolution_ratio=float(abs(observer)/max(error,1e-300)),
        boundary_residual=float(boundary_error),relative_mean_residual=float(mean),
        relative_collar_tail=float(collar_tail),relative_refinement_difference=float(relative_error),
        finite_difference_ODE_residual=float(max(residuals)),
        normalized_fifth_wall_jets=wall_jets,wall_fifth_relative_residual=float(wall_relative),
        sampled_x=grid[::40].tolist(),sampled_source=source[::40].tolist(),
        sampled_curvature=curvature[::40].tolist(),
        integration_evaluations=[design_nfev,coarse_nfev,fine_nfev],
        methods=['DOP853 simultaneous basis','RK45 combined source','DOP853 combined source'],
        success=bool(passed),gate_results=gates,conditioning_warnings=warnings)


def audit():
    start = time.monotonic()
    rows = [control(.5,0.,.02),control(10.5,float(32*s.pi),.002)]
    return dict(responses=rows,all_finite_controls_pass=all(r['success'] for r in rows),
        basis_centers=CENTERS.tolist(),basis_width=WIDTH,observer_gap=[-.15,.15],
        wall_collars=[[-1.,-.8],[.8,1.]],runtime_seconds=time.monotonic()-start,
        environment=dict(python=platform.python_version(),numpy=np.__version__,
                         scipy=scipy.__version__,sympy=s.__version__),
        scope='Finite floating-point full-background signed initial-jet control and fifth-wall-jet '
              'check only. No certified exact rank, all-order wall compatibility, nonlinear '
              'shared-data construction for this new profile, or evolution theorem.')


def print_report(result):
    for number,row in enumerate(result['responses'],1):
        status = '[ok]' if row['success'] else '[FAIL]'
        print(f'{number}. {status}', 'y0',row['y0'],'control singular values',
              row['control_singular_values'],'observer/peak',row['observer_to_peak_ratio'],
              'collar relative',row['relative_collar_tail'],'wall fifth relative',
              row['wall_fifth_relative_residual'])
        for gate_number,(gate,passed) in enumerate(row['gate_results'].items(),1):
            print(f'   {number}.{gate_number}.', '[ok]' if passed else '[FAIL]', gate)
        for warning in row['conditioning_warnings']:
            print('WARNING:',warning)
    print(result['scope'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    args = p.parse_args(); result = audit()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print_report(result)
    return 0 if result['all_finite_controls_pass'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
