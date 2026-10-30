#!/usr/bin/env python3
"""CM2_gas_rich_past: closed-box gas history capped by SN energy on CM1's formed cusp (CM1 setup and ICs read-only).
    python3 cm2_gas_rich.py run K1|C40|C10|MUTATE
    python3 cm2_gas_rich.py grade"""
import json, math, os, signal, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CM1 = os.path.join(os.path.dirname(HERE), "CM1_outflow_coupling"); sys.path.insert(0, CM1)
import cm1_outflow as C
S = json.load(open(os.path.join(CM1, "cm1_setup.json"))); RC = S["rep"]["canonical"]
Mb, Mg0, a, tu, xc = S["Mb"], S["Mg"], S["a_star"], S["tunit_Myr"], S["xc500"]; Mstar = Mb - Mg0
ESN = 0.5 * RC["L36"] / 100 * 1e51; EU = S["Eunit_erg"]; TOT = 10000.0; EPS = C.EPS
CFG = dict(K1=(40, 250.0, None), C40=(40, 250.0, 1.0), C10=(10, 1000.0, 1.0), MUTATE=(10, 1000.0, 0.01))
lift = lambda m: C.e_lift(S, m) * EU if m > 0 else 0.0

def schedule(N, cap):
    out = []
    for k in range(N):
        Mk = Mg0 + Mstar * (1 - k / N)
        if cap is None: out.append((Mg0, Mk)); continue
        lim = cap * ESN / N
        if lift(Mk) <= lim: out.append((Mk, Mk)); continue
        lo, hi = 0.0, Mk
        for _ in range(60):
            mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if lift(mid) <= lim else (lo, mid)
        out.append((lo, Mk))
    return out

def run(mode):
    N, per_my, cap = CFG[mode]; sch = schedule(N, cap); per = per_my / tu; up, dn = 5 / tu, 200 / tu
    I = np.load(os.path.join(CM1, "cm1_ics.npz")); pos, vel, mp = I["pos"].copy(), I["vel"].copy(), float(I["mp"])
    dt = 0.5 / tu; nst = int(round((1250 if mode == "K1" else TOT) / tu / dt)); mark = int(round(1250 / tu / dt))
    def state(t):
        k = min(int(t / per + 1e-9), N - 1); ph = t - k * per
        s = (1 - math.cos(math.pi * ph / up)) / 2 if ph < up else (1 + math.cos(math.pi * (ph - up) / dn)) / 2 if ph < up + dn else 0.0
        return sch[k][0], a * (1 + 7 * s)
    def Pb(r, Mf, ag): return C.hern_P(r, Mb - Mf, a) + C.hern_P(r, Mf, ag)
    def acc(p, Mf, ag):
        r = np.sqrt(np.einsum("ij,ij->i", p, p)); o = np.argsort(r); rank = np.empty(len(r)); rank[o] = np.arange(len(r))
        M = mp * rank + C.hern_M(r, Mb - Mf, a) + C.hern_M(r, Mf, ag); return -p * (M / (r * r + EPS * EPS) ** 1.5)[:, None], r
    def energy(p, v, Mf, ag):
        r = np.sqrt(np.einsum("ij,ij->i", p, p)); q = np.sort(r)
        return 0.5 * mp * float(np.sum(v * v)) - mp * mp * float(np.sum(np.arange(len(q)) / np.sqrt(q * q + EPS * EPS))) + mp * float(np.sum(Pb(r, Mf, ag)))
    stop = {"x": False}; signal.signal(signal.SIGTERM, lambda *_: stop.update(x=True))
    Mf, ag = state(0.0); E0 = energy(pos, vel, Mf, ag); W = 0.0; maxerr = 0.0; A, r = acc(pos, Mf, ag); marks = [dict(t=0, eta=C.eta_p(pos, xc))]
    res = dict(mode=mode, N=N, per=per_my, schedule=sch, lift_erg=[lift(m[0]) for m in sch], E_SN=ESN, E0=E0, marks=marks, done=False)
    path = os.path.join(HERE, f"cm2_run_{mode}.json")
    for i in range(nst):
        t = i * dt; Mm, am = state(t + dt / 2); Mn, an = state(t + dt)
        if (Mm, am) != (Mf, ag): W += mp * float(np.sum(Pb(r, Mm, am) - Pb(r, Mf, ag))); A, r = acc(pos, Mm, am)
        vel += dt / 2 * A; pos += dt * vel; A, r = acc(pos, Mm, am); vel += dt / 2 * A
        if (Mn, an) != (Mm, am): W += mp * float(np.sum(Pb(r, Mn, an) - Pb(r, Mm, am))); A, r = acc(pos, Mn, an)
        Mf, ag = Mn, an; k = i + 1
        if k % mark == 0:
            err = abs(energy(pos, vel, Mf, ag) - E0 - W) / abs(E0); maxerr = max(maxerr, err)
            marks.append(dict(t=int(round(k * dt * tu)), eta=C.eta_p(pos, xc), err=err, W=W)); print(mode, marks[-1], flush=True)
            res.update(maxerr=maxerr, W=W); json.dump(res, open(path, "w"), indent=1)
        if stop["x"]: print(mode, "SIGTERM: partial saved", flush=True); sys.exit(3)
    res.update(done=True, maxerr=maxerr, W=W); json.dump(res, open(path, "w"), indent=1)

