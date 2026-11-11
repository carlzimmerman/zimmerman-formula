#!/usr/bin/env python3
"""FRZ1R gate: SHARED MACHINERY. Set-up copied from HLF1's hlf1_forest.py (the record's ss1_cosmo.forest_eval executed
read-only on DESI DR1 P1D, reference replaced by form B's own CLASS spectrum, F1A B2 cold fit). Only the ratio R_cold(k, z)
fed to it is FRZ1R's own (frz1r_hm_<foot>.json). Usage: nice -n 19 python3 frz1r_forest.py <foot>
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, io, contextlib, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.linalg import cho_factor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion")
CO1 = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed")
F1AD = os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
os.environ["SS1_FOOT"] = FOOT; os.environ.pop("SS1_MUTATE", None)
sys.path.insert(0, SS1); src = open(os.path.join(SS1, "ss1_cosmo.py")).read(); cut = src.index("# ================================================================== run")
ns = {"__file__": os.path.join(SS1, "ss1_cosmo.py"), "__name__": "ss1c_frz1r"}; _a = sys.argv; sys.argv = ["ss1_cosmo.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "ss1c", "exec"), ns)
sys.argv = _a
signal.signal(signal.SIGTERM, lambda s, f: sys.exit(143))
Class, KG, ZG, forest_setup, forest_eval = (ns[k] for k in ("Class", "KG", "ZG", "forest_setup", "forest_eval"))
CLIGHT = 299792.458
FD = forest_setup(); md5ok = FD["md5"] == "33d7fc21bfd3d745ed71a0bbe80ca433"
def class_bg(Mx):
    b = Mx.get_background(); z = b['z'][::-1]; Hh = b['H [1/Mpc]'][::-1] * CLIGHT; DM = b['comov. dist.'][::-1]; m = z <= 3600
    return dict(z=z[m], H=Hh[m], DM=DM[m])
pr = json.load(open(os.path.join(F1AD, "parts", f"fit_B2_{FOOT}_cold.json")))["pars"]
MB = Class()
MB.set({'output': 'tCl,lCl,mPk', 'l_max_scalars': ns["LMAX"] + 100, 'h': pr["h"], 'omega_b': pr["ob"], 'omega_cdm': pr["oc"], 'A_s': math.exp(pr["lnA"]) * 1e-10,
        'n_s': pr["ns"], 'tau_reio': pr["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 210.0, 'z_max_pk': ns["ZPK"]})
MB.compute(); BGB = class_bg(MB); HB = pr["h"]
ns["M"] = MB; ns["REFBG"] = BGB
ZB = [float(z) for z in FD["ZB"]]
def amp(Rz_by_bin, kh_grid):
    """Rz_by_bin: {bin z: power ratio on kh_grid}; each ZG column gets the ratio of its nearest DESI bin."""
    out = np.empty((len(KG), len(ZG))); kh = KG / HB
    for j, z in enumerate(ZG):
        zb = min(ZB, key=lambda q: abs(q - z)); R = np.interp(np.log(kh), np.log(kh_grid), np.asarray(Rz_by_bin[zb], float))
        out[:, j] = np.sqrt(np.maximum(R, 0.0))
    return out
def perbin(A):
    res = {}
    cf, lower = FD["CF"]; U = np.tril(cf).T if lower else np.triu(cf); C = U.T @ U
    for z in FD["ZB"]:
        s_ = FD["zs"] == z
        sub = dict(FD, ZB=np.array([z]), zs=FD["zs"][s_], ks=FD["ks"][s_], Pd=FD["Pd"][s_], NB=int(s_.sum()), CF=cho_factor(C[np.ix_(s_, s_)]))
        res[f"{z:.1f}"] = float(forest_eval(sub, BGB, A)["dchi2"])
    return res
RES = dict(lane="FRZ1R", footing=FOOT, md5_ok=md5ok, gate="shared: ss1_cosmo.forest_eval via HLF1 set-up", note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
ONE = np.ones((len(KG), len(ZG)))
RES["V_R1"] = float(forest_eval(FD, BGB, ONE)["dchi2"]); P(f"[{FOOT}] R = 1: dchi2 {RES['V_R1']:.3e}; md5 ok {md5ok}")
HM = json.load(open(os.path.join(CO1, "co1_hm.json"))); KH = np.array(HM["k"]); Rc = HM["primary"][FOOT]["R_cold"]
RES["V_CO1_held"] = float(forest_eval(FD, BGB, amp({z: Rc for z in ZB}, KH))["dchi2"]); P(f"[{FOOT}] CO1 z 0 R_cold held: dchi2 {RES['V_CO1_held']:.2f}")
MY = json.load(open(os.path.join(HERE, f"frz1r_hm_{FOOT}.json"))); KM = np.array(MY["k"])
RES["V_own_z0_held"] = float(forest_eval(FD, BGB, amp({z: MY["z0"]["R_cold"] for z in ZB}, KM))["dchi2"]); P(f"[{FOOT}] own z 0 R_cold held: dchi2 {RES['V_own_z0_held']:.2f}")
for var in ("L", "V", "shell"):
    A = amp({z: MY[var][f"{z:.1f}"]["R_cold"] for z in ZB}, KM)
    r = forest_eval(FD, BGB, A); pb = perbin(A)
    RES[var] = dict(dchi2=float(r["dchi2"]), r_min=float(r["r_min"]), r_max=float(r["r_max"]), per_bin=pb)
    P(f"[{FOOT}] reading {var}: dchi2 {r['dchi2']:.2f} (amp ratio {r['r_min']:.5f}-{r['r_max']:.5f}); per bin " + " ".join(f"{k}:{v:.2f}" for k, v in pb.items()))
A = amp({z: (MY["MUTATE_a0_unscaled_z3"]["R_cold"] if abs(z - 3.0) < 1e-9 else MY["L"][f"{z:.1f}"]["R_cold"]) for z in ZB}, KM)
RES["MUTATE_a0_unscaled_z3_bin_swapped"] = float(forest_eval(FD, BGB, A)["dchi2"])
ok = md5ok and RES["V_R1"] == 0.0 and abs(RES["V_CO1_held"] - {"canonical": 160.74, "alt": 1025.57}[FOOT]) <= 0.5 and MY["MUTATE_bites"]
RES["label"] = ("FOREST ROW HOLDS" if RES["L"]["dchi2"] <= 4 else "FOREST ROW FAILS") if ok else "NO VERDICT"
P(f"[{FOOT}] gate validation ok {ok}; label (reading L, gate dchi2 <= 4): {RES['label']}")
json.dump(RES, open(os.path.join(HERE, f"frz1r_forest_{FOOT}.json"), "w"), indent=1)
open(os.path.join(HERE, f"frz1r_forest_{FOOT}.out"), "w").write("\n".join(OUT) + "\n")
