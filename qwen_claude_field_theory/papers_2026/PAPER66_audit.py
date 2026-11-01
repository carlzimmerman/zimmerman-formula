#!/usr/bin/env python3
"""PAPER66 audit: quoted numbers match AC1's committed results; seals match; PDF newer than TeX; naming rules; no local path.
Run: python3 PAPER66_audit.py (exit 0 only if all pass).  --mutate perturbs every JSON-derived number; exit 0 only if every number check then FAILS."""
import hashlib, json, os, re, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); STEM = "PAPER66_alma_release_predictions_2026"
TEX = open(os.path.join(HERE, STEM + ".tex")).read() + "".join(open(os.path.join(HERE, f"PAPER66_tables_{x}.tex")).read() for x in "abc")
D = json.load(open(os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions", "ac1_results.json"))); A, B, I = D["A"], D["B"], D["identity"]
F = N = NF = NN = 0
def check(n, ok, m=""):
    global F, N; N += 1; F += not ok
    if not MUT: print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f": {m}" if m else ""))
def bump(t):
    for i in range(len(t) - 1, -1, -1):
        if t[i].isdigit(): return t[:i] + str((int(t[i]) + 1) % 10) + t[i + 1:]
    return t + "1"
def num(n, v, fmt, ctx):
    """ctx is the sentence fragment in the TeX, with {} where the number sits, so a perturbed number cannot match elsewhere."""
    global NF, NN; t = format(v, fmt); t = bump(t) if MUT else t; ok = ctx.format(t) in TEX; NN += 1; NF += not ok
    if not MUT: check(n, ok, t)
K = "lgM*11.11|S2|alpha1.0"; f = B["forward"][K]; C = "n=1|canon 9.36e-11|"
num("sep U4_27928", I["sep_U4_27928"], ".3f", "U4\\_27928 lies {}$''$ away"); num("sep U4_28473", I["sep_U4_28473"], ".3f", "lies {}$''$ from the phase centre"); num("nu", I["nu_CO21_U4_27928"], ".2f", "at {}\\,GHz, does fall"); num("fwhm", I["fwhm"], ".0f", "for a {}$''$ beam"); num("pb", I["pb"], ".2f", "primary-beam response {} for")
num("empirical gas", A["empirical_logMgas"], ".2f", "gives $\\log M_{{\\rm gas}}={}$."); num("S/N 10.51", A["forecast"]["per_mass"]["10.51"]["SN_1000"], ".2f", "disc reads S/N {} at"); num("S/N 11", A["forecast"]["per_mass"]["11.0"]["SN_1000"], ".2f", "and {} at 11.0"); num("UL 4.36", A["forecast"]["UL3sig_alpha436"], ".2f", "limit is $\\log M_{{\\rm gas}}={}$ for"); num("UL 1", A["forecast"]["UL3sig_alpha1"], ".2f", "and {} for $\\alpha_{{\\rm CO}}=1$, below")
mx = max(y for c in A["req"].values() for k, v in c.items() if not k.startswith("route") for kk, x in v.items() if "F-" in kk for y in (x["logMgas_Rg=Rd"], x["logMgas_Rg=1.5Rd"]) if y); num("max requirement", mx, ".2f", "(at most {})")
num("gas 4.36", B["logMgas"]["4.36"], ".2f", "$\\log M_{{\\rm gas}}={}$ ($\\alpha_{{\\rm CO}}=4.36$)"); num("gas 1", B["logMgas"]["1.0"], ".2f", "or {} ($\\alpha_{{\\rm CO}}=1$)"); nw = [v["Newton"][2] for v in B["forward"].values()]; num("Newton min", min(nw), ".0f", "reach {}--"); num("Newton max", max(nw), ".0f", "--{}\\,km\\,s$^{{-1}}$ across")
num("F-DESI ratio", B["a0_ratio"]["F-DESI"], ".3f", "F-DESI {}, and"); num("R-H ratio", B["a0_ratio"]["R-H"], ".3f", "(R-H, {})"); num("L-fb ratio", B["a0_ratio"]["L-fb(RAR-eq)"], ".2f", "(L-fb, {}, held"); num("S2 Re", B["shapes"]["S2"], ".2f", "Stellar $R_e$ {}\\,kpc as")
cs = [c for v in B["aqual"].values() for c in v["C"]]; num("C min", min(cs), ".3f", "factor {}--"); num("C max", max(cs), ".3f", "--{} at 1--8"); num("core V 3 kpc", B["core"]["12.5"]["V"][2], ".0f", "about {}\\,km\\,s$^{{-1}}$ at lg")
fc = B["forecast"]; num("peak", fc["peak_SN_100"], ".1f", "Peak S/N {} per"); num("Rbeam", fc["Rmax_beam"], ".2f", "out to {}\\,kpc; 3$\\sigma$ per azimuthal"); num("Rring", fc["Rmax_ring"], ".2f", "ring out to {}\\,kpc"); num("m0", max(fc["moment0_aperture_SN_1000"].values()), ".2f", "peaks at only {},"); num("3D", fc["matched_3D_SN"], ".1f", "statistic reads {}."); num("beam", fc["beam_kpc"], ".2f", "Beam {}\\,kpc")
H = B["halpha_430_at_3kpc_information"]; num("alpha 0.88", float(H["lgM*11.11|S2"]["n=1|F-flat"]), ".2f", "is {} for lg"); num("alpha 0.07", float(H["lgM*11.31|S2"]["n=1|F-flat"]), ".2f", "S2, {} for 11.31")
num("flat - DESI", f[C + "F-flat"][2] - f[C + "F-DESI"][2], ".0f", "differ by {}\\,km\\,s$^{{-1}}$ at 3\\,kpc"); num("R-H - flat", f[C + "R-H"][2] - f[C + "F-flat"][2], ".0f", "sits {}\\,km\\,s$^{{-1}}$ above"); num("law - N 3", f[C + "F-flat"][2] - f["route N|12.5"][2], ".0f", "route N by {}\\,km\\,s$^{{-1}}$"); num("law - N 8", f[C + "F-flat"][5] - f["route N|12.5"][5], ".0f", "and by {} at 8\\,kpc")
PW = json.load(open(os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions", "ac1_score_power_results.json")))["runs"]; ST = json.load(open(os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions", "ac1_score_selftest_results.json")))["results"]
det = lambda k: sum(x["det"] for x in PW[k]) + bool(ST[k]["G1_3D"]["PASS"]); val = lambda k: sum(x["valid"] for x in PW[k]) + bool(ST[k].get("fits", {}).get("incl-Tadaki", {}).get("valid"))
num("smooth detected", det("realistic"), "d", "1.56\\,kpc & 0 of 7 & {} of 7"); num("smooth scored", val("realistic"), "d", "1.56\\,kpc & 0 of 7 & 1 of 7 & {} of 7"); num("compact detected", det("compact"), "d", "0.8\\,kpc & 0 of 7 & {} of 7"); num("compact scored", val("compact"), "d", "0.8\\,kpc & 0 of 7 & 6 of 7 & {} of 7"); num("no line detected", det("noise"), "d", "no line & 0 of 7 & {} of 7")
num("MOCK rms", (sum((x["Vc"] / 430 - 1) ** 2 for x in PW["compact"] if x["valid"]) / sum(x["valid"] for x in PW["compact"])) ** 0.5 * 100, ".1f", "recovery error is {}\\,\\%")
AC = os.path.join(ROOT, "rebuild_2026_10_22", "AC1_alma_condor_predictions"); NC = json.load(open(os.path.join(AC, "ac1_condor_noise_results.json"))); VA = json.load(open(os.path.join(AC, "ac1_score_VALIDATION.json"))); P2 = json.load(open(os.path.join(AC, "ac1_score_power_div2.54_condorbeam_results.json")))["summary"]
num("sister ratio", NC["ratio"], ".2f", "a ratio of {}, from"); num("sister measured", NC["measured"], ".3f", "the noise is {} against the listed"); num("sister listed", NC["listed"], ".3f", "against the listed {}, a ratio"); num("val flux", VA["UL"]["ap_flux"], ".2f", "flux {} $\\pm$"); num("val flux err", VA["UL"]["rms"], ".2f", "$\\pm$ {}\\,Jy\\,km\\,s$^{{-1}}$ against the published"); num("val z", VA["G1_frozen"]["z_line"], ".5f", "line redshift {} against")
R, CP = P2["realistic"], P2["compact"]; num("smooth m2", R["g3_pass"], "d", "1.56\\,kpc & 6 of 6 & {} of 6"); num("smooth V lo", min(R["Vc_valid"]), "d", "& {}--444"); num("smooth V hi", max(R["Vc_valid"]), "d", "& 408--{}"); num("compact V lo", min(CP["Vc_valid"]), "d", "& {}--438"); num("compact V hi", max(CP["Vc_valid"]), "d", "& 413--{}"); num("no line m2", P2["noise"]["g3_pass"], "d", "no line & 0 of 6 & {} of 6")
if MUT:
    print(f"MUTATE: {NF} of {NN} number checks fail"); sys.exit(0 if NF == NN else 1)
