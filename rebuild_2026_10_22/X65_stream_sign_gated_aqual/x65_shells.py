#!/usr/bin/env python3
"""X65: 1D spherical-shell collapse of the cold sector with an AQUAL pull gated by the stream-sign Q.

Frozen criteria: FROZEN_CRITERIA.md (committed first). Units kpc, Msun, Gyr.
Modes per run: N (gate off), G (gated), MUTATE (Q == 1 always; set X65_MUTATE=1, separate outputs).
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x65_shells.py
      X65_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x65_shells.py
"""
import json, os, sys, time
import numpy as np

G = 4.4985e-6                       # kpc^3 Msun^-1 Gyr^-2
MS2_TO_KPCGYR2 = (3.15576e16 ** 2) / 3.08568e19
FOOTINGS = {"canonical": 9.3603e-11, "alt": 1.1312e-10}   # m s^-2, never pooled
MASSES = [1e9, 1e10, 1e11, 1e12, 1e13, 1e14]
T_FF_OUT, T_END, T_AVG0, SNAP_DT = 5.0, 12.0, 10.0, 0.1
K_CHUNK, ETA, DT_MAX, DT_MIN = 32, 0.02, 0.01, 1e-7
BURKERT_PK = 0.2545                 # peak GM/r^2 of a Burkert halo / (2 pi G rho0 r0)
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("X65_MUTATE") == "1"


def initial_conditions(M, N, j):
    rho_bar = 3 * np.pi / (32 * G * T_FF_OUT ** 2)           # mean density of the outer shell's sphere
    R = (3 * M / (4 * np.pi * rho_bar)) ** (1 / 3)
    rc = 0.1 * R
    # M(<r) for rho ∝ (r^2+rc^2)^(-1/2):  ∝ r sqrt(r^2+rc^2) - rc^2 asinh(r/rc)
    prof = lambda r: r * np.sqrt(r * r + rc * rc) - rc * rc * np.arcsinh(r / rc)
    rg = np.linspace(0, R, 200001)
    fm = prof(rg) / prof(R)
    q = np.interp((np.arange(N) + 0.5) / N, fm, rg)
    m = np.full(N, M / N)
    Menc = np.cumsum(m) - 0.5 * m
    L = j * np.sqrt(G * Menc * q)
    return q, np.zeros(N), m, L, R


def q_of_streams(r, m):
    """Stream-sign Q per shell. r is in q-order (initial-radius order)."""
    sgn = np.sign(np.gradient(r))
    sgn[sgn == 0] = 1.0
    order = np.argsort(r, kind="stable")
    starts = np.arange(0, len(r), K_CHUNK)
    ms = np.add.reduceat((m * sgn)[order], starts)
    mt = np.add.reduceat(m[order], starts)
    qc = 1.0 - np.abs(ms) / mt
    Q = np.empty_like(r)
    Q[order] = np.repeat(qc, np.diff(np.append(starts, len(r))))
    return Q


def accel(r, m, L, eps, mode, a0):
    order = np.argsort(r, kind="stable")
    rs, ms = r[order], m[order]
    Menc = np.cumsum(ms) - 0.5 * ms
    soft = rs * rs + eps * eps
    a_s = -G * Menc / soft
    Q = None
    if mode != "N":
        Q = np.ones_like(r) if mode == "MUTATE" else q_of_streams(r, m)
        Qs = Q[order]
        gNQ = G * (np.cumsum(Qs * ms) - 0.5 * Qs * ms) / soft
        gphi = 0.5 * gNQ + np.sqrt(0.25 * gNQ * gNQ + gNQ * a0)
        a_s -= Qs * (gphi - gNQ)
    a = np.empty_like(r)
    a[order] = a_s
    return a + L * L / r ** 3, Q


def energy(r, v, m, L):
    order = np.argsort(r, kind="stable")
    Menc = np.cumsum(m[order]) - 0.5 * m[order]
    W = -np.sum(G * m[order] * Menc / r[order])
    return np.sum(0.5 * m * (v * v + L * L / (r * r))) + W


