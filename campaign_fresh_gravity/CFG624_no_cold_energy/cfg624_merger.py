#!/usr/bin/env python3
"""CFG624 G3 (FROZEN_CRITERIA.md 803cef306): the Bullet Cluster with NO COLD ENERGY.
CFG621's merger machinery (cfg621_sim.py -> CFG599/CFG597, imported read-only) in its alpha = inf mode: no cold-energy particles; the
dark field that gravitates and lenses is the round law-phantom of the CURRENT baryons, per progenitor, no EFE.  The ONE NCE change:
the phantom is NOT truncated at the progenitor's r_t (no supply edge; the law's phantom of the baryons out to the profile grid, 4000 kpc).
Cell = CFG621's calibrated merger cell (runs_B/ainf_*_v2666.7_eta1.132.json cfg), both footings; scored with cfg621_main.score_run.
M-G3 control: the same code path with the r_t truncation KEPT must reproduce CFG621's cached alpha = inf canonical cell (f, Z_B) to 1e-9.
Run from the repository root (single thread, nice 10, ~10 min per run):
  nice -n 10 python3 campaign_fresh_gravity/CFG624_no_cold_energy/cfg624_merger.py
kappa = 1/2 FITTED; footings never pooled; no particle species; not theory closed."""
import os, sys
os.environ["OMP_NUM_THREADS"] = "1"
import json, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
D621 = os.path.join(LANES, "CFG621_merger_stopwatch_v3")
sys.path.insert(0, D621)
import cfg621_sim as S621          # noqa: E402  (read-only; puts CFG599 on sys.path)
import cfg599_sim as S599          # noqa: E402
import cfg599_lib as L             # noqa: E402
import cfg621_main as M621         # noqa: E402  (read-only: score_run, T_L)
WORK = os.path.join(REPO, "..", "_external_data", "cfg624_work", "merger"); os.makedirs(WORK, exist_ok=True)
try:
    os.nice(10)
except OSError:
    pass
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


ORIG = S621.Sim


class SimNCE(ORIG):
    """phantom_field of CFG599 copied verbatim except: no truncation at p.rt (NCE: the law's phantom has no supply edge)."""
    def phantom_field(self):
        g = self.g
        gm = self.gas_masses()
        X, Y, Z = g.xc
        out = np.zeros(g.n)
        for k, p in enumerate(self.progs):
            sel = self.is_bp & (self.tag == k)
            xs, ms = self.x[sel], self.m[sel]
            c = self.xb[k].copy()
            for _ in range(3):                                   # centroiding inside r_t as CFG599 (a centre, not a truncation)
                r = g.radius_from(c)
                wg = gm[k] * (r < p.rt)
                Mc = wg.sum()
                cg = np.array([(wg.sum((1, 2)) * X).sum(), (wg.sum((0, 2)) * Y).sum(), (wg.sum((0, 1)) * Z).sum()])
                ds = np.linalg.norm(xs - c, axis=1) < p.rt
                Mc += ms[ds].sum(); cg += (ms[ds, None] * xs[ds]).sum(0)
                c = cg / Mc if Mc > 0 else c
            self.xb[k] = c
            r = g.radius_from(c)
            hb = np.histogram(r.ravel(), S599.RB, weights=gm[k].ravel())[0]
            hb += np.histogram(np.linalg.norm(xs - c, axis=1), S599.RB, weights=ms)[0]
            Mcum = np.concatenate([[0.0], np.cumsum(hb)])
            rho_ph, Mt = L.phantom_profile_from_mass(S599.RB, Mcum, self.a0, 1.0e12)      # CFG624: rt -> infinity
            f = np.interp(r, S599.RBC, rho_ph, right=0.0)                                   # CFG624: no (r < p.rt) cut
            s = f.sum() * g.dV
            if s > 0:
                f *= min(Mt, s) / s                              # keep the grid's own phantom mass (no renormalisation upward)
            out += f
        return out


def run_cell(cfg, nce, tag):
    fn = os.path.join(WORK, f"{tag}.json")
    if os.path.exists(fn):
        return json.load(open(fn))
    cfg = {k: (math.inf if v == "inf" else v) for k, v in cfg.items()}       # CFG621 worker(): alpha inf, v0 from v0_kms
    cfg["v0"] = cfg["v0_kms"] * L.KMS
    S621.Sim = SimNCE if nce else ORIG
    try:
        r = S621.run(cfg)
    finally:
        S621.Sim = ORIG
    json.dump(M621._round(r) if hasattr(M621, "_round") else r, open(fn, "w"))
    return json.load(open(fn))


P(__doc__.split("Run from")[0].strip())
RES = {"lane": "CFG624", "script": "cfg624_merger", "criteria": "803cef306", "T_L": M621.T_L, "cells": {}}
cached = {f: json.load(open(os.path.join(D621, "runs_B", f"ainf_{f}_v2666.7_eta1.132.json"))) for f in ("can", "alt")}
t0 = time.time()
# M-G3 control first: edge kept -> must reproduce the cached CFG621 alpha = inf canonical cell
ctl = run_cell(cached["can"]["cfg"], nce=False, tag="control_edge_kept_can")
sc_ctl, sc_cache = M621.score_run(ctl), M621.score_run(cached["can"])
ok = all(abs(sc_ctl.get(k, 0) - sc_cache.get(k, 0)) <= 1e-9 for k in ("f", "Z_B")) and sc_ctl.get("scorable_B") == sc_cache.get("scorable_B")
P(f"  [{'PASS' if ok else 'FAIL'}] M-G3 edge-kept code path reproduces CFG621 alpha = inf (can): f {sc_ctl.get('f')} vs {sc_cache.get('f')}; "
  f"Z_B {sc_ctl.get('Z_B')} vs {sc_cache.get('Z_B')} ({time.time() - t0:.0f} s)")
RES["M_G3"] = dict(ok=bool(ok), control=sc_ctl, cfg621_cached=sc_cache)
for f in ("can", "alt"):
    r = run_cell(cached[f]["cfg"], nce=True, tag=f"nce_{f}")
    sc = M621.score_run(r)
    RES["cells"][f] = dict(score=sc, cfg621_alpha_inf=M621.score_run(cached[f]), Mph_tot=r.get("Mph_tot"), Mb=r.get("Mb"), wall_s=r.get("wall_s"))
    P(f"  NCE [{f}]: scorable_B {sc.get('scorable_B')}, f {sc.get('f')}, Z_B {sc.get('Z_B')}, lens spread {sc.get('lens_spread_obs')}, "
      f"Harvey scorable {sc.get('scorable_H')} beta_bar {sc.get('beta_bar', sc.get('beta_bar_reported'))} Z_H {sc.get('Z_H')}, status {sc.get('status')}; "
      f"CFG621 alpha = inf (edge): f {RES['cells'][f]['cfg621_alpha_inf'].get('f')}, Z_B {RES['cells'][f]['cfg621_alpha_inf'].get('Z_B')}")
cl = [RES["cells"][f]["score"] for f in ("can", "alt")]
if all(c.get("scorable_B") and c["Z_B"] >= 3 for c in cl):
    v = "EXCLUDED"
elif all(c.get("scorable_B") and c.get("scorable_H") and abs(c["Z_B"]) < 2 and abs(c["Z_H"]) < 2 for c in cl):
    v = "PASS"
else:
    v = "UNDETERMINED"
RES["verdict"] = v if ok else f"{v} (CONTROL M-G3 FAILED)"
P(f"  G3 verdict: {RES['verdict']}  ({time.time() - t0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "cfg624_merger_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg624_merger.out"), "w").write("\n".join(LOG) + "\n")
