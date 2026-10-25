import argparse,json,math
from pathlib import Path
import numpy as np
import sympy as S
from scipy.integrate import solve_ivp
from scipy.linalg import eigh_tridiagonal

q,d=S.symbols('q d',real=True)
s=S.Rational(1,4);y=S.sin(S.sqrt(s)*q)**2/s;f=1-s*y
W=(1+(y-1)**2)/f**2;A=f**(-S.Rational(1,2))
V=W+d*A
HESS=S.lambdify((q,d),S.diff(V,q,2),'numpy')
QOUT=2*math.asin(math.sqrt(1/6));MOUT2=5.76
assert S.simplify(S.diff(V,q,2).subs(q,0)-(d/4-2))==0

def yy(qq):return 4*np.sin(.5*qq)**2

def delta_in(qq,dd):
    t=yy(qq);ff=1-.25*t
    return t*(-1+.875*t)/ff**2 + dd*(.25*t)/(np.sqrt(ff)*(1+np.sqrt(ff)))

def profile(dd,L,mutate=False):
    As=1+.4/dd;fs=As**-2;qs=2*math.asin(math.sqrt(1-fs))
    left=math.sqrt(max(0,2*delta_in(qs,0 if mutate else dd)))
    right=math.sqrt(1.8)*(2/3-yy(qs))/(1-.25*yy(qs))
    assert abs(left-right)<1e-12,'surface derivative mismatch'
    lin=solve_ivp(lambda z,u:[math.sqrt(max(0,2*delta_in(u[0],dd)))],[0,-L],[qs],
                   rtol=1e-11,atol=1e-13,dense_output=True)
    rout=solve_ivp(lambda z,u:[math.sqrt(1.8)*(2/3-yy(u[0]))/(1-.25*yy(u[0]))],[0,L],[qs],
                   rtol=1e-11,atol=1e-13,dense_output=True)
    assert lin.success and rout.success
    def background(z):
        if np.ndim(z)==0:return float((lin if z<0 else rout).sol(z)[0])
        return np.where(z<0,lin.sol(np.minimum(z,0))[0],rout.sol(np.maximum(z,0))[0])
    def pot(z):return float(HESS(background(z),dd if z<0 else 0))
    assert abs(background(-L))<1e-8 and abs(background(L)-QOUT)<1e-8
    return background,pot,dict(surface_q=qs,derivative_match_error=abs(left-right))

def scatter(pot,dd,L,pm):
    omega2=MOUT2*(1+pm*pm);kout=math.sqrt(MOUT2)*pm;mi=dd/4-2
    propagates=omega2>mi
    derivative=-1j*math.sqrt(omega2-mi) if propagates else complex(math.sqrt(mi-omega2))
    state=np.array([1+0j,derivative])
    for interval in [[-L,0],[0,L]]:
        # At the discontinuity its value at one point has no continuum effect.
        sol=solve_ivp(lambda z,u:[u[1],(pot(z)-omega2)*u[0]],interval,state,
                      method='DOP853',rtol=1e-10,atol=1e-12,max_step=.15)
        assert sol.success;state=sol.y[:,-1]
    u,du=state;incoming=(u+1j*du/kout)/2;reflected=(u-1j*du/kout)/2
    R=float(abs(reflected/incoming)**2)
    T=float(math.sqrt(omega2-mi)/kout/abs(incoming)**2) if propagates else 0.
    assert abs(R+T-1)<1e-6,'flux conservation failed'
    return dict(p_over_mout=pm,R=R,T=T,interior_propagating=propagates,flux_error=abs(R+T-1))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
 out=Path(args.output);out.mkdir(parents=True,exist_ok=True);rows=[]
 for dd in [20.,32.,100.]:
    domains=[]
    for L in [15.,20.]:
        bg,pot,info=profile(dd,L,args.mutate);eigs=[]
        for dx in [.02,.01]:
            # Cell-centred mesh avoids placing a sample on the density jump.
            z=np.arange(-L+dx/2,L,dx)
            hess=HESS(bg(z),np.where(z<0,dd,0))
            ev=eigh_tridiagonal(2/dx**2+hess,np.full(len(z)-1,-1/dx**2),
                select='i',select_range=(0,2),check_finite=False)[0]
            eigs.append(dict(dx=dx,lowest_eigenvalues=ev.tolist()))
        assert abs(eigs[0]['lowest_eigenvalues'][0]-eigs[1]['lowest_eigenvalues'][0])<.01
        waves=[scatter(pot,dd,L,pm) for pm in [.001,.1,1.,3.]]
        domains.append(dict(L=L,profile=info,eigenvalues=eigs,waves=waves))
    assert abs(domains[0]['eigenvalues'][-1]['lowest_eigenvalues'][0]-domains[1]['eigenvalues'][-1]['lowest_eigenvalues'][0])<.01
    for a,b in zip(domains[0]['waves'],domains[1]['waves']):
        assert abs(a['R']-b['R'])<1e-5 and abs(a['T']-b['T'])<1e-5,'domain scattering change'
    rows.append(dict(density_star_over_D=dd,domains=domains))
 result=dict(scope='fixed-source planar scalar interface; not full gravity or reservoir',cases=rows,
             checks=['surface first integrals','asymptotic endpoints','scalar eigenvalue resolution/domain',
                     'wave flux','scattering domain check'])
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps([dict(density=c['density_star_over_D'],lambda0=c['domains'][-1]['eigenvalues'][-1]['lowest_eigenvalues'][0],waves=c['domains'][-1]['waves']) for c in rows],indent=2))
if __name__=='__main__':main()
