#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG323 -- the SLUGGS law-only offset re-scored with MEASURED tracers (GC density profiles, anisotropy where tabulated, hot gas).
Criteria frozen and committed before any downloaded value was read: FROZEN_CRITERIA.md (b2e7ec16d).

Start: AUDIT_SLUGGS_2026-10-03/audit_sluggs_recompute.py (+0.0977 +- 0.0243 dex, 4.02 sigma canonical / 3.67 alt; gamma = 3, beta = 0).
Its source is exec'd read-only up to its "1. HEADLINE" block (bins, clipping, ML dispersions, JAM masses, kernel nu_mono inherited unchanged).
Law: g = nu_mono(g_N/a0) g_N, a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FIXED; footings 9.36e-11 | 1.13e-10.

Measured inputs (owner-approved downloads, ../_external_data/sluggs_tracers/, parsed by script from the arXiv LaTeX / HTML; manifest in README):
  Kartha+14 (1310.1979) Table 'surfden'    total-GC Sersic fits NGC 1023, 2768 (and 720, not in the 16)
  Kartha+16 (1602.01838) Table 'surfden07' total-GC Sersic fit NGC 3607 (SB and MA methods; MA primary -- the paper's total-system curve
                                           in its Fig. 8; the method choice is NOT in the frozen text and is reported both ways)
  Agnello+14 (1401.4461) Table 'tab:3pop'  M87 three-population Sersic (n, R_e, central-density ratios)
  Zhu+14 (1407.2263) text                  M87 total-GC Sersic of Peng+08 (b_n = 2.21 in log10, R0, n) -- reported alternative, PROVISIONAL (text)
  Churazov+08 (0711.4686) eq. ne           M87 n_e(r) beta-model 0.5'-10' -- replaces CFG57's extrapolation beyond the Lakhchaura field
  Urban+11 (1102.2430) text                Virgo n_e ~ r^-1.21 to ~1.2 Mpc (no normalisation) -- reported alternative only
  Forbes+17 (1701.04835) Table 6 + VizieR J/AJ/153/114 ReadMe   the 3,575 vs 4,492 row gap (provenance)
Anisotropy: NO downloaded paper TABULATES beta for a galaxy in the 16 (Agnello+14 posteriors and Zhu+14 beta(r) are figures; text values
  are used only in reported PROVISIONAL rows) -> isotropic everywhere in the primary, +-0.5 bracket.
Gas: CFG57's committed measured sources (Lakhchaura+18 n_e: 4486, 5846, 4374, 4649; Fukazawa+06 beta-model: 4365, 3607, 4697), CFG57's D1
  conventions (mu_e 1.155, outer power law of the last three points, r ~ D, n_e ~ D^-1/2, gas as mass only).

