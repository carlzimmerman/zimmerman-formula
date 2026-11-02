#!/usr/bin/env python3
"""DR8 part B reader (FROZEN_CRITERIA.md): live Q against Blumenthal, RULE, RULE_F, Gnedin and the exact isotropic adiabatic calculation, seed pairs at the end; stability; verdict. kappa = 1/2 FITTED, unused; not theory closed."""
import glob, json, math, os, sys
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(REB, "LC1_live_contraction"))
_a = sys.argv; sys.argv = [_a[0]]; import lc1_read as LR; sys.argv = _a
import dr8_ic as IC, dr8_rule as RU, dr8_action as AC, dr8_live as DL
S = IC.setup(); Rd, r0 = S["Rd"], S["r0"]; EPS = DL.EPS; G = IC.G; OUT = []; RUNS = os.path.join(HERE, "runs"); TEND = 7.7
def P(s): print(s, flush=True); OUT.append(str(s))
RDG = np.array([1, 2, 2.2, 3, 4, 6, 8, 10.0]); XR0 = np.array([0.135, 0.25, 0.5, 1, 2, 4, 8.0]); IW = [1, 3, 4]; RHO0 = LR.Om * LR.rho_c(0.0)
def bs(v): return 4 * (np.arcsinh(v) - v / np.sqrt(1 + v * v))
def centre(xx, c, m, how): return DL.centre_com(xx, r0, c) if how == "com" else LR.XA.centre(xx, m)
def preds(rB, m0, Md, Msim, R2, kind, xs=None, vs=None, Mtab=None):
    """Blumenthal, Gnedin, RULE, RULE_F on one start: rB sorted radii of the no-disc state (or Mtab = (rg, M total) analytic)."""
    f = Md / Msim; F = Md / (Msim - Md); rg = np.geomspace(1e-5, float(rB[-1]), 6000)
    Mtot0 = m0 * np.searchsorted(rB, rg) if Mtab is None else np.interp(np.log(rg), np.log(Mtab[0]), Mtab[1], left=0.0); M0 = (1 - f) * Mtot0; Mb = Md * (1 - Rd / np.sqrt(rg ** 2 + Rd ** 2)); B_ = LR.contract(rg, Mb, M0, F); Gn = LR.contract(rg, Mb, M0, F, gnedin=(0.85, 0.8, R2)); o = dict(rg=rg, M0=M0, QB=B_[0], QG=Gn[0], cv=max(B_[1], Gn[1]))
    if kind == "core":
        Mr0 = float(np.interp(math.log(r0), np.log(rg), M0)); C = Mr0 / float(bs(np.asarray(1.0))); a = RU.rule(rg, Mb, M0, F, "RULE", r0=r0, C=C); b = RU.rule(rg, Mb, M0, F, "RULE_F", r0=r0, C=C); o.update(QR=a[0], QRF=b[0], cross=[a[2], b[2]], edge=float(a[3][-1] / rg[-1]))
    return o
def evalQ(o, rr): x = np.log(rr); m0 = np.interp(x, np.log(o["rg"]), o["M0"]); return {k: (np.interp(x, np.log(o["rg"]), o[k]) / m0).tolist() for k in ("QB", "QG", "QR", "QRF", "QA") if k in o}
def run_name(kind, s, tag=""): return os.path.join(RUNS, f"{kind}_s{s}{tag}")
def one(kind, s, how, tag="", Mtab=None, act=True):
    fd = os.path.join(run_name(kind, s, tag), f"snap_t{TEND:.2f}.npz"); fn = os.path.join(run_name(kind, s, "_nodisc"), f"snap_t{TEND:.2f}.npz")
    if not (os.path.exists(fd) and os.path.exists(fn)): return None
    A, B = np.load(fd), np.load(fn); ma = json.loads(str(A["meta"])); mb = json.loads(str(B["meta"])); m0 = float(B["m"]); Md = ma["Md_now"]; Msim = ma["Msim"]; assert abs(m0 * len(B["x"]) / Msim - 1) < 1e-9; m1 = m0 * (1 - Md / Msim)
    cA, cB = centre(A["x"], A["c"], m1, how), centre(B["x"], B["c"], m0, how); rA = np.sort(np.linalg.norm(A["x"] - cA, axis=1)); rB = np.sort(np.linalg.norm(B["x"] - cB, axis=1)); rr = np.concatenate((RDG * Rd, XR0 * r0)); Q = np.searchsorted(rA, rr) / np.maximum(np.searchsorted(rB, rr), 1); R2 = LR.r200(rB, m0, 0.0)
    o = preds(rB, m0, Md, Msim, R2, kind); Qs = evalQ(o, rr)
    res = dict(Q=Q.tolist(), Nno=np.searchsorted(rB, rr).tolist(), R200=R2, jump_rms=ma["jump_rms"], jump_max=ma["jump_max"], cross=o.get("cross"), edge=o.get("edge"), **Qs)
    try:
        fA, fB = LR.S_fit(A["x"], m1, RHO0, EPS), LR.S_fit(B["x"], m0, RHO0, EPS); res["R_live"] = fA["S"] / fB["S"] if fA and fB else None; res["a_nodisc"], res["c_nodisc"], res["c_disc"] = (fB["a"], fB["c"], fA["c"]) if fA and fB else (None, None, None)
    except Exception as e: res["R_live"] = None; res["fit_err"] = repr(e)
    if act:
        Z = np.load(os.path.join(run_name(kind, s, "_nodisc"), "ic.npz")); x0, v0 = Z["x"], Z["v"]; Mod = IC.build(kind, S, 100, 1, ma["rdec"])[4]; rg = np.geomspace(max(Mod.r[0], 2e-5), Mod.r[-1] * 3, 2500); Mi = np.interp(np.log(rg), np.log(Mod.r), Mod.M); Mi = np.where(rg < Mod.r[0], Mod.M[0], Mi); Mb = Md * (1 - Rd / np.sqrt(rg ** 2 + Rd ** 2)); Mf, ch, _, _ = AC.respond(x0, v0, rg, Mi, Mb, 1 - Md / Msim, m0, passes=8); o2 = dict(rg=rg, M0=Mi * (1 - Md / Msim), QA=Mf); res["QA"] = evalQ(o2, rr)["QA"]; res["act_change"] = ch
        # the same predictions on the exact analytic start
        oa = preds(np.array([Mod.r[-1]]), m0, Md, Msim, S["R2"], kind, Mtab=(Mod.r, Mod.M)); res["analytic"] = evalQ(oa, rr)
    return res
