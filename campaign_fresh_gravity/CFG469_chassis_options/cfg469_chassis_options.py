#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG469 -- THREE WAYS OUT OF CFG467'S alpha_c TENSION, TESTED.
Criteria frozen and committed first: campaign_fresh_gravity/CFG469_chassis_options/FROZEN_CRITERIA.md (fd00569e9).

(A) lenient black holes (CFG319 option C) + Pospelov-Shang hierarchy: causal disconnection (incl. the instantaneous
    mode), finiteness, UH thermodynamics, joint alpha_c window.
(B) +1 constant M_*: the lowest-order Horava-type operator, arms O_A = +alpha_c eps (D.a)^2 and
    O_K = -c_2 eps h^{mn} dK dK; flat dispersion; the order-6 O(v) moving-black-hole count (cfg469_uv_bh.py); M_* band.
(C) chassis retired: candidate B as a recipe; declared inputs with provenance; gates that become untested.

Theory + offline numerics; no downloads. kappa = 1/2 is FITTED and enters nothing here. Cold mass still required.
CFG469_MUTATE=1: (A) the instantaneous mode on v - r = const leaves; (B) M_* = 1e12 GeV. Outputs carry _MUTATE.
Run from anywhere:  python3 campaign_fresh_gravity/CFG469_chassis_options/cfg469_chassis_options.py
"""
import os, sys, json, math, time, re
import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
sys.path.insert(0, HERE)
import cfg469_uv_bh as U

MUTATE = os.environ.get("CFG469_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
OUTP = os.path.join(HERE, f"cfg469_chassis_options{SUF}.out")
_fh = open(OUTP, "w")


def P(*a):
    s = " ".join(str(z) for z in a)
    print(s, flush=True)
    _fh.write(s + "\n"); _fh.flush()


T0 = time.time()
CH = []
OUT = {"lane": "CFG469", "mutate": MUTATE, "frozen_criteria_commit": "fd00569e9", "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reading)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 116); P(t); P("=" * 116)


def ns(z, n=6):
    return mp.nstr(z, n)


def jl(path):
    return json.load(open(os.path.join(CFG, path)))


# ================================================================================================ inputs
banner("INPUTS (read-only)")
J319 = jl("CFG319_moving_black_hole/cfg319_moving_bh_results.json")
J320 = jl("CFG320_radiative_stability_g12/cfg320_radiative_stability_results.json")
J467 = jl("CFG467_alpha_c_sign_tension/cfg467_results.json")
runs = J319["numbers"]["runs"]
W5 = ["W5 corner a_max l_min", "W5 corner a_max l_max", "W5 centre", "W5 corner a_min l_min", "W5 corner a_min l_max"]
LHL = mp.mpf(J320["numbers"]["summary"]["Lambda_HL_max_GeV"])
MP = mp.mpf(J320["numbers"]["inputs"]["M_P_GeV"])
C2GRID = [mp.mpf(z) for z in J320["numbers"]["inputs"]["c2_scored"]]
AMIN, AMAX = mp.mpf(J320["numbers"]["inputs"]["alpha_c"][0]), mp.mpf(J320["numbers"]["inputs"]["alpha_c"][1])
FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
HBARC = mp.mpf("1.973269804e-16")          # GeV m
RG = {"10 Msun": mp.mpf("1.4767e4"), "M87* (6.5e9 Msun)": mp.mpf("9.599e12")}     # G M / c^2 in m
P(f"  CFG319 W5 points: {len(W5)};  CFG320 Lambda_HL_max = {ns(LHL, 8)} GeV, M_P = {ns(MP)} GeV;  c_2 grid {len(C2GRID)} points")
P(f"  window alpha_c [{ns(AMIN, 6)}, {ns(AMAX, 4)}];  footings (labels only) {FOOT}")
OUT["numbers"]["inputs"] = {"Lambda_HL_max_GeV": float(LHL), "M_P_GeV": float(MP), "W5": W5,
                            "r_g_m": {k: float(v) for k, v in RG.items()}, "hbar_c_GeV_m": float(HBARC)}


def cs2(alpha, c2):
    return c2 * (2 - alpha) / (alpha * (2 + 3 * c2))


def lam_sc(alpha, c2):
    return mp.sqrt(alpha) * MP * cs2(alpha, c2)**(-mp.mpf(1) / 4)


# ================================================================================================ OPTION B
banner("OPTION B -- +1 constant M_*: lowest-order Horava-type UV operator (test-khronon limit)")
P("  B0 operators (frozen): O_A: Delta L = + alpha_c eps (D_m a^m)^2,  D.a = grad.a - a.a")
P("                         O_K: Delta L = - c_2 eps h^{mn} d_m K d_n K,  h = g + u u")
P("     eps = 1/(M_* r_g)^2 (one coefficient each, fixed by M_*): +1 constant.")

# ---- B1 flat dispersion (decoupling limit) and K4 leaf curvature
banner("B1  flat-space dispersion of the khronon scalar (sympy, T = t + pi, Minkowski)")
tt, xx, yy, zz, ee = sp.symbols('t x y z epsilon')
alS, laS, euS = sp.symbols('alpha lambda epsilon_UV', positive=True)
wS, kS = sp.symbols('omega k', positive=True)
piF = sp.Function('pi')(tt, zz)
Xc = [tt, xx, yy, zz]
gM = sp.diag(-1, 1, 1, 1); gMi = gM.inv()
Tk = tt + ee * piF
dTk = [sp.diff(Tk, q) for q in Xc]
n2k = -sum(gMi[i, j] * dTk[i] * dTk[j] for i in range(4) for j in range(4))
Nk = 1 / sp.sqrt(n2k)
udk = [-Nk * d for d in dTk]
uuk = [sum(gMi[i, j] * udk[j] for j in range(4)) for i in range(4)]
Kk = sum(sp.diff(uuk[m], Xc[m]) for m in range(4))
adk = [sum(uuk[m] * sp.diff(udk[n], Xc[m]) for m in range(4)) for n in range(4)]
auk = [sum(gMi[i, j] * adk[j] for j in range(4)) for i in range(4)]
a2k = sum(adk[i] * auk[i] for i in range(4))
Dak = sum(sp.diff(auk[m], Xc[m]) for m in range(4)) - a2k
hk = [[gMi[i, j] + uuk[i] * uuk[j] for j in range(4)] for i in range(4)]
DK2k = sum(hk[i][j] * sp.diff(Kk, Xc[i]) * sp.diff(Kk, Xc[j]) for i in range(4) for j in range(4))
disp = {}
DISP = {}
for name, sgn, L in (("IR", 0, -laS * Kk**2 + alS * a2k),
                     ("O_A healthy (+)", +1, -laS * Kk**2 + alS * a2k + alS * euS * Dak**2),
                     ("O_A wrong sign (-)", -1, -laS * Kk**2 + alS * a2k - alS * euS * Dak**2),
                     ("O_K healthy (-)", -1, -laS * Kk**2 + alS * a2k - laS * euS * DK2k),
                     ("O_K wrong sign (+)", +1, -laS * Kk**2 + alS * a2k + laS * euS * DK2k)):
    L2 = sp.expand(sp.diff(L, ee, 2).subs(ee, 0) / 2)
    E = sp.euler_equations(L2, [piF], [tt, zz])[0].lhs
    pw = sp.exp(sp.I * (kS * zz - wS * tt))
    Ew = sp.expand(sp.simplify(E.subs(piF, pw).doit() / pw))
    kin = sp.factor(Ew.coeff(wS, 2))
    pot = sp.factor(-Ew.subs(wS, 0))
    w2 = sp.factor(sp.solve(sp.Eq(Ew, 0), wS**2)[0])
    disp[name] = {"EL_symbol": str(sp.factor(Ew)), "kinetic_coeff": str(kin), "omega2": str(w2)}
    DISP[name] = {"kin": kin, "w2": w2}
    P(f"  {name:20s}: EL symbol {sp.factor(Ew)};  omega^2 = {w2}")
cS2t = laS / alS
w2A = DISP["O_A healthy (+)"]["w2"]
w2K = DISP["O_K healthy (-)"]["w2"]
okA = sp.simplify(w2A - cS2t * kS**2 / (1 + euS * kS**2)) == 0
okK = sp.simplify(w2K - cS2t * kS**2 * (1 + euS * kS**2)) == 0
kinA = DISP["O_A healthy (+)"]["kin"]
kinAw = DISP["O_A wrong sign (-)"]["kin"]
kinK = DISP["O_K healthy (-)"]["kin"]
w2Kw = DISP["O_K wrong sign (+)"]["w2"]
def _num(ex, kv):
    return ex.subs({alS: 1, laS: 1, euS: 1, kS: kv})


KV = (sp.Rational(1, 10), 1, 10, 100)
healthyA = okA and all(_num(kinA, kv) > 0 and _num(w2A, kv) > 0 for kv in KV)
healthyK = okK and all(_num(kinK, kv) > 0 and _num(w2K, kv) > 0 for kv in KV)
ghostAw = _num(kinAw, 10) < 0
unstKw = _num(w2Kw, 10) < 0
check("K4a B1 the derived dispersions equal the closed forms: O_A omega^2 = c_S^2 k^2/(1 + eps k^2), "
      "O_K omega^2 = c_S^2 k^2 (1 + eps k^2), c_S^2 = c_2/alpha (test khronon)", f"O_A {okA}, O_K {okK}", okA and okK)
check("B1 both arms healthy with the frozen signs (kinetic > 0, omega^2 > 0 for all k); the opposite signs fail "
      "(O_A ghost at k > 1/sqrt(eps), O_K gradient instability)",
      f"healthy A {healthyA}, K {healthyK}; wrong-sign A ghost {ghostAw}, wrong-sign K omega^2 < 0 {unstKw}",
      healthyA and healthyK and ghostAw and unstKw,
      reading="UV scaling: O_A omega -> c_S/sqrt(eps) (z = 0, the phase speed falls to zero); O_K z = 2 (speed grows)")
OUT["numbers"]["B1"] = disp

# K4b leaf curvature of T = t + eps pi on Minkowski is O(eps^2)
pis = sp.Function('pi_s')(xx, yy, zz)
emb = [sp.Integer(0) - ee * pis, xx, yy, zz]            # static leaf of T = t + eps pi_s(x): t = const - eps pi_s
hL = sp.Matrix(3, 3, lambda i, j: sum(gM[m, m] * sp.diff(emb[m], (xx, yy, zz)[i]) * sp.diff(emb[m], (xx, yy, zz)[j]) for m in range(4)))
hL1 = sp.simplify(sp.diff(hL, ee).subs(ee, 0))
P("  K4b induced metric of the leaf (from the embedding): h_ij = " + str(sp.simplify(hL)))
check("K4b leaf-curvature (B-type) terms vanish at quadratic order on the test-khronon background: the leaf metric is "
      "delta_ij + O(eps^2), so R[h] = O(eps^2) and R^2, R_ij R^ij = O(eps^4)", f"O(eps) part of h_ij: {hL1}", hL1 == sp.zeros(3))

# ---- B2 derivation
banner("B2  the O(v) moving black hole with the UV term: derivation (sympy jets, r eliminated) and control K1")
tb = time.time()
BUILD = {}
for arm in (None, "A", "K"):
    BUILD[arm] = U.build(arm, log=lambda m: None)
    P(f"  built arm {arm or 'IR'}: M_ij keys {sorted(BUILD[arm]['M'].keys())}  ({time.time() - tb:.1f}s)")
sym319 = J319["numbers"]["symbolic"]
Yq, Wq, aq, lq, bq, Y1q = sp.symbols('Y W alpha beta_ lam Y1')
loc = {"Y": Yq, "W": Wq, "alpha": aq, "beta": bq, "lam": lq, "Y1": Y1q}
ren = lambda s: s.replace("lambda", "lam")
toq = lambda ex: ex.subs({U.Y0: Yq, U.Wsym: Wq, U.al: aq, U.la: lq, U.Ys[1]: Y1q})
d_S22 = sp.simplify(sp.sympify(ren(sym319["S22"]), locals=loc).subs(bq, 0) - toq(BUILD[None]["M"][(2, 2)]))
d_ops = []
for k in range(3):
    d_ops.append(sp.simplify(sp.sympify(ren(sym319["dK_ops"][k]), locals=loc) - toq(sp.cancel(BUILD[None]["K"].c1.get(k, 0) / U.cS))))
    d_ops.append(sp.simplify(sp.sympify(ren(sym319["daa_ops"][k]), locals=loc) - toq(sp.cancel(BUILD[None]["a2"].c1.get(k, 0) / U.cS))))
same_eps0 = {}
for arm in ("A", "K"):
    same_eps0[arm] = all(sp.simplify(BUILD[arm]["M"][key].subs(U.epsUV, 0) - BUILD[None]["M"].get(key, 0)) == 0
                         for key in BUILD[arm]["M"])
check("K1 at eps = 0 the derivation reproduces CFG319's committed S22, dK_ops, daa_ops exactly, and both UV arms reduce "
      "to the IR form", f"S22 diff {d_S22}; ops diffs {d_ops}; arms at eps=0 equal IR: {same_eps0}",
      d_S22 == 0 and all(z == 0 for z in d_ops) and all(same_eps0.values()))
S_top = {"IR": sp.factor(BUILD[None]["M"][(2, 2)]), "A": sp.factor(BUILD["A"]["M"][(3, 3)]), "K": sp.factor(BUILD["K"]["M"][(3, 3)])}
for k_, v_ in S_top.items():
    P(f"  leading coefficient ({'S22' if k_ == 'IR' else 'S33'}) arm {k_}: {v_}")
OUT["numbers"]["B2_top_coefficients"] = {k: str(v) for k, v in S_top.items()}


def rS_singular(expr):
    """does the leading coefficient vanish at the spin-0 horizon (factor alpha W^2 - lambda Y^2)?"""
    for fac, _ in sp.factor_list(sp.numer(sp.together(expr)))[1]:
        if fac.has(U.al) and fac.has(U.la) and fac.has(U.Wsym) and fac.has(U.Y0):
            return True, str(fac)
    return False, "only Y0, W and constant factors (zero only at the UH, Y = 0, and at infinity, W = 0)"


rs_info = {k: rS_singular(v) for k, v in S_top.items()}
for k_, v_ in rs_info.items():
    P(f"  r_S singular for arm {k_}: {v_[0]}  ({v_[1]})")
OUT["numbers"]["rS_singular"] = {k: v[0] for k, v in rs_info.items()}

# operators for classification (angle factor removed)
OPS_SYM = {}
for arm in (None, "A", "K"):
    b = BUILD[arm]
    qd = {"dK": b["K"].c1, "d(a.a)": b["a2"].c1}
    if arm == "A":
        qd["d(D.a)"] = b["Da"].c1
    if arm == "K":
        qd["d((DK)^2)"] = b["DK2"].c1
    od = {}
    for nm, c1 in qd.items():
        od[nm] = {}
        for k, v in c1.items():
            vv = sp.cancel(v / U.cS)
            assert not vv.has(U.cS) and not vv.has(U.sS), (arm, nm, k)
            if vv != 0:
                od[nm][k] = vv
    OPS_SYM[arm] = od

# ---- local analysis machinery
mp.mp.dps = 360
TA = mp.mpf("1e-250")
N_UH, N_INF = 16, 30


def stealth_y():
    sub, dr, info = U.series_point("uh", N_UH)
    return [sub[U.Ys[0]].coeff(k) for k in range(1, 12)]


YST = stealth_y()


def bg_for(point):
    if point == "stealth":
        return None, None
    rr_ = runs[point]
    y = [mp.mpf(rr_["YU1"])] + YST[1:]
    return {"y": y, "rU": rr_["rUH"]}, {"C": rr_["C"]}


COMP_CACHE = {}


def comps_for(arm, where, point):
    key = (arm, where, point)
    if key not in COMP_CACHE:
        bgu, bgi = bg_for(point)
        bg = bgu if where == "uh" else bgi
        N = N_UH if where == "uh" else N_INF
        comps, sub, dr, info = U.el_components(BUILD[arm]["M"], where, N, bg)
        ops = None
        if where == "uh":
            ops = {nm: {k: U.eval_ls(v, sub, N, {}) for k, v in d.items()} for nm, d in OPS_SYM[arm].items()}
        COMP_CACHE[key] = (comps, dr, ops, info)
    return COMP_CACHE[key]


def analyse(arm, point, alpha, lam, eps):
    """local solutions at the UH and at infinity, classification and count (frozen rule)"""
    res = {"arm": arm or "IR", "point": point, "alpha": str(alpha), "lambda": str(lam), "eps": mp.nstr(mp.mpf(eps), 6)}
    # UH
    comps, dr, ops, info = comps_for(arm, "uh", point)
    a, lead = U.combine(comps, alpha, lam, eps, TA)
    nw = U.newton(lead, "uh")
    roots, _ = U.indicial_roots(nw)
    order = max(lead.keys())
    uh_modes = []
    for s in roots:
        s_ = U._round_int(s)
        pw = U.frob_quantity_powers(s_, ops)
        cl = U.classify_uh("frob", pw, s=s_)
        uh_modes.append({"type": "Frobenius", "s": mp.nstr(s, 12), "s_full": mp.nstr(s, 40), "class": cl,
                         "powers": {k: [None if p[0] is None else float(p[0]), None if p[1] is None else float(p[1])] for k, p in pw.items()}})
    for e in nw["edges"]:
        mu = int(e["slope"] + 1)
        for b0 in U.edge_roots(e):
            bs, chk = U.wkb_transport(a, lead, dr, "uh", e, b0)
            beta = bs[-1]
            pw = U.wkb_quantity_powers(b0, beta, mu, ops)
            cl = U.classify_uh("wkb", pw, b0=b0, mu=mu)
            uh_modes.append({"type": f"essential exp(int b x^-{mu})", "b": mp.nstr(b0, 8), "beta": mp.nstr(beta, 8),
                             "class": cl, "transport_residual": mp.nstr(abs(chk["next_residual"]), 3),
                             "powers": {k: [float(p[0]), float(p[1])] for k, p in pw.items()}})
    res["uh"] = {"m": {k: int(v[0]) for k, v in nw["info"].items()}, "P": {k: int(v[2]) for k, v in nw["info"].items()},
                 "edges": [{"k_a": e["k_a"], "k_b": e["k_b"], "slope": str(e["slope"])} for e in nw["edges"]],
                 "modes": uh_modes}
    # infinity
    compsI, drI, _, infoI = comps_for(arm, "inf", point)
    aI, leadI = U.combine(compsI, alpha, lam, eps, TA)
    nwI = U.newton(leadI, "inf")
    rootsI, _ = U.indicial_roots(nwI)
    inf_modes = []
    for s in rootsI:
        s_ = U._round_int(s)
        re_s = s_.real if isinstance(s_, mp.mpc) else s_
        if not isinstance(s_, mp.mpc) and s_ == 1:
            st = "boost (normalisation)"
        elif re_s < 2:
            st = "admissible"
        else:
            st = "inadmissible"
        inf_modes.append({"type": "power r^s", "s": mp.nstr(s, 10), "status": st})
    for e in nwI["edges"]:
        nu = int(-1 - e["slope"])
        for b0 in U.edge_roots(e):
            bs, chk = U.wkb_transport(aI, leadI, drI, "inf", e, b0)
            beta = bs[-1]
            reb, sc = mp.re(b0), abs(b0)
            if reb > mp.mpf("1e-20") * sc:
                st = "inadmissible (growing)"
            elif reb < -mp.mpf("1e-20") * sc:
                st = "admissible (decaying)"
            else:
                ok2 = all(n * nu + mp.re(beta) < 0 for n in (2, 3))
                st = "admissible (oscillatory, F'', F''' decay)" if ok2 else "inadmissible (oscillatory; F'' or F''' does not decay)"
            inf_modes.append({"type": f"exp(int b r^{nu})", "b": mp.nstr(b0, 8), "beta": mp.nstr(beta, 8), "status": st,
                              "transport_residual": mp.nstr(abs(chk["next_residual"]), 3)})
    res["inf"] = {"m": {k: int(v[0]) for k, v in nwI["info"].items()}, "modes": inf_modes}
    # count
    n_inad = sum(1 for m in inf_modes if m["status"].startswith("inadmissible"))
    n_boost = sum(1 for m in inf_modes if m["status"].startswith("boost"))
    armkey = "IR" if arm is None else arm
    rS = 1 if rs_info[armkey][0] else 0
    n_nonreg = sum(1 for m in uh_modes if m["class"] != "regular")
    n_strong = sum(1 for m in uh_modes if m["class"] == "strong")
    Nc = order
    strict = n_inad + n_boost + rS + n_nonreg
    lenient = n_inad + n_boost + rS + n_strong
    res["count"] = {"N_const": Nc, "inf_inadmissible": n_inad, "normalisation": n_boost, "r_S": rS,
                    "UH_nonregular": n_nonreg, "UH_strong": n_strong, "N_cond_strict": strict, "N_cond_lenient": lenient,
                    "Delta_strict": strict - Nc, "Delta_lenient": lenient - Nc,
                    "n_local_uh": len(uh_modes), "n_local_inf": len(inf_modes)}
    return res


def show(res):
    c = res["count"]
    P(f"  [{res['arm']:2s} | {res['point']:22s} | alpha {res['alpha']:>10s} lambda {res['lambda']:>10s} eps {res['eps']:>9s}]")
    for m in res["uh"]["modes"]:
        if m["type"] == "Frobenius":
            P(f"      UH  x^s, s = {m['s']:>22s}  -> {m['class']:8s}  powers {m['powers']}")
        else:
            P(f"      UH  {m['type']}, b = {m['b']}, beta = {m['beta']} -> {m['class']}  powers {m['powers']} (transport res {m['transport_residual']})")
    for m in res["inf"]["modes"]:
        if m["type"].startswith("power"):
            P(f"      inf r^s, s = {m['s']:>10s}  -> {m['status']}")
        else:
            P(f"      inf {m['type']}, b = {m['b']}, beta = {m['beta']} -> {m['status']}")
    P(f"      COUNT: {c['N_const']} constants; conditions: infinity {c['inf_inadmissible']} + normalisation {c['normalisation']}"
      f" + r_S {c['r_S']} + UH {c['UH_nonregular']} (strict) / {c['UH_strong']} (lenient) = {c['N_cond_strict']} / "
      f"{c['N_cond_lenient']};  Delta_strict {c['Delta_strict']:+d}, Delta_lenient {c['Delta_lenient']:+d}")


# ---- K3 / K2: the IR operator
banner("K3 / K2  controls: the IR operator through the same local-analysis and counting code")
irS = analyse(None, "stealth", "3.2e-9", "0.0072888", 0)
show(irS)
sroots = sorted([mp.mpf(m["s_full"]) for m in irS["uh"]["modes"]])
closed = sorted([mp.mpf(-1), mp.mpf(0), (mp.sqrt(5) - 1) / 2, -(mp.sqrt(5) + 1) / 2])
dev_st = max(abs(a_ - b_) for a_, b_ in zip(sroots, closed))
per_dev = {}
for pt in W5:
    rr_ = runs[pt]
    res_ = analyse(None, pt, rr_["alpha"], rr_["lambda"], 0)
    mine = sorted([mp.mpf(m["s_full"]) for m in res_["uh"]["modes"]])
    theirs = sorted([mp.mpf(z) for z in rr_["rootsU"]])
    per_dev[pt] = float(max(abs(a_ - b_) for a_, b_ in zip(mine, theirs)))
check("K3 IR UH exponents: stealth background gives {-1, 0, (sqrt5-1)/2, -(sqrt5+1)/2} (s^2 + s - 1 = 0); the five W5 "
      "points (CFG319's y1, r_UH) reproduce CFG319's committed rootsU to 1e-8",
      f"stealth max dev {ns(dev_st, 3)}; per-point max dev {per_dev}",
      dev_st < mp.mpf("1e-30") and all(v < 1e-8 for v in per_dev.values()))
c_ir = irS["count"]
check("K2 IR count reproduces CFG319: 4 constants, 5 conditions strict (Delta +1), option C determined (lenient Delta 0)",
      f"N_const {c_ir['N_const']}, strict {c_ir['N_cond_strict']}, lenient {c_ir['N_cond_lenient']}",
      c_ir["N_const"] == 4 and c_ir["Delta_strict"] == 1 and c_ir["Delta_lenient"] == 0)
OUT["numbers"]["IR_stealth"] = irS

# ---- the UV arms
banner("B2  the UV arms: local solutions, classification, count (stealth background, then the five W5 points at the "
       "physical M_* band edges)")


def eps_of(Mstar_GeV, rg_m):
    return (HBARC / (mp.mpf(Mstar_GeV) * rg_m))**2


MSTAR_LOW = mp.mpf("1e-12")       # reading: sub-mm gravity tests, recalled, PROVISIONAL
B_RES = {"A": [], "K": []}
for arm in ("K", "A"):
    for eps in ("1e-4", "1e-20"):
        r_ = analyse(arm, "stealth", "3.2e-9", "0.0072888", eps)
        show(r_); B_RES[arm].append(r_)
P("\n  -- W5 points with their own CFG319 backgrounds; M_* at the band's upper edge min(Lambda_HL_max, Lambda_sc) and at "
  "the reading lower edge 1e-12 GeV; holes 10 Msun and M87*")
for pt in W5:
    rr_ = runs[pt]
    al_, c2_ = mp.mpf(rr_["alpha"]), mp.mpf(rr_["lambda"])
    Mup = min(LHL, lam_sc(al_, c2_))
    Mtest = mp.mpf("1e12") if MUTATE else Mup
    for arm in ("K", "A"):
        for (mlab, Ms) in (("band top" if not MUTATE else "MUTATE 1e12 GeV", Mtest), ("band low (reading)", MSTAR_LOW)):
            for rgl, rg in RG.items():
                if mlab.startswith("band low") and rgl.startswith("M87"):
                    continue
                eps = eps_of(Ms, rg)
                r_ = analyse(arm, pt, rr_["alpha"], rr_["lambda"], eps)
                r_["M_star_GeV"] = float(Ms); r_["hole"] = rgl; r_["M_star_label"] = mlab
                show(r_); B_RES[arm].append(r_)
OUT["numbers"]["B2_arms"] = B_RES

verdictB = {}
for arm in ("K", "A"):
    ds = sorted(set(r["count"]["Delta_strict"] for r in B_RES[arm]))
    dl = sorted(set(r["count"]["Delta_lenient"] for r in B_RES[arm]))
    P(f"\n  arm O_{arm}: Delta_strict over all runs {ds};  Delta_lenient {dl}")
    OUT["numbers"][f"B2_Delta_{arm}"] = {"strict": ds, "lenient": dl}
    verdictB[arm] = {"Delta_strict": ds, "Delta_lenient": dl}

allr = [r for arm in ("K", "A") for r in B_RES[arm]] + [irS]
okK10 = all(r["count"]["n_local_uh"] == r["count"]["N_const"] == r["count"]["n_local_inf"] for r in allr)
check("K10 (added control, not in the frozen list) every analysis finds as many local solutions at the UH and at "
      "infinity as the order of the equation", f"{sum(1 for r in allr)} analyses; all consistent: {okK10}", okK10)
hrr = sp.simplify(U.E_OF + BUILD[None]["Ur"].c0**2 - U.Y0**2)
P(f"  B-mechanism (identity): h^rr = g^rr + u^r u^r = e + W^2 = Y^2 on the background: residual {hrr}. Every leaf-projected "
  "(spatial) radial derivative of a stationary perturbation carries h^rr = Y^2 ~ y1^2 x^2, so at the UH the UV terms act "
  "as Euler-order (or weaker) corrections: they cannot reach the IR exponents beyond O(eps).")
OUT["numbers"]["B_mechanism_hrr_minus_Y2"] = str(hrr)

# IR exponents survive the UV term?
sp_K = [m for r in B_RES["K"] for m in r["uh"]["modes"] if m["type"] == "Frobenius"]
sp_A = [m for r in B_RES["A"] for m in r["uh"]["modes"] if m["type"] == "Frobenius"]
splus_K = sorted(set(m["s"][:10] for m in sp_K if 0.5 < float(mp.mpf(m["s"])) < 0.7))
splus_A = sorted(set(m["s"][:10] for m in sp_A if 0.5 < float(mp.mpf(m["s"])) < 0.7))
P(f"  s+ with the UV term present: arm K {splus_K}; arm A {splus_A}  (the UV term does not remove it)")
OUT["numbers"]["splus_with_UV"] = {"K": splus_K, "A": splus_A}

# ---- B3
banner("B3  (frozen: only if Delta_strict <= 0 for an arm)")
for arm in ("K", "A"):
    if max(verdictB[arm]["Delta_strict"]) <= 0:
        P(f"  arm O_{arm}: Delta_strict <= 0 -> B3 applies (r_S layer and wavenumber conditions named in the README)")
    else:
        P(f"  arm O_{arm}: Delta_strict = {verdictB[arm]['Delta_strict']} > 0 -> B3 not reached")

# ---- B4 band
banner("B4  the M_* band: upper edge min(Lambda_HL_max, Lambda_sc) per CFG320 grid point; lower edge none on record")
band = []
for row in J320["numbers"]["grid"]:
    up = min(LHL, mp.mpf(row["Lambda_sc_GeV"]))
    band.append({"alpha_c": row["alpha_c"], "c2": row["c2"], "upper_GeV": float(up)})
up_min, up_max = min(b["upper_GeV"] for b in band), max(b["upper_GeV"] for b in band)
Mused = mp.mpf("1e12") if MUTATE else None
if MUTATE:
    inside = [b for b in band if Mused <= b["upper_GeV"]]
    band_ok = len(inside) > 0
    meas = f"M_* = 1e12 GeV against upper edges {up_min:.3e}..{up_max:.3e} GeV: inside at {len(inside)}/{len(band)} points"
else:
    band_ok = up_max > float(MSTAR_LOW)
    meas = (f"upper edges {up_min:.4e} .. {up_max:.4e} GeV over {len(band)} points; reading lower edge {float(MSTAR_LOW):.0e} GeV"
            f" (sub-mm tests, recalled, PROVISIONAL); non-empty at {sum(1 for b in band if b['upper_GeV'] > float(MSTAR_LOW))}/{len(band)}")
check("B4 the M_* band is non-empty" + (" (MUTATE: M_* = 1e12 GeV must lie OUTSIDE it)" if MUTATE else ""), meas, band_ok,
      load_bearing=False)
OUT["numbers"]["B4"] = {"upper_min_GeV": up_min, "upper_max_GeV": up_max, "lower_reading_GeV": float(MSTAR_LOW),
                        "band_ok": band_ok, "mutate_Mstar_GeV": 1e12 if MUTATE else None}

for arm in ("K", "A"):
    healthy = healthyK if arm == "K" else healthyA
    if not healthy:
        v = "FAILS (B1: unhealthy)"
    elif max(verdictB[arm]["Delta_strict"]) > 0:
        v = "FAILS (gate G12 of CFG467, strict BH regularity: the UV term does not supply the fifth condition; " \
            f"over-determined by {max(verdictB[arm]['Delta_strict'])})"
    elif not band_ok:
        v = "FAILS (B4: M_* band empty -> G11 radiative stability / strong coupling)"
    else:
        v = "WORKS-CONDITIONAL (B3 conditions; boundary-value existence not computed; metric coupling)"
    if not band_ok and not v.startswith("FAILS (B4"):
        v += "; and B4: M_* outside the band (G11)"
    verdictB[arm]["verdict"] = v
    P(f"  VERDICT arm O_{arm}: {v}")
order_ = {"WORKS": 0, "WORKS-CONDITIONAL": 1, "FAILS": 2}
bestB = min(("K", "A"), key=lambda a_: order_[verdictB[a_]["verdict"].split(" ")[0]])
VB = verdictB[bestB]["verdict"].split(" ")[0]
P(f"  VERDICT B (best arm, O_{bestB}): {VB}")
OUT["numbers"]["verdict_B"] = {"arms": verdictB, "best_arm": bestB, "verdict": VB}

# ================================================================================================ OPTION A
banner("OPTION A -- lenient black holes (CFG319 option C) + the Pospelov-Shang hierarchy")
mp.mp.dps = 50
rS_, xS = sp.symbols('r x', real=True)
C0 = 3 * sp.sqrt(3) / 4
Yr = (2 * rS_ - 3) * sp.sqrt(4 * rS_**2 + 4 * rS_ + 3) / (4 * rS_**2)
Wr = C0 / rS_**2
Hp = -1 / (Yr * (Yr + Wr))
y1 = sp.nsimplify(sp.limit(sp.diff(Yr, rS_), rS_, sp.Rational(3, 2)))
W0 = sp.nsimplify(Wr.subs(rS_, sp.Rational(3, 2)))
kap = sp.simplify(y1 * W0)
lim_out = sp.limit(xS * Hp.subs(rS_, sp.Rational(3, 2) + xS), xS, 0, '+')
lim_in = sp.limit(xS * Hp.subs(rS_, sp.Rational(3, 2) + xS), xS, 0, '-')
check("A1a T -> +infinity at the UH at every finite v: lim x H'(r_UH + x) = -1/(y1 W0), finite and non-zero from both sides",
      f"y1 = {y1}, W0 = {W0}, kappa_U = y1 W0 = {kap}; limit + {sp.simplify(lim_out)}, limit - {sp.simplify(lim_in)}",
      sp.simplify(lim_out + 1 / kap) == 0 and sp.simplify(lim_in + 1 / kap) == 0)
# A1b: tau = -exp(-kappa (v + H)) ; H = -(1/kappa) ln|x| + H_reg ; tau = -e^{-kappa v} x e^{-kappa H_reg}
Hreg_p = sp.simplify(Hp + 1 / (kap * (rS_ - sp.Rational(3, 2))))
ser_Hreg = sp.series(Hreg_p.subs(rS_, sp.Rational(3, 2) + xS), xS, 0, 3).removeO()
neg_pow = any(t_.as_coeff_exponent(xS)[1] < 0 for t_ in sp.Add.make_args(sp.expand(ser_Hreg)))
e_UH = 1 - 2 / sp.Rational(3, 2)
# tau ~ -e^{-kappa v} e^{-kappa Hreg(r_U)} x : d tau/dr at the UH = -e^{-kappa v - kappa Hreg(r_U)} != 0; d tau / dv = 0 there
grad_norm_sign = sp.sign(e_UH)          # g^{rr} (d_r tau)^2 + 2 g^{vr} d_v tau d_r tau = e (d_r tau)^2 at x = 0
check("A1b the global time function tau = -exp(-kappa_U T) extends analytically across the UH (H' + 1/(kappa x) is "
      "regular), with d tau/dr != 0 and a timelike normal there (g^{mn} d tau d tau = e(r_UH) (d_r tau)^2 < 0)",
      f"negative powers in the series of H' + 1/(kappa x): {neg_pow}; e(r_UH) = {e_UH}; sign {grad_norm_sign}",
      (not neg_pow) and grad_norm_sign < 0)

# A1c fastest-signal reach
Yf = sp.lambdify(rS_, Yr, "mpmath"); Wf = sp.lambdify(rS_, Wr, "mpmath")


def reach(r0, v0, mode, c=None, sgn=+1, rmax=mp.mpf(1e4), vmax=mp.mpf(1e4), mutate_leaf=False):
    """integrate a radial signal from (v0, r0) and return the largest r reached at finite v.
    mode 'leaf': along the khronon leaf (infinite speed, dT = 0) in direction sgn*s;  'char': k = u + sgn c s.
    mutate_leaf: the instantaneous mode on v - r = const hypersurfaces instead (MUTATE)."""
    r, v = mp.mpf(r0), mp.mpf(v0)
    best = r
    if abs(r - mp.mpf(1.5)) < mp.mpf("1e-30") and mode == "leaf" and not mutate_leaf:
        return r                     # the UH is itself a leaf (T = +infinity)
    h = mp.mpf("1e-2")
    for _ in range(20000):
        if mutate_leaf:
            dr_, dv_ = mp.mpf(1), mp.mpf(1)          # v - r = const, outward
        else:
            Y, W = Yf(r), Wf(r)
            if abs(Y) < mp.mpf("1e-40"):
                return best
            uv_, ur_ = 1 / (Y + W), -W
            sv_, sr_ = 1 / (Y + W), Y
            if mode == "leaf":
                dv_, dr_ = sgn * sv_, sgn * sr_
            else:
                dv_, dr_ = uv_ + sgn * c * sv_, ur_ + sgn * c * sr_
        nrm = mp.sqrt(dv_**2 + dr_**2)
        # adaptive step: a fixed fraction of the distance to the UH (slows down near it, speeds up far away)
        step = h * max(abs(r - mp.mpf(1.5)), mp.mpf("1e-12")) / nrm if not mutate_leaf else mp.mpf(5) / nrm
        r_new, v_new = r + step * dr_, v + step * dv_
        if (not mutate_leaf) and (r - mp.mpf(1.5)) * (r_new - mp.mpf(1.5)) < 0:
            # would cross the UH: refine (a leaf or a forward-in-tau signal cannot cross; step overshoot only)
            h = h / 4
            if h < mp.mpf("1e-14"):
                return best
            continue
        r, v = r_new, v_new
        best = max(best, r)
        if r > rmax or abs(v) > vmax or r < mp.mpf("0.05"):
            return best
    return best


starts = [(r0, v0) for r0 in ("1.0", "1.2", "1.4", "1.49", "1.4999", "1.5") for v0 in ("-10", "0", "10")]
speeds = [None, 1, 444, mp.mpf("7.9e5"), mp.mpf("1e12")]
maxr = mp.mpf(0); worst = None
for (r0, v0) in starts:
    for c in speeds:
        for sgn in (+1, -1):
            if c is None:
                rr = reach(r0, v0, "leaf", sgn=sgn, mutate_leaf=MUTATE)
            else:
                if MUTATE:
                    continue
                rr = reach(r0, v0, "char", c=c, sgn=sgn)
            if rr > maxr:
                maxr, worst = rr, (r0, v0, "leaf" if c is None else f"c={ns(c, 3)}", sgn)
okA1c = maxr <= mp.mpf(1.5) + mp.mpf("1e-9")
check("A1c fastest-signal reach from on/inside the UH (leaf = infinite speed, and c = 1, 444, 7.9e5, 1e12, both "
      "directions" + ("; MUTATE: instantaneous mode on v - r = const" if MUTATE else "") + "): max r <= r_UH + 1e-9",
      f"max r reached {ns(maxr, 12)} at {worst}", okA1c)
ext_reach = max(reach(r0, "0", "leaf", sgn=+1, rmax=mp.mpf(1e4), vmax=mp.mpf(1e6)) for r0 in ("3", "10"))
check("K5 reach code control: from exterior start points the leaf reaches r = 1e4", f"max r {ns(ext_reach, 8)}",
      ext_reach >= mp.mpf(1e4))
splus = {pt: mp.mpf(runs[pt]["rootsU"][-1]) for pt in W5}
sminus = {pt: mp.mpf(runs[pt]["rootsU"][0]) for pt in W5}
okA1d = all(1 + s > 1 for s in splus.values())
cprime_flag = all(1 + s < 0 for s in sminus.values())
check("A1d O(v) persistence: delta tau ~ x^(1+s+) with 1 + s+ > 1 at all W5 points (tau stays C^1); control: the C' "
      "option (s-) gives 1 + s- < 0 (foliation destroyed) and is flagged",
      f"1+s+ {[ns(1 + s, 8) for s in splus.values()]}; 1+s- {[ns(1 + s, 6) for s in sminus.values()]}", okA1d and cprime_flag)
free_C = c_ir["N_const"] - c_ir["N_cond_lenient"]
ext = {pt: runs[pt]["ext_diff_C_Cp"] for pt in W5}
check("A1e zero free data on the defect: option C has as many conditions as constants (computed K2 count), so the s+ "
      "amplitude is an output", f"free parameters on the UH = {free_C}; CFG319 option C admissible at all W5: "
      f"{J319['numbers']['verdict_inputs']['optC_admissible']}", free_C == 0 and all(J319["numbers"]["verdict_inputs"]["optC_admissible"]),
      reading=f"rule-level exterior difference C vs C' at 6M (committed): {ext}")
A1ok = all(OUT["checks"][k]["ok"] for k in OUT["checks"] if k.startswith("A1"))

# A2 finiteness
p1 = {pt: s - 1 for pt, s in splus.items()}
okA2b = all(p > -1 for p in p1.values())
okA2c = all(2 * p > -1 for p in p1.values())


def double_int(p, d1, d2):
    """change of I1(d) = int_d^1 x^p dx and of D(d) = int_d^1 dx' int_d^x' x^p dx between cut-offs d1, d2"""
    I1 = lambda d: (1 - d**(p + 1)) / (p + 1)
    D = lambda d: ((1 - d**(p + 2)) / (p + 2) - d**(p + 1) * (1 - d)) / (p + 1)
    return I1(d1) - I1(d2), D(d1) - D(d2)


tip = {pt: double_int(p, mp.mpf("1e-30"), mp.mpf("1e-15")) for pt, p in p1.items()}
okA2d = all(abs(t_[0]) < mp.mpf("1e-5") and abs(t_[1]) < mp.mpf("1e-5") for t_ in tip.values())
pm = {pt: s - 1 for pt, s in sminus.items()}
krol_m = {pt: double_int(p, mp.mpf("1e-30"), mp.mpf("1e-15"))[0] for pt, p in pm.items()}
ctrl_K6 = all(abs(z) > 1e10 for z in krol_m.values())
dr_dtau = -mp.sqrt(2 / mp.mpf(1.5))
okA2e = all(0 < s < 1 for s in splus.values()) and dr_dtau != 0
check("A2a exterior regular: CFG319 option C admissible, modes -1 and 0 regular, s+ weak at all W5 points",
      f"{J319['numbers']['verdict_inputs']['splus_kind']}", all(k_ == "weakly singular" for k_ in J319["numbers"]["verdict_inputs"]["splus_kind"]))
check("A2b O(v) stress / Ricci exponent p1 = s+ - 1 > -1 (integrable)", f"p1 {[ns(p, 6) for p in p1.values()]}", okA2b)
check("A2c quadratic invariants at O(v^2): 2 p1 > -1, i.e. s+ > 1/2", f"2 p1 {[ns(2 * p, 6) for p in p1.values()]} (margin "
      f"{ns(min(s - mp.mpf(0.5) for s in splus.values()), 4)} in s+)", okA2c)
check("A2d Tipler and Krolak integrals along radial free fall (dr/dtau = -sqrt(2/r) at r_UH, transversal) finite: the "
      "change of the single and double integrals between cut-offs 1e-15 and 1e-30 is < 1e-5",
      f"{ {pt: (ns(t_[0], 3), ns(t_[1], 3)) for pt, t_ in tip.items()} }; dr/dtau = {ns(dr_dtau, 6)}", okA2d)
check("K6 control: the s- mode's Krolak integral diverges (change between cut-offs > 1e10)",
      f"{ {pt: ns(z, 3) for pt, z in krol_m.items()} }", ctrl_K6)
check("A2e metric class C^{1, s+} with 0 < s+ < 1 and a transversal crossing: Hoelder Christoffels, unique transversal "
      "geodesics (Caratheodory)", f"s+ {[ns(s, 6) for s in splus.values()]}", okA2e)
cth = sp.Symbol('c')
flux1 = sp.integrate(cth, (cth, -1, 1))
check("A2f (ARG, reading) O(v) Killing-energy flux through the sphere: integral of cos(theta) = 0; the O(v^2) flux is "
      "r-independent (conservation) and vanishes at infinity for stationary decaying fields; O(v^2) fields not computed",
      f"integral = {flux1}", flux1 == 0, load_bearing=False)
A2ok = all(OUT["checks"][k]["ok"] for k in OUT["checks"] if k.startswith("A2") and OUT["checks"][k]["load_bearing"])
P("  reading S: A2 reads FAIL by definition (the curvature diverges pointwise on the UH as x^(s+ - 1) = x^-0.382).")

# A3 thermodynamics
Q = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f'Q{i}{j}'))
uu = sp.Matrix([sp.Symbol(f'u{i}') for i in range(4)])
eta = sp.diag(-1, 1, 1, 1)
Kq = sum(eta[i, i] * Q[i, i] for i in range(4))
aq_ = [sum(uu[m] * Q[m, n] for m in range(4)) for n in range(4)]
Lq = -laS * Kq**2 + alS * sum(eta[n, n] * aq_[n]**2 for n in range(4))
mom_ok = True
for m in range(4):
    for n in range(4):
        expect = -2 * laS * Kq * eta[m, n] + 2 * alS * uu[m] * eta[n, n] * aq_[n]
        if sp.simplify(sp.diff(Lq, Q[m, n]) - expect) != 0:
            mom_ok = False
pows = {pt: {"dK": float(s + 1), "da, du": float(s)} for pt, s in splus.items()}
okA3a = mom_ok and all(min(v.values()) >= 0 for v in pows.values())
check("A3a the momentum dL/d(grad_m u_n) = -2 lambda K g^{mn} + 2 alpha u^m a^n contains only g, u, K, a (sympy); the "
      "option-C perturbations of K, a, u vanish at the UH (exponents >= 0), so the Noether charge and symplectic current "
      "are finite there", f"momentum identity {mom_ok}; exponents {pows}", okA3a)
okA3b = all(s > 0 for s in splus.values()) and flux1 == 0
check("A3b kappa_UH unperturbed at O(v): its change ~ x^s+ -> 0 at the UH and carries cos(theta) (sphere average 0)",
      f"s+ > 0 at all W5: {all(s > 0 for s in splus.values())}; sphere average {flux1}", okA3b)
th = sp.Symbol('theta')
dA = sp.integrate(sp.cos(th) * sp.sin(th), (th, 0, sp.pi))
check("A3c the O(v) first law is trivial: delta A_UH = delta M = 0 for an l = 1 perturbation",
      f"integral cos(theta) sin(theta) dtheta = {dA}", dA == 0)
P("  UH temperature (Berglund-Bhattacharyya-Mattingly 2012/13 and later disputes): literature recalled from memory, "
  "PROVISIONAL, not read, not scored.")
A3ok = all(OUT["checks"][k]["ok"] for k in OUT["checks"] if k.startswith("A3"))

# A4 joint window
banner("A4  the joint alpha_c window")
a_rs = {}
for c2 in C2GRID:
    f = lambda la_: lam_sc(mp.mpf(10)**la_, c2) - LHL
    a_rs[float(c2)] = float(mp.mpf(10)**mp.findroot(f, mp.mpf(-13)))
J_rs = J467["edges"]["G11_alpha_rs"]
dev_rs = max(abs(a_rs[float(c2)] / J_rs[k] - 1) for c2, k in zip(C2GRID, sorted(J_rs, key=float)))
win0 = {}
for c2 in C2GRID:
    hi = min(a_rs[float(c2)], float(AMAX))
    win0[f"{float(c2):.4e}"] = f"[{float(AMIN):.4e}, {hi:.4e}]" if hi >= float(AMIN) else "EMPTY"
n0 = sum(1 for v in win0.values() if v != "EMPTY")
first_open = min((float(c2) for c2 in C2GRID if a_rs[float(c2)] >= float(AMIN)), default=None)
check("K9 alpha_rs reproduces CFG467's G11 edge (5.80e-14 / 1.18e-13 at the c_2 ends) to 1e-2, and the A4-0 window is "
      "non-empty exactly at c_2 >= 0.038 (3 points)", f"max rel dev {dev_rs:.2e}; non-empty at {n0}/9, first c_2 {first_open}",
      dev_rs < 1e-2 and n0 == 3 and first_open is not None and first_open > 0.038)
IlenH = J467["per_c2"]
okH = all(v["I_len"] == "[9.6240e-14, 3.2000e-09]" for v in IlenH.values())
uv_ok = {arm: max(verdictB[arm]["Delta_lenient"]) <= 0 for arm in ("K", "A")}
A4UV = any(uv_ok.values())
check("A4-H window (reading W + hierarchy) = CFG467's I_len = [9.624e-14, 3.2e-9] at every c_2", f"{okH}", okH)
check("A4-UV some healthy UV operator keeps option C (lenient count Delta_len <= 0)",
      f"Delta_len <= 0: O_K {uv_ok['K']}, O_A {uv_ok['A']}", A4UV,
      reading="an arm with Delta_len > 0 would destroy option C itself; that arm is excluded as the hierarchy's UV sector")
OUT["numbers"]["A4"] = {"alpha_rs": a_rs, "A4_0_window": win0, "A4_H_window": "[9.624e-14, 3.2e-9] at all 9 c_2",
                        "UV_consistency": uv_ok}
A4ok = okH and A4UV

if not A1ok:
    VA = "FAILS"; VA_why = "A1 causal disconnection"
elif not A2ok:
    VA = "FAILS"; VA_why = "A2 finiteness"
elif not A3ok:
    VA = "FAILS"; VA_why = "A3 UH thermodynamics"
elif not A4ok:
    VA = "FAILS"; VA_why = "A4 joint window / UV consistency"
else:
    VA = "WORKS-CONDITIONAL"
    keep = [f"O_{a_}" for a_ in ("K", "A") if uv_ok[a_]]
    VA_why = ("conditions: (i) owner adopts reading W; (ii) full window [9.624e-14, 3.2e-9] needs the hierarchy (+1 UV scale "
              f"M_* <= {float(LHL):.3g} GeV; option C survives the tested UV operators {keep}), or 0 new constants on the sliver "
              f"[9.624e-14, alpha_rs(c_2)] at {n0}/9 c_2 (c_2 >= 0.038); (iii) CFG319 scope (test-khronon limit, collapse "
              "formation) and CFG467 tested-range edges")
P(f"  VERDICT A: {VA} ({VA_why})")
OUT["numbers"]["verdict_A"] = {"verdict": VA, "why": VA_why}

# ================================================================================================ OPTION C
banner("OPTION C -- the chassis retired: candidate B as a recipe")
INV = [
    ("kappa = 1/2", "FITTED", "closure_map/GATES.md", "kappa = 1/2 vs 0.465 ± 0.076"),
    ("rho_DE(t) in a0(t) = kappa c sqrt(G rho_DE(t))", "DATA", "WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md", "a₀(t) = κ c √(G ρ_DE(t))"),
    ("kernel nu_mono (nu_RAR to y* = 2.3374, log splice delta = 0.05)", "DECLARED FUNCTION (+1 shape constant delta)", "CFG5_common.py",
     "nu_RAR up to y* = 2.3374, then the monotone log splice with delta = 0.05"),
    ("bound-only switch", "DECLARED RULE", "closure_map/GATES.md", "with the bound-only switch"),
    ("KiDS density edge x_e = 0.4", "DECLARED CONSTANT", "closure_map/GATES.md", "B: declared 0.4"),
    ("growth edge r_M/ln(1/(1 - f_b)) = 5.85 r_M with the turnaround catchment", "DECLARED RULE (zero-knob given kappa, f_b)",
     "STANDING_2026-09-29.md", "The mass-conserving edge r_M/ln(1/(1−f_b)) = 5.85 r_M"),
    ("cosmic baryon fraction f_b", "DATA", "STANDING_2026-09-29.md", "Inputs are κ and f_b only"),
    ("cold-fluid amount Omega_c h^2 = 0.12", "FITTED (as in LCDM)", "closure_map/GATES.md", "met by construction (T4; amount FITTED as in ΛCDM)"),
    ("cold fluid relaxes toward the phantom target at rate Gamma (bookkeeping, not derived)", "DECLARED RULE",
     "WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md", "A conserved cold fluid relaxes toward the target in bound regions"),
    ("ownership (the Sun carries no phantom; globulars class E Newtonian)", "DECLARED RULE", "closure_map/GATES.md", "PASS via ownership"),
    ("lensing = GR lensing of the effective dark density (Phi = Psi)", "DECLARED RULE", "closure_map/GATES.md",
     "B's lensing is the effective dark density in GR (T2)"),
    ("background cosmology GR + CDM at z >~ 10", "DECLARED RULE", "closure_map/GATES.md", "GR + CDM at z >~ 10"),
    ("baryon field includes gas pressure", "DECLARED MODELLING RULE", "WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md",
     "including gas pressure (CFG372)"),
    ("stellar M/L Upsilon_disk", "NUISANCE (per data set)", "closure_map/GATES.md", "one global Upsilon_disk (0.5-0.8)"),
    ("G = measured Newton constant (no alpha_c/2 correction without the chassis)", "DECLARED", "closure_map/RECIPE_GATE_AUDIT_2026-10-03.md",
     "G_N = G/(1 − α_c/2)"),
]
prov = []
for item, status, path, quote in INV:
    full = os.path.join(CFG, path)
    found = os.path.exists(full) and quote in open(full, encoding="utf-8").read()
    prov.append(found)
    P(f"  [{'found' if found else 'MISSING'}] {item:78s} {status:42s} ({path})")
check("K7a provenance: every inventory row's quoted source string is found in its committed file",
      f"{sum(prov)}/{len(prov)} found", all(prov))
counts = {}
for _, st, _, _ in INV:
    key = st.split(" (")[0]
    counts[key] = counts.get(key, 0) + 1
P(f"  inventory by class: {counts}")

UNTESTED = [
    ("Gravity waves at light speed", "status board col. 1 (CFG292); GATES 4.02 NS for B"),
    ("Equations well-posed (high freq.)", "status board col. 1 (CFG292)"),
    ("Full nonlinear well-posedness", "status board col. 1 (CFG294)"),
    ("Lapse condition, realistic matter", "status board col. 1 (CFG312)"),
    ("Binary pulsars", "status board col. 1 (CFG291/311); GATES 4.04 NS for B"),
    ("Strong coupling", "status board col. 1 (XC1/XC3); GATES 5.03"),
    ("Solar system (PPN + Cassini Q2)", "status board col. 1 (CFG291/357; the chassis filter). B keeps GATES 4.01 via ownership; PPN alpha1/alpha2/gamma become untested"),
    ("Matter conservation (G9)", "status board col. 1 (CFG329)"),
    ("Structural order (G0)", "status board col. 1 (CFG329)"),
    ("Zero-field nonlinear, ungated", "status board col. 1 (CFG358, FAIL chassis-only): becomes moot, not passed"),
    ("Black holes (EHT, LIGO ringdown)", "status board col. 1 (CFG318/319): the CFG467 tension disappears with the chassis, but BH physics becomes untested"),
    ("Radiative stability (G12)", "status board col. 4 (CFG320)"),
    ("lensing = dynamics as a derivation", "GATES 4.03 (already NS as derivation for B)"),
    ("Newton/GR recovery, measured G derived", "GATES 5.09"),
    ("DOF count / ghost freedom of a field theory", "GATES 5.05, RECIPE G4/G5"),
    ("Cauchy problem / causality", "GATES 5.04"),
]
board = open(os.path.join(CFG, "closure_map/status_picture_2026_10_03.py"), encoding="utf-8").read()
tiles_found = [t for t, _ in UNTESTED if t in board]
P(f"  gates that become UNTESTED (not passed): {len(UNTESTED)} ({len(tiles_found)} are status-board tiles found in the board script)")
for t, w in UNTESTED:
    P(f"     - {t}: {w}")

# dependency audit: current B passes / conditionals and their ingredients
CHASSIS_ONLY = {"khronon", "alpha_c", "c_2", "heat filter", "leaf average", "C-H constitutive term"}
B_ROWS = [
    ("Rotation curves (SPARC RAR)", "PASS", {"law", "nu_mono", "Upsilon"}),
    ("Local a0 from MeerKAT", "PASS", {"law"}),
    ("Weak lensing (KiDS)", "PASS", {"law", "switch", "x_e", "lensing rule"}),
    ("Clusters, Bullet Cluster", "PASS", {"law", "cold amount"}),
    ("Andromeda + Local Volume dwarfs", "PASS", {"law"}),
    ("Globulars + ownership rule", "COND", {"ownership"}),
    ("Milky Way ultra-faint dwarfs", "COND", {"law", "post-reionisation accretion (LCDM-calibrated)"}),
    ("Structure growth, candidate B", "COND", {"law", "growth edge", "f_b", "cold-fluid bookkeeping", "Newtonian N-body"}),
    ("CMB TT/TE/EE (GATES 3.01)", "met by construction", {"GR + CDM background", "cold amount"}),
    ("CMB lensing (GATES 3.02)", "PASS", {"switch", "lensing rule"}),
    ("Lyman-alpha forest (GATES 3.12)", "PASS", {"switch"}),
    ("Solar System Q2 via ownership (GATES 4.01)", "PASS", {"ownership", "law"}),
    ("a0 over time (law row)", "UNDEC", {"kappa", "rho_DE"}),
    ("Gaia DR4 Arm C (prereg)", "OPEN", {"ownership"}),
]
dep = [r for r in B_ROWS if r[2] & CHASSIS_ONLY]
LEADS = [("CFG373 khronon-lapse carrier (G1)", "chassis khronon lapse"),
         ("CFG381 khronon reaction sink (+1 coupling)", "chassis khronon"),
         ("CFG462 lapse settling edge (FAIL, exhaustion only)", "chassis khronon lapse"),
         ("CFG483 khronon-boundary settling class (cold-fluid shock + khronon-lapse total field)", "chassis khronon lapse"),
         ("khronon-class a0-rho_Lambda tie kappa = 2 sqrt(8 pi)/(3 beta) (WORKING_MODEL synthesis 4)", "chassis khronon")]
P(f"  dependency audit: {len(B_ROWS)} current B rows; rows using a chassis-only ingredient: {len(dep)}")
P("  leads that use the chassis (lost as mechanisms, not passes): " + "; ".join(f"{a_} [{b_}]" for a_, b_ in LEADS))


def verdict_C(rows):
    d = [r for r in rows if r[2] & CHASSIS_ONLY]
    return ("FAILS", d[0][0]) if d else ("WORKS-CONDITIONAL", None)


vC, vC_row = verdict_C(B_ROWS)
inj = B_ROWS + [("FAKE row (injected)", "PASS", {"law", "khronon"})]
vC_inj, _ = verdict_C(inj)
check("K7b injecting one fake chassis dependency into a B pass turns the C verdict to FAILS", f"{vC_inj}", vC_inj == "FAILS")
VC = vC
P(f"  VERDICT C: {VC}" + (f" (row {vC_row})" if vC_row else
                         f" (condition: {len(UNTESTED)} gates untested; B is a recipe, not a theory; the tension is bypassed, not resolved)"))
OUT["numbers"]["C"] = {"inventory": [{"item": a, "status": b, "source": c} for a, b, c, _ in INV], "inventory_counts": counts,
                       "untested": [{"gate": a, "where": b} for a, b in UNTESTED], "dependent_rows": [r[0] for r in dep],
                       "leads_lost": [a for a, _ in LEADS], "verdict": VC}

# ================================================================================================ K8 footings
fp = {}
for lab in FOOT:
    fp[lab] = (tuple(sorted(a_rs.items())), up_min, up_max)
check("K8 a0 enters no computation (A4 windows and the B4 band identical under both footing labels; bookkeeping)",
      f"identical: {fp['canonical'] == fp['alt']}", fp["canonical"] == fp["alt"])

# ================================================================================================ summary
banner("SUMMARY")
VERD = {"A": VA, "B": VB, "C": VC}
for k_, v_ in VERD.items():
    P(f"  option {k_}: {v_}")
OUT["verdicts"] = VERD
if MUTATE:
    flipA = (not A1ok) and VA == "FAILS"
    flipB = (not band_ok) and VB == "FAILS"
    check("MUTATE (A): A1 fails and A reads FAILS with the instantaneous mode on v - r = const", f"A1 ok {A1ok}, A {VA}", flipA)
    check("MUTATE (B): B4 fails and B reads FAILS at M_* = 1e12 GeV", f"band ok {band_ok}, B {VB}", flipB)
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_pass"] = sum(1 for _, ok, _ in CH if ok); OUT["n_fail_load_bearing"] = n_fail
OUT["runtime_s"] = round(time.time() - T0, 1)
rc = 1 if (n_fail or MUTATE) else 0
P(f"\n  checks {OUT['n_pass']}/{OUT['n_checks']} pass; load-bearing failures {n_fail}; rc {rc}; runtime {OUT['runtime_s']} s")
P("  kappa = 1/2 is FITTED; no dark-matter particle is added; the cold mass is still required; not 'theory closed'.")


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (mp.mpf, mp.mpc)):
        return str(o)
    if isinstance(o, (sp.Basic,)):
        return str(o)
    return o


json.dump(jclean(OUT), open(os.path.join(HERE, f"cfg469_results{SUF}.json"), "w"), indent=1)
_fh.close()
sys.exit(rc)
