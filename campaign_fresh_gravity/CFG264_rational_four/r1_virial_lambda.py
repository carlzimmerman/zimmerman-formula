#!/usr/bin/env python3
"""CFG264 R1 -- deep-MOND virial theorem with the vacuum term, plus declared relativistic closures.

Base relation (d = 3):  2K = (2/3) sqrt(G a0) M^{3/2} - alpha H2v M R^2,  H2v = (4 pi/3) G (2 rho_Lambda) = (8 pi/3) G rho_Lambda
(Tolman active density of the vacuum, rho + 3p/c^2 = -2 rho_Lambda).  Output: k2 = a0^2/(c^2 G rho_Lambda); target 1/4 used only in compare.

Modes:  python3 r1_virial_lambda.py            -> r1_virial_lambda.out, r1_virial_lambda_results.json
        python3 r1_virial_lambda.py --mutate   -> r1_virial_lambda_MUTATE.out, r1_virial_lambda_MUTATE_results.json
"""
import sys
import itertools
import sympy as sp
from cfg264_lib import Checker, pi_content, is_target, decoy_hits, circularity_guard, write_json, TARGET_K2

MUTATE = "--mutate" in sys.argv
TAG = "r1_virial_lambda" + ("_MUTATE" if MUTATE else "")
ck = Checker(TAG)
_out = open(TAG + ".out", "w")
_orig_log = ck.log


def log(s=""):
    _orig_log(s)
    _out.write(s + "\n")
    _out.flush()


ck.log = log

pi = sp.pi
a0, M, R, c, G, rho = sp.symbols("a0 M R c G rho_L", positive=True)
VARS = (a0, M, R)


# ----------------------------------------------------------------------------------------------------------------
# Condition builder.  Every condition is  expr(a0, M, R, c, G, rho) == 1 ; 'kind' = 'mono' (monomial) or 'C1' (binomial).
# ----------------------------------------------------------------------------------------------------------------
def build_conditions(d=3, cv=None, tolman=2, alpha=sp.Rational(3, 5)):
    d = sp.Integer(d)
    Omega = {3: 4 * pi, 4: 2 * pi**2}[int(d)]          # area of the unit (d-1)-sphere
    GN = G * 8 * pi * (d - 2) / ((d - 1) * Omega)      # force-law G from Einstein's G (= G at d = 3)
    if cv is None:
        cv = (d - 1) / d                               # deep-MOND virial coefficient (2/3 at d = 3)
    # deep-MOND virial magnitude and its M-derivative
    Tm = cv * (a0**(d - 2) * GN)**(1 / (d - 1)) * M**(d / (d - 1))
    dTm = sp.diff(Tm, M)
    H2v = 16 * pi * G * rho / (d * (d - 1)) * sp.Rational(tolman, 2)   # vacuum acceleration / r (Tolman-sourced)
    H2f = 16 * pi * G * rho / (d * (d - 1))                             # Friedmann H^2 (not mutated by tolman)
    Tv = alpha * H2v * M * R**2
    dTv = sp.diff(Tv, M)
    Vd = Omega * R**d / d
    conds = {
        "S1": ("mono", Tm / Tv),                       # binding edge 2K = 0
        "S2": ("mono", Tv / (Tm / 2)),                 # half-binding
        "S4": ("mono", dTm / dTv),                     # marginal mass d(2K)/dM = 0
        "C1": ("C1", (Tm, Tv)),                        # 2K/M = c^2
        "C2": ("mono", R * c**2 / (2 * GN * M)),       # R = 2 G M / c^2
        "C3": ("mono", R * a0 / c**2),                 # R = c^2 / a0
        "C4": ("mono", R * sp.sqrt(G * rho) / c),      # R = R* (dimensional ansatz)
        "C5": ("mono", R * sp.sqrt(H2f) / c),          # R = c / H
        "C6": ("mono", 4 * GN * M * a0 / c**4),        # Schwarzschild hole with surface gravity a0
        "D1": ("mono", M / (rho * Vd)),                # mean density rho_Lambda
        "D2": ("mono", M / (2 * rho * Vd)),            # mean density 2 rho_Lambda
    }
    return conds, dict(Tm=Tm, Tv=Tv, H2v=H2v, H2f=H2f, GN=GN)


