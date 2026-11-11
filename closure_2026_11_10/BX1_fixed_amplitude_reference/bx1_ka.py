#!/usr/bin/env python3
"""BX1 known answers on the simulations (FROZEN_CRITERIA.md 21e1c07e9a, section 3) and MUTATE MB2 (section 8).
  KA1  the copy, options off, CFG596's V-L settings, against CFG530 S0_L100_N256 (STRICT 1e-5); CFG596's own VLs reported.
  KA2  fixed run fA (seed 7101, 256^3): (a) the IC field's binned power / bin-averaged input = 1 to 1e-6 below k_Nyq / 2;
       (b) z_i r(k) = P / (D_i^2 P_lin(k_bin)) within +-0.02 of r_bin at k <= 0.5, rms(r / r_bin - 1) <= 1/5 of the random runs'.
       The same (b) on every 512^3 production run present (a failed run is not spliced).
  KA3  256^3 fixed pairs A, B against random R1..R5: (a) chi^2 of pair A against the random mean (Gaussian mode error with the
       pooled excess f), p >= 0.01 at z 1, 0.5, 0; (b) rms_k<=0.3 (PbarA / PbarB - 1) <= rms(sqrt(2) s / <P>) / 5.
  MB2  (MUTATE) single fixed runs A / B against the true pairs, z 0, k <= 0.5: rms(A / B - 1) >= 1.5 rms(PbarA / PbarB - 1).
The engine copy is imported for its own P_lin0 (no run). Reads ../_external_data/bx1_work, CFG530's and CFG596's stored runs.
  python3 bx1_ka.py     -> bx1_ka.json, bx1_ka.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, glob, importlib.util
os.environ["CFG596_RELIEF"] = "0"; os.environ["CFG596_THREADS"] = "1"; sys.dont_write_bytecode = True
import numpy as np
from scipy.stats import chi2 as CH
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data")); W = os.path.join(EXT, "bx1_work")
_sp = importlib.util.spec_from_file_location("bx1_pm_lib", os.path.join(HERE, "bx1_pm.py")); ENG = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(ENG)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def run(job):
    f = glob.glob(os.path.join(W, job, "bx1_*.json")); return json.load(open(f[0])) if f else None
ZS = ("z1", "z0.5", "z0")
RES = dict(lane="BX1", part="known answers on the simulations", criteria="21e1c07e9a", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, MUTATE={})

# ------------------------------------------------------------------ KA1
def cmp(a, b, kmax):
    out = {}
    for z in ("zi",) + ZS:
        ka = np.array(a["snap"][z]["k"]); m = ka <= kmax * (1 + 1e-9)
        dP = np.abs(np.array(b["snap"][z]["P"])[m] / np.array(a["snap"][z]["P"])[m] - 1)
        out[z] = dict(maxrelP=float(dP.max()), relsig8=float(abs(b["snap"][z]["sigma8"] / a["snap"][z]["sigma8"] - 1)))
    return out
ka1 = run("KA1")
if ka1 and "z0" in ka1["snap"]:
    ref = json.load(open(glob.glob(os.path.join(EXT, "cfg530_work", "runs", "S0_L100_N256", "cfg527_*.json"))[0]))
    vls = json.load(open(glob.glob(os.path.join(EXT, "cfg596_work", "VLs", "cfg596_*.json"))[0]))
    khi = math.pi * 256 / (4 * 100.0); c = cmp(ref, ka1, khi); cv = cmp(vls, ka1, 1e9)
    mp = max(v["maxrelP"] for v in c.values()); ms = max(v["relsig8"] for v in c.values())
    RES["KA"]["KA1"] = dict(vs_CFG530=c, max_relP=mp, max_relsig8=ms, pass_=bool(mp <= 1e-5 and ms <= 1e-5), vs_CFG596_VLs_reported=cv,
                            vs_VLs_max=max(max(v["maxrelP"], v["relsig8"]) for v in cv.values()))
    P(f"KA1 copy (options off) vs CFG530 S0_L100_N256 (k <= {khi:.2f}): max|dP/P| {mp:.2e}, max|ds8/s8| {ms:.2e} -> {'PASS' if RES['KA']['KA1']['pass_'] else 'FAIL'};"
      f"  vs CFG596's VLs (all k, reported): max {RES['KA']['KA1']['vs_VLs_max']:.2e}")
else: P("KA1: run missing or incomplete")

# ------------------------------------------------------------------ KA2
def zi_dev(J):
    c = J["ic_check"]; zi = J["snap"]["zi"]; k = np.array(zi["k"]); kc = np.array(c["k"])
    assert len(k) == len(kc) and np.max(np.abs(k / kc - 1)) < 1e-5, "bins differ"
    r = np.array(zi["P"]) / (zi["D"] ** 2 * ENG.P_lin0(k)); rb = np.array(c["r_bin"]); m = k <= 0.5
    return k, r, rb, m, (r / rb - 1)
RAND = [run(f"r{i}") for i in range(1, 6)]; RAND = [J for J in RAND if J and "z0" in J["snap"]]
fA = run("fA")
if fA and len(RAND) == 5:
    c = fA["ic_check"]; kc = np.array(c["k"]); kny = math.pi * fA["np"] / fA["L"]; mm = kc < kny / 2
    da = float(np.max(np.abs(np.array(c["ratio_to_binavg"])[mm] - 1)))
    k, r, rb, m, d = zi_dev(fA); dmax = float(np.max(np.abs(d[m]))); rms_f = float(np.sqrt(np.mean(d[m] ** 2)))
    rms_r = float(np.sqrt(np.mean(np.concatenate([zi_dev(J)[4][zi_dev(J)[3]] ** 2 for J in RAND]))))
    ra = [float(np.max(np.abs(np.array(J["ic_check"]["ratio_to_binavg"])[mm] - 1))) for J in RAND]
    ok = bool(da <= 1e-6 and dmax <= 0.02 and rms_f <= rms_r / 5)
    RES["KA"]["KA2"] = dict(a_max_IC_ratio_dev=da, b_max_zi_dev=dmax, b_rms_fixed=rms_f, b_rms_random=rms_r, random_IC_ratio_dev_max=ra, pass_=ok,
                            zi_rows=dict(k=k[m].tolist(), r=r[m].tolist(), r_bin=rb[m].tolist()), r_bin_max_dev=float(np.max(np.abs(rb[m] - 1))))
    P(f"KA2 fixed fA: (a) IC power / input, max|-1| below k_Nyq/2 = {da:.1e} (random runs: {min(ra):.2f} to {max(ra):.2f}); (b) z_i r / r_bin at k <= 0.5: "
      f"max|-1| {dmax:.4f}, rms {rms_f:.4f} against the random runs' {rms_r:.4f} (ratio {rms_r / max(rms_f, 1e-30):.1f}); r_bin itself within {RES['KA']['KA2']['r_bin_max_dev']:.4f} of 1 -> {'PASS' if ok else 'FAIL'}")
    P("     z_i r(k) fixed: " + ", ".join(f"{a:.3f}: {b:.4f}" for a, b in zip(k[m], r[m])))
    P("     z_i r(k) r1   : " + ", ".join(f"{a:.3f}: {b:.4f}" for a, b in zip(zi_dev(RAND[0])[0][m], zi_dev(RAND[0])[1][m])))
    for job in ("pA", "pAi", "pB", "pBi"):
        J = run(job)
        if J and "zi" in J["snap"] and "ic_check" in J:
            k2, r2, rb2, m2, d2 = zi_dev(J); c2 = J["ic_check"]; kc2 = np.array(c2["k"]); mm2 = kc2 < math.pi * J["np"] / J["L"] / 2
            ok2 = bool(np.max(np.abs(np.array(c2["ratio_to_binavg"])[mm2] - 1)) <= 1e-6 and np.max(np.abs(d2[m2])) <= 0.02)
            RES["KA"][f"KA2_{job}"] = dict(max_zi_dev=float(np.max(np.abs(d2[m2]))), rms=float(np.sqrt(np.mean(d2[m2] ** 2))), pass_=ok2, complete=bool("z0" in J["snap"]))
            P(f"KA2 on production {job}: z_i max|r / r_bin - 1| {RES['KA'][f'KA2_{job}']['max_zi_dev']:.4f}, rms {RES['KA'][f'KA2_{job}']['rms']:.4f} -> {'PASS' if ok2 else 'FAIL'}"
              + ("" if RES["KA"][f"KA2_{job}"]["complete"] else " (run not finished)"))
else: P("KA2: runs missing")

# ------------------------------------------------------------------ KA3 and MB2
J4 = {j: run(j) for j in ("fA", "fAi", "fB", "fBi")}
if all(J and "z0" in J["snap"] for J in J4.values()) and len(RAND) == 5:
    k = np.array(J4["fA"]["snap"]["z0"]["k"]); m5 = k <= 0.5; m3 = k <= 0.3; wt = np.array(J4["fA"]["ic_check"]["weight"])
    ka3 = {}; mb2 = {}
    for z in ZS:
        Pz = {j: np.array(J["snap"][z]["P"]) for j, J in J4.items()}; R = np.array([J["snap"][z]["P"] for J in RAND])
        pA, pB = (Pz["fA"] + Pz["fAi"]) / 2, (Pz["fB"] + Pz["fBi"]) / 2; mr = R.mean(0); s = R.std(0, ddof=1)
        sG = mr * np.sqrt(2 / wt); f = max(1.0, float(np.sqrt(np.mean((s[m5] / sG[m5]) ** 2))))
        def chi(pp):
            x = (pp[m5] - mr[m5]) / (f * sG[m5] / math.sqrt(5)); c2 = float(np.sum(x ** 2)); return c2, float(CH.sf(c2, int(m5.sum()))), x
        cA, pvA, xA = chi(pA); cB, pvB, xB = chi(pB)
        rho_pair = float(np.sqrt(np.mean((pA[m3] / pB[m3] - 1) ** 2))); rho_rand = float(np.sqrt(np.mean((math.sqrt(2) * s[m3] / mr[m3]) ** 2)))
        ka3[z] = dict(N_bins=int(m5.sum()), f_excess=f, chi2_A=cA, p_A=pvA, chi2_B=cB, p_B=pvB, x_A=xA.tolist(), rho_pair_k03=rho_pair, rho_rand_k03=rho_rand,
                      a_pass=bool(pvA >= 0.01), b_pass=bool(rho_pair <= rho_rand / 5), pair_over_rand_k05=(pA[m5] / mr[m5]).tolist(), k05=k[m5].tolist(),
                      rand_frac_sd_k05=(s[m5] / mr[m5]).tolist(), pairA_over_pairB_k05=(pA[m5] / pB[m5]).tolist())
        rs = float(np.sqrt(np.mean((Pz["fA"][m5] / Pz["fB"][m5] - 1) ** 2))); rp = float(np.sqrt(np.mean((pA[m5] / pB[m5] - 1) ** 2)))
        mb2[z] = dict(rho_single=rs, rho_pairs=rp, ratio=rs / max(rp, 1e-30))
        P(f"KA3 {z}: (a) pair A vs the random mean: chi2 {cA:.2f} / {int(m5.sum())} bins, p {pvA:.3f} (pair B p {pvB:.3f}; excess f {f:.2f}) -> {'PASS' if pvA >= 0.01 else 'FAIL'};"
          f"  (b) rms_k<=0.3 PbarA/PbarB-1 = {rho_pair:.2e} against random {rho_rand:.3f} (x{rho_rand / max(rho_pair, 1e-30):.0f}) -> {'PASS' if rho_pair <= rho_rand / 5 else 'FAIL'};"
          f"  MB2 single A/B {rs:.2e} vs pairs {rp:.2e} (x{rs / max(rp, 1e-30):.1f})")
        P("     pair A / random mean (k <= 0.5): " + ", ".join(f"{a:.3f}: {b:.3f}" for a, b in zip(k[m5], pA[m5] / mr[m5])) + "   random sd: " + ", ".join(f"{b:.3f}" for b in (s[m5] / mr[m5])))
    RES["KA"]["KA3"] = dict(rows=ka3, pass_=bool(all(v["a_pass"] and v["b_pass"] for v in ka3.values())))
    RES["MUTATE"]["MB2"] = dict(rows=mb2, bites=bool(mb2["z0"]["ratio"] >= 1.5))
    P(f"KA3 -> {'PASS' if RES['KA']['KA3']['pass_'] else 'FAIL'};  MB2 (MUTATE, z 0): ratio {mb2['z0']['ratio']:.1f} -> {'bites' if RES['MUTATE']['MB2']['bites'] else 'DOES NOT BITE'}")
    # ---------------- AMENDMENT A1 (4af7a4b905, post hoc): KA3 (a') band-averaged Welch t; MB2' line 1.1 at every z
    def band(J, z, kmax):
        s = J["snap"][z]; kk = np.array(s["k"]); mm = kk <= kmax; return float(np.mean((np.array(s["P"]) / (s["D"] ** 2 * ENG.P_lin0(kk)))[mm]))
    def welch(pairs, rands, z, kmax):
        a = np.array([0.5 * (band(x, z, kmax) + band(y, z, kmax)) for x, y in pairs]); b = np.array([band(J, z, kmax) for J in rands])
        se = math.sqrt(b.var(ddof=1) / len(b) + a.var(ddof=1) / len(a)); return dict(pairs=a.tolist(), random=b.tolist(), diff=float(a.mean() - b.mean()), se=se, t=float((a.mean() - b.mean()) / se))
    pr = [(J4["fA"], J4["fAi"]), (J4["fB"], J4["fBi"])]; a1 = {}
    for z in ZS:
        a1[z] = dict(k05=welch(pr, RAND, z, 0.5), k03=welch(pr, RAND, z, 0.3)); a1[z]["pass"] = bool(abs(a1[z]["k05"]["t"]) <= 3)
        P(f"KA3(a') [A1] {z}: band k<=0.5 pairs {np.round(a1[z]['k05']['pairs'], 4).tolist()} vs random mean {np.mean(a1[z]['k05']['random']):.4f} (sd {np.std(a1[z]['k05']['random'], ddof=1):.4f}): "
          f"diff {a1[z]['k05']['diff']:+.4f} +- {a1[z]['k05']['se']:.4f}, t {a1[z]['k05']['t']:+.2f} -> {'PASS' if a1[z]['pass'] else 'FAIL'};  k<=0.3: diff {a1[z]['k03']['diff']:+.4f} +- {a1[z]['k03']['se']:.4f}, t {a1[z]['k03']['t']:+.2f}")
    RES["KA"]["KA3a_A1"] = dict(rows=a1, pass_=bool(all(v["pass"] for v in a1.values())))
    RES["MUTATE"]["MB2_A1"] = dict(ratios={z: mb2[z]["ratio"] for z in ZS}, bites=bool(all(mb2[z]["ratio"] >= 1.1 for z in ZS)))
    P(f"KA3(a') [A1] -> {'PASS' if RES['KA']['KA3a_A1']['pass_'] else 'FAIL'};  MB2' [A1] ratios " + " / ".join(f"{mb2[z]['ratio']:.2f}" for z in ZS) + f" -> {'bites' if RES['MUTATE']['MB2_A1']['bites'] else 'DOES NOT BITE'}")
    # extended set (A1 section 5, reported only)
    EXT_R = [J for J in (run(f"r{i}") for i in range(6, 11)) if J and "z0" in J["snap"]]; EXT_P = [(run(f"f{c}"), run(f"f{c}i")) for c in "CD"]
    EXT_P = [(x, y) for x, y in EXT_P if x and y and "z0" in x["snap"] and "z0" in y["snap"]]
    if EXT_R or EXT_P:
        RES["KA"]["KA3a_A1_extended"] = {z: welch(pr + EXT_P, RAND + EXT_R, z, 0.5) for z in ZS}
        P(f"KA3(a') extended (reported; {len(pr + EXT_P)} pairs, {len(RAND + EXT_R)} random): " + "; ".join(f"{z} t {v['t']:+.2f} (diff {v['diff']:+.4f} +- {v['se']:.4f})" for z, v in RES["KA"]["KA3a_A1_extended"].items()))
else: P("KA3 / MB2: runs missing")
json.dump(RES, open(os.path.join(HERE, "bx1_ka.json"), "w"), indent=1)
open(os.path.join(HERE, "bx1_ka.out"), "w").write("\n".join(OUT) + "\n")
