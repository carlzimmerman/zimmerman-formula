"""CFG764: is the cold-energy formation clock a local orbital clock, tau = k t_orb?

Criteria: FROZEN_CRITERIA.md (committed alone, 9990bf4b1). f = 1 - exp(-t/(k t_orb)); TDG lower bound (CFG763 code), raw SPARC upper bound.
V_N, V_law and their errors: CFG441's (code copied). Ages at -1 sigma for the bound (floored at 0.05 Gyr).
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  python3 cfg764.py      (CFG764_MUTATE=1: V_obs := V_law; exit 1 iff k_min hits the grid floor and O1 opens)
"""
import os, sys, math, csv, json

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG4_common as C4  # noqa: E402  (read only)

MUT = os.environ.get("CFG764_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg764{TAG}.out"), "w")
RES = {"lane": "CFG764", "criteria": "9990bf4b1", "mutate": MUT, "numbers": {}}
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

sys.path.insert(0, os.path.join(CFG, "CFG760_p_wave_gap"))
import CFG691_copy as SP  # noqa: E402  (raw SPARC loader, checked in CFG760 K5)

# ------------------------------------------------------------------ upper bound: raw SPARC last points
torb = []
for gi in range(SP.NG):
    j = SP.last[gi]
    if SP.Vo[j] <= 0:
        continue
    torb.append(2 * math.pi * SP.Rm[j] / (SP.Vo[j] * 1e3) / 3.15576e16)
torb = np.array(torb)
kmax_all = 8.0 / (math.log(10) * torb)
KMAX = float(kmax_all.min())
P_(f"\nSPARC: {torb.size} galaxies; t_orb,last median {np.median(torb):.2f} Gyr, max {torb.max():.2f} Gyr;  k_max = {KMAX:.3f} "
   f"(5th pct {np.percentile(kmax_all, 5):.3f}, median {np.median(kmax_all):.3f})")
RES["numbers"]["SPARC"] = dict(n=int(torb.size), torb_median=float(np.median(torb)), torb_max=float(torb.max()), k_max=KMAX,
                               k_max_p5=float(np.percentile(kmax_all, 5)), k_max_median=float(np.median(kmax_all)))

KS = 10 ** np.round(np.arange(-2, 2.0001, 0.01), 2)
c441 = json.load(open(os.path.join(CFG, "CFG441_old_tdgs_tidal_origin", "cfg441_old_tdgs_results.json")))["numbers"]["tierB"]["out"]
k1, opens = True, {}
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
    ages = [max(o["t"] - o["et"], 0.05) for o in OBJ]

    def chi2(k):
        tot = 0.0
        for o, (vn, en, vl, el), v, t in zip(OBJ, pre, vobs, ages):
            fr = 1.0 if k == 0 else (0.0 if math.isinf(k) else 1 - math.exp(-t / (k * o["t_orb"])))
            vm = math.sqrt(vn ** 2 + fr * (vl ** 2 - vn ** 2))
            em = en + fr * (el - en)
            tot += (v - vm) ** 2 / (o["eV"] ** 2 + em ** 2)
        return tot

    cl, cn = chi2(0.0), chi2(math.inf)
    if not MUT:
        k1 &= abs(cl - c441[fo]["chi2_law"]) <= 0.01 and abs(cn - c441[fo]["chi2_N"]) <= 0.01
    ch = np.array([chi2(k) for k in KS])
    cmin = min(ch.min(), cn)
    ok = np.where(ch <= cmin + 3.84)[0]
    kmin = float(KS[ok[0]]) if ok.size else None
    op = kmin is not None and kmin <= KMAX
    opens[fo] = op
    fmed = 1 - math.exp(-8.0 / (kmin * float(np.median(torb)))) if kmin else None
    RES["numbers"][fo] = dict(k_min95=kmin, chi2_min=float(cmin), K1=(cl, cn), O1="OPEN" if op else "CLOSED",
                              f_median_sparc_at_kmin=fmed, n_sparc_excluded_at_kmin=int((kmax_all < kmin).sum()) if kmin else None)
    P_(f"{fo}: K1 chi2 k->0 {cl:.3f} (CFG441 {c441[fo]['chi2_law']:.3f}), k->inf {cn:.3f};  k_min,95 = {kmin} vs k_max = {KMAX:.3f}"
       f" -> O1 {'OPEN' if op else 'CLOSED'};  SPARC galaxies excluded at k_min: {RES['numbers'][fo]['n_sparc_excluded_at_kmin']}/"
       f"{torb.size};  f(last point, median galaxy, 8 Gyr) at k_min = {fmed:.3f}")
P_(f"K1 {'PASS' if k1 else 'FAIL'}")
RES["K1"] = bool(k1)
if MUT:
    bite = all(RES["numbers"][fo]["k_min95"] is not None and RES["numbers"][fo]["k_min95"] <= 0.01 and opens[fo] for fo in C4.FOOTS)
    P_(f"MUTATE bites: {bite}")
    rc = 1 if bite else 0
else:
    v = "OPEN" if all(opens.values()) else "CLOSED"
    RES["verdict"] = dict(O1=v)
    P_(f"VERDICT: O1 {v}")
    rc = 0
json.dump(RES, open(os.path.join(HERE, f"cfg764_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(rc)
