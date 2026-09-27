#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
MS3 -- COSMIC SHEAR ON THE MOND-SECTOR DOOR, RESOLUTION-FREE: why the record's mock cannot score it, where the region
kernel's lensing power actually comes from, and the one design target that passes.

WHY.  A construction passes cosmic shear iff the lensing power -- carrier + baryons + the MOND phantom its regions carry
-- stays within 20% of LCDM's P_NL at k = 0.1-1 h/Mpc (GP3's gate, R <= 1.2).  Every "shear ok" since L364 (L364,
L367, DE2/DE3/DE5, L388, AT3) scores the phantom on GP3's 100 Mpc mock.  L363 itself called its halo model "the
resolution-free, converged estimate" and found it FAILS (worst R 2.9-9.2), and L364 moved to the mock because groups
there share a collective field.  This lane asks, on the MOND-sector door (MS1/MS2): can the mock score phantom-supported
regions at all, and what does the resolution-free estimate say?

WHAT IS COMPUTED (L363's machinery -- region_phantom, the halo model's per-halo compensated phantom transform, GP3's
Sheth-Tormen + NFW P_NL, GP0's bound baryons -- loaded unedited; the lane adds a size cap on each region and the door's
edge reading):
  U1  the mock's region builder, started from ONE isolated seed cell (the way the mock deposits a galaxy's bound baryons),
      on L364's cell size (0.39 Mpc), at the linear cell's lens-epoch threshold, for the halo model's bound baryons of
      1e12, 1e13 and 1e14 Msun halos: how far does the region grow, against the analytic phantom edge?
  M1  L364's mock (seed 20260926): how many cluster-mass systems it holds, against the halo model's expectation.
  D1  the halo model at the linear cell (p = 1, x_c0 = 2.5; x(0.5) = 4.363), both footings: the phantom's power at
      k = 1 split by halo mass.
  X1  the door in the halo model: beyond r200 the door's edge is where the phantom alone reaches the gate (a host in the
      mean density: the ambient baryons cancel the door's baryonic background); L363's upper convention subtracts the
      full matter background (a host in vacuum).  Worst R over k = 0.1-1 for the carrier intact, cleared below 1e13,
      cleared below 1e14, and with L388's own retention by mass (v_k = 600 km/s, fixed-cell galaxy clearing 0.07).
  K1  THE DESIGN TARGET: every region's radius capped at r_cap (physical, z = 0.5); the largest cap that passes on both
      footings with L388's retention (reported beside it: the same caps with the carrier intact and with only galaxies
      cleared); its velocity form v_cap = r_cap H(0.5) sqrt(x) (the door's edge law beyond r200) and
      baryonic-mass form M_cap = v_cap^4/(G a0); against the KiDS lenses' own edges at z = 0.25 (DE1's law, M_b up to
      3e11 Msun).
CHECKS
  C1 CONTROL: with no cap, this lane's halo model reproduces L363's committed R(k) at its own cells (observed baryons,
     p = 1 x_c0 = 1.5 and p = 2 x_c0 = 2, canonical and alt) to 1e-6.
  U1 THE MOCK CANNOT SCORE THE DOOR: from an isolated seed cell the builder stops short of half the analytic edge for all
     three masses (it needs a surrounding matter-contrast region to grow: the one-cell Dirichlet phantom vanishes).
  X1 THE RECORD'S MOCK-BASED PASS DOES NOT SURVIVE THE RESOLUTION-FREE ESTIMATE: at the linear cell, with no cap, worst
     R > 1.2 on both footings for every carrier scenario, on both edge conventions.
  K1 A CAP PASSES: there is a cap at which worst R <= 1.2 on both footings with L388's retention, and at a fixed velocity
     scale it sits above every KiDS lens's own region.
MUTATE=1 removes the cap (r_cap -> infinity everywhere): K1 must FAIL (rc = 1).

SCOPE.  L363's halo model: isolated regions per halo (no collective field between neighbours -- it over-counts phantoms
in crowded places; the mock under-counts them, U1/M1), one lens epoch (z = 0.5), P(k) not xi_+-, the observed bound
baryons (GP0), L388's retention read from its M(<1 Mpc/h) bins as a function of halo mass.  The cap is a design target,
not a mechanism: no action term that produces it is proposed here.  A first version of this lane scored the door on the
mock itself and returned T_max(k = 1) ~ 1.06; U1 shows why that number is not physics, and it is withdrawn.

