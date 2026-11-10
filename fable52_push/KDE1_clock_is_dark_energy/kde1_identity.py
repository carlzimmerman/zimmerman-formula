"""KDE1 step R1 (+ KA1, KA2a, KA3): is the briefed candidate the record's AC2s?  Criteria: FROZEN_CRITERIA.md.

Two Lagrangian densities, built by two separate routes, evaluated on the same jets of random polynomial fields in 2+1:

  route K (KDE1, from the brief through QX17's closed forms):
      Q = sqrt(-g^ab d_a tau d_b tau),  P.A = -P^a d_a ln Q,  Pi = (1/sqrt-g) d_a(sqrt-g P^a) + P^a d_a ln Q
      L_K = sqrt-g [ Q^2/2 - V(tau) + P.A - W(K|P|; a0(tau)) - gam max(Pi,0)^2/2 + lam n.P ],  a0 = kappa sqrt(G V)
  route C (AC2s, from AC2's ACTION.md with AC6's switch, through Christoffel symbols):
      X = -(1/2) g^ab d_a phi d_b phi,  n_a = -d_a phi/sqrt(2X),  A_a = n^b nabla_b n_a,  D.P = h^ac nabla_a P_c
      L_C = sqrt-g [ X - V(phi) + P.A - W(p, a0) - (gam/2)(D.P)^2 [D.P >= 0] + lam_P n.P ],  a0^2 = xi G V, xi = kappa^2

Usage:  python3 kde1_identity.py            (main: R1, KA1, KA2a, KA3; writes kde1_identity.out / .json)
        python3 kde1_identity.py M1|M2|M3|M4 (MUTATE twin of route C; writes kde1_identity_MUTATE_<Mi>.out / .json)
Test units: K = 1/2, G = K/(4 pi), kappa = 1/2, Lstar = 7/10 (the identity is algebraic; units do not enter it).
"""
import sys, json, random, time
import sympy as sp
import mpmath as mp

MUT = sys.argv[1] if len(sys.argv) > 1 else None
assert MUT in (None, "M1", "M2", "M3", "M4")
mp.mp.dps = 50
t0 = time.time()
D = 3
X = sp.symbols("t x y")
Kv = mp.mpf(1) / 2
Gv = Kv / (4 * mp.pi)
kap = mp.mpf(1) / 2
xi = kap**2                                  # AC2's xi read as kappa^2 (KDE1's a0 = kappa sqrt(G V))
Lst = mp.mpf(7) / 10
gam = Kv * Lst**2 / 2                        # gamma_L = K Lstar^2/2 (QX17) = gamma (AC2)
MUK, LAM = mp.mpf(7) / 10, mp.mpf(3) / 10    # KA1 / M4: action (A)'s dust constant and Lambda (test values)
A0_CAN, A0_ALT = mp.mpf("9.3603e-11"), mp.mpf("1.1312e-10")
VCOEF = (mp.mpf(13) / 10, mp.mpf(-1) / 5, mp.mpf(3) / 20)   # V(tau) = v0 + v1 tau + v2 tau^2 > 0 for all tau

def W(p, a0):
    return (a0**2 / Kv) * (-p / a0 - mp.log(1 - p / a0))

# ------------------------------------------------------------------ random fields (as QX17), jets at points
def rpoly(rng, scale):
    t, x, y = X
    mons = [1, t, x, y, t*x, x*y, t*y, x**2, y**2, t**2]
    return sum(sp.Rational(rng.randint(-9, 9), 10) * scale * m for m in mons)

def make_config(seed):
    rng = random.Random(seed)
    eta = sp.diag(-1, 1, 1)
    g = sp.zeros(D, D)
    for a in range(D):
        for b in range(a, D):
            g[a, b] = g[b, a] = eta[a, b] + rpoly(rng, sp.Rational(1, 10))
    tau = X[0] + rpoly(rng, sp.Rational(1, 10))
    Vv = [rpoly(rng, sp.Rational(1, 20)) + (sp.Rational(1, 20) if a == 1 else 0) for a in range(D)]
    lamf = rpoly(rng, 1)
    pts = [tuple(sp.Rational(rng.randint(-30, 30), 100) for _ in range(D)) for _ in range(2)]
    return g, tau, Vv, lamf, pts

