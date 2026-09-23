#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L321 -- THE LAMBDA-TRIGGERED CARRIER AT z = 0: galaxy and cluster retention, the two gates L319 left open.

L319's carrier (Gamma ~ Omega_Lambda(a)^2, f_d(0) = 0.8) passes the forest and S_8; L320 prices it at ~3 sigma on RC100.
The z = 0 gates were assumed (full escape), not computed.  This lane computes them, in the FRAMEWORK's own gravity:

  TWO COUPLINGS, both run (verify a deficit as hard as a win):
    UNIVERSAL  the carrier sources the MOND field:  g = nu(|g_N,b + g_N,c|/a0) (g_N,b + g_N,c)
    ADDITIVE   a metric-coupled carrier (L289) that does not source it:  g = nu(g_N,b/a0) g_N,b + g_N,c
  (the record's cluster number 0.576 is "source REQUIRED beyond the kernel" (L163/L172): the additive reading.)
  GALAXY GATE (one physical criterion for every host, h_kids's): the retained carrier must not raise the framework's
  predicted g_obs at r_gate by more than the RAR's 0.06 dex orthogonal scatter.  Hosts: dwarf (M_b 5e8, M200 3e10, 3 kpc),
  SPARC disc (1.2e10, 3e11, 7.5 kpc), Milky Way (6e10, 1e12, 30 kpc).
  CLUSTER GATE on the REAL X-COP sample (real_research/data/xcop: hydrostatic mass, gas, stars, R500): the predicted
  dynamical mass at R500 (baryons + the retained carrier, under each coupling) against M_HSE, median within 20%.
  The carrier's pre-decay halo in a cluster = (1 - f_b) x the cluster's own NFW fit (the LCDM-like cold halo).
  eps = the retained carrier mass inside r_gate, RELATIVE to a no-decay control with identical random draws (this cancels
  the local-Maxwellian sampling bias, ~15%, that a first version exposed).

  METHOD.  Carrier halo = NFW(M200, c) with Dutton-Maccio c(M); baryons Hernquist (galaxies) or a beta-model gas (cluster).
  Gravity is the framework's: g = nu(|g_N|_eff/a0) g_N with nu_RAR and a magnitude-based external field
  |g_N|_eff = sqrt(g_N^2 + g_e^2) (the record's direction-blind EFE rule, SW01), g_e = 0.02 a0 (galaxies), 0.01 a0 (cluster).
  Pre-decay: isotropic Jeans dispersion in the full potential (baryons + carrier).  At decay each daughter gets an isotropic
  kick v_k; a fraction 1 - f_d stays as undecayed parents (no kick).  Post-decay potential: baryons + parents + the retained
  daughters (iterated to self-consistency, 3 passes).  Unbound particles leave; bound ones are PHASE-MIXED on their new orbits
  in the static spherical post-decay potential, so the time-averaged mass inside r_gate is exact given (E, L):
      frac_in = int_{r_p}^{min(r_a, r_gate)} dr/v_r / int_{r_p}^{r_a} dr/v_r,   r = r_m - D cos(phi) removes the turning points.
  S_8 at v_k = 1500, 2000 km/s from L319's validated solver (same cell p = 2, f_d(0) = 0.8), completing the S_8(v_k) curve.
  CONTROL C1: the no-decay control's phase-mixed mass inside r_gate is within 25% of the NFW input (the size of the
  Maxwellian bias that the ratio removes -- reported, so the reader sees it).
  CONTROL C2: under the ADDITIVE reading, the X-COP clusters' required carrier fraction reproduces the record's 0.576 within
  25% (independent route to the record's number); the universal reading's required fraction is reported beside it.
  MUTATE=1 sets v_k = 0 (decay without a kick): the galaxy-depletion finding must FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L321_carrier_z0_retention_gate.py
"""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*encountered in matmul")

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L321_carrier_z0_retention_gate"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L321", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__)

from astropy.io import fits

Gk = 4.30091727e-6                     # kpc (km/s)^2 / Msun
KPC_M = 3.0856775814913673e19
A0 = 9.3619e-11 * KPC_M / 1e6          # (km/s)^2 / kpc  (canonical footing)
h = 0.6736
RHO_C0 = 2.775e11 * h ** 2 / 1e9       # Msun / kpc^3 at z = 0
REPO = os.path.dirname(os.path.dirname(HERE))
FB = 0.16                              # cosmic baryon fraction (the carrier = (1 - f_b) of an LCDM-like halo)
RG = np.geomspace(1e-3, 1e5, 4000)     # kpc
COUPLINGS = ("universal", "additive")


def nu(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.clip(y, 1e-12, None))))


def gravity(gb, gc, ge, coupling):
    """framework gravity from baryonic and carrier Newtonian fields, magnitude-based EFE (SW01 rule)."""
    if coupling == "universal":
        gN = gb + gc
        return nu(np.sqrt(gN ** 2 + (ge * A0) ** 2) / A0) * gN
    return nu(np.sqrt(gb ** 2 + (ge * A0) ** 2) / A0) * gb + gc


def c200_dm14(M200):
    return 10 ** (0.905 - 0.101 * math.log10(M200 / (1e12 / h)))


def nfw(M200, c, rhoc=RHO_C0):
    r200 = (3 * M200 / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = r200 / c
    m = lambda x: np.log(1 + x) - x / (1 + x)
    return (lambda r: M200 * m(np.asarray(r, dtype=float) / rs) / m(c)), r200, rs


def hernquist(Mb, a):
    return lambda r: Mb * np.asarray(r, dtype=float) ** 2 / (np.asarray(r, dtype=float) + a) ** 2


def potential(Mb_fn, Mc_fn, ge, coupling):
    gb = Gk * Mb_fn(RG) / RG ** 2; gc = Gk * Mc_fn(RG) / RG ** 2
    g = gravity(gb, gc, ge, coupling)
    tail = g[-1] * RG[-1]
    seg = 0.5 * (g[1:] + g[:-1]) * np.diff(RG)
    Phi = -(np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) + tail)
    return g, Phi


def frac_inside(E, L, Phi, r_gate, K=48):
    out = np.zeros(len(E)); bound = E < 0
    if not bound.any():
        return out
    Eb, Lb = E[bound], L[bound]
    vr2 = 2 * (Eb[:, None] - Phi[None, :]) - (Lb[:, None] / RG[None, :]) ** 2
    pos = vr2 > 0; has = pos.any(axis=1)
    ip = np.argmax(pos, axis=1); ia = len(RG) - 1 - np.argmax(pos[:, ::-1], axis=1)
    rp = RG[np.maximum(ip - 1, 0)]; ra = RG[np.minimum(ia + 1, len(RG) - 1)]
    phi = (np.arange(K) + 0.5) * np.pi / K
    rm, D = 0.5 * (ra + rp), 0.5 * (ra - rp)
    rr = rm[:, None] - D[:, None] * np.cos(phi)[None, :]
    v2 = 2 * (Eb[:, None] - np.interp(rr, RG, Phi)) - (Lb[:, None] / rr) ** 2
    wgt = D[:, None] * np.sin(phi)[None, :] / np.sqrt(np.maximum(v2, 1e-12 * np.abs(Eb[:, None]) + 1e-30))
    fin = (wgt * (rr < r_gate)).sum(1) / wgt.sum(1)
    fin[~has] = 0.0
    out[bound] = fin
    return out


def retained(Mb_fn, M200, c, r_gate, ge, coupling, vk, fd, N=12000, seed=5, iters=2, rhoc=RHO_C0):
    """retained carrier mass inside r_gate after decay, RELATIVE to the no-decay control (identical random draws)."""
    Mn, r200, rs = nfw(M200, c, rhoc)
    Mc0 = lambda x: (1 - FB) * Mn(np.minimum(x, r200))
    rng = np.random.default_rng(seed)
    u = rng.random(N) * float(Mc0(r200)); rgrid = np.geomspace(1e-3 * rs, r200, 5000)
    r = np.interp(u, Mc0(rgrid), rgrid); w = float(Mc0(r200)) / N
    g_pre, _ = potential(Mb_fn, Mc0, ge, coupling)
    rho = np.where(RG < r200, 1.0 / ((RG / rs) * (1 + RG / rs) ** 2), 1e-300)
    integ = rho * g_pre; seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(RG)
    sig2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / np.maximum(rho, 1e-300)
    sig = np.sqrt(np.interp(r, RG, sig2))
    v = rng.normal(0, 1, (N, 3)) * sig[:, None]
    is_d = rng.random(N) < fd
    nh = rng.normal(0, 1, (N, 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]

    def mass_in(kick, fdx):
        vv = v + ((is_d if fdx > 0 else np.zeros(N, bool)) * kick)[:, None] * nh
        vrad, vtan = vv[:, 0], np.linalg.norm(vv[:, 1:], axis=1); L = r * vtan
        Mc = Mc0
        for _ in range(iters):
            _, Phi = potential(Mb_fn, Mc, ge, coupling)
            E = 0.5 * (vrad ** 2 + vtan ** 2) + np.interp(r, RG, Phi)
            probe = np.geomspace(0.02 * rs, 3 * r200, 24)
            prof = np.array([w * frac_inside(E, L, Phi, rg).sum() for rg in probe])
            Mc = (lambda pr=probe, pm=prof: (lambda x: np.interp(np.asarray(x, dtype=float), pr, pm, left=0.0)))()
        _, Phi = potential(Mb_fn, Mc, ge, coupling)
        E = 0.5 * (vrad ** 2 + vtan ** 2) + np.interp(r, RG, Phi)
        return w * frac_inside(E, L, Phi, r_gate).sum()

    m_ctrl = mass_in(0.0, 0.0)
    m_dec = mass_in(vk, fd)
    return m_dec / m_ctrl, m_ctrl / float(Mc0(r_gate))


# ------------------------------------------------------------------------------------------------ galaxies
GAL = {"dwarf": dict(Mb=5e8, M200=3e10, a=1.0, rg=3.0),
       "SPARC disc": dict(Mb=1.2e10, M200=3e11, a=2.5, rg=7.5),
       "Milky Way": dict(Mb=6e10, M200=1e12, a=3.0, rg=30.0)}
GE_GAL, GE_CL = 0.02, 0.01


def gal_shift(host, eps, coupling):
    """dex shift of the predicted g_obs at r_gate caused by the retained carrier eps (x the pre-decay cold halo)."""
    Mb_fn = hernquist(host["Mb"], host["a"]); Mn, r200, rs = nfw(host["M200"], c200_dm14(host["M200"]))
    r = host["rg"]; gb = Gk * float(Mb_fn(r)) / r ** 2; gc = Gk * eps * (1 - FB) * float(Mn(r)) / r ** 2
    return math.log10(float(gravity(gb, gc, GE_GAL, coupling)) / float(gravity(gb, 0.0, GE_GAL, coupling)))


# ------------------------------------------------------------------------------------------------ X-COP clusters
R500 = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json")))
CL = []
for name, meta in R500.items():
    d = os.path.join(REPO, "real_research", "data", "xcop", name)
    if not os.path.isdir(d):
        continue
    hm = fits.open(os.path.join(d, f"{name}_hydro_mass.fits"))
    Rk, Mf = hm[1].data["RADIUS"], hm[1].data["M_FORW"]
    par = {row["MODEL"].strip(): (float(row["RS"]), float(row["C200"])) for row in hm[2].data}
    fg = fits.open(os.path.join(d, f"{name}_fgas_profile.fits"))[1].data
    R5 = meta["R500"] * 1000.0
    Mgas = float(np.interp(1.0, fg["RADIUS"], fg["MGAS"]))
    ms_path = os.path.join(d, f"{name}_mstar.fits")
    if os.path.exists(ms_path):
        st = fits.open(ms_path)["MSTAR_SMOOTHED"].data
        Mst = float(np.interp(R5, st["RADIUS"], st["MSTAR"]))
    else:
        Mst = 0.015 * float(np.interp(R5, Rk, Mf))
    rs, c = par["NFW"]
    rhoc_z = RHO_C0 * (0.315 * (1 + meta["z"]) ** 3 + 0.685)
    M200 = 200 * rhoc_z * 4 / 3 * math.pi * (c * rs) ** 3
    Mn, _, _ = nfw(M200, c, rhoc_z)
    CL.append(dict(name=name, R500=R5, Mhse=float(np.interp(R5, Rk, Mf)), Mb=Mgas + Mst,
                   Mcarr=(1 - FB) * float(Mn(R5)), M200=M200, c=c, rhoc=rhoc_z, z=meta["z"]))
P(f"  X-COP clusters loaded: {len(CL)} ({', '.join(cl['name'] for cl in CL)})")


def cl_ratio(cl, eps, coupling):
    R = cl["R500"]; gb = Gk * cl["Mb"] / R ** 2; gc = Gk * eps * cl["Mcarr"] / R ** 2
    return float(gravity(gb, gc, GE_CL, coupling)) * R ** 2 / Gk / cl["Mhse"]


def eps_needed(cl, coupling):
    lo, hi = 0.0, 3.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if cl_ratio(cl, mid, coupling) < 1 else (lo, mid)
    return 0.5 * (lo + hi)


# ============================================================================================ controls
banner("CONTROLS")
bias = {}
for k, hst in GAL.items():
    _, b = retained(hernquist(hst["Mb"], hst["a"]), hst["M200"], c200_dm14(hst["M200"]), hst["rg"], GE_GAL,
                    "universal", 0.0, 0.0, N=6000)
    bias[k] = b
check("C1 the no-decay control reproduces the input cold mass inside each gate within 25% (the Maxwellian sampling bias "
      "the ratio method removes; reported so it is visible)", {k: round(v, 3) for k, v in bias.items()},
      all(abs(v - 1) < 0.25 for v in bias.values()))
need = {cp: np.array([eps_needed(cl, cp) for cl in CL]) for cp in COUPLINGS}
OUT["numbers"]["cluster_eps_needed"] = {cp: dict(median=float(np.median(v)), per=[float(x) for x in v]) for cp, v in need.items()}
check("C2 under the ADDITIVE reading the X-COP clusters need a carrier fraction reproducing the record's 0.576 within 25%; "
      "the universal reading needs less (the kernel boosts the carrier too)",
      f"additive median {np.median(need['additive']):.3f}; universal median {np.median(need['universal']):.3f}",
      abs(np.median(need["additive"]) / 0.576 - 1) < 0.25)

# ============================================================================================ the gate
banner("THE z = 0 GATE (f_d(0) = 0.8, the L319 cell): galaxies by the 0.06-dex criterion, X-COP by M_dyn/M_HSE")
VKS = [0.0] if MUTATE else [600.0, 800.0, 1000.0, 1500.0, 2000.0]
S8 = {0.0: 0.8347, 600.0: 0.8263, 800.0: 0.8154, 1000.0: 0.8026}     # L319 main run (the v_k = 0 entry is the no-kick limit)
if not MUTATE:
    src = open(os.path.join(HERE, "L319_lambda_triggered_kicked_decay.py")).read().split(
        "# ============================================================================================ controls")[0]
    import io, contextlib
    gl = {"__name__": "l319", "__file__": os.path.join(HERE, "L319_lambda_triggered_kicked_decay.py")}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, gl)
        LCr = gl["run"](np.ones(gl["N_A"]), 0.0); sv, _ = gl["surv_triggered"](0.8, 2)
        for vk in (1500.0, 2000.0):
            S8[vk] = float(gl["S8_of"](gl["T2"](gl["run"](sv, vk), LCr, 0.0)))
OUT["numbers"]["S8_vs_vk"] = {str(k): v for k, v in S8.items()}
res = {}
for cp in COUPLINGS:
    res[cp] = {}
    cl_ref = CL[int(np.argmin([abs(math.log10(cl["M200"] / 1e15)) for cl in CL]))]
    for vk in VKS:
        row = {}
        for k, hst in GAL.items():
            e, _ = retained(hernquist(hst["Mb"], hst["a"]), hst["M200"], c200_dm14(hst["M200"]), hst["rg"], GE_GAL,
                            cp, vk, 0.8)
            row[k] = dict(eps=float(e), shift=gal_shift(hst, e, cp))
        ecl, _ = retained(hernquist(1.0, 1.0) if False else (lambda x, cl=cl_ref: cl["Mb"] * np.clip(np.asarray(x, dtype=float) / cl["R500"], 0, 1)),
                          cl_ref["M200"], cl_ref["c"], cl_ref["R500"], GE_CL, cp, vk, 0.8, rhoc=cl_ref["rhoc"])
        ratios = np.array([cl_ratio(cl, ecl, cp) for cl in CL])
        row["X-COP"] = dict(eps=float(ecl), median_ratio=float(np.median(ratios)), ratios=[float(x) for x in ratios])
        gal_ok = all(row[k]["shift"] <= 0.06 for k in GAL)
        cl_ok = abs(row["X-COP"]["median_ratio"] - 1) <= 0.20
        s8_ok = S8.get(vk, 0.0) >= 0.767
        row["ok"] = dict(galaxies=bool(gal_ok), clusters=bool(cl_ok), S8=bool(s8_ok))
        res[cp][vk] = row
        P(f"    [{cp:9s}] v_k {vk:6.0f}: " + "; ".join(f"{k} eps {row[k]['eps']:.2f} (+{row[k]['shift']:.3f} dex)" for k in GAL)
          + f"; X-COP eps {ecl:.2f} -> M_dyn/M_HSE {row['X-COP']['median_ratio']:.2f}; S_8 {S8.get(vk, float('nan')):.3f}"
          + f"  [gal {'OK' if gal_ok else 'FAIL'}, cl {'OK' if cl_ok else 'FAIL'}, S8 {'OK' if s8_ok else 'FAIL'}]")
OUT["numbers"]["gate"] = {cp: {str(vk): v for vk, v in rows.items()} for cp, rows in res.items()}
windows = {cp: [vk for vk, row in rows.items() if all(row["ok"].values())] for cp, rows in res.items()}
OUT["numbers"]["windows"] = {cp: [float(v) for v in w] for cp, w in windows.items()}
gal_dep = any(all(res[cp][vk][k]["shift"] <= 0.06 for k in GAL) for cp in COUPLINGS for vk in VKS)
check("G1 the kicks deplete every galaxy host below the RAR-scatter criterion for some v_k (either coupling)",
      "; ".join(f"{cp} v_k {int(vk)}: " + ", ".join(f"{k} +{res[cp][vk][k]['shift']:.3f}" for k in GAL)
                for cp in COUPLINGS for vk in VKS[:3]), gal_dep,
      "kicked late decay empties galaxy halos in the framework's gravity")
check("G2 THE WINDOW -- galaxies, X-COP clusters (within 20%) and S_8 (>= 0.767) at a single v_k, reported per coupling",
      f"universal {windows['universal']}; additive {windows['additive']}", True if MUTATE else True,
      "a finding, not a pass condition: it is stated either way below", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
for cp in COUPLINGS:
    if windows[cp]:
        P(f"  [{cp}] WINDOW at v_k = {windows[cp]} km/s: galaxies depleted, X-COP matched within 20%, S_8 in range.")
    else:
        fails = {vk: [g for g, ok in res[cp][vk]['ok'].items() if not ok] for vk in VKS}
        P(f"  [{cp}] NO WINDOW: " + "; ".join(f"v_k {int(vk)} fails {', '.join(f)}" for vk, f in fails.items()))
P("  Combined with L319 (forest and S_8 pass) and L320 (RC100 ~3 sigma, universal coupling), the carrier's standing is set")
P("  by the coupling: see the per-coupling window above.")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time()-T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
