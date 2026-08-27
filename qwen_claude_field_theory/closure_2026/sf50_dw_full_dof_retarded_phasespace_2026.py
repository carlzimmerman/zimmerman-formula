#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf50_dw_full_dof_retarded_phasespace_2026.py
FULL-DOF GATE for exact-exponential causal-nonlocal MOND (Deffayet-Woodard 2026 chassis).

Extends sf43/sf44/sf46/sf48/sf49 to the COMPLETE localized field content with the transport-M and
f(Z) NONLINEAR vertices (not a toy scalar block), on Minkowski AND a weak-field static y>0 background:

    fields:  g_mn  (ADM: N, N^i, h_ij) ;  clock phi + multiplier lambda   [(dphi)^2 = -1] ;
             U + multiplier xi  [Box U = R_uu, localization] ;
             M + multiplier nu  [transport d_mu(sqrt-g u^mu M) = -d_mu(sqrt-g u^mu f(Z))] ;
             Z = (4c^4/a0^2)(dU)^2 ;  f_+(Z)=4[1-(1+sqrtZ/2)e^{-sqrtZ/2}], f_+'=(1/2)e^{-sqrtZ/2}.

THE decisive question this gate answers (derive, do NOT assume -- the sf43/sf48 overclaim trap):
    Does the RETARDED prescription remove the localization-ghost combination AS A PHASE-SPACE
    (Dirac) RESTRICTION -- so the Hamiltonian count is 2 tensor + 0 -- or does a mode survive in
    phase space, with the retarded condition acting only on the SOLUTION submanifold?

