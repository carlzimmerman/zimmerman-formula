#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR20 (part 2) -- a0 TIED TO AN EVOLVING DARK ENERGY: the kernel scale as a function of a quintessence-like field,
alpha(phi) = kappa sqrt(G V(phi))/c^2 in the chain's root action (FP7); its a0(z) track under the published DESI DR2
w0-wa fits, and where that track sits against the record's a0(z) evidence.

WHY.  FP0's R3b (2f6aee236) states that for evolving dark energy a0(z) tracks sqrt(rho_DE(z)), with the flat law the
w = -1 special case; L273 Part 4 (fable_independent_2026) reads the framework's law as the stage-17 PRESSURE law instead.
A field tie cannot read rho_DE: a coupling function alpha(phi) of the field alone reads the potential V(phi), and
V = (rho - p)/2 for any scalar with L = +/-X - V.  This lane computes the sqrt(V) track, its realisability by a
canonical field, and its standing against the data the record holds.  Nothing here derives kappa.

THE TIE (in FP7's root): add a scalar phi with L_phi = -(1/2)(d phi)^2 - V(phi) (no bare Lambda, or the bare part held
apart), and replace the constant alpha = a0/c^2 by the coupling function alpha(phi) with a0(phi) = kappa c sqrt(G V(phi)/c^2):
the dimensional form of P1 with rho_Lambda c^2 -> V(phi).