Primary Jeans: full Abel-deprojected rho(r) (local slope = the deprojected gamma_i(r) at every radius), constant beta, exact projection.
MUTATE (CFG323_MUTATE=1): the measured tracer profiles rho(r/R_e,gal) cyclically shuffled across the measured galaxies; separate outputs.
Run: python3 campaign_fresh_gravity/CFG323_sluggs_measured_tracers/cfg323_measured_tracers.py   (CFG323_MUTATE=1 for the control)
"""
import os, sys, re, math, json, io, contextlib, html as _html
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
EXT = os.path.normpath(os.path.join(REPO, "..", "_external_data", "sluggs_tracers"))
MUTATE = os.environ.get("CFG323_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = []


def P(s=""):
    print(s); OUT.append(str(s))


# ------------------------------------------------------------------ 0. the audit's machinery, read-only
_saved = os.environ.pop("MUTATE", None)
src = open(os.path.join(LANES, "AUDIT_SLUGGS_2026-10-03", "audit_sluggs_recompute.py")).read()
cut = src.index("\n# ------------------------------------------------------------------ 1. headline")
NS = {"__file__": os.path.join(LANES, "AUDIT_SLUGGS_2026-10-03", "audit_sluggs_recompute.py"), "__name__": "audit_ns"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], "audit_sluggs_recompute", "exec"), NS)
if _saved is not None:
    os.environ["MUTATE"] = _saved
B, GAL, RES, A0, KERN = NS["B"], NS["GAL"], NS["RES"], NS["A0"], NS["KERN"]
G, KPC, MSUN, ARCSEC = NS["G"], NS["KPC"], NS["MSUN"], NS["ARCSEC"]
RG, LR, stat, sig_los_audit = NS["RG"], NS["LR"], NS["stat"], NS["sig_los"]
S16 = NS["CFG55_16"]
CENTRALS = [4486, 4365, 4374, 5846]
KM = "nu_mono"
nu = KERN[KM]

P("=" * 120)
P("CFG323 -- SLUGGS law-only offset with MEASURED tracers (density profiles, beta where tabulated, hot gas)" + ("   *** MUTATE: measured profiles shuffled ***" if MUTATE else ""))
P("frozen criteria: FROZEN_CRITERIA.md (commit b2e7ec16d); kernel nu_mono, kappa = 1/2 fixed, footings " + ", ".join(f"{k} {v:.3g}" for k, v in A0.items()))
P("=" * 120)

checks = []


def check(lbl, cond, det):
    checks.append((lbl, bool(cond))); P(f"  [{'PASS' if cond else 'FAIL'}] {lbl}\n         {det}")


# ------------------------------------------------------------------ 1. transcription (by script, from the downloaded LaTeX / HTML)
def tex(rel):
    return open(os.path.join(EXT, "arxiv_src", rel), encoding="latin-1").read()


def pm(s):
    """'1.97$\\pm$0.34' -> (1.97, 0.34, 0.34); '2.25^{+1.45}_{-0.45}' -> (2.25, 1.45, 0.45)"""
    s = s.replace("$", "").replace("~", "").strip()
    m = re.match(r"([-\d.]+)\s*\\pm\s*([\d.]+)", s)
    if m:
        return float(m.group(1)), float(m.group(2)), float(m.group(2))
    m = re.match(r"([-\d.]+)\s*\^\{\+([\d.]+)\}_\{-([\d.]+)\}", s)
    if m:
        return float(m.group(1)), float(m.group(2)), float(m.group(3))
    return float(s), 0.0, 0.0


def table_rows(t, label):
    k = t.index("\\label{%s}" % label)
    a = t.rfind("\\begin{tabular", 0, k); b = t.find("\\end{tabular}", a)
    if a < 0 or b < 0 or b > k + 400 and t.find("\\end{tabular}", a) > k:
        a = t.find("\\begin{tabular", t.rfind("\\begin{table", 0, k)); b = t.find("\\end{tabular}", a)
    body = t[a:b]
    rows = [r.strip() for r in body.split("\\\\")]
    return [[c.strip() for c in r.replace("\\hline", "").split("&")] for r in rows if "&" in r]


TR = {}
# Kartha+14 total GC system
rows = [r for r in table_rows(tex("1310.1979/Kartha_arxiv.tex"), "surfden") if r[0].strip().isdigit()]
TR["K14"] = {int(r[0]): dict(Re_am=pm(r[1]), n=pm(r[2]), bg=pm(r[3]), ext_am=pm(r[4])) for r in rows}
# Kartha+16 NGC 3607 total GC system
rows = [r for r in table_rows(tex("1602.01838/MNRAS_manuscript_SSK_Rev2.tex"), "surfden07") if r[0].strip() in ("SB", "MA")]
TR["K16"] = {r[0].strip(): dict(Re_am=pm(r[1]), n=pm(r[2]), bg=pm(r[3]), ext_am=pm(r[4])) for r in rows}
# Agnello+14 M87 three populations (upper block of tab:3pop)
ta = tex("1401.4461/secpaper4.tex")
blk = ta[ta.rfind("\\begin{table}", 0, ta.index("\\label{tab:3pop}")):ta.index("\\label{tab:3pop}")]
nrow = re.search(r"\$n\$\s*&(.*?)\\\\", blk, re.S).group(1)
TR["A14_n"] = [pm(c.replace("\n", " ")) for c in nrow.split("&")]
rerow = re.search(r"R_\{\\rm e\}\(\\rm\{arcsec\}\)\$\s*&(.*?)\\\\", blk, re.S).group(1)
TR["A14_Re_as"] = [pm(c) for c in rerow.split("&")]
TR["A14_Sib"] = pm(re.search(r"Sigma_\{\\rm i/\s*b\}=(.*?),", blk, re.S).group(1))
TR["A14_Srb"] = pm(re.search(r"Sigma_\{\\rm r/b\}=(.*?)\$", blk, re.S).group(1))
# Zhu+14 text (Peng+08 total GC Sersic) -- PROVISIONAL
tz = tex("1407.2263/ms_apj.tex")
mz = re.search(r"\$b_n = ([\d.]+)\$, \$R_0 = ([\d.]+)''\\pm ([\d.]+)\$, \$n = ([\d.]+)\\pm ([\d.]+)\$", tz)
TR["Z14"] = dict(bn_log10=float(mz.group(1)), R0_as=(float(mz.group(2)), float(mz.group(3))), n=(float(mz.group(4)), float(mz.group(5))))
mzb = re.search(r"varying from \$(-?[\d.]+)\$ at the centre to ([\d.]+) at \$\\sim(\d+)\$ kpc, and gradually decreasing to zero at \$\\sim(\d+)\$ kpc", tz)
TR["Z14_beta_text"] = dict(b0=float(mzb.group(1)), bmax=float(mzb.group(2)), rmax=float(mzb.group(3)), r0=float(mzb.group(4)))
# Churazov+08 n_e(r)
tc = tex("0711.4686/m87p_11.tex")
mc = re.search(r"n_e=([\d.]+)~\\left\[1\+\\left\(\\frac\{r\}\{r_c\}\\right\)\^2\\right\]\^\{-\\frac\{3\}\{2\} \\beta\}", tc)
mc2 = re.search(r"where \$\\beta=([\d.]+)\$ and \$r_c=([\d.]+)'\$ \(or ([\d.]+) kpc\)", tc)
mcr = re.search(r"from \$\\sim ([\d.]+)'\$ to \$\\sim (\d+)'\$", tc)
mcd = re.search(r"We assume distances of (\d+) and ([\d.]+) Mpc for M87", tc)
TR["C08"] = dict(ne0=float(mc.group(1)), beta=float(mc2.group(1)), rc_am=float(mc2.group(2)), rc_kpc=float(mc2.group(3)),
                 rmin_am=float(mcr.group(1)), rmax_am=float(mcr.group(2)), D=float(mcd.group(1)))
# Urban+11 slope
tu = tex("1102.2430/virgoA.tex")
mu = re.search(r"index \$\\beta=([\d.]+)\\pm([\d.]+)\$", tu)
TR["U11"] = dict(slope=-float(mu.group(1)), err=float(mu.group(2)), rmax_kpc=1200.0 if "1.2~Mpc" in tu else float("nan"), D=16.1 if "16.1~Mpc" in tu else float("nan"))
# Forbes+17 Table 6 (N_GC) and the VizieR ReadMe record counts
tf = tex("1701.04835/forbes.tex")
t6 = tf[tf.index("\\tablecaption{GC system catalog properties}"):]
t6 = t6[t6.index("\\startdata"):t6.index("\\enddata")]
TR["F17_T6"] = {int(r.split("&")[0]): int(r.split("&")[3]) for r in t6.replace("\\startdata", "").split("\\\\") if r.strip() and r.split("&")[0].strip().isdigit()}
rm = open(os.path.join(EXT, "readme", "J_AJ_153_114_ReadMe")).read()
TR["VZ_records"] = {m.group(1): int(m.group(2)) for m in re.finditer(r"^(table\d)\.dat\s+\d+\s+(\d+)", rm, re.M)}

with open(os.path.join(HERE, f"cfg323_transcribed_values{TAG}.tsv"), "w") as fh:
    fh.write("# CFG323: values parsed BY SCRIPT from the downloaded arXiv LaTeX (positions: table label / sentence); Zhu+14 and Agnello/Zhu beta are TEXT values (PROVISIONAL)\n")
    fh.write("source\tkey\tvalue\n")
    for k, v in TR.items():
        fh.write(f"{k}\t-\t{json.dumps(v)}\n")

P("\n" + "-" * 120); P("1. TRANSCRIPTION (parsed by script)"); P("-" * 120)
for k in ("K14", "K16", "A14_n", "A14_Re_as", "A14_Sib", "A14_Srb", "Z14", "Z14_beta_text", "C08", "U11"):
    P(f"  {k:14}: {TR[k]}")
P(f"  F17 Table 6 rows: {len(TR['F17_T6'])};  VizieR J/AJ/153/114 record counts: {TR['VZ_records']}")


# ------------------------------------------------------------------ 2. Sersic, Abel deprojection
def bn_cb(n):  # Ciotti & Bertin 1999 (Agnello+14's kappa_n)
    return 2 * n - 1 / 3 + 4 / (405 * n) + 46 / (25515 * n ** 2)


def bn_k(n):   # Kartha+14/16 and Pota+13: 1.9992 n - 0.3271
    return 1.9992 * n - 0.3271


UU = np.linspace(0.0, 12.0, 6001)


def abel_rho(dSigma, r):
    """rho(r) = -(1/pi) int_0^inf Sigma'(r cosh u) du  (exact for Sigma -> 0 at infinity)"""
    out = np.empty_like(r)
    ch = np.cosh(UU)
    for i0 in range(0, len(r), 500):
        rr = r[i0:i0 + 500, None] * ch[None, :]
        out[i0:i0 + 500] = -np.trapz(dSigma(rr), UU, axis=1) / math.pi
    return out


