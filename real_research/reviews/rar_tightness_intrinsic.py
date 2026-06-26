#!/usr/bin/env python3
"""
RAR TIGHTNESS discriminator: observed scatter, error budget, implied INTRINSIC scatter.
=======================================================================================
Computes, on the REAL 175 SPARC rotation curves (data/sparc_data/*_rotmod.dat, Lelli+2016)
plus the master table (SPARC_Lelli2016c.mrt for per-galaxy D, e_D, inc, e_inc, Q):

  (1) total OBSERVED rms scatter about the best-fit RAR (orthogonal-ish: along log g_obs),
      at BOTH the McGaugh Upsilon=0.50 footing AND the framework Upsilon=0.70 footing;
  (2) a per-point measurement+M/L error budget (V, distance, inclination, M/L) in dex;
  (3) the implied INTRINSIC scatter sigma_int^2 = sigma_obs^2 - <sigma_err^2>;
  (4) the comparison to LCDM-simulation RAR-scatter predictions (literature, hard-coded
      with author+year) -- the actual discriminator.

Deterministic, no synthetic data. Needs numpy + scipy.
"""
import numpy as np, glob, os
from scipy.optimize import minimize_scalar

kpc = 3.0856775814913673e19
DATA = os.path.join(os.path.dirname(__file__), "..", "data")
ROT = os.path.join(DATA, "sparc_data")
MRT = os.path.join(DATA, "SPARC_Lelli2016c.mrt")
A0_MCG = 1.20e-10
A0_FRAME = 9.36e-11


def load_master():
    m = {}
    lines = open(MRT).readlines()
    seps = [i for i, l in enumerate(lines) if l.startswith("---")]
    for l in lines[seps[-1] + 1:]:
        p = l.split()
        if len(p) < 18:
            continue
        try:
            m[p[0]] = (float(p[2]), float(p[3]), float(p[5]), float(p[6]), int(p[17]))
        except ValueError:
            continue
    return m


def build(master, ML_D, ML_B, ml_dex=0.10, use_cuts=True):
    """Return per-point arrays: g_bar, g_obs, e_lg_obs, e_lg_bar (all dex), galaxy id."""
    gbar, gobs, elgo, elgb, gid = [], [], [], [], []
    g = 0
    for fpath in sorted(glob.glob(os.path.join(ROT, "*_rotmod.dat"))):
        name = os.path.basename(fpath).replace("_rotmod.dat", "")
        meta = master.get(name)
        if meta is None:
            continue
        D, e_D, inc, e_inc, Q = meta
        if use_cuts and (Q > 2 or inc < 30):
            continue
        try:
            d = np.genfromtxt(fpath, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        Rm = R * kpc
        Vb2 = np.sign(Vg) * Vg ** 2 + ML_D * Vd ** 2 + ML_B * Vb ** 2
        gb = Vb2 * 1e6 / Rm
        go = (Vo * 1e3) ** 2 / Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vo > 0) & (eV > 0)
        if use_cuts:
            ok &= (eV / np.maximum(Vo, 1e-9) < 0.10)
        gb, go, Vo_, eV_ = gb[ok], go[ok], Vo[ok], eV[ok]
        if len(gb) == 0:
            continue
        dlnV = eV_ / Vo_
        dD = e_D / max(D, 1e-3)
        dinc = np.deg2rad(e_inc) / max(np.tan(np.deg2rad(inc)), 0.1)
        # g_obs = V^2/(R); R inferred from angular size*D so depends on D and inc projection of V
        e_lgo = np.sqrt((2 * dlnV) ** 2 + dD ** 2 + (2 * dinc) ** 2) / np.log(10)
        # g_bar dominated by M/L (ml_dex), plus D (R scaling) + inc (V deprojection in V_disk)
        e_lgb = np.full_like(gb, np.sqrt((ml_dex * np.log(10)) ** 2 + dD ** 2 + (2 * dinc) ** 2) / np.log(10))
        gbar += list(gb); gobs += list(go); elgo += list(e_lgo); elgb += list(e_lgb)
        gid += [g] * len(gb)
        g += 1
    return map(np.array, (gbar, gobs, elgo, elgb, gid))


def rar_pred(gbar, a0):
    """McGaugh interpolating RAR (the standard fitting form)."""
    return gbar / (1.0 - np.exp(-np.sqrt(gbar / a0)))


def fit_a0_and_scatter(gbar, gobs, a0_fixed=None):
    lgo = np.log10(gobs)
    if a0_fixed is None:
        def cost(la):
            r = lgo - np.log10(rar_pred(gbar, 10 ** la))
            return np.std(r - np.median(r))
        res = minimize_scalar(cost, bounds=(np.log10(0.4e-10), np.log10(3e-10)), method="bounded")
        a0 = 10 ** res.x
    else:
        a0 = a0_fixed
    r = lgo - np.log10(rar_pred(gbar, a0))
    r = r - np.median(r)
    return a0, float(np.std(r)), r


