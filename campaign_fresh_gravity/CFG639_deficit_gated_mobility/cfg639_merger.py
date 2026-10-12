#!/usr/bin/env python3
"""CFG639 Part B (FROZEN_CRITERIA.md, dbe89ed33): the deficit-gated mobility HG in CFG623's merger pipeline (Bullet + Harvey).

CFG623's main (simulator cfg622_sim.py, estimator, window, stability rule, calibration, scores) is imported read-only.  The ONLY
change is CFG599's settle step with the gate G = 1[d > 0] (d = rho_ph - rho_cs, the code's own CIC grid) applied to the
displacement and to the OU update, momentum correction over gated elements only.  cfg["gate"] = "gate" (HG) or "none" (G = 1,
control B-G1).  Runs are cached in CFG639's own runs/ (never CFG623's).
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not "theory closed".
Run (heavy, ~10 GB over 4 processes): only via run_639.sh, which waits for the 1024^3 runs to end.
"""
import os, sys, json, math, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
C623 = os.path.join(HERE, "..", "CFG623_merger_stopwatch_v5")
sys.path.insert(0, C623)
import cfg623_main as M   # noqa: E402  (read-only; puts CFG622/621/599 on sys.path)
import cfg622_sim as S    # noqa: E402
import cfg599_sim as S599  # noqa: E402
L = M.L
RB, RBC = S599.RB, S599.RBC

