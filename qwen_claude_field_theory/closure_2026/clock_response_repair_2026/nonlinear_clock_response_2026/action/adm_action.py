#!/usr/bin/env python3
"""Unreduced plane ADM action through order four and nonlinear constraints.

The generator accepts arbitrary spatial jets at every perturbation order.
The exported witness uses one first-order cosine scalar / sine shift mode;
variation precedes projection, so zero/2k and 1k/3k sources survive.  It does
not integrate out the lapse, clock, metric, matter, or generated harmonics.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from math import comb
from pathlib import Path
import sys

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
ARCHIVE = BASE/'inhomogeneous_charge_2026/exterior/run_001/result.json'


class Jet:
    """Truncated ordinary epsilon coefficients (no factorial convention)."""
    __array_priority__ = 10000

    def __init__(self, coefficients):
        self.c = list(coefficients)
        self.order = len(self.c)-1
        self.exact = any(isinstance(x, sp.Basic) for x in self.c)
        if self.exact:
            self.c = [sp.sympify(x) for x in self.c]

    def coerce(self, other):
        if isinstance(other, Jet):
            if other.order != self.order:
                raise ValueError('Incompatible truncation orders')
            return other
        return Jet([other]+[0]*self.order)

    def __add__(self, other):
        other = self.coerce(other)
        return Jet([x+y for x, y in zip(self.c, other.c)])

    __radd__ = __add__

    def __neg__(self):
        return Jet([-x for x in self.c])

    def __sub__(self, other):
        return self+-self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other)+-self

    def __mul__(self, other):
        other = self.coerce(other)
        return Jet([sum(self.c[j]*other.c[i-j] for j in range(i+1))
                    for i in range(self.order+1)])

    __rmul__ = __mul__

    def reciprocal(self):
        numerator = sp.S.One if self.exact else 1.
        out = [numerator/self.c[0]]
        for i in range(1, self.order+1):
            out.append(-sum(self.c[j]*out[i-j] for j in range(1, i+1))/self.c[0])
        return Jet(out)

    def __truediv__(self, other):
        return self*self.coerce(other).reciprocal()

    def __rtruediv__(self, other):
        return self.coerce(other)*self.reciprocal()

    def __pow__(self, power):
        if not isinstance(power, int):
            raise TypeError('Only integer powers are supported')
        if power < 0:
            return self.reciprocal()**(-power)
        out = self.coerce(1)
        for _ in range(power):
            out = out*self
        return out

    def exp(self):
        out = [sp.exp(self.c[0]) if self.exact else np.exp(self.c[0])]
        for i in range(1, self.order+1):
            out.append(sum(j*self.c[j]*out[i-j] for j in range(1, i+1))/i)
        return Jet(out)


def exponential(value):
    if isinstance(value, Jet):
        return value.exp()
    return sp.exp(value) if isinstance(value, sp.Basic) else np.exp(value)


def geometry(f, bg):
    """Coordinate shift b=N^x; Ax=partial_x log A, Bx=partial_x log B."""
    N = 1+f['n']
    vol = bg['a']**3*exponential(3*f['z'])
    invA2 = exponential(-2*f['z']-4*f['e'])/bg['a']**2
    Ax, Bx = f['zx']+2*f['ex'], f['zx']-f['ex']
    Kx = (bg['H']+f['zd']+2*f['ed']-f['b']*Ax-f['bx'])/N
    Ky = (bg['H']+f['zd']-f['ed']-f['b']*Bx)/N
    Q = (bg['q']+f['sd']-f['b']*f['sx'])/N
    Y = invA2*f['sx']**2
    Yx = invA2*(2*f['sx']*f['sxx']-2*Ax*f['sx']**2)
    lap = invA2*(f['sxx']+(2*Bx-Ax)*f['sx'])
    gradY = invA2*f['sx']*Yx
    R3 = invA2*(-4*(f['zxx']-f['exx'])-6*Bx**2+4*Ax*Bx)
    RQ = (bg['qr']+f['rd']-f['b']*f['rx'])/N
    TQ = (1+f['td']-f['b']*f['tx'])/N
    return dict(N=N, vol=vol, invA2=invA2, Ax=Ax, Bx=Bx, Kx=Kx,
                Ky=Ky, K=Kx+2*Ky, Q=Q, Y=Y, Yx=Yx, lap=lap,
                gradY=gradY, R3=R3, X=Q**2-Y, RQ=RQ, TQ=TQ,
                Xr=RQ**2-invA2*f['rx']**2, Xd=TQ**2-invA2*f['tx']**2)


def taylor_constitutive(X, Y, bg):
    """Jets evaluated at (physical Q^2,0,tau); no new coefficient functions."""
    dX = X-bg['q']**2
    P = bg['P']+bg['PX']*dX+bg['PXX']*dX**2/2+bg['PXXX']*dX**3/6+bg['PXXXX']*dX**4/24
    PX = bg['PX']+bg['PXX']*dX+bg['PXXX']*dX**2/2+bg['PXXXX']*dX**3/6
    W = bg['W']+bg['WY']*Y+bg['WYY']*Y**2/2
    return P, PX, W


def action_pieces(f, bg, constitutive=taylor_constitutive):
    g = geometry(f, bg)
    N, v, Q, Kx, Ky, K, Y = (g[x] for x in ('N','vol','Q','Kx','Ky','K','Y'))
    P, _, W = constitutive(g['X'], Y, bg)
    # The last term, omitted in S2-only bridge code, starts at epsilon^3.
    cubic = bg['gamma']*(-2*Q**3*K/3+2*Q*Kx*Y+2*Q**2*g['lap']+g['gradY'])
    return dict(einstein=N*v*bg['M2']*(-4*Kx*Ky-2*Ky**2+g['R3'])/2,
                clock=N*v*(P-bg['V']+cubic)+v*bg['sbar']*W,
                radiation=N*v*bg['Cr']*g['Xr']**2,
                dust=N*v*(bg['rho']+f['drho'])*(g['Xd']-1)/2,
                lambda_term=-N*v*bg['M2']*bg['Lambda'])


def constraints(f, bg, constitutive=taylor_constitutive):
    """Exact delta S/delta N and delta S/delta b, including density factor.

    Independent verification differentiates the raw action and differentiates
    its b_x momentum spectrally. This implementation is a compact analytic
    variation, and is valid before substitution of Fourier modes.
    """
    g = geometry(f, bg)
    N,v,Q,Kx,Ky,K,Y,Ax,Bx = (g[x] for x in
        ('N','vol','Q','Kx','Ky','K','Y','Ax','Bx'))
    P, PX, _ = constitutive(g['X'], Y, bg)
    M, gamma = bg['M2'], bg['gamma']
    dens = bg['rho']+f['drho']
    lapse = v*(M*(g['R3']+4*Kx*Ky+2*Ky**2)/2+P-bg['V']-M*bg['Lambda']-2*Q**2*PX
        +gamma*(2*Q**3*K-2*Q*Kx*Y-2*Q**2*g['lap']+g['gradY'])
        +bg['Cr']*(g['Xr']**2-4*g['RQ']**2*g['Xr'])
        +dens*((g['Xd']-1)/2-g['TQ']**2))
    pKx = -2*M*Ky+gamma*(-2*Q**3/3+2*Q*Y)
    pKy = -2*M*(Kx+Ky)-4*gamma*Q**3/3
    pQ = 2*Q*PX+gamma*(-2*Q**2*K+2*Kx*Y+4*Q*g['lap'])
    Kyx = (f['zdx']-f['edx']-f['bx']*Bx-f['b']*(f['zxx']-f['exx'])-Ky*f['nx'])/N
    Qx = (f['sdx']-f['bx']*f['sx']-f['b']*f['sxx']-Q*f['nx'])/N
    pKxx = -2*M*Kyx+gamma*(-2*Q**2*Qx+2*Qx*Y+2*Q*g['Yx'])
    shift = v*(3*f['zx']*pKx+pKxx-pKx*Ax-pKy*Bx-pQ*f['sx']
               -4*bg['Cr']*g['RQ']*g['Xr']*f['rx']-dens*g['TQ']*f['tx'])
    return dict(lapse=lapse, shift=shift)


FIELD_JETS = {'z':('z','zx','zxx'), 'e':('e','ex','exx'),
              'zd':('zd','zdx'), 'ed':('ed','edx'),
              'n':('n','nx'), 'b':('b','bx'),
              'sigma':('sigma','sx','sxx'), 'sd':('sd','sdx'),
              'rad':('rad','rx'), 'radd':('rd',),
              'theta':('theta','tx'), 'td':('td',), 'drho':('drho',)}


def harmonic_fields(amplitudes, k, cosine, sine, order=None):
    """First-order witness; use arbitrary Jet-valued f with action_pieces for
    multi-order/multi-harmonic fields and induced response insertions.
    """
    out = {}
    for amplitude, names in FIELD_JETS.items():
        A = amplitudes[amplitude]
        even, odd = (sine, cosine) if amplitude == 'b' else (cosine, -sine)
        for derivative, name in enumerate(names):
            value = A*(even if derivative == 0 else k*odd if derivative == 1 else -k*k*even)
            out[name] = Jet([0,value]+[0]*(order-1)) if order is not None else value
    return out


@lru_cache(maxsize=4)
def symbolic(order=4):
    names = 'a H q sbar M2 gamma P PX PXX PXXX PXXXX V W WY WYY Cr qr rho Lambda k'
    bg = dict(zip(names.split(), sp.symbols(names, real=True)))
    amplitudes = {name:sp.Symbol(name, real=True) for name in FIELD_JETS}
    c, sn = sp.symbols('cosine sine', real=True)
    f = harmonic_fields(amplitudes, bg['k'], c, sn, order)
    pieces = {key:[sp.expand(x) for x in value.c]
              for key,value in action_pieces(f,bg).items()}
    con = {key:[sp.expand(x) for x in value.c[:min(order,3)+1]]
           for key,value in constraints(f,bg).items()}
    return dict(bg=bg, amplitudes=amplitudes, cosine=c, sine=sn,
                pieces=pieces, constraints=con)


def fourier_polynomial(expr, cosine, sine):
    """Exact complex Laurent coefficients: cos=(u+u^-1)/2, sin=(u-u^-1)/2i."""
    out = {}
    for (ic, ins), coefficient in sp.Poly(sp.expand(expr), cosine, sine).terms():
        for j in range(ic+1):
            for l in range(ins+1):
                mode = ic+ins-2*j-2*l
                weight = sp.Rational(comb(ic,j)*comb(ins,l)*(-1)**l, 2**(ic+ins))/sp.I**ins
                out[mode] = out.get(mode, 0)+coefficient*weight
    return {m:sp.expand(v) for m,v in sorted(out.items()) if sp.expand(v) != 0}


def real_harmonics(expr, cosine, sine):
    coeff = fourier_polynomial(expr, cosine, sine)
    out = {'constant':coeff.get(0,sp.S.Zero)}
    for m in sorted(x for x in coeff if x > 0):
        co = sp.expand(coeff.get(m,0)+coeff.get(-m,0))
        si = sp.expand(sp.I*(coeff.get(m,0)-coeff.get(-m,0)))
        if co != 0: out['cos'+str(m)] = co
        if si != 0: out['sin'+str(m)] = si
    return out


def quadratic_regression():
    path = BASE/'cosmological_bridge_2026/derive.py'
    spec = importlib.util.spec_from_file_location('original_bridge_for_regression',path)
    bridge = importlib.util.module_from_spec(spec); spec.loader.exec_module(bridge)
    original = bridge.construct()
    d = symbolic(2)
    aliases = {d['amplitudes']['sd']:original['s']['sd'],
               d['amplitudes']['td']:original['s']['td']}
    answer = {}
    for key, poly in d['pieces'].items():
        target = 'lambda' if key == 'lambda_term' else key
        averaged = fourier_polynomial(poly[2],d['cosine'],d['sine']).get(0,0)
        answer[target] = sp.expand(averaged.subs(aliases)-original[target]) == 0
    return answer


def series_check():
    x,u,v = sp.symbols('epsilon u v')
    j = Jet([sp.S.One,u,v,0,0])
    calculated = (j.exp()/j**3).c
    raw = sp.exp(1+u*x+v*x*x)/(1+u*x+v*x*x)**3
    return all(sp.simplify(calculated[m]-sp.diff(raw,x,m).subs(x,0)/sp.factorial(m)) == 0
               for m in range(5))


def covariant_braiding_check():
    """Independent Box(chi) divergence, arbitrary plane lapse and shift.

    Boundary: B^t=-gamma vol(Q^3/3-QY),
    B^x=gamma vol b(Q^3/3-QY)-gamma N vol h^xx chi_x(Q^2+Y).
    The compatibility relation is chi_t=NQ+b chi_x.
    """
    x,t = sp.symbols('x t',real=True)
    alpha,beta,N,b,Q,chi = [sp.Function(name)(x,t) for name in
                          ('alpha','beta','N','shift','Q','chi')]
    gamma = sp.Symbol('gamma',real=True)
    z,e = (alpha+2*beta)/3,(alpha-beta)/3
    f = {name:sp.S.Zero for names in FIELD_JETS.values() for name in names}
    for field,expr in [('z',z),('e',e)]:
        f.update({field:expr,field+'x':sp.diff(expr,x),field+'xx':sp.diff(expr,x,2),
                  field+'d':sp.diff(expr,t),field+'dx':sp.diff(expr,t,x)})
    f.update(n=N-1,nx=sp.diff(N,x),b=b,bx=sp.diff(b,x),
             sx=sp.diff(chi,x),sxx=sp.diff(chi,x,2),sd=N*Q+b*sp.diff(chi,x))
    bg = {name:sp.S.Zero for name in 'H q P PX PXX PXXX PXXXX V W WY WYY Cr qr rho Lambda M2 sbar'.split()}
    bg.update(a=sp.S.One,gamma=gamma)
    adm = action_pieces(f,bg)['clock']
    vol = sp.exp(alpha+2*beta)
    invA2 = sp.exp(-2*alpha)
    Y = invA2*sp.diff(chi,x)**2
    cov = gamma*(Q**2-Y)*(-sp.diff(vol*Q,t)+
               sp.diff(vol*b*Q+N*vol*invA2*sp.diff(chi,x),x))
    F = gamma*(Q**3/3-Q*Y)
    Bt = -vol*F
    Bx = vol*b*F-gamma*N*vol*invA2*sp.diff(chi,x)*(Q**2+Y)
    residual = sp.expand(cov-adm-sp.diff(Bt,t)-sp.diff(Bx,x))
    residual = residual.subs(sp.diff(chi,t,x),sp.diff(N*Q+b*sp.diff(chi,x),x)).doit()
    return sp.simplify(residual) == 0


@lru_cache(maxsize=1)
def sourced_snapshot():
    sys.path.insert(0,str(BASE/'nonlinear_evolution_2026'))
    from constitutive import Model
    row = json.loads(ARCHIVE.read_text())['rows'][0]
    model = Model(.1,gamma=row['gamma'])
    jets = model.jets(row['tau'],row['physical_Q']**2,0.)
    ref = model.background(row['tau'])
    denominator = ref['U']-2*ref['d']*row['physical_Q']**2
    pxxx = 8*ref['U']*ref['d']**3/denominator**3
    pxxxx = 48*ref['U']*ref['d']**4/denominator**4
    bg = dict(a=row['a'], H=row['H'], q=row['physical_Q'], sbar=row['clock_rate'],
              M2=1., gamma=row['gamma'], Lambda=.7, Cr=1., qr=(.01/3.)**.25, rho=.001,
              P=jets['P'],PX=jets['P_X'],PXX=jets['P_XX'],PXXX=pxxx,PXXXX=pxxxx,
              V=jets['V'],W=jets['W'],WY=jets['W_Y'],WYY=jets['W_YY'])
    # Raw exact constitutive evaluation bypasses only the real-domain guard for
    # complex-step differentiation; positivity is checked on real samples.
    def exact(X,Y,_):
        U,d,qb,Hb,ell = (ref[x] for x in ('U','d','q','H','ell'))
        P = -U*np.log((U-2*d*X)/(U-2*d*qb*qb))/2+3*model.gamma*qb*Hb*(X-qb*qb)
        PX = U*d/(U-2*d*X)+3*model.gamma*qb*Hb
        W = U+2*d*ell*(np.sqrt(1+Y/ell)-1)-2*model.gamma*qb*qb*ref['qdot']
        return P,PX,W
    assert abs(exact(bg['q']**2,0,bg)[0]-bg['P']) < 1e-14
    return model,row,ref,bg,exact


def spectral_dx(values,k):
    modes = np.fft.fftfreq(len(values),1/len(values))
    return np.fft.ifft(1j*k*modes*np.fft.fft(values)).real


@lru_cache(maxsize=1)
def numerical_checks():
    model,row,ref,bg,exact = sourced_snapshot()
    points,k = 512,1.7
    phase = 2*np.pi*np.arange(points)/points
    c,sn = np.cos(phase),np.sin(phase)
    amplitudes = dict(z=.021,e=-.013,zd=.017,ed=.019,n=.023,b=.029,
                      sigma=.11,sd=.037,rad=.031,radd=.043,theta=.047,td=.053,drho=.00007)
    f1 = harmonic_fields(amplitudes,k,c,sn)
    fj = harmonic_fields(amplitudes,k,c,sn,4)
    con = constraints(fj,bg)
    Lj = sum(action_pieces(fj,bg).values()).c
    def at(eps): return {key:eps*value for key,value in f1.items()}
    def L(f): return sum(action_pieces(f,bg,exact).values())
    testfield = at(.03)
    h = 1e-28
    independent = {}
    for key in ('n','b','bx'):
        altered = dict(testfield); altered[key] = altered[key].astype(complex)+1j*h
        independent[key] = np.imag(L(altered))/h
    independent['b'] -= spectral_dx(independent['bx'],k)
    computed = constraints(testfield,bg,exact)
    variation_error = max(float(np.max(abs(computed[key]-independent[other])))
                          for key,other in [('lapse','n'),('shift','b')])
    rows = []
    # Symmetric amplitude differences cancel opposite parity. Subtracting the
    # full local lower-order coefficient tests the unaveraged residual.
    for eps in (.04,.02,.01):
        plus,minus = constraints(at(eps),bg,exact),constraints(at(-eps),bg,exact)
        entry = dict(amplitude=eps)
        for order in (2,3):
            errors = []
            for key in con:
                if order == 2:
                    inferred = ((plus[key]+minus[key])/2-con[key].c[0])/eps**2
                else:
                    inferred = ((plus[key]-minus[key])/2-eps*con[key].c[1])/eps**3
                target = con[key].c[order]
                errors.append(np.max(abs(inferred-target))/max(np.max(abs(target)),1e-30))
            entry['source'+str(order)+'_relative_error'] = float(max(errors))
        inferred4 = ((L(at(eps))+L(at(-eps)))/2-Lj[0]-eps**2*Lj[2])/eps**4
        entry['action4_subtraction_relative_error'] = float(np.max(abs(inferred4-Lj[4]))/np.max(abs(Lj[4])))
        for field in (at(eps),at(-eps)):
            g = geometry(field,bg)
            model.jets(row['tau'],g['X'],g['Y'])
        rows.append(entry)
    # Cauchy's coefficient formula uses a larger complex radius, avoiding
    # cancellation of the background and quadratic terms divided by eps^4.
    # This is independent of the truncated-series algebra and uses the exact
    # unchanged logarithm/square-root functions at all contour nodes.
    contour = []
    for radius,nodes in ((.15,32),(.15,64),(.1,64)):
        angles = 2*np.pi*np.arange(nodes)/nodes
        inferred = sum(L(at(radius*np.exp(1j*angle)))*np.exp(-4j*angle)
                       for angle in angles)/(nodes*radius**4)
        error = float(np.max(abs(inferred-Lj[4]))/np.max(abs(Lj[4])))
        contour.append(dict(radius=radius,nodes=nodes,relative_error=error))
    d = symbolic(3)
    forbidden = 0
    for order in (2,3):
        allowed = {0,-2,2} if order == 2 else {-3,-1,1,3}
        for poly in d['constraints'].values():
            coeff = fourier_polynomial(poly[order],d['cosine'],d['sine'])
            forbidden += sum(1 for mode in coeff if mode not in allowed)
    return dict(independent_variation_max_error=variation_error,convergence=rows,
                **{key:value for key,value in rows[-1].items() if key != 'amplitude'},
                action4_relative_error=max(x['relative_error'] for x in contour),
                action4_cauchy_controls=contour,
                physical_Q_qbar_separation=abs(bg['q']-ref['q']),
                gamma=bg['gamma'],forbidden_harmonics_max=forbidden,
                snapshot=dict(physical_Q=bg['q'],reference_qbar=ref['q'],sbar=bg['sbar'],
                              rho_dust=bg['rho'],rho_rad=.01,a=bg['a'],H=bg['H']),
                amplitudes=amplitudes,k=k,points=points)


@lru_cache(maxsize=1)
def linear_seed_sources():
    """A valid first-order seed from the sourced six-state action system.

    Choose sigma=1 and deltaQ so sigma_dot=H sigma. Amplitude epsilon
    subsequently scales the entire perturbation, including metric/matter.
    Only first-order constraints are solved here; C2/C3 are sources awaiting
    the induced second-/third-order response fields.
    """
    sys.path.insert(0,str(BASE/'cosmological_bridge_2026'))
    from transfer_evolve import Background, mode_system
    background = Background(.01)
    v,_,background_constraint,_ = background.at(0.)
    k = 3.
    A,_,nrow,zrow,brow,Jrow = mode_system(v,k)
    u = np.zeros(6)
    u[0] = 1.
    u[1] = (v['H']-A[0,0])/A[0,1]
    ud = A@u
    n,z,b = float(nrow@u),float(zrow@u),float(brow@u)
    zd = v['H']*n-float(Jrow@u)/(2*v['M2'])
    amplitudes = dict(z=z,e=0.,zd=zd,ed=0.,n=n,b=b,sigma=u[0],sd=ud[0],
                      rad=u[2],radd=ud[2],theta=u[4],td=ud[4],drho=u[5])
    ref = background.model.background(0.)
    jets = background.model.jets(0.,v['q']**2,0.)
    denominator = ref['U']-2*ref['d']*v['q']**2
    bg = dict(v,PXXXX=48*ref['U']*ref['d']**4/denominator**4,WYY=jets['W_YY'])
    phase = 2*np.pi*np.arange(512)/512
    f = harmonic_fields(amplitudes,k,np.cos(phase),np.sin(phase),3)
    coefficients = constraints(f,bg)
    linear_max = max(float(np.max(abs(value.c[1]))) for value in coefficients.values())
    dq = ud[0]-v['q']*n
    dk = 3*zd-3*v['H']*n-k*b
    clock = 2*v['q']*v['PXt']*dq-v['W']*dk-2*v['q']*v['WY']*k*k*u[0]/v['a']**2
    values = dict(bg,**amplitudes,k=k)
    symbolic_data = symbolic(3)
    sources,projection_error = {},0.
    for field,poly in symbolic_data['constraints'].items():
        sources[field] = {}
        for order in (1,2,3):
            harmonics = real_harmonics(poly[order],symbolic_data['cosine'],symbolic_data['sine'])
            answer = {}
            for mode,expression in harmonics.items():
                analytic = float(expression.subs({x:values[str(x)] for x in expression.free_symbols}))
                sample = coefficients[field].c[order]
                if mode == 'constant': projected = np.mean(sample)
                elif mode.startswith('cos'): projected = 2*np.mean(sample*np.cos(int(mode[3:])*phase))
                else: projected = 2*np.mean(sample*np.sin(int(mode[3:])*phase))
                projection_error = max(projection_error,abs(float(projected)-analytic))
                answer[mode] = analytic
            sources[field][str(order)] = answer
    # Same physical initial background as sourced_snapshot, checked explicitly;
    # exact constitutive amplitude controls never replace Q by reference qbar.
    _,_,_,archived_bg,exact = sourced_snapshot()
    snapshot_error = max(abs(bg[name]-archived_bg[name]) for name in
                         ('a','H','q','sbar','PX','PXX','W','WY','rho','qr'))
    assert snapshot_error < 1e-11
    convergence = []
    linear = {name:value.c[1] for name,value in coefficients.items()}
    constant = {name:value.c[0] for name,value in coefficients.items()}
    first = harmonic_fields(amplitudes,k,np.cos(phase),np.sin(phase))
    for eps in (.002,.001,.0005):
        plus = constraints({name:eps*value for name,value in first.items()},bg,exact)
        minus = constraints({name:-eps*value for name,value in first.items()},bg,exact)
        errors = {}
        for order in (2,3):
            maximum = 0.
            for field in coefficients:
                inferred = ((plus[field]+minus[field])/2-constant[field])/eps**2 if order == 2 else (
                    (plus[field]-minus[field])/2-eps*linear[field])/eps**3
                target = coefficients[field].c[order]
                maximum = max(maximum,float(np.max(abs(inferred-target))/np.max(abs(target))))
            errors[str(order)] = maximum
        convergence.append(dict(epsilon=eps,source_relative_errors=errors))
    assert linear_max < 1e-11 and abs(clock) < 1e-11
    assert max(convergence[-1]['source_relative_errors'].values()) < 3e-4
    return dict(seed='sigma=1, sigma_dot=H sigma; other initial physical state entries zero except solved deltaQ',
                state_order=['sigma','deltaQ','rad','deltaQr','theta','drho'],state=u.tolist(),
                amplitudes={key:float(value) for key,value in amplitudes.items()},
                linear_lapse_shift_max=linear_max,clock_linear_residual=abs(float(clock)),
                background_constraint_max=float(max(abs(background_constraint[:2]))),
                source_projection_max_error=projection_error,sources=sources,
                convergence=convergence,k=k,physical_Q=v['q'],sbar=v['sbar'],gamma=v['gamma'],
                archived_snapshot_max_error=snapshot_error,
                interpretation='Linear constraints hold. The nonzero order-two and order-three residuals require induced responses; these are not completed nonlinear constraint solutions.')


def run():
    d = symbolic(4)
    actions = {}
    for order in (2,3,4):
        expr = sum(piece[order] for piece in d['pieces'].values())
        actions['S'+str(order)] = {key:str(sp.factor(value)) for key,value in
            real_harmonics(expr,d['cosine'],d['sine']).items()}
    sources = {key:{str(order):{mode:str(sp.factor(value)) for mode,value in
               real_harmonics(poly[order],d['cosine'],d['sine']).items()}
               for order in (1,2,3)} for key,poly in d['constraints'].items()}
    checks = dict(series_independent_differentiation=series_check(),
                  covariant_braiding_with_shift=covariant_braiding_check(),
                  quadratic_regression=quadratic_regression(),numerical=numerical_checks(),
                  linear_constraint_seed=linear_seed_sources())
    assert checks['series_independent_differentiation']
    assert checks['covariant_braiding_with_shift']
    assert all(checks['quadratic_regression'].values())
    n = checks['numerical']
    assert n['independent_variation_max_error'] < 2e-10
    assert max(n[x] for x in ('source2_relative_error','source3_relative_error','action4_relative_error')) < 3e-4
    assert n['forbidden_harmonics_max'] == 0
    return dict(scope='Unreduced S2/S3/S4, full plane ADM fields, matter, local lapse/shift sources; no nonlinear clock solution or attractor',
                coefficient_convention='[epsilon^r] local density; harmonic cos(m k x)/sin(m k x); no factorial',
                action_harmonics=actions,constraint_source_harmonics=sources,checks=checks,
                full_theory_status='OPEN',
                next_required='Insert response fields at orders 2 and 3; solve generated zero/2k metric, scalar, matter and preserved clock equations, then include their exchange in S4')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file',type=Path,required=True)
    args = parser.parse_args()
    result = run()
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],full_theory_status='OPEN'),indent=2))
