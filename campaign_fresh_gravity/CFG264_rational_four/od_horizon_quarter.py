#!/usr/bin/env python3
"""CFG264 OD -- OWNER-DIRECTED route: is the 1/2 (the 4 in 32 pi) a conversion between the horizon's entropy quarter (S = A/4)
and the bulk Einstein coupling (8 pi)?  Test: an equilibrium / extremum / matching condition between a horizon's entropy budget
S = k_B A c^3/(4 G hbar) and the vacuum energy it encloses, with hbar cancelling, that OUTPUTS k2 = a0^2/(c^2 G rho_L) = 1/4.

Modes:  python3 od_horizon_quarter.py           -> od_horizon_quarter.out, od_horizon_quarter_results.json
        python3 od_horizon_quarter.py --mutate  -> od_horizon_quarter_MUTATE.out, od_horizon_quarter_MUTATE_results.json
"""
import sys
import sympy as sp
from cfg264_lib import Checker, pi_content, is_target, decoy_hits, circularity_guard, write_json

MUTATE = "--mutate" in sys.argv
TAG = "od_horizon_quarter" + ("_MUTATE" if MUTATE else "")
ck = Checker(TAG)
_out = open(TAG + ".out", "w")
_orig_log = ck.log


def log(s=""):
    _orig_log(s)
    _out.write(s + "\n")
    _out.flush()


ck.log = log
pi = sp.pi
hbar, kB, c, G, rho, r, kap, a0 = sp.symbols("hbar k_B c G rho_L r kappa_h a0", positive=True)


def geometry(D=4):
    D = sp.Integer(D)
    Omega = {4: 4 * pi, 5: 2 * pi**2}[int(D)]           # area of the unit (D-2)-sphere
    A = Omega * r**(D - 2)
    V = Omega * r**(D - 1) / (D - 1)
    H2 = 16 * pi * G * rho / ((D - 1) * (D - 2))         # Friedmann H^2 in D dimensions
    tolman = sp.Integer(2) / (D - 3)                      # vacuum active density, dust-normalised (2 at D = 4)
    kS = (D - 3) * c**2 / (2 * r)                         # Tangherlini (flat probe) surface gravity
    kR = c**2 / r                                         # Rindler sphere: radius c^2/a, kappa = a
    return dict(D=D, Omega=Omega, A=A, V=V, H2=H2, tolman=tolman, kS=kS, kR=kR)


def thermo(kappa_expr, geo, two_pi=True, quarter=sp.Rational(1, 4)):
    T = hbar * kappa_expr / ((2 * pi if two_pi else 1) * c * kB)
    S = quarter * kB * geo["A"] * c**3 / (G * hbar)
    Nsur = geo["A"] * c**3 / (G * hbar)                   # Padmanabhan surface d.o.f. (no quarter)
    return T, S, Nsur


def budgets(kappa_expr, geo, two_pi=True, quarter=sp.Rational(1, 4)):
    T, S, Nsur = thermo(kappa_expr, geo, two_pi, quarter)
    Evac = rho * c**2 * geo["V"]
    EK = geo["tolman"] * rho * c**2 * geo["V"]
    B = {
        "B1 TS = E_vac": sp.Eq(T * S, Evac),
        "B2 2TS = E_vac": sp.Eq(2 * T * S, Evac),
        "B3 TS = E_Komar": sp.Eq(T * S, EK),
        "B4 N_sur kT/2 = E_Komar": sp.Eq(Nsur * kB * T / 2, EK),
        "B5 (S/k) kT/2 = E_Komar": sp.Eq(S / kB * kB * T / 2, EK),
        "B6 T dS/dr = dE_vac/dr": sp.Eq(T * sp.diff(S, r), sp.diff(Evac, r)),
        "B7 dF/dr = 0 at fixed T": sp.Eq(sp.diff(Evac, r) - T * sp.diff(S, r), 0),
        "B7' d(E_vac - T(r)S(r))/dr = 0": sp.Eq(sp.diff(Evac - T * S, r), 0),
    }
    return B, T, S


