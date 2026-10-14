"""CFG763: the formation clock — how slowly must cold energy form at rest for young tidal dwarfs to be Newtonian?

Criteria: FROZEN_CRITERIA.md (committed alone, 5b747a56b). V^2 = V_N^2 + f (V_law^2 - V_N^2), f = 1 - exp(-t/tau).
V_N, V_law and their errors: CFG441's (code copied). Ages at -1 sigma for the bound (floored at 0.05 Gyr).
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  python3 cfg763.py      (CFG763_MUTATE=1: V_obs := V_law; exit 1 iff the lower bound then vanishes)
"""
import os, sys, math, csv, json

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG4_common as C4  # noqa: E402  (read only)

MUT = os.environ.get("CFG763_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg763{TAG}.out"), "w")
RES = {"lane": "CFG763", "criteria": "5b747a56b", "mutate": MUT, "numbers": {}}
G_KPC, KPC_M = 4.30091727e-6, 3.0856775814913673e19
ACC = 1e6 / KPC_M
NU = C4.nu_mono


def P_(s=""):
    print(s, flush=True)
    OUT.write(s + "\n")


P_(__doc__.strip())


def v_newton(M, R):
    return math.sqrt(G_KPC * M / R)


def v_law(M, R, a0, Mhost=None, Dp=None):
    gNi = G_KPC * M / R ** 2 * ACC
    if Mhost is None:
        ai = gNi * float(NU(gNi / a0))
    else:
        gNe = G_KPC * Mhost / Dp ** 2 * ACC
        ai = gNi * float(NU((gNi + gNe) / a0)) + gNe * (float(NU((gNi + gNe) / a0)) - float(NU(gNe / a0)))
    return math.sqrt(ai / ACC * R)


def pred_err(fn, M, eM, R, eR):
    v0 = fn(M, R)
    dm = (fn(M * 1.01, R) - v0) / (0.01 * M) * eM
    dr = (fn(M, R * 1.01) - v0) / (0.01 * R) * eR
    return v0, math.hypot(dm, dr)


OBJ = []
for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv"))):
    f = lambda k: float(r[k])
    OBJ.append(dict(name=r["object"], V=f("V_circ_kms"), eV=f("e_V_circ_kms"), M=f("M_bar_1e8") * 1e8, eM=f("e_M_bar_1e8") * 1e8,
                    R=f("R_out_kpc"), eR=f("e_R_out_kpc"), Mhost=0.6 * f("host_LK_1e10Lsun") * 1e10, Dp=f("D_p_kpc"),
                    t=f("tmerg_over_torb") * f("t_orb_Gyr"), et=f("tmerg_over_torb") * f("e_t_orb_Gyr"), t_orb=f("t_orb_Gyr")))
for r in csv.DictReader(open(os.path.join(CFG, "CFG441_old_tdgs_tidal_origin", "data", "tierB_arp72c.csv"))):
    f = lambda k: float(r[k])
    V, R = f("V_circ_kms"), f("R_out_kpc")
    OBJ.append(dict(name=r["object"], V=V, eV=0.5 * (f("e_V_circ_up") + f("e_V_circ_lo")), M=f("M_bar_1e8") * 1e8,
                    eM=f("e_M_bar_1e8") * 1e8, R=R, eR=f("e_R_out_kpc"), Mhost=None, Dp=None, t=f("age_Myr") / 1e3,
                    et=f("e_age_Myr") / 1e3, t_orb=2 * math.pi * R * KPC_M / 1e3 / V / 3.15576e16))

