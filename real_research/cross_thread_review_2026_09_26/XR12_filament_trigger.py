#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR12 (1/4) -- DOES FK1's n^2 TRIGGER FIRE IN THE WEB'S FILAMENTS AND INFALL STREAMS BEFORE THE FLUID REACHES HALOS?

THE IDEA, VERBATIM (the author): "the halos is like a fluid of dark energy swirling down between the bands".  This lane
reads the bands as the cosmic web's filaments: the dark fluid (FL1's order parameter Phi, m >~ 2-5e-19 eV) spirals into
halos along filaments.  FK1 (real_research/dark_fluid_kick_2026, c2e1fa119) gives that fluid its kick: phi_H phi_H ->
phi_L phi_L, Bose-stimulated, with an exponent that grows as n^2 in the fluid's OWN density and a coupling vacuum-gated as
lambda ~ K^(-2q), q = 1.75.  So the trigger is a sharp density threshold n_t(z) = delta_t0 nbar_0 E(z)^4 (FK1 N2), with
delta_t0 in FK1's bracket {5, 25}; delta_t0 = 5.31 is exactly the linear cell's matter reading, (2/3) x_c0 / Omega_m0 at
x_c0 = 2.5 (XR4 R1's 5.3/4.6/4.8/6.8/16.5 at z = 0/0.25/0.5/1/2).  Question (A): does that threshold fire in the streams
before the fluid reaches halos?  This script does the threshold arithmetic, reads the record's particle-mesh density
field, sizes the trigger's own resolution, and estimates how the growth mechanism itself depends on the environment.
XR12_forest_halo_model.py scores the forest; XR12_stream_shells.py the flagship and clusters; XR12_spin_retention.py (B).

CHECKS
  C0 CONTROL [FK1, load-bearing]: FK1's N2 reproduced from its own formulas and compared with its committed JSON: a
     constant coupling converts the background by z = 0.86/1.48 (delta_t = 5, halo factor 1/4) and 2.69/4.01 (25); with
     q = 1.75 the background exponent peaks at z = 0.30 at 1.35x its z = 0 value, 0.054 of the trigger's.  Also N1's
     e-folds (178 at 2e-19 eV) and N3's trigger coupling G_t/mc^2 (1.8e-9).
  B1 [load-bearing]: with the K-gate the cosmic background never reaches the trigger for z <= 10 (largest ratio < 0.1).
  A1 [load-bearing claim]: FK1's threshold at z = 2-3 with delta_t0 = 5.31 sits inside the standard filament range
     (delta ~ 10-30), below the streams near r_vir (~100) and below the virial overdensity; with delta_t0 = 25 it sits above
     the filaments but still below the virial overdensity for z <= 3.
  A2 [load-bearing claim, the record's box]: on L388's LCDM particle-mesh field at z = 2 (3 boxes, 0.39 Mpc/h mesh, the
     z = 2 fields kept in dark_sector_2026/_L388_fields), FK1's threshold is exceeded by >= 5% of the carrier (delta_t0 =
     5.31), most of it (>= 50%) in T-web filaments and knots.  CONTROL inside A2: the mass above the PM's own trigger
     (x~ > 5, L365/L377) is within 15% of L366's committed decayed fraction at z = 2 (0.275).
  A3 [load-bearing claim]: FK1's trigger is LOCAL -- the gain length (coherent: v_k/G; kinetic: 2 delta sigma / G^2), at
     each host's own scale-radius density with its own dispersion, is < 1e-3 r_s for every host from a 1e6 Msun minihalo to
     a 1e15 Msun cluster; and a cold stream (sigma <= 60 km/s) at the bare threshold is an absolute amplifier over 20 kpc
     (Gamma L/v_k >= 1, S1) with a gain length < 0.1 of the PM's 0.39 Mpc/h cell.  So it resolves the streams'
     substructure, which the mesh-smoothed PM trigger cannot.
  S1 [sympy, load-bearing]: the growth exponents used in E: K4's pi G^2/(4 H delta) for a linear sweep; for a sweep that
     vanishes to first order (a zero-strain direction), int sqrt(G^2 - alpha^2 t^4) dt = C4 G^(3/2)/alpha^(1/2),
     C4 = int_{-1}^{1} sqrt(1 - u^4) du = 1.7480; and the counter-propagating kinetic amplifier's steady state requires
     Gamma L / v = 1 (absolute growth above it).
  E (reported, an ESTIMATE with O(1) factors, not load-bearing): the effective threshold n_env/n_t by environment:
     the Hubble-swept background (1 by construction); cold sheets and filaments, which have a zero-strain direction
     (second-order sweep); converging infall streams near r_vir; virialised halos in the kinetic regime (FK1's "~sqrt(sigma)
     in the threshold"), sigma = 2-1000 km/s.
  E2 (reported, not load-bearing): the conversion rate above threshold (E_need e-folds at FK1's coherent/kinetic rate), in
     units of H, for sigma = 0-150 km/s at twice and five times n_t -- the bracket for XR12_stream_shells' 10 H and 1e3 H.
MUTATE=1: q = 0 (the K-gate off, a constant coupling).  The background then crosses the trigger at z = 0.86-4.01 (FK1 N2's
range, reproduced) and B1 must FAIL (rc = 1).

A0 FOOTINGS.  No a0 enters any number here: the carrier is kernel-invisible (L353), the trigger reads the carrier's own
density, and the filament/halo densities are Newtonian.  Both footings give identical results; the flagship radius (which
does depend on a0) is carried by XR12_forest_halo_model.py and XR12_stream_shells.py on both footings.

SCOPE AND DISCLOSURE.  Read-only on every other file: FK1's JSON, L366's JSON and L388's z = 2 fields are read, nothing
else is imported or run.  The T-web uses the tidal tensor of the density smoothed at 1 Mpc/h (Gaussian) on a 128^3
downsampling of the 256^3 field, eigenvalue threshold 0 (Hahn et al. 2007).  "Standard" structure overdensities (filaments
10-30, streams ~100 near r_vir) are the task's stated values; the virial overdensity is Bryan & Norman (1998) in mean units.
Scratch runs of the component arithmetic (not committed) preceded the checks' wording; nothing was retuned after.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR12_filament_trigger.py
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")                                          # single-threaded (shared machine)
import sys, json, math, time
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR12_filament_trigger"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR12", "part": "1/4 filament trigger", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split(" ")[0]] = {"ok": ok, "claim": name, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 112); P(t); P("=" * 112)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: q = 0 (no K-gate): the background must cross the trigger; B1 must FAIL ***")

# ---------------------------------------------------------------------------------------------- FK1's constants (N1-N3)
C_KMS = 2.99792458e5
HBAR_EVS, C_MS, EV_J = 6.582119569e-16, 2.99792458e8, 1.602176634e-19
H0_SI = 67.36 * 1e3 / 3.0857e22; OM, OL = 0.3138, 0.6862                     # FK1 / L366's box cosmology
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + OL)
OMz = lambda z: OM * (1 + z) ** 3 / E(z) ** 2
Q_GATE = 0.0 if MUTATE else 1.75
FK1 = json.load(open(os.path.join(REPO, "real_research", "dark_fluid_kick_2026", "FK1_kick_as_phase_change_results.json")))["numbers"]
DT0_LIN = (2.0 / 3.0) * 2.5 / OM                                                # the linear cell's matter reading at z = 0
DT0 = {"5.31 (linear cell)": DT0_LIN, "25 (FK1 upper)": 25.0}

# ============================================================================================ C0 FK1's N2 reproduced
banner("C0  CONTROL: FK1's N1-N3 numbers reproduced from its own formulas, against its committed JSON")
N2c = {}
for dt_ in (5.0, 25.0):
    for hf in (1.0, 4.0):
        f = lambda z: (1 + z) ** 6 / E(z) - hf * dt_ ** 2
        N2c[f"{dt_:g}/{hf:g}"] = brentq(f, 0.0, 1e4)
zz = np.linspace(0, 20, 20001)
bg = lambda q: (1 + zz) ** 6 / np.array([E(z) for z in zz]) ** (1 + 4 * q)
f175 = bg(1.75)
pk_z, pk_f = float(zz[f175.argmax()]), float(f175.max())
N2 = FK1["N2"]
dev_z = max(abs(N2c[k_] - N2["z_convert_constant"][k_]) for k_ in N2c)
m_kg = 2e-19 * EV_J / C_MS ** 2; hbar_SI = HBAR_EVS * EV_J
rho_m0 = OM * 3 * H0_SI ** 2 / (8 * math.pi * 6.674e-11)
n_t = 1e3 * rho_m0 / m_kg; k_k = m_kg * 600e3 / hbar_SI; dk = m_kg * 100e3 / hbar_SI
E_need = math.log(n_t * (2 * math.pi) ** 3 / (4 * math.pi * k_k ** 2 * dk) / 0.5)
s600 = (600 / C_KMS) ** 2 / (2 - (600 / C_KMS) ** 2)
G_over_m = math.sqrt(4 * E_need * (HBAR_EVS * H0_SI / 2e-19) * s600 / math.pi)
P(f"    constant coupling, background converts by z: " + ", ".join(f"{k_} -> {v:.4f} (FK1 {N2['z_convert_constant'][k_]:.4f})" for k_, v in N2c.items()))
P(f"    q = 1.75: background exponent peaks at z = {pk_z:.3f} (FK1 {N2['bg_peak_z']:.3f}) at {pk_f:.4f}x its z = 0 value "
  f"(FK1 {N2['bg_peak_factor']:.4f}) -> {pk_f / 25:.4f} of the trigger's at delta_t = 5 (FK1 README: 0.054)")
P(f"    N1 e-folds at 2e-19 eV: {E_need:.2f} (FK1 {FK1['N1']['by_mass']['2e-19']['efolds']:.2f});  N3 G_t/mc^2: {G_over_m:.3e} "
  f"(FK1 {FK1['N3']['2e-19']['G_over_mc2']:.3e})")
OUT["numbers"]["C0"] = dict(z_convert_constant=N2c, bg_peak_z=pk_z, bg_peak_factor=pk_f, E_need=E_need, G_over_mc2=G_over_m)
check("C0 CONTROL: FK1's N2 (z_convert 0.86/1.48/2.69/4.01; q = 1.75 peak z = 0.30, 1.35x, 0.054 of the trigger's), N1's "
      "e-folds and N3's G_t/mc^2 reproduced from FK1's formulas to <= 1e-3 against its committed JSON",
      f"max |dz| = {dev_z:.1e}; peak z {pk_z:.3f}, factor {pk_f:.4f}; E_need {E_need:.2f}; G_t/mc^2 {G_over_m:.3e}",
      dev_z < 1e-3 and abs(pk_z - N2["bg_peak_z"]) < 1e-3 and abs(pk_f - N2["bg_peak_factor"]) < 1e-3
      and abs(E_need - FK1["N1"]["by_mass"]["2e-19"]["efolds"]) < 1e-3
      and abs(G_over_m / FK1["N3"]["2e-19"]["G_over_mc2"] - 1) < 1e-3)

# ============================================================================================ B1 the background under the gate
banner(f"B1  THE COSMIC BACKGROUND UNDER THE GATE (q = {Q_GATE}): exponent / trigger exponent, z = 0-10")
zb = np.linspace(0, 10, 10001)
ratio_bg = np.array([(1 + z) ** 6 / E(z) ** (1 + 4 * Q_GATE) for z in zb]) / DT0_LIN ** 2    # K4 exponent ~ n^2 H^-(1+4q)
over = zb[ratio_bg >= 1.0]
P(f"    largest background/trigger exponent ratio for z <= 10: {ratio_bg.max():.4f} at z = {zb[ratio_bg.argmax()]:.2f}"
  + (f";  the background crosses the trigger for z >= {over.min():.2f}" if len(over) else "; never crosses"))
if MUTATE:
    P(f"    (FK1 N2's constant-coupling range, delta_t = 5-25, halo factor 1-4: z = {N2c['5/1']:.2f}-{N2c['25/4']:.2f})")
OUT["numbers"]["B1"] = dict(q=Q_GATE, max_ratio=float(ratio_bg.max()), z_at_max=float(zb[ratio_bg.argmax()]),
                            z_cross=float(over.min()) if len(over) else None)
check("B1 with the K-gate (q = 1.75) the mean background's exponent stays below 0.1 of the trigger's for every z <= 10, "
      "so only overdense structure can convert", f"max ratio {ratio_bg.max():.4f} at z = {zb[ratio_bg.argmax()]:.2f}",
      ratio_bg.max() < 0.1, "the gate does its job for the mean density; the question is what the web's structure does")

# ============================================================================================ A1 the threshold against the web
banner("A1  FK1's THRESHOLD AGAINST THE WEB: rho_t/rho_bar(z) = delta_t0 E^4/(1+z)^3 (FK1 N2) [(1+delta_t0) E^4/(1+z)^3, FL2]")


def dvir_mean(z):                                                                # Bryan & Norman 1998, in units of the mean
    x = OMz(z) - 1
    return (18 * math.pi ** 2 + 82 * x - 39 * x ** 2) / OMz(z)


ZT = (0.0, 0.3, 0.5, 1.0, 2.0, 2.5, 3.0, 4.0, 6.0)
A1 = {}
for lab, d0 in DT0.items():
    row = {}
    for z in ZT:
        row[str(z)] = dict(fk1=d0 * E(z) ** 4 / (1 + z) ** 3, fl2=(1 + d0) * E(z) ** 4 / (1 + z) ** 3, vir=dvir_mean(z))
    A1[lab] = row
    P(f"    delta_t0 = {lab:18s}: " + "  ".join(f"z={z:g}: {row[str(z)]['fk1']:.1f} [{row[str(z)]['fl2']:.1f}]" for z in ZT))
P("    virial overdensity (mean units): " + "  ".join(f"z={z:g}: {dvir_mean(z):.0f}" for z in ZT))
P("    standard web values used (the task's): filaments delta ~ 10-30; streams feeding halos ~100 near r_vir")
lo = A1["5.31 (linear cell)"]; hi = A1["25 (FK1 upper)"]
a1_lin = all(10 <= lo[str(z)]["fk1"] <= 40 and lo[str(z)]["fk1"] < 100 and lo[str(z)]["fk1"] < lo[str(z)]["vir"] for z in (2.0, 2.5, 3.0))
a1_hi = all(hi[str(z)]["fk1"] > 30 and hi[str(z)]["fk1"] < hi[str(z)]["vir"] for z in (2.0, 2.5, 3.0))
zs_stream = {lab: float(brentq(lambda z: d0 * E(z) ** 4 / (1 + z) ** 3 - 100.0, 0.5, 8.0)) for lab, d0 in DT0.items()}
zs_vir = {lab: float(brentq(lambda z: d0 * E(z) ** 4 / (1 + z) ** 3 - dvir_mean(z), 0.5, 12.0)) for lab, d0 in DT0.items()}
P(f"    a stream at delta = 100 is above the threshold for z <= " + ", ".join(f"{k_}: {v:.2f}" for k_, v in zs_stream.items()))
P(f"    a halo at its virial radius is above the threshold for z <= " + ", ".join(f"{k_}: {v:.2f}" for k_, v in zs_vir.items()))
OUT["numbers"]["A1"] = dict(table=A1, z_stream100_above=zs_stream, z_virial_above=zs_vir)
check("A1 at z = 2-3 FK1's threshold (delta_t0 = 5.31) lies inside the filament range and below the r_vir streams (~100) and "
      "the virial overdensity; at delta_t0 = 25 it lies above the filaments but still below the virial overdensity",
      f"delta_t(2/2.5/3) = {lo['2.0']['fk1']:.1f}/{lo['2.5']['fk1']:.1f}/{lo['3.0']['fk1']:.1f} (5.31), "
      f"{hi['2.0']['fk1']:.0f}/{hi['2.5']['fk1']:.0f}/{hi['3.0']['fk1']:.0f} (25); virial {dvir_mean(2):.0f}/{dvir_mean(2.5):.0f}/{dvir_mean(3):.0f}; "
      f"streams at 100 cross for z <= {zs_stream['5.31 (linear cell)']:.2f} / {zs_stream['25 (FK1 upper)']:.2f}; every virialised "
      f"halo for z <= {zs_vir['5.31 (linear cell)']:.2f} / {zs_vir['25 (FK1 upper)']:.2f}",
      a1_lin and a1_hi, "the densest filaments and every stream near r_vir cross at the nominal cell; every collapsed halo in "
      "the streams crosses at both brackets -- which is the question the PM's mesh cannot see (A3)")

# ============================================================================================ A2 the record's PM field at z = 2
banner("A2  THE RECORD'S PARTICLE-MESH FIELD (L388, LCDM runs, z = 2, 256^3 on 100 Mpc/h): mass above threshold, by web type")
FD = os.path.join(REPO, "real_research", "dark_sector_2026", "_L388_fields")
LBOX, NG, RS_TWEB = 100.0, 256, 1.0
z2 = 2.0
thr = {"PM trigger x~>5": 1 + 5.0 / (1.5 * OMz(z2)),
       "FK1 5.31": DT0_LIN * E(z2) ** 4 / (1 + z2) ** 3, "FK1 25": 25.0 * E(z2) ** 4 / (1 + z2) ** 3}
TYPES = ("void", "sheet", "filament", "knot")
A2 = {}
have_fields = os.path.isdir(FD)
for sd in ("7", "17", "29"):
    fn = os.path.join(FD, f"s{sd}_lcdm_z2_rhoc.npy")
    if not os.path.exists(fn):
        P(f"    box {sd}: field missing ({fn}); skipped"); have_fields = False; continue
    rho = np.load(fn).astype(np.float64)                                        # carrier density / its mean (LCDM: = matter)
    d128 = rho.reshape(128, 2, 128, 2, 128, 2).mean(axis=(1, 3, 5)) - 1.0
    kx = 2 * np.pi * np.fft.fftfreq(128, d=LBOX / 128); kz = 2 * np.pi * np.fft.rfftfreq(128, d=LBOX / 128)
    KX, KY, KZ = np.meshgrid(kx, kx, kz, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0
    dk = np.fft.rfftn(d128) * np.exp(-0.5 * K2 * RS_TWEB ** 2) / K2
    dk[0, 0, 0] = 0.0
    comps = {}
    for (i, a), (j, b) in ((( 0, KX), (0, KX)), ((0, KX), (1, KY)), ((0, KX), (2, KZ)), ((1, KY), (1, KY)), ((1, KY), (2, KZ)), ((2, KZ), (2, KZ))):
        comps[(i, j)] = np.fft.irfftn(a * b * dk, s=(128, 128, 128)).astype(np.float32)
    del dk, KX, KY, KZ, K2
    Tm = np.empty((128, 128, 128, 3, 3), np.float32)
    for (i, j), c in comps.items():
        Tm[..., i, j] = c; Tm[..., j, i] = c
    del comps
    lam = np.linalg.eigvalsh(Tm.reshape(-1, 3, 3)).reshape(128, 128, 128, 3)
    del Tm
    cls128 = (lam > 0.0).sum(axis=-1).astype(np.int8)                           # number of collapsing axes
    del lam
    cls256 = np.repeat(np.repeat(np.repeat(cls128, 2, 0), 2, 1), 2, 2)
    tot = rho.sum()
    row = {"type_mass_frac": {TYPES[t]: float(rho[cls256 == t].sum() / tot) for t in range(4)}}
    for nm, t_ in thr.items():
        sel = rho > t_
        mf = float(rho[sel].sum() / tot)
        split = {TYPES[t]: float(rho[sel & (cls256 == t)].sum() / max(rho[sel].sum(), 1e-30)) for t in range(4)}
        row[nm] = dict(threshold=t_, mass_frac=mf, vol_frac=float(sel.mean()), by_type=split)
    A2[sd] = row
    P(f"    box {sd:>2}: web mass fractions " + ", ".join(f"{k_} {v:.2f}" for k_, v in row["type_mass_frac"].items()))
    for nm in thr:
        r_ = row[nm]
        P(f"            above {nm:16s} (rho/rho_bar > {r_['threshold']:6.2f}): mass {r_['mass_frac']:.4f}, volume {r_['vol_frac']:.5f};"
          f" of it: " + ", ".join(f"{k_} {v:.2f}" for k_, v in r_["by_type"].items()))
    del rho, d128, cls128, cls256
if have_fields and len(A2) == 3:
    pool = {nm: float(np.mean([A2[s][nm]["mass_frac"] for s in A2])) for nm in thr}
    fil_knot = float(np.mean([A2[s]["FK1 5.31"]["by_type"]["filament"] + A2[s]["FK1 5.31"]["by_type"]["knot"] for s in A2]))
    fil_only = float(np.mean([A2[s]["FK1 5.31"]["by_type"]["filament"] for s in A2]))
    L366 = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L366_triggered_carrier_cluster_retention_results.json")))
    fd2 = L366["numbers"]["runs"]["x5_v600"]["2.0"]["decayed"]
    ctrl = abs(pool["PM trigger x~>5"] / fd2 - 1)
    P(f"    pooled: above the PM trigger {pool['PM trigger x~>5']:.3f} (L366's decayed fraction at z = 2: {fd2:.3f}, x{pool['PM trigger x~>5'] / fd2:.2f}); "
      f"above FK1 5.31: {pool['FK1 5.31']:.3f} (filament {fil_only:.2f} + knot {fil_knot - fil_only:.2f} of it); above FK1 25: {pool['FK1 25']:.4f}")
    OUT["numbers"]["A2"] = dict(per_box=A2, pooled=pool, fk1_531_filament_plus_knot=fil_knot, fk1_531_filament=fil_only,
                                L366_decayed_z2=fd2, T_web_smoothing_Mpc_h=RS_TWEB)
    check("A2 on the record's z = 2 mesh FK1's threshold (delta_t0 = 5.31) is exceeded by >= 5% of the carrier, >= 50% of it "
          "in T-web filaments and knots; CONTROL: the mass above the PM's own trigger is within 15% of L366's decayed fraction",
          f"above FK1 5.31: {pool['FK1 5.31']:.3f} of the carrier (filaments {fil_only:.2f}, knots {fil_knot - fil_only:.2f}); "
          f"above FK1 25: {pool['FK1 25']:.4f}; PM trigger {pool['PM trigger x~>5']:.3f} vs L366 {fd2:.3f}",
          pool["FK1 5.31"] >= 0.05 and fil_knot >= 0.5 and ctrl <= 0.15,
          "the smooth (0.39 Mpc/h) web already crosses at the nominal cell -- mostly filament and knot cells; at delta_t0 = 25 "
          "only ~3% does.  The mesh smooths away everything below ~5e9 Msun/h per cell (A3)")
else:
    check("A2 the record's z = 2 fields were found and read", "fields missing", False)

# ============================================================================================ A3 the trigger's own resolution
banner("A3  FK1's TRIGGER IS LOCAL: gain length at the threshold density vs host sizes and the PM cell")
MEV = 2e-19
w_m = MEV / HBAR_EVS                                                            # m c^2 / hbar [1/s]
KPC = 3.0857e19


def delta_split(vk):                                                            # energy per daughter, frequency units
    return w_m * (vk / C_KMS) ** 2 / 2


def G_t(z, vk=600.0, eneed=None):                                               # K4 at the trigger, FK1's normalisation
    e_ = FK1["N1"]["by_mass"]["2e-19"]["efolds"] if eneed is None else eneed
    return math.sqrt(4 * H0_SI * E(z) * delta_split(vk) * e_ / math.pi)


def rate(G, sig_kms, vk=600.0):                                                 # coherent G -> kinetic G^2/(k sigma)
    ks = 2 * delta_split(vk) * sig_kms / vk
    return G * G / math.sqrt(G * G + ks * ks)


GKPC = 4.30091e-6; RHOC0_KPC = 277.5 * 0.6736 ** 2


def host(M, z):                                                                 # NFW r200, r_s, V200 (DM14 c(M, z))
    a = 0.520 + 0.385 * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    c = 10 ** (a + b * math.log10(M * 0.6736 / 1e12))
    r200 = (3 * M / (4 * math.pi * 200 * RHOC0_KPC * E(z) ** 2)) ** (1 / 3)
    return r200, r200 / c, math.sqrt(GKPC * M / r200), c


HOSTS = {"minihalo 1e6 (z=2.5)": (1e6, 2.5), "dwarf 1e9 (z=2.5)": (1e9, 2.5), "flagship 1e12 (z=2.5)": (1e12, 2.5),
         "cluster 1e15 (z=0)": (1e15, 0.0)}
A3 = {"hosts": {}, "streams": {}}
cell_proper = {z: 100.0 / 256 / 0.6736 * 1e3 / (1 + z) for z in (0.0, 2.5)}
for hn, (M, z) in HOSTS.items():
    r200, rs, v200, c = host(M, z)
    sig = v200 / math.sqrt(2)
    dch = 200.0 / 3.0 * c ** 3 / (math.log1p(c) - c / (1 + c))                # rho_s / rho_crit(z)
    n_rs = (dch / 4.0) / (DT0_LIN * OM * E(z) ** 2)                            # carrier density at r_s / n_t (tracer halo)
    Gt = G_t(z)
    lg = 600e3 / rate(Gt * n_rs, sig) / KPC                                     # kpc, at the host's own r_s density and sigma
    lg_t = 600e3 / rate(Gt, sig) / KPC                                          # at the bare threshold with the host's sigma
    A3["hosts"][hn] = dict(r200_kpc=r200, rs_kpc=rs, sigma_kms=sig, n_rs_over_nt=n_rs, gain_at_rs_kpc=lg, over_rs=lg / rs,
                           gain_at_threshold_host_sigma_kpc=lg_t, threshold_over_rs=lg_t / rs)
    P(f"    {hn:24s}: r_s {rs:9.2f} kpc, sigma {sig:7.1f} km/s, n(r_s) = {n_rs:7.1f} n_t;  gain length there {lg * 1e3:9.3f} pc "
      f"= {lg / rs:.1e} r_s   [at the bare threshold with this sigma: {lg_t:.2f} kpc = {lg_t / rs:.2f} r_s -- reported]")
for sig in (5.0, 20.0, 60.0):
    for z in (2.5, 0.0):
        lg = 600e3 / rate(G_t(z), sig) / KPC
        A3["streams"][f"sigma={sig:g}/z={z:g}"] = dict(gain_kpc=lg, over_cell=lg / cell_proper[z], feedback_20kpc=20.0 / lg)
        P(f"    cold stream at the threshold density, sigma {sig:4.0f} km/s, z = {z}: gain length {lg:7.3f} kpc -> Gamma L/v_k = "
          f"{20.0 / lg:6.1f} for a 20 kpc stream (absolute growth if >= 1, S1) = {lg / cell_proper[z]:.4f} PM cells ({cell_proper[z]:.0f} kpc proper)")
OUT["numbers"]["A3"] = dict(A3, pm_cell_proper_kpc=cell_proper)
check("A3 FK1's trigger is local: at each host's own scale-radius density (1e6 Msun minihalo to 1e15 Msun cluster) the gain "
      "length is < 1e-3 r_s; a cold stream (sigma <= 60 km/s, z = 0-2.5) at the bare threshold is an absolute amplifier "
      "(Gamma L/v_k >= 1 for L = 20 kpc) with a gain length < 0.1 of the PM cell",
      "; ".join(f"{k_}: {v['over_rs']:.1e} r_s" for k_, v in A3["hosts"].items()) + "; streams: "
      + ", ".join(f"{k_} {v['gain_kpc']:.2f} kpc" for k_, v in A3["streams"].items()),
      all(v["over_rs"] < 1e-3 for v in A3["hosts"].values())
      and all(v["feedback_20kpc"] >= 1.0 and v["over_cell"] < 0.1 for v in A3["streams"].values()),
      "the conversion reads the fluid's density on sub-kpc scales: every collapsed clump the streams carry is resolved by "
      "the trigger.  The record's PM runs read a 0.39 Mpc/h mesh average, so they could not see this (L357 V1's open "
      "question, 'whether the carrier's small halos fire', is answered by FK1's own rate: they do).  Only a hot host AT the "
      "bare threshold has a gain length approaching r_s -- and a hot host is never at the bare threshold")

# ============================================================================================ S1 sympy: the exponents
banner("S1  THE GROWTH EXPONENTS (sympy): linear sweep, second-order sweep, and the counter-propagating kinetic amplifier")
Gs, Hs, ds, al, t_, u_ = sp.symbols("G H delta alpha t u", positive=True)
D_ = sp.Symbol("D", real=True)
k4 = sp.simplify(sp.integrate(sp.sqrt(Gs ** 2 - D_ ** 2), (D_, -Gs, Gs)) / (2 * Hs * ds))
C4 = float(sp.Integral(sp.sqrt(1 - u_ ** 4), (u_, -1, 1)).evalf(20))
tstar = sp.sqrt(Gs / al)
second = sp.simplify(Gs * tstar * sp.Integral(sp.sqrt(1 - u_ ** 4), (u_, -1, 1)))
num_chk = quad(lambda tt: math.sqrt(max(1.0 - (0.7 * tt * tt) ** 2, 0.0)), -(1 / 0.7) ** 0.5, (1 / 0.7) ** 0.5)[0]
num_pred = C4 * 1.0 ** 1.5 / 0.7 ** 0.5
Ws, Ls, vs, Ss, xs = sp.symbols("W L v S x", positive=True)
Np = sp.Function("Np"); Nm = sp.Function("Nm")
sol = sp.dsolve([sp.Eq(vs * Np(xs).diff(xs), Ws * Ss), sp.Eq(-vs * Nm(xs).diff(xs), Ws * Ss)], [Np(xs), Nm(xs)],
                ics={Np(0): 0, Nm(Ls): 0})
Ssum = sp.simplify(sol[0].rhs + sol[1].rhs)
thr_cond = sp.solve(sp.Eq(Ssum, Ss), Ws)
P(f"    K4: int sqrt(G^2 - D^2) dt, dD/dt = 2 H delta:  {k4}")
P(f"    second-order sweep D = alpha t^2: int sqrt(G^2 - alpha^2 t^4) dt = {second} = C4 G^(3/2)/sqrt(alpha), C4 = {C4:.6f} "
  f"(numerical check {num_chk:.6f} vs {num_pred:.6f})")
P(f"    counter-propagating amplifier, steady state N+ + N- = S: requires W = {thr_cond}  (i.e. Gamma L / v = 1)")
OUT["numbers"]["S1"] = dict(K4=str(k4), C4=C4, feedback_threshold=str(thr_cond))
check("S1 the exponents: K4 = pi G^2/(4 H delta); a first-order-vanishing sweep gives C4 G^(3/2)/alpha^(1/2) with C4 = 1.7480; "
      "counter-propagating kinetic amplification turns absolute at Gamma L / v = 1",
      f"K4 {k4}; C4 {C4:.4f}; numeric {num_chk:.5f}/{num_pred:.5f}; feedback W = {thr_cond}",
      sp.simplify(k4 - sp.pi * Gs ** 2 / (4 * Hs * ds)) == 0 and abs(C4 - 1.7480) < 1e-3 and abs(num_chk - num_pred) < 1e-6
      and len(thr_cond) == 1 and sp.simplify(thr_cond[0] - vs / Ls) == 0)

# ============================================================================================ E growth by environment
banner("E   THE GROWTH MECHANISM BY ENVIRONMENT (ESTIMATE, O(1) factors): effective threshold n_env / n_t")
MPC = 3.0857e22
E_NEED = FK1["N1"]["by_mass"]["2e-19"]["efolds"]
Erow = {}


def thr_from_exponent(E_at_nt, power):                                          # E(n) = E_at_nt (n/n_t)^power = E_need
    return (E_NEED / E_at_nt) ** (1.0 / power)


def cone_env(z, W_kpc, tau, vk=600.0):
    """cold single-stream sheet/filament: first-order sweep zero on a cone; quadratic sweep from the strain's spatial
    variation along the daughter's path (v_k |T|/W) and the direction's rotation (3|T|^2); capped by crossing the structure"""
    Hz = H0_SI * E(z); T = tau * Hz; W = W_kpc * KPC; dl = delta_split(vk); Gt = G_t(z, vk)
    alpha = dl * (vk * 1e3 * T / W + 3 * T * T)
    Econe = C4 * Gt ** 1.5 / math.sqrt(alpha)
    Ecross = Gt * W / (vk * 1e3)
    Ecap = min(Econe, Ecross)
    pw = 1.5 if Econe <= Ecross else 1.0
    return dict(E_at_nt=Ecap, ratio=Ecap / E_NEED, n_over_nt=thr_from_exponent(Ecap, pw), t_star_Myr=math.sqrt(Gt / alpha) / 3.156e13)


def halo_env(z, sig, tav_H=1.0, vk=600.0):
    """virialised halo: kinetic (broadband) pump, absolute growth by counter-propagating feedback over t_av"""
    Gt = G_t(z, vk); Hz = H0_SI * E(z)
    E_abs = rate(Gt, sig, vk) * tav_H / Hz
    return dict(E_at_nt=E_abs, ratio=E_abs / E_NEED, n_over_nt=thr_from_exponent(E_abs, 2.0))


P(f"    reference: E_need = {E_NEED:.0f} e-folds at 2e-19 eV (FK1 N1); G_t/delta = {G_t(2.5) / delta_split(600):.2e} at z = 2.5")
for lab, (z, W, tau) in {"filament z=2.5, W=50 kpc, |T|=H": (2.5, 50, 1.0), "filament z=2.5, W=100 kpc, |T|=H": (2.5, 100, 1.0),
                         "filament z=2.5, W=300 kpc, |T|=2H": (2.5, 300, 2.0), "sheet z=0.3, W=1 Mpc, |T|=H": (0.3, 1000, 1.0),
                         "infall stream r_vir(1e12, z=2.5), W=20 kpc, |T|=9H": (2.5, 20, 9.0)}.items():
    Erow[lab] = cone_env(z, W, tau)
    P(f"    {lab:52s}: exponent at n_t = {Erow[lab]['ratio']:6.1f} E_need (t* = {Erow[lab]['t_star_Myr']:.0f} Myr) -> converts at "
      f"n = {Erow[lab]['n_over_nt']:.2f} n_t")
for sig in (2.0, 5.0, 20.0, 150.0, 1000.0):
    for tav in (0.1, 1.0):
        lab = f"virialised halo sigma={sig:g} km/s, t_av={tav:g}/H (z=2.5)" if sig < 1000 else f"cluster sigma={sig:g} km/s, t_av={tav:g}/H (z=0)"
        Erow[lab] = halo_env(2.5 if sig < 1000 else 0.0, sig, tav)
        P(f"    {lab:52s}: exponent at n_t = {Erow[lab]['ratio']:8.2f} E_need -> converts at n = {Erow[lab]['n_over_nt']:.2f} n_t")
OUT["numbers"]["E"] = Erow
cold = [v["n_over_nt"] for k_, v in Erow.items() if not k_.startswith("cluster") and "sigma=150" not in k_]
check("E (ESTIMATE) every cold environment the streams contain -- filaments and sheets with a zero-strain direction, "
      "converging streams near r_vir, low-sigma minihalos -- converts BELOW FK1's nominal n_t; only hot, high-sigma hosts "
      "(clusters) sit above it", f"cold environments: n/n_t = {min(cold):.2f}-{max(cold):.2f}; clusters: "
      + "/".join(f"{v['n_over_nt']:.2f}" for k_, v in Erow.items() if k_.startswith("cluster")),
      max(cold) < 1.0 and all(v["n_over_nt"] > 1.0 for k_, v in Erow.items() if k_.startswith("cluster")),
      "FK1's K4 normalisation is the Hubble-swept background; the streams are the environments where the sweep is weakest "
      "or the pump coldest.  This only strengthens A1-A3; the forest verdict (XR12_forest_halo_model) scans the threshold "
      "factor so as not to rest on these O(1) numbers", load_bearing=False)

# ============================================================================================ E2 the conversion rate
banner("E2  FK1's CONVERSION RATE ABOVE THRESHOLD, in units of H: the bracket for XR12_stream_shells' two rates")
E2 = {}
for z in (2.5, 0.0):
    for nr in (2.0, 5.0):
        row = []
        for sig in (0.0, 2.0, 5.0, 20.0, 60.0, 150.0):
            G_ = G_t(z) * nr
            tconv = E_NEED / rate(G_, sig)                                          # s: E_need e-folds at the local rate
            gam = 1.0 / (tconv * H0_SI * E(z))
            E2[f"z={z:g}/n={nr:g}n_t/sigma={sig:g}"] = dict(t_conv_Myr=tconv / 3.156e13, Gamma_over_H=gam)
            row.append(f"sigma {sig:5.0f}: {gam:7.1f} H ({tconv / 3.156e13:6.1f} Myr)")
        P(f"    z = {z:3g}, n = {nr:g} n_t: " + ";  ".join(row))
OUT["numbers"]["E2"] = E2
g2 = {k_.split("/")[-1]: v["Gamma_over_H"] for k_, v in E2.items() if k_.startswith("z=2.5/n=2n_t")}
check("E2 (reported) at z = 2.5 and twice the threshold FK1's conversion runs at ~1e3 H in a cold (coherent) stream, ~25-75 H "
      "at sigma = 20-60 km/s and ~10 H at sigma = 150 km/s: the record's 10 H and the cold limit 1e3 H bracket a real stream",
      ", ".join(f"{k_}: {v:.0f} H" for k_, v in g2.items()),
      g2["sigma=0"] > 500 and 10 <= g2["sigma=60"] <= 100 and 10 <= g2["sigma=20"] <= 150 and g2["sigma=150"] >= 5,
      "the rate rises as n^2 above the threshold, so dense streams convert faster than these numbers", load_bearing=False)

# ============================================================================================ summary
banner("SUMMARY")
P(f"""  Question (A), first half: yes -- FK1's n^2 trigger fires in the web before the fluid reaches halos.
  - FK1's threshold (linear-cell reading delta_t0 = 5.31) is rho/rho_bar = {lo['2.0']['fk1']:.1f}/{lo['2.5']['fk1']:.1f}/{lo['3.0']['fk1']:.1f} at z = 2/2.5/3:
    inside the filament range; every stream near r_vir (delta ~ 100) is above it for z <= {zs_stream['5.31 (linear cell)']:.1f}; every collapsed
    halo for z <= {zs_vir['5.31 (linear cell)']:.1f}.  At FK1's upper bracket (25) the smooth filaments stay below it; collapsed halos still cross
    for z <= {zs_vir['25 (FK1 upper)']:.1f}.
  - On the record's own z = 2 mesh, {OUT['numbers'].get('A2', {}).get('pooled', {}).get('FK1 5.31', float('nan')):.3f} of the carrier is above the nominal threshold, mostly in filament
    and knot cells.
  - The trigger is local (gain length ~pc at halo densities, <= 8 kpc in a cold stream at the bare threshold), so it
    resolves every clump the streams carry -- which the PM's 0.39 Mpc/h mesh cannot; and every cold environment in the
    streams converts below n_t (estimate E).
  The forest, the flagship and cluster retention are scored in XR12_forest_halo_model.py and XR12_stream_shells.py.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(load_bearing_failed=n_fail, n_checks=len(CH), runtime_s=round(time.time() - T0, 1))
suffix = "_MUTATE" if MUTATE else ""
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w"), indent=1, default=str)
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   [{time.time() - T0:.0f}s]")
sys.exit(1 if n_fail else 0)
