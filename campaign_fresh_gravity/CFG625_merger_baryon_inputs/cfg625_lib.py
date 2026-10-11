#!/usr/bin/env python3
"""CFG625 library (criteria FROZEN_CRITERIA.md, 9afb3f44b): data-based progenitor baryons for CFG623's merger model.

Progenitor625(M200, foot, swap, cloud, variant) mirrors CFG599's Progenitor599 step by step; only the baryon components differ by
variant (FROZEN_CRITERIA.md section 2).  variant 'BASE' must reproduce Progenitor599 exactly (gate C0).
Sim625 = CFG622's Sim (read-only) built with Progenitor625 and with extra projected-mass diagnostics (physics unchanged).
kappa = 1/2 is fitted; the cold energy's mass is required (an input); no particle species."""
import os, sys, math, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG622_merger_stopwatch_v4"))
import cfg622_sim as S622   # noqa: E402 (read-only; puts CFG621, CFG599, CFG597 on sys.path)
import cfg599_lib as L      # noqa: E402
from cfg599_lib import G, A0, r200_of, cumtrapz_sph, phantom_mass, F_CC, A_CC, R_CC_T  # noqa: E402

VARIANTS = ["B1", "B2", "B3"]
# [F26] Famaey 2026 Table 1 as transcribed in hunt_2026/h57_bullet_peaks.py (M [Msun], a [kpc])
F26_STARS = {"main": (1.196e13, 470.0), "sub": (4.0e12, 245.0)}
F26_GAS_MAIN = (2.0e14, 565.0)
F26_GAS_SUB = (1.5e13, 505.0)
F26_BULLET = ((1.5e13, 90.0), (6.8e12, 70.0))
# [C06] Clowe+06 Table 2 100-kpc aperture stellar masses at the BCGs
C06_MSTAR100 = {"main": 0.54e12, "sub": 0.58e12}
RE_BCG = 30.0                       # kpc, DECLARED bracket (no measured R_e on disk)
A_HERN = RE_BCG / 1.8153            # Hernquist scale from R_e
# lensing masses (M-RAW report only; PROVISIONAL)
P16_M250 = {"main": (2.5e14, 0.1e14), "sub": (2.0e14, 0.2e14)}
R26_M300 = {"main": 3.5e14, "sub": 2.3e14}


def plummer_rho(r, M, a):
    """Plummer density with total mass M (to infinity)."""
    return 3.0 * M / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5


def proj_half_mass_radius(r, rho):
    R = np.geomspace(1.0, r[-1] / 2, 400)
    Mp = np.array([proj_mass(r, rho, x) for x in R])
    return float(np.interp(0.5 * Mp[-1], Mp, R))


def proj_mass(r, rho, R):
    """mass of a spherical density rho(r) inside the cylinder of radius R (any length)."""
    w = np.where(r <= R, 1.0, 1.0 - np.sqrt(np.maximum(1.0 - (R / np.maximum(r, 1e-9)) ** 2, 0.0)))
    f = 4 * math.pi * r ** 2 * rho * w
    return float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(r)))


