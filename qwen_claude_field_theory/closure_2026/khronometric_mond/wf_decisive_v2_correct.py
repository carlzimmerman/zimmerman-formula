"""
wf_decisive_v2_correct.py -- CORRECTED decisive test.

Earlier map (-2f <-> a0^2 W at the action level) is WRONG: it is inconsistent with
Flanagan's OWN definition of the MOND function.  Flanagan (2302.14846) fixes f through
   varpi(abar) = abar (1 + chibar) = abar mu(abar/a0),   chibar = fbar'(abar)/(2 abar)
   =>   mu(y) = 1 + fbar'/(2 abar)   =>   fbar'(abar) = 2 abar (mu(y) - 1),   y = abar/a0.
This is the physically correct map (matches the SAME interpolating fn mu = W'/y = 1 - e^-y).

Reduced coefficients (Flanagan Eqs 32,33,42,43,53,54), a0=1, y=a/a0, mu = 1 - e^-y:
   chibar   = mu - 1               = -e^-y            (transverse kinetic  h_perp  ~ -chibar)
   fbar'    = 2 y (mu-1)           = -2 y e^-y
   fbar''   = 2(mu-1) + 2 y mu'    = 2(y-1) e^-y      (mu' = e^-y)   (long. kinetic ~ -fbar''/2)
   abar fbar'' - fbar'            = 2 y^2 e^-y  > 0                  (gradient combo, Eq53 part 2)
Flanagan no-ghost h^ij>=0 (Eq43):  fbar'<=0 (transverse) AND fbar''<=0 (longitudinal).
Flanagan Eq54:  f' <= a f'' <= 0.
"""
import sympy as sp, numpy as np
y = sp.symbols('y', positive=True)
mu   = 1 - sp.exp(-y)
mup  = sp.diff(mu,y)
chib = sp.simplify(mu - 1)                       # = -e^-y
fp   = sp.simplify(2*y*(mu-1))                    # fbar'
fpp  = sp.simplify(2*(mu-1) + 2*y*mup)            # fbar''
grad = sp.simplify(y*fpp - fp)                    # abar f'' - f'  (a0=1 so abar=y)
Lperp = sp.simplify(-chib)                        # transverse kinetic coeff  (h_perp)
Lpar  = sp.simplify(-fpp/2)                       # longitudinal kinetic coeff (h_par)

print("chibar        =", chib)
print("fbar'         =", fp)
print("fbar''        =", fpp, "   (factored:", sp.factor(fpp),")")
print("abar f''-f'   =", grad, "   (factored:", sp.factor(grad),")  [gradient combo]")
print("h_perp = -chibar         =", Lperp, "   [transverse KINETIC coeff]")
print("h_par  = -fbar''/2       =", sp.factor(Lpar), "   [longitudinal KINETIC coeff]")
print()

# sign analysis
fL = sp.lambdify(y, Lpar, 'numpy'); fT = sp.lambdify(y, Lperp,'numpy')
fG = sp.lambdify(y, grad,'numpy'); ffpp = sp.lambdify(y, fpp,'numpy')
ys = np.unique(np.concatenate([np.logspace(-6,6,400001), np.linspace(1e-3,30,400001)]))
print("=== SIGN over 1e-6 < y < 1e6 ===")
print(f"  h_perp=e^-y          min={fT(ys).min():+.4e}  -> POS-definite (transverse kinetic OK)")
print(f"  gradient=2y^2 e^-y   min={fG(ys).min():+.4e}  -> POS-definite (gradient OK)")
print(f"  h_par=(1-y)e^-y      min={fL(ys).min():+.6f} @y={ys[np.argmin(fL(ys))]:.4f}  max={fL(ys).max():+.4f}")
print(f"     -> SIGN-INDEFINITE: >0 for y<1, =0 at y=1, <0 for y>1 (LONGITUDINAL GHOST for a>a0)")
print()

# analytic min of h_par = (1-y)e^-y :  d/dy = -(2-y)e^-y = 0 -> y=2
ystar = sp.solve(sp.diff(Lpar,y),y)
print("h_par extremum: d/dy[(1-y)e^-y] =", sp.factor(sp.diff(Lpar,y)), "-> y* =", ystar)
print(f"   worst (most negative) h_par = (1-2)e^-2 = -e^-2 = {-np.exp(-2):.6f}  at y=2 (a=2 a0)")
print(f"   zero crossing at y=1 (a=a0)  <-- Flanagan predicts violation at a~a0. CONFIRMED.")
print()

print("=== GENERAL THEOREM (why this is forced) ===")
print("  fbar'(abar) = 2 abar (mu-1).  Newtonian recovery mu->1 => fbar'->0^- at BOTH")
print("  y->0 (mu->0) and y->inf (mu->1).  fbar' is 0 at both ends, negative between")
print("  => fbar'' MUST cross zero (neg then pos) => longitudinal kinetic -fbar''/2 MUST")
print("  go negative for large y.  Holds for ANY mu with Newtonian limit -> Flanagan no-go")
print("  is UNIVERSAL, not special to 1-e^-y.  MOND sector ALONE cannot avoid it.")
print()

print("=== BACKBONE REQUIREMENT (K^2 UV term supplies A_KH>0 to h_par) ===")
worst = np.exp(-2)
print(f"  Need A_KH + h_par(y) > 0 for all y.  min h_par = -e^-2 = {-worst:.6f} at y=2.")
print(f"  Bounded positive backbone  A_KH > e^-2 = {worst:.4f}  (matched units) SUFFICES.")
print("  c_T^2 = 1/(1-beta) = 1 => beta = 0 ; alpha_eff = 2 beta = 0.")
print("  Longitudinal khronon kinetic normalisation is set by lambda (the (1+lambda)K^2")
print("  term), INDEPENDENT of beta -> A_KH ~ O(1) > 0.135 attainable with beta=0 held.")
print("  Flanagan (Discussion, verbatim): khronometric instabilities 'can be cured by the")
print("  addition of higher spatial derivative terms to the action' -> strategy endorsed.")
print()
print("=== TABLE ===")
print(f"{'y':>7}{'mu':>9}{'h_perp':>9}{'h_par':>10}{'grad':>10}{'A_KH+h_par(.20)':>16}")
for yy in [1e-3,0.1,0.5,0.9,1.0,1.5,2.0,3.0,5.0,10.0,100.0]:
    print(f"{yy:7.3g}{1-np.exp(-yy):9.4f}{np.exp(-yy):9.4f}{(1-yy)*np.exp(-yy):10.5f}{2*yy*yy*np.exp(-yy):10.5f}{0.20+(1-yy)*np.exp(-yy):16.5f}")
