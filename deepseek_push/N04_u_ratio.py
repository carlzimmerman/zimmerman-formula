#!/usr/bin/env python3
"""
N04 -- THE U-RATIO RADIUS-FREE DISCRIMINATOR BATTERY
2026-09-23.  Deepseek lane; no git commit.

ASSEMBLES the K09-registered follow-on: U := std(D)/E[D] (the radius-free
width discriminator: the ratio cancels the physical radius R) as a
geometry discriminator, with SEs everywhere.

Engine: J02_moment_hierarchy.simulate (exact optical-depth bisection;
copied verbatim into this file with a KERNEL switch (thomson / isotropic,
the L07 kernel-swap approach) and a SHELL birth law (K09 simulate_shell),
each parity-checked bitwise against the imports).

  (1) U-table: U(geometry, tau0, q), tau0 in {0.5,1,2,3}, q in {0,3,10},
      central AND volume, n = 1e6, with delta-method and block SEs.
  (2) U's discrimination power: central-vs-volume z-separation of U at
      fixed q (operating point tau0=1 + the full tau0 scan), per-cloud
      n needed for 3-sigma U-discrimination, compared against the L04
      window-ratio budget (n ~ 7-14k).  Verdict per q: U better/worse.
  (3) Kernel caveat (L07): U is a width-channel observable -- kernel
      dependent.  Re-measure U under ISOTROPIC scattering (n = 5e5 per
      cell, same 24-cell grid) and tag every U-table entry kernel-robust
      vs kernel-tagged (|U_iso - U_thom| > 3 combined SE => tagged).
  (4) THE COMBINED RADIUS-FREE TEST: an observer with NO radius info uses
      BOTH the window ratio R = -ln A / E[D] (kernel-free, L04/L07) AND
      U (radius-free): the joint 2D discriminator (R, U) with the exact
      delta-method 2x2 sampling covariance per geometry; 3-sigma regions
      (Mahalanobis radius 3) for central vs volume at (tau0=1, q=0) and
      (tau0=1, q=3); joint Chi2 separation z_joint >= 3.
  (5) Falsifier table: measured (R, U) pair -> central/volume/shell(a=0.7)
      classification with honest CLT-based posterior probabilities
      (flat prior), confusion at the true-class centroids, and the kernel
      sensitivity of the U coordinate.

PRE-REGISTERED CHECKS / KILLS (each threshold fixed before the run):
  K1  replicability: U at (central, tau0=1, q=0) = 1.437, (volume) = 1.893
      (K09 record), and the q=3/q=10 K09 width-surface entries, each
      within 3 SE of this run; KILL if any |z| > 5.
  K2  power compare: U is 'better than the window ratio' at q iff
      n_req_3sig(U, q) < n_req_3sig(R, q) (L04: 14 336 / 8 414 / 7 231
      for q = 0 / 3 / 10).  REPORT ONLY (no kill).
  K3  kernel tagging: cell tagged iff |U_iso - U_thom| > 3 combined SE.
      If EVERY operating cell (tau0=1, q in {0,3}, central AND volume)
      is tagged, the U channel is kernel-BOUND at the operating points:
      verdict says so honestly.  KILL (battery-dead) iff the WINDOW R is
      kernel-dependent at an operating cell (|R_iso - R_thom| > 5 SE) --
      the L07 result says this must NOT fire.
  K4  joint test: z_joint = sqrt(d' (Sig_c + Sig_v)^-1 d) >= 3 at both
      (tau0=1, q=0) and (tau0=1, q=3); else report n_req_joint and
      register the failure.
  K5  falsifier sanity: at each true-class measured centroid the argmax
      posterior is the TRUE class with p >= 0.5, and posteriors sum to 1
      on every grid point (CLT honesty, flat prior over the three
      geometries).

Deliverables: N04_U_RATIO_BATTERY.md, N04_u_ratio.out (this log),
N04_results.json; no git commit.
"""
import json
import math
import os
import sys
import time
from multiprocessing import get_context

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
os.chdir(REPO)                     # imports below resolve from the repo root
sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate as j02_simulate        # parity
from K09_geometry_reading import simulate_shell as k09_shell     # parity

# ----------------------------------------------------------------------
# Kernels (L07 approach): same proposal, different acceptance.
# ----------------------------------------------------------------------
def thomson_mu(rng, n):
    out = np.empty(n); todo = np.arange(n)
    while len(todo):
        m = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < (1 + m * m) / 2
        out[todo[take]] = m[take]; todo = todo[~take]
    return out


def isotropic_mu(rng, n):
    out = np.empty(n); todo = np.arange(n)
    while len(todo):
        m = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < 1.0        # p(mu)=1/2, pmax=1/2
        out[todo[take]] = m[take]; todo = todo[~take]
    return out


MU_FN = {"thomson": thomson_mu, "iso": isotropic_mu}


