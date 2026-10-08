#!/usr/bin/env python3
"""CFG431: is the settling clock's scatter universal across galaxy / group / cluster?  (criteria: FROZEN_CRITERIA.md, 26d94268c)

Leftover branch e = exp(-Gamma t):  sigma(e)/e = |ln e| sigma(ln t)  =>  S = sigma_e / (e_med |ln e_med|).
Samples (definition A, b = 0, as on disk): galaxy = cm08's 23 non-central SLUGGS early types (5 Re);
group = 20 Lovisari groups (cfg382_target_audit); cluster = 7 X-COP clusters (cfg382_target_audit).
Run: python3 cfg431_clock_universality.py   |   T431_MUTATE=1 injects a x4 (or x1/4) galaxy clock break.
Local data only; no network.
"""
import json, math, os, re, sys
import numpy as np
from astropy.io import fits

MUT = os.environ.get("T431_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
import CFG4_common as C4  # noqa: E402  (read-only: nu_mono, as the target audit uses)

NB, NMC, SEED = 4000, 2000, 431
COSMIC = 0.1200 / 0.02237          # cm08's cosmic cold share (5.364)
A0_CAN, A0_ALT = 9.3603e-11, 1.1312e-10
lines = []
def say(s=""):
    lines.append(s); print(s)

# ------------------------------------------------------------------ galaxies (cm08, exactly)
tex = open(os.path.join(EXT, "alabi2017", "src", "halov3.tex")).read()
num = lambda s: re.sub(r"[^0-9.\-]", "", s.split("^")[0].split("_")[0])
t1 = {}
for line in tex.split("\\begin{table*}")[1].split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 12 and re.match(r"^\$?\s*\d{3,4}", c[0]):
        try: t1[num(c[0])] = (float(num(c[9])), float(num(c[10])))
        except ValueError: pass
t2 = {}
for line in (tex.split("\\begin{table*}")[2] + tex.split("\\begin{table*}")[3]).split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 6 and re.match(r"^\$\s*\d{3,4}\s*\$", c[0]) and re.match(r"^\$\s*0\s*\$", c[1]):
        mt, emt = [float(v) for v in c[4].strip("$").split("\\pm")]
        fd, efd = [float(v) for v in c[5].strip("$").split("\\pm")]
        t2[num(c[0])] = (mt * 1e11, fd, emt * 1e11, efd)
CENTRALS = ("4486", "4472", "1399", "1316", "4374", "4649", "5846", "1407", "4636")
GAL = [n for n in sorted(set(t1) & set(t2)) if n not in CENTRALS]
Gsi, Msun, kpc = 6.674e-11, 1.989e30, 3.0857e19

def gal_e(a0, Mt=None, fd=None):
    out = []
    for i, n in enumerate(GAL):
        Re = t1[n][0]
        mt = t2[n][0] if Mt is None else Mt[i]
        f_ = t2[n][1] if fd is None else fd[i]
        Ms = max(1 - f_, 0.05) * mt
        y = Gsi * Ms * Msun / (5 * Re * kpc) ** 2 / a0
        out.append((mt - math.sqrt(1 + 1 / y) * Ms) / (COSMIC * Ms))
    return np.array(out)

# ------------------------------------------------------------------ groups + clusters (cfg382_target_audit, exactly)
Gcgs, MSUN, KPC = 6.674e-8, 1.989e33, 3.0857e21
A0CGS = 9.3603e-9
def defA(Mhse, Mb, b, Rk):
    gN = Gcgs * Mb * MSUN / (Rk * KPC) ** 2
    Mph = (C4.nu_mono(np.array([gN / A0CGS]))[0] - 1) * Mb
    return (Mhse / (1 - b) - Mb - Mph) / (5.364 * Mb)

rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")) if not l.startswith("#")]
hdr, rows = rows[0], [x for x in rows[1:] if len(x) > 5]
GRP = [dict(R=float(x[hdr.index("R500_kpc")]), M=float(x[hdr.index("M500_1e13")]) * 1e13, eM=float(x[hdr.index("eM500")]) * 1e13,
            Mg=float(x[hdr.index("Mgas500_1e12")]) * 1e12, eMg=float(x[hdr.index("eMgas500")]) * 1e12) for x in rows]
def grp_e(b, M=None, Mg=None):
    return np.array([defA(g["M"] if M is None else M[i], 1.10 * (g["Mg"] if Mg is None else Mg[i]), b, g["R"]) for i, g in enumerate(GRP)])

xdir = os.path.join(REPO, "real_research", "data", "xcop")
r5 = json.load(open(os.path.join(xdir, "xcop_r500_ettori2019.json")))
CL = []
for nm in sorted(os.listdir(xdir)):
    d = os.path.join(xdir, nm)
    if not os.path.isdir(d) or nm not in r5 or not os.path.exists(os.path.join(d, f"{nm}_mstar.fits")):
        continue
    hm = fits.open(os.path.join(d, f"{nm}_hydro_mass.fits"))["HYDRO_MASS"].data
    fg = fits.open(os.path.join(d, f"{nm}_fgas_profile.fits"))["FGAS"].data
    ms = fits.open(os.path.join(d, f"{nm}_mstar.fits"))["MSTAR_SMOOTHED"].data
    Rk = r5[nm]["R500"] * 1000
    lr, lmg = np.log(np.asarray(fg["RADIUS"], float)), np.log(np.asarray(fg["MGAS"], float))
    CL.append(dict(name=nm, R=Rk,
                   M=float(np.interp(Rk, np.asarray(hm["RADIUS"], float), np.asarray(hm["M_FORW"], float))),
                   eM=float(np.interp(Rk, np.asarray(hm["RADIUS"], float), np.asarray(hm["EM_FORW"], float))),
                   Mg1=float(np.exp(np.interp(0.0, lr, lmg))),                       # the audit's quirk: M_gas at 1 Mpc
                   MgR=float(np.exp(np.interp(math.log(Rk / 1000), lr, lmg))),       # R2: M_gas at R500
                   Ms=float(np.exp(np.interp(np.log(Rk), np.log(np.asarray(ms["RADIUS"], float)), np.log(np.asarray(ms["MSTAR"], float)))))))
def cl_e(b, gasR500=False, M=None):
    return np.array([defA(c["M"] if M is None else M[i], (c["MgR"] if gasR500 else c["Mg1"]) + c["Ms"], b, c["R"]) for i, c in enumerate(CL)])

# ------------------------------------------------------------------ estimator
def S_of(e):
    em = float(np.median(e)); se = (np.percentile(e, 84) - np.percentile(e, 16)) / 2
    if not (0 < em < 1):
        return math.inf, em, se
    return se / (em * abs(math.log(em))), em, se

def boot_dln(e, rng):
    lnS = []
    n = len(e)
    for _ in range(NB):
        s = S_of(e[rng.integers(0, n, n)])[0]
        lnS.append(math.log(s) if (math.isfinite(s) and s > 0) else math.inf)
    lnS = np.sort(np.array(lnS))
    p16, p84 = lnS[int(0.16 * NB)], lnS[int(0.84 * NB)]
    return (p84 - p16) / 2 if math.isfinite(p84) else math.inf, float(np.mean(~np.isfinite(lnS)))

def verdict(cls):
    """cls: {name: (S, dln)}; returns (label, pairs)."""
    defined = {k: v for k, v in cls.items() if math.isfinite(v[0]) and v[0] > 0}
    undefined = sorted(set(cls) - set(defined))
    if "galaxy" not in defined:
        return "NOT POSSIBLE ON DISK (galaxy clock undefined)", [], undefined
    ks, pairs = sorted(defined), []
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, b = defined[ks[i]], defined[ks[j]]
            den = math.hypot(a[1], b[1])
            z = abs(math.log(a[0]) - math.log(b[0])) / den if math.isfinite(den) else 0.0
            pairs.append((ks[i], ks[j], z))
    if len(pairs) == 0:
        return "NOT POSSIBLE ON DISK (fewer than two clocks)", pairs, undefined
    if any(p[2] >= 2 for p in pairs):
        lab = "NOT UNIVERSAL"
    elif all(defined[k][1] <= 0.35 for k in defined):
        lab = "UNIVERSAL"
    else:
        lab = "CONSISTENT, NOT DIAGNOSTIC"
    if undefined:
        lab += f" [undefined: {', '.join(undefined)}]"
    return lab, pairs, undefined

def run_row(label, e_by_class, seed=SEED):
    rng = np.random.default_rng(seed)
    cls, txt = {}, []
    for k in ("galaxy", "group", "cluster"):
        e = e_by_class[k]
        S, em, se = S_of(e)
        dln, finf = boot_dln(e, rng)
        cls[k] = (S, dln)
        txt.append(f"     {k:8s} N {len(e):2d}  e_med {em:.3f}  sigma_e {se:.3f}  S = sigma(ln t) {S:.3f}  delta(ln S) {dln:.3f}  (boot e_med outside (0,1): {finf:.1%})")
    lab, pairs, und = verdict(cls)
    say(f"  {label}")
    for t in txt: say(t)
    say("     pairs: " + "; ".join(f"{a}-{b} z = {z:.2f}" for a, b, z in pairs) + f"  ->  {lab}")
    return cls, lab, pairs

checks = {}
# ------------------------------------------------------------------ C1 identity
ok = True
for e in np.linspace(0.02, 0.98, 40):
    x = -math.log(e); h = 1e-6
    num_ = (math.log(math.exp(-x * (1 + h))) - math.log(math.exp(-x * (1 - h)))) / (math.log(1 + h) - math.log(1 - h))
    ok &= abs(num_ - math.log(e)) < 1e-6 * abs(math.log(e))
    f = 1 - e; eps = (1 - f) * (-math.log(1 - f)) / f
    ok &= abs((0.1 / f) / eps - 0.1 / (e * abs(math.log(e)))) < 1e-12
checks["C1_identity"] = bool(ok)

# ------------------------------------------------------------------ data rows
e_gal = gal_e(A0_CAN); e_grp = grp_e(0.0); e_cl = cl_e(0.0)
S_gal_ref = S_of(e_gal)[0]
S_grp0, S_cl0 = S_of(e_grp)[0], S_of(e_cl)[0]

# C2 reproduction
t14 = lambda f, sf: (sf / f) / ((1 - f) * (-math.log(1 - f)) / f)
re_cl, re_g = 0.15 / (0.43 * abs(math.log(0.43))), 0.15 / (0.60 * abs(math.log(0.60)))
fb_cl, fb_g = t14(0.43, 0.15), t14(0.60, 0.15)
checks["C2_reproduction"] = bool(abs(re_cl - 0.413) < 0.002 and abs(re_g - 0.489) < 0.002 and abs(fb_cl - 0.468) < 0.002
                                 and abs(fb_g - 0.409) < 0.002 and abs(np.median(e_gal) - 0.13) < 0.005 and len(GAL) == 23
                                 and abs(np.median(e_grp) - 0.787) < 0.002 and abs(np.median(e_cl) - 0.413) < 0.002 and len(CL) == 7)

# MUTATE: injected galaxy clock break (x4 or x1/4, away from the geometric mean of the other two)
mut_k = None
if MUT:
    gm = math.sqrt(S_grp0 * S_cl0) if math.isfinite(S_grp0) and math.isfinite(S_cl0) else (S_cl0 if math.isfinite(S_cl0) else S_grp0)
    mut_k = 4.0 if S_gal_ref >= gm else 0.25
    em = np.median(e_gal); e_gal = em + mut_k * (e_gal - em)
checks["C3_control_integrity"] = bool(abs(S_of(e_gal)[0] / S_gal_ref - 1) < 1e-9)

say(f"CFG431 clock universality  MUTATE={MUT}" + (f"  (galaxy scatter x{mut_k})" if MUT else ""))
say("Branch: leftover e (definition A); S = sigma(ln t) = sigma_e/(e_med |ln e_med|). S is total scatter (upper bound on intrinsic).")
say("")
say("T14 inputs (0.43/0.60 +- 0.15 = CFG382 TOLERANCE bands, not population scatter), reported only:")
say(f"  e branch (correct per T15): clusters {re_cl:.3f}, groups {re_g:.3f}   |   T14's f branch: clusters {fb_cl:.3f}, groups {fb_g:.3f}")
say("")
say("PRIMARY (def A, b = 0, canonical; as on disk):")
cls_p, lab_p, pairs_p = run_row("primary", dict(galaxy=e_gal, group=e_grp, cluster=e_cl))

rob = {}
if not MUT:
    say("")
    say("ROBUSTNESS (reported):")
    rob["R1_alt_footing"] = run_row("R1 alt footing (galaxies a0 = 1.1312e-10)", dict(galaxy=gal_e(A0_ALT), group=e_grp, cluster=e_cl))[1]
    rob["R2_xcop_gas_R500"] = run_row("R2 X-COP gas mass at R500", dict(galaxy=e_gal, group=e_grp, cluster=cl_e(0.0, gasR500=True)))[1]
    rob["R3_b0.1"] = run_row("R3 hydrostatic bias b = 0.1", dict(galaxy=e_gal, group=grp_e(0.1), cluster=cl_e(0.1)))[1]
    # R4 noise-corrected
    rng = np.random.default_rng(SEED)
    def noise_sigma(draw):
        es = np.array([draw() for _ in range(NMC)])               # (NMC, N)
        dev = es - np.median(es, axis=0)
        return float(np.median((np.percentile(dev, 84, axis=0) - np.percentile(dev, 16, axis=0)) / 2))
    Mt0 = np.array([t2[n][0] for n in GAL]); eMt = np.array([t2[n][2] for n in GAL])
    fd0 = np.array([t2[n][1] for n in GAL]); efd = np.array([t2[n][3] for n in GAL])
    sn_gal = noise_sigma(lambda: gal_e(A0_CAN, Mt=np.clip(Mt0 + eMt * rng.standard_normal(len(GAL)), 1e9, None),
                                        fd=np.clip(fd0 + efd * rng.standard_normal(len(GAL)), 0.0, 0.95)))
    M0 = np.array([g["M"] for g in GRP]); eM = np.array([g["eM"] for g in GRP]); Mg0 = np.array([g["Mg"] for g in GRP]); eMg = np.array([g["eMg"] for g in GRP])
    sn_grp = noise_sigma(lambda: grp_e(0.0, M=np.clip(M0 + eM * rng.standard_normal(len(GRP)), 1e11, None),
                                        Mg=np.clip(Mg0 + eMg * rng.standard_normal(len(GRP)), 1e10, None)))
    Mc0 = np.array([c["M"] for c in CL]); eMc = np.array([c["eM"] for c in CL])
    sn_cl = noise_sigma(lambda: cl_e(0.0, M=np.clip(Mc0 + eMc * rng.standard_normal(len(CL)), 1e12, None)))
    say("  R4 noise-corrected (MC of per-object input errors; sigma_int^2 = sigma_e^2 - sigma_noise^2):")
    r4 = {}
    for k, e, sn in (("galaxy", e_gal, sn_gal), ("group", e_grp, sn_grp), ("cluster", e_cl, sn_cl)):
        S, em, se = S_of(e)
        si = math.sqrt(max(se ** 2 - sn ** 2, 0.0))
        Si = si / (em * abs(math.log(em))) if 0 < em < 1 else math.inf
        r4[k] = dict(sigma_e=se, sigma_noise=sn, sigma_int=si, S_int=Si)
        say(f"     {k:8s} sigma_e {se:.3f}  median per-object noise {sn:.3f}  sigma_int {si:.3f}  S_int {Si:.3f}")
    rob["R4_noise"] = r4
    # exact per-object map
    say("  exact per-object map ln t_i = ln(-ln e_i) (0 < e_i < 1 only):")
    for k, e in (("galaxy", e_gal), ("group", e_grp), ("cluster", e_cl)):
        m = (e > 0) & (e < 1); lt = np.log(-np.log(e[m]))
        say(f"     {k:8s} kept {m.sum()}/{len(e)}  sigma(ln t) robust {((np.percentile(lt, 84) - np.percentile(lt, 16)) / 2):.3f}")

# underpowered rule: decided from the MUTATE output file if present
mut_file = os.path.join(HERE, "cfg431_results_MUTATE.json")
final = lab_p
if not MUT:
    cats = {lab_p.split(" [")[0]} | {v.split(" [")[0] for k, v in rob.items() if isinstance(v, str)}
    if len(cats) > 1:
        final += "  (FRAGILE: robustness rows give " + " / ".join(sorted(cats)) + ")"
    if os.path.exists(mut_file):
        mv = json.load(open(mut_file))["verdict_primary"]
        if not mv.startswith("NOT UNIVERSAL") and not lab_p.startswith("NOT UNIVERSAL"):
            final = "CONSISTENT, NOT DIAGNOSTIC (MUTATE break not detected: underpowered)" + final[len(lab_p):]
        say("")
        say(f"MUTATE run verdict (from cfg431_results_MUTATE.json): {mv}")
    else:
        say(""); say("MUTATE output not found: run T431_MUTATE=1 first; underpowered rule not applied.")
else:
    checks["MUTATE_detected"] = lab_p.startswith("NOT UNIVERSAL")

say("")
say("checks: " + json.dumps(checks))
say(f"VERDICT{TAG}: {final}")
json.dump(dict(mutate=MUT, mut_k=mut_k, branch="leftover e (def A)",
               primary={k: dict(S=v[0], dlnS=v[1]) for k, v in cls_p.items()}, pairs=pairs_p, verdict_primary=lab_p,
               robustness=rob, final=final, t14_reread=dict(e_branch=[re_cl, re_g], f_branch=[fb_cl, fb_g]),
               galaxies=GAL, clusters=[c["name"] for c in CL], checks=checks),
          open(os.path.join(HERE, f"cfg431_results{TAG}.json"), "w"), indent=1, default=float)
ok = all(checks.values())
sys.exit(0 if ok else 1)
