#!/usr/bin/env python3
"""
ROUTE 2 -- ENTROPY / INFORMATION EXTREMUM attack on Koide r=sqrt2 / Q=2/3 / cos^2=3/4.

QUESTION: over the space of sqrt-mass configurations, is r=sqrt2 (equiv Q=2/3, cos^2=3/4)
a CRITICAL POINT (max / min / inflection / saddle) of a NATURAL information/entropy functional?

The functionals are DEFINED from ingredients that do NOT mention 2/3 / r=sqrt2 / cos^2=3/4 /
Koide -- only from the sqrt-mass vector v = (sqrt m1, sqrt m2, sqrt m3) and standard
information-theory quantities (Shannon entropy, Fisher information, variance, the democratic
direction (1,1,1)). For EACH functional we sympy/mpmath-derive its stationary point in r and
report whether it lands at r=sqrt2 EXACTLY, near, or elsewhere.

DISCIPLINE:
  - Trace every definition for a smuggled 2/3 / 3/4 / sqrt2 (a definition containing the target
    is the 168th re-labeling, DEAD).
  - "hit" = lands at r=sqrt2 EXACTLY (or with a FORCED small correction), not tuned there.
  - must be charged-LEPTON-specific-compatible: a flavor-blind extremum at 45deg for everyone is
    FALSIFIED by the quarks (Q_up=0.849, Q_down=0.731).

PARAMETRIZATION (Brannen circulant, phase-independent in Q -- sympy-proven elsewhere):
    sqrt(m_k) = M (1 + r cos(phi + 2 pi k/3)),  k=0,1,2
    => Q = 1/3 + r^2/6      (phase phi cancels; the ONLY shape DOF is r >= 0)
    cos^2(theta to (1,1,1)) = 1/(3Q) = 1/(1 + r^2/2)
    Q=2/3 <=> r=sqrt2 <=> cos^2=3/4 <=> theta=30deg(of v to (1,1,1))? -- see note below.

NOTE on the angle convention: cos^2(theta_v,(1,1,1)) = (sum sqrt m)^2/(3 sum m) = 1/(3Q).
   Q=2/3 -> cos^2 = 1/2 (the "45deg" used in the corpus is the angle of the *standard-rep
   component*, an equivalent restatement). We carry cos^2_dem := 1/(3Q) and flag the value
   at Q=2/3 explicitly so there is no ambiguity. The TARGET in r is unambiguous: r=sqrt2.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*86)
print("ROUTE 2 -- ENTROPY / INFORMATION EXTREMUM.  Target (NOT in any definition): r=sqrt2.")
print("="*86)

# --- symbols ---
r, M, phi, t = sp.symbols('r M phi t', real=True)
k = sp.symbols('k', integer=True)

# sqrt-mass components (circulant), masses, and the basic invariants
v = [M*(1 + r*sp.cos(phi + 2*sp.pi*kk/3)) for kk in range(3)]   # sqrt-masses
m = [sp.expand_trig(sp.expand(vi**2)) for vi in v]              # masses
S1 = sp.simplify(sum(v))           # sum sqrt m
S2 = sp.simplify(sum(m))           # sum m
Q_expr = sp.simplify(S2 / S1**2)
print("\n[setup] Q(r) = sum m / (sum sqrt m)^2 =", Q_expr, " (phase-independent)")
Q_of_r = sp.nsimplify(sp.simplify(Q_expr))
print("        Q(r) simplified =", sp.simplify(Q_expr))
# confirm Q = 1/3 + r^2/6
assert sp.simplify(Q_expr - (sp.Rational(1,3) + r**2/6)) == 0, "Q != 1/3 + r^2/6 !!"
print("        CONFIRMED  Q(r) = 1/3 + r^2/6   (sympy-exact, phase cancels)")
print("        => the SHAPE space is the single ray r in [0, inf).  r=sqrt2 <=> Q=2/3.")

# ==========================================================================================
# PART 0 -- Is Q=2/3 itself a special point of the Q-RANGE?  (honesty check)
# ==========================================================================================
print("\n" + "="*86)
print("PART 0 -- Is 2/3 a SPECIAL value in the range of Q?  (no functional yet -- the range itself)")
print("="*86)
print("""  Q(r)=1/3 + r^2/6 is a MONOTONE, smooth, convex parabola in r on [0,inf):
    Q(0)=1/3 (perfect democracy, all sqrt-masses equal), Q-> inf as r-> inf.
    dQ/dr = r/3 (zero only at r=0), d2Q/dr2 = 1/3 (constant>0).
  => Q has NO interior extremum, NO inflection anywhere except the trivial r=0 minimum.
     2/3 is a GENERIC INTERIOR VALUE of Q (it is just r=sqrt2 on a featureless ray).
  HONEST: 2/3 carries NO extremal/critical meaning *as a value of Q itself*. Any 'special'-ness
  must come from an EXTERNAL functional F(r) whose stationary point happens to sit at r=sqrt2.
