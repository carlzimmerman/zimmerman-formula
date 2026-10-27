"""CFG407: is X43's heavy-cluster outer excess real mass? X43's predicted total M(<r) (route E: M_b + M_h) vs X-COP hydrostatic M_FORW
over [R500, R200] for the 12 X-COP clusters on disk. Criteria: FROZEN_CRITERIA.md (65226042e3).
Run:  nice python3 cfg407_xcop_outer.py           -> cfg407.out, cfg407_results.json
      MUTATE=1 nice python3 cfg407_xcop_outer.py  -> predictions paired in reversed M500 order (scatter must at least double; rc 1)
Single thread. kappa = 1/2 FITTED; not theory closed."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math, json, time, io, contextlib, numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
REB = os.path.join(REPO, "rebuild_2026_10_22"); X43SRC = os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py")
XC = os.path.join(REPO, "real_research", "data", "xcop")
MUT = os.environ.get("MUTATE") == "1"; os.environ.pop("MUTATE", None)
OUT, CONTROLS = [], []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def K(name, ok, val): CONTROLS.append({"name": name, "pass": bool(ok), "value": val}); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")
T0 = time.time()

# =============================================================== X43 up to its final per-footing loop (read-only; X30 log redirected here)
src = open(X43SRC).read()
o = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'; assert src.count(o) == 1
src = src.replace(o, f'HERE = {HERE!r}; REB = {REB!r}')
cut = "\nfor f in FEET:\n"; assert src.count(cut) == 1
G = {"__file__": X43SRC, "__name__": "x43_cfg407"}; argv0 = sys.argv; sys.argv = [X43SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(cut)], X43SRC, "exec"), G)
sys.argv = argv0
NX = G["NX"]; sig_core, solve_r0, B, MSUNE, grade_clusters = (G[k] for k in ("sig_core", "solve_r0", "B", "MSUNE", "grade_clusters"))
gas, r_ta_com, RG, RM, MSUN, DM, DA_lcdm, HV, prep = (NX[k] for k in ("gas", "r_ta_com", "RG", "RM", "MSUN", "DM", "DA_lcdm", "HV", "prep"))
EPS, BGS = G["EPS"], G["BGS"]
FEET, HKS = ("canonical", "alt"), ("h0672", "h0686")
P("CFG407 X-COP hydrostatic mass vs X43's route-E total mass over [R500, R200]" + ("  [MUTATE: reversed M500 pairing]" if MUT else ""))
P("=" * 110); P(f"X43 machinery exec'd read-only up to its final loop [{time.time() - T0:.0f} s]; eta {G['ETA']:.4f}, c_f 4 EXTERNAL")

def mh_total(Mb, rta, Mfair, foot, tag):
    """X43's in-loop rule (grade_clusters): Sigma = sig_core(M_fair + M_bt), r0 = solve_r0(M_fair, r_ta, Sigma), M_h = pi Sigma r0^2 B(min(r, r_ta)/r0)."""
    Mtot = (Mfair + float(Mb[-1])) / MSUNE
    s, _ = sig_core(foot, tag, Mtot)
    r0 = solve_r0(Mfair, rta, s)
    return math.pi * s * r0 ** 2 * B(np.minimum(RM, rta) / r0)

# =============================================================== controls K1, K2
P("\nCONTROLS")
REF = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
gc = grade_clusters("canonical")
k1d = max(abs(gc["cells"]["h0672"][k]["pred"] - REF["footings"]["canonical"]["clusters"]["cells"]["h0672"][k]["pred"]) for k in ("G-OUT-M3", "G-OUT-all"))
K("K1 X43 machinery live: grade_clusters('canonical') reproduces committed h0672 pred of G-OUT-M3 and G-OUT-all (<= 1e-9)", k1d <= 1e-9,
  f"max |diff| {k1d:.1e} (G-OUT-M3 pred {gc['cells']['h0672']['G-OUT-M3']['pred']:.4f})")
k2d = 0.0
for i in (0, NX["N"] // 2, NX["N"] - 1):
    pp = prep(int(i), "canonical", "h0672"); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE
    s, _ = sig_core("canonical", "A_c2b_refit", Mtot, True); r0 = solve_r0(pp["Mfair"], pp["rta"], s)
    ref = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)
    mine = mh_total(pp["Mb"], pp["rta"], pp["Mfair"], "canonical", "A_c2b_refit")
    k2d = max(k2d, float(np.max(np.abs(mine / np.where(ref > 0, ref, 1) - 1) * (ref > 0))))
