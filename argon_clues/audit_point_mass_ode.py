"""argon_clues: check the pasted exact point-mass solution of the stiffened P-equation.
Dimensionless: x=r/L*, v=u/a0, m=G M/(a0 L*^2):  -(v''+2v'/x-2v/x^2) + v^2/(1-v) = m/x^2"""
import numpy as np, math
from scipy.integrate import solve_bvp
G=6.6743e-11; Ms=1.98847e30; pc=3.0857e16; a0=9.36e-11; Ls=5.75*pc
Mcrit=2*a0*Ls**2/G
print('M_crit = 2 a0 L*^2/G = %.3e Msun  (paste: 4.75e7 Msun -> off by ~%.0fx; with a0=1.0e-10 it is %.2e)'%(Mcrit/Ms,4.75e7/(Mcrit/Ms),2e-10*Ls**2/G/Ms))
print('1 Msun: m = %.2e, u(0)/a0 = m/2 = %.2e'%(G*Ms/(a0*Ls**2),G*Ms/(a0*Ls**2)/2))
def solve(m, eps=1e-3, X=60.0):
    def f(x,y): v,w=y; return np.vstack([w, -2*w/x+2*v/x**2+ v**2/(1-np.clip(v,None,0.999999)) - m/x**2])
    # algebraic far value: v^2/(1-v)=m/X^2
    c=m/X**2; vX=(c+math.sqrt(c*c+4*c))/2
    bc=lambda ya,yb: np.array([ya[0]-m/2, yb[0]-vX])
    x=np.geomspace(eps,X,400); y=np.vstack([np.minimum(m/2,0.9)*np.ones_like(x)*np.exp(-x/5)+vX, np.zeros_like(x)])
    s=solve_bvp(f,bc,x,y,tol=1e-6,max_nodes=200000)
    return s
for m in (4.5e-5, 0.05, 0.5, 1.5):
    s=solve(m)
    print('m=%.3g: converged %s ; v(eps)=%.4g (m/2=%.4g) ; max v=%.4g ; v(1)=%.4g v(10)=%.4g v(60)=%.4g'%(m,s.success,s.sol(1e-3)[0],m/2,s.y[0].max(),s.sol(1)[0],s.sol(10)[0],s.sol(60)[0]))
print('m=3 (v0>1): inner constant exceeds a0 -> no smooth sub-saturated solution of this form (paste: saturates at x->0 with a0-u ~ a0^2 r^2/(G(M-Mcrit)))')
