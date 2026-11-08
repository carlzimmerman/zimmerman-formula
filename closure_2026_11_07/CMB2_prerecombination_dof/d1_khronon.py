#!/usr/bin/env python3
"""CMB2 / D1 (FROZEN_CRITERIA.md, 3274689858): the khronon (v3s) and the clock (AC2q) at z ~ 1100, dust part removed.
Own linear Newtonian-gauge code (conformal time, 8 pi G = 1, Mpc units). Imports nothing from F1A; reads only F1A's
B2 fit parameters (parts/fit_B2_<foot>_cold.json) and its g4.json for the KA comparison.
Part S: sympy derivation of the linear khronon / clock equation from the actions (P = 0 block).
Part N: numbers. One thread, < 1 GB. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
F1A = os.path.join(HERE, "../F1A_primary_cmb_audit/parts")
NOTE = "kappa = 1/2 FITTED; not theory closed"
OMG = 2.4728e-5                                   # omega_gamma (T 2.7255 K)
OMR = OMG * (1 + 3.046 * 7 / 8 * (4 / 11) ** (4 / 3))
OUT = {"note": NOTE}
AMP = (1e-4, 1e-3, 1e-2)
LOG = []
def P(*s):
    t = " ".join(str(x) for x in s); print(t, flush=True); LOG.append(t)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9 / (1 if sys.platform == "darwin" else 1e-3)

# =============================================================== Part S: sympy
def part_S():
    eta, x, k, eps = sp.symbols("eta x k epsilon", real=True)
    a = sp.Function("a", positive=True)(eta); T = sp.Function("T")(eta)
    pi_ = sp.Function("pi")(eta, x); Psi = sp.Function("Psi")(eta, x); Phi = sp.Function("Phi")(eta, x)
    mu2, K, lam = sp.symbols("mu_K2 K lambda_V", positive=True)
    Vf = sp.Function("V")
    def S2(Flag, with_V):
        tau = T + eps * pi_
        sg = a ** 4 * sp.sqrt(1 + 2 * eps * Psi) * (1 - 2 * eps * Phi) ** sp.Rational(3, 2)
        Q2 = sp.diff(tau, eta) ** 2 / (a ** 2 * (1 + 2 * eps * Psi)) - sp.diff(tau, x) ** 2 / (a ** 2 * (1 - 2 * eps * Phi))
        Q = sp.sqrt(Q2)
        L = Flag(Q)
        if with_V: L = L - Vf(tau)
        dens = sg * L
        ser = sp.series(dens, eps, 0, 3).removeO()
        return sp.expand(ser.coeff(eps, 2)), sp.expand(ser.coeff(eps, 1))
    res = {}
    for name, Flag, with_V in (("v3s_khronon", lambda Q: mu2 * (Q - 1) ** 2 / (2 * K), False),
                               ("AC2q_clock", lambda Q: Q ** 2 / 2, True)):
        L2, L1 = S2(Flag, with_V)
        EL = sp.euler_equations(L2, [pi_], [eta, x])[0].lhs
        # background equation from L1 (coefficient of pi): d/d eta (dL1/d pi_eta) - dL1/d pi = 0
        EL0 = sp.euler_equations(L1, [pi_], [eta, x])[0].lhs
        Qb = sp.Function("Qb", positive=True)(eta)
        sub = {sp.Derivative(T, (eta, 2)): sp.diff(a * Qb, eta), sp.Derivative(T, eta): a * Qb}
        EL = sp.simplify(EL.subs(sub)); EL0 = sp.simplify(EL0.subs(sub))
        bgs = {sp.Derivative(Qb, eta): sp.solve(EL0, sp.Derivative(Qb, eta))[0]}
        EL = sp.simplify(EL.subs(bgs))
        # plane wave
        Pc, Ps, Ph = sp.Function("Pc")(eta), sp.Function("psi")(eta), sp.Function("phi")(eta)
        pw = {pi_: Pc * sp.cos(k * x), Psi: Ps * sp.cos(k * x), Phi: Ph * sp.cos(k * x)}
        ELk = sp.simplify((EL.subs(pw).doit()) / sp.cos(k * x))
        ELk = sp.simplify(ELk / sp.expand(ELk).coeff(sp.diff(Pc, eta, 2)))
        res[name] = dict(EL_background=EL0, EL_linear=ELk, bg=bgs)
        P(f"[S] {name}: background: Qb' = {sp.simplify(bgs[sp.Derivative(Qb, eta)])}")
        P(f"[S] {name}: linear (pi = Pc cos kx; Psi = psi cos kx; Phi = phi cos kx; background used):  {sp.collect(sp.expand(ELk), [sp.diff(Pc, eta, 2), sp.diff(Pc, eta), Pc], sp.factor)} = 0")
    # fluid check for v3s: rho = Q F' - F, p = F, dQ = Pc'/a - Qb psi, (rho+p) theta = F'(Qb) k^2 Pc / a
    Qb = sp.Function("Qb", positive=True)(eta); Pc, Ps, Ph = sp.Function("Pc")(eta), sp.Function("psi")(eta), sp.Function("phi")(eta)
    Fq = lambda Q: mu2 * (Q - 1) ** 2 / (2 * K); Q_ = sp.Symbol("Q_")
    F1 = sp.diff(Fq(Q_), Q_); F2 = sp.diff(Fq(Q_), Q_, 2)
    H = sp.diff(a, eta) / a
    dQ = sp.diff(Pc, eta) / a - Qb * Ps
    drho = (Q_ * F2).subs(Q_, Qb) * dQ; dp = F1.subs(Q_, Qb) * dQ
    rpth = F1.subs(Q_, Qb) * k ** 2 * Pc / a
    rpb = (Q_ * F1).subs(Q_, Qb)
    # background: a^3 F'(Qb) = const  ->  Qb' = -3 H F'/F''
    bg = {sp.Derivative(Qb, eta): sp.solve(sp.diff(a ** 3 * F1.subs(Q_, Qb), eta), sp.Derivative(Qb, eta))[0]}
    ELk = res["v3s_khronon"]["EL_linear"]
    sol = sp.solve(ELk, sp.Derivative(Pc, (eta, 2)))[0]
    cont = sp.diff(drho, eta) + 3 * H * (drho + dp) + rpth - 3 * rpb * sp.diff(Ph, eta)
    cont = cont.subs(sp.Derivative(Pc, (eta, 2)), sol).subs(bg).doit().subs(bg)
    euler = sp.diff(rpth, eta) + 4 * H * rpth - k ** 2 * dp - k ** 2 * rpb * Ps
    euler = euler.subs(bg).doit().subs(bg)
    c_ok = sp.simplify(cont) == 0; e_ok = sp.simplify(euler) == 0
    cs2 = sp.simplify((F1 / (Q_ * F2)).subs(Q_, Qb))
    P(f"[S] v3s fluid identity: continuity <=> EL: {c_ok}; Euler identity: {e_ok}; c_s^2 = dp/drho = {cs2}")
    # AC2q: KG form check  pi'' + 2H pi' + k^2 pi + a^2 V'' pi = 4 T' psi' ... (Ma-Bertschinger) with phi=psi allowed general
    EL2 = res["AC2q_clock"]["EL_linear"]
    phib = sp.Function("T")(eta)
    KG = (sp.diff(Pc, eta, 2) + 2 * H * sp.diff(Pc, eta) + k ** 2 * Pc + a ** 2 * sp.Subs(sp.diff(Vf(Q_), Q_, 2), Q_, phib).doit() * Pc
          - sp.diff(phib, eta) * (sp.diff(Ps, eta) + 3 * sp.diff(Ph, eta)) + 2 * a ** 2 * sp.Subs(sp.diff(Vf(Q_), Q_), Q_, phib).doit() * Ps)
    # EL2 is written with T' = a Qb; express KG the same way
    KG = KG.subs({sp.Derivative(phib, eta): a * Qb})
    sol2 = sp.solve(EL2, sp.Derivative(Pc, (eta, 2)))[0]
    bg2 = sp.solve(res["AC2q_clock"]["EL_background"], sp.Derivative(Qb, eta))
    chk = sp.simplify(KG.subs(sp.Derivative(Pc, (eta, 2)), sol2).subs(res["AC2q_clock"]["bg"]))
    kg_ok = chk == 0
    P(f"[S] AC2q clock: linear EL == KG [d'' + 2H d' + k^2 d + a^2 V'' d = phib'(psi' + 3 phi') - 2 a^2 V' psi]: {kg_ok} (residual {chk})")
    OUT["S"] = dict(v3s_continuity_equals_EL=bool(c_ok), v3s_euler_identity=bool(e_ok), v3s_cs2=str(cs2), AC2q_KG=bool(kg_ok),
                    v3s_EL=str(res["v3s_khronon"]["EL_linear"]), AC2q_EL=str(res["AC2q_clock"]["EL_linear"]),
                    v3s_bg=str(res["v3s_khronon"]["EL_background"]), AC2q_bg=str(res["AC2q_clock"]["EL_background"]))
    return c_ok and e_ok and kg_ok

# =============================================================== Part N: linear solver
class Model:
    """Components: list of dicts. kinds:
       'fluid' (Om, w(a), cs2(a) rest-frame = adiabatic for barotropic) ; 'gb' tight-coupled photon-baryon (Omg, Omb);
       'kg' canonical scalar with V = V0 exp(-lam phi) (8piG = 1 units); 'bgonly' (Om, w) background-only smooth."""
    def __init__(self, h, comps, rem=True):
        self.h = h; self.H0 = h / 2997.92458; self.c = comps
        tot = 0.0
        for c in comps:
            if c["kind"] in ("fluid", "bgonly"): tot += c["Om"]
            elif c["kind"] == "gb": tot += c["Omg"] + c["Omb"]
            elif c["kind"] == "kg": tot += c["Om_today_est"]
        self.OL = (1 - tot) if rem else 0.0
    def rho_bg(self, a, y_kg=None):
        H02 = 3 * self.H0 ** 2; out = []
        for i, c in enumerate(self.c):
            if c["kind"] in ("fluid", "bgonly"): out.append(H02 * c["rho"](a))
            elif c["kind"] == "gb": out.append(H02 * (c["Omg"] / a ** 4 + c["Omb"] / a ** 3))
            elif c["kind"] == "kg":
                ph, dph = y_kg; out.append(dph ** 2 / (2 * a ** 2) + c["V0"] * math.exp(-c["lam"] * ph))
        return out, H02 * self.OL

    def run(self, k, a_out, ai=1e-6, rtol=1e-8, atol=1e-12, ic="poisson"):
        """state: [ln eta-free] we integrate in x = ln a.  y = [Phi, per comp...]; returns dict at each a in a_out."""
        H0 = self.H0; c = self.c
        # layout
        lay = []; n = 1
        for comp in c:
            if comp["kind"] == "fluid": lay.append(("fluid", n)); n += 2
            elif comp["kind"] == "gb": lay.append(("gb", n)); n += 3      # dg, db, theta
            elif comp["kind"] == "kg": lay.append(("kg", n)); n += 4      # phib, phib', dphi, dphi'
            else: lay.append(("bgonly", None))
        def unpack(a, y):
            ykg = None
            for (kd, j), comp in zip(lay, c):
                if kd == "kg": ykg = (y[j], y[j + 1])
            rr, rL = self.rho_bg(a, ykg); return rr, rL, ykg
        def rhs(xx, y):
            a = math.exp(xx); rr, rL, _ = unpack(a, y); tot = sum(rr) + rL
            Hc = a * math.sqrt(tot / 3.0)
            ph = y[0]; S = 0.0                                  # sum (rho+p) theta
            for (kd, j), comp, r in zip(lay, c, rr):
                if kd == "fluid": S += r * (1 + comp["w"](a)) * y[j + 1]
                elif kd == "gb":
                    rg = 3 * H0 ** 2 * comp["Omg"] / a ** 4; rb = 3 * H0 ** 2 * comp["Omb"] / a ** 3
                    S += (4 / 3 * rg + rb) * y[j + 2]
                elif kd == "kg": S += k ** 2 * y[j + 1] * y[j + 2] / a ** 2
            dph = -Hc * ph + a ** 2 * S / (2 * k ** 2)
            d = np.zeros_like(y); d[0] = dph
            for (kd, j), comp in zip(lay, c):
                if kd == "fluid":
                    w, cs2, ca2 = comp["w"](a), comp["cs2"](a), comp["ca2"](a); dl, th = y[j], y[j + 1]
                    dpr = cs2 * dl + 3 * Hc * (1 + w) * (cs2 - ca2) * th / k ** 2          # rest-frame sound speed cs2, adiabatic ca2
                    wp = -3 * Hc * (1 + w) * (ca2 - w)
                    d[j] = -(1 + w) * (th - 3 * dph) - 3 * Hc * (dpr - w * dl)
                    d[j + 1] = -Hc * (1 - 3 * w) * th - wp / (1 + w) * th + k ** 2 * dpr / (1 + w) + k ** 2 * ph
                elif kd == "gb":
                    Rb = 0.75 * comp["Omb"] / comp["Omg"] * a; dg, db, th = y[j], y[j + 1], y[j + 2]
                    d[j] = -4 / 3 * (th - 3 * dph); d[j + 1] = -(th - 3 * dph)
                    d[j + 2] = (-Hc * Rb * th + k ** 2 * dg / 4) / (1 + Rb) + k ** 2 * ph
                elif kd == "kg":
                    lam, V0 = comp["lam"], comp["V0"]; pb, pbd, dp, dpd = y[j:j + 4]
                    V = V0 * math.exp(-lam * pb); Vp = -lam * V; Vpp = lam ** 2 * V
                    d[j] = pbd; d[j + 1] = -2 * Hc * pbd - a ** 2 * Vp
                    d[j + 2] = dpd; d[j + 3] = -2 * Hc * dpd - k ** 2 * dp - a ** 2 * Vpp * dp + 4 * pbd * dph - 2 * a ** 2 * Vp * ph
            return d / Hc
        # initial conditions (adiabatic, superhorizon, Phi = Psi = 1)
        rr0, _ = self.rho_bg(ai, (c[[i for i, cc in enumerate(c) if cc["kind"] == "kg"][0]]["phi_i"], c[[i for i, cc in enumerate(c) if cc["kind"] == "kg"][0]]["dphi_i"]) if any(cc["kind"] == "kg" for cc in c) else None)
        Hci = ai * math.sqrt((sum(rr0) + 3 * H0 ** 2 * self.OL) / 3.0); eta_i = 1.0 / Hci     # radiation era eta = 1/Hc
        # ic = "f1a": theta = k^2 tau_i / 2 with tau_i = a_i/(H0 sqrt(Omega_r)) (F1A G4's convention);
        # ic = "poisson": common theta fixed so the 00+0i (Poisson) constraint k^2 Phi = -(a^2/2) sum rho Delta holds at a_i
        if ic == "f1a":
            Orad = sum(cc["Om"] for cc in c if cc["kind"] == "fluid" and abs(cc["w"](1.0) - 1 / 3) < 1e-12) + sum(cc["Omg"] for cc in c if cc["kind"] == "gb")
            th0 = 0.5 * k ** 2 * ai / (H0 * math.sqrt(Orad))
        else:
            sd = 0.0; sth = 0.0
            for (kd, j), comp, r in zip(lay, c, rr0):
                if kd == "fluid": w = comp["w"](ai); sd += r * (-1.5 * (1 + w)); sth += r * 3 * Hci * (1 + w) / k ** 2
                elif kd == "gb":
                    rg = 3 * H0 ** 2 * comp["Omg"] / ai ** 4; rb = 3 * H0 ** 2 * comp["Omb"] / ai ** 3
                    sd += -2 * rg - 1.5 * rb; sth += (4 * rg + 3 * rb) * Hci / k ** 2
            th0 = (-2 * k ** 2 / ai ** 2 - sd) / sth
        self.th0 = th0
        y0 = [1.0]
        for (kd, j), comp in zip(lay, c):
            if kd == "fluid": w = comp["w"](ai); y0 += [-1.5 * (1 + w), th0]
            elif kd == "gb": y0 += [-2.0, -1.5, th0]
            elif kd == "kg": y0 += [comp["phi_i"], comp["dphi_i"], 0.0, 0.0]
        xs = np.log(np.atleast_1d(a_out))
        s = solve_ivp(rhs, (math.log(ai), xs.max()), y0, method="LSODA", rtol=rtol, atol=atol, t_eval=np.sort(xs))
        if not s.success: raise RuntimeError(s.message)
        res = []
        for ii, xx in enumerate(s.t):
            a = math.exp(xx); y = s.y[:, ii]; rr, rL, ykg = unpack(a, y); tot = sum(rr) + rL; Hc = a * math.sqrt(tot / 3)
            row = dict(a=a, Phi=y[0], comp={})
            for (kd, j), comp, r in zip(lay, c, rr):
                nm = comp["name"]
                if kd == "fluid":
                    w = comp["w"](a); D = r * (y[j] + 3 * Hc * (1 + w) * y[j + 1] / k ** 2)
                    row["comp"][nm] = dict(delta=y[j], drho=r * y[j], PhiW=-a ** 2 * D / (2 * k ** 2))
                elif kd == "gb":
                    rg = 3 * H0 ** 2 * comp["Omg"] / a ** 4; rb = 3 * H0 ** 2 * comp["Omb"] / a ** 3
                    Dg = rg * (y[j] + 4 * Hc * y[j + 2] / k ** 2); Db = rb * (y[j + 1] + 3 * Hc * y[j + 2] / k ** 2)
                    row["comp"][nm] = dict(delta_g=y[j], delta_b=y[j + 1], PhiW=-a ** 2 * (Dg + Db) / (2 * k ** 2))
                elif kd == "kg":
                    pb, pbd, dp, dpd = y[j:j + 4]; V = comp["V0"] * math.exp(-comp["lam"] * pb); Vp = -comp["lam"] * V
                    drho = (pbd * dpd - pbd ** 2 * y[0]) / a ** 2 + Vp * dp; rpth = k ** 2 * pbd * dp / a ** 2
                    D = drho + 3 * Hc * rpth / k ** 2
                    row["comp"][nm] = dict(drho=drho, delta=drho / r, PhiW=-a ** 2 * D / (2 * k ** 2), w=(pbd ** 2 / (2 * a ** 2) - V) / r, Omega=r / tot)
            res.append(row)
        return res

def const(v): return lambda a: v
def fl(name, Om, w=0.0, cs2=0.0):
    return dict(kind="fluid", name=name, Om=Om, w=const(w), cs2=const(cs2), ca2=const(w), rho=lambda a, Om=Om, w=w: Om * a ** (-3 * (1 + w)))
def khronon(name, Om, w0):
    """v3s K(Q) fluid: rho = 3H0^2 Om (1 + w0/a^3)/a^3, w = w0/(w0+a^3), c_s^2 = q/(1+q) = 2w0/(a^3+2w0)."""
    return dict(kind="fluid", name=name, Om=Om, w=lambda a: w0 / (w0 + a ** 3), cs2=lambda a: 2 * w0 / (a ** 3 + 2 * w0), ca2=lambda a: 2 * w0 / (a ** 3 + 2 * w0),
                rho=lambda a: Om * (1 + w0 / a ** 3) / a ** 3)

# =============================================================== main
def main():
    t0 = time.time()
    P("D1 khronon / clock at z 1100.", NOTE)
    okS = part_S(); OUT["S_pass"] = bool(okS)
    zs = 1100.0; aZ = 1 / (1 + zs); KS = [0.01, 0.03, 0.1, 0.3]
    # still/follows window
    zwin = np.linspace(700.0, 3000.0, 160); awin = np.sort(1 / (1 + zwin))
    g4 = json.load(open(os.path.join(F1A, "g4.json")))
    for foot in ("canonical", "alt"):
        pr = json.load(open(os.path.join(F1A, f"fit_B2_{foot}_cold.json")))["pars"]
        h = pr["h"]; Ob = pr["ob"] / h ** 2; Od = pr["oc"] / h ** 2; Or = OMR / h ** 2; Og = OMG / h ** 2; On = Or - Og
        R = Od / Ob; FO = dict(h=h, Ob=Ob, Od=Od, Or=Or, R=R); OUT[foot] = FO
        fcap = {"canonical": 0.33, "alt": 0.19}[foot]
        P(f"\n=== {foot}: B2 cold fit h {h:.6f} Ob {Ob:.6f} Od {Od:.6f} R = Od/Ob {R:.4f}; KD1 cap f {fcap}")
        # ---------------- KA-dust (F1A G4 model: radiation one fluid, baryons dust, cold dust, Lambda remainder)
        ka = {}
        for k in (0.02, 0.05, 0.1, 0.2, 0.3):
            m = Model(h, [fl("r", Or, 1 / 3, 1 / 3), fl("b", Ob), fl("d", Od)])
            ref = m.run(k, [aZ], ic="f1a")[0]
            mX1 = Model(h, [fl("r", Or, 1 / 3, 1 / 3), fl("b", Ob), fl("d", Od), fl("X", 1 - Or - Ob - Od, -0.95, 1.0)])
            x1 = mX1.run(k, [aZ], ic="f1a")[0]
            mX2 = Model(h, [fl("r", Or, 1 / 3, 1 / 3), fl("b", Ob), fl("X", Od, 0.0, 1.0)])
            x2 = mX2.run(k, [aZ], ic="f1a")[0]
            # same model, constraint-consistent initial data (Poisson residual 0 at a_i), and its a_i convergence
            refP = Model(h, [fl("r", Or, 1 / 3, 1 / 3), fl("b", Ob), fl("d", Od)]).run(k, [aZ], ic="poisson", rtol=1e-9, atol=1e-14)[0]
            refP7 = Model(h, [fl("r", Or, 1 / 3, 1 / 3), fl("b", Ob), fl("d", Od)]).run(k, [aZ], ai=1e-7, ic="poisson", rtol=1e-9, atol=1e-14)[0]
            refF7 = Model(h, [fl("r", Or, 1 / 3, 1 / 3), fl("b", Ob), fl("d", Od)]).run(k, [aZ], ai=1e-7, ic="f1a", rtol=1e-9, atol=1e-14)[0]
            ka[k] = dict(delta_b=ref["comp"]["b"]["delta"], Q_X1=abs(x1["comp"]["X"]["drho"]) / abs(ref["comp"]["d"]["drho"]),
                         Q_X2=abs(x2["comp"]["X"]["drho"]) / abs(ref["comp"]["d"]["drho"]),
                         delta_b_poissonIC=refP["comp"]["b"]["delta"], delta_b_poissonIC_ai1em7=refP7["comp"]["b"]["delta"],
                         delta_b_f1aIC_ai1em7=refF7["comp"]["b"]["delta"])
            P(f"[KA {foot}] k {k}: F1A IC: delta_b {ka[k]['delta_b']:.4f} (a_i 1e-7: {refF7['comp']['b']['delta']:.4f}); "
              f"constraint-consistent IC: {refP['comp']['b']['delta']:.4f} (a_i 1e-7: {refP7['comp']['b']['delta']:.4f});  Q_X1 {ka[k]['Q_X1']:.3e}  Q_X2 {ka[k]['Q_X2']:.3e}")
        tgt = {0.05: -26.8, 0.3: -108.1}
        ka_pass = all(abs(ka[k]["delta_b"] / tgt[k] - 1) <= 0.05 for k in tgt)
        ka_pass_P = all(abs(ka[k]["delta_b_poissonIC"] / tgt[k] - 1) <= 0.05 for k in tgt)
        cmp_g4 = None
        if foot == "canonical":
            cmp_g4 = {r["k"]: dict(delta_b_F1A=r["delta_b_ref"], Q_X1_F1A=r["Q_X1"], Q_X2_F1A=r["Q_X2"]) for r in g4["rows"]}
        FO["KA_dust"] = dict(rows=ka, targets=tgt, pass_=bool(ka_pass), pass_constraint_consistent_IC=bool(ka_pass_P), F1A_g4=cmp_g4,
                             Q_X1_max=max(v["Q_X1"] for v in ka.values()), Q_X2_max_k_ge_0p05=max(v["Q_X2"] for k, v in ka.items() if k >= 0.05))
        P(f"[KA {foot}] delta_b vs -26.8 / -108.1 (F1A IC): {ka[0.05]['delta_b']:.3f} / {ka[0.3]['delta_b']:.3f} -> {'PASS' if ka_pass else 'FAIL'};"
          f" constraint-consistent IC: {ka[0.05]['delta_b_poissonIC']:.3f} / {ka[0.3]['delta_b_poissonIC']:.3f} -> {'PASS' if ka_pass_P else 'FAIL'};"
          f" Q_X1 max {FO['KA_dust']['Q_X1_max']:.2e}, Q_X2 (k>=0.05) max {FO['KA_dust']['Q_X2_max_k_ge_0p05']:.2e}")

        # ---------------- graded runs: tight-coupled photon-baryon + neutrino fluid (no anisotropic stress)
        base = lambda: [dict(kind="gb", name="gb", Omg=Og, Omb=Ob), fl("nu", On, 1 / 3, 1 / 3)]
        # thawing clock: V = V0 exp(-lam phi), lam 0.5, frozen at a_i;  tracker clock lam = sqrt(40) on its radiation attractor
        def clock(lam, mode):
            if mode == "thaw":
                return dict(kind="kg", name="clock", lam=lam, V0=3 * (h / 2997.92458) ** 2 * (1 - Or - Ob - Od), phi_i=0.0, dphi_i=0.0, Om_today_est=1 - Or - Ob - Od)
            # radiation-era scaling attractor: x = sqrt(3/2)(4/3)/lam, y^2 = 3(1-1/9)/(2 lam^2) -> Omega = 4/lam^2
            H0 = h / 2997.92458; ai = 1e-6; Om_phi = 4 / lam ** 2
            rho_oth = 3 * H0 ** 2 * (Or / ai ** 4 + (Ob + Od * 0) / ai ** 3); Htot2 = rho_oth / (3 * (1 - Om_phi))
            xx = math.sqrt(1.5) * (4 / 3) / lam; yy = math.sqrt(3 * (1 - 1 / 9) / (2 * lam ** 2))
            dphidt = xx * math.sqrt(6 * Htot2); V = yy ** 2 * 3 * Htot2
            return dict(kind="kg", name="clock", lam=lam, V0=V, phi_i=0.0, dphi_i=ai * dphidt, Om_today_est=0.0)
        cases = {
            "dust_R": base() + [fl("d", Od)],
            "khronon_fcap": base() + [khronon("K", fcap * Ob, 0.0)],
            "khronon_fcap_Hfixed": base() + [khronon("K", fcap * Ob, 0.0), dict(kind="bgonly", name="smooth", Om=Od - fcap * Ob, w=const(0.0), rho=lambda a, O=Od - fcap * Ob: O / a ** 3)],
            "clock_thaw": base() + [fl("d", Od), clock(0.5, "thaw")],
            "clock_track_lam6.32_noCold": base() + [clock(math.sqrt(40.0), "track")],
            "clock_stiff_fullOd_X2": base() + [fl("X", Od, 0.0, 1.0)],
            "baryons_only": base(),
        }
        # (c) non-dust khronon: w0 at the BBN bound; mu_B scales with Omega_K (KD1 B1b): w0max = 0.067 Om_r a_BBN^2 / Om_K
        abbn = 1 / (1 + 1e5 / (8.617333262e-5 * 2.7255)); Om_r_kd1 = 2.47e-5 * (1 + 0.2271 * 3.046) / h ** 2
        H0 = h / 2997.92458
        def w0_at(OmK, mu): return 3 * H0 ** 2 * OmK / (4 * mu ** 2)
        for tag, OmK in (("full", Od), ("fcap", fcap * Ob)):
            w0B = 0.067 * Om_r_kd1 * abbn ** 2 / OmK; muB = math.sqrt(3 * H0 ** 2 * OmK / (4 * w0B))
            FO[f"BBN_{tag}"] = dict(Om_K=OmK, mu_B=muB, w0_B=w0B, w_z1100=w0B / (w0B + aZ ** 3), cs2_z1100=2 * w0B / (aZ ** 3 + 2 * w0B),
                                   kJ_comoving_z1100=aZ * muB)
            P(f"[c {foot}] {tag}: Om_K {OmK:.5f}: mu_B {muB:.4e} Mpc^-1, w0 {w0B:.3e}, w(z1100) {w0B / (w0B + aZ ** 3):.3e}, comoving k_J(z1100) {aZ * muB:.3e} Mpc^-1")
            # amplified w0 runs: scale factor s on w0 (mu -> mu_B/sqrt(s)); difference to w0 = 0 scales as s -> extrapolate to s = 1
            # amplified w0 so that w(a_i = 1e-6) = 1e-4, 1e-3, 1e-2 (keys AMP); the response is linear in w0 there
            for wi in AMP:
                cases[f"khr_{tag}_w0x{wi:.0e}"] = base() + [khronon("K", OmK, wi * 1e-18)]
            cases[f"khr_{tag}_w0x0"] = base() + [khronon("K", OmK, 0.0)]
            cases[f"khr_{tag}_w0B"] = base() + [khronon("K", OmK, w0B)]
        # (a') the uncaptured window: mu_K <= 79.43 (QX3 capture bound) with the largest BBN-allowed Om_K there
        muC = 79.43; OmK_C = None
        # BBN: w0 = 3H0^2 OmK/(4 mu^2) <= 0.067 Om_r a_BBN^2 / OmK  ->  OmK^2 <= 0.067 Om_r a_BBN^2 4 mu^2/(3 H0^2)
        OmK_C = math.sqrt(0.067 * Om_r_kd1 * abbn ** 2 * 4 * muC ** 2 / (3 * H0 ** 2)); w0C = w0_at(OmK_C, muC)
        FO["uncaptured_window"] = dict(mu_K=muC, Om_K_max=OmK_C, f_of_baryons=OmK_C / Ob, w0=w0C, w_z1100=w0C / (w0C + aZ ** 3),
                                      kJ_comoving_z1100=aZ * muC)
        cases["khr_uncaptured"] = base() + [khronon("K", OmK_C, w0C)]
        P(f"[a' {foot}] mu_K {muC}: BBN allows Om_K <= {OmK_C:.3e} (f = {OmK_C / Ob:.2e} of baryons); comoving k_J(z1100) {aZ * muC:.3f} Mpc^-1")

        tab = {}
        for k in KS:
            rows = {}
            for nm, comps in cases.items():
                rtol = 1e-10 if nm.startswith("khr_") else 1e-8
                m = Model(h, comps)
                rr = m.run(k, list(awin) + [aZ], rtol=rtol, atol=1e-14)
                rows[nm] = rr
            def at(nm): return [r for r in rows[nm] if abs(r["a"] - aZ) < 1e-12][0]
            Pd = at("dust_R")["comp"]["d"]["PhiW"]
            def series(nm, cmp_):
                return np.array([r["comp"][cmp_]["PhiW"] for r in rows[nm] if abs(r["a"] - aZ) > 1e-12])
            dg = np.array([r["comp"]["gb"]["delta_g"] for r in rows["dust_R"] if abs(r["a"] - aZ) > 1e-12])
            xw = np.log(awin)
            def osc(sv):
                c_ = np.polyfit(xw, sv, 2); res_ = sv - np.polyval(c_, xw); return res_, np.sqrt(np.mean(res_ ** 2)) / max(np.sqrt(np.mean(sv ** 2)), 1e-300)
            rg, sg = osc(dg)
            def still(sv):
                r_, s_ = osc(sv); O = s_ / sg; corr = float(np.corrcoef(r_, rg)[0, 1]) if np.std(r_) > 0 else 0.0
                lab = "still" if O < 0.1 else ("follows" if (O >= 0.5 and abs(corr) >= 0.5) else "mixed")
                return dict(O=float(O), corr=corr, label=lab)
            row = dict(PhiW_dust=Pd, Phi_total_dust=at("dust_R")["Phi"], dust=still(series("dust_R", "d")), photon_osc_index=float(sg))
            # MUTATE-phase: planted Weyl source phase-locked to delta_gamma with the dust's amplitude
            planted = dg / np.max(np.abs(dg)) * np.max(np.abs(series("dust_R", "d")))
            row["MUTATE_phase"] = still(planted); row["MUTATE_phase"]["ratio_max"] = float(np.max(np.abs(planted)) / abs(Pd))
            row["MUTATE_phase"]["prescreen_pass"] = bool(row["MUTATE_phase"]["label"] == "still" and row["MUTATE_phase"]["ratio_max"] >= 0.5)
            row["KA_dust_prescreen"] = dict(ratio=1.0, label=row["dust"]["label"], pass_=bool(row["dust"]["label"] == "still"))
            for nm, cmp_ in (("khronon_fcap", "K"), ("khronon_fcap_Hfixed", "K"), ("clock_thaw", "clock"),
                             ("clock_track_lam6.32_noCold", "clock"), ("clock_stiff_fullOd_X2", "X"), ("khr_uncaptured", "K")):
                v = at(nm)["comp"][cmp_]["PhiW"]; row[nm] = dict(ratio=v / Pd, **still(series(nm, cmp_)))
                if "Omega" in at(nm)["comp"][cmp_]: row[nm]["Omega_z1100"] = at(nm)["comp"][cmp_]["Omega"]; row[nm]["w_z1100"] = at(nm)["comp"][cmp_]["w"]
            # (c) non-dust part: Delta PhiW_K(w0) - PhiW_K(0) relative to the dust's
            for tag in ("full", "fcap"):
                b0 = at(f"khr_{tag}_w0x0")["comp"]["K"]["PhiW"]
                amp = {}
                for wi in AMP:
                    amp[wi] = (at(f"khr_{tag}_w0x{wi:.0e}")["comp"]["K"]["PhiW"] - b0) / Pd
                direct = (at(f"khr_{tag}_w0B")["comp"]["K"]["PhiW"] - b0) / Pd
                w0B = FO[f"BBN_{tag}"]["w0_B"]
                slope = amp[AMP[0]] / (AMP[0] * 1e-18) * w0B
                row[f"nondust_{tag}"] = dict(amplified_w_ai={f"{wi:.0e}": v for wi, v in amp.items()}, linear_check=amp[AMP[1]] / amp[AMP[0]] / (AMP[1] / AMP[0]),
                                            extrapolated_at_w0B=slope, direct_at_w0B=direct)
            mA = Model(h, cases["dust_R"]).run(k, [aZ], ic="f1a")[0]["comp"]["d"]["PhiW"]
            mB = Model(h, cases["khronon_fcap"]).run(k, [aZ], ic="f1a")[0]["comp"]["K"]["PhiW"]
            row["khronon_fcap"]["ratio_with_F1A_IC"] = mB / mA
            tab[k] = row
            P(f"[{foot}] k {k}: PhiW(dust R {R:.2f}) {Pd:.4e} [{row['dust']['label']} O {row['dust']['O']:.3f}]; "
              f"khronon f {fcap}: {row['khronon_fcap']['ratio']:.4f} ({row['khronon_fcap']['label']}), H-fixed {row['khronon_fcap_Hfixed']['ratio']:.4f}; "
              f"clock thaw {row['clock_thaw']['ratio']:.2e}; tracker {row['clock_track_lam6.32_noCold']['ratio']:.2e} ({row['clock_track_lam6.32_noCold']['label']}); "
              f"stiff X2 {row['clock_stiff_fullOd_X2']['ratio']:.2e}; uncaptured {row['khr_uncaptured']['ratio']:.2e}; "
              f"non-dust full {row['nondust_full']['extrapolated_at_w0B']:.2e} (lin {row['nondust_full']['linear_check']:.2f}), fcap {row['nondust_fcap']['extrapolated_at_w0B']:.2e}; "
              f"MUTATE-phase {row['MUTATE_phase']['label']} (O {row['MUTATE_phase']['O']:.2f})")
        FO["table"] = tab
        # pre-screen
        def best(key): return max(abs(tab[k][key]["ratio"]) if tab[k][key]["label"] == "still" else 0.0 for k in (0.03, 0.1, 0.3))
        ps = dict(khronon_fcap=best("khronon_fcap"), khronon_fcap_Hfixed=best("khronon_fcap_Hfixed"), clock_thaw=best("clock_thaw"),
                  clock_tracker=best("clock_track_lam6.32_noCold"), stiff_X2=best("clock_stiff_fullOd_X2"), uncaptured=best("khr_uncaptured"),
                  nondust=max(max(abs(tab[k]["nondust_full"]["extrapolated_at_w0B"]), abs(tab[k]["nondust_fcap"]["extrapolated_at_w0B"])) for k in (0.03, 0.1, 0.3)))
        ps["max_still_ratio"] = max(ps.values()); ps["pass_"] = bool(ps["max_still_ratio"] >= 0.5)
        ps["KA_dust_prescreen_pass"] = bool(all(tab[k]["KA_dust_prescreen"]["pass_"] for k in (0.03, 0.1, 0.3)))
        ps["MUTATE_phase_fails_prescreen"] = bool(all(not tab[k]["MUTATE_phase"]["prescreen_pass"] and tab[k]["MUTATE_phase"]["label"] == "follows" for k in (0.03, 0.1, 0.3)))
        FO["prescreen"] = ps
        P(f"[{foot}] PRE-SCREEN D1: max still ratio {ps['max_still_ratio']:.4f} (line 0.5) -> {'PASS' if ps['pass_'] else 'FAIL'}; "
          f"KA-dust prescreen {ps['KA_dust_prescreen_pass']}; MUTATE-phase reads follows and fails: {ps['MUTATE_phase_fails_prescreen']}")
    OUT["runtime_s"] = time.time() - t0; OUT["peak_rss_GB"] = rss()
    P(f"done {OUT['runtime_s']:.0f} s, peak RSS {OUT['peak_rss_GB']:.2f} GB")
    json.dump(OUT, open(os.path.join(HERE, "d1_khronon.json"), "w"), indent=1, default=lambda o: float(o) if isinstance(o, (np.floating,)) else str(o))

if __name__ == "__main__":
    main()
