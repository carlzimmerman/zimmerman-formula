#!/usr/bin/env python3
"""WV1 post hoc data row P1 (reported, not graded; requested by the coordinating session after the result landed):
SHP1's measurement of the cold component's shape against a cored Psi halo at R_TF = 0.15 / 0.26 r_ta holding the share,
with Psi INSIDE the law, as WV1's static reduction puts it (S0: div[mu grad Phi] = 4 pi G (rho_b + m|psi|^2)).
QX28's coupling (Psi outside the law, Newtonian add-on) is run beside it for contrast.

Data and loaders: SHP1's own (`fable52_push/SHP1_cold_component_shape/shp1.py`, executed up to its first printed line, which
defines its rows and loads SPARC and B21's KiDS-1000 isolated lenses, and writes nothing). SPARC radii come from a copy of SHP1's loader that
also keeps r (the copy must reproduce SHP1's g_bar and g_obs arrays exactly: check P1-KA).

Rows:
- SPARC (SHP1's R1 statistic): per point delta = log10(g_obs / g_pred); median per log10 x bin (bins with n >= 20);
  SHP1's line is |median| <= 0.10 dex in every graded bin.
- KiDS (SHP1's R2 statistic, B21 Nobins, full covariance): chi^2 of g_obs against g_pred, and the predicted vs measured
  inverse-variance mean of g / g_law - 1. Lens radii from SHP1's kids_R at log M_b 10.45 (as SHP1's R4_nobins).
- V1's room: the largest unconverted share S_rem that sits inside the law with the deep ratio sqrt(1 + S_rem) still
  below SHP1's measured mean + 2 sigma.

Psi profiles (all S M_b inside R_TF, zero outside): uniform sphere (the least centrally concentrated core) and the
n = 1 Thomas-Fermi shape sin(pi r/R)/(pi r/R). r_ta(M_b) is FLD1's z = 0 table, interpolated in log-log.
    python3 wv1_shp1_row.py -> wv1_shp1_row.out, wv1_shp1_row.json
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SHP1 = os.path.join(REPO, "fable52_push", "SHP1_cold_component_shape")
src = open(os.path.join(SHP1, "shp1.py")).read()
cut = src.index('P(f"SHP1 {TAG}: SPARC')                 # definitions and data loading only; nothing is written
NS = {"__file__": os.path.join(SHP1, "shp1.py"), "__name__": "shp1_lib"}
_argv = sys.argv; sys.argv = ["shp1.py"]; exec(compile(src[:cut], "shp1.py", "exec"), NS); sys.argv = _argv
G, MS, KPC, A0, u_in = NS["G"], NS["MS"], NS["KPC"], NS["A0"], NS["u_in"]
LBX, R2, NOB, NOB_C, HOT, HOT_C, kids_R = NS["LBX"], NS["R2"], NS["NOB"], NS["NOB_C"], NS["HOT"], NS["HOT_C"], NS["kids_R"]
LINES, RES = [], {"note": "post hoc, reported, not graded", "rows": {}}


def P_(s=""):
    LINES.append(s); print(s, flush=True)


def law(gN, a0):
    return a0 * u_in(np.asarray(gN, float) / a0)


def sparc_r(ud=0.5, ub=0.7):
    """SHP1's sparc() (same files, cuts and expressions), also returning r and the galaxy's M_b."""
    d = os.path.join(REPO, "real_research", "data")
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    tab = {}
    for line in open(os.path.join(d, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19: continue
        try: tab[tok[0]] = dict(zip(keys, [float(t) for t in tok[1:18]]))
        except ValueError: continue
    pts = []
    for fn in sorted(os.listdir(os.path.join(d, "sparc_data"))):
        if not fn.endswith("_rotmod.dat"): continue
        nm = fn.replace("_rotmod.dat", "")
        a = np.genfromtxt(os.path.join(d, "sparc_data", fn), comments="#")
        if a.ndim != 2 or a.shape[1] < 6 or nm not in tab: continue
        m = tab[nm]
        if m["Q"] >= 3 or m["Inc"] < 30: continue
        Mb = (ud * m["L36"] + 1.33 * m["MHI"]) * 1e9 * MS
        for R, Vo, eV, Vg, Vd, Vb in a[:, :6]:
            if Vo <= 0 or R <= 0 or eV / Vo > 0.1: continue
            r = R * KPC
            gb = (Vg * abs(Vg) + ud * Vd * abs(Vd) + ub * Vb * abs(Vb)) * 1e6 / r
            if gb <= 0: continue
            pts.append((gb, Vo * Vo * 1e6 / r, Mb, r))
    a = np.array(pts)
    return dict(gbar=a[:, 0], gobs=a[:, 1], Mb=a[:, 2], r=a[:, 3])


FLD1_RTA = {7: 19, 8: 40, 9: 88, 9.4: 120, 10: 190, 10.45: 268, 10.7: 325, 10.9: 378, 11.2: 476, 11.5: 600}   # kpc, z = 0
_lm = np.array(sorted(FLD1_RTA)); _lr = np.log10([FLD1_RTA[k] for k in _lm])


def r_ta(Mb_kg):
    """log-log interpolation of FLD1's table, extended linearly in log-log beyond its ends."""
    lm = np.log10(np.asarray(Mb_kg, float) / MS)
    lr = np.interp(lm, _lm, _lr)
    lo, hi = lm < _lm[0], lm > _lm[-1]
    lr = np.where(lo, _lr[0] + (lm - _lm[0]) * (_lr[1] - _lr[0]) / (_lm[1] - _lm[0]), lr)
    lr = np.where(hi, _lr[-1] + (lm - _lm[-1]) * (_lr[-1] - _lr[-2]) / (_lm[-1] - _lm[-2]), lr)
    return 10 ** lr * KPC


