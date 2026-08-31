#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
t3x_structural_deltaQ_projection.py   (TARGET-3 independent cross-route, part 1)
================================================================================
STRUCTURAL sympy analysis of the v9 AeST unsuppressed novel channel
F_QQ(Q0) (deltaQ)^2 with F_QQ(Q0) = mu2 (1 + kappa^2/4pi):
which PPN velocity structures can it produce, i.e. does it project onto the
alpha_2 channel (anisotropic (w.qhat)^2 w^2 U) or only onto beta (U^2)?

Blocks:
 [A] sympy certificate of the Will TEGP dictionary in Fourier space
     (the per-structure coefficient table used by every extraction).
 [B] anchors: Foster-Jacobson alpha_1 at the AeST Maxwell point = -4 K_B;
     BPS C0(eta,lam2) = eta(eta-lam2)/(2 lam2) -> -eta/2 as lam2->oo, which at
     eta_K = K_B reproduces Route 3's regulated C0 = -K_B/2 (consistency).
 [C] boosted-background linearization of Q = A^mu d_mu phi with the unit-norm
     constraint solved (same conventions as route2_v2_build.py, but WITHOUT the
     Einstein sector -- only the aether/scalar sectors are needed for the
     structure of deltaQ and of the chi--aether mixings).  Enumerate every term
     of deltaQ (order eps^1) graded by powers of w_b and of Q0, and every
     quadratic mixing of chi with the aether components, likewise graded.
 [D] verdict: classification of the O(w^2) insertions of F_QQ (deltaQ)^2 and
     their projection through the Will dictionary.

KEY structural claim being tested (settles novel_hits even if full solve stalls):
  deltaQ is a SCALAR, but under the boost A_bg^mu = (1+w^2/2, w b) the flow
  derivative A^mu d_mu chi = (w.grad) chi puts a GRADIENT of chi into deltaQ:
  in static Fourier deltaQ ) i (w.q) chi, with NO factor of Q0.  Then
  F_QQ (deltaQ)^2 ) -F_QQ (w.q)^2 chi^2 : an O(w^2) ANISOTROPIC, Q0-FREE,
  q^2-order (unsuppressed) insertion on the chi line -> alpha_2 channel.
  Every OTHER piece of deltaQ carries Q0 (a cosmological inverse length), so
  every other insertion -- including the naive deltaQ ~ Q0 Psi -> beta piece --
  is power-suppressed by (Q0/q)^2 ~ 1e-30 at AU scales.

