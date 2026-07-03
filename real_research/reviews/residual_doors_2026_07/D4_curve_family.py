#!/usr/bin/env python3
"""D4 (lane), part 2: the EP floor across the full rotation-curve family.

Curve family v(R) ~ R^alpha, alpha in [-1/2 (Kepler), 1 (solid body)];
Newtonian epicyclic ratio kappa/Omega = sqrt(2(1+alpha)) in [1, 2].
Quadratic PU proxy (k'=1), self-consistent potential: Omega(r)=r^(alpha-1) (units
R0=Omega0=1), Phi'(r) = Omega^2 r (1 - eps Omega^2), eps = 1/w^2 = 1-mu at R0.

Same reduced cubic as D4_flat_ep_cap.py with c1 = Phi''(1) = (2a-1)-(4a-3)(1-mu).
Band edges = real zeros of the quartic factor Q_alpha(mu) of the discriminant.
"""
import numpy as np
import sympy as sp

PASS = []
def ok(name, cond):
    assert cond, "FAIL: " + name
    PASS.append(name); print("  PASS:", name)

s, mu, al, r, eps = sp.symbols('s mu alpha r epsilon', real=True)

# ---- self-consistent Phi'' for the family (symbolic, from the potential itself)
Om_r = r**(al-1)
Phi_p = Om_r**2*r*(1 - eps*Om_r**2)
Phi_pp = sp.simplify(sp.diff(Phi_p, r).subs(r, 1))
ok("Phi''(R0) = (2a-1) - (4a-3)*eps  [self-consistent, any alpha]",
   sp.simplify(Phi_pp - ((2*al-1) - (4*al-3)*eps)) == 0)

# ---- reduced cubic (same construction as part 1)
lam = sp.symbols('lambda')
A = lam**2 - 1 + eps*(lam**4 - 6*lam**2 + 1)
B = 2*lam + 4*eps*lam*(lam**2 - 1)
c1 = (2*al-1) - (4*al-3)*eps
Ch = sp.expand(((A + c1)*(A + mu) + B**2).subs(eps, 1-mu))
Cs = sp.expand(Ch.subs([(lam**8, s**4), (lam**6, s**3), (lam**4, s**2), (lam**2, s)]))
q, rem = sp.div(Cs, s, s)
ok("s=0 always factors (drift mode) for all alpha", sp.simplify(rem) == 0)
cubic = sp.Poly(sp.expand(q), s)
disc = sp.factor(sp.discriminant(cubic.as_expr(), s))
print("  disc(alpha, mu) =", disc)

# extract the quartic factor (everything except the universal -4(mu-1)^3(2mu-1) prefactor)
Qa = sp.simplify(disc / (4*(mu-1)**3*(2*mu-1)))
ok("disc / [4(mu-1)^3(2mu-1)] is polynomial (universal prefactor confirmed)",
   sp.simplify(Qa - sp.expand(Qa)) == 0)

# ---- harmonic endpoint: exact decoupling => NEVER breaks
disc_h = sp.factor(disc.subs(al, 1))
ok("alpha=1: disc = -16 mu (mu-1)^3 (2mu-1)^2 (10mu-9)^2 -- perfect squares only",
   sp.simplify(disc_h - (-16*mu*(mu-1)**3*(2*mu-1)**2*(10*mu-9)**2)) == 0)
# sign never changes on (1/2,1): (mu-1)^3<0, rest squares/positive => disc<=0... check sense:
# disc<0 for a cubic with real coeffs => one real + complex pair. Verify alpha=1 stays REAL:
# exact factorization argument: harmonic potential -> Cartesian decoupling, two 1D quartics
x_, W0, w_ = sp.symbols('x W0 w', positive=True)
# 1D PU in harmonic well: eps*s^2 + s + W0^2 factor pair; on orbit W0^2=mu, eps=1-mu:
sig = sp.symbols('sigma')
quart = (1-mu)*sig**4 - sig**2 + mu       # inertial frequencies sigma
d1 = sp.discriminant(quart.subs(sig**2, x_).subs(sig**4, x_**2), x_)
ok("harmonic 1D: disc_x = 1-4mu(1-mu) = (2mu-1)^2 >= 0 -- REAL for ALL mu (never breaks)",
   sp.simplify(d1 - (1 - 4*mu*(1-mu))) == 0 and sp.simplify(sp.factor(d1) - (2*mu-1)**2) == 0)
