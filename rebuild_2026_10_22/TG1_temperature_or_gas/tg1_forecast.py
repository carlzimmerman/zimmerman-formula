#!/usr/bin/env python3
"""TG1 forecast (FROZEN_CRITERIA.md). Mocks only: no conditional statistic on real data. TG1_MUTATE=1 for the twin. kappa = 1/2 FITTED; not theory closed."""
from tg1_common import *
OUT = []; RES = {"mutate": MUT}; CHK = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(n, ok, t): CHK.append((n, bool(ok))); P(f"{n} {'PASS' if ok else 'FAIL'}: {t}"); RES.setdefault("checks", {})[n] = dict(ok=bool(ok), t=str(t))
def strip(r): return {k: v for k, v in r.items() if k not in ("H0", "HTz", "HGz")}
# ---- checks on inputs
d0 = dump(); n0, W0 = nW("h0672"); oo = n0.sum(0) / d0["V_canonical_h0672"].sum(0); LM = json.load(open(os.path.join(RB, "LM1_law_missing_mass_map", "lm1_results.json")))
def find(o):
    if isinstance(o, dict):
        if "obs_over_law" in o: return o["obs_over_law"]
        for v in o.values():
            f = find(v)
            if f is not None: return f
L0 = np.array(find(LM)); I_ = np.where(np.isfinite(CAT["KT"]) & (CAT["KT"] > 0))[0]; dI = len(I_) == len(d0["I"]) and bool(np.all(I_ == d0["I"])); xkt = np.log10(CAT["KT"][I_] / np.median(CAT["KT"][I_])); tid = np.digitize(xkt, np.quantile(xkt, [1/3, 2/3])); dT = len(tid) == len(d0["TID"]) and bool(np.all(tid == d0["TID"]))
check("K0", np.max(np.abs(oo - L0)) <= 1e-10 and dI and dT, f"obs/law vs LM1 max|dev| {np.max(np.abs(oo - L0)):.1e}; KT index equals dump I: {dI}; KT terciles equal dump TID: {dT}")
k1 = float(np.max(np.abs(col("MGAS500") * 1e11 / np.asarray(X["Mgas500"], float) - 1))); check("K1", k1 <= 1e-10, f"MGAS500 by NAME vs npz rel {k1:.1e}")
S = sample("canonical", "h0672"); w = S["W"].sum(1); e = w * (.7 + 1.3 * S["t"]); th = joint(e, w, (np.ones(S["t"].size), S["t"], S["g"])); bs = split_pair(e, w, S["t"], S["g"])
RES["K2_split_on_plant"] = list(map(float, bs)); check("K2", abs(th[1] - 1.3) <= 1e-9 and abs(th[2]) <= 1e-9 and abs(bs[0] / 1.3 - 1) <= .25, f"joint plant (b_T, b_G) {th[1]:.10f}, {th[2]:.1e}; split b_T {bs[0]:.3f}, b_G {bs[1]:+.3f} for plant 1.3 (split's b_G is the mock-free leak of a noiseless plant)")
# ---- primary
P(f"\nsample N by cell, errors missing (t, g) {S['ms']}; median sigma lg KT {np.median(S['st']):.3f}, lg Mg {np.median(S['sg']):.3f}; dump I {len(I_)}")
RES["prim"] = {}; MK = {}; CL = {}
for fi, f in enumerate(FEET):
    for hi_, h in enumerate(HS):
        S = sample(f, h); mk = Mock(S, 0); MK[(f, h)] = mk; r = run(mk, 100 + 10 * fi + hi_); RES["prim"][f"{f}|{h}"] = strip(r); CL.update({f"{f}|{h}|{c}": r[c] for c in ("H0", "HTz", "HGz")})
        Ci = mk.Cint; P(f"{f} {h} N {mk.N}: marginal alpha {mk.alpha:+.2f} beta {mk.beta:+.2f}; intrinsic sd t {Ci[0,0]**.5:.3f} g {Ci[1,1]**.5:.3f} rho {Ci[0,1]/(Ci[0,0]*Ci[1,1])**.5:+.2f}; gamma med {np.median(mk.gam):.2f}; s_T {r['s'][0]:.2f} s_G {r['s'][1]:.2f}"); P("  " + row(r))
        if (f, h) == ("canonical", "h0672"): R0 = r
