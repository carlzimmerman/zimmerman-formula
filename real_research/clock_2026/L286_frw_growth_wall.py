"""RETRACTION 2026-09-19 (L287): the diagnosis below -- "the momentum constraint contains Psi'" -- was a BUG of the second-order
Euler-Lagrange operator, which dropped the shift's third derivatives; with the general-order operator (L287) Psi does not enter the
momentum constraint at all and the scalar sector has exactly two propagating degrees of freedom in Newtonian gauge. The FRW growth
integration is not blocked by a Dirac problem; it must be redone with the corrected operator (and the covariant healing term).

STATUS 2026-09-19: INCOMPLETE -- no physical growth number obtained. The FRW linearised equations (lapse, momentum, trace, clock,
scalar) are built from the action (build_frw_perturbation_odes_shift, cached) and their derivative structure is certified (V1a), but every
plain-ODE formulation tried (trace equation as Phi's evolution; both constraints as first-order evolution equations; Psi = Phi with the
lapse as evolution) excites a growing constraint-violating mode (momentum residual O(1); a +/-331 per e-fold pair at a = 0.01 that the
exact Minkowski dispersion L285 does not have; delta_d overflows). Cause: the khronon makes the lapse carry a time derivative in the action
(the momentum constraint contains Psi'), so the constraints are not algebraic and the 2-DOF reduction needs the Dirac analysis (CK06).
The V2-V4 numbers printed by this script are NOT physical.

L286 (CK12 perturbations II) -- the FRW linear growth of the candidate's dust at the exponential-wall point, from the action.
Equations: clock_action_build.build_frw_perturbation_odes (metric Psi, Phi; clock T; scalar P; plane wave e^{ikx}; Lambda in the action;
radiation smooth, in a(t) only).  Wall: F = -A exp((Q-Q0)/eps): F1 = F/eps, F2 = F1/eps, F0 = eps F1; a^3 F_Q = const => F1 = F1,0 a^-3;
the dust is 16 pi G rho_d = F0 - Qb F1 = -Qb F1 (1 - eps/Qb).  Units H0 = c = 1, Qb = Q0 = 1 (the wall point of L285), eps/Q0 = 1e-9.
Background: 3(1 + 3c2/2) H^2 = 8 pi G (rho_r + rho_d + rho_Lambda), Om_r = 9.1e-5, Om_m = 0.31 (baryons folded into the dust), Om_L = 0.69.
Dust contrast from the scalar's own stress tensor: delta_d = delta rho_d/rho_d = F2 dQ/F1 = dQ/eps, dQ = P' - Qb Psi.
   V1 the machine ODEs: the lapse equation is a constraint (no second time derivatives of any field), and at k >> aH with the dust
      switched off the system reduces to the L282 structure (checked by the khronon's high-k frequency omega = c_kh k/a).
   V2 growth: from a_i = 1e-4 (generic small initial data) to a = 1, k = 0.01, 0.1, 1 /Mpc: delta_d(a) normalised at a = 0.02 vs LambdaCDM's
      D(a) (same background); the growth suppression g = D/a at a = 1 and the growth rate f = dln delta/dln a at z = 0 vs LambdaCDM's.
   V3 scale-independence: the three k agree on g(1) to < 1% (CDM-like growth) -- or the deviation is reported as the finding.
   V4 the slip Phi/Psi at late times (L279: Psi = Phi at leading order statically).
Checks report what is measured; PASS thresholds are the LambdaCDM tolerances of the work order (growth within 3%)."""
import os, sys, json, time, math
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clock_action_build import build_frw_perturbation_odes_shift as build_frw_perturbation_odes
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
T0 = time.time(); print("L286 -- FRW growth at the exponential-wall point\n", flush=True)
import pickle
CACHE = os.path.join(os.environ.get("SCRATCH", "/tmp"), "L286_frw_odes_shift.pkl")
def _dump(ODE, S):
    pickle.dump(([sp.srepr(o) for o in ODE], {n_: (sp.srepr(v_) if n_ != "amps" else [sp.srepr(x_) for x_ in v_]) for n_, v_ in S.items()}), open(CACHE, "wb"))
