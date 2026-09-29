#!/usr/bin/env python3
"""CFG142 -- does the dust continuum exclude the gas CFG141's P2 model needs? The KURVS-CDFS discs inside GOODS-ALMA 1.1 mm.

Frozen criteria: CFG142_FROZEN_CRITERIA.md (ae867cd1d), committed before the data chat's cross-match (b25d5c902, README fix fef5d64ed).
Data: data_assembly/goodsalma_crossmatch/ (placement on the mosaic, catalogue matches, the survey's stated frequency and thresholds).

  conversion  Scoville et al. 2016 eqs. A4/A8 (alpha_850 = 6.7e19), T_d = 25 K, nu_obs = the survey's stated 265.0 GHz, Planck18 d_L.
  S_req,gen   the 1.1-mm flux at mu_total = 4 at the generous end: gas-to-dust x 2 (mu_dust = 2) and M* 0.2 dex below MAGPHYS.
  covered     inside the mosaic under both of the data chat's orientation readings; edge-flagged if within 0.5' of the edge.
  detected    a catalogue source within 0.6".  not detected: the limit is N_det x rms, N_det = 4.4 (the paper's blind 100%-purity
              threshold in the combined map), rms = the survey average 68.4 uJy/beam (APPROXIMATE: no local rms is available).
  powered     S_req,gen > N_det x rms (a point source; the extended-source sensitivity is a reported row).
  H1          no scored disc excludes the requirement; FAIL needs >= 2 excluding discs as the majority; < 2 scored -> NON-DIAGNOSTIC.
MUTATE=1: every scored disc's flux set to S_req,gen with its measured error -> no scored disc may exclude.
MUTATE=2: every scored disc a detection of zero flux with its error / 10 -> every scored disc must exclude (sample verdict only if >= 2).
Each MUTATE run exits 0 when it behaves as required. kappa = 1/2 and Omega_c h^2 stay fitted.
Run: python3 campaign_fresh_gravity/CFG142_goodsalma_gas_test.py   (MUTATE=1 or MUTATE=2 for the pinned controls)
"""
import os, sys, io, csv, math, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import CFG7_common as C

MODE = os.environ.get("MUTATE", "").strip()
assert MODE in ("", "1", "2"), "MUTATE must be unset, 1 or 2"
R = C.Report("CFG142_goodsalma_gas_test" + (f"_MUTATE{MODE}" if MODE else ""), False)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MODE:
    P(f"\n  *** MUTATE={MODE}: pinned control ({'flux = S_req,gen' if MODE == '1' else 'zero-flux detection, error / 10'}) ***")

# ------------------------------------------------------------------ the conversion (identical to CFG142_requirement_fluxes.py)
h_, k_, c_ = 6.62607015e-34, 1.380649e-23, 2.99792458e8
NU850 = c_ / 850e-6
H0, OM = 67.66, 0.30966


def d_l_gpc(z, n=20000):
    s = sum(1.0 / math.sqrt(OM * (1 + z * (i + 0.5) / n) ** 3 + 1 - OM) for i in range(n)) * z / n
    return (1 + z) * c_ / 1e3 / H0 * s / 1e3


def gam(nu, z, td):
    x = h_ * nu * (1 + z) / (k_ * td)
    return x / math.expm1(x)


def mism_per_mjy(z, nu_obs, td=25.0):
    """Msun of ISM per mJy of observed flux (Scoville et al. 2016 eq. A8 with alpha_850 = 6.7e19)."""
    return 1.78 * (1 + z) ** -4.8 * (NU850 / nu_obs) ** 3.8 * (gam(NU850, 0, td) / gam(nu_obs, z, td)) * d_l_gpc(z) ** 2 * 1e10


def s_req(z, lm, nu_obs, generous=True, td=25.0):
    if generous:
        return 2 * 10 ** (lm - 0.2) / mism_per_mjy(z, nu_obs, td)      # mu_dust = 2 at M* - 0.2 dex
    return 4 * 10 ** lm / mism_per_mjy(z, nu_obs, td)                   # mu_dust = 4 at nominal M*


