#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gaest_setup_fj_anchors_stability_2026.py   (SETUP certificate, part 2 of 2)
============================================================================
Generalized-aether completion: c1 = -c3 = K_B (c13 = 0), c2, c4 FREE.
Pure algebra (fast). Companion to gaest_setup_quadratic_modes_2026.py, which
DERIVES the mode speeds used here.

Sections
  0. DICTIONARY. Mostly-plus FJ-dictionary aether Lagrangian (the one the
     FJ-controlled pipeline aest_j10/wf3_pure_ea_control_build.py uses):
        L_EA = -c1 D_aA^m D^aA_m - c2 (D.A)^2 - c3 D_aA^m D_mA^a + c4 a.a
     THE_GENERALIZED_COMPLETION.md writes "+ c2 (D.A)^2 + c4 a.a", so
        c2_FJ = -c2_doc ,  c4_FJ = +c4_doc.      (sign of c2 must be fixed in
     the doc or read through this map; every formula below is in FJ c's.)
  1. FJ anchors (gr-qc/0509083; Jacobson 0801.1547 eqs 4-8; OMW 1802.04303
     eq 1.1): transcription self-consistency (published alpha=0 surface zeroes
     them), then the c13=0-plane closed forms
        alpha_1 = -4 c14 ,
        alpha_2 = c14 (c14 - c2 + 2 c2 c14) / (c2 (2 - c14)) ,
        G_N = G/(1 - c14/2),
     the published alpha=0 surface meets c13=0 ONLY at (c2,c4)=(0,-K_B), i.e.
     c14 = 0 = c123 (the doubly-degenerate point), and a numeric anchor table
     the generalized pipeline must reproduce in its pure-EA (scalar-frozen)
     limit. Mutation controls: a sign-flipped alpha_1 fails the surface test.
  2. Banked base-AeST anchor at c2=c4=0 (two SOLID two-gauge solves,
     wf3_eta_K_final.out): eta_K=(K_B J_Y+2)/(J_Y+1), alpha_1=-4 eta_K;
     numeric values the generalized solve must hit at c2=c4=0.
  3. STABILITY on the c13=0 plane with c2, c4 free (speeds DERIVED in part 1;
     no-ghost from residue signs there == OMW 1802.04303 eq 3.1):
        c_T^2 = 1 ; c_V^2 = K_B/c14 ; c_S^2 = c2(2-c14)/(c14(2+3c2))
        no-ghost: q_T = 1 > 0, q_V = c14 > 0, q_S = (2+3c2)/c2 > 0
        real speeds: c_V^2 > 0 (<=> c14>0 given K_B>0), c_S^2 > 0
        no instantaneous channel: c14 > 0 STRICTLY (c14 -> 0+ sends c_V^2,
           c_S^2 -> +inf: the aether time-kinetic term is c14 (d_t a^i)^2),
           and 2+3c2 != 0, c2 != 0 (c_S^2 finite and nonzero: c2 -> 0 is the
           frozen/strong-coupling point where FJ alpha_2 has its pole).
        Cerenkov (Elliott-Moore-Stoica; standard EA position: superluminal
           aether modes are REQUIRED, subluminal excluded, instantaneous
           excluded): c_V^2 >= 1 <=> c4 <= 0 ; c_S^2 >= 1.
        BBN (Carroll-Lim form, pure-EA, INHERITED/approximate for AeST):
           |G_cos/G_N - 1| <= 1/8 with G_cos/G_N = (1-c14/2)/(1+3c2/2).
     Region printed at K_B in {0.05, 0.1, 0.25}: inequalities + ASCII scan.
  4. The pure-EA alpha_1 = 0 locus c4 = -K_B is c14 = 0: EXCLUDED (instant.)
     -> in pure EA on c13=0 the LLR-allowed sliver is 0 < c14 < 2.5e-5
     (OMW eq 3.13). The generalized question is whether the scalar drag moves
     the alpha_1 zero to c14 > 0 -- NOT computed here (owed to the solve).
"""
import sympy as sp, sys
P = lambda *a: print(*a, flush=True)
FAIL = []
def CHECK(name, ok):
    P(("  [PASS] " if ok else "  [FAIL] ") + name)
    if not ok: FAIL.append(name)
R = sp.Rational
c1, c2, c3, c4, KB, JY = sp.symbols('c1 c2 c3 c4 K_B J_Y', real=True)
c13 = c1 + c3; c14 = c1 + c4; c123 = c1 + c2 + c3

P("="*74); P("0. DICTIONARY (doc -> FJ)"); P("="*74)
P("  FJ mostly-plus: L_EA = -c1 (DA)^2_{aa} - c2 (D.A)^2 - c3 (DA)^2_{cross} + c4 a.a")
P("  doc writes     : + c2_doc (D.A)^2 + c4_doc a.a")
P("  => c2_FJ = -c2_doc , c4_FJ = +c4_doc ; c1 = -c3 = K_B from -(K_B/2)F^2 (part-1 tie-in)")
P("  [FLAG] THE_GENERALIZED_COMPLETION.md must either flip the sign of its c2 term or")
P("         define c2 through this map; its gate-7 formula c_S^2=c2(2-c14)/(c14(2+3c2)) is")
P("         the FJ-c2 formula, so as written the doc mixes conventions.")

P("\n" + "="*74); P("1. FOSTER-JACOBSON ANCHORS"); P("="*74)
alpha1 = -8*(c3**2 + c1*c4)/(2*c1 - c1**2 + c3**2)
alpha2 = alpha1/2 - (c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4)/(c123*(2 - c14))
GN = 1/(1 - c14/2)
# FJ's own alternative alpha_2 form (gr-qc/0509083 as fetched) -- must agree
alpha2_FJform = ((2*c13 - c14)**2/(c123*(2 - c14))
                 - (12*c3*c13 + 2*c1*c14*(1 - 2*c14) + (c1**2 - c3**2)*(4 - 6*c13 + 7*c14))
                 / ((2 - c14)*(2*c1 - c1**2 + c3**2)))
CHECK("alpha_2 (OMW/Jacobson form) == alpha_2 (FJ gr-qc/0509083 form)",
      sp.simplify(alpha2 - alpha2_FJform) == 0)
c2_null = (-2*c1**2 - c1*c3 + c3**2)/(3*c1); c4_null = -c3**2/c1
CHECK("published alpha=0 surface zeroes alpha_1", sp.simplify(alpha1.subs({c2: c2_null, c4: c4_null})) == 0)
CHECK("published alpha=0 surface zeroes alpha_2", sp.simplify(alpha2.subs({c2: c2_null, c4: c4_null})) == 0)
# mutation controls: a mis-transcribed coefficient must FAIL the surface test
# (an overall sign flip cannot be detected there because alpha_1 = 0 on the surface by
#  construction -- so mutate coefficients, not signs)
alpha1_mut = -8*(c3**2 - c1*c4)/(2*c1 - c1**2 + c3**2)                       # c1 c4 -> -c1 c4
alpha2_mut = alpha1/2 - (c1 + 2*c3 - c4)*(2*c1 + 2*c2 + c3 + c4)/(c123*(2 - c14))  # 3c2 -> 2c2
CHECK("mutation control: alpha_1 with c1c4 -> -c1c4 FAILS the surface test",
      sp.simplify(alpha1_mut.subs({c2: c2_null, c4: c4_null})) != 0)
CHECK("mutation control: alpha_2 with 3c2 -> 2c2 FAILS the surface test",
      sp.simplify(alpha2_mut.subs({c2: c2_null, c4: c4_null})) != 0)
# wf3 control targets (independent evaluation, as in wf4_skeptic1)
for cv, (a1t, a2t) in [((R(3, 10), R(1, 5), R(1, 10), R(1, 20)), (R(-5, 13), R(-461, 572))),
                       ((R(1, 5), R(2, 5), R(-1, 10), R(1, 10)), (R(-24, 37), R(-428, 3145)))]:
    s = dict(zip((c1, c2, c3, c4), cv))
    CHECK(f"wf3 control target c={cv}: alpha_1={a1t}, alpha_2={a2t}",
          sp.simplify(alpha1.subs(s) - a1t) == 0 and sp.simplify(alpha2.subs(s) - a2t) == 0)

P("\n  --- c13 = 0 plane: c1 = K_B, c3 = -K_B, c2, c4 free ---")
sK = {c1: KB, c3: -KB}
a1K = sp.simplify(alpha1.subs(sK)); a2K = sp.factor(sp.simplify(alpha2.subs(sK)))
GNK = sp.simplify(GN.subs(sK))
P("  alpha_1 =", a1K); P("  alpha_2 =", a2K); P("  G_N/G   =", GNK)
CHECK("alpha_1 == -4 c14 = -4(K_B+c4) on c13=0", sp.simplify(a1K + 4*(KB + c4)) == 0)
a2_closed = (KB + c4)*((KB + c4) - c2 + 2*c2*(KB + c4))/(c2*(2 - KB - c4))
CHECK("alpha_2 == c14(c14 - c2 + 2 c2 c14)/(c2(2-c14)) on c13=0", sp.simplify(a2K - a2_closed) == 0)
CHECK("alpha_2 on c13=0 is proportional to c14 (alpha_1=alpha_2=0 <=> c14=0 in pure EA)",
      sp.simplify(a2K.subs(c4, -KB)) == 0)
CHECK("alpha_2 = 0 ALONE at c14 = c2/(1+2c2) with c14 != 0",
      sp.simplify(a2K.subs(c4, c2/(1+2*c2) - KB)) == 0)
CHECK("alpha_1 at c2=c4=0 == -4K_B (Maxwell anchor)", sp.simplify(a1K.subs({c2: 0, c4: 0}) + 4*KB) == 0)
CHECK("alpha_2 pole at c2 -> 0+ with c4=0, K_B=1/5 (c123=0 strong-coupling point)",
      sp.limit(a2K.subs({c4: 0, KB: R(1, 5)}), c2, 0, '+') == sp.oo)
# published surface restricted to c13=0
req_c2 = sp.simplify(c2_null.subs(sK)); req_c4 = sp.simplify(c4_null.subs(sK))
P(f"  published alpha=0 surface at c13=0 requires c2 = {req_c2}, c4 = {req_c4}  (=> c14 = 0 AND c123 = 0)")
CHECK("alpha=0 surface meets c13=0 only at (c2,c4)=(0,-K_B)", req_c2 == 0 and sp.simplify(req_c4 + KB) == 0)
CHECK("that point has c_S^2 = 0/0 (doubly degenerate)",
      sp.simplify((c123*(2-c14)).subs(sK).subs({c2: 0, c4: -KB})) == 0
      and sp.simplify((c14*(1-c13)*(2+c13+3*c2)).subs(sK).subs({c2: 0, c4: -KB})) == 0)

P("\n  --- ANCHOR TABLE (pure EA, scalar frozen): the generalized pipeline must hit these ---")
P("  (K_B, c2, c4) -> alpha_1, alpha_2, G_N/G, c_V^2, c_S^2")
anchors = [(R(1, 5), R(1, 10), R(1, 20)), (R(1, 5), R(1, 10), -R(1, 10)), (R(1, 10), R(1, 20), 0),
           (R(1, 4), R(1, 5), -R(1, 8)), (R(1, 20), R(1, 100), -R(1, 25)), (R(1, 5), 0, R(1, 20))]
for kb, cc2, cc4 in anchors:
    s = {KB: kb, c2: cc2, c4: cc4}
    cv2 = kb/(kb + cc4)
    cs2 = (cc2*(2 - kb - cc4)/((kb + cc4)*(2 + 3*cc2))) if cc2 != 0 else sp.nan
    a2v = a2K.subs(s) if cc2 != 0 else 'POLE (c123=0)'
    P(f"    ({kb},{cc2},{cc4}): alpha_1={a1K.subs(s)}  alpha_2={a2v}  G_N/G={GNK.subs(s)}  c_V^2={cv2}  c_S^2={cs2}")

P("\n" + "="*74); P("2. BANKED c2=c4=0 ANCHOR (base AeST, scalar live) -- wf3_eta_K_final.out"); P("="*74)
etaK = (KB*JY + 2)/(JY + 1)
a1_banked = -4*etaK
P("  eta_K = (K_B J_Y + 2)/(J_Y + 1),  alpha_1 = -4 eta_K,  alpha_3 = 0")
CHECK("J_Y -> oo recovers pure-EA -4K_B", sp.simplify(sp.limit(a1_banked, JY, sp.oo) + 4*KB) == 0)
CHECK("J_Y = 1 gives -2(K_B+2)", sp.simplify(a1_banked.subs(JY, 1) + 2*(KB + 2)) == 0)
grid = [((R(1, 5), 1), R(-22, 5)), ((R(1, 5), 2), R(-16, 5)), ((R(1, 5), 5), -2), ((R(3, 10), 1), R(-23, 5)),
        ((R(1, 10), 1), R(-21, 5)), ((R(1, 2), 1), -5), ((R(1, 4), 1), R(-9, 2)), ((R(3, 10), 3), R(-29, 10)),
        ((R(1, 10), 2), R(-44, 15)), ((R(2, 5), 4), R(-72, 25))]
ok = all(sp.simplify(a1_banked.subs({KB: kb, JY: jy}) - val) == 0 for (kb, jy), val in grid)
CHECK("all 10 banked wf3 grid values alpha_1(0) reproduced by -4 eta_K", ok)
P("  => generalized solve at c2=c4=0 MUST return alpha_1 = -4(K_B J_Y+2)/(J_Y+1); e.g. (K_B,J_Y)=(1/5,1): -22/5")
P("  The decisive unknown: d eta_K / d c4 at fixed K_B, J_Y=1 -- does the '+2' (scalar drag) scale with c14?")
P("  If eta_K(c4) = (c14 J_Y + 2)/(J_Y+1) [drag c4-blind]  -> alpha_1 -> -4 at c14->0: DEAD for all c2,c4.")
P("  If eta_K(c4) = c14 (J_Y + 2/K_B)/(J_Y+1) [drag ~ c14] -> zero only at c14=0: instantaneous, DEAD.")
P("  Only a c4-dependence that is NOT proportional to c14 and crosses zero at 0<c14<2 can pass. NOT-COMPUTED.")

P("\n" + "="*74); P("3. STABILITY REGION on c13=0 (c2, c4 free), speeds from part-1 derivation"); P("="*74)
cT2 = sp.Integer(1); cV2 = KB/(KB + c4); cS2 = c2*(2 - KB - c4)/((KB + c4)*(2 + 3*c2))
cS2_lit = (c123*(2 - c14)/(c14*(1 - c13)*(2 + c13 + 3*c2))).subs(sK)
CHECK("c_S^2 on c13=0 == Jacobson eq.13 restricted", sp.simplify(cS2 - cS2_lit) == 0)
cV2_lit = ((2*c1 - c1**2 + c3**2)/(2*c14*(1 - c13))).subs(sK)
CHECK("c_V^2 on c13=0 == Jacobson eq.12 restricted", sp.simplify(cV2 - cV2_lit) == 0)
CHECK("c_S^2 -> +oo as c14 -> 0+ (instantaneous scalar) for c2>0",
      sp.limit(cS2.subs({c2: R(1, 10), KB: R(1, 10)}), c4, -R(1, 10), '+') == sp.oo)
CHECK("c_V^2 -> +oo as c14 -> 0+ (instantaneous vector)",
      sp.limit(cV2.subs(KB, R(1, 10)), c4, -R(1, 10), '+') == sp.oo)
CHECK("c_S^2 -> 0 as c2 -> 0 (frozen spin-0 = FJ alpha_2 pole)", sp.limit(cS2.subs({KB: R(1, 5), c4: 0}), c2, 0) == 0)
# no-ghost: OMW q's (certified against residue signs in part 1)
qV = KB + c4; qS = (2 + 3*c2)/c2
# Cerenkov
cer_V = sp.solve(cV2 - 1, c4)            # c4 = 0 boundary
P("  c_V^2 >= 1  <=>  c4 <= 0   (boundary c4 =", cer_V, ")")
CHECK("c_V^2 >= 1 <=> c4 <= 0 (given K_B>0, c14>0)", sp.simplify(cV2.subs(c4, 0) - 1) == 0 and cV2.subs({KB: R(1, 10), c4: R(1, 100)}) < 1)
cS2_ge1 = sp.solve(sp.Eq(cS2, 1), c2)
P("  c_S^2 = 1 boundary: c2 =", [sp.simplify(x) for x in cS2_ge1], "  i.e. c2 = c14/(1-2c14) for c14<1/2")
c14s = sp.Symbol('c14', positive=True)
CHECK("c_S^2 >= 1 <=> c2 >= c14/(1-2c14) for 0<c14<1/2, c2>0",
      sp.simplify(cS2.subs(c4, c14s - KB).subs(c2, c14s/(1 - 2*c14s)) - 1) == 0)
# BBN (Carroll-Lim, pure-EA form; INHERITED)
Gratio = (1 - (KB + c4)/2)/(1 + 3*c2/2)
CHECK("BBN form reduces to 1-K_B/2 at c2=c4=0 (repo stage-50 K_B<=1/4 bound)",
      sp.simplify(Gratio.subs({c2: 0, c4: 0}) - (1 - KB/2)) == 0 and sp.solve(1 - KB/2 - R(7, 8), KB) == [R(1, 4)])
c2_bbn_max = sp.solve(sp.Eq(Gratio, R(7, 8)), c2)[0]
P("  BBN upper edge (G_cos/G_N = 7/8): c2 <= ", sp.factor(c2_bbn_max), " = (2/21)(1 - 4 c14)")
c2_bbn_min = sp.solve(sp.Eq(Gratio, R(9, 8)), c2)[0]
P("  BBN lower edge (G_cos/G_N = 9/8): c2 >= ", sp.factor(c2_bbn_min), " (negative for small c14; inactive on c2>0)")
# combined Cerenkov + BBN feasibility on c2>0: c14/(1-2c14) <= (2/21)(1-4c14)
feas = sp.solve(sp.Eq(c14s/(1 - 2*c14s), R(2, 21)*(1 - 4*c14s)), c14s)
c14_star = min(x for x in feas if x > 0)
P("  Cerenkov(c_S^2>=1) AND BBN(7/8) feasible iff c14 <= c14* =", c14_star, "=", float(c14_star))
P("  [INHERITED band: BBN form is the pure-EA Carroll-Lim ratio; AeST's scalar sector shifts G_cos -- SUGGESTIVE only]")

P("\n  Healthy region (no-ghost + real speeds + no instantaneous channel), c13=0:")
P("     0 < c14 = K_B + c4 < 2   AND   ( c2 > 0  OR  c2 < -2/3 )")
P("     [c2 < -2/3 branch: G_cos < 0 (1+3c2/2 < 0) -> cosmologically dead; BBN kills it]")
P("  + Cerenkov (standard EA position; superluminal REQUIRED, not merely allowed):")
P("     -K_B < c4 <= 0   AND   c2 >= c14/(1-2c14)")
P("  + BBN (inherited): c2 <= (2/21)(1-4c14)")
for kb in (R(1, 20), R(1, 10), R(1, 4)):
    P(f"\n  K_B = {kb}:")
    P(f"    no-ghost/finite: c4 in (-{kb}, {2-kb}) open ; c2>0 (or c2<-2/3)")
    P(f"    Cerenkov: c4 in (-{kb}, 0] ; c2 >= (K_B+c4)/(1-2(K_B+c4)) : at c4=0 -> c2 >= {kb/(1-2*kb)} = {float(kb/(1-2*kb)):.4f}")
    P(f"    BBN: c2 <= (2/21)(1-4(K_B+c4)) : at c4=0 -> c2 <= {R(2,21)*(1-4*kb)} = {float(R(2,21)*(1-4*kb)):.4f}")
    both = (kb <= c14_star)
    P(f"    Cerenkov+BBN jointly feasible at c4=0? {both} ; jointly feasible for c4 <= {c14_star - kb} = {float(c14_star-kb):.4f}")
    P(f"    pure-EA alpha_1 = -4 c14 in (-{4*kb}, 0) ; LLR |alpha_1|<1e-4 needs c14 < 2.5e-5 i.e. c4 < {float(-kb + R(1,40000)):.6f} (sliver at the instantaneous wall)")
    # ASCII scan
    P("    scan (rows c4 from -K_B..+0.3, cols c2 from -1..0.4): H=healthy  C=healthy+Cerenkov  B=healthy+Cerenkov+BBN  .=unhealthy")
    c4s = [(-kb) + (R(3, 10) + kb)*i/10 for i in range(11)]
    c2s = [-1 + R(14, 10)*j/14 for j in range(15)]
    P("           c2: " + " ".join(f"{float(x):+.2f}" for x in c2s))
    for cc4 in c4s:
        row = ""
        for cc2 in c2s:
            s = {KB: kb, c2: cc2, c4: cc4}
            c14v = kb + cc4
            if cc2 == 0 or (2 + 3*cc2) == 0 or c14v <= 0 or c14v >= 2:
                row += "   .  "; continue
            healthy = (c14v > 0) and (c14v < 2) and (qS.subs(s) > 0) and (cS2.subs(s) > 0) and (cV2.subs(s) > 0)
            cer = healthy and cV2.subs(s) >= 1 and cS2.subs(s) >= 1
            bbn = cer and abs(Gratio.subs(s) - 1) <= R(1, 8)
            row += "   " + ("B" if bbn else "C" if cer else "H" if healthy else ".") + "  "
        P(f"    c4={float(cc4):+.3f} " + row)
    P("    (left block = the c2 < -2/3 branch: locally healthy but G_cos = G/(1+3c2/2) < 0 -> cosmologically dead)")
    # fine scan of the Cerenkov+BBN corridor (c2 step 0.01, c4 <= 0)
    P("    fine corridor scan, c4 in (-K_B, 0], c2 in [0.01, 0.20] step 0.01 (B = healthy+Cerenkov+BBN):")
    c2f = [R(j, 100) for j in range(1, 21)]
    P("           c2: " + " ".join(f"{float(x):.2f}" for x in c2f))
    nB = 0
    for i in range(5):
        cc4 = -kb + kb*(i+1)/5
        row = ""
        for cc2 in c2f:
            s = {KB: kb, c2: cc2, c4: cc4}; c14v = kb + cc4
            healthy = (0 < c14v < 2) and (qS.subs(s) > 0) and (cS2.subs(s) > 0)
            cer = healthy and cV2.subs(s) >= 1 and cS2.subs(s) >= 1
            bbn = cer and abs(Gratio.subs(s) - 1) <= R(1, 8)
            nB += int(bool(bbn))
            row += "  " + ("B" if bbn else "C" if cer else "H" if healthy else ".") + " "
        P(f"    c4={float(cc4):+.3f} " + row)
    c4_scanned = [-kb + kb*(i+1)/5 for i in range(5)]
    expect_B = any(cc4 <= c14_star - kb for cc4 in c4_scanned)
    P(f"    B-cells found: {nB}  (analytic: B exists iff some scanned c4 <= c14* - K_B = {c14_star - kb}: {expect_B})")
    CHECK(f"K_B={kb}: corridor scan agrees with the analytic feasibility c14 <= {c14_star}", (nB > 0) == expect_B)

P("\n" + "="*74); P("4. THE PURE-EA alpha_1=0 LOCUS IS THE INSTANTANEOUS WALL"); P("="*74)
CHECK("alpha_1^{EA} = 0 on c13=0 <=> c14 = 0", sp.solve(a1K, c4) == [-KB])
CHECK("at c14=0 the aether time-kinetic coefficient (c1+c4) vanishes -> A^i non-propagating (instantaneous)",
      sp.simplify(c14.subs(sK).subs(c4, -KB)) == 0)
P("  => in PURE EA on c13=0, alpha_1 = alpha_2 = 0 is reachable only at the excluded corner c14 = 0.")
P("     OMW 1802.04303 eq 3.13/3.20: surviving pure-EA sliver 0 < c14 <= 2.5e-5, c14 <~ c2 <~ 0.095.")
P("     The generalized-AeST question (owed to the solve, NOT computed here): does the scalar drag")
P("     2(2-K_B) a.grad(phi) shift the alpha_1 zero to c14 > 0 while alpha_2 also vanishes there?")

P("\n" + "="*74); P("SUMMARY"); P("="*74)
P("  alpha_1 = -4c14, alpha_2 = c14(c14-c2+2c2c14)/(c2(2-c14)) on c13=0   [SOLID, FJ-transcribed + self-consistent]")
P("  healthy region: 0<c14<2, c2>0 (c2<-2/3 cosmologically dead); Cerenkov: c4<=0, c2>=c14/(1-2c14)")
P("  BBN(inherited): c2<=(2/21)(1-4c14); Cerenkov+BBN feasible only for c14 <= %s" % float(c14_star))
P("  pure-EA alpha=0 locus = c14=0 = instantaneous wall (EXCLUDED)          [SOLID]")
P(f"  FAILED CHECKS: {len(FAIL)} {FAIL}")
sys.exit(1 if FAIL else 0)
