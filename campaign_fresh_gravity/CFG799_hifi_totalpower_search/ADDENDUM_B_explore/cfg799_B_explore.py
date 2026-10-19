"""CFG799 ADDENDUM B, EXPLORATORY decomposition of the 90-observation stack.  Sets no class; changes no frozen rule.

Run:  python3 -I cfg799_B_explore.py <data_dir> <new35_ids.txt> <out_dir>
It imports the unchanged ../ADDENDUM_B_full90/cfg799.py (sha256 7486117b...a81488) and only decomposes its stack.

DECLARED LIST (fixed before the first run; everything is reported, nothing is selected):
  K1  reproduce B1: nu_t a = -6.577 mK (z -1.13), nu_2 a = +15.343 mK (z +3.04), within 0.01 mK.
  E1  per observation at nu_t and nu_2: a, sigma (no chi2 inflation), z; old-55 / new-35 flag; leave-one-observation-out
      range of the stack z; share of the stack amplitude carried by the five largest contributors; spread of the
      per-observation z (a standard deviation near 1 means the formal errors are right, above 1 means baseline texture).
  E2  halves of the stack at nu_t and nu_2, difference z = (a1 - a2)/hypot(s1, s2):
        H vs V polarisation; early vs late (split at the median obsid of the contributing spectra); USB vs LSB;
        line-rich vs other targets (target-name substrings below); old-55 vs new-35; point vs spectral-scan mode.
      12 comparisons in all (6 splits x 2 frequencies); read any single one against that count.
  E3  Gaussian FWHM 1.14, 2, 4, 8, 16 MHz at nu_t and nu_2 (same baseline); a narrow line should peak at <= 2 MHz.
  E4  empirical null: the +-40 MHz scan (0.5 MHz steps, centred on nu_t, nu_2 sits at +36) for total power, REF-only and
      Level-1.  Report mean and standard deviation of z over steps away from nu_t and nu_2 (+-5 MHz), the fraction of
      those far steps with |z| >= the z at nu_2 and at nu_t REF-only.  Also print the total/REF/Level-1 z at the steps
      +34 to +40 MHz.  (The first run also printed a "look-elsewhere p" that multiplied this fraction, which already
      counts steps, by a trials factor: it double counted and is dropped in the re-run.)
  E4b ADDED AFTER THE FIRST RUN (post-hoc arithmetic on the E4 output, labelled as such): the empirical-null z of the
      nu_2 total-power stack and of the nu_t REF-only stack, (z - mean)/std over the far steps; and the nu_t 95% limit
      with the formal sigma_a scaled by max(1, std of the total-power far-step z), reported beside the frozen number.
  E5  power of B2: the expected z of the 35 added scans if the nu_2 amplitude were the original +20.5 mK or the B1
      +15.3 mK, and the chance of B2's observed amplitude or lower in each case.
  E6  integration locked in the added scans that fail the anchor, and the best-case sensitivity gain from recovering
      all of it (1/sqrt of the hours; an upper bound, ignores that the stack is baseline-limited).
Target-name substrings for 'line-rich': orion, sgr b2, sgrb2, irc+10216, g34, w49, w51, ngc6334, ngc 6334, dr21, hot core.
"""
import importlib.util, json, os, sys
import numpy as np

