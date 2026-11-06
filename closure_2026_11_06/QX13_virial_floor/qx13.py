#!/usr/bin/env python3
"""QX13 iter_1 (FROZEN_CRITERIA.md, 5584787fbd): virial-shock-heated sector with an entropy floor.
gamma = 5/3, isentropic per host, K = max(K_sh, K_0). K_sh from the strong-shock jump at r_sh = r_ta/2 (upstream rho_sea
in free fall from r_ta). Floor c_min from galaxy gates G5/G6/G7 only; X-COP + groups predicted. Hosts and grader are
QX12 iter_3's (read-only import); only the solver is replaced.
    python3 qx13.py [--workers 4]   -> qx13.json/.out
    python3 qx13.py --mutate        -> qx13_MUTATE.json/.out  (M1 floor off, M2 heating off, M3 K x 1e-4)
kappa = 1/2 FITTED; not theory closed; footings never pooled. Units kpc, Msun, km/s."""
import os, sys, json, math, runpy, io, contextlib
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
MUT = "--mutate" in sys.argv; TAG = "qx13_MUTATE" if MUT else "qx13"
WK = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
I3 = os.path.join(REPO, "closure_2026_11_06", "QX12_triangle", "iter_3_isothermal_sea", "qx12_i3.py")
argv0 = sys.argv; sys.argv = [I3]
with contextlib.redirect_stdout(io.StringIO()):
    L3 = runpy.run_path(I3, run_name="qx12_i3_lib")
sys.argv = argv0
GK, glaw, A0K, RHO_D0, BASE = L3["GK"], L3["glaw"], L3["A0K"], L3["RHO_D0"], L3["BASE"]
pointmass = L3["pointmass"]

MODE = dict(heat=True, floor=True, kfac=1.0)       # mutated per job


def solve_poly(Mb_fn, M_cap, c2, rta, a0k, law=True, host=True, rho_sea=RHO_D0, n=900, rmin=1e-3):
    """c2 = c_0^2 (floor sound speed of the sea today). Same signature/return as QX12 iter_3's solve_iso."""
    r = np.geomspace(rmin, rta, n); lr = np.log(r)
    Mb = np.array([Mb_fn(x) for x in r]) if host else np.zeros(n)
    dr = np.diff(r); shell = 4 * math.pi * r ** 2
    Msea = 4 / 3 * math.pi * rho_sea * r ** 3
    Md = Msea.copy(); rsh = 0.5 * rta
    K0 = (0.6 * c2 / rho_sea ** (2 / 3)) if MODE["floor"] else 0.0
    err = 1.0; info = {}
    for it in range(4000):
        gN = GK * (Mb + Md - Msea) / r ** 2
        g = glaw(gN, a0k) if law else gN
        Hc = np.concatenate([np.cumsum((0.5 * (g[1:] + g[:-1]) * dr)[::-1])[::-1], [0.0]])     # int_r^{r_ta} g
        Hsh = float(np.interp(math.log(rsh), lr, Hc))
        Ksh = (0.75 * rho_sea * 2 * Hsh) / (4 * rho_sea) ** (5 / 3) if MODE["heat"] else 0.0
        if Ksh >= K0 and Ksh > 0:
            K = Ksh * MODE["kfac"]; wsh = 2.5 * Ksh * (4 * rho_sea) ** (2 / 3)
            info["ka2"] = abs(wsh / (15 / 16 * Hsh) - 1) if Hsh > 0 else 0.0
            # inside r_sh: boundary rho(r_sh) = 4 rho_sea, enthalpy w = (5/2) K rho^(2/3) + int_r^{r_sh} g
            rho = ((4 * rho_sea) ** (2 / 3) + 2 * np.maximum(Hc - Hsh, 0.0) / (5 * K)) ** 1.5
            rho = np.where(r <= rsh, rho, rho_sea); case = "shock"
        elif K0 > 0:
            K = K0 * MODE["kfac"]                                    # open contact with the sea at r_ta
            rho = (rho_sea ** (2 / 3) + 2 * Hc / (5 * K)) ** 1.5; case = "floor"
        else:
            rho = np.full(n, rho_sea); case = "none"
        seg = 0.5 * (shell[1:] * rho[1:] + shell[:-1] * rho[:-1]) * dr
        mc = np.cumsum(np.concatenate([[4 / 3 * math.pi * r[0] ** 3 * rho[0]], seg]))
        if M_cap is not None and mc[-1] > M_cap:
            new = mc / mc[-1] * M_cap; capped = True
        else:
            new = mc; capped = False
        err = float(np.max(np.abs(new - Md)) / max(np.max(new), 1e-300))
        Md = 0.5 * Md + 0.5 * new
        if err < 1e-7 and it > 5: break
    return dict(r=r, Md=new - Msea, capped=capped, its=it, err=err, conv=bool(err < 1e-7), case=case, Ksh=Ksh, K0=K0,
                ka2=info.get("ka2", 0.0))


