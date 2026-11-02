#!/usr/bin/env python3
"""AF1 stage 3 grade: Pareto fronts on holdouts, label control, frozen-line margins, IC 1613, Bullet. FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed. Margins are not a pass of the 15 keys."""
import csv, json, math, os, re, sys, importlib.util
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); OUT = []; SUF = os.environ.get("AF1_SUF", "")
def P(s): print(s, flush=True); OUT.append(s)
src = open(os.path.join(HERE, "af1_stage3.py")).read().replace("main(sys.argv[1])", ""); NS = {"__file__": os.path.join(HERE, "af1_stage3.py")}; exec(compile(src, "s3", "exec"), NS); load, SAMPLES, FEAT = NS["load"], NS["SAMPLES"], NS["FEAT"]
FN = dict(exp=np.exp, log=np.log, sqrt=np.sqrt, square=np.square, safe_log=np.log, safe_sqrt=np.sqrt)
def f_eq(eq):
    code = compile(eq, "e", "eval")
    def f(Z): return np.broadcast_to(eval(code, {"__builtins__": {}}, dict(FN, **{f"z_{k}": Z[:, i] for i, k in enumerate(FEAT)})), (len(Z),)).astype(float)
    return f
def nconst(eq): return len(re.findall(r"(?<![a-z_])\d+\.?\d*(?:e[+-]?\d+)?", eq))
def wrms(x): return float(np.sqrt(np.mean(x ** 2)))
def sc(D, pred):
    te = ~D["train"]; o = {}; res = D["r"] - pred
    for s in SAMPLES:
        m = te & (D["sample"] == s); tr = D["train"] & (D["sample"] == s); c = float(np.average(D["r"][tr], weights=D["w"][tr])) if tr.any() else 0.0
        o[s] = dict(n=int(m.sum()), rms=wrms(res[m]), med=float(np.median(res[m])), mean=float(res[m].mean()), law=wrms(D["r"][m]), lab=wrms(D["r"][m] - c), bad=bool(not np.all(np.isfinite(pred[m]))))
    return o
def margins(D, pred):
    te = ~D["train"]; res = D["r"] - pred; X = te & (D["sample"] == "XCOP"); Sx = te & (D["sample"] == "SPARC"); Gr = te & (D["sample"] == "groups"); Sh = te & (D["sample"] == "shearM"); Dw = te & (D["sample"] == "dwarfs")
    m = dict(XCOP_mean=float(res[X].mean()), XCOP_rms=wrms(res[X]), XCOP_ok=bool(abs(res[X].mean()) <= .05 and wrms(res[X]) <= .10), SPARC_rms_ratio=wrms(res[Sx]) / wrms(D["r"][Sx]), SPARC_med=float(np.median(res[Sx])), SPARC_ok=bool(wrms(res[Sx]) <= 1.3 * wrms(D["r"][Sx]) and abs(np.median(res[Sx])) <= .06), groups_Z=float(res[Gr].mean() / 2 / (.0422 * math.sqrt(63 / Gr.sum()))), shear_chi2=float((res[Sh] ** 2 / D["sig"][Sh] ** 2).sum()), shear_n=int(Sh.sum()), dwarf_med=float(np.median(res[Dw])))
    m["groups_ok"] = bool(abs(m["groups_Z"]) < 2)
    cl = np.array([s.split("|")[-1] for s in D["system"]]); Zs = {}
    for c in ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field"):
        q = Dw & (cl == c)
        if q.sum() >= 3:
            g = np.random.default_rng(20261026); ix = g.integers(0, q.sum(), (4000, q.sum())); e = res[q]; s_ = D["sig"][q]; sd = np.std(np.median(e[ix] + s_[ix] * g.standard_normal(ix.shape), axis=1)); Zs[c] = float(np.median(e) / sd)
    m["dwarf_Z"] = Zs; m["dwarf_ok"] = bool(all(abs(z) < 2 for z in Zs.values())); return m
def ic(foot, D, f):
    J = json.load(open(os.path.join(HERE, "af1_stage1.json")))[foot]["ic1613"]; a0 = dict(canonical=9.360324825027975e-11, alt=1.1312e-10)[foot]; ly = math.log10(J["y"]); ls = ly + math.log10(2.88e7 * .5 * 2 / 10 ** 7.944975908412048 if False else 2.88e7 / 10 ** 7.944975908412048); ms = 7.944975908412048 + math.log10(6.674e-11 * 1.989e30 * a0 / 299792458.0 ** 4); z = (np.array([[ly, ls, math.log10(J["ell"]), ms]]) - D["mu"]) / D["sd"]; p = float(f(z)[0]); return dict(E=J["r"], pred=p, res=J["r"] - p, Z=(J["r"] - p) / .075)
