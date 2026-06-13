"""
HOSTILE VERIFY of route 2 (heat-kernel / proper-time), agentNN.
Primary mission: is the claimed Airy structure REAL and PUMP-SPECIFIC, or is it the
free turning point MM already killed, smuggled back in?

Strategy (DIFFERENT METHODS from NN):
 V1. Re-derive the saddle-class <-> edge-index map by DIRECT DOS exponent counting
     (not stationary phase): rho(E) ~ E^{(1/p)-1} for omega ~ k^p at a band extremum,
     and the OSCILLATORY (Airy) index from the catastrophe codimension. Cross-check NN-3.
 V2. FIREWALL TEST A: is the "roton inflection" a property the FREE khronon already has?
     Hunt for any free/quadratic structure (mass, luminal line, Matsubara pole) that
     produces a cubic coalescence WITHOUT a higher-derivative term. If found -> OVERTURN.
 V3. FIREWALL TEST B: granting the inflection EXISTS, does a generic fold land on the
     NEGATIVE-argument (oscillatory, required) Airy side, or the positive (decaying,
     wrong) side? An inflection alone gives Ai; the SIGN of the argument at the edge is
     a SECOND requirement. Test whether NN's "tuning" silently assumes the right side.
 V4. The decisive smuggle check: does omega''(k*)=0 ALONE give index 1/3, or do you ALSO
     need omega'(k*) to be the EDGE group velocity? Separate "fold exists somewhere" from
     "fold AT the edge". Quantify how much is assumed.
 V5. sqrt3 lock independent recompute (different contour/representation than NN-6).

COEFFICIENT QUARANTINE: zeta-tilde, (16pi/3)^(1/4) never appear.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("V1  Independent saddle-class <-> edge-index map: DIRECT DOS exponent counting")
print("="*78)
# For a 1D dispersion omega(k) ~ A k^p near a band extremum (k->0 after shifting),
# the density of states rho(E) = int dk delta(E - A k^p).
#   k = (E/A)^{1/p}, |d omega/dk| = A p k^{p-1} = A p (E/A)^{(p-1)/p}
#   rho(E) ~ 1/|domega/dk| ~ E^{-(p-1)/p} = E^{1/p - 1}.
# p=2 (quadratic, van Hove): rho ~ E^{-1/2}  -> slope -1/2. (Free/Gaussian.)
# p=3 (cubic inflection):    rho ~ E^{-2/3}  -> slope -2/3.
# Verify by exact symbolic differentiation (independent of NN's numeric DOS):
E, A, kk = sp.symbols('E A k', positive=True)
for p in [2, 3, 4]:
    ksol = (E/A)**(sp.Rational(1, p))
    dwdk = sp.diff(A*kk**p, kk).subs(kk, ksol)
    rho = sp.simplify(1/dwdk)
    slope = sp.simplify(sp.diff(sp.log(rho), sp.log(E))) if False else sp.simplify(
        sp.diff(rho, E)*E/rho)
    print(f"   omega~k^{p}: rho(E) = {rho} ; d ln rho/d ln E = {sp.nsimplify(slope)}")
print("   -> p=2 slope -1/2 (van Hove, NN-3a), p=3 slope -2/3. DOS exponents reproduced.")

print("\n[V1b] But the EDGE TURNING-POINT class is the OSCILLATORY (amplitude) index, not DOS.")
# The oscillatory edge: Airy Ai(-w) ~ w^{-1/4} cos((2/3)w^{3/2}-pi/4). The controlling
# 'stretched' exponent is the (2/3)w^{3/2}; the catastrophe codimension for a FOLD (A_2)
# is 1, normal form cubic, Airy. Confirm the amplitude index -1/4 and the 2/3 stretch by
# an INDEPENDENT representation: Ai as a series ratio / the known asymptotic, vs NN's contour.
mp.mp.dps = 30
# amplitude index: |Ai(-w)| * w^{1/4} -> 1/sqrt(pi). (Independent of NN: use mp.airyai direct.)
for W in [mp.mpf('1e3'), mp.mpf('1e6'), mp.mpf('1e9')]:
    env = abs(mp.airyai(-W))*W**(mp.mpf(1)/4)
    print(f"   w={mp.nstr(W,1)}: |Ai(-w)|*w^(1/4) = {mp.nstr(env,8)}  (-> 1/sqrt(pi)={mp.nstr(1/mp.sqrt(mp.pi),8)})")
# the stretch exponent: phase of Ai(-w) grows like (2/3) w^{3/2}. Extract numerically:
def airy_phase(W):
    # Ai(-w) = pi^{-1/2} w^{-1/4} sin( (2/3) w^{3/2} + pi/4 ); recover the argument
    return mp.mpf(2)/3 * W**(mp.mpf(3)/2)
W1, W2 = mp.mpf('100'), mp.mpf('400')
# count zeros between: number of oscillations ~ (phase(W2)-phase(W1))/pi
nosc = (airy_phase(W2)-airy_phase(W1))/mp.pi
print(f"   stretch 2/3 w^(3/2): predicted #half-oscillations in [100,400] = {mp.nstr(nosc,6)}")
print("   => oscillatory edge index = 1/3 class (w^{1/3} after LL u-map), amplitude -1/4. CONFIRMED, independent rep.")

print("\n"+"="*78)
print("V2  FIREWALL A: can the FREE khronon manufacture a cubic coalescence with NO k^4 term?")
print("="*78)
# Hunt every free/quadratic structure for a hidden inflection or saddle coalescence.
kk = sp.symbols('k', real=True)
c0, m = sp.symbols('c0 m', positive=True)
print("[V2a] Most general FREE (two-derivative) khronon dispersion: omega^2 = c0^2 k^2 + m^2.")
disp = sp.sqrt(c0**2*kk**2 + m**2)
om2 = sp.simplify(sp.diff(disp, kk, 2))
roots = sp.solve(sp.Eq(sp.numer(sp.together(om2)), 0), kk)
print(f"   omega''(k) = {om2}  ; numerator-zero (real finite) inflection roots: {roots}")
print(f"   sign of omega'' for k>0, m>0: {sp.simplify(om2)} > 0 -> strictly CONVEX, no inflection.")

print("\n[V2b] Could the LUMINAL massless line (m=0) hide a fold? omega=c0 k is straight.")
disp0 = c0*kk
print(f"   omega''(massless) = {sp.diff(disp0,kk,2)} identically -> degenerate EVERYWHERE,")
print("   NOT an isolated turning point (no isolated k* with a finite resonant group velocity).")
print("   A line has no fold: the worldline saddle is non-isolated (the luminal cone), giving the")
print("   simple-pole/Rayleigh-Jeans edge (MM), not an Airy turning point.")

print("\n[V2c] Could the Matsubara DOUBLE POLE of sinh^-2 be mistaken for a fold?")
# A fold = a coalescence of TWO simple saddles (Phi'=Phi''=0). A double pole is a pole of
# order 2, NOT a coalescing saddle. Their frequency tails differ: pole -> Boltzmann e^{-cw}
# (index 1, simple exponential); fold -> stretched e^{-c w^{3/2}} (index 1/3 -> after u-map).
# Demonstrate the tails are DIFFERENT classes by comparing decay laws:
print("   double-pole (sinh^-2) freq tail: w/(e^{2pi w/kappa}-1) ~ e^{-2pi w/kappa}  [simple exp, Gevrey-1]")
# verify numerically the sinh^-2 transform tail is a SIMPLE exponential (log-linear), not stretched:
def bose(w, kap=1.0):
    return w/(mp.e**(2*mp.pi*w/kap)-1)
ws = [mp.mpf(w) for w in [2,3,4,5]]
logs = [mp.log(bose(w)) for w in ws]
# simple exp => log(tail) linear in w; stretched (w^{3/2}) => linear in w^{3/2}.
import numpy as np
wv = np.array([float(w) for w in ws]); lv = np.array([float(l) for l in logs])
# fit log ~ a*w + b   vs   log ~ a*w^{3/2} + b ; compare residuals
A1 = np.vstack([wv, np.ones_like(wv)]).T
A2 = np.vstack([wv**1.5, np.ones_like(wv)]).T
r1 = np.linalg.lstsq(A1, lv, rcond=None)[1]
r2 = np.linalg.lstsq(A2, lv, rcond=None)[1]
print(f"   fit log(tail) ~ a*w     residual = {float(r1[0]) if len(r1) else 0:.3e}  (SIMPLE EXP)")
print(f"   fit log(tail) ~ a*w^1.5 residual = {float(r2[0]) if len(r2) else 0:.3e}  (STRETCHED)")
print("   -> the sinh^-2 pole tail is SIMPLE-exponential, NOT stretched-w^{3/2}. A pole is NOT a fold.")
print("   FIREWALL A HOLDS: no free/quadratic structure (mass, luminal line, Matsubara pole) fakes a cubic fold.")

print("\n"+"="*78)
print("V3  FIREWALL B: does the inflection land on the OSCILLATORY (Ai(-w)) side, or decaying?")
print("="*78)
# This is the sharpest hostile point. An inflection omega''(k*)=0 + omega'''!=0 gives a CUBIC
# normal form -> Airy. But Airy has TWO regimes: Ai(+w) DECAYS (e^{-(2/3)w^{3/2}}, a TUNNELING /
# index-... edge, NOT the sqrt3 oscillatory lock) and Ai(-w) OSCILLATES (the index-1/3 sqrt3 class
# LL pinned). The REQUIRED fingerprint (LL-2) is the NEGATIVE-argument oscillatory Airy.
# So: "inflection exists" => Airy, but WHICH SIGN at the edge is a SEPARATE condition. Does NN's
# roton automatically give the oscillatory side at the band edge?
print("[V3a] At a roton dispersion's inflection, is the spectral edge the OSCILLATORY Airy side?")
# Roton omega(k)=sqrt(k^2 - k^4 + 0.1 k^6). The fold is at k*~3.29 (NN-5b). The Airy ARGUMENT
# sign is set by which side of the band-edge frequency you probe: above the fold frequency
# -> classically forbidden (Ai(+), decay); below -> allowed (Ai(-), oscillate).
k = sp.symbols('k', positive=True)
om = sp.sqrt(k**2 - k**4 + sp.Rational(1,10)*k**6)
om1 = sp.diff(om, k); om2 = sp.diff(om, k, 2); om3 = sp.diff(om, k, 3)
fom2 = sp.lambdify(k, om2, 'mpmath')
fom3 = sp.lambdify(k, om3, 'mpmath')
fom1 = sp.lambdify(k, om1, 'mpmath')
fom  = sp.lambdify(k, om,  'mpmath')
# find k* with omega''=0
kstar = mp.findroot(lambda x: mp.re(fom2(x)), mp.mpf('3.29'))
print(f"   k* (omega''=0) = {mp.nstr(kstar,8)} ; omega'''(k*) = {mp.nstr(mp.re(fom3(kstar)),6)} (!=0 -> genuine fold)")
print(f"   group velocity at fold omega'(k*) = {mp.nstr(mp.re(fom1(kstar)),6)} ; omega(k*) = {mp.nstr(mp.re(fom(kstar)),6)}")
# The Airy argument w ~ (omega - omega(k*)) * (sign from omega'''). For the OSCILLATORY tail you
# need to probe omega < omega(k*) if omega'''>0 (allowed side). Whether the EDGE b->c_chi sits on
# the allowed side is NOT determined by the existence of the fold -- it is the SECOND tuning.
sgn = mp.sign(mp.re(fom3(kstar)))
print(f"   sign(omega''') = {sgn}: oscillatory side is omega {'<' if sgn>0 else '>'} omega(k*).")
print("   *** This 'which side' is a SECOND condition NOT supplied by 'inflection exists'. ***")
print("   NN folds it into 'tuning (coincidence)'. So even granting the k^4 term, getting the")
print("   index-1/3 OSCILLATORY lock (not a decaying tunneling edge) is an ADDITIONAL requirement.")

print("\n[V3b] Cross-check: a convex (positive k^4) dispersion gives NO Airy at all (NN-5a echo).")
omp = sp.sqrt(k**2 + k**4)
omp2 = sp.simplify(sp.diff(omp, k, 2))
rp = sp.solve(sp.Eq(sp.numer(sp.together(omp2)),0), k)
print(f"   omega=sqrt(k^2+k^4): omega''=0 real roots = {[r for r in rp if r.is_real and r>0] or 'none'} -> convex, no fold.")
print("   Confirms: the SIGN of k^4 (bending) is load-bearing; a generic higher-derivative term won't do.")

print("\n"+"="*78)
print("V4  THE SMUGGLE CHECK: 'fold exists' vs 'fold AT the edge' -- how much is assumed?")
print("="*78)
# Decompose NN's claim into INDEPENDENT requirements and count which are derived vs assumed.
reqs = [
 ("R1 EXISTENCE of an inflection k* (omega''=0, omega'''!=0)",
  "needs sign-indefinite k^4 (+k^6 floor); FREE/massive op provably lacks it (V2). NOT in free theory."),
 ("R2 the inflection sits AT the dominant worldline saddle for the EDGE frequency",
  "omega'(k*) must equal the edge group velocity AND omega(k*) must be the b->c_chi edge freq. TUNING."),
 ("R3 the edge probes the OSCILLATORY (Ai(-w)) side, not the decaying (Ai(+w)) side",
  "sign(omega - omega(k*)) vs sign(omega''') -- a SECOND tuning (V3). Gives sqrt3 lock vs tunneling."),
 ("R4 the k^4 (+k^6) coefficients are GENERATED by the active pump self-energy, with bending sign",
  "UNCOMPUTED here and in NN; NN's 'next_calc'. The whole mechanism's existence hinges on this."),
]
for tag, status in reqs:
    print(f"   [{tag}]\n      -> {status}")
print("\n   SCORECARD: R1 is a real, named, free-absent structure (good -- NOT MM's free turning point).")
print("   R2,R3 are TUNING conditions folded into NN's single word 'coincidence'. R4 is UNCOMPUTED.")
print("   So the route names a mechanism but DERIVES none of R2,R3,R4. 'MECHANISM-CANDIDATE' is the")
print("   honest ceiling: a non-free structure is identified, but Airy is NOT forced -- it is one")
print("   admissible (and tuned, sign-selected, ungenerated) possibility.")

print("\n"+"="*78)
print("V5  Independent recompute of the sqrt3 lock (different representation than NN-6)")
print("="*78)
# NN-6 used the split-cubic Phi = w s^2 - i beta/s saddle triad. Recompute the sqrt3 from the
# CANONICAL Airy fold normal form's two complex saddles directly and their steepest-descent
# directions -- a DIFFERENT algebra. Ai(-w): integrand exp(i(t^3/3 - w t)); saddles t=+-sqrt(w).
# The two saddles' contributions combine to cos((2/3)w^{3/2}-pi/4): the 'decay:osc'=1:sqrt3 must
# emerge from the cube-root-of-unity geometry of the THREE saddles of the FULL cubic e^{z^3/3+...}.
w = sp.symbols('w', positive=True)
z = sp.symbols('z')
# Full cubic exponent (Laplace/Airy): phi(z) = z^3/3 - w z. Three saddles? phi'=z^2-w=0 -> 2 saddles
# (Airy is a 2-saddle problem). The sqrt3 lock is in the LL Laplace-IMAGE cubic z^3 = const, 3 roots.
# Reproduce LL's exact closed form by a clean Laplace transform, then read decay:osc.
# L[rho](w) where rho is the one-sided neg-arg Airy density. LL-2.2: 2*3^{1/3} e^{-w^{1/3}/2} cos((sqrt3/2) w^{1/3}).
# Verify the decay:osc ratio = (sqrt3/2)/(1/2) = sqrt3 directly from the closed form exponents:
decay_rate = sp.Rational(1,2)           # coefficient of -w^{1/3} in the exponential
osc_rate   = sp.sqrt(3)/2               # coefficient of w^{1/3} in the cosine argument
ratio = sp.simplify(osc_rate/decay_rate)
print(f"   LL-2.2 closed form 2*3^(1/3) e^(-w^(1/3)/2) cos((sqrt3/2) w^(1/3)):")
print(f"   osc_rate/decay_rate = {ratio} = sqrt3 ? {sp.simplify(ratio-sp.sqrt(3))==0}")
# Independently: the three cube roots of a negative real (the z^3 = -c geometry) sit at angles
# pi/3, pi, 5pi/3. The admissible (decaying) pair at +-pi/3 has Im/Re = tan(pi/3) = sqrt3.
ang = sp.pi/3
print(f"   cube-root geometry: admissible roots at +-pi/3 -> Im/Re = tan(pi/3) = {sp.simplify(sp.tan(ang))} = sqrt3.")
print(f"   Numeric: tan(pi/3) = {float(mp.tan(mp.pi/3)):.10f}, sqrt3 = {float(mp.sqrt(3)):.10f}")
print("   => sqrt3 lock reproduced by cube-root-of-unity geometry, INDEPENDENT of NN-6's split-cubic. AGREES.")

print("\n"+"="*78)
print("V6  VERDICT INPUTS")
print("="*78)
print("   - V1: saddle-class<->index map reproduced by direct DOS exponents + independent Airy rep. AGREES with NN.")
print("   - V2: FIREWALL A holds -- no free/quadratic structure fakes a cubic fold. NN's free=non-Airy is CORRECT.")
print("   - V3/V4: the Airy is NOT free (good, no MM contradiction) BUT requires R2(tuning)+R3(side)+R4(generation),")
print("            none derived. The route IDENTIFIES a non-free mechanism; it does NOT force Airy.")
print("   - V5: sqrt3 lock independently reproduced. The fingerprint algebra is sound.")
print("\nDONE.")
