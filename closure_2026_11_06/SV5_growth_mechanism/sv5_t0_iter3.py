#!/usr/bin/env python3
"""SV5 T0 (target function map) + iter_3 (class T: lambda_J = F(a0(z)/a0(0))). Criteria: FROZEN_CRITERIA.md (247d2eaa2f).
    python3 sv5_t0_iter3.py            -> sv5_t0.json/.out, iter_3_a0z_tied_coupling/sv5_iter3.json/.out
    python3 sv5_t0_iter3.py --mutate   -> iter_3_a0z_tied_coupling/sv5_iter3_MUTATE.json/.out
kappa = 1/2 FITTED; not theory closed. 1 thread. Footings never pooled."""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sv5_common as C
import numpy as np
MUT = "--mutate" in sys.argv; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
HERE = C.HERE; IT3 = os.path.join(HERE, "iter_3_a0z_tied_coupling")
N3 = C.load_growth(); g2gen, solve_gen, I2 = N3["g2gen"], N3["solve_gen"], N3["I2"]
Q = C.load_qx10()
DUST = 1e8; SMOOTH = 1e-8          # physical kJ in Mpc^-1
LINE = I2.DCHI2_LINE
sigA, AX0 = C.sigma_A_rel(N3)

# ---------------- T0.3 host requirement (needed by iter_3 and its MUTATE)
lam_grid = np.geomspace(1.0, 1000.0, 31)          # Mpc
def host_ok(lam_mpc, f):
    a0k = Q["A0K"][f]; o = Q["grade_cell"](lam_mpc * 1e3, a0k); bL, bE = Q["baselines"](a0k)
    g6 = o["G6_mean"] - bL; g7 = o["G7_mean"] - bE; g5 = max(x["ratio"] for x in o["G5"]["rows"])
    return dict(lam=float(lam_mpc), G5_max=float(g5), G6_shift=float(g6), G7_shift=float(g7),
                pass_=bool(o["G5"]["pass_"] and abs(g6) <= 0.05 and abs(g7) <= 0.15))

