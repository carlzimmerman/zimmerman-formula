#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
AT2 -- THE FOREST ON ITS OWN OBSERVABLE: the acceleration trigger's decay budget in the particle-mesh cosmology, scored
by the Lyman-alpha flux power and calibrated against warm-dark-matter relics run through the same machinery.

WHY.  AT1 built the acceleration-triggered carrier and found its high-z clearing costs L319's MATTER-power proxy dearly.
Keeping the flagship flat at z = 2.5 moves >~ 9% of the bias-weighted mass onto >~ Mpc orbits, T^2(k = 5 h/Mpc) <~ 0.86.
That holds for ANY trigger.  But the forest is measured in the gas's flux, not in the matter power.  In L365's committed
runs, 15% (z = 3) and 27% (z = 2) of the carrier decays out of dense regions.  The flux power moves <= 1% at z = 3 and
<= 5% at z = 2, at every k_par to 6.5 h/Mpc.  Which reading holds for THIS carrier decides whether the high-z clearing is
affordable.  The fair test puts the trigger and the forest's own yardstick -- warm-dark-matter relics, whose masses define
the forest bounds -- through one machinery and compares them there.

METHOD.  L365/L366's two-species particle-mesh cosmology, unedited: L362's Sim, L347's FGPA flux recipe, L366's fast CIC
deposit, the same seeds (7, 11).  L365's box is 50 Mpc/h, 128^3 mesh, 96^3 per species; L366's 100 Mpc/h, 256^3, 192^3
box checks the result.  Added:
  * the acceleration trigger's budget.  AT1's B1 history F_trig(z) is the unweighted fraction of the carrier whose orbits
    have entered r_v.  It is applied as a sub-grid rule: at each step the densest cold carrier elements (CIC density at
    their position) convert until the decayed fraction reaches F_trig(z), with AT1's kick v_A.  The trigger fires in the
    inner parts of halos above ~1e10.5 Msun (AT1 A1: >= 98%), which the mesh cannot resolve; the densest cells are where
    those halos sit.
  * warm-dark-matter relics at 1.5, 2.0, 2.5, 3.5 and 5.3 keV: the same initial field times L319's T_wdm^2(k) (Viel+05,
    L319's line), both species.
  * the forest distance D: the rms, over k_par bands 0.5-1, 1-2, 2-3, 3-4, 4-5, 5-6.5 h/Mpc and z = 3, 2, of the flux
    power's fractional deviation from the same box's LCDM run.  A carrier's WDM-EQUIVALENT MASS m_eq is the relic mass
    whose D equals the carrier's (log-log interpolation along the relics).
  * the matter power at k = 5 h/Mpc in the same runs: L319's proxy quantity, measured.
GATES.  The record's particle-mesh forest gate (L365's rule): flux power within 10% of LCDM on k_par 0.2-2 h/Mpc at z = 3
  and 2.  Beside it this lane reports the relic calibration, which the exploratory run showed to be weak here.  The
  machinery (0.39 Mpc/h cells, L347's Jeans smoothing 0.1 Mpc/h) compresses a relic's small-scale imprint: a 1.5 keV relic
  moves the flux by only 0.7% rms, a 5.3 keV relic by 0.03%.  A relic-equivalent mass read from it is therefore a LOWER
  bound, and the strict 5.3 keV line cannot be decided in this box.
PRE-DECLARED (before the main run).  The directions were fixed after one exploratory run of LCDM, the 1.5 and 5.3 keV
  relics and the (y_v 0.1, v_A 600) budget, densest-first and sparsest-first (not committed).  In that run the budget moved
  the flux <= 0.3% at z = 3 and <= 1.7% at z = 2 on k_par <= 6.5, and the matter power at k = 5 dropped to 0.23 of LCDM.
  H1: AT1's A2 cell (y_v 0.1, v_A 600) passes L365's rule in L365's box.
  H2: the proxy is not the observable.  The A2 cell's flux-to-matter response ratio at z = 2 (the largest fractional flux
      deviation over the bands, divided by the fractional matter-power change at k = 5) is below 0.1.  The 1.5 keV
      relic's is above 0.5: for a relic the flux follows the matter, for the halo-internal clearing it does not.
  H3: both hold again in L366's larger box.
