#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE 1 -- CAN THE det-CLASS ELASTIC MEDIUM *DERIVE* THE SHEAR-ANHARMONICITY FRACTION w? (P5)
=============================================================================================
Candidate structure: E(eps) = (mu/2) J2 + F(det(1+eps)),  J2 = e:e (deviatoric), all
anharmonicity volumetric.  Banked Lane-C bound: Branch B needs w <= 0.22-0.26 (canonical)
/ 0.17-0.19 (alt), where Q2_medium = w * Q2_scalar-class.

This script:
 (a) EXACT second-order probe expansion around the anisotropic galactic pre-strain
     (bulk t = J1_bg AND deviator d = e_bg amplitude), sympy, no truncation of det;
 (b) F pinned to the banked deep-MOND displacement law (lane3 Verlinde matching);
 (c) the shear modulus mu pinned two independent ways -- (i) shear waves = GWs
     (GR/GW170817 normalization), (ii) Verlinde's own deep energy match -- and the two
     CHECKED against each other;
 (d) w computed as a number-with-band, both footings;
 (e) strain-convention stress test (kappa, a0 vs a0_V normalization, probe shape, p, S, beta).
HONESTY: 'w is O(1), P5 not derivable' and 'w tiny' hunted with equal force; every fork shown.
"""
import numpy as np
import sympy as sp

# ---------------------------------------------------------------- constants (SI)
c_l  = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
AU   = 1.495978707e11
Mpc  = 3.0857e22

Z        = np.sqrt(32*np.pi/3.0)      # 5.7873
A0_CANON = 9.36e-11                    # cH_Lambda/Z
A0_ALT   = 1.13e-10                    # cH0/Z-ish (rho_total footing)
cH_Lam   = Z*A0_CANON                  # 5.418e-10
H0       = 67.4e3/Mpc
cH0      = c_l*H0                      # 6.55e-10
Q2_CEIL  = 5.2e-27                     # Cassini 2-sigma ceiling [s^-2]
Q2_SCAL  = {"canonical": (2.0e-26, 2.4e-26), "alt": (2.7e-26, 3.0e-26)}  # banked scalar-class
W_BOUND  = {"canonical": (0.22, 0.26), "alt": (0.17, 0.19)}

def nu_fw(y): return np.sqrt(1.0 + 1.0/y)

print("="*100)
print(" LANE 1 -- DERIVING w FOR THE det-CLASS MEDIUM  E = (mu/2) J2 + F(det(1+eps))")
print("="*100)

# ====================================================================================================
# PART 0 -- GEOMETRIC FACTS, DERIVED EXACTLY (sympy)
# ====================================================================================================
print("\n[0] det geometry, exact (sympy):")
e11,e22,e33,e12,e13,e23 = sp.symbols('e11 e22 e33 e12 e13 e23', real=True)
EPS = sp.Matrix([[e11,e12,e13],[e12,e22,e23],[e13,e23,e33]])
I3m = sp.eye(3)
I1 = sp.trace(EPS)
I2 = sp.Rational(1,2)*(sp.trace(EPS)**2 - sp.trace(EPS*EPS))
I3 = EPS.det()
assert sp.simplify((I3m+EPS).det() - (1 + I1 + I2 + I3)) == 0
J1 = I1
Edev = EPS - (J1/3)*I3m
J2s = sp.trace(Edev*Edev)
second = 1 + J1 + J1**2/sp.Integer(3) - J2s/sp.Integer(2)
diff2 = sp.simplify(sp.expand((I3m+EPS).det() - second))
# residual must be pure third order (I3): check by scaling eps -> s*eps
s_ = sp.symbols('s')
scaled = diff2.subs({v: s_*v for v in (e11,e22,e33,e12,e13,e23)})
assert sp.simplify(sp.expand(scaled) - s_**3*diff2) == 0
print("    det(1+eps) = 1 + I1 + I2 + I3                      [VERIFIED exact]")
print("    det(1+eps) = 1 + J1 + J1^2/3 - J2/2 + O(eps^3)     [VERIFIED: residual pure 3rd order]")
# first-order det derivative is shear-blind:
grad = sp.Matrix(3,3, lambda i,j: sp.diff((I3m+EPS).det(), EPS[i,j]))
grad0 = grad.subs({v:0 for v in (e11,e22,e33,e12,e13,e23)})
assert grad0 == I3m
print("    d det/d eps |_{eps=0} = delta_ij (shear-blind at first order)   [VERIFIED]")

# ====================================================================================================
# PART 1(a) -- EXACT PROBE-QUADRATIC FORM AROUND THE PRE-STRAINED STATE (sympy, det NOT truncated)
# ====================================================================================================
print("\n" + "="*100)
print("[1a] EXACT second-order shear expansion around the galactic pre-strain (t = J1_bg, d = e_bg)")
print("="*100)
t, d, F1, F2, mu, ar, at, cc = sp.symbols('t d F1 F2 mu a_r a_t c', real=True)
# background: eps_bg = (t/3) I + d (ee - I/3), e = z-hat  (galactic direction)
Mb  = sp.diag(1 + t/3 - d/3, 1 + t/3 - d/3, 1 + t/3 + 2*d/3)
Jst = Mb.det()                         # det(1+eps_bg), exact
Mi  = Mb.inv()
# probe: the Sun's locally-radial strain field at direction rhat(theta), cc = cos(theta)
rhat  = sp.Matrix([sp.sqrt(1-cc**2), 0, cc])
eps_s = (ar-at)*(rhat*rhat.T) + at*I3m           # eps_rr = a_r, eps_perp = a_t
es_dev = eps_s - (sp.trace(eps_s)/3)*I3m
# exact second variation of E:
#   dE  = F'(J*) J* tr(Mi eps_s)                                   (first order)
#   d2E = 1/2 [ F'' J*^2 (tr Mi eps_s)^2 + F' J* ((tr Mi eps_s)^2 - tr(Mi eps_s Mi eps_s)) ]
#         + (mu/2) es_dev:es_dev
trX  = sp.trace(Mi*eps_s)
trXX = sp.trace(Mi*eps_s*Mi*eps_s)
Q = sp.Rational(1,2)*( F2*Jst**2*trX**2 + F1*Jst*(trX**2 - trXX) ) \
    + sp.Rational(1,2)*mu*sp.trace(es_dev*es_dev)
Q = sp.expand(sp.simplify(Q))
P2c = (3*cc**2 - 1)/2
Q0  = sp.simplify(sp.Rational(1,2)*sp.integrate(Q, (cc,-1,1)))
Q2  = sp.simplify(sp.Rational(5,2)*sp.integrate(Q*P2c, (cc,-1,1)))
# gate checks:
assert sp.simplify(Q2.subs(d,0)) == 0, "isotropic background must give zero l=2"
print("    d = 0  =>  Q2 == 0 exactly (isotropic background sources no l=2)   [VERIFIED]")
Q2ser = sp.expand(sp.series(Q2, d, 0, 3).removeO())
Q2_lin  = sp.simplify(sp.expand(Q2ser.coeff(d,1))*d)
Q2_quad = sp.simplify(sp.expand(Q2ser.coeff(d,2))*d**2)
print("\n    THE DIRECTIONAL SHEAR-SHEAR COUPLING (exact l=2 amplitude of the probe response),")
print("    expanded in the pre-strain deviator d (coefficients exact in F', F'', t):")
print("      O(d)  :", sp.nsimplify(sp.simplify(Q2_lin/d)), " * d")
print("      O(d^2):", sp.nsimplify(sp.simplify(Q2_quad/d**2)), " * d^2")
print("    NOTE: mu (material-linear shear) contributes NOTHING to Q2 -- the entire l=2 comes")
print("    from the F-sector geometry (F' and F'' terms), as the det-class construction intends;")
print("    but it is NOT zero: the det geometry itself couples shear to direction at O(d).")

# ====================================================================================================
# PART 1(pre) -- THE PRE-STRAIN DEVIATOR FROM THE DISPLACEMENT LAW (exact + numeric)
# ====================================================================================================
print("\n" + "="*100)
print("[1-pre] e_bg from the displacement law (volumetric reading, radial galactic field)")
print("="*100)
R, qq, n = sp.symbols('R q n', positive=True)
J1prof = R**(-qq)                       # J1(R) ~ R^-q near the Sun (local power law)
u = sp.integrate(R**2*J1prof, R)/R**2   # (R^2 u)' = R^2 J1  (volumetric reading J1 = eps)
dev = sp.simplify(sp.diff(u,R) - u/R)   # deviator amplitude d = u' - u/R
ratio = sp.simplify(dev/J1prof)
if isinstance(ratio, sp.Piecewise):        # generic branch (q != 3; q~0.1 physically)
    ratio = ratio.args[0][0]
print("    radial u from (R^2 u)' = R^2 J1, J1 ~ R^-q  =>  d/J1 =", sp.simplify(ratio), "  [exact]")
assert sp.simplify(ratio - (-qq/(3-qq))) == 0
# deep profile lemma: u ~ R^-n => J2/J1^2 fixed by geometry; deep-MOND (eps ~ 1/R) is n=0:
J1n = (2-n); dn = -(n+1)                # per u ~ R^-n (units of u/R)
J2overJ1sq = sp.simplify(sp.Rational(2,3)*dn**2/J1n**2)
print("    u ~ R^-n  =>  J2/J1^2 = (2/3)(n+1)^2/(2-n)^2 ; deep profile (n=0): J2 = J1^2/6")
print("    => NO decaying radial displacement is shear-free: the deep-MOND response CARRIES")
print("       shear at fixed 1/6 weight -- the shear sector CANNOT hide from the deep match.")

def prestrain(y, p, kappa=2.0):
    """screened pre-strain at external y=g_bar/a0: t=J1_bg, d, and the local profile slope."""
    eps  = kappa*(np.sqrt(y*y+y) - y)                 # eps = kappa*(nu-1)*y, framework nu
    deps = kappa*((2*y+1)/(2*np.sqrt(y*y+y)) - 1.0)   # d eps/dy
    slope = y*deps/eps                                # dln eps/dln y
    q = p*slope
    dd = -q/(3.0-q)*eps
    return eps, dd, slope, q

print("\n    screened pre-strain at the Sun (eps = kappa*(nu-1)*y, kappa=2 Verlinde norm):")
print(f"    {'footing':<11}{'y_ext':>7}{'eps=J1_bg':>11}{'dln e/dln y':>13}{'p':>5}{'d_bg':>9}{'d/J1':>8}")
for tag, a0v in (("canonical",A0_CANON), ("alt",A0_ALT)):
    for p in (1.0, 1.3, 2.0):
        y = 2.2 if tag=="canonical" else 2.06e-10/A0_ALT
        eps, dd, slope, q = prestrain(y, p)
        print(f"    {tag:<11}{y:>7.2f}{eps:>11.3f}{slope:>13.4f}{p:>5.1f}{dd:>9.4f}{dd/eps:>8.4f}")
print("    KEY MECHANISM (derived, not assumed): the SCREEN saturates the strain (eps -> kappa/2")
print("    as y -> inf), so dln eps/dln y ~ 0.085 at y=2.2 -- the pre-strain profile is nearly")
print("    FLAT, and a flat J1 field is pure dilation: d/J1 = -q/(3-q) ~ -0.03..-0.06, NOT the")
print("    naive -1/2 of the deep profile. The screen itself QUENCHES the pre-strain deviator.")
print("    (Unscreened deep fiction eps=2.8, d/J1=-1/2 kept below as a stress-test row.)")

# ====================================================================================================
# PART 1(b) -- F PINNED TO THE BANKED DEEP-MOND DISPLACEMENT LAW (physical units)
# ====================================================================================================
print("\n" + "="*100)
print("[1b] F', F'' in physical units from the lane3 Verlinde matching")
print("="*100)
print("""    Banked deep law: g_D = sqrt(a0_V g_bar/6); elastic energy density u_el = g_D^2/(8 pi G).
    STRAIN NORMALIZATION (stated, carried): eps = kappa * g_D / a0 with kappa = 2 (the Lane-C /
    Verlinde convention; eps then saturates at kappa/2 = 1). Volumetric reading: eps = J1.
    Deep profile (n=0) has J2 = J1^2/6 exactly [derived above], so the deep energy match reads
        (1/2) K_F J1^2 + mu J1^2/6 = u_el = a0^2 J1^2/(8 pi G kappa^2)
      =>  K_F + mu/3 = K_eff,   K_eff := a0^2/(4 pi G kappa^2)   [kappa=2: a0^2/(16 pi G)]
    This pins the TOTAL deep stiffness; beta := mu/(3 K_eff) in [0,1] is the shear share.""")
for tag, a0v in (("canonical",A0_CANON), ("alt",A0_ALT)):
    Keff = a0v**2/(16*np.pi*G)
    print(f"    {tag:<10}: K_eff = a0^2/(16 pi G) = {Keff:.3e} Pa ; F'(J*) ~ K_eff*(J*-1), F''_deep = (1-beta) K_eff")
print("    At the operating point the bulk law is nu-stiffened (P2, banked): F'' = S*(1-beta)*K_eff")
print("    with S in [1, ~kappa*dy/deps ~ 30] (tangent stiffening of the screen; carried as a band).")

# ====================================================================================================
# PART 1(c) -- THE TWO mu PINS, CHECKED AGAINST EACH OTHER
# ====================================================================================================
print("\n" + "="*100)
print("[1c] PINNING mu: (i) shear waves = GWs  vs  (ii) Verlinde deep energy match")
print("="*100)
print("""    (i) GR normalization. Linearized GR fixes only the RATIO mu/rho = c^2 (wave speed);
        the metric perturbation h is dimensionless strain, so GR has NO intrinsic modulus --
        the absolute mu needs the medium's inertial density. Medium = dark energy => rho = rho_L:""")