""")
dQ = sp.diff(sp.Rational(1,3)+r**2/6, r)
d2Q = sp.diff(dQ, r)
print("   dQ/dr =", dQ, " ;  d2Q/dr2 =", d2Q, " (constant, no inflection) ")

def report_stationary(name, F, indep_note, dps=40):
    """Differentiate F(r), solve F'(r)=0 on r>0, classify, compare to sqrt2."""
    print("\n" + "-"*86)
    print(f"FUNCTIONAL: {name}")
    print(f"  independence: {indep_note}")
    Fr = sp.simplify(F)
    print("  F(r) =", Fr)
    dF = sp.simplify(sp.diff(Fr, r))
    print("  F'(r) =", dF)
    # solve on reals
    try:
        sols = sp.solve(sp.Eq(dF, 0), r)
    except Exception as e:
        sols = []
        print("  (symbolic solve failed:", e, ")")
    real_pos = []
    for s in sols:
        try:
            val = complex(s)
            if abs(val.imag) < 1e-12 and val.real > 1e-9:
                real_pos.append(sp.nsimplify(s))
        except Exception:
            # may be symbolic; try numeric
            try:
                val = complex(sp.N(s, 30))
                if abs(val.imag) < 1e-12 and val.real > 1e-9:
                    real_pos.append(s)
            except Exception:
                pass
    print("  stationary r>0 :", real_pos if real_pos else "NONE in (0,inf)")
    sqrt2 = sp.sqrt(2)
    hit = False
    for s in real_pos:
        diff = sp.simplify(s - sqrt2)
        is_exact = (diff == 0)
        try:
            numdiff = float(sp.N(diff, 30))
        except Exception:
            numdiff = float('nan')
        d2 = sp.simplify(sp.diff(Fr, r, 2)).subs(r, s)
        try:
            d2v = float(sp.N(d2, 30))
            kind = "MIN" if d2v > 0 else ("MAX" if d2v < 0 else "INFLECTION/degenerate")
        except Exception:
            d2v, kind = float('nan'), "?"
        print(f"     r*={sp.N(s,20)}  exact==sqrt2? {is_exact}  (r*-sqrt2={numdiff:+.3e})  type={kind}")
        if is_exact:
            hit = True
    if not real_pos:
        print("     -> no interior stationary point: r=sqrt2 is NOT singled out by this functional.")
    elif hit:
        print("     -> *** LANDS AT r=sqrt2 EXACTLY *** (flag for independence audit).")
    else:
        print("     -> stationary point is NOT at sqrt2.")
    return real_pos, hit

# ==========================================================================================
# THE FUNCTIONALS.  Each is built ONLY from v=(sqrt m_k), the masses m_k, the democratic
# direction, and standard info-theory quantities.  None mentions 2/3 / 3/4 / sqrt2 / Koide.
# We use the mass distribution p_k = m_k / sum(m) and the sqrt-mass distribution
# q_k = sqrt(m_k)/sum(sqrt m) as the natural probability vectors on the 3 generations.
# We set phi=0 WLOG for the entropy/Fisher functionals that are phase-dependent, and ALSO
# check phase-robustness numerically afterwards (Q is phase-free; the entropies are not, so
# we must check whether the EXTREMUM in r is phase-free).
# ==========================================================================================
print("\n\n" + "#"*86)
print("# THE FUNCTIONALS  (definitions audited for smuggled 2/3 / 3/4 / sqrt2 -- none present)")
print("#"*86)

