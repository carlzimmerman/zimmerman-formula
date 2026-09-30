#!/usr/bin/env python3
"""v02_sparc_refit_systematics.py -- what moves the SPARC a0, measured with the record's own profile-likelihood machinery
(Upsilon_disk free per galaxy), re-implemented (vectorised) in v_common.py.  NOTHING IS ADJUSTED: every perturbation is reported as a
shift d ln a0; the reader decides whether it is inside a budget.

 R  reproduce the record's a0_hat = 1.0766e-10, 1.24% / 5.44% (its grid method) and then correct the interpolation error of its grid
 B  galaxy bootstrap / jackknife: the honest galaxy-clustered sigma(a0) (replaces the crude sqrt(N_pts/N_gal) inflation)
 I  interpolating function (IF) x Upsilon-treatment matrix: alpha1 (record kernel), RAR, simple, standard  x  Upsilon free / [0.25,1] / [0.3,0.8] / fixed 0.5
 F  fixed-Upsilon fit as MLS16 did it: does the machinery return ~1.20e-10 for the RAR IF, and ESR's 1.11/1.13/1.54?  (validation against papers)
 S  which IF makes a0 most consistent between gas-dominated (T>=8) and star-dominated (T<=5) galaxies?
 D  distance-scale, gas-mass and inclination perturbations (exact transformations of the rotmod content, v_common.transform)
 H  H0-coupled distances: SPARC's f_D = 1 distances are Hubble-flow distances at H0 = 73, so a0_obs depends on the H0 used for them
 M  mocks: estimator bias with the right kernel; kernel-mismatch bias; is the RAR-vs-alpha1 chi2 preference an artefact?
Exit 0 = every check held.  Results go to v02_results.json (read by v03/v04/v05).
"""
import json, math, sys, time, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v_common import *

ok = []
def check(cond, msg):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {msg}")

t0 = time.time()
U = 1e-10
gals = load_sparc()
res = {}
print(f"loaded {len(gals)} galaxies, {sum(len(g['Vobs']) for g in gals)} points")
A0GRID = np.exp(np.linspace(math.log(0.62e-10), math.log(1.75e-10), 61))     # 61-point log grid
SIGI = None

print("\nC0  every IF has the same normalisation (sqrt(g a0) deep, g Newtonian)")
for nm, F in IFS.items():
    check(deep_limit_ok(F), f"C0 {nm}: deep-MOND and Newtonian limits both correct")

# ---------------------------------------------------------------------------------------------- R reproduce (record's own grid procedure)
print("\nR  reproduce the record's profile likelihood (alpha1 kernel, Upsilon free per galaxy 0.05-3.0)")
P1 = Profile(gals, IF_alpha1)
SIGI = P1.calibrate_sig_int(A0_FW_REC)
ch0, n0 = P1.chi2(A0_FW_REC, SIGI)
print(f"   sig_int (chi2/dof = 1 at canonical a0) = {SIGI:.4f} dex   (record: 0.0808)   chi2 = {ch0:.1f}, npts = {n0}  (record: 3204.0, 3380)")
check(abs(SIGI - 0.0808) < 0.0006 and n0 == 3380 and abs(ch0 - 3204.0) < 3.0, "R1 sig_int, n_pts and chi2 at canonical a0 reproduce the record's P2b")
# the record's grid: 31 points 0.70..1.45 x A0_FW plus 3 extras; crossings by linear interpolation
A0_ALT = 1.13e-10
recgrid = np.array(sorted(set(np.concatenate([np.linspace(0.70, 1.45, 31) * A0_FW_REC, [A0_FW_REC, A0_ALT, c_l * H0_REC / (2 * math.pi)]]))))
chr_ = np.array([P1.chi2(a, SIGI)[0] for a in recgrid])
im = int(np.argmin(chr_)); a_rec = recgrid[im]
def crossings(a, chv, im_, target=1.0):
    out = []
    for side in (range(im_, len(a) - 1), range(im_, 0, -1)):
        prev = None
        for i in side:
            d = chv[i] - chv[im_]
            if prev is not None and (prev[1] - target) * (d - target) <= 0 and prev[1] != d:
                t = (target - prev[1]) / (d - prev[1]); out.append(prev[0] + t * (a[i] - prev[0])); break
            prev = (a[i], d)
    return out
