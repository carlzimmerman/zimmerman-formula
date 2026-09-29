#!/usr/bin/env python3
"""
CFG101 ATTACK -- which hypotheses of the CFG50 no-go are load-bearing?  FROZEN BEFORE ANY RUN of this script (the main script cfg101_main.py had already been run and its
results seen; the diagnosis of the 0.505 vs 0.5008 difference in the main run was done AFTER that run by reading CFG50's D2 script, and is reported as such).
Same conventions as cfg101_main.py (exponential sphere, units G = M_b = h = 1, eps = a0 h^2/(G M_b), target option A, Pi = the target's own Jeans stress, chi_c = 3).  Nothing here says the theory is closed.
Question set (each is a modification of ONE hypothesis; the no-go is 'load-bearing' on it iff the ceiling or the reciprocity failure moves):
  X1  COUPLING FORM, three free constants.  h_ij = a d_i d_j Phi_b + b delta_ij lap Phi_b + c delta_ij Phi_b   (tidal = (a,b,c) = (-chi, chi, 0); c-term = a WEP-violating rescaling of the fluid's kinetic term by the baryon potential).
       Fluid-side force (definition D_c4, CFG50's): a_f = (1/2 rho_c)[h_rr' Pi_rr + 2 h_perp' Pi_perp].  Ghost-free: 1 + h_rr >= 0 and 1 + h_perp >= 0 at every r (linear in (a,b,c) -> LP).
       Reaction (adjoint, general): a_react = 2 pi G [ a (Pi_rr' + 2(Pi_rr-Pi_perp)/r) + b (Pi_rr' + 2 Pi_perp') ] + 2 pi G c r^-2 Int_0^r r'^2 (Pi_rr + 2 Pi_perp) dr'.
       LP (scipy linprog, r grid 0.3..3 h and a coarse global grid for the ghost constraint):  O1 = max a_f/g_tot at r = 0.3h, 1h, 3h; O2 = max t s.t. a_f/g_tot >= t on [0.3h,3h];
       O3 = min rho s.t. |a_react|/g_tot <= rho on [0.3h,3h] at eps of M_b = 1e10 (0.614) and a_f/g_tot >= t0 on [0.3h,3h] for t0 = 0.5*O2(tidal) and t0 = 0.1.  Each for (i) the tidal line b=-a, c=0 (control: must reproduce cfg101_main's ceiling 0.5008 at 1h-ish) and (ii) the full (a,b,c) family.
       Reported, no pass line; the question is whether a_f/g_tot reaches 1 (full support) anywhere in [0.3h,3h] and whether the reciprocity ratio can be made small.
  X2  FLUID-SIDE FORCE DEFINITION.  D_c4 (above) versus D_full = the force appearing in the exact canonical-momentum balance of a particle in L = (1/2)(delta+h)v v - Phi (geodesic + Jeans identity substituted):
       a_full/g = (s/2)[ -h_rr'/2 + (1-beta) h_perp' + 2(1-beta)(h_perp-h_rr)/s ] + h_rr,   1-beta = Pi_perp/Pi_rr   (derived by hand from d/dt(g_ij v^j) = (1/2) d_i h_jk v^j v^k - d_i Phi; the moment form is checked symbolically below).
       Ceiling of D_full at the tidal ghost limit and in the (a,b,c) LP.  The REACTION is definition-independent (first variation of S_int at fixed Pi), so only the fluid side changes.
  X3  NONLINEAR COUPLING.  h = exp(chi T) - 1 (ghost-free by construction for all chi).  Scan chi<0: sup_r a_f/g_tot over [0.3,5]h and the reaction ratio |a_react|/a_f at the chi that first gives a_f(1h)/g_tot >= 1 (if it exists).  Control: chi small reproduces the linear coupling to 1e-2.
  X4  FLUID DISPERSION SCALE: a_f and a_react are both LINEAR in Pi.  Multiplying Pi by kappa_sigma changes the ceiling and the reaction by the same factor (ratio a_react/a_f is Pi-scale-free) -- verified numerically; the ceiling 0.5 is a statement at sigma_r^2 = V_c^2/2.
  X5  ISOTROPIC Pi (any baryon geometry): sympy: q = chi lap(P) exactly, so lambda = -4 pi G chi P, a_react = 4 pi G chi grad P, and a_f = (4 pi G chi P/rho_c) grad(rho_b) (contact term): verified in Cartesian sympy and against the 3-D adjoint machinery.
  X6  NON-SPHERICAL BARYONS (ghost side only; the reciprocity theorem is geometry-free, already tested in 3-D in the main script): homogeneous oblate spheroid, exact depolarisation factors N_z(q), N_x = (1-N_z)/2, T_ii(0) = 4 pi G rho (1-N_i),
       lambda_max(T) at fixed M and equatorial radius: ratio to the sphere = (1/q)(1-N_x)/(2/3); control q = 1 -> ratio 1.  A defined non-spherical TARGET does not exist (CFG44: disc closure differs 3-15x), so no ceiling is computed for flattened baryons.
  X7  DIAGNOSTIC of the main run's ceiling (0.5008 vs CFG50's 0.505), run on my own code: chi_c from a grid starting at r0 = 0.01 h (CFG50's D2 declares r0 = 1e-2 h in its source header -- read only after my main run) versus the continuum limit.
Controls (must hold): X1 tidal LP reproduces the direct evaluation; superset property (full family >= tidal line); X3 small-chi limit; X6 q=1; X5 sympy identities.
MUTATE=1 : the 'tidal line' of X1 is replaced by b = +a (non-tidal); the control 'tidal LP reproduces the direct tidal evaluation (0.5008)' must FAIL.
Exit 0 iff all controls pass (mutant must exit 1).
"""
import os, sys, json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import linprog
from scipy.special import gammainc
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
MUT = os.environ.get("MUTATE", "0")
OUT = HERE / f"cfg101_attack_results{'' if MUT=='0' else '_MUTATE_'+MUT}.json"
CH = []; NUM = {}
def check(n, ok, d=""):
    CH.append((n, bool(ok), d)); print(f"[{'PASS' if ok else 'FAIL'}] {n} :: {d}")

