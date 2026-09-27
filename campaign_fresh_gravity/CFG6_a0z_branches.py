#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG6 (part 1) -- SHOULD a0 FOLLOW THE DARK ENERGY THROUGH COSMIC TIME?  The branches: what each tie reads, which have a
healthy action, which need a ghost, their constants, and their a0(z) for z = 0-5 under the DESI DR2 fits, both footings.

FOUNDING PRINCIPLE (this lane, plain words).  a0 is set by the vacuum's energy: a0 = kappa c sqrt(G rho_vac), kappa = 1/2
FITTED, never derived (equivalently Z = 5.7888).  If the dark energy is a true constant, a0 is exactly flat in redshift --
the framework's distinctive prediction against the rival a0 ~ H(z).  If the dark energy evolves, the principle does not say
by itself WHICH scalar of the dark-energy sector a0 reads.  This lane writes each reading down, asks whether it can be put
into an action with no new constant and no harm, and computes its a0(z) under the published fits.

THE BRANCHES (each: a0(z)/a0(0), field content, constants)
  A  unimodular tie (XR20 T1, XR30): a0 reads the Henneaux-Teitelboim integration constant Lambda_0.  a0(z)/a0(0) = 1
     exactly, whatever else the dark energy does.  Fields: the HT 3-form multiplier (1 global DOF, no local mode).
  B  density tie (FP0 R3b; L273 Parts 1-3): a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)).
  C  potential tie (XR20 T5): a0 ~ sqrt(V(phi)), V = (rho - p)/2 for any scalar.
  D  pressure tie (stage-17's promotion a0^2 ~ -K(Q); L273 Part 4; PAPER7 v2's note): a0 ~ sqrt(-p).  With stage-17's
     w = -1 vacuum and its excitation it is flat to < 1% for z <= 5 (PAPER7's 'own law'); with DESI's w(z) read through
     it, L273 Part 4.
  Each of B, C, D is evaluated two ways: FOLLOWING the published CPL fits (which cross w = -1 at z = 0.35-0.44; a minimally
  coupled single field cannot follow them past the crossing) and with a HEALTHY canonical thawing field (exponential
  potential), projected onto the fits two ways -- matched to each posterior sample's w0 (XR20's convention) and
  conditioned on the fits' posterior through its CPL-equivalent (w0, wa) (a Gaussian likelihood proxy).

INPUTS.  DESI DR2 BAO + CMB + SNe w0waCDM (DESI Collaboration 2025, arXiv:2503.14738): DESY5 (-0.752, -0.86), Pantheon+
(-0.838, -0.62), Union3 (-0.667, -1.09); the SNe samples are Pantheon+ (Scolnic et al. 2022; Brout et al. 2022), Union3
(Rubin et al. 2023, arXiv:2311.12098) and DES-SN5YR (DES Collaboration 2024, arXiv:2401.02929).  Uncertainties are
propagated through the DESI DR2 public chains (data.desi.lbl.gov, cobaya base_w_wa), in the thinned copies L275 committed
(fable_independent_2026/data/desi_dr2_w0wa_thinned/).  Footings: FP0's a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt)
m/s^2; on rho_Lambda the alt value is kappa = 0.6043.  The chain's MOND term is FP7's -(1/16 pi G) 2 alpha^2 J(Y/alpha^2),
with J_P2 (FP7) and nu_mono (L340/XC4; the kernel the record adopted on 09-26), both in two-field form.