Run from the repository root:  python3 real_research/mond_sector_gate_2026/MS3_cosmic_shear_bound_mond_sector.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
from scipy import ndimage
from scipy.special import spherical_jn
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "MS3_cosmic_shear_bound_mond_sector"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "MS3", "mutate": MUTATE, "checks": {}, "numbers": {}}
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
KG = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: no cap on any region; K1 must FAIL ***")

# ---------------------------------------------------------------------------------- L363's machinery, loaded unedited
P63 = os.path.join(REPO, "real_research", "g03_audit_2026", "L363_region_kernel_lensing_power.py")
N = {"__name__": "l363", "__file__": P63}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P63).read().split("# ============================================================================================ C1 control")[0]
         .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), N)
GP0, KC, RHO, PNL, PLIN, h, ZS, aS = N["GP0"], N["KC"], N["RHO"], N["PNL"], N["PLIN_HM"], N["h"], N["ZS"], N["aS"]
G, MS, MPC, nu_mono, Omz, E2, I1, nfw_uk = N["G"], N["MS"], N["MPC"], N["nu_mono"], N["Omz"], N["E2"], N["I1"], N["nfw_uk"]
FB = float(GP0.FB)
L363R = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L363_region_kernel_lensing_power_results.json")))["numbers"]
L388R = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L388_linear_gate_pooled_results.json")))["numbers"]
dn, bh, _ = GP0.mass_function(ZS)
LMH = np.arange(10.0, 15.51, 0.05); dlnM = 0.05 * math.log(10)
XLIN = 2.5 * E2
rho_bar_phys = RHO / aS ** 3; rho_c_phys = GP0.RHO_CRIT0 * E2
H05 = math.sqrt(8 * math.pi * G * rho_c_phys * MS / MPC ** 3 / 3) * MPC / 1e3          # km/s/Mpc at z = 0.5
P(f"  L363 loaded: z = {ZS}, E^2 = {E2:.6f}, x_lin = {XLIN:.6f}, f_b = {FB:.4f}, H(0.5) = {H05:.2f} km/s/Mpc   [{time.time() - T0:.0f}s]")

# ---------------------------------------------------------------------------------- L388's retention by halo mass (v_k = 600)
rb = L388R["retention_by_mass"]["v600"]
cen = {"6.0e+13-1.0e+14": 7.75e13, "1.0e+14-1.5e+14": 1.22e14, "1.5e+14-2.5e+14": 1.94e14, "2.5e+14-1.0e+17": 5.0e14}
lx = [math.log10(1e13)] + [math.log10(cen[k_]) for k_ in cen]
ly = [float(L388R["table"]["pooled"]["v600"]["clear_fixed"])] + [rb[k_][0] for k_ in cen]
ret_L388 = lambda M: float(np.interp(math.log10(M), lx, ly, left=ly[0], right=ly[-1]))
P("  L388 retention (v_k = 600, pooled; galaxies at its fixed-cell clearing): " + ", ".join(f"1e{a:.2f}: {b:.3f}" for a, b in zip(lx, ly)))


def transform(M, Mb, xc, a0, rcap, conv):
    """L363's halo_phantom_transform with a size cap (physical Mpc) and an edge convention: 'upper' (L363: the host in
    vacuum, background 1) or 'door' (the host in the mean density: the phantom alone must reach the gate beyond r200)."""
    c = 10 ** (0.905 - 0.101 * math.log10(M / (1e12 / h))) * (1 + ZS) ** -0.5
    r200 = (3 * M / (4 * math.pi * 200 * rho_c_phys)) ** (1 / 3); rs = r200 / c; mc = math.log(1 + c) - c / (1 + c)
    r = np.geomspace(1e-3 * r200, 30.0, 4000)
    y = G * Mb * MS / (r * MPC) ** 2 / a0
    Mph = (nu_mono(y) - 1) * Mb
    rho_ph = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
    rho_h = np.where(r < r200, M / (4 * math.pi * rs ** 3 * mc) / ((r / rs) * (1 + r / rs) ** 2), 0.0)
    if conv == "upper":
        x = 1.5 * Omz * ((rho_h + np.maximum(rho_ph, 0)) / rho_bar_phys - 1)
    else:                                                                 # the door: baryons (f_b of the host) + phantom
        x = 1.5 * Omz * ((FB * rho_h + np.maximum(rho_ph, 0)) / rho_bar_phys)
    above = np.where(x >= xc)[0]
    re = float(r[above.max()]) if above.size else float(r[0])
    re = min(re, rcap)
    sel = r <= re; rc = r[sel] / aS; kr = np.outer(KC, rc)
    return np.trapz(Mph[sel][None, :] * KC[:, None] * spherical_jn(1, kr), rc, axis=1), re


