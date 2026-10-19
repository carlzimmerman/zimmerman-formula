#!/usr/bin/env python3
"""CFG848: maximum-entropy (non-degenerate Lynden-Bell) partition of tethered and free cold energy in the reciprocal
two-population functional of the 2026-10-18 analytic review (KINETIC_PARTITION.md). Criteria: FROZEN_CRITERIA.md, committed
alone in cf0aad80f before this script existed.

Units G = a0 = M_b = 1 (r_M = 1, V_f^2 = 1). Hernquist baryons M_b(r) = r^2/(r+a)^2, Phi_b = -1/(r+a).
Models:
  C   two labels t, f of one carrier, conversion allowed (chemical equilibrium), common beta   [PRIMARY]
  NC  tethered only, no conversion (K1 law limit; diagnostic)
  N1  one ordinary Newtonian species, no tether (MUTATE; K2 Antonov with baryons off)
Run:   nice -n 19 python3 cfg848_maxent.py                  -> cfg848.out, cfg848_results.json        (exit 0 iff K1-K3 pass)
       CFG848_MUTATE=1 nice -n 19 python3 cfg848_maxent.py  -> cfg848_MUTATE.out, cfg848_results_MUTATE.json (exit 1 iff it bites)
"""
import os, sys, json, math, time
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import root, brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG848_MUTATE", "0") == "1"
SFX = "_MUTATE" if MUT else ""
OUT = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


# ---------------------------------------------------------------- inputs (FROZEN_CRITERIA "Inputs")
G_SI, MSUN, MPC = 6.67430e-11, 1.98892e30, 3.0856776e22
A0 = {"can": 9.3603e-11, "alt": 1.1312e-10}
H0_SI = 67.4e3 / MPC
OM = 0.315
SUP = 5.364
FB = 1.0 / (1.0 + SUP)
DTA_FILE = os.path.join(HERE, "..", "CFG654_independent_inputs", "cfg654_delta_ta.json")
DTA = json.load(open(DTA_FILE))
assert abs(DTA["z"][0]) < 1e-12
DELTA_TA0 = DTA["D"][0]                       # 11.8308 (CFG654 N0)
RHO_M0 = OM * 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
SYSTEMS = {"P1": dict(logMb=6.5, a=3.0), "P2": dict(logMb=10.5, a=0.3)}


def r_ta_over_rM(logMb, N, foot):
    Mb = 10 ** logMb * MSUN
    Mta = N * Mb / FB
    rta = (3 * Mta / (4 * math.pi * DELTA_TA0 * RHO_M0)) ** (1 / 3)
    rM = math.sqrt(G_SI * Mb / A0[foot])
    return rta / rM


def R_fill(Mc, a):                            # r^2/(r+a) = Mc
    return 0.5 * (Mc + math.sqrt(Mc * Mc + 4 * Mc * a))


def M_law(r, a):
    return r * r / (r + a)


def r_g(a):                                   # g_bar = 1/(r+a)^2 = 0.01
    return 10.0 - a


# ---------------------------------------------------------------- energies of the reference states
def E_INF(Mc, R, a, model, mb=1.0):
    ib = R * R / 2 - a * R + a * a * math.log((R + a) / a) if mb else 0.0
    Ub = -mb * 3 * Mc / R ** 3 * ib
    if model in ("C", "NC"):                  # all tethered, at rest, uniform: self-gravity cancelled, cubic push
        return Ub + Mc ** 3 / (6 * R ** 3)
    return Ub - 0.6 * Mc * Mc / R             # N1: ordinary mass


def E_LAW(Mc, a):
    Rf = R_fill(Mc, a)
    Ub = quad(lambda r: -1.0 / (r + a) * (r * r + 2 * a * r) / (r + a) ** 2, 0, Rf, limit=400)[0]
    Uc = quad(lambda r: r * r / (r + a) ** 3 / 3.0, 0, Rf, limit=400)[0] + Mc ** 3 / (9 * Rf ** 3)
    return Ub + Uc


