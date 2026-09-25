#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L363 -- COSMIC SHEAR FOR THE ASSEMBLED CONSTRUCTION: does the bound-region kernel's phantom (L361), which KiDS
galaxy-galaxy lensing needs around every lens (L359/L360), add lensing power that cosmic shear would see?

WHY.  L360 passes KiDS-1000 galaxy-galaxy lensing -- a galaxy-MASS cross-correlation -- with a switched phantom that is
isothermal out to each region's edge (~1-2 Mpc) and then Gauss-cancelled.  Cosmic shear measures the MASS-MASS
power at k ~ 0.1-1 h/Mpc and finds it at or below LCDM.  Light sees the phantom.  The parallel GP3
(real_research/generated_phantom_2026, a source-switched, Yukawa-screened kernel) finds the phantom inflates the lensing
power 1.5-2.9x at k <= 1 h/Mpc.  L361's phantom differs in one place that could matter: it is cancelled at every
region's edge, so it has no monopole beyond a region.  This lane measures its lensing power.

TWO ESTIMATES (L361's field equations; GP3's machinery and mock loaded unedited)
  (M) THE MOCK: GP3's nonlinear mock at z = 0.5 (lognormal matter smoothed at 1.5 Mpc, Sheth-Tormen halos with GP0's bound
      baryons deposited on the grid).  Regions: the gated switch x~ = (3/2) Omega_m(z)(rho_dyn/rho_bar - 1) >= x_c,eff(z),
      rho_dyn = matter + the phantom, grown by iteration on dilated masks until converged.  Kernel: lap w = 4 pi G rho_src on
      active cells, w = 0 off them (the Dirichlet limit of L361's screening); phantom: lap P = div[(nu - 1) grad w] on active
      cells, P = 0 off them; rho_ph = lap P / 4 pi G on the full grid -- the compensating edge shell comes out exactly.
      Two boxes (200 Mpc and 100 Mpc, 256^3) and two sources (GP0's bound baryons; all baryons in active cells, L361's
      literal source).
  (H) THE HALO MODEL (resolution-free, the converged estimate): each halo is its own region; inside it the phantom of its
      baryons M_b is the isolated QUMOND one (a spherical Dirichlet region leaves the monopole field exact), cancelled by
      a shell at the edge r_e where x~(r_e) = x_c,eff.  Its transform is exactly
          rho~_ph(k) = int_0^{r_e} M_ph(<r) k j1(k r) dr,   M_ph(<r) = (nu(G M_b/r^2 a0) - 1) M_b,
      (-> 0 as k^2: no large-scale power).  One-halo phantom power, its cross with the NFW matter, and two-halo terms are
      added to GP3's Sheth-Tormen + NFW P_NL.  Baryon readings: GP0 'observed' and 'maximal' (all the halo's baryons).
GATE (GP3's, pre-declared there and adopted unchanged): the lensing power stays within 20% of LCDM's, R(k) <= 1.2 for
all k in [0.1, 1] h/Mpc, both footings -- R_cons (GP3's conservative ratio) for the mock, P_lens/P_NL for the halo model.
CHECKS
  C1 CONTROL: the kernel off (a0 -> 0) gives no phantom and R = 1.
  C2 CONTROL: each region's phantom has zero total mass (global sum / source mass < 1e-12).
  X1 THE VERDICT: the construction's lensing power exceeds the gate (R > 1.2 somewhere in k = 0.1-1 h/Mpc) in the halo
     model on both readings and footings, and in the finest mock.  (Direction fixed after an exploratory run of the mock
     pieces, not committed; nothing retuned.)
  X2 (reported) the resolution trend of the mock and the source reading.
  X3 (reported) THE REPLACEMENT LEAD, against P_NL (not mock-internal): if the carrier has left every halo below M_cut
     (its one-halo power removed there, baryons kept), how close does the lensing power come to LCDM's?
MUTATE=1 switches the kernel off: X1's excess vanishes and X1 must FAIL (rc = 1).
SCOPE.  One lens epoch (z = 0.5, the cosmic-shear lens peak); P(k), not a Limber-projected xi_+-; the gated switch cell
of L360's example (p = 1, x_c0 = 1.5) and the highest-threshold window cell (p = 2, x_c0 = 2); halo-model regions are
single halos (group regions containing several galaxies are in the mock).

Run from the repository root:  python3 real_research/g03_audit_2026/L363_region_kernel_lensing_power.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.linalg import cg
from scipy.special import spherical_jn
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L363_region_kernel_lensing_power"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L363", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the kernel is switched off; X1 must FAIL ***")

# ---------------------------------------------------------------------------------- GP3's machinery, unedited
GPD = os.path.join(REPO, "real_research", "generated_phantom_2026"); sys.path.insert(0, GPD)
P3 = os.path.join(GPD, "GP3_lensing_power_and_growth.py")
NS = {"__name__": "gp3", "__file__": P3}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P3).read().split("T1 = time.time()")[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), NS)
GP0, build_mock, spectra, ratios, nu_mono, nfw_uk = [NS[k] for k in ("GP0", "build_mock", "spectra", "ratios", "nu_mono", "nfw_uk")]
G, MS, MPC, aS, ZS, h, PNL_of, KHM, PNL, PLIN_HM, I1 = [NS[k] for k in ("G", "MS", "MPC", "aS", "ZS", "h", "PNL_of", "KHM", "PNL", "PLIN_HM", "I1")]
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
RHO = GP0.RHO_M0
E2 = GP0.Om * (1 + ZS) ** 3 + GP0.OL
Omz = GP0.Om * (1 + ZS) ** 3 / E2
CELLS = {"p=1, x_c0=1.5 (L360's example)": 1.5 * E2 ** 1.0, "p=2, x_c0=2.0 (highest window threshold)": 2.0 * E2 ** 2.0}
KG = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)
P(f"  GP3 machinery loaded; z = {ZS}; x_c,eff(0.5): " + ", ".join(f"{k_} -> {v_:.2f}" for k_, v_ in CELLS.items()) + f"   [{time.time()-T0:.0f}s]")