rows = []
for tag, a0v, rho in (("canonical", A0_CANON, 3*(cH_Lam/c_l)**2/(8*np.pi*G)),
                      ("alt",       A0_ALT,   3*(cH0/c_l)**2/(8*np.pi*G))):
    Keff = a0v**2/(16*np.pi*G)
    mu_gw = rho*c_l**2
    ratio = mu_gw/(3*Keff)
    rows.append((tag, Keff, mu_gw, ratio))
    print(f"        {tag:<10}: rho c^2 = {mu_gw:.3e} Pa ; rho c^2/K_eff = {mu_gw/Keff:.1f}"
          f"  [closed form: 6 Z^2 = {6*Z**2:.1f} on canonical]")
print("""        (static-GR alternative mu(L) = c^4/(16 pi G L^2): 1.1e14 Pa at 1e3 AU, 8.8e-11 Pa
         at L=Hubble -- scale-hostage, quoted for reference only; the wave pin is the physical one.)
    (ii) Verlinde-internal: the deep match above FORCES mu <= 3 K_eff (beta <= 1), i.e.
        mu <= {:.2e} Pa (canonical).
    CROSS-CHECK: (i) vs (ii) REFUSE EACH OTHER by the factor mu_GW/(3 K_eff) = 2 Z^2 = {:.0f}:""".format(
        3*A0_CANON**2/(16*np.pi*G), 2*Z**2))