DATA = os.path.abspath(sys.argv[1]); NEW = os.path.abspath(sys.argv[2]); OUTD = os.path.abspath(sys.argv[3])
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["cfg799.py", DATA]
spec = importlib.util.spec_from_file_location("cfg799", os.path.join(HERE, "..", "ADDENDUM_B_full90", "cfg799.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LINE_RICH = ("orion", "sgr b2", "sgrb2", "irc+10216", "g34", "w49", "w51", "ngc6334", "ngc 6334", "dr21", "hot core")
OUT, R = [], {}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


man, obs = m.load()
new = set(open(NEW).read().split())
anc, spectra = {}, []
for oid, o in obs.items():
    a = m.anchor(o); anc[oid] = a
    if a["ok"]:
        spectra += m.build_spectra(oid, o, a["tS"])
sp, drops = m.prep(spectra)
NU = (("nu_t", m.NU_T), ("nu_2", m.NU_2))
P("CFG799 ADDENDUM B exploratory decomposition (sets no class)")
P(f"  spectra {len(sp)}, observations used {len({s['obs'] for s in sp})}, new-35 among them "
  f"{len({s['obs'] for s in sp} & new)}")

# ---- K1
base = {}
for name, nu in NU:
    a = m.amps(sp, nu); st = m.stack(a); base[name] = (a, st)
want = {"nu_t": -6.577e-3, "nu_2": 15.343e-3}
for name in base:
    P(f"  K1 {name}: a = {base[name][1]['a'] * 1e3:+.3f} mK, z {base[name][1]['z']:+.2f}  "
      f"{'REPRODUCES B1' if abs(base[name][1]['a'] - want[name]) < 1e-5 else 'DOES NOT REPRODUCE'}")
    assert abs(base[name][1]["a"] - want[name]) < 1e-5

# ---- E1
P("\nE1 per observation")
R["E1"] = {}
for name, nu in NU:
    a, st = base[name]
    by = {}
    for x in a:
        by.setdefault(x[2]["obs"], []).append(x)
    rows = []
    wtot = sum(1 / x[1] ** 2 for x in a)
    for oid, xs in by.items():
        s1 = m.stack(xs, inflate=False)
        contrib = sum(x[0] / x[1] ** 2 for x in xs) / wtot
        rows.append(dict(obs=oid, new=oid in new, target=man.get(oid, {}).get("target", ""), n=len(xs), a=s1["a"], sig=s1["sig"],
                         z=s1["z"], contrib=contrib))
    zs = np.array([r["z"] for r in rows])
    loo = []
    for oid in by:
        rest = [x for x in a if x[2]["obs"] != oid]
        loo.append((m.stack(rest)["z"], oid))
    loo.sort()
    top = sorted(rows, key=lambda r: -abs(r["contrib"]))[:5]
    share = sum(r["contrib"] for r in top) / st["a"] if st["a"] else float("nan")
    R["E1"][name] = dict(rows=rows, loo_min=loo[0], loo_max=loo[-1], z_std=float(np.std(zs)), z_frac_gt2=float(np.mean(np.abs(zs) > 2)),
                         top_share=share)
    P(f"  [{name}] {len(rows)} obs; per-obs z std {np.std(zs):.2f} (1 = formal errors right), |z|>2 in {np.mean(np.abs(zs) > 2) * 100:.0f}% "
      f"(expect 5%)")
    P(f"     stack z {st['z']:+.2f}; leave-one-out z from {loo[0][0]:+.2f} (drop {loo[0][1]}) to {loo[-1][0]:+.2f} (drop {loo[-1][1]})")
    P(f"     five largest contributors carry {share * 100:.0f}% of the stack amplitude: " +
      "; ".join(f"{r['obs']} {r['target'][:14]} a {r['a'] * 1e3:+.1f}+-{r['sig'] * 1e3:.1f} mK z {r['z']:+.1f}{' [new]' if r['new'] else ''}" for r in top))

# ---- E2
P("\nE2 halves of the stack (difference z = (a1-a2)/hypot(s1,s2))")
R["E2"] = {}
allobs = sorted({s["obs"] for s in sp}); med_obs = float(np.median([int(o) for o in allobs]))


def lr(oid):
    t = man.get(oid, {}).get("target", "").lower()
    return any(k in t for k in LINE_RICH)


SPL = [("H vs V", lambda s: s["pol"] == "h", "H", "V"),
       ("early vs late", lambda s: int(s["obs"]) <= med_obs, "early", "late"),
       ("USB vs LSB", lambda s: s["usb"], "USB", "LSB"),
       ("line-rich vs other", lambda s: lr(s["obs"]), "line-rich", "other"),
       ("old-55 vs new-35", lambda s: s["obs"] not in new, "old", "new"),
       ("point vs scan", lambda s: "SScan" not in man.get(s["obs"], {}).get("mode", ""), "point", "scan")]
for name, nu in NU:
    a, st = base[name]; R["E2"][name] = {}
    for lab, pred, n1, n2 in SPL:
        s1 = m.stack([x for x in a if pred(x[2])]); s2 = m.stack([x for x in a if not pred(x[2])])
        dz = (s1["a"] - s2["a"]) / np.hypot(s1["sig"], s2["sig"]) if s1["n"] and s2["n"] else float("nan")
        R["E2"][name][lab] = dict(h1=s1, h2=s2, dz=float(dz))
        P(f"  [{name}] {lab:19s} {n1}: a {s1['a'] * 1e3:+6.1f}+-{s1['sig'] * 1e3:4.1f} mK z {s1['z']:+5.2f} (n {s1['n']:3d}) | "
          f"{n2}: a {s2['a'] * 1e3:+6.1f}+-{s2['sig'] * 1e3:4.1f} mK z {s2['z']:+5.2f} (n {s2['n']:3d}) | diff z {dz:+.2f}")

# ---- E3
P("\nE3 width (FWHM, MHz): stack z, a")
R["E3"] = {}
sig0 = m.SIG_G
for name, nu in NU:
    row = {}
    for fw in (1.14, 2.0, 4.0, 8.0, 16.0):
        m.SIG_G = fw / 2.3548
        st = m.stack(m.amps(sp, nu)); row[fw] = st
    m.SIG_G = sig0
    R["E3"][name] = row
    P(f"  [{name}] " + "  ".join(f"{fw:g}: z {st['z']:+.2f} (a {st['a'] * 1e3:+.1f} mK)" for fw, st in row.items()))

# ---- E4
P("\nE4 empirical null: +-40 MHz scan about nu_t (nu_2 at +36)")
deltas = np.arange(-40, 40.01, 0.5)
Z = {key: np.array([m.stack(m.amps(sp, m.NU_T + d / 1000, key=key))["z"] for d in deltas]) for key in ("Tall", "Tref", "L1")}
R["E4"] = dict(delta_MHz=deltas.tolist(), **{k: v.tolist() for k, v in Z.items()})
far = (np.abs(deltas) > 5) & (np.abs(deltas - 36) > 5)
z2 = base["nu_2"][1]["z"]; ref_t = m.stack(m.amps(sp, m.NU_T, key="Tref"))["z"]
for key, lab in (("Tall", "total power"), ("Tref", "REF-only"), ("L1", "Level-1")):
    z = Z[key]
    P(f"  {lab:12s}: z over steps away from nu_t and nu_2: mean {np.nanmean(z[far]):+.2f}, std {np.nanstd(z[far]):.2f}; "
      f"max |z| {np.nanmax(np.abs(z)):.2f} at {deltas[np.nanargmax(np.abs(z))]:+.1f} MHz; steps |z|>=3: {int(np.sum(np.abs(z) >= 3))}")
fr2 = float(np.mean(np.abs(Z["Tall"][far]) >= abs(z2))); frr = float(np.mean(np.abs(Z["Tref"][far]) >= abs(ref_t)))
P(f"  far steps ({int(far.sum())}): total power |z| >= {abs(z2):.2f} (the nu_2 value) at {fr2 * 100:.1f}% of them; "
  f"REF-only |z| >= {abs(ref_t):.2f} (the nu_t REF-only value) at {frr * 100:.1f}%")
idx = [i for i, d in enumerate(deltas) if 34 <= d <= 40]
P("  z at +34..+40 MHz (total / REF-only / Level-1): " + "; ".join(f"{deltas[i]:+.1f}: {Z['Tall'][i]:+.1f}/{Z['Tref'][i]:+.1f}/{Z['L1'][i]:+.1f}" for i in idx[::2]))
mu_a, sd_a = float(np.nanmean(Z["Tall"][far])), float(np.nanstd(Z["Tall"][far]))
mu_r, sd_r = float(np.nanmean(Z["Tref"][far])), float(np.nanstd(Z["Tref"][far]))
P(f"  E4b (post-hoc arithmetic): empirical-null z of nu_2 total power {(z2 - mu_a) / sd_a:+.2f}; of nu_t REF-only {(ref_t - mu_r) / sd_r:+.2f}")
st_t = base["nu_t"][1]; k_sc = max(1.0, sd_a)
a95_f = max(st_t["a"], 0) + 1.645 * st_t["sig"]; a95_e = max(st_t["a"], 0) + 1.645 * st_t["sig"] * k_sc
P(f"  E4b nu_t 95% limit: frozen a95 {a95_f * 1e3:.2f} mK -> with sigma x{k_sc:.2f}: {a95_e * 1e3:.2f} mK;  eps95 (S=10/50/1000) frozen "
  + "/".join(f"{m.eps_of(a95_f, S):.2e}" for S in m.S_LIST) + " -> scaled " + "/".join(f"{m.eps_of(a95_e, S):.2e}" for S in m.S_LIST)
  + f";  kill line 1e-12 missed by x" + "/".join(f"{m.eps_of(a95_e, S) / 1e-12:.1f}" for S in m.S_LIST) + " (scaled)")
R["E4_summary"] = dict(frac_ge_z2_far=fr2, frac_ref_ge_far=frr, mean_far={"Tall": mu_a, "Tref": mu_r}, std_far={k: float(np.nanstd(v[far])) for k, v in Z.items()},
                       z_emp_nu2=(z2 - mu_a) / sd_a, z_emp_ref_nut=(ref_t - mu_r) / sd_r, a95_frozen=a95_f, a95_scaled=a95_e,
                       eps95_scaled={f"S{S:.0f}": m.eps_of(a95_e, S) for S in m.S_LIST})

# ---- E5
P("\nE5 power of the 35 added scans alone (B2 numbers recomputed here)")
sp_new = [s for s in sp if s["obs"] in new]
a_new = m.amps(sp_new, m.NU_2); st_new = m.stack(a_new)
from scipy.stats import norm
for amp in (20.5e-3, 15.3e-3):
    zexp = amp / st_new["sig"]; pobs = float(norm.cdf((st_new["a"] - amp) / st_new["sig"]))
    P(f"  true a = {amp * 1e3:.1f} mK: expected z {zexp:+.2f}; chance of B2's amplitude ({st_new['a'] * 1e3:+.1f} mK) or lower {pobs:.2f}; "
      f"chance of z >= 3 {float(norm.sf(3 - zexp)):.2f}")
R["E5"] = dict(new=st_new)

# ---- E6
P("\nE6 integration in the added scans")
tin = {o: man[o]["t_int_h"] for o in new}; fail = [o for o in new if not anc[o]["ok"]]
usedn = {s["obs"] for s in sp_new}
P(f"  added scans {sum(tin.values()):.2f} h; failing the anchor {sum(tin[o] for o in fail):.2f} h ({len(fail)} scans); used {sum(tin[o] for o in usedn):.2f} h")
tuse = np.sum([man[o]["t_int_h"] for o in {s['obs'] for s in sp}])
gain = np.sqrt((tuse + sum(tin[o] for o in fail)) / tuse)
P(f"  all used observations {tuse:.2f} h; recovering every failed scan would give at most a x{gain:.2f} sensitivity gain "
  f"(sigma down {100 * (1 - 1 / gain):.0f}%), before the baseline limit")
R["E6"] = dict(added_h=sum(tin.values()), fail_h=sum(tin[o] for o in fail), used_h=float(tuse), best_gain=float(gain))

open(os.path.join(OUTD, "explore.out"), "w").write("\n".join(OUT) + "\n")
json.dump(R, open(os.path.join(OUTD, "explore_results.json"), "w"), indent=1, default=str)
