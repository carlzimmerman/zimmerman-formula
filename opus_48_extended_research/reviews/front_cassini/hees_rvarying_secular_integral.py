"""
RIGOROUS r-varying correction to the framework's induced s^TX bound.

QUESTION (the one remaining computational door on Front A / Cassini s^TX):
  The Hees-2016 / Bailey-Kostelecky-2006 (BK) secular planetary bound on s_bar^{munu}
  is derived assuming a CONSTANT s_bar background. The Zimmerman framework induces
      s_bar(r) = (a0 / 2|a|) (u^mu u^nu)_traceless ,  |a| = GM/r^2
  so the spurion AMPLITUDE varies around the orbit as
      s_bar(r) = s_bar(a) * (r/a)^2 .
  "Evaluate at a" (the banked 8.68e-10 Saturn value) is therefore an approximation.
  Does inserting the true r^2-varying s_bar into the BK secular-drift INTEGRAND and
  orbit-averaging make the framework's EFFECTIVE constrained s^TX (and hence the
  margin vs the 1.3e-9 bound) TIGHTER or LOOSER than the ~1.5x "evaluate-at-a" value?

WHY THE NAIVE <(r/a)^2>_t IS NOT THE ANSWER:
  The secular rate is NOT a plain time-average of s_bar. It is
      <element>_dot = (1/T) integral over orbit of [ Gauss geometric kernel(f) * alpha'(f) ] dt
  where the BK perturbing acceleration alpha'(f) ~ GM*s/r^2 ALREADY carries r^{-2}, and
  dt = r^2/(n a^2 sqrt(1-e^2)) df ALREADY carries +r^2. For CONSTANT s these cancel and
  the rate reduces to the clean (a,e,i,n)-only Eq.7/170. The framework multiplies s by
  (r/a)^2, so a net (r/a)^2 survives -- but it is weighted by the ACTUAL secular
  integrand K(f) = [Gauss kernel(f)] * [angular projection of the s-tensor onto P,Q,k(f)],
  which is an f-DEPENDENT weight, NOT flat. The honest enhancement is the ratio of two
  full secular integrals:
      eta = < (r/a)^2 * K(f) >_f  /  < K(f) >_f
  evaluated for the specific element (Omega or omega) and the specific s-tensor structure
  that the s^TX coefficient feeds. THAT is what this script computes -- the genuine O(1)
  kernel weighting, in EITHER direction.

PRIMARIES (extracted by pdftotext in the parent workflow, structure verbatim):
  Bailey & Kostelecky 2006, gr-qc/0603030, PRD 74 045001:
     perturbing accel Eq.165, Keplerian insert Eq.167, true-anomaly average l.4338-4343,
     secular rates Eq.168-171, perihelion-shift Eq.189-190.
  Hees, Bailey, Le Poncin-Lafitte, Bourgoin et al. 2015, arXiv:1508.03478, PRD 92 064049:
     secular rates Eq.7a/7b, six-planet INPOP10a inputs Table I, s^TX fit Table II.

QUARANTINE: a0 = 9.36e-11 is the framework INPUT and is unchanged here. This script
pins ONLY the kernel-weighting O(1); it derives nothing about a0/Z/kappa.

BOTH-WAYS: report the honest sign and size. If r-varying TIGHTENS toward ~1x, say so;
if it LOOSENS toward ~3-6x, say so.
"""
import numpy as np
import sympy as sp
from scipy.integrate import quad

# ----------------------------------------------------------------------------------
# 0. real planetary elements (a in AU, e dimensionless, i in deg).  IAU/INPOP values.
#    Saturn = lowest-acceleration well-tracked body in the Hees six -> worst corner.
# ----------------------------------------------------------------------------------
PLANETS = {
    # name      a(AU)     e        i(deg, to ecliptic)
    'Mercury': (0.38710, 0.20563, 7.005),
    'Venus':   (0.72333, 0.00677, 3.395),
    'Earth':   (1.00000, 0.01671, 0.000),   # EMB
    'Mars':    (1.52368, 0.09340, 1.850),
    'Jupiter': (5.20260, 0.04849, 1.303),
    'Saturn':  (9.55491, 0.05551, 2.489),
}

