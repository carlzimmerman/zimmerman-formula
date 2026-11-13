#!/usr/bin/env python3
"""JNT2R (READING.md, 5abea0324b): G1 halo-model part. R_cold(k, z) at the DESI P1D bins under the crossing-speed joint.
FZS1's fzs1_hm.py is executed read-only up to its "checkpointed run" marker (which executes FRZ1's frz1_hm.py prefix
unchanged). The layout assembly (law inside R_set for haloes at or below v*(z), reference elsewhere, FZS1's junction) is
copied from SRJ2's lay_J; the membership is this lane's (jnt2r_common).
  Memberships: P (primary: FZS1's Mb_fold against M_b*(z)), B (bracket B-halo: FRZ1's v_vir against v*(z)),
  V (TW-V: SRJ2's v_vir > v_stiff), N (TW-N: none above), H / D (TW-H / TW-D: primary with v*/2, 2 v*).
  python3 jnt2r_hm.py -> jnt2r_hm.json / .out  (checkpoint jnt2r_hm_partial.json; SIGTERM-safe)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, signal, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); import jnt2r_common as JC
FZD = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius")
SRC = os.path.join(FZD, "fzs1_hm.py"); code = open(SRC).read()
cut = code.index("# ------------------------------------------------------------------ checkpointed run\n")
Z = {"__file__": SRC, "__name__": "fzs1_lib"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), Z)
F, L = Z["F"], Z["L"]; layout, set_z, regime, Bar, rset_com, CUR, Mb_fold = (Z[k] for k in ("layout", "set_z", "regime", "Bar", "rset_com", "CUR", "Mb_fold"))
KK, ZB, FOOTS, VST, at, h = Z["KK"], Z["ZB"], Z["FOOTS"], Z["VST"], Z["at"], Z["h"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()

# ------------------------------------------------------------------ membership (this lane's)
def is_above(mode, hb, ft, z):
    if mode == "N": return False
    if mode == "V": return regime(hb, ft) == "cluster"
    if mode == "B": return F["v_vir"](hb) > JC.vstar(ft, z)
    s = {"P": 1.0, "H": 0.5, "D": 2.0}[mode]
    return JC.above(ft, Mb_fold(hb, ft) / h, z, s)

def lay_J(foot, z, fac, mode):
    def fn(hb):
        if is_above(mode, hb, foot, z):
            CUR[0] = 0.0; rR, MR, inf = layout(hb, foot, mode="Rb"); return rR, MR, dict(inf, R_set=0.0, above=True)
        R = rset_com(hb, foot, z, fac); CUR[0] = R
        rB, MB, inf = layout(hb, foot, mode="B"); rR, MR, _ = layout(hb, foot, mode="Rb"); CUR[0] = 0.0
        if R <= 0 or inf["regime"] == "L": return rR, MR, dict(inf, R_set=R, above=False)
        assert len(rB) == len(rR) and np.array_equal(rB, rR)
        bar = Bar(hb, foot, rB); CB, CR = MB - bar, MR - bar
        i = int(np.argmin(abs(rB - R))); assert abs(rB[i] / R - 1) < 1e-12
        s = CR[i] / CB[i]
        return rB, np.where(rB <= rB[i], bar + s * CB, bar + CR), dict(inf, R_set=R, s=float(s), above=False)
    return fn
def ratios_J(foot, z, fac, mode):
    CUR[0] = 0.0
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb")); PR, _, _ = L["spectra_ta"](UR)
    US, inf = L["U_set"](lay_J(foot, z, fac, mode)); PS, _, _ = L["spectra_ta"](US)
    Rtot = 1 + (PS - PLta) / Pstd; Rbar = 1 + (PR - PLta) / Pstd
    return Rtot, Rbar, Rtot / Rbar, inf

PART = os.path.join(HERE, "jnt2r_hm_partial.json")
RES = json.load(open(PART)) if os.path.exists(PART) else dict(cases={}, KA={}, member={})
def save(): json.dump(RES, open(PART, "w"))
def on_term(sig, frm):
    save(); print("SIGTERM: checkpoint written; rerun to resume", flush=True); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
P("JNT2R G1 halo model, crossing-speed joint. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

# ------------------------------------------------------------------ membership table per z bin (all modes)
for ft in FOOTS:
    for z in ZB:
        key = f"{ft}|{z}"
        if key in RES["member"]: continue
        with contextlib.redirect_stdout(io.StringIO()): set_z(z)
        m = {mode: [bool(is_above(mode, hb, ft, z)) for hb in L["HB"]] for mode in ("P", "B", "V", "H", "D")}
        Ms = [hb["M"] for hb in L["HB"]]
        def lightest(lst): return min((M for M, a in zip(Ms, lst) if a), default=None)
        RES["member"][key] = dict(vstar=JC.vstar(ft, z), lMbstar=math.log10(JC.mbstar(ft, z)), n=len(Ms),
                                  counts={k: int(sum(v)) for k, v in m.items()}, lightest_above_M_h={k: lightest(v) for k, v in m.items()},
                                  P_equals_B=m["P"] == m["B"], P_equals_V=m["P"] == m["V"])
    save()
    P(f"[{ft}] haloes above v*(z) per z bin (P primary / B halo bracket / V = SRJ2 / H / D) of {RES['member'][ft + '|2.2']['n']}: "
      + "; ".join(f"z {z}: v* {RES['member'][f'{ft}|{z}']['vstar']:.0f} km/s, " + "/".join(str(RES['member'][f'{ft}|{z}']['counts'][k]) for k in ('P', 'B', 'V', 'H', 'D')) for z in ZB))

# C4: KA-M for the joint at z 3 (primary)
with contextlib.redirect_stdout(io.StringIO()): set_z(3.0)
err = 0.0; mono = True
for ft in FOOTS:
    for fac in (0.75, 1.0, 1.25, 3.0):
        fn = lay_J(ft, 3.0, fac, "P")
        for hb in L["HB"]:
            r, Mx, _ = fn(hb)
            err = max(err, abs(Mx[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(Mx) >= -1e-9 * hb["Mta"]))
RES["KA"]["C4_KA_M"] = dict(max_rel=err, monotone=mono, pass_=bool(err <= 1e-9 and mono))
P(f"KA4 KA-M (joint, z 3, f 0.75 / 1 / 1.25 / 3): max |M(r_ta) - M_ta| / M_ta {err:.1e}, non-decreasing {mono} -> {'PASS' if RES['KA']['C4_KA_M']['pass_'] else 'FAIL'}")
save()

FG = (0.75, 1.0, 1.25, 1.5, 2.0, 3.0)
CASES = [("KA_0", 0.0, "P")] + [(f"P_f{f:.2f}", f, "P") for f in FG] + [(f"B_f{f:.2f}", f, "B") for f in FG] + \
        [("TWV_f1.00", 1.0, "V"), ("TWN_f1.00", 1.0, "N"), ("TWH_f1.00", 1.0, "H"), ("TWD_f1.00", 1.0, "D")]
for name, fac, mode in CASES:
    for ft in FOOTS:
        key = f"{name}|{ft}"
        if key in RES["cases"]: continue
        if mode == "B" and all(RES["member"][f"{ft}|{z}"]["P_equals_B"] for z in ZB):
            RES["cases"][key] = dict(RES["cases"][f"P_f{fac:.2f}|{ft}"]); RES["cases"][key]["_same_as"] = f"P_f{fac:.2f}"; save(); continue
        rows = {}
        for z in ZB:
            with contextlib.redirect_stdout(io.StringIO()): set_z(z)
            Rt, Rb, Rc, inf = ratios_J(ft, z, fac, mode)
            rows[str(z)] = dict(R_cold=Rc.tolist(), R_cold_at=at(Rc), n_above=sum(1 for i in inf if i.get("above")), n_haloes=len(inf))
        RES["cases"][key] = rows; save()
        P(f"  {name:10s} {ft:9s} R_cold at k 1/3/5/10: z 2.2 " + "/".join(f"{x:.5f}" for x in rows["2.2"]["R_cold_at"]) + "; z 4.4 "
          + "/".join(f"{x:.5f}" for x in rows["4.4"]["R_cold_at"]) + f"; above z 2.2 / 4.4: {rows['2.2']['n_above']} / {rows['4.4']['n_above']}   [{time.time() - T0:.0f} s]")
FZ = json.load(open(os.path.join(FZD, "fzs1_hm.json")))
k0 = {ft: max(float(np.max(np.abs(np.array(RES["cases"][f"KA_0|{ft}"][str(z)]["R_cold"]) - 1))) for z in ZB) for ft in FOOTS}
c1 = {ft: max(float(np.max(np.abs(np.array(RES["cases"][f"TWN_f1.00|{ft}"][str(z)]["R_cold"]) / np.array(FZ["cases"][f"primary|{ft}"][str(z)]["R_cold"]) - 1))) for z in ZB) for ft in FOOTS}
RES["KA"]["KA_0_hm"] = dict(max_abs=k0, pass_=bool(max(k0.values()) <= 1e-12))
RES["KA"]["TWN_hm_vs_FZS1"] = dict(max_rel=c1, pass_=bool(max(c1.values()) <= 1e-10))
P(f"KA4 f 0: max |R_cold - 1| {k0} -> {'PASS' if RES['KA']['KA_0_hm']['pass_'] else 'FAIL'}")
P(f"TW-N (halo model) against FZS1's stored primary R_cold: max rel {c1} -> {'PASS' if RES['KA']['TWN_hm_vs_FZS1']['pass_'] else 'FAIL'}")
RES.update(lane="JNT2R", part="G1 halo model", reading="5abea0324b", k=KK.tolist(), z_bins=ZB, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", seconds=time.time() - T0)
json.dump(RES, open(os.path.join(HERE, "jnt2r_hm.json"), "w"), indent=1)
open(os.path.join(HERE, "jnt2r_hm.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
os.remove(PART); P(f"done ({time.time() - T0:.0f} s)")
