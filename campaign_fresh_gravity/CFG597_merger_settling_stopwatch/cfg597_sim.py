#!/usr/bin/env python3
"""CFG597 single-run simulator (criteria FROZEN_CRITERIA.md, ae49ff4d7).  Imported by cfg597_main.py; run() returns a dict
of time series.  One run = one (mass ratio, case, rule, alpha, footing) cell of section 2 M-7, or a calibration / control run."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import math, time
import numpy as np
np.seterr(over="ignore", divide="ignore", invalid="ignore")
import cfg597_lib as L

M_MAIN = 1.5e15
M_SUB = {"10": 1.5e14, "4": 3.75e14}
D0 = 2300.0
N_ST = (40000, 20000)
N_CS = (160000, 60000)
N_CU = (120000, 40000)
RB = np.linspace(0.0, 4000.0, 321)            # radial bin edges for the phantom and the Jeans target (12.5 kpc)
RBC = 0.5 * (RB[1:] + RB[:-1])
DIAG_EVERY = 0.01                             # Gyr
PX = 12.5                                     # projected map pixel, kpc


def jeans_maxwell(rng, prog, rho_tr, rr):
    s2 = prog.jeans_sigma2(rho_tr)
    s = np.sqrt(np.maximum(np.interp(rr, prog.r, s2), 0.0))
    return rng.standard_normal((rr.size, 3)) * s[:, None]


class Sim:
    def __init__(self, cfg):
        self.cfg = cfg
        self.rng = np.random.default_rng(cfg.get("seed", 597))
        self.g = L.Grid()
        foot, case, swap = cfg["foot"], cfg["case"], cfg.get("swap", False)
        self.alpha = cfg["alpha"]                 # float, or math.inf
        self.rule = cfg.get("rule", "2S")
        self.ou = cfg.get("ou", True) and self.alpha > 0
        self.a0 = L.A0[foot]
        iso = cfg.get("mode") == "isolated"
        progs = [L.Progenitor(M_MAIN, foot, case, swap=swap)]
        if not iso:
            progs.append(L.Progenitor(M_SUB[cfg["ratio"]], foot, case, swap=swap, rc_frac=cfg.get("sub_rc_frac", 0.1)))
        self.progs = progs
        Mt = [p.Mtot[-1] for p in progs]
        if iso:
            cen = [np.zeros(3)]; vel = [np.zeros(3)]
        else:
            fm = Mt[1] / (Mt[0] + Mt[1])
            cen = [np.array([-D0 * fm, 0, 0]), np.array([D0 * (1 - fm), 0, 0])]
            v0 = cfg["v0"]
            vel = [np.array([v0 * fm, 0, 0]), np.array([-v0 * (1 - fm), 0, 0])]
        self.cen0 = cen
        # ---- gas on the grid
        g = self.g
        rho = np.zeros(g.n); P = np.zeros(g.n); mom = np.zeros((3,) + g.n); rs = np.zeros(g.n)
        for k, p in enumerate(progs):
            r = g.radius_from(cen[k])
            rk = np.interp(r, p.r, p.rho_g); Pk = np.interp(r, p.r, p.P)
            rho += rk; P += Pk; mom += rk[None] * vel[k][:, None, None, None]
            if k == 1:
                rs = rk
        self.rho_floor = 1e-4 * progs[0].rho_g0
        rho_f = np.maximum(rho, self.rho_floor)
        v = mom / rho_f
        X = rs / rho_f
        self.U = L.cons(rho_f, v, np.maximum(P, 1e-8 * rho_f * (1e3 * L.KMS) ** 2), X)
        # ---- particles: stars, settled cold (unless alpha = inf), unsettled cold (case U)
        pos, vv, mm, tag, kind = [], [], [], [], []
        for k, p in enumerate(progs):
            comps = [("s", p.rho_s, p.Ms, N_ST[k])]
            if math.isfinite(self.alpha):
                comps.append(("c", p.rho_ph, p.Mph, N_CS[k]))
            if case == "U":
                comps.append(("u", p.rho_u, p.Mu, N_CU[k]))
            for kd, rho_tr, Mcum, n in comps:
                x, rr = L.sample_radial(self.rng, p.r, Mcum, n)
                vk = jeans_maxwell(self.rng, p, rho_tr, rr)
                pos.append(x + cen[k]); vv.append(vk + vel[k]); mm.append(np.full(n, Mcum[-1] / n))
                tag.append(np.full(n, k)); kind.append(np.full(n, kd))
        self.x = np.concatenate(pos); self.v = np.concatenate(vv); self.m = np.concatenate(mm)
        self.tag = np.concatenate(tag); self.kind = np.concatenate(kind)
        self.is_s = self.kind == "s"; self.is_c = self.kind == "c"; self.is_u = self.kind == "u"
        self.xb = [c.copy() for c in cen]          # baryon centres (phantom)
        self.xc = [c.copy() for c in cen]          # settled cold centres (Jeans target)
        # tau floor: rho_m floor = rho_floor x (rho_m/rho_gas) at the main IC centre
        p0 = progs[0]
        ratio = (p0.rho_g[1] + p0.rho_s[1] + p0.rho_ph[1] + p0.rho_u[1]) / p0.rho_g[1]
        self.rho_m_floor = self.rho_floor * ratio
        self.field_cs = None
        self.n_cap = 0; self.n_mv = 0
        self.Mcs0 = float(self.m[self.is_c].sum()) if self.is_c.any() else None
        if not math.isfinite(self.alpha):
            self.field_cs = self.phantom_field()
        self.diag = []
        self.t = 0.0

    # ------------------------------------------------------------------ the phantom of the CURRENT baryons
    def gas_masses(self):
        rho = self.U[0]; X = np.clip(self.U[5] / rho, 0, 1)
        Mc = rho * self.g.dV
        return [Mc * (1 - X), Mc * X][:len(self.progs)]

    def phantom_field(self):
        g = self.g
        gm = self.gas_masses()
        X, Y, Z = g.xc
        out = np.zeros(g.n)
        for k, p in enumerate(self.progs):
            sel = self.is_s & (self.tag == k)
            xs, ms = self.x[sel], self.m[sel]
            c = self.xb[k].copy()
            for _ in range(3):
                r = g.radius_from(c)
                inn = r < p.rt
                wg = gm[k] * inn
                M = wg.sum()
                cg = np.array([(wg.sum((1, 2)) * X).sum(), (wg.sum((0, 2)) * Y).sum(), (wg.sum((0, 1)) * Z).sum()])
                ds = np.linalg.norm(xs - c, axis=1) < p.rt
                M += ms[ds].sum(); cg += (ms[ds, None] * xs[ds]).sum(0)
                c = cg / M if M > 0 else c
            self.xb[k] = c
            r = g.radius_from(c)
            hb = np.histogram(r.ravel(), RB, weights=gm[k].ravel())[0]
            hb += np.histogram(np.linalg.norm(xs - c, axis=1), RB, weights=ms)[0]
            Mcum = np.concatenate([[0.0], np.cumsum(hb)])
            rho_ph, Mt = L.phantom_profile_from_mass(RB, Mcum, self.a0, p.rt)
            f = np.interp(r, RBC, rho_ph, right=0.0) * (r < p.rt)
            s = f.sum() * g.dV
            if s > 0:
                f *= Mt / s
            out += f
        return out

    # ------------------------------------------------------------------ one step
    def step(self, dt):
        g = self.g
        x, v, m = self.x, self.v, self.m
        rho_p = g.deposit(x, m)                       # stars + settled particles + unsettled particles
        rho_tot = self.U[0] + rho_p + (self.field_cs if self.field_cs is not None else 0.0)
        phi = g.poisson(rho_tot)
        gr = [-a for a in g.grad(phi)]
        ax_, ay_, az_ = g.interp(x, gr)
        v += np.stack([ax_, ay_, az_], 1) * dt
        x += v * dt
        self.U = L.hydro_step(self.U, gr, dt, g.dx, self.rho_floor)
        if not math.isfinite(self.alpha):
            self.field_cs = self.phantom_field()
        elif self.alpha > 0:
            self.settle(dt, rho_tot)
        self.t += dt

    def settle(self, dt, rho_tot):
        g = self.g
        c = self.is_c
        xc, vc, mc = self.x[c], self.v[c], self.m[c]
        rho_cs = g.deposit(xc, mc)
        rho_ph = self.phantom_field()
        d = rho_ph - rho_cs
        if self.rule == "1S":
            d = np.maximum(d, 0.0)
        psi = g.poisson(d)
        gp = g.grad(psi)
        tau = 1.0 / np.sqrt(4 * math.pi * L.G * np.maximum(rho_tot, self.rho_m_floor))
        px, py, pz, taup = g.interp(xc, gp + [tau])
        disp = -self.alpha * taup[:, None] * np.stack([px, py, pz], 1) * dt
        nd = np.linalg.norm(disp, axis=1); lim = 0.5 * g.dx
        cap = nd > lim
        disp[cap] *= (lim / nd[cap])[:, None]
        self.n_cap += int(cap.sum()); self.n_mv += int(nd.size)
        xc = xc + disp
        if self.ou:
            # local mean velocity of settled cold energy
            mx = g.deposit(xc, mc * vc[:, 0]); my = g.deposit(xc, mc * vc[:, 1]); mz = g.deposit(xc, mc * vc[:, 2])
            mrho = g.deposit(xc, mc)
            ix, iy, iz, im = g.interp(xc, [mx, my, mz, mrho])
            u = np.stack([ix, iy, iz], 1) / np.maximum(im, 1e-300)[:, None]
            s2 = np.zeros(xc.shape[0])
            tg = self.tag[c]
            for k, p in enumerate(self.progs):
                sel = tg == k
                cc = self.xc[k].copy()
                for _ in range(4):
                    rr = np.linalg.norm(xc[sel] - cc, axis=1); w = rr < 300.0
                    if w.sum() > 50:
                        cc = (mc[sel][w, None] * xc[sel][w]).sum(0) / mc[sel][w].sum()
                self.xc[k] = cc
                rr = np.linalg.norm(xc[sel] - cc, axis=1)
                vol = 4 * math.pi / 3 * np.diff(RB ** 3)
                rho_c = np.histogram(rr, RB, weights=mc[sel])[0] / vol
                # total mass of the progenitor about the same centre: its baryons + its cold energy
                Mall = np.histogram(rr, RB, weights=mc[sel])[0]
                oth = (self.tag == k) & ~c
                Mall += np.histogram(np.linalg.norm(self.x[oth] - cc, axis=1), RB, weights=self.m[oth])[0]
                gm = self.gas_masses()[k]
                Mall += np.histogram(g.radius_from(cc).ravel(), RB, weights=gm.ravel())[0]
                Menc = np.cumsum(Mall)
                gN = L.G * Menc / RB[1:] ** 2
                f = rho_c * gN * np.diff(RB)
                I = np.cumsum(f[::-1])[::-1]
                s2k = np.where(rho_c > 0, I / np.maximum(rho_c, 1e-300), 0.0)
                s2[sel] = np.interp(rr, RBC, s2k)
            a = np.exp(-self.alpha * dt / taup)
            # isotropic target: each Cartesian component has variance s2 (the 1-D isotropic Jeans sigma^2)
            vn = u + a[:, None] * (vc - u) + np.sqrt(np.maximum(1 - a ** 2, 0) * s2)[:, None] * self.rng.standard_normal(vc.shape)
            dv = vn - vc
            dv -= (mc[:, None] * dv).sum(0) / mc.sum()       # exact momentum conservation (C5)
            vc = vc + dv
            self.v[c] = vc
        self.x[c] = xc

    # ------------------------------------------------------------------ diagnostics
    def project(self):
        g = self.g
        nxp = int(round(g.L[0] / PX)); nyp = int(round(g.L[1] / PX))
        X = g.lo[0] + (np.arange(nxp) + 0.5) * PX; Y = g.lo[1] + (np.arange(nyp) + 0.5) * PX
        rep = int(round(g.dx / PX))
        def up(F):        # project a 3-D density along z and upsample to the PX grid, mass conserving
            S = F.sum(2) * g.dx
            return np.repeat(np.repeat(S, rep, 0), rep, 1)
        def dep2(sel):
            xy = self.x[sel, :2]; mm = self.m[sel]
            u = (xy - g.lo[:2]) / PX - 0.5
            i0 = np.floor(u).astype(int); w1 = u - i0; w0 = 1 - w1
            out = np.zeros(nxp * nyp)
            for a in (0, 1):
                for b in (0, 1):
                    ia = i0[:, 0] + a; ib = i0[:, 1] + b
                    w = (w0[:, 0] if a == 0 else w1[:, 0]) * (w0[:, 1] if b == 0 else w1[:, 1])
                    ok = (ia >= 0) & (ia < nxp) & (ib >= 0) & (ib < nyp)
                    out += np.bincount(ia[ok] * nyp + ib[ok], weights=(mm * w)[ok], minlength=out.size)
            return out.reshape(nxp, nyp) / PX ** 2
        rho = self.U[0]; Xs = np.clip(self.U[5] / rho, 0, 1)
        gas_all = up(rho)
        gas_k = [up(rho * (1 - Xs)), up(rho * Xs)][:len(self.progs)]
        st_k = [dep2(self.is_s & (self.tag == k)) for k in range(len(self.progs))]
        cold = dep2(self.is_c | self.is_u)
        if self.field_cs is not None:
            cold = cold + up(self.field_cs)
        stars = sum(st_k)
        tot = gas_all + stars + cold
        return np.meshgrid(X, Y, indexing="ij"), gas_k, st_k, tot, cold

    def diagnose(self):
        (XX, YY), gas_k, st_k, tot, cold = self.project()
        rec = {"t": self.t}
        for k, nm in enumerate(["main", "sub"][:len(self.progs)]):
            sel = self.is_s & (self.tag == k)
            start = np.median(self.x[sel, :2], axis=0)
            gal = L.iter_centroid_2d(XX, YY, st_k[k], start, 150.0)
            sg = gas_k[k]
            near = ((XX - gal[0]) ** 2 + (YY - gal[1]) ** 2) < 800.0 ** 2
            ip = np.unravel_index(np.argmax(sg * near), sg.shape)
            gas = L.iter_centroid_2d(XX, YY, sg, (XX[ip], YY[ip]), 150.0)
            l100 = L.iter_centroid_2d(XX, YY, tot, gal, 100.0)
            l150 = L.iter_centroid_2d(XX, YY, tot, gal, 150.0)
            c150 = L.iter_centroid_2d(XX, YY, cold, gal, 150.0)
            vg = self.v[sel & (np.linalg.norm(self.x[:, :2] - gal, axis=1) < 200.0)]
            rec[nm] = dict(gal=gal.tolist(), gas=gas.tolist(), lens100=l100.tolist(), lens150=l150.tolist(), cold150=c150.tolist(),
                           vgal=vg.mean(0).tolist() if len(vg) else [0, 0, 0],
                           M300=float(tot[((XX - gal[0]) ** 2 + (YY - gal[1]) ** 2) < 300.0 ** 2].sum() * PX ** 2))
        rec["cap_frac"] = self.n_cap / max(self.n_mv, 1)
        if self.Mcs0 is not None:
            rec["Mcs_rel"] = float(self.m[self.is_c].sum() / self.Mcs0 - 1)
        self.diag.append(rec)
        return rec


def run(cfg):
    T0 = time.time()
    s = Sim(cfg)
    mode = cfg.get("mode", "full")
    t_end_max = cfg.get("t_max", 3.0)
    next_diag = 0.0
    t_peri = None
    rec = s.diagnose(); next_diag += DIAG_EVERY
    while True:
        vmax = np.abs(s.v).max()
        dt = min(L.hydro_dt(s.U, s.g.dx), 0.3 * s.g.dx / vmax, 0.005, next_diag - s.t + 1e-9)
        dt = max(dt, 1e-5)
        s.step(dt)
        if s.t >= next_diag - 1e-9:
            rec = s.diagnose(); next_diag += DIAG_EVERY
            if mode != "isolated" and t_peri is None and len(s.diag) > 1:
                d1 = s.diag[-2]; d2 = s.diag[-1]
                s1 = d1["sub"]["gal"][0] - d1["main"]["gal"][0]; s2 = d2["sub"]["gal"][0] - d2["main"]["gal"][0]
                if s1 > 0 >= s2:
                    t_peri = d1["t"] + (d2["t"] - d1["t"]) * s1 / (s1 - s2)
            if mode == "calib" and t_peri is not None and len(s.diag) > 2:
                # Disclosure 2026-10-10 (README D-1): calibrate on the relative galaxy speed at the 720-kpc post-pericentre epoch
                d0, d1, d2 = s.diag[-3], s.diag[-2], s.diag[-1]
                sep = [d["sub"]["gal"][0] - d["main"]["gal"][0] for d in (d0, d1, d2)]
                if sep[2] <= -cfg.get("sep_obs", 720.0):
                    vp = -(sep[2] - sep[0]) / (d2["t"] - d0["t"])
                    return dict(cfg=_clean(cfg), t_peri=t_peri, v_obs_kms=vp / L.KMS, t_obs=d2["t"], wall_s=time.time() - T0)
            if mode == "isolated" and s.t >= cfg.get("t_iso", 0.6):
                break
            if t_peri is not None and s.t >= t_peri + cfg.get("t_after", 0.8):
                break
            if s.t >= t_end_max:
                break
    return dict(cfg=_clean(cfg), t_peri=t_peri, wall_s=time.time() - T0, n_cap=s.n_cap, n_mv=s.n_mv,
                u_frac=[p.u_frac for p in s.progs], Mph_tot=[p.Mph_tot for p in s.progs], Mb=[p.Mb for p in s.progs],
                Mu_tot=[p.Mu_tot for p in s.progs], rt=[p.rt for p in s.progs], r200=[p.r200 for p in s.progs], diag=s.diag)


def _clean(cfg):
    out = {}
    for k, v in cfg.items():
        out[k] = ("inf" if (isinstance(v, float) and math.isinf(v)) else v)
    return out