def solve_horizon(hname, geo, two_pi=True, quarter=sp.Rational(1, 4)):
    rows = []
    if hname == "HdS":
        H = sp.sqrt(geo["H2"])
        kexpr = c * H
        B, T, S = budgets(kexpr, geo, two_pi, quarter)
        for bn, eq in B.items():
            e = sp.simplify((eq.lhs - eq.rhs).subs(r, c / H))
            lhs = sp.simplify(eq.lhs.subs(r, c / H))
            rhs = sp.simplify(eq.rhs.subs(r, c / H))
            ident = sp.simplify(e) == 0
            ratio = sp.simplify(lhs / rhs) if rhs != 0 else None
            k2 = sp.simplify(kexpr**2 / (c**2 * G * rho))
            rows.append(dict(horizon=hname, budget=bn, status="identity" if ident else "violated", ratio=str(ratio),
                             k2_if_a0_is_kappa_h=str(k2), hbar_free=not (e.has(hbar) or e.has(kB))))
        return rows
    kexpr = geo["kS"] if hname == "HS" else geo["kR"]
    B, T, S = budgets(kexpr, geo, two_pi, quarter)
    for bn, eq in B.items():
        e = sp.simplify(eq.lhs - eq.rhs)
        hb = not (e.has(hbar) or e.has(kB))
        sols = [s for s in sp.solve(sp.Eq(e, 0), r) if s.is_positive]
        if not sols:
            rows.append(dict(horizon=hname, budget=bn, status="no_positive_radius", hbar_free=hb))
            continue
        for s_ in sols:
            k2 = sp.simplify((kexpr**2).subs(r, s_) / (c**2 * G * rho))
            pk = pi_content(k2)
            rows.append(dict(horizon=hname, budget=bn, status="solved", r=str(s_), k2=str(k2), k2_float=float(sp.N(k2)),
                             pi_kind=pk[0], pi_coeff=str(pk[1]), pi_exp=str(pk[2]), hbar_free=hb and not k2.has(hbar) and not k2.has(kB),
                             hits_target=bool(is_target(k2)), decoys=decoy_hits(k2)))
    return rows


def run_menu(D=4, two_pi=True, quarter=sp.Rational(1, 4), label="baseline"):
    geo = geometry(D)
    table = []
    for h in ("HdS", "HS", "HR"):
        table += solve_horizon(h, geo, two_pi, quarter)
    log(f"\n--- {label}: D = {D}, thermal 2 pi {'ON' if two_pi else 'OFF'}, entropy factor {quarter} ---")
    for row in table:
        if row["status"] == "solved":
            tag = "   <-- k2 = 1/4" if row["hits_target"] else ""
            log(f"   {row['horizon']:<4} {row['budget']:<32} k2 = {row['k2']:<14} ({row['k2_float']:.6f}; {row['pi_kind']} x pi^{row['pi_exp']}; hbar-free {row['hbar_free']}){tag}")
        elif row["status"] in ("identity", "violated"):
            log(f"   {row['horizon']:<4} {row['budget']:<32} {row['status']:<9} (LHS/RHS = {row['ratio']}; the dS horizon's kappa = cH gives k2 = {row['k2_if_a0_is_kappa_h']})")
        else:
            log(f"   {row['horizon']:<4} {row['budget']:<32} {row['status']}")
    return table


results = {"lane": "CFG264", "route": "OD owner-directed: horizon quarter vs bulk 8 pi", "mode": "MUTATE" if MUTATE else "main"}

