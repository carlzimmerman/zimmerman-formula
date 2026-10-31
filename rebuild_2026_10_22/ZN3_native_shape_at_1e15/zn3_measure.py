#!/usr/bin/env python3
"""ZN3 measurement: ZN1's measure() on the 1e15 runs; merged with ZN1's 1e13 and 1e14 stacks into zn3_shapes.json. At z 0.5 the 1e15 node is its z_f snapshot (FROZEN_CRITERIA.md). kappa = 1/2 FITTED; not theory closed."""
import glob, importlib.util, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); ZD = os.path.join(RB, "ZN1_zooms_to_z0"); _s = importlib.util.spec_from_file_location("zn1_measure", os.path.join(ZD, "zn1_measure.py")); ZM = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = [_a[0]]; _s.loader.exec_module(ZM); sys.argv = _a; measure, FIT, XA, XG = ZM.measure, ZM.FIT, ZM.XA, ZM.XG; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("ZN3 read-outs at 1e15; kappa = 1/2 FITTED; not theory closed"); Z1 = json.load(open(os.path.join(ZD, "zn1_shapes.json"))); RES = {"x": XG.tolist(), "1e13": Z1["1e13"], "1e14": Z1["1e14"], "1e15": {}}
for zs in ("0.50", "0.25", "0.00"):
    rows = []
    for d in sorted(glob.glob(os.path.join(HERE, "runs", "M1e15_s?_ng64"))):
        s = os.path.basename(d); A = np.load(os.path.join(HERE, "runs_zf", s, "snap_zf.npz"), allow_pickle=False) if os.path.exists(os.path.join(HERE, "runs_zf", s, "snap_zf.npz")) else None
        if A is None: continue
        if zs == "0.50": Z = A; zv = json.loads(str(A["meta"]))["zf"]
        else:
            f = os.path.join(d, f"snap_z{zs}.npz")
            if not os.path.exists(f): continue
            Z = np.load(f, allow_pickle=False); zv = float(zs)
        meta = json.loads(str(Z["meta"])); x, m = Z["x"], float(Z["m"]); o = measure(x, m, zv, meta["eps"]); assert len(x) == meta["N"], "K4 N changed"; rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + zv) ** 3; f0, f1 = FIT(x, m, rho, meta["eps"]); rf = meta["rf_phys"]; ca = XA.centre(A["x"], float(A["m"])); ra = np.sort(np.sqrt(((A["x"] - ca) ** 2).sum(1))); g = np.array([0.1, 0.2, 0.5, 1.0, 1.5]) * rf; gr = (np.searchsorted(o["r"], g) / np.maximum(np.searchsorted(ra, g), 1)).tolist(); i2 = np.searchsorted(XG, 1.0); ie = np.searchsorted(XG, o["x_edge"]); slope = float(np.polyfit(np.log(XG[i2:ie]), np.array(o["lnm"])[i2:ie], 1)[0]) if ie > i2 + 3 else float("nan")
        rows.append(dict(seed=s, lgM=math.log10(o["M200"]), R200=o["R200"], M_over_nom=o["M200"] / meta["M"], x_conv=o["x_conv"], x_edge=o["x_edge"], lnm=o["lnm"], c_nfw=(f0.get("c_nfw_fit") if f1 is not None else None), eta=(f1["S"]["eta"] if f1 is not None else None), a=(f1["S"]["a"] if f1 is not None else None), ratio_rf=gr, gamma_out=3 - slope, r_over_rf=o["R200"] / rf, z=zv))
    if not rows: P(f"  z {zs}: none finished"); continue
    lm = np.array([q["lnm"] for q in rows]); RES["1e15"][zs] = dict(n=len(rows), lgM=float(np.median([q["lgM"] for q in rows])), x_edge=min(q["x_edge"] for q in rows), lnm=np.median(lm, axis=0).tolist(), seeds=rows, x=XG.tolist()); md = lambda k: float(np.nanmedian([np.nan if q[k] is None else q[k] for q in rows])); P(f"  M 1e15 z {zs} (snapshot z {rows[0]['z']:.3f}): n {len(rows)}; lg M200 {RES['1e15'][zs]['lgM']:.3f}, M200/M nominal {md('M_over_nom'):.3f}, R200/r_f {md('r_over_rf'):.3f}, x_edge min {RES['1e15'][zs]['x_edge']:.2f}; c_nfw {md('c_nfw'):.2f}, eta {md('eta'):.2f}, a {md('a'):.2f}; slope past R200 {md('gamma_out'):.2f}; M(<r)/M(<r, z_f) at r/r_f 0.1, 0.2, 0.5, 1, 1.5: " + ", ".join(f"{float(np.median([q['ratio_rf'][k] for q in rows])):.3f}" for k in range(5)))
json.dump(RES, open(os.path.join(HERE, "zn3_shapes.json"), "w")); open(os.path.join(HERE, "zn3_readouts.out"), "w").write("\n".join(OUT) + "\n")