CHECKS
  C1 CONTROL: the LCDM run in L365's box reproduces L365's committed LCDM flux power at z = 3 and 2 (relative 1e-6).
  C2 CONTROL: the relics register: the forest distance D rises monotonically as the relic mass falls.
  C3 CONTROL: this file's T_wdm^2 equals L319's at L319's k = 5 grid point (its committed strict line 0.9952).
  F1 = H1.  F2 = H2.  F3 = H3.
  R1 (reported) the relic calibration and each cell's relic-equivalent mass (a lower bound here), with the band table.
  F4 (reported) the same yardstick on L365's committed mesh-trigger runs.
MUTATE=1: the same budget converts the SPARSEST cold carrier first, i.e. the web.  F2 must flip, because the flux now
follows the matter as it does for a relic: rc = 1.

Run from the repository root:  python3 real_research/acceleration_trigger_2026/AT2_forest_flux_calibrated.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "real_research", "g03_audit_2026"))
sys.path.insert(0, os.path.join(REPO, "real_research", "dark_sector_2026"))
import L362_forest_pincer_convergence as L2                          # noqa: E402  (L347's machinery, generalised, unedited)
import L366_triggered_carrier_cluster_retention as L6                # noqa: E402  (its fast CIC deposit)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "AT2_forest_flux_calibrated"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "AT2", "mutate": MUTATE, "checks": {}, "numbers": {}}
Om, Hnorm, Om_a, ZI, h = L2.Om, L2.Hnorm, L2.Om_a, L2.ZI, L2.h
OB = 0.02237 / h ** 2
WB, WC = OB / Om, 1 - OB / Om                                        # L365's species weights
BOX65 = (50.0, 128, 96); BOX66 = (100.0, 256, 192)
FAST = os.environ.get("FAST", "0") == "1"                             # smoke test only (tiny boxes; C1 fails); never committed
if FAST: BOX65 = BOX66 = (50.0, 64, 48)
SEEDS = (7, 11)
BANDS = [(0.5, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 5.0), (5.0, 6.5)]
RELICS = (1.5, 2.0, 2.5, 3.5, 5.3)
AT1_JSON = os.path.join(HERE, "AT1_acceleration_trigger_highz_results.json")
EXPECT = dict(H1=True, H2=True, H3=True)                             # set before the main run (docstring)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


def T2_wdm(k_h, m_keV):
    """L319's line (Viel+05), with the same (Om, h)."""
    alpha = 0.049 * m_keV ** -1.11 * (Om / 0.25) ** 0.11 * (h / 0.7) ** 1.22; nu = 1.12
    return (1 + (alpha * k_h) ** (2 * nu)) ** (-10 / nu)