def report(tag, master, ML_D, ML_B):
    gbar, gobs, elgo, elgb, gid = build(master, ML_D, ML_B)
    elg = np.sqrt(elgo ** 2 + elgb ** 2)
    ngal = len(np.unique(gid))
    print(f"\n{'='*78}\n{tag}: Upsilon_disk={ML_D}, Upsilon_bulge={ML_B}  ({ngal} gal, {len(gbar)} pts)\n{'='*78}")

    # free-fit a0
    a0f, sc_free, r_free = fit_a0_and_scatter(gbar, gobs)
    # fixed framework a0
    _, sc_frame, r_frame = fit_a0_and_scatter(gbar, gobs, a0_fixed=A0_FRAME)
    # fixed canonical a0
    _, sc_mcg, r_mcg = fit_a0_and_scatter(gbar, gobs, a0_fixed=A0_MCG)

    med_err = float(np.median(elg))
    mean_err2 = float(np.mean(elg ** 2))
    rms_err = float(np.sqrt(mean_err2))

    print(f"  best-fit a0                 = {a0f*1e10:.3f}e-10  m/s^2")
    print(f"  TOTAL observed rms scatter  = {sc_free:.4f} dex  (free a0)")
    print(f"                                {sc_frame:.4f} dex  (fixed a0=9.36e-11, framework)")
    print(f"                                {sc_mcg:.4f} dex  (fixed a0=1.20e-10, McGaugh)")
    print(f"  median per-pt err budget    = {med_err:.4f} dex   (rms {rms_err:.4f} dex)")

    # implied intrinsic (subtract in quadrature, using rms error to match variance accounting)
    for sc, lab in [(sc_free, "free-a0"), (sc_frame, "framework-a0")]:
        var_int = sc ** 2 - mean_err2
        if var_int > 0:
            sig_int = np.sqrt(var_int)
            print(f"  implied INTRINSIC ({lab:11}): sqrt({sc:.3f}^2 - {rms_err:.3f}^2) = {sig_int:.4f} dex")
        else:
            print(f"  implied INTRINSIC ({lab:11}): {sc:.3f}^2 - {rms_err:.3f}^2 < 0  -> error budget >= observed; "
                  f"intrinsic <~ {0.5*abs(var_int)**0.5:.3f} dex (consistent with 0)")
    return sc_free, sc_frame, rms_err


def main():
    master = load_master()
    print("#" * 78)
    print("# RAR TIGHTNESS: observed scatter, error budget, implied INTRINSIC scatter")
    print("# Real SPARC (Lelli+2016), McGaugh interpolating RAR, both-ways footing")
    print("#" * 78)

    # both footings
    sf50, sx50, e50 = report("McGaugh footing", master, 0.50, 0.70)
    sf70, sx70, e70 = report("FRAMEWORK footing", master, 0.70, 0.70)

    # also with a smaller M/L error (0.07 dex, which several RAR papers adopt for 3.6um)
    print(f"\n{'='*78}\nSENSITIVITY: M/L scatter assumption (drives the error budget)\n{'='*78}")
    for ml_dex in (0.07, 0.10, 0.13):
        gbar, gobs, elgo, elgb, gid = build(master, 0.70, 0.70, ml_dex=ml_dex)
        elg = np.sqrt(elgo ** 2 + elgb ** 2)
        rms_err = float(np.sqrt(np.mean(elg ** 2)))
        _, sc, _ = fit_a0_and_scatter(gbar, gobs)
        vint = sc ** 2 - rms_err ** 2
        sint = (vint ** 0.5) if vint > 0 else 0.0
        print(f"  M/L scatter {ml_dex:.2f} dex -> rms err {rms_err:.3f} dex, obs {sc:.3f} dex, "
              f"intrinsic {sint:.3f} dex" + ("" if vint > 0 else "  (consistent with 0)"))

    print(f"\n{'='*78}\nLITERATURE: LCDM-simulation RAR-scatter predictions vs observed ~0.13 dex\n{'='*78}")
    lit = [
        ("Lelli+2017 (obs intrinsic)",      "0.057 dex intrinsic (after full error budget); 0.13 dex total observed", "OBS"),
        ("Desmond 2017 (semi-emp LCDM)",    "predicts >~0.05-0.06 dex floor from M*-Mhalo + c-Mhalo scatter ALONE; "
                                            "argues full feedback scatter would exceed observed unless conspiratorial", "LCDM"),
        ("Keller & Wadsley 2017 (MUGS2)",   "18 zoom sims reproduce RAR with ~0.05-0.1 dex scatter -- BUT only 18 gal, "
                                            "tuned feedback, no abundance-matching scatter sampled", "LCDM"),
        ("Ludlow+2017 (EAGLE/APOSTLE)",     "hydro sims yield a tight RAR ~0.09 dex; emergent, attributed to "
                                            "dissipative collapse self-regulation (LCDM CAN make it tight)", "LCDM"),
        ("Dutton+2019 (NIHAO)",             "~0.05-0.08 dex sim scatter, RAR reproduced; sim-dependent normalization", "LCDM"),
        ("Stone & Courteau 2019",           "obs total ~0.11-0.13 dex incl. larger sample, consistent", "OBS"),
    ]
    for src, claim, kind in lit:
        print(f"  [{kind:4}] {src:30} {claim}")


if __name__ == "__main__":
    main()