def R_of(xc, a0, rcap=math.inf, conv="upper", ret=None, bands=None):
    """lensing power / P_NL; ret(M) = the carrier's retained fraction in a halo (None = intact)."""
    P1 = np.zeros_like(KC); X1 = np.zeros_like(KC); B = np.zeros_like(KC); rm = np.zeros_like(KC)
    P1b = {b: np.zeros_like(KC) for b in (bands or [])}
    for lm in LMH:
        M = 10 ** lm; n = float(np.interp(lm, GP0.LM, dn)); b = float(np.interp(lm, GP0.LM, bh))
        Mb = float(GP0.M_bound(M, ZS, "observed")); tr, re = transform(M, Mb, xc, a0, rcap, conv); uk = nfw_uk(M, KC)
        P1 += n * tr ** 2 * dlnM / RHO ** 2; B += n * b * tr * dlnM / RHO
        for bb in P1b:
            if bb[0] <= lm < bb[1]: P1b[bb] += n * tr ** 2 * dlnM / RHO ** 2
        if ret is None:
            X1 += n * M * uk * tr * dlnM / RHO ** 2                       # L363's own cross term, the carrier intact
        else:
            fr = ret(M); fd = 1 - FB
            mass_1h = (FB + fd * fr) * M                                  # baryons kept, carrier retained at fr
            rm += n * ((M * uk) ** 2 - (mass_1h * uk) ** 2) * dlnM / RHO ** 2
            X1 += n * mass_1h * uk * tr * dlnM / RHO ** 2
    Pph = P1 + B ** 2 * PLIN; Pxm = X1 + I1 * B * PLIN
    R = (PNL - rm + 2 * Pxm + Pph) / PNL
    at = lambda arr, q: float(np.interp(math.log(q * h), np.log(KC), arr))
    out = {q: at(R, q) for q in KG}
    s2 = {q: at(Pph / PNL, q) for q in KG}
    bandv = {f"{bb[0]}-{bb[1]}": at(v_ / PNL, 1.0) for bb, v_ in P1b.items()}
    return out, s2, bandv


cut = lambda Mc: (lambda M: 0.0 if M < Mc else 1.0)
SCEN = {"intact": None, "cleared<1e13": cut(1e13), "cleared<1e14": cut(1e14), "L388 retention": ret_L388}

# ============================================================================================ C1 control
banner("C1  CONTROL: with no cap the lane's halo model reproduces L363's committed R(k)")
d1 = 0.0
for cell, xc in (("p=1, x_c0=1.5 (L360's example)", 1.5 * E2), ("p=2, x_c0=2.0 (highest window threshold)", 2.0 * E2 ** 2)):
    for foot in A0:
        R, _, _ = R_of(xc, A0[foot])
        ref = L363R["halo_model"][f"observed/{cell}/{foot}"]
        d1 = max(d1, max(abs(R[q] - ref[str(q)]) for q in KG))
check("C1 CONTROL: no cap, observed baryons: L363's committed halo-model R(k) reproduced at its two cells, both footings",
      f"max |diff| = {d1:.1e}", d1 < 1e-6, load_bearing=False)