def bullet_ns():
    s = open(os.path.join(RB, "UX6_gas_term_bullet", "ux6_bullet.py")).read(); s = s[:s.index('say("=" * 90)')].replace('OUT = open(os.path.join(HERE, f"ux6_bullet{TAG}.out"), "w")', 'OUT = open(os.devnull, "w")')
    a = 'if form in ("L1", "L1c", "S", "N3a", "N3b"):'; assert s.count(a) == 1; s = s.replace(a, 'if form == "AF":\n            ys = np.sqrt(C["st"][0]**2 + C["st"][1]**2 + C["st"][2]**2)/a0; return tuple(gb[i]*(m*10**sp["H"](np.maximum(g/a0,1e-12), np.maximum(ys,1e-12)) - 1) for i in range(3))\n        ' + a)
    n = {"__file__": os.path.join(RB, "UX6_gas_term_bullet", "ux6_bullet.py"), "__name__": "ux6ro"}; exec(compile(s, "ux6", "exec"), n); return n
def main():
    RES = {}; BN = None; D = {f: load(f) for f in ("canonical", "alt")}; TR = {}
    # planted
    Hp = list(csv.DictReader(open(os.path.join(HERE, "af1_hof_planted.csv")))); Dp = D["canonical"]; g = np.random.default_rng(20261102 + 5); Z = Dp["X"]; tp = 0.2 * Z[:, 0] ** 2 - 0.3 * Z[:, 2] + 0.1 + g.normal(0, .1, len(Z)); te = ~Dp["train"]; ok = False
    P("PLANTED, truth 0.2 z_ly^2 - 0.3 z_lell + 0.1, noise 0.1, holdout rms must be <= 0.12")
    for h in Hp:
        p = f_eq(h["equation"])(Z); rm = wrms((tp - p)[te]); ok |= rm <= .12; P(f"  c {h['complexity']:>2s} holdout rms {rm:.3f}  {h['equation'][:100]}")
    RES["planted_recovered"] = bool(ok); P(f"planted: {'RECOVERED' if ok else 'NOT RECOVERED'}")
    Hs = {int(h["complexity"]): h["equation"] for h in csv.DictReader(open(os.path.join(HERE, "af1_hof_scrambled.csv")))}; sw = {}
    P("\nSCRAMBLED control, canonical, holdout per-sample mean rms on REAL holdout rows")
    for c, e in sorted(Hs.items()):
        pr = f_eq(e)(Dp["X"]); o = sc(Dp, pr); sw[c] = float(np.mean([o[s]["rms"] for s in SAMPLES])); P(f"  c {c:2d} mean rms {sw[c]:.3f}  {e[:90]}")
    Lb = np.mean([sc(Dp, np.zeros(len(Dp['r'])))[s]["lab"] for s in SAMPLES]); P(f"label control mean rms {Lb:.3f}")
    for foot in ("canonical", "alt"):
        d = D[foot]; H = list(csv.DictReader(open(os.path.join(HERE, f"af1_hof_{foot}{SUF}.csv")))); RES[foot] = []; P(f"\n[{foot}] Pareto front. Law: " + " ".join(f"{s} {sc(d, np.zeros(len(d['r'])))[s]['law']:.3f}" for s in SAMPLES)); P(f"  label control:  " + " ".join(f"{s} {sc(d, np.zeros(len(d['r'])))[s]['lab']:.3f}" for s in SAMPLES))
        for h in H:
            e = h["equation"]; f = f_eq(e); pr = f(d["X"]); o = sc(d, pr)
            if any(o[s]["bad"] for s in SAMPLES): P(f"  c {h['complexity']:>2s} non-finite on holdout: UNDEFINED  {e[:80]}"); RES[foot].append(dict(c=int(h["complexity"]), eq=e, undefined=True, transfers=False)); continue
            nb = sum(o[s]["rms"] < o[s]["lab"] for s in SAMPLES); nw = [s for s in SAMPLES if o[s]["rms"] > 1.1 * o[s]["law"]]; mg = margins(d, pr); i_ = ic(foot, d, f); mr = float(np.mean([o[s]["rms"] for s in SAMPLES])); c_ = int(h["complexity"]); sv = min((v for k, v in sw.items() if k <= c_), default=np.inf); T = nb >= 5 and not nw
            RES[foot].append(dict(c=c_, eq=e, nconst=nconst(e), train_loss=float(h["loss"]), per_sample=o, margins=mg, ic1613=i_, n_beat_label=nb, worse_than_law=nw, mean_rms=mr, scrambled_best=sv, transfers_one_footing=bool(T), beats_scrambled=bool(mr < sv)))
            P(f"  c {c_:2d} k {nconst(e):2d} beat-label {nb}/7 worse-law {','.join(nw) or '-'} mean {mr:.3f} scr {sv:.3f} | " + " ".join(f"{s} {o[s]['rms']:.3f}" for s in SAMPLES) + f" | XCOP {mg['XCOP_mean']:+.3f},{mg['XCOP_rms']:.3f} SPmed {mg['SPARC_med']:+.3f} gZ {mg['groups_Z']:+.1f} shX2 {mg['shear_chi2']:.0f}/{mg['shear_n']} IC Z {i_['Z']:+.1f}"); P(f"       {e[:170]}")
    tr = {}
    for x in RES["canonical"]:
        if x.get("undefined"): continue
        a = next((y for y in RES["alt"] if y["c"] == x["c"] and not y.get("undefined")), None); tr[x["c"]] = bool(x["transfers_one_footing"] and x["beats_scrambled"] and a and a["transfers_one_footing"])
    RES["transfers"] = tr; lab = "SOME TRANSFER" if any(tr.values()) else "NO FORMULA TRANSFERS"; RES["label"] = lab; P(f"\nFROZEN LABEL: {lab} ({sum(tr.values())} of {len(tr)} canonical complexities with alt partner at same complexity)")
    # Bullet, equations with only y and y_star
    n = bullet_ns(); P("\nBullet, UX6's path, equations using only z_ly, z_ly_star (local); others NOT EVALUABLE")
    specs = {}; meta = {}
    for foot in ("canonical", "alt"):
        d = D[foot]; a0 = n["A0F"][foot]; specs[f"LAW|{foot}"] = dict(form="LAW", a0=a0, k=0.0)
        L = [x for x in RES[foot] if not x.get("undefined")]; evs = [x for x in L if not re.search("z_lell|z_m_sys", x["eq"]) and x["c"] > 1]; ne = len(L) - len(evs); RES[foot + "_bullet_not_evaluable"] = ne
        best = sorted(evs, key=lambda x: x["mean_rms"])[:3]
        for x in best:
            f = f_eq(x["eq"]); mu, sdv = d["mu"], d["sd"]
            def mk(f=f, mu=mu, sdv=sdv):
                def H(y, ys):
                    sh = y.shape; Z_ = np.column_stack([(np.log10(y.ravel()) - mu[0]) / sdv[0], (np.log10(ys.ravel()) - mu[1]) / sdv[1], np.zeros(y.size), np.zeros(y.size)]); return np.nan_to_num(f(Z_), nan=0.0, posinf=3.0, neginf=-3.0).clip(-3, 3).reshape(sh)
                return H
            specs[f"c{x['c']}|{foot}"] = dict(form="AF", a0=a0, k=0.0, H=mk()); meta[f"c{x['c']}|{foot}"] = x["eq"]
    R = n["run"](specs); RES["bullet"] = {}
    for k, (S, m) in R.items():
        o = n["observe"](S, m); RES["bullet"][k] = {a: o[a] for a in ("M300", "ZO3", "ratio", "cls")}; RES["bullet"][k]["dkappa"] = [o["main"]["dkappa"], o["sub"]["dkappa"]]; RES["bullet"][k]["d_gas"] = [o["main"]["d_gas"], o["sub"]["d_gas"]]; RES["bullet"][k]["d_bcg"] = [o["main"]["d_bcg"], o["sub"]["d_bcg"]]; P(f"  {k:16s} {o['cls']:8s} M300 {o['M300'][0]/1e14:.2f} {o['M300'][1]/1e14:.2f} (Z {o['ZO3'][0]:+.1f} {o['ZO3'][1]:+.1f}) dkappa {o['main']['dkappa']:+.3f} {o['sub']['dkappa']:+.3f} peak-BCG {o['main']['d_bcg']:.0f} {o['sub']['d_bcg']:.0f} peak-gas {o['main']['d_gas']:.0f} {o['sub']['d_gas']:.0f}")
    P(f"  not evaluable: canonical {RES.get('canonical_bullet_not_evaluable')}, alt {RES.get('alt_bullet_not_evaluable')} equations hold z_lell or z_m_sys (non-local)")
    json.dump(RES, open(os.path.join(HERE, f"af1_stage3{SUF}.json"), "w"), indent=0, sort_keys=True, default=float); open(os.path.join(HERE, f"af1_stage3{SUF}.out"), "w").write("\n".join(OUT) + "\n")
main()
