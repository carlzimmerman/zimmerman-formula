"""CFG799 ADDENDUM C, EXPLORATORY decomposition of the 595.463 GHz frozen run (INCONCLUSIVE: C2 fails, nu_2 z -5.96).
Sets no class; changes no frozen rule.  Imports the unchanged ./cfg799.py of this folder.

Run:  python3 -I cfg799_C_explore.py <data_dir> <out_dir>

DECLARED LIST (fixed before the first run; everything is reported, one run, no variants beyond those listed):
  K1   reproduce the frozen run: nu_t a = +12.647 mK, nu_2 a = -41.531 mK (within 0.01 mK).
  CE1  H-only and V-only stacks at nu_t and nu_2: a, sigma, z, n.
  CE2  empirical null: the +-40 MHz scan (0.5 MHz steps) for total power, REF-only and Level-1; mean and standard deviation
       of z over the far steps (excluding +-5 MHz about nu_t and about nu_2, which sits at +37 MHz); the number of far steps
       with |z| >= 5; and the nu_t 95% limit with the formal sigma_a scaled by max(1, total-power far-step std), beside the
       frozen limit.
  CE3  baseline variants: Legendre degree 2, 3 (frozen), 4, 5 with half-window 50 (frozen) and 100 MHz (masks unchanged):
       nu_t and nu_2 a, sigma, z, and the far-step z std on a 1 MHz scan.  A sensitivity table; no variant is chosen.
  CE4  H-only and V-only total-power z(delta) over +-60 MHz in 1 MHz steps: std, steps with |z| >= 3, corr(H, V) over +-60
       and +-40 MHz, and the range of each against the combined stack's range over +-40 MHz.
  CE5  nu_2 (z -5.96) and nu_t decomposition: leave-one-observation-out range of the stack z; the five largest contributors by
       weight x amplitude; halves H/V, USB/LSB, early/late (median obsid), point/scan, line-rich/other (target-name
       substrings: orion, sgr b2, sgrb2, irc+10216, g34, w49, w51, ngc6334, ngc 6334, dr21, hot core).
  CE6  width: Gaussian FWHM 1.154, 2, 4, 8, 16 MHz at nu_t and nu_2.
"""
import importlib.util, json, os, sys
import numpy as np

