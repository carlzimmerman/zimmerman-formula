#!/usr/bin/env python3
"""CFG639 Part A (FROZEN_CRITERIA.md, dbe89ed33): the deficit-gated mobility HG on CFG544's galaxy bench.

CFG544's spherical N-body toy is imported read-only and run unchanged (FIX-2: two-sided deficit + OU to the instantaneous
isotropic Jeans dispersion, alpha = 1), except that the drift and the OU update act only on particles whose radial bin has
d = rho_ph - rho_c > 0 (gate G).  Modes: 'gate' (HG), 'none' (G = 1, control A-C1), 'inv' (G = 1 where d < 0, tooth A-M1).
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not "theory closed".
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg639_galaxy.py   (2 processes, < 1 GB each)
"""
import os, sys, json, math
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG544_settling_kinetic_consistency"))
import cfg544 as T544  # noqa: E402  (read-only)

R544 = json.load(open(os.path.join(HERE, "..", "CFG544_settling_kinetic_consistency", "cfg544_results.json")))
OUT = []


def log(s=""):
    print(s, flush=True); OUT.append(str(s))


def gated_class(mode):
    Base = T544.Toy

    class GatedToy(Base):
        n_off = 0; n_in = 0

        def _gate_bins(self, r):
            mc = self.m * np.histogram(r, self.rf)[0]
            d = self.rhoph - mc / self.V
            if mode == "gate":
                return d > 0
            if mode == "inv":
                return d < 0
            return np.ones(d.size, bool)

        # CFG544 drift_step with the gate on the mobility (identical arithmetic when the gate is all True)
        def drift_step(self, r, dt, g):
            c = self.c
            inside = r < c["rta"]
            mc = self.m * np.histogram(r, self.rf)[0]
            rho = mc / self.V
            d = (self.rhoph - rho) if self.rule == "two" else np.maximum(self.rhoph - rho, 0.0)
            Md = np.concatenate([[0.0], np.cumsum(d * self.V)])
            k = np.clip(np.searchsorted(self.rf, r) - 1, 0, T544.NB - 1)
            gk = self._gate_bins(r)[k]
            type(self).n_in += int(inside.sum()); type(self).n_off += int((inside & ~gk).sum())
            dpsi = np.interp(r, self.rf, Md) / r ** 2
            tau = 1.0 / np.sqrt(4 * math.pi * (self.rhob + rho))[k]
            vs = np.where(inside & gk, -T544.ALPHA * tau * dpsi, 0.0)
            dx = vs * dt; lim = 0.5 * self.dr[k]
            over = np.abs(dx) > lim
            self.n_lim += int((over & inside).sum()); self.n_mv += int(inside.sum())
            dx = np.clip(dx, -lim, lim)
            rn = r + dx
            rn = np.where(rn < T544.RMIN, 2 * T544.RMIN - rn, rn)
            work = self.m * np.sum(g * (rn - r))
            return rn, work

        # CFG544 ou_step with the gate (identical arithmetic and RNG draws when the gate is all True)
        def ou_step(self, r, vr, vt, dt, g, rng):
            c = self.c
            mc = self.m * np.histogram(r, self.rf)[0]; rho = mc / self.V
            Menc_c = T544.Mb_enc(c, self.rc) + np.concatenate([[0.0], np.cumsum(mc)[:-1]]) + 0.5 * mc
            gb = Menc_c * self.rc / (self.rc ** 2 + T544.EPS ** 2) ** 1.5
            fP = rho * gb * self.dr
            Pf = np.concatenate([np.cumsum(fP[::-1])[::-1], [0.0]])
            Pc = 0.5 * (Pf[1:] + Pf[:-1])
            s2J = np.where(rho > 0, Pc / np.maximum(rho, 1e-300), 0.0) * self.ou_scale
            k = np.clip(np.searchsorted(self.rf, r) - 1, 0, T544.NB - 1)
            inside = (r < c["rta"]) & self._gate_bins(r)[k]
            gam = T544.ALPHA * np.sqrt(4 * math.pi * (self.rhob + rho))[k]
            a = np.exp(-gam * dt); b = np.sqrt(s2J[k] * (1 - a ** 2))
            K0 = 0.5 * self.m * np.sum(vr ** 2 + vt ** 2)
            x1, x2, x3 = rng.standard_normal((3, r.size))
            vr_n = np.where(inside, a * vr + b * x1, vr)
            vtx = a * vt + b * x2; vty = b * x3
            vt_n = np.where(inside, np.hypot(vtx, vty), vt)
            K1 = 0.5 * self.m * np.sum(vr_n ** 2 + vt_n ** 2)
            return vr_n, vt_n, K1 - K0

    return GatedToy


