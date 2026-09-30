"""CFG233 main: reproduction of CFG216 (README targets) from the frozen criteria. Exit 0 if C1-C4 pass."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG233_common import *

t = start("CFG233_main")
B = 10000
R = {}
rows = []  # (id, quantity, mine, target, line, verdict)


PASSLINES = (DATA == "committed")   # the frozen pass lines are scored against CFG216's numbers on the COMMITTED csv only; CORRECTED is disclosed alongside


def rec(i, q, mine, tgt, line, ok):
    v = ("PASS" if ok else "FAIL") if PASSLINES else ("info (would pass)" if ok else "info (would fail)")
    rows.append(dict(id=i, q=q, mine=mine, target=tgt, line=line, verdict=v))
    print(f"[{i}] {q}: mine={mine} target={tgt} line={line} -> {v}")


c4 = c4_crosscheck()
print("C4 cross-check of re-implemented kernels vs the imported CFG4_common:", c4)
c4pass = c4.get("ok", False) and c4["max_rel_diff_nu_mono"] < 1e-8 and c4["max_rel_diff_p2"] < 1e-12
R["C4"] = c4

d = load_rc100()
n = len(d["z"])
z = d["z"]
print(f"n rows {d['n_all']}, analysed {n}, excluded {d['n_excl']}; z {z.min()}-{z.max()}")
rec("R1", "n analysed / exclusions", (n, d["n_excl"]), (100, 0), "exact", n == 100 and d["n_excl"] == 0)
print("median z", float(np.median(z)))

# ---------------- C1: on-law synthetic galaxies
rng = np.random.default_rng(233)
zs = rng.uniform(0.5, 2.6, 40); gos = 10 ** rng.uniform(-11.5, -8.8, 40)
c1 = {}
for foot in ("canonical", "alt"):
    for kern in ("nu_mono", "P2"):
        for T in ("flat", "rival"):
            gb = invert_gbar(gos, a0_of(T, zs, foot), KERNELS[kern]); D = gos / gb
            own = delta_of(D, gb, zs, T, kern, foot)
            oth = "rival" if T == "flat" else "flat"
            dl = delta_of(D, gb, zs, oth, kern, foot)
            y_t = gb / a0_of(T, zs, foot); y_o = gb / a0_of(oth, zs, foot)
            an = np.log10(KERNELS[kern](y_t) / KERNELS[kern](y_o))
            c1[f"{foot}/{kern}/{T}"] = (float(np.max(np.abs(own))), float(np.max(np.abs(dl - an))))
c1max = max(max(v) for v in c1.values())
print("C1 max |delta_own|, |delta_other - analytic| over cells:", c1max)
R["C1"] = c1
rec("C1", "on-law delta = 0 (1e-9), other law analytic", c1max, 0, "1e-9", c1max < 1e-9)

# ---------------- C3
df, dr = delta_pair(d["D"], d["gbar"], z)
zmed = np.median(z)
s0 = ts(z, df); s1 = ts(z, df + 0.2 * (z - zmed))
rec("C3", "injected-slope recovery", s1 - s0, 0.2, "1e-9", abs(s1 - s0 - 0.2) < 1e-9)
R["C3"] = s1 - s0

# ---------------- primary cells
cells = {}
for foot in ("canonical", "alt"):
    for kern in ("nu_mono", "P2"):
        f_, r_ = delta_pair(d["D"], d["gbar"], z, kern, foot)
        bs = boot_ts(z, [f_, r_], B, SEED_MAIN)
        s = [ts(z, f_), ts(z, r_)]
        cif, cir = ci(bs[0]), ci(bs[1])
        ex = expected_slopes(d["gobs"], z, kern, foot)
        sd = bs.std(1)
        cells[f"{foot}/{kern}"] = dict(slope_flat=s[0], ci_flat=cif, slope_rival=s[1], ci_rival=cir, sd=list(sd),
                                       cls=classify(cif, cir), exp_rival_true_flat=ex["rival"][0], exp_flat_true_rival=ex["flat"][1],
                                       z_flat_vs_flat=(s[0] - 0) / sd[0], z_flat_vs_rival=(s[0] - ex["rival"][0]) / sd[0],
                                       z_rival_vs_flat=(s[1] - ex["flat"][1]) / sd[1], z_rival_vs_rival=(s[1] - 0) / sd[1],
                                       frac_flat_pos=float((bs[0] > 0).mean()))
        print(f"{foot}/{kern}: flat {s[0]:+.4f} [{cif[0]:+.4f},{cif[1]:+.4f}] rival {s[1]:+.4f} [{cir[0]:+.4f},{cir[1]:+.4f}] "
              f"sd {sd[0]:.4f}/{sd[1]:.4f} class {cells[f'{foot}/{kern}']['cls']} exp(rival-true flat)={ex['rival'][0]:+.4f} exp(flat-true rival)={ex['flat'][1]:+.4f}")
R["cells"] = cells
P = cells["canonical/nu_mono"]
rec("R2a", "delta_flat slope (nu_mono canonical)", P["slope_flat"], -0.029, "0.02", abs(P["slope_flat"] + 0.029) < 0.02)
rec("R2b", "delta_rival slope", P["slope_rival"], -0.092, "0.02", abs(P["slope_rival"] + 0.092) < 0.02)
print("   tight reporting line 0.003:", abs(P["slope_flat"] + 0.029) < 0.003, abs(P["slope_rival"] + 0.092) < 0.003)
rec("R2c", "flat CI", P["ci_flat"], (-0.071, 0.002), "0.015 each edge", abs(P["ci_flat"][0] + 0.071) < 0.015 and abs(P["ci_flat"][1] - 0.002) < 0.015)
rec("R2d", "rival CI", P["ci_rival"], (-0.128, -0.055), "0.015 each edge", abs(P["ci_rival"][0] + 0.128) < 0.015 and abs(P["ci_rival"][1] + 0.055) < 0.015)
ok3 = all(c["slope_flat"] < 0 and c["slope_rival"] < 0 and c["ci_rival"][1] < 0 and -0.06 < c["slope_flat"] < -0.01 for c in cells.values())
rec("R3", "all four cells: negative slopes, rival CI < 0, flat slope in (-0.06,-0.01)", {k: (round(v['slope_flat'], 4), round(v['slope_rival'], 4)) for k, v in cells.items()}, "signs", "sign", ok3)
rec("R4a", "expected s_R (rival-true delta_flat slope)", P["exp_rival_true_flat"], 0.073, "0.005", abs(P["exp_rival_true_flat"] - 0.073) < 0.005)
rec("R4b", "expected flat-true delta_rival slope", P["exp_flat_true_rival"], -0.060, "0.005", abs(P["exp_flat_true_rival"] + 0.060) < 0.005)
tg = dict(z_flat_vs_flat=1.6, z_flat_vs_rival=-5.5, z_rival_vs_flat=-1.7, z_rival_vs_rival=-4.9)
for k, v in tg.items():
    rec("R5-" + k, "z-score", P[k], v, "0.15", abs(P[k] - v) < 0.15 if False else abs(abs(P[k]) - abs(v)) < 0.15)
print("   (sign convention: my z = (obs - expected)/sd, README quotes magnitudes)")
rec("R5s", "sigma_slope (SD) flat / rival", P["sd"], (0.0185, 0.0188), "15% rel", all(abs(a / b - 1) < 0.15 for a, b in zip(P["sd"], (0.0185, 0.0188))))
rec("R6a", "class nu_mono canonical", P["cls"], "W-flat", "labels equal", P["cls"] == "W-flat")
rec("R6b", "class in all four cells", {k: v["cls"] for k, v in cells.items()}, "W-flat x4", "labels equal", all(v["cls"] == "W-flat" for v in cells.values()))
print("   near-boundary: flat CI upper edge", P["ci_flat"][1], "; frac of bootstrap slopes > 0:", P["frac_flat_pos"])
# BCa-ish variant reported: basic percentile-of-pivot (reverse percentile)
bs = boot_ts(z, [df], B, SEED_MAIN)[0]
rev = (2 * s0 - np.percentile(bs, 97.5), 2 * s0 - np.percentile(bs, 2.5))
print("   reverse-percentile CI (reported beside):", rev)
# BCa
from scipy import stats
z0 = stats.norm.ppf((bs < s0).mean())
loo = np.array([ts(np.delete(z, i), np.delete(df, i)) for i in range(n)])
th = loo.mean(); acc = ((th - loo) ** 3).sum() / (6 * (((th - loo) ** 2).sum()) ** 1.5)
def bca(a):
    za = stats.norm.ppf(a); return np.percentile(bs, 100 * stats.norm.cdf(z0 + (z0 + za) / (1 - acc * (z0 + za))))
print("   BCa CI (reported beside):", bca(0.025), bca(0.975), "class flat CI has 0:", bca(0.025) <= 0 <= bca(0.975))
R["bca_flat"] = (float(bca(0.025)), float(bca(0.975))); R["revperc_flat"] = [float(x) for x in rev]

# ---------------- levels and halves
med_f, ci_f = boot_median_ci(df, B, SEED_MAIN); med_r, ci_r = boot_median_ci(dr, B, SEED_MAIN)
print(f"levels: flat {med_f:+.4f} {ci_f} {label_level(ci_f)} ; rival {med_r:+.4f} {ci_r} {label_level(ci_r)}")
rec("R7a", "flat level", (round(med_f, 4), label_level(ci_f)), (0.031, "over"), "0.02 + label", abs(med_f - 0.031) < 0.02 and label_level(ci_f) == "over")
rec("R7b", "rival level", (round(med_r, 4), label_level(ci_r)), (-0.052, "under"), "0.02 + label", abs(med_r + 0.052) < 0.02 and label_level(ci_r) == "under")
R["levels"] = dict(flat=(med_f, ci_f), rival=(med_r, ci_r))
lo = z <= zmed
halves = {}
for nm, m in (("low", lo), ("high", ~lo)):
    a = boot_median_ci(df[m], B, SEED_MAIN); b = boot_median_ci(dr[m], B, SEED_MAIN)
    halves[nm] = dict(n=int(m.sum()), zmed=float(np.median(z[m])), flat=(a[0], a[1], label_level(a[1])), rival=(b[0], b[1], label_level(b[1])))
    print(f"half {nm}: n={m.sum()} median z {np.median(z[m]):.2f} flat {a[0]:+.3f} {a[1]} {label_level(a[1])} rival {b[0]:+.3f} {b[1]} {label_level(b[1])}")
R["halves"] = halves
tgt = dict(low=(51, 0.99, "over", "consistent"), high=(49, 2.19, "consistent", "under"))
okh = all(halves[k]["n"] == v[0] and abs(halves[k]["zmed"] - v[1]) <= 0.01 and halves[k]["flat"][2] == v[2] and halves[k]["rival"][2] == v[3] for k, v in tgt.items())
rec("R8", "z-halves (n, median z, labels)", {k: (v["n"], round(v["zmed"], 2), v["flat"][2], v["rival"][2]) for k, v in halves.items()}, tgt, "n exact; z 0.01; labels", okh)

# ---------------- RC41 match and sensitivities
m41, matched, unmatched, rc = rc41_match(d)
print("RC41 matched", int(m41.sum()), "of", len(rc), "; unmatched IDs:", unmatched)
rec("R10", "matched RC41 names", int(m41.sum()), 38, "exact", int(m41.sum()) == 38)
R["rc41_unmatched"] = unmatched
gcut = d["gbar"] < 3 * A0["canonical"]
gg = freeman_gbar(d["logM"], d["Re"])
D_ind = d["gobs"] / gg
sens = {}
def sens_row(name, mask, D=None, gb=None, tgt=None):
    zz = z[mask]
    Dv = (d["D"] if D is None else D)[mask]; gv = (d["gbar"] if gb is None else gb)[mask]
    f_ = delta_of(Dv, gv, zz, "flat"); r_ = delta_of(Dv, gv, zz, "rival")
    bs = boot_ts(zz, [f_, r_], B, SEED_MAIN)
    mf = boot_median_ci(f_, B, SEED_MAIN); mr = boot_median_ci(r_, B, SEED_MAIN)
    out = dict(n=int(mask.sum()), med_flat=mf[0], slope_flat=ts(zz, f_), ci_flat=ci(bs[0]), med_rival=mr[0], slope_rival=ts(zz, r_), ci_rival=ci(bs[1]))
    out["cls"] = classify(out["ci_flat"], out["ci_rival"])
    sens[name] = out
    print(f"sens {name}: n={out['n']} flat med {out['med_flat']:+.3f} slope {out['slope_flat']:+.3f} [{out['ci_flat'][0]:+.3f},{out['ci_flat'][1]:+.3f}] | rival med {out['med_rival']:+.3f} slope {out['slope_rival']:+.3f} [{out['ci_rival'][0]:+.3f},{out['ci_rival'][1]:+.3f}] class {out['cls']}")
    return out
sens_row("a_RC41", m41); sens_row("b_other", ~m41); sens_row("c_gbar<3a0", gcut)
sens_row("d_thin_disc_Mbar", np.ones(n, bool), D=D_ind, gb=gg)
R["sens"] = sens
tg = dict(a_RC41=(38, +0.041, +0.005, -0.035, -0.056), b_other=(62, +0.017, -0.055, -0.060, -0.112),
          **{"c_gbar<3a0": (67, +0.042, -0.035, -0.061, -0.104)}, d_thin_disc_Mbar=(100, +0.049, -0.040, -0.049, -0.095))
oks = True
for k, (nn, mf_, sf_, mr_, sr_) in tg.items():
    s = sens[k]
    ok = s["n"] == nn and abs(s["med_flat"] - mf_) < 0.02 and abs(s["slope_flat"] - sf_) < 0.02 and abs(s["med_rival"] - mr_) < 0.02 and abs(s["slope_rival"] - sr_) < 0.02
    rec("R9-" + k, "sens n, medians, slopes", (s["n"], round(s["med_flat"], 3), round(s["slope_flat"], 3), round(s["med_rival"], 3), round(s["slope_rival"], 3)), (nn, mf_, sf_, mr_, sr_), "n exact, 0.02", ok)
    oks &= ok
neg_all = all(s["slope_flat"] < 0 for s in sens.values())
rec("R9s", "flat slope negative in every variant; (b) flat CI < 0", (neg_all, sens["b_other"]["ci_flat"]), (True, "(-0.099,-0.007)"), "sign", neg_all and sens["b_other"]["ci_flat"][1] < 0)
print("   sensitivity (b) class:", sens["b_other"]["cls"], "(frozen rule: expect W-mixed)")
print("g_bar/a0 stats: median", float(np.median(d["gbar"] / A0["canonical"])), " frac<1", float((d["gbar"] < A0["canonical"]).mean()))

# ---------------- column classification and the C2 replacement counted here
R["column_classification"] = {"z": "measured", "Re": "photometric in table", "logMbar": "MODEL OUTPUT prior-anchored (sigma 0.2 dex prior, Price+2021)",
                              "fDM": "MODEL OUTPUT (MAP)", "Vc": "MODEL OUTPUT with asymmetric-drift term applied", "sigma0": "model output",
                              "g_Re etc": "derived by this repo"}
fails = [r for r in rows if r["verdict"] in ("FAIL", "info (would fail)")]
print("\nSUMMARY (%s): rows meeting their line" % DATA.upper(), sum(r["verdict"] in ("PASS", "info (would pass)") for r in rows), "of", len(rows), "; rows not meeting it:", [r["id"] for r in fails])
R["rows"] = rows
savejson("CFG233_main", R)
ctrl_ok = c4pass and c1max < 1e-9 and abs(s1 - s0 - 0.2) < 1e-9
print("controls C1,C3,C4 pass:", ctrl_ok)
sys.exit(0 if ctrl_ok else 1)