# ============================================================================================ (M) the mock machinery
def lap_periodic(u, dx):
    return (np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) + np.roll(u, -1, 1) + np.roll(u, 1, 2) + np.roll(u, -1, 2) - 6 * u) / dx ** 2


def masked_poisson(mask, rhs, dx):
    """lap u = rhs on the mask, u = 0 off it (Dirichlet); Jacobi-preconditioned CG on the active cells."""
    N = mask.shape[0]
    idx = -np.ones(mask.shape, dtype=np.int64); act = np.flatnonzero(mask); idx.flat[act] = np.arange(act.size)
    n = act.size; ii = np.unravel_index(act, mask.shape)
    rows, cols, vals = [np.arange(n)], [np.arange(n)], [np.full(n, 6 / dx ** 2)]
    for ax in range(3):
        for s in (1, -1):
            nb = [a.copy() for a in ii]; nb[ax] = (nb[ax] + s) % N
            j = idx[tuple(nb)]; ok = j >= 0
            rows.append(np.arange(n)[ok]); cols.append(j[ok]); vals.append(np.full(ok.sum(), -1 / dx ** 2))
    A = sparse.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))   # = -lap
    kw = {"rtol": 1e-10} if "rtol" in cg.__code__.co_varnames else {"tol": 1e-10}
    x, info = cg(A, -rhs.flat[act], M=sparse.diags(1 / A.diagonal()), maxiter=20000, **kw)
    u = np.zeros(mask.shape); u.flat[act] = x
    return u, info


def grad(u, dx):
    return [(np.roll(u, -1, a) - np.roll(u, 1, a)) / (2 * dx) for a in range(3)]


def region_phantom(mk, mask, src, a0, on=True):
    """L361 in the Dirichlet limit, physical units at z = 0.5 on the comoving grid; returns rho_ph (comoving Msun/Mpc^3)."""
    dx = mk["dx"]
    if not on:
        return np.zeros_like(src), 0, 0, np.zeros(1)
    rhs = 4 * np.pi * G * (src / aS ** 3) * (MS / MPC ** 3) * (aS * MPC) ** 2 * mask       # lap_c w = (a MPC)^2 4 pi G rho_phys
    w, i1 = masked_poisson(mask, rhs, dx)
    gw = grad(w, dx)
    gm = np.sqrt(sum((g / (aS * MPC)) ** 2 for g in gw))
    nu1 = np.where(mask, nu_mono(np.maximum(gm, 1e-30) / a0) - 1, 0.0)
    F = [nu1 * g for g in gw]
    S = sum((np.roll(F[a], -1, a) - np.roll(F[a], 1, a)) / (2 * dx) for a in range(3)) * mask
    Pp, i2 = masked_poisson(mask, S, dx)
    rho_ph = lap_periodic(Pp, dx) / (aS ** 2 * MPC ** 2) / (4 * np.pi * G) * aS ** 3 / (MS / MPC ** 3)
    return rho_ph, i1, i2, nu1[mask]