# ---------------- histories r(z) = a0(z)/a0(0)
NODES = [0.0, 0.4, 0.7, 1.0, 1.5, 2.33]
cfg = json.load(open(os.path.join(C.REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao", "cfg689.json")))
a0n = cfg["BAO+SN"]["P3"]["a0_node_q"]; wn = np.array([a0n[str(z)][2] ** 2 for z in NODES])   # rho_DE ~ a0^2
def r_native(z): return np.sqrt(np.interp(z, NODES, wn) / wn[0])                                  # held beyond 2.33
def r_cpl(z, w0=-0.838, wa=-0.62): return np.sqrt((1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z)))
def r_flat(z): return np.ones_like(np.asarray(z, float))
HIST = {"H-flat": r_flat, "H-native": r_native, "H-CPL(reported)": r_cpl}
ZH = np.linspace(0.0, 0.5, 501)

def kJ_from_lam(lamfun):
    return lambda a: 2 * np.pi / max(lamfun(1 / a - 1), 2 * np.pi / DUST)

def member_star(rf, lam_host, extra=None):
    rH = rf(ZH); lo, hi = float(rH.min()), float(rH.max())
    def lam(z):
        rr = float(rf(z)); inI = (lo - 1e-12 <= rr <= hi + 1e-12)
        if extra is not None and extra[0] <= z <= extra[1]: inI = True
        return lam_host if inI else 0.0
    return lam, (lo, hi)

def member_pow(rf, lam_host, q):
    lam0 = lam_host / float(np.min(rf(ZH) ** q))
    return (lambda z: lam0 * float(rf(z)) ** q), lam0

if not MUT:
    # ---------------- T0.1 required source
    ref = N3["ref"]; dm_s = solve_gen(lambda a: SMOOTH)
    kg, zg = N3["kgrid"], N3["zgrid"]
    Rreq = {}
    for zt in (0.5, 1.0, 2.0, 5.0, 10.0):
        j = int(np.argmin(np.abs(zg - zt)))
        Rreq[f"z{zg[j]:.2f}"] = {f"k{k:.3g}": float(ref[i, j] / dm_s[i, j]) for i, k in enumerate(kg) if 1e-3 <= k <= 1.0 and i % 4 == 0}
    S_sm = I2.limber_ratio(N3["M"], N3["H0"], kg, zg, dm_s / ref)
    d_smooth = g2gen(lambda a: SMOOTH)
    it2 = json.load(open(os.path.join(C.CL, "QX3_cmb_growth", "iter2_kq_dust", "iter2.json")))
    odr = [r["omega_d_best"] for r in it2["G1"]]
    P("SV5 T0 target map. kappa = 1/2 FITTED; not theory closed. Criteria 247d2eaa2f.")
    P(f"T0.4 PR4 amplitude: A_X0 {AX0:.4f}, sigma_A,rel {sigA:.4f}")
    P(f"T0.1 dust amplitude omega_d {min(odr):.4f}-{max(odr):.4f} (QX3 iter2 G1 corners). Smooth sector: shape dchi2 {d_smooth:.1f}; "
      f"S_smooth(L) at L 30/100/300/400: " + "/".join(f"{S_sm[L]:.3g}" for L in (30, 100, 300, 400)))
    for k_, v in Rreq.items():
        P(f"  R_req(k) {k_}: " + ", ".join(f"{kk} {vv:.3g}" for kk, vv in v.items()))
    # ---------------- T0.2 tolerated late stiffening
    T02 = {}
    for ls in (1.0, 3.0, 10.0, 30.0, 100.0, 1000.0):
        row = {}
        for zs in (0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0):
            row[str(zs)] = g2gen(kJ_from_lam(lambda z, ls=ls, zs=zs: ls if z < zs else 0.0))
        ok = [float(zs) for zs, d in row.items() if d <= LINE]
        T02[str(ls)] = dict(dchi2=row, zs_max=(max(ok) if ok else None))
        P(f"T0.2 step lambda_s {ls:g} Mpc: dchi2 by z_s " + ", ".join(f"{zs} {d:.2f}" for zs, d in row.items()) + f" -> z_s,max {T02[str(ls)]['zs_max']}")
    # ---------------- T0.3
    T03 = {}
    for f in C.A0:
        rows = []; first = None
        for lam in lam_grid:
            rr = host_ok(lam, f); rows.append(rr)
            if rr["pass_"] and first is None: first = rr["lam"]
        T03[f] = dict(rows=rows, lam_host=first)
        P(f"T0.3 [{f}] lambda_host {first} Mpc; at grid: " + ", ".join(f"{r_['lam']:.3g}:{r_['G6_shift']:+.3f}{'P' if r_['pass_'] else 'F'}" for r_ in rows[::3]))
    lam_host = {f: T03[f]["lam_host"] for f in C.A0}
    LH = None if any(v is None for v in lam_host.values()) else max(lam_host.values())
    P(f"T0.3 lambda_host = max over footings = {LH} Mpc")
    json.dump(dict(lane="SV5 T0", criteria="247d2eaa2f", sigma_A_rel=sigA, A_X0=AX0, omega_d_range=[min(odr), max(odr)],
                   smooth_dchi2=d_smooth, S_smooth={str(L): float(S_sm[L]) for L in (8, 30, 100, 200, 300, 400)}, R_req=Rreq,
                   T02=T02, T03=T03, lambda_host=LH, note="kappa = 1/2 FITTED; not theory closed"),
              open(os.path.join(HERE, "sv5_t0.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "sv5_t0.out"), "w").write("\n".join(OUT) + "\n"); OUT.clear()

    # ---------------- iter_3
    P("SV5 iter_3 (class T: lambda_J = F(a0(z)/a0(0))). kappa = 1/2 FITTED; not theory closed. Criteria 247d2eaa2f.")
    RES = dict(lane="SV5 iter_3", criteria="247d2eaa2f", lambda_host=LH, lambda_host_by_footing=lam_host, hist={})
    if LH is None:
        RES["label"] = "NOT EVALUABLE (lambda_host NOT FOUND)"; P(RES["label"])
    else:
        for hn, rf in HIST.items():
            lam, I_H = member_star(rf, LH); dS = g2gen(kJ_from_lam(lam))
            zz = np.linspace(0, 20, 4001); stiff = [float(z) for z in zz if lam(z) > 0]
            lamK, _ = member_star(rf, LH, extra=(1.0, 2.0)); dK = g2gen(kJ_from_lam(lamK))
            pows = {}
            for q in np.arange(-6, 6.0001, 0.5):
                lf, l0 = member_pow(rf, LH, q); pows[f"{q:+.1f}"] = dict(lambda_0=l0, dchi2=g2gen(kJ_from_lam(lf)))
            best = min(pows.items(), key=lambda kv: kv[1]["dchi2"])
            ext = (min(stiff), max(stiff)) if stiff else None
            h = dict(I_H=list(I_H), stiff_z_extent=ext, stiff_fraction_z0_20=len(stiff) / len(zz), Mstar_dchi2=dS,
                     Kmono_dchi2=dK, Kmono_pass=bool(dK >= dS - 1e-6), power=pows, best_power=[best[0], best[1]["dchi2"]])
            # per-footing reading (lambda_host per footing)
            h["Mstar_by_footing"] = {f: g2gen(kJ_from_lam(member_star(rf, lam_host[f])[0])) for f in C.A0}
            if dS <= LINE: lab = "WINDOW-CONDITIONAL"
            else: lab = "NO-GO FOR CLASS" if h["Kmono_pass"] else "FAIL"
            h["label"] = lab; RES["hist"][hn] = h
            P(f"[{hn}] I_H = r(Z_H) = [{I_H[0]:.4f}, {I_H[1]:.4f}]; M* stiff on z in {ext} (z<20 fraction {h['stiff_fraction_z0_20']:.3f}); "
              f"M* dchi2 {dS:.2f} (canonical {h['Mstar_by_footing']['canonical']:.2f}, alt {h['Mstar_by_footing']['alt']:.2f}); "
              f"K-mono {dK:.2f} -> {'PASS' if h['Kmono_pass'] else 'FAIL'}; best power law q {best[0]} dchi2 {best[1]['dchi2']:.2f} -> {lab}")
        RES["label"] = {hn: h["label"] for hn, h in RES["hist"].items()}
    P(f"iter_3 labels: {RES['label']}")
    json.dump(RES, open(os.path.join(IT3, "sv5_iter3.json"), "w"), indent=1, default=float)
    open(os.path.join(IT3, "sv5_iter3.out"), "w").write("\n".join(OUT) + "\n")
else:
    t0 = json.load(open(os.path.join(HERE, "sv5_t0.json"))); LH = t0["lambda_host"]
    P("SV5 iter_3 MUTATE. kappa = 1/2 FITTED; not theory closed.")
    R = dict(lane="SV5 iter_3 MUTATE", criteria="247d2eaa2f")
    m1 = {f: host_ok(1e-3, f) for f in C.A0}
    R["M1"] = dict(rows=m1, bites=bool(all(not v["pass_"] for v in m1.values())))
    P("M1 (F == dust, lambda 1 kpc): " + "; ".join(f"{f} G5 max {v['G5_max']:.2f} G6 {v['G6_shift']:+.3f} -> {'FAIL' if not v['pass_'] else 'PASS'}" for f, v in m1.items())
      + f" -> {'BITES' if R['M1']['bites'] else 'NO BITE'}")
    d2 = g2gen(kJ_from_lam(lambda z: LH)); R["M2"] = dict(dchi2=d2, bites=bool(d2 > I2.DCHI2_LINE))
    P(f"M2 (F == lambda_host {LH} Mpc at every z): dchi2 {d2:.1f} -> {'BITES' if R['M2']['bites'] else 'NO BITE'}")
    json.dump(R, open(os.path.join(IT3, "sv5_iter3_MUTATE.json"), "w"), indent=1, default=float)
    open(os.path.join(IT3, "sv5_iter3_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
