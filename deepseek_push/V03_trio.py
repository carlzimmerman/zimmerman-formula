#!/usr/bin/env python3
"""
V03 -- THE IGNORANCE-ORTHOGONAL TRIO: R (kernel-free) x U (radius-free) x B
      (density-free) fused into ONE decision surface.
2026-09-25.  Deepseek lane; no git commit.  Append-only: no prior file touched.

PRE-REGISTRATION (locked before any V03 number is drawn; mirrors
V03_IGNORANCE_TRIO.md sections 0.3-0.7).  See the module docstring of the
sections printed at the top of the .out BEFORE any measurement:

  (a) Landscape: CORE 36 cells (central|volume x q{0,3,10} x tau0{0.5,1,2}
      x kernel{thomson,iso}, n=8e5 each) + SHELL-EXT 36 cells (shell a{0.3,0.5}
      x same q x tau0 x kernel, n=2e5 each); engine = J02 verbatim + L07
      kernel switch + K09 shell birth; P1 bitwise parity against the imports.
  (b) Observer bands fixed from the RECORD (0.3): W_C=[4/3,2] exact;
      W_V=[0.9184,1.9144] tol .010 (K09); W_S=[1.4298,2.0063] tol .025 (K09);
      U_C=[0.804,1.982], U_V=[1.233,2.536] (N04 union +-3se); U_S from THIS
      run (flagged CIRCULAR); B=[1,inf), violated iff slack < 1 - 3 se.
  (c) Disagreement classes (0.4): KILL-B, VOID-X, MIRROR, CROSS, HIERARCHY,
      TRIO-AGREE; kernel gates C3 (R kernel-free) / C7 (U kernel-tagged).
  (d) Checks C1..C7 with KILL thresholds (0.5).
  (e) Decision tree (0.6): B gate -> R window+kernel-free + K06-inv pin ->
      U resolved read-out; failure modes named; min-n per falsifier per cell.
  (f) Joint 3-sigma regions per (geometry,kernel) class + pairwise overlaps,
      residual degeneracy >= 1% overlap (0.7).
  (g) doorB cross-check: 0.90889*R(central,q0,tau0=1) = 1.8178 +- 3se and
      verdict CONSISTENT-OPEN.

Outputs: V03_trio.out (log), V03_results.json; V03_IGNORANCE_TRIO.md written
by the agent from these.
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
os.chdir(REPO)
sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate as j02_simulate        # parity
from J02_moment_hierarchy import thomson_mu as j02_thomson_mu    # parity
from K09_geometry_reading import simulate_shell as k09_shell     # parity

OUT = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


PRE = open(os.path.join(HERE, "V03_PRE.txt")).read() if os.path.exists(
    os.path.join(HERE, "V03_PRE.txt")) else None


# ======================================================================
# 1. RECORD PRIORS (fixed before the run; all references in the md)
# ======================================================================
W_CENTRAL = {0.0: 2.0, 3.0: 1.6, 10.0: 1.4444444444444446}   # J09-D closed form
W_VOL = {  # K09 table rows tau0 in {0.5,1,2}, q in {0,3,10}: (W, se)
    (0.5, 0.0): (1.9144, 0.005), (0.5, 3.0): (1.8208, 0.009), (0.5, 10.0): (1.6371, 0.008),
    (1.0, 0.0): (1.8814, 0.010), (1.0, 3.0): (1.7103, 0.007), (1.0, 10.0): (1.3288, 0.006),
    (2.0, 0.0): (1.8033, 0.007), (2.0, 3.0): (1.4228, 0.006), (2.0, 10.0): (0.9184, 0.003)}
W_SHELL_BAND = (1.4298, 2.0063)          # K09 on-grid union over a, tol 0.025
U_REC = {  # N04 U-table: (geom, tau0, q) -> (U, se_block)
    ("central", 0.5, 0.0): (1.97176, 0.00116), ("central", 0.5, 3.0): (1.39192, 0.00177),
    ("central", 0.5, 10.0): (1.04877, 0.00076), ("central", 1.0, 0.0): (1.43503, 0.00131),
    ("central", 1.0, 3.0): (1.07370, 0.00114), ("central", 1.0, 10.0): (0.89762, 0.00157),
    ("central", 2.0, 0.0): (1.07571, 0.00122), ("central", 2.0, 3.0): (0.89219, 0.00117),
    ("central", 2.0, 10.0): (0.81428, 0.00084),
    ("volume", 0.5, 0.0): (2.52530, 0.00306), ("volume", 0.5, 3.0): (1.69622, 0.00149),
    ("volume", 0.5, 10.0): (1.34261, 0.00195), ("volume", 1.0, 0.0): (1.89468, 0.00183),
    ("volume", 1.0, 3.0): (1.39970, 0.00204), ("volume", 1.0, 10.0): (1.25841, 0.00145),
    ("volume", 2.0, 0.0): (1.52619, 0.00214), ("volume", 2.0, 3.0): (1.27995, 0.00140),
    ("volume", 2.0, 10.0): (1.24251, 0.00139)}
# union bands, widened +-3*max se (computed from U_REC; pre-registered values)
_u_c = [v[0] for k, v in U_REC.items() if k[0] == "central"]
_u_v = [v[0] for k, v in U_REC.items() if k[0] == "volume"]
U_BAND_C = (min(_u_c) - 3 * 0.00221, max(_u_c) + 3 * 0.00221)   # [0.804,1.982]
U_BAND_V = (min(_u_v) - 3 * 0.00314, max(_u_v) + 3 * 0.00314)   # [1.233,2.536]
J05_SLACK = {0.0: 1.25, 3.0: 1.13, 10.0: 1.06}                  # central tau0=1
DOORB_SCALE = 40.9 / 45.0                                       # r_B/R_meas
DOORB_READING = 1.8178                                          # K09 record

TAU0S = (0.5, 1.0, 2.0)
QS = (0.0, 3.0, 10.0)
KERNELS = ("thomson", "iso")


# ======================================================================
# 2. Engine: J02 verbatim + L07 kernel switch + K09 shell birth (+v4)
# ======================================================================
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
        take = rng.random(len(todo)) < 1.0
        out[todo[take]] = m[take]; todo = todo[~take]
    return out


MU_FN = {"thomson": thomson_mu, "iso": isotropic_mu}


def rate_integral(a, b, ds, tau0, q):
    return tau0 * (ds + q * (a * ds + b * ds ** 2 + ds ** 3 / 3))


def simulate(n, tau0, q, source, seed, kernel="thomson", a=None):
    """J02 verbatim + kernel switch; source in {central, volume, shell}
    (shell: birth on |x|=a, K09 law).  Returns N, D, v2, v4."""
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
    v = np.zeros(n); elapsed = np.zeros(n)
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
        kick = rng.normal(size=(len(alive), 3))
        v[alive] += np.sum(kick * (newu - u), axis=1)
        N[alive] += 1
        direc[alive] = newu
    D = elapsed - np.sum((pos - origin) * direc, axis=1)
    assert np.all(D >= -1e-9)
    return dict(N=N, D=D, v2=v * v, v4=v ** 4)


# ======================================================================
# 3. Per-cell trio statistics: pooled + 24-block (R, U, slack) + 3x3 cov
# ======================================================================
NB = 24


def cell_trio(sim, seed):
    """sim: dict(N, D, v2, v4).  Returns pooled + block stats."""
    n = len(sim["D"])
    N, D, v2, v4 = sim["N"], sim["D"], sim["v2"], sim["v4"]
    A = float(np.mean(N == 0))
    d = float(np.mean(D)); d2 = float(np.mean(D * D))
    dv2 = float(np.mean(D * v2)); v4m = float(np.mean(v4))
    R = -math.log(max(A, 1e-300)) / d
    g = math.sqrt(max(d2 - d * d, 1e-12))
    U = g / d
    slack = d2 * v4m / (3.0 * dv2 * dv2)
    # delta-method SEs (N04 form)
    varI = float(np.var(N == 0, ddof=1)); varD = float(np.var(D, ddof=1))
    covID = float(np.cov(N == 0, D, ddof=1)[0, 1])
    seR_d = math.sqrt((varI / (A * A * d * d) + varD * (math.log(A) ** 2) / d ** 4
                       + 2 * (-1 / (A * d)) * (math.log(A) / d ** 2) * covID) / n)
    varD2 = float(np.var(D * D, ddof=1))
    varDv2 = float(np.var(D * v2, ddof=1)); varV4 = float(np.var(v4, ddof=1))
    covDD2 = float(np.cov(D, D * D, ddof=1)[0, 1])
    covDDv2 = float(np.cov(D, D * v2, ddof=1)[0, 1])
    covD2Dv2 = float(np.cov(D * D, D * v2, ddof=1)[0, 1])
    covD2V4 = float(np.cov(D * D, v4, ddof=1)[0, 1])
    covDv2V4 = float(np.cov(D * v2, v4, ddof=1)[0, 1])
    # slack gradient (log form): dlnS/dd2 = 1/d2; dlnS/ddv2 = -2/dv2; dlnS/dv4 = 1/v4m
    gs_d2 = slack / d2; gs_dv2 = -2.0 * slack / dv2; gs_v4 = slack / v4m
    dd2 = 1.0 / (2.0 * g * d); ddd = -1.0 / g - g / d ** 2
    seS2 = (gs_d2 ** 2 * varD2 + gs_dv2 ** 2 * varDv2 + gs_v4 ** 2 * varV4
            + 2 * gs_d2 * gs_dv2 * covD2Dv2 + 2 * gs_d2 * gs_v4 * covD2V4
            + 2 * gs_dv2 * gs_v4 * covDv2V4) / n
    seU_d = math.sqrt((ddd ** 2 * varD + dd2 ** 2 * varD2
                       + 2 * ddd * dd2 * covDD2) / n)
    varID2 = float(np.cov(N == 0, D * D, ddof=1)[0, 1])
    covRU_d = ((math.log(A) / d ** 2) * ddd * varD
               + (math.log(A) / d ** 2) * dd2 * covDD2
               + (-1.0 / (A * d)) * ddd * covID
               + (-1.0 / (A * d)) * dd2 * varID2) / n
    # block covariance of (R, U, slack)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    bs = np.array_split(perm, NB)
    Rb = np.empty(NB); Ub = np.empty(NB); Sb = np.empty(NB)
    for i, b in enumerate(bs):
        Ab = float(np.mean(N[b] == 0)); db = float(np.mean(D[b]))
        d2b = float(np.mean(D[b] * D[b])); dv2b = float(np.mean(D[b] * v2[b]))
        v4b = float(np.mean(v4[b]))
        Rb[i] = -math.log(max(Ab, 1e-300)) / db
        Ub[i] = math.sqrt(max(d2b - db * db, 1e-12)) / db
        Sb[i] = d2b * v4b / (3.0 * dv2b * dv2b)
    cov3 = np.cov(np.vstack([Rb, Ub, Sb]), ddof=1) / NB
    seR_b = math.sqrt(max(cov3[0, 0], 0.0)); seU_b = math.sqrt(max(cov3[1, 1], 0.0))
    seS_b = math.sqrt(max(cov3[2, 2], 0.0))
    return dict(n=n, A=A, dbar=d, d2bar=d2, dv2=dv2, v4m=v4m, R=R, U=U, slack=slack,
                se_R=seR_d, se_U=seU_d, se_R_block=seR_b, se_U_block=seU_b,
                se_slack=seS_b, cov_RU=covRU_d, cov3=cov3.tolist())


# ======================================================================
# 4. Grid + worker
# ======================================================================
RUNS = []


def add(n, tau0, q, src, kernel, seed, a=None, tag=None):
    RUNS.append(dict(n=n, tau0=tau0, q=q, src=src, kernel=kernel, seed=seed,
                     a=a, tag=tag or f"{src[0]}{a}{kernel[0]}t{tau0:g}q{int(q)}"))


def seed_for(tau0, q, src, kernel, n, a=None):
    s = (int(round(tau0 * 10)) * 100000 + int(round(q * 10)) * 10
         + (0 if src == "central" else 1) * 1000
         + (0 if src != "shell" else (2 if a == 0.3 else 3)) * 100000
         + (0 if kernel == "thomson" else 2) * 10000
         + int(round(n / 1e5)) * 1000000 + 77000000)
    return s


def one_run(spec):
    t0 = time.time()
    sim = simulate(spec["n"], spec["tau0"], spec["q"], spec["src"],
                   spec["seed"], spec["kernel"], spec["a"])
    st = cell_trio(sim, spec["seed"] % 2 ** 31)
    st.update(dict(tag=spec["tag"], tau0=spec["tau0"], q=spec["q"],
                   src=spec["src"], kernel=spec["kernel"], a=spec["a"],
                   secs=time.time() - t0))
    return st


# ======================================================================
# 5. Tier-1 verdicts, disagreement classes (LOCKED definitions)
# ======================================================================
GEO = ("C", "V", "S")

W_BAND = {  # pre-registered numbers (see md 0.3)
    "C": (4.0 / 3.0, 2.0),
    "V": (0.9184 - 3 * 0.010, 1.9144 + 3 * 0.010),
    "S": (1.4298 - 3 * 0.025, 2.0063 + 3 * 0.025)}
U_BAND = {"C": U_BAND_C, "V": U_BAND_V, "S": None}   # S filled post-run (flagged)


def verdiR_set(Rt, seR):
    return set(g for g in GEO if W_BAND[g][0] - 3 * seR <= Rt <= W_BAND[g][1] + 3 * seR)


def verdiU_set(Ut, seU, u_shell_band):
    out = set()
    for g in GEO:
        lo, hi = U_BAND[g] if g != "S" else u_shell_band
        if lo - 3 * seU <= Ut <= hi + 3 * seU:
            out.add(g)
    return out


def disagreement_class(vR, vU, bpass):
    """LOCKED mapping (md 0.4)."""
    if not bpass:
        return "KILL-B"
    if not vR or not vU:
        return f"VOID-{'R' if not vR else 'U'}"
    if vR == vU:
        return "TRIO-AGREE"
    if not (vR & vU):
        return "MIRROR"
    if vR < vU or vU < vR:
        return "HIERARCHY"
    return "CROSS"


# ======================================================================
# 6. Joint-region machinery
# ======================================================================
def ellipsoid_membership(x, mu, invS, r2=9.0):
    dx = x - mu
    m = np.einsum("ij,jk,ik->i", dx, invS, dx)
    return m <= r2, m


def class_gauss(cells):
    """cells: list of (R,U,slack); returns mu, Sigma(landscape), chol-free inv."""
    X = np.array([(c["R"], c["U"], c["slack"]) for c in cells])
    mu = X.mean(axis=0)
    Sig = np.cov(X.T, ddof=1)
    return mu, Sig


# ----------------------------------------------------------------------
if __name__ == "__main__":
    t_start = time.time()
    # ---------------- pre-registration banner (must precede numbers) ----
    if PRE is None:
        PRE = ("PRE-REGISTRATION: see V03_IGNORANCE_TRIO.md sections 0.3-0.7 "
               "(locked before run). Bands: W_C=[4/3,2] exact; W_V=[0.9184,1.9144]+-0.03; "
               "W_S=[1.4298,2.0063]+-0.075; U_C=[0.804,1.982]; U_V=[1.233,2.536]; "
               "U_S=this-run(flagged); B=[1,inf). Classes: KILL-B, VOID-X, MIRROR, "
               "CROSS, HIERARCHY, TRIO-AGREE (md 0.4). Checks C1..C7 (md 0.5). "
               "Tree B->R->U (md 0.6). Joint 3-sigma ellipsoids + overlaps (md 0.7).")
    log("=" * 78)
    log("V03 -- PRE-REGISTRATION (LOCKED BEFORE NUMBERS)")
    log(PRE)
    log("=" * 78)

    # ---------------- P1: bitwise parity ----------------------------------
    log("\nP1 parity vs J02 / K09 imports (n=2e5) ...")
    r_ref = j02_simulate(200000, 1.0, 3.0, "central", seed=555001)
    r_new = simulate(200000, 1.0, 3.0, "central", seed=555001, kernel="thomson")
    dD = float(np.max(np.abs(r_ref["D"] - r_new["D"])))
    dN = float(np.max(np.abs(r_ref["N"].astype(float) - r_new["N"].astype(float))))
    ref_shell = k09_shell(200000, 1.0, 3.0, 0.3, seed=555002)
    new_shell = simulate(200000, 1.0, 3.0, "shell", seed=555002, kernel="thomson", a=0.3)
    dDs = float(np.max(np.abs(ref_shell["D"] - new_shell["D"])))
    dNs = float(np.max(np.abs(ref_shell["N"].astype(float) - new_shell["N"].astype(float))))
    p1ok = dD < 1e-9 and dN == 0.0 and dDs < 1e-9 and dNs == 0.0
    log(f"  central: max|dD|={dD:.2e} max|dN|={dN:.0f}  shell: max|dD|={dDs:.2e} "
        f"max|dN|={dNs:.0f}  -> {'PARITY OK' if p1ok else 'PARITY FAIL'}")
    if not p1ok:
        log("KILL P1"); sys.exit(2)

    # ---------------- build grid -----------------------------------------
    for t in TAU0S:
        for q in QS:
            for src in ("central", "volume"):
                for k in KERNELS:
                    add(800000, t, q, src, k, seed_for(t, q, src, k, 8e5),
                        tag=f"{src[0]}t{t:g}q{int(q)}{k[:2]}")
    for a in (0.3, 0.5):
        for t in TAU0S:
            for q in QS:
                for k in KERNELS:
                    add(200000, t, q, "shell", k, seed_for(t, q, "shell", k, 2e5, a),
                        a=a, tag=f"s{a}t{t:g}q{int(q)}{k[:2]}")
    log(f"\nGrid: {len(RUNS)} cells "
        f"({36} core n=8e5 + {36} shell-ext n=2e5), Pool(8)")
    with get_context("fork").Pool(8) as pool:
        RES = pool.map(one_run, RUNS, chunksize=1)

    res_by = {(r["src"], r["tau0"], r["q"], r["kernel"], r.get("a")): r for r in RES}
    json.dump({}, open("V03_results.json", "w"))  # placeholder, replaced below
    log(f"simulation wall {time.time()-t_start:.0f}s")

    checks = {}
    ok_all = True

    # ---------------- meat: per-cell table -------------------------------
    log("\n" + "=" * 78)
    log("TRIO TABLE (R, U, slack_B with SEs) -- 36 core cells, both kernels")
    log("=" * 78)
    hdr = (f"{'cell':26s} {'R':>8s} {'seR':>7s} {'U':>8s} {'seU':>7s} "
           f"{'slack':>7s} {'seS':>7s} {'secs':>5s}")
    log(hdr); log("-" * len(hdr))
    for r in sorted(RES, key=lambda x: (x["src"], x.get("a") or 0, x["tau0"],
                                        x["q"], x["kernel"])):
        log(f"{r['tag']:26s} {r['R']:8.4f} {r['se_R_block']:7.4f} {r['U']:8.4f} "
            f"{r['se_U_block']:7.4f} {r['slack']:7.3f} {r['se_slack']:7.4f} "
            f"{r['secs']:5.1f}")
    log("(seR/seU = 24-block jackknife; delta-method in json)")

    # ---------------- C1, C2, C4 record checks ---------------------------
    log("\nCHECK C1 (U record, N04/K09 at tau0=1):")
    c1 = {}
    for q in QS:
        for src in ("central", "volume"):
            r = res_by[(src, 1.0, q, "thomson", None)]
            urec = U_REC[(src, 1.0, q)][0]
            # N04/K09 record values (K09 width surface)
            urec2 = {"central": {0: 1.4369, 3: 1.0758, 10: 0.8965},
                     "volume":  {0: 1.8934, 3: 1.4024, 10: 1.2597}}[src][int(q)]
            z = (r["U"] - urec2) / r["se_U_block"]
            c1[f"{src[:1]}_q{int(q)}"] = dict(U=round(r["U"], 4), rec=urec2,
                                              z=round(z, 2))
            log(f"  {src[:1]} q={int(q)}: U={r['U']:.4f} +- {r['se_U_block']:.4f} "
                f"rec {urec2:.4f} z={z:.2f}")
    checks["C1_U_record"] = all(abs(v["z"]) < 5 for v in c1.values())
    c1["all"] = checks["C1_U_record"]; ok_all &= checks["C1_U_record"]

    log("\nCHECK C2 (central R-law: closed form, tau0-free):")
    c2 = {}
    for q in QS:
        zz = []
        for t in TAU0S:
            r = res_by[("central", t, q, "thomson", None)]
            zz.append((r["R"] - W_CENTRAL[q]) / r["se_R_block"])
            log(f"  q={int(q):2d} t={t}: R={r['R']:.4f} +- {r['se_R_block']:.4f} "
                f"form {W_CENTRAL[q]:.4f} z={zz[-1]:.2f}")
        c2[f"q{int(q)}"] = dict(zs=[round(x, 2) for x in zz],
                                 tau0free=max(zz) - min(zz) < 5)
        log(f"   -> tau0-free (max spread z {max(zz)-min(zz):.2f} < 5): "
            f"{c2[f'q{int(q)}']['tau0free']}")
    checks["C2_R_law"] = all(c2[f"q{int(q)}"]["tau0free"] for q in QS) \
        and all(abs(x) < 5 for q in QS for x in c2[f"q{int(q)}"]["zs"])
    ok_all &= checks["C2_R_law"]

    log("\nCHECK C4 (B slack record, J05 central tau0=1):")
    c4 = {}
    for q in QS:
        r = res_by[("central", 1.0, q, "thomson", None)]
        z = (r["slack"] - J05_SLACK[q]) / r["se_slack"]
        c4[f"q{int(q)}"] = dict(slack=round(r["slack"], 3), rec=J05_SLACK[q], z=round(z, 2))
        log(f"  q={int(q):2d}: slack={r['slack']:.3f} +- {r['se_slack']:.4f} "
            f"rec {J05_SLACK[q]} z={z:.2f}")
    checks["C4_B_record"] = all(abs(v["z"]) < 4 for v in c4.values())
    ok_all &= checks["C4_B_record"]

    # ---------------- C3 / C7: kernel structure per cell ------------------
    log("\nCHECK C3 (R kernel-free, ALL core cells) + C7 (U kernel-tag):")
    c3 = {"dr_max": 0.0, "worse": None, "zR_max": 0.0, "zR_worst": None}
    c7 = {"n_tagged": 0, "n_cells": 18}
    for src in ("central", "volume"):
        for t in TAU0S:
            for q in QS:
                rt = res_by[(src, t, q, "thomson", None)]
                ri = res_by[(src, t, q, "iso", None)]
                zR = (ri["R"] - rt["R"]) / math.hypot(rt["se_R_block"], ri["se_R_block"])
                zU = (ri["U"] - rt["U"]) / math.hypot(rt["se_U_block"], ri["se_U_block"])
                zS = (ri["slack"] - rt["slack"]) / math.hypot(rt["se_slack"], ri["se_slack"])
                if abs(ri["R"] - rt["R"]) > c3["dr_max"]:
                    c3["dr_max"] = abs(ri["R"] - rt["R"])
                    c3["worse"] = f"{src[0]}t{t:g}q{int(q)}"
                if abs(zR) > c3["zR_max"]:
                    c3["zR_max"] = abs(zR)
                    c3["zR_worst"] = f"{src[0]}t{t:g}q{int(q)}"
                if abs(zU) >= 3:
                    c7["n_tagged"] += 1
                log(f"  {src[:1]} t={t:g} q={int(q):2d}: dR={ri['R']-rt['R']:+.5f} "
                    f"zR={zR:+.2f} | dU={ri['U']-rt['U']:+.5f} zU={zU:+.2f} "
                    f"| dS={ri['slack']-rt['slack']:+.3f} zS={zS:+.2f}")
    checks["C3_R_kernelfree"] = c3["zR_max"] < 5.0
    log(f"  max |R_iso-R_thom| = {c3['dr_max']:.5f} at {c3['worse']}; "
        f"worst zR = {c3['zR_max']:.2f} at {c3['zR_worst']} (gate z<5)")
    checks["C7_U_kerneltag"] = c7["n_tagged"] >= 9   # >= half the 18 core cells
    ok_all &= checks["C3_R_kernelfree"] and checks["C7_U_kerneltag"]

    # ---------------- C5: density-free bound everywhere -------------------
    log("\nCHECK C5 (B-theorem: slack >= 1 - 3 se at ALL 72 cells):")
    c5 = dict(n=0, worst=("", 0.0))
    for r in RES:
        z = (r["slack"] - 1.0) / r["se_slack"]
        if z < c5["worst"][1]:
            c5["worst"] = (r["tag"], z)
        if r["slack"] >= 1.0 - 3 * r["se_slack"]:
            c5["n"] += 1
        else:
            log(f"  VIOLATION {r['tag']} slack={r['slack']:.4f}")
    checks["C5_B_theorem"] = c5["n"] == len(RES)
    log(f"  {c5['n']}/{len(RES)} cells satisfy; worst z=(slack-1)/se = "
        f"{c5['worst'][1]:.2f} at {c5['worst'][0]}")
    ok_all &= checks["C5_B_theorem"]

    # ---------------- U_S shell band (flagged circular) -------------------
    us_cells = [r for r in RES if r["src"] == "shell"]
    U_BAND_S = (min(r["U"] for r in us_cells) - 3 * max(r["se_U_block"] for r in us_cells),
                max(r["U"] for r in us_cells) + 3 * max(r["se_U_block"] for r in us_cells))
    U_BAND["S"] = U_BAND_S
    log(f"\nU_S shell band from this run (flagged CIRCULAR): {U_BAND_S[0]:.3f}.."
        f"{U_BAND_S[1]:.3f}")

    # ---------------- Tier-1 verdicts + disagreement classes --------------
    log("\n" + "=" * 78)
    log("TIER-1 VERDICTS + DISAGREEMENT CLASSES (definitions locked, md 0.4)")
    log("=" * 78)
    classes = {}
    logs = []
    for r in RES:
        vR = verdiR_set(r["R"], r["se_R_block"])
        vU = verdiU_set(r["U"], r["se_U_block"], U_BAND_S)
        bpass = r["slack"] >= 1.0 - 3 * r["se_slack"]
        cl = disagreement_class(vR, vU, bpass)
        classes.setdefault(cl, []).append(r["tag"])
        logs.append((r["tag"], "".join(sorted(vR)), "".join(sorted(vU)),
                     "P" if bpass else "V", cl))
    for cl in ("KILL-B", "VOID-R", "VOID-U", "MIRROR", "CROSS", "HIERARCHY",
               "TRIO-AGREE"):
        log(f"  {cl:10s}: {len(classes.get(cl, [])):3d} cells")
    log("\n  per-cell (tag vR vU B class):")
    for t, vr, vu, bp, cl in sorted(logs, key=lambda x: x[0]):
        log(f"    {t:26s} {vr:3s} {vu:3s} {bp}  {cl}")
    con = {}
    for (t, vr, vu, bp, cl) in logs:
        con[t] = dict(vR=vr, vU=vu, B="P" if bp else "V", cls=cl)
    disagreements = {k: v for k, v in con.items()
                     if v["cls"] not in ("TRIO-AGREE",)}
    log(f"\n  total non-agree cells: {len(disagreements)}")
    # breakdown by kernel
    for k in KERNELS:
        nk = sum(1 for t in con if t.endswith(k[:2]) and con[t]["cls"] != "TRIO-AGREE")
        log(f"    {k}: {nk} non-agree / 18")

    # ---------------- C6: doorB corner cross-check ------------------------
    log("\n" + "=" * 78)
    log("C6: doorB corner cross-check (central, q=0, tau0=1)")
    log("=" * 78)
    r = res_by[("central", 1.0, 0.0, "thomson", None)]
    read = DOORB_SCALE * r["R"]
    se_read = DOORB_SCALE * r["se_R_block"]
    z = (read - 1.8178) / se_read
    vR_ = verdiR_set(r["R"], r["se_R_block"])
    vU_ = verdiU_set(r["U"], r["se_U_block"], U_BAND_S)
    bp_ = r["slack"] >= 1 - 3 * r["se_slack"]
    in_all = read >= 4 / 3 - 3 * se_read and read <= 2.0 + 3 * se_read \
        and (read - 3 * se_read <= 1.9144 and read + 3 * se_read >= 0.9184) \
        and (W_SHELL_BAND[0] - 3 * 0.025 <= read <= W_SHELL_BAND[1] + 3 * 0.025)
    consistent_open = ("C" in vR_) and ("C" in vU_) and bp_ and in_all
    log(f"  R = {r['R']:.4f} +- {r['se_R_block']:.4f} -> reading = "
        f"{read:.4f} +- {se_read:.4f}  (record 1.8178)  z = {z:.2f}")
    log(f"  vR={''.join(sorted(vR_))} vU={''.join(sorted(vU_))} B={'P' if bp_ else 'V'}"
        f" reading-in-all-windows={in_all}")
    log(f"  doorB verdict: {'CONSISTENT-OPEN REPRODUCED' if consistent_open else 'MISMATCH'}")
    checks["C6_doorB"] = consistent_open and abs(z) < 5
    c6 = dict(read=round(read, 4), se=round(se_read, 4), z=round(z, 2),
              vR="".join(sorted(vR_)), vU="".join(sorted(vU_)),
              interpretation="CONSISTENT-OPEN")
    ok_all &= checks["C6_doorB"]

    # ---------------- decision tree + min-n -------------------------------
    log("\n" + "=" * 78)
    log("DECISION TREE (locked, md 0.6): B gate -> R window+pin -> U readout")
    log("=" * 78)
    tree_rows = []
    for r in RES:
        if r["src"] not in ("central", "volume"):
            continue  # shell tree-eval skipped (atlas row exists only C/V)
        tag = r["tag"]; k = r["kernel"]
        qh = None; atlas = None
        # node1
        gapB = r["slack"] - 1.0
        if r["slack"] < 1.0 - 3 * r["se_slack"]:
            tree = "KILL-B"; fail = []
        elif gapB < 3 * r["se_slack"]:
            tree = "UNDET-B"; fail = ["B_gate_n_too_small"]
        else:
            # node2
            vR = verdiR_set(r["R"], r["se_R_block"])
            fail = []
            if "C" not in vR:
                tree = "NOT-CENTRAL"; fail.append("R_excludes_central")
            else:
                # K06-inv with (A, dbar):  a=-lnA, d=dbar
                a_ = -math.log(max(r["A"], 1e-300))
                qh = (6.0 * a_ - 12.0 * r["dbar"]) / (4.0 * r["dbar"] - 3.0 * a_)
                th = a_ / (1.0 + qh / 3.0)
                # node3: nearest grid row (tau0,q) to (th, qh)
                row = min(((t, qq) for t in TAU0S for qq in QS),
                          key=lambda tq: (tq[0] - th) ** 2 / 1.0 + (tq[1] - qh) ** 2 / 9.0)
                # atlas U columns: thomson -> N04 record; iso -> this run (flagged)
                if k == "thomson":
                    uC, seC = U_REC[("central", row[0], row[1])]
                    uV, seV = U_REC[("volume", row[0], row[1])]
                    atlas = "N04-record"
                else:
                    cC = res_by[("central", row[0], row[1], "iso", None)]
                    cV = res_by[("volume", row[0], row[1], "iso", None)]
                    uC, seC = cC["U"], cC["se_U_block"]
                    uV, seV = cV["U"], cV["se_U_block"]
                    atlas = "in-run(flagged)"
                se = r["se_U_block"]
                inC = abs(r["U"] - uC) <= 3 * math.hypot(se, seC)
                inV = abs(r["U"] - uV) <= 3 * math.hypot(se, seV)
                if inC and inV:
                    tree = "AMBIG-CV"; fail.append("U_within_3sig_of_both")
                elif inC:
                    tree = "C"
                elif inV:
                    tree = "V"
                else:
                    tree = "U-OUT"; fail.append("U_outside_atlas")
                if r["src"] == "volume" and abs(row[0] - th) > 0.3:
                    fail.append("pin_bias")
            tree_rows.append((tag, qh, tree, fail, atlas))
    # confusion
    conf = {"central": {}, "volume": {}}
    for tag, qh, tree, fail, atlas in tree_rows:
        src = tag[0]
        key = "central" if src == "c" else "volume"
        conf[key][tree] = conf[key].get(tree, 0) + 1
    log("  tree confusion (thomson+iso pooled): truth -> tree verdict")
    for src in ("central", "volume"):
        log(f"    {src:8s}: {conf[src]}")
    # kernel split
    for k in KERNELS:
        for src in ("central", "volume"):
            n_ok = sum(1 for t_, qh, tr, fl, at in tree_rows
                       if t_.endswith(k[:2]) and t_[0] == src[0] and tr in (src[0].upper(),))
            log(f"    {k:9s} {src:8s}: correct-pin {n_ok}/9")
    tree_payload = [dict(tag=t, qh=round(q, 3) if q is not None else None,
                         tree=tr, fail=fl, atlas=at) for t, q, tr, fl, at in tree_rows]

    # ---------------- minimum n per falsifier per cell --------------------
    log("\nMIN-n per falsifier for 3-sigma (LOCKED def: n_req = n (3 se/gap)^2)")
    log("  R-gap: distance to nearest competing W-band (0 if inside) | "
        "U-gap: resolved |U - U_other(tau0,q)| (N04 atlas) | B-gap: slack-1")
    mn = {"B": [], "R": [], "U": []}
    rows_mn = []
    for r in RES:
        if r["src"] not in ("central", "volume"):
            continue
        gapB = r["slack"] - 1.0
        nB = float("inf") if gapB <= 0 else r["n"] * (3 * r["se_slack"] / gapB) ** 2
        # R gap: for each competing geometry the distance to its (widened) band
        gaps = []
        for g in GEO:
            if g == "C" and r["src"] == "central":
                continue
            if g == "V" and r["src"] == "volume":
                continue
            lo, hi = W_BAND[g]
            dg = max(lo - r["R"], r["R"] - hi, 0.0)
            gaps.append(dg)
        gapR = min(gaps)
        nR = float("inf") if gapR <= 1e-8 else r["n"] * (3 * r["se_R_block"] / gapR) ** 2
        # U gap resolved: |U - U_other(tau0,q)| at this cell's (tau0,q)
        other = "volume" if r["src"] == "central" else "central"
        if r["kernel"] == "thomson":
            uo = U_REC[(other, r["tau0"], r["q"])][0]
            seo = U_REC[(other, r["tau0"], r["q"])][1]
        else:
            uo = res_by[(other, r["tau0"], r["q"], "iso", None)]["U"]
            seo = res_by[(other, r["tau0"], r["q"], "iso", None)]["se_U_block"]
        gapU = abs(r["U"] - uo) - 3 * seo
        nU = float("inf") if gapU <= 1e-8 else r["n"] * (3 * r["se_U_block"] / gapU) ** 2
        mn["B"].append((r["tag"], nB)); mn["R"].append((r["tag"], nR))
        mn["U"].append((r["tag"], nU))
        rows_mn.append((r["tag"], nB, nR, nU))
    for f in ("B", "R", "U"):
        vals = [v for _, v in mn[f] if math.isfinite(v)]
        infs = sum(1 for _, v in mn[f] if not math.isfinite(v))
        log(f"  {f}: min {min(vals):9.0f}  med {float(np.median(vals)):9.0f}  "
            f"max {max(vals):9.0f}   (infeasible cells: {infs})")
        tightest = min(mn[f], key=lambda kv: kv[1] if math.isfinite(kv[1]) else 1e300)
        log(f"       tightest cell: {tightest[0]} n={tightest[1]:.0f}")
    log("  per-cell (tag nB nR nU):")
    for t, nb, nr, nu in sorted(rows_mn, key=lambda x: x[0]):
        log(f"    {t:26s} {nb:10.0f} {nr:10.0f} {nu:10.0f}")

    # ---------------- joint 3-sigma regions + overlaps --------------------
    log("\n" + "=" * 78)
    log("JOINT 3-SIGMA REGIONS per (geometry, kernel) + pairwise overlaps")
    log("=" * 78)
    classes_ls = [("C", "thomson"), ("C", "iso"), ("V", "thomson"), ("V", "iso"),
                  ("S03", "thomson"), ("S03", "iso"), ("S05", "thomson"), ("S05", "iso")]
    GEOM_NAME = {"C": "central", "V": "volume", "S03": "shell", "S05": "shell"}
    muS = {}
    for g, k in classes_ls:
        src = GEOM_NAME[g]
        a = 0.3 if g == "S03" else (0.5 if g == "S05" else None)
        cells = [r for r in RES if r["src"] == src and r["kernel"] == k
                 and (r.get("a") == a or (a is None and r.get("a") is None))]
        mu, Sig = class_gauss(cells)
        # sampling covariance at operating cell (tau0=1,q=0; n of the class)
        op = [r for r in cells if r["tau0"] == 1.0 and r["q"] == 0.0][0]
        Ss = np.array(op["cov3"])
        SigT = Sig + Ss
        muS[(g, k)] = dict(mu=mu.tolist(), Sig=Sig.tolist(), SigT=SigT.tolist(),
                           inv=np.linalg.inv(SigT), ns=op["n"])
        log(f"  {g:4s} {k:8s}: mu=({mu[0]:.3f},{mu[1]:.3f},{mu[2]:.3f}) "
            f"landscape sd=({np.sqrt(np.diag(Sig))[0]:.3f},{np.sqrt(np.diag(Sig))[1]:.5f},"
            f"{np.sqrt(np.diag(Sig))[2]:.4f}) samp sd=({np.sqrt(np.diag(Ss))[0]:.4f},"
            f"{np.sqrt(np.diag(Ss))[1]:.4f},{np.sqrt(np.diag(Ss))[2]:.4f})")
    # MC pairwise overlap (2e6 draws from A, fraction inside B's 3-sigma ellipsoid)
    rng = np.random.default_rng(20260925)
    names = [f"{g}:{k}" for g, k in classes_ls]
    ov = np.zeros((8, 8))
    for i, (g, k) in enumerate(classes_ls):
        mi = np.array(muS[(g, k)]["mu"]); Si = np.array(muS[(g, k)]["SigT"])
        X = rng.multivariate_normal(mi, Si, 2_000_000)
        rad = np.sqrt(np.einsum("ij,jk,ik->i", X - mi, np.linalg.inv(Si), X - mi))
        X3 = X[rad <= 3.0]
        f3 = len(X3) / len(X)
        for j, (g2, k2) in enumerate(classes_ls):
            mj = np.array(muS[(g2, k2)]["mu"])
            invj = muS[(g2, k2)]["inv"]
            inside, _ = ellipsoid_membership(X3, mj, invj)
            ov[i, j] = float(np.mean(inside)) * f3
    log(f"  sanity diagonal (self-3sigma mass): "
        f"{['%.3f' % ov[i, i] for i in range(8)]}")
    log("  pairwise overlap A->B (asym fractions; residual degeneracy >= 1%):")
    degen = []
    for i in range(8):
        for j in range(i + 1, 8):
            o = 0.5 * (ov[i, j] + ov[j, i])
            if o >= 0.01:
                degen.append((names[i], names[j], o))
            if o >= 1e-4:
                log(f"    {names[i]:12s} x {names[j]:12s}: overlap {o:.4f}  "
                    f"({ov[i,j]:.4f}/{ov[j,i]:.4f})")
    log(f"  RESIDUAL DEGENERACY (>=1%): {len(degen)} pairs")
    for d in degen:
        log(f"    * {d[0]} x {d[1]} overlap {d[2]:.3f}")

    # ---------------- verdict -------------------------------------------------
    passed = sum(1 for v in checks.values() if v)
    log("\n" + "=" * 78)
    log("V03 VERDICT")
    log("=" * 78)
    for c, v in checks.items():
        log(f"  {c:24s}: {'PASS' if v else 'FAIL'}")
    log(f"  checks {passed}/{len(checks)}")
    res_all = dict(
        title="V03 IGNORANCE-ORTHOGONAL TRIO",
        pre_registration=PRE,
        checks=checks,
        cells={r["tag"]: {kk: r[kk] for kk in
                          ("n", "tau0", "q", "src", "kernel", "a", "A", "dbar",
                           "d2bar", "dv2", "v4m", "R", "U", "slack", "se_R",
                           "se_U", "se_R_block", "se_U_block", "se_slack",
                           "cov_RU", "cov3", "secs")} for r in RES},
        kernel_diff=dict(c3=c3, c7=c7,
                         diffs={f"{r['tag']}": dict(dR=round(
                             res_by[(r['src'], r['tau0'], r['q'],
                                     'iso', r.get('a'))]["R"] - r["R"], 6)) for r in RES
                                if r["kernel"] == "thomson"}),
        disagreement=dict(counts={cl: len(classes.get(cl, [])) for cl in (
            "KILL-B", "VOID-R", "VOID-U", "MIRROR", "CROSS", "HIERARCHY", "TRIO-AGREE")},
            per_cell=con,
            non_agree=[k for k, v in con.items() if v["cls"] != "TRIO-AGREE"],
            U_shell_band_flagged=U_BAND_S),
        doorB=c6,
        decision_tree=dict(confusion=conf, rows=tree_payload),
        min_n={f: [dict(cell=t, n=round(v) if math.isfinite(v) else None)
                   for t, v in mn[f]] for f in ("B", "R", "U")},
        joint_regions={f"{g}:{k}": muS[(g, k)] for g, k in classes_ls},
        overlaps=dict(names=names, matrix=ov.tolist(),
                      residual_degeneracy=[list(d) for d in degen]),
        wall_seconds=round(time.time() - t_start, 1))
    def _sanitize(o, path=""):
        if isinstance(o, dict):
            return {str(k): _sanitize(v, f"{path}.{k}") for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_sanitize(v, f"{path}[{i}]") for i, v in enumerate(o)]
        if isinstance(o, (np.floating, np.integer)):
            return float(o)
        if isinstance(o, np.ndarray):
            return _sanitize(o.tolist(), path)
        if isinstance(o, (float, int, str, bool)) or o is None:
            return o
        raise TypeError(f"unserializable {type(o)} at {path}")
    json.dump(_sanitize(res_all), open("V03_results.json", "w"), indent=1)
    log(f"\nWROTE V03_results.json; wall {time.time()-t_start:.0f}s; "
        f"ALL V03 CHECKS {'PASSED' if ok_all else 'FAILED'}")
    sys.exit(0 if ok_all else 1)