def sersic_dS(Re, n, b, S0=1.0):
    """S(R) = S0 exp(-b (R/Re)^(1/n)) (central normalisation; any other normalisation only rescales)"""
    def d(R):
        x = np.maximum(R / Re, 1e-300)
        e = np.exp(-b * x ** (1.0 / n))
        return -S0 * e * b / (n * Re) * x ** (1.0 / n - 1.0)
    return d


def sersic_rho(Re, n, b, S0=1.0):
    return np.maximum(abel_rho(sersic_dS(Re, n, b, S0), RG), 0.0)


def am2kpc(a, D):
    return a * math.pi / 180 / 60 * D * 1e3


# ------------------------------------------------------------------ 3. general-profile Jeans (own), gas, calibration
def g_law(M, a_h, a0, Mgas=None):
    Mb = M * RG ** 2 / (RG + a_h) ** 2 + (Mgas if Mgas is not None else 0.0)
    gN = G * Mb * MSUN / (RG * KPC) ** 2
    return gN * nu(gN / a0)


def lnf_of(beta):
    """f(r) = exp(int 2 beta dln r); beta a constant or an array on RG"""
    if np.isscalar(beta):
        return 2 * beta * LR
    b = np.asarray(beta, float)
    return np.concatenate([[2 * b[0] * LR[0]], 2 * b[0] * LR[0] + np.cumsum(0.5 * (2 * b[1:] + 2 * b[:-1]) * np.diff(LR))])


UP = np.linspace(0, 14, 4000); CHP = np.cosh(UP)


def sig_parts(Rb, g, rho, beta=0.0):
    """returns (num, den) of the projected second moment at each R: num = int (1 - beta/ch^2) rho sigma_r^2 r du, den = int rho r du"""
    lnf = lnf_of(beta)
    w = rho * np.exp(lnf) * g * RG * KPC                       # per d ln r
    cum = np.concatenate([np.cumsum((0.5 * (w[1:] + w[:-1]) * np.diff(LR))[::-1])[::-1], [0.0]])
    Pr = cum / np.exp(lnf)                                      # rho sigma_r^2
    lP = np.log(np.maximum(Pr, 1e-300)); lrho = np.log(np.maximum(rho, 1e-300))
    bet = (np.full_like(RG, beta) if np.isscalar(beta) else np.asarray(beta, float))
    num, den = [], []
    for R in Rb:
        r = R * CHP; lr_ = np.log(r)
        Pi = np.exp(np.interp(lr_, LR, lP)); ri = np.exp(np.interp(lr_, LR, lrho)); bi = np.interp(lr_, LR, bet)
        num.append(np.trapz((1 - bi / CHP ** 2) * Pi * r, UP)); den.append(np.trapz(ri * r, UP))
    return np.array(num), np.array(den)


def sig_los(Rb, g, comps):
    """comps = list of (rho, beta): exact mixture sigma^2 = sum num_k / sum den_k"""
    N = np.zeros(len(Rb)); D = np.zeros(len(Rb))
    for rho, beta in comps:
        n_, d_ = sig_parts(Rb, g, rho, beta); N += n_; D += d_
    return np.sqrt(N / D) / 1e3


MU_E, MP_G, KPC_CM, MSUN_G = 1.155, 1.67262192e-24, 3.0856775814913673e21, 1.98892e33   # CFG57's constants
RHO_PER_NE = MU_E * MP_G * KPC_CM ** 3 / MSUN_G
RGAS = np.geomspace(1e-3, 3e4, 4000)                                                       # CFG57's gas grid (clamped beyond)
DD = os.path.join(REPO, "real_research", "data", "cfg57_gas_sources")


def rd_tsv(fn):
    L = [l.rstrip("\n").split("\t") for l in open(os.path.join(DD, fn)) if l.strip() and not l.startswith("#")]
    H = [h.strip() for h in L[0]]
    return [dict(zip(H, [x.strip() for x in r])) for r in L[1:]]


LAK, FUK = {}, {r_["name"]: r_ for r_ in rd_tsv("fukazawa2006_table4.tsv")}
for r_ in rd_tsv("lakhchaura2018_ne_profiles.tsv"):
    LAK.setdefault(r_["name"], []).append(r_)
SRC1 = [4486, 5846, 4374, 4649]; SRC2 = [4365, 4494, 3607, 4697]


def mass_on_RG(rho_gas):
    dm = 4 * math.pi * RGAS ** 2 * rho_gas
    M = np.concatenate([[dm[0] * RGAS[0] / 3], dm[0] * RGAS[0] / 3 + np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RGAS))])
    return np.interp(np.log(RG), np.log(RGAS), M)                                          # clamped beyond 3e4 kpc as in CFG57