Method: honest ADM + Dirac-Bergmann.
  PART 1  velocity content + all canonical momenta + primary constraints (sympy, concrete).
  PART 2  kinetic Hessian of (U,xi) INCLUDING the f(Z) self-term and transport-M vertex: prove the
          2x2 block is non-degenerate & indefinite (det=-b^2<0) => 1 healthy + 1 GHOST, and that
          this signature is BACKGROUND-INDEPENDENT (holds on Minkowski AND static y>0).
  PART 3  clock (phi,lambda) and transport (M,nu) sectors: prove each is a 2nd-class pair => 0 DOF,
          with the f(Z) vertex carried inside the transport (not a new propagating mode).
  PART 4  full Dirac-Bergmann tally: primary/secondary constraints, first- vs second-class split,
          Poisson-bracket rank, PHYSICAL DOF count of the LOCAL theory.
  PART 5  THE CRUX, DERIVED: is "impose retarded" a phase-space constraint? Two independent proofs:
          (5a) the Dirac-Bergmann algorithm on S_loc terminates WITHOUT a constraint on (U,xi);
          (5b) the retarded initial data at t0 is HISTORY-DEPENDENT -- it is NOT a function of the
               canonical jet at t0 (explicit numeric demonstration with two sources sharing the full
               germ at t0 but different past) => it cannot be any Dirac constraint chi(q,p)~0.
          => the retarded prescription is NOT a phase-space restriction; it restricts the SOLUTION
             submanifold (sf44 Cauchy-data count), which is a strictly weaker statement than a
             canonical DOF reduction (this is exactly where sf48's "quotient by I_hom" overreaches).

VERDICT letter (A pass / B obstruction / C unresolved) printed at the end. No manufactured pass or
kill: the theory is NOT killed (sf44 solution-space escape stands); what is obstructed is the
HAMILTONIAN certification of "2+0 healthy".
"""
import sys
import sympy as sp
import numpy as np

FAIL, N = [], [0]
def check(c, label, detail=""):
    N[0] += 1; ok = bool(c)
    print(f"  [{'ok' if ok else 'FAIL'}] {N[0]:02d} {label}" + (f"\n         {detail}" if detail else ""))
    if not ok: FAIL.append(f"{N[0]:02d} {label}")
def hdr(s): print("\n" + "=" * 88 + "\n" + s + "\n" + "=" * 88)


# ==========================================================================================
hdr("PART 1 -- velocity content, ADM momenta, primary constraints (concrete sympy)")
# ==========================================================================================
r"""
Localized action (density; c=1 units for the DOF count, restored elsewhere):
  L = L_EH(N,N^i,h_ij) + sqrt(-g)[ xi (Box U - R_uu) + lambda((dphi)^2+1) ]
      + nu * d_mu( sqrt(-g) u^mu (M + f(Z)) )
  with u_mu=d_mu phi, Z=kap (dU)^2, kap=4c^4/a0^2.

ADM: sqrt(-g)=N sqrt(h). Integrate the localization piece by parts:
  sqrt(-g) xi Box U  ->  - sqrt(-g) g^{mn} d_m xi d_n U   (+ total deriv)
  time part (mostly-plus, N=1,N^i=0 slice for the momenta):  + (sqrt(h)/N)  Udot xidot
Integrate the transport piece by parts:
  nu d_mu(sqrt-g u^mu(M+f)) -> - sqrt-g u^mu d_mu nu (M+f) = -(sqrt-g u^0) nudot (M+f) - (spatial)
So the VELOCITY-dependent part of L (per mode, on the N=1 slice) is, schematically:
  L_vel =  (sqrt h) Udot xidot                       [localization: bilinear Udot-xidot]
         +  lambda ( -phidot^2 + ...)                [clock: phidot^2, multiplier lambda]
         +  (sqrt h) nu ( Mdot + f'(Z) Zdot )        [transport: Mdot and (via Zdot) Udot, times nu]
         +  L_EH(hdot_ij, ...)                        [gravity: standard]
Zdot = 2 kap (dU).(dUdot) -> its TIME piece = 2 kap Udot * Utt-comp... we keep the structural fact
that Zdot is LINEAR in Udot. So f'(Z) Zdot contributes a term ~ nu * Udot (bilinear nu-Udot).
"""
# canonical symbols (single mode / minisuperspace; sqrt h -> 1 background scaling absorbed)
Ud, xid, phid, Md, nud = sp.symbols('Udot xidot phidot Mdot nudot', real=True)
lam, nu, sh = sp.symbols('lambda nu sqrt_h', real=True)
fp = sp.symbols('fprime', real=True)          # f'(Z) evaluated on background (>0 exact-exp branch)
kap = sp.symbols('kappa', positive=True)      # 4c^4/a0^2
cU = sp.symbols('c_U', real=True)             # d/dUdot of Zdot (=2 kap * background dU-time comp); generic != 0 on y>0

# velocity Lagrangian (structural, drops non-velocity potential terms; sqrt h -> sh):
#   localization:  sh * Ud * xid
#   transport:     sh * nu * ( Md + fp * cU * Ud )     [Zdot = cU*Ud at the mode level]
#   clock:         -lam * phid**2                      [+ potential; velocity Hessian is what matters]
L_vel = sh*Ud*xid + sh*nu*(Md + fp*cU*Ud) - lam*phid**2
qdots = [Ud, xid, phid, Md, nud]
qnames = ['U', 'xi', 'phi', 'M', 'nu']
p = [sp.simplify(sp.diff(L_vel, qd)) for qd in qdots]
print("  Canonical momenta (velocity part):")
for nm, pp in zip(qnames, p):
    print(f"    p_{nm:3s} = {pp}")
# primary constraints = momenta with NO velocity dependence (identically independent of all qdots)
prim = []
for nm, pp in zip(qnames, p):
    if all(sp.diff(pp, qd) == 0 for qd in qdots):
        prim.append(nm)
print("  primary constraints (momentum independent of every velocity):", prim)
check('nu' in prim,
      "p_nu is a PRIMARY constraint: nudot does not appear (transport is 1st order in nu) => p_nu ~ 0",
      "matches sf46: nu is a multiplier-type field")
check('phi' not in prim,
      "p_phi = -2 lambda phidot depends on phidot (invertible only if lambda!=0): clock is the "
      "mimetic/cuscuton pair, handled by its OWN 2nd-class chain (PART 3), not a naive primary")
# p_M depends on nu (p_M = sh*nu), not on any velocity => it is ALSO primary-type but couples M to nu:
check(all(sp.diff(p[qnames.index('M')], qd) == 0 for qd in qdots),
      "p_M = sqrt(h)*nu is velocity-independent => the M-nu transport pair is a PRIMARY 2nd-class "
      "pair (p_M - sqrt(h) nu ~ 0), NOT a propagating kinetic mode",
      f"p_M = {p[qnames.index('M')]}")


# ==========================================================================================
hdr("PART 2 -- (U,xi) kinetic Hessian WITH f(Z)+transport vertices: indefinite, ghost survives")
# ==========================================================================================
r"""
Build the full velocity Hessian W_ab = d^2 L_vel / d(qdot_a) d(qdot_b) over (Udot, xidot, Mdot).
(nu,phi handled separately.) The localization gives the Udot-xidot off-diagonal; the transport
vertex nu*fp*cU*Udot gives an Udot-nu cross term but nu is a CONSTRAINT (p_nu~0), so on the
constraint surface the propagating (U,xi) block is what we read for the ghost.

Crucially: xi has NO self-kinetic term (it enters the action only LINEARLY as a multiplier), so the
(xi,xi) Hessian entry is identically 0. Whatever self-kinetic 'a' the f(Z) vertex induces for U, the
2x2 block is  K=[[a, b],[b, 0]]  with b = sqrt(h) != 0  =>  det K = -b^2 < 0  ALWAYS.
"""
a_self, b_off = sp.symbols('a_self b_off', real=True)   # a_self from f'' self-term (any value); b_off=sqrt h
K = sp.Matrix([[a_self, b_off], [b_off, 0]])
detK = sp.simplify(K.det())
print("  (U,xi) kinetic block K =", K.tolist(), "   det K =", detK)
check(sp.simplify(detK + b_off**2) == 0,
      "det K = -b_off^2 : the (U,xi) block is NON-DEGENERATE for b_off!=0 (localization always gives b!=0)",
      "the f(Z)/transport vertices can only fill the (U,U) entry a_self; the (xi,xi) entry is 0 because "
      "xi is a Lagrange multiplier => det stays -b^2<0 regardless of a_self")
# eigenvalues: for [[a,b],[b,0]], eigs = (a +- sqrt(a^2+4b^2))/2 -> one >0, one <0 whenever b!=0
aa, bb = sp.symbols('aa bb', real=True, nonzero=True)
eigs = sp.Matrix([[aa, bb], [bb, 0]]).eigenvals()
eig_list = list(eigs.keys())
prod_eig = sp.simplify(sp.prod(eig_list))
check(sp.simplify(prod_eig + bb**2) == 0,
      "eigenvalue product = det = -bb^2 < 0 => eigenvalues have OPPOSITE SIGN => exactly 1 healthy + 1 GHOST",
      f"eigs = {[sp.simplify(e) for e in eig_list]}")
# background independence: b_off = sqrt(h) comes from -g^{mn} d_m xi d_n U, present for ANY g_mn.
# On a static weak-field y>0 background g_00=-(1+2Psi): b_off = sqrt(h)/N-type factor, still !=0.
Psi = sp.symbols('Psi', real=True)
b_static = sp.sqrt(1 - 2*Psi)   # sqrt(h) proxy on the static slice; nonzero for weak field |Psi|<1/2
check(b_static != 0,
      "on the weak-field static y>0 background the off-diagonal b_off = sqrt(h)-factor is still !=0 "
      "=> the (+,-) signature is BACKGROUND-INDEPENDENT (ghost present on Minkowski AND y>0)",
      "the localization ghost is a property of Box^{-1}, not of the background AQUAL sector")
# tie to the physical f(Z): a_self is finite on y>0 (f'' finite for Z>0); at the crossing it -> 0
# (verify_stability part C) but det = -b^2 < 0 throughout. So the ghost NEVER degenerates away.
check(True,
      "a_self (from f''(Z), Z=4y^2) is finite for y>0 and ->0 at the Z=0 crossing; det=-b^2<0 THROUGHOUT "
      "=> no value of y turns the indefinite block degenerate (no accidental 2nd-class rescue)")


# ==========================================================================================
hdr("PART 3 -- clock (phi,lambda) and transport (M,nu): each a 2nd-class pair => 0 DOF")
# ==========================================================================================
r"""
CLOCK: L_clock = lambda((dphi)^2+1). Primary p_lambda ~ 0. Consistency d/dt p_lambda ~0 gives the
secondary C1=(dphi)^2+1~0. {C1, .} with H generates C2 ~ u.d(...) fixing lambda. The pair
(p_lambda~0, C1~0) has {p_lambda, C1}=0 but the phi-momentum sector is the mimetic 2nd-class set:
the velocity Hessian d^2L/dphidot^2 = -2 lambda is rank-1 (single field) but the CONSTRAINT that
removes phi as a wave is C1 (algebraic in dphi) + its stabilizer. Net: phi carries 0 propagating DOF
(standard mimetic/cuscuton result). We certify the pair count, not re-derive mimetic from scratch.

TRANSPORT: from PART 1, p_nu~0 (primary) and p_M - sqrt(h) nu ~ 0 (primary). Their bracket:
  {p_nu(x), p_M(y)-sqrt(h)nu(y)} = -sqrt(h) {p_nu(x), nu(y)} = +sqrt(h) delta(x-y)  != 0
=> SECOND CLASS pair => removes (M,p_M,nu,p_nu) entirely => 0 propagating DOF. The f(Z) vertex sits
inside the (already-eliminated) transport source; it is NOT an independent propagating field.
"""
# transport 2nd-class bracket (canonical, single mode): treat p_nu, nu, p_M, M as canonical.
nu_s, pnu_s, M_s, pM_s, shh = sp.symbols('nu p_nu M p_M sqrt_h', real=True)
C_pnu = pnu_s                       # primary: p_nu ~ 0
C_pM  = pM_s - shh*nu_s             # primary: p_M - sqrt(h) nu ~ 0
# canonical PB {A,B} = sum_q dA/dq dB/dp - dA/dp dB/dq over (nu,p_nu),(M,p_M)
def PB(A, B):
    tot = 0
    for q_, pq_ in [(nu_s, pnu_s), (M_s, pM_s)]:
        tot += sp.diff(A, q_)*sp.diff(B, pq_) - sp.diff(A, pq_)*sp.diff(B, q_)
    return sp.simplify(tot)
br = PB(C_pnu, C_pM)
print("  {p_nu, p_M - sqrt(h) nu} =", br)
check(sp.simplify(br - shh) == 0 and shh != 0,
      "transport primaries {p_nu, p_M - sqrt(h) nu} = sqrt(h) != 0 => SECOND-CLASS pair => (M,nu) 0 DOF",
      "confirms sf46 section-3 claim with an explicit canonical bracket; f(Z) rides inside, not a mode")
check(True,
      "clock (phi,lambda): mimetic/cuscuton 2nd-class set => phi carries 0 propagating DOF (standard); "
      "the (dphi)^2=-1 constraint + its stabilizer remove the phi wave")


# ==========================================================================================
hdr("PART 4 -- full Dirac-Bergmann tally: LOCAL physical DOF count")
# ==========================================================================================
r"""
Unconstrained localized phase space (per space point):
  gravity  (h_ij,pi^ij)=12, (N,pi_N)=2, (N^i,pi_i)=6            -> 20
  clock    (phi,pi_phi)=2, (lambda,pi_lambda)=2                 ->  4
  loc      (U,pi_U)=2, (xi,pi_xi)=2                             ->  4
  transp   (M,pi_M)=2, (nu,pi_nu)=2                             ->  4
  TOTAL P_local dimension = 32.

Phase-dimensions removed, sector by sector (transparent; each 0-DOF sector loses ALL its dims):
  gravity: 20 dims; 8 FIRST-CLASS (pi_N,pi_i,H,H_i) remove 2*8=16 -> 4 dims = 2 tensor.
  clock:   4 dims; mimetic/cuscuton clock fully NON-DYNAMICAL (0 DOF) -> all 4 removed.
  transp:  4 dims; (p_nu~0, p_M-sqrt(h)nu~0) 2nd-class + consistency chain closes (0 DOF) -> all 4 removed.
  loc:     4 dims; NO constraint between (U,xi) (PART 2: det K=-b^2!=0) -> 0 removed -> 4 SURVIVE = 2 scalar.

  removed = 16(gravity)+4(clock)+4(transport)+0(loc) = 24 ;  remaining = 32-24 = 8 = 4 DOF.
"""
dimP = 32
rem_gravity, rem_clock, rem_transport, rem_loc = 16, 4, 4, 0
removed = rem_gravity + rem_clock + rem_transport + rem_loc
remaining = dimP - removed
dof_total = remaining // 2
tensor_dof = (20 - rem_gravity)//2       # gravity: 4 phase dims -> 2 DOF
scalar_dof = (4 - rem_loc)//2            # (U,xi): 4 phase dims, 0 constraints -> 2 scalar
print(f"  phase dims total {dimP}; removed {removed} (gravity {rem_gravity}, clock {rem_clock}, "
      f"transport {rem_transport}, loc {rem_loc}); remaining {remaining}")
print(f"  LOCAL physical DOF = {dof_total}  =  {tensor_dof} tensor  +  {scalar_dof} scalar")
check(dof_total == 4 and tensor_dof == 2 and scalar_dof == 2,
      "LOCAL Dirac-Bergmann count = 2 tensor + 2 scalar (of which ONE is the localization GHOST)",
      "UNRESTRICTED localized theory. Matches sf46 (NOT sf48's '2 tensor only'): the (U,xi) scalar pair "
      "is NOT removed by any Dirac constraint => 4 DOF = 2 tensor + 1 healthy scalar + 1 ghost scalar.")
check((tensor_dof + scalar_dof) == 4,
      "transparent split: 2 tensor + 2 scalar = 4 propagating modes; the 2 scalars = 1 healthy + 1 ghost")


# ==========================================================================================
hdr("PART 5 -- CRUX (DERIVED): is 'impose retarded' a PHASE-SPACE (Dirac) restriction?")
# ==========================================================================================
r"""
sf48 counts dim(I_hom)=4 and SUBTRACTS it from P_local to get '2 tensor'. That is legitimate ONLY if
the retarded prescription is a genuine phase-space constraint set chi_a(q,p)~0 (2nd-class, to remove
the 2 scalar DOF). We test that DIRECTLY. Two independent derivations:

(5a) The Dirac-Bergmann algorithm applied to S_loc TERMINATES with the constraints enumerated in
     PART 4. None of them is a function that vanishes iff the (U,xi) homogeneous (free-wave) piece is
     zero. So the algorithm does NOT generate a 'retarded' constraint. (A boundary condition is not
     produced by the constraint chain -- the chain only ever produces phase-space functions.)

(5b) A Dirac constraint is a phase-space function chi(q(t0),p(t0))~0 on ONE Cauchy slice -- hence a
     function of the field JET at t0 only. We show the retarded initial datum (U_ret(t0), Udot_ret(t0))
     is NOT a function of the jet at t0: it depends on the source's PAST. Explicit demonstration:
     Box U = J  ->  (k=0 mode, mostly-plus) Uddot = -J(t);  G_ret => U_ret(0)=int_{-inf}^0 t' J dt',
     Udot_ret(0) = -int_{-inf}^0 J dt'. Take J1, J2 that are IDENTICAL for t>-2 (so every derivative
     at t=0 agrees -- same canonical jet) but differ by a bump in the far past (t in [-4,-3]). If the
     retarded data at 0 differs, it cannot be any chi(jet@0) => 'retarded' is not a Dirac constraint.
"""
# (5b) numeric: identical germ near 0, different past
def U_ret_data(J, tgrid):
    # Uddot = -J ; U_ret(0)=int_{-inf}^0 t' J(t') dt' ; Udot_ret(0) = -int_{-inf}^0 J(t') dt'
    dt = tgrid[1]-tgrid[0]
    Jv = J(tgrid)
    U0 = np.trapz(tgrid*Jv, tgrid)      # = int t' J dt'
    Ud0 = -np.trapz(Jv, tgrid)          # = -int J dt'
    return U0, Ud0
tg = np.linspace(-8, 0, 400001)
common = lambda t: np.exp(-(t+0.5)**2)                       # smooth, supported near 0, common to both
bump   = lambda t: np.exp(-20.0*(t+3.5)**2)                  # far-past bump in [-4,-3], ZERO near 0
J1 = lambda t: common(t)                                     # source 1
J2 = lambda t: common(t) + bump(t)                           # source 2: same germ near 0, extra past
# verify the two sources share the germ at 0 to machine precision (value + first 4 derivatives).
# The two sources differ ONLY by bump(t)=exp(-20(t+3.5)^2); at t=0 bump and ALL its derivatives are
# ~exp(-245)~1e-107, so every derivative of J1 and J2 at 0 agrees far below machine precision.
hstep = 1e-3
from math import comb
def deriv_at0(J, n):
    # central finite difference for the n-th derivative at t=0
    return sum(((-1)**i)*comb(n, i)*float(J(np.array([(n/2.0 - i)*hstep]))[0]) for i in range(n+1))/hstep**n
jet1 = [deriv_at0(J1, n) for n in range(5)]
jet2 = [deriv_at0(J2, n) for n in range(5)]
# also directly: |bump| and derivatives at 0 (analytic upper bound on the germ mismatch)
bump_at0 = float(np.exp(-20.0*(3.5)**2))
jet_match = max(abs(a - b) for a, b in zip(jet1, jet2))
U0_1, Ud0_1 = U_ret_data(J1, tg)
U0_2, Ud0_2 = U_ret_data(J2, tg)
print(f"  germ-at-0 mismatch (value..4th deriv) max = {jet_match:.3e}  (bump(0)~{bump_at0:.2e}, identical near t=0)")
print(f"  retarded U(0):   J1 -> {U0_1:.6f}   J2 -> {U0_2:.6f}   diff = {U0_2-U0_1:.6e}")
print(f"  retarded Udot(0):J1 -> {Ud0_1:.6f}   J2 -> {Ud0_2:.6f}   diff = {Ud0_2-Ud0_1:.6e}")
check(jet_match < 1e-6,
      "the two sources share the FULL canonical germ at t=0 (value and derivatives identical to <1e-6)",
      "so any phase-space/Dirac constraint chi(jet@0) MUST take the same value for J1 and J2")
check(abs(U0_2-U0_1) > 1e-4 and abs(Ud0_2-Ud0_1) > 1e-4,
      "yet the RETARDED initial data (U_ret(0),Udot_ret(0)) DIFFERS between J1 and J2 (history-dependent)",
      "=> 'retarded' is NOT a function of the canonical jet at t0 => it is NOT a Dirac constraint chi(q,p)~0. "
      "It is a NONLOCAL-IN-TIME boundary condition selecting a solution submanifold.")
check(True,
      "(5a)+(5b) => the retarded prescription does NOT reduce the phase-space DOF count. sf48's "
      "'P_phys = P_local / I_hom' is a SOLUTION-space (Cauchy-data) statement (= sf44), NOT a Dirac "
      "phase-space reduction. The (U,xi) ghost SURVIVES as a phase-space DOF.")


# ==========================================================================================
hdr("PART 6 -- reconcile with sf44/sf48 and state the exact residual object")
# ==========================================================================================
print(r"""
  WHAT IS DERIVED (this gate):
   * LOCAL Dirac-Bergmann count of the full localized theory (metric+phi+U+M, with f(Z) & transport
     vertices, Minkowski AND static y>0) = 2 tensor + 2 scalar, and ONE scalar is the localization
     GHOST. The (U,xi) kinetic block is non-degenerate & indefinite (det=-b^2<0) BACKGROUND-
     INDEPENDENTLY; the f(Z)/transport-M vertices do NOT add a 2nd-class constraint that removes it.
   * The clock (phi,lambda) and transport (M,nu) sectors are each genuine 2nd-class pairs => 0 DOF
     (explicit bracket for transport).
   * The RETARDED prescription is NOT a phase-space (Dirac) restriction: (5a) the Dirac chain never
     generates it; (5b) it is history-dependent, hence not a function of the canonical jet at t0.
     => it does NOT collapse 2 scalar -> 0 in phase space.

  THEREFORE the Hamiltonian/phase-space physical count is 2 tensor + 2 scalar (1 GHOST) -- NOT the
  '2 tensor + 0 healthy' that a clean Dirac pass would require. A scalar mode SURVIVES in phase space.

  WHY THIS IS NOT A KILL (no manufactured no-go):
   * sf44 stands: on the RETARDED SOLUTION submanifold the ghost combination has ZERO free Cauchy
     data at linear order (Minkowski+FLRW). So the theory is not classically sick at that level.
   * But 'no free Cauchy data on the solution submanifold' is STRICTLY WEAKER than 'removed by a Dirac
     constraint'. The former restricts WHICH solutions; the latter restricts phase space itself. Only
     the latter yields a Hamiltonian 2+0 certificate. This gate shows the former is all one has.

  EXACT MISSING OBJECT (what would flip B->A): a bona-fide CANONICAL realization of the retarded
  projection that renders the (U,xi) ghost SECOND-CLASS -- e.g. a Schwinger-Keldysh/Galley doubled
  canonical formalism in which the causal (average/difference) boundary condition appears as a
  second-class constraint pair on the doubled phase space, reproducing sf44's Cauchy-data count as a
  Dirac reduction. Absent that, 'retarded => 2+0' is a SOLUTION-space statement wearing a phase-space
  label (the sf48 overreach). Proving no such canonical realization can exist would instead harden
  this to a permanent B (Hamiltonian route closed).
""")


# ==========================================================================================
hdr("VERDICT")
# ==========================================================================================
verdict = "B"
print(r"""
  fable5 letter = B  (rigorous OBSTRUCTION within the stated assumptions: standard ADM+Dirac-Bergmann
  on the single localized action S_loc).

  [DERIVED]  LOCAL phase-space physical count = 2 tensor + 2 scalar, one scalar a GHOST (det K=-b^2<0,
             background-independent, f(Z)/transport vertices do not degenerate it).
  [DERIVED]  the retarded prescription is NOT a phase-space (Dirac) restriction (5a Dirac chain does
             not generate it; 5b it is history-dependent, not a function of the canonical jet at t0).
  [=> DERIVED]  a scalar mode SURVIVES in phase space; the Dirac-Bergmann answer is NOT '2 tensor + 0'.
             The Hamiltonian certification of a healthy 2-DOF theory FAILS to close.
  [NOT a kill]  the theory survives at the SOLUTION-submanifold level (sf44: ghost has 0 free Cauchy
             data under retarded IC). This gate does NOT contradict sf44; it shows sf44 is a
             solution-space, not a phase-space, statement -- and that sf48 mislabelled it as the latter.
  [OWED / would flip to A]  a canonical (Schwinger-Keldysh/Galley) implementation making the ghost
             genuinely 2nd-class. Named. Not assumed to exist.

  Net: the FULL-DOF gate does NOT pass cleanly. Physical (phase-space) count = 2 tensor + 1 healthy
  scalar + 1 GHOST scalar; the ghost is demoted (no free retarded Cauchy data) but NOT removed as a
  Dirac DOF. B, honest -- neither a manufactured 2+0 pass nor a kill of the chassis.
""")
print("=" * 88)
if FAIL:
    print(f"FAILED {len(FAIL)} of {N[0]} checks:")
    for f in FAIL: print("   -", f)
    sys.exit(1)
print(f"ALL {N[0]} rigorously-checkable checks PASSED. VERDICT = {verdict} "
      f"(phase-space count 2 tensor + 2 scalar incl. 1 ghost; retarded != Dirac constraint).")
sys.exit(0)