# ---------------------------------------------------------------- equilibrium integrator
class Model:
    """Isothermal extremum rho_i = exp(l_i - beta psi_i), psi_i(0) = 0, integrated in s = ln r."""

    def __init__(self, kind, Mc, R, a, mb=1.0):
        self.kind, self.Mc, self.R, self.a, self.mb = kind, Mc, R, a, mb
        self.rin = 1e-6 * min(a, 1.0) if mb else 1e-6 * R
        self.rhobar = 3 * Mc / (4 * math.pi * R ** 3)
        self.ns = 2 if kind == "C" else 1

    def Mb(self, r):
        return self.mb * r * r / (r + self.a) ** 2

    def rhs(self, s, y, beta, l):
        r = math.exp(s)
        mb = self.Mb(r)
        if self.kind == "C":
            Mt, Mf, pt, pf = y[0], y[1], y[2], y[3]
            et, ef = min(l[0] - beta * pt, 700.0), min(l[1] - beta * pf, 700.0)
            rt, rf = math.exp(et), math.exp(ef)
            dMt, dMf = 4 * math.pi * r ** 3 * rt, 4 * math.pi * r ** 3 * rf
            dpt = (mb + Mf) / r - Mt * Mt / r ** 3
            dpf = (mb + Mt + Mf) / r
            phib = -self.mb / (r + self.a)
            F = -0.5 * (Mf * Mf + 2 * Mt * Mf) / r ** 2 + Mt ** 3 / (3 * r ** 4)
            return [dMt, dMf, dpt, dpf, phib * (dMt + dMf), F * r]
        M, p = y[0], y[1]
        e = min(l[0] - beta * p, 700.0)
        rho = math.exp(e)
        dM = 4 * math.pi * r ** 3 * rho
        phib = -self.mb / (r + self.a) if self.mb else 0.0
        if self.kind == "NC":
            dp = mb / r - M * M / r ** 3
            F = M ** 3 / (3 * r ** 4)
        else:                                  # N1
            dp = (mb + M) / r
            F = -0.5 * M * M / r ** 2
        return [dM, dp, phib * dM, F * r]

    def y0(self, beta, l):
        r = self.rin
        c = r * r / (2 * self.a ** 2) * self.mb if self.mb else 0.0
        if self.kind == "C":
            rt, rf = math.exp(min(l[0], 700)), math.exp(min(l[1], 700))
            Mt, Mf = 4 * math.pi / 3 * rt * r ** 3, 4 * math.pi / 3 * rf * r ** 3
            return [Mt, Mf, c + 2 * math.pi / 3 * rf * r * r, c + 2 * math.pi / 3 * (rt + rf) * r * r, 0.0, 0.0]
        rho = math.exp(min(l[0], 700))
        M = 4 * math.pi / 3 * rho * r ** 3
        own = 0.0 if self.kind == "NC" else 2 * math.pi / 3 * rho * r * r
        return [M, c + own, 0.0, 0.0]

    def integrate(self, beta, l, dense=False):
        Mc = self.Mc

        def blow(s, y, *args):
            return (y[0] + (y[1] if self.kind == "C" else 0.0)) - 1e4 * Mc
        blow.terminal = True
        sol = solve_ivp(self.rhs, (math.log(self.rin), math.log(self.R)), self.y0(beta, l), method="LSODA",
                        args=(beta, l), rtol=1e-10, atol=1e-13, events=blow, dense_output=dense)
        return sol

    def summary(self, beta, l):
        try:
            sol = self.integrate(beta, l)
        except Exception:
            return dict(ok=False, Mtot=-1.0, chem=0.0, E=float("nan"), U=float("nan"), beta=beta, l=list(l))
        y = sol.y[:, -1]
        ok = sol.status == 0 and bool(np.all(np.isfinite(y)))
        R, a = self.R, self.a
        phibR = -self.mb / (R + a) if self.mb else 0.0
        if self.kind == "C":
            T, F, pt, pf, Ub, Uf = y
            Phit0 = (phibR - F / R + T * T / (3 * R ** 3)) - pt
            Phif0 = (phibR - (T + F) / R) - pf
            U = Ub + Uf - 0.5 * (F * F + 2 * T * F) / R + T ** 3 / (9 * R ** 3)
            Mtot = T + F
            chem = (l[0] + beta * Phit0) - (l[1] + beta * Phif0)
        else:
            M, p, Ub, Uf = y
            Mtot = M
            chem = 0.0
            U = Ub + Uf + (M ** 3 / (9 * R ** 3) if self.kind == "NC" else -0.5 * M * M / R)
        E = 1.5 * Mtot / beta + U
        return dict(ok=ok, Mtot=Mtot, chem=chem, E=E, U=U, beta=beta, l=list(l))

    # unknowns: C -> (ln beta, l_t) at fixed l_f ; NC/N1 -> (ln beta) at fixed l
    def solve_at(self, p, guess):
        lfix = p + math.log(self.rhobar)

        def res(x):
            beta = math.exp(x[0])
            l = [x[1], lfix] if self.kind == "C" else [lfix]
            sm = self.summary(beta, l)
            if not sm["ok"] or sm["Mtot"] <= 0:
                return [50.0] * len(x)
            r1 = math.log(sm["Mtot"] / self.Mc)
            return [r1, sm["chem"]] if self.kind == "C" else [r1]

        for meth in ("hybr", "lm"):
            sol = root(res, guess, method=meth, options={"xtol": 1e-12} if meth == "hybr" else {"xtol": 1e-12, "ftol": 1e-13})
            if sol.success and max(abs(v) for v in res(sol.x)) < 1e-8:
                x = sol.x
                beta = math.exp(x[0])
                l = [x[1], lfix] if self.kind == "C" else [lfix]
                sm = self.summary(beta, l)
                sm["p"], sm["x"] = p, list(x)
                return sm
        return None

    def _unpack(self, z):
        p, beta = z[0], math.exp(z[1])
        lfix = p + math.log(self.rhobar)
        l = [z[2], lfix] if self.kind == "C" else [lfix]
        return beta, l

    def res_z(self, z):
        if not np.all(np.isfinite(z)) or abs(z[1]) > 30 or z[0] > 80 or (self.kind == "C" and abs(z[2]) > 600):
            return [50.0] * (len(z) - 1)
        beta, l = self._unpack(z)
        sm = self.summary(beta, l)
        if not sm["ok"] or sm["Mtot"] <= 0:
            return [50.0] * (len(z) - 1)
        r1 = math.log(sm["Mtot"] / self.Mc)
        return [r1, sm["chem"]] if self.kind == "C" else [r1]

    def state_z(self, z):
        beta, l = self._unpack(z)
        sm = self.summary(beta, l)
        sm["p"], sm["x"] = float(z[0]), [float(v) for v in z[1:]]
        return sm

    def hot_start(self):
        """Solve at a weak-coupling beta for the central log densities; returns the first series point."""
        beta0 = 1e-3 / (self.Mc / self.R + (1.0 / self.a if self.mb else 0.0))
        if self.kind == "C":
            def res(x):
                sm = self.summary(beta0, [x[0], x[1]])
                if not sm["ok"]:
                    return [50.0, 50.0]
                return [math.log(sm["Mtot"] / self.Mc), sm["chem"]]
            g = [math.log(self.rhobar / 2)] * 2
            sol = root(res, g, method="hybr", options={"xtol": 1e-13})
            p = sol.x[1] - math.log(self.rhobar)
            return p, [math.log(beta0), sol.x[0]]
        p = 1e-4
        return p, [math.log(beta0)]


