#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE11b -- IS DE11's FOREST PASS CONVERGED?  The converged model's switch at L362's mass and mesh resolutions.

WHY.  DE11 found the converged model (MOND-sector switch, vacuum-gated at p = 1, x_c0 = 2.5) passes the forest easily:
worst |P1D/P1D_LCDM - 1| = 0.0041 against 0.10.  But the deviation grew 4.6x from the 50 to the 25 Mpc/h box, as the halo
cores where the gate switches on became better resolved.  L362 found the constant-threshold switch's deviation keeps
growing with resolution.  A pass that grows 4.6x per doubling would cross 0.10 within about two more doublings.  This
lane measures the next step.

METHOD.  L362's generalised machinery is imported unchanged: L347's arithmetic line for line, with any (box L, mesh NG,
particles NP), CLASS extended to 60 h/Mpc, and the same seed.  DE11's MOND-sector switch is inserted exactly as in DE11:
x_MS = 1.5 Omega_m(a)[f_b delta + delta_ph], the phantom lagged one step, threshold 2.5 E(z)^2, W with w = 0.25.
Runs at 25 Mpc/h:
  ctrl (25, 128, 96)   DE11's own resolution (control)
  B    (25, 128, 128)  mass resolution (L362's B)
  C    (25, 256, 192)  mesh and mass, 2x finer mesh (L362's C)
The kernel reads all matter, and the fluid is single, so the phantom is over-stated as in DE11.
CHECKS
  C1 CONTROL: the ctrl run reproduces DE11's committed L25 (canonical, w = 0.25) worst deviation to 1e-3 (CLASS's
     k-table differs, 40 vs 60 h/Mpc, as in L362's own control).
  F1 [pre-declared hypothesis, load-bearing] the converged model still passes L347's rule at the highest resolution:
     worst <= 0.10 at B and C (alt footing, the worse one in DE11; canonical at B).
  G1 (reported) the growth, footing by footing: worst(B)/worst(ctrl) and worst(C)/worst(ctrl), against DE11's 4.6x
     per doubling.
MUTATE=1: the switch is on everywhere (f = 1, full QUMOND) at B: F1 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_energy_2026/DE11b_forest_convergence.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
G03 = os.path.join(REPO, "real_research", "g03_audit_2026")
sys.path.insert(0, G03)
import L362_forest_pincer_convergence as L62                          # noqa: E402  (L362's machinery, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE11b_forest_convergence"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE11b", "mutate": MUTATE, "checks": {}, "numbers": {}}
FB = 0.02237 / (0.02237 + 0.1200)
EXPECT_PASS = True                                                    # F1, set before the run
INF = float("inf")


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


def Wsm(t):
    t = np.asarray(t, float)
    tt = np.clip(t, 1e-6, 1 - 1e-6)
    ell = np.clip(1 / tt - 1 / (1 - tt), -700, 700)
    return np.where(t >= 1, 1.0, np.where(t <= 0, 0.0, 1 / (1 + np.exp(ell))))


def run(cfg):
    """L362's run() with DE11's switch.  mode: 'lcdm' | 'mond' (DE11's door) | 'all' (f = 1 everywhere)."""
    name, L, NG, NP, mode, foot, w = cfg
    s = L62.Sim(L, NG, NP)
    rng = np.random.default_rng(7)
    kk = np.sqrt(s.K2); kk[0, 0, 0] = s.kf
    Pk = np.vectorize(lambda q: L62.P_lin(q, L62.ZI))(np.clip(kk, s.kf, 60.0)); Pk[0, 0, 0] = 0
    white = np.fft.fftn(rng.normal(size=(NG, NG, NG)))
    delta0 = np.real(np.fft.ifftn(white * np.sqrt(Pk * NG ** 3 / L ** 3)))
    psi = [-gg for gg in s.grad(s.poisson(delta0))]
    q = (np.arange(NP) + 0.5) * L / NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing='ij'); Q = np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)
    disp = np.stack([s.interp(pp, Q) for pp in psi], 1)
    ai = 1 / (1 + L62.ZI); fg = L62.Om_a(ai) ** 0.55
    x = (Q + disp) % L; p = ai ** 2 * L62.Hnorm(ai) * fg * disp
    npart = len(x); a0 = L62.A0[foot]
    state = {"dph": np.zeros((NG, NG, NG)), "f": np.zeros((NG, NG, NG))}

    def accel(x, a):
        rho = s.deposit(x, np.full(npart, 1.0)) * NG ** 3 / npart
        delta = rho - 1.0
        phiN = s.poisson(1.5 * L62.Om * delta / a)
        if mode == "lcdm":
            phi = phiN
        else:
            gphi = s.grad(phiN)
            mag = np.sqrt(sum((gg / a ** 2) ** 2 for gg in gphi)) + 1e-30
            nu = L62.nu_mono(mag / a0)
            if mode == "all":
                f = np.ones_like(delta)
            else:
                z = 1 / a - 1
                xce = 2.5 * (L62.Om * (1 + z) ** 3 + L62.OL)
                xs = 1.5 * L62.Om_a(a) * (FB * delta + state["dph"])
                f = Wsm((xs / xce - 1) / (2 * w) + 0.5)
            src = s.div([f * (nu - 1) * gg for gg in gphi])
            phi = phiN + s.poisson(src)
            state["dph"] = src / (1.5 * L62.Om / a)
            state["f"] = f
        return -np.stack([s.interp(gg, x) for gg in s.grad(phi)], 1)

    a = ai; dlna = 0.02; zs = list(L62.ZOUT); out = {}
    acc = accel(x, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * L62.Hnorm(a))
        p += 0.5 * dt * acc; x = (x + dt * p / a ** 2) % L; a = a + da
        acc = accel(x, a); p += 0.5 * dt * acc
        for z in list(zs):
            if 1 / a - 1 <= z + 1e-9:
                kpar, p1d = s.flux_p1d(x, p, a, z)
                out[str(z)] = {"kpar": kpar.tolist(), "p1d": p1d.tolist(), "active": float(np.mean(state["f"] > 0.5))}
                zs.remove(z)
    return name, out


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: the switch is on everywhere at B; F1 must FAIL ***")
    if MUTATE:
        cfgs = [("B_lcdm", 25.0, 128, 128, "lcdm", "canonical", 0.25), ("B_alt", 25.0, 128, 128, "all", "alt", 0.25),
                ("ctrl_lcdm", 25.0, 128, 96, "lcdm", "canonical", 0.25), ("ctrl_canonical", 25.0, 128, 96, "mond", "canonical", 0.25)]
    else:
        cfgs = [("C_lcdm", 25.0, 256, 192, "lcdm", "canonical", 0.25), ("C_alt", 25.0, 256, 192, "mond", "alt", 0.25),
                ("B_lcdm", 25.0, 128, 128, "lcdm", "canonical", 0.25), ("B_alt", 25.0, 128, 128, "mond", "alt", 0.25),
                ("B_canonical", 25.0, 128, 128, "mond", "canonical", 0.25),
                ("ctrl_lcdm", 25.0, 128, 96, "lcdm", "canonical", 0.25), ("ctrl_canonical", 25.0, 128, 96, "mond", "canonical", 0.25),
                ("ctrl_alt", 25.0, 128, 96, "mond", "alt", 0.25)]
    with Pool(int(os.environ.get("DE11B_POOL", "3"))) as pool:
        res = dict(pool.map(run, cfgs, chunksize=1))
    P(f"  {len(cfgs)} runs done   [{time.time() - T0:.0f}s]")

    def worst(nm, ref):
        out = 0.0
        for z in ("3.0", "2.0"):
            kp = np.array(res[nm][z]["kpar"]); r = np.array(res[nm][z]["p1d"]) / np.array(res[ref][z]["p1d"])
            m = (kp >= 0.2) & (kp <= 2.0)
            out = max(out, float(np.max(np.abs(r[m] - 1))))
        return out

    banner("C1  CONTROL: DE11's resolution reproduced through L362's generalised machinery")
    D11 = json.load(open(os.path.join(HERE, "DE11_forest_converged_model_results.json")))["numbers"]["F1"]["cells"]
    ref11 = max(D11["L25_canonical_w0.25/z3.0"], D11["L25_canonical_w0.25/z2.0"])
    wc = worst("ctrl_canonical", "ctrl_lcdm")
    check("C1 CONTROL: at DE11's resolution (25, 128, 96) the worst deviation reproduces DE11's committed L25 canonical value",
          f"{wc:.4f} vs DE11 {ref11:.4f} (|diff| {abs(wc - ref11):.1e})", abs(wc - ref11) < 1e-3,
          "CLASS's k-table is extended to 60 h/Mpc here (L362), 40 in DE11")

    banner("F1 G1  THE CONVERGED MODEL'S FOREST AT HIGHER RESOLUTION")
    W = {}
    for nm in [c[0] for c in cfgs if c[4] != "lcdm"]:
        ref = nm.split("_")[0] + "_lcdm"
        W[nm] = worst(nm, ref)
        P(f"    {nm:15s}: worst {W[nm]:.4f};  active mesh fraction z = 2 {res[nm]['2.0']['active']:.2e}")
    OUT["numbers"]["worst"] = W
    tested = {k: v for k, v in W.items() if not k.startswith("ctrl")}
    ok = all(v <= 0.10 for v in tested.values())
    check("F1 [pre-declared] the converged model still passes L347's rule (worst <= 0.10) at the higher resolutions",
          {k: round(v, 4) for k, v in tested.items()}, ok == EXPECT_PASS)
    if not MUTATE:
        g = {"B/ctrl canonical": W["B_canonical"] / W["ctrl_canonical"], "B/ctrl alt": W["B_alt"] / W["ctrl_alt"],
             "C/ctrl alt (2x mesh)": W["C_alt"] / W["ctrl_alt"]}
        OUT["numbers"]["growth"] = g
        check("G1 (reported) growth with resolution against DE11's 4.6x per doubling of the box resolution", g, True,
              load_bearing=False)

    nlb = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    P(f"\n  {sum(ok_ for _, ok_, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