class Progenitor625:
    def __init__(self, M200, foot, swap=False, cloud=False, nr=4000, rmax=8000.0, variant="BASE"):
        self.variant = variant
        role = "sub" if cloud else "main"
        self.role = role
        self.M200 = M200; self.r200 = r200_of(M200); self.rt = min(self.r200, 1200.0)
        self.a0 = A0[foot]
        r = np.concatenate([[0.0], np.geomspace(0.5, rmax, nr)]); self.r = r
        rr = np.maximum(r, 1e-3)
        soft = np.where(r < self.rt, 1.0, (rr / self.rt) ** -8.0)
        hard = (r < self.rt).astype(float)
        self.cloud = cloud
        # ---------------- components: (grid-gas shape, grid-gas mass), (cloud shape, mass), (stars rho)
        if variant == "BASE":
            self.Mb = M200 / 6.73
            fg, fs = (0.13, 0.87) if swap else (0.87, 0.13)
            self.Mgas_all, self.Mst = fg * self.Mb, fs * self.Mb
            self.Mcc = F_CC * self.Mgas_all if cloud else 0.0
            self.Mgas = self.Mgas_all - self.Mcc
            rc = 0.1 * self.r200
            sh = (1 + (r / rc) ** 2) ** -1.0 * soft
            Mg = cumtrapz_sph(r, sh)
            self.rho_g0 = self.Mgas / Mg[-1]
            self.rho_g = self.rho_g0 * sh; self.Mg = self.rho_g0 * Mg
            if cloud:
                pl = (1 + (r / A_CC) ** 2) ** -2.5 * (r < R_CC_T)
                Mp = cumtrapz_sph(r, pl)
                self.rho_cc = self.Mcc * pl / Mp[-1]; self.Mcc_r = self.Mcc * Mp / Mp[-1]
            else:
                self.rho_cc = 0 * r; self.Mcc_r = 0 * r
            self.Sigma_cc = self.Mcc / (math.pi * A_CC ** 2) if cloud else None
            rs = self.r200 / 4.0
            nfw = np.where(r < self.rt, 1.0 / (np.maximum(r, 1e-3) / rs * (1 + r / rs) ** 2), 0.0)
            Mn = cumtrapz_sph(r, nfw)
            self.nfw_shape = nfw / Mn[-1]; self.Mnfw_unit = Mn / Mn[-1]
            self.rho_s = self.Mst * self.nfw_shape; self.Ms = self.Mst * self.Mnfw_unit
        else:
            Ms_, as_ = F26_STARS[role]
            rho_s = plummer_rho(r, Ms_, as_) * hard
            if variant == "B2":
                Mbcg = C06_MSTAR100[role]
                rho_s = plummer_rho(r, Ms_ - Mbcg, as_) * hard
                hern = 1.0 / ((rr / A_HERN) * (1 + rr / A_HERN) ** 3) * hard
                Mh = cumtrapz_sph(r, hern)
                rho_s = rho_s + Mbcg * hern / Mh[-1]
            Mst = cumtrapz_sph(r, rho_s)[-1]
            # gas (grid) shape and cloud
            if variant in ("B1", "B2"):
                Mb = M200 / 6.73
                Mgas_all = Mb - Mst
                Mcc = F_CC * Mgas_all if cloud else 0.0
                rc = 0.1 * self.r200
                gsh = (1 + (r / rc) ** 2) ** -1.0 * soft
                Mgs = cumtrapz_sph(r, gsh)
                rho_g = (Mgas_all - Mcc) / Mgs[-1] * gsh
                if cloud:
                    pl = (1 + (r / A_CC) ** 2) ** -2.5 * (r < R_CC_T)
                    rho_cc = Mcc * pl / cumtrapz_sph(r, pl)[-1]
                    a_eff = A_CC
                else:
                    rho_cc = 0 * r; a_eff = None
            else:  # B3
                Mg_, ag_ = F26_GAS_MAIN if role == "main" else F26_GAS_SUB
                rho_g = plummer_rho(r, Mg_, ag_) * soft
                if cloud:
                    (m1, a1), (m2, a2) = F26_BULLET
                    rho_cc = (plummer_rho(r, m1, a1) - plummer_rho(r, m2, a2)) * (r < R_CC_T)
                    assert (rho_cc >= 0).all(), "F26 bullet density negative"
                    a_eff = proj_half_mass_radius(r, rho_cc)
                else:
                    rho_cc = 0 * r; a_eff = None
            Mgrid = cumtrapz_sph(r, rho_g)[-1]
            Mcc_t = cumtrapz_sph(r, rho_cc)[-1] if cloud else 0.0
            if swap:   # exchange stellar mass and total gas mass; shapes and the cloud share kept
                Mgas_tot = Mgrid + Mcc_t
                fs_new = Mgas_tot / Mst; fg_new = Mst / Mgas_tot
                rho_s = rho_s * fs_new; rho_g = rho_g * fg_new; rho_cc = rho_cc * fg_new
                Mgrid *= fg_new; Mcc_t *= fg_new; Mst *= fs_new
            self.rho_g = rho_g; self.Mg = cumtrapz_sph(r, rho_g); self.Mgas = self.Mg[-1]
            self.rho_g0 = float(rho_g[0])
            self.rho_cc = rho_cc; self.Mcc_r = cumtrapz_sph(r, rho_cc) if cloud else 0 * r
            self.Mcc = float(self.Mcc_r[-1]) if cloud else 0.0
            self.Mgas_all = self.Mgas + self.Mcc
            self.Sigma_cc = self.Mcc / (math.pi * a_eff ** 2) if cloud else None
            self.a_eff = a_eff
            self.rho_s = rho_s; self.Ms = cumtrapz_sph(r, rho_s); self.Mst = float(self.Ms[-1])
            self.Mb = self.Mgas_all + self.Mst
        # ---------------- identical to Progenitor599 from here
        self.Mbar = self.Mg + self.Ms + self.Mcc_r
        Mph = phantom_mass(r, self.Mbar, self.a0)
        Mph_t = np.interp(self.rt, r, Mph)
        self.Mph = np.where(r < self.rt, Mph, Mph_t)
        self.rho_ph = np.gradient(self.Mph, r) / (4 * math.pi * np.maximum(r, 1e-3) ** 2)
        self.rho_ph[r >= self.rt] = 0.0
        self.Mph_tot = Mph_t
        self.Mtot = self.Mbar + self.Mph
        gN = G * self.Mtot / np.maximum(r, 1e-3) ** 2
        integrand = self.rho_g * gN
        P = np.zeros_like(r)
        P[-1] = self.rho_g[-1] * 0.5 * G * self.Mtot[-1] / r[-1]
        for k in range(len(r) - 2, -1, -1):
            P[k] = P[k + 1] + 0.5 * (integrand[k] + integrand[k + 1]) * (r[k + 1] - r[k])
        self.P = P
        self.rho_u = 0 * r; self.Mu = 0 * r; self.Mu_tot = 0.0; self.u_frac = 0.0

    jeans_sigma2 = L.Progenitor599.jeans_sigma2

    def static_masses(self):
        r = self.r
        bar = self.rho_g + self.rho_cc + self.rho_s
        return dict(Mb=float(self.Mbar[-1]), Mstars=self.Mst, Mgas=self.Mgas, Mcloud=self.Mcc, Mcold=float(self.Mph_tot),
                    Mb_proj250=proj_mass(r, bar, 250.0), Mcold_proj250=proj_mass(r, self.rho_ph, 250.0),
                    Mstars_proj100=proj_mass(r, self.rho_s, 100.0), a_eff_cloud=getattr(self, "a_eff", A_CC if self.cloud else None))


