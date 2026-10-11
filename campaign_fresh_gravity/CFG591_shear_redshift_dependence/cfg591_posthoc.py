#!/usr/bin/env python3
"""CFG591 post-hoc (dated 2026-10-10; NOT a verdict input). Control HZ1 (mass conservation of the PRIMARY) failed at z = 1: in halos whose
supply edge reaches r_ta (capped; log M_ta > 16.1 at z = 1), CFG559's frame_profile_kin adds M_set Delta m(r/r_e) with r_e clamped to r_ta,
so Delta m(1) != 0 at r_ta and M_F(<r_ta) != M_ta.  This script measures what those halos do to R(k, z): the PRIMARY rebuilt with the
kinetic term switched off ONLY in capped halos (their sharp profile conserves mass), vs the as-run PRIMARY.  Same for the DESI variant
(CFG591_DESI=1) when its toy tables exist.
  OMP_NUM_THREADS=4 nice -n 10 python3 cfg591_posthoc.py [-> cfg591_posthoc.out / .json; with CFG591_DESI=1 -> *_DESI.*]
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg591_lib as C
DESI = os.environ.get("CFG591_DESI", "0") == "1"; SUF = "_DESI" if DESI else ""
if DESI:
    import cfg591_desi as DSI
    DSI.activate(*DSI.desi_w0wa())
JT = json.load(open(os.path.join(HERE, f"cfg591_toy{SUF}_results.json")))
JH = json.load(open(os.path.join(HERE, f"cfg591_halo{SUF}_results.json")))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P("CFG591 post-hoc (not a verdict input): effect of the capped-halo mass-conservation failure on R(k, z)" + (" [DESI variant]" if DESI else ""))
res = {}
for z in C.ZNODES:
    H = C.namespace(z); KK = H["KK"]
    C.K9._CACHE.pop("MAIN", None)
    if z == 0.0 and not DESI:
        C.K9.table(False)
    else:
        C.K9._CACHE["MAIN"] = JT["tables"][str(z)]
    Ustd = H["U_std"](); Pstd = H["spectra_std"](Ustd)[0]
    Ulta, _ = H["U_set"](lambda hb: (lambda r: (r, H["M_L"](hb, r), {}))(H["rgrid"](hb, hb["rta"]))); Plta = H["spectra_ta"](Ulta)[0]
    for ft in C.FOOTS:
        sc = C.sc_grid(H, ft, z)
        def fn(hb, _it=iter(sc)):
            s = next(_it); r, M, inf = H["frame_profile_kin"](hb, ft, s, "kin", "primary")
            if inf["capped"]:
                r, M, inf = H["frame_profile_sc"](hb, ft, s); inf["capped_fixed"] = True
            return r, M, inf
        U, infos = H["U_set"](fn)
        R = 1 + (H["spectra_ta"](U)[0] - Plta) / Pstd
        R0 = np.array(JH["R"][str(z)][ft]["PRIMARY"])
        ncap = sum(bool(i.get("capped_fixed")) for i in infos)
        lt = [math.log10(hb["Mta"]) for hb, i in zip(H["HB"], infos) if i.get("capped_fixed")]
        d = float(np.max(np.abs(R - R0)))
        res[f"{z}|{ft}"] = dict(n_capped=ncap, logMta_capped_min=(min(lt) if lt else None), max_abs_dR=d, dR_k1=float(np.interp(1.0, KK, R - R0)))
        P(f"  z {z} {ft:9s}: capped halos {ncap} (log M_ta >= {min(lt):.2f})" if lt else f"  z {z} {ft:9s}: capped halos 0", f"; max |dR| over k = {d:.2e}")
json.dump(res, open(os.path.join(HERE, f"cfg591_posthoc{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg591_posthoc{SUF}.out"), "w").write("\n".join(OUT) + "\n")
