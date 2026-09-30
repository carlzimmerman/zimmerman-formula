#!/usr/bin/env python3
"""CFG197 pre-flight -- can the gas-floor test discriminate the flat a0 from a0 proportional to H(z) at all?

Frozen criteria: campaign_fresh_gravity/CFG197_FROZEN_CRITERIA.md (written before this script ran).
PHASE 1 ONLY: uses M_star, the radius r and z (plus catalogue flags and, for Roman-Oliveira, the measured H2 mass).
NO dynamical mass, rotation velocity, dispersion or f_DM value is read: a column guard refuses them at load time.

For each galaxy and law L in {flat, rival (a0 E(z))}: x_L = g_star(r)/a0_L(z); the law's gas-free FLOOR nu(x_L) on M_dyn/M_star.
Discriminability (frozen rule): D0 = -median log s_req^rival(R_hyp), R_hyp = nu_P2(x_flat) (a gas-free population sitting on
the flat floor); CAN if D0 >= 0.30 in both footings, MARGINAL if 0.20 <= D0 < 0.30, CANNOT if D0 < 0.20.  D_mu repeats it for
flat-law populations with gas mu inside r (mu = 0.5, 1, 2).  Also the floor separation against the 0.2-0.3 dex M_star systematic.
Roman-Oliveira: the gas-only predicted floor on g_obs (stars only add), as a minimum circular speed per law -- no velocity used.
Controls C1-C7; MUTATE=1 forces E(z) = 1 and swaps the lemma check to L5's switch law: C6 and C7 must then FAIL (exit 1).
Run: python3 campaign_fresh_gravity/CFG197_gas_floor_highz/CFG197_preflight.py   [MUTATE=1 for the control run]
"""
import os, sys, re, csv, math, json, builtins
import numpy as np
from scipy.special import i0, k0, i1, k1

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
SLUG = "CFG197_preflight" + ("_MUTATE" if MUT else "")

LINES, CHECKS, NUM = [], [], {}


def P(s=""):
    print(s, flush=True)
    LINES.append(s)


def check(name, detail, ok, load_bearing=True):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")


def banner(s):
    P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)


P(__doc__.split("Run: python3")[0].strip())
if MUT:
    P("\n*** MUTATE=1: E(z) forced to 1 for the rival; lemma check C6 uses L5's switch law.  C6 and C7 must FAIL. ***")

# ================================================================================================= constants
G, MSUN, KPC = K.G_SI, K.MSUN, K.KPC
A0 = dict(K.A0)
FOOTS = K.FOOTS
OM = C.OM_PL
assert abs(OM - 0.3153) < 1e-12
E = (lambda z: 1.0) if MUT else (lambda z: math.sqrt(OM * (1 + z) ** 3 + 1 - OM))
RE_RD = 1.6783469900166625          # R_e/R_d of an exponential disc (1 - (1 + t) e^-t = 1/2)
UV2HA = 1.58                        # Danhaive's UV -> H-alpha size factor (the 'compact stars' alternative)
K_TOT = 1.8                         # Price+2022 virial coefficient (q0 = 0.2), as used by Danhaive
F_THICK = 2.0 / K_TOT
MUS = (0.0, 0.5, 1.0, 2.0)
SEED, NBOOT = 197, 4000
KERN = {"P2": K.nu_p2, "nu_mono": K.nu_mono}
LAWS = ("flat", "rival")


def a0_law(foot, law, z):
    return A0[foot] * (E(z) if law == "rival" else 1.0)


# ================================================================================================= the column guard (phase-1 rule)
FORBID = re.compile(r"(mdyn|vrot|^v_|_v_|vobs|vmax|vext|v_at|v_over|sigma0_kms$|sigma0_kms_err|sigma_|fdm|mtot|vcirc|jstar)", re.I)
LOADED = []


def load(fname, cols):
    """read ONLY the named columns; refuse any kinematic / dynamical column (flags ending _lim/_flag are catalogue flags)."""
    for c in cols:
        if FORBID.search(c) and not (c.endswith("_lim") or c.endswith("_flag")):
            raise PermissionError(f"phase 1 refuses column {c!r} of {fname}")
    rows = []
    with builtins.open(os.path.join(AT, fname)) as fh:
        for r in csv.DictReader(fh):
            rows.append({c: r[c] for c in cols})
    LOADED.append((fname, tuple(cols)))
    return rows


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return float("nan")


# ================================================================================================= geometry of g_star
def g_freeman(M, R, Rd):
    """razor-thin exponential disc midplane radial acceleration (Freeman 1970)."""
    y = R / (2.0 * Rd)
    return 2.0 * G * M * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y)) / (Rd * R)


