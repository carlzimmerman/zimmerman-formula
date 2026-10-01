#!/usr/bin/env python3
"""CFG264 R2 -- two-sided (in/out averaged) junction of a MOND-critical wall with the vacuum.

Pure-tension spherical wall (S_ij = -sigma h_ij) between a de Sitter interior (rho_in = rho_L) and a Minkowski exterior.
Derived here from the metric: the wall's side accelerations k_in, k_out, their jump 8 pi G sigma/(D-2) and their average
abar = Delta rho c^2/((D-1) sigma). Declared conditions (J) identify a0 with a wall acceleration; declared closures (Sg) fix sigma.
Output k2 = a0^2/(c^2 G rho_L); the target 1/4 is used only in compare.

Modes:  python3 r2_two_sided_junction.py           -> .out, _results.json
        python3 r2_two_sided_junction.py --mutate  -> _MUTATE.out, _MUTATE_results.json
"""
import sys
import sympy as sp
from cfg264_lib import Checker, pi_content, is_target, decoy_hits, circularity_guard, write_json

MUTATE = "--mutate" in sys.argv
TAG = "r2_two_sided_junction" + ("_MUTATE" if MUTATE else "")
ck = Checker(TAG)
_out = open(TAG + ".out", "w")
_orig_log = ck.log


def log(s=""):
    _orig_log(s)
    _out.write(s + "\n")
    _out.flush()


ck.log = log
pi = sp.pi
a0, sigma, rho, c, G, Rw = sp.symbols("a0 sigma rho_L c G R_w", positive=True)


def wall_quantities(D=4, rho_in=None, rho_out=0, sigma_=sigma):
    """Return dict with signed side accelerations (orientation chosen so abar > 0), abar, jump, R_w."""
    D = sp.Integer(D)
    if rho_in is None:
        rho_in = rho
    H2in = 16 * pi * G * rho_in / ((D - 1) * (D - 2))                    # H^2 (1/s^2); Friedmann in D dimensions
    H2out = 16 * pi * G * rho_out / ((D - 1) * (D - 2))
    jump = 8 * pi * G * sigma_ / (D - 2)                                   # acceleration jump (m/s^2)
    abar = c**2 * (H2in - H2out) / (2 * jump) if jump != 0 else sp.oo      # from k_out^2 - k_in^2 = c^2 (H_in^2 - H_out^2)
    a_in = abar - jump / 2
    a_out = abar + jump / 2
    # worldvolume radius from k_out^2 = c^4/R_w^2 - c^2 H_out^2  (k in m/s^2, R_w in m)
    Rw_ = c**2 / sp.sqrt(a_out**2 + c**2 * H2out)
    return dict(H2in=H2in, H2out=H2out, jump=jump, abar=sp.simplify(abar), a_in=sp.simplify(a_in), a_out=sp.simplify(a_out), Rw=sp.simplify(Rw_))


def build(D=4, mode="baseline"):
    W = wall_quantities(D=D)
    D = sp.Integer(D)
    half_jump = W["jump"] / 2          # = Z2 wall's own proper acceleration in D dims (2 pi G sigma at D = 4)
    J = {
        "J1": sp.Eq(W["abar"], a0),
        "J2+": sp.Eq(W["a_in"], a0),
        "J2-": sp.Eq(W["a_in"], -a0),
        "J3": sp.Eq(W["a_out"], a0),
        "J4": sp.Eq(W["a_in"] * W["a_out"], a0**2),
        "J5": sp.Eq(half_jump, a0),
    }
    if mode == "M1_one_sided":
        J["J1"] = sp.Eq(W["a_out"], a0)        # two-sided average replaced by one side
    Sg = {
        "Sg1": sp.Eq(half_jump, a0),                                         # Sigma_M (D = 4: 2 pi G sigma = a0)
        "Sg2": sp.Eq(W["jump"], a0),                                         # field jump = a0
        "Sg3": sp.Eq(W["a_in"], 0),                                          # wall on the interior's dS horizon
        "Sg4": sp.Eq(W["a_out"], 0),
        "Sg5": sp.Eq(sp.Integer(1) * sigma, rho * W["Rw"] / (D - 1)),        # wall mass = enclosed vacuum mass (area x sigma = volume x rho)
        "Sg6": sp.Eq(16 * pi * G * W["Rw"] * sigma / (D - 2), c**2),          # D = 4: 4 pi G R sigma = c^2/2 (wall mass = Schwarzschild mass of R_w)
    }
    if mode == "M3_piFree_sigma":
        q = sp.Symbol("q", positive=True)
        Sg = {"SgQ": sp.Eq(sigma, q * a0 / G)}
    return W, J, Sg


