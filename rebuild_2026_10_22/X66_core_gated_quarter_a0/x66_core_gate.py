#!/usr/bin/env python3
"""X66: X65's shell harness with the core-gated boost  g += Q*Theta(dg/dr>0)*max(0,(a0/4)/g_sigma - 1)*g_N.

Frozen criteria: FROZEN_CRITERIA.md (committed first). Harness and measurement are imported from X65 unchanged.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x66_core_gate.py
      X66_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x66_core_gate.py   # threshold a0/2
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "X65_stream_sign_gated_aqual"))
import x65_shells as h  # noqa: E402

G, K = h.G, h.K_CHUNK
CAP = 100.0
MUTATE = os.environ.get("X66_MUTATE") == "1"
DIV = 2.0 if MUTATE else 4.0
MASSES = h.MASSES


def smooth3(x):
    s = np.convolve(x, np.ones(3), "same")
    n = np.convolve(np.ones_like(x), np.ones(3), "same")
    return s / n


def accel(r, v, m, L, eps, mode, a0, diag=None):
    order = np.argsort(r, kind="stable")
    rs, ms, vs, Ls = r[order], m[order], v[order], L[order]
    Menc = np.cumsum(ms) - 0.5 * ms
    gN = G * Menc / (rs * rs + eps * eps)
    a_s = -gN.copy()
    if mode == "G":
        Q = h.q_of_streams(r, m)[order]
        starts = np.arange(0, len(r), K)
        ends = np.append(starts[1:], len(r))
        mt = np.add.reduceat(ms, starts)
        rk = np.add.reduceat(ms * rs, starts) / mt
        edges = np.append(np.append(0.0, rs[starts[1:]]), rs[-1])
        vol = 4 / 3 * np.pi * np.maximum(edges[1:] ** 3 - edges[:-1] ** 3, 1e-30)
        w2 = vs * vs + Ls * Ls / (rs * rs)
        s2 = np.add.reduceat(ms * w2, starts) / mt - (np.add.reduceat(ms * vs, starts) / mt) ** 2
        rho = smooth3(mt / vol)
        s2 = smooth3(np.maximum(s2, 0.0))
        gk = G * (np.cumsum(mt) - 0.5 * mt) / rk ** 2
        T = 4 * np.pi * G * rho - 2 * gk / rk
        gsig = np.sqrt(np.pi / 3 * G * rho * s2)
        thr = a0 / DIV
        with np.errstate(divide="ignore"):
            boost = np.where(gsig > 0, np.maximum(0.0, thr / gsig - 1.0), CAP)
        capped = boost > CAP
        boost = np.minimum(boost, CAP)
        qk = Q[starts]
        Wb = qk * (T > 0) * boost
        Wb_s = np.repeat(Wb, ends - starts)
        a_s -= Wb_s * gN
        if diag is not None:
            diag.update(frac_boosted=float(np.sum(mt[Wb > 0]) / mt.sum()), max_boost=float(Wb.max()),
                        cap_hit=bool(np.any(capped & (qk * (T > 0) > 0))), gsig0_over_thr=float(gsig[0] / thr))
    a = np.empty_like(r)
    a[order] = a_s
    return a + L * L / r ** 3


def run(M, mode, a0_si, j=0.1, N=2000):
    a0 = a0_si * h.MS2_TO_KPCGYR2
    r, v, m, L, R = h.initial_conditions(M, N, j)
    eps = 1e-3 * R
    E0 = h.energy(r, v, m, L)
    t, nstep, s1_viol, cap_any = 0.0, 0, 0, False
    snaps, snap_t = [], h.T_AVG0
    a = accel(r, v, m, L, eps, mode, a0)
    while t < h.T_END - 1e-12:
        dt = min(h.DT_MAX, max(h.DT_MIN, h.ETA * np.min(np.sqrt(r / np.maximum(np.abs(a), 1e-30)))))
        dt = min(dt, max(snap_t - t, 1e-12)) if snap_t <= h.T_END + 1e-9 else min(dt, h.T_END - t)
        v += 0.5 * dt * a
        r += dt * v
        r = np.abs(r)
        d = {} if mode == "G" else None
        a = accel(r, v, m, L, eps, mode, a0, d)
        v += 0.5 * dt * a
        t += dt
        nstep += 1
        if d:
            cap_any |= d["cap_hit"]
        if mode == "G" and np.all(np.diff(r) > 0) and h.q_of_streams(r, m).max() != 0.0:
            s1_viol += 1
        if t >= snap_t - 1e-9 and snap_t <= h.T_END + 1e-9:
            snaps.append(r.copy())
            snap_t += h.SNAP_DT
    d = {}
    if mode == "G":
        accel(r, v, m, L, eps, mode, a0, d)
    Qend = h.q_of_streams(r, m) if mode == "G" else np.zeros_like(r)
    return dict(M=M, mode=mode, j=j, N=N, a0=a0, R=R, nstep=nstep, s1_viol=s1_viol,
                dE=float((h.energy(r, v, m, L) - E0) / abs(E0)), snaps=np.array(snaps), m=m,
                r_end=r, Q_end=Qend, diag=dict(d, cap_any=bool(cap_any)))


def main():
    t0 = time.time()
    rows = []

    def do(M, mode, foot, j=0.1, N=2000):
        a0 = h.FOOTINGS[foot]
        sig = a0 * h.MS2_TO_KPCGYR2 / (2 * np.pi * G)
        res = run(M, mode, a0, j, N)
        row = h.measure(res, sig)
        row.update(footing=foot, **res["diag"])
        rows.append(row)
        print(f"{mode} {foot:9s} M={M:.0e} j={j} N={N}: R={row['R']:.3f} P={row['P']:.3f} r0={row['r0']:.3g} "
              f"fit={row['fit_rms']:.3f} dE={row['dE']:+.4f} steps={row['nstep']}"
              + (f" fB={row['frac_boosted']:.2f} maxB={row['max_boost']:.2f} cap={row['cap_any']} "
                 f"gs0/thr={row['gsig0_over_thr']:.2f} Qcore={row['Q_core']:.2f}" if mode == "G" else ""), flush=True)
        return row

    if MUTATE:
        for M in MASSES:
            do(M, "G", "canonical")
        json.dump(rows, open(os.path.join(HERE, "x66_results_MUTATE.json"), "w"), indent=1)
        print(f"wall {time.time() - t0:.0f} s")
        return 0

    if os.environ.get("X66_REGRADE") == "1":
        # The first full run finished all 36 runs, then crashed writing the verdict (numpy bool in j_cases, fixed
        # above). Its rows were recovered unchanged from the partial JSON into x66_rows_recovered.json.
        rows = json.load(open(os.path.join(HERE, "x66_rows_recovered.json")))
        verdict = grade(rows)
        json.dump(dict(rows=rows, verdict=verdict), open(os.path.join(HERE, "x66_results.json"), "w"), indent=1)
        print(json.dumps(verdict, indent=1))
        return 0 if verdict["status"] == "GRADED" else 1

    JM = (1e9, 1e10, 1e11, 1e13)
    for M in MASSES:
        do(M, "N", "canonical")
    for j in (0.05, 0.2):
        for M in JM:
            do(M, "N", "canonical", j=j)
    for foot in h.FOOTINGS:
        for M in MASSES:
            do(M, "G", foot)
    for j in (0.05, 0.2):
        for M in JM:
            do(M, "G", "canonical", j=j)
    for M in (1e9, 1e10):
        do(M, "G", "canonical", N=1000)

    verdict = grade(rows)
    json.dump(dict(rows=rows, verdict=verdict), open(os.path.join(HERE, "x66_results.json"), "w"), indent=1)
    print(json.dumps(verdict, indent=1))
    print(f"wall {time.time() - t0:.0f} s")
    return 0 if verdict["status"] == "GRADED" else 1


def pick(rows, **kw):
    hit = [r for r in rows if all(r[k] == v for k, v in kw.items())]
    assert len(hit) == 1, kw
    return hit[0]


def lg(x, y):
    return float(np.log10(x / y))


def grade(rows):
    v = dict(status="GRADED", footings={}, fails=[])
    if max(abs(r["dE"]) for r in rows if r["mode"] == "N") > 0.02:
        v["status"] = "UNDECIDED (E1 energy)"
    if any(r["s1_viol"] for r in rows):
        v["status"] = "UNDECIDED (S1)"
    sig = {f: a * h.MS2_TO_KPCGYR2 / (2 * np.pi * G) for f, a in h.FOOTINGS.items()}
    RN = lambda M, foot, j=0.1: pick(rows, M=M, mode="N", j=j, N=2000)["R"] * sig["canonical"] / sig[foot]
    fitN = lambda M, j=0.1: pick(rows, M=M, mode="N", j=j, N=2000)["fit_ok"]
    RG = lambda M, foot, j=0.1, N=2000: pick(rows, M=M, mode="G", footing=foot, j=j, N=N)["R"]
    S_can = None
    for foot in h.FOOTINGS:
        f = dict(per_mass={f"{M:.0e}": dict(R_N=RN(M, foot), R_G=RG(M, foot), fit_N=fitN(M)) for M in MASSES})
        S = [M for M in MASSES if fitN(M) and RN(M, foot) < 0.7]
        if foot == "canonical":
            S_can = S
        if not S:
            f["verdict"] = "UNDECIDED (no below-floor mass)"
            v["fails"].append(f"{foot}: no below-floor mass")
        else:
            rg = np.array([RG(M, foot) for M in S])
            lift = np.median([lg(RG(M, foot), RN(M, foot)) for M in S])
            spread = lg(rg.max(), rg.min())
            if np.all((rg >= 0.67) & (rg <= 1.5)) and spread <= 0.2:
                f["verdict"] = "FLOOR EMERGES"
            elif lift > 0.1:
                f["verdict"] = "RAISES, NO FLOOR"
            elif abs(lift) <= 0.1:
                f["verdict"] = "NO EFFECT"
            else:
                f["verdict"] = "LOWERS (unlisted; reported)"
            f.update(S=[f"{M:.0e}" for M in S], median_lift_dex=float(lift), spread_dex=float(spread))
            if f["verdict"] != "FLOOR EMERGES":
                v["fails"].append(f"{foot}: {f['verdict']}")
        above = [M for M in MASSES if RN(M, foot) > 1.5]
        f["max_rule"] = ("REPRODUCED" if all(abs(lg(RG(M, foot), RN(M, foot))) <= 0.1 for M in above)
                         else "BROKEN") if above else "n/a"
        if f["max_rule"] == "BROKEN":
            v["fails"].append(f"{foot}: max() BROKEN")
        v["footings"][foot] = f
    jcases = []
    for j in (0.05, 0.2):
        for M in (1e9, 1e10, 1e11, 1e13):
            rn, rgj = RN(M, "canonical", j), RG(M, "canonical", j)
            if M == 1e13 or rn > 1.5:
                ok = bool(abs(lg(rgj, rn)) <= 0.1)
            elif rn < 0.7:
                ok = bool(0.67 <= rgj <= 1.5)
            else:
                ok = None
            jcases.append(dict(M=f"{M:.0e}", j=j, R_N=rn, R_G=rgj, ok=ok))
    v["j_cases"] = jcases
    v["j_robust"] = "ROBUST" if all(c["ok"] is not False for c in jcases) else "j-DEPENDENT"
    if v["j_robust"] != "ROBUST":
        v["fails"].append("j-DEPENDENT")
    res = {f"{M:.0e}": lg(RG(M, "canonical", N=1000), RG(M, "canonical")) for M in (1e9, 1e10)}
    v["resolution_dex"] = res
    if any(abs(x) > 0.1 for x in res.values()):
        v["fails"].append("UNRESOLVED")
    pm = os.path.join(HERE, "x66_results_MUTATE.json")
    if os.path.exists(pm) and S_can:
        mut = {r["M"]: r["R"] for r in json.load(open(pm))}
        rise = float(np.median([lg(mut[M], RG(M, "canonical")) for M in S_can]))
        v["mutate_rise_dex"] = rise
        v["mutate_R"] = {f"{M:.0e}": mut[M] for M in MASSES}
        if rise < 0.2:
            v["fails"].append("THRESHOLD-INSENSITIVE")
    else:
        v["fails"].append("MUTATE missing")
    v["overall"] = "PASS" if (v["status"] == "GRADED" and not v["fails"]) else "FAIL"
    v["caveat"] = "a0/4 encodes R = 1 by construction; a pass is not a derivation of a0/(2 pi G) and not an action"
    return v


if __name__ == "__main__":
    sys.exit(main())
