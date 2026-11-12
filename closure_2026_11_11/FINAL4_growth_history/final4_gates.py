#!/usr/bin/env python3
"""FINAL4 (GROWTH), parts 2 and 3: P(k, z) through FRZ1's own forest gate, and the two independent rows.

Criteria c5d897706f. R_cold(k, z) is READ from FRZ1's and SRH1's committed tables (no halo-model re-run);
the forest gate (DESI DR1 P1D, 755 points, 12 bins, full covariance) is FRZ1's own frz1_forest.py executed
from its own path, read-only. TEST lane; adopts nothing.
"""
import os, sys, json, math, time, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.interpolate import RegularGridInterpolator, CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
CO1D = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed")

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time(); tm = lambda: f"[{time.time()-T0:7.1f}s]"

P("=" * 100)
P("FINAL4 (GROWTH), parts 2 and 3 -- forest gate and the independent rows")
P("     criteria FROZEN_CRITERIA.md (c5d897706f).  kappa = 1/2 FITTED; not theory closed.  Adopts nothing.")
P("=" * 100)

GATE = 4.0
FOOTS = ("canonical", "alt")

# ================================================================ FRZ1's forest gate, per footing
def load_gate(foot):
    os.environ["HLF1_FOOT"] = foot
    os.environ.pop("HLF1_MUTATE", None)
    src = os.path.join(FRZ, "frz1_forest.py")
    code = open(src).read()
    cut = code.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
    N = {"__file__": src, "__name__": f"frz1_forest_lib_{foot}"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code[:cut], src, "exec"), N)
    return N

NG = {ft: load_gate(ft) for ft in FOOTS}
P(f"FRZ1 forest gate loaded for {FOOTS}  {tm()}")

FZ = {ft: json.load(open(os.path.join(FRZ, f"frz1_forest_{ft}.json"))) for ft in FOOTS}
HM = json.load(open(os.path.join(SRH, "srh1_hm.json")))
KK = np.array(HM["k"])

def rcold_from_stored(case, foot):
    key = f"{case}|{foot}"
    rows = HM["cases"][key]
    return {str(z): np.array(rows[z]["R_cold"]) for z in rows}

def dchi2_gate(foot, rcd):
    N = NG[foot]
    RZ = N["Rkz_z"]({z: v.tolist() for z, v in rcd.items()})
    r = N["forest_eval"](N["FD"], N["BGB"], RZ)
    return dict(dchi2=float(r["dchi2"]), per_z=dict(N["perz"](RZ)), status=r["status"],
                  r_min=float(r["r_min"]), r_max=float(r["r_max"]))

# ================================================================ the graded histories
# fac = R_set / R_fold.  fac = 0 is the cold reference (R_set = 0); fac = inf is R_set = r_ta (form B's full layout).
# The formation reading, share fixed at formation: the settled region is the region the charge has filled = up to r_ta
# (section 1 closing condition) => fac = inf, which is FRZ1's baseline.  FZS1's fac = 1 and the passing fac = 0.5
# are graded beside as brackets, and SRH1's tilt cases as H5 / H6.
HIST = [("H_A  derived: R_set = r_ta (share fixed at formation)", "inf", "FRZ1 primary"),
        ("H_B  bracket: R_set = R_fold (FZS1 primary)", "1.00", "srh1 f1.00"),
        ("H_C  bracket: R_set = 0.5 R_fold (the passing value)", "0.50", "srh1 f0.50"),
        ("H_0  comparator: cold reference, R_set = 0", "0.00", "srh1 KA_0"),
        ("H5a  tilt beta -1, f0 1.50", "tilt_b-1.0_f1.50", "srh1 tilt"),
        ("H5b  tilt beta -1, f0 2.00", "tilt_b-1.0_f2.00", "srh1 tilt"),
        ("H5c  tilt beta -0.5, f0 1.25", "tilt_b-0.5_f1.25", "srh1 tilt"),
        ("H6   control: tilt beta -1, f0 1.00", "tilt_b-1.0_f1.00", "srh1 tilt")]

FZJ = {ft: json.load(open(os.path.join(FRZ, f"frz1_forest_{ft}.json"))) for ft in FOOTS}

sec_out = {}
P("")
P("-- PART 2: P(k, z) through FRZ1's own forest gate (755 points, 12 bins, full covariance, gate 4) --")
for label, case, src in HIST:
    for foot in FOOTS:
        if case == "inf":
            d = dict(dchi2=float(FZJ[foot]["cases"]["primary"]["dchi2"]),
                     per_z=dict(FZJ[foot]["cases"]["primary"]["per_z"]),
                     status="FAIL" if float(FZJ[foot]["cases"]["primary"]["dchi2"]) > GATE else "PASS")
        elif case.startswith("tilt_"):
            tj = json.load(open(os.path.join(SRH, "srh1_tilt.json")))
            gg = float(tj["foot"][foot][case]["G1_dchi2"])
            d = dict(dchi2=gg, per_z={}, status="PASS" if gg <= GATE else "FAIL", r_min=float("nan"),
                          r_max=float("nan"))
        else:
            if case in ("1.00", "0.50", "0.00"):
                cname = "f1.00" if case == "1.00" else ("f0.50" if case == "0.50" else "KA_0")
            else:
                cname = case
            rcd = rcold_from_stored(cname, foot)
            d = dchi2_gate(foot, rcd)
        sec_out[(case, foot)] = d
        P(f"  {label:52s} [{foot:9s}] dchi2 {d['dchi2']:10.3f} -> {d['status']}   {tm()}")

P("")
P("  per-bin Delta chi^2 (canonical / alt):")
for z in HM["z_bins"]:
    a = sec_out[("inf", "canonical")]["per_z"].get(str(z)); b = sec_out[("inf", "alt")]["per_z"].get(str(z))
    P(f"    z {z:4.1f}: {a:10.3f} / {b:10.3f}")

json.dump({f"{a}|{b}": c for (a, b), c in sec_out.items()},
          open(os.path.join(HERE, "final4_gates.json"), "w"), indent=1, default=float)