# ------------------------------------------------------------------ inputs
POS = {r["kurvs_id"]: r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "arxiv_tables", "kurvs_positions", "kurvs_positions.csv")))}
XM = {r["kurvs_id"]: r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "goodsalma_crossmatch", "kurvs_goodsalma_summary.csv")))}
TEN = ["3", "7", "8", "9", "11", "13", "15", "16", "17", "21"]
NU_OBS = 265.0e9            # the survey's stated tuning (data chat README: ALMA Band 6, 265.0 GHz, lambda = 1.13 mm)
RMS = 0.0684                # mJy/beam, the survey-average combined-map rms (APPROXIMATE for every position)
N_DET = 4.4                 # the paper's blind 100%-purity threshold in the combined map (sigma_p)
MATCH_ARCSEC = 0.6

# ------------------------------------------------------------------ C-0: the conversion reproduces the pre-data table at 272.5 GHz
pre = {"9": (0.249, 0.498), "11": (0.912, 1.824), "16": (0.273, 0.546), "3": (0.825, 1.650)}
dev0 = max(max(abs(s_req(float(POS[k]["z_halpha"]), float(POS[k]["logMstar"]), c_ / 1.1e-3, generous=True) * 10 ** 0.2 / v[0] - 1),
               abs(s_req(float(POS[k]["z_halpha"]), float(POS[k]["logMstar"]), c_ / 1.1e-3, generous=False) / v[1] - 1)) for k, v in pre.items())
check("C-0 CONTROL: the conversion reproduces CFG142's committed pre-data table at 272.5 GHz (S(mu_dust = 2) and S(mu_dust = 4), 3-digit print)",
      f"max relative deviation {dev0:.1e} over KURVS 3, 9, 11, 16", dev0 < 2.5e-3)

# ------------------------------------------------------------------ C1: CFG141's pipeline reproduces its committed per-disc P2 rows
F141 = os.path.join(HERE, "CFG141_kurvs_measured_sigma.py")
src = open(F141).read()
g141 = {"__file__": F141, "__name__": "cfg141"}
_saved = os.environ.pop("MUTATE", None)          # CFG141/CFG140 read the same variable: run their pipeline unmutated in every mode
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index("# ================================================================== C1 / C2")], "CFG141", "exec"), g141)
finally:
    if _saved is not None:
        os.environ["MUTATE"] = _saved
KU2, SP, score = g141["KU2"], g141["SP"], g141["score"]
out141 = open(os.path.join(HERE, "CFG141_kurvs_measured_sigma.out")).read()
ref = {}
for part in out141.split("R2 (reported) per galaxy (central cell, P2, unanchored)")[1].split("\n")[1].split(";"):
    part = part.strip()
    if ":" in part and "D_flat" in part:
        kid = part.split(":")[0].strip()
        ref[kid] = (float(part.split("D_flat ")[1].split(",")[0]), float(part.split("D_H ")[1].split(",")[0]))
_, Dk, _ = score(KU2, 0.67, 0.0, "P1", "canonical")
_, Dkh, _ = score(KU2, 0.67, 0.0, "P1", "canonical", rival=True)
mine = {o["name"].split("-")[1]: (round(float(d), 2), round(float(dh), 2)) for o, d, dh in zip(KU2, Dk, Dkh)}
c1ok = len(ref) == 10 and all(mine[k] == ref[k] for k in ref)
check("C1 CONTROL: CFG141's pipeline (exec'd read-only) reproduces its committed per-disc P2 D_flat and D_H at mu = 0.67 (2-decimal print)",
      f"{sum(mine[k] == ref[k] for k in ref)}/{len(ref)} discs match: " + ", ".join(f"{k}: {mine[k][0]:+.2f}/{mine[k][1]:+.2f}" for k in TEN), c1ok)


def disc_delta(kid, mu, foot="canonical"):
    o = next(q for q in KU2 if q["name"] == f"KURVS-{kid}")
    (d, _), _, _ = score([o], mu, 0.0, "P1", foot)
    (dh, _), _, _ = score([o], mu, 0.0, "P1", foot, rival=True)
    (af, _), _, _ = score(SP, mu, 0.0, "P1", foot, measured_gas=True)
    (ah, _), _, _ = score(SP, mu, 0.0, "P1", foot, measured_gas=True, rival=True)
    return d, dh, d - af, dh - ah


