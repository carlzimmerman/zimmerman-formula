#!/usr/bin/env python3
"""CFG122 edge-fixed solutions: G1.4 (edge step), G1.5 (far-shell), G1.6 (crossover universality), G2.4(ii) (halo number injection), G3.2 (injection energy).
The per-halo constant mu is fixed by the door's own phase-boundary condition (frozen file, (b) 'The phase structure' and G1.5 'the model's own case'):
   R_c from the imported NFW halo:  rho_NFW(R_c) = m n_c(T),  T = m sigma^2, sigma^2 = V_f^2/2 (BTFR, postulated);   mu from n_DM(R_c) = n_c.
NFW: Moster+2013 halo of M_* = M_b (declared), Duffy+2008 full-200c c(M); R_c capped at R_200 if the NFW density there still exceeds m n_c.
Y(r_lo) roots are located on the coarse grid Y = 0, +-10^k m G M/r_M (k=-6..6) by sign changes of ln n(R_c) - ln n_c, then bisected (45 iterations); every root is kept
(existence over roots, branches B-, B+hi, B+lo, and the (m, alpha) plane).  Point-mass baryons.  Env: ZF_REPO (for CFG7_common's committed r_ta_law), MUTATE = c.
Run: ZF_REPO=<repo> python3 cfg122_g1_edge.py"""
import os, sys, math, time, itertools
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import *

MUT = os.environ.get("MUTATE", "")
POSTHOC_AHI = os.environ.get("POSTHOC_ALPHA_HI")      # POST-HOC labelled variant: extend the alpha axis (not part of the frozen plane)
R = Report("cfg122_g1_edge" + (("_POSTHOC_alphaHI" + POSTHOC_AHI) if POSTHOC_AHI else ""))
P, check = R.P, R.check
N = 220
PLANE_N = int(os.environ.get("PLANE_N", "60"))
mg, ag, Mm, Aa = plane(PLANE_N, a_hi=(float(POSTHOC_AHI) if POSTHOC_AHI else 2))
KS = np.arange(-6, 7)
YFAC = np.concatenate([-(10.0 ** KS[::-1]), [0.0], 10.0 ** KS])        # sorted ascending, 27 values
ALPHA_C_FAC = 1e-12 if MUT == "c" else None
SHELL_MFAC, SHELL_R_KPC = 10.0, 40.0
TH = 0.10

# ------------------------------------------------------------------ r_ta conventions (G3.2)
OM48, HH48, DELTA_TA48 = 0.3153, 0.6736, 11.81
RHOC0_MPC = 2.775e11 * HH48 ** 2
OMEGA_C_OVER_B = 0.1200 / 0.02237
KPC_M = 3.0856775814913673e19


def r_ta48_kpc(Mb_msun):
    Mcol = Mb_msun * (1.0 + OMEGA_C_OVER_B)
    return 1e3 * (3.0 * Mcol / (4.0 * math.pi * OM48 * RHOC0_MPC * DELTA_TA48)) ** (1.0 / 3.0)


C7 = None
if REPO is not None:
    try:
        sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
        import CFG7_common as C7                                   # read-only: B's committed r_ta_law (CFG4's convention)
    except Exception as e:                                         # noqa
        P(f"  (CFG7_common import failed: {e}; the committed r_ta convention is then NOT available)")


def r_ta_committed_kpc(Mb_msun):
    if C7 is None:
        return float("nan")
    return 1e3 * float(C7.r_ta_law(Mb_msun, C7.A0["canonical"], C7.nu_mono, 1.0))


def interp_at(q, i0, w):
    """q: (N+1, E); linear interpolation along axis 0 at fractional index i0 + w."""
    a = np.take_along_axis(q, i0[None, :], axis=0)[0]
    b = np.take_along_axis(q, (i0 + 1)[None, :], axis=0)[0]
    return (1 - w) * a + w * b


