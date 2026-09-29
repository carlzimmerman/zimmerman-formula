#!/usr/bin/env python3
"""CFG160 -- KURVS a0(z) under the simulation-calibrated pressure-support factor of Kretschmer et al. 2021 (P4).

Frozen criteria: CFG160_FROZEN_CRITERIA.md (ae252ceb6), committed before any number under this prescription was computed.
  P4          V_c^2 = V_obs^2 + alpha(x) sigma_out^2, alpha(x) = -0.146 x^2 + 1.204 x + 1.475, x = R/R_e - 1 (Kretschmer et al. 2021,
              MNRAS 503, 5238, Table 1: gas in discs, 40% scatter); x clipped to [0, 4] (alpha 1.475 .. 3.955).
  R_e         primary: the paper's R_eff (= 1.68 R_d in CFG140); variant: 2 R_eff.  SPARC anchor: sigma = 10 km/s, R_e = 1.68 R_disk.
  pipeline    CFG141's, exec'd read-only (which exec's CFG140's): sample, baryons, gas and M* brackets, footings, anchor, pooling, errors.
  C1 CONTROL  with alpha = 2 R/R_d the P4 path reproduces CFG141's committed P2 grid exactly (1e-12).
  C2 CONTROL  alpha(0) = 1.475, alpha(1) = 2.533, alpha(4) = 3.955.
  H1 [HEADLINE; MUTATE must change it] under P4 flat a0 NOT disfavoured: NOT (Delta'_flat > +2 sigma in every one of the 24 P4 cells).
  H2 (reported verdict) under P4 the rival a0 ~ H(z) disfavoured: Delta'_H < -2 sigma in every P4 cell.
MUTATE=1: every KURVS v_last x 10^0.3 (inherited from CFG140's exec'd prefix) -- H1 must FAIL (rc = 1).
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour either model, or that the theory is closed.
Run: python3 campaign_fresh_gravity/CFG160_kurvs_kretschmer.py   (MUTATE=1 for the control)
"""
import os, sys, io, math, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG160_kurvs_kretschmer", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every KURVS v_last x 10^0.3 (g_obs x 4) -- H1 must FAIL ***")

F141 = os.path.join(HERE, "CFG141_kurvs_measured_sigma.py")
src = open(F141).read()
g141 = {"__file__": F141, "__name__": "cfg141"}
with contextlib.redirect_stdout(io.StringIO()):                 # the MUTATE variable is inherited on purpose: it is this lane's declared MUTATE
    exec(compile(src[:src.index("# ================================================================== C1 / C2")], "CFG141", "exec"), g141)
KU2, SP, A0, E = g141["KU2"], g141["SP"], g141["A0"], g141["E"]
gbar, gpred, slope, pooled, KPC = g141["gbar"], g141["gpred"], g141["slope"], g141["pooled"], g141["KPC"]
MUS, DELS, FOOTS = g141["MUS"], g141["DELS"], g141["FOOTS"]


def alpha_k21(x):
    x = min(max(x, 0.0), 4.0)
    return -0.146 * x * x + 1.204 * x + 1.475


def alpha_of(o, mode, re_fac, a_scale):
    if mode == "P2":
        return 2.0 * o["R"] / o["Rd"]
    return a_scale * alpha_k21(o["R"] / (re_fac * 1.68 * o["Rd"]) - 1.0)


def gobs4(o, mode="K21", re_fac=1.0, a_scale=1.0):
    al = alpha_of(o, mode, re_fac, a_scale)
    vc2 = o["V"] ** 2 + al * o["sig"] ** 2
    return vc2 * 1e6 / (o["R"] * KPC), vc2, al


def dlog4(o, mode="K21", re_fac=1.0, a_scale=1.0):
    _, vc2, al = gobs4(o, mode, re_fac, a_scale)
    V = o["V"]
    tv = 2 * V * o["eV"]
    ts = 2 * al * o["sig"] * o["esig"]
    inc = math.radians(o["inc"]) if np.isfinite(o["inc"]) and o["inc"] > 1 else math.radians(60)
    ti = 2 * V ** 2 * o["einc"] / math.tan(inc)
    return math.sqrt(tv ** 2 + ts ** 2 + ti ** 2) / vc2 / math.log(10)


def score4(objs, mu, dlt, foot, measured_gas=False, rival=False, mode="K21", re_fac=1.0, a_scale=1.0, per=False):
    D, S = [], []
    for o in objs:
        a = A0[foot] * (E(o["z"]) if rival else 1.0)
        gb = gbar(o, mu, dlt, measured_gas)
        gp = gpred(gb, a)
        go, _, _ = gobs4(o, mode, re_fac, a_scale)
        D.append(math.log10(go / gp)); S.append(math.hypot(dlog4(o, mode, re_fac, a_scale), slope(gb, a) * o["sm"]))
    return (pooled(D, S), np.array(D), np.array(S)) if per else pooled(D, S)