cr = crossings(recgrid, chr_, im)
sig_rec = 0.5 * abs(cr[0] - cr[1]) / a_rec
infl = math.sqrt(n0 / 175)
print(f"   record's grid: a0_hat(grid min) = {a_rec*1e10:.4f}e-10 (record 1.0766), sigma_ind = {100*sig_rec:.2f}% (record 1.24%), x{infl:.2f} = {100*sig_rec*infl:.2f}% (record 5.44%)")
check(abs(a_rec / 1.0766e-10 - 1) < 0.001 and abs(100 * sig_rec - 1.24) < 0.03 and abs(100 * sig_rec * infl - 5.44) < 0.15,
      "R2 the record's own grid procedure reproduces 1.0766e-10, 1.24% and 5.44%")
# fine local grid: the record's 2.3% grid spacing interpolates the crossings too coarsely
fine = np.exp(np.linspace(math.log(a_rec) - 0.09, math.log(a_rec) + 0.09, 73))
chf = np.array([P1.chi2(a, SIGI)[0] for a in fine]); imf = int(np.argmin(chf))
crf = crossings(fine, chf, imf)
a_fine, s_par = parabola_min(fine, chf, k=12)
sig_fine = 0.5 * abs(crf[0] - crf[1]) / fine[imf]
print(f"   fine local grid (73 pts, +-9%): a0_hat = {a_fine*1e10:.4f}e-10, sigma_ind = {100*sig_fine:.2f}% (Dchi2 = 1 crossings) / {100*s_par:.2f}% (parabola); x{infl:.2f} = {100*sig_fine*infl:.2f}%")
print(f"   -> the record's 1.24% is an interpolation underestimate (true ~{100*sig_fine:.2f}%); its 5.44% is ~{100*sig_fine*infl:.1f}% by the same crude rule.  Immaterial to any verdict; corrected here.")
check(sig_fine > sig_rec and abs(a_fine / a_rec - 1) < 0.02, "R3 the fine-grid sigma_ind exceeds the record's (coarse-grid interpolation bias) and a0_hat moves by < 2%")
res["record_pl"] = dict(a0_hat_record_grid=float(a_rec), a0_hat=float(a_fine), sig_ln_ind_record_grid=float(sig_rec), sig_ln_ind=float(sig_fine),
                        sig_ln_clustered_crude=float(sig_fine * infl), sig_ln_clustered_crude_record=float(sig_rec * infl), sig_int=float(SIGI), chi2_min=float(chf.min()), n_pts=int(n0))
a0_hat = a_fine; s_ln = sig_fine

# ---------------------------------------------------------------------------------------------- B bootstrap
print("\nB  galaxy bootstrap / jackknife of the profile (per-galaxy profiled chi2 on a grid, resampled galaxies)")
def per_gal_chi2(gs, IF, a0grid, sig_int_, **kw):
    out = np.zeros((len(gs), len(a0grid)))
    for j, g in enumerate(gs):
        P = Profile([g], IF, **kw)
        for k, a in enumerate(a0grid):
            out[j, k] = P.chi2(a, sig_int_)[0]
    return out
BGRID = np.exp(np.linspace(math.log(a0_hat) - 0.35, math.log(a0_hat) + 0.35, 57))
CHIG = per_gal_chi2(gals, IF_alpha1, BGRID, SIGI)
chB = np.array([P1.chi2(a, SIGI)[0] for a in BGRID])
check(abs(CHIG.sum(0) - chB).max() < 1e-6, "B1 per-galaxy profiled chi2 sums to the total profile (max diff < 1e-6)")
rng = np.random.default_rng(20260929)
boot = np.array([parabola_min(BGRID, CHIG[rng.integers(0, len(gals), len(gals))].sum(0), k=10)[0] for _ in range(2000)])
sig_boot = float(np.std(np.log(boot)))
jk = np.array([math.log(parabola_min(BGRID, CHIG.sum(0) - CHIG[j], k=10)[0]) for j in range(len(gals))])
sig_jk = math.sqrt((len(jk) - 1) / len(jk) * np.sum((jk - jk.mean()) ** 2))
print(f"   bootstrap sigma(ln a0) = {100*sig_boot:.2f}%   68% interval [{np.percentile(boot,16)*1e10:.4f}, {np.percentile(boot,84)*1e10:.4f}]e-10;  jackknife sigma = {100*sig_jk:.2f}%")
print(f"   compare: points-independent {100*s_ln:.2f}%, crude x4.39 rule {100*s_ln*infl:.2f}%, record 5.44%")
res["record_pl"].update(sig_ln_bootstrap=sig_boot, sig_ln_jackknife=float(sig_jk))
check(sig_boot > 2 * s_ln, "B2 galaxy-clustered error is > 2x the points-independent error (clustering matters)")
check(abs(sig_boot / sig_jk - 1) < 0.25, "B3 bootstrap and jackknife agree within 25%")

