#!/usr/bin/env python3
"""BF2 step 2 detail: where SPARC breaks, fixed and free Upsilon, by V_flat and gas share. kappa = 1/2 FITTED; not theory closed."""
import importlib.util as iu, json, math, os, sys
from bf2_common import *
A = rq3(); A.crg(); import crg1_sparc as Cs
OUT = open(os.path.join(LANE, f"bf2_sparc{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n")
def load(t, p):
    sp = iu.spec_from_file_location(t, p); m = iu.module_from_spec(sp); sp.loader.exec_module(m); return m
CS = {"law": load("law", os.path.join(RQ3, "candidates", "law.py")), **{t: load(t, os.path.join(LANE, "candidates", f"{t}{TAG}.py")) for t in ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8")}}
G = Cs.load_gal(); UPS = Cs.UPS; i05 = int(np.argmin(np.abs(UPS - .5)))
FG = np.array([1.33 * g["MHI"] / max(.5 * g["L36"] + 1.33 * g["MHI"], 1e-9) for g in G]); V = np.array([g["Vflat"] for g in G]); QF = np.array([g["Q"] < 3 and g["Inc"] >= 30 for g in G]); Q2 = np.array([g["Q"] <= 2 and g["Inc"] >= 30 for g in G])
VB = [(1, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)]; t1, t2 = np.percentile(FG[Q2], [100 / 3, 200 / 3]); GB = [(0, t1), (t1, t2), (t2, 1.01)]; say(f"gas-share terciles, 1.33 M_HI / M_b at Upsilon 0.5, Q<=2: {t1:.3f}, {t2:.3f}")
RES = {}
for ft in FEET:
    a0 = A0[ft]
    for n, c in CS.items():
        def model(g, gb):
            gg = np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"]; return c.g(dict(gb=gb, gg=np.broadcast_to(gg, gb.shape), gs=gb - gg, r=np.broadcast_to(g["R"], gb.shape), a0=a0))
        r = Cs.fit(G, model); Yb = r["Yb"]; fi, fw = [], []; mn = []; fx = []
        for k, g in enumerate(G):
            gb = Cs.gB_mat(g); gO = (g["Vobs"] * 1e3) ** 2 / g["R"]; ok = (gb > 0) & (gO > 0) & (g["Vobs"] > 0); gp = model(g, gb); W = 1 / (np.maximum(g["eV"], 1) / np.maximum(g["Vobs"], 1)) ** 2; d = np.where(ok, np.log10(np.where(gO > 0, gO, 1.)) - np.log10(np.maximum(gp, 1e-300)), 0.); iy = int(np.argmin(np.abs(UPS - Yb[k]))) if np.isfinite(Yb[k]) else i05
            fi.append(((W * d[iy] ** 2 * ok[iy]).sum(), (W * ok[iy]).sum(), float(np.nanmean(d[iy][ok[iy]])) if ok[iy].any() else 0.)); o5 = ok[i05]; fx.append(d[i05][o5] if o5.any() else np.array([])); mn.append(float(np.min(gp[iy][ok[iy]] / gb[iy][ok[iy]])) if ok[iy].any() else np.nan)
        fi = np.array(fi); gr = np.sqrt(fi[:, 0] / np.maximum(fi[:, 1], 1e-99)); fxr = np.array([math.sqrt((x * x).mean()) if len(x) else np.nan for x in fx]); fxm = np.array([x.mean() if len(x) else np.nan for x in fx])
        def part(s):
            return dict(n=int(s.sum()), free=float(math.sqrt(fi[s, 0].sum() / fi[s, 1].sum())), U=float(np.nanmedian(Yb[s])), fixed=float(np.sqrt(np.mean(np.concatenate([fx[i] for i in np.nonzero(s)[0]]) ** 2))), fixed_mean=float(np.mean(np.concatenate([fx[i] for i in np.nonzero(s)[0]]))))
        b = {f"V{x}-{y}": part(Q2 & (V >= x) & (V < y)) for x, y in VB}; gb_ = {f"f{i}": part(Q2 & (FG >= x) & (FG < y)) for i, (x, y) in enumerate(GB)}
        all_q = np.concatenate([fx[i] for i in np.nonzero(QF)[0]]); wf = sorted(np.nonzero(QF)[0], key=lambda i: -np.nan_to_num(fxr[i])); wv = sorted(np.nonzero(Q2)[0], key=lambda i: -gr[i])
        RES[f"{n}|{ft}"] = dict(rms=r["rms"], U=r["Y_med"], tilt=Cs.tilt(G, Yb)["tilt"], fixed_all=float(np.sqrt((all_q ** 2).mean())), fixed_med=float(np.median(all_q)), bins=b, gas=gb_, min_g_over_gb=float(np.nanmin(mn)), n_U_at_floor=int((Yb[Q2] <= .3001).sum()), n_U_at_ceiling=int((Yb[Q2] >= 1.1999).sum()), worst_fixed=[[G[i]["name"], round(float(fxr[i]), 3), round(float(fxm[i]), 3), V[i], round(float(FG[i]), 2)] for i in wf[:8]], worst_free=[[G[i]["name"], round(float(gr[i]), 3), float(Yb[i]), V[i], round(float(FG[i]), 2)] for i in wv[:8]])
        X = RES[f"{n}|{ft}"]; say(f"\n== {n} {ft}: free rms {X['rms']:.4f} U {X['U']:.2f} tilt {X['tilt']:+.3f}; fixed Q<3 rms {X['fixed_all']:.3f} med {X['fixed_med']:+.3f}; min g/g_b {X['min_g_over_gb']:.3f}; U at floor 0.30: {X['n_U_at_floor']}, ceiling 1.20: {X['n_U_at_ceiling']}")
        for lab, D in (("V_flat", b), ("gas", gb_)):
            for k, v in D.items(): say(f"  {k:10s} n {v['n']:3d} free {v['free']:.3f} U {v['U']:.2f} | fixed {v['fixed']:.3f} mean resid {v['fixed_mean']:+.3f}")
        say("  worst fixed (name, rms, mean, Vf, gas):", X["worst_fixed"][:6]); say("  worst free (name, rms, U, Vf, gas):", X["worst_free"][:6])
json.dump(RES, open(os.path.join(LANE, f"bf2_sparc{TAG}.json"), "w"), indent=0, sort_keys=True, default=float); OUT.close()
