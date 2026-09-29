#!/usr/bin/env python3
"""x1_2_knob_fits -- Track K of lane X1: the 29 pairs in which the exotic masses (E6) or the intermediate scale (B-L) are treated as UNKNOWNS (pre-registered in X1_PREREGISTRATION.md).
Question asked of each: is there ANY choice of the knobs that satisfies the rule, and how many parameters does that cost against the independent equalities (excess = K_eq - u - m).
Under amendment A0 no Track-K pair can be a lead of the framework; this script only measures what the knobs would have to be.
Run (real):    PYTHONDONTWRITEBYTECODE=1 python3 x1_2_knob_fits.py           -> writes x1_2_results.json; exit 0 iff the controls pass (2 otherwise)
Run (control): PYTHONDONTWRITEBYTECODE=1 python3 x1_2_knob_fits.py MUTATE    -> the recovery target of K1 is perturbed by 35% in M: K1 must FAIL; exit 1 if the control bites, 3 if it does not; writes x1_2_results_MUTATE.json
Controls inside: K1 the mass solver finds (and recovers) the masses of a synthetic solvable world; K2 a synthetic world with the mass box restricted to 1e14-1e16 GeV is reported infeasible; K3 the excess arithmetic on the SM (R-B: K_eq 2, u 1, m 0 -> 1);
K4 the monotone reach test flags a target outside the reachable interval and accepts one inside.
Unknown parametrisation: M_D = 1 TeV (X/1 TeV)^f_D, M_H = 100 GeV (X/100 GeV)^f_H with f in [0,1] (f = 0: the collider floor, f = 1: decoupled at X), so the box is 1 TeV <= M_D <= X and 100 GeV <= M_H <= X.
"""
import sys
sys.dont_write_bytecode = True
import json
import math
import time
import numpy as np
from scipy.optimize import least_squares
import x1_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
chk = L.Checks(MUT)
XP, XR, MZ = L.XP, L.XR, L.MZ
XS = L.species_scale
FD, FH = L.FLOOR_D, L.FLOOR_H
T0 = time.time()


def jsonable(o):
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o


def masses(fD, fH, X, floorD=FD, floorH=FH):
    return floorD * (X / floorD) ** fD, floorH * (X / floorH) ** fH


def ra_res(run, X):
    A = run.A(X)
    a1, a2, a3 = 0.6 * A[0], A[1], A[2]
    return np.array([L.ratio_res(a1 / a2, 1.0), L.ratio_res(a3 / a2, 1.0)])


def find_solutions(resfun, dim, ngrid=9, tol_sol=1e-7, lo=None, hi=None):
    """Multi-start least squares on [lo, hi]^dim (default [0,1]); returns (solutions, best_theta, best_maxabs, n_evals)."""
    lo = np.zeros(dim) if lo is None else np.array(lo, dtype=float)
    hi = np.ones(dim) if hi is None else np.array(hi, dtype=float)
    axes = [np.linspace(lo[k], hi[k], ngrid) for k in range(dim)]
    grid = np.array(np.meshgrid(*axes, indexing="ij")).reshape(dim, -1).T
    vals = []
    for th in grid:
        try:
            r = resfun(th)
            vals.append(float(np.max(np.abs(r))))
        except Exception:
            vals.append(1e9)
    vals = np.array(vals)
    order = np.argsort(vals)
    starts = [grid[i] for i in order[:4]]
    idx = vals.reshape([ngrid] * dim)
    for flat in range(len(vals)):
        ijk = np.unravel_index(flat, idx.shape)
        loc = True
        for d in range(dim):
            for s in (-1, 1):
                nb = list(ijk)
                nb[d] += s
                if 0 <= nb[d] < ngrid and idx[tuple(nb)] < vals[flat]:
                    loc = False
        if loc and vals[flat] < 1e8:
            starts.append(grid[flat])
    sols, best = [], (None, 1e9)
    for x0 in starts:
        try:
            out = least_squares(resfun, x0, bounds=(lo, hi), xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=200)
        except Exception:
            continue
        mx = float(np.max(np.abs(out.fun)))
        if mx < best[1]:
            best = (out.x.copy(), mx)
        if mx < tol_sol and not any(np.max(np.abs(out.x - s)) < 1e-4 for s in sols):
            sols.append(out.x.copy())
    return sols, best[0], best[1], len(vals)