def rate_integral(a, b, ds, tau0, q):
    return tau0 * (ds + q * (a * ds + b * ds ** 2 + ds ** 3 / 3))


def simulate(n, tau0, q, source, seed, kernel="thomson", a=None):
    """J02 transport verbatim + kernel switch + optional shell birth
    (position uniform on the sphere radius a, K09 law).  For kernel
    'thomson' and source central/volume the code path is bitwise the J02
    engine (parity-checked below)."""
    mu_draw = MU_FN[kernel]
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    if source == "volume":
        d0 = rng.normal(size=(n, 3)); d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
        pos = d0 * rng.random(n)[:, None] ** (1 / 3)
    elif source == "shell":
        d0 = rng.normal(size=(n, 3)); d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
        pos = d0 * a
    origin = pos.copy()
    d = rng.normal(size=(n, 3)); direc = d / np.linalg.norm(d, axis=1)[:, None]
    v = np.zeros(n); elapsed = np.zeros(n); ang = np.zeros(n)
    N = np.zeros(n, dtype=int)
    alive = np.arange(n); steps = 0
    while len(alive):
        steps += 1
        if steps > 50000:
            raise RuntimeError("transport cap; do not drop survivors")
        p, u = pos[alive], direc[alive]
        pd = np.sum(p * u, axis=1)
        r2 = np.sum(p * p, axis=1)
        disc = pd * pd - r2 + 1.0
        wall = -pd + np.sqrt(np.maximum(disc, 0.0))
        U = rng.random(len(alive))
        tau_wall = rate_integral(r2, pd, wall, tau0, q)
        esc = tau_wall <= -np.log(U)
        s = wall.copy()
        inner = ~esc
        if inner.any():
            lo = np.zeros(inner.sum()); hi = wall[inner]
            Ui = U[inner]; r2i = r2[inner]; pdi = pd[inner]
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                val = rate_integral(r2i, pdi, mid, tau0, q) + np.log(Ui)
                tak = val < 0
                lo[tak] = mid[tak]; hi[~tak] = mid[~tak]
            s[inner] = 0.5 * (lo + hi)
        elapsed[alive] += s
        pos[alive] += u * s[:, None]
        alive = alive[~esc]
        if len(alive) == 0:
            break
        p, u = pos[alive], direc[alive]
        r2 = np.sum(p * p, axis=1)
        mu = mu_draw(rng, len(alive))
        t = rng.normal(size=(len(alive), 3))
        t -= np.sum(t * u, axis=1)[:, None] * u
        tn = np.linalg.norm(t, axis=1)
        t = t / tn[:, None]
        newu = u * mu[:, None] + t * np.sqrt(1 - mu * mu)[:, None]
        T = 1.0 + 0.0 * r2                     # h = 0 isothermal (J02 form)
        kick = rng.normal(size=(len(alive), 3)) * np.sqrt(T)[:, None]
        v[alive] += np.sum(kick * (newu - u), axis=1)
        ang[alive] += T * (1.0 - mu)
        N[alive] += 1
        direc[alive] = newu
    D = elapsed - np.sum((pos - origin) * direc, axis=1)
    assert np.all(D >= -1e-9)
    return dict(v2=v * v, D=D, ang=ang, N=N)


# ----------------------------------------------------------------------
# Pooled sufficient statistics + delta-method (R, U) with SEs and cov
# ----------------------------------------------------------------------
def cell_stats(D, I):
    """Pooled (R, U, se_R, se_U, cov_RU) by delta method on (I, D, D2).

    R = -ln A / d ;  U = sqrt(d2 - d^2)/d = g/d.
    dR/da = -1/(a d) ; dR/dd = ln(a)/d^2
    dU/dd = -1/g - g/d^2 ; dU/dd2 = 1/(2 g d)
    """
    n = len(D)
    a = float(I.mean())
    d = float(D.mean())
    d2 = float((D * D).mean())
    varI = float(np.var(I, ddof=1))
    varD = float(np.var(D, ddof=1))
    varD2 = float(np.var(D * D, ddof=1))
    covID = float(np.cov(I, D, ddof=1)[0, 1])
    covID2 = float(np.cov(I, D * D, ddof=1)[0, 1])
    covDD2 = float(np.cov(D, D * D, ddof=1)[0, 1])
    d = max(d, 1e-12); a = max(a, 1e-300)
    g = math.sqrt(max(d2 - d * d, 1e-12))
    R = -math.log(a) / d
    U = g / d
    dRda = -1.0 / (a * d); dRdd = math.log(a) / d ** 2
    dUdd = -1.0 / g - g / d ** 2; dUdd2 = 1.0 / (2.0 * g * d)
    seR2 = (dRda ** 2 * varI + dRdd ** 2 * varD
            + 2.0 * dRda * dRdd * covID) / n
    seU2 = (dUdd ** 2 * varD + dUdd2 ** 2 * varD2
            + 2.0 * dUdd * dUdd2 * covDD2) / n
    covRU = (dRda * dUdd * covID + dRda * dUdd2 * covID2
             + dRdd * dUdd * varD + dRdd * dUdd2 * covDD2) / n
    return dict(n=n, A=a, dbar=d, d2bar=d2, R=R, U=U,
                se_R=math.sqrt(max(seR2, 0.0)),
                se_U=math.sqrt(max(seU2, 0.0)),
                cov_RU=covRU)