def gas_mass(n, m87_outer="churazov", drop_last=True):
    """measured gas M_gas(<r) on RG (Msun), or None; m87_outer in {'churazov', 'cfg57', 'urban_trunc'}.
    drop_last=True is CFG57's D1 (the frozen text names 'CFG57's D1 conventions'): the upturned outermost Lakhchaura shell is dropped and the
    outer power law is fitted to the three points before it.  drop_last=False = CFG57's mechanical frozen rule (reported only; unbounded gas)."""
    DS = GAL[n]["D"]; key = f"NGC{n}"
    lg = np.log(RGAS)
    if n in SRC1 and key in LAK:
        rows = sorted(LAK[key], key=lambda x: float(x["r_kpc"]))[:(-1 if drop_last else None)]
        Dp = float(rows[0]["D_Mpc_paper"]); f = DS / Dp
        r = np.array([float(x["r_kpc"]) for x in rows]) * f; ne = np.array([float(x["ne_cm3"]) for x in rows]) * f ** -0.5
        o = np.argsort(r); r, ne = r[o], ne[o]
        lr_, ln_ = np.log(r), np.log(ne)
        s = np.polyfit(lr_[-3:], ln_[-3:], 1)[0]
        lne = np.where(lg <= lr_[0], ln_[0], np.where(lg >= lr_[-1], ln_[-1] + s * (lg - lr_[-1]), np.interp(lg, lr_, ln_)))
        info = dict(src="Lakhchaura+18 (D1)" if drop_last else "Lakhchaura+18 (no drop)", r_last=float(r[-1]), slope=float(s))
        if n == 4486 and m87_outer != "cfg57":
            c = TR["C08"]; fc = DS / c["D"]
            ne_c = lambda x: c["ne0"] * fc ** -0.5 * (1 + (x / (c["rc_kpc"] * fc)) ** 2) ** (-1.5 * c["beta"])
            rcmax = am2kpc(c["rmax_am"], c["D"]) * fc
            beyond = lg > lr_[-1]
            if m87_outer == "churazov":
                lne = np.where(beyond, np.log(ne_c(RGAS)), lne)
                info.update(outer=f"Churazov+08 beta-model from {r[-1]:.1f} kpc (measured to {rcmax:.1f} kpc; continued beyond = EXTRAPOLATED)")
            elif m87_outer == "urban_trunc":
                u = TR["U11"]; fu = DS / u["D"]
                ln_rc = math.log(ne_c(rcmax))
                l2 = np.where(lg <= math.log(rcmax), np.log(ne_c(RGAS)), ln_rc + u["slope"] * (lg - math.log(rcmax)))
                l2 = np.where(lg > math.log(u["rmax_kpc"] * fu), -700.0, l2)
                lne = np.where(beyond, l2, lne)
                info.update(outer=f"Churazov+08 to {rcmax:.1f} kpc, Urban+11 slope {u['slope']} to {u['rmax_kpc'] * fu:.0f} kpc, zero beyond")
            info["rc_measured_max"] = rcmax
        return mass_on_RG(RHO_PER_NE * np.exp(lne)), info
    if n in SRC2 and key in FUK and math.isfinite(float(FUK[key]["ne10_1e-3cm3"])):
        row = FUK[key]; f = DS / float(row["D_Mpc"])
        ne10 = float(row["ne10_1e-3cm3"]) * 1e-3 * f ** -0.5; r10 = 10.0 * f
        shape = lambda x: (1 + (x / 1.0) ** 2) ** (-0.75)
        return mass_on_RG(RHO_PER_NE * ne10 * shape(RGAS) / shape(r10)), dict(src="Fukazawa+06 beta-model", Rmax=float(row["Rmax_kpc"]) * f)
    return None, None


def calib_mass(n, a0, Mg):
    b = B[n]; Mjam, r12 = b["Mjam"], b["r12"]
    Mg12 = 0.0 if Mg is None else float(np.interp(math.log(r12), LR, Mg))
    def fn(lm):
        Mb = 0.5 * 10 ** lm + Mg12
        return math.log10(Mb * float(nu(G * Mb * MSUN / (r12 * KPC) ** 2 / a0))) - math.log10(0.5 * Mjam)
    lo, hi = math.log10(Mjam) - 6, math.log10(Mjam) + 1
    if fn(lo) > 0:
        return float("nan")
    return 10 ** brentq(fn, lo, hi, xtol=1e-12)


# ------------------------------------------------------------------ 4. tracer models
def powerlaw_rho(gamma):
    return RG ** (-gamma)


MEASURED = [1023, 2768, 3607, 4486]
TRACER, TRACER_ERR, EXTENT = {}, {}, {}


def k_sersic(n, rec):
    D = GAL[n]["D"]; Re = am2kpc(rec["Re_am"][0], D); nn = rec["n"][0]
    return sersic_rho(Re, nn, bn_k(nn))


def k_perturbed(n, rec):
    D = GAL[n]["D"]; out = []
    for which in ("Re_am", "n"):
        for sgn in (+1, -1):
            v, ep, em = rec[which]
            val = v + (ep if sgn > 0 else -em)
            Re = am2kpc(val if which == "Re_am" else rec["Re_am"][0], D)
            nn = val if which == "n" else rec["n"][0]
            if nn <= 0.2 or Re <= 0:
                continue
            out.append((f"{which}{'+' if sgn > 0 else '-'}1s", sersic_rho(Re, nn, bn_k(nn))))
    return out


def a14_pops(nmod=None, remod=None):
    """M87 three populations: S_j(R) = S0_j exp(-kappa_n (R/Re_j)^(1/n_j)); S0_b = 1, S0_i = Sib, S0_r = Srb"""
    D = GAL[4486]["D"]; S0 = [1.0, TR["A14_Sib"][0], TR["A14_Srb"][0]]
    pops = []
    for j in range(3):
        nn = TR["A14_n"][j][0] if not (nmod and nmod[0] == j) else nmod[1]
        Re_as = TR["A14_Re_as"][j][0] if not (remod and remod[0] == j) else remod[1]
        Re = Re_as / 60.0
        pops.append(sersic_rho(am2kpc(Re, D), nn, bn_cb(nn), S0[j]))
    return pops


TRACER[1023] = [k_sersic(1023, TR["K14"][1023])]
TRACER[2768] = [k_sersic(2768, TR["K14"][2768])]
TRACER[3607] = [k_sersic(3607, TR["K16"]["MA"])]
A14 = a14_pops()
TRACER[4486] = [A14[0] + A14[1] + A14[2]]                         # isotropic primary: mixture == summed density
for n, rec in ((1023, TR["K14"][1023]), (2768, TR["K14"][2768]), (3607, TR["K16"]["MA"])):
    TRACER_ERR[n] = k_perturbed(n, rec); EXTENT[n] = am2kpc(rec["ext_am"][0], GAL[n]["D"])
pert = []
for j in range(3):
    v, ep, em = TR["A14_n"][j]
    for val, lab in ((v + ep, "+"), (v - em, "-")):
        p_ = a14_pops(nmod=(j, val)); pert.append((f"n_{'bir'[j]}{lab}1s", p_[0] + p_[1] + p_[2]))
    v, ep, em = TR["A14_Re_as"][j]
    for val, lab in ((v + ep, "+"), (v - em, "-")):
        p_ = a14_pops(remod=(j, val)); pert.append((f"Re_{'bir'[j]}{lab}1s", p_[0] + p_[1] + p_[2]))
TRACER_ERR[4486] = pert

if MUTATE:
    # cyclic shuffle of rho(x = r / R_e,gal) across the measured galaxies
    prof = {n: TRACER[n][0] for n in MEASURED}
    sh = MEASURED[1:] + MEASURED[:1]
    newT = {}
    for n, m in zip(MEASURED, sh):
        x_src = RG / B[m]["Re"]                                   # donor profile on x
        x_tgt = RG / B[n]["Re"]
        newT[n] = [np.exp(np.interp(np.log(x_tgt), np.log(x_src), np.log(np.maximum(prof[m], 1e-300))))]
        P(f"  MUTATE: NGC{n} receives the measured profile of NGC{m} (in units of R_e,gal)")
    UNMUT = {n: TRACER[n] for n in MEASURED}
    TRACER.update(newT)