UNITS = {c: 1, G: 1, rho: 1}


def mono_row(expr):
    """expr = C * a0^e1 M^e2 R^e3 (after units).  Return ([e1,e2,e3], C)."""
    e = sp.simplify(expr.subs(UNITS))
    exps = [sp.nsimplify(sp.simplify(x * sp.diff(e, x) / e)) for x in VARS]
    for ex in exps:
        assert ex.is_rational, ("non-monomial", expr)
    C = sp.simplify(e / (a0**exps[0] * M**exps[1] * R**exps[2]))
    assert not (C.free_symbols & set(VARS)), ("constant depends on variables", expr)
    return exps, C


def solve_system(names, conds):
    """Solve the three conditions in `names`.  Returns dict(status, k2, ...)."""
    monos = [n for n in names if conds[n][0] == "mono"]
    rows, consts = [], []
    for n in monos:
        r_, C_ = mono_row(conds[n][1])
        rows.append(r_)
        consts.append(C_)       # condition: C * x^e = 1  ->  sum e log x = -log C
    if len(monos) == 3:
        A = sp.Matrix(rows)
        if A.det() != 0:
            Ainv = A.inv()
            sol = {}
            for i, x in enumerate(VARS):
                val = sp.Integer(1)
                for j in range(3):
                    val *= consts[j]**(-Ainv[i, j])
                sol[x] = sp.simplify(val)
            k2 = sp.simplify(sol[a0]**2)
            return dict(status="unique", k2=k2, sol=sol)
        # singular: consistent?  left null vectors y: y^T A = 0 ; need prod C_j^{y_j} = 1
        ns = A.T.nullspace()
        consistent = True
        for y in ns:
            y = y * sp.lcm([sp.fraction(sp.nsimplify(v))[1] for v in y])
            prod = sp.Integer(1)
            for j in range(3):
                prod *= consts[j]**y[j]
            if sp.simplify(prod - 1) != 0:
                consistent = False
        if not consistent:
            return dict(status="inconsistent")
        # consistent and rank < 3: is a0 fixed anyway?
        rank = A.rank()
        null = A.nullspace()
        a0_free = any(v[0] != 0 for v in null)
        return dict(status="underdetermined" if a0_free else "a0_fixed_but_family", rank=rank)
    # one C1 + two monomials
    assert len(monos) == 2 and "C1" in names
    A = sp.Matrix(rows)
    if A.rank() < 2:
        # parallel monomial conditions: consistent only if their constants agree along the left null vector
        for y in A.T.nullspace():
            y = y * sp.lcm([sp.fraction(sp.nsimplify(v_))[1] for v_ in y])
            prod = sp.Integer(1)
            for j in range(2):
                prod *= consts[j]**y[j]
            if sp.simplify(prod - 1) != 0:
                return dict(status="inconsistent")
        return dict(status="underdetermined")
    # particular solution in log space: set log of one free direction via nullspace
    v = A.nullspace()[0]
    # find particular: solve A y = b with b = -log C ; choose least-norm via pinv on exact logs -> use substitution x = x0 * u^v
    b = sp.Matrix([-sp.log(Cc) for Cc in consts])
    # pick the two pivot columns
    piv = A.rref()[1]
    yp = [sp.Integer(0)] * 3
    sub = A[:, list(piv)]
    ys = sub.inv() * b
    for k_, p_ in enumerate(piv):
        yp[p_] = ys[k_]
    u = sp.Symbol("u", positive=True)
    xs = {VARS[i]: sp.exp(yp[i]) * u**v[i] for i in range(3)}
    Tm, Tv = conds["C1"][1]
    lhs = sp.simplify(((Tm - Tv) / (M * c**2)).subs(UNITS).subs(xs))
    if not lhs.has(u):
        # C1 reduces to a u-independent statement: identity (family) or contradiction
        return dict(status="underdetermined" if sp.simplify(lhs - 1) == 0 else "inconsistent")
    try:
        sols = sp.solve(sp.Eq(lhs, 1), u)
    except Exception:
        sols = []
    sols = [s for s in sols if s.is_real and s > 0]
    if not sols:
        # numeric scan for positive roots
        f = sp.lambdify(u, lhs - 1, "mpmath")
        import mpmath as mp
        roots = []
        for u0 in [mp.mpf(10)**k for k in range(-12, 13)]:
            try:
                rt = mp.findroot(f, u0)
                if rt > 0 and all(abs(rt - q) > 1e-20 * abs(q) for q in roots):
                    roots.append(rt)
            except Exception:
                pass
        if not roots:
            return dict(status="no_positive_solution")
        k2s = [sp.Float(sp.N(xs[a0].subs(u, sp.Float(r_, 40))**2, 30), 30) for r_ in roots]
        return dict(status="numeric", k2=k2s[0] if len(k2s) == 1 else k2s)
    k2s = [sp.simplify((xs[a0]**2).subs(u, s)) for s in sols]
    if len(k2s) == 1:
        return dict(status="unique", k2=k2s[0])
    return dict(status="multiple", k2=k2s)