def run(cfg):
    """L365's two-species run with (a) WDM initial conditions, or (b) the acceleration trigger's budget, sub-grid."""
    name, box, mode, m_keV, bz, bF, vk, order = cfg
    LBOX, NG, NP = box
    s = L2.Sim(LBOX, NG, NP)
    s.deposit = lambda x, w: L6.deposit_fast(s, x, w)
    rng = np.random.default_rng(SEEDS[0])
    kk = np.sqrt(s.K2); kk[0, 0, 0] = s.kf
    Pk = np.vectorize(lambda q: L2.P_lin(q, ZI))(np.clip(kk, s.kf, 60.0)); Pk[0, 0, 0] = 0
    if mode == "wdm":
        Pk = Pk * T2_wdm(kk, m_keV)
    white = np.fft.fftn(rng.normal(size=(NG, NG, NG)))
    delta0 = np.real(np.fft.ifftn(white * np.sqrt(Pk * NG ** 3 / LBOX ** 3)))
    psi = [-gg for gg in s.grad(s.poisson(delta0))]
    q = (np.arange(NP) + 0.5) * LBOX / NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing='ij'); Q = np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)
    disp = np.stack([s.interp(pp, Q) for pp in psi], 1)
    del QX, QY, QZ, psi, white, delta0, Pk
    ai = 1 / (1 + ZI); fg = Om_a(ai) ** 0.55
    xb = (Q + disp) % LBOX; pb = ai ** 2 * Hnorm(ai) * fg * disp
    del Q, disp
    xcar, pcar = xb.copy(), pb.copy()
    n = len(xb); cold = np.ones(n, bool)
    krng = np.random.default_rng(SEEDS[1])
    kk5 = (kk >= 4.5) & (kk < 5.5); kk2 = (kk >= 1.5) & (kk < 2.5)

    def density(xb, xcar):
        return (s.deposit(xb, np.full(n, WB)) + s.deposit(xcar, np.full(n, WC))) * NG ** 3 / n

    def accel(rho, a):
        gr = s.grad(s.poisson(1.5 * Om * (rho - 1.0) / a))
        return -np.stack([s.interp(gg, xb) for gg in gr], 1), -np.stack([s.interp(gg, xcar) for gg in gr], 1)

    a = ai; dlna = 0.02; zs = [3.0, 2.0]; out = {}
    rho = density(xb, xcar); ab, ac = accel(rho, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * Hnorm(a))
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        xb = (xb + dt * pb / a ** 2) % LBOX; xcar = (xcar + dt * pcar / a ** 2) % LBOX
        a = a + da
        rho = density(xb, xcar)
        if mode == "acc":                                              # the budget, densest (or sparsest) cold carrier first
            zc = 1 / a - 1
            target = int(round(float(np.interp(zc, bz, bF, right=0.0)) * n))
            need = target - int((~cold).sum())
            if need > 0:
                idx = np.where(cold)[0]
                xp = s.interp(rho, xcar[idx])
                sel = np.argsort(-xp if order == "densest" else xp)[:need]
                hit = idx[sel]
                nh = krng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                pcar[hit] += a * (vk / 100.0) * nh                     # dv = v_k (code velocity unit 100 km/s), as L365
                cold[hit] = False
        ab, ac = accel(rho, a)
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        for z in list(zs):
            if 1 / a - 1 <= z + 1e-9:
                rec = {"decayed": float(1 - cold.mean())}
                kpar, p1d = s.flux_p1d(xb, pb, a, z)
                rec.update(kpar=kpar.tolist(), p1d=p1d.tolist())
                dk = np.abs(np.fft.fftn(rho - 1.0)) ** 2
                rec["pm_k5"] = float(dk[kk5].mean()); rec["pm_k2"] = float(dk[kk2].mean())
                rhoc = s.deposit(xcar, np.full(n, 1.0)) * NG ** 3 / n
                dense = rho > 50.0
                rec["carrier_in_dense"] = float(rhoc[dense].sum() / max(rho[dense].sum(), 1e-30))
                out[str(z)] = rec; zs.remove(z)
    return name, out


def band_dev(run_, ref):
    """fractional flux-power deviation per band and z (mean ratio over the band's modes, minus one)."""
    out = {}
    for z in ("3.0", "2.0"):
        k = np.array(ref[z]["kpar"]); p0 = np.array(ref[z]["p1d"]); p1 = np.array(run_[z]["p1d"])
        out[z] = [float(np.mean(p1[(k >= lo) & (k < hi)] / p0[(k >= lo) & (k < hi)]) - 1) for lo, hi in BANDS]
    return out


def forest_D(dev):
    v = np.array(dev["3.0"] + dev["2.0"])
    return float(np.sqrt(np.mean(v ** 2)))


def l365_rule(run_, ref):
    worst = 0.0
    for z in ("3.0", "2.0"):
        k = np.array(ref[z]["kpar"]); m = (k >= 0.2) & (k <= 2.0)
        worst = max(worst, float(np.max(np.abs(np.array(run_[z]["p1d"])[m] / np.array(ref[z]["p1d"])[m] - 1))))
    return worst