# ------------------------------------------------------------------ 5. offsets
GAS = {n: gas_mass(n) for n in S16}
MSTAR = {}


def offset(n, foot, comps=None, gas=True, Mg=None, use_calib=None):
    b = B[n]; a0 = A0[foot]
    if Mg is None and gas:
        Mg = GAS[n][0]
    M = calib_mass(n, a0, Mg if gas else None) if use_calib is None else use_calib
    g = g_law(M, b["Re"] / 1.8153, a0, Mg if gas else None)
    if comps is None:
        comps = [(powerlaw_rho(3.0), 0.0)]
    s = sig_los(b["Rb"], g, comps)
    m = b["outer"]
    return float(np.mean(np.log10(b["Sb"][m] / s[m])))


def comps_for(n, beta=0.0, gamma_unmeas=3.0, tracer=None):
    T = TRACER if tracer is None else tracer
    if n in T:
        return [(rho, beta) for rho in T[n]]
    return [(powerlaw_rho(gamma_unmeas), beta)]


def classify(mean, z):
    if abs(z) < 2:
        return "NOT SIGNIFICANT"
    if mean < 0:
        return "REVERSED"
    return "FAIL CONFIRMED" if z >= 3 else "WEAKENED"


ORDER = ["FAIL CONFIRMED", "WEAKENED", "NOT SIGNIFICANT", "REVERSED"]

# ---- C3 Abel control (Plummer)
P("\n" + "-" * 120); P("2. CONTROLS"); P("-" * 120)
rp = abel_rho(lambda R: -4 * R * (1 + R ** 2) ** -3, RG)
mask = (RG > 0.1) & (RG < 30)
sl_num = -np.gradient(np.log(np.maximum(rp, 1e-300)), LR)[mask]
sl_an = (5 * RG ** 2 / (1 + RG ** 2))[mask]
c3 = float(np.max(np.abs(sl_num - sl_an)))
norm = float(np.median((rp / (1 + RG ** 2) ** -2.5)[mask]))
check("C3 Abel deprojection: Plummer Sigma ~ (1+R^2)^-2 -> rho ~ (1+r^2)^-5/2, log-slope within 0.01 over 0.1-30 a",
      c3 < 0.01, f"max |slope_num - slope_exact| = {c3:.2e}; normalisation ratio (exact 4/(3)/... const) median {norm:.6f}")

# ---- C1 audit baseline
base = {}
for foot in A0:
    base[foot] = stat([RES[(KM, foot)][n]["off"] for n in S16])
check("C1 audit baseline reproduced (nu_mono, gamma 3, beta 0, 16): canonical +0.0977, alt +0.0885 within 0.001 dex",
      abs(base["canonical"][0] - 0.0977) < 0.001 and abs(base["alt"][0] - 0.0885) < 0.001,
      f"canonical {base['canonical'][0]:+.4f} +- {base['canonical'][1]:.4f} ({base['canonical'][2]:.2f} sigma); alt {base['alt'][0]:+.4f} +- {base['alt'][1]:.4f} ({base['alt'][2]:.2f} sigma)")

# ---- C2 general Jeans with rho ~ r^-3, no gas, vs the audit per galaxy
c2 = {}
for foot in A0:
    c2[foot] = {n: offset(n, foot, comps=[(powerlaw_rho(3.0), 0.0)], gas=False) for n in S16}
d2 = max(abs(c2[f][n] - RES[(KM, f)][n]["off"]) for f in A0 for n in S16)
check("C2 general-profile Jeans (rho ~ r^-3, beta 0, no gas) reproduces the audit per-galaxy offsets within 0.001 dex",
      d2 < 0.001, f"max |diff| over 16 x 2 footings = {d2:.2e} dex")

# ---- C6 gas-zero path identical to C2
c6 = max(abs(offset(n, "canonical", comps=[(powerlaw_rho(3.0), 0.0)], gas=True, Mg=np.zeros_like(RG)) - c2["canonical"][n]) for n in S16)
check("C6 gas-zero (explicit zero gas array) with gamma 3 reproduces C2 exactly (<= 1e-9 dex)", c6 <= 1e-9, f"max |diff| = {c6:.2e}")

# ---- C4 internal consistency: Prugniel-Simien asymptotic slope vs numerical gamma at 3 R_e,GC
P("  C4 detail (no published power-law index for the same profiles: Kartha+14/16 quote alpha only as a symbol of the azimuthal fit) ->"
  " Prugniel-Simien fallback")
c4 = []
def ps_slope(n_, b_, x):
    p = 1 - 0.6097 / n_ + 0.05463 / n_ ** 2
    return p + b_ / n_ * x ** (1 / n_)
items = [("NGC1023 K14", TR["K14"][1023]["Re_am"][0], TR["K14"][1023]["n"][0], bn_k, 1023),
         ("NGC2768 K14", TR["K14"][2768]["Re_am"][0], TR["K14"][2768]["n"][0], bn_k, 2768),
         ("NGC3607 K16 MA", TR["K16"]["MA"]["Re_am"][0], TR["K16"]["MA"]["n"][0], bn_k, 3607),
         ("NGC3607 K16 SB", TR["K16"]["SB"]["Re_am"][0], TR["K16"]["SB"]["n"][0], bn_k, 3607)]
for j in range(3):
    items.append((f"M87 A14 pop {'bir'[j]}", TR["A14_Re_as"][j][0] / 60, TR["A14_n"][j][0], bn_cb, 4486))
items.append(("M87 Z14/Peng08", TR["Z14"]["R0_as"][0] / 60, TR["Z14"]["n"][0], lambda n_: TR["Z14"]["bn_log10"] * math.log(10), 4486))
for lab, Re_am, n_, bf, gal in items:
    Re = am2kpc(Re_am, GAL[gal]["D"]); rho = sersic_rho(Re, n_, bf(n_))
    gnum = float(np.interp(math.log(3 * Re), LR, -np.gradient(np.log(np.maximum(rho, 1e-300)), LR)))
    gps = ps_slope(n_, bf(n_), 3.0)
    c4.append(abs(gnum - gps))
    P(f"     {lab:18} R_e {Re:7.2f} kpc  n {n_:5.2f}  b {bf(n_):6.3f}  gamma(3 R_e) numerical {gnum:6.3f}  Prugniel-Simien {gps:6.3f}  diff {gnum - gps:+.3f}")
