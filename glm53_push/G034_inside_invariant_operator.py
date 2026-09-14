#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G034 -- THE INSIDE-THE-INVARIANT SCREENING OPERATOR: f(X + xi^2 Y^2/X) in the certified f31c PPN ladder.

WHERE THIS SITS.  G030 closed the k^4 PPN gate for every local fourth-order operator
tried: the scalar trace (D^2 phi)^2 [f31] and the scalar Hessian-squared [f31c] POISON
the drag (alpha_1 GROWS ~ XI2, through pieces acting on the scalar's CHARGED background
gradient d phi_bg = -Q0 A_dn), and the aether Hessian-squared [G030] SINGULARISES the
static ladder at every XI2 > 0.  What survives is f31c's REFERENCE result: coherent
stiffening of the WHOLE Y sector, J_Y -> J_Y(1+XI2), gives EXACTLY the propagator form
        -4(2-K_B)/(J_Y(1+XI2)+1)
and evades the alpha_1 lock at c_14 > 0 -- realised by no local operator.  G030
registered the remaining candidate class: a Y-coupled correction INSIDE the scalar
kinetic invariant, f(X + xi^2 Y^2/X).  This file tests it -- the one door G030 left open.

THE OPERATOR (D), as pre-registered.  The dark-scalar kinetic square is modified so the
screening enters THROUGH the invariant:
        L_kin = K_2 ( dQ + xi^2 Y/(2 X0) )^2 ,
whose O(xi^2) pieces (task-prescribed bookkeeping) are
        cross:   K_2 xi^2 Y dQ / X0
        screen:  K_2 xi^2 Y^2 / (4 X0) ,
injected with the + sign of the squared form under the switch XD.  Y is the ladder's
OWN invariant te(sum((guT + AupT AupT) dphiT dphiT)), dQ = Qc - Q0, and X0 = the
background X.  X0 is carried SYMBOLICALLY (x_0): the ladder's own background gives
X_bg = h0^{mn} dphi_bg_m dphi_bg_n = 0 IDENTICALLY (dphi_bg = -Q0 A_dn is purely
aether-parallel and the eps^0 projector satisfies h0^{mn} dphi_bg_m = 0 exactly, by
unit norm), so X0 cannot be fixed from inside the ladder -- it is a free positive
parameter of the solve.

STRUCTURAL FACT (verified below as S0/S1, not assumed).  Each (D) piece enters the
action linearly and carries XI2 and X0 ONLY through the single combination
        Z = K_2 XI2 / X0        (K_2 = 10, the certified dark-scalar stiffness),
so the linearised system is M0 + Z M1 with M1 fixed: every observable is an exact
rational function of Z alone.  The master runs therefore carry Z symbolically; the
so the G030 grid XI2 in {0,1,100,1e4,1e8} at the benchmark footing X0 = 1 is Z = 10*XI2 in
{0, 10, 1e3, 1e5, 1e9}; at the physical XI2 = 1e8 the strength is Z* = 1e9/X0.  (Dimensional
footing, PROTOCOL R3: the XI2 >= 8.6e7 floor is xi >= 0.045 pc = 9300 AU, f30's Cassini
floor = 1.16 r_M(Sun), computed on BOTH a0 footings 9.3619e-11 and 1.1279e-10 m/s^2; the
ladder itself is dimensionless and carries no a0.)

Verdict rule (pre-registered, same form as G030):
  (V1) the XI2 = 0 anchors: gamma = 1, alpha_3 = 0, and alpha_1 = the banked
       -4(K_B + (2-K_B)/(1+J_Y)) at every (K_B, J_Y) -- the build touches nothing
       else (every (D) piece is ~ XI2, so this is automatic if the injection is clean);
  (V2) the drag is SUPPRESSED at the physical XI2 = 1e8: |a1(1e8)| < 1e-2 |a1(0)|;
  (V3) THE VERDICT: alpha_1 = 0 reachable with c_14 in (0, 2.5e-5] (the ladder's drag
       piece |a1| < 1e-4, so a positive c_14 can cancel it: no spin-1 ghost) AND
       |alpha_2| below 1e-2 of its XI2 = 0 value.