def f_root(out, Rc, nc, r_lo, ds, m):
    """f = ln n(R_c) - ln n_c along a 1-D element array of solutions; nan where the branch does not exist up to R_c."""
    with np.errstate(divide="ignore", invalid="ignore"):
        lnr = np.log(Rc / r_lo) / ds
    okr = np.isfinite(lnr) & (lnr >= 0) & (lnr <= N - 1e-9)
    t = np.clip(np.where(okr, lnr, 0.0), 0, N - 1e-9)
    i0 = np.floor(t).astype(int)
    w = t - i0
    fin = np.cumprod(np.isfinite(out["rho"]) & np.isfinite(out["a_phi"]), axis=0).astype(bool)
    val = np.take_along_axis(fin, (i0 + 1)[None, :], axis=0)[0] & okr
    with np.errstate(invalid="ignore", divide="ignore"):
        lnn = np.log(out["rho"] / m)
    lnn_c = (1 - w) * np.take_along_axis(lnn, i0[None, :], axis=0)[0] + w * np.take_along_axis(lnn, (i0 + 1)[None, :], axis=0)[0]
    return np.where(val, lnn_c - np.log(nc), np.nan)


def solve_elems(m, alpha, Lam, prof, r_lo, r_hi, Y0, br, a0n, Rc, nc, ac):
    out = integrate(m, alpha, Lam, prof, r_lo, r_hi, N, Y0, br, a0n, alpha_c=ac)
    ds = math.log(r_hi / r_lo) / N
    return out, f_root(out, Rc, nc, r_lo, ds, m)


