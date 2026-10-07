#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG441 -- OLD TIDAL DWARF GALAXIES SELECTED BY TIDAL ORIGIN: Newtonian (settling) or boosted (the law)?

Frozen rules: FROZEN_CRITERIA.md (committed alone first, 6f2023e4c). kappa = 1/2 FITTED; both a0 footings; no dark-matter
particle (the framework's cold-fluid mass is still required wherever the law needs it).

  Tier A (verdict sample): S0 tidal origin + S1 age >= 1 Gyr + S2 kinematic quality + S3 >= 1 orbit at the measured radius.
  Tier B (reported): S0 + S2 but fails S1 or S3 (the CFG7 young six; Arp 72c).
  Tier C (reported): collision debris (DF2/DF4), quoted from the committed CFG7 FG001 record only.
  Statistic: chi^2 of V_obs vs Newton and vs the law (nu_mono, 1-D EFE form of CFG7 / FM12 eq. 60, nominal host mass;
  isolated if no host); Delta chi^2 = chi^2_law - chi^2_N.  SETTLING SUPPORTED if Delta > +9 on both footings; LAW
  SUPPORTED if Delta < -9 on both; else NON-DISCRIMINATING (also if N_A < 3).
  C1: CFG7's young-TDG Newton chi^2 1.09 (6) within 0.01, and its nu_mono most-favourable-host chi^2_EFE (10.55 / 13.08)
      within 0.05.   C2: the nu_mono import.
  MUTATE=1: V_obs := V_N on the analysis set (Tier A if N_A >= 3, else Tier A + B); must return SETTLING SUPPORTED on both
  footings -> exit 1.
  F1 (forecast, not a measurement): NGC 5557-E1, the oldest secure TDG (4 Gyr), has no usable kinematics; the velocity
  that Newton and the law predict for it, bracketing its untabulated gas mass, and the velocity precision needed.
Run: python3 campaign_fresh_gravity/CFG441_old_tdgs_tidal_origin/cfg441_old_tdgs.py   (MUTATE=1 for the control; ~3 s)
"""
import os, sys, math, csv, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG4_common as C4                                                                # committed nu_mono, A0 footings

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "cfg441_old_tdgs" + ("_MUTATE" if MUTATE else "")
LINES, CHECKS, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LINES.append(s)


def check(name, detail, ok, load_bearing=True):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")


def banner(s):
    P("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110)


P(__doc__.split("Run:")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: V_obs replaced by the Newtonian prediction -- the verdict must be SETTLING SUPPORTED (exit 1) ***")

G_KPC = 4.30091727e-6                                                                   # kpc (km/s)^2 / Msun
KPC_M = 3.0856775814913673e19
ACC = 1e6 / KPC_M                                                                       # (km/s)^2/kpc -> m/s^2
FOOTS = C4.FOOTS
A0 = C4.A0
NU = C4.nu_mono
THR = 9.0

# ================================================================================================ C2 kernel import
banner("C2  CONTROL: the committed nu_mono and the two footings")
n1 = float(NU(1.0)); deep = float(NU(1e-4) * math.sqrt(1e-4))
P(f"    nu_mono(1) = {n1:.12f}; nu_mono(1e-4) * sqrt(1e-4) = {deep:.5f}; a0 = {A0['canonical']:.5e} / {A0['alt']:.5e} m/s^2")
check("C2 CONTROL: nu_mono imported from CFG4_common (deep limit nu sqrt(y) within 2% of 1 at y = 1e-4); footings 9.3603e-11 / "
      "1.1312e-10", f"deep-limit ratio {deep:.4f}", abs(deep - 1) < 0.02 and abs(A0['canonical'] - 9.3603e-11) < 1e-15
      and abs(A0['alt'] - 1.1312e-10) < 1e-15)


# ================================================================================================ the model
def v_newton(M, R):
    return math.sqrt(G_KPC * M / R)


def v_law(M, R, a0, Mhost=None, Dp=None):
    """CFG7's eq. 4 (FM12 eq. 60): a_i = gNi nu((gNi+gNe)/a0) + gNe[nu((gNi+gNe)/a0) - nu(gNe/a0)]; isolated if no host."""
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


def chi2(objs, model, a0=None, host_fac=1.0, vkey="V", extra=0.0):
    tot, per = 0.0, []
    for o in objs:
        if model == "N":
            fn = lambda M, R: v_newton(M, R)
        elif model == "iso" or o.get("Mhost") is None:
            fn = lambda M, R: v_law(M, R, a0)
        else:
            fn = lambda M, R, o=o: v_law(M, R, a0, o["Mhost"] * host_fac, o["Dp"])
        v, e = pred_err(fn, o["M"], o["eM"], o["R"], o["eR"])
        c = (o[vkey] - v) ** 2 / (o["eV"] ** 2 + e ** 2 + (extra * o[vkey]) ** 2)
        tot += c; per.append(dict(obj=o["name"], v_obs=o[vkey], v_pred=v, e_pred=e, chi2=c))
    return tot, per


# ================================================================================================ data
L15 = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv"))))
young = []
for r in L15:
    f = lambda k: float(r[k])
    young.append(dict(name=r["object"], tier="B", V=f("V_circ_kms"), eV=f("e_V_circ_kms"), M=f("M_bar_1e8") * 1e8,
                      eM=f("e_M_bar_1e8") * 1e8, R=f("R_out_kpc"), eR=f("e_R_out_kpc"), Mhost=0.6 * f("host_LK_1e10Lsun") * 1e10,
                      Dp=f("D_p_kpc"), t_form=f("tmerg_over_torb") * f("t_orb_Gyr"), t_orb=f("t_orb_Gyr")))
arp = []
for r in csv.DictReader(open(os.path.join(HERE, "data", "tierB_arp72c.csv"))):
    f = lambda k: float(r[k])
    V, R = f("V_circ_kms"), f("R_out_kpc")
    arp.append(dict(name=r["object"], tier="B", V=V, eV=0.5 * (f("e_V_circ_up") + f("e_V_circ_lo")), M=f("M_bar_1e8") * 1e8,
                    eM=f("e_M_bar_1e8") * 1e8, R=R, eR=f("e_R_out_kpc"), Mhost=None, Dp=None, t_form=f("age_Myr") / 1e3,
                    t_orb=2 * math.pi * R * KPC_M / 1e3 / (V) / 3.15576e16))
cand = list(csv.DictReader(open(os.path.join(HERE, "data", "candidates.csv"))))

# ================================================================================================ selection
banner("SELECTION  (frozen S0-S3; every candidate and its reason in data/candidates.csv)")
for c in cand:
    P(f"    {c['object'][:44]:44s} tier {c['tier']:9s} | S0 {c['S0_tidal_origin'][:4]:4s} S1 {c['S1_age_ge_1Gyr'][:4]:4s} "
      f"S2 {c['S2_kinematics'][:4]:4s} S3 {c['S3_ge_1_orbit'][:4]:4s} | {c['reason'][:60]}")
for o in young + arp:
    P(f"    S3 audit {o['name']:11s}: t_form {o['t_form']:.2f} Gyr, t_orb {o['t_orb']:.2f} Gyr -> {o['t_form'] / o['t_orb']:.2f} orbits")
TIER_A = []                                                                                # no candidate passes S0-S3
TIER_B = young + arp
NA = len(TIER_A)
P(f"\n    Tier A (verdict sample): N_A = {NA}.  Tier B (reported): {len(TIER_B)} ({', '.join(o['name'] for o in TIER_B)}).")
P("    Tier C (reported, from the committed CFG7 FG001 record): NGC 1052-DF2 Newton 0.0 sigma, law+EFE 3.0 sigma; DF4 0.8 / 1.5 sigma.")
NUM["N_A"] = NA; NUM["tier_B"] = [o["name"] for o in TIER_B]
check("S3 audit: every Tier B object has turned < 1 orbit (so none could be promoted to Tier A by S3)",
      ", ".join(f"{o['name']} {o['t_form'] / o['t_orb']:.2f}" for o in TIER_B), all(o["t_form"] / o["t_orb"] < 1 for o in TIER_B),
      load_bearing=False)

# ================================================================================================ C1 CFG7 reproduction
banner("C1  CONTROL: CFG7 FG041's young-TDG chi^2 with this lane's code")
if not MUTATE:
    cN, _ = chi2(young, "N")
    best = {}
    for ft in FOOTS:
        tot = 0.0
        for h in sorted(set(r["host"] for r in L15)):
            sub = [o for o, r in zip(young, L15) if r["host"] == h]
            tot += min(chi2(sub, "efe", A0[ft], fac)[0] for fac in (0.5, 1.0, 2.0))
        best[ft] = tot
    ref = json.load(open(os.path.join(CFG, "CFG7_tdg_fg041_results.json")))["numbers"]["H2"]
    P(f"    Newton chi^2 = {cN:.4f} (CFG7 1.0950); nu_mono+EFE most favourable host: canonical {best['canonical']:.3f} "
      f"(CFG7 {ref['canonical|nu_mono']['chi_efe']:.3f}), alt {best['alt']:.3f} (CFG7 {ref['alt|nu_mono']['chi_efe']:.3f})")
    ok = abs(cN - 1.09) <= 0.01 and all(abs(best[f] - ref[f"{f}|nu_mono"]["chi_efe"]) <= 0.05 for f in FOOTS)
    check("C1 CONTROL: CFG7 Newton chi^2 1.09 (6 TDGs) within 0.01 and nu_mono+EFE (canonical 10.55 / alt 13.08) within 0.05",
          f"Newton {cN:.4f}; EFE {best['canonical']:.3f} / {best['alt']:.3f}", ok)
    NUM["C1"] = dict(chi2_newton=cN, chi2_efe_best=best)
else:
    P("    (skipped under MUTATE; the main run carries it)")


# ================================================================================================ verdict machinery
def verdict(objs, vkey):
    out = {}
    for ft in FOOTS:
        cN, pN = chi2(objs, "N", vkey=vkey)
        cL, pL = chi2(objs, "efe", A0[ft], 1.0, vkey=vkey)
        cI, _ = chi2(objs, "iso", A0[ft], vkey=vkey)
        rob = {fac: chi2(objs, "efe", A0[ft], fac, vkey=vkey)[0] - chi2(objs, "N", vkey=vkey)[0] for fac in (0.5, 2.0)}
        sysd = chi2(objs, "efe", A0[ft], 1.0, vkey=vkey, extra=0.1)[0] - chi2(objs, "N", vkey=vkey, extra=0.1)[0]
        out[ft] = dict(chi2_N=cN, chi2_law=cL, chi2_iso=cI, d=cL - cN, d_fac=rob, d_sys10=sysd, per_N=pN, per_law=pL)
    ds = [out[f]["d"] for f in FOOTS]
    v = "SETTLING SUPPORTED" if all(d > THR for d in ds) else ("LAW SUPPORTED" if all(d < -THR for d in ds) else "NON-DISCRIMINATING")
    return v, out


def show(out, label):
    for ft in FOOTS:
        o = out[ft]
        P(f"    {label} {ft:9s}: chi^2 Newton {o['chi2_N']:7.2f} | law+EFE (nominal host) {o['chi2_law']:7.2f} | law isolated "
          f"{o['chi2_iso']:7.2f} | Delta (law+EFE - N) {o['d']:+7.2f}; host x0.5 {o['d_fac'][0.5]:+.2f}, x2 {o['d_fac'][2.0]:+.2f}; "
          f"10% sys {o['d_sys10']:+.2f}")
        P("        per object (V_obs / Newton / law): " + "; ".join(
            f"{a['obj']} {a['v_obs']:.0f}/{a['v_pred']:.0f}/{b['v_pred']:.0f}" for a, b in zip(o["per_N"], o["per_law"])))


# ================================================================================================ the verdict
banner("VERDICT ON TIER A (old TDGs by tidal origin)")
analysis = TIER_A if NA >= 3 else TIER_A + TIER_B
for o in analysis:
    o["V_mut"] = v_newton(o["M"], o["R"])
if not MUTATE:
    if NA < 3:
        V_A = "NON-DISCRIMINATING"
        P(f"    N_A = {NA} < 3: NON-DISCRIMINATING by the frozen rule, on both footings (no Tier A chi^2 exists).")
    else:
        V_A, outA = verdict(TIER_A, "V"); show(outA, "TierA"); NUM["tierA"] = outA
    NUM["verdict"] = {f: V_A for f in FOOTS}
    banner("REPORTED (never a verdict): Tier B -- tidal origin + kinematics, but young / < 1 orbit")
    vB, outB = verdict(TIER_B, "V"); show(outB, "TierB")
    P(f"    Tier B would read '{vB}' under the Tier A thresholds -- reported only (it fails S1/S3 by construction).")
    NUM["tierB"] = dict(would_read=vB, out=outB)
else:
    vM, outM = verdict(analysis, "V_mut"); show(outM, "MUTATE")
    P(f"    MUTATE analysis set ({'Tier A' if NA >= 3 else 'Tier A + Tier B, N rule suspended'}; N = {len(analysis)}): {vM}")
    NUM["mutate"] = dict(verdict=vM, out=outM)
    check("MUTATE: V_obs := V_Newton must be read as SETTLING SUPPORTED on both footings (expected; exit 1 when detected)",
          f"{vM}; Delta canonical {outM['canonical']['d']:+.2f}, alt {outM['alt']['d']:+.2f}", vM != "SETTLING SUPPORTED")

# ================================================================================================ F1 forecast
banner("F1  FORECAST (not a measurement): NGC 5557-E1, 4 Gyr old, no usable kinematics -- what would decide it")
D = 38.8                                                                                    # Mpc (Duc+2014 Table 1; ATLAS3D)
ra_e1, de_e1 = (14 + 18 / 60 + 55.9 / 3600) * 15, 36 + 28 / 60 + 57 / 3600
ses = open(os.path.join(HERE, "fetched", "sesame_ngc5557.txt")).read().split("%J ")[1].split()
ra_h, de_h = float(ses[0]), float(ses[1])
sep = math.degrees(math.acos(math.sin(math.radians(de_e1)) * math.sin(math.radians(de_h)) + math.cos(math.radians(de_e1)) *
                             math.cos(math.radians(de_h)) * math.cos(math.radians(ra_e1 - ra_h))))
Dp = sep * math.pi / 180 * D * 1e3
MK = None
for line in open(os.path.join(HERE, "fetched", "atlas3d_ngc5557.tsv")):
    if "NGC5557" in line and not line.startswith("#"):
        MK = float(line.split("\t")[10])
LK = 10 ** (-0.4 * (MK - 3.28)); Mhost = 0.6 * LK
Mstar, Re = 1.2e8, 2.3
R = 2 * Re
P(f"    E1-host projected distance {Dp:.1f} kpc ({sep * 3600:.0f} arcsec at {D} Mpc); host M_K {MK} -> L_K {LK:.3e}, M_host = 0.6 L_K "
  f"= {Mhost:.3e} Msun; E1 M_* = 1.2e8, R_e = 2.3 kpc, evaluated at R = 2 R_e = {R:.1f} kpc")
F1 = []
for fg in (1.0, 3.0):
    M = Mstar * (1 + 1.4 * fg)
    vN = v_newton(M, R)
    row = dict(M_HI_over_Mstar=fg, M_bar=M, v_N=vN)
    for ft in FOOTS:
        row[f"v_law_efe_{ft}"] = v_law(M, R, A0[ft], Mhost, Dp); row[f"v_law_iso_{ft}"] = v_law(M, R, A0[ft])
    F1.append(row)
    P(f"    M_HI = {fg:.0f} x M_* -> M_bar {M:.2e}: V_Newton {vN:5.1f} km/s; law+EFE {row['v_law_efe_canonical']:5.1f} / "
      f"{row['v_law_efe_alt']:5.1f}; law isolated {row['v_law_iso_canonical']:5.1f} / {row['v_law_iso_alt']:5.1f} km/s (canonical / alt)")
gap = min(min(r[f"v_law_efe_{f}"] for f in FOOTS) - r["v_N"] for r in F1)
P(f"    smallest Newton-to-law+EFE gap {gap:.1f} km/s: a 3-sigma split for this one object needs a total velocity error <= {gap / 3:.1f} km/s "
  "(V_circ incl. asymmetric drift, inclination and baryonic-mass errors) -- resolved HI (VLA/MeerKAT-class, ~5 km/s channels) or "
  "IFU H-alpha kinematics, plus a measured HI mass.")
NUM["F1"] = dict(Dp_kpc=Dp, M_host=Mhost, rows=F1, min_gap_kms=gap)

# ================================================================================================ write
lb = [c for c in CHECKS if c["load_bearing"]]
nf = sum(not c["ok"] for c in lb)
P(f"\n  {sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {nf}")
if not MUTATE:
    P(f"  VERDICT (Tier A, both footings): {NUM['verdict']['canonical']} / {NUM['verdict']['alt']}  (N_A = {NA})")


def jclean(x):
    if isinstance(x, dict):
        return {str(k): jclean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jclean(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    return x


json.dump(jclean(dict(slug=SLUG, checks=CHECKS, numbers=NUM, load_bearing_failures=nf)),
          open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LINES) + "\n")
sys.exit(1 if nf else 0)
