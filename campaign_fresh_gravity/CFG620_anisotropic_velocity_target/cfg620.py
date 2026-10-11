#!/usr/bin/env python3
"""CFG620: an anisotropic, self-consistent velocity-relaxation target (FIX-2 successor test). FROZEN_CRITERIA.md (93abcbeb6).

Route ME: the maximum-entropy exact stationary F(E, L) of the law's truncated settled halo (no isotropy, no energy constraint;
beta is an output). Part S: exact law (unsoftened, units r_M). Part N: the bench's own softened equilibrium field. LP isotropy and
mirror tests (Part S). Sympy K1-K5, numeric K6 (cfg620_sympy.py). Bench = CFG544's toy imported unchanged through CFG554's
module: FIX-A (BGK toward the ME target conditional), FIX-AG (anisotropic Gaussian OU, reported), FIX-2 (comparator = forced
isotropy). Cells: MW-like, cluster-like, compact-elliptical-like (b <= 0.1 r_M) x can / alt.
Kernel: the EXPONENTIAL RAR form nu(y) = 1/(1 - exp(-sqrt y)) (THEORY_v1 A1 naming; not the repaired nu_mono).
kappa = 1/2 FITTED; footings never pooled; candidate B; G9; no EFE; cold energy mass required; not "theory closed".
CFG620_MUTATE=1 -> MI (reads the main JSON), MF (mirrored-anisotropy arm), MT (target hot); exit 1 iff all teeth bite.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg620.py      (4 processes)
"""
import os, sys, json, math, time, importlib.util, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ["CFG544_MUTATE"] = "0"; os.environ["CFG550_MUTATE"] = "0"; os.environ["CFG554_MUTATE"] = "0"
import numpy as np
from multiprocessing import Pool

warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious Accelerate FP flags (CFG559 disclosure)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg620_lib as L
import cfg620_sympy as SY


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, "..", rel))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


T554 = _load("cfg554", os.path.join("CFG554_selfconsistent_jeans_target", "cfg554.py"))
T544 = T554.T544
sys.path.insert(0, os.path.join(HERE, "..", "CFG541_cold_energy_equations_precise"))
_cwd = os.getcwd()
os.chdir(os.path.join(HERE, "..", "CFG541_cold_energy_equations_precise"))
import cfg541 as M541                                                     # noqa: E402  (read-only import)
os.chdir(_cwd)
J544 = json.load(open(os.path.join(HERE, "..", "CFG544_settling_kinetic_consistency", "cfg544_results.json")))
J559K = os.path.join(HERE, "..", "CFG559_kinetic_settled_profile", "cfg559_kids_results.json")

