#!/usr/bin/env python3
"""EUC21R driver (blind re-grade of EUC21).  Criteria: closure_2026_11_14/EUC21_mask_mass_gas_lane_reread/FROZEN_CRITERIA.md;
reading: READING.md in this folder.

Runs ESZ1's committed script text (closure_2026_11_12/ESZ1_wide_lens_gas_pressure/esz1.py) under its own path, with
  * one exact substitution (the gate before the stack ignores K6 and K7), asserted to match exactly once;
  * EUC1's loader wrapped so that every catalogue row with a mask gets lm - log10 f (mode corrected / F1a / F1b),
    lm + log10 f (twin `invert`) or lm - log10 1 (harness);
  * every file ESZ1 writes into its own folder redirected to runs/<mode>/ here (any other write is refused).

  python3 -I euc21r_run.py --mode harness|corrected|F1a|F1b|invert

Exit: the source's exit code for harness / corrected / F1a / F1b (expected 0 / 3 / 3 / 3); for `invert`, 1 if B100's
least predicted stack rises on both footings against ESZ1's committed value, else 2.
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import os, sys
for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_k, "4")
os.environ.pop("ESZ1_MUTATE", None)
sys.dont_write_bytecode = True
import argparse, builtins, csv, hashlib, json, math, subprocess, time

HERE = os.path.dirname(os.path.realpath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", ".."))
ESZ1_DIR = os.path.join(REPO, "closure_2026_11_12", "ESZ1_wide_lens_gas_pressure")
ESZ1_PY = os.path.join(ESZ1_DIR, "esz1.py")
MASKS = [os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread", "euc17_masks.csv"),
         os.path.join(REPO, "closure_2026_11_14", "EUC19_grade_b_mask_table", "euc19_masks.csv")]
SOURCE_PATHS = ["closure_2026_11_12/ESZ1_wide_lens_gas_pressure", "closure_2026_11_12/EUC1_eclipse_saturation_ceiling",
                "closure_2026_11_12/EUC4_wide_lenses", "closure_2026_11_12/EUC5_dynamical_boost",
                "closure_2026_11_12/EUC8_wide_lens_residual_profile",
                "closure_2026_11_13/EUC17_mask_aperture_mass_reread/euc17_masks.csv",
                "closure_2026_11_14/EUC19_grade_b_mask_table/euc19_masks.csv"]
OLD = 'if not all(v["ok"] for v in CK.values()):'
NEW = 'if not all(v["ok"] for k, v in CK.items() if k not in ("K6", "K7")):'
MODES = {"harness": (0, 1.0), "corrected": (-1, 1.0), "F1a": (-1, 0.80), "F1b": (-1, 1.25), "invert": (+1, 1.0)}
#          mode: (sign s in lm + s * log10 f, scale on R_e inside f only); harness uses f = 1


def rel(p):
    """repo-relative name, or <repo-parent>/... for the external data, never a home path."""
    p = os.path.realpath(p); par = os.path.dirname(REPO)
    if p.startswith(REPO + os.sep): return os.path.relpath(p, REPO)
    if p.startswith(par + os.sep): return "<repo-parent>/" + os.path.relpath(p, par)
    return os.path.basename(p)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def source_state():
    """git status (tracked, untracked and ignored) of the source folders, and sha256 of every file in ESZ1's folder."""
    st = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--ignored", "--"] + SOURCE_PATHS,
                        cwd=REPO, capture_output=True, text=True, check=True).stdout
    hs = {}
    for root, _, files in os.walk(ESZ1_DIR):
        for fn in sorted(files):
            p = os.path.join(root, fn); hs[os.path.relpath(p, REPO)] = sha256(p)
    return st, hs