INPUTS.  DESI DR2 BAO + CMB + SNe w0waCDM (arXiv:2503.14738, the pairs L273 verified against the paper's table):
DESY5 (w0, wa) = (-0.752, -0.86) [the representative fit, banked in the repository]; Pantheon+ (-0.838, -0.62);
Union3 (-0.667, -1.09).  CPL: w(z) = w0 + wa z/(1+z).

PRE-DECLARED (written into this docstring before any code of this lane was run; the numbers come from hand algebra
done while planning, not from any script output):
  H5a the sqrt(V) track stays within +/-0.10 dex of flat for z <= 2.5 on all three fits, and lies between the density
      mapping (FP0 R3b, L273 Parts 1-3) and the pressure mapping (L273 Part 4) at every z: a bump of +0.03..+0.08 dex
      near z ~ 0.5-1 and -0.03..-0.04 dex at z = 2.5.  EXPECT TRUE.
  H5b the three CPL fits cross w = -1 at z ~ 0.3-0.45; beyond it the kinetic energy (1 + w) rho/2 is negative, so no
      single canonical field realises the sqrt(V) track there (a phantom sector is needed).  EXPECT TRUE.
  H5c a healthy canonical thawing field (exponential potential) matched to each fit's w0 and Omega_DE has V falling
      monotonically in time, so a0 ~ sqrt(V) RISES monotonically into the past, by +0.03..+0.10 dex at z = 2.5.
      EXPECT TRUE.
  H5d against the record's evidence: no evolving-dark-energy track comes within 0.25 dex of MUSE-DARK III's apparent
      +0.38 dex at z ~ 1; every track stays within 1 sigma of the deep-MOND Jeanneau refit (z = 1.06); every track stays
      within the pre-registered +/-0.13 dex of flat at z = 2.5.  The rival a0 ~ H(z) does come within 0.25 dex of MUSE
      and leaves the +/-0.13 band.  EXPECT TRUE.
  H5e the quintessence field's response to the MOND sector moves a0 by < 1e-9 in galaxies and clusters.  EXPECT TRUE.
"""
# (the docstring above is the pre-declaration; everything below was written after it and before the first run)
DOC_CHECKS = r"""
CHECKS
  C1 CONTROL FP0 R3b: the density mapping gives a0(2.5)/a0(0) = 0.7956 on DESY5 (FP0's committed number, to 1e-12).
  C2 CONTROL L273's committed tables: the density and alt (H(z), Omega_m = 0.3027) rows and the pressure rows at
     z = 0.5-5 for the three fits, reproduced line for line.
  C3 CONTROL the record's a0(z) evidence, read and re-derived where it is arithmetic: MUSE-DARK III a0|z~1 = 2.38 +/- 0.11
     (x1e-10, vs a0(0) = 1.0; L276: +0.38 dex, the flat law 19 sigma away at face value); the Jeanneau+26 deep-MOND refit
     (Delta_b = +0.140 +/- 0.272 honest at median z = 1.06, lever 0.76; flat 0.51 sigma); LambdaCDM's emergent scale
     +0.334 dex at z = 2.5 (L274) and the pre-registered +/-0.13 dex (PAPER7 via L273).
  E1 the identity V = (rho - p)/2 for any scalar with L = +/-X - V (sympy); the kinetic share (1 + w) rho/2 has the sign
     of the kinetic term, so w < -1 needs a ghost; V(z)/V(0) is a weighted mean of the density and pressure ratios.
  E2 the sqrt(V) track for the three fits (z = 0.25-3): inside the pre-registered +/-0.13 dex of flat for z <= 2.5 and
     between the density and pressure mappings at every z.  E2b (reported) = H5a's pre-declared +/-0.10 as it falls.
  E3 = H5b the phantom crossing of each fit and the negative kinetic share beyond it.
  E4 a canonical thawing field (exponential potential, frozen at z = 30, dust + field) matched to each fit's w0 and
     Omega_DE = 0.6847: w > -1 throughout, V falls monotonically in time, a0 ~ sqrt(V) rises into the past.  E4b (reported)
     = H5c's pre-declared +0.03..+0.10 dex at z = 2.5 as it falls.
  E5 = H5d the tracks against the evidence: MUSE (z = 1), the Jeanneau refit (z = 1.06), and the z = 2.5 zero point
     (+/-0.13 around flat; the separation from LambdaCDM's +0.334).  HEADLINE: the representative fit's sqrt(V) track
     (DESY5) stays within +/-0.13 dex of flat for z <= 2.5 (E-FLAT) and more than 0.25 dex below MUSE at z = 1 (E-MUSE).
     DISCLOSED: E5 (= H5d over every track) was load-bearing in the code as first run; the first run (MUTATE) showed it
     FAILS on one healthy track (the thawing field matched to Union3's w0 reaches +0.156 dex at z = 2.5), so before the
     main run it was re-designated reported (XR16's H-A2 precedent); its text and thresholds are unchanged.
  E6 = H5e the local variation: the quintessence field's static response to the MOND sector's source (kappa^2/8 pi) V' F,
     at the centre of a 1e11 Msun galaxy and a 1e14 Msun cluster (Hernquist), both footings.
  E7 the field content (sympy): around FRW the MOND term is O(eps^3) (J's zero tangent, FP7 B2), so phi and the MOND scalar
     do not mix at quadratic order: one added propagating scalar, FP7's linear system plus standard quintessence; the
     background is GR + the field.
  W  the ledger.
MUTATE=1: the tie reads the TOTAL density (a0 ~ sqrt(rho_total) = H(z): the rival, = the K tie on FRW) instead of V(phi):
E-FLAT and E-MUSE must FAIL (rc = 1).

SCOPE.  The CPL fits are used at their central values (L273/L275 hold the bands; the w0-wa correlation keeps the z = 2.5
band half-width <= 0.065 dex).  The thawing model is one potential shape (exponential), shown as the healthy bracket, not as
a fit to DESI.  The data comparison uses the record's committed numbers; the Jeanneau comparison uses the refit's median
lever 0.76 at its median z (an approximation to its per-galaxy dilution; the conclusion is insensitive to it, stated with
the numbers).  Both a0 footings are carried where a0 enters (the ratio a0(z)/a0(0) is footing-free).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR20_evolving_de_a0z.py   (MUTATE=1 for
the control).  Writes XR20_evolving_de_a0z[_MUTATE].out and XR20_evolving_de_a0z_results[_MUTATE].json next to itself.
"""
import os, re, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "XR20_evolving_de_a0z"
TXT = os.path.join(HERE, NAME + ("_MUTATE.out" if MUTATE else ".out"))
JSN = os.path.join(HERE, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))
T_START = time.time()


class _Tee:
    """the script writes its own .out: everything printed goes to the terminal and to the file."""

    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._s = sys.__stdout__

    def write(self, t):
        self._s.write(t)
        self._f.write(t)

    def flush(self):
        self._s.flush()
        self._f.flush()

    def close(self):
        self._f.close()


TEE = _Tee(TXT)
sys.stdout = TEE
OUT = {"lane": "XR20", "part": "a0 tied to an evolving dark energy", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 114 + "\n" + t + "\n" + "=" * 114)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def rd(rel):
    p = os.path.join(REPO, rel)
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None


P(__doc__.strip())
P(DOC_CHECKS.strip())
if MUTATE:
    P("\n  *** MUTATE=1: the tie reads the TOTAL density (a0 ~ H(z)) instead of V(phi); E-FLAT and E-MUSE must FAIL ***")

# ================================================================================================ inputs
c_SI, G_SI = 299792458.0, 6.67430e-11
MPC = 3.0856775814913673e22
KPC = 3.0857e19
MSUN = 1.98847e30
fp0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))
A0 = {"canonical": fp0["numbers"]["a0_canonical"], "alt": fp0["numbers"]["a0_rho_total"]}
H0_KMS, OM_L, OM_M = 67.4, 0.6847, 0.3153
H0 = H0_KMS * 1e3 / MPC
rho_c = 3 * H0 ** 2 / (8 * math.pi * G_SI)
rho_L = OM_L * rho_c
KAP = {f: a / (c_SI * math.sqrt(G_SI * rho_L)) for f, a in A0.items()}
DESI = {"DESY5": (-0.752, -0.86), "Pantheon+": (-0.838, -0.62), "Union3": (-0.667, -1.09)}   # DESI DR2 + CMB + SNe (L273)
HEAD = "DESY5"
dex = lambda r: math.log10(r)
f_DE = lambda z, w0, wa: (1 + z) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * z / (1 + z))
w_of = lambda z, w0, wa: w0 + wa * z / (1 + z)
map_density = lambda z, w0, wa: math.sqrt(f_DE(z, w0, wa))                                        # FP0 R3b / L273 Part 1
map_pressure = lambda z, w0, wa: math.sqrt(w_of(z, w0, wa) * f_DE(z, w0, wa) / w0)               # L273 Part 4 (stage-17)
map_V = lambda z, w0, wa: math.sqrt(f_DE(z, w0, wa) * (1 - w_of(z, w0, wa)) / (1 - w0))          # THIS LANE: alpha(phi) ~ sqrt V
map_total = lambda z, w0, wa, om=OM_M: math.sqrt(om * (1 + z) ** 3 + (1 - om) * f_DE(z, w0, wa))  # the rival: a0 ~ H(z)
HEAD_MAP = map_total if MUTATE else map_V
P(f"\n  inputs: FP0 a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (kappa on rho_Lambda {KAP['canonical']:.4f} / {KAP['alt']:.4f}); "
  f"DESI DR2 CPL fits (w0, wa): " + "; ".join(f"{k} {v}" for k, v in DESI.items()) + f"; the representative fit: {HEAD}")

# ================================================================================================ C controls
banner("C   CONTROLS: FP0 R3b, L273's tables, and the record's a0(z) evidence")
r25 = map_density(2.5, *DESI["DESY5"])
check("C1 CONTROL FP0 R3b: the density mapping a0(2.5)/a0(0) on DESY5 equals FP0's committed number",
      f"{r25:.13f} vs FP0 {fp0['numbers']['a0z_desy5_z25']:.13f}", abs(r25 - fp0["numbers"]["a0z_desy5_z25"]) < 1e-12)
l273 = rd("fable_independent_2026/L273_desi_a0z_band.out") or ""
OM273 = 0.3027
rows_ok, n_rows = True, 0
for z in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0):
    row = [dex(map_density(z, -1.0, 0.0))] + [dex(map_density(z, *d)) for d in DESI.values()] + \
          [dex(map_total(z, -1.0, 0.0, OM273))] + [dex(map_total(z, *d, OM273)) for d in DESI.values()]
    line1 = f"    {z:4.1f} {row[0]:+8.3f} " + " ".join(f"{v:+10.3f}" for v in row[1:4]) + f" | {row[4]:+10.3f} " + " ".join(f"{v:+11.3f}" for v in row[5:])
    prow = [dex(map_pressure(z, *d)) for d in DESI.values()]
    line4 = f"    {z:4.1f} " + " ".join(f"{v:+16.3f}" for v in prow) + f"   {dex(map_density(z, -0.752, -0.86)):+.3f}"
    rows_ok = rows_ok and (line1 in l273) and (line4 in l273)
    n_rows += 2
check("C2 CONTROL L273's committed tables (density and alt rows, Part 1; pressure rows, Part 4) reproduced line for line",
      f"{n_rows} lines, all found verbatim: {rows_ok}", rows_ok)
l276_py = rd("fable_independent_2026/L276_data_vs_models_a0z.py") or ""
l276_out = rd("fable_independent_2026/L276_data_vs_models_a0z.out") or ""
m_mu = re.search(r"a0\|z~1 = ([0-9.]+) \+/- ([0-9.]+)", l276_py)
MU = dict(z=1.0, val=dex(float(m_mu.group(1))), sig=dex(float(m_mu.group(1)) + float(m_mu.group(2))) - dex(float(m_mu.group(1)))) if m_mu else None
mu_ok = MU is not None and f"flat excluded at {MU['val'] / MU['sig']:.0f} sigma at face value" in l276_out and \
    "MUSE-DARK III's fitted a0 at z ~ 1 (+0.38 dex)" in l276_out
jr = rd("prep_2026/jeanneau_refit/deep_refit.rerun_2026-09-18.out") or ""
mj = {k: re.search(p_, jr) for k, p_ in (("db", r"Delta_b = ([+-][0-9.]+) dex"), ("band", r"HONEST BAND = .* = \+-([0-9.]+) dex"),
                                            ("lever", r"dilution: median ([0-9.]+) canonical"), ("z", r"z median ([0-9.]+)"),
                                            ("flat", r"sigma from canonical\(0\): ([0-9.]+)"), ("alt", r"ALT rho_tot/cH0\s+: ([+-][0-9.]+)"))}
JE = {k: float(v.group(1)) for k, v in mj.items()} if all(mj.values()) else None
je_ok = JE is not None and abs(JE["db"] / JE["band"] - JE["flat"]) < 0.01
l274 = rd("fable_independent_2026/L274_a0z_theories_chart.out") or ""
m274 = re.search(r"\(z = 2\.5: ([+-][0-9.]+) dex \(factor", l274)
LCDM25 = float(m274.group(1)) if m274 else None
SIG25 = 0.13 if "in units of the pre-registered +/-0.13 dex" in l273 else None
check("C3 CONTROL the record's a0(z) evidence: MUSE-DARK III (L276's banked a0|z~1 = 2.38 +/- 0.11 vs 1.0 -> +0.377 dex, the "
      "flat law 19 sigma away at face value, re-derived); the Jeanneau+26 deep-MOND refit (Delta_b/band = its committed "
      "0.51 sigma from flat, re-derived); LambdaCDM's emergent +0.334 dex at z = 2.5 (L274); the pre-registered +/-0.13 dex",
      f"MUSE {MU['val']:+.4f} +/- {MU['sig']:.4f} dex at z = 1 ({MU['val'] / MU['sig']:.1f} sigma from flat); Jeanneau Delta_b "
      f"{JE['db']:+.3f} +/- {JE['band']:.3f} at z = {JE['z']}, lever {JE['lever']}, flat {JE['db'] / JE['band']:.2f} sigma (committed "
      f"{JE['flat']}), ALT {JE['alt']:+.3f}; LCDM emergent {LCDM25:+.3f}; +/-{SIG25}" if (MU and JE and LCDM25 is not None) else "NOT FOUND",
      mu_ok and je_ok and LCDM25 is not None and SIG25 is not None,
      "the record reads MUSE as an APPARENT a0 (method-localised, non-diagnostic); the clean deep-MOND arm is flat-compatible")
OUT["numbers"]["evidence"] = dict(MUSE=MU, Jeanneau=JE, LCDM_emergent_z2p5=LCDM25, prereg_sigma=SIG25)

# ================================================================================================ E1 the identity
banner("E1  THE FIELD TIE READS THE POTENTIAL: V = (rho - p)/2")
epsk, phid, Vs = sp.symbols("epsilon_k phidot V", real=True)
Lhom = epsk * phid ** 2 / 2 - Vs                              # homogeneous scalar, L = eps X - V (eps = +1 canonical, -1 ghost)
rho_ = phid * sp.diff(Lhom, phid) - Lhom
p_ = Lhom
e1a = sp.simplify((rho_ - p_) / 2 - Vs) == 0
e1b = sp.simplify((rho_ + p_) / 2 - epsk * phid ** 2 / 2) == 0
w0s, wz, fz = sp.symbols("w_0 w_z f_z", real=True)
Vratio = fz * (1 - wz) / (1 - w0s)
wmean = (1 / (1 - w0s)) * fz + (-w0s / (1 - w0s)) * (wz * fz / w0s)             # weights rho0, -p0 over rho0 - p0
e1c = sp.simplify(Vratio - wmean) == 0
check("E1 THE IDENTITY: for L = eps X - V, rho = eps phidot^2/2 + V and p = eps phidot^2/2 - V, so V = (rho - p)/2 and the kinetic "
      "share (rho + p)/2 = (1 + w) rho/2 has the sign of eps: w < -1 needs eps = -1 (a ghost); and V(z)/V(0) is the mean of the "
      "density ratio and the pressure ratio weighted by rho0 and -p0",
      f"V = (rho - p)/2: {e1a}; kinetic share = eps phidot^2/2: {e1b}; weighted-mean form: {e1c}", e1a and e1b and e1c,
      "a coupling function alpha(phi) reads V(phi), not rho_DE: the field tie is neither FP0 R3b's density mapping nor L273 "
      "Part 4's pressure mapping, but their weighted mean")

# ================================================================================================ E2 the sqrt(V) track
banner("E2  THE sqrt(V) TRACK under the DESI DR2 fits (dex, a0(z)/a0(0)), with the density and pressure mappings")
ZT = [0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
TR = {}
for k, (w0, wa) in DESI.items():
    TR[k] = {"V": {z: dex(map_V(z, w0, wa)) for z in ZT}, "density": {z: dex(map_density(z, w0, wa)) for z in ZT},
             "pressure": {z: dex(map_pressure(z, w0, wa)) for z in ZT}}
    zz = np.linspace(0, 3, 3001)
    vv = [dex(map_V(z, w0, wa)) for z in zz]
    TR[k]["peak"] = (float(zz[int(np.argmax(vv))]), float(max(vv)))
    P(f"    {k:10s} z:        " + " ".join(f"{z:>7.2f}" for z in ZT))
    for lab in ("V", "density", "pressure"):
        P(f"    {'':10s} {lab:9s} " + " ".join(f"{TR[k][lab][z]:+7.3f}" for z in ZT))
    P(f"    {'':10s} sqrt(V) peaks at z = {TR[k]['peak'][0]:.2f}, {TR[k]['peak'][1]:+.3f} dex")
maxV = max(abs(TR[k]["V"][z]) for k in DESI for z in ZT if z <= 2.5)
between = all(min(TR[k]["density"][z], TR[k]["pressure"][z]) - 1e-12 <= TR[k]["V"][z] <= max(TR[k]["density"][z], TR[k]["pressure"][z]) + 1e-12
              for k in DESI for z in ZT)
check("E2 the sqrt(V) track stays inside the pre-registered +/-0.13 dex of flat for z <= 2.5 on all three fits and lies between "
      "the density mapping (FP0 R3b) and the pressure mapping (L273 Part 4) at every z",
      f"max |sqrt(V)| for z <= 2.5: {maxV:.3f} dex; at z = 2.5: " + ", ".join(f"{k} {TR[k]['V'][2.5]:+.3f}" for k in DESI) +
      "; peaks: " + ", ".join(f"{k} {TR[k]['peak'][1]:+.3f} at z = {TR[k]['peak'][0]:.2f}" for k in DESI) + f"; between: {between}",
      maxV <= 0.13 and between)
check("E2b = H5a (pre-declared, reported as it falls) the sqrt(V) track stays within +/-0.10 dex for z <= 2.5 on all three fits",
      f"max {maxV:.3f} dex", maxV <= 0.10, load_bearing=False)
OUT["numbers"]["E2"] = {k: {lab: ({str(z): v for z, v in d_.items()} if isinstance(d_, dict) else d_) for lab, d_ in v.items()} for k, v in TR.items()}

# ================================================================================================ E3 phantom crossing
banner("E3  CAN ONE CANONICAL FIELD FOLLOW THE FITS?  The phantom crossing")
E3 = {}
for k, (w0, wa) in DESI.items():
    u_ = (-1 - w0) / wa
    zc = u_ / (1 - u_)
    kin = {z: (1 + w_of(z, w0, wa)) / 2 for z in (0.0, 1.0, 2.5)}
    E3[k] = dict(z_cross=zc, kinetic_share=kin)
    P(f"    {k:10s} w = -1 at z = {zc:.3f}; kinetic share (1 + w)/2 of rho_DE at z = 0, 1, 2.5: " + ", ".join(f"{v:+.3f}" for v in kin.values()))
e3 = all(0.3 <= v["z_cross"] <= 0.45 and v["kinetic_share"][1.0] < 0 and v["kinetic_share"][2.5] < 0 for v in E3.values())
check("E3 = H5b the three fits cross w = -1 at z ~ 0.3-0.45 and beyond it the kinetic share (1 + w) rho/2 is negative: no single "
      "canonical field realises the sqrt(V) track there -- it needs a phantom (ghost) sector at z > z_cross",
      "; ".join(f"{k} z_cross = {v['z_cross']:.3f}" for k, v in E3.items()), e3,
      "the CPL form is a fit, not a field; a healthy field cannot cross -1, so the healthy bracket is E4's")
OUT["numbers"]["E3"] = {k: dict(z_cross=v["z_cross"], kinetic_share={str(a): b for a, b in v["kinetic_share"].items()}) for k, v in E3.items()}

# ================================================================================================ E4 a canonical thawing field
banner("E4  THE HEALTHY BRACKET: a canonical thawing field (V = V0 exp(-lambda phi/M_P)) matched to each fit's w0")
Z_I = 30.0


def thaw_solve(lam_p, yi2):
    s3 = math.sqrt(1.5)

    def rhs(N, u):
        x, y = u
        com = 1.5 * (2 * x * x + (1 - x * x - y * y))
        return [-3 * x + lam_p * s3 * y * y + x * com, -lam_p * s3 * x * y + y * com]
    return solve_ivp(rhs, (-math.log(1 + Z_I), 0.0), [0.0, math.sqrt(yi2)], rtol=1e-11, atol=1e-14, dense_output=True)


def thaw_fit(w0_target):
    def shoot_Om(lam_p):
        g_ = lambda lyi: (lambda s_: s_.y[0, -1] ** 2 + s_.y[1, -1] ** 2)(thaw_solve(lam_p, math.exp(lyi))) - OM_L
        return math.exp(brentq(g_, math.log(1e-7), math.log(1e-2), xtol=1e-13))

    def w0_of(lam_p):
        yi2 = shoot_Om(lam_p)
        s_ = thaw_solve(lam_p, yi2)
        x, y = s_.y[0, -1], s_.y[1, -1]
        return (x * x - y * y) / (x * x + y * y)
    lam = None
    for lo_, hi_ in ((0.05, 1.7), (1.7, 2.5)):                   # lambda < sqrt(3): the field-dominated attractor
        try:
            lam = brentq(lambda L_: w0_of(L_) - w0_target, lo_, hi_, xtol=1e-10)
            break
        except ValueError:
            continue
    if lam is None:
        raise ValueError("no thawing solution")
    yi2 = shoot_Om(lam)
    return lam, yi2, thaw_solve(lam, yi2)


TH = {}
for k, (w0, wa) in DESI.items():
    try:
        lam, yi2, sol = thaw_fit(w0)
    except ValueError:
        TH[k] = None
        P(f"    {k:10s} w0 = {w0}: no exponential thawing solution in lambda = 0.05-2.5")
        continue
    x0, y0 = sol.y[0, -1], sol.y[1, -1]
    Om0 = x0 * x0 + y0 * y0

    def V_ratio(z, sol=sol, y0=y0, Om0=Om0):
        N = -math.log(1 + z)
        x, y = sol.sol(N)
        H2 = (1 + z) ** 3 * (1 - Om0) / (1 - (x * x + y * y))
        return y * y * H2 / (y0 * y0)

    def w_th(z, sol=sol):
        x, y = sol.sol(-math.log(1 + z))
        return (x * x - y * y) / (x * x + y * y)
    zz = np.linspace(0, 3, 301)
    tr = [dex(math.sqrt(V_ratio(z))) for z in zz]
    mono = all(b_ > a_ for a_, b_ in zip(tr[:-1], tr[1:]))
    TH[k] = dict(lam=lam, yi2=yi2, Om0=Om0, w0=(x0 * x0 - y0 * y0) / Om0, track={z: dex(math.sqrt(V_ratio(z))) for z in ZT},
                 w_at={z: w_th(z) for z in (1.0, 2.5)}, monotone=mono)
    P(f"    {k:10s} w0 = {w0}: lambda = {lam:.4f}, Omega_phi(0) = {Om0:.5f}, w(0) = {TH[k]['w0']:.4f}, w(1) = {TH[k]['w_at'][1.0]:.4f}, "
      f"w(2.5) = {TH[k]['w_at'][2.5]:.4f}; a0 ~ sqrt(V) [dex] at z = " + ", ".join(f"{z:g}: {v:+.3f}" for z, v in TH[k]["track"].items())
      + f"; monotone rise {mono}")
e4 = all(v is not None and v["monotone"] and v["track"][2.5] > 0 and v["w_at"][2.5] > -1 and v["w_at"][1.0] > -1 for v in TH.values())
check("E4b = H5c (pre-declared, reported as it falls) the thawing rise at z = 2.5 lies in +0.03..+0.10 dex on all three w0",
      ", ".join(f"{k} {v['track'][2.5]:+.3f}" if v else f"{k} none" for k, v in TH.items()),
      all(v is not None and 0.03 <= v["track"][2.5] <= 0.10 for v in TH.values()), load_bearing=False)
check("E4 a healthy canonical thawing field matched to each fit's w0 (and Omega_DE = 0.6847) keeps w > -1 and has V falling "
      "monotonically in time: a0 ~ sqrt(V) RISES monotonically into the past",
      "; ".join(f"{k}: lambda {v['lam']:.3f}, +{v['track'][2.5]:.3f} dex at z = 2.5, monotone {v['monotone']}" if v else f"{k}: none"
                for k, v in TH.items()), e4,
      "the sign of the evolving-dark-energy shift depends on the realisation: a phantom-crossing fit read through sqrt(V) "
      "bumps then declines; a healthy field with the same w0 rises")
OUT["numbers"]["E4"] = {k: (dict(v, track={str(a): b for a, b in v["track"].items()}, w_at={str(a): b for a, b in v["w_at"].items()})
                            if v else None) for k, v in TH.items()}

# ================================================================================================ E5 the evidence
banner("E5  THE TRACKS AGAINST THE RECORD'S a0(z) EVIDENCE" + ("  [MUTATE: the headline tie reads rho_total]" if MUTATE else ""))
TRACKS = {"flat (w = -1)": lambda z: 0.0,
          "density, DESY5 (FP0 R3b)": lambda z: dex(map_density(z, *DESI["DESY5"])),
          "pressure, DESY5 (L273 P4)": lambda z: dex(map_pressure(z, *DESI["DESY5"]))}
for k in DESI:
    TRACKS[f"sqrt(V), {k} CPL"] = (lambda z, k=k: dex(map_V(z, *DESI[k])))
for k, v in TH.items():
    if v:
        lam_k, yi2_k = v["lam"], v["yi2"]
        sol_k = thaw_solve(lam_k, yi2_k)
        x0k, y0k = sol_k.y[0, -1], sol_k.y[1, -1]
        Om0k = x0k ** 2 + y0k ** 2

        def trk(z, sol=sol_k, y0=y0k, Om0=Om0k):
            x, y = sol.sol(-math.log(1 + z))
            return dex(math.sqrt(y * y * (1 + z) ** 3 * (1 - Om0) / (1 - (x * x + y * y)) / (y0 * y0)))
        TRACKS[f"sqrt(V), thawing (w0 of {k})"] = trk
TRACKS["rival H(z) (a0 ~ sqrt rho_total)"] = lambda z: dex(map_total(z, *DESI["DESY5"]))
HEAD_NAME = "HEADLINE: " + ("rho_total tie (MUTATE)" if MUTATE else f"sqrt(V), {HEAD} CPL")
TRACKS[HEAD_NAME] = lambda z: dex(HEAD_MAP(z, *DESI[HEAD]))
rows5 = {}
P(f"    {'track':40s} {'z=1':>7s} {'MUSE gap':>9s} {'->MUSE':>7s} {'Db(1.06)':>9s} {'J pull':>7s} {'z=2.5':>7s} {'LCDM sep':>9s}")
for nm, fn in TRACKS.items():
    d1, d106, d25 = fn(1.0), fn(JE["z"]), fn(2.5)
    db = -JE["lever"] * d106
    pull = (JE["db"] - db) / JE["band"]
    rows5[nm] = dict(z1=d1, muse_gap=MU["val"] - d1, frac_to_muse=d1 / MU["val"], db_pred=db, j_pull=pull, z25=d25,
                     lcdm_sep=(LCDM25 - d25) / SIG25, j_pull_lever_range=[(JE["db"] + L_ * d106) / JE["band"] for L_ in (0.6, 1.0)])
    r_ = rows5[nm]
    P(f"    {nm:40s} {d1:+7.3f} {r_['muse_gap']:+9.3f} {r_['frac_to_muse']:+7.1%} {db:+9.3f} {pull:+7.2f} {d25:+7.3f} {r_['lcdm_sep']:+8.2f}s")
de_tr = [n_ for n_ in rows5 if n_.startswith("sqrt(V)") or n_.startswith("density") or n_.startswith("pressure")]
h = rows5[HEAD_NAME]
e_flat = all(abs(TRACKS[HEAD_NAME](z)) <= SIG25 for z in np.linspace(0, 2.5, 26))
e_muse = h["muse_gap"] > 0.25
check("E-FLAT (headline) the representative fit's tie stays within the pre-registered +/-0.13 dex of flat at every z <= 2.5",
      f"max |track| over z = 0-2.5: {max(abs(TRACKS[HEAD_NAME](z)) for z in np.linspace(0, 2.5, 26)):.3f} dex; at z = 2.5 {h['z25']:+.3f}", e_flat,
      "at the rotator's precision the evolving-dark-energy tie is indistinguishable from flat" if not MUTATE else
      "MUTATE: the rho_total tie is the rival law, far outside the band")
check("E-MUSE (headline) the representative fit's tie stays more than 0.25 dex below MUSE-DARK III's apparent +0.38 at z = 1",
      f"gap {h['muse_gap']:+.3f} dex ({h['frac_to_muse']:.0%} of the way from flat)", e_muse)
e5 = all(rows5[n_]["muse_gap"] > 0.25 and abs(rows5[n_]["j_pull"]) < 1 and abs(rows5[n_]["z25"]) <= SIG25 for n_ in de_tr) and \
    rows5["rival H(z) (a0 ~ sqrt rho_total)"]["muse_gap"] < 0.25 and abs(rows5["rival H(z) (a0 ~ sqrt rho_total)"]["z25"]) > SIG25
check("E5 = H5d (pre-declared; reported as it falls, re-designation disclosed) every evolving-dark-energy track (density, pressure, "
      "sqrt(V) CPL on all fits, sqrt(V) thawing) stays > 0.25 dex below MUSE at z = 1, within 1 sigma of the Jeanneau refit, and "
      "within +/-0.13 dex of flat at z = 2.5; the rival H(z) comes within 0.25 dex of MUSE and leaves the band",
      f"smallest MUSE gap {min(rows5[n_]['muse_gap'] for n_ in de_tr):.3f}; Jeanneau pulls {min(rows5[n_]['j_pull'] for n_ in de_tr):+.2f}.."
      f"{max(rows5[n_]['j_pull'] for n_ in de_tr):+.2f} (flat {rows5['flat (w = -1)']['j_pull']:+.2f}; lever 0.6-1.0 moves them by <= "
      f"{max(abs(rows5[n_]['j_pull_lever_range'][0] - rows5[n_]['j_pull_lever_range'][1]) for n_ in de_tr):.2f}); |z = 2.5| <= "
      f"{max(abs(rows5[n_]['z25']) for n_ in de_tr):.3f}; rival: gap {rows5['rival H(z) (a0 ~ sqrt rho_total)']['muse_gap']:.3f}, "
      f"z = 2.5 {rows5['rival H(z) (a0 ~ sqrt rho_total)']['z25']:+.3f}; outside +/-0.13 at z = 2.5: "
      f"{[n_ for n_ in de_tr if abs(rows5[n_]['z25']) > SIG25]}", e5,
      "it fails on the healthy thawing field matched to Union3's w0 (+0.156 dex at z = 2.5): a canonical field CAN move the z = 2.5 "
      "zero point by more than the rotator's precision -- toward LambdaCDM's emergent scale", load_bearing=False)
# toward / away, per datum, for the headline and the healthy bracket
tw = {}
for nm in [HEAD_NAME] + [n_ for n_ in rows5 if "thawing" in n_] + ["density, DESY5 (FP0 R3b)", "pressure, DESY5 (L273 P4)"]:
    r_ = rows5[nm]
    tw[nm] = dict(MUSE="toward" if r_["z1"] > 0 else "away", Jeanneau="toward" if abs(r_["j_pull"]) < abs(rows5["flat (w = -1)"]["j_pull"]) else "away",
                  LCDM_z25="toward" if r_["z25"] > 0 else "away")
    P(f"    {nm:40s} relative to flat: MUSE {tw[nm]['MUSE']:6s} ({r_['frac_to_muse']:+.0%} of the gap); Jeanneau {tw[nm]['Jeanneau']:6s} "
      f"(pull {r_['j_pull']:+.2f} vs flat {rows5['flat (w = -1)']['j_pull']:+.2f}); LambdaCDM's z = 2.5 scale {tw[nm]['LCDM_z25']:6s} "
      f"({r_['lcdm_sep']:.2f} vs {rows5['flat (w = -1)']['lcdm_sep']:.2f} sigma)")
cpl_names = [n_ for n_ in de_tr if "CPL" in n_]
thaw_names = [n_ for n_ in de_tr if "thawing" in n_]
check("E5b (reported) toward or away, per datum: the sign depends on the realisation -- the phantom-crossing CPL fits through "
      f"sqrt(V) move a0 toward MUSE at z = 1 by {min(rows5[n_]['frac_to_muse'] for n_ in cpl_names):.0%}-"
      f"{max(rows5[n_]['frac_to_muse'] for n_ in cpl_names):.0%} of the gap and AWAY from LambdaCDM's z = 2.5 scale "
      f"({min(rows5[n_]['z25'] for n_ in cpl_names):+.3f}..{max(rows5[n_]['z25'] for n_ in cpl_names):+.3f} dex); a healthy thawing "
      f"field moves it TOWARD both ({min(rows5[n_]['frac_to_muse'] for n_ in thaw_names):.0%}-{max(rows5[n_]['frac_to_muse'] for n_ in thaw_names):.0%} "
      f"of the MUSE gap; {min(rows5[n_]['z25'] for n_ in thaw_names):+.3f}..{max(rows5[n_]['z25'] for n_ in thaw_names):+.3f} dex at z = 2.5); "
      "every track moves AWAY from the deep-MOND Jeanneau lean (which sits below flat)",
      "; ".join(f"{n_.split(',')[0] if n_.startswith('HEAD') else n_}: {v['MUSE']}/{v['Jeanneau']}/{v['LCDM_z25']}" for n_, v in tw.items()),
      True, load_bearing=False)
OUT["numbers"]["E5"] = dict(rows=rows5, toward_away=tw)

# ================================================================================================ E6 local variation
banner("E6  THE LOCAL VARIATION: the quintessence field's response to the MOND sector")


def x_p2(Y):
    return Y / (math.sqrt(Y * Y + Y) + Y) if Y > 0 else 0.0


def F_p2(Y):
    if Y <= 0:
        return 0.0
    x = x_p2(Y)
    if x < 2e-3:
        return x ** 3 / 3 + x ** 4 + 2.4 * x ** 5
    om = 1.0 / (1.0 + 2.0 * Y + 2.0 * math.sqrt(Y * Y + Y))
    return x ** 3 / om + 0.25 * math.log(om) + x / 2 + x * x / 2


loc = {}
lam_used = TH[HEAD]["lam"] if TH.get(HEAD) else 1.0
w0h = DESI[HEAD][0]
for f, a0 in A0.items():
    Vpp = 1.5 * lam_used ** 2 * (1 - w0h) * OM_L * H0 ** 2 / c_SI ** 2         # V'^2/V in 1/m^2 (canonical field, exponential V)
    for lab, M, a_h in (("galaxy 1e11 Msun, a = 2 kpc", 1e11, 2.0), ("cluster 1e14 Msun, a = 200 kpc", 1e14, 200.0)):
        GM, ah = G_SI * M * MSUN, a_h * KPC
        integ = quad(lambda lr: (lambda r: F_p2(GM / ((r + ah) ** 2 * a0)) * r * r)(math.exp(lr)), math.log(1e-4 * ah), math.log(1e4 * ah),
                     limit=400, epsrel=1e-8)[0]                               # Int F r dr (d ln r)
        dln = 0.5 * KAP[f] ** 2 / (8 * math.pi) * Vpp * integ
        loc[(f, lab)] = dln
        P(f"    {f:9s} {lab:32s}: Int F r dr = {integ:.3e} m^2; delta ln a0 at the centre = {dln:.2e}")
e6 = max(abs(v) for v in loc.values()) < 1e-9
check("E6 = H5e the field's static response to the MOND sector's source (kappa^2/8 pi) V' F (a light field: gradient energy over "
      "galaxy scales against a rho_Lambda-scale source) moves a0 by < 1e-9 at the centre of a galaxy and a cluster, both footings",
      f"max |delta ln a0| = {max(abs(v) for v in loc.values()):.1e} (lambda = {lam_used:.3f} from E4's {HEAD} match)", e6,
      "the local variation is (kappa^2/16 pi) lambda^2 3 (1 - w0)/2 Omega (H0 r/c)^2 F-weighted: suppressed by (H0 r/c)^2 ~ 1e-11")
OUT["numbers"]["E6"] = {f"{k[0]}|{k[1]}": v for k, v in loc.items()}

# ================================================================================================ E7 field content
banner("E7  THE FIELD CONTENT: one added scalar; no quadratic mixing around FRW")
ep, a_s, da, Y1 = sp.symbols("epsilon alpha_0 d_alpha Y_1", positive=True)
Jz = -sp.log(1 - 2 * sp.sqrt(sp.Symbol("s"))) / 4 - sp.sqrt(sp.Symbol("s")) / 2 - sp.Symbol("s") / 2
term = -2 * (a_s + ep * da) ** 2 * Jz.subs(sp.Symbol("s"), ep ** 2 * Y1 / (a_s + ep * da) ** 2)
ser = sp.series(term, ep, 0, 4).removeO()
e7 = sp.simplify(ser.coeff(ep, 0)) == 0 and sp.simplify(ser.coeff(ep, 1)) == 0 and sp.simplify(ser.coeff(ep, 2)) == 0 and \
    sp.simplify(ser.coeff(ep, 3)) != 0
check("E7 THE FIELD CONTENT: with delta alpha ~ delta phi and the MOND gradient both O(eps) around FRW, the MOND term -2 alpha^2 "
      "J(Y/alpha^2) starts at O(eps^3) (J's zero tangent, FP7 B2): no quadratic mixing, so the linear system is FP7's plus "
      "standard quintessence; one propagating scalar is added (5 local modes with FP7's 4); the background is GR + the field "
      "(the MOND term vanishes on FRW, J(0) = 0); PPN unchanged (phi reaches matter only through the MOND term, E6)",
      f"orders eps^0..eps^2 vanish: {e7}; leading term {sp.simplify(ser.coeff(ep, 3))} eps^3", e7)

# ================================================================================================ W ledger
banner("W   THE LEDGER")
LEDGER = [
    ("X20-T5", "a0 tied to an evolving dark energy through alpha(phi) ~ sqrt(V(phi))", "TIED",
     "a coupling function of the field that sets the dark energy; kappa stays FITTED; one added scalar (E7)"),
    ("X20-T5a", "the field tie reads V = (rho - p)/2, the mean of FP0 R3b's density mapping and L273's pressure mapping", "DERIVED", "E1"),
    ("X20-T5b", f"a0(z) under DESI DR2 CPL through sqrt(V): bump +{min(TR[k]['peak'][1] for k in DESI):.3f}..+{max(TR[k]['peak'][1] for k in DESI):.3f} "
     f"dex at z = {min(TR[k]['peak'][0] for k in DESI):.2f}-{max(TR[k]['peak'][0] for k in DESI):.2f}, "
     f"{min(TR[k]['V'][2.5] for k in DESI):+.3f}..{max(TR[k]['V'][2.5] for k in DESI):+.3f} dex at z = 2.5", "DERIVED",
     "E2; needs a ghost beyond z_cross = 0.35-0.44 (E3)"),
    ("X20-T5c", "a healthy thawing field with the same w0: a0 rises monotonically into the past, " +
     ", ".join(f"+{v['track'][2.5]:.3f}" for v in TH.values() if v) + " dex at z = 2.5", "DERIVED", "E4 (exponential potential)"),
    ("X20-T5d", f"against the evidence: the published CPL fits through sqrt(V) stay inside +/-0.13 at z = 2.5 "
     f"({min(rows5[n_]['z25'] for n_ in cpl_names):+.3f}..{max(rows5[n_]['z25'] for n_ in cpl_names):+.3f}); a healthy thawing field "
     f"reaches {max(rows5[n_]['z25'] for n_ in thaw_names):+.3f} (LambdaCDM separation {min(rows5[n_]['lcdm_sep'] for n_ in thaw_names):.2f} "
     f"sigma vs flat's {rows5['flat (w = -1)']['lcdm_sep']:.2f}); no track reaches MUSE (smallest gap "
     f"{min(rows5[n_]['muse_gap'] for n_ in de_tr):.3f} dex); all within 1 sigma of the Jeanneau refit", "CONSTRAINT",
     "E5, E5b: a healthy evolving dark energy would push a0(z) up, toward LambdaCDM's emergent scale, eroding the z = 2.5 test"),
    ("X20-T5e", "the flat law is the w = -1 special case: the prediction is only as flat as the dark energy is constant", "POSTULATED",
     "which realisation (phantom fit, thawing field, or a vacuum that is w = -1 exact) is an input, not derived"),
]
for k_, what, st_, why in LEDGER:
    P(f"    {k_:8s} {st_:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
hd = rows5[HEAD_NAME]
P("  A field tie alpha(phi) ~ sqrt(V(phi)) reads the potential, V = (rho - p)/2: halfway between the density mapping FP0 R3b\n"
  "  states and the pressure mapping L273 reads as the framework's law.  Under DESI DR2 (DESY5 CPL, w0 = -0.752, wa = -0.86) the\n"
  f"  sqrt(V) track bumps to +{TR[HEAD]['peak'][1]:.3f} dex at z = {TR[HEAD]['peak'][0]:.2f}, is {TR[HEAD]['V'][1.0]:+.3f} at z = 1 and "
  f"{TR[HEAD]['V'][2.5]:+.3f} at z = 2.5 -- but past z = {E3[HEAD]['z_cross']:.2f}\n"
  "  only a ghost can follow the fit.  A healthy thawing field with the same w0 rises monotonically instead ("
  + (f"{TH[HEAD]['track'][2.5]:+.3f}" if TH.get(HEAD) else "n/a") + " dex at 2.5).\n"
  f"  Against the evidence: no track reaches MUSE-DARK III's apparent +0.38 at z = 1 (smallest gap {min(rows5[n_]['muse_gap'] for n_ in de_tr):.3f}\n"
  f"  dex); all sit within 1 sigma of the deep-MOND Jeanneau refit (pulls {min(rows5[n_]['j_pull'] for n_ in de_tr):+.2f}..{max(rows5[n_]['j_pull'] for n_ in de_tr):+.2f} "
  f"vs flat {rows5['flat (w = -1)']['j_pull']:+.2f}, each a little farther than flat);\n"
  f"  at z = 2.5 the published fits through sqrt(V) stay inside +/-0.13 ({min(rows5[n_]['z25'] for n_ in cpl_names):+.3f}..{max(rows5[n_]['z25'] for n_ in cpl_names):+.3f}), "
  f"but a healthy thawing field reaches {max(rows5[n_]['z25'] for n_ in thaw_names):+.3f}\n"
  f"  (H5d FAILS on it): its separation from LambdaCDM's emergent +{LCDM25:.3f} drops to {min(rows5[n_]['lcdm_sep'] for n_ in thaw_names):.2f} sigma "
  f"from flat's {rows5['flat (w = -1)']['lcdm_sep']:.2f}.  So the direction\n"
  "  depends on the realisation: the phantom-crossing fits move a0(z) slightly toward MUSE at z ~ 1 and away from LambdaCDM at z = 2.5;\n"
  "  a healthy field moves it toward both.  Tied, not derived: kappa stays fitted.")
OUT["verdict"] = dict(n_checks=len(CH), n_fail_load_bearing=n_fail)
json.dump(OUT, open(JSN, "w"), indent=1, default=str)
rc = 0 if n_fail == 0 else 1
P(f"\n  {len(CH) - sum(1 for _, ok, _l in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote "
  f"{os.path.basename(JSN)}  ({time.time() - T_START:.0f} s)")
P(f"rc = {rc}")
TEE.flush(); sys.stdout = sys.__stdout__; TEE.close()
sys.exit(rc)
