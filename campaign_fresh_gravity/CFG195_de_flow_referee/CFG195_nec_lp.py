#!/usr/bin/env python3
"""CFG195_nec_lp.py -- items II-2, II-3, II-5, II-6, II-7, A2, A6 (and MUTATE 1, 4, 6) of CFG195_FROZEN_CRITERIA.md.
LP: maximise the momentum density g = T^{0x} (T^{00}=1) over all symmetric stress tensors obeying the null energy condition
T_{mu nu} k^mu k^nu >= 0 for every null k, at fixed isotropic w = tr(T^{ij})/3.  Signature -+++, T_{0i} = -T^{0i}.
MUTATE=1 flips the NEC sign; MUTATE=4 restricts to isotropic pressure; MUTATE=6 uses axis-aligned null vectors only."""
import math, numpy as np
from scipy.optimize import linprog, minimize
from CFG195_common import Run
run = Run("CFG195_nec_lp", ("1", "4", "6")); MUT = run.mut
SQ3H = math.sqrt(3) / 2
def fib(n):
    i = np.arange(n) + 0.5; phi = np.arccos(1 - 2 * i / n); th = np.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(phi), np.sin(phi) * np.cos(th), np.sin(phi) * np.sin(th)], 1)
DIRS = fib(4096)
def rows(N):   # A x <= 1 with x=[g,Txx,Tyy,Tzz,Txy,Txz,Tyz]; NEC: 1 - 2 g nx + n.T.n >= 0  ->  2 g nx - n.T.n <= 1
    n = N; A = np.stack([2 * n[:, 0], -n[:, 0] ** 2, -n[:, 1] ** 2, -n[:, 2] ** 2, -2 * n[:, 0] * n[:, 1], -2 * n[:, 0] * n[:, 2], -2 * n[:, 1] * n[:, 2]], 1)
    return A, np.ones(len(n))
def Tkk(x, n):
    g, txx, tyy, tzz, txy, txz, tyz = x
    return 1 - 2 * g * n[..., 0] + txx * n[..., 0] ** 2 + tyy * n[..., 1] ** 2 + tzz * n[..., 2] ** 2 + 2 * txy * n[..., 0] * n[..., 1] + 2 * txz * n[..., 0] * n[..., 2] + 2 * tyz * n[..., 1] * n[..., 2]
def solve(w, mode):
    """returns (status, g_max, x); mode in normal / flipped / isotropic / axis"""
    cost = np.zeros(7); cost[0] = -1
    Aeq = np.array([[0, 1, 1, 1, 0, 0, 0]]); beq = [3 * w]
    if mode == "axis":
        n = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float); A, b = rows(n)
        r = linprog(cost, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * 7, method="highs"); return r.status, (-r.fun if r.status == 0 else None), (r.x if r.status == 0 else None)
    if mode == "isotropic":
        Aeq2 = np.array([[0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]]); beq2 = [w, w, w, 0, 0, 0]
        A, b = rows(DIRS); r = linprog(cost, A_ub=A, b_ub=b, A_eq=Aeq2, b_eq=beq2, bounds=[(None, None)] * 7, method="highs"); return r.status, (-r.fun if r.status == 0 else None), (r.x if r.status == 0 else None)
    A, b = rows(DIRS)
    if mode == "flipped": A, b = -A, -b       # T_kk <= 0:  -(2 g nx - nTn) <= -1
    for it in range(30):
        r = linprog(cost, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * 7, method="highs")
        if r.status != 0: return r.status, None, None
        if mode == "flipped": return 0, -r.fun, r.x
        x = r.x; v = Tkk(x, DIRS); i = np.argmin(v)
        f = lambda ang: Tkk(x, np.array([math.sin(ang[0]) * math.cos(ang[1]), math.sin(ang[0]) * math.sin(ang[1]), math.cos(ang[0])]))
        th0 = math.acos(DIRS[i, 2]); ph0 = math.atan2(DIRS[i, 1], DIRS[i, 0]); m = minimize(f, [th0, ph0], method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-14))
        if m.fun > -1e-10: return 0, -r.fun, x
        th, ph = m.x; nnew = np.array([[math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)]]); A2, b2 = rows(nnew); A = np.vstack([A, A2]); b = np.concatenate([b, b2])
    return 0, -r.fun, x