ROOTS = {}
t0 = time.time()
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    for Mmsun in MASSES:
        prof = Prof("point", Mmsun)
        rMv = float(rM(prof.M, a0n))
        nfw = NFW(Mmsun)
        V2 = float(Vf2(prof.M, a0n)); sig2 = 0.5 * V2
        Rc_m = np.zeros(PLANE_N); flag_m = []
        for i, mm in enumerate(mg):
            nc_ = n_crit(mm, sig2)
            rc, fl = nfw.r_of_rho(mm * nc_)
            Rc_m[i] = rc; flag_m.append(fl)
        r_lo = 0.1 * rMv
        r_hi = max(30 * rMv, 1.02 * nfw.R200)
        ds = math.log(r_hi / r_lo) / N
        P(f"[{foot}] M_b = {Mmsun:.0e}: r_M = {rMv / KPC_EV:.3g} kpc; NFW M_h = {nfw.Mh_msun:.3g} Msun, c = {nfw.c:.2f}, R200 = {nfw.R200 / KPC_EV:.3g} kpc; R_c(m): "
          f"none for {sum(f == 'none' for f in flag_m)}/{PLANE_N} values of m, capped at R200 for {sum(f == 'capped_R200' for f in flag_m)}; grid to {r_hi / rMv:.3g} r_M")
        goodm = np.array([(f != "none") and (r_lo < rc < r_hi) for f, rc in zip(flag_m, Rc_m)])
        for br in BRANCHES:
            cells = []      # element records
            for rw in np.array_split(np.arange(PLANE_N), 6):
                m_, a_ = Mm[rw][:, :, None] * np.ones((1, 1, len(YFAC))), Aa[rw][:, :, None] * np.ones((1, 1, len(YFAC)))
                Lm = lam_tie(m_, a_, a0n)
                base = m_ * G_N * prof.M / rMv
                Y0 = base * YFAC[None, None, :]
                Rc = Rc_m[rw][:, None, None] * np.ones_like(m_)
                nc = n_crit(m_, sig2)
                shp = m_.shape
                fl = lambda x: x.reshape(-1)
                ac = None if ALPHA_C_FAC is None else ALPHA_C_FAC * fl(a_)
                out, f = solve_elems(fl(m_), fl(a_), fl(Lm), prof, r_lo, r_hi, fl(Y0), br, a0n, fl(Rc), fl(nc), ac)
                f = f.reshape(shp)
                gm = goodm[rw][:, None] * np.ones((1, PLANE_N), bool)
                for k in range(len(YFAC) - 1):
                    f1, f2 = f[..., k], f[..., k + 1]
                    act = np.isfinite(f1) & np.isfinite(f2) & (np.sign(f1) != np.sign(f2)) & gm
                    if not act.any():
                        continue
                    ii, jj = np.nonzero(act)
                    cells.append(dict(i=rw[ii], j=jj, ylo=Y0[ii, jj, k], yhi=Y0[ii, jj, k + 1], flo=f1[ii, jj], m=m_[ii, jj, 0], a=a_[ii, jj, 0], Lam=Lm[ii, jj, 0],
                                      Rc=Rc[ii, jj, 0], nc=nc[ii, jj, 0]))
            if not cells:
                ROOTS[(foot, Mmsun, br)] = None
                P(f"    {br:5s}: no roots")
                continue
            c = {k: np.concatenate([d[k] for d in cells]) for k in cells[0]}
            ylo, yhi, flo = c["ylo"].copy(), c["yhi"].copy(), c["flo"].copy()
            acs = None if ALPHA_C_FAC is None else ALPHA_C_FAC * c["a"]
            for it in range(45):
                ymid = 0.5 * (ylo + yhi)
                _, fm = solve_elems(c["m"], c["a"], c["Lam"], prof, r_lo, r_hi, ymid, br, a0n, c["Rc"], c["nc"], acs)
                fm = np.where(np.isfinite(fm), fm, np.nan)
                left = np.sign(fm) == np.sign(flo)
                ylo = np.where(left, ymid, ylo); yhi = np.where(left, yhi, ymid)
                flo = np.where(left, fm, flo)
            yr = 0.5 * (ylo + yhi)
            out, fr = solve_elems(c["m"], c["a"], c["Lam"], prof, r_lo, r_hi, yr, br, a0n, c["Rc"], c["nc"], acs)
            good = np.isfinite(fr) & (np.abs(fr) < 1e-6)
            # diagnostics at the roots
            r = out["r"]
            x = r / rMv
            Rc = c["Rc"]
            t = np.clip(np.log(Rc / r_lo) / ds, 0, N - 1e-9); i0 = np.floor(t).astype(int); w = t - i0
            MD_c = interp_at(out["MD"], i0, w)
            aphi_c = interp_at(out["a_phi"], i0, w)
            Y_c = interp_at(out["Y"], i0, w)
            Mnfw = nfw.M(Rc)
            step_S = np.abs((prof.M + MD_c) - (prof.M + Mnfw)) / (prof.M + Mnfw)
            Mdyn_minus = prof.M + MD_c + Rc ** 2 * aphi_c / G_N
            step_F = np.abs(Mdyn_minus - (prof.M + Mnfw)) / (prof.M + Mnfw)
            with np.errstate(invalid="ignore", divide="ignore"):
                ratio = out["a_phi"] / (G_N * prof.M / r[:, None] ** 2)                # a_phi / g_N (point mass)
            # crossover: first node with ratio >= 1 (linear interpolation in ln r); a_x = g_N there / a0
            cover = (r[:, None] <= Rc[None, :]) & np.isfinite(ratio)
            above = cover & (ratio >= 1.0)
            first = np.where(above.any(axis=0), above.argmax(axis=0), -1)
            a_x = np.full(first.shape, np.nan); flagx = np.array(["none"] * len(first), dtype=object)
            for e in range(len(first)):
                k = first[e]
                if k > 0 and cover[k - 1, e]:
                    l0, l1 = math.log(ratio[k - 1, e]), math.log(ratio[k, e])
                    wq = (0 - l0) / (l1 - l0) if l1 != l0 else 0.5
                    rx = math.exp(math.log(r[k - 1]) * (1 - wq) + math.log(r[k]) * wq)
                    a_x[e] = G_N * prof.M / rx ** 2 / a0n; flagx[e] = "ok"
                elif k == 0:
                    flagx[e] = "below_range"
            # injection: number rate Ndot = alpha Lam M_b / M_Pl (eV), t_H = 1/H0, condensate number N_DM = M_DM(R_c)/m
            aeff = c["a"] if ALPHA_C_FAC is None else ALPHA_C_FAC * c["a"]
            Ndot = aeff * c["Lam"] * prof.M / MPL
            N_DM = MD_c / c["m"]
            frac_halo = Ndot / H0_EV / N_DM
            # mu = Y(R_c) + m Phi(R_c), Phi(R_c) = -G M_b/R_c + Phi_NFW(R_c)
            Phi_c = -G_N * prof.M / Rc + nfw.Phi(Rc)
            mu = Y_c + c["m"] * Phi_c
            ROOTS[(foot, Mmsun, br)] = dict(i=c["i"][good], j=c["j"][good], m=c["m"][good], a=c["a"][good], Lam=c["Lam"][good], Y0=yr[good], Rc=Rc[good], MDc=MD_c[good], aphi_c=aphi_c[good],
                                            step_S=step_S[good], step_F=step_F[good], a_x=a_x[good], flag_x=flagx[good], frac_halo=frac_halo[good], mu=mu[good], Ndot=Ndot[good],
                                            Rc_over_rM=(Rc / rMv)[good], base=(c["m"] * G_N * prof.M / rMv)[good], rMv=rMv, R200=nfw.R200, Vf2=V2)
            P(f"    {br:5s}: {int(good.sum())} converged roots in {len(np.unique(c['i'][good] * PLANE_N + c['j'][good]))} (m, alpha) cells ({time.time() - t0:.0f} s)")

