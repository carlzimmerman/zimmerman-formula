#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sector2_conserved_charge_dust_2026.py
=====================================
SECTOR 2 (c)+(d): THE CONSERVED SHIFT CHARGE AND THE DUST IDENTIFICATION, derived on FRW from the
GENERALIZED action by minisuperspace variation (lapse N(t), scale factor a(t), khronon phi(t),
comoving unit aether A^mu = (1/N, 0, 0, 0)), plus the general Legendre theorem behind stage 5.

WHAT IS DERIVED HERE (each certified by a sympy check capable of failing):
  (C1) the Friedmann equation from delta S/delta N:  3H^2 (1 - 24 pi G c2) = Lambda + 8 pi G rho_Q,
       rho_Q = sigma_K [ Q K'(Q) - K(Q) ]      (the c2 (nabla.A)^2 term renormalises G on FRW as in
       Einstein-aether: 1 - 24 pi G c2 = 1 + (3/2) c2^{JM}, c2^{JM} = -16 pi G c2).
  (C2) SIGN CONSTRAINT (derived, not assumed): at the dS minimum rho_Q(Q0) = -sigma_K K(Q0) = sigma_K M^4,
       so rho_vac = rho_Lambda > 0 REQUIRES sigma_K > 0.  The doc's displayed "-2K(Q)" (sigma_K = -2)
       gives rho_vac = -2 M^4 < 0 and a wrong-sign phidot^2 kinetic term for the excitation.  The
       physically consistent reading (and the one every repo script uses: stage 5/17/22, p = K) is
       L_Q = +K(Q).  This is a transcription-sign finding, flagged; all Sector-2 equations keep sigma_K.
  (C3) the scalar equation on FRW is exactly  d/dt [ a^3 sigma_K K'(Q) ] = 0:  n = sigma_K K'(Q) is the
       conserved shift-charge density, n a^3 = const.  The promoted MOND term and the bump contribute
       NOTHING to it (G(0) = 0, B(0) = 0): the charge is promotion-blind on FRW.
  (C4) STAGE 5's THEOREM, generalised: for ANY shift-symmetric L(Q; Y) with a stationary point at Q0
       (n(Q0) = 0),  rho = rho_vac(Y) + Q0 n + O(n^2)  with rho_vac(Y) = -L(Q0; Y).  The dark-sector
       gravitating mass is Q0 times the conserved charge to leading order, INDEPENDENT of the bump
       amplitude Acal, of the bump shape B, and of the promotion (kappa).  d(rho/n)/d(anything) -> 0.
  (C5) beta = 1 DBI closed forms on FRW (sigma_K = +1):  with nu = n/(mu M^2) and n a^3 = const,
       rho_Q = Q0 n + M^4 sqrt(1+nu^2),  p_Q = -M^4/sqrt(1+nu^2),  rho_nd p_nd = -M^8 (exact invariant);
       w = -1 EXACTLY at nu = 0; the excitation is DUST (w_exc -> 0 as nu -> 0, rho_exc = Q0 n ∝ a^-3);
       the promotion then gives a0^2(z)/a0^2(0) = sqrt(1+nu0^2)/sqrt(1+nu0^2 (1+z)^6) (stage 17 B2).
  (C6) on-shell continuity: rhodot_Q + 3H (rho_Q + p_Q) = sigma_K Q a^-3 d(a^3 K')/dt = 0 EXACTLY on the
       charge equation -- the Q-sector stress tensor is conserved on FRW by the scalar equation alone
       (the Bianchi-consistency of Sector 2 with the metric sector).
  (C7) CONTROL: breaking the shift symmetry (L -> L - V(phi)) gives d(a^3 n)/dt = -a^3 V'(phi) != 0
       and the dust scaling fails.  Conservation <=> shift symmetry, exactly as stage 5 B2.

(d) THE STRUCTURE (a statement, not a new theorem):  shift symmetry of the Q-sector  <=>  a conserved
    charge n a^3  =>  the excitation's leading energy is Q0 n ∝ a^-3 (DUST: this is what the CMB
    measures, THE_COMPLETION rows 9/19)  AND  the SAME K(Q) at n = 0 has p = -rho = K(Q0) (w = -1
    EXACT: dark energy).  One property of one field.  The session-level universal conclusion
    (HANDOFF_2026-08-31 §2e; YORK_CAUSAL_GATE_VERDICT.md; FRIED_CHICKEN_VERDICT_2026-09-01.md) --
    {MOND lensing} + {2 local DOF} + {causal single metric} => a dark field -- is CITED, not re-proved
    here.  What Sector 2 adds is only the mechanism inside THIS action: the charge that carries
    Omega_dm is the Noether charge of the shift symmetry, and it cannot be removed locally (stage 5).

CONVENTIONS: (-,+,+,+), c = 1, a0^2(Q) = -kappa^2 G K(Q) (INPUT), K(Q) = -M^4 sqrt(1 - mu^2 (Q-Q0)^2/M^4).
"""
import sys
import sympy as sp

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""), flush=True)
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""), flush=True)


print(__doc__)

t = sp.Symbol("t", real=True)
G, Lam, c2, sK, kap, Ac = sp.symbols("G Lambda c_2 sigma_K kappa Acal", real=True)
KB, c4 = sp.symbols("K_B c_4", real=True)
M4, mu, Q0 = sp.symbols("M4 mu Q_0", positive=True)
N = sp.Function("N", positive=True)(t)
a = sp.Function("a", positive=True)(t)
ph = sp.Function("phi")(t)
Kg = sp.Function("K")                                     # generic K(Q) first

# ================================================================================================
print("=" * 100)
print("PART C1/C2 -- minisuperspace: Friedmann equation from delta S/delta N, and the sign of rho_Q")
print("=" * 100)
# FRW with lapse: R = 6[ addot/(a N^2) + adot^2/(a^2 N^2) - adot Ndot/(a N^3) ]
adot, addot, Ndot = sp.diff(a, t), sp.diff(a, t, 2), sp.diff(N, t)
R = 6 * (addot / (a * N ** 2) + adot ** 2 / (a ** 2 * N ** 2) - adot * Ndot / (a * N ** 3))
sqrtg = N * a ** 3
Q = sp.diff(ph, t) / N                                    # Q = A^mu d_mu phi with A^0 = 1/N
divA = 3 * adot / (a * N)                                 # nabla_mu A^mu for the comoving aether
# the aether pieces on FRW: F = 0, a^mu = 0, Y = 0, lambda-term = 0 (all shown in Script A, Part 3b)
L_EH = sqrtg * (R - 2 * Lam) / (16 * sp.pi * G)
L_ae = sqrtg * (c2 * divA ** 2)                           # c4 a^2 = 0, F^2 = 0, drag = 0, Y = 0
L_Q = sqrtg * sK * Kg(Q)
# promoted MOND term and bump on FRW: Y = 0 => G(0) = 0, B(0) = 0  (checked in C3 with the real forms)
Ltot = L_EH + L_ae + L_Q


def EL(Lag, f):
    return sp.expand(sp.diff(Lag, f) - sp.diff(sp.diff(Lag, sp.diff(f, t)), t)
                     + sp.diff(sp.diff(Lag, sp.diff(f, t, 2)), t, 2))


E_N = sp.simplify(EL(Ltot, N).subs(N, 1).doit())
H = adot / a
rhoQ_claim = sK * (Q * sp.Derivative(Kg(Q), Q) - Kg(Q))
rhoQ_claim = sK * (sp.diff(ph, t) * sp.diff(Kg(sp.Symbol("q")), sp.Symbol("q")).subs(sp.Symbol("q"), sp.diff(ph, t)) - Kg(sp.diff(ph, t)))
friedmann = 3 * H ** 2 * (1 - 24 * sp.pi * G * c2) - Lam - 8 * sp.pi * G * rhoQ_claim
# E_N = 0 should be  -(a^3/(8 pi G)) * friedmann  (up to overall sign convention)
ratio = sp.simplify(E_N / friedmann)
check(sp.simplify(ratio + a ** 3 / (8 * sp.pi * G)) == 0 or sp.simplify(ratio - a ** 3 / (8 * sp.pi * G)) == 0,
      "(C1) delta S/delta N = 0  <=>  3H^2 (1 - 24 pi G c2) = Lambda + 8 pi G rho_Q,  rho_Q = sigma_K [Q K'(Q) - K(Q)]",
      f"E_N / friedmann = {ratio}")
info("(C1) the c2 (nabla.A)^2 term renormalises the cosmological G exactly as Einstein-aether: "
     "1 - 24 pi G c2 = 1 + (3/2) c2^{JM} with c2^{JM} = -16 pi G c2 (the doc's +c2(nabla.A)^2 is MINUS the "
     "Jacobson-Mattingly sign; its quoted c_S^2 formula uses the JM sign -- flagged for the metric/PPN sectors)")

# sign constraint at the dS minimum
Kdbi = lambda q: -M4 * sp.sqrt(1 - mu ** 2 * (q - Q0) ** 2 / M4)
q = sp.Symbol("q", real=True)
rho_dbi = sK * (q * sp.diff(Kdbi(q), q) - Kdbi(q))
p_dbi = sK * Kdbi(q)
rho_vac = sp.simplify(rho_dbi.subs(q, Q0))
p_vac = sp.simplify(p_dbi.subs(q, Q0))
check(rho_vac == sK * M4 and p_vac == -sK * M4,
      "(C2) at the minimum Q = Q0: rho_Q = sigma_K M^4, p_Q = -sigma_K M^4  =>  w = -1 EXACTLY for either sign",
      "rho_vac = rho_Lambda = M^4 > 0 REQUIRES sigma_K > 0")
u = sp.Symbol("u", real=True)
Lkin = sp.series(sK * Kdbi(Q0 + u), u, 0, 3).removeO()
check(sp.expand(Lkin - (-sK * M4 + sK * mu ** 2 * u ** 2 / 2)) == 0,
      "(C2) L_Q = sigma_K K(Q0+u) = -sigma_K M^4 + sigma_K mu^2 u^2/2 + O(u^4): the excitation's phidot^2 "
      "coefficient has the sign of sigma_K -- healthy iff sigma_K > 0 (K'' = mu^2 > 0 given)")
check(rho_vac.subs(sK, -2) < 0,
      "(C2) *** the doc's literal '-2K(Q)' (sigma_K = -2) gives rho_vac = -2 M^4 < 0 (anti-de Sitter) -- "
      "inconsistent with its own '-K(Q0) = rho_Lambda at the de Sitter minimum'.  Consistent reading: L_Q = +K(Q) ***",
      "transcription-sign finding; the repo's scripts (stage 5/17, svt aether_cross_check: +sqrt(-g) K) all use +K")

# ================================================================================================
print()
print("=" * 100)
print("PART C3 -- the scalar equation on FRW is charge conservation; promotion and bump are blind to it")
print("=" * 100)
# the REAL L_s on FRW: promoted G term and bump, with Y as a symbol to be set to 0 after differentiating
Ysym = sp.Symbol("Y", nonnegative=True)
a0sq = -kap ** 2 * G * Kdbi(q)
yv = sp.sqrt(Ysym) / sp.sqrt(a0sq)
Gk = yv ** 2 + 2 * (1 + yv) * sp.exp(-yv) - 2
Bf = lambda w: w / (1 + w) ** 2
Ls_real = a0sq / (8 * sp.pi * G) * Gk + sK * Kdbi(q) + Ac * Bf(Ysym / a0sq) * (q - Q0) ** 2
FQ_Y0 = sp.simplify(sp.diff(Ls_real, q).subs(Ysym, 0))
check(sp.simplify(FQ_Y0 - sK * sp.diff(Kdbi(q), q)) == 0,
      "(C3) F_Q(Y=0, Q) = sigma_K K'(Q): the promoted MOND term and the bump drop out of the FRW charge exactly")
check(sp.simplify(Ls_real.subs(Ysym, 0) - sK * Kdbi(q)) == 0,
      "(C3) L_s(Y=0, Q) = sigma_K K(Q): they drop out of the FRW background Lagrangian too (G(0) = B(0) = 0)")
E_phi = sp.expand(EL(Ltot, ph).subs(N, 1).doit())
n_claim = sK * sp.diff(Kg(q), q).subs(q, sp.diff(ph, t))
charge_law = sp.diff(a ** 3 * n_claim, t)
check(sp.simplify(E_phi + charge_law) == 0,
      "(C3) delta S/delta phi = 0  <=>  d/dt [ a^3 sigma_K K'(Q) ] = 0:  n = sigma_K K'(Q), n a^3 = const  (the shift charge)")

# ================================================================================================
print()
print("=" * 100)
print("PART C4 -- stage 5's theorem, generalised: rho = rho_vac + Q0 n + O(n^2) for ANY shift-symmetric L")
print("=" * 100)
Lg = sp.Function("L")                                     # generic L(Q; Y) -- Y a parameter
Lfun = Lg(Q0 + u, Ysym)
n_g = sp.diff(Lfun, u)
rho_g = (Q0 + u) * n_g - Lfun
# impose only: n(Q0; Y) = 0  (Q0 is a stationary point of L in Q for every Y)
n1 = sp.Symbol("n_1", real=True)                           # dn/du at u = 0
L0 = sp.Symbol("L_0", real=True)
ser_rho = sp.series(rho_g, u, 0, 3).removeO()
ser_n = sp.series(n_g, u, 0, 3).removeO()
# replace derivatives at u=0 by symbols; the stationarity condition sets the first derivative to zero
D1 = sp.Subs(sp.Derivative(Lg(sp.Symbol("_q"), Ysym), sp.Symbol("_q")), sp.Symbol("_q"), Q0)
subs_map = {}
for at in (ser_rho.atoms(sp.Subs) | ser_n.atoms(sp.Subs) | ser_rho.atoms(sp.Derivative)):
    pass
# cleaner: build the expansion by hand from Taylor coefficients of a generic function
L1, L2, L3 = sp.symbols("L_1 L_2 L_3", real=True)
Ltay = L0 + L1 * u + L2 * u ** 2 / 2 + L3 * u ** 3 / 6
n_t = sp.diff(Ltay, u)
rho_t = sp.expand((Q0 + u) * n_t - Ltay)
rho_t0 = rho_t.subs(L1, 0)                                 # stationarity: n(Q0) = L1 = 0
n_t0 = n_t.subs(L1, 0)
resid = sp.expand(rho_t0 - (-L0 + Q0 * n_t0))
check(sp.Poly(resid, u).degree() >= 2 and resid.coeff(u, 0) == 0 and resid.coeff(u, 1) == 0,
      "(C4) rho = -L(Q0;Y) + Q0 n + O(u^2) for a GENERIC L with n(Q0) = 0: the leading excitation energy is "
      "Q0 x (conserved charge), whatever the Y-dependence (bump, promotion, kernel)",
      f"remainder = {sp.factor(resid)}  (= n^2/(2 L_2) + ... : the stage-5 'cost' term)")
check(sp.simplify(sp.limit(rho_t0.subs(L0, 0) / n_t0, u, 0) - Q0) == 0,
      "(C4) rho_exc / n -> Q0 as u -> 0, independent of L_2, L_3 (i.e. of Acal, B, kappa): stage 5 B1 generalised")
# the same with the ACTUAL L_s, Y kept as a parameter (stage 5's setting: static environment, Y != 0)
n_real = sp.diff(Ls_real, q)
rho_real = q * n_real - Ls_real
ser = sp.series(rho_real.subs(q, Q0 + u), u, 0, 2).removeO()
lead = sp.simplify(ser.coeff(u, 1))
n_lead = sp.simplify(sp.series(n_real.subs(q, Q0 + u), u, 0, 2).removeO().coeff(u, 1))
check(sp.simplify(lead - Q0 * n_lead) == 0 and sp.simplify(n_real.subs(q, Q0)) == 0,
      "(C4) with the doc's ACTUAL L_s (kernel + DBI + bump + promotion, Y != 0): n(Q0) = 0 and "
      "d rho/du|_0 = Q0 dn/du|_0 -- rho_exc = Q0 n at leading order, promotion and bump included",
      f"dn/du|_0 = {n_lead}  (stage 5's mu^2 + 2 A_s S, here sigma_K mu^2 + 2 Acal B(Y/a0^2))")
check(sp.simplify(sp.diff(lead / n_lead, Ac)) == 0 and sp.simplify(sp.diff(lead / n_lead, kap)) == 0,
      "(C4) rho/n at leading order is independent of Acal and of kappa: no bump amplitude, no promotion strength "
      "changes how much mass a given charge carries")

# ================================================================================================
print()
print("=" * 100)
print("PART C5 -- beta = 1 DBI closed forms on FRW (sigma_K = +1) and the derived a0(z) law")
print("=" * 100)
nu = sp.Symbol("nu", positive=True)
s = nu / sp.sqrt(1 + nu ** 2)                               # u mu / M^2 = s  (exact inversion of n(u))
u_of_nu = s * M4 / mu                                       # M^2 = sqrt(M4); write M^4 = M4, M^2 = sqrt(M4)
u_of_nu = s * sp.sqrt(M4) / mu
n_dbi = sp.diff(Kdbi(q), q)                                 # sigma_K = 1
n_nu = sp.simplify(n_dbi.subs(q, Q0 + u_of_nu))
check(sp.simplify(n_nu - mu * sp.sqrt(M4) * nu) == 0,
      "(C5) charge-to-excitation inversion: n = mu M^2 nu  with  u = (M^2/mu) nu/sqrt(1+nu^2)  (exact)")
rho_nu = sp.simplify((q * n_dbi - Kdbi(q)).subs(q, Q0 + u_of_nu))
p_nu = sp.simplify(Kdbi(q).subs(q, Q0 + u_of_nu))
check(sp.simplify(rho_nu - (Q0 * n_nu + M4 * sp.sqrt(1 + nu ** 2))) == 0 and sp.simplify(p_nu + M4 / sp.sqrt(1 + nu ** 2)) == 0,
      "(C5) rho_Q = Q0 n + M^4 sqrt(1+nu^2),   p_Q = -M^4/sqrt(1+nu^2)   (exact, beta = 1)")
rho_nd = rho_nu - Q0 * n_nu
check(sp.simplify(rho_nd * p_nu + M4 ** 2) == 0,
      "(C5) rho_nd p_nd = -M^8: the non-dust remainder obeys an exact invariant (THE_COMPLETION non-claim 2f)")
w_vac = sp.simplify((p_nu / rho_nu).subs(nu, 0))
check(w_vac == -1, "(C5) w = -1 EXACTLY at nu = 0 (the dS minimum): dark energy")
rho_exc = sp.simplify(rho_nu - M4)
p_exc = sp.simplify(p_nu + M4)
w_exc = sp.simplify(p_exc / rho_exc)
check(sp.limit(w_exc, nu, 0) == 0 and sp.simplify(sp.series(rho_exc, nu, 0, 2).removeO() - Q0 * mu * sp.sqrt(M4) * nu) == 0,
      "(C5) the excitation is DUST: w_exc -> 0 and rho_exc = Q0 n + O(nu^2), with n a^3 = const => rho_exc ∝ a^-3",
      f"w_exc = {w_exc}")
# the promotion (INPUT) evaluated along the background: a0^2 ∝ -K
a0sq_nu = sp.simplify((-kap ** 2 * G * Kdbi(q)).subs(q, Q0 + u_of_nu))
nu0, zz = sp.symbols("nu_0 z", positive=True)
law = sp.simplify(a0sq_nu.subs(nu, nu0 * (1 + zz) ** 3) / a0sq_nu.subs(nu, nu0))
check(sp.simplify(law - sp.sqrt(1 + nu0 ** 2) / sp.sqrt(1 + nu0 ** 2 * (1 + zz) ** 6)) == 0,
      "(C5) a0^2(z)/a0^2(0) = sqrt(1+nu0^2)/sqrt(1+nu0^2 (1+z)^6)  [DERIVED from the promotion, which is INPUT; "
      "nu ∝ a^-3 from the charge law]; a0^2(0) = kappa^2 G M^4/sqrt(1+nu0^2) -> kappa^2 G rho_Lambda as nu0 -> 0")

# ================================================================================================
print()
print("=" * 100)
print("PART C6 -- on-shell continuity of the Q-sector from the charge equation alone")
print("=" * 100)
Kq = sp.Function("K")
Qt = sp.Function("Q")(t)
rhoQ_t = sK * (Qt * sp.Derivative(Kq(Qt), Qt) - Kq(Qt))
pQ_t = sK * Kq(Qt)
Ht = sp.Function("H")(t)
cont = sp.diff(rhoQ_t, t) + 3 * Ht * (rhoQ_t + pQ_t)
charge_rate = sK * Qt * (sp.diff(sp.Derivative(Kq(Qt), Qt), t) + 3 * Ht * sp.Derivative(Kq(Qt), Qt))
check(sp.simplify(cont - charge_rate) == 0,
      "(C6) rhodot_Q + 3H(rho_Q + p_Q) = sigma_K Q [ dK'/dt + 3H K' ] = sigma_K Q a^-3 d(a^3 K')/dt = 0 on the charge law")

# ================================================================================================
print()
print("=" * 100)
print("PART C7 -- CONTROL: break the shift symmetry and the charge law fails")
print("=" * 100)
V = sp.Function("V")
Ltot_V = Ltot - sqrtg * V(ph)
E_phi_V = sp.expand(EL(Ltot_V, ph).subs(N, 1).doit())
check(sp.simplify(E_phi_V + charge_law + a ** 3 * sp.Derivative(V(ph), ph)) == 0,
      "(C7) with L -> L - V(phi):  d/dt [a^3 n] = -a^3 V'(phi) != 0 -- the charge is no longer conserved "
      "(stage 5 B2: conservation <=> shift symmetry)")
# and the dust scaling fails: a toy V = m^2 phi^2/2 with K quadratic gives d(a^3 n)/dt = -a^3 m^2 phi
m = sp.Symbol("m", positive=True)
check(sp.simplify((E_phi_V + charge_law).subs(V(ph), m ** 2 * ph ** 2 / 2).doit() + a ** 3 * m ** 2 * ph) == 0,
      "(C7) e.g. V = m^2 phi^2/2:  d(a^3 n)/dt = -a^3 m^2 phi  =>  rho_exc = Q0 n is no longer ∝ a^-3")

print()
print("=" * 100)
print("(d) THE STRUCTURE -- one property of one field (statement)")
print("=" * 100)
print(r"""
   shift symmetry  phi -> phi + const  of the Q-sector
        <=>  nabla_mu J^mu = 0  with  J^0 sqrt(-g) = a^3 sigma_K K'(Q)   (C3; control C7)
        =>   n a^3 = const, and  rho_exc = Q0 n + O(n^2)                  (C4: Legendre identity, generic L)
        =>   the excitation gravitates as DUST, rho_exc ∝ a^-3, w_exc -> 0  (C5)
   and the SAME K(Q), at n = 0:  p = -rho = sigma_K K(Q0)  =>  w = -1 EXACTLY   (C2, C5)
   with the promotion reading off -K(Q) along the same background: a0^2(z) ∝ M^4/sqrt(1+nu^2)   (C5; INPUT)

   The dark-energy triumph (w = -1 exact), the CMB's clustering component (dust from the charge), and the
   inability to remove that component locally (stage 5: a conserved charge can only be moved or not
   conserved) are the same property of the same field.  This is the mechanism, inside THIS action, behind
   the session's universal conclusion that every causal single-metric MOND-lensing completion carries a
   dark field (cited: HANDOFF_2026-08-31 §2e).  Not claimed: that the dark field must be THIS field, that
   sigma_K's sign is settled by the doc as written (C2 says it is not), or that a0(z) is derived (C5: the
   promotion is a definitional input; only the closed form downstream of it is derived).
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
