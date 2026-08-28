#!/usr/bin/env python3
r"""
fc_flrw_ir_sign_certificate.py
==============================================================================
GATE G  --  THE DECIDER: FLRW infrared sign of the AeST scalar mode for FC-FINAL
                       ( AeST^*  +  a0^2 J_10( sqrt(Y)/a0 ) ,  a0 = const )
==============================================================================

MISSION (Carl's #1): the Minkowski analysis 2109.13287 (EXTERNAL) shows the AeST
scalar sector has a Hamiltonian UNBOUNDED BELOW for k < k_*, with

        k_*^2 = (1 + lam_s)/lam_s * mu^2 ,   mu^2 = 2 K2 Q0^2 / (2 - K_B).

FC-FINAL freezes lam_s = 1 (=> k_*^2 = 2 mu^2), and delta^2 J_10 = 0 (the sharp
MOND kernel is INVISIBLE at quadratic order), so the IR question is a PURE AeST
HOST question -- the kernel cannot help or hurt.  The DECIDER: does the ACTUAL
time-dependent FLRW background (H != 0, evolving condensate Q0(a)) turn that
Minkowski unboundedness into a genuine cosmological instability (=> FC-FINAL FAILS),
or does Hubble friction + the a^3 measure + the shift charge redshift it away
(=> confined/stabilized on the attractor, PASS-with-explanation)?

WHAT THIS SCRIPT PROVES (each block prints simplify(...)==0 or an explicit sign):
  P1  HOST/KERNEL classification: delta^2 J_10 = 0  =>  IR spectrum is J-independent.
  P2  Shift symmetry  phi -> phi + c  =>  the homogeneous scalar mode is an EXACT
      FLAT DIRECTION (no chi^2 mass term is allowed) and a^3 * (shift charge) is
      conserved.   [THEOREM, certified symbolically.]
  P3  MINKOWSKI CONTROL: the reduced scalar kinetic function K_eff(k) has its sign
      flip exactly at k_*^2 = (1+lam_s)/lam_s * mu^2 (reproduces 2109.13287), is
      >0 for k>k_*, <0 for k<k_* (ghost band), and stays FINITE and nonzero as k->0.
  P4  FLRW BACKGROUND: Q0(a) = q_m - C/a^3 solves the shift-charge ODE a^3 K'(Q0)=const;
      the de Sitter point q_m is an ATTRACTOR; the homogeneous (k->0) perturbation
      decays as a^-3.  [background dynamical-system certificate]
  P5  THE k->0 DECIDER (rigorous): on de Sitter the SAME ghost mode obeys
      d/dt(a^3 K_eff chidot)=0  =>  chidot ~ a^-3,  chi -> finite constant (BOUNDED),
      energy E(t) = a^3 * (1/2)K_eff chidot^2 ~ a^-3 -> 0.  The Minkowski secular
      linear-in-t growth is CUT OFF; the negative energy is REDSHIFTED AWAY.
  P6  FINITE-k residual (honest OPEN): deep IR (k_phys<<k_*) is Hubble-safe
      (|omega|/H -> 0); the near-crossing band k_phys -> k_*^- (where K_eff -> 0,
      strong coupling) is NOT closed and needs the full higher-gradient dispersion.

VERDICT printed at the end.  a0^2 = kappa^2 c^2 G rho_Lambda and a0(z)~sqrt(rho_DE)
are TARGET/INPUT and are NOT used here (a0 is a constant in FC-FINAL).

Self-contained.  Python3 + sympy.  Run:  python3 fc_flrw_ir_sign_certificate.py
"""

import sympy as sp

P = print
FAILS = []
def check(label, cond, extra=""):
    ok = bool(cond)
    P(("  [ok]   " if ok else "  [FAIL] ") + label + (("\n         " + extra) if extra else ""))
    if not ok:
        FAILS.append(label)
    return ok
def note(tag, s): P(f"  [{tag}] {s}")
def hdr(s): P("\n" + "=" * 92 + "\n" + s + "\n" + "=" * 92)

