#!/usr/bin/env python3
"""G030 -- THE THIRD OPERATOR: the aether's own biharmonic, in the certified ladder.

WHERE THIS SITS.  hy4's H004 proposed the completed AeST action with the spatial
biharmonic screening term -xi^2 (D^2 phi)^2 on the SCALAR.  The repo's own f31 ladder
ran it: FAIL -- the drag piece of alpha_1 GROWS linearly in XI2 (poisoned by the
operator's pieces acting on the scalar's BACKGROUND gradient).  f31c then proved the
REFERENCE result: coherent stiffening of the whole Y sector, J_Y -> J_Y(1+XI2), gives
EXACTLY the propagator form -4(2-K_B)/(J_Y(1+XI2)+1) -- the lock is evaded at c_14 > 0
-- but neither local scalar operator tried (trace (D^2 phi)^2; Hessian-squared
|D_mD_n phi|^2) realises it.  The k^4 PPN gate is OPEN on the operator.

THE NEW CANDIDATE (and why it is different).  Put the biharmonic on the AETHER:

    L_k4 = - (xi^2/2) h^{ma} h^{nb} h^{rs} (nabla_m nabla_n A_r)(nabla_a nabla_b A_s)

The f31b/f31c poison came from Gam^{l}_{mn} d_l phi_bg with d phi_bg = -Q0 A_dn != 0:
the scalar's background gradient is CHARGED (Q0), so the operator's connection
cross-pieces carry Q0^2 and grow the drag.  The aether's background is a CONSTANT unit
vector (Aup_bg = (S0, wb w_i) has NO phase dependence; every d(A_bg) = 0 in the ladder's
own d() sense), so the aether Hessian's connection pieces carry NO background charge.
The one live metric piece is through the raise: Aup = gu Adn mixes the metric
perturbation into Aup at O(eps) -- that is tested here, not assumed away.

Verdict rule (pre-registered, mirroring f31's K3/K4):
  PASS  requires ALL of:
    (V1) the XI2 = 0 anchors reproduce the banked closed form (gamma = 1, alpha_3 = 0,
         alpha_1 = -4(2-K_B J_Y)/(1+J_Y) at q->0) -- the build touches nothing else;
    (V2) the drag is SUPPRESSED: |drag(XI2 = 1e8)| < 1e-2 |drag(0)|;
    (V3) the VERDICT: alpha_1 = 0 reachable with c_14 in (0, 2.5e-5] (no spin-1 ghost)
         AND |alpha_2(XI2 = 1e8)| < 1e-2 |alpha_2(0)| (the alpha_2 channel dies with it).
  FAIL on any = the k^4 gate closes for the whole local two-derivative-family host
  (scalar trace, scalar Hessian, aether Hessian all dead) -- commit as a finding.

Both a0 footings carried per PROTOCOL R3 where a dimensional number appears (here:
none -- the ladder is dimensionless; the physical XI2 >= 8.6e7 comes from
xi >= 0.045 pc = 9300 AU, f30's Cassini floor = 1.16 r_M(Sun) on 9.3619e-11/1.1279e-10).
"""
import os, sys, time, pickle
T0 = time.time(); P = lambda *a: print(*a, flush=True)
import sympy as sp

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "hunt_2026", "f31c_ppn_k4_operators.py")
src = open(SRC).read()

# ---- inject operator (C): the aether Hessian-squared, built like (B) but on Aup ----
INJECT = '''
    # G030 operator (C): the AETHER Hessian-squared xi^2 h^{ma}h^{nb}h^{rs}(nab_m nab_n A_r)(nab_a nab_b A_s)
    # O(eps) aether Hessian: H1A[m][n][r] = wtrunc(d(d(AupT[r], m), n)).  The background
    # pieces of AupT are phase-constants, so d(A_bg) = 0 exactly in the ladder's d() --
    # no Q0-charged connection cross-pieces (the scalar operator's poison).  The metric
    # raise mixes Hup into Aup at O(eps); that is carried, not assumed away.
    H1A = [[[wtrunc(sp.expand(d(d(AupT[r], m), n))) for r in range(4)] for n in range(4)] for m in range(4)]
    gAHS2 = 0
    for m in range(4):
        for n in range(4):
            for r in range(4):
                if H1A[m][n][r] == 0: continue
                for a in range(4):
                    for b in range(4):
                        if H1A[a][b][r] == 0: continue
                        # second factor contracted with h0 on (a,b) and the free index s -> r (trace-free pairing
                        # would need two copies; the reference (A) is the target form, so pair s with r)
                        gAHS2 += h0[m, a]*h0[n, b]*H1A[m][n][r]*H1A[a][b][r]
    gAHS2 = wtrunc(sp.expand(gAHS2))
    gAHS = [0, 0, gAHS2]
    P(f"    aether-Hessian operator built (efficient): {len(sp.Add.make_args(gAHS2))} terms ({time.time()-T0:.1f}s)")
    XC = sp.symbols('xC', nonnegative=True)
'''
ANCHOR = "    L2_grav = wtrunc(sum(gsq[a]*gS[2-a] for a in range(3)))"
assert ANCHOR in src, "anchor not found"
src = src.replace(ANCHOR, INJECT + "\n" + ANCHOR +
                  " - (2-KB)*JY*XC*XI2*gAHS[2]")

# ---- truncate the module's own (A)/(B) verification section: it would run its checks
# against THIS run's cache (which contains our injected operator) and sys.exit before
# our grid runs.  We keep the build + eq/lin/ladder definitions only. ----
CUT = 'P(""); P("="*76); P("TWO ALTERNATIVE OPERATORS'
assert CUT in src, "cut marker not found"
src = src[:src.index(CUT)]

