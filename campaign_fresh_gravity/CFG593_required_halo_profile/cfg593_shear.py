#!/usr/bin/env python3
"""CFG593 constraint (a) (FROZEN_CRITERIA.md sections 2, 3a, 6, 7, 8): the declared profile family through CFG556's halo model and
CFG590's cosmic-shear mapping M1 (both exec'd read-only).

  nice -n 10 python3 cfg593_shear.py                   -> cfg593_shear.out, cfg593_shear_results.json  (R tables -> _external_data/cfg593_work/)
  CFG593_MUTATE=1 nice -n 10 python3 cfg593_shear.py   -> *_MUTATE.* (MU1 framework profile outside the shear region; MU2 LCDM / NFW member inside)
                                                          exit 1 = all teeth bite
DIAGNOSTIC, data-driven: the allowed profiles are what the data require, not a framework derivation.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np
import multiprocessing as MP

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg593_lib as L

MUT = os.environ.get("CFG593_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
os.makedirs(L.WORK, exist_ok=True)
try:
    os.nice(10)
except OSError:
    pass
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

FOOTS = ("canonical", "alt")
BARY = ("cen", "emg")
P(f"CFG593 shear {'(MUTATE)' if MUT else ''} -- FROZEN_CRITERIA.md. kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
P("DIAGNOSTIC, data-driven: allowed profiles are what the data require, NOT a framework derivation.")

H = L.H556(); L.hm_refs(); KK = H["KK"]
J556 = json.load(open(os.path.join(L.LANES, "CFG556_halo_model_matter_power", "cfg556_results.json")))
J557 = json.load(open(os.path.join(L.LANES, "CFG557_settling_catchment_derived", "cfg557_tests_results.json")))
J559 = json.load(open(os.path.join(L.LANES, "CFG559_kinetic_settled_profile", "cfg559_tests_results.json")))
J590 = json.load(open(os.path.join(L.LANES, "CFG590_framework_pk_vs_cosmic_shear", "cfg590_results.json")))


def hm_task(args):
    foot, xe, f, y, bary, mode = args
    U, infos, cons = L.hm_R(foot, xe, f, y, bary, mode)
    R = L.R_of_U(U)
    lt = np.log10(H["MTA"])
    d = dict(R=R, cons=cons, n_capped_supply=int(sum(bool(i.get("capped_supply")) for i in infos)),
             q_at={str(l): float(np.interp(l, lt, [i["q"] for i in infos])) for l in (12, 13, 14, 15)},
             re_over_rta_at={str(l): float(np.interp(l, lt, [i["re_over_rta"] for i in infos])) for l in (12, 13, 14, 15)})
    return args, d


PTS = L.family_points()
if MUT:
    tasks = [(ft, 0, 0, 0, "cen", "census") for ft in FOOTS] + [(ft, 1.0, 0.0, 0, "cen", "family") for ft in FOOTS]
else:
    tasks = [(ft, 0, 0, 0, "cen", "census") for ft in FOOTS] + [(ft, 0, 0, 0, "emg", "emg") for ft in FOOTS]
    tasks += [(ft, xe, f, y, b, "family") for ft in FOOTS for b in BARY for (xe, f, y) in PTS]
P(f"  halo-model evaluations: {len(tasks)} (4 processes, 1 thread each)")
with MP.get_context("fork").Pool(4) as pool:
    HM = dict(pool.map(hm_task, tasks, chunksize=8))
P(f"  halo model done ({time.time() - T0:.0f} s)")
if not MUT:
    np.savez_compressed(os.path.join(L.WORK, "cfg593_R.npz"), k=KK, **{"|".join(map(str, k)): v["R"] for k, v in HM.items()})

# ---------------------------------------------------------------- CFG590 machinery (exec'd read-only up to its controls block)
P590 = os.path.join(L.LANES, "CFG590_framework_pk_vs_cosmic_shear", "cfg590_shear.py")
_src = open(P590).read(); _cut = _src.index("# ------------------------------------------------------------------ controls")
NS = {"__file__": P590, "__name__": "cfg590_ro"}
_e = os.environ.pop("CFG590_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_cut], "cfg590_ro", "exec"), NS)
A_M1, DATA, TFULL, TFID, KR = NS["A_M1"], NS["DATA"], NS["TFULL"], NS["TFID"], NS["KR"]
assert np.allclose(KR, KK, rtol=0, atol=0)
P(f"  CFG590 machinery loaded ({time.time() - T0:.0f} s); data (recalled, PROVISIONAL) {DATA}; fiducial T {TFID}")


def shear_eval(R):
    A = {str(T): {d: A_M1(d, R, T) for d in DATA} for T in TFULL}
    A["off"] = {d: A_M1(d, R, None) for d in DATA}
    Z = {T: {d: (A[T][d] - DATA[d][0]) / DATA[d][1] for d in DATA} for T in A}
    zmax = {T: max(abs(v) for v in z.values()) for T, z in Z.items()}
    fid = [str(T) for T in TFID]; full = [str(T) for T in TFULL]
    best_fid = min(fid, key=lambda T: zmax[T]); best_full = min(full, key=lambda T: zmax[T])
    return dict(A=A, Z=Z, Zmax=zmax, allowed_fid=bool(zmax[best_fid] < 2), allowed_full=bool(zmax[best_full] < 2),
                best_T_fid=float(best_fid), Zmax_best_fid=zmax[best_fid], best_T_full=float(best_full), Zmax_best_full=zmax[best_full],
                R_at={str(k): float(np.interp(k, KK, R)) for k in (0.3, 0.5, 1.0, 2.0)})


res = dict(lane="CFG593", script="cfg593_shear", date="2026-10-10", mutate=MUT, data=DATA, T_fid=TFID, T_full=TFULL,
           settings="kappa = 1/2 FITTED; footings never pooled; nu_mono; candidate B; cold energy mass required; not theory closed; DIAGNOSTIC data-driven")
ONES = np.ones_like(KK)
LC = shear_eval(ONES)
P(f"\nLCDM (R = 1): best fiducial T {LC['best_T_fid']} Zmax {LC['Zmax_best_fid']:.2f} -> allowed {LC['allowed_fid']}")
res["LCDM"] = LC

if MUT:
    teeth = {}
    for ft in FOOTS:
        cen = shear_eval(HM[(ft, 0, 0, 0, "cen", "census")]["R"])
        k559 = shear_eval(np.array(J559["halo_model"][ft]["PRIMARY_kin"]["R"]))
        nfw = shear_eval(HM[(ft, 1.0, 0.0, 0, "cen", "family")]["R"])
        t1 = (not cen["allowed_fid"]) and (not k559["allowed_fid"]) and (not cen["allowed_full"]) and (not k559["allowed_full"])
        cls_ok = J590["models"][f"{ft}|PRIMARY CFG559 kin"]["final_class"] == "EXCLUDED" and min(k559["Zmax"][str(T)] for T in TFULL) >= 3
        t2 = LC["allowed_fid"] and nfw["allowed_fid"]
        teeth[ft] = dict(MU1_bites=bool(t1 and cls_ok), MU2_bites=bool(t2), census_Zmax_best_fid=cen["Zmax_best_fid"], k559_Zmax_best_fid=k559["Zmax_best_fid"],
                         k559_min_Zmax_full=min(k559["Zmax"][str(T)] for T in TFULL), nfw_member_Zmax_best_fid=nfw["Zmax_best_fid"], nfw_member_allowed=nfw["allowed_fid"],
                         LCDM_allowed=LC["allowed_fid"])
        P(f"  [{ft}] MU1 framework current: CFG556 census Zmax(best fid T) {cen['Zmax_best_fid']:.2f}, CFG559 PRIMARY {k559['Zmax_best_fid']:.2f} "
          f"(min over 7.3-8.3 {teeth[ft]['k559_min_Zmax_full']:.2f}, CFG590 class EXCLUDED) -> {'BITES' if teeth[ft]['MU1_bites'] else 'FAILS'};  "
          f"MU2 LCDM allowed {LC['allowed_fid']}, NFW member Zmax {nfw['Zmax_best_fid']:.2f} allowed {nfw['allowed_fid']} -> {'BITES' if t2 else 'FAILS'}")
    res["teeth"] = teeth
    allb = all(v["MU1_bites"] and v["MU2_bites"] for v in teeth.values())
    res["all_teeth_bite"] = bool(allb)
    P(f"\nMUTATE (shear): all teeth bite -> {allb}")
else:
    # controls
    k1 = {}
    for ft in FOOTS:
        k1[ft] = dict(cen=float(np.max(np.abs(HM[(ft, 0, 0, 0, "cen", "census")]["R"] - np.array(J556["cases"][f"{ft}|census|cen"]["R"])))),
                      emg=float(np.max(np.abs(HM[(ft, 0, 0, 0, "emg", "emg")]["R"] - np.array(J556["cases"][f"{ft}|census|emg"]["R"])))))
    k1p = all(v <= 1e-10 for d in k1.values() for v in d.values())
    P(f"\nK1 family code reproduces CFG556 census|cen / census|emg R: {k1} -> {'PASS' if k1p else 'FAIL'}")
    k2 = 0.0
    for ft in FOOTS:
        R9 = np.array(J559["halo_model"][ft]["PRIMARY_kin"]["R"])
        for d in DATA:
            k2 = max(k2, abs(A_M1(d, R9, 7.8) - J590["models"][f"{ft}|PRIMARY CFG559 kin"]["A_table"]["7.8"][f"A_M1_{d}"]),
                     abs(A_M1(d, None, 7.8) - J590["models"]["LCDM-DMO"]["A_table"]["7.8"][f"A_M1_{d}"]))
    P(f"K2 CFG590 code reproduces stored A_M1 (LCDM, CFG559 PRIMARY; T 7.8): max |d| {k2:.1e} -> {'PASS' if k2 <= 1e-9 else 'FAIL'}")
    k5 = max(v["cons"] for v in HM.values())
    P(f"K5 mass conservation max |M(<r_ta) - M_ta| / M_ta over all points and halos: {k5:.1e} -> {'PASS' if k5 <= 1e-6 else 'FAIL'}")
    res["controls"] = dict(K1=k1, K1_pass=k1p, K2=k2, K2_pass=k2 <= 1e-9, K5=k5, K5_pass=k5 <= 1e-6)

    # record rules
    rec = {}
    for ft in FOOTS:
        rec[ft] = {"CFG556 census edge (= CFG541 analytic edge)": shear_eval(HM[(ft, 0, 0, 0, "cen", "census")]["R"]),
                   "CFG556 emergent edge": shear_eval(HM[(ft, 0, 0, 0, "emg", "emg")]["R"]),
                   "CFG557 finite-age supply (TESTED)": shear_eval(np.array(J557["halo_model"][ft]["TESTED"]["R"])),
                   "CFG559 kinetic PRIMARY": shear_eval(np.array(J559["halo_model"][ft]["PRIMARY_kin"]["R"])),
                   "CFG559 kinetic full supply": shear_eval(np.array(J559["halo_model"][ft]["VARIANT_full_kin"]["R"]))}
    P("\nRecord rules, shear (a): Zmax at the best fiducial T; allowed (fid / full band)")
    for ft in FOOTS:
        for n, o in rec[ft].items():
            P(f"  [{ft:9s}] {n:46s} R(1) {o['R_at']['1.0']:.3f}  A_KiDS(T {o['best_T_fid']}) {o['A'][str(o['best_T_fid'])]['KiDS']:.3f}  Zmax {o['Zmax_best_fid']:.2f} -> {o['allowed_fid']} / {o['allowed_full']}")
    res["record_rules"] = {ft: {n: {k: v for k, v in o.items() if k != "A"} | {"A_bestfid": o["A"][str(o["best_T_fid"])], "A_off": o["A"]["off"]}
                                for n, o in d.items()} for ft, d in rec.items()}

    # the family scan
    scan = {}
    for ft in FOOTS:
        for b in BARY:
            for (xe, f, y) in PTS:
                hm = HM[(ft, xe, f, y, b, "family")]
                o = shear_eval(hm["R"])
                scan[f"{ft}|{b}|{xe:.2f}|{f:.1f}|{y}"] = dict(xe=xe, f=f, y=y, allowed_fid=o["allowed_fid"], allowed_full=o["allowed_full"],
                                                               Zmax_best_fid=o["Zmax_best_fid"], best_T_fid=o["best_T_fid"], Zmax_best_full=o["Zmax_best_full"],
                                                               Z_bestfid=o["Z"][str(o["best_T_fid"])], A_off=o["A"]["off"], R_at=o["R_at"],
                                                               q_at=hm["q_at"], re_over_rta_at=hm["re_over_rta_at"], n_capped_supply=hm["n_capped_supply"])
    res["scan"] = scan
    P("\nShear-allowed region (fiducial band), per footing / baryon convention: allowed x_e at each f (y = 0 | 1 | 3 | 10)")
    for ft in FOOTS:
        for b in BARY:
            na = sum(1 for k, v in scan.items() if k.startswith(f"{ft}|{b}|") and v["allowed_fid"])
            P(f"  [{ft} | baryons {b}] {na} / {len(PTS)} points allowed (full band: {sum(1 for k, v in scan.items() if k.startswith(f'{ft}|{b}|') and v['allowed_full'])})")
            for f in L.F_GRID:
                row = []
                for y in (L.Y_GRID if f < 1 else [0]):
                    xs = [xe for xe in L.XE_GRID if scan[f"{ft}|{b}|{xe:.2f}|{f:.1f}|{y}"]["allowed_fid"]]
                    row.append(",".join(f"{x:g}" for x in xs) if xs else "-")
                P(f"     f {f:.1f}: " + " | ".join(row))
    for ft in FOOTS:
        P(f"  [{ft}] Zmax(best fid T), baryons cen, y = 0:  rows f = 0..1, columns x_e = " + " ".join(f"{x:g}" for x in L.XE_GRID))
        for f in L.F_GRID:
            P(f"     f {f:.1f}: " + " ".join(f"{scan[f'{ft}|cen|{xe:.2f}|{f:.1f}|0']['Zmax_best_fid']:5.2f}" for xe in L.XE_GRID))

P(f"\nelapsed {time.time() - T0:.0f} s")
json.dump(res, open(os.path.join(HERE, f"cfg593_shear_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg593_shear{SUF}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    sys.exit(1 if res["all_teeth_bite"] else 0)