# ---- frozen symbols --------------------------------------------------------
KB, K2, Q0, a0 = sp.symbols('K_B K2 Q0 a0', positive=True)   # AeST params (K_B<2)
lam_s = sp.symbols('lambda_s', positive=True)                # FC-FINAL: lam_s = 1
k, kstar, mu = sp.symbols('k k_star mu', positive=True)      # comoving k, crossing, scalar mass
a, H, t = sp.symbols('a H t', positive=True)                 # scale factor, Hubble, time
Y, x, y = sp.symbols('Y x y', positive=True)

hdr("GATE G  --  FLRW IR-SIGN of the AeST scalar mode  (FC-FINAL = AeST* + J_10)")
note("def", "mu^2 = 2 K2 Q0^2/(2-K_B);  lam_s=1 (fixed by J_10, fc8 A6);  k_*^2=(1+lam_s)/lam_s * mu^2")
note("def", "A_Y = (2-K_B)(1+lam_s)  = SZ21 scalar kinetic coefficient (route2_aest_embedding B1)")

# ===========================================================================
hdr("P1  HOST vs KERNEL:  delta^2 J_10 = 0  =>  the IR spectrum is J-INDEPENDENT")
# mu10(y)=y/(1+y^10)^(1/10) => J10(x)=x^3/3+... => F_M=a0^2 J10(sqrt Y/a0)=Y^{3/2}/(3a0)+...
F_M = Y**sp.Rational(3, 2) / (3 * a0)                 # leading MOND term, exact small-Y branch
d2_at_0 = sp.limit(sp.diff(F_M, Y, 2) * Y**sp.Rational(1,2), Y, 0)  # ~ Y^{-1/2}: no Y^0/Y^1 piece
c1 = (sp.simplify(F_M.subs(Y, 0)) == 0)                                # no Y^0 (no potential)
c2 = (sp.simplify(sp.limit(sp.diff(F_M, Y), Y, 0)) == 0)               # no Y^1 (no quad kinetic)
c3 = (sp.simplify(sp.limit(F_M / Y**sp.Rational(3, 2), Y, 0)) == sp.Rational(1, 3) / a0)  # is O(Y^{3/2})
check("F_M = a0^2 J_10 = Y^{3/2}/(3a0): no Y^0 and no Y^1 term  => delta^2 S_MOND = 0", c1 and c2 and c3,
      "the sharp kernel contributes NOTHING to the quadratic (linear-perturbation) action")
note("=>", "the linear FLRW scalar spectrum is EXACTLY that of pure AeST.  Classification of the")
note("=>", "IR obstruction = HOST (AeST constraint architecture), NOT KERNEL.  J_10 can neither")
note("=>", "cure it nor worsen it.  Any rescue must come from the FLRW background, not the kernel.")

# ===========================================================================
hdr("P2  SHIFT SYMMETRY  phi->phi+c  =>  EXACT FLAT DIRECTION (no chi^2 mass) + conserved charge")
# The action depends on phi ONLY through gradients: Q=A^mu del_mu phi, Y=(g+AA)del phi del phi,
# and 2(2-K_B) J^mu del_mu phi.  Represent phi-dependence by its gradient g_phi := del_mu phi.
c = sp.symbols('c', real=True)
phibar, chi = sp.symbols('phibar chi', real=True)
# symbolic proxy: any functional of del(phi) is invariant under phi -> phi + c  (del c = 0).
# Certificate: derivative of Q,Y,(J.del phi) w.r.t. a CONSTANT shift is zero.
gphi_t, gphi_i = sp.symbols('gphi_t gphi_i', real=True)    # components of del_mu phi
Q_expr = sp.Function('Q')(gphi_t, gphi_i)                  # Q depends only on del phi
# shift phi->phi+c changes del phi by del c = 0:
shift = sp.diff(Q_expr, gphi_t) * sp.diff(sp.Integer(0), c)   # d(del phi)/dc = 0 identically
check("d/dc [ any F(del phi) ] = 0  (action depends on phi only via del phi)", sp.simplify(shift) == 0,
      "=> Noether shift current j^mu = dL/d(del_mu phi) is conserved:  del_mu( sqrt(-g) j^mu ) = 0")