for tag, Keff, mu_gw, ratio in rows:
    v_max = np.sqrt(3*Keff/(mu_gw/c_l**2))/c_l
    print(f"        {tag:<10}: if mu = rho c^2 (shear waves ARE GWs at c), the shear term alone")
    print(f"                    overshoots the deep energy budget {ratio:.0f}x -> deep coefficient"
          f" 0.982 -> {0.982/np.sqrt(ratio+1):.3f} (SPARC-DEAD);")
    print(f"                    if the deep match holds, v_shear <= {v_max:.3f} c -> shear waves are NOT GWs")
    print(f"                    (GW170817 |v-c|<1e-15 kills the identification, not the medium).")
print("""    VERDICT (c): the DEEP CANDIDATE MECHANISM ('the medium's linear shear sector IS GR,
    so w ~ a0-scale/GR-scale is generically tiny') is REFUTED: the normalizations refuse.
    Spherical compatibility (J2 = J1^2/6, derived) puts the shear sector INSIDE the deep-MOND
    energy budget, so mu is FORCED soft (a0^2/G-scale, within 3x of the bulk modulus). The
    hoped-for 42-order stiffness hierarchy is unavailable to the det-class. w must therefore be
    computed with BOTH stiffnesses at the common K_eff scale -- it is an O(angular x pre-strain)
    number, small ONLY if the pre-strain deviator is small.""")