# ============================================================================================ U1 the mock's builder
banner("U1  CAN THE MOCK SCORE THE DOOR? L363's region builder from one isolated seed cell (L364's cell size)")
Nn = 96; dx = 100.0 / 256; U1 = {}
for lM in (12.0, 13.0, 14.0):
    Mb = float(GP0.M_bound(10 ** lM, ZS, "observed"))
    rhoB = np.zeros((Nn, Nn, Nn)); c0 = Nn // 2; rhoB[c0, c0, c0] = Mb / dx ** 3
    mk = {"dx": dx, "rho_m": np.full((Nn, Nn, Nn), RHO), "rhoB": rhoB}
    read = rhoB + FB * mk["rho_m"]
    mask = (1.5 * Omz * (read / RHO - FB) >= XLIN) | (rhoB > 0)
    st = ndimage.generate_binary_structure(3, 1)
    for it in range(40):
        dil = ndimage.binary_dilation(mask, structure=st)
        rp, _, _, _ = N["region_phantom"](mk, dil, rhoB, A0["canonical"], True)
        new = (1.5 * Omz * ((read + np.maximum(np.where(dil, rp, 0.0), 0.0)) / RHO - FB) >= XLIN) & dil
        grew = int((new & ~mask).sum()); mask = mask | new
        if grew < 1e-4 * mask.sum(): break
    R_grid = (3 * mask.sum() * dx ** 3 / (4 * math.pi)) ** (1 / 3)
    _, re_phys = transform(10 ** lM, Mb, XLIN, A0["canonical"], math.inf, "door")
    U1[lM] = dict(M_bound=Mb, cells=int(mask.sum()), R_grid_Mpc=R_grid, R_edge_Mpc=re_phys / aS, iterations=it + 1)
    P(f"    halo 1e{lM:.0f} (bound baryons {Mb:.2e}): region {int(mask.sum())} cell(s), radius {R_grid:.2f} Mpc comoving after "
      f"{it + 1} iteration(s); the door's analytic edge {re_phys / aS:.2f} Mpc comoving ({re_phys / aS / dx:.1f} cells)")
OUT["numbers"]["U1"] = {str(k_): v_ for k_, v_ in U1.items()}
check("U1 THE MOCK CANNOT SCORE THE DOOR: from an isolated seed cell L363's builder stops short of half the analytic phantom "
      "edge for 1e12, 1e13 and 1e14 Msun hosts -- a region grows only where a matter-contrast region already surrounds it",
      "; ".join(f"1e{k_:.0f}: {v_['R_grid_Mpc']:.2f} vs {v_['R_edge_Mpc']:.2f} Mpc" for k_, v_ in U1.items()),
      all(v_["R_grid_Mpc"] < 0.5 * v_["R_edge_Mpc"] for v_ in U1.values()),
      "the one-cell Dirichlet phantom vanishes (centred gradients see the zero boundary), so phantom-supported regions -- "
      "the door's, and every isolated galaxy's on the record's branches -- are absent from the mock")

# ============================================================================================ M1 clusters in the mock
banner("M1  THE MOCK'S CLUSTERS: L364's 100 Mpc box against the halo model's expectation")
MK = N["build_mock"](100.0, 256, 20260926)
Vc = MK["dx"] ** 3; Vbox = 100.0 ** 3
M1 = {}
for lM in (13.5, 14.0, 14.5):
    thr = float(GP0.M_bound(10 ** lM, ZS, "observed"))
    ncells = int((MK["rhoB"] * Vc >= thr).sum())
    sel = LMH >= lM
    nexp = float(np.trapz(np.interp(LMH[sel], GP0.LM, dn), LMH[sel] * math.log(10))) * Vbox
    M1[lM] = dict(cells_with_bound_baryons_above=ncells, expected_halos_above=nexp)
    P(f"    cells holding bound baryons >= those of a 1e{lM} halo: {ncells}; halo-model expectation for halos >= 1e{lM} in the box: {nexp:.1f}")
del MK
OUT["numbers"]["M1"] = {str(k_): v_ for k_, v_ in M1.items()}

# ============================================================================================ D1 decomposition
banner("D1  WHERE THE PHANTOM'S POWER AT k = 1 COMES FROM (halo model, linear cell, no cap, upper convention)")
BANDS = [(10.0, 12.0), (12.0, 13.0), (13.0, 14.0), (14.0, 15.6)]
D1 = {}
for foot in A0:
    R, s2, bandv = R_of(XLIN, A0[foot], bands=BANDS)
    D1[foot] = dict(s2_k1=s2[1.0], bands=bandv)
    P(f"    {foot:9s}: phantom power s^2(k = 1) = {s2[1.0]:.3f}; one-halo share by log M: "
      + ", ".join(f"[{k_}] {v_:.4f}" for k_, v_ in bandv.items()))
