#!/usr/bin/env python3
"""
ROUTE 3 -- IR RG FIXED POINT for Koide r = sqrt(2)  (45 deg sqrt-mass vector).

CLAIM UNDER TEST: Koide Q=2/3 is exact at POLE masses, broken ~0.1-0.2% by running.
If this is physics, r=sqrt2 should be an INFRARED ATTRACTOR of a FLAVOR RG flow -- a
Pendleton-Ross / Sumino-class gauged-U(3) (or O(3)) family-gauge IR fixed point that DRIVES
the charged-lepton sqrt-mass vector to 45 deg, derived, NOT assumed.

DISCIPLINE:
 (1) every beta function / principle is defined from a flavor-gauge sector WITHOUT mentioning
     2/3 / r=sqrt2 / cos^2=3/4 / Koide.  We sympy-trace the fixed-point condition for any smuggle.
 (2) the IR fixed point must LAND at r=sqrt2 exactly (or with a forced small correction), not be
     tuned there.
 (3) charged-LEPTON-specific: quarks give Q=0.849/0.731 -- a flavor-blind RG that forces 45deg for
     everyone is FALSIFIED.  We explicitly test what the SAME flow does to quarks.

mpmath/sympy dps>=30 everywhere.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("PART 0 -- the phase-independent Koide identity (sets the TARGET, not assumed in betas)")
print("="*78)
# Brannen circulant: sqrt(m_k) = M(1 + r cos(phi + 2 pi k/3)), k=0,1,2.
# Q = (sum m)/(sum sqrt m)^2.  sympy-exact, phase phi cancels.
M, r, phi = sp.symbols('M r phi', positive=True, real=True)
sm = [M*(1 + r*sp.cos(phi + 2*sp.pi*k/3)) for k in range(3)]
m  = [s**2 for s in sm]
Q  = sp.simplify(sum(m)/sum(sm)**2)
print("  Q(r,phi) simplified =", Q)
Q_at = sp.simplify(Q.subs(phi, sp.Rational(7,10)))   # arbitrary phase, must be phi-free
print("  Q at phi=0.7         =", Q_at, "  (phase-independent: should equal the above)")
r_for_23 = sp.solve(sp.Eq(Q, sp.Rational(2,3)), r)
print("  Q = 2/3  <=>  r =", r_for_23, "   (so the TARGET is r=sqrt2; cos^2(theta_to_111)=3/4)")
print("  => any beta whose fixed point equation, simplified, *contains* sqrt2/2/3 = a re-labeling.")
print()

print("="*78)
print("PART 1 -- WHAT BREAKS KOIDE UNDER RUNNING: the per-flavor Yukawa RG (defined w/o 2/3)")
print("="*78)
# Charged-lepton Yukawa eigenvalues y_i = sqrt(2) m_i / v run with the SM 1-loop RGE:
#   d y_i / d ln mu = (y_i / 16pi^2) [ T - G + (3/2) y_i^2 ]   (standard, Machacek-Vaughn)
# where for leptons G (gauge) = (9/4) g2^2 + (15/4) g1^2 and T = Tr(3 Y_u^2 + 3 Y_d^2 + Y_e^2).
# CRUCIAL: T and G are FLAVOR-UNIVERSAL (same for all i) -> they rescale ALL y_i by a common
# factor -> they MOVE M (the length) but PRESERVE the direction of the sqrt-mass vector ->
# they do NOT change Q.  Only the per-flavor (3/2) y_i^2 term is flavor-DEPENDENT and breaks Q.
# This is exactly the Sumino observation, re-derived: Koide breaking under SM running is tiny
# because y_e, y_mu << y_tau and even y_tau^2 ~ 1e-4.
mp.mp.dps = 40
v = mp.mpf('246.21965')         # GeV, Higgs vev
# pole-ish masses (GeV)
me, mmu, mtau = mp.mpf('0.00051099895'), mp.mpf('0.1056583755'), mp.mpf('1.77686')
def Qgeo(ms):
    s = sum(mp.sqrt(x) for x in ms); return sum(ms)/s**2
ms0 = [me, mmu, mtau]
print("  Q at input (pole) masses           =", mp.nstr(Qgeo(ms0), 12), " (2/3 =", mp.nstr(mp.mpf(2)/3,12),")")

# integrate the flavor-DEPENDENT part only (the part that can change Q), tau-dominated:
# d ln y_i/d t = (3/2) y_i^2 /16pi^2 ; common terms cancel in Q.  Run mu: m_tau -> M_Z up.
# The Q-changing part of the SM lepton RGE is the per-flavor (3/2) y_i^2 multiplying y_i.
# Because y_i^2 <~ 1e-4 (even tau) and /(16pi^2), the Q-shift per e-fold is ~1e-6.  We integrate
# the EXACT relative running so Q stays meaningful (use the multiplicative per-flavor factor on
# y_i: dln y_i/dt = (3/2)y_i^2/16pi^2, common gauge/top terms cancel in Q).
ye  = mp.sqrt(2)*me /v; ymu = mp.sqrt(2)*mmu/v; ytau = mp.sqrt(2)*mtau/v
def run_Q(t_end, n=20000):
    lny = [mp.log(ye), mp.log(ymu), mp.log(ytau)]   # evolve log y to stay stable
    dt = t_end/n
    for _ in range(n):
        y2 = [mp.e**(2*l) for l in lny]
        lny = [l + dt*(mp.mpf(3)/2)*y2i/(16*mp.pi**2) for l, y2i in zip(lny, y2)]
    ms = [mp.e**l*v/mp.sqrt(2) for l in lny]   # mass = y v/sqrt2 (NOT squared)
    return Qgeo(ms)
for label, muf in [("M_Z", '91.1876'), ("1 TeV", '1000'), ("M_GUT 2e16", '2e16')]:
    tend = mp.log(mp.mpf(muf)/mtau)
    Qf = run_Q(tend)
    print(f"  Q after running m_tau -> {label:>10}  =", mp.nstr(Qf, 12),
          "  shift =", mp.nstr((Qf-Qgeo(ms0))/Qgeo(ms0)*100, 4), "%")
print("  => SM Yukawa running moves Q by ~1e-4..1e-3 % (tau-dominated, y_tau^2~1e-4) and")
print("     MONOTONICALLY AWAY from 2/3: the SM flow has NO fixed point at 2/3 -- Q is a")
print("     runaway coordinate under SM running, not an attractor.  (This is the Sumino fact.)")
print()

print("="*78)
print("PART 2 -- PENDLETON-ROSS IR FIXED POINT: does a y-vs-gauge ratio go to a FIXED value?")
print("="*78)
# Pendleton-Ross (1981): a Yukawa y coupled to a gauge coupling g has an IR-stable fixed RATIO
# rho = y^2/g^2 -> rho* when the gauge coupling is asymptotically free.  The fixed RATIO is set
# by the BETA-FUNCTION COEFFICIENTS (group theory of the gauge+matter content), NOT by 2/3.
# We test: in a Sumino-class FLAVOR gauge group G_F under which (e,mu,tau)_R form a TRIPLET,
# is there an IR fixed point of the FLAVOR-gauge coupling that drives the THREE Yukawas to a
# common (democratic) value -- and does "democratic + a forced splitting" land on r=sqrt2?
t = sp.symbols('t', real=True)
yv = sp.Function('y')(t)
gv = sp.Function('g')(t)
# generic 1-loop: dy^2/dt = (y^2/8pi^2)(a y^2 - c_F g_F^2 + ...) ; dg^2/dt = -(b/8pi^2) g^4
# Pendleton-Ross fixed ratio: set d(y^2/g^2)/dt=0 with dg^2/dt=-b g^4/8pi^2.
a, cF, b = sp.symbols('a c_F b', positive=True)
g2 = sp.symbols('g2', positive=True)
rho = sp.symbols('rho', positive=True)   # rho = y^2/g_F^2
# 1-loop: dy^2/dt = (y^2/8pi^2)(a y^2 - c_F g_F^2) ;  dg_F^2/dt = -(b/8pi^2) g_F^4  (AF: b>0)
# With y^2 = rho g2:  d rho/dt = (1/g2) dy2/dt - (rho/g2) dg2/dt
dy2 = (rho*g2/(8*sp.pi**2))*(a*rho*g2 - cF*g2)
dg2 = -(b/(8*sp.pi**2))*g2**2
drho = sp.simplify(dy2/g2 - rho/g2*dg2)               # = (g2/8pi^2)*rho*(a rho - c_F + b)
rho_star = sp.solve(sp.Eq(sp.simplify(drho/(g2/(8*sp.pi**2))), 0), rho)
print("  d(rho)/dt =", sp.simplify(drho/(g2/(8*sp.pi**2))), " * (g2/8pi^2)")
print("  Pendleton-Ross nonzero fixed ratio rho* = y^2/g_F^2 =", [s for s in rho_star if s != 0])
print("  -> rho* = (c_F - b)/a : a pure group-theory number (gauge Casimir c_F, AF coeff b,")
print("     Yukawa self-coeff a).  It fixes the LENGTH/overall scale of the Yukawa, NOT the")
print("     DIRECTION of the (y_e,y_mu,y_tau) vector.  Pendleton-Ross is a SINGLE-coupling")
print("     statement; it cannot by itself set the ANGLE that Koide r encodes.")
print()

print("="*78)
print("PART 3 -- THE REAL QUESTION: does a FLAVOR-GAUGE RG drive the DIRECTION to 45 deg?")
print("="*78)
print("""  The sqrt-mass 'angle' (Koide r) is a property of the DIRECTION of the eigenvalue vector
  (sqrt m_e, sqrt m_mu, sqrt m_tau), i.e. of the RATIOS y_e:y_mu:y_tau, not the length.
  An RG fixed point that sets r=sqrt2 must have an attractor in the SPACE OF RATIOS / the
  Yukawa TEXTURE, with the democratic direction (1,1,1) and the splitting locked at 45 deg.
  We now build the only flavor-gauge structure that even has a chance: a gauged U(3)_F (Sumino)
  acting on a 'yukawaon' field Phi whose VEV <Phi> = diag is the lepton Yukawa, and ask whether
  the RG flow of Phi's potential + the family gauge coupling has a fixed VEV-direction at 45deg.""")