# ------------------------------------------------ profile (same as main)
s_ = sp.symbols('s', positive=True)
Mf = sp.Function('Mf')(s_)
dM = {sp.Derivative(Mf, s_): s_**2 * sp.exp(-s_) / 2}
Dd = lambda e: sp.diff(e, s_).subs(dM)
rho_e = sp.exp(-s_) / (8 * sp.pi)
Phi_e = -Mf / s_ - (1 + s_) * sp.exp(-s_) / 2
Trr_e = 2 * Mf / s_**3; Tp_e = 4 * sp.pi * rho_e - Mf / s_**3
Pirr_e = Mf / (8 * sp.pi * s_**2); Pip_e = Pirr_e * (1 + 2 * sp.pi * s_**3 * rho_e / Mf)
# building blocks of h for the (a,b,c) family: h_rr = a Hrr + b Bt + c Ph ; h_perp = a Hp + b Bt + c Ph
Hrr_e = 4 * sp.pi * rho_e - 2 * Mf / s_**3   # Phi''
Hp_e = Mf / s_**3                             # Phi'/r
Bt_e = 4 * sp.pi * rho_e                      # lap Phi
lam = lambda e: sp.lambdify(s_, e, modules=[{'Mf': lambda v: gammainc(3, v)}, 'numpy'])
E = dict(Mb=Mf, rho=rho_e, Trr=Trr_e, Tp=Tp_e, Pirr=Pirr_e, Pip=Pip_e, Hrr=Hrr_e, Hp=Hp_e, Bt=Bt_e, Ph=Phi_e)
for k in list(E):
    E["d" + k] = Dd(E[k])
F = {k: lam(v) for k, v in E.items()}
Mfun = lambda v: gammainc(3, v)
GT = 1 - 0  # placeholder

def gtot(eps, s):
    s0 = 1e-8 * min(1.0, eps)
    sol = solve_ivp(lambda t, m: [eps * t * Mfun(t) / (Mfun(t) + m[0])], (s0, s[-1]), [np.sqrt(eps * s0**5 / 15.0)], t_eval=s, rtol=1e-12, atol=1e-30, method="LSODA")
    return (Mfun(s) + sol.y[0]) / s**2

