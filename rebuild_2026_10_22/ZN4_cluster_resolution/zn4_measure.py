#!/usr/bin/env python3
"""ZN4 measurement: ZN1's measure() on the ng 80 runs at 1e14 and 1e15, merged with ZN1's 1e13 stack into zn4_shapes.json. A z 0.5 node missing at a mass is its z_f snapshot, as in ZN3. kappa = 1/2 FITTED; not theory closed."""
import glob, importlib.util, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); ZD = os.path.join(RB, "ZN1_zooms_to_z0"); _s = importlib.util.spec_from_file_location("zn1_measure", os.path.join(ZD, "zn1_measure.py")); ZM = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = [_a[0]]; _s.loader.exec_module(ZM); sys.argv = _a; measure, FIT, XA, XG = ZM.measure, ZM.FIT, ZM.XA, ZM.XG; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("ZN4 read-outs, ng 80 at 1e14 and 1e15; kappa = 1/2 FITTED; not theory closed"); Z1 = json.load(open(os.path.join(ZD, "zn1_shapes.json"))); RES = {"x": XG.tolist(), "1e13": Z1["1e13"], "1e14": {}, "1e15": {}}
for M in ("1e14", "1e15"):
    for zs in ("0.50", "0.25", "0.00"):
        rows = []
        for d in sorted(glob.glob(os.path.join(HERE, "runs", f"M{M}_s?_ng80"))):
            s = os.path.basename(d); f = os.path.join(d, f"snap_z{zs}.npz"); A = np.load(os.path.join(HERE, "runs_zf", s, "snap_zf.npz"), allow_pickle=False)
            if os.path.exists(f): Z = np.load(f, allow_pickle=False); zv = float(zs)
            elif zs == "0.50": Z = A; zv = json.loads(str(A["meta"]))["zf"]
            else: continue
            meta = json.loads(str(Z["meta"])); x, m = Z["x"], float(Z["m"]); o = measure(x, m, zv, meta["eps"]); assert len(x) == meta["N"], "K4 N changed"; rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + zv) ** 3; f0, f1 = FIT(x, m, rho, meta["eps"]); i2 = np.searchsorted(XG, 1.0); ie = np.searchsorted(XG, o["x_edge"]); slope = float(np.polyfit(np.log(XG[i2:ie]), np.array(o["lnm"])[i2:ie], 1)[0]) if ie > i2 + 3 else float("nan")
            rows.append(dict(seed=s, lgM=math.log10(o["M200"]), R200=o["R200"], M_over_nom=o["M200"] / meta["M"], x_conv=o["x_conv"], x_edge=o["x_edge"], lnm=o["lnm"], c_nfw=(f0.get("c_nfw_fit") if f1 is not None else None), eta=(f1["S"]["eta"] if f1 is not None else None), a=(f1["S"]["a"] if f1 is not None else None), gamma_out=3 - slope, z=zv))
        if not rows: P(f"  {M} z {zs}: none finished"); continue
        RES[M][zs] = dict(n=len(rows), lgM=float(np.median([q["lgM"] for q in rows])), x_edge=min(q["x_edge"] for q in rows), lnm=np.median(np.array([q["lnm"] for q in rows]), axis=0).tolist(), seeds=rows, x=XG.tolist()); md = lambda k: float(np.nanmedian([np.nan if q[k] is None else q[k] for q in rows])); P(f"  M {M} z {zs} (snapshot z {rows[0]['z']:.3f}): n {len(rows)}; lg M200 {RES[M][zs]['lgM']:.3f}, M200/M nominal {md('M_over_nom'):.3f}, x_edge min {RES[M][zs]['x_edge']:.2f}, x_conv {md('x_conv'):.4f}; c_nfw {md('c_nfw'):.2f}, eta {md('eta'):.2f}, a {md('a'):.2f}; slope past R200 {md('gamma_out'):.2f}")
json.dump(RES, open(os.path.join(HERE, "zn4_shapes.json"), "w")); open(os.path.join(HERE, "zn4_readouts.out"), "w").write("\n".join(OUT) + "\n")
