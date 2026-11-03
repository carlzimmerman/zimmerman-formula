#!/usr/bin/env python3
"""BF3 Stage 2: RQ3 scorecard on selected forms, keys, TDG, LT, IC 1613, DiskMass, Bullet; beside it groups and Milky Way at assumed f, lens gas scaled, Saturn at f = 1. Lines unmoved. kappa = 1/2 FITTED; not theory closed."""
import importlib.util as iu, json, os, sys, types
from bf3_common import *
OUT = open(os.path.join(LANE, f"bf3_holdout{TAG}.out"), "a")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
TPL = '''"""BF3 candidate, generated. Description, no action, no fitted float; chosen from a search of about 1e10 tries. kappa = 1/2 FITTED."""
import math, numpy as np
NAME = {name!r}; EXPR = {expr!r}; WRAP = {wrap}; VERTICAL = ("R",); HMUT = {hmut}
_F = dict(sqrt=np.sqrt, log1p=np.log1p, inv1p=lambda x: 1 / (1 + x), sq=lambda x: x * x, pi=math.pi)
_USES_ELL = {ue}
def _law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"]; gg = np.asarray(Q["gg"], float); pos = gb > 0; gq = np.where(pos, gb, 1.0)
    y = gq / a; f = np.clip(np.broadcast_to(gg, gq.shape) / gq, 0.0, 1.0)
    ell = np.broadcast_to(np.asarray(Q["r"], float), gq.shape) * a / 299792458.0 ** 2 if _USES_ELL else y * 0
    with np.errstate(all="ignore"):
        H = HMUT * (eval(EXPR, {{"__builtins__": {{}}}}, dict(_F, y=y, ell=ell, f=f)) * np.ones_like(y))
        v = _law(gq, a * H) if WRAP == 1 else _law(gq * H, a) if WRAP == 2 else _law(gq, a) * H
    return np.where(pos, v, gb)
'''
def full_expr(s, fam): return f"(1.0+f*({s}))" if fam in ("A", "E") else s
def main():
    A = rq3(); A.crg(); sel = json.load(open(os.path.join(LANE, "bf3_final.json")))["selection"]; sel = sel + json.load(open(os.path.join(LANE, "bf3_nearmiss_pick.json"))) if os.path.exists(os.path.join(LANE, "bf3_nearmiss_pick.json")) else sel; cd = os.path.join(LANE, "candidates"); os.makedirs(cd, exist_ok=True); os.makedirs(os.path.join(LANE, "results"), exist_ok=True); RES = {}
    names = ["law_ref"] + [f"F{i + 1}" for i in range(len(sel))]; items = [dict(s="1.0", w=3, fam="H")] + sel
    for t, x in zip(names, items):
        e = full_expr(x["s"], x["fam"]); p = os.path.join(cd, f"{t}{TAG}.py"); open(p, "w").write(TPL.format(name=f"BF3 {t}{TAG}", expr=e, wrap=x["w"], hmut=HMUT, ue="ell" in e)); rf = os.path.join(LANE, "results", f"{t}{TAG}.json")
        if os.path.exists(rf): o = json.load(open(rf))
        else: o = A.scorecard(p, True, True); A.write(o, f"{t}"); o = json.load(open(rf))
        sp = iu.spec_from_file_location(t, p); c0 = iu.module_from_spec(sp); sp.loader.exec_module(c0); RES[t] = dict(form=e, w=x["w"], foot={})
        for ft in FEET:
            r = o["footings"][ft]["rows"]; ks = [k for k in r if k[0] == "B" and ":" in k]; kp = sum(r[k]["label"] == "PASS" for k in ks); kf = {k.split(":")[1]: round(r[k]["Z"], 2) for k in ks if r[k]["label"] == "FAIL"}; zz = lambda k: r[k].get("Z"); nn = {}
            for k in ("A1", "A2", "A3", "A4", "A9", "A10", "A18", "A23a", "A23b", "A5", "A6", "A12", "A13", "A20", "A21", "A24", "A26a", "B1", "B2", "B23", "B24", "B25", "B28", "A30", "C1", "B19", "B20"): nn[k] = dict(label=r.get(k, {}).get("label"), v=r.get(k, {}).get("value"), Z=r.get(k, {}).get("Z"), p=r.get(k, {}).get("p"))
            D = dict(keys=kp, keys_fail=kf, rows=nn, B28_detail={q: r["B28"].get(q) for q in ("label", "M300", "dkappa", "peak", "old") if q in r["B28"]}, counts=o["footings"][ft]["summary"]["counts"], overall=o["footings"][ft]["summary"]["overall"]); RES[t]["foot"][ft] = D; say(f"\n{t} {ft} {e} W{x['w']}: {D['overall']} {D['counts']}; keys {kp}/15 fail {kf}"); say("  " + "; ".join(f"{k} {v['label']} {v['v'] if not isinstance(v['v'], float) else round(v['v'], 3)} Z {None if v['Z'] is None else round(v['Z'], 2)}" for k, v in nn.items())); say("  Bullet", D["B28_detail"])
            for fx in GFALL:
                cw = types.SimpleNamespace(g=lambda Q, fx=fx: c0.g(dict(Q, gg=fx * np.asarray(Q["gb"], float), r=np.where(np.isfinite(np.asarray(Q["r"], float)), Q["r"], 1e21)))); q = A.rows_groups(cw, ft)["B1"]; D[f"groups{fx}"] = q; say(f"  groups f {fx}: {q['label']} {q['value']:+.3f} Z {q['Z']:+.2f}")
            for fx in (.05, .15):
                def gm(Q, fx=fx):
                    q = dict(Q); gb = np.asarray(Q["gb"], float); q["gg"] = fx * gb; q["r"] = np.where(np.isfinite(np.asarray(Q.get("r", gb * np.nan), float)), Q.get("r", gb * 0), 1e21); return c0.g(q)
                try: q = A.rows_mw(types.SimpleNamespace(g=gm, VERTICAL=("R",)), ft); D[f"MW{fx}"] = q; say(f"  MW f {fx}: A15 {q['A15']['label']} {q['A15'].get('value')} Z {q['A15'].get('Z')}; A16 {q['A16']['label']} {q['A16'].get('value')}")
                except Exception as e_: say("  MW", fx, type(e_).__name__, str(e_)[:80])
            for sc in (.5, .25):
                q = A.rows_lens(types.SimpleNamespace(g=lambda Q, sc=sc: c0.g(dict(Q, gg=np.asarray(Q["gg"], float) * sc))), ft)["A30"]; D[f"A30gas{sc}"] = q; say(f"  A30 cov-only, gas x {sc}: {q['value']:.1f}")
            gs_ = 1.32712440018e20 / (9.58 * 149597870700.0) ** 2; a = A0[ft]; rs = np.array([9.58 * 149597870700.0]); vv = float(c0.g(dict(gb=np.array([gs_]), gg=np.array([gs_]), r=rs, a0=a))[0]); D["Saturn_f1_anom"] = vv - gs_; say(f"  Saturn at f = 1: anomaly {vv - gs_:.3e} m/s^2, Z {(vv - gs_) / 9.68e-15:.3g}; law's at f = 0 {float(law(np.array([gs_]), a)[0]) - gs_:.3e}")
    json.dump(RES, open(os.path.join(LANE, f"bf3_holdout{TAG}.json"), "w"), indent=0, sort_keys=True, default=float); OUT.close()
main()