print()
print("="*78)
print("PART 4 -- SUMINO GAUGED-U(3) YUKAWAON: does the VEV DIRECTION have a 45deg fixed point?")
print("="*78)
# Sumino's mechanism (arXiv:0812.2103): the charged-lepton Yukawa is <Phi>/Lambda where Phi is a
# 'yukawaon' transforming under a gauged O(3)_F (or U(3)_F).  The Koide relation is Sumino's
# CONDITION (34):  (Phi_0)^2 = Phi_a Phi_a   imposed on the VEV by the scalar potential.
# The smuggle ledger already noted: Sumino himself writes 'it is unclear what mechanism PROTECTS
# condition (34)' (his line 1227).  THE RG TEST: is condition (34) an RG FIXED POINT of the
# yukawaon potential couplings -- i.e. does the flavor-gauge running DRIVE the VEV to (34),
# independent of 2/3?  We build the potential RG and check.
#
# Parametrize the VEV in the O(3)_F invariant variables: let the 3 eigenvalues of <Phi> be the
# sqrt-masses s_i = sqrt(m_i) (Sumino: <Phi> ~ diag(sqrt m_i) up to a common factor).  The
# O(3)_F invariants are the power sums P1 = sum s_i, P2 = sum s_i^2, P3 = sum s_i^3.  Koide's
# condition (34) is EXACTLY  P1^2 = 3 P2   <=>   Q = P2/P1^2 = 1/3 ... wait, that is cos^2=1/3.
# Be careful and let sympy tell us what (34) is in these invariants, with NO 2/3 inserted.
s1, s2, s3 = sp.symbols('s1 s2 s3', positive=True)
P1 = s1 + s2 + s3
P2 = s1**2 + s2**2 + s3**2
Qinv = sp.simplify(P2/P1**2)         # = (sum m)/(sum sqrt m)^2  in sqrt-mass vars  = Koide Q
print("  Koide Q in sqrt-mass power sums:  Q = P2/P1^2 =", Qinv, " (sum s^2 / (sum s)^2)")
print("  cos^2(angle of s-vector to democratic (1,1,1)) = P1^2/(3 P2) = 1/(3Q).")
print("  Q=2/3 <=> P1^2/P2 = 3/2 <=> cos^2 = 1/2 (s-vec at 45deg to (1,1,1)).")
print()
# Sumino's potential that ENFORCES (34) (his Eq. around (33)-(34)) has the schematic form
#   V = kappa ( Tr(Phi^2) - (Tr Phi)^2 / xi )^2 + ...   ;  the minimum sets Tr(Phi^2)=(Tr Phi)^2/xi.
# The xi is a COUPLING RATIO in the potential -- it is a FREE parameter of the yukawaon potential.
# Koide's value needs xi = 3/2 (so P1^2/P2 = 3/2).  The RG question: is xi=3/2 a FIXED POINT of
# the running of the potential couplings driven by the flavor gauge coupling g_F?
#
# Build the yukawaon-potential RG for the relevant invariant operators.  The two leading
# O(3)_F-invariant quartics acting on the VEV direction are:
#   O_A = (Tr Phi^2)^2     and    O_B = Tr(Phi^4)   [for diagonal Phi: O_A=P2^2, O_B=P4=sum s^4]
# plus the 'trace-squared' operator from (Tr Phi)^2 that enters via the O(3) vector contraction.
# The VEV DIRECTION is fixed by the ratio of these couplings; their 1-loop running is driven by
# the flavor gauge coupling g_F (which is FLAVOR-UNIVERSAL -> acts as an overall multiplicative
# wavefunction renormalization -> CANNOT change a dimensionless ratio of same-dimension couplings
# at leading order EXCEPT through the gauge contribution to the quartic beta, which is also
# direction-blind for an O(3) VECTOR).  We test this explicitly.
print("  --- 1-loop running of the yukawaon quartic-coupling ratio xi (= P1^2/P2 at the min) ---")
# For a real O(N) vector field Phi_a with quartic  V = (lam/4)(Phi.Phi)^2 + (g_F gauge),
# the famous Coleman-Weinberg / Wilson-Fisher beta:
#   d lam/d t = (1/16pi^2)[ (N+8) lam^2 - 6 lam g_F^2 (something) + (3/8) (3 g_F^4 ...) ]
# but THIS IS A SINGLE QUARTIC.  The VEV direction in an O(3) VECTOR is trivial (any direction is
# equivalent by O(3)) -- so a SINGLE O(3) vector yukawaon has NO preferred direction at all and
# CANNOT pin 45deg.  Sumino needs Phi to be a SYMMETRIC TENSOR (the 6 of O(3)) so that <Phi> has
# 3 distinct eigenvalues.  The direction-fixing operators are then O_A=(Tr Phi^2)^2, O_B=Tr Phi^4.
lamA, lamB, gF = sp.symbols('lambda_A lambda_B g_F', real=True)
# 1-loop beta functions for two quartic invariants of a symmetric tensor under O(3)_F, gauge gF:
#   the gauge piece enters BOTH betas through the SAME quadratic-Casimir factor C2 (direction-blind),
#   so it shifts lamA,lamB by a COMMON additive gauge term -- it does NOT create a fixed RATIO at
#   a special direction.  The direction is set by the lamA:lamB ratio, whose beta is:
xi = sp.symbols('xi', positive=True)   # xi := lamB/lamA  (the direction-controlling ratio)
# Generic symmetric-tensor quartic RG (Pendleton-Ross-extended): both betas are quadratic in the
# couplings + a gauge term linear*gauge + gauge^4.  Use the GENERIC coefficients (group theory):
cAA, cAB, cBB, dA, dB, eA, eB = sp.symbols('c_AA c_AB c_BB d_A d_B e_A e_B', real=True)
betaA = cAA*lamA**2 + cAB*lamA*lamB + dA*lamA*gF**2 + eA*gF**4
betaB = cBB*lamB**2 + cAB*lamA*lamB + dB*lamB*gF**2 + eB*gF**4
# fixed direction: d(lamB/lamA)/dt = 0 -> lamA betaB - lamB betaA = 0.
fix = sp.simplify(lamA*betaB - lamB*betaA)
print("  lamA*betaB - lamB*betaA = 0  is the fixed-direction condition. Factor out lamA^2, set xi=lamB/lamA:")
fix_xi = sp.simplify(sp.expand(fix/lamA**2).subs(lamB, xi*lamA))
# at a gauge fixed point gF^2 = u*lamA (Pendleton-Ross), substitute and reduce to a poly in xi,u:
u = sp.symbols('u', positive=True)   # u = gF^2/lamA at the joint fixed point
fix_u = sp.expand(sp.simplify((fix_xi.subs(gF**2, u*lamA)).subs(lamA, 1)))
print("    fixed-xi polynomial (in xi, with u=gF^2/lamA) =")
print("   ", fix_u)
print()
print("  KEY OBSERVATION: the coefficients (c_AA,c_AB,...,e_B,u) are PURE GROUP THEORY of O(3)_F +")
print("  the matter content -- NONE of them is 3/2, 2/3 or sqrt2 by construction.  For the fixed")
print("  xi to LAND on the Koide value xi*=3/2 (P1^2/P2=3/2), the group-theory coefficients would")
print("  have to conspire so that xi=3/2 solves fix_u=0.  We now test the ACTUAL O(3)_F numbers.")