def jets(g, tau, Vv, lamf, pt):
    """numeric jets at pt: g, dg[c], tau, dtau, ddtau, P_a, dP[a][b] = d_b P_a, lam.  P = h.V built numerically,
    its first derivatives by mpmath differentiation of that numerical P (n.P = 0 then holds in a neighbourhood)."""
    sub = dict(zip(X, pt))
    gl = [[sp.lambdify(X, g[a, b], "mpmath") for b in range(D)] for a in range(D)]
    tl = sp.lambdify(X, tau, "mpmath")
    dtl = [sp.lambdify(X, sp.diff(tau, X[a]), "mpmath") for a in range(D)]
    Vl = [sp.lambdify(X, Vv[a], "mpmath") for a in range(D)]
    def P_at(*q):
        G = mp.matrix([[gl[a][b](*q) for b in range(D)] for a in range(D)])
        Gi = G**-1
        dt = [dtl[a](*q) for a in range(D)]
        Q = mp.sqrt(-sum(Gi[a, b] * dt[a] * dt[b] for a in range(D) for b in range(D)))
        n = [-dt[a] / Q for a in range(D)]
        nu = [sum(Gi[a, b] * n[b] for b in range(D)) for a in range(D)]
        V = [Vl[a](*q) for a in range(D)]
        nV = sum(nu[a] * V[a] for a in range(D))
        return [V[a] + n[a] * nV for a in range(D)]
    q0 = [rq(c) for c in pt]
    J = {}
    J["g"] = mp.matrix([[mp.mpf(sp.N(g[a, b].subs(sub), 60)) for b in range(D)] for a in range(D)])
    J["dg"] = [mp.matrix([[mp.mpf(sp.N(sp.diff(g[a, b], X[c]).subs(sub), 60)) for b in range(D)] for a in range(D)])
               for c in range(D)]
    J["tau"] = mp.mpf(sp.N(tau.subs(sub), 60))
    J["dt"] = [mp.mpf(sp.N(sp.diff(tau, X[a]).subs(sub), 60)) for a in range(D)]
    J["ddt"] = [[mp.mpf(sp.N(sp.diff(tau, X[a], X[b]).subs(sub), 60)) for b in range(D)] for a in range(D)]
    J["P"] = P_at(*q0)
    J["dP"] = [[None] * D for _ in range(D)]
    for b in range(D):
        for a in range(D):
            J["dP"][a][b] = mp.diff(lambda *q: P_at(*q)[a], q0, tuple(1 if k == b else 0 for k in range(D)))
    J["lam"] = mp.mpf(sp.N(lamf.subs(sub), 60))
    return J

def rq(c):
    c = sp.Rational(c)
    return mp.mpf(int(c.p)) / int(c.q)

def Vfun(t, scale):
    return scale * (VCOEF[0] + VCOEF[1] * t + VCOEF[2] * t**2)

# ------------------------------------------------------------------ route K: QX17's closed forms
def route_K(J, scale, kinetic="canonical"):
    G, dG, dt, ddt, P, dP, lam = J["g"], J["dg"], J["dt"], J["ddt"], J["P"], J["dP"], J["lam"]
    Gi = G**-1
    detg = mp.det(G)
    sg = mp.sqrt(-detg)
    dGi = [-Gi * dG[c] * Gi for c in range(D)]
    Q2 = -sum(Gi[a, b] * dt[a] * dt[b] for a in range(D) for b in range(D))
    Q = mp.sqrt(Q2)
    dQ2 = [-sum(dGi[c][a, b] * dt[a] * dt[b] for a in range(D) for b in range(D))
           - 2 * sum(Gi[a, b] * ddt[a][c] * dt[b] for a in range(D) for b in range(D)) for c in range(D)]
    dl = [dQ2[c] / (2 * Q2) for c in range(D)]
    Pu = [sum(Gi[a, b] * P[b] for b in range(D)) for a in range(D)]
    dlnsg = [sum(Gi[a, b] * dG[c][a, b] for a in range(D) for b in range(D)) / 2 for c in range(D)]
    divP = sum(dGi[a][a, b] * P[b] + Gi[a, b] * dP[b][a] + Gi[a, b] * P[b] * dlnsg[a]
               for a in range(D) for b in range(D))
    Pdl = sum(Pu[a] * dl[a] for a in range(D))
    PA = -Pdl
    Pi = divP + Pdl
    p = Kv * mp.sqrt(sum(Pu[a] * P[a] for a in range(D)))
    n = [-dt[a] / Q for a in range(D)]
    nP = sum(Gi[a, b] * n[a] * P[b] for a in range(D) for b in range(D))
    if kinetic == "canonical":
        V = Vfun(J["tau"], scale)
        a0 = kap * mp.sqrt(Gv * V)
        Lclock = Q2 / 2 - V
    else:                                     # KA1: action (A)'s dust term and Lambda, constant a0
        a0 = kap * mp.sqrt(Gv * Vfun(0, scale))
        Lclock = (-2 * LAM + 2 * MUK**2 * (Q - 1)**2) / (4 * Kv)
    stiff = gam * max(Pi, 0)**2 / 2
    return sg * (Lclock + PA - W(p, a0) - stiff + lam * nP), {"Pi": Pi, "PA": PA, "p": p, "a0": a0}