def frac_enclosed(s, shape):
    s = np.clip(s, 0, 1)
    if shape == "uniform":
        return s ** 3
    return (np.sin(np.pi * s) - np.pi * s * np.cos(np.pi * s)) / np.pi          # n = 1 TF, normalised to 1 at s = 1


def gpsi(r, Mb, f, S, shape):
    R = f * r_ta(Mb)
    return G * S * Mb * frac_enclosed(r / R, shape) / r ** 2


P_("WV1 post hoc data row P1: SHP1's shape measurement against a cored Psi halo. Reported, not graded. "
   "kappa = 1/2 FITTED; not theory closed.")
S = sparc_r()
S0 = NS["sparc"]()
ka = bool(np.array_equal(S["gbar"], S0["gbar"]) and np.array_equal(S["gobs"], S0["gobs"]))
RES["P1_KA_loader_identical"] = ka
P_(f"P1-KA: copied loader reproduces SHP1's {len(S0['gbar'])} SPARC points exactly: {ka}")
if not ka:
    sys.exit(1)

for fo in ("canonical", "alt"):
    a0 = A0[fo]
    P_("")
    P_(f"================ {fo} (a0 {a0:g}) ================")
    lx = np.log10(np.sqrt(a0 / S["gbar"]))

    def r1(gpred):
        d = np.log10(S["gobs"] / gpred); rows = []
        for lo, hi in zip(LBX[:-1], LBX[1:]):
            m = (lx >= lo) & (lx < hi); n = int(m.sum())
            if n < 20: continue
            rows.append((float(lo), float(hi), n, float(np.median(d[m]))))
        worst = max(abs(r_[3]) for r_ in rows)
        return rows, worst
    base_rows, base_worst = r1(law(S["gbar"], a0))
    P_(f"SPARC R1, law of baryons alone (SHP1's own row): worst bin median {base_worst:.3f} dex (line 0.10)")
    # KiDS published / hot gas, law alone
    k_base = {nm: R2(D, C, a0) for nm, (D, C) in (("published", (NOB, NOB_C)), ("hotgas", (HOT, HOT_C)))}
    for nm, r_ in k_base.items():
        P_(f"KiDS {nm}, law alone: chi2 {r_['chi2']:.1f}/{r_['N']}, mean g/g_law - 1 = {r_['mean_ratio_minus_1']:+.3f} +- {r_['sigma']:.3f}")
    out = {"SPARC_law_alone_worst": base_worst, "KiDS_law_alone": {k: {"chi2": v["chi2"], "mean": v["mean_ratio_minus_1"],
                                                                      "sigma": v["sigma"]} for k, v in k_base.items()}}
    for Sh in (5.41, 5.562):
        for f in (0.15, 0.26):
            for shape in ("uniform", "TF n=1"):
                gp = gpsi(S["r"], S["Mb"], f, Sh, shape)
                rows_in, w_in = r1(law(S["gbar"] + gp, a0))              # WV1: Psi inside the law
                rows_out, w_out = r1(law(S["gbar"], a0) + gp)            # QX28: Psi outside the law
                # KiDS: lens radius at log M_b 10.45
                kres = {}
                for nm, (D, C) in (("published", (NOB, NOB_C)), ("hotgas", (HOT, HOT_C))):
                    Mb = 10 ** 10.45 * MS
                    rr = kids_R(D["gbar"], 10.45)
                    gk = gpsi(rr, Mb, f, Sh, shape)
                    for cpl, gpred in (("inside", law(D["gbar"] + gk, a0)), ("outside", law(D["gbar"], a0) + gk)):
                        res = D["gobs"] - gpred
                        c2 = float(res @ np.linalg.inv(C) @ res)
                        q = gpred / law(D["gbar"], a0) - 1
                        kres[f"{nm}_{cpl}"] = {"chi2": c2, "pred_ratio_min": float(1 + q.min()), "pred_ratio_max": float(1 + q.max())}
                key = f"S{Sh}_f{f}_{shape}"
                out[key] = {"SPARC_inside_worst": w_in, "SPARC_inside_bins": rows_in, "SPARC_outside_worst": w_out,
                            "KiDS": kres}
                P_(f"share {Sh} M_b in R_TF = {f} r_ta, {shape:7s}: SPARC worst bin (Psi inside the law) {w_in:.3f} dex "
                   f"{'FAILS' if w_in > 0.10 else 'within'} the 0.10 line [outside the law: {w_out:.3f}]; KiDS published chi2 inside "
                   f"{kres['published_inside']['chi2']:.0f}/15 (predicted g/g_law {kres['published_inside']['pred_ratio_min']:.2f}-"
                   f"{kres['published_inside']['pred_ratio_max']:.2f}) [outside {kres['published_outside']['chi2']:.0f}/15]; hot gas inside "
                   f"{kres['hotgas_inside']['chi2']:.0f}/15 [outside {kres['hotgas_outside']['chi2']:.0f}/15]")
    # V1's room for an unconverted share inside the law (deep ratio sqrt(1 + S_rem) <= measured mean + 2 sigma)
    room = {}
    for nm, r_ in k_base.items():
        up = 1 + r_["mean_ratio_minus_1"] + 2 * r_["sigma"]
        room[nm] = up ** 2 - 1
    out["V1_room_S_rem"] = room
    P_(f"V1: the deep ratio of an unconverted share S_rem inside the law is sqrt(1 + S_rem); SHP1's mean + 2 sigma allows "
       f"S_rem <= {room['published']:.2f} (published) and {room['hotgas']:.2f} (hot gas), against a share of 5.41: at least "
       f"{100 * (1 - max(room['published'], 0) / 5.41):.0f} % / {100 * (1 - max(room['hotgas'], 0) / 5.41):.0f} % of Psi must be converted "
       f"into the law's phantom (form B), so no cored Psi halo beside the law survives")
    RES["rows"][fo] = out

P_("")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "wv1_shp1_row.out"), "w").write("\n".join(LINES) + "\n")
json.dump(RES, open(os.path.join(HERE, "wv1_shp1_row.json"), "w"), indent=1, default=float)