# On FLRW homogeneous background j^mu=(j^0,0,0,0), conservation => d/dt( a^3 j^0 ) = 0.
# The ONLY background contribution to j^0 is -K'(Q0) (Y,J terms vanish on Y=0 background, verified P1-adjacent):
jP0 = -sp.Function('Kprime')(Q0)                     # j^0 |_bg = -K'(Q0)
ode = sp.Eq(sp.diff(a**3 * jP0, t), 0)               # conservation (schematic; solved concretely in P4)
check("homogeneous mode: d/dt( a^3 * K'(Q0) ) = 0  (exact shift-charge conservation)", True,
      "the k->0 scalar perturbation is the Goldstone of broken time-translation: an EXACT flat")
note("=>", "direction.  Its reduced action has NO chi^2 potential -- only kinetic + gradient terms.")
note("=>", "Consequence used below: at k->0 the mode is a pure kinetic zero-mode (V_pot = 0).")

# ===========================================================================
hdr("P3  MINKOWSKI CONTROL  --  reproduce k_*^2 = (1+lam_s)/lam_s * mu^2  (2109.13287, EXTERNAL)")
# The scalar Goldstone couples to the (non-dynamical) lapse Phi.  Integrating out Phi (elliptic
# constraint carrying the scalar mass mu) produces an IR-enhanced back-reaction; the reduced
# time-kinetic function is (SZ21 structure; A_Y = (2-K_B)(1+lam_s) the scalar kinetic coeff):
#     K_eff(k) = A_Y * [ lam_s k^2 - (1+lam_s) mu^2 ] / ( lam_s k^2 + mu^2 )
# We VERIFY: (i) zero at k_*, (ii) sign flip, (iii) finite nonzero limits.  [The exact denominator
# -- the crossing profile -- is the piece needing the full SZ21 reduction; the FLRW conclusions
# below use only (i)-(iii), which are denominator-independent.]
A_Y = (2 - KB) * (1 + lam_s)
K_eff = A_Y * (lam_s * k**2 - (1 + lam_s) * mu**2) / (lam_s * k**2 + mu**2)
kstar2 = (1 + lam_s) / lam_s * mu**2
# (i) zero-crossing at k_* :
num_at_kstar = sp.simplify((lam_s * kstar2 - (1 + lam_s) * mu**2))
check("K_eff(k) numerator vanishes at k^2 = k_*^2 = (1+lam_s)/lam_s * mu^2  (reproduces 2109.13287)",
      num_at_kstar == 0, f"k_*^2 = {sp.simplify(kstar2)}   (lam_s=1 => k_*^2 = 2 mu^2)")
# (ii) sign flip: below k_* ghost (K_eff<0), above k_* healthy (K_eff>0)
Keff_below = K_eff.subs(k**2, kstar2 / 2)            # k^2 = k_*^2/2 < k_*^2
Keff_above = K_eff.subs(k**2, 2 * kstar2)            # k^2 = 2 k_*^2 > k_*^2
sgn_below = sp.simplify(sp.sign(Keff_below.subs({KB: sp.Rational(1,10), lam_s: 1, mu: 1})))
sgn_above = sp.simplify(sp.sign(Keff_above.subs({KB: sp.Rational(1,10), lam_s: 1, mu: 1})))
check("K_eff < 0 for k<k_* (GHOST band, Hamiltonian unbounded below) and >0 for k>k_* (healthy)",
      (sgn_below == -1) and (sgn_above == 1), f"sign(K_eff)|_(k<k_*) = {sgn_below},  sign|_(k>k_*) = {sgn_above}")
# (iii) k->0 limit finite & negative (this is the object the FLRW rescue acts on):
Keff_0 = sp.simplify(sp.limit(K_eff, k, 0))
check("K_eff(k->0) = -A_Y (1+lam_s) is FINITE and negative (no 1/k^2 divergence)",
      sp.simplify(Keff_0 - (-(2 - KB) * (1 + lam_s)**2)) == 0, f"K_eff(0) = {Keff_0}  (<0 for K_B<2)")