# ====================================================================================================
# PART 1(d) -- w: THE NUMBER (exact angular algebra x pinned normalizations)
# ====================================================================================================
print("="*100)
print("[1d] w = |l=2| / |l=0| of the medium response, normalized to the scalar class")
print("="*100)
# scalar-class reference (banked Lane-C measure): fractional l=2 of the phantom response
def s_of_y(y, R):
    h=1e-5; return (np.log(R(y*(1+h)))-np.log(R(y*(1-h))))/(2*h)
def a2_scalar(y):
    R = lambda yy: (nu_fw(yy)-1.0)*yy
    h=1e-4
    s  = s_of_y(y,R); spp=(s_of_y(y*(1+h),R)-s_of_y(y*(1-h),R))/(2*h)
    return (s*s-2*s+spp)/3.0
lamQ0 = sp.lambdify((t,d,F1,F2,mu,ar,at), Q0, "numpy")
lamQ2 = sp.lambdify((t,d,F1,F2,mu,ar,at), Q2, "numpy")

PROBES = {"deep (a_r=0,a_t=1)": (0.0,1.0), "Newtonian tail (-2,1)": (-2.0,1.0),
          "generic (1,1)*": (1.0,1.0), "pure radial (1,0)": (1.0,0.0)}
def w_value(a0v, tag, y, p, kappa, S, beta, f1fac, eps_override=None, dratio_override=None):
    Keff = a0v**2/(4*np.pi*G*kappa**2)
    eps, dd, slope, q = prestrain(y, p, kappa)
    if eps_override is not None: eps = eps_override
    if dratio_override is not None: dd = dratio_override*eps
    F1v = f1fac*eps*Keff          # F'(J*) ~ K_eff * (J*-1) * band
    F2v = S*(1-beta)*Keff
    muv = 3*beta*Keff
    ws = {}
    for name,(arv,atv) in PROBES.items():
        q0 = lamQ0(eps,dd,F1v,F2v,muv,arv,atv)
        q2 = lamQ2(eps,dd,F1v,F2v,muv,arv,atv)
        a2m = q2/q0
        ws[name] = abs(a2m)/abs(a2_scalar(y))
    return ws, eps, dd