# evaluate-at-a magnitudes |s^TX(a)| from the banked dipole calc (a0 r^2/2GM * beta n_X).
# These scale exactly as a^2 (|a|=GM/r^2). Anchor: Saturn = 8.68e-10 at a=9.55 AU.
S_SAT_AT_A = 8.68e-10
def s_at_a(a_AU):
    return S_SAT_AT_A * (a_AU / 9.55491)**2

BOUND_TIGHTEST = 1.3e-9   # K-R Data Tables v19 1-sigma on s^TX (combined fit, Hees 2016)

# ----------------------------------------------------------------------------------
# 1. The Gauss planetary equations for the SECULAR node & perihelion drift.
#    Standard form (e.g. Burns 1976; BK use the same Lagrange/Gauss machinery).
#    Decompose the perturbing accel into (R radial, T transverse, W out-of-plane):
#       dOmega/dt = r sin(u) W / (n a^2 sqrt(1-e^2) sin i)
#       domega/dt = -cos i dOmega/dt
#                   + sqrt(1-e^2)/(n a e) [ -R cos f + T (1 + r/p) sin f ]
#    with u = omega + f (argument of latitude), p = a(1-e^2), r = p/(1+e cos f).
#    Time-average:  <X>_dt = (1/2pi) integral_0^2pi X (r/a)^2 / sqrt(1-e^2) df   [areal law]
#    (the (r/a)^2/sqrt(1-e^2) is the dt->df Jacobian; integral of it over f = 1).
#
#    The BK Lorentz-violating perturbing acceleration (Eq.165), gravity sector:
#       alpha'^j = (GM/r^2) [ shat^{jk} rhat^k - (3/2) shat^{kl} rhat^k rhat^l rhat^j ]
#    i.e. magnitude GM*s/r^2 times a CONSTANT-tensor angular pattern in rhat.
#    Project onto (R,T,W): each is (GM/r^2) * g_X(f) with g_X a function of the orbit
#    angles and the FIXED s-tensor components -- NO extra r-power beyond the 1/r^2.
#
#    => the secular integrand for any element is
#         [Gauss geom kernel ~ r or 1] * (GM/r^2) g(f) * (r/a)^2 df   (the areal Jacobian)
#       The constant-s rate: the r-powers combine to leave the clean (a,e,i,n) result.
#    For the FRAMEWORK we multiply the s-tensor (hence g(f)) by (r/a)^2:
#         integrand_fw(f) = integrand_const(f) * (r(f)/a)^2 .
#    Enhancement eta = <integrand_const * (r/a)^2>_f / <integrand_const>_f .
#    This is computed BELOW with the FULL f-dependent integrand (not a flat avg).
# ----------------------------------------------------------------------------------

def rp_over_a(f, e):
    """r/a as a function of true anomaly."""
    return (1 - e**2) / (1 + e*np.cos(f))

def jac(f, e):
    """dt->df areal Jacobian (normalized: integral over f of jac = 1)."""
    return (rp_over_a(f, e)**2 / np.sqrt(1 - e**2)) / (2*np.pi)

# ----------------------------------------------------------------------------------
# 2. Build the ACTUAL secular integrands for dOmega/dt and domega/dt with the BK
#    s-tensor angular pattern, for the s^TX-type coefficient, and orbit-average both
#    the constant-s and the framework r^2 versions. Take the RATIO -> eta(element).
#
#    s^TX is a MIXED time-space coefficient S^X (BK 'S^k' / 'S^Q' terms): it enters
#    the secular rates through the boost-type pieces. From Hees Eq.7a/7b the S^k, S^Q
#    terms ride the SAME f-dependence (cos f / sin f) as the rest, multiplied by 'na'.
#    We therefore audit BOTH the pure-spatial s^jk channel (s_kP sin w, s_kQ cos w with
#    the sin u / cos u f-pattern) AND the mixed S^k cos f channel, since which one
#    dominates the s^TX projection is itself an O(1) question. We report the eta for
#    each and take the WORST (largest enhancement = tightest margin) -- conservative.
# ----------------------------------------------------------------------------------