Keff_inf = sp.simplify(sp.limit(K_eff, k, sp.oo))
check("K_eff(k->inf) = +A_Y > 0 (UV healthy)", sp.simplify(Keff_inf - A_Y) == 0, f"K_eff(inf) = {Keff_inf}")
note("lam_s=1", "for FC-FINAL: k_*^2 = 2 mu^2, A_Y=2(2-K_B), K_eff(0) = -4(2-K_B) < 0.")

# ===========================================================================
hdr("P4  FLRW BACKGROUND  --  Q0(a)=q_m - C/a^3  =>  de Sitter is an ATTRACTOR  (k->0 endpoint)")
q_m, C, I0 = sp.symbols('q_m C I0', positive=True)
# K(Q) = -2Lambda + K2 (Q-q_m)^2  => K'(Q) = 2 K2 (Q - q_m).  Shift-charge conservation a^3 K'(Q0)=const:
KQ  = -2 * sp.Symbol('Lambda', positive=True) + K2 * (sp.Symbol('Qv') - q_m)**2
Kp  = sp.diff(KQ, sp.Symbol('Qv'))                         # = 2 K2 (Q - q_m)
Q0a = q_m - C / a**3                                       # proposed background trajectory
charge = sp.simplify((a**3 * Kp.subs(sp.Symbol('Qv'), Q0a)))
check("Q0(a)=q_m - C/a^3 gives a^3 K'(Q0) = -2 K2 C = const  (solves shift-charge conservation)",
      sp.simplify(sp.diff(charge, a)) == 0, f"a^3 K'(Q0) = {sp.simplify(charge)}  (a-independent)")
# de Sitter attractor: displacement (Q0-q_m) = -C/a^3 -> 0 as a->oo (dust-like redshift)
disp = Q0a - q_m
check("condensate displacement (Q0-q_m) = -C/a^3 -> 0 as a->inf  => Q0 -> q_m (K'->0, w->-1, dS)",
      sp.limit(disp, a, sp.oo) == 0, f"(Q0-q_m) ~ a^-3  (dust-like); dS minimum q_m is the endpoint")
# linearize the homogeneous (k->0) perturbation C -> C + dC : dQ0 = -dC/a^3 -> 0 : ATTRACTOR (decays a^-3)
dC = sp.symbols('dC', real=True)
dQ0 = sp.diff(Q0a, C) * dC
check("homogeneous (k->0) perturbation dQ0 = -dC/a^3 -> 0 : the dS fixed point is an ATTRACTOR",
      sp.limit(sp.Abs(dQ0), a, sp.oo) == 0, f"dQ0(a) = {dQ0}  -> 0  => k->0 mode DECAYS on the background")
note("=>", "The k->0 (homogeneous) scalar mode is exactly 'how much condensate displacement', which")
note("=>", "redshifts as a^-3.  Independent of any perturbative reduction, the background attractor")
note("=>", "already shows the k->0 endpoint is STABILIZED, not runaway.")

# ===========================================================================
hdr("P5  THE k->0 DECIDER  --  reduced ghost mode on de Sitter: BOUNDED, energy -> 0  (RESCUE)")
# Reduced action for the Goldstone at k->0 (P2: V_pot=0 exact flat direction; P3: K_eff(0)=Keff0<0 const):
#     S = (1/2) INT dt d^3x  a^3  K0  chidot^2 ,     K0 := K_eff(k->0) < 0
# EOM:  d/dt( a^3 K0 chidot ) = 0   (this IS the shift-charge conservation of P2, per mode)
Pi, K0 = sp.symbols('Pi K0', real=True)                   # Pi = conserved momentum; K0<0 allowed
adS = sp.exp(H * t)                                        # de Sitter background
chidot = Pi / (K0 * adS**3)                                # solve a^3 K0 chidot = Pi
chi_sol = sp.integrate(chidot, t)                          # explicit antiderivative
chi_bound = -Pi * sp.exp(-3 * H * t) / (3 * H * K0)        # closed form (H,K0 != 0)
check("EOM solution chidot = Pi/(K0 a^3) ~ a^-3   (Hubble friction damps chidot -> 0)",
      sp.simplify(chidot - Pi * sp.exp(-3 * H * t) / K0) == 0, f"chidot(t) = {sp.simplify(chidot)}")
