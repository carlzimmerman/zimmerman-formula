#!/usr/bin/env python3
"""CL5_agn_gas_cycles Part A (see FROZEN_CRITERIA.md): CM1's harness on converged cluster cusps, gas cycles capped by black-hole energy and gas in place.
    python3 cl5_cycles.py setup; python3 cl5_cycles.py run NAME; python3 cl5_cycles.py grade"""
import json, math, os, signal, sys, textwrap
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CM1 = os.path.join(os.path.dirname(HERE), "CM1_outflow_coupling"); sys.path.insert(0, CM1)
import cm1_outflow as C
hern_M, hern_P, EPS = C.hern_M, C.hern_P, C.EPS
S1 = json.load(open(os.path.join(CM1, "cm1_setup.json"))); R1 = S1["rep"]["canonical"]; tu = S1["tunit_Myr"]
G, MSUN, KPC, ERG, CL = C.G_SI, C.MSUN, C.KPC, C.ERG, 2.998e8
rho_c = 3 * R1["M200"] * MSUN / (4 * math.pi * 200 * (R1["R200_kpc"] * KPC) ** 3)
ETAS = {"1e14": 16.91, "1e13": 17.67}; NEED = {k: 14.3 / v for k, v in ETAS.items()}
MG, AG, MS, AS = 0.10, 0.20, 0.0615 * 0.10, 0.05; TOT = 10000.0; dt = 1.0 / tu
# name: (mass, a_f, N, eps_c); eps_c None = no cap (BOUND), N 0 = STATIC
RUNS = dict(M14_e1=("1e14", 0.05, 10, 1.0), M14_e03=("1e14", 0.05, 10, 0.3), M14_e005=("1e14", 0.05, 10, 0.05), M14_N3=("1e14", 0.05, 3, 1.0), M14_N40=("1e14", 0.05, 40, 1.0),
            M14_a002=("1e14", 0.02, 10, 1.0), M14_BOUND=("1e14", AG, 10, None), M14_STATIC=("1e14", 0.05, 0, 0.0),
            M13_e1=("1e13", 0.05, 10, 1.0), M13_e005=("1e13", 0.05, 10, 0.05), M13_STATIC=("1e13", 0.05, 0, 0.0))
def units(m):
    M = float(m); R = (3 * M * MSUN / (4 * math.pi * 200 * rho_c)) ** (1 / 3); EU = G * (M * MSUN) ** 2 / R / ERG
    EA = 0.1 * 0.005 * MS * M * MSUN * CL ** 2 / ERG; return R / KPC, EU, EA / EU
def c_of(eta):
    lo, hi = 2.0, 30.0
    for _ in range(40):
        mid = 0.5 * (lo + hi); e = C.eta_a(C.a_fit_profile(C.M_nfw(mid), 1e-3)); lo, hi = (mid, hi) if e < eta else (lo, mid)
    return 0.5 * (lo + hi)
def e_lift(c, Mf, af):
    mc = math.log1p(c) - c / (1 + c); rs = 1 / c; rg = np.geomspace(1e-6, 3.0, 200001); Pc = -np.log1p(rg / rs) / (mc * rg)
    def U(ag):
        d = np.diff(hern_M(rg, Mf, ag)); rm = 0.5 * (rg[1:] + rg[:-1])
        return -Mf * Mf / (6 * ag) + float(np.sum(d * (hern_P(rm, MS, AS) + hern_P(rm, MG - Mf, AG) + np.interp(rm, rg, Pc))))
    return U(8 * af) - U(af)
def gas_cap(af): return 2 * hern_M(2.414 * af, MG, AG)
def moved(c, EA, af, N, e):
    cap = gas_cap(af); lim = e * EA / N
    if e_lift(c, cap, af) <= lim: return cap, "gas"
    lo, hi = 0.0, cap
    for _ in range(50):
        mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if e_lift(c, mid, af) <= lim else (lo, mid)
    return lo, "energy"