phi0 = sp.Integer(0)  # representative phase; phase-robustness checked numerically below

# probability vectors at phi=0
v0 = [vi.subs(phi, phi0) for vi in v]
m0 = [mi.subs(phi, phi0) for mi in m]
S1_0 = sp.simplify(sum(v0))
S2_0 = sp.simplify(sum(m0))
p = [sp.simplify(mi/S2_0) for mi in m0]            # mass distribution  (sum p =1)
qd = [sp.simplify(vi/S1_0) for vi in v0]           # sqrt-mass distribution (sum q =1)

# -----------------------------------------------------------------------------------------
# F1 -- SHANNON ENTROPY of the mass distribution p_k.  H(p) = -sum p log p.
#   "Max-entropy" trivially peaks at r=0 (uniform).  The interesting question: does the
#   entropy of the SQRT-mass distribution, or a constrained max-ent, have a non-trivial
#   stationary point?  We report H(p) extremum honestly.
# -----------------------------------------------------------------------------------------
H_p = -sum(pk*sp.log(pk) for pk in p)
report_stationary("F1: Shannon entropy H(p) of mass distribution p_k=m_k/sum m  (phi=0)",
                  H_p,
                  "definition uses only m_k and log; NO 2/3/sqrt2. (max-ent => expect r=0 trivially)")

# -----------------------------------------------------------------------------------------
# F2 -- Shannon entropy of the SQRT-mass distribution q_k.  Same triviality expected (peak r=0).
# -----------------------------------------------------------------------------------------
H_q = -sum(qk*sp.log(qk) for qk in qd)
report_stationary("F2: Shannon entropy H(q) of sqrt-mass distribution q_k=sqrt(m_k)/sum sqrt m",
                  H_q,
                  "only sqrt(m_k) and log; NO target. (expect trivial r=0 peak)")

# -----------------------------------------------------------------------------------------
# F3 -- "DEMOCRATIC + DEVIATION BALANCE":  the product (or difference) of
#   (a) closeness-to-democracy  D(r) = cos^2(theta_v,(1,1,1)) = (sum v)^2/(3 sum v^2)
#       [= 1/(3Q); MAXIMAL democracy at r=0]  and
#   (b) the "spread" / breaking  B(r) = 1 - D(r)  [breaking of democracy].
# The "maximally democratic AND maximally deviating" balance is the EXTREMUM of D*(1-D),
# a STANDARD concentration functional (Gini/quadratic-entropy form). Audit: built from the
# angle to (1,1,1); NO 2/3 in the definition. D*(1-D) is extremal at D=1/2 by calculus of
# x(1-x) -- and D=1/2 happens to be Q=2/3.  THIS IS THE LOAD-BEARING TEST.
# -----------------------------------------------------------------------------------------
D = sp.simplify(S1_0**2 / (3*S2_0))                  # = 1/(3Q) = cos^2 democratic
D = sp.simplify(D)
print("\n[F3 setup] democratic alignment D(r)=cos^2(v,(1,1,1)) =", D, " (= 1/(3Q))")
F3 = sp.simplify(D*(1-D))   # quadratic-entropy / Gini-type 'balance' functional
report_stationary("F3: democracy-deviation balance  D*(1-D),  D=cos^2(v,(1,1,1))=(sum v)^2/(3 sum m)",
                  F3,
                  "D is the angle-to-democracy ONLY; x(1-x) is the generic balance functional. NO 2/3 smuggled. BUT see trace below.")