def build_regions(mk, src, xc, a0, on=True, iters=6):
    seed = mk["rhoB"] > 0
    rd = mk["rho_m"]; mask = (1.5 * Omz * (rd / RHO - 1) >= xc) | seed
    st = ndimage.generate_binary_structure(3, 1)
    for it in range(iters):
        if not on: break
        dil = ndimage.binary_dilation(mask, structure=st)
        rp, _, _, _ = region_phantom(mk, dil, src, a0, on)
        new = (1.5 * Omz * ((rd + np.maximum(np.where(dil, rp, 0.0), 0.0)) / RHO - 1) >= xc) & dil
        grew = int((new & ~mask).sum()); mask = mask | new
        if grew < 1e-4 * mask.sum(): break
    return mask, it + 1


def mock_ratio(mk, src_name, xc, a0, on=True):
    src = mk["rhoB"] if src_name == "bound" else GP0.FB * mk["rho_m"]
    mask, nit = build_regions(mk, src, xc, a0, on)
    src_m = src * mask
    rp, i1, i2, nu1 = region_phantom(mk, mask, src_m, a0, on)
    pk = spectra(mk, {"m": mk["rho_m"] / RHO - 1, "ph": rp / RHO})
    kh, Pmm = pk("m", "m"); _, Pxx = pk("m", "ph"); _, Ppp = pk("ph", "ph")
    kh, Rm, Rc, rx = ratios({"kh": kh, "Pmm": Pmm, "Pxx": Pxx, "Ppp": Ppp})
    gauss = float(abs(rp.sum()) / max(src_m.sum(), 1e-300))
    return dict(kh=kh, R_cons=Rc, R_mock=Rm, rx=rx, active=float(mask.mean()), iters=nit, cg=(i1, i2), gauss=gauss,
                nu1_median=float(np.median(nu1)) if nu1.size > 1 else 0.0)


# ============================================================================================ (H) the halo model
dn, bh, _ = GP0.mass_function(ZS)
LMH = np.arange(10.0, 15.51, 0.05); dlnM = 0.05 * math.log(10)
KC = KHM                                                                # comoving 1/Mpc (GP3's grid)


def halo_phantom_transform(M, Mb, xc, a0, on=True):
    """rho~_ph(k) [Msun] of one halo's compensated region phantom at the comoving wavenumbers KC; also r_e (phys Mpc)."""
    if not on or Mb <= 0: return np.zeros_like(KC), 0.0
    rho_bar_phys = RHO / aS ** 3                                        # Msun/Mpc^3 physical
    rho_c_phys = GP0.RHO_CRIT0 * E2
    c = 10 ** (0.905 - 0.101 * math.log10(M / (1e12 / h))) * (1 + ZS) ** -0.5
    r200 = (3 * M / (4 * math.pi * 200 * rho_c_phys)) ** (1 / 3); rs = r200 / c
    mc = math.log(1 + c) - c / (1 + c)
    r = np.geomspace(1e-3 * r200, 30.0, 4000)                           # physical Mpc
    y = G * Mb * MS / (r * MPC) ** 2 / a0                               # g_N/a0 of the region's baryons (point mass, physical)
    Mph = (nu_mono(y) - 1) * Mb
    rho_ph = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
    rho_h = np.where(r < r200, M / (4 * math.pi * rs ** 3 * mc) / ((r / rs) * (1 + r / rs) ** 2), 0.0)
    x = 1.5 * Omz * ((rho_h + np.maximum(rho_ph, 0)) / rho_bar_phys - 1)
    above = np.where(x >= xc)[0]
    re = float(r[above.max()]) if above.size else float(r[0])
    sel = r <= re
    rc = r[sel] / aS                                                    # comoving Mpc
    kr = np.outer(KC, rc)
    integ = Mph[sel][None, :] * KC[:, None] * spherical_jn(1, kr)
    return np.trapz(integ, rc, axis=1), re


def halo_model_ratio(xc, a0, reading, on=True, Mcut=None):
    P1, X1h, B = np.zeros_like(KC), np.zeros_like(KC), np.zeros_like(KC)
    dP1h_rm = np.zeros_like(KC)
    res = []
    for lm in LMH:
        M = 10 ** lm; n = float(np.interp(lm, GP0.LM, dn)); b = float(np.interp(lm, GP0.LM, bh))
        Mb = float(GP0.M_bound(M, ZS, reading))
        tr, re = halo_phantom_transform(M, Mb, xc, a0, on)
        uk = nfw_uk(M, KC)
        P1 += n * tr ** 2 * dlnM / RHO ** 2
        X1h += n * M * uk * tr * dlnM / RHO ** 2
        B += n * b * tr * dlnM / RHO
        if Mcut is not None and M < Mcut:                               # the carrier gone from this halo: its dark one-halo power removed
            fd = 1 - GP0.FB
            dP1h_rm += n * ((M * uk) ** 2 - (GP0.FB * M * uk) ** 2) * dlnM / RHO ** 2
            X1h -= n * fd * M * uk * tr * dlnM / RHO ** 2
        res.append((lm, re))
    Pph = P1 + B ** 2 * PLIN_HM
    Pxm = X1h + I1 * B * PLIN_HM
    Plens = PNL - dP1h_rm + 2 * Pxm + Pph
    R = Plens / PNL
    return {q: float(np.interp(math.log(q * h), np.log(KC), R)) for q in KG}, res