def eta_for_pattern(e, pattern):
    """
    eta = <(r/a)^2 * |K(f)|>_t / <|K(f)|>_t  where K(f) is the f-dependent secular
    integrand pattern and <.>_t is the areal-Jacobian time average.
    We use |K| because the secular rate is the NET (signed) integral; using |K| gives
    the magnitude enhancement of the *constrained amplitude* in the most direct way and
    is conservative (a signed integral can only reduce, never increase, the net vs |.|,
    so |K| is the right object for 'how much does the r^2 inflate the constrained s').
    pattern(f) returns the f-dependent kernel for the chosen element/channel.
    """
    num = quad(lambda f: rp_over_a(f, e)**2 * abs(pattern(f, e)) * jac(f, e), 0, 2*np.pi)[0]
    den = quad(lambda f:                      abs(pattern(f, e)) * jac(f, e), 0, 2*np.pi)[0]
    return num / den

# --- the f-dependent kernel patterns (argument of latitude u = w + f; set w=0 WLOG for
#     the f-shape audit -- the secular average is over a full orbit so the omega phase
#     only rotates the pattern, it does not change the eta integral by more than the
#     spread we already bracket; we additionally scan omega below to confirm) ---

def K_node_W(f, e, w=0.0):
    # dOmega/dt integrand ~ (r/a) * sin(u) * g_W(f)/r^2 * jac ; the s^jk W-projection
    # carries sin(u). Net f-shape of the CONSTANT-s integrand (before the extra (r/a)^2):
    #   (r/a) * sin(u) * (1/(r/a)^2)  ->  sin(u)/(r/a) = sin(u)(1+e cos f)/(1-e^2)
    u = w + f
    return np.sin(u) * (1 + e*np.cos(f)) / (1 - e**2)

def K_peri(f, e, w=0.0):
    # domega/dt in-plane part ~ sqrt(1-e^2)/(nae)[-R cos f + T(1+r/p) sin f].
    # R,T are (GM/r^2)*g(f). Net constant-s integrand f-shape (before extra (r/a)^2):
    #   [ -cos f + (1 + (r/a)/(1-e^2)... ) sin f ] * (1/(r/a)^2)
    # Use the standard r/p = 1/(1+e cos f)... we take the dominant transverse term shape:
    ra = rp_over_a(f, e)
    R_pat = -np.cos(f)
    T_pat = (1 + 1.0/(1 + e*np.cos(f))) * np.sin(f)
    return (R_pat + T_pat) / ra**2

def K_mixedS(f, e, w=0.0):
    # the mixed time-space S^k / S^Q boost channel rides cos f (Hees Eq.7a last term
    # '-(2 n a eps/(e c)) S^k cos w' and Eq.7b '+ ... S^Q'): f-shape ~ cos f / (r/a)^2.
    return np.cos(f) / rp_over_a(f, e)**2

print("="*78)
print("RIGOROUS r-varying secular-integral correction (full f-dependent kernel)")
print("eta = <(r/a)^2 * |K(f)|>_t / <|K(f)|>_t  per element/channel, per planet")
print("="*78)

channels = {
    'node dOmega/dt (W, sin u)': K_node_W,
    'peri domega/dt (in-plane)': K_peri,
    'mixed S^X boost (cos f)':   K_mixedS,
}