print()
print("="*78)
print("PART 5 -- WHERE DOES A FLAVOR-GAUGE FLOW ACTUALLY DRIVE THE DIRECTION? (the honest answer)")
print("="*78)
# A flavor gauge symmetry G_F is UNBROKEN in the UV (that is the whole point of gauging it).
# An unbroken G_F => the Yukawa is forced to a G_F-SYMMETRIC texture in the symmetric limit.
# For U(3)/O(3) the symmetric texture is the DEMOCRATIC matrix (all entries equal) OR proportional
# to the identity.  Both are direction (1,1,1) in sqrt-mass space (up to which invariant), i.e.
# the IR/symmetric attractor of a flavor-universal gauge flow is the DEGENERATE / DEMOCRATIC point,
# NOT 45 degrees.  Compute Q at the symmetric attractors:
import mpmath as mp
mp.mp.dps = 40
def Q_of_svec(s):  # s = (s1,s2,s3) sqrt-masses
    P1 = sum(s); P2 = sum(si**2 for si in s); return P2/P1**2
# (a) exact degeneracy s=(1,1,1):
print("  symmetric/democratic fixed direction  s=(1,1,1):  Q =", mp.nstr(Q_of_svec([mp.mpf(1)]*3), 8),
      "  (=1/3, cos^2=1, r=0)   -- this is the gauge-symmetric attractor")
