"""argon_clues: check the five pasted 'new structural identities' of g_N = g^2/(g+a0)."""
import sympy as s, math
g,a0,u,y,K = s.symbols('g a0 u y K', positive=True)
gN = g**2/(g+a0); uu = g-gN
ok=lambda n,e: print(('TRUE  ' if s.simplify(e)==0 else 'FALSE ')+n, '' if s.simplify(e)==0 else '-> residual %s'%s.simplify(e))
# 1 Legendre dual
Wfull = a0**2*(-s.log(1-u/a0)-u/a0)           # K*W_full
gofu = u/(1-u/a0)
Wstar = (u*gofu - Wfull).subs(u, g*a0/(g+a0))
ok('1a  K W*_full(g) = a0^2 (g/a0 - ln(1+g/a0))', Wstar - a0**2*(g/a0 - s.log(1+g/a0)))
ok('1b  dW*/dg = u (Legendre) [paste: g/(g+a0) = u/a0 = 1/nu_s]', s.diff(a0**2*(g/a0-s.log(1+g/a0)),g) - g*a0/(g+a0))
ok('1c  W*(g) deep: g^2/2, Newton: a0 g (limits)', s.limit(a0**2*(g/a0-s.log(1+g/a0))/g**2, g, 0) - s.Rational(1,2))
print('      (1 is true; "Born-Infeld/string tension" is an analogy, not a derived statement)')
# 2 identities
nu = g/gN
ok('2a  y nu (nu-1) = 1 with y = g_N/a0', (gN/a0)*nu*(nu-1) - 1)
ok('2b  g_N a0 = g u', gN*a0 - g*uu)
nu1 = (1+math.sqrt(5))/2
print('TRUE  2c  nu_s(y=1) = golden ratio %.6f ; tether mass share at y=1: (nu-1)/nu = %.4f'%(nu1,(nu1-1)/nu1))
# 3 harmonic
ok('3a  1/u = 1/g + 1/a0', 1/uu - 1/g - 1/a0)
ok('3b  tau_u^2 = tau_g^2 + tau_a0^2 (tau^2 = l/acc)', 1/uu - 1/g - 1/a0)
ok('3 note: the paste first claimed 1/g_N - 1/g = 1/a0 and then corrected itself: that version is', 1/gN - 1/g - 1/a0)
# 4 curvature
Wp = lambda x: x**2/(a0-x)
W2 = s.diff(Wp(u),u).subs(u, g*a0/(g+a0))
ok('4a  K W_rem\'\'(u) = g(g+2a0)/a0^2', W2 - g*(g+2*a0)/a0**2)
ok('4b  K W_full\'\' = (1+g/a0)^2', 1+W2 - (1+g/a0)**2)
ok('4c  radial/transverse stiffness = 2 + g/a0', W2/(Wp(u).subs(u,g*a0/(g+a0))/(g*a0/(g+a0))) - (2+g/a0))
print('      4: "refractive index n=(1-u/a0)^(3/2)" in the heading is never derived; 2:1 anisotropy is a statement about delta-P wave stiffness, no observable attached')
# 5 numerology
R0=5.364; x=math.sqrt(1+R0)-1; gNa=x**2/(1+x); nuv=(1+x)/x
print('5. set K W_full\'\' = 1+R0 -> g/a0 = %.4f, g_N/a0 = %.4f (paste: ~1; off by %.1f%%), nu = %.4f vs golden ratio %.4f (off by %.1f%%)'%(x,gNa,100*abs(gNa-1),nuv,nu1,100*abs(nuv-nu1)/nu1))
print('   the condition K W\'\'(u) = R0 is arbitrary (no physical reason to equate a stiffness to a mass ratio); this is the retracted-numerology pattern.')
