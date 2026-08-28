#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_alpha2_preferred_frame_2026.py
=================================================================================
FC-FINAL (AeST + frozen J_10) PREFERRED-FRAME PPN: alpha_1, alpha_2 DERIVED from the
AeST field equations with a moving source (aether boosted by velocity w), NOT imported
from Einstein-aether or khronometric formulas.

MISSION DISCIPLINE (Carl):
  - Do NOT import EA/khronon PPN formulas; DERIVE the map from the FC-FINAL action.
  - Every load-bearing number carries a sympy simplify(...)==0 certificate.
  - alpha_2 may end OPEN (bounded-but-uncomputed); say so honestly if so.

ACTION (frozen, arXiv:2007.00082 Eq.5; mostly-plus eta=diag(-1,1,1,1)):
  S = int (sqrt(-g)/16 pi Gt)[ R - 2 Lambda - (K_B/2)F_{mn}F^{mn} + 2(2-K_B)J^m d_m phi
        - (2-K_B)Y - F(Y,Q) - lambda(A^m A_m + 1) ] + S_m
  Q = A^m d_m phi,  Y = (g^{mn}+A^m A^n)d_m phi d_n phi,  F_{mn}=2 d_[m A_n], J^m=A^n d_n A^m.
  F(Y,Q) = (2-K_B) Jcal(Y) + K(Q),  K(Q)=-2Lambda+K2 (Q-Q0)^2  (SZ21 quadratic).
  Jcal = MOND free function; J_Y=dJcal/dY carried as an inert symbol (the frozen mu_10
  kernel enters ONLY through J_Y, and at Solar-System accelerations J_Y->1 -- kernel-blind).

METHOD (two-parameter expansion, following the *validated* pipelines in
  real_research/reviews/typeII_direct_variation_2026.py  (covariant AeST assembly, static
      sector: gamma=1, 00-eq with Ghat=Gt/(1-K_B/2), m_Psi^2=K2 Q0^2/(2-K_B))
  qwen_claude_field_theory/theory_2026/first_principles/sec11_alpha12_preferred_frame.py
      (boosted-background Fourier solve -> alpha_1,alpha_2 -- KHRONON, template only)):
  * eps  = metric/field perturbation (Newtonian potential U ~ eps).
  * wb   = boost of the aether background relative to the source rest frame (preferred-frame w).
  * Aether background boosted:  A^m_bg=(S0, wb w^i), S0=sqrt(1+wb^2 w.w), A_m A^m=-1 exactly.
  * Scalar background aligned:  d_m phi_bg = -Q0 A_m_bg  => Q=Q0, Y=0 on background (certified).
  * Expand the covariant Lagrangian to O(eps^2) and O(wb^2); Fourier plane wave e^{i k.x};
    solve the scalar (chi) and spatial-aether (a_i) EOMs on the Newtonian seed; solve the
    Einstein response for h_0i (O(wb^1)) and h_00 (O(wb^2)); read off, in the standard PPN
    source-at-rest / frame-moving normalisation (Will 4.2):
        h_0i = (alpha_1/2) w_i U  - alpha_2 w_j (d_i d_j chi_U),   lap chi_U = U
        h_00 (w^2 sector) = ... - alpha_2 (w.x/r)^2-type structure.
  All PPN extraction identities are the SAME position<->Fourier dictionary certified in sec11.

EXIT 0 iff every numbered certificate passes.  alpha_2 verdict printed explicitly.

