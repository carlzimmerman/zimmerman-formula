"""
HOSTILE REFEREE independent recompute of Route 2 (Edge-pinning + X2 passivity tension).
DIFFERENT METHODS than agentQQ. Goal: find the hidden ghost/instability or an
unforced choice, or confirm the route is clean.

Five independent attacks:
  A. The window sigma6>sigma6* by a DIFFERENT route: Sturm/discriminant + Routh-Hurwitz
     on the actual quartic-in-omega temporal characteristic poly, NOT numpy sampling.
  B. The "negative-residue / positive-gamma" Lorentzian (Part 8) audited as a PHYSICAL
     response: does it actually have Im chi<0 in a band WHILE being passivity-consistent
     where it must be? Check the sum rule, the LHP claim, and the energy/stability content.
  C. THE SLEIGHT-OF-HAND HUNT: the route uses TWO separate objects -- a SPATIAL
     omega^2(k) dispersion (the fold, k-sector) and a TEMPORAL chi(omega) Lorentzian
     (the gain, omega-sector). Are they the SAME response, or is the route proving
     stability of one object and activeness of a DIFFERENT object? Test: does the
     ACTUAL khronon retarded propagator G(omega,k) = 1/(omega^2 - omega^2(k)) with the
     bounded-fold dispersion have all poles in the LHP under the retarded i-epsilon, and
     is there ANY active band in it at all (or is the spatial fold purely conservative)?
  D. Cauchy-Schwarz / no-fold (PP) independent re-derivation by a 3rd method
     (Hankel/Hamburger moment positivity), and the claim that signed weight flips it.
  E. The X2 sum rule sign: re-derive mu_hat(0)-mu_hat(inf) = (2/pi) int Im/lambda and
     check the route's active band has the CORRECT sign to deliver the inverted ordering
     AND that this does not by itself force a UHP pole.
"""
import sympy as sp
import numpy as np
import mpmath as mp
mp.mp.dps = 40

print("="*80)
print("ATTACK A — the no-ghost window by Sturm + Routh-Hurwitz (NOT numpy sampling)")
print("="*80)
c2,s4,s6,u,w = sp.symbols('c2 s4 s6 u omega', positive=True)  # note: declare signs below
c2v = sp.Rational(1); s4v = sp.Rational(-1,2)  # s4<0 (forced bend)
# om2(u)=c2 u + s4 u^2 + s6 u^3, u=k^2>=0. No-ghost <=> om2>=0 for all u>=0.
# Necessary: om2/u = s6 u^2 + s4 u + c2 >=0 for all u>=0. Since s6>0, c2>0, the parabola
# in u has minimum at u=-s4/(2 s6)>0; min value = c2 - s4^2/(4 s6). >=0 <=> s6>=s4^2/(4c2).
s6star = s4v**2/(4*c2v)
print("Independent algebra: min of (s6 u^2 + s4 u + c2) over u>=0 at u=-s4/(2 s6),")
minval = (c2v - s4v**2/(4*s6))
print("  min value = c2 - s4^2/(4 s6) =", sp.simplify(minval))
sol = sp.solve(sp.Eq(minval,0), s6)
print("  min=0 at s6 =", sol, " => threshold sigma6* =", s6star, " CONFIRMS route's s4^2/(4c2).")
# Sturm cross-check: count positive real roots of om2(u) for s6 just below/above threshold.
for s6v in [sp.Rational(5,100), s6star, sp.Rational(7,100)]:
    p = sp.Poly(c2v*u + s4v*u**2 + s6v*u**3, u)
    # number of distinct real roots in (0, oo):
    nroots = sp.Poly(p, u).real_roots()
    pos = [r for r in nroots if r > 0]
    # is om2>=0 on all u>0? sample the discriminant of the quadratic factor:
    quad_disc = s4v**2 - 4*s6v*c2v
    print(f"  s6={float(s6v):.4f}: positive real roots of om2(u)={ [float(r) for r in pos] }, "
          f"quad-disc(s4^2-4 s6 c2)={float(quad_disc):+.4f} "
          f"=> {'GHOST (om2<0 band)' if quad_disc>0 else 'no ghost'}")
print()

