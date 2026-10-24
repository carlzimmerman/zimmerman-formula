#!/usr/bin/env python3
"""ZT_zstar_tests / Z-T3: well-posedness of design Z*'s two-sided obstacle 0 <= D.P <= rho_d (R1), on X3's machinery.

Frozen line: Z1_successor_design/TEST_PLAN.md section 2 (0d1959a4f5); implementation choices: FROZEN_CRITERIA.md section 4.
Part B: X3's nonlinear principal symbol c^2 = (s0 + rho_d)(gamma_L/2) F''(s0) with the switched stiffness plus the upper wall.
Part C: X3's slab (its slab() exec'd from X3's source text; K0 reproduces X3's committed C2 ladder) and this lane's two-sided
copy: held density s0^Z = min(s0, rho_d), rho_tau = s0^Z + rho_d, stiffness on s0^Z > 0; the one-sided linearisation at the
wall is bracketed by (ii) RELEASED (saturated nodes keep gamma_L) and (i) PINNED (delta(D.P) = 0 there: gamma -> infinity,
taken as gamma_sat = 1e6 with a 1e4 convergence check).

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 zt3_two_sided_obstacle.py [--mutate]
      --mutate: the switch removed (Theta = 1) inside the two-sided ladders and F = s^2 in the symbol; the slab line must FAIL.
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import json, math, os, resource, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import scipy.linalg as sla
import sympy as sp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []; CHECKS = []
RES = {"lane": "ZT_zstar_tests", "test": "Z-T3", "plan": "Z1_successor_design/TEST_PLAN.md @ 0d1959a4f5", "mutate": MUT}


def say(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(k, ok, val, thr, what=""):
    CHECKS.append((k, bool(ok))); say(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  -- {what}")
    RES.setdefault("checks", {})[k] = dict(pass_=bool(ok), value=str(val), threshold=str(thr), what=what)


def rss_gb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


say(f"Z-T3 two-sided obstacle 0 <= D.P <= rho_d (Z* v3s-OC) {'MUTATE (switch removed)' if MUT else 'normal run'}")
say("kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. Cold energy, no particle. Not 'theory closed'.\n")

G_SI = 6.67430e-11; PC = 3.0856775814913673e16
LSTAR = {"canonical": 21.680757539917785, "alt": 22.847696106846282}      # D10 central floors (pc), as X3
LAMBDA_PC = (100.0, 1000.0)

# ============================================================ PART B: principal symbol with the upper wall (sympy)
s, s0 = sp.symbols("s s_0", real=True)
pos = dict(positive=True)
rd_, gL_, sn_, eps_ = sp.symbols("rho_d gamma_L s_n epsilon", **pos)
P_ = sp.Symbol("P", nonnegative=True)
oo_, kk_, h1 = sp.symbols("omega k h_1")
Msym = sp.Matrix([[-sp.I * oo_, sp.I * kk_ * (s0 + rd_)], [sp.I * kk_ * h1, -sp.I * oo_]])        # X3's frozen-coefficient system
c2gen = sp.simplify(sp.solve(sp.Eq(Msym.det(), 0), oo_)[0] ** 2 / kk_ ** 2)                       # = (s0 + rho_d) h1
F_sw = s ** 2 if MUT else sp.Piecewise((s ** 2, s > 0), (0, True))
F_wall = F_sw + P_ * sp.Piecewise(((s - rd_) ** 2, s > rd_), (0, True))                             # exact penalty; P -> oo = obstacle


def c2_of(F, s0val):
    return sp.simplify(c2gen.subs(h1, gL_ / 2 * sp.diff(F, s, 2)).subs(s, s0val).subs(s0, s0val))


t_ = sp.Symbol("t", positive=True)


def c2_region(s0expr, sw_on, pen_on):
    """c^2 on a region where the branch of each Piecewise is known (switch on/off, wall penalty on/off)."""
    F2 = (2 if (sw_on or MUT) else 0) + (2 * P_ if pen_on else 0)
    return sp.simplify((s0expr + rd_) * gL_ / 2 * F2)


c2_below = c2_region(rd_ / (1 + t_), True, False)       # 0 < s0 < rho_d: stiff band, approaching the wall from below
c2_at = sp.simplify(sp.limit(c2_below, t_, 0, "+"))     # one-sided value in the saturated set {s0 = rho_d}
c2_above = c2_region(rd_ * (1 + t_), True, True)        # penalty side (wall pushed), P >= 0
c2_soft = c2_region(-(rd_ + sn_), False, False)         # soft region rho_tau < 0 (the wall does not reach it)
# cross-check of the branch bookkeeping against the Piecewise forms at numeric points (rho_d 0.1, gamma_L 1, P 3)
num = {rd_: 0.1, gL_: 1, P_: 3}
xchk = max(abs(float(c2_of(F_wall, sp.Float(v)).subs(num)) - float(e_.subs(num).subs(t_, tv)))
           for v, e_, tv in ((0.1 / 1.25, c2_below, 0.25), (0.1 * 1.25, c2_above, 0.25)))
xchk = max(xchk, abs(float(c2_of(F_wall, sp.Float(-0.15)).subs(num)) - float(c2_soft.subs(num).subs(sn_, 0.05))))
ok_at = bool(c2_at.is_positive)
ok_above = bool(c2_above.is_nonnegative)
# footings: gamma_L = K L*^2 / 2 with K = 4 pi G (SI), saturated set for rho_d = 1e-3 .. 1 Msun/pc^3, P = 0, 1, 1e6
MSUN_PC3 = 1.98847e30 / PC ** 3
foot_vals = {}
for f, L in LSTAR.items():
    gv = 4 * math.pi * G_SI * (L * PC) ** 2 / 2
    foot_vals[f] = [float(c2_at.subs({gL_: gv, rd_: r_ * MSUN_PC3})) for r_ in (1e-3, 1e-1, 1.0)] + \
                   [float(c2_above.subs({gL_: gv, rd_: r_ * MSUN_PC3, t_: 0.1, P_: Pv})) for r_ in (1e-3, 1.0) for Pv in (0, 1, 1e6)]
ok_feet = all(v >= 0 for vs in foot_vals.values() for v in vs)
# diagnostics: a smoothed wall reaching the soft region, and a penalty whose support starts at rho_d - eps
F_soft = F_sw + P_ * ((s - rd_ + sp.sqrt((s - rd_) ** 2 + eps_ ** 2)) / 2) ** 2
c2_soft_smooth = c2_of(F_soft, -(rd_ + sn_))
vals_smooth = [float(c2_soft_smooth.subs({gL_: 1, rd_: 0.1, sn_: 0.05, P_: 1, eps_: e_})) for e_ in (1e-3, 1e-2, 1e-1)]
shift_rows = []
for e_ in (0.05, 0.19, 0.21, 0.5):
    lo_ = 0.1 - e_
    sv = 0.5 * (lo_ - 0.1) if lo_ < -0.1 else -0.1 - 1e-3            # a rho_tau < 0 point inside the support if one exists
    F_shift = F_sw + P_ * sp.Piecewise(((s - lo_) ** 2, s > lo_), (0, True))
    shift_rows.append((e_, sv, float(c2_of(F_shift, sp.Float(sv)).subs({gL_: 1, rd_: 0.1, P_: 1}))))
say("PART B (principal symbol, X3's B2-S with the upper wall):")
say(f"   c^2 = {c2gen} with h1 = (gamma_L/2) F''(s0)")
say(f"   saturated set, from below: c^2 -> {c2_at}; penalty side s0 = rho_d (1 + t): {c2_above}; soft side s0 = -(rho_d + s_n): {c2_soft}")
say(f"   footings (gamma_L = 4 pi G L*^2 / 2 at the D10 floors; rho_d 1e-3..1 Msun/pc^3; P 0/1/1e6): min c^2 "
    + ", ".join(f"{f} {min(v):.3e}" for f, v in foot_vals.items()) + " m^2 s^-2 (SI)")
say(f"   diagnostic: smoothed wall in the soft region (rho_d 0.1, s_n 0.05, eps 1e-3/1e-2/1e-1): c^2 {[f'{v:.2e}' for v in vals_smooth]}")
say(f"   diagnostic: penalty support from rho_d - eps (rho_d 0.1): " + "; ".join(f"eps {e_}: c^2({sv:.3f}) {c:.2e}" for e_, sv, c in shift_rows)
    + "  [c^2 < 0 possible iff eps > 2 rho_d]")
check("B2-Z", ok_at and ok_above and ok_feet and xchk < 1e-12,
      f"saturated set c^2 = {c2_at} > 0 (rho_d > 0); penalty side >= 0: {ok_above}; both footings >= 0: {ok_feet}; branch x-check {xchk:.0e}",
      "c^2 >= 0 everywhere in the saturated set for rho_d > 0, both footings", "frozen symbol line")
RES["B"] = dict(c2_general=str(c2gen), c2_saturated=str(c2_at), c2_penalty_side=str(c2_above), c2_soft=str(c2_soft),
                footing_values=foot_vals, smoothed_wall_soft_region=vals_smooth, shifted_penalty=shift_rows)

# ============================================================ PART C: slab (X3's slab exec'd; two-sided copy)
X3SRC = open(os.path.join(REB, "X3_switched_stiffness", "x3_switched_stiffness.py")).read()
i0 = X3SRC.index("def slab("); i1 = X3SRC.index("def _slab_task(", i0)
NSX = {"np": np, "sla": sla, "math": math, "MUTATE": False}
exec(X3SRC[i0:i1], NSX)
slab_x3 = NSX["slab"]
X3J = json.load(open(os.path.join(REB, "X3_switched_stiffness", "x3_switched_stiffness_results.json")))
ref = X3J["C"]["C2_0.001"]
k0 = max(abs(slab_x3(r_["N"], 1e-3, rho_d=0.1, grid="unaligned")[0] / r_["Gamma"] - 1) for r_ in ref)
check("K0", k0 <= 1e-9, f"max rel |Gamma - X3 C2 (gamma_L 1e-3, N 64-1024)| {k0:.1e}", "<= 1e-9", "X3's slab exec'd from source reproduces X3")


def slab2(N, gL, rho_d, case, grid="unaligned", wall=True, lower=False, gsat=1e6, K=1.0, M=2.0):
    """two-sided copy of X3's slab.  case 'released' | 'pinned'.  wall=False: no upper obstacle (X3's operator)."""
    i = np.arange(N); zf = (i + 0.5) / N; zn = i / N
    sf = -0.5 + np.cos(2 * np.pi * zf); sn_ = -0.5 + np.cos(2 * np.pi * zn)
    if grid == "aligned":                                   # X3's aligned zero-dust grid: node zeros at m = N/6
        m = np.minimum(i, N - i); sn_ = np.where(6 * m == N, 0.0, sn_)
    hi = rho_d if wall else np.inf
    sfz = np.minimum(sf, hi); snz = np.minimum(sn_, hi)
    if lower:
        sfz = np.maximum(sfz, 0.0); snz = np.maximum(snz, 0.0)
    rho = sfz + rho_d
    on = (snz > 0).astype(float)
    if MUT:
        on = np.ones(N)
    sat = (sn_ >= rho_d) if wall else np.zeros(N, bool)
    if lower:
        sat = sat | (sn_ <= 0)
    gam = gL * on
    if case == "pinned":
        gam = np.where(sat, gsat, gam)
    h = 1.0 / N; E = np.eye(N); Dm = (E - np.roll(E, 1, axis=0)) / h
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        L = K * (M - 1) * E + (K / N) * np.ones((N, N)) + Dm.T @ (gam[:, None] * Dm)
    stiff = (gam > 0)
    viol = int(np.sum(stiff & ((rho < 0) | (np.roll(rho, 1) < 0))))
    Q = sla.null_space(np.ones((1, N)))
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        A = Q.T @ (-rho[:, None] * Q); Xs = sla.solve(L, Q, assume_a="pos"); B = Q.T @ Xs
    B = 0.5 * (B + B.T); A = 0.5 * (A + A.T)
    w = sla.eigh(A, B, eigvals_only=True, subset_by_index=[N - 2, N - 2])
    Gm = math.sqrt(max(float(w[0]), 0.0))
    neg = rho < 0; fm = neg.mean()
    bound = math.sqrt(K * (M - 1 + fm) * (np.max(-rho[neg]) if neg.any() else 0.0))
    return dict(N=N, Gamma=Gm, bound=bound, violations=viol, n_sat=int(sat.sum()), frac_neg=float(fm))


k1 = max(abs(slab2(N, 1e-3, 0.1, "released", wall=False)["Gamma"] / slab_x3(N, 1e-3, rho_d=0.1, grid="unaligned")[0] - 1)
         for N in (64, 256)) if not MUT else 0.0
check("K1", k1 <= 1e-12, f"two-sided copy with the wall removed vs X3's slab: max rel {k1:.1e}", "<= 1e-12 (skipped under MUTATE)",
      "the copy differs from X3 only by the wall")
# pinning convergence: gamma_sat 1e4 vs 1e6 (finest level of the canonical lambda = 100 pc ladder)
gfoot = {(f, lam): LSTAR[f] ** 2 / (2 * lam ** 2) for f in LSTAR for lam in LAMBDA_PC}
g_a = slab2(512, gfoot[("canonical", 100.0)], 0.1, "pinned", gsat=1e4)["Gamma"]
g_b = slab2(512, gfoot[("canonical", 100.0)], 0.1, "pinned", gsat=1e6)["Gamma"]
check("K2", abs(g_b / g_a - 1) <= 1e-3, f"pinned Gamma at gamma_sat 1e4 / 1e6 (N 512): {g_a:.7f} / {g_b:.7f}", "agree to 1e-3",
      "the pinned limit is reached (delta(D.P) = 0 on saturated nodes)")

NS_ = (64, 128, 256, 512, 1024)
LAD = {}
say("\nPART C (slab; K = 1, M = 2, s0 = -0.5 + cos 2 pi z; rho_d = 0.1; unaligned grid; X3's bound):")
say(f"   footing gamma_L = L*^2/(2 lambda^2): " + ", ".join(f"{f} lambda {int(l)} pc {g:.4e}" for (f, l), g in gfoot.items()))
prim_ok = True; prim_fail = False
for (f, lam), gv in gfoot.items():
    for case in ("released", "pinned"):
        lad = [slab2(N, gv, 0.1, case) for N in NS_]
        Gs = [r_["Gamma"] for r_ in lad]; ratio = Gs[-1] / Gs[-2]
        okb = all(r_["Gamma"] <= r_["bound"] * (1 + 1e-9) for r_ in lad)
        conv = abs(ratio - 1) <= 0.10
        LAD[f"{f}|{int(lam)}|{case}"] = dict(ladder=lad, finest_ratio=ratio, bound_ok=okb, converged=conv)
        prim_ok &= conv and okb; prim_fail |= ratio > 1.10
        say(f"   {f:9s} lambda {int(lam):4d} pc {case:8s}: Gamma {[round(g, 6) for g in Gs]}; finest ratio {ratio:.5f}; "
            f"bound {lad[-1]['bound']:.5f} held {okb}; saturated nodes {lad[-1]['n_sat']}/{NS_[-1]}; violations {[r_['violations'] for r_ in lad]}")
    if rss_gb() > 0.95:
        say("RSS GUARD"); sys.exit(3)
for case in ("released", "pinned"):
    lad = [slab2(N, 1e-3, 0.1, case) for N in NS_]; Gs = [r_["Gamma"] for r_ in lad]
    LAD[f"X3gL1e-3|{case}"] = dict(ladder=lad, finest_ratio=Gs[-1] / Gs[-2])
    say(f"   X3's gamma_L 1e-3   {case:8s}: Gamma {[round(g, 6) for g in Gs]}; finest ratio {Gs[-1] / Gs[-2]:.5f} (X3 C2 without the wall: 1.183214)")
check("C-Z", prim_ok, f"all 8 primary ladders converge (finest ratios {min(v['finest_ratio'] for k, v in LAD.items() if not k.startswith('X3')):.5f}-"
      f"{max(v['finest_ratio'] for k, v in LAD.items() if not k.startswith('X3')):.5f}) and Gamma <= bound at every level: {prim_ok}",
      "|ratio - 1| <= 0.10; Gamma <= sqrt(K(M - 1 + f_-) max|rho_-|)", "frozen slab line (both brackets, both footings, both lambda)")
RES["C_primary"] = LAD

# ---------------- diagnostics (no verdict weight)
say("\n   diagnostics (no verdict weight):")
DIAG = {}
# A1 (dev run, memory): the first run hit this lane's 0.95 GB guard at N = 2048 in these diagnostics (after every verdict line had
# printed: B2-Z PASS, C-Z PASS); diagnostic ladders are now capped at N = 1024 (aligned 768).
for lab, kw, Ns in (("rho_d 0.01 unaligned", dict(rho_d=0.01), (64, 128, 256, 512, 1024)),
                    ("rho_d 0 aligned (wall = switch)", dict(rho_d=0.0, grid="aligned"), (48, 96, 192, 384, 768)),
                    ("rho_d 0 unaligned (wall = switch)", dict(rho_d=0.0), (64, 128, 256, 512, 1024)),
                    ("lower obstacle literal, rho_d 0.1", dict(rho_d=0.1, lower=True), (64, 256, 1024))):
    for case in ("released", "pinned"):
        lad = [slab2(N, 1e-2, case=case, **kw) for N in Ns]; Gs = [r_["Gamma"] for r_ in lad]
        ratio = Gs[-1] / Gs[-2] if Gs[-2] > 0 else float("nan")
        slope = math.log(Gs[-1] / Gs[-2]) / math.log(Ns[-1] / Ns[-2]) if Gs[-2] > 0 and Gs[-1] > 0 else float("nan")
        DIAG[f"{lab}|{case}"] = dict(ladder=lad, finest_ratio=ratio, slope=slope)
        say(f"   {lab:34s} {case:8s} (gamma_L 1e-2): Gamma {[round(g, 5) for g in Gs]}; finest ratio {ratio:.4f}; slope {slope:.3f}; "
            f"violations {[r_['violations'] for r_ in lad]}")
        if rss_gb() > 0.95:
            say("RSS GUARD"); sys.exit(3)
gs_scan = {gs: slab2(384, 1e-2, 0.0, "pinned", grid="aligned", gsat=gs)["Gamma"] for gs in (1e2, 1e4, 1e6)}
DIAG["rho_d 0 aligned pinned, N 384, gamma_sat scan"] = gs_scan
say(f"   rho_d 0 aligned pinned, N 384: Gamma at gamma_sat 1e2 / 1e4 / 1e6 = " + " / ".join(f"{v:.4g}" for v in gs_scan.values())
    + "  (Gamma ~ sqrt(gamma_sat): the zero-dust pinned limit has no finite rate)")
RES["C_diagnostics"] = DIAG

# ============================================================ verdict (frozen)
pk = rss_gb(); check("K3", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB", "memory")
ck = dict(CHECKS)
if ck.get("B2-Z") and ck.get("C-Z"):
    V = "PASS"
elif prim_fail or not ck.get("B2-Z"):
    V = "FAIL"
else:
    V = "UNDECIDED"
RES["verdict"] = V
say(f"\nZ-T3 FROZEN VERDICT: {V}  (symbol B2-Z {'PASS' if ck.get('B2-Z') else 'FAIL'}; slab C-Z {'PASS' if ck.get('C-Z') else 'FAIL'}; "
    f"divergent primary ladder: {prim_fail})")
npass = sum(ok for _, ok in CHECKS)
RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk)
say(f"ZT3 COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time() - T0:.0f} s]")
open(os.path.join(HERE, f"zt3_two_sided_obstacle{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"zt3_two_sided_obstacle_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
sys.exit(0 if npass == len(CHECKS) else 1)