bz = TR["Z14"]["bn_log10"] * math.log(10)
P(f"     Zhu+14 b_n = 2.21 read as log10: ln-equivalent {bz:.3f} vs Ciotti-Bertin b({TR['Z14']['n'][0]}) = {bn_cb(TR['Z14']['n'][0]):.3f} (supports the log10 reading)")
check("C4 measured slopes internally consistent with the published Sersic fits (numerical gamma(3 R_e,GC) vs Prugniel-Simien within 0.15)",
      max(c4) < 0.15, f"max |diff| = {max(c4):.3f} over {len(c4)} profiles")

# ---- C5 transcription + spot values
nK14, nK16 = len(TR["K14"]), len(TR["K16"])
check("C5 transcription by script: Kartha+14 table 3 rows, Kartha+16 table 2 rows, Agnello+14 3 n + 3 R_e + 2 ratios, Forbes+17 Table 6 27 rows",
      nK14 == 3 and nK16 == 2 and len(TR["A14_n"]) == 3 and len(TR["A14_Re_as"]) == 3 and len(TR["F17_T6"]) == 27,
      f"spot values: K14 NGC 2768 R_e {TR['K14'][2768]['Re_am']} arcmin, n {TR['K14'][2768]['n']}; K16 MA R_e {TR['K16']['MA']['Re_am']}; "
      f"A14 R_e,b {TR['A14_Re_as'][0]} arcsec, Sigma_r/b {TR['A14_Srb']}; Churazov ne0 {TR['C08']['ne0']} beta {TR['C08']['beta']} rc {TR['C08']['rc_kpc']} kpc")

# ---- P1 row gap (added post-freeze; provenance only)
NGCS = NS["GCS"]
ondisk = {n: len(NGCS[n]) for n in NGCS}
nrows = sum(ondisk.values())
galN = sum(int(r["N"]) for r in NS["vizier"]("sluggs_forbes2017_galaxies.tsv") if r["NGC"].isdigit())
vz = TR["VZ_records"]; vz25 = sum(vz.get(f"table{i}", 0) for i in (2, 3, 4, 5))
mism = {n: (ondisk.get(n, 0), TR["F17_T6"][n]) for n in TR["F17_T6"] if ondisk.get(n, 0) != TR["F17_T6"][n]}
raw_rows = len(NS["vizier"]("sluggs_forbes2017_gcvel.tsv"))
P("\n  ROW GAP: galaxy-table N (VizieR ReadMe: 'Number of galaxy data in tables 2-5') sums to "
  f"{galN}; VizieR records table2 contaminants {vz.get('table2')} + table3 neighbour galaxies {vz.get('table3')} + table4 UCDs {vz.get('table4')}"
  f" + table5 GCs {vz.get('table5')} (erratum, AJ 154, 80) = {vz25}")
P(f"  on-disk velocity file: {raw_rows} data rows, {nrows} parsed GC rows keyed to the 27 galaxies; per-galaxy vs Forbes+17 Table 6 N_GC: "
  f"{27 - len(mism)}/27 equal; differences {mism}")
check("P1 (post-freeze, provenance) the 4,492 is N over Tables 2-5 (contaminants + neighbours + UCDs + GCs), not a GC count",
      galN == vz25, f"N sum {galN} == {vz25}; GCs alone {vz.get('table5')}")

# ------------------------------------------------------------------ 6. primary and subsets
P("\n" + "-" * 120); P("3. PER GALAXY (primary: measured profiles where available, gamma 3 elsewhere, isotropic, measured gas where covered)"); P("-" * 120)
PER = {}
for foot in A0:
    PER[foot] = {}
    for n in S16:
        PER[foot][n] = dict(primary=offset(n, foot, comps=comps_for(n)),
                            nogas=offset(n, foot, comps=comps_for(n), gas=False),
                            g3gas=offset(n, foot, comps=[(powerlaw_rho(3.0), 0.0)]),
                            base=RES[(KM, foot)][n]["off"])
for n in S16:
    r = PER["canonical"][n]; gi = GAS[n][1]
    rho = TRACER[n][0] if n in TRACER else powerlaw_rho(3.0)
    gam = -np.gradient(np.log(np.maximum(rho, 1e-300)), LR)
    gb = ", ".join(f"{float(np.interp(math.log(R), LR, gam)):.2f}" for R in B[n]["Rb"][B[n]["outer"]])
    P(f"   NGC{n:<5} {'MEAS' if n in TRACER else 'g=3 '} {'CENT' if n in CENTRALS else '    '} base {r['base']:+.3f}  g3+gas {r['g3gas']:+.3f}  "
      f"meas,nogas {r['nogas']:+.3f}  PRIMARY {r['primary']:+.3f}   gamma at outer bins [{gb}]  gas: {gi['src'] if gi else '-'}")
    if gi and "outer" in gi:
        P(f"            M87 gas: {gi['outer']}; Lakhchaura last point {gi['r_last']:.1f} kpc")
    if n in EXTENT:
        P(f"            GC-system extent (published) {EXTENT[n]:.1f} kpc; outermost bin {B[n]['Rb'][-1]:.1f} kpc")

SUB = {"ALL": S16, "MEASURED": [n for n in S16 if n in MEASURED], "UNMEASURED": [n for n in S16 if n not in MEASURED],
       "NO-CENTRALS": [n for n in S16 if n not in CENTRALS], "CENTRALS": [n for n in S16 if n in CENTRALS]}

# systematic variants
VAR = {}
for foot in A0:
    VAR[foot] = {}
    for lab, kw in (("g_unmeas_3.5", dict(gamma_unmeas=3.5)), ("g_unmeas_2.5", dict(gamma_unmeas=2.5)),
                    ("beta+0.5", dict(beta=0.5)), ("beta-0.5", dict(beta=-0.5))):
        VAR[foot][lab] = {n: offset(n, foot, comps=comps_for(n, **kw)) for n in S16}
    VAR[foot]["meas_delta"] = {}
    for n in MEASURED:
        dl = []
        for lab, rho in TRACER_ERR[n]:
            dl.append((lab, offset(n, foot, comps=[(rho, 0.0)]) - PER[foot][n]["primary"]))
        VAR[foot]["meas_delta"][n] = dl


