#!/usr/bin/env python3
"""CQ5: AeST + v3s's switched stiffness, -(gamma_L/2K^2)[max(D.V, 0)]^2 on AeST's scalar. See FROZEN_CRITERIA.md.

    OMP_NUM_THREADS=1 nice -n 10 python3 -I cq5_graft.py [--mutate] [--tag TAG]

Execs the byte-identical AX1 engine copy (common/ax1_engine.py, never edited) for classes AeST and v3s and uses
its constants, fields and functions. --mutate = stiffness off (gamma_L = 0): the graft is then AeST.
kappa = 1/2 FITTED; not theory closed. Footings never pooled. Nothing here says the data favour the framework."""
import os, sys, json, math, hashlib, glob
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "../.."))
MUT = "--mutate" in sys.argv
TAG = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else ""
OUT, FAILS = [], []
RES = {"lane": "CQ5_aest_switched_stiffness", "mutate": MUT, "standing": "kappa = 1/2 FITTED; not theory closed; footings never pooled"}
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = bool(ok)
    if not ok: FAILS.append(name)
def J(p): return json.load(open(os.path.join(ROOT, p)))
def rel(a, b): return abs(a - b) / max(abs(b), 1e-300)

P(f"CQ5 graft{' MUTATE (stiffness off)' if MUT else ''}. kappa = 1/2 FITTED; not theory closed.")
# ---------------- KA0: engine copy is byte-identical
ENG = os.path.join(HERE, "common", "ax1_engine.py"); AX1 = "rebuild_2026_10_22/AX1_action_for_law"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
s0, s1 = sha(ENG), sha(os.path.join(ROOT, AX1, "common/ax1_engine.py"))
check("KA0", s0 == s1, f"engine copy SHA-256 {s0[:16]}... equals AX1's {s1[:16]}...")
RES["engine_sha256"] = s0

def run_engine(cls):
    os.makedirs(os.path.join(HERE, cls), exist_ok=True)
    g = {"__name__": "ax1_engine_copy", "__file__": ENG}; argv = sys.argv
    sys.argv = [ENG, cls, "--tag", "_CQ5" + TAG + ("_stiffoff" if MUT else "")]; code = None
    try: exec(compile(open(ENG).read(), ENG, "exec"), g)
    except SystemExit as e: code = e.code
    finally: sys.argv = argv
    return g, code

# ---------------- KA1: copy run as AeST reproduces AX1's committed AeST numbers
gA, codeA = run_engine("AeST"); ref = J(f"{AX1}/AeST/ax1_AeST.json")
worst = 0.0
for k, s in gA["RES"]["static"].items():
    r = ref["static"][k]
    for E in s["Q2_QUMOND"]: worst = max(worst, rel(s["Q2_QUMOND"][E], r["Q2_QUMOND"][E]))
    if s["over_Hees_AQUAL_E2"] is not None:
        for a, b in zip(s["over_Hees_AQUAL_E2"], r["over_Hees_AQUAL_E2"]): worst = max(worst, rel(a, b))
    worst = max(worst, rel(s["Saturn_over_bound"], r["Saturn_over_bound"]))
labs_same = all(gA["RES"]["labels"][f]["label"] == ref["labels"][f]["label"] for f in ref["labels"])
eng_ok = all(gA["RES"]["checks"].get(c) for c in ("K1", "K2", "K3", "K4"))
check("KA1", worst <= 1e-12 and labs_same and eng_ok, f"copy as AeST vs AX1 ax1_AeST.json: max rel {worst:.1e} (<= 1e-12); labels identical {labs_same}; engine K1-K4 pass {eng_ok}")
RES["AeST_engine_labels"] = {f: gA["RES"]["labels"][f]["label"] for f in gA["RES"]["labels"]}

# ---------------- KA2: copy run as v3s reproduces AX1's hedgehog table and C6 margins
gV, codeV = run_engine("v3s"); refV = J(f"{AX1}/v3s/ax1_v3s.json")
hh_e, hh_r = gV["RES"]["extra"]["hedgehog_GM_over_Lstar2_over_bound"], refV["extra"]["hedgehog_GM_over_Lstar2_over_bound"]
GM, PC, AU = gA["GM"], gA["PC"], gA["AU"]; BOUNDS = gV["bounds"]
def hedgehog(Lpc, muK_perMpc=0.0):
    a = GM / (Lpc * PC) ** 2 + GM * (muK_perMpc / (1e6 * PC)) ** 2 / 2
    return {p: a / b for p, b in BOUNDS.items()}