# ------------------------------------------------------------------------------------------------ gates
def cell_key(d):
    return d["i"] * PLANE_N + d["j"]


def exist_all_masses(foot, name, pred, branches=BRANCHES):
    """cells where, for every mass, some root (any listed branch) satisfies pred(root-array) -> boolean array; returns the set of cells and per-mass counts."""
    per_mass = []
    for Mmsun in MASSES:
        cs = set()
        for br in branches:
            d = ROOTS.get((foot, Mmsun, br))
            if d is None:
                continue
            ok = pred(d, Mmsun)
            cs |= set(cell_key(d)[ok].tolist())
        per_mass.append(cs)
    return set.intersection(*per_mass), [len(s) for s in per_mass]


def best_stat(foot, name, branches=BRANCHES):
    out = {}
    for Mmsun in MASSES:
        vals = []
        for br in branches:
            d = ROOTS.get((foot, Mmsun, br))
            if d is not None and len(d[name]):
                v = d[name][np.isfinite(d[name])]
                if len(v):
                    vals.append(float(v.min()))
        out[Mmsun] = min(vals) if vals else float("nan")
    return out


R.banner("root census: cells with an edge-fixed solution (n_DM(R_c) = n_c with R_c from the NFW halo)")
census = {}
for foot in FOOTINGS:
    for br in BRANCHES:
        cs = [len(set(cell_key(ROOTS[(foot, M, br)]).tolist())) if ROOTS.get((foot, M, br)) is not None else 0 for M in MASSES]
        census[(foot, br)] = cs
        P(f"  [{foot}] {br:5s}: cells with >= 1 root at masses {MASSES}: {cs}")
R.num("root_census", {str(k): v for k, v in census.items()})

R.banner("G1.4  edge step at R_c: |M(R_c^-) - M(R_c^+)| / M <= 10%  (S: real mass M_b + M_DM vs M_b + M_NFW ;  F: dynamical mass incl. the phonon force vs M_b + M_NFW)")
g14 = {}
for label, nm in (("S (real mass)", "step_S"), ("F (dynamical)", "step_F")):
    for foot in FOOTINGS:
        cells, cnt = exist_all_masses(foot, nm, lambda d, M: d[nm] <= TH)
        bs = best_stat(foot, nm)
        g14[(label, foot)] = dict(cells=len(cells), per_mass=cnt, best=bs)
        P(f"  [{foot}] Branch {label}: (m, alpha) cells passing at all four masses: {len(cells)}; per-mass cell counts {cnt}; best step per mass {['%.3g' % bs[M] for M in MASSES]}")
R.num("G1.4", {f"{k[0]}|{k[1]}": v for k, v in g14.items()})
R.verdict("G1.4-S", "PASS" if all(g14[("S (real mass)", f)]["cells"] > 0 for f in FOOTINGS) else "FAIL", f"cells {[g14[('S (real mass)', f)]['cells'] for f in FOOTINGS]}; best steps {[['%.3g' % v for v in g14[('S (real mass)', f)]['best'].values()] for f in FOOTINGS]}")
R.verdict("G1.4-F", "PASS" if all(g14[("F (dynamical)", f)]["cells"] > 0 for f in FOOTINGS) else "FAIL", f"cells {[g14[('F (dynamical)', f)]['cells'] for f in FOOTINGS]}; best steps {[['%.3g' % v for v in g14[('F (dynamical)', f)]['best'].values()] for f in FOOTINGS]}")