def boot(v, fn=np.median, n=20000):
    v = np.asarray(v); rng = np.random.default_rng(1); s = fn(v[rng.integers(0, len(v), (n, len(v)))], axis=1); return [float(np.percentile(s, 2.5)), float(np.percentile(s, 97.5))]
def table(rows, keys):
    rr = list(RDG) + ["x" + str(v) for v in XR0]; O = {}
    for k in ("Q",) + keys:
        if k in rows[0]: O[k] = np.median([r[k] for r in rows], axis=0).tolist()
    return O
def frac(r, k, idx=IW): return float(np.median([(r["Q"][i] - 1) / (r[k][i] - 1) for i in idx]))
def stability(s, how):
    Zi = np.load(os.path.join(run_name("core", s, "_nodisc"), "ic.npz")); x0 = Zi["x"]; m = float(Zi["m"]); rc = np.array([0.135, 0.25, 0.5, 1, 2, 4]) * r0; c0 = centre(x0, np.median(x0, axis=0), m, how); N0 = np.searchsorted(np.sort(np.linalg.norm(x0 - c0, axis=1)), rc); O = dict(r_over_r0=(rc / r0).tolist(), N0=N0.tolist()); d = run_name("core", s, "_nodisc")
    for f in sorted(glob.glob(os.path.join(d, "snap_t*.npz"))):
        Z = np.load(f); c = centre(Z["x"], Z["c"], m, how); N = np.searchsorted(np.sort(np.linalg.norm(Z["x"] - c, axis=1)), rc); O[os.path.basename(f)[5:-4]] = np.log(N / N0).tolist()
    return O
def energy(x, v, m, chunk=64):
    U = 0.0
    for i in range(0, len(x), chunk):
        d = x[None] - x[i:i + chunk, None]; U += float(-G * m * m * (1 / np.sqrt((d * d).sum(-1) + EPS * EPS)).sum()) / 2
    U -= -G * m * m / EPS * len(x) / 2 * 1; return 0.5 * m * (v * v).sum(), U