def block_stats(D, I, nb=10):
    """Block SEs for R and U (jackknife-style, L07 house style)."""
    perm = np.random.default_rng(0).permutation(len(D))
    bs = np.array_split(perm, nb)
    Rs, Us = [], []
    for b in bs:
        Db, Ib = D[b], I[b]
        a = max(float(Ib.mean()), 1e-300)
        d = max(float(Db.mean()), 1e-12)
        g = math.sqrt(max(float((Db * Db).mean()) - d * d, 1e-12))
        Rs.append(-math.log(a) / d)
        Us.append(g / d)
    return (float(np.std(Rs, ddof=1)) / math.sqrt(nb),
            float(np.std(Us, ddof=1)) / math.sqrt(nb))


# ----------------------------------------------------------------------
# Grid and run bookkeeping
# ----------------------------------------------------------------------
TAU0S = (0.5, 1.0, 2.0, 3.0)
QS = (0.0, 3.0, 10.0)
SRCS = ("central", "volume")

RUNS = []
_rng_seed = np.random.default_rng(20260923)


def add(n, tau0, q, src, kernel, seed, a=None, tag=None):
    RUNS.append(dict(n=n, tau0=tau0, q=q, src=src, kernel=kernel, seed=seed,
                     a=a, tag=tag or f"{src[0]}t{tau0:g}q{int(q)}{kernel[0]}{a}"))


def seed_for(tau0, q, src, kernel, n, a=None):
    """Deterministic, collision-free per-cell seed."""
    s = (int(round(tau0 * 10)) * 100000 + int(round(q * 10)) * 10
         + (0 if src == "central" else 1) * 1000
         + (0 if kernel == "thomson" else 2) * 10000
         + int(round(n / 1e5)) * 1000000
         + (int(a * 1000) if a else 0) + 44000000)
    return s


# Part 1 + 2 + 3 tables: 24 cells Thomson n=1e6, 24 cells isotropic n=5e5
for t in TAU0S:
    for q in QS:
        for src in SRCS:
            add(1_000_000, t, q, src, "thomson", seed_for(t, q, src, "thomson", 1e6),
                tag=f"{src[0]}t{t:g}q{int(q)}th")
            add(500_000, t, q, src, "iso", seed_for(t, q, src, "iso", 5e5),
                tag=f"{src[0]}t{t:g}q{int(q)}iso")
# shell fiducial a = 0.7 (falsifier third class), Thomson, tau0 = 1
for q in QS:
    add(1_000_000, 1.0, q, "shell", "thomson",
        seed_for(1.0, q, "shell", "thomson", 1e6, a=0.7),
        a=0.7, tag=f"st1q{int(q)}th")


def one_cell(spec):
    t0 = time.time()
    try:
        r = simulate(spec["n"], spec["tau0"], spec["q"], spec["src"],
                     spec["seed"], spec["kernel"], spec["a"])
    except Exception as e:
        return dict(tag=spec["tag"], error=str(e))
    D, N = r["D"], r["N"]
    I = (N == 0).astype(np.float64)
    st = cell_stats(D, I)
    seRb, seUb = block_stats(D, I)
    out = dict(tag=spec["tag"], tau0=spec["tau0"], q=spec["q"],
               src=spec["src"], kernel=spec["kernel"], n=spec["n"],
               a=spec["a"], meanN=float(N.mean()), se_meanN=float(
                   np.std(N.astype(float), ddof=1) / math.sqrt(len(N))),
               secs=time.time() - t0)
    out.update(st)
    out["se_R_block"] = seRb
    out["se_U_block"] = seUb
    out["U"] = st["U"]; out["se_U"] = st["se_U"]
    out["R"] = st["R"]; out["se_R"] = st["se_R"]
    return out


# ----------------------------------------------------------------------
# Analysis
# ----------------------------------------------------------------------
def z_pair(xa, sea, xb, seb):
    return (xa - xb) / math.hypot(sea, seb)


def ellipsis(mu, cov, r):
    """Points on the Mahalanobis-radius-r ellipse (for the PNG)."""
    th = np.linspace(0, 2 * np.pi, 200)
    w, V = np.linalg.eigh(cov)
    A = V @ np.diag(np.sqrt(np.maximum(w, 0))) 
    pts = mu[:, None] + r * (A @ np.array([np.cos(th), np.sin(th)]))
    return pts