def f_enc(t):
    return 1.0 - (1.0 + t) * math.exp(-t)


F_ENC_COMPACT = f_enc(RE_RD * UV2HA)          # 0.7425
VARIANTS = [("sph", "mlf"), ("thick", "mlf"), ("thin", "mlf"), ("sph", "compact"), ("thick", "compact"), ("thin", "compact")]
PRIMARY = ("sph", "mlf")


def gstar(M_msun, r_kpc, geom, rad, frac_mlf=0.5, rhalf_over_r=1.0):
    """g_star(r) in m/s^2.  mlf: M(<r) = frac_mlf M (0.5 at r_e); compact: stellar half-mass radius = r_half/1.58."""
    M, R = M_msun * MSUN, r_kpc * KPC
    rhalf = rhalf_over_r * R                                   # the stellar half-light radius (= r unless a 3 R_D radius)
    if rad == "mlf":
        Rd, fsph = rhalf / RE_RD, frac_mlf
    else:
        Rd = (rhalf / UV2HA) / RE_RD
        fsph = f_enc(R / Rd)
    if geom == "sph":
        return G * fsph * M / R ** 2
    if geom == "thick":
        return F_THICK * G * fsph * M / R ** 2
    return float(g_freeman(M, R, Rd))


# ================================================================================================= s_req
def phi_inv(k, t, nit=90):
    """Phi_k^-1(t), Phi(y) = y nu_k(y), by log-space bisection on [1e-14, t] (Phi(y) >= y, so the root is <= t)."""
    t = np.asarray(t, float)
    lo, hi = np.full_like(t, math.log(1e-14)), np.log(np.maximum(t, 1e-14))
    for _ in range(nit):
        mid = 0.5 * (lo + hi)
        ym = np.exp(mid)
        big = ym * KERN[k](ym) > t
        hi = np.where(big, mid, hi)
        lo = np.where(big, lo, mid)
    return np.exp(0.5 * (lo + hi))


def log_sreq(k, x, R):
    x, R = np.asarray(x, float), np.asarray(R, float)
    if k == "Newton":
        return np.log10(R)
    if k == "P2":
        return np.log10(2.0 * x * R ** 2 / (np.sqrt(1.0 + 4.0 * x ** 2 * R ** 2) + 1.0))
    return np.log10(phi_inv(k, x * R) / x)


def boot_median(v, rng):
    v = np.asarray(v, float)
    idx = rng.integers(0, len(v), size=(NBOOT, len(v)))
    m = np.median(v[idx], axis=1)
    return dict(median=float(np.median(v)), p5=float(np.percentile(m, 5)), p16=float(np.percentile(m, 16)),
                p84=float(np.percentile(m, 84)), p95=float(np.percentile(m, 95)))


# ================================================================================================= samples
banner("SAMPLES (M_star, r, z and catalogue flags only)")
GAL = []
# --- Danhaive+2025 gold (H-alpha, z 3.8-5.8)
for r in load("danhaive2025_gold.csv", ["jades_id", "z", "logMstar", "logMstar_errhi", "logMstar_errlo", "logMstar_lim", "re_kpc",
                                         "re_kpc_lim", "logMdyn_lim", "sigma0_kms_lim"]):
    GAL.append(dict(sample="danhaive", id=r["jades_id"], z=fnum(r["z"]), logM=fnum(r["logMstar"]), r=fnum(r["re_kpc"]),
                    rhalf=1.0, frac=0.5, flags=("sigma0<" if r["sigma0_kms_lim"] == "<" else ""),
                    inlim=(r["logMstar_lim"] == "" and r["re_kpc_lim"] == "" and r["logMdyn_lim"] == "")))
# --- ALMA-CRISTAL ([CII], z 4.4-5.7): modelled discs with an SED M_star
samp = {r["id"]: r for r in load("cristal2025_sample.csv", ["id", "z_cii", "logMstar"])}
alias = {"09": "09a"}
cr_excl = []
for r in load("cristal2025_dynamics.csv", ["id", "Re_disk_kpc", "Re_disk_kpc_errhi"]):
    sid = alias.get(r["id"], r["id"])
    s_ = samp[sid]
    if not np.isfinite(fnum(s_["logMstar"])):
        cr_excl.append(r["id"])
        continue
    GAL.append(dict(sample="cristal", id=r["id"], z=fnum(s_["z_cii"]), logM=fnum(s_["logMstar"]), r=fnum(r["Re_disk_kpc"]),
                    rhalf=1.0, frac=0.5, flags=("Re_fixed" if not np.isfinite(fnum(r["Re_disk_kpc_errhi"])) else ""), inlim=True))