# ------------------------------------------------------------------ route C: Christoffel symbols (AC2 / AC6)
def route_C(J, scale, variant="AC2s", clock="canonical"):
    G, dG, ph, dph, ddph, P, dP, lam = J["g"], J["dg"], J["tau"], J["dt"], J["ddt"], J["P"], J["dP"], J["lam"]
    Gi = G**-1
    sg = mp.sqrt(-mp.det(G))
    # Gamma^a_{bc} = (1/2) g^{ad} (d_b g_{dc} + d_c g_{db} - d_d g_{bc}),  dG[c][a,b] = d_c g_ab
    Gam = [[[sum(Gi[a, d] * (dG[b][d, c] + dG[c][d, b] - dG[d][b, c]) for d in range(D)) / 2
             for c in range(D)] for b in range(D)] for a in range(D)]
    X2 = -sum(Gi[a, b] * dph[a] * dph[b] for a in range(D) for b in range(D))      # 2X
    Xk = X2 / 2
    s = mp.sqrt(X2)
    dGi = [-Gi * dG[c] * Gi for c in range(D)]
    dX2 = [-sum(dGi[c][a, b] * dph[a] * dph[b] for a in range(D) for b in range(D))
           - 2 * sum(Gi[a, b] * ddph[a][c] * dph[b] for a in range(D) for b in range(D)) for c in range(D)]
    ds = [dX2[c] / (2 * s) for c in range(D)]
    n = [-dph[a] / s for a in range(D)]
    dn = [[-ddph[a][b] / s + dph[a] * ds[b] / s**2 for b in range(D)] for a in range(D)]     # d_b n_a
    cov_n = [[dn[a][b] - sum(Gam[c][b][a] * n[c] for c in range(D)) for b in range(D)] for a in range(D)]  # nabla_b n_a
    nu = [sum(Gi[a, b] * n[b] for b in range(D)) for a in range(D)]
    A = [sum(nu[b] * cov_n[a][b] for b in range(D)) for a in range(D)]
    PA = sum(Gi[a, b] * P[a] * A[b] for a in range(D) for b in range(D))
    cov_P = [[dP[c][a] - sum(Gam[d][a][c] * P[d] for d in range(D)) for c in range(D)] for a in range(D)]  # nabla_a P_c
    h = [[Gi[a, c] + nu[a] * nu[c] for c in range(D)] for a in range(D)]
    DP = sum(h[a][c] * cov_P[a][c] for a in range(D) for c in range(D))
    p = Kv * mp.sqrt(sum(Gi[a, b] * P[a] * P[b] for a in range(D) for b in range(D)))
    nP = sum(nu[a] * P[a] for a in range(D))
    V = Vfun(ph, scale)
    if variant == "M3":
        a0 = mp.sqrt(xi * Gv * (Xk + V))
    elif clock == "dust":
        a0 = kap * mp.sqrt(Gv * Vfun(0, scale))
    else:
        a0 = mp.sqrt(xi * Gv * V)
    if variant == "M1":
        stiff = (gam / 2) * DP**2
    elif variant == "M2":
        stiff = (gam / 2) * (max(DP + X2, 0)**2 - X2**2)
    else:
        stiff = (gam / 2) * DP**2 if DP >= 0 else mp.mpf(0)
    if clock == "dust":                       # action (A) (QX17 section 0), written from the RESULT text
        Lclock = (-2 * LAM + 2 * MUK**2 * (s - 1)**2) / (4 * Kv)
    else:
        Lclock = Xk - V
    return sg * (Lclock + PA - W(p, a0) - stiff + lam * nP), {"DP": DP, "PA": PA, "p": p, "a0": a0}