def work(job):
    cls = gated_class(job["gate"])
    T544.Toy = cls
    res = T544.run(job)
    res["gate_mode"] = job["gate"]
    res["gated_off_frac"] = cls.n_off / max(cls.n_in, 1)
    res.pop("series", None) if job.get("drop_series") else None
    return res


def main():
    cells = {f"{s}_{f}": T544.make_cell(s, f) for s in T544.SYS for f in T544.FOOT}
    log("CFG639 Part A: deficit-gated mobility on CFG544's bench (FIX-2 + gate G = 1[d > 0])")
    jobs = []
    for k, c in cells.items():
        jobs += [dict(c=c, name=f"{k}|gate_B", ic="B", rule="two", ou=True, T=10.0, gate="gate"),
                 dict(c=c, name=f"{k}|gate_C", ic="C", rule="two", ou=True, T=5.0, gate="gate")]
    c0 = cells["MW_can"]
    jobs += [dict(c=c0, name="MW_can|C1_none_C", ic="C", rule="two", ou=True, T=5.0, gate="none"),
             dict(c=c0, name="MW_can|M1_inv_C", ic="C", rule="two", ou=True, T=5.0, gate="inv")]
    jobs.sort(key=lambda j: -j["T"] / j["c"]["dt"] / j["c"]["tu_Gyr"])
    with Pool(2) as pool:
        out = pool.map(work, jobs, chunksize=1)
    runs = {o["name"]: o for o in out}

    log("\nRuns (end state; shell 0.1-0.9 r_*):")
    for nm in sorted(runs):
        o = runs[nm]; f = o["final"]
        log(f"  {nm:22s} t {o['T_Gyr']:4.1f}  logX {f['logX']:+.4f}  D {f['D']:+.4f}  last2 {o['d_logX_last2']:+.3f}/{o['d_D_last2']:+.3f}"
            f"  M(<r*)/Mph {f['Mc_in_rstar_over_Mph']:.3f}  excess {f['excess_in_rstar']:+.4f}  r99 {f['r99']:.3f}  beta {f['beta']:+.2f}"
            f"  sink {f['sink_cum_over_Vf2Mcat']:+.3f}  gated_off {o['gated_off_frac']:.3f}  G550 {o['gate']}  ({o['wall_s']:.0f}s)")

    # A-C1: G = 1 reproduces CFG544 MW_can|fix2_C exactly
    ref = R544["runs"]["MW_can|fix2_C"]["final"]; cc = runs["MW_can|C1_none_C"]["final"]
    c1 = dict(dlogX=cc["logX"] - ref["logX"], dD=cc["D"] - ref["D"])
    c1_ok = c1["dlogX"] == 0 and c1["dD"] == 0
    # A-M1: inverted gate changes the MW_can IC-C end state by |dD| > 0.02 vs the gated run
    m1 = runs["MW_can|M1_inv_C"]["final"]["D"] - runs["MW_can|gate_C"]["final"]["D"]
    m1_ok = abs(m1) > 0.02
    g550 = {k: dict(B=runs[f"{k}|gate_B"]["gate"], C=runs[f"{k}|gate_C"]["gate"]) for k in cells}
    allpass = all(v["B"] and v["C"] for v in g550.values())
    if not c1_ok:
        label = "VOID (control A-C1 fails)"
    elif not m1_ok:
        label = "NOT DIAGNOSTIC (tooth A-M1: the gate does not act)"
    else:
        label = "A-PASS" if allpass else "A-FAIL: " + ", ".join(f"{k}|{ic}" for k, v in g550.items() for ic in "BC" if not v[ic])
    log(f"\nA-C1 (G = 1 vs CFG544 fix2_C, MW_can): dlogX {c1['dlogX']:+.3e}  dD {c1['dD']:+.3e} -> {'PASS' if c1_ok else 'FAIL'}")
    log(f"A-M1 (inverted gate, MW_can IC-C): dD vs gated {m1:+.4f} -> {'bites' if m1_ok else 'DOES NOT BITE'}")
    log(f"G550 per cell: {g550}")
    log(f"\nPART A LABEL: {label}")
    res = dict(lane="CFG639", part="A", criteria="dbe89ed33", A_C1=dict(**c1, pass_=c1_ok), A_M1=dict(dD=m1, bites=m1_ok),
               G550=g550, label=label, runs={k: {kk: vv for kk, vv in v.items() if kk != "series"} | {"series": v.get("series")}
                                              for k, v in runs.items()})
    json.dump(res, open(os.path.join(HERE, "cfg639_galaxy_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg639_galaxy.out"), "w").write("\n".join(OUT) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
