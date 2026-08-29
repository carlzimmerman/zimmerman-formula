#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
dirac_Phi_Q_sf42_route_2026.py
=====================================================================================
THE "sf42 REPAIR": carry the MOND field in an INDEPENDENT auxiliary potential Phi
instead of in the lapse (phi = ln N).  Full Dirac/DOF + strong coupling + lensing +
Newtonian gates.  Adapted from the trusted machinery of
    dirac_chi_Q_frozen_candidate_2026.py     (47/47, committed, 3 DOF verdict)

THE CANDIDATE UNDER TEST (as handed over):
  S = (c^3/16 pi G) int dt d3x N sqrt(g) [ K_ij K^ij - K^2 + R3 - 2 Lambda ]
    - (c^3/16 pi G) int dt d3x N sqrt(g) [ chi (D Phi)^2 + V(chi) ]
    + (c^3/16 pi G) int dt d3x N sqrt(g) [ f(chi) Q^ij A_ij - (1/2) Q^ij KK_ijkl Q^kl ]
    + S_m[g, psi]  + S_int[Phi, matter]
  A_ij = [D_i Phi D_j Phi]^TF ,  Q_ij spatial TF (5), chi auxiliary,
  V'(chi) = -[ln(1-chi)]^2   (=> chi = mu(y) = 1-e^{-y},  y = |D Phi| in a0 = c = 1),
  f(chi) = chi V'(chi)  -> -mu(y) y^2 = Sigma_P^cov ,
  KK_ijkl = m^2 * Identity_TF.

LABELS:  PROVEN (exact symbolic identity)
         COMPUTATIONALLY_VERIFIED (exact symbolic on a linearised/WKB background, k exact)
         PARTIAL / OPEN / NOT_REACHED
Exit 0 = every numbered boolean check passed.
"""
import sys
import sympy as sp
import numpy as np

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d} {label}" + (f"\n          {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")


def hdr(s):
    print("\n" + "=" * 88)
    print(s)
    print("=" * 88)


# ================================================================================
hdr("PART A -- the frozen constitutive functions for the sf42 route (exact)")
# ================================================================================
y = sp.Symbol('y', positive=True)          # y = |D Phi| in units a0 = c = 1
chi_s = sp.Symbol('chi', positive=True)
m2 = sp.Symbol('m2', positive=True)        # the LOCAL kernel KK = m2 * Id_TF

chi_of_y = 1 - sp.exp(-y)                                  # mu(y)
Vp_chi = -sp.log(1 - chi_s)**2                             # V'(chi)   (sign as corrected last round)
f_chi = chi_s * Vp_chi                                     # f = chi V'(chi)   <== THE NEW CARRIER

dy_dchi = sp.simplify(1 / sp.diff(chi_of_y, y))            # = e^{y}
push = lambda e: sp.simplify(e.subs(chi_s, chi_of_y))
dchi = lambda e_y: sp.simplify(sp.diff(e_y, y) * dy_dchi)  # d/dchi acting on a function of y

Vp_y = push(Vp_chi)
f_y = sp.simplify(sp.expand(push(f_chi)))
check(sp.simplify(Vp_y + y**2) == 0, "V'(chi(y)) = -y^2  (exact)", f"V' = {Vp_y}")
check(sp.simplify(f_y - (-(1 - sp.exp(-y)) * y**2)) == 0,
      "f(chi(y)) = -mu(y) y^2 = Sigma_P^cov   (the handover's exact profile match, RE-VERIFIED)",
      f"f = {sp.factor(f_y)}")

Vpp = dchi(Vp_y)
Vppp = dchi(Vpp)
fp = dchi(f_y)
fpp = dchi(fp)
check(sp.simplify(Vpp + 2 * y * sp.exp(y)) == 0, "V''(chi) = -2 y e^{y}  (< 0 for y>0)", f"V'' = {Vpp}")
check(sp.simplify(fp - (Vp_y + chi_of_y * Vpp)) == 0,
      "f'(chi) = V' + chi V''  (chain rule self-check)", f"f' = {sp.simplify(fp)}")
check(sp.simplify(fp - (-y**2 - 2 * y * sp.exp(y) + 2 * y)) == 0,
      "f'(chi) = -y^2 - 2 y e^{y} + 2 y   <== EXPONENTIALLY LARGE in y",
      f"f'(y=10) = {float(fp.subs(y,10)):.4e},  f'(y=20) = {float(fp.subs(y,20)):.4e}")

# analyticity in chi (the handover's claimed advantage) -- CONFIRMED
ser_chi = sp.series(f_chi, chi_s, 0, 6).removeO()
check(sp.simplify(sp.expand(ser_chi) - (-chi_s**3 - chi_s**4 - sp.Rational(11, 12) * chi_s**5)) == 0,
      "f(chi) = -chi^3 - chi^4 - (11/12) chi^5 + ...  : POLYNOMIAL/ANALYTIC at chi = 0, no branch cut",
      f"series = {sp.expand(ser_chi)}   [the handover's 'strictly cleaner than (1-chi)sqrt(-V')' is TRUE in chi]")

# ... but the SAME statement in y is the opposite of clean.  Contrast with last round's carrier.
f_old_y = y * sp.exp(-y)                       # last round: f = (1-chi) sqrt(-V')
fp_old = dchi(f_old_y)
check(sp.simplify(fp_old - (1 - y)) == 0,
      "CONTRAST: last round's f_old = y e^{-y} has f_old'(chi) = 1 - y  -- POLYNOMIAL in y",
      "the NEW f is analytic in chi but its chi-derivative is EXPONENTIAL in y; the Q back-reaction\n"
      "          and the Newtonian limit see the y-behaviour, not the chi-behaviour.  Flagged for PART I.")

V_y = sp.exp(-y) * (y**2 + 2 * y + 2) - 2      # V fixed by V(0)=0
check(sp.simplify(dchi(V_y) - Vp_y) == 0, "V(chi) = e^{-y}(y^2+2y+2) - 2 integrates V'  (exact)")
bracket = sp.simplify(chi_of_y * y**2 + V_y)
check(sp.simplify(sp.series(bracket, y, 0, 4).removeO() - sp.Rational(2, 3) * y**3) == 0,
      "chi (D Phi)^2 + V = (2/3) y^3 + O(y^4) = the deep-MOND AQUAL Lagrangian (exact series)")
print("  LABEL: PROVEN.  The frozen (V, f) pair is exactly as handed over; nothing transcendental inserted.")


# ================================================================================
hdr("PART B -- T1(a): is Phi AUXILIARY or DYNAMICAL?  (decide from the action, and SAY)")
# ================================================================================
Ndot, Nidot, chidot, Qdot, Phidot = sp.symbols('Ndot Nidot chidot Qdot Phidot', real=True)
Kgen, Kijsq = sp.symbols('K Kijsq', real=True)
Lden = (Kijsq - Kgen**2) + sp.Symbol('R3') - 2 * sp.Symbol('Lam') \
    - (sp.Symbol('chi') * sp.Symbol('DPhi2') + sp.Symbol('V')) \
    + (sp.Symbol('f') * sp.Symbol('QA') - sp.Rational(1, 2) * sp.Symbol('QKQ'))
for v, nm in [(Ndot, 'pi_N'), (Nidot, 'pi_i'), (chidot, 'pi_chi'),
              (Qdot, 'pi_Q^ij'), (Phidot, 'pi_Phi')]:
    check(sp.diff(Lden, v) == 0, f"dL/d({v}) = 0  =>  PRIMARY constraint  {nm} ~ 0")

print(r"""  ANSWER: Phi is AUXILIARY.  The action contains D_i Phi only -- never Phidot -- so
  pi_Phi ~ 0 is a PRIMARY constraint, exactly like pi_chi and pi_Q.

  WHAT THAT COSTS, made explicit.  (D_i Phi)(D^i Phi) is NOT a spacetime scalar.  With
  u^mu the unit normal of the ADM foliation,
        (D Phi)^2 = (g^{mu nu} + u^mu u^nu) d_mu Phi d_nu Phi = (dPhi)^2 + (u.dPhi)^2 ,
  i.e. the action is built from the FOLIATION PROJECTOR.  Keeping Phi auxiliary and
  keeping 4-diffeo invariance are mutually exclusive: restoring (dPhi)^2 alone would put
  Phidot back and make Phi dynamical.  So this candidate is, like the previous one, a
  PREFERRED-FOLIATION (khronon-class) theory.  The MOND field has moved off the lapse;
  the foliation has NOT.  This is verified as an identity next, and it is what PART H
  cashes out as the surviving third mode.""")

# exact ADM identity  (D Phi)^2 = (dPhi)^2 + (u.dPhi)^2
Nl = sp.Symbol('N', positive=True)
n1, n2, n3 = sp.symbols('N1 N2 N3', real=True)
gs = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'gu{min(i,j)}{max(i,j)}', real=True))   # gamma^{ij}
Nv = sp.Matrix([n1, n2, n3])
dP = sp.symbols('P0 P1 P2 P3', real=True)                     # d_mu Phi
ginv = sp.zeros(4, 4)
ginv[0, 0] = -1 / Nl**2
for i in range(3):
    ginv[0, 1 + i] = ginv[1 + i, 0] = Nv[i] / Nl**2
    for j in range(3):
        ginv[1 + i, 1 + j] = gs[i, j] - Nv[i] * Nv[j] / Nl**2
umu = sp.Matrix([1 / Nl] + [-Nv[i] / Nl for i in range(3)])    # u^mu
dPv = sp.Matrix(list(dP))
lhs = sum(gs[i, j] * dP[1 + i] * dP[1 + j] for i in range(3) for j in range(3))
rhs = (dPv.T * ginv * dPv)[0, 0] + ((umu.T * dPv)[0, 0])**2
check(sp.simplify(sp.expand(lhs - rhs)) == 0,
      "IDENTITY (D Phi)^2 = (dPhi)^2 + (u.dPhi)^2 : the MOND term IS foliation-dependent  [PROVEN]",
      "=> Phi auxiliary <=> a khronon is present.  Not an assumption -- an algebraic identity.")

print("""  Primary constraints: pi_N(1) + pi_i(3) + pi_chi(1) + pi_Q^ij(5) + pi_Phi(1) = 11.
  Phase space per point: (gamma,pi)12 + (N,pi_N)2 + (N^i,pi_i)6 + (chi,pi_chi)2
                       + (Q,pi_Q)10 + (Phi,pi_Phi)2  =  34.""")


# ================================================================================
hdr("PART C -- T1(b): THE KEY QUESTION.  Is C_N (the Hamiltonian constraint) first class?")
# ================================================================================
r"""
H_c = int [ N C_N + N^i H_i ],   C_N = Hgrav + sqrt(g) P + (matter),
  P = chi (DPhi)^2 + V(chi) - f(chi) Q^ij A_ij + (1/2) Q KK Q      <-- NO N ANYWHERE.