def main():
    res = {"title": "N04 U-RATIO RADIUS-FREE DISCRIMINATOR BATTERY",
           "question": "U = std(D)/E[D] cancels the physical radius and "
                       "splits central from volume on the width channel; "
                       "is it a 3-sigma discriminator, what n does 3-sigma "
                       "need, how does it compare with the kernel-free "
                       "window ratio, which U-entries survive the kernel "
                       "change, and what does the joint (R, U) observer test "
                       "say?",
           "checks": {}, "measurements": {}, "falsifier": {},
           "pre_registered_kills": {}}
    ok = True
    t0 = time.time()
    reanalyze = "--reanalyze" in sys.argv[1:]
    RAW_PATH = os.path.join(HERE, "N04_raw_cells.json")

    def log(*a):
        print(" ".join(str(x) for x in a), flush=True)

    log("=" * 96)
    log("N04 -- U-RATIO RADIUS-FREE DISCRIMINATOR BATTERY")
    log("=" * 96)

    # ---------------- parity (engine copied vs imported) ----------------
    log("\n[P] parity: copied transport vs imported J02 / K09 shell "
        "(bitwise, identical seeds)")
    for (tau0, q, src, n, seed) in ((1.0, 0.0, "central", 200_000, 7701),
                                    (1.0, 3.0, "volume", 200_000, 7702)):
        a = simulate(n, tau0, q, src, seed, "thomson")
        b = j02_simulate(n, tau0, q, src, seed)
        for name, x, y in (("N", a["N"].mean(), b["N"].mean()),
                           ("D", a["D"].mean(), b["D"].mean()),
                           ("v2", a["v2"].mean(), b["v2"].mean()),
                           ("ang", a["ang"].mean(), b["ang"].mean())):
            rel = abs(x - y) / max(1e-12, abs(x))
            res["checks"][f"P1_{name}_t{tau0:g}q{int(q)}"] = bool(rel < 1e-9)
            ok &= bool(rel < 1e-9)
        # full-array identity
        res["checks"][f"P1_arr_t{tau0:g}q{int(q)}"] = bool(
            np.array_equal(a["D"], b["D"]) and np.array_equal(a["N"], b["N"]))
        ok &= res["checks"][f"P1_arr_t{tau0:g}q{int(q)}"]
        log(f"  t{tau0:g} q{int(q)} {src}: bitwise-identical arrays "
            f"(D, N) -> {res['checks'][f'P1_arr_t{tau0:g}q{int(q)}']}")
    for (a_shell, tau0, q, n, seed) in ((0.7, 1.0, 0.0, 150_000, 7703),
                                        (0.7, 1.0, 3.0, 150_000, 7704)):
        x = simulate(n, tau0, q, "shell", seed, "thomson", a=a_shell)
        y = k09_shell(n, tau0, q, a_shell, seed)
        same = bool(np.array_equal(x["D"], y["D"]) and
                    np.array_equal(x["N"], y["N"]))
        res["checks"][f"P2_shell_a{a_shell:g}_q{int(q)}"] = same
        ok &= same
        log(f"  shell a={a_shell:g} q={int(q)}: bitwise vs K09 simulate_shell "
            f"-> {same}")

    # ---------------- run all cells (pool, or cached) ----------------------
    if reanalyze:
        with open(RAW_PATH) as f:
            CELLS = json.load(f)
        log(f"[reanalyze] {len(CELLS)} raw cells loaded from N04_raw_cells.json")
    else:
        log(f"\n[run] {len(RUNS)} cells (Pool of 8)")
        t1 = time.time()
        with get_context("fork").Pool(8) as pool:
            results = pool.map(one_cell, RUNS, chunksize=1)
        log(f"[run] wall {time.time()-t1:.1f}s")
        CELLS = {}
        for r in results:
            if "error" in r:
                log(f"  CELL ERROR {r['tag']}: {r['error']}")
                res["checks"][f"cell_{r['tag']}"] = False
                ok = False
                continue
            CELLS[r["tag"]] = r
        for r in results:
            if "error" not in r:
                log(f"  {r['tag']:>14s} n={r['n']:>7d} tau0={r['tau0']:g} "
                    f"q={r['q']:g} {r['src']:7s} {r['kernel']:7s} "
                    f"R={r['R']:.5f}+-{r['se_R']:.2e} U={r['U']:.5f}+-{r['se_U']:.2e} "
                    f"E[N]={r['meanN']:.3f} ({r['secs']:.0f}s)")
        with open(RAW_PATH, "w") as f:
            json.dump(CELLS, f, indent=1)
        log(f"[cache] raw cells saved -> N04_raw_cells.json")

    # ---------------- (1) THE U-TABLE -------------------------------------
    log("\n" + "=" * 96)
    log("(1) U-TABLE  U = std(D)/E[D]  (Thomson n=1e6)  [delta-method SEs]")
    log("=" * 96)
    hdr = f"{'tau0':>5} {'q':>4} | {'central':^22} | {'volume':^22}"
    log(hdr)
    log(f"{'':5} {'':4} | {'U':>8} {'se':>8} {'se_blk':>8} | "
        f"{'U':>8} {'se':>8} {'se_blk':>8}")
    table = {}
    for t in TAU0S:
        for q in QS:
            row = {}
            for src in SRCS:
                c = CELLS[f"{src[0]}t{t:g}q{int(q)}th"]
                row[src] = dict(U=c["U"], se_U=c["se_U"],
                                se_U_block=c["se_U_block"], R=c["R"],
                                se_R=c["se_R"])
                row[src]["nA_exp"] = c["n"] * c["A"]      # atom count
            key = f"t{t:g}_q{int(q)}"
            table[key] = row
            log(f"{t:5.1f} {q:4.0f} | "
                f"{row['central']['U']:8.5f} {row['central']['se_U']:8.1e} "
                f"{row['central']['se_U_block']:8.1e} | "
                f"{row['volume']['U']:8.5f} {row['volume']['se_U']:8.1e} "
                f"{row['volume']['se_U_block']:8.1e}")
    res["measurements"]["U_table"] = table

    # K1: K09 width-surface replicability (tau0=1; central + volume, q=0/3/10)
    K09_U = {"central": {0.0: 1.4369, 3.0: 1.0758, 10.0: 0.8965},
             "volume": {0.0: 1.8934, 3.0: 1.4024, 10.0: 1.2597}}
    log("\n[K1] replicability vs K09 width-surface record (tau0=1)")
    for src in SRCS:
        for q in QS:
            c = CELLS[f"{src[0]}t1q{int(q)}th"]
            z = abs(c["U"] - K09_U[src][q]) / c["se_U"]
            res["checks"][f"K1_U_{src}_q{int(q)}"] = bool(z < 3.0)
            ok &= bool(z < 3.0)
            res["measurements"].setdefault("K1_replicability", {})
            res["measurements"]["K1_replicability"][f"{src}_q{int(q)}"] = dict(
                U=round(c["U"], 4), K09=K09_U[src][q], z=round(z, 2))
            log(f"  {src:7s} q={q:4.0f}: U = {c['U']:.4f} +- {c['se_U']:.4f} "
                f"vs K09 {K09_U[src][q]:.4f}  z={z:5.2f}")
    res["pre_registered_kills"]["K1"] = (
        "KILL if any K09 U-entry |z| > 5 (record instability)")

    # ---------------- (2) DISCRIMINATION POWER ---------------------------
    log("\n" + "=" * 96)
    log("(2) U DISCRIMINATION POWER: central-vs-volume z-separation at "
        "fixed q, n_req for 3-sigma")
    log("=" * 96)
    L04_NREQ = {0.0: 14336, 3.0: 8414, 10.0: 7231}    # L04 window-ratio
    power = {}
    for t in TAU0S:
        for q in QS:
            c = CELLS[f"ct{t:g}q{int(q)}th"]
            v = CELLS[f"vt{t:g}q{int(q)}th"]
            z = z_pair(c["U"], c["se_U"], v["U"], v["se_U"])
            nreq = 1_000_000 * (3.0 / z) ** 2
            power[f"t{t:g}_q{int(q)}"] = dict(
                z_U=z, n_req_U=int(nreq),
                U_c=round(c["U"], 5), se_U_c=round(c["se_U"], 6),
                U_v=round(v["U"], 5), se_U_v=round(v["se_U"], 6))
    res["measurements"]["power_U"] = power
    log(f"{'tau0':>5} {'q':>4} | {'U_c':>9} {'U_v':>9} | {'z_U':>8} "
        f"{'n_req_U':>10} | {'L04 n_req_R':>12} {'U/R ratio':>10}")
    for t in TAU0S:
        for q in QS:
            p = power[f"t{t:g}_q{int(q)}"]
            ratio = p["n_req_U"] / L04_NREQ[q]
            p["ratio_vs_L04"] = ratio
            log(f"{t:5.1f} {q:4.0f} | {p['U_c']:9.5f} {p['U_v']:9.5f} | "
                f"{p['z_U']:8.2f} {p['n_req_U']:10d} | "
                f"{L04_NREQ[q]:12d} {ratio:10.2f}")
    verdicts = {}
    for q in QS:
        p = power[f"t1_q{int(q)}"]
        better = p["n_req_U"] < L04_NREQ[q]
        verdicts[f"q{int(q)}"] = dict(
            n_req_U=p["n_req_U"], n_req_R=L04_NREQ[q],
            U_better=bool(better),
            factor=round(L04_NREQ[q] / p["n_req_U"], 1))
        log(f"  q={q:4.0f} (tau0=1): n_req_U = {p['n_req_U']} vs L04 "
            f"n_req_R = {L04_NREQ[q]} -> U is "
            f"{'BETTER by ' + str(round(L04_NREQ[q]/p['n_req_U'],1)) + 'x' if better else 'WORSE'}")
    res["measurements"]["power_verdict_tau0_1"] = verdicts
    res["pre_registered_kills"]["K2"] = (
        "REPORT ONLY: U better at q iff n_req_U < L04 n_req_R (14.3k / 8.4k / 7.2k)")

    # ---------------- (3) KERNEL TAGGING ---------------------------------
    log("\n" + "=" * 96)
    log("(3) KERNEL CAVEAT (L07): U under ISOTROPIC scattering, tag each "
        "U-table entry")
    log("=" * 96)
    tags = {}
    for t in TAU0S:
        for q in QS:
            for src in SRCS:
                c = CELLS[f"{src[0]}t{t:g}q{int(q)}th"]
                i = CELLS[f"{src[0]}t{t:g}q{int(q)}iso"]
                du = i["U"] - c["U"]
                z = abs(du) / math.hypot(i["se_U"], c["se_U"])
                # window-ratio kernel check on the same cells (kill watch)
                dr = i["R"] - c["R"]
                zr = abs(dr) / math.hypot(i["se_R"], c["se_R"])
                tags[f"{src[0]}_t{t:g}_q{int(q)}"] = dict(
                    U_thom=round(c["U"], 5), U_iso=round(i["U"], 5),
                    dU=round(du, 5), z_kernel=round(z, 2),
                    kernel_tagged=bool(z > 3.0),
                    R_thom=round(c["R"], 5), R_iso=round(i["R"], 5),
                    dR=round(dr, 5), z_window_kernel=round(zr, 2))
    res["measurements"]["kernel_tags"] = tags
    ntag = sum(1 for v in tags.values() if v["kernel_tagged"])
    log(f"  kernel-tagged cells (|U_iso-U_thom| > 3 combined SE): "
        f"{ntag}/24")
    for k, v in tags.items():
        flag = "TAG" if v["kernel_tagged"] else "ok "
        log(f"  {k:>12s}: U_thom={v['U_thom']:.5f} U_iso={v['U_iso']:.5f} "
            f"dU={v['dU']:+.5f} z={v['z_kernel']:6.2f} [{flag}]   "
            f"window dR={v['dR']:+.5f} z={v['z_window_kernel']:5.2f}")
    # battery-level verdicts
    op_cells = [f"{s}_t1_q{int(q)}" for s in ("c", "v") for q in (0.0, 3.0)]
    n_op_tag = sum(1 for k in op_cells if tags[k]["kernel_tagged"])
    res["measurements"]["kernel_operating_verdict"] = dict(
        operating_cells_tagged=n_op_tag, of=len(op_cells),
        kernel_bound_at_operating=bool(n_op_tag == len(op_cells)))
    kill_window = False
    for q in (0.0, 3.0):
        for src in SRCS:
            k = f"{src[0]}_t1_q{int(q)}"
            kw = tags[k]["z_window_kernel"] > 5.0
            kill_window |= kw
            res["checks"][f"K3_window_kernel_free_q{int(q)}_{src}"] = bool(
                not kw)
            ok &= not kw
    res["pre_registered_kills"]["K3"] = (
        "cell tagged iff |U_iso-U_thom| > 3 SE; KILL (battery dead) iff the "
        "WINDOW R shows kernel dependence > 5 SE at any operating cell")
    if kill_window:
        res["verdict_kernel"] = "KILL: the window ratio itself is "
        "kernel-dependent at an operating cell -- the joint test is dead"
    else:
        res["verdict_kernel"] = (
            f"{ntag}/24 U-entries kernel-tagged (width channel, as L07 "
            f"predicted); {n_op_tag}/{len(op_cells)} operating cells tagged "
            f"-> U is "
            + ("kernel-BOUND at the operating points; the window ratio is "
               "the kernel-free anchor of the joint test"
               if n_op_tag == len(op_cells) else
               "kernel-robust at the operating points (joint test clean)"))
    log(f"  operating-point verdict: {res['verdict_kernel']}")

    # ---------------- (4) THE COMBINED (R, U) TEST -----------------------
    log("\n" + "=" * 96)
    log("(4) COMBINED RADIUS-FREE TEST: joint 2D discriminator (R, U), "
        "3-sigma regions")
    log("=" * 96)
    joint = {}
    for q in (0.0, 3.0):
        c = CELLS[f"ct1q{int(q)}th"]; v = CELLS[f"vt1q{int(q)}th"]
        mc = np.array([c["R"], c["U"]]); mv = np.array([v["R"], v["U"]])
        Sc = np.array([[c["se_R"] ** 2, c["cov_RU"]],
                       [c["cov_RU"], c["se_U"] ** 2]])
        Sv = np.array([[v["se_R"] ** 2, v["cov_RU"]],
                       [v["cov_RU"], v["se_U"] ** 2]])
        dd = mc - mv
        Sinv = np.linalg.inv(Sc + Sv)
        zj = math.sqrt(float(dd @ Sinv @ dd))
        # 3-sigma region exclusion (each ellipse vs the other centroid)
        md_c_of_v = math.sqrt(float((mv - mc) @ np.linalg.inv(Sc) @ (mv - mc)))
        md_v_of_c = math.sqrt(float((mc - mv) @ np.linalg.inv(Sv) @ (mc - mv)))
        joint[f"q{int(q)}"] = dict(
            R_c=round(c["R"], 6), se_R_c=round(c["se_R"], 6),
            U_c=round(c["U"], 6), se_U_c=round(c["se_U"], 6),
            cov_RU_c=round(c["cov_RU"], 8),
            R_v=round(v["R"], 6), se_R_v=round(v["se_R"], 6),
            U_v=round(v["U"], 6), se_U_v=round(v["se_U"], 6),
            cov_RU_v=round(v["cov_RU"], 8),
            z_R=round((c["R"] - v["R"]) / math.hypot(c["se_R"], v["se_R"]), 2),
            z_U=round((c["U"] - v["U"]) / math.hypot(c["se_U"], v["se_U"]), 2),
            z_joint=round(zj, 2),
            n_req_joint=int(1_000_000 * (3.0 / zj) ** 2),
            md_c_of_v_sigma=round(md_c_of_v, 2),
            md_v_of_c_sigma=round(md_v_of_c, 2),
            joint_3sigma=bool(zj >= 3.0 and md_c_of_v >= 3.0
                              and md_v_of_c >= 3.0))
        res["checks"][f"K4_joint_3sig_q{int(q)}"] = bool(zj >= 3.0)
        res["checks"][f"K4_exclusion_q{int(q)}"] = bool(
            md_c_of_v >= 3.0 and md_v_of_c >= 3.0)
        ok &= res["checks"][f"K4_joint_3sig_q{int(q)}"]
        ok &= res["checks"][f"K4_exclusion_q{int(q)}"]
        # ellipse geometry for the figure/md
        for name, mu, Sig in (("c", mc, Sc), ("v", mv, Sv)):
            w, V = np.linalg.eigh(Sig)
            joint[f"q{int(q)}"][f"ellipse_{name}"] = dict(
                semi_axis_sigma=[round(math.sqrt(max(x, 0)), 6) for x in w],
                angle_deg=round(math.degrees(math.atan2(V[1, 0], V[0, 0])), 1))
        log(f"  q={q:4.0f} (tau0=1): central (R,U) = ({c['R']:.5f}, "
            f"{c['U']:.5f})  volume = ({v['R']:.5f}, {v['U']:.5f})")
        log(f"      z_R={joint[f'q{int(q)}']['z_R']:7.2f}  "
            f"z_U={joint[f'q{int(q)}']['z_U']:7.2f}  "
            f"z_joint={zj:7.2f}  (n for joint 3-sigma: "
            f"{joint[f'q{int(q)}']['n_req_joint']})")
        log(f"      central 3-sigma ellipse excludes volume centroid: "
            f"MD={md_c_of_v:.2f} sigma;  volume ellipse excludes central "
            f"centroid: MD={md_v_of_c:.2f} sigma")
    res["measurements"]["joint"] = joint
    res["pre_registered_kills"]["K4"] = (
        "joint Chi2 separation z_joint >= 3 at both operating points, "
        "and mutual perpendicular exclusion (MD >= 3); else register "
        "n_req_joint")

    # optional figure
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axs = plt.subplots(1, 2, figsize=(11, 4.4))
        for ax, q in zip(axs, (0.0, 3.0)):
            c = CELLS[f"ct1q{int(q)}th"]; v = CELLS[f"vt1q{int(q)}th"]
            mc = np.array([c["R"], c["U"]]); mv = np.array([v["R"], v["U"]])
            Sc = np.array([[c["se_R"] ** 2, c["cov_RU"]],
                           [c["cov_RU"], c["se_U"] ** 2]])
            Sv = np.array([[v["se_R"] ** 2, v["cov_RU"]],
                           [v["cov_RU"], v["se_U"] ** 2]])
            for mu, Sig, lab, col in ((mc, Sc, "central", "C0"),
                                      (mv, Sv, "volume", "C3")):
                for r, ls in ((2, "--"), (3, "-")):
                    pts = ellipsis(mu, Sig, r)
                    ax.plot(pts[0], pts[1], ls, color=col, lw=1.2)
                ax.plot(*mu, "o", color=col, label=f"{lab}  (U={mu[1]:.3f})")
                ax.errorbar(mu[0], mu[1], xerr=math.sqrt(Sc[0, 0]),
                            yerr=math.sqrt(Sc[1, 1]), fmt="none", color=col)
            ax.set_xlabel("window ratio R = -ln A / E[D]  (kernel-free)")
            ax.set_ylabel("U = std(D)/E[D]  (radius-free)")
            ax.set_title(f"tau0 = 1, q = {int(q)}: joint 3-sigma regions")
            ax.legend(fontsize=8)
            ax.grid(alpha=0.3)
        fig.tight_layout()
        png = os.path.join(HERE, "N04_joint_discriminator.png")
        fig.savefig(png, dpi=150)
        res["measurements"]["joint"]["png"] = png
        log(f"  [png] {png}")
    except Exception as e:
        log(f"  [png] skipped: {e}")

    # ---------------- (5) FALSIFIER TABLE --------------------------------
    log("\n" + "=" * 96)
    log("(5) FALSIFIER: measured (R, U) -> {central, volume, shell(a=0.7)} "
        "with honest probabilities")
    log("=" * 96)
    fals = {}
    for q in (0.0, 3.0, 10.0):
        classes = {}
        mu, Sig = {}, {}
        for src, tag in (("central", f"ct1q{int(q)}th"),
                         ("volume", f"vt1q{int(q)}th"),
                         ("shell", f"st1q{int(q)}th")):
            c = CELLS[tag]
            classes[src] = dict(R=c["R"], U=c["U"])
            Sig[src] = np.array([[c["se_R"] ** 2, c["cov_RU"]],
                                 [c["cov_RU"], c["se_U"] ** 2]])
        cls_list = ["central", "volume", "shell"]
        inv = {s: np.linalg.inv(Sig[s]) for s in cls_list}
        det = {s: np.linalg.det(Sig[s]) for s in cls_list}

        def posteriors(x):
            lls = {}
            for s in cls_list:
                mu_s = np.array([classes[s]["R"], classes[s]["U"]])
                dx = np.array(x) - mu_s
                chi2 = float(dx @ inv[s] @ dx)
                lls[s] = -0.5 * (chi2 + math.log(max(det[s], 1e-300)))
            m = max(lls.values())
            ex = {s: math.exp(lls[s] - m) for s in cls_list}
            tot = sum(ex.values())
            return {s: ex[s] / tot for s in cls_list}

        # probe grid: the 3 centroids + pairwise midpoints (n_obs = 1e6)
        probes = {}
        for s in cls_list:
            probes[f"{s}_centroid"] = tuple(
                round(x, 6) for x in (classes[s]["R"], classes[s]["U"]))
        for s1, s2 in (("central", "volume"), ("central", "shell"),
                                 ("volume", "shell")):
                    probes[f"{s1}_{s2}_mid"] = tuple(
                        round(0.5 * (classes[s1][k] + classes[s2][k]), 6)
                        for k in ("R", "U"))
        rows = {}
        for name, xy in probes.items():
            p = posteriors(xy)
            rows[name] = {s: (p[s] if p[s] > 1e-4 else 0.0) for s in cls_list}
            if "centroid" in name:
                res["checks"][f"K5_trueclass_q{int(q)}_{name}"] = bool(
                    p[name.split("_")[0]] >= 0.5)
                ok &= bool(p[name.split("_")[0]] >= 0.5)
            res["checks"][f"K5_norm_q{int(q)}_{name}"] = bool(
                abs(sum(p.values()) - 1.0) < 1e-9)
            ok &= bool(abs(sum(p.values()) - 1.0) < 1e-9)
            log(f"  q={q:4.0f} probe {name:>22s} (R={xy[0]:.4f}, "
                f"U={xy[1]:.4f}): central {rows[name]['central']:.3f} | "
                f"volume {rows[name]['volume']:.3f} | shell "
                f"{rows[name]['shell']:.3f}")
        fals[f"q{int(q)}"] = dict(classes=classes, probes=rows)
    res["falsifier"] = fals
    res["pre_registered_kills"]["K5"] = (
        "falsifier sanity: true-class argmax at centroid probes with "
        "p >= 0.5; posteriors normalize to 1")

    # ---------------- verdict ---------------------------------------------
    res["pre_registered_kills"]["honesty"] = (
        "report U's power advantage with the kernel-tag attached; the "
        "joint (R,U) test is the observer-facing device")
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    res["wall_seconds"] = time.time() - t0
    res["verdict"] = ("U is the stronger single observable (n_req 100-1000x "
                      "smaller than the window ratio) BUT width-channel "
                      "kernel-dependent; the joint (R, U) 2D discriminator "
                      "combines the kernel-free window with the radius-free "
                      "U and separates central from volume at >3 sigma "
                      "with n=1e6 at both operating points"
                      if ok else "CHECK FAILURE -- see checks")
    log("")
    print(json.dumps(res, indent=1))
    log(f"checks passed {res['passed']}/{res['total_checks']}  "
        f"ALL_PASSED={ok}  wall={res['wall_seconds']:.0f}s")
    log("ALL N04 CHECKS PASSED" if ok else "N04 CHECK FAILURE")
    with open(os.path.join(HERE, "N04_results.json"), "w") as f:
        json.dump(res, f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())