def grid(mode="K21", re_fac=1.0, a_scale=1.0):
    G = {}
    for mu in MUS:
        for dlt in DELS:
            for foot in FOOTS:
                kf, ekf = score4(KU2, mu, dlt, foot, mode=mode, re_fac=re_fac, a_scale=a_scale)
                kh, ekh = score4(KU2, mu, dlt, foot, rival=True, mode=mode, re_fac=re_fac, a_scale=a_scale)
                af, eaf = score4(SP, mu, dlt, foot, measured_gas=True, mode=mode, re_fac=re_fac, a_scale=a_scale)
                ah, eah = score4(SP, mu, dlt, foot, measured_gas=True, rival=True, mode=mode, re_fac=re_fac, a_scale=a_scale)
                G[(mu, dlt, foot)] = dict(df=kf - af, edf=math.hypot(ekf, eaf), dh=kh - ah, edh=math.hypot(ekh, eah))
    return G


def verdicts(Gd):
    fd = sum(1 for v in Gd.values() if v["df"] > 2 * v["edf"])
    rd_ = sum(1 for v in Gd.values() if v["dh"] < -2 * v["edh"])
    fw = sum(1 for v in Gd.values() if abs(v["df"]) <= 2 * v["edf"])
    rw = sum(1 for v in Gd.values() if abs(v["dh"]) <= 2 * v["edh"])
    return dict(flat_above_2s=fd, rival_below_m2s=rd_, flat_within_2s=fw, rival_within_2s=rw, n=len(Gd))


# ================================================================== C1 / C2
R.banner("C1 / C2  CONTROLS")
c141 = json.load(open(os.path.join(HERE, "CFG141_kurvs_measured_sigma" + ("_MUTATE" if MUTATE else "") + "_results.json")))["numbers"]["P2"]
GP2 = grid(mode="P2")
dev = max(abs(GP2[(mu, dlt, foot)][q] - c141[f"{mu}|{dlt}|{foot}"][q]) for mu in MUS for dlt in DELS for foot in FOOTS
          for q in ("df", "edf", "dh", "edh"))
check("C1 CONTROL: with alpha = 2R/R_d the P4 code path reproduces CFG141's committed P2 grid exactly (1e-12)",
      f"max |difference| {dev:.1e} over 24 cells x 4 quantities" + ("  [against CFG141's MUTATE grid]" if MUTATE else ""), dev < 1e-12)
a0_, a1_, a4_ = alpha_k21(0.0), alpha_k21(1.0), alpha_k21(4.0)
check("C2 CONTROL: alpha(0) = 1.475, alpha(1) = 2.533, alpha(4) = 3.955 (Kretschmer et al. 2021 Table 1, gas, disc)",
      f"alpha(0) {a0_:.4f}, alpha(1) {a1_:.4f}, alpha(4) {a4_:.4f}", abs(a0_ - 1.475) < 1e-12 and abs(a1_ - 2.533) < 1e-12 and abs(a4_ - 3.955) < 1e-12)

# ================================================================== the P4 grid, H1 / H2
R.banner("H1 / H2  UNDER P4 (Kretschmer et al. 2021 alpha, primary R_e = R_eff), anchor-corrected")
G4 = grid()
R0 = {k: (v["df"] - v["dh"]) / max(v["edf"], v["edh"]) for k, v in G4.items()}
check("R0 (reported) POWER under P4: separation of the two readings over the larger cell error",
      f"{min(R0.values()):.2f} .. {max(R0.values()):.2f} sigma across 24 cells", True, load_bearing=False)
for foot in FOOTS:
    P(f"    {foot} P4 (delta 0): " + "; ".join(f"mu {mu}: D'_flat {G4[(mu, 0.0, foot)]['df']:+.3f}+-{G4[(mu, 0.0, foot)]['edf']:.3f}, "
                                                f"D'_H {G4[(mu, 0.0, foot)]['dh']:+.3f}+-{G4[(mu, 0.0, foot)]['edh']:.3f}" for mu in MUS))
V4 = verdicts(G4)
check("H1 [HEADLINE] UNDER P4 THE FRAMEWORK'S FLAT a0 IS NOT DISFAVOURED: NOT (Delta'_flat > +2 sigma in every one of the 24 P4 cells)"
      + ("  [MUTATE: v x 2]" if MUTATE else ""),
      f"cells with flat > +2 sigma: {V4['flat_above_2s']}/24; flat within 2 sigma: {V4['flat_within_2s']}/24", V4["flat_above_2s"] < 24)
check("H2 (reported verdict) UNDER P4 THE RIVAL a0 ~ H(z) IS DISFAVOURED: Delta'_H < -2 sigma in every P4 cell",
      f"cells with rival < -2 sigma: {V4['rival_below_m2s']}/24; rival within 2 sigma: {V4['rival_within_2s']}/24",
      V4["rival_below_m2s"] == 24, load_bearing=False)

