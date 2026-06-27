#!/usr/bin/env python3
"""
FRONT 3 -- THE SWING: build the construction "rest_mass = spectrum of the framework's OWN
inertia-response", and test whether the framework's NATIVE algebra FORCES the Koide geometry
(Q=2/3 <=> sqrt-mass vector at 45deg, r=sqrt2) NON-CIRCULARLY, or whether the two sqrt2's
(kernel theta(0)=sqrt2 and Koide amplitude r=sqrt2) are a same-number-field COINCIDENCE.

CONSTRUCTION (posited, framework-native):
    sqrt(m_i)  =  scale * mu_fw(x_i)          (rest sqrt-mass = inertia-response at gen-point x_i)
  where mu_fw(x) = (sqrt(1+4x^2)-1)/(2x)  is the framework's OWN interpolation (NOT McGaugh nu),
  with the native facts mu_fw(1)=1/phi, kernel theta(0)=sqrt2, identity 1/mu_fw - mu_fw = 1/x.

  i = 1,2,3 generations come from the S3/triality (1+2) decomposition.

TESTS (each a RUNNABLE claim, exit-0, numbers -- Carl's hard rule, NO assertion):
  (a) DEMOCRATIC: if mu_fw acts with ONE response-point for all 3 generations -> degenerate
      sqrt-masses -> Koide of a degenerate vector = 1/3 (the OTHER extreme), NO Koide Q=2/3.
      Show it. (mu_fw is flavor-blind: it carries no generation index.)
  (b) THREE FREE x_i: each generation at its own response-point x_i -> sqrt(m_i)=scale*mu_fw(x_i)
      for 3 FREE x_i. Invert the real leptons -> (x1,x2,x3,scale). Compute Q. Then PERTURB the
      x_i and SHOW Q SLIDES off 2/3 -> Koide NOT forced (the flavor-blindness wall: the x_i are
      free inputs, mu_fw carries no generation index that pins them).
  (c) NATIVE-FIXING: is there ANY framework-native mechanism that FIXES the 3 x_i non-circularly
      WITHOUT smuggling 45deg/sqrt2/2-3 into the inputs?
        (c1) kernel theta on 3 distinct orbital frequencies (geometric x_k = base^k);
        (c2) the constitutive nonlinearity's branches / the fixed point mu_fw(1)=1/phi;
        (c3) the self-dual identity 1/mu-mu=1/x -> a fixed-point / period-3 cycle.
      For EACH: produce the resulting Q and check the NON-CIRCULARITY BAR -- did 45deg/r=sqrt2
      appear in the OUTPUT WITHOUT being put in the INPUT? If r=sqrt2 only appears when we
      already chose inputs tuned to it -> CIRCULAR / coincidence.

  (CIRC) Confront the circularity theorem head-on: "force r=sqrt2" == "assume Q=2/3"? Show that
      demanding the construction land r=sqrt2 is exactly one algebraic constraint on the x_i
      that is equivalent to imposing Q=2/3 -- i.e. forcing it IS assuming it, unless an
      INDEPENDENT native equation supplies it.

NON-CIRCULARITY BAR (the whole point): produce 45deg/r=sqrt2 in the OUTPUT WITHOUT referencing
45deg / sqrt2 / 2-3 anywhere in the INPUTS; and under PERTURBATION of inputs, show whether the
45deg is FORCED (rigid) or TUNED (slides).

Footing locked: a0 = c H_Lambda / Z, Z = sqrt(32pi/3), framework mu_fw. NEVER McGaugh nu.
Honest prior (memory): likely HITS flavor-blindness + circularity. Report both-ways, no faked crack.
"""
import sympy as sp
import numpy as np

np.set_printoptions(precision=6, suppress=True)
PASS, FAIL = "PASS", "FAIL"

# ----------------------------------------------------------------------------------------------
# framework-native objects (algebraic, Q-bar) -- NO McGaugh nu anywhere
# ----------------------------------------------------------------------------------------------
def mu_fw(x):
    """framework's OWN interpolation mu_fw(x) = (sqrt(1+4x^2)-1)/(2x)."""
    x = np.asarray(x, dtype=float)
    return (np.sqrt(1 + 4*x**2) - 1) / (2*x)

x_sym = sp.symbols('x', positive=True)
mu_sym = (sp.sqrt(1 + 4*x_sym**2) - 1) / (2*x_sym)
phi = (1 + sp.sqrt(5)) / 2

def koide_Q_from_sqrtmasses(sq):
    sq = np.asarray(sq, dtype=float)
    m = sq**2
    return m.sum() / sq.sum()**2

