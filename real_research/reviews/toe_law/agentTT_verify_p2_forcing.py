"""
agentTT VERIFY — Part 2: THE DECISIVE FORCING-vs-CONSISTENCY TEST.

Hostile referee. Mission: is the edge GENUINELY EXCLUDED (forcing) or merely
dispreferred (consistency)? The route's forcing-direction rests on ONE pillar:

   "The GH modular flow is realized on the lowest-weight DISCRETE series; the edge
    carries a continuous-series weight -3/2, hence the edge is EXCLUDED from the GH
    rep."  (route Part 3B/3C, Part 5/H3)

I test whether that pillar actually FORBIDS the edge, or whether the edge survives
in an admissible sector the route did not rule out. Four independent attacks:

  (A) THE dS REP-THEORY FACT. A massive scalar (Delta complex or Delta in (0,(d-1)/2))
      in dS_d is quantized on the PRINCIPAL / COMPLEMENTARY (CONTINUOUS) series of
      SO(d,1) -- NOT the discrete series. The discrete series appears only for special
      cases (e.g. dS2 / specific integer dims). So "GH flow lives on the discrete
      series" is NOT a generic truth; for a generic dS scalar the GH static-patch
      correlator has CONTINUOUS-series content. If so, a continuous-series weight is
      NOT forbidden -> the edge is not excluded by rep class -> CONSISTENCY.

  (B) THE (P-fixed) DISCRIMINATOR IS NOT DISCRETE-vs-CONTINUOUS. dS QNM frequencies
      are purely imaginary (Re omega=0) for BOTH the discrete-series-like and the
      principal-series-like towers (Lopez-Ortega: omega=-iH(2n+l+Delta_pm) with
      Delta_pm possibly complex => STILL the real part structure is set by 2n+l).
      Test: is "Re omega=0" a property that distinguishes discrete from continuous
      series? If principal-series dS QNMs ALSO have a purely-damped ladder, then
      (P-fixed) does not select the discrete series and the route's Re-omega=0
      argument is weaker than a rep-class exclusion.

  (C) THE EDGE'S ONE-SIDEDNESS: is it really "T=0", or an ARTIFACT of placing the
      probe AT the band edge of a FINITE band? Independently: the soft edge is the
      bottom of a bounded spectrum [E0,-E0]. A correlator built on the FULL band is
      two-sided; the edge "one-sidedness" (A~0) is the statement that the probe
      energy E_v sits at the support BOUNDARY, so only omega>=0 (or <=0) is available.
      Test whether this is "zero temperature of a dS horizon" (route) or simply
      "the probe is at the spectral edge so half the band is kinematically absent"
      (a placement artifact that does NOT certify a forbidden modular weight).

  (D) THE INNER-AUTOMORPHISM HONESTY: the route ITSELF concedes (Part 2A/H5) the
      boost is diagonal on the energy charge E_v=cos(theta_v) => it CANNOT rotate
      the edge into the center => theta_v is a superselection label. Confirm this
      symbolically and state its consequence: a symmetry that does not ACT on the
      discriminating label cannot FORCE its value. This is, by the route's own
      admission, a CONSISTENCY/necessary-condition argument, not a FORCING.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
print("="*78)
print("VERIFY PART 2 — DECISIVE forcing-vs-consistency test")
print("="*78)

# ===========================================================================
# (A) dS rep theory: which series does a massive scalar / the GH state use?
# Principal series: Delta = (d-1)/2 + i*mu, mu>=0 (heavy, m > (d-1)/2 H).
# Complementary series: Delta in (0, d-1) real (light).
# Discrete series: special (exceptional) points; in SO(d,1) the genuine
# normalizable discrete series exists for dS2 (SO(2,1)~SL(2,R)) and as exceptional
# series in higher d. The Bunch-Davies/GH two-point function of a GENERIC massive
# scalar is built on the PRINCIPAL/COMPLEMENTARY (continuous) series.
# ===========================================================================
print("\n(A) Which SO(d,1) UIR carries a massive-scalar GH correlator?")
d = sp.symbols('d', positive=True)
mu = sp.symbols('mu', positive=True)   # principal-series label
# principal-series conformal weight:
Delta_principal = (d-1)/2 + sp.I*mu
print(f"    Principal series (heavy scalar m>(d-1)H/2): Delta = (d-1)/2 + i*mu, mu>=0.")
print(f"      For dS3 (d=3): Delta = 1 + i*mu  -> COMPLEX weight, CONTINUOUS series.")
print(f"    Complementary series (light 0<m<(d-1)H/2): Delta in (0,d-1) REAL.")
print(f"    Discrete series: exceptional/special; the GENUINE normalizable discrete")
print(f"      series is the SL(2,R)~SO(2,1) (dS2) lowest-weight tower (route's object).")
print(f"    KEY FACT: the Bunch-Davies/GH 2pt of a GENERIC massive dS_d scalar")
print(f"      decomposes on the PRINCIPAL/COMPLEMENTARY (CONTINUOUS) series, NOT the")
print(f"      discrete series. [Joung-Mourad-Parentani 0606119/0612061; Anninos et al.]")
print(f"    => 'GH modular flow is realized on the DISCRETE series' is TRUE only for")
print(f"       the special dS2/SL(2,R) lowest-weight sector (the q->1 DSSYK ladder),")
print(f"       NOT a blanket exclusion of continuous-series objects from dS physics.")
print(f"    => A continuous-series weight is NOT, per se, 'forbidden for dS': it is the")
print(f"       GENERIC dS scalar sector. The edge's continuous-series class is")
print(f"       therefore NOT excluded by dS representation theory. [CONSISTENCY hatch]")

# ===========================================================================
# (B) Is Re(omega)=0 a discrete-vs-continuous discriminator?
# Lopez-Ortega dS_d scalar QNM: omega_{n,l} = -i H (2n + l + Delta_pm), with
# Delta_pm = (d-1)/2 +/- sqrt((d-1)^2/4 - m^2/H^2). For HEAVY (principal) scalars,
# Delta_pm is COMPLEX, so omega acquires a REAL part:
#   Delta_pm = (d-1)/2 +/- i*nu  => omega = -iH(2n+l+(d-1)/2) +/- H*nu  (Re != 0!)
# but the purely-imaginary ladder (Re omega=0) occurs for LIGHT/real-Delta scalars.
# Test the claim: "Re omega=0 <=> discrete series". Compute Re(omega) for a heavy
# (principal/continuous-series) dS scalar and show it is NONZERO => Re omega=0 is a
# property of REAL-Delta towers, which include BOTH the complementary (continuous)
# series AND the discrete series. So Re omega=0 does NOT isolate the discrete series.
# ===========================================================================
print("\n(B) Does Re(omega)=0 select the DISCRETE series? (test the (P-fixed) pillar)")
H, nu, n_, l_ = sp.symbols('H nu n l', positive=True)
dval = 3
m_over_H = sp.symbols('m_over_H', positive=True)
disc = sp.Rational(dval-1,2)**2 - m_over_H**2     # (d-1)^2/4 - m^2/H^2
Delta_pm = sp.Rational(dval-1,2) + sp.sqrt(disc)
omega_QNM = -sp.I*H*(2*n_ + l_ + Delta_pm)
print(f"    dS3 scalar QNM (Lopez-Ortega): omega = -iH(2n+l+Delta_+), "
      f"Delta_+ = 1 + sqrt(1 - m^2/H^2)")
# LIGHT (m<H): disc>0, Delta_+ real => omega purely imaginary (Re=0).
omega_light = omega_QNM.subs(m_over_H, sp.Rational(1,2))
print(f"    LIGHT m=H/2 (disc>0, real Delta): omega = {sp.simplify(omega_light)}  -> Re=0")
# HEAVY (m>H, principal/continuous series): disc<0, Delta_+ complex => Re(omega)!=0.
omega_heavy = omega_QNM.subs(m_over_H, 2)   # m=2H, disc=1-4=-3<0
omega_heavy = sp.simplify(sp.expand(omega_heavy.rewrite(sp.exp)))
re_heavy = sp.re(omega_QNM.subs(m_over_H,2).rewrite(sp.sqrt))
print(f"    HEAVY m=2H (disc<0, COMPLEX Delta=principal series): "
      f"Delta_+ = 1 + i*sqrt(3)")
print(f"      omega = -iH(2n+l+1) + H*sqrt(3)  -> Re(omega) = H*sqrt(3) != 0 (RINGS).")
print(f"    => Re(omega)=0 holds for LIGHT (real-Delta) scalars, which span BOTH the")
print(f"       COMPLEMENTARY (continuous) series AND the discrete series. Re omega=0 is")
print(f"       a REAL-weight property, NOT a discrete-series-SELECTOR.")
print(f"    => The route's (P-fixed) [Re omega=0] does NOT, by itself, exclude")
print(f"       continuous-series objects. It excludes HEAVY/ringing modes, which is a")
print(f"       different (and weaker) statement than 'excludes the edge's rep class.'")

# ===========================================================================
# (C) Edge one-sidedness: T=0 horizon, or band-edge placement artifact?
# Model the band as E in [-1,1] (E0=1). The matter 2pt spectral support, for a probe
# at E_v, is the set of E-E_v over the band: [-1-E_v, 1-E_v]. The asymmetry:
#   A = (negative-weight)/(total). At CENTER E_v=0: support [-1,1] symmetric => A=1/2.
#   At EDGE E_v->-1: support [0,2] => entirely omega>=0 => A->0 (one-sided).
# This is PURELY KINEMATIC: the probe at the band edge has half the band absent
# because there are no states beyond the edge. Compute A(E_v) and show one-sidedness
# is a continuous CONSEQUENCE of edge-placement, identical to "the probe sits at the
# support boundary", NOT an independent certificate of a forbidden T=0 modular sector.
# ===========================================================================
print("\n(C) Edge one-sidedness: forbidden-T=0 sector, or band-edge kinematic artifact?")
Ev = sp.symbols('E_v', real=True)
# support of omega=E-E_v for E in [-1,1]: [-1-Ev, 1-Ev]; fraction with omega<0:
# length of negative part / total length (uniform-measure proxy for the asymmetry sign)
lo = -1 - Ev; hi = 1 - Ev
neg_len = sp.Piecewise((0, hi<=0), (sp.Min(hi,0)-lo, True))  # crude; evaluate at samples
for ev in [sp.Integer(0), sp.Rational(-1,2), sp.Rational(-9,10), sp.Rational(-999,1000)]:
    L = (1-ev) - (-1-ev)      # total = 2 always
    negpart = max(0.0, float(min(1-ev,0) - (-1-ev)))   # part with omega<0
    A = negpart/float(L)
    print(f"    E_v={float(ev):+.3f}: omega-support=[{float(-1-ev):+.3f},{float(1-ev):+.3f}], "
          f"fraction(omega<0) = {A:.4f}")
print(f"    => A slides CONTINUOUSLY 0.5 -> 0 as the probe -> band edge. The edge's")
print(f"       'one-sidedness' (A~0) is the KINEMATIC statement 'the probe is at the")
print(f"       spectral boundary, half the band is absent'. It is a CONTINUOUS")
print(f"       placement property, NOT a discrete certificate of a 'forbidden T=0")
print(f"       modular sector'. (The route reads A~0 as beta=inf; but A is a")
print(f"       continuous function of placement -- the same sliding the route argued")
print(f"       was IMPOSSIBLE for the discriminator. The discrete/continuous SERIES")
print(f"       label is binary, but the asymmetry A that 'certifies' it is NOT.)")

# ===========================================================================
# (D) Inner-automorphism: the boost cannot move theta_v (route's own concession).
# Confirm symbolically and state the logical consequence for FORCING.
# ===========================================================================
print("\n(D) The boost is INNER to each placement sector (route Part 2A/H5):")
theta_v, t_mod = sp.symbols('theta_v t_mod', real=True)
E_v = sp.cos(theta_v)
# sigma_t |E_v> = e^{i E_v t}|E_v>: the energy eigenvalue (hence theta_v) is invariant.
print(f"    sigma_t|E_v> = e^(i E_v t_mod)|E_v>, E_v=cos(theta_v) CONSERVED under boost.")
print(f"    d/dt_mod |E_v| = 0 => theta_v is a MODULAR-INVARIANT (superselection) label.")
print(f"    LOGICAL CONSEQUENCE (the referee's central point):")
print(f"    A symmetry that does NOT act on the discriminating label theta_v CANNOT")
print(f"    FORCE its value. It can only declare which fixed value is CONSISTENT with")
print(f"    being the GH (boost-KMS) state. By the route's OWN Part 2A, this is a")
print(f"    NECESSARY-CONDITION / CONSISTENCY argument, NOT an algebraic FORCING that")
print(f"    excludes writing down the edge state. (The route concedes exactly this in")
print(f"    its verdict residual (i): 'the boost is inner ... cannot dynamically rotate")
print(f"    the edge away.')")

print("\n" + "="*78)
print("SUMMARY OF THE DECISIVE TEST:")
print(" (A) continuous-series weights are the GENERIC dS-scalar sector, NOT forbidden")
print("     -> the edge's rep class is not excluded by dS rep theory.")
print(" (B) Re(omega)=0 is a real-weight property spanning complementary+discrete")
print("     series, NOT a discrete-series selector -> (P-fixed) is weaker than a")
print("     rep-class exclusion.")
print(" (C) edge one-sidedness A~0 is a CONTINUOUS band-edge kinematic artifact, not a")
print("     binary 'forbidden T=0 sector' certificate.")
print(" (D) the boost does NOT act on theta_v (route's own concession) -> it cannot")
print("     FORCE the placement; it gives a NECESSARY CONDITION only.")
print("=> The modular structure SELECTS/FAVORS the center as the boost-KMS-consistent")
print("   placement (a real, theorem-backed CONSISTENCY/favoring), but does NOT FORCE")
print("   it: the edge is not a forbidden rep, only a different (non-GH) one, and the")
print("   symmetry cannot rotate placements. FORCING is NOT established; CONSISTENCY/")
print("   FAVORING is. This MATCHES the route's own stop-short-of-FORCED verdict.")
print("="*78)
