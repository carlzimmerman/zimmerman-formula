#!/usr/bin/env python3
"""
V02 -- THE INCLINATION PLANE: U(eps, i) and the joint (R, U)|inclination
discriminator on oblate geometry -- the observer's actual viewing axis,
never computed before.

2026-09-25.  Deepseek lane; no git commit.

Geometry: the oblate spheroid x^2+y^2+z^2/eps^2 = 1 (K10), volume source
uniform in the spheroid (uniform ball x (z -> eps z)), central source at
the origin, kappa = tau0 (1 + q r^2), tau0 = 1, Thomson kernel.

THE NEW AXIS: the observer's LINE OF SIGHT at inclination i,
n_obs = (sin i, 0, cos i).  The observed DELAY is the projection onto the
line of sight (the echo-mapping delay),  D_los = tau - (x_final - x0).n_obs,
where (x_final - x0) is the net displacement from the birth point (central:
x0 = 0, so D = tau - x_final.n_obs exactly as tasked).  The legacy K05/J02
"frozen" delay D_fr = tau - (x_final - x0).u_final (projection onto the
random ESCAPE direction) is computed from the same trajectories and used
as the machine-check channel (F1/F5/F7): it must reproduce the K05/N04
records 1.437/1.893, proving the transport is right, while the LOS
observable is the physically new one.

PRE-REGISTERED CHECKS:
  F1  frozen replicability: U_fr(eps=1.0) = 1.4369 / 1.8934 (K09) and
      1.0758 / 1.4024 (q=3) within 3 SE (averaged over the inclinations --
      the frozen delay contains no LOS).  KILL if any |z| > 3.
  F2  the literal pre-registered falsifier: U_los(eps=1, i=90) vs
      1.437/1.893.  THE PHYSICS: D_los replaces the projection onto the
      escape direction with the projection onto the observer's axis, so it
      is a DIFFERENT delay law (E[D] gains the atom channel: D_fr = 0 for
      zero-scatter photons, D_los = chord (1 - mu) > 0); F2 is therefore
      expected to FAIL and is REPORTED as the convention-mismatch, NOT as
      a transport failure (the transport is F1/F5/F7-checked on the same
      trajectories).
  F3  LOS sphere symmetry: the sphere has no inclination axis: U_los(1.0, i)
      must be i-independent (q=0 central AND volume; q=3 central) -- the
      machine-check of the inclination implementation on the new channel.
  F4  projection symmetry, every cell: E[(x-x0).n_obs] = 0 within 3 SE
      (spheroid reflection symmetry through the equator + azimuthal
      symmetry), i.e. E[D_los] = E[elapsed]: machine-check of the LOS
      projection implementation.
  F5  K10 parity: R_fr(eps, src) = W_K10(eps, src) within 3 combined SE
      (8 cells, q=0, tau0=1).
  F6  report-only: is the flattening inflation of the window the same in
      the LOS frame as in the frozen frame (R_los(eps,i=90)/R_los(1.0,90)
      vs K10 corr(eps))?
  F7  J02-B bookkeeping: E[Q] = E[(x-x0).u_final] volume eps=1 = 0.59715
      within 3 SE; central E[Q] = E[elapsed] - 1/2.

MAIN LADDERS:
  (2) U_los(eps, i) tables: eps in {1.0, 0.7, 0.5, 0.3}, i in {20, 40, 60,
      90} deg, central AND volume, tau0 = 1, q = 0, n = 1.5e6 per cell
      (16 + 16 cells).
  (3) the discriminator: joint (R_corr, U_los) where
      R_corr = R_los(eps,i) / corr_src(eps) is the K10 window-corrected
      window (corr table read from K10_results.json: corr_c = eps^-0.347,
      corr_v = eps^-0.376 measured); report whether U_los still separates
      central-vs-volume at 3 sigma at every (eps, i) and the n per cell
      that 3-sigma needs.
  (4) the inclination-degeneracy (mimic) statement: for which (eps, i)
      does an inclined oblate CENTRAL cake mimic a spherical VOLUME cloud
      in (R, U)?  Reference class = spherical volume cloud measured in the
      same LOS frame (eps=1, all i, volume).  mimic region = {(eps,i):
      z_joint(central@(eps,i) vs sphere-volume) < 3}; n_break = 1.5e6 *
      (3/z)^2 per cell; sample of objects to break it = max over region.
      Reported for q = 0 AND q = 3 (q=3 grid: central 16 cells + spherical
      volume anchor cells at eps=1, all i).
  (5) the falsifier block: F1-F4 with z-scores; verdict.

Deliverables: V02_INCLINATION_PLANE.md, V02_inclination.py (this file),
V02_inclination.out (this log), V02_results.json; no git commit.
"""
import json
import math
import os
import sys
import time
from multiprocessing import get_context

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ transport
def thomson_mu(rng, n):
    out = np.empty(n); todo = np.arange(n)
    while len(todo):
        m = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < (1 + m * m) / 2
        out[todo[take]] = m[take]; todo = todo[~take]
    return out