def zsys(foot, names, per_key="primary", per=None):
    per = PER if per is None else per
    x = [per[foot][n][per_key] for n in names]
    m, e, z = stat(x)
    V = VAR[foot]
    sg = abs(np.mean([V["g_unmeas_3.5"][n] for n in names]) - np.mean([V["g_unmeas_2.5"][n] for n in names])) / 2
    sb = abs(np.mean([V["beta+0.5"][n] for n in names]) - np.mean([V["beta-0.5"][n] for n in names])) / 2
    dm = [max(abs(d) for _, d in V["meas_delta"][n]) for n in names if n in MEASURED]
    smeas = math.sqrt(sum(d * d for d in dm)) / len(names)
    tot = math.sqrt(e * e + sg * sg + sb * sb + smeas * smeas)
    return dict(mean=m, err_stat=e, z_stat=z, s_gamma=sg, s_beta=sb, s_meas=smeas, err_tot=tot, z_sys=m / tot,
                cls_stat=classify(m, z), cls_sys=classify(m, m / tot), N=len(names))


P("\n" + "-" * 120); P("4. STATISTICS (mean over galaxies; Z_stat = galaxy SEM; Z_sys adds shared gamma(unmeasured) +-0.5, beta +-0.5, fit errors)"); P("-" * 120)
STATS = {}
for foot in A0:
    STATS[foot] = {}
    for s, names in SUB.items():
        z = zsys(foot, names); STATS[foot][s] = z
        P(f"  {foot:9} {s:12} N={z['N']:2d}: {z['mean']:+.4f}  stat +-{z['err_stat']:.4f} (Z_stat {z['z_stat']:+.2f}, {z['cls_stat']})  | "
          f"s_gamma {z['s_gamma']:.4f} s_beta {z['s_beta']:.4f} s_meas {z['s_meas']:.4f} -> tot +-{z['err_tot']:.4f} (Z_sys {z['z_sys']:+.2f}, {z['cls_sys']})")
FRAG = {}
for foot in A0:
    z = STATS[foot]["ALL"]; e = z["err_stat"]
    no1023 = math.sqrt(sum(max(abs(d) for _, d in VAR[foot]["meas_delta"][n]) ** 2 for n in MEASURED if n != 1023)) / 16
    rows_ = {"Z_sys without s_meas": z["mean"] / math.sqrt(e ** 2 + z["s_gamma"] ** 2 + z["s_beta"] ** 2),
             "Z_sys with s_meas excluding NGC 1023 (n = 3.15 +- 2.85 -> n-1s = 0.30)": z["mean"] / math.sqrt(e ** 2 + z["s_gamma"] ** 2 + z["s_beta"] ** 2 + no1023 ** 2),
             "Z_sys without s_gamma": z["mean"] / math.sqrt(e ** 2 + z["s_beta"] ** 2 + z["s_meas"] ** 2)}
    FRAG[foot] = rows_
    for k, v in rows_.items():
        P(f"  {foot:9} REPORTED (not a decision row) ALL {k}: {v:+.2f} ({classify(z['mean'], v)})")
for foot in A0:
    P(f"  {foot:9} measured-galaxy fit-error deltas (dex): " + "; ".join(f"NGC{n} max {max(abs(d) for _, d in VAR[foot]['meas_delta'][n]):.4f}" for n in MEASURED))

# ------------------------------------------------------------------ 7. secondary S1 / S2 and reported rows
P("\n" + "-" * 120); P("5. SECONDARY (pre-stated) AND REPORTED ROWS"); P("-" * 120)
SEC = {}
for foot in A0:
    a0 = A0[foot]
    s1, s2 = {}, {}
    for n in S16:
        if n not in TRACER:
            s1[n] = PER[foot][n]["primary"]; s2[n] = PER[foot][n]["primary"]; continue
        b = B[n]; Mg = GAS[n][0]; M = calib_mass(n, a0, Mg); g = g_law(M, b["Re"] / 1.8153, a0, Mg)
        rho = TRACER[n][0]; gam = -np.gradient(np.log(np.maximum(rho, 1e-300)), LR)
        vals = []
        for R, S_, o in zip(b["Rb"], b["Sb"], b["outer"]):
            if not o:
                continue
            gi = float(np.interp(math.log(R), LR, gam))
            vals.append(math.log10(S_ / sig_los(np.array([R]), g, [(powerlaw_rho(gi), 0.0)])[0]))
        s1[n] = float(np.mean(vals))
        if n in EXTENT:
            rt = np.where(RG <= EXTENT[n], rho, 0.0)
            s2[n] = offset(n, foot, comps=[(rt, 0.0)])
        else:
            s2[n] = PER[foot][n]["primary"]
    SEC[foot] = dict(S1=s1, S2=s2)
    for lab in ("S1", "S2"):
        per = {foot: {n: {"x": SEC[foot][lab][n]} for n in S16}}
        z = zsys(foot, S16, per_key="x", per=per)
        SEC[foot][lab + "_stat"] = z
        P(f"  {foot:9} {lab} ({'local power law at each bin radius' if lab == 'S1' else 'rho truncated at the published GC-system extent'}): "
          f"{z['mean']:+.4f}  Z_stat {z['z_stat']:+.2f}  Z_sys {z['z_sys']:+.2f}  ({z['cls_sys']})")

REP = {}
for foot in A0:
    a0 = A0[foot]; R_ = {}
    R_["NGC3607 Kartha+16 SB instead of MA"] = {3607: offset(3607, foot, comps=[(k_sersic(3607, TR["K16"]["SB"]), 0.0)])}
    D87 = GAL[4486]["D"]; nz = TR["Z14"]["n"][0]
    rz = sersic_rho(am2kpc(TR["Z14"]["R0_as"][0] / 60, D87), nz, TR["Z14"]["bn_log10"] * math.log(10))
    R_["M87 Zhu+14/Peng+08 total Sersic (PROVISIONAL text)"] = {4486: offset(4486, foot, comps=[(rz, 0.0)])}
    R_["M87 Agnello+14 mixture, text beta (b 0, i +0.3, r 0) PROVISIONAL"] = {4486: offset(4486, foot, comps=[(A14[0], 0.0), (A14[1], 0.3), (A14[2], 0.0)])}
    zb = TR["Z14_beta_text"]
    bz_r = np.interp(RG, [0.0, zb["rmax"], zb["r0"], 1e9], [zb["b0"], zb["bmax"], 0.0, 0.0])
    R_["M87 Zhu+14 text beta(r) -0.2 -> +0.2 @40 kpc -> 0 @120 kpc (PROVISIONAL, linear)"] = {4486: offset(4486, foot, comps=[(TRACER[4486][0], bz_r)])}
    for mo in ("cfg57", "urban_trunc"):
        Mg, inf = gas_mass(4486, m87_outer=mo)
        R_[f"M87 gas outer = {mo}"] = {4486: offset(4486, foot, comps=comps_for(4486), Mg=Mg)}
    R_["M87 no gas"] = {4486: PER[foot][4486]["nogas"]}
    REP[foot] = R_
    # CFG57's mechanical frozen gas rule (outermost upturned shell kept) for every Lakhchaura galaxy -- reported, known unbounded
    xs = []
    for m in S16:
        if m in SRC1:
            Mg, _ = gas_mass(m, m87_outer="cfg57", drop_last=False); xs.append(offset(m, foot, comps=comps_for(m), Mg=Mg))
        else:
            xs.append(PER[foot][m]["primary"])
    mm, ee, zz = stat(xs)
    P(f"  {foot:9} {'Lakhchaura upturned last shell KEPT (CFG57 mechanical rule; unbounded gas)':78}: ALL {mm:+.4f} Z_stat {zz:+.2f}  per: " +
      ", ".join(f"NGC{m} {x:+.2f}" for m, x in zip(S16, xs) if m in SRC1))
    for k, v in R_.items():
        n = list(v)[0]; xs = [v[n] if m == n else PER[foot][m]["primary"] for m in S16]
        m, e, z = stat(xs)
        P(f"  {foot:9} {k:78}: NGC{n} {v[n]:+.3f} (primary {PER[foot][n]['primary']:+.3f}) -> ALL {m:+.4f} Z_stat {z:+.2f}")
    xs = [PER[foot][n]["nogas"] for n in S16]; m, e, z = stat(xs)
    P(f"  {foot:9} {'all galaxies without gas (measured slopes only)':78}: ALL {m:+.4f} Z_stat {z:+.2f}")
    xs = [PER[foot][n]["g3gas"] for n in S16]; m, e, z = stat(xs)
    P(f"  {foot:9} {'gamma 3 everywhere, measured gas only':78}: ALL {m:+.4f} Z_stat {z:+.2f}")