K("K2 rule identity: single-cluster M_h equals X43's in-loop expression for 3 eRASS1 clusters (<= 1e-12 rel)", k2d <= 1e-12, f"max rel {k2d:.1e}")

# =============================================================== X-COP inputs
J5 = json.load(open(os.path.join(XC, "xcop_r500_ettori2019.json")))
NAMES = sorted(n for n in J5 if os.path.isdir(os.path.join(XC, n)))
def lli(x, xp, fp): return float(np.exp(np.interp(math.log(x), np.log(xp), np.log(fp))))
XD = {}
for n in NAMES:
    hm = fits.open(os.path.join(XC, n, f"{n}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(XC, n, f"{n}_fgas_profile.fits"))[1].data
    ms = fits.open(os.path.join(XC, n, f"{n}_mstar.fits"))[2].data
    XD[n] = dict(z=J5[n]["z"], R500=J5[n]["R500"], R200=J5[n]["R200"], M500=J5[n]["M500"],
                 r_h=np.array(hm["RADIUS"], float) / 1e3, M_f=np.array(hm["M_FORW"], float), eM_f=np.array(hm["EM_FORW"], float), M_nfw_h=np.array(hm["M_NFW"], float),
                 x_g=np.array(fg["RADIUS"], float), M_g=np.array(fg["MGAS"], float), M_nfw_g=np.array(fg["M_NFW"], float),
                 r_s=np.array(ms["RADIUS"], float) / 1e3, M_s=np.array(ms["MSTAR"], float))
P(f"  X-COP clusters with profile files: {len(NAMES)} ({', '.join(NAMES)}); in table without files: {sorted(set(J5) - set(NAMES))}")
k3 = {n: lli(1.0, d["x_g"], d["M_nfw_g"]) / lli(d["R500"], d["r_h"], d["M_nfw_h"]) - 1 for n, d in XD.items()}
K("K3 units: fgas M_NFW at R/R500 = 1 vs hydro M_NFW at JSON R500 within 1.5% (all 12; CFG450 U2)", all(abs(v) <= 0.015 for v in k3.values()),
  f"max |dev| {max(abs(v) for v in k3.values()):.4f}")
cov = {n: float(d["x_g"].max() / (d["R200"] / d["R500"])) for n, d in XD.items()}
short = [n for n, c in cov.items() if c < 0.95]
K("K4 coverage: MGAS reaches >= 0.95 R200 (short clusters reported and kept, never dropped)", True,
  "all reach" if not short else "short (extrapolated gas flagged): " + ", ".join(f"{n} {cov[n]:.2f}" for n in short))

# native background (L1 / CFG886) and K5
L1 = dict(Om=0.2976016, h=0.6856427, wb=0.0223081); OBn = L1["wb"] / L1["h"] ** 2; RATIO_N = (L1["Om"] - OBn) / OBn
G946, MPC946 = 6.67430e-11, 3.0856775814913673e22
RHOMn = L1["Om"] * 3 * (L1["h"] * 100e3 / MPC946) ** 2 / (8 * math.pi * G946)
def r_ta_nat(Mb_kg): return (3 * (L1["Om"] / OBn) * Mb_kg / (4 * math.pi * NX["DTA"] * RHOMn)) ** (1 / 3)
hB = BGS["B_cfg886_bg"]["h"]; OmB = EPS["B_cfg886_bg"]["rhom0"] / (2.775e11 * EPS["B_cfg886_bg"]["h"] ** 2)
k5 = abs(hB - L1["h"]) <= 1e-4 and abs(OmB - L1["Om"]) <= 1e-4
K("K5 background identity (V-NAT): B_cfg886_bg h and Omega_m equal L1's to 1e-4", k5, f"h {hB:.7f} vs {L1['h']}, Om {OmB:.7f} vs {L1['Om']}")
TAGN = "B_cfg886_bg" if k5 else "A_c2b_refit"
P(f"  native Omega_c/Omega_b = {RATIO_N:.4f} (criteria 5.2715); V-NAT collapse table: {TAGN}")

# =============================================================== predictions
def baryons(n, hk, recipe):
    d = XD[n]; z = d["z"]; q = (float(DM(z, HV[hk])) / (1 + z)) / DA_lcdm(z)
    R500 = d["R500"] * q; Mg500 = lli(1.0, d["x_g"], d["M_g"]) * q ** 2.5
    Mg, rho_g = gas(Mg500, R500, "P")                                                   # kg on RG (Mpc), "P" shape, cut at 3 Mpc
    if recipe == "X43":
        return Mg * 1.20, q
    # V-MEAS: measured gas to its last point, continued with the "P" density shape matched there; measured stars, continued with gas
    rg = d["x_g"] * d["R500"] * q; mg = d["M_g"] * q ** 2.5 * MSUN; rl = rg[-1]
    Mgm = np.where(RG <= rl, np.exp(np.interp(np.log(RG), np.log(rg), np.log(mg), left=-np.inf)), 0.0)
    Mgm[RG < rg[0]] = mg[0] * (RG[RG < rg[0]] / rg[0]) ** 3
    rho_l = (mg[-1] - mg[-2]) / (4 * math.pi * (rl * MPC946) ** 2 * (rg[-1] - rg[-2]) * MPC946)
    sh = rho_g / float(np.interp(rl, RG, rho_g)) * rho_l; out = RG > rl
    dm = 4 * math.pi * (RG * MPC946) ** 2 * sh; cum = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RG * MPC946))]
    Mgm[out] = mg[-1] + (cum[out] - float(np.interp(rl, RG, cum)))
    rs = d["r_s"] * q; msv = d["M_s"] * q ** 2 * MSUN; sl = rs[-1]
    Ms = np.exp(np.interp(np.log(RG), np.log(rs), np.log(msv)))
    Ms[RG < rs[0]] = msv[0] * (RG[RG < rs[0]] / rs[0]) ** 3
    Ms[RG > sl] = msv[-1] * Mgm[RG > sl] / float(np.interp(sl, RG, Mgm))
    return Mgm + Ms, q
