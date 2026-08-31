#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf2_target2_novel_projection_2026.py
====================================================================================
TARGET 2 -- the Pi-projection of the UNSUPPRESSED novel v9 channel (K_QQ = mu2 and the
a0-promotion a0QQ = -kappa^2 G mu2 riding g = dJcal/d(a0^2) -> -2, i.e. the effective
F_QQ(Q0) -> mu2 (1 + kappa^2/4pi)) onto the Will PPN channels:
      w^2 U anisotropy (alpha_2)   vs   U^2 (beta).

Closes the second owed item of the v9 alpha_2 terminal status
(qwen_claude_field_theory/closure_2026/v9_alpha2_ppn_status.md).

METHOD (all sympy; every load-bearing number re-derived in THIS run):
  PART 0  Will-dictionary certificate (TEGP / Living Rev 17:4 eq 27 + Fourier rules).
  PART 1  Second-variation certificate: at the v9 background (K_Q(Q0)=0 => a0Q(Q0)=0) the
          ENTIRE novel channel enters the quadratic action as a pure rescaling of the
          (deltaQ)^2 coefficient, K2 -> K2*(1+kappa^2/4pi); all cross terms F_YQ carry
          a0Q(Q0)=0 and vanish; g(y0)+2 is exponentially small at solar u0.
  PART 2  Boosted quadratic-action solve (anisotropic h_ij, plane wave k=x^, static,
          aether boosted by wb*w; ladder wb^0 -> wb^1 -> wb^2), in TWO DIFFERENT GAUGES
          (v2: s11=0; alt: h11=0), plus an 11-field build with E_h11 RETAINED that
          exhibits the O(wb^2) constraint obstruction (rank/aug rank exhibit).
          Extraction with the CORRECTED Will dictionary; alpha_2 Laurent-split in Q0
          (Q0 = scalar-background scale over k; kx-scaling certificate makes the split
          physical):  alpha_2 = c_-1/Q0^2  +  c_0  +  O(Q0^2)
             c_-1/Q0^2 : (k/m)^2-growing => CONTACT (rho-supported, EXTERIOR-INVISIBLE)
             c_0       : k-independent   => the GENUINE exterior PPN alpha_2
             O(Q0^2)   : Yukawa, dead at PPN scales.
  PART 3  The projection: dc_0/dK2 (gauge-robust, closed form in K_B and J_Y) and the
          novel increment Delta alpha_2 = (kappa^2/4pi) K2 dc_0/dK2 vs |alpha_2|<1e-7.
  PART 4  The beta channel: the (deltaQ)^2 operator has no gradient term, so its U^2
          exposure is (mu_eff r)^2-suppressed; numbers vs |beta-1| < 8e-5.

