"""QX4 iteration 2: the external field effect. Requirement on g_e, then the host a regular disc would need.

Criteria: FROZEN_CRITERIA.md (c0d7f31b1e), iteration 2. 1D EFE estimator as in UD1/UD2:
g = nu((g_N+g_e)/a0)(g_N+g_e) - nu(g_e/a0) g_e. Data and baryons come from UD1/UD2, executed read-only.
Both footings, never pooled. Kappa = 1/2 FITTED; not theory closed. One galaxy excludes nothing.

usage: python3 iter2_efe.py [main|MUTATE]   MUTATE: nu = 1 (EFE has no effect: g_e,req must not exist for AGC,
       because Newton fails there at chi2 55; outputs iter2_MUTATE.*)
"""
import io, json, os, sys, contextlib
import numpy as np
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MODE = sys.argv[1] if len(sys.argv) > 1 else "main"
UD1 = os.path.join(ROOT, "rebuild_2026_10_22", "UD1_agc114905_udg_rotation", "ud1.py")
UD2 = os.path.join(ROOT, "rebuild_2026_10_22", "UD2_malin1_giant_lsb", "ud2.py")
FOOT = dict(canonical=9.3603e-11, alt=1.1312e-10)
CONV = 1e6 / 3.0857e19; G = 4.30091e-6
OUT, RES = [], {}


def P(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s, flush=True)


def nu(y):
    if MODE == "MUTATE": return np.ones_like(np.asarray(y, float))
    y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)


def law_v(vb2, R, a0, ge):
    gN = vb2 / R * CONV; gt = gN + ge * a0
    g = nu(gt / a0) * gt - (nu(ge) * ge * a0 if ge > 0 else 0.0)
    return np.sqrt(np.maximum(g / CONV * R, 0))


def chi2p(v, e, m): c = float(np.sum(((v - m) / e) ** 2)); return c, float(CHI2.sf(c, len(v)))


def load(path, stop):
    src = open(path).read(); ns = dict(__file__=path, __name__="ud_import"); old = sys.argv; sys.argv = [path, "law"]
    try:
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index(stop)], path, "exec"), ns)
    finally: sys.argv = old
    return ns


u1 = load(UD1, "# ---- K0a"); u2 = load(UD2, "# ---- grade")
GAL = dict(AGC114905=dict(R=np.asarray(u1["Rk"]), V=np.asarray(u1["V"]), E=np.asarray(u1["E"]), vb2=np.asarray(u1["vb2"])),
           Malin1=dict(R=u2["RT"], V=u2["VT"], E=u2["ET"],
                       vb2=u2["comp"]["gas"] ** 2 + u2["comp"]["lsb"] ** 2 + u2["comp"]["hsb"] ** 2))
GE = np.concatenate([[0.0], np.exp(np.linspace(np.log(1e-3), np.log(3.0), 3000))])
P(f"QX4 iter2 EFE, mode {MODE}. kappa = 1/2 FITTED; not theory closed.")
KPC = 3.0857e19; MSUN = 1.989e30; GSI = 6.674e-11
for gname, d in GAL.items():
    RES[gname] = {}
    for f, a0 in FOOT.items():
        ch = np.array([chi2p(d["V"], d["E"], law_v(d["vb2"], d["R"], a0, ge)) for ge in GE])
        ok = GE[ch[:, 1] >= 0.05]; ib = int(np.argmin(ch[:, 0]))
        row = dict(chi2_min=float(ch[ib, 0]), ge_at_min=float(GE[ib]), p_ok=[float(ok.min()), float(ok.max())] if len(ok) else None)
        if len(ok):
            ge = float(ok.min()) * a0                                                  # m/s^2, smallest rescuing field
            Ro = float(d["R"][-1]) * KPC; gint = (float(d["V"][-1]) * 1e3) ** 2 / Ro
            if ge < a0:                                                                # host deep-MOND region at d
                dmin = ge * Ro / gint; M = (ge * dmin) ** 2 / (GSI * a0)
            else:                                                                      # Newtonian host region, tidal 2 g R/d
                dmin = 2 * ge * Ro / gint; M = ge * dmin ** 2 / GSI
            row.update(ge_req_over_a0=float(ok.min()), g_int_over_a0=gint / a0, host_dmin_kpc=dmin / KPC,
                       host_Mb_min_Msun=M / MSUN, label="CONDITIONAL")
            P(f"[{gname} {f}] chi2(g_e=0) {ch[0,0]:.1f}; p>=0.05 for g_e/a0 in {row['p_ok']}; requirement g_e >= {ok.min():.3f} a0;"
              f" outer g_int = {gint/a0:.3f} a0 -> a regular disc needs a host of baryonic mass >= {M/MSUN:.2e} Msun within"
              f" d >= {dmin/KPC:.0f} kpc (tidal g_e R/d < g_int) -> CONDITIONAL")
        else:
            row["label"] = "NOT RESCUED (no g_e in [0, 3 a0])"
            P(f"[{gname} {f}] chi2(g_e=0) {ch[0,0]:.1f}; min chi2 {ch[ib,0]:.1f} at g_e {GE[ib]:.3f} a0; no g_e in [0, 3] a0 reaches p >= 0.05 -> NOT RESCUED")
        RES[gname][f] = row
name = "iter2_MUTATE" if MODE == "MUTATE" else "iter2"
json.dump(RES, open(os.path.join(HERE, name + ".json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, name + ".out"), "w").write("\n".join(OUT) + "\n")