def predict(n, foot, hk, variant):
    Mb, q = baryons(n, hk, "MEAS" if variant == "V-MEAS" else "X43"); z = XD[n]["z"]; Mbt = float(Mb[-1])
    if variant == "V-NAT":
        rta, Mfair, tag = r_ta_nat(Mbt) / (1 + z), RATIO_N * Mbt, TAGN
    else:
        rta, Mfair, tag = r_ta_com(Mbt) / (1 + z), 5.364 * Mbt, "A_c2b_refit"
    return (Mb + mh_total(Mb, rta, Mfair, foot, tag)) / MSUN, q                           # Msun on RG

def radii(n, q, lo=1.0, hi=None):
    d = XD[n]; R5 = d["R500"] * q; top = (d["R200"] / d["R500"]) if hi is None else hi
    return R5 * top ** (np.arange(5) / 4) if hi is None else R5 * np.exp(np.linspace(math.log(lo), math.log(hi), 5))
def deltas(variant, b, pair=None, inner=False):
    """Delta_i per cluster (mean over the 5 radii) for each footing x h cell; pair maps HSE cluster -> prediction cluster (MUTATE)."""
    res = {}
    for foot in FEET:
        for hk in HKS:
            Di, rows, chi = [], {}, 0.0
            for n in NAMES:
                pn = n if pair is None else pair[n]
                Mx, _ = predict(pn, foot, hk, variant); d = XD[n]; z = d["z"]; q = (float(DM(z, HV[hk])) / (1 + z)) / DA_lcdm(z)
                rk = radii(n, q, 0.3, 0.7) if inner else radii(n, q)
                Mh = np.array([lli(r / q, d["r_h"], d["M_f"]) * q for r in rk]); eh = np.array([lli(r / q, d["r_h"], d["eM_f"]) * q for r in rk])
                Mp = np.exp(np.interp(np.log(rk), np.log(RG), np.log(Mx)))
                dk = np.log10(Mh / (1 - b) / Mp); Di.append(float(dk.mean())); rows[n] = dict(dk=dk.tolist(), q=q, R200_over_R500=d["R200"] / d["R500"])
                chi += float(np.sum((np.log10(Mh / Mp) / (eh / Mh / math.log(10))) ** 2))
            Di = np.array(Di); mean, se = float(Di.mean()), float(Di.std(ddof=1) / math.sqrt(len(Di)))
            res[f"{foot}|{hk}"] = dict(mean=mean, se=se, Z=mean / se, rms=float(Di.std(ddof=1)), Di=dict(zip(NAMES, Di.tolist())), rows=rows, chi2_b0=chi)
    return res