def read_masks():
    """id -> mask radius (arcsec); EUC17's table first; conflicts between the tables reported."""
    rad, src, conflicts, nomask = {}, {}, [], []
    for path in MASKS:
        with open(path, newline="") as f:
            for r in csv.DictReader(f):
                try: R = float(r["mask_radius_arcsec"])
                except Exception: R = float("nan")
                ok = r["has_mask"].strip() == "1" and math.isfinite(R) and R > 0
                uid = r["unique_identifier"]
                if not ok:
                    nomask.append((uid, os.path.basename(path))); continue
                if uid in rad:
                    if abs(rad[uid] - R) > 1e-12: conflicts.append((uid, rad[uid], R))
                    continue
                rad[uid] = R; src[uid] = os.path.basename(path)
    return rad, src, conflicts, nomask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=sorted(MODES))
    ap.add_argument("--data-dir", default=os.path.join(REPO, "_external_data", "euclid_dr1_eclipse"))
    ap.add_argument("--y-dir", default=os.path.join(os.path.dirname(REPO), "_external_data", "act_dr6_nilc"))
    ap.add_argument("--erass", default=os.path.join(os.path.dirname(REPO), "_external_data", "cfg687_inputs", "erass1_main.tsv"))
    a = ap.parse_args()
    sign, rescale = MODES[a.mode]
    outdir = os.path.join(HERE, "runs", a.mode); os.makedirs(outdir, exist_ok=True)
    t0 = time.time()
    REC = dict(lane="EUC21R", mode=a.mode, sign=sign, re_scale_in_f=rescale, source=rel(ESZ1_PY), source_sha256=sha256(ESZ1_PY),
               inputs=dict(data_dir=rel(a.data_dir), y_dir=rel(a.y_dir), erass=rel(a.erass), masks=[rel(m) for m in MASKS]),
               threads=os.environ.get("OMP_NUM_THREADS"))
    st0, hs0 = source_state()

    # ---- the one substitution
    text = open(ESZ1_PY, encoding="utf-8").read()
    REC["substitution_count"] = text.count(OLD)
    if REC["substitution_count"] != 1:
        REC["error"] = "substitution text found %d times (must be exactly once)" % REC["substitution_count"]
        json.dump(REC, open(os.path.join(outdir, "driver.json"), "w"), indent=1); print(REC["error"], file=sys.stderr); sys.exit(4)
    text = text.replace(OLD, NEW, 1)

    # ---- redirect ESZ1's writes
    real_open = builtins.open; redirected = []
    def ropen(file, mode="r", *args, **kw):
        if isinstance(file, (str, bytes, os.PathLike)) and any(c in mode for c in "wax+"):
            p = os.path.realpath(os.fsdecode(file))
            if os.path.dirname(p) == ESZ1_DIR:
                q = os.path.join(outdir, os.path.basename(p)); redirected.append(os.path.basename(p))
                return real_open(q, mode, *args, **kw)
            raise RuntimeError("EUC21R: write outside ESZ1's own folder refused: %s" % rel(p))
        return real_open(file, mode, *args, **kw)

    ns = {"__name__": "esz1_under_euc21r", "__file__": ESZ1_PY, "__builtins__": builtins, "open": ropen}
    argv0 = sys.argv
    sys.argv = [ESZ1_PY, "--data-dir", a.data_dir, "--y-dir", a.y_dir, "--erass", a.erass]
    exec(compile(text, ESZ1_PY, "exec"), ns)            # module level only: imports EUC1, EUC4, EUC8 from their own folders
    E = ns["E"]

    # ---- wrap EUC1's loader
    rad, src, conflicts, nomask = read_masks()
    REC["mask_table"] = dict(with_mask=len(rad), conflicts=conflicts, no_mask_rows=len(nomask))
    FT = []
    orig_load = E.load
    def load_wrapped(data_dir):
        rows, nobj = orig_load(data_dir)
        S_ids = {r["id"] for r in E.select(rows, ("A", "B"))[0]}         # selection before the shift (lm > 0 is unchanged by f <= 1)
        miss, bad = [], []
        for r in rows:
            uid = r["id"]
            if uid not in rad:
                if uid in S_ids: miss.append(uid)
                continue
            if a.mode == "harness":
                f = 1.0
            else:
                f = float(E.M2D_frac(rad[uid], r["te"] * rescale, r["n"]))
            if not (math.isfinite(f) and 0.0 < f <= 1.0):
                if uid in S_ids: bad.append((uid, f))
                FT.append((uid, int(uid in S_ids), rad[uid], r["te"], r["n"], f, r["lm"], r["lm"]))
                continue
            lm0 = r["lm"]
            r["lm"] = lm0 + sign * math.log10(f) if sign != 0 else lm0 - math.log10(f)
            FT.append((uid, int(uid in S_ids), rad[uid], r["te"], r["n"], f, lm0, r["lm"]))
        REC["S_ids"] = len(S_ids); REC["S_without_mask"] = miss; REC["S_bad_f"] = bad
        REC["rows_shifted"] = len(FT)
        return rows, nobj
    E.load = load_wrapped

    code = None
    try:
        ns["main"]()
        code = 0
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 9)
    finally:
        sys.argv = argv0
        import gc; gc.collect()
    REC["source_exit"] = code; REC["redirected_writes"] = redirected

    with real_open(os.path.join(outdir, "f_table.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["unique_identifier", "in_S", "mask_radius_arcsec", "te_arcsec", "sersic_n", "f", "lm_catalogue", "lm_used"])
        for row in FT: w.writerow([row[0], row[1], "%.10g" % row[2], "%.10g" % row[3], "%.10g" % row[4], "%.10g" % row[5], "%.6f" % row[6], "%.6f" % row[7]])

    st1, hs1 = source_state()
    REC["H1_git_status_unchanged"] = st0 == st1; REC["H1_esz1_hashes_unchanged"] = hs0 == hs1
    REC["H1_ok"] = bool(st0 == st1 and hs0 == hs1)

    exit_code = code
    if a.mode == "invert":
        try:
            now = json.load(real_open(os.path.join(outdir, "esz1_results.json")))["partG"]["primary"]["fam"]
            was = json.load(real_open(os.path.join(ESZ1_DIR, "esz1_results.json")))["partG"]["primary"]["fam"]
            pm = {nm: (now["%s|B100" % nm]["pred_min"], was["%s|B100" % nm]["pred_min"]) for nm in ("canonical", "alt")}
            bites = all(x > y for x, y in pm.values())
        except Exception as e:
            pm, bites = {"error": repr(e)}, False
        REC["twin_B100_pred_min_now_vs_committed"] = pm; REC["twin_bites"] = bool(bites)
        exit_code = 1 if bites else 2
    REC["driver_exit"] = exit_code; REC["seconds"] = round(time.time() - t0, 1)
    json.dump(REC, real_open(os.path.join(outdir, "driver.json"), "w"), indent=1, default=str)
    print("EUC21R driver: mode %s, source exit %s, driver exit %s, H1 %s" % (a.mode, code, exit_code, REC["H1_ok"]), file=sys.stderr)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