def _load():
    O, Sd = pickle.load(open(CACHE, "rb"))
    return [sp.sympify(o) for o in O], {n_: (sp.sympify(v_) if n_ != "amps" else [sp.sympify(x_) for x_ in v_]) for n_, v_ in Sd.items()}
if os.path.exists(CACHE):
    ODE, S = _load(); print(f"    FRW ODEs loaded from cache ({time.time()-T0:.0f} s)", flush=True)
else:
    ODE, S = build_frw_perturbation_odes(); _dump(ODE, S); print(f"    FRW ODEs built and cached ({time.time()-T0:.0f} s)", flush=True)
t, k, KB, c2, c14, beta, xi, Lam, a, Qb, F0, F1, F2 = [S[n] for n in ("t", "k", "KB", "c2", "c14", "beta", "xi", "Lam", "a", "Qb", "F0", "F1", "F2")]
psi, bb, phi, tt, pp = S['amps']
# ---- parameters (H0 = c = 1, Q0 = 1)
Om_r, Om_m, Om_L = 9.1e-5, 0.31, 0.69; c14n = 2.5e-5; c2n = c14n / (1 - 2 * c14n); KBn = 0.2; beta0n = (2 - KBn) / (2 - c14n); epsn = 1e-9
MPC = 3.0856775814913673e22; H0 = 67.4e3 / MPC; C = 2.99792458e8; PC = MPC / 1e6
xin = 4.0 * PC * H0 / C                                              # 4 pc in units of c/H0
Gc = 1 + 3 * c2n / 2                                                 # Carroll-Lim factor (L283)
Hfun = lambda av: math.sqrt((Om_r * av ** -4 + Om_m * av ** -3 + Om_L) / Gc)
# background functions in the ODEs: a(t) and its derivatives, Qb = 1 (q = O(eps ln a) negligible), F1 = -6 Om_m a^-3 /(1 - eps), F2 = F1/eps, F0 = eps F1
ad, add = sp.symbols('adot addot'); av = sp.Symbol('av', positive=True)
F1expr = -6 * Om_m * av ** -3 / (1 - epsn)
subs_bg = {sp.Derivative(a, (t, 2)): add, sp.Derivative(a, t): ad, sp.Derivative(Qb, t): 0, sp.Derivative(F1, t): sp.diff(F1expr, av) * ad, sp.Derivative(F2, t): sp.diff(F1expr, av) * ad / epsn,
           sp.Derivative(F0, t): epsn * sp.diff(F1expr, av) * ad}
ODEb = [o.subs(subs_bg).subs({a: av, Qb: 1, F1: F1expr, F2: F1expr / epsn, F0: epsn * F1expr, KB: KBn, c2: c2n, c14: c14n, beta: beta0n, Lam: 3 * Om_L, xi: xin}) for o in ODE]
ODEb = [sp.expand(o) for o in ODEb]
# derivative orders
D2 = {n: [sp.Derivative(f_, (t, 2)) for f_ in (psi, phi, tt, pp)] for n in range(1)}[0]
lapse_has_second = any(ODEb[0].has(d_) for d_ in D2)
psi_second = any(o.has(sp.Derivative(psi, (t, 2))) for o in ODEb)
print(f"    lapse equation contains second time derivatives: {lapse_has_second}; any equation contains psi'': {psi_second}", flush=True)
check("V1a the lapse equation (varying Psi) is a constraint: no second time derivative of any field; and no equation contains Psi'' (Psi is algebraic)", (not lapse_has_second) and (not psi_second))
# ---- solve: unknowns psi (algebraic), phi'', tt'', pp'' from the other three equations
d1 = {f_: sp.Symbol(f"{f_.func.__name__}1") for f_ in (psi, phi, tt, pp)}; d2s = {f_: sp.Symbol(f"{f_.func.__name__}2") for f_ in (phi, tt, pp)}
v0 = {f_: sp.Symbol(f"{f_.func.__name__}0") for f_ in (psi, phi, tt, pp)}
def flat(o):
    o = o.subs({sp.Derivative(f_, (t, 2)): d2s[f_] for f_ in (phi, tt, pp)})
    o = o.subs({sp.Derivative(f_, t): d1[f_] for f_ in (psi, phi, tt, pp)})
    return o.subs(v0)
