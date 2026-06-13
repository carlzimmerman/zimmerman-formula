"""
agentOO Route 2 — Block 3: CONCRETE solvable model removing the Block1-vs-Block2 sign ambiguity,
then the actual Gibbons-Hawking spectrum's peakedness test.

The Block1/Block2 discrepancy is NOT a contradiction -- it is the whole physics. The sign of
sigma4 is set by whether the dominant bath weight sits ABOVE or BELOW the on-shell khronon
frequency omega_on = c_chi k at the relevant k. We resolve it with an EXACTLY solvable
two-field model (khronon linearly coupled to a continuum of oscillators), where the renormalized
dispersion is the root of an explicit secular equation -- no expansion-convention freedom.

MODEL (standard system+bath, the canonical microscopic realization of a passive linear bath):
  L = (1/2)[ (d_t chi)^2 - c0^2 (grad chi)^2 ]               # bare khronon, sound speed c0
    + sum_W (1/2)[ (d_t phi_W)^2 - W^2 phi_W^2 ]             # bath oscillators, freq W
    - chi * grad . [ sum_W g(W) phi_W ]   (derivative/momentum coupling)

Integrating out phi_W gives the renormalized inverse propagator (per momentum k):
  G^{-1}(omega,k) = omega^2 - c0^2 k^2 - Pi(omega,k),
  Pi(omega,k) = k^2 * int dW J(W) / (omega^2 - W^2 + i0),   J(W)=g(W)^2 spectral density >=0,
the k^2 from the derivative coupling. The DISPERSION omega^2(k) solves G^{-1}=0:
  omega^2 = c0^2 k^2 + k^2 int dW J(W)/(omega^2 - W^2).
This is EXACT; no convention. Solve perturbatively in k for omega^2 = c_eff^2 k^2 + s4 k^4 + ...
and read s4's sign UNAMBIGUOUSLY -- including the on-shell pole structure (omega^2 -> W^2).
"""
import sympy as sp

print("="*78)
print("BLOCK 3a: EXACT secular dispersion, sign of sigma4 with NO convention freedom")
print("="*78)

k = sp.symbols('k', positive=True)
c0 = sp.symbols('c0', positive=True)
# Treat the bath integral moments as symbols (positivity-tracked):
#   I_n = int dW J(W)/W^(2n)   (all >0 for J>=0, IF convergent)
I1, I2, I3 = sp.symbols('I1 I2 I3', positive=True)  # I1=int J/W^2, I2=int J/W^4, I3=int J/W^6
Om2 = sp.symbols('Omega2', positive=True)  # placeholder omega^2

# Self-energy moment expansion: Pi/k^2 = int J/(omega^2 - W^2)
#   = -int J/W^2 * 1/(1 - omega^2/W^2) = -int J/W^2 (1 + omega^2/W^2 + omega^4/W^4 + ...)
#   = -(I1 + omega^2 I2 + omega^4 I3 + ...)      [valid when omega^2 < W^2 for dominant weight]
# So Pi(omega,k) = -k^2 (I1 + omega^2 I2 + omega^4 I3 + ...).
# Secular: omega^2 = c0^2 k^2 + Pi = c0^2 k^2 - k^2(I1 + omega^2 I2 + omega^4 I3)
# Solve order by order: omega^2 = A2 k^2 + A4 k^4 + A6 k^6
A2, A4, A6 = sp.symbols('A2 A4 A6')
om2 = A2*k**2 + A4*k**4 + A6*k**6
lhs = om2
rhs = c0**2*k**2 - k**2*(I1 + om2*I2 + om2**2*I3)
eq = sp.expand(lhs - rhs)
# collect powers of k
sol = {}
e2 = eq.coeff(k,2)
solA2 = sp.solve(e2, A2)
print("k^2 order:  A2 =", solA2)
A2v = solA2[0]
eq2 = eq.subs(A2, A2v)
e4 = sp.expand(eq2).coeff(k,4)
solA4 = sp.solve(e4, A4)
print("k^4 order:  A4 (= sigma4) =", sp.simplify(solA4[0]))
A4v = solA4[0]
eq3 = sp.expand(eq2.subs(A4, A4v))
e6 = eq3.coeff(k,6)
solA6 = sp.solve(e6, A6)
print("k^6 order:  A6 (= sigma6) =", sp.simplify(solA6[0]))
A6v = solA6[0]

print("\n--- SIGN of sigma4 = A4 ---")
print("A4 =", sp.simplify(A4v))
# A2 = c0^2 - I1 (renormalized sound speed^2 = c_chi^2). For stability c_chi^2=A2>0.
# A4 sign:
print("""
A2 = c0^2 - I1 = c_chi^2  (renormalized sound speed squared, must be >0 for a stable mode)
A4 = -I2 * (c0^2 - I1) = -I2 * c_chi^2     <-- the EXACT result, no convention
With I2 = int J(W)/W^4 > 0 (passive bath, J>=0) and c_chi^2>0 (stable mode):

        sigma4 = -I2 * c_chi^2  <  0     ==>  BEND  (roton-capable, Airy side)

*** This MATCHES Block 1, and OVERRULES Block 2's naive even-KK guess. ***
The exact secular solution is unambiguous: integrating out a passive bath with positive
spectral density J(W)>=0 and a derivative coupling produces a STRICTLY NEGATIVE induced k^4.
Block 2's "+sign" came from mis-assigning the symmetric KK kernel; the EXACT eigenvalue problem
settles it. The bend is the generic adiabatic/level-repulsion sign of integrating out a bath
the khronon sits BELOW (the loop pole omega^2->W^2 is approached from below for the IR-dominant
modes), PROVIDED the moment I2=int J/W^4 CONVERGES.
""")
print("sigma6 = A6 =", sp.simplify(A6v))
print("""
sigma6 sign check: with I3=int J/W^6>0, the sextic moment. Print its explicit form above;
the +k^6 STABILIZER requires sigma6 > 0. We test that sign next, and the CONVERGENCE of I2,I3
against the actual GH spectrum (Block 3b) -- because if J(W) is too UV-heavy (featureless
thermal tail), I2,I3 DIVERGE and the naive moment fails: that is precisely the 'featureless bath'
regime where the local expansion breaks and the bend is NOT delivered cleanly.
""")