M.RUNS = os.path.join(HERE, "runs"); os.makedirs(M.RUNS, exist_ok=True)
NODES = [0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
FEET = M.FEET
BASE = M.BASE
STATS = {}
_name623 = M.name_of


def name_of(c):
    s = _name623(c)
    if c.get("gate", "gate") == "none":
        s += "_G1"
    return s


class Sim639(S.Sim):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.gate_mode = cfg.get("gate", "gate")
        self.gstat = []                                   # (t, n_off, n_tot) per settle step

    def settle(self, dt, rho_tot):
        """CFG599 settle (CFG597 M-5 rule 2S + FIX-2 OU) with the mobility gate G on drift and OU."""
        g = self.g
        c = self.is_c
        xc, vc, mc = self.x[c], self.v[c], self.m[c]
        rho_cs = g.deposit(xc, mc)
        rho_ph = self.phantom_field()
        d = rho_ph - rho_cs
        psi = g.poisson(d)
        gp = g.grad(psi)
        tau = 1.0 / np.sqrt(4 * math.pi * L.G * np.maximum(rho_tot, self.rho_m_floor))
        px, py, pz, taup, dp = g.interp(xc, gp + [tau, d])
        G = (dp > 0) if self.gate_mode == "gate" else np.ones(dp.size, bool)
        self.gstat.append((self.t, int((~G).sum()), int(G.size)))
        disp = -self.alpha * taup[:, None] * np.stack([px, py, pz], 1) * dt
        disp[~G] = 0.0
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
            dv[~G] = 0.0
            if G.any():
                dv[G] -= (mc[G, None] * dv[G]).sum(0) / mc[G].sum()
            vc = vc + dv
            self.v[c] = vc
        self.x[c] = xc
        STATS["gstat"] = self.gstat


def worker(c):
    import cfg622_sim as SS
    fn = os.path.join(M.RUNS, name_of(c) + ".json")
    if os.path.exists(fn):
        return
    cc = dict(c); cc["v0"] = cc["v0_kms"] * L.KMS
    STATS.clear()
    res = SS.run(cc)
    res["gstat"] = STATS.get("gstat", [])
    json.dump(M._round(res), open(fn + ".tmp", "w")); os.replace(fn + ".tmp", fn)


# the gate only differs from CFG623 inside settle(); everything else is CFG623's code
S.Sim = Sim639
M.name_of = name_of
M.worker = worker


def max_diff(r, o):
    n = min(len(o["diag"]), len(r["diag"])); mx = 0.0
    for i in range(n):
        for key in ("gal", "gas", "lens", "lens_nomask"):
            mx = max(mx, float(np.hypot(*(np.array(r["diag"][i]["sub"][key]) - np.array(o["diag"][i]["sub"][key])))))
        for a, b in zip(r["diag"][i]["sub"]["lens_alts"], o["diag"][i]["sub"]["lens_alts"]):
            mx = max(mx, float(np.hypot(*(np.array(a) - np.array(b)))))
    return dict(n_epochs=[len(o["diag"]), len(r["diag"])], max_diff_kpc=mx)


def main():
    T0 = time.time()
    P = M.P
    P("CFG639 Part B: deficit-gated mobility in CFG623's merger pipeline (criteria dbe89ed33)")
    cfgs = [dict(alpha=a, foot=f, gate="gate", **BASE) for f in FEET for a in NODES]
    ctl = dict(alpha=0.1, foot="can", gate="none", **BASE)
    runs = M.pool_map(cfgs + [ctl])
    rg, rctl = runs[:-1], runs[-1]
    cells = {f"{M.astr(c['alpha'])}_{c['foot']}": M.score_run(r) for c, r in zip(cfgs, rg)}
    R = {"lane": "CFG639", "part": "B", "criteria": "dbe89ed33", "cells": cells, "void_reasons": []}
    # B-R: alpha = 0 reproduces CFG623 exactly
    br = {}
    for f in FEET:
        c = dict(alpha=0.0, foot=f, **BASE)
        o = json.load(open(os.path.join(C623, "runs", _name623(c) + ".json")))
        r = rg[cfgs.index(dict(alpha=0.0, foot=f, gate="gate", **BASE))]
        br[f] = max_diff(r, o)
    br_ok = all(v["max_diff_kpc"] == 0.0 for v in br.values())
    # B-G1: G = 1 at alpha = 0.1 canonical reproduces CFG623 a0.1_can exactly
    o = json.load(open(os.path.join(C623, "runs", _name623(dict(alpha=0.1, foot="can", **BASE)) + ".json")))
    bg1 = max_diff(rctl, o); bg1_ok = bg1["max_diff_kpc"] == 0.0
    R["B_R"] = dict(per_foot=br, pass_=br_ok); R["B_G1"] = dict(**bg1, pass_=bg1_ok)
    if not br_ok:
        R["void_reasons"].append("B-R: alpha = 0 does not reproduce CFG623")
    if not bg1_ok:
        R["void_reasons"].append("B-G1: G = 1 does not reproduce CFG623 a0.1_can")
    # B-M1: the gate acts in the merger
    r01 = rg[cfgs.index(dict(alpha=0.1, foot="can", gate="gate", **BASE))]
    tp = r01["t_peri"]; gs = np.array(r01.get("gstat") or [[0, 0, 1]], float)
    w = (gs[:, 0] >= tp - 0.3) & (gs[:, 0] <= tp + 0.6) if tp is not None else np.zeros(len(gs), bool)
    off = float(gs[w, 1].sum() / max(gs[w, 2].sum(), 1)) if w.any() else 0.0
    c623 = json.load(open(os.path.join(C623, "cfg623_results.json")))["cells"]["0.1_can"]
    c639 = cells["0.1_can"]
    df = abs(c639.get("f", np.nan) - c623.get("f", np.nan))
    db = abs(c639.get("beta_bar", c639.get("beta_bar_reported", np.nan)) - c623.get("beta_bar", c623.get("beta_bar_reported", np.nan)))
    m1_ok = off >= 0.05 and ((df > 0.02) or (db > 0.02))
    R["B_M1"] = dict(gated_off_frac_window=off, d_f=df, d_beta_bar=db, bites=bool(m1_ok))
    # footing validity at alpha = 0 (CFG623 rule)
    fv = {}
    for f in FEET:
        s0 = cells[f"0_{f}"]
        fv[f] = bool(s0.get("speed_kms") is not None and abs(s0["speed_kms"] - M.V_TARGET) <= M.V_TOL and abs(s0["dSG"] - M.DSG_OBS) <= M.DSG_TOL)
    R["footing_validity_alpha0"] = fv
    st = lambda a, f: "VOID" if not fv[f] else cells[f"{M.astr(a)}_{f}"]["status"]
    P("\nPER-NODE (gated):")
    for f in FEET:
        for a in NODES:
            s = cells[f"{M.astr(a)}_{f}"]
            P(f"  alpha {M.astr(a):>5s} {f}: f {s.get('f', float('nan')):+.3f} Z_B {s.get('Z_B', float('nan')):+.2f} "
              f"bbar {s.get('beta_bar', s.get('beta_bar_reported', float('nan'))):+.3f} Z_H {s.get('Z_H', float('nan')):+.2f} -> {st(a, f)}")
    hi = [a for a in NODES if a >= 0.1]
    both = lambda a: all(st(a, f) == "ALLOWED" for f in FEET)
    scor_both = [a for a in hi if all(st(a, f) in ("ALLOWED", "EXCLUDED") for f in FEET)]
    V = {}
    if any(both(a) for a in hi):
        V["VG1_merger_rescue"] = "RESCUES"
    elif scor_both and all(any(st(a, f) == "EXCLUDED" for f in FEET) for a in hi if a in scor_both) and \
            all(not both(a) for a in hi):
        V["VG1_merger_rescue"] = "DOES NOT RESCUE"
    else:
        V["VG1_merger_rescue"] = "UNDETERMINED"
    fa = os.path.join(HERE, "cfg639_galaxy_results.json")
    A = json.load(open(fa))["label"] if os.path.exists(fa) else "MISSING"
    if A.startswith("VOID") or A.startswith("NOT DIAGNOSTIC") or A == "MISSING":
        V["VG2_one_alpha"] = f"UNDETERMINED (Part A: {A})"
    elif both(1.0) and A == "A-PASS":
        V["VG2_one_alpha"] = "COMPATIBLE"
    elif any(both(a) for a in (0.3, 3.0)) and A == "A-PASS":
        V["VG2_one_alpha"] = "PARTIAL"
    else:
        V["VG2_one_alpha"] = "INCOMPATIBLE (" + ("Part A fails" if A != "A-PASS" else "merger side") + ")"
    if not m1_ok:
        V = {k: f"NOT DIAGNOSTIC (B-M1: gate does not act); as-run {v}" for k, v in V.items()}
    R["verdicts"] = V; R["part_A_label"] = A
    R["status"] = "VALID" if not R["void_reasons"] else "VOID"
    R["allowed_set"] = {f: [M.astr(a) for a in NODES if st(a, f) == "ALLOWED"] for f in FEET}
    P(f"\nB-R {br} -> {br_ok}\nB-G1 {bg1} -> {bg1_ok}\nB-M1 {R['B_M1']}\nfooting validity {fv}")
    P(f"ALLOWED: {R['allowed_set']}\nVERDICTS ({R['status']}): {V}")
    R["wall_s"] = time.time() - T0
    json.dump(M._round(R), open(os.path.join(HERE, "cfg639_merger_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg639_merger.out"), "w").write("\n".join(M.OUT) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