print("    w per probe shape (canonical footing, y=2.2, kappa=2; scalar ref a2_scalar(y)):")
print(f"    a2_scalar(2.2) = {a2_scalar(2.2):+.4f}  (the scalar class's own fractional l=2 -- w=1 ref)")
hdr = f"    {'p':>4}{'S':>5}{'beta':>6}{'f1':>4} | " + "".join(f"{k[:14]:>16}" for k in PROBES)
print(hdr)
grid_can = []
for p in (1.0,1.3,2.0):
    for S in (1,5,30):
        for beta in (0.33,0.67,0.95):
            for f1 in (1.0,3.0):
                ws,eps,dd = w_value(A0_CANON,"canonical",2.2,p,2.0,S,beta,f1)
                grid_can.append(max(ws.values()))
                if (p,S,beta,f1) in [(1.3,1,0.67,1.0),(1.3,5,0.67,1.0),(1.3,30,0.67,1.0),
                                     (1.3,30,0.33,3.0),(2.0,30,0.33,3.0),(1.0,1,0.95,1.0)]:
                    print(f"    {p:>4.1f}{S:>5.0f}{beta:>6.2f}{f1:>4.1f} | " +
                          "".join(f"{ws[k]:>16.4f}" for k in PROBES))
w_can_med = np.median(grid_can); w_can_lo, w_can_hi = np.min(grid_can), np.max(grid_can)
print(f"\n    CANONICAL grid (worst probe per cell): w = {w_can_lo:.3f} .. {w_can_hi:.3f}, median {w_can_med:.3f}")

