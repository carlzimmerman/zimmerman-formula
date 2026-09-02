#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gen_aest_dispersion_health.py -- HEALTH of the generalized completion (companion to gate 4).
============================================================================================
Same action as gen_aest_alpha1_c2c4.py (AeST + c2 (D.A)^2 + c4 a.a), but now the vacuum
perturbation spectrum about the UNBOOSTED background A^mu=(1,0,0,0), phi = Q0 t, Minkowski,
plane wave e^{i(k x - omega t)} along xhat, no source. Sectors by helicity about k:
  spin-2 : s23 (and s22)            -> c_T^2 (must be 1: c2, c4 tensor-blind)
  spin-1 : {B2 = h02, a2}           -> kinetic coefficient of the transverse aether and c_V^2
  spin-0 : {Psi, Phi, s22, a1, chi} -> kinetic-matrix signature (no ghost) and speeds
KEY QUESTION: in pure EA the boosted-response coefficient (alpha_1 = -4 c14) and the rest-frame
spin-1 kinetic coefficient are the SAME c14. The AeST drag 2(2-K_B) a.grad(phi) enters the
boosted sector only (grad phi_bg ~ w_b), so here they may DIFFER. This script gives the
rest-frame spin-1 kinetic coefficient as a function of (K_B, c4, J_Y, K2): if it is c14 = K_B + c4
while alpha_1 = -4 eta_K with eta_K != c14, then the alpha_1 = 0 locus is healthy iff c14* > 0.
Checks that can fail: c_T^2 == 1; pure-EA limits reproduce the textbook spin-1/spin-0 results
(c_V^2 = c1/c14 at c13=0; c_S^2 = c2(2-c14)/(c14(2+3c2)) at c13=0 when the scalar is frozen).
"""
import sympy as sp, time, pickle, os, sys
T0 = time.time(); P = lambda *a: print(*a, flush=True)
SC = os.environ.get('SCRATCH', '/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/2842cbcf-b95e-45e6-8ed2-7f6c29341e4f/scratchpad') + '/'
os.makedirs(SC, exist_ok=True); CACHE = SC + 'L2dc_gen_disp.pkl'
FAILS = []
def check(name, ok, detail=''):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ''))
    if not ok: FAILS.append(name)
eps = sp.Symbol('eps', positive=True)
KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)
C2, C4 = sp.symbols('c2 c4', real=True)
LAM = sp.Symbol('Lambda', real=True)
om, kx = sp.symbols('omega k_x', real=True)
eta = sp.diag(-1, 1, 1, 1); I = sp.I
Es, Eis = sp.symbols('E_s E_is')
kv = [-om, kx, 0, 0]          # e^{i(k x - omega t)}: d_t -> -i omega on the ket
def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b'); return ket*Es + bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)
Psi, Psik, Psib = nf('Psi'); Phi, Phik, Phib = nf('Phi')
B2f, B2k, B2b = nf('B2'); B3f, B3k, B3b = nf('B3')
s22, s22k, s22b = nf('s22'); s23, s23k, s23b = nf('s23')
a1f, a1k, a1b = nf('a1'); a2f, a2k, a2b = nf('a2'); a3f, a3k, a3b = nf('a3')
chif, chik, chib = nf('chi'); a0f, a0k, a0b = nf('a0p')
KETS = [Psik, Phik, B2k, B3k, s22k, s23k, a1k, a2k, a3k, chik]
BRAS = [Psib, Phib, B2b, B3b, s22b, s23b, a1b, a2b, a3b, chib]
if os.path.exists(CACHE) and '--rebuild' not in sys.argv:
    L2dc = pickle.load(open(CACHE, 'rb')); P(f"[cache] loaded {CACHE}")
else:
    Aup_bg = sp.Matrix([1, 0, 0, 0]); Adn_bg = eta*Aup_bg; dphi_bg = -Q0*Adn_bg
    H = sp.zeros(4, 4)
    H[0, 0] = -2*Psi; H[0, 2] = B2f; H[2, 0] = B2f; H[0, 3] = B3f; H[3, 0] = B3f
    H[1, 1] = -2*Phi; H[2, 2] = -2*Phi + s22; H[3, 3] = -2*Phi - s22; H[2, 3] = s23; H[3, 2] = s23
    gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n]); Hup = eta*H*eta
    gu = sp.Matrix(4, 4, lambda i, j: (eta - eps*Hup + eps**2*(Hup*H*eta))[i, j])
    trH = sum(eta[m, n]*H[m, n] for m in range(4) for n in range(4))
    HH = sum(Hup[m, n]*H[m, n] for m in range(4) for n in range(4))
    sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)
    Adn = sp.Matrix([Adn_bg[0]-eps*a0f, eps*a1f, eps*a2f, eps*a3f])
    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
    C1c = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
    solA = sp.solve([sp.expand(C1c).coeff(Es, 1), sp.expand(C1c).coeff(Eis, 1)], [a0k, a0b], dict=True)[0]
    a0f = a0f.subs(solA)
    Adn = sp.Matrix([Adn_bg[0]-eps*a0f, eps*a1f, eps*a2f, eps*a3f])
    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
    dphi = sp.Matrix([dphi_bg[m] + eps*d(chif, m) for m in range(4)])
    def te(e):
        e = sp.expand(e); return sum(e.coeff(eps, i)*eps**i for i in range(3))
    guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n])); gdT = sp.Matrix(4, 4, lambda m, n: te(gd[m, n]))
    AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
    Gam = [[[sp.Rational(1, 2)*sum(gu[r, s]*(d(gd[s, n], m)+d(gd[s, m], n)-d(gd[m, n], s)) for s in range(4))
             for n in range(4)] for m in range(4)] for r in range(4)]
    GamT = [[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]
    dphiT = sp.Matrix(4, 1, lambda i, j: te(dphi[i]))
    Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m)-d(Adn[m], n)))
    F1 = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
    F2 = eps**2*sum(F1[m, n]*F1[a, b]*eta[m, a]*eta[n, b] for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    Jup = [te(sum(AupT[nu]*(d(AupT[al], nu)+sum(GamT[al][nu][r]*AupT[r] for r in range(4))) for nu in range(4))) for al in range(4)]
    term4 = te(sum(gdT[m, n]*Jup[m]*Jup[n] for m in range(4) for n in range(4)))
    divA = te(sum(d(AupT[a], a) + sum(GamT[a][a][r]*AupT[r] for r in range(4)) for a in range(4)))
    term2 = te(divA**2)
    Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
    Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
    Yc = te(sum((guT[m, n]+AupT[m]*AupT[n])*dphiT[m]*dphiT[n] for m in range(4) for n in range(4)))
    Kq = -2*LAM + K2*te((Qc - Q0)**2)
    P(f"    operators ({time.time()-T0:.1f}s)")
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
    gF2 = grade(F2); gJ = grade(Jdphi); gY = grade(Yc); gK = grade(Kq)
    g2 = grade(term2); g4 = grade(term4); gsq = grade(sqg); gR = grade(Rsc)
    gS = [gR[n] - (2*LAM if n == 0 else 0) - (KB/2)*gF2[n] - C2*g2[n] + C4*g4[n]
          + 2*(2-KB)*gJ[n] - (2-KB)*gY[n] - gK[n] for n in range(3)]
    L2 = sp.expand(sum(gsq[a]*gS[2-a] for a in range(3)) - (2-KB)*JY*gY[2])
    def DC(e):
        e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
        for mon, c in zip(pol.monoms(), pol.coeffs()):
            if mon[0] == mon[1]: out += c*(Es*Eis)**mon[0]
        return out.subs(Es*Eis, 1) if out != 0 else out
    L2dc = DC(L2); pickle.dump(L2dc, open(CACHE, 'wb'))
    P(f"    L2dc built+cached: {len(sp.Add.make_args(L2dc))} terms ({time.time()-T0:.1f}s)")

L2dc = L2dc.subs(LAM, 0)
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}
def sector(keep):
    """Hermitian form restricted to a helicity sector: kets/bras outside `keep` set to 0."""
    zero = {k: 0 for k in KETS if k not in keep}; zero.update({b: 0 for b in BRAS if sp.Symbol(str(b)[:-1]+'k') not in keep})
    return {b: sp.expand(eq[b].subs(zero)) for b in BRAS if sp.Symbol(str(b)[:-1]+'k') in keep}
def kin_matrix(eqs, kets):
    """M(omega,k) with eqs = M . kets ; returns M."""
    M, _ = sp.linear_eq_to_matrix(list(eqs.values()), kets); return M

P(""); P("="*76); P("SPIN-2: c_T^2 from the s23 mode (c2, c4 must be tensor-blind)"); P("="*76)
Mt = kin_matrix(sector([s23k]), [s23k]); disp_t = sp.factor(Mt[0, 0])
P(f"  s23 equation coefficient: {disp_t}")
cT2 = sp.solve(sp.Eq(disp_t, 0), om**2)
P(f"  omega^2 = {cT2}")
check("c_T^2 == 1 for all K_B, c2, c4, J_Y, K2", all(sp.simplify(s - kx**2) == 0 for s in cT2))

P(""); P("="*76); P("SPIN-1: {B2 = h02, a2} transverse sector"); P("="*76)
Mv = kin_matrix(sector([B2k, a2k]), [B2k, a2k]); Mv = Mv.applyfunc(sp.factor)
P(f"  M = {Mv.tolist()}")
detv = sp.factor(Mv.det()); P(f"  det M = {detv}")
sols_v = sp.solve(sp.Eq(detv, 0), om**2); P(f"  omega^2 solutions: {sols_v}")
# integrate out B2 (constraint): effective a2 equation
B2sol = sp.solve(Mv[0, 0]*B2k + Mv[0, 1]*a2k, B2k)
eff = sp.factor(sp.simplify((Mv[1, 0]*B2sol[0] + Mv[1, 1]*a2k)/a2k)) if B2sol else None
P(f"  effective a2 kernel after eliminating h02: {eff}")
if eff is not None:
    num = sp.numer(sp.together(eff)); kin = sp.factor(sp.Poly(sp.expand(num), om).coeff_monomial(om**2)); grad = sp.factor(sp.Poly(sp.expand(num), om).coeff_monomial(om**0))
    P(f"  spin-1 kinetic coefficient (omega^2):   {kin}")
    P(f"  spin-1 gradient coefficient (omega^0):  {grad}")
    cV2 = sp.factor(-grad/kin/kx**2) if kin != 0 else None; P(f"  c_V^2 = {cV2}")
    check("spin-1 kinetic coefficient is c14 = K_B + c4 up to a positive factor (drag-blind at rest)",
          sp.simplify(sp.factor(kin/(KB+C4))).is_number if kin != 0 else False, f"kin/(K_B+c4) = {sp.simplify(kin/(KB+C4)) if kin != 0 else None}")
    check("pure-EA anchor: c_V^2 -> c1/c14 = K_B/(K_B+c4) (c13=0 textbook)", cV2 is not None and sp.simplify(cV2 - KB/(KB+C4)) == 0)
    check("spin-1 sector independent of J_Y, K2, c2, Q0 at rest", not any(sp.sympify(eff).has(s) for s in (JY, K2, C2, Q0)))

P(""); P("="*76); P("SPIN-0: {Psi, Phi, s22, a1, chi} longitudinal sector"); P("="*76)
Ms = kin_matrix(sector([Psik, Phik, s22k, a1k, chik]), [Psik, Phik, s22k, a1k, chik])
dets = sp.factor(Ms.det()); P(f"  det M(omega,k) = {dets}")
sols_s = sp.solve(sp.Eq(dets, 0), om**2); P(f"  omega^2 roots (propagating spin-0 modes): {sols_s}")
# pure-EA frozen-scalar anchor: send the scalar stiff (J_Y->oo) and Q0->0, compare with c_S^2 = c2(2-c14)/(c14(2+3c2)) at c13=0
for s in sols_s:
    s0 = sp.simplify(sp.limit(sp.simplify(s.subs(Q0, 0)), JY, sp.oo)/kx**2)
    P(f"    J_Y->oo, Q0->0 limit of a root / k^2: {s0}")
cS2_EA = C2*(2-(KB+C4))/((KB+C4)*(2+3*C2))
P(f"  textbook pure-EA c_S^2 at c13=0: {sp.factor(cS2_EA)}")
check("some spin-0 root reproduces the pure-EA c_S^2 in the frozen-scalar limit",
      any(sp.simplify(sp.limit(sp.simplify(s.subs(Q0, 0)), JY, sp.oo)/kx**2 - cS2_EA) == 0 for s in sols_s))
# kinetic-matrix signature at the alpha_1=0 candidate locus is evaluated numerically by the caller
pickle.dump({'spin1_kin': sp.srepr(kin) if eff is not None else None, 'spin1_cV2': sp.srepr(cV2) if eff is not None else None,
             'spin0_det': sp.srepr(dets), 'spin0_roots': [sp.srepr(s) for s in sols_s]}, open(SC+'gen_aest_dispersion.pkl', 'wb'))
P(""); P(f"FAILED CHECKS: {FAILS if FAILS else 'none'}"); P(f"done ({time.time()-T0:.1f}s)")
sys.exit(1 if FAILS else 0)