# -----------------------------------------------------------------------------------------
# F4 -- FISHER INFORMATION of the mass distribution treated as a function of a 'tilt'
#   parameter, OR the Fisher info of q.  We use the simplest invariant: the Fisher info
#   metric of the family p(r) along r,  I_F(r) = sum_k (1/p_k)(dp_k/dr)^2.  Its stationary
#   points are candidate 'natural scales'.  Audit: only p_k and derivatives; no target.
# -----------------------------------------------------------------------------------------
IF = sp.simplify(sum( (sp.diff(pk, r))**2 / pk for pk in p))
report_stationary("F4: Fisher information I_F(r)=sum (dp_k/dr)^2/p_k of mass distribution along r",
                  IF,
                  "only p_k(r) and d/dr; NO 2/3/sqrt2.")

# -----------------------------------------------------------------------------------------
# F5 -- RENYI-2 / 'inverse participation ratio' of the sqrt-mass distribution:
#   IPR(q) = sum q_k^2.  Extremum = most/least 'localized'. Audit: pure sum of squares.
# -----------------------------------------------------------------------------------------
IPR = sp.simplify(sum(qk**2 for qk in qd))
report_stationary("F5: inverse participation ratio sum q_k^2 (Renyi-2) of sqrt-mass distribution",
                  IPR,
                  "pure sum of squares of q_k; NO target.")

# -----------------------------------------------------------------------------------------
# F6 -- the 'maximal-deviation-at-fixed-democracy' Lagrangian is degenerate on a 1-ray;
#   instead test the VARIANCE of the sqrt-mass distribution normalized by mean, i.e. the
#   squared coefficient of variation CV^2 = Var(v)/mean(v)^2 -- a standard dispersion measure.
#   On the circulant, CV^2 = r^2/2 EXACTLY (the variance of cos over a period). Its 'natural'
#   extremum, and whether CV^2=1 (=> r=sqrt2) is singled out by any balance with entropy.
# -----------------------------------------------------------------------------------------
mean_v = sp.simplify(S1_0/3)
var_v = sp.simplify(sum((vi-mean_v)**2 for vi in v0)/3)
CV2 = sp.simplify(var_v/mean_v**2)
print("\n[F6 setup] CV^2(v) = Var(sqrt m)/mean(sqrt m)^2 =", CV2, "  (=> r=sqrt2 means CV^2=1)")
# F6: balance of dispersion against concentration: CV^2 * (concentration) -- test D*CV^2 etc.
F6 = sp.simplify(D - var_v/mean_v**2 * D)  # placeholder generic; real content reported below
print("   NOTE: CV^2 = r^2/2. So 'CV^2 = 1' (unit dispersion) <=> r=sqrt2. Is CV^2=1 forced by")
print("   any *entropy* extremum?  Tested via the max-ent-at-fixed-dispersion below (PART 2).")

# ==========================================================================================
# PART 1 -- THE F3 HIT, AUDITED.  D*(1-D) peaks at r=sqrt2 EXACTLY (a MAXIMUM). Is it real?
# ==========================================================================================
print("\n\n" + "="*86)
print("PART 1 -- AUDIT THE F3 HIT:  D*(1-D) is MAXIMAL at r=sqrt2.  Is 2/3 smuggled?")
print("="*86)
print("""
  D(r) = 1/(3Q) = 2/(r^2+2) is the cos^2 democratic alignment (max=1 at r=0, ->0 at r->inf).
  The functional x(1-x) has its UNIQUE maximum at x=1/2 (elementary, target-free calculus).
  So F3 is maximal where D=1/2.  And D=1/2  <=>  1/(3Q)=1/2  <=>  Q=2/3  <=>  r=sqrt2.

  THE SMUGGLE QUESTION: is 'D=1/2' an INDEPENDENT condition, or a disguised 'Q=2/3'?
""")
# Trace: the value of the EXTREMUM-LOCATING condition is x=1/2, a property of x(1-x), NOT of Q.
# But the *map* from x to r is D=1/(3Q): x=1/2 -> Q=2/3. Is choosing the variable 'D' (vs some
# other monotone function of r) what forces 1/2 -> 2/3?  Test the COVARIANCE of the extremum:
print("  TEST A -- COORDINATE-DEPENDENCE of the x(1-x) extremum (the killer test).")
print("  x(1-x) peaks at x=1/2 only because x is THIS particular variable. Re-run the SAME")
print("  'balance functional' g(1-g) with g = a DIFFERENT but equally-natural concentration")
print("  measure, and see if the peak still lands at r=sqrt2 or moves. If it MOVES, the r=sqrt2")
print("  was an artifact of choosing g=D (=1/3Q); the principle is coordinate-arbitrary => DEAD.")