if not MUTATE:
    log("CFG264 OD (OWNER-DIRECTED) -- the entropy quarter vs the bulk 8 pi (main run)")
    log("=" * 100)
    # ------------------------------------------------------------------------------------------------------------
    log("\nA. hbar-cancellation lemma: with T = hbar kappa/(2 pi c k_B) and S = k_B A c^3/(4 G hbar), T^a S^b is hbar- and k_B-free iff a = b")
    T0 = hbar * kap / (2 * pi * c * kB)
    S0 = kB * sp.Symbol("A", positive=True) * c**3 / (4 * G * hbar)
    ok = all(((T0**i * S0**j).has(hbar) or (T0**i * S0**j).has(kB)) == (i != j) for i in range(-3, 4) for j in range(-3, 4))
    ck.check("A1 among T^a S^b (|a|,|b| <= 3) exactly the a = b products are free of hbar and k_B", ok)
    TS = sp.simplify(T0 * S0)
    ck.check("A2 TS = kappa A c^2/(8 pi G): the quarter enters an hbar-free budget only as (1/4)(1/2 pi) = 1/(8 pi)",
             sp.simplify(TS - kap * sp.Symbol("A", positive=True) * c**2 / (8 * pi * G)) == 0)
    Ns = sp.Symbol("A", positive=True) * c**3 / (G * hbar)
    ck.check("A3 Padmanabhan N_sur k_B T = kappa A c^2/(2 pi G): without the quarter only the thermal 1/(2 pi) survives",
             sp.simplify(Ns * kB * T0 - kap * sp.Symbol("A", positive=True) * c**2 / (2 * pi * G)) == 0)
    # Einstein's 8 pi against the entropy's 8 pi: ratio TS / E_vac with rho = Lambda c^2/(8 pi G)
    Lam = sp.Symbol("Lambda", positive=True)
    Vs = sp.Symbol("V", positive=True)
    ratio = sp.simplify(TS / ((Lam * c**2 / (8 * pi * G)) * c**2 * Vs))
    ck.check("A4 TS / E_vac with rho_L = Lambda c^2/(8 pi G) is kappa A/(Lambda c^2 V): the entropy's 8 pi CANCELS Einstein's 8 pi (it does not multiply it)",
             sp.simplify(ratio - kap * sp.Symbol("A", positive=True) / (Lam * c**2 * Vs)) == 0 and not ratio.has(pi))

    # ------------------------------------------------------------------------------------------------------------
    log("\nB. Where the quarter lives: GHY vs Einstein-Hilbert, and the Euclidean Schwarzschild action (c = hbar = k_B = 1)")
    ck.check("B1 normalisations: GHY 1/(8 pi G) over bulk 1/(16 pi G) = 2 (a factor 2, not 1/4; D-independent)",
             sp.Rational(1, 8) / sp.Rational(1, 16) == 2)
    Rb, Mm, beta = sp.symbols("R_b M beta", positive=True)
    rr = sp.Symbol("rr", positive=True)
    fS = 1 - 2 * G * Mm / rr
    # Euclidean: ds^2 = f dtau^2 + dr^2/f + r^2 dOmega^2 ; boundary r = R_b ; K = (1/r^2) d(r^2 sqrt f)/dr
    K = sp.diff(rr**2 * sp.sqrt(fS), rr) / rr**2
    surf = beta * 4 * pi * sp.sqrt(fS) * rr**2 * K                      # integral of sqrt(h) K
    surf0 = (beta * sp.sqrt(fS)) * 4 * pi * rr**2 * (2 / rr)            # flat subtraction, matched proper period
    I_E = sp.limit(-(surf - surf0) / (8 * pi * G), rr, sp.oo)
    ck.check("B2 Schwarzschild: R = 0 on shell, GHY with flat subtraction gives I_E = beta M/2", sp.simplify(I_E - beta * Mm / 2) == 0)
    beta_H = 8 * pi * G * Mm                                            # 2 pi/kappa, kappa = 1/(4 G M)
    S_E = sp.simplify(beta_H * Mm - I_E.subs(beta, beta_H))
    A_h = 4 * pi * (2 * G * Mm)**2
    ck.check("B3 S = beta M - I_E = A/(4G): the quarter is produced by the thermal period 2 pi/kappa and the GHY boundary term together",
             sp.simplify(S_E - A_h / (4 * G)) == 0)
    ck.check("B4 the quarter is therefore an ENTROPY normalisation (it needs beta = 2 pi/kappa), not an action normalisation (GHY/EH = 2)",
             sp.simplify(S_E / (beta_H * Mm)) == sp.Rational(1, 2) and sp.simplify(I_E.subs(beta, beta_H) / (beta_H * Mm)) == sp.Rational(1, 2))

    # ------------------------------------------------------------------------------------------------------------
    log("\nC. Circularity guard and audit")
    geo = geometry(4)
    eqs = []
    for h in ("HS", "HR"):
        B, _, _ = budgets(geo["kS"] if h == "HS" else geo["kR"], geo)
        for bn, eq in B.items():
            eqs.append(eq.subs(r, c**2 / (2 * a0) if h == "HS" else c**2 / a0))
    gd = circularity_guard(eqs, a0, rho, c, G)
    ck.check("C1 no single budget condition, with a0 := kappa_h, already forces k2 = 1/4 (guard on all HS/HR budgets)",
             all(v.startswith("ok") for _, v in gd), str([v for _, v in gd][:4]) + " ...")
    log("   audit: inputs = Unruh/Hawking T, Bekenstein-Hawking S (with hbar), the vacuum energy rho_L c^2 V (Einstein's 8 pi G only through H in HdS),"
        " the Komar/Tolman factor 2, Padmanabhan's N_sur, horizon surface gravities (Schwarzschild c^2/2r, Rindler c^2/r, de Sitter cH). No input"
        " contains kappa = 1/2, 32 pi, Lambda = 32 pi a0^2/c^4 or R*. The owner's 'ratio of 1/4 to 8 pi' is never inserted as a number.")

    # ------------------------------------------------------------------------------------------------------------
    log("\nD. Declared matching menu (D = 4): horizons {HdS, HS, HR} x budgets {B1..B7, B7'}")
    table = run_menu()
    results["baseline_table"] = table
    solved = [t for t in table if t["status"] == "solved"]
    ck.check("D1 hbar and k_B cancel in every solved budget", all(t["hbar_free"] for t in solved) and len(solved) > 0, f"{len(solved)} solved")
    b1ds = [t for t in table if t["horizon"] == "HdS" and t["budget"].startswith("B1")][0]
    ck.check("D2 HE3: on the de Sitter horizon TS = E_vac is an IDENTITY (Friedmann); its acceleration cH gives k2 = 8 pi/3 (a0 = cH: Z = 1, kappa = 2.894, lane N member (ii); NOT the forced kernel kappa = 1)",
             b1ds["status"] == "identity" and sp.simplify(sp.sympify(b1ds["k2_if_a0_is_kappa_h"]) - 8 * pi / 3) == 0)
    hs = {t["budget"][:3]: t for t in solved if t["horizon"] == "HS"}
    ck.check("D3 cross-lane: HS-B1 (TS = |PV|) = 4 pi/3 and HS-B2 (2TS = |PV|) = 2 pi/3 reproduce X3's flat-probe entries",
             sp.simplify(sp.sympify(hs["B1 "]["k2"]) - 4 * pi / 3) == 0 and sp.simplify(sp.sympify(hs["B2 "]["k2"]) - 2 * pi / 3) == 0)
    b6 = {t["horizon"]: t.get("k2") for t in solved if t["budget"].startswith("B6")}
    b7 = {t["horizon"]: t.get("k2") for t in solved if t["budget"].startswith("B7 ")}
    ck.check("D4 Addendum 2: B7 (fixed-T stationary point) coincides with B6 on every horizon", b6 == b7 and len(b6) == 2, f"B6 {b6}, B7 {b7}")
    allpi = all(t["pi_exp"] == "1" for t in solved)
    ck.check("D5 every solved HS/HR budget gives k2 = (rational) x pi^1: the thermal 2 pi paired with the quarter leaves one pi", allpi)
    hits = [(t["horizon"], t["budget"]) for t in solved if t["hits_target"]]
    log(f"   INFO (verdict input, not a check): systems hitting k2 = 1/4: {hits}")

    # ------------------------------------------------------------------------------------------------------------
    log("\nE. Obstacle (a): the 'Einstein 8 pi x entropy 4' reading and the double count")
    k2sym = sp.Symbol("k2", positive=True)
    # the reading: a0^2 = (1/4) x (Lambda c^4/(8 pi)) with Lambda = 8 pi G rho_L/c^2
    reading = sp.simplify(sp.Rational(1, 4) * (8 * pi * G * rho / c**2) * c**4 / (8 * pi) / (c**2 * G * rho))
    ck.check("E1 the conversion reading a0^2 = (1/4)(Lambda c^4/8 pi) is k2 = 1/4 by construction: the quarter is INSERTED as the number, i.e. a restatement",
             reading == sp.Rational(1, 4))
    # a literal SECOND quarter on top of the TS pairing: rerun B1-B6 with S -> S/4
    t2 = []
    geo = geometry(4)
    for h in ("HS", "HR"):
        t2 += solve_horizon(h, geo, quarter=sp.Rational(1, 16))
    pi2 = all(t["pi_exp"] == "1" for t in t2 if t["status"] == "solved")
    ck.check("E2 even counting the quarter twice (S -> A/16) leaves every budget at (rational) x pi^1: the 4 in 32 pi cannot come from an entropy factor",
             pi2 and not any(t.get("hits_target") for t in t2))
    results["double_count_table"] = t2

    # ------------------------------------------------------------------------------------------------------------
    log("\nF. POST-RUN check (Addendum 3; requested after CFG263): does the owner's balance couple an a0-sector ENERGY DENSITY?")
    Hs = sp.Symbol("H", positive=True)
    rho_of_H = 3 * Hs**2 / (8 * pi * G)
    allowed = {r, c, G, Hs, hbar, kB}
    clean = True
    for h in ("HS", "HR"):
        Bh, _, _ = budgets(geo["kS"] if h == "HS" else geo["kR"], geo)
        for bn, eq in Bh.items():
            fs = (eq.lhs - eq.rhs).subs(rho, rho_of_H).free_symbols
            if not fs <= allowed or a0 in fs:
                clean = False
    ck.check("F1 every HS/HR budget, with rho_L = 3H^2/(8 pi G), contains only {r, c, G, H, hbar, k_B}: no a0-sector energy density occurs;"
             " a0 enters only as the label on kappa_h", clean)
    qs = [sp.nsimplify(sp.simplify(sp.sympify(t["k2"]) / (8 * pi / 3))) for t in table if t["status"] == "solved"]
    ck.check("F1b every solved k2 is (8 pi/3) x rational, i.e. a0/(cH) is algebraic: the 'scales a and H only' class that CFG263 excludes",
             len(qs) == 16 and all(q.is_rational for q in qs), str(sorted(set(qs))))
    # F2: couple an a0-sector energy density eps = W a0^2/G as the vacuum (rho_L c^2 = eps)
    Wv = sp.Symbol("W", positive=True)
    eps = Wv * a0**2 / G
    H_eps = sp.sqrt(8 * pi * G * (eps / c**2) / 3)
    Td = hbar * (c * H_eps) / (2 * pi * c * kB)
    Sd = sp.Rational(1, 4) * kB * 4 * pi * (c / H_eps)**2 * c**3 / (G * hbar)
    resid = sp.simplify(Td * Sd - eps * sp.Rational(4, 3) * pi * (c / H_eps)**3)
    ck.check("F2 de Sitter horizon with the vacuum = an a0-sector energy density eps = W a0^2/G: TS = eps V holds for EVERY W (identity);"
             " the horizon budget fixes nothing, so W = 4 (k2 = 1/W = 1/4) would have to come from the a0 sector itself (lane K's open target)",
             resid == 0)
    rS = c**2 / (2 * a0)
    TS_S = sp.simplify((hbar * a0 / (2 * pi * c * kB)) * (kB * 4 * pi * rS**2 * c**3 / (4 * G * hbar)))
    Wsol = sp.solve(sp.Eq(TS_S, eps * sp.Rational(4, 3) * pi * rS**3), Wv)
    ck.check("F2b HS probe with kappa_h = a0 and the same eps: TS = eps V fixes W = 3/(4 pi), i.e. k2 = 1/W = 4 pi/3 (= HS-B1): coupling an"
             " a0-sector energy density through this budget re-inserts the pi", Wsol == [3 / (4 * pi)])
    results["post_run_CFG263_check"] = dict(F1_clean=clean, F1b_q_values=[str(q) for q in sorted(set(qs))], F2_dS_identity=(resid == 0),
                                            F2b_W=[str(w) for w in Wsol])
    results["checks"] = ck.records
    verdict = ("SCOPED NO-GO (binding failure: hbar-cancellation). For hbar to cancel the quarter must travel with the thermal 1/(2 pi), as 1/(8 pi);"
               " in any entropy-vs-vacuum-energy budget that 8 pi CANCELS Einstein's 8 pi instead of multiplying it, so every declared condition"
               " gives k2 = (rational) x pi (HS/HR) or the de Sitter identity with k2 = 8 pi/3, i.e. a0 = c H_Lambda (HdS). The 'conversion factor' reading (32 pi = 8 pi x 4,"
               " 4 = 1/quarter) is a RESTATEMENT: the 1/4 enters only when inserted as a number, which is the DERIVE_Z strike-3 double count."
               if not hits else "CANDIDATE HIT -- apply the menu-selection rule")
    log("\nVERDICT OD: " + verdict)
    results["verdict"] = verdict