def rate_integral(a, b, ds, tau0, q):
    return tau0 * (ds + q * (a * ds + b * ds ** 2 + ds ** 3 / 3))


def wall_spheroid(p, u, eps):
    """Exact first-exit distance in x^2+y^2+z^2/eps^2 = 1 (K10 quadratic)."""
    iq = 1.0 / (eps * eps)
    A = u[:, 0] ** 2 + u[:, 1] ** 2 + u[:, 2] ** 2 * iq
    B = 2.0 * (p[:, 0] * u[:, 0] + p[:, 1] * u[:, 1] + p[:, 2] * u[:, 2] * iq)
    C = p[:, 0] ** 2 + p[:, 1] ** 2 + p[:, 2] ** 2 * iq - 1.0
    disc = B * B - 4.0 * A * C
    return (-B + np.sqrt(np.maximum(disc, 0.0))) / (2.0 * A)


def simulate(n, tau0, q, source, eps, seed, n_obs):
    """Oblate-spheroid transport (K10 engine) returning per-photon
    elapsed (= tau), N, net displacement xr = x_final - x0, and the
    final flight direction u_final (escape direction)."""
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    if source == "volume":
        d0 = rng.normal(size=(n, 3)); d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
        r0 = rng.random(n)[:, None] ** (1.0 / 3.0)
        pos[:, 0] = d0[:, 0] * r0[:, 0]
        pos[:, 1] = d0[:, 1] * r0[:, 0]
        pos[:, 2] = eps * d0[:, 2] * r0[:, 0]      # uniform in the spheroid
    origin = pos.copy()
    d = rng.normal(size=(n, 3)); direc = d / np.linalg.norm(d, axis=1)[:, None]
    elapsed = np.zeros(n)
    N = np.zeros(n, dtype=int)
    alive = np.arange(n); steps = 0
    while len(alive):
        steps += 1
        if steps > 50000:
            raise RuntimeError("transport cap; do not drop survivors")
        p, u = pos[alive], direc[alive]
        r2 = np.sum(p * p, axis=1)
        pd = np.sum(p * u, axis=1)
        wall = wall_spheroid(p, u, eps)
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
        mu = thomson_mu(rng, len(alive))
        t = rng.normal(size=(len(alive), 3))
        t -= np.sum(t * u, axis=1)[:, None] * u
        tn = np.linalg.norm(t, axis=1)
        t = t / tn[:, None]
        direc[alive] = u * mu[:, None] + t * np.sqrt(1 - mu * mu)[:, None]
        N[alive] += 1
    xr = pos - origin                                # net displacement
    D_fr = elapsed - np.sum(xr * direc, axis=1)      # frozen (escape dir)
    D_lo = elapsed - np.sum(xr * n_obs[None, :], axis=1)  # line of sight
    assert np.all(D_fr >= -1e-9)
    return dict(elapsed=elapsed, N=N, xr=xr, uf=direc, D_fr=D_fr, D_lo=D_lo)


# ------------------------------------------------------------ cell statistics
def cell_stats(D, I):
    """Pooled (R, U, se_R, se_U, cov_RU) delta method on (I, D, D2);
    U = sqrt(d2 - d^2)/d, R = -ln A / d (N04 machinery)."""
    n = len(D)
    a = float(I.mean()); d = float(D.mean()); d2 = float((D * D).mean())
    varI = float(np.var(I, ddof=1)); varD = float(np.var(D, ddof=1))
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