TAUS = 10 ** np.round(np.arange(-2, 2.0001, 0.01), 2)
c441 = json.load(open(os.path.join(CFG, "CFG441_old_tdgs_tidal_origin", "cfg441_old_tdgs_results.json")))["numbers"]["tierB"]["out"]
k1 = True
for fo in C4.FOOTS:
    a0 = C4.A0[fo]
    pre = []
    for o in OBJ:
        vn, en = pred_err(lambda M, R: v_newton(M, R), o["M"], o["eM"], o["R"], o["eR"])
        if o["Mhost"] is None:
            vl, el = pred_err(lambda M, R: v_law(M, R, a0), o["M"], o["eM"], o["R"], o["eR"])
        else:
            vl, el = pred_err(lambda M, R, o=o: v_law(M, R, a0, o["Mhost"], o["Dp"]), o["M"], o["eM"], o["R"], o["eR"])
        pre.append((vn, en, vl, el))
    vobs = np.array([p[2] if MUT else o["V"] for o, p in zip(OBJ, pre)])

    def chi2(tau, ages):
        tot = 0.0
        for o, (vn, en, vl, el), v, t in zip(OBJ, pre, vobs, ages):
            fr = 1.0 if tau == 0 else (0.0 if math.isinf(tau) else 1 - math.exp(-t / tau))
            vm = math.sqrt(vn ** 2 + fr * (vl ** 2 - vn ** 2))
            em = en + fr * (el - en)
            tot += (v - vm) ** 2 / (o["eV"] ** 2 + em ** 2)
        return tot

    lo_age = [max(o["t"] - o["et"], 0.05) for o in OBJ]
    nom_age = [o["t"] for o in OBJ]
    cl, cn = chi2(0.0, lo_age), chi2(math.inf, lo_age)
    if not MUT:
        k1 &= abs(cl - c441[fo]["chi2_law"]) <= 0.01 and abs(cn - c441[fo]["chi2_N"]) <= 0.01
    P_(f"\n{fo}: K1 chi2 tau->0 {cl:.3f} (CFG441 {c441[fo]['chi2_law']:.3f}); tau->inf {cn:.3f} (CFG441 {c441[fo]['chi2_N']:.3f})")
    out = {}
    for lab, ages in (("lower_1sigma_ages", lo_age), ("nominal_ages", nom_age)):
        ch = np.array([chi2(t, ages) for t in TAUS])
        cmin = min(ch.min(), chi2(math.inf, ages))
        ok = np.where(ch <= cmin + 3.84)[0]
        tmin = float(TAUS[ok[0]]) if ok.size else None
        fr = {tt: (1 - math.exp(-tt / tmin)) if tmin else None for tt in (1.0, 2.0, 3.0, 8.0)}
        orb = [tmin / o["t_orb"] for o in OBJ] if tmin else None
        out[lab] = dict(tau_min95_Gyr=tmin, chi2_min=float(cmin), f_at=fr, tau_over_torb=orb)
        P_(f"    {lab:18s}: tau_min,95 = {tmin} Gyr (chi2_min {cmin:.2f});  f(1/2/3/8 Gyr) = "
           + " / ".join(f"{fr[k]:.2f}" for k in (1.0, 2.0, 3.0, 8.0)) + f";  tau/t_orb = {min(orb):.2f}-{max(orb):.2f}")
    win = out["lower_1sigma_ages"]["tau_min95_Gyr"] is not None and out["lower_1sigma_ages"]["tau_min95_Gyr"] <= 3.47
    out["F2_window"] = "OPEN" if win else "CLOSED"
    P_(f"    F2: window [tau_min,95, 3.47 Gyr] {out['F2_window']}")
    RES["numbers"][fo] = out
P_(f"\nK1 {'PASS' if k1 else 'FAIL'}")
RES["K1"] = bool(k1)
if MUT:
    bite = all(RES["numbers"][fo]["lower_1sigma_ages"]["tau_min95_Gyr"] is not None
               and RES["numbers"][fo]["lower_1sigma_ages"]["tau_min95_Gyr"] <= 0.05 for fo in C4.FOOTS)
    P_(f"MUTATE bites: {bite}")
    rc = 1 if bite else 0
else:
    v = "OPEN" if all(RES["numbers"][fo]["F2_window"] == "OPEN" for fo in C4.FOOTS) else "CLOSED"
    RES["verdict"] = dict(F2=v)
    P_(f"VERDICT: F2 window {v}")
    rc = 0
json.dump(RES, open(os.path.join(HERE, f"cfg763_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(rc)
