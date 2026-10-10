#!/usr/bin/env python3
"""CFG558: velocity part -- is the isotropic (scalar) constraint forced; knob-free overfill removal; alpha-robustness by the age.
FROZEN_CRITERIA.md (f6b7ced5d).

Q1: sympy I1-I5 (equivariance of the dissipative bracket, invariant linear constraints, invariance theorem, what the bracket
alone imposes, the tensor multiplier term) + toy diagnostic (anisotropy and tensor-Jeans residual of the realised end states).
Q2: V3 = two-sided drift (FIX-1) + OU toward sigma_*^2 = P_hat/rho_hat, rho_hat = min(rho_c, rho_ph) (T1-admissible part of the
current density), P_hat = int_r^R rho_hat g (g of the current real enclosed mass, G9).
Q3: V3 at alpha = 0.5, 1, 2, IC-B and IC-C, 15 Gyr; gate at 13.8 Gyr; t90.
Bench = CFG544's spherical N-body toy, imported unchanged via CFG554's module (read only).
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy mass required; not "theory closed".
CFG558_MUTATE=1 -> MI (tensor maxent target on rho_hat), MO (overfill rule removed = FIX-2), alpha x 0.25 reported.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg558.py
"""
import os, sys, json, math, time, importlib.util
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ["CFG544_MUTATE"] = "0"; os.environ["CFG550_MUTATE"] = "0"; os.environ["CFG554_MUTATE"] = "0"
import numpy as np
import sympy as sp
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("cfg554", os.path.join(HERE, "..", "CFG554_selfconsistent_jeans_target", "cfg554.py"))
T554 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(T554)
T544 = T554.T544                      # one shared instance (ALPHA is set on it per job)
J544 = T554.J544; J541 = T544.J541
MUT = os.environ.get("CFG558_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
NPROC = 4
NB, NPART, EPS = T544.NB, T544.NPART, T544.EPS
Mb_enc, Mph_enc = T544.Mb_enc, T544.Mph_enc
C2_544 = T554.C2_544
T_AGE = 13.8
OUT, RES = [], {"lane": "CFG558", "mutate": MUT, "criteria_commit": "f6b7ced5d",
                "settings": dict(kappa=0.5, footings=T544.FOOT, toy="CFG544 cfg544.py imported unchanged (via CFG554)",
                                 N=NPART, seed=T544.SEED, alphas=[0.5, 1.0, 2.0], T_Gyr=15.0, t_age=T_AGE)}


def log(s=""):
    print(s, flush=True); OUT.append(s)


# ================================================================================================ V3 target
def v3_target(c, rf, rc, dr, mc, rho, rhoph, cap=True):
    """sigma_*^2 per bin: hydrostatic temperature of rho_hat = min(rho, rho_ph) in the field of the current real mass.
    With cap=False this is FIX-2's sigma_J^2 (same operations as CFG544 ou_step). Returns (s2, rho_hat, gf, n_guard)."""
    rho_hat = np.minimum(rho, rhoph) if cap else rho
    Menc_c = Mb_enc(c, rc) + np.concatenate([[0.0], np.cumsum(mc)[:-1]]) + 0.5 * mc
    gb = Menc_c * rc / (rc ** 2 + EPS ** 2) ** 1.5
    fP = rho_hat * gb * dr
    Pf = np.concatenate([np.cumsum(fP[::-1])[::-1], [0.0]])
    Pc = 0.5 * (Pf[1:] + Pf[:-1])
    guard = (rho > 0) & (rho_hat <= 0)
    s2 = np.where(rho_hat > 0, Pc / np.maximum(rho_hat, 1e-300), 0.0)
    if guard.any():                                  # rho_ph = 0 in an occupied bin: fall back to FIX-2 (counted, disclosed)
        s2J = np.where(rho > 0, np.concatenate([np.cumsum((rho * gb * dr)[::-1])[::-1], [0.0]])[:-1] / np.maximum(rho, 1e-300), 0.0)
        s2 = np.where(guard, s2J, s2)
    Mf = Mb_enc(c, rf) + np.concatenate([[0.0], np.cumsum(mc)])
    gf = Mf * rf / (rf ** 2 + EPS ** 2) ** 1.5
    return s2, rho_hat, gf, int(guard.sum())


class Toy558(T554.Toy554):
    def __init__(self, c, mode):
        super().__init__(c, "b" if mode != "none" else "none", 1.0, None)
        self.mode558 = mode; self.n_guard = 0; self.n_fail = 0; self.n_solve = 0; self.last_s2 = None
        self.n_over_bins = 0; self.n_bins_occ = 0

    def vel_step(self, r, vr, vt, dt, g, rng):
        c = self.c; al = T544.ALPHA
        mc = self.m * np.histogram(r, self.rf)[0]; rho = mc / self.V
        k = np.clip(np.searchsorted(self.rf, r) - 1, 0, NB - 1)
        inside = r < c["rta"]
        gam = al * np.sqrt(4 * math.pi * (self.rhob + rho))[k]
        a = np.exp(-gam * dt)
        if self.mode558 in ("v3", "fix2"):
            s2, rho_hat, gf, ng = v3_target(c, self.rf, self.rc, self.dr, mc, rho, self.rhoph, cap=(self.mode558 == "v3"))
            self.n_guard += ng; self.last_s2 = s2
            self.n_over_bins += int(((rho > self.rhoph) & (rho > 0)).sum()); self.n_bins_occ += int((rho > 0).sum())
            b = np.sqrt(s2[k] * (1 - a ** 2))
            K0 = 0.5 * self.m * np.sum(vr ** 2 + vt ** 2)
            x1, x2, x3 = rng.standard_normal((3, r.size))
            vr_n = np.where(inside, a * vr + b * x1, vr)
            vtx = a * vt + b * x2; vty = b * x3
            vt_n = np.where(inside, np.hypot(vtx, vty), vt)
            K1 = 0.5 * self.m * np.sum(vr_n ** 2 + vt_n ** 2)
            return vr_n, vt_n, K1 - K0
        if self.mode558 == "mi":                          # tensor (route-a) maxent target on rho_hat
            s2i, rho_hat, gf, _ = v3_target(c, self.rf, self.rc, self.dr, mc, rho, self.rhoph, cap=True)
            occ = np.where(rho_hat > 0)[0]
            self.n_solve += 1
            sr2, st2, ok = T554.maxent_target(self.rf, rho_hat, gf, s2i[occ[0]] if occ.size else 1.0)
            if not ok:
                self.n_fail += 1
                return vr, vt, 0.0
            br = np.sqrt(sr2[k] * (1 - a ** 2)); bt = np.sqrt(st2[k] * (1 - a ** 2))
            K0 = 0.5 * self.m * np.sum(vr ** 2 + vt ** 2)
            x1, x2, x3 = rng.standard_normal((3, r.size))
            nr = a * vr + br * x1; vtx = a * vt + bt * x2; vty = bt * x3; nt = np.hypot(vtx, vty)
            vr_n = np.where(inside, nr, vr); vt_n = np.where(inside, nt, vt)
            K1 = 0.5 * self.m * np.sum(vr_n ** 2 + vt_n ** 2)
            return vr_n, vt_n, K1 - K0
        raise ValueError(self.mode558)

    def moment_kl(self, r, vr, vt):
        if self.last_s2 is None:
            return None
        inside = r < self.c["rta"]
        k = np.clip(np.searchsorted(self.rf, r[inside]) - 1, 0, NB - 1)
        n = np.bincount(k, minlength=NB)
        ssum = np.bincount(k, weights=(vr[inside] ** 2 + vt[inside] ** 2) / 3, minlength=NB)
        ok = (n >= 20) & (self.last_s2 > 0)
        s = ssum[ok] / n[ok]; t = self.last_s2[ok]; x = s / t
        return float(np.sum(self.m * n[ok] * 1.5 * (x - 1 - np.log(x))))


def tensor_jeans_resid(toy, r, vr, L):
    """median |resid| over shells 0.1-0.9 r_*: tensor [P_r' + 2(P_r - P_t)/r + rho g]/(rho g) and scalar [(trP/3)' + rho g]/(rho g)."""
    c = toy.c; vt = L / r
    be = np.geomspace(0.1, 0.9, 13); rcb = np.sqrt(be[1:] * be[:-1]); Vb = 4 * math.pi / 3 * np.diff(be ** 3)
    idx = np.digitize(r, be) - 1
    Pr = np.zeros(12); Pt = np.zeros(12); rho = np.zeros(12)
    for i in range(12):
        mk = idx == i
        rho[i] = toy.m * mk.sum() / Vb[i]
        Pr[i] = rho[i] * np.mean(vr[mk] ** 2); Pt[i] = rho[i] * np.mean(vt[mk] ** 2) / 2
    Menc = Mb_enc(c, rcb) + toy.m * np.searchsorted(np.sort(r), rcb)
    g = Menc * rcb / (rcb ** 2 + EPS ** 2) ** 1.5
    lr = np.log(rcb)
    dPr = np.gradient(Pr, lr) / rcb; dPs = np.gradient((Pr + 2 * Pt) / 3, lr) / rcb
    rt = (dPr + 2 * (Pr - Pt) / rcb + rho * g) / (rho * g)
    rs = (dPs + rho * g) / (rho * g)
    beta = 1 - Pt / Pr
    return dict(tensor_median_abs=float(np.median(np.abs(rt[1:-1]))), scalar_median_abs=float(np.median(np.abs(rs[1:-1]))),
                beta_bins=beta.tolist(), beta_median=float(np.median(beta)))


# ================================================================================================ run
def t90_of(series, key):
    x0 = series[0][key]; xe = series[-1][key]
    if abs(x0 - xe) < 0.05:
        return None
    tol = 0.1 * abs(x0 - xe); t = None
    for s in reversed(series):
        if abs(s[key] - xe) <= tol:
            t = s["t"]
        else:
            break
    return t


def gate_at(series, t, cellkey, thr=0.05, end_thr=0.05):
    s = min(series, key=lambda q: abs(q["t"] - t))
    ref = min(series, key=lambda q: abs(q["t"] - (s["t"] - 2.0)))
    e = math.log(s["r99"] / RES_CELLS[cellkey]["r99_analytic"])
    out = dict(t=s["t"], logXJ=s["logXJ"], D=s["D"], dlogXJ_2=s["logXJ"] - ref["logXJ"], dD_2=s["D"] - ref["D"], edge=e,
               sink=s["sink"], r99=s["r99"])
    out["end_ok"] = bool(abs(s["logXJ"]) <= end_thr and abs(s["D"]) <= end_thr)
    out["steady_ok"] = bool(abs(out["dlogXJ_2"]) <= thr and abs(out["dD_2"]) <= thr)
    out["edge_ok"] = bool(-0.1 <= e <= C2_544[cellkey] + 0.1)
    out["pass"] = out["end_ok"] and out["steady_ok"] and out["edge_ok"]
    return out


RES_CELLS = {}


def run(job):
    c, name, ic, mode, T_Gyr = job["c"], job["name"], job["ic"], job["mode"], job["T"]
    T544.ALPHA = job.get("alpha", 1.0)
    rng = np.random.default_rng(T544.SEED)
    r, vr, L, m = T544.make_ic(c, ic, rng, inject=job.get("inject", False))
    toy = Toy558(c, mode); toy.m = m
    n0 = r.size
    dt = c["dt"]; nsteps = int(round(T_Gyr / (dt * c["tu_Gyr"])))
    every = max(1, int(round(0.25 / (dt * c["tu_Gyr"]))))
    K0, W0 = toy.energy(r, vr, L)
    W_drift = 0.0; W_ou = 0.0; W_ou_pos = 0.0
    snaps = []; t0 = time.time(); blow = False; kl = []
    for it in range(nsteps + 1):
        if it % every == 0 or it == nsteps:
            dg = toy.diag554(r, vr, L); K, W = toy.energy(r, vr, L)
            dg.update(t_Gyr=it * dt * c["tu_Gyr"], E=K + W, sink_cum=-(W_drift + W_ou) / c["Mcat"],
                      relax_in_gross=W_ou_pos / c["Mcat"], integ_err=(K + W - K0 - W0 - W_drift - W_ou) / abs(K0 + W0))
            snaps.append(dg)
            if dg["relax_in_gross"] > 10.0 or dg["vmax"] > 50.0:
                blow = True
        if it == nsteps: break
        r, vr, ns = T544.vlasov_step(toy, r, vr, L, dt)
        if toy.drift:
            vt = L / r
            g, _ = toy.gravity(r)
            _, Wb = toy.energy(r, vr, L)
            rn, _w = toy.drift_step(r, dt, g)
            Ln = rn * vt
            _, Wa = toy.energy(rn, vr, Ln)
            W_drift += Wa - Wb
            L = Ln; r = rn
            snap_next = ((it + 1) % every == 0)
            vr_old, vt_old = vr, vt
            vr, vt, dk = toy.vel_step(r, vr, vt, dt, g, rng)
            if snap_next and mode in ("v3", "fix2"):
                kb = toy.moment_kl(r, vr_old, vt_old); ka = toy.moment_kl(r, vr, vt)
                if kb is not None:
                    kl.append((kb, ka))
            W_ou += dk; W_ou_pos += max(dk, 0.0); L = r * vt
    fin = snaps[-1]
    series = [dict(t=s["t_Gyr"], logX=s["logX"], logXJ=s["logXJ"], D=s["D"], r99=s["r99"], sink=s["sink_cum"], F=s["F"],
                   beta=s["beta"], excess_in_rstar=s["excess_in_rstar"]) for s in snaps]
    res = dict(name=name, sys=c["sys"], foot=c["foot"], ic=ic, mode=mode, alpha=T544.ALPHA, T_Gyr=T_Gyr, steps=nsteps,
               n_particles=n0, mass_exact=bool(r.size == n0), final=fin, series=series, wall_s=time.time() - t0,
               integ_err_maxabs=float(max(abs(s["integ_err"]) for s in snaps)), blow_up=bool(blow),
               vmax_code=float(max(s["vmax"] for s in snaps)), relax_in_gross_max=float(max(s["relax_in_gross"] for s in snaps)),
               n_guard=toy.n_guard, overfilled_bin_frac=(toy.n_over_bins / toy.n_bins_occ) if toy.n_bins_occ else None,
               solver_fail_frac=(toy.n_fail / toy.n_solve) if toy.n_solve else None)
    if kl:
        res["kl_steps"] = len(kl); res["kl_decrease_frac"] = float(np.mean([a < b for b, a in kl]))
        res["kl_mean_before"] = float(np.mean([b for b, a in kl])); res["kl_mean_after"] = float(np.mean([a for b, a in kl]))
    if mode != "none":
        res["tensor_jeans_final"] = tensor_jeans_resid(toy, r, vr, L)
    return res


# ================================================================================================ sympy
def sympy_items():
    R = {}
    v = sp.Matrix(sp.symbols("v1:4", real=True))
    k1, k2, k3 = sp.symbols("k1:4", real=True)
    K = sp.Matrix([[0, -k3, k2], [k3, 0, -k1], [-k2, k1, 0]])
    Rot = (sp.eye(3) - K).inv() * (sp.eye(3) + K)                       # Cayley: general rotation
    R["I1_cayley_orthogonal"] = bool(sp.simplify(Rot.T * Rot - sp.eye(3)) == sp.zeros(3, 3))
    Phi = sp.Symbol("Phi"); f = sp.Function("f")
    dE = lambda w: (w.T * w)[0] / 2 + Phi
    R["I1_dE_invariant"] = bool(sp.simplify(dE(Rot * v) - dE(v)) == 0)
    R["I1_dSB_invariant_for_isotropic_f"] = "delta S_B/delta f = -ln f - 1: a function of f only, so invariant whenever f(Rv) = f(v)"
    vi, vj = sp.Matrix(sp.symbols("a1:4", real=True)), sp.Matrix(sp.symbols("b1:4", real=True))
    wE = dE(vj) - dE(vi)
    R["I1_pair_energy_weight_invariant"] = bool(sp.simplify(dE(Rot * vj) - dE(Rot * vi) - wE) == 0)
    R["I1_position_block_v_independent"] = "delta(-F/Theta)/delta f = -psi(x)/Theta (round psi, CFG541/542): no v dependence"
    # pair weight through the trace only: Delta(v^2/2) = (1/2) Delta tr(v v^T)
    R["I1_pair_couples_to_trace"] = bool(sp.simplify(wE - ((vj * vj.T).trace() - (vi * vi.T).trace()) / 2) == 0)
    # I2
    A = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"A{min(i, j)}{max(i, j)}"))
    Lg = [sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]]), sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]]),
          sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])]
    eqs = []
    for G in Lg:
        eqs += list(G * A - A * G)
    sol = sp.solve(eqs, list(A.free_symbols), dict=True)
    Asol = A.subs(sol[0]) if sol else None
    R["I2_invariant_A"] = str(Asol)
    R["I2_A_is_multiple_of_identity"] = bool(Asol is not None and sp.simplify(Asol - Asol[0, 0] * sp.eye(3)) == sp.zeros(3, 3))
    # I3
    c1, c2, c3, lm, Tt = sp.symbols("c1 c2 c3 lam T", positive=True)
    Sg = sp.log(c1 * c2 * c3) / 2 - lm * (c1 + c2 + c3 - 3 * Tt)
    s3 = sp.solve([sp.diff(Sg, x) for x in (c1, c2, c3, lm)], [c1, c2, c3, lm], dict=True)
    R["I3_maximiser"] = str(s3)
    R["I3_isotropic"] = bool(len(s3) == 1 and s3[0][c1] == Tt and s3[0][c2] == Tt and s3[0][c3] == Tt)
    # I4
    eta, w = sp.symbols("eta w", positive=True)
    left = sp.integrate(sp.exp(-eta * w), (w, 0, sp.oo)); right = sp.integrate(sp.exp(eta * w), (w, 0, sp.oo))
    zero = sp.integrate(sp.Integer(1), (w, 0, sp.oo))
    R["I4_half_line_integrals"] = [str(left), str(right), str(zero)]
    R["I4_not_normalisable"] = bool(right == sp.oo and zero == sp.oo)
    R["I4_note"] = ("max S_B at fixed rho and fixed tangential momentum, no energy multiplier (the zero-entropy partner takes the "
                    "energy, CFG550 b1): f = exp(-1 - mu - eta.v_t) diverges along -eta (and for eta = 0). The dissipative "
                    "bracket alone fixes no temperature profile; the profile must come from the reversible flow L.")
    # I5
    rs = sp.symbols("r", positive=True); lf = sp.Function("l")
    X, Y, Z = sp.symbols("X Y Z", real=True); rr = sp.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    lam_vec = [lf(rr) * q / rr for q in (X, Y, Z)]
    Jm = sp.Matrix(3, 3, lambda i, j: sp.diff(lam_vec[i], (X, Y, Z)[j]))
    Jx = sp.simplify(((Jm + Jm.T) / 2).subs({Y: 0, Z: 0}).subs(X, rs))
    R["I5_sym_grad_lambda_diag"] = [str(sp.simplify(Jx[0, 0])), str(sp.simplify(Jx[1, 1])), str(sp.simplify(Jx[2, 2]))]
    lsol = sp.dsolve(sp.Eq(sp.simplify(Jx[0, 0]), sp.simplify(Jx[1, 1])), lf(rs))
    R["I5_isotropy_condition_solution"] = str(lsol)
    R["I5_invariant_iff_isothermal"] = bool(sp.diff(sp.simplify(-1 / (2 * sp.diff(lsol.rhs, rs))), rs) == 0)
    R["Q1_I_all_pass"] = bool(R["I1_cayley_orthogonal"] and R["I1_dE_invariant"] and R["I1_pair_energy_weight_invariant"]
                              and R["I1_pair_couples_to_trace"] and R["I2_A_is_multiple_of_identity"] and R["I3_isotropic"]
                              and R["I4_not_normalisable"] and R["I5_invariant_iff_isothermal"])
    R["Q1_structural_refutation_of_tensor"] = False
    R["Q1_structural_note"] = (
        "No committed element excludes the tensor constraint: (1) CFG550/554: M of the velocity block is symmetric PSD with "
        "M dE = 0 and dS >= 0 for ANY reference measure, anisotropic included (S2); (2) the round rule (CFG516/541) acts on "
        "the position block (shell-averaged rho_c, radial psi); in spherical symmetry the tensor constraint is itself a single "
        "radial condition built from shell quantities, so roundness does not discriminate; (3) G9 is satisfied by both "
        "(Phi of real mass); (4) the tensor moment d_t(rho u)|_Vlasov = -J is the exact first moment of the reversible part L "
        "of Pb, so it is the framework's own stationarity statement. I1-I5 show: the bracket is SO(3)_v-equivariant, it can "
        "only impose trace (isotropic) linear constraints, and alone it fixes no temperature at all (I4). The temperature "
        "profile must therefore be imported from L, and importing the full tensor (route a) or its SO(3)_v average (the "
        "scalar constraint) is a choice. The scalar target is the maximiser under the single principle 'the target of an "
        "SO(3)_v-equivariant dissipative bracket uses only SO(3)_v-invariant constraints' (equivalently: the rotation average "
        "<R Pi R^T> = tr Pi/3 I of L's stationarity), which is not implied by Pb's GENERIC conditions.")
    # S2': nonlocal state-dependent reference
    T0, Th = sp.symbols("T0 Theta", positive=True)
    vs = [sp.Rational(1, 3), sp.Rational(-1, 2), 2]
    fa = sp.symbols("fa0:3", positive=True); fb = sp.symbols("fb0:3", positive=True)
    ra, rb = sum(fa), sum(fb)
    sa = 1 + ra ** 2 + rb / 3; sb = 1 + rb + ra ** 2 / 5                     # nonlocal s(rho_a, rho_b)
    pa = [sp.exp(-vv ** 2 / (2 * sa)) for vv in vs]; pb = [sp.exp(-vv ** 2 / (2 * sb)) for vv in vs]
    Za, Zb = sum(pa), sum(pb)
    S = -(T0 / Th) * (sum(fa[i] * sp.log(fa[i] / (ra * pa[i] / Za)) for i in range(3)) +
                      sum(fb[i] * sp.log(fb[i] / (rb * pb[i] / Zb)) for i in range(3)))
    naive = [-(T0 / Th) * (sp.log(fa[i] / (ra * pa[i] / Za)) + 1) for i in range(3)]
    extra = [sp.diff(S, fa[i]) - naive[i] for i in range(3)]
    ra0, rb0 = sp.Rational(7, 5), sp.Rational(3, 4)
    sa0 = sa.subs({fa[0]: ra0, fa[1]: 0, fa[2]: 0, fb[0]: rb0, fb[1]: 0, fb[2]: 0})
    sb0 = sb.subs({fa[0]: ra0, fa[1]: 0, fa[2]: 0, fb[0]: rb0, fb[1]: 0, fb[2]: 0})
    pa0 = [sp.exp(-vv ** 2 / (2 * sa0)) for vv in vs]; pb0 = [sp.exp(-vv ** 2 / (2 * sb0)) for vv in vs]
    st = {**{fa[i]: ra0 * pa0[i] / sum(pa0) for i in range(3)}, **{fb[i]: rb0 * pb0[i] / sum(pb0) for i in range(3)}, T0: 1, Th: 1}
    ex_eq = [sp.N(e.subs(st), 30) for e in extra]
    off = {**{fa[i]: sp.Rational(i + 2, 7) for i in range(3)}, **{fb[i]: sp.Rational(5 - i, 9) for i in range(3)}, T0: 1, Th: 1}
    ex_off = [sp.N(e.subs(off), 30) for e in extra]
    R["S2p_extra_at_equilibrium"] = [float(x) for x in ex_eq]
    R["S2p_extra_off_equilibrium"] = [float(x) for x in ex_off]
    R["S2p_v_independent_off_equilibrium"] = bool(abs(ex_off[0] - ex_off[1]) < 1e-25 and abs(ex_off[1] - ex_off[2]) < 1e-25)
    R["S2p_equals_T0_over_Theta_at_equilibrium"] = bool(all(abs(x - 1) < 1e-25 for x in ex_eq))
    R["S2p_pass"] = bool(R["S2p_v_independent_off_equilibrium"] and R["S2p_equals_T0_over_Theta_at_equilibrium"])
    # Lyapunov (as CFG554)
    lamb, Aa, Bb, Cc, al = sp.symbols("lambda A B C alpha", positive=True)
    dL = lamb * Aa - al * (Bb + lamb ** 2 * Cc)
    mx = sp.simplify(dL.subs(lamb, sp.solve(sp.diff(dL, lamb), lamb)[0]))
    R["L_max_rate"] = str(mx); R["L_positive_if_alpha_below"] = str(sp.solve(sp.Eq(mx, 0), al))
    R["L_note"] = ("V3 changes only the reference; every candidate (F, F + KL to a rho-dependent target, E_N + Casimirs) still "
                   "has a Vlasov rate first order in the bulk velocity against O(alpha) dissipation (CFG554 section 4)")
    R["L_full_system"] = "NOT ESTABLISHED"
    return R


