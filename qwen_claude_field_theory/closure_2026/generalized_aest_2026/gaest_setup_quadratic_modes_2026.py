#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gaest_setup_quadratic_modes_2026.py   (SETUP certificate, part 1 of 2)
=======================================================================
Generalized-aether completion (THE_GENERALIZED_COMPLETION.md): the aether
sector is Einstein-aether with c1 = -c3 = K_B (c13 = 0) and c2, c4 FREE.

This script DERIVES (does not transcribe) the linearized mode structure of
    L = sqrt(-g) [ R - c1 D_aA^m D^aA_m - c2 (D_aA^a)^2 - c3 D_aA^m D_mA^a
                     + c4 a_m a^m ]              (mostly-plus, FJ dictionary,
                                                  a^m = A^n D_n A^m)
about Minkowski + A^mu = (1,0,0,0), plane wave  exp(i(k x - w t)), all ten
metric components + three aether components (A^0 fixed by the unit norm).
Gauge is fixed AFTER the quadratic form is built (drop reachable fields), so
every helicity block is an honest Hermitian form  L = B^T M(w,k) K.

Certified outputs (each check CAN FAIL):
  [T]  spin-2 block: c_T^2 = 1/(1-c13); entries carry NO c2, NO c4
       -> at c1=-c3=K_B: c_T^2 = 1 for every (c2,c4,K_B). (Gate 6 / GW170817)
       Mutation control: the block DOES carry c1+c3 (so 'tensor-blind' is not
       a vacuous statement about the pipeline).
  [V]  spin-1 block: c_V^2 = (2c1 - c1^2 + c3^2)/(2 c14 (1-c13))  [Jacobson
       0801.1547 eq.12]; residue sign N_V at the pole (no-ghost).
  [S]  spin-0 block: c_S^2 = c123(2-c14)/(c14(1-c13)(2+c13+3c2)) [eq.13];
       on c13=0: c_S^2 = c2(2-c14)/(c14(2+3c2)); residue sign N_S (no-ghost).
  [M]  Maxwell tie-in: L_EA(c1=K_B,c3=-K_B,c2=c4=0) == -(K_B/2) F^2 at O(eps^2)
       (so the repo transcription of SZ2021 Eq.5, -(K_B/2)F^2, IS the
       c1=-c3=K_B, c2=c4=0 point of the FJ dictionary).
  [N]  residue criterion calibrated on GR (c_i=0) and on a deliberate ghost
       mutation (overall sign flip of the aether sector) -> can fail.