SEAL = {"campaign_fresh_gravity/CFG571_prereg_proprietary_alma/cfg571_prereg_results.json": "be27457d", "argon_push/AG4e_n1_alma_seal/SEALED_N1.json": "9802de0d", "argon_push/AG4d_n2_alma_seal/SEALED_N2.json": "d64727b5", "rebuild_2026_10_22/S3_v3_mw_seals/SEALED_V3_ALMA_AQUAL.json": "b5d65a5e", "rebuild_2026_10_22/AC1_alma_condor_predictions/ac1_results.json": "bfdfed68"}
for p, h in SEAL.items(): check("hash " + os.path.basename(p), hashlib.sha256(open(os.path.join(ROOT, p), "rb").read()).hexdigest().startswith(h) and h in TEX)
check("all AC1 checks pass", all(o for _, o in D["checks"]))
pdf, tx = os.path.join(HERE, STEM + ".pdf"), os.path.join(HERE, STEM + ".tex"); check("PDF newer than TeX", os.path.getmtime(pdf) >= os.path.getmtime(tx))
low = TEX.lower(); check("naming", "cold dark matter" not in low and not re.search(r"(?<!lambda)(?<!\$\\lambda\$)\bcdm\b", low)); check("kappa fitted, not closed", "fitted" in low and "not closed" in low or "not theory closed" in low)
check("no local path", "/Users/" not in TEX and "carlzimmerman" not in TEX); check("no favour claim beyond the disclaimer", len(re.findall(r"\bfavour", low)) == 1)
print(f"{N - F} of {N} checks pass"); sys.exit(1 if F else 0)