# ---------------------------------------------------------------------------------------------- I matrix
print("\nI  a0_hat [1e-10 m/s^2] for each IF x Upsilon treatment (all 175 galaxies, sig_int fixed at the record's 0.0808 dex; chi2 in brackets)")
UTREAT = {"Upsilon free 0.05-3 (record)": {}, "Upsilon in [0.25,1.0] (factor-2)": dict(ulo=0.25, uhi=1.0),
          "Upsilon in [0.3,0.8]": dict(ulo=0.3, uhi=0.8), "Upsilon fixed 0.5 (bulge 0.7)": dict(ufixed=0.5)}
mat = {}
hdr = "".join(f"{k:>30}" for k in IFS)
print(f"   {'':<36}{hdr}")
for un, kw in UTREAT.items():
    row = {}
    line = f"   {un:<36}"
    for inm, F in IFS.items():
        P = Profile(gals, F, **kw); chv = P.scan(A0GRID, SIGI); a, s = parabola_min(A0GRID, chv)
        row[inm] = dict(a0=a, sig_ln=s, chi2=float(chv.min()))
        line += f"{a*1e10:>16.4f} ({chv.min():>7.0f})  "
    mat[un] = row
    print(line)
res["matrix"] = mat
cfree = {k: v["chi2"] for k, v in mat["Upsilon free 0.05-3 (record)"].items()}
aF = {k: v["a0"] for k, v in mat["Upsilon free 0.05-3 (record)"].items()}
print(f"   chi2_min (Upsilon free): " + ", ".join(f"{k.split()[0]} {v:.0f}" for k, v in cfree.items()))
dch = cfree["alpha1 (record kernel)"] - cfree["RAR (MLS16)"]
print(f"   the record's own likelihood prefers RAR over its alpha1 kernel by d chi2 = {dch:.0f} (points-independent; /{infl**2:.1f} = {dch/infl**2:.0f} on the crude clustered rule) at equal parameter count")
res["dchi2_alpha1_minus_RAR"] = float(dch)
check(all(max(r["a0"] for r in row.values()) > 1.02 * min(r["a0"] for r in row.values()) for row in mat.values()), "I1 (control that the fit is IF-sensitive) a0_hat differs by > 2% between IFs in every Upsilon treatment")
check(mat["Upsilon fixed 0.5 (bulge 0.7)"]["standard"]["a0"] > 1.3 * mat["Upsilon fixed 0.5 (bulge 0.7)"]["RAR (MLS16)"]["a0"], "I2 the standard IF returns a0 > 1.3x the RAR IF at fixed Upsilon (ESR paper: 1.54 vs 1.13)")

# robustness: recalibrate sig_int at each IF's OWN best a0 (the record calibrates at the canonical a0 with the alpha1 kernel)
recal = {}
for nm, F in IFS.items():
    P = Profile(gals, F); ah = mat["Upsilon free 0.05-3 (record)"][nm]["a0"]
    sr = P.calibrate_sig_int(ah); a2, _ = parabola_min(A0GRID, P.scan(A0GRID, sr))
    recal[nm] = dict(sig_int=sr, a0=a2, rel=a2 / ah - 1)
print("   recalibrating sig_int at each IF's own best a0 (chi2/dof = 1): " + ", ".join(f"{k.split()[0]} sig_int {v['sig_int']:.4f} -> a0 {v['a0']*1e10:.4f} ({100*v['rel']:+.2f}%)" for k, v in recal.items()))
res["recalibrated_sig_int"] = recal
check(max(abs(v["rel"]) for v in recal.values()) < 0.01, f"I3 recalibrating sig_int per IF changes a0_hat by < 1% (max {100*max(abs(v['rel']) for v in recal.values()):.2f}%)")

# ---------------------------------------------------------------------------------------------- F validation
print("\nF  fixed-Upsilon fit done the published way (Upsilon = 0.5/0.7, MLS16 cuts Q<=2 & inc>=30) -- validation against papers")
sel = [g for g in gals if g["Q"] <= 2 and g["inc"] >= 30]
check(len(sel) == 153, f"F1 the MLS16 cuts select exactly 153 SPARC galaxies (got {len(sel)})")
rowF = {}
for nm, F in IFS.items():
    P = Profile(sel, F, ufixed=0.5); chv = P.scan(A0GRID, 0.11)       # 0.11 dex scatter as in MLS16 (Gaussian fit width)
    a, s = parabola_min(A0GRID, chv); rowF[nm] = a