grade = L3["grade"]
grade.__globals__["solve_iso"] = solve_poly     # runpy returns a copy of the globals; patch grade's own namespace


def job(arg):
    f, c, kw, mode = arg
    MODE.update(mode)
    return f, c, mode, grade(c, A0K[f], BASE[f], **kw)


def jeans_cmax():
    """Largest adiabatic floor c_0 (km/s) with comoving k_J >= 50 /Mpc for every z in [10, 3400] (QX10 J0)."""
    Gm = 4.30091e-9                                                   # Mpc (km/s)^2 / Msun
    rho_crit_h = 3 * 100.0 ** 2 / (8 * math.pi * Gm)                  # Msun/Mpc^3 per h^2
    om, orad = 0.0215 + 0.11958060485606123, 4.15e-5
    worst = math.inf
    for z in np.geomspace(11, 3401, 4000) - 1:
        rho = rho_crit_h * (om * (1 + z) ** 3 + orad * (1 + z) ** 4)
        # c_s(z) = c0 (1+z); lambda_phys = c_s sqrt(pi/(G rho)); k_com = 2 pi (1+z)^-1 / lambda_phys... comoving: k = 2 pi a / lambda_phys
        lam_per_c0 = (1 + z) * math.sqrt(math.pi / (Gm * rho))          # Mpc per (km/s), physical
        kcom_per = 2 * math.pi / ((1 + z) * lam_per_c0)                  # k_com = a 2pi/lambda, a = 1/(1+z)
        worst = min(worst, kcom_per / 50.0)                              # c0 <= kcom_per/50
    return worst


