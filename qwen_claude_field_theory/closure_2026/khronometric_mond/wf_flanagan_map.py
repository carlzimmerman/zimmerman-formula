"""
!!! SUPERSEDED by wf_decisive_v2_correct.py !!!
This file used the ACTION-LEVEL map (-2f <-> a0^2 W), which is INCONSISTENT with
Flanagan's own MOND-function definition mu = 1 + fbar'/(2 abar).  The correct map is
via mu: fbar' = 2 abar (mu-1).  Under the correct map the DANGEROUS coefficient is the
LONGITUDINAL KINETIC term -fbar''/2 = (1-y)e^-y (ghost for y>1), NOT the gradient.
Kept only for provenance.  Use wf_decisive_v2_correct.py.
"""

"""
wf_flanagan_map.py
Map Carl's primitive W(y) onto Flanagan (arXiv:2302.14846) stability conditions
and TEST every natural sign-definite combination across the transition.

Flanagan action:   S = c^3/(16 pi G) int sqrt(-g)[R - 2 f(a)],  a = |khronon accel|.
Carl action term:  +a0^2 W(a/a0)  inside  M_Pl^2/2 [ R + ... + a0^2 W ].
Since M_Pl^2/2 = c^3/(16 pi G), matching the scalar potential pieces:
        -2 f(a)  <->  a0^2 W(a/a0) + const     =>     f(a) = -1/2 a0^2 W(a/a0) + C.
Let y=a/a0:
        f'(a)  = -1/2 a0   W'(y)
        f''(a) = -1/2       W''(y)
        a f''(a) = -1/2 a0 y W''(y)

Flanagan stability:
  Eq 43:  f' <= 0  AND  f'' <= 0
  Eq 54:  f' <= a f'' <= 0
Translate (divide by -1/2 a0 < 0, inequalities FLIP):
  f'  <= 0        <=>  W'(y)  >= 0
  f'' <= 0        <=>  W''(y) >= 0
  a f'' <= 0      <=>  W''(y) >= 0
  f' <= a f''     <=>  W'(y) >= y W''(y)   i.e.   G(y) := W'(y) - y W''(y) >= 0
"""
import sympy as sp

y = sp.symbols('y', positive=True)
W   = sp.Rational(1,2)*y**2 + (1+y)*sp.exp(-y) - 1
Wp  = sp.simplify(sp.diff(W,y))
Wpp = sp.simplify(sp.diff(W,y,2))
mu  = sp.simplify(Wp/y)

print("W'   =", Wp)
print("W''  =", Wpp)
print("mu   =", mu)
print()

# Flanagan Eq43 in W-language: W'>=0 and W''>=0
print("Eq43  W'(y)  >= 0 ?  W' =", Wp, " -> positive for all y>0 (y*(1-e^-y))")
print("Eq43  W''(y) >= 0 ?  W''=", Wpp)
print()

# Flanagan Eq54 nontrivial part: G(y) = W' - y W''  >= 0 ?
G = sp.simplify(Wp - y*Wpp)
print("Eq54 combination  G(y) = W'(y) - y*W''(y) =", G)
print("   factored:", sp.factor(G))
print()

# geometric interpretation: G = y*(mu - W'') = y*(H_perp - H_par)
diff_hess = sp.simplify(Wpp - mu)   # H_par - H_perp
print("H_par - H_perp = W'' - mu =", diff_hess, " = ", sp.factor(diff_hess))
print("G = y*(H_perp - H_par) =", sp.simplify(y*(mu - Wpp)), " (matches G above)")
print()

# Enumerate sign of every natural combination on (0,inf)
import numpy as np
def num(expr):
    fn = sp.lambdify(y, expr, 'numpy')
    ys = np.concatenate([np.logspace(-6,6,300001), np.linspace(1e-3,20,300001)])
    v = fn(ys)
    return v.min(), ys[np.argmin(v)], v.max(), ys[np.argmax(v)]

combos = {
 "W'  (Eq43 ghost/grad a)   = mu*y":      Wp,
 "W'' (Eq43 grad b, H_par)":              Wpp,
 "mu  (H_perp)":                          mu,
 "G = W'-yW'' (Eq54: >=0 needed)":        G,
 "H_par-H_perp = W''-mu":                 diff_hess,
 "W''+mu":                                sp.simplify(Wpp+mu),
 "W' (should be >0)":                     Wp,
}
print("=== SIGN OF COMBINATIONS over (1e-6,1e6) ===")
for name,expr in combos.items():
    mn,amn,mx,amx = num(expr)
    sign = "POS-definite" if mn>0 else ("NEG-definite" if mx<0 else "SIGN-INDEFINITE")
    print(f"{name:38s} min={mn:+.4e}@y={amn:.3e}  max={mx:+.4e}  -> {sign}")
