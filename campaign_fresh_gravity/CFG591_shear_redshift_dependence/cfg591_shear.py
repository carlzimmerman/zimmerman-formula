#!/usr/bin/env python3
"""CFG591 (FROZEN_CRITERIA.md sections 2-5): CFG590's cosmic-shear projection with R(k) -> R(k, z).
cfg590_shear.py is exec'd read-only up to its main block (CAMB HMcode-2020 DMO + BAHAMAS feedback, M1 Limber A_eff, M2, systematics,
classify / judge / full_report / crossings / S8-eq).  ONE function is replaced: R_of.  For a 2-D table (z nodes x k) it interpolates
linearly in z (r0 + w (r1 - r0)) at each Limber lens-plane z (M2: z = 0.5), then applies CFG590's own R_of in k.  z > 1: R(k, 1) held
(PRIMARY rule); bracket R = 1 for z > 1 (reported; HIGH-Z-TAIL-SENSITIVE flag).
  OMP_NUM_THREADS=2 nice -n 10 python3 cfg591_shear.py                 -> cfg591_shear.out, cfg591_results.json
  CFG591_MUTATE=1 OMP_NUM_THREADS=2 nice -n 10 python3 cfg591_shear.py -> *_MUTATE.out / *_MUTATE.json (exit 1 = all teeth bite)
kappa = 1/2 FITTED; footings never pooled; flat a0; cold energy mass required; not theory closed.  Nothing downloaded."""
import os, sys, io, json, math, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG591_MUTATE", "0") == "1"
DESI = os.environ.get("CFG591_DESI", "0") == "1"            # ADDENDUM 1 variant (w0wa background in CAMB, R from the DESI halo run)
SUF = ("_DESI" if DESI else "") + ("_MUTATE" if MUT else "")
D590 = os.path.join(LANES, "CFG590_framework_pk_vs_cosmic_shear")
P590 = os.path.join(D590, "cfg590_shear.py")
J590 = json.load(open(os.path.join(D590, "cfg590_results.json")))
JH = json.load(open(os.path.join(HERE, "cfg591_halo_DESI_results.json" if DESI else "cfg591_halo_results.json")))
sys.path.insert(0, HERE)
if DESI:
    import cfg591_desi as DSI
    W0, WA = DSI.desi_w0wa() if not MUT else (-1.0, 0.0)     # MD2 runs the DESI code path at (w0, wa) = (-1, 0)
ZN = np.array(JH["z_nodes"], float)

os.environ.pop("CFG590_MUTATE", None)
src = open(P590).read(); cut = src.index("\nif not MUT:")
if DESI:                                                    # ADDENDUM 1: the ONE textual insertion (CAMB w0wa, PPF)
    assert src.count("num_massive_neutrinos=0)") == 1
    src = src.replace("num_massive_neutrinos=0)", f"num_massive_neutrinos=0); p.set_dark_energy(w={W0!r}, wa={WA!r}, dark_energy_model='ppf')")
    cut = src.index("\nif not MUT:")
H = {"__file__": P590, "__name__": "cfg590_ro"}
exec(compile(src[:cut], "cfg590_ro", "exec"), H)        # prints CFG590's header + controls C1-C4 into H["OUT"]
P = H["P"]; DATA, TFULL, TFID = H["DATA"], H["TFULL"], H["TFID"]
H["OUT"].append("")
P("CFG591: CFG590's projection with R(k) -> R(k, z) from the epoch halo model (z nodes " + ", ".join(f"{z:g}" for z in ZN) + ")" + (" [MUTATE]" if MUT else ""))
if DESI:
    P(f"[ADDENDUM 1 DESI-tracking variant: CAMB w0wa PPF (w0, wa) = ({W0}, {WA}); R(k, z) from cfg591_halo_DESI_results.json; a0(z) = a0(0) sqrt(rho_DE ratio)]")
P("kappa = 1/2 FITTED; footings never pooled; " + ("a0(z) tracking DESI w0wa (ADDENDUM 1 variant)" if DESI else "flat a0 (w = -1)") + "; nu_mono; candidate B; cold energy MASS still required; not theory closed.")
assert np.allclose(np.array(JH["k"]), H["KR"], rtol=0, atol=1e-15), "k grid mismatch"
ORIG_R_of = H["R_of"]; ZG = H["ZG"]; ONES = H["ONES"]
STATE = {"tail": "hold"}

def Rz_at(Rt, z):
    if z > ZN[-1]:
        return Rt[-1] if STATE["tail"] == "hold" else ONES
    i = min(int(np.searchsorted(ZN, z, side="right")) - 1, len(ZN) - 2)
    w = (z - ZN[i]) / (ZN[i + 1] - ZN[i])
    return Rt[i] + w * (Rt[i + 1] - Rt[i])

