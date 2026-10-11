#!/usr/bin/env python3
"""CFG621 simulator: CFG599's model imported read-only (../CFG599_merger_stopwatch_v2/cfg599_sim.py), with the stage-A declared
estimator (FROZEN_CRITERIA_A.md E-1, E-2): shrinking circle R0 300 / R_min 75 kpc for galaxy, gas and lensing; lensing spread
over the variants (300,60) (300,90) (200,75) (400,75).  Nothing else differs from CFG599.
kappa = 1/2 is fitted; the cold energy's mass is required (an input); no particle species."""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG599_merger_stopwatch_v2"))
import cfg599_lib as L      # noqa: E402  (read-only re-use)
import cfg599_sim as S599   # noqa: E402

R0, RMIN = 300.0, 75.0
LENS_ALTS = [(300.0, 60.0), (300.0, 90.0), (200.0, 75.0), (400.0, 75.0)]
DIAG_EVERY = S599.DIAG_EVERY
PX = S599.PX
epoch = S599.epoch
_clean = S599._clean


class Sim(S599.Sim):
    def diagnose(self, alts=True):
        XX, YY = self.XX, self.YY
        gas_k, st_k, tot, cold = self.maps()
        rec = {"t": self.t}
        pk = lambda S, st, a=R0, b=RMIN: L.shrink_peak(XX, YY, S, st, R0=a, Rmin=b)
        for k, nm in enumerate(self.names):
            sel = self.is_s & (self.tag == k)
            gal, okg = pk(st_k[k], np.median(self.x[sel, :2], axis=0))
            gs = L.massweighted_start(XX, YY, gas_k[k], gal, 600.0)
            gas, oks = pk(gas_k[k], gs)
            lens, okl = pk(tot, gal)
            cpk, _ = pk(cold, gal) if cold.sum() > 0 else (gal, True)
            r = dict(gal=gal.tolist(), gas=gas.tolist(), lens=lens.tolist(), cold=cpk.tolist(), conv=[bool(okg), bool(oks), bool(okl)])
            if alts and (nm == "sub" or len(self.names) == 1):
                la = [pk(tot, gal, a, b)[0] for a, b in LENS_ALTS]
                r["lens_alts"] = [x.tolist() for x in la]
                r["lens_spread"] = float(max(np.hypot(*(x - lens)) for x in la))
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
    """CFG599 run() verbatim except that it builds the CFG621 Sim (declared estimator)."""
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