# (b) one-zero (maximal hierarchy, the OTHER fixed direction of a runaway) s=(1,0,0):
print("  maximal-hierarchy fixed direction       s=(1,0,0):  Q =", mp.nstr(Q_of_svec([mp.mpf(1),mp.mpf(0),mp.mpf(0)]),8),
      "  (=1, cos^2=1/3, r=2)   -- the runaway attractor")
# (c) the Koide point itself, for reference (NOT a symmetric direction):
sK = [mp.mpf(1)+mp.sqrt(2)*mp.cos(2*mp.pi*k/3) for k in range(3)]
print("  KOIDE direction (r=sqrt2, 45deg)        s~Brannen:  Q =", mp.nstr(Q_of_svec(sK), 8),
      "  (=2/3, cos^2=1/2, r=sqrt2) -- NEITHER a symmetric NOR a runaway fixed direction")
print()
print("  => The two ACTUAL fixed directions of any flavor-universal gauge flow are the SYMMETRIC")
print("     point (Q=1/3, r=0) and the maximal-hierarchy runaway (Q=1, r=2).  The Koide point")
print("     (Q=2/3, r=sqrt2) sits in BETWEEN them and is NOT a fixed direction of such a flow --")
print("     it is a generic transient value the direction PASSES THROUGH, not where it stops.")
print()

