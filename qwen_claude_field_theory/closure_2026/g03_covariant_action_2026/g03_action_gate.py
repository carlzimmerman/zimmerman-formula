#!/usr/bin/env python3
"""Finite/symbolic G03 diagnostics; success is not a healthy-theory certificate."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone

import numpy as np
import scipy
from scipy.linalg import expm, expm_frechet
from scipy.optimize import brentq
import sympy as sp

HERE = Path(__file__).resolve().parent


def kernel(p):
    """q(p^2), f(p), with exact inverse root solve; no clipped deep kernel."""
    p = np.asarray(p, dtype=float)
    s = np.abs(p)
    y = np.array([brentq(lambda z: z*(-np.expm1(-z))-v,
                        0, v+2*np.sqrt(v)+2, xtol=1e-14) for v in s.flat]).reshape(s.shape)
    primitive = y*y + 2*(1+y)*np.exp(-y)-2
    q = 2*s*y-primitive-s*s
    f = np.sign(p)*y*np.exp(-y)
    return q, f


def ring_geometry(w, dw=None):
    """Finite-volume intrinsic Laplacian for ds^2=e^(2w) dx^2 on S^1.

    Mesh spacing is one. Vertex mass=e^w; edge conductivity=e^(-w_edge).
    This is a curved-leaf surrogate, not a 3D continuum convergence test.
    """
    n = len(w)
    d = np.roll(np.eye(n), -1, axis=1)-np.eye(n)
    avg = (np.roll(np.eye(n), -1, axis=1)+np.eye(n))/2
    we = avg @ w
    m = np.exp(w)
    stiffness = d.T @ np.diag(np.exp(-we)) @ d
    lap = -stiffness/m[:, None]
    if dw is None:
        return d, avg, m, we, lap
    dstiff = d.T @ np.diag(-np.exp(-we)*(avg@dw)) @ d
    dlap = -dw[:, None]*lap-dstiff/m[:, None]
    return d, avg, m, we, lap, dlap


def checks():
    records = []
    details = {}

    def check(name, condition, evidence):
        condition = bool(condition)
        records.append(dict(name=name, passed=condition, evidence=evidence))
        print(f'[{"ok" if condition else "FAIL"}] {len(records)} {name}: {evidence}')

    y = sp.symbols('y', positive=True)
    s = y*(1-sp.exp(-y))
    lam = sp.diff(s,y)
    q = 2*s*y-(y*y+2*(1+y)*sp.exp(-y)-2)-s*s
    qprime = sp.simplify(sp.diff(q,y)/(2*s*lam))
    check('exact inverse primitive', sp.simplify(qprime-(y/s-1)) == 0,
          'd q(s^2)/d(s^2) = y/s - 1 by symbolic chain rule')

    ph, ps, uu, qq = sp.symbols('grad_phi grad_psi grad_U Q')
    le = 2*ps**2-4*ph*ps
    la = 2*(uu-ph)**2+2*qq
    reduced = sp.expand((le+la).subs(ps,ph))
    check('independent metric potentials and T-B static action',
          sp.diff(le+la, ps) == 4*(ps-ph)
          and sp.expand(reduced-(-4*ph*uu+2*uu**2+2*qq)) == 0,
          str(reduced)+'; slip equation is Delta(psi-phi)=0 at leading weak order')
    # Action differentiation, not assigned field equations: minus divergence
    # of each gradient derivative; the nonlinear Q variation is tested below.
    check('unsmoothed baryonic source coefficient',
          sp.diff(reduced, ph) == -4*uu and sp.diff(reduced, uu) == -4*ph+4*uu,
          'metric variation gives 4 Delta U; U variation gives 4 Delta phi - 4 Delta U')

    H, fdot, comlap, scale = sp.symbols('H f_dot comoving_laplacian a', nonzero=True)
    projected = comlap/scale**2-3*H*fdot
    intrinsic = sp.simplify(projected+3*H*fdot)
    check('intrinsic versus projected Hessian', intrinsic == comlap/scale**2,
          'Delta_h f = h^{mu nu} nabla_mu nabla_nu f + K n^mu partial_mu f; FLRW cancellation')

    variation_rows = []
    for n in (9, 15, 23):
        x = np.arange(n)*2*np.pi/n
        w = .22*np.cos(x)+.09*np.sin(2*x)
        dw = .21*np.sin(x)+.13*np.cos(3*x)
        N = np.exp(.27*np.sin(x))
        d, avg, m, we, lap, dlap = ring_geometry(w,dw)
        b = 1.3
        filt, dfilt = expm_frechet(b*lap, b*dlap)
        u = .61*np.sin(2*x)+.22*np.cos(3*x)
        du = .31*np.cos(x)+.27*np.sin(3*x)
        # Fixed affine-gradient background on periodic perturbations.
        raw = d@(filt@u)+.83
        p = np.exp(-we)*raw
        weights = (avg@N)*np.exp(we)
        qv, fv = kernel(p)
        grad_u = filt.T@d.T@(2*weights*fv*np.exp(-we))
        wrong_grad = d.T@(2*weights*fv*np.exp(-we))
        def energy(v, metric=w):
            dd, aa, mm, ee, ll = ring_geometry(metric)
            pp = np.exp(-ee)*(dd@(expm(b*ll)@v)+.83)
            return float(np.sum((aa@N)*np.exp(ee)*kernel(pp)[0]))
        h = 2e-5
        fd_u = (energy(u+h*du)-energy(u-h*du))/(2*h)
        exact_u = float(grad_u@du)
        no_outer = float(wrong_grad@du)
        dp = -(avg@dw)*p+np.exp(-we)*(d@(dfilt@u))
        exact_metric = float(np.sum(weights*((avg@dw)*qv+2*fv*dp)))
        frozen_metric = float(np.sum(weights*((avg@dw)*qv-2*fv*(avg@dw)*p)))
        fd_metric = (energy(u,w+h*dw)-energy(u,w-h*dw))/(2*h)
        fd_s = (expm(b*ring_geometry(w+h*dw)[-1])-expm(b*ring_geometry(w-h*dw)[-1]))/(2*h)
        measure = np.diag(N*m)
        adjoint = np.linalg.solve(measure, filt.T@measure)
        lhs = float(du@measure@filt@u)
        rhs = float((adjoint@du)@measure@u)
        rows = dict(n=n,
                    first_variation_error=abs(fd_u-exact_u),
                    omitted_outer_error=abs(fd_u-no_outer),
                    frechet_relative_error=float(np.linalg.norm(fd_s-dfilt)/np.linalg.norm(dfilt)),
                    metric_variation_error=abs(fd_metric-exact_metric),
                    frozen_filter_metric_error=abs(fd_metric-frozen_metric),
                    weighted_adjoint_error=abs(lhs-rhs),
                    lapse_adjoint_difference=float(np.linalg.norm(adjoint-filt)),
                    dc_error=float(np.linalg.norm(filt@np.ones(n)-1)),
                    leaf_symmetry_error=float(np.linalg.norm(np.diag(m)@lap-lap.T@np.diag(m))))
        variation_rows.append(rows)
    check('nonlinear action variation includes outer adjoint',
          all(r['first_variation_error'] < 2e-8 and r['omitted_outer_error'] > 1e-3 for r in variation_rows),
          str([(r['n'],r['first_variation_error'],r['omitted_outer_error']) for r in variation_rows]))
    check('metric variation differentiates heat operator',
          all(r['frechet_relative_error'] < 2e-7 and r['metric_variation_error'] < 2e-8
              and r['frozen_filter_metric_error'] > 1e-4 for r in variation_rows),
          str([(r['n'],r['metric_variation_error'],r['frozen_filter_metric_error']) for r in variation_rows]))
    check('leaf and lapse-weighted measures are distinct',
          all(r['weighted_adjoint_error'] < 2e-12 and r['lapse_adjoint_difference'] > .01
              and r['dc_error'] < 2e-12 and r['leaf_symmetry_error'] < 2e-12 for r in variation_rows),
          'S is self-adjoint in sqrt(h), S^dagger_N=N^-1 S N in N sqrt(h); three grids')
    details['curved_leaf_variations'] = variation_rows

    # Exact endpoint/localization check on a nonconstant lapse. The multiplier
    # transport is backwards in diffusion z, NOT an initial-data propagator in time.
    terminal = -np.linalg.solve(measure, d.T@(2*weights*fv*np.exp(-we)))
    L0 = adjoint@terminal
    check('diffusion multiplier endpoint recovers weighted adjoint',
          np.linalg.norm(-measure@L0-grad_u) < 2e-12,
          'W(0)=U, L(b)=-Euler_q, L(0)=S^dagger_N L(b); no independent z-endpoint data')

    backgrounds = []
    for label,a0 in (('canonical',9.3619e-11),('alt',1.1279e-10)):
        yy = 2.32e-10/a0
        mu = -math.expm1(-yy)
        ll = 1+(yy-1)*math.exp(-yy)
        A = math.exp(-yy)/mu
        B = -yy*math.exp(-yy)/(mu*ll)
        ratio = 2*yy/(5*(3*ll-yy))
        # Common positive radial amplitude factored out.
        Q2 = -2*B/15
        trace = A+B/3
        identity = (15*A+5*B)*Q2+2*B*trace
        backgrounds.append(dict(label=label,a0=a0,y=yy,s=yy*mu,
                                A=A,B=B,Q2_over_D=ratio,
                                longitudinal=A+B,identity_residual=identity))
    check('separate external backgrounds and division-free identity',
          all(abs(r['identity_residual']) < 1e-14 for r in backgrounds), str(backgrounds))
    details['backgrounds'] = backgrounds

    # Counterexample for the expressly stated scalar-wave realization ONLY.
    # It does not certify the constrained metric response of this candidate.
    r,t,xi = 3.,.2,1.
    z=r*t/xi**2
    leaked = t/(2*np.pi*xi**2)**1.5*np.exp(-(r*r+t*t)/(2*xi*xi))*np.sinh(z)/z
    check('naive spatially filtered wave has spacelike support',
          r>t and leaked>0,
          f'G_ret(t={t},r={r},xi={xi})={leaked:.12g}; local wave value=0')
    details['naive_wave_counterexample'] = dict(t=t,r=r,xi=xi,response=float(leaked),
                                               implication='FAIL for this unconstrained scalar realization only')

    # Scalar ADM principal/frozen-background block. Sources are normalized
    # by 16 pi G/c^4. beta is the longitudinal shift. These expressions are
    # obtained from K_ij K^ij-K^2, not a DOF/rank label.
    k,C,rho,j,stress = sp.symbols('k C rho j stress', nonzero=True)
    psi,phi,U,beta = sp.symbols('psi phi U beta')
    pdot,pddot,bdot = sp.symbols('psi_dot psi_ddot beta_dot')
    L = -6*pdot**2+4*k*k*beta*pdot+2*k*k*psi**2-4*k*k*phi*psi+2*k*k*(U-phi)**2+2*k*k*C*U**2-rho*phi+j*beta-stress*psi
    solution_U = sp.solve(sp.diff(L,U),U)[0]
    reduced_dynamic = sp.simplify(L.subs(U,solution_U))
    shift_eq = sp.diff(reduced_dynamic,beta)
    lapse_eq = sp.diff(reduced_dynamic,phi)
    spatial_eq = sp.diff(reduced_dynamic,psi)+12*pddot-4*k*k*bdot
    shift_expected = 4*k*k*pdot+j
    # With j = rho_dot from conservation, psi = -rho/(4k^2)+integration_data.
    integration_data = sp.symbols('integration_data')
    psi_general = -rho/(4*k*k)+integration_data
    phi_general = sp.simplify(sp.solve(lapse_eq,phi)[0].subs(psi,psi_general))
    bdot_solution = sp.solve(spatial_eq,bdot)[0]
    bardeen = sp.simplify(phi+bdot_solution)
    check('clock/lapse principal block is not a causal certificate',
          sp.simplify(shift_eq-shift_expected)==0
          and sp.simplify(phi_general-integration_data*(C+1)/C)==0
          and sp.diff(bardeen,C)==0 and sp.diff(bardeen,phi)==0,
          f'shift={shift_eq}; phi={phi_general}; phi+beta_dot={bardeen}')
    details['principal_scalar_block'] = dict(
        action=str(L), eliminated_U=str(solution_U), shift_equation=str(shift_eq),
        lapse_equation=str(lapse_eq), spatial_equation=str(spatial_eq),
        lapse_with_conserved_source=str(phi_general), bardeen_potential=str(bardeen),
        qualification='Frozen-coefficient scalar truncation, C nonzero, k nonzero; background stresses and clock consistency still owed. No full DOF or ghost verdict.')

    # A clock restoring decoupling diagnostic; negative coefficient is a flag,
    # not a ghost proof before constraints/metric mixing are reduced.
    coeffs=[]
    for bkg in backgrounds:
        for orientation in (0.,1.):
            cval=math.exp(-.4**2)*(bkg['A']+bkg['B']*orientation)
            coeffs.append(dict(background=bkg['label'],cos2=orientation,
                               C=cval,clock_decoupling_coefficient=2*cval/(1+cval)))
    check('clock restoring diagnostic resolves sign by direction',
          all(row['clock_decoupling_coefficient'] > 0 if row['cos2']==0
              else row['clock_decoupling_coefficient'] < 0 for row in coeffs),str(coeffs))
    details['clock_decoupling_flags'] = coeffs
    check('zero-field tangent is outside regular linearization',
          sp.limit(y/s-1,y,0,dir='+') == sp.oo,
          'q is C^1 as a function of the gradient, but its gradient Hessian diverges at p=0')
    return records,details


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--require-closed-g03',action='store_true',
                        help='Return 2 when diagnostics pass but the covariant gate remains open.')
    args=parser.parse_args()
    start=time.time()
    timestamp=datetime.now(timezone.utc).isoformat()
    records,details=checks()
    failed=[r['name'] for r in records if not r['passed']]
    # These are explicit outstanding obligations, not asserted success flags.
    unresolved=['ordinary-matter realization of the conserved-source causal test',
                'original compact-domain response and admissible physical boundary/initial data',
                'zero-field and homogeneous branches']
    payload=dict(checks=records,details=details,failed_checks=failed,
                 outstanding_obligations=unresolved,
                 G03_status='FAIL' if failed else 'OPEN',
                 status_basis='A reproducible candidate and finite static/variation diagnostics do not certify causal feasibility.')
    output=HERE/'results.json'
    output.write_text(json.dumps(payload,indent=2)+'\n')
    inventory=HERE/'file_inventory.json'
    inventory.write_text(json.dumps([
        dict(path=str(p.relative_to(HERE)),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        for p in sorted(HERE.rglob('*')) if p.is_file()
        and p not in (inventory,HERE/'computation_manifest.json')
        and '__pycache__' not in p.parts],indent=2)+'\n')
    rc=1 if failed else (2 if args.require_closed_g03 else 0)
    root=HERE.parents[2]
    sources=[HERE/'g03_action_gate.py',HERE/'reproduce_handoff.py']
    for name in ('ACTION.md','REPORT.md'):
        if (HERE/name).exists(): sources.append(HERE/name)
    for name in ('STANDING.md','FRIED_CHICKEN_ROADMAP_2026-09-04.md',
                 'FABLE_HANDOFF_2026-09-04.md','g00_contract.md',
                 'g02_filtered_efe.py','g02b_tidal_identity_crosscheck.py',
                 'g02_manifest.json','g02_filtered_efe.out','g02b_tidal_identity_crosscheck.out',
                 'smoothed_onset_action_2026/REPORT.md','filtered_tidal_relation_2026/REPORT.md'):
        sources.append(HERE.parent/name)
    for name in ('f31c_ppn_k4_operators.py','f31c_ppn_k4_operators.out',
                 'f21_two_kernels_and_the_phantom_maximum.py',
                 'f21_two_kernels_and_the_phantom_maximum.out'):
        sources.append(root/'hunt_2026'/name)
    manifest=dict(schema_version=1,claim_id='G03-explicit-clock-heat-candidate-v1',
        repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                        dirty=bool(subprocess.check_output(['git','status','--porcelain'],text=True)),
                        dirty_state=subprocess.check_output(['git','status','--porcelain'],text=True).splitlines(),
                        source_hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}),
        command='python3 '+str((HERE/'g03_action_gate.py').relative_to(root))+(' --require-closed-g03' if args.require_closed_g03 else ''),
        environment=dict(software=[f'Python {platform.python_version()}',f'NumPy {np.__version__}',
                                   f'SciPy {scipy.__version__}',f'SymPy {sp.__version__}'],hardware=platform.platform()),
        mathematics=dict(assertion_tested='Explicit action weak-static algebra, finite nonlinear/metric variations, scoped causal obstructions',
                         coefficient_domain='SymPy exact expressions and float64 finite differences/root solves',
                         conventions='(-+++), x0=ct, Delta_h negative spectrum, heat time xi^2/2',
                         inputs=['curved periodic 1D finite-volume surrogates','two separate a0 backgrounds'],
                         bounds=dict(grids=[9,15,23],difference_step=2e-5),
                         non_claims=['covariant closure','physical DOF count','PPN','no ghost','causality','prior-art novelty']),
        randomness=dict(used=False,generator='',seed=None),
        run=dict(started_at=timestamp,runtime_seconds=time.time()-start,exit_status=rc),
        outputs=[dict(path=str(p.relative_to(root)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in (output,inventory)],
        checks=records,result=payload['G03_status'],residual_risks=unresolved)
    (HERE/'computation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Finite diagnostics: {len(records)-len(failed)}/{len(records)}; G03={payload["G03_status"]}; rc={rc}')
    return rc


if __name__=='__main__':
    raise SystemExit(main())
