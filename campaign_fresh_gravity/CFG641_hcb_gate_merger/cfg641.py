#!/usr/bin/env python3
"""CFG640 (FROZEN_CRITERIA.md, 4b928d160): H-CB (stars-only phantom source) + the CFG639 deficit gate in CFG623's merger stopwatch.

Read-only re-use: CFG623's pipeline and scores (via CFG639's cfg639_merger, which also supplies the gated settle step Sim639) and
CFG621's calibrate().  Changes, all from the criteria:
  * progenitors: settled cold energy = stars-only phantom (truncated at r_t), plus a collisionless reservoir RN (NFW c = 4 in
    r200, 5.364 M_b - settled) or RI (cold(<r) = max(settled, 5.364 M_b(<r))); gas pressure re-solved in the new total mass;
  * settle-step phantom field: stars-only particles (no gas grid, no cool-core cloud);
  * (v0, eta) re-fit per reservoir rule by CFG621's calibrate().
cfg keys: src 'all' | 'stars', res 'R0' | 'RN' | 'RI', gate 'gate' | 'none'.  src='all', res='R0', gate='none' is CFG623 exactly.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not "theory closed".
Run (heavy, ~10 GB over 4 processes): only via run_640.sh.
"""
import os, sys, json, math, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG639_deficit_gated_mobility"))
sys.path.insert(0, os.path.join(HERE, "..", "CFG621_merger_stopwatch_v3"))
import cfg639_merger as B   # noqa: E402  (read-only; imports CFG623's main as B.M and defines Sim639)
import cfg621_main as C     # noqa: E402  (read-only; calibrate())
import cfg621_sim as S621   # noqa: E402
M, S, L, S599 = B.M, B.S, B.L, B.S599
RB, RBC = S599.RB, S599.RBC
C623 = B.C623
COLD = 5.364
NODES = [0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
FEET = ["can", "alt"]
CTX = {"src": "all", "res": "R0"}          # progenitor context (set per Sim before the progenitors are built)
CAL_ARM = {"src": "all", "res": "R0"}      # default for CFG621's calib cfgs, which carry no src/res keys
RUNS = os.path.join(HERE, "runs"); os.makedirs(RUNS, exist_ok=True)
_P599 = L.Progenitor599
_name623 = B._name623


# ------------------------------------------------------------------------------------------------ progenitors (criteria 1.1-1.2)
class ProgH(_P599):
    def __init__(self, M200, foot, swap=False, cloud=False, **kw):
        super().__init__(M200, foot, swap=swap, cloud=cloud, **kw)
        src, res = CTX["src"], CTX["res"]
        self.src, self.res = src, res
        if src == "all" and res == "R0":
            return                                              # CFG599's progenitor, untouched
        r = self.r
        Mph = L.phantom_mass(r, self.Ms if src == "stars" else self.Mbar, self.a0)
        Mt = float(np.interp(self.rt, r, Mph))
        Mset = np.where(r < self.rt, Mph, Mt)
        if res == "R0":
            Mcold = Mset
        elif res == "RN":
            Mu = max(COLD * self.Mb - Mt, 0.0)
            rs = self.r200 / 4.0
            nfw = np.where(r < self.r200, 1.0 / (np.maximum(r, 1e-3) / rs * (1 + r / rs) ** 2), 0.0)
            Mn = L.cumtrapz_sph(r, nfw)
            Mcold = Mset + Mu * Mn / Mn[-1]
        elif res == "RI":
            Mcold = np.maximum(Mset, COLD * self.Mbar)
        else:
            raise ValueError(res)
        Mcold = np.maximum.accumulate(Mcold)
        self.settled_tot = Mt; self.reservoir_tot = float(Mcold[-1] - Mt)
        self.Mph = Mcold
        self.rho_ph = np.maximum(np.gradient(Mcold, r) / (4 * math.pi * np.maximum(r, 1e-3) ** 2), 0.0)
        self.Mph_tot = float(Mcold[-1])
        self.Mtot = self.Mbar + self.Mph
        gN = L.G * self.Mtot / np.maximum(r, 1e-3) ** 2
        integrand = self.rho_g * gN
        P = np.zeros_like(r)
        P[-1] = self.rho_g[-1] * 0.5 * L.G * self.Mtot[-1] / r[-1]
        for k in range(len(r) - 2, -1, -1):
            P[k] = P[k + 1] + 0.5 * (integrand[k] + integrand[k + 1]) * (r[k + 1] - r[k])
        self.P = P


def prog_factory(M200, foot, swap=False, cloud=False, **kw):
    return ProgH(M200, foot, swap=swap, cloud=cloud, **kw)


# ------------------------------------------------------------------------------------------------ simulator (criteria 1.1b, 1.3)
class SimH(B.Sim639):
    def __init__(self, cfg):
        self.src = cfg.get("src", CAL_ARM["src"]); self.res = cfg.get("res", CAL_ARM["res"])
        CTX["src"], CTX["res"] = self.src, self.res
        super().__init__(cfg)

    def phantom_field(self):
        if self.src == "all":
            return super().phantom_field()
        g = self.g
        out = np.zeros(g.n)
        for k, p in enumerate(self.progs):
            sel = self.is_s & (self.tag == k)                   # condensed baryons only: stars
            xs, ms = self.x[sel], self.m[sel]
            c = self.xb[k].copy()
            for _ in range(3):
                ds = np.linalg.norm(xs - c, axis=1) < p.rt
                Mi = ms[ds].sum()
                c = (ms[ds, None] * xs[ds]).sum(0) / Mi if Mi > 0 else c
            self.xb[k] = c
            r = g.radius_from(c)
            hb = np.histogram(np.linalg.norm(xs - c, axis=1), RB, weights=ms)[0]
            Mcum = np.concatenate([[0.0], np.cumsum(hb)])
            rho_ph, Mt = L.phantom_profile_from_mass(RB, Mcum, self.a0, p.rt)
            f = np.interp(r, RBC, rho_ph, right=0.0) * (r < p.rt)
            s = f.sum() * g.dV
            if s > 0:
                f *= Mt / s
            out += f
        return out


def name_of(c):
    s = _name623(c)
    if "src" in c:
        s += f"_{c['src']}_{c['res']}_g{c.get('gate', 'gate')}"
    return s


def worker(c):
    import cfg622_sim as SS
    fn = os.path.join(M.RUNS, name_of(c) + ".json")
    if os.path.exists(fn):
        return
    cc = dict(c); cc["v0"] = cc["v0_kms"] * L.KMS
    B.STATS.clear()
    res = SS.run(cc)
    res["gstat"] = B.STATS.get("gstat", [])
    json.dump(M._round(res), open(fn + ".tmp", "w")); os.replace(fn + ".tmp", fn)


# patches (in-process only; every patched object is read-only code from CFG599/621/622/623/639)
L.Progenitor599 = prog_factory
S.Sim = SimH
S621.Sim = SimH
M.RUNS = RUNS; M.name_of = name_of; M.worker = worker


def max_diff(r, o):
    return B.max_diff(r, o)


def calibrate(res):
    CAL_ARM["src"], CAL_ARM["res"] = "stars", res
    C.RUNS = os.path.join(HERE, f"runs_calib_{res}"); os.makedirs(C.RUNS, exist_ok=True)
    fn = os.path.join(HERE, f"cfg640_calibration_{res}.json")
    if os.path.exists(fn):
        return json.load(open(fn))
    cal = C.calibrate()
    json.dump(M._round(cal), open(fn, "w"), indent=1, default=float)
    return cal


def arm(src, res, gate, cal):
    base = dict(v0_kms=float(round(cal["v0_kms"], 1)), eta=float(f"{cal['eta']:.4g}"))
    cfgs = [dict(alpha=a, foot=f, src=src, res=res, gate=gate, **base) for f in FEET for a in NODES]
    runs = M.pool_map(cfgs)
    cells = {f"{M.astr(c['alpha'])}_{c['foot']}": M.score_run(r) for c, r in zip(cfgs, runs)}
    fv = {}
    for f in FEET:
        s0 = cells[f"0_{f}"]
        fv[f] = bool(s0.get("speed_kms") is not None and abs(s0["speed_kms"] - M.V_TARGET) <= M.V_TOL and abs(s0["dSG"] - M.DSG_OBS) <= M.DSG_TOL)
    st = {k: ("VOID" if not fv[k.split("_")[1]] else v["status"]) for k, v in cells.items()}
    return dict(cfgs=cfgs, runs=runs, cells=cells, footing_validity=fv, status=st, base=base)


def both_allowed(A, a):
    return all(A["status"][f"{M.astr(a)}_{f}"] == "ALLOWED" for f in FEET)


def vh1(A):
    hi = [a for a in NODES if a >= 0.1]
    if any(both_allowed(A, a) for a in hi):
        return "RESCUES"
    if any(all(A["status"][f"{M.astr(a)}_{f}"] in ("ALLOWED", "EXCLUDED") for f in FEET) for a in hi):
        return "DOES NOT RESCUE"
    return "UNDETERMINED"


def main():
    T0 = time.time()
    P = M.P
    P("CFG640: H-CB (stars-only source) + deficit gate in CFG623's merger stopwatch (criteria 4b928d160)")
    R = {"lane": "CFG640", "criteria": "4b928d160", "void_reasons": []}
    # T-H static
    th = {}
    for f in FEET:
        CTX["src"], CTX["res"] = "all", "R0"; pa = ProgH(1.5e15, f)
        CTX["src"], CTX["res"] = "stars", "R0"; ps = ProgH(1.5e15, f)
        th[f] = ps.Mph_tot / pa.Mph_tot
    R["T_H"] = dict(ratio=th, pass_=all(v < 0.5 for v in th.values()))
    prog = {}
    for res in ("RN", "RI"):
        for f in FEET:
            for nm, M200, cl in (("main", 1.5e15, False), ("sub", 1.5e14, True)):
                CTX["src"], CTX["res"] = "stars", res; p = ProgH(M200, f, cloud=cl)
                prog[f"{res}_{f}_{nm}"] = dict(settled=p.settled_tot, reservoir=p.reservoir_tot, Mb=p.Mb, Mtot_end=float(p.Mtot[-1]))
    R["progenitors"] = prog
    P("progenitor masses (settled / reservoir / M_b): " + json.dumps({k: [f"{v['settled']:.3e}", f"{v['reservoir']:.3e}", f"{v['Mb']:.3e}"] for k, v in prog.items()}))
    P(f"T-H stars-only / all-baryon settled mass (main, inside r_t): {th}")
    # controls C-R0, C-R1 (CFG623 calibration)
    c0 = dict(alpha=0.0, foot="can", src="all", res="R0", gate="none", **M.BASE)
    c1 = dict(alpha=0.1, foot="can", src="all", res="R0", gate="none", **M.BASE)
    rc = M.pool_map([c0, c1])
    o0 = json.load(open(os.path.join(C623, "runs", _name623(dict(alpha=0.0, foot="can", **M.BASE)) + ".json")))
    o1 = json.load(open(os.path.join(C623, "runs", _name623(dict(alpha=0.1, foot="can", **M.BASE)) + ".json")))
    d0, d1 = max_diff(rc[0], o0), max_diff(rc[1], o1)
    R["C_R0"], R["C_R1"] = d0, d1
    ctrl_ok = d0["max_diff_kpc"] == 0.0 and d1["max_diff_kpc"] == 0.0
    P(f"C-R0 {d0}  C-R1 {d1} -> {'PASS' if ctrl_ok else 'FAIL'}")
    if not ctrl_ok:
        R["void_reasons"].append("C-R0/C-R1 do not reproduce CFG623")
        R["status"] = "VOID"; json.dump(M._round(R), open(os.path.join(HERE, "cfg640_results.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, "cfg640.out"), "w").write("\n".join(M.OUT) + "\n"); return 1
    arms = {}
    for res, tags in (("RN", (("P", "gate"), ("U", "none"))), ("RI", (("S", "gate"),))):
        P(f"\nCALIBRATION {res} (CFG621 calibrate(), alpha = 0, canonical)")
        cal = calibrate(res)
        R[f"calibration_{res}"] = {k: v for k, v in cal.items() if k != "log"}
        P(f"  -> {R[f'calibration_{res}']}")
        for tag, gate in tags:
            if not cal.get("ok"):
                arms[tag] = None; R["void_reasons"].append(f"arm {tag}: calibration {res} failed ({cal.get('reason')})"); continue
            A = arm("stars", res, gate, cal)
            arms[tag] = A
            P(f"\nARM {tag} (stars, {res}, gate {gate}; v0 {A['base']['v0_kms']}, eta {A['base']['eta']}); footing validity {A['footing_validity']}")
            for f in FEET:
                for a in NODES:
                    s = A["cells"][f"{M.astr(a)}_{f}"]
                    P(f"  alpha {M.astr(a):>5s} {f}: f {s.get('f', float('nan')):+.3f} Z_B {s.get('Z_B', float('nan')):+.2f} "
                      f"bbar {s.get('beta_bar', s.get('beta_bar_reported', float('nan'))):+.3f} Z_H {s.get('Z_H', float('nan')):+.2f} "
                      f"-> {A['status'][f'{M.astr(a)}_{f}']}")
    V = {}
    Pm, U, Sx = arms.get("P"), arms.get("U"), arms.get("S")
    if Pm:
        V["VH1_combo_rescues"] = vh1(Pm)
        V["VH1_alpha0_still_allowed"] = both_allowed(Pm, 0.0)
        V["VH2_alpha1_merger_side"] = ("MERGER SIDE COMPATIBLE AT alpha = 1 (full one-alpha verdict conditional on CFG639 Part A, NOT DIAGNOSTIC)"
                                       if both_allowed(Pm, 1.0) else
                                       "allowed set: " + str([M.astr(a) for a in NODES if both_allowed(Pm, a)]))
        # T-G
        r01 = Pm["runs"][Pm["cfgs"].index(next(c for c in Pm["cfgs"] if c["alpha"] == 0.1 and c["foot"] == "can"))]
        tp = r01["t_peri"]; gs = np.array(r01.get("gstat") or [[0, 0, 1]], float)
        w = (gs[:, 0] >= tp - 0.3) & (gs[:, 0] <= tp + 0.6) if tp is not None else np.zeros(len(gs), bool)
        off = float(gs[w, 1].sum() / max(gs[w, 2].sum(), 1)) if w.any() else 0.0
        tg = dict(gated_off_frac_window=off)
        if U:
            cp, cu = Pm["cells"]["0.1_can"], U["cells"]["0.1_can"]
            bb = lambda s: s.get("beta_bar", s.get("beta_bar_reported", float("nan")))
            tg.update(d_f=abs(cp.get("f", np.nan) - cu.get("f", np.nan)), d_beta_bar=abs(bb(cp) - bb(cu)))
            tg["bites"] = bool(off >= 0.05 and (tg["d_f"] > 0.02 or tg["d_beta_bar"] > 0.02))
            hiP = [a for a in NODES if a >= 0.1 and both_allowed(Pm, a)]
            hiU = [a for a in NODES if a >= 0.1 and both_allowed(U, a)]
            if any(a not in hiU for a in hiP):
                v3 = "GATE NEEDED"
            elif hiP and all(a in hiU for a in hiP):
                v3 = "H-CB SUFFICES"
            elif not hiP and not hiU:
                v3 = "NO RESCUE EITHER WAY"
            else:
                v3 = "MIXED"
            V["VH3_attribution"] = v3 if tg["bites"] else f"NOT DIAGNOSTIC (T-G); as-run {v3}"
            V["VH3_status_changes"] = {k: (U["status"][k], Pm["status"][k]) for k in Pm["status"] if U["status"][k] != Pm["status"][k]}
        R["T_G"] = tg
        if Sx:
            V["VH4_reservoir"] = "RESERVOIR-DEPENDENT" if vh1(Sx) != V["VH1_combo_rescues"] else "SAME UNDER RN AND RI"
            V["VH4_S_VH1"] = vh1(Sx)
    else:
        V["VH1_combo_rescues"] = "VOID (primary arm not run: calibration RN failed)"
    R["verdicts"] = V
    R["arms"] = {t: (None if A is None else dict(base=A["base"], footing_validity=A["footing_validity"], status=A["status"], cells=A["cells"]))
                 for t, A in arms.items()}
    R["status"] = "VALID" if not R["void_reasons"] else ("PARTIAL" if Pm else "VOID")
    P(f"\nVERDICTS ({R['status']}): {json.dumps(V, default=str)}")
    R["wall_s"] = time.time() - T0
    json.dump(M._round(R), open(os.path.join(HERE, "cfg640_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg640.out"), "w").write("\n".join(M.OUT) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