def run(M, mode, a0_si, j=0.1, N=2000):
    a0 = a0_si * MS2_TO_KPCGYR2
    r, v, m, L, R = initial_conditions(M, N, j)
    eps = 1e-3 * R
    E0 = energy(r, v, m, L)
    t, nstep, s1_viol = 0.0, 0, 0
    snaps, snap_t = [], T_AVG0
    a, Q = accel(r, m, L, eps, mode, a0)
    while t < T_END - 1e-12:
        dt = min(DT_MAX, max(DT_MIN, ETA * np.min(np.sqrt(r / np.maximum(np.abs(a), 1e-30)))))
        nxt = snap_t if snap_t <= T_END + 1e-12 else T_END
        dt = min(dt, max(nxt - t, 1e-12))
        v += 0.5 * dt * a
        r += dt * v
        r = np.abs(r)                      # a shell passing the centre reappears on the other side
        a, Q = accel(r, m, L, eps, mode, a0)
        v += 0.5 * dt * a
        t += dt
        nstep += 1
        if mode == "G" and np.all(np.diff(r) > 0) and Q.max() != 0.0:
            s1_viol += 1
        if t >= snap_t - 1e-9 and snap_t <= T_END + 1e-9:
            snaps.append(r.copy())
            snap_t += SNAP_DT
    Qend = q_of_streams(r, m) if mode != "N" else np.zeros_like(r)
    return dict(M=M, mode=mode, j=j, N=N, a0=a0, R=R, nstep=nstep, s1_viol=s1_viol,
                dE=float((energy(r, v, m, L) - E0) / abs(E0)), snaps=np.array(snaps), m=m,
                r_end=r, Q_end=Qend)


def burkert_log(x):
    return -np.log10((1 + x) * (1 + x * x))


def measure(res, sigma_a0):
    rs = res["snaps"].ravel()
    w = np.tile(res["m"], len(res["snaps"])) / len(res["snaps"])
    o = np.argsort(rs)
    rs, w = rs[o], w[o]
    cm = np.cumsum(w) / w.sum()
    r_in, r_out = np.interp(0.01, cm, rs), np.interp(0.60, cm, rs)
    edges = np.logspace(np.log10(r_in), np.log10(r_out), 26)
    mass, _ = np.histogram(rs, edges, weights=w)
    vol = 4 / 3 * np.pi * (edges[1:] ** 3 - edges[:-1] ** 3)
    rc = np.sqrt(edges[1:] * edges[:-1])
    ok = mass > 0
    lr, lrho = rc[ok], np.log10(mass[ok] / vol[ok])
    best = None
    for r0 in np.logspace(np.log10(r_in / 3), np.log10(3 * r_out), 400):
        f = burkert_log(lr / r0)
        lrho0 = np.mean(lrho - f)
        rms = np.sqrt(np.mean((lrho - lrho0 - f) ** 2))
        if best is None or rms < best[0]:
            best = (rms, r0, 10 ** lrho0)
    rms, r0, rho0 = best
    Menc = np.cumsum(w)
    sel = rs >= r_in
    g_pk = np.max(G * Menc[sel] / rs[sel] ** 2)
    out = dict(M=res["M"], mode=res["mode"], j=res["j"], N=res["N"], nstep=res["nstep"], dE=res["dE"],
               s1_viol=res["s1_viol"], r_in=r_in, r_out=r_out, r0=r0, rho0=rho0, fit_rms=rms,
               fit_ok=bool(rms <= 0.15), R=rho0 * r0 / sigma_a0, P=g_pk / res["a0"])
    if res["mode"] != "N":
        Qe, re, m = res["Q_end"], res["r_end"], res["m"]
        core = (re >= r_in) & (re <= r0)
        out["Q_core"] = float(np.sum(Qe[core] * m[core]) / np.sum(m[core])) if core.any() else float("nan")
        out["frac_Q_gt_half"] = float(np.sum(m[Qe > 0.5]) / np.sum(m))
        out["rQ_half_over_r0"] = float(re[Qe > 0.5].max() / r0) if (Qe > 0.5).any() else 0.0
    return out


def main():
    t0 = time.time()
    rows = []

    def do(M, mode, foot, j=0.1, N=2000):
        a0 = FOOTINGS[foot]
        sig = a0 * MS2_TO_KPCGYR2 / (2 * np.pi * G)
        row = measure(run(M, mode, a0, j, N), sig)
        row["footing"] = foot
        rows.append(row)
        print(f"{mode:6s} {foot:9s} M={M:.0e} j={j} N={N}: R={row['R']:.3f} P={row['P']:.3f} "
              f"r0={row['r0']:.3g} fit={row['fit_rms']:.3f} dE={row['dE']:+.4f} steps={row['nstep']}"
              + (f" Qcore={row['Q_core']:.2f} fQ={row['frac_Q_gt_half']:.2f} rQ/r0={row['rQ_half_over_r0']:.2f}"
                 if mode != "N" else ""), flush=True)
        return row

    if MUTATE:
        for M in MASSES:
            do(M, "MUTATE", "canonical")
        json.dump(rows, open(os.path.join(HERE, "x65_results_MUTATE.json"), "w"), indent=1)
        print(f"wall {time.time() - t0:.0f} s")
        return 0

    for M in MASSES:
        do(M, "N", "canonical")              # N does not depend on a0; the footing tag only sets Σ_a0
    for foot in FOOTINGS:
        for M in MASSES:
            do(M, "G", foot)
    for j in (0.05, 0.2):
        for M in (1e10, 1e11):
            do(M, "N", "canonical", j=j)
            do(M, "G", "canonical", j=j)
    for M in (1e10, 1e11):
        do(M, "G", "canonical", N=1000)

    verdict = grade(rows)
    json.dump(dict(rows=rows, verdict=verdict), open(os.path.join(HERE, "x65_results.json"), "w"), indent=1)
    print(json.dumps(verdict, indent=1))
    print(f"wall {time.time() - t0:.0f} s")
    return 0 if verdict["status"] == "GRADED" else 1