def R_of_z(Rarr, k):
    Rarr = np.asarray(Rarr, float)
    if Rarr.ndim == 1:
        return ORIG_R_of(Rarr, k)
    k = np.asarray(k, float)
    if k.ndim == 2:                         # Limber grid [ell, z_j], column j at ZG[j]
        out = np.empty_like(k)
        for j in range(k.shape[1]):
            out[:, j] = ORIG_R_of(Rz_at(Rarr, ZG[j]), k[:, j])
        return out
    return ORIG_R_of(Rz_at(Rarr, 0.5), k)   # M2 (z = 0.5)
H["R_of"] = R_of_z

def Rtab(foot, model):
    return np.array([JH["R"][f"{float(z)}"][foot][model] for z in ZN])
MAP590 = {"PRIMARY": "PRIMARY CFG559 kin", "CFG557_TESTED": "CFG557 TESTED", "CFG556_cen": "CFG556 census|cen (sharp)",
          "CFG556_emg": "CFG556 census|emg", "CFG556_r200scope": "CFG556 r200scope (reported)"}
MAINLINE = ["CFG557_TESTED", "CFG556_cen", "CFG556_emg"]
SURVIVORS = ["CFG556_emg", "CFG556_r200scope"]
RESULT = dict(lane="CFG591", date="2026-10-10", mutate=MUT, camb=H["camb"].__version__, data=DATA, z_nodes=ZN.tolist(), T_full=TFULL, T_fid=TFID,
              controls_cfg590=H["CONTROLS"], halo_controls=JH["controls"], models={})

def _clean(o):
    if isinstance(o, dict): return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.bool_): return bool(o)
    return o

if not MUT:
    lc = H["full_report"]("LCDM (R = 1), same feedback", None, do_s8=True)
    RESULT["models"]["LCDM-DMO"] = lc
    for foot in ("canonical", "alt"):
        P(f"\n===================== footing {foot} =====================")
        P("  R(k=1, z) PRIMARY: " + "  ".join(f"z {z:g}: {JH['info'][str(float(z))]['models'][f'{foot}|PRIMARY']['R_at']['1.0']:.3f}" for z in ZN))
        for nm in ["PRIMARY"] + MAINLINE + ["CFG556_r200scope"]:
            Rt = Rtab(foot, nm)
            rr = H["full_report"](f"{foot} | {nm} with R(k, z)", Rt, do_s8=(nm == "PRIMARY"), do_sys=True)
            rr["dA_vs_LCDM_M1"] = {T: {d: rr["A_table"][T][f"A_M1_{d}"] - lc["A_table"][T][f"A_M1_{d}"] for d in DATA} for T in ("off", "7.8", "8.3")}
            f590 = J590["models"][f"{foot}|{MAP590[nm]}"]
            # A_eff-equivalent scaling vs CFG590's fixed-R excess
            sA = {}
            for T in (() if DESI else ("off", "7.8", "8.3")):
                sA[T] = {d: (rr["A_table"][T][f"A_M1_{d}"] - lc["A_table"][T][f"A_M1_{d}"]) / (f590["A_table"][T][f"A_M1_{d}"] - J590["models"]["LCDM-DMO"]["A_table"][T][f"A_M1_{d}"])
                         if abs(f590["A_table"][T][f"A_M1_{d}"] - J590["models"]["LCDM-DMO"]["A_table"][T][f"A_M1_{d}"]) > 1e-6 else None for d in DATA}
            rr["s_A_vs_cfg590_fixed"] = sA; rr["cfg590_fixedR_class_M1"] = f590["class_M1"]; rr["cfg590_fixedR_final"] = f590.get("final_class")
            P(f"  excess dA (M1) vs LCDM: off KiDS {rr['dA_vs_LCDM_M1']['off']['KiDS']:+.3f} DES {rr['dA_vs_LCDM_M1']['off']['DES']:+.3f}; T8.3 KiDS {rr['dA_vs_LCDM_M1']['8.3']['KiDS']:+.3f} DES {rr['dA_vs_LCDM_M1']['8.3']['DES']:+.3f}"
              + ("" if DESI else "; s_A (vs CFG590 fixed R): " + "; ".join(f"{T} " + "/".join("n/a" if v is None else f"{v:.3f}" for v in sA[T].values()) for T in sA))
              + f"; CFG590 fixed-R class {f590['class_M1']}")
            if nm in ("PRIMARY", "CFG556_emg", "CFG556_r200scope"):
                STATE["tail"] = "one"
                cls_t, _, zmx = H["judge"](Rt)
                sysc = {"M2": H["judge"](Rt, "M2")[0], "lmax1000": H["judge"](Rt, lmax=1000)[0], "lmax3000": H["judge"](Rt, lmax=3000)[0],
                        "nz-0.1": H["judge"](Rt, dz=-0.1)[0], "nz+0.1": H["judge"](Rt, dz=+0.1)[0]}
                fin_t = "NOT DIAGNOSTIC" if any(v != cls_t for v in sysc.values()) else cls_t
                STATE["tail"] = "hold"
                rr["tail_R1_beyond_z1"] = dict(class_M1=cls_t, final_class=fin_t, min_Zmax=min(zmx.values()), systematics=sysc)
                rr["high_z_tail_sensitive"] = bool(cls_t != rr["class_M1"])
                P(f"  tail bracket (R = 1 for z > 1): M1 {cls_t} (min Zmax {min(zmx.values()):.2f}), final {fin_t} -> HIGH-Z-TAIL-SENSITIVE: {rr['high_z_tail_sensitive']}")
            RESULT["models"][f"{foot}|{nm}"] = rr
        prim = RESULT["models"][f"{foot}|PRIMARY"]
        vs = {n: RESULT["models"][f"{foot}|{n}"]["class_M1"] for n in MAINLINE}
        prim["variant_classes"] = vs; prim["variant_sensitive"] = any(v != prim["class_M1"] for v in vs.values())
        prim["cfg590_full_kin_fixedR_class"] = J590["models"][f"{foot}|CFG559 full_kin"]["class_M1"]
        P(f"\n  VERDICT [{foot}] framework PRIMARY with R(k, z): {prim['final_class']} (M1 {prim['class_M1']}, min Zmax {min(prim['Zmax_by_T'].values()):.2f}); "
          f"mainline variants {vs}{' -> VARIANT-SENSITIVE' if prim['variant_sensitive'] else ''}; HIGH-Z-TAIL-SENSITIVE {prim['high_z_tail_sensitive']}; "
          f"CFG559 full_kin carried at fixed z = 0 R (not rerun): {prim['cfg590_full_kin_fixedR_class']}")
        P(f"  survivors: emergent edge {RESULT['models'][f'{foot}|CFG556_emg']['final_class']} (M1 {RESULT['models'][f'{foot}|CFG556_emg']['class_M1']}); "
          f"r200m scope {RESULT['models'][f'{foot}|CFG556_r200scope']['final_class']} (M1 {RESULT['models'][f'{foot}|CFG556_r200scope']['class_M1']})")
    P(f"\n  VERDICT LCDM-DMO (same rule, same feedback): {lc['final_class']} (M1 {lc['class_M1']})")
    RESULT["verdict"] = {"LCDM-DMO": lc["final_class"], **{f: RESULT["models"][f"{f}|PRIMARY"]["final_class"] for f in ("canonical", "alt")},
                         "survivors": {f"{f}|{n}": RESULT["models"][f"{f}|{n}"]["final_class"] for f in ("canonical", "alt") for n in SURVIVORS}}