print("   " + ", ".join(f"{k.split()[0]} {v*1e10:.3f}" for k, v in rowF.items()) + "   (1e-10 m/s^2; 153 galaxies, sig_int = 0.11 dex)")
print("   published: MLS16 RAR 1.20 +- 0.02 +- 0.24 (ODR);  Desmond-Bartlett-Ferreira 2023 Table 1 (Simple 1.11, RAR 1.13, Standard 1.54, prior-max galaxy parameters)")
check(abs(rowF["RAR (MLS16)"] / 1.20e-10 - 1) < 0.12, f"F2 RAR IF fixed-Upsilon a0 = {rowF['RAR (MLS16)']*1e10:.3f} is within 12% of MLS16's 1.20 (methods differ: LSQ vs ODR)")
check(abs(rowF["simple"] / 1.11e-10 - 1) < 0.06 and abs(rowF["standard"] / 1.54e-10 - 1) < 0.06 and abs(rowF["RAR (MLS16)"] / 1.13e-10 - 1) < 0.06,
      "F3 simple / RAR / standard fixed-Upsilon a0 reproduce the ESR paper's 1.11 / 1.13 / 1.54 within 6%")
res["fixed_ups_MLS16cuts"] = {k: float(v) for k, v in rowF.items()}

# ---------------------------------------------------------------------------------------------- S subsample consistency
print("\nS  subsample consistency: a0_hat for gas-dominated (T>=8, n=81) vs star-dominated (T<=5, n=62) galaxies, per IF and Upsilon treatment")
sub = {}
for un in ("Upsilon free 0.05-3 (record)", "Upsilon in [0.25,1.0] (factor-2)"):
    kw = UTREAT[un]
    for nm, F in IFS.items():
        ag = parabola_min(A0GRID, Profile([g for g in gals if g["T"] >= 8], F, **kw).scan(A0GRID, SIGI))
        as_ = parabola_min(A0GRID, Profile([g for g in gals if g["T"] <= 5], F, **kw).scan(A0GRID, SIGI))
        r = as_[0] / ag[0]
        zsig = math.log(r) / math.hypot(ag[1], as_[1])
        sub[f"{un} | {nm}"] = dict(gas=ag[0], star=as_[0], ratio=r, nsig_ind=zsig)
        print(f"   {un:<34}{nm:<24} gas-dom {ag[0]*1e10:.3f}  star-dom {as_[0]*1e10:.3f}  ratio {r:5.2f}  ({zsig:+5.1f} sigma, independent points)")
res["subsample_split"] = sub
best = min(sub, key=lambda k: abs(math.log(sub[k]["ratio"])))
worst = max(sub, key=lambda k: abs(math.log(sub[k]["ratio"])))
print(f"   most consistent split: {best} (ratio {sub[best]['ratio']:.2f});  least: {worst} (ratio {sub[worst]['ratio']:.2f})")
ratios_free = [sub[f"Upsilon free 0.05-3 (record) | {nm}"]["ratio"] for nm in IFS]
check(max(ratios_free) / min(ratios_free) < 1.15 and min(ratios_free) > 2.0,
      f"S1 the gas-/star-dominated a0 split is IF-INDEPENDENT (Upsilon free: ratio {min(ratios_free):.2f}-{max(ratios_free):.2f} for all four IFs): a different kernel does not remove it")
# the cleanest published-style split: RAR IF, fixed Upsilon 0.5/0.7, MLS16 cuts
selc = [g for g in gals if g["Q"] <= 2 and g["inc"] >= 30]
clean = {}
for lab, f in (("gas-dominated T>=8", lambda g: g["T"] >= 8), ("star-dominated T<=5", lambda g: g["T"] <= 5)):
    ss = [g for g in selc if f(g)]
    a_, s_ = parabola_min(np.exp(np.linspace(math.log(0.5e-10), math.log(2.2e-10), 69)), Profile(ss, IF_rar, ufixed=0.5).scan(np.exp(np.linspace(math.log(0.5e-10), math.log(2.2e-10), 69)), 0.11), k=8)
    clean[lab] = dict(n=len(ss), a0=a_, sig_ln=s_)