def solve_pair(eqJ, eqS):
    """Solve two equations for sigma, a0 > 0; return list of k2 (a0^2/(c^2 G rho))."""
    try:
        sols = sp.solve([eqJ, eqS], [sigma, a0], dict=True)
    except Exception as e:
        return "error", str(e)
    out = []
    for s in sols:
        if sigma not in s or a0 not in s:
            continue
        sg, aa = sp.simplify(s[sigma]), sp.simplify(s[a0])
        if aa.free_symbols - {c, G, rho} or sg.free_symbols - {c, G, rho, a0}:
            out.append(("family", str(aa)))
            continue
        k2 = sp.simplify(aa**2 / (c**2 * G * rho))
        if k2.free_symbols:
            out.append(("family", str(k2)))
            continue
        try:
            av = complex(sp.N(aa.subs({c: 1, G: 1, rho: 1})))
            sv = complex(sp.N(sg.subs({c: 1, G: 1, rho: 1, a0: aa.subs({c: 1, G: 1, rho: 1})})))
        except Exception:
            continue
        if abs(av.imag) > 1e-12 or abs(sv.imag) > 1e-12 or av.real <= 0 or sv.real <= 0:
            continue
        out.append(("k2", k2))
    if not sols:
        return "no_solution", []
    if not out:
        return "no_positive_solution", []
    return "ok", out


def run_menu(D=4, mode="baseline"):
    W, J, Sg = build(D=D, mode=mode)
    table = []
    for jn, eqJ in J.items():
        for sn, eqS in Sg.items():
            if jn == "J5" and sn == "Sg1":
                continue
            st, res = solve_pair(eqJ, eqS)
            row = dict(system=f"{jn}+{sn}", status=st)
            if st == "ok":
                vals = []
                for kind, v in res:
                    if kind == "k2":
                        pk = pi_content(v)
                        vals.append(dict(k2=str(v), k2_float=float(sp.N(v)), pi_kind=pk[0], pi_coeff=str(pk[1]), pi_exp=str(pk[2]),
                                         hits_target=bool(is_target(v)), decoys=decoy_hits(v)))
                    else:
                        vals.append(dict(family=v))
                row["solutions"] = vals
            table.append(row)
    return W, table


def report(table, title):
    log(f"\n--- {title}: {len(table)} (J, Sg) systems ---")
    nsol = 0
    hits, rational0 = [], []
    for r in table:
        if r["status"] != "ok":
            log(f"   {r['system']:<10} {r['status']}")
            continue
        for s in r["solutions"]:
            if "k2" in s:
                nsol += 1
                tag = "  <-- k2 = 1/4" if s["hits_target"] else ""
                log(f"   {r['system']:<10} k2 = {s['k2']:<34} ({s['k2_float']:.6f}; {s['pi_kind']} x pi^{s['pi_exp']}){tag}")
                if s["hits_target"]:
                    hits.append(r["system"])
                if s["pi_kind"] == "rational" and s["pi_exp"] == "0":
                    rational0.append((r["system"], s["k2"]))
            else:
                log(f"   {r['system']:<10} one-parameter family: a0 = {s['family']}")
    return dict(n_solutions=nsol, target_hits=hits, rational_pi0=rational0)


results = {"lane": "CFG264", "route": "R2 two-sided MOND-critical junction", "mode": "MUTATE" if MUTATE else "main"}