def fixed_X_masses(X, n27, floorD=FD, floorH=FH, ngrid=9):
    """RA at fixed X, unknown (M_D, M_H)."""
    def rf(th):
        mD, mH = masses(th[0], th[1], X, floorD, floorH)
        return ra_res(L.Run("2L-T", L.exotics_e6(mD, mH, n27), rtol=1e-8), X)
    sols, b, bm, ne = find_solutions(rf, 2, ngrid=ngrid)
    return [dict(f=s.tolist(), MD=masses(s[0], s[1], X, floorD, floorH)[0], MH=masses(s[0], s[1], X, floorD, floorH)[1]) for s in sols], bm


def final_check(X, n27, MD, MH):
    """Re-evaluate a solution with rtol 1e-10 and the full T-JOINT bands; returns dict."""
    rule = L.make_rule("RA", X=X, xtag="sol")
    ev = L.evaluate_bands(rule, L.exotics_e6(MD, MH, n27))
    run = L.Run("2L-T", L.exotics_e6(MD, MH, n27))
    A = run.A(X)
    pc, tau = L.proton_check(X, A[1])
    return dict(max_r=float(max(abs(np.array(ev["cen_r"])))), tol=ev["tol"], passes=ev["pass"], a_G=float(A[1]), proton=pc, tau_yr=tau, perturbative=L.perturbative_check(run, X))


# ================================================================================ controls
print("=" * 118)
print("X1-2 Track K (knobs allowed) -- mode:", "MUTATE (control)" if MUT else "REAL RUN")
print("=" * 118)
# K3 excess arithmetic
chk("K3 excess arithmetic on the SM: R-B (K_eq 2, u 1, m 0) -> 1 = the alpha_3 prediction; R-A at fixed X (2, 0, 0) -> 2; dual-Coxeter at X_P (3, 0, 0) -> 3",
    (L.excess(L.make_rule("RB", xtag="cross"), 0), L.excess(L.make_rule("RA", X=XP), 0), L.excess(L.make_rule("RD", X=XP, h=8), 0)) == (1, 2, 3))

# K1 / K2 synthetic world
n27c, X0, MD0, MH0 = 3, 1.0e16, 3.0e6, 2.0e4
from scipy.optimize import fsolve
base_a = L.boundaries(L.SET_A)


def build_world(aY, a3):
    return np.array([aY, base_a[1], a3])


def world_res(u):
    a0 = build_world(u[0], u[1])
    run = L.Run("2L-T", L.exotics_e6(MD0, MH0, n27c), a0=a0, rtol=1e-10)
    return ra_res(run, X0)


u_sol = fsolve(world_res, [base_a[0], base_a[2]], xtol=1e-13)
a0_syn = build_world(*u_sol)
print(f"      synthetic solvable world: n27 = 3, X0 = 1e16, M_D = 3e6, M_H = 2e4; couplings at m_Z constructed so that a_1 = a_2 = a_3 at X0: a_Y, a_3 shifted by ({u_sol[0] - base_a[0]:+.3f}, {u_sol[1] - base_a[2]:+.3f}); residual {np.max(np.abs(world_res(u_sol))):.2e}")


def synthetic_solve(floorD, floorH, X):
    def rf(th):
        mD, mH = masses(th[0], th[1], X, floorD, floorH)
        return ra_res(L.Run("2L-T", L.exotics_e6(mD, mH, n27c), a0=a0_syn, rtol=1e-8), X)
    sols, b, bm, ne = find_solutions(rf, 2, ngrid=9)
    return [(masses(s[0], s[1], X, floorD, floorH)) for s in sols], bm


