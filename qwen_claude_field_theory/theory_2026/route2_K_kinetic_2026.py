#!/usr/bin/env python3
r"""ROUTE 2 first gate: does a0 = a0(K) poison the kinetic sector?

K = h^ij K_ij contains hdot_ij, UNLIKE a_mu and E_mu-nu.  So a0(K) enters the MOMENTA and
can shift the no-ghost condition.  That is the fast structural test, before any cosmology."""
import sympy as sp, numpy as np
def head(t): print("\n"+"="*94+f"\n{t}\n"+"="*94)
def ok(c,l,d=""): print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else "")); return c
X,a0,aa,c_,Z,K=sp.symbols('X a_0 a c Z K',positive=True)

head("A -- the a0-dependence of the MOND term is NOT just the prefactor")
print("  L_F = -(2 a0^2/c^4) F(X),   X = c^4 a_mu a^mu / a0^2   -- a0 appears in BOTH places.")
Fs=-2*sp.sqrt(X)+2*sp.log(1+sp.sqrt(X))
Ga=a0**2*Fs.subs(X,c_**4*aa**2/a0**2)
dG=sp.simplify(sp.diff(Ga,a0))
print(f"  d/da0 [a0^2 F(X)] = {sp.simplify(dG.rewrite(sp.log))}")
comb=sp.simplify((Fs-X*sp.diff(Fs,X)))
print(f"  = 2 a0 [F - X F_X],   with  F - X F_X = {sp.simplify(comb)}")
head("B -- and F - X F_X is UNBOUNDED")
lim=sp.limit(comb/sp.sqrt(X),X,sp.oo)
print(f"  large-X:  (F - X F_X)/sqrt(X) -> {lim}    i.e.  F - X F_X ~ -sqrt(X) = -g/a0")
ok(lim!=0,"B1  the combination grows without bound in the NEWTONIAN regime",
   "MOND's correction to the field equation vanishes there (mu -> 1) but F itself does not")
for Xv in (1e0,1e6,1e12,1e22):
    print(f"     X = {Xv:.0e}:  F - X F_X = {float(comb.subs(X,Xv)):+.4e}   (sqrt(X) = {Xv**0.5:.2e})")
head("C -- feed it into the momentum")
print("  a0 = c|K|/Z  =>  (2 a0^2/c^4) F = (2 K^2/(Z^2 c^2)) F(X)")
print("  so the F-term contributes to the K^2 coefficient of the ADM Lagrangian:")
print("     lam_eff = lam_K + (2/Z^2)(F - X F_X)        [pure-trace, exactly the lam_K slot]")
print("  and pi^ij picks up Delta pi^ij ~ -sqrt(h) (2 a0 a0_K/c^4) F(X) h^ij .")
head("D -- the number")
H0=2.184e-18; cc=2.99792458e8; a0v=9.3619e-11
Zv=3*cc*H0/a0v
print(f"  a0 = 3cH0/Z with a0 = {a0v:.4e}  =>  Z = {Zv:.2f},  Z^2 = {Zv**2:.1f}")
print(f"  {'location':<26}{'g [m/s^2]':>12}{'X = (g/a0)^2':>14}{'shift in lam_eff':>19}")
for lab,g in (("deep MOND, x=0.1",0.1*a0v),("MOND transition",a0v),("Milky Way at Sun",2.1e-10),
              ("Saturn orbit",6.5e-5),("Earth surface",9.81),("Sun surface",274.0)):
    Xv=(g/a0v)**2; sh=float(2*comb.subs(X,Xv)/Zv**2)
    print(f"  {lab:<26}{g:>12.3g}{Xv:>14.3e}{sh:>19.3e}")
print("\n  no-ghost needs lam_eff > 1 (or < 1/3).  The shift is NEGATIVE and enormous:")
sh_earth=float(2*comb.subs(X,(9.81/a0v)**2)/Zv**2)
ok(abs(sh_earth)<1,"D1  a0 = c|K|/Z is compatible with the no-ghost condition",
   f"shift at the Earth's surface = {sh_earth:.3e}")
head("E -- verdict")
print("""  Route 2 in the form a0 = a0(K) is DEAD, and for a reason specific to K:
  a_mu and E_mu-nu contain no time derivatives, so Y and the tidal sector never touched the
  momenta.  K does.  Making a0 depend on it drags the unbounded combination F - X F_X ~ -g/a0
  straight into the lam_K slot, and the no-ghost condition fails by ~1e8 at the Earth's
  surface -- worse the deeper into the Newtonian regime you go.

  WHAT SURVIVES: the SCALING a0 ~ cH is untouched by this; what fails is putting K inside
  the action as the generator.  Any Route-2 variant must make a0 depend on the cosmological
  K WITHOUT that dependence appearing in the local Lagrangian -- which is precisely the
  'you cannot insert K_background by hand into a covariant action' problem, now with a
  quantitative reason why the naive fix is fatal.""")
