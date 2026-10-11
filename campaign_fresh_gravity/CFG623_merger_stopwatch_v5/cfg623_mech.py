#!/usr/bin/env python3
"""CFG623 step 1: controls-only MECHANISM test of CFG622 disclosure D-2 (a diagnostic, NOT a verdict input).

Hypothesis H (CFG622 D-2): at alpha = 0 the sub's cold energy is cored on the lensing map, so just after pericentre the dense
cool-core gas cloud (CFG599 M-3b: 15% of the sub's gas, Plummer a = 50 kpc) sets the sub's lensing peak until d_SG grows past
about 200 kpc; that is why the Harvey beta is 0.4-0.95 for t - t_peri < 0.2 Gyr.

Runs (alpha = 0 only, canonical footing, seed 600 = a CFG622 control seed, never the seed-599 alpha grid; CFG621's v0, eta;
CFG622 simulator and masked estimator E-M imported read-only):
  BASE  the unmodified model, with extra decomposition peaks (the physics is identical to CFG622's seed-600 control);
  NC    cool-core cloud removed, its mass returned to the smooth grid gas of the sub (total baryons conserved);
  CUSP  the sub's cold energy drawn from a cuspier profile: NFW with c = 10 (r_s = r200/10) truncated at r_t, same total mass
        (gas pressure and Jeans velocities recomputed for the new total mass; the cloud is kept).
Every run records, besides CFG622's diagnostics, the sub's primary (300, 75) E-M lensing peak on three decomposed maps:
  lens_nocloud  total minus the sub's cloud particles;  lens_nogas  total minus all of the sub's gas (cloud + grid);
  cold          cold energy only (already in CFG622).
Declared reading (written before the runs):
  P1 (BASE): for t - t_peri in [0.1, 0.2) Gyr, beta on the total map >= 0.3 (reproduces D-2) while beta on lens_nocloud <= 0.15.
  P2 (NC):   beta-bar over [0.1, 0.2) Gyr <= 0.15 (no cloud -> no early gas-set peak).
  P3 (CUSP): beta-bar over [0.1, 0.2) Gyr below BASE (reported; a 50-kpc PM grid limits how cuspy the core can stay).
  H CONFIRMED iff P1 and P2 hold; NOT CONFIRMED iff either fails; P3 reported only.
POST HOC (added after the runs, reported only, changes no reading above): the same means in kpc, i.e. the lensing-peak offset
from the galaxies projected on the galaxy->gas direction (beta x d_SG), because NC and CUSP change d_SG itself.
kappa = 1/2 is fitted; the cold energy's mass is required (an input); no particle species; yardsticks raw data only.
Run: nice -n 10 python3 cfg623_mech.py   -> runs_mech/, cfg623_mech.out, cfg623_mech_results.json"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import sys, json, math, time
import multiprocessing as mp
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG622_merger_stopwatch_v4"))
import cfg622_sim as S622   # noqa: E402 (read-only; puts CFG621 and CFG599 on sys.path)
import cfg599_lib as L      # noqa: E402
import cfg599_sim as S599   # noqa: E402

RUNS = os.path.join(HERE, "runs_mech"); os.makedirs(RUNS, exist_ok=True)
C621 = os.path.join(HERE, "..", "CFG621_merger_stopwatch_v3")
CAL = json.load(open(os.path.join(C621, "cfg621_results.json")))["calibration"]
BASE = dict(alpha=0.0, foot="can", seed=600, v0_kms=float(round(CAL["v0_kms"], 1)), eta=float(f"{CAL['eta']:.4g}"))
VARIANTS = ["BASE", "NC", "CUSP"]
C_CUSP = 10.0
_ORIG = L.Progenitor599


def make_prog(variant):
    def prog(M200, foot, swap=False, cloud=False, **kw):
        if variant == "NC":
            return _ORIG(M200, foot, swap=swap, cloud=False, **kw)
        p = _ORIG(M200, foot, swap=swap, cloud=cloud, **kw)
        if variant == "CUSP" and cloud:
            r = p.r; rs = p.r200 / C_CUSP
            nfw = np.where(r < p.rt, 1.0 / (np.maximum(r, 1e-3) / rs * (1 + r / rs) ** 2), 0.0)
            Mn = L.cumtrapz_sph(r, nfw)
            Mph = p.Mph_tot * Mn / np.interp(p.rt, r, Mn)
            p.Mph = np.where(r < p.rt, Mph, p.Mph_tot)
            p.rho_ph = np.gradient(p.Mph, r) / (4 * math.pi * np.maximum(r, 1e-3) ** 2); p.rho_ph[r >= p.rt] = 0.0
            p.Mtot = p.Mbar + p.Mph
            gN = L.G * p.Mtot / np.maximum(r, 1e-3) ** 2
            f = p.rho_g * gN; P = np.zeros_like(r)
            P[-1] = p.rho_g[-1] * 0.5 * L.G * p.Mtot[-1] / r[-1]
            for k in range(len(r) - 2, -1, -1):
                P[k] = P[k + 1] + 0.5 * (f[k] + f[k + 1]) * (r[k + 1] - r[k])
            p.P = P
        return p
    return prog


class MechSim(S622.Sim):
    def __init__(self, cfg):
        L.Progenitor599 = make_prog(cfg["mech"])
        try:
            super().__init__(cfg)
        finally:
            L.Progenitor599 = _ORIG

    def diagnose(self, alts=True):
        rec = super().diagnose(alts=alts)
        if len(self.names) != 2:
            return rec
        XX, YY = self.XX, self.YY
        gas_k, st_k, tot, cold = self.maps()
        gal = np.array(rec["sub"]["gal"]); go = np.array(rec["main"]["gal"]); u = gal - go
        mask = ((XX - 0.5 * (gal[0] + go[0])) * u[0] + (YY - 0.5 * (gal[1] + go[1])) * u[1]) >= 0.0
        cloud = self.dep2(self.is_g & (self.tag == 1)) if self.is_g.any() else 0.0 * tot
        pk = lambda S: L.shrink_peak(XX, YY, S * mask, gal, R0=S622.R0, Rmin=S622.RMIN)[0].tolist()
        rec["sub"]["lens_nocloud"] = pk(tot - cloud)
        rec["sub"]["lens_nogas"] = pk(tot - gas_k[1])
        r = np.hypot(XX - gal[0], YY - gal[1])
        rec["sub"]["Sig75"] = dict(tot=float(tot[r < 75].mean()), cloud=float(np.asarray(cloud)[r < 75].mean()) if np.ndim(cloud) else 0.0,
                                   cold=float(cold[r < 75].mean()), gas=float(gas_k[1][r < 75].mean()))
        return rec


def run(cfg):
    """CFG622 run() verbatim except that it builds MechSim."""
    T0 = time.time()
    s = MechSim(cfg)
    next_diag = 0.0; t_peri = None
    s.diagnose(); next_diag += S622.DIAG_EVERY
    while True:
        vmax = np.abs(s.v).max()
        dt = min(L.hydro_dt(s.U, s.g.dx), 0.3 * s.g.dx / vmax, 0.005, next_diag - s.t + 1e-9)
        dt = max(dt, 1e-5)
        s.step(dt)
        if s.t >= next_diag - 1e-9:
            s.diagnose(); next_diag += S622.DIAG_EVERY
            if t_peri is None and len(s.diag) > 1:
                d1 = s.diag[-2]; d2 = s.diag[-1]
                s1 = d1["sub"]["gal"][0] - d1["main"]["gal"][0]; s2 = d2["sub"]["gal"][0] - d2["main"]["gal"][0]
                if s1 > 0 >= s2:
                    t_peri = d1["t"] + (d2["t"] - d1["t"]) * s1 / (s1 - s2)
            if t_peri is not None and s.t >= t_peri + cfg.get("t_after", 0.8):
                break
            if s.t >= cfg.get("t_max", 3.0):
                break
    return dict(cfg=S622._clean(cfg), t_peri=t_peri, wall_s=time.time() - T0, Mph_tot=[p.Mph_tot for p in s.progs],
                Mcc=[p.Mcc for p in s.progs], diag=s.diag)


def _round(o):
    if isinstance(o, float):
        return round(o, 4)
    if isinstance(o, list):
        return [_round(x) for x in o]
    if isinstance(o, dict):
        return {k: _round(v) for k, v in o.items()}
    return o


def worker(v):
    fn = os.path.join(RUNS, f"mech_{v}.json")
    if os.path.exists(fn):
        return
    c = dict(BASE, mech=v); c["v0"] = c["v0_kms"] * L.KMS
    json.dump(_round(run(c)), open(fn + ".tmp", "w")); os.replace(fn + ".tmp", fn)


def beta(d, key):
    s = d["sub"]; gal, gas, x = np.array(s["gal"]), np.array(s["gas"]), np.array(s[key])
    e = gas - gal; n = np.linalg.norm(e)
    return (float(np.dot(x - gal, e) / n ** 2) if n > 0 else float("nan")), float(n)


def main():
    todo = [v for v in VARIANTS if not os.path.exists(os.path.join(RUNS, f"mech_{v}.json"))]
    if todo:
        with mp.get_context("fork").Pool(min(3, len(todo))) as pool:
            pool.map(worker, todo, chunksize=1)
    OUT, RES = [], {"lane": "CFG623", "step": "mechanism test (diagnostic only)", "config": BASE, "c_cusp": C_CUSP}
    P = lambda s="": (print(s, flush=True), OUT.append(s))
    P("CFG623 MECHANISM TEST (controls only, alpha = 0, canonical, seed 600; diagnostic, not a verdict input)")
    P("kappa = 1/2 FITTED; cold energy's mass required; no particle species.")
    keys = ["lens", "lens_nocloud", "lens_nogas", "cold"]
    for v in VARIANTS:
        r = json.load(open(os.path.join(RUNS, f"mech_{v}.json"))); tp = r["t_peri"]
        rows = []
        for d in r["diag"]:
            ta = d["t"] - tp
            if -1e-9 <= ta <= 0.6 + 1e-9:
                b = {k: beta(d, k)[0] for k in keys}; dsg = beta(d, "lens")[1]
                rows.append(dict(t_after=round(ta, 3), dSG=dsg, **{f"beta_{k}": b[k] for k in keys}, Sig75=d["sub"].get("Sig75")))
        def mean(k, lo, hi):
            xs = [x[f"beta_{k}"] for x in rows if lo - 1e-9 <= x["t_after"] < hi - 1e-9 and x["dSG"] >= 50]
            return float(np.mean(xs)) if xs else None
        summ = {f"{k}_{lo}_{hi}": mean(k, lo, hi) for k in keys for lo, hi in ((0.1, 0.2), (0.2, 0.6 + 1e-6), (0.1, 0.6 + 1e-6))}
        def mean_kpc(k, lo, hi):
            xs = [x[f"beta_{k}"] * x["dSG"] for x in rows if lo - 1e-9 <= x["t_after"] < hi - 1e-9 and x["dSG"] >= 50]
            return float(np.mean(xs)) if xs else None
        summ_kpc = {f"{k}_{lo}_{hi}": mean_kpc(k, lo, hi) for k in keys for lo, hi in ((0.1, 0.2), (0.2, 0.6 + 1e-6))}
        dsg_at = {str(t): float(np.interp(t, [x["t_after"] for x in rows], [x["dSG"] for x in rows])) for t in (0.1, 0.15, 0.2, 0.3, 0.4, 0.6)}
        ep = S622.epoch(r["diag"], tp)
        RES[v] = dict(t_peri=tp, summary=summ, posthoc_offset_kpc=summ_kpc, dSG_at_t_after=dsg_at, epoch720=ep and dict(v_kms=ep["v_obs_kms"], dSG=ep["dSG_obs"]),
                      rows=rows)
        P(f"\n{v}: t_peri {tp:.4f}; d_SG at t-t_peri 0.1/0.15/0.2/0.3/0.6: " + " / ".join(f"{dsg_at[k]:.0f}" for k in ("0.1", "0.15", "0.2", "0.3", "0.6"))
          + (f"; 720-kpc epoch speed {ep['v_obs_kms']:.0f} km/s, d_SG {ep['dSG_obs']:.0f} kpc" if ep else ""))
        for k in keys:
            P(f"  beta-bar {k:13s}: [0.1,0.2) {summ[f'{k}_0.1_0.2']:+.3f}   [0.2,0.6] {summ[f'{k}_0.2_0.600001']:+.3f}   [0.1,0.6] {summ[f'{k}_0.1_0.600001']:+.3f}"
              f"   | post hoc offset along gas [0.1,0.2) {summ_kpc[f'{k}_0.1_0.2']:+6.1f} kpc, [0.2,0.6] {summ_kpc[f'{k}_0.2_0.600001']:+6.1f} kpc")
        early = [x for x in rows if 0.1 - 1e-9 <= x["t_after"] < 0.2 - 1e-9 and x["Sig75"]]
        if early:
            P("  mean surface density within 75 kpc of the sub galaxies, t-t_peri in [0.1,0.2) (Msun/kpc^2): " +
              ", ".join(f"{k} {np.mean([x['Sig75'][k] for x in early]):.3g}" for k in ("tot", "cloud", "gas", "cold")))
    b, n, c = RES["BASE"]["summary"], RES["NC"]["summary"], RES["CUSP"]["summary"]
    p1 = b["lens_0.1_0.2"] >= 0.3 and b["lens_nocloud_0.1_0.2"] <= 0.15
    p2 = n["lens_0.1_0.2"] <= 0.15
    p3 = c["lens_0.1_0.2"] < b["lens_0.1_0.2"]
    RES["P1"], RES["P2"], RES["P3_reported"] = bool(p1), bool(p2), bool(p3)
    RES["H"] = "CONFIRMED" if (p1 and p2) else "NOT CONFIRMED"
    P(f"\nP1 (BASE total >= 0.3 and no-cloud <= 0.15 over [0.1,0.2)): {b['lens_0.1_0.2']:+.3f} / {b['lens_nocloud_0.1_0.2']:+.3f} -> {'HOLDS' if p1 else 'FAILS'}")
    P(f"P2 (NC beta-bar [0.1,0.2) <= 0.15): {n['lens_0.1_0.2']:+.3f} -> {'HOLDS' if p2 else 'FAILS'}")
    P(f"P3 (CUSP below BASE over [0.1,0.2), reported): {c['lens_0.1_0.2']:+.3f} vs {b['lens_0.1_0.2']:+.3f} -> {'yes' if p3 else 'no'}")
    P(f"HYPOTHESIS H (cool-core cloud sets the early alpha = 0 lensing peak): {RES['H']}")
    open(os.path.join(HERE, "cfg623_mech.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(RES, open(os.path.join(HERE, "cfg623_mech_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