def series(m, E_targets, p_max=60.0, beta_min_stop=None, label="", time_cap=1500.0):
    """Pseudo-arclength continuation of the extremum series from the hot end in z = (p, ln beta[, l_t]).
    Returns the points, the first turning point of E (microcanonical stability loss, refined) and the stable-branch states
    at each E_target (or None)."""
    p0, x0 = m.hot_start()
    s0 = m.solve_at(p0, x0)
    if s0 is None:
        return dict(points=[], turn=None, states={k: None for k in E_targets}, status="hot start failed")
    s1 = m.solve_at(p0 + 0.02, s0["x"])
    if s1 is None:
        return dict(points=[s0], turn=None, states={k: None for k in E_targets}, status="second point failed")
    Z = lambda s: np.array([s["p"]] + list(s["x"]))
    pts = [s0, s1]
    t = Z(s1) - Z(s0)
    t /= np.linalg.norm(t)
    ds, turn, status = 0.02, None, "p_max"
    t_start = time.time()

    def corrector(zb, tb, sig, guess=None):
        zp = zb + sig * tb if guess is None else guess

        def F(z):
            r = m.res_z(z)
            return list(r) + [float(np.dot(z - zb, tb) - sig)]
        sol = root(F, zp, method="hybr", options={"xtol": 1e-12})
        if not sol.success:
            sol = root(F, zp, method="lm", options={"xtol": 1e-12, "ftol": 1e-14})
        if not sol.success or max(abs(v) for v in F(sol.x)) > 1e-8:
            return None
        sm = m.state_z(sol.x)
        return sm

    while True:
        zb = Z(pts[-1])
        sm = corrector(zb, t, ds)
        if sm is None:
            ds *= 0.5
            if ds < 1e-7:
                status = "solver failure at p=%.4f beta=%.4g" % (pts[-1]["p"], pts[-1]["beta"])
                break
            continue
        if sm["E"] > pts[-1]["E"] and turn is None:
            # E rises: refine the minimum of E along the arc from the previous point
            zb2 = Z(pts[-2])
            t2 = Z(pts[-1]) - zb2
            L = np.linalg.norm(t2) + ds
            t2 = t2 / np.linalg.norm(t2)
            from scipy.optimize import minimize_scalar
            cache = {}

            def Es(sig):
                s2 = corrector(zb2, t2, sig)
                cache[sig] = s2
                return s2["E"] if s2 else float("inf")
            mr = minimize_scalar(Es, bounds=(0.0, L), method="bounded", options={"xatol": 1e-9})
            tp = cache.get(mr.x) or corrector(zb2, t2, mr.x)
            if tp is None or tp["E"] > pts[-1]["E"]:
                tp = pts[-1]
            if tp is not pts[-1]:
                if np.dot(Z(tp) - zb2, t2) < np.dot(Z(pts[-1]) - zb2, t2):
                    pts = pts[:-1] + [tp]          # the last point was already past the minimum
                else:
                    pts = pts + [tp]
            turn = tp
            pts.append(sm)
            status = "turning point"
            break
        tn = Z(sm) - zb
        tn /= np.linalg.norm(tn)
        if np.dot(tn, t) < 0:          # never reverse along the curve
            ds *= 0.5
            continue
        t = tn
        pts.append(sm)
        ds = min(ds * 1.3, 0.25)
        if sm["p"] > p_max:
            status = "p_max"
            break
        if beta_min_stop is not None and sm["beta"] >= beta_min_stop:
            status = "beta target reached"
            break
        if time.time() - t_start > time_cap:
            status = "time cap"
            break
    stable = pts if turn is None else pts[:pts.index(turn) + 1]
    states = {}
    for k, Et in E_targets.items():
        st = None
        for i in range(1, len(stable)):
            E1, E2 = stable[i - 1]["E"], stable[i]["E"]
            if (E1 - Et) * (E2 - Et) <= 0:
                zb = Z(stable[i - 1])
                tb = Z(stable[i]) - zb
                L = np.linalg.norm(tb)
                tb = tb / L

                def f(sig):
                    s2 = corrector(zb, tb, sig)
                    return (s2["E"] if s2 else float("nan")) - Et
                try:
                    sr = brentq(f, 0.0, L, xtol=1e-11)
                    st = corrector(zb, tb, sr)
                except Exception:
                    st = None
                break
        states[k] = st
    return dict(points=pts, turn=turn, states=states, status=status)