# --- MSA-3D (z 0.58-1.68): r = R_e,disk (DysmalPy)
mg = {r["id"]: r for r in load("msa3d_galaxies.csv", ["id", "sample", "z", "logMstar", "footnote"])}
for r in load("msa3d_kinematics.csv", ["id", "re_disk_kpc", "sigma0_kms_flag"]):
    g_ = mg[r["id"]]
    fl = ",".join(f for f in (("fn_" + g_["footnote"]) if g_["footnote"] else "", ("sigma0_" + r["sigma0_kms_flag"]) if r["sigma0_kms_flag"] else "") if f)
    GAL.append(dict(sample="msa3d", id=r["id"], z=fnum(g_["z"]), logM=fnum(g_["logMstar"]), r=fnum(r["re_disk_kpc"]),
                    rhalf=1.0, frac=0.5, flags=fl, golden=(g_["sample"] == "golden"), inlim=True))
# --- KURVS-CDFS (z 1.2-1.6): the 10 rotation-supported discs with the paper's f_DM (ids only; no f_DM value read)
ki = {r["kurvs_id"]: r for r in load("kurvs2023_integrated.csv", ["kurvs_id", "z_halpha", "logMstar", "reff_kpc"])}
for r in load("kurvs2023_fdm.csv", ["kurvs_id", "flag_star"]):
    g_ = ki[r["kurvs_id"]]
    GAL.append(dict(sample="kurvs", id=r["kurvs_id"], z=fnum(g_["z_halpha"]), logM=fnum(g_["logMstar"]), r=fnum(g_["reff_kpc"]),
                    rhalf=1.0, frac=0.5, flags=("flag_star" if r["flag_star"] else ""), inlim=True))
    # the declared 3 R_D sensitivity (radius 3 R_eff/1.678, M(<3R_D) = 0.8009 M)
    GAL.append(dict(sample="kurvs3RD", id=r["kurvs_id"], z=fnum(g_["z_halpha"]), logM=fnum(g_["logMstar"]),
                    r=3.0 * fnum(g_["reff_kpc"]) / RE_RD, rhalf=RE_RD / 3.0, frac=f_enc(3.0), flags="", inlim=True))

for g_ in GAL:
    g_["gs"] = {v: gstar(10 ** g_["logM"], g_["r"], *v, frac_mlf=g_["frac"], rhalf_over_r=g_["rhalf"]) for v in VARIANTS}

BINS = {
    "z>3.5 pooled (Danhaive + CRISTAL)": [g for g in GAL if g["sample"] in ("danhaive", "cristal")],
    "  Halpha sub-bin: Danhaive gold": [g for g in GAL if g["sample"] == "danhaive"],
    "  Halpha, V-lim (sigma0 detected)": [g for g in GAL if g["sample"] == "danhaive" and not g["flags"]],
    "  [CII] sub-bin: CRISTAL": [g for g in GAL if g["sample"] == "cristal"],
    "comparison: MSA-3D (all 30)": [g for g in GAL if g["sample"] == "msa3d"],
    "  MSA-3D golden": [g for g in GAL if g["sample"] == "msa3d" and g.get("golden")],
    "comparison: KURVS (10, r = R_eff)": [g for g in GAL if g["sample"] == "kurvs"],
    "  KURVS at 3 R_D (sensitivity)": [g for g in GAL if g["sample"] == "kurvs3RD"],
}
for b, gs in BINS.items():
    zz = [g["z"] for g in gs]
    P(f"  {b:38s} N = {len(gs):3d}   z {min(zz):.2f}-{max(zz):.2f} (median {np.median(zz):.2f}, E = {E(np.median(zz)):.2f})   "
      f"log M* {min(g['logM'] for g in gs):.2f}-{max(g['logM'] for g in gs):.2f}   r {min(g['r'] for g in gs):.2f}-"
      f"{max(g['r'] for g in gs):.2f} kpc   flagged {sum(bool(g['flags']) for g in gs)}")
P(f"  CRISTAL modelled discs excluded for no SED M* (their M* = M_dyn - M_gas would be circular): {cr_excl}")
check("C0 (phase-1 rule) no dynamical-mass, velocity, dispersion or f_DM column was loaded (the guard refuses them; only the listed "
      "columns were read)", "; ".join(f"{f}: {list(c)}" for f, c in LOADED),
      all(not (FORBID.search(c) and not (c.endswith('_lim') or c.endswith('_flag'))) for _, cs in LOADED for c in cs))