rcl = clean["star-dominated T<=5"]["a0"] / clean["gas-dominated T>=8"]["a0"]
print(f"   cleanest published-style split (RAR IF, Upsilon fixed 0.5/0.7, MLS16 cuts, 0.11 dex): gas-dominated {clean['gas-dominated T>=8']['a0']*1e10:.3f} (n={clean['gas-dominated T>=8']['n']}), star-dominated {clean['star-dominated T<=5']['a0']*1e10:.3f} (n={clean['star-dominated T<=5']['n']}); ratio {rcl:.2f}")
res["class_split_clean"] = dict(clean, ratio=rcl, half_range_ln=0.5 * math.log(rcl))
check(rcl > 1.2, f"S2 even in the cleanest published-style fit the two galaxy classes disagree on a0 by {100*(rcl-1):.0f}% (half-range in ln a0 = {100*0.5*math.log(rcl):.0f}%): a class-heterogeneity systematic no statistical error covers")

# ---------------------------------------------------------------------------------------------- D perturbations
print("\nD  systematic perturbations of the baseline fit (alpha1 kernel, Upsilon free, sig_int fixed 0.0808), all 175 galaxies")
# unit test of the transform: distance rescale leaves g_bar exactly invariant and scales g_obs by 1/s
def gbar_gobs(g, U=0.5):
    Vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2
    return Vb2 * 1e6 / g["Rm"], (g["Vobs"] * 1e3) ** 2 / g["Rm"]
maxdev = 0.0
for g in gals[:40]:
    gb0, go0 = gbar_gobs(g); gb1, go1 = gbar_gobs(transform(g, dist_scale=1.07))
    maxdev = max(maxdev, np.max(np.abs(gb1 / gb0 - 1)), np.max(np.abs(go1 / go0 * 1.07 - 1)))
check(maxdev < 1e-9, f"D0 transform unit test: a distance rescale leaves g_bar invariant and scales g_obs by 1/s (max deviation {maxdev:.1e})")
def bad_dir(g, s):       # mutation: distance rescaled in the wrong direction for R only
    h = dict(g); h["Rm"] = g["Rm"] / s; return h
gb0, go0 = gbar_gobs(gals[0]); gb1, go1 = gbar_gobs(bad_dir(gals[0], 1.07))
check(np.max(np.abs(gb1 / gb0 - 1)) > 0.05, "D0m the unit test FAILS for a wrongly-implemented transform (the test has teeth)")

nHF = sum(g["fD"] == 1 for g in gals)
fdc = {k: int(sum(g["fD"] == k for g in gals)) for k in (1, 2, 3, 4, 5)}
print("   distance methods: " + ", ".join(f"f_D={k}: {v}" for k, v in fdc.items()) + f"   (f_D = 1 is Hubble flow at H0 = 73; {nHF} of 175 galaxies)")
res["fD_counts"] = fdc
base = a0_hat
Pbase = Profile(gals, IF_alpha1)
def base_fit():
    return parabola_min(A0GRID, Pbase.scan(A0GRID, SIGI))[0]
base_grid = base_fit()          # baseline on the SAME 61-pt grid used for the variants (removes grid-refinement offsets)
pert = {}
def run(name, tf):
    a, s = parabola_min(A0GRID, Profile([tf(g) for g in gals], IF_alpha1).scan(A0GRID, SIGI))
    pert[name] = dict(a0=a, dln=math.log(a / base_grid)); print(f"   {name:<62}a0_hat = {a*1e10:.4f}e-10   d ln a0 = {100*math.log(a/base_grid):+6.2f}%")