OUT["numbers"]["D1"] = D1
clus = min(D1[f]["bands"]["14.0-15.6"] / max(D1[f]["s2_k1"], 1e-30) for f in A0)
gal = max(D1[f]["bands"]["10.0-12.0"] + D1[f]["bands"]["12.0-13.0"] for f in A0)
check("D1 (reported) clusters (>= 1e14 Msun) carry most of the phantom's power at k = 1; galaxies below 1e13 almost none",
      f"cluster share of s^2(1) >= {clus:.2f} on both footings; halos below 1e13 give <= {gal:.4f} of P_NL", True,
      load_bearing=False)

# ============================================================================================ X1 no cap: the verdict at the linear cell
banner("X1  THE LINEAR CELL WITH NO CAP: every carrier scenario, both edge conventions, both footings")
X1 = {}
for conv in ("upper", "door"):
    for sname, ret in SCEN.items():
        for foot in A0:
            R, s2, _ = R_of(XLIN, A0[foot], math.inf, conv, ret)
            X1[f"{conv}/{sname}/{foot}"] = dict(worst=max(R.values()), R=R, s2_k1=s2[1.0])
        P(f"    {conv:5s} {sname:15s}: worst R canonical {X1[f'{conv}/{sname}/canonical']['worst']:.2f}, alt {X1[f'{conv}/{sname}/alt']['worst']:.2f}")
OUT["numbers"]["X1"] = X1
check("X1 THE RECORD'S MOCK-BASED PASS DOES NOT SURVIVE THE RESOLUTION-FREE ESTIMATE: at the linear cell with no cap, "
      "worst R > 1.2 for every carrier scenario, both edge conventions and both footings",
      f"min worst R = {min(v_['worst'] for v_ in X1.values()):.2f}", min(v_["worst"] for v_ in X1.values()) > 1.2,
      "DE3/DE5's bound, and L388's 'shear ok', rest on a 100 Mpc mock that holds too few clusters (M1) and cannot grow "
      "phantom-supported regions (U1); on L363's own converged estimate the region kernel's cluster phantoms fail cosmic shear")

# ============================================================================================ K1 the cap
banner("K1  THE DESIGN TARGET: cap every region at r_cap (physical, z = 0.5); L388's retention; the door's edges")
CAPS = [math.inf] if MUTATE else [3.0, 2.0, 1.75, 1.5, 1.35, 1.2, 1.0]
K1 = {}
for rc_ in CAPS:
    row = {}
    for foot in A0:
        R, s2, _ = R_of(XLIN, A0[foot], rc_, "door", ret_L388)
        row[foot] = dict(worst=max(R.values()), R1=R[1.0], R05=R[0.5], s2_k1=s2[1.0])
    for sname in ("intact", "cleared<1e13"):                            # the cap alone, without the PM's group/cluster clearing
        row[sname] = {f: max(R_of(XLIN, A0[f], rc_, "door", SCEN[sname])[0].values()) for f in A0}
    K1[rc_] = row
    P(f"    r_cap {rc_:5.2f} Mpc: worst R canonical {row['canonical']['worst']:.3f}, alt {row['alt']['worst']:.3f}  "
      f"(s^2(1) {row['canonical']['s2_k1']:.3f}/{row['alt']['s2_k1']:.3f});  same cap, carrier intact {row['intact']['canonical']:.2f}/"
      f"{row['intact']['alt']:.2f}, galaxies only cleared {row['cleared<1e13']['canonical']:.2f}/{row['cleared<1e13']['alt']:.2f}")
passing = [rc_ for rc_, row in K1.items() if all(row[f]["worst"] <= 1.2 for f in A0)]
cap_alone = [rc_ for rc_, row in K1.items() if all(row["intact"][f] <= 1.2 for f in A0)]
P(f"    caps that pass with the carrier INTACT (the cap alone): {cap_alone if cap_alone else 'none'} -- the PM's group/cluster "
  f"clearing (L388's retention) is needed as well")