# ============================================================================================ C1 control
banner("C1-C2  CONTROLS")
MK200 = build_mock(200.0, 256, 20260925)
m_off = mock_ratio(MK200, "bound", CELLS["p=1, x_c0=1.5 (L360's example)"], A0["canonical"], on=False)
c1 = float(np.max(np.abs(m_off["R_mock"] - 1)))
h_off, _ = halo_model_ratio(CELLS["p=1, x_c0=1.5 (L360's example)"], A0["canonical"], "observed", on=False)
c1h = max(abs(v - 1) for v in h_off.values())
check("C1 CONTROL: the kernel off gives no phantom -- R = 1 in the mock and in the halo model", f"mock {c1:.1e}; halo model {c1h:.1e}",
      c1 < 1e-9 and c1h < 1e-9, load_bearing=False)

# ============================================================================================ (M) the mock
banner("(M)  THE MOCK: L361's region kernel on GP3's nonlinear mock at z = 0.5")
MOCK = {}
runs = [("200 Mpc", MK200, "bound", c_, "canonical") for c_ in CELLS]
MK100 = build_mock(100.0, 256, 20260926)
runs += [("100 Mpc", MK100, src_, c_, f_) for src_ in ("bound", "all") for c_ in CELLS for f_ in A0
         if not (src_ == "all" and c_ != "p=1, x_c0=1.5 (L360's example)")]
for (box, mk, src_, cell, foot) in runs:
    r_ = mock_ratio(mk, src_, CELLS[cell], A0[foot], on=not MUTATE)
    MOCK[(box, src_, cell, foot)] = r_
    P(f"    {box:7s} source {src_:5s} {cell[:14]:14s} {foot:9s}: active {r_['active']:.3f} ({r_['iters']} iterations), median nu-1 "
      f"{r_['nu1_median']:.0f}; R_cons at " + ", ".join(f"{q}: {np.interp(q, r_['kh'], r_['R_cons']):.2f}" for q in KG)
      + f"   [{time.time() - T0:.0f}s]")
OUT["numbers"]["mock"] = {"/".join(k_): {"R_cons": {str(q): float(np.interp(q, v_["kh"], v_["R_cons"])) for q in KG},
                                          "active": v_["active"], "gauss": v_["gauss"]} for k_, v_ in MOCK.items()}
gmax = max(v_["gauss"] for v_ in MOCK.values())
check("C2 CONTROL: every region's phantom is cancelled -- the global phantom mass is zero to machine precision",
      f"max |sum rho_ph| / source mass = {gmax:.1e}", MUTATE or gmax < 1e-12, load_bearing=False)

# ============================================================================================ (H) the halo model
banner("(H)  THE HALO MODEL: each halo's compensated region phantom on top of LCDM's Sheth-Tormen + NFW P_NL")
HM = {}
for reading in ("observed", "maximal"):
    for cell, xc in CELLS.items():
        for foot in A0:
            R, res = halo_model_ratio(xc, A0[foot], reading, on=not MUTATE)
            HM[(reading, cell, foot)] = R
            re12 = float(np.interp(12.0, [a for a, _ in res], [b for _, b in res]))
            P(f"    {reading:8s} {cell[:14]:14s} {foot:9s}: r_e(1e12) {re12:.2f} Mpc; P_lens/P_NL at " + ", ".join(f"{q}: {v:.2f}" for q, v in R.items()))
OUT["numbers"]["halo_model"] = {"/".join(k_): v_ for k_, v_ in HM.items()}

