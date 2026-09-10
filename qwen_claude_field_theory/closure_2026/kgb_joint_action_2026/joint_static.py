#!/usr/bin/env python3
"""Two halo inverse for ONE P(X)-G(X) box(phi) action, no particle dark matter.

Preserving G_X/P_X equality determines P_X; differentiation determines P_XX.
No independent stability steering remains. This is a generic nonzero-P_X chart,
not a no-go at its singularities or proof of universal/cosmological existence.
Units c=a0=m=|q|=1; epsilon=sqrt(G_bare M a0)/c^2.
"""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import sympy as s

spec = importlib.util.spec_from_file_location('pressure_source', Path(__file__).resolve().parent.parent/'kgb_shared_pressure_2026/shared_pressure.py')
source = importlib.util.module_from_spec(spec); spec.loader.exec_module(source)


def symbolic_reduction():
    r, g, gr, T, Tr, P, X, U, W, PX = s.symbols('r g gr T Tr P X U W PX', nonzero=True)
    Z = U/X-r*g
    Xr = W/PX
    BrB = Tr/T-(2*r*P+r*r*W)/(1+r*r*P)
    Ur = -2*g*(2*X+U)-2*Xr
    Zr = Ur/X-U*Xr/X**2-g-r*gr
    log_derivative = ((BrB+Ur/U)/2+1/r-Xr/X-Zr/Z)/Xr
    aa = -1/U+(2+r*g)/(X*Z)
    v0 = BrB/2-g*(2*X+U)/U
    bb = (v0+1/r+(2*g*(2*X+U)/X+g+r*gr)/Z)/W
    return dict(log_derivative_residual=s.factor(log_derivative-aa-PX*bb),
                a=aa, b=bb,
                preservation='(H1*a1-H2*a2)+P_X*(H1*b1-H2*b2)=0')


def coefficients(eps, y, X, U, P):
    """Analytic on the stated chart; no abs/casts, also usable by complex step."""
    mu = -np.expm1(-y); lam = mu+y*np.exp(-y)
    r = eps/np.sqrt(y*mu); ry = -r*lam/(2*y*mu)
    yr = 1/ry; c = r*y; cr = y+r*yr
    T = 1/(1-2*c); Tr = 2*cr*T*T
    g = y*T; gr = yr*T+y*Tr
    B = T/(1+r*r*P); Z = U/X-r*g
    rho0 = 4*y*y*np.exp(-y)/(r*lam)
    E0 = rho0+P*(1-3/T+r*Tr/(T*T))
    W = Z*E0/(r*(1+Z/T))
    H = np.sqrt(B*U)*r/(2*X*Z)
    BrB = Tr/T-(2*r*P+r*r*W)/(1+r*r*P)
    aa = -1/U+(2+r*g)/(X*Z)
    v0 = BrB/2-g*(2*X+U)/U
    bb = (v0+1/r+(2*g*(2*X+U)/X+g+r*gr)/Z)/W
    return dict(eps=eps,y=y,X=X,U=U,P=P,r=r,ry=ry,g=g,gr=gr,
                T=T,Tr=Tr,B=B,Z=Z,W=W,E0=E0,H=H,a=aa,b=bb,BrB=BrB)


def initial(eps1, eps2, y1, y2, bscale, X=.5, P=0.):
    a = coefficients(eps1,y1,X,1e-6,P)
    U1 = bscale*X*a['r']*a['g']
    a = coefficients(eps1,y1,X,U1,P)
    b = coefficients(eps2,y2,X,1e-6,P)
    target = a['H']; V = X*b['r']*b['g']; aa = np.sqrt(b['B'])*b['r']
    root = np.sqrt(aa*aa+16*target*target*V)
    # Positive sqrt(U) on the correct unsquared sign branch, stable at small H.
    sqrtU = (aa+root)/(4*target) if target>0 else 4*abs(target)*V/(aa+root)
    return np.array([np.log(y1),U1/eps1,np.log(y2),sqrtU**2/eps2,P])


