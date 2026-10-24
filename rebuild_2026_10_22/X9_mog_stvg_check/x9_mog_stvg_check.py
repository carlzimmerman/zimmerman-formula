#!/usr/bin/env python3
"""X9_mog_stvg_check (criteria 8c548f725d): does MOG/STVG with its published universal set (alpha = 8.89, mu = 0.042/kpc;
Moffat & Rahvar 2013, reused for clusters by Moffat & Rahvar 2014) pass (a) P4's SPARC RAR line and (b) X2's fixed-form
cluster pass line on the eRASS1 x KiDS stack?  Nothing is fitted here beyond P4's per-galaxy Upsilon convention.

MOG (LITERATURE-INPUT, PROVISIONAL): massive particles feel g = (1 + alpha) g_N - alpha g_Yukawa (superposed point-mass law);
light feels G0 = (1 + alpha) G_N only (lensing mass (1 + alpha) M; MRT18 Eqs. 30-32).  Engines: exact spherical shells
(Newton + Yukawa) and a razor-thin-disc Hankel multiplier m(k) = 1 - k/sqrt(k^2 + mu^2) (FFTLog, scipy.fft.fht).
Record code is exec'd read-only from its source text: P4 (SPARC loader and statistics), F1 + X2 (cluster data, model pieces,
statistics).  --mutate: the engines use alpha = 0 (Newton); K1, K2, K4 (references at the published alpha, mu) must FAIL.
kappa = 1/2 FITTED for the programme's law (reference rows only); footings never pooled; no dark-matter particle; not theory closed.
Run: OMP_NUM_THREADS=1 nice -n 15 python3 x9_mog_stvg_check.py [--mutate]
"""
import os, sys, io, json, math, time, hashlib, resource, contextlib, warnings
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.fft import fht, ifht, fhtoffset
from scipy.special import i0e, i1e, k0e, k1e
from scipy.stats import chi2 as CHI2
warnings.filterwarnings("ignore", category=RuntimeWarning)
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
CFGD = os.path.join(REPO, "campaign_fresh_gravity"); DATA = os.path.join(REPO, "real_research", "data")
X2D = os.path.join(REB, "X2_cluster_outskirts"); P4D = os.path.join(REB, "P4_v3_galaxy_tiles"); F1D = os.path.join(REB, "F1_cluster_cores")
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"x9_mog_stvg_check{TAG}.out"), "w")


def say(*a):
    s = " ".join(str(x) for x in a)
    if os.environ.get("X9_RSS_TRACE"): s += f"   [rss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.3f} GB]"
    print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()


RES = {"lane": "X9_mog_stvg_check", "criteria": "8c548f725d", "mutate": MUT, "checks": {}}
CHECKS = []


