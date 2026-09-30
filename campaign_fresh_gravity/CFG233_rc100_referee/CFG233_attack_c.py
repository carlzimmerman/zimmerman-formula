"""CFG233 attack (c): the expected-slope computation and the slope-difference uncertainty."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG233_common import *

start("CFG233_attack_c")
d = load_rc100(); z = d["z"]; n = len(z)
R = {}
B = 10000
print("=== c1: expected slopes by kernel and footing (inversion definition) and the hold-g_bar definition")
tab = {}
for foot in ("canonical", "alt"):
    for kern in ("nu_mono", "P2", "simple"):
        f_, r_ = delta_pair(d["D"], d["gbar"], z, kern, foot)
        bs = boot_ts(z, [f_, r_], 4000, SEED_MAIN)
        ex = expected_slopes(d["gobs"], z, kern, foot)
        # hold-g_bar definition: baryons as observed; law T's g_obs re-predicted; D = nu_T(y_T)
        hold = {}
        for T in ("flat", "rival"):
            nuT = KERNELS[kern](d["gbar"] / a0_of(T, z, foot))
            hold[T] = (ts(z, delta_of(nuT, d["gbar"], z, "flat", kern, foot)), ts(z, delta_of(nuT, d["gbar"], z, "rival", kern, foot)))
        sf, sr = ts(z, f_), ts(z, r_); sdf, sdr = bs[0].std(), bs[1].std()
        row = dict(obs_flat=sf, obs_rival=sr, sd_flat=float(sdf), sd_rival=float(sdr), s_R=ex["rival"][0], m_sF=ex["flat"][1],
                   T_flat_vs_R=(sf - ex["rival"][0]) / sdf, T_rival_vs_R=sr / sdr, T_flat_vs_F=sf / sdf, T_rival_vs_F=(sr - ex["flat"][1]) / sdr,
                   hold_s_R=hold["rival"][0], hold_m_sF=hold["flat"][1])
        row["T_flat_vs_R_hold"] = (sf - hold["rival"][0]) / sdf; row["T_rival_vs_F_hold"] = (sr - hold["flat"][1]) / sdr
        tab[f"{foot}/{kern}"] = row
        print(f"  {foot:9}/{kern:7}: obs {sf:+.3f}/{sr:+.3f} | s_R {row['s_R']:+.4f} (hold-g_bar {row['hold_s_R']:+.4f}) -s_F {row['m_sF']:+.4f} (hold {row['hold_m_sF']:+.4f}) | tension flat-slope vs rival-exp {row['T_flat_vs_R']:+.1f} (hold {row['T_flat_vs_R_hold']:+.1f}), rival-slope vs 0 {row['T_rival_vs_R']:+.1f}")
R["kernels"] = tab
ref = tab["canonical/nu_mono"]
worst = max(max(abs(v["T_flat_vs_R"] - ref["T_flat_vs_R"]), abs(v["T_rival_vs_R"] - ref["T_rival_vs_R"]), abs(v["T_flat_vs_R_hold"] - ref["T_flat_vs_R"])) for v in tab.values())
print(f"  largest change of either rival tension across {{P2, simple, alt, hold-g_bar}} vs the primary: {worst:.2f} sigma; line: > 1 sigma -> 'not robust to the expected-slope definition': {'NOT ROBUST' if worst > 1 else 'robust'}")
R["worst_tension_change"] = worst
# deep-MOND ceiling
ceil = ts(z, 0.5 * np.log10(E_of_z(z)))
print(f"  analytic deep-MOND ceiling 0.5 log10 E(z) slope on the sample's z: {ceil:+.4f} (observed-sample expected s_R {ref['s_R']:+.4f}); ceiling/sample = {ceil/ref['s_R']:.2f}")
R["ceiling"] = ceil

print("\n=== c1: expected slopes vs mass range and g_bar distribution (nu_mono canonical; subsets defined on the observed sample)")
sub_res = {}
def exp_on(mask, label):
    zz = z[mask]
    if mask.sum() < 8 or len(np.unique(zz)) < 3:
        print(f"  {label}: n={mask.sum()} too small"); return
    ex = expected_slopes(d["gobs"][mask], zz)
    f_, r_ = delta_pair(d["D"][mask], d["gbar"][mask], zz)
    sub_res[label] = dict(n=int(mask.sum()), s_R=ex["rival"][0], m_sF=ex["flat"][1], obs_flat=ts(zz, f_), obs_rival=ts(zz, r_))
    print(f"  {label:22}: n={mask.sum():3d} s_R {ex['rival'][0]:+.4f}  -s_F {ex['flat'][1]:+.4f}  | obs flat {ts(zz,f_):+.4f} rival {ts(zz,r_):+.4f}")
for nm, key in (("logM", d["logM"]), ("g_bar", d["gbar"])):
    q = np.percentile(key, [33.3, 66.7])
    exp_on(key <= q[0], f"{nm} tercile 1 (low)"); exp_on((key > q[0]) & (key <= q[1]), f"{nm} tercile 2"); exp_on(key > q[1], f"{nm} tercile 3 (high)")
exp_on(d["gbar"] < 3 * A0["canonical"], "g_bar < 3 a0"); exp_on(d["gbar"] < A0["canonical"], "g_bar < a0")
R["subsets"] = sub_res

print("\n=== c2: joint bootstrap of (observed slope - expected slope) with the expected slope recomputed on each resample (N=10000, seed 233)")
f_, r_ = delta_pair(d["D"], d["gbar"], z)
gbR = invert_gbar(d["gobs"], a0_of("rival", z), nu_mono); DR = d["gobs"] / gbR
gbF = invert_gbar(d["gobs"], a0_of("flat", z), nu_mono); DF = d["gobs"] / gbF
dfR = delta_of(DR, gbR, z, "flat"); drF = delta_of(DF, gbF, z, "rival")   # per-galaxy expected deltas
bs = boot_ts(z, [f_, r_, dfR, drF], B, SEED_MAIN)
diff1 = bs[0] - bs[2]      # flat slope minus its rival-true expectation
diff2 = bs[1] - bs[3]      # rival slope minus its flat-true expectation
obs1 = ts(z, f_) - ts(z, dfR); obs2 = ts(z, r_) - ts(z, drF)
print(f"  flat slope - rival-true expectation: {obs1:+.4f}; SD const-expected {bs[0].std():.4f} -> {obs1/bs[0].std():+.2f} sigma; joint SD {diff1.std():.4f} -> {obs1/diff1.std():+.2f} sigma; corr(obs, exp) {np.corrcoef(bs[0], bs[2])[0,1]:+.2f}")
print(f"  rival slope - flat-true expectation: {obs2:+.4f}; SD const-expected {bs[1].std():.4f} -> {obs2/bs[1].std():+.2f} sigma; joint SD {diff2.std():.4f} -> {obs2/diff2.std():+.2f} sigma; corr {np.corrcoef(bs[1], bs[3])[0,1]:+.2f}")
print(f"  rival slope vs 0 (rival-true expectation is 0): {ts(z,r_)/bs[1].std():+.2f} sigma; flat slope vs 0: {ts(z,f_)/bs[0].std():+.2f}")
R["joint"] = dict(obs1=obs1, sd_const1=float(bs[0].std()), sd_joint1=float(diff1.std()), obs2=obs2, sd_const2=float(bs[1].std()), sd_joint2=float(diff2.std()),
                  corr1=float(np.corrcoef(bs[0], bs[2])[0, 1]), corr2=float(np.corrcoef(bs[1], bs[3])[0, 1]))

print("\n=== c3: noise propagation (Monte Carlo N=4000, seed 233): z sd 0.01, f_DM sd (RC41 median), V_c 5%, R_e 5%; observed AND expected slopes recomputed")
rc = load_rc41()
sigf = float(np.median([0.5 * (float(r["fDM_lo"]) + float(r["fDM_hi"])) for r in rc]))
rng = np.random.default_rng(SEED_MAIN)
NM = 4000
zz = np.clip(z[None] + rng.normal(0, 0.01, (NM, n)), 0.3, None)
ff = np.clip(d["f"][None] + rng.normal(0, sigf, (NM, n)), 0.01, 0.99)
Vv = d["Vc"][None] * (1 + rng.normal(0, 0.05, (NM, n))); Rr = d["Re"][None] * (1 + rng.normal(0, 0.05, (NM, n)))
go = (Vv * 1e3) ** 2 / (Rr * KPC); gb = (1 - ff) * go; DD = 1 / (1 - ff)
a = delta_of(DD, gb, zz, "flat"); b = delta_of(DD, gb, zz, "rival")
so_f = ts_batch(zz, a); so_r = ts_batch(zz, b)
gbRm = invert_gbar(go, a0_of("rival", zz), nu_mono); gbFm = invert_gbar(go, a0_of("flat", zz), nu_mono)
e1 = ts_batch(zz, delta_of(go / gbRm, gbRm, zz, "flat")); e2 = ts_batch(zz, delta_of(go / gbFm, gbFm, zz, "rival"))
print(f"  sigma_f used {sigf:.3f}. flat slope: mean {so_f.mean():+.4f} SD {so_f.std():.4f} (mean shift from noise {so_f.mean()-ts(z,f_):+.4f}); expected s_R: mean {e1.mean():+.4f} SD {e1.std():.4f}; SD of (obs - exp) {np.std(so_f-e1):.4f}")
print(f"  rival slope: mean {so_r.mean():+.4f} SD {so_r.std():.4f}; expected -s_F: mean {e2.mean():+.4f}; SD of (obs - exp) {np.std(so_r-e2):.4f}")
print("  note: this Monte Carlo treats the MAP values as if they were noisy with the RC41 posterior widths; the noise here is independent across galaxies, which the galaxy bootstrap already includes (added in quadrature it would double count); it is a check that measurement noise does not bias either slope.")
R["noise"] = dict(sigf=sigf, so_f=(float(so_f.mean()), float(so_f.std())), e1=(float(e1.mean()), float(e1.std())), so_r=(float(so_r.mean()), float(so_r.std())), e2=(float(e2.mean()), float(e2.std())),
                  sd_diff1=float(np.std(so_f - e1)), sd_diff2=float(np.std(so_r - e2)))
# analytic check of d delta / d f
hh = 1e-5
fa = d["f"]
def delta_f(fv):
    go_ = d["gobs"]; return delta_of(1 / (1 - fv), (1 - fv) * go_, z, "flat")
num = (delta_f(fa + hh) - delta_f(fa - hh)) / (2 * hh)
y = d["gbar"] / A0["canonical"]; h = 1e-4
s_loc = -(np.log10(nu_mono(y * 10 ** h)) - np.log10(nu_mono(y * 10 ** -h))) / (2 * h)
ana = (1 - s_loc) / ((1 - fa) * np.log(10))
print(f"\nanalytic d delta/d f = (1-s)/((1-f) ln10): max |num/ana - 1| = {np.max(np.abs(num/ana-1)):.2e}; s_bar = {s_loc.mean():.3f} (range {s_loc.min():.2f}-{s_loc.max():.2f}); naive independent-error overstatement sqrt(1+s^2)/(1-s) at s_bar = {math.sqrt(1+s_loc.mean()**2)/(1-s_loc.mean()):.2f}")
R["analytic"] = dict(maxrel=float(np.max(np.abs(num / ana - 1))), s_bar=float(s_loc.mean()))
savejson("CFG233_attack_c", R)