def profile(m, st, radii):
    """Masses, local free fraction and Delta at the requested radii for a solved state."""
    beta, l = st["beta"], st["l"]
    sol = m.integrate(beta, l, dense=True)
    out = {}
    for name, r in radii.items():
        r = min(max(r, m.rin * 10), m.R)
        y = sol.sol(math.log(r))
        mb = m.Mb(r)
        if m.kind == "C":
            Mt, Mf = y[0], y[1]
            rt, rf = math.exp(min(l[0] - beta * y[2], 700)), math.exp(min(l[1] - beta * y[3], 700))
            ffree = rf / (rt + rf)
            Fenc = Mf / (Mt + Mf)
        else:
            Mt, Mf = (y[0], 0.0) if m.kind == "NC" else (0.0, y[0])
            ffree = 0.0 if m.kind == "NC" else 1.0
            Fenc = ffree
        Mc = Mt + Mf
        D = math.log10((mb + Mc) / (mb + M_law(r, m.a))) if m.mb else float("nan")
        out[name] = dict(r=r, Mt=Mt, Mf=Mf, M_law=M_law(r, m.a), f_free=ffree, F_enc=Fenc, Delta=D)
    return out


def dphi_min(m, st):
    """min over r of Phi_t - Phi_f on a model-C extremum (K3 pre-statement)."""
    beta, l = st["beta"], st["l"]
    sol = m.integrate(beta, l, dense=True)
    R, a = m.R, m.a
    yR = sol.y[:, -1]
    T, F = yR[0], yR[1]
    phibR = -m.mb / (R + a)
    PtR, PfR = phibR - F / R + T * T / (3 * R ** 3), phibR - (T + F) / R
    ss = np.linspace(math.log(m.rin * 10), math.log(R), 400)
    vals = []
    for s in ss:
        y = sol.sol(s)
        vals.append((PtR - (yR[2] - y[2])) - (PfR - (yR[3] - y[3])))
    return min(vals), (PtR - PfR)


def classify(st, prof, prof_half):
    if st is None:
        return "ILL-POSED (a)"
    D = prof["rg"]["Delta"]
    rising = prof["rg"]["f_free"] - prof_half["f_free"] >= 0.05
    if D > 0.80:
        return "OVERSHOOT"
    if 0.15 <= D <= 0.80:
        return "CONCENTRATED FREE CORE" if rising else "INTERMEDIATE"
    if 0.05 <= D < 0.15:
        return "INTERMEDIATE"
    if -0.05 < D < 0.05 or prof["rg"]["f_free"] < 0.05:
        return "NO FREE EXCESS"
    return "WRONG SIGN"


def state_report(m, st, tag):
    if st is None:
        P(f"    {tag}: no stable-branch extremum at this energy")
        return None
    a = m.a
    radii = {"0.5rg": 0.5 * r_g(a), "rh": 2.414 * a, "rg": r_g(a), "2rg": 2 * r_g(a), "Rhalf": 0.5 * m.R}
    pr = profile(m, st, radii)
    sig = 1.0 / st["beta"]
    P(f"    {tag}: beta {st['beta']:.4g}  sigma^2/(Vf^2/2) {2 * sig:.4g}  E {st['E']:.5g}  p {st['p']:.3f}")
    for k in ("0.5rg", "rh", "rg", "2rg", "Rhalf"):
        q = pr[k]
        P(f"      r={q['r']:8.3f} ({k:5s}) Mt {q['Mt']:.4g}  Mf {q['Mf']:.4g}  M_law {q['M_law']:.4g}  f_free {q['f_free']:.4f}"
          f"  F(<r) {q['F_enc']:.4f}  Delta {q['Delta']:+.3f} dex")
    return pr