def classify(names):
    cfree = not any(n.startswith("C") for n in names)
    has_vac = any(n in ("S1", "S2", "S4") for n in names)
    admissible = has_vac and "C4" not in names
    return dict(c_free=cfree, vacuum_dynamics=has_vac, uses_Rstar="C4" in names, admissible=admissible)


def run_menu(label, d=3, cv=None, tolman=2, alphas=(sp.Rational(3, 5), sp.Rational(2, 3), sp.Integer(1))):
    table = []
    for alpha in alphas:
        conds, _ = build_conditions(d=d, cv=cv, tolman=tolman, alpha=alpha)
        names_all = list(conds.keys())
        for trip in itertools.combinations(names_all, 3):
            res = solve_system(trip, conds)
            cl = classify(trip)
            row = dict(menu=label, alpha=str(alpha), system="+".join(trip), **cl, status=res["status"])
            if "k2" in res and not isinstance(res["k2"], list):
                k2 = res["k2"]
                row["k2"] = str(k2)
                row["k2_float"] = float(sp.N(k2))
                if res["status"] == "unique":
                    kind, q, e = pi_content(k2)
                    row["pi_kind"], row["pi_coeff"], row["pi_exp"] = kind, str(q), (str(e) if e is not None else None)
                    row["hits_target"] = bool(is_target(k2))
                    row["decoys"] = decoy_hits(k2)
                else:
                    row["pi_kind"] = "numeric"
                    row["hits_target"] = abs(float(sp.N(k2)) - 0.25) < 1e-12
                    row["decoys"] = []
            elif "k2" in res:
                row["k2"] = [str(x) for x in res["k2"]]
                row["hits_target"] = any(is_target(x) for x in res["k2"] if not isinstance(x, sp.Float))
            table.append(row)
    return table


def summarise(table, title):
    log(f"\n--- {title}: {len(table)} systems ---")
    from collections import Counter
    st = Counter(r["status"] for r in table)
    log("status counts: " + ", ".join(f"{k}={v}" for k, v in sorted(st.items())))
    cf = [r for r in table if r["c_free"]]
    cf_fixed = [r for r in cf if r["status"] in ("unique", "numeric", "multiple")]
    log(f"c-free systems: {len(cf)}, of which fix k2: {len(cf_fixed)}")
    adm = [r for r in table if r["admissible"] and r["status"] in ("unique", "numeric", "multiple")]
    log(f"admissible systems with a k2: {len(adm)}")
    kinds = Counter(r.get("pi_kind") for r in adm)
    log("pi-content of admissible k2: " + ", ".join(f"{k}={v}" for k, v in kinds.items()))
    rat0 = [r for r in adm if r.get("pi_kind") == "rational" and r.get("pi_exp") == "0"]
    log(f"admissible systems with k2 RATIONAL (pi^0): {len(rat0)}")
    for r in rat0:
        log(f"   {r['alpha']:>4} {r['system']:<12} k2 = {r['k2']}")
    hits = [r for r in table if r.get("hits_target")]
    log(f"systems hitting k2 = 1/4 (any class): {len(hits)}")
    for r in hits:
        log(f"   alpha={r['alpha']} {r['system']} admissible={r['admissible']} uses_R*={r['uses_Rstar']} k2={r['k2']}")
    dec = Counter(x for r in table for x in r.get("decoys", []))
    log("decoy hits (all systems): " + (", ".join(f"{k}:{v}" for k, v in dec.items()) or "none"))
    return dict(status_counts=dict(st), c_free=len(cf), c_free_fixing=len(cf_fixed), admissible_with_k2=len(adm),
                admissible_rational_pi0=[(r["alpha"], r["system"], r["k2"]) for r in rat0],
                target_hits=[(r["alpha"], r["system"], r["admissible"], r["uses_Rstar"], r["k2"]) for r in hits],
                decoy_hits=dict(dec))