STATUS (2026-08-28): WORK-IN-PROGRESS, DOES NOT CLOSE.  Certificates [A*],[B1],[C3-C6] PASS
(boosted background, unit constraint, gamma_PPN=1, type-II static 00-eq reproduced, w-sectors
solve).  But [D1] alpha_1 != -4K_B and [D2] the two g_00 extractions of alpha_2 DISAGREE under
the reduced ISOTROPIC spatial ansatz h_ij=-2Phi*delta_ij.  Reason (see FINAL_PPN.md): the aether
sources an ANISOTROPIC spatial stress at O(w^2); the traceless-ij equations are then non-trivial
and the isotropic ansatz cannot satisfy them -> the extracted alpha's are NOT a valid solution and
are WITHHELD.  The fix is the full generic (anisotropic-h_ij / harmonic-gauge) metric solve.
The rigorous, certified results live in fc_ctensor_map_2026.py (alpha_1=-4K_B, c123=0 theorem).
"""
import sympy as sp
import time

T0 = time.time()
P = lambda *a: print(*a, flush=True)
FAIL = []
NCH = [0]
def check(cond, label, detail=""):
    NCH[0] += 1
    ok = bool(cond)
    P(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok

# ---------------------------------------------------------------- coordinates & params
t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
CO = [t, x1, x2, x3]
SPC = [x1, x2, x3]
eps, wb = sp.symbols('eps w_b', positive=True)
KB, Q0, K2, LAM, GT, rhoh, JY = sp.symbols('K_B Q_0 K_2 Lambda G_t rhohat J_Y', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
WV = [w1, w2, w3]
eta = sp.diag(-1, 1, 1, 1)
I = sp.I

def tr(e, p, n):
    """truncate polynomial in p at degree n"""
    e = sp.expand(e)
    return sum(e.coeff(p, k) * p**k for k in range(n + 1))

def trew(e):
    """truncate at eps^2 and wb^2"""
    e = sp.expand(e)
    out = 0
    for i in range(3):
        for j in range(3):
            out += e.coeff(eps, i).coeff(wb, j) * eps**i * wb**j
    return sp.expand(out)

# ================================================================ [A] backgrounds
P("="*90); P("[A] boosted backgrounds: aether A^m_bg=(S0, wb w^i), phi aligned"); P("="*90)
ww = w1**2 + w2**2 + w3**2
# S0 expanded polynomially in wb to O(wb^2) (exact sqrt would defeat wb-truncation)
S0 = 1 + wb**2*ww/2
Aup_bg = sp.Matrix([S0, wb*w1, wb*w2, wb*w3])
Adn_bg = eta*Aup_bg                                    # flat background
normc = sp.expand(tr((Adn_bg.T*Aup_bg)[0] + 1, wb, 2))
check(normc == 0, "[A1] A_m A^m = -1 on the boosted background to O(wb^2)",
      f"A_mA^m+1 = {normc}")
# scalar aligned: d_m phi_bg = -Q0 A_m_bg
dphi_bg = -Q0*Adn_bg
Qbg = sp.expand(tr((Aup_bg.T*dphi_bg)[0], wb, 2))
check(sp.simplify(Qbg - Q0) == 0, "[A2] Q = A^m d_m phi = Q_0 on background (Q-shift is O(wb^4))",
      f"Q_bg = {Qbg}")
proj = sp.Matrix(4, 4, lambda m, n: eta[m, n] + Aup_bg[m]*Aup_bg[n])
Ybg = sp.expand(tr((dphi_bg.T*proj*dphi_bg)[0], wb, 2))
check(sp.simplify(Ybg) == 0, "[A3] Y = 0 on the boosted background (spatial projector kills it)",
      f"Y_bg = {Ybg}")
P(f"    ({time.time()-T0:.1f}s)")


# ================================================================ [B] Fourier amplitudes (fast)
P("="*90); P("[B] plane-wave amplitudes; exact ik derivative; single truncation at L2"); P("="*90)
Es, Eis = sp.symbols('E_s E_is')
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
kv = [0, kx, ky, kz]
k2 = kx**2 + ky**2 + kz**2

def nf(tag):
    ket = sp.Symbol(tag + 'k'); bra = sp.Symbol(tag + 'b')
    return ket*Es + bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)

Psi, Psik, Psib = nf('Psi'); Phi, Phik, Phib = nf('Phi')
Bf = []; Bk = []; Bb = []
for i in range(3):
    f, kk, bb = nf(f'B{i+1}'); Bf.append(f); Bk.append(kk); Bb.append(bb)
af = []; ak = []; ab = []
for i in range(3):
    f, kk, bb = nf(f'a{i+1}'); af.append(f); ak.append(kk); ab.append(bb)
chi, chik, chib = nf('chi')
rho, Rk, Rb = nf('rho')
a0f, a0k, a0b = nf('a0p')
KETS = [Psik, Phik] + Bk + ak + [chik]
BRAS = [Psib, Phib] + Bb + ab + [chib]

H = sp.zeros(4, 4); H[0, 0] = -2*Psi
for i in range(3):
    H[0, i+1] = Bf[i]; H[i+1, 0] = Bf[i]; H[i+1, i+1] = -2*Phi
gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
Hup = eta*H*eta
gu = sp.Matrix(4, 4, lambda i, j: (eta - eps*Hup + eps**2*(Hup*H*eta))[i, j])
trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))
HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)

# aether: temporal perturbation a0f solved from unit constraint at O(eps) (linear)
Adn = sp.Matrix([Adn_bg[0] - eps*a0f, Adn_bg[1] + eps*af[0],
                 Adn_bg[2] + eps*af[1], Adn_bg[3] + eps*af[2]])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
C1 = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
C1 = sp.expand(C1)
solA = sp.solve([C1.coeff(Es, 1), C1.coeff(Eis, 1)], [a0k, a0b], dict=True)[0]
# wb-truncate the constraint solution immediately (kills the 1/(2+wb^2 w^2) denominator)
wbtr = lambda e: sum(sp.series(sp.expand(e), wb, 0, 3).removeO().coeff(wb, n)*wb**n for n in range(3)) \
    if e != 0 else e
solA = {k: sp.expand(sp.series(v, wb, 0, 3).removeO()) for k, v in solA.items()}
a0f = a0f.subs(solA)
Adn = sp.Matrix([Adn_bg[0] - eps*a0f, Adn_bg[1] + eps*af[0],
                 Adn_bg[2] + eps*af[1], Adn_bg[3] + eps*af[2]])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
Cchk = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
_wt = lambda e: sum(sp.expand(e).coeff(wb, n)*wb**n for n in range(3))
check(sp.expand(_wt(Cchk.coeff(Es, 1))) == 0 and sp.expand(_wt(Cchk.coeff(Eis, 1))) == 0,
      "[B1] unit constraint A.A=-1 solved at O(eps) (to O(wb^2)); temporal aether fixed")
P(f"    constraint solved ({time.time()-T0:.1f}s)")

import os, pickle
_CACHE = 'L2dc_cache.pkl'
_HAVE_CACHE = os.path.exists(_CACHE)
dphi = sp.Matrix([dphi_bg[m] + eps*d(chi, m) for m in range(4)])
Gam = [[[sp.Rational(1, 2)*sum(gu[r, s]*(d(gd[s, n], m)+d(gd[s, m], n)-d(gd[m, n], s))
        for s in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
# analytic LINEARIZED Einstein tensor G1_{mn}(ket) -- fast (linear in ket amplitudes).
Hket = sp.Matrix(4, 4, lambda m, n: H[m, n].coeff(Es, 1)*Es)   # ket-only metric perturbation
Gam1 = [[[sp.Rational(1, 2)*sum(eta[r, s]*(d(Hket[s, n], m)+d(Hket[s, m], n)-d(Hket[m, n], s))
         for s in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
def R1(m, n):
    return sum(d(Gam1[a][m][n], a) - d(Gam1[a][m][a], n) for a in range(4))
R1sc = sum(eta[m, n]*R1(m, n) for m in range(4) for n in range(4))
G1 = sp.Matrix(4, 4, lambda m, n: sp.expand(R1(m, n) - sp.Rational(1, 2)*eta[m, n]*R1sc))
P(f"    linearized Einstein tensor assembled ({time.time()-T0:.1f}s)")

seh = sp.Symbol('s_eh')
def wtrunc(e):
    e = sp.expand(e)
    return sum(e.coeff(wb, n)*wb**n for n in range(3))
if _HAVE_CACHE:
    L2dc = pickle.load(open(_CACHE, 'rb'))
    P(f"    L2dc loaded from cache ({time.time()-T0:.1f}s)")
else:
    def te(e):
        e = sp.expand(e); out = 0
        for i in range(3):
            ci = e.coeff(eps, i)
            for j in range(3):
                out += ci.coeff(wb, j)*eps**i*wb**j
        return out
    guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))
    AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
    GamT = [[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]
    dphiT = sp.Matrix(4, 1, lambda i, j: te(dphi[i]))
    Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m) - d(Adn[m], n)))
    F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
    F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta[m, a]*eta[n, b]
                    for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    Jup = [te(sum(AupT[nu]*(d(AupT[al], nu) + sum(GamT[al][nu][r]*AupT[r] for r in range(4)))
                 for nu in range(4))) for al in range(4)]
    Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
    Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
    Yc = te(sum((guT[m, n] + AupT[m]*AupT[n])*dphiT[m]*dphiT[n] for m in range(4) for n in range(4)))
    dQ = Qc - Q0
    Kq = -2*LAM + K2*te(dQ**2)
    P(f"    dark scalars assembled ({time.time()-T0:.1f}s)")
    def grade(e):
        e = sp.expand(e)
        return [wtrunc(e.coeff(eps, n)) for n in range(3)]
    # GENUINE Einstein-Hilbert quadratic Lagrangian: sqrt(-g) R to O(eps^2) (full nonlinear
    # Ricci, reduced ansatz).  This is the correct EH action whose EL gives the linearized
    # Einstein tensor consistently in EVERY metric component (the hand-built h.G1 shortcut is
    # NOT the EH action and mis-normalises the off-diagonal/trace sectors).
    def ric(a, b):
        o = 0
        for m in range(4):
            o += d(Gam[m][b][a], m) - d(Gam[m][m][a], b)
            for l in range(4):
                o += Gam[m][m][l]*Gam[l][b][a] - Gam[m][b][l]*Gam[l][m][a]
        return o
    Rsc = te(sum(guT[m, n]*ric(m, n) for m in range(4) for n in range(4)))
    P(f"    Ricci scalar assembled ({time.time()-T0:.1f}s)")
    gF2 = grade(F2); gJ = grade(Jdphi); gY = grade(Yc); gK = grade(Kq); gsq = grade(sqg)
    gR = grade(Rsc)
    # full scalar S = R - 2Lam - (K_B/2)F2 + 2(2-K_B)Jdphi - (2-K_B)Y - K(Q)
    gS = [gR[n] - (2*LAM if n == 0 else 0) - (KB/2)*gF2[n] + 2*(2-KB)*gJ[n]
          - (2-KB)*gY[n] - gK[n] for n in range(3)]
    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3))) - (2-KB)*JY*gY[2]
    L2_matt = -16*sp.pi*GT*wtrunc(rho*(-H[0, 0]/2))
    L2 = sp.expand(L2_grav + L2_matt)
    P(f"    L2 built: {len(sp.Add.make_args(L2))} terms ({time.time()-T0:.1f}s)")
    def DC(e):
        e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
        for mon, c in zip(pol.monoms(), pol.coeffs()):
            if mon[0] == mon[1]:
                out += c*(Es*Eis)**mon[0]
        return out.subs(Es*Eis, 1) if out != 0 else out
    L2dc = DC(L2)
    pickle.dump(L2dc, open(_CACHE, 'wb'))
    P(f"    DC extracted + cached ({time.time()-T0:.1f}s)")

# GAUGE FIXING (k along x): the longitudinal metric-vector h_01=B1 (shifted by d_1 xi_0) and
# the longitudinal aether a_1 (degenerate with chi -- typeII D8) are pure gauge => set to 0 and
# drop their (now-redundant Bianchi) equations.  Physical: B2,B3 (transverse) and chi.
GAUGE = {Bk[0]: 0, Bb[0]: 0, ak[0]: 0, ab[0]: 0}
L2dc = sp.expand(L2dc.subs(GAUGE))
BRAS_phys = [Psib, Phib, Bb[1], Bb[2], ab[1], ab[2], chib]
KETS_phys = [Psik, Phik, Bk[1], Bk[2], ak[1], ak[2], chik]
# field equations: vary each physical bra amplitude
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS_phys}
P(f"    EOMs assembled (gauge-fixed B1=a1=0) ({time.time()-T0:.1f}s)")

# genuine EH => normalisation is FIXED (no free constant).  Q0->0 is a degenerate corner (the
# scalar locks to Psi there) so it is NOT used for calibration; Newton + gamma=1 are verified in
# the PHYSICAL static sector below ([C4], and Psik(static) reduces to the committed typeII 00-eq).
SEH = 1
P(f"    genuine EH: fixed normalisation, no free constant ({time.time()-T0:.1f}s)")

# ---- full solve (dark on), order by order in wb ------------------------------------------------
# fix the wavevector direction k=(kx,0,0) (alpha's are rotation-covariant; w kept general).
# This collapses kx,ky,kz -> kx and makes the order-by-order wb solve tractable.
# alpha's are dimensionless: fix k=(1,0,0), Gt=1, Lambda=0 (background) to make the symbolic
# solve tractable.  K_B, K_2, Q_0, J_Y kept symbolic.  Length scale set by k=1, so the
# combination that carries the AeST scalar mass is (K_2 Q_0^2) [ = mu^2/(2-K_B)*(2-K_B) in k-units ].
NUM = {ky: 0, kz: 0, kx: 1, GT: 1, LAM: 0}
eqf = {A: sp.expand(eq[A].subs(seh, SEH).subs(NUM)) for A in BRAS_phys}
UNK = KETS_phys
def lin_solve(eqs, unk):
    A, b = sp.linear_eq_to_matrix(eqs, unk)
    sol = list(sp.linsolve((A, b), unk))
    if not sol:
        return None
    return dict(zip(unk, sol[0]))
# static (wb^0): transverse vector/aether (B2,B3,a2,a3) are odd-in-w -> 0; solve scalars.
VZ = {Bk[1]: 0, Bk[2]: 0, ak[1]: 0, ak[2]: 0}
eq0s = [sp.expand(eqf[A].coeff(wb, 0).subs(VZ)) for A in [Psib, Phib, chib]]
s0s = lin_solve(eq0s, [Psik, Phik, chik])
check(s0s is not None, "[C3] static (wb=0) scalar sector solves uniquely (k along x)")
s0 = {**s0s, Bk[1]: sp.S(0), Bk[2]: sp.S(0), ak[1]: sp.S(0), ak[2]: sp.S(0)}
gam_static = sp.simplify(s0[Phik] - s0[Psik])
check(sp.simplify(gam_static) == 0, "[C4] static gamma_PPN=1 (Phi=Psi at wb=0)")
P(f"    static sector solved ({time.time()-T0:.1f}s)")

dk1 = {A: sp.Symbol(f'd1_{A}') for A in UNK}
dk2 = {A: sp.Symbol(f'd2_{A}') for A in UNK}
subFull = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in UNK}
eqW = {A: sp.expand(eqf[A].subs(subFull)) for A in BRAS_phys}
sol1w = lin_solve([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS_phys], list(dk1.values()))
check(sol1w is not None, "[C5] O(wb^1) sector solves (h_0i sourced)")
eq2 = [sp.expand(eqW[A].coeff(wb, 2)).subs(sol1w) for A in BRAS_phys]
sol2w = lin_solve(eq2, list(dk2.values()))
check(sol2w is not None, "[C6] O(wb^2) sector solves (g_00 w^2 sourced)")
def ketval(A):
    return sp.expand(s0[A] + wb*dk1[A].subs(sol1w) + wb**2*dk2[A].subs(sol2w))
Bsol = [sp.S(0), sp.expand(ketval(Bk[1])), sp.expand(ketval(Bk[2]))]
Psisol = sp.expand(ketval(Psik))
P(f"    wb-perturbative solve done ({time.time()-T0:.1f}s)")

pickle.dump({'Bsol': Bsol, 'Psisol': Psisol, 'SEH': SEH}, open('SOLVE_cache.pkl', 'wb'))
# define Newtonian amplitude Uh (k=1,Gt=1 units): Psik_GR = -4 pi Gt Rk/k2 = -4 pi Rk = Uh
Uh = sp.Symbol('U_hat')
subU = {Rk: -Uh/(4*sp.pi)}

# =============================================================== [D] PPN extraction
P("="*90); P("[D] PPN extraction (wb = boost magnitude stripped; w_i = unit direction)"); P("="*90)
# k=(1,0,0).  Physical source-frame velocity v_i = wb * w_i.  h_0i is O(wb^1); g00 w-part O(wb^2).
# --- alpha_1 from h_0i (transverse, gauge-invariant): g_0i = (alpha_1/2) v_i U ---------------
b2 = sp.expand(Bsol[1].coeff(wb, 1).subs(subU))     # O(v) coeff of h_02 (perp to k); v_2 = w2
q1 = sp.cancel(b2.coeff(w2*Uh))                     # = alpha_1/2   (perp: (v.k)k_2 = 0)
alpha1 = sp.cancel(2*q1)
P(f"    ALPHA_1 = {alpha1}")
check(sp.simplify(alpha1 - (-4*KB)) == 0,
      "[D1] *** alpha_1 = -4 K_B  (DERIVED; matches committed EA-vector value) ***",
      f"alpha_1 + 4 K_B = {sp.simplify(alpha1 + 4*KB)}")

# --- alpha_2 (gauge-invariant) from the w^2 sector of g_00 = -1 - 2 eps Psi -------------------
ps2 = sp.expand(Psisol.coeff(wb, 2).subs(subU))     # O(v^2) coeff of Psi;  metric w-part = -2*ps2
PA = sp.cancel(-2*ps2.coeff(w2**2*Uh))              # coeff of v^2 U        = 2 alpha_2 - alpha_1
PApar = sp.cancel(-2*ps2.coeff(w1**2*Uh))           # coeff of v_par^2 U    = PA + PB
PB = sp.cancel(PApar - PA)                          # coeff of (v.k)^2 U/k2 = -2 alpha_2
alpha2_A = sp.cancel((PA + alpha1)/2)               # from v^2 U structure
alpha2_B = sp.cancel(-PB/2)                         # from (v.k)^2/k2 structure (independent)
check(sp.simplify(alpha2_A - alpha2_B) == 0,
      "[D2] alpha_2 agrees from the two independent g_00 structures (v^2 and (v.k)^2)",
      f"diff = {sp.simplify(alpha2_A - alpha2_B)}")
alpha2 = sp.cancel(sp.simplify(alpha2_B))
P("="*90); P(f"    *** ALPHA_2 = {alpha2} ***"); P("="*90)

# ---- numerical sanity + kernel-blind Solar-System limit -----------------------------------------
P("[E] numeric checks + Solar-System (Newtonian branch J_Y->1) limit")
import itertools
num_ok = True
for kbv, k2v, q0v, jyv in itertools.product([0.05, 0.3], [10.0, 300.0], [0.2, 0.9], [1.0, 2.0]):
    sub = {KB: kbv, K2: k2v, Q0: q0v, JY: jyv}
    a1n = complex(alpha1.subs(sub)); a2An = complex(alpha2_A.subs(sub)); a2Bn = complex(alpha2_B.subs(sub))
    if abs(a1n + 4*kbv) > 1e-9 or abs(a2An - a2Bn) > 1e-9:
        num_ok = False
        P(f"    MISMATCH at {sub}: a1={a1n}, a2A={a2An}, a2B={a2Bn}")
check(num_ok, "[E1] numeric: alpha_1=-4K_B and the two alpha_2 extractions agree over a param grid")

# Solar-System: J_Y -> 1 (mu_10 -> 1, MOND kernel invisible); and the AeST scalar-mass scale
# mu^2 = K_2 Q_0^2 is << k^2 (=1 here) at Solar-System scales, so take K_2 Q_0^2 -> 0.
alpha2_JY1 = sp.cancel(alpha2.subs(JY, 1))
P(f"    alpha_2 (J_Y=1)                    = {alpha2_JY1}")
# massless / short-distance limit K_2 Q_0^2 -> 0 (mu/k -> 0):
alpha2_SS = sp.simplify(sp.limit(alpha2_JY1.subs(K2, sp.Symbol('mm')/Q0**2), sp.Symbol('mm'), 0))
P(f"    alpha_2 (J_Y=1, K_2 Q_0^2 -> 0)   = {alpha2_SS}")
a1_SS = sp.simplify(alpha1.subs(JY, 1))

import sys
P("="*90)
nfail = len(FAIL)
P(f"    {NCH[0]-nfail}/{NCH[0]} certificates pass" + ("" if nfail == 0 else f";  FAILED: {FAIL}"))
with open('ALPHA_RESULT.txt', 'w') as fp:
    fp.write("FC-FINAL (AeST + frozen J_10) preferred-frame PPN, DERIVED from the action\n")
    fp.write(f"seh (EH normalisation, calibrated by Newton) = {SEH}\n\n")
    fp.write(f"alpha_1 = {alpha1}\n\n")
    fp.write(f"alpha_2 (full, symbolic in K_B,K_2,Q_0,J_Y; k=1 units) =\n{alpha2}\n\n")
    fp.write(f"alpha_2 (J_Y=1) = {alpha2_JY1}\n\n")
    fp.write(f"alpha_2 (J_Y=1, K_2 Q_0^2 -> 0, i.e. Solar-System short-distance) = {alpha2_SS}\n")
    fp.write(f"alpha_1 (J_Y=1) = {a1_SS}\n")
sys.exit(0 if nfail == 0 else 1)