def setup():
    src = open(os.path.join(CM1, "cm1_outflow.py")).read(); body = src.split("    # cold density")[1].split("    xc = float(np.sort(r)[499])")[0]
    old = 'Mb = S["Mb"]; a = S["a_star"]; Mt = Mc + hern_M(rg, Mb, a)'; assert body.count(old) == 1
    body = body.replace(old, "Mt = Mc + hern_M(rg, MS, AS) + hern_M(rg, MG, AG)")
    for m, eta in ETAS.items():
        c = c_of(eta); d = os.path.join(HERE, f"ics_{m}"); os.makedirs(d, exist_ok=True); ns = dict(vars(C)); ns.update(S=dict(), c=c, HERE=d, SEED=1, MS=MS, AS=AS, MG=MG, AG=AG)
        exec(textwrap.dedent("    # cold density" + body), ns); r = np.linalg.norm(ns["pos"], axis=1); xc = float(np.sort(r)[499])
        R, EU, EA = units(m); S = dict(mass=m, eta_t=eta, c=c, xc500=xc, eta_an=C.eta_a(C.a_fit_profile(C.M_nfw(c), xc)), eta_p0=C.eta_p(ns["pos"]), R200_kpc=R, EU_erg=EU, EA=EA, tu=tu)
        json.dump(S, open(os.path.join(d, "setup.json"), "w"), indent=1); print(m, S, flush=True)
def run(name):
    m, af, N, e = RUNS[name]; d = os.path.join(HERE, f"ics_{m}"); S = json.load(open(os.path.join(d, "setup.json"))); I = np.load(os.path.join(d, "cm1_ics.npz"))
    pos, vel, mp = I["pos"].copy(), I["vel"].copy(), float(I["mp"]); xc = S["xc500"]
    if N == 0: Mf, bind, el = 0.0, "none", 0.0
    elif e is None: Mf, bind, el = MG, "no cap", e_lift(S["c"], MG, af)
    else: Mf, bind = moved(S["c"], S["EA"], af, N, e); el = e_lift(S["c"], Mf, af)
    per = TOT / N / tu if N else 0.0; up, dn = 50 / tu, min(400.0, (TOT / N - 50) if N else 400.0) / tu; nst = int(round(TOT / tu / dt)); mark = int(round(1250 / tu / dt))
    def ascale(t):
        if not N: return af
        ph = t % per
        s = (1 - math.cos(math.pi * ph / up)) / 2 if ph < up else (1 + math.cos(math.pi * (ph - up) / dn)) / 2 if ph < up + dn else 0.0
        return af * (1 + 7 * s)
    def Pb(r, ag): return hern_P(r, MS, AS) + hern_P(r, MG - Mf, AG) + hern_P(r, Mf, ag)
    def acc(p, ag):
        r = np.sqrt(np.einsum("ij,ij->i", p, p)); o = np.argsort(r); rank = np.empty(len(r)); rank[o] = np.arange(len(r))
        M = mp * rank + hern_M(r, MS, AS) + hern_M(r, MG - Mf, AG) + hern_M(r, Mf, ag); return -p * (M / (r * r + EPS * EPS) ** 1.5)[:, None], r
    def energy(p, v, ag):
        r = np.sqrt(np.einsum("ij,ij->i", p, p)); q = np.sort(r)
        return 0.5 * mp * float(np.sum(v * v)) - mp * mp * float(np.sum(np.arange(len(q)) / np.sqrt(q * q + EPS * EPS))) + mp * float(np.sum(Pb(r, ag)))
    stop = {"x": False}; signal.signal(signal.SIGTERM, lambda *_: stop.update(x=True))
    ag = ascale(0.0); E0 = energy(pos, vel, ag); W = 0.0; maxerr = 0.0; A, r = acc(pos, ag); marks = [dict(t=0, eta=C.eta_p(pos, xc))]
    res = dict(name=name, mass=m, a_f=af, N=N, eps_c=e, Mf=Mf, bind=bind, lift_each=el, EA=S["EA"], E0=E0, marks=marks, done=False); path = os.path.join(HERE, f"cl5_run_{name}.json")
    for i in range(nst):
        t = i * dt; am, an = ascale(t + dt / 2), ascale(t + dt)
        if am != ag: W += mp * float(np.sum(Pb(r, am) - Pb(r, ag))); A, r = acc(pos, am)
        vel += dt / 2 * A; pos += dt * vel; A, r = acc(pos, am); vel += dt / 2 * A
        if an != am: W += mp * float(np.sum(Pb(r, an) - Pb(r, am))); A, r = acc(pos, an)
        ag = an; k = i + 1
        if k % mark == 0:
            err = abs(energy(pos, vel, ag) - E0 - W) / abs(E0); maxerr = max(maxerr, err); marks.append(dict(t=int(round(k * dt * tu)), eta=C.eta_p(pos, xc), err=err, W=W)); print(name, marks[-1], flush=True)
            res.update(maxerr=maxerr, W=W); json.dump(res, open(path, "w"), indent=1)
        if stop["x"]: print(name, "SIGTERM: partial saved", flush=True); sys.exit(3)
    res.update(done=True, maxerr=maxerr, W=W); json.dump(res, open(path, "w"), indent=1)