if not MUTATE:
    log("CFG264 R2 -- two-sided junction of a MOND-critical wall with the vacuum (main run)")
    log("=" * 100)
    # --------------------------------------------------------------------------------------------------------
    log("\nA. Wall kinematics from the metric  ds^2 = -f c^2 dt^2 + dr^2/f + r^2 dOmega^2  (c = 1 in A only)")
    tau = sp.Symbol("tau", real=True)
    r = sp.Symbol("r", positive=True)
    H = sp.Symbol("H", positive=True)
    k = sp.Symbol("k", positive=True)
    Rf = sp.Function("R")(tau)
    f = sp.Function("f")
    # radial timelike worldline (t(tau), R(tau)); u = (tdot, Rdot); normalisation f tdot^2 - Rdot^2/f = 1
    Rd = sp.diff(Rf, tau)
    Rdd = sp.diff(Rf, tau, 2)
    fR = f(Rf)
    tdot = sp.sqrt(fR + Rd**2) / fR
    # Christoffels of the (t, r) block: G^t_tr = f'/(2f), G^r_tt = f f'/2, G^r_rr = -f'/(2f)
    fp = sp.diff(f(r), r).subs(r, Rf)
    tdd = sp.diff(tdot, tau)
    acc_t = tdd + 2 * (fp / (2 * fR)) * tdot * Rd
    acc_r = Rdd + (fR * fp / 2) * tdot**2 - (fp / (2 * fR)) * Rd**2
    acc2 = sp.simplify(-fR * acc_t**2 + acc_r**2 / fR)            # a^mu a_mu
    target_acc = (Rdd + fp / 2) / sp.sqrt(fR + Rd**2)
    ck.check("A1 proper acceleration of a radial worldline: |a| = (R'' + f'/2)/sqrt(f + R'^2) (from the Christoffels)",
             sp.simplify(acc2 - target_acc**2) == 0)
    # unit normal n (orthogonal to u, n^r = sqrt(f + Rdot^2)) -> angular extrinsic curvature K^th_th = n^r / R
    nr = sp.sqrt(fR + Rd**2)
    nt = Rd / fR
    ck.check("A2 unit normal n = (Rdot/f, sqrt(f+Rdot^2)) is orthogonal to u and normalised",
             sp.simplify(-fR * tdot * nt + Rd * nr / fR) == 0 and sp.simplify(-fR * nt**2 + nr**2 / fR - 1) == 0)
    # umbilic pure-tension solution in dS: f = 1 - H^2 r^2, R(tau) = cosh(w tau)/w, w^2 = k^2 + H^2
    w = sp.sqrt(k**2 + H**2)
    Rsol = sp.cosh(w * tau) / w
    fdS = lambda x: 1 - H**2 * x**2
    # exact identities (sympy cannot take sqrt(cosh^2) without cosh > 0, which holds for real tau): f + Rdot^2 = cosh^2 k^2/w^2,
    # and the K^tau_tau numerator R'' + f'/2 = k^2 R; hence K^th_th = K^tau_tau = k. Plus numeric spot checks.
    inner = sp.simplify(fdS(Rsol) + sp.diff(Rsol, tau)**2)
    numtt = sp.simplify(sp.diff(Rsol, tau, 2) + sp.diff(fdS(r), r).subs(r, Rsol) / 2)
    spots = []
    for tv in (-1.3, 0.0, 0.7, 2.1):
        for hv, kv in ((0.5, 1.2), (2.0, 0.3), (1.0, 1.0)):
            sub = {tau: tv, H: hv, k: kv}
            spots.append(abs(float(sp.N((sp.sqrt(inner) / Rsol).subs(sub))) - kv) < 1e-12 and abs(float(sp.N((numtt / sp.sqrt(inner)).subs(sub))) - kv) < 1e-12)
    ck.check("A3 dS: R(tau) = cosh(w tau)/w, w^2 = k^2 + H^2, is umbilic with K^tau_tau = K^th_th = k (exact identities + 12 numeric spots)",
             sp.simplify(inner - sp.cosh(w * tau)**2 * k**2 / w**2) == 0 and sp.simplify(numtt - k**2 * Rsol) == 0 and all(spots))
    innerM = sp.simplify(1 + sp.diff(sp.cosh(k * tau) / k, tau)**2)
    ck.check("A4 Minkowski limit H = 0: f + Rdot^2 = cosh^2, so K^th_th = k = 1/R_w (uniformly accelerated sphere)",
             sp.simplify(innerM - sp.cosh(k * tau)**2) == 0)
    # Israel, pure tension, general D:  [K_ij] - h_ij [K] = -8 pi G S_ij,  S_ij = -sigma h_ij,  K_ij = kk h_ij (n = D-1 worldvolume dims)
    Dg = sp.Symbol("D", positive=True, integer=True)
    dk = sp.Symbol("dk")
    nwv = Dg - 1
    eq_israel = sp.Eq(dk - nwv * dk, -8 * pi * G * (-sigma))
    dk_sol = sp.solve(eq_israel, dk)[0]
    ck.check("A5 Israel for pure tension: [k] = -8 pi G sigma/(D-2) (D = 4: magnitude 4 pi G sigma)",
             sp.simplify(dk_sol + 8 * pi * G * sigma / (Dg - 2)) == 0 and sp.simplify(dk_sol.subs(Dg, 4) + 4 * pi * G * sigma) == 0)
    # normal-force (shell equation of motion) form: (D-1) sigma kbar = Delta rho c^2  <->  abar
    W4 = wall_quantities(D=4)
    ck.check("A6 two-sided average abar = Delta rho c^2/(3 sigma) at D = 4 (from k_out^2 - k_in^2 = c^2 H_in^2 and the jump)",
             sp.simplify(W4["abar"] - rho * c**2 / (3 * sigma)) == 0)
    Dsym = sp.Symbol("Dd", positive=True)
    H2D = 16 * pi * G * rho / ((Dsym - 1) * (Dsym - 2))
    abarD = sp.simplify(c**2 * H2D / (2 * 8 * pi * G * sigma / (Dsym - 2)))
    ck.check("A7 general D: abar = Delta rho c^2/((D-1) sigma), i.e. (D-1) sigma abar = Delta p (the shell's normal-force equation)",
             sp.simplify(abarD - rho * c**2 / ((Dsym - 1) * sigma)) == 0)
    ck.check("A8 side accelerations reproduce the record's audit H1: A, B = Delta P/(3 sigma) -+ 2 pi G sigma",
             sp.simplify(W4["a_in"] - (rho * c**2 / (3 * sigma) - 2 * pi * G * sigma)) == 0
             and sp.simplify(W4["a_out"] - (rho * c**2 / (3 * sigma) + 2 * pi * G * sigma)) == 0)
    # consistency: both sides share the worldvolume radius
    ck.check("A9 both sides induce the same worldvolume radius R_w (c^4/R_w^2 = k_in^2 + c^2 H_in^2 = k_out^2; squared identity)",
             sp.simplify(W4["a_in"]**2 + c**2 * W4["H2in"] - W4["a_out"]**2) == 0)
    # pi bookkeeping
    ck.check("A10 abar is pi-free in G rho_L and carries c; the jump 4 pi G sigma carries pi",
             not W4["abar"].has(pi) and W4["abar"].has(c) and W4["jump"].has(pi))
    # Z2 control: rho_in = rho_out
    Wz = wall_quantities(D=4, rho_in=rho, rho_out=rho)
    ck.check("A11 Z2 control (rho_in = rho_out): abar = 0 and each side accelerates at 2 pi G sigma, for every rho (no a0-rho relation possible)",
             sp.simplify(Wz["abar"]) == 0 and sp.simplify(Wz["a_out"] - 2 * pi * G * sigma) == 0)

    # --------------------------------------------------------------------------------------------------------
    log("\nB. Circularity guard and audit")
    W, J, Sg = build()
    guard = circularity_guard(list(J.values()) + list(Sg.values()), a0, rho, c, G)
    names = list(J.keys()) + list(Sg.keys())
    for (i, v), n in zip(guard, names):
        log(f"   guard {n}: {v}")
    ck.check("B1 no single declared condition forces k2 = 1/4 on its own", all(v.startswith("ok") for _, v in guard))
    log("   audit: inputs = Israel junction (GR), interior de Sitter with H^2 = (8 pi/3) G rho_L (Einstein's 8 pi G), the wall kinematics of A,"
        " identifications J (a0 = a wall acceleration) and closures Sg (Gauss/Milgrom surface densities, horizon, mass budgets). No input contains"
        " kappa, 32 pi, Lambda = 32 pi a0^2/c^4 or R*.")

    # --------------------------------------------------------------------------------------------------------
    log("\nC. Declared menu: one J x one Sg (D = 4)")
    W, table = run_menu()
    S = report(table, "baseline D = 4")
    results["baseline"] = S
    results["baseline_table"] = table
    j1sg1 = [s for r in table if r["system"] == "J1+Sg1" for s in r.get("solutions", []) if "k2" in s]
    ck.check("C1 the MOND-critical wall with the two-sided average (J1 + Sg1) gives k2 = 2 pi/3 (kappa = 1.447, a0 = c H/2)",
             len(j1sg1) == 1 and sp.simplify(sp.sympify(j1sg1[0]["k2"]) - 2 * pi / 3) == 0)
    allpi = all(s["pi_exp"] != "0" for r in table for s in r.get("solutions", []) if "k2" in s)
    ck.check("C2 every solved (J, Sg) system carries pi in k2 (no pi-free value in the declared menu)", allpi)
    log(f"   INFO (verdict input, not a check): systems hitting k2 = 1/4: {S['target_hits']}")
    # where the pi enters: abar is pi-free, so it must come from the sigma closure or the self-gravity term
    sg_has_pi = {n: (sp.solve(eq, sigma)[0].has(pi) if sp.solve(eq, sigma) else None) for n, eq in Sg.items() if n in ("Sg1", "Sg2")}
    ck.check("C3 the Gauss/Milgrom closures fix sigma with a 1/pi (Sg1: a0/(2 pi G), Sg2: a0/(4 pi G))", all(sg_has_pi.values()), str(sg_has_pi))
    results["checks"] = ck.records
    verdict = ("SCOPED NO-GO: no declared (J, Sg) pair gives k2 = 1/4; the two-sided average abar = rho c^2/(3 sigma) is pi-free, but every declared"
               " sigma-closure is a Gauss/Israel field or budget condition that carries pi (binding failure: the Gauss 2 pi in Sigma_M; pi-weight)."
               " The natural MOND-critical wall gives k2 = 2 pi/3 (a0 = c H_L/2, kappa = 1.447)." if not S["target_hits"]
               else "CANDIDATE HIT -- apply the menu-selection rule")
    log("\nVERDICT R2: " + verdict)
    results["verdict"] = verdict