rbest = max(passing) if passing else None
a0c = A0["canonical"]
vcap = (rbest * H05 * math.sqrt(XLIN)) if (rbest is not None and math.isfinite(rbest)) else None
Mcap = ((vcap * 1e3) ** 4 / (G * a0c) / MS) if vcap else None
# KiDS lenses' own edges at z = 0.25 (DE1's law: host in vacuum, the record's KiDS convention; and host in the mean)
E2k = GP0.Om * 1.25 ** 3 + GP0.OL; Omk = GP0.Om * 1.25 ** 3 / E2k
Hk = H05 * math.sqrt(E2k / E2); xk = 2.5 * E2k
kids = {}
for Mb in (3e10, 1e11, 3e11):
    vf = (G * Mb * MS * a0c) ** 0.25 / 1e3
    kids[f"{Mb:.0e}"] = dict(v_f=vf, r_e_vacuum=vf / (Hk * math.sqrt(xk + 1.5 * Omk)), r_e_mean=vf / (Hk * math.sqrt(xk)))
rcap_k = (vcap / (Hk * math.sqrt(xk))) if vcap else None
P(f"    largest passing cap (both footings): {rbest} Mpc at z = 0.5" + (f"  ->  v_cap = {vcap:.0f} km/s, M_b,cap = {Mcap:.2e} Msun; "
  f"the same v_cap caps regions at {rcap_k:.2f} Mpc at z = 0.25" if vcap else ""))
for k_, v_ in kids.items():
    P(f"    KiDS lens M_b = {k_}: v_f {v_['v_f']:.0f} km/s, own edge at z = 0.25 {v_['r_e_vacuum']:.2f} Mpc (host in vacuum, the record's "
      f"KiDS convention) / {v_['r_e_mean']:.2f} Mpc (host in the mean)")
OUT["numbers"]["K1"] = {str(k_): v_ for k_, v_ in K1.items()}
OUT["numbers"]["K1_design"] = dict(r_cap_z05=rbest, v_cap=vcap, M_b_cap=Mcap, r_cap_z025=rcap_k, kids_edges=kids,
                                   caps_passing_with_carrier_intact=cap_alone)
kids_ok = bool(vcap) and all(v_["v_f"] <= vcap for v_ in kids.values())
check("K1 A CAP PASSES: some region-size cap passes cosmic shear on both footings with L388's retention, and at a fixed "
      "velocity scale it sits above every KiDS lens's own region (M_b <= 3e11 Msun, v_f <= v_cap), so KiDS is untouched",
      f"largest passing cap {rbest} Mpc (z = 0.5), v_cap {None if vcap is None else round(vcap)} km/s; KiDS lenses v_f "
      + ", ".join(f"{v_['v_f']:.0f}" for v_ in kids.values()) + " km/s", bool(passing) and kids_ok,
      "cosmic shear is a group-and-cluster phantom problem: regions must stop growing near the largest galaxies' scale")

# ============================================================================================ summary
banner("SUMMARY")
P(f"""  The mock cannot score phantom-supported regions (U1) and holds too few clusters (M1), so the record's mock-based
  cosmic-shear passes are not evidence.  On L363's resolution-free halo model the region kernel's lensing power at k = 1 is
  dominated by groups and clusters (D1), and at the linear cell it fails cosmic shear for every carrier history, on either
  edge convention (X1).  It passes once every region stops growing at ~{rbest} Mpc at z = 0.5 -- a velocity scale
  v_cap ~ {None if vcap is None else round(vcap)} km/s, i.e. baryonic masses above ~{None if Mcap is None else f'{Mcap:.1e}'} Msun -- with L388's retention (K1);
  the cap alone, with the carrier intact, passes at {cap_alone if cap_alone else 'no cap tested'}: the density trigger's group/cluster clearing is needed too.
  Every KiDS lens (v_f <= {max(v_['v_f'] for v_ in kids.values()):.0f} km/s) keeps its own region, so the KiDS-shear pincer is a galaxy-versus-cluster
  separation, not a single scale.  What produces the cap is the open piece.""")

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail; OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