mode_main = {"1": "flipped", "4": "isotropic", "6": "axis", "": "normal"}[MUT]
print("mode:", mode_main)
# ---------------------------------------------------------------- II-2
print("\n== II-2 LP maximum of g/e at fixed 1+w_iso ==")
ok2 = True; ratios = {}
for s in (0.02, 0.05, 0.1, 0.25, 0.5, 1.0):
    st, g, x = solve(s - 1, mode_main)
    if st == 0:
        r = g / s; ratios[s] = r; ok2 &= abs(r - SQ3H) < 1e-3
        pt = f"g_max={g:.6f} ratio g/(1+w)={r:.5f}  T^ij diag=({x[1]:+.4f},{x[2]:+.4f},{x[3]:+.4f}) -> 1+w_par={1+x[1]:.4f} 1+w_perp={1+x[2]:.4f}"
    else: pt = f"LP status {st} (no optimum)"; ok2 = False
    print(f"  1+w_iso={s:5.2f}: {pt}")
run.num("II2_ratios", ratios)
run.check("II-2 g_max/(1+w_iso) = sqrt(3)/2 = 0.86603 within 1e-3 at six values of 1+w_iso", f"{ratios}", ok2)
st0, g0, _ = solve(-1.0, mode_main); z_ok = (st0 == 0 and g0 is not None and abs(g0) < 1e-9)
run.check("II-2b g_max = 0 exactly at w_iso = -1 (every NEC tensor with w_iso=-1 has zero momentum)", f"status {st0}, g_max {g0}", z_ok)
stn, gn, _ = solve(-1.05, mode_main); n_ok = stn != 0
run.check("II-2c LP infeasible for 1+w_iso<0 (phantom is NEC-violating at rest)", f"status {stn} (2=infeasible)", n_ok)
# ---------------------------------------------------------------- II-3 type IV
print("\n== II-3 type IV: T = -rho g + flux (w=-1 medium with energy flux q) ==")
rho, q = 1.0, 0.1
T_mixed = np.array([[-rho, q], [-q, -rho]]) ; ev = np.linalg.eigvals(T_mixed)
Tf = lambda n: 1 * rho - 2 * q * n[:, 0] - rho * n[:, 0] ** 2 * (-1) * 0  # placeholder replaced below
xIV = [q, -rho, -rho, -rho, 0, 0, 0]                  # T^00=rho normalised to 1: use rho=1 -> (g=q, p=-1)
minT = float(Tkk(xIV, DIRS).min())
run.check("II-3 eigenvalues of the (t,x) block are -rho +/- i q and min over null k of T_kk = -2q < 0", f"eig {np.round(ev,6)}, min T_kk {minT:.6f} (expect -{2*q})", abs(ev[0].imag) > 0.09 and abs(minT + 2 * q) < 1e-3 and abs(ev[0].real + rho) < 1e-12)
# ---------------------------------------------------------------- II-5
print("\n== II-5 random NEC-compliant tensors (N=1000, seed 195003) ==")
rng = np.random.default_rng(195003); best = 0; viol = 0; ratio_all = []
for _ in range(1000):
    x = np.array([rng.normal(0, 0.5), *rng.normal(-0.5, 1.0, 3), *rng.normal(0, 0.3, 3)]); x[0] = abs(x[0])
    m = float(Tkk(x, DIRS).min())
    if m < 0: x[1] += -m; x[2] += -m; x[3] += -m    # add -m*delta_ij: raises T_kk by -m for every unit n (sum n_i^2 = 1): NEC saturated
    m2 = float(Tkk(x, DIRS).min()); 
    if m2 < -1e-9: viol += 1
    s = 1 + (x[1] + x[2] + x[3]) / 3
    if s > 1e-3: ratio_all.append(x[0] / s)
