#!/usr/bin/env python3
"""Bounded matrix-free Newton steps retaining the positive elliptic branch."""
import warnings
import numpy as np
from scipy.sparse.linalg import LinearOperator,gmres
import grid3d as D

class MatvecLimit(Exception):pass
class YieldRequested(Exception):pass

def solve(grid,source,epsilon,initial,accepted=None,stop=None,history=None):
    """One epsilon level. Callback persists accepted safe states for the worker."""
    phi=np.array(initial,float,copy=True);source=np.asarray(source,float)
    if phi.shape!=grid.shape or source.shape!=grid.interior:raise ValueError('Grid/source shape mismatch')
    if not np.all(np.isfinite(phi)) or not np.all(np.isfinite(source)):raise ValueError('Nonfinite input')
    scale=max(1.,float(np.max(abs(source))));history=[] if history is None else list(history)
    h=D.hessian(grid,phi);residual=D.operator(h,epsilon)-source
    norm=float(np.max(abs(residual))/scale);minimum=D.principal_min(h,epsilon)
    if not history:history=[dict(step=0,residual=norm,principal_min=minimum,matvecs=0)]
    def finish(status):
        return phi,dict(status=status,residual=norm,principal_min=minimum,updates=history[-1]['step'],history=history)
    if not np.isfinite(minimum) or minimum<=0:return finish('nonelliptic_initial')
    if stop is not None and stop():return finish('interrupted')
    if norm<=1e-8:return finish('converged')
    size=source.size
    for step in range(history[-1]['step']+1,61):
        counter=[0]
        def product(vector):
            if stop is not None and stop():raise YieldRequested
            counter[0]+=1
            if counter[0]>400:raise MatvecLimit
            return D.jacobian_product(h,D.hessian(grid,grid.with_interior(vector)),epsilon).ravel()
        # Exact diagonal, including nonuniform mixed central coefficients.
        xx,yy,zz,xy,xz,yz=h
        diagonal=(epsilon+2*(yy+zz))*grid.second[0][1]+(epsilon+2*(xx+zz))*grid.second[1][1]+(epsilon+2*(xx+yy))*grid.second[2][1]
        for component,a,b in [(xy,0,1),(xz,0,2),(yz,1,2)]:
            diagonal-=4*component*grid.first[a][1]*grid.first[b][1]
        if np.any(~np.isfinite(diagonal)) or np.any(diagonal==0):return finish('invalid_preconditioner')
        operator=LinearOperator((size,size),matvec=product,dtype=np.float64)
        preconditioner=LinearOperator((size,size),matvec=lambda v:v/diagonal.ravel(),dtype=np.float64)
        try:
            with warnings.catch_warnings(record=True) as observed:
                warnings.simplefilter('always',RuntimeWarning)
                delta,info=gmres(operator,-residual.ravel(),M=preconditioner,rtol=1e-5,atol=0.,restart=20,maxiter=400,callback_type='legacy')
        except MatvecLimit:return finish('linear_matvec_limit')
        except YieldRequested:return finish('interrupted')
        if info!=0 or not np.all(np.isfinite(delta)):return finish('linear_solve_failed')
        warning_messages=sorted(set(str(w.message) for w in observed))
        known_warnings={name+' encountered in matmul' for name in ['divide by zero','overflow','invalid value']}
        if any(message not in known_warnings for message in warning_messages):return finish('unrecognized_linear_warning')
        # Independently recompute the unpreconditioned residual. The captured
        # platform matmul warnings are retained, never treated as convergence.
        try:linear_residual=product(delta)+residual.ravel()
        except MatvecLimit:return finish('linear_matvec_limit')
        except YieldRequested:return finish('interrupted')
        linear_relative=float(np.linalg.norm(linear_residual)/np.linalg.norm(residual.ravel()))
        if not np.isfinite(linear_relative) or linear_relative>1e-5:return finish('linear_residual_failed')
        if stop is not None and stop():return finish('interrupted')
        delta=grid.with_interior(delta);taken=False
        for backtrack in range(31):
            length=2.**(-backtrack);trial=phi+length*delta
            trial_h=D.hessian(grid,trial);trial_residual=D.operator(trial_h,epsilon)-source
            trial_norm=float(np.max(abs(trial_residual))/scale)
            if not np.isfinite(trial_norm) or trial_norm>=norm:continue
            trial_min=D.principal_min(trial_h,epsilon)
            if not np.isfinite(trial_min) or trial_min<=0:continue
            phi=trial;h=trial_h;residual=trial_residual;norm=trial_norm;minimum=trial_min;taken=True
            history.append(dict(step=step,residual=norm,principal_min=minimum,matvecs=counter[0],step_length=length,linear_relative_residual=linear_relative,linear_warnings=warning_messages))
            if accepted is not None:accepted(phi,history)
            break
        if not taken:return finish('line_search_failed')
        if stop is not None and stop():return finish('interrupted')
        if norm<=1e-8:return finish('converged')
    return finish('newton_limit')