LAB = {}
for f in FEET:
    A = [RES["prim"][f"{f}|{h}"] for h in HS]; ok = all(a["F"] >= 3 and min(a["acc"].values()) >= .9 for a in A); LAB[f] = "SEPARABLE" if ok else "NOT SEPARABLE"; P(f"FORECAST LABEL {f}: {LAB[f]}  (F {A[0]['F']:.2f}, {A[1]['F']:.2f}; line 3; acc floor .90; N needed for F=3 at this noise ~ {int(np.ceil(A[0]['N'] * (3 / A[0]['F']) ** 2))})")
RES["forecast_label"] = LAB
# ---- report rows, primary h 0.672, both footings
RES["rows"] = {}; RO = [("nuisances off", dict(nuis=0.)), ("T errors x0.5", dict(terr=.5)), ("T errors x2", dict(terr=2.)), ("T errors x3 (K4)", dict(terr=3.)), ("plants off (K4)", dict(a=0., b=0.)), ("eps_g sd x10 (K4)", dict(eps_x=10.)), ("fixed alpha 1.5, beta 1", dict(a=1.5, b=1.)), ("q per patch", dict(patch=True))]
if True: RO.append(("plant x3 (MUTATE plant)", "x3"))
for fi, f in enumerate(FEET):
    mk = MK[(f, "h0672")]
    for k, (nm_, kw) in enumerate(RO):
        kw = dict(a=3 * mk.alpha, b=3 * mk.beta) if kw == "x3" else kw; r = run(mk, 500 + 100 * fi + k, **kw); RES["rows"][f"{f}|{nm_}"] = strip(r); P(f"row {f} {nm_}: " + row(r))
    mi = Mock(sample(f, "h0672", "IM"), 0); r = run(mi, 900 + fi); RES["rows"][f"{f}|band IM"] = strip(r); P(f"row {f} band IM (alpha {mi.alpha:+.2f} beta {mi.beta:+.2f}): " + row(r))
Rr = RES["rows"]; b = "canonical|"; Fb = R0["F"]; sdb = R0["Z_sd"]["HT"][1]
k4a = Rr[b + "T errors x3 (K4)"]["F"] <= .9 * Fb; k4b = Rr[b + "plants off (K4)"]["F"] <= .5; k4c = Rr[b + "eps_g sd x10 (K4)"]["Z_sd"]["HT"][1] >= 1.1 * sdb
check("K4", k4a and k4b and k4c, f"T err x3 F {Rr[b + 'T errors x3 (K4)']['F']:.2f} vs {Fb:.2f} (need <= 0.9x): {k4a}; plants off F {Rr[b + 'plants off (K4)']['F']:.2f} (<= 0.5): {k4b}; eps x10 sd Z_G in HT {Rr[b + 'eps_g sd x10 (K4)']['Z_sd']['HT'][1]:.2f} vs {sdb:.2f} (>= 1.1x): {k4c}")
Fx3 = Rr[b + "plant x3 (MUTATE plant)"]["F"]; P(f"plant MUTATE: exponents x3 F {Fx3:.2f} vs {Fb:.2f}: {'RAISED, as required' if Fx3 > Fb else 'NOT RAISED'}"); RES["plant_mutate_raises"] = bool(Fx3 > Fb)
H0 = R0["H0"]; mdn = np.abs(np.median(H0, 0)); sd = H0.std(0, ddof=1); check("K5", mdn.max() <= .25 and np.abs(sd - 1).max() <= .1, f"H0 |median Z| {mdn.round(3).tolist()}, sd {sd.round(3).tolist()}")
check("K6", rss() < 4, "peak RSS under 4 GB, one thread, nice 15")
np.savez_compressed(os.path.join(HERE, f"tg1_clouds{TAG}.npz"), **CL)
P(f"\nchecks {sum(o for _, o in CHK)}/{len(CHK)} PASS"); open(os.path.join(HERE, f"tg1_forecast{TAG}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"tg1_forecast{TAG}.json"), "w"), indent=0, default=float); sys.exit(0 if all(o for _, o in CHK) else 1)
