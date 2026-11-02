#!/usr/bin/env python3
"""RS1 Part 1: requirement map + collapse test + K1, K2. RS1_MUTATE=1: a0 x 2, separate outputs, K1 must fail. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import rs1_rows as T
import numpy as np
from scipy.stats import spearmanr
from sklearn.isotonic import IsotonicRegression
MUT = os.environ.get("RS1_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
out = []; res = dict(checks={}, map={}, collapse={})
def P(s=""): print(s, flush=True); out.append(str(s))
NM = {"S": "SPARC", "LT": "LITTLE THINGS", "G3": "groups f .3", "G6": "groups f .6", "X": "X-COP HSE", "L": "lensing SIS", "Dw": "dwarfs"}
P("RS1 Part 1. M_x = (g_N,req - g_b) r^2/G. kappa = 1/2 FITTED; not theory closed." + (" [MUTATE a0 x 2]" if MUT else ""))
for ft in ("canonical", "alt"):
    for ups in T.UPS:
        a0 = T.A0[ft] * (2 if MUT else 1); A = T.arrays(T.table(ft, ups)); L = T.leaves(A, a0); gN = T.greq(A["gobs"], a0); gx = gN - A["gb"]; Mx = gx * A["r"] ** 2 / T.G; Mb = A["gb"] * A["r"] ** 2 / T.G
        d = np.log10(A["gobs"] / T.law(A["gb"], a0)); key = f"{ft}|{ups}"; res["map"][key] = {}
        if ups == "U50":
            k2 = float(np.max(np.abs(T.law(gN, a0) / A["gobs"] - 1))); res["checks"].setdefault("K2", {})[ft] = k2
            e = {}
            X = A["c"] == T.CLS.index("X"); e["xcop"] = (float(d[X].mean()), float(np.sqrt((d[X] ** 2).mean()))); e["LT_median"] = float(np.median(d[A["c"] == T.CLS.index("LT")]))
            DW = A["c"] == T.CLS.index("Dw"); Z = {}
            rg = np.random.default_rng(20261026)
            for cl in T.DW.CLASSES:
                i = np.nonzero(DW & (A["sub"] == cl))[0]; ix = rg.integers(0, len(i), (10000, len(i))); z = rg.standard_normal((10000, len(i))); sd = float(np.std(np.median(d[i][ix] + A["err"][i][ix] * z, axis=1))); Z[cl] = float(np.median(d[i]) / sd)
            e["Dw_Z"] = Z; res["checks"].setdefault("K1", {})[ft] = e
            for c in ("G3", "L"):
                i = A["c"] == T.CLS.index(c); e[c + "_mean"] = float(d[i].mean())
            for n in sorted(set(A["name"][A["c"] == T.CLS.index("L")])):
                i = (A["c"] == T.CLS.index("L")) & (A["name"] == n); e["L_" + n] = float(d[i].mean())
            P(f"\n{ft} law K1: {json.dumps(e)}")
        P(f"\n== {ft} {ups}: class, n, M_x/M_b 16/50/84, share M_x<0, share |M_x|>2 err, mean rho_x (Msun/pc3), rho_x/rho_b, lg Q (Msun/pc3/(km/s)3), rho(M_gas), rho(M_star)")
        for c in T.CLS:
            i = A["c"] == T.CLS.index(c); q = Mx[i] / Mb[i]; v = 4 * math.pi * A["r"][i] ** 3 / 3; rx = Mx[i] / v / (T.MS / T.PC ** 3); rb = Mb[i] / v / (T.MS / T.PC ** 3)
            sg = np.nan
            if np.isfinite(A["err"][i]).any():
                eg = A["err"][i] * math.log(10) * A["gobs"][i] * (A["gobs"][i] * (A["gobs"][i] + 2 * a0) / (A["gobs"][i] + a0) ** 2); sg = float(np.mean(np.abs(gx[i]) > 2 * eg))
            s = A["sig"][i] / 1e3; pos = (Mx[i] > 0) & np.isfinite(s); lQ = float(np.median(np.log10(rx[pos] / s[pos] ** 3))) if pos.any() else np.nan
            Mg = A["gg"][i] * A["r"][i] ** 2 / T.G; Ms = A["gs"][i] * A["r"][i] ** 2 / T.G; r1 = spearmanr(Mx[i], Mg)[0] if np.ptp(Mg) > 0 else np.nan; r2 = spearmanr(Mx[i], Ms)[0]
            pc = np.percentile(q, [16, 50, 84]); w = dict(n=int(i.sum()), q=pc.tolist(), neg=float(np.mean(q < 0)), sig=sg, rho_x=float(np.median(rx)), ratio=float(np.median(rx / rb)), lgQ=lQ, r_gas=float(r1), r_star=float(r2)); res["map"][key][c] = w
            P(f"  {NM[c]:15s} {w['n']:5d}  {pc[0]:+9.3f} {pc[1]:+9.3f} {pc[2]:+9.3f}  neg {w['neg']:.2f}  sig {sg:.2f}  rho_x {w['rho_x']:+.2e}  x/b {w['ratio']:+8.3f}  lgQ {lQ:+6.2f}  gas {r1:+.2f}  star {r2:+.2f}")
        # local rho and partial correlation inside SPARC and X-COP, and collapse
        pos = (Mx > 0) & (Mb > 0); w = np.array([1 / np.sum(A["c"][pos] == c) for c in A["c"][pos]]); Y = np.log10(Mx[pos] / Mb[pos])
        rho_b = Mb / (4 * math.pi * A["r"] ** 3 / 3); V = dict(y_g=L["y_g"], y_s=L["y_s"], y=A["gb"] / a0, f=L["f"], ell=L["ell"], mu=L["mu"], x=L["x"], rho_b=rho_b * T.G * (T.CL / a0) ** 2, Q=(Mx / (4 * math.pi * A["r"] ** 3 / 3)) / np.where(A["sig"] > 0, A["sig"], np.nan) ** 3)
        sm = float(np.average(Y, weights=w)); r0 = float(np.sqrt(np.average((Y - sm) ** 2, weights=w))); res["collapse"][key] = dict(rms_mean=r0, vars={}); rg = np.random.default_rng(20261102); ups_any = False
        P(f"  collapse, {pos.sum()} rows M_x > 0, classes weighted equally, rms about mean {r0:.3f}: variable, rms about monotone fit, worst class median offset, shuffled null median, verdict")
        for nm, v in V.items():
            ok = pos & np.isfinite(v) & (v > 0) if nm != "f" else pos & np.isfinite(v); xx = np.log10(np.maximum(v[ok], 1e-300)) if nm != "f" else v[ok]; yy = np.log10(Mx[ok] / Mb[ok]); ww = np.array([1 / np.sum(A["c"][ok] == c) for c in A["c"][ok]]); cc = A["c"][ok]
            def fit(xv):
                b = (9e9, None)
                for inc in (True, False):
                    m = IsotonicRegression(increasing=inc, out_of_bounds="clip").fit(xv, yy, sample_weight=ww); p = m.predict(xv); s = float(np.sqrt(np.average((yy - p) ** 2, weights=ww)))
                    if s < b[0]: b = (s, p)
                return b
            s, p = fit(xx); wc = max(abs(float(np.median((yy - p)[cc == c]))) for c in np.unique(cc)); nl = [fit(rg.permutation(xx))[0] for _ in range(200 if not MUT else 3)]
            coll = s <= 0.20 and wc <= 0.20; res["collapse"][key]["vars"][nm] = dict(rms=s, worst=wc, null=float(np.median(nl)), nullmin=float(np.min(nl)), collapses=bool(coll), n=int(ok.sum()), circular=nm == "Q"); ups_any |= coll
            P(f"    {nm:6s} {s:.3f}  {wc:.3f}  null {np.median(nl):.3f}  {'COLLAPSES' if coll else 'does not'}{'  [circular, descriptive]' if nm == 'Q' else ''}")
# Milky Way and IC 1613: the sign only, from the record's own rows
rq = json.load(open(os.path.join(T.RB, "RQ3_acceptance_v2", "results", "law.json")))
P("\nMW, IC 1613: law's rows, not an inversion"); res["mw_ic"] = {}
for ft in ("canonical", "alt"):
    r = rq["footings"][ft]["rows"]; res["mw_ic"][ft] = dict(A10=r.get("A10"), A15=r.get("A15")); P(f"  {ft} A10 value {r['A10'].get('value')} Z {r['A10'].get('Z')}; A15 value {r['A15'].get('value')} Z {r['A15'].get('Z')}")
k = res["checks"]["K1"]["canonical"]; ok = abs(k["xcop"][0] - 0.467) <= 0.01 and abs(k["xcop"][1] - 0.476) <= 0.01 and abs(k["LT_median"] + 0.025) <= 0.002 and abs(k["Dw_Z"]["MW ultra-faint"] - 5.22) <= 0.05
res["checks"]["K1_pass"] = bool(ok); res["checks"]["K2_pass"] = bool(max(res["checks"]["K2"].values()) < 1e-10); P(f"\nchecks: K1 {ok}, K2 {res['checks']['K2_pass']}"); P("kappa = 1/2 FITTED. Not theory closed.")
json.dump(res, open(os.path.join(HERE, f"rs1_map{TAG}.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"rs1_map{TAG}.out"), "w").write("\n".join(out) + "\n"); sys.exit(0 if ok else 1)