else:
    log("CFG264 OD -- MUTATE run (separate outputs)")
    log("=" * 100)
    base = run_menu(label="baseline (recomputed)")
    bmap = {(t["horizon"], t["budget"]): t.get("k2", t.get("status")) for t in base}
    muts = {"M1 thermal 2 pi removed (T = hbar kappa/(c k_B))": dict(two_pi=False),
            "M2 entropy quarter -> 1/2 (S = A/2)": dict(quarter=sp.Rational(1, 2)),
            "M3 D = 4 -> 5": dict(D=5)}
    results["mutations"] = {}
    for label, kw in muts.items():
        t = run_menu(label=label, **kw)
        ch = [(x["horizon"], x["budget"]) for x in t if x.get("k2", x.get("status")) != bmap.get((x["horizon"], x["budget"]))]
        ck.check(f"{label}: output changes", len(ch) > 0, f"{len(ch)} rows changed")
        sol = [x for x in t if x["status"] == "solved"]
        rat0 = sorted(set(x["k2"] for x in sol if x["pi_exp"] == "0"))
        hits = [(x["horizon"], x["budget"]) for x in sol if x["hits_target"]]
        log(f"   pi-free k2 values under this mutation: {rat0}; k2 = 1/4 hits: {hits}")
        results["mutations"][label] = dict(changed=len(ch), pi_free_values=rat0, target_hits=hits, table=t)
        if label.startswith("M1"):
            ck.check("M1b removing the thermal 2 pi makes every HS/HR budget pi-free (the pi of the main run IS the thermal 2 pi)",
                     all(x["pi_exp"] == "0" for x in sol) and len(sol) > 0)
    results["checks"] = ck.records

ck.summary()
results["n_pass"], results["n_fail"] = ck.n_pass, ck.n_fail
write_json(TAG + "_results.json", results)
_out.close()
sys.exit(0 if ck.n_fail == 0 else 1)
