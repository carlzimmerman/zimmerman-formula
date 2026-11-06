#!/usr/bin/env python3
"""AC12: is the Sun's own charged khronon halo carried with the Sun? v3s (s = 0) and AC2q side by side.

Criteria: FROZEN_CRITERIA.md (4db782ee4e). Geometric units G = c = 1 (K = 4 pi) inside the formulas, SI for reporting.
Run from the repo root:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC12_comoving_halo/ac12.py
AC12_MUTATE=1 flips the q' u' transport term (KA2 must then fail). kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys, json, math, time, hashlib, resource
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from sympy.calculus.euler import euler_equations

T0 = time.monotonic()
MUT = os.environ.get("AC12_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
OUT, CHK = [], {}
RES = {"lane": "AC12_comoving_halo", "criteria": "4db782ee4e", "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), detail=str(detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


P("AC12  co-moving solar halo" + ("  [MUTATE: q' u' sign flipped]" if MUT else ""))

# ================================================= H0: sigma Euler-Lagrange from P.grad Xi is charge continuity
t, x, y, z = Xs = sp.symbols("t x y z", real=True)
sig = sp.Function("sigma")(*Xs); Pf = [sp.Function(f"P{i}")(*Xs) for i in range(3)]; phi = sp.Function("phi")(*Xs)
xs3 = (x, y, z)
Xi = phi - sp.diff(sig, t) + sum(sp.diff(sig, v) ** 2 for v in xs3) / 2
L = sum(Pf[i] * sp.diff(Xi, xs3[i]) for i in range(3))
(el,) = euler_equations(L, [sig], Xs)
q = sum(sp.diff(Pf[i], xs3[i]) for i in range(3))
vv = [-sp.diff(sig, w) for w in xs3]                        # v = -grad sigma
cont = sp.diff(q, t) + sum(sp.diff(q * vv[i], xs3[i]) for i in range(3))
r0 = sp.simplify(sp.expand(el.lhs) - cont); r1 = sp.simplify(sp.expand(el.lhs) + cont)
check("H0", r0 == 0 or r1 == 0, f"sigma-EL of P.grad Xi = +/-(d_t q + div(q v)), v = -grad sigma: residuals {r0 if r0 == 0 else r1}")

# ================================================= AC11's on-region system (reimplemented verbatim) for Omega'^2
K, s, Mt, k, om = sp.symbols("K s M_theta k omega", positive=True)
gL = sp.Symbol("gamma_L", positive=True); d0 = sp.Symbol("rho0", positive=True); W2 = sp.Symbol("W2", positive=True)
dphi, dsig, dXi, drb = sp.symbols("dphi dsigma dXi drho_b"); dP = sp.symbols("dP0:3")


def system(gam_):
    dPz = dP[2]
    dC2 = s ** 2 * (-2 * sp.I * om * dsig - 2 * dphi)
    dD = sp.I * k * dPz
    Peq_ = sp.I * k * dXi - K * Mt * dPz - gam_ * k ** 2 * dPz + sp.I * gam_ * k * dC2
    drt = (1 - 2 * gam_ * s ** 2) * dD + s ** 2 * (1 - 2 * gam_ * d0) * (-sp.I * om * dsig - 2 * dphi)
    rx0 = d0 + s ** 2 * (1 - 2 * gam_ * d0)
    ce = -sp.I * om * drt + rx0 * k ** 2 * dsig
    pois = -k ** 2 * dphi - K * ((1 - 2 * gam_ * s ** 2) * dD + s ** 2 * (1 - 2 * gam_ * d0) * (-2 * sp.I * om * dsig - 3 * dphi)) - K * drb
    be = dXi - (dphi + sp.I * om * dsig)
    unk = [dphi, dsig, dXi, dPz]
    Am, bm = sp.linear_eq_to_matrix([pois, ce, be, Peq_], unk)
    det = sp.expand(Am.det(method="berkowitz"))
    xa = [sp.expand(v) for v in (Am.adjugate() * bm)]
    sub = dict(zip(unk, xa))
    return sp.cancel(sp.expand(drt.subs(sub)) / (det * drb))


Tr = sp.cancel(system(gL).subs(om, sp.sqrt(W2)))
den = sp.expand(sp.fraction(Tr)[1])
(Om2,) = sp.solve(sp.Eq(den, 0), W2)
fOm2 = sp.lambdify((K, d0, Mt, gL, s, k), Om2, "mpmath")

# ================================================= inputs (AZ37 / AC11)
cl = 2.99792458e8; PC = 3.0856775814913673e16; AU = 1.495978707e11; G = 6.67430e-11; MSUN = 1.98847e30
GMs = 1.32712440018e20
inputs = {"canonical": dict(a0=9.3603e-11, rho=0.0447, xe=1.15, lengths=(21.68, 24., 27.)),
          "alt": dict(a0=1.1312e-10, rho=0.0514, xe=2.6, lengths=(22.85, 24., 24.60))}
VS = (220e3, 369e3)
AC11 = json.load(open(os.path.join(ROOT, "action_search_2026_11_05/AC11_moving_sun/ac11.json")))


def cph(rho_local_geo, mt, gl, sval, rr):
    kk = 1 / rr
    O2 = float(fOm2(4 * math.pi, rho_local_geo, mt, gl, sval, kk))
    return (math.sqrt(O2) * cl / kk) if O2 > 0 else float("nan")


# ================================================= H1: the co-motion ODE in x = r / r_eq, y1 = u, y2 = x u'
def halo_solve(eps, halo=True, x0=1e-7, rtol=1e-10, atol=1e-12, xmax=200.0, mutate=MUT, dense=True):
    sg = -1.0 if mutate else 1.0

    def rhs(tt, Y):
        xx = math.exp(tt)
        if halo:
            xq = -1.0 / (xx * (1 + eps) + 1.0)                # x q'/q for q = (1+eps) + 1/x
        else:
            xq = 0.0
        return [Y[1], -(1 + sg * xq) * Y[1] + 2 * Y[0]]
    if halo:
        p = (math.sqrt(3) - 1) if mutate else math.sqrt(2)
    else:
        p = 1.0
    sol = solve_ivp(rhs, (math.log(x0), math.log(xmax)), [x0 ** p, p * x0 ** p], method="DOP853",
                    rtol=rtol, atol=atol * x0 ** p, dense_output=dense)
    return sol


def alpha_of(sol, xx):
    y1, y2 = sol.sol(math.log(xx))
    return (2 * y1 + y2) / (3 * xx)


def fvals(sol, alpha, xx):
    y1, y2 = sol.sol(math.log(xx))
    return max(abs(y2 / xx), abs(y1 / xx)) / abs(alpha), (y1 / (-alpha), y2 / (-alpha))


def Bvalue(sol, alpha, xx, eps, halo=True):
    """max over theta of |grad(|w|^2/2)| in units V^2/r_eq, w = V grad(u cos theta), u normalized to -x at infinity."""
    y1, y2 = [c / (-alpha) for c in sol.sol(math.log(xx))]
    u = y1; up = y2 / xx
    xq = (-1.0 / (xx * (1 + eps) + 1.0)) if halo else 0.0
    sg = -1.0 if MUT else 1.0
    upp = (-(1 + sg * xq) * y2 + 2 * y1 - y2) / xx ** 2       # x^2 u'' = d(y2)/dt - y2
    a, b = up, u / xx
    ap, bp = upp, (a - b) / xx
    best = 0.0
    for th in np.linspace(0, math.pi, 721):
        c_, s_ = math.cos(th), math.sin(th)
        gr = a * ap * c_ ** 2 + b * bp * s_ ** 2
        gt = (b * b - a * a) * s_ * c_ / xx
        best = max(best, math.hypot(gr, gt))
    return best


# known answer KA1 (halo off): u = -x exactly
s_off = halo_solve(0.0, halo=False)
a_off = alpha_of(s_off, 100.0)
f_off = [fvals(s_off, a_off, xx)[0] for xx in (1e-3, 1e-1, 1.0, 10.0)]
check("KA1_f", all(abs(v - 1) < 1e-9 for v in f_off), f"halo off: f = {f_off} (exactly 1: relative flow = V everywhere)")

# KA2 inner slope
sol_ref = halo_solve(0.0)
xa, xb = 1e-6, 1e-5
slope = (math.log(fvals(sol_ref, 1.0, xb)[0]) - math.log(fvals(sol_ref, 1.0, xa)[0])) / math.log(xb / xa)
check("KA2", abs(slope - (math.sqrt(2) - 1)) <= 1e-3, f"inner log-slope of f = {slope:.6f} vs sqrt(2) - 1 = {math.sqrt(2) - 1:.6f}")

# fit quality and convergence
alphas = [alpha_of(sol_ref, xx) for xx in np.linspace(50, 200, 31)]
fit_res = (max(alphas) - min(alphas)) / abs(np.mean(alphas))
check("H1_fit", fit_res <= 1e-4, f"alpha from two-term fit varies by {fit_res:.2e} relative over x in [50, 200] (line 1e-4)")
alpha_ref = float(np.mean(alphas))
# diagnostic (not frozen; reported): far fit on [2e3, 1e4]
sol_far = halo_solve(0.0, xmax=1e4)
alphas_far = [alpha_of(sol_far, xx) for xx in np.linspace(2e3, 1e4, 31)]
alpha_far = float(np.mean(alphas_far)); far_res = (max(alphas_far) - min(alphas_far)) / abs(alpha_far)
P(f"  diagnostic (post-freeze, reported): far fit alpha on [2e3, 1e4] = {alpha_far:.8e} (spread {far_res:.1e}) vs [50, 200] {alpha_ref:.8e}"
  f" (rel {abs(alpha_far / alpha_ref - 1):.1e})")
RES["alpha"] = dict(fit_50_200=alpha_ref, spread_50_200=fit_res, fit_2e3_1e4=alpha_far, spread_far=far_res)

H = {}
conv_worst = 0.0
for foot, p in inputs.items():
    rho_geo = G * p["rho"] * MSUN / PC ** 3 / cl ** 2
    ag = p["a0"] / cl ** 2; s2v = 8 * ag ** 2; mt = (1 + p["xe"]) ** 2
    rows = []
    for Lpc in p["lengths"]:
        gl = 4 * math.pi * (Lpc * PC) ** 2 / 2
        r_eq = GMs / cl ** 2 / gl / rho_geo                  # metres (geometric length)
        for model, sval in (("v3s", 0.0), ("AC2q", math.sqrt(s2v))):
            eps = sval ** 2 / rho_geo
            sols = [halo_solve(eps, x0=x0_, rtol=rt, atol=at, xmax=1e4)
                    for x0_ in (1e-7, 1e-8) for (rt, at) in ((1e-10, 1e-12), (1e-12, 1e-13))]
            als = [float(np.mean([alpha_of(so, xx) for xx in np.linspace(50, 200, 31)])) for so in sols]
            pts = {"1AU": AU, "9.58AU": 9.58 * AU, "r_eq": r_eq}
            row = dict(model=model, Lstar_pc=Lpc, r_eq_AU=r_eq / AU, eps=eps, pts={})
            for nm, rr in pts.items():
                xx = rr / r_eq
                fs = [fvals(so, al, xx)[0] for so, al in zip(sols, als)]
                conv = (max(fs) - min(fs)) / fs[0]; conv_worst = max(conv_worst, conv)
                f_ = fs[-1]; al = als[-1]; so = sols[-1]
                q_loc = rho_geo * (1 + r_eq / rr)                # Sun's halo + Galactic (s^2 enters via system's rx0)
                c_loc = cph(q_loc, mt, gl, sval, rr)
                c_gal = cph(rho_geo, mt, gl, sval, rr)
                vK = math.sqrt(GMs / rr)
                Bd = Bvalue(so, al, xx, eps)                      # units V^2 / r_eq
                cells = []
                for V in VS:
                    Bv = V ** 2 / r_eq * Bd / (GMs / rr ** 2)
                    Mach = f_ * V / c_loc
                    cells.append(dict(V=V, rel_flow_m_s=f_ * V, Mach=Mach, pole_cosine=(1 / Mach) if Mach > 1 else None, B=Bv))
                row["pts"][nm] = dict(x=xx, f=f_, conv=conv, c_ph_local=c_loc, c_ph_galactic_only=c_gal, v_Kepler=vK, cells=cells)
            rows.append(row)
            P(f"  [{foot} {model} Lstar {Lpc} pc] r_eq {r_eq / AU:.0f} AU")
            for nm, d in row["pts"].items():
                cs = "; ".join(f"V {c['V'] / 1e3:.0f}: w {c['rel_flow_m_s'] / 1e3:.2f} km/s Mach {c['Mach']:.3g} B {c['B']:.3g}" for c in d["cells"])
                P(f"     {nm:6s} f {d['f']:.5f}  c_ph local {d['c_ph_local']:.1f} m/s (Galactic-only {d['c_ph_galactic_only']:.1f}; "
                  f"v_K {d['v_Kepler']:.0f})  {cs}")
    H[foot] = rows
RES["H"] = H
check("H1_conv", conv_worst <= 1e-6, f"f over two x0 and two rtol pairs: max relative spread {conv_worst:.2e} (line 1e-6)")

# KA1 phase speeds: halo off (q = rho0) at 1 and 9.58 AU, s = 0, against AC11's stored ac11.json
ka_err = 0.0; nka = 0
for foot, p in inputs.items():
    rho_geo = G * p["rho"] * MSUN / PC ** 3 / cl ** 2; mt = (1 + p["xe"]) ** 2
    for row in AC11["B2"][foot]:
        if row["s"] != 0.0 or not row.get("real_phase_speed"):
            continue
        gl = 4 * math.pi * (row["Lstar_pc"] * PC) ** 2 / 2
        c_ = cph(rho_geo, mt, gl, 0.0, row["r_AU"] * AU)
        ka_err = max(ka_err, abs(c_ / row["phase_speed_m_s"] - 1)); nka += 1
check("KA1_cph", ka_err <= 1e-9, f"halo off, s = 0: phase speeds vs AC11 ac11.json on {nka} rows, max rel diff {ka_err:.1e} (line 1e-9)")

# H4 bounds (reported)
H4 = {}
for foot, p in inputs.items():
    rho_si = p["rho"] * MSUN / PC ** 3
    out = {}
    for nm, rr in (("1AU", AU), ("9.58AU", 9.58 * AU)):
        tidal = (4 * math.pi / 3) * 2 * rho_si * rr ** 3 / MSUN
        Bmax = max(c["B"] for row in H[foot] for c in row["pts"][nm]["cells"])
        Lmin = min(p["lengths"]) * PC
        metric = max(Bmax, 1.0) * 2 * rr ** 2 / Lmin ** 2
        out[nm] = dict(tidal_bound_rel=tidal, flow_charge_metric_rel=metric, Bmax=Bmax)
        P(f"  H4 [{foot}] {nm}: matching-region tide <= {tidal:.2e} g_N; flow-induced charge metric effect <= {metric:.2e} g_N (B max {Bmax:.3g})")
    H4[foot] = out
RES["H4"] = H4

# ================================================= labels per footing / model / Lstar
labels = {}
for foot in inputs:
    for row in H[foot]:
        d1 = row["pts"]["1AU"]
        sub_ok = all(c["Mach"] < 1 for c in d1["cells"])
        B_ok = all(c["B"] < 0.1 for c in d1["cells"])
        if any(math.isnan(row["pts"][n]["c_ph_local"]) for n in row["pts"]):
            lab = "FAIL CANDIDATE (imaginary c_ph with q > 0)"
        elif sub_ok and B_ok:
            lab = "CO-MOVING SUBSONIC CORE at 1 AU"
        else:
            parts = []
            if not sub_ok:
                parts.append("SUPERSONIC at 1 AU")
            if not B_ok:
                parts.append("KINEMATICS NOT SELF-CONSISTENT at 1 AU")
            lab = "; ".join(parts)
        sup958 = any(c["Mach"] > 1 for c in row["pts"]["9.58AU"]["cells"])
        supeq = any(c["Mach"] > 1 for c in row["pts"]["r_eq"]["cells"])
        Bbad958 = any(c["B"] >= 0.1 for c in row["pts"]["9.58AU"]["cells"])
        key = f"{foot}/{row['model']}/{row['Lstar_pc']}"
        labels[key] = dict(at_1AU=lab, supersonic_9p58AU=sup958, supersonic_r_eq=supeq, B_ge_0p1_9p58AU=Bbad958)
        P(f"  LABEL {key}: 1 AU {lab}; 9.58 AU supersonic {sup958}, B>=0.1 {Bbad958}; r_eq supersonic {supeq}")
RES["labels"] = labels
RES["moving_sun_label"] = "NO VERDICT (AZ37 lines: no full nonlinear moving branch solved)"
P(f"MOVING-SUN LABEL: {RES['moving_sun_label']}" + ("  [MUTATE: KA2 must FAIL]" if MUT else ""))
srcs = [os.path.join(HERE, "ac12.py"), os.path.join(HERE, "FROZEN_CRITERIA.md"),
        os.path.join(ROOT, "action_search_2026_11_05/AC11_moving_sun/ac11.py"),
        os.path.join(ROOT, "action_search_2026_11_05/AC11_moving_sun/ac11.json")]
RES["sources"] = {os.path.relpath(q_, ROOT): hashlib.sha256(open(q_, "rb").read()).hexdigest() for q_ in srcs}
RES["seconds"] = time.monotonic() - T0
RES["peak_rss_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
with open(os.path.join(HERE, f"ac12{TAG}.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
with open(os.path.join(HERE, f"ac12{TAG}.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