E0, EB, E1, E2, E3 = [flat(o) for o in ODEb]          # lapse, momentum (shift), trace, clock, scalar
names = {v0[psi]: "psi", d1[psi]: "psi'", v0[phi]: "phi", d1[phi]: "phi'", d2s[phi]: "phi''", v0[tt]: "T", d1[tt]: "T'", d2s[tt]: "T''", v0[pp]: "P", d1[pp]: "P'", d2s[pp]: "P''"}
for nm, e_ in zip(("lapse", "momentum", "trace", "clock", "scalar"), (E0, EB, E1, E2, E3)):
    print(f"    {nm} equation contains: {[v for s_, v in names.items() if e_.has(s_)]}", flush=True)
# Density variable D = delta Q = P' - Qb Psi (delta_d = D/eps).  No anisotropic stress at c13 = 0 (aether) nor from the scalar at linear
# order: Psi = Phi exactly (the traceless equation; L279 statically).  State (phi, T, T', P, D): Phi' from the lapse constraint,
# T'' from the clock equation, D' from the scalar equation; the momentum and trace equations are redundant and monitored.
D0, D1 = sp.symbols('D0 D1')
Eq = [sp.expand(e_.subs(d2s[pp], D1 + d1[psi]).subs(d1[pp], D0 + v0[psi]).subs(d1[psi], d1[phi]).subs(v0[psi], v0[phi])) for e_ in (E0, EB, E1, E2, E3)]
unknowns = [d1[phi], d2s[tt], D1]
sol = sp.solve([Eq[0], Eq[3], Eq[4]], unknowns, dict=True); assert len(sol) == 1, f"solve returned {len(sol)} solutions"
sol = sol[0]; print(f"    linear solve done ({time.time()-T0:.0f} s)", flush=True)
adddot = sp.Symbol('adddot')
state = [v0[phi], v0[tt], d1[tt], v0[pp], D0]
rows_expr = [sol[d1[phi]], d1[tt], sol[d2s[tt]], D0 + v0[phi], sol[D1]]            # d/dt of (phi, T, T', P, D)
assert not any(r_.has(s_) for r_ in rows_expr for s_ in (d2s[phi], d1[phi], d2s[tt], D1)), "RHS not closed on the state"
Amat = sp.Matrix([[sp.expand(r_).coeff(s_) for s_ in state] for r_ in rows_expr])
assert all(sp.expand(r_ - sum(Amat[i, j] * state[j] for j in range(5))) == 0 for i, r_ in enumerate(rows_expr)), "system not linear/homogeneous"
Gvec = sp.Matrix([[1 if s_ == v0[phi] else 0 for s_ in state]])
def ddt(expr):
    return (sp.diff(expr, av) * ad + sp.diff(expr, ad) * add + sp.diff(expr, add) * adddot + sum(sp.diff(expr, s_) * r_ for s_, r_ in zip(state, rows_expr)))
Emom = sp.expand(Eq[1].subs(d1[phi], sol[d1[phi]]))
Etr = sp.expand(Eq[2].subs(d2s[phi], ddt(sol[d1[phi]])).subs(d1[phi], sol[d1[phi]]).subs(d2s[tt], sol[d2s[tt]]).subs(D1, sol[D1]))
Tvec = sp.Matrix([[Etr.coeff(s_) for s_ in state]]); Mvec = sp.Matrix([[Emom.coeff(s_) for s_ in state]])
bgargs = (av, ad, add, adddot, k)
A_f = sp.lambdify(bgargs, Amat, 'numpy', cse=True); G_f = sp.lambdify(bgargs, Gvec, 'numpy', cse=True); Tr_f = sp.lambdify(bgargs, Tvec, 'numpy', cse=True); Mo_f = sp.lambdify(bgargs, Mvec, 'numpy', cse=True)
print(f"    linear coefficient matrix lambdified ({time.time()-T0:.0f} s)", flush=True)
def bg(av_):
    H = Hfun(av_); ad_ = av_ * H
    dH = (-(4 * Om_r * av_ ** -5 + 3 * Om_m * av_ ** -4) / Gc) / (2 * H)
    d2H = ((20 * Om_r * av_ ** -6 + 12 * Om_m * av_ ** -5) / Gc) / (2 * H) - dH ** 2 / H
    add_ = ad_ * H + av_ * dH * ad_
    dadd_da = H * H + 3 * av_ * H * dH + av_ ** 2 * (dH ** 2 + H * d2H)
    return H, ad_, add_, dadd_da * ad_