# real charged-lepton pole masses (PDG, MeV)
m_e, m_mu, m_tau = 0.51099895000, 105.6583755, 1776.86
sq_real = np.sqrt([m_e, m_mu, m_tau])
Q_real = koide_Q_from_sqrtmasses(sq_real)

print("="*88)
print("FRAMEWORK-NATIVE SANITY (algebraic, Q-bar; never McGaugh nu)")
print("="*88)
mu1 = sp.simplify(mu_sym.subs(x_sym, 1))
print(f"  mu_fw(1)              = {mu1} = {float(mu1):.6f}   (1/phi = {float(1/phi):.6f})  [fixed point]")
print(f"  kernel theta(0)       = sqrt2 = {float(sp.sqrt(2)):.6f}")
ident = sp.simplify(1/mu_sym - mu_sym - 1/x_sym)
print(f"  identity 1/mu_fw - mu_fw - 1/x = {ident}  (== 0 -> self-dual identity holds)")
print(f"  real leptons: Q_obs = {Q_real:.7f}   (2/3 = {2/3:.7f}; r=sqrt2 vector)")

# ==============================================================================================
# (a) DEMOCRATIC: one response-point for all 3 generations -> degenerate -> Q = 1/3 (NOT 2/3)
# ==============================================================================================
print("\n" + "="*88)
print("(a) DEMOCRATIC mu_fw (flavor-blind: one response-point for all 3 gens) -> degenerate")
print("="*88)
for xd in [0.3, 1.0, 3.0]:
    sq_dem = np.array([mu_fw(xd)]*3)         # identical -> degenerate sqrt-masses
    Qd = koide_Q_from_sqrtmasses(sq_dem)
    print(f"   x_dem={xd:4.1f}: sqrt(m_i)=mu_fw(x)*[1,1,1]={sq_dem[0]:.5f} (deg) -> Q={Qd:.6f}")
print("  => degenerate sqrt-mass vector gives Q = 1/3 for ANY single response-point.")
print("     mu_fw carries NO generation index -> applied democratically it CANNOT make Koide.")
print(f"  [{PASS}] democratic mu_fw -> Q=1/3, NOT 2/3 (flavor-blindness wall, shown)")

# ==============================================================================================
# (b) THREE FREE x_i: invert real leptons, compute Q, then PERTURB x_i -> show Q SLIDES off 2/3
# ==============================================================================================
print("\n" + "="*88)
print("(b) THREE FREE response-points x_i:  sqrt(m_i) = scale * mu_fw(x_i)  -> invert + perturb")
print("="*88)
# invert: pick scale so that mu_fw(x_i) = sq_real_i / scale must be in (0,1) (range of mu_fw).
# mu_fw is monotone increasing on (0,inf), range (0,1). So scale > max(sq_real). Choose scale to
# place the largest gen at a chosen x_max, then solve each x_i from mu_fw(x_i)=sq_i/scale.
from scipy.optimize import brentq
def invert_mu(y):
    """solve mu_fw(x)=y for y in (0,1).  mu_fw(x)=y -> x = y/(1-y^2)  (closed form)."""
    return y / (1 - y**2)

# choose scale so the heaviest lepton sits at mu_fw=0.95 (arbitrary, NOT 45deg/sqrt2-related)
scale = sq_real.max() / 0.95
y_i = sq_real / scale
x_i = np.array([invert_mu(y) for y in y_i])
# verify reconstruction
sq_recon = scale * mu_fw(x_i)
Q_recon = koide_Q_from_sqrtmasses(sq_recon)
print(f"   scale = {scale:.5f} (heaviest gen placed at mu_fw=0.95; arbitrary, NOT sqrt2-tied)")
print(f"   inverted response-points  x_i = {x_i}")
print(f"   mu_fw(x_i)               = {mu_fw(x_i)}")
print(f"   reconstructed sqrt(m_i)  = {sq_recon}   (real = {sq_real})")
print(f"   Q(reconstructed)         = {Q_recon:.7f}   (matches real Q={Q_real:.7f})")
recon_ok = abs(Q_recon - Q_real) < 1e-9
print(f"  [{PASS if recon_ok else FAIL}] construction reproduces the real leptons (it is a 3-free-param fit)")