sH = H0_SHOES / H0_PLANCK
run("all distances x 1.05", lambda g: transform(g, dist_scale=1.05))
run("all distances x 0.95", lambda g: transform(g, dist_scale=0.95))
run("all distances x 1.10", lambda g: transform(g, dist_scale=1.10))
run("all distances x 0.90", lambda g: transform(g, dist_scale=0.90))
run(f"Hubble-flow (f_D=1) distances x {sH:.4f} (H0 73 -> 67.4)", lambda g: transform(g, dist_scale=sH if g["fD"] == 1 else 1.0))
run(f"ALL distances x {sH:.4f} (ladder biased if H0 = 67.4)", lambda g: transform(g, dist_scale=sH))
run("Hubble-flow (f_D=1) distances x 0.95", lambda g: transform(g, dist_scale=0.95 if g["fD"] == 1 else 1.0))
run("Hubble-flow (f_D=1) distances x 1.05", lambda g: transform(g, dist_scale=1.05 if g["fD"] == 1 else 1.0))
run("gas mass x 1.10", lambda g: transform(g, gas_scale=1.10))
run("gas mass x 0.90", lambda g: transform(g, gas_scale=0.90))
run("gas mass x 1.20", lambda g: transform(g, gas_scale=1.20))
run("inclination + 1 sigma_i (coherent, per-galaxy e_Inc)", lambda g: transform(g, dinc_deg=+g["einc"]))
run("inclination - 1 sigma_i (coherent, per-galaxy e_Inc)", lambda g: transform(g, dinc_deg=-g["einc"]))
res["perturbations"] = pert
d105 = pert["all distances x 1.05"]["dln"]; lo_, hi_ = -2 * math.log(1.05), -math.log(1.05)
check(lo_ - 0.01 < d105 < hi_ + 0.01, f"D1 a global distance rescale x1.05 shifts a0 by {100*d105:+.2f}%, inside the analytic bracket [{100*lo_:.2f}%, {100*hi_:.2f}%] (deep-MOND a0 ~ D^-2, Newtonian ~ D^-1)")
check(pert["all distances x 0.95"]["dln"] > 0 > pert["gas mass x 1.10"]["dln"], "D2 signs: smaller distances -> larger a0; more gas mass -> smaller a0 (a0 ~ 1/M_gas where the gas anchors it)")
check(abs(pert[f"ALL distances x {sH:.4f} (ladder biased if H0 = 67.4)"]["dln"]) > abs(pert[f"Hubble-flow (f_D=1) distances x {sH:.4f} (H0 73 -> 67.4)"]["dln"]),
      "D3 rescaling ALL distances moves a0 more than rescaling only the Hubble-flow subset")
pi_, pm_ = pert["inclination + 1 sigma_i (coherent, per-galaxy e_Inc)"]["dln"], pert["inclination - 1 sigma_i (coherent, per-galaxy e_Inc)"]["dln"]
check(pi_ * pm_ < 0, f"D4 the coherent inclination shift moves a0 in OPPOSITE directions for +/-1 sigma_i ({100*pi_:+.1f}%, {100*pm_:+.1f}%); an earlier version with an edge-on singularity moved both down and was fixed")

# H0-coupled distances for each IF (Upsilon free): a0_obs in the 'Planck world' where SPARC's Hubble-flow (or all) distances are rescaled by 73/67.4
print("\n   H0-coupled a0_obs per IF (Upsilon free): baseline / Hubble-flow distances x 73/67.4 / ALL distances x 73/67.4   [1e-10 m/s^2]")
h0c = {}
for nm, F in IFS.items():
    r_ = {}
    for lab, tf in (("baseline", lambda g: g), ("HF only", lambda g: transform(g, dist_scale=sH if g["fD"] == 1 else 1.0)), ("all distances", lambda g: transform(g, dist_scale=sH))):
        r_[lab] = parabola_min(A0GRID, Profile([tf(g) for g in gals], F).scan(A0GRID, SIGI))[0]
    h0c[nm] = r_
    print(f"   {nm:<26}{r_['baseline']*1e10:>9.4f}{r_['HF only']*1e10:>12.4f}{r_['all distances']*1e10:>16.4f}   (d ln: {100*math.log(r_['HF only']/r_['baseline']):+.1f}%, {100*math.log(r_['all distances']/r_['baseline']):+.1f}%)")
res["H0_coupled"] = h0c
check(all(v["all distances"] < v["HF only"] < v["baseline"] for v in h0c.values()), "H1 for every IF: a0_obs(all distances x 1.083) < a0_obs(HF only) < a0_obs(baseline)")

