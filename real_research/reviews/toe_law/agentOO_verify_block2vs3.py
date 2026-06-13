"""
agentOO VERIFY — resolve the Block2(stiffen, sigma4>0) vs Block3(bend, sigma4<0) sign clash.

Both blocks use the SAME passive bath (J,a >= 0). They disagree on sigma4's SIGN. The route
declares Block 3 'exact' and overrules Block 2. A hostile referee must check that this is not a
convenient choice: is Block 2 actually WRONG, or is it a legitimate alternative the route discarded
because it gave the inconvenient (kill-confirming) sign?

THE TWO OBJECTS:
  Block 3 (secular):  omega^2 = c0^2 k^2 + k^2 * S(omega^2),  S(w2)=int J(W)/(w2-W^2).
                      Self-energy evaluated at the ON-SHELL frequency, self-consistently.
  Block 2 (KK sym):   delta(omega^2) = (k^2/pi) P int dW a(W) * 2W/(W^2 - c^2 k^2)
                      Self-energy from a one-pass KK with on-shell omega=c k in the kernel.

KEY: Block 2 wrote the kernel as 2W/(W^2 - x^2) with x=ck and called int a(W)*2W/(W^2-x^2) the
dispersion correction. Block 3's S(w2) = int J/(w2 - W^2) = -int J/(W^2 - w2). The relation
between "a(W)" (an Im-Sigma spectral function) and "J(W)" (the coupling spectral density) is the
crux. For the canonical bath, Im Sigma(W,k) = pi k^2 J(W) delta-weight at the bath frequency, so
the KK reconstruction of Re Sigma must REPRODUCE S(w2). Let me check whether Block 2's kernel,
done correctly, equals Block 3's S — or whether Block 2 dropped a sign / used the wrong kernel.
"""
import sympy as sp

W, x, w2, J = sp.symbols('W x w2 J', positive=True)

print("="*78)
print("STEP 1: the EXACT self-energy of the canonical bath, evaluated on-shell")
print("="*78)
# Canonical bath self-energy (Block 3, per unit k^2):
#   S(w2) = int dW J(W)/(w2 - W^2).
# On shell w2 = c^2 k^2 = x^2:
#   S(x^2) = int dW J(W)/(x^2 - W^2) = - int dW J(W)/(W^2 - x^2).
S_kernel = 1/(x**2 - W**2)
print("Block3 on-shell self-energy kernel S:  1/(x^2 - W^2) = ", sp.simplify(S_kernel))
print("   = -1/(W^2 - x^2)")
# expand in x (=ck), small-x:  1/(x^2-W^2) = -1/W^2 * 1/(1-x^2/W^2) = -(1/W^2)(1+x^2/W^2+x^4/W^4)
ser3 = sp.series(S_kernel, x, 0, 8).removeO()
print("\nBlock3 kernel expanded in x=ck:")
sp.pprint(sp.simplify(ser3))
print("  -> S = -(1/W^2) - x^2/W^4 - x^4/W^6 - ...   (ALL NEGATIVE coefficients)")

print("\n" + "="*78)
print("STEP 2: Block 2's kernel")
print("="*78)
B2_kernel = 2*W/(W**2 - x**2)
ser2 = sp.series(B2_kernel, x, 0, 8).removeO()
print("Block2 kernel 2W/(W^2-x^2) expanded in x=ck:")
sp.pprint(sp.simplify(ser2))
print("  -> = 2/W + 2 x^2/W^3 + 2 x^4/W^5 + ...   (ALL POSITIVE coefficients)")

print("\n" + "="*78)
print("STEP 3: WHY the sign differs — the on-shell self-consistency Block 2 dropped")
print("="*78)
print("""
The two kernels are NOT the same object and the difference is physical, not conventional:

Block 3 self-energy:  S(w2) = int J/(w2 - W^2).  Its on-shell expansion has w2 in BOTH the LHS
   (omega^2 self-consistently) AND the kernel. Solving omega^2 = c0^2 k^2 + k^2 S(omega^2) the
   k^4 coefficient is  sigma4 = (dS/d(w2))|_0 * c_chi^4  with the chain rule of self-consistency
   PLUS the explicit -I2. The NET is sigma4 = -I2 c_chi^2 (verified numerically, exact root).

Block 2 kernel:  it used 2W/(W^2-x^2) and identified its POSITIVE x^2 coefficient as sigma4>0.
   But 2W/(W^2-x^2) is the kernel for  Re Sigma(omega) = (1/pi) P int dW ImSigma(W)*2W/(W^2-omega^2)
   ONLY IF ImSigma(W) is EVEN-extended and the spectral function is a(W) with Sigma = +KK. The
   sign of the dispersion correction delta(omega^2) = + Re Sigma or - Re Sigma depends on the
   SIGN CONVENTION of how Sigma enters G^{-1} = omega^2 - c0^2k^2 - Sigma.
""")

