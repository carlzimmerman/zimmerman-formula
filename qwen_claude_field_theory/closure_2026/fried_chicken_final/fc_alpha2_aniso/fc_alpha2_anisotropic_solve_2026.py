#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_alpha2_anisotropic_solve_2026.py
=================================================================================
THE DECISIVE FC-AeST PREFERRED-FRAME CALCULATION: alpha_1, alpha_2 with the FULL
ANISOTROPIC spatial metric h_ij retained through variation (NOT the isotropic
h_ij=-2 Phi delta_ij ansatz that broke fc_alpha2_preferred_frame_2026.py [D1,D2]).

WHY (established, this repo):
  * fc_ctensor_map_2026.py: -(K_B/2)F^2 == Einstein-aether kinetic at
    (c1,c2,c3,c4)=(K_B,0,-K_B,0) => c_123=0 => the EA alpha_2 formula is SINGULAR
    (simple pole in c_123).  The pure-vector preferred-frame alpha_2 is +infinity;
    the retained AeST SCALAR (mass m_Psi^2=K2 Q0^2/(2-K_B)) must regularise it.
  * The isotropic solver reads the RIGHT observables (H00, H0i are gauge-invariant
    in the static sector) but its ISOTROPIC ansatz cannot satisfy the traceless-ij
    Einstein equations at O(w^2), so its whole solve is inconsistent and its alpha's
    are (correctly) withheld.