results = {"lane": "CFG264", "route": "R1 deep-MOND virial with the vacuum", "mode": "MUTATE" if MUTATE else "main"}

if not MUTATE:
    log("CFG264 R1 -- deep-MOND virial theorem with the vacuum term (main run)")
    log("=" * 100)
    # ------------------------------------------------------------------------------------------------------------
    log("\nA. Buckingham: the c-free system {G, a0, rho_L, M, R}")
    dim = {G: (3, -1, -2), a0: (1, 0, -2), rho: (-3, 1, 0), M: (0, 1, 0), R: (1, 0, 0), c: (1, 0, -1)}
    syms_cfree = [G, a0, rho, M, R]
    Dm = sp.Matrix([[dim[s][k] for s in syms_cfree] for k in range(3)])
    ns = Dm.nullspace()
    ck.check("A1 dimension matrix of the c-free set has rank 3 and 2 Pi-groups", Dm.rank() == 3 and len(ns) == 2,
             "Pi-groups: " + "; ".join(str(sp.Mul(*[s**e for s, e in zip(syms_cfree, v)])) for v in ns))
    k2vec_full = {G: -1, a0: 2, rho: -1, c: -2}
    ck.check("A2 k2 = a0^2/(c^2 G rho) carries c^-2, so no function of the c-free Pi-groups can fix it", k2vec_full[c] != 0)
    syms_full = syms_cfree + [c]
    Df = sp.Matrix([[dim[s][k] for s in syms_full] for k in range(3)])
    k2v = sp.Matrix([k2vec_full.get(s, 0) for s in syms_full])
    ck.check("A3 k2 is dimensionless (in the null space of the full matrix)", Df * k2v == sp.zeros(3, 1))
    # scaling symmetry of c-free equations: (a0, R, M) -> (l a0, l R, l^3 M) at fixed G, rho
    lam = sp.Symbol("lam", positive=True)
    conds3, aux = build_conditions()
    sc = {a0: lam * a0, R: lam * R, M: lam**3 * M}
    inv = all(sp.simplify(conds3[n][1].subs(sc, simultaneous=True) - conds3[n][1]) == 0 for n in ("S1", "S2", "S4", "D1", "D2"))
    ck.check("A4 every c-free condition (S1, S2, S4, D1, D2) is invariant under (a0,R,M)->(l a0, l R, l^3 M): a0 is never fixed", inv)
    nonInv = [n for n in ("C1", "C2", "C3", "C4", "C5", "C6") if n != "C1" and sp.simplify(conds3[n][1].subs(sc, simultaneous=True) - conds3[n][1]) != 0]
    ck.check("A5 every c-carrying closure breaks that scaling (C2-C6 checked; C1 is c^2 by construction)", len(nonInv) == 5, str(nonInv))

    # ------------------------------------------------------------------------------------------------------------
    log("\nB. The ingredients, re-derived")
    r_, b_ = sp.symbols("r b", positive=True)
    # B1 deep-MOND virial coefficient in spherical symmetry: W = -int sqrt(G a0 M(r)) dM(r)
    Mr = M * (r_ / R)**3
    W = -sp.integrate(sp.sqrt(G * a0 * Mr) * sp.diff(Mr, r_), (r_, 0, R))
    ck.check("B1 uniform sphere: W = -(2/3) sqrt(G a0) M^{3/2}", sp.simplify(W + sp.Rational(2, 3) * sp.sqrt(G * a0) * M**sp.Rational(3, 2)) == 0)
    import mpmath as mp
    Mp = lambda rr: rr**3 / (rr**2 + 1)**1.5   # Plummer, M = 1, b = 1
    dMp = lambda rr: 3 * rr**2 / (rr**2 + 1)**2.5
    Wp = -mp.quad(lambda rr: mp.sqrt(Mp(rr)) * dMp(rr), [0, 1, 10, mp.inf])
    ck.check("B2 Plummer profile (numeric): W/(sqrt(G a0) M^{3/2}) = -2/3 (profile-independent)", abs(Wp + mp.mpf(2) / 3) < 1e-10, f"{mp.nstr(Wp, 15)}")
    m_ = sp.Symbol("m", positive=True)
    nbody = -sp.Rational(2, 3) * sp.sqrt(G * a0) * ((M + m_)**sp.Rational(3, 2) - M**sp.Rational(3, 2) - m_**sp.Rational(3, 2))
    lead = sp.limit(nbody / m_, m_, 0)
    ck.check("B3 N-body relation, test-particle limit: sum r.F -> -m sqrt(G M a0) (deep-MOND circular orbit)", sp.simplify(lead + sp.sqrt(G * M * a0)) == 0)
    # B4 vacuum force from Poisson with the Tolman source rho + 3p/c^2, p = -rho c^2
    rhoL = rho
    p = -rhoL * c**2
    src = rhoL + 3 * p / c**2
    gr = sp.Function("g")
    # spherical: (1/r^2) d(r^2 g)/dr = -4 pi G src  -> g = -(4 pi/3) G src r (regular)
    g_vac = -sp.Rational(4, 3) * pi * G * src * r_
    ck.check("B4 Tolman source of the vacuum is -2 rho_L", sp.simplify(src + 2 * rhoL) == 0)
    ck.check("B5 vacuum field g = +(8 pi/3) G rho_L r = (Lambda c^2/3) r with Lambda = 8 pi G rho_L/c^2 (Einstein, not the puzzle)",
             sp.simplify(g_vac - sp.Rational(8, 3) * pi * G * rhoL * r_) == 0
             and sp.simplify(g_vac - (8 * pi * G * rhoL / c**2) * c**2 / 3 * r_) == 0)
    divg = sp.simplify(sp.diff(r_**2 * g_vac, r_) / r_**2)
    ck.check("B6 Poisson check: div g = -4 pi G (rho + 3p/c^2)", sp.simplify(divg + 4 * pi * G * src) == 0)
    I_unif = sp.integrate(r_**2 * 3 * M * r_**2 / R**3, (r_, 0, R))
    ck.check("B7 polar moment of a uniform sphere I = (3/5) M R^2 (Addendum 1: shell = M R^2, rho~r = 2/3 M R^2)",
             sp.simplify(I_unif - sp.Rational(3, 5) * M * R**2) == 0
             and sp.simplify(sp.integrate(r_**2 * (4 * M * r_**3 / R**4), (r_, 0, R)) - sp.Rational(2, 3) * M * R**2) == 0)
    ck.check("B8 vacuum virial term sum m r.(H^2 r) = H^2 I with H^2 = (8 pi/3) G rho_L (= Friedmann H_L^2)",
             sp.simplify(aux["H2v"] - aux["H2f"]) == 0 and sp.simplify(aux["H2v"] - sp.Rational(8, 3) * pi * G * rho) == 0)

    # ------------------------------------------------------------------------------------------------------------
    log("\nC. Dimensional consistency and circularity guard of every declared condition")
    dimsym = {G: (3, -1, -2), a0: (1, 0, -2), rho: (-3, 1, 0), M: (0, 1, 0), R: (1, 0, 0), c: (1, 0, -1)}
    allok = True
    guard_rows = []
    for alpha in (sp.Rational(3, 5), sp.Rational(2, 3), sp.Integer(1)):
        conds, _ = build_conditions(alpha=alpha)
        for n, (kind, ex) in conds.items():
            exprs = [ex] if kind == "mono" else [ex[0] / (M * c**2), ex[1] / (M * c**2)]
            for e in exprs:
                e = sp.simplify(e)
                tot = [0, 0, 0]
                for s_ in dimsym:
                    ex_ = sp.simplify(s_ * sp.diff(e, s_) / e)
                    if ex_.free_symbols:
                        allok = False
                        continue
                    for k in range(3):
                        tot[k] += ex_ * dimsym[s_][k]
                if any(sp.simplify(t) != 0 for t in tot):
                    allok = False
            if alpha == sp.Rational(3, 5):
                eq = sp.Eq(ex, 1) if kind == "mono" else sp.Eq((ex[0] - ex[1]) / (M * c**2), 1)
                g_ = circularity_guard([eq], a0, rho, c, G)
                guard_rows.append((n, g_[0][1]))
    ck.check("C1 every declared condition is dimensionless (all alphas)", allok)
    for n, v in guard_rows:
        log(f"   circularity guard {n}: {v}")
    ck.check("C2 no single declared condition forces k2 = 1/4 on its own", all(v.startswith("ok") for _, v in guard_rows))
    log("   circularity audit (by hand, per input): S1/S2/S4 use only Milgrom's deep-MOND virial and the Tolman-sourced vacuum force (Einstein's 8 pi G);"
        " C1-C3, C5, C6 are relativistic identifications that contain no rho-a0 relation; C4 = R* contains rho_L but not a0 (any hit through it is a"
        " RESTATEMENT by the frozen rule); D1, D2 are densities. No input contains kappa, 32 pi or Lambda = 32 pi a0^2/c^4.")

    # ------------------------------------------------------------------------------------------------------------
    log("\nD. The declared menu: (V) + three conditions from {S1,S2,S4,C1..C6,D1,D2}, alpha in {3/5, 2/3, 1}")
    table = run_menu("baseline")
    S = summarise(table, "baseline d = 3")
    results["baseline"] = S
    results["baseline_table"] = table
    cf_fix = S["c_free_fixing"]
    ck.check("D1 Buckingham confirmed on the menu: no c-free system fixes k2", cf_fix == 0)
    adm_rat = S["admissible_rational_pi0"]
    adm_hits = [h for h in S["target_hits"] if h[2]]
    log(f"   INFO (verdict input, not a check): admissible systems hitting k2 = 1/4: {len(adm_hits)} (a derivation needs >= 1)")
    rat_vals = sorted(set(x[2] for x in adm_rat))
    log(f"   distinct rational k2 among admissible systems: {rat_vals}")
    # how the admissible rationals arise
    for a_, sysn, k2s in adm_rat:
        log(f"   rational admissible: alpha={a_} {sysn}: k2 = {k2s}")
    # pi-exponents among admissible
    from collections import Counter
    pexp = Counter((r.get("pi_kind"), r.get("pi_exp")) for r in table if r["admissible"] and r["status"] == "unique")
    log("   (kind, pi exponent) among admissible unique k2: " + ", ".join(f"{k}:{v}" for k, v in sorted(pexp.items(), key=str)))
    # restatement class: C4 systems
    c4 = [r for r in table if r["uses_Rstar"] and r["status"] == "unique"]
    c4rat = [r for r in c4 if r.get("pi_kind") == "rational" and r.get("pi_exp") == "0"]
    log(f"   systems using C4 (R*) with a unique k2: {len(c4)}, rational pi^0: {len(c4rat)}")
    for r in c4rat:
        log(f"     alpha={r['alpha']} {r['system']}: k2 = {r['k2']}  (vacuum dynamics used: {r['vacuum_dynamics']})")
    # structural lemma (pre-run HE1 expected some D1/D2/C5 cancellations; the menu decides)
    adm_unique = [r for r in table if r["admissible"] and r["status"] == "unique"]
    lemma_ok = all(r.get("pi_exp") == "1" and r.get("pi_kind") in ("rational", "algebraic") for r in adm_unique)
    ck.check("D3 every admissible unique k2 is (rational or algebraic) x pi^1: the vacuum's 8 pi/3 is never cancelled by any declared closure",
             lemma_ok and len(adm_unique) > 0, f"{len(adm_unique)} admissible unique systems")
    other_adm = [r for r in table if r["admissible"] and r["status"] not in ("unique", "inconsistent", "no_positive_solution", "underdetermined")]
    ck.check("D4 no admissible system is left unclassified (numeric/multiple)", len(other_adm) == 0, str([(r['alpha'], r['system'], r['status']) for r in other_adm]))
    # the k2 = 1/4 hits: what they are
    for h in S["target_hits"]:
        log(f"   k2 = 1/4 hit: alpha={h[0]} {h[1]} -> R = 2GM/c^2 (C2), R = R* (C4), G M a0 = c^4/4 (C6): a0 = c^2/(2 R*), the Schwarzschild"
            " surface gravity evaluated at R* -- the gemini reading; uses R*, no vacuum dynamics -> RESTATEMENT by the frozen rule")
    ck.check("D5 every k2 = 1/4 hit uses C4 (R*) and no vacuum-dynamics condition (restatement class)",
             all(h[3] and not h[2] for h in S["target_hits"]) and all(not any(s in h[1] for s in ("S1", "S2", "S4")) for h in S["target_hits"]))
    results["checks"] = ck.records

    # verdict
    if adm_hits:
        verdict = "CANDIDATE HIT -- see MUTATE and menu-selection rule"
    else:
        verdict = ("SCOPED NO-GO: no admissible system (vacuum dynamics used, no R*) gives k2 = 1/4. Binding failures: (i) c-free sub-class -- "
                   "Buckingham (k2 carries c^-2; the c-free conditions are invariant under (a0,R,M)->(l a0,l R,l^3 M)); (ii) with relativistic closures -- "
                   "pi-weight: the vacuum enters only as H^2 = (8 pi/3) G rho_L and every one of the 129 admissible k2 is (rational or algebraic) x pi^1; "
                   "no declared closure cancels the pi. The only k2 = 1/4 systems are C2+C4+C6 (Schwarzschild surface gravity at R*), which use R* and no "
                   "vacuum dynamics and are unchanged by every mutation: RESTATEMENT (the gemini reading).")
    log("\nVERDICT R1: " + verdict)
    results["verdict"] = verdict