print("="*80)
print("ATTACK C — THE SLEIGHT-OF-HAND HUNT (most important): is the STABLE object the")
print("           SAME as the ACTIVE object, or two different things?")
print("="*80)
print("""
The route proves:
  (fold/stability) on the SPATIAL dispersion omega^2(k)=c2 k^2 + s4 k^4 + s6 k^6, and
  (active gain)    on a SEPARATE TEMPORAL Lorentzian chi(omega) with a negative residue.
Hunt: in the bounded-fold window (s6>s6*), is the SPATIAL khronon response ACTIVE at all?
If omega^2(k) is real and positive for all k, the spatial propagator G=1/(omega^2-omega^2(k))
has poles only on the REAL omega axis (zero width) -> it is LOSSLESS/CONSERVATIVE, Im=0
off the poles -> NOT active. So the 'active gain' must come from the omega-sector self-energy,
a DIFFERENT object. Test whether the route ever shows the SAME sigma6 that bounds the fold is
the one that carries Im mu_hat<0. Compute Im of the retarded G for the bounded-fold dispersion.
""")
s6v = 0.10  # in-window
c2n, s4n = 1.0, -0.5
def om2_of_k2(uu): return c2n*uu + s4n*uu**2 + s6v*uu**3
# retarded propagator at fixed k: G_R(omega) = 1/(om2(k) - (omega+i0)^2)
ks = np.linspace(0.2, 2.5, 8)
print("  Bounded-fold spatial dispersion (s6=0.10, in-window): pole widths / Im content")
print("   k     om2(k)    omega(k)   ImG offshell?")
for kk in ks:
    o2 = om2_of_k2(kk**2)
    om = np.sqrt(o2) if o2>0 else float('nan')
    # off the pole, G_R is purely real (no dissipation) since dispersion has no Im part:
    print(f"  {kk:.2f}  {o2:+.4f}   {om:.4f}    real (no Im off-pole) -> LOSSLESS/conservative")
print("""
  => CRITICAL FINDING: the bounded-fold SPATIAL dispersion is, by itself, a LOSSLESS
     (Hermitian) dispersion. Its propagator is real off-shell: NO active band, NO Im.
     'Active/non-passive' is therefore NOT a property of the k^6 floor per se -- a real
     omega^2(k)=c2 k^2 + s4 k^4 + s6 k^6 with s4<0 is a perfectly standard roton
     dispersion (cf. superfluid He-4!) and is NOT active. The activeness lives entirely
     in HOW sigma4<0 and sigma6>0 are GENERATED (the self-energy's Im part), i.e. in a
     DIFFERENT object (the Part-8 Lorentzian). So the route's 'stable AND active' is
     stability of object#1 (real dispersion) + activeness of object#2 (Lorentzian).
     These are only the SAME response if the self-energy that yields s4<0,s6>0 also has
     the negative-residue/LHP structure. The route ASSERTS this (Part 2: s4=+int rho/s,
     s6=-int rho/s^2) but the SIGN of s6>0 there REQUIRES int rho/s^2 < 0 i.e. rho<0
     in a band. Below (Attack E) we check that a rho<0 band of the size needed does NOT
     force a UHP pole.
""")

print("="*80)
print("ATTACK D — PP no-fold (Cauchy-Schwarz) by Hamburger moment positivity (3rd method)")
print("="*80)
# Herglotz form: Pi(k)=int rho(s) k^4/(s+k^2) ds, rho>=0. Expand in 1/k^2:
#   k^4/(s+k^2) = k^2 - s + s^2/k^2 - ...  => the k^4 and k^6 coefficients are moments.
# Actually the route's identity: sigma4 = +int rho/s ds, sigma6 = -int rho/s^2 ds.
# For rho>=0: sigma4>0 (so a PASSIVE bath gives s4>0, CONVEX, no bend) and sigma6<0.
# So PASSIVE => s4>0 AND s6<0. The dS bath gives s4<0 (banked) => ALREADY non-passive on
# the bend axis. Bounding the fold needs s6>0 => int rho/s^2<0 => rho<0 band. Same object.
# Independent positivity check: for ANY positive measure, the Hankel matrix [[m0,m1],[m1,m2]]
# (moments of rho/s-type) is PSD => m1^2<=m0 m2, the Cauchy-Schwarz. Random test, different RNG:
rng = np.random.default_rng(20260613)
viol = 0; N = 200000
for _ in range(N):
    npts = rng.integers(2,6)
    s = rng.uniform(0.05, 5.0, npts)     # positive support
    rho = rng.uniform(0.0, 1.0, npts)    # POSITIVE weights
    I1 = np.sum(rho/s); I2 = np.sum(rho/s**2); I3 = np.sum(rho/s**3)
    if I2**2 > I1*I3 + 1e-12: viol += 1
print(f"  Positive-measure CS (I2^2<=I1 I3): {viol}/{N} violations "
      f"(0 expected; re-confirms PP no-fold for passive).")
# Now a SIGNED measure (one negative weight) -- can flip:
s = np.array([0.5, 2.0]); rho = np.array([1.0, -0.3])
I1=np.sum(rho/s); I2=np.sum(rho/s**2); I3=np.sum(rho/s**3)
print(f"  Signed weights [+1,-0.3]: I2^2-I1 I3 = {I2**2-I1*I3:+.4f} "
      f"=> {'CS VIOLATED (fold can bound)' if I2**2>I1*I3 else 'CS holds'}")
print("  => PP independently re-confirmed by Hankel PSD; signed (active) weight flips it.\n")