_ORIG = L.Progenitor599


def make_prog(variant):
    def prog(M200, foot, swap=False, cloud=False, **kw):
        return Progenitor625(M200, foot, swap=swap, cloud=cloud, variant=variant, **kw)
    return prog


class Sim625(S622.Sim):
    def __init__(self, cfg):
        L.Progenitor599 = make_prog(cfg["variant"])
        try:
            super().__init__(cfg)
        finally:
            L.Progenitor599 = _ORIG

    def diagnose(self, alts=True):
        rec = super().diagnose(alts=alts)
        XX, YY = self.XX, self.YY
        gas_k, st_k, tot, cold = self.maps()
        bar = tot - cold
        PX2 = S622.PX ** 2
        for nm in self.names:
            g = np.array(rec[nm]["gal"])
            rr2 = (XX - g[0]) ** 2 + (YY - g[1]) ** 2
            for R in (250, 300):
                m = rr2 < R * R
                rec[nm][f"Mproj{R}"] = [float(tot[m].sum() * PX2), float(bar[m].sum() * PX2), float(cold[m].sum() * PX2)]
        return rec


def run(cfg):
    """CFG622 run() verbatim except that it builds Sim625."""
    T0 = time.time()
    s = Sim625(cfg)
    mode = cfg.get("mode", "full")
    t_end_max = cfg.get("t_max", 3.0)
    next_diag = 0.0
    t_peri = None
    calib = mode == "calib"
    s.diagnose(alts=not calib); next_diag += S622.DIAG_EVERY
    while True:
        vmax = np.abs(s.v).max()
        dt = min(L.hydro_dt(s.U, s.g.dx), 0.3 * s.g.dx / vmax, 0.005, next_diag - s.t + 1e-9)
        dt = max(dt, 1e-5)
        s.step(dt)
        if s.t >= next_diag - 1e-9:
            s.diagnose(alts=not calib); next_diag += S622.DIAG_EVERY
            if mode != "isolated" and t_peri is None and len(s.diag) > 1:
                d1 = s.diag[-2]; d2 = s.diag[-1]
                s1 = d1["sub"]["gal"][0] - d1["main"]["gal"][0]; s2 = d2["sub"]["gal"][0] - d2["main"]["gal"][0]
                if s1 > 0 >= s2:
                    t_peri = d1["t"] + (d2["t"] - d1["t"]) * s1 / (s1 - s2)
            if calib and t_peri is not None:
                ep = S622.epoch(s.diag, t_peri)
                if ep is not None:
                    i = ep["i_obs"]
                    return dict(cfg=S622._clean(cfg), t_peri=t_peri, wall_s=time.time() - T0,
                                Mproj_obs={nm: [s.diag[j][nm][k] for j in (i - 1, i) for k in ("Mproj250", "Mproj300")]
                                           for nm in s.names}, **ep)
            if mode == "isolated" and s.t >= cfg.get("t_iso", 0.6) - 1e-9:
                break
            if t_peri is not None and s.t >= t_peri + cfg.get("t_after", 0.8):
                break
            if s.t >= t_end_max:
                break
    return dict(cfg=S622._clean(cfg), t_peri=t_peri, wall_s=time.time() - T0, n_cap=s.n_cap, n_mv=s.n_mv,
                Mph_tot=[p.Mph_tot for p in s.progs], Mb=[p.Mb for p in s.progs], Mcc=[p.Mcc for p in s.progs],
                Sigma_cc=s.Sigma_cc, rt=[p.rt for p in s.progs], r200=[p.r200 for p in s.progs], diag=s.diag)