if MUT:
    order = sorted(NAMES, key=lambda n: XD[n]["M500"]); pair = dict(zip(order, order[::-1]))
    base, mut = deltas("PRIMARY", 0.0), deltas("PRIMARY", 0.0, pair)
    ok = all(mut[c]["rms"] >= 2 * base[c]["rms"] for c in base)
    K("MUTATE reversed-M500 pairing: rms of Delta_i at least doubles in every cell", ok, {c: (round(base[c]["rms"], 3), round(mut[c]["rms"], 3)) for c in base})
    json.dump({"lane": "CFG407", "mutate": True, "controls": CONTROLS, "base": base, "mutated": mut}, open(os.path.join(HERE, "cfg407_results_MUTATE.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg407_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1)

R = {}
for var in ("PRIMARY", "V-NAT", "V-MEAS"):
    R[var] = {b: deltas(var, b) for b in (0.0, 0.3)}
R["V-INNER"] = {0.0: deltas("PRIMARY", 0.0, inner=True)}

def classify(rv):
    cls = {}
    for c in rv[0.0]:
        m0, s0 = rv[0.0][c]["mean"], rv[0.0][c]["se"]; m3, s3 = rv[0.3][c]["mean"], rv[0.3][c]["se"]
        cls[c] = "EXCESS CONFIRMED" if m0 >= 2 * s0 else ("X43 OVERPREDICTS" if m3 <= -2 * s3 else "CONSISTENT")
    u = set(cls.values()); return (u.pop() if len(u) == 1 else "MIXED"), cls
P("\nRESULTS (Delta = log10[M_HSE/(1-b)/M_X43], mean over [R500, R200]; se = cluster scatter / sqrt(12))")
SUMM = {}
for var in ("PRIMARY", "V-NAT", "V-MEAS"):
    overall, cls = classify(R[var]); SUMM[var] = dict(overall=overall, cells=cls)
    P(f"  {var}: {overall}")
    for c in R[var][0.0]:
        a, b3 = R[var][0.0][c], R[var][0.3][c]; bstar = 1 - 10 ** a["mean"] if a["mean"] < 0 else None
        P(f"    {c:16s} b=0: {a['mean']:+.3f} +- {a['se']:.3f} (Z {a['Z']:+.2f}, rms {a['rms']:.3f}) | b=0.3: {b3['mean']:+.3f} +- {b3['se']:.3f} -> {cls[c]}"
          + (f" | b* {bstar:.3f}" if bstar is not None else "") + f" | chi2(b=0) {a['chi2_b0']:.0f}/60")
P("  per cluster Delta_i (PRIMARY, canonical|h0672, b = 0): " + ", ".join(f"{n} {v:+.3f}" for n, v in R["PRIMARY"][0.0]["canonical|h0672"]["Di"].items()))
P("  Delta at R200 alone (PRIMARY, canonical|h0672, b = 0): " + ", ".join(f"{n} {R['PRIMARY'][0.0]['canonical|h0672']['rows'][n]['dk'][-1]:+.3f}" for n in NAMES))
vi = R["V-INNER"][0.0]["canonical|h0672"]; P(f"  V-INNER (0.3-0.7 R500, reported): canonical|h0672 {vi['mean']:+.3f} +- {vi['se']:.3f}")
P(f"  KiDS link (reported, not graded): X43 short by +0.087 dex in projected Delta Sigma at 1.42-3 Mpc (G-OUT-M3); X-COP PRIMARY b=0 canonical|h0672 {R['PRIMARY'][0.0]['canonical|h0672']['mean']:+.3f} dex in 3-D M(<r)")
flips = [v for v in ("V-NAT", "V-MEAS") if SUMM[v]["overall"] != SUMM["PRIMARY"]["overall"]]
valid = all(c["pass"] for c in CONTROLS)
reading = "INVALID (a control failed)" if not valid else SUMM["PRIMARY"]["overall"]
P(f"\nREADING (frozen, PRIMARY): {reading}" + (f"   [class changes in: {', '.join(flips)}]" if flips else "   [no variant changes the class]"))
P(f"controls {sum(c['pass'] for c in CONTROLS)}/{len(CONTROLS)}; runtime {time.time() - T0:.0f} s")
json.dump({"lane": "CFG407", "mutate": False, "controls": CONTROLS, "reading": reading, "summary": SUMM, "flips": flips,
           "results": {v: {str(b): r for b, r in rv.items()} for v, rv in R.items()}, "native_ratio": RATIO_N, "native_tag": TAGN, "coverage": cov},
          open(os.path.join(HERE, "cfg407_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg407.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if valid else 2)
