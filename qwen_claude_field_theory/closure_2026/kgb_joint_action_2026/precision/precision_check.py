#!/usr/bin/env python3
"""Independent arbitrary-precision two-mass joint-action local check.

Derive P_X directly by differentiating H1-H2, then differentiate that determined
function along the full flow for P_XX. No complex-step or root coefficients a,b
are used in this construction. Original action principal/stress expressions are
the sole imported mathematical expressions.
"""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

CLOSURE = Path(__file__).resolve().parents[2]
SOURCE = CLOSURE/'ticking_kgb_inverse_2026/kgb_inverse.py'


@lru_cache(None)
def evaluator():
    spec = importlib.util.spec_from_file_location('joint_precision_action', SOURCE)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    a = model.principal_template()
    args = [a['m'],a['G1'],a['G2'],a['P'],a['P1'],a['P2']]
    args += list(a['v'])+[a['H'][i,j] for i in range(4) for j in range(i,4)]
    return s.lambdify(args, (a['M'],a['T']), 'mpmath', cse=True)


def geometry(eps, X, y, U, P):
    radius = lambda v: eps/mp.sqrt(v*(-mp.expm1(-v)))
    lapse_slope = lambda v: v/(1-2*radius(v)*v)
    r = radius(y)
    ry = mp.diff(radius, y)
    g = lapse_slope(y)
    gr = mp.diff(lapse_slope, y)/ry
    T = 1+2*r*g
    B = T/(1+r*r*P)
    # Direct derivative holding P fixed, with no residual-density closed form.
    fixed_pressure_B = lambda v: (1+2*radius(v)*lapse_slope(v))/(1+radius(v)**2*P)
    Br_partial = mp.diff(fixed_pressure_B, y)/ry
    E0 = (1-1/B)/r**2+Br_partial/(B**2*r)+P
    Z = U/X-r*g
    W = Z*E0/(r*(1+Z/T))
    H = mp.sqrt(B*U)*r/(2*X*Z)
    return dict(eps=eps,X=X,y=y,U=U,P=P,r=r,ry=ry,g=g,gr=gr,T=T,
                B=B,Br_partial=Br_partial,E0=E0,Z=Z,W=W,H=H)


def Hvalue(eps, X, y, U, P):
    # Keep the differentiated function minimal and independent of W or E0.
    r = eps/mp.sqrt(y*(-mp.expm1(-y)))
    g = y/(1-2*r*y)
    B = (1+2*r*g)/(1+r*r*P)
    return mp.sqrt(B*U)*r/(2*X*(U/X-r*g))


def partials(function, point):
    return [mp.diff(function, point, tuple(int(i==j) for i in range(len(point))))
            for j in range(len(point))]


def H_coefficients(eps, X, y, U, P):
    v = geometry(eps,X,y,U,P)
    hx,hy,hu,hp = partials(lambda *p:Hvalue(eps,*p), (X,y,U,P))
    # dH/dX = D0 + P_X D1 along dy/dX=P_X/(r_y W),
    # dU/dX=-2-2g(2X+U)P_X/W and dP/dX=P_X.
    D0 = hx-2*hu
    D1 = hy/(v['ry']*v['W'])-2*v['g']*(2*X+U)*hu/v['W']+hp
    return D0,D1,v


def slope(eps, X, y1, U1, y2, U2, P):
    a0,a1,_ = H_coefficients(eps[0],X,y1,U1,P)
    b0,b1,_ = H_coefficients(eps[1],X,y2,U2,P)
    return -(a0-b0)/(a1-b1)


