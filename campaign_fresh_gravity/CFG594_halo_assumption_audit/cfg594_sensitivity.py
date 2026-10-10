#!/usr/bin/env python3
"""CFG594 quick check (FROZEN_CRITERIA.md, commit d7fbcc267): sensitivity of the CFG556 halo-model excess E (a CONTEXT statistic,
no verdict role) to one-at-a-time changes of LCDM-inherited and standard-MOND-inherited ingredients.

  OMP_NUM_THREADS=2 nice -n 10 python3 cfg594_sensitivity.py                -> cfg594_sensitivity.out, cfg594_sensitivity_results.json
  CFG594_MUTATE=1 OMP_NUM_THREADS=2 nice -n 10 python3 cfg594_sensitivity.py -> *_MUTATE.out / *_MUTATE.json (exit 1 = both teeth bite)

CFG556's source is exec'd read-only up to its run marker with literal text substitutions; the primary case is rebuilt exactly as
CFG556's summarize() does (edge 'cen', census f_ret, scope 'ta').
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
SRC556 = os.path.join(HERE, "..", "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
J556 = json.load(open(os.path.join(HERE, "..", "CFG556_halo_model_matter_power", "cfg556_results.json")))
MUTATE = os.environ.get("CFG594_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)

SRC = open(SRC556).read()
CUT = SRC.index("# ------------------------------------------------------------------ run")
BASE = SRC[:CUT]
FOOTS = ("canonical", "alt")

RE_LINE = "        re = rM / math.log1p(f * FB / (1 - FB))"
SUP_LINE = "    Mb = f * FB * Mta; supply = (1 - FB) * Mta; a0 = A0MPC[foot]"
FRET_LINE = '    f = fret_of(math.log10(Mta)) if fret_mode == "census" else 1.0'
for s in (RE_LINE, SUP_LINE, FRET_LINE, "def conc(M): return 10.14 * (M / 2e12) ** -0.081", "    return ms * h\n",
          "NS, SIG8 = 0.965, 0.811", "DTA = 11.81", "fT = 0.186 * ((SIG / 2.57) ** -1.47 + 1) * np.exp(-1.19 / SIG ** 2)",
          "BIAS = 1 - A10 * NUP ** a10 / (NUP ** a10 + DC ** a10) + B10 * NUP ** b10 + C10 * NUP ** c10"):
    assert SRC.count(s) == 1, s

def nu_rar(y):
    y = np.maximum(y, 1e-300); s = np.sqrt(y)
    return np.where(s > 50, 1.0, 1.0 / -np.expm1(-np.minimum(s, 50)))
def nu_simple(y):
    y = np.maximum(y, 1e-300); return 0.5 + np.sqrt(0.25 + 1.0 / y)
def nu_standard(y):
    y = np.maximum(y, 1e-300); return np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y ** 2))

def make_nu(kernel, yext):
    base = {"rar": nu_rar, "simple": nu_simple, "standard": nu_standard}[kernel]
    if yext == 0.0:
        return base
    return lambda y: base(np.sqrt(np.asarray(y, float) ** 2 + yext ** 2))

def edge_num_factory(nu):
    def edge_num(Mb, supply, rM):
        """point-mass supply exhaustion: Mb (nu((rM/r)^2) - 1) = supply; returns r_e (inf if never reached)."""
        g = lambda lx: float(nu(np.array(10.0 ** (-2 * lx)))) - 1.0 - supply / Mb
        lo, hi = -4.0, 8.0
        if g(lo) * g(hi) > 0:
            return math.inf if g(hi) < 0 else rM * 10 ** lo     # never exhausts the supply -> inf (capped at r_ta); already exhausted -> tiny
        return rM * 10 ** brentq(g, lo, hi, xtol=1e-13, rtol=1e-13)
    return edge_num

def build(subs=(), kernel="rar", yext=0.0, numedge=False):
    src = BASE
    for a, b in subs:
        assert src.count(a) == 1, a
        src = src.replace(a, b)
    if numedge:
        src = src.replace(RE_LINE, "        re = _EDGE_NUM(Mb, supply, rM)")
    H = {"__name__": "cfg556_ro", "__file__": SRC556}
    exec(compile(src, "cfg556_ro", "exec"), H)
    nu = make_nu(kernel, yext)
    H["nu_k"] = nu
    H["_EDGE_NUM"] = edge_num_factory(nu)
    return H

def primary(H, fret_mode="census", mode="normal"):
    """CFG556 summarize() primary statistic per footing."""
    KK = H["KK"]
    Ustd = H["U_std"](); Pstd, _, _ = H["spectra_std"](Ustd)
    Ulta, _ = H["U_set"](lambda hb: H["frame_profile"](hb, "canonical", mode="lta")); Plta, _, _ = H["spectra_ta"](Ulta)
    out = {}
    w8 = H["_W8"](KK * 8.0) ** 2 * KK ** 2 / (2 * math.pi ** 2)
    m = (KK >= 0.05) & (KK <= 1.0)
    for ft in FOOTS:
        U, infos = H["U_set"](lambda hb: H["frame_profile"](hb, ft, edge="cen", fret_mode=fret_mode, mode=mode))
        PF, _, _ = H["spectra_ta"](U)
        R = 1 + (PF - Plta) / Pstd
        dP = PF - Plta
        s8F = math.sqrt(H["s8_of"](Pstd) ** 2 + np.trapz(dP * w8, KK))
        c3 = 0.0
        for i in range(0, len(H["HB"]), 8):
            r, Mc, _ = H["frame_profile"](H["HB"][i], ft, edge="cen", fret_mode=fret_mode, mode=mode)
            c3 = max(c3, abs(Mc[-1] - H["HB"][i]["Mta"]) / H["HB"][i]["Mta"])
        lM = np.log10(H["MTA"])
        re_ta = np.array([inf["re"] / hb["rta"] if np.isfinite(inf.get("re", np.nan)) else np.nan for inf, hb in zip(infos, H["HB"])])
        ncap = int(sum(bool(inf.get("capped", False)) for inf in infos))
        out[ft] = dict(E=float(np.max(R[m] - 1)), kE=float(KK[m][np.argmax(R[m])]), D=float(np.min(R[m] - 1)),
                       R035=float(np.interp(0.35, KK, R)), R1=float(np.interp(1.0, KK, R)), s8_ratio=s8F / H["s8_of"](Pstd),
                       C3=c3, n_capped=ncap,
                       re_over_rta={f"{l}": (float(np.interp(l, lM, re_ta)) if mode == "normal" else None) for l in (12, 13, 14, 15)})
    return out

E556 = {ft: J556["cases"][f"{ft}|census|cen"]["E"] for ft in FOOTS}
E556_1 = {ft: J556["cases"][f"{ft}|fret1|cen"]["E"] for ft in FOOTS}

def classify(E, ft):
    d = E - E556[ft]
    c = "DRIVER" if abs(d) >= 0.25 else ("MODERATE" if abs(d) >= 0.10 else "MINOR")
    return d, c, E <= 0.10

def sup(s):
    return [(SUP_LINE, f"    Mb = f * FB * Mta; supply = {s!r} * (1 - FB) * Mta; a0 = A0MPC[foot]"),
            (RE_LINE, f"        re = rM / math.log1p(f * FB / ({s!r} * (1 - FB)))")]

VARIANTS = {
    "L1 c(M) x0.7": dict(subs=[("def conc(M): return 10.14 *", f"def conc(M): return {10.14 * 0.7!r} *")]),
    "L2 c(M) x1.3": dict(subs=[("def conc(M): return 10.14 *", f"def conc(M): return {10.14 * 1.3!r} *")]),
    "L3 Moster M* x0.5": dict(subs=[("    return ms * h\n", "    return ms * h * 0.5\n")]),
    "L4 Moster M* x2": dict(subs=[("    return ms * h\n", "    return ms * h * 2.0\n")]),
    "L5 sigma8 0.76": dict(subs=[("NS, SIG8 = 0.965, 0.811", "NS, SIG8 = 0.965, 0.76")]),
    "L6 Delta_ta x0.8": dict(subs=[("DTA = 11.81", f"DTA = {11.81 * 0.8!r}")]),
    "L7 Delta_ta x1.2": dict(subs=[("DTA = 11.81", f"DTA = {11.81 * 1.2!r}")]),
    "L8 Press-Schechter mf + MW bias": dict(subs=[("fT = 0.186 * ((SIG / 2.57) ** -1.47 + 1) * np.exp(-1.19 / SIG ** 2)",
                                                   "fT = math.sqrt(2 / math.pi) * (DC / SIG) * np.exp(-0.5 * (DC / SIG) ** 2)"),
                                                  ("BIAS = 1 - A10 * NUP ** a10 / (NUP ** a10 + DC ** a10) + B10 * NUP ** b10 + C10 * NUP ** c10",
                                                   "BIAS = 1 + (NUP ** 2 - 1) / DC")]),
    "L9 f_ret x0.5": dict(subs=[(FRET_LINE, '    f = min(0.5 * fret_of(math.log10(Mta)), 1.0) if fret_mode == "census" else 1.0')]),
    "L10 f_ret x2": dict(subs=[(FRET_LINE, '    f = min(2.0 * fret_of(math.log10(Mta)), 1.0) if fret_mode == "census" else 1.0')]),
    "L11 supply x0.5": dict(subs=sup(0.5)),
    "L12 supply x0.75": dict(subs=sup(0.75)),
    "M0 numerical edge, RAR (control C1)": dict(numedge=True),
    "M1 nu_simple": dict(numedge=True, kernel="simple"),
    "M2 nu_standard": dict(numedge=True, kernel="standard"),
    "M3 EFE y_ext 0.01": dict(numedge=True, yext=0.01),
    "M4 EFE y_ext 0.03": dict(numedge=True, yext=0.03),
}

P(f"CFG594 sensitivity of the CFG556 halo-model excess {'(MUTATE)' if MUTATE else ''} -- FROZEN_CRITERIA.md (d7fbcc267).")
P("kappa = 1/2 FITTED; footings never pooled; flat a0; candidate B; cold energy MASS still required; not theory closed. CONTEXT statistic, no verdict role.")
res = dict(lane="CFG594", date="2026-10-10", mutate=MUTATE, E556=E556, controls={}, variants={})

H0 = build()
base = primary(H0)
c0 = max(abs(base[ft]["E"] - E556[ft]) for ft in FOOTS)
one = primary(H0, fret_mode="one")
c2 = max(abs(one[ft]["E"] - E556_1[ft]) for ft in FOOTS)
P(f"\nC0 reproduce CFG556 primary E: can {base['canonical']['E']:+.6f} (556 {E556['canonical']:+.6f}), alt {base['alt']['E']:+.6f} "
  f"(556 {E556['alt']:+.6f}); max |d| {c0:.1e} (<= 1e-6) -> {'PASS' if c0 <= 1e-6 else 'FAIL'}")
P(f"C2 f_ret = 1 reproduces CFG556 fret1: max |d| {c2:.1e} (<= 1e-6) -> {'PASS' if c2 <= 1e-6 else 'FAIL'}")
res["controls"].update(C0=c0, C0_pass=bool(c0 <= 1e-6), C2=c2, C2_pass=bool(c2 <= 1e-6), base=base)
ok_all = (c0 <= 1e-6) and (c2 <= 1e-6)

if not MUTATE:
    P(f"\n{'variant':36s} | {'canonical E (dE) class':34s} | {'alt E (dE) class':34s} | R(0.35) c/a   | R(1) c/a      | s8 c/a        | C3")
    for name, spec in VARIANTS.items():
        H = build(**spec)
        o = primary(H)
        row = {}
        for ft in FOOTS:
            d, c, cut = classify(o[ft]["E"], ft)
            row[ft] = dict(o[ft], dE=d, cls=c, cut_setting=bool(cut))
        c3 = max(row[ft]["C3"] for ft in FOOTS)
        row["C3_pass"] = bool(c3 <= 1e-6)
        if name.startswith("M0"):
            c1 = max(abs(row[ft]["E"] - base[ft]["E"]) for ft in FOOTS)
            res["controls"].update(C1=c1, C1_pass=bool(c1 <= 1e-4)); ok_all &= c1 <= 1e-4
        res["variants"][name] = row
        f = lambda ft: f"{row[ft]['E']:+.3f} ({row[ft]['dE']:+.3f}) {row[ft]['cls']}{' CUT' if row[ft]['cut_setting'] else ''}"
        P(f"{name:36s} | {f('canonical'):34s} | {f('alt'):34s} | {row['canonical']['R035']:.3f}/{row['alt']['R035']:.3f} | "
          f"{row['canonical']['R1']:.3f}/{row['alt']['R1']:.3f} | {row['canonical']['s8_ratio']:.4f}/{row['alt']['s8_ratio']:.4f} | "
          f"{c3:.1e} {'PASS' if row['C3_pass'] else 'FAIL'}")
        if name[0] == "M" and not name.startswith("M0"):
            P(f"{'':36s}   r_e/r_ta at log M_ta 12/13/14/15 (can): " + " ".join(
                f"{row['canonical']['re_over_rta'][str(l)]:.3f}" for l in (12, 13, 14, 15)) + f"; capped can/alt {row['canonical']['n_capped']}/{row['alt']['n_capped']}")
        ok_all &= row["C3_pass"]
    P(f"\nC1 numerical RAR edge reproduces closed form: max |dE| {res['controls']['C1']:.1e} (<= 1e-4) -> {'PASS' if res['controls']['C1_pass'] else 'FAIL'}")
    # item-level summary
    items = {"c(M) [Duffy08]": ["L1 c(M) x0.7", "L2 c(M) x1.3"], "SHMR [Moster13]": ["L3 Moster M* x0.5", "L4 Moster M* x2"],
             "sigma8 / IC amplitude": ["L5 sigma8 0.76"], "Delta_ta": ["L6 Delta_ta x0.8", "L7 Delta_ta x1.2"],
             "mass function + bias [Tinker]": ["L8 Press-Schechter mf + MW bias"], "census f_ret": ["L9 f_ret x0.5", "L10 f_ret x2"],
             "catchment supply amount": ["L11 supply x0.5", "L12 supply x0.75"], "kernel low-y form": ["M1 nu_simple", "M2 nu_standard"],
             "EFE (standard MOND)": ["M3 EFE y_ext 0.01", "M4 EFE y_ext 0.03"]}
    rank = {"MINOR": 0, "MODERATE": 1, "DRIVER": 2}
    P("\nItem summary (worst class over its declared variants, per footing; 'removes' = a variant CUT-SETTING on both footings):")
    res["items"] = {}
    for it, vs in items.items():
        cl = {ft: max((res["variants"][v][ft]["cls"] for v in vs), key=lambda c: rank[c]) for ft in FOOTS}
        rem = any(all(res["variants"][v][ft]["cut_setting"] for ft in FOOTS) for v in vs)
        mx = {ft: max(abs(res["variants"][v][ft]["dE"]) for v in vs) for ft in FOOTS}
        res["items"][it] = dict(cls=cl, removes=bool(rem), max_abs_dE=mx)
        P(f"  {it:32s} can {cl['canonical']:8s} (max|dE| {mx['canonical']:.3f})  alt {cl['alt']:8s} (max|dE| {mx['alt']:.3f})  removes excess: {'YES' if rem else 'no'}")
    P(f"\nAll controls: {'PASS' if ok_all else 'FAIL -> NO RESULT for affected variants'}")
    res["all_controls_pass"] = bool(ok_all)
else:
    teeth = {}
    o = primary(build(subs=sup(0.2)))
    teeth["MU1"] = bool(all(classify(o[ft]["E"], ft)[1] == "DRIVER" for ft in FOOTS))
    P(f"MU1 supply x0.2: E can {o['canonical']['E']:+.3f} alt {o['alt']['E']:+.3f} -> {'BITES' if teeth['MU1'] else 'FAILS'} (DRIVER required on both)")
    o2 = primary(H0, mode="lta")
    teeth["MU2"] = bool(all(abs(o2[ft]["E"]) <= 1e-9 for ft in FOOTS))
    P(f"MU2 framework profile := NFW: |E| can {abs(o2['canonical']['E']):.1e} alt {abs(o2['alt']['E']):.1e} -> {'BITES' if teeth['MU2'] else 'FAILS'} (<= 1e-9)")
    res["teeth"] = teeth

json.dump(res, open(os.path.join(HERE, f"cfg594_sensitivity_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg594_sensitivity{SUF}.out"), "w").write("\n".join(OUT) + "\n")
if MUTATE:
    sys.exit(1 if all(res["teeth"].values()) else 0)