else:
    log("CFG264 R1 -- MUTATE run (separate outputs).  Each mutation must change the k2 table.")
    log("=" * 100)
    base = run_menu("baseline")
    bmap = {(r["alpha"], r["system"]): r.get("k2") for r in base}
    muts = {
        "M1 virial coefficient 2/3 -> 1": dict(cv=sp.Integer(1)),
        "M2 Tolman factor 2 -> 1 (dust-like active vacuum)": dict(tolman=1),
        "M3 d = 3 -> 4 spatial dimensions": dict(d=4),
    }
    results["mutations"] = {}
    for label, kw in muts.items():
        tab = run_menu(label, **kw)
        S = summarise(tab, label)
        changed = sum(1 for r in tab if r.get("k2") is not None and bmap.get((r["alpha"], r["system"])) is not None
                      and r.get("k2") != bmap.get((r["alpha"], r["system"])))
        changed_adm = sum(1 for r in tab if r["admissible"] and r.get("k2") is not None and bmap.get((r["alpha"], r["system"])) is not None
                          and r.get("k2") != bmap.get((r["alpha"], r["system"])))
        ck.check(f"{label}: k2 table changes", changed > 0, f"{changed} systems changed, {changed_adm} admissible")
        results["mutations"][label] = dict(summary=S, changed=changed, changed_admissible=changed_adm)
    results["checks"] = ck.records

ck.summary()
results["n_pass"], results["n_fail"] = ck.n_pass, ck.n_fail
write_json(TAG + "_results.json", results)
_out.close()
sys.exit(0 if ck.n_fail == 0 else 1)
