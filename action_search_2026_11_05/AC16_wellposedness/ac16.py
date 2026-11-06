#!/usr/bin/env python3
"""AC16: final label for v3s / AC2q nonlinear well-posedness (PN label system of AC10).

C1 soft branch: principal part v*I in (P, v); per-label ODE closes.
C2 stiff branch: H = diag(gamma, Pi) symmetrizes A = [[v, Pi], [gamma, v]]; real speeds iff gamma*Pi >= 0.
C3 switch interface: force jump -gamma*Pi_x(x*); transport keeps the compatible class; numeric ladder N3a-N3d.
MUTATE (AC16_MUTATE=1): gamma -> -gamma (C2 must fail). Outputs ac16.json/.out or ac16_MUTATE.json/.out.
Run from the repo root, one thread:  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC16_wellposedness/ac16.py
kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("AC16_MUTATE") == "1"
SGN = -1 if MUT else 1
tag = "ac16_MUTATE" if MUT else "ac16"
res, ok = {}, {}

# ---------------- C1: soft branch ----------------
t, x, a = sp.symbols("t x a", real=True)
v, P, s2 = sp.symbols("v P s2", real=True)
# (P, v): P_t + v P_x = -s2 v (+c), v_t + v v_x = G(P) (zero order); principal matrix:
A_soft = sp.Matrix([[v, 0], [0, v]])
ok["C1_principal_diag"] = A_soft == v * sp.eye(2)
# per-label: enclosed charge S(a,t) = int_{-inf}^{X(a,t)} Pi dx = int_{-inf}^{a} Pi0 da' (labels do not cross)
J = sp.Function("J")(a, t); Pi0 = sp.Function("Pi0")(a)
Pi_lab = Pi0 / J
# d/dt of int Pi dx over label interval = int d_t(Pi J) da = 0 when Pi J = Pi0
ok["C1_label_charge_const"] = sp.simplify(sp.diff(Pi_lab * J, t)) == 0
res["C1"] = dict(principal=str(A_soft), label_charge_rate=str(sp.simplify(sp.diff(Pi_lab * J, t))))

# ---------------- C2: stiff branch ----------------
g = sp.Symbol("gamma", positive=True) * SGN
Pi = sp.Symbol("Pi", positive=True)
A = sp.Matrix([[v, Pi], [g, v]])
H = sp.diag(g, Pi)
sym_res = sp.simplify(H * A - A.T * H)
ev = list(A.eigenvals().keys())
H_pos = bool(sp.ask(sp.Q.positive(g), sp.Q.positive(sp.Symbol("gamma"))) is True)
speeds_real = all(sp.ask(sp.Q.real(e), sp.Q.real(v) & sp.Q.positive(sp.Symbol("gamma")) & sp.Q.positive(Pi)) is True
                  for e in ev)
ok["C2_symmetrizer"] = sym_res == sp.zeros(2, 2)
ok["C2_H_positive"] = H_pos
ok["C2_speeds_real"] = speeds_real
res["C2"] = dict(HA_minus_ATH=str(sym_res), eigenvalues=[str(e) for e in ev], H_positive=H_pos)

# ---------------- C3: switch interface, sympy ----------------
xs, h = sp.symbols("x_s h", real=True)
c1 = sp.Symbol("c1", positive=True)
Pi_loc = c1 * (x - xs)                     # transverse zero, stiff on the right
force = lambda X: -sp.Symbol("gamma") * sp.diff(sp.Max(Pi_loc, 0), x).subs(x, X)
jump = sp.limit(-sp.Symbol("gamma") * sp.diff(sp.Max(Pi_loc, 0), x), x, xs, "+") - \
       sp.limit(-sp.Symbol("gamma") * sp.diff(sp.Max(Pi_loc, 0), x), x, xs, "-")
ok["C3_force_jump"] = sp.simplify(jump - (-sp.Symbol("gamma") * c1)) == 0
# transport: Pi(x) = Pi0(a)/J, d_x = J^-1 d_a  =>  Pi_x = J^-2 Pi0' - Pi0 J^-3 J_a
Pix = sp.diff(Pi0 / J, a) / J
ident = sp.simplify(Pix - (sp.diff(Pi0, a) / J**2 - Pi0 * sp.diff(J, a) / J**3))
astar = sp.Symbol("a_s")
f = sp.Function("f")
Pi0c = (a - astar) ** 2 * f(a)             # compatible: Pi0(a*) = Pi0'(a*) = 0
at_star = sp.simplify((sp.diff(Pi0c, a) / J**2 - Pi0c * sp.diff(J, a) / J**3).subs(a, astar))
ok["C3_transport_identity"] = ident == 0
ok["C3_compatible_preserved"] = at_star == 0
res["C3_sympy"] = dict(force_jump=str(jump), transport_identity_residual=str(ident), compatible_at_astar=str(at_star))


# ---------------- C3: numerics (Lagrangian staggered scheme, gamma = 1, K = 0) ----------------
def run(N, Pi0f, t_meas=0.1, t_max=1.0, gam=1.0, hD=0.05):
    an = np.linspace(-3.0, 3.0, N + 1)
    am = 0.5 * (an[1:] + an[:-1])
    da = an[1] - an[0]
    m = Pi0f(am) * da                        # cell charge; switch state carried by the label (sign of m)
    on = m > 0
    X = an.copy(); V = np.zeros(N + 1)

    def acc(X):
        w = np.diff(X)
        Pc = np.where(on, m / np.where(w > 0, w, np.inf), 0.0)    # max(Pi, 0) per cell; soft cells contribute 0
        a_ = np.zeros_like(X)
        dxn = 0.5 * (X[2:] - X[:-2])
        a_[1:-1] = -gam * (Pc[1:] - Pc[:-1]) / dxn
        return a_

    dt = 0.1 * da
    tcur, t_inv, D = 0.0, None, None
    nsteps_meas = int(round(t_meas / dt)); dt_m = t_meas / nsteps_meas
    step = 0
    while tcur < t_max - 1e-14:
        hstep = dt_m if step < nsteps_meas else dt
        # RK4 on (X, V)
        k1x, k1v = V, acc(X)
        k2x, k2v = V + 0.5 * hstep * k1v, acc(X + 0.5 * hstep * k1x)
        k3x, k3v = V + 0.5 * hstep * k2v, acc(X + 0.5 * hstep * k2x)
        k4x, k4v = V + hstep * k3v, acc(X + hstep * k3x)
        X = X + hstep / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        V = V + hstep / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        tcur += hstep; step += 1
        w = np.diff(X)
        near = np.abs(am) < 0.5
        if t_inv is None and np.any(w[near] <= 0):
            t_inv = tcur
        if step == nsteps_meas:
            D = float(np.interp(hD, an, V) - np.interp(-hD, an, V))
        if t_inv is not None and D is not None:
            break
    return dict(N=N, D=D, t_inv=t_inv)


cases = {
    "N3a_transverse_stiff_right": lambda q: np.tanh(q),
    "N3c_transverse_stiff_left": lambda q: -np.tanh(q),
    "N3d_compatible": lambda q: np.tanh(q) ** 3,
}
Ns = [400, 800, 1600, 3200]
num = {k: [run(N, f) for N in Ns] for k, f in cases.items()}
res["numerics"] = num


def rel(a_, b_):
    return abs(a_ - b_) / max(abs(b_), 1e-300)


A3 = num["N3a_transverse_stiff_right"]; C3c = num["N3c_transverse_stiff_left"]; D3 = num["N3d_compatible"]
pred = -1.0 * 1.0 * 0.1
ok["N3a_converged"] = rel(A3[-1]["D"], A3[-2]["D"]) <= 0.02
ok["N3a_matches_pred"] = rel(A3[-1]["D"], pred) <= 0.15
ok["N3a_not_shrinking"] = abs(A3[-1]["D"]) >= 0.9 * abs(A3[0]["D"])
tinv = [r["t_inv"] for r in A3]
ratios = [tinv[i] / tinv[i + 1] for i in range(len(tinv) - 1)] if all(tinv) else []
ok["N3b_tinv_falls_sqrt2"] = bool(ratios) and all(1.2 <= r <= 1.7 for r in ratios)
ok["N3c_opening"] = rel(C3c[-1]["D"], -pred) <= 0.15 and rel(C3c[-1]["D"], C3c[-2]["D"]) <= 0.02
Dd = [abs(r["D"]) for r in D3]
ok["N3d_falls_with_N"] = all(Dd[i + 1] <= Dd[i] for i in range(len(Dd) - 1))
ok["N3d_small"] = Dd[-1] < 0.1 * abs(A3[-1]["D"])
tinv_d = [r["t_inv"] for r in D3]
if all(tinv_d):
    rat_d = [tinv_d[i] / tinv_d[i + 1] for i in range(len(tinv_d) - 1)]
    ok["N3d_tinv_not_sqrt2"] = not all(1.2 <= r <= 1.7 for r in rat_d)
else:
    rat_d = None
    ok["N3d_tinv_not_sqrt2"] = True
res["N3b_ratios"] = ratios; res["N3d_tinv_ratios"] = rat_d; res["prediction_N3a"] = pred

c1_ok = ok["C1_principal_diag"] and ok["C1_label_charge_const"]
c2_ok = ok["C2_symmetrizer"] and ok["C2_H_positive"] and ok["C2_speeds_real"]
c3_sym = ok["C3_force_jump"] and ok["C3_transport_identity"] and ok["C3_compatible_preserved"]
c3_num = all(ok[k] for k in ok if k.startswith("N3a") or k.startswith("N3b") or k.startswith("N3c"))
control = ok["N3d_falls_with_N"] and ok["N3d_small"] and ok["N3d_tinv_not_sqrt2"]
if c1_ok and c2_ok and c3_sym:
    label = "FAIL (classical, generic data): no C1 solution across a transverse switch interface; well-posed per branch"
    if not (c3_num and control):
        label += " [C3 numerics not fully confirming, see checks]"
else:
    label = "branch check failed: " + ", ".join(k for k in ("C1", "C2") if not {"C1": c1_ok, "C2": c2_ok}[k])
out = dict(mode="MUTATE" if MUT else "main", label=label, checks=ok, C1_pass=c1_ok, C2_pass=c2_ok,
           C3_sympy=c3_sym, C3_numerics=c3_num, C3_control_separates=control, results=res,
           note="kappa = 1/2 FITTED; not theory closed")
txt = json.dumps(out, indent=1, default=str)
open(os.path.join(HERE, tag + ".json"), "w").write(txt + "\n")
lines = [f"{k}: {'ok' if val else 'FAIL'}" for k, val in ok.items()]
summary = "\n".join(lines) + f"\nN3a: {[ (r['N'], r['D'], r['t_inv']) for r in A3]}\nN3c: {[(r['N'], r['D']) for r in C3c]}\n" \
          f"N3d: {[(r['N'], r['D'], r['t_inv']) for r in D3]}\nN3b ratios {ratios}\nLABEL: {label}\n"
open(os.path.join(HERE, tag + ".out"), "w").write(summary)
print(summary)
sys.exit(0 if (c1_ok and c2_ok and c3_sym) else 1)