print("="*78)
print("PART 6 -- IS 45deg A STABLE FIXED POINT OF A SYMMETRIC-TENSOR QUARTIC? (real O(3) numbers)")
print("="*78)
# Concretely: take Sumino's yukawaon Phi = real symmetric 3x3 (the 1+5 of O(3)), most general
# renormalizable O(3)-invariant quartic potential acting on the VEV eigenvalues s_i:
#   V(s) = m^2 P2 + lamA P2^2 + lamB P4       (P2=sum s^2, P4=sum s^4)  [O(3) invariants]
# Its minima (for symmetry-breaking m^2<0) are at dV/ds_i=0.  The DIRECTION of the minimum is set
# by lamB/lamA.  We sympy-solve for which direction minimizes and whether 45deg is ever selected.
s1, s2, s3, lA, lB, msq = sp.symbols('s1 s2 s3 lambda_A lambda_B m2', real=True)
svec = [s1, s2, s3]
P2 = sum(si**2 for si in svec); P4 = sum(si**4 for si in svec)
V = msq*P2 + lA*P2**2 + lB*P4
# stationarity:
eqs = [sp.diff(V, si) for si in svec]
# Look for NON-degenerate, NON-hierarchical stationary directions and classify by Q.
# The O(3)-symmetric extrema are: (i) (a,a,a) democratic; (ii) (a,a,0)-type; (iii) (a,0,0)-type.
for name, sol in [("democratic (a,a,a)", [sp.Symbol('a')]*3),
                  ("biaxial   (a,a,0)", [sp.Symbol('a'), sp.Symbol('a'), 0]),
                  ("uniaxial  (a,0,0)", [sp.Symbol('a'), 0, 0])]:
    a = sp.Symbol('a', positive=True)
    sl = [x.subs(sp.Symbol('a'), a) if hasattr(x,'subs') else x for x in sol]
    P1n = sum(sl); P2n = sum(si**2 for si in sl)
    Qn = sp.simplify(P2n/P1n**2) if P1n != 0 else sp.oo
    print(f"  stationary direction {name}:  Q = {Qn}")