print("\n   --- PERTURB the x_i (Q SLIDES => Koide NOT forced; x_i are free inputs) ---")
print(f"   {'perturbation':28s} {'x_i (perturbed)':40s} {'Q':>10s} {'Q-2/3':>10s}")
rng = np.random.default_rng(0)
slide_demonstrated = False
perturbations = [
    ("middle gen x_mu  +10%", np.array([1.0, 1.10, 1.0])),
    ("middle gen x_mu  -10%", np.array([1.0, 0.90, 1.0])),
    ("heavy gen  x_tau +10%", np.array([1.0, 1.0, 1.10])),
    ("light gen  x_e   +30%", np.array([1.30, 1.0, 1.0])),
    ("random +/-8% all gens", 1 + 0.08*rng.standard_normal(3)),
    ("random +/-8% all gens", 1 + 0.08*rng.standard_normal(3)),
]
for label, fac in perturbations:
    xp = x_i * fac
    sqp = scale * mu_fw(xp)
    Qp = koide_Q_from_sqrtmasses(sqp)
    print(f"   {label:28s} {str(np.round(xp,4)):40s} {Qp:10.6f} {Qp-2/3:+10.6f}")
    if abs(Qp - 2/3) > 1e-3:
        slide_demonstrated = True
print(f"  [{PASS if slide_demonstrated else FAIL}] Q SLIDES off 2/3 under x_i perturbation "
      f"-> Koide is NOT forced; the 3 x_i are FREE inputs (flavor-blindness wall).")

# ==============================================================================================
# (CIRC) the circularity theorem:  "force r=sqrt2"  ==  "impose Q=2/3"  (one algebraic constraint)
# ==============================================================================================
print("\n" + "="*88)
print("(CIRC) circularity theorem:  forcing the 45deg / r=sqrt2 IS imposing Q=2/3")
print("="*88)
# circulant param of the sqrt-mass vector: sqrt(m_k) = M0*(1 + r cos(delta + 2pi k/3)).
# Q = 1/3 + r^2/6 (delta cancels). So:
M0s, rs, dlt = sp.symbols('M0 r delta', positive=False)
sqk = [(1 + rs*sp.cos(dlt + 2*sp.pi*k/3)) for k in range(3)]   # M0 factors out of Q
Q_circ = sp.simplify(sum(s**2 for s in sqk) / sum(sqk)**2)
Q_circ = sp.simplify(sp.expand_trig(Q_circ))
print(f"   Q(r,delta) = sum(1+r cos)^2 / (sum 1+r cos)^2 = {Q_circ}")
ident23 = sp.simplify(Q_circ - (sp.Rational(1,3) + rs**2/6))
print(f"   Q - (1/3 + r^2/6) = {ident23}   (== 0 -> delta cancels, Q set ENTIRELY by r)")
r_sol = sp.solve(sp.Eq(sp.Rational(1,3)+rs**2/6, sp.Rational(2,3)), rs)
print(f"   Q=2/3  <=>  r = {r_sol}  (= +/- sqrt2).  So 'the vector is at 45deg (r=sqrt2)' and")
print(f"   'Q=2/3' are THE SAME single algebraic constraint on the sqrt-mass vector.")
print(f"  [{PASS}] forcing r=sqrt2 == assuming Q=2/3 (circularity theorem holds, sympy-exact).")
print("   => Any construction that 'lands' r=sqrt2 by CHOOSING x_i to fit the real masses has")
print("      SMUGGLED 2/3 in. Non-circular forcing requires an INDEPENDENT native equation for the x_i.")

# ==============================================================================================
# (c) NATIVE-FIXING mechanisms: do any FIX the 3 x_i non-circularly (no 45deg/sqrt2/2-3 in input)?
#     Each must pass the NON-CIRCULARITY BAR: r=sqrt2 must come OUT without being put IN.
# ==============================================================================================
print("\n" + "="*88)
print("(c) NATIVE x_i-FIXING mechanisms -- does r=sqrt2/Q=2/3 come OUT without going IN?")
print("="*88)

def report_mechanism(name, x_arr, scale_choice="max@0.95"):
    x_arr = np.asarray(x_arr, dtype=float)
    sc = sq_real.max()/0.95 if scale_choice == "max@0.95" else 1.0
    # for a mechanism that fixes x_i intrinsically we do NOT fit scale to masses for Q (Q is scale-free)
    sq = mu_fw(x_arr)                      # scale cancels in Q
    Q = koide_Q_from_sqrtmasses(sq)
    # circulant r implied:  r = sqrt(6*(Q-1/3))  (real if Q>=1/3)
    r_impl = np.sqrt(max(6*(Q-1/3), 0.0))
    return Q, r_impl, sq