def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES["checks"][name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


def guard(tag):
    g = rss()
    if g > 0.95:
        say(f"RSS GUARD {g:.3f} GB at {tag} -> abort"); sys.exit(3)


say(__doc__.strip())
# ===================================================================================================== MOG parameters (frozen)
ALPHA_PUB, MU_PUB = 8.89, 0.042                     # MR13 universal set (kpc^-1); MR14 reuses it for clusters
ALPHA = 0.0 if MUT else ALPHA_PUB                   # the engines' alpha (MUTATE: Newton)
CORNERS = [(8.55, 0.038), (8.55, 0.046), (9.23, 0.038), (9.23, 0.046)]
S1_GINF, S1_D, S1_E = 20.0, 6250.0, 25000.0         # MRT18 Eqs. 11-14 (Moffat & Toth 2009): G_inf/G_N, D [Msun^1/2/kpc], E [Msun^1/2]
def s1_alpha(M): return (S1_GINF - 1.0) * M / (np.sqrt(M) + S1_E) ** 2
def s1_mu(M): return S1_D / np.sqrt(M)              # kpc^-1
RES["parameters"] = dict(alpha=ALPHA_PUB, mu_per_kpc=MU_PUB, engine_alpha=ALPHA, corners=CORNERS,
                         S1=dict(Ginf_over_GN=S1_GINF, D=S1_D, E=S1_E), S2="BM06 Eqs. 23, 33")
say(f"\nMOG universal set U: alpha {ALPHA_PUB}, mu {MU_PUB} kpc^-1 (1/mu = {1/MU_PUB:.1f} kpc); engine alpha {ALPHA}")


# ===================================================================================================== engines
def yfac(r, s, mu):
    """r^2 g_Yukawa(r) / (G m) for a thin shell of mass m at radius s (exact; inward positive).  r > s: (1+x) e^-x sinh(y)/y;
    r < s: -e^-y (x cosh x - sinh x)/y, x = mu r, y = mu s; combined exponents (no overflow), series at small x, y."""
    r = np.asarray(r, float); s = np.asarray(s, float); x = mu * r; y = mu * s
    out_ext = np.where(y < 1e-2, (1 + x) * np.exp(-x) * (1 + y * y / 6 + y ** 4 / 120),
                       (1 + x) * (np.exp(-(x - y)) - np.exp(-(x + y))) / (2 * np.maximum(y, 1e-300)))
    c_int = np.where(x < 1e-2, np.exp(-y) * (x ** 3 / 3 + x ** 5 / 30 + x ** 7 / 840),
                     0.5 * ((x - 1) * np.exp(-(y - x)) + (x + 1) * np.exp(-(y + x))))
    out_int = -c_int / np.maximum(y, 1e-300)
    return np.where(r > s, out_ext, out_int)


def sph_masses(r_eval, s, dm, mu, chunk=None):
    """(M_N enclosed, M_Y) at r_eval for shells (s, dm): g_MOG r^2/G = (1 + alpha) M_N - alpha M_Y."""
    r_eval = np.asarray(r_eval, float); MN = np.empty(len(r_eval)); MY = np.empty(len(r_eval))
    chunk = chunk or max(1, int(1e5 // max(len(s), 1)))                # A2: small temporaries (RSS)
    for a in range(0, len(r_eval), chunk):
        rr = r_eval[a:a + chunk, None]
        MN[a:a + chunk] = (dm[None, :] * (s[None, :] < rr)).sum(1)
        MY[a:a + chunk] = yfac(rr, s[None, :], mu) @ dm
    return MN, MY


class DiscFFT:
    """razor-thin disc: delta g = g_N - g_Y from the in-plane Newtonian field via the order-1 Hankel multiplier
    m(k) = 1 - k/sqrt(k^2 + mu^2) (in-plane Yukawa/Newton ratio of a thin sheet = k/sqrt(k^2 + mu^2)).  a(r) = g_N r = V^2."""
    def __init__(self, rmin=1e-4, rmax=1e6, n=4096, q=0.5):
        self.lr = np.linspace(math.log(rmin), math.log(rmax), n); self.r = np.exp(self.lr); self.dln = self.lr[1] - self.lr[0]
        self.q = q; self.off = fhtoffset(self.dln, mu=1, initial=0.0, bias=q)
        jc = (n - 1) / 2; rc = math.exp(0.5 * (self.lr[0] + self.lr[-1])); kc = math.exp(self.off) / rc
        self.k = kc * np.exp((np.arange(n) - jc) * self.dln)

    def A(self, R, V2):
        r = self.r; a = np.interp(r, R, V2)
        a = np.where(r < R[0], V2[0] * (r / R[0]) ** 2, a); a = np.where(r > R[-1], V2[-1] * (R[-1] / r), a)
        return fht(a, self.dln, mu=1, offset=self.off, bias=self.q)

    def dg(self, A, mu, R):
        s = np.sqrt(self.k ** 2 + mu * mu); m = mu * mu / (s * (s + self.k))
        a2 = ifht(A * m, self.dln, mu=1, offset=self.off, bias=self.q)
        return np.interp(np.log(R), self.lr, a2) / R


DF = DiscFFT()


def freeman_V2(R, Rd, M=1.0):
    y = R / (2 * Rd); S0 = M / (2 * np.pi * Rd ** 2)
    return 4 * np.pi * S0 * Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def dg_direct(Rs, Rd, mu, M=1.0, ns=6000, nt=2000, smax=40.0):
    """direct 2-D quadrature of the exponential disc with the smooth kernel [1 - e^{-mu d}(1 + mu d)]/d^2 (delta g, inward)."""
    S0 = M / (2 * np.pi * Rd ** 2); ds = smax * Rd / ns; s = (np.arange(ns) + 0.5) * ds
    dth = np.pi / nt; th = (np.arange(nt) + 0.5) * dth; ct = np.cos(th); out = []
    for Ri in Rs:
        tot = 0.0
        for a in range(0, ns, 50):                                       # A2: small temporaries (RSS)
            S = s[a:a + 50, None]; d2 = Ri * Ri + S * S - 2 * Ri * S * ct[None, :]; d = np.sqrt(np.maximum(d2, 1e-300)); md = mu * d
            K = np.where(md < 1e-3, mu * mu / 2 - mu ** 3 * d / 3 + mu ** 4 * d2 / 8, (1 - np.exp(-md) * (1 + md)) / np.maximum(d2, 1e-300))
            tot += float((S0 * np.exp(-S / Rd) * S * (Ri - S * ct[None, :]) / d * K).sum())
        out.append(2 * tot * ds * dth)
    return np.array(out)


# ===================================================================================================== K1, K2, K4: engines vs references
say("\n=== engine checks (references always at the published alpha, mu) ===")
e1 = np.logspace(-7, 0, 2001); ap = 1e-3; Mpl = e1 ** 3 / (e1 ** 2 + ap ** 2) ** 1.5
s1 = np.sqrt(e1[:-1] * e1[1:]); dm1 = np.diff(Mpl); r1 = np.logspace(math.log10(0.5), math.log10(300), 60)
MN1, MY1 = sph_masses(r1, s1, dm1, MU_PUB); Mt1 = Mpl[-1]
eng1 = ((1 + ALPHA) * MN1 - ALPHA * MY1) / Mt1
ref1 = 1 + ALPHA_PUB - ALPHA_PUB * np.exp(-MU_PUB * r1) * (1 + MU_PUB * r1)
k1 = float(np.max(np.abs(eng1 / ref1 - 1)))
check("K1", k1 <= 1e-3, f"compact Plummer: max rel {k1:.2e} (G_eff/G_N at 300 kpc engine {eng1[-1]:.4f}, closed form {ref1[-1]:.4f})", "<= 1e-3")
RES["K1"] = dict(max_rel=k1, r=r1.tolist(), engine=eng1.tolist(), closed=ref1.tolist())
k2 = {}; k2ext = {}
for Rd in (1.0, 3.0, 6.0):
    Rt = np.logspace(math.log10(0.25), 1.0, 10) * Rd
    dgD = dg_direct(Rt, Rd, MU_PUB); gN = freeman_V2(Rt, Rd) / Rt; ref = gN + ALPHA_PUB * dgD
    Rs = np.linspace(0.05, 30, 600) * Rd; V2s = freeman_V2(Rs, Rd); eng = gN + ALPHA * DF.dg(DF.A(Rs, V2s), MU_PUB, Rt)
    k2[Rd] = float(np.max(np.abs(eng / ref - 1)))
    Re = np.linspace(0.25, 10, 40) * Rd; V2e = freeman_V2(Re, Rd); dge = DF.dg(DF.A(Re, V2e), MU_PUB, Rt)
    k2ext[Rd] = float(np.max(np.abs((gN + ALPHA_PUB * dge) / (gN + ALPHA_PUB * dgD) - 1)))
check("K2", max(k2.values()) <= 5e-3, f"exponential discs Rd 1/3/6 kpc, R 0.25-10 Rd: max rel g_MOG {', '.join(f'{v:.2e}' for v in k2.values())} "
      f"(samples 0.05-30 Rd, amendment A1)", "<= 5e-3")
say(f"  D-EXT (diagnostic, no weight): samples truncated at 10 Rd with the declared R^-2 extension: max rel g_MOG "
    + ", ".join(f"{v:.2e}" for v in k2ext.values()))
RES["K2"] = dict(max_rel=k2, D_EXT_truncated_10Rd=k2ext)
k4 = {}
for a_s in (5.0, 50.0):
    ed = np.linspace(0, a_s, 4001); Mu_ = (ed / a_s) ** 3; s4 = 0.5 * (ed[:-1] + ed[1:]); dm4 = np.diff(Mu_)
    r4 = np.r_[ed[400::200], a_s * np.array([1.2, 1.5, 2, 3, 5])]
    MN4, MY4 = sph_masses(r4, s4, dm4, MU_PUB); eng = ((1 + ALPHA) * MN4 - ALPHA * MY4) / r4 ** 2
    rho = 3.0 / (4 * np.pi * a_s ** 3); mu = MU_PUB; ma = mu * a_s
    # interior Phi = -4 pi rho/mu^2 + A sinh(mu r)/r, exterior Phi = B e^{-mu r}/r; match value and slope at a (G = 1, M = 1)
    Mx = np.array([[math.sinh(ma) / a_s, -math.exp(-ma) / a_s],
                   [(ma * math.cosh(ma) - math.sinh(ma)) / a_s ** 2, math.exp(-ma) * (1 + ma) / a_s ** 2]])
    Ac, Bc = np.linalg.solve(Mx, [4 * np.pi * rho / mu ** 2, 0.0])
    gy = np.where(r4 <= a_s, Ac * (mu * r4 * np.cosh(mu * r4) - np.sinh(mu * r4)) / r4 ** 2, -Bc * np.exp(-mu * r4) * (1 + mu * r4) / r4 ** 2)
    gn = np.minimum(1.0, (r4 / a_s) ** 3) / r4 ** 2; ref = (1 + ALPHA_PUB) * gn - ALPHA_PUB * gy
    k4[a_s] = float(np.max(np.abs(eng / ref - 1)))
check("K4", max(k4.values()) <= 1e-3, f"uniform sphere a = 5 / 50 kpc, r 0.1-5 a: max rel {k4[5.0]:.2e} / {k4[50.0]:.2e}", "<= 1e-3")
RES["K4"] = dict(max_rel=k4)

# ===================================================================================================== P4: SPARC loader and statistics
say("\n=== (a) SPARC: P4's loader and statistics (exec'd read-only) ===")
P4SRC = os.path.join(P4D, "p4_v3_galaxy_tiles.py"); P4T = open(P4SRC).read(); RES["p4_source_sha256"] = sha(P4SRC)
sys.path.insert(0, P4D)
import p4_solver as S4                               # read-only import (nu1 for the law reference)
with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, CFGD)
    import CFG4_common as C4                         # read-only: footings, the record's SPARC loader
A0 = {f: float(C4.A0[f]) for f in ("canonical", "alt")}
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
NP4 = {"np": np, "math": math, "os": os, "DATA": DATA, "CHI2": CHI2, "LN10": math.log(10.0), "S": S4}
i0_ = P4T.index("KPC_S = 3.0857e19"); j0_ = P4T.index('if want("T1"):', i0_); exec(P4T[i0_:j0_], NP4)
KPC_S, UPS = NP4["KPC_S"], NP4["UPS"]
load_sparc_own, gal_arrays, fit_sample, pooled, t1_line, chi2_label = (NP4[k] for k in ("load_sparc_own", "gal_arrays", "fit_sample", "pooled", "t1_line", "chi2_label"))
GALS = load_sparc_own()
with contextlib.redirect_stdout(io.StringIO()):
    REF = C4.load_sparc()
same = len(REF) == len(GALS) and all(a["name"] == b["name"] and all(np.array_equal(a[k], b[k]) for k in ("R", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"))
                                     and a["meta"] == b["meta"] for a, b in zip(GALS, REF))
R695 = json.load(open(os.path.join(CFGD, "CFG695_saturating_vacuum", "cfg695_results.json")))["numbers"]["S2"]
Rm = np.concatenate([q["R"] for q in GALS]) * KPC_S
Vo = np.concatenate([q["Vobs"] for q in GALS]); eV = np.concatenate([q["eV"] for q in GALS])
Vg = np.concatenate([q["Vgas"] for q in GALS]); Vd = np.concatenate([q["Vdisk"] for q in GALS]); Vb = np.concatenate([q["Vbul"] for q in GALS])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GBa = VB2 * 1e6 / Rm[:, None]; GOa = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GBa)
OKa = (GBa > 0) & (GOa > 0) & np.isfinite(GBa) & np.isfinite(GOa) & (Vo > 0)[:, None]
WWa = np.where(OKa, (1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2)[:, None], 0.0)
rep = {}
for f in A0:
    gb = np.where(OKa, GBa, 1.0)
    r_ = np.log10(np.where(OKa, GOa, 1.0)) - np.log10(np.where(OKa, S4.nu1(gb / A0[f]) * gb, 1.0))
    mse = (WWa * r_ ** 2).sum(0) / WWa.sum(0); i = int(np.argmin(mse)); rep[f] = dict(rms=math.sqrt(mse[i]), U=float(UPS[i]))
dr1 = max(abs(rep[f]["rms"] - R695[f]["rms"]) for f in A0); ur1 = all(rep[f]["U"] == R695[f]["U"] for f in A0)
check("R1", same and dr1 <= 1e-4 and ur1, f"loader_equal={same}; CFG695 S2 {rep['canonical']['rms']:.4f}@{rep['canonical']['U']:.2f} / "
      f"{rep['alt']['rms']:.4f}@{rep['alt']['U']:.2f}; max|drms| {dr1:.1e}", "equal; <= 1e-4; U equal")
P4J = json.load(open(os.path.join(P4D, "p4_v3_galaxy_tiles_results.json")))["tiles"]["T1"]["footings"]
LAW = {}; dr2 = []; okr2 = True
for f in A0:
    LG = {}
    for q in GALS:
        GB, GO, OK, W = gal_arrays(q, UPS); LG[q["name"]] = np.log10(np.where(GB > 0, S4.nu1(np.maximum(GB, 1e-300) / A0[f]) * np.maximum(GB, 1e-300), 1e-300))
    st = pooled(fit_sample(GALS, LG)); ref = P4J[f]["iso_perUps"]
    dr2.append(abs(st["rms"] - ref["rms"])); okr2 &= (st["U_median"] == ref["U_median"]) and (st["frac_p_ok"] == ref["frac_p_ok"])
    LAW[f] = dict(iso_perUps={k: st[k] for k in ("N", "rms", "U_median", "chi2nu", "frac_p_ok")},
                  P4_v3_L24={k: P4J[f]["L24"][k] for k in ("rms", "U_median", "chi2nu", "frac_p_ok")})
check("R2", max(dr2) <= 1e-6 and okr2, f"law iso per-galaxy Upsilon rms {LAW['canonical']['iso_perUps']['rms']:.5f} / {LAW['alt']['iso_perUps']['rms']:.5f}, "
      f"median U {LAW['canonical']['iso_perUps']['U_median']:.2f} / {LAW['alt']['iso_perUps']['U_median']:.2f}; max|drms| {max(dr2):.1e}", "<= 1e-6; U, fraction equal")
RES["sparc_law_reference"] = LAW


# ===================================================================================================== (a) MOG on SPARC
def sph_shells_gal(R, V2, n_log=400):
    """P4's spherical mass function for one component, M = V^2 r (km/s)^2 kpc: linear V^2 between points, uniform core inside
    the first point, constant mass beyond the last; shells between edges that include every data radius."""
    ed = np.unique(np.r_[np.logspace(math.log10(R[0] / 30), math.log10(R[-1]), n_log), R])
    v = np.interp(ed, R, V2); M = v * ed
    M = np.where(ed < R[0], V2[0] * R[0] * (ed / R[0]) ** 3, M)
    s = np.r_[ed[0] / 2, np.sqrt(ed[:-1] * ed[1:])]; dm = np.r_[M[0], np.diff(M)]
    return s, dm


def comp_g_sph(R, V2, alpha, mu):
    if not np.any(V2 != 0): return np.zeros_like(R)
    s, dm = sph_shells_gal(R, V2); MN, MY = sph_masses(R, s, dm, mu)
    return ((1 + alpha) * MN - alpha * MY) / R ** 2 * 1e6 / KPC_S


CONV = 1e6 / KPC_S
COMP = {}                                                         # per galaxy: component arrays
for q in GALS:
    R = q["R"]; V2g = np.sign(q["Vgas"]) * q["Vgas"] ** 2; V2d = q["Vdisk"] ** 2; V2b = q["Vbul"] ** 2
    COMP[q["name"]] = dict(R=R, V2g=V2g, V2d=V2d, V2b=V2b, Ag=DF.A(R, V2g), Ad=DF.A(R, V2d))


def mog_components(q, alpha, mu, geom="disc", df=None):
    """g_MOG per unit of each component (gas, disk per unit Upsilon, bulge per unit Upsilon before the 1.4) at the data radii, m/s^2."""
    c = COMP[q["name"]]; R = c["R"]
    if geom == "disc":
        if df is None:
            gg = (c["V2g"] / R + alpha * DF.dg(c["Ag"], mu, R)) * CONV; gd = (c["V2d"] / R + alpha * DF.dg(c["Ad"], mu, R)) * CONV
        else:
            gg = (c["V2g"] / R + alpha * df.dg(df.A(R, c["V2g"]), mu, R)) * CONV; gd = (c["V2d"] / R + alpha * df.dg(df.A(R, c["V2d"]), mu, R)) * CONV
    else:
        gg = comp_g_sph(R, c["V2g"], alpha, mu); gd = comp_g_sph(R, c["V2d"], alpha, mu)
    gb = comp_g_sph(R, c["V2b"], alpha, mu)
    return gg, gd, gb


NEGPTS = {}
def lg_of(gg, gd, gb, q, tag):
    g = gg[:, None] + UPS[None, :] * gd[:, None] + 1.4 * UPS[None, :] * gb[:, None]
    GB, GO, OK, W = gal_arrays(q, UPS); bad = int(np.sum(OK & (g <= 0)))
    if bad: NEGPTS[tag] = NEGPTS.get(tag, 0) + bad
    return np.log10(np.maximum(g, 1e-300))


def run_sparc(alpha, mu, geom="disc", tag="", df=None):
    LG = {}
    for q in GALS:
        gg, gd, gb = mog_components(q, alpha, mu, geom, df); LG[q["name"]] = lg_of(gg, gd, gb, q, tag)
    return LG


def summarize(rows, st):
    U = np.array([x["U_rms"] for x in rows]); out = {k: st[k] for k in ("N", "rms", "U_median", "U_q", "chi2", "dof", "chi2nu", "frac_p_ok", "chi2nu_median")}
    out["line_pass"] = t1_line(st); out["chi2_line"] = chi2_label(st["frac_p_ok"])
    out["frac_U_at_1p20"] = float(np.mean(U >= 1.2 - 1e-9)); out["frac_U_at_0p30"] = float(np.mean(U <= 0.30 + 1e-9))
    cls = {"small": [], "large": []}
    for x in rows:
        m = next(g for g in GALS if g["name"] == x["name"])["meta"]; Mb = 1.33 * m["MHI"] * 1e9 + x["U_rms"] * m["L36"] * 1e9
        cls["small" if Mb <= 3e9 else "large"].append(x["wmean"])
    out["classes_at_best_U"] = {k: dict(N=len(v), mean=float(np.mean(v)), se=float(np.std(v, ddof=1) / math.sqrt(len(v)))) for k, v in cls.items()}
    out["readingB_Upsilon_from_cov_chi2"] = st["readingB_Upsilon_from_cov_chi2"]
    return out


SP = {}
t1 = time.time()
LGP = run_sparc(ALPHA, MU_PUB, "disc", "primary"); rows_p = fit_sample(GALS, LGP); SP["primary"] = summarize(rows_p, pooled(rows_p))
SP["primary"]["per_galaxy"] = [dict(name=x["name"], U=x["U_rms"], wmean=x["wmean"], chi2=x["chi2"], dof=x["dof"], p=x["p"]) for x in rows_p]
SP["primary"]["Q_le_2"] = summarize([x for x in rows_p if x["Q"] <= 2], pooled(rows_p, lambda x: x["Q"] <= 2))
rows_pr = fit_sample(GALS, LGP, prior=True); SP["primary"]["prior_Chae"] = summarize(rows_pr, pooled(rows_pr))
LGS = run_sparc(ALPHA, MU_PUB, "sph", "gsph"); rows_s = fit_sample(GALS, LGS); SP["G_SPH"] = summarize(rows_s, pooled(rows_s))
LGN = {}
for q in GALS:
    GB, GO, OK, W = gal_arrays(q, UPS); LGN[q["name"]] = np.log10(np.where(GB > 0, GB, 1e-300))
rows_n = fit_sample(GALS, LGN); SP["newton"] = summarize(rows_n, pooled(rows_n))
dnewt = max(float(np.max(np.abs(np.where(gal_arrays(q, UPS)[0] > 0, LGP[q["name"]] - LGN[q["name"]], 0.0)))) for q in GALS)
RES["mutate_info_max_dlog_vs_newton"] = dnewt
SP["corners"] = {}
for (a_, m_) in CORNERS:
    LGc = run_sparc(0.0 if MUT else a_, m_, "disc", f"corner{a_}_{m_}"); rc = fit_sample(GALS, LGc)
    SP["corners"][f"alpha{a_}|mu{m_}"] = summarize(rc, pooled(rc))
say(f"  MOG on SPARC computed ({time.time() - t1:.0f} s); points with g_MOG <= 0 where g_bar > 0: {NEGPTS if NEGPTS else 'none'}")
RES["neg_points"] = NEGPTS
# K3: disc-engine convergence (grid x2 points, range x10 at both ends), every galaxy at Upsilon 0.5
DF2 = DiscFFT(rmin=1e-5, rmax=1e7, n=8192); k3 = 0.0
for q in GALS:
    a = mog_components(q, ALPHA_PUB, MU_PUB, "disc"); b = mog_components(q, ALPHA_PUB, MU_PUB, "disc", df=DF2)
    ga = a[0] + 0.5 * a[1] + 0.7 * a[2]; gb_ = b[0] + 0.5 * b[1] + 0.7 * b[2]; ok = (ga > 0) & (gb_ > 0)
    if ok.any(): k3 = max(k3, float(np.max(np.abs(np.log10(ga[ok]) - np.log10(gb_[ok])))))
check("K3", k3 <= 1e-3, f"disc engine grid x2, range x10: max |dlog g| {k3:.2e} dex (175 galaxies, Upsilon 0.5)", "<= 1e-3 dex")
guard("sparc")
# S1 side reading: parameter-free alpha(M), mu(M) per trial Upsilon (PRIMARY geometry)
if not MUT:
    LG1 = {}; A1rng = []
    for q in GALS:
        m = q["meta"]; c = COMP[q["name"]]; R = c["R"]; g = np.empty((len(R), len(UPS)))
        for j, U in enumerate(UPS):
            Mb = (1.33 * m["MHI"] + U * m["L36"]) * 1e9; al = float(s1_alpha(Mb)); mu = float(s1_mu(Mb)); A1rng.append((al, mu))
            gg = (c["V2g"] / R + al * DF.dg(c["Ag"], mu, R)) * CONV; gd = (c["V2d"] / R + al * DF.dg(c["Ad"], mu, R)) * CONV
            gb = comp_g_sph(R, c["V2b"], al, mu)
            g[:, j] = gg + U * gd + 1.4 * U * gb
        LG1[q["name"]] = np.log10(np.maximum(g, 1e-300))
    r1s = fit_sample(GALS, LG1); SP["S1_parameter_free"] = summarize(r1s, pooled(r1s))
    A1rng = np.array(A1rng); SP["S1_parameter_free"]["alpha_range_16_50_84"] = np.percentile(A1rng[:, 0], [16, 50, 84]).tolist()
    SP["S1_parameter_free"]["mu_range_16_50_84"] = np.percentile(A1rng[:, 1], [16, 50, 84]).tolist()
RES["sparc"] = SP
for k in ("primary", "G_SPH", "newton"):
    s_ = SP[k]; say(f"  {k:8s}: rms {s_['rms']:.4f} dex, median U {s_['U_median']:.2f} (16-84 {s_['U_q'][0]:.2f}-{s_['U_q'][1]:.2f}), at U=1.20 {s_['frac_U_at_1p20']:.2f}, "
                    f"chi2/dof {s_['chi2nu']:.2f}, frac p>=1e-3 {s_['frac_p_ok']:.3f} -> line {'PASS' if s_['line_pass'] else 'FAIL'}, chi2 line {s_['chi2_line']}; "
                    f"small {s_['classes_at_best_U']['small']['mean']:+.3f}+-{s_['classes_at_best_U']['small']['se']:.3f} large {s_['classes_at_best_U']['large']['mean']:+.3f}+-{s_['classes_at_best_U']['large']['se']:.3f}")
for k in ("Q_le_2", "prior_Chae"):
    s_ = SP["primary"][k]; say(f"  primary {k}: rms {s_['rms']:.4f}, median U {s_['U_median']:.2f} -> line {'PASS' if s_['line_pass'] else 'FAIL'}")
for k, s_ in SP["corners"].items(): say(f"  corner {k}: rms {s_['rms']:.4f}, median U {s_['U_median']:.2f} -> line {'PASS' if s_['line_pass'] else 'FAIL'}")
if "S1_parameter_free" in SP:
    s_ = SP["S1_parameter_free"]; say(f"  S1 (side, no weight): rms {s_['rms']:.4f}, median U {s_['U_median']:.2f}, chi2 line {s_['chi2_line']}; alpha 16/50/84 "
                                      f"{np.round(s_['alpha_range_16_50_84'], 2).tolist()}, mu {np.round(s_['mu_range_16_50_84'], 3).tolist()} /kpc")
for f in A0: say(f"  law {f}: iso per-U rms {LAW[f]['iso_perUps']['rms']:.4f} (median U {LAW[f]['iso_perUps']['U_median']:.2f}); P4 v3 L*24 rms {LAW[f]['P4_v3_L24']['rms']:.4f}")
# class (frozen)
pl, sl = SP["primary"]["line_pass"], SP["G_SPH"]["line_pass"]
SPARC_CLASS = "PASS" if (pl and sl) else ("FAIL" if (not pl and not sl) else "UNDECIDED (geometry-dependent)")
flips = [k for k, s_ in SP["corners"].items() if s_["line_pass"] != pl] + [k for k in ("prior_Chae", "Q_le_2") if SP["primary"][k]["line_pass"] != pl]
SPARC_QUAL = "FRAGILE" if flips else "ROBUST"
RES["sparc_class"] = dict(cls=SPARC_CLASS, qualifier=SPARC_QUAL, flips=flips, chi2_line=SP["primary"]["chi2_line"])
say(f"  SPARC class: {SPARC_CLASS} ({SPARC_QUAL}{': ' + ', '.join(flips) if flips else ''}); chi2 line {SP['primary']['chi2_line']}")

# ===================================================================================================== (b) clusters: F1 + X2 exec'd read-only
say("\n=== (b) clusters: X2's replay npz, F1/X2 functions exec'd read-only ===")
X2SRC = os.path.join(X2D, "x2_cluster_outskirts.py"); X2T = open(X2SRC).read(); RES["x2_source_sha256"] = sha(X2SRC)
RES["f1_source_sha256"] = sha(os.path.join(F1D, "f1_cluster_cores.py")); RES["replay_npz_sha256"] = sha(os.path.join(X2D, "x2_replay_percluster.npz"))
def cutx(a, b): i = X2T.index(a); j = X2T.index(b, i); return X2T[i:j]
XN = {"np": np, "os": os, "sys": sys, "math": math, "REB": REB, "REPO": REPO, "HERE": X2D, "sha": sha, "RES": {}, "say": say, "MUT": False,
      "guard": guard, "CTAB": {}, "Cof": None, "N9": {}, "debris": None}
with contextlib.redirect_stdout(io.StringIO()):
    exec(cutx("F1SRC = os.path.join(REB", "# ============================================================== data: the replay"), XN)
exec(cutx("NPZ = os.path.join(HERE", "# ============================================================== statistics"), XN)
for a_, b_ in (("PB = [3, 4, 5, 6, 7]", "# ============================================================== projector"),
               ("def project_floor(", "# ============================================================== gas profiles"),
               ("def gas(Mg500, R500, shape):", "# ============================================================== EFE"),
               ("def model(cl, foot, hk,", "# ============================================================== K2, K3, K7")):
    exec(cutx(a_, b_), XN)
G, MSUN, MPC, KG_PC2 = XN["G"], XN["MSUN"], XN["MPC"], XN["KG_PC2"]
RG, RM, RC, DM, DA_lcdm, HV, HK = XN["RG"], XN["RM"], XN["RC"], XN["DM"], XN["DA_lcdm"], XN["HV"], XN["HK"]
CL, N, DAT, ALL, TERC, X = XN["CL"], XN["N"], XN["DAT"], XN["ALL"], XN["TERC"], XN["X"]
stats, jk, gas, redfac, stack_model = XN["stats"], XN["jk"], XN["gas"], XN["redfac"], XN["stack_model"]
project_floor, offset_floor, dsig_from_sig, at_bins, sig_bins = (XN[k] for k in ("project_floor", "offset_floor", "dsig_from_sig", "at_bins", "sig_bins"))
X2J = json.load(open(os.path.join(X2D, "x2_cluster_outskirts_results.json")))
CELLS4 = [(f, h) for f in ("canonical", "alt") for h in HK]
# R3: C0 law; R4: (a1), (d), (e) law rows
def lawrow(label, conv="boost", sysx=False, **kw):
    out = {}
    for f, hk in CELLS4:
        out[f"{f}|{hk}"] = stats(hk, stack_model(f, hk, **kw)[0], conv, ALL, sysx)
    return out
def devrow(mine, label, sysx):
    ref = X2J["rows"][label]["boost"]; dA = 0.0; dc = 0.0
    for c in mine:
        for b in ("MID", "OUTER"):
            dA = max(dA, abs(mine[c][b]["A"] - ref[c][b]["A"]), abs(mine[c][b]["s_tot" if sysx else "s_jk"] - ref[c][b]["s_tot" if sysx else "s_jk"]))
        dc = max(dc, abs(mine[c]["chi2"] - ref[c]["chi2"]))
    return dA, dc
LAWC0 = lawrow("C0"); dA3, dc3 = devrow(LAWC0, "C0 (F1 PRIMARY)", False)
check("R3", dA3 <= 1e-6 and dc3 <= 1e-3, f"law C0 vs X2 JSON: max|dA|,|dsigma| {dA3:.1e}; max|dchi2| {dc3:.1e}; A_MID can/alt h0672 "
      f"{LAWC0['canonical|h0672']['MID']['A']:.3f}/{LAWC0['alt|h0672']['MID']['A']:.3f}", "<= 1e-6; <= 1e-3")
L_a1 = lawrow("a1", gasshape="P"); L_d = lawrow("d", red=True); L_e = lawrow("e", sysx=True)
d4 = [devrow(L_a1, "(a1) CFG814 gas: r^-3 beyond 2.2 R500", False), devrow(L_d, "(d) reduced shear", False), devrow(L_e, "(e) systematics propagated", True)]
check("R4", max(x[0] for x in d4) <= 1e-6 and max(x[1] for x in d4) <= 1e-3, f"law (a1)/(d)/(e): max|dA|,|dsigma| {max(x[0] for x in d4):.1e}; max|dchi2| {max(x[1] for x in d4):.1e}", "<= 1e-6; <= 1e-3")
LAWCS = {c: X2J["rows"]["C* corrected baseline"]["boost"][c] for c in X2J["rows"]["C* corrected baseline"]["boost"]}
# R5: F1's Newtonian baryons at h 0.70 (record recipe), F1's own predict() and F1's projector
F1J = json.load(open(os.path.join(F1D, "f1_cluster_cores_results.json")))
D70 = X["D"][:, 0]; E70 = X["E"][:, 0]; W70 = np.where(E70 < 1e8, 1 / E70 ** 2, 0)
P70 = np.array([XN["predict_f1"](cl, 0.0, kernel="aqual", hkey="h070") for cl in CL]); a70 = jk(D70, P70, W70)
d5 = max(abs(a70["MID"][0] - F1J["newton_h070"]["MID"][0]), abs(a70["OUTER"][0] - F1J["newton_h070"]["OUTER"][0]))
check("R5", d5 <= 1e-4, f"F1 Newtonian baryons h0.70: MID {a70['MID'][0]:.3f}+-{a70['MID'][1]:.3f} OUTER {a70['OUTER'][0]:.3f}+-{a70['OUTER'][1]:.3f}; max|d| {d5:.1e}", "<= 1e-4")
RES["clusters_reference"] = dict(law_C0=LAWC0, law_Cstar_X2=LAWCS, newton_h070_F1recipe=a70)
guard("cluster refs")


# ===================================================================================================== (b) MOG on the stack
def lens(cl, h, ML):
    rho = np.gradient(ML, RM) / (4 * np.pi * RM ** 2); Sig = project_floor(rho)
    d = np.radians(cl["off_deg"]) * float(DM(cl["z"], h)) / (1 + cl["z"]); So = offset_floor(Sig, d)
    return at_bins(dsig_from_sig(So)) / KG_PC2, sig_bins(So)


NEWT = {}
def newton_parts(hk, gasshape):
    key = (hk, gasshape)
    if key in NEWT: return NEWT[key]
    h = HV[hk]; P = np.empty((N, 8)); Sb = np.empty((N, 8)); MB = np.empty((N, len(RG))); RHO = np.empty((N, len(RG)))
    for i, cl in enumerate(CL):
        q = (float(DM(cl["z"], h)) / (1 + cl["z"])) / DA_lcdm(cl["z"])
        if gasshape == "G2":                                             # A3 diagnostic: F1's C3c G2, gas inside R500 only
            Mg = XN["gas_mass_f1"](cl, cl["Mgas500"] * q ** 2.5, cl["R500"] * q, "G2"); rg = np.zeros_like(RG)
        else:
            Mg, rg = gas(cl["Mgas500"] * q ** 2.5, cl["R500"] * q, gasshape)
        MB[i] = Mg * 1.2; RHO[i] = rg; P[i], Sb[i] = lens(cl, h, MB[i])
    NEWT[key] = (P, Sb, MB, RHO); guard("newton_parts"); return NEWT[key]


YM = None
def ymat():
    global YM
    if YM is None:
        s = np.sqrt(RG[:-1] * RG[1:]); YM = np.empty((len(RG), len(s)))
        for a in range(0, len(RG), 40): YM[a:a + 40] = yfac(RG[a:a + 40, None], s[None, :], MU_PUB * 1e3)    # Mpc^-1; A2 chunk
    return YM


def mog_P(hk, gasshape, red, mode="PH", alpha=None):
    """(N, 8) model.  PH: Sigma = (1 + alpha) Sigma_N (light feels G0 only); VDYN: dynamical mass r^2 g_MOG/G_N (sph engine);
    S1: (1 + alpha(M_b)) Sigma_N; S2: BM06 running G(r) dynamical mass."""
    al = ALPHA if alpha is None else alpha
    Pn, Sbn, MB, RHO = newton_parts(hk, gasshape); h = HV[hk]
    if mode == "PH":
        P = (1 + al) * Pn; Sb = (1 + al) * Sbn
    else:
        P = np.empty((N, 8)); Sb = np.empty((N, 8))
        for i, cl in enumerate(CL):
            Mb = MB[i]
            if mode == "VDYN":
                ML = (1 + al) * Mb - al * (ymat() @ np.diff(Mb))
            elif mode == "S1":
                a1 = float(s1_alpha(Mb[-1] / MSUN)); ML = (1 + a1) * Mb
            elif mode == "S2":
                below = np.nonzero((RHO[i] < 1e-25) & (RG > 1e-2))[0]; rout = min(float(RG[below[0]]) if below.size else 3.0, 3.0)
                Mgo = float(np.interp(rout, RG, Mb / 1.2)) / MSUN; M0 = 58.8e14 * (Mgo / 1e14) ** 0.39 * MSUN
                r0 = rout / 10 if rout <= 0.65 else 0.1392; x = RG / r0
                ML = Mb + np.sqrt(M0 * np.maximum(Mb, 0)) * (1 - np.exp(-x) * (1 + x))
            P[i], Sb[i] = lens(cl, h, ML)
    if red:
        P = P.copy()
        for i in range(N): P[i] = P[i] * redfac(hk, i, Sb[i])[0]
    return P


SETUPS = {"C0": dict(gasshape="G0", red=False, sysx=False), "Cstar": dict(gasshape="P", red=True, sysx=True)}
def grade(mode="PH", conv="boost", alpha=None, sel=ALL, setups=None):
    out = {}
    for su, kw in (setups or SETUPS).items():
        out[su] = {}
        for hk in HK:
            st = stats(hk, mog_P(hk, kw["gasshape"], kw["red"], mode, alpha), conv, sel, kw["sysx"])
            st.pop("resid", None)
            st["line"] = bool(st["chi2"] <= 11.07 and abs(st["Z_MID"]) <= 2 and abs(st["Z_OUT"]) <= 2); out[su][hk] = st
        out[su]["line_both_h"] = all(out[su][hk]["line"] for hk in HK); out[su]["line_any_h"] = any(out[su][hk]["line"] for hk in HK)
    return out


def show(lab, g, setups=None):
    for su in (setups or SETUPS):
        for hk in HK:
            s_ = g[su][hk]; u = "s_tot" if (setups or SETUPS)[su]["sysx"] else "s_jk"
            say(f"  {lab:28s} {su:5s} {hk}: MID {s_['MID']['A']:.3f}+-{s_['MID'][u]:.3f} (Z {s_['Z_MID']:+.2f})  OUT {s_['OUTER']['A']:.3f}+-{s_['OUTER'][u]:.3f} "
                f"(Z {s_['Z_OUT']:+.2f})  INNER {s_['INNER']['A']:.2f}  chi2 {s_['chi2']:.1f}  -> line {'MET' if s_['line'] else 'NOT MET'}")


t1 = time.time(); CLR = {}
CLR["PH"] = grade("PH"); show("P-PH (primary)", CLR["PH"])
CLR["PH_clip"] = grade("PH", conv="clip"); show("P-PH clipped boost", CLR["PH_clip"])
for a_ in (8.55, 9.23):
    CLR[f"PH_alpha{a_}"] = grade("PH", alpha=0.0 if MUT else a_); show(f"P-PH alpha {a_}", CLR[f"PH_alpha{a_}"])
CLR["VDYN"] = grade("VDYN"); show("V-DYN (brief's reading)", CLR["VDYN"])
PN0 = newton_parts("h0672", "G0")[0]; PV0 = mog_P("h0672", "G0", False, "VDYN"); PP0 = mog_P("h0672", "G0", False, "PH")
CLR["VDYN_over_PH_bins3to7"] = dict(median=float(np.median(PV0[:, 3:] / PP0[:, 3:])), min=float(np.min(PV0[:, 3:] / PP0[:, 3:])), max=float(np.max(PV0[:, 3:] / PP0[:, 3:])))
say(f"  V-DYN / P-PH model ratio, bins 3-7, C0 h0672: median {CLR['VDYN_over_PH_bins3to7']['median']:.4f} (min {CLR['VDYN_over_PH_bins3to7']['min']:.4f}, max {CLR['VDYN_over_PH_bins3to7']['max']:.4f})")
newt = {}
for hk in HK:
    st = stats(hk, newton_parts(hk, "G0")[0], "boost", ALL, False); newt[hk] = dict(MID=st["MID"], OUTER=st["OUTER"], chi2=st["chi2"])
CLR["newton_C0"] = newt
say("  Newtonian baryons at C0 (floored projector): " + "  ".join(f"{hk}: MID {newt[hk]['MID']['A']:.3f} OUTER {newt[hk]['OUTER']['A']:.3f}" for hk in HK))
terc = {}
for t, sel in TERC.items():
    terc[t] = {}
    for hk in HK:
        st = stats(hk, mog_P(hk, "G0", False, "PH"), "boost", sel, False); terc[t][hk] = dict(MID=st["MID"], OUTER=st["OUTER"], chi2=st["chi2"], Z_MID=st["Z_MID"], Z_OUT=st["Z_OUT"])
    say(f"  tercile {t} (P-PH, C0): " + "  ".join(f"{hk}: MID {terc[t][hk]['MID']['A']:.3f}+-{terc[t][hk]['MID']['s_jk']:.3f} OUT {terc[t][hk]['OUTER']['A']:.3f}+-{terc[t][hk]['OUTER']['s_jk']:.3f}" for hk in HK))
CLR["terciles_C0_PH"] = terc
if not MUT:
    CLR["S1"] = grade("S1"); show("S1 parameter-free alpha(M)", CLR["S1"])
    a1s = [float(s1_alpha(newton_parts("h0672", "G0")[2][i, -1] / MSUN)) for i in range(N)]
    CLR["S1_alpha_16_50_84"] = np.percentile(a1s, [16, 50, 84]).tolist(); say(f"    S1 alpha(M_b) 16/50/84: {np.round(CLR['S1_alpha_16_50_84'], 2).tolist()}")
    CLR["S2"] = grade("S2"); show("S2 BM06 MSTG clusters", CLR["S2"])
say(f"  clusters computed ({time.time() - t1:.0f} s, peak RSS {rss():.3f} GB)")
for k in ("PH", "PH_clip", "PH_alpha8.55", "PH_alpha9.23", "VDYN", "S1", "S2"):
    if k in CLR:
        for su in SETUPS: CLR[k][su] = {kk: vv for kk, vv in CLR[k][su].items()}
# A3 (POST-RESULT diagnostic, no class weight): does the cluster outcome rest on the gas beyond R500?  X2's bracket (a3)
# (rho ~ r^-3 from R500) and F1's G2 (gas inside R500 only), at both setups; and the corner most favourable to MOG
# (G2 gas, clipped boost, alpha 8.55).
SU_A3 = {"C0|a3": dict(gasshape="R5", red=False, sysx=False), "C*|a3": dict(gasshape="R5", red=True, sysx=True),
         "C0|G2": dict(gasshape="G2", red=False, sysx=False), "C*|G2": dict(gasshape="G2", red=True, sysx=True)}
say("  A3 diagnostic (POST-RESULT, no class weight): gas beyond R500")
CLR["A3_gas_beyond_R500"] = grade("PH", setups=SU_A3); show("P-PH, gas bracket", CLR["A3_gas_beyond_R500"], SU_A3)
SU_F = {"C0|G2": SU_A3["C0|G2"], "C*|G2": SU_A3["C*|G2"]}
CLR["A3_favourable_G2_clip_a8.55"] = grade("PH", conv="clip", alpha=0.0 if MUT else 8.55, setups=SU_F); show("P-PH G2+clip+alpha 8.55", CLR["A3_favourable_G2_clip_a8.55"], SU_F)
RES["clusters"] = CLR
# class (frozen)
def ccls(g):
    c0, cs = g["C0"]["line_both_h"], g["Cstar"]["line_both_h"]; c0n, csn = not g["C0"]["line_any_h"], not g["Cstar"]["line_any_h"]
    if c0 and cs: return "PASS"
    if c0n and csn: return "FAIL"
    if cs and c0n: return "UNDECIDED (MET ONLY WITH (e): C* met, C0 not)"
    if c0 and csn: return "UNDECIDED (MET ONLY AT C0)"
    return "UNDECIDED (h split)"
def outcome(g): return (g["C0"]["line_both_h"], g["C0"]["line_any_h"], g["Cstar"]["line_both_h"], g["Cstar"]["line_any_h"])
CL_CLASS = ccls(CLR["PH"]); quals = []
if outcome(CLR["PH_clip"]) != outcome(CLR["PH"]): quals.append("BOOST-DEPENDENT")
if any(outcome(CLR[f"PH_alpha{a_}"]) != outcome(CLR["PH"]) for a_ in (8.55, 9.23)): quals.append("PARAMETER-FRAGILE")
if outcome(CLR["VDYN"]) != outcome(CLR["PH"]): quals.append("PRESCRIPTION-DEPENDENT")
RES["cluster_class"] = dict(cls=CL_CLASS, qualifiers=quals)
say(f"  CLUSTER class: {CL_CLASS}{' [' + ', '.join(quals) + ']' if quals else ''}")
# overall (frozen)
fails = [n for n, c in (("SPARC", SPARC_CLASS), ("CLUSTERS", CL_CLASS)) if c == "FAIL"]
if SPARC_CLASS == "PASS" and CL_CLASS == "PASS": OV = "MOG UNIVERSAL SET PASSES BOTH"
elif fails: OV = "MOG UNIVERSAL SET FAILS (" + (" + ".join(fails) if len(fails) < 2 else "BOTH") + ")"
else: OV = "MOG UNIVERSAL SET UNDECIDED (" + ", ".join(n for n, c in (("SPARC", SPARC_CLASS), ("CLUSTERS", CL_CLASS)) if c.startswith("UNDECIDED")) + ")"
other = [f"{n} {c}" for n, c in (("SPARC", SPARC_CLASS), ("CLUSTERS", CL_CLASS))]
RES["overall"] = OV
say(f"\nVERDICT (frozen classes): {OV}   [{'; '.join(other)}]")
if MUT:
    say(f"MUTATE info: engines at alpha = 0 reproduce Newton: SPARC max |dlog g| vs g_bar {dnewt:.1e}; cluster P-PH = Newtonian model "
        f"(C0 h0672 MID {CLR['PH']['C0']['h0672']['MID']['A']:.3f} vs Newtonian {newt['h0672']['MID']['A']:.3f})")
check("K5", rss() < 1.0, f"peak RSS {rss():.3f} GB", "< 1 GB")
npass = sum(ok for _, ok in CHECKS); RES["n_checks_pass"] = npass; RES["n_checks"] = len(CHECKS); RES["runtime_s"] = time.time() - T0
say(f"X9_MOG_STVG_CHECK COMPLETE: {npass}/{len(CHECKS)} checks PASS ({time.time() - T0:.0f} s).")
json.dump(RES, open(os.path.join(HERE, f"x9_mog_stvg_check_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
sys.exit(0 if npass == len(CHECKS) else 1)
