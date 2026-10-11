#!/usr/bin/env python3
"""CFG622 simulator: CFG621's simulator (../CFG621_merger_stopwatch_v3/cfg621_sim.py, itself CFG599's model) imported read-only,
with ONLY the diagnostic changed (FROZEN_CRITERIA.md B-1): the sub's lensing and cold-energy peaks are found on maps masked to
the sub's side of the perpendicular bisector of the sub-main galaxy-peak segment (main: the complementary side).  Galaxy and gas
peaks are CFG621's E-1, unchanged.  Also recorded: signed distances of every masked lensing peak and of the sub's gas peak from
the bisector (edge and gas guards, B-3) and the unmasked CFG621 primary and spread (reported only).
kappa = 1/2 is fitted; the cold energy's mass is required (an input); no particle species."""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG621_merger_stopwatch_v3"))
import cfg621_sim as S621   # noqa: E402  (read-only; puts CFG599 on sys.path)
import cfg599_lib as L      # noqa: E402

R0, RMIN = S621.R0, S621.RMIN
LENS_ALTS = S621.LENS_ALTS
DIAG_EVERY = S621.DIAG_EVERY
PX = S621.PX
epoch = S621.epoch
_clean = S621._clean


def side(p, g_self, g_other):
    """signed distance of p from the bisector of (g_self, g_other); > 0 on g_self's side."""
    u = np.asarray(g_self) - np.asarray(g_other); n = np.linalg.norm(u)
    if n <= 0:
        return np.inf
    return float(np.dot(np.asarray(p) - 0.5 * (np.asarray(g_self) + np.asarray(g_other)), u / n))


class Sim(S621.Sim):
    def diagnose(self, alts=True):
        XX, YY = self.XX, self.YY
        gas_k, st_k, tot, cold = self.maps()
        rec = {"t": self.t}
        pk = lambda S, st, a=R0, b=RMIN: L.shrink_peak(XX, YY, S, st, R0=a, Rmin=b)
        gals, okgs = [], []
        for k in range(len(self.names)):
            sel = self.is_s & (self.tag == k)
            g, ok = pk(st_k[k], np.median(self.x[sel, :2], axis=0)); gals.append(g); okgs.append(ok)
        two = len(self.names) == 2
        for k, nm in enumerate(self.names):
            sel = self.is_s & (self.tag == k)
            gal, okg = gals[k], okgs[k]
            if two:
                go = gals[1 - k]
                u = gal - go
                mask = ((XX - 0.5 * (gal[0] + go[0])) * u[0] + (YY - 0.5 * (gal[1] + go[1])) * u[1]) >= 0.0
                totm, coldm = tot * mask, cold * mask
            else:
                go = None; totm, coldm = tot, cold
            gs = L.massweighted_start(XX, YY, gas_k[k], gal, 600.0)
            gas, oks = pk(gas_k[k], gs)
            lens, okl = pk(totm, gal)
            cpk, _ = pk(coldm, gal) if coldm.sum() > 0 else (gal, True)
            r = dict(gal=gal.tolist(), gas=gas.tolist(), lens=lens.tolist(), cold=cpk.tolist(), conv=[bool(okg), bool(oks), bool(okl)])
            if two:
                r["gas_edge"] = side(gas, gal, go); r["lens_edge"] = side(lens, gal, go)
            if alts and (nm == "sub" or not two):
                la = [pk(totm, gal, a, b)[0] for a, b in LENS_ALTS]
                r["lens_alts"] = [x.tolist() for x in la]
                r["lens_spread"] = float(max(np.hypot(*(x - lens)) for x in la))
                if two:
                    r["alts_edge"] = [side(x, gal, go) for x in la]
                    l0, _ = pk(tot, gal)
                    la0 = [pk(tot, gal, a, b)[0] for a, b in LENS_ALTS]
                    r["lens_nomask"] = l0.tolist()
                    r["lens_spread_nomask"] = float(max(np.hypot(*(x - l0)) for x in la0))
            vg = self.v[sel & (np.linalg.norm(self.x[:, :2] - gal, axis=1) < 200.0)]
            r["vgal"] = vg.mean(0).tolist() if len(vg) else [0, 0, 0]
            r["M300"] = float(tot[((XX - gal[0]) ** 2 + (YY - gal[1]) ** 2) < 300.0 ** 2].sum() * PX ** 2)
            if self.is_g.any() and nm == "sub":
                cg = self.is_g & (self.tag == k)
                r["cloud_com"] = ((self.m[cg, None] * self.x[cg, :2]).sum(0) / self.m[cg].sum()).tolist()
            rec[nm] = r
        rec["cap_frac"] = self.n_cap / max(self.n_mv, 1)
        if self.Mcs0 is not None:
            rec["Mcs_rel"] = float(self.m[self.is_c].sum() / self.Mcs0 - 1)
        self.diag.append(rec)
        return rec


def run(cfg):
    """CFG621 run() verbatim except that it builds the CFG622 Sim (masked lensing estimator)."""
    T0 = time.time()
    s = Sim(cfg)
    mode = cfg.get("mode", "full")
    t_end_max = cfg.get("t_max", 3.0)
    next_diag = 0.0
    t_peri = None
    calib = mode == "calib"
    s.diagnose(alts=not calib); next_diag += DIAG_EVERY
    while True:
        vmax = np.abs(s.v).max()
        dt = min(L.hydro_dt(s.U, s.g.dx), 0.3 * s.g.dx / vmax, 0.005, next_diag - s.t + 1e-9)
        dt = max(dt, 1e-5)
        s.step(dt)
        if s.t >= next_diag - 1e-9:
            s.diagnose(alts=not calib); next_diag += DIAG_EVERY
            if mode != "isolated" and t_peri is None and len(s.diag) > 1:
                d1 = s.diag[-2]; d2 = s.diag[-1]
                s1 = d1["sub"]["gal"][0] - d1["main"]["gal"][0]; s2 = d2["sub"]["gal"][0] - d2["main"]["gal"][0]
                if s1 > 0 >= s2:
                    t_peri = d1["t"] + (d2["t"] - d1["t"]) * s1 / (s1 - s2)
            if calib and t_peri is not None:
                ep = epoch(s.diag, t_peri)
                if ep is not None:
                    return dict(cfg=_clean(cfg), t_peri=t_peri, wall_s=time.time() - T0, **ep)
            if mode == "isolated" and s.t >= cfg.get("t_iso", 0.6) - 1e-9:
                break
            if t_peri is not None and s.t >= t_peri + cfg.get("t_after", 0.8):
                break
            if s.t >= t_end_max:
                break
    return dict(cfg=_clean(cfg), t_peri=t_peri, wall_s=time.time() - T0, n_cap=s.n_cap, n_mv=s.n_mv,
                Mph_tot=[p.Mph_tot for p in s.progs], Mb=[p.Mb for p in s.progs], Mcc=[p.Mcc for p in s.progs],
                Sigma_cc=s.Sigma_cc, rt=[p.rt for p in s.progs], r200=[p.r200 for p in s.progs], diag=s.diag)