def run_cell(kind, sysname, foot, N, Rmode, E_keys=("E_INF", "E_LAW"), p_max=60.0):
    s = SYSTEMS[sysname]
    a = s["a"]
    Mc = SUP * N
    rta = r_ta_over_rM(s["logMb"], N, foot)
    Rf = R_fill(Mc, a)
    R = rta if Rmode == "r_ta" else Rf
    m = Model(kind, Mc, R, a)
    targets = {}
    if "E_INF" in E_keys:
        targets["E_INF"] = E_INF(Mc, R, a, kind)
    if "E_LAW" in E_keys and kind != "N1":
        targets["E_LAW"] = E_LAW(Mc, a)
    t0 = time.time()
    ser = series(m, targets, p_max=p_max)
    P(f"  [{kind}] {sysname} {foot} N={N} R={Rmode}: R = {R:.2f} r_M (r_ta {rta:.1f}, R_fill {Rf:.2f}), M_c = {Mc:.3f}, a = {a}")
    P(f"    targets: " + ", ".join(f"{k} = {v:.5g}" for k, v in targets.items()) + f"   series: {len(ser['points'])} pts, "
      f"status {ser['status']}, {time.time() - t0:.0f} s")
    if ser["points"]:
        Es = [q["E"] for q in ser["points"]]
        P(f"    series E range: hot {Es[0]:.5g} -> last {Es[-1]:.5g}; min on stable branch "
          f"{(ser['turn']['E'] if ser['turn'] else min(Es)):.5g} at p {(ser['turn']['p'] if ser['turn'] else ser['points'][int(np.argmin(Es))]['p']):.3f}"
          f"{' (TURNING POINT)' if ser['turn'] else ' (no turning point found)'}")
    res = dict(kind=kind, system=sysname, footing=foot, N=N, Rmode=Rmode, R=R, r_ta=rta, R_fill=Rf, Mc=Mc, a=a,
               targets=targets, status=ser["status"], n_pts=len(ser["points"]),
               E_turn=(ser["turn"]["E"] if ser["turn"] else None), p_turn=(ser["turn"]["p"] if ser["turn"] else None),
               E_last=(ser["points"][-1]["E"] if ser["points"] else None), states={})
    if ser["turn"] is not None and kind != "NC":
        # post-result diagnostic (not graded): the most concentrated state that is still a local maximum
        tpr = profile(m, ser["turn"], {"rg": r_g(a), "Rhalf": 0.5 * R})
        res["turn_profile"] = tpr
        P(f"    [diagnostic, not graded] at the turning point (most concentrated local maximum): beta {ser['turn']['beta']:.4g}, "
          f"Delta(r_g) {tpr['rg']['Delta']:+.3f} dex, f_free(r_g) {tpr['rg']['f_free']:.4f}, f_free(R/2) {tpr['Rhalf']['f_free']:.4f}")
    for k in targets:
        st = ser["states"][k]
        pr = state_report(m, st, k)
        entry = dict(found=st is not None)
        if st is not None:
            entry.update(beta=st["beta"], E=st["E"], p=st["p"], profile=pr)
            if kind == "C":
                dmin, _ = dphi_min(m, st)
                entry["min_dPhi"] = dmin
            entry["class"] = classify(st, pr, pr["Rhalf"]) if kind != "NC" else None
        else:
            # distinguish no-maximum (turning point above target) from not reached
            reached_turn = ser["turn"] is not None
            entry["reason"] = ("E_target below the stable branch (turning point at E = %.5g)" % ser["turn"]["E"]) if reached_turn \
                else ("not reached (%s; last E = %.5g)" % (ser["status"], res["E_last"] if res["E_last"] is not None else float('nan')))
            entry["class"] = "ILL-POSED (a)"
        res["states"][k] = entry
    return res, m, ser


def nc_grid(Mc, R, a, betas, N=1600, rmin=1e-4, m0=None):
    """Tethered-only (model NC) extremum on a radial grid: damped Newton on the convex free energy
    F_beta(m) = U_d(m) + (1/beta) sum m ln(m/V) at fixed total mass (KKT), line search on F_beta. Independent of the shooting;
    used for K1 at large beta, where outward shooting is unstable (the pinned law is an outward-unstable manifold).
    U_d = sum m_k Phi_b(r_k) + (1/3) sum W_i M_i^3 + T^3/(9R^3), M_i = sum_{j<i} m_j + m_i/2."""
    re = np.concatenate([[0.5 * rmin], np.geomspace(rmin, R, N)])
    rc = np.sqrt(re[:-1] * re[1:])
    V = 4 * np.pi / 3 * (re[1:] ** 3 - re[:-1] ** 3)
    W = (re[:-1] ** -3 - re[1:] ** -3) / 3.0
    phib = -1.0 / (rc + a)
    n = len(rc)
    m = Mc * V / V.sum() if m0 is None else m0.copy()
    out = []

    def parts(m):
        Me = np.cumsum(m)
        Mi = Me - 0.5 * m
        T = Me[-1]
        S = np.concatenate([np.cumsum((2 * W * Mi)[::-1])[::-1], [0.0]])     # S[k] = sum_{i>=k} 2 W_i M_i
        return Me, Mi, T, S

    def Ud(m):
        Me, Mi, T, S = parts(m)
        return float(np.sum(m * phib) + np.sum(W * Mi ** 3) / 3.0 + T ** 3 / (9 * R ** 3))

    def Fb(m, beta):
        return Ud(m) + float(np.sum(m * np.log(m / V))) / beta

    idx = np.arange(n)
    for beta in betas:
        for it in range(400):
            Me, Mi, T, S = parts(m)
            S2 = np.concatenate([np.cumsum((W * Mi ** 2)[::-1])[::-1], [0.0]])  # sum_{i>=k} W_i M_i^2
            Q = 0.5 * W * Mi ** 2 + S2[1:] + T ** 2 / (3 * R ** 3)
            g = phib + Q + (np.log(m / V) + 1.0) / beta
            K = np.maximum(idx[:, None], idx[None, :])
            Hc = (W * Mi)[K] + S[1:][K]
            Hc[idx, idx] = 0.5 * W * Mi + S[1:]
            Hc += 2 * T / (3 * R ** 3)
            H = Hc + np.diag(1.0 / (beta * m))
            KKT = np.zeros((n + 1, n + 1))
            KKT[:n, :n] = H
            KKT[:n, n] = 1.0
            KKT[n, :n] = 1.0
            sol = np.linalg.solve(KKT, np.concatenate([-g, [0.0]]))
            dm = sol[:n]
            dec = float(-np.dot(g, dm))
            if dec < 1e-13 * max(1.0, abs(Fb(m, beta))):
                break
            neg = dm < 0
            amax = min(1.0, 0.99 * float(np.min(-m[neg] / dm[neg]))) if np.any(neg) else 1.0
            F0, alpha = Fb(m, beta), amax
            while alpha > 1e-12:
                m2 = m + alpha * dm
                if np.all(m2 > 0) and Fb(m2, beta) <= F0 - 1e-4 * alpha * dec:
                    break
                alpha *= 0.5
            m = m + alpha * dm
        Me, Mi, T, S = parts(m)
        U = Ud(m)
        out.append(dict(beta=beta, E=1.5 * T / beta + U, U=U, decrement=dec, its=it, m=m.copy(),
                        Mt_at=lambda r, Me=Me: float(np.interp(r, re[1:], Me))))
    return out


