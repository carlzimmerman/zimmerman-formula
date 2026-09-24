#!/usr/bin/env python3
"""
L07 -- PHASE-FUNCTION INDEPENDENCE OF THE WINDOW + INVERSION
      (the KERNEL-FREE WINDOW test)
2026-09-23.  Deepseek lane; no git commit.

CLAIM (strong robustness statement).  The central-source window
    -ln A / E[D]  =  (1+q/3)/(1/2+q/4)
and the inversion (A, E[D]) -> (tau0, q) (K04/K06-inv) use ONLY the atom
fraction A = P(no collision) and the mean delay E[D].  A is a no-scattering
probability (the kernel never fires), and E[D] = int_0^1 r kappa(r) dr obeys
a first-moment identity whose scattering term is proportional to the kernel
mean cosine E[mu] (the J02 Dynkin argument: L(x.u) = 1 - x.u + E[mu]-term).
ANY symmetric kernel (E[mu] = 0) leaves both unchanged.  The WIDTH channel
E[v^2] = 2 E[ang] = 2 E[N] carries the phase function through E[N], the
residence functional.  Hence the falsifier battery F1 (atom A), F2 (E[D]
from the lag), F6 (the window) classify the scattering phase function ONLY
through the width channel: an observer who does not know the kernel can
still use (A, dbar) for the J10-I radius test.

TEST.  Replace the Thomson kernel (3/8)(1+mu^2) with ISOTROPIC p(mu) = 1/2
(acceptance-sampled, same envelope proposal as thomson_mu), SAME optical-
depth transport (verbatim J02 copy with a kernel switch; parity-checked
against the imported engine under the Thomson kernel).  Central source,
tau0 = 1, q in {0, 3, 10}, n = 3e6:
  (a) A = exp(-tau0 (1+q/3))   unchanged (kernel never fires for the atom)
  (b) E[D] = tau0 (1/2+q/4)    unchanged (symmetric-kernel first moment)
  (c) window ratio = (1+q/3)/(1/2+q/4) within 3 SE of the closed form, and
      iso-vs-Thomson window equal within 3 combined SE (direct read)
  (d) E[N] and E[v^2] DIFFER from Thomson: the kernel enters the width
      channel -- measure the difference and its SE significance
  (e) the K06-inv inversion on the isotropic (A_hat, dbar_hat) recovers
      (tau0, q) = (1, q) within 3 SE (inversion is kernel-independent)
Volume source, q = 0, tau0 in {0.5, 1, 2, 3} (n = 2e6): does the J11
tau0-CROSSING of the volume window (2.049/1.894/1.629/1.423 Thomson record)
survive the kernel change?  (E[D]_vol carries the kernel-dependent Q; the
atom A_vol is kernel-free and must match J11 quadrature exactly.)

KILL (pre-registered): (c) violation > 5 SE of the closed-form window =>
the window carries kernel dependence and the J09/J10 radius test must be
kernel-tagged.  Reported with the measured deviation.
"""
import json
import math
import sys
import time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, "/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push")
from J02_moment_hierarchy import simulate as j02_simulate  # parity reference

OUT = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)

# ----------------------------------------------------------------------
# Kernels.  thomson_mu verbatim from J02; isotropic_mu acceptance-sampled
# with the same proposal (uniform on [-1,1]): p(m)/pmax = (1/2)/(1/2) = 1,
# so the first candidate is accepted -- the loop structure is kept so the
# acceptance sampling is visible and the API matches thomson_mu.
# ----------------------------------------------------------------------
def thomson_mu(rng, n):
    out = np.empty(n); todo = np.arange(n)
    while len(todo):
        m = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < (1 + m*m) / 2
        out[todo[take]] = m[take]; todo = todo[~take]
    return out


def isotropic_mu(rng, n):
    # p(mu) = 1/2 on [-1,1]  (normalized: int_-1^1 (1/2) dmu = 1)
    out = np.empty(n); todo = np.arange(n)
    while len(todo):
        m = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < 1.0      # p(m)/pmax = (1/2)/(1/2) = 1
        out[todo[take]] = m[take]; todo = todo[~take]
    return out


MU_FN = {"thomson": thomson_mu, "iso": isotropic_mu}

# ----------------------------------------------------------------------
# Transport: verbatim J02_moment_hierarchy.simulate with a kernel switch.
# Same exact optical-depth bisection, same rate integral, same flight
# geometry; only the mu draw changes.
# ----------------------------------------------------------------------
def rate_integral(a, b, ds, tau0, q):
    return tau0 * (ds + q * (a * ds + b * ds**2 + ds**3 / 3))