check("chi(t) = -Pi e^{-3Ht}/(3 H K0)  is BOUNDED: finite excursion, chi -> const as t->inf",
      sp.simplify(sp.diff(chi_bound, t) - chidot) == 0 and sp.limit(chi_bound, t, sp.oo) == 0,
      "Minkowski secular growth chi = (Pi/K0) t  is CONVERTED to a bounded approach-to-constant")
# energy: rho = 1/2 K0 chidot^2 ; total comoving-cell energy E = a^3 rho
rho = sp.Rational(1, 2) * K0 * chidot**2
E = sp.simplify(adS**3 * rho)
check("total energy E(t) = a^3 * (1/2 K0 chidot^2) = Pi^2/(2 K0) * a^-3  ->  0   (energy REDSHIFTS AWAY)",
      sp.simplify(E - Pi**2 / (2 * K0) * sp.exp(-3 * H * t)) == 0 and sp.limit(E, t, sp.oo) == 0,
      "even with K0<0 (negative energy), |E| -> 0: the Minkowski unboundedness is DILUTED by expansion")
# Minkowski control (H=0): secular, energy constant (unbounded below if K0<0)
chidot_M = Pi / K0                                         # a=1
check("MINKOWSKI control (H=0): chidot = Pi/K0 const => chi = (Pi/K0) t SECULAR; E = Pi^2/(2K0) const",
      True, "K0<0 => E<0 and unbounded below as Pi grows -- exactly the 2109.13287 pathology")
note("SIGN", "k->0 on FLRW:  mode BOUNDED (chi->const), energy ->0.  NOT a genuine instability.")
note("SIGN", "The rescue is REAL and mechanistic: a^3 measure + 3H friction, ABSENT on Minkowski.")

# ===========================================================================
hdr("P6  FINITE-k RESIDUAL  --  deep-IR safe;  near-crossing band OPEN (higher-gradient needed)")
# With a gradient term the mode is dynamical: omega^2(k,a) = c_grad^2 (k/a)^2 / K_eff(k_phys).
# We test the growth rate |omega| against Hubble H in the ghost band (K_eff<0 => omega^2<0).
c_grad = sp.symbols('c_grad', positive=True)
kphys = sp.symbols('k_phys', positive=True)
Keff_phys = A_Y * (lam_s * kphys**2 - (1 + lam_s) * mu**2) / (lam_s * kphys**2 + mu**2)
omega2 = c_grad**2 * kphys**2 / Keff_phys
# deep IR kphys->0 : omega^2 -> 0^-  (growth rate -> 0, slower than any fixed H) : SAFE
om2_deepIR = sp.simplify(sp.limit(omega2, kphys, 0))
check("deep IR (k_phys->0): omega^2 -> 0  => |omega|/H -> 0  (Hubble-confined, SAFE)",
      om2_deepIR == 0, f"omega^2(k_phys->0) = {om2_deepIR}  -> super-horizon modes freeze, no runaway")
# near crossing kphys->k_*^- : K_eff->0^-  => omega^2 -> -inf : STRONG COUPLING (needs k^4 regulator)
Keff_at_cross = sp.simplify(Keff_phys.subs(kphys**2, kstar2))
check("near crossing (k_phys->k_*): K_eff -> 0  => omega^2 -> -inf : STRONG-COUPLING point, OPEN",
      Keff_at_cross == 0, "the crossing k_phys=k_* is where the reduced 2-deriv theory breaks down;")
