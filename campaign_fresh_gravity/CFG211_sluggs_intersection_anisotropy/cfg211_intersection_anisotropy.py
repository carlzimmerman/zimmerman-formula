#!/usr/bin/env python3
"""CFG211 -- does CFG112's ten-population 2-sigma intersection (one debris fraction phi for all populations) open when SLUGGS's
U5d prediction uses a constant GC orbital anisotropy beta (CFG113's Jeans machinery)?  Published slopes, unshifted.
Frozen criteria: FROZEN_CRITERIA.md here (0f0fdcea8), committed before any number.  kappa = 1/2 FITTED, NOT DERIVED.
PRIMARY beta (measured-anchored): NGC 5846 +0.275; NGC 1407, NGC 4486 and the other 13: 0.  Sensitivity: +0.25 / +0.5 for all.
Machinery: CFG112's script exec'd read-only up to its controls (MUTATE forced 0, output captured); the one change is beta in
sigma_r2 / sigma_los (CFG55/h50's functions, which take a constant beta).
Run:  python3 campaign_fresh_gravity/CFG211_sluggs_intersection_anisotropy/cfg211_intersection_anisotropy.py   (MUTATE=1: beta = 0)
"""
import os, sys, io, json, contextlib
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
R = C.Report("cfg211_intersection_anisotropy", MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())

# ---- CFG112, exec'd read-only up to its controls
F112 = os.path.join(CFG, "CFG112_universal_fraction_published_slopes.py")
src = open(F112).read()
cut = src.index("# ================================================================== C1 / C2 / C3")
ns = {"__file__": F112, "__name__": "cfg112"}
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], "CFG112", "exec"), ns)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
assert ns["MUTATE"] is False and ns["GUSE"] is ns["GLIT"]
G16, GRID, OTHERS, S71, U5 = ns["G16"], ns["GRID"], ns["OTHERS"], ns["S71"], ns["U5"]
cal, inter, inside, runs, fmt, GLIT, NAMES = ns["cal"], ns["inter"], ns["inside"], ns["runs"], ns["fmt"], ns["GLIT"], ns["NAMES"]
A0SI55, debris_phi, G55, MSUN55, KPC55, nu55, nfw55, FB55 = (ns[k] for k in ("A0SI55", "debris_phi", "G55", "MSUN55", "KPC55", "nu55",
                                                                            "nfw55", "FB55"))
sr2, slos = ns["sr2"], ns["slos"]
FOOTS = ("canonical", "alt")


def off_phi_gb(g, foot, Ms, phi, gam, beta):
    """CFG112's off_phi_g with the constant GC anisotropy beta in sigma_r2 and sigma_los (the lane's one change)."""
    r = g["r"]; a0 = A0SI55[foot]; a_h = r["Re"] / 1.8153
    fx, Mh = debris_phi(Ms, foot)

    def gf(rr):
        Mb = Ms * MSUN55 * rr ** 2 / (rr + a_h) ** 2; gN = G55 * Mb / (rr * KPC55) ** 2
        out = gN * nu55(gN / a0)
        if phi * fx > 0:
            out = out + phi * fx * (1 - FB55) * G55 * np.asarray(nfw55(Mh, rr), float) * MSUN55 / (rr * KPC55) ** 2
        return out
    s_ = slos(r["Rb"], sr2(gf, gam, beta), gam, beta)
    return float(np.mean(np.log10(r["Sb"][r["out"]] / s_[r["out"]])))


def scan_b(foot, betas):
    oo, ee, nx = [], [], []
    for ph in GRID:
        off = []
        for g in G16:
            m = cal(g, foot, ph)
            off.append(float("nan") if not np.isfinite(m) else off_phi_gb(g, foot, m, ph, GLIT[g["name"]], betas[g["name"]]))
        off = np.array(off); ok = np.isfinite(off); o = off[ok]
        oo.append(float(o.mean())); ee.append(float(o.std(ddof=1) / np.sqrt(len(o)))); nx.append(int((~ok).sum()))
    return dict(o=np.array(oo), e=np.array(ee), nexcl=nx)


B0 = {n: 0.0 for n in NAMES}
PRIMARY = dict(B0, NGC5846=0.275)
CONFIGS = {"PRIMARY (measured-anchored)": PRIMARY, "S1 beta = +0.25 for all": {n: 0.25 for n in NAMES},
           "S2 beta = +0.5 for all": {n: 0.5 for n in NAMES}, "variant: primary with M87 at -0.25": dict(PRIMARY, NGC4486=-0.25)}
if MUT:
    CONFIGS = {"PRIMARY (measured-anchored)": B0}
    P("\n  *** MUTATE=1: beta = 0 for every galaxy (the lane's one change undone) -- H1 must FAIL, reproducing CFG112 ***")

# ------------------------------------------------------------------------------------------------ controls
R.banner("CONTROLS")
c112 = json.load(open(os.path.join(CFG, "CFG112_universal_fraction_published_slopes_results.json")))["numbers"]["U5d"]
SC0 = {f: scan_b(f, B0) for f in FOOTS}
d1 = max(max(float(np.max(np.abs(SC0[f]["o"] - np.array(c112[f]["o"])))), float(np.max(np.abs(SC0[f]["e"] - np.array(c112[f]["e"])))))
         for f in FOOTS)
