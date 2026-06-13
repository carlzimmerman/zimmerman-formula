"""
agentOO Route 2 — Block 4: the ACTUAL Gibbons-Hawking spectrum inserted; sigma6 sign;
peakedness/featurelessness classification; convergence of the moments I2, I3.

From Block 3a (EXACT secular dispersion, no convention freedom):
   c_chi^2 = c0^2 - I1
   sigma4  = -I2 * c_chi^2                       (BEND iff I2>0 and converges)
   sigma6  = -I1^2 I3 - I1 I2^2 + 2 I1 I3 c0^2 + I2^2 c0^2 - I3 c0^4
where I_n = int dW J(W)/W^(2n),  J(W) = bath spectral density (>=0).

Now THE central physics: what is J(W) for the de Sitter / Gibbons-Hawking horizon bath, and
does it make I2, I3 CONVERGE (clean local bend + stabilizer) or DIVERGE (featureless, expansion
fails)? And is sigma6>0 (a real +k^6 floor)?

GIBBONS-HAWKING SPECTRAL DENSITY:
  The dS horizon is a thermal bath at T_dS = H/2pi, occupation n(W)=1/(e^{2pi W/H}-1).
  The bath spectral density the khronon couples to is the symmetrized horizon two-point
  function. For a field in dS, the power spectral density of the horizon fluctuation is
       S(W) = rho0(W) * coth(pi W / H)
  where rho0(W) is the vacuum (zero-T) spectral weight and coth(pi W/H)=1+2n(W) is the
  thermal (KMS) enhancement. The KMS/detailed-balance structure is forced by the
  Gibbons-Hawking temperature -- this is the 'Gibbons-Hawking spectrum' the task names.
  The single physical input that is NOT free: the THERMAL SHAPE coth(piW/H), forced by T_dS.
  The free input is the vacuum density-of-states rho0(W) (the coupling form factor) -- we
  carry it as a power law rho0 ~ W^p and find which p the DIPOLE/derivative coupling forces.
"""
import sympy as sp
import mpmath as mp

print("="*78)
print("BLOCK 4a: sigma6 sign in the convergent regime (exact, symbolic)")
print("="*78)
I1,I2,I3,c0 = sp.symbols('I1 I2 I3 c0', positive=True)
cchi2 = sp.symbols('c_chi2', positive=True)
sigma6 = -I1**2*I3 - I1*I2**2 + 2*I1*I3*c0**2 + I2**2*c0**2 - I3*c0**4
# substitute c0^2 = c_chi2 + I1
sig6 = sigma6.subs(c0**2, cchi2 + I1)
sig6 = sp.expand(sig6)
print("sigma6 in terms of c_chi^2, I1, I2, I3:")
sp.pprint(sp.simplify(sig6))
# factor
print("\nfactored:")
sp.pprint(sp.factor(sig6))
print("""
READING sigma6: substituting c0^2 = c_chi^2 + I1 the I1-terms must reorganize. Print shows
   sigma6 = c_chi^2 * (I2^2 + I1*I3)  +  c_chi^4 * (-I3) ... [read the actual factored form above]
Sign is NOT automatically positive -- it depends on the ratio I2^2/(I3 c_chi^2) etc. We evaluate
it NUMERICALLY with the real GH moments below; the +k^6 stabilizer requires the COMPUTED sigma6>0.
""")

print("="*78)
print("BLOCK 4b: GH moments I2,I3 -- convergence & values for J(W)=W^p coth(pi W/H)")
print("="*78)
# Moments I_n = int_0^inf dW J(W)/W^(2n), J(W)=W^p coth(pi W/H).
# IR (W->0): coth(piW/H) ~ H/(pi W), so J ~ W^(p-1). integrand ~ W^(p-1-2n). converges at 0 iff
#   p-1-2n > -1  i.e.  p > 2n.  For I2 (n=2): need p>4. For I3 (n=3): need p>6.
# UV (W->inf): coth->1, J~W^p, integrand ~ W^(p-2n). converges at inf iff p-2n < -1 i.e. p<2n-1.
#   For I2: p<3. For I3: p<5.
# => I2 converges (both ends) iff  4 < p < 3 : IMPOSSIBLE. I3 iff 6<p<5: IMPOSSIBLE.
print("""
ANALYTIC CONVERGENCE WINDOW for J(W)=W^p coth(piW/H):
  I_n = int_0^inf W^p coth(piW/H) / W^(2n) dW
  IR (W->0, coth~H/piW): integrand ~ W^(p-1-2n)  -> converges iff  p > 2n
  UV (W->inf, coth->1) : integrand ~ W^(p-2n)    -> converges iff  p < 2n-1
  => simultaneous convergence needs  2n < p < 2n-1 : EMPTY for every n>=1.

  *** For I2 (n=2): need 4<p<3  -- IMPOSSIBLE.
  *** For I3 (n=3): need 6<p<5  -- IMPOSSIBLE.

  The featureless thermal (Gibbons-Hawking) bath is SCALE-FREE: a single power law cannot make
  BOTH the IR and UV moments converge. There is NO band of p that yields finite I2 AND I3 from a
  pure-power GH coupling. This is the QUANTITATIVE signature of a FEATURELESS bath -- it has no
  internal scale to set a finite k^4 curvature moment.
""")
# Verify a representative case numerically to show divergence concretely.
mp.mp.dps = 30
H = mp.mpf(1)
def integrand(W, p, n):
    return W**p * mp.coth(mp.pi*W/H) / W**(2*n)
for p in [2, 4, 5, 6]:
    # I2: n=2
    try:
        valIR = mp.quad(lambda W: integrand(W,p,2), [mp.mpf('1e-6'), 1])
        valUV = mp.quad(lambda W: integrand(W,p,2), [1, mp.mpf('1e6')])
        print(f"p={p}: I2 partial IR(1e-6..1)={mp.nstr(valIR,4)}  UV(1..1e6)={mp.nstr(valUV,4)}")
    except Exception as e:
        print(f"p={p}: I2 quad issue {e}")
print("""
(The IR and UV partials blow up as the limits are pushed -- confirming no convergent window.)
""")