def pick(rows, **kw):
    hit = [r for r in rows if all(r[k] == v for k, v in kw.items())]
    assert len(hit) == 1, kw
    return hit[0]


def grade(rows):
    v = dict(status="GRADED", footings={})
    Nrows = [r for r in rows if r["mode"] == "N" and r["j"] == 0.1]
    if max(abs(r["dE"]) for r in rows if r["mode"] == "N") > 0.02:
        v["status"] = "UNDECIDED (E1 energy)"
    if any(r["s1_viol"] for r in rows):
        v["status"] = "UNDECIDED (S1 Q nonzero on single-valued map)"
    mut = None
    pm = os.path.join(HERE, "x65_results_MUTATE.json")
    if os.path.exists(pm):
        mut = {r["M"]: r for r in json.load(open(pm))}
    for foot, a0 in FOOTINGS.items():
        sig = a0 * MS2_TO_KPCGYR2 / (2 * np.pi * G)
        sig_can = FOOTINGS["canonical"] * MS2_TO_KPCGYR2 / (2 * np.pi * G)
        f = {}
        RN = {r["M"]: r["R"] * sig_can / sig for r in Nrows}     # restate N on this footing's Σ_a0
        fitN = {r["M"]: r["fit_ok"] for r in Nrows}
        Gr = {M: pick(rows, M=M, mode="G", footing=foot, j=0.1, N=2000) for M in MASSES}
        f["per_mass"] = {f"{M:.0e}": dict(R_N=RN[M], R_G=Gr[M]["R"], P_G=Gr[M]["P"], fit_N=fitN[M],
                                          fit_G=Gr[M]["fit_ok"], Q_core=Gr[M]["Q_core"]) for M in MASSES}
        if any(Gr[M]["Q_core"] < 0.7 for M in MASSES):
            f["gate"] = "GATE INACTIVE in " + ",".join(f"{M:.0e}" for M in MASSES if Gr[M]["Q_core"] < 0.7)
        S = [M for M in MASSES if fitN[M] and RN[M] < 0.7]
        if not S:
            f["verdict"] = "UNDECIDED (no below-floor mass)"
        else:
            RG = np.array([Gr[M]["R"] for M in S])
            lift = np.median(np.log10(RG / np.array([RN[M] for M in S])))
            spread = np.log10(RG.max() / RG.min())
            if np.all((RG >= 0.67) & (RG <= 1.5)) and spread <= 0.2:
                f["verdict"] = "FLOOR EMERGES"
            elif np.all((RG >= 2.6) & (RG <= 5.9)):
                f["verdict"] = "SLAB READING"
            elif lift > 0.1:
                f["verdict"] = "RAISES, NO FLOOR"
            elif abs(lift) <= 0.1:
                f["verdict"] = "NO EFFECT"
            else:
                f["verdict"] = "LOWERS (unlisted; reported)"
            f.update(S=[f"{M:.0e}" for M in S], median_lift_dex=float(lift), spread_dex=float(spread))
        above = [M for M in MASSES if RN[M] > 1.5]
        if above:
            f["max_rule"] = "REPRODUCED" if all(abs(np.log10(Gr[M]["R"] / RN[M])) <= 0.1 for M in above) else "BROKEN"
        flags = []
        if foot == "canonical":
            for j in (0.05, 0.2):
                for M in (1e10, 1e11):
                    if abs(np.log10(pick(rows, M=M, mode="G", footing=foot, j=j, N=2000)["R"] / Gr[M]["R"])) > 0.15:
                        flags.append(f"j-DEPENDENT ({M:.0e}, j={j})")
            for M in (1e10, 1e11):
                if abs(np.log10(pick(rows, M=M, mode="G", footing=foot, j=0.1, N=1000)["R"] / Gr[M]["R"])) > 0.1:
                    flags.append(f"UNRESOLVED ({M:.0e})")
            if mut and all(abs(np.log10(mut[M]["R"] / Gr[M]["R"])) <= 0.01 for M in MASSES):
                flags.append("HARNESS INSENSITIVE")
            if mut:
                f["mutate_R"] = {f"{M:.0e}": mut[M]["R"] for M in MASSES}
        f["flags"] = sorted(set(flags))
        v["footings"][foot] = f
    return v


if __name__ == "__main__":
    sys.exit(main())
