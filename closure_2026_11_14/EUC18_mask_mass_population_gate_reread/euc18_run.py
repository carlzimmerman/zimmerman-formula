#!/usr/bin/env python3
"""EUC18 driver.  Frozen criteria: FROZEN_CRITERIA.md (commit c8908592a4), section 1.

Runs EUC13's committed script UNMODIFIED.  EUC1's loader is wrapped so each lens's catalogued log mass becomes
lm - log10 f, with f = M2D_frac(mask radius, R_e, n) from EUC17's committed mask table.  Every file the source
script writes into its own folder is redirected to runs/<mode>/ in this lane.

  python3 -I euc18_run.py --mode f1|primary|F1a|F1b|invert --data-dir <ECLIPSE dir> --lit <EUC10 literature dir>

modes: f1 (no shift: the harness), primary, F1a (f with R_e x 0.80), F1b (f with R_e x 1.25),
       invert (twin: lm + log10 f; must exit 1).
"""
import argparse, builtins, csv, json, math, os, runpy, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D12 = os.path.join(REPO, "closure_2026_11_12")
SRC_DIR = os.path.join(D12, "EUC13_population_source_gate")
SRC = os.path.join(SRC_DIR, "euc13.py")
MASKS = os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread", "euc17_masks.csv")
sys.path.insert(0, os.path.join(D12, "EUC1_eclipse_saturation_ceiling"))
import euc1 as E          # noqa: E402

MODES = ("f1", "primary", "F1a", "F1b", "invert")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=MODES)
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--lit", required=True)
    a = ap.parse_args()
    out_dir = os.path.join(HERE, "runs", a.mode)
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()

    R = {}
    with open(MASKS, newline="") as f:
        for r in csv.DictReader(f):
            if r["has_mask"] == "1":
                R[r["unique_identifier"]] = float(r["mask_radius_arcsec"])

    info = dict(mode=a.mode, criteria_commit="c8908592a4", source="closure_2026_11_12/EUC13_population_source_gate/euc13.py")
    orig_load = E.load

    def load(data_dir):
        rows, n = orig_load(data_dir)
        lfs, nshift = [], 0
        if a.mode != "f1":
            scale = 0.80 if a.mode == "F1a" else 1.25 if a.mode == "F1b" else 1.0
            for r in rows:
                rm = R.get(r["id"])
                if rm is None or not (r["te"] > 0.0) or not (r["n"] > 0.0):
                    continue
                lf = math.log10(float(E.M2D_frac(rm, r["te"] * scale, r["n"])))
                if a.mode == "invert":
                    lf = -lf
                r["lm"] = r["lm"] - lf
                nshift += 1; r["_euc18_lf"] = lf
        Pm, _ = E.select(rows, ("A",))
        miss = [r["id"] for r in Pm if a.mode != "f1" and "_euc18_lf" not in r]
        lfP = sorted(r.get("_euc18_lf", 0.0) for r in Pm)
        info.update(rows=len(rows), shifted=nshift, P=len(Pm), P_without_mask=len(miss),
                    median_log10f_P=(lfP[len(lfP) // 2] if lfP else None))
        for r in rows:
            r.pop("_euc18_lf", None)
        if miss:
            print("EUC18 driver: %d lenses of P have no mask; stopping." % len(miss)); sys.exit(4)
        return rows, n

    E.load = load

    real_open = builtins.open
    src_real = os.path.realpath(SRC_DIR)
    redirected = []

    def open_(file, mode="r", *args, **kw):
        if isinstance(file, (str, os.PathLike)) and any(c in mode for c in "wax+"):
            p = os.path.realpath(os.fspath(file))
            if os.path.dirname(p) == src_real:
                redirected.append(os.path.basename(p))
                file = os.path.join(out_dir, os.path.basename(p))
        return real_open(file, mode, *args, **kw)

    builtins.open = open_
    os.environ.pop("EUC13_MUTATE", None)
    sys.argv = [SRC, "--data-dir", a.data_dir, "--lit", a.lit]
    code = 0
    try:
        runpy.run_path(SRC, run_name="__main__")
    except SystemExit as ex:
        code = ex.code if isinstance(ex.code, int) else (0 if ex.code is None else 9)
    finally:
        builtins.open = real_open
        E.load = orig_load
    info.update(source_exit_code=code, redirected_files=sorted(set(redirected)), elapsed_s=round(time.time() - t0, 1))

    exit_code = 0
    if a.mode == "invert":
        ref = json.load(open(os.path.join(SRC_DIR, "euc13_results.json")))
        new = json.load(open(os.path.join(out_dir, "euc13_results.json")))
        rise = all(new["members"][m][nm]["med"]["point"] > ref["members"][m][nm]["med"]["point"]
                   for m in ref["members"] for nm in ("canonical", "alt") if m in new["members"])
        same_members = sorted(new["members"]) == sorted(ref["members"])
        info.update(twin_b_med_rises_for_every_member=bool(rise), twin_same_members=bool(same_members))
        print("EUC18 twin invert: every member's b_med rises on both footings: %s" % ("YES" if rise and same_members else "NO"))
        exit_code = 1 if (rise and same_members) else 3
    with open(os.path.join(out_dir, "driver.json"), "w") as f:
        json.dump(info, f, indent=1)
    print("EUC18 driver: mode %s; source exit %s; %d lenses shifted; %.0f s" % (a.mode, code, info.get("shifted", 0), time.time() - t0))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
