#!/usr/bin/env python3
"""WF1 gates 2-3: HF1's code and CRG1's graders read-only, solver swapped in memory. Modes: controls | select | run M WF WB [SIGMULT] | planted M WF WB. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); HF = os.path.join(RB, "HF1_hybrid_fermion"); sys.path.insert(0, HF); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
_argv = sys.argv[:]; sys.argv = ["hf1_g23.py"]
import hf1_g23 as H
sys.argv = _argv
import numpy as np, wf1_solver as S
H.FM.solve = S.solve; C, CO, GR, DW, SP = H.C, H.CO, H.GR, H.DW, H.SP; A0 = H.A0; MPC = H.MPC; MSUN = H.MSUN
def cache(tag):
    d = os.path.join(HERE, "cache", tag); os.makedirs(d, exist_ok=True); CO.CACHE = d
def stat(reset=True):
    s = {k: S.STAT[k] for k in ("rows", "unbound", "unres", "zero", "noconv", "big")}
    if reset: S.STAT.update(rows=0, unbound=0, unres=0, zero=0, noconv=0, big=0)
    return s
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def controls():
    ck = {}; D, CSS, XC, G, LT = H.load_common()
    x = H.xcop_rows(XC, 0.0, 1e-24, "canonical"); ck["K_zero_xcop"] = dict(mean=x["all"]["mean"], rms=x["all"]["rms"], passed=bool(abs(x["all"]["mean"] - .467) <= .01 and abs(x["all"]["rms"] - .476) <= .01))
    r0, t0, _ = H.sparc_fit(G, 0.0, 1e-24, A0["canonical"]); ck["K_zero_sparc"] = dict(rms=r0["rms"], Y=r0["Y_med"], passed=bool(abs(r0["rms"] - .0541) <= 2e-4 and abs(r0["Y_med"] - .52) <= .011))
    c = XC[0]; Mg = C.li(c["gr"], c["gm"], c["R500"]); Rp = c["R500"] / 1e3; _, Mb, Mbt, rta = C.chain(Mg, Rp, 0.034, c["z"], CO.E.Msun, seed=3 * 1.2 * Mg * CO.E.Msun); Ms = {}
    for n in (420, 840):
        r = np.geomspace(1e-3 * MPC, rta * 1.0001, n); s = S.solve(r, np.interp(np.log(r), np.log(C.RM), Mb), rta, Rp * MPC, 5.0 * Mbt, 1e-23, A0["canonical"]); Ms[n] = (float(np.interp(Rp * MPC, r, s["Mf"])), float(s["Mf"][-1]), s["conv"], float(s["Ms"]), float(s["rs"]))
    ck["K_grid_fair"] = dict(M500=[Ms[420][0], Ms[840][0]], ratio=Ms[420][0] / Ms[840][0], fair=Ms[840][1] / (5.0 * Mbt), conv=[Ms[420][2], Ms[840][2]], Ms_kg=Ms[840][3], rs_kpc=Ms[840][4] / 3.0857e19, passed=bool(abs(Ms[420][0] / Ms[840][0] - 1) <= .01 and abs(Ms[840][1] / (5.0 * Mbt) - 1) <= .01 and Ms[840][2]))
    json.dump(ck, open(os.path.join(HERE, "wf1_g23_controls.json"), "w"), indent=1, default=float); print(json.dumps(ck, indent=1, default=float), flush=True); return all(v["passed"] for v in ck.values())
def select():
    g1 = json.load(open(os.path.join(HERE, "wf1_g1_results.json")))["rows"]; D, CSS, XC, G, LT = H.load_common(); T = {}
    pool0 = [w for w in g1.values() if "omega_f" in w]; ps = [w for w in pool0 if w.get("passed")]
    P(f"WF1 select, A/R3 rule. gate-1 passers: {[w['m'] for w in ps]}")
    for w in (ps or pool0):
        Rf = w["omega_f"] / w["omega_b"]; m = w["m"]; x = H.xcop_rows(XC, Rf, m, "canonical"); sx = stat(); s = H.bf1_train(G, Rf, m, A0["canonical"]); ss = stat(); T[f"{m:g}"] = dict(m=m, omega_f=w["omega_f"], omega_b=w["omega_b"], S=w.get("S"), xtrain=x["train"], strain=s, by_x=x["by_x"], stat_x=sx, stat_s=ss)
        P(f"  m {m:g} wf {w['omega_f']:.4f}: X-COP train {x['train']['mean']:+.3f}, {x['train']['rms']:.3f} {x['train']['passed']}; by x {[round(v, 3) for v in x['by_x'].values()]}; SPARC train rms {s['rms']:.4f} (law {s['rms_law']:.4f}), median {s['median']:+.3f} {s['passed']}; X flags {sx}; S flags {ss}")
    both = [t for t in T.values() if t["xtrain"]["passed"] and t["strain"]["passed"]]; ch = min(both, key=lambda t: t["S"]) if both else min(T.values(), key=lambda t: abs(t["xtrain"]["mean"])); P(f"CHOSEN m {ch['m']:g}, omega_f {ch['omega_f']:.5f}, omega_b {ch['omega_b']:.5f}; rule {'both pass, lowest S' if both else 'none pass both: smallest |mean| on X-COP train'}")
    json.dump(CO.fmt(dict(table=T, chosen=ch)), open(os.path.join(HERE, "wf1_select.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "wf1_select.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED. Not theory closed.\n")
def run(m, wf, wb, sm=1.0):
    S.Cfg.sig_mult = sm; tag = f"m{m:g}_s{sm:g}"; cache(tag); D, CSS, XC, G, LT = H.load_common(); Rf = wf / wb
    P(f"WF1 gates 2-3 on HF1's report; the 'cap' words in that report are fermion text and don't apply: the cap is off, the core rule is the ground state. sigma x {sm:g}.")
    R = H.report_gate("RUN", Rf, m, wf, wb, D, CSS, XC, G, LT); fl = stat(); P(f"  flags over all rows {fl}")
    OUT.extend(H.OUT); sf = f"_{tag}"; json.dump(CO.fmt(dict(R=R, flags=fl)), open(os.path.join(HERE, f"wf1_RUN{sf}.json"), "w"), indent=1, sort_keys=True, default=float); open(os.path.join(HERE, f"wf1_RUN{sf}.out"), "w").write("\n".join(H.OUT) + f"\n  flags {fl}\nkappa = 1/2 FITTED. Not theory closed.\n")
def planted(m, wf, wb):
    cache("planted"); D, CSS, XC, G, LT = H.load_common(); r, t, _ = H.sparc_fit(G, 100 * wf / wb, m, A0["canonical"]); ok = r["rms"] <= .11 and .5 <= r["Y_med"] <= .8 and abs(t["tilt"]) <= .15; d = dict(m=m, rms=r["rms"], Y=r["Y_med"], tilt=t["tilt"], gate3_pass=bool(ok), passed=not ok); json.dump(d, open(os.path.join(HERE, "wf1_planted_MUTATE.json"), "w"), indent=1, default=float); print(d)
if __name__ == "__main__":
    a = sys.argv[1]
    if a == "controls": sys.exit(0 if controls() else 1)
    if a == "select": select()
    if a == "run": run(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]) if len(sys.argv) > 5 else 1.0)
    if a == "planted": planted(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
