#!/usr/bin/env python3
"""
U4L1 -- a secondary, no-verdict reading of the 2026-11-06 ALMA upper limit on U4_27928 against the gas
requirement computed before the release (AC1 Part A). Criteria: FROZEN_CRITERIA.md (04f671aa84) with AMENDMENT_A1.md (KA2 re-specified after run 1 stopped there).
Usage: python3 u4l1.py      Writes u4l1.out, u4l1_results.json, u4l1_mut.out next to this file.
The governing plan (CFG806, A-U6) forms no Delta_m on a non-detection; nothing here changes that.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, json, math, hashlib, subprocess, collections
import numpy as np
from scipy.special import i0, i1, k0, k1
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
REQ = os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions", "ac1_results.json")
SHA = "bfdfed6806020ce61586c084006a43f04a2efe33e366aef229886ecd1da042d9"

# ---------------------------------------------------------------- constants (SI) and inputs fixed before the release
G, MSUN, KPC, C = 6.674e-11, 1.989e30, 3.0857e19, 2.99792458e8
Z, LOGMS, RE_ARCSEC = 1.41933, 10.74, 0.49
S_LIM, R21 = 0.511, 0.77                       # Jy km/s (3 sigma), CO(2-1)/CO(1-0)
ALPHA = collections.OrderedDict([("4.36", 4.36), ("1.0", 1.0)])
A0 = collections.OrderedDict([("canon 9.36e-11", 9.3603e-11), ("alt 1.13e-10", 1.1312e-10)])
W0, WA, OM = -0.838, -0.62, 0.315
def r_desi(z): a = 1 / (1 + z); return math.sqrt(a ** (-3 * (1 + W0 + WA)) * math.exp(-3 * WA * (1 - a)))
def r_H(z): return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
def r_fb(z): return float(np.interp(z, [0, 1, 2, 2.5], [1.0, 1.20, 2.82, 4.88]))
MODELS = collections.OrderedDict([("F-DESI", r_desi), ("F-flat", lambda z: 1.0), ("R-H", r_H), ("L-fb(RAR-eq)", r_fb)])
FRAME, RIVAL = ("F-flat", "F-DESI"), ("R-H", "L-fb(RAR-eq)")
TOL = 0.30                                     # twice the plan's 0.15 dex systematic floor

OUT = open(os.path.join(HERE, "u4l1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 112); say(t); say("=" * 112)
FAILS = []
def ka(name, ok, detail=""):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         ({detail})" if detail else ""))
    if not ok: FAILS.append(name)

# ---------------------------------------------------------------- geometry and the limit (independent, SI)
H0 = 70.0e3 / 3.0857e22
DC = C / H0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, Z)[0]        # m
DA, DL = DC / (1 + Z), DC * (1 + Z)
RE = RE_ARCSEC / 206264.806 * DA / KPC                                                 # kpc
R, RD = 2 * RE, RE / 1.678
NU_OBS = 230.538 / (1 + Z)                                                             # GHz
LPRIME21 = 3.25e7 * S_LIM * NU_OBS ** -2 * (DL / 3.0857e22) ** 2 * (1 + Z) ** -3       # K km/s pc^2
LIM = {k: math.log10(a * LPRIME21 / R21) for k, a in ALPHA.items()}

def frac(Rg): x = R / Rg; return 1 - (1 + x) * math.exp(-x)

# ---------------------------------------------------------------- independent requirement (closed-form kernels)
def Bf(y): return y * y * (i0(y) * k0(y) - i1(y) * k1(y))
def gb_closed(g, a0, kern):
    if kern == "n=1": return g * g / (g + a0)                       # mu(x) = x/(1+x)
    if kern == "n=2": return (-a0 + math.sqrt(a0 * a0 + 4 * g * g)) / 2   # g^2 = gb^2 + a0 gb
    raise ValueError(kern)
G_SEALED = 4.30091e-6 * 1e6 * KPC / MSUN        # the sealed code's G (kpc (km/s)^2 / Msun) in SI; amendment A1
def req_own(Vc_kms, a0, kern, Rg_kpc, Gc=G):
    Rm, Rdm, Rgm = R * KPC, RD * KPC, Rg_kpc * KPC
    g = (Vc_kms * 1e3) ** 2 / Rm
    vb2 = gb_closed(g, a0, kern) * Rm
    vs2 = 2 * Gc * 10 ** LOGMS * MSUN / Rdm * Bf(Rm / (2 * Rdm))
    vg2 = vb2 - vs2
    return None if vg2 <= 0 else math.log10(vg2 * Rgm / (2 * Gc * Bf(Rm / (2 * Rgm))) / MSUN)

# ====================================================================================================
sec("U4L1  the ALMA upper limit on U4_27928 against the pre-release gas requirement   (criteria 04f671aa84)")
say("     Secondary reading, no verdict weight. The governing plan scores nothing on a non-detection.")
say(f"     R = 2 R_e = {R:.3f} kpc, R_d = {RD:.4f} kpc, D_A = {DA/3.0857e22:.1f} Mpc, D_L = {DL/3.0857e22:.1f} Mpc")

sec("KNOWN-ANSWER CHECKS")
ka("KA1 the limit recomputed in SI from 0.511 Jy km/s (10.88 and 10.24, each within 0.03 dex)",
   abs(LIM["4.36"] - 10.88) <= 0.03 and abs(LIM["1.0"] - 10.24) <= 0.03,
   f"L'(2-1) = {LPRIME21:.3e} K km/s pc^2; log M_gas < {LIM['4.36']:.3f} (alpha 4.36), < {LIM['1.0']:.3f} (alpha 1.0)")
D = json.load(open(REQ))["A"]
wa, wb, wlow, nf, cells = 0.0, 0.0, 0.0, 0, 0
for case, Vc in D["cases"].items():
    for kern in ("n=1", "n=2"):
        for fn, a00 in A0.items():
            for mn in FRAME:
                v = D["req"][case][kern][f"{fn}|{mn}"]["logMgas_Rg=Rd"]
                oa = req_own(Vc, a00 * MODELS[mn](Z), kern, RD, G_SEALED); ob = req_own(Vc, a00 * MODELS[mn](Z), kern, RD, G)
                cells += 1
                if (oa is None) != (v is None) or (ob is None) != (v is None): nf += 1
                elif v is not None:
                    wa = max(wa, abs(oa - v))
                    if v >= 9.5: wb = max(wb, abs(ob - v))
                    else: wlow = max(wlow, abs(ob - v))
ka("KA2a (amendment A1) implementation: the independent routine with the sealed code's G, framework cells, n = 1 and n = 2, R_g = R_d",
   wa <= 1e-6 and nf == 0, f"largest difference {wa:.1e} dex over {cells} cells; FLOOR flags differing: {nf}")
ka("KA2b (amendment A1) constants: the same with standard SI constants, cells with a requirement >= 9.5 within 0.01 dex",
   wb <= 0.01, f"largest difference {wb:.4f} dex; cells below 9.5 (printed, not graded): largest {wlow:.4f} dex")
sha = hashlib.sha256(open(REQ, "rb").read()).hexdigest()
try:
    first = subprocess.run(["git", "-C", ROOT, "log", "--diff-filter=A", "--format=%aI", "--", os.path.relpath(REQ, ROOT)],
                           capture_output=True, text=True).stdout.split()[-1]
except Exception:
    first = "unknown"
ka("KA3 provenance: sha256 as frozen; first commit before the release (2026-11-06 02:42 UTC)",
   sha == SHA and first[:10] < "2026-11-06", f"sha256 {sha[:16]}...; first commit {first}")
num = quad(lambda r: r * math.exp(-r / RD), 0, R)[0] / RD ** 2
ka("KA4 aperture fraction: closed form equals the integral to 1e-6; 0.849 +- 0.002 at R_g = R_d",
   abs(num - frac(RD)) < 1e-6 and abs(frac(RD) - 0.849) <= 0.002, f"f(R_d) = {frac(RD):.4f}, f(1.5 R_d) = {frac(1.5*RD):.4f}")
if FAILS:
    say("\nSTOPPED: known-answer check failed -> no label formed.")
    json.dump({"lane": "U4L1", "label": "NO LABEL (stopped at " + FAILS[0].split()[0] + ")"}, open(os.path.join(HERE, "u4l1_results.json"), "w"), indent=1)
    sys.exit(0)

# ---------------------------------------------------------------- labels
def lab(d):
    return "ALLOWED" if d >= 0 else ("MARGINAL" if d >= -TOL else "IN TENSION")
def cell(case, kern, fn, mn, gs, alpha_key, shift=0.0):
    c = D["req"][case][kern][f"{fn}|{mn}"]; v = c[f"logMgas_{gs}"]
    if v is None: return dict(req=None, label="FLOOR (not tested)", fragile=False)
    Rg = RD if gs == "Rg=Rd" else 1.5 * RD
    L = LIM[alpha_key] + shift
    dm, dp = L - (v + math.log10(frac(Rg))), L - v
    return dict(req=v, d_matched=dm, d_printed=dp, label=lab(dm), label_printed=lab(dp), fragile=lab(dm) != lab(dp))
GRID = [(case, kern, fn, mn, gs) for case in D["cases"] for kern in ("n=1", "nu_mono", "n=2") for fn in A0 for mn in MODELS for gs in ("Rg=Rd", "Rg=1.5Rd")]

MUT = open(os.path.join(HERE, "u4l1_mut.out"), "w")
MUT.write("U4L1 mutations (criteria 04f671aa84). Each must bite.\n")
bite = True
for ak in ALPHA:
    up = [cell(*g, ak, +1.0) for g in GRID]; dn = [cell(*g, ak, -1.0) for g in GRID if not g[0].startswith("a ")]
    b1 = not any(c["label"] == "IN TENSION" for c in up)
    b2 = all(c["label"] in ("IN TENSION", "FLOOR (not tested)") for c in dn)
    MUT.write(f"alpha {ak}: M1 limit +1 dex -> cells IN TENSION: {sum(c['label']=='IN TENSION' for c in up)} [{'bites' if b1 else 'DOES NOT BITE'}];  "
              f"M2 limit -1 dex -> non-FLOOR cells at b, c, d not IN TENSION: {sum(c['label'] not in ('IN TENSION','FLOOR (not tested)') for c in dn)} [{'bites' if b2 else 'DOES NOT BITE'}]\n")
    bite &= b1 and b2
MUT.close()
sec("MUTATIONS")
say(f"  written to u4l1_mut.out: {'both bite' if bite else 'AT LEAST ONE DOES NOT BITE'}")

sec("PRIMARY CELLS  kernel n = 1, R_g = R_d.  D = log limit - log requirement (matched = requirement inside the aperture)")
say(f"  limits: log M_gas < {LIM['4.36']:.2f} (alpha_CO 4.36), < {LIM['1.0']:.2f} (alpha_CO 1.0); aperture fraction {frac(RD):.3f} ({math.log10(frac(RD)):+.3f} dex)")
RES = {"cells": {}}
for case, Vc in D["cases"].items():
    say(f"\n  case {case}: V_c = {Vc:.1f} km/s")
    say("     footing          model          requirement   alpha 4.36: D_matched D_printed  label                 alpha 1.0: D_matched D_printed  label")
    for fn in A0:
        for mn in MODELS:
            row = f"     {fn:15s}  {mn:13s}"
            c4 = cell(case, "n=1", fn, mn, "Rg=Rd", "4.36"); c1 = cell(case, "n=1", fn, mn, "Rg=Rd", "1.0")
            if c4["req"] is None:
                row += "  FLOOR         (not tested by a non-detection)"
            else:
                row += f"  {c4['req']:6.2f}        "
                for c in (c4, c1):
                    row += f"        {c['d_matched']:+5.2f}    {c['d_printed']:+5.2f}    {(c['label'] + (', FRAGILE' if c['fragile'] else '')):22s}"
            say(row)
            RES["cells"][f"{case}|{fn}|{mn}"] = {"4.36": c4, "1.0": c1}

sec("ALL CELLS  counts over the three kernels and two gas scales (non-FLOOR cells only)")
RES["counts"] = {}
for ak in ALPHA:
    say(f"\n  alpha_CO {ak}:   case         framework (F-flat, F-DESI)                      rivals (R-H, L-fb)")
    for case in D["cases"]:
        out = []
        for grp in (FRAME, RIVAL):
            cs = [cell(case, kern, fn, mn, gs, ak) for kern in ("n=1", "nu_mono", "n=2") for fn in A0 for mn in grp for gs in ("Rg=Rd", "Rg=1.5Rd")]
            cnt = collections.Counter(c["label"] for c in cs); fr = sum(c["fragile"] for c in cs)
            out.append(f"allowed {cnt['ALLOWED']:2d}, marginal {cnt['MARGINAL']:2d}, in tension {cnt['IN TENSION']:2d}, floor {cnt['FLOOR (not tested)']:2d} (fragile {fr})")
            RES["counts"][f"{ak}|{case}|{'framework' if grp is FRAME else 'rivals'}"] = dict(cnt)
        say(f"     {case:13s} {out[0]:52s} {out[1]}")

sec("LANE LABEL  framework cells at the primary kernel and gas scale, both footings")
def prim(case, ak): return [cell(case, "n=1", fn, mn, "Rg=Rd", ak) for fn in A0 for mn in FRAME]
def rivals(case, ak): return [c for c in (cell(case, "n=1", fn, mn, "Rg=Rd", ak) for fn in A0 for mn in RIVAL) if c["req"] is not None]
c436 = prim("c P-B", "4.36"); a436 = prim("a P0", "4.36")
all_tension_c = all(c["label"] == "IN TENSION" for c in c436)
none_tension = not any(x in ("IN TENSION",) for c in c436 + a436 for x in (c["label"], c.get("label_printed", c["label"])))
if all_tension_c: LABEL = "TENSION AT THE PLAN'S PRIMARY BRANCH"
elif none_tension: LABEL = "NO TENSION"
else: LABEL = "CONDITIONAL"
say(f"  alpha 4.36, case c (the plan's primary pressure branch): " + ", ".join(c["label"] + ("*" if c["fragile"] else "") for c in c436))
say(f"  alpha 4.36, case a (the plan's branch, no pressure term): " + ", ".join(c["label"] + ("*" if c["fragile"] else "") for c in a436))
say("  (* = the as-printed reading gives a different label)")
say("\n  where tension appears, by case and conversion (primary cells; framework | rivals that are not FLOOR):")
RES["by_branch"] = {}
for ak in ALPHA:
    for case in D["cases"]:
        f_ = [c["label"] for c in prim(case, ak)]; r_ = [c["label"] for c in rivals(case, ak)]
        nd = bool(r_) and set(r_) == set(f_)
        RES["by_branch"][f"{ak}|{case}"] = dict(framework=f_, rivals=r_, not_discriminating=nd)
        say(f"     alpha {ak:4s} {case:13s}: {', '.join(f_):52s} | {', '.join(r_) if r_ else 'all FLOOR'}" + ("   NOT DISCRIMINATING" if nd else ""))
say(f"\n  LANE LABEL: {LABEL}")

sec("REPORTED, NOT GRADED")
emp = D["empirical_logMgas"]
say(f"  scaling-relation gas mass {emp:.2f}: against the limits (matched) " + ", ".join(f"alpha {ak}: D = {LIM[ak] - (emp + math.log10(frac(RD))):+.2f} ({lab(LIM[ak] - (emp + math.log10(frac(RD))))})" for ak in ALPHA))
say("  for each primary framework cell: the conversion factor at which the limit equals the requirement inside the aperture,")
say("  and the unseen (atomic or CO-dark) gas that would lift it to ALLOWED at alpha_CO 4.36 and 1.0 [1e10 Msun]:")
RES["reported"] = {}
for case in D["cases"]:
    for fn in A0:
        for mn in FRAME:
            c = D["req"][case]["n=1"][f"{fn}|{mn}"]["logMgas_Rg=Rd"]
            if c is None: continue
            inside = c + math.log10(frac(RD))
            aeq = 10 ** inside / (LPRIME21 / R21)
            need = {ak: max(0.0, 10 ** inside - 10 ** LIM[ak]) / 1e10 for ak in ALPHA}
            RES["reported"][f"{case}|{fn}|{mn}"] = dict(alpha_equal=aeq, unseen_1e10=need)
            say(f"     {case:13s} {fn:15s} {mn:7s}: alpha_CO = {aeq:5.2f};  unseen gas {need['4.36']:5.2f} / {need['1.0']:5.2f}")
RES.update(lane="U4L1", criteria="04f671aa84", date="2026-11-12", label=LABEL, limits=LIM, R_kpc=R, Rd_kpc=RD, aperture_fraction=frac(RD))
json.dump(RES, open(os.path.join(HERE, "u4l1_results.json"), "w"), indent=1, default=str)
say("\nU4L1 COMPLETE. Secondary reading; no verdict weight. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
