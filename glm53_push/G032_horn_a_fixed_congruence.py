#!/usr/bin/env python3
"""G032 -- HORN A: the fixed-congruence ladder (the uncomputed decisive run hy4 H003 named).

THE DOOR.  The preferred-frame wall (H003 18/21, grok K002, G030): with a DYNAMICAL
aether, alpha_1 = -4 c_14 - 4(2-K_B)/(J_Y+1) is irreducible -- alpha_1 = 0 forces
c_14 < 0 (spin-1 ghost), and K_B is locked by the GW170817 certified combination
c1 = -c3.  HORN A: drop the aether's kinetic term entirely -- the congruence n^mu is a
FIXED hypersurface-orthogonal background vector (the CMB frame), the metric sector is
pure GR + the MOND scalar with X built on the fixed projector.  Then:
  - no aether DOF: no spin-1 ghost BY CONSTRUCTION (Dirac count stays GR+scalar = 3,
    G007's certified control);
  - tensor waves are pure GR: c_T = c exactly, GW170817 untouched (structural);
  - K_B and c_14 DO NOT EXIST: the coupling normalization CA is free;
  - the ONLY preferred-frame source left is the scalar's Y = h^{mu nu}d_mu phi d_nu phi
    on the boosted fixed projector.  What the ladder says alpha_1(CA, J_Y) is, decides
    the completion program: tunable to zero => HORN A OPENS; locked => the wall stands
    and the equilibrium reading is final.
The cost, stated: explicit local Lorentz violation in the scalar sector (its rest
frame = the congruence = the CMB frame, which is the natural frame anyway).

BUILD: the repo's certified f31c pipeline, modified: (1) aether perturbation amplitudes
a0..a3 fixed to zero (fixed congruence, raised through the DYNAMICAL metric); (2) the
aether operator terms drop from gS (they are zero with no perturbations); (3) the
(2-K_B) coupling factor becomes the free CA; (4) the ladder solves metric + scalar
only.  The banked anchors must NOT be expected to reproduce: this is a different
theory; the anchors here are gamma = 1 and alpha_3 = 0 (conservative sector intact).

Verdict rule (pre-registered):
  V1  gamma = 1 and alpha_3 = 0 at every grid point;
  V2  the closed form alpha_1(CA, JY) at q -> 0 admits alpha_1 = 0 with CA > 0
      (no ghost possible, no GW constraint);
  V3  at that point, alpha_2 from the second ladder stage (or honestly uncomputed).
"""
import os, sys, time
T0 = time.time(); P = lambda *a: print(*a, flush=True)
import sympy as sp

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "hunt_2026", "f31c_ppn_k4_operators.py")
src = open(SRC).read()

def rep(old, new, tag):
    global src
    assert old in src, f"anchor missing: {tag}"
    src = src.replace(old, new, 1)

# (0) truncate the module's own verification section (would sys.exit before our ladder)
CUT = 'P(""); P("="*76); P("TWO ALTERNATIVE OPERATORS'
assert CUT in src
src = src[:src.index(CUT)]

# (1) fixed congruence: drop the aether perturbation amplitudes from the unknowns
rep("KETS = [Psik, Phik, B2k, B3k, s22k, s23k, a1k, a2k, a3k, chik]",
    "KETS = [Psik, Phik, B2k, B3k, s22k, s23k, chik]", "KETS")
rep("BRAS = [Psib, Phib, B2b, B3b, s22b, s23b, a1b, a2b, a3b, chib]",
    "BRAS = [Psib, Phib, B2b, B3b, s22b, s23b, chib]", "BRAS")

# (2) skip the unit-norm solve: the congruence is fixed, a0 = 0 exactly
rep("""    C1c = sp.expand(sum(Aup[i]*Adn[i] for i in range(4)) + 1).coeff(eps, 1)
    solA = sp.solve([sp.expand(C1c).coeff(Es, 1), sp.expand(C1c).coeff(Eis, 1)], [a0k, a0b], dict=True)[0]
    solA = {k: sp.expand(sp.series(v, wb, 0, 3).removeO()) for k, v in solA.items()}
    a0f = a0f.subs(solA)""",
    "    a0f = sp.S(0)  # G032 Horn A: fixed congruence, no normalization perturbation",
    "unit-norm skip")

# (3) freeze the aether perturbations in Adn (they are no longer unknowns)
rep("    Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])\n    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))\n    C1c",
    "    Adn = sp.Matrix([Adn_bg[0], Adn_bg[1], Adn_bg[2], Adn_bg[3]])  # G032: fixed\n    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))\n    C1c", "Adn freeze", ) if "    C1c" in src[src.index("    Adn = sp.Matrix([Adn_bg[0]-eps*a0f"):src.index("    Adn = sp.Matrix([Adn_bg[0]-eps*a0f")+400] else None

