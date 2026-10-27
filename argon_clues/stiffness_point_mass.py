"""argon_clues: what the stiffened tether equation actually does around a point mass.
-(v''+2v'/x-2v/x^2) + v^2/(1-v) = m/x^2 ; x=r/L*, v=u/a0, m=G M/(a0 L*^2) = M/M_crit*2 (M_crit = 2 a0 L*^2/G).
Phantom mass inside r:  M_ph = u r^2/G -> M_ph/M = v x^2/m.   Inner regularity: m<2: v(0)=m/2 ; m>2: 1-v = x^2/(m-2)."""
import numpy as np, math
from scipy.integrate import solve_bvp
def solve(m, X=400.0, x0=1e-3):
    def f(x,y):
        v=np.clip(y[0],None,1-1e-12); w=y[1]
        return np.vstack([w, -2*w/x+2*v/x**2+v**2/(1-v)-m/x**2])
    c=m/X**2; vX=(c+math.sqrt(c*c+4*c))/2            # algebraic far field
    v0 = m/2 if m<2 else 1-x0**2/(m-2)
    bc=lambda ya,yb: np.array([ya[0]-v0, yb[0]-vX])
    x=np.geomspace(x0,X,600)
    # initial guess: algebraic solution capped
    alg=np.array([(m/xx**2+math.sqrt((m/xx**2)**2+4*m/xx**2))/2 for xx in x]); g=np.minimum(alg,0.999*np.ones_like(alg))
    g=np.minimum(np.where(x<2,v0,g),0.999)
    y=np.vstack([g,np.gradient(g,x)])
    s=solve_bvp(f,bc,x,y,tol=1e-6,max_nodes=400000)
    return s,vX
def alg_v(m,x):                                          # algebraic law: v = u/a0 with g_N = m/x^2 (units a0): u = g a0/(g+a0), g from g_N=g^2/(g+a0)
    gN=m/x**2; g=(gN+math.sqrt(gN*gN+4*gN))/2; return g/(g+1)
G=6.6743e-11; Ms=1.98847e30; a0=9.36e-11; pc=3.0857e16; Ls=5.75*pc; Mc=2*a0*Ls**2/G/Ms
print('M_crit = %.3e Msun ; M = m/2 * M_crit'%Mc)
print('%9s %9s %5s | %8s %8s | phantom mass / M inside x=0.3,1,3,10,100 : stiffened | algebraic'%('M(Msun)','m','conv','v(x=.1)','max v'))
for M in (1,100,4.4e4,1e5,4e6,1e8,1e10):
    m=2*M/Mc; s,vX=solve(m)
    xs=[0.3,1,3,10,100]
    ph=[s.sol(x)[0]*x**2/m for x in xs]; pa=[alg_v(m,x)*x**2/m for x in xs]
    print('%9.1e %9.2e %5s | %8.4f %8.4f | %s | %s'%(M,m,s.success,s.sol(0.1)[0],s.y[0].max(),' '.join('%.3g'%p for p in ph),' '.join('%.3g'%p for p in pa)))
print()
print('Saturated regime (m>2): 1-v = x^2/(m-2) near the centre; u reaches a0 only at r -> 0, and the phantom mass inside L* is capped at M_ph(<L*) <= a0 L*^2/G = M_crit/2 = %.2e Msun.'%(Mc/2))