nD = len(BINS["  Halpha sub-bin: Danhaive gold"])
nC = len(BINS["  [CII] sub-bin: CRISTAL"])
check("C0b sample counts match the frozen in/out rules (Danhaive 41 with no limit flags on M*, r_e or M_dyn and 17 sigma0 limits; "
      "CRISTAL 12 = 14 minus 10a-E and 23c; MSA-3D 30 / 23 golden; KURVS 10)",
      f"Danhaive {nD} (all in: {all(g['inlim'] for g in BINS['  Halpha sub-bin: Danhaive gold'])}), sigma0 limits "
      f"{sum(g['flags'] == 'sigma0<' for g in BINS['  Halpha sub-bin: Danhaive gold'])}; CRISTAL {nC} (excluded {cr_excl}); "
      f"MSA-3D {len(BINS['comparison: MSA-3D (all 30)'])} / {len(BINS['  MSA-3D golden'])}; KURVS {len(BINS['comparison: KURVS (10, r = R_eff)'])}",
      nD == 41 and nC == 12 and sorted(cr_excl) == ["10a-E", "23c"] and len(BINS["comparison: MSA-3D (all 30)"]) == 30
      and len(BINS["  MSA-3D golden"]) == 23 and len(BINS["comparison: KURVS (10, r = R_eff)"]) == 10
      and sum(g["flags"] == "sigma0<" for g in BINS["  Halpha sub-bin: Danhaive gold"]) == 17)

# ================================================================================================= geometry constants
banner("GEOMETRY CONSTANTS (data-free)")
gt = float(g_freeman(1.0, RE_RD, 1.0)) / (G * 0.5 / RE_RD ** 2)
P(f"  thin exponential disc at R_e: g/(G (M/2)/R_e^2) = {gt:.4f};  thick q0 = 0.2 (2/k_tot) = {F_THICK:.4f};  sphere = 1")
P(f"  compact stars (half-mass radius r/{UV2HA}): M(<r)/M = {F_ENC_COMPACT:.4f} (sphere);  M(<3 R_D)/M = {f_enc(3.0):.4f}")
check("C0c the frozen geometry constants are reproduced (thin 1.2503, compact 0.7425, 3 R_D 0.8009)",
      f"{gt:.4f}, {F_ENC_COMPACT:.4f}, {f_enc(3.0):.4f}", abs(gt - 1.2503) < 1e-4 and abs(F_ENC_COMPACT - 0.7425) < 1e-4
      and abs(f_enc(3.0) - 0.8009) < 1e-4)

# ================================================================================================= floors and separation
rng = np.random.default_rng(SEED)
RES = {}


def bin_numbers(gs, var, foot, k):
    z = np.array([g["z"] for g in gs])
    gsv = np.array([g["gs"][var] for g in gs])
    xf = gsv / np.array([a0_law(foot, "flat", zi) for zi in z])
    xr = gsv / np.array([a0_law(foot, "rival", zi) for zi in z])
    nf, nr = KERN[k](xf), KERN[k](xr)
    out = dict(x_flat=xf, x_rival=xr, floor_flat=nf, floor_rival=nr, dfloor=np.log10(nr / nf))
    for mu in MUS:
        Rh = (1 + mu) * KERN[k]((1 + mu) * xf)                       # a flat-law population with gas mu inside r, no dark mass
        out[f"lsf_{mu}"] = log_sreq(k, xf, Rh)                       # flat: log s_req (0 at mu = 0)
        out[f"lsr_{mu}"] = log_sreq(k, xr, Rh)                       # rival
    return out


banner("PER-GALAXY FLOORS, z > 3.5 (P2, canonical footing, primary variant: sphere, mass follows light)")
P(f"  {'sample':9s} {'id':>9s} {'z':>5s} {'logM*':>6s} {'r kpc':>6s} {'E(z)':>5s} {'x_flat':>7s} {'x_rival':>7s} {'floor_f':>7s} "
  f"{'floor_r':>7s} {'dlog':>6s} {'D0_gal':>6s}  flags")
for b in ("  Halpha sub-bin: Danhaive gold", "  [CII] sub-bin: CRISTAL"):
    gs = BINS[b]
    o = bin_numbers(gs, PRIMARY, "canonical", "P2")
    for i, g in enumerate(gs):
        P(f"  {g['sample']:9s} {g['id']:>9s} {g['z']:5.2f} {g['logM']:6.2f} {g['r']:6.2f} {E(g['z']):5.2f} {o['x_flat'][i]:7.3f} "
          f"{o['x_rival'][i]:7.3f} {o['floor_flat'][i]:7.3f} {o['floor_rival'][i]:7.3f} {o['dfloor'][i]:6.3f} {-o['lsr_0.0'][i]:6.3f}  {g['flags']}")

banner("BIN SUMMARY (primary variant).  dlog = log floor_rival - log floor_flat;  D_mu = -median log s_req^rival for a flat-law "
       "population with gas mu (D0 = gas-free).  [16-84] = bootstrap of the median")
