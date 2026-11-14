#!/usr/bin/env python3
"""EUC21 driver.  Frozen criteria: FROZEN_CRITERIA.md (commit 33778cb9a6), section 1.

Runs ESZ1's committed text under its own path with the catalogue stellar mass corrected to the in-mask mass
(lm - log10 f; masks from EUC17's and EUC19's tables), EUC1's loader wrapped, and ONE exact substitution: the gate
that stops the run before the stack when a check has failed ignores K6 and K7 (they assert uncorrected numbers).
Every file ESZ1 writes into its own folder goes to runs/<mode>/.

  python3 -I euc21_run.py --mode f1|primary|F1a|F1b|invert --data-dir <ECLIPSE dir> --y-dir <ACT map dir> --erass <erass1_main.tsv>
"""
import argparse, builtins, csv, json, math, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D12 = os.path.join(REPO, "closure_2026_11_12")
SRC_DIR = os.path.join(D12, "ESZ1_wide_lens_gas_pressure")
SRC = os.path.join(SRC_DIR, "esz1.py")
TABLES = [os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread", "euc17_masks.csv"),
          os.path.join(REPO, "closure_2026_11_14", "EUC19_grade_b_mask_table", "euc19_masks.csv")]
OLD = 'if not all(v["ok"] for v in CK.values()):'
NEW = 'if not all(v["ok"] for k, v in CK.items() if k not in ("K6", "K7")):'
sys.path.insert(0, os.path.join(D12, "EUC1_eclipse_saturation_ceiling"))
import euc1 as E          # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=("f1", "primary", "F1a", "F1b", "invert"))
    ap.add_argument("--data-dir", required=True); ap.add_argument("--y-dir", required=True); ap.add_argument("--erass", required=True)
    a = ap.parse_args()
    out_dir = os.path.join(HERE, "runs", a.mode); os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    R = {}
    for t in TABLES:
        with open(t, newline="") as f:
            for r in csv.DictReader(f):
                if r["has_mask"] == "1": R[r["unique_identifier"]] = float(r["mask_radius_arcsec"])
    orig_load = E.load
    rows0, _ = orig_load(a.data_dir); E.OUT.clear()
    LF = {}
    if a.mode != "f1":
        scale = 0.80 if a.mode == "F1a" else 1.25 if a.mode == "F1b" else 1.0
        for r in rows0:
            rm = R.get(r["id"])
            if rm is None or not (r["te"] > 0.0) or not (r["n"] > 0.0): continue
            lf = math.log10(float(E.M2D_frac(rm, r["te"] * scale, r["n"])))
            LF[r["id"]] = -lf if a.mode == "invert" else lf
    Sm, _ = E.select(rows0, ("A", "B"))
    info = dict(mode=a.mode, criteria_commit="33778cb9a6", source=os.path.relpath(SRC, REPO), masks=len(R), S=len(Sm),
                S_without_mask=sum(1 for r in Sm if r["id"] not in R), shifted=len(LF))

    def load(data_dir):
        rows, n = orig_load(data_dir)
        for r in rows:
            lf = LF.get(r["id"])
            if lf is not None: r["lm"] = r["lm"] - lf
        return rows, n

    real_open = builtins.open
    src_real = os.path.realpath(SRC_DIR); redirected = []

    def open_(file, mode="r", *args, **kw):
        if isinstance(file, (str, os.PathLike)) and any(c in mode for c in "wax+"):
            p = os.path.realpath(os.fspath(file))
            if os.path.dirname(p) == src_real:
                redirected.append(os.path.basename(p)); file = os.path.join(out_dir, os.path.basename(p))
        return real_open(file, mode, *args, **kw)

    text = real_open(SRC, encoding="utf-8").read()
    info["substitution_matches"] = text.count(OLD)
    if info["substitution_matches"] != 1:
        print("EUC21 driver: the substitution matches %d times, not once; stopping." % info["substitution_matches"]); sys.exit(4)
    for k in ("ESZ1_MUTATE", "EUC1_MUTATE", "EUC8_MUTATE", "EUC5_MUTATE"):
        os.environ.pop(k, None)
    E.load = load; builtins.open = open_
    sys.argv = [SRC, "--data-dir", a.data_dir, "--y-dir", a.y_dir, "--erass", a.erass]
    code = 0
    try:
        exec(compile(text.replace(OLD, NEW), SRC, "exec"), {"__name__": "__main__", "__file__": SRC, "__builtins__": builtins})
    except SystemExit as ex:
        code = ex.code if isinstance(ex.code, int) else (0 if ex.code is None else 9)
    finally:
        builtins.open = real_open; E.load = orig_load
    info.update(source_exit_code=code, redirected_files=sorted(set(redirected)), elapsed_s=round(time.time() - t0, 1))
    with open(os.path.join(out_dir, "driver.json"), "w") as f:
        json.dump(info, f, indent=1)
    print("EUC21 driver: mode %s; source exit %s; %d lenses shifted; S without a mask %d; %.0f s"
          % (a.mode, code, len(LF), info["S_without_mask"], time.time() - t0))
    sys.exit(1 if a.mode == "invert" else 0)


if __name__ == "__main__":
    main()
