#!/usr/bin/env python3
"""V3X W4c: health of v3s's beta = eta = 0 khronon pair plus metric on the Sun's screened background.

Criteria: FROZEN_CRITERIA.md (859c76bec3); amendment A2 (K4 range) in AMENDMENTS.md (0f79edf051).
(a) quadratic action: PN (sympy, 3D, general background) + C5's relativistic local 10-field matrix (C5's source executed
    read-only by AST extraction, nothing edited).
(b) kinetic / gradient operators and the full non-WKB radial spectrum on C6's Route N solar background (lower / upper
    brackets, mpmath), plus C5's local matrix on the Solar-System background at beta = eta = gamma_F = 0.
(c) 3D principal symbol (sympy, all directions) and on the actual background; cones.
Run:  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 v3x_w4c_health.py
      V3X_MUTATE=eta       (eta = gamma_L put back, beta = 0: relativistic part only)
      V3X_MUTATE=noscreen  (gamma_L -> 0: Route N at Lambda = 0, PN parts only)
Units in the PN spectrum: lengths r_M = sqrt(GM/a0), rho~ = K rho r_M / a0 (K = 4 pi G), omega^2 in a0 / r_M.
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, time, ast, resource, subprocess, warnings, hashlib
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
warnings.filterwarnings("ignore")
import numpy as np
import mpmath as mp
import sympy as sp
import multiprocessing as mpc
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
MUT = os.environ.get("V3X_MUTATE", "")
if MUT not in ("", "eta", "noscreen"):
    sys.exit(f"unknown V3X_MUTATE={MUT}")
TAG = f"_MUTATE_{MUT}" if MUT else ""
OUT, CHK, SIDE = [], {}, {}
RES = {"lane": "V3X_v3s_close_undecided", "part": "W4c", "criteria": "859c76bec3", "amendment": "A2 0f79edf051",
       "mutate": MUT or None}
t0 = time.time()
RSS_KILL = 0.85e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def T(s):
    print(f"  [{s}; {time.time() - t0:.0f}s]", file=sys.stderr, flush=True)


def check(name, ok, detail):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), detail=str(detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


def J(*p): return json.load(open(os.path.join(ROOT, *p)))


def forked(fn, *args, label=""):
    """run fn(*args) in a forked child under the RSS watchdog; returns its result dict."""
    ctx = mpc.get_context("fork")
    a, b = ctx.Pipe(False)
    def tgt(conn, *aa):
        try:
            r = fn(*aa)
            r["_rss"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1.0 if sys.platform == "darwin" else 1e-3)
            conn.send(r)
        except Exception as ex:
            conn.send({"_error": f"{type(ex).__name__}: {ex}"})
        conn.close()
    p = ctx.Process(target=tgt, args=(b,) + args)
    t1 = time.time(); p.start(); b.close()
    peak, killed = 0.0, False
    while p.is_alive():
        if a.poll(0.1):
            break
        try:
            r = float(subprocess.run(["ps", "-o", "rss=", "-p", str(p.pid)], capture_output=True, text=True).stdout.strip() or 0) * 1024
        except ValueError:
            r = 0.0
        peak = max(peak, r)
        if r > RSS_KILL:
            p.kill(); killed = True; break
    out = a.recv() if (not killed and a.poll(10.0)) else {"_error": "killed at the RSS line" if killed else "no result"}
    p.join()
    SIDE[label] = dict(rss_bytes=max(peak, out.pop("_rss", 0.0)), seconds=round(time.time() - t1, 1), killed=killed)
    T(f"{label}: {'ok' if '_error' not in out else out['_error']} RSS {SIDE[label]['rss_bytes'] / 1e9:.2f} GB")
    if "_error" in out:
        raise RuntimeError(f"{label}: {out['_error']}")
    return out


GM = 1.32712440018e20; AU = 1.495978707e11; PC = 3.0857e16; c_SI = 2.99792458e8
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FLOOR = {"canonical": 21.7, "alt": 22.9}
def rM_of(a0): return math.sqrt(GM / a0)


P("=" * 100)
P("V3X W4c: health of v3s's beta = eta = 0 khronon pair + metric on the Sun's screened background" + (f"  [MUTATE: {MUT}]" if MUT else ""))
P("kappa = 1/2 FITTED; footings never pooled; adopts nothing; not theory closed.")
P("=" * 100)

# =================================================================================================== (a) PN quadratic action
t, x, y, z = sp.symbols("t x y z", real=True)
X3 = (x, y, z); TX = (t, x, y, z)
K = sp.Symbol("K", positive=True); gam, muK, Cc, eps = sp.symbols("gamma_L mu_K C epsilon", real=True)
wf = sp.Function("w")                                       # W as a function of s = P.P (W(K|P|) = w(P.P))
phib = sp.Function("phib")(x, y, z); rhob = sp.Function("rho_b")(x, y, z)
Pb = [sp.Function(f"Pb{i}")(x, y, z) for i in (1, 2, 3)]
dphi = sp.Function("dphi")(*TX); dsig = sp.Function("dsig")(*TX); dP = [sp.Function(f"dP{i}")(*TX) for i in (1, 2, 3)]
phiF = sp.Function("phi")(*TX); sigF = sp.Function("sigma")(*TX); PF = [sp.Function(f"P{i}")(*TX) for i in (1, 2, 3)]


def grad(f): return [sp.diff(f, v) for v in X3]
def div(V): return sum(sp.diff(V[i], X3[i]) for i in range(3))


def Lag(phi, sig, Pv, withP=True, gv=gam, mv=muK):
    Xi = phi - sp.diff(sig, t) + sum(d ** 2 for d in grad(sig)) / 2
    L = -sum(d ** 2 for d in grad(phi)) / (2 * K) - rhob * phi
    if withP:
        s = sum(p ** 2 for p in Pv)
        L += sum(Pv[i] * sp.diff(Xi, X3[i]) for i in range(3)) - wf(s) - gv / 2 * div(Pv) ** 2
    return L + mv ** 2 * Xi ** 2 / (2 * K)


def wrepl(e):
    """replace w-derivatives evaluated on the background, Subs(d^n w, s-bar), by background functions w_n(x, y, z)."""
    e = e.doit()
    mp_ = {}
    for sb in e.atoms(sp.Subs):
        d = sb.expr
        if isinstance(d, sp.Derivative) and d.expr.func == wf:
            n = sum(c for _, c in d.variable_count)
            mp_[sb] = sp.Function(f"w{n}")(x, y, z)
    return sp.expand(e.xreplace(mp_))


def EL(L, fields):
    """Euler-Lagrange expressions for every field (sympy's euler_equations drops equations that vanish identically,
    so it is re-implemented here with the same rule and every residual kept)."""
    from itertools import combinations_with_replacement
    order = max([sum(c for _, c in d.variable_count) for d in L.atoms(sp.Derivative) if d.expr in fields] + [0])
    out = []
    for f in fields:
        eq = sp.diff(L, f)
        for i in range(1, order + 1):
            for p_ in combinations_with_replacement(TX, i):
                eq += (-1) ** i * sp.diff(sp.diff(L, sp.diff(f, *p_)), *p_)
        out.append(sp.expand(eq))
    return out


pert = {phiF: phib + eps * dphi, sigF: -Cc * t + eps * dsig}
pert.update({PF[i]: Pb[i] + eps * dP[i] for i in range(3)})
DF = [dphi, dsig] + dP
part_a = {}
if MUT != "eta":
    Lfull = Lag(phiF, sigF, PF)
    Lsub = Lfull.subs(pert).doit()
    L2 = wrepl(sp.diff(Lsub, eps, 2).subs(eps, 0) / 2)
    # (a1) EL(L2) = linearised EL(L)
    ELfull = EL(Lfull, [phiF, sigF] + PF)
    lin = [wrepl(sp.diff(e.subs(pert).doit(), eps).subs(eps, 0)) for e in ELfull]
    EL2 = EL(L2, DF)
    r_a1 = [sp.simplify(a_ - b_) for a_, b_ in zip(EL2, lin)]
    ok_a1 = all(r_ == 0 for r_ in r_a1)
    T("a1")
    # (a2) reduced form L2*
    w1, w2 = sp.Function("w1")(x, y, z), sp.Function("w2")(x, y, z)
    H = sp.Matrix(3, 3, lambda i, j: 2 * w1 * (1 if i == j else 0) + 4 * w2 * Pb[i] * Pb[j])
    rho_tau = div(Pb) - muK ** 2 * (phib + Cc) / K
    dXi1 = dphi - sp.diff(dsig, t)
    dPv = sp.Matrix(dP)
    L2s = (-sum(d ** 2 for d in grad(dphi)) / (2 * K) - dXi1 * div(dP) - rho_tau * sum(d ** 2 for d in grad(dsig)) / 2
           - (dPv.T * H * dPv)[0] / 2 - gam / 2 * div(dP) ** 2 + muK ** 2 * dXi1 ** 2 / (2 * K))
    r_a2 = [sp.simplify(e) for e in EL(sp.expand(L2 - L2s), DF)]
    ok_a2 = all(r_ == 0 for r_ in r_a2)
    T("a2")
    # (a3) GR limit: P sector removed
    LGR = Lag(phiF, sigF, PF, withP=False, mv=0)
    L2GR = sp.expand(sp.diff(LGR.subs(pert).doit(), eps, 2).subs(eps, 0) / 2)
    r_a3 = sp.simplify(L2GR + sum(d ** 2 for d in grad(dphi)) / (2 * K))
    ok_a3 = r_a3 == 0 and not L2GR.has(dsig)
    # uniform-background reduction (b's operators): plane waves in L2*'s EL equations
    k_, om_ = sp.symbols("k omega", positive=True)
    r0, MT, ML, th = sp.symbols("rho_0 M_T M_L theta", positive=True)
    amp = sp.symbols("A_phi A_sig A_P1 A_P2 A_P3")
    ph = sp.exp(sp.I * (k_ * z - om_ * t))
    Ph = sp.Matrix([sp.sin(th), 0, sp.cos(th)])
    Hu = K * (MT * sp.eye(3) + (ML - MT) * Ph * Ph.T)
    Lu = (-sum(d ** 2 for d in grad(dphi)) / (2 * K) - dXi1 * div(dP) - r0 * sum(d ** 2 for d in grad(dsig)) / 2
          - (dPv.T * Hu * dPv)[0] / 2 - gam / 2 * div(dP) ** 2 + muK ** 2 * dXi1 ** 2 / (2 * K))
    ELu = EL(sp.expand(Lu), DF)
    subsw = {DF[i]: amp[i] * ph for i in range(5)}
    rows = [sp.expand(sp.simplify(e.subs(subsw).doit() / ph)) for e in ELu]
    Msys = sp.Matrix([[sp.diff(rw, a_) for a_ in amp] for rw in rows])
    W2s = sp.Symbol("W2")
    det = sp.factor(sp.simplify(Msys.det()))
    sol = [sp.simplify(s_) for s_ in sp.solve(sp.Eq(det.subs(om_, sp.sqrt(W2s)), 0), W2s)]
    Mth = 1 / (sp.cos(th) ** 2 / ML + sp.sin(th) ** 2 / MT)
    chi = k_ ** 2 / (K * Mth + gam * k_ ** 2) + muK ** 2 / K
    expect = r0 * (k_ ** 2 / chi - K)
    r_b = [sp.simplify(s_ - expect) for s_ in sol]
    ok_bred = any(r_ == 0 for r_ in r_b)
    r_b0 = sp.simplify(expect.subs(muK, 0) - (K * r0 * (Mth - 1) + r0 * gam * k_ ** 2))
    ok_bred = ok_bred and r_b0 == 0
    part_a = dict(L2_reduced="-|grad dphi|^2/2K - dXi1 div dP - rho_tau |grad dsig|^2/2 - dP.H.dP/2 - (gamma_L/2)(div dP)^2 + mu^2 dXi1^2/2K",
                  a1_residuals=[str(r_) for r_ in r_a1], a2_residuals=[str(r_) for r_ in r_a2], a3_residual=str(r_a3),
                  uniform_roots=[str(s_) for s_ in sol], uniform_residual_vs_H4=[str(r_) for r_ in r_b], mu0_form_residual=str(r_b0))
    check("W4c-a1", ok_a1, f"EL(L2) - linearised EL(L), 5 fields, general 3D background and W: residuals {[str(r_) for r_ in r_a1]}")
    check("W4c-a2", ok_a2, f"L2 - L2* is a null Lagrangian (its EL operator vanishes): residuals {[str(r_) for r_ in r_a2]}")
    check("W4c-a3", ok_a3, f"GR limit (P sector removed): L2 + |grad dphi|^2/2K = {r_a3}; dsig absent: {not L2GR.has(dsig)}")
    check("W4c-b0", ok_bred, f"uniform background: omega^2 roots {[str(s_) for s_ in sol]}; residual vs H4/X3 rho(k^2/chi - K): "
          f"{[str(r_) for r_ in r_b]}; mu = 0 form K rho (M_theta - 1) + rho gamma_L k^2: {r_b0}")
    T("a3, b0")

# =================================================================================================== C5's local matrix (read-only)
C5PY = os.path.join(ROOT, "covariant_push_2026_10_22", "C5_health", "c5_health.py")
C5J = J("covariant_push_2026_10_22", "C5_health", "c5_health_results.json")


def c5_namespace():
    src = open(C5PY).read()
    tree = ast.parse(src)
    want_f = {"trunc", "build_local", "quad_matrix", "mats", "detpoly", "modes", "clusters_of", "summarize", "bg",
              "a0L_of", "bg_named"}
    starts = ("t, x, y, z = ", "eps = ", "w, k = ", "beta, eta, gL, gF, muK, g, P0, th, W1, W2, xi = ", "NAMES = ",
              "Mloc = build_local()", "PN = ", "SYM = ", "ARGS = ", "Mcoef = ", "assert (Mloc", "FM = ")
    code = []
    for nd in tree.body:
        seg = ast.get_source_segment(src, nd)
        if isinstance(nd, ast.FunctionDef) and nd.name in want_f:
            code.append(seg)
        elif isinstance(nd, (ast.Assign, ast.Assert)) and seg.startswith(starts):
            code.append(seg)
    ns = {"sp": sp, "mp": mp, "math": math, "os": os, "json": json, "c_SI": c_SI, "PC": 3.0856775814913673e16,
          "AU": AU, "GMSUN": GM, "A0": dict(FOOT), "KPC": 1e3 * 3.0856775814913673e16, "XI": 1, "SZSGN": 1}
    mp.mp.dps = 120
    exec(compile("\n\n".join(code), C5PY, "exec"), ns)
    return ns, len(code)


XE = {}
for key_, v_ in J("doors_push_2026_10_22", "D7d_screened_q2", "d7d_screened_q2_results.json")["R2_scan"].items():
    if isinstance(v_, dict) and "x_e" in v_:
        XE.setdefault(key_.split("|")[0], []).append(float(v_["x_e"]))


def rel_task(mut_eta):
    ns, ncode = c5_namespace()
    out = {"ncode": ncode}
    Mloc = ns["Mloc"]
    out["hermitian"] = (Mloc - Mloc.H).applyfunc(sp.simplify) == sp.zeros(10, 10)
    a0L = ns["a0L_of"]("canonical", 24)
    mo = ns["modes"](ns["bg"](a0L, 0, 0, 0, 0, 0), mp.mpf(1))                 # Minkowski, beta = eta = gF = mu = 0
    sm = ns["summarize"](mo, mp.mpf(1))
    out["minkowski"] = dict(n_modes=sm["n_modes"], zero_roots=sm["zero_roots"], n_unstable=sm["n_unstable"],
                            n_ghost=sm["n_ghost"], w2_over_k2=[mp.nstr(v, 30) for v in sm["w2_over_k2"]],
                            max_dev=mp.nstr(max(abs(v - 1) for v in sm["w2_over_k2"]), 5))
    rows = {}
    etaf = 1 if mut_eta else 0
    for f in FOOT:
        xe = mp.mpf(max(XE[f]))
        for Lpc in (FLOOR[f], 24, 90):
            par, _ks = ns["bg_named"](f, Lpc, "Solar System", xe, beta_v=0, etaf=etaf)
            par = dict(par); par["gamma_F"] = mp.mpf(0); par["beta"] = mp.mpf(0); par["mu_K"] = mp.mpf(0)
            Lm = Lpc * 3.0856775814913673e16
            for thv in [mp.pi * j / 12 for j in range(13)]:
                par["theta"] = thv
                for rau in (1, 10, 100, 1000):
                    kk = mp.mpf(Lm / (rau * AU))
                    s_ = ns["summarize"](ns["modes"](par, kk), kk)
                    nz = [v for v in s_["w2_over_k2"]]
                    rows[f"{f}|{Lpc}pc|theta={float(thv):.4f}|r={rau}AU"] = dict(
                        n_unstable=s_["n_unstable"], n_ghost=s_["n_ghost"], n_modes=s_["n_modes"], zero_roots=s_["zero_roots"],
                        nonzero_w2_over_k2=[mp.nstr(v, 20) for v in nz],
                        tensor_dev=mp.nstr(max([abs(v - 1) for v in nz] + [mp.mpf(0)]), 5),
                        min_w2=mp.nstr(s_["min_w2"], 10) if s_["min_w2"] is not None else None,
                        g_over_k=mp.nstr(par["g"] / kk, 4))
    out["rows"] = rows
    if mut_eta:                                                            # C5 H7's Solar-System rate, C5's own parameters
        h7 = {}
        for f in FOOT:
            par, ks = ns["bg_named"](f, 24, "Solar System", mp.mpf(max(XE[f])), beta_v=0, etaf=1)
            s_ = ns["summarize"](ns["modes"](par, ks[0]), ks[0])
            m_ = s_["min_w2"]
            rate = mp.sqrt(-m_) * c_SI / (24 * 3.0856775814913673e16) * 3.15576e7 if m_ < 0 else 0
            h7[f] = dict(w2_min=mp.nstr(m_, 10), rate_per_yr=mp.nstr(rate, 8))
        out["H7"] = h7
    return out


part_rel = {}
if MUT != "noscreen":
    rel = forked(rel_task, MUT == "eta", label="relativistic local matrix")
    part_rel = rel
    if MUT == "":
        mk = rel["minkowski"]; c5row = C5J["H4"]["C4-literal (beta=0, eta=0, gF=0, mu=0) | Minkowski"]
        ok_a4 = rel["hermitian"] and mk["n_modes"] == c5row["route1_modes"] and mk["zero_roots"] == c5row["zero_roots"] \
            and float(mk["max_dev"]) <= 1e-50 and mk["n_unstable"] == 0          # 120-digit arithmetic: "exactly" = at working precision and mk["n_ghost"] == 0
        check("W4c-a4", ok_a4, f"C5's 10-field matrix ({rel['ncode']} source blocks executed read-only): Hermitian {rel['hermitian']}; "
              f"Minkowski at beta = eta = gamma_F = 0: {mk['n_modes']} modes + {mk['zero_roots']} omega = 0 roots "
              f"(C5 H4 row: {c5row['route1_modes']} + {c5row['zero_roots']}), non-zero omega^2/k^2 - 1 max {mk['max_dev']} (GR tensors exactly)")
    rows = rel["rows"]
    bad = [k_ for k_, v_ in rows.items() if v_["n_unstable"] or v_["n_ghost"]]
    tdev = max(float(v_["tensor_dev"]) for v_ in rows.values())
    two = all(len(v_["nonzero_w2_over_k2"]) == 2 for v_ in rows.values())
    gk = max(float(v_["g_over_k"]) for v_ in rows.values())
    tmax = max(max(float(mp.mpf(q_)) for q_ in v_["nonzero_w2_over_k2"]) for v_ in rows.values())
    RES["relativistic"] = dict(n_points=len(rows), failing=bad, max_tensor_dev=tdev, all_two_nonzero=two, max_g_over_k=gk,
                               max_nonzero_w2_over_k2=tmax, cT_le_c=bool(tmax <= 1 + 1e-50),
                               zero_roots=sorted(set(v_["zero_roots"] for v_ in rows.values())),
                               sample=dict(list(rows.items())[:3]))
    ok_rel = not bad and tdev <= 1e-10 and two
    for f in FOOT:
        sub = {k_: v_ for k_, v_ in rows.items() if k_.startswith(f + "|")}
        bf = [k_ for k_ in bad if k_.startswith(f + "|")]
        td = max(float(v_["tensor_dev"]) for v_ in sub.values())
        tw = all(len(v_["nonzero_w2_over_k2"]) == 2 for v_ in sub.values())
        mins = [float(v_["min_w2"]) for v_ in sub.values() if v_["min_w2"] is not None]
        check(f"W4c-rel [{f}]", not bf and td <= 1e-10 and tw,
              f"{len(sub)} points (L* floor/24/90 pc, 13 angles, r = 1-1000 AU, g/k <= {max(float(v_['g_over_k']) for v_ in sub.values()):.1e}; "
              f"eta = {'gamma_L' if MUT == 'eta' else 0}): unstable/ghost points {len(bf)}; min omega^2 (L* units) {min(mins):.4e}; "
              f"non-zero roots = 2 tensors at every point {tw}, max |omega^2/k^2 - 1| {td:.1e}")
    if MUT == "eta":
        for f in FOOT:
            got = mp.mpf(rel["H7"][f]["w2_min"]); want = mp.mpf(C5J["H7"]["solar_system_beta0"][f]["w2_min_Lstar_units"])
            check(f"W4c-H7 [{f}]", abs(got / want - 1) <= 1e-3,
                  f"C5 H7 Solar-System rate reproduced: omega^2_min {mp.nstr(got, 8)} vs C5 {mp.nstr(want, 6)} (rel {mp.nstr(abs(got / want - 1), 2)}); "
                  f"rate {rel['H7'][f]['rate_per_yr']} /yr (C5 {C5J['H7']['solar_system_beta0'][f]['growth_rate_per_yr']})")

# =================================================================================================== (b) PN spectrum
import v3x_solver as V
S6 = V.S
X3J = J("rebuild_2026_10_22", "X3_switched_stiffness", "x3_switched_stiffness_results.json")["D2"]["galactic"]
d7b = J("doors_push_2026_10_22", "D7b_cassini_Q2", "d7b_cassini_q2_results.json")
GE = {f: d7b["grid"][f]["none"]["E2"]["ge_total"] for f in FOOT}
GRES = (30, 48)


def bg_task(Lam_run, xe):
    g = V.grid(Lam_run, GRES)
    U, fin, it = V.solve_v(g, Lam_run, xe, mu=1e-12, polish=3)
    return dict(U=U.tolist(), fin=float(fin), it=int(it))


def background(f):
    A0 = FOOT[f]; rM = rM_of(A0); xe = GE[f] / A0; Lam = 24 * PC / rM
    Lam_run = 0.0 if MUT == "noscreen" else Lam
    r = forked(bg_task, Lam_run, xe, label=f"background {f}")
    g = V.grid(Lam_run, GRES)
    U = np.array(r["U"])
    CT = np.broadcast_to(g.ct, (g.Nr, g.Nt)); ST = np.broadcast_to(g.st, (g.Nr, g.Nt))
    dpr, dpt, _ = S6.dP(xe, CT, ST, U[1], U[2])
    rdiv = np.gradient(dpr, g.x, axis=0, edge_order=2) + 2 * dpr + dpt @ g.D.T
    rho = rdiv / g.r[:, None]                                    # rho~ = K rho r_M / a0 (Sun's response)
    vr = xe * CT + U[1]; vt = -xe * ST + U[2]
    vm = np.sqrt(vr ** 2 + vt ** 2)
    conv = lambda m_sun_pc3: 4 * math.pi * GM * m_sun_pc3 / PC ** 3 * rM / A0
    return dict(g=g, rho=rho, vm=vm, vr=vr, vt=vt, Lam=Lam, xe=xe, rM=rM, A0=A0, fin=r["fin"], it=r["it"],
                rgal_lo=conv(X3J[f]["min_box"]), rgal_hi=conv(X3J[f]["at_sun"]))


DPS = 40


def mpf_list(a): return [mp.mpf(float(v)) for v in a]


def tridiag(rf, rc, af, ac, l, inner):
    """quadratic form of int (a f'^2 + a l(l+1) f^2/r^2) r^2 dr: FV on cells; outer Dirichlet; inner Neumann or Dirichlet."""
    n = len(rc)
    d = [mp.mpf(0)] * n; e = [mp.mpf(0)] * (n - 1)
    for k in range(1, n):
        c = af[k] * rf[k] ** 2 / (rc[k] - rc[k - 1])
        d[k - 1] += c; d[k] += c; e[k - 1] -= c
    d[n - 1] += af[n] * rf[n] ** 2 / (rf[n] - rc[n - 1])
    if inner == "dirichlet":
        d[0] += af[0] * rf[0] ** 2 / (rc[0] - rf[0])
    for i in range(n):
        d[i] += ac[i] * l * (l + 1) * (rf[i + 1] - rf[i])
    return d, e


def tri_inv(d, e):
    """dense inverse of a symmetric tridiagonal matrix (Thomas per column)."""
    n = len(d)
    Minv = mp.matrix(n, n)
    for j in range(n):
        cp = [mp.mpf(0)] * n; dp = [mp.mpf(0)] * n
        for i in range(n):
            a_ = e[i - 1] if i > 0 else 0
            den = d[i] - (a_ * cp[i - 1] if i > 0 else 0)
            cp[i] = (e[i] / den) if i < n - 1 else 0
            rhs = (1 if i == j else 0) - (a_ * dp[i - 1] if i > 0 else 0)
            dp[i] = rhs / den
        xs = [mp.mpf(0)] * n
        xs[n - 1] = dp[n - 1]
        for i in range(n - 2, -1, -1):
            xs[i] = dp[i] - cp[i] * xs[i + 1]
        for i in range(n):
            Minv[i, j] = xs[i]
    return Minv


def spectrum(rho_f, rho_c, rf, rc, l, gam_, M, inner, dps, nlow=5):
    """lower/upper-bracket radial problem: returns eigen summaries of the kinetic (A^-1) and gradient (V) matrices and omega^2."""
    with mp.workdps(dps):
        rf = mpf_list(rf); rc = mpf_list(rc); af = mpf_list(rho_f); ac = mpf_list(rho_c)
        n = len(rc)
        Vol = [(rf[i + 1] ** 3 - rf[i] ** 3) / 3 for i in range(n)]
        sq = [mp.sqrt(v) for v in Vol]
        dA, eA = tridiag(rf, rc, af, ac, l, inner)
        dL, eL = tridiag(rf, rc, [mp.mpf(1)] * (n + 1), [mp.mpf(1)] * n, l, inner)
        dA = [dA[i] / Vol[i] for i in range(n)]; eA = [eA[i] / (sq[i] * sq[i + 1]) for i in range(n - 1)]
        dL = [dL[i] / Vol[i] for i in range(n)]; eL = [eL[i] / (sq[i] * sq[i + 1]) for i in range(n - 1)]
        gam_ = mp.mpf(gam_); M = mp.mpf(M)
        Linv = tri_inv(dL, eL)
        Vh = Linv * (M - 1)
        for i in range(n):
            Vh[i, i] += gam_
        Vh = (Vh + Vh.T) / 2
        Ainv = tri_inv(dA, eA); Ainv = (Ainv + Ainv.T) / 2
        evAinv = sorted(mp.eigsy(Ainv, eigvals_only=True))
        evV = sorted(mp.eigsy(Vh, eigvals_only=True))
        out = dict(n=n, kin_min=mp.nstr(evAinv[0], 12), kin_max=mp.nstr(evAinv[-1], 12),
                   A_min=mp.nstr(1 / evAinv[-1], 15), A_max=mp.nstr(1 / evAinv[0], 15),
                   V_min=mp.nstr(evV[0], 20), V_max=mp.nstr(evV[-1], 12))
        A_pd = evAinv[0] > 0 and (1 / evAinv[-1]) > mp.mpf(10) ** -20 * (1 / evAinv[0])
        V_pd = evV[0] > 0 and evV[0] > mp.mpf(10) ** -20 * evV[-1]
        out["A_pd"] = bool(A_pd); out["V_pd"] = bool(V_pd); out["V_ge_gamma"] = bool(evV[0] >= gam_ * (1 - mp.mpf(10) ** -12))
        if A_pd:
            # Cholesky of the tridiagonal A-hat: L bidiagonal (l0 diag, l1 sub)
            l0 = [mp.mpf(0)] * n; l1 = [mp.mpf(0)] * (n - 1)
            for i in range(n):
                v = dA[i] - (l1[i - 1] ** 2 if i > 0 else 0)
                l0[i] = mp.sqrt(v)
                if i < n - 1:
                    l1[i] = eA[i] / l0[i]
            # C^-1 = L^-1 V^-1 L^-T, V^-1 = L-hat (gamma L-hat + (M-1) I)^-1 with L-hat = tridiag(dL, eL)
            Binv = tri_inv([gam_ * v + (M - 1) for v in dL], [gam_ * v for v in eL])
            Vinv = mp.matrix(n, n)
            for i in range(n):
                for j in range(n):
                    s_ = dL[i] * Binv[i, j]
                    if i > 0: s_ += eL[i - 1] * Binv[i - 1, j]
                    if i < n - 1: s_ += eL[i] * Binv[i + 1, j]
                    Vinv[i, j] = s_
            def Linv_apply_cols(Mx):            # L^-1 Mx (forward substitution, bidiagonal)
                R = mp.matrix(n, n)
                for j in range(n):
                    prev = mp.mpf(0)
                    for i in range(n):
                        v = (Mx[i, j] - (l1[i - 1] * prev if i > 0 else 0)) / l0[i]
                        R[i, j] = v; prev = v
                return R
            Y = Linv_apply_cols(Vinv)
            Cinv = Linv_apply_cols(Y.T)             # L^-1 (L^-1 V^-1)^T = L^-1 V^-1 L^-T (V^-1 symmetric)
            Cinv = (Cinv + Cinv.T) / 2
            evC = sorted(mp.eigsy(Cinv, eigvals_only=True), reverse=True)
            w2 = [1 / v for v in evC]               # ascending omega^2
            out["omega2_low"] = [mp.nstr(v, 20) for v in w2[:nlow]]
            out["omega2_min"] = mp.nstr(w2[0], 20); out["omega2_max"] = mp.nstr(w2[-1], 12)
            out["all_positive"] = bool(evC[-1] > 0)
            out["_w2"] = w2[:nlow]
            # float64 diagonalisation of C itself, beside it (conditioning)
            Lf = np.diag([float(v) for v in l0]) + np.diag([float(v) for v in l1], -1)
            Vf = np.array(Vh.tolist(), dtype=float)
            Cf = Lf.T @ Vf @ Lf
            ef = np.sort(np.linalg.eigvalsh((Cf + Cf.T) / 2))
            out["float64_omega2_low"] = [float(v) for v in ef[:3]]
        else:
            # inertia route: V^1/2 A V^1/2 (V positive definite) has the inertia of A
            Ad = mp.matrix(n, n)
            for i in range(n):
                Ad[i, i] = dA[i]
                if i < n - 1: Ad[i, i + 1] = eA[i]; Ad[i + 1, i] = eA[i]
            Ev, Q = mp.eigsy(Vh)
            Sh = Q * mp.diag([mp.sqrt(v) for v in Ev]) * Q.T
            evS = sorted(mp.eigsy(Sh * Ad * Sh, eigvals_only=True))
            out["omega2_low"] = [mp.nstr(v, 20) for v in evS[:nlow]]
            out["omega2_min"] = mp.nstr(evS[0], 20); out["omega2_max"] = mp.nstr(evS[-1], 12)
            out["all_positive"] = bool(evS[0] > 0)
            out["n_negative"] = int(sum(1 for v in evS if v < 0))
        return out


def grid_r(r_in, r_out, nd):
    nc = int(round(math.log10(r_out / r_in) * nd))
    xf = np.linspace(math.log(r_in), math.log(r_out), nc + 1)
    return np.exp(xf), np.exp(0.5 * (xf[1:] + xf[:-1]))


def interp_rho(rn, prof, rq):
    if np.all(prof > 0):
        return np.exp(np.interp(np.log(rq), np.log(rn), np.log(prof)))
    return np.interp(np.log(rq), np.log(rn), prof)


part_b = {}; part_c = {}
if MUT != "eta":
    # ------------------------------------------------ K3: uniform ball (known answer, W4b reproduced)
    k3 = {}; ok_k3 = True
    for nd in (8, 12, 16):
        rf, rc = grid_r(1e-6, 1.0, nd)
        for l in (0, 1):
            with mp.workdps(DPS):
                n = len(rc)
                rfm, rcm = mpf_list(rf), mpf_list(rc)
                Vol = [(rfm[i + 1] ** 3 - rfm[i] ** 3) / 3 for i in range(n)]
                dL, eL = tridiag(rfm, rcm, [mp.mpf(1)] * (n + 1), [mp.mpf(1)] * n, l, "neumann")
                sq = [mp.sqrt(v) for v in Vol]
                Lh = mp.matrix(n, n)
                for i in range(n):
                    Lh[i, i] = dL[i] / Vol[i]
                    if i < n - 1:
                        Lh[i, i + 1] = Lh[i + 1, i] = eL[i] / (sq[i] * sq[i + 1])
                lam = sorted(mp.eigsy(Lh, eigvals_only=True))
            sp_ = spectrum(np.ones(len(rf)), np.ones(len(rc)), rf, rc, l, 0.5, 2.0, "neumann", DPS)
            with mp.workdps(DPS):
                pred = [1 + 0.5 * v for v in lam[:5]]
                dev = max(abs(a_ / b_ - 1) for a_, b_ in zip(sp_["_w2"], pred))
                bz = (mp.pi if l == 0 else mp.findroot(lambda q: mp.tan(q) - q, 4.49)) ** 2
                bdev = abs(lam[0] / bz - 1)
            k3[f"nd{nd}|l{l}"] = dict(max_rel_dev_vs_exact=mp.nstr(dev, 3), lambda_1=mp.nstr(lam[0], 12), bessel=mp.nstr(bz, 12),
                                      bessel_rel=mp.nstr(bdev, 4))
            ok_k3 &= dev <= mp.mpf(10) ** -25
    bdevs = [[float(k3[f"nd{nd}|l{l}"]["bessel_rel"]) for nd in (8, 12, 16)] for l in (0, 1)]
    ok_k3 &= all(b_[0] > b_[1] > b_[2] for b_ in bdevs)
    V3W4 = J("rebuild_2026_10_22", "V3W_v3s_weak_spots", "w4_health_gw.json")
    xs = np.logspace(-4, 4, 81); kk = np.logspace(-4, 4, 81)
    w2min = min(min((1 + xv) - 1, (1 + xv) ** 2 - 1) + kv ** 2 / 2 for xv in xs for kv in kk)
    rec = V3W4["checks"]["W4-K6"]["detail"].split("= ")[1].split(" ")[0]
    ok_w4b = f"{w2min:.3e}" == rec
    part_b["K3"] = dict(cells=k3, W4K6_recomputed=w2min, W4K6_V3W=rec)
    check("W4c-K3", ok_k3 and ok_w4b, f"uniform ball rho = 1, M = 2 (x = 1), gamma = 0.5: discrete omega^2 = rho(M - 1) + rho gamma lambda_h to "
          f"max {max(float(v['max_rel_dev_vs_exact']) for v in k3.values()):.1e} (<= 1e-25); lambda_1 vs Bessel zeros by rung "
          f"l=0 {bdevs[0]}, l=1 {bdevs[1]} (decreasing); V3W W4-K6 recomputed {w2min:.3e} = V3W {rec}")
    T("K3")

    # ------------------------------------------------ per footing
    for f in FOOT:
        B = background(f)
        g, rho, vm = B["g"], B["rho"], B["vm"]
        Lam = B["Lam"]
        r_out = Lam if MUT != "noscreen" else Lam            # domain [1e-4, L*] in r_M (noscreen: same physical domain)
        dom = g.r <= r_out * (1 + 1e-12)
        gam_ = 0.0 if MUT == "noscreen" else Lam ** 2 / 2
        # background checks
        mono = np.linalg.lstsq(g.Bm[:, :7], rho.T, rcond=None)[0][0]
        hedge = 2 / (Lam ** 2 * g.r)
        sel_g = (g.r <= 1e-3 * Lam) & (np.arange(g.Nr) >= 3)
        sel_f = (g.r <= 0.1 * Lam) & (np.arange(g.Nr) >= 3)
        k4g = float(np.max(np.abs(mono[sel_g] / hedge[sel_g] - 1)))
        k4f = float(np.max(np.abs(mono[sel_f] / hedge[sel_f] - 1)))
        ok_k4 = k4g <= 1e-2
        rho_lo = rho[dom].min(axis=1) + B["rgal_lo"]; rho_hi = rho[dom].max(axis=1) + B["rgal_hi"]
        tot = rho[dom] + B["rgal_lo"]
        imin = np.unravel_index(np.argmin(tot), tot.shape)
        Mlo = float(1 + vm[dom].min()); Mhi = float((1 + vm[dom].max()) ** 2)
        bg_info = dict(Lambda=Lam, x_e=B["xe"], route_N_residual=B["fin"], newton_steps=B["it"], K4_graded_maxdev=k4g,
                       K4_frozen_range_maxdev=k4f, rho_gal_lo=B["rgal_lo"], rho_gal_hi=B["rgal_hi"],
                       min_rho_total=float(tot.min()), at_r_rM=float(g.r[dom][imin[0]]), at_theta=float(g.th[imin[1]]),
                       min_sun_response=float(rho[dom].min()), M_lo=Mlo, M_hi=Mhi,
                       hedgehog_mono_at=[[float(g.r[i]), float(mono[i]), float(hedge[i])] for i in range(3, g.Nr, 40) if dom[i]])
        if MUT != "noscreen":
            check(f"W4c-K4 [{f}]", ok_k4, f"Route N monopole of rho_tau vs hedgehog M/(2 pi L*^2 r) at r <= 1e-3 L* (A2): max rel {k4g:.2e} "
                  f"(<= 1e-2); frozen range r <= 0.1 L*, reported: {k4f:.2e}")
        P(f"  [{f}] background: Route N residual {B['fin']:.1e}; min rho_tau (Sun's response + rho_gal,min) {tot.min():.4e} at r = {bg_info['at_r_rM']:.3e} r_M "
          f"(rho_gal,min {B['rgal_lo']:.4e}); Sun's response min {rho[dom].min():.3e}; M_lo {Mlo:.6f}, M_hi {Mhi:.6f}")
        rn = g.r[dom]
        cases = {}
        def run_case(nd, l, br, inner="neumann", dps=DPS, rout=r_out, nlow=5):
            rf, rc = grid_r(1e-4, rout, nd)
            if rout > r_out * (1 + 1e-9):                    # extended domain (reported)
                dom2 = g.r <= rout * (1 + 1e-12)
                lo2 = rho[dom2].min(axis=1) + B["rgal_lo"]; hi2 = rho[dom2].max(axis=1) + B["rgal_hi"]
                rn2, prof = g.r[dom2], (lo2 if br == "lo" else hi2)
                M_ = float(1 + vm[dom2].min()) if br == "lo" else float((1 + vm[dom2].max()) ** 2)
            else:
                rn2, prof = rn, (rho_lo if br == "lo" else rho_hi)
                M_ = Mlo if br == "lo" else Mhi
            return spectrum(interp_rho(rn2, prof, rf), interp_rho(rn2, prof, rc), rf, rc, l, gam_, M_, inner, dps, nlow)
        LS = range(5)
        for nd in (8, 12, 16):
            for l in LS:
                for br in ("lo", "hi"):
                    cases[f"nd{nd}|l{l}|{br}|neumann"] = run_case(nd, l, br)
            T(f"{f} nd {nd}")
        for l in LS:
            for br in ("lo", "hi"):
                cases[f"nd16|l{l}|{br}|dirichlet"] = run_case(16, l, br, inner="dirichlet")
        prec = {}
        for br in ("lo", "hi"):
            for dps in (30, 60):
                cases[f"nd16|l0|{br}|neumann|dps{dps}"] = c_ = run_case(16, 0, br, dps=dps)
                ref = cases[f"nd16|l0|{br}|neumann"]
                if "omega2_low" in c_ and "omega2_low" in ref:
                    prec[f"{br}|dps{dps}"] = max(abs(mp.mpf(a_) / mp.mpf(b_) - 1) for a_, b_ in zip(c_["omega2_low"], ref["omega2_low"]))
        for l in (0, 1, 2):
            cases[f"nd16|l{l}|lo|neumann|rout10L"] = run_case(16, l, "lo", rout=10 * r_out)
        T(f"{f} spectra")
        # grade (b) PN
        graded = {k_: v_ for k_, v_ in cases.items() if "|dps" not in k_ and "rout10L" not in k_}
        all_pd = all(v_["A_pd"] and v_["V_pd"] for v_ in graded.values())
        all_ge = all(v_["V_ge_gamma"] for v_ in graded.values())
        all_pos = all(v_["all_positive"] for v_ in graded.values())
        negs = [k_ for k_, v_ in graded.items() if not v_["all_positive"]]
        lad = {}
        for l in LS:
            for br in ("lo", "hi"):
                a_ = cases[f"nd12|l{l}|{br}|neumann"]; b_ = cases[f"nd16|l{l}|{br}|neumann"]
                if a_["all_positive"] and b_["all_positive"]:
                    lad[f"l{l}|{br}"] = max(abs(mp.mpf(p_) / mp.mpf(q_) - 1) for p_, q_ in zip(a_["omega2_low"][:3], b_["omega2_low"][:3]))
        lad_ok = bool(lad) and len(lad) == 10 and max(lad.values()) < 0.05
        prec_ok = bool(prec) and len(prec) == 4 and max(prec.values()) <= mp.mpf(10) ** -12
        wmin = min(mp.mpf(v_["omega2_min"]) for v_ in graded.values())
        kinmin = min(mp.mpf(v_["A_min"]) for v_ in graded.values())
        vmin = min(mp.mpf(v_["V_min"]) for v_ in graded.values())
        rho_neg = float(tot.min()) < 0
        lowest = {f"l{l}": [cases[f"nd16|l{l}|{br}|neumann"].get("omega2_low", [None])[0] for br in ("lo", "hi")] for l in LS}
        w_unit = B["A0"] / B["rM"]                                    # s^-2 per unit omega~^2
        for v_ in cases.values():
            v_.pop("_w2", None)
        part_b[f] = dict(background=bg_info, cases=cases, ladder_rel=dict((k_, mp.nstr(v_, 4)) for k_, v_ in lad.items()),
                         precision_rel=dict((k_, mp.nstr(v_, 4)) for k_, v_ in prec.items()), omega2_unit_s2=w_unit,
                         lowest_omega2_by_l_lo_hi=lowest)
        P(f"  [{f}] PN radial spectrum, graded cases {len(graded)}: kinetic (A-hat) and gradient (V-hat) positive definite: {all_pd}; "
          f"min eig A-hat {mp.nstr(kinmin, 6)}, min eig V-hat {mp.nstr(vmin, 12)} (gamma {gam_:.6g}, V >= gamma: {all_ge}); "
          f"min omega^2 {mp.nstr(wmin, 8)} x {w_unit:.3e} s^-2; negative-omega^2 cases {len(negs)}")
        P(f"  [{f}] lowest omega^2 (nd16, lower / upper bracket) by l: " + "; ".join(f"{k_} {mp.nstr(mp.mpf(v_[0]), 6) if v_[0] else '-'} / "
                                                                                 f"{mp.nstr(mp.mpf(v_[1]), 6) if v_[1] else '-'}" for k_, v_ in lowest.items()))
        P(f"  [{f}] ladder 12 -> 16 per decade, lowest three omega^2: max rel change {mp.nstr(max(lad.values()), 4) if lad else '-'} (< 5e-2); "
          f"precision 30 / 60 vs 40 digits: max rel {mp.nstr(max(prec.values()), 4) if prec else '-'} (<= 1e-12); "
          f"float64 lowest (nd16 l0 lo) {cases['nd16|l0|lo|neumann'].get('float64_omega2_low')} vs mpmath {cases['nd16|l0|lo|neumann']['omega2_low'][:3]}")
        P(f"  [{f}] reported: inner Dirichlet (nd16) all positive {all(cases[f'nd16|l{l}|{br}|dirichlet']['all_positive'] for l in LS for br in ('lo', 'hi'))}; "
          f"r_out = 10 L* (l = 0-2, lower) all positive {all(cases[f'nd16|l{l}|lo|neumann|rout10L']['all_positive'] for l in (0, 1, 2))}, "
          f"lowest l0 {cases['nd16|l0|lo|neumann|rout10L']['omega2_min'][:12]}")
        part_b[f]["grade"] = dict(all_pd=all_pd, all_ge_gamma=all_ge, all_positive=all_pos, ladder_ok=lad_ok, precision_ok=prec_ok,
                                  rho_negative=rho_neg, negative_cases=negs[:10], K4=ok_k4 if MUT != "noscreen" else None)
        check(f"W4c-bPN [{f}]", all_pd and all_ge and all_pos and lad_ok and prec_ok and not rho_neg,
              f"A-hat, V-hat PD {all_pd}; V >= gamma {all_ge}; all omega^2 > 0 {all_pos}; ladder < 5e-2 {lad_ok}; precision <= 1e-12 {prec_ok}; "
              f"rho_tau >= 0 on the grid {not rho_neg}")
        # ------------------------------------------------ (c) on the actual background
        nodes = [(i, j) for i in range(0, g.Nr, 6) if dom[i] for j in range(0, g.Nt, 3)]
        nfib = 2000
        ii = np.arange(nfib) + 0.5
        phi_f = np.arccos(1 - 2 * ii / nfib); th_f = np.pi * (1 + 5 ** 0.5) * ii
        dirs = np.stack([np.cos(th_f) * np.sin(phi_f), np.sin(th_f) * np.sin(phi_f), np.cos(phi_f)], 1)
        dev = {1e3: 0.0, 1e6: 0.0}; c2min = np.inf
        for (i, j) in nodes:
            rr = g.r[i]; rho_ij = rho[i, j] + B["rgal_lo"]
            st, ct = g.st[j], g.ct[j]
            pv = vm[i, j]
            ph_ = (B["vr"][i, j] * np.array([st, 0, ct]) + B["vt"][i, j] * np.array([ct, 0, -st])) / pv
            MT_, ML_ = 1 + pv, (1 + pv) ** 2
            Hinv = (np.eye(3) - np.outer(ph_, ph_)) / MT_ + np.outer(ph_, ph_) / ML_
            q = np.einsum("ni,ij,nj->n", dirs, Hinv, dirs)
            c2 = gam_ * rho_ij
            c2min = min(c2min, c2)
            for kmag in dev:
                kk_ = kmag / rr
                w2_ = rho_ij * kk_ ** 2 * (gam_ + 1 / (kk_ ** 2 * q)) - rho_ij
                if c2 > 0:
                    dev[kmag] = max(dev[kmag], float(np.max(np.abs(w2_ / (c2 * kk_ ** 2) - 1))))
                else:
                    dev[kmag] = float("inf")
        # exact 9x9 roots on a subset (formula = full system)
        import scipy.linalg as sla
        sub_dev = 0.0
        for (i, j) in nodes[:: max(1, len(nodes) // 12)]:
            rr = g.r[i]; rho_ij = rho[i, j] + B["rgal_lo"]; st, ct = g.st[j], g.ct[j]; pv = vm[i, j]
            ph_ = (B["vr"][i, j] * np.array([st, 0, ct]) + B["vt"][i, j] * np.array([ct, 0, -st])) / pv
            Hm = (1 + pv) * (np.eye(3) - np.outer(ph_, ph_)) + (1 + pv) ** 2 * np.outer(ph_, ph_)
            for xi_ in dirs[::200]:
                kfull = xi_ * 1e3 / rr; kk2 = kfull @ kfull
                # the same system written in length units 1/|xi| (exact rescaling, for conditioning): unit xi, H -> H/|xi|^2,
                # K -> K/|xi|^2, omega -> omega/|xi|.  Unknowns: drho, dv(3), dP(3), dXi, dphi; M0 + omega M1 = 0 (v-bar = 0)
                kv = xi_ / np.linalg.norm(xi_); k2 = 1.0
                M0 = np.zeros((9, 9), complex); M1 = np.zeros((9, 9), complex)
                M1[0, 0] = -1j; M0[0, 1:4] = 1j * rho_ij * kv
                for a_ in range(3):
                    M1[1 + a_, 1 + a_] = -1j; M0[1 + a_, 7] = -1j * kv[a_]; M0[1 + a_, 8] = 1j * kv[a_]
                    M0[4 + a_, 7] = 1j * kv[a_]; M0[4 + a_, 4:7] = -Hm[a_] / kk2 - gam_ * kv[a_] * kv
                M0[7, 0] = 1; M0[7, 4:7] = -1j * kv
                M0[8, 8] = -k2; M0[8, 0] = -1 / kk2
                # exact elimination in 50-digit arithmetic: rows 4-8 carry no omega, so (dP, dXi, dphi) = -B^-1 C drho;
                # rows 0-3 then form a 4x4 standard eigenproblem omega x = E x in (drho, dv)
                with mp.workdps(50):
                    M0m = mp.matrix(M0.tolist())
                    Bm = M0m[4:9, 4:9]; Cm = M0m[4:9, 0:4]
                    Xm = -(mp.inverse(Bm) * Cm)
                    top = M0m[0:4, 0:4] + M0m[0:4, 4:9] * Xm
                    Em = top * mp.mpc(0, -1)                  # (top) x = -omega M1[0:4,0:4] x = i omega x  ->  omega x = -i top x
                    evm = mp.eig(Em, left=False, right=False)
                    ev = np.array([complex(v) for v in evm])
                w2n = np.sort(np.real(ev ** 2))[-1] * kk2
                qq = kfull @ np.linalg.solve(Hm, kfull)
                w2f = rho_ij * kk2 * (gam_ + 1 / qq) - rho_ij
                if w2f != 0:
                    sub_dev = max(sub_dev, abs(w2n / w2f - 1))
        cs2 = gam_ * float(tot.max()) * B["A0"] * B["rM"]
        cs_max = math.sqrt(max(cs2, 0.0))
        hedge_surface = math.sqrt(GM / 6.957e8); hedge_center = math.sqrt(1.5 * GM / 6.957e8)
        part_c[f] = dict(nodes=len(nodes), directions=nfib, c2_min=c2min, deviation_at_xi_1e3_over_r=dev[1e3],
                         deviation_at_xi_1e6_over_r=dev[1e6], formula_vs_9x9_maxrel=sub_dev, cs_max_m_s=cs_max, cs_max_over_c=cs_max / c_SI,
                         hedgehog_cs_solar_surface_m_s=hedge_surface, hedgehog_cs_center_uniform_sun_m_s=hedge_center,
                         with_vbar_370kms_over_c=(370e3 + hedge_center) / c_SI)
        P(f"  [{f}] 3D symbol on the background: {len(nodes)} nodes x {nfib} directions; c^2 min {c2min:.4e} (> 0: {c2min > 0}); "
          f"|omega^2/(c^2 xi^2) - 1| max {dev[1e3]:.2e} at |xi| = 1e3/r, {dev[1e6]:.2e} at 1e6/r; eliminated formula vs full 9x9 roots {sub_dev:.1e}; "
          f"c_s max {cs_max / 1e3:.2f} km/s in the domain ({cs_max / c_SI:.2e} c); hedgehog c_s = sqrt(|Phi_N|): {hedge_surface / 1e3:.0f} km/s at the solar surface, "
          f"{hedge_center / 1e3:.0f} km/s at a uniform Sun's centre; + 370 km/s: {(370e3 + hedge_center) / c_SI:.2e} c")
        okc = c2min > 0 and dev[1e6] < 1e-6 and sub_dev < 1e-6 and cs_max / c_SI < 1
        check(f"W4c-c-num [{f}]", okc, f"c^2 > 0 at every node {c2min > 0}; symbol -> c^2|xi|^2 (dev {dev[1e6]:.1e} at 1e6/r); formula = 9x9 roots ({sub_dev:.1e}); "
              f"c_s/c {cs_max / c_SI:.1e} < 1")
    # ------------------------------------------------ (c) symbolic 3D principal symbol
    if MUT == "":
        xi1, xi2, xi3, v1, v2, v3, h1, h2, h3, G_, rb, Ks, om = sp.symbols("xi1 xi2 xi3 v1 v2 v3 h1 h2 h3 G rho K omega", real=True)
        xiv = sp.Matrix([xi1, xi2, xi3]); vb = sp.Matrix([v1, v2, v3]); Hd = sp.diag(h1, h2, h3)
        Om = om - (vb.T * xiv)[0]
        M = sp.zeros(9, 9)
        M[0, 0] = -sp.I * Om
        for a_ in range(3):
            M[0, 1 + a_] = sp.I * rb * xiv[a_]
            M[1 + a_, 1 + a_] = -sp.I * Om; M[1 + a_, 7] = -sp.I * xiv[a_]; M[1 + a_, 8] = sp.I * xiv[a_]
            M[4 + a_, 7] = sp.I * xiv[a_]
            for b_ in range(3):
                M[4 + a_, 4 + b_] = -Hd[a_, b_] - G_ * xiv[a_] * xiv[b_]
        M[7, 0] = 1
        for a_ in range(3):
            M[7, 4 + a_] = -sp.I * xiv[a_]
        k2s = xi1 ** 2 + xi2 ** 2 + xi3 ** 2
        M[8, 8] = -k2s; M[8, 0] = -Ks
        detM = sp.factor(M.det(method="berkowitz"))
        qH = xi1 ** 2 / h1 + xi2 ** 2 / h2 + xi3 ** 2 / h3
        disp = Om ** 2 - rb * k2s * (G_ + 1 / qH) + Ks * rb
        ratio = sp.factor(sp.cancel(detM / (Om ** 2 * disp)))
        free_om = sp.simplify(sp.diff(ratio, om)) == 0
        lead = sp.limit(sp.simplify((rb * k2s * (G_ + 1 / qH) - Ks * rb).subs({xi1: sp.Symbol("s") * sp.Symbol("e1"), xi2: sp.Symbol("s") * sp.Symbol("e2"),
                                                                                 xi3: sp.Symbol("s") * sp.Symbol("e3")}) / sp.Symbol("s") ** 2), sp.Symbol("s"), sp.oo)
        lead = sp.factor(sp.simplify(lead))
        lead_res = sp.simplify(lead - rb * G_ * (sp.Symbol("e1") ** 2 + sp.Symbol("e2") ** 2 + sp.Symbol("e3") ** 2))
        Qsym = Hd + G_ * xiv * xiv.T
        sm_res = sp.simplify((xiv.T * Qsym.inv() * xiv)[0] - qH / (1 + G_ * qH))
        part_c["symbolic"] = dict(det_over_Omega2_disp=str(ratio), omega_free=free_om, principal_limit=str(lead), principal_residual=str(lead_res),
                                  sherman_morrison_residual=str(sm_res),
                                  reading="roots: omega = v.xi (double: the curl part of dv, absent for v = -grad sigma) and "
                                          "Omega^2 = rho |xi|^2 (gamma_L Theta + 1/(xi.H^-1.xi)) - K rho; principal part Omega^2 = gamma_L Theta rho |xi|^2")
        okS = free_om and lead_res == 0 and sm_res == 0 and ratio != 0
        check("W4c-c-sym", okS, f"3D frozen-coefficient system (9 unknowns, H = diag(h1,h2,h3) in its own frame, arbitrary xi and v-bar): "
              f"det / [Omega^2 (Omega^2 - rho|xi|^2(G + 1/xi.H^-1.xi) + K rho)] = {ratio} (omega-free {free_om}); principal limit "
              f"Omega^2/|xi|^2 -> {lead} (residual {lead_res}); P-symbol H + G xi xi^T: xi.Q^-1.xi residual {sm_res}")
        T("c symbolic")

# =================================================================================================== labels
labels = {}
for f in FOOT:
    lab = {}
    if MUT == "eta":
        rel_ok = CHK.get(f"W4c-rel [{f}]", False)
        lab["b"] = "PASS" if rel_ok else f"FAIL: eta = gamma_L, beta = 0 on the Solar-System background gives omega^2 < 0 (relativistic local matrix)"
        labels[f] = lab; continue
    if MUT == "":
        a_ok = all(CHK.get(k_, False) for k_ in ("W4c-a1", "W4c-a2", "W4c-a3", "W4c-a4"))
        lab["a"] = "PASS: PN L2 derived (a1, a2 residual 0), GR limit exact (a3), C5's local matrix Hermitian with GR's tensors at Minkowski (a4)" if a_ok \
            else "UNDECIDED: " + str([k_ for k_ in ("W4c-a1", "W4c-a2", "W4c-a3", "W4c-a4") if not CHK.get(k_, False)])
    G = part_b.get(f, {}).get("grade", {})
    rel_ok = CHK.get(f"W4c-rel [{f}]", True if MUT == "noscreen" else False)
    pn_ok = CHK.get(f"W4c-bPN [{f}]", False)
    k_ok = CHK.get("W4c-K3", False) and (MUT == "noscreen" or CHK.get(f"W4c-K4 [{f}]", False)) and CHK.get("W4c-b0", MUT == "noscreen")
    rel_bad = bool(RES.get("relativistic", {}).get("failing"))            # omega^2 < 0 or negative Krein in C5's matrix
    if G.get("rho_negative") or not G.get("all_positive", True) or (MUT == "" and rel_bad):
        lab["b"] = f"FAIL: rho_tau < 0 on the solution grid (min {part_b[f]['background']['min_rho_total']:.3e}) / omega^2 < 0 " \
                   f"(cases {len(G.get('negative_cases', []))})"
    elif pn_ok and rel_ok and k_ok:
        lab["b"] = "PASS"
    else:
        lab["b"] = "UNDECIDED: " + str([k_ for k_ in (f"W4c-bPN [{f}]", f"W4c-rel [{f}]", "W4c-K3", f"W4c-K4 [{f}]", "W4c-b0") if not CHK.get(k_, False)])
    cn = CHK.get(f"W4c-c-num [{f}]", False); cs_ = CHK.get("W4c-c-sym", MUT == "noscreen")
    pd_ = G.get("all_pd", False)
    if part_c.get(f, {}).get("c2_min", 1) < 0:
        lab["c"] = "FAIL: c^2 < 0 at a node"
    elif part_c.get(f, {}).get("c2_min", 1) == 0:
        lab["c"] = "UNDECIDED: c^2 = 0 in the domain (no strict hyperbolicity)"
    cT_ok = MUT == "noscreen" or (not RES.get("relativistic", {}).get("failing") and RES.get("relativistic", {}).get("cT_le_c", False))
    if part_c.get(f, {}).get("c2_min", 1) < 0 or part_c.get(f, {}).get("c2_min", 1) == 0:
        pass
    elif cn and cs_ and pd_ and cT_ok:
        lab["c"] = "PASS (constraints instantaneous: C5 criterion A fails, carried)"
    else:
        lab["c"] = "UNDECIDED: " + str([k_ for k_ in (f"W4c-c-num [{f}]", "W4c-c-sym") if not CHK.get(k_, False)] + ([] if pd_ else ["A/V not PD"])
                                       + ([] if cT_ok else ["tensor speed not shown <= c"]))
    labels[f] = lab
    for k_, v_ in lab.items():
        P(f"W4c [{f}] ({k_}): {v_}")
RES["labels"] = labels
RES["part_a"] = part_a; RES["part_b"] = part_b; RES["part_c"] = part_c
if part_rel:
    RES["relativistic_minkowski"] = part_rel.get("minkowski"); RES["relativistic_H7"] = part_rel.get("H7")
n_ok = sum(CHK.values())
P(f"\nW4c COMPLETE: {n_ok}/{len(CHK)} checks PASS")


def clean(o):
    if isinstance(o, dict): return {str(k_): clean(v_) for k_, v_ in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v_) for v_ in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, (mp.mpf,)): return mp.nstr(o, 20)
    return o


json.dump(clean(RES), open(os.path.join(HERE, f"v3x_w4c_health{TAG}.json"), "w"), indent=1, sort_keys=True)
json.dump(clean(SIDE), open(os.path.join(HERE, f"v3x_w4c_health{TAG}_rss.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, f"v3x_w4c_health{TAG}.out"), "w").write("\n".join(OUT) + "\n")
allpass = all(v_.startswith("PASS") for lab in labels.values() for v_ in lab.values())
sys.exit(0 if (n_ok == len(CHK) and allpass) else 1)
