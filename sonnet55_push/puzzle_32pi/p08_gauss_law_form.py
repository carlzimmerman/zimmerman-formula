"""p08: does the puzzle have a Gauss-law form in the Henneaux-Teitelboim / four-form language?  G = c = 1.
HT/BT: F4 = E vol4 with E constant on shell; rho = E^2/2 = Lambda/(8 pi); the dual current T^mu obeys div T = sqrt(g) (flux = 4-volume).
Test: express the a0-horizon area in terms of the four-form flux / 4-volume and ask whether any coefficient is FIXED by Gauss's law or flux quantisation.
"""
import sympy as sp, sys
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
L,th1,th2,th3,ph=sp.symbols('L th1 th2 th3 ph',positive=True)
# volume of S^4_L by direct integration of the round metric
V4=L**4*sp.integrate(sp.sin(th1)**3,(th1,0,sp.pi))*sp.integrate(sp.sin(th2)**2,(th2,0,sp.pi))*sp.integrate(sp.sin(th3),(th3,0,sp.pi))*2*sp.pi
chk("1 Vol(S^4_L) = 8 pi^2 L^4/3", sp.simplify(V4-8*sp.pi**2*L**4/3)==0)
Lam=3/L**2; Z2=32*sp.pi/3
Aa0=sp.pi*Z2*L**2                      # A = pi/a0^2, a0 = 1/(Z L)
chk("2 A_a0 = (4/3) Lambda Vol(S^4) = 4 Vol/L^2", sp.simplify(Aa0-sp.Rational(4,3)*Lam*V4)==0 and sp.simplify(Aa0-4*V4/L**2)==0)
SdS=sp.pi*L**2
chk("3 A_a0 / S_dS = Z^2 ; S_a0/S_dS = 8 pi/3", sp.simplify(Aa0/SdS-Z2)==0 and sp.simplify(Aa0/4/SdS-8*sp.pi/3)==0)
E=sp.sqrt(2*Lam/(8*sp.pi))
Phi=sp.simplify(E*V4)
print("   4-form flux through S^4:  Phi = E*Vol =",Phi)
# the flux is E*Vol = sqrt(Lambda/(4 pi))*Vol ; a0 enters nowhere: a0 is not a function of the flux unless the coefficient is supplied
a0=1/(sp.sqrt(Z2)*L)
Phi_a0=sp.simplify(Phi.subs(L,1/(sp.sqrt(Z2)*a0)))
chk("4 flux quantisation Phi = n e fixes L^3 (Lambda) for given n, e; it contains NO relation between a0 and Lambda (a0 only enters through Z, which is the input)",
    sp.simplify(sp.diff(Phi,L)/Phi - 3/L)==0)
# 5. what the Gauss law would have to say: A_a0 = (4/3) Lambda Vol_4 with Vol_4 = flux/E  ->  A_a0 = (4/3) Lambda Phi / E
chk("5 A_a0 = (4/3) Lambda Phi/E is an identity once A_a0 := pi/a0^2 with a0 = H/Z (it restates Z^2 = 32pi/3, it does not derive it)",
    sp.simplify(Aa0-sp.Rational(4,3)*Lam*Phi/E)==0)
# 6. mutation: a different coefficient (Milgrom 2 pi: Z_M = 2 pi sqrt(3/ (8 pi)) ...) has an equally good Gauss-law form with a different rational -> no selection
ZM2=(2*sp.pi)**2*sp.Rational(3,8)/sp.pi*sp.Rational(8,3)   # Z_M = 2 pi in units of H, so Z_M^2 = 4 pi^2
AM=sp.pi*(4*sp.pi**2)*L**2
ratio=sp.simplify(AM/(Lam*V4))
chk("6 control: Milgrom's 2 pi gives A_M = %s * Lambda Vol_4 -- also a 'Gauss-law form', with pi-dependence: the form selects nothing"%ratio, ratio!=sp.Rational(4,3))
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