# ================================================================== R2 the decision cell, with the declared band and variant
R.banner("R2  the decision cell (mu = 0.67, delta = 0, canonical): P4 primary, the alpha x 0.6 / x 1.4 band, the R_e = 2 R_eff variant")
dec = {}
for name, kw in (("P4 primary", {}), ("alpha x 0.6", dict(a_scale=0.6)), ("alpha x 1.4", dict(a_scale=1.4)), ("R_e = 2 R_eff", dict(re_fac=2.0)),
                 ("P2 (CFG141)", dict(mode="P2"))):
    kf, ekf = score4(KU2, 0.67, 0.0, "canonical", **kw); kh, ekh = score4(KU2, 0.67, 0.0, "canonical", rival=True, **kw)
    af, eaf = score4(SP, 0.67, 0.0, "canonical", measured_gas=True, **kw); ah, eah = score4(SP, 0.67, 0.0, "canonical", measured_gas=True, rival=True, **kw)
    df, edf, dh, edh = kf - af, math.hypot(ekf, eaf), kh - ah, math.hypot(ekh, eah)
    dec[name] = dict(df=df, edf=edf, dh=dh, edh=edh)
    P(f"  {name:14s}: D'_flat {df:+.3f} +- {edf:.3f} ({df / edf:+.1f} sigma);  D'_H {dh:+.3f} +- {edh:.3f} ({dh / edh:+.1f} sigma)")
R.num("decision_cell", dec)

# ================================================================== R3 per galaxy
R.banner("R3  per galaxy (central cell mu = 0.67, delta = 0, canonical, unanchored)")
_, Df, _ = score4(KU2, 0.67, 0.0, "canonical", per=True)
_, Dh, _ = score4(KU2, 0.67, 0.0, "canonical", rival=True, per=True)
r3 = {}
for o, d, dh in zip(KU2, Df, Dh):
    x = o["R"] / (1.68 * o["Rd"]) - 1.0
    _, vc2, al = gobs4(o)
    fac4, fac2 = vc2 / o["V"] ** 2, (o["V"] ** 2 + 2 * o["sig"] ** 2 * o["R"] / o["Rd"]) / o["V"] ** 2
    r3[o["name"]] = dict(x=x, alpha=al, P4_fac=fac4, P2_fac=fac2, D_flat=float(d), D_H=float(dh))
    P(f"  {o['name']:9s}: x = R/R_e - 1 = {x:4.2f}, alpha {al:4.2f} (P2's 2R/R_d = {2 * o['R'] / o['Rd']:5.2f}); V_c^2/V^2 P4 {fac4:4.2f} vs P2 {fac2:4.2f}; "
      f"D_flat {d:+.2f}, D_H {dh:+.2f}")
R.num("R3", r3)

# ================================================================== R1 / R4 full grids and verdict rows for the variants
R.banner("R1 / R4  the P4 grid and the declared variants as full verdict rows")
rows = {}
for name, kw in (("P4 primary", {}), ("alpha x 0.6", dict(a_scale=0.6)), ("alpha x 1.4", dict(a_scale=1.4)), ("R_e = 2 R_eff", dict(re_fac=2.0))):
    Gv = G4 if name == "P4 primary" else grid(**kw)
    Vv = verdicts(Gv)
    rows[name] = dict(verdicts=Vv, grid={f"{k[0]}|{k[1]}|{k[2]}": v for k, v in Gv.items()})
    P(f"  {name:14s}: flat > +2 sigma in {Vv['flat_above_2s']}/24, flat within 2 sigma {Vv['flat_within_2s']}/24; "
      f"rival < -2 sigma in {Vv['rival_below_m2s']}/24, rival within 2 sigma {Vv['rival_within_2s']}/24")
    for foot in FOOTS:
        P(f"      {foot}, delta 0: " + "; ".join(f"mu {mu}: {Gv[(mu, 0.0, foot)]['df']:+.3f} / {Gv[(mu, 0.0, foot)]['dh']:+.3f}" for mu in MUS))
R.num("grids", rows)

d0 = dec["P4 primary"]
fw, rw = abs(d0["df"]) <= 2 * d0["edf"], abs(d0["dh"]) <= 2 * d0["edh"]
if fw and d0["dh"] < -2 * d0["edh"]:
    reading = "a Kretschmer-conditional lean toward flat a0 at z ~ 1.5 at the decision cell (gas unmeasured); NOT 'the data favour the framework'"
elif rw and d0["df"] > 2 * d0["edf"]:
    reading = "a Kretschmer-conditional lean toward the rival a0 ~ H(z) at the decision cell (gas unmeasured)"
else:
    reading = "non-diagnostic under P4 at the decision cell (both within 2 sigma, or both outside)"
R.num("reading", reading)
P(f"\n    READING (declared): {reading}")
nf = R.write()
raise SystemExit(1 if nf else 0)
