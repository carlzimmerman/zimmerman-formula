#!/usr/bin/env python3
"""CFG526 question B (FROZEN_CRITERIA.md): does the predicted small-scale suppression P/P_S0 conflict with cosmic-shear constraints?
r(k, z) from the run JSONs (particles; z = 0.5 primary, z = 0 reported), lensing-tracer variant from cfg526_profiles stage 1 (z = 0).
A_eq(k) = (r F P_NL - P_L)/(P_NL - P_L), A_eff = mean over k = 1, 2, 4 h/Mpc; compared with A_mod (Amon & Efstathiou 2022 KiDS-1000:
0.858 +- 0.052; Preston, Amon & Efstathiou 2023 DES Y3: 0.82 +- 0.04) -- recalled literature values, PROVISIONAL. Nothing downloaded.
CFG526_MUTATE=1: r -> 0.5 r at k >= 1 must be EXCLUDED and r = 1 must not -> _MUTATE outputs, exit 1 = detected."""
import os, sys, json, math, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
WORK = os.path.join(EXT, "cfg526_work")
MUT = os.environ.get("CFG526_MUTATE", "0") == "1"
spec = importlib.util.spec_from_file_location("eng", os.path.join(CFG, "CFG521_small_box_galaxy_regime", "cfg521_pm.py"))
eng = importlib.util.module_from_spec(spec); spec.loader.exec_module(eng)

DATA = {"KiDS-1000 (Amon & Efstathiou 2022)": (0.858, 0.052), "DES Y3 (Preston, Amon & Efstathiou 2023)": (0.82, 0.04)}   # PROVISIONAL
KS = [1.0, 2.0, 4.0]
F_FID_LO = [0.90, 0.85, 0.80]; F_FID_HI = [0.98, 0.95, 0.92]; F_STRONG = [0.82, 0.76, 0.72]      # PROVISIONAL bands at k = 1, 2, 4
ZA = {"z1": 0.5, "z0.5": 2 / 3, "z0": 1.0}

W521, W518, W359 = (os.path.join(EXT, d) for d in ("cfg521_work", "cfg518_work", "cfg359_work"))
def j521(sw, L, foot="canonical"):
    return os.path.join(W521, f"cfg521_{sw}_TA_MIXA_MASSCONS_fretcensus_FLAT_{foot}_N256" + (f"_L{L}" if L != 200 else "") + ".json")
BOX = {"canonical": {100: ("DCcan_L100", j521("RES", 100), j521("S0", 100)), 50: ("DCcan_L50", j521("RES", 50), j521("S0", 50)),
                     25: ("DCcan_L25", j521("RES", 25), j521("S0", 25))},
       "alt": {50: ("DCalt_L50", j521("RES", 50, "alt"), j521("S0", 50)), 25: ("DCalt_L25", j521("RES", 25, "alt"), j521("S0", 25))}}
L200 = {"canonical": (os.path.join(W518, "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256.json"), os.path.join(W359, "cfg359_S0_FLAT_canonical_N256.json")),
        "alt": (os.path.join(W518, "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_alt_N256.json"), os.path.join(W359, "cfg359_S0_FLAT_canonical_N256.json"))}
LINES = []
def P(s=""):
    print(s); LINES.append(s)

def ratio_at(run, s0, snap, k):
    a, b = json.load(open(run))["snap"][snap], json.load(open(s0))["snap"][snap]
    kk = np.array(a["k"]); i = int(np.argmin(np.abs(np.log(kk / k))))
    return float(a["P"][i] / b["P"][i]), float(kk[i]), float(b["P"][i])

def A_eq(r, F, Pnl, Pl):
    return (r * F * Pnl - Pl) / (Pnl - Pl)