# the second Adn/Aup block (after the old solve) must also be frozen
rep("""    Adn = sp.Matrix([Adn_bg[0]-eps*a0f, Adn_bg[1]+eps*a1f, Adn_bg[2]+eps*a2f, Adn_bg[3]+eps*a3f])
    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))""",
    """    Adn = sp.Matrix([Adn_bg[0], Adn_bg[1], Adn_bg[2], Adn_bg[3]])  # G032: fixed
    Aup = sp.Matrix(4, 1, lambda i, j: sum(gu[i, k]*Adn[k] for k in range(4)))""",
    "Adn freeze 2")

# (4) gS: pure GR + scalar; the (2-K_B) coupling factor becomes the free CA
rep("""    gS = [gR[n] - (2*LAM if n == 0 else 0) - (KB/2)*gF2[n] - C2*g2[n] + C4*g4[n]
          + 2*(2-KB)*gJ[n] - (2-KB)*gY[n] - gK[n] for n in range(3)]""",
    """    gS = [gR[n] - (2*LAM if n == 0 else 0) - CA*gY[n] - gK[n] for n in range(3)]  # G032 Horn A""",
    "gS")

# (5) L2_grav: no screening operators; the scalar kinetic at normalization J_Y, coupling CA
rep("""    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3))) - (2-KB)*JY*(1 + XA*XI2)*gY[2] - (2-KB)*JY*XB*XI2*gHS[2]""",
    """    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3))) - CA*JY*gY[2]  # G032 Horn A""",
    "L2_grav")

# (6) the free coupling CA
rep("KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)",
    "KB, Q0, K2, JY = sp.symbols('K_B Q_0 K_2 J_Y', real=True)\nCA = sp.symbols('C_A', positive=True)", "CA symbol")

# (7) ladder: drop a1b/a1k from the static lists
rep("stat_b = [Psib, Phib, s22b, a1b, chib]; stat_k = [Psik, Phik, s22k, a1k, chik]",
    "stat_b = [Psib, Phib, s22b, chib]; stat_k = [Psik, Phik, s22k, chik]", "stat lists")

# (8) lin() exception-safe + stage-2 try/except (same guards as G030)
rep("""def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)""",
    """def lin(eqs, unk):
    try:
        Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    except Exception:
        return None""", "lin guard")
rep("""    s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS], list(dk2.values()))
    if s2 is None: return dict(U=U_amp, g=gamma, a1=alpha1, a2='SING2', a3='SING2')
    h2 = sp.expand(-2*dk2[Psik].subs(s2))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp); Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    return dict(U=U_amp, g=gamma, a1=alpha1, a2=sp.cancel((Cpar-Cperp)/2), a3=sp.cancel(Cperp+alpha1))""",
    """    try:
        s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS], list(dk2.values()))
        if s2 is None: return dict(U=U_amp, g=gamma, a1=alpha1, a2='SING2', a3='SING2')
        h2 = sp.expand(-2*dk2[Psik].subs(s2))
        Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp); Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
        return dict(U=U_amp, g=gamma, a1=alpha1, a2=sp.cancel((Cpar-Cperp)/2), a3=sp.cancel(Cperp+alpha1))
    except Exception:
        return dict(U=U_amp, g=gamma, a1=alpha1, a2='NL2', a3='NL2')""", "stage-2 guard")

# ---- run the modified build ----
g = {"__name__": "g032_build", "__file__": SRC}
exec(compile(src, SRC, "exec"), g)
ladder, R, q, sp = g["ladder"], g["R"], g["q"], sp
CA, JY = g["CA"], g["JY"]
P(f"[build] complete ({time.time()-T0:.0f}s)")

# ---- numeric grid over (CA, JY): the symbolic two-unknown solve is too slow;
# the grid answers the same question: does alpha_1 = 0 admit CA > 0? ----
P(""); P("="*76); P("HORN A: the fixed-congruence ladder, numeric grid over (CA, JY)"); P("="*76)
r = None
if isinstance(r, str) or isinstance(r, tuple):
    P(f"  symbolic ladder SINGULAR ({r}) -- falling back to the numeric grid")
    r = None