elif DESI:
    teeth = {}
    Ts = [None] + TFULL
    # MD2: DESI code path at (w0, wa) = (-1, 0), R = 1 -> CFG590's LCDM A_eff table
    AL = {("off" if T is None else str(T)): {"A_M1_KiDS": H["A_M1"]("KiDS", None, T), "A_M1_DES": H["A_M1"]("DES", None, T), "A_M2": H["A_M2"](None, T)} for T in Ts}
    ref = J590["models"]["LCDM-DMO"]["A_table"]
    md2 = max(abs(AL[t][c] - ref[t][c]) for t in AL for c in AL[t])
    teeth["MD2"] = bool(md2 <= 1e-6)
    P(f"  MD2 DESI path at (w0, wa) = (-1, 0), R = 1: max |A - A_CFG590,LCDM| = {md2:.2e} (<= 1e-6) -> {'BITES' if teeth['MD2'] else 'FAILS'}")
    # MD1: background at (-1, 0) vs the w = -1 machinery, z = 0.5
    import cfg591_lib as CL
    Lb = CL.L; a5 = 1 / 1.5
    ref1 = dict(D=Lb.Dgrow(a5) / Lb.Dgrow(1.0), age=Lb.age(a5), DODE=CL.epoch(0.5).Delta_ta)
    Hn = CL.namespace(0.5); ref1["sc"] = {ft: CL.sc_grid_compute(Hn, ft, 0.5) for ft in CL.FOOTS}
    DSI.activate(-1.0, 0.0)
    new1 = dict(D=Lb.Dgrow(a5) / Lb.Dgrow(1.0), age=Lb.age(a5), DODE=CL.epoch(0.5).Delta_ta)
    Hd = CL.namespace(0.5); new1["sc"] = {ft: CL.sc_grid_compute(Hd, ft, 0.5) for ft in CL.FOOTS}
    md1 = dict(D=abs(new1["D"] / ref1["D"] - 1), age=abs(new1["age"] / ref1["age"] - 1), DODE=abs(new1["DODE"] / ref1["DODE"] - 1),
               sc=float(max(np.max(np.abs(new1["sc"][ft] / ref1["sc"][ft] - 1)) for ft in CL.FOOTS)))
    teeth["MD1"] = bool(all(v <= 1e-6 for v in md1.values()))
    P(f"  MD1 DESI background at (-1, 0) vs w = -1, z = 0.5: rel |dD| {md1['D']:.1e}, |dage| {md1['age']:.1e}, |dDelta_ODE| {md1['DODE']:.1e}, max |ds_c| {md1['sc']:.1e} (each <= 1e-6) -> {'BITES' if teeth['MD1'] else 'FAILS'}")
    RESULT["mutate"] = dict(teeth=teeth, MD1=md1, MD2_max_dA=md2)
    P(f"\nMUTATE (ADDENDUM 1): all teeth bite: {all(teeth.values())}")