def control_c8(c):
    toy = T544.Toy(c, "two");
    mc = toy.rhoph * toy.V * (toy.rc <= 1.0)
    rho = mc / toy.V
    s2v, _, _, _ = v3_target(c, toy.rf, toy.rc, toy.dr, mc, rho, toy.rhoph, cap=True)
    s2f, _, _, _ = v3_target(c, toy.rf, toy.rc, toy.dr, mc, rho, toy.rhoph, cap=False)
    occ = rho > 0
    return float(np.max(np.abs(s2v[occ] - s2f[occ]) / np.maximum(s2f[occ], 1e-300)))


# ================================================================================================ main
def main():
    cells = {f"{s}_{f}": T544.make_cell(s, f) for s in T544.SYS for f in T544.FOOT}
    keys = list(cells)
    RES["cells"] = {}
    for k, c in cells.items():
        RES["cells"][k] = dict(Vf_kms=c["Vf_kms"], rstar_kpc=c["rstar_kpc"], Mcat=c["Mcat"], tu_Gyr=c["tu_Gyr"],
                               r99_analytic=T544.r99_analytic(c),
                               CFG541_dW_over_Vf2=J541["one_d"][c["foot"]][c["sys"]]["dW_per_mass"] / c["Vf2_SI"])
    RES_CELLS.update(RES["cells"])
    log("CFG558 velocity part: isotropy, overfill, alpha-robustness" + (" [MUTATE]" if MUT else ""))
    for k in keys:
        log(f"{k}: {RES['cells'][k]}")
    if not MUT:
        t0 = time.time(); RES["sympy"] = sympy_items()
        log(f"\nSympy ({time.time() - t0:.0f}s):")
        for kk, vv in RES["sympy"].items():
            log(f"  {kk}: {vv}")
        RES["C8"] = {k: control_c8(c) for k, c in cells.items()}
        log(f"C8 max rel |sigma_*^2 - sigma_J^2| on rho_c = rho_ph: {RES['C8']}")
        RES["ang_mom_test"] = T554.ang_mom_test(); log(f"Angular momentum (CFG554 test re-run): {RES['ang_mom_test']}")

    jobs = []
    for k, c in cells.items():
        if not MUT:
            jobs += [dict(c=c, name=f"{k}|C2_vlasov_eq", ic="E", mode="none", T=2.0),
                     dict(c=c, name=f"{k}|C5_capoff_C", ic="C", mode="fix2", T=5.0),
                     dict(c=c, name=f"{k}|v3_over_base", ic="E", mode="v3", T=5.0),
                     dict(c=c, name=f"{k}|v3_over_inj", ic="E", mode="v3", T=5.0, inject=True)]
            for al in (0.5, 1.0, 2.0):
                for ic in ("B", "C"):
                    jobs.append(dict(c=c, name=f"{k}|v3_{ic}_al{al}", ic=ic, mode="v3", T=15.0, alpha=al))
        else:
            jobs += [dict(c=c, name=f"{k}|MI_B", ic="B", mode="mi", T=10.0),
                     dict(c=c, name=f"{k}|MO_over_base", ic="E", mode="fix2", T=5.0),
                     dict(c=c, name=f"{k}|MO_over_inj", ic="E", mode="fix2", T=5.0, inject=True)]
            for ic in ("B", "C"):
                jobs.append(dict(c=c, name=f"{k}|v3_{ic}_al0.25", ic=ic, mode="v3", T=15.0, alpha=0.25))
    cost = lambda j: j["T"] / j["c"]["dt"] / j["c"]["tu_Gyr"] * (3.0 if j["mode"] == "mi" else 1.0)
    jobs.sort(key=lambda j: -cost(j))
    with Pool(NPROC, initializer=_init_cells, initargs=(RES["cells"],)) as pool:
        out = pool.map(run, jobs, chunksize=1)
    runs = {o["name"]: o for o in out}
    RES["runs"] = runs
    log("\nRuns (end state):")
    for nm in sorted(runs):
        o = runs[nm]; f = o["final"]
        log(f"  {nm:30s} {o['T_Gyr']:4.1f} Gyr a={o['alpha']} logXJ {f['logXJ']:+.3f} D {f['D']:+.3f} r99 {f['r99']:.3f} beta {f['beta']:+.2f}"
            f" sink {f['sink_cum']:+.3f} integ {o['integ_err_maxabs']:.1e} vmax {o['vmax_code']:.2f} blow {o['blow_up']}"
            f" guard {o['n_guard']} overbins {o['overfilled_bin_frac']} fail {o['solver_fail_frac']}"
            f" KLdec {o.get('kl_decrease_frac')} ({o['wall_s']:.0f}s)")

    def P_of(base, inj, k):
        Mi = (inj["n_particles"] - base["n_particles"]) * cells[k]["Mcat"] / NPART
        return (inj["final"]["excess_in_rstar"] - base["final"]["excess_in_rstar"]) / Mi

    if MUT:
        mi = {}
        for k in keys:
            o = runs[f"{k}|MI_B"]; s = o["series"]
            g = gate_at(s, 10.0, k, thr=0.05, end_thr=0.1)
            mi[k] = dict(G550_pass=bool(g["end_ok"] and g["steady_ok"]), logXJ=g["logXJ"], D=g["D"], edge=g["edge"],
                         energy_net=g["sink"], solver_fail_frac=o["solver_fail_frac"], blow_up=o["blow_up"])
        mo = {k: P_of(runs[f"{k}|MO_over_base"], runs[f"{k}|MO_over_inj"], k) for k in keys}
        a25 = {}
        for k in keys:
            for ic in ("B", "C"):
                o = runs[f"{k}|v3_{ic}_al0.25"]; s = o["series"]
                a25[f"{k}|{ic}"] = dict(gate_13p8=gate_at(s, T_AGE, k), gate_15=gate_at(s, 15.0, k),
                                        t90=_t90(s), t_band=_tband(s), blow_up=o["blow_up"])
        bite = dict(MI=bool(all(not mi[k]["G550_pass"] for k in keys if k.startswith("cluster"))),
                    MO=bool(all(v > 0.2 for v in mo.values())))
        RES["mutate"] = dict(MI=mi, MO_P=mo, alpha_0p25=a25, bite=bite)
        log(f"\nMUTATE MI (tensor target on rho_hat, IC-B 10 Gyr): {mi}")
        log(f"MUTATE MO (overfill rule removed) P: {mo}")
        log("alpha x 0.25 (reported): " + "; ".join(f"{kk}: pass13.8 {v['gate_13p8']['pass']} logXJ {v['gate_13p8']['logXJ']:+.3f} D {v['gate_13p8']['D']:+.3f} "
                                                  f"dXJ/dD {v['gate_13p8']['dlogXJ_2']:+.3f}/{v['gate_13p8']['dD_2']:+.3f} edge {v['gate_13p8']['edge']:+.3f} t90 {v['t90']} tband {v['t_band']}"
                                                  for kk, v in a25.items()))
        log(f"bite {bite}")
        return 1 if all(bite.values()) else 0

    # controls
    c2 = {k: bool(abs(runs[f"{k}|C2_vlasov_eq"]["final"]["logX"]) <= 0.1 and abs(runs[f"{k}|C2_vlasov_eq"]["final"]["D"]) <= 0.1) for k in keys}
    c5 = {}
    for k in keys:
        a = runs[f"{k}|C5_capoff_C"]["final"]; b = J544["runs"][f"{k}|fix2_C"]["final"]
        c5[k] = dict(dlogX=abs(a["logX"] - b["logX"]), dD=abs(a["D"] - b["D"]), ok=bool(abs(a["logX"] - b["logX"]) <= 1e-6 and abs(a["D"] - b["D"]) <= 1e-6))
    c8 = all(v <= 1e-12 for v in RES["C8"].values())
    mass = all(o["mass_exact"] for o in runs.values())
    ctrl = all(c2.values()) and all(v["ok"] for v in c5.values()) and c8 and mass
    RES["controls"] = dict(C2=c2, C5=c5, C8=c8, mass_exact=mass, all_pass=ctrl)
    log(f"\nControls: C2 {c2}; C5 {c5}; C8 {c8}; mass {mass} -> {'PASS' if ctrl else 'FAIL'}")

    sy = RES["sympy"]
    # Q2
    P = {k: P_of(runs[f"{k}|v3_over_base"], runs[f"{k}|v3_over_inj"], k) for k in keys}
    g550 = {}; edge = {}; en = {}
    for k in keys:
        sB = runs[f"{k}|v3_B_al1.0"]["series"]; sC = runs[f"{k}|v3_C_al1.0"]["series"]
        gB = gate_at(sB, 10.0, k, thr=0.05, end_thr=0.1); gC = gate_at(sC, 5.0, k, thr=0.05, end_thr=0.1)
        g550[k] = dict(B=bool(gB["end_ok"] and gB["steady_ok"]), C=bool(gC["end_ok"] and gC["steady_ok"]), B_detail=gB, C_detail=gC)
        edge[k] = dict(B=gB["edge"], C=gC["edge"], ok=bool(gB["edge_ok"] and gC["edge_ok"]))
        en[k] = dict(B_net_10=gB["sink"], C_net_5=gC["sink"], C_whole_history=RES["cells"][k]["CFG541_dW_over_Vf2"] + gC["sink"])
        en[k]["ok"] = bool(0 <= en[k]["B_net_10"] <= 1.0 and 0 <= en[k]["C_whole_history"] <= 1.0)
    over_ok = all(v <= 0.2 for v in P.values())
    gate1 = all(v["B"] and v["C"] for v in g550.values()); edge_ok = all(v["edge_ok"] if "edge_ok" in v else v["ok"] for v in edge.values())
    en_ok = all(v["ok"] for v in en.values())
    v3runs = [o for nm, o in runs.items() if o["mode"] == "v3"]
    blow = {o["name"]: True for o in v3runs if o["blow_up"]}
    guard_total = int(sum(o["n_guard"] for o in v3runs))
    reasons = [n for n, okk in (("P > 0.2", over_ok), ("G550 at alpha = 1", gate1), ("edge", edge_ok), ("energy", en_ok),
                                 ("blow-up", not blow)) if not okk]
    overfill = "HANDLED" if not reasons else "NOT HANDLED (" + ", ".join(reasons) + ")"
    RES["Q2"] = dict(P=P, G550_alpha1=g550, edge=edge, energy=en, blow_ups=blow, guard_steps_total=guard_total, label=overfill)
    log(f"\nQ2 overfill P {P}\n  G550 a=1 {{k: (B, C)}} {{{', '.join(f'{k}: ({v['B']}, {v['C']})' for k, v in g550.items())}}}\n  edge {edge}\n  energy {en}\n  -> OVERFILL {overfill}")
    # Q3
    q3 = {}; fails = []
    for k in keys:
        for al in (0.5, 1.0, 2.0):
            for ic in ("B", "C"):
                o = runs[f"{k}|v3_{ic}_al{al}"]; s = o["series"]
                d = dict(gate_10=gate_at(s, 10.0, k), gate_13p8=gate_at(s, T_AGE, k), gate_15=gate_at(s, 15.0, k),
                         t90=_t90(s), t_band=_tband(s), blow_up=o["blow_up"], integ_err_maxabs=o["integ_err_maxabs"],
                         kl_decrease_frac=o.get("kl_decrease_frac"), tensor_jeans_final=o.get("tensor_jeans_final"))
                q3[f"{k}|{ic}|al{al}"] = d
                if not d["gate_13p8"]["pass"]:
                    fails.append(f"{k}|{ic}|al{al}")
    rob = "alpha-ROBUST (by the age)" if not fails else "NOT alpha-ROBUST"
    t90tab = {f"al{al}": {f"{k}|{ic}": q3[f"{k}|{ic}|al{al}"]["t90"] for k in keys for ic in ("B", "C")} for al in (0.5, 1.0, 2.0)}
    RES["Q3"] = dict(runs=q3, failing=fails, label=rob, t90=t90tab)
    log("\nQ3 (gate at 13.8 Gyr):")
    for kk, d in q3.items():
        g = d["gate_13p8"]
        log(f"  {kk:24s} pass {g['pass']} logXJ {g['logXJ']:+.3f} D {g['D']:+.3f} dXJ/dD(2 Gyr) {g['dlogXJ_2']:+.3f}/{g['dD_2']:+.3f} edge {g['edge']:+.3f}"
            f" | 10 Gyr pass {d['gate_10']['pass']} | 15 Gyr pass {d['gate_15']['pass']} | t90 {d['t90']} t_band {d['t_band']}")
    log(f"  -> {rob}; failing {fails}")
    # Q1
    t_iii = {f"{k}|{ic}": q3[f"{k}|{ic}|al1.0"]["tensor_jeans_final"] for k in keys for ic in ("B", "C")}
    iso_forced = bool(sy["Q1_I_all_pass"] and sy["Q1_structural_refutation_of_tensor"])
    iso = "ISOTROPY FORCED" if iso_forced else "ISOTROPY CHOSEN"
    RES["Q1"] = dict(I_all_pass=sy["Q1_I_all_pass"], structural_refutation=sy["Q1_structural_refutation_of_tensor"],
                     toy_iii_end_states=t_iii, label=iso)
    log(f"\nQ1 toy (iii) end states alpha = 1 (tensor / scalar Jeans residual medians, beta median): " +
        "; ".join(f"{kk}: {v['tensor_median_abs']:.3f} / {v['scalar_median_abs']:.3f}, beta {v['beta_median']:+.2f}" for kk, v in t_iii.items()))
    log(f"  -> {iso}")
    # checks
    angmom = bool(RES["ang_mom_test"]["pass"])
    lyap = sy["L_full_system"]
    kl_all = [o.get("kl_decrease_frac") for o in v3runs if o.get("kl_decrease_frac") is not None]
    integ_max = float(max(o["integ_err_maxabs"] for o in v3runs))
    RES["checks"] = dict(G9="target field = baryons + current cold energy (real mass); rho_ph only as the T1 comparison density",
                         energy_alpha1=en_ok, S2p=sy["S2p_pass"], kl_decrease_frac_min=min(kl_all) if kl_all else None,
                         kl_decrease_frac_mean=float(np.mean(kl_all)) if kl_all else None, lyapunov=lyap,
                         edge_alpha1=edge_ok, angular_momentum=angmom, blow_ups=blow, integ_err_max_v3=integ_max, mass_exact=mass)
    log(f"\nChecks: {RES['checks']}")
    # overall
    if not ctrl:
        overall = "NO LABEL (controls fail)"
    elif (not gate1) or blow or (not en_ok):
        overall = "INCONSISTENT"
    elif not iso_forced:
        overall = "POSITED"
    else:
        opn = [n for n, okk in (("overfill", over_ok), ("alpha robustness", not fails), ("edge", edge_ok),
                                ("angular momentum", angmom), ("Lyapunov", lyap == "ESTABLISHED")) if not okk]
        overall = "DERIVED" if not opn else "DERIVED WITH OPEN ITEMS (" + ", ".join(opn) + ")"
    RES["labels"] = dict(Q1=iso, Q2="OVERFILL " + overfill, Q3=rob, overall="VELOCITY PART " + overall, lyapunov=lyap)
    log(f"\nLABELS: {RES['labels']}")
    return 0 if ctrl else 1


def _t90(s):
    a = t90_of(s, "D"); b = t90_of(s, "logXJ")
    v = [x for x in (a, b) if x is not None]
    return dict(D=a, logXJ=b, t90=max(v) if v else None)


def _tband(s):
    t = None
    for q in reversed(s):
        if abs(q["D"]) <= 0.05 and abs(q["logXJ"]) <= 0.05:
            t = q["t"]
        else:
            break
    return t


def _init_cells(cells):
    RES_CELLS.update(cells)


if __name__ == "__main__":
    rc = main()
    with open(os.path.join(HERE, f"cfg558{TAG}.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    with open(os.path.join(HERE, f"cfg558_results{TAG}.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    sys.exit(rc)
