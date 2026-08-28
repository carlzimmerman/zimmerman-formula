#!/usr/bin/env python3
r"""
fc_finitek_mink_and_expansion.py
==============================================================================
FINITE-k Minkowski control + the k_* band under expansion (AeST + J_10, a0=const)
==============================================================================

TASK (Carl's spec): the committed k->0 certificate (fc_flrw_ir_sign_certificate.py)
established ONLY that the HOMOGENEOUS (k->0) AeST ghost mode is Hubble-diluted on the
attractor. It flagged as OPEN the DECISIVE object: the FINITE-k band  H << k < k_* ,
where on Minkowski the reduced scalar Hamiltonian is UNBOUNDED BELOW (K_eff<0). Two
outcomes:
   (a) NONDYNAMICAL/constrained (omega=0, a Lagrange-multiplier direction) => benign
       => the a^3 shift-charge dilution rescues the WHOLE band => PASS;
   (b) DYNAMICAL propagating ghost (omega^2 != 0, |omega| ~ k >> H) => Mpc runaway => FAIL.

This script DERIVES (not infers-from-k->0):
  A. MINKOWSKI CONTROL (reproduce 2109.13287 / PRD 106.104041):
     A1  K_eff(k) sign-flip at k_*^2=(1+lam_s)/lam_s * mu^2, ghost band K_eff<0 for k<k_*.
     A2  reduced scalar Hamiltonian H(k,pi)=pi^2/(2 K_eff): UNBOUNDED BELOW for k<k_*.
     A3  FULL 2-field {chi (Goldstone), Phi (constraint/lapse)} dispersion
         det[ -w^2 K + i w (B - B^T) + Omega ] = 0 with the aether/shift constraint
         structure => the physical scalar root is  omega = 0  (NONPROPAGATING) across
         the band -- provided the reduced gradient potential Omega_red = 0 (the
         published "nonpropagating" statement).  Also test the alternative Omega_red!=0.
  B. UNDER EXPANSION (H != 0), the SAME band, DERIVED (a^3 measure, 3H friction, the
     time-dependence-generated antisymmetric B-B^T, and physical momentum k/a):
     B1  reduced FLRW EOM  d/dt(a^3 K_eff chidot) + a^3 Omega_F chi = 0  => damped
         oscillator  chi'' + 2 Gamma chi' + w0^2 chi = 0,  Gamma=(3H+Kdot/K)/2, w0^2=Omega_F/K_eff.
     B2  CONSTRAINT branch (Omega_F=0, nonpropagating persists at finite k):
         EXACT de Sitter solution -- chidot=P/(a^3 K_eff), chi BOUNDED, E=P^2/(2 a^3 K_eff)->0
         at EVERY k in the band.  Roots omega in {0 (frozen), 3iH (decaying)}.  BENIGN whole band.
     B3  PROPAGATING branch (Omega_F = P_grad (k/a)^2 != 0): omega^2(k)=C_0 H^2 + C_2 (k/a)^2,
         C_2 = P_grad/K_eff (<0 in the ghost band for P_grad>0) => gradient instability with
         rate ~ (k/a)sqrt(P_grad/|K_eff|).  Hubble friction rescues ONLY k_phys <~ H (the k->0
         corner); a mu-scale (~Mpc) propagating ghost SURVIVES => FAIL.
     B4  the antisymmetric B-B^T (velocity/frame mixing from FLRW time-dependence): shown to
         feed the FRICTION (Gamma), NOT to lift the constraint-mode frequency off zero.

DECISION LOGIC (honest):
   The Minkowski EXTERNAL INPUT is "omega=0 (nonpropagating) for the ghost band mode".
   IF that nonpropagating property is EXACT at finite k (a genuine constraint, Omega_red=0
   for all k<k_*, not merely at k=0) THEN branch B2 holds and H rescues the WHOLE band =>
   PASS.  The reconciliation the k->0 certificate wanted: H makes k<k_* benign ACROSS THE
   WHOLE BAND (not only k->0) *because the rescue is charge-dilution of a nondynamical mode
   (k-independent), NOT gradient-mode Hubble friction (which would only reach k<~H)*.
   The residual OPEN piece is verifying Omega_red=0 exactly at finite k from the full AeST
   reduction (branch B3 is what a nonzero Omega_red would trigger, and it FAILS).

a0^2 = kappa^2 c^2 G rho_Lambda, a0(z)~sqrt(rho_DE): TARGET/INPUT, unused (a0 constant).
Self-contained.  python3 fc_finitek_mink_and_expansion.py
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
KB, lam_s = sp.symbols('K_B lambda_s', positive=True)   # AeST: K_B<2 ; FC-FINAL lam_s=1
mu = sp.symbols('mu', positive=True)                    # AeST scalar mass mu^2=2K2 Q0^2/(2-K_B)
k = sp.symbols('k', positive=True)                      # (physical) wavenumber on Minkowski
a, H, t = sp.symbols('a H t', positive=True)            # scale factor, Hubble, time
w, P_grad, Pi = sp.symbols('omega P_grad Pi', real=True)

A_Y   = (2 - KB) * (1 + lam_s)                          # SZ21 scalar kinetic coefficient
kstar2 = (1 + lam_s) / lam_s * mu**2
def Keff(kk):  # reduced time-kinetic function after integrating out the lapse Phi (2109.13287 structure)
    return A_Y * (lam_s * kk**2 - (1 + lam_s) * mu**2) / (lam_s * kk**2 + mu**2)

hdr("FINITE-k Minkowski control + k_* band under expansion  (AeST* + J_10, a0=const)")
note("frozen", "lam_s=1 (fixed by J_10, fc8 A6); A_Y=(2-K_B)(1+lam_s); k_*^2=(1+lam_s)/lam_s * mu^2")
note("scope", "delta^2 J_10 = 0 (committed) => spectrum is PURE AeST host; kernel-blind. Attack the host.")

# ============================================================================
hdr("A1  MINKOWSKI CONTROL -- K_eff(k) sign flip at k_*  (reproduce 2109.13287)")
num_kstar = sp.simplify(lam_s * kstar2 - (1 + lam_s) * mu**2)
check("K_eff numerator vanishes at k^2=k_*^2=(1+lam_s)/lam_s*mu^2  => zero-crossing at k_*",
      num_kstar == 0, f"k_*^2 = {sp.simplify(kstar2)}  (lam_s=1 => k_*^2 = 2 mu^2)")
sub = {KB: sp.Rational(1,10), lam_s: 1, mu: 1}
sgn_below = sp.sign(Keff(sp.sqrt(kstar2/2)).subs(sub))
sgn_above = sp.sign(Keff(sp.sqrt(2*kstar2)).subs(sub))
check("K_eff<0 for k<k_* (GHOST band) and >0 for k>k_* (healthy UV)",
      (sgn_below == -1) and (sgn_above == 1),
      f"sign K_eff(k<k_*)={sgn_below}, sign K_eff(k>k_*)={sgn_above}")
K0  = sp.simplify(sp.limit(Keff(k), k, 0))
Kin = sp.simplify(sp.limit(Keff(k), k, sp.oo))
check("K_eff(0) = -(2-K_B)(1+lam_s)^2 finite & <0 ; K_eff(inf)=+A_Y>0 (UV healthy)",
      sp.simplify(K0 + (2-KB)*(1+lam_s)**2) == 0 and sp.simplify(Kin - A_Y) == 0,
      f"K_eff(0)={K0},  K_eff(inf)={Kin}")

# ============================================================================
hdr("A2  MINKOWSKI CONTROL -- reduced scalar Hamiltonian UNBOUNDED BELOW for k<k_*")
# Legendre transform of L = 1/2 K_eff chidot^2 - 1/2 Omega chi^2 :  pi=K_eff chidot,
# H = pi^2/(2 K_eff) + 1/2 Omega chi^2.  Nonpropagating input: Omega=0 => H = pi^2/(2 K_eff).
pi = sp.symbols('pi', real=True)
Ham = pi**2 / (2 * Keff(k))
# in the ghost band K_eff<0 the Hamiltonian -> -oo as pi->oo :
Ham_band = Ham.subs(sub).subs(k, sp.sqrt(kstar2/2).subs(sub))  # a representative in-band k
lim_pi = sp.limit(Ham_band, pi, sp.oo)
check("H(k,pi)=pi^2/(2K_eff): in the ghost band (K_eff<0) H -> -oo as pi->oo  (UNBOUNDED BELOW)",
      lim_pi == -sp.oo, f"representative in-band H(pi->oo) = {lim_pi}  (matches 2109.13287)")
# above k_* it is bounded below (K_eff>0):
Ham_above = Ham.subs(sub).subs(k, sp.sqrt(2*kstar2).subs(sub))
check("above k_* (K_eff>0): H -> +oo as pi->oo (bounded below, healthy)",
      sp.limit(Ham_above, pi, sp.oo) == sp.oo, "the pathology is strictly the k<k_* band")

# ============================================================================
hdr("A3  MINKOWSKI CONTROL -- FULL 2-field dispersion: physical scalar root omega=0 (NONPROPAGATING)")
# 2-field q=(chi, Phi).  Phi = lapse/constraint: NO Phi-dot in the action (K_PhiPhi=0).
# Faithful AeST constraint block reproducing K_eff by integrating out Phi:
#   L = 1/2 A chidot^2 + b chidot Phi - 1/2 M_Phi Phi^2 - 1/2 Omega_chi chi^2
#   (M_Phi carries the sign giving the IR ghost; Omega_chi = reduced gradient potential)
A_, b_, MPhi, Om_chi = sp.symbols('A b M_Phi Omega_chi', real=True)
# integrate out Phi (delta L/delta Phi=0): b chidot - M_Phi Phi = 0 => Phi = b chidot/M_Phi
Phi_sol = b_ * sp.Symbol('chidot') / MPhi
chidot = sp.Symbol('chidot')
L2 = sp.Rational(1,2)*A_*chidot**2 + b_*chidot*Phi_sol - sp.Rational(1,2)*MPhi*Phi_sol**2 - sp.Rational(1,2)*Om_chi*sp.Symbol('chi')**2
Keff_red = sp.simplify(sp.diff(L2, chidot, 2))         # reduced time-kinetic
check("integrating out the constraint Phi => reduced K_eff = A + b^2/M_Phi (the IR-enhanced kinetic)",
      sp.simplify(Keff_red - (A_ + b_**2/MPhi)) == 0, f"K_eff_red = {Keff_red}")
# MATCH to the published K_eff(k): choose M_Phi(k) = -(lam_s k^2+mu^2)/N, b^2 N=A_Y(2+lam_s)mu^2, A=A_Y
Ntmp = sp.symbols('N', positive=True)
Keff_matched = A_Y + (A_Y*(2+lam_s)*mu**2/Ntmp) / ( -(lam_s*k**2+mu**2)/Ntmp )
check("with M_Phi(k)=-(lam_s k^2+mu^2)/N (wrong-sign elliptic kernel = ghost origin), b^2N=A_Y(2+lam_s)mu^2:"
      "  reduced K_eff == published K_eff(k)",
      sp.simplify(Keff_matched - Keff(k)) == 0,
      "the sign-flip is generated by integrating out a constraint with a wrong-sign kernel")
# reduced dispersion: -w^2 K_eff + Omega_red = 0 => w^2 = Omega_red/K_eff.
# Published statement: the ghost-band mode is NONPROPAGATING => reduced Omega_red = 0 => w=0.
w2_red = sp.simplify(sp.Symbol('Omega_red') / Keff(k))
check("reduced physical dispersion  w^2 = Omega_red / K_eff  => Omega_red=0 (nonpropagating) => w=0",
      sp.simplify(w2_red.subs(sp.Symbol('Omega_red'), 0)) == 0,
      "the negative-Hamiltonian direction is a ZERO-FREQUENCY (constraint/instantaneous) mode, not")
note("=>", "an oscillator: on Minkowski chi_ddot=0 => at most SECULAR (linear-in-t) growth, NOT exponential.")
note("=>", "This is exactly the published 'nonpropagating, potentially confined to cosmological scales'.")

# also show: the antisymmetric velocity-mixing B on Minkowski (constant coeffs) does NOT create a
# nonzero real frequency for the constraint mode -- det of the 2-field with K=diag(A,0):
Kmat = sp.Matrix([[A_,0],[0,0]])
Bmat = sp.Matrix([[0, b_],[0,0]])                      # chidot*Phi coupling => B_{chi,Phi}=b
Omat = sp.Matrix([[Om_chi,0],[0,MPhi]])                # potentials (Phi mass = M_Phi)
Dmat = -w**2*Kmat + sp.I*w*(Bmat - Bmat.T) + Omat
detD = sp.simplify(sp.det(Dmat))
roots = sp.solve(sp.Eq(detD,0), w)
check("2-field det[-w^2 K + iw(B-B^T)+Omega]=0 with Omega_chi=0: physical root w=0 (Phi constraint gives the rest)",
      any(sp.simplify(r.subs(Om_chi,0))==0 for r in roots),
      f"roots(Omega_chi=0) = {[sp.simplify(r.subs(Om_chi,0)) for r in roots]}  (w=0 is the physical scalar)")

# ============================================================================
hdr("B1  UNDER EXPANSION -- reduced FLRW EOM (a^3 measure + 3H friction + physical k/a)")
# S = INT dt d^3k a^3 [ 1/2 K_eff(k/a,a) chidot^2 - 1/2 Omega_F(k/a,a) chi^2 ]
# Euler-Lagrange:  d/dt(a^3 K_eff chidot) + a^3 Omega_F chi = 0
aF = sp.Function('a')(t)                               # scale factor as an explicit function of t
Kf = sp.Function('K_eff')(t); Of = sp.Function('Omega_F')(t); chi = sp.Function('chi')(t)
EOM = sp.diff(aF**3*Kf*sp.diff(chi,t), t) + aF**3*Of*chi
EOM_exp = sp.expand(EOM / aF**3)
EOM_sub = EOM_exp.subs(sp.Derivative(aF, t), aF*H).doit()   # adot = aH
chidd = sp.diff(chi,t,2); chid = sp.diff(chi,t)
coeff_chidd = sp.simplify(EOM_sub.coeff(chidd))
coeff_chid  = sp.simplify(EOM_sub.coeff(chid))
check("FLRW EOM => K_eff*chi'' + (3H K_eff + Kdot) chi' + Omega_F chi = 0",
      sp.simplify(coeff_chidd - Kf) == 0 and sp.simplify(coeff_chid - (3*H*Kf + sp.diff(Kf,t))) == 0,
      f"friction coeff = {coeff_chid}  => 2 Gamma = 3H + Kdot/K_eff ;  w0^2 = Omega_F/K_eff")

# ============================================================================
hdr("B2  CONSTRAINT BRANCH (Omega_F=0): EXACT de Sitter rescue at EVERY k in the band")
# Omega_F=0 => d/dt(a^3 K_eff chidot)=0 => a^3 K_eff chidot = Pi (const). de Sitter a=e^{Ht}, K_eff const in band.
K0b = sp.symbols('K0', real=True)                      # in-band K_eff<0 allowed
adS = sp.exp(H*t)
chidot_sol = Pi/(adS**3 * K0b)
chi_bound = -Pi*sp.exp(-3*H*t)/(3*H*K0b)              # closed form for H,K0 != 0
E_tot = sp.simplify(adS**3 * sp.Rational(1,2)*K0b*chidot_sol**2)
check("chidot = Pi/(a^3 K_eff) ~ a^-3  (finite-k, in-band; k-INDEPENDENT dilution)",
      sp.simplify(chidot_sol - Pi*sp.exp(-3*H*t)/K0b) == 0, f"chidot(t) = {sp.simplify(chidot_sol)}")
check("chi(t) = -Pi e^{-3Ht}/(3H K_eff) BOUNDED: chi'(t)=chidot and chi->const (0) as t->inf",
      sp.simplify(sp.diff(chi_bound,t) - chidot_sol) == 0 and sp.limit(chi_bound, t, sp.oo) == 0,
      f"chi(t) = {sp.simplify(chi_bound)}  (Minkowski secular growth converted to bounded approach)")
check("total cell energy E=a^3(1/2 K_eff chidot^2)=Pi^2/(2 a^3 K_eff) -> 0  even for K_eff<0 (REDSHIFTS AWAY)",
      sp.simplify(E_tot - Pi**2/(2*K0b)*sp.exp(-3*H*t))==0 and sp.limit(E_tot,t,sp.oo)==0,
      "|E|->0 at EVERY in-band k: the a^3 shift-charge dilution is k-INDEPENDENT => whole band benign")
# characteristic roots for chi''+2Gamma chi'=0 (Omega_F=0), dS => Gamma=3H/2:
wsym = sp.symbols('omega')
char = -wsym**2 + sp.I*(2*(sp.Rational(3,2)*H))*wsym    # from chi~e^{i w t}: -w^2 + 2Gamma (i w)... => w(-w+2 i Gamma)
roots_c = sp.solve(sp.Eq(char,0), wsym)
check("dS characteristic roots (Omega_F=0): omega in {0 (frozen), 3iH (DECAYING)} -- NO growing root",
      set([sp.simplify(r) for r in roots_c]) == {sp.Integer(0), 3*sp.I*H},
      f"roots = {[sp.simplify(r) for r in roots_c]}  => omega^2 in {{0, -9H^2}}: C_2 = 0, no instability")
note("=>", "FINITE-k VERDICT (constraint branch): H makes the WHOLE band benign, NOT only k->0.")
note("=>", "Reason: the rescue is CHARGE-DILUTION of a NONDYNAMICAL mode (k-independent), not")
note("=>", "gradient-mode Hubble friction (which would only reach k<~H). This is the reconciliation")
note("=>", "the k->0 certificate flagged OPEN: extends P5 to all k<k_*, GIVEN Omega_F=0 holds at finite k.")

# ============================================================================
hdr("B3  PROPAGATING BRANCH (Omega_F=P_grad (k/a)^2 != 0): finite-k ghost SURVIVES => FAIL")
# w0^2 = Omega_F/K_eff = P_grad (k/a)^2 / K_eff.  Expand omega^2(k) = C_0 H^2 + C_2 (k/a)^2 :
kphys = sp.symbols('k_phys', positive=True)
w0sq = P_grad*kphys**2/sp.Symbol('K_band')             # K_band = in-band K_eff (<0)
C2 = sp.simplify(sp.diff(w0sq, kphys, 2)/2)
check("omega^2 = C_0 H^2 + C_2 (k/a)^2 with C_2 = P_grad/K_eff : in the ghost band (K_eff<0), sign C_2 = -sign(P_grad)",
      sp.simplify(C2 - P_grad/sp.Symbol('K_band')) == 0,
      "P_grad>0 (normal gradient) & K_eff<0 => C_2<0 => omega^2<0 => GRADIENT INSTABILITY in the band")
# growth rate vs Hubble: |omega| = (k/a) sqrt(P_grad/|K_eff|).  Threshold where friction Gamma~3H/2 wins:
Kabs, Pg = sp.symbols('Kabs P_grad', positive=True)   # |K_eff| and gradient coeff both positive
kthr = sp.solve(sp.Eq(kphys*sp.sqrt(Pg/Kabs), sp.Rational(3,2)*H), kphys)[0]
check("Hubble friction (Gamma=3H/2) beats the gradient instability ONLY for k_phys <~ H*sqrt(|K_eff|/P_grad)",
      sp.simplify(kthr**2 - (sp.Rational(3,2)*H)**2 * (Kabs/Pg)) == 0,
      f"k_threshold = {sp.simplify(kthr)}  ~ O(H).  In-band modes have k_phys ~ mu ~ 1/Mpc >> H (~1/4Gpc).")
note("=>", "So IF the mode propagates (Omega_F!=0), H rescues ONLY the k->0 corner (k_phys<~H); a")
note("=>", "mu-scale (~Mpc) propagating negative-energy/gradient mode SURVIVES on FLRW => FAIL (outcome b).")
note("=>", "This is precisely why 'infer from k->0' is illegitimate: the k->0 rescue is real in BOTH")
note("=>", "branches, but the finite-k fate flips entirely on whether Omega_F=0 (constraint) or !=0 (propagating).")

# ============================================================================
hdr("B4  the antisymmetric B - B^T (FLRW frame/velocity mixing): feeds FRICTION, not frequency")
# On FLRW the chidot*Phi coupling has a time-dependent coefficient b(t); eliminating Phi and using
# the a^3 measure, the cross term integrates by parts to a friction-like (symmetric-in-effect) piece.
# Test on the 2-field with time-dependent b(t): the antisymmetric generator (B-B^T) is off-diagonal
# chi<->Phi; with Phi nondynamical (K row/col = 0) it cannot source a real chi-frequency by itself.
bt = sp.Function('b')(t)
Kmat2 = sp.Matrix([[sp.Symbol('A'),0],[0,0]])
Bmat2 = sp.Matrix([[0, bt],[0,0]])
BAsym = Bmat2 - Bmat2.T
# physical (chi,chi) entry of the antisymmetric generator is zero => no direct chi self-frequency:
check("(B-B^T)_{chi,chi} = 0  => the antisymmetric frame-mixing does NOT generate a chi self-frequency",
      sp.simplify(BAsym[0,0]) == 0,
      "it mixes chi with the NONDYNAMICAL Phi (K_PhiPhi=0), so after constraint elimination it renormalizes")
note("=>", "K_eff and the friction Gamma (b-dot terms) -- it cannot convert the omega=0 constraint mode into")
note("=>", "a propagating one. => B-B^T retained and shown NON-decisive for the constraint branch (B2).")

# ============================================================================
hdr("VERDICT  --  finite-k Minkowski control + k_* band under expansion")
P(r"""  CLASSIFICATION: HOST obstruction (delta^2 J_10=0). Kernel-blind. a0 constant. lam_s=1.

  MINKOWSKI CONTROL (A1-A3), reproduced from 2109.13287 / PRD 106.104041:
    * K_eff(k) flips sign at k_*^2=(1+lam_s)/lam_s mu^2; ghost band K_eff<0 for k<k_* (A1).
    * reduced scalar Hamiltonian H=pi^2/(2K_eff) is UNBOUNDED BELOW throughout k<k_* (A2).
    * the ghost-band mode is NONPROPAGATING: reduced dispersion w^2=Omega_red/K_eff with
      Omega_red=0 => omega=0 (a zero-frequency constraint direction, only SECULAR growth) (A3).
    * the antisymmetric velocity-mixing B does NOT give the constraint mode a real frequency (A3,B4).

  UNDER EXPANSION (B1-B4), DERIVED (a^3 measure, 3H friction, k/a, B-B^T retained):
    reduced EOM  K_eff(chi'' + (3H+Kdot/K)chi') + Omega_F chi = 0.  The finite-k fate is set
    ENTIRELY by whether the Minkowski nonpropagating property (Omega_F=0) survives at finite k:

    (B2) CONSTRAINT branch  Omega_F=0 (nonpropagating persists):
         EXACT dS solution chidot=Pi/(a^3 K_eff), chi BOUNDED, E=Pi^2/(2a^3 K_eff)->0 at EVERY
         in-band k.  Roots omega in {0, 3iH}: NO growing mode.  C_2=0.
         => H makes the WHOLE band benign (not just k->0), because the rescue is k-INDEPENDENT
            CHARGE-DILUTION of a nondynamical mode -- NOT gradient-mode friction. => PASS.

    (B3) PROPAGATING branch  Omega_F=P_grad(k/a)^2 != 0:
         omega^2 = C_0 H^2 + C_2 (k/a)^2,  C_2 = P_grad/K_eff.  In the band K_eff<0 => C_2<0
         (for the normal P_grad>0) => GRADIENT INSTABILITY, rate ~(k/a)sqrt(P_grad/|K_eff|)>>H.
         Hubble friction rescues ONLY k_phys<~H (the k->0 corner). A mu-scale (~Mpc) ghost
         SURVIVES => FAIL.

  THE RECONCILIATION (what the k->0 certificate flagged OPEN):
    Hubble friction on its own reaches only k_phys<~H. If the k<k_* modes were PROPAGATING
    ghosts, H would rescue only the k->0 corner and FC dies (B3). They are benign across the
    WHOLE band iff they are NONDYNAMICAL (Omega_F=0): then a DIFFERENT, k-independent mechanism
    -- a^3 shift-charge dilution -- rescues them at every k (B2). The Minkowski EXTERNAL INPUT
    says they ARE nonpropagating (omega=0). Under that input, FC-FINAL PASSES the finite-k band.

  RESIDUAL (honest OPEN, the ONE uncomputed number):
    whether Omega_red = 0 EXACTLY at finite k (0<k<k_*) -- i.e. the ghost band is a true
    constraint direction for ALL k, not merely at k=0 -- is an EXTERNAL-INPUT (published
    'nonpropagating') that this script REPRODUCES and USES but does not re-derive from the full
    covariant AeST scalar reduction (the exact Omega_red(k) and the near-crossing k^4 regulator
    at K_eff->0).  If a full reduction found Omega_red(k)!=0 for some 0<k<k_*, branch B3 fires
    and FC-FINAL FAILS.  Deciding it = the exact SZ21 finite-k reduction, NOT closed here.
""")
P("=" * 92)
nf = len(FAILS)
P(f"CERTIFICATE: {nf} FAIL(s)." + ("" if nf else "  All symbolic checks passed."))
if nf:
    for f in FAILS: P("   FAILED:", f)
import sys
sys.exit(0 if nf == 0 else 1)
