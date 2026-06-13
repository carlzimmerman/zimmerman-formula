"""
REFEREE part 5 — DEFINITIVE, exact, convention-pinned. A manifestly-correct retarded
self-energy from a sum of REAL-axis spectral poles, EXACT polynomial roots (no seeds).

Construction (textbook): retarded self-energy with spectral density
   rho(nu) >= 0  (passive),  rho(nu) on nu>0, extended oddly so Pi is even in omega.
Discretize rho as a sum of delta functions at nu_j>0 with weights g_j:
   Pi_R(omega) = sum_j g_j * 2 nu_j / (nu_j^2 - (omega+i0)^2).
This is the EXACT discrete spectral rep. It is analytic in the UHP. Passivity <=> all g_j>0.
Dressed propagator: D(omega) = omega^2 - omega0^2 - Pi_R(omega) = 0.
Clear denominators -> exact polynomial -> ALL roots via numpy. With the +i0, retarded poles
of a PASSIVE response are guaranteed in the closed LHP (Im<=0). Flip ONE g_j<0 (the active
band needed for sigma6>0) and see if a root crosses to the UHP.

Convention pin: the retarded G_R(omega)=1/(omega^2-omega0^2-Pi_R). On the real axis just
above, Im Pi_R(omega) = -pi sum g_j [delta(omega-nu_j)-delta(omega+nu_j)] * (...). The
spectral function (density of states) ~ -Im G_R/pi >=0 requires the g_j>0 -- standard.
We verify the passive case has ALL poles in the (closed) LHP, establishing the baseline,
then test the active flip. This is convention-robust because we read stability off the
ACTUAL pole locations of the dressed propagator, not off a sign label.
"""
import numpy as np
import sympy as sp

w = sp.symbols('omega')

def dressed_roots(spec, omega0=1.0, label="", eta=0.0):
    # spec: list of (nu_j, g_j). Pi = sum g_j*2 nu_j/(nu_j^2 - omega^2) (retarded: omega->omega+i eta)
    # Use a small width eta to regularize delta-poles into the LHP correctly (retarded).
    # Pi_j = g_j * 2 nu_j / (nu_j^2 - omega^2 - i*eta*omega)  (eta>0 small = retarded broadening)
    denoms=[(nu**2 - w**2 - sp.I*eta*w) for (nu,g) in spec]
    prod=sp.prod(denoms)
    expr=(w**2-omega0**2)*prod
    for (nu,g),dj in zip(spec,denoms):
        rest=sp.prod([dk for dk in denoms if dk is not dj])
        expr -= g*2*nu*rest
    poly=sp.Poly(sp.expand(expr), w)
    coeffs=[complex(c) for c in poly.all_coeffs()]
    roots=np.roots(coeffs)
    uhp=[r for r in roots if r.imag>1e-9]
    print(f"  [{label}] eta={eta}: deg {poly.degree()}, UHP(runaway)={len(uhp)}")
    for r in sorted(roots,key=lambda z:(round(z.real,3),z.imag)):
        flag="  <-- UHP RUNAWAY" if r.imag>1e-9 else ""
        print(f"     omega={r.real:+.5f}{r.imag:+.5f}j{flag}")
    return len(uhp)

print("="*80)
print("DEFINITIVE dressed-pole test, exact roots, retarded broadening eta>0")
print("="*80)
print("""
Baseline must hold: PASSIVE (all g>0) with retarded eta>0 -> ALL poles Im<=0 (LHP).
""")
for eta in [0.0, 0.1]:
    print(f"\n--- eta={eta} ---")
    print(" PASSIVE g>0:")
    dressed_roots([(1.5,0.3),(2.5,0.2)], label="passive", eta=eta)
    print(" ACTIVE one g<0 (active band for sigma6>0), modest:")
    dressed_roots([(1.5,0.3),(2.5,-0.4)], label="active -0.4", eta=eta)
    print(" ACTIVE one g<0, stronger:")
    dressed_roots([(1.5,0.3),(2.5,-1.0)], label="active -1.0", eta=eta)
    print(" ACTIVE band near the bare resonance (detuning small):")
    dressed_roots([(1.2,0.5),(1.4,-0.6)], label="active near-res", eta=eta)

print("""
================================================================================
NOTE ON CONVENTION (decisive): with retarded broadening eta>0 the spectral function is
   rho_DOS(omega) = -Im G_R(omega)/pi.
A PASSIVE medium has rho_DOS>=0, realized by g_j>0 in this rep, and the dressed poles MUST
lie in the LHP (this is the Herglotz/positive-real theorem -- passive => stable). The flip
g_j<0 is the active/negative-spectral-weight band. The test reads the ACTUAL dressed-pole
half-plane. If the passive baseline is clean (all LHP at eta>0) and an active flip produces
a UHP pole, then 'bound the fold by a negative-weight band' generically buys an absolute
instability unless tuned -- the route's 'stable' is then NOT generic, contradicting Part 7-8's
sweeping claim. If even active stays LHP, the route survives this test.
""")
print("DONE.")