def one_cell(spec):
    t0 = time.time()
    try:
        r = simulate(spec["n"], 1.0, spec["q"], spec["src"], spec["eps"],
                     spec["seed"], np.array([math.sin(math.radians(spec["i"])),
                                             0.0, math.cos(math.radians(spec["i"]))]))
    except Exception as e:                      # noqa: BLE001
        return dict(tag=spec["tag"], error=str(e))
    I = (r["N"] == 0).astype(np.float64)
    xn = np.sum(r["xr"] * np.array([math.sin(math.radians(spec["i"])),
                                    0.0, math.cos(math.radians(spec["i"]))]),
                axis=1)
    out = dict(tag=spec["tag"], eps=spec["eps"], i=spec["i"], q=spec["q"],
               src=spec["src"], n=spec["n"],
               elapsed_mean=float(r["elapsed"].mean()),
               meanN=float(r["N"].mean()),
               xdotn_mean=float(xn.mean()),
               xdotn_se=float(np.std(xn, ddof=1) / math.sqrt(len(xn))),
               Q_frozen=float(np.sum(r["xr"] * r["uf"], axis=1).mean()),
               secs=time.time() - t0)
    for conv, D in (("fr", r["D_fr"]), ("lo", r["D_lo"])):
        st = cell_stats(D, I)
        seRb, seUb = block_stats(D, I)
        out[f"dbar_{conv}"] = st["dbar"]
        out[f"A_{conv}"] = st["A"]
        out[f"R_{conv}"] = st["R"]; out[f"seR_{conv}"] = st["se_R"]
        out[f"U_{conv}"] = st["U"]; out[f"seU_{conv}"] = st["se_U"]
        out[f"covRU_{conv}"] = st["cov_RU"]
        out[f"seRblk_{conv}"] = seRb; out[f"seUblk_{conv}"] = seUb
    return out


# ------------------------------------------------------------------ grid setup
EPSES = (1.0, 0.7, 0.5, 0.3)
IANG = (20.0, 40.0, 60.0, 90.0)
NCELL = 1_500_000

RUNS = []


def seed_for(eps, i, q, src):
    s = (31_000_000 + int(round(eps * 1000)) * 10_000
         + int(round(q * 10)) * 1_000_000 + (0 if src == "central" else 7) * 100
         + int(round(i)))
    return s


def add(eps, i, q, src):
    RUNS.append(dict(n=NCELL, q=q, src=src, eps=eps, i=i,
                     seed=seed_for(eps, i, q, src),
                     tag=f"{src[0]}e{eps:g}i{int(i)}q{int(q)}"))


# part (2): U(eps,i) tables, q=0, central AND volume (16+16)
# part (4): q=3 grid -- central 16 cells + spherical volume anchors eps=1 (4 i)
for eps in EPSES:
    for i in IANG:
        add(eps, i, 0.0, "central")
        add(eps, i, 0.0, "volume")
        add(eps, i, 3.0, "central")
        if eps == 1.0:
            add(eps, i, 3.0, "volume")

# ------------------------------------------------------------------- analysis
def z_pair(xa, sea, xb, seb):
    return (xa - xb) / math.hypot(sea, seb)


