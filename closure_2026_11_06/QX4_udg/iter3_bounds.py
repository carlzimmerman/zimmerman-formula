"""QX4 iteration 3: what else the action and the data could do, as bounds and requirements.

Criteria: FROZEN_CRITERIA.md (c0d7f31b1e), iteration 3. Data and baryons come from UD1/UD2, executed read-only.
Algebraic law with UD's nu. Both footings, never pooled. Kappa = 1/2 FITTED; not theory closed.

usage: python3 iter3_bounds.py [main|MUTATE]   MUTATE: nu = 1. With Newton there is no deep-MOND D^(1/2) scaling,
       so the distance requirement must change (the scan sees the law); outputs iter3_MUTATE.*
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
LSTAR = dict(canonical=0.0217, alt=0.0229)                     # kpc (D10 lower bounds)
CONV = 1e6 / 3.0857e19
KMS_KPC_MYR = 977.8                                            # 1 kpc / (1 km/s) in Myr
OUT, RES = [], {}


def P(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s, flush=True)


def nu(y):
    if MODE == "MUTATE": return np.ones_like(np.asarray(y, float))
    y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)


def law_v(vb2, R, a0):
    gN = vb2 / R * CONV; return np.sqrt(nu(gN / a0) * gN / CONV * R)


def chi2p(v, e, m): c = float(np.sum(((v - m) / e) ** 2)); return c, float(CHI2.sf(c, len(v)))


def load(path, stop):
    src = open(path).read(); ns = dict(__file__=path, __name__="ud_import"); old = sys.argv; sys.argv = [path, "law"]
    try:
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index(stop)], path, "exec"), ns)
    finally: sys.argv = old
    return ns


u1 = load(UD1, "# ---- K0a"); u2 = load(UD2, "# ---- grade")
kin = np.asarray(u1["AD2"])
GAL = dict(AGC114905=dict(R=np.asarray(u1["Rk"]), V=np.asarray(u1["V"]), E=np.asarray(u1["E"]), vb2=np.asarray(u1["vb2"]),
                          D=78.7, AD2=kin),
           Malin1=dict(R=u2["RT"], V=u2["VT"], E=u2["ET"], D=322.0, AD2=None,
                       vb2=u2["comp"]["gas"] ** 2 + u2["comp"]["lsb"] ** 2 + u2["comp"]["hsb"] ** 2))
S = np.exp(np.linspace(np.log(0.01), np.log(3.0), 4000))
P(f"QX4 iter3 bounds and requirements, mode {MODE}. kappa = 1/2 FITTED; not theory closed.")
for gname, d in GAL.items():
    RES[gname] = {}
    for f, a0 in FOOT.items():
        vl = law_v(d["vb2"], d["R"], a0); need = (d["V"] / vl) ** 2 - 1; iw = int(np.argmax(np.abs(need)))
        stiff = (LSTAR[f] / d["R"]) ** 2
        # distance: R -> s R, V_bar^2 -> s V_bar^2 (M ~ D^2, R ~ D); V_obs fixed
        dist = np.array([chi2p(d["V"], d["E"], law_v(s * d["vb2"], s * d["R"], a0)) for s in S])
        mass = np.array([chi2p(d["V"], d["E"], law_v(s * d["vb2"], d["R"], a0)) for s in S])
        okD = S[dist[:, 1] >= 0.05]; okM = S[mass[:, 1] >= 0.05]
        Ro, Vo = float(d["R"][-1]), float(d["V"][-1])
        t_ff = Ro / vl[-1] * KMS_KPC_MYR; t_orb = 2 * np.pi * Ro / Vo * KMS_KPC_MYR
        row = dict(required_rel_dg=need.tolist(), worst_ring=float(d["R"][iw]), worst_need=float(need[iw]),
                   stiffness_bound=stiff.tolist(), stiffness_over_need=float(np.max(stiff) / abs(need[iw])),
                   ac2q_bound=2.2e-10,
                   D_factor_ok=[float(okD.min()), float(okD.max())] if len(okD) else None,
                   mass_factor_ok=[float(okM.min()), float(okM.max())] if len(okM) else None,
                   t_ff_Myr=t_ff, t_orb_Myr=t_orb)
        if d["AD2"] is not None: row["asym_drift_sign"] = "raises V_c (wrong sign)" if np.all(d["AD2"] >= 0) else "mixed"
        RES[gname][f] = row
        P(f"[{gname} {f}] required relative change in g, ring by ring: {np.round(need,3).tolist()} (worst {need[iw]:+.3f} at R {d['R'][iw]:.1f})")
        P(f"   v3s stiffness bound (Lstar/R)^2 <= {np.max(stiff):.1e}; AC2q s^2 terms <= 2.2e-10 -> {np.max(stiff)/abs(need[iw]):.1e} of the need: NOT RESCUED")
        P(f"   distance factor for p >= 0.05: {row['D_factor_ok']} (D = {d['D']} Mpc x that); mass factor: {row['mass_factor_ok']}")
        P(f"   non-equilibrium: infall time at the law's speed {t_ff:.0f} Myr vs orbital period {t_orb:.0f} Myr"
          f" (ratio {t_ff/t_orb:.2f}): rescue needs the disc younger than {t_ff:.0f} Myr")
        if d["AD2"] is not None: P(f"   asymmetric drift V_c^2 - V_rot^2 = {np.round(d['AD2'],0).tolist()} (km/s)^2: {row['asym_drift_sign']}")
name = "iter3_MUTATE" if MODE == "MUTATE" else "iter3"
json.dump(RES, open(os.path.join(HERE, name + ".json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, name + ".out"), "w").write("\n".join(OUT) + "\n")