MUT = os.environ.get("CFG620_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
NPROC = 4
RMIN, EPS, NB, NPART = T544.RMIN, T544.EPS, T544.NB, T544.NPART
Mb_enc, Mph_enc = T544.Mb_enc, T544.Mph_enc
G_SI, MSUN, KPC, GYR = T544.G_SI, T544.MSUN, T544.KPC, T544.GYR
FOOT = T544.FOOT
C2_CELL = {"MW_can": 0.255, "MW_alt": 0.333, "cluster_can": 0.445, "cluster_alt": 0.539}   # CFG554/558 allowance (report)
NBIN_LIB, SUB_LIB = 120, 2
DYN = 1e-9                                        # library lower limit: rho_ph >= DYN * max (disclosed numerical rule)
OUT = []
RES = {"lane": "CFG620", "mutate": MUT, "criteria_commit": "93abcbeb6 (committed as CFG598; renamed CFG620 for an ID collision)", "date": "2026-10-10",
       "settings": dict(kappa=0.5, footings=FOOT, kernel="exponential RAR nu(y)=1/(1-exp(-sqrt y)) (THEORY_v1 A1 naming)",
                        toy="CFG544 cfg544.py imported unchanged via CFG554", N=NPART, eps_over_rstar=EPS, rmin=RMIN,
                        seed=T544.SEED, library=dict(bins=NBIN_LIB, sub=SUB_LIB, ntheta=L.NTH, dyn_floor=DYN),
                        inputs="CFG541 JSON + CFG541 Model (compact cell), CFG544/554/559 JSON (read only)")}


def log(s=""):
    print(s, flush=True); OUT.append(s)


# ============================================================================================================ cells
def compact_cell(foot):
    a0 = FOOT[foot]; Mb_sun, a_kpc = 1.0e11, 1.0
    f = M541.fret_census(Mb_sun)[0]
    mod = M541.Model(Mb_sun, a_kpc, a0, f)
    rstar = mod.analytic_rstar(); rstar_kpc = rstar / KPC
    Mb = Mb_sun * MSUN; Vf = (G_SI * Mb * a0) ** 0.25; rM = math.sqrt(G_SI * Mb / a0)
    return dict(sys="compact", foot=foot, Vf_kms=Vf / 1e3, rstar_kpc=rstar_kpc, fret=f, Mb=rM / rstar, a=a_kpc / rstar_kpc,
                rta=mod.rta / rstar, Mcat=mod.Mcat / mod.Mb * rM / rstar, tu_Gyr=rstar / Vf / GYR, dt=1e-3,
                Vf2_SI=Vf ** 2, rstar_SI=rstar, rM_kpc=rM / KPC, b_over_rM=a_kpc * KPC / rM), mod


def all_cells():
    cells = {}
    for s in ("MW", "cluster"):
        for f in FOOT:
            c = T544.make_cell(s, f); c["rM_kpc"] = math.sqrt(G_SI * T544.SYS[s]["Mb"] * MSUN / FOOT[f]) / KPC
            c["b_over_rM"] = 0.0 if T544.SYS[s]["a_kpc"] is None else T544.SYS[s]["a_kpc"] / c["rM_kpc"]
            cells[f"{s}_{f}"] = c
    for f in FOOT:
        cells[f"compact_{f}"] = compact_cell(f)[0]
    return cells


def compact_dW(foot):
    """CFG541's drift-only release for the compact cell (same computation as CFG541's dW_per_mass), per V_f^2."""
    c, mod = compact_cell(foot)
    r = mod.run(alpha=1.0)
    m0 = mod.rhoc0 * mod.V
    Wi, Ki = mod.energy(m0); Wf, Kf = mod.energy(r["m"])
    return (Wi - Wf) / mod.Mcat / c["Vf2_SI"]


def dW541(k, c):
    if c["sys"] == "compact":
        return compact_dW(c["foot"])
    j = T544.J541["one_d"][c["foot"]][c["sys"]]
    return j["dW_per_mass"] / c["Vf2_SI"]


# ============================================================================================================ Part S (exact law)
def law_S(b, R):
    """units G = M_b = r_M = a0 = 1. Hernquist b (0 = point). Returns Mb(r), Mph(r) (untruncated) and real-mass g(r)."""
    def Mb(r):
        r = np.asarray(r, float); return np.ones_like(r) if b == 0 else r ** 2 / (r + b) ** 2
    def Mph(r):
        r = np.asarray(r, float); return Mb(r) / np.expm1(1.0 / (r + b))
    MR = float(Mph(np.array([R]))[0])
    def g(r):
        r = np.asarray(r, float); return (Mb(r) + np.where(r < R, Mph(np.minimum(r, R)), MR)) / r ** 2
    return Mb, Mph, g


def lib_floor(rho_fun, rlo0, rhi):
    rr = np.geomspace(rlo0, rhi, 20001); rho = rho_fun(rr)
    return float(max(rlo0, rr[np.argmax(rho >= DYN * rho.max())]))


def build_target(g, Mfun, rlo, rhi):
    F = L.Field(g, rlo, rhi)
    lib = L.Library(F, rlo, rhi, nb=NBIN_LIB, sub=SUB_LIB)
    M = L.bin_masses(lib, Mfun)
    sol = L.maxent(lib, M)
    s2r, s2t, beta, Pr, Pt = L.moments(lib, sol["y"], M)
    rc = np.exp(0.5 * (lib.ub[1:] + lib.ub[:-1]))
    rho_b = M / (4 * math.pi / 3 * np.diff(np.exp(lib.ub) ** 3))
    return dict(F=F, lib=lib, M=M, sol=sol, s2r=s2r, s2t=s2t, beta=beta, rc=rc, rho_b=rho_b)


def fine_recon(T, nsub=4):
    """report only: density on a 4x finer radial grid from the solved F (cell masses re-binned by time fractions)."""
    lib = T["lib"]; F = lib.F
    ubf = np.linspace(lib.ub[0], lib.ub[-1], lib.nb * nsub + 1)
    th = (np.arange(L.NTH) + 0.5) * math.pi / L.NTH
    rbar = 0.5 * (lib.rp + lib.ra); dl = 0.5 * (lib.ra - lib.rp)
    Mf = np.zeros(ubf.size - 1); y = T["sol"]["y"]
    for s in range(0, lib.rp.size, 4000):
        sl = slice(s, min(s + 4000, lib.rp.size))
        r = rbar[sl, None] - dl[sl, None] * np.cos(th)[None, :]
        ra = lib.ra[sl, None]; Lc = lib.L[sl, None]
        vr2 = np.maximum(2 * (F.phi(ra) + Lc ** 2 / (2 * ra ** 2) - F.phi(r) - Lc ** 2 / (2 * r ** 2)), 1e-300)
        dt = dl[sl, None] * np.sin(th)[None, :] / np.sqrt(vr2); dt /= dt.sum(1, keepdims=True)
        k = np.clip(np.searchsorted(ubf, np.log(r)) - 1, 0, Mf.size - 1)
        np.add.at(Mf, k.ravel(), (dt * y[sl, None]).ravel())
    return ubf, Mf


def part_S_cell(arg):
    k, c = arg
    lines = []
    if True:
        b = c["b_over_rM"]; R = 1.0 / c["Mb"]                     # r_* / r_M  (c['Mb'] = r_M / r_*)
        Mb, Mph, g = law_S(b, R)
        rho = lambda r: np.gradient(Mph(r), r) / np.asarray(r) ** 2
        rlo = lib_floor(rho, 0.005, R)
        t0 = time.time()
        T = build_target(g, Mph, rlo, R)
        rc, beta, s2r, s2t, rb = T["rc"], T["beta"], T["s2r"], T["s2t"], T["rho_b"]
        rep = rc >= 0.05
        kpk = int(np.argmax(np.where(rep, rb, -1)))
        hollow = bool(np.any(np.diff(rb[rep]) > 0))
        r_pk = float(rc[kpk]) if hollow else None
        hol = np.where(rep & (rc < rc[kpk]))[0] if hollow else np.array([], int)
        outer = np.where((rc > (rc[kpk] if hollow else 0.05)) & (rc < 0.9 * R))[0]
        # cusp-slope-anisotropy line (report only): gamma = -dln rho/dln r from the exact law
        rg = np.geomspace(rlo * 0.9, R * 1.01, 40001); lnrho = np.log(np.maximum(rho(rg), 1e-300))
        gam = -np.interp(np.log(rc), np.log(rg), np.gradient(lnrho, np.log(rg)))
        gd = [dict(r=float(rc[i]), beta=float(beta[i]), gamma_half=float(gam[i] / 2)) for i in hol[::max(1, hol.size // 6)]]
        gdsai_viol = int(np.sum(beta[hol] > gam[hol] / 2 + 1e-3)) if hol.size else 0
        ubf, Mf = fine_recon(T)
        Mtrue = np.diff(Mph(np.exp(ubf)))
        okf = (np.exp(0.5 * (ubf[1:] + ubf[:-1])) >= 0.05) & (Mtrue > 0)
        fine_dev = float(np.median(np.abs(np.log10(np.maximum(Mf[okf], 1e-300) / Mtrue[okf]))))
        edge = rc > 0.97 * R
        rec = dict(b_over_rM=b, R_over_rM=R, lib_rlo=rlo, solver_err=T["sol"]["err"], solver_it=T["sol"]["it"],
                   self_consistent=bool(T["sol"]["err"] <= 1e-3), Fmin_positive=bool(np.all(T["sol"]["F"] > 0)),
                   hollow=hollow, r_pk_over_rM=r_pk, n_hollow_bins=int(hol.size),
                   beta_hollow_median=float(np.median(beta[hol])) if hol.size else None,
                   beta_hollow_min=float(np.min(beta[hol])) if hol.size else None,
                   beta_bulk_median=float(np.median(beta[(rc > (r_pk or 0.05)) & (rc < 0.5 * R)])),
                   beta_bulk_range=[float(np.min(beta[(rc > (r_pk or 0.05)) & (rc < 0.5 * R)])),
                                    float(np.max(beta[(rc > (r_pk or 0.05)) & (rc < 0.5 * R)]))],
                   edge_sr2_over_st2_last_bin=float(s2r[-1] / s2t[-1]), edge_beta_last_bin=float(beta[-1]),
                   edge_sr2_over_st2_outer3pct=float(np.median(s2r[edge] / s2t[edge])),
                   gdsai_line_hollow_samples=gd, gdsai_violations_hollow=gdsai_viol, fine_grid_median_abs_dlog=fine_dev,
                   profile=dict(r=rc[rep].tolist(), beta=beta[rep].tolist(), s2r=s2r[rep].tolist(), s2t=s2t[rep].tolist(),
                                rho=rb[rep].tolist()), wall_s=time.time() - t0)
        # LP tests
        if hol.size:
            t, ok = L.lp_minimax(T["lib"], T["M"], hol, np.full(hol.size, 2.0), time_limit=60.0)
            rec["LP_ISO_hollow_dmin"] = t; rec["LP_ISO_hollow_undetermined_LPs"] = ok["undetermined"]
        else:
            rec["LP_ISO_hollow_dmin"] = None
        t, ok = L.lp_minimax(T["lib"], T["M"], outer, np.full(outer.size, 2.0), time_limit=60.0)
        rec["LP_ISO_outer_dmin"] = t; rec["LP_ISO_outer_undetermined_LPs"] = ok["undetermined"]
        x = s2t / (2 * s2r); bp = 1 - 1 / x
        sel = np.where((np.abs(beta) >= 0.05) & rep)[0]
        t, ok = L.lp_minimax(T["lib"], T["M"], sel, 2 * (1 - bp[sel]), time_limit=60.0)
        rec["LP_MIRROR_dmin"] = t; rec["LP_MIRROR_undetermined_LPs"] = ok["undetermined"]; rec["LP_MIRROR_nbins"] = int(sel.size)
        if hol.size:
            selh = np.intersect1d(sel, hol)
            t, ok = L.lp_minimax(T["lib"], T["M"], selh, 2 * (1 - bp[selh]), time_limit=60.0) if selh.size else (None, {"undetermined": None})
            rec["LP_MIRROR_hollow_dmin"] = t; rec["LP_MIRROR_hollow_undetermined_LPs"] = ok["undetermined"]
        else:
            rec["LP_MIRROR_hollow_dmin"] = None
        lines.append(f"{k}: b/r_M {b:.3f}, R {R:.2f} r_M, lib r_lo {rlo:.4f}; solver err {rec['solver_err']:.1e} ({rec['solver_it']} it); "
            f"hollow {hollow} (r_pk {r_pk if r_pk is None else round(r_pk, 3)} r_M, {hol.size} bins); beta hollow median "
            f"{rec['beta_hollow_median']}, bulk median {rec['beta_bulk_median']:+.3f} {rec['beta_bulk_range']}; edge sr2/st2 "
            f"{rec['edge_sr2_over_st2_last_bin']:.3f} (beta {rec['edge_beta_last_bin']:+.1f}); GDSAI violations {gdsai_viol}; "
            f"fine-grid |dlog| {fine_dev:.3f}")
        lines.append(f"    LP ISO d_min hollow {rec['LP_ISO_hollow_dmin']} / outer {rec['LP_ISO_outer_dmin']:.4f}; LP MIRROR d'_min "
            f"{rec['LP_MIRROR_dmin']} ({sel.size} bins), hollow {rec['LP_MIRROR_hollow_dmin']}")
    return k, rec, lines


def part_S(cells):
    log("\n== Part S: ME target of the exact law (unsoftened, units r_M), reported region r >= 0.05 r_M ==")
    with Pool(NPROC) as pool:
        out = pool.map(part_S_cell, list(cells.items()), chunksize=1)
    S = {}
    for k, rec, lines in out:
        S[k] = rec
        for ln in lines: log(ln)
    return S


def control_CS():
    from scipy.special import erf
    F = L.Field(lambda r: np.asarray(r, float), 0.01, 5.0)
    lib = L.Library(F, 0.01, 5.0, nb=NBIN_LIB, sub=SUB_LIB)
    Menc = lambda r: math.sqrt(math.pi / 2) * erf(r / math.sqrt(2)) - r * np.exp(-r ** 2 / 2)
    M = L.bin_masses(lib, Menc); sol = L.maxent(lib, M)
    s2r, s2t, beta, _, _ = L.moments(lib, sol["y"], M)
    rc = np.exp(0.5 * (lib.ub[1:] + lib.ub[:-1]))
    m3 = rc <= 3.0; mb = m3 & (rc >= 0.1)
    dev = lambda m: float(max(np.max(np.abs(s2r[m] - 1)), np.max(np.abs(s2t[m] / 2 - 1))))
    return dict(bin_err=sol["err"], maxdev_r_le_3=dev(m3), pass_as_frozen=bool(dev(m3) <= 0.02 and sol["err"] <= 1e-3),
                maxdev_r_0p1_to_3=dev(mb), pass_outside_inner_boundary_layer=bool(dev(mb) <= 0.02 and sol["err"] <= 1e-3),
                inner_layer_bins=[dict(r=float(rc[i]), s2r=float(s2r[i]), s2t_half=float(s2t[i] / 2)) for i in range(0, 12, 2)])


# ============================================================================================================ Part N (bench field)
def toy_target(c):
    """ME target in the toy's own softened equilibrium field (baryons + rho_ph truncated at r_* = 1, mass from RMIN)."""
    m0 = float(Mph_enc(c, np.array([RMIN]))[0])
    M1 = float(Mph_enc(c, np.array([1.0]))[0]) - m0
    def Mc(r):
        r = np.asarray(r, float); return np.where(r < 1.0, Mph_enc(c, np.minimum(r, 1.0)) - m0, M1)
    g = lambda r: (Mb_enc(c, r) + Mc(r)) * np.asarray(r) / (np.asarray(r) ** 2 + EPS ** 2) ** 1.5
    rho = lambda r: np.gradient(Mph_enc(c, r), r) / np.asarray(r) ** 2
    rlo = lib_floor(rho, RMIN, 1.0)
    T = build_target(g, lambda r: Mph_enc(c, r), rlo, 1.0)
    T["rlo"] = rlo
    return T


def hollow_toy(c):
    """r_pk of the toy's (unsoftened) law profile on (RMIN, 1); None if monotone."""
    rr = np.geomspace(RMIN, 1.0, 4001)
    rho = np.gradient(Mph_enc(c, rr), rr) / rr ** 2
    if not np.any(np.diff(rho) > 0):
        return None
    return float(rr[int(np.argmax(rho))])


class Toy620(T554.Toy554):
    def __init__(self, c, mode, T=None, hot=1.0):
        super().__init__(c, "b" if mode == "b" else ("none" if mode == "none" else "x"), 1.0)
        self.mode620 = mode; self.T = T; self.hot = hot
        if T is not None:
            self.sampler = L.Sampler(T["lib"], T["sol"]["y"])
            lr = np.log(T["rc"])
            self.s2r_t = lambda r: np.interp(np.log(r), lr, T["s2r"]); self.s2t_t = lambda r: np.interp(np.log(r), lr, T["s2t"])
        self.n_resample = 0

    def cur_field(self, r):
        """current real-mass field (G9: baryons + all cold energy, the toy's softened gravity) as callables phi, g."""
        rs = np.sort(r); m = self.m; c = self.c
        gfun = lambda x: (Mb_enc(c, x) + m * np.searchsorted(rs, x)) * np.asarray(x) / (np.asarray(x) ** 2 + EPS ** 2) ** 1.5
        F = L.Field(gfun, RMIN * 0.5, max(2.0, float(rs[-1]) * 1.05), n=1201)
        return F.phi, F.g

    def vel_step(self, r, vr, vt, dt, g, rng):
        mode = self.mode620
        if mode == "b":
            return self.ou_step(r, vr, vt, dt, g, rng)                 # FIX-2 exactly (CFG544 operator)
        c = self.c; al = T544.ALPHA
        mc = self.m * np.histogram(r, self.rf)[0]; rho = mc / self.V
        k = np.clip(np.searchsorted(self.rf, r) - 1, 0, NB - 1)
        gam = al * np.sqrt(4 * math.pi * (self.rhob + rho))[k]
        inside = r < 1.0
        K0 = 0.5 * self.m * np.sum(vr ** 2 + vt ** 2)
        if mode == "A":
            sel = inside & (rng.random(r.size) < (1 - np.exp(-gam * dt)))
            if sel.any():
                phi, gf = self.cur_field(r)
                nvr, nvt = self.sampler.draw(r[sel], phi, gf, rng)
                vr = vr.copy(); vt = vt.copy()
                vr[sel] = nvr * self.hot; vt[sel] = nvt * self.hot
                self.n_resample += int(sel.sum())
            K1 = 0.5 * self.m * np.sum(vr ** 2 + vt ** 2)
            return vr, vt, K1 - K0
        # Gaussian OU with the target's moments (AG) or the mirrored ratio (AGm), inside r_*
        a = np.exp(-gam * dt)
        s2r = self.s2r_t(np.clip(r, self.T["rc"][0], 1.0)); s2t = self.s2t_t(np.clip(r, self.T["rc"][0], 1.0))
        if mode == "AGm":
            x = s2t / (2 * s2r); xm = 1 / x; tot = s2r + s2t
            s2r = tot / (1 + 2 * xm); s2t = 2 * xm * tot / (1 + 2 * xm)
        br = np.sqrt(s2r * (1 - a ** 2)); bt = np.sqrt(0.5 * s2t * (1 - a ** 2))
        x1, x2, x3 = rng.standard_normal((3, r.size))
        nr = a * vr + br * x1; vtx = a * vt + bt * x2; vty = bt * x3; nt = np.hypot(vtx, vty)
        vr_n = np.where(inside, nr, vr); vt_n = np.where(inside, nt, vt)
        K1 = 0.5 * self.m * np.sum(vr_n ** 2 + vt_n ** 2)
        return vr_n, vt_n, K1 - K0


def make_ic_F(c, T, rng, inject=False):
    """IC-F: positions from rho_ph (RMIN..r_*), velocities from the target conditional in the target's own field."""
    m = c["Mcat"] / NPART
    r = T544.sample_ph(c, NPART, 1.0, rng)
    if inject:
        Mi = 0.3 * float(Mph_enc(c, np.array([0.3]))[0] - Mph_enc(c, np.array([RMIN]))[0])
        ni = int(round(Mi / m)); r = np.concatenate([r, T544.sample_ph(c, ni, 0.3, rng)])
    S = L.Sampler(T["lib"], T["sol"]["y"])
    vr, vt = S.draw(r, T["F"].phi, T["F"].g, rng)
    return r, vr, r * vt, m


def run(job):
    c, name, ic, mode, T_Gyr = job["c"], job["name"], job["ic"], job["mode"], job["T"]
    T544.ALPHA = job.get("alpha", 1.0)
    reads = sorted(set(job.get("reads", [T_Gyr])))
    T = toy_target(c) if mode in ("A", "AG", "AGm") or ic == "F" else None
    rng = np.random.default_rng(T544.SEED)
    if ic == "F":
        r, vr, Lm, m = make_ic_F(c, T, rng, inject=job.get("inject", False))
    else:
        r, vr, Lm, m = T544.make_ic(c, ic, rng, sig2_scale=job.get("sig2", 1.0), inject=job.get("inject", False))
    toy = Toy620(c, mode, T, hot=job.get("hot", 1.0)); toy.m = m
    r_pk = hollow_toy(c)
    Mph_h = float(Mph_enc(c, np.array([r_pk]))[0] - Mph_enc(c, np.array([RMIN]))[0]) if r_pk else None
    win = {t: [0.0, 0] for t in reads}
    n0 = r.size; dt = c["dt"]; tu = c["tu_Gyr"]
    nsteps = int(round(T_Gyr / (dt * tu))); every = max(1, int(round(0.25 / (dt * tu))))
    K0, W0 = toy.energy(r, vr, Lm)
    W_drift = 0.0; W_ou = 0.0; W_ou_pos = 0.0
    snaps = []; t0 = time.time(); blow = False; nsub_max = 0
    for it in range(nsteps + 1):
        tnow = it * dt * tu
        if r_pk and it % 10 == 0:
            cnt = int(np.sum(r < r_pk))
            for tr in reads:
                if tr - 2.0 <= tnow <= tr + 1e-9:
                    win[tr][0] += cnt; win[tr][1] += 1
        if it % every == 0 or it == nsteps:
            dg = toy.diag554(r, vr, Lm); K, W = toy.energy(r, vr, Lm)
            dg.update(t_Gyr=tnow, E=K + W, sink_cum=-(W_drift + W_ou) / c["Mcat"], drift_out=-W_drift / c["Mcat"],
                      relax_in=W_ou / c["Mcat"], relax_in_gross=W_ou_pos / c["Mcat"],
                      integ_err=(K + W - K0 - W0 - W_drift - W_ou) / abs(K0 + W0))
            snaps.append(dg)
            if dg["relax_in_gross"] > 10.0 or dg["vmax"] > 50.0:
                blow = True
        if it == nsteps: break
        r, vr, ns = T544.vlasov_step(toy, r, vr, Lm, dt)
        nsub_max = max(nsub_max, ns)
        if toy.drift:
            vt = Lm / r
            g, _ = toy.gravity(r)
            _, Wb = toy.energy(r, vr, Lm)
            rn, _w = toy.drift_step(r, dt, g)
            Ln = rn * vt
            _, Wa = toy.energy(rn, vr, Ln)
            W_drift += Wa - Wb
            Lm = Ln; r = rn
            vr, vt, dk = toy.vel_step(r, vr, vt, dt, g, rng)
            W_ou += dk; W_ou_pos += max(dk, 0.0); Lm = r * vt
    r99a = T544.r99_analytic(c)
    def at(tr):
        s = min(snaps, key=lambda q: abs(q["t_Gyr"] - tr)); ref = min(snaps, key=lambda q: abs(q["t_Gyr"] - (s["t_Gyr"] - 2.0)))
        o = dict(t=s["t_Gyr"], logX=s["logX"], logXJ=s["logXJ"], D=s["D"], r99=s["r99"], dln_r99=float(math.log(s["r99"] / r99a)),
                 beta_shell=s["beta"], sink=s["sink_cum"], d_logXJ_last2=float(s["logXJ"] - ref["logXJ"]),
                 d_D_last2=float(s["D"] - ref["D"]), d_logX_last2=float(s["logX"] - ref["logX"]),
                 frac_beyond_rta=s["frac_beyond_rta"], Mc_in_rstar_over_Mph=s["Mc_in_rstar_over_Mph"],
                 excess_in_rstar=s["excess_in_rstar"])
        o["G550"] = bool(abs(o["D"]) <= 0.1 and abs(o["logXJ"]) <= 0.1 and abs(o["d_D_last2"]) <= 0.05 and abs(o["d_logXJ_last2"]) <= 0.05)
        o["gate544"] = bool(abs(o["D"]) <= 0.1 and abs(o["logX"]) <= 0.1 and abs(o["d_D_last2"]) <= 0.05 and abs(o["d_logX_last2"]) <= 0.05)
        o["gate_age"] = bool(abs(o["D"]) <= 0.05 and abs(o["logXJ"]) <= 0.05 and abs(o["d_D_last2"]) <= 0.05 and abs(o["d_logXJ_last2"]) <= 0.05)
        o["edge_sharp"] = bool(abs(o["dln_r99"]) <= 0.1)
        if r_pk:
            cnt, ns_ = win[tr]
            nbar = cnt / max(ns_, 1)
            o["hollow_mean_count"] = nbar; o["hollow_samples"] = ns_
            o["hollow_expected_count"] = Mph_h / m
            o["H"] = float(math.log10(max(nbar, 1e-3) * m / Mph_h))
            o["sigma_H"] = float(1 / (math.log(10) * math.sqrt(max(nbar, 1.0))))
            o["hollow_held"] = bool(abs(o["H"]) <= 0.15 + 2 * o["sigma_H"])
        return o
    res = dict(name=name, cell=f"{c['sys']}_{c['foot']}", ic=ic, mode=mode, alpha=T544.ALPHA, T_Gyr=T_Gyr, steps=nsteps,
               n_particles=n0, mass_exact=bool(r.size == n0), r99_analytic=r99a, r_pk=r_pk,
               reads={str(tr): at(tr) for tr in reads}, final=at(T_Gyr),
               series=[dict(t=s["t_Gyr"], logXJ=s["logXJ"], D=s["D"], r99=s["r99"], sink=s["sink_cum"], beta=s["beta"],
                            F=s["F"]) for s in snaps],
               wall_s=time.time() - t0, nsub_max=nsub_max, integ_err_maxabs=float(max(abs(s["integ_err"]) for s in snaps)),
               vmax_code=float(max(s["vmax"] for s in snaps)), relax_in_gross_max=float(max(s["relax_in_gross"] for s in snaps)),
               blow_up=bool(blow), n_resample=toy.n_resample,
               max_rise_F_over_F0=float(max(snaps[i + 1]["F"] - snaps[i]["F"] for i in range(len(snaps) - 1)) / snaps[0]["F"])
               if snaps[0]["F"] > 0 else None)
    return res


# ============================================================================================================ main
def jobs_main(cells):
    J = []
    for k, c in cells.items():
        for al in (0.5, 1.0, 2.0):
            J.append(dict(c=c, name=f"{k}|A_B_a{al}", ic="B", mode="A", T=13.8, alpha=al, reads=[10.0, 13.8]))
            J.append(dict(c=c, name=f"{k}|A_C_a{al}", ic="C", mode="A", T=13.8, alpha=al, reads=[5.0, 13.8]))
        for md in ("AG", "b"):
            J.append(dict(c=c, name=f"{k}|{md}_B", ic="B", mode=md, T=10.0, reads=[10.0]))
            J.append(dict(c=c, name=f"{k}|{md}_C", ic="C", mode=md, T=5.0, reads=[5.0]))
        J.append(dict(c=c, name=f"{k}|A_over_base", ic="F", mode="A", T=5.0))
        J.append(dict(c=c, name=f"{k}|A_over_inj", ic="F", mode="A", T=5.0, inject=True))
        J.append(dict(c=c, name=f"{k}|C2p_vlasov_F", ic="F", mode="none", T=2.0))
    return J


def jobs_mut(cells):
    J = []
    for k, c in cells.items():
        J.append(dict(c=c, name=f"{k}|MF_AGm_C", ic="C", mode="AGm", T=5.0))
        J.append(dict(c=c, name=f"{k}|MT_Ahot_C", ic="C", mode="A", T=5.0, hot=math.sqrt(2.0)))
    return J


def cost(j):
    return j["T"] / (j["c"]["dt"] * j["c"]["tu_Gyr"])


def main():
    cells = all_cells()
    RES["cells"] = {k: {kk: vv for kk, vv in v.items() if kk not in ("Vf2_SI", "rstar_SI")} for k, v in cells.items()}
    log("CFG620 anisotropic velocity-relaxation target" + (" [MUTATE]" if MUT else ""))
    for k, c in cells.items():
        c4 = abs(float(Mph_enc(c, np.array([1.0]))[0]) / c["Mcat"] - 1)
        RES["cells"][k].update(C4=c4, r99_analytic=T544.r99_analytic(c), r_pk_toy=hollow_toy(c))
        log(f"{k}: V_f {c['Vf_kms']:.1f} km/s, r_* {c['rstar_kpc']:.1f} kpc, r_M {c['rM_kpc']:.2f} kpc, b/r_M {c['b_over_rM']:.3f}, "
            f"f_ret {c['fret']:.3f}, r_ta/r_* {c['rta']:.3f}, M_cat/M_b {c['Mcat'] / c['Mb']:.2f}, t_unit {c['tu_Gyr']:.3f} Gyr; "
            f"C4 {c4:.2e}; toy hollow r_pk {RES['cells'][k]['r_pk_toy']}")
    if not MUT:
        RES["CS"] = control_CS()
        log(f"\nCS (harmonic isothermal): {RES['CS']}")
        RES["sympy"] = SY.all_items()
        log("\nSympy / K6:")
        for kk, vv in RES["sympy"].items():
            log(f"  {kk}: {vv}")
        RES["partS"] = part_S(cells)
        log("\n== Part N: ME target in the bench field ==")
        RES["partN"] = {}
        for k, c in cells.items():
            T = toy_target(c)
            rc = T["rc"]; b = T["beta"]
            sh = (rc > 0.1) & (rc < 0.9)
            RES["partN"][k] = dict(lib_rlo=T["rlo"], solver_err=T["sol"]["err"], self_consistent=bool(T["sol"]["err"] <= 1e-3),
                                   beta_shell_median=float(np.median(b[sh])), beta_edge_last_bin=float(b[-1]),
                                   beta_inner_median=float(np.median(b[rc < 0.05])) if np.any(rc < 0.05) else None,
                                   profile=dict(r=rc.tolist(), beta=b.tolist(), s2r=T["s2r"].tolist(), s2t=T["s2t"].tolist()))
            log(f"{k}: lib r_lo {T['rlo']:.4g} r_*, solver err {T['sol']['err']:.1e}; beta shell median "
                f"{RES['partN'][k]['beta_shell_median']:+.3f}, inner median {RES['partN'][k]['beta_inner_median']}, edge "
                f"{b[-1]:+.1f}")
        RES["dW541"] = {k: dW541(k, c) for k, c in cells.items()}
        log(f"\nCFG541 drift-only release dW/V_f^2 per M_cat: {RES['dW541']}")
        jobs = jobs_main(cells)
    else:
        jobs = jobs_mut(cells)
    jobs.sort(key=lambda j: -cost(j))
    log(f"\nbench: {len(jobs)} runs on {NPROC} processes")
    t0 = time.time()
    with Pool(NPROC) as pool:
        out = pool.map(run, jobs, chunksize=1)
    log(f"bench wall {time.time() - t0:.0f} s")
    runs = {o["name"]: o for o in out}
    RES["runs"] = runs
    for o in out:
        f = o["final"]
        log(f"  {o['name']:28s} t {f['t']:.2f}  logXJ {f['logXJ']:+.3f} D {f['D']:+.3f} dlnr99 {f['dln_r99']:+.3f} beta "
            f"{f['beta_shell']:+.2f} sink {f['sink']:+.3f} G550 {f['G550']} H {f.get('H')} blow {o['blow_up']} "
            f"err {o['integ_err_maxabs']:.1e} wall {o['wall_s']:.0f}s")
    labels(cells, runs) if not MUT else mutate_eval(cells, runs)
    path = os.path.join(HERE, f"cfg620_results{TAG}.json")
    json.dump(RES, open(path, "w"), indent=1, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x))
    open(os.path.join(HERE, f"cfg620{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    if MUT:
        sys.exit(1 if RES["MUTATE"]["all_bite"] else 0)


def labels(cells, runs):
    keys = list(cells); hcells = [k for k in keys if RES["cells"][k]["r_pk_toy"]]
    A1 = {k: dict(B=runs[f"{k}|A_B_a1.0"]["reads"]["10.0"], C=runs[f"{k}|A_C_a1.0"]["reads"]["5.0"]) for k in keys}
    # controls
    c2 = {k: runs[f"{k}|C2p_vlasov_F"]["final"] for k in keys}
    C2p = all(abs(v["D"]) <= 0.1 and abs(v["logXJ"]) <= 0.1 for v in c2.values())
    c5 = {}
    for k in ("MW_can", "MW_alt", "cluster_can", "cluster_alt"):
        f = runs[f"{k}|b_C"]["final"]; ref = J544["runs"][f"{k}|fix2_C"]["final"] if "runs" in J544 else None
        c5[k] = dict(dlogX=abs(f["logX"] - ref["logX"]) if ref else None, dD=abs(f["D"] - ref["D"]) if ref else None)
    C5 = all(v["dlogX"] is not None and v["dlogX"] <= 1e-6 and v["dD"] <= 1e-6 for v in c5.values())
    mass = all(o["mass_exact"] for o in runs.values())
    C4 = {k: RES["cells"][k]["C4"] for k in keys}
    CS = RES["CS"]
    ctrl = dict(CS_as_frozen=CS["pass_as_frozen"], CS_outside_inner_layer=CS["pass_outside_inner_boundary_layer"],
                C2p=C2p, C2p_detail={k: dict(D=v["D"], logXJ=v["logXJ"], dln_r99=v["dln_r99"]) for k, v in c2.items()},
                C4=C4, C4_pass_1e4=all(v <= 1e-4 for v in C4.values()), C5=C5, C5_detail=c5, mass_exact=mass)
    # target items
    S = RES["partS"]; N = RES["partN"]
    sc = all(S[k]["self_consistent"] for k in keys) and all(N[k]["self_consistent"] for k in keys)
    sym = RES["sympy"]["K1_K5_pass"]
    g550 = {k: A1[k]["B"]["G550"] and A1[k]["C"]["G550"] for k in keys}
    blow = {k: any(runs[f"{k}|A_{ic}_a1.0"]["blow_up"] for ic in "BC") for k in keys}
    eB = {k: A1[k]["B"]["sink"] for k in keys}
    eC = {k: RES["dW541"][k] + A1[k]["C"]["sink"] for k in keys}
    energy = all(0 <= eB[k] <= 1.0 and 0 <= eC[k] <= 1.0 for k in keys)
    hold = {k: bool(A1[k]["B"].get("hollow_held") and A1[k]["C"].get("hollow_held")) for k in hcells}
    derived = sc and sym and all(g550.values()) and not any(blow.values()) and energy and all(hold.values())
    inconsistent = (not sc) or (not all(g550.values())) or any(blow.values()) or (not energy) or (not all(hold.values()))
    tlabel = "ANISOTROPIC TARGET DERIVED" if derived else ("INCONSISTENT" if inconsistent else "POSITED")
    edge = {k: dict(B=A1[k]["B"]["dln_r99"], C=A1[k]["C"]["dln_r99"]) for k in keys}
    sharp = all(abs(v["B"]) <= 0.1 and abs(v["C"]) <= 0.1 for v in edge.values())
    edge2 = {k: dict(B=runs[f"{k}|b_B"]["final"]["dln_r99"], C=runs[f"{k}|b_C"]["final"]["dln_r99"]) for k in keys}
    edgeG = {k: dict(B=runs[f"{k}|AG_B"]["final"]["dln_r99"], C=runs[f"{k}|AG_C"]["final"]["dln_r99"]) for k in keys}
    comp = [k for k in keys if k.startswith("compact") or k.startswith("cluster")]
    works = all(g550[k] and not blow[k] and hold.get(k, True) for k in comp)
    # overfill
    P = {}
    for k in keys:
        ob, oi = runs[f"{k}|A_over_base"]["final"], runs[f"{k}|A_over_inj"]["final"]
        Mi = 0.3 * float(Mph_enc(cells[k], np.array([0.3]))[0] - Mph_enc(cells[k], np.array([RMIN]))[0])
        ni = int(round(Mi / (cells[k]["Mcat"] / NPART))); Minj = ni * cells[k]["Mcat"] / NPART
        P[k] = float((oi["excess_in_rstar"] - ob["excess_in_rstar"]) / Minj)
    over = all(v <= 0.2 for v in P.values())
    # alpha robustness
    rob = {}
    for k in keys:
        for al in (0.5, 1.0, 2.0):
            for ic in "BC":
                o = runs[f"{k}|A_{ic}_a{al}"]["reads"]["13.8"]
                rob[f"{k}|{ic}|a{al}"] = dict(pass_=bool(o["gate_age"] and o["edge_sharp"]), gate_age=o["gate_age"],
                                              logXJ=o["logXJ"], D=o["D"], dD=o["d_D_last2"], dXJ=o["d_logXJ_last2"],
                                              dln_r99=o["dln_r99"],
                                              within_CFG558_allowance=(bool(-0.1 <= o["dln_r99"] <= C2_CELL[k] + 0.1)
                                                                       if k in C2_CELL else None),
                                              H=o.get("H"), hollow_held=o.get("hollow_held"))
    robust = all(v["pass_"] for v in rob.values())
    lyap = max(o["max_rise_F_over_F0"] or 0 for n, o in runs.items() if "|A_" in n)
    # Q2 context: CFG559 sharp (MK0) KiDS numbers
    q2 = {}
    try:
        jk = json.load(open(J559K))
        q2["cfg559_kids_scores"] = jk.get("scores")
    except Exception as e:                                                          # pragma: no cover
        q2["error"] = str(e)
    RES["labels"] = dict(target=tlabel, edge="SHARP" if sharp else "SOFTENED", works_in_compact="YES" if works else "NO",
                         overfill="HANDLED" if over else "NOT HANDLED", alpha="alpha-ROBUST" if robust else "NOT alpha-ROBUST",
                         lyapunov="NOT ESTABLISHED", controls_pass_as_frozen=bool(ctrl["CS_as_frozen"] and C2p and C5 and mass),
                         controls_pass_CS_read_outside_layer=bool(ctrl["CS_outside_inner_layer"] and C2p and C5 and mass))
    RES["verdict_detail"] = dict(controls=ctrl, self_consistent=sc, sympy_K1_K5=sym, G550_alpha1=g550, blow_up=blow,
                                 energy_B_net=eB, energy_C_whole=eC, energy_compatible=energy, hollow_cells=hcells,
                                 hollow_held=hold, hollow_detail={k: dict(B=dict(H=A1[k]["B"]["H"], sH=A1[k]["B"]["sigma_H"],
                                                                                 n=A1[k]["B"]["hollow_mean_count"],
                                                                                 n_exp=A1[k]["B"]["hollow_expected_count"]),
                                                                          C=dict(H=A1[k]["C"]["H"], sH=A1[k]["C"]["sigma_H"],
                                                                                 n=A1[k]["C"]["hollow_mean_count"]))
                                                                  for k in hcells},
                                 hollow_FIX2={k: dict(B=runs[f"{k}|b_B"]["final"].get("H"), C=runs[f"{k}|b_C"]["final"].get("H"))
                                              for k in hcells},
                                 hollow_AG={k: dict(B=runs[f"{k}|AG_B"]["final"].get("H"), C=runs[f"{k}|AG_C"]["final"].get("H"))
                                            for k in hcells},
                                 edge_FIXA=edge, edge_FIX2=edge2, edge_FIXAG=edgeG, overfill_P=P, alpha=rob,
                                 lyapunov_max_rise_F=lyap, Q2=q2)
    log("\n== Labels ==")
    for kk, vv in RES["labels"].items():
        log(f"  {kk}: {vv}")
    log(f"  controls: {json.dumps({k: v for k, v in ctrl.items() if k not in ('C2p_detail', 'C5_detail')})}")
    log(f"  G550 (alpha 1): {g550}; blow-up {blow}")
    log(f"  energy IC-B net {eB}; IC-C whole history {eC}")
    log(f"  hollow held {hold}; FIX-A H {RES['verdict_detail']['hollow_detail']}")
    log(f"  FIX-2 H {RES['verdict_detail']['hollow_FIX2']}; FIX-AG H {RES['verdict_detail']['hollow_AG']}")
    log(f"  edge FIX-A {edge}\n  edge FIX-2 {edge2}\n  edge FIX-AG {edgeG}")
    log(f"  overfill P {P}")
    log(f"  alpha robustness: {sum(v['pass_'] for v in rob.values())}/{len(rob)} pass")
    for kk, vv in rob.items():
        log(f"    {kk}: {vv}")


def mutate_eval(cells, runs):
    keys = list(cells)
    jm = json.load(open(os.path.join(HERE, "cfg620_results.json")))
    S = jm["partS"]; hS = [k for k in keys if S[k]["hollow"]]
    hT = [k for k in keys if jm["cells"][k]["r_pk_toy"]]
    MI_a = all((S[k]["LP_ISO_hollow_dmin"] is not None) and S[k]["LP_ISO_hollow_dmin"] >= 0.1 for k in hS)
    e2 = {k: (jm["runs"][f"{k}|b_B"]["final"]["dln_r99"], jm["runs"][f"{k}|b_C"]["final"]["dln_r99"]) for k in keys}
    MI_b1 = all(min(v) > 0.1 for v in e2.values())
    H2 = {k: (jm["runs"][f"{k}|b_B"]["final"].get("H"), jm["runs"][f"{k}|b_C"]["final"].get("H")) for k in hT}
    MI_b2 = all(max(h for h in v if h is not None) >= 0.3 for v in H2.values())
    MI = MI_a and MI_b1 and MI_b2
    MF_a = all((S[k]["LP_MIRROR_hollow_dmin"] is not None) and S[k]["LP_MIRROR_hollow_dmin"] >= 0.05 for k in hS)
    mf = {}
    for k in keys:
        f = runs[f"{k}|MF_AGm_C"]["final"]
        fails = (not f["G550"]) or (not f["edge_sharp"]) or (f.get("hollow_held") is False)
        mf[k] = dict(G550=f["G550"], dln_r99=f["dln_r99"], H=f.get("H"), hollow_held=f.get("hollow_held"), fails=bool(fails))
    MF_b = all(v["fails"] for v in mf.values())
    MF = MF_a and MF_b
    mt = {k: dict(G550=runs[f"{k}|MT_Ahot_C"]["final"]["G550"], logXJ=runs[f"{k}|MT_Ahot_C"]["final"]["logXJ"],
                  D=runs[f"{k}|MT_Ahot_C"]["final"]["D"]) for k in keys}
    MT = all(not v["G550"] for v in mt.values())
    RES["MUTATE"] = dict(MI=dict(bites=MI, LP_ISO_hollow={k: S[k]["LP_ISO_hollow_dmin"] for k in hS}, a=MI_a,
                                 FIX2_edge=e2, b_edge=MI_b1, FIX2_H=H2, b_hollow=MI_b2),
                         MF=dict(bites=MF, LP_MIRROR_hollow={k: S[k]["LP_MIRROR_hollow_dmin"] for k in hS}, a=MF_a,
                                 bench=mf, b=MF_b),
                         MT=dict(bites=MT, bench=mt), all_bite=bool(MI and MF and MT))
    log("\n== MUTATE ==")
    for kk, vv in RES["MUTATE"].items():
        log(f"  {kk}: {vv}")


if __name__ == "__main__":
    main()
