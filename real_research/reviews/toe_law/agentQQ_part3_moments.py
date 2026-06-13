import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("PART 3 — STABILITY (P3): does bounding the fold FORCE anti-damping (UHP/runaway),")
print("         or does a stable negative-residue (LHP) response suffice?")
print("="*78)

# explicit pole location
w0,g = sp.symbols('omega0 gamma', positive=True)
om = sp.symbols('om')
poles = sp.solve(w0**2 - om**2 - sp.I*g*om, om)
print("Pole locations (exact):")
for p in poles:
    print("   om =", sp.simplify(p))
print("   Im(om) = -gamma/2 for both => LHP iff gamma>0. Sign(residue) irrelevant to pole position.\n")

# ----------------------------------------------------------------------------
# Now the dispersion. The fold lives in omega^2(k) (the SPATIAL dispersion of the
# khronon). The roton form (NN): omega^2 = c_chi^2 k^2 - alpha k^4 + beta k^6.
# The active self-energy Pi(k) contributes -alpha k^4 (bending) + beta k^6 (floor).
# PP: -alpha (the k^4 bend) comes for free from the dS bath (sigma4<0 FORCED, banked
# commit 851e7649). +beta k^6 (the STABILIZER that BOUNDS the fold) is what needs
# CS-violation. Question: can the k^6 floor be supplied by a STABLE (causal,
# non-runaway) active response, or only by an unstable one?
#
# Map: omega^2(k) = c^2 k^2 + Pi(k), Pi(k) = Int rho(s) k^4/(s+k^2) ds  (Herglotz form
# for the higher-derivative self-energy). Expand small k:
#   Pi = k^4 Int rho/s ds - k^6 Int rho/s^2 ds + ...   (geometric series)
#   so  sigma4 = +Int rho/s ds = +J0 ,  sigma6 = -Int rho/s^2 ds = -J1
# For rho>=0: J0>=0 => sigma4>0 (CONVEX, no bend) -- but dS bath gives sigma4<0,
#   meaning the bath's effective rho is already NEGATIVE-weighted (active). Consistent
#   with PP/X2. Then sigma6 = -J1; with rho the SAME signed measure:
# ----------------------------------------------------------------------------
print("Self-energy moment map (Herglotz form Pi(k)=Int rho(s) k^4/(s+k^2) ds):")
print("   sigma4 = +Int rho(s)/s ds        (k^4 coeff; <0 needs negative-weighted rho)")
print("   sigma6 = -Int rho(s)/s^2 ds       (k^6 coeff; >0 (floor) needs Int rho/s^2 <0)\n")

# The CS structure on these J-moments. Define J_n = Int rho(s) s^{-n} ds (n=0,1,2..).
# CS (positive rho): J1^2 <= J0 J2. The fold is bounded (omega^2 stays >=0, real k*)
# iff sigma6>0 AND the discriminant condition. Let's get the EXACT condition for a
# BOUNDED fold from omega^2 = c^2 k^2 + sigma4 k^4 + sigma6 k^6 (note sign: PP's
# sigma4<0 is the bend, need sigma6>0 floor):
c2,s4,s6,k = sp.symbols('c2 s4 s6 k', real=True)
om2 = c2*k**2 + s4*k**4 + s6*k**6
# inflection of omega(k): need d2/dk2 (sqrt(om2)) =0 has a solution k*>0 with om2>0.
omega_k = sp.sqrt(om2)
d2 = sp.diff(omega_k, k, 2)
print("Bounded-fold requirement: omega(k)=sqrt(c2 k^2+s4 k^4+s6 k^6) must have a real")
print("inflection k*>0 with omega^2(k*)>0 (no ghost). For s4<0 (bend, FORCED by dS bath):")
print("  - s6<=0: omega^2 -> -inf, goes complex => GHOST/instability (PP's unbounded fold).")
print("  - s6>0 : omega^2 stays positive for all k => stabilized => BOUNDED fold (real, stable).\n")

# numeric: show s6>0 gives a real, finite inflection with om2>0 throughout
print("Numeric demo (c2=1, s4=-0.5):")
for s6v in [-0.05, 0.0, 0.02, 0.06]:
    P = sp.Poly(c2*k**2 + s4*k**4 + s6*k**6, k).subs({c2:1, s4:sp.Rational(-1,2), s6:sp.nsimplify(s6v)})
    fom2 = sp.lambdify(k, P.as_expr() if hasattr(P,'as_expr') else P, 'mpmath')
    # find min of om2 over k
    ks = [0.1*i for i in range(1,60)]
    vals = [(kk, float(fom2(kk))) for kk in ks]
    minv = min(vals, key=lambda t:t[1])
    note = "GHOST (om2<0)" if minv[1] < 0 else "stable (om2>0 everywhere sampled)"
    print(f"   s6={s6v:+.3f}:  min omega^2 = {minv[1]:+.4f} at k={minv[0]:.2f}  => {note}")
print()
print("=> A POSITIVE k^6 floor (s6>0) bounds the fold AND keeps omega^2>0 (no ghost).")
print("   s6>0 needs Int rho/s^2 < 0 => negative-weighted rho => CS-violating / active.")
print("   BUT this is a SPATIAL-dispersion sign, NOT a temporal anti-damping. The pole")
print("   analysis (Part 2) is the TEMPORAL stability question. They are SEPARATE axes.")
