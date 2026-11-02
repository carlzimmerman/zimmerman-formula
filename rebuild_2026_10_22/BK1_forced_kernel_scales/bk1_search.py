#!/usr/bin/env python3
"""BK1 target search. Gate 5 said DOES NOT CERTIFY, so no gate 2 PASS can be issued: raw hits, Z, control rates, near misses. kappa = 1/2 FITTED; not theory closed. --only RUN to run one."""
import csv, gzip, json, math, os, sys, time
import numpy as np
from bk1_engine import *
B = json.load(open("bk1_budget.json")); A0 = dict(canonical=9.360324825027975e-11, alt=1.1312e-10); CC = 2.99792458e8; GG = 6.6743e-11; H0 = .675 * 3.2407793e-18; FB = B["XR"]["f_b"]
def leaves(ft, alpha, fb):
    d = dict(c=CC, G=GG, rho=(2 * A0[ft] / CC) ** 2 / GG, a0=A0[ft])
    if fb: d["f_b"] = FB
    if alpha == "B": d["H0"] = H0
    return d
def dimless(ft):
    F = B[ft]; o = []
    for t in ("K", "D8", "D5"): o += [Window(t, F[t]["value"], F[t]["sigma"]), Window(t + "_2nd", F[t]["value"], F[t]["sigma_hsc"])]
    o.append(Window("FQ", B["FQ"]["value"], B["FQ"]["sigma"])); return o
RUNS = []
for ft in ("canonical", "alt"):
    for al in ("A", "B"):
        RUNS.append((f"{ft}_{al}_dimless", ft, al, True, "none", dimless(ft), True))
        RUNS.append((f"{ft}_{al}_XR", ft, al, False, "none", [Window("XR", B["XR"]["value"], B["XR"]["sigma"]), Window("XR_2nd", B["XR"]["value"], B["XR"]["sigma_2"])], True))
        RUNS.append((f"{ft}_{al}_RHO", ft, al, False, "density", [Window("RHO", B["RHO"]["value"], B["RHO"]["sigma"]), Window("RHO_2nd", B["RHO"]["value"], B["RHO"]["sigma_2"])] + ([Window("PLANT_rho3", (2 * A0[ft] / CC) ** 2 / GG / 3, (2 * A0[ft] / CC) ** 2 / GG / 3e3)] if al == "A" else []), True))
for al in ("A", "B"):
    RUNS.append((f"canonical_{al}_T", "canonical", al, True, "mass", [Window("T", B["T"]["value"] + math.log10(1.989e30), .05, dex=True)], True))
def refs(T, ft, tdim):
    """Log value of the dimensional reference, so the coefficient can be read: density rho, mass c^3/(G sqrt(G rho))."""
    r = (2 * A0[ft] / CC) ** 2 / GG
    return dict(none=0., density=math.log10(r), mass=math.log10(CC ** 3 / (GG * math.sqrt(GG * r))))[tdim]
def coef(T, i, ft, tdim):
    n = T.names; e = T.e[i]; v = float(e @ T.lv + T.c[i]) - refs(T, ft, tdim); r = (2 * A0[ft] / CC) ** 2 / GG
    if "f_b" in n: v -= e[n.index("f_b")] * math.log10(FB)
    if "H0" in n: v -= e[n.index("H0")] * math.log10(H0 / math.sqrt(GG * r))
    return 10 ** v
only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
os.makedirs("runs", exist_ok=True)
for name, ft, al, fb, td, WS, g2 in RUNS:
    if only and only != name: continue
    fn = f"runs/{name}.json"
    if os.path.exists(fn) and not only: continue
    t0 = time.time(); T = Tree(leaves(ft, al, fb))
    for d in (2, 3): T.layer(d)
    H, HG, rows, zh, st = search(T, TARGET_DIMS[td], WS, G2=g2); cum = cumulative(H); span = None
    if td != "none":
        occ = np.where((H[1] + H[2] + H[3] + H[4]) > 0)[0]; span = (LO + BIN * occ.min(), LO + BIN * occ.max()) if len(occ) else None
    R = dict(run=name, footing=ft, alphabet=al, f_b=fb, stats=st, span=span, targets={}); dk = T.dimk(); tk = dkey(TARGET_DIMS[td]); v = T.vals(); M3 = (dk == tk).all(1); idx3 = np.where(M3)[0]
    allc = np.array([coef(T, i, ft, td) for i in idx3[:200000]]) if td == "none" and len(idx3) < 200000 else None
    for w in WS:
        g = grade(cum, w); g["span_null"] = grade(cum, w, span=span) if span else None; g["z_hist_depth4"] = zh[w.name].tolist(); g["sigma"] = w.sigma; g["value"] = w.value
        if HG is not None:
            cg = dict(cum); ch = {6: np.concatenate([[0], np.cumsum(H[1] + H[2] + H[3] + HG)])}; gg = grade(ch, w); g["G2"] = gg["depth"][6]; g["G2_bits"] = bits_of(gg["depth"][6]["ctrl_P"]) if gg["depth"][6]["real"] else None
        m = idx3[(v[idx3] >= w.lo) & (v[idx3] <= w.hi)]; L = []
        for i in m[np.lexsort((np.abs(w.z(v[m])), T.d[m]))]:
            cf = coef(T, i, ft, td); dec = decompose(cf); L.append(dict(depth=int(T.d[i]), expr=T.expr(int(i)), logv=float(v[i]), Z=float(w.z(v[i])), coef=cf, g3_mech=[str(x) for x in dec[:2]]))
        g["hits_le3"] = L; g["g3_mech_le3"] = sum(1 for x in L if x["g3_mech"])
        rr = rows[w.name]
        if rr:
            pr = prune(rr, w, 200000); g["d4_rows_kept"] = int(len(pr[0])); o = np.argsort(np.abs(w.z(pr[0])))[:30]; g["d4_lowest_Z"] = [dict(logv=float(pr[0][j]), Z=float(w.z(pr[0][j])), op=int(pr[1][j]), a=T.expr(int(pr[2][j])), b=T.expr(int(pr[3][j]))) for j in o]
            with gzip.GzipFile(f"runs/{name}_{w.name}_d4.csv.gz", "wb", mtime=0) as f:
                f.write(b"logv,Z,op,i,j\n" + "".join(f"{a:.9f},{float(w.z(np.array(a))):.4f},{b},{c},{d}\n" for a, b, c, d in zip(pr[0][:2000], pr[1][:2000], pr[2][:2000], pr[3][:2000])).encode())
        R["targets"][w.name] = g
    if td == "none":
        vv = v[idx3]; R["mech_rate_le3"] = dict(trees=len(idx3), mech=sum(1 for i in idx3[:20000] if decompose(coef(T, i, ft, td))), sampled=min(20000, len(idx3)))
    R["seconds_not_compared"] = None; json.dump(R, open(fn, "w"), indent=0, sort_keys=True, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print(name, f"{time.time() - t0:.0f}s", st["tried_formal"], {k: (x["dstar"], x.get("bits")) for k, x in R["targets"].items()}, flush=True)