grid_alt = []
y_alt = 2.06e-10/A0_ALT
for p in (1.0,1.3,2.0):
    for S in (1,5,30):
        for beta in (0.33,0.67,0.95):
            for f1 in (1.0,3.0):
                ws,_,_ = w_value(A0_ALT,"alt",y_alt,p,2.0,S,beta,f1)
                grid_alt.append(max(ws.values()))
w_alt_med = np.median(grid_alt); w_alt_lo, w_alt_hi = np.min(grid_alt), np.max(grid_alt)
print(f"    ALT       grid (worst probe per cell): w = {w_alt_lo:.3f} .. {w_alt_hi:.3f}, median {w_alt_med:.3f}")
for tag,(lo,hi),(wl,wh,wm) in (("canonical",W_BOUND["canonical"],(w_can_lo,w_can_hi,w_can_med)),
                               ("alt",W_BOUND["alt"],(w_alt_lo,w_alt_hi,w_alt_med))):
    q2lo,q2hi = Q2_SCAL[tag]
    print(f"    {tag:<10}: bound w <= {lo:.2f}-{hi:.2f}; derived band [{wl:.3f},{wh:.3f}] median {wm:.3f}"
          f" -> Q2_med ~ {wm*q2lo:.1e}-{wh*q2hi:.1e} s^-2 vs ceiling {Q2_CEIL:.1e}")

# measure-mapping honesty: the scalar-class reference itself spans 0.076 (a2 local proxy) to
# ~0.25 (AQUAL L0 / modulus family, Lane-C C1 'O(1) ledger'); w scales inversely with it:
print("\n    MEASURE MAPPING (named ambiguity): scalar-class fractional-l=2 reference spans")
print(f"    |a2_scalar| = {abs(a2_scalar(2.2)):.3f} (local proxy) .. 0.25 (Lane-C C1 modulus-family edge);")
wsB,_,_ = w_value(A0_CANON,"canonical",2.2,1.3,2.0,5,0.67,1.0)
for ref,lab in ((abs(a2_scalar(2.2)),"a2 proxy"),(0.25,"L0 edge")):
    wref = max(wsB.values())*abs(a2_scalar(2.2))/ref
    print(f"      base cell w -> {wref:.3f} under the {lab} reference")
print("    g_ext sensitivity (base cell, canonical): ", end="")
print(", ".join(f"y={g/A0_CANON:.2f}: w={max(w_value(A0_CANON,'canonical',g/A0_CANON,1.3,2.0,5,0.67,1.0)[0].values()):.3f}"
                for g in (1.9e-10, 2.15e-10, 2.32e-10)))

# ====================================================================================================
# PART 1(e) -- CONVENTION STRESS TEST
# ====================================================================================================
print("\n" + "="*100)
print("[1e] STRESS TEST: is the verdict convention-hostage?")
print("="*100)
print(f"    {'variation':<52}{'w (median-cell, worst probe)':>30}")
base_ws,_,_ = w_value(A0_CANON,"canonical",2.2,1.3,2.0,5,0.67,1.0)
print(f"    {'BASE: kappa=2, screened eps, d/J1 from profile':<52}{max(base_ws.values()):>30.4f}")
for label, kw in [
    ("kappa=1 (strain = g_D/a0)",              dict(kappa=1.0)),
    ("kappa=2/Z (strain = 2 g_D/a0_V)",        dict(kappa=2.0/Z)),
    ("UNSCREENED deep fiction eps=2.8, d/J1=-1/2", dict(eps_override=2.8, dratio_override=-0.5)),
    ("screened eps but naive d/J1=-1/2",       dict(dratio_override=-0.5)),
    ("d/J1=-1/4",                              dict(dratio_override=-0.25)),
]:
    args = dict(a0v=A0_CANON,tag="canonical",y=2.2,p=1.3,kappa=2.0,S=5,beta=0.67,f1fac=1.0)
    args.update(kw)
    ws,eps,dd = w_value(**args)
    print(f"    {label:<52}{max(ws.values()):>30.4f}")