# ---------------------------------------------------------------------------------------------- K the record's headline comparison under other IFs
print("\nK  the record's headline comparison (framework Z_F vs Milgrom 2 pi vs Verlinde 6 ...) re-run with each IF: d chi2 of the point a0 = c H_eff/Z relative to the IF's own best fit (Upsilon free);")
print("   deflated sigma = sqrt(d chi2 / (N_pts/N_gal = 19.3)) as in the record's P3 table.  H0 = 67.4.")
cH0_, cHL_ = c_si * H_si(67.4), c_si * H_si(67.4) * math.sqrt(OM_L)
HYPZ = [("F 5.789", Z_F), ("V 6", 6.0), ("M 2pi", Z_M), ("N 3sqrt3", 3 * math.sqrt(3)), ("P 4.943", 0.5 + math.pi * math.sqrt(2))]
kres = {}
print(f"   {'IF':<26}{'a0_hat':>8} | " + "".join(f"{'tot '+n:>14}" for n, _ in HYPZ) + " | " + "".join(f"{'Lam '+n:>14}" for n, _ in HYPZ))
for nm, F in IFS.items():
    P = Profile(gals, F); ah = mat["Upsilon free 0.05-3 (record)"][nm]["a0"]; cmin = P.chi2(ah, SIGI)[0]
    row = {}
    for foot, cH in (("tot", cH0_), ("Lam", cHL_)):
        for n, Z in HYPZ:
            d = P.chi2(cH / Z, SIGI)[0] - cmin
            row[f"{foot} {n}"] = dict(a0=cH / Z, dchi2=float(d), nsig=float(math.sqrt(max(d, 0) / infl ** 2)), sign=1 if cH / Z > ah else -1)
    kres[nm] = row
    print(f"   {nm:<26}{ah/U:>8.4f} | " + "".join(f"{row['tot '+n]['sign']*row['tot '+n]['nsig']:>+13.2f}s" for n, _ in HYPZ) + " | " + "".join(f"{row['Lam '+n]['sign']*row['Lam '+n]['nsig']:>+13.2f}s" for n, _ in HYPZ))
res["K_headline"] = kres
print("   (signed: + = the hypothesis's a0 lies ABOVE the IF's best fit)")
a1 = kres["alpha1 (record kernel)"]; ra = kres["RAR (MLS16)"]
check(a1["Lam F 5.789"]["dchi2"] < a1["Lam M 2pi"]["dchi2"], "K1 with the record's alpha1 kernel the SPARC profile prefers the framework Z_F over Milgrom's 2 pi on the rho_Lambda footing (the record's P3-KEY)")
check(ra["Lam M 2pi"]["dchi2"] < ra["Lam F 5.789"]["dchi2"], "K2 with the RAR IF the ORDER FLIPS on the rho_Lambda footing: 2 pi fits better than Z_F (the record's P3-KEY is kernel-conditional)")

def half(a, b): return 0.5 * abs(pert[a]["dln"] - pert[b]["dln"])
budget = {
    "interpolating function, data-preferred pair (RAR vs simple, Upsilon free)": 0.5 * abs(math.log(aF["RAR (MLS16)"] / aF["simple"])),
    "interpolating function, all four IFs (half-range, Upsilon free)": 0.5 * math.log(max(aF.values()) / min(aF.values())),
    "Upsilon treatment (free vs fixed 0.5, RAR IF; half-range)": 0.5 * abs(math.log(mat["Upsilon fixed 0.5 (bulge 0.7)"]["RAR (MLS16)"]["a0"] / mat["Upsilon free 0.05-3 (record)"]["RAR (MLS16)"]["a0"])),
    "global distance scale +-5% (calibrator zero point)": half("all distances x 1.05", "all distances x 0.95"),
    "Hubble-flow subset +-5%": half("Hubble-flow (f_D=1) distances x 1.05", "Hubble-flow (f_D=1) distances x 0.95"),
    "gas mass +-10% (HI calibration, H2, helium)": half("gas mass x 1.10", "gas mass x 0.90"),
    "coherent inclination bias +-1 sigma_i (upper bound)": half("inclination + 1 sigma_i (coherent, per-galaxy e_Inc)", "inclination - 1 sigma_i (coherent, per-galaxy e_Inc)"),
    "galaxy-class heterogeneity (gas- vs star-dominated, cleanest fit; half-range)": res["class_split_clean"]["half_range_ln"],
}
print("\n   a0 systematics measured here (half-ranges of the perturbations above; d ln a0; NOT applied to anything):")
for k, v in budget.items(): print(f"     {k:<70}{100*v:6.2f}%")
res["budget"] = budget