else:
    log("CFG264 R2 -- MUTATE run (separate outputs)")
    log("=" * 100)
    _, base = run_menu()
    bmap = {r["system"]: [s.get("k2") for s in r.get("solutions", [])] for r in base}
    results["mutations"] = {}
    # M1: one-sided instead of two-sided in J1
    _, t1 = run_menu(mode="M1_one_sided")
    S1 = report(t1, "M1 one-sided (J1 uses a_out instead of abar)")
    ch = [r["system"] for r in t1 if r["system"].startswith("J1+") and [s.get("k2") for s in r.get("solutions", [])] != bmap.get(r["system"])]
    ck.check("M1 one-sided instead of two-sided changes the J1 rows", len(ch) > 0, str(ch))
    j1 = [s for r in t1 if r["system"] == "J1+Sg1" for s in r.get("solutions", []) if "k2" in s]
    log(f"   J1+Sg1 one-sided: {[s['k2'] for s in j1]}  (two-sided: 2*pi/3)")
    results["mutations"]["M1"] = dict(summary=S1, changed=ch)
    # M2: D = 5
    _, t2 = run_menu(D=5)
    S2 = report(t2, "M2 D = 4 -> 5")
    ch2 = [r["system"] for r in t2 if [s.get("k2") for s in r.get("solutions", [])] != bmap.get(r["system"])]
    ck.check("M2 D = 5 changes the table", len(ch2) > 0, f"{len(ch2)} systems changed")
    results["mutations"]["M2"] = dict(summary=S2, changed=ch2)
    # M3: pi-free sigma control sigma = q a0/G
    q = sp.Symbol("q", positive=True)
    W, J, Sg = build(mode="M3_piFree_sigma")
    log("\n--- M3 control: sigma = q a0/G (q a free positive number; NOT a declared closure, shows where the pi enters) ---")
    m3 = {}
    for jn, eqJ in J.items():
        try:
            sols = sp.solve([eqJ, Sg["SgQ"]], [sigma, a0], dict=True)
        except Exception:
            sols = []
        ks = []
        for s in sols:
            if a0 in s:
                ks.append(sp.simplify(s[a0]**2 / (c**2 * G * rho)))
        m3[jn] = [str(x) for x in ks]
        log(f"   {jn:<4} k2(q) = {m3[jn]}")
    j1q = sp.sympify(m3["J1"][0], locals={"q": q}) if m3["J1"] else None
    ck.check("M3 J1 (two-sided) with sigma = q a0/G gives the pi-free k2 = 1/(3q): kappa = 1/2 <=> q = 4/3",
             j1q is not None and sp.simplify(j1q - 1 / (3 * q)) == 0 and sp.solve(sp.Eq(j1q, sp.Rational(1, 4)), q) == [sp.Rational(4, 3)])
    j3q = [sp.sympify(x, locals={"q": q}) for x in m3.get("J3", [])]
    ck.check("M3b the one-sided J3 with the same sigma re-introduces pi through the self-gravity term (k2 depends on pi q)",
             all(x.has(pi) for x in j3q) and len(j3q) > 0, str(m3.get("J3")))
    results["mutations"]["M3"] = m3
    results["checks"] = ck.records

ck.summary()
results["n_pass"], results["n_fail"] = ck.n_pass, ck.n_fail
write_json(TAG + "_results.json", results)
_out.close()
sys.exit(0 if ck.n_fail == 0 else 1)
