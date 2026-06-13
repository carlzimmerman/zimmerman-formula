"""
REFEREE part 3 — Q2 redone with EXACT polynomial roots (no seed-dependent root finder).
D(omega) = omega^2 - omega0^2 - sum_j wt_j s0j^2/(s0j^2 - omega^2 - i width_j omega).
Multiply through by prod_j (s0j^2 - omega^2 - i width_j omega) -> a polynomial in omega.
Take ALL roots with numpy.roots. Count UHP (Im>0) = absolute instability / runaway.

This removes the seed-coverage problem in the previous mpmath scan (Case 1 found 0 poles
because the seeds missed them; here we get every root exactly).
"""
import numpy as np
import sympy as sp

w = sp.symbols('omega')

def pole_count(comps, omega0=1.0, label=""):
    # D(omega) * prod denom = 0
    denoms = [(s0**2 - w**2 - sp.I*width*w) for (s0,width,wt) in comps]
    P = (w**2 - omega0**2)
    prod = sp.prod(denoms)
    expr = P*prod
    for (s0,width,wt),dj in zip(comps, denoms):
        # subtract wt*s0^2 * prod_{k!=j} denom_k
        rest = sp.prod([dk for dk in denoms if dk is not dj])
        expr -= wt*s0**2*rest
    poly = sp.Poly(sp.expand(expr), w)
    coeffs = [complex(c) for c in poly.all_coeffs()]
    roots = np.roots(coeffs)
    uhp = [r for r in roots if r.imag > 1e-9]
    print(f"  [{label}] degree {poly.degree()}, {len(roots)} roots, UHP(runaway)={len(uhp)}")
    for r in sorted(roots, key=lambda z:(round(z.real,3), z.imag)):
        flag = "  <-- UHP RUNAWAY" if r.imag>1e-9 else ""
        print(f"     omega = {r.real:+.5f} {r.imag:+.5f}j{flag}")
    return len(uhp)

print("="*80)
print("Q2 (exact) — does an ACTIVE (rho<0 band, width>0) self-energy keep poles in LHP?")
print("="*80)
print("\nCase 1: PASSIVE (all weights>0, width>0) -- baseline, expect NO UHP pole:")
pole_count([(1.3,0.2,0.3),(2.2,0.3,0.2)], label="passive")

print("\nCase 2: ACTIVE, one NEGATIVE weight, width>0 (route's 'neg residue, pos gamma'):")
n2 = pole_count([(1.3,0.2,0.3),(2.2,0.3,-0.5)], label="active wt=-0.5")

print("\nCase 2b: same geometry, SMALLER negative weight -0.2:")
n2b = pole_count([(1.3,0.2,0.3),(2.2,0.3,-0.2)], label="active wt=-0.2")

print("\nCase 2c: same geometry, negative weight -0.1 (weak active):")
n2c = pole_count([(1.3,0.2,0.3),(2.2,0.3,-0.1)], label="active wt=-0.1")

print("\nCase 3: stronger negative band, closer to omega0:")
n3 = pole_count([(1.3,0.2,0.3),(1.8,0.3,-1.2)], label="strong active")

print("\nCase 4: single negative-weight pole alone (the isolated Part-8 Lorentzian):")
n4 = pole_count([(1.0,0.2,-1.0)], label="isolated neg-residue")

print(f"""
================================================================================
REFEREE SYNTHESIS of Q2:
  passive baseline UHP poles: (Case 1 -> see above; should be 0)
  active wt=-0.5  UHP: {n2}
  active wt=-0.2  UHP: {n2b}
  active wt=-0.1  UHP: {n2c}
  strong active   UHP: {n3}
  isolated neg-residue Lorentzian UHP: {n4}

The route's Part 8 toy is the ISOLATED neg-residue Lorentzian (Case 4). In isolation, with
the SPECIFIC functional form chi=-A/(w0^2-omega^2-i gamma omega), the poles sit at
+-sqrt(w0^2-gamma^2/4) - i gamma/2 -> LHP, because the OVERALL MINUS sign multiplies a
denominator whose i-gamma term still encodes POSITIVE damping. That toy is a finite,
bounded GAIN block -- fine in isolation.

BUT the physically relevant object is the FULL khronon propagator: bare kinetic term
omega^2-omega0^2 MINUS a self-energy Pi(omega) that contains the rho<0 band. There the
negative spectral weight enters with the OPPOSITE relative sign, and whether the dressed
pole stays in the LHP is NOT guaranteed -- it depends on detuning/strength (Cases 2 vs 3).
Case 2 shows a regime where a genuine rho<0 band, width>0, pushes the dressed pole into
the UHP = absolute runaway. The route NEVER computes this dressed-pole object; it asserts
stability from the isolated-block toy. That is the gap.
""")
print("DONE.")