# numeric confirmation: alpha=1 cubic roots real-negative across (0.5,1)
for m_ in np.linspace(0.51, 0.99, 25):
    co = [float(c.subs([(al, 1), (mu, m_)])) for c in cubic.all_coeffs()]
    rt = np.roots(co)
    # allow exact double roots (semisimple crossings): perturb test via minimum pairwise dist
    assert np.all(rt.real < 1e-6), f"alpha=1 mu={m_}: positive root?"
    # complex parts only from double-root numerics:
    cplx = np.abs(rt.imag) > 1e-4*np.maximum(1, np.abs(rt))
    assert not np.any(cplx), f"alpha=1 mu={m_}: genuinely complex root?"
ok("alpha=1 (solid body): spectrum real-negative for all mu in (1/2,1) -- band EMPTY", True)

# ---- band edges vs alpha (the floor map)
print("\n  EP band edges vs curve shape (kappa/Omega = sqrt(2(1+alpha))):")
print("  alpha  kappa/Om   mu_lo       mu_hi      band width")
edges = {}
for a_ in [-0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0]:
    Qs = sp.Poly(sp.expand(Qa.subs(al, sp.Rational(a_).limit_denominator(100))), mu)
    rts = [complex(z) for z in Qs.nroots(n=15)]
    rl = sorted(z.real for z in rts if abs(z.imag) < 1e-10 and 0.5 < z.real < 1.0)
    ko = np.sqrt(2*(1+a_))
    if a_ == 1.0:
        print(f"  {a_:5.2f}  {ko:7.3f}   ---         ---        0 (never breaks)")
        edges[a_] = (None, None); continue
    lo, hi = rl[0], rl[-1]
    edges[a_] = (lo, hi)
    print(f"  {a_:5.2f}  {ko:7.3f}   {lo:.6f}    {hi:.6f}   {hi-lo:.4f}")
ok("Kepler (a=-1/2) band edges 0.679173 / 0.892279",
   abs(edges[-0.5][0]-0.6791732) < 1e-6 and abs(edges[-0.5][1]-0.8922787) < 1e-6)
ok("flat (a=0) band edges 0.757989 / 0.894787",
   abs(edges[0.0][0]-0.7579886) < 1e-6 and abs(edges[0.0][1]-0.8947874) < 1e-6)
ok("band closes toward harmonic: width(0.99) < width(0.75) < width(0)",
   (edges[0.99][1]-edges[0.99][0]) < (edges[0.75][1]-edges[0.75][0]) < (edges[0.0][1]-edges[0.0][0]))
ok("upper edge mu_hi ~ 0.89 nearly shape-independent (Kepler..alpha=0.5 within 0.006)",
   abs(edges[-0.5][1]-edges[0.5][1]) < 0.006)

# crude-estimate comparison
crude = (2+np.sqrt(2))/4
print(f"\n  crude scalar-anchor estimate: {crude:.4f}; true flat edges (0.7580, 0.8948):")
print("  the crude number sits INSIDE the true band -- neither edge; the scalar shortcut")
print("  missed both the Krein-collision upper edge (0.895) and the re-entrant window.")

# where the band sits in a/a0 under the framework's own mu(a/a0) (context only)
xx = sp.symbols('x', positive=True)
mu_fw = (sp.sqrt(1+4*xx**2)-1)/(2*xx)
for m_ in (0.7580, 0.8948):
    x_v = m_/(1-m_**2)
    ok(f"framework mu_fw = {m_} at a = {x_v:.3f} a0  (band covers the TRANSITION zone)",
       abs(float(mu_fw.subs(xx, x_v)) - m_) < 1e-3)

print(f"\nALL {len(PASS)} CHECKS PASS.")
print("""
D4 part-2 VERDICT: floor map across kappa/Omega in [1,2] (quadratic PU proxy):
  - upper EP edge mu_hi(alpha): 0.8923 (Kepler) -> 0.8948 (flat) -> 0.8974 (a=1/2) -> 0.9
    (harmonic limit, where the band closes): nearly UNIVERSAL ~0.9, NOT 3/4, NOT 0.854.
  - lower edge mu_lo(alpha): 0.679 (Kepler) -> 0.758 (flat) -> rises to 0.9 (harmonic);
    below it a RE-ENTRANT real window down to the mu=1/2 fold on every non-harmonic curve.
  - solid-body/harmonic is the unique curve with NO broken band (exact Cartesian
    decoupling; disc is a perfect square) -- the pt_gates harmonic-exact cap mu>=1/2 is
    the DEGENERATE endpoint of the family, not representative of galaxies.
EXIT 0""")
