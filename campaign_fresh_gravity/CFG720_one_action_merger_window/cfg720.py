#!/usr/bin/env python3
"""CFG720 (FROZEN_CRITERIA.md, 7687ef48c): the one-action construction C* on the merger stopwatch (response-time window).

CFG623's pipeline imported read-only; field mode (CFG599 alpha = inf: the cold mass is a grid field from each progenitor's own baryons,
round rule inside r_t); C*'s static kernel nu_s(y) = 1/2 + sqrt(1/4 + 1/y) swapped in for nu_mono (cfg597_lib.nu_mono, the only kernel
hook); the field relaxes toward its target with response time t_resp (overdamped stand-in for C*'s inertia).  (v0, eta) re-fit with
CFG621's calibrate() in field mode, nu_s, t_resp = 0.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not "theory closed".
Run (heavy): only via run_720.sh.  CFG720_MUTATE=1 -> _MUTATE outputs."""
import os, sys, json, math, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
C623 = os.path.join(LANES, "CFG623_merger_stopwatch_v5")
sys.path.insert(0, C623); sys.path.insert(0, os.path.join(LANES, "CFG621_merger_stopwatch_v3"))
import cfg623_main as M    # noqa: E402  (read-only)
import cfg622_sim as S     # noqa: E402
import cfg621_main as C    # noqa: E402
import cfg621_sim as S621  # noqa: E402
import cfg599_sim as S599  # noqa: E402
import cfg597_lib as L597  # noqa: E402
L = M.L
MUT = os.environ.get("CFG720_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
NU_MONO = L597.nu_mono


def nu_s(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


NODES = [0.0, 0.1, 0.3, 1.0, 3.0]
FEET = ["can", "alt"]
CAL = {"kernel": "s", "t_resp": 0.0}
LAG = {}
RUNS = os.path.join(HERE, "runs"); os.makedirs(RUNS, exist_ok=True)
_name623 = M.name_of


class Sim720(S.Sim):
    def __init__(self, cfg):
        self.kernel = cfg.get("kernel", CAL["kernel"]); self.t_resp = float(cfg.get("t_resp", CAL["t_resp"]))
        L597.nu_mono = nu_s if self.kernel == "s" else NU_MONO
        self.lagdiag = []
        super().__init__(cfg)

    def _sub_centroid(self, F):
        X = self.g.xc[0]
        mid = 0.5 * (self.xb[0][0] + self.xb[1][0]) if len(self.xb) > 1 else 0.0
        w = F * (X[:, None, None] > mid)
        tot = w.sum()
        return float((w.sum((1, 2)) * X).sum() / tot) if tot > 0 else float("nan")

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
        target = self.phantom_field()
        if self.t_resp <= 0:
            self.field_cs = target
        else:
            self.field_cs = self.field_cs + (target - self.field_cs) * (1.0 - math.exp(-dt / self.t_resp))
        if len(self.diag) and (len(self.lagdiag) == 0 or self.t - self.lagdiag[-1][0] >= 0.02):
            self.lagdiag.append((self.t, self._sub_centroid(self.field_cs), self._sub_centroid(target)))
            LAG["d"] = self.lagdiag
        self.t += dt


def name_of(c):
    s = _name623(c)
    if "kernel" in c:
        s += f"_k{c['kernel']}_tr{c['t_resp']:g}"
    return s


def worker(c):
    import cfg622_sim as SS
    fn = os.path.join(M.RUNS, name_of(c) + ".json")
    if os.path.exists(fn):
        return
    cc = dict(c); cc["v0"] = cc["v0_kms"] * L.KMS
    LAG.clear()
    res = SS.run(cc)
    res["lagdiag"] = LAG.get("d", [])
    json.dump(M._round(res), open(fn + ".tmp", "w")); os.replace(fn + ".tmp", fn)


def calib_cfg(v0, eta, foot="can"):
    return dict(alpha=math.inf, foot=foot, v0_kms=float(round(v0, 1)), eta=float(f"{eta:.4g}"), mode="calib")


S.Sim = Sim720; S621.Sim = Sim720
M.RUNS = RUNS; M.name_of = name_of; M.worker = worker
C.calib_cfg = calib_cfg


def max_diff(r, o):
    n = min(len(o["diag"]), len(r["diag"])); mx = 0.0
    for i in range(n):
        for key in ("gal", "gas", "lens", "lens_nomask"):
            mx = max(mx, float(np.hypot(*(np.array(r["diag"][i]["sub"][key]) - np.array(o["diag"][i]["sub"][key])))))
        for a, b in zip(r["diag"][i]["sub"]["lens_alts"], o["diag"][i]["sub"]["lens_alts"]):
            mx = max(mx, float(np.hypot(*(np.array(a) - np.array(b)))))
    return dict(n_epochs=[len(o["diag"]), len(r["diag"])], max_diff_kpc=mx)


def main():
    T0 = time.time(); P = M.P
    P("CFG720: one-action construction C* on the merger stopwatch (criteria 7687ef48c)" + (" [MUTATE]" if MUT else ""))
    R = {"lane": "CFG720", "criteria": "7687ef48c", "mutate": MUT, "void_reasons": []}
    # C-R: nu_mono, t_resp 0, CFG621 calibration reproduces CFG623 ainf_can
    cr = dict(alpha=math.inf, foot="can", kernel="mono", t_resp=0.0, **M.BASE)
    rcr = M.pool_map([cr])[0]
    o = json.load(open(os.path.join(C623, "runs", _name623(dict(alpha=math.inf, foot="can", **M.BASE)) + ".json")))
    R["C_R"] = max_diff(rcr, o)
    P(f"C-R (nu_mono, t_resp 0) vs CFG623 ainf_can: {R['C_R']}")
    if R["C_R"]["max_diff_kpc"] != 0.0:
        R["void_reasons"].append("C-R fails")
    # calibration (field mode, nu_s, t_resp 0)
    C.RUNS = os.path.join(HERE, "runs_calib"); os.makedirs(C.RUNS, exist_ok=True)
    fcal = os.path.join(HERE, "cfg720_calibration.json")
    if os.path.exists(fcal):
        cal = json.load(open(fcal))
    else:
        CAL.update(kernel="s", t_resp=0.0)
        cal = C.calibrate(); json.dump(M._round(cal), open(fcal, "w"), indent=1, default=float)
    R["calibration"] = {k: v for k, v in cal.items() if k != "log"}
    P(f"calibration (field mode, nu_s): {R['calibration']}")
    if not cal.get("ok"):
        R["void_reasons"].append(f"calibration failed ({cal.get('reason')})")
        R["status"] = "VOID"; json.dump(M._round(R), open(os.path.join(HERE, f"cfg720_results{TAG}.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, f"cfg720{TAG}.out"), "w").write("\n".join(M.OUT) + "\n"); return 1
    base = dict(v0_kms=float(round(cal["v0_kms"], 1)), eta=float(f"{cal['eta']:.4g}"))
    cfgs = [dict(alpha=math.inf, foot=f, kernel="s", t_resp=t, **base) for f in FEET for t in NODES]
    extra = []
    if MUT:
        extra = [dict(alpha=math.inf, foot="can", kernel="s", t_resp=0.0, **M.BASE),
                 dict(alpha=math.inf, foot="can", kernel="s", t_resp=100.0, **base)]
    runs = M.pool_map(cfgs + extra)
    rg = runs[:len(cfgs)]
    cells = {f"{c['t_resp']:g}_{c['foot']}": M.score_run(r) for c, r in zip(cfgs, rg)}
    fv = {}
    for f in FEET:
        s0 = cells[f"0_{f}"]
        fv[f] = bool(s0.get("speed_kms") is not None and abs(s0["speed_kms"] - M.V_TARGET) <= M.V_TOL and abs(s0["dSG"] - M.DSG_OBS) <= M.DSG_TOL)
    st = lambda t, f: "VOID" if not fv[f] else cells[f"{t:g}_{f}"]["status"]
    P(f"\nfooting validity at t_resp = 0: {fv}")
    for f in FEET:
        for t in NODES:
            s = cells[f"{t:g}_{f}"]
            P(f"  t_resp {t:>4g} Gyr {f}: f {s.get('f', float('nan')):+.3f} Z_B {s.get('Z_B', float('nan')):+.2f} "
              f"bbar {s.get('beta_bar', s.get('beta_bar_reported', float('nan'))):+.3f} Z_H {s.get('Z_H', float('nan')):+.2f} -> {st(t, f)}")
    # C-L: lag acts (t_resp 1 Gyr, canonical): field-target sub centroid offset at the first epoch after pericentre
    r1 = rg[cfgs.index(dict(alpha=math.inf, foot="can", kernel="s", t_resp=1.0, **base))]
    tp = r1["t_peri"]; ld = [row for row in r1.get("lagdiag", []) if tp is not None and row[0] >= tp]
    off = abs(ld[0][1] - ld[0][2]) if ld else float("nan")
    R["C_L"] = dict(offset_kpc=off, acts=bool(off > 20))
    P(f"C-L (lag acts, t_resp 1 Gyr can): field-target sub centroid offset after pericentre = {off:.1f} kpc -> {R['C_L']['acts']}")
    both = lambda t: all(st(t, f) == "ALLOWED" for f in FEET)
    V = {"VR1_quasistatic": {f: st(0.0, f) for f in FEET}}
    allowed = [t for t in NODES if both(t)]
    V["VR2_window"] = (f"mergers require t_resp >= {min(allowed):g} Gyr" if allowed else "NO WINDOW UP TO 3 Gyr")
    if not allowed:
        V["VR3_galaxy"] = "INCOMPATIBLE"
    else:
        V["VR3_galaxy"] = "COMPATIBLE" if min(allowed) <= 1.0 else "TENSION"
    if not R["C_L"]["acts"]:
        V["VR2_window"] = "NOT DIAGNOSTIC (C-L: lag does not act); as-run " + V["VR2_window"]
    R.update(cells=cells, footing_validity=fv, verdicts=V, base=base)
    if MUT:
        rk = runs[len(cfgs)]; r100 = runs[len(cfgs) + 1]
        m1 = max_diff(rk, rcr)["max_diff_kpc"] > 5.0
        s100 = M.score_run(r100); f0 = cells["0_can"].get("f", float("nan"))
        m2 = s100.get("f", float("nan")) < f0 - 0.2
        R["MUTATE"] = dict(M1_kernel_acts=bool(m1), M2_frozen_field=bool(m2), f_100=s100.get("f"), f_0=f0)
        P(f"MUTATE: M1 kernel swap acts {m1}; M2 huge lag lowers f (f_100 {s100.get('f')}, f_0 {f0}) {m2}")
    R["status"] = "VALID" if not R["void_reasons"] else "VOID"
    P(f"\nVERDICTS ({R['status']}): {json.dumps(V)}")
    R["wall_s"] = time.time() - T0
    json.dump(M._round(R), open(os.path.join(HERE, f"cfg720_results{TAG}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg720{TAG}.out"), "w").write("\n".join(M.OUT) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