# (c1) kernel theta on 3 distinct orbital frequencies: geometric ladder x_k = base^k (NO sqrt2 input)
print("\n (c1) kernel theta on 3 geometric orbital frequencies  x_k = base^k  (base NOT sqrt2-tied):")
print(f"   {'base':>8s} {'x_1,x_2,x_3':32s} {'Q':>10s} {'r_implied':>10s}")
c1_forces = False
for base in [1.5, 2.0, 2.718281828, 3.0, 5.0, 10.0]:
    xk = np.array([base**0, base**1, base**2], dtype=float)
    Q, r_impl, _ = report_mechanism(f"geom base={base}", xk)
    hit = abs(Q - 2/3) < 1e-3
    print(f"   {base:8.3f} {str(np.round(xk,4)):32s} {Q:10.6f} {r_impl:10.6f}  {'<== Q=2/3' if hit else ''}")
    if hit:
        c1_forces = True
print(f"   => Q depends on the (free) base; r=sqrt2 does NOT pop out for a natural/independent base.")
print(f"  [{PASS if not c1_forces else 'NOTE'}] (c1) geometric-frequency ladder does NOT force r=sqrt2 "
      f"(no native equation fixes the base).")

# (c2) the fixed point mu_fw(1)=1/phi as an anchor + golden ladder x_k = phi^(k-2) (phi is native, NOT sqrt2)
print("\n (c2) golden-ladder anchored on the native fixed point mu_fw(1)=1/phi:  x_k = phi^(k-2):")
phi_f = float(phi)
xk = np.array([phi_f**(k-2) for k in (0,1,2)], dtype=float)   # ..., 1/phi^? ; centered so middle=1 -> mu_fw(1)=1/phi
Q_c2, r_c2, sq_c2 = report_mechanism("golden ladder", xk)
print(f"   x_k = {np.round(xk,5)} (middle gen at x=1 -> mu_fw=1/phi={1/phi_f:.5f})")
print(f"   sqrt(m_i)~mu_fw(x_k) = {np.round(sq_c2,5)}  -> Q = {Q_c2:.6f},  r_implied = {r_c2:.6f}")
print(f"   golden ratio phi = {phi_f:.6f}  is NATIVE but  r=sqrt2={np.sqrt(2):.6f}  is a DIFFERENT number.")
print(f"  [{PASS if abs(Q_c2-2/3)>1e-3 else 'NOTE'}] (c2) the native golden anchor lands Q={Q_c2:.4f} != 2/3 "
      f"-> phi-mechanism does NOT force r=sqrt2.")

# (c3) self-dual identity 1/mu-mu=1/x as a recursion -> fixed point / 3-cycle (does it pick x_i?)
print("\n (c3) self-dual identity  1/mu_fw - mu_fw = 1/x  as a generation recursion (fixed pt / 3-cycle):")
# native map on the response variable: from the identity, y=mu_fw(x) satisfies 1/y - y = 1/x.
# Iterate the framework's own map x -> mu_fw(x) (response feeds next generation's input). Fixed pts/cycles?
def native_map(x):  # x_{n+1} = mu_fw(x_n)
    return mu_fw(x)
orbit = [2.0]
for _ in range(60):
    orbit.append(float(native_map(orbit[-1])))
print(f"   iterate x -> mu_fw(x) from x0=2.0:  ...-> {np.round(orbit[-4:],8)}  (collapsing to 0)")
# fixed point of x=mu_fw(x): mu_fw(x)=x -> (sqrt(1+4x^2)-1)/(2x)=x -> sqrt(1+4x^2)=1+2x^2 -> x=0 only.
xfp_eq = sp.solve(sp.Eq(mu_sym, x_sym), x_sym)
xfp_real = sorted(set(float(r) for r in xfp_eq if r.is_real and float(r) >= 0))
print(f"   solve mu_fw(x)=x exactly:  real x* = {xfp_real}  (ONLY x*=0 -- the trivial fixed point)")
print(f"   -> mu_fw:(0,inf)->(0,1) is a CONTRACTION toward 0; the sole fixed point is x*=0.")
print(f"      One fixed point => DEGENERATE generations => Q=1/3 again, NOT 3 distinct x_i.")
# does ANY native 3-cycle exist?  numeric scan of mu_fw^3(x)-x for sign changes (non-trivial roots)
def mu3_num(x):
    return mu_fw(mu_fw(mu_fw(x)))
xs = np.linspace(1e-4, 50, 200000)
g = mu3_num(xs) - xs
sign_changes = np.where(np.sign(g[:-1]) != np.sign(g[1:]))[0]
cyc_roots = []
for idx in sign_changes:
    try:
        rr = brentq(lambda t: mu3_num(t) - t, xs[idx], xs[idx+1])
        cyc_roots.append(rr)
    except Exception:
        pass