def k2_antonov():
    m = Model("N1", 1.0, 1.0, 1.0, mb=0.0)
    ser = series(m, {}, p_max=12.0)
    if ser["turn"] is None:
        return dict(ok=False, note="no turning point", status=ser["status"])
    st = ser["turn"]
    sol = m.integrate(st["beta"], st["l"])
    contrast = math.exp(st["beta"] * sol.y[1, -1])
    Lam = -st["E"] * 1.0 / 1.0
    ok = abs(Lam - 0.3346) < 0.002 and 690 <= contrast <= 730
    return dict(ok=ok, Lambda=Lam, contrast=contrast, beta=st["beta"])


def k3_identity():
    import sympy as sp
    r, f, G, Mb, V = sp.symbols("r f G M_b V", positive=True)
    out = {}
    for name, C, D in (("t", G * Mb * (1 - f ** 2), (1 - f) * V ** 2), ("f", G * Mb, V ** 2)):
        s2 = C / (3 * r) + D / 2
        jeans = sp.simplify(sp.diff(s2, r) - 2 * s2 / r + C / r ** 2 + D / r)
        out[name] = (s2, jeans)
    diff = sp.simplify(out["f"][0] - out["t"][0] - (f ** 2 * G * Mb / (3 * r) + f * V ** 2 / 2))
    ok = diff == 0 and out["t"][1] == 0 and out["f"][1] == 0
    return dict(ok=bool(ok), residual=str(diff), jeans_t=str(out["t"][1]), jeans_f=str(out["f"][1]))