R.banner("G1.6  crossover universality: a_x(M_b) (g_N at which a_phi = g_N) across 1e9..1e12, spread max/min <= 1.10; existence over roots, branches and the plane")
g16 = {}
for foot in FOOTINGS:
    percell = {}
    for Mmsun in MASSES:
        for br in BRANCHES:
            d = ROOTS.get((foot, Mmsun, br))
            if d is None:
                continue
            ok = np.isfinite(d["a_x"])
            for k, v in zip(cell_key(d)[ok], d["a_x"][ok]):
                percell.setdefault(int(k), {}).setdefault(Mmsun, []).append(float(v))
    best = (np.inf, None)
    ncomplete = 0
    for k, dm in percell.items():
        if len(dm) < len(MASSES):
            continue
        ncomplete += 1
        lists = [dm[M][:8] for M in MASSES]
        for combo in itertools.product(*lists):
            sp = max(combo) / min(combo)
            if sp < best[0]:
                best = (sp, (k, combo))
    g16[foot] = dict(cells_with_crossover_at_all_masses=ncomplete, best_spread=best[0], where=None if best[1] is None else dict(m=float(mg[best[1][0] // PLANE_N]), alpha=float(ag[best[1][0] % PLANE_N]), a_x_over_a0=list(best[1][1])))
    P(f"  [{foot}] cells with a crossover inside the covered range at all four masses: {ncomplete}; smallest spread over roots/branches: {best[0]:.4g}"
      + ("" if best[1] is None else f" at m = {mg[best[1][0] // PLANE_N]:.3g} eV, alpha = {ag[best[1][0] % PLANE_N]:.3g}, a_x/a0 = {['%.3g' % v for v in best[1][1]]}"))
R.num("G1.6", {f: v for f, v in g16.items()})
R.verdict("G1.6", "PASS" if all(g16[f]["best_spread"] <= 1.10 for f in FOOTINGS) else "FAIL", f"smallest spread {[round(g16[f]['best_spread'], 4) for f in FOOTINGS]} (canonical, alt) against the 1.10 line; cells with a crossover at all masses {[g16[f]['cells_with_crossover_at_all_masses'] for f in FOOTINGS]}")

R.banner("G2.4 (ii) number injection inside a halo over one Hubble time: Ndot t_H / N_DM(<R_c) <= 10%   [(i) background is in cfg122_g2.py]")
g24 = {}
for foot in FOOTINGS:
    cells, cnt = exist_all_masses(foot, "frac_halo", lambda d, M: d["frac_halo"] <= 0.10)
    bs = best_stat(foot, "frac_halo")
    g24[foot] = dict(cells=len(cells), per_mass=cnt, best=bs)
    P(f"  [{foot}] cells passing at all masses: {len(cells)}; per-mass cell counts {cnt}; smallest injected fraction per mass {['%.3g' % bs[M] for M in MASSES]}")
R.num("G2.4_ii", {f: v for f, v in g24.items()})
R.verdict("G2.4-ii", "PASS" if all(g24[f]["cells"] > 0 for f in FOOTINGS) else "FAIL", f"cells {[g24[f]['cells'] for f in FOOTINGS]}; smallest fractions {[['%.3g' % v for v in g24[f]['best'].values()] for f in FOOTINGS]}")

R.banner("G3.2  energy of the injected number: |mu| Ndot t vs (1/2) M_b V_f^2, t = t_dyn(r_e) = r_e/V_f in both r_ta conventions (r_e = 0.4 r_ta) and t = 1/H0; PASS iff <= 1 (all)")
V_f_over_c = lambda M, a0n: float(Vf2(M * MSUN_EV, a0n)) ** 0.5
g32 = {}
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    rows = {}
    for Mmsun in MASSES:
        Vf = V_f_over_c(Mmsun, a0n)
        re48 = 0.4 * r_ta48_kpc(Mmsun) * KPC_EV
        rec = 0.4 * r_ta_committed_kpc(Mmsun) * KPC_EV
        rows[Mmsun] = dict(t48=re48 / Vf, tcm=rec / Vf, tH=1.0 / H0_EV)
        rMv = float(rM(Mmsun * MSUN_EV, a0n))
        rows[Mmsun].update(Ec48=1.5 * re48 / rMv, Eccm=1.5 * rec / rMv)
    cellsets = {"t48": [], "tcm": [], "tH": []}
    best = {k: {} for k in cellsets}
    for tag in cellsets:
        per_mass = []
        for Mmsun in MASSES:
            E0 = 0.5 * Mmsun * MSUN_EV * float(Vf2(Mmsun * MSUN_EV, a0n))
            cs = set(); bv = []
            for br in BRANCHES:
                d = ROOTS.get((foot, Mmsun, br))
                if d is None:
                    continue
                ratio = np.abs(d["mu"]) * d["Ndot"] * rows[Mmsun][tag] / E0
                ok = np.isfinite(ratio) & (ratio <= 1.0)
                cs |= set(cell_key(d)[ok].tolist())
                if np.isfinite(ratio).any():
                    bv.append(float(np.nanmin(ratio)))
            per_mass.append(cs); best[tag][Mmsun] = min(bv) if bv else float("nan")
        cellsets[tag] = set.intersection(*per_mass)
    g32[foot] = dict(cells={k: len(v) for k, v in cellsets.items()}, best=best, cells_all=len(set.intersection(*cellsets.values())),
                     t_dyn_Gyr={f"{M:.0e}": {k: v / GYR_EV for k, v in rows[M].items() if k.startswith("t")} for M in MASSES}, Ec_ratio={f"{M:.0e}": [rows[M]["Ec48"], rows[M]["Eccm"]] for M in MASSES})
    P(f"  [{foot}] cells passing at all masses: t_dyn(CFG48 r_ta) {len(cellsets['t48'])}, t_dyn(committed r_ta) {len(cellsets['tcm'])}, t_H {len(cellsets['tH'])}; all three {g32[foot]['cells_all']}")
    for tag in cellsets:
        P(f"        smallest |mu| Ndot t/(1/2 M V_f^2) per mass ({tag}): {['%.3g' % best[tag][M] for M in MASSES]}")
    P(f"        t_dyn(r_e) [Gyr] (CFG48 | committed): " + ", ".join(f"{M:.0e}: {rows[M]['t48'] / GYR_EV:.2f} | {rows[M]['tcm'] / GYR_EV:.2f}" for M in MASSES))
    P(f"        reference (reported): CFG44's own target energy E_c/(1/2 M V_f^2) = 1.5 r_e/r_M: " + ", ".join(f"{M:.0e}: {rows[M]['Ec48']:.1f} | {rows[M]['Eccm']:.1f}" for M in MASSES))
    # rest-mass energy m Ndot t (reported)
    rest = {}
    for Mmsun in MASSES:
        E0 = 0.5 * Mmsun * MSUN_EV * float(Vf2(Mmsun * MSUN_EV, a0n))
        bv = []
        for br in BRANCHES:
            d = ROOTS.get((foot, Mmsun, br))
            if d is not None and len(d["m"]):
                bv.append(float(np.nanmin(d["m"] * d["Ndot"] * rows[Mmsun]["tH"] / E0)))
        rest[Mmsun] = min(bv) if bv else float("nan")
    P(f"        reported: smallest rest-mass energy m Ndot t_H/(1/2 M V_f^2) per mass: {['%.3g' % rest[M] for M in MASSES]}")
    g32[foot]["rest_mass_ratio_tH"] = {f"{M:.0e}": v for M, v in rest.items()}
R.num("G3.2", g32)
R.verdict("G3.2", "PASS" if all(g32[f]["cells_all"] > 0 for f in FOOTINGS) else "FAIL", f"cells passing all three timescales at all masses {[g32[f]['cells_all'] for f in FOOTINGS]}; smallest ratios (t_H) {[['%.3g' % v for v in g32[f]['best']['tH'].values()] for f in FOOTINGS]}")

# ------------------------------------------------------------------------------------------------ G1.5 far-shell test (coarse sub-plane, both cases)
R.banner(f"G1.5  far-shell test: add a shell of {SHELL_MFAC:.0f} M_b at R' = {SHELL_R_KPC:.0f} kpc; r* = min(3 r_M, R'/2); target rho unchanged; PASS iff |d rho/rho| <= 1% (case 2 decides)")
g15 = {}
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    res = {}
    for Mmsun in MASSES:
        rMv = float(rM(Mmsun * MSUN_EV, a0n))
        Rsh = SHELL_R_KPC * KPC_EV
        rstar = min(3 * rMv, 0.5 * Rsh)
        prof0 = Prof("point", Mmsun)
        prof_sh = Prof("point", Mmsun, shell=(Rsh, SHELL_MFAC * prof0.M))
        r_lo = 0.1 * rMv
        Vv = float(Vf2(prof0.M, a0n)); sig2 = 0.5 * Vv
        for br in BRANCHES:
            d = ROOTS.get((foot, Mmsun, br))
            if d is None:
                continue
            sel = np.nonzero(((d["i"] % 3) == 0) & ((d["j"] % 3) == 0))[0]              # coarse sub-plane for cost
            if len(sel) == 0:
                continue
            m_, a_, L_, Y0, Rc = d["m"][sel], d["a"][sel], d["Lam"][sel], d["Y0"][sel], d["Rc"][sel]
            nc = n_crit(m_, sig2)
            r_hi = max(30 * rMv, 1.02 * d["R200"])
            ds = math.log(r_hi / r_lo) / N
            acs = None if ALPHA_C_FAC is None else ALPHA_C_FAC * a_
            o0 = integrate(m_, a_, L_, prof0, r_lo, r_hi, N, Y0, br, a0n, alpha_c=acs)
            ist = int(round(math.log(rstar / r_lo) / ds))
            rho0 = o0["rho"][ist]
            # case 1: mu fixed => Y(r) shifts by m G m_sh / R'
            Y1 = Y0 + m_ * G_N * SHELL_MFAC * prof0.M / Rsh
            o1 = integrate(m_, a_, L_, prof0, r_lo, r_hi, N, Y1, br, a0n, alpha_c=acs)
            d1 = np.abs(o1["rho"][ist] / rho0 - 1)
            # case 2: R_c held, Y re-fixed by n(R_c) = n_c with the shell present (secant); Delta = 0 exactly when R_c <= R'
            d2 = np.full(len(sel), np.nan)             # nan = vacuous (R_c <= R': the shell lies outside the condensate; case 2 is then trivially 0 and is EXCLUDED from the pass count)
            act = Rc > Rsh
            if act.any():
                Ya, Yb = Y0[act].copy(), Y0[act] * (1 + 1e-3) + 1e-3 * d["base"][sel][act]
                sub = lambda Y: solve_elems(m_[act], a_[act], L_[act], prof_sh, r_lo, r_hi, Y, br, a0n, Rc[act], nc[act], None if acs is None else acs[act])
                oa, fa = sub(Ya); ob, fb = sub(Yb)
                for it in range(30):
                    with np.errstate(invalid="ignore", divide="ignore"):
                        Yn = Yb - fb * (Yb - Ya) / (fb - fa)
                    Yn = np.where(np.isfinite(Yn), Yn, Yb)
                    Ya, fa, Yb = Yb, fb, Yn
                    ob, fb = sub(Yb)
                oF, fF = sub(Yb)
                conv = np.isfinite(fF) & (np.abs(fF) < 1e-6)
                with np.errstate(invalid="ignore", divide="ignore"):
                    dd = np.abs(oF["rho"][ist] / rho0[act] - 1)
                d2[act] = np.where(conv, dd, np.nan)
            res[(Mmsun, br)] = dict(cells=cell_key({"i": d["i"][sel], "j": d["j"][sel]}), d1=d1, d2=d2, frac_R_gt_Rp=float(act.mean()))
    # existence: cells with all masses <= 1% (case 2 decides); case 1 reported
    for case, nm in (("case 1 (mu fixed)", "d1"), ("case 2 (edge re-fixed)", "d2")):
        per_mass = []
        minv = {}
        for Mmsun in MASSES:
            cs = set(); mv = []
            for br in BRANCHES:
                r_ = res.get((Mmsun, br))
                if r_ is None:
                    continue
                v = r_[nm]
                ok = np.isfinite(v) & (v <= 0.01)
                cs |= set(r_["cells"][ok].tolist())
                if np.isfinite(v).any():
                    mv.append(float(np.nanmin(v)))
            per_mass.append(cs); minv[Mmsun] = min(mv) if mv else float("nan")
        allc = set.intersection(*per_mass)
        g15[(foot, nm)] = dict(cells=len(allc), per_mass=[len(s) for s in per_mass], min_delta=minv)
        P(f"  [{foot}] {case}: sub-plane cells with |d rho/rho| <= 1% at all four masses: {len(allc)} (per mass {[len(s) for s in per_mass]}); smallest |d rho/rho| per mass {['%.3g' % minv[M] for M in MASSES]}")
    fr = {f"{M:.0e}": [res[(M, br)]["frac_R_gt_Rp"] for br in BRANCHES if (M, br) in res] for M in MASSES}
    P(f"        fraction of roots with R_c > R' (shell inside the condensate; otherwise case 2 is trivially 0): {fr}")
R.num("G1.5", {f"{k[0]}|{k[1]}": v for k, v in g15.items()})
R.verdict("G1.5", "PASS" if all(g15[(f, 'd2')]["cells"] > 0 for f in FOOTINGS) else "FAIL", f"case 2 cells {[g15[(f, 'd2')]['cells'] for f in FOOTINGS]}; case 1 cells {[g15[(f, 'd1')]['cells'] for f in FOOTINGS]}")

nf, gf = R.write()
sys.exit(1 if (nf or gf) else 0)