# candidate concentration measures g(r), each in [0,1], each 'maximally democratic' at r=0:
cands = {}
# g1 = D = cos^2 democratic = 2/(r^2+2)
cands['D=cos^2_dem=1/(3Q)'] = sp.simplify(2/(r**2+2))
# g2 = D^2 (equally natural: squared alignment)
cands['D^2'] = sp.simplify((2/(r**2+2))**2)
# g3 = sqrt(D) (alignment, not squared) -- |cos| not cos^2
cands['sqrt(D)=|cos|_dem'] = sp.simplify(sp.sqrt(2/(r**2+2)))
# g4 = the normalized Renyi-2 of q SCALED to [0,1]: (3*IPR-1)/2 maps r=0->0?? actually IPR=Q,
#      define participation-based concentration: (IPR - 1/3)/(1-1/3)?? IPR unbounded; skip scale
# g5 = exp(-CV^2) = exp(-r^2/2): a natural [0,1] 'order parameter', democratic(=1) at r=0
cands['exp(-CV^2)=exp(-r^2/2)'] = sp.simplify(sp.exp(-r**2/2))
# g6 = 1/(1+CV^2) = 2/(r^2+2) == D !! (note CV^2=r^2/2 so 1/(1+CV^2)=2/(r^2+2)=D). same as g1.
# g7 = Shannon entropy of q normalized to [0,1] (H/log3), democratic(=1) at r=0
Hq = -sum(qk*sp.log(qk) for qk in qd)
cands['H(q)/log3 (Shannon)'] = sp.simplify(Hq/sp.log(3))

print("\n   For each concentration measure g(r) in [0,1] (all maximal at r=0, the democratic")
print("   point), find argmax of g*(1-g) and compare to sqrt2 (=1.41421356):")
for nm, g in cands.items():
    Fg = sp.simplify(g*(1-g))
    dFg = sp.simplify(sp.diff(Fg, r))
    # numeric root-find on (0, 8)
    f = sp.lambdify(r, dFg, 'mpmath')
    roots = []
    xs = [mp.mpf(i)/20 for i in range(2, 161)]
    prev = None
    for x in xs:
        try:
            val = f(x)
            if hasattr(val, 'imag') and abs(mp.im(val)) > 1e-20:
                prev = None  # complex (a q went negative) -> domain edge, reset bracket
                continue
            val = mp.re(val)
        except Exception:
            prev = None
            continue
        if prev is not None and prev[1]*val < 0:
            try:
                rt = mp.findroot(f, (prev[0]+x)/2)
                if rt > 1e-6 and all(abs(rt-rr)>1e-9 for rr in roots):
                    roots.append(rt)
            except Exception:
                pass
        prev = (x, val)
    rk = ", ".join(mp.nstr(rt, 12) for rt in roots) if roots else "none in (0,8)"
    flag = ""
    for rt in roots:
        if abs(rt - mp.sqrt(2)) < mp.mpf('1e-8'):
            flag = "  <== sqrt2"
    print(f"     g = {nm:28s} argmax g(1-g): r* = {rk}{flag}")

print("""
  TEST A RESULT (read above): the argmax of g*(1-g) lands at r=sqrt2 ONLY for the measures
  that are MONOTONE-1/(3Q)-LINEAR (g=D and its CV-form 1/(1+CV^2)). For g=D^2, sqrt(D),
  exp(-CV^2), Shannon-H, the 'balance' peak is at a DIFFERENT r. => the r=sqrt2 location is
  NOT invariant under the (arbitrary) choice of which [0,1] concentration measure you balance.
  The x=1/2 of x(1-x) is real and target-free, but the PULLBACK to r=sqrt2 happens ONLY when
  you pre-select g = 1/(3Q) -- i.e. you must already privilege the quantity whose half-value
  is Q=2/3. That privileging IS the smuggle: 'balance D at 1/2' is coordinate-equivalent to
  'set Q=2/3'.  F3 is the 168th re-labeling unless an INDEPENDENT reason forces g=D specifically.
""")

