"""CFG819 step 1 (DERIVATION ONLY, no lensing score): the framework's own splashback of free cold energy.
From CFG818/815-P's Infall machinery (split H-EX, eROSITA retention, relation M_cond), for the median cluster of each eRASS1 gas
tercile: per free element, apocentre r_a in the final potential; the free-mass density profile (Method A orbit average) and its
steepest logarithmic slope = r_sp; compare r_sp with the eRASS1 band radii (MID = 0.48-1.24 Mpc; OUTER 1.24-3 Mpc)."""
import os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
os.environ["CFG818_MODE"] = "defs"; os.environ["CFG818_SNAP"] = "0"
src = os.path.join(LANES, "CFG818_unrelaxed_free_placement", "cfg818.py")
txt = open(src).read().split("# ============================================================================================ eRASS1 (CFG687)")[0]
G = {"__file__": src, "__name__": "d"}; exec(compile(txt, src, "exec"), G)
L = G["L"]; d = G["_d687"]; mg = d["mg"]; q = np.quantile(mg, [1 / 3, 2 / 3])
T = [mg <= q[0], (mg > q[0]) & (mg <= q[1]), mg > q[1]]
EDG = G["EDGES"]
cap = {}
class Probe(G["InfallSnap"]):
    def final_profile(self, nr=500, ntheta=160):
        super().final_profile(nr, ntheta); cap["I"] = self; return self
G["InfallSnap"] = Probe
for lab, t in zip(("light", "middle", "heavy"), T):
    idx = np.where(t)[0]; i = int(idx[np.argsort(mg[idx])[len(idx) // 2]])
    Mg = G["_beta_gas"](i); z = float(d["z"][i]); R5 = float(d["R500"][i])
    G["cluster_runs"](Mg, 0.2, z, R5 * 1000.0)
    I = cap["I"]; rg = I.rg / 1000.0; Mr = I.M_res_g                    # Mpc, Msun
    if Mr[-1] <= 0:
        print(f"{lab:6s}: cluster {i}, R500 {R5:.2f} Mpc: no free mass"); continue
    rho = np.gradient(Mr, rg) / (4 * np.pi * rg ** 2); ok = rho > 0
    sl = np.gradient(np.log(np.where(ok, rho, 1e-300)), np.log(rg))
    win = ok & (rg > 0.05) & (rg < 0.9 * I.rta / 1000.0)
    rsp = float(rg[win][np.argmin(sl[win])]) if win.any() else np.nan
    half = float(np.interp(0.5 * Mr[-1], Mr, rg))
    band = "MID" if 0.48 <= rsp <= 1.24 else ("OUTER" if 1.24 < rsp <= 3.0 else ("INNER" if rsp < 0.48 else "beyond"))
    print(f"{lab:6s}: cluster {i}, R500 {R5:.2f} Mpc, r_ta {I.rta / 1000:.1f} Mpc, free {I.M_res_tot / I.supply_turned:.2f} of supply; "
          f"free half-mass radius {half:.2f} Mpc; steepest slope {sl[win].min():.2f} at r_sp = {rsp:.2f} Mpc ({rsp / R5:.2f} R500, {rsp / (I.rta / 1000):.3f} r_ta) -> {band} band")
print(f"band edges (Mpc): {np.round(EDG, 2)}")