def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), mp.mpf(10)**-45)

# ------------------------------------------------------------------ R1 (and twins)
out = {"mutate": MUT, "criteria": "FROZEN_CRITERIA.md", "units": "K = 1/2, G = K/(4 pi), kappa = 1/2, Lstar = 7/10",
       "R1": {}, "known_answers": {}}
lines = []
def say(s):
    print(s, flush=True); lines.append(s)

say(f"KDE1 identity run, mutate = {MUT}")
pts_cache = []
need = 8
seed = 0
while True:
    seed += 1
    g, tau, Vv, lamf, pts = make_config(seed)
    for pt in pts:
        J = jets(g, tau, Vv, lamf, pt)
        pts_cache.append((seed, pt, J))
    npos = sum(1 for (_, _, J) in pts_cache if route_K(J, 1)[1]["Pi"] > 0)
    nneg = len(pts_cache) - npos
    if (npos >= need and nneg >= need) or seed >= 400:
        break
say(f"seeds used: 1..{seed}; points {len(pts_cache)}: Pi > 0 on {npos}, Pi < 0 on {nneg}")

variant = MUT if MUT in ("M1", "M2", "M3") else "AC2s"
clock = "dust" if MUT == "M4" else "canonical"
for foot, a0f in (("canonical", A0_CAN), ("alt", A0_ALT)):
    scale = (a0f / A0_CAN)**2
    rows, skipped = [], 0
    for (sd, pt, J) in pts_cache:
        LK, iK = route_K(J, scale)
        if not (iK["p"] < iK["a0"]):
            skipped += 1
            continue
        LC, iC = route_C(J, scale, variant=variant, clock=clock)
        rows.append({"seed": sd, "pt": [str(c) for c in pt], "Pi": mp.nstr(iK["Pi"], 12), "DP": mp.nstr(iC["DP"], 12),
                     "L_K": mp.nstr(LK, 20), "L_C": mp.nstr(LC, 20), "rel": mp.nstr(rel(LK, LC), 5),
                     "rel_PA": mp.nstr(rel(iK["PA"], iC["PA"]), 5), "rel_Pi": mp.nstr(rel(iK["Pi"], iC["DP"]), 5),
                     "branch": "Pi>0" if iK["Pi"] > 0 else "Pi<0"})
    rmax = max(mp.mpf(r["rel"]) for r in rows)
    rpos = max((mp.mpf(r["rel"]) for r in rows if r["branch"] == "Pi>0"), default=mp.mpf(0))
    rneg = max((mp.mpf(r["rel"]) for r in rows if r["branch"] == "Pi<0"), default=mp.mpf(0))
    npos_f = sum(1 for r in rows if r["branch"] == "Pi>0")
    nneg_f = len(rows) - npos_f
    if rmax <= mp.mpf("1e-30") and npos_f >= need and nneg_f >= need:
        verdict = "IDENTICAL"
    elif rmax > mp.mpf("1e-6"):
        verdict = "DIFFERENT"
    else:
        verdict = "UNDECIDED"
    out["R1"][foot] = {"points_used": len(rows), "skipped_p_ge_a0": skipped, "n_Pi_pos": npos_f, "n_Pi_neg": nneg_f,
                       "max_rel": mp.nstr(rmax, 5), "max_rel_Pi_pos": mp.nstr(rpos, 5),
                       "max_rel_Pi_neg": mp.nstr(rneg, 5), "verdict": verdict, "rows": rows}
    say(f"R1 [{foot}] route K (KDE1) vs route C ({'AC2s' if MUT is None else 'twin ' + MUT}): "
        f"{len(rows)} points (Pi>0 {npos_f}, Pi<0 {nneg_f}, skipped {skipped}); max rel {mp.nstr(rmax, 4)} "
        f"(Pi>0 {mp.nstr(rpos, 4)}, Pi<0 {mp.nstr(rneg, 4)}) -> {verdict}")
    say(f"    worst P.A rel {mp.nstr(max(mp.mpf(r['rel_PA']) for r in rows), 4)}, "
        f"worst Pi vs D.P rel {mp.nstr(max(mp.mpf(r['rel_Pi']) for r in rows), 4)}")