def shared(X, state, eps):
    a = coefficients(eps[0],np.exp(state[0]),X,eps[0]*state[1],state[4])
    b = coefficients(eps[1],np.exp(state[2]),X,eps[1]*state[3],state[4])
    numerator = a['H']*a['a']-b['H']*b['a']
    denominator = a['H']*a['b']-b['H']*b['b']
    return -numerator/denominator, a, b


def flow(X, state, eps):
    px, a, b = shared(X,state,eps)
    out = []
    for e, v in zip(eps,(a,b)):
        out.extend([px/(v['y']*v['ry']*v['W']),
                    (-2-2*v['g']*(2*X+v['U'])*px/v['W'])/e])
    return np.array(out+[px])


def action_jet(X, state, eps):
    """Total derivative of the determined slope, NOT a tunable health parameter."""
    px = shared(X,state,eps)[0]
    vector = flow(X,state,eps)
    h = 1e-25
    pxx = np.imag(shared(X+1j*h,state,eps)[0])/h
    for i in range(5):
        perturbed = np.asarray(state,dtype=complex).copy(); perturbed[i] += 1j*h
        pxx += np.imag(shared(X,perturbed,eps)[0])/h*vector[i]
    return px, pxx


def local(v, px, pxx):
    X,U,r,g,gr,P,B,Z,W,BrB = [v[k] for k in ('X','U','r','g','gr','P','B','Z','W','BrB')]
    if min(X,U,r,B)<=0 or px==0 or W==0 or Z==0:
        raise ValueError('outside generic inverse chart')
    invA = 2*X+U; p = np.sqrt(B*U); Xr = W/px
    Ur = -2*g*invA-2*Xr; Lp = (BrB+Ur/U)/2
    GX = px*v['H']
    GXX = pxx*v['H']+GX*(v['a']+px*v['b'])
    H = np.array([[-g*p/B,g*np.sqrt(invA/B),0,0],
                  [g*np.sqrt(invA/B),p*(Lp-BrB/2)/B,0,0],
                  [0,0,p/(B*r),0],[0,0,0,p/(B*r)]])
    vv = [-np.sqrt(invA),np.sqrt(U),0,0]
    C, stress = source.evaluator()(1,GX,GXX,P,px,pxx,*vv,*[H[i,j] for i in range(4) for j in range(i,4)])
    rho = v['E0']-r*W/v['T']-P
    pt = (gr+g*g-g*BrB/2+(g-BrB/2)/r)/B
    error = max(abs(stress[0,0]-rho),abs(stress[1,1]-P),abs(stress[2,2]-pt),abs(stress[0,1]))/max(abs(rho),abs(P),abs(pt),1e-200)
    K,cross,radial,angular = C[0,0],C[0,1],C[1,1],C[2,2]
    bounded = bool(K>0 and radial<0 and angular<0)
    # For the bounded-energy branch, cone containment reduces to a quadratic
    # on 0<=t<=1, including its interior minimum. Floating evaluation only.
    points = [0.,1.]
    if radial>angular:
        t = abs(cross)/(radial-angular)
        if 0<t<1: points.append(t)
    margin = min(K+angular-2*abs(cross)*t+(radial-angular)*t*t for t in points)
    causal = bool(bounded and K>abs(cross) and margin>0)
    return dict(y=float(v['y']),U=float(U),GX=float(GX),GXX=float(GXX),
                kinetic=float(K),cross=float(cross),radial=float(radial),angular=float(angular),
                bounded_static_hamiltonian=bounded,strict_cone=causal,light_margin=float(margin),
                rho=float(rho),P=float(P),relative_stress_error=float(error),
                leading_Weyl_fraction=float(r*P/(4*g)))