def simulate(n, tau0, q, source, seed, kernel="thomson"):
    mu_draw = MU_FN[kernel]
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    if source == "volume":
        d0 = rng.normal(size=(n, 3)); d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
        pos = d0 * rng.random(n)[:, None] ** (1/3)      # uniform in unit ball
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
        disc = pd*pd - r2 + 1.0
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
                mid = 0.5*(lo + hi)
                val = rate_integral(r2i, pdi, mid, tau0, q) + np.log(Ui)
                tak = val < 0
                lo[tak] = mid[tak]; hi[~tak] = mid[~tak]
            s[inner] = 0.5*(lo + hi)
        elapsed[alive] += s
        pos[alive] += u * s[:, None]
        alive = alive[~esc]
        if len(alive) == 0:
            break
        p, u = pos[alive], direc[alive]
        r2 = np.sum(p*p, axis=1)
        mu = mu_draw(rng, len(alive))
        t = rng.normal(size=(len(alive), 3))
        t -= np.sum(t*u, axis=1)[:, None] * u
        tn = np.linalg.norm(t, axis=1)
        t = t / tn[:, None]
        newu = u*mu[:, None] + t*np.sqrt(1 - mu*mu)[:, None]
        kick = rng.normal(size=(len(alive), 3))
        v[alive] += np.sum(kick*(newu - u), axis=1)
        ang[alive] += 1.0 - mu
        N[alive] += 1
        direc[alive] = newu
    D = elapsed - np.sum((pos - origin) * direc, axis=1)
    assert np.all(D >= -1e-9)
    return dict(v2=v*v, D=D, ang=ang, N=N)


def se(x):
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))


def block_estimates(A_bool, D, nb=10, seed=0):
    """Per-block (A, dbar, window); SE of the pooled window from blocks."""
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(D))
    bs = np.array_split(perm, nb)
    out = []
    for b in bs:
        A_b = float(A_bool[b].mean())
        d_b = float(D[b].mean())
        out.append((A_b, d_b, -math.log(max(A_b, 1e-300)) / d_b))
    return np.array(out)


def inv_of(a, d):
    """K06-inv closed-form inversion: (a, d) = (-ln A, E[D]) -> (tau0, q)."""
    qh = (6.0*a - 12.0*d) / (4.0*d - 3.0*a)
    th = a / (1.0 + qh/3.0)
    return th, qh


# ----------------------------------------------------------------------
RUNS = []
def add_central(q, kernel, seed, n=3_000_000):
    RUNS.append(dict(n=n, tau0=1.0, q=q, source="central", kernel=kernel,
                     seed=seed, tag=f"c_q{int(q)}_{kernel}"))
def add_volume(tau0, q, kernel, seed, n=2_000_000):
    RUNS.append(dict(n=n, tau0=tau0, q=q, source="volume", kernel=kernel,
                     seed=seed, tag=f"v_t{tau0:g}_q{int(q)}_{kernel}"))

# isotropic science runs (central, n = 3e6)
for q in (0.0, 3.0, 10.0):
    add_central(q, "iso", seed=20260001 + int(q))
# Thomson same-(tau0,q) baselines at the same n (width-channel comparisons)
for q in (0.0, 3.0, 10.0):
    add_central(q, "thomson", seed=20261001 + int(q))
# volume-scan runs: J11 port under the isotropic kernel (q=0) + baselines
for t in (0.5, 1.0, 2.0, 3.0):
    add_volume(t, 0.0, "iso", seed=20262001 + int(t*10))
add_volume(1.0, 0.0, "thomson", seed=20262101)        # same-n Thomson baseline
add_volume(1.0, 10.0, "iso", seed=20262201)           # sub-4/3 landmark bonus


def one_run(spec):
    t0 = time.time()
    r = simulate(spec["n"], spec["tau0"], spec["q"], spec["source"],
                 spec["seed"], spec["kernel"])
    A_bool = (r["N"] == 0)
    A = float(A_bool.mean())
    dbar = float(r["D"].mean())
    w = -math.log(max(A, 1e-300)) / dbar
    res = dict(
        tag=spec["tag"], tau0=spec["tau0"], q=spec["q"], source=spec["source"],
        kernel=spec["kernel"], n=spec["n"],
        A=A, seA=se(A_bool),
        dbar=dbar, seD=se(r["D"]),
        window=w, blocks=block_estimates(A_bool, r["D"], seed=spec["seed"] % 2**31),
        meanN=float(r["N"].mean()), seN=se(r["N"].astype(float)),
        meanv2=float(r["v2"].mean()), sev2=se(r["v2"]),
        secs=time.time()-t0)
    return res