# ------------------------------------------------------------------ R1 per disc: placement, match, limit, powered
R.banner("R1  per disc (the ten rotation-supported KURVS discs)")
rows = {}
for k in TEN:
    x, p = XM[k], POS[k]
    z, lm = float(p["z_halpha"]), float(p["logMstar"])
    nom, env = x["footprint_nominal"], x["footprint_envelope"]
    covered = nom.startswith("inside") and env.startswith("inside")
    edge = "0.5'" in nom or "0.5'" in env
    sep = float(x["separation_arcsec"]) if x["separation_arcsec"] else float("nan")
    detected = np.isfinite(sep) and sep <= MATCH_ARCSEC
    sg, sn = s_req(z, lm, NU_OBS, True), s_req(z, lm, NU_OBS, False)
    lim = N_DET * RMS
    if detected:
        S, eS = float(x["S1p1mm_mJy"]), float(x["S1p1mm_err_mJy"])
    else:
        S, eS = float("nan"), RMS
    if MODE == "1":
        S, eS, detected_eff = sg, (eS if detected else RMS), True
    elif MODE == "2":
        S, eS, detected_eff = 0.0, (eS if detected else RMS) / 10.0, True
    else:
        detected_eff = detected
    powered = covered and (detected or sg > lim)
    scored = covered and powered
    if detected_eff:
        excludes = scored and (S + 2 * eS < sg)
    else:
        excludes = scored and (sg > lim)
    mu_max = (lim * mism_per_mjy(z, NU_OBS)) / 10 ** lm              # mu_dust upper limit at nominal calibration (5-sigma-type limit)
    rows[k] = dict(z=z, lm=lm, nominal=nom, envelope=env, covered=covered, edge=edge, sep=sep, detected=detected, S=S, eS=eS,
                   S_req_gen=sg, S_req_nom=sn, limit=lim, powered=powered, scored=scored, excludes=excludes, mu_dust_max=mu_max,
                   nearest_any=x["nearest_source_any_arcsec"])
    P(f"  KURVS-{k:>2s} z {z:.3f} logM* {lm:5.2f}  placement {nom:34s} / {env:34s}  covered {covered!s:5s} edge {edge!s:5s}  "
      f"match {'yes' if detected else 'none'} (nearest {x['nearest_source_any_arcsec']}\")  S_req,gen {sg:.3f} nom {sn:.3f} mJy  "
      f"limit {lim:.3f}  powered {powered!s:5s}  scored {scored!s:5s}  excludes {excludes!s:5s}  mu_dust,max(nominal) {mu_max:.2f}")
R.num("R1", rows)

scored = [k for k in TEN if rows[k]["scored"]]
excl = [k for k in scored if rows[k]["excludes"]]
if len(scored) < 2:
    verdict = "NON-DIAGNOSTIC for the sample (fewer than two scored discs); reported per disc"
elif not excl:
    verdict = "PASS (no scored disc excludes the requirement)"
elif len(excl) >= 2 and len(excl) > len(scored) / 2:
    verdict = "FAIL (the requirement is excluded in a majority of >= 2 scored discs)"
else:
    verdict = "MIXED"
R.num("H1", dict(scored=scored, excluding=excl, verdict=verdict, N_det=N_DET, rms=RMS, nu_obs=NU_OBS))

if MODE == "1":
    check("MUTATE=1 [pinned control]: with every scored disc's flux at S_req,gen, no scored disc excludes the requirement",
          f"scored {scored}; excluding {excl}; sample verdict {verdict}", len(scored) >= 1 and not excl)
elif MODE == "2":
    check("MUTATE=2 [pinned control]: with every scored disc a zero-flux detection (error / 10), every scored disc excludes the requirement",
          f"scored {scored}; excluding {excl}; sample verdict {verdict}"
          + ("" if len(scored) >= 2 else "  (the sample-level FAIL is not applicable with fewer than two scored discs, as frozen)"),
          len(scored) >= 1 and set(excl) == set(scored))