else:
    teeth = {}
    Ts = [None] + TFULL
    def Atab(R):
        return {("off" if T is None else str(T)): {"A_M1_KiDS": H["A_M1"]("KiDS", R, T), "A_M1_DES": H["A_M1"]("DES", R, T), "A_M2": H["A_M2"](R, T)} for T in Ts}
    # MZ1: R(k, z) := R(k, 0) at every node reproduces CFG590
    d1 = 0.0; cls_ok = True; rows = {}
    for foot in ("canonical", "alt"):
        for nm, n590 in MAP590.items():
            R0 = np.array(JH["R"]["0.0"][foot][nm]); Rt = np.tile(R0, (len(ZN), 1))
            A = Atab(Rt); ref = J590["models"][f"{foot}|{n590}"]
            dd = max(abs(A[t][c] - ref["A_table"][t][c]) for t in A for c in A[t])
            cm1 = H["judge"](Rt)[0]
            ok = cm1 == ref["class_M1"]
            if "final_class" in ref:
                sysc = [H["judge"](Rt, "M2")[0], H["judge"](Rt, lmax=1000)[0], H["judge"](Rt, lmax=3000)[0], H["judge"](Rt, dz=-0.1)[0], H["judge"](Rt, dz=+0.1)[0]]
                fin = "NOT DIAGNOSTIC" if any(v != cm1 for v in sysc) else cm1
                ok = ok and fin == ref["final_class"]
            else:
                fin = None
            rows[f"{foot}|{nm}"] = dict(max_dA=dd, class_M1=cm1, final=fin, ref_class_M1=ref["class_M1"], ref_final=ref.get("final_class"))
            d1 = max(d1, dd); cls_ok = cls_ok and ok
            P(f"  MZ1 {foot:9s} {nm:17s}: max |A - A_CFG590| = {dd:.2e}; class {cm1}/{fin} vs CFG590 {ref['class_M1']}/{ref.get('final_class')}")
    teeth["MZ1"] = bool(d1 <= 1e-12 and cls_ok)
    P(f"  MZ1 R(k, z) = R(k, 0): max |dA| {d1:.2e} (<= 1e-12), classes equal {cls_ok} -> {'BITES' if teeth['MZ1'] else 'FAILS'}")
    # MZ2: R = 1 (2-D) reproduces LCDM
    Rt1 = np.ones((len(ZN), len(H["KR"])))
    A1 = Atab(Rt1); AL = Atab(None)
    d2 = max(abs(A1[t][c] - AL[t][c]) for t in A1 for c in A1[t])
    c1, cl = H["judge"](Rt1)[0], H["judge"](None)[0]
    teeth["MZ2"] = bool(d2 <= 1e-12 and c1 == cl)
    P(f"  MZ2 R = 1 (2-D table): max |A - A_LCDM| = {d2:.2e}; class {c1} vs LCDM {cl} -> {'BITES' if teeth['MZ2'] else 'FAILS'}")
    RESULT["mutate"] = dict(teeth=teeth, MZ1_max_dA=d1, MZ1_rows=rows, MZ2_max_dA=d2, MZ2_class=c1, LCDM_class=cl)
    P(f"\nMUTATE: all teeth bite: {all(teeth.values())}")

open(os.path.join(HERE, f"cfg591_shear{SUF}.out"), "w").write("\n".join(H["OUT"]) + "\n")
json.dump(_clean(RESULT), open(os.path.join(HERE, f"cfg591_results{SUF}.json"), "w"), indent=1)
if MUT:
    sys.exit(1 if all(RESULT["mutate"]["teeth"].values()) else 0)
