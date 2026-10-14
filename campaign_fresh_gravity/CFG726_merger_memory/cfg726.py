#!/usr/bin/env python3
"""CFG726 (FROZEN_CRITERIA.md, 78e51c189): MERGER MEMORY (H-MM). Cold energy is conserved and collisionless; each bound progenitor
carries its tethered cold energy (its own law phantom, cut at its own supply edge and its own r_ta). The law is sub-additive, so the
superposed progenitor halos C(<r) can exceed the remnant's law T_rem(<r); the excess cannot be destroyed and persists as free memory
mass:  M_HMM(<r) = M_b(<r) + max[C(<r), T_rem(<r)].  POST-HOC: every target was already seen.
Stages (CFG726_MODE): tk | erass | accept | efeds | score   (work files in ../_external_data/cfg726_work, not committed)
Run from the repository root, one stage at a time:
  CFG726_MODE=<stage> OMP_NUM_THREADS=1 nice -n 10 python3 -u campaign_fresh_gravity/CFG726_merger_memory/cfg726.py
No Method A infall run (cfg637_lib.derive is never called), no PM run; one process, < 0.8 GB.
kappa = 1/2 FITTED; cold energy mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, contextlib, subprocess
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg726_work"); os.makedirs(WORK, exist_ok=True)
for d in (LANES, os.path.join(LANES, "CFG637_derived_reservoir"), os.path.join(LANES, "CFG652_hot_group_discriminator"),
          os.path.join(LANES, "CFG540_vizier2026_bfjr_mhongoose")):
    sys.path.insert(0, d)
try:
    os.nice(10)
except OSError:
    pass
import cfg637_lib as L                                              # noqa: E402
import CFG4_common as C4                                            # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import cfg652_model as M652                                     # noqa: E402
    import cfg540_bfjr as C540                                      # noqa: E402
MODE = os.environ.get("CFG726_MODE", "score")
T0 = time.time(); LOG = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def memcheck(stage):
    """Abort the stage if free + inactive memory < 10 GB (machine shared with a 1024^3 job)."""
    try:
        out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
        pg = 16384
        for l in out.splitlines():
            if "page size of" in l: pg = int(l.split("page size of")[1].split()[0])
        val = {l.split(":")[0].strip(): int(l.split(":")[1].strip().rstrip(".")) for l in out.splitlines()[1:] if ":" in l}
        gb = (val.get("Pages free", 0) + val.get("Pages inactive", 0)) * pg / 1e9
    except Exception:
        return
    P(f"  vm_stat before {stage}: free+inactive {gb:.1f} GB")
    if gb < 10.0:
        P(f"  ABORT {stage}: free+inactive {gb:.1f} GB < 10 GB"); sys.exit(3)


def nu_s(y):                                                         # CFG695: g_N = g^2/(g + a0)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_add(y):                                                       # M-ADD: additive law, phantom = source
    return 2.0 + 0.0 * np.asarray(y, float)


KERN = {"s": nu_s, "mono": C4.nu_mono}
KALL = dict(KERN, add=nu_add)
FEET = ("canonical", "alt")
A0K = {f: C4.A0[f] * L.SI_TO_KPCGYR2 for f in FEET}                  # kpc / Gyr^2
A0SI = {f: C4.A0[f] for f in FEET}
RE_GAL = M652.RE_BCG                                                 # 15 kpc (inherited)
SUP_PER_COND = M652.COLD_PER_B / M652.F_COND_FLOOR                   # 53.64 x m for a condensed progenitor
_RTA = {}


def rta_of(M_ta, z):
    k = (round(math.log10(M_ta), 4), round(z, 4))
    if k not in _RTA:
        _RTA[k] = L.r_ta_single(M_ta, 1.0 / (1.0 + z))[0]
    return _RTA[k]


def prog_halo(rg, Mshape, m, z, a0, nu):
    """Tethered cold energy of one condensed progenitor of baryon mass m whose cumulative profile is m*Mshape(rg) (rg kpc):
    its own law phantom, cut at its own supply edge (53.64 m) and confined to its own r_ta. Returns T(<s) on rg, r_ta, x_edge."""
    rta = rta_of(m / M652.F_COND_FLOOR / L.FB, z)
    mph, xe = L.phantom_trunc(rg / rta, m * Mshape, rta, a0, nu, SUP_PER_COND * m)
    return mph, rta, xe


def shell_frac(s, d, R):
    """fraction of a spherical shell (radius s, centre at distance d from the origin) inside the ball of radius R."""
    f = (R ** 2 - (d - s) ** 2) / (4.0 * np.maximum(d * s, 1e-300))
    f = np.clip(f, 0.0, 1.0)
    f = np.where(R >= s + d, 1.0, f)
    f = np.where(R <= np.abs(s - d), 0.0, f)
    return f


RCOARSE = np.geomspace(0.3, 3.0e4, 170)                              # kpc


def convolve_members(dk, Ncum, sk, Tcum, Rout_kpc):
    """Superpose identical halos T(<s) (on sk, kpc) centred on members whose cluster-centric cumulative count fraction is Ncum(<d)
    (on dk, kpc). Returns cluster-centric cumulative C(<R) per unit member count on Rout_kpc (log interpolation of a coarse grid)."""
    dN = np.diff(Ncum); dm = np.sqrt(dk[1:] * dk[:-1])
    dT = np.r_[Tcum[0], np.diff(Tcum)]; sm = np.r_[sk[0] * 0.5, np.sqrt(sk[1:] * sk[:-1])]
    Cc = np.zeros(len(RCOARSE))
    for j0 in range(0, len(RCOARSE), 34):
        Rj = RCOARSE[j0:j0 + 34]
        A = shell_frac(sm[None, :, None], dm[:, None, None], Rj[None, None, :])
        Cc[j0:j0 + 34] = np.einsum("d,s,dsr->r", dN, dT, A)
    Cc = np.maximum.accumulate(Cc)
    lo = np.log(np.maximum(Cc, 1e-300))
    out = np.exp(np.interp(np.log(Rout_kpc), np.log(RCOARSE), lo, left=-700.0))
    out[Rout_kpc > RCOARSE[-1]] = Cc[-1]
    return np.where(out < 1e-250, 0.0, out)


R_OBS = np.geomspace(0.5, 6e4, 900)


def rx_of(Mhot):                                                     # CFG721 aperture convention (eRASS1 Mgas500-R500 power law)
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    p = np.polyfit(np.log10(d["mg"]), np.log10(d["R500"]), 1)
    return 1000.0 * 10 ** (p[0] * np.log10(Mhot) + p[1])


def maxent_P2(rg, Mb, T, Cmax, rta):
    """REPORTED bracket P2: free mass F = max(C - T)^+ re-placed as CFG637 Method B (Woolley F(E), total potential, bounded at r_ta),
    energy target = sum dM_free [Phi + 3/4 v_c^2] on the P1 free distribution. Returns M_free,P2(<r) on rg and F."""
    E = np.maximum(Cmax - T, 0.0); F = float(E.max())
    if F <= 0:
        return np.zeros(len(rg)), 0.0
    kp = int(np.argmax(E)); dE = np.r_[E[0], np.diff(E)]; dE[kp + 1:] = 0.0; dE = np.maximum(dE, 0.0)
    Mt = Mb + np.maximum(Cmax, T)
    g = L.G * Mt / rg ** 2 - L.OL * L.H0 ** 2 * rg
    Phi = np.zeros(len(rg)); Phi[-1] = -L.G * Mt[-1] / rg[-1] - 0.5 * L.OL * L.H0 ** 2 * rg[-1] ** 2
    seg = 0.5 * (g[1:] + g[:-1]) * np.diff(rg); Phi[:-1] = Phi[-1] - np.cumsum(seg[::-1])[::-1]
    Et = float(np.sum(dE * (Phi + 0.75 * L.G * Mt / rg))) / max(dE.sum(), 1e-300) * F
    Mr, s2, Ereach, ok = L.maxent_reservoir(rg, Mb + T, F, Et, rta)
    return np.nan_to_num(Mr), F


# ============================================================================================ T-K KiDS early/late (+ T-S2)
if MODE == "tk":
    memcheck("tk")
    RK = np.array([50.0, 70.71, 100.0]); out = []
    SETS = {f"N{n}": [1.0 / n] * n for n in (1, 2, 3, 4, 5)}; SETS["q1/3"] = [0.75, 0.25]
    for kern in KALL:
        for foot in FEET:
            a0 = A0K[foot]; nu = KALL[kern]
            for lm in (10.0, 10.5, 11.0, 11.5):
                Mb = 10 ** lm; Rx = rx_of(Mb)
                mc, mh = M652.profiles(Mb, 0.0, Rx, R_OBS); shape = mc / Mb
                rta = rta_of(Mb / M652.F_COND_FLOOR / L.FB, 0.0)
                gN = L.G * mc / R_OBS ** 2; T = mc * (nu(gN / a0) - 1.0)            # remnant plain law (uncut, to r_ta)
                base = M652.delta_sigma(R_OBS, mc + T, RK, rmax=rta)
                row = dict(kern=kern, foot=foot, lMb=lm, rta=rta, base=base.tolist(), sets={})
                for nm, fr in SETS.items():
                    C = np.zeros(len(R_OBS)); edges = []
                    for f in fr:
                        h, rt, xe = prog_halo(R_OBS, shape, f * Mb, 0.0, a0, nu); C += h; edges.append(None if xe is None else xe * rt)
                    Mx = np.maximum(C, T); E = Mx - T
                    hmm = M652.delta_sigma(R_OBS, mc + Mx, RK, rmax=rta)
                    rec = dict(hmm=hmm.tolist(), dlog=float(np.mean(np.log10(hmm / base))), F=float(E.max()), F_over_T_at_rpeak=float(E.max() / max(T[int(np.argmax(E))], 1e-300)),
                               r_peak=float(R_OBS[int(np.argmax(E))]), edges_kpc=edges, maxrelE=float(np.max(E / np.maximum(T, 1e-300))),
                               ratio_C_T_50_100=[float(np.interp(r, R_OBS, C) / np.interp(r, R_OBS, T)) for r in RK],
                               cons_ok=bool(Mx.max() <= max(SUP_PER_COND * Mb, T.max()) * (1 + 1e-12)))
                    if kern == "s" and foot == "canonical" and nm in ("N2", "N3"):
                        rgp = np.geomspace(0.5, 2.0 * rta, 700)
                        Ti = np.interp(rgp, R_OBS, T); Ci = np.interp(rgp, R_OBS, Mx); mbi = np.interp(rgp, R_OBS, mc)
                        Mf, F2 = maxent_P2(rgp, mbi, Ti, Ci, rta)
                        p2 = M652.delta_sigma(rgp, mbi + Ti + Mf, RK, rmax=rta); b2 = M652.delta_sigma(rgp, mbi + Ti, RK, rmax=rta)
                        rec["P2_dlog"] = float(np.mean(np.log10(p2 / b2)))
                    row["sets"][nm] = rec
                # T-S2 (reported): disc with accreted fraction in 1% pieces, concentric memory
                if kern in KERN and lm in (10.0, 11.0):
                    ts2 = {}
                    for fa in (0.01, 0.03, 0.10):
                        n = int(round(fa / 0.01)); C = prog_halo(R_OBS, shape, (1 - fa) * Mb, 0.0, a0, nu)[0]
                        hs = prog_halo(R_OBS, shape, 0.01 * Mb, 0.0, a0, nu)[0]; C = C + n * hs
                        E = np.maximum(C - T, 0.0)
                        ts2[f"{fa}"] = {f"{r:g}": float(np.interp(r, R_OBS, E) / np.interp(r, R_OBS, T)) for r in (10.0, 30.0, 100.0)}
                        ts2[f"{fa}"].update({f"Vratio_{r:g}": float(math.sqrt((np.interp(r, R_OBS, mc + T + E)) / np.interp(r, R_OBS, mc + T))) for r in (10.0, 30.0, 100.0)})
                    row["TS2"] = ts2
                out.append(row)
                P(f"  T-K {kern} {foot[:3]} lMb {lm}: " + " ".join(f"{k} {v['dlog']:+.3f}" for k, v in row["sets"].items())
                  + (f" | P2 N2 {row['sets']['N2'].get('P2_dlog', float('nan')):+.3f}" if "P2_dlog" in row["sets"]["N2"] else ""))
    json.dump(C4.jclean(out), open(os.path.join(WORK, "tk.json"), "w"))

# ============================================================================================ cluster projection (CFG686/687 code via CFG721)
G = 6.674e-11; MSUN = 1.989e30; MPC = 3.0857e22; KG = MSUN / (3.0857e16) ** 2
RGRID = np.logspace(-3, np.log10(30), 3000); U_GRID = np.linspace(0, 1, 4001)
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:] * EDGES[:-1])
RK_GRID = RGRID * 1000.0


def sigma_proj(rhoL, r, R):
    umax = np.arccosh(r[-1] / R); u = U_GRID * umax; rr = R * np.cosh(u)
    rho_u = np.exp(np.interp(np.log(rr), np.log(r), np.log(np.maximum(rhoL, 1e-300))))
    return 2 * np.trapz(rho_u * rr * MPC, u)


def dsig_from_M(ML_msun):
    ML = ML_msun * MSUN; r = RGRID
    rhoL = np.gradient(ML, r * MPC) / (4 * np.pi * (r * MPC) ** 2)
    Sig = np.array([sigma_proj(rhoL, r, R) for R in RC])
    M2 = np.array([np.interp(R, r, ML) + np.trapz(4 * np.pi * (r[r > R] * MPC) ** 2 * rhoL[r > R] * (1 - np.sqrt(1 - (R / r[r > R]) ** 2)), r[r > R] * MPC) for R in RC])
    return (M2 / (np.pi * (RC * MPC) ** 2) - Sig) / KG


def law_M(Mb_msun, foot, nu):
    gb = G * Mb_msun * MSUN / (RGRID * MPC) ** 2
    return Mb_msun * nu(gb / A0SI[foot])


def lam_relation():
    """redMaPPer lambda for CFG687's clusters (CFG688's match rule) and the log-log relation lambda(M_gas(<1 Mpc)) on the matches."""
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    rm = np.array([list(map(float, l.split("\t"))) for l in open(os.path.join(LANES, "CFG688_richness_split", "redmapper_z004_06.tsv"))])
    n = len(d["z"]); lam = np.full(n, np.nan)
    for i in range(n):
        dd = np.degrees(np.arccos(np.clip(np.sin(np.radians(d["dec"][i])) * np.sin(np.radians(rm[:, 1])) + np.cos(np.radians(d["dec"][i])) * np.cos(np.radians(rm[:, 1])) * np.cos(np.radians(d["ra"][i] - rm[:, 0])), -1, 1))) * 60
        ok = (dd < 2.0) & (np.abs(rm[:, 2] - d["z"][i]) < 0.04)
        if ok.any(): lam[i] = rm[ok][np.argmin(dd[ok]), 3]
    mg1 = np.array([float(np.interp(1.0, RGRID, erass_gas(i, d))) for i in range(n)])
    m = np.isfinite(lam); p = np.polyfit(np.log10(mg1[m]), np.log10(lam[m]), 1)
    return lam, mg1, p


def erass_gas(i, d):
    R5, mgas = float(d["R500"][i]), float(d["mg"][i])
    r = RGRID; rc = 0.15 * R5; shape = (1 + (r / rc) ** 2) ** (-1.0); shape[r > 3.0] = 0
    dm = 4 * np.pi * (r * MPC) ** 2 * shape; Mm = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * MPC))]
    return Mm * (mgas / np.interp(R5, r, Mm))


DK = np.geomspace(1.0, 3000.0, 140)


def cluster_hmm(Mg, fs, z, Nmem, feet=FEET, kerns=None, brackets=True, mutate=True):
    """Mg: gas M(<r) on RGRID (Msun). Stars fs*Mg co-distributed (CFG687 primary). Returns dict of DeltaSigma arrays and diagnostics."""
    Mb = Mg * (1 + fs); Ms = fs * Mg; Mstar = float(Ms[-1])
    Ncum = np.interp(DK / 1000.0, RGRID, Mg) / Mg[-1]
    out = {}
    for kern in (kerns or KALL):
        nu = KALL[kern]
        for foot in feet:
            a0 = A0K[foot]
            Mlaw = law_M(Mb, foot, nu); T = Mlaw - Mb
            key = f"{kern}|{foot}"; out["law|" + key] = dsig_from_M(Mlaw)
            variants = {"primary": Nmem}
            if brackets and kern in KERN:
                variants.update({"Nx0.5": max(1.0, round(0.5 * Nmem)), "Nx2": round(2 * Nmem), "stripped": Nmem, "bcg_half": Nmem})
            for vn, Nv in variants.items():
                Nv = max(1, int(round(Nv)))
                if vn == "bcg_half":
                    mbcg = 0.5 * Mstar; nmem = max(1, Nv - 1); mi = 0.5 * Mstar / nmem
                else:
                    mbcg = 0.0; nmem = Nv; mi = Mstar / nmem
                sk = R_OBS; shape = M652.hern(sk, 1.0, RE_GAL)
                h, rt, xe = prog_halo(sk, shape, mi, z, a0, nu)
                if vn == "stripped":
                    C = nmem * float(h[-1]) * Ncum_full(Mg)
                else:
                    C = nmem * convolve_members(DK, Ncum, sk, h, RK_GRID)
                if mbcg > 0:
                    hb, _, _ = prog_halo(sk, shape, mbcg, z, a0, nu); C = C + np.interp(RK_GRID, sk, hb, left=0.0, right=hb[-1])
                Mx = np.maximum(C, T); E = Mx - T
                out[f"hmm|{key}|{vn}"] = dsig_from_M(Mb + Mx)
                out[f"diag|{key}|{vn}"] = dict(N=nmem, m_i=mi, edge_kpc=(None if xe is None else xe * rt), rta_i=rt, F=float(E.max()),
                                               F_over_S=float(E.max() / (SUP_PER_COND * Mstar)), C_tot=float(C[-1]), S_tot=SUP_PER_COND * Mstar,
                                               E_over_T_1Mpc=float(np.interp(1.0, RGRID, E) / np.interp(1.0, RGRID, T)),
                                               cons_ok=bool(Mx.max() <= max(SUP_PER_COND * Mstar, T.max()) * (1 + 1e-12)))
            if mutate and kern in KERN:                                                    # M-N1: one concentric progenitor = all stars
                rta1 = rta_of(Mstar / M652.F_COND_FLOOR / L.FB, z)
                c1, _ = L.phantom_trunc(RK_GRID / rta1, Ms, rta1, a0, nu, SUP_PER_COND * Mstar)
                Mx1 = np.maximum(c1, T)
                out[f"MN1|{key}"] = dict(maxrelE=float(np.max((Mx1 - T) / np.maximum(T, 1e-300))), ds=dsig_from_M(Mb + Mx1))
    return out


def Ncum_full(Mg):
    return Mg / Mg[-1]


# ============================================================================================ eRASS1 (CFG687)
if MODE == "erass":
    memcheck("erass")
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    lam, mg1, p = lam_relation()
    Nm = np.where(np.isfinite(lam), lam, 10 ** (p[0] * np.log10(mg1) + p[1]))
    P(f"  lambda: {int(np.isfinite(lam).sum())} matched; relation log lambda = {p[0]:.3f} log Mgas(<1Mpc) + {p[1]:.3f}; N_mem median {np.median(Nm):.1f} range {Nm.min():.1f}-{Nm.max():.1f}")
    json.dump(dict(lam=np.nan_to_num(lam, nan=-1).tolist(), mg1=mg1.tolist(), p=p.tolist(), Nmem=Nm.tolist()), open(os.path.join(WORK, "lambda.json"), "w"))
    res = []
    for i in range(len(d["mg"])):
        Mg = erass_gas(i, d)
        o = cluster_hmm(Mg, 0.20, float(d["z"][i]), float(Nm[i]))
        res.append(o)
        if (i + 1) % 20 == 0:
            P(f"  eRASS1 {i + 1}/{len(d['mg'])} ({time.time() - T0:.0f} s); last s|can primary F/S {o['diag|s|canonical|primary']['F_over_S']:.3f} "
              f"E/T(1 Mpc) {o['diag|s|canonical|primary']['E_over_T_1Mpc']:.3f} N {o['diag|s|canonical|primary']['N']}")
        if (i + 1) % 60 == 0:
            memcheck(f"erass {i + 1}")
    np.save(os.path.join(WORK, "erass.npy"), np.array(res, dtype=object), allow_pickle=True)

# ============================================================================================ ACCEPT (CFG686, gas construction as CFG721)
if MODE == "accept":
    memcheck("accept")
    from scipy.interpolate import PchipInterpolator
    c = 2.998e8; MP = 1.6726e-27
    zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
    DHb = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295); DMb = np.sqrt(7.942 ** 3 / (0.295 * DHb))
    pch = PchipInterpolator(np.r_[0, 0.295, zb], np.r_[0, DMb, DMr]); RD = 101.54 / 0.70
    DM = lambda z: pch(np.minimum(np.asarray(z, float), 2.33)) * RD
    prof = {}
    for l in open(os.path.join(EXT, "cfg686_inputs", "accept", "all_profiles.dat")):
        if l.startswith("#"): continue
        pp = l.split()
        try: prof.setdefault(pp[0], []).append([float(x) for x in pp[1:14]])
        except ValueError: pass
    C686 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))["clusters"]
    lamj = json.load(open(os.path.join(WORK, "lambda.json"))); p = lamj["p"]
    res = []
    for cl in C686:
        Pp = np.array(prof[cl["key"]]); Pp = Pp[np.argsort(Pp[:, 0])]; rin, rout, ne = Pp[:, 0], Pp[:, 1], Pp[:, 2]
        ok_ = ne > 0; rin, rout, ne = rin[ok_], rout[ok_], ne[ok_]
        zl = cl["z"]; zz = np.linspace(0, zl, 400); Ez = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7); DA_acc = np.trapz(1 / Ez, zz) * c / (70e3 / MPC) / MPC / (1 + zl)
        q = (float(DM(zl)) / (1 + zl)) / DA_acc; rin, rout, ne = rin * q, rout * q, ne * q ** -0.5
        rm = 0.5 * (rin + rout); rho = 1.17 * MP * ne * 1e6
        half = rm >= np.exp(0.5 * (np.log(rm[0]) + np.log(rm[-1]))); b0 = -np.polyfit(np.log(rm[half]), np.log(rho[half]), 1)[0]
        flag = not (b0 >= 1.5); b = 2.0 if flag else b0
        r = RGRID; rho_g = np.interp(r, rm, rho, left=rho[0], right=np.nan)
        out_ = r > rm[-1]; rho_g[out_] = rho[-1] * (r[out_] / rm[-1]) ** (-b); rho_g[r > 3.0] = 0.0
        Mg = np.r_[0, np.cumsum(0.5 * (4 * np.pi * (r[1:] * MPC) ** 2 * rho_g[1:] + 4 * np.pi * (r[:-1] * MPC) ** 2 * rho_g[:-1]) * np.diff(r) * MPC)] / MSUN
        mg1 = float(np.interp(1.0, RGRID, Mg)); Nm = 10 ** (p[0] * math.log10(mg1) + p[1])
        o = cluster_hmm(Mg, 0.20, zl, Nm); o["name"] = cl["name"]; o["Nmem"] = Nm
        res.append(o)
        P(f"  ACCEPT {cl['name']}: N_mem {Nm:.1f}; s|can F/S {o['diag|s|canonical|primary']['F_over_S']:.3f} E/T(1 Mpc) {o['diag|s|canonical|primary']['E_over_T_1Mpc']:.3f}")
    np.save(os.path.join(WORK, "accept.npy"), np.array(res, dtype=object), allow_pickle=True)

# ============================================================================================ eFEDS (CFG652 inputs; candidate B analytic baseline)
if MODE == "efeds":
    memcheck("efeds")
    W652 = os.path.join(EXT, "cfg652_work")
    I = np.load(os.path.join(W652, "cfg652_inputs.npz"))
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1]); n = len(I["z"])
    out = {}
    KE = dict(KALL, c540=C540.nu)
    arrs = {}
    for i in range(n):
        if I["Mcond"][i] <= 0: continue
        Mcd, Mh0, Rx, z = float(I["Mcond"][i]), float(I["Mhot"][i]), float(I["Rx_kpc"][i]), float(I["z"][i])
        mc, mh = M652.profiles(Mcd, Mh0, Rx, R_OBS, gas_trunc=2.0); core = mc + mh
        bc, sup, fret = M652.catchment(Mcd, float(mh[-1])); rta = rta_of(bc / L.FB, z)
        mbcg = min(float(I["Mbcg"][i]), Mcd); nmem = max(1, int(round(float(I["Nmem"][i])))); mi = (Mcd - mbcg) / nmem
        shape = M652.hern(R_OBS, 1.0, RE_GAL)
        Ncum = M652.hern(DK, 1.0, 0.5 * Rx)
        for kern, nu in KE.items():
            for foot in FEET:
                if kern == "c540" and foot != "canonical": continue
                a0 = A0K[foot]
                T, xe = L.phantom_trunc(R_OBS / rta, core, rta, a0, nu, sup)            # candidate B (analytic cut law)
                base = M652.delta_sigma(R_OBS, core + T, RCg, rmax=rta)
                arrs.setdefault(f"base|{kern}|{foot}", np.full((n, len(RCg)), np.nan))[i] = base
                if kern == "c540": continue
                C = np.zeros(len(R_OBS))
                if mi > 0:
                    h, rt, xm = prog_halo(R_OBS, shape, mi, z, a0, nu); C += nmem * convolve_members(DK, Ncum / Ncum[-1], R_OBS, h, R_OBS)
                if mbcg > 0:
                    hb, _, _ = prog_halo(R_OBS, shape, mbcg, z, a0, nu); C += hb
                Mx = np.maximum(C, T); E = Mx - T
                arrs.setdefault(f"hmm|{kern}|{foot}", np.full((n, len(RCg)), np.nan))[i] = M652.delta_sigma(R_OBS, core + Mx, RCg, rmax=rta)
                arrs.setdefault(f"F_over_S|{kern}|{foot}", np.full(n, np.nan))[i] = E.max() / (SUP_PER_COND * Mcd)
                arrs.setdefault(f"cons|{kern}|{foot}", np.full(n, np.nan))[i] = float(Mx.max() <= max(sup, T.max()) * (1 + 1e-12))
                if kern in KERN:                                                       # M-N1: one concentric progenitor = all condensed
                    rta1 = rta_of(Mcd / M652.F_COND_FLOOR / L.FB, z)
                    c1, _ = L.phantom_trunc(R_OBS / rta1, mc, rta1, a0, nu, SUP_PER_COND * Mcd)
                    Mx1 = np.maximum(c1, T)
                    arrs.setdefault(f"MN1|{kern}|{foot}", np.full(n, np.nan))[i] = float(np.max((Mx1 - T) / np.maximum(T, 1e-300)))
                    arrs.setdefault(f"MN1ds|{kern}|{foot}", np.full((n, len(RCg)), np.nan))[i] = M652.delta_sigma(R_OBS, core + Mx1, RCg, rmax=rta)
        if (i + 1) % 20 == 0:
            P(f"  eFEDS {i + 1}/{n} ({time.time() - T0:.0f} s)")
    np.savez(os.path.join(WORK, "efeds.npz"), **{k.replace("|", "__"): v for k, v in arrs.items()})

# ============================================================================================ score
if MODE == "score":
    from scipy.stats import chi2 as CHI2
    RES = {"lane": "CFG726", "criteria": "78e51c189", "post_hoc": True}
    CHK = {}

    def check(name, ok, msg):
        CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")

    P(__doc__.split("Stages")[0].strip())
    # ---------------- T-K
    TK = json.load(open(os.path.join(WORK, "tk.json")))
    P("\n== T-K KiDS f30 early/late at matched M_b (obs +0.280 +- 0.083; CFG658 law -0.027); prediction = -0.027 + D_MM(early); late N = 1")
    TKR = {}
    for kern in KALL:
        for foot in FEET:
            rows = [r for r in TK if r["kern"] == kern and r["foot"] == foot]
            for nm in rows[0]["sets"]:
                dl = float(np.mean([r["sets"][nm]["dlog"] for r in rows])); pred = -0.027 + dl
                rec = dict(D_MM=dl, pred=pred, Z=(0.280 - pred) / 0.083, pass_=bool(abs(pred - 0.280) < 2 * 0.083),
                           per_mass=[r["sets"][nm]["dlog"] for r in rows], F_over_T_peak=[r["sets"][nm]["F_over_T_at_rpeak"] for r in rows],
                           r_peak_kpc=[r["sets"][nm]["r_peak"] for r in rows], C_over_T_50_100=[r["sets"][nm]["ratio_C_T_50_100"] for r in rows],
                           edges_kpc=[r["sets"][nm]["edges_kpc"] for r in rows], cons_ok=all(r["sets"][nm]["cons_ok"] for r in rows))
                if "P2_dlog" in rows[0]["sets"][nm]:
                    rec["P2_D_MM"] = float(np.mean([r["sets"][nm]["P2_dlog"] for r in rows])); rec["P2_pred"] = -0.027 + rec["P2_D_MM"]
                TKR[f"{kern}|{foot}|{nm}"] = rec
            if kern in KERN:
                P(f"  {kern} {foot[:3]}: " + "  ".join(f"{nm} {TKR[f'{kern}|{foot}|{nm}']['pred']:+.3f} (Z {TKR[f'{kern}|{foot}|{nm}']['Z']:+.2f})" for nm in rows[0]["sets"])
                  + f"  | PRIMARY N2 -> {'PASS' if TKR[f'{kern}|{foot}|N2']['pass_'] else 'FAIL'}")
    for nm in ("N2", "N3"):
        r_ = TKR[f"s|canonical|{nm}"]
        P(f"  P2 bracket (reported, s can) {nm}: pred {r_['P2_pred']:+.3f} vs P1 {r_['pred']:+.3f}")
    mn1 = max(abs(TKR[f"{k}|{f}|N1"]["D_MM"]) for k in KALL for f in FEET)
    mn1E = max(r["sets"]["N1"]["maxrelE"] for r in TK)
    madd = max(r["sets"][nm]["maxrelE"] for r in TK if r["kern"] == "add" for nm in r["sets"])
    check("M-N1 T-K: N = 1 gives the plain law exactly", mn1 <= 1e-12 and mn1E <= 1e-12, f"max |D_MM| {mn1:.1e}, max E/T {mn1E:.1e}")
    check("M-ADD T-K: additive law gives zero excess", madd <= 1e-12, f"max E/T {madd:.1e} (all N sets)")
    check("C-CONS T-K", all(v["cons_ok"] for v in TKR.values()), "max(C,T) <= max(S_tot, max T)")
    RES["T_K"] = TKR
    # T-S2
    P("\n== T-S2 (reported vulnerability): disc + accreted fraction in 1% pieces, concentric memory; E/T and V_HMM/V_law at 10/30/100 kpc")
    TS2 = {}
    for r in TK:
        if "TS2" in r:
            TS2[f"{r['kern']}|{r['foot']}|{r['lMb']}"] = r["TS2"]
            P(f"  {r['kern']} {r['foot'][:3]} lMb {r['lMb']}: " + "; ".join(f"f_acc {fa}: E/T " + "/".join(f"{v[k]:.3f}" for k in ('10', '30', '100'))
                                                                       + " V ratio " + "/".join(f"{v['Vratio_' + k]:.3f}" for k in ('10', '30', '100')) for fa, v in r["TS2"].items()))
    RES["T_S2"] = TS2
    RES["T_S"] = dict(verdict="PASS (identity: discs N = 1, H-MM = plain law; RAR rms 0.100 dex unchanged)", checked_by="M-N1")

    # ---------------- T-R eRASS1
    d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
    ER = list(np.load(os.path.join(WORK, "erass.npy"), allow_pickle=True)); lamj = json.load(open(os.path.join(WORK, "lambda.json")))
    D, E = d["D"], d["E"]; W = np.where(E > 0, 1 / E ** 2, 0); n = len(D)
    order = np.argsort(d["ra"]); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
    BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
    mg = d["mg"]; q = np.quantile(mg, [0, 1 / 3, 2 / 3, 1]); tid = np.clip(np.digitize(mg, q[1:-1]), 0, 2)

    def A_of(sel, Pm):
        return {b: (W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum() for b, j in BANDS.items()}

    def jk(fun):
        full = fun(np.ones(n, bool)); reps = [fun(patch != p) for p in range(30)]
        return {k: (float(full[k]), float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}

    def slope(sel, arr):
        xs, ys = [], []
        for t in range(3):
            s = sel & (tid == t); j = BANDS["OUTER"]; v = (W[s][:, j] * arr[s][:, j]).sum() / W[s][:, j].sum()
            if v <= 0: return np.nan
            xs.append(np.log10(np.median(mg[s]))); ys.append(np.log10(v))
        return np.polyfit(xs, ys, 1)[0]

    P(f"\n== eRASS1 members: lambda matched {sum(1 for x in lamj['lam'] if x > 0)}; relation log lambda = {lamj['p'][0]:.3f} log Mgas(<1Mpc) {lamj['p'][1]:+.3f}; "
      f"N_mem median {np.median(lamj['Nmem']):.1f}")
    PM0 = np.array([o["law|mono|canonical"] for o in ER])
    rel = np.median(np.abs(PM0 / d["PL"] - 1), axis=0)
    A0m = jk(lambda s: A_of(s, PM0)); APL = jk(lambda s: A_of(s, d["PL"]))
    dA = max(abs(A0m[b][0] - APL[b][0]) for b in BANDS)
    check("M0 eRASS1: plain law reproduced (median per-bin <= 1%, band A <= 0.01)", rel.max() <= 0.01 and dA <= 0.01, f"median |rel| max {rel.max():.2e}; max |dA| {dA:.4f}")
    w1 = max(float(np.max(np.abs(o[f"MN1|{k}|{f}"]["ds"] / o[f"law|{k}|{f}"] - 1))) for o in ER for k in KERN for f in FEET)
    e1 = max(o[f"MN1|{k}|{f}"]["maxrelE"] for o in ER for k in KERN for f in FEET)
    check("M-N1 eRASS1: single concentric progenitor = plain law", w1 <= 1e-12 and e1 <= 1e-12, f"max |rel dS| {w1:.1e}, max E/T {e1:.1e}")
    wa = max(float(np.max(np.abs(o[f"hmm|add|{f}|primary"] / o[f"law|add|{f}"] - 1))) for o in ER for f in FEET)
    ea = max(o[f"diag|add|{f}|primary"]["F"] for o in ER for f in FEET)
    check("M-ADD eRASS1: additive law gives zero excess", wa <= 1e-12 and ea == 0.0, f"max |rel dS| {wa:.1e}, max F {ea:.1e}")
    check("C-CONS eRASS1", all(o[k]["cons_ok"] for o in ER for k in o if k.startswith("diag|")), "max(C,T) <= max(S_tot, max T)")
    s_obs = jk(lambda s: {"s": slope(s, D)})["s"]
    TR = {}
    P("\n== T-R eRASS1 318: A = obs / H-MM (jackknife 30 patches); pass |A_MID-1| < 2 sig AND |A_OUTER-1| < 2 sig")
    for kern in KERN:
        for foot in FEET:
            PLk = np.array([o[f"law|{kern}|{foot}"] for o in ER]); Alaw = jk(lambda s: A_of(s, PLk)); s_law = slope(np.ones(n, bool), PLk)
            for vn in ("primary", "Nx0.5", "Nx2", "stripped", "bcg_half"):
                Ph = np.array([o[f"hmm|{kern}|{foot}|{vn}"] for o in ER]); A = jk(lambda s: A_of(s, Ph))
                zmid = (A["MID"][0] - 1) / A["MID"][1]; zout = (A["OUTER"][0] - 1) / A["OUTER"][1]
                ok = abs(zmid) < 2 and abs(zout) < 2; s_h = slope(np.ones(n, bool), Ph)
                expl = abs(s_obs[0] - s_h) < 2 * s_obs[1] and (s_h - s_law) >= 0.21
                FS = np.array([o[f"diag|{kern}|{foot}|{vn}"]["F_over_S"] for o in ER]); ET = np.array([o[f"diag|{kern}|{foot}|{vn}"]["E_over_T_1Mpc"] for o in ER])
                At = [float((W[tid == t][:, 3:6] * D[tid == t][:, 3:6]).sum() / (W[tid == t][:, 3:6] * Ph[tid == t][:, 3:6]).sum()) for t in range(3)]
                AtO = [float((W[tid == t][:, 6:8] * D[tid == t][:, 6:8]).sum() / (W[tid == t][:, 6:8] * Ph[tid == t][:, 6:8]).sum()) for t in range(3)]
                TR[f"{kern}|{foot}|{vn}"] = dict(A=A, A_law=Alaw, Z_mid=zmid, Z_outer=zout, pass_=bool(ok), s_HMM=float(s_h), s_law=float(s_law), s_obs=s_obs,
                                                 explains_090=bool(expl), F_over_S_median=float(np.median(FS)), E_over_T_1Mpc_median=float(np.median(ET)),
                                                 A_tercile_MID=At, A_tercile_OUTER=AtO)
                P(f"  {kern} {foot[:3]} {vn:9s}: F/S med {np.median(FS):.3f}, E/T(1Mpc) med {np.median(ET):.2f}; A INNER {A['INNER'][0]:.2f}+-{A['INNER'][1]:.2f} "
                  f"MID {A['MID'][0]:.2f}+-{A['MID'][1]:.2f} (Z {zmid:+.1f}) OUTER {A['OUTER'][0]:.2f}+-{A['OUTER'][1]:.2f} (Z {zout:+.1f}) -> {'PASS' if ok else 'FAIL'}"
                  f" | slope {s_h:.2f} (law {s_law:.2f}, obs {s_obs[0]:.2f}+-{s_obs[1]:.2f}) explains: {expl} | MID A by tercile " + " ".join(f"{x:.2f}" for x in At))
            P(f"     law {kern} {foot[:3]}: A MID {Alaw['MID'][0]:.2f}+-{Alaw['MID'][1]:.2f} OUTER {Alaw['OUTER'][0]:.2f}+-{Alaw['OUTER'][1]:.2f}")
    RES["T_R"] = TR

    # ---------------- T-A ACCEPT
    C686 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))
    cls = C686["clusters"]; AC = list(np.load(os.path.join(WORK, "accept.npy"), allow_pickle=True))
    D_ = np.nan_to_num(np.array([x["dsig"] for x in cls])); E_ = np.array([x["err"] for x in cls]); W_ = np.where(np.isfinite(E_) & (E_ > 0), 1 / E_ ** 2, 0)
    worst = 0.0
    for foot in FEET:
        PM = np.array([o[f"law|mono|{foot}"] for o in AC]); PS = np.array([x["pred"][f"{foot}|b+0.0|f0.20"] for x in cls])
        worst = max(worst, float(np.max(np.abs(PM / PS - 1))))
    check("M0 ACCEPT: plain law reproduced (<= 1% every bin)", worst <= 0.01, f"max |rel| {worst:.2e}")
    w1 = max(float(np.max(np.abs(o[f"MN1|{k}|{f}"]["ds"] / o[f"law|{k}|{f}"] - 1))) for o in AC for k in KERN for f in FEET)
    wa = max(float(np.max(np.abs(o[f"hmm|add|{f}|primary"] / o[f"law|add|{f}"] - 1))) for o in AC for f in FEET)
    check("M-N1 + M-ADD ACCEPT", w1 <= 1e-12 and wa <= 1e-12, f"N1 max |rel| {w1:.1e}; ADD max |rel| {wa:.1e}")

    def bandA(Pm, sel):
        o_ = {}
        for b, j in BANDS.items():
            num = (W_[sel][:, j] * D_[sel][:, j]).sum(); den = (W_[sel][:, j] * Pm[sel][:, j]).sum(); o_[b] = num / den if den != 0 else np.nan
        return o_
    TA = {}
    P("\n== T-A ACCEPT 8 clusters (bootstrap 1000, seed 1); N_mem " + " ".join(f"{o['Nmem']:.0f}" for o in AC))
    for kern in KERN:
        for foot in FEET:
            for vn in ("primary", "Nx0.5", "Nx2", "stripped", "bcg_half"):
                Pm = np.array([o[f"hmm|{kern}|{foot}|{vn}"] for o in AC])
                A = bandA(Pm, np.arange(len(cls))); rb = np.random.default_rng(1)
                boots = [bandA(Pm, rb.integers(0, len(cls), len(cls))) for _ in range(1000)]
                sig = {b: float(np.nanstd([bb[b] for bb in boots])) for b in BANDS}
                zm, zo = (A["MID"] - 1) / sig["MID"], (A["OUTER"] - 1) / sig["OUTER"]
                ok = abs(zm) < 2 and abs(zo) < 2
                TA[f"{kern}|{foot}|{vn}"] = dict(A={b: [float(A[b]), sig[b]] for b in BANDS}, Z_mid=float(zm), Z_outer=float(zo), pass_=bool(ok))
                P(f"  {kern} {foot[:3]} {vn:9s}: A INNER {A['INNER']:.2f}+-{sig['INNER']:.2f} MID {A['MID']:.2f}+-{sig['MID']:.2f} (Z {zm:+.1f}) "
                  f"OUTER {A['OUTER']:.2f}+-{sig['OUTER']:.2f} (Z {zo:+.1f}) -> {'PASS' if ok else 'FAIL'}")
    RES["T_A"] = TA

    # ---------------- T-E eFEDS (CFG652 score code, as CFG721)
    W652 = os.path.join(EXT, "cfg652_work")
    I0 = np.load(os.path.join(W652, "cfg652_inputs.npz")); D0 = np.load(os.path.join(W652, "cfg652_esd.npz"))
    MD = np.load(os.path.join(W652, "cfg652_models.npz")); EM = np.load(os.path.join(WORK, "efeds.npz"))
    keep = I0["Mcond"] > 0
    wb = float(np.nanmax(np.abs(EM["base__c540__canonical"][keep] / MD["canonical__x1__b"][keep] - 1)))
    check("M0 eFEDS: analytic candidate B (C540.nu) vs cfg652_models (b) canonical x1 (<= 2%)", wb <= 0.02, f"max |rel| {wb:.3e}")
    w1 = max(float(np.nanmax(np.abs(EM[f"MN1ds__{k}__{f}"][keep] / EM[f"base__{k}__{f}"][keep] - 1))) for k in KERN for f in FEET)
    e1 = max(float(np.nanmax(EM[f"MN1__{k}__{f}"][keep])) for k in KERN for f in FEET)
    wa = max(float(np.nanmax(np.abs(EM[f"hmm__add__{f}"][keep] / EM[f"base__add__{f}"][keep] - 1))) for f in FEET)
    check("M-N1 + M-ADD eFEDS", w1 <= 1e-12 and e1 <= 1e-12 and wa <= 1e-12, f"N1 max |rel| {w1:.1e} (E/T {e1:.1e}); ADD max |rel| {wa:.1e}")
    check("C-CONS eFEDS", all(np.nanmin(EM[f"cons__{k}__{f}"][keep]) == 1.0 for k in KALL for f in FEET), "max(C,T) <= max(supply, max T)")
    RB = np.geomspace(30, 3000, 13); RCg = np.sqrt(RB[1:] * RB[:-1])
    USE = (RCg >= 50) & (RCg <= 1000); BAND = (RCg >= 250) & (RCg <= 1000); NPATCH = 30
    Dd = {k: (D0[k][keep] if k in ("WG", "WX", "WW", "NN", "pg") else D0[k]) for k in D0.files}

    def esd(sel_g, sel_r):
        Wg = Dd["WW"][sel_g].sum(0); Wr = Dd["rWW"][sel_r].sum(0)
        g = Dd["WG"][sel_g].sum(0) / np.where(Wg > 0, Wg, np.nan); r = Dd["rWG"][sel_r].sum(0) / np.where(Wr > 0, Wr, np.nan)
        boost = (Dd["NN"][sel_g].sum(0) / max(sel_g.sum(), 1)) / (Dd["rNN"][sel_r].sum(0) / max(sel_r.sum(), 1))
        return boost * g - r

    def model_stack(arr, sel_g):
        Wm = Dd["WW"][sel_g]
        return (Wm * arr[sel_g]).sum(0) / np.where(Wm.sum(0) > 0, Wm.sum(0), np.nan)
    ng = int(keep.sum()); allg = np.ones(ng, bool); allr = np.ones(len(Dd["rz"]), bool)
    vals = np.array([esd(Dd["pg"] != p, Dd["pr"] != p)[USE] for p in range(NPATCH)]); mv = vals.mean(0)
    Cv = (NPATCH - 1) / NPATCH * (vals - mv).T @ (vals - mv)
    nb = int(USE.sum()); hart = (NPATCH - nb - 2) / (NPATCH - 1); Ci = np.linalg.inv(Cv) * hart
    obs = esd(allg, allr)
    aout = lambda o, m: float(np.log10(np.sum(o[BAND]) / np.sum(m[BAND])))
    ms = model_stack(MD["canonical__x1__a"][keep], allg); dd = obs[USE] - ms[USE]
    check("eFEDS score code reproduces CFG652's chi2 (a, canonical, x1) to 0.01", abs(float(dd @ Ci @ dd) - 22.895815392627757) < 0.01, f"{float(dd @ Ci @ dd):.4f} vs 22.8958")
    TE = {}
    P("\n== T-E eFEDS 131 groups; pass chi2 p >= 0.01 AND |A_out| < 2 sigma")
    for kern in KERN:
        for foot in FEET:
            for tag in ("base", "hmm"):
                arr = EM[f"{tag}__{kern}__{foot}"][keep]; ms = model_stack(arr, allg); dd = obs[USE] - ms[USE]
                ch = float(dd @ Ci @ dd); p = float(CHI2.sf(ch, nb)); A = aout(obs, ms)
                Aj = np.array([aout(esd(Dd["pg"] != qq, Dd["pr"] != qq), model_stack(arr, Dd["pg"] != qq)) for qq in range(NPATCH)])
                sA = float(math.sqrt((NPATCH - 1) / NPATCH * np.sum((Aj - Aj.mean()) ** 2)))
                ok = p >= 0.01 and abs(A) < 2 * sA
                rec = dict(chi2=ch, p=p, A_out=A, sA=sA, pass_=bool(ok), model=ms[USE].tolist())
                if tag == "hmm":
                    rec["F_over_S_median"] = float(np.nanmedian(EM[f"F_over_S__{kern}__{foot}"][keep])); TE[f"{kern}|{foot}"] = rec
                else:
                    TE[f"law|{kern}|{foot}"] = rec
                P(f"  {kern} {foot[:3]} {'H-MM' if tag == 'hmm' else 'law (cand. B)'}: chi2 {ch:.1f}/{nb} p {p:.3g}; A_out {A:+.3f} +- {sA:.3f} -> {'PASS' if ok else 'FAIL'}"
                  + (f"; F/S median {rec['F_over_S_median']:.3f}" if tag == "hmm" else ""))
                P("     model " + " ".join(f"{x:6.1f}" for x in ms[USE]) + " | obs " + " ".join(f"{x:6.1f}" for x in obs[USE]))
    RES["T_E"] = TE
    RES["T_X"] = "NOT RUN"; RES["T_B"] = "NOT RUN"

    # ---------------- verdict
    P("\n== VERDICT per kernel (both footings; T-X and T-B NOT RUN block a full PASS)")
    V = {}
    for kern in KERN:
        fails = []
        for foot in FEET:
            if not TKR[f"{kern}|{foot}|N2"]["pass_"]: fails.append(f"T-K[{foot[:3]}]")
            if not TR[f"{kern}|{foot}|primary"]["pass_"]: fails.append(f"T-R[{foot[:3]}]")
            if not TA[f"{kern}|{foot}|primary"]["pass_"]: fails.append(f"T-A[{foot[:3]}]")
            if not TE[f"{kern}|{foot}"]["pass_"]: fails.append(f"T-E[{foot[:3]}]")
        V[kern] = ("H-MM FAILS: " + ", ".join(fails)) if fails else "H-MM PASSES THE RUN TARGETS (T-X, T-B NOT RUN)"
        P(f"  kernel {kern}: {V[kern]}")
    RES["verdict"] = V; RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
    nf = sum(1 for c in CHK.values() if not c["ok"])
    P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass. kappa fitted; cold energy mass required; not theory closed.")
    json.dump(C4.jclean(RES), open(os.path.join(HERE, "cfg726_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg726.out"), "w").write("\n".join(LOG) + "\n")
    sys.exit(1 if nf else 0)

if MODE != "score":
    open(os.path.join(HERE, f"cfg726_{MODE}.log"), "w").write("\n".join(LOG) + f"\nelapsed {time.time() - T0:.0f} s\n")