check("C1 beta = 0 for all reproduces CFG112's committed U5d scan (o, e; 101 points; both footings) to 1e-9", f"max |difference| {d1:.1e}", d1 < 1e-9)
c113 = json.load(open(os.path.join(CFG, "CFG113_sluggs_anisotropy_results.json")))["numbers"]["RES"]
SC5 = {f: scan_b(f, {n: 0.5 for n in NAMES}) for f in FOOTS}
d2, rows = 0.0, []
for f in FOOTS:
    for which, idx in (("law", 0), ("rule", -1)):
        mo, me = SC5[f]["o"][idx], SC5[f]["e"][idx]
        ref = c113[f]["0.5"][which]
        d2 = max(d2, abs(mo - ref["mean"]), abs(me - ref["err"]))
        rows.append(f"{f} {which} {mo:+.6f}+-{me:.6f} (CFG113 {ref['mean']:+.6f}+-{ref['err']:.6f})")
check("C2 beta = +0.5 for all: U5d at phi = 0 / 1 reproduces CFG113's committed law / rule means and errors at beta = +0.5 (both footings) to 1e-6",
      f"max |difference| {d2:.1e}; " + "; ".join(rows), d2 < 1e-6)
want = {"canonical": (0.23, 0.71), "alt": (0.21, 0.66)}
got = {f: inter(None, f, 2, drop_u5=True) for f in FOOTS}
check("C3 CFG75's intersection without SLUGGS reproduced ([0.23, 0.71] canonical, [0.21, 0.66] alt)", "; ".join(f"{f} {fmt(got[f])}" for f in FOOTS),
      all(got[f] is not None and round(got[f][0], 2) == want[f][0] and round(got[f][1], 2) == want[f][1] for f in FOOTS))
ko = all(inter(dict(o=np.zeros(len(GRID)), e=SC0[f]["e"]), f, 2) == got[f] for f in FOOTS)
kc = all(inter(dict(o=5 * SC0[f]["e"], e=SC0[f]["e"]), f, 2) is None for f in FOOTS)
check("K_open / K_close: with U5d's o set to 0 the intersection equals C3's set; with o = 5e it is empty (both footings)", f"open {ko}, close {kc}", ko and kc)

# ------------------------------------------------------------------------------------------------ configurations
RESULT = {}
for name, betas in CONFIGS.items():
    R.banner(f"{name}: beta = " + ", ".join(f"{k} {v:+.3f}" for k, v in betas.items() if v != 0.0) if any(betas.values()) else f"{name}: beta = 0 for all")
    SC = SC5 if name.startswith("S2") and not MUT else ({f: SC0[f] for f in FOOTS} if MUT else {f: scan_b(f, betas) for f in FOOTS})
    I2 = {f: inter(SC[f], f, 2) for f in FOOTS}
    bind = {}
    for f in FOOTS:
        s5 = inside(SC[f]["o"], SC[f]["e"], 2)
        bind[f] = [n.split(" ")[0] for n in OTHERS if not (s5 & inside(S71[n + "|" + f]["o"], S71[n + "|" + f]["e"], 2)).any()]
        P(f"    {f}: U5d o/e at phi = 0, 0.25, 0.5, 0.71, 1: " + ", ".join(f"{SC[f]['o'][i]:+.4f}/{SC[f]['e'][i]:.4f} ({SC[f]['o'][i] / SC[f]['e'][i]:+.2f})"
                                                                   for i in (0, 25, 50, 71, 100)))
        P(f"        U5d 2-sigma set {runs(inside(SC[f]['o'], SC[f]['e'], 2)) or 'empty'}; ten-population 2-sigma intersection {fmt(I2[f])}; "
          f"populations disjoint from SLUGGS: {', '.join(bind[f]) or 'none'}")
    RESULT[name] = dict(I2=I2, bind=bind, U5d={f: dict(o=SC[f]["o"].tolist(), e=SC[f]["e"].tolist()) for f in FOOTS})

R.banner("DECISION ROWS")
prim = RESULT["PRIMARY (measured-anchored)"]["I2"]
h1 = all(prim[f] is not None for f in FOOTS)
lab = ("the intersection opens with measured-anchored anisotropy" if h1 else
       ("mixed: non-empty on one footing only" if any(prim[f] is not None for f in FOOTS) else "the clause stands under measured-anchored anisotropy"))
check("H1 [HEADLINE] with the PRIMARY (measured-anchored) beta the ten-population 2-sigma intersection is non-empty on both footings"
      + ("  [MUTATE: beta = 0]" if MUT else ""), "; ".join(f"{f}: {fmt(prim[f])}" for f in FOOTS) + f"  -> {lab}", h1)
if not MUT:
    for key, label in (("S1 beta = +0.25 for all", "conditional on uniform radial anisotropy beta = +0.25 in every galaxy (measured only for the red GCs of one galaxy outside ~3 R_e)"),
                       ("S2 beta = +0.5 for all", "conditional on radial anisotropy at or beyond the edge of the measured range")):
        I = RESULT[key]["I2"]
        opens = all(I[f] is not None for f in FOOTS)
        P(f"  {key}: " + "; ".join(f"{f} {fmt(I[f])}" for f in FOOTS) + (f"  -> OPENS: '{label}'" if opens else
                                                                         ("  -> mixed" if any(I[f] is not None for f in FOOTS) else "  -> stays empty")))
    Iv = RESULT["variant: primary with M87 at -0.25"]["I2"]
    P("  variant (M87 at -0.25, illustrative): " + "; ".join(f"{f} {fmt(Iv[f])}" for f in FOOTS))
R.num("results", {k: dict(I2=v["I2"], bind=v["bind"]) for k, v in RESULT.items()})
R.num("U5d", {k: v["U5d"] for k, v in RESULT.items()})
R.num("label", lab)
nf = R.write(here=LANE)
sys.exit(1 if nf else 0)