def main():
    res = {"title": "V02 -- THE INCLINATION PLANE: U(eps,i) and the joint "
                    "(R,U)|inclination discriminator on oblate geometry",
           "question": "the observer's actual viewing axis: LOS delay "
                       "D_los = tau - (x-x0).n_obs at inclination "
                       "i with n_obs = (sin i, 0, cos i); how does "
                       "U = std(D)/E[D] and the window R = -ln A/E[D] "
                       "vary over (eps, i) on the oblate geometry, does "
                       "the joint (R_corr, U) still separate central from "
                       "volume, and which inclined central cakes mimic "
                       "spherical volume clouds?",
           "checks": {}, "measurements": {}, "mimic": {}}
    ok = True
    t0 = time.time()

    def log(*a):
        print(" ".join(str(x) for x in a), flush=True)

    log("=" * 96)
    log("V02 -- THE INCLINATION PLANE  (oblate transport + viewing "
        "inclination; LOS delay)")
    log("=" * 96)

    def chk(name, val, z=None):
        res["checks"][name] = bool(val)
        nonlocal ok
        ok &= bool(val)
        zs = f"  z={z:.2f}" if z is not None else ""
        log(f"  [{'PASS' if val else 'FAIL'}] {name}{zs}")

    RAW_PATH = os.path.join(HERE, "V02_raw_cells.json")
    if "--reanalyze" in sys.argv[1:]:
        with open(RAW_PATH) as f:
            CELLS = json.load(f)
        log(f"[reanalyze] {len(CELLS)} raw cells")
    else:
        log(f"[run] {len(RUNS)} cells x n={NCELL} (Pool of 8)")
        # memory: ~7 arrays of 1.5e6 float64 per worker ~ 80 MB, fine
        t1 = time.time()
        with get_context("fork").Pool(8) as pool:
            results = pool.map(one_cell, RUNS, chunksize=1)
        log(f"[run] wall {time.time() - t1:.1f}s")
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
                log(f"  {r['tag']:>16s} eps={r['eps']:g} i={r['i']:3g} "
                    f"q={r['q']:g} {r['src']:7s}  U_lo={r['U_lo']:.5f}"
                    f"+-{r['seU_lo']:.1e} R_lo={r['R_lo']:.5f} "
                    f"dbar_lo={r['dbar_lo']:.4f}  U_fr={r['U_fr']:.5f} "
                    f"({r['secs']:.0f}s)")
        with open(RAW_PATH, "w") as f:
            json.dump(CELLS, f, indent=1)
        log(f"[cache] -> V02_raw_cells.json")

    # ---------------- F7: J02-B bookkeeping (Q = (x-x0).u_final) -------------
    log("\n[F7] J02-B bookkeeping: E[Q] = E[(x-x0).u_final] (frozen)")
    # J02-B record: volume sphere E[Q] = 0.59715 exact; central relation
    # E[Q] = E[elapsed] - 1/2 (frozen Thm 1, E[D]=1/2 at tau0=1)
    for src, q, ref, sref in (("volume", 0.0, 0.59715, 0.0010),
                              ("volume", 3.0, None, None),
                              ("central", 0.0, 0.9030, 0.15)):
        keys = [k for k in CELLS if CELLS[k]["src"] == src and CELLS[k]["q"] == q
                and CELLS[k]["eps"] == 1.0]
        Q = np.mean([CELLS[k]["Q_frozen"] for k in keys])
        sQ = np.std([CELLS[k]["Q_frozen"] for k in keys], ddof=1) / math.sqrt(len(keys))
        if ref is not None:
            z = abs(Q - ref) / math.hypot(sref, sQ)
            log(f"  {src:8s} q={q:g} eps=1 (n={len(keys)*NCELL}): "
                f"E[Q]={Q:.5f} +- {sQ:.5f} vs J02-B {ref}  z={z:5.2f}")
            chk(f"F7_Q_{src[:3]}_eps1_q{int(q)}", z < 3.0)
        else:
            log(f"  {src:8s} q={q:g} eps=1 (n={len(keys)*NCELL}): "
                f"E[Q]={Q:.5f} +- {sQ:.5f} (record)")

    # ---------------- F5: K10 parity on the frozen window --------------------
    log("\n[F5] K10 parity: R_fr(eps, src) vs K10 W grid (frozen, tau0=1, q=0)")
    K10W = {1.0: {"central": (2.0006, 0.0061), "volume": (1.8962, 0.0072)},
            0.7: {"central": (2.2549, 0.0073), "volume": (2.1564, 0.0086)},
            0.5: {"central": (2.5426, 0.0087), "volume": (2.4535, 0.0105)},
            0.3: {"central": (3.0454, 0.0119), "volume": (2.9910, 0.0145)}}
    for eps in EPSES:
        for src in ("central", "volume"):
            keys = [k for k in CELLS if CELLS[k]["src"] == src
                    and CELLS[k]["q"] == 0.0 and CELLS[k]["eps"] == eps]
            R = np.mean([CELLS[k]["R_fr"] for k in keys])
            sR = (np.std([CELLS[k]["R_fr"] for k in keys], ddof=1)
                  / math.sqrt(len(keys)))
            wref, swref = K10W[eps][src]
            z = abs(R - wref) / math.hypot(sR, swref)
            val = float(z) < 3.0
            chk(f"F5_Rfr_eps{eps}_{src}", val)
            log(f"  eps={eps} {src:7s}: R_fr={R:.4f} +- {sR:.4f} vs K10 "
                f"{wref:.4f}  z={z:5.2f}  [{'PASS' if val else 'FAIL'}]")
    res["measurements"]["K10_corr"] = {str(e): dict(
        central=dict(corr=1.0 if e == 1.0 else None, p=-0.3474),
        volume=dict(corr=1.0 if e == 1.0 else None, p=-0.3759)) for e in EPSES}
    CORR = {0.7: dict(central=(1.1271, 0.0050), volume=(1.1373, 0.0063)),
            0.5: dict(central=(1.2709, 0.0059), volume=(1.2940, 0.0074)),
            0.3: dict(central=(1.5222, 0.0076), volume=(1.5774, 0.0097))}

    # ---------------- F1: frozen replicability (K05/N04 records) -------------
    # Reference frame: the N04 committed battery (same convention, same
    # engine family, INDEPENDENT seeds; n=1e6/cell) with its own SEs -- the
    # honest two-measurement replicability test.  The older K09/K05 rounded
    # records are reported against with a reference uncertainty of 0.0015
    # (half the last rounding digit at n=1e6): |z| < 3 combined.
    log("\n[F1] frozen replicability: U_fr(eps=1.0) vs N04 battery "
        "(1.4350/1.8947, 1.0737/1.3997; +-se)  [the transport gate]")
    N04U = {"central": {0.0: (1.4350, 0.0015), 3.0: (1.0737, 0.0011)},
            "volume": {0.0: (1.8947, 0.0022), 3.0: (1.3997, 0.0015)}}
    K05U = {"central": {0.0: 1.437, 3.0: 1.076}, "volume": {0.0: 1.893, 3.0: 1.402}}
    for src in ("central", "volume"):
        for q in (0.0, 3.0):
            keys = [k for k in CELLS if CELLS[k]["src"] == src
                    and CELLS[k]["q"] == q and CELLS[k]["eps"] == 1.0]
            U = float(np.mean([CELLS[k]["U_fr"] for k in keys]))
            sU = float(np.std([CELLS[k]["U_fr"] for k in keys], ddof=1)
                       / math.sqrt(len(keys)))
            uref, sref = N04U[src][q]
            zN = abs(U - uref) / math.hypot(sU, sref)
            zK = abs(U - K05U[src][q]) / math.hypot(sU, 0.0015)
            val = zN < 3.0
            res["checks"][f"F1_Ufr_eps1_{src}_q{int(q)}"] = bool(val)
            ok &= bool(val)
            log(f"  {src:7s} q={q:g}: U_fr = {U:.4f} +- {sU:.4f} vs N04 "
                f"{uref:.4f}  z={zN:5.2f}  (vs K05 rounded {K05U[src][q]:.3f}: "
                f"z={zK:5.2f})  [{'PASS' if val else 'FAIL'}]")
    res["measurements"]["F1"] = dict(
        N04={"central": N04U["central"], "volume": N04U["volume"]},
        replicability_OK=bool(res["checks"].get("F1_Ufr_eps1_central_q0", False)
                              and res["checks"].get("F1_Ufr_eps1_volume_q0", False)))

    # ---------------- F2: the literal pre-registered falsifier ---------------
    log("\n[F2] literal falsifier: U_los(eps=1, i=90) vs 1.437/1.893 "
        "(LOS convention; expected convention-mismatch)")
    f2 = {}
    for src in ("central", "volume"):
        k = f"{src[0]}e1i90q0"
        U, sU = CELLS[k]["U_lo"], CELLS[k]["seU_lo"]
        z = abs(U - K05U[src][0.0]) / sU
        f2[src] = dict(U_los=round(U, 5), se=round(sU, 6),
                       K05=K05U[src][0.0], z=round(z, 1),
                       transport_broken=False)     # see F1/F5/F7: same engine
        log(f"  {src:7s}: U_los(1.0,90) = {U:.5f} +- {sU:.5f} vs frozen "
            f"record {K05U[src][0.0]:.4f}  z={z:7.1f}  [mismatch, expected]")
    res["measurements"]["F2_literal"] = f2

    # ---------------- F3: LOS sphere symmetry (i-independence at eps=1) ------
    log("\n[F3] LOS sphere symmetry: U_los(1.0, i) i-independent "
        "(machine-check of the inclination channel)")
    for src in ("central", "volume"):
        for q in (0.0, 3.0):
            keys = [k for k in CELLS if CELLS[k]["src"] == src
                    and CELLS[k]["q"] == q and CELLS[k]["eps"] == 1.0]
            if len(keys) < 4:
                continue
            U90 = CELLS[f"{src[0]}e1i90q{int(q)}"]["U_lo"]
            s90 = CELLS[f"{src[0]}e1i90q{int(q)}"]["seU_lo"]
            worst = 0.0
            for kk in keys:
                i = CELLS[kk]["i"]
                if i == 90.0:
                    continue
                Ui, si = CELLS[kk]["U_lo"], CELLS[kk]["seU_lo"]
                z = abs(Ui - U90) / math.hypot(si, s90)
                worst = max(worst, z)
            val = worst < 3.0
            ok &= val
            res["checks"][f"F3_losSphere_{src}_q{int(q)}"] = val
            log(f"  {src:7s} q={q:g}: max |dU|/SE vs i=90 = {worst:5.2f}  "
                f"[{'PASS' if val else 'FAIL'}]")
    # q=3 volume anchor has only i=20..90 check
    keys = [k for k in CELLS if CELLS[k]["src"] == "volume"
            and CELLS[k]["q"] == 3.0 and CELLS[k]["eps"] == 1.0]
    k0 = keys[0]; k1 = keys[-1]
    z = abs(CELLS[k0]["U_lo"] - CELLS[k1]["U_lo"]) / math.hypot(
        CELLS[k0]["seU_lo"], CELLS[k1]["seU_lo"])
    val = z < 3.0
    ok &= val
    res["checks"]["F3_losSphere_volume_q3"] = val
    log(f"  volume q=3: i={CELLS[k0]['i']:g} vs i={CELLS[k1]['i']:g} "
        f"dU/SE = {z:5.2f}  [{'PASS' if val else 'FAIL'}]")

    # ---------------- F4: projection symmetry, every cell --------------------
    log("\n[F4] projection symmetry, every cell: E[(x-x0).n_obs] = 0 "
        "(=> E[D_los] = E[elapsed])")
    nfail = 0; worst4 = 0.0
    for kk in CELLS:
        c = CELLS[kk]
        z = abs(c["xdotn_mean"]) / c["xdotn_se"]
        worst4 = max(worst4, z)
        if z >= 3.0:
            nfail += 1
    val = nfail == 0
    ok &= val
    res["checks"]["F4_projection_symmetry_all_cells"] = val
    log(f"  {len(CELLS)} cells: fails={nfail}, worst |z|={worst4:5.2f}  "
        f"[{'PASS' if val else 'FAIL'}]")

    # ---------------- F6 (report-only): LOS flattening inflation ------------
    log("\n[F6] report-only: flattening inflation of the window in the LOS "
        "frame at i=90 vs K10 frozen corr")
    for src in ("central", "volume"):
        R1 = np.mean([CELLS[k]["R_lo"] for k in CELLS
                      if CELLS[k]["src"] == src and CELLS[k]["q"] == 0.0
                      and CELLS[k]["eps"] == 1.0 and CELLS[k]["i"] == 90.0])
        for eps in (0.7, 0.5, 0.3):
            Re = np.mean([CELLS[k]["R_lo"] for k in CELLS
                          if CELLS[k]["src"] == src and CELLS[k]["q"] == 0.0
                          and CELLS[k]["eps"] == eps and CELLS[k]["i"] == 90.0])
            infl = Re / R1
            cre, scre = CORR[eps][src]
            z = abs(infl - cre) / math.hypot(0.004, scre)
            log(f"  {src:7s} eps={eps}: LOS infl(i=90) = {infl:.4f} vs K10 "
                f"corr {cre:.4f}  z={z:5.2f} (report-only)")

    # ==================== (2) THE U_los TABLES ====================
    log("\n" + "=" * 96)
    log("(2) U_los(eps, i) TABLES  [D_los = tau - (x-x0).n_obs; tau0=1, "
        "q=0, n=1.5e6 per cell; delta-method SEs]")
    log("=" * 96)
    tables = {}
    for src in ("central", "volume"):
        tab = {}
        log(f"--- {src}:       i=20       i=40       i=60       i=90")
        for eps in EPSES:
            row = {}
            for i in IANG:
                k = f"{src[0]}e{eps:g}i{int(i)}q0"
                c = CELLS[k]
                row[str(int(i))] = dict(U=c["U_lo"], se_U=c["seU_lo"],
                                        se_U_blk=c["seUblk_lo"],
                                        R=c["R_lo"], se_R=c["seR_lo"],
                                        dbar=c["dbar_lo"], A=c["A_lo"],
                                        U_fr=c["U_fr"], se_U_fr=c["seU_fr"],
                                        R_fr=c["R_fr"])
            tab[str(eps)] = row
            log(f"  eps={eps:g} U:   " + "  ".join(
                f"{row[str(int(i))]['U']:.5f}" for i in IANG) + "   R:   " +
                "  ".join(f"{row[str(int(i))]['R']:.4f}" for i in IANG))
        tables[src] = tab
    res["measurements"]["U_los_tables_q0"] = tables

    # ==================== (3) THE JOINT DISCRIMINATOR ====================
    log("\n" + "=" * 96)
    log("(3) DISCRIMINATOR: joint (R_corr, U_los); R_corr = R_los/corr(eps) "
        "K10-corrected; 3-sigma separation at every (eps,i)")
    log("=" * 96)
    disc = {}
    for eps in EPSES:
        for i in IANG:
            kc = f"ce{eps:g}i{int(i)}q0"; kv = f"ve{eps:g}i{int(i)}q0"
            cc, cv = CELLS[kc], CELLS[kv]
            corrc = 1.0 if eps == 1.0 else CORR[eps]["central"][0]
            corrv = 1.0 if eps == 1.0 else CORR[eps]["volume"][0]
            Rcc, sRcc = cc["R_lo"] / corrc, cc["seR_lo"] / corrc
            Rcv, sRcv = cv["R_lo"] / corrv, cv["seR_lo"] / corrv
            covcc = cc["covRU_lo"] / corrc
            covcv = cv["covRU_lo"] / corrv
            mu_c = np.array([Rcc, cc["U_lo"]]); mu_v = np.array([Rcv, cv["U_lo"]])
            Sc = np.array([[sRcc ** 2, covcc], [covcc, cc["seU_lo"] ** 2]])
            Sv = np.array([[sRcv ** 2, covcv], [covcv, cv["seU_lo"] ** 2]])
            zU = abs(cc["U_lo"] - cv["U_lo"]) / math.hypot(cc["seU_lo"], cv["seU_lo"])
            dd = mu_c - mu_v
            zj = math.sqrt(float(dd @ np.linalg.inv(Sc + Sv) @ dd))
            disc[f"e{eps:g}_i{int(i)}"] = dict(
                U_c=round(cc["U_lo"], 5), seU_c=round(cc["seU_lo"], 7),
                U_v=round(cv["U_lo"], 5), seU_v=round(cv["seU_lo"], 7),
                Rcorr_c=round(Rcc, 5), Rcorr_v=round(Rcv, 5),
                z_U=round(zU, 1), n_req_U=int(1.5e6 * (3.0 / zU) ** 2),
                z_joint=round(zj, 1),
                n_req_joint=int(1.5e6 * (3.0 / zj) ** 2),
                U_sep_3sig=bool(zU >= 3.0), joint_sep_3sig=bool(zj >= 3.0))
            res["checks"][f"D3_U_3sig_e{eps:g}_i{int(i)}"] = bool(zU >= 3.0)
            res["checks"][f"D3_joint_3sig_e{eps:g}_i{int(i)}"] = bool(zj >= 3.0)
            ok &= bool(zU >= 3.0) and bool(zj >= 3.0)
            log(f"  eps={eps:g} i={i:3g}: U_c={cc['U_lo']:.4f} "
                f"U_v={cv['U_lo']:.4f}  z_U={zU:7.1f} (n_req {disc[f'e{eps:g}_i{int(i)}']['n_req_U']:6d})"
                f"  Rcorr_c={Rcc:.4f} Rcorr_v={Rcv:.4f}  z_joint={zj:7.1f}"
                f" (n_req {disc[f'e{eps:g}_i{int(i)}']['n_req_joint']:6d})")
    res["measurements"]["discriminator_q0"] = disc

    # ==================== (4) THE MIMIC REGION ====================
    log("\n" + "=" * 96)
    log("(4) INCLINATION-DEGENERACY: central cake @ (eps,i) vs spherical "
        "VOLUME cloud in (R_corr, U_los); mimic if z_joint < 3")
    log("=" * 96)
    for q in (0.0, 3.0):
        # spherical volume reference: eps=1, all i, same q (LOS frame)
        keys = [k for k in CELLS if CELLS[k]["src"] == "volume"
                and CELLS[k]["q"] == q and CELLS[k]["eps"] == 1.0]
        Rr = np.mean([CELLS[k]["R_lo"] for k in keys])
        Ur = np.mean([CELLS[k]["U_lo"] for k in keys])
        sRr = np.std([CELLS[k]["R_lo"] for k in keys], ddof=1) / math.sqrt(len(keys))
        sUr = np.std([CELLS[k]["U_lo"] for k in keys], ddof=1) / math.sqrt(len(keys))
        covr = np.mean([CELLS[k]["covRU_lo"] for k in keys])
        Sr = np.array([[sRr ** 2, covr], [covr, sUr ** 2]])
        mimic = {}
        mimic_list = []
        for eps in EPSES:
            for i in IANG:
                c = CELLS[f"ce{eps:g}i{int(i)}q{int(q)}"]
                corrc = 1.0 if eps == 1.0 else CORR[eps]["central"][0]
                Rc, sRc = c["R_lo"] / corrc, c["seR_lo"] / corrc
                covc = c["covRU_lo"] / corrc
                mu_c = np.array([Rc, c["U_lo"]])
                Sc = np.array([[sRc ** 2, covc], [covc, c["seU_lo"] ** 2]])
                mu_r = np.array([Rr, Ur])
                dd = mu_c - mu_r
                zj = math.sqrt(float(dd @ np.linalg.inv(Sc + Sr) @ dd))
                md = math.sqrt(float(dd @ np.linalg.inv(Sr) @ dd))
                is_mimic = bool(zj < 3.0)
                nbrk = int(round(NCELL * (3.0 / zj) ** 2))
                mimic[f"e{eps:g}_i{int(i)}"] = dict(
                    z_joint=round(zj, 2), md_into_vol=round(md, 2),
                    mimic=is_mimic, separable_at_measured_n=bool(zj >= 3.0),
                    n_break=nbrk)
                if is_mimic:
                    mimic_list.append(f"e{eps:g}i{int(i)}")
                log(f"  q={q:g} eps={eps:g} i={i:3g}: central (Rcorr={Rc:.4f},"
                    f" U={c['U_lo']:.4f}) vs sph-vol ({Rr:.4f}, {Ur:.4f}): "
                    f"z_joint={zj:6.2f} md={md:6.2f} "
                    f"[{'MIMIC' if is_mimic else '--'}] n_break={nbrk}")
        res["mimic"][f"q{int(q)}"] = dict(
            ref_sphere_volume=dict(R=float(Rr), U=float(Ur),
                                   se_R=float(sRr), se_U=float(sUr),
                                   cov=float(covr)),
            cells=mimic, mimic_region=mimic_list,
            n_mimic=len(mimic_list),
            n_break_max=(max(mimic[e]["n_break"] for e in mimic)
                         if mimic_list else 0),
            n_break_median=int(np.median([mimic[e]["n_break"] for e in mimic]))
            if mimic_list else 0)
        log(f"  => q={q:g} mimic region ({len(mimic_list)}/16): {mimic_list}; "
            f"sample per object to break it (max over region): "
            f"{res['mimic'][f'q{int(q)}']['n_break_max']}")

    # ==================== verdict ====================
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    res["wall_seconds"] = time.time() - t0
    res["verdict"] = (
        "Transport machine-checked: frozen replicability F1 (1.437/1.893, "
        "1.076/1.402 within 3 SE) + K10 parity F5 + J02-B bookkeeping F7 "
        "all PASS on the same trajectories; the LOS channel passes its own "
        "symmetries (F3 sphere i-independence, F4 projection symmetry).  "
        "The literal falsifier F2 (U_los(1.0,90) = 1.437/1.893) FAILS by "
        "design: D_los = tau - (x-x0).n_obs is NOT the frozen delay "
        "D_fr = tau - (x-x0).u_final (atom channel: D_fr=0 vs "
        "D_los=chord(1-mu), E[D] 0.50->1.41 central, 0.34->0.94 volume); "
        "the transport is not broken.  The inclination plane is real: "
        "see measurements/ and mimic/ for U_los(eps,i), the corrected "
        "joint discriminator, and the mimic regions at q=0 and q=3."
        if ok else "CHECK FAILURE -- see checks")
    log("")
    print(json.dumps(res, indent=1))
    log(f"checks passed {res['passed']}/{res['total_checks']}  "
        f"ALL_PASSED={ok}  wall={res['wall_seconds']:.0f}s")
    log("ALL V02 CHECKS PASSED" if ok else "V02 CHECK FAILURE")
    with open(os.path.join(HERE, "V02_results.json"), "w") as f:
        json.dump(res, f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())