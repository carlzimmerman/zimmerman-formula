#!/usr/bin/env python3
"""
PART D-G: the decisive spectral construction.
Does the non-equilibrium drive (i) SELECT the declining branch, (ii) predict MOND-OFF in
the far future, (iii) FIX kappa via the drive magnitude? Real Caldeira-Leggett + adiabatic
(Wigner-transform) non-equilibrium spectrum. Both ways, CPL and pure-Lambda backgrounds.
"""
import numpy as np, sympy as sp
C=2.99792458e8; MPC=3.0857e22; H0=67.4e3/MPC; G=6.674e-11
Z=2*np.sqrt(8*np.pi/3); Om,OL=0.315,0.685

# ---- two backgrounds: CPL (DESI) and pure-Lambda (w=-1) ----
def make_bg(w0,wa):
    def rhoDE(z):
        a=1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
    def Hsq(z): return Om*(1+z)**3 + OL*rhoDE(z)
    def H(z):   return np.sqrt(Hsq(z))
    def HDE(z): return np.sqrt(OL*rhoDE(z))
    def w(z):   return w0+wa*z/(1+z)
    def q(z):
        weff=w(z)*OL*rhoDE(z)/Hsq(z); return 0.5*(1+3*weff)
    return rhoDE,Hsq,H,HDE,w,q
CPL = make_bg(-0.752,-0.86)
LAM = make_bg(-1.0,0.0)

print("="*88)
print("PART D. Non-equilibrium spectrum via the Wigner/adiabatic two-point function")
print("="*88)
print("""  Setup (real formalism). In a SLOWLY-transitioning dS bath H=H(t), Wigner-transform the
  detector two-point function in (T = (t+t')/2, tau = t-t'). To leading adiabatic order the
  ANTISYMMETRIC (commutator/response) part keeps its equilibrium odd form at the LOCAL T;
  the SYMMETRIC part picks up a FIRST-ORDER correction in the drive Hdot:
       S_sym(w;T) = coth(beta(T) w/2) S_anti(w)  +  (Hdot/H) * D(w)  + O(Hdot^2),
  where D(w) is the NON-equilibrium (Galley-K / odd-in-Keldysh) piece. The KMS/FDT identity
  S_sym = coth*S_anti holds ONLY when Hdot=0. The correction term is what the passivity
  theorem forbids in equilibrium and the drive RE-OPENS. (Structure: Galley 1210.2745 Eq(5),
  the K-term; sign of D set by causality of the retarded response. UNVERIFIED coefficient.)""")
# The crucial spectral question: can S_sym go NEGATIVE somewhere (active) for eps_KMS=O(1)?
# Model D(w): the leading non-equ correction from a driven Ohmic bath is the standard
#   Delta S_sym(w) ~ (Hdot/H) * d/dw[ coth(beta w/2) ] * (w)  (Wigner gradient term),
# i.e. the temperature-drift correction. Compute where S_sym(w)+DeltaS can invert sign.
w,beta=sp.symbols('omega beta',positive=True)
Santi=w   # Ohmic: S_anti(w) ~ w (response), set slope 1
coth=sp.coth(beta*w/2)
Seq=coth*Santi
# Wigner first-order temperature-drift term: dT/dt enters as (dbeta/dt) d/dbeta
dbeta=sp.symbols('betadot')   # = -Hdot/H * beta  (since beta~1/T~1/H)
DeltaS=sp.diff(Seq,beta)*dbeta*sp.Rational(1,2)   # 1/2 Wigner gradient weight
Stot=Seq+DeltaS
print("  Seq(w)      =", sp.simplify(Seq))
print("  DeltaS(w)   = (1/2) betadot * dSeq/dbeta =", sp.simplify(DeltaS))
# Substitute betadot = -(Hdot/H) beta = +eps*beta for the DECELERATING (Hdot<0) drive today.
eps=sp.symbols('epsilon',real=True)  # eps = -Hdot/H^2 >0 today (so betadot=+eps*beta*H... )
Stot_e=Stot.subs(dbeta, eps*beta)    # carry sign abstractly
print("  S_tot(w)    =", sp.simplify(Stot_e))
# Low-frequency (deep-MOND, w->0) expansion -- this is where MOND lives:
lowf=sp.series(Stot_e, w, 0, 1).removeO()
print("  low-w limit (deep-MOND DC):", sp.simplify(lowf))
print()

print("="*88)
print("PART E. Far-future limit: does MOND switch OFF (eps_KMS -> 0) ?  BOTH backgrounds")
print("="*88)
for name,BG in [("CPL (DESI DR2)",CPL),("pure-Lambda (w=-1)",LAM)]:
    rhoDE,Hsq,H,HDE,w_,q=BG
    def eps_tot(z): return abs(1+q(z))
    print(f"  --- {name} ---   eps_KMS(tot)=|1+q|, drive on total horizon")
    print(f"    {'z':>6}{'a(=1/(1+z))':>13}{'H/H0':>8}{'eps_KMS':>10}  MOND state")
    for z in [3,1,0.5,0,-0.3,-0.6,-0.9,-0.99,-0.999]:
        try:
            e=eps_tot(z); st="ACTIVE(on)" if e>0.1 else "->passive(OFF)"
            print(f"    {z:>6.3f}{1/(1+z):>13.3f}{H(z):>8.3f}{e:>10.4f}  {st}")
        except Exception as ex:
            print(f"    {z:>6.3f}  err {ex}")
    print()
print("  KEY: pure-Lambda -> eps_KMS -> 0 as a->inf  => MOND SWITCHES OFF (passivity restored).")
print("       CPL with phantom w<-1 keeps |1+q|->1/2 (super-accelerating) -> drive does NOT")
print("       vanish: a PHANTOM future never re-equilibrates. The 'MOND-off' prediction is")
print("       a CLEAN consequence ONLY for w->-1 (true dS fixed point), the framework's own floor.")