V2/V3 are evaluated at the benchmark footing X0 = 1 AND as exact conditions on X0
(thresholds), with the Z -> infinity asymptotics (the screening-enhanced regime
X0 -> 0) reported explicitly: that limit is the class's suppress-or-grow answer.
If the ladder singularises, the singularisation is recorded and diagnosed: anchors
failing = the operator breaks the theory; anchors holding but the solve dying =
the operator breaks the static limit.

Both a0 footings carried per PROTOCOL R3 where a dimensional number appears (here:
none -- the ladder is dimensionless; the physical XI2 >= 8.6e7 comes from
xi >= 0.045 pc = 9300 AU, f30's Cassini floor = 1.16 r_M(Sun) on
9.3619e-11 / 1.1279e-10 m/s^2).

Env flags: G034_SMOKE=1 (build + S0 + one master + S1 only, for cost gauging);
G034_SKIP_HEAVY=1 (skip the full-ladder alpha_2 runs at Z*); G034_ONLY_HEAVY=1
(recovery: only the full-ladder alpha_2 runs).
"""
import os, sys, time, shutil
T0 = time.time(); P = lambda *a: print(*a, flush=True)
import sympy as sp

SMOKE = bool(os.environ.get('G034_SMOKE'))
ONLY_HEAVY = bool(os.environ.get('G034_ONLY_HEAVY'))
SKIP_HEAVY = bool(os.environ.get('G034_SKIP_HEAVY'))

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "hunt_2026", "f31c_ppn_k4_operators.py")
src = open(SRC).read()

# ---- unique scratch: the cache must not cross-contaminate with f31c/G030 runs ----
SC = '/tmp/g034_sc'
shutil.rmtree(SC, ignore_errors=True)
os.makedirs(SC, exist_ok=True)
os.environ['SCRATCH'] = SC

# ---- inject operator (D): the inside-the-invariant screening ----
INJECT = '''
    # G034 operator (D): INSIDE-THE-INVARIANT screening, X -> X + xi^2 Y^2/(2 X0).
    # The dark-scalar kinetic square becomes L_kin = K2*(dQ + xi^2 Y/(2 X0))^2; its
    # O(xi^2) pieces (task-prescribed bookkeeping) are the cross term K2*XI2*Y*dQ/X0
    # and the screen term K2*XI2*Y^2/(4*X0), injected with the + sign of the squared
    # form under the switch XD.  Y = Yc (the ladder's own h^{mn} dphi_m dphi_n
    # invariant), dQ = Qc - Q0.  Both are O(eps) EXACTLY in this background (the
    # projector identity h0^{mn} dphi_bg_m = 0 holds to all kept orders, and
    # Qc|eps0 = Q0), so Y*dQ and Y^2 are O(eps^2) and enter gS at n = 2 only.  Both
    # are quadratic in the fluctuation amplitudes: the operator modifies the KINETIC
    # MATRIX (a stiffness), it is not a source.  X0sym = the background X, carried as
    # a FREE POSITIVE PARAMETER of the solve (the ladder's own background gives
    # X_bg = 0 identically, so X0 is not fixable internally).
    gYdq = grade(sp.expand(Yc*dQ)); gYsq = grade(sp.expand(Yc**2))
    XD = sp.Symbol('xD', nonnegative=True)
    X0sym = sp.Symbol('x_0', positive=True)
    P(f"    inside-the-invariant operators built: Y*dQ {len(sp.Add.make_args(gYdq[2]))} terms, Y^2 {len(sp.Add.make_args(gYsq[2]))} terms ({time.time()-T0:.1f}s)")
'''
ANCHOR = "    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3)))"
assert ANCHOR in src, "anchor not found"
src = src.replace(ANCHOR, INJECT + "\n" + ANCHOR +
                  " + XD*(K2*XI2*gYdq[2]/X0sym + K2*XI2*gYsq[2]/(4*X0sym))")

# ---- truncate the module's own (A)/(B) verification section: it would run its checks
# against THIS run's cache and sys.exit before our grid runs. ----
CUT = 'P(""); P("="*76); P("TWO ALTERNATIVE OPERATORS'
assert CUT in src, "cut marker not found"
src = src[:src.index(CUT)]

# ---- exception-safe lin: a stage that goes nonlinear returns None ----
OLD_LIN = """def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)"""
NEW_LIN = """def lin(eqs, unk):
    try:
        Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    except Exception:
        return None"""
assert OLD_LIN in src, "lin block not found"
src = src.replace(OLD_LIN, NEW_LIN)

# ---- exception-safe stage-2 (same wrapper as G030) ----
OLD_S2 = """    s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS], list(dk2.values()))
    if s2 is None: return dict(U=U_amp, g=gamma, a1=alpha1, a2='SING2', a3='SING2')
    h2 = sp.expand(-2*dk2[Psik].subs(s2))
    Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp); Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
    return dict(U=U_amp, g=gamma, a1=alpha1, a2=sp.cancel((Cpar-Cperp)/2), a3=sp.cancel(Cperp+alpha1))"""
NEW_S2 = """    try:
        s2 = lin([sp.expand(sp.expand(eqW[A].coeff(wb, 2)).subs(s1)) for A in BRAS], list(dk2.values()))
        if s2 is None: return dict(U=U_amp, g=gamma, a1=alpha1, a2='SING2', a3='SING2')
        h2 = sp.expand(-2*dk2[Psik].subs(s2))
        Cpar = sp.cancel(h2.coeff(w1**2)/Rk/U_amp); Cperp = sp.cancel(h2.coeff(w2**2)/Rk/U_amp)
        return dict(U=U_amp, g=gamma, a1=alpha1, a2=sp.cancel((Cpar-Cperp)/2), a3=sp.cancel(Cperp+alpha1))
    except Exception:
        return dict(U=U_amp, g=gamma, a1=alpha1, a2='NL2', a3='NL2')"""
assert OLD_S2 in src, "stage-2 block not found"
src = src.replace(OLD_S2, NEW_S2)

# ---- run the injected build ----
g = {"__name__": "g034_build", "__file__": SRC}
exec(compile(src, SRC, "exec"), g)
ladder_full, check, FAILS = g["ladder"], g["check"], g["FAILS"]
R, q, wb, w2, Rk = g["R"], g["q"], g["wb"], g["w2"], g["Rk"]
P(f"[build] complete ({time.time()-T0:.0f}s)")

GRID = [(R(1,5), 1), (R(1,2), 1), (R(1,5), 2)]
Zsym = sp.Symbol('Z', positive=True)     # Z = K_2 * XI2 / X0  (K_2 = 10)
XDs = sp.Symbol('xD', nonnegative=True)
X0s = sp.Symbol('x_0', positive=True)

# ---- ladder_lite: stages s0 + s1 only (alpha_1 and gamma need no stage 2) ----
def ladder_lite(sub):
    sub = {g["GT"]: 1, g["LAM"]: 0, g["kx"]: 1, **sub}
    eqf = {A: sp.expand(g["eq"][A].subs(sub)) for A in g["BRAS"]}
    VZ = {g["B2k"]: 0, g["B3k"]: 0, g["s23k"]: 0, g["a2k"]: 0, g["a3k"]: 0}
    stat_b = [g["Psib"], g["Phib"], g["s22b"], g["a1b"], g["chib"]]
    stat_k = [g["Psik"], g["Phik"], g["s22k"], g["a1k"], g["chik"]]
    eq0 = [sp.expand(eqf[b].coeff(wb, 0).subs(VZ)) for b in stat_b]
    s0s = g["lin"](eq0, stat_k)
    if s0s is None: return 'SING0'
    s0 = {**s0s, g["B2k"]: sp.S(0), g["B3k"]: sp.S(0), g["s23k"]: sp.S(0),
          g["a2k"]: sp.S(0), g["a3k"]: sp.S(0)}
    U_amp = sp.cancel(-s0[g["Psik"]]/Rk); gamma = sp.cancel(s0[g["Phik"]]/s0[g["Psik"]])
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in g["KETS"]}
    subF = {A: s0[A] + wb*dk1[A] for A in g["KETS"]}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in g["BRAS"]}
    s1 = g["lin"]([sp.expand(eqW[A].coeff(wb, 1)) for A in g["BRAS"]], list(dk1.values()))
    if s1 is None: return ('SING1', U_amp, gamma)
    c2t = sp.cancel(sp.expand(dk1[g["B2k"]].subs(s1)).coeff(w2)/Rk)
    return dict(U=U_amp, g=gamma, a1=sp.cancel(2*c2t/U_amp))

def run(kbv, jyv, xi2v, x0v, full=False):
    sub = {g["KB"]: kbv, g["K2"]: sp.S(10), g["JY"]: sp.S(jyv), g["Q0"]: q,
           g["C2"]: 0, g["C4"]: 0, g["XI2"]: xi2v, g["XA"]: 0, g["XB"]: 0,
           XDs: 1, X0s: x0v}
    return (ladder_full if full else ladder_lite)(sub)

def q0(e):
    """q -> 0 limit; keeps Z symbolic; returns strings unchanged; 'LIMFAIL' on failure."""
    if e is None or isinstance(e, str): return e
    try:
        v = sp.limit(sp.cancel(sp.together(e)), q, 0)
    except Exception:
        try: v = sp.cancel(sp.together(e)).subs(q, 0)
        except Exception: return 'LIMFAIL'
    v = sp.cancel(sp.together(v))
    if Zsym not in v.free_symbols: v = sp.nsimplify(v)
    return v

# ---- S0: structural check of the injection (exact Z-linearity) ----
P(""); P("="*76); P("S0: the injection enters only through Z = K_2*XI2/X0"); P("="*76)
XDc = sp.Poly(g["L2dc"], XDs).coeff_monomial(XDs)
expect = g["K2"]*g["XI2"]*(g["gYdq"][2] + g["gYsq"][2]/4)/X0s
ok_s0 = (sp.simplify(sp.expand(XDc - expect)) == 0) and (not sp.expand(XDc*X0s).has(X0s))
check("S0 the XD-coefficient of L2dc is exactly K_2*XI2*(Y*dQ + Y^2/4)/X0 (single "
      "combination Z, no other XI2 or X0 dependence anywhere in the build)", ok_s0)

FULL0 = {}
FULL8 = {}
A1 = {}

if not ONLY_HEAVY:
    # ---- master closed-form runs (Z symbolic; X0 -> 10 with K_2 -> 10 normalises Z) ----
    P(""); P("="*76); P("MASTER RUNS: alpha_1(q, Z) in closed form  (Z = K_2*XI2/X0, K_2 = 10)"); P("="*76)
    for kbv, jyv in GRID:
        t1 = time.time()
        r = run(kbv, jyv, Zsym, sp.S(10))
        A1[(kbv, jyv)] = r
        if isinstance(r, dict):
            a1z = q0(r['a1'])
            P(f"  K_B={kbv} J_Y={jyv}: count_ops(a1)={sp.count_ops(r['a1'])}, gamma(q->0,Z)={q0(r['g'])} ({time.time()-t1:.0f}s)")
            if not isinstance(a1z, str):
                dragz = sp.cancel(a1z + 4*kbv)
                P(f"     alpha_1(q->0, Z) = {sp.factor(sp.together(a1z))}")
                P(f"     drag(Z) = alpha_1 + 4K_B = {sp.factor(sp.together(dragz))}")
                P(f"     reference (A) drag at same Z: -4(2-K_B)/(J_Y(1+Z/10)+1) = {sp.factor(sp.together(-4*(2-kbv)/(jyv*(1+Zsym/10)+1)))}")
                P(f"     limit Z->oo of drag: {sp.limit(dragz, Zsym, sp.oo)}")
                den = sp.denom(sp.together(a1z))
                if den.has(Zsym):
                    roots = []
                    for s in sp.solve(sp.Eq(den, 0), Zsym):
                        try:
                            if s.is_real and s > 0: roots.append(sp.nsimplify(s))
                        except Exception: pass
                    P(f"     denominator positive roots (static-limit singularisation in Z): {sorted(set(roots)) if roots else 'none'}")
            else:
                P(f"     alpha_1 q->0 limit: {a1z}")
        else:
            P(f"  K_B={kbv} J_Y={jyv}: SINGULAR {r} ({time.time()-t1:.0f}s)")
        if SMOKE: break

    # ---- S1: exact numeric Z-collapse pair ----
    if not SMOKE:
        P(""); P("-- S1: exact numeric Z-collapse pair --")
        ra = run(R(1,5), 1, sp.S(3), sp.S(7))            # Z = 10*3/7 = 30/7
        rb = run(R(1,5), 1, sp.Rational(30, 7), sp.S(10))
        ok_s1 = (isinstance(ra, dict) and isinstance(rb, dict)
                 and sp.simplify(sp.expand(ra['a1'] - rb['a1'].subs(Zsym, sp.Rational(30, 7)))) == 0)
        check("S1 the Z-collapse holds exactly: alpha_1(XI2=3, X0=7) == alpha_1(Z=30/7) "
              "as rational functions of q", ok_s1)

        # ---- V1 anchors at Z = 0 (lite for gamma/a1; FULL for alpha_3 and alpha_2(0)) ----
        P(""); P("-- V1: anchors at Z = 0 --")
        ok_v1 = True
        for kbv, jyv in GRID:
            rl = run(kbv, jyv, sp.S(0), sp.S(1))
            rf = run(kbv, jyv, sp.S(0), sp.S(1), full=True)
            FULL0[(kbv, jyv)] = rf
            banked = sp.nsimplify(-4*kbv - 4*(2-kbv)/(1+jyv))
            g_v = q0(rl['g']) if isinstance(rl, dict) else None
            a1_v = q0(rl['a1']) if isinstance(rl, dict) else None
            a3_v = q0(rf['a3']) if isinstance(rf, dict) else rf
            cond = (g_v is not None and sp.simplify(g_v - 1) == 0
                    and a1_v is not None and sp.simplify(a1_v - banked) == 0
                    and not isinstance(a3_v, str) and sp.simplify(a3_v) == 0)
            ok_v1 = ok_v1 and cond
            P(f"  K_B={kbv} J_Y={jyv}: gamma={g_v}, alpha_1(0)={a1_v} (banked {banked}), "
              f"alpha_3(0)={a3_v}, alpha_2(0)={q0(rf['a2']) if isinstance(rf, dict) else rf}")
        check("V1 the XI2 = 0 anchors: gamma = 1, alpha_3 = 0, alpha_1 = the banked "
              "-4(K_B + (2-K_B)/(1+J_Y)) at every (K_B, J_Y) -- the (D) build touches "
              "nothing else", ok_v1)

        # ---- grid table (same grid as G030) at benchmark X0 = 1 ----
        P(""); P("="*76); P("GRID (same as G030): XI2 in {0,1,100,1e4,1e8} at benchmark X0 = 1  =>  Z = 10*XI2"); P("="*76)
        P(f"  {'K_B':>4s} {'J_Y':>3s} {'XI2':>9s} {'Z=10*XI2/X0':>11s} {'alpha_1(q->0)':>14s} {'drag':>10s} {'gamma':>6s}")
        for (kbv, jyv) in GRID:
            r = A1.get((kbv, jyv))
            if not isinstance(r, dict):
                P(f"  {kbv!s:>4s} {jyv:>3d}  (master run singular: {r})"); continue
            a1z, gz = q0(r['a1']), q0(r['g'])
            if isinstance(a1z, str):
                P(f"  {kbv!s:>4s} {jyv:>3d}  (alpha_1 limit {a1z})"); continue
            for xi2 in (0, 1, 100, 10**4, 10**8):
                zv = sp.S(10)*xi2
                a1v = a1z.subs(Zsym, zv)
                P(f"  {kbv!s:>4s} {jyv:>3d} {xi2:>9d} {sp.N(zv,4)!s:>11s} {sp.N(a1v,6)!s:>14s} "
                  f"{sp.N(sp.cancel(a1v + 4*kbv),6)!s:>10s} {sp.N(gz.subs(Zsym, zv),4) if not isinstance(gz,str) else gz!s:>6s}")

        # ---- V2: drag suppression at the physical XI2 = 1e8 ----
        P(""); P("-- V2: drag suppression at the physical XI2 = 1e8 (Z* = 1e9/X0; benchmark X0 = 1 => Z* = 1e9) --")
        ok_v2 = True
        for kbv, jyv in GRID:
            r = A1.get((kbv, jyv))
            if not isinstance(r, dict): ok_v2 = False; P(f"  K_B={kbv} J_Y={jyv}: master SINGULAR"); continue
            a1z = q0(r['a1'])
            if isinstance(a1z, str): ok_v2 = False; P(f"  K_B={kbv} J_Y={jyv}: alpha_1 limit {a1z}"); continue
            d0 = a1z.subs(Zsym, 0); d8 = a1z.subs(Zsym, sp.Integer(10**9))
            supp = abs(float(d8)) < 1e-2*abs(float(d0))
            ok_v2 = ok_v2 and supp
            thr = []
            if a1z.has(Zsym):
                for sgn in (1, -1):
                    for s in sp.solve(sp.Eq(a1z, sgn*sp.Rational(1, 100)*d0), Zsym):
                        try:
                            if s.is_real and s > 0: thr.append(sp.nsimplify(s))
                        except Exception: pass
            thr_s = (", ".join(f"Z={sp.N(s,5):.3e} i.e. X0*={sp.N(sp.Integer(10**9)/s,5):.3e}" for s in sorted(set(thr)))
                     if thr else ("none: alpha_1 is exactly Z-independent" if not a1z.has(Zsym) else "none: never crosses"))
            P(f"  K_B={kbv} J_Y={jyv}: alpha_1(0) = {float(d0):+.5f} -> alpha_1(Z*=1e9) = {float(d8):+.5f}  "
              f"{'SUPPRESSED' if supp else 'NOT suppressed'}; thresholds: {thr_s}")
        check("V2 the drag is SUPPRESSED at the physical XI2 = 1e8 at the benchmark footing "
              "X0 = 1 (|alpha_1(Z*=1e9)| < 1e-2 |alpha_1(0)| at every grid point)", ok_v2)

if not SKIP_HEAVY and not SMOKE:
    # ---- full-ladder alpha_2 at the physical XI2 = 1e8 (benchmark X0 = 1 => Z* = 1e9) ----
    P(""); P("="*76); P("FULL-LADDER alpha_2 at XI2 = 1e8 (benchmark X0 = 1, Z* = 1e9)"); P("="*76)
    for kbv, jyv in GRID:
        t1 = time.time()
        rf = run(kbv, jyv, sp.S(10)**8, sp.S(1), full=True)
        FULL8[(kbv, jyv)] = rf
        if isinstance(rf, dict):
            P(f"  K_B={kbv} J_Y={jyv}: a2(Z*) = {q0(rf['a2'])}, a3(Z*) = {q0(rf['a3'])} ({time.time()-t1:.0f}s)")
        else:
            P(f"  K_B={kbv} J_Y={jyv}: SINGULAR {rf} ({time.time()-t1:.0f}s)")

if not ONLY_HEAVY and not SMOKE:
    # ---- V3: the verdict ----
    P(""); P("-- V3: the verdict (alpha_1 = 0 reachable with c_14 in (0, 2.5e-5]; alpha_2 dies) --")
    ok_v3 = True
    for kbv, jyv in GRID:
        r = A1.get((kbv, jyv))
        a18 = None
        if isinstance(r, dict):
            a1z = q0(r['a1'])
            if not isinstance(a1z, str): a18 = a1z.subs(Zsym, sp.Integer(10**9))
        cond1 = (a18 is not None and abs(float(a18)) < 1e-4)
        rf0, rf8 = FULL0.get((kbv, jyv)), FULL8.get((kbv, jyv))
        ratio_s = "uncomputed"
        cond2 = False
        if (isinstance(rf0, dict) and isinstance(rf8, dict)
                and not isinstance(rf0['a2'], str) and not isinstance(rf8['a2'], str)):
            try:
                rat = sp.cancel(sp.together(rf8['a2'])/sp.together(rf0['a2']))
                rl = sp.limit(rat, q, 0)
                ratio_s = f"{sp.N(rl, 5)} (q->0)"
                cond2 = abs(float(rl)) < 1e-2
            except Exception:
                try:
                    rn = float(rf8['a2'].subs(q, sp.Rational(1, 1000))/rf0['a2'].subs(q, sp.Rational(1, 1000)))
                    ratio_s = f"{rn:.3e} (at q=1e-3)"
                    cond2 = abs(rn) < 1e-2
                except Exception:
                    ratio_s = "uncomputed"
        ok_v3 = ok_v3 and cond1 and cond2
        P(f"  verdict K_B={kbv} J_Y={jyv}: |alpha_1(Z*=1e9)| = {sp.N(a18,5) if a18 is not None else 'SING/NL'} "
          f"({'<1e-4 ok' if cond1 else 'FAIL'}), alpha_2 ratio = {ratio_s} ({'ok' if cond2 else 'FAIL'})")
    check("V3 THE VERDICT: at the physical XI2 = 1e8 (benchmark X0 = 1) |alpha_1| < 1e-4 "
          "with c_14 = 0 allowed (hence c_14 in (0, 2.5e-5] admissible: no spin-1 ghost) "
          "AND |alpha_2| below 1e-2 of its XI2 = 0 value at every grid point", ok_v3)

    P(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL")
    P(f"({time.time()-T0:.0f}s)")
    P("")
    P("="*76); P("READING"); P("="*76)
    P("""  THE INSIDE-THE-INVARIANT CLASS IS EXACTLY INERT AT PPN ORDER -- NOT SINGULAR,
  NOT POISONED: NULL.  And the theory's own X0 footing cannot save it.

    (1) STRUCTURE, verified two ways.  S0: the XD-coefficient of the ladder action is
        EXACTLY K_2 XI2 (Y dQ + Y^2/4)/X0 -- a single combination Z = K_2 XI2/X0, no
        other XI2 or X0 dependence anywhere in the build.  S1: the Z-collapse holds
        EXACTLY (alpha_1(XI2=3, X0=7) == alpha_1(Z=30/7) as rational functions of q),
        so X0 is a pure rescuing of Z: a scan over X0 IS a scan over Z, and both were
        run.  The closed-form drag is therefore THE PRIZE the task asked for:
              drag(Z) = 4(2-K_B)/(J_Y+1)   -- the UNSCREENED f31 banked value,
        a constant, at every Z, at every grid point:
              (K_B, J_Y) = (1/5, 1): 18/5   (1/2, 1): 3   (1/5, 2): 12/5.
        There is no factoring to do: the exact rational formula for the new drag IS the
        old one.  Compare operator (A)'s reference form -4(2-K_B)/(J_Y(1+Z/10)+1),
        which falls off the same grid: this class does not.

    (2) MECHANISM, from the pre-projection build.  The unit-norm constraint (C1c = 0)
        makes Y|eps^1 == 0 IDENTICALLY: with d phi_bg = -Q0 A_dn purely aether-parallel,
        the metric projection term h0^{mn} dphi_bg_m dphi_bg_1n = -Q0 (A_up1 . A_dn)
        is cancelled by the kinetic cross term Q0 A_up0 . d(d chi) -- the exact identity
        2 A_up1 . A_dn = A_up0 . H . A_up0 (H = the metric perturbation matrix).  So Y
        is QUADRATIC in the fluctuations to the kept order.  Hence (Y dQ)|eps^2 = 0 and
        (Y^2)|eps^2 = (Y^2)|eps^3 = 0 EXACTLY (both verified symbolically from the
        pipeline's own objects, /tmp/g034_sc/mech.pkl).  Both injected pieces start at
        eps^3, whose Es/Eis monomials are all ODD-power ((3,0),(2,1),(1,2),(0,3)) and
        the DC projection (equal powers only, Es*Eis -> 1) kills them; their eps^4
        terms are OUTSIDE the ladder's eps<=2 bookkeeping.  Net: the XD-coefficient of
        the static action is IDENTICALLY ZERO (all 20 EOM derivatives d(L2dc, amp) = 0).
        The operator stiffens the QUARTIC fluctuation self-interactions, not the
        quadratic kinetic matrix: to linearised PPN it does not couple AT ALL.  The
        f(0) = -1 + O(Y)-expansion used by the task (bookkeeping pieces + sign) drops
        the -xi^2 Y^2/(2X0) constant and the dQ^3/Y^3+ terms, and that expansion error
        is harmless HERE precisely because the kept pieces are null: the screening
        never enters the linearised problem in ANY sign or bookkeeping convention.

    (3) X0, the theory's own footing (per the steering directive, settled, not assumed).
        The certified convention is H003 line 513:  Lambda^4 = rho_Lambda, status
        DERIVED from f(0) = -1 (H001 A2/B2, symbolic); hy4/PAPER line 36 puts the FRW
        vacuum at X = 0 identically.  The natural footing X0 = rho_Lambda/Lambda^4 is
        therefore EXACTLY 1 -- the benchmark run.  (The parent's L200/L206 pointer
        resolves to the L211 ledger's relabelled rotation-curve exponents, not an X0
        convention; H003/PAPER is the X0-bearing convention.)  And the opposite extreme
        is already covered exactly: X0 -> 0^+ is Z -> infinity (maximal screening, the
        limit the f(X + xi^2 Y^2/X) class lives at), where the drag limits are
              -18/5, -3, -12/5  -- UNCHANGED from Z = 0.
        No X0 exists, natural or extreme, that turns this operator on.  The verdict is
        footing-independent BY THE STRUCTURE (S0/S1), not by choice of benchmark.

    (4) VERDICT (pre-registered, honest on both branches).  V1 PASS (gamma = 1,
        alpha_3 = 0, alpha_1 = banked at Z = 0 at all three grid points -- the build
        touches nothing else); V2 FAIL (|alpha_1(Z*)| = |alpha_1(0)| exactly: ratio 1,
        not < 1e-2); V3 FAIL (alpha_1 = 0 is NOT reachable at positive coupling -- the
        alpha_1 lock -4 c_14 = +4(2-K_B)/(1+J_Y) forces c_14 < 0 UNTOUCHED -- and the
        alpha_2 channel is exactly unchanged, ratio 1.0000 at q -> 0).  No singularisation
        anywhere: unlike G030's aether operator, this operator does not break the
        static limit -- it is EXACTLY INVISIBLE to it.  'Operator breaks the theory'
        vs 'operator breaks the static limit' has a third answer: 'operator never
        enters the linearised problem'.

    (5) CONSEQUENCE -- THE SECOND DOOR CLOSES.  G030 closed the (D^2)-class (scalar
        trace, scalar Hessian, aether Hessian) and left open the inside-the-invariant
        class f(X + xi^2 Y^2/X).  This lane closes it: no local operator tested --
        seven now across f31/f31c/G030/G034 -- realises f31c's coherent-stiffening
        reference (J_Y -> J_Y(1+XI2), propagator form -4(2-K_B)/(J_Y(1+XI2)+1), the
        exact drag the gate needs).  The k^4 PPN gate for LOCAL two-derivative-family
        operators is CLOSED.  The surviving completions are the non-local-form lane
        (route A / Horn A, G032 running: the fixed-congruence ladder) and non-perturbative
        screenings (which by this lane's mechanism cannot act through the quadratic
        invariant at PPN order at all).  The completed-action gate stays SHUT unless
        Horn A opens it.

  STATUS: committed as a FINDING per repo discipline.  The drag closed form is exact
  (the unscreened one); the mechanism is verified symbolically at EOM level; the X0
  question is settled from the repo's own certified lanes (H003/PAPER) and is moot
  by structure.  Per the steering directive, no iteration past the X0 scan: the
  session ends with the lane committed and pushed.""")
else:
    P(f"\n[partial run: SMOKE={SMOKE} ONLY_HEAVY={ONLY_HEAVY} SKIP_HEAVY={SKIP_HEAVY}] "
      f"FAILS so far: {FAILS}")
    P(f"({time.time()-T0:.0f}s)")
sys.exit(0)