else:
    check("H1 [HEADLINE, reported verdict] the dust continuum does not exclude CFG141's P2 gas requirement in the scored covered discs",
          f"scored {scored}; excluding {excl}: {verdict}.  Every limit is APPROXIMATE (survey-average rms, point source).", True, load_bearing=False)

# ------------------------------------------------------------------ R2: CFG141's P2 Delta per scored disc at the gas bound
R.banner("R2  per scored disc: CFG141's P2 D_flat, D_H (unanchored; anchor-corrected) at mu_total = mu_dust,max x {1, 2}  (lower bounds)")
r2 = {}
for k in scored:
    mm = rows[k]["mu_dust_max"]
    vals = {}
    for fac in (1, 2):
        d, dh, dp, dhp = disc_delta(k, mm * fac)
        vals[fac] = dict(mu=mm * fac, D_flat=d, D_H=dh, Dp_flat=dp, Dp_H=dhp)
        P(f"  KURVS-{k}: mu_total = {mm * fac:.2f} (x{fac}): D_flat {d:+.3f}, D_H {dh:+.3f}; anchor-corrected {dp:+.3f}, {dhp:+.3f}")
    d4, dh4, dp4, dhp4 = disc_delta(k, 4.0)
    P(f"  KURVS-{k}: at the P2 requirement mu = 4 for comparison: D_flat {d4:+.3f}, D_H {dh4:+.3f}; anchor-corrected {dp4:+.3f}, {dhp4:+.3f}")
    r2[k] = vals
R.num("R2", r2)

# ------------------------------------------------------------------ R3 and variants (reported): T_d, thresholds, extended sources, context
R.banner("R3 and declared variants (reported only)")
r3 = {}
for k in TEN:
    z, lm = rows[k]["z"], rows[k]["lm"]
    r3[k] = dict(S_req_gen_35K=s_req(z, lm, NU_OBS, True, 35.0), S_req_gen_272GHz=s_req(z, lm, c_ / 1.1e-3, True))
P("  T_d = 35 K, S_req,gen (mJy): " + ", ".join(f"{k}: {r3[k]['S_req_gen_35K']:.3f}" for k in TEN))
var = {}
for name, lim in (("N_det 4.4 (primary)", 4.4 * RMS), ("N_det 5.2 (high-res)", 5.2 * RMS), ("N_det 3.5 (prior-based)", 3.5 * RMS),
                  ("faintest blind-table flux 0.49 mJy", 0.49)):
    for fpt in (1.0, 0.5, 0.3):
        eff = lim / fpt
        pw = [k for k in TEN if rows[k]["covered"] and rows[k]["S_req_gen"] > eff]
        var[f"{name} | peak/total {fpt}"] = pw
        P(f"  limit {name:34s}, peak/total {fpt:.1f} (effective total-flux limit {eff:.3f} mJy): powered covered discs {pw}")
R.num("variants", var)
ctx = {}
for k in ("12", "22"):
    x, p = XM[k], POS[k]
    if x["separation_arcsec"] and float(x["separation_arcsec"]) <= MATCH_ARCSEC:
        z, lm, S = float(p["z_halpha"]), float(p["logMstar"]), float(x["S1p1mm_mJy"])
        mu = S * mism_per_mjy(z, NU_OBS) / 10 ** lm
        ctx[k] = dict(S=S, z=z, lm=lm, mu_dust_nominal=mu, mu_total_generous=2 * mu / 10 ** -0.2)
        P(f"  context (not in the ten, not scored): KURVS-{k} detected, {S:.2f} mJy, z {z:.3f}, logM* {lm:.2f}: mu_dust {mu:.2f} (nominal), "
          f"mu_total {2 * mu / 10 ** -0.2:.2f} at the generous end")
R.num("context", ctx)
P("  KURVS-15 note: a prior-based source (A2GS75, 0.69 mJy, catalogue z 1.618) lies 6.9\" away, outside the 0.6\" rule; not used.")

nf = R.write()
raise SystemExit(1 if nf else 0)
