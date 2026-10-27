"""argon_clues: audit of the 'Gauss-Codazzi / Poisson flux mismatch' derivation of Z/2 = sqrt(8pi/3), and the pasted Gaia/ALMA numbers."""
import math, sympy as s
c, G, rho, H = s.symbols('c G rho H', positive=True)
# 1. Friedmann from Gauss-Codazzi: true, standard
print('1. K^2-K_ijK^ij = 6H^2/c^2 = 16piG rho/c^2 -> H^2 =', s.solve(s.Eq(6*H**2, 16*s.pi*G*rho), H**2)[0], '(correct, textbook Friedmann)')
# 2. The step that does the work: WHICH scale the Deser-Levin gate acts on
kin = 2*c*H                                   # CORRECTED: mu_fw(x)=mDL(2x) => a_floor=a0/2, so floor=kappa_dS gives a0=2cH
gDC = c*s.sqrt(G*rho)                         # the pasted choice
Hs = s.sqrt(8*s.pi*G*rho/3)
print('2. DL gate with floor kappa_dS = cH gives a0 = 2cH: a_kin/(c sqrt(G rho)) =', s.simplify((2*c*Hs)/gDC), '=', float(s.simplify((2*c*Hs)/gDC)), ' (observed 0.5)')
print('   observed a0 = g_DC/2; mismatch to DL(kappa_dS) =', s.simplify((2*c*Hs)/(gDC/2)), '= 2Z = 4 sqrt(8pi/3)')
print('   => the paste applies the DL factor 2 to g_DC instead of to cH: i.e. it ASSUMES the gate scale is c sqrt(G rho_DE), not cH. That assumption IS the open number; Friedmann just re-expresses it.')
print('   Same assumption separates "a0 ∝ sqrt(rho_DE)" (tracks DE) from "a0 ∝ H" (rival): not derived, posited.')
# 3. Gaia numbers in the paste
mu = lambda x: (math.sqrt(1+4*x*x)-1)/(2*x)
x = 2.17e-10/9.36e-11
print('3. mu_fw(%.3f) = %.4f (paste 0.8075 ok)' % (x, mu(x)))
def boost(fudge):   # the pasted 'MI locked' formula at 1e4 AU
    a0=9.36e-11; G_=6.6743e-11; M=1.6*1.98847e30; r=1e4*1.495978707e11
    xin=G_*M/r**2/a0; xe=x
    xeff=math.sqrt(xe**2+0.5*xin**2); dmu=lambda y:(1/math.sqrt(1+4*y*y)-mu(y))/y
    mut=mu(xeff); mur=mut+xeff*dmu(xeff); mueff=(2*mur+mut)/3; dec=xin/(xin+xe)
    ml=1-(1-mueff)*(1-fudge*(1-dec)); return (1/math.sqrt(ml)-1)*100
for f in (0.0, 0.3, 0.65, 1.0): print('   pasted WB boost at 1e4 AU with hand-set constant 0.65 -> %.2f: %+.2f%%' % (f, boost(f)))
# 4. ALMA exponent
print('4. a0(z)=a0(0)(1+z)^-0.217 gives z=3 ratio %.3f : exponent chosen to hit 0.74, not derived from rho_DE(z)' % (4**-0.217))
print('   v_flat ratio %.3f ; a0∝H(z) at z=3: v ratio %.2f (arithmetic ok)' % (0.74**0.25, (math.sqrt(0.3153*64+0.6847))**0.25))