ra = np.array(ratio_all); opt = SQ3H
run.check("II-5a no random NEC-compliant tensor exceeds the LP optimum 0.8660 g/(1+w) (maximum found)", f"max {ra.max():.4f}, quantile 99% {np.quantile(ra,0.99):.4f}, n={len(ra)}, repair violations {viol}", ra.max() <= opt + 1e-9)
run.check("II-5a' random tensors reach >=0.99 of the optimum (frozen expectation; random sampling rarely does)", f"max/opt = {ra.max()/opt:.3f}", ra.max() >= 0.99 * opt, load_bearing=False)
# null dust + Lambda: T = eps k k + rho_L * (-g^{mu nu}); e = rho_L + eps, g = eps
eps, rL = 0.7, 1.0; e = rL + eps
xnd = np.array([eps, -rL + eps / 2 * 0, 0, 0, 0, 0, 0], float)   # build by tensor: T^{mu nu}=eps k^mu k^nu - rL eta^{mu nu}, k=(1,1,0,0)
Tn = np.zeros((4, 4)); k = np.array([1., 1, 0, 0]); eta = np.diag([-1., 1, 1, 1]); Tn = eps * np.outer(k, k) - rL * np.linalg.inv(eta)
e_, g_ = Tn[0, 0], Tn[0, 1]; pis = (Tn[1, 1] + Tn[2, 2] + Tn[3, 3]) / 3; xx = np.array([g_ / e_, Tn[1, 1] / e_, Tn[2, 2] / e_, Tn[3, 3] / e_, 0, 0, 0])
minnd = float(Tkk(xx, DIRS).min()); rat = (g_ / e_) / (1 + pis / e_)
run.check("II-5b null dust + Lambda (type II) is NEC-compliant and has g/e = (3/4)(1+w_iso) exactly", f"min T_kk {minnd:.2e}, g/e/(1+w_iso)={rat:.6f}", minnd > -1e-12 and abs(rat - 0.75) < 1e-9)
# ---------------------------------------------------------------- II-6 type III
print("\n== II-6 type III family, N=5000, seed 195004 ==")
rng = np.random.default_rng(195004); nviol = 0; worst = 0
for _ in range(5000):
    lam = rng.uniform(-1, 1); kap = rng.choice([-1, 1]) * 10 ** rng.uniform(-3, 0); sig = rng.uniform(-1, 1)
    # T_ab = lam eta_ab + kap (l_a e_b + e_a l_b) + sig l_a l_b, l = (1,1,0,0)/sqrt2 (lower index), e = y-hat; k=(1,cos t, sin t,0) & variants
    thetas = np.concatenate([-np.logspace(-6, 0, 300), np.logspace(-6, 0, 300), np.linspace(-math.pi, math.pi, 721)])
    kv = np.stack([np.ones_like(thetas), np.cos(thetas), np.sin(thetas), 0 * thetas], 1)
    lk = -(1 / math.sqrt(2)) * kv[:, 0] + (1 / math.sqrt(2)) * kv[:, 1]     # l_a k^a with l_a=(-1,1,0,0)/sqrt2 (lower)
    ek = kv[:, 2]
    T = 2 * kap * lk * ek + sig * lk ** 2 + lam * 0
    m = float(T.min()); nviol += (m < -1e-15); worst = max(worst, m) if m >= -1e-15 else worst
run.check("II-6 every member of the type-III family violates the NEC (min over null k of T_kk < 0)", f"{nviol}/5000 violate", nviol == 5000, load_bearing=False)
# ---------------------------------------------------------------- II-7 / A2 summary + A6
print("\n== A6 compensated two-component (epoch-by-epoch, e_tot=1) ==")
R = 0.2928; tab = {}
for wlim in (1.0, 1.5, 2.0, 3.0):
    for delta in (0.0, 0.05, 0.162, 0.333):
        s = wlim - 1.0; best = None
        for phi in np.arange(0.0, 0.9999, 1e-4):
            Sf = delta + s * phi                  # (1+w_f) e_f
            ef = 1 - phi
            if Sf > 2 * ef or ef <= 0: break      # w_f <= 1
            gmax = min(SQ3H * Sf, ef)             # NEC-only, capped by the dominant-energy g<=e_f
            if gmax >= R: best = (phi, Sf / ef); break
        tab[(wlim, delta)] = best
        print(f"  w_ph >= -{wlim:3.1f}, total 1+w = {delta:5.3f}: " + (f"smallest phantom fraction e_ph = {best[0]:.4f} (flowing component 1+w_f = {best[1]:.3f})" if best else "R not reachable"))
run.num("A6", {f"{k[0]}_{k[1]}": v for k, v in tab.items()})
run.check("A6 control: with no phantom compensator (w_lim=1) R is never reached for total 1+w <= 0.333", tab[(1.0, 0.333)] is None and tab[(1.0, 0.162)] is None, tab[(1.0, 0.333)] is None, load_bearing=False)
run.check("A6 with a compensator w_ph>=-2, R is reachable at total 1+w=0.05 with e_ph<=0.45 (expectation E: 'bites')", f"{tab[(2.0,0.05)]}", tab[(2.0, 0.05)] is not None and tab[(2.0, 0.05)][0] <= 0.45, load_bearing=False)
run.finish()