def main():
    ok = True
    res = {"title": "L07 KERNEL-FREE WINDOW: phase-function independence of "
                    "the window + inversion (atom A, lag E[D], ratio F6)",
           "question": "Hold the optical-depth transport fixed and replace the "
                       "Thomson kernel (3/8)(1+mu^2) by ISOTROPIC p(mu)=1/2: "
                       "do A, E[D], the window and the inversion survive "
                       "(phase-function-independent), while E[N], E[v^2] "
                       "absorb the kernel (width channel)?",
           "checks": {}, "measurements": {}}
    log("=" * 96)
    log("L07 -- KERNEL-FREE WINDOW  (phase-function independence of window + inversion)")
    log("=" * 96)

    # ---- P: parity of the copied transport vs the imported J02 engine -----
    log("\n[P] parity: copied Thomson transport vs imported J02 simulate")
    for (tau0, q, n) in ((1.0, 0.0, 200_000), (1.0, 3.0, 200_000)):
        a = simulate(n, tau0, q, "central", 777, "thomson")
        b = j02_simulate(n, tau0, q, "central", 777)
        for name, x, y in (("E[N]", a["N"].mean(), b["N"].mean()),
                           ("E[D]", a["D"].mean(), b["D"].mean()),
                           ("A", (a["N"] == 0).mean(), (b["N"] == 0).mean()),
                           ("E[v2]", a["v2"].mean(), b["v2"].mean())):
            # identical seeds + identical code path -> bitwise identity
            z = abs(x - y) / max(1e-12, abs(x))
            res["checks"][f"P_{name}_q{int(q)}"] = bool(z < 1e-9)
            ok &= res["checks"][f"P_{name}_q{int(q)}"]
        log(f"  tau0={tau0} q={q}: E[N] {a['N'].mean():.6f} vs {b['N'].mean():.6f}"
            f"  E[D] {a['D'].mean():.6f} vs {b['D'].mean():.6f}"
            f"  A {((a['N']==0).mean()):.6f} vs {((b['N']==0).mean()):.6f}"
            f"  E[v2] {a['v2'].mean():.6f} vs {b['v2'].mean():.6f}"
            "  (identical seeds -> bitwise-identical)")

    # ---- run all specs (parallel) -----------------------------------------
    t0 = time.time()
    log(f"\n[run] {len(RUNS)} specifications (pool of 6)")
    with Pool(6) as pool:
        results = pool.map(one_run, RUNS, chunksize=1)
    log(f"[run] wall {time.time()-t0:.1f}s")
    R = {}
    for r in results:
        R[r["tag"]] = r

    WPRED = {q: (1.0 + q/3.0) / (0.5 + q/4.0) for q in (0.0, 3.0, 10.0)}

    # ---- (a)(b)(c)(e) central isotropic vs closed forms --------------------
    log("\n[A] central source, tau0=1, ISOTROPIC kernel  (n=3e6, SEs from data)")
    log("    q   A_hat      seA      E[D]_hat   seD     window   seW   "
        "W_pred   zW    tau0_hat  q_hat")
    for q in (0.0, 3.0, 10.0):
        r = R[f"c_q{int(q)}_iso"]
        blocks = r["blocks"]
        seW = float(blocks[:, 2].std(ddof=1)) / math.sqrt(len(blocks))
        # (a)
        A_pred = math.exp(-1.0 * (1.0 + q/3.0))
        zA = abs(r["A"] - A_pred) / r["seA"]
        res["checks"][f"K1a_atom_q{int(q)}"] = bool(zA < 3.0)
        ok &= res["checks"][f"K1a_atom_q{int(q)}"]
        # (b)
        d_pred = 1.0 * (0.5 + q/4.0)
        zD = abs(r["dbar"] - d_pred) / r["seD"]
        res["checks"][f"K1b_lag_q{int(q)}"] = bool(zD < 3.0)
        ok &= res["checks"][f"K1b_lag_q{int(q)}"]
        # (c) window vs closed form, 3 SE budget; KILL at > 5 SE
        zW = abs(r["window"] - WPRED[q]) / seW
        res["checks"][f"K1c_window_q{int(q)}"] = bool(zW < 3.0)
        killed = zW > 5.0
        res["measurements"][f"K1c_kill_q{int(q)}"] = bool(killed)
        ok &= res["checks"][f"K1c_window_q{int(q)}"]
        # (e) inversion from (A_hat, dbar_hat), block SEs
        # a = -ln A enters the closed-form inverse (K06-inv)
        invs = np.array([inv_of(-math.log(max(b[0], 1e-300)), b[1])
                         for b in blocks])
        tau0h, qh = inv_of(-math.log(r["A"]), r["dbar"])
        seT = float(invs[:, 0].std(ddof=1)) / math.sqrt(len(invs))
        seQ = float(invs[:, 1].std(ddof=1)) / math.sqrt(len(invs))
        zT = abs(tau0h - 1.0) / seT
        zQ = abs(qh - q) / seQ
        res["checks"][f"K1e_inv_tau0_q{int(q)}"] = bool(zT < 3.0)
        res["checks"][f"K1e_inv_q_q{int(q)}"] = bool(zQ < 3.0)
        ok &= res["checks"][f"K1e_inv_tau0_q{int(q)}"] and res["checks"][f"K1e_inv_q_q{int(q)}"]
        res["measurements"][f"c_q{int(q)}_iso"] = dict(
            A=round(r["A"], 6), A_pred=round(A_pred, 6), zA=round(zA, 2),
            dbar=round(r["dbar"], 6), d_pred=round(d_pred, 6), zD=round(zD, 2),
            window=round(r["window"], 6), W_pred=round(WPRED[q], 6),
            zW=round(zW, 2), seW=round(seW, 6),
            tau0_hat=round(tau0h, 6), q_hat=round(qh, 6),
            seT=round(seT, 5), seQ=round(seQ, 5), zT=round(zT, 2), zQ=round(zQ, 2),
            meanN=round(r["meanN"], 5), seN=round(r["seN"], 5),
            meanv2=round(r["meanv2"], 5), sev2=round(r["sev2"], 5),
            secs=round(r["secs"], 1))
        log(f"  q={q:5.0f} {r['A']:.6f} {r['seA']:.2e} {r['dbar']:.6f} {r['seD']:.2e} "
            f"{r['window']:.5f} {seW:.2e} {WPRED[q]:.5f} {zW:5.2f}  "
            f"{tau0h:6.3f} {qh:6.3f}   (zA={zA:.2f} zD={zD:.2f})"
            + ("   *** KILL: window > 5 SE ***" if killed else ""))

    # ---- (c2)(d) iso vs Thomson, direct cross-kernel reads ----------------
    log("\n[B] cross-kernel: ISOTROPIC vs THOMSON at the same (tau0=1, q, n=3e6)")
    res["measurements"]["width_channel"] = {}
    for q in (0.0, 3.0, 10.0):
        ri = R[f"c_q{int(q)}_iso"]
        rt = R[f"c_q{int(q)}_thomson"]
        seWi = float(ri["blocks"][:, 2].std(ddof=1)) / math.sqrt(10)
        seWt = float(rt["blocks"][:, 2].std(ddof=1)) / math.sqrt(10)
        zWx = abs(ri["window"] - rt["window"]) / math.hypot(seWi, seWt)
        res["checks"][f"K1c2_window_iso_vs_thom_q{int(q)}"] = bool(zWx < 3.0)
        ok &= res["checks"][f"K1c2_window_iso_vs_thom_q{int(q)}"]
        # (d) width channel: E[N] and E[v2] must DIFFER (kernel enters here)
        dN = ri["meanN"] - rt["meanN"]
        zN = abs(dN) / math.hypot(ri["seN"], rt["seN"])
        dV = ri["meanv2"] - rt["meanv2"]
        zV = abs(dV) / math.hypot(ri["sev2"], rt["sev2"])
        res["checks"][f"K1d_N_differs_q{int(q)}"] = bool(zN > 3.0)
        ok &= res["checks"][f"K1d_N_differs_q{int(q)}"]
        # E[v^2] = 2 E[N] (spine; E[mu]=0 both kernels) => the v^2 shift must
        # equal TWO times the N shift; that is how the kernel enters the
        # width channel (measured, not assumed)
        dV2 = abs(dV - 2.0*dN) / math.hypot(ri["sev2"], rt["sev2"],
                                            2.0*ri["seN"], 2.0*rt["seN"])
        res["checks"][f"K1d_v2_tracks_2N_q{int(q)}"] = bool(dV2 < 3.0)
        ok &= res["checks"][f"K1d_v2_tracks_2N_q{int(q)}"]
        # spine consistency per kernel: E[v2] = 2 E[N] (E[mu]=0 both kernels)
        for k, r_ in (("iso", ri), ("thomson", rt)):
            zE = abs(r_["meanv2"] - 2.0*r_["meanN"]) / math.hypot(r_["sev2"], 2.0*r_["seN"])
            res["checks"][f"K1d_spine_{k}_q{int(q)}"] = bool(zE < 3.0)
            ok &= res["checks"][f"K1d_spine_{k}_q{int(q)}"]
        res["measurements"]["width_channel"][f"q{int(q)}"] = dict(
            window_iso=round(ri["window"], 6), window_thom=round(rt["window"], 6),
            zWx=round(zWx, 2),
            meanN_iso=round(ri["meanN"], 5), meanN_thom=round(rt["meanN"], 5),
            dN=round(dN, 5), zN=round(zN, 2), relN=round(dN/rt["meanN"], 4),
            meanv2_iso=round(ri["meanv2"], 5), meanv2_thom=round(rt["meanv2"], 5),
            dV=round(dV, 5), zV=round(zV, 2), relV=round(dV/rt["meanv2"], 4))
        log(f"  q={q:5.0f} window iso {ri['window']:.5f} vs thom {rt['window']:.5f}"
            f"  z={zWx:5.2f}   |   E[N] iso {ri['meanN']:7.4f} vs thom {rt['meanN']:7.4f}"
            f"  d={dN:+7.4f} z={zN:6.1f} ({dN/rt['meanN']:+.1%})  |  "
            f"E[v2] iso {ri['meanv2']:7.4f} vs thom {rt['meanv2']:7.4f}"
            f"  d={dV:+7.4f} z={zV:6.1f} ({dV/rt['meanv2']:+.1%})")

    # ---- (4) volume source, isotropic kernel: J11 tau0-crossing -----------
    log("\n[C] volume source q=0, ISOTROPIC kernel  (n=2e6): J11 port")
    log("    tau0  A_iso     A_quad    zA   E[D]v,iso   window_iso  "
        "J11 thom  central-flat")
    quad = {}
    for t in (0.5, 1.0, 2.0, 3.0):
        quad[t] = quadrature_A_vol(t, 0.0)
    seq = []
    for t in (0.5, 1.0, 2.0, 3.0):
        r = R[f"v_t{t:g}_q0_iso"]
        Aq = quad[t]
        # volume atom is kernel-free: must match the J11 quadrature exactly
        zAq = abs(r["A"] - Aq) / r["seA"]
        res["checks"][f"K4_vol_atom_quad_t{int(t*10)}"] = bool(zAq < 3.0)
        ok &= res["checks"][f"K4_vol_atom_quad_t{int(t*10)}"]
        seW = float(r["blocks"][:, 2].std(ddof=1)) / math.sqrt(10)
        seq.append((t, r["window"], seW))
        log(f"  t={t:4.1f} {r['A']:.5f}  {Aq:.5f}  {zAq:4.2f}   "
            f"{r['dbar']:.5f}   {r['window']:.5f} +- {seW:.4f}")
    w05, se05 = seq[0][1], seq[0][2]
    w30, se30 = seq[-1][1], seq[-1][2]
    z_dec = (w05 - w30) / math.hypot(se05, se30)
    # J11 fingerprint (direct MC reading): volume window strictly BELOW the
    # central flat value 2.0 at every depth (the discriminator), decreasing
    # in tau0 (the tau0-crossing), and sub-4/3 at q=10.  (J11's own table
    # entry 2.049 at t=0.5 was the thin-scaling PROXY -lnA/(t*0.338), not a
    # direct window; the direct MC values in J11's V3 were 1.897 at t=1.)
    below = [(2.0 - w) / sw for (_t, w, sw) in seq]
    res["checks"]["K4_vol_window_below_central_2"] = bool(min(below) > 10.0)
    res["checks"]["K4_crossing_monotone_down"] = bool(z_dec > 4.0)
    ok &= (res["checks"]["K4_vol_window_below_central_2"]
           and res["checks"]["K4_crossing_monotone_down"])
    # same-n Thomson baseline at tau0=1: measure the kernel shift in E[D]_vol
    rt = R["v_t1_q0_thomson"]
    ri1 = R["v_t1_q0_iso"]
    zDvol = abs(ri1["dbar"] - rt["dbar"]) / math.hypot(ri1["seD"], rt["seD"])
    zWvol = abs(ri1["window"] - rt["window"]) / math.hypot(
        float(ri1["blocks"][:, 2].std(ddof=1)) / math.sqrt(10),
        float(rt["blocks"][:, 2].std(ddof=1)) / math.sqrt(10))
    res["checks"]["K4_Edvol_kernel_shift_measured"] = bool(zDvol > 3.0)
    res["measurements"]["volume"] = dict(
        iso_seq={f"t{t:g}": dict(A=round(R[f"v_t{t:g}_q0_iso"]["A"], 6),
                                 dbar=round(R[f"v_t{t:g}_q0_iso"]["dbar"], 6),
                                 window=round(R[f"v_t{t:g}_q0_iso"]["window"], 6),
                                 seW=round(float(
                                     R[f"v_t{t:g}_q0_iso"]["blocks"][:, 2].std(ddof=1)
                                     / math.sqrt(10)), 6))
                 for t in (0.5, 1.0, 2.0, 3.0)},
        thom_t1=dict(dbar=round(rt["dbar"], 6), window=round(rt["window"], 6)),
        iso_t1=dict(dbar=round(ri1["dbar"], 6), window=round(ri1["window"], 6)),
        z_Dvol_shift=round(zDvol, 2), z_window_shift=round(zWvol, 2),
        tau0_crossing_decrease_z=round(z_dec, 2),
        J11_thom_record=[2.049, 1.894, 1.629, 1.423])
    log(f"  E[D]_vol(iso,t=1)={ri1['dbar']:.5f} vs thom {rt['dbar']:.5f}"
        f"  z={zDvol:.2f}   window {ri1['window']:.5f} vs {rt['window']:.5f}"
        f"  z={zWvol:.2f}")
    # bonus: q=10 volume landmark (J11: 1.3142, below 4/3) under iso
    rb = R["v_t1_q10_iso"]
    seWb = float(rb["blocks"][:, 2].std(ddof=1)) / math.sqrt(10)
    z43 = (4.0/3.0 - rb["window"]) / seWb
    res["checks"]["K4_vol_q10_below_4over3"] = bool(z43 > 3.0)
    ok &= res["checks"]["K4_vol_q10_below_4over3"]
    log(f"  [bonus] volume q=10 tau0=1 iso: window = {rb['window']:.5f} +- {seWb:.4f}"
        f"  (4/3 - w)/se = {z43:.1f}   (J11 Thomson: 1.3142)")
    res["measurements"]["volume"]["q10_iso_t1"] = dict(
        window=round(rb["window"], 6), A=round(rb["A"], 6),
        dbar=round(rb["dbar"], 6), z43=round(z43, 2), W_J11_thom=1.3142)

    # ---- verdict -----------------------------------------------------------
    KILLED = any(res["measurements"].get(f"K1c_kill_q{int(q)}", False) for q in (0.0, 3.0, 10.0))
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    res["window_kernel_dependence_kill"] = bool(KILLED)
    res["verdict"] = ("WINDOW KERNEL-DEPENDENT (KILL FIRED)" if KILLED else
                      "PHASE-FUNCTION-INDEPENDENT: window + inversion survive "
                      "the kernel change; kernel enters only the width channel")
    print(json.dumps(res, indent=1))
    print("ALL L07 CHECKS PASSED" if ok else "L07 CHECK FAILURE")
    with open("/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/"
              "L07_results.json", "w") as f:
        json.dump(res, f, indent=1)
    return 0 if ok else 1


def quadrature_A_vol(tau0, q, ng=80):
    """J11 closed-form volume atom (kernel-free escape probability)."""
    xr, wr = np.polynomial.legendre.leggauss(ng); r = 0.5*xr + 0.5
    xm, wm = np.polynomial.legendre.leggauss(2*ng); mu = xm
    R = r[:, None]; MU = mu[None, :]
    Wr = (3.0*R**2) * (0.5*wr[:, None])
    Wm = 0.5*wm[None, :]
    ch = -R*MU + np.sqrt(np.maximum(0.0, 1.0 - R*R*(1.0 - MU*MU)))
    te = tau0 * (ch + q*(R*R*ch + R*MU*ch*ch + ch**3/3.0))
    return float(np.sum(Wr * np.exp(-te) * Wm))


if __name__ == "__main__":
    sys.exit(main())