solsK1, bmK1 = synthetic_solve(FD, FH, X0)
target = (MD0 * (1.35 if MUT else 1.0), MH0 * (1.35 if MUT else 1.0))
recovered = any(abs(math.log(m[0] / target[0])) < 0.05 and abs(math.log(m[1] / target[1])) < 0.05 for m in solsK1)
chk("K1 the mass solver finds a solution of a solvable synthetic world and RECOVERS its masses (to 5% in ln M)" + (" [MUTATE: target perturbed by 35%]" if MUT else ""), len(solsK1) > 0 and recovered,
    f"(solutions found: {[(f'{a:.3g}', f'{b:.3g}') for a, b in solsK1]}, best residual {bmK1:.2e})")
a0_syn_good = a0_syn.copy()
a0_syn = a0_syn_good * np.array([1.10, 1.0, 1.0])          # K2 world: a_Y(m_Z) +10% (a_1 - a_2 at X0 moves by ~+6.6), off the single line that the split-multiplet direction can reach
solsK2, bmK2 = synthetic_solve(FD, FH, X0)
a0_syn = a0_syn_good
chk("K2 a synthetic world whose a_Y(m_Z) is moved by +10% (off the one direction the split multiplet can act along, at the same X) is reported INFEASIBLE: no exact solution and closest approach > 0.01 (the T-JOINT floor)", len(solsK2) == 0 and bmK2 > 0.01, f"(closest approach {bmK2:.3f})")

def reach(X, n27, floors=(FD, FH)):
    lo = L.Run("2L-T", L.exotics_e6(floors[0], floors[1], n27)).A(X)
    hi = L.desert("2L-T").A(X)
    return lo, hi


def inside_reach(pred, lo, hi):
    return bool(np.all((pred >= lo - 1e-12) & (pred <= hi + 1e-12)))


lo4, hi4 = reach(XP, 3)
chk("K4 reach test: a target at the midpoint of the reachable interval [A(floors), A(desert)] is inside; a target 3x the desert value is outside", inside_reach(0.5 * (lo4 + hi4), lo4, hi4) and not inside_reach(3 * hi4, lo4, hi4))

# ================================================================================ the 29 variants
records = []


def rec(**kw):
    records.append(kw)
    return kw


def excess_of(K_eq, u, m):
    return K_eq - u - m


def report(r):
    print(f"{r['id']:8s} {r['spectrum']} n27={r['n27']} {r['variant']:14s} K_eq={r['K_eq']} u={r['u']} m={r['m']} excess={r['excess']:+d}  -> {r['verdict']}")
    for line in r.get("notes", []):
        print("           " + line)