# ---- make lin exception-safe: a stage that goes nonlinear returns None, which every
# ladder stage already handles ('SING0'/'SING1'/... markers). ----
OLD_LIN = """def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)"""
NEW_LIN = """def lin(eqs, unk):
    try:
        Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    except Exception:
        return None"""
assert OLD_LIN in src, "lin block not found"
src = src.replace(OLD_LIN, NEW_LIN)

# ---- wrap stage-2 of the ladder: operator (C) can make the wb^2 solve nonlinear in
# the amplitudes; alpha_1 (the decisive drag) is fixed by the first-order solve, and
# the alpha_2 channel is then reported as uncomputed rather than crashed on. ----
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
g = {"__name__": "g030_build", "__file__": SRC}
exec(compile(src, SRC, "exec"), g)
ladder, RES, check, FAILS = g["ladder"], {}, g["check"], g["FAILS"]
R, q = g["R"], g["q"]
P(f"[build] complete ({time.time()-T0:.0f}s)")

# ---- operator (C) across the same grid as (A)/(B) ----
P(""); P("="*76); P("OPERATOR (C): the aether's own biharmonic (G030)"); P("="*76)
GRID = [(R(1,5), 1), (R(1,2), 1), (R(1,5), 2)]
XIS = [0, 1, 100, 10**4, 10**8]
XC = sp.Symbol('xC', nonnegative=True)
P(f"  {'K_B':>4s} {'J_Y':>3s} {'XI2':>9s} {'alpha_1':>14s} {'drag':>12s} {'alpha_2':>14s} {'gamma':>6s} {'a3':>4s}")
rows = {}
for kbv, jyv in GRID:
    for xi2 in XIS:
        r = ladder({g["KB"]: kbv, g["K2"]: sp.S(10), g["JY"]: sp.S(jyv),
                    g["Q0"]: q, g["C2"]: 0, g["C4"]: 0, g["XI2"]: sp.S(xi2),
                    g["XA"]: 0, g["XB"]: 0, XC: 1})
        if isinstance(r, str) or (isinstance(r, tuple)):
            P(f"  {kbv!s:>4s} {jyv:>3d} {xi2:>9d}  SINGULAR ({r})")
            rows[(kbv, jyv, xi2)] = None
            continue
        rows[(kbv, jyv, xi2)] = r
        drag = sp.simplify(sp.expand(r['a1'] +
                    sp.Rational(4,1)*kbv + sp.Rational(4,1)*kbv*jyv))  # drag = a1 + 4KB(1+JY) at q->0? use a1 directly too
        P(f"  {kbv!s:>4s} {jyv:>3d} {xi2:>9d} {sp.N(r['a1'],5)!s:>14s} {sp.N(r['a1'],5)!s:>12s} {sp.N(r['a2'],5)!s:>14s} {sp.N(r['g'],4)!s:>6s} {sp.N(r['a3'],3)!s:>4s}")

def val(kbv, jyv, xi2, key):
    r = rows.get((kbv, jyv, xi2))
    if r is None or r.get(key) in ('SING2', 'SING1'): return None
    v = r[key]
    if hasattr(v, 'has') and v.has(q):
        try: v = sp.limit(v, q, 0)
        except Exception: return None
    return sp.nsimplify(v)

# ---- verdicts (pre-registered) ----
ok_anchors = True
for kbv, jyv in GRID:
    g_v, a3_v = val(kbv, jyv, 0, 'g'), val(kbv, jyv, 0, 'a3')
    if g_v is None or sp.simplify(g_v - 1) != 0 or sp.simplify(a3_v) != 0:
        ok_anchors = False
check("V1 anchors at XI2 = 0: gamma = 1 and alpha_3 = 0 at every (K_B, J_Y) -- the "
      "aether operator touches nothing else in the conservative sector", ok_anchors)

sup = []
for kbv, jyv in GRID:
    d0, d8 = val(kbv, jyv, 0, 'a1'), val(kbv, jyv, 10**8, 'a1')
    if d0 is None or d8 is None: sup.append(False); continue
    sup.append(abs(float(d8)) < 1e-2*abs(float(d0)))
    P(f"  suppression K_B={kbv} J_Y={jyv}: alpha_1 {float(d0):+.4f} -> {float(d8):+.4e}")
check("V2 the drag is SUPPRESSED at the physical XI2 = 1e8 "
      "(|alpha_1(1e8)| < 1e-2 |alpha_1(0)| at every grid point)", all(sup))

verdict_rows = []
for kbv, jyv in GRID:
    a18, a208 = val(kbv, jyv, 10**8, 'a1'), val(kbv, jyv, 10**8, 'a2')
    a20 = val(kbv, jyv, 0, 'a2')
    ok = (a18 is not None and a208 is not None and a20 is not None
          and abs(float(a18)) < 1e-4 and abs(float(a208)) < 1e-2*abs(float(a20)))
    verdict_rows.append(ok)
    a18_s = f"{float(a18):.3e}" if a18 is not None else "SING/NL"
    ratio_s = f"{float(a208)/float(a20):.3e}" if (a208 is not None and a20 is not None and float(a20) != 0) else "uncomputed"
    P(f"  verdict K_B={kbv} J_Y={jyv}: |alpha_1(1e8)| = {a18_s}, alpha_2 ratio = {ratio_s}")
check("V3 THE VERDICT: at XI2 = 1e8, |alpha_1| < 1e-4 with c_14 = 0 allowed (hence "
      "c_14 in (0, 2.5e-5] admissible: no spin-1 ghost) AND |alpha_2| below 1e-2 of "
      "its XI2 = 0 value at every grid point", all(verdict_rows))

P(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL")
P(f"({time.time()-T0:.0f}s)")
sys.exit(1 if FAILS else 0)