w2 = max(rel(hh_e[L][p], hh_r[str(L)][p]) for L in hh_e for p in hh_e[L])
w3 = max(rel(hedgehog(L)[p], hh_e[L][p]) for L in hh_e for p in hh_e[L])
mg = max(rel(gV["RES"]["extra"]["C6_R1_margin"][k], refV["extra"]["C6_R1_margin"][k]) for k in refV["extra"]["C6_R1_margin"])
check("KA2", max(w2, w3, mg) <= 1e-12, f"copy as v3s vs AX1 ax1_v3s.json hedgehog {w2:.1e}, C6 margins {mg:.1e}; lane hedgehog vs engine {w3:.1e} (<= 1e-12)")

# ---------------- KA3: closed-form screened Q2 (curl-free scalar + longitudinal stiffness; AS3 Part 2 form)
A_law, eta_of, FOOT, FOOT_D7C, EFS, HEES, PARK = gA["A_law"], gA["eta_of"], gA["FOOT"], gA["FOOT_D7C"], gA["EFS"], gA["HEES"], gA["PARK"]
def xe(a0, E):
    eta = eta_of(A_law, a0, E); return eta * (1.0 + float(A_law(np.array([eta]))[0]))
def Q2s(a0, E, Lpc, nq=400):
    x = xe(a0, E); Sp, Sl = x, x * (2.0 + x); u, w = np.polynomial.legendre.leggauss(nq)
    I = float(np.sum(w * (0.5 - 1.5 * u * u) * np.sqrt(Sp * (1 - u * u) + Sl * u * u)))
    return math.sqrt(2.0) * GM / (Lpc * PC) ** 3 * abs(I), x
as3 = J("rebuild_2026_10_22/AS3_ppn_and_khronon_scalar/as3_part2.json")["Q2"]
ra = max(rel(Q2s(FOOT[k.split("|")[0]], k.split("|")[1], float(k.split("|")[2]))[0], abs(v["Q2"])) for k, v in as3.items() if len(k.split("|")) == 3 and isinstance(v, dict) and "Q2" in v)
c3 = J("covariant_push_2026_10_22/C3_scale_map/c3_scale_map_results.json")["K6_cassini"]
rc = max(rel(Q2s(FOOT_D7C[k.split("|")[0]], k.split("|")[2], float(k.split("|")[1]))[0], v["Q2_V1"]) for k, v in c3.items() if len(k.split("|")) == 3 and isinstance(v, dict) and "Q2_V1" in v)
rq = max(rel(Q2s(a0, E, 24.0, nq=800)[0], Q2s(a0, E, 24.0)[0]) for a0 in FOOT.values() for E in EFS)
check("KA3", ra <= 1e-6 and rc <= 1e-2 and rq <= 1e-9, f"closed form vs AS3 Part 2 ({len(as3)} cells) max rel {ra:.1e} (<= 1e-6); vs C3 V1 K6 ({len(c3)} cells, D7c a0) {rc:.1e} (<= 1e-2); quadrature doubling {rq:.1e} (<= 1e-9)")
RES["KA3"] = dict(AS3_max_rel=ra, C3_V1_max_rel=rc, quad_doubling=rq, AS3_cells=len(as3), C3_cells=len(c3))

# ---------------- sympy S1-S4
t, x, y, z = sp.symbols("t x y z", real=True); X = [t, x, y, z]
def DdotV(g, A, phi):
    gi = sp.simplify(g.inv()); n = 4; dphi = [sp.diff(phi, c) for c in X]
    G = [[[sum(gi[l, s] * (sp.diff(g[s, m], X[k]) + sp.diff(g[s, k], X[m]) - sp.diff(g[m, k], X[s])) for s in range(n)) / 2
           for k in range(n)] for m in range(n)] for l in range(n)]
    q = [[gi[m, k] + A[m] * A[k] for k in range(n)] for m in range(n)]
    t1 = sum(q[m][k] * (sp.diff(phi, X[m], X[k]) - sum(G[l][m][k] * dphi[l] for l in range(n))) for m in range(n) for k in range(n))
    sq = sp.sqrt(-g.det()); th = sum(sp.diff(sq * A[m], X[m]) for m in range(n)) / sq
    Q = sum(A[m] * dphi[m] for m in range(n)); V = [sum(q[m][k] * dphi[k] for k in range(n)) for m in range(n)]
    return t1 + th * Q, V