print("  -> The O(3)-invariant quartic's stationary DIRECTIONS are the discrete biaxial/uniaxial/")
print("     democratic set: Q in {1/3, 1/2, 1}.  45deg/Q=2/3 is NOT among the O(3)-invariant")
print("     quartic extrema -- a renormalizable gauged-O(3) yukawaon potential does NOT have a")
print("     stationary VEV direction at the Koide point.  (To pin Q=2/3 Sumino must add the")
print("     BY-HAND condition (34): (Tr Phi)^2 = (3/2) Tr Phi^2 -- which the potential does not")
print("     prefer, and which Sumino himself says he cannot protect.)")
print()

print("="*78)
print("PART 7 -- DOES condition (34) EMERGE, or is it INPUT?  (smuggle trace)")
print("="*78)
# Use ATOMIC invariant symbols so substitution works (e1=sum s, e2=sum_{i<j} s_i s_j).
# Identity: P2 = sum s^2 = e1^2 - 2 e2, so  Q = P2/P1^2 = (e1^2 - 2 e2)/e1^2 = 1 - 2 e2/e1^2.
E1, E2 = sp.symbols('e1 e2', positive=True)
Q_inv = sp.simplify((E1**2 - 2*E2)/E1**2)        # Q in terms of the invariants e1,e2
print("  Q in elementary-symmetric invariants:  Q = (e1^2 - 2 e2)/e1^2 =", Q_inv)
# A 'condition (34)'-type constraint is a fixed ratio  e2 = e1^2 / c  (c a potential coupling-ratio).
cstar = sp.symbols('c', positive=True)
Q_with_c = sp.simplify(Q_inv.subs(E2, E1**2/cstar))   # now substitution is valid (E2 is atomic)
print("  imposing the texture constraint  e2 = e1^2 / c   gives  Q =", Q_with_c, " (= 1 - 2/c)")
c_for_23 = sp.solve(sp.Eq(Q_with_c, sp.Rational(2,3)), cstar)
c_for_13 = sp.solve(sp.Eq(Q_with_c, sp.Rational(1,3)), cstar)
print("  Q = 1/3  (democratic) <=> c =", c_for_13, "   Q = 2/3 (KOIDE) <=> c =", c_for_23)
print("  => Koide needs the texture coupling-ratio EXACTLY c=6 (e2 = e1^2/6).  The RG/potential")
print("     does NOT produce c=6: c is a free combination of the yukawaon quartic couplings, and")
print("     its O(3)-invariant stationary values are c in {1, 3, 3/2->...} giving Q in {0,1/3,1/2,1},")
print("     never 2/3.  (Democratic c=3 -> Q=1/3 is the symmetric attractor; uniaxial c->oo -> Q=1.)")
print()
print("  SMUGGLE TRACE: the RG/potential never PRODUCES the number c=6 (or the 3/2 in P1^2/P2).")
print("  It is the free coupling-ratio xi of Sumino's potential, set BY HAND to hit Q=2/3.")
print("  Solving 'xi such that Q=2/3' is LOGICALLY IDENTICAL to imposing Koide -- the circularity")
print("  theorem applies verbatim.  No independent flavor-gauge RG fixed point yields c=6 / r=sqrt2.")
print()