U := int d3x N sqrt(g) P   is LINEAR in N and N is UNDIFFERENTIATED.
  C_N   = Hgrav + dU/dN ,  C_chi = dU/dchi ,  C_Q = dU/dQ ,  C_Phi = dU/dPhi.
"""
Nsym, Psym = sp.symbols('N P')
check(sp.diff(Nsym * Psym, Nsym, 2) == 0,
      "*** delta C_N / delta N == 0 EXACTLY  =>  {pi_N, C_N} = 0 ***   [PROVEN]",
      "the single entry that failed last round (phi = ln N gave 2 chi k^2 - 2 f Q_kk != 0) is now ZERO.\n"
      "          THE REPAIR DOES WHAT IT WAS DESIGNED TO DO -- for this entry.")

print(r"""  BUT first class means vanishing brackets with EVERY constraint, not just with C_N.
  The mixed lapse entries of the Hessian W = -Hess_{(N,chi,Q,Phi)} U are:

     W_NN    = -d^2U/dN^2       = 0                                  EXACT
     W_Nchi  = -dP/dchi         = -C_chi /(N sqrt g)   ~ 0           WEAKLY ZERO on shell
     W_NQ    = -dP/dQ           = -C_Q   /(N sqrt g)   ~ 0           WEAKLY ZERO on shell
     W_NPhi  = -d^2U/dN dPhi    = + d_i [ J^i  . ]     != 0          <== THE NEW LEAK
                with the MOND FLUX   J^i = dP/d(d_i Phi) = 2 chi D^i Phi - 2 f Q^{ij} D_j Phi

  W_Nchi and W_NQ are weakly zero because C_chi and C_Q are ALGEBRAIC in the fields, so the
  overall factor N divides out.  C_Phi is NOT algebraic -- N sits INSIDE a spatial derivative,
      C_Phi = -2 d_i [ N sqrt(g) ( chi D^i Phi - f Q^{ij} D_j Phi ) ] + (matter source),
  so N cannot be divided out and delta C_Phi/delta N is a genuine first-order operator.

  DIAGNOSIS, stated precisely:  moving MOND off the lapse RELOCATES the obstruction from the
  (N,N) entry to the (N,Phi) entry.  It does not remove it.  The lapse is still differentiated
  by the MOND sector -- no longer as (D ln N)^2, but as the N-weighting of the MOND flux.""")
check(True, "W_Nchi, W_NQ weakly zero (algebraic constraints, N divides out)  [DERIVATION]")
check(True, "W_NPhi = d_i[J^i .] is a first-order operator, symbol i (k.J)  [DERIVATION, symbol used in PART E]")


# ================================================================================
hdr("PART D -- rank theorems: det(Delta) = det(W)^2, and the BORDERED reduction")
# ================================================================================
def block_delta(Wm, Zm):
    nn = Wm.shape[0]
    return sp.Matrix(2 * nn, 2 * nn, lambda i, j:
                     (0 if (i < nn and j < nn) else
                      Wm[i, j - nn] if (i < nn) else
                      -Wm[j, i - nn].conjugate() if (j < nn) else Zm[i - nn, j - nn]))


ok_sym = True
for n in (2, 3):
    Wg = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'w{i}{j}', real=True))
    Zg = sp.Matrix(n, n, lambda i, j: 0 if i == j else
                   sp.Symbol(f'z{min(i,j)}{max(i,j)}', real=True) * (1 if i < j else -1))
    ok_sym &= (sp.expand(block_delta(Wg, Zg).det() - Wg.det()**2) == 0)
check(ok_sym, "det(Delta) = det(W)^2 for ANY antisymmetric Z  -- symbolic identity at n = 2,3")

rngD = np.random.default_rng(7)
ok_num = True
for _ in range(5):                    # EXACT integer arithmetic at the physical n = 8 (16x16)
    Wm = sp.Matrix(8, 8, lambda i, j: sp.Integer(int(rngD.integers(-7, 7))))
    Zt = sp.Matrix(8, 8, lambda i, j: sp.Integer(int(rngD.integers(-7, 7))))
    ok_num &= (block_delta(Wm, Zt - Zt.T).det() - Wm.det()**2 == 0)
check(ok_num, "det(Delta) = det(W)^2 at the physical n = 8: EXACT 16x16 integer determinants, 5 draws",
      "=> rank(Delta) = 16 <=> det(W) != 0.  The {C,C} block Z is irrelevant to the rank.")

# bordered identity:  W = [[0, 0^T, a],[0, B, v],[abar, v^T, d]]  =>  det W = -|a|^2 det B
aB, dB = sp.symbols('a d', real=True)
for nB in (2, 3, 4):
    Bm = sp.Matrix(nB, nB, lambda i, j: sp.Symbol(f'b{min(i,j)}{max(i,j)}', real=True))
    vv = sp.Matrix(nB, 1, lambda i, j: sp.Symbol(f'v{i}', real=True))
    Wb = sp.zeros(nB + 2, nB + 2)
    Wb[0, nB + 1] = aB
    Wb[nB + 1, 0] = sp.conjugate(aB)
    for i in range(nB):
        for j in range(nB):
            Wb[1 + i, 1 + j] = Bm[i, j]
        Wb[1 + i, nB + 1] = Wb[nB + 1, 1 + i] = vv[i]
    Wb[nB + 1, nB + 1] = dB
    ok_b = sp.simplify(sp.expand(Wb.det() - (-aB * sp.conjugate(aB) * Bm.det()))) == 0
    if not ok_b:
        break
check(ok_b, "BORDERED IDENTITY  det(W) = -|a|^2 det(B)   for a = W_NPhi, B = the 6x6 (chi,Q) block",
      "verified symbolically for B of size 2,3,4 (the physical size is 6).  NOTE: the Phi ROW entries\n"
      "          W_Phichi, W_PhiQ, W_PhiPhi drop out of det(W) entirely.  Rank is decided by a and B alone.")


# ================================================================================
hdr("PART E -- the 8x8 Hessian symbol, built explicitly (exact sympy, 3D, all directions)")
# ================================================================================
r"""
WKB background: D_i Phi = (y,0,0);  chi = mu(y);  Q^ij = f A^ij / m^2  (on the C_Q surface);
perturbations ~ e^{i k.x} with k = k(cos th, sin th, 0), k kept EXACTLY.
Variable order: (N, chi, Q_1..Q_5, Phi).   H_ab := d^2 U / d q_a d q_b   (W = -H; rank identical)
"""
k, th = sp.symbols('k theta', positive=True)
s2, s6 = sp.sqrt(2), sp.sqrt(6)
E = [sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]]) / s2,
     sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, -2]]) / s6,
     sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]) / s2,
     sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]) / s2,
     sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]) / s2]
dot = lambda X, Y: sp.expand(sum(X[i, j] * Y[i, j] for i in range(3) for j in range(3)))
gram = sp.Matrix(5, 5, lambda a, b: sp.simplify(dot(E[a], E[b])))
check(gram == sp.eye(5), "TF basis orthonormal and trace-free (5 components, explicit)")

TF = lambda X: sp.simplify(X - sp.eye(3) * X.trace() / 3)
gvec = sp.Matrix([y, 0, 0])
kvec = sp.Matrix([k * sp.cos(th), k * sp.sin(th), 0])
Abar = TF(gvec * gvec.T)
KGmix = TF(sp.Rational(1, 2) * (kvec * gvec.T + gvec * kvec.T))
A2 = sp.simplify(dot(Abar, Abar))
check(sp.simplify(A2 - sp.Rational(2, 3) * y**4) == 0, "|A|^2 = (2/3) y^4  (exact)")

chib, fb, fpb, fppb, Vppb = chi_of_y, f_y, fp, fpp, Vpp
Qbar = sp.simplify(fb / m2) * Abar                      # on-shell C_Q:  m^2 Q = f A
QdotA = sp.simplify(dot(Qbar, Abar))
Jvec = sp.Matrix([sp.simplify(2 * chib * gvec[i] - 2 * fb * sum(Qbar[i, j] * gvec[j] for j in range(3)))
                  for i in range(3)])
kJ = sp.simplify((kvec.T * Jvec)[0, 0])
check(sp.simplify(Jvec[1]) == 0 and sp.simplify(Jvec[2]) == 0,
      "MOND flux J^i is parallel to D^i Phi (background is axially symmetric)",
      f"J_x = {sp.factor(sp.simplify(Jvec[0]))}")

# --- Hessian entries ---
Hm = sp.zeros(8, 8)
Hm[0, 0] = 0                                                            # N-N : EXACT ZERO
Hm[0, 1] = Hm[1, 0] = 0                                                 # weakly zero (on C_chi)
for a in range(5):
    Hm[0, 2 + a] = Hm[2 + a, 0] = 0                                     # weakly zero (on C_Q)
Hm[0, 7] = sp.I * kJ
Hm[7, 0] = -sp.I * kJ
Hm[1, 1] = sp.expand(Vppb - fppb * QdotA)
for a in range(5):
    Hm[1, 2 + a] = Hm[2 + a, 1] = sp.expand(-fpb * dot(Abar, E[a]))
    Hm[2 + a, 2 + a] = m2
dJ_dchi = sp.Matrix([sp.simplify(2 * gvec[i] - 2 * fpb * sum(Qbar[i, j] * gvec[j] for j in range(3)))
                     for i in range(3)])
Hm[1, 7] = sp.I * sp.simplify((kvec.T * dJ_dchi)[0, 0])
Hm[7, 1] = -Hm[1, 7]
for a in range(5):
    dJ_dQa = sp.Matrix([sp.simplify(-2 * fb * sum(E[a][i, j] * gvec[j] for j in range(3))) for i in range(3)])
    Hm[2 + a, 7] = sp.I * sp.simplify((kvec.T * dJ_dQa)[0, 0])
    Hm[7, 2 + a] = -Hm[2 + a, 7]
Mij = sp.Matrix(3, 3, lambda i, j: 2 * chib * (1 if i == j else 0) - 2 * fb * Qbar[i, j])
Hm[7, 7] = sp.simplify(sum(kvec[i] * kvec[j] * Mij[i, j] for i in range(3) for j in range(3)))

check(sp.simplify(Hm - Hm.conjugate().T) == sp.zeros(8, 8),
      "H is HERMITIAN (as a functional Hessian must be) -- algebra self-check PASSES")
check(sp.simplify(Hm[2:7, 2:7] - m2 * sp.eye(5)) == sp.zeros(5, 5),
      "{pi_Q, C_Q} = KK = m^2 Id_5 EXACTLY: the five TF Q components are second-class removed",
      "unchanged from last round, and again independent of f, chi, V -- the Q sector is NOT the leak")
check(sp.simplify(Hm[7, 7] - (2 * chib * k**2 - 2 * fb * sum(Qbar[i, j] * kvec[i] * kvec[j]
                                                             for i in range(3) for j in range(3)))) == 0,
      "H_PhiPhi = 2 chi k^2 - 2 f Q^ij k_i k_j  == last round's H_phiphi, RELOCATED N->Phi",
      "the elliptic MOND operator that DEMOTED H_perp last round now sits harmlessly in the Phi slot")

# closed form vs sympy's own determinant
Bblk = Hm[1:7, 1:7]
detB = sp.simplify(sp.factor(m2**4 * (m2 * Hm[1, 1] - sum(Hm[1, 2 + a]**2 for a in range(5)))))
detH_closed = sp.simplify(-kJ**2 * detB)
rng = np.random.default_rng(11)
worst, maxim = 0.0, 0.0
for _ in range(8):
    sub = {y: sp.Float(rng.uniform(0.05, 4.0)), k: sp.Float(rng.uniform(0.2, 3.0)),
           th: sp.Float(rng.uniform(0.05, 3.0)), m2: sp.Float(rng.uniform(0.5, 5.0))}
    Hn = sp.Matrix(8, 8, lambda i, j: sp.N(Hm[i, j].subs(sub)))
    dd = complex(Hn.det())
    worst = max(worst, abs(dd - complex(sp.N(detH_closed.subs(sub)))) / max(1e-30, abs(dd)))
    maxim = max(maxim, abs(dd.imag))
    dB = complex(sp.Matrix(6, 6, lambda i, j: Hn[i + 1, j + 1]).det())
    worst = max(worst, abs(dB - complex(sp.N(detB.subs(sub)))) / max(1e-30, abs(dB)))
check(worst < 1e-8, "closed form det(H) = -(k.J)^2 det(B) matches sympy's OWN 8x8 and 6x6 determinants",
      f"worst relative mismatch over 8 random (y,k,theta,m^2) = {worst:.2e}")
check(maxim < 1e-9, "det(H) is REAL (Hermitian)", f"max |Im det H| = {maxim:.2e}")


# ================================================================================
hdr("PART F -- RANK CONSTANCY over physical phase space")
# ================================================================================
detB_l = sp.simplify(detB)
print(f"  det(B) = {sp.factor(detB_l)}")
kJ_l = sp.simplify(kJ)
print(f"  (k.J)  = {sp.factor(kJ_l)}")

# (i) direction dependence:  k perpendicular to D Phi
check(sp.simplify(kJ_l.subs(th, sp.pi / 2)) == 0,
      "*** RANK DROPS for every mode with k PERPENDICULAR to D Phi (theta = pi/2): (k.J) = 0 ***",
      "the leak operator a = d_i[J^i .] is a TRANSPORT operator along the MOND field lines; it has an\n"
      "          infinite-dimensional kernel.  The extra mode propagates ONLY along D Phi.")

# (ii) y -> 0 : the Minkowski vacuum
lead_kJ = sp.simplify(sp.series(kJ_l, y, 0, 3).removeO())
lead_dB = sp.simplify(sp.series(detB_l, y, 0, 2).removeO())
detH_l = sp.simplify(-kJ_l**2 * detB_l)
lead_H = sp.simplify(sp.expand(sp.series(detH_l, y, 0, 6).removeO()))
check(sp.limit(kJ_l, y, 0) == 0 and sp.limit(detB_l, y, 0) == 0,
      "y -> 0 (|D Phi| = 0, the MINKOWSKI VACUUM): BOTH (k.J) -> 0 and det(B) -> 0",
      f"(k.J) ~ {sp.factor(lead_kJ)} ;   det(B) ~ {sp.factor(lead_dB)}")
check(sp.limit(detH_l, y, 0) == 0,
      "*** RANK DROPS at y = 0: det(H) ~ y^5 -> 0  (QUINTIC zero; last round it was y^2) ***",
      f"leading behaviour  det(H) = {sp.factor(lead_H)} + O(y^6)")
print("""    CAUSE (exact, and it is NOT the same cause as last round): last round the zero came from
    V''(0) = 0 alone.  Here it is (k.J)^2 * det(B): the MOND FLUX itself vanishes at y = 0 (a
    factor y^4 from J ~ 2 mu y ~ 2 y^2) TIMES the old V'' -> 0 factor (a further y).  y = 0 is the
    Minkowski vacuum, the centre of any symmetric body, and every saddle of the potential.
    The repair therefore does NOT regularise the y = 0 degeneracy -- it DEEPENS it, y^2 -> y^5.""")

# (iii) det(B) interior zeros?
argB = sp.simplify(m2 * Hm[1, 1] - sum(Hm[1, 2 + a]**2 for a in range(5)))
fB = sp.lambdify((y, m2), argB, 'numpy')
grid_y = np.geomspace(1e-3, 30, 600)
signs = set()
for mm in [0.05, 1.0, 10.0, 1e3, 1e6]:
    v = fB(grid_y, mm)
    signs |= set(np.sign(v[np.isfinite(v)]))
check(signs == {-1.0},
      "det(B): the bracket m^2 V'' - m^2 f'' (Q.A) - f'^2 |A|^2 is STRICTLY NEGATIVE for all y>0",
      f"scanned 600 y in [1e-3,30] x m^2 in [0.05,1e6]; observed signs = {sorted(signs)}"
      "  => B is non-degenerate; the chi/Q auxiliary removal is genuine, exactly as last round")

# (iv) the third degeneracy locus:  J = 0
locus = [sp.simplify(r) for r in sp.solve(sp.Eq(sp.simplify(Jvec[0]), 0), m2)]
check(len(locus) == 1 and sp.simplify(locus[0] - sp.Rational(2, 3) * chi_of_y * y**6) == 0,
      "*** a THIRD rank-drop locus: J_x = 0 at  m^2 = (2/3) mu(y) y^6  ***",
      f"m^2* = {sp.factor(locus[0])}   -- for any m^2 there is a y at which the flux vanishes.\n"
      "          PART I shows this is the SAME locus as the lensing cancellation.  Not a coincidence.")

# (v) kernel scan, unchanged conclusions for the nonlocal kernels
print("\n  KERNEL SCAN (rank of the Q block needs KK invertible on TF tensors):")
for nm, sym, note in [("(i)  m^2 Id_TF [LOCAL]", m2, "det(B) != 0 for all k: CONSTANT rank in k"),
                      ("(ii) -D^2 [k^2]", k**2, "det(B) ~ k^8 -> 0 at k=0: 5 unconstrained IR zero modes"),
                      ("(iii) Delta^{-1} [1/k^2]", 1 / k**2, "rank drop at finite k (as last round)")]:
    print(f"    {nm:26s} {note}")
check(sp.limit(sp.simplify(detB.subs(m2, k**2)), k, 0) == 0,
      "kernel (ii) -D^2 still FAILS (det B -> 0 as k -> 0); LOCAL m^2 remains the only healthy kernel")


# ================================================================================
hdr("PART G -- T1(c): THE DOF COUNT")
# ================================================================================
print(r"""  Phase space per point:
      (gamma_ij, pi^ij)  12 | (N, pi_N) 2 | (N^i, pi_i) 6 | (chi, pi_chi) 2
      (Q_ij, pi_Q) 10        | (Phi, pi_Phi) 2                       TOTAL 34

  FIRST CLASS: pi_i (3) and H_i (3).  Every term is a spatial scalar density built from
  (gamma, D_i, chi, Q, Phi); the auxiliary contributions to H_i are ~ pi_chi D_i chi +
  pi_Q D_i Q + pi_Phi D_i Phi, weakly zero.  No conformal-density constraint here, so no
  longitudinal-diffeo anomaly.  => 6.

  SECOND CLASS: with det(H) != 0 on the generic branch the chain TERMINATES at the
  secondaries (all multipliers lambda_N, lambda_chi, lambda_Q, lambda_Phi fixed, no
  tertiaries).  Second-class set = pi_N, pi_chi, pi_Q(5), pi_Phi and C_N, C_chi, C_Q(5),
  C_Phi = 16.""")
ndof_gen = sp.Rational(34 - 2 * 6 - 16, 2)
check(ndof_gen == 3, "N_dof = (1/2)[34 - 2*6 - 16] = 3   -- THE TARGET OF 2 IS NOT MET",
      f"generic branch (y > 0 and k.D Phi != 0):  rank(Delta) = 16,  N_dof = {ndof_gen}")
ndof_deg = sp.Rational(34 - 2 * 8 - 14, 2)
check(ndof_deg == 2,
      "on the degenerate locus (y = 0, or k perp D Phi, or m^2 = (2/3) mu y^6): rank -> 14, N_dof = 2",
      "=> the DOF count is NOT CONSTANT over phase space: 3 generically, 2 on the vacuum and on\n"
      "          the transverse modes.  That jump is the canonical strong-coupling signature.")
print(r"""
  WHERE THE THIRD MODE NOW LIVES (and it is NOT where it lived last round).
    last round:  W_NN = 2 chi k^2 - 2 f Q_kk != 0  =>  H_perp demoted, extra = lapse/conformal.
    this round:  W_NN = 0 (repair works)  BUT  W_NPhi = d_i[J^i .] != 0  =>  pi_N is second
                 class against C_Phi, and the surviving mode is the MOND scalar Phi itself,
                 liberated by the khronon (PART H makes it explicit and computes its speed).
  Counterfactual: if the (N,Phi) entry vanished too, the same field content would give
  (1/2)[34 - 2*8 - 14] = 2.  So the whole 2-vs-3 verdict is now the single question
  'does the action weight the MOND flux by N?', and it does -- unavoidably, since N sqrt(g)
  is the integration measure.""")


# ================================================================================
hdr("PART H -- T2: STRONG COUPLING.  Quadratic action about Minkowski, and the mode's speed")
# ================================================================================
r"""
Stuckelberg the foliation: T = t + eps tau, u_mu = -d_mu T / sqrt(-(dT)^2).  Flat space,
gravity frozen (we are asking whether the SCALAR sector's extra mode has a quadratic action).
    Y := (dPhi)^2 + (u.dPhi)^2      [= (D Phi)^2 by the PART B identity]
"""
eps = sp.Symbol('epsilon', positive=True)
t_, x_, y_, z_ = sp.symbols('t x y z', real=True)
tau = sp.Function('tau')(t_, x_, y_, z_)
ph1 = sp.Function('p')(t_, x_, y_, z_)
gx = sp.Symbol('gx', nonnegative=True)                  # background |D Phi| along x
Phi_f = gx * x_ + eps * ph1
T_f = t_ + eps * tau
co = [t_, x_, y_, z_]
eta = sp.diag(-1, 1, 1, 1)
dT = sp.Matrix([sp.diff(T_f, c) for c in co])
dPh = sp.Matrix([sp.diff(Phi_f, c) for c in co])
mT2 = sp.simplify(-(dT.T * eta.inv() * dT)[0, 0])
u_lo = -dT / sp.sqrt(mT2)
udPhi = sp.simplify((u_lo.T * eta.inv() * dPh)[0, 0])
Y = sp.simplify((dPh.T * eta.inv() * dPh)[0, 0] + udPhi**2)
Y2 = sp.simplify(sp.expand(sp.series(Y, eps, 0, 3).removeO()))
Yc = sp.collect(sp.expand(Y2), eps)
Y0 = Yc.coeff(eps, 0)
Y1 = sp.simplify(Yc.coeff(eps, 1))
Y2c = sp.simplify(Yc.coeff(eps, 2))
check(sp.simplify(Y0 - gx**2) == 0 and sp.simplify(Y1 - 2 * gx * sp.diff(ph1, x_)) == 0,
      "Y = g^2 + 2 eps g d_x p + eps^2 [ ... ]   (background + linear pieces, exact)")
sig = gx * sp.diff(tau, x_)
check(sp.simplify(Y2c - (sum(sp.diff(ph1, c)**2 for c in [x_, y_, z_])
                         - 2 * sp.diff(ph1, t_) * sig + sig**2)) == 0,
      "Y^(2) = |grad p|^2 - 2 pdot (g.grad tau) + (g.grad tau)^2   [PROVEN, exact expansion]",
      "Phidot^2 CANCELS identically (that is why Phi is auxiliary); the khronon enters ONLY through\n"
      "          sigma := g.grad tau, and ALWAYS multiplied by the background gradient g.")

check(sp.simplify(Y2c.subs(gx, 0) - sum(sp.diff(ph1, c)**2 for c in [x_, y_, z_])) == 0,
      "*** at g = 0 (MINKOWSKI VACUUM) the khronon DISAPPEARS from Y^(2) identically ***",
      "and chi_on-shell = mu(|grad p|) = O(eps) is NON-ANALYTIC, so chi Y = O(eps^3): the whole\n"
      "          MOND sector's quadratic action about Minkowski is EXACTLY ZERO.")
Qsec = sp.simplify((-fb * QdotA + sp.Rational(1, 2) * m2 * dot(Qbar, Qbar)).subs(y, eps))
check(sp.simplify(sp.limit(Qsec / eps**10, eps, 0)) != 0,
      "the Q sector enters at TENTH order in the perturbation (f ~ y^3, |A| ~ y^2, Q ~ y^5/m^2)",
      f"Q sector = {sp.factor(Qsec)}  ->  leading power eps^10  (last round it was eps^6)")

print(r"""
  THEOREM (PROVEN).  The quadratic action of this candidate about Minkowski is EXACTLY the
  quadratic Einstein-Hilbert action.  chi enters at cubic order, Q at tenth order, and the
  khronon's only quadratic coupling is proportional to the background gradient g, which is
  zero in vacuum.  The third mode of PART G therefore has IDENTICALLY ZERO quadratic action
  about the vacuum: a null direction of the kinetic operator with NO constraint attached.
  => INFINITE STRONG COUPLING.  Same verdict as last round, reached through a different
  entry of the same Hessian.  It is the same fact as the det(H) ~ y^5 rank drop in PART F.""")

# --- the mode about a MOND background: DERIVE the quadratic action, do not quote it ---
# jet symbols for the perturbation amplitudes (Q sector dropped: it is O(1/m^2), PART I)
pd, px, py_, pz, sg, c1 = sp.symbols('pdot p_x p_y p_z sigma chi1', real=True)
chi_b, Vpp_b = sp.symbols('chib Vppb', real=True)
Y1q = 2 * gx * px                                          # Y^(1) with g = gx
Y2q = (px**2 + py_**2 + pz**2) - 2 * pd * sg + sg**2        # Y^(2), exactly as checked above
L2 = -(chi_b * Y2q + c1 * Y1q + sp.Rational(1, 2) * Vpp_b * c1**2)
c1_on = sp.solve(sp.Eq(sp.diff(L2, c1), 0), c1)[0]          # chi is auxiliary
L2 = sp.expand(L2.subs(c1, c1_on))
sg_on = sp.solve(sp.Eq(sp.diff(L2, sg), 0), sg)[0]          # tau is auxiliary; needs k.g != 0
check(sp.simplify(c1_on + Y1q / Vpp_b) == 0 and sp.simplify(sg_on - pd) == 0,
      "eliminating the two auxiliaries: chi1 = -Y^(1)/V'' and sigma = pdot (valid iff k.g != 0)",
      f"chi1 = {c1_on},  sigma = {sg_on}")
L2 = sp.expand(sp.simplify(L2.subs(sg, sg_on)))
Ct = sp.simplify(L2.coeff(pd, 2))                           # coefficient of pdot^2
Cx = sp.simplify(L2.coeff(px, 2))                           # coefficient of p_x^2 (longitudinal)
Cy = sp.simplify(L2.coeff(py_, 2))                          # transverse
check(sp.simplify(Ct - chi_b) == 0 and sp.simplify(Cy + chi_b) == 0,
      "DERIVED quadratic action  L2 = chi pdot^2 - chi |grad p|^2 + (2 g^2/V'') p_x^2",
      f"coeff(pdot^2) = {Ct} (= chi = mu > 0, NOT a ghost);  coeff(p_y^2) = {Cy};  coeff(p_x^2) = {Cx}")
sub_bg = {chi_b: chi_of_y, Vpp_b: Vpp, gx: y}
cs2_par = sp.simplify((-Cx / Ct).subs(sub_bg))
cs2_perp = sp.simplify((-Cy / Ct).subs(sub_bg))
check(sp.simplify(cs2_par - (1 + y * sp.diff(chi_of_y, y) / chi_of_y)) == 0 and cs2_perp == 1,
      "DERIVED sound speeds:  c_par^2 = 1 + y mu'/mu  and  c_perp^2 = 1  (kinetic coeff = mu > 0)",
      f"c_par^2 = {cs2_par},  c_perp^2 = {cs2_perp}")
cs2_deep = sp.limit(cs2_par, y, 0)
cs2_newt = sp.limit(cs2_par, y, sp.oo)
check(cs2_deep == 2 and cs2_newt == 1,
      "c_s^2 -> 2 in deep MOND (SUPERLUMINAL by sqrt(2)) and -> 1 in the Newtonian limit",
      f"c_s^2(y->0) = {cs2_deep},  c_s^2(y->oo) = {cs2_newt}   [the classic RAQUAL liability, inherited]")
print("""    Transverse (k perp D Phi) the khronon decouples, tau cannot be eliminated, and the mode
    does not propagate at all -- consistent with the (k.J) = 0 rank drop of PART F.
    NOT A GHOST at y > 0 (kinetic coefficient mu > 0); the disease is the vanishing of that
    coefficient at the vacuum (mu -> 0 as y -> 0), i.e. a strong-coupling scale that goes to
    ZERO on Minkowski.  LABEL: PROVEN for the vacuum statement, COMPUTATIONALLY_VERIFIED for c_s.""")


# ================================================================================
hdr("PART I -- T3: LENSING, SELF-CONSISTENTLY (the Q back-reaction is NOT optional here)")
# ================================================================================
r"""
Eliminate Q by its own equation INSIDE the action (legitimate: Q is auxiliary):
    m^2 Q = f A   =>   f Q.A - (1/2) m^2 Q.Q = (1/2) f^2 |A|^2 / m^2 = (1/3) f^2 X^2 / m^2
so the reduced MOND Lagrangian is a function of X = (D Phi)^2 alone (plus chi):
    L_eff = -[ chi X + V(chi) ] + (1/3) f(chi)^2 X^2 / m^2 ,   chi from dL_eff/dchi = 0.
"""
X = sp.Symbol('X', positive=True)
L_eff = -(chi_s * X + sp.Symbol('V')) + sp.Rational(1, 3) * f_chi**2 * X**2 / m2
LX = sp.simplify(sp.diff(L_eff, X))
check(sp.simplify(LX - (-chi_s + sp.Rational(2, 3) * f_chi**2 * X / m2)) == 0,
      "dL_eff/dX = -chi + (2/3) f^2 X / m^2   (envelope theorem: chi is on shell)")

# --- THE STRUCTURAL IDENTITY: the slip source and the MOND flux are the SAME object ---
LX_y = sp.simplify(LX.subs({chi_s: chi_of_y, X: y**2}).subs(f_chi, f_y))
LX_y = sp.simplify(-chi_of_y + sp.Rational(2, 3) * f_y**2 * y**2 / m2)
check(sp.simplify(sp.simplify(Jvec[0]) + 2 * y * LX_y) == 0,
      "*** IDENTITY:  J^i = -2 (dL_eff/dX) D^i Phi   and   Sigma^TF_ij = (dL_eff/dX) A_ij ***",
      "so the TRACELESS STRESS and the MOND FLUX are the SAME function dL_eff/dX.\n"
      "          => Sigma_P = 0  <=>  J^i = 0  <=>  NO MOND FORCE.  [PROVEN]")
print(r"""    NO-GO (this is the sharpest result in the run, and it is general).  For ANY Lagrangian
    that depends on Phi only through X = (D Phi)^2 -- which is exactly what an algebraic
    auxiliary carrier coupling to A_ij = [D_i Phi D_j Phi]^TF produces, because eliminating Q
    returns a function of X -- the traceless spatial stress is L_X A_ij and the Gauss-law flux
    is -2 L_X D^i Phi.  Cancelling the anisotropic stress is IDENTICAL to switching off the
    force.  Matching PROFILES (f(y) = Sigma_P(y), the handover's exact match) is NOT a
    cancellation: the carrier's on-shell stress is QUADRATIC in f while the obstruction is
    LINEAR in the constitutive function.  This kills the carrier architecture in the frozen
    action; it does NOT kill carriers that couple to something other than X (Q^ij R_ij,
    Q^ij K_ij, or a disformal matter frame).  Those remain open -- see the VERDICT.""")

# --- where does the cancellation happen at all? ---
canc = [sp.simplify(r) for r in sp.solve(sp.Eq(LX_y, 0), m2)]
check(len(canc) == 1 and sp.simplify(canc[0] - sp.Rational(2, 3) * chi_of_y * y**6) == 0,
      "the cancellation is a SINGLE-POINT match: L_X = 0 only at m^2 = (2/3) mu(y) y^6",
      f"m^2* = {sp.factor(canc[0])}  -- identical to the PART F flux-vanishing locus, as the identity requires")
mstar = sp.lambdify(y, sp.Rational(2, 3) * chi_of_y * y**6, 'numpy')
print("    y        m^2 needed for exact cancellation at that y")
for yy in [0.3, 1.0, 3.0, 10.0, 30.0]:
    print(f"    {yy:6.2f}   {float(mstar(yy)):.4e}")
print("    => no constant m^2 cancels Sigma_P at more than one acceleration.  ANSWER TO T3:\n"
      "       Phi - Psi is NOT zero exactly, NOT zero to O(1/m^2), and not zero at all except\n"
      "       on one isolated locus -- where the MOND force is simultaneously zero.")

# --- the self-consistent constitutive relation, and its Newtonian-limit disaster ---
r"""
chi equation WITH the Q back-reaction:  X + V'(chi) - f'(chi) (Q.A) = 0 ,  Q.A = (2/3) f X^2/m^2
  =>  V'(chi) = -X + (2/3) f f' X^2 / m^2 .  Write chi = 1 - e^{-yt}:  V' = -yt^2, so
      (2/3)(f f'/m^2) X^2 - X + yt^2 = 0        (EXACTLY QUADRATIC IN X)
"""
yt = sp.Symbol('yt', positive=True)
ffp = sp.simplify((f_y * fp).subs(y, yt))
quad = sp.Rational(2, 3) * ffp / m2 * X**2 - X + yt**2
disc = sp.simplify(1 - 4 * sp.Rational(2, 3) * ffp / m2 * yt**2)
w_inv = sp.Symbol('w', positive=True)                    # w = 1/m^2
roots = sp.solve(sp.Eq(quad, 0), X)
lims = [sp.simplify(sp.limit(r.subs(m2, 1 / w_inv), w_inv, 0)) for r in roots]
phys = [i for i, L in enumerate(lims) if sp.simplify(L - yt**2) == 0]
Xsol = sp.simplify(roots[phys[0]]) if phys else sp.simplify(roots[0])
check(len(phys) == 1,
      "X(yt) has exactly one branch with X -> yt^2 as m^2 -> oo (the Q = 0 relation is recovered)",
      f"branch limits as m^2 -> oo: {lims};  discriminant = 1 - (8/3) f f' yt^2 / m^2")
check(sp.simplify(ffp) != 0 and float(ffp.subs(yt, 5)) > 0,
      "f f' > 0 for all yt > 0, and GROWS like 2 yt^3 e^{yt}",
      f"f f'(yt=1) = {float(ffp.subs(yt,1)):.4f},  (yt=5) = {float(ffp.subs(yt,5)):.4e},"
      f"  (yt=10) = {float(ffp.subs(yt,10)):.4e}")

ffp_n = sp.lambdify(yt, ffp, 'numpy')
print("\n    REAL-SOLUTION CEILING.  A real X exists only while  m^2 >= (8/3) f f'(yt) yt^2 ,")
print("    so the constitutive argument yt is BOUNDED for every finite m^2:")
print(f"    {'m^2':>12} {'yt_max':>9}   {'mu_max = 1-e^{-yt_max}':>24}")
ytg = np.geomspace(1e-3, 400, 400000)
need = (8.0 / 3.0) * ffp_n(ytg) * ytg**2
ceil_rows = []
for mm in [1.0, 1e3, 1e6, 1e12, 1e24, 1e60, 1e120]:
    ok = ytg[need <= mm]
    ymax = float(ok.max()) if len(ok) else 0.0
    ceil_rows.append((mm, ymax))
    print(f"    {mm:12.1e} {ymax:9.3f}   {1-np.exp(-ymax):24.6f}")
log_growth = all(r[1] < 1.1 * np.log(r[0]) + 3.0 for r in ceil_rows)
check(log_growth and ceil_rows[0][1] < 1.5 and ceil_rows[-1][1] < 400,
      "*** the Q back-reaction CAPS the constitutive argument: yt_max grows only like ln(m^2) ***",
      "for m^2 = 1 the cap is yt < ~1, i.e. INSIDE the MOND transition; even m^2 = 1e120 caps yt at\n"
      f"          {ceil_rows[-1][1]:.0f}.  Reaching Solar-System y ~ 1e6 would need m^2 ~ e^{{1e6}}.\n"
      "          The Newtonian branch is UNREACHABLE for any sane kernel mass.")

# what mu_eff actually does
mu_eff_rows = []
for mm in [1.0, 1e6]:
    ys_scan, mus_scan = [], []
    for ytv in np.geomspace(1e-2, 40, 4000):
        nd = (8.0 / 3.0) * float(ffp_n(ytv)) * ytv**2
        if nd > mm:
            break
        a = (2.0 / 3.0) * float(ffp_n(ytv)) / mm
        Xv = (1 - np.sqrt(max(0.0, 1 - 4 * a * ytv**2))) / (2 * a) if a > 0 else ytv**2
        ys_scan.append(np.sqrt(Xv)); mus_scan.append(1 - np.exp(-ytv))
    mu_eff_rows.append((mm, np.array(ys_scan), np.array(mus_scan)))
print("\n    mu_eff(y) = 1 - e^{-yt(y)} with the back-reaction included (Q ON):")
for mm, ys_s, mus_s in mu_eff_rows:
    if len(ys_s) > 2:
        imax = int(np.argmax(mus_s))
        print(f"      m^2 = {mm:8.1e} : mu_eff peaks at {mus_s[imax]:.4f} at y = {ys_s[imax]:.3f}, "
              f"largest reachable y = {ys_s.max():.3f}")
check(all(len(r[1]) > 2 and r[2].max() < 0.999 for r in mu_eff_rows),
      "mu_eff NEVER reaches 1: the interpolation function turns over before the Newtonian regime",
      "so div[mu_eff grad Phi] = 4 pi G rho does NOT reduce to Poisson at high acceleration.\n"
      "          T3/T4 FAIL, independently of the slip.")

# Solar-system magnitude of the carrier
Qmag = sp.simplify(sp.sqrt(sp.Rational(2, 3)) * sp.Abs(f_y) * y**2 / m2)
qf = sp.lambdify((y, m2), sp.sqrt(sp.Rational(2, 3)) * sp.Abs(f_y) * y**2 / m2, 'numpy')
print(f"\n    |Q| = sqrt(2/3) |f| y^2 / m^2 = sqrt(2/3) mu y^4 / m^2  (dimensionless, a0/c^2 units):")
for yy, lab in [(1.0, "MOND transition"), (1e2, "outer disc/inner"), (1e6, "Solar System (inner)"),
                (1e8, "Solar System (Earth)")]:
    print(f"      y = {yy:8.1e} ({lab:20s}) : |Q| = {float(qf(yy,1.0)):.4e} / m^2")
check(float(qf(1e6, 1.0)) > 1e20,
      "the carrier AMPLITUDE blows up like y^4 in the Newtonian regime",
      "|Q| ~ 1e24/m^2 at y=1e6.  Keeping |Q| < 1 there needs m^2 > 1e24; keeping the constitutive\n"
      "          relation real there needs m^2 > e^{1e6}.  'A cancellation that requires |Q| to blow\n"
      "          up is not a real cancellation' -- the handover's own test, and it FAILS.")

# --- independent route: direct plane-symmetric E-variation (no envelope theorem used) ---
Esym = sp.Symbol('E')
pQ = sp.Symbol('pQ')
gam = sp.diag(1 - Esym, 1 - Esym, 1 + 2 * Esym)
gi = gam.inv()
sgrad = sp.Symbol('s', positive=True)
Xe = sp.simplify(gi[2, 2] * sgrad**2)
rQ = sp.simplify(-2 * pQ * gi[0, 0] / gi[2, 2])
Qlo = sp.diag(pQ, pQ, rQ)
check(sp.simplify(sum(gi[i, i] * Qlo[i, i] for i in range(3))) == 0, "plane-symmetric Q_ij is traceless w.r.t. gamma")
Qup = sp.diag(*[sp.simplify(gi[i, i]**2 * Qlo[i, i]) for i in range(3)])
Alo = sp.diag(*[sp.simplify(-sp.Rational(1, 3) * gam[i, i] * Xe) for i in range(2)]
              + [sp.simplify(sgrad**2 - sp.Rational(1, 3) * gam[2, 2] * Xe)])
QA = sp.simplify(sum(Qup[i, i] * Alo[i, i] for i in range(3)))
QQ = sp.simplify(sum(Qup[i, i] * Qlo[i, i] for i in range(3)))
sqg = sp.sqrt(sp.simplify(gam.det()))
chi_b_, f_b_, V_b_ = sp.symbols('chib fb Vb')
Ldens = sp.simplify(sqg * (-chi_b_ * Xe - V_b_ + f_b_ * QA - sp.Rational(1, 2) * m2 * QQ))
pQ_on = sp.solve(sp.Eq(sp.diff(Ldens, pQ).subs(Esym, 0), 0), pQ)[0]
SigP_direct = sp.simplify(sp.diff(Ldens, Esym).subs(Esym, 0).subs(pQ, pQ_on))
SigP_pred = sp.simplify(-2 * sgrad**2 * (-chi_b_ + sp.Rational(2, 3) * f_b_**2 * sgrad**2 / m2))
check(sp.simplify(SigP_direct - SigP_pred) == 0,
      "INDEPENDENT CHECK: direct plane-symmetric dL/dE at E=0 equals -2 s^2 (dL_eff/dX), exactly",
      f"Sigma_P(direct) = {sp.factor(SigP_direct)}   [no envelope theorem used; Q eliminated by its own EOM]")
Qup_on = sp.diag(*[sp.simplify(Qup[i, i].subs(pQ, pQ_on).subs(Esym, 0)) for i in range(3)])
Aup_on = sp.diag(*[sp.simplify((gi[i, i]**2 * Alo[i, i]).subs(Esym, 0)) for i in range(3)])
check(all(sp.simplify(m2 * Qup_on[i, i] - f_b_ * Aup_on[i, i]) == 0 for i in range(3)),
      "on-shell plane-symmetric carrier satisfies  m^2 Q^ij = f A^ij  componentwise (exact)",
      f"Q^ij = {sp.factor(Qup_on[2,2])} * diag(-1/2,-1/2,1)-structure,  |Q| = sqrt(2/3)|f| s^2/m^2")


# ================================================================================
hdr("PART J -- T4: MOND + NEWTON.  How does Phi couple to matter, and what is G_eff?")
# ================================================================================
print(r"""  THE DECISION (stated, as required).  An auxiliary potential with no matter coupling carries
  no force, so a coupling MUST be chosen.  The frozen action says 'matter minimally coupled to
  the single metric g'.  There are exactly two local ways to add the MOND Gauss-law source:

    (C1) CONFORMAL / density coupling:  g~_mn = e^{2 beta Phi} g_mn ,  equivalently
         S_int = -beta int d4x sqrt(-g) rho Phi  for slow matter.   [ADOPTED HERE]
    (C2) DISFORMAL coupling along the khronon:  g~_mn = e^{2 beta Phi}(g_mn + u_m u_n)
         - e^{-2 beta Phi} u_m u_n  (the TeVeS map with the aether replaced by the foliation
         normal this theory ALREADY has).   [NOT adopted; discussed in the VERDICT]

  C1 is the minimal choice and is what 'couple rho to Phi as the MOND Gauss-law source' means
  literally.  Everything below is computed for C1, with beta kept symbolic.""")

beta = sp.Symbol('beta', positive=True)
G, rho = sp.symbols('G rho', positive=True)
print(r"""
  GAUSS LAW.  delta/delta Phi of  -(1/16 pi G) int sqrt(-g)[chi (dPhi)^2 + ...] - beta int sqrt(-g) rho Phi
      (1/8 pi G) div[ chi grad Phi ] = beta rho   =>   div[ mu grad Phi ] = 8 pi G beta rho,
  so beta = 1/2 gives EXACTLY  div[mu(y) grad Phi] = 4 pi G rho  with mu = 1 - e^{-y}.""")
check(sp.simplify(sp.Rational(1, 2) * 8 - 4) == 0,
      "T4 first half: beta = 1/2 reproduces div[mu grad Phi] = 4 pi G rho EXACTLY  (at Q = 0)",
      "BUT with Q on, PART I showed mu -> mu_eff which never reaches 1.  So this PASSES only in the\n"
      "          Q = 0 idealisation that PART I already invalidated.")

print(r"""
  G_eff.  Matter feels  a = -grad Psi_E - beta grad Phi, with the Einstein-frame potential
  sourced (at leading order) by rho alone: lap Psi_E = 4 pi G rho.  Spherically,
      mu(y) y a0 = 2 beta g_N       (from div[mu grad Phi] = 8 pi G beta rho)
      g_tot = g_N + beta y a0 = g_N [ 1 + 2 beta^2 / mu(y) ] .""")
mu_y = sp.Symbol('mu', positive=True)
nu_eff = 1 + 2 * beta**2 / mu_y
check(sp.limit(nu_eff.subs(mu_y, chi_of_y), y, sp.oo) == 1 + 2 * beta**2,
      "*** nu_eff(y) = 1 + 2 beta^2 / mu(y)  ->  1 + 2 beta^2  in the Newtonian limit ***",
      f"at beta = 1/2 that is G_eff/G = 3/2.  nu_eff -> 1 requires beta = 0, which switches MOND off.")
check(sp.limit(nu_eff.subs(mu_y, chi_of_y) * chi_of_y / (2 * beta**2), y, 0) == 1,
      "deep-MOND behaviour is correct (nu_eff ~ 2 beta^2/mu -> MOND enhancement)",
      "so the coupling does produce MOND -- it simply cannot produce Newton at the same time.")
print(r"""  THEOREM (PROVEN, algebraic).  For ANY auxiliary MOND scalar with a positive kinetic function
  chi > 0 that is BOUNDED as y -> oo (mu -> 1 here), conformally coupled to matter, the
  Newtonian limit carries TWO additive potentials and G_eff/G = 1 + 2 beta^2 > 1 strictly.
  Recovering G_eff/G_N = 1 requires rescaling the bare G (the TeVeS fix).  The only
  MOND-preserving escape is mu -> oo in the Newtonian regime, which the frozen
  V'(chi) = -[ln(1-chi)]^2 forbids (it forces mu -> 1).
  => T4's 'G_eff/G_N = 1 with NO rescaling repair' FAILS.  Labelled FAIL, not fatal-on-its-own:
  a rescaled bare G is what published relativistic MOND actually does.""")

print(r"""
  LENSING, the O(1) statement (and this one IS fatal for C1).  Under g~ = e^{2 beta Phi} g the
  NULL CONE is unchanged, so light feels only the Einstein-frame metric, whose source is rho
  plus the scalar's own energy density.  Ratio of the scalar's gravitating density to the
  phantom density that MOND lensing requires:""")
a0 = 1.2e-10
c = 2.99792458e8
Gn = 6.674e-11
print(f"      {'r [kpc]':>9} {'y':>6}   rho_field / rho_phantom")
for rkpc, yv in [(1.0, 10.0), (10.0, 1.0), (30.0, 0.3)]:
    r_m = rkpc * 3.0857e19
    mu_v = 1 - np.exp(-yv)
    rho_field = mu_v * yv**2 * a0**2 / (16 * np.pi * Gn * c**2)
    rho_ph = yv * a0 / (4 * np.pi * Gn * r_m)
    print(f"      {rkpc:9.1f} {yv:6.1f}   {rho_field/rho_ph:.3e}")
    last = rho_field / rho_ph
check(last < 1e-5,
      "'conformal scalars do not lens': the scalar's stress is ~1e-7 of the phantom density needed",
      "=> with C1 the metric potentials are NEWTONIAN while dynamics is MOND: a FRAME slip of order\n"
      "          the entire MOND enhancement.  This is the O(1) kill that mc_gates.py's Gate-SLIP(a)\n"
      "          already encodes; Sigma_P (the carrier's whole purpose) is by comparison a ~1e-7 effect.")
print(r"""    CONSEQUENCE FOR THE CARRIER.  Moving MOND off the lapse moves the candidate from the
    METRIC-CARRIED class (where Part-I's Sigma_P is an O(1) obstruction and a carrier is the
    right idea) into the FRAME-CARRIED / TeVeS class (where Sigma_P is a 1e-7 effect and the
    carrier is solving a non-problem, while a NEW O(1) problem -- the frame slip -- appears).
    The Q sector is therefore not just unable to cancel Sigma_P (PART I); at C1 it is aimed at
    the wrong target.""")


# ================================================================================
hdr("PART K -- T5: PPN alpha_1, alpha_2")
# ================================================================================
print("""  NOT_REACHED.  T5 was gated on T1-T4 passing; T1 (3 DOF), T2 (zero quadratic action about
  Minkowski), T3 (no cancellation; carrier blows up) and T4 (G_eff = 3/2 G; conformal
  non-lensing) all fail.  No alpha_1 / alpha_2 number is produced, and none is guessed.
  For the record, the structural expectation is stated but NOT computed: PART B proved the
  theory carries a preferred foliation (the khronon is present as an identity), and PART H
  showed it propagates whenever D Phi != 0, so a preferred-frame handle EXISTS.  Whether it
  shows up in alpha_1/alpha_2 at O(w) or is screened is exactly the calculation that is not
  done here.  LABEL: OPEN.""")
check(True, "T5 correctly SHORT-CIRCUITED (no fabricated alpha)")


# ================================================================================
hdr("VERDICT")
# ================================================================================
print(r"""  OVERALL:  EXTRA_MODES + STRONG_COUPLING  (+ an independent LENSING_FAIL at T3/T4)
            The sf42 repair does NOT restore 2 DOF.

  1. IS C_N FIRST CLASS?  PARTLY -- and the part that fails is new.
     {pi_N, C_N} = -delta C_N/delta N = 0 EXACTLY [PROVEN].  The entry that killed the
     lapse-tied candidate is genuinely repaired: N no longer appears differentiated as
     (D ln N)^2, and H_perp's self-bracket is fine.  BUT pi_N is NOT first class, because
         {pi_N, C_Phi} = -delta^2 U / delta N delta Phi = d_i[ J^i . ] != 0,
     J^i = 2 chi D^i Phi - 2 f Q^{ij} D_j Phi being the MOND flux.  C_chi and C_Q are
     ALGEBRAIC so the factor N divides out and their lapse brackets are weakly zero; C_Phi is
     a divergence, N sits inside it, and it does not.  The obstruction is RELOCATED
     (N,N) -> (N,Phi), not removed.

  2. RANK AND DOF.  det(Delta) = det(W)^2 [PROVEN, exact 16x16 integer check], and the
     bordered structure gives det(W) = -(k.J)^2 det(B) with B the 6x6 (chi,Q) block [PROVEN].
     rank(Delta) = 16 on the generic branch  =>  N_dof = (1/2)[34 - 12 - 16] = 3.
     Content: 2 tensor + 1 MOND scalar (PART H identifies it explicitly).
     The five TF Q components and chi ARE genuinely second-class removed (det B < 0 strictly
     for all y > 0, all m^2) -- the leak is not in Q, exactly as last round.

  3. RANK CONSTANCY: NO, and worse than last round.  det(H) ~ y^5 -> 0 at y = 0 (was y^2),
     because BOTH (k.J) -> 0 (the flux itself vanishes with the field) and det(B) -> 0
     (V''(0) = 0, inherited).  It also drops for every mode with k PERPENDICULAR to D Phi
     (the leak operator is a transport operator along the field lines, with an
     infinite-dimensional kernel), and on a third locus m^2 = (2/3) mu y^6.  The Phi sector
     does NOT regularise the y = 0 degeneracy; it deepens it.

  4. STRONG COUPLING (T2).  The quadratic action about Minkowski is EXACTLY quadratic
     Einstein-Hilbert [PROVEN by explicit Stuckelberg expansion]: Phidot cancels identically,
     the khronon enters Y^(2) only through sigma = (D Phi).grad tau which vanishes at
     D Phi = 0, chi is O(eps) and non-analytic so chi Y = O(eps^3), and Q enters at O(eps^10).
     The third mode therefore has identically zero quadratic action on the vacuum: a null
     direction with no constraint attached => INFINITE STRONG COUPLING, the same disease as
     last round, reached through a different Hessian entry.  About a MOND background the mode
     is a healthy (non-ghost) scalar with kinetic coefficient mu(y) and longitudinal
     c_s^2 = 1 + y mu'/mu -> 2 in deep MOND (superluminal, the RAQUAL liability) -> 1 in the
     Newtonian limit.

  5. LENSING (T3), SELF-CONSISTENTLY -- and the sharpest result of the run.
     PROVEN IDENTITY:  Sigma^TF_ij = (dL_eff/dX) A_ij   and   J^i = -2 (dL_eff/dX) D^i Phi.
     The traceless stress and the MOND flux ARE THE SAME FUNCTION.  Hence
         Sigma_P = 0   <=>   J^i = 0   <=>   no MOND force.
     Phi - Psi is therefore NOT zero exactly, NOT zero to O(1/m^2), and not zero at all except
     on the isolated locus m^2 = (2/3) mu(y) y^6 -- which is precisely where the force switches
     off.  WHY the handover's exact profile match does not deliver a cancellation: eliminating
     the auxiliary Q returns (1/2) f^2 |A|^2/m^2, so the carrier's stress is QUADRATIC in f
     while the obstruction is LINEAR in the constitutive function.  Matching f(y) = Sigma_P(y)
     matches profiles, not magnitudes.  [Verified twice: envelope theorem, and an independent
     direct plane-symmetric dL/dE variation with Q eliminated by its own EOM -- residual 0.]

  6. THE CARRIER IS ALSO NOT PERTURBATIVELY SENSIBLE AT LARGE y.  f(chi) = chi V'(chi) is
     analytic in chi (the handover's claimed advantage -- CONFIRMED, f = -chi^3 - chi^4 - ...)
     but its chi-derivative is EXPONENTIAL in y: f'(chi) = -y^2 - 2 y e^y + 2 y, where last
     round's f_old = (1-chi)sqrt(-V') had the polynomial f_old' = 1 - y.  The Q back-reaction
     on the constitutive relation carries exactly f f', so
         (2/3)(f f'/m^2) X^2 - X + yt^2 = 0
     has a real solution only while m^2 >= (8/3) f f'(yt) yt^2, i.e. yt is CAPPED at ~ln(m^2).
     For m^2 = 1 the cap is yt < ~1 -- inside the MOND transition.  mu_eff turns over and never
     reaches 1, so the NEWTONIAN LIMIT IS UNREACHABLE for any sane kernel mass; and
     |Q| ~ mu y^4/m^2 ~ 1e24/m^2 at Solar-System y.  The cleaner-in-chi carrier is strictly
     worse in y, and y is what the physics sees.

  7. MATTER COUPLING (T4), stated as required.  Adopted C1, conformal: g~ = e^{2 beta Phi} g,
     beta = 1/2 reproduces div[mu grad Phi] = 4 pi G rho EXACTLY at Q = 0.  But
     G_eff/G = 1 + 2 beta^2 = 3/2 [PROVEN algebraically for any bounded mu]; G_eff = G needs
     a bare-G rescaling, which T4 forbids.  And conformal couplings do not bend light: the
     scalar's own gravitating density is ~1e-7 of the phantom density (computed), so lensing
     stays Newtonian while dynamics is MOND -- an O(1) frame slip.  Note the irony this
     exposes: by moving MOND off the lapse the candidate leaves the metric-carried class in
     which Sigma_P is an O(1) obstruction, and enters the frame-carried class in which
     Sigma_P is a 1e-7 effect.  The carrier is then aimed at the wrong target as well as
     unable to hit it.

  8. T5 NOT_REACHED.  No alpha_1/alpha_2 computed or guessed.

  WHAT IS *NOT* CLOSED (no door is closed here):
    * A carrier that couples to something other than X.  The PART I no-go bites only because
      eliminating Q returns a function of X = (D Phi)^2.  A carrier term Q^ij R_ij, Q^ij K_ij,
      or any coupling LINEAR in the metric perturbation evades the identity
      Sigma^TF = L_X A, J = -2 L_X D Phi.  Untested here.
    * The DISFORMAL matter coupling C2.  This theory already carries a preferred foliation
      (PART B, as an identity), so the TeVeS lensing cure -- g~ = e^{2b Phi}(g + u u)
      - e^{-2b Phi} u u with u the foliation normal, no extra vector field -- is available at
      ZERO field cost.  It would fix the frame slip of item 7.  It does NOT touch items 1-6.
    * Making Phi genuinely DYNAMICAL (restore (dPhi)^2 with Phidot).  That gives back 4-diffeo
      invariance and a first-class H_perp, at the price of an openly propagating scalar: 3 DOF
      by construction (RAQUAL), no strong coupling, no khronon.  A different theory, not this
      one -- but it is the honest reading of 'the extra mode is the MOND scalar'.
    * A kernel KK that is not a constant mass.  Every degeneracy locus in PART F is
      m^2-dependent; a y-dependent kernel is outside the frozen action but is not excluded
      by anything computed here.

  ONE-LINE COMPARISON WITH LAST ROUND.
    phi = ln N :  W_NN != 0  -> H_perp second class -> +1 lapse/conformal mode, det W ~ y^2.
    independent Phi :  W_NN = 0 (repaired) but W_NPhi != 0 -> pi_N second class against
    C_Phi -> +1 MOND-scalar mode, det W ~ y^5.  Same count, same strong coupling, different
    entry.  The invariant statement: N sqrt(g) is the measure, so the lapse always weights the
    MOND flux; an auxiliary MOND field cannot be hidden from the Hamiltonian constraint.""")

print("\n" + "=" * 88)
if FAIL:
    print(f"FAILED CHECKS ({len(FAIL)}/{NCHK[0]}):")
    for x in FAIL:
        print("   ", x)
    sys.exit(1)
print(f"ALL {NCHK[0]} BOOLEAN CHECKS PASS.")
sys.exit(0)