PRE-DECLARED (copied from the lane's hypothesis file, written 2026-09-27T16:03Z before any code of this lane ran; from
hand algebra, no probe outputs):
  H1 controls: FP0 R3b 0.7956404957595 (1e-12); XR20's sqrt(V) track (+0.051 at z = 1, -0.034 at z = 2.5, DESY5; the full
     E2 table vs XR20's JSON); L275's chain bands at z = 2.5 exactly; L273's Gaussian rho = -0.9 pressure bands quoted by
     PAPER7 v2 (+0.007/+0.030/+0.058; [-0.015,+0.028], [+0.007,+0.054], [+0.019,+0.097]) by replaying L273's RNG; XR20's
     thawing tracks (+0.111/+0.070/+0.156 at z = 2.5, 1e-6); stage-17's flat law < 1% for z <= 5 over its nu0 window
     [2.1e-5, 1.8e-4], z_t in [18, 36]; PAPER7's LCDM-emergent factors 1.23/1.76/2.13/2.82 at z = 1/2/2.5/3.25, +0.33 dex.
     EXPECT TRUE.
  H2 reading family: alpha^2 = kappa^2 G Phi, Phi = u rho + v(-p) = (u+v) V + (u-v) X for a canonical field.  B (1,0),
     C (1/2,1/2), D (0,1).  Only C is a function of the field alone; B and D need X (local, derivative couplings).
     EXPECT TRUE.
  H3 health of derivative ties with the chain's MOND term -(1/8 pi G) A J(Y/A): P_X,eff = 1 + b eps F,
     P_XX,eff = -b^2 eps s^2 J''/Phi, eps = kappa^2/8 pi, b = u - v.  D (b = -1): ghost where eps F > 1, y >~ 200 (can) /
     140 (alt) with J_P2 (~560 AU around a solar mass).  B (b = +1): P_X > 0, but c_s^2 < 0 for modes transverse to the
     MOND field where eps(1+w) s^2 J'' > 1 + eps F: J_P2 at y >~ 20-30 for 1+w = 0.25; nu_mono only if 1+w >~ 0.05.
     C (b = 0): healthy.  EXPECT D fails around every star; B fails for DESI-like 1+w0 (0.16-0.33) in the Newtonian regime
     on both kernels; C passes.  Uncertain: the nu_mono threshold on 1+w (hand estimate 0.05); longitudinal mixing on the
     lambda = 0 root expected to stabilise k || grad(phi): K_eff = 1 + eps[bF - b^2 (1+w) s^2 J'' J'/(J' + 2 s J'')] > 0.
  H4 global realisation: a leaf-averaged tie alpha^2 = kappa^2 G <Phi>_h on the CMC leaves reads Phi exactly on FRW; its
     coupling to a localised perturbation is O(1/V_leaf).  B and D realisable this way with healthy local dynamics; A is
     Phi = Lambda.  EXPECT TRUE.
  H5 constants: every branch = kappa (fitted) + the DE history (measured).  A with an evolving DE component needs one extra
     choice (the HT share of today's DE).  EXPECT TRUE.
  H6 predictions at z = 2.5, DESY5 chains, median [68%]: B-CPL -0.099 [-0.140, -0.060]; C-CPL -0.034 (+/-0.03); D-CPL
     +0.030 [+0.007, +0.053]; thawing w0-matched C +0.07..+0.16, B ~+0.05..+0.12, D ~+0.09..+0.20.  A healthy field fitted
     to the data rises less: 30-60% of the w0-matched rise (C-thaw <= +0.08 at z = 2.5).
  H7 z = 0 normalisation with kappa = 1/2 held: the DESI w0wa cosmologies move a0(0) by -0.014..+0.002 dex.  EXPECT TRUE.
  MUTATE: branch A reads rho_total (a0 ~ H(z)): the flat-law control must FAIL, rc = 1.
"""
# (the docstring above is the pre-declaration; everything below was written after it and before the first run)
DOC_CHECKS = r"""
CHECKS
  C1-C8 CONTROLS (numbers the record committed, reproduced by this lane's own code): C1 FP0 R3b; C2 XR20's sqrt(V) E2 table;
     C3 L275's chain bands (density, pressure, H(z); all z, all three combinations); C4 L273's Gaussian pressure bands and
     PAPER7 v2's quoted strings (RNG replayed); C5 XR20's thawing tracks; C6 stage-17's derived pressure law (the window,
     z_t, < 1% for z <= 5, and PAPER7's sentence); C7 PAPER7's LCDM-emergent factors (the parent's convention) and L274's
     +0.334; C8 FP0's footings and the canonical->alt lever.
  B1 (sympy) the reading family Phi = u rho + v(-p) for L = X - V and for a general P(X, phi); which readings need X.
  B2 (sympy) the tie's derivatives of the MOND term (random-point identities with J_P2) and the local dispersion relation
     of (d phi_DE, d phi_MOND) plane waves on a static MOND background with the DE field rolling: K_eff(theta), the
     transverse k-essence criterion, lambda-independence of the transverse mode.
  B3 the health map on J_P2 and nu_mono, both footings: D's ghost radius, B's instability onset for DESI-like w, the nu_mono
     threshold on 1 + w, C's health (mass^2 > 0 for an exponential V).
  B4 the leaf-averaged (global) tie on an N-site lattice (sympy + numeric): uniform P_X,eff = 1 + b <eps F>, cross terms
     O(1/N); <eps F> for today's universe (reported estimate).
  B5 the phantom crossing in the chains (posterior mass crossing w = -1 in 0 < z < 2.5).
  B6 the branch ledger: formula, field content, constants, action, ghost/crossing need.
  P1 CPL-following B, C, D from the chains; P2 thawing w0-matched from the chains; P3 thawing conditioned on the posterior;
  P4 the rival H(z) and LCDM-emergent references; P5 both footings in absolute units and the z = 0 normalisation.
  HEADLINE-FLAT branch A is exactly flat (1e-12) at every z of the table on both footings.
  W  the ledger.
The main run also writes CFG6_a0z_branches_thawgrid.json (the thawing tracks, 1e-7 dex, z <= 3.5), which part 2 reads; the
MUTATE run does not write it (the grid does not depend on the MUTATE switch).
MUTATE=1: branch A's tie reads the TOTAL density (a0 ~ H(z)) instead of the HT constant: HEADLINE-FLAT must FAIL (rc = 1).

SCOPE.  The CPL form beyond z ~ 2.5 is an extrapolation of fits constrained at z <~ 2.3 (flagged in the tables).  The thawing
field is one potential shape (exponential), frozen at z = 30, dust + field (radiation ignored below z = 30).  The
posterior-conditioned projection uses a 3-d Gaussian of the chains in (w0, wa, Omega_m) as a likelihood proxy and each
thawing track's least-squares CPL equivalent over z <= 2.5; it is a projection, not a fit to the BAO/SNe/CMB likelihoods.
The local stability analysis is flat-space, frozen coefficients, gravity decoupled (the high-k/UV question); the MOND
scalar's inertia lambda is kept general (FP7) and at 0 (FP14's root).
"""
import os, sys, re, json, math, time, warnings
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True                   # write nothing outside CFG6_* (no __pycache__)
import CFG6_common as C                          # sets the thread limits before numpy loads
import numpy as np
import sympy as sp
import mpmath as mp
from sympy.calculus.euler import euler_equations

warnings.filterwarnings("ignore")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "CFG6_a0z_branches"
TXT = os.path.join(HERE, NAME + ("_MUTATE.out" if MUTATE else ".out"))
JSN = os.path.join(HERE, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))
T_START = time.time()
TEE = C.Tee(TXT)
sys.stdout = TEE
OUT = {"lane": "CFG6", "part": "branches, health, predictions", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
R = C.Recorder(OUT)
P, banner, check = R.P, R.banner, R.check
dex = np.log10

P(__doc__.strip())
P(DOC_CHECKS.strip())
if MUTATE:
    P("\n  *** MUTATE=1: branch A's tie reads the TOTAL density (a0 ~ H(z)); HEADLINE-FLAT must FAIL ***")
P(f"\n  inputs: FP0 a0 = {C.A0['canonical']:.4e} / {C.A0['alt']:.4e} m/s^2; kappa on rho_Lambda {C.KAPPA['canonical']:.4f} / "
  f"{C.KAPPA['alt']:.4f}; eps = kappa^2/8pi = {C.EPS['canonical']:.5f} / {C.EPS['alt']:.5f}; DESI DR2 CPL: " +
  "; ".join(f"{k} {v}" for k, v in C.DESI.items()))

ZT20 = [0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]                         # XR20's E2 grid
ZP = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
ZG = np.round(np.linspace(0.0, 5.0, 101), 10)                        # the thawing grid's redshifts (dz = 0.05)

# ================================================================================================ C controls
banner("C   CONTROLS: the record's committed a0(z) numbers, reproduced by this lane's own code")
fp0 = json.load(open(C.rpath("real_research", "derivation_chain_2026", "FP0_core_postulates_results.json")))
r25 = float(C.R_density(2.5, *C.DESI["DESY5"]))
check("C1 CONTROL FP0 R3b: the density tie's a0(2.5)/a0(0) on DESY5 equals FP0's committed number (1e-12)",
      f"{r25:.13f} vs FP0 {fp0['numbers']['a0z_desy5_z25']:.13f}", abs(r25 - fp0["numbers"]["a0z_desy5_z25"]) < 1e-12)

xr20 = json.load(open(C.rpath("real_research", "cross_thread_review_2026_09_26", "XR20_evolving_de_a0z_results.json")))
dmax = 0.0
for k, (w0, wa) in C.DESI.items():
    for z in ZT20:
        for lab, fn in (("V", C.R_potential), ("density", C.R_density), ("pressure", C.R_pressure)):
            dmax = max(dmax, abs(float(dex(fn(z, w0, wa))) - xr20["numbers"]["E2"][k][lab][str(z)]))
v1, v25 = float(dex(C.R_potential(1.0, *C.DESI["DESY5"]))), float(dex(C.R_potential(2.5, *C.DESI["DESY5"])))
check("C2 CONTROL XR20 T5: the potential tie sqrt(V) (and the density and pressure rows) reproduce XR20's committed E2 table, "
      "all three fits, z = 0.25-3 (1e-12); the headline +0.051 at z = 1 and -0.034 at z = 2.5 (DESY5)",
      f"max |diff| {dmax:.1e}; DESY5 sqrt(V): {v1:+.3f} at z = 1, {v25:+.3f} at z = 2.5", dmax < 1e-12 and f"{v1:+.3f}" == "+0.051"
      and f"{v25:+.3f}" == "-0.034")

l275 = json.load(open(C.rpath("fable_independent_2026", "L275_results.json")))
CH_DATA = {k: C.load_chain(k) for k in C.DESI_ORDER}
SN_OF = {"DESY5": "desy5sn", "Pantheon+": "pantheonplus", "Union3": "union3"}
dmax3, n3 = 0.0, 0
for k in C.DESI_ORDER:
    wt, w0s, was, oms = CH_DATA[k]
    for z in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0):
        for key, fn in (("pressure", lambda z: dex(C.R_pressure(z, w0s, was))), ("density", lambda z: dex(C.R_density(z, w0s, was))),
                        ("hz", lambda z: dex(C.R_total(z, w0s, was, oms)))):
            mine = C.wpct(fn(z), wt, [16, 50, 84])
            ref = l275["bands"][key][SN_OF[k]]["table"][str(float(z))]
            dmax3 = max(dmax3, float(np.max(np.abs(np.array(mine) - np.array(ref)))))
            n3 += 1
check("C3 CONTROL L275: the DESI DR2 chain bands (16/50/84) of the density, pressure and H(z) readings, z = 0.5-5, all three "
      "combinations, reproduced from the committed thinned chains",
      f"{n3} bands, max |diff| {dmax3:.1e}", dmax3 < 1e-12)

l273 = json.load(open(C.rpath("fable_independent_2026", "L273_results.json")))
p7 = C.rd("qwen_claude_field_theory/papers_2026/PAPER7_a0z_decisive_measurement_2026.tex") or ""
D273 = {"DESY5": dict(w0=-0.752, sw0=0.057, wa=-0.86, swa=0.215), "Pantheon+": dict(w0=-0.838, sw0=0.055, wa=-0.62, swa=0.205),
        "Union3": dict(w0=-0.667, sw0=0.088, wa=-1.09, swa=0.29)}
rng = np.random.default_rng(273)
with np.errstate(all="ignore"):
    for name, d in D273.items():                                     # L273 Part 2's draws, in its order (consumed, not used)
        for rho in (0.0, -0.8, -0.9, -0.95):
            cov = np.array([[d["sw0"] ** 2, rho * d["sw0"] * d["swa"]], [rho * d["sw0"] * d["swa"], d["swa"] ** 2]])
            rng.multivariate_normal([d["w0"], d["wa"]], cov, size=200000, method="cholesky")
    bands_p = {}
    for name, d in D273.items():                                     # L273 Part 4's draws
        cov = np.array([[d["sw0"] ** 2, -0.9 * d["sw0"] * d["swa"]], [-0.9 * d["sw0"] * d["swa"], d["swa"] ** 2]])
        smp = rng.multivariate_normal([d["w0"], d["wa"]], cov, size=200000, method="cholesky")
        bands_p[name] = np.percentile(dex(C.R_pressure(2.5, smp[:, 0], smp[:, 1])), [16, 50, 84])
d4 = max(float(np.max(np.abs(bands_p[k] - np.array(l273["pressure_band_z2p5_rho-0.9"][k])))) for k in D273)
cen = f"${bands_p['Pantheon+'][1]:+.3f}$, ${bands_p['DESY5'][1]:+.3f}$ and ${bands_p['Union3'][1]:+.3f}$"
bnd = ", ".join(f"$[{bands_p[k][0]:+.3f},{bands_p[k][2]:+.3f}]$" for k in ("Pantheon+", "DESY5", "Union3"))
check("C4 CONTROL L273 Part 4 / PAPER7 v2's note: the face-value DESI pressure mapping at z = 2.5 (Gaussian, rho = -0.9, L273's "
      "RNG sequence replayed) reproduces L273's committed bands and the strings PAPER7 v2 prints",
      f"max |diff| vs L273 JSON {d4:.1e}; PAPER7 central '{cen}' found: {cen in p7}; bands '{bnd}' found: {bnd in p7}",
      d4 < 1e-12 and cen in p7 and bnd in p7)

TH20 = {}
dmax5 = 0.0
for k in C.DESI_ORDER:
    e4 = xr20["numbers"]["E4"][k]
    tr = C.thaw_tracks(e4["lam"], C.OM_M, np.array(ZT20))
    TH20[k] = tr
    dmax5 = max(dmax5, float(np.max(np.abs(tr["V"] - np.array([e4["track"][str(z)] for z in ZT20])))))
    dmax5 = max(dmax5, abs(tr["w0"] - e4["w0"]))
check("C5 CONTROL XR20 E4: this lane's thawing solver, at XR20's lambda for each fit, reproduces XR20's committed sqrt(V) tracks "
      "(z = 0.25-3) and w0 (1e-6)",
      f"max |diff| {dmax5:.1e}; z = 2.5: " + ", ".join(f"{k} {TH20[k]['V'][ZT20.index(2.5)]:+.3f}" for k in C.DESI_ORDER),
      dmax5 < 1e-6)

st17 = C.rd("nbody_2026/stage17_a0z_from_the_action_2026.py") or ""
mp.mp.dps = 30
Z_REC, OFF = mp.mpf(1090), mp.mpf("0.006")
MPC_mp = mp.mpf("3.0856775814913673e22")
nu0_floor = 1 / ((1 + Z_REC) ** 3 * OFF ** 2)
T_FF_TH = (mp.mpf("15") * MPC_mp / 1000 / mp.mpf("2.0e5")) / mp.mpf("4.35e17")
nu0_ceil = mp.mpf("0.141") / (mp.mpf("1.5e5") * T_FF_TH)
a0_st17 = lambda z, nu0: ((1 + nu0 ** 2) / (1 + (nu0 * (1 + mp.mpf(z)) ** 3) ** 2)) ** mp.mpf("0.25")     # beta = 1 closed form
dev17 = max(abs(a0_st17(z, nu) - 1) for nu in (nu0_floor, nu0_ceil) for z in np.linspace(0, 5, 51))
zt = (float(nu0_ceil ** (-mp.mpf(1) / 3) - 1), float(nu0_floor ** (-mp.mpf(1) / 3) - 1))
rec = (float(a0_st17(1090, nu0_ceil)), float(a0_st17(1090, nu0_floor)))
mp.mp.dps = 40
# stage 17 commits no .out: its committed code is run read-only (it only prints) and its printed numbers are the reference
import subprocess
s17 = subprocess.run([sys.executable, C.rpath("nbody_2026", "stage17_a0z_from_the_action_2026.py")], capture_output=True, text=True,
                     cwd=C.REPO, timeout=300).stdout
m_w = re.search(r"nu_0 in \[([0-9.e-]+), ([0-9.e-]+)\] -- a factor", s17)
m_z = re.search(r"z_t = nu_0\^\(-1/3\) - 1 lies in \[([0-9.]+), ([0-9.]+)\]", s17)
m_r = re.search(r"off at recombination \(([0-9.]+)-([0-9.]+)\)", s17)
s17_ok = bool(m_w and m_z and m_r and "CHECKS: 17/17 passed" in s17)
mine = (f"{float(nu0_floor):.3g}", f"{float(nu0_ceil):.3g}", f"{zt[0]:.3g}", f"{zt[1]:.3g}", f"{rec[0]:.2g}", f"{rec[1]:.2g}")
theirs = (m_w.group(1), m_w.group(2), m_z.group(1), m_z.group(2), m_r.group(1), m_r.group(2)) if s17_ok else None
same = s17_ok and all(abs(float(a) - float(b)) <= 0.006 * abs(float(b)) for a, b in zip(mine, theirs))
ok6 = (float(dev17) < 0.01 and same and "a_0^2(Q) = kappa^2 c^2 G (-K(Q)) / c^2" in st17 and "within 1\\% of flat for $z\\le5$" in p7)
check("C6 CONTROL stage-17 / PAPER7: the derived pressure law a0^2/a0^2(0) = [1 - (1 - (1+nu^2)^-1/2)]/[...](nu0), nu = nu0 (1+z)^3, "
      "is flat to < 1% for z <= 5 across its window; this lane's window, transition redshift and recombination off-switch equal "
      "the numbers stage-17's committed code prints (run read-only); PAPER7's 'within 1% of flat for z <= 5' located",
      f"max |a0(z)/a0(0) - 1| over z <= 5 and the window = {float(dev17):.2e}; this lane: window [{mine[0]}, {mine[1]}], z_t [{mine[2]}, "
      f"{mine[3]}], a0(1090)/a0(0) {mine[4]}-{mine[5]}; stage 17 prints {theirs}", ok6,
      "branch D's own law (a w = -1 vacuum plus the excitation's pressure) is flat: it is branch A at the rotator's precision.  "
      "Reading note: stage-17's docstring gives 'z_t in [18, 36]', which is 1 + z_t; its code prints z_t in [16.8, 35.0] "
      "(this lane's pre-declared H1 copied the docstring's numbers)")
OUT["numbers"]["C6"] = dict(max_dev=float(dev17), window=[float(nu0_floor), float(nu0_ceil)], z_t=list(zt), a0_1090=list(rec),
                            stage17_printed=theirs)


def lcdm_paper7(z):                                                  # the parent's convention (OM 0.315, M = 1e12 Msun, h = 0.674)
    OMp, h_ = 0.3150, 0.674
    E = lambda z: np.sqrt(OMp * (1 + z) ** 3 + 1 - OMp)
    cM = lambda z: 10 ** ((0.520 + (0.905 - 0.520) * np.exp(-0.617 * z ** 1.21)) + (-0.101 + 0.026 * z) * np.log10(1e12 * h_ / 1e12))
    fc = lambda x: np.log(1 + x) - x / (1 + x)
    return E(z) ** (4 / 3) * (cM(z) ** 2 / fc(cM(z))) / (cM(0.0) ** 2 / fc(cM(0.0)))


fac = [float(lcdm_paper7(z)) for z in (1.0, 2.0, 2.5, 3.25)]
fstr = "factors $" + "$, $".join(f"{f:.2f}" for f in fac[:3]) + f"$ and ${fac[3]:.2f}$"
l274 = C.rd("fable_independent_2026/L274_a0z_theories_chart.out") or ""
m274 = re.search(r"\(z = 2\.5: ([+-][0-9.]+) dex \(factor", l274)
LCDM25 = float(m274.group(1)) if m274 else float("nan")
lc25 = float(dex(C.lcdm_emergent(2.5)))
check("C7 CONTROL PAPER7's LambdaCDM-native emergent scale: the parent's convention gives the factors PAPER7 prints at z = 1, 2, "
      "2.5, 3.25; L274's convention gives its committed +0.334 dex at z = 2.5",
      f"'{fstr}' found in PAPER7: {fstr in p7}; L274 +{lc25:.4f} vs committed {LCDM25:+.3f}",
      fstr in p7 and abs(lc25 - LCDM25) < 5e-4)
check("C8 CONTROL FP0's footings: canonical 9.3603e-11, alt 1.1312e-10 m/s^2 (kappa 0.5000 / 0.6043 on rho_Lambda); the "
      "canonical->alt lever is +0.0823 dex in a0 (the committed yardstick for 'how much does a gate move per dex of a0')",
      f"{C.A0['canonical']:.4e} / {C.A0['alt']:.4e}; kappa {C.KAPPA['canonical']:.4f} / {C.KAPPA['alt']:.4f}; lever {C.LEVER_FOOT:+.4f} dex",
      f"{C.A0['canonical']:.4e}" == "9.3603e-11" and f"{C.A0['alt']:.4e}" == "1.1312e-10" and abs(C.KAPPA["canonical"] - 0.5) < 1e-3)

# ================================================================================================ B1 the reading family
banner("B1  WHAT EACH TIE READS: alpha^2 = kappa^2 G Phi, Phi = u rho + v (-p)")
Xs, Vs, u_, v_ = sp.symbols("X V u v", real=True)
rho_c, p_c = Xs + Vs, Xs - Vs                                        # canonical: L = X - V, rho = 2X P_X - P, p = P
Phi = sp.expand(u_ * rho_c + v_ * (-p_c))
fam = {"B density (1, 0)": (1, 0), "C potential (1/2, 1/2)": (sp.Rational(1, 2), sp.Rational(1, 2)), "D pressure (0, 1)": (0, 1)}
rows = {k: sp.expand(Phi.subs({u_: a, v_: b})) for k, (a, b) in fam.items()}
b_of = {k: sp.diff(e, Xs) for k, e in rows.items()}
Pf = sp.Function("P")
Xg, ph = sp.symbols("X phi", positive=True)
rho_g = 2 * Xg * sp.diff(Pf(Xg, ph), Xg) - Pf(Xg, ph)
V_g = sp.simplify((rho_g - Pf(Xg, ph)) / 2)
e1 = (sp.simplify(Phi - ((u_ + v_) * Vs + (u_ - v_) * Xs)) == 0 and b_of["C potential (1/2, 1/2)"] == 0
      and b_of["B density (1, 0)"] == 1 and b_of["D pressure (0, 1)"] == -1)
for k, e in rows.items():
    P(f"    {k:24s}: Phi = {e}   (d Phi/dX = b = {b_of[k]})")
P(f"    general P(X, phi): rho = {rho_g}; (rho - p)/2 = {V_g}  -> depends on X unless P is linear in X")
check("B1 THE READING FAMILY: for a canonical field Phi = u rho + v(-p) = (u+v) V + (u-v) X, so only the potential tie C "
      "(u = v) is a function of the field alone; the density tie B (b = +1) and the pressure tie D (b = -1) read the kinetic "
      "scalar X = -(d phi)^2/2 too: they are local, but derivative, couplings.  (XR20 E1's 'no local coupling realises "
      "sqrt(rho_DE)' holds for alpha(phi); alpha(phi, X) does realise it on FRW, exactly.)",
      f"identity {e1}; b = +1 / 0 / -1 for B / C / D", e1)

# ================================================================================================ B2 local dispersion (sympy)
banner("B2  THE DERIVATIVE TIES ON A STATIC MOND BACKGROUND: the local dispersion relation (sympy)")
kap, Gs, gg, bb, Vv, Ys = sp.symbols("kappa G g b V Y", positive=True)
Xv = sp.Symbol("X", positive=True)
Jf = sp.Function("J")
A_expr = kap ** 2 * Gs * (bb * Xv + Vv)
LM = -gg * A_expr * Jf(Ys / A_expr)                                   # FP7: -(1/16 pi G) 2 alpha^2 J(Y/alpha^2), g = 1/8 pi G
Ltot = Xv - Vv + LM
LX_, LXX_, LXY_ = sp.diff(Ltot, Xv), sp.diff(Ltot, Xv, 2), sp.diff(Ltot, Xv, Ys)
LY_, LYY_ = sp.diff(Ltot, Ys), sp.diff(Ltot, Ys, 2)
# the claimed closed forms, eps = kappa^2/8 pi with g = 1/(8 pi G); s = Y/A; Phi = b X + V
s_sym = sp.Symbol("s", positive=True)
Jp2 = lambda s: -sp.log(1 - 2 * sp.sqrt(s)) / 4 - sp.sqrt(s) / 2 - s / 2
J1 = sp.diff(Jp2(s_sym), s_sym)
J2 = sp.diff(Jp2(s_sym), s_sym, 2)
Fs = s_sym * J1 - Jp2(s_sym)
rng_b = np.random.default_rng(627)
maxrel = 0.0
for trial in range(6):
    vals = {kap: sp.Rational(int(rng_b.integers(3, 9)), 10), Gs: sp.Rational(int(rng_b.integers(1, 9)), 7), bb: [1, -1, 1, -1, 1, 1][trial],
            Vv: sp.Rational(int(rng_b.integers(5, 15)), 4), Xv: sp.Rational(int(rng_b.integers(1, 9)), 11)}
    vals[gg] = 1 / (8 * sp.pi * vals[Gs])
    Aval = (vals[kap] ** 2 * vals[Gs] * (vals[bb] * vals[Xv] + vals[Vv]))
    sval = sp.Rational(int(rng_b.integers(1, 20)), 100)               # s < 1/4 (J_P2's domain)
    vals[Ys] = sval * Aval
    subsJ = lambda e: e.replace(Jf, lambda arg: Jp2(arg)).doit()
    Phi_v = vals[bb] * vals[Xv] + vals[Vv]
    epsv = vals[kap] ** 2 / (8 * sp.pi)
    claims = {"L_X": 1 + epsv * vals[bb] * Fs.subs(s_sym, sval),
              "L_XX": -epsv * vals[bb] ** 2 * (s_sym ** 2 * J2).subs(s_sym, sval) / Phi_v,
              "L_XY": epsv * vals[bb] * (s_sym * J2).subs(s_sym, sval) / Aval,
              "L_Y": -vals[gg] * J1.subs(s_sym, sval), "L_YY": -vals[gg] * J2.subs(s_sym, sval) / Aval}
    got = {"L_X": LX_, "L_XX": LXX_, "L_XY": LXY_, "L_Y": LY_, "L_YY": LYY_}
    for key in claims:
        a_ = sp.N(subsJ(got[key]).subs(vals), 40)
        b_ = sp.N(claims[key], 40)
        maxrel = max(maxrel, float(abs(a_ - b_) / (abs(b_) + 1e-30)))
check("B2a the tie's second derivatives of the MOND term (J_P2, random rational points, both signs of b): L_X = 1 + b eps F, "
      "L_XX = -b^2 eps s^2 J''/Phi, L_XY = b eps s J''/A, L_Y = -g J', L_YY = -g J''/A, with eps = kappa^2/8 pi, F = s J' - J, "
      "s = Y/A, A = kappa^2 G Phi",
      f"max relative residual {maxrel:.1e} over 6 points x 5 derivatives", maxrel < 1e-30)
# the local dispersion relation
t_, x_, z_ = sp.symbols("t x z", real=True)
vt = sp.Function("vt")(t_, x_, z_)
vp = sp.Function("vp")(t_, x_, z_)
LX, LXX, LXY, LY, LYY, vv, Y0, lam = sp.symbols("L_X L_XX L_XY L_Y L_YY v Y_0 lambda", real=True)
dX1, dX2 = vv * vt.diff(t_), (vt.diff(t_) ** 2 - vt.diff(x_) ** 2 - vt.diff(z_) ** 2) / 2        # X = (v + d_t vt)^2/2 - |grad vt|^2/2
dY1, dY2 = 2 * sp.sqrt(Y0) * vp.diff(x_), vp.diff(x_) ** 2 + vp.diff(z_) ** 2                     # Y = |grad phi|^2, background along x
L2 = LX * dX2 + LY * dY2 + LXX * dX1 ** 2 / 2 + LXY * dX1 * dY1 + LYY * dY1 ** 2 / 2 + gg * lam * vp.diff(t_) ** 2
eqs = euler_equations(L2, [vt, vp], [t_, x_, z_])
Aa, Bb, om, kx, kz = sp.symbols("A_amp B_amp omega k_x k_z")
Ew = sp.exp(sp.I * (kx * x_ + kz * z_ - om * t_))
Mrows = []
for eq in eqs:
    e = sp.expand(sp.simplify((eq.lhs - eq.rhs).subs({vt: Aa * Ew, vp: Bb * Ew}).doit() / Ew))
    Mrows.append([e.coeff(Aa), e.coeff(Bb)])
Mdisp = sp.Matrix(Mrows)
det0 = sp.factor(sp.expand(Mdisp.det().subs(lam, 0)))
Kt = LX + LXX * vv ** 2
Sx, Sz = -2 * LY - 4 * Y0 * LYY, -2 * LY
Keff_theta = Kt + (2 * vv * sp.sqrt(Y0) * LXY) ** 2 * kx ** 2 / (Sx * kx ** 2 + Sz * kz ** 2)
om2_claim = LX * (kx ** 2 + kz ** 2) / Keff_theta
det_at = sp.simplify(det0.subs(om, sp.sqrt(om2_claim)))
trans_ok = sp.simplify(Mdisp[0, 1].subs(kx, 0)) == 0 and sp.simplify(Mdisp[1, 0].subs(kx, 0)) == 0
om_t = sp.simplify(sp.solve(Mdisp[0, 0].subs(kx, 0), om)[0] ** 2)
b2_ok = sp.simplify(det_at) == 0 and trans_ok and sp.simplify(om_t - LX * kz ** 2 / Kt) == 0
# the tie's K_eff(theta) in closed form
epsS, bS, FS, J1S, J2S, sS, rvS, PhiS, cth = sp.symbols("epsilon b F Jp Jpp s r_v Phi c_theta", positive=True)
A_S = epsS * PhiS / gg                                               # g A = eps Phi
subs_tie = {LX: 1 + epsS * bS * FS, LXX: -epsS * bS ** 2 * sS ** 2 * J2S / PhiS, LXY: epsS * bS * sS * J2S / A_S,
            LY: -gg * J1S, LYY: -gg * J2S / A_S, Y0: sS * A_S, vv: sp.sqrt(rvS * PhiS)}
Keff_tie = sp.simplify(Keff_theta.subs(subs_tie).subs({kx: cth, kz: sp.sqrt(1 - cth ** 2)}))
Keff_claim = 1 + epsS * (bS * FS - bS ** 2 * rvS * sS ** 2 * J2S * J1S / (J1S + 2 * sS * J2S * cth ** 2))
b2b = sp.simplify(Keff_tie - Keff_claim) == 0
P(f"    det M at lambda = 0 (factored): {det0}")
P(f"    lambda = 0: omega^2 = L_X k^2 / K_eff(theta), K_eff = L_X + L_XX v^2 + (2 v sqrt(Y0) L_XY)^2 kx^2/(S_x kx^2 + S_z kz^2): "
  f"residual 0 = {sp.simplify(det_at) == 0}")
P(f"    transverse (k_x = 0), any lambda: the DE mode decouples, omega^2 = L_X k^2/(L_X + L_XX v^2): {trans_ok and sp.simplify(om_t - LX * kz ** 2 / Kt) == 0}")
P(f"    with the tie: K_eff(theta) = 1 + eps [b F - b^2 r_v s^2 J'' J'/(J' + 2 s J'' cos^2 theta)], r_v = v^2/Phi: {b2b}")
check("B2b THE LOCAL DISPERSION RELATION (sympy, Euler-Lagrange on plane waves): a rolling DE field (d_t phi = v) with the tie, on "
      "a static MOND background (grad phi_M along x), has omega^2 = L_X k^2 / K_eff(theta); for waves transverse to the MOND "
      "field the DE mode decouples at ANY MOND inertia lambda and obeys the k-essence law c_s^2 = L_X/(L_X + L_XX v^2); with "
      "the tie K_eff = 1 + eps[bF - b^2 r_v s^2 J'' J'/(J' + 2 s J'' cos^2 theta)], r_v = 2X/Phi (1 + w for B, (1+w)/(-w) for D)",
      f"lambda = 0 dispersion: {sp.simplify(det_at) == 0}; transverse decoupling: {trans_ok}; K_eff closed form: {b2b}", b2_ok and b2b,
      "the instability, where it exists, is transverse: no inertia of the MOND scalar can remove it")

# ================================================================================================ B3 the health map
banner("B3  THE HEALTH MAP: where each derivative tie breaks, on J_P2 (FP7) and nu_mono (the adopted kernel), both footings")
KERNELS = {"J_P2": C.KernelP2(), "nu_mono": C.KernelNuMono()}
# closed-form H of J_P2 against quadrature (the formula B3 uses)
hq = max(abs(C.KernelP2.H(y) - mp.quad(C.KernelP2.h, [0, y])) / C.KernelP2.H(y) for y in (mp.mpf("0.01"), 1, 50))
YG = [mp.mpf(10) ** e for e in np.linspace(-3, 13, 161)]
KQ = {kn: [C.kernel_quantities(K, y) for y in YG] for kn, K in KERNELS.items()}
Y_AU = C.G_SI * C.MSUN / C.AU ** 2                                   # g_N at 1 AU (m/s^2)
Y_SUN = C.G_SI * C.MSUN / 6.957e8 ** 2                               # at the solar surface
DE_WS = {"CPL w0, Pantheon+": 1 + C.DESI["Pantheon+"][0], "CPL w0, DESY5": 1 + C.DESI["DESY5"][0], "CPL w0, Union3": 1 + C.DESI["Union3"][0],
         "0.10": 0.10, "0.05": 0.05, "0.02": 0.02}


def first_cross(fvals, ys):
    """first y where fvals changes sign from + to - (log-linear bisection between grid points); None if never"""
    for i in range(1, len(fvals)):
        if fvals[i - 1] > 0 >= fvals[i]:
            y0_, y1_ = ys[i - 1], ys[i]
            f0, f1 = fvals[i - 1], fvals[i]
            return float(mp.e ** (mp.log(y0_) + (mp.log(y1_) - mp.log(y0_)) * f0 / (f0 - f1)))
    return None


H3 = {}
for kn in KERNELS:
    for foot in ("canonical", "alt"):
        eps = mp.mpf(C.EPS[foot])
        q = KQ[kn]
        LXD = [1 - eps * r["F"] for r in q]
        yD = first_cross(LXD, YG)
        rB = {}
        for lab, opw in DE_WS.items():
            KtB = [1 + eps * (r["F"] - opw * r["s2Jpp"]) for r in q]
            rB[lab] = first_cross(KtB, YG)
        thr = {lab: float((1 + eps * C.kernel_quantities(KERNELS[kn], y)["F"]) / (eps * C.kernel_quantities(KERNELS[kn], y)["s2Jpp"]))
               for lab, y in (("y=1e2", mp.mpf(100)), ("y=1e4", mp.mpf(10) ** 4), ("1 AU", mp.mpf(Y_AU / C.A0[foot])),
                              ("solar surface", mp.mpf(Y_SUN / C.A0[foot])))}
        cmin = min(float(r["s2Jpp"] - r["F"]) for r in q)                  # C: mass^2 ~ 1 + eps (s^2 J'' - F) for exponential V
        klong = min(float(1 + eps * (r["F"] - DE_WS["CPL w0, Union3"] * r["s2Jpp"] * r["Jp"] / r["JpL"])) for r in q)
        r_au = lambda yv: math.sqrt(C.G_SI * C.MSUN / (yv * C.A0[foot])) / C.AU if yv else None
        H3[(kn, foot)] = dict(yD=yD, rD_AU=r_au(yD), yB=rB, rB_AU={k: r_au(v) for k, v in rB.items()}, thr=thr, Cmin=cmin, Klong_min=klong)
        P(f"    {kn:8s} {foot:9s}: D ghost (1 - eps F < 0) from y = {yD:8.1f}  (within {r_au(yD):7.0f} AU of a solar mass)")
        P(f"    {'':8s} {'':9s}  B transverse c_s^2 < 0 from y = " + ", ".join(f"{v:.3g} (1+w {lab})" if v else f"never (1+w {lab})"
                                                                              for lab, v in rB.items()))
        P(f"    {'':8s} {'':9s}  B's threshold on 1 + w, (1 + eps F)/(eps s^2 J''): " + ", ".join(f"{k} {v:.4f}" for k, v in thr.items()))
        P(f"    {'':8s} {'':9s}  C: min over y of (s^2 J'' - F) = {cmin:+.3e} (>= 0: an exponential V keeps mass^2 > 0); "
          f"B longitudinal K_eff(0) min at 1+w = 0.333: {klong:+.4f}")
OUT["numbers"]["B3"] = {f"{k[0]}|{k[1]}": v for k, v in H3.items()}
dfail = all(H3[(kn, f)]["yD"] is not None and H3[(kn, f)]["yD"] < 1e3 for kn in KERNELS for f in ("canonical", "alt"))
yD_p2 = [H3[("J_P2", f)]["yD"] for f in ("canonical", "alt")]
check("B3a = H3 (D) THE LOCAL PRESSURE TIE IS A GHOST AROUND EVERY STAR: its DE field's kinetic coefficient 1 - eps F turns "
      "negative for y above ~150-200 on both kernels and footings (J_P2: 200/140 pre-declared), i.e. within a few hundred AU "
      "of every solar-mass star, and throughout the Solar System",
      "; ".join(f"{kn} {f}: y > {H3[(kn, f)]['yD']:.0f} (r < {H3[(kn, f)]['rD_AU']:.0f} AU)" for kn in KERNELS for f in ("canonical", "alt")),
      dfail and 150 < yD_p2[0] < 260 and 100 < yD_p2[1] < 180,
      "a derivative-coupled pressure tie has no healthy local action; the same structure sits in stage-17's a0^2 ~ -K(Q) "
      "promotion if it is coupled to this MOND term (its K'' term flips with 1 - eps F; the charge suppression covers only K')")
bfail = all(H3[(kn, f)]["yB"][lab] is not None and H3[(kn, f)]["yB"][lab] < 1e3 for kn in KERNELS for f in ("canonical", "alt")
            for lab in ("CPL w0, Pantheon+", "CPL w0, DESY5", "CPL w0, Union3"))
check("B3b = H3 (B) THE LOCAL DENSITY TIE IS ILL-POSED FOR DESI-LIKE w: with 1 + w = 0.16-0.33 (the CPL w0's) its transverse "
      "modes have c_s^2 < 0 (Hadamard growth ~ k) from y of a few tens, on both kernels and footings: within ~10^3 AU of every "
      "solar-mass star and in every inner galaxy",
      "; ".join(f"{kn} {f}: y > {min(H3[(kn, f)]['yB'][l] for l in ('CPL w0, Pantheon+', 'CPL w0, DESY5', 'CPL w0, Union3')):.0f}-"
                f"{max(H3[(kn, f)]['yB'][l] for l in ('CPL w0, Pantheon+', 'CPL w0, DESY5', 'CPL w0, Union3')):.0f}"
                for kn in KERNELS for f in ("canonical", "alt")), bfail,
      "alpha(phi, X) reads sqrt(rho_DE) exactly on FRW but turns the dark energy into a k-essence with P_XX < 0 wherever the MOND "
      "term is stiff; the density tie needs another realisation (B4)")
thr_nm = H3[("nu_mono", "canonical")]["thr"]
check("B3c (reported; H3's uncertain part) the nu_mono threshold on 1 + w for B's instability is ~0.05 (hand estimate): below it "
      "the local density tie is healthy even in the Solar System",
      ", ".join(f"{k} {v:.4f}" for k, v in thr_nm.items()), 0.03 <= thr_nm["1 AU"] <= 0.08, load_bearing=False)
cok = all(H3[(kn, f)]["Cmin"] >= 0 for kn in KERNELS for f in ("canonical", "alt"))
check("B3d = H3 (C) THE POTENTIAL TIE IS HEALTHY at every y from 1e-3 to 1e13: no derivative coupling (L_X = 1, L_XX = 0, no "
      "mixing at O(k^2)); its field-dependence adds only a mass term, eps V'^2/V (s^2 J'' - F) + (1 - eps F) V'', positive for an "
      "exponential V because s^2 J'' >= F everywhere",
      "min (s^2 J'' - F) = " + ", ".join(f"{kn} {f}: {H3[(kn, f)]['Cmin']:+.2e}" for kn in KERNELS for f in ("canonical", "alt")) +
      f"; J_P2's closed-form H vs quadrature {float(hq):.1e}", cok and float(hq) < 1e-25)
check("B3e (reported; H3's longitudinal expectation) on the lambda = 0 root the density tie's LONGITUDINAL mode is stable "
      "(K_eff(0) > 0) at every y even at 1 + w = 0.333: the MOND scalar's constraint adds a positive term; the failure is "
      "transverse only",
      ", ".join(f"{kn} {f}: min K_eff(0) {H3[(kn, f)]['Klong_min']:+.3f}" for kn in KERNELS for f in ("canonical", "alt")),
      all(H3[(kn, f)]["Klong_min"] > 0 for kn in KERNELS for f in ("canonical", "alt")), load_bearing=False)

# ================================================================================================ B4 the leaf-averaged tie
banner("B4  THE GLOBAL REALISATION: a leaf-averaged tie alpha^2 = kappa^2 G <Phi>_h on the khronon's CMC leaves")
Nsym = 3
Xi = sp.symbols(f"X0:{Nsym}", positive=True)
Yi = sp.symbols(f"Y0:{Nsym}", positive=True)
Vi = sp.symbols(f"V0:{Nsym}", positive=True)
Abar = kap ** 2 * Gs * sum(bb * Xi[j] + Vi[j] for j in range(Nsym)) / Nsym
Lleaf = sum(Xi[j] - Vi[j] - gg * Abar * Jf(Yi[j] / Abar) for j in range(Nsym))
dL0 = sp.diff(Lleaf, Xi[0])
Asym = sp.Symbol("A_bar", positive=True)
dLM_dA = sum(sp.diff(-gg * Asym * Jf(Yi[j] / Asym), Asym) for j in range(Nsym)).subs(Asym, Abar)
unif = sp.simplify(dL0 - (1 + kap ** 2 * Gs * bb * dLM_dA / Nsym))
cross = sp.diff(Lleaf, Xi[0], Xi[1])
d2LM_dA2 = sum(sp.diff(-gg * Asym * Jf(Yi[j] / Asym), Asym, 2) for j in range(Nsym)).subs(Asym, Abar)
cross_res = sp.simplify(cross - (kap ** 2 * Gs * bb / Nsym) ** 2 * d2LM_dA2)
unif = sp.simplify(unif) + sp.simplify(cross_res)
P(f"    N = {Nsym}: dL/dX_0 = 1 + (kappa^2 G b/N) sum_j dL_M/dA (uniform: the same at every site): residual {unif}")
P(f"    cross term d^2L/dX_0 dX_1 = (kappa^2 G b/N)^2 sum_j d^2 L_M/dA^2 -> O(1/N)")
# numeric scaling of the cross term with N (J_P2, random y_j), both signs of b
rng4 = np.random.default_rng(4)
scal = []
for Nn in (10, 100, 1000):
    ys = 10 ** rng4.uniform(-2, 2, Nn)
    ss = [float(C.KernelP2.h(y)) ** 2 for y in ys]                   # s = x^2, x = h(y) on the P2 branch
    s2J = [float(C.kernel_quantities(C.KernelP2, y)["s2Jpp"]) for y in ys]
    epsv = C.EPS["canonical"]
    cross_n = epsv * sum(s2J) / Nn / Nn                               # (eps b^2/Phi) <s^2 J''>/N in units Phi = 1
    diag_F = epsv * float(np.mean([float(C.kernel_quantities(C.KernelP2, y)["F"]) for y in ys]))
    scal.append((Nn, cross_n, diag_F))
P("    numeric (J_P2, y_j uniform in log 0.01-100): " + "; ".join(f"N = {n}: cross {c:.2e}, N x cross {n * c:.3f}, <eps F> {d:.4f}" for n, c, d in scal))
# today's <eps F>: an L* galaxy's MOND term over its region, times a generous number density
Mb, n_gal = 6e10 * C.MSUN, 0.01 / C.MPC ** 3
epsF = {}
for foot in ("canonical", "alt"):
    Kn = KERNELS["nu_mono"]
    rr = np.logspace(math.log10(0.05 * C.KPC), math.log10(1.75 * C.MPC), 400)
    Fv = np.array([float(C.kernel_quantities(Kn, C.G_SI * Mb / (r * r * C.A0[foot]))["F"]) for r in rr])
    integ = float(np.trapezoid(Fv * 4 * math.pi * rr ** 2 * rr, np.log(rr))) if hasattr(np, "trapezoid") else float(np.trapz(Fv * 4 * math.pi * rr ** 3, np.log(rr)))
    epsF[foot] = C.EPS[foot] * integ * n_gal
P(f"    today's <eps F> (one 6e10 Msun galaxy per 100 Mpc^3, nu_mono to the 1.75 Mpc cap): " + ", ".join(f"{f} {v:.1e}" for f, v in epsF.items()))
b4 = unif == 0 and abs(scal[2][0] * scal[2][1] / (scal[1][0] * scal[1][1]) - 1) < 0.5 and scal[2][1] < scal[0][1] / 50
check("B4 = H4 THE LEAF-AVERAGED TIE: with alpha^2 = kappa^2 G <Phi>_h (the same kind of term as FP14's leaf average <K>_h), the "
      "DE field's kinetic coefficient is 1 + b <eps F> at EVERY site (the MOND term's weight averaged over the leaf), and the "
      "cross terms fall as 1/N: a localised perturbation feels no derivative coupling.  On FRW it reads Phi exactly.  B and D "
      "are realisable this way with healthy local dynamics; A is the Phi = Lambda case",
      f"uniformity residual {unif}; N x cross term {scal[0][0] * scal[0][1]:.3f} / {scal[1][0] * scal[1][1]:.3f} / "
      f"{scal[2][0] * scal[2][1]:.3f} (N = 10/100/1000); today's <eps F> {epsF['canonical']:.1e} / {epsF['alt']:.1e} (reported estimate)", b4,
      "no new field and no new constant; the price is the preferred foliation the khronon already supplies, and a drift of a0 "
      "of order <eps F> as structure forms (~1e-7 or less)")
OUT["numbers"]["B4"] = dict(N_scaling=[list(s) for s in scal], epsF_today=epsF)

# ================================================================================================ B5 the phantom crossing
banner("B5  THE PHANTOM CROSSING in the DESI DR2 chains (w = w0 + wa z/(1+z) crossing -1 in 0 < z < 2.5)")
B5 = {}
for k in C.DESI_ORDER:
    wt, w0s, was, oms = CH_DATA[k]
    w25 = w0s + was * 2.5 / 3.5
    cross_ = ((w0s > -1) & (w25 < -1)) | ((w0s < -1) & (w25 > -1))
    healthy = (w0s >= -1) & (w25 >= -1)
    u_ = (-1 - w0s) / np.where(was != 0, was, np.nan)
    zc = np.where(cross_, u_ / (1 - u_), np.nan)
    B5[k] = dict(p_cross=float(np.sum(wt[cross_]) / np.sum(wt)), p_never_phantom=float(np.sum(wt[healthy]) / np.sum(wt)),
                 z_cross_med=float(C.wpct(zc[cross_], wt[cross_], [50])[0]))
    P(f"    {k:10s}: posterior mass crossing -1 in 0 < z < 2.5: {B5[k]['p_cross']:.4f}; never below -1 on [0, 2.5]: "
      f"{B5[k]['p_never_phantom']:.4f}; median z_cross {B5[k]['z_cross_med']:.3f}")
OUT["numbers"]["B5"] = B5
check("B5 THE FITS CROSS: more than 90% of every combination's posterior crosses w = -1 inside 0 < z < 2.5, so following the fits "
      "past the crossing needs a ghost (a minimally coupled single field cannot cross; Vikman 2005) or a non-minimally coupled / "
      "kinetically braided dark energy (Deffayet, Pujolas, Sawicki & Vikman 2010) -- new physics this record does not have",
      "; ".join(f"{k} {v['p_cross']:.3f} (z_cross {v['z_cross_med']:.2f})" for k, v in B5.items()), all(v["p_cross"] > 0.9 for v in B5.values()))

# ================================================================================================ P the predictions
banner("P   a0(z)/a0(0) FOR EVERY BRANCH, z = 0-5, DESI DR2 chains propagated (dex; median [16, 84])")
PRED = {}


def band(arr, wt):
    return [float(v) for v in C.wpct(arr, wt, [16, 50, 84])]


for k in C.DESI_ORDER:
    wt, w0s, was, oms = CH_DATA[k]
    for br, fn in C.CPL_MAPS.items():
        PRED.setdefault(f"{br}-CPL", {})[k] = {str(z): band(dex(fn(z, w0s, was)), wt) for z in ZP}
    PRED.setdefault("rival H(z)", {})[k] = {str(z): band(dex(C.R_total(z, w0s, was, oms)), wt) for z in ZP}
# the thawing grid (lambda x Omega_m)
t_grid = time.time()
LAMS = np.concatenate([[0.0], np.linspace(0.05, 2.0, 40)])      # lambda > 2 has no thawing solution at low Omega_m (probe 3)
OMS = np.round(np.arange(0.27, 0.3901, 0.01), 4)
GRID = {key: np.zeros((len(OMS), len(LAMS), len(ZG))) for key in ("dens", "V", "press", "logE", "w")}
W0G, W0E, WAE = (np.zeros((len(OMS), len(LAMS))) for _ in range(3))
for i, omv in enumerate(OMS):
    for j, lv in enumerate(LAMS):
        tr = C.thaw_tracks(lv, float(omv), ZG)
        for key in GRID:
            GRID[key][i, j] = tr[key]
        W0G[i, j] = tr["w0"]
        W0E[i, j], WAE[i, j] = C.cpl_equivalent(ZG, tr["w"])
P(f"    thawing grid: {len(OMS)} Omega_m x {len(LAMS)} lambda nodes built in {time.time() - t_grid:.0f} s; w0 range {W0G.min():.3f} to "
  f"{W0G.max():.3f}; monotone in lambda at every Omega_m: {bool(np.all(np.diff(W0G, axis=1) > 0))}")
MAPKEY = {"B": "dens", "C": "V", "D": "press"}


def thaw_w0_matched(key, w0s, oms, zq):
    return C.thaw_interp_w0(LAMS, OMS, ZG, W0G, GRID[key], w0s, oms, zq)


FLAGS = {}
for k in C.DESI_ORDER:
    wt, w0s, was, oms = CH_DATA[k]
    FLAGS[k] = dict(w0_below_m1=float(np.sum(wt[w0s < -1]) / np.sum(wt)), om_outside=float(np.sum(wt[(oms < OMS[0]) | (oms > OMS[-1])]) / np.sum(wt)),
                    w0_above_grid=float(np.sum(wt[w0s > W0G.min(axis=0)[-1]]) / np.sum(wt)))
    for br, key in MAPKEY.items():
        arr = thaw_w0_matched(key, w0s, oms, ZP)
        PRED.setdefault(f"{br}-thaw(w0)", {})[k] = {str(z): band(arr[:, iz], wt) for iz, z in enumerate(ZP)}
# the posterior-conditioned thawing field: a Gaussian proxy of each posterior in (w0, wa, Omega_m)
PCW = {}
for k in C.DESI_ORDER:
    wt, w0s, was, oms = CH_DATA[k]
    Xm = np.vstack([w0s, was, oms])
    mu = np.average(Xm, axis=1, weights=wt)
    cov = np.cov(Xm, aweights=wt)
    ci = np.linalg.inv(cov)
    dvec = np.stack([W0E - mu[0], WAE - mu[1], np.broadcast_to(OMS[:, None], W0E.shape) - mu[2]], axis=-1)
    q2 = np.einsum("ija,ab,ijb->ij", dvec, ci, dvec)
    wn = np.exp(-0.5 * (q2 - q2.min()))
    wn /= wn.sum()
    ib = np.unravel_index(np.argmin(q2), q2.shape)
    q_lcdm = float(q2[:, 0].min())                                     # Lambda (the lambda = 0 nodes), same 3-d proxy
    PCW[k] = dict(weights=wn, best=(float(OMS[ib[0]]), float(LAMS[ib[1]]), float(W0E[ib]), float(WAE[ib])), q2min=float(q2.min()),
                  q2_lcdm=q_lcdm, mean_w0eff=float(np.sum(wn * W0E)), mean_lam=float(np.sum(wn * LAMS[None, :])))
    for br, key in MAPKEY.items():
        nodes = C.thaw_nodes_at(ZG, GRID[key], ZP)
        PRED.setdefault(f"{br}-thaw(post)", {})[k] = {str(z): band(nodes[:, :, iz].ravel(), wn.ravel()) for iz, z in enumerate(ZP)}
    P(f"    {k:10s} posterior-conditioned thawing: best node Omega_m {PCW[k]['best'][0]:.2f}, lambda {PCW[k]['best'][1]:.2f} "
      f"(CPL-equivalent w0 {PCW[k]['best'][2]:+.3f}, wa {PCW[k]['best'][3]:+.3f}); chi^2-proxy {PCW[k]['q2min']:.1f} there vs "
      f"{PCW[k]['q2_lcdm']:.1f} for Lambda (same 3-d proxy); weighted <w0_eff> {PCW[k]['mean_w0eff']:+.3f}, <lambda> {PCW[k]['mean_lam']:.2f}")
    P(f"    {'':10s} flags: w0 < -1 (set to Lambda) {FLAGS[k]['w0_below_m1']:.4f}; Omega_m outside [0.27, 0.39] (clipped) "
      f"{FLAGS[k]['om_outside']:.4f}; w0 above the grid (clipped) {FLAGS[k]['w0_above_grid']:.4f}")
# A (flat) and its MUTATE
R_A = (lambda z: np.sqrt(C.OM_M * (1 + z) ** 3 + C.OM_L)) if MUTATE else (lambda z: np.ones_like(np.asarray(z, float)))
PRED["A"] = {k: {str(z): [float(dex(R_A(z)))] * 3 for z in ZP} for k in C.DESI_ORDER}
# LCDM-emergent reference
LCR = {str(z): [*C.lcdm_emergent_range(z)[:1], float(dex(C.lcdm_emergent(z))), C.lcdm_emergent_range(z)[1]] for z in ZP}
ORDER_P = ["A", "B-CPL", "C-CPL", "D-CPL", "B-thaw(w0)", "C-thaw(w0)", "D-thaw(w0)", "B-thaw(post)", "C-thaw(post)", "D-thaw(post)", "rival H(z)"]
ZSHOW = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0]
P("\n    branch            z:  " + "".join(f"{z:>22.2f}" for z in ZSHOW))
for br in ORDER_P:
    b = PRED[br]["DESY5"]
    P(f"    {br:16s} DESY5  " + "".join(f"{b[str(z)][1]:+.3f} [{b[str(z)][0]:+.3f},{b[str(z)][2]:+.3f}]".rjust(22) for z in ZSHOW))
    P(f"    {'':16s} P+/U3  " + "".join(f"{PRED[br]['Pantheon+'][str(z)][1]:+.3f} / {PRED[br]['Union3'][str(z)][1]:+.3f}".rjust(22) for z in ZSHOW))
P(f"    {'LCDM-emergent':16s} (L274) " + "".join(f"{LCR[str(z)][1]:+.3f} [{LCR[str(z)][0]:+.3f},{LCR[str(z)][2]:+.3f}]".rjust(22) for z in ZSHOW))
P("    (z > 2.5 extrapolates CPL fits constrained at z <~ 2.3; the thawing rows are healthy fields, not fits)")
OUT["numbers"]["P"] = dict(pred=PRED, lcdm_emergent=LCR, flags=FLAGS, posterior_conditioned={k: {kk: vv for kk, vv in v.items() if kk != "weights"} for k, v in PCW.items()})
NZS = int(np.searchsorted(ZG, 3.5)) + 1                            # part 2 needs z <= 3.5 only
GRIDF = os.path.join(HERE, NAME + "_thawgrid.json")                  # the tracks: a compact companion file, main run only
OUT["numbers"]["thaw_grid"] = dict(lams=LAMS.tolist(), oms=OMS.tolist(), zg=ZG.tolist(), w0=W0G.tolist(), w0_eff=W0E.tolist(), wa_eff=WAE.tolist(),
                                   post_weights={k: PCW[k]["weights"].tolist() for k in C.DESI_ORDER},
                                   tracks_file=None if MUTATE else os.path.basename(GRIDF), tracks_zmax=float(ZG[NZS - 1]))
if not MUTATE:                                                       # the grid does not depend on the MUTATE switch (A only)
    json.dump(dict(lams=LAMS.tolist(), oms=OMS.tolist(), zg=ZG[:NZS].tolist(), w0=W0G.tolist(),
                   tracks={key: np.round(GRID[key][:, :, :NZS], 7).tolist() for key in ("dens", "V", "press", "logE")}),
              open(GRIDF, "w"), separators=(",", ":"))
g25 = lambda br, k="DESY5", i=1: PRED[br][k]["2.5"][i]
check("P1 = H6 (CPL rows, reported as they fall) at z = 2.5 on DESY5: B-CPL -0.099 [-0.140, -0.060], C-CPL -0.034 (band within "
      "+/-0.03), D-CPL +0.030 [+0.007, +0.053] (the pre-declared values)",
      f"B {g25('B-CPL'):+.3f} [{g25('B-CPL', i=0):+.3f}, {g25('B-CPL', i=2):+.3f}]; C {g25('C-CPL'):+.3f} [{g25('C-CPL', i=0):+.3f}, "
      f"{g25('C-CPL', i=2):+.3f}]; D {g25('D-CPL'):+.3f} [{g25('D-CPL', i=0):+.3f}, {g25('D-CPL', i=2):+.3f}]",
      abs(g25("B-CPL") + 0.099) < 0.005 and abs(g25("C-CPL") + 0.034) < 0.005 and abs(g25("D-CPL") - 0.030) < 0.005
      and g25("C-CPL", i=2) - g25("C-CPL", i=0) < 0.06, load_bearing=False)
thw = {br: [PRED[f"{br}-thaw(w0)"][k]["2.5"][1] for k in C.DESI_ORDER] for br in "BCD"}
thp = {br: [PRED[f"{br}-thaw(post)"][k]["2.5"][1] for k in C.DESI_ORDER] for br in "BCD"}
frac = [thp["C"][i] / thw["C"][i] for i in range(3)]
check("P2 = H6 (thawing rows, reported as they fall) the w0-matched healthy field rises at z = 2.5 by C +0.07..+0.16, B "
      "+0.05..+0.12, D +0.09..+0.20; the posterior-conditioned healthy field rises by 30-60% of the w0-matched rise (C <= +0.08)",
      "w0-matched (DESY5/P+/U3): " + "; ".join(f"{br} " + "/".join(f"{v:+.3f}" for v in thw[br]) for br in "BCD") +
      " | posterior-conditioned: " + "; ".join(f"{br} " + "/".join(f"{v:+.3f}" for v in thp[br]) for br in "BCD") +
      " | C ratio " + "/".join(f"{f_:.2f}" for f_ in frac),
      all(0.07 <= v <= 0.16 for v in thw["C"]) and all(0.05 <= v <= 0.12 for v in thw["B"]) and all(0.09 <= v <= 0.20 for v in thw["D"])
      and all(0.3 <= f_ <= 0.6 for f_ in frac) and max(thp["C"]) <= 0.08, load_bearing=False)

# ================================================================================================ P5 both footings, z = 0
banner("P5  BOTH FOOTINGS: absolute a0(z) (DESY5 medians) and the z = 0 normalisation under each DESI cosmology")
ABS = {}
for foot in ("canonical", "alt"):
    ABS[foot] = {br: {str(z): C.A0[foot] * 10 ** PRED[br]["DESY5"][str(z)][1] for z in ZP} for br in ORDER_P}
    P(f"    {foot:9s} a0(z) [1e-11 m/s^2]  " + "".join(f"{'z=' + str(z):>9s}" for z in (0.0, 1.0, 2.5, 5.0)))
    for br in ORDER_P:
        P(f"    {'':9s} {br:22s} " + "".join(f"{ABS[foot][br][str(z)] * 1e11:9.3f}" for z in (0.0, 1.0, 2.5, 5.0)))
dt = C.desi_table_from_record()
NORM = {}
for k in C.DESI_ORDER:
    ratio = (dt[k]["H0"] / C.H0_KMS) * math.sqrt((1 - dt[k]["Om"]) / C.OM_L)
    NORM[k] = dict(H0=dt[k]["H0"], Om=dt[k]["Om"], dlog_a0_at_kappa_half=math.log10(ratio), kappa_to_keep_a0=0.5 / ratio,
                   kappa_alt_to_keep=C.KAPPA["alt"] / ratio)
    P(f"    {k:10s} (H0 {dt[k]['H0']}, Omega_m {dt[k]['Om']}): kappa = 1/2 held -> a0(0) moves {NORM[k]['dlog_a0_at_kappa_half']:+.4f} dex; "
      f"a0(0) held -> kappa = {NORM[k]['kappa_to_keep_a0']:.4f} (alt {NORM[k]['kappa_alt_to_keep']:.4f})")
OUT["numbers"]["P5"] = dict(absolute=ABS, z0_normalisation=NORM)
nv = [NORM[k]["dlog_a0_at_kappa_half"] for k in C.DESI_ORDER]
check("P5 = H7 (reported) holding kappa = 1/2, the DESI w0wa cosmologies move today's a0 by -0.014..+0.002 dex (rho_DE,0 ~ H0^2 "
      "Omega_DE changes); holding a0(0), kappa refits by the same fraction -- a z = 0 normalisation, not a redshift dependence",
      ", ".join(f"{k} {v:+.4f}" for k, v in zip(C.DESI_ORDER, nv)), -0.016 <= min(nv) and max(nv) <= 0.004, load_bearing=False)

# ================================================================================================ HEADLINE
banner("HEADLINE: branch A (the unimodular tie) is exactly flat" + ("  [MUTATE: A reads rho_total]" if MUTATE else ""))
fl = max(abs(PRED["A"][k][str(z)][1]) for k in C.DESI_ORDER for z in ZP)
flat_abs = max(abs(ABS[f]["A"][str(z)] / C.A0[f] - 1) for f in ("canonical", "alt") for z in ZP)
check("HEADLINE-FLAT branch A's a0(z)/a0(0) = 1 at every z of the table (0-5), on both footings, whatever the dark energy does "
      "(1e-12)", f"max |log ratio| {fl:.2e}; max |a0(z)/a0(0) - 1| over both footings {flat_abs:.2e}" +
      (f"; z = 2.5 {PRED['A']['DESY5']['2.5'][1]:+.3f} dex" if MUTATE else ""), fl < 1e-12 and flat_abs < 1e-12,
      "A decouples a0 from the dark energy's dynamics: DESI's w(z) does not touch the flat law" if not MUTATE else
      "MUTATE: the rho_total tie is the rival law a0 ~ H(z)")

# ================================================================================================ B6 + W the ledger
banner("B6/W  THE BRANCH LEDGER: formula, field content, constants, action, ghost/crossing")
LEDGER = [
    ("A", "a0(z)/a0(0) = 1 (a0 reads the HT constant Lambda_0)", "HT 3-form multiplier: 1 global DOF, 0 local",
     "kappa (FITTED) + Lambda (measured); with an evolving DE component also the HT share of today's DE (1 choice)",
     "YES (XR20 T1, XR30)", "none; flat for ANY dark-energy history"),
    ("B", "sqrt(rho_DE(z)/rho_DE(0))", "none new if leaf-averaged (khronon leaves); +1 derivative coupling if local",
     "kappa + the DE history (measured)", "leaf-averaged: YES, healthy (B4); local alpha(phi, X): ILL-POSED for 1+w >~ 0.05 (B3b)",
     "following the CPL fits: a ghost or braided DE past z_cross; healthy DE: a thawing field (rises)"),
    ("C", "sqrt(V(z)/V(0)), V = (rho - p)/2", "none new beyond the DE scalar (alpha(phi))", "kappa + the DE history",
     "YES, local, healthy (XR20 E7; B3d)", "following the CPL fits: a ghost past z_cross; healthy DE: rises"),
    ("D", "sqrt(p(z)/p(0)); stage-17's own law flat < 1% (z <= 5)", "none new if leaf-averaged; stage-17: the (closed) v9 sector",
     "kappa + the DE history", "leaf-averaged: YES (B4); local alpha(phi, X) / stage-17 form: GHOST within ~550 AU of every star (B3a)",
     "following the CPL fits: a ghost past z_cross; with a w = -1 vacuum: flat (= A)"),
]
for br, form, fields, consts, action, need in LEDGER:
    P(f"    {br}: {form}\n       fields: {fields}\n       constants: {consts}\n       action: {action}\n       ghost/crossing: {need}")
OUT["ledger"] = [dict(branch=a, a0z=b, fields=c, constants=d, action=e, ghost_or_crossing=f) for a, b, c, d, e, f in LEDGER]
check("B6 = H5 (reported) THE CONSTANT COUNT: every branch carries kappa (fitted) and the dark-energy history (measured) and no "
      "other constant; branch A with an evolving dark-energy component needs one extra choice (the HT share of today's DE), "
      "which moves kappa's fitted value, not the flat law", "4 branches tabulated", True, load_bearing=False)

# ================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in R.CH if lb and not ok)
banner("VERDICT")
P(f"""  The founding principle (a0 set by the vacuum's energy, kappa = 1/2 fitted) fixes the form, not the reading.  Four readings:
  A (the unimodular constant) is flat for any dark-energy history and has a healthy action; C (the potential) has a healthy local
  action; B (the density) and D (the pressure) are realisable locally only through the dark energy's kinetic scalar, and that
  derivative coupling is ill-posed (B, for 1 + w >~ {thr_nm['1 AU']:.2f}) or a ghost (D, within ~{H3[('J_P2', 'canonical')]['rD_AU']:.0f} AU of every star);
  both are healthy as leaf-averaged (global) ties on the khronon's leaves, with no new field or constant.
  Under DESI DR2 (DESY5, chains propagated) at z = 2.5: A 0.000; B {g25('B-CPL'):+.3f}, C {g25('C-CPL'):+.3f}, D {g25('D-CPL'):+.3f} following
  the fits (which cross w = -1: a ghost or braided dark energy is needed); a healthy thawing field raises a0 instead:
  w0-matched C {thw['C'][0]:+.3f}, conditioned on the posterior C {thp['C'][0]:+.3f} (B {thp['B'][0]:+.3f}, D {thp['D'][0]:+.3f}).
  Every branch adds no constant beyond kappa and the measured dark-energy history.  kappa stays FITTED; nothing here derives it.""")
OUT["verdict"] = dict(n_checks=len(R.CH), n_fail_load_bearing=n_fail)
json.dump(OUT, open(JSN, "w"), indent=1, default=str)
rc = 0 if n_fail == 0 else 1
P(f"\n  {len(R.CH) - sum(1 for _, ok, _l in R.CH if not ok)}/{len(R.CH)} checks pass; load-bearing failures: {n_fail}; wrote "
  f"{os.path.basename(JSN)}  ({time.time() - T_START:.0f} s)")
P(f"rc = {rc}")
TEE.flush()
sys.stdout = sys.__stdout__
TEE.close()
sys.exit(rc)