# ---------------------------------------------------------------------------------------------- M mocks
print("\nM  mocks from the SPARC baryon content (true Upsilon ~ 0.5 x lognormal 0.1 dex, scatter 0.06 dex, SPARC errV); 16 mocks per truth")
rng = np.random.default_rng(7)
def make_mock(F_true, a_true, rng):
    out = []
    for g in gals:
        U = 0.5 * 10 ** rng.normal(0, 0.10)
        Vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2
        gb = Vb2 * 1e6 / g["Rm"]; okp = gb > 0
        go = np.where(okp, F_true(np.where(okp, gb, 1.0), a_true), np.nan)
        sig = (g["eV"] / g["Vobs"]) * 2 / math.log(10)
        lg = np.log10(go) + rng.normal(0, 1, len(go)) * np.sqrt(sig ** 2 + 0.06 ** 2)
        h = dict(g); V = np.sqrt(10 ** lg * g["Rm"]) / 1e3
        h["Vobs"] = np.where(np.isfinite(V) & (V > 0), V, g["Vobs"]); h["eV"] = g["eV"] / g["Vobs"] * h["Vobs"]
        out.append(h)
    return out
NM = 16
mres = {}
for truth, Ft in (("RAR", IF_rar), ("alpha1", IF_alpha1)):
    bR, bA, dC = [], [], []
    for k in range(NM):
        mg = make_mock(Ft, 1.0e-10, rng)
        PR, PA = Profile(mg, IF_rar), Profile(mg, IF_alpha1)
        cR, cA = PR.scan(A0GRID, 0.06), PA.scan(A0GRID, 0.06)
        bR.append(math.log(parabola_min(A0GRID, cR)[0] / 1e-10)); bA.append(math.log(parabola_min(A0GRID, cA)[0] / 1e-10))
        dC.append(cA.min() - cR.min())
    bR, bA, dC = map(np.array, (bR, bA, dC))
    mres[truth] = dict(bias_fit_RAR=float(bR.mean()), bias_fit_alpha1=float(bA.mean()), sem=float(bR.std(ddof=1) / math.sqrt(NM)), dchi2_alpha1_minus_RAR_mean=float(dC.mean()), dchi2_min=float(dC.min()), dchi2_max=float(dC.max()))
    print(f"   truth {truth:<7}: fit with RAR -> bias {100*bR.mean():+6.2f}% (+-{100*bR.std(ddof=1)/math.sqrt(NM):.2f});  fit with alpha1 -> bias {100*bA.mean():+6.2f}%;  chi2(alpha1)-chi2(RAR) = {dC.mean():+.0f} [{dC.min():+.0f}, {dC.max():+.0f}]")
res["mocks"] = mres
check(abs(mres["RAR"]["bias_fit_RAR"]) < 3 * mres["RAR"]["sem"] + 0.005, "M1 estimator unbiased when the fitted kernel is the true one (RAR truth, RAR fit)")
check(abs(mres["alpha1"]["bias_fit_alpha1"]) < 3 * mres["alpha1"]["sem"] + 0.005, "M2 estimator unbiased when the fitted kernel is the true one (alpha1 truth, alpha1 fit)")
check(mres["RAR"]["bias_fit_alpha1"] > 0.10 and mres["alpha1"]["bias_fit_RAR"] < -0.10, "M3 a wrong kernel biases a0 by >10% in the expected direction (alpha1 fit to RAR truth: high; RAR fit to alpha1 truth: low)")
check(mres["RAR"]["dchi2_alpha1_minus_RAR_mean"] > 0 > mres["alpha1"]["dchi2_alpha1_minus_RAR_mean"], "M4 the chi2 preference follows the truth: alpha1 - RAR chi2 is >0 for RAR-truth mocks and <0 for alpha1-truth mocks")
real_shift = math.log(aF["alpha1 (record kernel)"] / aF["RAR (MLS16)"])
print(f"   real data: alpha1/RAR a0 ratio = {aF['alpha1 (record kernel)']/aF['RAR (MLS16)']:.3f} (ln = {real_shift:+.3f}); RAR-truth mocks predict ln = {mres['RAR']['bias_fit_alpha1']-mres['RAR']['bias_fit_RAR']:+.3f}; alpha1-truth mocks predict {mres['alpha1']['bias_fit_alpha1']-mres['alpha1']['bias_fit_RAR']:+.3f}")
print(f"   real data: chi2(alpha1)-chi2(RAR) = {dch:+.0f}: RAR-truth mocks give {mres['RAR']['dchi2_alpha1_minus_RAR_mean']:+.0f}, alpha1-truth mocks {mres['alpha1']['dchi2_alpha1_minus_RAR_mean']:+.0f}")

print(f"\n  {sum(ok)}/{len(ok)} checks held.   ({time.time()-t0:.0f} s)")
json.dump(res, open("v02_results.json", "w"), indent=1, default=float)
sys.exit(0 if all(ok) else 1)