if MUT is not None:
    bites = all(out["R1"][f]["verdict"] == "DIFFERENT" for f in out["R1"])
    out["bites"] = bites
    say(f"MUTATE {MUT}: {'BITES' if bites else 'DOES NOT BITE'} (R1 must read DIFFERENT on both footings)")
else:
    # ---------------- GR term normalisation
    Gs, Ks = sp.symbols("G K", positive=True)
    Mpl2 = 1 / (8 * sp.pi * Gs)
    gr_ok = sp.simplify((Mpl2 / 2 - 1 / (4 * Ks)).subs(Ks, 4 * sp.pi * Gs)) == 0
    out["known_answers"]["GR_normalisation"] = {"Mpl^2/2 - 1/(4K) at K = 4 pi G": "0" if gr_ok else "nonzero",
                                                "pass": bool(gr_ok)}
    say(f"GR term: Mpl^2/2 = 1/(4K) with Mpl^2 = 1/(8 pi G), K = 4 pi G: {'PASS' if gr_ok else 'FAIL'}")
    # ---------------- KA1: route K with action (A)'s clock terms vs action (A) via route C (Christoffel)
    worst = mp.mpf(0)
    for (sd, pt, J) in pts_cache:
        LK, iK = route_K(J, 1, kinetic="dust")
        if not (iK["p"] < iK["a0"]):
            continue
        LC, _ = route_C(J, 1, variant="AC2s", clock="dust")
        worst = max(worst, rel(LK, LC))
    ka1 = worst <= mp.mpf("1e-30")
    out["known_answers"]["KA1"] = {"what": "KDE1 density with (1/2)Q^2 - V -> mu^2(Q-1)^2/(2K) - Lambda/(2K), a0 const, "
                                   "vs action (A) of QX17 section 0 coded through Christoffel symbols",
                                   "max_rel": mp.nstr(worst, 5), "pass": bool(ka1)}
    say(f"KA1 (replacement gives action (A)): max rel {mp.nstr(worst, 4)} -> {'PASS' if ka1 else 'FAIL'}")
    # ---------------- KA2a: Legendre value at a0 = kappa sqrt(G V), exact
    kp, Gs2, Vs, Ks2, p, Am = sp.symbols("kappa G V K p A", positive=True)
    a0s = kp * sp.sqrt(Gs2 * Vs)
    Ws = (a0s**2 / Ks2) * (-p / a0s - sp.log(1 - p / a0s))
    pst = a0s * (Am / a0s) / (1 + Am / a0s)
    stat = sp.simplify(Am - Ks2 * sp.diff(Ws, p).subs(p, pst))
    u = Am / a0s
    val = sp.simplify(sp.expand_log((pst / Ks2) * Am - Ws.subs(p, pst) - (a0s**2 / Ks2) * (u - sp.log(1 + u)), force=True))
    ka2 = (stat == 0) and (val == 0)
    out["known_answers"]["KA2a"] = {"stationarity_residual": str(stat), "value_residual": str(val), "pass": bool(ka2)}
    say(f"KA2a (Legendre: max_P[P.A - W] = (a0^2/K)[u - ln(1+u)] at a0 = kappa sqrt(G V)): residuals {stat}, {val} "
        f"-> {'PASS' if ka2 else 'FAIL'}")
    # ---------------- KA3: law off, tau Euler-Lagrange (jet route + numerical total derivative) vs Christoffel box
    worst3 = mp.mpf(0)
    Gsym = sp.Matrix(D, D, lambda a, b: sp.Symbol(f"g{min(a,b)}{max(a,b)}"))
    Tc = sp.symbols("T0 T1 T2")
    Tv = sp.Symbol("Tv")
    Q2s = -sum((Gsym.adjugate() / Gsym.det())[a, b] * Tc[a] * Tc[b] for a in range(D) for b in range(D))
    Vs3 = sp.Rational(13, 10) - sp.Rational(1, 5) * Tv + sp.Rational(3, 20) * Tv**2
    Ls = sp.sqrt(-Gsym.det()) * (Q2s / 2 - Vs3)
    jsyms = [Gsym[a, b] for a in range(D) for b in range(a, D)] + list(Tc) + [Tv]
    dLdTv = sp.lambdify(jsyms, sp.diff(Ls, Tv), "mpmath")
    dLdTc = [sp.lambdify(jsyms, sp.diff(Ls, Tc[c]), "mpmath") for c in range(D)]
    for seed3 in (101, 202, 303):
        g, tau, _, _, pts = make_config(seed3)
        gl = [sp.lambdify(X, g[a, b], "mpmath") for a in range(D) for b in range(a, D)]
        dtl = [sp.lambdify(X, sp.diff(tau, X[c]), "mpmath") for c in range(D)]
        tl = sp.lambdify(X, tau, "mpmath")
        jv = lambda *q: [f(*q) for f in gl] + [f(*q) for f in dtl] + [tl(*q)]
        for pt in pts:
            q0 = [rq(c) for c in pt]
            EL = dLdTv(*jv(*q0)) - sum(mp.diff(lambda *q, c=c: dLdTc[c](*jv(*q)), q0,
                                               tuple(1 if k == c else 0 for k in range(D))) for c in range(D))
            J = jets(g, tau, [0, 0, 0], sp.Integer(0), pt)
            Gm, dG = J["g"], J["dg"]
            Gi = Gm**-1
            sg = mp.sqrt(-mp.det(Gm))
            Gam = [[[sum(Gi[a, d] * (dG[b][d, c] + dG[c][d, b] - dG[d][b, c]) for d in range(D)) / 2
                     for c in range(D)] for b in range(D)] for a in range(D)]
            box = sum(Gi[a, b] * (J["ddt"][a][b] - sum(Gam[c][a][b] * J["dt"][c] for c in range(D)))
                      for a in range(D) for b in range(D))
            Vp = VCOEF[1] + 2 * VCOEF[2] * J["tau"]
            ref = sg * (box - Vp)
            worst3 = max(worst3, rel(EL, ref))
    a_, t_, qv = sp.Function("a"), sp.Symbol("t"), sp.Symbol("q")
    th = sp.Function("theta")(t_)
    c0, c1, c2, c3, c4 = sp.symbols("c0:5")
    Vq = c0 + c1 * qv + c2 * qv**2 + c3 * sp.exp(-c4 * qv)
    Lfrw = a_(t_)**3 * (sp.diff(th, t_)**2 / 2 - Vq.subs(qv, th))
    ELfrw = sp.diff(Lfrw, th) - sp.diff(sp.diff(Lfrw, sp.diff(th, t_)), t_)
    target = -a_(t_)**3 * (sp.diff(th, t_, 2) + 3 * sp.diff(a_(t_), t_) / a_(t_) * sp.diff(th, t_)
                           + sp.diff(Vq, qv).subs(qv, th))
    frw_ok = sp.simplify(ELfrw - target) == 0
    ka3 = worst3 <= mp.mpf("1e-30") and frw_ok
    out["known_answers"]["KA3"] = {"what": "law off: tau EL of sqrt(-g)[Q^2/2 - V] = +sqrt(-g)(box tau - V'), 3 configs; "
                                   "FRW: tau'' + 3H tau' + V' = 0", "max_rel": mp.nstr(worst3, 5),
                                   "frw_exact": bool(frw_ok), "pass": bool(ka3)}
    say(f"KA3 (law off = quintessence): EL vs sqrt(-g)(box tau - V') max rel {mp.nstr(worst3, 4)}; FRW exact "
        f"{frw_ok} -> {'PASS' if ka3 else 'FAIL'}")

say(f"runtime {time.time() - t0:.1f} s")
out["runtime_s"] = round(time.time() - t0, 1)
tag = "" if MUT is None else f"_MUTATE_{MUT}"
with open(f"kde1_identity{tag}.json", "w") as f:
    json.dump(out, f, indent=1)
with open(f"kde1_identity{tag}.out", "w") as f:
    f.write("\n".join(lines) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