VERD = {}
for b, gs in BINS.items():
    P(f"\n  {b}  (N = {len(gs)})")
    for k in ("P2", "nu_mono"):
        for foot in FOOTS:
            o = bin_numbers(gs, PRIMARY, foot, k)
            bd = boot_median(o["dfloor"], rng)
            bD0 = boot_median(-o["lsr_0.0"], rng)
            Ds = {mu: float(-np.median(o[f"lsr_{mu}"])) for mu in MUS}
            frac03 = float(np.mean(-o["lsr_0.0"] >= 0.30))
            RES[(b, k, foot)] = dict(N=len(gs), median_x_flat=float(np.median(o["x_flat"])), median_x_rival=float(np.median(o["x_rival"])),
                                     median_floor_flat=float(np.median(o["floor_flat"])), median_floor_rival=float(np.median(o["floor_rival"])),
                                     dfloor=bd, D0=bD0, D_mu=Ds, frac_gal_D0_ge_0p30=frac03)
            P(f"    {k:7s} {foot:9s} x_flat {np.median(o['x_flat']):6.3f}  x_rival {np.median(o['x_rival']):6.3f}  floors flat "
              f"{np.median(o['floor_flat']):5.3f} rival {np.median(o['floor_rival']):5.3f}  dlog {bd['median']:.3f} [{bd['p16']:.3f}-{bd['p84']:.3f}]  "
              f"D0 {Ds[0.0]:.3f} [{bD0['p16']:.3f}-{bD0['p84']:.3f}]  D0.5 {Ds[0.5]:.3f}  D1 {Ds[1.0]:.3f}  D2 {Ds[2.0]:.3f}  "
              f"gal D0>=0.30: {100 * frac03:.0f}%")
    d0 = [RES[(b, "P2", f)]["D_mu"][0.0] for f in FOOTS]
    v = "CAN" if min(d0) >= 0.30 else ("MARGINAL" if min(d0) >= 0.20 else "CANNOT")
    VERD[b] = v
    d1 = [RES[(b, "P2", f)]["D_mu"][1.0] for f in FOOTS]
    P(f"    => frozen rule (P2, both footings): D0 = {d0[0]:.3f} / {d0[1]:.3f}  ->  {v}.   With mu = 1 (gas = stars inside r): "
      f"D1 = {d1[0]:.3f} / {d1[1]:.3f} ({'still >= 0.30' if min(d1) >= 0.30 else 'BELOW 0.30: a gas-rich flat-law population would not push the rival past the line'})")

banner("VARIANT GRID: D0 (P2) in every declared geometry / radius variant (canonical | alt)")
P(f"  {'bin':38s} " + "  ".join(f"{g_}/{r_:7s}" for g_, r_ in VARIANTS))
VARD0 = {}
for b, gs in BINS.items():
    row = []
    for var in VARIANTS:
        vals = [float(-np.median(bin_numbers(gs, var, f, "P2")["lsr_0.0"])) for f in FOOTS]
        VARD0[(b, var)] = vals
        row.append(f"{vals[0]:.3f}|{vals[1]:.3f}")
    P(f"  {b:38s} " + "  ".join(f"{s_:>13s}" for s_ in row))
    allv = [v_ for var in VARIANTS for v_ in VARD0[(b, var)]]
    P(f"  {'':38s} range over variants and footings: {min(allv):.3f}-{max(allv):.3f}")

# ================================================================================================= reported: where the decision lines sit
banner("REPORTED (added after the first run; no rule changed): the observed ratio R_obs = M_dyn(<r)/M*(<r) at which each law's "
       "log s_req crosses the frozen lines, at the bin's median x (approximate: the bin median of log s_req is not exactly its value "
       "at the median x).  Newton's lines are 10^-0.30 = 0.50 and 10^-0.10 = 0.79 (the ESTIMATOR-LIMITED line)")
P(f"  {'bin':38s} {'kernel':7s} {'foot':9s}   {'rival: DISF <':>13s} {'CONS >=':>8s}   {'flat: DISF <':>12s} {'CONS >=':>8s}   "
  f"{'Newton: LIMITED <':>17s}")
THR = {}
for b, gs in BINS.items():
    for k in ("P2", "nu_mono"):
        for foot in FOOTS:
            o = bin_numbers(gs, PRIMARY, foot, k)
            t = {}
            for law, xx in (("rival", float(np.median(o["x_rival"]))), ("flat", float(np.median(o["x_flat"])))):
                for line in (-0.30, -0.10):
                    sx = 10 ** line * xx
                    t[(law, line)] = float(sx * KERN[k](sx) / xx)
            THR[f"{b.strip()}|{k}|{foot}"] = {f"{l_}|{ln:+.2f}": v_ for (l_, ln), v_ in t.items()}
            P(f"  {b:38s} {k:7s} {foot:9s}   {t[('rival', -0.30)]:13.2f} {t[('rival', -0.10)]:8.2f}   {t[('flat', -0.30)]:12.2f} "
              f"{t[('flat', -0.10)]:8.2f}   {10 ** -0.10:17.2f}")
