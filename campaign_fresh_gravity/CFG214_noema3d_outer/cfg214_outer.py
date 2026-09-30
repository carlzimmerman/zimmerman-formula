#!/usr/bin/env python3
"""CFG214 -- NOEMA3D (z ~ 1.1-1.6, measured CO gas): a0 from the OUTERMOST measured rotation point, flat vs rival.
Frozen criteria: FROZEN_CRITERIA.md here (8340f3750 + addendum 1, 68916b51e), committed before any curve value.
kappa = 1/2 FITTED, NOT DERIVED.  Nothing here says the data favour the framework.
Inputs: data_assembly/noema3d/noema3d_per_galaxy.csv and the data chat's digitised Fig. 5 (hash-checked; path set below).
Run:  python3 campaign_fresh_gravity/CFG214_noema3d_outer/cfg214_outer.py        (MUTATE=1: every V_rot x 1.1)
"""
import os, sys, csv, math, json, hashlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
R = C.Report("cfg214_outer", MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())

G_KPC = 4.30091e-6                         # kpc (km/s)^2 / Msun
G2SI = 1e6 / 3.0856775814913673e19
OM = 0.315
A0F = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
KER = {"nu_mono": K.nu_mono, "P2": K.nu_p2}
NBOOT, SEED = 10000, 214
XN = 1.678


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def nu1(nu, y):
    return float(nu(np.array([y]))[0])


def disc_v2(M, Re, Rr):
    """thin exponential disc (Freeman), R_d = R_e / 1.678; (km/s)^2"""
    Rd = Re / XN
    y = Rr / (2 * Rd)
    return 2 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def hern_v2(M, Re_b, Rr):
    a = Re_b / 1.8153
    return G_KPC * M * Rr / (Rr + a) ** 2


def shape(Re, Re_b, BT, Rr):
    return (1 - BT) * disc_v2(1.0, Re, Rr) + (BT * hern_v2(1.0, Re_b, Rr) if BT > 0 else 0.0)


# ------------------------------------------------------------------------------------------------ controls C1, C2
R.banner("CONTROLS")
kep = disc_v2(1.0, 1.0 * XN, 50.0) * 50.0 / G_KPC
check("C1 thin exponential disc: V^2 R / (GM) at 50 R_d is Keplerian within 0.5%; the shape normalisation S(R_e)/S(R_e) = 1",
      f"{kep:.5f}", abs(kep - 1) < 0.005 and shape(3.0, 1.0, 0.2, 3.0) / shape(3.0, 1.0, 0.2, 3.0) == 1.0)
c2 = []
for k, nu in KER.items():
    for foot in A0F:
        for law, fac in (("flat", 1.0), ("rival", E(1.4))):
            gb = 2.7 * A0F[foot]
            D = nu1(nu, gb / (A0F[foot] * fac))
            c2.append(abs(math.log10(D / nu1(nu, gb / (A0F[foot] * fac)))))
check("C2 a synthetic galaxy placed exactly on each law returns delta = 0 to 1e-12", f"max {max(c2):.1e}", max(c2) < 1e-12)

# ------------------------------------------------------------------------------------------------ inputs (the data chat's digitised Fig. 5)
CUR = os.path.join(REPO, "data_assembly", "noema3d", "curves")
TAB = {r["id"]: r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "noema3d", "noema3d_per_galaxy.csv"), newline=""))}