def grade():
    L = lambda m: json.load(open(os.path.join(HERE, f"cm2_run_{m}.json"))); R = {m: L(m) for m in CFG}
    st = json.load(open(os.path.join(CM1, "cm1_run_STATIC.json")))["marks"]; es = st[-1]["eta"]; prim = json.load(open(os.path.join(CM1, "cm1_run_PRIMARY.json")))["marks"]
    out = []; 
    def P(s): print(s, flush=True); out.append(s)
    P("CM2 gas-rich past (see FROZEN_CRITERIA.md); kappa = 1/2 FITTED; not theory closed; cold dark energy is a gravitating field, never a particle")
    k1 = R["K1"]["marks"][1]["eta"] == prim[1]["eta"]; P(f"K1 eta at 1250 Myr {R['K1']['marks'][1]['eta']:.3f} vs CM1 PRIMARY {prim[1]['eta']:.3f}: {'PASS' if k1 else 'FAIL'}")
    k2 = all(R[m]["maxerr"] < 0.01 for m in CFG); P("K2 work balance: " + ", ".join(f"{m} {R[m]['maxerr']:.1e}" for m in CFG) + f": {'PASS' if k2 else 'FAIL'}")
    k3 = True; Rs = {}; eu = {}
    for m in ("C40", "C10", "MUTATE"):
        q = R[m]; cap = CFG[m][2]; eu[m] = sum(q["lift_erg"]) / q["E_SN"]; k3 &= eu[m] <= cap * (1 + 1e-9) and all(f <= g for f, g in q["schedule"])
        Rs[m] = [x["eta"] / st[i]["eta"] for i, x in enumerate(q["marks"])]; f = [s[0] for s in q["schedule"]]
        P(f"  {m}: R by 1250 Myr " + " ".join(f"{v:.3f}" for v in Rs[m]) + f"; moved mass first/median/last {f[0]:.4f}/{np.median(f):.4f}/{f[-1]:.4f}; eps_used {eu[m]:.3f}; net work {q['W']:.3e}")
    P(f"K3 energy and gas caps: {'PASS' if k3 else 'FAIL'}")
    rc40, rc10, rm = Rs["C40"][-1], Rs["C10"][-1], Rs["MUTATE"][-1]; mp_ = abs(1 - rm) < 0.5 * abs(1 - rc10); P(f"MUTATE R {rm:.3f} vs C10 {rc10:.3f}: {'PASS' if mp_ else 'FAIL'}")
    hit = (rc40 <= C.NEED, rc10 <= C.NEED); ok = k1 and k2 and k3 and mp_ and all(R[m]["done"] for m in CFG)
    v = "NOT DECIDED" if not ok else "REACHED AT BOTH CADENCES" if all(hit) else "CADENCE-DEPENDENT" if any(hit) else "NOT REACHED AT CEILING"
    P(f"VERDICT (needed R <= {C.NEED:.3f}): C40 R {rc40:.3f}, C10 R {rc10:.3f}: {v}")
    open(os.path.join(HERE, "cm2.out"), "w").write("\n".join(out) + "\n"); json.dump(dict(R=Rs, eps_used=eu, verdict=v), open(os.path.join(HERE, "cm2_results.json"), "w"), indent=1)

if __name__ == "__main__":
    run(sys.argv[2]) if sys.argv[1] == "run" else grade()