hz = [b.strip() for b in BINS if b.strip().startswith(("z>3.5", "Halpha", "[CII]"))]
fl_p2 = [THR[f"{b}|P2|{f}"]["flat|-0.30"] for b in hz for f in FOOTS]
fl_nm = [THR[f"{b}|nu_mono|{f}"]["flat|-0.30"] for b in hz for f in FOOTS]
rv_p2 = [THR[f"{b}|P2|{f}"]["rival|-0.30"] for b in hz for f in FOOTS]
P(f"  Reading: in the z > 3.5 bins the flat law's DISFAVOURED line sits at R_obs {min(fl_p2):.2f}-{max(fl_p2):.2f} (P2; nu_mono "
  f"{min(fl_nm):.2f}-{max(fl_nm):.2f}),")
P(f"  within about 0.1 of Newton's ESTIMATOR-LIMITED line {10 ** -0.1:.2f}: in practice the flat law cannot be headlined DISFAVOURED")
P(f"  there unless the bin is (nearly) estimator-limited.  The rival's DISFAVOURED line sits at R_obs {min(rv_p2):.2f}-{max(rv_p2):.2f} (P2):")
P("  the test is, in practice, a test of the rival.  (Danhaive's own M_dyn/M* = 0.9 R_obs in the primary sphere geometry.)")
NUM["reading_flat_disf_line_P2"] = [min(fl_p2), max(fl_p2)]
NUM["reading_rival_disf_line_P2"] = [min(rv_p2), max(rv_p2)]

# ================================================================================================= Roman-Oliveira gas-only floor
banner("ROMAN-OLIVEIRA (measured CO gas): the gas-only predicted floor on g_obs (stars only add) -- no velocity used")
ro_s = {r["id"]: r for r in load("romanoliveira2023_sample.csv", ["id", "z", "kpc_per_arcsec"])}
ro_g = {r["id"]: r for r in load("romanoliveira2023_gasmasses.csv", ["id", "mh2_msun", "e_mh2", "mh2_flag"])}
ro_k = [r["id"] for r in load("romanoliveira2023_kinematics.csv", ["id"])]
RINGS = {"AzTEC 1": (4, 0.11), "BRI1335-0417": (5, 0.15), "J081740": (4, 0.13), "SGP38326-1": (5, 0.13), "SGP38326-2": (3, 0.12)}
P("  kinematic sources (ids only read from the kinematics table): " + ", ".join(ro_k))
P("  stellar mass on disk: none for any kinematic source (AzTEC1's ~1e11 is in the text, but AzTEC1 has no kinematics: a likely merger)")
P("  r_ext = the mean radius of the last two rings (V_ext, sigma_ext average them): primary (N - 1) RADSEP (ring centres at (i + 1/2) "
  "RADSEP); variant (N - 1.5) RADSEP")
P(f"  {'id':13s} {'z':>6s} {'ring':>7s} {'r_ext kpc':>9s} {'M_H2':>9s} {'f_g':>4s} {'foot':9s} {'g_gas/a0':>8s}   V_floor km/s: "
  f"{'Newton':>7s} {'flat':>7s} {'rival':>7s}  rival/flat")
RO = {}
for sid in ro_k:
    z = fnum(ro_s[sid]["z"])
    nr, rs = RINGS[sid]
    mh2 = fnum(ro_g[sid]["mh2_msun"])
    for ring, off in (("primary", 1.0), ("variant", 1.5)):
        rext = (nr - off) * rs * fnum(ro_s[sid]["kpc_per_arcsec"])
        for fg in (0.5, 0.25):
            for foot in FOOTS:
                gg = G * fg * mh2 * MSUN / (rext * KPC) ** 2
                vf = {}
                for law in ("Newton",) + LAWS:
                    if law == "Newton":
                        gpred = gg
                    else:
                        a = a0_law(foot, law, z)
                        gpred = gg * float(K.nu_p2(gg / a))
                    vf[law] = math.sqrt(gpred * rext * KPC) / 1e3
                RO[(sid, ring, fg, foot)] = dict(z=z, r_ext_kpc=rext, mh2=mh2, g_gas_over_a0=gg / A0[foot], V_floor_kms=vf)
                P(f"  {sid:13s} {z:6.3f} {ring:>7s} {rext:9.2f} {mh2:9.2e} {fg:4.2f} {foot:9s} {gg / A0[foot]:8.2f}   {'':13s}"
                  f"{vf['Newton']:7.1f} {vf['flat']:7.1f} {vf['rival']:7.1f}  {vf['rival'] / vf['flat']:.3f}")
