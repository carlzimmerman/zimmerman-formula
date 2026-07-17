#!/usr/bin/env python3
"""
est_marg.py -- THE MARGINALIZED-NUISANCE LANE for the a0-line M/L (Upsilon) wall.

Framework (its OWN terms): modified-INERTIA, horizon-derived a0=cH_L/Z, its own
dS-Unruh interpolation g_obs=sqrt(g_bar^2 + g_bar*a0). Squaring => the through-origin
identity  E = g_obs^2 - g_bar^2 = a0*g_bar.  Kernel credit: nu=sqrt(1+1/y) is
Milgrom 1999 PLA 253:273 Eq.9; the distinctive content is the cH_L/Z coefficient +
the MI completion. SPARC = Lelli-McGaugh-Schombert 2016. SPS M/L decomposition:
Schombert-McGaugh-Lelli 2019, Meidt+2014, McGaugh-Schombert 2014, Bell-de Jong 2001.

THE QUESTION (this lane): the QUADRATURE budget (fire_common) adds the coherent
Upsilon uncertainty as an error bar sysU = KU*a0*sig_lnU IN QUADRATURE. That
ASSUMES the coherent Upsilon shift is a PERFECT clone of an a0 shift (fully
degenerate, no self-calibration). Here we instead treat the coherent Upsilon SPS
zero-point as a NUISANCE PARAMETER alpha (log-Upsilon offset, same for every
galaxy) marginalized in a proper Bayesian a0-line fit, with the per-galaxy
external color/SPS priors entering as DATA (reduced per-galaxy prior width).

  KEY: is the coherent Upsilon zero-point DEGENERATE with a0? A coherent Upsilon
  shift moves g_bar by  d g_bar/d ln U = phi*g_bar  (phi = stellar share). Its
  effect on the residual r = E - a0*g_bar is
        dr/d(lnU) = -(2 g_bar + a0) * phi * g_bar  =: -U_i
  vs the a0 direction dr/da0 = -g_bar =: -g_i.  These are degenerate iff U_i is
  proportional to g_i across the sample, i.e. iff  phi_i*(2 g_bar_i + a0)  is
  ~constant. On gas-dom dwarfs (phi small, g_bar<<a0 so 2g_bar+a0~a0) U_i ~ a0*phi_i*g_i,
  so the degeneracy is controlled by how much phi VARIES with g_bar. We quantify
  the a0-alpha posterior covariance and ask: does marginalizing WIDEN or TIGHTEN
  a0 vs the quadrature error bar?

EXACT identity used (proved in header of the RESULTS): marginalizing a global
Gaussian template U with prior variance s^2 is IDENTICAL to GLS through the origin
with data covariance  C = diag(sig2_i) + s^2 * U U^T  (template marginalization /
Sherman-Morrison). Per-galaxy Upsilon offsets beta_k (reducible, external priors)
add block-rank-1 terms s_pg^2 * U_k U_k^T. Gas-cal is a SECOND global template G.

Reuses ../a0_line/fire_common.py READ-ONLY for data load + cuts + the honest
model-based weights w=1/sig2 (the guard that caught the fake 3.3e-11 obs-weight
deficit). Writes ONLY to a0_line_mlpriors/. Exit 0. Not a verdict; a measurement.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, "/Users/carlzimmerman/new_physics/prep_2026/a0_line")
import fire_common as fc

OUT = "/Users/carlzimmerman/new_physics/prep_2026/a0_line_mlpriors"
A0C, A0A = fc.A0C, fc.A0A          # canonical 9.355e-11 (cH_L/Z) / ALT 1.1305e-10 (cH0/Z)
SC, SA = fc.SC, fc.SA              # Planck anchor widths
LN10 = np.log(10.0)
HQ = {2, 3}                        # TRGB + Cepheid distance flags

# ---- Upsilon-uncertainty DECOMPOSITION (dex), literature-defensible ----
# current global fire_common SIG_LNU = 0.23 nat = 0.10 dex is split into a
# COHERENT SPS/IMF zero-point floor (irreducible) + a PER-GALAXY relative part
# (reducible with external per-galaxy color/SPS M/L). sqrt(coh^2+pg_pre^2)~=0.10 dex
# recovers the current global width. External priors shrink pg_pre -> pg_res.
SIG_COH_SCEN = {"optimistic": 0.05, "fiducial": 0.06, "nir_realistic": 0.075}  # dex
SIG_PG_PRE = 0.080      # dex, per-galaxy BEFORE external priors (SML19-scatter scale)
SIG_PG_RES = 0.037      # dex, per-galaxy AFTER external [3.6]+color SPS priors (~1/sqrt-averaged)
SIG_GAS = 0.10          # NAT (fire_common SIG_LNG=0.10 nat ~=0.043 dex); NOT dex -> no *LN10

con = []
def p(s=""):
    con.append(s); print(s)


# ---------- Occam bans (VERBATIM shape of fire_occam / verify_trgb) ----------
def logB_logflat(a0hat, tot, astar, s_anchor, lo=1e-11, hi=1e-9):
    """log10 Bayes factor M0(a0==astar)/M1(log-flat prior). +bans => favor anchor.
    Returns (bans, t_sigma). t_sigma is the convention-ROBUST tension number."""
    xhat = np.log(a0hat); s_meas = tot / a0hat; s_anch = s_anchor / astar
    xg = np.linspace(np.log(lo), np.log(hi), 200001)
    s_eff = np.hypot(s_meas, s_anch)
    lnZ0 = -0.5 * ((np.log(astar) - xhat) / s_eff) ** 2 - np.log(np.sqrt(2 * np.pi) * s_eff)
    Lx = np.exp(-0.5 * ((xg - xhat) / s_meas) ** 2) / (np.sqrt(2 * np.pi) * s_meas)
    lnZ1 = np.log(np.trapz(Lx / (np.log(hi) - np.log(lo)), xg))
    return float((lnZ0 - lnZ1) / LN10), float((np.log(astar) - xhat) / s_eff)


def logB_linflat(a0hat, tot, astar, s_anchor, lo=1e-11, hi=1e-9, n=8000):
    """Prior-sensitivity control: LINEAR-flat prior. Ban value differs => bans are
    convention-fragile; the sigma tension is the robust number."""
    grid = np.linspace(lo, hi, n); s_eff = np.hypot(tot, s_anchor)
    m0 = np.exp(-0.5 * ((a0hat - astar) / s_eff) ** 2) / (np.sqrt(2 * np.pi) * s_eff)
    like = np.exp(-0.5 * ((a0hat - grid) / tot) ** 2) / (np.sqrt(2 * np.pi) * tot)
    m1 = np.trapz(like / (hi - lo), grid)
    return float(np.log10(m0 / m1))


# ---------- flat arrays for a galaxy subset (gas-dom points) ----------
def flatten(gals, fD_in=None):
    GB, GO, FV, PHI, GAL = [], [], [], [], []
    for g in gals:
        if fD_in is not None and g["fD"] not in fD_in:
            continue
        m = g["gasdom"]
        n = int(m.sum())
        if n == 0:
            continue
        GB += list(g["gb"][m]); GO += list(g["go"][m]); FV += list(g["fv"][m])
        PHI += list(g["phi"][m]); GAL += [g["name"]] * n
    return (np.array(GB), np.array(GO), np.array(FV), np.array(PHI),
            np.array(GAL, dtype=object))


def gls_weights(GB, GO, FV):
    """Honest model-based iterated GLS (fire_common.gls, biased=False): a0hat, fint,
    and per-point weights w=1/sig2 (NO Upsilon in sig2 -- Upsilon is a parameter here)."""
    a0, fint, c2n, w = fc.gls(GB, GO, FV, biased=False)
    return float(a0), float(fint), float(c2n), np.asarray(w)


def analyze(gals, fD_in, label):
    GB, GO, FV, PHI, GAL = flatten(gals, fD_in)
    if len(GB) < 10:
        return None
    a0, fint, c2n, w = gls_weights(GB, GO, FV)
    E = GO ** 2 - GB ** 2
    names = sorted(set(GAL.tolist()))
    Ngal = len(names)

    # design columns (all POSITIVE by construction; sign folded into derivation)
    g = GB.copy()                                   #  dr/da0 = -g_i
    U = PHI * GB * (2 * GB + a0)                     #  -dr/dlnU_coherent = U_i
    Gt = (1 - PHI) * GB * (2 * GB + a0)              #  -dr/dln(gascal)  = G_i  (2nd global template)

    S = np.sum(w * g * g)                            # = g^T W g   (fire_common S)
    gWU = np.sum(w * g * U)                          # = g^T W U
    gWG = np.sum(w * g * Gt)
    KU = gWU / (a0 * S)                              # must equal fire_common KU
    KG = gWG / (a0 * S)
    UWU = np.sum(w * U * U)
    GWG = np.sum(w * Gt * Gt)

    var_stat = 1.0 / S                               # pure statistical (=fire_common stat^2)

    # ---------- (A) 2x2 marginal (a0, alpha_coh): the DEGENERACY answer ----------
    # Fisher F = [[g^TWg, g^TWU],[U^TWg, U^TWU + 1/s_coh^2]] ; cov = F^{-1}
    twobytwo = {}
    for scen, sc_dex in SIG_COH_SCEN.items():
        s_coh = sc_dex * LN10                         # dex -> nat
        F = np.array([[S, gWU], [gWU, UWU + 1.0 / s_coh ** 2]])
        cov = np.linalg.inv(F)
        var_a0_marg2 = cov[0, 0]
        rho = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
        var_a0_quad2 = var_stat + (a0 * KU * s_coh) ** 2      # quadrature (fire_common) stat+sysU_coh
        twobytwo[scen] = dict(
            s_coh_dex=sc_dex, rho_a0_alpha=float(rho),
            sig_a0_marg=float(np.sqrt(var_a0_marg2)),
            sig_a0_quad=float(np.sqrt(var_a0_quad2)),
            marg_over_quad=float(np.sqrt(var_a0_marg2 / var_a0_quad2)),
            sU_coh_quad=float(a0 * KU * sc_dex * LN10))

    # ---------- (B) FULL covariance marginalization (data-space GLS) ----------
    # C = diag(sig2) + s_coh^2 U U^T + s_gas^2 G G^T + s_pg^2 sum_k U_k U_k^T
    # a0hat_marg = (g^T C^{-1} E)/(g^T C^{-1} g); var = 1/(g^T C^{-1} g).
    sig2 = 1.0 / w
    # per-galaxy index membership (for the reducible per-galaxy Upsilon blocks)
    gidx = {nm: (GAL == nm) for nm in names}

    def full_marg(s_coh_dex, s_pg_dex, include_gas=True):
        s_coh = s_coh_dex * LN10; s_pg = s_pg_dex * LN10; s_gas = SIG_GAS  # gas-cal already nat
        C = np.diag(sig2).astype(float)
        C += s_coh ** 2 * np.outer(U, U)                       # global coherent Upsilon
        if include_gas:
            C += s_gas ** 2 * np.outer(Gt, Gt)                 # global coherent gas-cal
        for nm in names:                                       # per-galaxy reducible Upsilon
            mk = gidx[nm]
            Uk = np.where(mk, U, 0.0)
            C += s_pg ** 2 * np.outer(Uk, Uk)
        Cig = np.linalg.solve(C, g)
        CiE = np.linalg.solve(C, E)
        denom = float(g @ Cig)
        a0m = float((g @ CiE) / denom)
        var = 1.0 / denom
        return a0m, float(np.sqrt(var))

    # ---------- (C) assemble TOTAL error: marg(Upsilon coh+pg[+gas]) (x) sysD,sysI,sysEst ----------
    bud = fc.budget(gals if fD_in is None else [gg for gg in gals if gg["fD"] in fD_in],
                    gas_only=True)
    sysD, sysI, sysEst = bud["sysD"], bud["sysI"], bud["sysEst"]
    sysU_quad, sysG_quad = bud["sysU"], bud["sysG"]
    a0_bud, tot_quad = bud["a0hat"], bud["tot"]
    a0_med = bud["a0med"]

    results = {}
    for scen, sc_dex in SIG_COH_SCEN.items():
        row = {}
        # marginal a0 error from Upsilon (coh + per-galaxy), gas-cal NOT yet marginalized
        for tag, s_pg in (("pg_pre", SIG_PG_PRE), ("pg_res", SIG_PG_RES)):
            a0m_U, sig_U = full_marg(sc_dex, s_pg, include_gas=False)
            # this sig_U already contains stat (x) marg(Upsilon). add sysD,I,Est,G(quad):
            tot_Uquad = float(np.hypot.reduce([sig_U, sysD, sysI, sysEst, sysG_quad]))
            # fully-marginalized variant: gas-cal ALSO a marginalized global template
            a0m_UG, sig_UG = full_marg(sc_dex, s_pg, include_gas=True)
            tot_UG = float(np.hypot.reduce([sig_UG, sysD, sysI, sysEst]))
            row[tag] = dict(
                a0hat_marg=a0m_U, sig_from_UpsMarg=sig_U, tot_gascalQuad=tot_Uquad,
                a0hat_margUG=a0m_UG, sig_from_UGmarg=sig_UG, tot_gascalMarg=tot_UG)
        results[scen] = row

    return dict(
        label=label, Ngal=Ngal, Npts=int(len(GB)),
        a0hat=a0, a0med=a0_med, fint=fint, chi2N=c2n,
        KU=float(KU), KG=float(KG), phibar=float(np.sum(w * g * g * PHI) / S / 1.0),
        var_stat=float(var_stat), sig_stat=float(np.sqrt(var_stat)),
        sysD=sysD, sysI=sysI, sysEst=sysEst, sysU_quad=sysU_quad, sysG_quad=sysG_quad,
        tot_quad_budget=tot_quad,
        twobytwo=twobytwo, full=results)


# ============================== DRIVE ==============================
p("=" * 82)
p("MARGINALIZED-NUISANCE LANE -- coherent Upsilon SPS zero-point as a nuisance param")
p(f"footings: canonical={A0C:.4e} (cH_L/Z)  ALT={A0A:.4e} (cH0/Z)  gap={100*(A0A/A0C-1):.1f}%")
p(f"footing 2-sigma split target |Delta|/2 = {0.5*abs(A0A-A0C):.3e}")
p(f"Upsilon decomp (dex): coherent SPS floor {SIG_COH_SCEN} ; per-galaxy pre={SIG_PG_PRE}"
  f" -> res={SIG_PG_RES} (external [3.6]+color SPS); gas-cal={SIG_GAS}")
p("credit: Schombert-McGaugh-Lelli 2019, Meidt+2014, McGaugh-Schombert 2014, "
  "Bell-de Jong 2001, LMS 2016. Kernel = Milgrom 1999 Eq.9.")
p("=" * 82)

SETS = [("full_gas", None), ("TRGB", HQ)]
allres = {}
for Ud in (0.5, 0.7):
    gals = fc.load(Ud)
    allres[str(Ud)] = {}
    p(f"\n{'#'*78}\n## Ud = {Ud} (disk M/L; bulge 1.4*Ud) "
      f"{'[BANKED HEADLINE]' if Ud == 0.7 else '[fiducial]'}")
    for sname, fD in SETS:
        r = analyze(gals, fD, sname)
        if r is None:
            continue
        allres[str(Ud)][sname] = r
        p(f"\n  --- {sname}: N={r['Npts']}pts / {r['Ngal']}gal | a0hat(GLS)={r['a0hat']*1e10:.3f}"
          f"  a0med={r['a0med']*1e10:.3f}e-10  chi2/N={r['chi2N']:.2f} ---")
        p(f"      KU={r['KU']:.4f} (Upsilon lever)  KG={r['KG']:.4f} (gas lever)  "
          f"sig_stat={r['sig_stat']*1e12:.2f}e-12")
        p(f"      quadrature budget: sysU={r['sysU_quad']*1e12:.2f} sysG={r['sysG_quad']*1e12:.2f}"
          f" sysD={r['sysD']*1e12:.2f} sysI={r['sysI']*1e12:.2f} sysEst={r['sysEst']*1e12:.2f}"
          f" -> tot={r['tot_quad_budget']*1e12:.2f}e-12")

        p("      (A) a0 <-> coherent-Upsilon-zeropoint DEGENERACY (2x2 marginal):")
        for scen, t in r["twobytwo"].items():
            p(f"          sig_coh={t['s_coh_dex']:.3f}dex: rho(a0,alpha)={t['rho_a0_alpha']:+.4f}"
              f"  sig_a0[marg]={t['sig_a0_marg']*1e12:.2f} vs [quad]={t['sig_a0_quad']*1e12:.2f}e-12"
              f"  (marg/quad={t['marg_over_quad']:.3f})")

        p("      (B/C) FULL marginal totals (Upsilon coh+per-gal; gas-cal quad vs marg):")
        for scen in SIG_COH_SCEN:
            for tag in ("pg_pre", "pg_res"):
                f = r["full"][scen][tag]
                p(f"          [{scen:13s}/{tag}] a0m={f['a0hat_marg']*1e10:.3f}e-10 "
                  f"sig(UpsMarg)={f['sig_from_UpsMarg']*1e12:.2f}  "
                  f"tot(gasQuad)={f['tot_gascalQuad']*1e12:.2f}  "
                  f"tot(gasMarg)={f['tot_gascalMarg']*1e12:.2f}e-12")

# ============================== FOOTING BANS ==============================
p(f"\n{'='*82}\nFOOTING DECIDABILITY under the marginalized totals (both footings)")
p("using nir_realistic coherent floor + external per-galaxy priors (pg_res); "
  "central = GLS a0hat (carry the declining-a0/nu-shape caveat).")
p("=" * 82)
foot = {}
for Ud in ("0.5", "0.7"):
    foot[Ud] = {}
    for sname in ("full_gas", "TRGB"):
        r = allres[Ud].get(sname)
        if r is None:
            continue
        a0h = r["a0hat"]
        # binding realistic total: coherent SPS floor 0.075 dex, external per-galaxy priors, gas-cal marginalized
        tot = r["full"]["nir_realistic"]["pg_res"]["tot_gascalMarg"]
        # also the fiducial-floor variant (0.06 dex) for the optimistic edge
        tot_fid = r["full"]["fiducial"]["pg_res"]["tot_gascalMarg"]
        bans = {}
        for lbl, tt in (("nir_realistic", tot), ("fiducial_floor", tot_fid)):
            bc, tc = logB_logflat(a0h, tt, A0C, SC)
            ba, ta = logB_logflat(a0h, tt, A0A, SA)
            bcl = logB_linflat(a0h, tt, A0C, SC); bal = logB_linflat(a0h, tt, A0A, SA)
            sep = abs(bc - ba)
            bans[lbl] = dict(tot=tt, canon_ban=bc, canon_sig=tc, alt_ban=ba, alt_sig=ta,
                             canon_ban_lin=bcl, alt_ban_lin=bal, sep_ban=sep,
                             decisive_2ban=bool(sep >= 2.0),
                             two_sigma_split=bool(abs(tc) >= 2.0 or abs(ta) >= 2.0))
        foot[Ud][sname] = dict(a0hat=a0h, bans=bans)
        b = bans["nir_realistic"]
        p(f"\n  Ud={Ud} {sname}: a0hat={a0h*1e10:.3f}e-10  tot(realistic)={b['tot']*1e12:.2f}e-12"
          f" ({100*b['tot']/a0h:.1f}%)")
        p(f"     log-flat: canon {b['canon_ban']:+.2f} ban ({b['canon_sig']:+.2f}s) | "
          f"alt {b['alt_ban']:+.2f} ban ({b['alt_sig']:+.2f}s) | sep {b['sep_ban']:.2f} ban")
        p(f"     lin-flat: canon {b['canon_ban_lin']:+.2f} | alt {b['alt_ban_lin']:+.2f} "
          f"(prior-sensitivity control)")
        p(f"     -> {'DECIDES (>=2 ban & a footing >2s from other)' if (b['decisive_2ban'] and b['two_sigma_split']) else 'NON-DECISIVE (<2 ban sep)'}")

allres["_footing"] = foot
allres["_meta"] = dict(
    A0C=A0C, A0A=A0A, sig_coh_scen=SIG_COH_SCEN, sig_pg_pre=SIG_PG_PRE,
    sig_pg_res=SIG_PG_RES, sig_gas=SIG_GAS,
    split_target=0.5 * abs(A0A - A0C))

json.dump(allres, open(os.path.join(OUT, "est_marg_results.json"), "w"), indent=1, default=float)
open(os.path.join(OUT, "_marg_console.txt"), "w").write("\n".join(con))
p(f"\n{'='*82}\n[est_marg_results.json + _marg_console.txt written to a0_line_mlpriors/]  EXIT 0")
p("NOT a verdict. a0 value + s=-1 remain postulates. per-point a0=E/g_bar DECLINES "
  "with g_bar (nu-shape leaking into magnitude) -- box straddles BOTH footings.")
