#!/usr/bin/env python3
"""DYNAMICAL make-or-break: does the CAUSAL completion of the un-localized F+ kernel stay ghost-free?
Two levels: (1) discrete real poles (a ghost pole = a real zero of F+ with wrong-sign residue);
(2) the pseudo-differential sqrt(box) branch cut -- its spectral density sign decides unitarity/ghost
on the second sheet (the nonlocal ghost-tower question). All symbolic; verdict HELD for audit."""
import sympy as sp

Z = sp.symbols('Z', positive=True)
u = sp.symbols('u', real=True)                      # u = sqrt(Z)/2
Fp = 4*(1 - (1 + sp.sqrt(Z)/2)*sp.exp(-sp.sqrt(Z)/2))
Fp_u = 4*(1 - (1 + u)*sp.exp(-u))                   # F+ as a function of u=sqrt(Z)/2

print("=== LEVEL 1: discrete real poles -- does F+ add a GHOST pole? ===")
# real zeros of F+ (=poles of the propagator ~ 1/F+). (1+u)e^{-u}=1 ?
h = (1+u)*sp.exp(-u)
print(f"   F+=0  <=>  (1+u)e^-u = 1.  d/du[(1+u)e^-u] = {sp.simplify(sp.diff(h,u))} = -u e^-u <= 0")
print(f"   => (1+u)e^-u strictly DECREASES from 1 (at u=0); equals 1 ONLY at u=0.")
print(f"   => F+ has EXACTLY ONE real zero (Z=0 = the massless graviton), NO extra real zeros.")
res0 = sp.limit(Fp_u/u**2, u, 0)                    # F+ ~ res0 * u^2 near 0 -> residue sign
print(f"   near Z=0: F+ ~ {res0} u^2  (u^2=Z/4)  => F+ ~ (Z/2) -> massless pole residue ~ 1/F+'(0) > 0")
print("   LEVEL 1: HEALTHY -- no extra discrete pole, so NO discrete ghost. (rules out the simplest kill)")

print("\n=== LEVEL 2: the sqrt(box) branch cut -- spectral density sign (ghost-tower test) ===")
# on-shell timelike: Z = -s (s>0). Retarded: sqrt(Z) -> -i sqrt(s) (lower-half prescription).
# => u = sqrt(Z)/2 -> -i*theta, theta = sqrt(s)/2. Compute Im F+ = the spectral weight.
th = sp.symbols('theta', positive=True)
Fp_cut = 4*(1 - (1 - sp.I*th)*sp.exp(sp.I*th))       # u -> -i theta
ImF = sp.simplify(sp.im(sp.expand(Fp_cut.rewrite(sp.cos))))
ImF = sp.simplify(4*(th*sp.cos(th) - sp.sin(th)))    # = derived by hand; verify:
check = sp.simplify(sp.im(sp.expand_complex(Fp_cut)) - 4*(th*sp.cos(th) - sp.sin(th)))
print(f"   Im F+(on cut) = 4(theta cos theta - sin theta)   (verify residual = {check})")
print("   sign of the spectral weight sigma(theta) = theta cos theta - sin theta:")
for tv in [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]:
    val = tv*sp.cos(tv) - sp.sin(tv)
    print(f"     theta={tv}: sigma={float(val):+.4f}  {'(-)' if val<0 else '(+)'}")
print("   small theta: theta cos - sin ~ -theta^3/3 < 0; then OSCILLATES sign as theta grows.")
print("   An OSCILLATING (sign-changing) spectral density = the propagator has an INFINITE tower of")
print("   second-sheet poles with ALTERNATING residues = the classic NONLOCAL GHOST TOWER of a")
print("   NON-ENTIRE form factor (F+ ~ polynomial x e^{-sqrt}, NOT the ghost-free entire form e^{H}).")

print("\n=== HONESTY CAVEAT: which realization? (this scopes the Level-2 claim) ===")
print("   The ghost-tower analysis assumes F+ enters as a FORM FACTOR of the d'Alembertian, f(box),")
print("   with sqrt(box) pseudo-differential. BUT in the repo primitive, Z=4y^2 is the NONLINEAR")
print("   ACCELERATION invariant (Z built from |grad Phi|/a0), NOT box. If F+ is a CONSTITUTIVE function")
print("   of the acceleration invariant (AQUAL-type) with the nonlocality only in box^-1 (elliptic,")
print("   healthier), the sqrt(box) ghost tower does NOT directly apply. So Level 2 KILLS the")
print("   f(box)=F+(box) form-factor realization, but the constitutive-plus-elliptic realization is a")
print("   SEPARATE case. The terminal question INCLUDES settling which realization can source the")
print("   converged eta=1 M(k): a form factor (=> ghost tower, likely dead) or a constitutive+elliptic")
print("   operator (=> must re-derive whether IT can source Psi off the (1,-2) ray without a frame).")
print("\n=== HELD VERDICT (pending adversarial audit) ===")
print("LEVEL 1 clean (no discrete ghost). LEVEL 2 is the wall: the pseudo-differential sqrt(box) gives an")
print("OSCILLATING spectral density => a nonlocal ghost tower on the second sheet -- the 'cascades")
print("through core' worry made concrete. This is a NEGATIVE indicator for the causal completion of the")
print("RAW F+ kernel. NOT a clean kill: (a) ghost-free nonlocal gravities EXIST (Deser-Woodard-type use")
print("box^-1 of CURVATURE, entire-form factors, or a specific causal/'in-in' prescription that avoids the")
print("tower); (b) the tower sign needs the FULL action's propagator, not the kernel alone. So the honest")
print("outcome: the RAW un-localized F+ likely carries the tower, but a ghost-free nonlocal REALIZATION")
print("of the (converged-calc) M(k) is not excluded -- it must use an entire/curvature-based form factor.")
print("=> the door is NARROWED to: find an ENTIRE (ghost-tower-free) nonlocal form factor that reproduces")
print("   both mu=1-e^-y AND the eta=1 M(k). If none exists, the single-metric space CLOSES; if one does,")
print("   it is the chicken. That is the exact terminal question of the whole program.")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"causal-residue","status":"HELD-NEGATIVE-NARROWED",
 "certificate":("LEVEL 1 (discrete poles): F+ has EXACTLY ONE real zero (Z=0, massless graviton, "
   "residue F+'(0)=1/2>0) -- NO extra discrete ghost. LEVEL 2 (causal/sqrt(box) branch cut): the "
   "on-cut spectral weight Im F+ = 4(theta cos theta - sin theta) OSCILLATES sign (starts -theta^3/3<0) "
   "=> infinite second-sheet poles with alternating residues = the NONLOCAL GHOST TOWER of a NON-ENTIRE "
   "form factor. NEGATIVE indicator for the RAW F+ causal completion ('cascades through core' concrete). "
   "NOT a clean kill: ghost-free nonlocal gravities exist via ENTIRE form factors (e^H) or curvature-"
   "based box^-1; the tower sign needs the full-action propagator. TERMINAL question: does an ENTIRE "
   "(tower-free) nonlocal form factor reproduce BOTH mu=1-e^-y AND the converged eta=1 M(k)? none => "
   "single-metric CLOSES; one => the chicken."),
 "numeric_values":{"real_zeros":1,"graviton_residue":"+1/2","spectral_weight":"oscillates (ghost tower)"}}))