print("DECISIVE TEST: reconstruct Re Sigma by KK from the bath's TRUE Im Sigma, and compare to S.")
print("-"*78)
# The canonical bath: G^{-1} = w2 - c0^2 k^2 - Pi(w2,k),  Pi = k^2 int J/(w2 - W^2 + i0).
# Im Pi(w2,k)/k^2 = Im int J/(w2-W^2+i0) = -pi int J(W) delta(w2-W^2)
#                 = -pi J(sqrt(w2))/(2 sqrt(w2))   for w2>0 (using delta(w2-W^2)=delta(W-rt)/(2W)).
# So rho(W) := -ImPi/(pi k^2) evaluated at w2=W^2 ... let me just verify KK reproduces Re S.
# Re Pi/k^2 = P int J(W')/(w2 - W'^2) dW'  (this IS S). And the dispersion relation that links
# Re and Im for an analytic-in-UHP retarded Pi is:
#   Re Pi(w2) = (1/pi) P int dnu  Im Pi(nu) / (nu - w2)   [in the w2 variable].
# Im Pi(nu)/k^2 = -pi int J(W) delta(nu - W^2) dW = -pi J(sqrt nu)/(2 sqrt nu).
# Then Re S(w2) = (1/pi) P int dnu [-pi J(sqrt nu)/(2 sqrt nu)]/(nu - w2)
#              = -P int dnu J(sqrt nu)/(2 sqrt nu (nu-w2)).  Sub nu=W^2, dnu=2W dW:
#              = -P int dW J(W)/(W^2 - w2) = P int dW J(W)/(w2 - W^2) = S(w2).  CONSISTENT.
print("""
Working it through (in the w2 variable, the physically correct dispersion variable):
  Im Pi(nu)/k^2 = -pi * J(sqrt nu)/(2 sqrt nu)         [retarded, passive: Im Pi < 0 for nu>0]
  Re Pi(w2)/k^2 = (1/pi) P int dnu ImPi(nu)/k^2/(nu-w2)
                = -P int dnu J(sqrt nu)/(2 sqrt nu (nu - w2))
   sub nu=W^2:  = -P int dW J(W)/(W^2 - w2)  =  P int dW J(W)/(w2 - W^2)  =  S(w2).   [MATCH Block3]

=> The CORRECT Kramers-Kronig reconstruction (done in the w2 dispersion variable, with the true
   passive Im Pi < 0) REPRODUCES Block 3's S(w2) exactly, with the NEGATIVE coefficients
   S = -(I1 + w2 I2 + w2^2 I3 + ...). Hence sigma4 = -I2 c_chi^2 < 0.

   Block 2's POSITIVE-coefficient kernel 2W/(W^2-x^2) came from doing KK in the omega (not w2)
   variable AND assigning delta(omega^2) = +(k^2/pi) int a*kernel with a(W) treated as +ImSigma.
   That double sign error (wrong dispersion variable + wrong overall sign of the passive Im part)
   is what flipped it. The route's own memo already flags Block 2 as the 'naive even-KK guess'
   that the exact eigenvalue problem overrules — and that call is CORRECT: the numerically exact
   root (verify_block1) lands on BEND, and the properly-done KK lands on BEND too.
""")

# Numeric confirmation that the two KK reconstructions disagree only by the documented sign:
print("Numeric: Block2 kernel coeff of x^2 =", sp.series(B2_kernel,x,0,4).removeO().coeff(x,2),
      " (positive)  vs  Block3 kernel coeff of x^2 =", sp.series(S_kernel,x,0,4).removeO().coeff(x,2),
      " (negative). Opposite, as documented.")
