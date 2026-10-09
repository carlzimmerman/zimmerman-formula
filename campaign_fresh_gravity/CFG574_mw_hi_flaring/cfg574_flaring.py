"""CFG574: Milky Way HI flaring, round rule (RM) vs phantom disc (PD). Criteria: FROZEN_CRITERIA.md (0371938fe).

Re-uses CFG516's committed definitions by execution (CFG514 solver, McMillan17 baryons, RM-phi, RM-v, PD, homeoid).
Data: Kalberla & Dedes 2008 (arXiv:0804.4831) HWHM h(R) = 0.15 exp((R - 8.5)/9.8) kpc, 5 <~ R <~ 35 kpc.
MUTATE: CFG574_MUTATE=1 puts RM-phi's cold mass in a q = 0.3 homeoid; outputs carry the _MUTATE tag.
"""
import os, sys, json, math
import numpy as np
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
SRC516 = os.path.join(HERE, "..", "CFG516_round_cold_energy", "cfg516_mw.py")
src = open(SRC516).read()
head = src.split("# ------------------------------------------------------------------ controls")[0]
ns516 = {"__file__": os.path.abspath(SRC516)}
_stdout = sys.stdout
sys.stdout = open(os.devnull, "w")                     # CFG516's banner is not part of this lane's output
exec(compile(head, "cfg516_head", "exec"), ns516)
sys.stdout = _stdout
g = ns516
GR, Base, FieldModel, build_PD = g["GR"], g["Base"], g["FieldModel"], g["build_PD"]
Mcold_phi, Mcold_v, homeoid_field = g["Mcold_phi"], g["Mcold_v"], g["homeoid_field"]
rho_mcm, R0_MODEL, A0, ns514 = g["rho_mcm"], g["R0"], g["A0"], g["ns"]
S0_HI = ns514["S0_HI"]

