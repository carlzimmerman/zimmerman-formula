#!/usr/bin/env python3
"""IC14: a local implicit-branch matter construction; full theory remains OPEN."""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as sp
import ic11_clock_pressure as vacuum


@lru_cache(None)
def build():
    model = vacuum.build()
    S, w, P = model['S'], model['w'], model['P']
    third = [sp.diff(P, S, S, w), sp.diff(P, S, w, w), sp.diff(P, w, w, w)]
    return dict(evaluate=model['evaluate'],
                third=sp.lambdify((S, w), third, 'mpmath', cse=True))


def branch_jets(S):
    """Implicit derivatives of the original root; no fitted coefficient table."""
    S = mp.mpf(S)
    if S <= 0:
        raise ValueError('Require S>0 on the inherited vacuum chart')
    w = vacuum.old.state(S)['w']
    F, Pw, PS, B, C, PSS = build()['evaluate'](S, w)
    PSSw, PSww, Pwww = build()['third'](S, w)
    if B == 0:
        raise ValueError('Original implicit vacuum root is singular')
    X = mp.exp(-2*S)/2
    wS = -C/B
    wSS = -(PSSw+2*PSww*wS+Pwww*wS*wS)/B
    z0 = mp.exp(2*w)
    zS, zSS = 2*z0*wS, 2*z0*(wSS+2*wS*wS)
    return dict(S=S, X=X, w0=w, z0=z0, F=F, FX=-PS/(2*X),
                FXX=(PSS-C*C/B+2*PS)/(4*X*X),
                z0X=-zS/(2*X), z0XX=(zSS+2*zS)/(4*X*X),
                original_constraint=Pw)


def raw(S, z, Y, t='0.1'):
    j = branch_jets(S)
    t, z, Y = map(mp.mpf, (t, z, Y))
    if t <= 0 or z <= 0:
        raise ValueError('Require t>0 and z>0')
    return j['F']-(z-j['z0'])**2/(2*t)+z*Y


def state(S, Y, t='0.1'):
    S, Y, t = map(mp.mpf, (S, Y, t))
    if S <= 0 or Y < 0 or t <= 0:
        raise ValueError('Require S>0, Y>=0, t>0')
    j = branch_jets(S)
    X, z0, zx, zxx = (j[k] for k in ('X', 'z0', 'z0X', 'z0XX'))
    z = z0+t*Y
    w = mp.log(z)/2
    pressure = j['F']+z0*Y+t*Y*Y/2
    LX, LY, LXX = j['FX']+zx*Y, z, j['FXX']+zxx*Y
    K = mp.matrix([[LX+2*X*LXX, 2*mp.sqrt(X*Y)*zx],
                   [2*mp.sqrt(X*Y)*zx, LY+2*Y*t]])
    D = mp.diag([LX, LY])
    M = mp.diag([LX+2*X*(LXX-zx*zx/t), z])
    q = mp.matrix([mp.sqrt(2*X)*zx/t, mp.sqrt(2*Y)])
    canonical = -1/t-(q.T*M**-1*q)[0] if mp.det(M) else mp.nan
    kinetic = list(mp.eigsy(K, eigvals_only=True))
    margin = list(mp.eigsy(K-D, eigvals_only=True))
    speeds = list(mp.eig(K**-1*D, left=False, right=False))
    rho = 2*X*LX+2*Y*LY-pressure
    H = mp.sqrt(rho/(3*mp.exp(-mp.mpf(1)/6))) if rho > 0 else mp.nan
    velocities = mp.matrix([mp.sqrt(2*X), mp.sqrt(2*Y)])
    vdot = -3*H*K**-1*D*velocities
    Xdot, Ydot = velocities[0]*vdot[0], velocities[1]*vdot[1]
    wdot = (zx*Xdot+t*Ydot)/(2*z)
    r = mp.exp(S-mp.mpf(1)/6)*H/z
    chart = bool(mp.exp(-S) < z < 1)
    plateau = bool(mp.mpf(3)/4 <= r*r <= mp.mpf(5)/4)
    healthy = bool(min(kinetic) > 0 and LX > 0 and LY > 0 and min(margin) >= -mp.mpf('1e-35'))
    return dict(**j, Y=Y, t=t, z=z, w=w, pressure=pressure, K=K, D=D,
                constraint=2*z*(-(z-z0)/t+Y), Lww=-4*z*z/t,
                canonical_auxiliary_schur_w=4*z*z*canonical,
                kinetic_eigenvalues=kinetic, cone_margin_eigenvalues=margin,
                speeds_squared=speeds, energy=rho, activation_r=r,
                physical_H=mp.exp(-w)*(H+wdot),
                original_chart_Y_upper=(1-z0)/t,
                inside_original_chart=chart, inside_eta_one=plateau,
                healthy_causal=healthy, admissible=chart and plateau and healthy)


def scan(samples=101, t='0.1'):
    if samples < 2:
        raise ValueError('Require at least two samples')
    t = mp.mpf(t)
    rows = [branch_jets(mp.mpf('.03')+mp.mpf('.17')*i/(samples-1)) for i in range(samples)]
    return dict(S_min='.03', S_max='.2', samples=samples, interval_certified=False,
                minimum_FX=min(r['FX'] for r in rows),
                minimum_FXX=min(r['FXX'] for r in rows),
                minimum_z0X=min(r['z0X'] for r in rows),
                minimum_z0XX=min(r['z0XX'] for r in rows),
                maximum_required_t=max(r['z0X']**2/r['FXX'] for r in rows),
                minimum_cone_determinant_at_Y_zero=min(t*r['FXX']-r['z0X']**2 for r in rows))