# ---- S3 (E6), N27 in {1, 3}
for n27 in (1, 3):
    Ns = 118 + 22 * n27
    # KA-P, KA-R, KA-S
    for tag, X in (("X_P", XP), ("X_R", XR), ("X_S", XS(Ns))):
        sols, bm = fixed_X_masses(X, n27)
        notes = []
        info = []
        for s in sols:
            fc = final_check(X, n27, s["MD"], s["MH"])
            info.append(dict(s, **fc))
            notes.append(f"solution: M_D = {s['MD']:.3e}, M_H = {s['MH']:.3e} GeV; a_G = {fc['a_G']:.2f}; proton {fc['proton']}; perturbative {fc['perturbative']}; T-JOINT pass {fc['passes']}")
        m_, K_, u_ = 2, 2, 0
        ex = excess_of(K_, u_, m_)
        if sols:
            verdict = "K-REFIT (a solution exists; excess <= 0: nothing predicted beyond what was fitted)" if ex <= 0 else "K-LEAD-CANDIDATE"
        else:
            verdict = f"K-DEAD (no solution in the box; closest approach max|r| = {bm:.3f})"
        if not sols:
            notes.append(f"closest approach max|r| = {bm:.4f}")
        r = rec(id=f"K:{n27}:KA-{tag}", spectrum="S3", n27=n27, variant=f"KA-{tag}", K_eq=K_, u=u_, m=m_, excess=ex, verdict=verdict, X=X, solutions=info, closest=bm, notes=notes)
        report(r)
    # KA-free: X is an UNKNOWN (Amendment A5: a scan on an X grid misses the isolated scale at which the split-multiplet direction can act)
    print(f"   [n27={n27}] KA-free: 3-dimensional least squares over (X, f_D, f_H)  ({time.time() - T0:.0f}s)")
    LXLO, LXHI = math.log(1e6), math.log(XP)

    def rfree(th):
        X = math.exp(LXLO + th[0] * (LXHI - LXLO))
        mD, mH = masses(th[1], th[2], X)
        return ra_res(L.Run("2L-T", L.exotics_e6(mD, mH, n27), rtol=1e-8), X)
    rng = np.random.default_rng(11)
    starts = [np.array([t, fd, fh]) for t in np.linspace(0.05, 0.95, 7) for fd in (0.2, 0.6, 1.0) for fh in (0.0, 0.3, 0.6)]
    starts += [rng.uniform(0, 1, 3) for _ in range(40)]
    fam, bestc = [], (None, 1e9)
    for x0 in starts:
        try:
            out = least_squares(rfree, x0, bounds=([0, 0, 0], [1, 1, 1]), xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=300)
        except Exception:
            continue
        mx = float(np.max(np.abs(out.fun)))
        if mx < bestc[1]:
            bestc = (out.x.copy(), mx)
        if mx < 1e-7 and not any(np.max(np.abs(out.x - q["theta"])) < 1e-3 for q in fam):
            X = math.exp(LXLO + out.x[0] * (LXHI - LXLO))
            mD, mH = masses(out.x[1], out.x[2], X)
            fc = final_check(X, n27, mD, mH)
            fam.append(dict(theta=out.x.copy(), log10X=X and math.log10(X), X=X, MD=mD, MH=mH, **fc))
    m_, K_, u_ = 2, 2, 1
    ex = excess_of(K_, u_, m_)
    notes = []
    if fam:
        xs = [f["log10X"] for f in fam]
        okp = [f for f in fam if f["proton"] in ("PASS", "UNCERTAIN")]
        notes.append(f"{len(fam)} distinct exact solutions found (a curve, not a point); log10 X in [{min(xs):.2f}, {max(xs):.2f}]; M_D in [{min(f['MD'] for f in fam):.2e}, {max(f['MD'] for f in fam):.2e}], M_H in [{min(f['MH'] for f in fam):.2e}, {max(f['MH'] for f in fam):.2e}] GeV; proton check PASS or UNCERTAIN at {len(okp)} of them; T-JOINT passes at {sum(1 for f in fam if f['passes'])}; perturbative at {sum(1 for f in fam if f['perturbative'])}")
        for f in sorted(fam, key=lambda q: q["MD"])[:: max(1, len(fam) // 6)]:
            notes.append(f"  X = {f['X']:.3e}: M_D = {f['MD']:.3e}, M_H = {f['MH']:.3e}, a_G = {f['a_G']:.1f}, tau_p ~ {f['tau_yr']:.1e} yr ({f['proton']})")
        # effective number of mass knobs: singular values of the Jacobian of the two residuals w.r.t. (ln M_D, ln M_H) at fixed X, at the first solution
        f0 = fam[0]
        def rj(v):
            return ra_res(L.Run("2L-T", L.exotics_e6(math.exp(v[0]), math.exp(v[1]), n27), rtol=1e-10), f0["X"])
        v0 = np.array([math.log(f0["MD"]), math.log(f0["MH"])])
        J = np.zeros((2, 2))
        for k in range(2):
            dv = np.zeros(2); dv[k] = 1e-3
            J[:, k] = (rj(v0 + dv) - rj(v0 - dv)) / 2e-3
        sv = np.linalg.svd(J, compute_uv=False)
        notes.append(f"Jacobian of the two residuals w.r.t. (ln M_D, ln M_H) at X = {f0['X']:.2e}: singular values {sv[0]:.3e}, {sv[1]:.3e} (ratio {sv[1] / sv[0]:.1e}): effectively ONE mass direction (the split-multiplet direction M_H/M_D); the other is flat up to two-loop terms")
        verdict = "K-REFIT (exact solutions exist: excess = -1 nominal, 0 effective; the scale is pinned, see proton check)"
        if not okp:
            verdict += "; the proton-lifetime check FAILS at every solution -> excluded"
    else:
        # Amendment A8: the pre-registered K-DEAD rule is "no point of the box within tol", not "no exact solution": minimise max|r| from the best least-squares point and compare with the T-JOINT tolerance there
        from scipy.optimize import minimize
        def fmax(th):
            th = np.clip(th, 0.0, 1.0)
            return float(np.max(np.abs(rfree(th)))) + 10.0 * float(np.sum(np.abs(th - np.array(th))))
        best_mm = (bestc[0], float(np.max(np.abs(rfree(bestc[0])))))
        for x0 in [bestc[0]] + [best_mm[0] + 0.02 * rng.standard_normal(3) for _ in range(6)]:
            x0 = np.clip(x0, 0.0, 1.0)
            out = minimize(lambda th: float(np.max(np.abs(rfree(np.clip(th, 0, 1))))), x0, method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-10, maxiter=1500))
            th = np.clip(out.x, 0, 1)
            v = float(np.max(np.abs(rfree(th))))
            if v < best_mm[1]:
                best_mm = (th, v)
        thm = best_mm[0]
        Xm = math.exp(LXLO + thm[0] * (LXHI - LXLO))
        mDm, mHm = masses(thm[1], thm[2], Xm)
        fcm = final_check(Xm, n27, mDm, mHm)
        within = bool(fcm["passes"])
        notes.append(f"closest approach in the max-norm: max|r| = {best_mm[1]:.4f} at X = {Xm:.3e}, M_D = {mDm:.3e}, M_H = {mHm:.3e}; T-JOINT tolerance there {np.round(fcm['tol'], 4).tolist()}; within tolerance: {within}; proton check {fcm['proton']} (tau ~ {fcm['tau_yr']:.1e} yr)")
        if within:
            verdict = f"K-REFIT (no exact solution, but the closest approach max|r| = {best_mm[1]:.4f} is inside the running's tolerance; the scale is pinned near {Xm:.1e}, proton check {fcm['proton']})"
            fam.append(dict(theta=thm.copy(), log10X=math.log10(Xm), X=Xm, MD=mDm, MH=mHm, **fcm))
        else:
            verdict = f"K-DEAD (no point of the box within the T-JOINT tolerance; closest approach max|r| = {best_mm[1]:.4f}, tolerance {np.round(fcm['tol'], 3).tolist()})"
        notes.append(f"least-squares closest approach max|r| = {bestc[1]:.4f}")
    r = rec(id=f"K:{n27}:KA-free", spectrum="S3", n27=n27, variant="KA-free", K_eq=K_, u=u_, m=m_, excess=ex, verdict=verdict, family=fam, closest=bestc[1], notes=notes)
    report(r)
    # KDeg: M_D = M_H = M, X free
    def rdeg(th):
        X = math.exp(th[1])
        M = FD * (X / FD) ** th[0]
        return ra_res(L.Run("2L-T", L.exotics_e6(M, M, n27), rtol=1e-8), X)
    sols, b, bm, ne = find_solutions(rdeg, 2, ngrid=11, lo=[0.0, math.log(1e4)], hi=[1.0, math.log(XP)])
    m_, K_, u_ = 1, 2, 1
    ex = excess_of(K_, u_, m_)
    notes = [f"closest approach max|r| = {bm:.4f} (complete-SU(5) multiplet; expected: cannot cure, gate G3)"]
    if sols:
        notes = [f"exact solutions: {[(math.exp(s[1]), FD * (math.exp(s[1]) / FD) ** s[0]) for s in sols]}"]
    r = rec(id=f"K:{n27}:KDeg", spectrum="S3", n27=n27, variant="KDeg", K_eq=K_, u=u_, m=m_, excess=ex,
            verdict=("K-REFIT" if sols else f"K-DEAD (complete multiplet cannot satisfy the ratios; closest approach max|r| = {bm:.3f})"), notes=notes)
    report(r)
    # KD (dual Coxeter, h = 12): monotone reach over the whole box
    hh = 4 * math.pi * 12
    pred = np.array([(5 / 3) * hh, hh, hh])
    for tag, X in (("X_P", XP), ("X_S", XS(Ns)), ("free", None)):
        if X is not None:
            lo, hi = reach(X, n27)
            inside = inside_reach(pred, lo, hi)
            notes = [f"targets (a_Y, a_2, a_3) = {np.round(pred, 1)}; reachable interval at X: a_Y [{lo[0]:.1f}, {hi[0]:.1f}], a_2 [{lo[1]:.1f}, {hi[1]:.1f}], a_3 [{lo[2]:.1f}, {hi[2]:.1f}]"]
            K_, u_ = 3, 0
        else:
            hi_max = np.max([L.desert("2L-T").A(math.exp(l)) for l in np.linspace(math.log(MZ * 1.0001), math.log(XP), 400)], axis=0)
            inside = bool(np.all(pred <= hi_max))
            notes = [f"targets {np.round(pred, 1)}; sup over 91 GeV <= X <= M_P and over all masses of (a_Y, a_2, a_3) = {np.round(hi_max, 1)} (added matter only lowers a_i)"]
            K_, u_ = 3, 1
        m_ = 2
        ex = excess_of(K_, u_, m_)
        verdict = "K-DEAD (T-MONO over the whole knob box: the dual-Coxeter targets lie above every reachable value)" if not inside else "K-OPEN (reachable; solve)"
        r = rec(id=f"K:{n27}:KD-{tag}", spectrum="S3", n27=n27, variant=f"KD-{tag}", K_eq=K_, u=u_, m=m_, excess=ex, verdict=verdict, notes=notes)
        report(r)
        if inside:
            print("           WARNING: target reachable -- would require a solve (not expected)")
    # KE heterotic
    def rhet(th):
        mD, mH = masses(th[0], th[1], XR)     # masses bounded by M_red here; X_het < M_red for these runs
        run = L.Run("2L-T", L.exotics_e6(mD, mH, n27), rtol=1e-8)
        X = L.solve_hetero(run)
        if X is None:
            return np.array([1e3, 1e3])
        return ra_res(run, X)
    sols, b, bm, ne = find_solutions(rhet, 2, ngrid=9)
    m_, K_, u_ = 2, 3, 1
    ex = excess_of(K_, u_, m_)
    notes = [f"closest approach max|r| = {bm:.4f}"]
    infoE = []
    for s in sols:
        mD, mH = masses(s[0], s[1], XR)
        run = L.Run("2L-T", L.exotics_e6(mD, mH, n27))
        X = L.solve_hetero(run)
        fc = final_check(X, n27, mD, mH)
        infoE.append(dict(MD=mD, MH=mH, X=X, **fc))
        notes.append(f"solution: M_D = {mD:.3e}, M_H = {mH:.3e}, X_het = {X:.3e}; a_G = {fc['a_G']:.1f}; proton {fc['proton']}")
    verdict = ("K-REFIT (exact solution; excess = 0: two mass knobs spent on two equalities, the scale relation costs the recalled constant)" if sols else f"K-DEAD (no solution in the box; closest approach {bm:.3f})")
    r = rec(id=f"K:{n27}:KE", spectrum="S3", n27=n27, variant="KE-het", K_eq=K_, u=u_, m=m_, excess=ex, verdict=verdict, solutions=infoE, closest=bm, notes=notes)
    report(r)
    # KF / KG emergence
    for base in (118, 126):
        N = base + 22 * n27
        X = XS(N)
        lo, hi = reach(X, n27)
        notes = [f"a_i(Lambda = M_red/sqrt({N}) = {X:.3e}) reachable interval [floors, desert]: a_Y [{lo[0]:.1f}, {hi[0]:.1f}], a_2 [{lo[1]:.1f}, {hi[1]:.1f}], a_3 [{lo[2]:.1f}, {hi[2]:.1f}]; target 0"]
        deadF = bool(np.any(lo > 0))
        deadG = bool(lo[0] > 0)
        m_ = 2
        rF = rec(id=f"K:{n27}:KF-{base}", spectrum="S3", n27=n27, variant=f"KF-{base}", K_eq=3, u=0, m=m_, excess=excess_of(3, 0, m_),
                 verdict=("K-DEAD (T-MONO over the box: at least one coupling cannot reach 0 even with both exotic masses at their floors)" if deadF else "K-OPEN"), notes=notes)
        report(rF)
        rG = rec(id=f"K:{n27}:KG-{base}", spectrum="S3", n27=n27, variant=f"KG-{base}", K_eq=1, u=0, m=m_, excess=excess_of(1, 0, m_),
                 verdict=("K-DEAD (a_Y cannot reach 0 even with both exotic masses at their floors)" if deadG else "K-OPEN"), notes=[f"min a_Y(Lambda) = {lo[0]:.2f} at the floors"])
        report(rG)

# ---- S4 (gauged B-L), one loop above M_BL
print(f"   S4 (SM x U(1)_(B-L) between M_BL and X)  ({time.time() - T0:.0f}s)")
# charges (T3R, X=(B-L)/2) of the Weyl multiplets: (multiplicity of components, qR, qX)
FERM = [(6, 0.0, 1 / 6), (3, -0.5, -1 / 6), (3, 0.5, -1 / 6), (2, 0.0, -0.5), (1, 0.5, 0.5), (1, -0.5, 0.5)]      # Q, u^c, d^c, L, e^c, nu^c
SCAL = [(2, 0.5, 0.0), (1, 1.0, -1.0)]                                                        # H (T3R = 1/2, X = 0; two components), S (T3R, X) = (1, -1)
bmat = np.zeros((2, 2))
for gens, lst, f in ((3, FERM, 2 / 3), (1, SCAL, 1 / 3)):
    for (nc, qR, qX) in lst:
        q = np.array([qR, qX])
        bmat += gens * f * nc * np.outer(q, q)
print(f"      one-loop abelian block b_ab (rows R, X): {np.round(bmat, 4).tolist()}; b_R + b_X + 2 b_RX = {bmat.sum():.6f} (b_Y = 41/6 = {41 / 6:.6f})")
chk("K5 the abelian block of SM x U(1)_R x U(1)_X sums to the hypercharge coefficient: b_RR + b_XX + 2 b_RX = 41/6 (S is neutral under Y, nu^c is neutral): M_BL cannot change the one-loop running of a_Y", abs(bmat.sum() - 41 / 6) < 1e-12)

sm = L.desert("2L-T")


def s4_state(X, tBL, aR0, aRX0):
    """a_R, a_X, a_RX at X given values at M_BL = exp(tBL); a_X0 from the matching a_Y(M_BL) = a_R + a_X + 2 a_RX; SU(2), SU(3) and a_Y below M_BL from the two-loop SM run."""
    MBL = math.exp(tBL)
    aY_BL = sm.A(MBL)[0]
    aX0 = aY_BL - aR0 - 2 * aRX0
    a0 = np.array([[aR0, aRX0], [aRX0, aX0]])
    aX_ = a0 - bmat / L.TWO_PI * math.log(X / MBL)
    return aX_


def s4_residuals(X, th):
    tBL, aR0, aRX0 = th
    a = s4_state(X, tBL, aR0, aRX0)
    A = sm.A(X)
    a2 = A[1]
    return np.array([(a[0, 0] - a2) / a2, (a[1, 1] - (2 / 3) * a2) / a2, a[0, 1] / a2])


def s4_solve(X):
    def rf(th):
        return s4_residuals(X, [th[0], th[1], th[2]])
    best = (None, 1e9)
    lo = [math.log(MZ * 1.5), 1.0, -50.0]
    hi = [math.log(X), 300.0, 50.0]
    rng = np.random.default_rng(3)
    for _ in range(40):
        x0 = [rng.uniform(lo[0], hi[0]), rng.uniform(20, 120), rng.uniform(-10, 10)]
        try:
            out = least_squares(rf, x0, bounds=(lo, hi), xtol=1e-14, ftol=1e-14, gtol=1e-14)
        except Exception:
            continue
        mx = float(np.max(np.abs(out.fun)))
        if mx < best[1]:
            best = (out.x, mx)
    return best


s4_out = []
s4_check = []
for tag, X in (("X_P", XP), ("X_S", XS(118))):
    th, mx = s4_solve(X)
    A = sm.A(X)
    r_sum = L.ratio_res(0.6 * A[0] / A[1], 1.0)
    # M_BL independence of the sum-rule miss: evaluate the sum a_R + a_X + 2 a_RX at X for several M_BL and arbitrary a_R0, a_RX0
    sums = []
    for tb in (math.log(1e3), math.log(1e8), math.log(1e13)):
        a = s4_state(X, tb, 40.0, 2.0)
        sums.append(float(a[0, 0] + a[1, 1] + 2 * a[0, 1]))
    spread = max(sums) - min(sums)
    notes = [f"best least-squares residual over (M_BL, a_R0, a_RX0): max|r| = {mx:.4f} (the SM-desert R-A miss in a_1/a_2 at this X is {r_sum:+.4f}); (a_R + a_X + 2 a_RX)(X) for M_BL = 1e3, 1e8, 1e13 differs by {spread:.3f} (hybrid two-loop drift; exactly 0 at one loop)",
             f"the Spin(10) sum rule needs a_R + a_X + 2 a_RX = (5/3) a_2 = {5 / 3 * A[1]:.2f} at X; the SM one-loop hypercharge run gives {A[0]:.2f}"]
    verdict = f"K-DEAD (the B-L intermediate scale cannot move the sum a_R + a_X + 2 a_RX, which is a_Y; the residual equals the desert R-A miss)"
    r = rec(id=f"K:S4:{tag}", spectrum="S4", n27=0, variant=f"S4-{tag}", K_eq=3, u=0, m=3, excess=excess_of(3, 0, 3), verdict=verdict, closest=mx, sum_rule_miss=r_sum, notes=notes)
    report(r)
    s4_out.append((mx, r_sum))
    Sx = sums[0]
    s4_check.append((mx, abs(Sx - 5 / 3 * A[1]) / (3 * A[1]), spread / (3 * A[1])))
# X free: minimise over X the larger of (sum-rule miss, a_3/a_2 miss)
xs_ = np.exp(np.linspace(math.log(1e11), math.log(XP), 400))
best = (None, 1e9)
for X in xs_:
    A = sm.A(X)
    v = max(abs(L.ratio_res(0.6 * A[0] / A[1], 1.0)), abs(L.ratio_res(A[2] / A[1], 1.0)))
    if v < best[1]:
        best = (X, v)
notes = [f"min over X of max(|sum-rule miss|, |a_3/a_2 miss|) = {best[1]:.4f} at X = {best[0]:.3e} (identical to the S2 R-A/R-B miss: M_BL does not enter)"]
r = rec(id="K:S4:free", spectrum="S4", n27=0, variant="S4-free", K_eq=4, u=1, m=3, excess=excess_of(4, 1, 3), verdict="K-DEAD (same residual as the desert: a_1 = a_2 and a_3 = a_2 cannot both hold)", closest=best[1], notes=notes)
report(r)
chk("K6 S4 is the desert in disguise: the best S4 residual over (M_BL, a_R0, a_RX0) equals |S - (5/3) a_2| / (3 a_2) (the least-squares minimiser of the three residuals under the constraint a_R + a_X + 2 a_RX = S puts (1, 1, 2)/6 of the miss on them; the constraint cannot be moved by M_BL) within the hybrid two-loop drift, and is >= 5% at both scales",
    all(m >= 0.05 and abs(m - e) <= dr + 1e-6 for (m, e, dr) in s4_check), f"({[(round(m, 4), round(e, 4), round(dr, 4)) for (m, e, dr) in s4_check]})")

# ================================================================================ tallies
kinds = {}
for r in records:
    key = r["verdict"].split(" ")[0]
    kinds[key] = kinds.get(key, 0) + 1
print(f"\nTrack K: {len(records)} variants; verdict classes: {kinds}")
chk("K0 registered Track-K variants: 29 (S3: 13 per N27 x 2 = 26; S4: 3)", len(records) == 29, f"({len(records)})")
with open("x1_2_results_MUTATE.json" if MUT else "x1_2_results.json", "w") as f:
    json.dump(jsonable(dict(variants=records, tally=kinds, mutate=MUT)), f, indent=1)
print(f"elapsed {time.time() - T0:.0f} s")
chk.finish("X1-2")