P("  (P2 kernel.  Phase 2 compares these minimum circular speeds with sqrt(V_ext^2 + alpha sigma_ext^2); the upper side needs M*.)")

# ================================================================================================= controls
banner("CONTROLS")
allz = [g for g in GAL if g["sample"] != "kurvs3RD"]
# C1: E = 1 makes the laws identical
_E_saved = E
E = lambda z: 1.0                                                   # run the same pipeline with E(z) forced to 1
d1max = 0.0
for gs in BINS.values():
    for var in VARIANTS:
        for foot in FOOTS:
            for k in ("P2", "nu_mono"):
                o = bin_numbers(gs, var, foot, k)
                d1max = max(d1max, float(np.max(np.abs(o["dfloor"]))),
                            max(float(np.max(np.abs(o[f"lsr_{mu}"] - o[f"lsf_{mu}"]))) for mu in MUS))
E = _E_saved
check("C1 E(z) = 1 makes the rival identical to the flat law (the same pipeline re-run with E forced to 1: max |dlog floor| and "
      "|dlog s_req| over all bins, variants, kernels, footings and gas amounts)", f"{d1max:.1e}", d1max < 1e-12)
# C2: planted R = 1 at each bin's median x
c2 = []
for b, gs in BINS.items():
    for foot in FOOTS:
        for k in ("P2", "nu_mono"):
            o = bin_numbers(gs, PRIMARY, foot, k)
            for law, xx in (("flat", np.median(o["x_flat"])), ("rival", np.median(o["x_rival"]))):
                c2.append((b, foot, k, law, float(log_sreq(k, xx, 1.0))))
worst2 = max(c2, key=lambda t: t[4])
nN = float(log_sreq("Newton", 1.0, 1.0))
check("C2 a planted galaxy with M_dyn/M_star = 1 at each bin's median x is BELOW both laws' floors (log s_req < 0; both kernels and "
      "footings) and exactly ON Newton's (log s_req = 0)", f"largest log s_req over {len(c2)} cases = {worst2[4]:+.4f} ({worst2[:4]}); "
      f"Newton {nN:+.1e}", worst2[4] < 0 and nN == 0.0)
# C3: a galaxy exactly on a law's floor has log s_req = 0
c3 = 0.0
for g in allz:
    for foot in FOOTS:
        for k in ("P2", "nu_mono"):
            for law in LAWS:
                xx = g["gs"][PRIMARY] / a0_law(foot, law, g["z"])
                c3 = max(c3, abs(float(log_sreq(k, xx, KERN[k](xx)))))
check("C3 a galaxy exactly on a law's own floor (R = nu(x)) has log s_req = 0 (to 1e-9), P2 closed form and nu_mono inversion",
      f"max |log s_req| = {c3:.1e}", c3 < 1e-9)
# C3b: the generic inversion reproduces P2's closed form
xg = np.logspace(-3, 3, 61)[:, None]
Rg = np.logspace(-0.5, 1.5, 21)[None, :]
p2gen = np.log10(phi_inv("P2", xg * Rg) / xg) if "P2" in KERN else None
c3b = float(np.max(np.abs(p2gen - log_sreq("P2", xg, Rg))))
check("C3b the generic bisection inverse reproduces P2's closed-form s_req (x = 1e-3..1e3, R = 0.3..30)", f"max diff {c3b:.1e} dex", c3b < 1e-9)
# C4: a planted flat-law galaxy with gas mu = 1 has flat log s_req > 0
c4 = min(float(np.min(bin_numbers(gs, PRIMARY, f, k)["lsf_1.0"])) for gs in BINS.values() for f in FOOTS for k in ("P2", "nu_mono"))
check("C4 a planted flat-law galaxy with gas mu = 1 inside r is CONSISTENT with the flat law (log s_req > 0) for every real x",
      f"min log s_req = {c4:+.4f}", c4 > 0)
# C5: rival s_req <= flat s_req for every galaxy (L4)
c5 = max(float(np.max(o[f"lsr_{mu}"] - o[f"lsf_{mu}"])) for gs in BINS.values() for f in FOOTS for k in ("P2", "nu_mono")
         for o in [bin_numbers(gs, PRIMARY, f, k)] for mu in MUS)
check("C5 the rival's log s_req never exceeds the flat law's (L4: the floor can single out the rival, never the flat law)",
      f"max (rival - flat) = {c5:+.2e}", c5 <= 1e-12)