def grade():
    L = {k: json.load(open(os.path.join(HERE, f"cl5_run_{k}.json"))) for k in RUNS}; out = []
    def P(s): print(s, flush=True); out.append(s)
    P("CL5 Part A (see FROZEN_CRITERIA.md); kappa = 1/2 FITTED; not theory closed; cold dark energy is a gravitating field, never a particle")
    k1 = True
    for m in ETAS:
        S = json.load(open(os.path.join(HERE, f"ics_{m}", "setup.json"))); st = L[f"M{m[-2:]}_STATIC"]["marks"]; dr = st[-1]["eta"] / st[0]["eta"]; a = abs(S["eta_p0"] / S["eta_an"] - 1) <= 0.05; b = 0.97 <= dr <= 1.03; k1 &= a and b
        P(f"K1 {m}: c {S['c']:.3f}, R200 {S['R200_kpc']:.0f} kpc, x_c {S['xc500']:.4f}, particle eta {S['eta_p0']:.2f} vs analytic {S['eta_an']:.2f}; STATIC {st[0]['eta']:.2f} -> {st[-1]['eta']:.2f}: {'PASS' if a and b else 'FAIL'}; E_AGN {S['EA'] * S['EU_erg']:.2e} erg = {S['EA']:.3f} E_unit")
    k2 = all(q["maxerr"] < 0.01 for q in L.values()); k3 = True; Rs = {}; done = all(q["done"] for q in L.values())
    for k, (m, af, N, e) in RUNS.items():
        if not N: continue
        q = L[k]; es = L[f"M{m[-2:]}_STATIC"]["marks"][-1]["eta"]; Rs[k] = q["marks"][-1]["eta"] / es; used = N * q["lift_each"] / q["EA"]
        if e is not None: k3 &= used <= e * (1 + 1e-6) and q["Mf"] <= gas_cap(af) * (1 + 1e-9)
        P(f"  {k}: a_f {af} N {N} eps_c {e}: M_f {q['Mf']:.5f} ({q['bind']} cap), lift share of E_AGN {used:.3f}, net work {q['W']:.3e}, err {q['maxerr']:.1e}: R {Rs[k]:.3f} ({'reaches' if Rs[k] <= NEED[m] else 'misses'}, need {NEED[m]:.3f}); by 1250 Myr " + " ".join(f"{x['eta'] / L[f'M{m[-2:]}_STATIC']['marks'][i]['eta']:.3f}" for i, x in enumerate(q["marks"])))
    P(f"K2 work balance: {'PASS' if k2 else 'FAIL'}; K3 caps: {'PASS' if k3 else 'FAIL'}; all done: {done}")
    a, b_, c_ = Rs["M14_e1"], Rs["M14_e03"], Rs["M14_e005"]; mu = b_ >= a - 0.03 and c_ >= b_ - 0.03; sens = abs(1 - Rs["M14_BOUND"]) > 0.03
    P(f"MUTATE monotonic 1e14 N 10: eps 1 {a:.3f}, 0.3 {b_:.3f}, 0.05 {c_:.3f}: {'PASS' if mu else 'FAIL'}; BOUND R {Rs['M14_BOUND']:.3f}, moved > 0.03: {'PASS' if sens else 'FAIL'}")
    ok = k1 and k2 and k3 and mu and sens and done; hit = lambda m, f: any(Rs[k] <= NEED[m] for k, v in RUNS.items() if v[0] == m and v[2] and v[3] is not None and f(v[3]))
    v = "NOT DECIDED" if not ok else "REACHES AT REALISTIC COUPLING" if Rs["M14_e005"] <= NEED["1e14"] and Rs["M13_e005"] <= NEED["1e13"] else "CEILING ONLY" if all(hit(m, lambda e: e > 0.05) for m in ETAS) else "NOT REACHED AT CEILING" if not all(hit(m, lambda e: True) for m in ETAS) else "MIXED"
    P(f"VERDICT Part A: {v}")
    open(os.path.join(HERE, "cl5_A.out"), "w").write("\n".join(out) + "\n"); json.dump(dict(R=Rs, need=NEED, verdict=v, K1=k1, K2=k2, K3=k3, mutate=mu, sens=sens), open(os.path.join(HERE, "cl5_A_results.json"), "w"), indent=1)
if __name__ == "__main__":
    {"setup": setup, "grade": grade}[sys.argv[1]]() if sys.argv[1] != "run" else run(sys.argv[2])