a_ = sp.Function("a", positive=True)(t); ph = sp.Function("phi")(t); h = sp.Function("h")(t, z)
dv1, V1 = DdotV(sp.diag(-1, a_ ** 2, a_ ** 2, a_ ** 2), [1, 0, 0, 0], ph)
s1 = sp.simplify(dv1) == 0 and all(sp.simplify(v) == 0 for v in V1)
check("S1", s1, "flat FRW, any a(t), phi(t), comoving unit aether: V^mu = 0 and D.V = q^{mn} nabla_m nabla_n phi + theta Q = 0 identically")
dv4, V4 = DdotV(sp.diag(-1, a_ ** 2 * (1 + h), a_ ** 2 * (1 - h), a_ ** 2), [1, 0, 0, 0], ph)
s4 = sp.simplify(dv4) == 0 and all(sp.simplify(v) == 0 for v in V4)
check("S4", s4, "FRW + finite TT tensor mode h(t,z): V^mu = 0 and D.V = 0 exactly, so the graft term is absent from the tensor sector")
eps, Q0 = sp.symbols("epsilon Q_0")
Psi, Phi, chi, a1, a2, a3 = [sp.Function(n_)(t, x, y, z) for n_ in ("Psi", "Phi", "chi", "a1", "a2", "a3")]
gw = sp.diag(-(1 + 2 * eps * Psi), 1 - 2 * eps * Phi, 1 - 2 * eps * Phi, 1 - 2 * eps * Phi)
Ai = [eps * a1, eps * a2, eps * a3]
A0 = sp.sqrt((1 + sum(gw[i + 1, i + 1] * Ai[i] ** 2 for i in range(3))) / (1 + 2 * eps * Psi))
dvw, _ = DdotV(gw, [A0] + Ai, Q0 * t + eps * chi)
d0 = sp.simplify(dvw.subs(eps, 0)); d1 = sp.simplify(sp.expand(sp.diff(dvw, eps).subs(eps, 0)))
target = sum(sp.diff(chi, c, 2) for c in (x, y, z)) + Q0 * (sp.diff(a1, x) + sp.diff(a2, y) + sp.diff(a3, z))
s2 = d0 == 0 and sp.simplify(d1 - target) == 0 and not d1.has(Psi) and not d1.has(Phi)
check("S2", s2, "weak field (Psi, Phi, chi, a ~ eps, time-dependent): D.V = lap chi + Q0 div a + O(eps^2), no Psi or Phi at O(eps) -> Phi = Psi kept, gamma - 1 = 0")
tder = [d for d in d1.atoms(sp.Derivative) if d.expr == chi and any(v == t for v, _ in d.variable_count)]
check("S3", len(tder) == 0, f"O(eps) part of D.V has no time derivative of chi ({len(tder)} found): the graft adds no kinetic term for chi")
RES["sympy"] = dict(S2_first_order=str(d1), S1=s1, S4=s4)

# ---------------- G2a, G2b, G2gamma
LFLOOR = {"canonical": 21.7, "alt": 22.9}; LGRADE = {f: [LFLOOR[f], 50.0] for f in FOOT}
G = {f: {} for f in FOOT}; TAB = {}
for f, a0 in FOOT.items():
    if MUT:
        s = gA["RES"]["static"][f"{f}|law"]; oh = s["over_Hees_AQUAL_E2"]
        TAB[f] = dict(G2a_over_Hees_AQUAL_E2=oh, Saturn_over_bound=s["Saturn_over_bound"])
        G[f]["G2a"] = all(v <= 1 for v in oh); G[f]["G2b"] = s["Saturn_over_bound"] <= 1
    else:
        cells = {}
        for L in LGRADE[f]:
            for E in EFS:
                q, xx = Q2s(a0, E, L); cells[f"{L:g}|{E}"] = dict(Q2=q, x_e=xx, over_Hees=q / HEES, over_Park=q / PARK)
        planets = {f"{L:g}|muK{m:g}": hedgehog(L, m) for L in LGRADE[f] for m in (0.1, 1.0)}
        TAB[f] = dict(G2a=cells, G2b=planets)
        G[f]["G2a"] = all(c["over_Hees"] <= 1 and c["over_Park"] <= 1 for c in cells.values())
        G[f]["G2b"] = all(v <= 1 for d in planets.values() for v in d.values())
    G[f]["G2gamma"] = bool(s2)