# C6: the lemma in context -- min over gas of the predicted ratio equals nu(x) at every real x (MUTATE: the switch law)
mus_g = np.concatenate([[0.0], np.logspace(-3, 2.5, 221)])
nu_sw = lambda v: 1.0 + (1.0 / (1.0 + np.asarray(v, float) ** 8)) / np.asarray(v, float)
lemma_k = {"switch (L5)": nu_sw} if MUT else {"P2": K.nu_p2, "nu_mono": K.nu_mono}
xs_all = np.array([g["gs"][PRIMARY] / a0_law(f, law, g["z"]) for g in allz for f in FOOTS for law in LAWS])
xs_all = np.concatenate([xs_all, np.linspace(0.5, 1.2, 15)])       # plus the switch law's sensitive stretch (x ~ y_c = 1)
c6 = {}
for nm, f in lemma_k.items():
    Fm = (1 + mus_g[None, :]) * f((1 + mus_g[None, :]) * xs_all[:, None])
    c6[nm] = float(np.min(Fm.min(axis=1) / f(xs_all) - 1.0))
check("C6 the lemma at every real x (and x = 0.5-1.2): min over gas mu of the predicted ratio equals the gas-free floor nu(x)"
      + ("  [MUTATE: switch law, must FAIL]" if MUT else ""), "; ".join(f"{k_}: min ratio - 1 = {v_:+.2e}" for k_, v_ in c6.items()),
      all(v_ >= -1e-12 for v_ in c6.values()))
# C7: the laws separate in every z > 0 bin (MUTATE: E = 1 -> no separation)
sep = {b: min(RES[(b, "P2", f)]["dfloor"]["median"] for f in FOOTS) for b in BINS}
check("C7 the floors separate (median dlog > 0) in every bin (all bins have z > 0)" + ("  [MUTATE: E = 1, must FAIL]" if MUT else ""),
      "; ".join(f"{b.strip()[:26]}: {v_:.3f}" for b, v_ in sep.items()), all(v_ > 1e-6 for v_ in sep.values()))

# ================================================================================================= bottom line
banner("PRE-FLIGHT BOTTOM LINE (the frozen rule, P2, primary variant, both footings)")
for b in BINS:
    d0 = [RES[(b, "P2", f)]["D_mu"][0.0] for f in FOOTS]
    d1 = [RES[(b, "P2", f)]["D_mu"][1.0] for f in FOOTS]
    df = [RES[(b, "P2", f)]["dfloor"]["median"] for f in FOOTS]
    allv = [v_ for var in VARIANTS for v_ in VARD0[(b, var)]]
    P(f"  {b:38s} {VERD[b]:8s}  D0 {d0[0]:.2f}/{d0[1]:.2f}  D1 {d1[0]:.2f}/{d1[1]:.2f}  floor sep {df[0]:.2f}/{df[1]:.2f} dex  "
      f"(D0 over variants {min(allv):.2f}-{max(allv):.2f})")
P("  Against the 0.2-0.3 dex M_star systematic: CAN means a gas-free flat-law population would put the rival past -0.30 dex.")
P("  Structural (L4): the test can single out the rival, never the flat law; the flat law can only fail with the rival or to Newton.")

for (b, k, f), v_ in RES.items():
    NUM[f"{b.strip()}|{k}|{f}"] = v_
NUM["verdicts"] = VERD
NUM["variant_D0_P2"] = {f"{b.strip()}|{v[0]}/{v[1]}": vals for (b, v), vals in VARD0.items()}
NUM["roman_oliveira"] = {f"{s}|{rg}|fg{fg}|{f}": v_ for (s, rg, fg, f), v_ in RO.items()}
NUM["thresholds_at_median_x"] = THR
NUM["loaded_columns"] = [dict(file=f, cols=list(c)) for f, c in LOADED]
lb = [c for c in CHECKS if c["load_bearing"]]
nf = sum(not c["ok"] for c in lb)
P(f"\n  {sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {nf}")


def jclean(o):
    if isinstance(o, dict):
        return {str(k_): jclean(v_) for k_, v_ in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v_) for v_ in o]
    if isinstance(o, (np.floating, float)):
        return float(o)
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, np.bool_):
        return bool(o)
    return o


json.dump(jclean(dict(slug=SLUG, mutate=MUT, summary=dict(n_checks=len(CHECKS), load_bearing_failures=nf,
                                                           failed=[c["name"][:90] for c in CHECKS if not c["ok"]]),
                      checks=CHECKS, numbers=NUM)), builtins.open(os.path.join(LANE, SLUG + "_results.json"), "w"), indent=1)
builtins.open(os.path.join(LANE, SLUG + ".out"), "w").write("\n".join(LINES) + "\n")
sys.exit(1 if nf else 0)