def local(v, PX, PXX, Hprime):
    X,U,P,r,g,gr,B,W = [v[k] for k in ('X','U','P','r','g','gr','B','W')]
    invA = 2*X+U
    Xr = W/PX
    Br = v['Br_partial']-v['T']*r*r*W/(1+r*r*P)**2
    Ur = -2*g*invA-2*Xr
    p = mp.sqrt(B*U)
    pr = p*(Br/B+Ur/U)/2
    GX = PX*v['H']
    GXX = PXX*v['H']+PX*Hprime
    Hess = mp.matrix([[-g*p/B,g*mp.sqrt(invA/B),0,0],
        [g*mp.sqrt(invA/B),(pr-Br*p/(2*B))/B,0,0],
        [0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
    gradient = [-mp.sqrt(invA),mp.sqrt(U),0,0]
    C,stress = evaluator()(1,GX,GXX,P,PX,PXX,*gradient,
                           *[Hess[i,j] for i in range(4) for j in range(i,4)])
    rho = (1-1/B)/r**2+Br/(B**2*r)
    radial_pressure = (1/B-1)/r**2+2*g/(B*r)
    angular_pressure = (gr+g*g-g*Br/(2*B)+(g-Br/(2*B))/r)/B
    stress_scale = max(abs(rho),abs(radial_pressure),abs(angular_pressure))
    stress_error = max(abs(stress[0,0]-rho),abs(stress[1,1]-radial_pressure),
        abs(stress[2,2]-angular_pressure),abs(stress[0,1]))/stress_scale
    current_terms = [PX*p/B,2*GX*X*g/B,-2*GX*p*p/(B*B*r)]
    current_error = abs(sum(current_terms))/sum(abs(t) for t in current_terms)
    K,cross,radial,angular = C[0,0],C[0,1],C[1,1],C[2,2]
    candidates = [mp.mpf(0),mp.mpf(1)]
    if radial>angular:
        vertex = abs(cross)/(radial-angular)
        if 0<vertex<1:
            candidates.append(vertex)
    margins = [K+angular-2*abs(cross)*t+(radial-angular)*t*t for t in candidates]
    margin = min(margins)
    bounded = bool(K>0 and radial<0 and angular<0)
    return dict(y=v['y'],U=U,H=v['H'],Hprime=Hprime,GX=GX,GXX=GXX,
        Xr=Xr,rho=rho,radial_pressure=radial_pressure,angular_pressure=angular_pressure,
        kinetic=K,cross=cross,radial=radial,angular=angular,
        radial_discriminant=cross**2-K*radial,
        light_margin=margin,kinetic_minus_abs_cross=K-abs(cross),
        minimizing_t=candidates[margins.index(margin)],
        bounded_static_hamiltonian=bounded,
        strict_cone=bool(bounded and K>abs(cross) and margin>0),
        relative_stress_error=stress_error,relative_current_error=current_error)


@lru_cache(None)
def check(dps=60):
    with mp.workdps(dps):
        eps = (mp.mpf('1e-6'),mp.mpf('2e-6'))
        X,y1,y2,P = map(mp.mpf,('.5','.1','.3','0'))
        seed = geometry(eps[0],X,y1,mp.mpf('1e-6'),P)
        U1 = mp.mpf('.25')*X*seed['r']*seed['g']
        target = Hvalue(eps[0],X,y1,U1,P)
        other = geometry(eps[1],X,y2,mp.mpf('1e-6'),P)
        V = X*other['r']*other['g']
        a = mp.sqrt(other['B'])*other['r']
        radical = mp.sqrt(a*a+16*target*target*V)
        sqrtU2 = (a+radical)/(4*target) if target>0 else -4*target*V/(a+radical)
        U2 = sqrtU2**2
        point = (X,y1,U1,y2,U2,P)
        PX = slope(eps,*point)
        a0,a1,one = H_coefficients(eps[0],X,y1,U1,P)
        b0,b1,two = H_coefficients(eps[1],X,y2,U2,P)
        tangent = [mp.mpf(1)]
        for v in (one,two):
            tangent += [PX/(v['ry']*v['W']),-2-2*v['g']*(2*X+v['U'])*PX/v['W']]
        tangent += [PX]
        # Total real mpmath derivative along the tangent, including explicit X.
        PXX = mp.diff(lambda h:slope(eps,*[p+h*d for p,d in zip(point,tangent)]),mp.mpf(0))
        Hprime1,Hprime2 = a0+PX*a1,b0+PX*b1
        rows = [local(one,PX,PXX,Hprime1),local(two,PX,PXX,Hprime2)]
        mismatch = lambda key:abs(rows[0][key]-rows[1][key])/max(abs(rows[0][key]),abs(rows[1][key]))
        return dict(dps=dps,X=X,P=P,PX=PX,PXX=PXX,point=point,
            constraint_denominator=a1-b1,halos=rows,
            H_relative_mismatch=mismatch('H'),Hprime_relative_mismatch=mismatch('Hprime'),
            GX_relative_mismatch=mismatch('GX'),GXX_relative_mismatch=mismatch('GXX'),
            status='LOCAL TWO-MASS JET ONLY; GLOBAL AND COSMOLOGICAL THEORY OPEN')


def second_H_partial(v, PX):
    """d(H_X)/dX along the halo, keeping PX fixed inside H_X.

The full second derivative is this value plus D1*PXX.
"""
    point = (v['X'],v['y'],v['U'],v['P'])
    tangent = (mp.mpf(1),PX/(v['ry']*v['W']),
               -2-2*v['g']*(2*v['X']+v['U'])*PX/v['W'],PX)
    def along(h):
        d0,d1,_ = H_coefficients(v['eps'],*[p+h*d for p,d in zip(point,tangent)])
        return d0+PX*d1
    return mp.diff(along,mp.mpf(0))


@lru_cache(None)
def third_mass_check(dps=60):
    with mp.workdps(dps):
        original = check(dps)
        X,y1,U1,_,_,P = original['point']
        PX,PXX = original['PX'],original['PXX']
        eps1,eps3 = mp.mpf('1e-6'),mp.mpf('1.5e-6')
        d01,d11,one = H_coefficients(eps1,X,y1,U1,P)
        target_H,target_Hprime = one['H'],d01+PX*d11
        def matched(y):
            v = geometry(eps3,X,y,eps3,P)
            V = X*v['r']*v['g']
            a = mp.sqrt(v['B'])*v['r']
            radical = mp.sqrt(a*a+16*target_H*target_H*V)
            sqrtU = (a+radical)/(4*target_H) if target_H>0 else -4*target_H*V/(a+radical)
            return H_coefficients(eps3,X,y,sqrtU**2,P)
        def residual(y):
            d0,d1,_ = matched(y)
            return (d0+PX*d1-target_Hprime)/abs(target_Hprime)
        y3 = mp.findroot(residual,(mp.mpf('.15'),mp.mpf('.17')),
                        tol=mp.mpf(10)**(-(dps-10)),maxsteps=30)
        d03,d13,three = matched(y3)
        k1 = second_H_partial(one,PX)
        k3 = second_H_partial(three,PX)
        required_PXX = -(k3-k1)/(d13-d11)
        Hsecond1,Hsecond3 = k1+d11*PXX,k3+d13*PXX
        return dict(dps=dps,epsilon3=eps3,y3=y3,U3=three['U'],
            H_relative_mismatch=abs(three['H']/target_H-1),
            Hprime_relative_mismatch=abs(residual(y3)),
            common_PXX=PXX,required_PXX=required_PXX,
            required_PXX_fractional_change=(required_PXX-PXX)/PXX,
            Hsecond_reference=Hsecond1,Hsecond_third=Hsecond3,
            Hsecond_relative_mismatch=abs(Hsecond3-Hsecond1)/max(abs(Hsecond1),abs(Hsecond3)),
            third_halo=local(three,PX,PXX,d03+PX*d13),
            scope='Only the root near y3=0.1604 for epsilon3=1.5e-6; no all-roots or universal no-go claim.')


def serial(value):
    if isinstance(value,dict):
        return {k:serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [serial(v) for v in value]
    if isinstance(value,(bool,int,str)):
        return value
    return mp.nstr(value,50)


if __name__=='__main__':
    print(json.dumps(serial(check()),indent=2))