def inspect(X,state,eps):
    px, pxx = action_jet(X,state,eps)
    _,a,b = shared(X,state,eps)
    rows = [local(v,px,pxx) for v in (a,b)]
    mismatch = lambda key:abs(rows[0][key]-rows[1][key])/max(abs(rows[0][key]),abs(rows[1][key]),1e-200)
    result=dict(X=float(X),P=float(state[4]),PX=float(px),PXX=float(pxx),halos=rows,
                H_relative_mismatch=float(abs(a['H']/b['H']-1)),
                GX_relative_mismatch=float(mismatch('GX')),GXX_relative_mismatch=float(mismatch('GXX')),
                both_bounded=all(v['bounded_static_hamiltonian'] for v in rows),
                both_causal=all(v['strict_cone'] for v in rows))
    if len(state)>5:result['G']=float(state[5])
    json.dumps(result,allow_nan=False)  # Nonfinite computations are not negative physics results.
    return result


def scan():
    rows=[]; eps=(1e-6,2e-6)
    for y1 in (.1,1.,10.,20.):
        for y2 in (.1,.3,.6,1.,2.,5.,10.,20.):
            for b in (.25,.75,1.25,4.):
                state=initial(*eps,y1,y2,b)
                try:
                    row=inspect(.5,state,eps)
                    row.update(y1=y1,y2=y2,bscale=b,state=state.tolist())
                    rows.append(row)
                except (ValueError,FloatingPointError) as exc:
                    rows.append(dict(y1=y1,y2=y2,bscale=b,error=str(exc)))
    return rows


def integrate(state, eps=(1e-6,2e-6), duration=.05, rtol=2e-9, stop_health=False):
    """Use t=(X-.5)/eps1; inspect accepted output, never failed trial values."""
    def rhs(t,v):
        X=.5+eps[0]*t
        px,a,_=shared(X,v,eps)
        return eps[0]*np.append(flow(X,v,eps),px*a['H'])
    def health_event(t,v):
        row=inspect(.5+eps[0]*t,v,eps)
        margins=[]
        for h in row['halos']:
            margins.extend([h['kinetic'],-h['radial'],-h['angular'],h['light_margin'],
                            h['kinetic']-abs(h['cross'])])
        return min(margins)/1e11
    health_event.terminal=True; health_event.direction=-1
    # G(.5)=0 is an irrelevant integration constant (a boundary term).
    sol=solve_ivp(rhs,(0,duration),np.append(state,0.),method='DOP853',rtol=rtol,atol=rtol/100,
                  max_step=min(abs(duration)/100,.005),dense_output=True,
                  events=health_event if stop_health else None)
    times=np.linspace(0,sol.t[-1],51)
    rows=[]
    for t in times:
        try:rows.append(inspect(.5+eps[0]*t,sol.sol(t),eps))
        except (ValueError,FloatingPointError):break
    return dict(duration=duration,rtol=rtol,solver_success=bool(sol.success),
                endpoint=float(sol.t[-1]),nfev=sol.nfev,message=sol.message,rows=rows,
                endpoint_state=sol.y[:,-1].tolist(),
                stopped_at_health_boundary=bool(stop_health and len(sol.t_events[0])))


def main():
    print('SYMBOLIC='+json.dumps({k:str(v) for k,v in symbolic_reduction().items()}))
    rows=scan()
    print('SCAN='+json.dumps(dict(rows=rows,bounded=sum(x.get('both_bounded',False) for x in rows),
                                 causal=sum(x.get('both_causal',False) for x in rows))))
    healthy=[x for x in rows if x.get('both_causal',False)]
    for v in healthy[:2]:
        for direction in (1,-1):
            run=integrate(np.array(v['state']),duration=.05*direction)
            print('CONTINUATION='+json.dumps(dict(initial={k:v[k] for k in ('y1','y2','bscale')},run=run)),flush=True)
            for tolerance in (2e-9,2e-11):
                run=integrate(np.array(v['state']),duration=direction,rtol=tolerance,stop_health=True)
                print('BOUNDARY='+json.dumps(dict(initial={k:v[k] for k in ('y1','y2','bscale')},run=run)),flush=True)
    print('STATUS=OPEN; finite shared-action inverse test, not full gravity certification')
    return 0


if __name__=='__main__':raise SystemExit(main())