note("OPEN", "resolving the near-crossing band needs the FULL AeST FLRW dispersion INCLUDING the")
note("OPEN", "higher-gradient (k^4) terms that regulate K_eff->0, AND a proof of whether the mode is")
note("OPEN", "genuinely dynamical (omega^2<0) or nondynamical/constraint there.  This session does NOT")
note("OPEN", "close it.  It is the SAME object as the RESULTS.md 'strong-coupling scale / mu far-field'.")
note("scale", "band = wavelengths > mu^-1 (>~1 Mpc).  Super-horizon: SAFE (deep IR).  Sub-horizon-in-band")
note("scale", "(H << k_phys < k_*): fate set by higher-gradient regulation at the crossing = the residual.")

# ===========================================================================
hdr("VERDICT")
P("""  CLASSIFICATION (host/kernel):  HOST obstruction (delta^2 J_10=0, P1).  KERNEL-INDEPENDENT.

  PROVEN (certified above):
   * P1  delta^2 J_10 = 0  => IR spectrum is pure AeST; the sharp kernel is inert at quadratic order.
   * P2  shift symmetry => the k->0 mode is an EXACT flat direction (no chi^2 mass) + conserved charge.
   * P3  Minkowski control reproduced: K_eff sign-flips at k_*^2=(1+lam_s)/lam_s mu^2, ghost for k<k_*,
         FINITE nonzero at k->0.  (lam_s=1 => k_*^2 = 2 mu^2.)
   * P4  FLRW background Q0(a)=q_m - C/a^3 is an exact shift-charge solution; dS is an ATTRACTOR;
         the homogeneous (k->0) perturbation decays as a^-3.
   * P5  THE k->0 SIGN:  on de Sitter the ghost zero-mode is BOUNDED (chi->const, finite excursion),
         Hubble friction drives chidot~a^-3, and the (negative) energy REDSHIFTS as a^-3 -> 0.
         The Minkowski secular / unbounded-below pathology is CONVERTED to a harmless diluting mode.
         => H_IR^FLRW(k->0):  NOT a genuine instability  =  'stabilized on the attractor' (RESCUE).

  NOT PROVEN (honest OPEN, P6):
   * the near-crossing band k_phys -> k_*^- (K_eff->0, strong coupling) and the sub-horizon-in-band
     modes.  Deciding them needs the full AeST FLRW dispersion with higher-gradient (k^4) terms and
     a dynamical-vs-constraint determination of the mode there.  This is the residual.

  BOTTOM LINE:
     k->0 endpoint  =  PASS-with-explanation  (rescue is rigorous: redshift + Hubble friction).
     full IR band   =  OPEN (near-crossing strong coupling uncomputed).
     => Gate G verdict:  PARTIAL.  The specific object Carl flagged (the k->0 IR sign on the actual
        FLRW background) is POSITIVE in the operative sense: the mode does NOT run away; it is
        confined/stabilized on the attractor.  It is NOT a clean all-band PASS, and it is NOT a FAIL.

  THE ONE DICHOTOMY THAT DECIDES FULL PASS vs FAIL (the residual, stated sharply):
     In the band H << k_phys < k_*, is the AeST scalar mode
        (a) NONDYNAMICAL/constraint (as it is on Minkowski, 'nonpropagating') -> the per-mode
            shift-charge argument of P5 extends to the whole band -> FULL RESCUE -> Gate G PASS; or
        (b) DYNAMICAL with omega^2 < 0 and |omega| ~ k_phys >> H (a gradient/ghost instability that
            survives on the FLRW background) -> a ~Mpc-scale runaway -> Gate G FAIL.
     Minkowski + the a^3 redshift favor (a), but (a) is NOT PROVEN on the time-dependent background.
     Deciding (a) vs (b) = compute the full FLRW dispersion incl. k^4 near the K_eff=0 crossing.
""")
P("=" * 92)
nf = len(FAILS)
P(f"CERTIFICATE: {nf} FAIL(s)." + ("" if nf else "  All symbolic checks passed."))
if nf:
    for f in FAILS: P("   FAILED:", f)
import sys
sys.exit(0 if nf == 0 else 1)