def plateau_boundary(S, t='0.1'):
    """First positive algebraic eta-boundary crossing at fixed S, not evolution."""
    j = branch_jets(S)
    t, S = mp.mpf(t), mp.mpf(S)
    X, z0 = j['X'], j['z0']
    a, b = 2*X*j['FX']-j['F'], 2*X*j['z0X']+z0
    prefactor = mp.exp(2*S-mp.mpf(1)/3)/(3*mp.exp(-mp.mpf(1)/6))
    roots = []
    for target in (mp.mpf(3)/4, mp.mpf(5)/4):
        A = prefactor*3*t/2-target*t*t
        B = prefactor*b-2*target*z0*t
        C = prefactor*a-target*z0*z0
        discriminant = B*B-4*A*C
        if discriminant >= 0:
            candidates = [-C/B] if A == 0 else [(-B+sign*mp.sqrt(discriminant))/(2*A) for sign in (-1, 1)]
            roots.extend((root, target) for root in candidates if root > 0)
    if not roots:
        raise ValueError('No positive activation crossing located')
    Y, target = min(roots)
    return dict(**state(S, Y, t), boundary_r_squared=target)


def identities():
    z, z0, Y, t, F, w = sp.symbols('z z0 Y t F w', real=True)
    L = F-(z-z0)**2/(2*t)+z*Y
    root = {z: z0+t*Y}
    wL = L.subs(z, sp.exp(2*w))
    return dict(auxiliary_equation=sp.simplify(sp.diff(L,z).subs(root)),
                eliminated_pressure=sp.simplify(L.subs(root)-(F+z0*Y+t*Y**2/2)),
                vacuum_pressure=sp.simplify(L.subs({z:z0,Y:0})-F),
                root_w_curvature=sp.simplify(sp.diff(wL,w,2).subs(sp.exp(2*w),z).subs(root)+4*(z0+t*Y)**2/t))


def boosted_characteristics(S, Y, boost, t='0.1'):
    """Frozen local principal symbol, wave vector parallel to matter boost.

    This is not a homogeneous FLRW solution or a checked activated-action state.
    Y is the invariant matter kinetic argument, not its clock-frame time part.
    """
    Y, boost, t = map(mp.mpf, (Y, boost, t))
    if Y < 0 or t <= 0 or abs(boost) >= 1:
        raise ValueError('Require Y>=0, t>0 and |boost|<1')
    j = branch_jets(S)
    X, zx = j['X'], j['z0X']
    LX, LY, hxx = j['FX']+Y*zx, j['z0']+t*Y, j['FXX']+Y*j['z0XX']
    gamma2 = 1/(1-boost*boost)
    d, e = 2*Y*gamma2*t, 4*X*Y*gamma2*zx*zx
    a0, a2 = LX, -(LX+2*X*hxx)
    b0, b1, b2 = LY-d*boost*boost, 2*d*boost, -(LY+d)
    coefficients = [a2*b2-e, a2*b1+2*e*boost,
                    a0*b2+a2*b0-e*boost*boost, a0*b1, a0*b0]
    roots = mp.polyroots(coefficients, maxsteps=1000, error=False)
    roots = sorted(roots, key=lambda c:(mp.re(c),mp.im(c)))
    residuals = []
    for c in roots:
        dots = mp.matrix([mp.sqrt(2*X)*c, mp.sqrt(2*Y*gamma2)*(c-boost)])
        principal = mp.matrix([[LX*(1-c*c)-hxx*dots[0]**2, -zx*dots[0]*dots[1]],
                               [-zx*dots[0]*dots[1], LY*(1-c*c)-t*dots[1]**2]])
        residuals.append(abs(mp.det(principal)))
    return dict(S=mp.mpf(S), Y=Y, boost=boost, roots=roots,
                maximum_principal_residual=max(residuals),
                real_subluminal=all(abs(mp.im(c)) < mp.mpf('1e-35') and abs(mp.re(c)) <= 1 for c in roots),
                physical_activation_checked=False)


def report():
    mp.mp.dps = 50
    fields = ('S','Y','w','energy','activation_r','physical_H','original_chart_Y_upper',
              'speeds_squared','inside_original_chart','inside_eta_one','healthy_causal')
    compact = lambda bg: {k:bg[k] for k in fields}
    return dict(candidate='IC14 local conformal-square matter construction', full_theory='OPEN',
                t='0.1', exact_checks={k:v == 0 for k,v in identities().items()},
                finite_scan=scan(),
                samples=[compact(state(S,Y)) for S in ('.03','.05','.1','.2') for Y in ('0','.0001','.01','.1')],
                fixed_S_activation_boundaries=[compact(plateau_boundary(S)) for S in ('.03','.05','.1','.2')],
                boosted_principal_controls=[boosted_characteristics('.1','.0001',v) for v in ('.5','.9')],
                nonclaims=['Implicit vacuum branch coefficients define a local action chart only',
                           'Finite samples do not certify a continuous X interval',
                           'All-Y algebra does not extend the original u chart or eta plateau',
                           'Aligned homogeneous massless matter only; no transition, PPN, galaxies, or strong-coupling certificate'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure', action='store_true')
    args = parser.parse_args()
    print(json.dumps(report(), indent=2, default=lambda value:mp.nstr(value,24)))
    raise SystemExit(2 if args.require_full_closure else 0)