RES["solar_system"] = TAB
if MUT:
    m1 = all(not G[f]["G2a"] and not G[f]["G2b"] for f in FOOT) and worst <= 1e-12
    check("M1", m1, "MUTATE bites: stiffness off reproduces AX1's AeST G2a/G2b failure (to 1e-12) and fails both")

# ---------------- reported: does the switch stay on in the Solar System? Sun's own D.V in the linear model
def Fprof(Sp, Sl, rho, thx, nc=8000, nb=64):
    c = (np.arange(nc) + 0.5) / nc; b = 2 * np.pi * np.arange(nb) / nb; C, B = np.meshgrid(c, b, indexing="ij")
    u = C * math.cos(thx) + np.sqrt(1 - C * C) * math.sin(thx) * np.cos(B); s = Sp * (1 - u * u) + Sl * u * u
    I = 2 * np.sum(np.sqrt(s / 2) * np.exp(-np.sqrt(2 * s) * rho * C)) * (1.0 / nc) * (2 * np.pi / nb)
    return 1.0 - rho / (2 * np.pi) * I   # D.V_sun = (2GM/(L^2 r)) F
f_iso = Fprof(2.0, 2.0, 1.3, 0.4); sw0 = abs(f_iso - math.exp(-2.0 * 1.3)) / math.exp(-2.0 * 1.3)
GAL_MIN = {"canonical": 0.0055, "alt": 0.0062}  # Msun/pc^3, X3 D2 (H4 MW-like disc solver), READ
SW = {}
if not MUT:
    rhos = np.geomspace(0.3, 40.0, 60); ths = np.linspace(0, np.pi / 2, 10)
    for f, a0 in FOOT.items():
        for E in EFS:
            xx = xe(a0, E); Fm, at = 1e9, None
            for r_ in rhos:
                for th_ in ths:
                    v = Fprof(xx, xx * (2 + xx), r_, th_) / r_
                    if v < Fm: Fm, at = v, (float(r_), float(th_))
            for L in LGRADE[f]:
                rho_min = min(Fm, 0.0) / (2 * np.pi * L ** 3)   # Msun/pc^3 for 1 Msun: (M/(2 pi L^2 r)) F
                SW[f"{f}|{E}|{L:g}"] = dict(min_F_over_rho=Fm, at_r_over_L_theta=at, sun_min_rho_ph=rho_min,
                                           margin=(GAL_MIN[f] / abs(rho_min) if rho_min < 0 else float("inf")))
    mins = [v["margin"] for v in SW.values()]
    P(f"  switch: Sun's own D.V minimum in the graft's linear model; smallest margin vs X3's Galactic floor {min(mins):.3g} (iso self-check rel {sw0:.1e})")
check("SW0", sw0 <= 1e-4, f"Sun's-own D.V profile, isotropic self-check vs exp(-sqrt(2S) r/L): rel {sw0:.1e} (<= 1e-4)")
RES["switch_on_check"] = SW

# ---------------- G2c (carried + reading), BG, LAW, G4
KB = sp.Rational(1, 5); Jy = sp.Symbol("J", positive=True); al1 = -4 * (2 + KB * Jy) / (1 + Jy)
ka_as3 = al1.subs(Jy, 1) == sp.Rational(-22, 5); al1_inf = sp.limit(al1, Jy, sp.oo)
RES["G2c"] = dict(entry="F (AX1 AeST, record AS3), carried", branch_a="no sound speed: moving source alpha1 = alpha2 = 0, law lost for moving systems; graft adds no kinetic term (S3) so unchanged",
                  branch_b=f"static-branch alpha1 = -4(2 + K_B J)/(1 + J): {al1.subs(Jy, 1)} at J = 1 (AS3 -22/5 reproduced: {ka_as3}); stiffness drives J_eff -> oo at r << L*: alpha1 -> {al1_inf} = -4 K_B at K_B = 1/5; |alpha1| < 1e-4 needs K_B < 2.5e-5 [READING]")
for f in FOOT: G[f]["G2c"] = False
lk = {}
for L in sorted({v for f in FOOT for v in LGRADE[f]}):
    for r_ in (0.5, 1, 2, 5, 10):
        for xx in (0.05, 0.1, 0.5, 1.0):
            e = (L / (r_ * 1e3)) ** 2 / (2 * xx); lk[f"{L:g}|{r_:g}kpc|x{xx:g}"] = math.log10(1 + e)