# ==========================================================================================
# PART 2 -- THE PROPER MAX-ENTROPY PROBLEM.  "Max-entropy of the mass distribution" only has
# content WITH a constraint. The natural target-free constraint is "fixed dispersion of the
# sqrt-masses" (fix CV^2, i.e. fix the second moment). Solve: does max-ent pick a SPECIAL
# dispersion = the one with CV^2=1 (r=sqrt2)? Or is the dispersion a FREE input?
# ==========================================================================================
print("\n\n" + "="*86)
print("PART 2 -- MAX-ENTROPY with a target-free constraint. Is r=sqrt2 the max-ent point?")
print("="*86)
print("""
  Plain max-entropy over a 3-point distribution gives the UNIFORM distribution (r=0), i.e. the
  perfectly-democratic spectrum -- NOT Koide. To get a non-trivial r you must CONSTRAIN. The
  only target-free constraint is to fix some dispersion functional (mean energy, variance).
  Lagrange: maximize H(p) - lambda*<f> gives a Gibbs/Boltzmann p_k ~ exp(-lambda f_k). The
  resulting r is a FREE FUNCTION of lambda -- it scans the WHOLE ray [0,inf). There is no
  lambda that the entropy principle ITSELF prefers: the constraint VALUE is an external input.
  => max-ent does NOT pick r=sqrt2; it picks whatever dispersion you feed it. NON-DIAGNOSTIC.
""")
# Demonstrate: Gibbs over generations with a linear 'energy' E_k = k gives p_k ~ x^k (x=exp(-lambda)).
# Map that to a circulant r? The Gibbs distribution is NOT circulant-shaped, so it doesn't even
# live on our 1-ray. Show the entropy of the circulant family H(p(r)) is MONOTONE DECREASING in
# r (max at r=0), so 'max H' => r=0, not sqrt2:
x = sp.symbols('x', positive=True)
Hp_num = sp.lambdify(r, sp.simplify(-sum(pk*sp.log(pk) for pk in p)), 'mpmath')
print("  H(p(r)) along the circulant ray (max-ent would pick the LARGEST):")
for rr in [mp.mpf('0.0001'), mp.mpf('0.5'), mp.mpf('1.0'), mp.sqrt(2), mp.mpf('1.7'), mp.mpf('2.0')]:
    try:
        hv = mp.re(Hp_num(rr))
    except Exception:
        hv = float('nan')
    tag = "  <- r=sqrt2" if abs(rr-mp.sqrt(2))<1e-6 else ""
    print(f"     r={mp.nstr(rr,8):>10s}  H(p)= {mp.nstr(hv,8)}{tag}")
print("  => H(p) is MAXIMAL at r->0 (uniform), NOT at sqrt2. Unconstrained max-ent kills Koide;")
print("     constrained max-ent leaves r free. r=sqrt2 is NOT a max-entropy point. NULL.")

# ==========================================================================================
# PART 3 -- THE F5 SMOKING GUN + CROSS-FERMION.  F5 (IPR of sqrt-mass dist) == Q EXACTLY.
# ==========================================================================================
print("\n\n" + "="*86)
print("PART 3 -- WHY 'information functional = 2/3' is circular: the IPR IS Q.")
print("="*86)
IPR = sp.simplify(sum(qk**2 for qk in qd))
print("  F5 inverse-participation-ratio sum_k q_k^2  with q_k = sqrt(m_k)/sum sqrt m :")
print("     sum q_k^2 = (sum m)/(sum sqrt m)^2  =  Q   IDENTICALLY.   sympy:", IPR, "= 1/3+r^2/6 = Q")
assert sp.simplify(IPR - (sp.Rational(1,3)+r**2/6)) == 0
print("  => ANY information functional built as 'the Renyi-2 / participation of the sqrt-mass")
print("     distribution = 1/2' is LITERALLY 'Q=2/3' rewritten. Setting it to a value (2/3) is")
print("     the definition of Koide, not a derivation. (This is the cleanest smuggle to flag.)")