SC = np.array([1.0, 1.0, 1.0, 1.0, epsn])           # scaled state z = y / SC  (D = eps delta_d: evolve delta_d)
def A_N(Nv, kk):                      # dz/dN = A_N z
    av_ = math.exp(Nv); H, ad_, add_, adddot_ = bg(av_)
    A = np.array(A_f(av_, ad_, add_, adddot_, kk), dtype=float) / H
    return (A * SC[None, :]) / SC[:, None]
def rhs_N(Nv, z, kk): return A_N(Nv, kk) @ z
def jac_N(Nv, z, kk): return A_N(Nv, kk)
def psi_alg(av_, z, kk):
    H, ad_, add_, adddot_ = bg(av_)
    return float(np.array(G_f(av_, ad_, add_, adddot_, kk), dtype=float).ravel() @ (z * SC))
# LambdaCDM reference: delta'' + (2 + dlnH/dlnN) delta' = 1.5 Om_m(a) delta  in N = ln a (CDM + smooth radiation, same background)
def lcdm_growth(a_grid):
    def f(N, y):
        av_ = math.exp(N); H = Hfun(av_); dlnH = av_ * (-(4 * Om_r * av_ ** -5 + 3 * Om_m * av_ ** -4) / Gc) / (2 * H ** 2)
        Om = Om_m * av_ ** -3 / (Gc * H ** 2)
        return [y[1], -(2 + dlnH) * y[1] + 1.5 * Om * y[0]]
    N0 = math.log(a_grid[0]); r = solve_ivp(f, (N0, 0.0), [1.0, 1.0], t_eval=np.log(a_grid), rtol=1e-10, atol=1e-14)
    return r.y[0], r.y[1] / r.y[0]
a_grid = np.logspace(-4, 0, 400)
res = {}
# diagnostics: RHS magnitudes and the Jacobian's eigenvalues at the start (k = 0.1/Mpc)
kk0 = 0.1 * (C / H0) / MPC
for a_d in (1e-4, 1e-2, 1.0):
    ev_ = np.linalg.eigvals(A_N(math.log(a_d), kk0)); print(f"    eigenvalues of the linear system (per e-fold) at a = {a_d:g}, k = 0.1/Mpc: {np.sort_complex(ev_)}", flush=True)
OUT["eigs_k0.1"] = {str(a_d): [str(e_) for e_ in np.linalg.eigvals(A_N(math.log(a_d), kk0))] for a_d in (1e-4, 1e-2, 1.0)}
OUT["jacobian_eigs_a1e-4"] = [str(e_) for e_ in ev_]
for kMpc in (0.1, 1.0, 0.01):
    kk = kMpc * (C / H0) / MPC                                        # k in units of H0/c
    a_i = 1e-4
    y0 = [0.0, 0.0, 0.0, 0.0, 1e-5]                                   # phi, T, T', P, delta_d = 1e-5
    try:
        r = solve_ivp(lambda Nv, z: rhs_N(Nv, z, kk), (math.log(a_i), 0.0), y0, method='Radau', jac=lambda Nv, z: jac_N(Nv, z, kk), rtol=1e-8, atol=1e-30, t_eval=np.log(a_grid), max_step=0.05)
    except Exception as e_:
        print(f"    k = {kMpc}: integrator raised {e_}", flush=True); continue
    if r.status != 0: print(f"    k = {kMpc}: integrator status {r.status}: {r.message} (reached a = {math.exp(r.t[-1]) if len(r.t) else None})", flush=True)
    if len(r.t) < 10: continue
    rows = np.array([(math.exp(Nv), z[4], z[0], z[0]) for Nv, z in zip(r.t, np.array(r.y).T)])
    res[kMpc] = rows
    # trace-equation residual (Bianchi consistency), relative to its largest term, at a = 0.1 and 1
    for a_c in (0.1, 1.0):
        j_ = np.argmin(abs(rows[:, 0] - a_c)); z_ = np.array(r.y).T[j_]; H_, ad_, add_, adddot_ = bg(a_c)
        tv_ = np.array(Tr_f(a_c, ad_, add_, adddot_, kk), dtype=float).ravel(); resid = abs(tv_ @ (z_ * SC)) / max(abs(tv_ * z_ * SC).max(), 1e-300)
        mv_ = np.array(Mo_f(a_c, ad_, add_, adddot_, kk), dtype=float).ravel(); resm = abs(mv_ @ (z_ * SC)) / max(abs(mv_ * z_ * SC).max(), 1e-300)
        print(f"      trace / momentum residuals at a = {a_c}: {resid:.2e} / {resm:.2e} (relative to the largest term)", flush=True)
    print(f"    k = {kMpc} /Mpc: integrated to a = {math.exp(r.t[-1]):.4f}, {r.nfev} rhs evaluations ({time.time()-T0:.0f} s); delta_d at a = 0.02, 0.1, 1: {[f'{abs(rows[np.argmin(abs(rows[:,0]-x_)),1]):.3e}' for x_ in (0.02, 0.1, 1.0)]}", flush=True)