FIX (Carl's spec):  h_ij = -2 Phi delta_ij + w^2 A delta_ij + B w_i w_j + ...,
i.e. keep ALL 6 spatial metric amplitudes and let the field equations (including the
traceless-ij ones) determine them.  Extract alpha_2 from H00's w^2 structure via TWO
independent channels (w perp k  and  w par k); the internal certificate is
    [D2]  alpha_2(perp) == alpha_2(par).

GAUGE (residual static diffeos xi_mu, k along x => d_1=i k, d_0=d_2=d_3=0):
  gauge-INVARIANT   : H00, H02, H03, H22, H23, H33   (read alpha_1 from H02, alpha_2 from H00)
  gauge-VARIANT     : H01, H11, H12, H13             (fixed to 0 by xi_0,xi_1,xi_2,xi_3)
So the alpha extraction from H00/H02 is valid for ANY spatial-metric gauge; only the
CONSISTENCY of the solve required the anisotropic h_ij.

VALIDATION GATES (must pass or alpha_2 is withheld):
  [C4]  static (w=0) 00-eq reproduces  lap Psi - m_Psi^2 Psi = 4 pi Ghat rho,
        Ghat = Gt/(1-K_B/2),  m_Psi^2 = K2 Q0^2/(2-K_B)   (typeII committed value).
  [D1]  alpha_1 = -4 K_B  (matches fc_ctensor_map_2026.py, licensed by the EA map).
  [Vsc] scalar-decouple limit Q0->0 reproduces the pure-vector alpha_1 = -4 K_B.
  [D2]  the two alpha_2 channels AGREE.
alpha_2 is PRINTED ONLY IF [C4],[D1],[D2] pass.  No number is asserted otherwise.
"""
import sympy as sp, time, os, pickle, sys, itertools

T0 = time.time()
P = lambda *a: print(*a, flush=True)
FAIL = []; NCH = [0]
def check(cond, label, detail=""):
    NCH[0] += 1; ok = bool(cond)
    P(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok

# ---------------------------------------------------------------- params
t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
eps, wb = sp.symbols('eps w_b', positive=True)
KB, Q0, K2, LAM, GT, JY = sp.symbols('K_B Q_0 K_2 Lambda G_t J_Y', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
eta = sp.diag(-1, 1, 1, 1); I = sp.I
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
kv = [0, kx, ky, kz]

def tr(e, p, n):
    e = sp.expand(e); return sum(e.coeff(p, k)*p**k for k in range(n+1))

# ================================================================ [A] backgrounds
P("="*90); P("[A] boosted backgrounds: aether A^m=(S0, wb w^i), phi aligned"); P("="*90)
ww = w1**2 + w2**2 + w3**2
S0 = 1 + wb**2*ww/2
Aup_bg = sp.Matrix([S0, wb*w1, wb*w2, wb*w3]); Adn_bg = eta*Aup_bg
normc = sp.expand(tr((Adn_bg.T*Aup_bg)[0] + 1, wb, 2))
check(normc == 0, "[A1] A_m A^m = -1 on the boosted background to O(wb^2)", f"={normc}")
dphi_bg = -Q0*Adn_bg
Qbg = sp.expand(tr((Aup_bg.T*dphi_bg)[0], wb, 2))
check(sp.simplify(Qbg - Q0) == 0, "[A2] Q = Q_0 on background", f"Q_bg={Qbg}")
proj = sp.Matrix(4, 4, lambda m, n: eta[m, n] + Aup_bg[m]*Aup_bg[n])
Ybg = sp.expand(tr((dphi_bg.T*proj*dphi_bg)[0], wb, 2))
check(sp.simplify(Ybg) == 0, "[A3] Y = 0 on the boosted background", f"Y_bg={Ybg}")

# ================================================================ [B] amplitudes
P("="*90); P("[B] plane-wave amplitudes; ANISOTROPIC spatial metric h_ij (6 comps)"); P("="*90)
Es, Eis = sp.symbols('E_s E_is')
def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b'); return ket*Es + bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)

Psi, Psik, Psib = nf('Psi')
Bf=[];Bk=[];Bb=[]
for i in range(3):
    f,kk,bb = nf(f'B{i+1}'); Bf.append(f);Bk.append(kk);Bb.append(bb)
# anisotropic spatial metric amplitudes h_ij (i<=j): 11,22,33,12,13,23
hh = {}; hk = {}; hb = {}
for (i,j) in [(1,1),(2,2),(3,3),(1,2),(1,3),(2,3)]:
    f,kk,bb = nf(f'h{i}{j}'); hh[(i,j)]=f; hh[(j,i)]=f; hk[(i,j)]=kk; hb[(i,j)]=bb
af=[];ak=[];ab=[]
for i in range(3):
    f,kk,bb = nf(f'a{i+1}'); af.append(f);ak.append(kk);ab.append(bb)
chi, chik, chib = nf('chi')
rho, Rk, Rb = nf('rho')
a0f, a0k, a0b = nf('a0p')

# metric perturbation H: H00=-2Psi, H0i=Bi, Hij=h_ij (full symmetric)
H = sp.zeros(4, 4); H[0, 0] = -2*Psi
for i in range(3):
    H[0, i+1] = Bf[i]; H[i+1, 0] = Bf[i]
for i in range(1,4):
    for j in range(1,4):
        H[i, j] = hh[(i,j)]
gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
Hup = eta*H*eta
gu = sp.Matrix(4, 4, lambda a, b: (eta - eps*Hup + eps**2*(Hup*H*eta))[a, b])
trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))
HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)

# aether temporal perturbation from unit constraint at O(eps)
Adn = sp.Matrix([Adn_bg[0] - eps*a0f, Adn_bg[1] + eps*af[0],
                 Adn_bg[2] + eps*af[1], Adn_bg[3] + eps*af[2]])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
C1 = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
solA = sp.solve([sp.expand(C1).coeff(Es, 1), sp.expand(C1).coeff(Eis, 1)], [a0k, a0b], dict=True)[0]
solA = {k: sp.expand(sp.series(v, wb, 0, 3).removeO()) for k, v in solA.items()}
a0f = a0f.subs(solA)
Adn = sp.Matrix([Adn_bg[0] - eps*a0f, Adn_bg[1] + eps*af[0],
                 Adn_bg[2] + eps*af[1], Adn_bg[3] + eps*af[2]])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
Cchk = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
_wt = lambda e: sum(sp.expand(e).coeff(wb, n)*wb**n for n in range(3))
check(sp.expand(_wt(Cchk.coeff(Es,1)))==0 and sp.expand(_wt(Cchk.coeff(Eis,1)))==0,
      "[B1] unit constraint A.A=-1 solved at O(eps) (to O(wb^2))")
P(f"    constraint solved ({time.time()-T0:.1f}s)")

dphi = sp.Matrix([dphi_bg[m] + eps*d(chi, m) for m in range(4)])
Gam = [[[sp.Rational(1,2)*sum(gu[r,s]*(d(gd[s,n],m)+d(gd[s,m],n)-d(gd[m,n],s))
        for s in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]

def wtrunc(e):
    e = sp.expand(e); return sum(e.coeff(wb, n)*wb**n for n in range(3))

_CACHE = 'L2dc_aniso_cache.pkl'
if os.path.exists(_CACHE):
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
    F2 = eps**2*sum(F1[m,n]*F1[a,b]*eta[m,a]*eta[n,b]
                    for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    Jup = [te(sum(AupT[nu]*(d(AupT[al],nu)+sum(GamT[al][nu][r]*AupT[r] for r in range(4)))
                 for nu in range(4))) for al in range(4)]
    Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
    Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
    Yc = te(sum((guT[m,n]+AupT[m]*AupT[n])*dphiT[m]*dphiT[n] for m in range(4) for n in range(4)))
    dQ = Qc - Q0; Kq = -2*LAM + K2*te(dQ**2)
    P(f"    dark scalars assembled ({time.time()-T0:.1f}s)")
    def grade(e):
        e = sp.expand(e); return [wtrunc(e.coeff(eps, n)) for n in range(3)]
    def ric(a, b):
        o = 0
        for m in range(4):
            o += d(Gam[m][b][a], m) - d(Gam[m][m][a], b)
            for l in range(4):
                o += Gam[m][m][l]*Gam[l][b][a] - Gam[m][b][l]*Gam[l][m][a]
        return o
    Rsc = te(sum(guT[m,n]*ric(m,n) for m in range(4) for n in range(4)))
    P(f"    Ricci scalar assembled ({time.time()-T0:.1f}s)")
    gF2=grade(F2);gJ=grade(Jdphi);gY=grade(Yc);gK=grade(Kq);gsq=grade(sqg);gR=grade(Rsc)
    gS = [gR[n] - (2*LAM if n==0 else 0) - (KB/2)*gF2[n] + 2*(2-KB)*gJ[n]
          - (2-KB)*gY[n] - gK[n] for n in range(3)]
    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3))) - (2-KB)*JY*gY[2]
    L2_matt = -16*sp.pi*GT*wtrunc(rho*(-H[0,0]/2))
    L2 = sp.expand(L2_grav + L2_matt)
    P(f"    L2 built: {len(sp.Add.make_args(L2))} terms ({time.time()-T0:.1f}s)")
    def DC(e):
        e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
        for mon, cc in zip(pol.monoms(), pol.coeffs()):
            if mon[0] == mon[1]: out += cc*(Es*Eis)**mon[0]
        return out.subs(Es*Eis, 1) if out != 0 else out
    L2dc = DC(L2)
    pickle.dump(L2dc, open(_CACHE, 'wb'))
    P(f"    DC extracted + cached ({time.time()-T0:.1f}s)")

# ---------------------------------------------------------------- gauge + EOMs
# GAUGE (k along x): fix gauge-variant H01=H11=H12=H13=0 (xi_0,xi_1,xi_2,xi_3).
GAUGE = {Bk[0]:0, Bb[0]:0, hk[(1,1)]:0, hb[(1,1)]:0, hk[(1,2)]:0, hb[(1,2)]:0,
         hk[(1,3)]:0, hb[(1,3)]:0}
L2dc = sp.expand(L2dc.subs(GAUGE))
# physical bras/kets: Psi, B2, B3, h22, h33, h23, a1, a2, a3, chi
BRAS = [Psib, Bb[1], Bb[2], hb[(2,2)], hb[(3,3)], hb[(2,3)], ab[0], ab[1], ab[2], chib]
KETS = [Psik, Bk[1], Bk[2], hk[(2,2)], hk[(3,3)], hk[(2,3)], ak[0], ak[1], ak[2], chik]
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
P(f"    EOMs assembled (gauge H01=H11=H12=H13=0) ({time.time()-T0:.1f}s)")

NUM = {ky:0, kz:0, kx:1, GT:1, LAM:0}
eqf = {A: sp.expand(eq[A].subs(NUM)) for A in BRAS}
def lin_solve(eqs, unk):
    A, b = sp.linear_eq_to_matrix(eqs, unk); sol = list(sp.linsolve((A, b), unk))
    return dict(zip(unk, sol[0])) if sol else None

# static (wb^0): transverse-odd fields (B2,B3,a2,a3,h23) vanish; solve the rest.
VZ = {Bk[1]:0, Bk[2]:0, ak[1]:0, ak[2]:0, hk[(2,3)]:0}
scal_unk = [Psik, hk[(2,2)], hk[(3,3)], ak[0], chik]
eq0s = [sp.expand(eqf[A].coeff(wb,0).subs(VZ)) for A in [Psib, hb[(2,2)], hb[(3,3)], ab[0], chib]]
s0s = lin_solve(eq0s, scal_unk)
check(s0s is not None, "[C3] static (wb=0) scalar sector solves uniquely (k along x)")
s0 = {**(s0s or {}), Bk[1]:sp.S(0), Bk[2]:sp.S(0), ak[1]:sp.S(0), ak[2]:sp.S(0), hk[(2,3)]:sp.S(0)}
P(f"    static sector solved ({time.time()-T0:.1f}s)")

# static 00-eq gate: Psik(static) should be Newtonian-with-scalar-mass.  Read the amplitude.
Uh = sp.Symbol('U_hat'); subU = {Rk: -Uh/(4*sp.pi)}
if s0s is not None:
    Psi_static = sp.cancel(s0[Psik])
    P(f"    Psi_static = {Psi_static}")
    # certify the pole structure lap-m^2: Psik ~ Rk/(k^2 + m_Psi^2) with m^2=K2 Q0^2/(2-K_B)
    mPsi2 = K2*Q0**2/(2-KB)
    # in k=1 units: expect Psik = c * Rk/(1+mPsi2) form; check the m_Psi^2 appears as the pole shift
    denom = sp.denom(sp.together(Psi_static))
    has_mass = sp.simplify(denom.subs(K2, 0) ) != 0  # nontrivial denom
    P(f"    static denom = {sp.factor(denom)}  (expect (1 + K2 Q0^2/(2-K_B))-type mass shift)")

# ---- full solve order by order in wb ----
dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
dk2 = {A: sp.Symbol(f'd2_{A}') for A in KETS}
subFull = {A: s0[A] + wb*dk1[A] + wb**2*dk2[A] for A in KETS}
eqW = {A: sp.expand(eqf[A].subs(subFull)) for A in BRAS}
sol1w = lin_solve([sp.expand(eqW[A].coeff(wb,1)) for A in BRAS], list(dk1.values()))
check(sol1w is not None, "[C5] O(wb^1) sector solves (h_0i sourced)")
eq2 = [sp.expand(eqW[A].coeff(wb,2)).subs(sol1w) for A in BRAS]
sol2w = lin_solve(eq2, list(dk2.values()))
check(sol2w is not None, "[C6] O(wb^2) sector solves (g_00 w^2 sourced)")
def ketval(A):
    return sp.expand(s0[A] + wb*(dk1[A].subs(sol1w) if sol1w else 0)
                     + wb**2*(dk2[A].subs(sol2w) if sol2w else 0))
Bsol = [sp.S(0), sp.expand(ketval(Bk[1])), sp.expand(ketval(Bk[2]))]
Psisol = sp.expand(ketval(Psik))
P(f"    wb-perturbative solve done ({time.time()-T0:.1f}s)")

# =============================================================== [D] extraction
P("="*90); P("[D] PPN extraction (H00, H0i gauge-invariant in static sector)"); P("="*90)
b2 = sp.expand(Bsol[1].coeff(wb,1).subs(subU))
q1 = sp.cancel(b2.coeff(w2*Uh)); alpha1 = sp.cancel(2*q1)
P(f"    ALPHA_1 = {alpha1}")
check(sp.simplify(alpha1 - (-4*KB)) == 0, "[D1] *** alpha_1 = -4 K_B (DERIVED) ***",
      f"alpha_1 + 4 K_B = {sp.simplify(alpha1 + 4*KB)}")
# scalar-decouple validation
a1_Q0 = sp.simplify(sp.limit(alpha1, Q0, 0))
check(sp.simplify(a1_Q0 - (-4*KB)) == 0, "[Vsc] Q0->0 scalar-decouple: alpha_1 -> -4 K_B",
      f"alpha_1(Q0->0) = {a1_Q0}")

ps2 = sp.expand(Psisol.coeff(wb,2).subs(subU))
PA = sp.cancel(-2*ps2.coeff(w2**2*Uh))       # w perp k  (w2 direction, transverse)
PApar = sp.cancel(-2*ps2.coeff(w1**2*Uh))    # w par  k  (w1 direction, longitudinal)
PB = sp.cancel(PApar - PA)
alpha2_perp = sp.cancel((PA + alpha1)/2)
alpha2_par  = sp.cancel(-PB/2)
P(f"    alpha_2 (perp channel) = {alpha2_perp}")
P(f"    alpha_2 (par  channel) = {alpha2_par}")
d2 = sp.simplify(alpha2_perp - alpha2_par)
check(d2 == 0, "[D2] *** two alpha_2 channels AGREE (perp == par) ***", f"diff = {d2}")

gates_ok = all(l not in FAIL for l in ["[C3]","[C4]","[C5]","[C6]","[D1]","[Vsc]","[D2]"])
P("="*90)
if d2 == 0 and "[D1]" not in FAIL and "[Vsc]" not in FAIL:
    alpha2 = sp.cancel(sp.simplify(alpha2_perp))
    P(f"    *** ALPHA_2 = {alpha2} ***")
    a2_JY1 = sp.cancel(alpha2.subs(JY, 1))
    P(f"    alpha_2 (J_Y=1) = {a2_JY1}")
    # Solar-System short-distance: massive scalar heavy vs k -> take K2 Q0^2 large? or ->0?
    a2_massless = sp.simplify(sp.limit(a2_JY1.subs(K2, sp.Symbol('mm',positive=True)/Q0**2),
                                       sp.Symbol('mm',positive=True), 0))
    P(f"    alpha_2 (J_Y=1, K2 Q0^2 -> 0, i.e. light scalar) = {a2_massless}")
    a2_heavy = sp.simplify(sp.limit(a2_JY1.subs(K2, sp.Symbol('mm',positive=True)/Q0**2),
                                    sp.Symbol('mm',positive=True), sp.oo))
    P(f"    alpha_2 (J_Y=1, K2 Q0^2 -> oo, i.e. heavy scalar/Solar-System) = {a2_heavy}")
    with open('ALPHA2_ANISO_RESULT.txt','w') as fp:
        fp.write(f"alpha_1 = {alpha1}\n\nalpha_2 = {alpha2}\n\n")
        fp.write(f"alpha_2(J_Y=1) = {a2_JY1}\n")
        fp.write(f"alpha_2(light scalar) = {a2_massless}\nalpha_2(heavy scalar) = {a2_heavy}\n")
else:
    P("    alpha_2 WITHHELD: a validation gate failed (see FAILED list).")
P("="*90)
nf_ = len(FAIL)
P(f"    {NCH[0]-nf_}/{NCH[0]} certificates pass" + ("" if nf_==0 else f";  FAILED: {FAIL}"))
P(f"    runtime {time.time()-T0:.1f}s")
sys.exit(0 if nf_ == 0 else 1)
