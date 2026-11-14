#!/usr/bin/env python3
"""EUC20R common pieces (blind re-grade of EUC20; reading note READING.md, commit 025dc97b73).

Paths, the mask union (EUC17 + EUC19 tables), the per-lens share f = M2D_frac(mask_radius, R_e, n) with EUC1's own
function, the log-mass shift of each mode, and a write-redirecting open.  Imported by the other EUC20R scripts.
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import builtins, csv, math, os, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "_external_data", "euclid_dr1_eclipse")
DIRS = dict(
    EUC1=os.path.join(REPO, "closure_2026_11_12", "EUC1_eclipse_saturation_ceiling"),
    EUC4=os.path.join(REPO, "closure_2026_11_12", "EUC4_wide_lenses"),
    EUC5=os.path.join(REPO, "closure_2026_11_12", "EUC5_dynamical_boost"),
    EUC6=os.path.join(REPO, "closure_2026_11_12", "EUC6_wide_lens_environment"),
    EUC8=os.path.join(REPO, "closure_2026_11_12", "EUC8_wide_lens_residual_profile"),
    EUC10=os.path.join(REPO, "closure_2026_11_12", "EUC10_published_source_redshifts"),
    EUC17=os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread"),
    EUC19=os.path.join(REPO, "closure_2026_11_14", "EUC19_grade_b_mask_table"),
    LNJ1=os.path.join(REPO, "closure_2026_11_13", "LNJ1_joint_switch_on_euclid_lenses"),
    JNT2=os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint"),
    PD1=os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust"),
)
MASK_FILES = [os.path.join(DIRS["EUC17"], "euc17_masks.csv"), os.path.join(DIRS["EUC19"], "euc19_masks.csv")]
MODES = ("f1", "primary", "F1a", "F1b", "invert")
RE_SCALE = {"f1": 1.0, "primary": 1.0, "F1a": 0.80, "F1b": 1.25, "invert": 1.0}
FOOT = {"canonical": 9.3603e-11, "alt": 1.132e-10}


def rel(p):
    return os.path.relpath(p, REPO)


def load_masks():
    """id -> mask radius (arcsec) for lenses with a mask record; plus the raw counts."""
    masks, seen, info = {}, set(), {}
    for p in MASK_FILES:
        n_rows = n_mask = 0
        with builtins.open(p, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                n_rows += 1
                uid = r["unique_identifier"]
                if uid in seen:
                    raise SystemExit("identifier in both mask tables: %s" % uid)
                seen.add(uid)
                try:
                    rad = float(r["mask_radius_arcsec"])
                except Exception:
                    rad = float("nan")
                if r["has_mask"].strip() == "1" and math.isfinite(rad) and rad > 0:
                    masks[uid] = rad; n_mask += 1
        info[rel(p)] = dict(rows=n_rows, with_mask=n_mask)
    return masks, info


_E = None
def euc1():
    """EUC1's module, imported under the name both source scripts use."""
    global _E
    if _E is None:
        if DIRS["EUC1"] not in sys.path:
            sys.path.insert(0, DIRS["EUC1"])
        import euc1 as E
        _E = E
    return _E


def share(mask_radius, te_arcsec, n, re_scale=1.0):
    """f = M2D_frac(mask radius, R_e x re_scale, n), EUC1's function; None if not finite or not in (0, 1]."""
    E = euc1()
    try:
        te = float(te_arcsec) * re_scale; n = float(n)
        if not (te > 0 and math.isfinite(n) and n > 0):
            return None
        f = float(E.M2D_frac(float(mask_radius), te, n))
    except Exception:
        return None
    if not (math.isfinite(f) and 0.0 < f <= 1.0):
        return None
    return f


class Shifter:
    """the log-mass shift of each lens in a mode: f1 -> 0; primary/F1a/F1b -> -log10 f; invert -> +log10 f."""
    def __init__(self, mode):
        if mode not in MODES:
            raise SystemExit("unknown mode %s" % mode)
        self.mode = mode; self.scale = RE_SCALE[mode]
        self.masks, self.info = load_masks()
        self.applied, self.nomask, self.badf = set(), set(), set()

    def dlm(self, uid, te_arcsec, n):
        if self.mode == "f1":
            return 0.0
        rad = self.masks.get(uid)
        if rad is None:
            self.nomask.add(uid); return 0.0
        f = share(rad, te_arcsec, n, self.scale)
        if f is None:
            self.badf.add(uid); return 0.0
        self.applied.add(uid)
        lf = math.log10(f)
        return lf if self.mode == "invert" else -lf

    def logf(self, uid, te_arcsec, n):
        """log10 f of the mode's share (0 if no mask), independent of the sign convention."""
        rad = self.masks.get(uid)
        if rad is None:
            return 0.0, False
        f = share(rad, te_arcsec, n, self.scale)
        if f is None:
            return 0.0, False
        return math.log10(f), True


def redirecting_open(outdir, log):
    """an open() that sends every write-mode open to outdir (same basename) and leaves reads alone."""
    real = builtins.open
    def _open(file, mode="r", *a, **kw):
        if isinstance(file, (str, bytes, os.PathLike)) and any(c in mode for c in "wax+"):
            src = os.fspath(file)
            dst = os.path.join(outdir, os.path.basename(src))
            log.append(dict(source=rel(os.path.abspath(src)), written=rel(dst), mode=mode))
            return real(dst, mode, *a, **kw)
        return real(file, mode, *a, **kw)
    return _open
