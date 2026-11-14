#!/usr/bin/env python3
"""EUC20 driver.  Frozen criteria: FROZEN_CRITERIA.md (commit cbd14e4ca4), section 1.

Runs a source lane's committed script with the catalogue stellar mass corrected to the in-mask mass
(lm - log10 f, f = M2D_frac(mask radius, R_e, n); masks from EUC17's and EUC19's tables).  A lens without a mask
keeps its catalogued mass.  Every file the source script writes into its own folder goes to runs/<lane>/<mode>/.

  python3 -I euc20_run.py --lane euc8|euc5a1|lnj1 --mode f1|primary|F1a|F1b|invert --data-dir <ECLIPSE dir>

lanes:  euc8, euc5a1   run unmodified, EUC1's loader wrapped;
        lnj1           reads the catalogue itself: its text is executed under its own path with ONE exact
                       substitution on the expression that parses eclipse_log_survived_mass_med.
modes:  f1 (no shift: harness), primary, F1a (f with R_e x 0.80), F1b (R_e x 1.25), invert (twin, lm + log10 f).
"""
import argparse, builtins, csv, json, math, os, runpy, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D12 = os.path.join(REPO, "closure_2026_11_12")
D13 = os.path.join(REPO, "closure_2026_11_13")
TABLES = [os.path.join(D13, "EUC17_mask_aperture_mass_reread", "euc17_masks.csv"),
          os.path.join(REPO, "closure_2026_11_14", "EUC19_grade_b_mask_table", "euc19_masks.csv")]
LANES = {"euc8": (os.path.join(D12, "EUC8_wide_lens_residual_profile"), "euc8.py"),
         "euc5a1": (os.path.join(D12, "EUC5_dynamical_boost"), "euc5_a1.py"),
         "lnj1": (os.path.join(D13, "LNJ1_joint_switch_on_euclid_lenses"), "lnj1.py")}
LNJ1_OLD = 'lm=fl(r["eclipse_log_survived_mass_med"])'
LNJ1_NEW = 'lm=fl(r["eclipse_log_survived_mass_med"]) - _EUC20_LF.get(r["unique_identifier"], 0.0)'
sys.path.insert(0, os.path.join(D12, "EUC1_eclipse_saturation_ceiling"))
import euc1 as E          # noqa: E402


def masks():
    R = {}
    for t in TABLES:
        with open(t, newline="") as f:
            for r in csv.DictReader(f):
                if r["has_mask"] == "1":
                    R[r["unique_identifier"]] = float(r["mask_radius_arcsec"])
    return R


def shifts(rows, R, mode):
    """log10 f per lens for the mode (sign as subtracted from lm); empty for f1."""
    if mode == "f1":
        return {}
    scale = 0.80 if mode == "F1a" else 1.25 if mode == "F1b" else 1.0
    LF = {}
    for r in rows:
        rm = R.get(r["id"])
        if rm is None or not (r["te"] > 0.0) or not (r["n"] > 0.0):
            continue
        lf = math.log10(float(E.M2D_frac(rm, r["te"] * scale, r["n"])))
        LF[r["id"]] = -lf if mode == "invert" else lf
    return LF


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True, choices=sorted(LANES))
    ap.add_argument("--mode", required=True, choices=("f1", "primary", "F1a", "F1b", "invert"))
    ap.add_argument("--data-dir", required=True)
    a = ap.parse_args()
    src_dir, script = LANES[a.lane]; src = os.path.join(src_dir, script)
    out_dir = os.path.join(HERE, "runs", a.lane, a.mode)
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    R = masks()
    orig_load = E.load
    rows0, _ = orig_load(a.data_dir); E.OUT.clear()
    LF = shifts(rows0, R, a.mode)
    Sm, _ = E.select(rows0, ("A", "B"))
    lfS = sorted(LF.get(r["id"], 0.0) for r in Sm)
    info = dict(lane=a.lane, mode=a.mode, criteria_commit="cbd14e4ca4", source=os.path.relpath(src, REPO),
                masks=len(R), S=len(Sm), S_without_mask=sum(1 for r in Sm if r["id"] not in R),
                shifted=len(LF), median_log10f_S=(lfS[len(lfS) // 2] if lfS else None))

    def load(data_dir):
        rows, n = orig_load(data_dir)
        for r in rows:
            lf = LF.get(r["id"])
            if lf is not None:
                r["lm"] = r["lm"] - lf
        return rows, n

    real_open = builtins.open
    src_real = os.path.realpath(src_dir)
    redirected = []

    def open_(file, mode="r", *args, **kw):
        if isinstance(file, (str, os.PathLike)) and any(c in mode for c in "wax+"):
            p = os.path.realpath(os.fspath(file))
            if os.path.dirname(p) == src_real:
                redirected.append(os.path.basename(p))
                file = os.path.join(out_dir, os.path.basename(p))
        return real_open(file, mode, *args, **kw)

    for k in ("EUC8_MUTATE", "EUC5_MUTATE", "EUC1_MUTATE"):
        os.environ.pop(k, None)
    builtins.open = open_
    code = 0
    try:
        if a.lane == "lnj1":
            text = real_open(src, encoding="utf-8").read()
            n_old = text.count(LNJ1_OLD)
            info["lnj1_substitution_matches"] = n_old
            if n_old != 1:
                print("EUC20 driver: the LNJ1 substitution matches %d times, not once; stopping." % n_old); sys.exit(4)
            sys.argv = [src]
            g = {"__name__": "__main__", "__file__": src, "__builtins__": builtins, "_EUC20_LF": LF}
            exec(compile(text.replace(LNJ1_OLD, LNJ1_NEW), src, "exec"), g)
        else:
            E.load = load
            sys.argv = [src, "--data-dir", a.data_dir]
            runpy.run_path(src, run_name="__main__")
    except SystemExit as ex:
        code = ex.code if isinstance(ex.code, int) else (0 if ex.code is None else 9)
        if not isinstance(ex.code, int) and ex.code is not None:
            info["source_exit_message"] = str(ex.code)[:200]
    finally:
        builtins.open = real_open
        E.load = orig_load
    info.update(source_exit_code=code, redirected_files=sorted(set(redirected)), elapsed_s=round(time.time() - t0, 1))
    with open(os.path.join(out_dir, "driver.json"), "w") as f:
        json.dump(info, f, indent=1)
    print("EUC20 driver: lane %s mode %s; source exit %s; %d lenses shifted; S without a mask %d; %.0f s"
          % (a.lane, a.mode, code, len(LF), info["S_without_mask"], time.time() - t0))
    sys.exit(1 if a.mode == "invert" else 0)


if __name__ == "__main__":
    main()