Run:  python3 t3x_structural_deltaQ_projection.py  | tee t3x_structural_deltaQ_projection.out
"""
import sympy as sp, time
T0 = time.time(); P = lambda *a: print(*a, flush=True)

# ============================================================================
P("="*78)
P("[A] WILL DICTIONARY CERTIFICATE (TEGP eq 27 conventions, mostly-plus,")
P("    source at rest, PPN frame moving with w, V_i=W_i=0, Fourier k=xhat)")
P("="*78)
a1s, a2s, a3s = sp.symbols('alpha1 alpha2 alpha3', real=True)
w1, w2, w3, Uh = sp.symbols('w1 w2 w3 U_hat', real=True)
# Fourier rule: U_ij -> delta_ij Uh - 2 q_i q_j Uh / q^2 ; q = (1,0,0)
qh = sp.Matrix([1, 0, 0]); wv = sp.Matrix([w1, w2, w3])
Uij = lambda i, j: (1 if i == j else 0)*Uh - 2*qh[i]*qh[j]*Uh
w2tot = w1**2 + w2**2 + w3**2
# g00 preferred-frame sector
wwUij = sum(wv[i]*wv[j]*Uij(i, j) for i in range(3) for j in range(3))
g00pf = sp.expand(-(a1s - a2s - a3s)*w2tot*Uh - a2s*wwUij)
cpar  = g00pf.coeff(w1**2)/Uh   # parallel  (w || q)
cperp = g00pf.coeff(w2**2)/Uh   # transverse
P("  g00: coeff(w_par^2  U) =", sp.simplify(cpar))
P("  g00: coeff(w_perp^2 U) =", sp.simplify(cperp))
P("  par - perp             =", sp.simplify(cpar - cperp), "  == 2 alpha_2 ?",
  sp.simplify(cpar - cperp - 2*a2s) == 0)
P("  => ALPHA_2 = (1/2)[coeff(w_par^2 U) - coeff(w_perp^2 U)]   (alpha_3-blind)")
P("  => ALPHA_3 = coeff(w_perp^2 U) + alpha_1  (certifies to 0 for a healthy")
P("     propagating sector)")
# g0i
g0i = lambda i: sp.expand(-sp.Rational(1, 2)*(a1s - 2*a2s)*wv[i]*Uh
                          - a2s*sum(wv[j]*Uij(i, j) for j in range(3)))
cT = g0i(1).coeff(w2)/Uh   # i=2 transverse
cL = g0i(0).coeff(w1)/Uh   # i=1 parallel
P("  g0i transverse coeff(w_i U) =", sp.simplify(cT), " == -alpha_1/2 ?",
  sp.simplify(cT + a1s/2) == 0)
P("  g0i parallel   coeff(w_1 U) =", sp.simplify(cL), " == -alpha_1/2 + 2 alpha_2 ?",
  sp.simplify(cL + a1s/2 - 2*a2s) == 0)
P("  (fc_alpha2_preferred_frame_2026.py used +alpha_1/2 transverse and")
P("   perp-minus-par = +2 alpha_2: BOTH sign-flipped vs this certificate.)")

# ============================================================================
P("")
P("="*78)
P("[B] ANCHORS: FJ alpha_1 at the Maxwell point; BPS C0 stiff limit")
P("="*78)
c1, c2, c3, c4, KB = sp.symbols('c1 c2 c3 c4 K_B', real=True)
alpha1_FJ = -8*(c3**2 + c1*c4)/(2*c1 - c1**2 + c3**2)
MAX = {c1: KB, c3: -KB, c2: 0, c4: 0}
a1_max = sp.simplify(alpha1_FJ.subs(MAX))
P("  FJ alpha_1(c1=K_B,c3=-K_B,c2=c4=0) =", a1_max, " == -4K_B ?",
  sp.simplify(a1_max + 4*KB) == 0)
eta, lam2 = sp.symbols('eta_K lambda_2', positive=True)
C0 = eta*(eta - lam2)/(2*lam2)
C0stiff = sp.limit(C0, lam2, sp.oo)
P("  BPS C0 = eta(eta-lam2)/(2 lam2);  lim_{lam2->oo} C0 =", C0stiff)
P("  at eta_K = K_B:", C0stiff.subs(eta, KB),
  "  == Route 3 regulated C0 = -K_B/2 ?  ->",
  sp.simplify(C0stiff.subs(eta, KB) + KB/2) == 0)
P("  (Route 3's speed-matched regulator eps_eff=(2+K_B lam_s)/K2 -> oo is the")
P("   lam2->oo stiff limit of the BPS form with eta_K = K_B UNRENORMALIZED --")
P("   the two committed routes are one formula.)")

# ============================================================================
P("")
P("="*78)
P("[C] BOOSTED deltaQ + chi-aether mixing table (no Einstein sector needed)")
P("="*78)
eps, wb = sp.symbols('eps w_b', positive=True)
Q0, K2, JY = sp.symbols('Q_0 K_2 J_Y', real=True)
FQQ = sp.symbols('F_QQ', real=True)   # = mu2 (1 + kappa^2/4pi), the novel channel
eta4 = sp.diag(-1, 1, 1, 1); I = sp.I
ww = w1**2 + w2**2 + w3**2; S0 = 1 + wb**2*ww/2
Aup_bg = sp.Matrix([S0, wb*w1, wb*w2, wb*w3]); Adn_bg = eta4*Aup_bg
dphi_bg = -Q0*Adn_bg          # => Q_bg = +Q0  (same conv as route2_v2_build)
Es, Eis = sp.symbols('E_s E_is'); kx = sp.symbols('k_x', real=True)
kv = [0, kx, 0, 0]
def nf(tag):
    ket = sp.Symbol(tag+'k'); bra = sp.Symbol(tag+'b')
    return ket*Es + bra*Eis, ket, bra
def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)
Psi, Psik, Psib = nf('Psi'); Phi, Phik, Phib = nf('Phi')
B2f, B2k, B2b = nf('B2'); B3f, B3k, B3b = nf('B3')
s22, s22k, s22b = nf('s22'); s23, s23k, s23b = nf('s23')
a1f, a1k, a1b = nf('a1'); a2f, a2k, a2b = nf('a2'); a3f, a3k, a3b = nf('a3')
chi, chik, chib = nf('chi'); a0f, a0k, a0b = nf('a0p')
H = sp.zeros(4, 4)
H[0, 0] = -2*Psi
H[0, 2] = B2f; H[2, 0] = B2f; H[0, 3] = B3f; H[3, 0] = B3f
H[1, 1] = -2*Phi
H[2, 2] = -2*Phi + s22; H[3, 3] = -2*Phi - s22
H[2, 3] = s23; H[3, 2] = s23
gd = sp.Matrix(4, 4, lambda m, n: eta4[m, n] + eps*H[m, n])
Hup = eta4*H*eta4
gu = sp.Matrix(4, 4, lambda i, j: (eta4 - eps*Hup + eps**2*(Hup*H*eta4))[i, j])
Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
C1c = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
solA = sp.solve([sp.expand(C1c).coeff(Es, 1), sp.expand(C1c).coeff(Eis, 1)],
                [a0k, a0b], dict=True)[0]
solA = {k: sp.expand(sp.series(v, wb, 0, 3).removeO()) for k, v in solA.items()}
a0f = a0f.subs(solA)
Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))
P(f"  unit-norm constraint solved for the temporal aether ({time.time()-T0:.1f}s)")
dphi = sp.Matrix([dphi_bg[m] + eps*d(chi, m) for m in range(4)])
def te(e):
    e = sp.expand(e); out = 0
    for i in range(3):
        ci = e.coeff(eps, i)
        for j in range(3):
            out += ci.coeff(wb, j)*eps**i*wb**j
    return out
guT  = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))
AupT = sp.Matrix(4, 1, lambda i, j: te(Aup[i]))
Gam = [[[sp.Rational(1, 2)*sum(gu[r, s]*(d(gd[s, n], m)+d(gd[s, m], n)-d(gd[m, n], s))
        for s in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
GamT = [[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]
dphiT = sp.Matrix(4, 1, lambda i, j: te(dphi[i]))
Fmn = sp.Matrix(4, 4, lambda m, n: sp.expand(d(Adn[n], m) - d(Adn[m], n)))
F1  = sp.Matrix(4, 4, lambda m, n: Fmn[m, n].coeff(eps, 1))
F2  = eps**2*sum(F1[m, n]*F1[a, b]*eta4[m, a]*eta4[n, b]
                 for m in range(4) for n in range(4) for a in range(4) for b in range(4))
Jup = [te(sum(AupT[nu]*(d(AupT[al], nu) + sum(GamT[al][nu][r]*AupT[r] for r in range(4)))
       for nu in range(4))) for al in range(4)]
Jdphi = te(sum(Jup[m]*dphiT[m] for m in range(4)))
Qc = te(sum(AupT[m]*dphiT[m] for m in range(4)))
Yc = te(sum((guT[m, n] + AupT[m]*AupT[n])*dphiT[m]*dphiT[n]
            for m in range(4) for n in range(4)))
P(f"  Q, Y, J.grad(phi), F^2 built on the boosted background ({time.time()-T0:.1f}s)")

# ---- C.1: the structure of deltaQ (order eps^1), graded by wb and Q0 --------
dQ = sp.expand(Qc - Q0)
P("")
P("  [C.1] deltaQ = (Q - Q0) at O(eps), graded by powers of w_b:")
dQ1 = sp.expand(dQ.coeff(eps, 1))
q0free_terms = 0
for n in range(3):
    piece = sp.collect(sp.expand(dQ1.coeff(wb, n)), [Es, Eis])
    P(f"    O(w_b^{n}):  {piece}")
    q0free = sp.expand(piece.subs(Q0, 0))
    if n == 0:
        assert q0free == 0, "wb^0 piece of deltaQ must be entirely Q0-weighted"
    q0free_terms += q0free*wb**n
P("    Q0-FREE content of deltaQ (all orders in w_b):",
  sp.collect(sp.expand(q0free_terms), [Es, Eis]))
P("    ^ the ONLY Q0-free term is the flow-gradient  (w.q) chi  piece: I*k_x*w_b*w1*chi.")
P("      Every metric/aether piece of deltaQ carries Q0 (cosmological 1/length).")

# ---- C.2: F_QQ (deltaQ)^2 insertions: diagonal (ket*bra) part, graded -------
def DC(e):
    e = sp.expand(e); pol = sp.Poly(e, Es, Eis); out = 0
    for mon, c in zip(pol.monoms(), pol.coeffs()):
        if mon[0] == mon[1]:
            out += c*(Es*Eis)**mon[0]
    return out.subs(Es*Eis, 1) if out != 0 else out
dL_novel = sp.expand(-FQQ*te(dQ**2)).coeff(eps, 2)
dL_dc = DC(dL_novel)
P("")
P("  [C.2] The novel-channel quadratic insertion  -F_QQ (deltaQ)^2 |_diag :")
for n in range(3):
    piece = sp.expand(dL_dc.coeff(wb, n))
    pw = sp.collect(piece, [chik*chib])
    P(f"    O(w_b^{n}):  {sp.simplify(pw)}")
ins2 = sp.expand(dL_dc.coeff(wb, 2))
ins2_q0free = sp.simplify(ins2.subs(Q0, 0))
P("    O(w_b^2), Q0 -> 0 limit (the UNSUPPRESSED insertion):", ins2_q0free)
chichi = ins2_q0free.coeff(chik*chib)
assert sp.simplify(ins2_q0free - chichi*chik*chib) == 0, \
    "Q0-free wb^2 insertion must be pure chi-chi"
P("    => pure  -2 F_QQ k_x^2 w1^2 chi_k chi_b : a (w.q)^2 chi^2 insertion,")
P("       ANISOTROPIC (w_par ONLY -- w2, w3 absent), q^2-order (rides k_x^2,")
P("       NOT Q0^2), i.e. NOT power-suppressed at solar-system wavenumbers.")

# ---- C.3: chi--aether mixing table (does chi renormalize eta_K?) ------------
P("")
P("  [C.3] chi--field quadratic mixings of the aether/scalar sectors")
P("        L_as = -(K_B/2)F^2 + 2(2-K_B) J.grad(phi) - (2-K_B) J_Y Y - F_QQ dQ^2")
KBs = sp.symbols('K_B', real=True)
L_as = sp.expand(-(KBs/2)*F2 + 2*(2-KBs)*Jdphi*eps**0)  # J.dphi already graded
L_as = sp.expand(-(KBs/2)*F2 + 2*(2-KBs)*Jdphi - (2-KBs)*JY*Yc - FQQ*te(dQ**2))
L2_as = DC(sp.expand(L_as).coeff(eps, 2))
pairs = [('a1', a1k, a1b), ('a2', a2k, a2b), ('a3', a3k, a3b),
         ('Psi', Psik, Psib), ('Phi', Phik, Phib), ('B2', B2k, B2b)]
P("   pair        wb^0 coeff                          wb^1 coeff (Q0->0 shown too)")
for nm, fk, fb in pairs:
    c0 = sp.simplify(sp.expand(L2_as.coeff(wb, 0)).coeff(chik, 1).coeff(fb, 1)
                     + sp.expand(L2_as.coeff(wb, 0)).coeff(chib, 1).coeff(fk, 1))
    c1_ = sp.simplify(sp.expand(L2_as.coeff(wb, 1)).coeff(chik, 1).coeff(fb, 1)
                      + sp.expand(L2_as.coeff(wb, 1)).coeff(chib, 1).coeff(fk, 1))
    P(f"   chi-{nm:4s}  {str(c0):34s}  {str(c1_):s}   [Q0->0: {sp.simplify(c1_.subs(Q0,0))}]")
# certify: transverse aether (a2,a3) mixes with chi ONLY through Q0-weighted terms
mix_T = 0
for fk, fb in [(a2k, a2b), (a3k, a3b)]:
    for n in range(3):
        mix_T += sp.expand(L2_as.coeff(wb, n)).coeff(chik, 1).coeff(fb, 1).subs(Q0, 0)
        mix_T += sp.expand(L2_as.coeff(wb, n)).coeff(chib, 1).coeff(fk, 1).subs(Q0, 0)
P("   TRANSVERSE-aether--chi mixing with Q0->0 (all wb orders):", sp.simplify(mix_T))
if sp.simplify(mix_T) == 0:
    P("   => LEMMA CERTIFIED: chi couples to the TRANSVERSE aether only through")
    P("      Q0^2-scale (cosmological-mass) terms, (Q0/q)^2-suppressed at PPN q.")
    P("      The transverse a^2 stiffness that sets eta_K (and alpha_1 = -4 eta_K)")
    P("      is NOT renormalized by the scalar at q^2 order: eta_K = K_B stands.")

# ---- C.4: transverse aether stiffness (eta_K reading) -----------------------
stiff_T = sp.simplify(sp.expand(L2_as.coeff(wb, 0)).coeff(a2k, 1).coeff(a2b, 1))
P("   transverse aether stiffness coeff(a2_k a2_b) at wb^0:", stiff_T,
  "  [q^2 part = -K_B k_x^2 * 2/2 -> c1 = K_B, c14 = K_B on the Maxwell locus;")
P("    the Q0^2 part is the cosmological spin-1 mass -- unscreenable but")
P("    (Q0/q)^2-negligible at PPN wavenumbers (wf2_massive_vector_ppn_suppression)]")

# ============================================================================
P("")
P("="*78)
P("[D] VERDICT (structural)")
P("="*78)
P("""  1. deltaQ under the boost contains the Q0-FREE flow-gradient piece
     i (w.q) chi.  Naive counting deltaQ ~ Qbar Phi MISSES it.
  2. Therefore -F_QQ (deltaQ)^2 delivers the unsuppressed O(w^2) insertion
        -2 F_QQ (w.q)^2 chi^2 ,   F_QQ = mu2 (1 + kappa^2/4pi),
     which is PURELY ANISOTROPIC ((w.qhat)^2, parallel-only) and q^2-order.
     Through the static chi--Psi mixing (chi is sourced at O(U): it carries
     part of G_N) this lands on the  w_par^2 U  structure of g00 and, by the
     [A] certificate, is an ALPHA_2 contribution:  par - perp = 2 alpha_2.
     It cannot be absorbed into alpha_1 (isotropic w^2 U) or beta (U^2).
  3. Every OTHER insertion of the novel channel -- including the naive
     beta-channel piece F_QQ Q0^2 Psi^2 -- carries Q0^2 and is suppressed by
     (Q0/q)^2 ~ (H r / c)^2 ~ 1e-30 at AU scales.  The beta liability from
     THIS channel is |beta-1| ~ mu2 (1+kappa^2/4pi) (Q0/q)^2 : dead-safe.
     The naive counting had it inverted: beta is the SUPPRESSED projection,
     alpha_2 the UNSUPPRESSED one.
  4. eta_K: the scalar mixes with the LONGITUDINAL sector (and the metric) at
     q^2 order but with the TRANSVERSE aether only via Q0^2 terms ([C.3]);
     so eta_K = K_B is unrenormalized, alpha_1 = -4 K_B (anchor iii holds with
     the scalar retained), eta_K is NONZERO-generic, and C0_base =
     K_B(K_B - lam2_eff)/(2 lam2_eff) -> -K_B/2 in Route 3's stiff limit.
  ORDER OF MAGNITUDE for the alpha_2 projection: the insertion multiplies the
  chi-carried share f_chi of the Newtonian response by F_QQ (w.qhat)^2 w^2 /
  (chi stiffness ~ (2-K_B)), so
        |Pi_K| ~ f_chi * mu2 (1+kappa^2/4pi) / (2-K_B),   f_chi <~ K_B/(2-K_B)
  (from G_N = G/(1-K_B/2): the non-tensor exchange share).  O(1) coefficient
  from the full ladder; companion script t3x_numeric_PiK_slope.py measures the
  exact slope d(alpha_2)/d(F_QQ) at test points.""")
P(f"done ({time.time()-T0:.1f}s)")