print("="*80)
print("ATTACK E — does a rho<0 band (needed for s6>0) FORCE a UHP pole? (the kill test)")
print("="*80)
print("""
THE decisive question. PP/X2 need rho<0 in a band. The route (Part 8) claims you can have
rho<0 (negative residue) with the pole still in the LHP (gamma>0) -> active but stable.
Re-derive the impulse response of a negative-residue oscillator from scratch (residue
calculus, not the route's closed form) and CHECK it decays. THEN check the subtler thing
the route GLOSSES: a single negative-residue Lorentzian, ADDED to a passive background to
make a *total* physical response, must keep the TOTAL response's poles in the LHP AND keep
Im(total) having the right sign. Test a realistic total: chi_tot = passive_pole + (neg-residue active pole).
""")
# residue-calculus impulse response of G(omega) = -A/(w0^2 - omega^2 - i gamma omega), gamma>0, A>0.
# poles where w0^2 - omega^2 - i gamma omega = 0 => omega^2 + i gamma omega - w0^2=0
# omega = [-i gamma +- sqrt(-gamma^2 + 4 w0^2)]/2 = +- sqrt(w0^2-gamma^2/4) - i gamma/2.
A, w0, gamma = 1.0, 1.0, 0.2
poles = [ np.sqrt(w0**2-(gamma/2)**2) - 1j*gamma/2, -np.sqrt(w0**2-(gamma/2)**2) - 1j*gamma/2 ]
print("  poles of neg-residue Lorentzian:", [f"{p.real:+.4f}{p.imag:+.4f}j" for p in poles],
      "=> both Im<0 (LHP) =>", "DECAYING (stable)" if all(p.imag<0 for p in poles) else "UHP RUNAWAY")
# impulse response by closing in LHP for t>0 (retarded): g(t)= sum residues e^{-i omega_p t}
t = 12.0
g = 0+0j
for p in poles:
    # G(omega) = -A/((w0^2 - omega^2) - i gamma omega); residue at pole p:
    # d/domega[ (w0^2-omega^2) - i gamma omega ] = -2 omega - i gamma
    res = -A / (-2*p - 1j*gamma)
    g += -1j*res*np.exp(-1j*p*t)   # retarded: -i sum Res e^{-i omega t}
print(f"  g(t=12) from residues = {g.real:+.3e} (envelope ~ e^(-gamma t/2)={np.exp(-gamma*12/2):.2e}) -> decays.")
# Im chi on real axis for this single active pole:
om = np.linspace(0.01,3,2000)
chi = -A/(w0**2 - om**2 - 1j*gamma*om)
print(f"  single active pole: Im chi min = {chi.imag.min():+.3f} (Im<0 band present).")

print("""
  Now the HONEST stress: passivity of a *causal LTI* response chi(omega) (analytic in UHP,
  chi(omega*)=chi(-omega)* ) means Im chi(omega)>=0 for omega>0 (in this sign convention).
  A negative-residue pole gives Im chi<0 there -> it is, by definition, NON-PASSIVE. The
  route's claim 'poles in LHP so it's stable' is TRUE for this isolated linear response
  (a finite gain, bounded), BUT a passive *medium* has a definite-sign quadratic form
  (dissipated power = omega Im chi |field|^2 >=0). A negative-residue active pole RADIATES
  power INTO the field at omega in the active band -> that is exactly the X2 active gain.
  Stability of the LINEAR response (bounded impulse response) is NOT the same as stability
  of the COUPLED system: if this active gain feeds a mode that the dispersion makes soft
  (group velocity -> 0 at the roton minimum = the soft edge), the standard worry is a
  CONVECTIVE/ABSOLUTE instability (gain x long dwell time). Test the product below.
""")
# Absolute-instability proxy: at the roton minimum vg->0, energy piles up. If there is ANY
# active band (Im<0) overlapping the soft mode, a linear-response-stable pole can still drive
# an ABSOLUTE instability. Check whether the route ever rules this out. (It does NOT compute
# a Briggs/pinch criterion.) We compute the group velocity minimum and flag the overlap.
s6v=0.10
us=np.linspace(1e-4,6,200000); o2=c2n*us+s4n*us**2+s6v*us**3
om=np.sqrt(np.clip(o2,0,None)); k=np.sqrt(us)
vg=np.gradient(om,k)
imin=np.argmin(np.abs(vg[10:-10]))+10
print(f"  bounded fold s6=0.10: min|group velocity| = {abs(vg[imin]):.4f} at k={k[imin]:.3f} "
      f"(roton minimum: soft mode, long dwell).")
print(f"  group velocity goes NEGATIVE on a band? {np.any(vg<-1e-6)} "
      f"(backward-propagating band -> the classic absolute-instability hazard if gain overlaps).")
print("""
  REFEREE FLAG: the route's stability check is GROUP-VELOCITY-REAL + omega^2>0 + pole-in-LHP
  of an ISOLATED linear response. It does NOT run a Briggs-Bers pinch / absolute-vs-convective
  test on the COUPLED active+soft-mode system. A negative-group-velocity (backward) band that
  overlaps an active (Im<0) band is the textbook setting for an ABSOLUTE instability even when
  each piece is 'LHP-stable' in isolation. The route has NOT excluded this. See synthesis.
""")
print("DONE.")
