"""Fix of part (b): gate positivity as a function of the dimensionless x=|a|/N alone."""
import sympy as sp, mpmath as mp
mp.mp.dps = 30
xs = sp.symbols('x', positive=True)   # clean dimensionless symbol = |a|/N
K_long = 2*xs/sp.sqrt(1+4*xs**2)
mu_fw  = (sp.sqrt(1+4*xs**2)-1)/(2*xs)
print("Gate functions of x=|a|/N ALONE:")
print("  K_long =", K_long, "   mu_fw =", mu_fw)
Kl = sp.lambdify(xs, K_long, 'mpmath'); Mf = sp.lambdify(xs, mu_fw, 'mpmath')
pts = [mp.mpf('1e-6'), mp.mpf('1e-3'), mp.mpf(1), mp.mpf('1e3'), mp.mpf('1e6')]
print("  x:        K_long>0 ?   mu_fw>0 ?")
allpos = True
for xx in pts:
    kl, mf = Kl(xx), Mf(xx); allpos &= (kl>0 and mf>0)
    print(f"  {float(xx):.0e}:   {kl>0}        {mf>0}")
print("ALL positive across 12 decades:", allpos)
# Is there ANY interior sign change / ghost boundary in x>0? Check derivative signs / roots.
print("Roots of K_long in x>0:", sp.solve(sp.Eq(K_long,0), xs))
print("Roots of mu_fw  in x>0:", sp.solve(sp.Eq(mu_fw,0),  xs))
print(">>> Only root at x=0 (boundary). NO interior x* => no special scale pinned.")
print(">>> Carrying N INSIDE the gate (x=|a|/N) STILL does not let positivity pin N.")
print(">>> N-invariance is STRUCTURAL, not an artifact of inserting N as an overall factor.")