law_ok = {f: MUT or max(v for k, v in lk.items() if float(k.split("|")[0]) in LGRADE[f] and float(k.split("|")[1][:-3]) >= 1) <= 0.02 for f in FOOT}
frw = {f"L{L:g}|k{k:g}|z{zz:g}": (L * 1e-6 * k * (1 + zz)) ** 2 / 2 for L in (21.7, 22.9, 50.0) for k in (0.01, 0.1, 0.3) for zz in (0, 1100, 1e4, 1e5)}
RES["background"] = dict(exact_zero=bool(s1 and s4), perturbation_ratio=frw, k1pz_where_ratio_1_perMpc={f"L{L:g}": math.sqrt(2) / (L * 1e-6) for L in (21.7, 22.9, 50.0)},
                         note="CMB not recomputed; background sits on the switch's kink, so linear perturbations see the stiffness only where delta(D.V) > 0")
RES["law_dex"] = lk
for f in FOOT:
    G[f]["BG"] = bool(s1 and s4); G[f]["LAW"] = bool(law_ok[f])
    G[f]["G4"] = MUT  # graft: I1 (v4 ill-posed where the aether twists) applies where D.V > 0; stiffness off: AeST's own G4 'O' (not F)
RES["G4"] = dict(c_T="unchanged from AeST (S4); AeST c_T = c by construction [PROVISIONAL]" if s4 else "S4 failed",
                 health=("AeST's own entry O (X6 H1 not re-read), as AX1" if MUT else "F: graft = v4 where D.V > 0; I1 ill-posed wherever the aether twists (forced off symmetry, I1 K5); the switch removes the stiffness only where D.V < 0"))

# ---------------- labels
RES["gates"] = G; RES["labels"] = {}
bad = [c for c in ("KA0", "KA1", "KA2", "KA3", "S1", "S2", "S3", "S4") if c in FAILS]
P("\nGates and labels")
for f in FOOT:
    failed = [k for k in ("G2a", "G2b", "G2gamma", "G2c", "BG", "LAW", "G4") if not G[f][k]]
    lab = "NOT EVALUABLE [" + ", ".join(bad) + "]" if bad else ("GRAFT PASSES" if not failed else "GRAFT FAILS: " + ", ".join(failed))
    RES["labels"][f] = lab
    P(f"  {f}: {lab}; gates {G[f]}")
    if not MUT:
        cm = max(TAB[f]["G2a"].values(), key=lambda c: c["over_Hees"])
        P(f"    G2a max Q2/Hees {cm['over_Hees']:.3g}, Q2/Park {cm['over_Park']:.3g} (L* {LGRADE[f]}); G2b worst " +
          f"{max(v for d in TAB[f]['G2b'].values() for v in d.values()):.3g} of bound; Mars at floor {TAB[f]['G2b'][f'{LFLOOR[f]:g}|muK0.1']['Mars']:.3f}")
    else:
        P(f"    AeST (stiffness off): Q2/Hees AQUAL E2 {[round(v, 3) for v in TAB[f]['G2a_over_Hees_AQUAL_E2']]}; Saturn {TAB[f]['Saturn_over_bound']:.3g}x")
P(f"  G2c: {RES['G2c']['branch_b']}")
P(f"  law: max dex at r >= 1 kpc, x >= 0.05: " + ", ".join(f"L* {L:g}: {max(v for k, v in lk.items() if float(k.split('|')[0]) == L and float(k.split('|')[1][:-3]) >= 1):.4f}" for L in (21.7, 22.9, 50.0)))
P("  FRW: D.V = 0 exactly on the background; (L* k (1+z))^2/2 at L* 21.7: " + ", ".join(f"k{k:g} z{zz:g} {(21.7e-6 * k * (1 + zz)) ** 2 / 2:.1e}" for k in (0.1, 0.3) for zz in (1100, 1e5)))
RES["failed_checks"] = FAILS
sfx = TAG + ("_MUTATE" if MUT else "")
open(os.path.join(HERE, f"cq5_graft{sfx}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"cq5_graft{sfx}.json"), "w"), indent=1, sort_keys=True, default=str)
sys.exit(1 if MUT or FAILS else 0)