print("\n  CROSS-FERMION (the falsifier any extremum claim must pass):")
def Qgeo(masses):
    masses = [mp.mpf(str(x)) for x in masses]
    s = sum(mp.sqrt(x) for x in masses)
    return sum(masses)/s**2
lep = Qgeo([0.51099895, 105.6583755, 1776.86])
up  = Qgeo([2.16, 1270.0, 172690.0])
dn  = Qgeo([4.67, 93.4, 4180.0])
for nm, Qv in [("charged leptons", lep), ("up quarks", up), ("down quarks", dn)]:
    rv = mp.sqrt(6*Qv-2)
    Dv = 1/(3*Qv)
    bal = Dv*(1-Dv)
    print(f"     {nm:16s} Q={mp.nstr(Qv,8)}  r_eff={mp.nstr(rv,8)}  D=1/(3Q)={mp.nstr(Dv,8)}  D(1-D)={mp.nstr(bal,8)}")
print("""  The 'balance' D(1-D) is MAXIMIZED (=1/4) only at the leptons' D=1/2. Quarks sit OFF the
  maximum (up D=0.393 -> 0.238; down D=0.456 -> 0.248). So IF nature maximized D(1-D) for every
  fermion, quarks would be driven to D=1/2 (Q=2/3) too -- they are NOT. => a flavor-blind
  'maximize democracy-deviation balance' principle is CROSS-FERMION FALSIFIED. It would need a
  charged-lepton-specific reason to apply only to leptons -- and the functional carries none.""")

# ==========================================================================================
# VERDICT
# ==========================================================================================
print("\n\n" + "="*86)
print("ROUTE 2 VERDICT")
print("="*86)
print("""
  * Is 2/3 a special VALUE of Q? NO. Q(r)=1/3+r^2/6 is a featureless monotone parabola; 2/3 is a
    generic interior value (PART 0). No extremal meaning as a value of Q.
  * Unconstrained max-entropy of the mass distribution => r=0 (uniform), NOT r=sqrt2 (PART 2).
    Constrained max-ent leaves r a free function of the Lagrange multiplier => NON-DIAGNOSTIC.
  * Shannon H(p), H(q), Fisher info I_F, Renyi-2 IPR: NONE has an interior stationary point at
    sqrt2 (F1,F2,F4,F5). IPR is IDENTICALLY Q, so 'IPR=2/3' is a re-labeling (PART 3).
  * The ONE functional that peaks AT r=sqrt2 -- F3, the democracy-deviation balance D(1-D) -- is
    maximal there ONLY because D=1/(3Q) and x(1-x) peaks at x=1/2, and D=1/2 <=> Q=2/3. The peak
    MOVES off sqrt2 the instant you use any other equally-natural [0,1] concentration measure
    (D^2 -> 0.910, sqrt(D) -> 2.449, exp(-CV^2) -> 1.177): r=sqrt2 is NOT coordinate-invariant,
    so 'balance D at 1/2' is coordinate-equivalent to imposing Q=2/3 (PART 1). 168th re-labeling.
  * Cross-fermion: maximizing D(1-D) is flavor-blind => would force quarks to 2/3 too (FALSE).
    No charged-lepton-specific ingredient in any functional (PART 3).

  NULL. r=sqrt2 / Q=2/3 / cos^2=3/4 is NOT the non-circular extremum of a natural information/
  entropy functional. The only 'hit' (D(1-D)) smuggles 2/3 through the choice of the variable D
  whose half-value is Q=2/3, fails coordinate-invariance, and is cross-fermion-falsified.
  The last door (Route 2) is closed. No maximal-re-verification flag warranted.
""")
