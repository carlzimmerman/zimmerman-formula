#!/usr/bin/env python3
"""CFG599 single-run simulator (criteria FROZEN_CRITERIA.md, 8a10775bd).  CFG597's model (grid hydro + PM + cold-energy drift
and FIX-2 OU toward the round phantom of the CURRENT baryons, no EFE) with the frozen fixes: the sub's cool-core cloud with
ram-pressure drag (M-3b), more particles (M-5b), the mass-conserving projection and shrinking-circle peaks (O-1, O-2) with the
lensing-peak convergence check.  run(cfg) returns a dict of time series."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import math, time
import numpy as np
np.seterr(over="ignore", divide="ignore", invalid="ignore")
import cfg599_lib as L
import cfg597_lib as L597

M_MAIN = 1.5e15
M_SUB = 1.5e14
D0 = 2300.0
N_ST = (160000, 100000)
N_CS = (200000, 100000)
N_CL = 40000
RB = np.linspace(0.0, 4000.0, 321)
RBC = 0.5 * (RB[1:] + RB[:-1])
DIAG_EVERY = 0.01
PX = 12.5
LENS_ALTS = [(300.0, 35.0), (300.0, 75.0), (200.0, 50.0), (400.0, 50.0)]


def jeans_maxwell(rng, prog, rho_tr, rr):
    s2 = prog.jeans_sigma2(rho_tr)
    s = np.sqrt(np.maximum(np.interp(rr, prog.r, s2), 0.0))
    return rng.standard_normal((rr.size, 3)) * s[:, None]


class Sim:
    def __init__(self, cfg):
        self.cfg = cfg
        self.rng = np.random.default_rng(cfg.get("seed", 599))
        self.g = L.Grid()
        foot, swap = cfg["foot"], cfg.get("swap", False)
        self.alpha = cfg["alpha"]
        self.eta = cfg.get("eta", 1.0)
        self.ou = self.alpha > 0
        self.a0 = L.A0[foot]
        mode = cfg.get("mode", "full")
        iso = mode == "isolated"
        if iso:
            which = cfg.get("iso_which", "main")
            progs = [L.Progenitor599(M_MAIN if which == "main" else M_SUB, foot, swap=swap, cloud=(which == "sub"))]
            nst = [N_ST[0] if which == "main" else N_ST[1]]; ncs = [N_CS[0] if which == "main" else N_CS[1]]
            self.names = [which]
        else:
            progs = [L.Progenitor599(M_MAIN, foot, swap=swap, cloud=False), L.Progenitor599(M_SUB, foot, swap=swap, cloud=True)]
            nst = list(N_ST); ncs = list(N_CS)
            self.names = ["main", "sub"]
        self.progs = progs
        Mt = [p.Mtot[-1] for p in progs]
        if iso:
            cen = [np.zeros(3)]; vel = [np.zeros(3)]
        else:
            fm = Mt[1] / (Mt[0] + Mt[1])
            cen = [np.array([-D0 * fm, 0, 0]), np.array([D0 * (1 - fm), 0, 0])]
            v0 = cfg["v0"]
            vel = [np.array([v0 * fm, 0, 0]), np.array([-v0 * (1 - fm), 0, 0])]
        g = self.g
        rho = np.zeros(g.n); P = np.zeros(g.n); mom = np.zeros((3,) + g.n); rs = np.zeros(g.n)
        for k, p in enumerate(progs):
            r = g.radius_from(cen[k])
            rk = np.interp(r, p.r, p.rho_g); Pk = np.interp(r, p.r, p.P)
            rho += rk; P += Pk; mom += rk[None] * vel[k][:, None, None, None]
            if self.names[k] == "sub":
                rs = rk
        self.rho_floor = 1e-4 * progs[0].rho_g0 if self.names[0] == "main" else 1e-4 * L.Progenitor599(M_MAIN, foot).rho_g0
        rho_f = np.maximum(rho, self.rho_floor)
        v = mom / rho_f
        X = rs / rho_f
        self.U = L.cons(rho_f, v, np.maximum(P, 1e-8 * rho_f * (1e3 * L.KMS) ** 2), X)
        pos, vv, mm, tag, kind = [], [], [], [], []
        for k, p in enumerate(progs):
            comps = [("s", p.rho_s, p.Ms, nst[k])]
            if math.isfinite(self.alpha):
                comps.append(("c", p.rho_ph, p.Mph, ncs[k]))
            if p.cloud:
                comps.append(("g", p.rho_cc, p.Mcc_r, N_CL))
            for kd, rho_tr, Mcum, n in comps:
                x, rr = L.sample_radial(self.rng, p.r, Mcum, n)
                vk = jeans_maxwell(self.rng, p, rho_tr, rr)
                pos.append(x + cen[k]); vv.append(vk + vel[k]); mm.append(np.full(n, Mcum[-1] / n))
                tag.append(np.full(n, k)); kind.append(np.full(n, kd))
        self.x = np.concatenate(pos); self.v = np.concatenate(vv); self.m = np.concatenate(mm)
        self.tag = np.concatenate(tag); self.kind = np.concatenate(kind)
        self.is_s = self.kind == "s"; self.is_c = self.kind == "c"; self.is_g = self.kind == "g"
        self.is_bp = self.is_s | self.is_g                   # baryonic particles
        self.Sigma_cc = next((p.Sigma_cc for p in progs if p.cloud), None)
        self.xb = [c.copy() for c in cen]
        self.xc = [c.copy() for c in cen]
        p0 = progs[0]
        ratio = (p0.rho_g[1] + p0.rho_s[1] + p0.rho_ph[1] + p0.rho_cc[1]) / p0.rho_g[1]
        self.rho_m_floor = self.rho_floor * ratio
        self.field_cs = None
        self.n_cap = 0; self.n_mv = 0
        self.Mcs0 = float(self.m[self.is_c].sum()) if self.is_c.any() else None
        if not math.isfinite(self.alpha):
            self.field_cs = self.phantom_field()
        self.diag = []
        self.t = 0.0
        nxp = int(round(g.L[0] / PX)); nyp = int(round(g.L[1] / PX))
        self.Xp = g.lo[0] + (np.arange(nxp) + 0.5) * PX; self.Yp = g.lo[1] + (np.arange(nyp) + 0.5) * PX
        self.XX, self.YY = np.meshgrid(self.Xp, self.Yp, indexing="ij")

    # ------------------------------------------------------------------ gas mass per progenitor on the grid
    def gas_masses(self):
        rho = self.U[0]; X = np.clip(self.U[5] / rho, 0, 1)
        Mc = rho * self.g.dV
        if len(self.progs) == 1:
            return [Mc]
        return [Mc * (1 - X), Mc * X]

    def phantom_field(self):
        g = self.g
        gm = self.gas_masses()
        X, Y, Z = g.xc
        out = np.zeros(g.n)
        for k, p in enumerate(self.progs):
            sel = self.is_bp & (self.tag == k)
            xs, ms = self.x[sel], self.m[sel]
            c = self.xb[k].copy()
            for _ in range(3):
                r = g.radius_from(c)
                wg = gm[k] * (r < p.rt)
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

    # ------------------------------------------------------------------ M-3b ram-pressure drag on the cool core
    def drag(self, dt):
        if not self.is_g.any() or self.eta <= 0:
            return
        g = self.g
        sel = self.is_g
        xg, vg, mg = self.x[sel], self.v[sel], self.m[sel]
        rho = self.U[0]
        ug = [self.U[1 + i] / rho for i in range(3)]
        mc = g.deposit(xg, mg)
        pc = [g.deposit(xg, mg * vg[:, i]) for i in range(3)]
        out = g.interp(xg, pc + [mc, rho] + ug)
        im = np.maximum(out[3], 1e-300)
        ucl = np.stack(out[:3], 1) / im[:, None]
        rg = out[4]; ugp = np.stack(out[5:8], 1)
        du = ucl - ugp
        s = np.linalg.norm(du, axis=1)
        k = self.eta * rg / self.Sigma_cc
        dun = du / (1.0 + k * s * dt)[:, None]
        dv = dun - du
        vn = vg + dv
        dp = mg[:, None] * dv
        dKE = 0.5 * mg * ((vn ** 2).sum(1) - (vg ** 2).sum(1))
        for i in range(3):
            self.U[1 + i] -= g.deposit(xg, dp[:, i])
        self.U[4] -= g.deposit(xg, dKE)
        self.v[sel] = vn
        L597._fix(self.U, self.rho_floor)

    # ------------------------------------------------------------------ one step (CFG597 order, drag after hydro)
    def step(self, dt):
        g = self.g
        x, v, m = self.x, self.v, self.m
        rho_p = g.deposit(x, m)
        rho_tot = self.U[0] + rho_p + (self.field_cs if self.field_cs is not None else 0.0)
        phi = g.poisson(rho_tot)
        gr = [-a for a in g.grad(phi)]
        ax_, ay_, az_ = g.interp(x, gr)
        v += np.stack([ax_, ay_, az_], 1) * dt
        x += v * dt
        self.U = L.hydro_step(self.U, gr, dt, g.dx, self.rho_floor)
        self.drag(dt)
        if not math.isfinite(self.alpha):
            self.field_cs = self.phantom_field()
        elif self.alpha > 0:
            self.settle(dt, rho_tot)
        self.t += dt

    def settle(self, dt, rho_tot):
        """CFG597 M-5 settle step (rule 2S), unchanged except that the baryon particles include the cloud."""
        g = self.g
        c = self.is_c
        xc, vc, mc = self.x[c], self.v[c], self.m[c]
        rho_cs = g.deposit(xc, mc)
        rho_ph = self.phantom_field()
        d = rho_ph - rho_cs
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
            mx = g.deposit(xc, mc * vc[:, 0]); my = g.deposit(xc, mc * vc[:, 1]); mz = g.deposit(xc, mc * vc[:, 2])
            mrho = g.deposit(xc, mc)
            ix, iy, iz, im = g.interp(xc, [mx, my, mz, mrho])
            u = np.stack([ix, iy, iz], 1) / np.maximum(im, 1e-300)[:, None]
            s2 = np.zeros(xc.shape[0])
            tg = self.tag[c]
            gms = self.gas_masses()
            vol = 4 * math.pi / 3 * np.diff(RB ** 3)
            for k, p in enumerate(self.progs):
                sel = tg == k
                cc = self.xc[k].copy()
                for _ in range(4):
                    rr = np.linalg.norm(xc[sel] - cc, axis=1); w = rr < 300.0
                    if w.sum() > 50:
                        cc = (mc[sel][w, None] * xc[sel][w]).sum(0) / mc[sel][w].sum()
                self.xc[k] = cc
                rr = np.linalg.norm(xc[sel] - cc, axis=1)
                rho_c = np.histogram(rr, RB, weights=mc[sel])[0] / vol
                Mall = np.histogram(rr, RB, weights=mc[sel])[0]
                oth = (self.tag == k) & ~c
                Mall += np.histogram(np.linalg.norm(self.x[oth] - cc, axis=1), RB, weights=self.m[oth])[0]
                Mall += np.histogram(g.radius_from(cc).ravel(), RB, weights=gms[k].ravel())[0]
                Menc = np.cumsum(Mall)
                gN = L.G * Menc / RB[1:] ** 2
                f = rho_c * gN * np.diff(RB)
                I = np.cumsum(f[::-1])[::-1]
                s2k = np.where(rho_c > 0, I / np.maximum(rho_c, 1e-300), 0.0)
                s2[sel] = np.interp(rr, RBC, s2k)
            a = np.exp(-self.alpha * dt / taup)
            vn = u + a[:, None] * (vc - u) + np.sqrt(np.maximum(1 - a ** 2, 0) * s2)[:, None] * self.rng.standard_normal(vc.shape)
            dv = vn - vc
            dv -= (mc[:, None] * dv).sum(0) / mc.sum()
            vc = vc + dv
            self.v[c] = vc
        self.x[c] = xc

    # ------------------------------------------------------------------ diagnostics (O-1, O-2)
    def dep2(self, sel):
        g = self.g
        nxp, nyp = self.XX.shape
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

    def maps(self):
        g = self.g
        rho = self.U[0]; Xs = np.clip(self.U[5] / rho, 0, 1)
        proj = lambda F: L.project_grid_bilinear(F, g, self.Xp, self.Yp)
        gas_all = proj(rho)
        if len(self.progs) == 1:
            gas_k = [gas_all.copy()]
        else:
            gas_k = [proj(rho * (1 - Xs)), proj(rho * Xs)]
        cloud = [self.dep2(self.is_g & (self.tag == k)) for k in range(len(self.progs))]
        gas_k = [gk + ck for gk, ck in zip(gas_k, cloud)]
        st_k = [self.dep2(self.is_s & (self.tag == k)) for k in range(len(self.progs))]
        cold = self.dep2(self.is_c)
        if self.field_cs is not None:
            cold = cold + proj(self.field_cs)
        tot = gas_all + sum(cloud) + sum(st_k) + cold
        return gas_k, st_k, tot, cold

    def diagnose(self, alts=True):
        XX, YY = self.XX, self.YY
        gas_k, st_k, tot, cold = self.maps()
        rec = {"t": self.t}
        for k, nm in enumerate(self.names):
            sel = self.is_s & (self.tag == k)
            gal, okg = L.shrink_peak(XX, YY, st_k[k], np.median(self.x[sel, :2], axis=0))
            gs = L.massweighted_start(XX, YY, gas_k[k], gal, 600.0)
            gas, oks = L.shrink_peak(XX, YY, gas_k[k], gs)
            lens, okl = L.shrink_peak(XX, YY, tot, gal)
            cpk, _ = L.shrink_peak(XX, YY, cold, gal) if cold.sum() > 0 else (gal, True)
            r = dict(gal=gal.tolist(), gas=gas.tolist(), lens=lens.tolist(), cold=cpk.tolist(), conv=[bool(okg), bool(oks), bool(okl)])
            if alts and (nm == "sub" or len(self.names) == 1):
                la = [L.shrink_peak(XX, YY, tot, gal, R0=a, Rmin=b)[0] for a, b in LENS_ALTS]
                r["lens_alts"] = [x.tolist() for x in la]
                r["lens_spread"] = float(max(np.hypot(*(x - lens)) for x in la))
            vg = self.v[sel & (np.linalg.norm(self.x[:, :2] - gal, axis=1) < 200.0)]
            r["vgal"] = vg.mean(0).tolist() if len(vg) else [0, 0, 0]
            r["M300"] = float(tot[((XX - gal[0]) ** 2 + (YY - gal[1]) ** 2) < 300.0 ** 2].sum() * PX ** 2)
            if self.is_g.any() and nm == "sub":
                cg = self.is_g & (self.tag == k)
                r["cloud_com"] = (self.m[cg, None] * self.x[cg, :2]).sum(0).__truediv__(self.m[cg].sum()).tolist()
            rec[nm] = r
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


SEP_OBS = 720.0


def epoch(diag, t_peri, sep_obs=SEP_OBS):
    """M-6 K1 epoch: first post-pericentre diagnostic with sub-main galaxy separation <= -720 kpc; speed = two-point difference
    over the bracketing diagnostics; d_SG and t interpolated to the crossing.  None if not reached."""
    sep = [d["sub"]["gal"][0] - d["main"]["gal"][0] for d in diag]
    t = [d["t"] for d in diag]
    for i in range(1, len(diag)):
        if t[i] > t_peri and sep[i] <= -sep_obs:
            if t[i - 1] <= t_peri:
                continue
            w = (sep[i - 1] + sep_obs) / (sep[i - 1] - sep[i])
            dsg = [math.hypot(diag[j]["sub"]["gas"][0] - diag[j]["sub"]["gal"][0], diag[j]["sub"]["gas"][1] - diag[j]["sub"]["gal"][1]) for j in (i - 1, i)]
            return dict(i_obs=i, w_obs=w, t_obs=t[i - 1] + w * (t[i] - t[i - 1]),
                        v_obs_kms=-(sep[i] - sep[i - 1]) / (t[i] - t[i - 1]) / L.KMS,
                        dSG_obs=dsg[0] + w * (dsg[1] - dsg[0]))
    return None


def _clean(cfg):
    return {k: ("inf" if (isinstance(v, float) and math.isinf(v)) else v) for k, v in cfg.items()}