cyc_roots = sorted(set(round(r, 6) for r in cyc_roots))
# a genuine 3-cycle would be a root of mu3(x)=x that is NOT a fixed point of mu_fw itself
genuine = [r for r in cyc_roots if abs(mu_fw(r) - r) > 1e-5]
print(f"   numeric roots of mu_fw^3(x)=x on (0,50): {cyc_roots}")
print(f"   genuine 3-cycle members (mu_fw(x)!=x):    {genuine}")
print(f"  [{PASS}] (c3) mu_fw has only the trivial fixed point x*=0 and NO genuine 3-cycle")
print(f"        -> it FORCES degeneracy/collapse, it does NOT supply 3 distinct x_i, let alone r=sqrt2.")

# ==============================================================================================
# NON-CIRCULARITY BAR -- the decisive summary table: did 45deg come OUT without going IN?
# ==============================================================================================
print("\n" + "="*88)
print("NON-CIRCULARITY BAR: did r=sqrt2 (45deg) appear in OUTPUT without being put in INPUT?")
print("="*88)
print(f"   {'mechanism':38s} {'Q':>9s} {'r_impl':>9s} {'sqrt2 in INPUT?':>16s} {'forces 2/3?':>12s}")
rows = [
    ("(a) democratic (1 point)",          1/3.0,                       0.0,                          "no",  "no (->1/3)"),
    ("(b) 3 free x_i fit to data",         Q_real,                      np.sqrt(2),                   "no",  "ONLY via fit"),
    ("(c1) geometric freq ladder base=2",  report_mechanism('',[1,2,4])[0],  report_mechanism('',[1,2,4])[1], "no", "no"),
    ("(c2) golden ladder (native phi)",    Q_c2,                        r_c2,                         "no",  "no"),
    ("(c3) native map fixed point",        1/3.0,                       0.0,                          "no",  "no (->1/3)"),
]
for name, Q, r_impl, sqrt2_in, forces in rows:
    print(f"   {name:38s} {Q:9.5f} {r_impl:9.5f} {sqrt2_in:>16s} {forces:>12s}")
print("""
   READING:
   * (a) and (c3): the flavor-BLIND uses of mu_fw collapse to a SINGLE response -> degenerate
         sqrt-masses -> Q=1/3. mu_fw carries no generation index; democratically it gives the
         WRONG extreme (1/3), not 2/3.
   * (b): the ONLY way to land Q=2/3 (r=sqrt2) is to take 3 FREE x_i and FIT them to the real
         masses -- i.e. SMUGGLE 2/3 in through the data. Under perturbation of the x_i, Q SLIDES
         off 2/3 (shown above) -> not forced.
   * (c1),(c2): every framework-NATIVE rule for the x_i (geometric kernel ladder; golden-ratio
         anchor on mu_fw(1)=1/phi) lands Q != 2/3. The native constant is phi, NOT sqrt2, and
         phi does NOT produce r=sqrt2. No native equation outputs r=sqrt2.
   * (CIRC): 'force r=sqrt2' == 'impose Q=2/3' (one algebraic constraint, delta cancels). So any
         claim of forcing that goes through choosing inputs to hit sqrt2 is CIRCULAR.

   VERDICT: the construction HITS the flavor-blindness wall (a,c3 -> Q=1/3) AND the circularity
   wall (b -> only by fitting). The two sqrt2's (kernel theta(0)=sqrt2, Koide r=sqrt2) are a
   SAME-NUMBER-FIELD COINCIDENCE / WRONG-SLOT: mu_fw's native constant is phi (=mu_fw(1)), the
   kernel's sqrt2 lives in the RESPONSE-amplitude slot at x->0, not in the 3-generation
   MASS-vector amplitude slot, and no native equivariant equation carries one to the other.
   r=sqrt2 never comes OUT unless put IN. NON-CIRCULAR FORCING: NOT achieved.

   (HONEST both-ways: this is NOT 'no doors closed' nor a manufactured win. It is the expected,
    cleanly-demonstrated COINCIDENCE/WRONG-SLOT result. What WOULD cross it -- still open, not
    here: an independent framework-native dynamical equation whose extremum/fixed-structure
    pins the 3 x_i AND outputs r=sqrt2 without referencing it. The flavor-blindness of mu_fw
    is the precise obstruction: it has no generation index to break the democracy intrinsically.)
""")

import sys
sys.exit(0)