# ------------------------------------------------------------------ 8. verdict
P("\n" + "-" * 120); P("6. VERDICT (decision rule (e) on Z_sys of ALL; headline = the weaker class over the two footings)"); P("-" * 120)
cl = {f: STATS[f]["ALL"]["cls_sys"] for f in A0}
verdict = max(cl.values(), key=lambda c: ORDER.index(c)) if "REVERSED" not in cl.values() else ("REVERSED" if all(v == "REVERSED" for v in cl.values()) else "NOT SIGNIFICANT")
cov = sum(1 for n in S16 if n in TRACER)
vtxt = verdict + (f"  [MEASURED-TRACER COVERAGE {cov}/16]" if cov < 3 else f"  [measured-tracer coverage {cov}/16]")
P(f"  canonical: {cl['canonical']} (Z_sys {STATS['canonical']['ALL']['z_sys']:+.2f}); alt: {cl['alt']} (Z_sys {STATS['alt']['ALL']['z_sys']:+.2f})")
P(f"  VERDICT: {vtxt}")
for foot in A0:
    if SEC[foot]["S1_stat"]["cls_sys"] != STATS[foot]["ALL"]["cls_sys"]:
        P(f"  PRIMARY/S1 DISAGREE ({foot}): primary {STATS[foot]['ALL']['cls_sys']} vs S1 {SEC[foot]['S1_stat']['cls_sys']}")
P(f"  centrals split (not the headline): NO-CENTRALS canonical {STATS['canonical']['NO-CENTRALS']['mean']:+.4f} Z_sys {STATS['canonical']['NO-CENTRALS']['z_sys']:+.2f} "
  f"({STATS['canonical']['NO-CENTRALS']['cls_sys']}), alt Z_sys {STATS['alt']['NO-CENTRALS']['z_sys']:+.2f} ({STATS['alt']['NO-CENTRALS']['cls_sys']}); "
  f"CENTRALS canonical {STATS['canonical']['CENTRALS']['mean']:+.4f} Z_stat {STATS['canonical']['CENTRALS']['z_stat']:+.2f}")

# ------------------------------------------------------------------ 9. MUTATE check
if MUTATE:
    P("\n" + "-" * 120); P("7. MUTATE CHECK"); P("-" * 120)
    um = {}
    for foot in A0:
        um[foot] = np.mean([offset(n, foot, comps=[(rho, 0.0) for rho in UNMUT[n]]) for n in MEASURED])
    dm_ = {f: STATS[f]["MEASURED"]["mean"] - um[f] for f in A0}
    jm = os.path.join(HERE, "cfg323_measured_tracers_results.json")
    cls_main = None
    if os.path.exists(jm):
        cls_main = json.load(open(jm)).get("verdict_class")
    changed = (cls_main is not None and cls_main != verdict)
    ok = abs(dm_["canonical"]) >= 0.01 or changed
    P(f"  MEASURED-subset mean: shuffled {STATS['canonical']['MEASURED']['mean']:+.4f} vs unshuffled {um['canonical']:+.4f} (canonical; delta {dm_['canonical']:+.4f}); "
      f"alt delta {dm_['alt']:+.4f}; verdict class main run {cls_main} vs shuffled {verdict}")
    if not ok:
        P("  MUTATE INSENSITIVE")
    check("M1 MUTATE: shuffling the measured profiles moves the MEASURED-subset mean by >= 0.01 dex or changes the verdict class",
          ok, f"delta canonical {dm_['canonical']:+.4f}, class change {changed}")

npass = sum(1 for _, c in checks if c)
P(f"\n  {npass}/{len(checks)} checks pass")
res = dict(lane="CFG323", mutate=MUTATE, frozen_commit="b2e7ec16d", kernel=KM, kappa=0.5, a0=A0,
           measured=[n for n in S16 if n in TRACER], centrals=CENTRALS,
           baseline={f: base[f] for f in A0},
           per_galaxy={f: {str(n): PER[f][n] for n in S16} for f in A0},
           stats=STATS, secondary={f: {k: (v if k.endswith("_stat") else {str(n): x for n, x in v.items()}) for k, v in SEC[f].items()} for f in A0},
           reported={f: {k: {str(n): x for n, x in v.items()} for k, v in REP[f].items()} for f in A0},
           meas_fit_deltas={f: {str(n): VAR[f]["meas_delta"][n] for n in MEASURED} for f in A0},
           verdict=vtxt, verdict_class=verdict, fragility=FRAG, verdict_by_footing=cl,
           row_gap=dict(N_sum=galN, vizier_records=vz, ondisk_rows=raw_rows, parsed_gc_rows=nrows, table6_mismatch={str(k): v for k, v in mism.items()}),
           transcribed={k: v for k, v in TR.items() if k != "F17_T6"},
           checks=[dict(label=l, passed=c) for l, c in checks], n_pass=npass, n_checks=len(checks))
json.dump(res, open(os.path.join(HERE, f"cfg323_measured_tracers{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg323_measured_tracers{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(checks) else 1)