results = {}
for name, (a, e, inc) in PLANETS.items():
    etas = {ch: eta_for_pattern(e, fn) for ch, fn in channels.items()}
    # scan omega in [0,2pi) for the two patterns that carry u=w+f, take worst
    wscan = np.linspace(0, 2*np.pi, 24, endpoint=False)
    eta_node_scan = max(eta_for_pattern(e, lambda f, ee, ww=w: K_node_W(f, ee, ww)) for w in wscan)
    eta_worst = max(max(etas.values()), eta_node_scan)
    results[name] = (etas, eta_worst)
    print(f"\n{name:8s}  e={e:.4f}")
    for ch, v in etas.items():
        print(f"    {ch:28s} eta={v:.4f}  (+{100*(v-1):+.2f}%)")
    print(f"    node omega-scan worst             eta={eta_node_scan:.4f}")
    print(f"    --> WORST-channel eta             {eta_worst:.4f}  (+{100*(eta_worst-1):+.2f}%)")

# ----------------------------------------------------------------------------------
# 3. Corrected effective s^TX and margin, per planet, using the WORST-channel eta
#    (conservative = most tightening). The constrained EFFECTIVE amplitude that the
#    secular fit actually limits is s_eff = s_at_a * eta. Margin = bound / s_eff.
# ----------------------------------------------------------------------------------
print("\n" + "="*78)
print("CORRECTED margin per planet (worst-channel eta, conservative/most-tightening)")
print(f"tightest bound 1-sigma = {BOUND_TIGHTEST:.2e}")
print("="*78)
print(f"{'planet':8s} {'s_at_a':>10s} {'eta':>7s} {'s_eff':>10s} {'margin_a':>9s} {'margin_corr':>11s}")
worst_corner = None
worst_margin = np.inf
for name, (a, e, inc) in PLANETS.items():
    sa = s_at_a(a)
    eta = results[name][1]
    seff = sa * eta
    m_a = BOUND_TIGHTEST / sa
    m_c = BOUND_TIGHTEST / seff
    print(f"{name:8s} {sa:10.3e} {eta:7.4f} {seff:10.3e} {m_a:9.2f} {m_c:11.2f}")
    if m_c < worst_margin:
        worst_margin = m_c
        worst_corner = name

print("\n" + "="*78)
print(f"WORST CORNER (binding): {worst_corner}")
print(f"  evaluate-at-a margin  : {BOUND_TIGHTEST/s_at_a(PLANETS[worst_corner][0]):.3f}x")
print(f"  r-varying corrected   : {worst_margin:.3f}x")
shift = worst_margin / (BOUND_TIGHTEST/s_at_a(PLANETS[worst_corner][0]))
print(f"  multiplicative shift  : {shift:.4f}  ({'TIGHTER' if shift<1 else 'LOOSER' if shift>1 else 'SAME'})")
print("="*78)

# ----------------------------------------------------------------------------------
# 4. Cross-check against the naive plain time-average <(r/a)^2>_t (the banked number),
#    to show the FULL-kernel result vs the crude estimate.
# ----------------------------------------------------------------------------------
def naive_rp2(e):
    return quad(lambda f: rp_over_a(f, e)**2 * jac(f, e), 0, 2*np.pi)[0]
print("\nCROSS-CHECK: naive flat <(r/a)^2>_t (banked) vs full-kernel worst eta:")
for name, (a, e, inc) in PLANETS.items():
    print(f"  {name:8s} naive={naive_rp2(e):.4f}  full-kernel-worst={results[name][1]:.4f}")

# bracket the O(1) kernel-power p=1..3 on the worst corner body too
print("\nBRACKET kernel power p=1..3 (flat avg) at Saturn / Mercury:")
for p in (1,2,3):
    sat = quad(lambda f: rp_over_a(f,0.0555)**p*jac(f,0.0555),0,2*np.pi)[0]
    mer = quad(lambda f: rp_over_a(f,0.2056)**p*jac(f,0.2056),0,2*np.pi)[0]
    print(f"  p={p}: Saturn={sat:.4f}  Mercury={mer:.4f}")
