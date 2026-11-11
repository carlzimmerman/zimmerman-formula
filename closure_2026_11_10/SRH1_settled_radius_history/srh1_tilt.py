#!/usr/bin/env python3
"""SRH1 tilt extension, reported only (FROZEN_CRITERIA.md section 1 item 4; AMENDMENT_A1.md, post hoc): f(z) = f0 (1 + z)^beta.
G4 for the frozen tilt cases (beta -1, -0.5, +0.5; f0 0.5, 0.75, 1.0) and for A1's cases (beta -1: f0 1.25, 1.5, 2.0; beta -0.5:
f0 1.25, 1.5); G1 for A1's cases (FZS1's halo model through srh1_hm.py's prefix, then FRZ1's forest gate per footing, read-only);
G2 / G3 coverage from srh1_rc.json. Executes srh1_lens.py's prefix (ONE1's machinery, this lane's settled-halo table).
  nice -n 10 python3 srh1_tilt.py -> srh1_tilt.json / .out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib
sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__)); _LS = os.path.join(_HERE, "srh1_lens.py"); _src = open(_LS).read()
exec(compile(_src[:_src.index("# ---------------- runs, checkpointed\n")], _LS, "exec"), globals())
LEJ = json.load(open(os.path.join(HERE, "srh1_lens.json"))); RCJ = json.load(open(os.path.join(HERE, "srh1_rc.json")))
FOJ = {ft: json.load(open(os.path.join(HERE, f"srh1_forest_{ft}.json"))) for ft in FOOT}
TILTS = [(b, f0, "frozen") for b in (-1.0, -0.5, 0.5) for f0 in (0.5, 0.75, 1.0)] + [(-1.0, 1.25, "A1"), (-1.0, 1.5, "A1"), (-1.0, 2.0, "A1"), (-0.5, 1.25, "A1"), (-0.5, 1.5, "A1")]
nm = lambda b, f0: f"tilt_b{b:+.1f}_f{f0:.2f}"
def table_t(ft, f0, b):
    T = np.empty((len(LMG), len(ZG), len(UT)))
    for i, lm in enumerate(LMG):
        for j, z in enumerate(ZG):
            pc, M3, inf = profile(ft, float(lm), float(z), f0 * (1 + float(z)) ** b, "S"); T[i, j] = dsig_prof(UT, pc, M3) / DINF_T
    return T
RES = dict(lane="SRH1", part="tilt (reported)", criteria="5ed8a37ec6", amendment="AMENDMENT_A1.md", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", foot={})
# ---- G1 for A1's cases: halo model (FZS1's, via srh1_hm's prefix in H) then the forest gate per footing
HMR = {}
for b, f0, src_ in TILTS:
    if src_ != "A1": continue
    for ft in FOOT:
        rows = {}
        for z in H["ZB"]:
            H["set_z"](z); Rt, Rb, Rc, inf = H["ratios_S"](ft, z, fac=(lambda zz, f0=f0, b=b: f0 * (1 + zz) ** b)); rows[str(z)] = dict(R_cold=Rc.tolist())
        HMR[f"{nm(b, f0)}|{ft}"] = rows
P(f"A1 halo-model rows done {tm()}")
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z"); FSRC = os.path.join(FRZ, "frz1_forest.py"); fcode = open(FSRC).read()
fcut = fcode.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))'); G1A = {}
for ft in FOOT:
    os.environ["HLF1_FOOT"] = ft; os.environ.pop("HLF1_MUTATE", None); N = {"__file__": FSRC, "__name__": "frz1_forest_lib"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(fcode[:fcut], FSRC, "exec"), N)
    # known answer: the frozen case beta -1, f0 1.0 recomputed through this path equals srh1_forest's value
    for b, f0, src_ in TILTS:
        if src_ == "A1":
            r_ = N["forest_eval"](N["FD"], N["BGB"], N["Rkz_z"]({z: v["R_cold"] for z, v in HMR[f"{nm(b, f0)}|{ft}"].items()})); G1A[f"{nm(b, f0)}|{ft}"] = float(r_["dchi2"])
    hm = json.load(open(os.path.join(HERE, "srh1_hm.json")))["cases"][f"{nm(-1.0, 1.0)}|{ft}"]
    chk = float(N["forest_eval"](N["FD"], N["BGB"], N["Rkz_z"]({z: v["R_cold"] for z, v in hm.items()}))["dchi2"]); ref = FOJ[ft]["cases"][nm(-1.0, 1.0)]["dchi2"]
    RES.setdefault("KA_path", {})[ft] = dict(recomputed=chk, srh1_forest=ref, pass_=bool(abs(chk - ref) <= 1e-6 * max(1.0, abs(ref))))
    P(f"[{ft}] KA (this path vs srh1_forest, {nm(-1.0, 1.0)}): {chk:.4f} vs {ref:.4f} -> {'PASS' if RES['KA_path'][ft]['pass_'] else 'FAIL'}  {tm()}")
# ---- G4 for every tilt case
for ft in FOOT:
    X = XP[ft]; lams9 = sorted(set([0.65] + LEJ["KA_G4a"][ft]["lams"] + [2.57]))
    with contextlib.redirect_stdout(io.StringIO()):
        Tr, Ts, npr = O["neighbours"](X, lams9, O["Htab_of"](X))
    SNB, kval = nb_sums(ft, Tr - Ts[2], lams9); R = RES["foot"][ft] = {}
    for b, f0, src_ in TILTS:
        T = table_t(ft, f0, b); OS = own_S(ft, T); rn = {mk: fit(mk, ft, OS[mk] + SNB[mk], kvalid=kval) for mk in MK}; gt = gate_of(rn)
        g1 = G1A[f"{nm(b, f0)}|{ft}"] if src_ == "A1" else FOJ[ft]["cases"][nm(b, f0)]["dchi2"]; tt = RCJ["foot"][ft]["tilt"][f"{b:+.1f}"]
        g2 = bool(f0 >= tt["f0_min_G2"]); g3 = bool(f0 >= tt["f0_min_G3a"])
        R[nm(b, f0)] = dict(beta=b, f0=f0, source=src_, f_at_z0_31=f0 * 1.31 ** b, f_at_z2_2=f0 * 3.2 ** b, G1_dchi2=g1, G1=bool(g1 <= 4), G2=g2, G3a=g3, G4=gt["status"],
                            G4_failing=gt["failing"], G4_z={s: (rn[("KO1", 1.6, s)]["z"] if rn[("KO1", 1.6, s)] else None) for s in ("all", "late", "early")},
                            all_four=bool(g1 <= 4 and g2 and g3 and gt["status"] == "PASS"))
        x = R[nm(b, f0)]
        P(f"[{ft}] {nm(b, f0):20s} ({src_:6s}) f(z 0.31) {x['f_at_z0_31']:.3f}, f(z 2.2) {x['f_at_z2_2']:.3f} | G1 {g1:9.2f} {'P' if x['G1'] else 'F'} | G2 {'P' if g2 else 'F'} | G3a {'P' if g3 else 'F'} | "
          f"G4 {gt['status']} {gt['failing']} z all/late/early " + " / ".join("None" if v is None else f"{v:+.2f}" for v in x["G4_z"].values()) + f" | all four {'YES' if x['all_four'] else 'no'}  {tm()}")
json.dump(RES, open(os.path.join(HERE, "srh1_tilt.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "srh1_tilt.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