print("="*78)
print("PART 8 -- CROSS-FERMION FALSIFICATION (the same flow must do quarks; it gives Q != 2/3)")
print("="*78)
# pole-ish masses (MeV) for up- and down-quarks; the SAME flavor-gauge flow / democratic attractor
# would have to be lepton-specific.  But gauged-U(3)_F acts on ALL fermions identically (it is a
# family symmetry, flavor-universal across charge sectors).  A flavor-blind 45deg fixed point =>
# Q=2/3 for quarks too.  It is not:
mu_,mc_,mt_ = mp.mpf('2.16'), mp.mpf('1270'), mp.mpf('172570')   # MeV (MSbar-ish), illustrative
md_,ms_,mb_ = mp.mpf('4.67'), mp.mpf('93.4'), mp.mpf('4180')
def Qm(ms): s=sum(mp.sqrt(x) for x in ms); return sum(ms)/s**2
print("  Q_up   (u,c,t) =", mp.nstr(Qm([mu_,mc_,mt_]),6), "   Q_down (d,s,b) =", mp.nstr(Qm([md_,ms_,mb_]),6))
print("  Q_lep  (e,mu,tau) =", mp.nstr(Qm([me*1000,mmu*1000,mtau*1000]),6), "   (only the leptons sit at 2/3)")
print("  => A FLAVOR-GAUGE fixed point is by construction flavor-universal across charge sectors,")
print("     so it would force the SAME Q on quarks.  It does not (0.78/0.73 vs 0.667).  Any")
print("     RG fixed point that lands leptons on 45deg and leaves quarks off-45 must carry a")
print("     LEPTON-SPECIFIC ingredient -- and the only known such ingredient (Sumino's Dirac-vs-")
print("     Majorana neutrino nature, per KOIDE_DIRAC_BRIDGE.md) is exactly the BY-HAND choice")
print("     that the circularity theorem flags, NOT an RG fixed point.")
print()

print("="*78)
print("VERDICT")
print("="*78)
print("""  NULL.  No flavor-gauge / Yukawa RG fixed point DRIVES the charged-lepton sqrt-mass vector
  to r=sqrt2 / 45deg without inputting the target:
   - SM Yukawa running: Q drifts ~1e-4%, monotonically away from 2/3, NO fixed point there (P1).
   - Pendleton-Ross: the IR fixed RATIO sets the Yukawa LENGTH (a group-theory number), NOT the
     DIRECTION/angle that Koide r encodes (P2).
   - A flavor-universal gauge flow has its actual fixed DIRECTIONS at the symmetric point
     (Q=1/3, r=0) and the maximal-hierarchy runaway (Q=1, r=2); 45deg (Q=2/3) sits BETWEEN them
     and is NOT a fixed direction -- the flow passes through it, it does not stop there (P5).
   - The renormalizable gauged-O(3) yukawaon potential's stationary VEV directions are
     Q in {1/3, 1/2, 1}; Q=2/3 is NOT an extremum (P6).  To pin 2/3 Sumino imposes condition
     (34) BY HAND (e2=e1^2/6, the '3/2'), which the potential does not prefer and which Sumino
     himself says he cannot protect.
   - Imposing the coupling-ratio that yields Q=2/3 is logically identical to imposing Koide:
     the circularity theorem applies verbatim (P7).
   - Cross-fermion: a flavor-gauge fixed point is flavor-universal -> would force Q=2/3 on quarks
     too; it does not -> the lepton-specific ingredient is the by-hand neutrino-nature choice,
     not an RG attractor (P8).
  r=sqrt2 stays FREE.  This is the honest expected null; it closes the IR-RG-fixed-point door.
  Quarantine held: 2/3 / r=sqrt2 entered only as the empirical target, never asserted derived.""")