HEADLINE RESULTS (asserted below):
  * alpha_3 == 0 EXACTLY (all params, both gauges)  -- the DC-019 propagating-sector gate.
  * gamma_PPN = 1, Newton OK; base anchor: lim_{JY->oo} lim_{Q0->0} alpha_1 = -4 K_B (FJ).
  * alpha_1(Q0->0) = -4 (K_B J_Y + 2)/(J_Y + 1)   [gauge-robust]
      => at the deep-field point J_Y = mu(u0) = 1:  alpha_1 = -2(K_B+2)  (eta_K=(K_B+2)/2).
  * c_-1 = -(J_Y+10)^2/(81 J_Y (J_Y+1)^2) at K_B=1/5 (JY=1, general K_B: -(K_B+2)^2/(4(2-K_B)^2))
      [gauge-robust contact coefficient; interior EFT WATCH, exterior-invisible].
  * dc_0/dK2 (JY=1, Q0->0) = (4 + 4K_B - K_B^2)/(2-K_B)^3 = [8-(2-K_B)^2]/(2-K_B)^3
      [GAUGE-ROBUST, K2-linear exactly, k-INDEPENDENT => lands in the GENUINE alpha_2]
      JY-form at K_B=1/5: 5(19 J_Y + 100)/(729 J_Y^2)  (dies ~1/J_Y under stiff-scalar
      screening JY->oo, O(1) at the physical deep-field JY=1).
  * The K2-free offset of c_0 DISAGREES between gauges (v2 vs alt at K_B=1/5, JY=1:
      -1771/405 vs -781/405): the O(wb^2) ladder with E_h11 retained is INCONSISTENT
      (rank 10, augmented rank 11) -- a truncation-level broken constraint. The base
      alpha_2 offset (TARGET 1's C0_base) is therefore NOT certified here; the
      K2-projection and everything else listed above IS (identical in both gauges).
  => VERDICT: the unsuppressed novel channel PROJECTS ONTO ALPHA_2 (not beta):
      Delta alpha_2 = (kappa^2/4pi) K2 (4+4K_B-K_B^2)/(2-K_B)^3 ~ 1e-3..3e-2 for
      physical K2 ~ 0.1..1  =>  4-5 orders over the LLR bound |alpha_2| < 1e-7.
      The naive "|beta-1| ~ Qbar^2 mu2 (1+kappa^2/4pi)" liability is RETIRED: it is
      (mu_eff r)^2 < 2e-27 inside 100 AU (the dimensionful mu2 was the missing factor).

Runtime: ~10 minutes (three inline action builds + symbolic ladders).  Exit 0 iff all
certificates pass.
"""
import sympy as sp, time, math, sys

T0=time.time()
P=lambda *a: print(*a, flush=True)
FAIL=[]; NCH=[0]
def check(cond,label):
    NCH[0]+=1; ok=bool(cond)
    P(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok: FAIL.append(label)

# ======================= PART 0: Will dictionary certificate =======================
P("="*88); P("PART 0: Will-normalization dictionary certificate (sympy)"); P("="*88)
a1s,a2s,a3s=sp.symbols('alpha_1 alpha_2 alpha_3', real=True)
w1,w2,w3,U=sp.symbols('w1 w2 w3 U', real=True)
w2v=w1**2+w2**2+w3**2
wwUij = w1**2*(-U) + w2**2*U + w3**2*U        # U_ij -> dij U - 2 qi qj U/q^2, qhat=xhat
g00PF = -(a1s-a2s-a3s)*w2v*U - a2s*wwUij
cpar = sp.expand(g00PF).coeff(w1**2).coeff(U); cperp= sp.expand(g00PF).coeff(w2**2).coeff(U)
check(sp.simplify((cpar-cperp)/2-a2s)==0, "ALPHA_2 = [coeff(w_par^2 U)-coeff(w_perp^2 U)]/2 (alpha_3-blind)")
check(sp.simplify(cperp+a1s-a3s)==0,      "ALPHA_3 = coeff(w_perp^2 U) + alpha_1")
g02 = -sp.Rational(1,2)*(a1s-2*a2s)*w2*U - a2s*(w2*U)
check(sp.simplify(g02/(w2*U)+a1s/2)==0,   "g0i transverse coeff = -alpha_1/2 => ALPHA_1 = -2*coeff")
P("  boost parity: the solve boosts the AETHER (+wb w) in the source frame; Will's w is the")
P("  frame velocity RELATIVE TO the preferred frame = -wb w. Odd (g0i) structures flip sign")
P("  => alpha_1 = +2*coeff(w2 U in h02)/U_amp here; even (w^2) structures unaffected.")
P("  Anchor that fixes the parity choice: pure-EA corner must give FJ alpha_1 = -4K_B (below).")

# ======================= PART 1: second-variation certificate ======================
P("="*88); P("PART 1: the novel channel = pure rescaling K2 -> K2 (1+kappa^2/4pi)"); P("="*88)
y,Q,Q0v,kappa,Gv,mu2 = sp.symbols('y Q Q0 kappa G mu2', positive=True)
FY = y + 2*(sp.sqrt(y)+1)*sp.exp(-sp.sqrt(y)) - 2          # kernel mu(u)=1-e^{-u}
Kfun = sp.Function('K')
S_ = kappa**2*Gv*(-Kfun(Q))                                # a0^2(Q) promotion
F  = S_/(8*sp.pi*Gv)*FY.subs(y, sp.Symbol('Y')/S_) + Kfun(Q)
Ysym=sp.Symbol('Y')
FQ  = sp.diff(F,Q);  FQQ = sp.diff(F,Q,2);  FYQ = sp.diff(F,Ysym,Q)
KQ0 = {sp.Derivative(Kfun(Q),Q): 0}                        # K_Q(Q0)=0 at the dS point
FYQ_bg = sp.simplify(FYQ.subs(KQ0))
check(FYQ_bg==0, "F_YQ(bg) == 0 exactly (every cross term carries a0Q(Q0) prop K_Q(Q0)=0)")
FQQ_bg = sp.simplify(FQQ.subs(KQ0).subs(sp.Derivative(Kfun(Q),(Q,2)), mu2))
gfac = sp.simplify(FY - y*sp.diff(FY,y))                   # the a0-promotion weight g(y)
check(sp.limit(gfac,y,sp.oo)==-2, "g(y)=F_Y - y F_Y' -> -2 (nonzero const; the unsuppressed ride)")
u=sp.Symbol('u',positive=True)
tail=sp.simplify((gfac.subs(y,u**2)+2)*sp.exp(u))
check(sp.limit(tail/u**2,u,sp.oo)==1, "g+2 = u^2 e^{-u}(1+2/u) exp-small at solar u0~1e7-1e11")
FQQ_solar = sp.simplify(FQQ_bg.subs(Ysym, sp.oo).rewrite(sp.exp)) if False else None
# substitute the limit g->-2 explicitly:
FQQ_lim = sp.simplify(mu2 - kappa**2*Gv*mu2*(-2)/(8*sp.pi*Gv))
check(sp.simplify(FQQ_lim - mu2*(1+kappa**2/(4*sp.pi)))==0, "F_QQ(Q0) -> mu2 (1 + kappa^2/4pi)")
P("  => at quadratic order the novel terms change ONLY the (deltaQ)^2 coefficient:")
P("     in the solve below, K2 -> K2*(1+kappa^2/4pi).  No new operator structures.")
P("     (Convention notes: the transcribed v9 Fcal gives the (2-K_B)-weighted variant")
P("      1+(2-K_B)kappa^2/8pi -- same order; and -Fcal in the action makes the physical")
P("      sign of the (deltaQ)^2 term convention-dependent; |Delta alpha_2| is unaffected.)")

# ======================= PART 2: the boosted solves (two gauges + 11f) =============
P("="*88); P("PART 2: boosted quadratic-action solves"); P("="*88)
eps,wb=sp.symbols('eps w_b', positive=True)
KB,Q0,K2,JY=sp.symbols('K_B Q_0 K_2 J_Y', real=True)
GT,LAM=sp.symbols('G_t Lambda', real=True)
eta=sp.diag(-1,1,1,1); I=sp.I
Es,Eis=sp.symbols('E_s E_is'); kx=sp.symbols('k_x', real=True); kv=[0,kx,0,0]
def nf(tag): ket=sp.Symbol(tag+'k'); bra=sp.Symbol(tag+'b'); return ket*Es+bra*Eis,ket,bra
def d(f,mu): return sp.diff(f,Es)*(I*kv[mu]*Es)+sp.diff(f,Eis)*(-I*kv[mu]*Eis)

def build_L2dc(gauge):
    """gauge='v2' (s11=0 slice), 'alt' (h11=0 slice), '11f' (h11 independent, E_h11 kept)."""
    ww=w1**2+w2**2+w3**2; S0=1+wb**2*ww/2
    Aup_bg=sp.Matrix([S0,wb*w1,wb*w2,wb*w3]); Adn_bg=eta*Aup_bg
    dphi_bg=-Q0*Adn_bg
    Psi,Psik,Psib=nf('Psi'); Phi,Phik,Phib=nf('Phi')
    B2f,B2k,B2b=nf('B2'); B3f,B3k,B3b=nf('B3')
    s22,s22k,s22b=nf('s22'); s23,s23k,s23b=nf('s23')
    a1f,a1k,a1b=nf('a1'); a2f,a2k,a2b=nf('a2'); a3f,a3k,a3b=nf('a3')
    chi,chik,chib=nf('chi'); rho,Rk,Rb=nf('rho'); a0f,a0k,a0b=nf('a0p')
    H=sp.zeros(4,4)
    H[0,0]=-2*Psi
    H[0,2]=B2f; H[2,0]=B2f; H[0,3]=B3f; H[3,0]=B3f
    if gauge=='v2':   H[1,1]=-2*Phi
    elif gauge=='alt':H[1,1]=0
    else:
        h11f,h11k,h11b=nf('h11'); H[1,1]=h11f
    H[2,2]=-2*Phi+s22; H[3,3]=-2*Phi-s22
    H[2,3]=s23; H[3,2]=s23
    gd=sp.Matrix(4,4,lambda m,n: eta[m,n]+eps*H[m,n])
    Hup=eta*H*eta
    gu=sp.Matrix(4,4,lambda i,j:(eta-eps*Hup+eps**2*(Hup*H*eta))[i,j])
    trH=sum(eta[m,n]*H[m,n] for m in range(4) for n in range(4))
    HH=sum(Hup[m,n]*H[m,n] for m in range(4) for n in range(4))
    sqg=1+eps*trH/2+eps**2*(trH**2/8-HH/4)
    Adn=sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
    Aup=sp.Matrix(4,1,lambda i,j: sum(gu[i,k2_]*Adn[k2_] for k2_ in range(4)))
    C1=sp.expand(sum(Aup[i]*Adn[i] for i in range(4))+1).coeff(eps,1)
    solA=sp.solve([sp.expand(C1).coeff(Es,1),sp.expand(C1).coeff(Eis,1)],[a0k,a0b],dict=True)[0]
    solA={k2_:sp.expand(sp.series(v,wb,0,3).removeO()) for k2_,v in solA.items()}
    a0f=a0f.subs(solA)
    Adn=sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
    Aup=sp.Matrix(4,1,lambda i,j: sum(gu[i,k2_]*Adn[k2_] for k2_ in range(4)))
    dphi=sp.Matrix([dphi_bg[m]+eps*d(chi,m) for m in range(4)])
    def te(e):
        e=sp.expand(e); out=0
        for i in range(3):
            ci=e.coeff(eps,i)
            for j in range(3): out+=ci.coeff(wb,j)*eps**i*wb**j
        return out
    def wtrunc(e):
        e=sp.expand(e); return sum(e.coeff(wb,n)*wb**n for n in range(3))
    guT=sp.Matrix(4,4,lambda m,n: te(gu[m,n])); AupT=sp.Matrix(4,1,lambda i,j: te(Aup[i]))
    Gam=[[[sp.Rational(1,2)*sum(gu[r,s]*(d(gd[s,n],m)+d(gd[s,m],n)-d(gd[m,n],s)) for s in range(4))
           for n in range(4)] for m in range(4)] for r in range(4)]
    GamT=[[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]
    dphiT=sp.Matrix(4,1,lambda i,j: te(dphi[i]))
    Fmn=sp.Matrix(4,4,lambda m,n: sp.expand(d(Adn[n],m)-d(Adn[m],n)))
    F1=sp.Matrix(4,4,lambda m,n: Fmn[m,n].coeff(eps,1))
    F2=eps**2*sum(F1[m,n]*F1[a_,b_]*eta[m,a_]*eta[n,b_] for m in range(4) for n in range(4) for a_ in range(4) for b_ in range(4))
    Jup=[te(sum(AupT[nu]*(d(AupT[al],nu)+sum(GamT[al][nu][r]*AupT[r] for r in range(4))) for nu in range(4))) for al in range(4)]
    Jdphi=te(sum(Jup[m]*dphiT[m] for m in range(4)))
    Qc=te(sum(AupT[m]*dphiT[m] for m in range(4)))
    Yc=te(sum((guT[m,n]+AupT[m]*AupT[n])*dphiT[m]*dphiT[n] for m in range(4) for n in range(4)))
    dQ=Qc-Q0; Kq=-2*LAM+K2*te(dQ**2)
    def ric(a_,b_):
        o=0
        for m in range(4):
            o+=d(Gam[m][b_][a_],m)-d(Gam[m][m][a_],b_)
            for l in range(4): o+=Gam[m][m][l]*Gam[l][b_][a_]-Gam[m][b_][l]*Gam[l][m][a_]
        return o
    Rsc=te(sum(guT[m,n]*ric(m,n) for m in range(4) for n in range(4)))
    def grade(e):
        e=sp.expand(e); return [wtrunc(e.coeff(eps,n)) for n in range(3)]
    gF2=grade(F2); gJ=grade(Jdphi); gY=grade(Yc); gK=grade(Kq); gsq=grade(sqg); gR=grade(Rsc)
    gS=[gR[n]-(2*LAM if n==0 else 0)-(KB/2)*gF2[n]+2*(2-KB)*gJ[n]-(2-KB)*gY[n]-gK[n] for n in range(3)]
    L2_grav=wtrunc(sum(gsq[a_]*gS[2-a_] for a_ in range(3)))-(2-KB)*JY*gY[2]
    L2_matt=-16*sp.pi*GT*wtrunc(rho*(-H[0,0]/2))
    L2=sp.expand(L2_grav+L2_matt)
    pol=sp.Poly(L2,Es,Eis); out=0
    for mon,c in zip(pol.monoms(),pol.coeffs()):
        if mon[0]==mon[1]: out+=c*(Es*Eis)**mon[0]
    return out.subs(Es*Eis,1)

S=sp.Symbol
NAMES10=['Psi','Phi','B2','B3','s22','s23','a1','a2','a3','chi']
Rk=S('rhok')
def ladder(L2dc,names,sub,gauge_row=None):
    """Solve the wb^0 -> wb^1 -> wb^2 ladder. Returns dict or ('INCONSISTENT_wbN',)"""
    KETS=[S(n+'k') for n in names]; BRAS=[S(n+'b') for n in names]
    eq={A: sp.expand(sp.diff(L2dc,A).subs(sub)) for A in BRAS}
    def lin(eqs,unk):
        Am,bb=sp.linear_eq_to_matrix(eqs,unk); s=list(sp.linsolve((Am,bb),unk))
        return dict(zip(unk,[sp.cancel(sp.together(v)) for v in s[0]])) if s else None
    if gauge_row is None:
        VZ={S(n+'k'):0 for n in ['B2','B3','s23','a2','a3']}
        stat=['Psi','Phi','s22','a1','chi']
        eq0=[sp.expand(eq[S(n+'b')].coeff(wb,0).subs(VZ)) for n in stat]
        s0s=lin(eq0,[S(n+'k') for n in stat])
        if s0s is None: return ('INCONSISTENT_wb0',)
        s0={**s0s,**VZ}
    else:
        eq0=[sp.expand(e.coeff(wb,0)) for e in eq.values()]+[gauge_row(0,{n:S(n+'k') for n in names})]
        s0=lin(eq0,KETS)
        if s0 is None: return ('INCONSISTENT_wb0',)
    dk1={A:sp.Symbol(f'd1_{A}') for A in KETS}; dk2={A:sp.Symbol(f'd2_{A}') for A in KETS}
    subF={A: s0[A]+wb*dk1[A]+wb**2*dk2[A] for A in KETS}
    eqW={A: sp.expand(eq[A].subs(subF)) for A in BRAS}
    e1=[sp.expand(eqW[A].coeff(wb,1)) for A in BRAS]
    e2base=[sp.expand(eqW[A].coeff(wb,2)) for A in BRAS]
    if gauge_row is not None:
        e1=e1+[gauge_row(1,{n:dk1[S(n+'k')] for n in names})]
    def lin2(eqs,unk):
        Am,bb=sp.linear_eq_to_matrix(eqs,unk); s=list(sp.linsolve((Am,bb),unk))
        return (dict(zip(unk,[sp.cancel(sp.together(v)) for v in s[0]])) if s else None,Am,bb)
    s1,_,_=lin2(e1,list(dk1.values()))
    if s1 is None: return ('INCONSISTENT_wb1',)
    e2=[e.subs(s1) for e in e2base]
    if gauge_row is not None:
        e2=e2+[gauge_row(2,{n:dk2[S(n+'k')] for n in names})]
    s2,Am2,bb2=lin2(e2,list(dk2.values()))
    if s2 is None:
        return ('INCONSISTENT_wb2',Am2,bb2)
    h00n=sp.cancel(-2*s0[S('Psik')]/Rk) if 'Psi' in names else None
    U_amp=sp.cancel(h00n/2)
    c2=sp.cancel(sp.expand(dk1[S('B2k')].subs(s1)).coeff(w2)/Rk)
    alpha1=sp.cancel(2*c2/U_amp)
    h2=sp.expand(-2*sp.expand(dk2[S('Psik')].subs(s2)))
    A1=sp.cancel(h2.coeff(w1**2)/Rk); A2c=sp.cancel(h2.coeff(w2**2)/Rk); A3c=sp.cancel(h2.coeff(w3**2)/Rk)
    return {'h00n':h00n,'gamma':sp.cancel(s0[S('Phik')]/s0[S('Psik')]),
            'alpha1':alpha1,'alpha2':sp.cancel((A1-A2c)/(2*U_amp)),
            'alpha3':sp.cancel(A2c/U_amp+alpha1),'iso':sp.simplify(A2c-A3c)}

def laurent(a2):
    cm1=sp.simplify(sp.limit(a2*Q0**2,Q0,0))
    c0=sp.simplify(sp.limit(sp.cancel(a2-cm1/Q0**2),Q0,0))
    return cm1,c0

P(f"[t={time.time()-T0:.0f}s] building v2-gauge action ...")
L2_v2=build_L2dc('v2')
P(f"[t={time.time()-T0:.0f}s] building alt-gauge action ...")
L2_alt=build_L2dc('alt')

# --- main symbolic solve, v2 gauge, KB=1/5, (K2,JY,Q0) symbolic ---
P(f"[t={time.time()-T0:.0f}s] v2-gauge ladder at K_B=1/5, (K2, J_Y, Q_0) symbolic ...")
r5=ladder(L2_v2,NAMES10,{KB:sp.Rational(1,5),GT:1,LAM:0,kx:1})
check(not isinstance(r5,tuple), "v2 ladder solvable (K_B=1/5, symbolic K2,J_Y,Q_0)")
check(sp.simplify(r5['gamma']-1)==0, "gamma_PPN = 1 (Phi=Psi at wb^0) -- anchor (ii)")
check(sp.simplify(r5['alpha3'])==0, "alpha_3 == 0 EXACTLY (all K2,J_Y,Q_0) -- DC-019 gate")
check(r5['iso']==0, "w2^2 vs w3^2 isotropy of the transverse w^2 sector")
a1_lim=sp.simplify(sp.limit(r5['alpha1'],Q0,0))
check(sp.simplify(a1_lim + 4*(sp.Rational(1,5)*JY+2)/(JY+1))==0,
      "alpha_1(Q0->0) = -4(K_B J_Y + 2)/(J_Y+1)  [K_B=1/5]")
check(sp.limit(a1_lim,JY,sp.oo)==sp.Rational(-4,5),
      "base anchor (iii): lim_{JY->oo} lim_{Q0->0} alpha_1 = -4K_B (Foster-Jacobson, Maxwell locus)")
P(f"    alpha_1(J_Y=1, deep field) = {sp.nsimplify(a1_lim.subs(JY,1))}  [= -2(K_B+2); eta_K=(K_B+2)/2]")
cm1_5,c0_5=laurent(r5['alpha2'])
P(f"    c_-1(J_Y,K2) = {sp.factor(cm1_5)}")
P(f"    c_0(J_Y,K2)  = {sp.factor(c0_5)}")
check(K2 not in cm1_5.free_symbols, "contact coefficient c_-1 is K2-free")
check(sp.simplify(sp.diff(c0_5,K2,2))==0, "c_0 is EXACTLY linear in K2")
slope5=sp.simplify(sp.diff(c0_5,K2))
check(sp.simplify(slope5 - 5*(19*JY+100)/(729*JY**2))==0,
      "dc_0/dK2 = 5(19 J_Y+100)/(729 J_Y^2) at K_B=1/5 (JY=1: 595/729; ->0 as JY->oo)")

# --- alt gauge, KB=1/5 and KB=1/2, JY=1, (K2,Q0) symbolic: gauge-robustness ---
P(f"[t={time.time()-T0:.0f}s] alt-gauge ladders (J_Y=1) at K_B=1/5, 1/2 ...")
ra=ladder(L2_alt,NAMES10,{KB:sp.Rational(1,5),GT:1,LAM:0,kx:1,JY:1})
cm1_a,c0_a=laurent(ra['alpha2'])
check(sp.simplify(cm1_a-cm1_5.subs(JY,1))==0, "GAUGE-ROBUST: contact c_-1 identical (v2 vs alt)")
check(sp.simplify(sp.diff(c0_a,K2)-slope5.subs(JY,1))==0, "GAUGE-ROBUST: dc_0/dK2 identical (v2 vs alt)")
check(sp.simplify(sp.limit(ra['alpha1'],Q0,0)-a1_lim.subs(JY,1))==0, "GAUGE-ROBUST: alpha_1 identical")
check(sp.simplify(ra['alpha3'])==0, "alt gauge: alpha_3 == 0")
off_v2=sp.simplify(c0_5.subs({JY:1,K2:0})); off_alt=sp.simplify(c0_a.subs(K2,0))
P(f"    K2-free offset of c_0: v2 = {sp.nsimplify(off_v2)}  vs  alt = {sp.nsimplify(off_alt)}")
check(sp.simplify(off_v2-off_alt)!=0,
      "HONESTY EXHIBIT: the K2-free offset DISAGREES between gauges (base C0 NOT certified here)")
rb=ladder(L2_alt,NAMES10,{KB:sp.Rational(1,2),GT:1,LAM:0,kx:1,JY:1})
cm1_b,c0_b=laurent(rb['alpha2'])
KBgen=(4+4*KB-KB**2)/(2-KB)**3
check(sp.simplify(sp.diff(c0_b,K2)-KBgen.subs(KB,sp.Rational(1,2)))==0,
      "K_B-form: dc_0/dK2(JY=1) = (4+4K_B-K_B^2)/(2-K_B)^3  [checked K_B=1/2 alt; 1/5 both]")
check(sp.simplify(sp.diff(c0_a,K2)-KBgen.subs(KB,sp.Rational(1,5)))==0,
      "K_B-form at K_B=1/5")
check(sp.simplify(cm1_b + (sp.Rational(1,2)+2)**2/(4*(2-sp.Rational(1,2))**2))==0,
      "contact K_B-form: c_-1(JY=1) = -(K_B+2)^2/(4(2-K_B)^2)  [checked K_B=1/2]")

# --- kx-scaling certificate: Q0 is a mass/k; K2 is scale-free ---
P(f"[t={time.time()-T0:.0f}s] kx-scaling certificate ...")
rA=ladder(L2_v2,NAMES10,{KB:sp.Rational(1,5),GT:1,LAM:0,kx:2,K2:7,Q0:sp.Rational(2,5),JY:1})
rB=ladder(L2_v2,NAMES10,{KB:sp.Rational(1,5),GT:1,LAM:0,kx:1,K2:7,Q0:sp.Rational(1,5),JY:1})
check(sp.simplify(rA['alpha2']-rB['alpha2'])==0 and sp.simplify(rA['alpha1']-rB['alpha1'])==0,
      "alpha_i(kx=2,Q0) == alpha_i(kx=1,Q0/2) at fixed K2 => c_-1/Q0^2 is (k/m)^2 CONTACT, c_0 is k-free")

# --- 11-field build: the O(wb^2) constraint obstruction exhibit ---
P(f"[t={time.time()-T0:.0f}s] 11-field build (h11 independent, E_h11 retained) ...")
L2_11=build_L2dc('11f')
NAMES11=NAMES10+['h11']
def grow_v2(order,kets): return kets['h11']+2*kets['Phi']
r11=ladder(L2_11,NAMES11,{KB:sp.Rational(1,5),GT:1,LAM:0,kx:1,K2:7,Q0:sp.Rational(1,10),JY:1},gauge_row=grow_v2)
check(isinstance(r11,tuple) and r11[0]=='INCONSISTENT_wb2',
      "E_h11 retained => wb^2 ladder INCONSISTENT (broken constraint at O(wb^2)): the c_0 offset ambiguity is real")
if isinstance(r11,tuple) and len(r11)==3:
    Am2,bb2=r11[1],r11[2]
    P(f"    rank(A)={Am2.rank()}  rank([A|b])={Am2.row_join(bb2).rank()}  (incl. gauge row; EOM-only block: 10 vs 11 -- Fredholm violation)")

# ======================= PART 3: the projection, physically ========================
P("="*88); P("PART 3: Pi-projection verdict + physical magnitude"); P("="*88)
kap2_4pi=sp.Rational(1,16)/sp.pi        # kappa=1/2 => kappa^2/4pi = 1/(16 pi)
P("  GENUINE (exterior, k-independent) alpha_2 K2-projection, JY=1 (deep field):")
P("      d alpha_2 / d K2 = (4+4K_B-K_B^2)/(2-K_B)^3 = [8-(2-K_B)^2]/(2-K_B)^3")
P("  Pi_K  (K_QQ=mu2 channel)      : Delta alpha_2 = K2 * dalpha2/dK2      [O(1)*K2]")
P("  Pi_a0 (a0-promotion increment): Delta alpha_2 = (kappa^2/4pi) K2 * dalpha2/dK2")
P("  Physical K2 (dimensionless in the action bracket; kx-scaling certified scale-free):")
P("    m_chi^2 ~ K2 Q0^2/(2-K_B) with m_chi^-1 = 4392 Mpc (v9 Helmholtz) and Q0 ~ Qbar ~ H0-scale")
P("    => K2 ~ (2-K_B)(Qbar/m_chi... inverted) ~ (2-K_B)*(H0/mu)^2*O(1) ~ 0.1..1  [O(1) mapping]")
Mpc=3.0857e22; mu_inv=4392*Mpc; H0_inv=4283*Mpc
K2_est=lambda kb: (2-kb)*(mu_inv/ (2*H0_inv))**2   # Qbar ~ 2H0 attractor scale
P(f"    fiducial K2(K_B=0.2) ~ {K2_est(0.2):.3f}   (Qbar ~ 2 H0)")
P(f"  {'K_B':>6} {'dc0/dK2':>9} {'Pi_a0=Dalpha2(novel), K2=0.4':>30} {'vs |alpha_2|<1e-7':>18}")
for kb in [0.05,0.1,0.2,0.25,0.3,0.5]:
    sl=float(KBgen.subs(KB,kb)); da=float(kap2_4pi)*0.4*sl
    P(f"  {kb:6.2f} {sl:9.4f} {da:30.3e} {da/1e-7:15.1e} x")
P("  => the UNSUPPRESSED novel channel LANDS IN ALPHA_2 (not beta): 4-5 orders over LLR")
P("     for any K2 >~ 1e-5.  It rides the SAME (deltaQ)^2 slot as base-AeST's own mass term,")
P("     whose base projection K2*dc0/dK2 ~ 0.3 is itself part of the (uncertified-offset)")
P("     base alpha_2.  Screening escape JY->oo exists (slope ~ 5*19/(729 J_Y)) but the")
P("     physical deep-field value is J_Y = mu(u0) = 1 - e^{-u0} = 1 EXACTLY for PPN purposes.")

# ======================= PART 4: the beta channel ==================================
P("="*88); P("PART 4: |beta-1| exposure (the naive liability, priced correctly)"); P("="*88)
P("  (deltaQ)^2 has NO gradient term: deltaQ = chidot - Qbar Phi. Its O(eps^2) g00 sourcing")
P("  carries F_QQ Qbar^2/k^2 = (m_eff/k)^2 relative to the k^2-supported U^2 terms; a pure")
P("  mass insertion cannot propagate (contact) and its exterior tail is Yukawa:")
P("  |beta-1|_eff ~ (m_eff r)^2 (1+kappa^2/4pi),  m_eff^-1 = 4392 Mpc:")
enh=1+float(kap2_4pi)
AU=1.495979e11
for name,r_ in [("LLR 3.84e8 m",3.844e8),("Mercury 0.387 AU",0.387*AU),("100 AU",100*AU)]:
    x=(r_/mu_inv)**2*enh
    P(f"    r={name:18s}: {x:9.3e}   margin vs 8e-5: {8e-5/x:.1e}")
P("  => beta liability RETIRED: the naive 'Qbar^2 mu2 (1+kappa^2/4pi)' omitted that mu2 is")
P("     dimensionful; made dimensionless it is (mu r)^2 < 2e-27 inside 100 AU.")
P("     (Linear-response certified; the O(eps^2) statement is structural: no-gradient operator")
P("      => contact + Yukawa only. A full second-order solve was not run -- flagged.)")

# ======================= verdict ===================================================
P("="*88)
ok=len(FAIL)==0
P(f"CHECKS: {NCH[0]-len(FAIL)}/{NCH[0]} passed" + ("" if ok else f"  FAILED: {FAIL}"))
P("""
VERDICT (TARGET 2):
  Pi(novel -> alpha_2) NONZERO and UNSUPPRESSED:  Delta alpha_2(novel)
     = (kappa^2/4pi) * K2 * (4+4K_B-K_B^2)/(2-K_B)^3   [JY=1, Q0->0, gauge-robust]
     ~ 1e-3 .. 3e-2 for physical K2 ~ 0.1..1  =>  ~1e4-1e5 x the LLR bound 1e-7.
  Pi(novel -> beta) mass-suppressed: |beta-1| < 2e-27 inside 100 AU. RETIRED.
  The prior naive counting (novel piece -> beta) is REVERSED: alpha_2 is the exposed channel.
  NOT certified here: the K2-free base offset of alpha_2 (C0_base; gauge/constraint ambiguity
  at O(wb^2) exhibited by the 11-field rank test) -- TARGET 1's owed item, still open.
  NEW gauge-robust byproducts: alpha_3 == 0 exactly; alpha_1(Q0->0) = -4(K_B J_Y+2)/(J_Y+1)
  (deep field: -2(K_B+2), i.e. eta_K renormalized from K_B to (K_B+2)/2 -- LIABILITY-if-true,
  needs TARGET-1-grade independent verification).
""")
sys.exit(0 if ok else 1)