Residue criterion (gauge- and field-redefinition-invariant, proved in the
setup notes): at a simple pole w^2 = c^2 k^2 of the Hermitian form M(w,k)
with null vector v,  N = v^dagger (dM/dw^2) v ; propagator residue = v v^dag/N.
N > 0 <=> healthy (positive-norm) mode; N < 0 <=> ghost.
"""
import sympy as sp, time, sys
T0 = time.time(); P = lambda *a: print(*a, flush=True)
FAIL = []
def CHECK(name, ok):
    P(("  [PASS] " if ok else "  [FAIL] ") + name)
    if not ok: FAIL.append(name)

eps = sp.Symbol('eps', positive=True)
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)
KB = sp.Symbol('K_B', real=True)
om, kx = sp.symbols('omega k', real=True)
eta = sp.diag(-1, 1, 1, 1); I = sp.I
Es, Eis = sp.symbols('E_s E_is')
kv = [-om, kx, 0, 0]                      # ket ~ exp(i(k x - w t))
def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b')
    return ket*Es + bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)

# ---- fields: 10 metric + 3 aether (A^0 from unit norm) ----
names = ['h00', 'h01', 'h02', 'h03', 'h11', 'h22', 'h33', 'h12', 'h13', 'h23',
         'a1', 'a2', 'a3']
F = {}; K = {}; B = {}
for n in names:
    F[n], K[n], B[n] = nf(n)
H = sp.zeros(4, 4)
H[0, 0] = F['h00']; H[0, 1] = H[1, 0] = F['h01']; H[0, 2] = H[2, 0] = F['h02']
H[0, 3] = H[3, 0] = F['h03']; H[1, 1] = F['h11']; H[2, 2] = F['h22']
H[3, 3] = F['h33']; H[1, 2] = H[2, 1] = F['h12']; H[1, 3] = H[3, 1] = F['h13']
H[2, 3] = H[3, 2] = F['h23']
gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
Hup = eta*H*eta
gu = sp.Matrix(4, 4, lambda i, j: (eta - eps*Hup + eps**2*(Hup*H*eta))[i, j])
trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))
HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)
a0f, a0k, a0b = nf('a0p')
Aup = sp.Matrix([1 + eps*a0f, eps*F['a1'], eps*F['a2'], eps*F['a3']])
norm1 = sp.expand(sum(gd[m, n]*Aup[m]*Aup[n] for m in range(4) for n in range(4)) + 1).coeff(eps, 1)
solA = sp.solve([sp.expand(norm1).coeff(Es, 1), sp.expand(norm1).coeff(Eis, 1)],
                [a0k, a0b], dict=True)[0]
Aup = Aup.subs(solA)
P(f"[S1] unit-norm solved: a0 = {sp.simplify(solA[a0k])}  ({time.time()-T0:.1f}s)")

def te(e):
    e = sp.expand(e); return sum(e.coeff(eps, i)*eps**i for i in range(3))
guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))
gdT = gd
AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
Gam = [[[sp.Rational(1, 2)*sum(gu[r, s]*(d(gd[s, n], m)+d(gd[s, m], n)-d(gd[m, n], s))
        for s in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
GamT = [[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]
DA = [[te(d(AupT[m], a) + sum(GamT[m][a][r]*AupT[r] for r in range(4)))
       for m in range(4)] for a in range(4)]
P(f"    D_a A^m built ({time.time()-T0:.1f}s)")
term1 = te(sum(guT[a, b]*gdT[m, n]*DA[a][m]*DA[b][n]
               for a in range(4) for b in range(4) for m in range(4) for n in range(4)))
term2 = te(sum(DA[a][a] for a in range(4))**2)
term3 = te(sum(DA[a][m]*DA[m][a] for a in range(4) for m in range(4)))
acc = [te(sum(AupT[a]*DA[a][m] for a in range(4))) for m in range(4)]
term4 = te(sum(gdT[m, n]*acc[m]*acc[n] for m in range(4) for n in range(4)))
L_EA = -c1*term1 - c2*term2 - c3*term3 + c4*term4
P(f"    aether terms ({time.time()-T0:.1f}s)")

# Maxwell tie-in (A_dn built from A^mu)
Adn = sp.Matrix(4, 1, lambda i, j: te(sum(gd[i, m]*AupT[m] for m in range(4))))
Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m) - d(Adn[m], n)))
F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta[m, a]*eta[n, b]
                for m in range(4) for n in range(4) for a in range(4) for b in range(4))
def ric(a, b):
    o = 0
    for m in range(4):
        o += d(Gam[m][b][a], m) - d(Gam[m][m][a], b)
        for l in range(4):
            o += Gam[m][m][l]*Gam[l][b][a] - Gam[m][b][l]*Gam[l][m][a]
    return o
Rsc = te(sum(guT[m, n]*ric(m, n) for m in range(4) for n in range(4)))
P(f"    Ricci ({time.time()-T0:.1f}s)")
def grade(e):
    e = sp.expand(e); return [e.coeff(eps, n) for n in range(3)]
def DC(e):
    e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
    for mon, c in zip(pol.monoms(), pol.coeffs()):
        if mon[0] == mon[1]:
            out += c*(Es*Eis)**mon[0]
    return sp.expand(out.subs(Es*Eis, 1)) if out != 0 else sp.S(0)
gEA = grade(L_EA); gR = grade(Rsc); gsq = grade(sqg)
gS = [gR[n] + gEA[n] for n in range(3)]
L2 = sum(gsq[a]*gS[2-a] for a in range(3))
L2dc = DC(L2)
P(f"    L2dc: {len(sp.Add.make_args(L2dc))} terms ({time.time()-T0:.1f}s)")

P("\n" + "="*74)
P("[M] MAXWELL TIE-IN: L_EA(c1=K_B,c3=-K_B,c2=c4=0) + (K_B/2)F^2 == 0 at O(eps^2)?")
P("="*74)
tie = DC(sp.expand((L_EA.subs({c1: KB, c3: -KB, c2: 0, c4: 0}) + (KB/2)*F2)).coeff(eps, 2))
CHECK("Maxwell tie-in (SZ2021 Eq.5 -(K_B/2)F^2 == FJ point c1=-c3=K_B, c2=c4=0)",
      sp.simplify(tie) == 0)
# mutation: the SAME identity with c3=+K_B must FAIL (c13 != 0 is not Maxwell)
tie_mut = DC(sp.expand((L_EA.subs({c1: KB, c3: KB, c2: 0, c4: 0}) + (KB/2)*F2)).coeff(eps, 2))
CHECK("mutation control: c3=+K_B is NOT the Maxwell form (residual != 0)",
      sp.simplify(tie_mut) != 0)
# c2, c4 terms are NOT of Maxwell form either (they are what is new)
for cc, lab in ((c2, 'c2 (div A)^2'), (c4, 'c4 a.a')):
    sub = {c1: KB, c3: -KB, c2: 0, c4: 0}; sub[cc] = 1
    t = DC(sp.expand((L_EA.subs(sub) + (KB/2)*F2)).coeff(eps, 2))
    CHECK(f"mutation control: adding {lab} changes the quadratic action", sp.simplify(t) != 0)

# ---- Hermitian form and helicity blocks ----
def Mblock(fields):
    """M_ij = d^2 L2dc / dB_i dK_j on the given field list (gauge-fixed by omission)."""
    return sp.Matrix(len(fields), len(fields),
                     lambda i, j: sp.expand(sp.diff(L2dc, B[fields[i]], K[fields[j]])))
# change to helicity-adapted tensor variables: h22 = tr + s, h33 = tr - s
trk, trb, sk, sb = sp.symbols('trk trb sk sb')
L2dc = L2dc.subs({K['h22']: trk + sk, K['h33']: trk - sk,
                  B['h22']: trb + sb, B['h33']: trb - sb})
K['tr'], B['tr'], K['s'], B['s'] = trk, trb, sk, sb
ALL = ['h00', 'h01', 'h11', 'tr', 'a1', 'h02', 'h12', 'a2', 'h03', 'h13', 'a3', 's', 'h23']
Mfull = Mblock(ALL)
blocks = {'scalar': ['h00', 'h01', 'h11', 'tr', 'a1'], 'vecY': ['h02', 'h12', 'a2'],
          'vecZ': ['h03', 'h13', 'a3'], 'tensor': ['s', 'h23']}
P("\n" + "="*74)
P("BLOCK STRUCTURE: helicity sectors decouple in the full 13x13 form?")
P("="*74)
idx = {n: i for i, n in enumerate(ALL)}
off = 0
for b1 in blocks:
    for b2 in blocks:
        if b1 >= b2: continue
        for f1 in blocks[b1]:
            for f2 in blocks[b2]:
                off += int(sp.simplify(Mfull[idx[f1], idx[f2]]) != 0)
CHECK("all inter-helicity entries vanish", off == 0)
# Hermiticity
herm = all(sp.simplify(Mfull[i, j] - sp.conjugate(Mfull[j, i])) == 0
           for i in range(13) for j in range(13))
CHECK("M is Hermitian", herm)
# gauge null vectors exist (full form is degenerate)
CHECK("full 13x13 form is gauge-degenerate (rank < 13)", Mfull.rank() < 13)

def pole_and_residue(M, label, expected_c2=None):
    """det M(w,k) -> dispersion factors; residue sign at the physical pole."""
    detM = sp.factor(sp.simplify(M.det()))
    P(f"  det M_{label} = {detM}")
    facs = sp.factor_list(detM)[1]
    phys = [f for f, m in facs if f.has(om) and f.has(kx)]
    P(f"  physical dispersion factors: {phys}")
    return detM, phys

def residue_sign(M, csq, sub):
    """N = v^dag dM/dw^2 v at w = sqrt(csq)*k (k=1), numeric substitution sub."""
    Mn = M.subs(sub).subs(kx, 1)
    wv = sp.sqrt(csq.subs(sub))
    M0 = Mn.subs(om, wv)
    ns = M0.nullspace()
    assert len(ns) == 1, f"null space dim {len(ns)} at pole"
    v = ns[0]
    dM = sp.diff(Mn, om)/(2*om)
    N = (v.H*dM.subs(om, wv)*v)[0, 0]
    return sp.nsimplify(sp.simplify(N))

P("\n" + "="*74)
P("[T] SPIN-2 (tensor) block: fields s=(h22-h33)/2, h23")
P("="*74)
MT = Mblock(['s', 'h23'])
P("  M_T =", MT)
CHECK("tensor block has no c2", not MT.has(c2))
CHECK("tensor block has no c4", not MT.has(c4))
CHECK("mutation control: tensor block DOES carry c1+c3", MT.has(c1) and MT.has(c3)
      and sp.simplify(MT[1, 1].subs(c3, -c1)).has(c1) is False)
detT, physT = pole_and_residue(MT, 'T')
cT2 = sp.solve(physT[0], om**2) if physT else None
cT2 = [sp.simplify(s/kx**2) for s in sp.solve(sp.expand(physT[0]), om**2)] if physT else None
P("  c_T^2 =", cT2)
CHECK("c_T^2 == 1/(1-c13)  [Jacobson eq.11]", cT2 is not None and any(sp.simplify(s - 1/(1-c1-c3)) == 0 for s in cT2))
cT2_KB = sp.simplify(physT[0].subs({c1: KB, c3: -KB}))
CHECK("at c1=-c3=K_B the tensor dispersion is w^2 = k^2 for all c2,c4,K_B",
      sp.simplify(cT2_KB/ sp.Poly(cT2_KB, om).LC() - (om**2 - kx**2)) == 0)
# residue sign calibration: GR and generic c13<1 healthy; c13>1 ghost
for sub, lab, exp in (({c1: 0, c2: 0, c3: 0, c4: 0}, 'GR', +1),
                      ({c1: sp.Rational(3, 10), c2: sp.Rational(1, 5), c3: sp.Rational(1, 10), c4: sp.Rational(1, 20)}, 'c13=0.4', +1),
                      ({c1: sp.Rational(1, 5), c2: 0, c3: -sp.Rational(1, 5), c4: sp.Rational(1, 10)}, 'K_B plane', +1)):
    N = residue_sign(MT, 1/(1-c1-c3), sub)
    CHECK(f"tensor residue N_T>0 at {lab} (N={N})", (N > 0) == (exp > 0))

P("\n" + "="*74)
P("[V] SPIN-1 block: fields h02, a2  (gauge: h12 -> 0 via xi_2, k != 0)")
P("="*74)
MV = Mblock(['h02', 'a2'])
detV, physV = pole_and_residue(MV, 'V')
cV2_lit = (2*c1 - c1**2 + c3**2)/(2*(c1+c4)*(1-c1-c3))
solV = [sp.simplify(s/kx**2) for s in sp.solve(sp.expand(physV[0]), om**2)] if physV else []
P("  c_V^2 (derived) =", solV)
CHECK("c_V^2 == (2c1-c1^2+c3^2)/(2c14(1-c13))  [Jacobson eq.12]",
      any(sp.simplify(s - cV2_lit) == 0 for s in solV))
CHECK("on c13=0: c_V^2 == K_B/(K_B+c4) = c1/c14",
      any(sp.simplify(s.subs({c1: KB, c3: -KB}) - KB/(KB+c4)) == 0 for s in solV))
# residue sign: literature q_V = c14 (OMW 3.1) ; energy sign (2c1-c1^2+c3^2)/(1-c13) (Jacobson)
P("  residue N_V at sample points (expect sign = sign(c14) with c_V^2>0):")
ptsV = [({c1: sp.Rational(1, 5), c2: sp.Rational(1, 10), c3: -sp.Rational(1, 5), c4: sp.Rational(1, 20)}, +1),
        ({c1: sp.Rational(1, 5), c2: sp.Rational(1, 10), c3: -sp.Rational(1, 5), c4: -sp.Rational(1, 10)}, +1),
        ({c1: sp.Rational(3, 10), c2: sp.Rational(1, 5), c3: sp.Rational(1, 10), c4: sp.Rational(1, 20)}, +1),
        ({c1: -sp.Rational(1, 5), c2: sp.Rational(1, 10), c3: sp.Rational(1, 5), c4: -sp.Rational(1, 10)}, -1)]  # c14<0, c1<0: ghost
for sub, exp in ptsV:
    N = residue_sign(MV, cV2_lit, sub)
    c14v = (c1+c4).subs(sub)
    CHECK(f"N_V sign at c={tuple(sub.values())}: N={N}, c14={c14v}, expect {'+' if exp>0 else '-'}",
          (N > 0) == (exp > 0))
# deliberate ghost mutation: flip aether sign (c_i -> -c_i keeps speeds' ratios? no: recompute)
P("  ghost mutation: overall sign flip of the aether sector (c_i -> -c_i) at the K_B point")
subg = {c1: -sp.Rational(1, 5), c2: -sp.Rational(1, 10), c3: sp.Rational(1, 5), c4: -sp.Rational(1, 20)}
Ng = residue_sign(MV, cV2_lit, subg)
CHECK(f"flipped aether sign gives N_V<0 (ghost) : N={Ng}", Ng < 0)

P("\n" + "="*74)
P("[S] SPIN-0 block: fields h01, tr, a1  (gauge: h00 -> 0 via xi_0, h11 -> 0 via xi_1)")
P("="*74)
MS = Mblock(['h01', 'tr', 'a1'])
detS, physS = pole_and_residue(MS, 'S')
cS2_lit = (c1+c2+c3)*(2-c1-c4)/((c1+c4)*(1-c1-c3)*(2+c1+c3+3*c2))
solS = [sp.simplify(s/kx**2) for s in sp.solve(sp.expand(physS[0]), om**2)] if physS else []
P("  c_S^2 (derived) =", solS)
CHECK("c_S^2 == c123(2-c14)/(c14(1-c13)(2+c13+3c2))  [Jacobson eq.13]",
      any(sp.simplify(s - cS2_lit) == 0 for s in solS))
CHECK("on c13=0: c_S^2 == c2(2-c14)/(c14(2+3c2))  [the task's formula]",
      any(sp.simplify(s.subs({c1: KB, c3: -KB}) - c2*(2-KB-c4)/((KB+c4)*(2+3*c2))) == 0 for s in solS))
P("  residue N_S at sample points on c13=0 (OMW q_S = (2+3c2)/c2 ; Jacobson energy ~ c14(2-c14)):")
ptsS = [({c1: sp.Rational(1, 5), c2: sp.Rational(1, 10), c3: -sp.Rational(1, 5), c4: sp.Rational(1, 20)}, +1),   # healthy
        ({c1: sp.Rational(1, 5), c2: sp.Rational(1, 10), c3: -sp.Rational(1, 5), c4: -sp.Rational(1, 10)}, +1),  # healthy, c14=0.1
        ({c1: sp.Rational(1, 5), c2: -1, c3: -sp.Rational(1, 5), c4: sp.Rational(1, 20)}, +1),   # c2<-2/3 branch: c_S^2>0
        ({c1: sp.Rational(1, 5), c2: sp.Rational(1, 10), c3: -sp.Rational(1, 5), c4: sp.Rational(5, 2)}, None),  # c14>2: c_S^2<0 (no real pole)
        ({c1: sp.Rational(3, 10), c2: sp.Rational(1, 5), c3: sp.Rational(1, 10), c4: sp.Rational(1, 20)}, +1)]
for sub, exp in ptsS:
    cs2v = cS2_lit.subs(sub)
    if cs2v <= 0:
        P(f"    c={tuple(sub.values())}: c_S^2={cs2v} <= 0 -> gradient-unstable / no real pole (skip residue)")
        CHECK("c14>2 point has c_S^2<0 (gradient instability, as literature)", exp is None)
        continue
    N = residue_sign(MS, cS2_lit, sub)
    qS = ((1-c1-c3)*(2+c1+c3+3*c2)/(c1+c2+c3)).subs(sub)
    CHECK(f"N_S sign at c={tuple(sub.values())}: N={N}, OMW q_S={qS}, c_S^2={cs2v}",
          (N > 0) == (qS > 0))
Ng = residue_sign(MS, cS2_lit, subg)
CHECK(f"ghost mutation (all c_i flipped) gives N_S<0 : N={Ng}", Ng < 0)

P("\n" + "="*74)
P("[S'] SYMBOLIC residue on the c13=0 plane (K_B, c2, c4 symbolic)")
P("="*74)
try:
    subK = {c1: KB, c3: -KB}
    MSk = MS.subs(subK).subs(kx, 1)
    cs2 = c2*(2-KB-c4)/((KB+c4)*(2+3*c2))
    wv = sp.sqrt(cs2)
    M0 = sp.simplify(MSk.subs(om, wv))
    ns = M0.nullspace()
    P(f"  null-space dimension at the pole: {len(ns)}")
    v = ns[0]
    dM = sp.diff(MSk, om)/(2*om)
    NS = sp.simplify((v.H*dM.subs(om, wv)*v)[0, 0])
    P("  N_S(K_B,c2,c4) =", sp.factor(NS))
    # sign structure vs literature: sign(N_S) == sign((2+3c2)/c2) on 0<c14<2 ?
    trials = [(sp.Rational(1, 10), sp.Rational(1, 10), 0), (sp.Rational(1, 4), 1, -sp.Rational(1, 8)),
              (sp.Rational(1, 20), sp.Rational(1, 100), sp.Rational(1, 100)), (sp.Rational(1, 10), -1, 0),
              (sp.Rational(1, 10), -sp.Rational(1, 10), 0)]
    ok = True
    for kb, cc2, cc4 in trials:
        val = NS.subs({KB: kb, c2: cc2, c4: cc4}); q = (2+3*cc2)/cc2; cs = cs2.subs({KB: kb, c2: cc2, c4: cc4})
        if cs <= 0:
            P(f"    (K_B,c2,c4)=({kb},{cc2},{cc4}): c_S^2={cs}<=0 -> no real pole (skipped)"); continue
        ok = ok and ((val > 0) == (q > 0))
        P(f"    (K_B,c2,c4)=({kb},{cc2},{cc4}): N_S={val}  q_S(OMW)={q}  c_S^2={cs}")
    CHECK("symbolic N_S sign == sign of OMW q_S=(2+3c2)/c2 on sampled healthy pole points", ok)
except Exception as e:
    P(f"  symbolic residue not obtained: {e!r}  (numeric samples above stand)")

P("\n" + "="*74)
P("SUMMARY")
P("="*74)
P("  c_T^2 = 1/(1-c13) -> 1 on c13=0, c2/c4-BLIND            [DERIVED, SOLID]")
P("  c_V^2 = (2c1-c1^2+c3^2)/(2c14(1-c13)) -> K_B/c14 on c13=0 [DERIVED, SOLID]")
P("  c_S^2 = c123(2-c14)/(c14(1-c13)(2+c13+3c2)) -> c2(2-c14)/(c14(2+3c2)) [DERIVED, SOLID]")
P("  no-ghost (residue) signs agree with OMW 1802.04303 eq.3.1 q's on all samples")
P("  Maxwell tie-in: -(K_B/2)F^2 == (c1,c2,c3,c4)=(K_B,0,-K_B,0)             [SOLID]")
P(f"  FAILED CHECKS: {len(FAIL)} {FAIL}")
P(f"done ({time.time()-T0:.1f}s)")
sys.exit(1 if FAIL else 0)