MUTATE = os.environ.get("CFG574_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(cond, msg):
    CHECKS.append((bool(cond), msg)); P(f"  [{'PASS' if cond else 'FAIL'}] {msg}"); return bool(cond)


# ------------------------------------------------------------------ data
R_SUN_KD, H0_KD, RF_KD = 8.5, 0.15, 9.8
SECH2_HWHM = 2 * math.acosh(math.sqrt(2.0))           # HWHM of sech^2(z/(2 zh)) in units of zh  (= 1.7627)


def h_obs(R):
    return H0_KD * np.exp((np.asarray(R, float) - R_SUN_KD) / RF_KD)


RSC = np.arange(10.0, 30.0 + 1e-9, 1.0)                 # scoring radii (frozen)
HOBS = h_obs(RSC)


# ------------------------------------------------------------------ baryons: McMillan17 with the HI layer at the observed flaring
def hi_fixed(R, z):
    Rs = np.maximum(R, 1e-6)
    return (S0_HI * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(np.abs(z) / (2 * 0.085)) ** 2


def hi_flared(R, z):
    Rs = np.maximum(R, 1e-6)
    zh = h_obs(Rs) / SECH2_HWHM
    return (S0_HI * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * zh)) / np.cosh(np.abs(z) / (2 * zh)) ** 2


def rho_obsHI(R, z):
    return rho_mcm(R, z) - hi_fixed(R, z) + hi_flared(R, z)


# ------------------------------------------------------------------ hydrostatic HWHM
ZG = np.linspace(0.0, 20.0, 8001)


def hwhm_from_rho(z, rho):
    half = 0.5 * rho[0]
    i = np.argmax(rho < half)
    if i == 0:
        return np.nan
    return float(z[i - 1] + (half - rho[i - 1]) * (z[i] - z[i - 1]) / (rho[i] - rho[i - 1]))


def phiz_table(model, R):
    Kz = np.abs(model.Kz(np.full_like(ZG, R), ZG))
    return np.concatenate([[0.0], np.cumsum(0.5 * (Kz[1:] + Kz[:-1]) * np.diff(ZG))])   # (km/s)^2


def hwhm(phiz, sigma):
    return hwhm_from_rho(ZG, np.exp(-phiz / sigma ** 2))


def score(model):
    tabs = [phiz_table(model, R) for R in RSC]

    def cost(s):
        h = np.array([hwhm(t, s) for t in tabs])
        return np.sum(np.log(h / HOBS) ** 2) if np.all(np.isfinite(h)) else 1e9
    res = minimize_scalar(cost, bounds=(1.0, 80.0), method="bounded", options=dict(xatol=1e-4))
    s = float(res.x)
    h = np.array([hwhm(t, s) for t in tabs])
    rms = float(np.sqrt(np.mean(np.log(h / HOBS) ** 2)))
    slope = np.polyfit(RSC, np.log(h), 1)[0]
    R0m = float(1.0 / slope) if slope > 0 else float("inf")
    ok = rms <= 0.15 and 7.8 <= R0m <= 11.8
    return dict(sigma=s, rms_ln=rms, R0=R0m, consistent=bool(ok), h=h.tolist(),
                sigma_flag=("" if 5.0 <= s <= 15.0 else "IMPLAUSIBLE"))


# ------------------------------------------------------------------ run
P("=" * 100)
P(f"CFG574  Milky Way HI flaring: RM vs PD  {'*** MUTATE: RM-phi cold mass in a q=0.3 homeoid ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
P(f"data: Kalberla & Dedes 2008 HWHM = {H0_KD} exp((R-{R_SUN_KD})/{RF_KD}) kpc; scored R = 10-30 kpc; model R0 = {R0_MODEL} kpc")

P("\n--- controls")
zt = np.linspace(0, 3, 30001); zh = 0.2
check(abs(hwhm_from_rho(zt, np.cosh(zt / (2 * zh)) ** -2) / (SECH2_HWHM * zh) - 1) < 0.01,
      f"C3 HWHM extractor recovers a sech^2 HWHM ({SECH2_HWHM * zh:.4f} kpc) to 1%")
b_fix = Base("B1_McMillan17", rho_mcm)
check(abs(b_fix.Mb / 6.64e10 - 1) < 0.02, f"C1 B1 (fixed 85 pc HI) grid baryon mass {b_fix.Mb:.4e} matches CFG514's 6.64e10 to 2%")
b_obs = Base("B1_obsHI", rho_obsHI)
P(f"     B1 with the observed-flaring HI layer: grid baryon mass {b_obs.Mb:.4e} (same surface densities; thicker gas)")

results = {}
for bname, base in (("primary_obsHI", b_obs), ("variant_fixedHI", b_fix)):
    results[bname] = {}
    for foot in ("canonical", "alt"):
        Mphi, _ = Mcold_phi(base, 1.0, foot)
        models = {
            "RM-phi": FieldModel(base, 1.0, Mcold=Mphi),
            "RM-v": FieldModel(base, 1.0, Mcold=Mcold_v(base, 1.0, foot)),
            "PD": build_PD(base, 1.0, foot)[0],
            "Newton(C2)": FieldModel(base, 1.0),
        }
        if MUTATE:
            fh, _, _, _ = homeoid_field(Mphi, q=0.3)
            models["RM-phi"] = FieldModel(base, 1.0, Mcold=fh)
        P(f"\n--- {bname}  footing {foot} (a0 = {A0[foot]:.3e})")
        P(f"    {'model':11s} {'sigma':>7s} {'rms_ln':>7s} {'R0':>7s}  consistent  h(10,15,20,25,30) kpc   [obs {', '.join(f'{x:.2f}' for x in HOBS[::5])}]")
        res = {}
        for mn, m in models.items():
            r = score(m); res[mn] = r
            hs = ", ".join(f"{x:.2f}" for x in np.array(r["h"])[::5])
            P(f"    {mn:11s} {r['sigma']:7.2f} {r['rms_ln']:7.3f} {r['R0']:7.2f}  {str(r['consistent']):10s}  [{hs}] {r['sigma_flag']}")
        if bname == "primary_obsHI":
            n = res["Newton(C2)"]
            check(not n["consistent"] or n["sigma_flag"] == "IMPLAUSIBLE",
                  f"C2 [{foot}] Newtonian baryons alone are not a plausible match (rms {n['rms_ln']:.3f}, R0 {n['R0']:.2f}, sigma {n['sigma']:.1f})")
        rmok = res["RM-phi"]["consistent"] and res["RM-v"]["consistent"]
        pdok = res["PD"]["consistent"]
        call = ("ROUND FAVOURED" if rmok and not pdok else "PD FAVOURED" if pdok and not (res["RM-phi"]["consistent"] or res["RM-v"]["consistent"])
                else "NOT DIAGNOSTIC")
        res["call"] = call
        P(f"    call: {call}")
        results[bname][foot] = res

prim = results["primary_obsHI"]
overall = prim["canonical"]["call"] if prim["canonical"]["call"] == prim["alt"]["call"] else "SPLIT"
P(f"\nVERDICT (primary, both footings): {overall}")
if MUTATE:
    P("MUTATE reading: compare RM-phi here with the PRIMARY output's RM-phi (frozen: must not be consistent where RM-phi was).")

# post-freeze disclosed variant: rescale KD08 kinematic distances to the model's R0 (R and h scale with R_sun)
P(f"\nDISCLOSED post-freeze variant (not a gate): KD08 distances rescaled by R0/8.5 = {R0_MODEL / R_SUN_KD:.4f}")
sc = R0_MODEL / R_SUN_KD
HOBS_sav = HOBS.copy()
HOBS = h_obs(RSC / sc) * sc
for foot in ("canonical", "alt"):
    Mphi, _ = Mcold_phi(b_obs, 1.0, foot)
    for mn, m in (("RM-phi", FieldModel(b_obs, 1.0, Mcold=Mphi)), ("PD", build_PD(b_obs, 1.0, foot)[0])):
        r = score(m)
        P(f"    [{foot}] {mn:7s} sigma {r['sigma']:6.2f}  rms_ln {r['rms_ln']:.3f}  R0 {r['R0']:.2f}  consistent {r['consistent']}")
HOBS = HOBS_sav

P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(results=results, verdict=overall, checks=CHECKS), open(os.path.join(HERE, f"cfg574_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg574_flaring{TAG}.out"), "w").write("\n".join(OUT) + "\n")