SGL = np.geomspace(1e-3, 60.0, 1500)          # global ghost-constraint grid
SW = np.geomspace(0.3, 3.0, 60)                # support window
def rows(s):
    """return dict of arrays: h_rr,h_perp,dh_rr,dh_perp as linear maps of (a,b,c): shape (n,3)"""
    hrr = np.stack([F["Hrr"](s), F["Bt"](s), F["Ph"](s)], 1)
    hp = np.stack([F["Hp"](s), F["Bt"](s), F["Ph"](s)], 1)
    dhrr = np.stack([F["dHrr"](s), F["dBt"](s), F["dPh"](s)], 1)
    dhp = np.stack([F["dHp"](s), F["dBt"](s), F["dPh"](s)], 1)
    return hrr, hp, dhrr, dhp
def af_rows_c4(s):
    hrr, hp, dhrr, dhp = rows(s)
    Mb = F["Mb"](s); pr = F["Pirr"](s)[:, None]; pp = F["Pip"](s)[:, None]
    return (2 * np.pi * s**3 / Mb)[:, None] * (dhrr * pr + 2 * dhp * pp)
def af_rows_full(s):
    hrr, hp, dhrr, dhp = rows(s)
    ratio = (F["Pip"](s) / F["Pirr"](s))[:, None]        # 1-beta
    return (s[:, None] / 2) * (-0.5 * dhrr + ratio * dhp + 2 * ratio * (hp - hrr) / s[:, None]) + hrr
def react_rows(s, eps, gt):
    # Pi = eps * (Pirr_h, Pip_h);  a_react/g_tot
    Pr, Pp = F["Pirr"](s), F["Pip"](s); dPr, dPp = F["dPirr"](s), F["dPip"](s)
    ra = 2 * np.pi * (dPr + 2 * (Pr - Pp) / s)
    rb = 2 * np.pi * (dPr + 2 * dPp)
    from scipy.integrate import cumulative_trapezoid
    fine = np.geomspace(1e-6, s[-1], 40001)
    integ = cumulative_trapezoid(fine**2 * (F["Pirr"](fine) + 2 * F["Pip"](fine)), fine, initial=0)
    rc = 2 * np.pi * np.interp(s, fine, integ) / s**2
    return eps * np.stack([ra, rb, rc], 1) / gt[:, None]

def ghost_A():
    hrr, hp, _, _ = rows(SGL)
    # 1 + h >= 0  ->  -h <= 1
    return np.vstack([-hrr, -hp]), np.ones(2 * len(SGL))

def lp_max(objective_row, mask_tidal=None, extra_A=None, extra_b=None, bounds=None):
    Ag, bg = ghost_A()
    A = Ag; b = bg
    if extra_A is not None: A = np.vstack([A, extra_A]); b = np.concatenate([b, extra_b])
    Aeq = None; beq = None
    if mask_tidal:   # a + b = 0 (tidal: b=-a  => here parameters (a,b,c) with b=-a means chi=-a... ), c = 0
        Aeq = np.array([[1.0 if MUT == "0" else -1.0, 1.0, 0.0], [0, 0, 1.0]]); beq = np.zeros(2)   # MUT=1: b = +a instead of b = -a
    res = linprog(-objective_row, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=[(-1e4, 1e4)] * 3, method="highs")
    return res

def lp_maxmin(Arows, mask_tidal):
    # variables (a,b,c,t): maximize t s.t. Arows(s) v >= t
    Ag, bg = ghost_A()
    A = np.hstack([Ag, np.zeros((Ag.shape[0], 1))]); b = bg.copy()
    A = np.vstack([A, np.hstack([-Arows, np.ones((Arows.shape[0], 1))])]); b = np.concatenate([b, np.zeros(Arows.shape[0])])
    Aeq = beq = None
    if mask_tidal:
        Aeq = np.array([[1.0 if MUT == "0" else -1.0, 1.0, 0, 0], [0, 0, 1.0, 0]]); beq = np.zeros(2)
    res = linprog(np.array([0, 0, 0, -1.0]), A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=[(-1e4, 1e4)] * 3 + [(-1e4, 1e4)], method="highs")
    return res

def lp_min_reaction(Aaf, Ar, t0, mask_tidal):
    # variables (a,b,c,rho): minimize rho s.t. Ar v <= rho, -Ar v <= rho, Aaf v >= t0, ghost
    Ag, bg = ghost_A()
    n = Ar.shape[0]
    A = np.vstack([np.hstack([Ag, np.zeros((Ag.shape[0], 1))]), np.hstack([Ar, -np.ones((n, 1))]), np.hstack([-Ar, -np.ones((n, 1))]),
                   np.hstack([-Aaf, np.zeros((Aaf.shape[0], 1))])])
    b = np.concatenate([bg, np.zeros(n), np.zeros(n), -t0 * np.ones(Aaf.shape[0])])
    Aeq = beq = None
    if mask_tidal:
        Aeq = np.array([[1.0, 1.0, 0, 0], [0, 0, 1.0, 0]]); beq = np.zeros(2)
    res = linprog(np.array([0, 0, 0, 1.0]), A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=[(-1e4, 1e4)] * 3 + [(0, 1e6)], method="highs")
    return res