DATA = os.path.abspath(sys.argv[1]); OUTD = os.path.abspath(sys.argv[2])
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["cfg799.py", DATA]
spec = importlib.util.spec_from_file_location("cfg799c", os.path.join(HERE, "cfg799.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LINE_RICH = ("orion", "sgr b2", "sgrb2", "irc+10216", "g34", "w49", "w51", "ngc6334", "ngc 6334", "dr21", "hot core")
OUT, R = [], {}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


man, obs = m.load()
spectra = []
for oid, o in obs.items():
    a = m.anchor(o)
    if a["ok"]:
        spectra += m.build_spectra(oid, o, a["tS"])
sp, drops = m.prep(spectra)
NU = (("nu_t", m.NU_T), ("nu_2", m.NU_2))
P("CFG799 ADDENDUM C exploratory decomposition (595.463 GHz; sets no class)")
base = {name: (m.amps(sp, nu), m.stack(m.amps(sp, nu))) for name, nu in NU}
want = {"nu_t": 12.647e-3, "nu_2": -41.531e-3}
for name in base:
    P(f"  K1 {name}: a = {base[name][1]['a'] * 1e3:+.3f} mK z {base[name][1]['z']:+.2f}  "
      f"{'REPRODUCES' if abs(base[name][1]['a'] - want[name]) < 1e-5 else 'DOES NOT REPRODUCE'}")
    assert abs(base[name][1]["a"] - want[name]) < 1e-5


def row(st):
    return f"{st['a'] * 1e3:+7.1f}+-{st['sig'] * 1e3:5.1f} mK z {st['z']:+6.2f} (n {st['n']:3d})"


# CE1
P("\nCE1 H-only / V-only")
R["CE1"] = {}
for name, nu in NU:
    a = base[name][0]
    h = m.stack([x for x in a if x[2]["pol"] == "h"]); v = m.stack([x for x in a if x[2]["pol"] == "v"])
    R["CE1"][name] = dict(H=h, V=v)
    P(f"  [{name}] H: {row(h)} | V: {row(v)}")

# CE2
P("\nCE2 empirical null (+-40 MHz scan, 0.5 MHz steps)")
deltas = np.arange(-40, 40.01, 0.5)
nu2_off = (m.NU_2 - m.NU_T) * 1000.0
far = (np.abs(deltas) > 5) & (np.abs(deltas - nu2_off) > 5)
Z = {key: np.array([m.stack(m.amps(sp, m.NU_T + d / 1000, key=key))["z"] for d in deltas]) for key in ("Tall", "Tref", "L1")}
R["CE2"] = dict(delta_MHz=deltas.tolist(), **{k: v.tolist() for k, v in Z.items()})
P(f"  nu_2 sits at {nu2_off:+.1f} MHz about nu_t; {int(far.sum())} far steps")
for key, lab in (("Tall", "total power"), ("Tref", "REF-only"), ("L1", "Level-1")):
    z = Z[key]
    P(f"  {lab:12s}: far-step mean {np.nanmean(z[far]):+.2f}, std {np.nanstd(z[far]):.2f}; far steps |z|>=5: {int(np.sum(np.abs(z[far]) >= 5))}; "
      f"max |z| {np.nanmax(np.abs(z)):.2f} at {deltas[np.nanargmax(np.abs(z))]:+.1f} MHz")
sd_a = float(np.nanstd(Z["Tall"][far])); st_t = base["nu_t"][1]; k_sc = max(1.0, sd_a)
a95_f = max(st_t["a"], 0) + 1.645 * st_t["sig"]; a95_e = max(st_t["a"], 0) + 1.645 * st_t["sig"] * k_sc
P(f"  nu_t 95 pct limit: frozen a95 {a95_f * 1e3:.2f} mK -> sigma x{k_sc:.2f}: {a95_e * 1e3:.2f} mK;  eps95 (S=10/50/1000) frozen "
  + "/".join(f"{m.eps_of(a95_f, S):.2e}" for S in m.S_LIST) + " -> scaled " + "/".join(f"{m.eps_of(a95_e, S):.2e}" for S in m.S_LIST))
R["CE2_limit"] = dict(far_std=sd_a, a95_frozen=a95_f, a95_scaled=a95_e, eps95_scaled={f"S{S:.0f}": m.eps_of(a95_e, S) for S in m.S_LIST})

# CE3
P("\nCE3 baseline variants (frozen = degree 3, +-50 MHz).  nu_t | nu_2 | far-step z std (1 MHz scan)")
orig_fit, orig_leg, orig_half = m.fit_one, m.legendre_design, m.HALF
d1 = np.arange(-40, 40.01, 1.0); far1 = (np.abs(d1) > 5) & (np.abs(d1 - nu2_off) > 5)


def variant(deg, half):
    def fit(IFax, y, flag, centre, inject=0.0, with_line=True):
        m.legendre_design = lambda x, ncoef=deg + 1: orig_leg(x, ncoef)
        m.HALF = half
        try:
            return orig_fit(IFax, y, flag, centre, inject=inject, with_line=with_line)
        finally:
            m.legendre_design, m.HALF = orig_leg, orig_half
    return fit


R["CE3"] = {}
for half in (50.0, 100.0):
    for deg in (2, 3, 4, 5):
        m.fit_one = variant(deg, half)
        rw = {name: m.stack(m.amps(sp, nu)) for name, nu in NU}
        zs = np.array([m.stack(m.amps(sp, m.NU_T + d / 1000))["z"] for d in d1])
        sd = float(np.nanstd(zs[far1]))
        R["CE3"][f"deg{deg}_half{half:g}"] = dict(rw, far_std=sd)
        P(f"  deg {deg}, +-{half:3g}: nu_t {row(rw['nu_t'])} | nu_2 {row(rw['nu_2'])} | std {sd:4.2f}" + ("  <- frozen" if deg == 3 and half == 50.0 else ""))
m.fit_one = orig_fit

# CE4
P("\nCE4 H-only vs V-only z(delta), +-60 MHz, 1 MHz steps")
dd = np.arange(-60, 60.01, 1.0); ZH = {}
for pol in ("h", "v"):
    spp = [s for s in sp if s["pol"] == pol]
    ZH[pol] = np.array([m.stack(m.amps(spp, m.NU_T + d / 1000))["z"] for d in dd])
zc = np.array([m.stack(m.amps(sp, m.NU_T + d / 1000))["z"] for d in dd])
R["CE4"] = dict(delta_MHz=dd.tolist(), H=ZH["h"].tolist(), V=ZH["v"].tolist(), combined=zc.tolist())
s40 = np.abs(dd) <= 40
for pol in ("h", "v"):
    z = ZH[pol]
    P(f"  {pol.upper()}: mean {np.nanmean(z):+.2f}, std {np.nanstd(z):.2f}; steps |z|>=3: {int(np.sum(np.abs(z) >= 3))} of {len(z)}; range within +-40: {np.nanmin(z[s40]):+.1f}..{np.nanmax(z[s40]):+.1f}")
P(f"  corr(H, V): +-60 MHz {np.corrcoef(ZH['h'], ZH['v'])[0, 1]:+.2f}, +-40 MHz {np.corrcoef(ZH['h'][s40], ZH['v'][s40])[0, 1]:+.2f}; "
  f"combined range within +-40: {np.nanmin(zc[s40]):+.1f}..{np.nanmax(zc[s40]):+.1f}, std {np.nanstd(zc[s40]):.2f}")

# CE5
P("\nCE5 decomposition")
R["CE5"] = {}
allobs = sorted({s["obs"] for s in sp}); med_obs = float(np.median([int(o) for o in allobs]))
lr = lambda oid: any(k in man.get(oid, {}).get("target", "").lower() for k in LINE_RICH)
SPL = [("H vs V", lambda s: s["pol"] == "h", "H", "V"), ("USB vs LSB", lambda s: s["usb"], "USB", "LSB"),
       ("early vs late", lambda s: int(s["obs"]) <= med_obs, "early", "late"),
       ("point vs scan", lambda s: "SScan" not in man.get(s["obs"], {}).get("mode", ""), "point", "scan"),
       ("line-rich vs other", lambda s: lr(s["obs"]), "line-rich", "other")]
for name, nu in NU:
    a, st = base[name]; by = {}
    for x in a:
        by.setdefault(x[2]["obs"], []).append(x)
    loo = sorted((m.stack([x for x in a if x[2]["obs"] != oid])["z"], oid) for oid in by)
    wtot = sum(1 / x[1] ** 2 for x in a)
    rows = []
    for oid, xs in by.items():
        s1 = m.stack(xs, inflate=False)
        rows.append((abs(sum(x[0] / x[1] ** 2 for x in xs) / wtot), oid, s1))
    rows.sort(reverse=True)
    P(f"  [{name}] {len(by)} obs; stack z {st['z']:+.2f}; leave-one-out z from {loo[0][0]:+.2f} (drop {loo[0][1]}) to {loo[-1][0]:+.2f} (drop {loo[-1][1]})")
    P("     largest contributors: " + "; ".join(f"{oid} {man.get(oid, {}).get('target', '')[:12]} a {s1['a'] * 1e3:+.0f}+-{s1['sig'] * 1e3:.0f} mK" for _, oid, s1 in rows[:5]))
    R["CE5"][name] = dict(loo_min=loo[0], loo_max=loo[-1])
    for lab, pred, n1, n2 in SPL:
        s1 = m.stack([x for x in a if pred(x[2])]); s2 = m.stack([x for x in a if not pred(x[2])])
        dz = (s1["a"] - s2["a"]) / np.hypot(s1["sig"], s2["sig"]) if s1["n"] and s2["n"] else float("nan")
        P(f"     {lab:19s} {n1}: {row(s1)} | {n2}: {row(s2)} | diff z {dz:+.2f}")

# CE6
P("\nCE6 width (FWHM MHz): stack z (a mK)")
sig0 = m.SIG_G; R["CE6"] = {}
for name, nu in NU:
    rw = {}
    for fw in (1.154, 2.0, 4.0, 8.0, 16.0):
        m.SIG_G = fw / 2.3548; rw[fw] = m.stack(m.amps(sp, nu))
    m.SIG_G = sig0; R["CE6"][name] = rw
    P(f"  [{name}] " + "  ".join(f"{fw:g}: {st['z']:+.2f} ({st['a'] * 1e3:+.0f})" for fw, st in rw.items()))

open(os.path.join(OUTD, "explore_C.out"), "w").write("\n".join(OUT) + "\n")
json.dump(R, open(os.path.join(OUTD, "explore_C_results.json"), "w"), indent=1, default=str)
