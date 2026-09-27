#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG5 (1/6) -- THE PRINCIPLE: the vacuum caps the stress the dark field can carry, and the cap is written in at collapse.

THE CHAIN (lane CFG5 of campaign_fresh_gravity).  Gravity is exactly GR; there is no MOND field.  The dark component is the
framework's own cold coherent field (FL1: a classical order parameter at occupation ~1e77, not a particle species; its mass is
still required).  The field already has a conversion that ejects dark mass (FK1: its two real components split by
eps Re(Phi^2); phi_H phi_H -> phi_L phi_L back to back at v_k = 575-650 km/s, Bose-stimulated).  The founding idea: the galaxy
law is written into each halo DURING COLLAPSE by a process keyed to a0 = kappa c sqrt(G rho_Lambda).

THE PRINCIPLE, IN PLAIN WORDS.  The vacuum limits how hard the dark field can be squeezed.  The field's own internal stress --
the momentum flux of its streams, measured in its mean rest frame, a local invariant of its stress tensor -- cannot exceed
the stress at which a self-gravitating body of that field would pull with the vacuum's acceleration a0.  Where collapse drives
the stress past that limit, the field changes state (FK1's conversion) and the converted part leaves (galaxies) or stays
bound and hotter (clusters).  The conversion is a coherent, Bose-stimulated process, so it runs while the crossing streams are
still cold; a phase-mixed halo is a broadband pump and no longer converts.  The cap is therefore written at shell crossing:
a fossil of collapse.

THE DERIVATION (this script, sympy + numbers).
  P1  The self-gravitating isothermal equilibrium is the unique self-similar one, and on it 8 pi G P = g^2 at every radius.
      That identity turns a stress into an acceleration without a new number: the limit is 8 pi G P_d <= a0^2.
  P2  The same limit in the three forms the brief lists -- the field energy density against rho_Lambda c^2
      (P_d <= kappa^2 rho_Lambda c^2/8pi), the local acceleration (g_SIS <= a0), and the collapse rate against the vacuum's
      rate (sqrt(8 pi G rho_d) sigma_d <= kappa c sqrt(G rho_Lambda)): identities, one threshold.  TIED to the core law.
  P3  At collapse the baryons still follow the dark field (fraction f_b, Planck 2018).  The dark field carries (1 - f_b) of
      the stress, so the cap reads g <= a0/sqrt(1 - f_b), i.e. the dark field's own pull g_d <= sqrt(1 - f_b) a0 = 0.918 a0.
      f_b is measured by the CMB; no constant is added.
  P4  The switch is DERIVED, not added: a single cold stream carries no internal stress.  A plane collapse sampled with N
      particles has coarse-grained stress exactly zero until shell crossing and positive after.  The Hubble flow and every
      linear perturbation are single-stream, so the linear universe never converts: the CMB, BAO and linear growth are the
      cold field's (LCDM's).  Post-crossing sheets and filaments sit orders of magnitude below the cap: the conversion stays
      out of the voids and the web (the record's XR19 found the same for FK1's trigger; here it is a consequence of the gate).
  P5  (reported, estimate) The coherence clause: FK1's conversion in a phase-mixed halo is Doppler-broadened; its rate falls by
      sqrt(pi) G/(m v_k sigma) relative to a cold stream (FP10 A5's broadband rate over the narrowband one).
  P6  [data, pre-declared H1] The principle's cap against the observed dark acceleration in SPARC.
  P7  [pre-declared H2] The relaxed fossil of a dark-dominated core: the isothermal equilibrium whose central stress is the
      cap.  Its central surface density (Burkert fit, the observers' definition) against the observed universal value.
  P8  (reported) the maximum dark pull of that relaxed core.

HYPOTHESES (declared before the first full run of this script; exploratory scratch runs are disclosed under HISTORY).
  H1  The observed dark acceleration h_obs = (g_obs - g_bar)/a0 in SPARC (the record's loader, Upsilon_d = 0.5) has a plateau
      at y = g_bar/a0 in [1.5, 5] whose median lies within 0.15 of the principle's sqrt(1 - f_b) = 0.918, on BOTH footings.
  H2  The relaxed capped core's Burkert central surface density rho_B r_B lies inside the observed 1-sigma band of the
      universal value, 89-224 Msun/pc^2 (central 141), on BOTH footings.
CHECKS
  C1 CONTROL [load-bearing]: FK1's committed N1, N2, N3 reproduced exactly (FK1 executed read-only, file writes refused).
  C2 CONTROL [load-bearing]: the record's SPARC RAR fit (L92 A1 = L61's gate): 155 galaxies, 2786 points, the bounded-boost
     kernel rms 0.1453 / 0.1421 dex, medians +0.030 / +0.003, on the machinery footings, to the printed digits.
  P1, P2, P3 [load-bearing, sympy]; P4 [load-bearing, numbers]; P5 (reported); P6 = H1 [load-bearing]; P7 = H2
  [load-bearing]; P8 (reported); W the tie ledger (which of the record's own results each step uses).
MUTATE=1 sets a0 -> 0 inside the cap only (P_c = 0: every multistream dark field converts).  P6 and P7 must FAIL (rc = 1).

FOOTINGS.  canonical a0 = 9.3603e-11, alt 1.1312e-10 m/s^2 (charter); the controls use the record's 9.3619e-11 / 1.1279e-10.
kappa = 1/2 is FITTED (Z = 5.7888); nothing here derives it.

HISTORY (disclosed).  Before this script was written, three scratch explorations (not committed) were run on SPARC:
  (a) the RAR-implied dark Jeans stress P_d(0) spans 0.05-94 P_c and rises with baryon dominance -- so a stress cap read on
      the FINAL (baryon-condensed) configuration cannot be the RAR's fossil; this fixed the collapse-time reading (P3);
  (b) the binned observed dark acceleration rises to ~0.8-0.95 a0 (canonical) / ~0.7 a0 (alt) at y ~ 1.5-5 and falls beyond;
  (c) fossil variants on abundance-matched NFW halos (lane script 3 re-does this with pre-declared hypotheses).
The tolerances of H1/H2 were set from the observational uncertainties (Upsilon +-0.1 moves g_bar by +-0.08 dex; the
universal surface density's own 1-sigma band), not from the explorations' numbers.

Run from the repository root:  python3 campaign_fresh_gravity/CFG5_1_principle.py
"""
import os, sys, math, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import CFG5_common as C

L = C.Lane("CFG5_1_principle", "CFG5.1")
P, banner, check = L.P, L.banner, L.check
MUT = L.MUTATE
P(__doc__.split("CHECKS")[0].strip())
if MUT:
    P("\n  *** MUTATE=1: a0 -> 0 inside the cap (P_c = 0) -- P6 (H1) and P7 (H2) must FAIL ***")
A0 = {f: (0.0 if MUT else a) for f, a in C.FOOT.items()}          # the cap's a0 (the data's y always uses the true a0)

# ============================================================================================ C1 FK1's N1-N3 exactly
banner("C1  CONTROL: FK1's committed N1, N2, N3 reproduced exactly (FK1 executed read-only)")
PFK1 = os.path.join(C.REPO, "real_research", "dark_fluid_kick_2026", "FK1_kick_as_phase_change.py")
JFK1 = json.load(open(os.path.join(C.REPO, "real_research", "dark_fluid_kick_2026", "FK1_kick_as_phase_change_results.json")))
ns = {"__file__": PFK1, "__name__": "fk1_ro", "open": C.ro_open}
with C.quiet_env(MUTATE="0"):
    try:
        exec(compile(open(PFK1).read(), PFK1, "exec"), ns)
    except (PermissionError, SystemExit):
        pass                                                         # its results file is refused; the numbers are in ns
num = ns["OUT"]["numbers"]


def flat(d, pre=""):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(flat(v, f"{pre}/{k}"))
    elif isinstance(d, (list, tuple)):
        for i, v in enumerate(d):
            out.update(flat(v, f"{pre}[{i}]"))
    else:
        out[pre] = d
    return out


dev, nkeys = 0.0, 0
for key in ("N1", "N2", "N3"):
    a, b = flat(C.jclean(num[key])), flat(JFK1["numbers"][key])
    assert set(a) == set(b), (key, set(a) ^ set(b))
    for k in a:
        x, y = float(a[k]), float(b[k]); nkeys += 1
        dev = max(dev, abs(x - y) / max(abs(y), 1e-300))
P(f"    compared {nkeys} committed numbers of N1-N3; e.g. N1 e-folds at 2e-19 eV = {num['N1']['by_mass']['2e-19']['efolds']:.6f} "
  f"(committed {JFK1['numbers']['N1']['by_mass']['2e-19']['efolds']:.6f}); N3 G/mc^2 at 2e-19 eV = "
  f"{num['N3']['2e-19']['G_over_mc2']:.6e}; N2 background peak {num['N2']['bg_peak_factor']:.6f} at z = {num['N2']['bg_peak_z']}")
L.OUT["numbers"]["C1"] = dict(n_compared=nkeys, max_rel_dev=dev, G_over_mc2_2e19=num["N3"]["2e-19"]["G_over_mc2"],
                              efolds_2e19=num["N1"]["by_mass"]["2e-19"]["efolds"])
check("C1 CONTROL: FK1's committed N1-N3 reproduced exactly", f"{nkeys} numbers, max relative deviation {dev:.1e}", dev == 0.0)
G_OVER_MC2 = float(num["N3"]["2e-19"]["G_over_mc2"])

# ============================================================================================ C2 the record's SPARC fit
banner("C2  CONTROL: the record's SPARC RAR fit (L92 A1 = L61's gate) reproduced to the printed digits")
GAL = C.load_sparc()
NPT = sum(len(g["r"]) for g in GAL)
GB = np.concatenate([g["gb"] for g in GAL]); GO = np.concatenate([g["go"] for g in GAL])
S_SAT, D_SAT = 2.540, 0.6476


def g_bb(gb, a0):
    s = gb / a0; sc = np.clip(s, 1e-300, S_SAT)
    d = np.where(s > 0, sc / np.expm1(np.sqrt(sc)), 0.0)
    return gb + a0 * np.where(s > S_SAT, D_SAT, d)


rowc = {}
for f, a0 in C.FOOT_REC.items():
    res = np.log10(GO / g_bb(GB, a0))
    rowc[f] = (float(np.sqrt(np.mean(res ** 2))), float(np.median(res)))
txt = open(os.path.join(C.REPO, "fable_independent_2026", "L92_sparc_rar_fit.out")).read()
m = re.search(r"carried bounded-boost kernel:\s+rms ([0-9.]+) / ([0-9.]+) dex\s+medians ([+-][0-9.]+) / ([+-][0-9.]+)", txt)
mg = re.search(r"(\d+) galaxies, (\d+) points", txt)
committed = dict(n_gal=int(mg.group(1)), n_pt=int(mg.group(2)), rms=(m.group(1), m.group(2)), med=(m.group(3), m.group(4)))
mine = dict(n_gal=len(GAL), n_pt=NPT, rms=(f"{rowc['canonical'][0]:.4f}", f"{rowc['alt'][0]:.4f}"),
            med=(f"{rowc['canonical'][1]:+.3f}", f"{rowc['alt'][1]:+.3f}"))
P(f"    committed (L92 .out): {committed}\n    this lane's loader:   {mine}")
L.OUT["numbers"]["C2"] = dict(committed=committed, reproduced=mine)
check("C2 CONTROL: the record's SPARC RAR fit reproduced (155 galaxies / 2786 points; 0.1453/0.1421 dex; +0.030/+0.003)",
      mine, mine == committed)

# ============================================================================================ P1 the SIS identity
banner("P1  THE SIS IDENTITY: on the self-gravitating isothermal equilibrium 8 pi G P = g^2 at every radius")
r, s, Gs = sp.symbols("r sigma G", positive=True)
rho_sis = s ** 2 / (2 * sp.pi * Gs * r ** 2)
M_sis = sp.integrate(4 * sp.pi * r ** 2 * rho_sis, (r, 0, r))
g_sis = sp.simplify(Gs * M_sis / r ** 2)
P_sis = rho_sis * s ** 2
jeans = sp.simplify(sp.diff(P_sis, r) + rho_sis * g_sis)                       # hydrostatic (Jeans) balance
ident = sp.simplify(8 * sp.pi * Gs * P_sis - g_sis ** 2)
P(f"    rho = sigma^2/(2 pi G r^2): g = {g_sis},  P = rho sigma^2,  Jeans residual dP/dr + rho g = {jeans},  8 pi G P - g^2 = {ident}")
check("P1 on the self-gravitating isothermal equilibrium (Jeans-balanced) 8 pi G P = g^2 identically: a stress maps to an "
      "acceleration with no new number", f"Jeans residual {jeans}; 8 pi G P - g^2 = {ident}", jeans == 0 and ident == 0)

# ============================================================================================ P2 the three forms
banner("P2  ONE THRESHOLD, THREE FORMS: field energy vs rho_Lambda c^2, local acceleration, collapse rate vs vacuum rate")
kap, c_, rhoL, rhod, a0s, Pd = sp.symbols("kappa c rho_Lambda rho_d a_0 P_d", positive=True)
a0_law = kap * c_ * sp.sqrt(Gs * rhoL)
Pc = a0_law ** 2 / (8 * sp.pi * Gs)
form_energy = sp.simplify(Pc - kap ** 2 * rhoL * c_ ** 2 / (8 * sp.pi))
form_rate = sp.simplify((sp.sqrt(8 * sp.pi * Gs * rhod) * s) ** 2 - 8 * sp.pi * Gs * rhod * s ** 2)
form_rate_cap = sp.simplify((kap * c_ * sp.sqrt(Gs * rhoL)) ** 2 - 8 * sp.pi * Gs * Pc)
P(f"    P_c = a0^2/(8 pi G) with a0 = kappa c sqrt(G rho_L):  P_c - kappa^2 rho_L c^2/(8 pi) = {form_energy}")
P(f"    rate form: [sqrt(8 pi G rho_d) sigma_d]^2 = 8 pi G P_d (residual {form_rate}); vacuum side [kappa c sqrt(G rho_L)]^2 - 8 pi G P_c = {form_rate_cap}")
Pc_num = {f: C.P_cap(C.FOOT[f]) for f in C.FOOT}
frac = {f: Pc_num[f] / (C.RHO_LAMBDA_SI * C.C_SI ** 2) for f in C.FOOT}
P(f"    numbers: P_c = {Pc_num['canonical']:.4e} / {Pc_num['alt']:.4e} Pa = {frac['canonical']:.5f} / {frac['alt']:.5f} of rho_Lambda c^2 "
  f"(kappa^2/8pi = {C.KAPPA ** 2 / (8 * math.pi):.5f}; the alt footing is kappa = 0.6043 on rho_Lambda)")
L.OUT["numbers"]["P2"] = dict(P_c_Pa=Pc_num, P_c_over_rhoLc2=frac)
check("P2 the stress limit is one threshold in the three forms (energy density vs rho_Lambda c^2; acceleration; rate x speed vs "
      "vacuum rate x c): TIED to a0 = kappa c sqrt(G rho_Lambda), no new constant",
      f"residuals {form_energy}, {form_rate}, {form_rate_cap}", form_energy == 0 and form_rate == 0 and form_rate_cap == 0)

# ============================================================================================ P3 the dark-component tie
banner("P3  THE CAP ON THE DARK FIELD'S OWN PULL AT COLLAPSE: g_d <= sqrt(1 - f_b) a0")
eps_b, gg = sp.symbols("epsilon_b g", positive=True)                             # eps_b = 1 - f_b in (0, 1)
fb = 1 - eps_b
Pd_mix = (1 - fb) * gg ** 2 / (8 * sp.pi * Gs)                                  # the dark share of the mixture's SIS stress
g_lim = sp.solve(sp.Eq(Pd_mix, a0s ** 2 / (8 * sp.pi * Gs)), gg)[0]
gd_lim = sp.simplify((1 - fb) * g_lim)
P(f"    dark stress in a mixture following the dark field: P_d = (1 - f_b) g^2/(8 pi G) -> g_max = {g_lim}, g_d,max = {gd_lim}"
  f"   (epsilon_b = 1 - f_b)")
gcap = {f: C.g_cap(C.FOOT[f]) for f in C.FOOT}
P(f"    f_b = Omega_b/Omega_m = {C.F_B:.4f} (Planck 2018) -> sqrt(1 - f_b) = {math.sqrt(1 - C.F_B):.4f}: g_c = {gcap['canonical']:.4e} / {gcap['alt']:.4e} m/s^2")
L.OUT["numbers"]["P3"] = dict(f_b=C.F_B, sqrt_1_minus_fb=math.sqrt(1 - C.F_B), g_c=gcap)
check("P3 at collapse the dark field carries (1 - f_b) of the mixture's stress, so the cap reads g_d <= sqrt(1 - f_b) a0 "
      "(f_b measured by the CMB: TIED, no new constant)", f"g_d,max = {gd_lim}; = {math.sqrt(1 - C.F_B):.4f} a0",
      sp.simplify(gd_lim - sp.sqrt(1 - fb) * a0s) == 0)

# ============================================================================================ P4 the derived switch
banner("P4  THE SWITCH IS DERIVED: a single cold stream carries no stress; only shell crossing creates it")
# plane-parallel Zel'dovich collapse of one sine mode (exact until shell crossing), N particles, coarse-grained stress
Npart, Lbox, A_amp = 200000, 1.0, 1.0 / (2 * math.pi)
q = (np.arange(Npart) + 0.5) / Npart * Lbox
S_q = A_amp * np.sin(2 * math.pi * q / Lbox)                                     # displacement field (shell crossing at D = 1)
res_P4 = {}
for Dg in (0.3, 0.6, 0.9, 0.999, 1.2, 1.6, 2.5):
    x = (q + Dg * S_q) % Lbox
    v = S_q * 1.0                                                                # peculiar velocity ~ dD/dt S(q), unit rate
    nb = 400
    idx = np.minimum((x / Lbox * nb).astype(int), nb - 1)
    m = np.bincount(idx, minlength=nb).astype(float)
    mv = np.bincount(idx, weights=v, minlength=nb)
    mv2 = np.bincount(idx, weights=v * v, minlength=nb)
    # stress inside a cell: sum m (v - <v>)^2 -- zero for one stream up to the within-cell velocity gradient (resolution)
    Pcell = mv2 - mv ** 2 / np.maximum(m, 1)
    # the resolution term of a single stream: the velocity gradient across a cell; subtract it with a two-resolution test
    nb2 = 1600
    idx2 = np.minimum((x / Lbox * nb2).astype(int), nb2 - 1)
    m2 = np.bincount(idx2, minlength=nb2).astype(float); mv_2 = np.bincount(idx2, weights=v, minlength=nb2)
    mv2_2 = np.bincount(idx2, weights=v * v, minlength=nb2)
    P2c = (mv2_2 - mv_2 ** 2 / np.maximum(m2, 1)).reshape(nb, nb2 // nb).sum(1)
    # a single stream's stress falls as (cell size)^2 when the cells are refined; a multistream stress does not
    ratio = float(P2c.max() / max(Pcell.max(), 1e-300))
    res_P4[Dg] = dict(P_max=float(Pcell.max()), refine_ratio=ratio)
    P(f"    D = {Dg:5.3f}: max coarse stress (400 cells) {Pcell.max():.3e}, refined/coarse {ratio:.3f}  "
      f"({'single stream: stress is the cell-gradient term, falls ~16x on 4x refinement' if Dg < 1 else 'multistream: survives refinement'})")
single_ok = all(res_P4[D]["refine_ratio"] < 0.1 for D in (0.3, 0.6, 0.9))
multi_ok = all(res_P4[D]["refine_ratio"] > 0.5 for D in (1.2, 1.6, 2.5))
# the web against the cap
web = {}
rho_bar0 = C.OMEGA_M * C.RHO_CRIT0_SI
for lab, dlt, sg in (("sheet", 10, 20e3), ("filament", 30, 50e3), ("filament, dense", 100, 100e3),
                     ("group outskirts (r200)", 200 / C.OMEGA_M, 400e3), ("cluster outskirts (r200)", 200 / C.OMEGA_M, 900e3)):
    Pw = dlt * rho_bar0 * sg ** 2
    web[lab] = {f: Pw / C.P_cap(C.FOOT[f]) for f in C.FOOT}
    P(f"    {lab:26s}: rho = {dlt:6.0f} rho_bar, sigma = {sg / 1e3:5.0f} km/s -> P/P_c = {web[lab]['canonical']:.2e} / {web[lab]['alt']:.2e}")
L.OUT["numbers"]["P4"] = dict(zeldovich=res_P4, web=web)
check("P4 a single cold stream carries no stress (its cell stress is a resolution term that vanishes on refinement) and shell "
      "crossing creates a stress that survives refinement: the linear universe and the Hubble flow never reach the cap; the "
      "post-crossing web sits >= 100x below it (the conversion stays out of voids and the web)",
      f"refined/coarse at D = 0.3/0.6/0.9: {[round(res_P4[D]['refine_ratio'], 4) for D in (0.3, 0.6, 0.9)]}; at 1.2/1.6/2.5: "
      f"{[round(res_P4[D]['refine_ratio'], 3) for D in (1.2, 1.6, 2.5)]}; web max P/P_c = "
      f"{max(max(v.values()) for k, v in web.items() if 'outskirts' not in k):.1e}",
      single_ok and multi_ok and max(max(v.values()) for k, v in web.items() if "outskirts" not in k) < 1e-2)

# ============================================================================================ P5 coherence (reported)
banner("P5  (reported, estimate) THE COHERENCE CLAUSE: a phase-mixed halo is a broadband pump and converts ~1e3x slower")
C_KMS = 2.99792458e5
supp = {}
for sg in (30.0, 100.0, 300.0):
    for vk in (575.0, 650.0):
        supp[f"{sg:.0f}/{vk:.0f}"] = math.sqrt(math.pi) * G_OVER_MC2 * C_KMS ** 2 / (vk * sg)
P("    broadband/narrowband rate = sqrt(pi) G/(m v_k sigma), G/mc^2 = %.2e (FK1 N3 at 2e-19 eV):  " % G_OVER_MC2
  + ", ".join(f"sigma/v_k {k}: {v:.1e}" for k, v in supp.items()))
L.OUT["numbers"]["P5"] = supp
check("P5 (reported) in a phase-mixed halo the conversion rate is suppressed by ~1e-3 relative to a cold crossing stream, so the "
      "cap is written at shell crossing (an estimate with O(1) factors; FK1's halo-regime rate carries the same caveat)",
      {k: f"{v:.1e}" for k, v in supp.items()}, max(supp.values()) < 0.05, load_bearing=False)

# ============================================================================================ P6 = H1 the observed plateau
banner("P6  [H1] THE OBSERVED DARK-ACCELERATION PLATEAU IN SPARC against the principle's sqrt(1 - f_b) a0")
h1 = {}
for f, a0 in C.FOOT.items():
    y = GB / a0; hobs = (GO - GB) / a0
    sel = (y >= 1.5) & (y < 5.0)
    med = float(np.median(hobs[sel]))
    # bootstrap over galaxies (points within a galaxy are correlated)
    rng = np.random.default_rng(5)
    idx_g = np.concatenate([np.full(len(g["r"]), i) for i, g in enumerate(GAL)])
    bs = []
    for _ in range(400):
        pick = rng.integers(0, len(GAL), len(GAL))
        ww = np.concatenate([np.where(idx_g == i)[0] for i in pick])
        yy, hh = y[ww], hobs[ww]
        s2 = (yy >= 1.5) & (yy < 5.0)
        if s2.sum() > 10:
            bs.append(np.median(hh[s2]))
    pred = C.g_cap(A0[f]) / a0
    h1[f] = dict(median=med, boot_sigma=float(np.std(bs)), N=int(sel.sum()), predicted=pred, diff=med - pred)
    P(f"    [{f:9s}] y in [1.5, 5): N = {sel.sum()} points; median h_obs = {med:.3f} +- {np.std(bs):.3f} (galaxy bootstrap); "
      f"principle {pred:.3f}; difference {med - pred:+.3f}")
    for ud in (0.4, 0.6, 0.7):                                                   # reported: the Upsilon sensitivity
        G2 = C.load_sparc(ups_d=ud, ups_b=1.4 * ud)
        gb2 = np.concatenate([g["gb"] for g in G2]); go2 = np.concatenate([g["go"] for g in G2])
        s3 = (gb2 / a0 >= 1.5) & (gb2 / a0 < 5.0)
        h1[f][f"median_at_Upsilon_{ud}"] = float(np.median((go2 - gb2)[s3] / a0))
    P(f"               Upsilon_d = 0.4 / 0.6 / 0.7 (Upsilon_b = 1.4 Upsilon_d): median h_obs = "
      f"{h1[f]['median_at_Upsilon_0.4']:.3f} / {h1[f]['median_at_Upsilon_0.6']:.3f} / {h1[f]['median_at_Upsilon_0.7']:.3f} (reported)")
L.OUT["numbers"]["P6"] = h1
check("P6 [H1] the observed dark-acceleration plateau (y in [1.5, 5], Upsilon_d = 0.5) lies within 0.15 of sqrt(1 - f_b) = 0.918 "
      "on BOTH footings", {f: f"{v['median']:.3f} vs {v['predicted']:.3f} (diff {v['diff']:+.3f})" for f, v in h1.items()},
      all(abs(v["diff"]) <= 0.15 for v in h1.values()),
      f"in absolute units the plateau is {h1['canonical']['median'] * C.FOOT['canonical']:.3e} / {h1['alt']['median'] * C.FOOT['alt']:.3e} m/s^2 "
      f"(the two footings' readings of one set of points); the caps are {C.g_cap(A0['canonical']):.3e} / {C.g_cap(A0['alt']):.3e}")

# ============================================================================================ P7 = H2 the relaxed capped core
banner("P7  [H2] THE RELAXED FOSSIL OF A DARK-DOMINATED CORE: the isothermal sphere whose central stress is the cap")


def iso_sphere(xmax=60.0):
    """dimensionless isothermal sphere: psi'' + 2 psi'/x = exp(-psi) (x = r/r0, r0^2 = sigma^2/(4 pi G rho_0))."""
    f = lambda x, u: [u[1], math.exp(-u[0]) - 2 * u[1] / x]
    x0 = 1e-4
    sol = solve_ivp(f, [x0, xmax], [x0 ** 2 / 6, x0 / 3], rtol=1e-10, atol=1e-12, dense_output=True)
    xs = np.geomspace(x0, xmax, 4000)
    psi, dpsi = sol.sol(xs)
    return xs, np.exp(-psi), dpsi                                                # rho/rho_0 and d psi/dx (= g / (4 pi G rho0 r0))


xs, rr, dpsi = iso_sphere()
h2 = {}
for f, a0 in C.FOOT.items():
    a0c = A0[f]
    Pc = C.P_cap(a0c) if a0c > 0 else 0.0
    out = {}
    for sig_kms in (20.0, 50.0, 150.0):
        sig = sig_kms * 1e3
        rho0 = Pc / sig ** 2                                                     # the cap: rho_0 sigma^2 = P_c
        if rho0 <= 0:
            out[sig_kms] = dict(rhoB_rB=0.0, mean_sigma_rB=0.0, gmax_over_a0=0.0); continue
        r0 = sig / math.sqrt(4 * math.pi * C.G_SI * rho0)
        rad = xs * r0; rho = rr * rho0
        g = 4 * math.pi * C.G_SI * rho0 * r0 * dpsi
        sel = rad < 12 * r0
        fit = least_squares(lambda p: np.log(10 ** p[0] / ((1 + rad[sel] / 10 ** p[1]) * (1 + (rad[sel] / 10 ** p[1]) ** 2))) - np.log(rho[sel]),
                            [math.log10(rho0), math.log10(1.5 * r0)])
        rhoB, rB = 10 ** fit.x[0], 10 ** fit.x[1]
        Menc = np.interp(rB, rad, g * rad ** 2 / C.G_SI)
        to_msun_pc2 = C.PC ** 2 / C.MSUN
        out[sig_kms] = dict(rhoB_rB=rhoB * rB * to_msun_pc2, mean_sigma_rB=Menc / (math.pi * rB ** 2) * to_msun_pc2,
                            rB_kpc=rB / C.KPC, gmax_over_a0=float(g.max() / a0))
    h2[f] = out
    P(f"    [{f:9s}] P_c = {Pc:.3e} Pa: " + "; ".join(
        f"sigma {k:.0f} km/s: rho_B r_B = {v['rhoB_rB']:.1f} Msun/pc^2, <Sigma>(<r_B) = {v['mean_sigma_rB']:.1f}, "
        f"r_B = {v.get('rB_kpc', 0):.2f} kpc, max g/a0 = {v['gmax_over_a0']:.3f}" for k, v in out.items()))
L.OUT["numbers"]["P7"] = h2
vals = {f: h2[f][50.0]["rhoB_rB"] for f in h2}
spread = {f: max(v["rhoB_rB"] for v in h2[f].values()) / max(min(v["rhoB_rB"] for v in h2[f].values()), 1e-300) for f in h2}
check("P7 [H2] the relaxed capped core has a universal Burkert central surface density rho_B r_B (independent of sigma) inside "
      "the observed 1-sigma band 89-224 Msun/pc^2, on BOTH footings",
      {f: f"{vals[f]:.1f} Msun/pc^2 (sigma-spread {spread[f]:.3f}x)" for f in vals},
      all(89 <= vals[f] <= 224 and spread[f] < 1.01 for f in vals))

# ============================================================================================ P8 (reported)
banner("P8  (reported) THE MAXIMUM DARK PULL OF THE RELAXED CAPPED CORE")
P("    " + "; ".join(f"{f}: max g_d/a0 = {h2[f][50.0]['gmax_over_a0']:.3f}" for f in h2)
  + "  (the relaxed core of a dark-dominated system; the RAR's nu_RAR peak is 0.648 a0, the principle's collapse cap 0.918 a0)")
check("P8 (reported) the relaxed capped core's maximum dark pull, in a0 units", {f: round(h2[f][50.0]["gmax_over_a0"], 3) for f in h2},
      True, load_bearing=False)

# ============================================================================================ W the tie ledger
banner("W   THE TIE LEDGER: which of the record's own results each step uses")
L.ledger("W1", "FITTED", "kappa = 1/2 (Z = 5.7888): the only fitted constant of the core, used through a0", "core; charter")
L.ledger("W2", "TIED", "the stress cap P_c = a0^2/(8 pi G) = (kappa^2/8 pi) rho_Lambda c^2: the SIS identity maps a0 to a stress", "P1, P2")
L.ledger("W3", "TIED", "the cap is exactly constant in time and space: a0 and Lambda are one unimodular integration constant", "XR20 T1, XR30")
L.ledger("W4", "TIED", "the cap reads rho_Lambda, never the local density: the BIG-SPARC environmental null", "BIG-SPARC null (record)")
L.ledger("W5", "TIED", "the dark share at collapse (1 - f_b), f_b = 0.1564 from the CMB: g_d <= sqrt(1 - f_b) a0", "P3")
L.ledger("W6", "DERIVED", "the switch: zero stress in single-stream flow -> no conversion in the Hubble flow, the linear universe, the voids", "P4; consistent with XR19")
L.ledger("W7", "DERIVED", "the cold field is GDM(0,0,0) on linear scales before collapse: LCDM's CMB and linear growth", "GDM theorem; FL1 F5")
L.ledger("W8", "DECLARED", "the conversion mechanism and its kick v_k = 575-650 km/s (eps/m^2 = 1.84-2.35e-6)", "FK1 K2")
L.ledger("W9", "DECLARED", "the coherence clause (conversion needs a narrowband pump): a window on the coupling lambda", "P5; FK1 K3/K4")
L.ledger("W10", "DECLARED", "the field's mass m >= 2-5e-19 eV (CDM-like on every scale tested)", "FL1 F5, L383")
L.ledger("W11", "REMOVED", "FK1's K-gate exponent q and the khronon: the stress gate replaces them (no khronon in a GR chain)", "P4")
check("W the tie ledger (reported)", f"{len(L.OUT['ledger'])} links", True, load_bearing=False)

banner("VERDICT")
P(f"""  The principle is one number-free statement: the dark field's stress cannot exceed a0^2/(8 pi G) = (kappa^2/8pi) rho_Lambda c^2.
  Through the self-gravitating isothermal identity it is at once a field-energy bound against rho_Lambda c^2, an acceleration
  bound at a0 and a rate bound against the vacuum's rate (P1, P2).  At collapse the dark field carries (1 - f_b) of the stress, so
  it caps the dark field's own pull at sqrt(1 - f_b) a0 = 0.918 a0 (P3).  The switch is derived: single-stream flow carries no
  stress, so the linear universe never converts (P4).  Against SPARC: the observed dark plateau at y = 1.5-5 is
  {h1['canonical']['median']:.3f} (canonical) / {h1['alt']['median']:.3f} (alt) against 0.918 (P6); the relaxed capped core's central
  surface density is {vals['canonical']:.0f} / {vals['alt']:.0f} Msun/pc^2 against the observed 141 (89-224) (P7).
  kappa stays fitted; nothing here is closed.""")
sys.exit(L.finish())