def main():
    # ---------------- X5 / X2 sympy
    x, y, z = sp.symbols('x y z', real=True)
    P = sp.exp(-(x**2 + 2 * y**2 + 3 * z**2)) * (1 + x + y * z)
    chi = sp.symbols('chi')
    Fm = chi * P / 2 * sp.eye(3)
    X = (x, y, z)
    lap = lambda f: sum(sp.diff(f, v, 2) for v in X)
    q = lap(Fm.trace()) - sum(sp.diff(Fm[i, j], X[i], X[j]) for i in range(3) for j in range(3))
    check("X5 isotropic Pi: q = (delta lap - d d)F = chi lap(P) exactly (Cartesian sympy)", sp.simplify(q - chi * lap(P)) == 0, "so lambda = -4 pi G chi P, a_react = 4 pi G chi grad P; a_f = (4 pi G chi P/rho_c) grad rho_b is contact")
    # moment-form identity for D_full: radial component of 1/rho [ 1/2 d_i h_jk Pi^jk - d_j (h_ik Pi^jk) ] equals the geodesic expression after Jeans substitution
    r, hr, hp, Pr, Pp, rho, g = sp.symbols('r h_r h_p P_r P_p rho g')
    hrf, hpf, Prf, Ppf = [sp.Function(n)(r) for n in ('hr', 'hp', 'Pr', 'Pp')]
    mom = (sp.Rational(1, 2) * (sp.diff(hrf, r) * Prf + 2 * sp.diff(hpf, r) * Ppf) - (sp.diff(hrf * Prf, r) + 2 * (hrf * Prf - hpf * Ppf) / r))
    jeans = sp.diff(Prf, r) + 2 * (Prf - Ppf) / r          # = -rho g
    geo = (-sp.Rational(1, 2) * sp.diff(hrf, r) * Prf + sp.diff(hpf, r) * Ppf + 2 * (hpf - hrf) * Ppf / r) + hrf * (-jeans)
    check("X2 canonical-momentum-flux force = geodesic expression after Jeans substitution (sympy)", sp.simplify(mom - geo) == 0, "-(1/2) h_rr' P_r + h_p' P_p + 2(h_p-h_r)P_p/r + h_r rho g")

    # ---------------- X1/X2 LP
    eps10 = 0.6141
    gt_w = gtot(eps10, SW)
    Ac4 = af_rows_c4(SW); Afu = af_rows_full(SW); Arw = react_rows(SW, eps10, gt_w)
    for name, Aaf in (("c4", Ac4), ("full", Afu)):
        print(f"\n--- fluid-side force definition D_{name} ---")
        for lab, mt in (("tidal line", True), ("full (a,b,c)", False)):
            out = {}
            for s0 in (0.3, 1.0, 3.0):
                row = (af_rows_c4(np.array([s0])) if name == "c4" else af_rows_full(np.array([s0])))[0]
                res = lp_max(row, mask_tidal=mt)
                out[s0] = (-res.fun if res.status == 0 else float('nan'), res.status)
            res2 = lp_maxmin(Aaf, mt)
            t = res2.x[3] if res2.status == 0 else float('nan')
            NUM[f"{name}|{lab}|O1"] = {str(k): v for k, v in out.items()}; NUM[f"{name}|{lab}|O2"] = (float(t), int(res2.status), None if res2.status else [float(v) for v in res2.x[:3]])
            print(f"  {lab:14s}: O1 sup a_f/g at 0.3h,1h,3h = " + ", ".join(f"{out[k][0]:.4f}(st{out[k][1]})" for k in out) + f";  O2 max-min over [0.3,3]h = {t:.4f} (st {res2.status})" + ("" if res2.status else f"  (a,b,c)={np.round(res2.x[:3],4)}"))
            # O3
            tid_t = NUM.get(f"{name}|tidal line|O2", (0,))[0]
            for t0 in (0.1, 0.5 * tid_t if tid_t == tid_t else 0.05):
                r3 = lp_min_reaction(Aaf, Arw, t0, mt)
                NUM[f"{name}|{lab}|O3|t0={t0:.3f}"] = (float(r3.x[3]) if r3.status == 0 else None, int(r3.status))
                print(f"     O3 t0={t0:.3f}: min max|a_react|/g on [0.3,3]h (eps={eps10}) = " + (f"{r3.x[3]:.4f}" if r3.status == 0 else f"infeasible/status {r3.status}"))
    # control: tidal LP O1 at s0 ~ peak vs direct evaluation
    sp_ = np.linspace(0.7, 1.0, 301)
    rowsA = af_rows_c4(sp_)
    direct = np.max(rowsA @ np.array([3.0, -3.0, 0.0]))            # a=-chi with chi=-3 -> a=+3, b=-3 ; T = -(chi)*... ; (a,b)=(+3,-3) is chi=-3 (a=-chi)
    lpv = max(-lp_max(rowsA[i], mask_tidal=True).fun for i in range(0, len(sp_), 10))
    check("X1 control: tidal-line LP sup a_f/g (r in 0.7..1) equals the direct tidal evaluation at chi=-chi_c (0.5008)", abs(lpv - direct) < 2e-3 and abs(direct - 0.5008) < 1e-3, f"LP {lpv:.5f}, direct {direct:.5f}")
    # superset property
    ok_sup = True
    for name, fn in (("c4", af_rows_c4), ("full", af_rows_full)):
        for s0 in (0.3, 1.0, 3.0):
            row = fn(np.array([s0]))[0]
            a1 = -lp_max(row, mask_tidal=True).fun; a2 = -lp_max(row, mask_tidal=False).fun
            ok_sup &= (a2 >= a1 - 1e-9)
    check("X1 control: full-family optimum >= tidal-line optimum (superset)", ok_sup, "")

    # ---------------- X3 nonlinear
    s = np.geomspace(0.02, 40, 6000)
    Trr, Tp = F["Trr"](s), F["Tp"](s); dTrr, dTp = F["dTrr"](s), F["dTp"](s)
    Pr, Pp = F["Pirr"](s), F["Pip"](s); Mb = F["Mb"](s)
    def nl(chi_):
        hpr = chi_ * dTrr * np.exp(chi_ * Trr); hpp = chi_ * dTp * np.exp(chi_ * Tp)
        af = 2 * np.pi * s**3 / Mb * (hpr * Pr + 2 * hpp * Pp)
        return af
    def lin(chi_):
        return 2 * np.pi * s**3 / Mb * (chi_ * dTrr * Pr + 2 * chi_ * dTp * Pp)
    e_small = -3.0e-3
    check("X3 control: exp coupling at |chi| = 1e-3 chi_c equals the linear coupling to 1e-2", np.max(np.abs(nl(e_small) - lin(e_small))[(s > 0.3) & (s < 5)]) < 1e-2 * np.max(np.abs(lin(e_small))), f"max rel {np.max(np.abs(nl(e_small)-lin(e_small))[(s>0.3)&(s<5)])/np.max(np.abs(lin(e_small))):.2e}")
    gt_s = gtot(eps10, s)
    print("\n--- X3 nonlinear h = exp(chi T) - 1, chi = -k chi_c, eps=0.614 (M_b=1e10) ---")
    scan = []
    for k in (0.5, 1, 2, 3, 5, 10, 20, 50):
        chi_ = -3.0 * k
        af = nl(chi_)
        Frr = 0.5 * Pr * chi_ * np.exp(chi_ * Trr) * eps10; Fp = 0.5 * Pp * chi_ * np.exp(chi_ * Tp) * eps10
        ar = 8 * np.pi * (np.gradient(Fp, s) + (Fp - Frr) / s) / gt_s
        m = (s > 0.3) & (s < 5)
        i1 = np.argmin(abs(s - 1.0)); i03 = np.argmin(abs(s - 0.3))
        row = (k, af[m].max(), af[i1], ar[i1], ar[i1] / (af[i1] * 1.0 if abs(af[i1]) > 1e-12 else np.nan), af[i03], ar[i03])
        scan.append(row)
        print(f"  k={k:5.1f}: sup_[0.3,5]h a_f/g = {row[1]:9.4f}; at 1h a_f/g = {row[2]:9.4f}, a_react/g = {row[3]:9.4f}, ratio a_react/(a_f) = {row[3]/row[2] if abs(row[2])>1e-12 else float('nan'):8.3f}; at 0.3h a_f/g={row[5]:9.4f} a_react/g={row[6]:9.4f}")
    NUM["X3_scan"] = [[float(v) for v in r_] for r_ in scan]

    # ---------------- X4 Pi-scale invariance of the ratio (linear) -- numeric
    R1 = react_rows(SW, eps10, gt_w) @ np.array([3.0, -3.0, 0.0]) / (Ac4 @ np.array([3.0, -3.0, 0.0]))
    R2 = react_rows(SW, eps10 * 7.0, gt_w * 1.0) @ np.array([3.0, -3.0, 0.0]) / (7.0 * (Ac4 @ np.array([3.0, -3.0, 0.0])))
    check("X4 ratio a_react/a_f is invariant under a rescaling of Pi at fixed g_tot (both linear in Pi)", np.allclose(R1, R2, rtol=1e-9), f"R(0.3h)={R1[0]:.3f}, R(1h)~{np.interp(1.0,SW,R1):.3f} at eps={eps10}")
    NUM["R_ratio_eps0.614"] = dict(s03=float(R1[0]), s1=float(np.interp(1.0, SW, R1)))
    for tag, eps_ in (("1e9", 2.741), ("1e10", 0.6141), ("1e12", 0.01717)):
        g_ = gtot(eps_, np.array([0.3, 1.0, 3.0]))
        Rr = react_rows(np.array([0.3, 1.0, 3.0]), eps_, g_) @ np.array([3.0, -3.0, 0.0]) / (af_rows_c4(np.array([0.3, 1.0, 3.0])) @ np.array([3.0, -3.0, 0.0]))
        print(f"  a_react/a_f (tidal, ghost-limited, c4) at 0.3h,1h,3h for M_b={tag} (eps={eps_}): {np.round(Rr,3)}")
        NUM[f"R_{tag}"] = [float(v) for v in Rr]

    # ---------------- X6 spheroid
    print("\n--- X6 oblate homogeneous spheroid: lambda_max(T_center)/sphere at fixed M and equatorial radius ---")
    ok6 = True
    for qv in (1.0 - 1e-6, 0.5, 0.2, 0.1, 0.05):
        Nz = (1 / (1 - qv**2)) * (1 - qv * np.arccos(qv) / np.sqrt(1 - qv**2))
        Nx = (1 - Nz) / 2
        ratio = (1 / qv) * (1 - Nx) / (2 / 3)
        print(f"  q={qv:8.6f}: N_z={Nz:.5f}, N_x={Nx:.5f}, lambda_max/lambda_sphere = {ratio:.4f}  (chi_c scales as 1/{ratio:.3f})")
        NUM[f"X6_q{qv:.3f}"] = float(ratio)
        if qv > 0.999: ok6 &= abs(ratio - 1) < 1e-4 and abs(Nz - 1 / 3) < 1e-5
    check("X6 control: q -> 1 gives N = 1/3 and ratio 1", ok6, "")

    # ---------------- X7 grid-start diagnostic
    print("\n--- X7 ceiling vs the start radius r0 of the chi_c grid (main run: r0 = 1e-5 h) ---")
    for r0 in (1e-5, 1e-3, 1e-2):
        sg = np.geomspace(r0, 30, 6001)
        lm = max(F["Trr"](sg).max(), F["Tp"](sg).max())
        af = np.abs(-1 / lm * 2 * np.pi * sg**3 / F["Mb"](sg) * (F["dTrr"](sg) * F["Pirr"](sg) + 2 * F["dTp"](sg) * F["Pip"](sg)))
        m = (sg > 0.3) & (sg < 5)
        print(f"  r0={r0:g}: chi_c = {1/lm:.6f}, ceiling = {af[m].max():.5f} at r/h = {sg[m][af[m].argmax()]:.3f}")
        NUM[f"X7_r0_{r0:g}"] = (float(1 / lm), float(af[m].max()))

    nf = sum(1 for c in CH if not c[1])
    NUM["checks"] = CH
    OUT.write_text(json.dumps(NUM, indent=1, default=float))
    print(f"\nMUTATE={MUT}: {len(CH)-nf}/{len(CH)} controls pass")
    sys.exit(0 if nf == 0 else 1)

if __name__ == "__main__":
    main()