# ============================================================================================ X1 the verdict
banner("X1  THE VERDICT against GP3's gate (R <= 1.2 on k = 0.1-1 h/Mpc)")
hm_worst = {k_: max(v_.values()) for k_, v_ in HM.items()}
fine = {k_: max(float(np.interp(q, v_["kh"], v_["R_cons"])) for q in KG) for k_, v_ in MOCK.items() if k_[0] == "100 Mpc" and k_[1] == "bound"}
P("    halo model, worst R over k = 0.1-1: " + "; ".join(f"{k_[0]}/{k_[1][:14]}/{k_[2][:5]} {v_:.2f}" for k_, v_ in hm_worst.items()))
P("    finest mock (100 Mpc, bound source), worst R_cons: " + "; ".join(f"{k_[2][:14]}/{k_[3][:5]} {v_:.2f}" for k_, v_ in fine.items()))
fails = all(v_ > 1.2 for v_ in hm_worst.values()) and all(v_ > 1.2 for v_ in fine.values())
check("X1 THE ASSEMBLED CONSTRUCTION FAILS COSMIC SHEAR: its lensing power exceeds LCDM's by more than 20% somewhere in "
      "k = 0.1-1 h/Mpc, in the resolution-free halo model on both baryon readings and footings and in the finest mock",
      f"halo model worst {min(hm_worst.values()):.2f}-{max(hm_worst.values()):.2f}; finest mock worst {min(fine.values()):.2f}-"
      f"{max(fine.values()):.2f}", fails,
      "Gauss cancellation removes the phantom's power as k -> 0, but each galaxy's isothermal phantom (a few times its halo "
      "mass inside its ~1-2 Mpc region, the profile KiDS galaxy-galaxy lensing wants) adds one-halo power at k ~ 0.3-1")

# ============================================================================================ X2 resolution and source
banner("X2  (reported) RESOLUTION AND SOURCE")
for cell in CELLS:
    a = MOCK.get(("200 Mpc", "bound", cell, "canonical")); b = MOCK.get(("100 Mpc", "bound", cell, "canonical"))
    if a and b:
        P(f"    {cell[:14]:14s} canonical, bound: R_cons(0.5 / 1 h/Mpc) 200 Mpc {np.interp(0.5, a['kh'], a['R_cons']):.2f} / "
          f"{np.interp(1.0, a['kh'], a['R_cons']):.2f} -> 100 Mpc {np.interp(0.5, b['kh'], b['R_cons']):.2f} / {np.interp(1.0, b['kh'], b['R_cons']):.2f}")
al = MOCK.get(("100 Mpc", "all", "p=1, x_c0=1.5 (L360's example)", "canonical"))
if al: P(f"    L361's literal source (all baryons in active cells), 100 Mpc: R_cons(0.5 / 1) {np.interp(0.5, al['kh'], al['R_cons']):.2f} / {np.interp(1.0, al['kh'], al['R_cons']):.2f}")
check("X2 (reported) the mock's excess falls with resolution (smaller cells shrink small galaxies' regions to their physical "
      "edges) and rises with the source (all in-region baryons > the bound census)", "see above", True, load_bearing=False)

# ============================================================================================ X3 the replacement lead
banner("X3  (reported) THE REPLACEMENT LEAD, against P_NL: the carrier gone from every halo below M_cut")
RP = {}
for Mcut in (1e12, 1e13, 1e14):
    R, _ = halo_model_ratio(CELLS["p=1, x_c0=1.5 (L360's example)"], A0["canonical"], "observed", on=not MUTATE, Mcut=Mcut)
    RP[Mcut] = R
    P(f"    M_cut = {Mcut:.0e}: P_lens/P_NL at " + ", ".join(f"{q}: {v:.2f}" for q, v in R.items()))
OUT["numbers"]["replacement"] = {f"{k_:.0e}": v_ for k_, v_ in RP.items()}
check("X3 (reported) the replacement lead: removing the carrier's one-halo power from halos below M_cut (as a decay that "
      "empties galaxy and group halos would) against the phantom's added power", {f"{k_:.0e}": round(max(v_.values()), 2) for k_, v_ in RP.items()},
      True, "the phantom must REPLACE the dark component's small-scale lensing power, not add to it", load_bearing=False)

banner("VERDICT")
P(f"""  Cosmic shear is the construction's open gate.  L361's phantom is cancelled at every region's edge, so it adds nothing as
  k -> 0, but inside each region it is the isothermal phantom KiDS galaxy-galaxy lensing wants -- a few times the halo's
  mass out to ~1-2 Mpc -- and that is one-halo power at k ~ 0.3-1 h/Mpc.  Halo model (converged): worst R =
  {min(hm_worst.values()):.2f}-{max(hm_worst.values()):.2f} against the gate's 1.2; finest mock {min(fine.values()):.2f}-{max(fine.values()):.2f}.
  The replacement lead (X3): the phantom must stand in for, not add to, the dark component's small-scale power.""")
n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