print("""    READING (e):
    * kappa (absolute strain normalization) moves w roughly as kappa^2 -- a REAL residual
      ambiguity (Verlinde's heuristic pins only K_eff*eps^2, not eps). Within the det-class read
      strictly, F(det) has O(1) geometric structure in J-1, so the screen onset at eps ~ O(1)
      (kappa ~ 2) is the natural reading; kappa=2/Z would need an engineered F hierarchy.
    * The single most decisive input is NOT a convention: it is whether the pre-strain deviator
      is the screened-profile value (d/J1 ~ -0.03..-0.07, derived from the framework nu's own
      saturation) or the naive deep value (-1/2). Using the deep fiction at the Sun is
      INCONSISTENT (the Sun sits at y=2.2 where the screen is active); the screened value is
      the framework-first one. That mechanism -- screen saturation flattens the strain profile,
      a flat J1 field is pure dilation -- is what makes w small, and it is DERIVED, not posited.""")

# ====================================================================================================
# VERDICT
# ====================================================================================================
print("="*100)
print(" LANE 1 VERDICT")
print("="*100)
print(f"""  (a) EXACT: the det-class directional shear coupling derived with no truncation of det;
      it VANISHES with the pre-strain deviator d and is O(d) with F',F''-coefficients printed
      above. mu contributes zero anisotropy (material-linear shear, as constructed).
  (b) F pinned: K_F + mu/3 = K_eff = a0^2/(16 pi G) = {A0_CANON**2/(16*np.pi*G):.2e} Pa (canonical, kappa=2).
  (c) The GR-stiff shear identification REFUTED: deep-MOND compatibility (J2 = J1^2/6, exact)
      forces mu <= 3 K_eff ~ {3*A0_CANON**2/(16*np.pi*G):.1e} Pa, i.e. v_shear <= 0.12 c: the medium's shear waves
      are NOT gravitational waves (GW170817), and the 6 Z^2 = 201x stiffness hierarchy the deep
      candidate hoped for does NOT exist. w is NOT tiny-by-hierarchy.
  (d) A SECOND, genuine suppression mechanism IS derived: the screen saturates the strain
      (eps -> kappa/2), the galactic strain profile at y=2.2 is nearly flat (dln eps/dln y = 0.085),
      and a flat volumetric field is nearly pure dilation (d/J1 = -q/(3-q) ~ -0.03..-0.06, NOT
      the naive -1/2) -- the screen quenches the pre-strain deviator ~10x, buying ~10-40x in w
      versus the deep-fiction pre-strain (which would give w ~ 5-16: instantly dead).
      BUT the quench is NOT enough for a clean pass: the derived band is
        w = [{w_can_lo:.3f}, {w_can_hi:.2f}] canonical (median {w_can_med:.2f}) vs bound 0.22-0.26
        w = [{w_alt_lo:.3f}, {w_alt_hi:.2f}] alt       (median {w_alt_med:.2f}) vs bound 0.17-0.19
      The band STRADDLES the Cassini gate: central cells sit AT or 1-2x ABOVE it, low corners
      (kappa<=1, mild stiffening, L0-edge scalar reference) clear it by ~2-4x, high corners
      (S~30, p=2, boosted F') fail it by up to ~10x.
  (e) VERDICT: w is NOT DERIVABLE to a number sharper than ~[0.06, 2.5] from the banked
      machinery -- P5 remains a posit, now BOUNDED and MECHANISED but not decided. The named
      missing ingredients that would decide it:
        (m1) the absolute strain normalization kappa (w ~ kappa^2; Verlinde's heuristic pins
             only K_eff*eps^2, i.e. the product, never eps itself);
        (m2) the constitutive reconstruction F(J) from the nu-response (fixes S and f1);
        (m3) the medium's own Q2 kernel (anisotropic-elasticity BVP around the Sun) to replace
             the local-modulation proxy and the scalar-reference mapping (factor ~3 by itself).
      EQUALLY REPORTABLE NEGATIVE (banked above): the 'generically tiny by GR-stiffness' route
      is REFUTED -- no 201x hierarchy exists for the det-class; smallness, if true, comes only
      from the saturation quench, and that lands at the gate's edge, not safely under it.""")
print("EXIT 0")