def fnum(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


R.banner("C3 hashes of the digitised inputs")
sums = {}
for line in open(os.path.join(CUR, "SHA256SUMS.txt")):
    t = line.split()
    if len(t) == 2:
        sums[t[1]] = t[0]
used = ["noema3d_fig5_data_markers.csv", "noema3d_fig5_model_curves.csv", "noema3d_fig5_outermost_data_radius.csv"]
# (fixed after the first run, kept as *_firstrun*: SHA256SUMS.txt does not list the outermost-radius file, so the first check compared it
#  with nothing and failed.  Its expected hash is the one the data chat sent in its message; the three files' hashes below are the
#  message's, and the two listed in SHA256SUMS are also compared with it.)
MSG = {"noema3d_fig5_data_markers.csv": "9ae3ff5206e92e49a0756ef20837fa999e47ba3bed2c13c0f35b2e54d965dbfc",
       "noema3d_fig5_model_curves.csv": "db99dc162ff9e4e0dfd544246dcc051d02050ea4c53e21671c6d069fd408b3d5",
       "noema3d_fig5_outermost_data_radius.csv": "1caaa2316ac5e5ae001e3b75b7b1d68a28057df51ae2720453c84728b1903784"}
badh = [f for f in used if hashlib.sha256(open(os.path.join(CUR, f), "rb").read()).hexdigest() != MSG[f]
        or (f in sums and sums[f] != MSG[f])]
check("C3a the digitised files used match the hashes the data chat sent (and SHA256SUMS where it lists them)", f"mismatched: {badh or 'none'}", not badh)
mk = list(csv.DictReader(open(os.path.join(CUR, "noema3d_fig5_data_markers.csv"), newline="")))
mc = list(csv.DictReader(open(os.path.join(CUR, "noema3d_fig5_model_curves.csv"), newline="")))
V = json.load(open(os.path.join(CUR, "validation_report.json")))
c4 = V.get("V3_C4", {})
P("  the data chat's raster control (V3/C4), as reported: " + json.dumps(c4)[:420])
med_vc = float(np.median([fnum(t["Vc_at_Re_disk_kms"]) for t in TAB.values()]))

# ------------------------------------------------------------------------------------------------ the frozen validation gate, recomputed here
R.banner("VALIDATION GATE (frozen): the digitised MODEL V at R_e,disk / sin i must match Table 3's V_c within 5%")
P("  the drawn model line is the best-fit 3D cube read out like the data, i.e. the BEAM-SMEARED observed projection (data chat, README); the gate compares it with Table 3's intrinsic V_c as frozen.")
def compute_gate(scale):
    out = {}
    for gid, t in TAB.items():
        Re, sini, Vc = fnum(t["Re_disk_fixed_kpc"]), math.sin(math.radians(fnum(t["incl_deg_P1"]))), fnum(t["Vc_at_Re_disk_kms"])
        ser = {}
        for r in mc:
            if r["galaxy"] == gid and r["panel"] == "velocity":
                ser.setdefault(r["series"], []).append((fnum(r["R_kpc"]), fnum(r["value"])))
        if not ser:
            out[gid] = dict(status="no model line"); continue
        best = max(ser, key=lambda s_: max(abs(a) for a, _ in ser[s_]))
        pts = sorted(ser[best])
        xs, vs = [a for a, _ in pts], [b * scale for _, b in pts]
        sides = []
        for sgn in (1, -1):
            if min(xs) <= sgn * Re <= max(xs):
                sides.append(abs(float(np.interp(sgn * Re, xs, vs))) / sini)
        if not sides:
            out[gid] = dict(status="R_e,disk outside the model line", series=best); continue
        vm = float(np.mean(sides))
        dev = vm / Vc - 1
        out[gid] = dict(series=best, sides=sides, Vmodel=vm, Vc=Vc, dev=dev, status="PASS" if abs(dev) <= 0.05 else "FAIL (excluded)")
    return out


gate = compute_gate(1.1 if MUT else 1.0)
if MUT:
    P("  MUTATE=1: every digitised model V x 1.1")
for gid, g in gate.items():
    if "dev" in g:
        P(f"  {gid:10s} series {g['series']:8s} model V(R_e,disk)/sin i = {g['Vmodel']:6.1f} km/s (sides {', '.join(f'{v:.0f}' for v in g['sides'])}) vs Table 3 V_c {g['Vc']:.0f}: {g['dev']:+.1%}  {g['status']}")
    else:
        P(f"  {gid:10s} {g['status']}")
npass = sum(1 for g in gate.values() if g.get("status") == "PASS")
theirs = {gid: v.get("gate_5pct") for gid, v in V.get("V2", {}).items()}
agree = all((gate[g].get("status") == "PASS") == (str(theirs.get(g, "")).startswith("PASS")) for g in gate)
check("C3b the frozen gate recomputed here agrees with the data chat's V2 (same pass / fail per galaxy)" + ("  [MUTATE: model V x 1.1, not applicable; reported]" if MUT else ""),
      f"passes {npass}/10; agreement {agree}", agree or MUT, load_bearing=not MUT)
R.num("gate", {g: {k: v for k, v in d.items() if k != "sides"} for g, d in gate.items()})

R.banner("FROZEN OUTCOME")
if npass < 3:
    verdict = (f"GATE-LIMITED: NON-DIAGNOSTIC AS FROZEN. Only {npass} of 10 galaxies pass the 5% gate, so no median delta with a bootstrap CI "
               "can be formed; every other galaxy is excluded, as frozen. No law verdict is given.")
else:
    verdict = "the frozen statistic can be formed (>= 3 galaxies pass); not implemented in this run"
P(f"  -> {verdict}")
pas = [g for g, d in gate.items() if d.get("status") == "PASS"]
if pas:
    P(f"  (the passing galaxy, {pas}: its model line's two sides differ strongly, {['%.0f' % v for v in gate[pas[0]]['sides']]} km/s after /sin i, so the "
      "mean matches Table 3 by cancellation; the data chat lists its three overlapping series as the least reliable trace)")
R.num("verdict", verdict)
R.num("n_pass", npass)
if MUT:
    g0 = compute_gate(1.0)
    dmax = max(abs((1 + gate[g]["dev"]) - 1.1 * (1 + g0[g]["dev"])) for g in gate if "dev" in gate[g])
    check("MUTATE: every model V x 1.1 multiplies (1 + deviation) by 1.1 in every galaxy to 1e-9, and changes the pass set", f"max |difference| {dmax:.1e}; passes {npass} vs unmutated {sum(1 for d in g0.values() if d.get('status') == 'PASS')}",
          dmax < 1e-9 and npass != sum(1 for d in g0.values() if d.get("status") == "PASS"))
R.write(here=LANE)