def main():
    P("CFG526 B: framework small-scale suppression vs cosmic-shear A_mod constraints (recalled, PROVISIONAL)")
    P("kappa = 1/2 FITTED; footings never pooled; cold energy MASS still required; not theory closed. Nothing downloaded.")
    for n, (m, s) in DATA.items(): P(f"  {n}: A_mod = {m} +- {s}  [PROVISIONAL]")
    P(f"  feedback F(k = 1, 2, 4): fiducial band {F_FID_LO} - {F_FID_HI}; strong {F_STRONG}  [PROVISIONAL]")
    OUT = {}
    for foot, boxes in BOX.items():
        P(f"\n===== footing {foot} =====")
        tab = {}
        for snap in ("z1", "z0.5", "z0"):
            for L, (nm, run, s0) in boxes.items():
                tab[(snap, L)] = [ratio_at(run, s0, snap, k) for k in KS]
            run, s0 = L200[foot]; tab[(snap, 200)] = [ratio_at(run, s0, snap, k) for k in KS]
        for snap in ("z1", "z0.5", "z0"):
            P(f"  {snap}: r = P/P_S0 at k = 1, 2, 4 (nearest bin)")
            for L in sorted({l for (s, l) in tab if s == snap}, reverse=True):
                P(f"    L{L:<4d} " + "  ".join(f"k {x[1]:.2f}: {x[0]:.3f}" for x in tab[(snap, L)]) + ("   (k = 4 is the L200 Nyquist bin; reported only)" if L == 200 else ""))
        # lensing-tracer variant (z = 0)
        grav = {}
        for L, (nm, run, s0) in boxes.items():
            f = os.path.join(WORK, f"cfg526_{nm}.npz"); f0 = os.path.join(WORK, f"cfg526_S0_L{L}.npz")
            if os.path.exists(f) and os.path.exists(f0):
                d, d0 = np.load(f), np.load(f0); kk = d["kgrav"]
                grav[L] = []
                for k in KS:
                    i = int(np.argmin(np.abs(np.log(kk / k))))
                    grav[L].append([float(d["pgrav"][i] / d0["ppart"][i]), float(d["ppart"][i] / d0["ppart"][i])])
        P("  z0 lensing tracer: r_grav = P(delta_grav)/P_S0 vs r_part at k = 1, 2, 4")
        for L, v in grav.items():
            P(f"    L{L:<4d} " + "  ".join(f"{g:.3f} vs {p:.3f}" for g, p in v))
        # convergence and conservative r at z0.5
        Ls = sorted(boxes, reverse=True)
        conv, cons, mono = [], [], []
        for j, k in enumerate(KS):
            rs = {L: tab[("z0.5", L)][j][0] for L in Ls}
            c = abs(rs[50] - rs[25]) <= 0.05 and (100 in rs and abs(rs[100] - rs[50]) <= 0.05)
            seq = [rs[L] for L in Ls]
            m = all(seq[i] + 0.02 >= seq[i + 1] for i in range(len(seq) - 1))
            conv.append(bool(c)); mono.append(bool(m)); cons.append(rs[25] if m else max(seq))
        P(f"  z0.5 convergence at k = 1, 2, 4: {conv} (alt has no L100 run -> cannot be verified); monotone deepening: {mono}")
        P(f"  conservative (least suppressed) r at z0.5: {[round(x, 3) for x in cons]}")
        def aeff(rv, F, snap="z0.5", Lref=None):
            out = []
            for j, k in enumerate(KS):
                L = Lref if Lref else (25 if mono[j] else max(Ls, key=lambda l: tab[(snap, l)][j][0]))
                r_, kb, Pnl = tab[(snap, L)][j]
                Pl = float(eng.P_lin0(np.array([kb]))[0]) * eng.Dgrow(ZA[snap]) ** 2
                out.append(A_eq(rv[j], F[j], Pnl, Pl))
            return float(np.mean(out)), out
        cases = {"F=1 conservative r": (cons, [1, 1, 1]), "fid-lo F, conservative r": (cons, F_FID_LO), "fid-hi F, conservative r": (cons, F_FID_HI),
                 "strong F, conservative r": (cons, F_STRONG)}
        for L in Ls:
            cases[f"F=1, L{L} r"] = ([tab[("z0.5", L)][j][0] for j in range(3)], [1, 1, 1])
            cases[f"fid-hi F, L{L} r"] = ([tab[("z0.5", L)][j][0] for j in range(3)], F_FID_HI)
        cases["LCDM (r = 1), F=1"] = ([1, 1, 1], [1, 1, 1]); cases["LCDM, fid-lo F"] = ([1, 1, 1], F_FID_LO); cases["LCDM, fid-hi F"] = ([1, 1, 1], F_FID_HI)
        if MUT:
            cases["MUTATE 0.5 r"] = ([0.5 * x for x in cons], [1, 1, 1])
        res = {}
        P("  A_eff (z0.5) and pulls z_d = (A_eff - A_mod)/sigma:")
        for cn, (rv, F) in cases.items():
            a, per = aeff(rv, F)
            pulls = {n: (a - m) / s for n, (m, s) in DATA.items()}
            res[cn] = {"A_eff": a, "A_eq_k": per, "pulls": pulls}
            P(f"    {cn:28s} A_eff {a:.3f}  (A_eq k1/2/4 {per[0]:.3f} {per[1]:.3f} {per[2]:.3f})  pulls KiDS {list(pulls.values())[0]:+.2f}  DES {list(pulls.values())[1]:+.2f}")
        # lensing-tracer sensitivity at z0 (F = 1, same box choice per k as conservative; L25 if monotone)
        dvar = None
        if grav:
            ap, ag = [], []
            for j, k in enumerate(KS):
                L = 25 if mono[j] else max(Ls, key=lambda l: tab[("z0.5", l)][j][0])
                if L not in grav: continue
                r_, kb, Pnl = tab[("z0", L)][j]; Pl = float(eng.P_lin0(np.array([kb]))[0])
                ap.append(A_eq(grav[L][j][1], 1, Pnl, Pl)); ag.append(A_eq(grav[L][j][0], 1, Pnl, Pl))
            dvar = float(np.mean(ag) - np.mean(ap)) if ap else None
        P(f"  z0 lensing-tracer shift of A_eff (grav - particles, F = 1): {dvar:+.3f}" if dvar is not None else "  z0 lensing-tracer shift: n/a")
        # Lya flag
        lya = any(tab[("z1", L)][j][0] < 0.90 for L in Ls for j in range(3))
        P(f"  Lya rule: r(z = 1, k <= 4) < 0.90 in some box: {lya}" + (" -> a z >= 2 snapshot is needed" if lya else " -> Lya NOT DIAGNOSTIC (no z >= 2 snapshot; deficit develops late)"))
        # verdict
        pc = res["F=1 conservative r"]["pulls"]
        if all(v < -3 for v in pc.values()):
            v = "EXCLUDED"; why = "F = 1, conservative r: pulls " + ", ".join(f"{x:+.2f}" for x in pc.values())
        elif not all(conv) or (dvar is not None and abs(dvar) > 0.04):
            v = "NOT DIAGNOSTIC"; why = f"r not converged at k = {[k for k, c in zip(KS, conv) if not c]}" + (f"; lensing-tracer shift {dvar:+.3f}" if dvar is not None and abs(dvar) > 0.04 else "")
        else:
            fl, fh = res["fid-lo F, conservative r"]["pulls"], res["fid-hi F, conservative r"]["pulls"]
            ll, lh = res["LCDM, fid-lo F"]["pulls"], res["LCDM, fid-hi F"]["pulls"]
            if all(abs(fl[n]) <= 1 or abs(fh[n]) <= 1 for n in DATA) and all(min(abs(ll[n]), abs(lh[n])) > 2 for n in DATA):
                v, why = "PREFERRED-HINT", "framework + fiducial feedback within 1 sigma of both; LCDM + same feedback > 2 sigma"
            elif any(abs(fl[n]) <= 2 or abs(fh[n]) <= 2 for n in DATA):
                v, why = "ALLOWED", "framework + fiducial feedback within 2 sigma of at least one dataset"
            else:
                v, why = "NOT DIAGNOSTIC", "no rule met"
        P(f"  VERDICT B [{foot}]: {v} -- {why}")
        OUT[foot] = {"verdict": v, "why": why, "r": {f"{s}_L{L}": tab[(s, L)] for (s, L) in tab}, "grav_z0": grav, "converged": conv,
                     "monotone": mono, "r_conservative_z05": cons, "cases": res, "tracer_shift": dvar, "lya_flag": lya}
        if MUT:
            OUT[foot]["mutate_excluded"] = all(x < -3 for x in res["MUTATE 0.5 r"]["pulls"].values())
            OUT[foot]["lcdm_not_excluded"] = not all(x < -3 for x in res["LCDM (r = 1), F=1"]["pulls"].values())
    sfx = "_MUTATE" if MUT else ""
    if MUT:
        det = all(OUT[f]["mutate_excluded"] and OUT[f]["lcdm_not_excluded"] for f in OUT)
        P(f"\nMUTATE (B): 0.5 r EXCLUDED and r = 1 not excluded in both footings: {'DETECTED' if det else 'NOT DETECTED'}")
    open(os.path.join(HERE, f"cfg526_data{sfx}.out"), "w").write("\n".join(LINES) + "\n")
    json.dump(OUT, open(os.path.join(HERE, f"cfg526_data{sfx}.json"), "w"), indent=1)
    if MUT: sys.exit(1 if det else 0)

if __name__ == "__main__":
    main()