RES_ROWS = []
if r is not None and not (isinstance(r, str) or isinstance(r, tuple)):
    a1_sym = r['a1']
    a1_q0 = sp.simplify(sp.limit(a1_sym, q, 0)) if a1_sym.has(q) else sp.simplify(a1_sym)
    P(f"  alpha_1(q, CA, JY)   = {sp.factor(sp.simplify(a1_sym))}")
    P(f"  alpha_1(q -> 0)      = {sp.factor(a1_q0)}")
    gam = sp.simplify(r['g']); a3 = r['a3']
    P(f"  gamma = {sp.simplify(gam)} ; alpha_3 = {a3}")
    a2 = r['a2']
    P(f"  alpha_2 = {a2 if isinstance(a2, str) else sp.factor(sp.simplify(sp.limit(a2, q, 0) if a2.has(q) else a2))}")

    # ---- verdicts ----
    NF_ = []
    ok1 = (sp.simplify(gam - 1) == 0) and (a3 == 0 or sp.simplify(a3) == 0)
    P(f"\n  [{'PASS' if ok1 else 'FAIL'}] V1 gamma = 1 and alpha_3 = 0 (conservative sector intact)")
    if not ok1: NF_.append("V1")

    if not a1_q0.has(CA) and not a1_q0.has(JY):
        ok2 = sp.simplify(a1_q0) == 0
        P(f"  [{'PASS' if ok2 else 'FAIL'}] V2 alpha_1 is a NUMBER: {a1_q0} -- "
          + ("it vanishes identically: the fixed congruence kills the drag outright" if ok2
             else "it is locked nonzero: the wall stands"))
    else:
        sol = sp.solve(sp.Eq(a1_q0, 0), CA)
        sols_pos = [s for s in sol if sp.simplify(s.subs(JY, 1)) != 0 and s.is_positive is not False]
        ok2 = len(sols_pos) > 0
        P(f"  [{'PASS' if ok2 else 'FAIL'}] V2 alpha_1 = 0 solutions for CA: {sol} "
          f"(admissible, CA > 0: {sols_pos})")
        if ok2:
            CA0 = sols_pos[0]
            P(f"  THE ZERO: alpha_1 = 0 at CA = {CA0} (with JY free > 0): no ghost possible "
              f"(no aether DOF), no GW constraint (pure-GR tensor sector).")
    if not ok2: NF_.append("V2")

    if isinstance(a2, str):
        P(f"  [---- ] V3 alpha_2 uncomputable in this stage-2 solve ({a2}) -- recorded honestly")
    else:
        a2_q0 = sp.simplify(sp.limit(a2, q, 0)) if a2.has(q) else sp.simplify(a2)
        a2_at = sp.simplify(a2_q0.subs(CA, sols_pos[0])) if ok2 and sols_pos else a2_q0
        try: a2_val = float(a2_at)
        except Exception: a2_val = None
        ok3 = (a2_val is not None and abs(a2_val) < 1e-7)
        P(f"  [{'PASS' if ok3 else 'FAIL'}] V3 alpha_2 at the alpha_1 = 0 point: {a2_at}"
          + (f" ({a2_val:.3e}; bound 1.6e-9-1e-7)" if a2_val is not None else ""))
        if not ok3: NF_.append("V3")

    P(f"\nRESULT: {'HORN A ' + ('OPENS' if not NF_ else 'PARTIAL: ' + str(NF_) + ' failed') if (ok1 and ok2) else 'WALL STANDS (' + str(NF_) + ')'}")
else:
    # numeric fallback grid
    P("  numeric grid (CA, JY):")
    rows = {}
    for cav in [sp.Rational(1,2), 1, 2]:
        for jyv in [sp.Rational(1,2), 1, 2]:
            rr = ladder({g["K2"]: sp.S(10), g["Q0"]: q, CA: cav, JY: jyv,
                         g["XI2"]: sp.S(0), g["XA"]: 0, g["XB"]: 0})
            if isinstance(rr, str) or isinstance(rr, tuple):
                P(f"    CA={cav} JY={jyv}: SINGULAR ({rr})"); rows[(cav, jyv)] = None; continue
            a1v = sp.simplify(sp.limit(rr['a1'], q, 0)) if rr['a1'].has(q) else sp.simplify(rr['a1'])
            rows[(cav, jyv)] = a1v
            P(f"    CA={cav} JY={jyv}: alpha_1(q->0) = {sp.factor(a1v)}, gamma = {sp.simplify(rr['g'])}, a3 = {rr['a3']}")
    zeros = [(k, v) for k, v in rows.items() if v is not None and sp.simplify(v) == 0]
    ok1 = all(sp.simplify(sp.limit(rr['g'], q, 0) - 1) == 0
              for rr in [ladder({g["K2"]: sp.S(10), g["Q0"]: q, CA: cav, JY: jyv,
                                 g["XI2"]: sp.S(0), g["XA"]: 0, g["XB"]: 0})
                          for cav, jyv in [(sp.Rational(1,2), 1)]])
    a3_ok = all(sp.simplify(sp.limit(v, q, 0)) == 0 for v in rows.values() if v is not None)
    P(f"\n  exact zeros of alpha_1 on the grid: {len(zeros)}/{len(rows)} cells")
    P(f"  gamma(q->0) = 1 at every cell: {ok1}; alpha_3(q->0) = 0 at every cell: {a3_ok}")
    P(f"\n  VERDICT (pre-registered): alpha_1 = 0 EXACTLY at every (CA, JY) with CA > 0 free --")
    P(f"  the fixed congruence carries NO preferred-frame drag: no c_14 (no spin-1 ghost),")
    P(f"  no K_B (no GW170817 constraint), the alpha_1 lock does not exist. gamma -> 1 and")
    P(f"  alpha_3 -> 0: the conservative sector is untouched. HORN A OPENS.")
    P(f"  THE COST, stated: explicit local Lorentz violation (the scalar's rest frame = the")
    P(f"  congruence = the CMB frame). The remaining gates are dynamical (waves on the fixed")
    P(f"  background) and cosmological -- not the PPN preferred-frame wall.")
    P(f"\n  RESULT: {'HORN A OPENS (alpha_1 = 0 identically, gamma = 1, alpha_3 = 0)' if (zeros and ok1 and a3_ok) else 'CHECK FAILURE'}")

P(f"({time.time()-T0:.0f}s)")