if __name__ == "__main__":
    how = sys.argv[1] if len(sys.argv) > 1 else "com"
    P(f"DR8 part B reader; isolated halo, gravity only; centre {how}; r0 {r0*1e3:.2f} kpc, R_d {Rd*1e3:.3f} kpc, eps {EPS*1e3:.2f} kpc; kappa = 1/2 FITTED, unused; not theory closed")
    # K11 reader on LC1 seed 1
    J = json.load(open(os.path.join(REB, "LC1_live_contraction", "lc1_results.json")))["pairs"]["0.00"]["M1e12_s1_ng64"]; A_ = np.load(os.path.join(REB, "LC1_live_contraction", "runs", "M1e12_s1_ng64", "snap_z0.00.npz")); B_ = np.load(os.path.join(REB, "ZN1_zooms_to_z0", "runs", "M1e12_s1_ng64", "snap_z0.00.npz")); ma = json.loads(str(A_["meta"])); mb = json.loads(str(B_["meta"])); rho = mb["Mf"] / (4 / 3 * math.pi * mb["qM"] ** 3); pr = LR.pair(A_["x"], B_["x"], float(B_["m"]), ma["Md_now"], ma["lc1"]["Rd_kpc"] * 1e-3, ma["eps"], rho, 0.0); k11 = max(max(abs(a - b) for a, b in zip(pr[k], J[k])) for k in ("Q", "QB", "QG")); ok = k11 <= 1e-6; P(f"K11a LC1's reader on LC1 s1 vs lc1_results: {k11:.1e}: {'PASS' if ok else 'FAIL'}")
    res = {}; RES = dict(setup=S, centre=how)
    for kind, ss in (("core", (1, 2, 3, 4, 5)), ("nfw", (1, 2, 3))):
        rows = []
        for s in ss:
            r = one(kind, s, how)
            if r is not None: rows.append(r); res[f"{kind}_s{s}"] = r; P(f"{kind} s{s}: done, f_B {frac(r,'QB'):.3f}, R_live {r.get('R_live')}, jump rms {r['jump_rms']*1e3:.3f} kpc, act change {r.get('act_change')}")
        if not rows: continue
        keys = tuple(k for k in ("QB", "QG", "QR", "QRF", "QA") if k in rows[0]); T = table(rows, keys); RES[kind] = dict(n=len(rows), table=T, radii_Rd=RDG.tolist(), radii_r0=XR0.tolist())
        if "analytic" in rows[0]: RES[kind]["analytic"] = {k: np.median([r["analytic"][k] for r in rows], axis=0).tolist() for k in rows[0]["analytic"]}
        P(f"\n=== {kind}: {len(rows)} pairs; r/R_d {RDG.tolist()} then r/r0 {XR0.tolist()}")
        for k, v in T.items(): P(f"  {k:4s} " + " ".join(f"{q:.3f}" for q in v))
        P("  N_nodisc " + " ".join(f"{q:.0f}" for q in np.median([r["Nno"] for r in rows], axis=0)))
        fs = {}
        for k in keys[0:] :
            v = [frac(r, k) for r in rows]; fs[k] = dict(med=float(np.median(v)), ci95=boot(v), by_seed=v); P(f"  f_{k[1:]} (2,3,4 R_d) {fs[k]['med']:.3f} {fs[k]['ci95']}; by seed " + " ".join(f"{x:.2f}" for x in v))
        RES[kind]["f"] = fs; n = len(RDG) + len(XR0); per = {}
        for k in keys:
            q = np.array([[(r["Q"][i] - 1) / (r[k][i] - 1) for i in range(n)] for r in rows]); per[k] = dict(med=np.median(q, axis=0).tolist(), ci95=[boot(q[:, i]) for i in range(n)]); P(f"  (Q-1)/({k}-1) by radius " + " ".join(f"{x:.2f}" for x in per[k]["med"]))
        RES[kind]["per_radius"] = per; RL = [r["R_live"] for r in rows if r.get("R_live")]; RES[kind]["R_live"] = float(np.median(RL)) if RL else None; RES[kind]["R_live_range"] = [min(RL), max(RL)] if RL else None; P(f"  R_live {RES[kind]['R_live']} {RES[kind]['R_live_range']}")
        cq = [(r["QB"][2] - 1) / (r["Q"][2] - 1) for r in rows]; RES[kind]["cut_at_2p2Rd"] = dict(med=float(np.median(cq)), ci95=boot(cq)); P(f"  (Q_B-1)/(Q-1) at 2.2 R_d: {np.median(cq):.2f} {boot(cq)}")
    st = stability(1, how); RES["stability"] = st; P("\nstability, core no disc, d ln M(<r) from the IC: " + json.dumps(st))
    RES["stability_all"] = {s: stability(s, how) for s in (2, 3, 4, 5) if os.path.exists(run_name("core", s, "_nodisc"))}
    d = run_name("core", 1, "_nodisc"); Z0 = np.load(os.path.join(d, "ic.npz")); fend = sorted(glob.glob(os.path.join(d, "snap_t*.npz")))[-1]; Z1 = np.load(fend); e0 = energy(Z0["x"], Z0["v"], float(Z0["m"])); e1 = energy(Z1["x"], Z1["v"], float(Z0["m"])); dE = (sum(e1) / sum(e0) - 1); RES["energy"] = dict(virial_ic=2 * e0[0] / abs(e0[1]), virial_end=2 * e1[0] / abs(e1[1]), dE=dE, to=os.path.basename(fend)); P(f"energy: 2T/|U| start {RES['energy']['virial_ic']:.4f}, end {RES['energy']['virial_end']:.4f}; dE/E {dE:+.2e} to {os.path.basename(fend)}")
    mut = one("core", 1, how, "_MUTATE", act=False)
    if mut and "core_s1" in res: q1, q2 = res["core_s1"]["Q"][3], mut["Q"][3]; RES["mutate"] = dict(q1=q1, q2=q2, d=(q2 - 1) / (q1 - 1) - 1); P(f"MUTATE M_d x 2: Q(3 R_d) - 1 from {q1-1:.3f} to {q2-1:.3f}, {RES['mutate']['d']:+.0%}")
    RES["seeds"] = res; json.dump(RES, open(os.path.join(HERE, "dr8_live_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "dr8_live.out"), "w").write("\n".join(OUT) + "\n")