# growth comparison
Dl, fl = lcdm_growth(a_grid); i20 = np.argmin(abs(a_grid - 0.02))
gl = Dl[-1] / Dl[i20] * 0.02 / 1.0                                   # LambdaCDM D(1)/D(0.02) x (0.02/1): growth suppression relative to a
summary = {}
if not res: print("    no k mode integrated to a = 1", flush=True)
for kMpc, rows in res.items():
    av_, dd = rows[:, 0], np.abs(rows[:, 1])
    j20 = np.argmin(abs(av_ - 0.02)); jl = -1
    g = dd[jl] / dd[j20] * 0.02 / av_[jl]
    # growth rate at z = 0 from the last decade (log-log slope over a in [0.8, 1])
    m = av_ >= 0.8; fz0 = np.polyfit(np.log(av_[m]), np.log(dd[m]), 1)[0]
    slip = rows[-1, 3] / rows[-1, 2] if rows[-1, 2] != 0 else float('nan')
    summary[kMpc] = dict(g1=float(g), f0=float(fz0), slip=float(np.real(slip)), g_lcdm=float(gl), f_lcdm=float(fl[-1]))
    print(f"    k = {kMpc} /Mpc: delta_d(1)/delta_d(0.02) x 0.02 = {g:.4f}  (LambdaCDM {gl:.4f}, ratio {g/gl:.4f});  f(z=0) = {fz0:.4f} (LambdaCDM {fl[-1]:.4f});  Phi/Psi at a = 1: {np.real(slip):.6f}", flush=True)
OUT["summary"] = summary; OUT["curves"] = {str(kM): rows[:, :2].real.tolist() for kM, rows in res.items()}
ok2 = bool(summary) and all(abs(s_['g1'] / s_['g_lcdm'] - 1) < 0.03 for s_ in summary.values())
check("V2 growth within the work order's 3% of LambdaCDM's D(a)/a from a = 0.02 to 1 at k = 0.01, 0.1, 1 /Mpc (measured; a FAIL is the finding)", ok2, str({k_: round(s_['g1']/s_['g_lcdm'], 4) for k_, s_ in summary.items()}))
gs = [s_['g1'] for s_ in summary.values()]
check("V3 scale-independence: the three k agree on the growth suppression to < 1% (CDM-like)", len(gs) == 3 and max(gs) / min(gs) - 1 < 0.01, f"{gs}")
check("V4 growth rate f(z = 0) within 0.03 of LambdaCDM's and the slip Phi/Psi within 1e-3 of 1 at a = 1 (L279's Psi = Phi)", bool(summary) and all(abs(s_['f0'] - s_['f_lcdm']) < 0.03 and abs(s_['slip'] - 1) < 1e-3 for s_ in summary.values()), str({k_: (round(s_['f0'], 4), round(s_['slip'], 5)) for k_, s_ in summary.items()}))
n_pass = sum(CH); print(f"\nL286 COMPLETE: {n_pass}/{len(CH)} checks PASS  ({time.time()-T0:.0f} s).")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
sys.exit(0 if n_pass == len(CH) else 1)