if __name__ == "__main__":
    OUT = []
    def P(s=""): print(s, flush=True); OUT.append(str(s))
    RES = dict(lane="QX13 iter_1", criteria="5584787fbd", mutate=MUT, note="kappa = 1/2 FITTED; not theory closed")
    P(f"QX13 iter_1 ({'MUTATE' if MUT else 'main'}): virial-shock sector with entropy floor, gamma 5/3. kappa = 1/2 FITTED; not theory closed.")
    base_mode = dict(heat=True, floor=True, kfac=1.0)
    grid = [0.0] + list(np.geomspace(1.0, 3000.0, 60))
    if not MUT:
        MODE.update(dict(heat=True, floor=True, kfac=1.0))
        s = solve_poly(pointmass(0.0), None, 3000.0 ** 2, 1000.0, 1.0, law=False, host=False)
        ka1 = float(np.max(np.abs(s["Md"] / (4 / 3 * math.pi * RHO_D0 * s["r"] ** 3))))
        RES["KA1"] = ka1; P(f"KA1 uniform sea (no host, c0 3000): max rel {ka1:.2e} -> {'PASS' if ka1 <= 1e-4 else 'FAIL'}")
        with Pool(WK) as pool:
            rows = pool.map(job, [(f, float(c), {}, base_mode) for f in A0K for c in grid])
            rows_v = pool.map(job, [(f, float(c), dict(variant=True), base_mode) for f in A0K for c in grid])
            ka3 = {f: o for f, c, m, o in pool.map(job, [(f, 100.0, dict(Rfac=0.0), base_mode) for f in A0K])}
        RES["KA3"] = {f: ka3[f]["X_mean"] for f in A0K}
        ka3ok = all(abs(RES["KA3"][f] - (0.4675 if f == "canonical" else 0.4345)) <= 2e-3 for f in A0K)
        P(f"KA3 (R = 0): X-COP {RES['KA3']['canonical']:+.4f} / {RES['KA3']['alt']:+.4f} -> {'PASS' if ka3ok else 'FAIL'}")
        # KA2 on representative hosts: shock identity
        MODE.update(base_mode); ka2 = []
        for nm, Mb, Ro in L3["G5SYS"][:3]:
            ss = solve_poly(L3["expdisc"](Mb, Ro), L3["FCAP"] * L3["R"] * Mb, 0.0, L3["r_ta"](Mb), A0K["canonical"]); ka2.append(ss["ka2"])
        RES["KA2"] = max(ka2); P(f"KA2 shock identity w_sh = (15/16) H_sh: max rel {RES['KA2']:.1e} -> {'PASS' if RES['KA2'] <= 1e-10 else 'FAIL'}")
        RES["scan"] = {f: [dict(c=c, **o) for ff, c, m, o in rows if ff == f] for f in A0K}
        RES["scan_variant"] = {f: [dict(c=c, **o) for ff, c, m, o in rows_v if ff == f] for f in A0K}
        cmaxJ = jeans_cmax(); RES["J0_c0_max_adiabatic"] = cmaxJ
        P(f"T1/J0: adiabatic floor allowed only for c0 <= {cmaxJ:.3g} km/s (k_com >= 50/Mpc on z 10-3400)")

        def pick(sc):
            ok = [x["galaxies_pass"] for x in sc]
            for i in range(len(sc)):
                if all(ok[i:]): return sc[i]
            return None
        RES["foot"] = {}
        for f in A0K:
            sc = RES["scan"][f]
            for x in sc[::4]:
                P(f"   [{f}] c0 {x['c']:7.2f}: G5 {x['G5_max']:.3f} G6 {x['G6_shift']:+.3f} G7 {x['G7_shift']:+.3f} gal {'Y' if x['galaxies_pass'] else 'n'} | "
                  f"X-COP {x['X_mean']:+.3f}/{x['X_rms']:.3f} groups [{x['G_fst1']:+.3f},{x['G_fst0']:+.3f}] strict {x['G_strict']} conv {x['conv_frac']:.2f}")
            cm = pick(sc); cmv = pick(RES["scan_variant"][f])
            if cm is None:
                lab = "NO VERDICT (no c0 passes galaxies)"; miss = None
            else:
                lab = "PASS" if (cm["X_pass"] and cm["G_band"]) else "FAIL"
                miss = "under" if cm["X_mean"] > 0.05 else ("over" if cm["X_mean"] < -0.05 else "rms" if not cm["X_pass"] else "x-pass")
                labv = None if cmv is None else ("PASS" if (cmv["X_pass"] and cmv["G_band"]) else "FAIL")
                if labv != lab: lab = "NO VERDICT (host sensitive)"
                P(f"[{f}] variant host: c_min {cmv['c'] if cmv else None}, X-COP {cmv['X_mean']:+.3f}/{cmv['X_rms']:.3f}, groups [{cmv['G_fst1']:+.3f},{cmv['G_fst0']:+.3f}] -> {labv}")
            cs = [x["c"] for x in sc if cm and x["c"] >= cm["c"] and x["X_pass"] and x["G_band"]]
            RES["foot"][f] = dict(c_min=cm, label=lab, X_miss=miss, cluster_set_c=cs, J0_ok=bool(cm is not None and cm["c"] <= cmaxJ))
            if cm:
                P(f"[{f}] c_min = {cm['c']:.2f} km/s (galaxy gates only). PREDICTION: X-COP {cm['X_mean']:+.3f}/{cm['X_rms']:.3f} -> {'PASS' if cm['X_pass'] else 'FAIL'} ({miss}); "
                  f"groups [{cm['G_fst1']:+.3f},{cm['G_fst0']:+.3f}] -> {'PASS' if cm['G_band'] else 'FAIL'}; strict {cm['G_strict']}; conv {cm['conv_frac']:.2f}")
                P(f"[{f}] J0 adiabatic: c_min {'<=' if cm['c'] <= cmaxJ else '>'} {cmaxJ:.3g} -> {'primordial floor allowed' if cm['c'] <= cmaxJ else 'floor must be injected late (mechanism OWED)'}")
            P(f"[{f}] LABEL: {lab}; CLUSTER-SET c0 passing X-COP and groups band: {[round(c, 2) for c in cs]}")
        RES["label"] = "PASS" if all(RES["foot"][f]["label"] == "PASS" for f in A0K) else ("FAIL" if all(RES["foot"][f]["label"] in ("PASS", "FAIL") for f in A0K) else "NO VERDICT")
        P(f"LABEL: {RES['label']}")
    else:
        main = json.load(open(os.path.join(HERE, "qx13.json")))
        jobs = []
        for f in A0K:
            cm = main["foot"][f]["c_min"]; c = cm["c"] if cm else 0.0
            jobs += [(f, 0.0, {}, dict(heat=True, floor=False, kfac=1.0)),
                     (f, c, {}, dict(heat=False, floor=True, kfac=1.0)),
                     (f, c, {}, dict(heat=True, floor=True, kfac=1e-4))]
        with Pool(WK) as pool:
            rr = pool.map(job, jobs)
        RES["M"] = {}
        for f, c, mode, o in rr:
            key = "M1" if not mode["floor"] else ("M2" if not mode["heat"] else "M3")
            RES["M"].setdefault(f, {})[key] = dict(c=c, **o)
        for f in A0K:
            cm = main["foot"][f]["c_min"]; m = RES["M"][f]
            m1, m2, m3 = m["M1"], m["M2"], m["M3"]
            vac = bool(cm is not None and cm["c"] == 0.0)
            m["M1_vacuous"] = vac
            m["M1_bites"] = bool(vac or (not m1["galaxies_pass"]) or max(abs(m1["G_fst0"] - cm["G_fst0"]), abs(m1["G_fst1"] - cm["G_fst1"])) > 0.05)
            m["M2_bites"] = bool(abs(m2["X_mean"] - cm["X_mean"]) > 0.05)
            m["M3_bites"] = bool(not m3["galaxies_pass"])
            P(f"[{f}] M1 floor off: gal {m1['galaxies_pass']}, X-COP {m1['X_mean']:+.3f}/{m1['X_rms']:.3f}, groups [{m1['G_fst1']:+.3f},{m1['G_fst0']:+.3f}] -> "
              f"{'VACUOUS (c_min = 0)' if vac else ('BITES' if m['M1_bites'] else 'DOES NOT BITE')}")
            P(f"[{f}] M2 heating off at c_min: X-COP {m2['X_mean']:+.3f}/{m2['X_rms']:.3f} (main {cm['X_mean']:+.3f}) -> {'BITES' if m['M2_bites'] else 'DOES NOT BITE (heating irrelevant)'}")
            P(f"[{f}] M3 K x 1e-4: gal {m3['galaxies_pass']} (G5 {m3['G5_max']:.2f}, G6 {m3['G6_shift']:+.3f}) -> {'BITES' if m['M3_bites'] else 'DOES NOT BITE'}")
        RES["gate_power"] = bool(all(RES["M"][f]["M3_bites"] for f in A0K))
        P(f"gate power (M3) on both footings: {RES['gate_power']}")
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
