#!/usr/bin/env python3
"""V3W W2: rerun C6's carried checks (C1, C3-C8) and replace its check C6 by an in-window Route N resolution ladder (C6').

Criteria: FROZEN_CRITERIA.md (37c16dcbaa). C6's code is imported read-only (no bytecode written):
covariant_push_2026_10_22/C6_literal_cassini/c6_solver.py (and D7d's solver through it).
Run:  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 w2_c6_rerun.py      (V3W_MUTATE=1: screening removed)
Each Route N solve runs in its own forked process; RSS is reported per job. Timing goes to stderr only.
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, time, resource, warnings
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import multiprocessing as mp
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
C6DIR = os.path.join(ROOT, "covariant_push_2026_10_22", "C6_literal_cassini")
sys.path.insert(0, C6DIR)
import c6_solver as C          # read-only
S = C.S
MUT = os.environ.get("V3W_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
OUT, CHK = [], {}
RES = {"lane": "V3W_v3s_weak_spots", "part": "W2", "criteria": "37c16dcbaa", "mutate": MUT}
t0 = time.time()


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def T(s):
    print(f"  [{s}; {time.time() - t0:.0f}s]", file=sys.stderr, flush=True)


def check(name, ok, detail):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), detail=str(detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


def rel(*p): return os.path.join(ROOT, *p)
def J(*p): return json.load(open(rel(*p)))
def rss_child():
    sc = 1e9 if sys.platform == "darwin" else 1e6
    return resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / sc


# ---------------------------------------------------------------- C6's inputs, as C6 used them
GM = 1.32712440018e20; AU = 1.495978707e11; PC = 3.0857e16
A0C6 = {"canonical": 9.36e-11, "alt": 1.13e-10}
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
R_SAT = 9.58 * AU
BN11 = (3.8e-26, 1.2e-10, 1.9e-10)
d7b = J("doors_push_2026_10_22", "D7b_cassini_Q2", "d7b_cassini_q2_results.json")
EV = {f: {E: dict(gNe=v["gNe"], ge=v["ge_total"]) for E, v in d7b["grid"][f]["none"].items()} for f in A0C6}
e2 = J("doors_push_2026_10_22", "E2_field_equation", "e2_field_equation_results.json")
E2AQ = {E: e2["R1"]["canonical|none"]["cells"][E]["Q2_AQUAL"] for E in ("E0", "E1", "E2", "E3")}
C6J = J("covariant_push_2026_10_22", "C6_literal_cassini", "c6_literal_cassini_results.json")
C6PJ = J("rebuild_2026_10_22", "C6P_cassini_high_precision", "c6p_cassini_hp.json")
G1, G2 = (30, 48), (40, 64)
def rich(q1, q2): return (16 * q2 - 9 * q1) / 7
def rM_of(a0): return math.sqrt(GM / a0)
def xe_of(f, E): return EV[f][E]["ge"] / A0C6[f]
def toQ(raw, a0): return -raw * a0 / rM_of(a0)


def isolated(fn, *a):
    with mp.get_context("fork").Pool(1, maxtasksperchild=1) as pool:
        return pool.apply(fn, a)


def grid(Lam, gres): return S.Grid(1e-4, (1e3 if Lam <= 30 else 300.0) * max(1.0, Lam), gres[0], gres[1])


def run_v(Lam, xe, gres, rF=0.0, U0g=None, tol=1e-9):
    g = grid(Lam, gres)
    U0 = None if U0g is None else S.regrid(U0g[0], U0g[1], g)
    U, fin, it = C.solve_v(g, Lam, xe, rF, U0=U0, mutate=False, tol=tol)
    return g, U, fin, it


def _qn1(Lam, xe, a0, gres, rqs):
    g, U, fin, it = run_v(Lam, xe, gres)
    sc = 1e9 if sys.platform == "darwin" else 1e6
    return [toQ(S.q2_raw(g, U[0], rq / rM_of(a0)), a0) for rq in rqs], fin, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / sc


def QN(Lam, xe, a0):
    out = [isolated(_qn1, Lam, xe, a0, gres, [R_SAT]) for gres in (G1, G2)]
    qq = [o[0][0] for o in out]
    return qq, rich(*qq), max(o[2] for o in out)


def cmp(new, old):
    return abs(new - old) / max(abs(old), 1e-300)


P("=" * 100)
P("V3W W2: C6's carried checks rerun (C6's inputs, C6's pass lines) + C6' in-window ladder" + ("  [MUTATE: screening removed]" if MUT else ""))
P("kappa = 1/2 FITTED; footings never pooled; adopts nothing; not theory closed.")
P("=" * 100)
REPRO = {}

# ---------------------------------------------------------------- C1 (sympy), C6's code path verbatim
import sympy as sy
x, y, z = sy.symbols("x y z", real=True)
K, a0s, L = sy.symbols("K a0 L", positive=True)
Phi = sy.Function("Phi")(x, y, z); rho = sy.Function("rho")(x, y, z)
Pv = [sy.Function(f"P{i}")(x, y, z) for i in (1, 2, 3)]
X = (x, y, z)
gL = K * L ** 2 / 2
Pm = sy.sqrt(sum(p ** 2 for p in Pv)); u = K * Pm
W = (a0s ** 2 / K) * (-u / a0s - sy.log(1 - u / a0s))
divP = sum(sy.diff(Pv[i], X[i]) for i in range(3))
Lag = -sum(sy.diff(Phi, X[i]) ** 2 for i in range(3)) / (2 * K) + sum(Pv[i] * sy.diff(Phi, X[i]) for i in range(3)) - W - gL / 2 * divP ** 2 - rho * Phi
from sympy.calculus.euler import euler_equations
EL = euler_equations(Lag, [Phi] + Pv, X)
lap = sum(sy.diff(Phi, X[i], 2) for i in range(3))
pv = [K * p for p in Pv]; pm = K * Pm; divp = K * divP
resL = sy.simplify(K * EL[0].lhs - (lap - K * rho - divp))
h = [a0s * pv[i] / (a0s - pm) for i in range(3)]
resP = [sy.simplify(EL[i + 1].lhs - (sy.diff(Phi, X[i]) + (L ** 2 / 2) * sy.diff(divp, X[i]) - h[i])) for i in range(3)]
kap, c_, jp, jl = sy.symbols("kappa c j_p j_l", positive=True)
s_ = sy.sqrt(1 - c_ ** 2); kh = sy.Matrix([s_, c_])
Am = (kap ** 2 / 2) * kh * kh.T + sy.diag(jp, jl) - kh * kh.T
m_ = (1 - c_ ** 2) / jp + c_ ** 2 / jl
resK = sy.simplify((kh.T * Am.inv() * kh)[0] - m_ / (1 - m_ + kap ** 2 * m_ / 2))
ok1 = resL == 0 and all(r_ == 0 for r_ in resP) and resK == 0
REPRO["C1"] = "reproduced" if ok1 and C6J["checks"]["C1"]["ok"] else "failed"
check("C1", ok1, f"(L), (P_L), kernel residuals {resL}, {resP}, {resK} (all 0); C6 recorded PASS -> {REPRO['C1']}")
T("C1")

# ---------------------------------------------------------------- C3
g3 = S.Grid(1e-4, 3e4, 20, 16)
A_me, b_me, nl_me = C.build(g3, 30.0, 1.0)
A_d, b_d, nl_d = S.build(g3, 30.0, False, "stiff")
dA = float(abs(A_me - A_d).max()); db = float(np.max(np.abs(b_me - b_d)))
A_0, _, _ = C.build(g3, 30.0, 0.0, False)
d0 = float(abs(A_0 - A_d).max())
ok3 = dA == 0.0 and db == 0.0 and bool(np.all(nl_me == nl_d))
REPRO["C3"] = "reproduced" if ok3 and d0 == C6J["C3"]["rF0_differs_from_rF1"] else ("changed" if ok3 else "failed")
check("C3", ok3, f"r_F=1 build vs D7d build: max|dA| {dA:.1e}, max|drhs| {db:.1e} (== 0); r_F=0 differs by {d0:.6e} (C6 {C6J['C3']['rF0_differs_from_rF1']:.6e}) -> {REPRO['C3']}")

# ---------------------------------------------------------------- C4 AQUAL anchor (L* = 0)
qq, Rb, m4 = QN(0.0, BN11[2] / BN11[1], BN11[1])
c4 = dict(BN11=dict(Q=qq, R=Rb)); worst = 0.0; dmax = cmp(Rb, C6J["C4_AQUAL"]["BN11"]["R"])
for E in E2AQ:
    qq, R, mm = QN(0.0, xe_of("canonical", E), A0C6["canonical"]); m4 = max(m4, mm)
    c4[E] = dict(Q=qq, R=R); worst = max(worst, abs(R / E2AQ[E] - 1)); dmax = max(dmax, cmp(R, C6J["C4_AQUAL"][E]["R"]))
ok4 = abs(Rb / BN11[0] - 1) < 0.10 and worst < 0.03
REPRO["C4"] = ("reproduced" if dmax <= 1e-9 else "changed") if ok4 else "failed"
RES["C4"] = dict(cells=c4, max_rel_vs_C6=dmax, rss_GB=m4)
check("C4", ok4, f"L*=0 AQUAL: BN11 {Rb:.4e} (ratio {Rb / BN11[0]:.4f}); E2 canonical max|ratio-1| {worst:.2e} (<3e-2); vs C6 max rel {dmax:.1e} -> {REPRO['C4']}"); T(f"C4 RSS {m4:.2f} GB")
T("C4")

# ---------------------------------------------------------------- C5 Route N vs Route F at Lam = 30, 100
a0 = A0C6["canonical"]; c5 = {}; worst = 0.0; signok = True; dmax = 0.0; m5 = 0.0
for Lam in (30.0, 100.0):
    for E in ("E0", "E3"):
        xe = xe_of("canonical", E)
        qq, R, mm = QN(Lam, xe, a0); F = C.routeF_Q2(GM, Lam * rM_of(a0), xe, 0.0); m5 = max(m5, mm)
        c5[f"{Lam:g}_{E}"] = dict(Q=qq, R=R, F=F, ratio=R / F); worst = max(worst, abs(R / F - 1)); signok &= (R > 0) == (F > 0)
        dmax = max(dmax, cmp(R, C6J["C5_N_vs_F"][f"{Lam:g}_{E}"]["R"]))
ok5 = worst < 0.05 and signok
REPRO["C5"] = ("reproduced" if dmax <= 1e-9 else "changed") if ok5 else "failed"
RES["C5"] = dict(cells=c5, max_rel_vs_C6=dmax, rss_GB=m5)
check("C5", ok5, f"max|N/F-1| {worst:.2e} at Lam 30, 100 (E0, E3), sign agree {signok} (<5e-2); vs C6 max rel {dmax:.1e} -> {REPRO['C5']}"); T(f"C5 RSS {m5:.2f} GB")
T("C5")

# ---------------------------------------------------------------- C6 as recorded (Lam = 0.01 vs 0, one grid)
def _c6(xe2, a0):
    rq = R_SAT / rM_of(a0)
    g0, U0, f0, _ = run_v(0.0, xe2, G1); Q0 = toQ(S.q2_raw(g0, U0[0], rq), a0)
    gs, Us, fs, _ = run_v(0.01, xe2, G1, U0g=(U0, g0)); Qs = toQ(S.q2_raw(gs, Us[0], rq), a0)
    return Q0, Qs, f0, fs
Q0, Qs, f0, fs = isolated(_c6, xe_of("canonical", "E2"), a0)
ok6 = abs(Qs / Q0 - 1) < 0.02
d6 = max(cmp(Q0, C6J["C6"]["Q_L0"]), cmp(Qs, C6J["C6"]["Q_L001"]))
REPRO["C6"] = ("reproduced (still unconverged, weak)" if d6 <= 1e-9 and fs >= 1e-9 else ("changed" if ok6 else "failed"))
RES["C6_as_recorded"] = dict(Q_L0=Q0, Q_L001=Qs, residual=[f0, fs], max_rel_vs_C6=d6)
P(f"C6 (as recorded, not graded) ratio Lam=0.01/0 - 1 = {Qs / Q0 - 1:+.2e} (<2e-2: {ok6}); residual at Lam=0.01 {fs:.2e} "
  f"({'converged' if fs < 1e-9 else 'NOT converged'}); vs C6 max rel {d6:.1e} -> {REPRO['C6']}")
RES.setdefault("checks", {})["C6_as_recorded"] = dict(ok=bool(ok6), detail=REPRO["C6"], graded=False)
T("C6 as recorded")

# ---------------------------------------------------------------- C7
xe = xe_of("canonical", "E2")
i1 = C.routeF_I2(xe, 0.0); i2 = C.routeF_I2(xe, 0.0, nk=8000, nc=128, kmin=1e-5, kmax=2e4)
cq = np.polynomial.legendre.leggauss(256); P2 = 0.5 * (3 * cq[0] ** 2 - 1)
kb = 1e3; num = 2.5 * (C.chi_gen(kb, cq[0], xe, 0.0) * P2 * cq[1]).sum() * kb ** 4
tail_rel = abs(num / (-4 * C.tail_c2(xe, 0.0)) - 1)
ok7 = abs(i2 / i1 - 1) < 1e-6 and tail_rel < 1e-4
d7 = max(cmp(i1, C6J["C7"]["I2"]), cmp(i2, C6J["C7"]["I2_fine"]), cmp(tail_rel, C6J["C7"]["tail_rel"]))
REPRO["C7"] = ("reproduced" if d7 <= 1e-9 else "changed") if ok7 else "failed"
check("C7", ok7, f"I2 refinement {abs(i2 / i1 - 1):.2e} (<1e-6); tail {tail_rel:.2e} (<1e-4); vs C6 max rel {d7:.1e} -> {REPRO['C7']}")

# ---------------------------------------------------------------- C8
worst = 0.0
for f in A0C6:
    for E in EV[f]:
        xe = xe_of(f, E); worst = max(worst, GM / (24 * PC) ** 2 * (1 + xe) ** 2 / (A0C6[f] * xe))
ok8 = worst < 1e-4
rec8 = float(C6J["checks"]["C8"]["detail"].split("= ")[1].split(" ")[0])
REPRO["C8"] = ("reproduced" if abs(worst - rec8) / rec8 < 5e-3 else "changed") if ok8 else "failed"     # C6 printed 3 digits
check("C8", ok8, f"max (GM/L*^2)(1+x_e)^2/(a0 x_e) at 24 pc {worst:.4e} (<1e-4); C6 printed {rec8:.2e} -> {REPRO['C8']}")
T("C7, C8")

# ---------------------------------------------------------------- C6' in-window ladder (exact footings, E2)
LADDER = [(20, 32), (30, 48), (40, 64)]
RQS = [R_SAT, 10 * R_SAT, 100 * R_SAT]
GRADED = 2                                  # index of 100 r_Saturn
GE = {f: d7b["grid"][f]["none"]["E2"]["ge_total"] for f in FOOT}
c6p = {}; ok6p = True
for f, A in FOOT.items():
    xe2 = GE[f] / A; rM = rM_of(A)
    for Ltag, Lam in (("Lam100", 100.0), ("L24pc", 24 * PC / rM)):
        Lam_run = 0.0 if MUT else Lam                 # MUTATE: screening removed -> AQUAL
        rows = [isolated(_qn1, Lam_run, xe2, A, gres, RQS) for gres in LADDER]
        Q = np.array([r_[0] for r_ in rows]); res_ = [r_[1] for r_ in rows]; rs = [r_[2] for r_ in rows]
        conv = all(v < 1e-9 for v in res_)
        q = Q[:, GRADED]
        d12, d23 = abs(q[1] - q[0]), abs(q[2] - q[1])
        Rr = rich(q[1], q[2])
        F = C.routeF_Q2(GM, Lam * rM, xe2, 0.0)
        lad_ok = conv and d23 < d12 and abs(Rr / q[2] - 1) < 2e-2
        nf_ok = abs(Rr / F - 1) < 5e-2 and (Rr > 0) == (F > 0)
        mem_ok = max(rs) < 1.0
        okc = lad_ok and nf_ok and mem_ok
        ok6p &= okc
        c6p[f"{f}|{Ltag}"] = dict(Lam=Lam, x_e=xe2, Q_by_rung_by_radius=Q.tolist(), residuals=res_, rss_GB=rs, d12=d12, d23=d23,
                                 richardson=Rr, rich_vs_finest=Rr / q[2] - 1, routeF=F, N_over_F=Rr / F, ok=okc,
                                 per_radius_N_over_F=[float(rich(Q[1, j], Q[2, j]) / F) for j in range(3)])
        P(f"  C6' {f:9s} {Ltag:6s} Lam={Lam:7.1f}: Q2@100 r_Sat by rung " + " ".join(f"{v:.5e}" for v in q) +
          f"; residuals max {max(res_):.1e}; Richardson {Rr:.5e} (vs finest {Rr / q[2] - 1:+.1e}); Route F {F:.5e}; N/F {Rr / F:.5f}; "
          f"N/F at 1, 10, 100 r_Sat " + ", ".join(f"{v:.4f}" for v in c6p[f'{f}|{Ltag}']['per_radius_N_over_F']) + f" -> {'ok' if okc else 'FAIL'}"); T(f"RSS max {max(rs):.2f} GB")
        T(f"C6' {f} {Ltag}")
RES["C6prime"] = c6p
check("C6'", ok6p, "in-window Route N ladder (20,32)/(30,48)/(40,64): converged, shrinking steps, Richardson within 2e-2 of finest, N/F within 5e-2, RSS < 1 GB, every cell")

# ---------------------------------------------------------------- label
RES["reproduction"] = REPRO
P("")
P("Reproduction status: " + "; ".join(f"{k} {v}" for k, v in REPRO.items()))
c6p_gate = C6PJ["labels"]
q2max = {f: max(v["Q2_f"] for v in C6PJ["gate"][f]["G2a"].values()) for f in FOOT}
labels = {}
for f in FOOT:
    rerun_ok = all(CHK[k] for k in ("C1", "C3", "C4", "C5", "C7", "C8"))
    band_ok = q2max[f] <= 9.0e-27 and c6p_gate[f] == "PASS"
    if MUT:
        q2m = max(c6p[f"{f}|L24pc"]["Q_by_rung_by_radius"][2][0], 0.0)
        band_ok = q2m <= 9.0e-27
    if rerun_ok and CHK["C6'"] and band_ok:
        labels[f] = f"PASS: C1, C3-C5, C7, C8 rerun ({', '.join(sorted(set(REPRO[k] for k in ('C1','C3','C4','C5','C7','C8'))))}); C6' in-window ladder passes; C6P Q2 max {q2max[f]:.2e} s^-2 <= 9.0e-27"
    elif rerun_ok and not band_ok:
        labels[f] = f"FAIL: Q2 outside the Hees band"
    else:
        bad = [k for k in ("C1", "C3", "C4", "C5", "C7", "C8", "C6'") if not CHK[k]]
        labels[f] = f"UNDECIDED: {bad} failed"
    P(f"W2 [{f}]: {labels[f]}")
RES["labels"] = labels
n_ok = sum(CHK.values())
P(f"\nW2 COMPLETE: {n_ok}/{len(CHK)} checks PASS")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o
for k in list(RES.get("C4", {}).keys()) + []:
    pass
# RSS values differ run to run; keep them in a side file so the main JSON/.out are byte-comparable
side = {"C4": RES.get("C4", {}).pop("rss_GB", None), "C5": RES.get("C5", {}).pop("rss_GB", None),
        "C6prime": {k: v.pop("rss_GB") for k, v in c6p.items()}}
json.dump(clean(RES), open(os.path.join(HERE, f"w2_c6_rerun{TAG}.json"), "w"), indent=1, sort_keys=True)
json.dump(clean(side), open(os.path.join(HERE, f"w2_c6_rerun{TAG}_rss.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, f"w2_c6_rerun{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n_ok == len(CHK) else 1)