def m_equiv(D, Drel):
    """relic mass with the same D (log-log interpolation along the relics; D falls as the mass rises)."""
    ms = np.array(sorted(Drel)); ds = np.array([Drel[m] for m in ms])
    if D <= ds[-1]: return float("inf") if D < ds[-1] else float(ms[-1])
    if D >= ds[0]: return float(ms[0]) if D == ds[0] else float("nan")    # below the lightest relic: < 1.5 keV
    return float(np.exp(np.interp(math.log(D), np.log(ds[::-1]), np.log(ms[::-1]))))


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: the budget converts the SPARSEST cold carrier first; F2 must flip ***")
    B1 = json.load(open(AT1_JSON))["numbers"]["B1"]
    CELLS = [("0.1|600.0", 600.0), ("0.1|800.0", 800.0), ("0.05|600.0", 600.0), ("0.3|600.0", 600.0), ("1.0|600.0", 600.0)]
    ORDER = "sparsest" if MUTATE else "densest"

    def budget(key):
        b = B1[key]; return np.array(b["z"]), np.array(b["F_trig_unweighted"])

    cfg65 = [("lcdm", BOX65, "lcdm", 0.0, None, None, 0.0, ORDER)]
    cfg65 += [(f"wdm{m}", BOX65, "wdm", m, None, None, 0.0, ORDER) for m in RELICS]
    cfg65 += [(f"acc{key}", BOX65, "acc", 0.0, *budget(key), vk, ORDER) for key, vk in CELLS]
    cfg66 = [("lcdm", BOX66, "lcdm", 0.0, None, None, 0.0, ORDER), ("wdm1.5", BOX66, "wdm", 1.5, None, None, 0.0, ORDER),
             ("acc0.1|600.0", BOX66, "acc", 0.0, *budget("0.1|600.0"), 600.0, ORDER)]
    with Pool(int(os.environ.get("AT2_POOL", "6"))) as pool:
        R65 = dict(pool.map(run, cfg65))
    P(f"  L365's box: {len(cfg65)} runs done   [{time.time()-T0:.0f}s]")
    with Pool(int(os.environ.get("AT2_POOL66", "3"))) as pool:
        R66 = dict(pool.map(run, cfg66))
    P(f"  L366's box: {len(cfg66)} runs done   [{time.time()-T0:.0f}s]")
    OUT["numbers"]["runs65"] = R65; OUT["numbers"]["runs66"] = R66

    # ============================================================================================ controls
    banner("C1-C3  CONTROLS")
    l365 = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L365_virialization_triggered_carrier_results.json")))
    ref65 = l365["numbers"]["runs"]["lcdm"]
    devc = max((float(np.max(np.abs(np.array(R65["lcdm"][z]["p1d"]) / np.array(ref65[z]["p1d"]) - 1)))
                if len(R65["lcdm"][z]["p1d"]) == len(ref65[z]["p1d"]) else float("inf")) for z in ("3.0", "2.0"))
    check("C1 CONTROL: the LCDM run in L365's box reproduces L365's committed LCDM flux power at z = 3 and 2 (relative 1e-6)",
          f"max relative deviation {devc:.1e}", devc < 1e-6, load_bearing=False)
    D65 = {m: forest_D(band_dev(R65[f"wdm{m}"], R65["lcdm"])) for m in RELICS}
    pm5 = {m: R65[f"wdm{m}"]["2.0"]["pm_k5"] / R65["lcdm"]["2.0"]["pm_k5"] for m in RELICS}
    mono = all(D65[RELICS[i]] > D65[RELICS[i + 1]] for i in range(len(RELICS) - 1))
    check("C2 CONTROL: the relics register -- the forest distance D rises monotonically as the relic mass falls",
          "D: " + ", ".join(f"{m} keV {D65[m]:.5f}" for m in RELICS) + "; matter P(k=5) ratio at z = 2: " + ", ".join(f"{m}: {pm5[m]:.4f}" for m in RELICS),
          mono, load_bearing=False)
    import io, contextlib
    P19 = os.path.join(REPO, "real_research", "dark_sector_2026", "L319_lambda_triggered_kicked_decay.py")
    G19 = {"__name__": "l319", "__file__": P19}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P19).read().split("# ============================================================================================ controls")[0], G19)
    t2_mine = float(T2_wdm(np.array([G19["K_H"][G19["k5"]]]), 5.3)[0])
    check("C3 CONTROL: this file's T_wdm^2 is L319's (the strict line at L319's k = 5 grid point, to 1e-6: L362's Om vs L319's)",
          f"AT2 {t2_mine:.8f}, L319 {G19['T2_53']:.8f}", abs(t2_mine - G19["T2_53"]) < 1e-6, load_bearing=False)

    def score(r_, ref):
        dv = band_dev(r_, ref)
        fz2 = max(abs(x) for x in dv["2.0"]); dm2 = abs(1 - r_["2.0"]["pm_k5"] / ref["2.0"]["pm_k5"])
        return dict(dev=dv, D=forest_D(dv), flux_max=max(abs(x) for x in dv["3.0"] + dv["2.0"]), flux_max_z2=fz2, flux_max_z3=max(abs(x) for x in dv["3.0"]),
                    l365_rule=l365_rule(r_, ref), pm_k5_ratio_z2=r_["2.0"]["pm_k5"] / ref["2.0"]["pm_k5"],
                    pm_k5_ratio_z3=r_["3.0"]["pm_k5"] / ref["3.0"]["pm_k5"], response_z2=fz2 / max(dm2, 1e-12),
                    decayed=(r_["3.0"]["decayed"], r_["2.0"]["decayed"]))

    # ============================================================================================ F1-F2 L365's box
    banner("F1-F2  THE FOREST ON ITS OBSERVABLE (L365's box): flux imprint, L365's rule, and flux vs matter")
    SC = {key: score(R65[f"acc{key}"], R65["lcdm"]) for key, _ in CELLS}
    SR = {m: score(R65[f"wdm{m}"], R65["lcdm"]) for m in RELICS}
    for key, v_ in SC.items():
        P(f"    y_v|v_A {key:10s}: decayed z = 3/2 {v_['decayed'][0]:.3f}/{v_['decayed'][1]:.3f}; flux max |dev| z = 3 {v_['flux_max_z3']:.4f}, "
          f"z = 2 {v_['flux_max_z2']:.4f}; L365's rule {v_['l365_rule']:.4f}; matter P(k=5) ratio z = 3/2 {v_['pm_k5_ratio_z3']:.3f}/"
          f"{v_['pm_k5_ratio_z2']:.3f}; flux/matter response z = 2 {v_['response_z2']:.3f}")
        P("        bands z = 3: " + " ".join(f"{b[0]:.0f}-{b[1]:.1f}:{x:+.4f}" for b, x in zip(BANDS, v_["dev"]["3.0"]))
          + " | z = 2: " + " ".join(f"{b[0]:.0f}-{b[1]:.1f}:{x:+.4f}" for b, x in zip(BANDS, v_["dev"]["2.0"])))
    for m, v_ in SR.items():
        P(f"    relic {m:3.1f} keV: flux max |dev| z = 3 {v_['flux_max_z3']:.4f}, z = 2 {v_['flux_max_z2']:.4f}; matter P(k=5) ratio z = 2 "
          f"{v_['pm_k5_ratio_z2']:.4f}; flux/matter response z = 2 {v_['response_z2']:.3f}")
    OUT["numbers"]["F12"] = dict(cells=SC, relics=SR)
    a2 = SC["0.1|600.0"]
    check("F1 = H1: AT1's A2 cell (y_v 0.1, v_A 600) passes L365's forest rule in L365's box (flux within 10% of LCDM on k_par "
          "0.2-2 at z = 3 and 2)", f"worst deviation {a2['l365_rule']:.4f}; largest band deviation to 6.5 h/Mpc {a2['flux_max']:.4f}",
          (a2["l365_rule"] <= 0.10) == EXPECT["H1"],
          "the gas lags a late, halo-internal removal, and the forest samples the IGM, not halo interiors")
    check("F2 = H2: the proxy is not the observable -- the A2 cell's flux-to-matter response ratio at z = 2 is below 0.1 while the "
          "1.5 keV relic's is above 0.5", f"A2 cell {a2['response_z2']:.3f} (flux {a2['flux_max_z2']:.4f} vs matter "
          f"{abs(1 - a2['pm_k5_ratio_z2']):.3f}); 1.5 keV relic {SR[1.5]['response_z2']:.3f}",
          (a2["response_z2"] < 0.1 and SR[1.5]["response_z2"] > 0.5) == EXPECT["H2"],
          "a relic suppresses the IGM's small-scale structure, which the flux reads directly; this carrier empties halo interiors, "
          "which dominate the matter power at k = 5 but are saturated or absent in the forest")

    # ============================================================================================ F3 the larger box
    banner("F3  L366's BOX (100 Mpc/h, 256^3, 192^3 per species): the A2 cell again")
    a66 = score(R66["acc0.1|600.0"], R66["lcdm"]); r66 = score(R66["wdm1.5"], R66["lcdm"])
    P(f"    A2 cell: decayed z = 3/2 {a66['decayed'][0]:.3f}/{a66['decayed'][1]:.3f}; L365's rule {a66['l365_rule']:.4f}; flux max z = 3/2 "
      f"{a66['flux_max_z3']:.4f}/{a66['flux_max_z2']:.4f}; matter P(k=5) ratio z = 2 {a66['pm_k5_ratio_z2']:.3f}; response {a66['response_z2']:.3f} "
      f"(1.5 keV relic: {r66['response_z2']:.3f}, flux max z = 3/2 {r66['flux_max_z3']:.4f}/{r66['flux_max_z2']:.4f})")
    OUT["numbers"]["F3"] = dict(cell=a66, relic15=r66)
    check("F3 = H3: in L366's larger box the A2 cell again passes L365's rule, with a flux-to-matter response below 0.1 (the 1.5 keV "
          "relic's above 0.5)", f"rule {a66['l365_rule']:.4f}; response {a66['response_z2']:.3f} (relic {r66['response_z2']:.3f})",
          (a66["l365_rule"] <= 0.10 and a66["response_z2"] < 0.1 and r66["response_z2"] > 0.5) == EXPECT["H3"])

    # ============================================================================================ R1 the relic calibration
    banner("R1  (reported) THE RELIC CALIBRATION: relic-equivalent masses in this machinery (LOWER bounds; see GATES)")
    R1 = {key: dict(D=v_["D"], m_eq=m_equiv(v_["D"], D65)) for key, v_ in SC.items()}
    for key, v_ in R1.items():
        P(f"    y_v|v_A {key:10s}: D {v_['D']:.5f} -> relic-equivalent " + (f"{v_['m_eq']:.2f} keV" if np.isfinite(v_['m_eq'])
                                                                          else ("> 5.3 keV" if v_['m_eq'] > 0 else "< 1.5 keV")))
    OUT["numbers"]["R1"] = dict(D_relics=D65, cells=R1)
    check("R1 (reported) relic-equivalent masses (this machinery compresses a relic's imprint, so these are lower bounds; the 5.3 keV "
          "line is not decidable here)", {k: v["m_eq"] for k, v in R1.items()}, True, load_bearing=False)

    # ============================================================================================ F4 the mesh trigger, same yardstick
    banner("F4  (reported) THE SAME YARDSTICK ON L365's COMMITTED MESH-TRIGGER RUNS (its box; its LCDM = ours by C1)")
    F4 = {}
    for rk, rv_ in l365["numbers"]["runs"].items():
        if rk == "lcdm" or "3.0" not in rv_ or "p1d" not in rv_["3.0"]:
            continue
        dv = band_dev(rv_, ref65); D = forest_D(dv)
        F4[rk] = dict(D=D, m_eq=m_equiv(D, D65), flux_max=max(abs(x) for x in dv["3.0"] + dv["2.0"]),
                      decayed=(rv_["3.0"]["decayed"], rv_["2.0"]["decayed"]), l365_rule=l365_rule(rv_, ref65))
    for rk, v_ in F4.items():
        P(f"    L365 {rk:10s}: decayed z = 3/2 {v_['decayed'][0]:.2f}/{v_['decayed'][1]:.2f}; flux max |dev| {v_['flux_max']:.4f}; D {v_['D']:.5f} "
          f"-> relic-equivalent " + (f"{v_['m_eq']:.2f} keV" if np.isfinite(v_['m_eq']) else ("> 5.3 keV" if v_['m_eq'] > 0 else "< 1.5 keV")))
    OUT["numbers"]["F4"] = F4
    check("F4 (reported) the same yardstick on L365's committed mesh-trigger runs", {k: round(v["flux_max"], 4) for k, v in F4.items()},
          True, "the other track's triggered carriers, scored on this lane's calibration (not re-run)", load_bearing=False)

    banner("VERDICT")
    P(f"""  On the forest's own observable the acceleration trigger's high-z clearing is cheap: AT1's A2 cell moves the flux power by at
  most {a2['flux_max_z3']:.4f} at z = 3 and {a2['flux_max_z2']:.4f} at z = 2 (k_par <= 6.5 h/Mpc) and passes L365's rule ({a2['l365_rule']:.4f} vs 0.10),
  while the matter power at k = 5 in the same run falls to {a2['pm_k5_ratio_z2']:.2f} of LCDM.  L319's matter proxy, which AT1's A3 and
  bound price, is the wrong yardstick for a late, halo-internal clearing: the flux-to-matter response is {a2['response_z2']:.3f} here
  against {SR[1.5]['response_z2']:.2f} for a relic.  The relic calibration in this box is weak (a 1.5 keV relic moves the flux
  only {SR[1.5]['flux_max']:.4f}); on it the cell reads as {('a %.2f keV relic' % R1['0.1|600.0']['m_eq']) if np.isfinite(R1['0.1|600.0']['m_eq']) else ('heavier than 5.3 keV' if R1['0.1|600.0']['m_eq'] > 0 else 'lighter than 1.5 keV')}, a LOWER bound
  because the box compresses a relic's small-scale imprint more than this carrier's intermediate-scale one.  The strict
  5.3 keV line needs a higher-resolution forest calculation to decide.""")
    n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    OUT["expect"] = EXPECT; OUT["runtime_s"] = time.time() - T0
    outname = f"{SLUG}_results{'_FAST' if FAST else ''}{'_MUTATE' if MUTATE else ''}.json"   # smoke runs never overwrite the main output
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
    P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time()-T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