def main():
    T0 = time.time()
    P(f"CFG848 maximum-entropy partition{' -- MUTATE (tether removed: one ordinary species)' if MUT else ''}")
    P(f"criteria cf0aad80f; Delta_ta(0) = {DELTA_TA0:.6f} (CFG654 N0); rho_m0 = {RHO_M0:.4e} kg/m^3 (H0 67.4, Om 0.315); f_b = {FB:.5f}")
    for sname, s in SYSTEMS.items():
        for foot in ("can", "alt"):
            P(f"  {sname} {foot}: r_ta/r_M = {r_ta_over_rM(s['logMb'], 10, foot):.2f} (N=10), {r_ta_over_rM(s['logMb'], 5.6, foot):.2f} (N=5.6);"
              f" R_fill = {R_fill(SUP * 10, s['a']):.3f}; r_g = {r_g(s['a'])}; E_LAW = {E_LAW(SUP * 10, s['a']):.5g}")
    RES = dict(lane="CFG848", mutate=MUT, criteria_commit="cf0aad80f", inputs=dict(Delta_ta0=DELTA_TA0, H0=67.4, Om=OM, fb=FB,
               sup=SUP, systems=SYSTEMS, a0=A0), cells=[], controls={})
    kind = "N1" if MUT else "C"

    P("\n== Controls")
    k3 = k3_identity()
    P(f"  K3 Codex identity sigma_f^2 - sigma_t^2 = f^2 G M_b/3r + f V^2/2: residual {k3['residual']}, Jeans residuals "
      f"{k3['jeans_t']}, {k3['jeans_f']} -> {'PASS' if k3['ok'] else 'FAIL'}")
    k2 = k2_antonov()
    P(f"  K2 Antonov (no baryons, no tether): Lambda = {k2.get('Lambda', float('nan')):.4f}, contrast = "
      f"{k2.get('contrast', float('nan')):.1f} -> {'PASS' if k2['ok'] else 'FAIL'}")
    RES["controls"]["K3"], RES["controls"]["K2"] = k3, k2

    # K1: NC series in the P1 canonical primary box. Outward shooting stalls once the law is pinned (outward-unstable
    # manifold, beta ~ 1e2); the series is continued to beta = 2e4 with the independent convex grid solver (nc_grid),
    # cross-validated against the shooting at beta = 20, 40, 55.
    s = SYSTEMS["P1"]
    Mc = SUP * 10
    R = r_ta_over_rM(s["logMb"], 10, "can")
    mK = Model("NC", Mc, R, s["a"])
    serK = series(mK, {}, p_max=60.0, beta_min_stop=1e3)
    P(f"  K1 shooting NC series: {len(serK['points'])} pts, last beta {serK['points'][-1]['beta']:.4g} [{serK['status']}]")
    xval = []
    for B in (20.0, 40.0, 55.0):
        pts = serK["points"]
        i = next((k for k, q in enumerate(pts) if q["beta"] >= B), None)
        if i is None or i == 0:
            continue

        def fB(p):
            sm = mK.summary(B, [p + math.log(mK.rhobar)])
            return math.log(sm["Mtot"] / Mc) if sm["ok"] and sm["Mtot"] > 0 else 50.0
        pB = brentq(fB, pts[i - 1]["p"] - 0.5, pts[i]["p"] + 0.5, xtol=1e-12)
        stB = mK.state_z(np.array([pB, math.log(B)]))
        prB = profile(mK, stB, {"rg": r_g(s["a"])})
        gB = nc_grid(Mc, R, s["a"], list(np.geomspace(2.0, B, 20)), N=1600)[-1]
        xval.append(dict(beta=B, E_shoot=stB["E"], E_grid=gB["E"], Mt_shoot=prB["rg"]["Mt"], Mt_grid=gB["Mt_at"](r_g(s["a"]))))
        P(f"    cross-check beta {B:.0f}: E shoot {stB['E']:.7g} grid {gB['E']:.7g}; M_t(r_g) shoot {prB['rg']['Mt']:.6g} "
          f"grid {gB['Mt_at'](r_g(s['a'])):.6g}")
    gK = nc_grid(Mc, R, s["a"], list(np.geomspace(2.0, 2e4, 60)), N=1600)
    lastG = gK[-1]
    ELAW = E_LAW(Mc, s["a"])
    ratio = lastG["Mt_at"](r_g(s["a"])) / M_law(r_g(s["a"]), s["a"])
    minE = min([q["E"] for q in serK["points"]] + [q["E"] for q in gK])
    k1ok = abs(ratio - 1) < 0.02 and abs(lastG["E"] - ELAW) < 0.02 * abs(ELAW) and ELAW <= minE + 1e-9
    for q in gK[::12] + [gK[-1]]:
        P(f"    grid beta {q['beta']:9.4g}: E {q['E']:+.6g}  M_t(r_g)/M_law {q['Mt_at'](r_g(s['a'])) / M_law(r_g(s['a']), s['a']):.5f}"
          f"  M_t(30)/M_law {q['Mt_at'](30.0) / M_law(30.0, s['a']):.5f}")
    P(f"  K1 law limit (NC, P1 can box R={R:.1f}): beta reached {lastG['beta']:.4g}; M_t(r_g)/M_law = {ratio:.5f}; "
      f"E = {lastG['E']:.6g} vs E_LAW = {ELAW:.6g} (rel {abs(lastG['E'] - ELAW) / abs(ELAW):.4f}); E_LAW <= min series E "
      f"({minE:.5g}): {ELAW <= minE + 1e-9} -> {'PASS' if k1ok else 'FAIL'}")
    RES["controls"]["K1"] = dict(ok=bool(k1ok), beta=lastG["beta"], ratio=ratio, E=lastG["E"], E_LAW=ELAW, minE=minE,
                                 shoot_status=serK["status"], shoot_last_beta=serK["points"][-1]["beta"], crosscheck=xval)

    P(f"\n== Cells (model {kind})")
    min_dphi = []
    for foot in ("can", "alt"):
        for sname in ("P1", "P2"):
            for Rmode in ("r_ta", "R_fill"):
                res, m, ser = run_cell(kind, sname, foot, 10, Rmode)
                RES["cells"].append(res)
                for k, e in res["states"].items():
                    if e.get("min_dPhi") is not None:
                        min_dphi.append(e["min_dPhi"])
    for sname in ("P1", "P2"):
        res, m, ser = run_cell(kind, sname, "can", 5.6, "r_ta")
        RES["cells"].append(res)
        for k, e in res["states"].items():
            if e.get("min_dPhi") is not None:
                min_dphi.append(e["min_dPhi"])
    if not MUT:
        P("\n== Diagnostic: NC (no conversion, all tethered) at E_INF, primary boxes")
        P("   (shooting series as frozen; it stalls where the law is pinned, so the E_INF state is located with the convex")
        P("    grid solver nc_grid, which K1 cross-validated against the shooting to ~1e-6; post-result implementation fix of an")
        P("    ungraded diagnostic, disclosed)")
        for foot in ("can", "alt"):
            for sname in ("P1", "P2"):
                res, m, ser = run_cell("NC", sname, foot, 10, "r_ta", E_keys=("E_INF",))
                sy = SYSTEMS[sname]
                Et = res["targets"]["E_INF"]
                gl = nc_grid(res["Mc"], res["R"], sy["a"], list(np.geomspace(1.0, 2e4, 160)), N=800)
                Eg = [q["E"] for q in gl]
                i = next((k for k in range(1, len(gl)) if (Eg[k - 1] - Et) * (Eg[k] - Et) <= 0), None)
                if i is None:
                    P(f"    NC grid: E_INF not bracketed (E range {Eg[0]:.4g} .. {Eg[-1]:.4g})")
                    res["nc_grid"] = None
                else:
                    lo, hi = gl[i - 1], gl[i]
                    b0, b1, E0, E1 = math.log(lo["beta"]), math.log(hi["beta"]), lo["E"] - Et, hi["E"] - Et
                    q = hi
                    for _ in range(40):
                        bm = b0 - E0 * (b1 - b0) / (E1 - E0)
                        q = nc_grid(res["Mc"], res["R"], sy["a"], [math.exp(bm)], N=800, m0=lo["m"])[-1]
                        if abs(q["E"] - Et) < 1e-9 * max(1.0, abs(Et)):
                            break
                        if (q["E"] - Et) * E0 > 0:
                            b0, E0 = bm, q["E"] - Et
                        else:
                            b1, E1 = bm, q["E"] - Et
                    rg_ = r_g(sy["a"])
                    rh_ = 2.414 * sy["a"]
                    Dg = math.log10((1 / (rg_ + sy["a"]) ** 2 * rg_ ** 2 + q["Mt_at"](rg_)) / (rg_ ** 2 / (rg_ + sy["a"]) ** 2 + M_law(rg_, sy["a"])))
                    Dh = math.log10((rh_ ** 2 / (rh_ + sy["a"]) ** 2 + q["Mt_at"](rh_)) / (rh_ ** 2 / (rh_ + sy["a"]) ** 2 + M_law(rh_, sy["a"])))
                    P(f"    NC grid at E_INF: beta {q['beta']:.4g} (sigma^2/(Vf^2/2) {2 / q['beta']:.4g}), E {q['E']:.6g}; "
                      f"M_t(r_g)/M_law {q['Mt_at'](rg_) / M_law(rg_, sy['a']):.4f}, Delta(r_g) {Dg:+.3f} dex, Delta(r_h) {Dh:+.3f} dex")
                    res["nc_grid"] = dict(beta=q["beta"], E=q["E"], Delta_rg=Dg, Delta_rh=Dh,
                                          Mt_rg_over_law=q["Mt_at"](rg_) / M_law(rg_, sy["a"]))
                RES["cells"].append(res)
        k3b = (len(min_dphi) > 0 and min(min_dphi) > 0)
        P(f"\n  K3 pre-statement: min over all model-C extrema of min_r (Phi_t - Phi_f) = "
          f"{(min(min_dphi) if min_dphi else float('nan')):.4g} -> {'PASS' if k3b else 'FAIL'}")
        RES["controls"]["K3_dPhi"] = dict(ok=bool(k3b), min=(min(min_dphi) if min_dphi else None))
    else:
        k3b = True

    # grading
    P("\n== Classes (primary cells: R = r_ta, E = E_INF, N = 10)")
    grade = {}
    for foot in ("can", "alt"):
        for sname in ("P1", "P2"):
            c_p = next(c for c in RES["cells"] if c["kind"] == kind and c["system"] == sname and c["footing"] == foot
                       and c["N"] == 10 and c["Rmode"] == "r_ta")
            c_f = next(c for c in RES["cells"] if c["kind"] == kind and c["system"] == sname and c["footing"] == foot
                       and c["N"] == 10 and c["Rmode"] == "R_fill")
            cp, cf = c_p["states"]["E_INF"]["class"], c_f["states"]["E_INF"]["class"]
            final = cp
            if cp != "ILL-POSED (a)" and cf != cp:
                final = f"ILL-POSED (b) truncation-dependent [r_ta: {cp}; R_fill: {cf}]"
            Dp = c_p["states"]["E_INF"].get("profile", {}).get("rg", {}).get("Delta")
            Df = c_f["states"]["E_INF"].get("profile", {}).get("rg", {}).get("Delta")
            grade[f"{sname}_{foot}"] = dict(class_=final, r_ta_class=cp, R_fill_class=cf, Delta_rg_rta=Dp, Delta_rg_Rfill=Df)
            P(f"  {sname} {foot}: {final}   (Delta(r_g): r_ta {Dp if Dp is None else round(Dp, 3)}, R_fill "
              f"{Df if Df is None else round(Df, 3)})")
    RES["grade"] = grade
    ok_controls = RES["controls"]["K1"]["ok"] and k2["ok"] and k3["ok"] and k3b
    RES["controls_pass"] = bool(ok_controls)
    if MUT:
        mainf = os.path.join(HERE, "cfg848_results.json")
        bites = None
        if os.path.exists(mainf):
            MAIN = json.load(open(mainf))
            bites = False
            for key, g in grade.items():
                gm = MAIN["grade"].get(key)
                if gm is None:
                    continue
                if gm["class_"] != g["class_"]:
                    bites = True
                Dm, Dn = gm.get("Delta_rg_rta"), g.get("Delta_rg_rta")
                if (Dm is None) != (Dn is None) or (Dm is not None and Dn is not None and abs(Dm - Dn) >= 0.05):
                    bites = True
        RES["mutate_bites"] = bites
        P(f"\nMUTATE bites: {bites}")
    P(f"\ncontrols pass: {ok_controls}; total time {time.time() - T0:.0f} s")
    json.dump(RES, open(os.path.join(HERE, f"cfg848_results{SFX}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg848{SFX}.out"), "w").write("\n".join(OUT) + "\n")
    if MUT:
        sys.exit(1 if RES.get("mutate_bites") else 0)
    sys.exit(0 if ok_controls else 1)


if __name__ == "__main__":
    main()
